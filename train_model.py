import csv,datetime,urllib.request
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error
from threadpoolctl import threadpool_limits
from model import *

def features(date,history,start):
    d=datetime.date.fromisoformat(date);weekday=d.weekday();month=d.month
    return [math.sin(2*math.pi*weekday/7),math.cos(2*math.pi*weekday/7),math.sin(2*math.pi*month/12),math.cos(2*math.pi*month/12),(d-start).days,history[-1],history[-7],float(np.mean(history[-7:])),float(np.mean(history[-14:]))]

def train():
    p=ROOT/'data/day.csv'
    if not p.exists():
        import io,zipfile
        p.parent.mkdir(exist_ok=True);z=zipfile.ZipFile(io.BytesIO(urllib.request.urlopen('https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip').read()));p.write_bytes(z.read('day.csv'))
    source=json.loads((ROOT/'data/SOURCE.json').read_text())
    if digest(p)!=source['sha256']:raise ValueError('Dataset checksum mismatch')
    rows=list(csv.DictReader(p.open()));counts=[float(r['cnt']) for r in rows];start=datetime.date.fromisoformat(rows[0]['dteday'])
    assert all((datetime.date.fromisoformat(rows[i]['dteday'])-start).days==i for i in range(len(rows)))
    X=np.array([features(rows[i]['dteday'],counts[:i],start) for i in range(14,len(rows))]);y=np.array(counts[14:]);n=len(y);a=int(n*.6);b=int(n*.8)
    sx=StandardScaler().fit(X[:a]);sy=StandardScaler().fit(y[:a,None]);tx=sx.transform(X[:a]);ty=sy.transform(y[:a,None]).ravel()
    scores={};nets={}
    with threadpool_limits(limits=1):
        for width in (16,32):
            net=MLPRegressor(hidden_layer_sizes=(width,),random_state=42,max_iter=500,early_stopping=False,alpha=.1,learning_rate_init=.003).fit(tx,ty)
            scores[f'MLP-{width}']=float(mean_absolute_error(y[a:b],sy.inverse_transform(net.predict(sx.transform(X[a:b]))[:,None]).ravel()));nets[width]=net
        ridge=Ridge(alpha=10).fit(tx,ty);scores['Ridge']=float(mean_absolute_error(y[a:b],sy.inverse_transform(ridge.predict(sx.transform(X[a:b]))[:,None]).ravel()))
        width=min(nets,key=lambda w:scores[f'MLP-{w}']);sx=StandardScaler().fit(X[:b]);sy=StandardScaler().fit(y[:b,None]);net=MLPRegressor(hidden_layer_sizes=(width,),random_state=42,max_iter=500,early_stopping=False,alpha=.1,learning_rate_init=.003).fit(sx.transform(X[:b]),sy.transform(y[:b,None]).ravel())
        ridge=Ridge(alpha=10).fit(sx.transform(X[:b]),sy.transform(y[:b,None]).ravel())
    model={'task':'demand','features':['weekday_sin','weekday_cos','month_sin','month_cos','elapsed_days','lag_1_day','lag_7_days','past_7_day_mean','past_14_day_mean'],'mean':sx.mean_.tolist(),'scale':sx.scale_.tolist(),'target_mean':float(sy.mean_[0]),'target_scale':float(sy.scale_[0]),'weights':[w.tolist() for w in net.coefs_],'biases':[v.tolist() for v in net.intercepts_],'architecture':[9,width,1],'seed':42}
    pred=np.array([predict({'features':x.tolist()},model)['prediction'] for x in X[b:]]);baseline=X[b:,6];rp=np.maximum(0,sy.inverse_transform(ridge.predict(sx.transform(X[b:]))[:,None]).ravel())
    assert np.allclose(pred,np.maximum(0,sy.inverse_transform(net.predict(sx.transform(X[b:]))[:,None]).ravel()))
    examples=[{'date':rows[i+14]['dteday'],'features':X[i].tolist(),'actual':float(y[i]),'prediction':float(pred[i-b]),'baseline':float(baseline[i-b])} for i in range(b,n)]
    report={'task':'Next-day daily bicycle demand','source_rows':len(rows),'usable_rows':n,'split':{'train':a,'validation':b-a,'test':n-b,'train_end':rows[a+13]['dteday'],'validation_end':rows[b+13]['dteday'],'test_start':rows[b+14]['dteday']},'protocol':'Chronological 60/20/20; architecture selected by validation MAE, then refit train+validation. Rolling one-day forecasts: observed earlier test days are available for subsequent predictions. No target-day weather, casual/registered counts or future demand.','validation_mae':scores,'chosen_neural_architecture':width,'overall_validation_winner':min(scores,key=scores.get),'test_mae':float(mean_absolute_error(y[b:],pred)),'test_rmse':float(mean_squared_error(y[b:],pred)**.5),'baseline_mae':float(mean_absolute_error(y[b:],baseline)),'ridge_test_mae':float(mean_absolute_error(y[b:],rp)),'loss_curve':net.loss_curve_,'iterations':net.n_iter_,'source_sha256':digest(p),'examples':examples,'worst_errors':sorted(examples,key=lambda e:abs(e['actual']-e['prediction']),reverse=True)[:10],'limits':'731 historical days from one system (2011–2012). Small CPU MLP; no multi-day fixed-origin guarantee, production deployment or causal claim. Neural model is published as an experiment even if Ridge wins validation.'}
    save(model,report);print(json.dumps({k:report[k] for k in ('test_mae','baseline_mae','ridge_test_mae','validation_mae')}))
if __name__=='__main__':train()
