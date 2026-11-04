import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from hive.decision import record, verify
from hive.review import ROOT, Meta, review, render
from test_hive import FakeModel


class ReleaseTests(unittest.TestCase):
    def test_semantic_fixture_does_not_claim_ai_detection(self):
        for case in ('semantic_conflict', 'semantic_clear'):
            r = review(ROOT / 'fixtures' / case)
            self.assertEqual(r['status'], 'ALLOW')
            self.assertFalse(r['challenge']['performed'])
            self.assertIn('does not evaluate meaning', render([r]))

    def test_semantic_concern_with_two_sources(self):
        sources = []
        for role, line in [('invoice', 9), ('installation', 10)]:
            text = (ROOT / 'fixtures/semantic_conflict' / (role + '.txt')).read_text()
            sources.append({'role': role, 'line': line, 'quote': text.splitlines()[line-1]})
        model = FakeModel(challenge={'concerns': [{'detail': 'Completion claim conflicts with incomplete commissioning.', 'sources': sources}]})
        r = review(ROOT / 'fixtures/semantic_conflict', model)
        self.assertEqual(r['status'], 'REVIEW')
        self.assertEqual([f['rule'] for f in r['findings']], ['R04'])
        self.assertEqual(len(r['findings'][0]['sources']), 2)
        self.assertTrue(r['challenge']['performed'])
        self.assertIn('Contradictor proposal', render([r]))

    def test_uncited_concern_blocks(self):
        model = FakeModel(challenge={'concerns': [{'detail': 'Unproven', 'sources': []}]})
        self.assertEqual(review(ROOT / 'fixtures/coherent', model)['status'], 'BLOCK')

    def test_decision_preserves_original_and_detects_changed_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'original.json'
            r = review(ROOT / 'fixtures/contradictory')
            raw = json.dumps(r).encode();p.write_bytes(raw)
            folder = record(p, 'REQUEST_CHANGES', 'Reviewer', 'Please resolve quantity difference.')
            self.assertEqual(p.read_bytes(), raw)
            self.assertEqual(verify(folder)['decision'], 'REQUEST_CHANGES')
            self.assertIn('REQUEST_CHANGES', (folder / 'report.html').read_text())
            (folder / 'source-report.json').write_bytes(raw + b' ')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                verify(folder)

    def test_human_cannot_approve_block_or_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'original.json'
            for status in ('BLOCK', 'REVIEW'):
                p.write_text(json.dumps({'status': status, 'human_decision': 'PENDING'}))
                with self.assertRaisesRegex(ValueError, 'requires ALLOW'):
                    record(p, 'APPROVE', 'Reviewer', 'Reviewed')
            self.assertFalse((p.parent / 'decisions').exists())

    def test_approval_is_separate_and_html_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'original.json'
            p.write_text(json.dumps(review(ROOT / 'fixtures/coherent')))
            folder = record(p, 'APPROVE', '<script>actor</script>', '<img src=x onerror=alert(1)>')
            self.assertEqual(verify(folder)['decision'], 'APPROVE')
            self.assertNotIn('<script>', (folder / 'report.html').read_text())
            self.assertNotIn('<img ', (folder / 'report.html').read_text())

    def test_meta_rejects_incomplete_and_invalid_json_without_retry(self):
        for status, output in [('incomplete', '{}'), ('completed', 'not json')]:
            adapter = object.__new__(Meta)
            adapter.calls, adapter.audit = 0, []
            response = SimpleNamespace(id='test', model='test', status=status, usage=None, output_text=output)
            create = Mock(return_value=response)
            adapter.client = SimpleNamespace(responses=SimpleNamespace(create=create))
            with self.assertRaises(ValueError):
                adapter('instructions', {})
            self.assertEqual(adapter.calls, 1)
            self.assertEqual(create.call_count, 1)
            self.assertFalse(create.call_args.kwargs['store'])
