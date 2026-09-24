"""Bounded exercises against the synthetic loopback casebook app only."""
import argparse,hashlib,hmac,http.client,json,time
from lab_app import WEBHOOK_SECRET

def request(port,method,path,token=None,data=None,extra=None):
    connection=http.client.HTTPConnection('127.0.0.1',port,timeout=3)
    headers={'Content-Type':'application/json'}
    if token:headers['Authorization']='Bearer '+token
    if extra:headers.update(extra)
    body=json.dumps(data,separators=(',',':')).encode() if data is not None else None
    try:
        connection.request(method,path,body=body,headers=headers)
        response=connection.getresponse();raw=response.read(65537)
        if len(raw)>65536:raise ValueError('Response too large')
        return response.status,json.loads(raw)
    finally:connection.close()

def run(port,expected='fixed',case='all'):
    vulnerable=expected=='vulnerable';checks=[]
    def check(name,condition):checks.append({'check':name,'passed':bool(condition)})
    status,login=request(port,'POST','/login',data={'user':'alice','password':'alice-lab'})
    if status!=200:raise ValueError('Lab login failed')
    pending=login['token']
    status,_=request(port,'GET','/api/invoices/1',pending)
    if case in ('all','auth'):check('pending session boundary',status==(200 if vulnerable else 401))
    status,verified=request(port,'POST','/mfa',pending,{'code':'123456'})
    if status!=200:raise ValueError('Lab MFA transition failed')
    token=verified['token']
    if case in ('all','auth'):
        check('token rotation', (token==pending) if vulnerable else (token!=pending))
        status,_=request(port,'GET','/api/invoices/1',pending)
        check('old token invalidation',status==(200 if vulnerable else 401))
    if case in ('all','api'):
        status,own=request(port,'GET','/api/invoices/1',token);check('owner read allowed',status==200 and own.get('owner')=='alice')
        status,_=request(port,'GET','/api/invoices/2',token);check('other owner/tenant denied',status==(200 if vulnerable else 403))
        status,_=request(port,'PATCH','/api/profile',token,{'role':'admin'});check('server-owned field protection',status==(200 if vulnerable else 400))
        status,profile=request(port,'GET','/api/profile',token);check('role remains policy-controlled',profile.get('role')==('admin' if vulnerable else 'user'))
        status,_=request(port,'PATCH','/api/profile',token,{'display_name':'Alice fixture'});check('permitted update works',status==200)
        status,_=request(port,'GET','/api/invoices?limit=11',token);check('list limit enforced',status==400)
        status,_=request(port,'GET','/api/v1/invoices',token);check('retired API route unavailable',status==(200 if vulnerable else 404))
        _,b=request(port,'POST','/login',data={'user':'bob','password':'bob-lab'})
        _,b=request(port,'POST','/mfa',b['token'],{'code':'123456'})
        status,row=request(port,'GET','/api/invoices/2',b['token']);check('second user own object allowed',status==200 and row.get('owner')=='bob')
    if case in ('all','logic'):
        first,_=request(port,'POST','/redeem',token,{'coupon':'LAB10'})
        second,_=request(port,'POST','/redeem',token,{'coupon':'LAB10'})
        check('single redemption',first==200 and second==409)
    if case in ('all','webhook'):
        stamp=str(int(time.time()));data={'event_id':'fixture-event-'+str(time.time_ns())}
        raw=json.dumps(data,separators=(',',':')).encode()
        signature=hmac.new(WEBHOOK_SECRET,stamp.encode()+b'.'+raw,hashlib.sha256).hexdigest()
        headers={'X-Lab-Timestamp':stamp,'X-Lab-Signature':signature}
        status,_=request(port,'POST','/webhook',data=data,extra={**headers,'X-Lab-Signature':'invalid'});check('webhook rejects bad signature',status==401)
        status,_=request(port,'POST','/webhook',data=data,extra=headers);check('signed webhook accepted',status==200)
        status,_=request(port,'POST','/webhook',data=data,extra=headers);check('webhook replay rejected',status==409)
    if case in ('all','auth'):
        request(port,'POST','/logout',token,{})
        status,_=request(port,'GET','/api/profile',token);check('logout invalidates token',status==401)
    return {'expected_mode':expected,'case':case,'checks':checks,'passed':all(x['passed'] for x in checks),'note':'Passed means observations match the selected teaching mode; vulnerable-mode success does not mean secure.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8901);p.add_argument('--expect',choices=['fixed','vulnerable'],default='fixed');p.add_argument('--case',choices=['all','api','auth','logic','webhook'],default='all');a=p.parse_args()
    if not 1<=a.port<=65535:p.error('Port must be 1..65535')
    try:
        report=run(a.port,a.expect,a.case);print(json.dumps(report,indent=2))
        raise SystemExit(0 if report['passed'] else 1)
    except (ValueError,OSError,http.client.HTTPException):p.exit(1,'Exercise failed: check fixture state, port and expected mode.\n')
