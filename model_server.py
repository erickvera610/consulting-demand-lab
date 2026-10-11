import os,json,mimetypes
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from model import ROOT,predict
class Handler(BaseHTTPRequestHandler):
 def send(self,status,payload):
  data=json.dumps(payload,allow_nan=False).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/health':return self.send(200,{'status':'ok','model':'artifacts/model.json'})
  name=self.path.split('?')[0].lstrip('/') or 'model-demo.html'
  if name not in {'model-demo.html','model.js','model.json','model-results.json'}:return self.send(404,{'error':'Not found'})
  data=(ROOT/'docs'/name).read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(name)[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_POST(self):
  if self.path!='/api/predict':return self.send(404,{'error':'Not found'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=65536:raise ValueError('Body must contain 1–65536 bytes')
   p=json.loads(self.rfile.read(length))
   if not isinstance(p,dict):raise ValueError('JSON object required')
   self.send(200,predict(p))
  except (ValueError,TypeError,KeyError,OverflowError) as e:self.send(400,{'error':str(e)})
if __name__=='__main__':
 host=os.environ.get('HOST','127.0.0.1');port=int(os.environ.get('PORT','8001'));print(f'Open http://{host}:{port}',flush=True);ThreadingHTTPServer((host,port),Handler).serve_forever()
