import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from hive.evidence import collect, RUNS


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

    def test_empty_collection_does_not_claim_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'No existing live reports'):
                collect(Path(tmp))
