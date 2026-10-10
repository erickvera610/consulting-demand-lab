import json,os
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from core import run
ROOT=Path(__file__).parent
class Handler(BaseHTTPRequestHandler):
    def send(self,status,data,kind='application/json'):
        body=data.encode() if isinstance(data,str) else json.dumps(data).encode()
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/health':return self.send(200,{'status':'ok'})
        if self.path=='/':return self.send(200,(ROOT/'index.html').read_text(),'text/html')
        self.send(404,{'error':'Not found'})
    def do_POST(self):
        if self.path!='/api/run':return self.send(404,{'error':'Not found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=65536:raise ValueError('Request body must be 1 to 65536 bytes')
            payload=json.loads(self.rfile.read(length))
            if not isinstance(payload,dict):raise ValueError('JSON object required')
            self.send(200,run(payload))
        except (ValueError,TypeError,KeyError,OverflowError) as e:self.send(400,{'error':str(e)})
if __name__=='__main__':
    host=os.environ.get('HOST','127.0.0.1');port=int(os.environ.get('PORT','8000'))
    print(f'Open http://{host}:{port}',flush=True)
    ThreadingHTTPServer((host,port),Handler).serve_forever()
