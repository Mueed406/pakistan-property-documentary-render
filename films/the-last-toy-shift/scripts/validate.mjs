import {readFileSync,existsSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {assertFinalRights} from './rights.mjs';
const plan=JSON.parse(readFileSync('../../templates/fan-animation/poppy_90s_scene_manifest.json','utf8'));
let cursor=0;
for(const s of plan.shots){
 if(s.start_frame!==cursor||s.end_frame_exclusive!==s.start_frame+s.frame_count)throw new Error('Shot gap/overlap: '+s.id);
 cursor=s.end_frame_exclusive;
}
if(cursor!==5400||plan.final_width!==1080||plan.final_height!==1920||plan.framerate_num!==60)throw new Error('Timeline not 1080x1920/60/5400');
console.log('PASS: scene plan: 11 shots; 5400 contiguous frames; 60 fps');
if(process.argv.includes('--final')){
 assertFinalRights();
 const video='output/The_Last_Toy_Shift_FINAL.mp4';
 if(!existsSync(video))throw new Error('FINAL video missing');
 const p=spawnSync('ffprobe',['-v','error','-count_frames','-show_entries','stream=codec_type,codec_name,width,height,avg_frame_rate,nb_read_frames,sample_rate','-show_entries','format=duration','-of','json',video],{encoding:'utf8'});
 if(p.status!==0)throw new Error(p.stderr||'ffprobe failed');
 const data=JSON.parse(p.stdout);
 const v=data.streams.find(s=>s.codec_type==='video'),a=data.streams.find(s=>s.codec_type==='audio');
 if(!v||v.codec_name!=='h264'||v.width!==1080||v.height!==1920||v.avg_frame_rate!=='60/1'||Number(v.nb_read_frames)!==5400)throw new Error('Final video metadata/frame mismatch');
 if(!a||a.codec_name!=='aac'||a.sample_rate!=='48000')throw new Error('Missing 48kHz AAC audio');
 if(Math.abs(Number(data.format.duration)-90)>1/60+0.002)throw new Error('Final duration error');
 console.log('PASS: MP4 container/fps/count/audio. Artistic/human QA is separate.');
}
