"""PyTorch next-day demand benchmark using the same UCI Bike Sharing protocol.

This adds framework-level deep-learning evidence while keeping the existing Ridge and
scikit-learn MLP comparisons. Model selection uses validation MAE only.
"""
from pathlib import Path
import csv, datetime, io, json, math, urllib.request, zipfile
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from model import ROOT, digest
from train_model import features

SEED=42
np.random.seed(SEED); torch.manual_seed(SEED)

class DemandMLP(nn.Module):
    def __init__(self,width):
        super().__init__(); self.net=nn.Sequential(nn.Linear(9,width),nn.ReLU(),nn.Dropout(.10),nn.Linear(width,1))
    def forward(self,x): return self.net(x).squeeze(-1)

def load_data():
    p=ROOT/'data/day.csv'
    if not p.exists():
        p.parent.mkdir(exist_ok=True)
        z=zipfile.ZipFile(io.BytesIO(urllib.request.urlopen('https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip').read()))
        p.write_bytes(z.read('day.csv'))
    source=json.loads((ROOT/'data/SOURCE.json').read_text())
    if digest(p)!=source['sha256']: raise ValueError('Dataset checksum mismatch')
    rows=list(csv.DictReader(p.open())); counts=[float(r['cnt']) for r in rows]; start=datetime.date.fromisoformat(rows[0]['dteday'])
    X=np.array([features(rows[i]['dteday'],counts[:i],start) for i in range(14,len(rows))],dtype='float32')
    y=np.array(counts[14:],dtype='float32'); return X,y,rows

def fit_candidate(X,y,a,b,width):
    sx=StandardScaler().fit(X[:a]); sy=StandardScaler().fit(y[:a,None])
    xt=torch.tensor(sx.transform(X[:a]),dtype=torch.float32); yt=torch.tensor(sy.transform(y[:a,None]).ravel(),dtype=torch.float32)
    xv=torch.tensor(sx.transform(X[a:b]),dtype=torch.float32)
    model=DemandMLP(width); opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4); loss_fn=nn.L1Loss()
    loader=DataLoader(TensorDataset(xt,yt),batch_size=64,shuffle=True)
    best=None; stale=0
    for epoch in range(250):
        model.train()
        for xb,yb in loader:
            opt.zero_grad(); loss=loss_fn(model(xb),yb); loss.backward(); opt.step()
        model.eval()
        with torch.no_grad(): pv=model(xv).numpy()
        pred=sy.inverse_transform(pv[:,None]).ravel(); mae=float(mean_absolute_error(y[a:b],pred))
        if best is None or mae<best[0]: best=(mae,{k:v.detach().clone() for k,v in model.state_dict().items()},epoch+1); stale=0
        else:
            stale+=1
            if stale>=25: break
    model.load_state_dict(best[1]); return model,sx,sy,best

def main():
    X,y,rows=load_data(); n=len(y); a=int(n*.6); b=int(n*.8)
    candidates={}; models={}
    for width in (16,32,64):
        torch.manual_seed(SEED)
        model,sx,sy,best=fit_candidate(X,y,a,b,width)
        candidates[str(width)]={'validation_mae':best[0],'epochs':best[2]}; models[width]=(model,sx,sy)
    winner=int(min(candidates,key=lambda k:candidates[k]['validation_mae']))
    # Refit selected architecture on train+validation using scaling from that fitting period.
    sx=StandardScaler().fit(X[:b]); sy=StandardScaler().fit(y[:b,None]); model=DemandMLP(winner)
    opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4); loss_fn=nn.L1Loss()
    loader=DataLoader(TensorDataset(torch.tensor(sx.transform(X[:b]),dtype=torch.float32),torch.tensor(sy.transform(y[:b,None]).ravel(),dtype=torch.float32)),batch_size=64,shuffle=True)
    torch.manual_seed(SEED)
    epochs=max(candidates[str(winner)]['epochs'],30)
    for _ in range(epochs):
        model.train()
        for xb,yb in loader:
            opt.zero_grad(); loss=loss_fn(model(xb),yb); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad(): scaled=model(torch.tensor(sx.transform(X[b:]),dtype=torch.float32)).numpy()
    pred=np.maximum(0,sy.inverse_transform(scaled[:,None]).ravel())
    baseline=X[b:,6]
    result={'framework':torch.__version__,'seed':SEED,'split':{'train':a,'validation':b-a,'test':n-b},'candidates':candidates,
            'selected_width':winner,'test_mae':float(mean_absolute_error(y[b:],pred)),'seasonal_baseline_mae':float(mean_absolute_error(y[b:],baseline)),
            'protocol':'Chronological 60/20/20; hidden width selected on validation MAE; final test untouched during selection.',
            'limitations':'Small CPU MLP on one historical bike-sharing system; not large-scale deep learning or production forecasting.'}
    out=ROOT/'artifacts'; out.mkdir(exist_ok=True); (out/'pytorch-demand-results.json').write_text(json.dumps(result,indent=2)); torch.save(model.state_dict(),out/'pytorch-demand.pt')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
