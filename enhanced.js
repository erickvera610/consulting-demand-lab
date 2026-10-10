const AIR=[112.0, 118.0, 132.0, 129.0, 121.0, 135.0, 148.0, 148.0, 136.0, 119.0, 104.0, 118.0, 115.0, 126.0, 141.0, 135.0, 125.0, 149.0, 170.0, 170.0, 158.0, 133.0, 114.0, 140.0, 145.0, 150.0, 178.0, 163.0, 172.0, 178.0, 199.0, 199.0, 184.0, 162.0, 146.0, 166.0, 171.0, 180.0, 193.0, 181.0, 183.0, 218.0, 230.0, 242.0, 209.0, 191.0, 172.0, 194.0, 196.0, 196.0, 236.0, 235.0, 229.0, 243.0, 264.0, 272.0, 237.0, 211.0, 180.0, 201.0, 204.0, 188.0, 235.0, 227.0, 234.0, 264.0, 302.0, 293.0, 259.0, 229.0, 203.0, 229.0, 242.0, 233.0, 267.0, 269.0, 270.0, 315.0, 364.0, 347.0, 312.0, 274.0, 237.0, 278.0, 284.0, 277.0, 317.0, 313.0, 318.0, 374.0, 413.0, 405.0, 355.0, 306.0, 271.0, 306.0, 315.0, 301.0, 356.0, 348.0, 355.0, 422.0, 465.0, 467.0, 404.0, 347.0, 305.0, 336.0, 340.0, 318.0, 362.0, 348.0, 363.0, 435.0, 491.0, 505.0, 404.0, 359.0, 310.0, 337.0, 360.0, 342.0, 406.0, 396.0, 420.0, 472.0, 548.0, 559.0, 463.0, 407.0, 362.0, 405.0, 417.0, 391.0, 419.0, 461.0, 472.0, 535.0, 622.0, 606.0, 508.0, 461.0, 390.0, 432.0];
function randomGenerator(seed=42) {
    let state=seed>>>0;
    return ()=> {
        state=(1664525*state+1013904223)>>>0;
        return state/4294967296;
    }
    ;
}
function normal(random) {
    return Math.sqrt(-2*Math.log(Math.max(random(),1e-10)))*Math.cos(2*Math.PI*random());
}
function forecastModel(train,horizon,period,model) {
    if(model==='seasonal_naive')return Array.from( {
        length:horizon
    }
    ,(_,i)=>train[train.length-period+i%period]);
    const log=model==='log_trend',values=log?train.map(v=>Math.log(Math.max(v,.001))):train,n=values.length,mx=(n-1)/2,my=values.reduce((a,b)=>a+b,0)/n,a=values.reduce((s,v,i)=>s+(i-mx)*(v-my),0)/values.reduce((s,v,i)=>s+(i-mx)**2,0),b=my-a*mx,seasonal=Array.from( {
        length:period
    }
    ,(_,d)=> {
        let sum=0,count=0;values.forEach((v,i)=> {
            if(i%period===d) {
                sum+=v-a*i-b;count++;
            }
        }
        );return sum/count;
    }
    );
    return Array.from( {
        length:horizon
    }
    ,(_,j)=> {
        const i=n+j,v=a*i+b+seasonal[i%period];return log?Math.exp(v):Math.max(0,v);
    }
    );
}
function evaluateSeries(data,period,horizon) {
    const end=data.length-horizon,origins=[end-3*horizon,end-2*horizon,end-horizon],mae=(a,b)=>a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)/a.length,errors= {
    }
    ,trials=['seasonal_naive','linear_trend','log_trend'].map(model=> {
        const folds=[];errors[model]=[];for(const origin of origins) {
            const prediction=forecastModel(data.slice(0,origin),horizon,period,model),actual=data.slice(origin,origin+horizon);folds.push( {
                train_end_exclusive:origin,validation_end_exclusive:origin+horizon,mae:mae(actual,prediction)
            }
            );errors[model].push(...actual.map((v,i)=>Math.abs(v-prediction[i])));
        }
        return  {
            model,validation_mae:folds.reduce((s,f)=>s+f.mae,0)/3,folds
        }
        ;
    }
    ),selected=trials.reduce((a,b)=>a.validation_mae<b.validation_mae?a:b).model,predicted=forecastModel(data.slice(0,end),horizon,period,selected),actual=data.slice(end),baseline=forecastModel(data.slice(0,end),horizon,period,'seasonal_naive'),residual=errors[selected].sort((a,b)=>a-b),radius=residual[Math.min(residual.length-1,Math.ceil(.8*(residual.length+1))-1)],lower=predicted.map(v=>Math.max(0,v-radius)),upper=predicted.map(v=>v+radius);
    return  {
        selected_model:selected,model_selection:trials,mae:mae(actual,predicted),baseline_mae:mae(actual,baseline),actual,predicted,baseline,lower,upper,interval_target:.8,interval_test_coverage:actual.filter((v,i)=>lower[i]<=v&&v<=upper[i]).length/horizon,train_days:end,test_days:horizon,period
    }
    ;
}
function runEnhanced(p= {
}
) {
    const real=p.dataset==='airpassengers',noise=Number(p.noise??5);
    if(!Number.isFinite(noise)||noise<0||noise>50)throw Error('Noise 0–50 required');
    const random=randomGenerator(p.seed??42),data=real?AIR: Array.from( {
        length:168
    }
    ,(_,i)=>Math.max(1,100+.5*i+[10,5,0,-5,-10,20,15][i%7]+noise*normal(random)));
    return  {
        ...evaluateSeries(data,real?12:7,real?12:28),dataset:real?'airpassengers':'synthetic',unit:real?'thousands of passengers per month':'fictional units per day',note:'Three earlier folds choose the model. Final chronological holdout is untouched during selection. Empirical intervals have no guaranteed coverage.'
    }
    ;
}
if(typeof module!=='undefined')module.exports= {
    runEnhanced,evaluateSeries,forecastModel
}
;
