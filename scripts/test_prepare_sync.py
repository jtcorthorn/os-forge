import json
import tempfile
import unittest
from pathlib import Path
from build_sync_bundle import build
from prepare_sync import prepare, verify, git_blob


class SyncPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        for name in ('README.md', 'CHANGELOG.md'):
            (self.source / name).write_text('Verified neutral update', encoding='utf-8')
        self.manifest = build(self.source, self.root / 'snapshot')
        self.bundle = self.root / 'snapshot/SYNC_BUNDLE.zip'
        self.baseline = {'files': [{'path': 'README.md', 'git_blob_sha1': git_blob(b'Prior neutral source')},
                                   {'path': 'CHANGELOG.md', 'git_blob_sha1': git_blob(b'Prior changelog')}]}
        self.remote = {'truncated': False, 'tree': [{'path': r['path'], 'sha': r['git_blob_sha1'], 'type': 'blob'}
                                                  for r in self.baseline['files']]}

    def test_changes_keep_remote_only_files_and_repeat_is_no_op(self):
        self.remote['tree'].append({'path': 'retained.md', 'sha': 'unmanaged', 'type': 'blob'})
        plan = prepare(self.bundle, self.manifest, self.remote, self.baseline)
        self.assertEqual(len(plan['changes']), 2)
        self.assertEqual(plan['retained_remote_paths'], ['retained.md'])
        self.remote['tree'] = [{'path': r['path'], 'sha': r['git_blob_sha1'], 'type': 'blob'} for r in plan['changes']]
        self.assertTrue(prepare(self.bundle, self.manifest, self.remote, self.baseline)['no_op'])

    def test_drift_and_protected_changes_stop_before_any_write(self):
        self.remote['tree'][0]['sha'] = 'another-writer'
        with self.assertRaisesRegex(ValueError, 'outside'):
            prepare(self.bundle, self.manifest, self.remote, self.baseline)
        self.remote['tree'][0]['sha'] = self.baseline['files'][0]['git_blob_sha1']
        with self.assertRaisesRegex(ValueError, 'Protected'):
            prepare(self.bundle, self.manifest, self.remote, self.baseline, ['README.md'])

    def test_corrupt_bundle_or_incomplete_tree_is_refused(self):
        self.remote['truncated'] = True
        with self.assertRaisesRegex(ValueError, 'coverage'):
            prepare(self.bundle, self.manifest, self.remote, self.baseline)
        self.bundle.write_bytes(self.bundle.read_bytes() + b'altered')
        with self.assertRaisesRegex(ValueError, 'Bundle hash'):
            verify(self.bundle, self.manifest)


if __name__ == '__main__':
    unittest.main()
