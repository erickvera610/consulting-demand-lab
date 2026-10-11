import unittest,json,hashlib,threading,urllib.request,urllib.error
from model import *
from model_server import Handler,ThreadingHTTPServer
class ModelTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=load_model();cls.r=json.loads((ROOT/'artifacts/model-results.json').read_text())
 def test_public_artifact_hash(self):
  self.assertEqual(digest(ROOT/'artifacts/model.json'),self.r['model_sha256']);self.assertEqual((ROOT/'artifacts/model.json').read_bytes(),(ROOT/'docs/model.json').read_bytes())
 def test_export_predictions(self):
  for e in self.r['examples']:
   if self.m['task']=='demand':self.assertAlmostEqual(predict({'features':e['features']})['prediction'],e['prediction'],places=7)
   else:self.assertEqual(predict({'text':e['text']})['label'],e['label'])
 def test_invalid_input(self):
  for p in ([{'features':[float('nan')]*9},{'features':[True]*9},{'features':[1]}] if self.m['task']=='demand' else [{'text':''},{'text':1},{'text':'x'*10001}]):
   with self.assertRaises(ValueError):predict(p)
 def test_partition_protocol(self):
  if self.m['task']=='demand':
   s=self.r['split'];self.assertLess(s['train_end'],s['validation_end']);self.assertLess(s['validation_end'],s['test_start']);self.assertNotIn('weather',self.m['features'])
  else:self.assertEqual(self.r['abstract_id_overlap'],0);self.assertEqual(sum(self.r['sentences'].values()),sum(sum(row) for row in self.r['confusion_matrix'])+self.r['sentences']['train']+self.r['sentences']['validation'])
 def test_http_prediction_and_validation(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   url=f'http://127.0.0.1:{server.server_port}/api/predict';e=self.r['examples'][0];p={'features':e['features']} if self.m['task']=='demand' else {'text':e['text']}
   request=urllib.request.Request(url,data=json.dumps(p).encode(),headers={'Content-Type':'application/json'});self.assertEqual(json.loads(urllib.request.urlopen(request).read()),predict(p))
   with self.assertRaises(urllib.error.HTTPError) as cm:urllib.request.urlopen(urllib.request.Request(url,data=b'{}'))
   self.assertEqual(cm.exception.code,400)
  finally:server.shutdown();server.server_close();thread.join()
