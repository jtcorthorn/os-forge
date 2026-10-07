import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).with_name("extract_sparse_xlsx.py")


class SparseXlsxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="osforge_sparse_test_")
        self.root = Path(self.tmp.name).resolve()
        (self.root / "originals").mkdir()
        self.book = self.root / "originals" / "sparse.xlsx"
        with zipfile.ZipFile(self.book, "w") as z:
            z.writestr("xl/workbook.xml", '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>')
            z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
            z.writestr("xl/sharedStrings.xml", '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><si><t>Top value</t></si></sst>')
            z.writestr("xl/worksheets/sheet1.xml", '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:C1048576"/><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c></row><row r="1048575"><c r="B1048575" s="1"/></row><row r="1048576"><c r="C1048576"><f>1+2</f><v>3</v></c></row></sheetData></worksheet>')
        self.digest = hashlib.sha256(self.book.read_bytes()).hexdigest()
        self.inventory = self.root / "inventory.csv"
        with self.inventory.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["relative_path", "sha256", "size_bytes"])
            writer.writeheader()
            writer.writerow({"relative_path": "originals/sparse.xlsx", "sha256": self.digest,
                             "size_bytes": self.book.stat().st_size})
        self.output = self.root / "_extracted" / "sparse"

    def tearDown(self):
        temp_root = Path(tempfile.gettempdir()).resolve()
        self.assertEqual(self.root.parent, temp_root)
        self.assertTrue(self.root.name.startswith("osforge_sparse_test_"))
        self.tmp.cleanup()

    def run_engine(self, extra=()):
        p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root),
                            "--inventory", str(self.inventory), "--output", str(self.output),
                            "--select", "originals/sparse.xlsx", *extra],
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        return manifest["sources"][0], p.stdout

    def test_sparse_late_row_and_resume(self):
        entry, stdout = self.run_engine()
        self.assertEqual(entry["status"], "complete")
        self.assertEqual(entry["metrics"]["sheets"][0]["declared_dimension"], "A1:C1048576")
        self.assertEqual(entry["metrics"]["stored_nonempty_cells_observed"], 2)
        self.assertNotIn("Top value", stdout)
        records = [json.loads(line) for line in (self.output / entry["content"]).read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["cell"] for r in records], ["A1", "C1048576"])
        self.assertEqual(records[0]["text"], "Top value")
        self.assertEqual(records[1]["formula"], "1+2")
        self.assertEqual(records[1]["cached_value_raw"], "3")
        again, _ = self.run_engine()
        self.assertTrue(again["resumed"])

    def test_limit_is_explicit_and_reextracts(self):
        self.run_engine()
        entry, _ = self.run_engine(["--max-cells", "1"])
        self.assertEqual(entry["status"], "truncated")
        self.assertNotIn("resumed", entry)
        self.assertIn("Cell budget reached; coverage incomplete", entry["warnings"])


if __name__ == "__main__":
    unittest.main()
