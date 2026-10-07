import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("search_extracted.py")


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="osforge_search_test_")
        self.root = Path(self.tmp.name).resolve()
        (self.root / "source").mkdir()
        (self.root / "extract" / "content").mkdir(parents=True)
        self.a = self.root / "source" / "a.txt"
        self.b = self.root / "source" / "b.txt"
        self.a.write_text("private alpha", encoding="utf-8")
        self.b.write_bytes(self.a.read_bytes())
        h = hashlib.sha256(self.a.read_bytes()).hexdigest()
        self.artifact = self.root / "extract" / "content" / (h + ".txt.jsonl")
        self.artifact.write_text(json.dumps({"locator": "line:1", "locator_kind": "line", "text": "The KEY fact is here."}) + "\n", encoding="utf-8")
        self.manifest = self.root / "extract" / "manifest.json"
        self.manifest.write_text(json.dumps({"sources": [
            {"relative_path": "source/a.txt", "sha256": h, "status": "complete", "content": "content/" + self.artifact.name},
            {"relative_path": "source/b.txt", "sha256": h, "status": "complete", "content": "content/" + self.artifact.name, "alias_of": "source/a.txt"},
            {"relative_path": "source/unsupported.bin", "status": "unsupported"}]}), encoding="utf-8")

    def tearDown(self):
        temp_root = Path(tempfile.gettempdir()).resolve()
        self.assertEqual(self.root.parent, temp_root)
        self.assertTrue(self.root.name.startswith("osforge_search_test_"))
        self.tmp.cleanup()

    def run_search(self, query, extra=()):
        p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                            "--manifest", str(self.manifest), "--query", query, *extra],
                           capture_output=True, text=True, timeout=10)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def test_search_alias_coverage_and_stale_source(self):
        result = self.run_search("key", ["--context", "3"])
        hit = result["hits"][0]
        self.assertEqual(hit["alias_count"], 1)
        self.assertEqual(hit["locator"], "line:1")
        self.assertEqual(hit["source_hash_state"], "current")
        self.assertLessEqual(len(hit["excerpt"]), 3 + 3 + 3)
        self.assertEqual(result["coverage"]["unique_artifacts_available"], 1)
        self.assertEqual(result["coverage"]["skipped_status_sources"], 1)
        self.a.write_text("changed", encoding="utf-8")
        self.assertEqual(self.run_search("KEY")["hits"][0]["source_hash_state"], "stale")

    def test_no_match_is_bounded(self):
        result = self.run_search("not present")
        self.assertEqual(result["hits"], [])
        self.assertTrue(result["coverage"]["scan_complete"])
        self.assertIn("not proof of absence", result["interpretation"])

    def test_artifact_escape_rejected(self):
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["sources"][0]["content"] = "../../elsewhere.jsonl"
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")
        p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                            "--manifest", str(self.manifest), "--query", "KEY"],
                           capture_output=True, text=True, timeout=10)
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
