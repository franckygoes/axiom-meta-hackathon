import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from hive.evidence import collect, RUNS
from hive.decision import record


class EvidenceTests(unittest.TestCase):
    def test_collect_preserves_failure_without_network_or_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.env').write_text('SECRET_MUST_NOT_BE_PACKAGED')
            for folder, case in RUNS:
                path = root / 'outputs' / folder
                path.mkdir(parents=True)
                report = {'case': case, 'mode': 'META_LIVE', 'meta_called': True,
                          'status': 'BLOCK' if folder == 'meta-incomplete' else 'REVIEW',
                          'sources': {}, 'findings': [], 'audit': [
                              {'status': 'completed', 'usage': {'input_tokens': 2, 'output_tokens': 3}}]}
                (path / (case + '.json')).write_text(json.dumps(report))
            with patch('socket.socket', side_effect=AssertionError('Network forbidden')):
                destination, archive, manifest = collect(root)
            self.assertTrue(manifest['complete'])
            self.assertEqual(manifest['runs'][2]['status'], 'BLOCK')
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(len(bundle.namelist()), 6)
                self.assertNotIn('.env', bundle.namelist())
                original = root / 'outputs/meta-incomplete/incomplete.json'
                self.assertEqual(bundle.read('meta-incomplete/incomplete.json'), original.read_bytes())
            self.assertTrue((destination / 'report.html').is_file())

    def test_matching_human_decision_is_archived(self):
        from hive.review import ROOT, review
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'outputs/meta-coherent/coherent.json'
            path.parent.mkdir(parents=True)
            result = review(ROOT / 'fixtures/coherent')
            # Synthetic test data, never a real API run.
            result.update(mode='META_LIVE', meta_called=True,
                          audit=[{'status': 'completed', 'usage': {'input_tokens': 1, 'output_tokens': 2}}])
            path.write_text(json.dumps(result))
            record(path, 'APPROVE', 'Test reviewer', 'Synthetic decision test')
            _, archive, manifest = collect(root)
            self.assertFalse(manifest['complete'])
            with zipfile.ZipFile(archive) as bundle:
                decisions = [n for n in bundle.namelist() if n.endswith('/decision.json')]
                self.assertEqual(len(decisions), 1)
                self.assertEqual(json.loads(bundle.read(decisions[0]))['decision'], 'APPROVE')

    def test_empty_collection_does_not_claim_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'No existing live reports'):
                collect(Path(tmp))
