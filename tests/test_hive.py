import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hive.review import ROOT, fixture_extract, render, review, Meta


class FakeModel:
    def __init__(self, mutate=None, challenge=None):
        self.calls = 0
        self.mutate = mutate
        self.challenge = challenge or {'concerns': []}

    def __call__(self, instructions, payload):
        self.calls += 1
        if self.calls == 2:
            return self.challenge
        data = fixture_extract(payload)
        if self.mutate:
            self.mutate(data)
        return data


class HiveTests(unittest.TestCase):
    def run_case(self, case='coherent', model=None):
        return review(ROOT / 'fixtures' / case, model)

    def test_fixture_outcomes_and_no_network(self):
        with patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            for case, expected in [('coherent','ALLOW'), ('incomplete','REVIEW'), ('contradictory','REVIEW')]:
                r = self.run_case(case)
                self.assertEqual(r['status'], expected)
                self.assertFalse(r['meta_called'])
                self.assertEqual(r['human_decision'], 'PENDING')

    def test_distinct_document_hashes(self):
        self.assertEqual(len({s['sha256'] for s in self.run_case()['sources'].values()}), 3)

    def test_two_stage_success(self):
        model = FakeModel()
        self.assertEqual(self.run_case(model=model)['status'], 'ALLOW')
        self.assertEqual(model.calls, 2)

    def test_invented_quote_blocks_before_second_call(self):
        model = FakeModel(lambda d: d['documents']['quote']['quantity'].update(quote='Quantity: 999'))
        self.assertEqual(self.run_case(model=model)['status'], 'BLOCK')
        self.assertEqual(model.calls, 1)

    def test_correct_citation_wrong_value_blocks(self):
        model = FakeModel(lambda d: d['documents']['quote']['quantity'].update(value=999))
        self.assertEqual(self.run_case(model=model)['status'], 'BLOCK')

    def test_boolean_quantity_blocks(self):
        model = FakeModel(lambda d: d['documents']['quote']['quantity'].update(value=True))
        self.assertEqual(self.run_case(model=model)['status'], 'BLOCK')

    def test_unknown_field_requires_review(self):
        model = FakeModel(lambda d: d['documents']['quote'].update(item=None))
        self.assertEqual(self.run_case(model=model)['status'], 'REVIEW')

    def test_model_cannot_clear_local_conflict(self):
        self.assertEqual(self.run_case('contradictory', FakeModel())['status'], 'REVIEW')

    def test_challenger_can_escalate(self):
        model = FakeModel(challenge={'concerns': [{'detail': 'Inspect this quantity.', 'role': 'quote', 'line': 6, 'quote': 'Quantity: 100'}]})
        self.assertEqual(self.run_case(model=model)['status'], 'REVIEW')

    def test_challenger_fabricated_source_blocks(self):
        model = FakeModel(challenge={'concerns': [{'detail': 'Concern', 'role': 'missing', 'line': 1, 'quote': 'x'}]})
        self.assertEqual(self.run_case(model=model)['status'], 'BLOCK')

    def test_model_exception_is_redacted(self):
        def fail(*args):
            raise RuntimeError('SECRET-TOKEN-123')
        result = self.run_case(model=fail)
        self.assertEqual(result['status'], 'BLOCK')
        self.assertNotIn('SECRET-TOKEN-123', str(result))

    def test_empty_dossier_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(review(Path(folder))['status'], 'BLOCK')

    def test_oversized_source_blocks_without_inference(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'quote.txt').write_text('x'*20001)
            model = FakeModel()
            self.assertEqual(review(Path(folder), model)['status'], 'BLOCK')
            self.assertEqual(model.calls, 0)

    def test_html_escapes_source_content(self):
        result = copy.deepcopy(self.run_case())
        result['sources']['quote']['text'] = '<script>alert(1)</script>'
        page = render([result])
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)

    def test_meta_budget_is_enforced_without_sdk(self):
        adapter = object.__new__(Meta)
        adapter.calls = 2
        with self.assertRaisesRegex(ValueError, 'budget'):
            adapter('', {})

    def test_wrong_field_label_blocks(self):
        model = FakeModel(lambda d: d['documents']['quote'].update(item=d['documents']['quote']['case_id']))
        self.assertEqual(self.run_case(model=model)['status'], 'BLOCK')


if __name__ == '__main__':
    unittest.main()
