from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
import argparse
class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        route=urlsplit(self.path).path
        if route=="/redirect":
            self.send_response(302);self.send_header("Location","/strong");self.end_headers();return
        if route not in ("/", "/strong", "/weak", "/cors"):
            self.send_response(404);self.end_headers();return
        body=b'<title>Fictional lab</title><a href="/strong?q=hidden">Review</a><form action="/never-submit" method="post"><input name="fixture" value="synthetic"></form>'
        self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8")
        if route=="/strong":
            self.send_header("Content-Security-Policy","default-src 'none'; frame-ancestors 'none'")
            self.send_header("X-Content-Type-Options","nosniff")
            self.send_header("Referrer-Policy","no-referrer")
            self.send_header("Set-Cookie","lab_session=FAKE_ONLY; Secure; HttpOnly; SameSite=Lax")
        else:self.send_header("Set-Cookie","lab_preference=FAKE_ONLY")
        if route=="/cors":
            self.send_header("Access-Control-Allow-Origin",self.headers.get("Origin","https://review.invalid"))
            self.send_header("Access-Control-Allow-Credentials","true")
        self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
    def log_message(self,*args):pass
if __name__=="__main__":
    p=argparse.ArgumentParser(description="Synthetic local fixture, not a production server")
    p.add_argument("--port",type=int,default=8891);a=p.parse_args()
    if not 1<=a.port<=65535:p.error("Port must be 1..65535")
    server=ThreadingHTTPServer(("127.0.0.1",a.port),Fixture)
    print(f"Fictional fixture: http://127.0.0.1:{a.port}; Ctrl+C stops it",flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
