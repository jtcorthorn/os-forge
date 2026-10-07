"""Synthetic preservation, collision and restart behavior; no private source inputs."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import relocate_sources as move


class RelocationTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix='os-forge-move-')
        self.root = Path(self.sandbox.name).resolve()
        if self.root.parent != Path(tempfile.gettempdir()).resolve() or not self.root.name.startswith('os-forge-move-'):
            raise RuntimeError('Unexpected test root')
        self.addCleanup(self.sandbox.cleanup)
        self.plan = self.root / 'plan.json'
        self.run = self.root / '_archive/run'
        self.rows = []
        for name, contents in [('a.txt', b'first original'), ('b.txt', b'second original')]:
            source = self.root / 'Incoming' / name
            source.parent.mkdir(exist_ok=True)
            source.write_bytes(contents)
            self.rows.append({'old': f'Incoming/{name}', 'new': f'20_Ventures/Example/originals/{name}',
                              'size_bytes': len(contents), 'sha256': hashlib.sha256(contents).hexdigest()})
        self.save_plan()

    def save_plan(self):
        self.plan.write_text(json.dumps({'schema_version': 1, 'files': self.rows}), encoding='utf-8')

    def test_preview_does_not_mutate(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertFalse(move.relocate(self.root, self.plan, self.run)['applied'])
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_apply_keeps_backup_bytes_and_retry_is_safe(self):
        self.assertTrue(move.relocate(self.root, self.plan, self.run, True)['applied'])
        for row in self.rows:
            self.assertFalse((self.root / row['old']).exists())
            self.assertEqual(move.digest(self.root / row['new']), row['sha256'])
            self.assertEqual(move.digest(self.run / 'originals' / row['sha256']), row['sha256'])
        self.assertEqual(move.relocate(self.root, self.plan, self.run, True)['already_moved'], 2)

    def test_one_collision_blocks_all_sources(self):
        target = self.root / self.rows[1]['new']
        target.parent.mkdir(parents=True)
        target.write_bytes(b'local work')
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run, True)
        self.assertTrue((self.root / self.rows[0]['old']).exists())
        self.assertFalse(self.run.exists())
        self.assertEqual(target.read_bytes(), b'local work')

    def test_changed_source_blocks_all(self):
        (self.root / self.rows[1]['old']).write_bytes(b'new edit')
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run, True)
        self.assertTrue((self.root / self.rows[0]['old']).exists())
        self.assertFalse(self.run.exists())

    def test_traversal_and_case_collision_rejected(self):
        self.rows[0]['new'] = '../outside.txt'
        self.save_plan()
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run)
        self.rows[0]['new'] = 'target/A.txt'
        self.rows[1]['new'] = 'target/a.txt'
        self.save_plan()
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run)

    def test_resume_after_interrupted_second_move(self):
        actual_rename = move.os.rename
        calls = []
        def fail_second(old, new):
            calls.append(old)
            if len(calls) == 2:
                raise OSError('synthetic interruption')
            return actual_rename(old, new)
        with patch.object(move.os, 'rename', side_effect=fail_second):
            with self.assertRaises(OSError):
                move.relocate(self.root, self.plan, self.run, True)
        self.assertFalse((self.run / 'apply.lock').exists())
        for row in self.rows:
            self.assertTrue(move.matches(self.run / 'originals' / row['sha256'], row))
        self.assertEqual(move.relocate(self.root, self.plan, self.run, True)['already_moved'], 1)

    def test_changed_plan_cannot_reuse_run(self):
        move.relocate(self.root, self.plan, self.run, True)
        self.rows[0]['new'] = 'different/a.txt'
        self.save_plan()
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run, True)

    def test_destination_parent_file_blocks_before_mutation(self):
        (self.root / 'blocked').write_bytes(b'local file')
        self.rows[1]['new'] = 'blocked/b.txt'
        self.save_plan()
        with self.assertRaises(ValueError):
            move.relocate(self.root, self.plan, self.run, True)
        self.assertTrue((self.root / self.rows[0]['old']).exists())
        self.assertFalse(self.run.exists())


if __name__ == '__main__':
    unittest.main()
