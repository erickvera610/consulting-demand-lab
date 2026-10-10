import random,math
def forecast(train,horizon):
    if len(train)<14 or horizon<1:raise ValueError('Need 14 training points and positive horizon')
    n=len(train);mx=(n-1)/2;my=sum(train)/n
    slope=sum((i-mx)*(y-my) for i,y in enumerate(train))/sum((i-mx)**2 for i in range(n));intercept=my-slope*mx
    residual=[y-(intercept+slope*i) for i,y in enumerate(train)]
    weekday=[sum(residual[i] for i in range(d,n,7))/len(range(d,n,7)) for d in range(7)]
    return [max(0,intercept+slope*i+weekday[i%7]) for i in range(n,n+horizon)]
def mae(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
def run(p):
    noise=float(p.get('noise',5))
    if not 0<=noise<=50:raise ValueError('Noise must be 0 to 50')
    rng=random.Random(int(p.get('seed',42)));data=[100+.5*i+[10,5,0,-5,-10,20,15][i%7]+rng.gauss(0,noise) for i in range(112)]
    train,test=data[:84],data[84:];pred=forecast(train,28);baseline=[train[-7+i%7] for i in range(28)]
    return {'mae':mae(test,pred),'baseline_mae':mae(test,baseline),'train_days':84,'test_days':28,'actual':test,'predicted':pred,'note':'Synthetic demand; chronological holdout. Independent consulting-sector project, not affiliated with BCG.'}
