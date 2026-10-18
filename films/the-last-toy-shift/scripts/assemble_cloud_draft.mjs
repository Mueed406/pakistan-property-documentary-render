/**
 * Strict 11-shot review-film builder.
 * This is NOT the production/release final: the rights gate stays closed.
 * Native 540x960 source; 1080x1920 delivery is upscaled, never called native.
 */
import {existsSync,readdirSync,readFileSync,writeFileSync,mkdirSync,statSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const plan=JSON.parse(readFileSync('../../templates/fan-animation/poppy_90s_scene_manifest.json','utf8'));
const rights=JSON.parse(readFileSync('RIGHTS_GATE.json','utf8'));
if(rights.release_authorized!==false)throw new Error('This script is DRAFT ONLY and cannot authorize release');
if(plan.shots.length!==11 || plan.frame_count!==5400)throw new Error('Expected 11 shots and 5400 frames');
const dir='output/segments';
const sourceAudio='output/cloud-audio/LAST_TOY_SHIFT_90S_ENGLISH_SFX_CLOUD_CPU_AUDITION_NOT_FINAL.m4a';
if(!existsSync(sourceAudio))throw new Error('No real English soundtrack available: '+sourceAudio);
mkdirSync('output/assembled',{recursive:true});
function call(bin,args,options={}){
 const v=spawnSync(bin,args,{encoding:'utf8',maxBuffer:15*1024*1024,...options});
 if(v.status!==0)throw new Error(bin+' failed: '+(v.stderr||'').slice(-2500));
 return (v.stdout||'').trim();
}
function probe(filename,frames){
 const j=JSON.parse(call('ffprobe',['-hide_banner','-v','error','-count_frames','-show_entries',
   'format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate,nb_read_frames,sample_rate,channels',
   '-of','json',filename]));
 const v=j.streams.find(x=>x.codec_type==='video');
 if(!v||v.width!==540||v.height!==960||v.avg_frame_rate!=='60/1'||Number(v.nb_read_frames)!==frames)
  throw new Error('Clip/frame validation failed '+filename+' : '+JSON.stringify(v));
 return j;
}
const clips=[];
for(const shot of plan.shots){
 const a=Number(shot.start_frame),b=Number(shot.end_frame_exclusive);
 const expected=b-a;
 const all=readdirSync(dir).filter(f=>f.startsWith('THREADJAW_ORIGINAL_'+expected+'FRAMES_'+a+'_'+b+'_NOT_FINAL_') && f.endsWith('.mp4'));
 if(all.length!==1)throw new Error('Missing / duplicate source segment for '+shot.id+': '+JSON.stringify(all));
 const file=all[0],src=dir+'/'+file;
 const metaFile=src+'.json';
 if(!existsSync(metaFile))throw new Error('Missing frame/rights metadata '+metaFile);
 const m=JSON.parse(readFileSync(metaFile,'utf8'));
 if(m.start!==a||m.end!==b||m.frames!==expected||m.width!==540||m.height!==960||m.fps!==60||m.mode!=='threadjaw-original'||m.rights_release_authorized!==false)
  throw new Error('Segment metadata invalid for '+shot.id);
 probe(src,expected);
 clips.push({scene:shot.id,start:a,end:b,frames:expected,file});
 console.log('PASS segment '+shot.id+' '+expected+'f; '+Math.round(statSync(src).size/1024)+'KiB');
}
if(clips.reduce((sum,x)=>sum+x.frames,0)!==5400)throw new Error('Shot frame coverage does not total 5400');
const names=clips.map(x=>"file '../segments/"+x.file.replaceAll("'","'\\''")+"'").join('\n')+'\n';
writeFileSync('output/assembled/shots.txt',names);
const temp='output/assembled/VIDEO_ONLY_90S_540x960.mp4';
call('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','concat','-safe','0',
              '-i','output/assembled/shots.txt','-an','-c:v','copy',
              '-movflags','+faststart',temp]);
probe(temp,5400);
const native='output/assembled/The_Last_Toy_Shift_COMPLETE_90S_540x960_60FPS_REVIEW_ONLY.mp4';
call('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',temp,'-i',sourceAudio,
 '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-shortest',
 '-movflags','+faststart',native]);
let j=probe(native,5400);
const a=j.streams.find(x=>x.codec_type==='audio');
if(!a||a.codec_name!=='aac'||Number(a.sample_rate)!==48000||a.channels!==2)
 throw new Error('Missing 48kHz stereo AAC');
if(Math.abs(Number(j.format.duration)-90)>.07)throw new Error('Not precisely 90sec: '+j.format.duration);
const big='output/assembled/The_Last_Toy_Shift_COMPLETE_90S_1080x1920_UPSCALED_DRAFT.mp4';
call('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',native,
 '-vf','scale=1080:1920:flags=lanczos,eq=contrast=1.07:saturation=0.91,unsharp=5:5:0.33',
 '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
 '-pix_fmt','yuv420p','-r','60','-frames:v','5400','-c:a','aac','-b:a','192k',
 '-movflags','+faststart',big]);
const biggest=JSON.parse(call('ffprobe',['-hide_banner','-v','error','-count_frames',
 '-show_entries','format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_read_frames,sample_rate,channels',
 '-of','json',big]));
const bv=biggest.streams.find(x=>x.codec_type==='video'),ba=biggest.streams.find(x=>x.codec_type==='audio');
if(!bv||bv.width!==1080||bv.height!==1920||bv.avg_frame_rate!=='60/1'||Number(bv.nb_read_frames)!==5400)
 throw new Error('Upscaled video invalid '+JSON.stringify(bv));
if(!ba||ba.codec_name!=='aac'||Number(ba.sample_rate)!==48000)
 throw new Error('Upscaled audio invalid');
if(Math.abs(Number(biggest.format.duration)-90)>.07)throw new Error('Upscaled runtime != 90s');
const sha=file=>createHash('sha256').update(readFileSync(file)).digest('hex');
const report={status:'PASS TECHNICAL ASSEMBLY / ARTISTIC QC NOT APPROVED',
 created_at:new Date().toISOString(),all_scenes:11,actual_frames:5400,actual_render_resolution:[540,960],
 real_fps:60,output_duration:90,
 upscale_disclosure:'1080p output UPSCALED FROM 540x960; not a native 1080p render',
 copyright_clearance:'ORIGINAL Threadjaw + three-model Kokoro voices + code-authored soundscape; no release authorization',
 artist_review:'FAILED / PENDING',
 source_shots:clips,
 files:[native,big].map(f=>({name:f.split('/').at(-1),bytes:statSync(f).size,sha256:sha(f)})),
 references:{cloud_voice_run:39097760161,threadjaw_source_run:39063523037}};
writeFileSync('output/assembled/CLOUD_FILM_90S_QA_NOT_FINAL.json',JSON.stringify(report,null,2)+'\n');
console.log('FILM_CUT_PASS',JSON.stringify({files:report.files,frames:5400,duration:90,scene_count:11},null,2));
