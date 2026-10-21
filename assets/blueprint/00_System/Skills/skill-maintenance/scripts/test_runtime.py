import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import runtime


class FixtureAPI:
    def get(self, path):return {'sha':'b'*40}
    def tree(self, repo, ref, prefix):return {'SKILL.md':runtime.git_sha(b'old\n' if ref=='a'*40 else b'new\n')}
    def blob(self, repo, identity):return b'old\n' if identity==runtime.git_sha(b'old\n') else b'new\n'


class RuntimeChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.skill=self.root/'skill';self.skill.mkdir();(self.skill/'SKILL.md').write_text('original')
        self.state=self.root/'events';self.artifact=self.root/'result.txt';self.artifact.write_text('actual')
        self.common=['--root',str(self.skill),'--run-id','fixture-context','--runtime','fixture-profile','--state-dir',str(self.state)]
    def tearDown(self):self.temp.cleanup()
    def call(self,action,*args):
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):code=runtime.main([action,*self.common,*args])
        return code,json.loads(stream.getvalue())
    def test_inspection_and_difference(self):
        self.assertEqual(self.call('inspect')[1]['discovery_and_use'],'unverified')
        other=self.root/'other';other.mkdir();(other/'SKILL.md').write_text('changed')
        self.assertEqual(self.call('inspect','--canonical',str(other))[1]['status'],'differs')
    def test_missing_source_is_incomplete(self):
        (self.skill/'SKILL.md').unlink();self.assertEqual(self.call('inspect')[0],2)
    def test_read_is_not_applied_and_repeat_is_deduplicated(self):
        self.assertEqual(self.call('read')[1]['status'],'delivered')
        self.assertEqual(self.call('read')[1]['status'],'unchanged')
        report=self.call('usage')[1];self.assertEqual(report['counts']['read'],1)
        self.assertEqual(report['counts']['applied_attested'],0)
    def test_changed_file_and_forced_read_are_delivered(self):
        self.call('read');(self.skill/'SKILL.md').write_text('v2')
        self.assertEqual(self.call('read')[1]['status'],'delivered')
        self.assertEqual(self.call('read','--force')[1]['status'],'delivered')
    def test_profile_coverage_is_unknown(self):
        self.call('read')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runtime.main(['usage','--runtime','other','--state-dir',str(self.state)]),0)
        self.assertEqual(runtime.usage(runtime.events(self.state),'other')['status'],'unknown')
    def test_application_and_property_verification(self):
        args=['--artifact',str(self.artifact)]
        self.assertEqual(self.call('applied',*args)[0],2)
        self.call('read');self.assertEqual(self.call('applied',*args)[1]['status'],'applied_attested')
        self.assertEqual(self.call('verify-bytes',*args,'--expected-sha256','0'*64,'--criterion','fixture byte identity')[0],1)
        self.assertEqual(self.call('verify-bytes',*args,'--expected-sha256',runtime.sha(self.artifact.read_bytes()),'--criterion','fixture byte identity')[0],0)
        self.artifact.write_text('later')
        self.assertGreater(self.call('usage')[1]['changed_or_missing_artifact_events'],0)
    def test_reference_escape_is_refused(self):
        self.assertEqual(self.call('read','--file','../result.txt')[0],2)
    def test_receipt_tampering_is_incomplete(self):
        self.call('read');p=next(self.state.glob('*.json'));row=json.loads(p.read_text());row['stage']='verified_property';p.write_text(json.dumps(row))
        self.assertEqual(self.call('usage')[0],2)
    def test_compare_preserves_local_adaptation(self):
        before=(self.skill/'SKILL.md').read_bytes()
        result=runtime.compare('example/skills','a'*40,'skills/demo',self.skill,FixtureAPI())
        self.assertEqual(result['status'],'update_available');self.assertIn('+new',result['diff'])
        self.assertEqual(result['local_upstream_drift'],['SKILL.md']);self.assertEqual((self.skill/'SKILL.md').read_bytes(),before)
    def test_repository_movement_without_skill_change_is_unchanged(self):
        api=FixtureAPI();api.tree=lambda *a:{'SKILL.md':runtime.git_sha(b'old\n')}
        self.assertEqual(runtime.compare('example/skills','a'*40,'skills/demo',api=api)['status'],'unchanged')
    def test_truncated_tree_is_refused(self):
        api=runtime.GitHub()
        with patch.object(api,'get',return_value={'truncated':True,'tree':[]}):
            with self.assertRaises(ValueError):api.tree('example/skills','a'*40,'skills/demo')
    def test_explicit_output_never_overwrites(self):
        output=self.root/'saved.json';self.call('inspect','--output',str(output));before=output.read_bytes()
        with self.assertRaises(FileExistsError):self.call('inspect','--output',str(output))
        self.assertEqual(output.read_bytes(),before)


if __name__=='__main__':unittest.main()
