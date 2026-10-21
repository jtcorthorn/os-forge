"""Behavioral tests for Forge snapshot deployment; no real factory writes."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("forge.py")
spec = importlib.util.spec_from_file_location("forge_under_test", SCRIPT)
forge = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(forge)


class ForgeDeploymentTests(unittest.TestCase):
    def test_english_entry_uses_owner_and_current_source_routes(self):
        actual = SCRIPT.parent.parent / 'assets' / 'entries' / 'en.md'
        entry = self.factory / 'assets' / 'entries' / 'en.md'
        entry.parent.mkdir(parents=True)
        entry.write_bytes(actual.read_bytes())
        result = forge.deploy({**self.config, 'owner': 'Alex', 'entry_language': 'en'}, self.target, apply=True)
        self.assertTrue(result['applied'])
        guide = (self.target / 'EMPIEZA_AQUI.md').read_text(encoding='utf-8')
        self.assertIn('Your OS, Alex', guide)
        self.assertIn('current original locations', guide)
        self.assertIn('00_System/Agents/MAPA.md', guide)

    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix="forge-test-")
        self.root = Path(self.sandbox.name).resolve()
        if not self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()) or not self.root.name.startswith('forge-test-'):
            raise RuntimeError('Unexpected temporary test directory; refusing recursive cleanup')
        self.addCleanup(self.sandbox.cleanup)
        self.factory = self.root / "factory"
        self.blueprint = self.factory / "assets" / "blueprint"
        self.blueprint.mkdir(parents=True)
        self.target = self.root / "recipient"
        self.target.mkdir()
        self.original_factory = forge.FACTORY
        forge.FACTORY = self.factory
        self.addCleanup(setattr, forge, "FACTORY", self.original_factory)
        self.config = {"owner": "Sample Owner", "external_intake": True}
        self.source("MAPA.md", b"# {{OWNER}} OS\n")
        self.source("00_System/Guide.md", b"Version one\n")

    def source(self, relative, data):
        path = self.blueprint / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def test_preview_reports_adds_without_mutating_target(self):
        before = self.snapshot()
        result = forge.deploy(self.config, self.target)
        self.assertFalse(result["applied"])
        self.assertEqual(result["counts"], {"add": 2})
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.target / "_meta/forge-manifest.json").exists())

    def test_apply_adds_and_records_rendered_hashes(self):
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(result["verified_files"], 2)
        self.assertEqual((self.target / "MAPA.md").read_bytes(), b"# Sample Owner OS\n")
        manifest = json.loads((self.target / "_meta/forge-manifest.json").read_text())
        self.assertEqual(set(manifest["files"]), {"MAPA.md", "00_System/Guide.md"})
        for relative, item in manifest["files"].items():
            self.assertEqual(item["sha256"], forge.sha((self.target / relative).read_bytes()))

    def test_blueprint_history_and_bytecode_are_not_deployed(self):
        self.source('00_System/Skills/_archive/old.md', b'[Historical](missing.md)\n')
        self.source('00_System/Tools/__pycache__/old.pyc', b'cached code')
        self.source('00_System/Tools/old.pyc', b'cached code')
        self.assertTrue(forge.deploy(self.config, self.target, apply=True)['applied'])
        self.assertFalse((self.target / '00_System/Skills/_archive').exists())
        self.assertFalse((self.target / '00_System/Tools/old.pyc').exists())

    def test_retained_history_does_not_hide_broken_active_routes(self):
        forge.deploy(self.config, self.target, apply=True)
        history = self.target / '00_System/Skills/_archive/old.md'
        history.parent.mkdir(parents=True)
        history.write_text('[Old route](missing.md)\n', encoding='utf-8')
        self.assertTrue(forge.verify(self.target)['pass'])
        active = self.target / '00_System/active.md'
        active.write_text('[Broken active route](missing.md)\n', encoding='utf-8')
        verified = forge.verify(self.target)
        self.assertFalse(verified['pass'])
        self.assertEqual(verified['broken_links'], [{'file': '00_System/active.md', 'link': 'missing.md'}])

    def test_same_config_is_idempotent(self):
        forge.deploy(self.config, self.target, apply=True)
        before = self.snapshot()
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertTrue(result["applied"])
        self.assertTrue(result["no_op"])
        self.assertEqual(result["counts"], {"unchanged": 2})
        self.assertEqual(self.snapshot(), before)

    def test_modified_managed_file_blocks_all_writes(self):
        forge.deploy(self.config, self.target, apply=True)
        (self.target / "MAPA.md").write_bytes(b"Local owner edit\n")
        self.source("MAPA.md", b"# Updated upstream owner OS\n")
        self.source("00_System/Guide.md", b"Version two\n")
        self.source("00_System/New.md", b"New package file\n")
        before = self.snapshot()
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertFalse(result["applied"])
        self.assertEqual(result["conflicts"], ["MAPA.md"])
        self.assertIn("blocked", result)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.target / "_archive").exists())

    def test_local_only_edit_survives_unrelated_update_then_conflicts_on_same_file_change(self):
        forge.deploy(self.config, self.target, apply=True)
        initial_manifest = json.loads((self.target / "_meta/forge-manifest.json").read_text())
        original_baseline = initial_manifest["files"]["MAPA.md"]["sha256"]
        (self.target / "MAPA.md").write_bytes(b"Local owner edit\n")
        self.source("00_System/Guide.md", b"Version two\n")
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(result["counts"], {"kept-local": 1, "update": 1})
        self.assertEqual((self.target / "MAPA.md").read_bytes(), b"Local owner edit\n")
        self.assertEqual((self.target / "00_System/Guide.md").read_bytes(), b"Version two\n")
        manifest = json.loads((self.target / "_meta/forge-manifest.json").read_text())
        self.assertEqual(manifest["files"]["MAPA.md"]["sha256"], original_baseline)
        self.source("MAPA.md", b"# Updated upstream owner OS\n")
        before = self.snapshot()
        conflict = forge.deploy(self.config, self.target, apply=True)
        self.assertFalse(conflict["applied"])
        self.assertEqual(conflict["conflicts"], ["MAPA.md"])
        self.assertEqual(self.snapshot(), before)

    def test_unmanaged_original_survives_add_and_update(self):
        original = self.target / "20_Ventures/original.txt"
        original.parent.mkdir(parents=True)
        original.write_bytes(b"Recipient original\n")
        forge.deploy(self.config, self.target, apply=True)
        self.source("00_System/Guide.md", b"Version two\n")
        forge.deploy(self.config, self.target, apply=True)
        self.assertEqual(original.read_bytes(), b"Recipient original\n")
        manifest = json.loads((self.target / "_meta/forge-manifest.json").read_text())
        self.assertNotIn("20_Ventures/original.txt", manifest["files"])

    def test_package_update_archives_prior_managed_bytes(self):
        forge.deploy(self.config, self.target, apply=True)
        prior_manifest = (self.target / "_meta/forge-manifest.json").read_bytes()
        prior_guide = (self.target / "00_System/Guide.md").read_bytes()
        self.source("00_System/Guide.md", b"Version two\n")
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(result["counts"], {"unchanged": 1, "update": 1})
        self.assertEqual((self.target / "00_System/Guide.md").read_bytes(), b"Version two\n")
        archives = list((self.target / "_archive/forge").glob("*/00_System/Guide.md"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_bytes(), prior_guide)
        self.assertEqual((archives[0].parents[1] / "forge-manifest.json").read_bytes(), prior_manifest)

    def test_only_upstream_removal_updates_manifest_without_removing_recipient_file(self):
        forge.deploy(self.config, self.target, apply=True)
        prior_guide = (self.target / "00_System/Guide.md").read_bytes()
        (self.blueprint / "00_System/Guide.md").unlink()
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual((self.target / "00_System/Guide.md").read_bytes(), prior_guide)
        manifest = json.loads((self.target / "_meta/forge-manifest.json").read_text())
        self.assertNotIn("00_System/Guide.md", manifest["files"])
        self.assertEqual(manifest["retained_upstream_removals"], ["00_System/Guide.md"])

    def test_identical_unmanaged_collision_is_not_claimed_for_future_overwrite(self):
        original = self.target / "00_System/Guide.md"
        original.parent.mkdir(parents=True)
        original.write_bytes(b"Version one\n")
        result = forge.deploy(self.config, self.target, apply=True)
        self.assertIn("00_System/Guide.md", result["conflicts"])
        self.assertEqual(original.read_bytes(), b"Version one\n")
        self.assertFalse((self.target / "_meta/forge-manifest.json").exists())

    def test_malicious_append_path_is_rejected_without_write(self):
        before = self.snapshot()
        config = {**self.config, "append": {"../escape.md": "Injected"}}
        with self.assertRaisesRegex(ValueError, "escapes root"):
            forge.deploy(config, self.target, apply=True)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "escape.md").exists())

    def test_factory_or_ancestor_target_is_rejected(self):
        for target in (self.factory, self.root):
            with self.subTest(target=target):
                with self.assertRaisesRegex(ValueError, "outside the factory"):
                    forge.deploy(self.config, target, apply=True)


if __name__ == "__main__":
    unittest.main()
