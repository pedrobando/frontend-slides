// NODE_PATH=motion/node_modules node stills.js motion/dist/NN.html out.png t1 t2 ... -> contact sheet, clip on the slide colour
const {chromium}=require('playwright');const path=require('path');const {execSync}=require('child_process');const fs=require('fs');
(async()=>{const [html,out,...ts]=process.argv.slice(2);
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:1200}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+path.resolve(html)+'?render');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 await p.evaluate(()=>{document.documentElement.style.background='#1B252F';document.body.style.background='#1B252F';});
 const st=await p.$('#stage');const dir=fs.mkdtempSync('/tmp/st');
 for(let i=0;i<ts.length;i++){await p.evaluate(t=>seek(t),+ts[i]);await st.screenshot({path:`${dir}/${String(i).padStart(3,'0')}.png`});}
 await b.close();
 const cols=Math.min(+process.env.COLS||2,ts.length),rows=Math.ceil(ts.length/cols);
 execSync(`ffmpeg -loglevel error -y -i ${dir}/%03d.png -vf "scale='min(900,iw)':-1,tile=${cols}x${rows}:padding=6:color=white" -frames:v 1 ${out}`);
 if(errs.length) console.log('ERR',errs); else console.log('ok',out);})();
