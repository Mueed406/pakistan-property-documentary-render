import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

/*
 * Original procedural TECHNICAL STAND-IN STAGE (not final character art).
 * No ripped proprietary meshes, sounds, footage or extracted game assets.
 * All time is derived from an integer frame index / 60, never wall time.
 */

type Shot = {id:string; start_frame:number; frame_count:number; end_frame_exclusive:number};
type Plan = {frame_count:number; shots:Shot[]};
declare global {
  interface Window {
    renderFrame:(index:number)=>void;
    productionReady:boolean;
    engineStatus:{mode:string;renderer:string;frames:number;models:string[];rigging?:{skinnedMeshes:number;clips:string[];selectedClip:string}|null};
  }
}

const displayMode=new URLSearchParams(location.search).get('mode') || 'technical';
const rigProof=displayMode==='rigproof';
const threadjawProof=displayMode==='threadjaw';
const technicalMode=displayMode!=='final';
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setPixelRatio(1);
renderer.setSize(innerWidth,innerHeight);
renderer.setClearColor(0x070b0e,1);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.48;
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
document.body.insertBefore(renderer.domElement,document.body.firstChild);

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x0b1015);
scene.fog=new THREE.FogExp2(0x121d20,0.018);
const camera=new THREE.PerspectiveCamera(58,innerWidth/innerHeight,0.08,180);
const root=new THREE.Group();
scene.add(root);
const dark=new THREE.MeshStandardMaterial({color:0x252e34,roughness:.76,metalness:.65});
const concrete=new THREE.MeshStandardMaterial({color:0x47515a,roughness:.95,metalness:.05});
const metal=new THREE.MeshStandardMaterial({color:0x455257,metalness:.85,roughness:.31});
const copper=new THREE.MeshStandardMaterial({color:0x866c4f,metalness:.68,roughness:.42});
const blue=new THREE.MeshPhysicalMaterial({color:0x1769a6,roughness:.85,metalness:.04});
const yellow=new THREE.MeshStandardMaterial({color:0xc9a457,metalness:.45,roughness:.52});
const screenMat=new THREE.MeshStandardMaterial({color:0x1d8b7b,emissive:0x19c4ab,emissiveIntensity:.74,roughness:.3});
const dangerMat=new THREE.MeshStandardMaterial({color:0x42090a,emissive:0xd6210e,emissiveIntensity:1.2});
const eyeWhite=new THREE.MeshPhysicalMaterial({color:0xf1e6d4,roughness:.14,clearcoat:1});
const iris=new THREE.MeshStandardMaterial({color:0x07181c,roughness:.1});

function box(w:number,h:number,d:number,x:number,y:number,z:number,mat:THREE.Material,parent:THREE.Object3D=root){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function ball(r:number,x:number,y:number,z:number,mat:THREE.Material,parent:THREE.Object3D=root){
 const m=new THREE.Mesh(new THREE.SphereGeometry(r,20,12),mat);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function beam(a:THREE.Vector3,b:THREE.Vector3,r:number,mat:THREE.Material,parent:THREE.Object3D=root){
 const dir=b.clone().sub(a), length=dir.length();
 const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,length,12),mat);
 m.position.copy(a).addScaledVector(dir,.5);
 m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());
 m.castShadow=true;parent.add(m);return m;
}
function vec(x:number,y:number,z:number){return new THREE.Vector3(x,y,z);}
function smooth(t:number){const u=THREE.MathUtils.clamp(t,0,1);return u*u*(3-2*u);}
function texture(seed:number,base:[number,number,number]){
 const el=document.createElement('canvas');el.width=256;el.height=256;
 const ctx=el.getContext('2d')!,img=ctx.createImageData(256,256);
 for(let y=0;y<256;y++)for(let x=0;x<256;x++){
  let n=(x*374761393+y*668265263+seed*1442695041)|0;
  n=Math.imul(n^(n>>>13),1274126177);
  const grit=((n>>>16)&255)/255-.5;
  const stain=Math.sin(x*.045+y*.018+seed)*.13;
  const c=THREE.MathUtils.clamp(grit*.24+stain,-.4,.4);
  const i=(y*256+x)*4;
  for(let k=0;k<3;k++)img.data[i+k]=Math.round(THREE.MathUtils.clamp(base[k]*(1+c),0,255));
  img.data[i+3]=255;
 }
 ctx.putImageData(img,0,0);
 const out=new THREE.CanvasTexture(el);out.colorSpace=THREE.SRGBColorSpace;
 out.wrapS=out.wrapT=THREE.RepeatWrapping;out.repeat.set(4,10);
 return out;
}
const floorMat=new THREE.MeshStandardMaterial({map:texture(11,[58,64,65]),metalness:.24,roughness:.91});
const wallMat=new THREE.MeshStandardMaterial({map:texture(27,[79,89,90]),metalness:.15,roughness:.94});
if(rigProof || threadjawProof){
 // Genuine CC0 Poly Haven three-map surface test; no source package is bundled in the repo.
 // API metadata, MD5 and SHA256 are checked by scripts/acquire-cc0-pbr.mjs.
 const imageLoader=new THREE.TextureLoader();
 const paths=['/assets/pbr/rusty_metal_sheet_diff.jpg','/assets/pbr/rusty_metal_sheet_nor_gl.jpg','/assets/pbr/rusty_metal_sheet_rough.jpg'];
 const maps=await Promise.all(paths.map(path=>imageLoader.loadAsync(path)));
 for(const tx of maps){tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(1,3);tx.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());}
 maps[0].colorSpace=THREE.SRGBColorSpace;
 metal.color.set(0xffffff);
 metal.map=maps[0];metal.normalMap=maps[1];metal.roughnessMap=maps[2];
 metal.normalScale.set(.36,.36);metal.metalness=.68;metal.roughness=.8;metal.needsUpdate=true;
}
box(12,.35,110,0,-.28,-19,floorMat);
box(.32,8,110,-5.6,3.5,-19,wallMat);
box(.32,8,110,5.6,3.5,-19,wallMat);
box(12,.3,110,0,7.6,-19,dark);
const stripeMat=new THREE.MeshStandardMaterial({color:0x887747,roughness:.74});
for(let z=26;z>=-70;z-=7){
 for(const x of [-5.2,5.2]){
  box(.6,7.6,.36,x,3.65,z,metal);
  box(1,.14,.7,x,6.15,z,copper);
 }
 beam(vec(-5.2,7.25,z),vec(5.2,7.25,z),.15,metal);
 box(.045,.004,3,-3.9,-.075,z,stripeMat);
 box(.045,.004,3,3.9,-.075,z,stripeMat);
}
for(let x of [-3.7,3.7]){
 beam(vec(x,6.2,25),vec(x,6.2,-70),.18,copper);
 beam(vec(x,5.8,25),vec(x,5.8,-70),.12,metal);
}
for(let z=22;z>=-63;z-=8){
 for(const x of [-3.5,3.5])box(2.5,.17,1.35,x,1.12,z,copper);
}
const overhead:THREE.SpotLight[]=[];
for(let z=10;z>=-48;z-=8){
 const light=new THREE.SpotLight(z<-29?0xee503a:0x8fcbe2,50,23,.55,.68,1.5);
 light.position.set(0,7.05,z);light.target.position.set(0,0,z-1);
 light.castShadow=(Math.round((10-z)/8)%2===0);light.shadow.mapSize.set(1024,1024);
 scene.add(light,light.target);overhead.push(light);
 box(1.2,.1,.45,0,7.09,z,metal);
 box(.7,.055,.3,0,6.99,z,new THREE.MeshStandardMaterial({color:0xb7c9d2,emissive:0xc4e4ee,emissiveIntensity:1.1}));
}
scene.add(new THREE.HemisphereLight(0x92abb7,0x372c27,2.1));
const rim=new THREE.PointLight(0xd44d2d,23,22);rim.position.set(2.5,3,-30);scene.add(rim);
const coldFill=new THREE.SpotLight(0xb6ddf3,145,36,.67,.7,1.45);
coldFill.position.set(3.5,6.6,-20);coldFill.target.position.set(0,1.8,-28);
coldFill.castShadow=true;coldFill.shadow.mapSize.set(1024,1024);scene.add(coldFill,coldFill.target);

// Conveyor: all components occupy real world-space, with perspective and occlusion.
const conveyor=new THREE.Group();root.add(conveyor);
box(2.1,.23,35,0,.81,-9,dark,conveyor);
box(.14,.36,35,-1.02,.92,-9,metal,conveyor);
box(.14,.36,35,1.02,.92,-9,metal,conveyor);
for(let z=7.8;z>=-26;z-=.75){
 const m=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,1.8,12),copper);
 m.rotation.z=Math.PI/2;m.position.set(0,.8,z);m.castShadow=true;conveyor.add(m);
}
for(let z=7;z>=-26;z-=5)for(const x of [-.83,.83])box(.16,.8,.16,x,.35,z,metal,conveyor);
const boxes:THREE.Mesh[]=[];
for(let i=0;i<11;i++)boxes.push(box(.55+(i%3)*.1,.46+(i%2)*.23,.6,0,1.25,0,i%2?copper:concrete));

// Articulated ORIGINAL toy rig, engineering stand-in only.
// RELEASE requires licensed and validated skinned GLB via GLTFLoader.
function makeToy(height:number,bodyMat:THREE.Material){
 const rig=new THREE.Group(),pelvis=new THREE.Group();rig.add(pelvis);
 const torso=ball(.34*height,0,.59*height,0,bodyMat,pelvis);
 torso.scale.set(1.04,1.25,.72);
 const neck=new THREE.Group();neck.position.y=.89*height;pelvis.add(neck);
 ball(.28*height,0,.18*height,0,bodyMat,neck);
 const mouthMat=new THREE.MeshStandardMaterial({color:0x65222a,roughness:.82});
 const mouth=ball(.16*height,0,.05*height,.26*height,mouthMat,neck);
 mouth.scale.set(1.26,.5,.30);
 for(let k=-3;k<=3;k++){
  const tooth=new THREE.Mesh(new THREE.ConeGeometry(.026*height,.063*height,5),eyeWhite);
  tooth.position.set(k*.038*height,.07*height,.312*height);
  tooth.rotation.z=Math.PI;neck.add(tooth);
 }
 if(height>2){
  const furGeo=new THREE.ConeGeometry(.014*height,.075*height,4);
  const fur=new THREE.InstancedMesh(furGeo,bodyMat,180);
  const obj=new THREE.Object3D();const up=vec(0,1,0);
  for(let i=0;i<180;i++){
   const phi=Math.acos(1-2*(i+.5)/180),theta=i*2.399963;
   const normal=vec(Math.sin(phi)*Math.cos(theta),Math.cos(phi),Math.sin(phi)*Math.sin(theta));
   obj.position.copy(normal).multiplyScalar(.278*height).add(vec(0,.18*height,0));
   obj.quaternion.setFromUnitVectors(up,normal);obj.scale.setScalar(.65+(.35*(i%7)/6));obj.updateMatrix();fur.setMatrixAt(i,obj.matrix);
  }
  fur.castShadow=true;neck.add(fur);
 }
 for(const x of [-.12,.12]){
  ball(.095*height,x,.2*height,.249*height,eyeWhite,neck);
  ball(.044*height,x,.19*height,.329*height,iris,neck);
 }
 const arms:THREE.Group[]=[],legs:THREE.Group[]=[];
 for(const sign of [-1,1]){
  const a=new THREE.Group();a.position.set(sign*.32*height,.74*height,0);
  pelvis.add(a);beam(vec(0,0,0),vec(sign*.12*height,-.46*height,0),.08*height,bodyMat,a);
  ball(.095*height,sign*.12*height,-.45*height,0,bodyMat,a);arms.push(a);
  const l=new THREE.Group();l.position.set(sign*.17*height,.33*height,0);
  pelvis.add(l);beam(vec(0,0,0),vec(0,-.34*height,.025*height),.1*height,bodyMat,l);
  box(.17*height,.07*height,.24*height,0,-.33*height,.08*height,bodyMat,l);
  legs.push(l);
 }
 return {rig,head:neck,arms,legs,torso};
}
const creature=makeToy(3.8,blue);root.add(creature.rig);
const toylines:ReturnType<typeof makeToy>[]=[];
for(let i=0;i<8;i++){
 const toy=makeToy(.85+(i%3)*.15,i%2?yellow:blue);
 toy.rig.position.set(i%2?3.1:-3.1,1.24,-9-Math.floor(i/2)*2.3);
 root.add(toy.rig);toylines.push(toy);
}

// Emergency control and tracked GrabPack-inspired hands/cable.
const switchUnit=new THREE.Group();switchUnit.position.set(-4.45,1.7,-7);root.add(switchUnit);
box(.55,.75,.2,0,0,0,copper,switchUnit);
box(.32,.37,.1,0,0,.15,dangerMat,switchUnit);
const spark=new THREE.PointLight(0x9bdfff,0,5);switchUnit.add(spark);spark.position.set(0,0,.3);
const sparkBuffer=new Float32Array(80*3);
const sparkGeometry=new THREE.BufferGeometry();
sparkGeometry.setAttribute('position',new THREE.BufferAttribute(sparkBuffer,3));
const sparkFX=new THREE.Points(sparkGeometry,new THREE.PointsMaterial({color:0xb4f7ff,size:.077,opacity:.92,transparent:true,depthWrite:false}));
sparkFX.visible=false;root.add(sparkFX);
const hand=new THREE.Group();root.add(hand);
const palm=box(.34,.2,.32,0,0,0,blue,hand);
for(let i=0;i<4;i++)box(.066,.12,.24,(i-1.5)*.09,.015,-.23,blue,hand);
const grabLine=new THREE.Line(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0xf4b846,linewidth:2}));root.add(grabLine);

// Physically modeled cassette/CRT assembly, not a flat image slideshow.
const crt=new THREE.Group();crt.position.set(1.4,1.35,-14);root.add(crt);
box(1.3,1.15,.75,0,0,0,dark,crt);
box(1.05,.82,.06,0,.09,.42,screenMat,crt);
box(.18,.18,.07,.48,-.39,.45,copper,crt);
const tape=box(.7,.13,.42,-.5,-.44,.68,metal,crt);
const reels:THREE.Mesh[]=[];
for(const x of [-.2,.2]){
 const reel=new THREE.Mesh(new THREE.CylinderGeometry(.13,.13,.055,24),dark);
 reel.position.set(x,-.35,.7);reel.rotation.x=Math.PI/2;crt.add(reel);reels.push(reel);
}
const crtLight=new THREE.PointLight(0x22baa3,3,5);crtLight.position.set(1.4,1.8,-13.5);scene.add(crtLight);
const crtCanvas=document.createElement('canvas');crtCanvas.width=512;crtCanvas.height=256;
const crtContext=crtCanvas.getContext('2d')!;
const crtTexture=new THREE.CanvasTexture(crtCanvas);crtTexture.colorSpace=THREE.SRGBColorSpace;
screenMat.color.set(0xffffff);screenMat.map=crtTexture;screenMat.emissiveMap=crtTexture;screenMat.needsUpdate=true;
function drawCrt(globalFrame:number,warning:boolean){
 crtContext.fillStyle='#041718';crtContext.fillRect(0,0,512,256);
 crtContext.fillStyle='#2bdcbb';crtContext.font='bold 26px monospace';
 if(warning){
  crtContext.fillText('FACTORY SAFETY',36,73);
  crtContext.fillText('DO NOT FOLLOW',36,124);
  crtContext.fillText('THE FOOTSTEPS',36,160);
 }else crtContext.fillText('NO SIGNAL',36,126);
 crtContext.fillStyle='rgba(2,5,7,0.27)';
 for(let y=(globalFrame%5);y<256;y+=5)crtContext.fillRect(0,y,512,2);
 if(warning){
  const g=(globalFrame*53)%241;
  crtContext.fillStyle='rgba(193,255,248,0.13)';
  crtContext.fillRect(0,g,512,2);
 }
 crtTexture.needsUpdate=true;
}

const doorGroup=new THREE.Group();doorGroup.position.set(0,2,-32);root.add(doorGroup);
box(5.4,5,.65,0,0,-.08,dark,doorGroup);
const slidingDoor=box(3.35,4.4,.28,0,0,.26,metal,doorGroup);
for(const x of [-1.7,1.7])box(.08,4.5,.34,x,0,.24,copper,doorGroup);
box(.5,.65,.17,2.05,-.2,.4,dark,doorGroup);
const lockLight=new THREE.PointLight(0xff3a16,0,5);
lockLight.position.set(2,1.5,-31);scene.add(lockLight);
const securityLamp=ball(.1,2.05,1.5,.5,dangerMat,doorGroup);
const safePanels:THREE.Mesh[]=[];
for(const x of [-2.7,2.7]){
 const m=box(.3,4.7,8,x,2.35,-38.6,concrete);safePanels.push(m);
}
const safetyLight=new THREE.PointLight(0xf1c57b,0,9);safetyLight.position.set(0,4,-38);scene.add(safetyLight);

// Dust points (true 3D positional parallax).
const pointPositions=new Float32Array(1800);
for(let i=0;i<600;i++){
 const k=(i*241+53)%997/997, j=(i*137+11)%983/983;
 pointPositions[i*3]=k*10-5;
 pointPositions[i*3+1]=(i*43%601)/601*7;
 pointPositions[i*3+2]=(j-.5)*83-16;
}
const dustGeometry=new THREE.BufferGeometry();dustGeometry.setAttribute('position',new THREE.BufferAttribute(pointPositions,3));
const dust=new THREE.Points(dustGeometry,new THREE.PointsMaterial({color:0xc0d4d4,size:.022,transparent:true,opacity:.32,sizeAttenuation:true,depthWrite:false}));scene.add(dust);

let importedModels:THREE.Object3D[]=[];
let externalMixer:THREE.AnimationMixer[]=[];
let riggingReport:{skinnedMeshes:number;clips:string[];selectedClip:string}|null=null;
async function loadReleaseRig(url:string,position:THREE.Vector3,desiredClip='Running'){
 const gltf=await new GLTFLoader().loadAsync(url);
 let skinned=0;
 gltf.scene.traverse(o=>{if((o as THREE.SkinnedMesh).isSkinnedMesh)skinned++;});
 if(skinned===0||gltf.animations.length===0)throw new Error('ANIMATED GLB must contain SkinnedMesh and skeletal clips: '+url);
 const clip=gltf.animations.find(x=>x.name.toLowerCase()===desiredClip.toLowerCase())||gltf.animations[0];
 gltf.scene.name=url.split('/').pop()||'animated-actor';
 riggingReport={skinnedMeshes:skinned,clips:gltf.animations.map(x=>x.name),selectedClip:clip.name};
 gltf.scene.position.copy(position);root.add(gltf.scene);importedModels.push(gltf.scene);
 const mixer=new THREE.AnimationMixer(gltf.scene);
 mixer.clipAction(clip).play();
 externalMixer.push(mixer);
 return gltf.scene;
}

const planned=await fetch('/scene_manifest.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error('Manifest missing. Run npm run sync.');return r.json() as Promise<Plan>});
if(planned.frame_count!==5400||planned.shots.length!==11)throw new Error('Unvalidated manifest');
if(threadjawProof){
 // Fresh ORIGINAL Blender-authored 3D furry toy stalker, with genuinely weighted
 // armature, face geometry, distinct animation clips and verified source manifest.
 const monster=await loadReleaseRig('/assets/original_threadjaw_stalker.glb',vec(0,0,-27),'Running');
 creature.rig.visible=false;
 monster.name='Threadjaw — original fan-film character';
} else if(rigProof){
 // Independently LICENSED CC0 engineering actor to test true skinning/AnimationMixer.
 // It is deliberately NOT a Poppy character and can NEVER satisfy the final-character gate.
 const model=await loadReleaseRig('/assets/cc0_robot_expressive.glb',vec(0,0,-27),'Running');
 model.scale.setScalar(1.15);
 creature.rig.visible=false;
} else if(!technicalMode){
 await loadReleaseRig('/assets/creature.glb',vec(0,0,-27),'Running');
 await loadReleaseRig('/assets/hero.glb',vec(1,0,-22),'Idle');
 await loadReleaseRig('/assets/doll.glb',vec(-1,0,-38),'Idle');
 creature.rig.visible=false;
 for(const toy of toylines)toy.rig.visible=false;
}
// Cinematography defined in shared world-space: position/tangent/target vary per shot.
const stages=[
 {from:[2.5,1.8,14],to:[1.2,1.65,5],look:[0,2,-13],fov:64},
 {from:[-1.2,1.7,-3.5],to:[-3.15,1.72,-6.4],look:[-4.45,1.7,-7],fov:47},
 {from:[.6,1.85,-7.0],to:[0,1.75,-11.1],look:[1.8,1.8,-13],fov:58},
 {from:[1.5,1.8,-11.8],to:[1.45,1.65,-12.8],look:[1.4,1.55,-14],fov:38},
 {from:[0,1.9,-16],to:[0,1.85,-21],look:[0,2.3,-30],fov:54},
 {from:[-.9,1.36,-19.5],to:[.6,1.55,-12.5],look:[0,2.2,-26],fov:54},
 {from:[1.25,1.88,-23.4],to:[-.9,1.75,-26],look:[0,2,-32],fov:59},
 {from:[-1.25,1.82,-24.6],to:[1.8,1.92,-23.9],look:[0,2,-32],fov:63},
 {from:[0,1.65,-34.6],to:[0,1.72,-39],look:[0,2,-41],fov:61},
 {from:[.6,1.72,-37.8],to:[-.25,1.81,-34.4],look:[0,2,-32],fov:63},
 {from:[0,1.7,-33],to:[0,1.7,-32.8],look:[0,2,-34],fov:50}
] as const;
const slate=document.getElementById('slate')!;
const state=document.getElementById('state')!;
if(new URLSearchParams(location.search).get('capture')==='1')state.style.display='none';
function localStage(f:number){
 const s=planned.shots.find(x=>f>=x.start_frame&&f<x.end_frame_exclusive);
 if(!s)throw new Error('Frame outside manifest: '+f);
 return {shot:s,index:planned.shots.indexOf(s),u:(f-s.start_frame)/s.frame_count};
}
function setCamera(index:number,u:number,seconds:number){
 const s=stages[index],v=smooth(u);
 camera.position.lerpVectors(new THREE.Vector3(...s.from),new THREE.Vector3(...s.to),v);
 if(index===5||index===9){
  camera.position.x+=Math.sin(seconds*13)*.045;
  camera.position.y+=Math.sin(seconds*17)*.033;
 }
 camera.fov=s.fov;camera.updateProjectionMatrix();
 camera.lookAt(new THREE.Vector3(...s.look));
}
function renderFrame(frame:number){
 if(!Number.isInteger(frame)||frame<0||frame>=5400)throw new Error('Frame must be integer [0,5399]');
 const t=frame/60,{shot,index,u}=localStage(frame);
 setCamera(index,u,t);
 dust.rotation.y=Math.sin(t*.06)*.015;
 for(let i=0;i<boxes.length;i++){
  const z=8-((t*.7+i*3.15)%34);
  boxes[i].position.set(.22*Math.sin(i*17),1.25,z);
  boxes[i].rotation.y=.1*Math.sin(t*.5+i);
 }
 const flick=t<5 || (index>=4&&index<=6);
 for(let i=0;i<overhead.length;i++)overhead[i].intensity=flick?(i%2===0?32:46)*(Math.sin(t*28+i*2)>-.85?1:.12):47;
 for(let i=0;i<toylines.length;i++){
  const toy=toylines[i],turn=smooth((t-(12+i*.52))/1.3);
  toy.head.rotation.y=turn*(i%2?-.46:.68);
  toy.head.rotation.x=turn*-.14;
 }
 const contact=smooth((t-6.0)/1.5)*(1-smooth((t-10)/1.0));
 hand.visible=index===1||index===6;
 hand.position.lerpVectors(vec(-1.35,1.05,-5.1),vec(-4.45,1.7,-6.57),index===1?contact:1-smooth((t-47)/4));
 const contactPoint=hand.position.clone(),anchor=vec(-1.3,1.15,-4.7);
 const vertices=[anchor,anchor.clone().lerp(contactPoint,.3).add(vec(0,-.18,0)),anchor.clone().lerp(contactPoint,.65).add(vec(0,-.24,0)),contactPoint];
 grabLine.geometry.dispose();
 grabLine.geometry=new THREE.BufferGeometry().setFromPoints(vertices);
 grabLine.visible=hand.visible;
 spark.intensity=index===1 && u>.4 && u<.74?8*(.6+.4*Math.sin(t*87)):0;
 const sparking=index===1&&u>.4&&u<.74;
 sparkFX.visible=sparking;
 if(sparking){
  for(let i=0;i<80;i++){
   const a=i*2.399963+frame*.092;
   const r=.04+((i*97+frame*13)%100)/100*.65;
   sparkBuffer[i*3]=-4.45+Math.cos(a)*r;
   sparkBuffer[i*3+1]=1.7+Math.sin(a)*r*.55;
   sparkBuffer[i*3+2]=-6.7+Math.sin(a*1.21)*r*.6;
  }
  (sparkGeometry.attributes.position as THREE.BufferAttribute).needsUpdate=true;
 }
 const attack=index===5?smooth(u):index===9?smooth(u):0;
 creature.rig.position.set(.2*Math.sin(t*1.2),0,index===5?-28+attack*9:index===9?-41+attack*6:-28);
 const gait=(index===5||index===9)?Math.sin(t*12):Math.sin(t*1.5)*.12;
 creature.head.rotation.z=Math.sin(t*1.7)*.06;
 creature.arms[0].rotation.x=gait*.65;
 creature.arms[1].rotation.x=-gait*.65;
 creature.legs[0].rotation.x=-gait*.48;
 creature.legs[1].rotation.x=gait*.48;
 creature.rig.rotation.y=index===9?Math.PI:0;
 if(importedModels[0]){importedModels[0].position.copy(creature.rig.position);importedModels[0].rotation.y=creature.rig.rotation.y;importedModels[0].visible=index===4||index===5||index===9;}
 if(index===5)camera.lookAt(creature.rig.position.clone().add(vec(0,2.05,0)));
 if(index===9 && u>.52){
  // Late over-the-shoulder reveal: camera physically turns to face the
  // pursuer rather than staring at the closed security door.
  camera.lookAt(creature.rig.position.clone().add(vec(0,2.1,0)));
 }
 doorGroup.visible=true;
 slidingDoor.position.x=index>=8?3.0*smooth((t-65)/1.5):0;
 lockLight.intensity=index===6?(3+5*(Math.sin(t*14)>.5?1:0)):index===7?2:0;
 securityLamp.material=dangerMat;
 for(let i=0;i<safePanels.length;i++)safePanels[i].position.x=(i===0?-2.7:2.7)*(1-smooth((t-69)/6)*.65);
 safetyLight.intensity=index===8?7*(1-smooth((t-69)/5)):0;
 for(const r of reels)r.rotation.z=t*3.3;
 crtLight.intensity=index===3?7:1;
 screenMat.emissiveIntensity=index===3?1.7*(.92+.08*Math.sin(t*47)):.25;
 if(index===3 || frame===0)drawCrt(frame,index===3);
 for(const mixer of externalMixer)mixer.setTime(t);
 slate.style.opacity=index===10?String(smooth(u*5)*(1-smooth((u-.83)*5))):'0';
 // End slate is deliberate black to preserve a separate 5-second fan disclaimer.
 if(index===10){scene.background=new THREE.Color(0x000000);root.visible=false;dust.visible=false;}
 else {scene.background=new THREE.Color(0x0b1015);root.visible=true;dust.visible=true;}
 state.textContent=threadjawProof?'ORIGINAL THREADJAW SKELETAL MODEL — ART QUALITY UNDER REVIEW':rigProof?'CC0 SKINNED ACTOR DIAGNOSTIC — NOT THE FINAL FILM':technicalMode?'ORIGINAL 3D ENGINEERING STAND-IN — '+shot.id:'RELEASE RIGS — '+shot.id;
 renderer.render(scene,camera);
}
window.renderFrame=renderFrame;
window.productionReady=true;
window.engineStatus={mode:threadjawProof?'threadjaw-original':rigProof?'rigproof-cc0':technicalMode?'technical-standin':'final-with-authorized-rigs',renderer:renderer.capabilities.isWebGL2?'WebGL2':'WebGL',frames:planned.frame_count,models:importedModels.map(x=>x.name),rigging:riggingReport} as typeof window.engineStatus;
renderFrame(0);
