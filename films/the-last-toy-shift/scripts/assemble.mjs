import {readFileSync,existsSync,writeFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {assertFinalRights} from './rights.mjs';
assertFinalRights();
const plan=JSON.parse(readFileSync('../../templates/fan-animation/poppy_90s_scene_manifest.json','utf8'));
const paths=[];
for(const s of plan.shots){
 const {readdirSync}=await import('node:fs');
 const p=readdirSync('output').filter(x=>x.startsWith(s.id+'_')&&x.endsWith('.mp4'));
 if(p.length!==1)throw new Error('Expected exactly one encoded shot for '+s.id+' (found '+p.length+')');
 const meta=JSON.parse(readFileSync('output/'+p[0]+'.json','utf8'));
 if(meta.mode!=='final'||meta.start!==s.start_frame||meta.end!==s.end_frame_exclusive||
    meta.width!==1080||meta.height!==1920||meta.fps!==60)throw new Error('Shot metadata invalid: '+s.id);
 paths.push(p[0]);
}
const audio='public/assets/audio/mix.wav';
if(!existsSync(audio))throw new Error('Approved voice/music/SFX stereo mix missing');
const list=paths.map(p=>"file '"+p.replaceAll("'","'\\''")+"'").join('\n')+'\n';
writeFileSync('output/concat.txt',list);
function ff(args){
 const p=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y',...args],{stdio:'inherit'});
 if(p.status!==0)throw new Error('FFmpeg assembly failed');
}
ff(['-f','concat','-safe','0','-i','output/concat.txt','-i',audio,
 '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-ar','48000',
 '-b:a','256k','-pix_fmt','yuv420p','-t','90','-movflags','+faststart','output/The_Last_Toy_Shift_FINAL.mp4']);
console.log('Assembled pending objective FFprobe and visual+audio human QA');
