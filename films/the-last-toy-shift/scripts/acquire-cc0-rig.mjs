/**
 * Authoritative, pinned CC0 skinned-actor TECHNICAL TEST ASSET ONLY.
 * Source project: mrdoob/three.js (not an extracted game asset).
 * Original model Tomas Laulhe, modifications Don McCurdy. CC0-1.0.
 * SHA is checked against pinned model bytes before writing.
 */
import {createHash} from 'node:crypto';
import {readFileSync,existsSync,mkdirSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
const url='https://raw.githubusercontent.com/mrdoob/three.js/eba30de865cfbf31ac736f792defd9a60ff28d57/examples/models/gltf/RobotExpressive/RobotExpressive.glb';
const expected='047f5e5fb3bb6d378bd1df16ca6137f2a596c99b3a1b5690b4020c05aaf6f319';
const path=join('public','assets','cc0_robot_expressive.glb');
const digest=x=>createHash('sha256').update(x).digest('hex');
let bytes;
if(existsSync(path) && digest(readFileSync(path))===expected){
 bytes=readFileSync(path);
 console.log('PASS: verified cached CC0 GLB');
}else{
 const response=await fetch(url,{redirect:'follow',signal:AbortSignal.timeout(60000)});
 if(!response.ok)throw new Error('Source download failed '+response.status);
 bytes=Buffer.from(await response.arrayBuffer());
 if(digest(bytes)!==expected)throw new Error('Pinned upstream hash mismatch; refusing unreviewed binary: '+digest(bytes));
 mkdirSync('public/assets',{recursive:true});
 writeFileSync(path,bytes);
 console.log('PASS: downloaded authoritative CC0 rig:',bytes.length,'bytes');
}
if(bytes.subarray(0,4).toString('ascii')!=='glTF')throw new Error('Invalid GLB header');
const jsonLength=bytes.readUInt32LE(12);
const jsonTag=bytes.readUInt32LE(16);
if(jsonTag!==0x4e4f534a)throw new Error('GLB JSON chunk missing');
const json=JSON.parse(bytes.subarray(20,20+jsonLength).toString('utf8').trim());
if(!json.skins?.length||!json.animations?.length)throw new Error('No actual skeletal rigs or animation clips');
const clips=json.animations.map(x=>x.name);
if(!clips.includes('Running'))throw new Error('Expected Running clip absent');
console.log('PASS: hash=',digest(bytes),'skins=',json.skins.length,'clips=',clips.join(', '));
