#!/usr/bin/env python3
"""Build an ORIGINAL rigged plush-factory monster: Threadjaw (NON-CANON).
For: blender -b --factory-startup --python scripts/blender_make_threadjaw.py
No game extraction, imported copyrighted geometry, purchased meshes, or AI faux 3D.
Arms, legs, head and jaw are actual weighted skinned meshes animated by an
armature and three NLA clips. Visually inspect before declaring film quality.
"""
import bpy
import math
import os
import random
from mathutils import Vector
from math import sin,cos,pi

random.seed(260118)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in bpy.data.materials: bpy.data.materials.remove(block)

def mat(name,color,rough=.8,metal=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(*color,1)
    bsdf.inputs["Roughness"].default_value=rough
    bsdf.inputs["Metallic"].default_value=metal
    return m

fur_blue=mat("THREADJAW__deep_cobalt_plush_fabric",(.025,.18,.40),.94)
fur_light=mat("THREADJAW__highlight_worn_blue",(.07,.29,.56),.87)
fabric_dark=mat("THREADJAW__seam_indigo",(.018,.035,.07),.95)
lip=mat("THREADJAW__worn_crimson_felt",(.31,.012,.055),.84)
mouth=mat("THREADJAW__mouth_shadow",(.006,.003,.009),.92)
tooth=mat("THREADJAW__ivory_aged_plastic",(.68,.59,.44),.37)
eyes=mat("THREADJAW__bone_buttons",(.83,.78,.62),.25)
pupils=mat("THREADJAW__glossy_black",(.004,.008,.015),.15)
stitch=mat("THREADJAW__repair_stitches",(.16,.10,.085),.99)

# Armature: Blender Z-up, film engine glTF transforms to Y-up.
bpy.ops.object.armature_add(enter_editmode=True,location=(0,0,0))
rig=bpy.context.object
rig.name="Threadjaw_Original_Skinned_Armature"
arm=rig.data
arm.name="Threadjaw_Rig_Data"
arm.edit_bones.remove(arm.edit_bones[0])
segments={
 "body":((0,0,1.58),(0,0,3.06),None),
 "neck":((0,0,3.03),(0,0,3.40),"body"),
 "head":((0,0,3.40),(0,0,3.86),"neck"),
 "jaw":((0,-.27,3.37),(0,-.34,3.05),"head"),
 "arm_L":((-.57,0,2.88),(-.81,0,2.10),"body"),
 "forearm_L":((-.81,0,2.10),(-.97,0,1.29),"arm_L"),
 "palm_L":((-.97,0,1.29),(-1.05,-.06,1.08),"forearm_L"),
 "arm_R":((.57,0,2.88),(.81,0,2.10),"body"),
 "forearm_R":((.81,0,2.10),(.97,0,1.29),"arm_R"),
 "palm_R":((.97,0,1.29),(1.05,-.06,1.08),"forearm_R"),
 "thigh_L":((-.32,0,1.72),(-.37,0,.87),"body"),
 "shin_L":((-.37,0,.87),(-.38,-.055,.24),"thigh_L"),
 "foot_L":((-.38,-.055,.24),(-.38,-.27,.10),"shin_L"),
 "thigh_R":((.32,0,1.72),(.37,0,.87),"body"),
 "shin_R":((.37,0,.87),(.38,-.055,.24),"thigh_R"),
 "foot_R":((.38,-.055,.24),(.38,-.27,.10),"shin_R")
}
for name,(h,t,parent) in segments.items():
    bone=arm.edit_bones.new(name);bone.head=h;bone.tail=t
for name,(h,t,parent) in segments.items():
    if parent:arm.edit_bones[name].parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode="OBJECT")

created=[]
def skin(obj,bone_name):
    group=obj.vertex_groups.new(name=bone_name)
    group.add(list(range(len(obj.data.vertices))),1.0,"REPLACE")
    mod=obj.modifiers.new("OriginalSkinnedArmature","ARMATURE")
    mod.object=rig
    obj.parent=rig
    created.append(obj)
    return obj

def ellipsoid(name,center,radii,material,bone,segments=20,rings=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=center)
    ob=bpy.context.object;ob.name=name
    ob.scale=radii
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(material)
    for poly in ob.data.polygons:poly.use_smooth=True
    return skin(ob,bone)

def tube(name,point_a,point_b,radius_a,radius_b,material,bone,steps=14):
    a=Vector(point_a);b=Vector(point_b)
    axis=(b-a).normalized()
    side=axis.cross(Vector((0,1,0))).normalized()
    if side.length<.02:side=axis.cross(Vector((0,0,1))).normalized()
    other=axis.cross(side).normalized()
    vs=[];faces=[]
    for j,(p,r) in enumerate(((a,radius_a),(b,radius_b))):
        for i in range(steps):
            v=p+r*(cos(2*pi*i/steps)*side+sin(2*pi*i/steps)*other)
            vs.append(tuple(v))
    for i in range(steps):
        k=(i+1)%steps
        faces.append((i,k,steps+k,steps+i))
    faces.extend([tuple(reversed(range(steps))),tuple(range(steps,steps*2))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    mesh.materials.append(material)
    for p in mesh.polygons:p.use_smooth=True
    return skin(obj,bone)

# Masses/volume anatomically coherent, long arms with plush limb joints.
ellipsoid("FullVolumeChest",(0,0,2.33),(.425,.305,.76),fur_blue,"body",32,22)
ellipsoid("NeckCuff",(0,0,3.03),(.27,.27,.26),fur_light,"neck")
ellipsoid("StitchedHead",(0,-.035,3.48),(.46,.405,.49),fur_blue,"head",32,20)
ellipsoid("SoftMuzzle",(0,-.32,3.28),(.365,.13,.19),fur_light,"head",26,14)
ellipsoid("GapingMouth",(0,-.448,3.245),(.285,.055,.157),mouth,"jaw",24,14)
ellipsoid("CrimsonFeltMouthTrim",(0,-.454,3.255),(.325,.042,.201),lip,"jaw",24,14)
ellipsoid("MouthBlackCenter",(0,-.509,3.252),(.274,.02,.155),mouth,"jaw",24,14)

for side in (-1,1):
    s="L" if side<0 else "R"
    ellipsoid("Shoulder_"+s,(side*.62,0,2.74),(.215,.22,.29),fur_light,"arm_"+s)
    tube("UpperArm_"+s,(side*.62,0,2.75),(side*.82,0,2.07),.216,.172,fur_blue,"arm_"+s)
    ellipsoid("ElbowSocket_"+s,(side*.81,0,2.10),(.185,.19,.20),fur_light,"arm_"+s)
    tube("LowerArm_"+s,(side*.81,0,2.08),(side*.97,-.015,1.29),.16,.195,fur_blue,"forearm_"+s)
    ellipsoid("HugeCushionedHand_"+s,(side*1.0,-.04,1.17),(.224,.19,.23),fur_light,"palm_"+s)
    for k in range(3):
        tube("Finger_%s_%i"%(s,k),(side*(.88+.11*k),-.135,1.085),
             (side*(.90+.11*k),-.31,1.00),.056,.028,fur_blue,"palm_"+s,8)
    ellipsoid("Hip_"+s,(side*.29,0,1.63),(.222,.228,.29),fur_blue,"thigh_"+s)
    tube("LegUpper_"+s,(side*.29,0,1.55),(side*.37,0,.86),.24,.185,fur_blue,"thigh_"+s)
    ellipsoid("Knee_"+s,(side*.36,0,.87),(.19,.19,.21),fur_light,"thigh_"+s)
    tube("LegLower_"+s,(side*.37,0,.84),(side*.38,0,.19),.175,.17,fur_blue,"shin_"+s)
    ellipsoid("HeavyFoot_"+s,(side*.38,-.15,.15),(.245,.38,.146),fur_light,"foot_"+s)

# Proprietary-free expressive face: eye socket + irregular bone buttons,
# black inset glossy pupils, visibly shaped grin and sculptural teeth.
for side in [-1,1]:
    ellipsoid("DarkEyeSocket_%s"%side,(side*.218,-.359,3.58),(.182,.08,.192),fabric_dark,"head",26,16)
    ellipsoid("AgedEyeButton_%s"%side,(side*.217,-.43,3.585),(.145,.079,.16),eyes,"head",26,16)
    ellipsoid("Pupil_%s"%side,(side*.221,-.493,3.573),(.071,.027,.079),pupils,"head",24,14)
    ellipsoid("EyeCatchlight_%s"%side,(side*.191,-.518,3.61),(.022,.011,.023),eyes,"head",12,8)
for i in range(9):
    x=(i-4)*.057
    for upper in (True,False):
        z=3.338 if upper else 3.157
        point=(x,-.535,z)
        end=(x+random.uniform(-.01,.01),-.535,z+(-.071 if upper else .069))
        tube("PointedTooth_%d_%s"%(i,"top" if upper else "bottom"),
             point,end,.027,.002,tooth,"jaw",8)
for side in (-1,1):
    # Fur-covered ears/tassels, original shape and silhouette.
    ellipsoid("TasselEar_%d"%side,(side*.414,0,3.835),(.145,.18,.27),fur_blue,"head",18,12)

# Fur tufts: real low-profile triangular geometry, not flat billboard PNGs.
# One batched skinned mesh per bone, no thousands of draw calls.
def tufts(name,center,radii,bone,count,spread=.05):
    vs=[];fs=[]
    for k in range(count):
        z=random.uniform(-1,1)
        az=random.random()*2*pi
        r=math.sqrt(max(0,1-z*z))
        normal=Vector((r*cos(az),r*sin(az),z))
        p=Vector(center)+Vector((normal.x*radii[0],normal.y*radii[1],normal.z*radii[2]))
        n=Vector((normal.x/max(.001,radii[0]),normal.y/max(.001,radii[1]),normal.z/max(.001,radii[2]))).normalized()
        side=n.cross(Vector((0,1,0)))
        if side.length<.02: side=n.cross(Vector((0,0,1)))
        side.normalize()
        up=n.cross(side).normalized()
        length=random.uniform(.025,.074)
        width=random.uniform(.007,.023)
        base=len(vs)
        for point in [p+side*width,p-side*width,p+up*width,p+n*length+up*spread*.15]:
            vs.append(tuple(point))
        fs.extend([(base,base+1,base+3),(base+1,base+2,base+3),(base+2,base,base+3)])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update()
    ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob)
    mesh.materials.append(fur_blue)
    skin(ob,bone)
tufts("TorsoFabricFibers",(0,0,2.33),(.424,.302,.758),"body",1350)
tufts("HeadFabricFibers",(0,-.035,3.48),(.461,.405,.492),"head",750)
for side in (-1,1):
    s="L" if side<0 else "R"
    tufts("ShoulderFiber_"+s,(side*.62,0,2.74),(.213,.218,.286),"arm_"+s,150)
    tufts("ElbowFiber_"+s,(side*.81,0,2.10),(.185,.19,.20),"arm_"+s,100)
    tufts("HandFiber_"+s,(side*1.0,-.04,1.17),(.224,.19,.23),"palm_"+s,140)
    tufts("HipFiber_"+s,(side*.29,0,1.63),(.22,.225,.288),"thigh_"+s,140)
    tufts("KneeFiber_"+s,(side*.36,0,.87),(.19,.19,.21),"thigh_"+s,90)

# Finishing model-only skin/weight checks before animation.
assert all(any(m.type=="ARMATURE" and m.object==rig for m in ob.modifiers) for ob in created)
assert sum(len(ob.data.polygons) for ob in created)>10000

# NLA clips with deterministic frame positions; 24fps authoring,
# renderer re-samples the baked 3D motion at 60fps.
scene=bpy.context.scene
scene.render.fps=24
for p in rig.pose.bones:p.rotation_mode="XYZ"

def clip(name,duration,drive):
    action=bpy.data.actions.new(name)
    action.use_fake_user=True
    rig.animation_data_create()
    rig.animation_data.action=action
    for frame in range(1,duration+1,4):
        q=(frame-1)/float(duration)
        for bone in rig.pose.bones:
            rot=drive(bone.name,q)
            bone.rotation_euler=rot
            bone.keyframe_insert(data_path="rotation_euler",frame=frame,group=bone.name)
    for bone in rig.pose.bones:
        bone.rotation_euler=drive(bone.name,1.0)
        bone.keyframe_insert(data_path="rotation_euler",frame=duration+1,group=bone.name)
    rig.animation_data.action=None
    track=rig.animation_data.nla_tracks.new()
    track.name=name
    track.strips.new(name,1,action)
    return action

def wave(q):return sin(2*pi*q)
def run(n,q):
    v=wave(2*q)
    sign=(-1 if n.endswith("_L") else 1)
    if n.startswith("arm_"):return (.68*sign*v,0,.09*sign)
    if n.startswith("forearm_"):return (-.22+.24*sign*v,0,.08*sign)
    if n.startswith("thigh_"):return (-.55*sign*v,0,0)
    if n.startswith("shin_"):return (.30+max(0,.52*sign*v),0,0)
    if n=="head":return (.045+.05*sin(4*pi*q),0,.045*sin(2*pi*q))
    if n=="body":return (.06*sin(4*pi*q),.018*sin(2*pi*q),.03*sin(2*pi*q))
    if n=="jaw":return (-.11-.07*abs(v),0,0)
    return (0,0,0)

def idle(n,q):
    if n=="body":return (.018*sin(2*pi*q),0,.028*sin(2*pi*q))
    if n=="head":return (.04*sin(2*pi*q+.9),.05*sin(2*pi*q),.025*sin(2*pi*q))
    if n=="jaw":return (-.045-.035*sin(2*pi*q),0,0)
    if n.startswith("arm_"):return (.015*sin(2*pi*q),0,0)
    return (0,0,0)

def lunge(n,q):
    u=(1-cos(pi*min(1,q)))*.5
    if n=="body":return (-.39*u,0,0)
    if n=="head":return (-.27*u,0,0)
    if n.startswith("arm_"):return (-1.1*u,0,0)
    if n.startswith("forearm_"):return (-.35*u,0,0)
    if n=="jaw":return (-.26*u,0,0)
    return (0,0,0)

clip("Running",32,run)
clip("Idle",48,idle)
clip("Lunge",24,lunge)
scene.frame_set(1)

# Validate nonzero 3D skeletal geometry and export standalone GLB.
output=os.environ.get("THREADJAW_GLB","public/assets/original_threadjaw_stalker.glb")
os.makedirs(os.path.dirname(output),exist_ok=True)
bpy.ops.object.select_all(action="DESELECT")
rig.select_set(True)
for ob in created:ob.select_set(True)
bpy.context.view_layer.objects.active=rig
kwargs=dict(filepath=output,export_format="GLB",use_selection=True,
            export_animations=True,export_nla_strips=True,
            export_skins=True,export_materials="EXPORT",
            export_apply=False)
try:
    bpy.ops.export_scene.gltf(**kwargs)
except TypeError:
    # Exporter API variants: retry only a documented optional argument.
    kwargs.pop("export_apply",None)
    bpy.ops.export_scene.gltf(**kwargs)
import json,hashlib
blend_path=os.path.join("output","Threadjaw_Original_Editable_Model.blend")
os.makedirs("output",exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(blend_path))
meta={
 "generator":"scripts/blender_make_threadjaw.py",
 "model":"Threadjaw (original toy-factory stalker, NOT official Poppy Playtime game asset)",
 "mesh_groups":len(created),
 "polygons":sum(len(ob.data.polygons) for ob in created),
 "armature_bones":len(arm.bones),
 "nla_names":[t.name for t in rig.animation_data.nla_tracks],
 "glb_bytes":os.stat(output).st_size,
 "glb_sha256":hashlib.sha256(open(output,"rb").read()).hexdigest(),
 "editable_blend":blend_path,
 "license":"Original project-authored non-canon character; no extracted game content",
 "not_final":"Rendering and artistic approval pending"
}
with open("output/threadjaw_asset_manifest.json","w") as manifest:
 json.dump(meta,manifest,indent=2)
print("ORIGINAL_THREADJAW_GENERATED",json.dumps(meta))
