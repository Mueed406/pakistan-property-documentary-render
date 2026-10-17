import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
export function assertFinalRights(){
 const upstream=spawnSync('python3',['../../tools/video_production/validate_scene_manifest.py','--render-ready'],{encoding:'utf8'});
 if(upstream.status!==0)throw new Error('Upstream strict asset-registry gate failed (or Python missing): '+String(upstream.stdout||upstream.stderr).slice(0,1300));
 const gate=JSON.parse(readFileSync('RIGHTS_GATE.json','utf8'));
 const missing=[];
 if(gate.release_authorized!==true)missing.push('project release_authorized=false');
 for(const a of gate.assets){
  if(!a.approved_for_project || !a.license || !a.owner || !a.source_url || !a.sha256) {missing.push(a.id+': rights/provenance incomplete');continue;}
  if(!existsSync(a.path)){missing.push(a.id+': file not present');continue;}
  const actual=createHash('sha256').update(readFileSync(a.path)).digest('hex');
  if(actual.toLowerCase()!==String(a.sha256).toLowerCase())missing.push(a.id+': SHA256 mismatch');
 }
 if(missing.length)throw new Error('FINAL EXPORT BLOCKED:\n - '+missing.join('\n - '));
}
