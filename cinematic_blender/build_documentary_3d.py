#!/usr/bin/env python3
"""Blender 3D cinematic scene director for a factual property documentary.

Creates actual keyframed architecture, land parcels, and dossiers in Blender.
Imports a licensed CC0 residential facade where available. The visuals are
clearly conceptual reconstructions, never represented as actual case imagery.
Uses physically based materials, Cycles raytracing, ambient occlusion, cinematic
camera/lens DOF and animated lighting. Produces editable .blend scenes and MP4s.
"""
import bpy, math, os, sys, json, random
from mathutils import Vector
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"cinematic_output"
OUT.mkdir(parents=True,exist_ok=True)
ARGS=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
QUALITY="final" if "--final" in ARGS else "preview"
PREVIEW=(1280,720,20,13)
FINAL=(1920,1080,24,24)
WIDTH,HEIGHT,FPS,SAMPLES=(FINAL if QUALITY=="final" else PREVIEW)
FRAMECOUNT=FPS*5
random.seed(20261017)

def mat(name,color,metal=0,rough=.4,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get("Principled BSDF")
 p.inputs["Base Color"].default_value=(*color,1)
 p.inputs["Metallic"].default_value=metal
 p.inputs["Roughness"].default_value=rough
 if emission:
  p.inputs["Emission Color"].default_value=(*color,1)
  p.inputs["Emission Strength"].default_value=emission
 return m

DARK=mat("Obsidian coated material",(.019,.029,.041),.42,.24)
FLOOR=mat("Mineral asphalt PBR",(.047,.059,.071),.17,.76)
CONCRETE=mat("Warm architectural cement",(.33,.34,.35),.02,.69)
WHITE=mat("Ceramic archival cards",(.78,.79,.76),0,.75)
GLASS=mat("Architectural blue glass",(.07,.15,.20),.68,.15)
GOLD=mat("Bronze documentary accent",(.72,.41,.14),.7,.23)
TEAL=mat("Approved lots glass",(.015,.46,.49),.38,.23,emission=.4)
ORANGE=mat("Disputed records orange",(.80,.19,.065),.40,.32,emission=.3)
INK=mat("Midnight black ink",(.015,.027,.04),0,.87)
ROAD=mat("Road matte texture",(.13,.15,.16),.07,.92)
LIGHT=mat("Windows warm light",(.92,.69,.33),.15,.22,emission=.3)

def box(name,loc,scale,material,bevel=.06):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 obj=bpy.context.object;obj.name=name
 obj.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 obj.data.materials.append(material)
 if bevel:
  mod=obj.modifiers.new("Micro bevels, realistic edge highlight","BEVEL")
  mod.width=bevel;mod.segments=2
  mod=obj.modifiers.new("Weighted hard-surface normals","WEIGHTED_NORMAL")
 return obj

def add_light(name,loc,power,color,size):
 data=bpy.data.lights.new(name,"AREA");data.energy=power;data.color=color;data.shape="DISK";data.size=size
 ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);ob.location=loc
 return ob

def look_at(obj,xyz):
 direction=Vector(xyz)-obj.location
 obj.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()

def cam(name,path,target,lens=44,fstop=4):
 d=bpy.data.cameras.new(name);c=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(c)
 scene=bpy.context.scene;scene.camera=c;d.lens=lens;d.dof.use_dof=True;d.dof.aperture_fstop=fstop
 focal=bpy.data.objects.new("Camera autofocus target",None);bpy.context.collection.objects.link(focal);focal.location=target
 d.dof.focus_object=focal
 for i,(p,aim) in enumerate(path):
  frame=1 if i==0 else FRAMECOUNT
  c.location=p;look_at(c,aim);c.keyframe_insert(data_path="location",frame=frame)
  c.keyframe_insert(data_path="rotation_euler",frame=frame)
 for fc in c.animation_data.action.fcurves if hasattr(c.animation_data.action,"fcurves") else []:
  for point in fc.keyframe_points:point.interpolation="BEZIER"
 return c

def ground(name,length=56,width=56):
 o=box(name,(0,0,-.48),(length,width,.8),FLOOR,.32)
 return o

def base_scene(name):
 bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene;scene.name=name
 scene.render.engine="CYCLES";scene.cycles.samples=SAMPLES
 scene.render.threads_mode="FIXED";scene.render.threads=4
 scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT
 scene.render.resolution_percentage=100
 scene.render.image_settings.color_mode="RGBA"
 scene.render.film_transparent=False
 scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=FRAMECOUNT
 scene.view_settings.view_transform="AgX"
 scene.world.use_nodes=True
 scene.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.025,.04,.063,1)
 scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.38
 add_light("Three quarter key softbox",(0,-14,23),2700,(.77,.88,1),13)
 add_light("Warm rim sunlight",(20,13,19),2900,(1,.71,.40),12)
 add_light("Low turquoise rim",(-18,8,13),850,(.19,.72,.8),8)
 scene.render.image_settings.file_format="FFMPEG"
 scene.render.ffmpeg.format="MPEG4";scene.render.ffmpeg.codec="H264"
 scene.render.ffmpeg.constant_rate_factor="HIGH"
 scene.render.ffmpeg.ffmpeg_preset="GOOD"
 scene.render.ffmpeg.audio_codec="NONE"
 scene.render.filepath=str(OUT/(name+".mp4"))
 scene.render.film_transparent=False
 scene.camera=None
 return scene

def import_architecture(assetpath):
 """Append CC0 facade objects with their material, scaled as a hero 3D cluster."""
 asset=Path(assetpath)
 if not asset.is_file():raise RuntimeError("CC0 Blender asset absent")
 imported=[]
 with bpy.data.libraries.load(str(asset),link=False) as (src,dst):
  names=[n for n in src.objects if n.lower() not in ("camera","light")]
  dst.objects=names[:220]
 for o in dst.objects:
  if o and o.type in ("MESH","CURVE"):
   bpy.context.collection.objects.link(o);imported.append(o)
 if len(imported)<2:raise RuntimeError("The sourced Blender asset had too little actual geometry")
 # Snapshot bounding data in world coordinates with original transforms.
 coords=[]
 for o in imported:
  if o.type!="MESH":continue
  try:
   coords.extend([o.matrix_world@Vector(x) for x in o.bound_box])
  except Exception:continue
 if not coords:raise RuntimeError("No imported bounding boxes")
 mini=Vector((min(p[i] for p in coords) for i in range(3)))
 maxi=Vector((max(p[i] for p in coords) for i in range(3)))
 mid=(mini+maxi)*.5
 size=max((maxi-mini).x,(maxi-mini).y,(maxi-mini).z)
 if not .001<size<10000:raise RuntimeError("Invalid imported scale")
 root=bpy.data.objects.new("Official Poly Haven CC0 architectural facade kit",None)
 bpy.context.collection.objects.link(root)
 ratio=17./size
 for o in imported:
  # Parent without altering original world position, then transform relative to root.
  original=o.matrix_world.copy()
  o.parent=root
  o.matrix_parent_inverse=root.matrix_world.inverted()
  o.matrix_world=original
 root.scale=(ratio,)*3
 root.location=(-mid.x*ratio,-mid.y*ratio,2.0-mini.z*ratio)
 return root

def map_animation():
 s=base_scene("01_cinematic_parcel_map")
 ground("Survey table charcoal stage",70,50)
 # Roads are modeled in real 3D, not rectangular infographics.
 for i in range(-3,4):
  box("Survey paved avenue horizontal",(0,i*6,-.02),(67,.5,.12),ROAD,.07)
 for j in range(-5,6):
  box("Survey street vertical",(j*6,0,-.01),(.50,47,.13),ROAD,.07)
 # 64 3D parcel extrusions. Material and vertical staging indicate conceptual supply, not factual allocation.
 for ix in range(-5,6):
  for iy in range(-3,4):
   if (ix+iy)%9==0:continue
   x,y=ix*6+2.35,iy*6+2.3
   selected=(ix+5+iy+3)%8 in (0,1)
   h=.45+random.random()*.13
   p=box("Legal land parcel physical 3D",(x,y,h*.5), (4.15,4.05,h),TEAL if selected else CONCRETE,.085)
   if selected:
    p.location.z=.01;p.keyframe_insert(data_path="location",frame=1)
    p.location.z=h*.6;p.keyframe_insert(data_path="location",frame=FRAMECOUNT//2)
 # High contrast emissive lattice delineates supply.
 for k in range(14):
  ix=(k%7)-3;iy=(k//7)-1
  o=box("Recorded file token floating over land",(ix*4,iy*5,6.2),(.9,1.4,.11),ORANGE,.07)
  o.location.z=-1;o.keyframe_insert(data_path="location",frame=1)
  o.location.z=1.3+ k*.055;o.keyframe_insert(data_path="location",frame=FRAMECOUNT)
 # volumetric set / camera drift.
 cam("Topographical dolly camera",[ ((-49,-38,41),(0,0,0)),((27,-39,33),(0,0,1)) ],(0,0,0),35,5.6)
 return s

def building_animation(asset):
 s=base_scene("02_architecture_construction")
 ground("Architectural render stage",48,47)
 root=import_architecture(asset)
 root.location.x-=1;root.location.y+=1
 # Additional realistically detailed tower portions and glowing window bands.
 for x in (-10,10):
  for y in (7,):
   base=box("PBR reinforced tower structure",(x,y,5.9),(7.5,7.5,12),CONCRETE,.2)
   for level in range(6):
    z=1+level*1.73
    for side in (-1,1):
     for i in range(4):
      box("Architectural reflective glazing",(x-2.5+i*1.67,y+side*3.86,z),(.95,.09,1.3),GLASS,.016)
  # Night time architectural light sources on actual 3D facade.
 add_light("Building reveal cinematic rim",(-10,-9,11),2900,(.40,.76,1),7)
 # 3D model rises from surveyed lot, not a screenshot/text card.
 root.location.z=-8.5;root.keyframe_insert(data_path="location",frame=1)
 root.location.z=0;root.keyframe_insert(data_path="location",frame=int(FPS*3.1))
 cam("Construction camera crane",[((-28,-39,18),(0,2,6)),((19,-35,21),(0,0,8))],(0,0,7),38,6)
 return s

def dossier_animation():
 s=base_scene("03_evidence_document_desk")
 # Museum-quality neutral desk with shallow DoF, actual mesh thickness.
 box("Oak desktop with eased bevel",(0,0,-.5),(40,28,1),DARK,.16)
 for i in range(20):
  y=3.8-i*.12;x=-5.5+i*.13
  p=box("Physical land allotment records stack", (x,y,.07+i*.055),(6.9,10.5,.072),WHITE,.026)
  p.rotation_euler.z=.008*i
  if i%4==0:
   for w in range(2):
    box("Printed record title line",(x-1.5,y-2+w*.7,.16+i*.055),(2.7,.055,.007),INK,.0)
 # Dark glass evidence folder and legal verification stamp.
 binder=box("Investigation hard-cover file",(5.5,0,.6),(8,11,.8),DARK,.18)
 for i in range(7):
  box("Separate allotment paperwork page",(4+i*.11,0+i*.06,1.05+i*.05),(6.7,8.3,.04),WHITE,.02)
 # Render genuine physical stamped words as raised metallic geometry (Latin numbers only).
 d=bpy.data.curves.new("Evidence number 42000",'FONT')
 d.body="42,000  /  6,000";d.size=.65;d.extrude=.012
 label=bpy.data.objects.new("Reported numbers physically typeset in 3D",d)
 bpy.context.collection.objects.link(label);label.location=(1.6,-2.4,1.46)
 label.data.materials.append(GOLD)
 add_light("Macro paper softbox",(3,-8,16),2700,(.90,.91,1),13)
 cam("Dossier desk dolly",[((0,-25,17),(0,0,1)),((12,-15,13),(2,0,.6))],(2,0,.3),56,3.8)
 return s

def render_scene(func,asset=None):
 s=func(asset) if asset is not None else func()
 bpy.context.window.scene=s
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(s.name+".blend")))
 bpy.ops.render.render(animation=True)
 if not (OUT/(s.name+".mp4")).exists():
  raise RuntimeError("Blender did not output the animation file")
 return s

def main():
 provenance=ROOT/"cinematic_assets"/"asset_provenance.json"
 if not provenance.is_file():raise RuntimeError("Need the licensed architecture first")
 asset=Path(json.loads(provenance.read_text())["file"])
 for f in (map_animation,lambda:building_animation(asset),dossier_animation):
  render_scene(f)
 print("3D PREVIEW COMPLETE",QUALITY,str(OUT),flush=True)

if __name__=="__main__":main()
