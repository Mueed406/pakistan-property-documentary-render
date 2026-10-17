import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
export function assertFinalRights(){
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
