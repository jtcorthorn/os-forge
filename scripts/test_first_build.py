"""Exercise the shipped package in isolated recipient roots, without accounts."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('first_build_forge', Path(__file__).with_name('forge.py'))
forge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forge)


class FirstBuildTests(unittest.TestCase):
    def test_shipped_blueprint_deploys_without_sources_or_connectors(self):
        for language in ('es', 'en'):
            with self.subTest(language=language), tempfile.TemporaryDirectory(prefix='forge-first-') as folder:
                root = Path(folder).resolve()
                self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
                config = {'owner': 'Example Owner', 'entry_language': language, 'external_intake': False}
                preview = forge.deploy(config, root)
                self.assertFalse(preview['applied'])
                self.assertEqual(list(root.iterdir()), [])
                self.assertTrue(forge.deploy(config, root, apply=True)['applied'])
                verified = forge.verify(root)
                self.assertTrue(verified['pass'], verified)
                self.assertEqual(verified['locally_modified'], [])
                before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
                self.assertTrue(forge.deploy(config, root, apply=True)['no_op'])
                self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_first_task_and_owner_edits_survive_redeployment(self):
        with tempfile.TemporaryDirectory(prefix='forge-first-') as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            source = root / 'Sources' / 'plan.txt'
            source.parent.mkdir()
            source.write_bytes(b'Owner supplied original.\n')
            original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            config = {'owner': 'Example Owner', 'external_intake': False}
            self.assertTrue(forge.deploy(config, root, apply=True)['applied'])
            result = root / '30_Projects' / 'first-result.md'
            result.write_text('# First result\n\nSource: [plan](../Sources/plan.txt).\n', encoding='utf-8')
            domain = root / '30_Projects' / 'MAPA.md'
            domain.write_text(domain.read_text(encoding='utf-8') + '\n[First result](first-result.md)\n', encoding='utf-8')
            saved_result, saved_map = result.read_bytes(), domain.read_bytes()
            self.assertTrue(forge.deploy(config, root, apply=True)['applied'])
            self.assertEqual(result.read_bytes(), saved_result)
            self.assertEqual(domain.read_bytes(), saved_map)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_hash)
            verified = forge.verify(root)
            self.assertTrue(verified['pass'], verified)
            self.assertIn('30_Projects/MAPA.md', verified['locally_modified'])


if __name__ == '__main__':
    unittest.main()
