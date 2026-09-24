import threading,unittest,time,json,hashlib,hmac
from concurrent.futures import ThreadPoolExecutor
from lab_app import LabServer,WEBHOOK_SECRET
from exercise import request,run
from race_demo import demonstrate
from auth_binding import bound_response

class LabTests(unittest.TestCase):
    def setUp(self):
        self.server=LabServer(('127.0.0.1',0));self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.port=self.server.server_port
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
    def login(self):
        _,value=request(self.port,'POST','/login',data={'user':'alice','password':'alice-lab'})
        _,value=request(self.port,'POST','/mfa',value['token'],{'code':'123456'})
        return value['token']
    def test_fixed_end_to_end(self):self.assertTrue(run(self.port)['passed'])
    def test_vulnerable_mode_reproduces(self):
        self.server.state.vulnerable=True
        self.assertTrue(run(self.port,'vulnerable')['passed'])
    def test_fixed_expectations_detect_vulnerable(self):
        self.server.state.vulnerable=True
        report=run(self.port,'fixed','api')
        self.assertFalse(report['passed'])
    def test_expired_session(self):
        token=self.login();self.server.state.sessions[token]['expires']=time.time()-1
        self.assertEqual(request(self.port,'GET','/api/profile',token)[0],401)
    def test_wrong_mfa_code(self):
        _,value=request(self.port,'POST','/login',data={'user':'alice','password':'alice-lab'})
        self.assertEqual(request(self.port,'POST','/mfa',value['token'],{'code':'wrong'})[0],401)
    def test_atomic_http_redemption(self):
        token=self.login()
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(request,self.port,'POST','/redeem',token,{'coupon':'LAB10'}) for _ in range(2)]
            self.assertEqual(sorted(f.result()[0] for f in futures),[200,409])
    def test_stale_webhook(self):
        stamp=str(int(time.time())-120);data={'event_id':'old-event'};raw=json.dumps(data,separators=(',',':')).encode()
        sig=hmac.new(WEBHOOK_SECRET,stamp.encode()+b'.'+raw,hashlib.sha256).hexdigest()
        self.assertEqual(request(self.port,'POST','/webhook',data=data,extra={'X-Lab-Timestamp':stamp,'X-Lab-Signature':sig})[0],401)
    def test_malformed_profile(self):
        token=self.login();self.assertEqual(request(self.port,'PATCH','/api/profile',token,{'display_name':[]})[0],400)
    def test_audit_has_no_tokens(self):
        token=self.login();request(self.port,'GET','/api/invoices/2',token)
        self.assertEqual(self.server.state.audit[-1]['result'],'deny')
        self.assertNotIn(token,json.dumps(self.server.state.audit))

class ModelTests(unittest.TestCase):
    def test_controlled_race(self):self.assertEqual(demonstrate(False),2);self.assertEqual(demonstrate(True),1)
    def test_auth_binding(self):
        expected={'state':'s','nonce':'n','issuer':'i','audience':'a'}
        self.assertTrue(bound_response(expected,dict(expected)))
        for key in expected:self.assertFalse(bound_response(expected,{**expected,key:'wrong'}))
    def test_auth_missing_claim(self):self.assertFalse(bound_response({'state':'s'},{}))

if __name__=='__main__':unittest.main(verbosity=2)
