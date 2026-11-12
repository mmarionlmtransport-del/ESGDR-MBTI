const {chromium}=require('playwright');
const [,,html,out,mode]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+html);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
const fs=require('fs');fs.mkdirSync(out,{recursive:true});
if(mode==='test'){for(const t of (process.env.TS||"2,4.2,7.5,9.6,12.5,13.3,15.1,17.9,18.8,20.5,23.8,27.5,30.8").split(",").map(Number)){await p.evaluate(([t])=>render(t,1),[t]);await p.screenshot({path:`${out}/t_${t}.jpg`,type:'jpeg',quality:70});}}
else{const N=32*30;for(let f=0;f<N;f++){await p.evaluate(([t,f])=>render(t,f),[f/30,f]);await p.screenshot({path:`${out}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});}}
await b.close();})();
