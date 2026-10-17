import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
const source=resolve('../../templates/fan-animation/poppy_90s_scene_manifest.json');
const plan=JSON.parse(readFileSync(source,'utf8'));
if(plan.frame_count!==5400 || plan.framerate_num!==60 || plan.shots.length!==11) throw new Error('Unexpected timeline; do not silently change the film');
let cursor=0;
for(const s of plan.shots){if(s.start_frame!==cursor || s.end_frame_exclusive!==cursor+s.frame_count)throw new Error('Noncontiguous shot: '+s.id);cursor=s.end_frame_exclusive;}
if(cursor!==5400)throw new Error('Manifest total mismatch');
mkdirSync('public',{recursive:true});
writeFileSync('public/scene_manifest.json',JSON.stringify(plan,null,2)+'\n');
console.log('Synchronized canonical 5,400-frame, 11-shot timeline');
