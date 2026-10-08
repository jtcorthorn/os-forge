import tempfile
import unittest
from pathlib import Path
from discover_improvements import discover

class DiscoveryTests(unittest.TestCase):
    def test_un_ticketed_proposal_and_changed_source_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / 'company/_agents/proposals/new.md'
            p.parent.mkdir(parents=True)
            p.write_text('P1. observed defect')
            first = discover(root, ['company'], 'company/_agents/proposals/new.md')
            self.assertEqual(first['status'], 'complete_for_declared_scopes')
            self.assertEqual(len(first['sources']), 1)
            p.write_text('P1. changed proposal')
            self.assertNotEqual(first['sources'][0]['sha256'], discover(root, ['company'])['sources'][0]['sha256'])

    def test_missing_scope_and_canary_are_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = discover(tmp, ['missing'], 'company/proposals/new.md')
            self.assertEqual(result['status'], 'incomplete')
            self.assertEqual(len(result['errors']), 2)

    def test_history_excluded_and_escape_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'company/_archive/proposal.md'
            p.parent.mkdir(parents=True)
            p.write_text('history')
            self.assertEqual(discover(tmp, ['company'])['sources'], [])
            with self.assertRaises(ValueError):
                discover(tmp, ['../other'])

if __name__ == '__main__':
    unittest.main()
