/*
 * Offline screenshot capture from a REAL WebGL2 frame state.
 * Requires npm install, npx playwright install chromium, FFmpeg, working GPU.
 * Source frame index, not browser framerate, controls animation state.
 */
import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {chromium} from 'playwright';
import {assertFinalRights} from './rights.mjs';

const args=new Map(process.argv.slice(2).filter(s=>s.startsWith('--')).map(s=>{
 const [k,...v]=s.slice(2).split('=');return [k,v.length?v.join('='):true];
}));
const final=args.get('mode')==='final';
if(final)assertFinalRights();
if(!final && args.has('all'))throw new Error('Technical stand-ins are NOT a complete fan film. Use --proof only.');
const width=Number(args.get('width')||1080),height=Number(args.get('height')||1920);
if(final && (width!==1080||height!==1920))throw new Error('Final output must be native 1080×1920');
if(!Number.isInteger(width)||!Number.isInteger(height)||width<270||height<480)throw new Error('Invalid capture size');
const timeline=JSON.parse(readFileSync('../../templates/fan-animation/poppy_90s_scene_manifest.json','utf8'));
const proofStart=1800,proofEnd=2760; // 30s–46s; stalker reveal + moving articulated chase
const shots=args.has('all')?timeline.shots.map(s=>({name:s.id,start:s.start_frame,end:s.end_frame_exclusive})):
 [{name:'PROOF_16S_NOT_FINAL',start:Number(args.get('start')||proofStart),end:Number(args.get('end')||proofEnd)}];
for(const s of shots)if(s.start<0||s.end>5400||s.end<=s.start||!Number.isInteger(s.start)||!Number.isInteger(s.end))throw new Error('Invalid frame selection');
mkdirSync('output',{recursive:true});
const sourceHash=createHash('sha256');
for(const path of ['src/main.ts','../../templates/fan-animation/poppy_90s_scene_manifest.json','RIGHTS_GATE.json'])sourceHash.update(readFileSync(path));
sourceHash.update(JSON.stringify({width,height,final}));
const fingerprint=sourceHash.digest('hex').slice(0,16);
const server=spawn('npm',['run','dev'],{stdio:'ignore'});
async function waitForServer(){
 for(let attempt=0;attempt<120;attempt++){
  if(server.exitCode!==null)throw new Error('Vite server exited');
  try{const r=await fetch('http://127.0.0.1:5173/');if(r.ok)return;}catch{}
  await new Promise(r=>setTimeout(r,250));
 }
 throw new Error('Vite dev server did not start');
}
let browser;
try{
 await waitForServer();
 browser=await chromium.launch({headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 page.on('pageerror',error=>console.error('Browser:',error.message));
 await page.goto('http://127.0.0.1:5173/?mode='+(final?'final':'technical')+'&capture=1',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.productionReady===true,{timeout:60000});
 const status=await page.evaluate(()=>window.engineStatus);
 if(final && status.mode!=='final-with-authorized-rigs')throw new Error('No validated imported rigs');
 console.log('Render stage: ',status,'resolution',width,height);
 for(const shot of shots){
  const output='output/'+shot.name+'_'+fingerprint+'.mp4';
  const metadata=output+'.json';
  if(existsSync(output)&&existsSync(metadata)){
   const old=JSON.parse(readFileSync(metadata,'utf8'));
   if(old.frames===shot.end-shot.start&&old.fingerprint===fingerprint){console.log('CACHED: '+output);continue;}
  }
  const temp=output+'.incomplete.mp4';
  const encoder=spawn('ffmpeg',['-hide_banner','-loglevel','error','-y',
   '-f','image2pipe','-vcodec','png','-framerate','60','-i','pipe:0',
   '-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',
   '-r','60','-movflags','+faststart',temp],{stdio:['pipe','inherit','inherit']});
  try{
   for(let i=shot.start;i<shot.end;i++){
    await page.evaluate(index=>window.renderFrame(index),i);
    const png=await page.screenshot({type:'png',animations:'disabled'});
    if(!encoder.stdin.write(png))await once(encoder.stdin,'drain');
    if((i-shot.start)%120===0)console.log(shot.name,'frame',i-shot.start,'/',shot.end-shot.start);
   }
   encoder.stdin.end();
   const [exitCode]=await once(encoder,'exit');
   if(exitCode!==0)throw new Error('FFmpeg exited '+exitCode);
   const {renameSync}=await import('node:fs');renameSync(temp,output);
   writeFileSync(metadata,JSON.stringify({start:shot.start,end:shot.end,frames:shot.end-shot.start,
    width,height,fps:60,fingerprint,mode:final?'final':'technical-standin',
    rights_release_authorized:final},null,2)+'\n');
   console.log('ENCODED '+output);
  }catch(e){encoder.stdin.destroy();encoder.kill('SIGKILL');throw e;}
 }
}finally{
 if(browser)await browser.close();
 server.kill('SIGTERM');
}
