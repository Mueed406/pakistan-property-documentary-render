/**
 * Assemble all 11 frame-accurate real 3D Threadjaw clips and ALREADY VALIDATED
 * original 3-voice Kokoro 90s soundtrack. Creates a FULL-LENGTH WORKPRINT,
 * not a rights-cleared cinematic final. Never calls assertFinalRights.
 */
import {readFileSync,writeFileSync,readdirSync,existsSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const master=JSON.parse(readFileSync('../../templates/fan-animation/poppy_90s_scene_manifest.json','utf8'));
const args=new Map(process.argv.slice(2).map(s=>s.replace(/^--/,'').split('=')));
const audio=args.get('audio')||'audio/LAST_TOY_SHIFT_90S_ENGLISH_SFX_CLOUD_CPU_AUDITION_NOT_FINAL.m4a';
if(!existsSync(audio))throw Error('Actual 90-second recorded soundtrack absent: '+audio);
const expectedSha='4e9054332da14b9c1789d666bea4934860defedb5c46a8bf69b1c5cc587f3be7';
const audioSha=createHash('sha256').update(readFileSync(audio)).digest('hex');
if(audioSha!==expectedSha)throw Error('Audio has wrong SHA-256: '+audioSha);
function ffprobe(path){
 const cmd=spawnSync('ffprobe',['-v','error','-count_frames','-show_entries',
  'stream=codec_name,codec_type,width,height,avg_frame_rate,nb_read_frames,sample_rate,channels:format=duration',
  '-of','json',path],{encoding:'utf8',maxBuffer:1024*1024*4});
 if(cmd.status!==0)throw Error('ffprobe failed: '+path+' '+cmd.stderr);
 return JSON.parse(cmd.stdout);
}
const entries=[];let previousEnd=0,sourceFingerprint=null;let videoFrames=0;
for(const shot of master.shots){
 if(shot.start_frame!==previousEnd)throw Error('Gapped film shot: '+shot.id);
 previousEnd=shot.end_frame_exclusive;
 const prefix='THREADJAW_ORIGINAL_'+shot.frame_count+'FRAMES_'+shot.start_frame+'_'+shot.end_frame_exclusive+'_NOT_FINAL_';
 const candidates=readdirSync('output').filter(f=>f.startsWith(prefix)&&f.endsWith('.mp4'));
 if(candidates.length!==1)throw Error('Require EXACTLY ONE authentic source clip for '+shot.id+'; found '+candidates.length);
 const file=candidates[0];
 const metaPath='output/'+file+'.json';
 if(!existsSync(metaPath))throw Error('Missing frame-origin metadata for '+file);
 const meta=JSON.parse(readFileSync(metaPath,'utf8'));
 if(meta.mode!=='threadjaw-original'||meta.width!==360||meta.height!==640||
    meta.fps!==60||meta.frames!==shot.frame_count||meta.start!==shot.start_frame||
    meta.end!==shot.end_frame_exclusive||meta.rights_release_authorized!==false)
  throw Error('Invalid scene metadata: '+shot.id);
 if(sourceFingerprint===null)sourceFingerprint=meta.fingerprint;
 // Blender's GLB binary exporter is not bitwise deterministic across hosts;
 // fingerprints incorporate the generated GLB SHA. All source jobs share the
 // same pinned github SHA and pass rig/clip/manifest validation separately.
 // Preserve each fingerprint in QA rather than falsely requiring bitwise equality.
 const p=ffprobe('output/'+file);
 const v=p.streams.find(s=>s.codec_type==='video');
 if(!v||v.codec_name!=='h264'||v.width!==360||v.height!==640||v.avg_frame_rate!=='60/1'||
   Number(v.nb_read_frames)!==shot.frame_count)throw Error('Frame/codec mismatch for '+file);
 entries.push({shot:shot.id,file,sha256:createHash('sha256').update(readFileSync('output/'+file)).digest('hex'),
   frames:shot.frame_count,model_binary_fingerprint:meta.fingerprint});
 videoFrames+=shot.frame_count;
}
if(videoFrames!==5400||previousEnd!==5400)throw Error('Full 5400 frames not rendered: '+videoFrames);
const ap=ffprobe(audio);
const a=ap.streams.find(s=>s.codec_type==='audio');
if(!a||a.codec_name!=='aac'||a.sample_rate!=='48000'||a.channels!==2||Math.abs(Number(ap.format.duration)-90)>.07)
 throw Error('Invalid previously rendered full soundtrack');
writeFileSync('output/concat_workprint.txt',entries.map(e=>"file '"+e.file.replaceAll("'","'\\''")+"'").join('\n')+'\n');
function ff(args){
 const p=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y',...args],{stdio:'inherit'});
 if(p.status!==0)throw Error('ffmpeg assembly/upscale failed, exit '+p.status);
}
const direct='output/THE_LAST_TOY_SHIFT_FULL_90S_360X640_60FPS_WORKPRINT_NOT_FINAL.mp4';
ff(['-f','concat','-safe','0','-i','output/concat_workprint.txt',
 '-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-ar','48000',
 '-b:a','256k','-t','90','-movflags','+faststart',direct]);
const full=ffprobe(direct), v=full.streams.find(s=>s.codec_type==='video');
if(Number(v?.nb_read_frames)!==5400||Math.abs(Number(full.format.duration)-90)>.07)
 throw Error('Assembled workprint failed exact 90s/5400 frame QA');
const upscaled='output/THE_LAST_TOY_SHIFT_FULL_90S_1080X1920_UPSCALED_WORKPRINT_NOT_FINAL.mp4';
if(args.get('upscale')!=='false'){
 const suppliedSrt=args.get('srt');
 const baseFilter='scale=1080:1920:flags=lanczos,setsar=1,eq=contrast=1.06:brightness=0.009:saturation=1.06:gamma=1.03,unsharp=5:5:0.22:3:3:0';
 const subtitlesStyle="FontName=DejaVu Sans,Fontsize=9,PrimaryColour=&H00FFFFFF,OutlineColour=&H00202020,BackColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,Alignment=2,MarginV=28";
 if(suppliedSrt&&!existsSync(suppliedSrt))throw Error('The actual TTS cue timing SRT was not found: '+suppliedSrt);
 const videoFilter=suppliedSrt?baseFilter+",subtitles="+suppliedSrt+":force_style='"+subtitlesStyle+"'":baseFilter;
 ff(['-i',direct,'-map','0:v:0','-map','0:a:0',
  '-vf',videoFilter,
  '-c:v','libx264','-preset','superfast','-crf','21','-pix_fmt','yuv420p',
  '-r','60','-c:a','copy','-movflags','+faststart',upscaled]);
 const probe=ffprobe(upscaled), video=probe.streams.find(s=>s.codec_type==='video');
 if(video.width!==1080||video.height!==1920||Number(video.nb_read_frames)!==5400||
   Math.abs(Number(probe.format.duration)-90)>.07)throw Error('Upscaled video QA failed');
}
const qa={status:'TECHNICALLY COMPLETE FULL 90-SECOND WORKPRINT, ARTISTIC GATE NOT PASSED',
 release_authorized:false,native_render_size:'360x640',upscaled_size:'1080x1920',upscaling_creates_no_new_detail:true,
 runtime_seconds:90,video_frames:5400,frame_rate:60,
 scenes:entries,first_shot_fingerprint:sourceFingerprint,git_source_sha:process.env.GITHUB_SHA||null,
 audio_sha256:audioSha,audio_source:'verified preexisting Kokoro original English/SFX full soundtrack',
 direct_sha256:createHash('sha256').update(readFileSync(direct)).digest('hex'),
 burned_in_subtitles:args.get('srt')||null,
 upscale_sha256:existsSync(upscaled)?createHash('sha256').update(readFileSync(upscaled)).digest('hex'):null,
 limitations:'Unapproved creature quality/scene blocking; primitive toy stand-ins, not final cinematic rig acting, source only 360p, soundtrack audition TTS and scripted SFX, noncanon fan rights review required.'};
writeFileSync('output/FULL_90S_WORKPRINT_QA.json',JSON.stringify(qa,null,2)+'\n');
console.log('FULL 5400-FRAME 90S VIDEO WORKPRINT QC PASS; ARTISTIC FINAL QC OPEN');
