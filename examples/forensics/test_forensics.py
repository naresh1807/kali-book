import hashlib,json,tempfile,unittest
from pathlib import Path
from forensic_lab import verify,timeline

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        (self.root/'sample.txt').write_bytes(b'fixture')
        self.manifest={'sample.txt':hashlib.sha256(b'fixture').hexdigest()}
    def tearDown(self):self.temp.cleanup()
    def test_match(self):self.assertEqual({'sample.txt':'match'},verify(self.root,self.manifest))
    def test_tamper_detected(self):
        (self.root/'sample.txt').write_bytes(b'changed')
        self.assertEqual('mismatch',verify(self.root,self.manifest)['sample.txt'])
    def test_missing(self):
        self.assertEqual('missing',verify(self.root,{'absent.txt':self.manifest['sample.txt']})['absent.txt'])
    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):verify(self.root,{'../sample.txt':self.manifest['sample.txt']})
    def test_malformed_digest(self):
        with self.assertRaises(ValueError):verify(self.root,{'sample.txt':'not-a-hash'})

class TimelineTests(unittest.TestCase):
    def record(self,id,stamp):return json.dumps(dict(id=id,source='fixture',timestamp=stamp,event='synthetic'))
    def test_offset_conversion(self):
        row=timeline(self.record('a','2026-01-10T10:30:00+05:30'))[0]
        self.assertEqual('2026-01-10T05:00:00Z',row['utc'])
        self.assertEqual('2026-01-10T10:30:00+05:30',row['timestamp'])
    def test_order_and_ties(self):
        text='\n'.join([self.record('b','2026-01-10T05:02:00Z'),self.record('a','2026-01-10T05:00:00Z'),self.record('c','2026-01-10T10:32:00+05:30')])
        self.assertEqual(['a','b','c'],[r['id'] for r in timeline(text)])
    def test_naive_rejected(self):
        with self.assertRaises(ValueError):timeline(self.record('a','2026-01-10T05:00:00'))
    def test_duplicate_rejected(self):
        row=self.record('a','2026-01-10T05:00:00Z')
        with self.assertRaises(ValueError):timeline(row+'\n'+row)
    def test_malformed_rejected(self):
        for text in ('not json','{}',self.record('a','yesterday')):
            with self.assertRaises(ValueError):timeline(text)

if __name__=='__main__':unittest.main()
