"""Synthetic loopback teaching app. Fixed by default; never a production service."""
import argparse, hashlib, hmac, json, secrets, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

USERS = {"alice": {"password": "alice-lab", "tenant": "A"}, "bob": {"password": "bob-lab", "tenant": "B"}}
WEBHOOK_SECRET = b"PUBLIC-TRAINING-KEY-NOT-A-REAL-SECRET"

class State:
    def __init__(self, vulnerable=False):
        self.vulnerable = vulnerable
        self.lock = threading.Lock()
        self.sessions = {}
        self.profiles = {name: {"display_name": name, "role": "user"} for name in USERS}
        self.redeemed = set()
        self.events = set()
        self.audit = []
        self.invoices = {1: {"id": 1, "owner": "alice", "tenant": "A", "amount": 100}, 2: {"id": 2, "owner": "bob", "tenant": "B", "amount": 200}}
    def record(self, action, user, result):
        with self.lock:
            self.audit.append({"action": action, "user": user, "result": result})
            self.audit = self.audit[-100:]

class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, vulnerable=False):
        self.state = State(vulnerable)
        super().__init__(address, Handler)

class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(3)
    def log_message(self, *args): pass
    def send(self, code, value):
        data = json.dumps(value).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)
    def body(self):
        raw_length = self.headers.get("Content-Length", "0")
        if not raw_length.isdigit() or int(raw_length) > 4096: raise ValueError("Invalid body size")
        raw = self.rfile.read(int(raw_length))
        if len(raw) != int(raw_length): raise ValueError("Incomplete body")
        data = json.loads(raw)
        if not isinstance(data, dict): raise ValueError("Object required")
        return raw, data
    def session(self, allow_pending=False):
        token = self.headers.get("Authorization", "").removeprefix("Bearer ")
        state = self.server.state
        with state.lock:
            session = state.sessions.get(token)
            if not session or session["expires"] < time.time(): return None, token
            if not allow_pending and session["stage"] != "complete" and not state.vulnerable: return None, token
            return dict(session), token
    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ("/", "/browser", "/browser.js"):
            file = "browser.js" if path.endswith('.js') else "browser.html"
            data = Path(__file__).with_name(file).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript" if file.endswith('.js') else "text/html; charset=utf-8")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.send_header("Content-Length",str(len(data)))
            self.end_headers();self.wfile.write(data);return
        state = self.server.state
        session, _ = self.session()
        if not session: self.send(401, {"error": "complete authentication required"});return
        user = session["user"]
        if path == "/api/profile":
            self.send(200, {"user": user, **state.profiles[user]});return
        if path == "/api/v1/invoices":
            self.send(200, list(state.invoices.values())) if state.vulnerable else self.send(404, {"error":"retired route"});return
        if path == "/api/invoices":
            try:
                limit = int(parse_qs(urlsplit(self.path).query).get('limit',['10'])[0])
                if not 1 <= limit <= 10: raise ValueError()
            except ValueError: self.send(400,{"error":"limit must be 1..10"});return
            data=[x for x in state.invoices.values() if x['owner']==user and x['tenant']==USERS[user]['tenant']]
            self.send(200,data[:limit]);return
        if path.startswith('/api/invoices/'):
            try: item=state.invoices[int(path.rsplit('/',1)[1])]
            except (ValueError,KeyError): self.send(404,{"error":"not found"});return
            allowed = state.vulnerable or (item['owner']==user and item['tenant']==USERS[user]['tenant'])
            state.record('invoice.read',user,'allow' if allowed else 'deny')
            self.send(200,item) if allowed else self.send(403,{'error':'forbidden'});return
        self.send(404,{'error':'not found'})
    def do_PATCH(self):
        if urlsplit(self.path).path != '/api/profile': self.send(404,{'error':'not found'});return
        session,_=self.session()
        if not session:self.send(401,{'error':'authentication required'});return
        try:
            _,data=self.body()
            allowed={'display_name','role'} if self.server.state.vulnerable else {'display_name'}
            if not data or set(data)-allowed or any(not isinstance(v,str) or len(v)>64 for v in data.values()):raise ValueError()
        except (ValueError,OSError):self.send(400,{'error':'unsupported profile fields'});return
        with self.server.state.lock:self.server.state.profiles[session['user']].update(data)
        self.send(200,{'updated':True})
    def do_POST(self):
        path=urlsplit(self.path).path;state=self.server.state
        try:raw,data=self.body()
        except (ValueError,OSError):self.send(400,{'error':'invalid JSON or size'});return
        if path=='/login':
            user=data.get('user');password=data.get('password')
            if not isinstance(user,str) or user not in USERS or password!=USERS[user]['password']:
                self.send(401,{'error':'invalid lab credentials'});return
            token=secrets.token_urlsafe(24)
            with state.lock:state.sessions[token]={'user':user,'stage':'pending','expires':time.time()+300}
            self.send(200,{'token':token,'stage':'pending','next':'POST /mfa with lab code 123456'});return
        if path=='/webhook':
            stamp=self.headers.get('X-Lab-Timestamp','');signature=self.headers.get('X-Lab-Signature','')
            try:
                valid_time=abs(time.time()-int(stamp))<=60
                expected=hmac.new(WEBHOOK_SECRET,stamp.encode()+b'.'+raw,hashlib.sha256).hexdigest()
                event=data.get('event_id')
                if not valid_time or not hmac.compare_digest(signature,expected) or not isinstance(event,str) or not 1<=len(event)<=64:raise ValueError()
            except (ValueError,UnicodeError):self.send(401,{'error':'invalid webhook proof'});return
            with state.lock:
                duplicate=event in state.events
                if not duplicate:state.events.add(event)
            self.send(409 if duplicate else 200,{'accepted':not duplicate});return
        session,token=self.session(allow_pending=path=='/mfa')
        if not session:self.send(401,{'error':'authentication required'});return
        user=session['user']
        if path=='/mfa':
            if data.get('code')!='123456' or session['stage']!='pending':self.send(401,{'error':'invalid lab proof'});return
            new_token=token if state.vulnerable else secrets.token_urlsafe(24)
            with state.lock:
                # Recheck the state under lock to make concurrent use single-use.
                current=state.sessions.get(token)
                if not current or current['stage']!='pending':self.send(401,{'error':'stale session'});return
                del state.sessions[token]
                state.sessions[new_token]={'user':user,'stage':'complete','expires':time.time()+300}
            self.send(200,{'token':new_token,'stage':'complete'});return
        if path=='/logout':
            with state.lock:state.sessions.pop(token,None)
            self.send(200,{'logged_out':True});return
        if path=='/redeem':
            if data != {'coupon':'LAB10'}:self.send(400,{'error':'only LAB10 fixture accepted'});return
            with state.lock:
                duplicate=user in state.redeemed
                if not duplicate:state.redeemed.add(user)
            self.send(409 if duplicate else 200,{'discount':0 if duplicate else 10});return
        self.send(404,{'error':'not found'})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8901);p.add_argument('--mode',choices=['fixed','vulnerable'],default='fixed');a=p.parse_args()
    if not 1<=a.port<=65535:p.error('Port must be 1..65535')
    server=LabServer(('127.0.0.1',a.port),a.mode=='vulnerable')
    print(f'TRAINING ONLY: {a.mode} on http://127.0.0.1:{a.port}; Ctrl+C stops; restart resets data.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
