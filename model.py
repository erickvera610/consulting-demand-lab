import hashlib,json,math,re
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parent

def load_model():
    return json.loads((ROOT/'artifacts/model.json').read_text())

def predict(payload, model=None):
    m=model or load_model()
    if m['task']=='demand':
        x=payload.get('features')
        if not isinstance(x,list) or len(x)!=len(m['features']) or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in x):
            raise ValueError('Expected finite numeric features in documented order')
        x=(np.array(x)-m['mean'])/m['scale']
        for i,(w,b) in enumerate(zip(m['weights'],m['biases'])):
            x=x@np.array(w)+b
            if i<len(m['weights'])-1:x=np.maximum(x,0)
        return {'prediction':float(max(0,x[0]*m['target_scale']+m['target_mean']))}
    s=payload.get('text')
    if not isinstance(s,str) or not s.strip() or len(s)>10000:raise ValueError('Text must contain 1–10000 characters')
    tokens=re.findall(r'[a-z][a-z]+',s.lower());v=m['vocabulary'];x=np.zeros(len(v))
    for t in tokens:
        if t in v:x[v[t]]+=1
    x*=m['idf'];norm=np.linalg.norm(x)
    if norm==0:return {'label':None,'probabilities':{},'out_of_vocabulary':True}
    x/=norm;scores=np.array(m['weights'])@x+m['biases'];p=np.exp(scores-max(scores));p/=p.sum()
    return {'label':m['classes'][int(p.argmax())],'probabilities':dict(zip(m['classes'],map(float,p))),'out_of_vocabulary':False}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(model,report):
    (ROOT/'artifacts').mkdir(exist_ok=True);(ROOT/'docs').mkdir(exist_ok=True)
    content=json.dumps(model,separators=(',',':'),allow_nan=False)
    report['model_sha256']=hashlib.sha256(content.encode()).hexdigest()
    for folder in ('artifacts','docs'):
        (ROOT/folder/'model.json').write_text(content)
        (ROOT/folder/'model-results.json').write_text(json.dumps(report,indent=2,allow_nan=False))
