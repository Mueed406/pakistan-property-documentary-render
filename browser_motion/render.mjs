#!/usr/bin/env node
/**
 * Browser motion compositor: deterministic HTML Canvas -> frame exact MP4.
 * Requires puppeteer-core (no browser download), Chrome or Edge, FFmpeg.
 * The script NEVER fetches third party web content; scenes load as local files.
 *
 * node browser_motion/render.mjs browser_motion/scene.html --out out.mp4 --fps 25 --seconds 7.5
 * For a fast smoke: --frames 18 --width 960 --height 540.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn,spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {once} from 'node:events';
import puppeteer from 'puppeteer-core';

function flag(n,defaultValue){const ix=process.argv.indexOf(n);return ix>=0?process.argv[ix+1]:defaultValue;}
const target=process.argv[2];
if(!target||target.startsWith('--'))throw new Error('Usage: render.mjs scene.html --out result.mp4 --fps 25 --seconds 7.5');
const file=path.resolve(target);
if(!fs.existsSync(file)||!file.toLowerCase().endsWith('.html'))throw new Error('A local HTML scene file is required');
const width=Number(flag('--width',1920)),height=Number(flag('--height',1080));
const fps=Number(flag('--fps',25)),seconds=Number(flag('--seconds',7.5));
const frames=Number(flag('--frames',Math.round(fps*seconds)));
const output=path.resolve(flag('--out','browser_motion_output.mp4'));
if(!Number.isInteger(width)||!Number.isInteger(height)||width<320||height<180||width>3840||height>2160)throw new Error('Invalid frame dimensions');
if(!Number.isInteger(fps)||fps<12||fps>60||!Number.isInteger(frames)||frames<1||frames>3600)throw new Error('Unreasonable framerate or duration');

const candidates=[
 process.env.CHROME_PATH,process.env.EDGE_PATH,
 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
 '/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser',
 '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
].filter(Boolean);
const browserPath=candidates.find(p=>fs.existsSync(p));
if(!browserPath)throw new Error('Chrome/Edge/Chromium not found; set CHROME_PATH');
const ffmpeg=process.env.FFMPEG_PATH||'ffmpeg';
if(spawnSync(ffmpeg,['-version'],{stdio:'ignore'}).status!==0)throw new Error('FFmpeg not available');
fs.mkdirSync(path.dirname(output),{recursive:true});
const browser=await puppeteer.launch({
 executablePath:browserPath,headless:true,
 args:['--disable-gpu-sandbox','--disable-dev-shm-usage','--no-first-run',...(process.platform==='linux'?['--no-sandbox']:[])]
});
let ff;
try{
 const page=await browser.newPage();
 await page.setViewport({width,height,deviceScaleFactor:1});
 const url=new URL(pathToFileURL(file).href);
 url.searchParams.set('width',String(width));url.searchParams.set('height',String(height));
if(flag('--scene',''))url.searchParams.set('scene',flag('--scene',''));
if(flag('--caption',''))url.searchParams.set('caption',flag('--caption',''));
 await page.goto(url.href,{waitUntil:'load',timeout:30000});
 await page.waitForFunction('window.__ready && typeof window.renderAt === "function"',{timeout:30000});
 const info=await page.evaluate(()=>window.motionInfo);
 console.log('SCENE READY',info);
 ff=spawn(ffmpeg,['-hide_banner','-loglevel','error','-y',
 '-f','image2pipe','-framerate',String(fps),'-vcodec','png','-i','pipe:0',
 '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
 '-movflags','+faststart',output],{stdio:['pipe','inherit','inherit']});
 ff.on('error',e=>console.error('FFmpeg launch error',e.message));
 for(let i=0;i<frames;i++){
  const t=i/fps;
  await page.evaluate((tm)=>window.renderAt(tm),t);
  const png=await page.screenshot({type:'png',captureBeyondViewport:false});
  if(i===0||i===Math.floor(frames/2)||i===frames-1){
   const label=String(i).padStart(4,'0');
   fs.writeFileSync(output+'.frame'+label+'.png',png);
  }
  if(!ff.stdin.write(png))await once(ff.stdin,'drain');
  if(i%25===0)console.log('Rendered frame',i+1,'/',frames);
 }
 ff.stdin.end();
 const [status]=await once(ff,'close');
 if(status!==0)throw new Error('FFmpeg encoding failed with code '+status);
 const st=fs.statSync(output);
 if(st.size<10000)throw new Error('MP4 unexpectedly small');
 console.log('RENDERED VALID FRAME-BY-FRAME VIDEO',output,'bytes:',st.size);
}catch(e){
 if(ff&&!ff.killed)ff.kill('SIGTERM');
 throw e;
}finally{await browser.close();}
