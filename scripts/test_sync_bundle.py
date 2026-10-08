import tempfile
import unittest
from pathlib import Path
from build_sync_bundle import build, collect

class PublicationTests(unittest.TestCase):
    def seed(self, root):
        (root / 'README.md').write_text('Neutral owner method')
        (root / 'CHANGELOG.md').write_text('Verified reusable change')

    def test_neutral_snapshot_is_repeatable_by_content_and_keeps_intake_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'public'
            root.mkdir()
            self.seed(root)
            folder = root / 'assets/blueprint/_inbox'
            folder.mkdir(parents=True)
            (folder / 'CONTEXT.md').write_text('Neutral intake contract')
            target = Path(temp) / 'snapshot'
            first = build(root, target)
            second = build(root, target)
            self.assertEqual(first['content_hash'], second['content_hash'])
            self.assertEqual(len(first['files']), 3)
            self.assertTrue((target / 'SYNC_BUNDLE.zip').is_file())

    def test_private_inputs_and_credential_content_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed(root)
            (root / 'instance.json').write_text('{}')
            with self.assertRaises(ValueError):
                collect(root)
            (root / 'instance.json').unlink()
            (root / 'README.md').write_text('sk-' + 'x' * 30)
            with self.assertRaises(ValueError):
                collect(root)

    def test_output_in_source_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed(root)
            with self.assertRaises(ValueError):
                build(root, root / 'snapshot')

if __name__ == '__main__':
    unittest.main()
