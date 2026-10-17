import {spawnSync} from 'node:child_process';
const path=process.argv[2];
if(!path)throw new Error('Pass an encoded MP4 path');
const p=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,avg_frame_rate,nb_read_frames','-of','json',path],{encoding:'utf8'});
if(p.status!==0)throw new Error(p.stderr);
const v=JSON.parse(p.stdout).streams[0];
if(v.avg_frame_rate!=='60/1'||!Number(v.nb_read_frames))throw new Error('Not native 60fps');
console.log('Verified encoded frames=',v.nb_read_frames,'resolution=',v.width+'x'+v.height,'rate=',v.avg_frame_rate);
console.log('WARNING: objective technical check only; rig motion/voices/rights require separate review');
