const assert=require('node:assert/strict');
const {runEnhanced,evaluateSeries}=require('./enhanced.js');const r=runEnhanced({dataset:'airpassengers'});assert.equal(r.test_days,12);const data=Array.from({length:168},(_,i)=>100+i*.4+i%7),a=evaluateSeries(data,7,28);data.splice(140,28,...Array(28).fill(999));const b=evaluateSeries(data,7,28);assert.deepEqual(a.model_selection,b.model_selection);assert.deepEqual(a.predicted,b.predicted);
console.log('Enhanced behavior tests passed');
