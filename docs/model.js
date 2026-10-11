function infer(p,m){
 if(m.task==='demand'){
  if(!Array.isArray(p.features)||p.features.length!==m.features.length||p.features.some(v=>typeof v!=='number'||!Number.isFinite(v)))throw Error('Expected finite numeric features');
  let x=p.features.map((v,i)=>(v-m.mean[i])/m.scale[i]);
  m.weights.forEach((w,l)=>{let y=m.biases[l].map((b,j)=>b+x.reduce((s,v,i)=>s+v*w[i][j],0));x=l<m.weights.length-1?y.map(v=>Math.max(0,v)):y});
  return {prediction:Math.max(0,x[0]*m.target_scale+m.target_mean)};
 }
 if(typeof p.text!=='string'||!p.text.trim()||p.text.length>10000)throw Error('Text must contain 1–10000 characters');
 let x=Array(m.idf.length).fill(0);(p.text.toLowerCase().match(/[a-z][a-z]+/g)||[]).forEach(t=>{if(Object.prototype.hasOwnProperty.call(m.vocabulary,t))x[m.vocabulary[t]]++});
 x=x.map((v,i)=>v*m.idf[i]);let norm=Math.sqrt(x.reduce((s,v)=>s+v*v,0));if(!norm)return {label:null,probabilities:{},out_of_vocabulary:true};x=x.map(v=>v/norm);
 let z=m.weights.map((w,i)=>m.biases[i]+w.reduce((s,v,j)=>s+v*x[j],0));let e=z.map(v=>Math.exp(v-Math.max(...z))),sum=e.reduce((s,v)=>s+v,0),q=e.map(v=>v/sum);
 return {label:m.classes[q.indexOf(Math.max(...q))],probabilities:Object.fromEntries(m.classes.map((c,i)=>[c,q[i]])),out_of_vocabulary:false};
}
if(typeof module!=='undefined')module.exports={infer};
