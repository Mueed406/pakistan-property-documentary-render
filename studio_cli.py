#!/usr/bin/env python3
"""AI-friendly cross-platform CLI for Pakistan Property Group documentary studio.

No direct billing, no YouTube uploads, no invented source footage.
Every action executes a tested underlying CLI with explicit inputs and exit codes.
Example: python studio_cli.py doctor
"""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def run(cmd,cwd=ROOT):
 print("STUDIO:",' '.join(str(x) for x in cmd),flush=True)
 subprocess.run([str(x) for x in cmd],cwd=str(cwd),check=True)

def blender_path():
 tool=shutil.which("blender")
 if tool:return tool
 if os.name=="nt":
  for pat in (r"C:\Program Files\Blender Foundation\Blender *\blender.exe",r"C:\Program Files (x86)\Blender Foundation\Blender *\blender.exe"):
   import glob
   hits=sorted(glob.glob(pat),reverse=True)
   if hits:return hits[0]
 return None

def doctor():
 tools={"python":sys.executable,"Blender":blender_path(),
 "FFmpeg":shutil.which("ffmpeg"),"FFprobe":shutil.which("ffprobe"),
 "Node":shutil.which("node"),"npm":shutil.which("npm.cmd" if os.name=="nt" else "npm")}
 required=("Blender","FFmpeg","FFprobe","Node","npm")
 checks={}
 for name,path in tools.items():
  status={"installed":bool(path),"path":path}
  if path and name in required:
   try:
    args=[path,"--version"] if name!="FFmpeg" and name!="FFprobe" else [path,"-version"]
    output=subprocess.run(args,capture_output=True,text=True,timeout=25)
    status["version"]=((output.stdout or output.stderr).splitlines() or [""])[0][:150]
    status["ok"]=output.returncode==0
   except Exception as e:status["ok"]=False;status["error"]=str(e)
  checks[name]=status
 result={"platform":sys.platform,"tools":checks,
 "internet_required_for_new_assets":True,"gemini_access":bool(os.environ.get("GEMINI_API_KEY")),
 "paid_service_used":False}
 print(json.dumps(result,indent=2,ensure_ascii=False))
 return 0 if all(checks[x].get("ok") for x in ("Blender","FFmpeg","FFprobe")) else 2

def main():
 p=argparse.ArgumentParser(description=__doc__)
 sub=p.add_subparsers(dest="action",required=True)
 sub.add_parser("doctor",help="Inspect locally installed binaries; no modifications")
 sub.add_parser("download-footage",help="Download licensed Pexels clips from the supplied manifest")
 sub.add_parser("download-architecture",help="Download official CC0 Blender architecture through Poly Haven API")
 b=sub.add_parser("render-3d",help="Render keyframed CC0 3D animation. CPU intensive")
 b.add_argument("--final",action="store_true",help="Use full-HD production profile, not rapid preview")
 sub.add_parser("gemini-plan",help="Count Urdu narration chunks; no Gemini API calls")
 v=sub.add_parser("master-voice",help="Master an ALREADY approved existing narrator file")
 v.add_argument("--input",required=True);v.add_argument("--output",required=True)
 m=sub.add_parser("motion-preview",help="Render React/Remotion animation for technical approval")
 f=sub.add_parser("render-full-browser",help="Produce true full-length HD documentary with eight distinct browser-motion scenes")
 f.add_argument("--base",required=True,help="Existing verified full-length moving-footage MP4")
 f.add_argument("--srt",required=True,help="Time-aligned real Urdu subtitle file")
 f.add_argument("--out",default="renders/Pakistan_Property_Full_Browser_Motion_Review.mp4")
 f.add_argument("--motion-dir",default="motion-output")
 pmp=sub.add_parser("render-premium-pearl",help="Composite 24 light pearl motion sequences over blurred stock footage")
 pmp.add_argument("--base",required=True)
 pmp.add_argument("--srt",required=True)
 pmp.add_argument("--out",default="renders/Pakistan_Property_Premium_Pearl_24_Motion_FullHD_Review.mp4")
 pmp.add_argument("--motion-dir",default="premium_motion")
 o=sub.add_parser("export-otio",help="Export editable timeline for external video editors")
 o.add_argument("--decisions",required=True);o.add_argument("--out",required=True)
 r=sub.add_parser("render-stock",help="Render real documentary only with approved audio and matching subtitles")
 r.add_argument("--voice",required=True);r.add_argument("--subtitles",required=True)
 r.add_argument("--music",required=True);r.add_argument("--approve-voice",action="store_true")
 a=p.parse_args()
 try:
  if a.action=="doctor":sys.exit(doctor())
  if a.action=="download-footage":
   run([sys.executable,ROOT/"documentary_editor.py","download"])
  if a.action=="download-architecture":
   run([sys.executable,ROOT/"cinematic_blender"/"fetch_cc0_assets.py"])
  if a.action=="render-3d":
   b=blender_path()
   if not b:raise RuntimeError("Blender not installed. Run windows/Install-Studio.ps1 -Install first.")
   cmd=[b,"-b","-t","4","-P",ROOT/"cinematic_blender"/"build_documentary_3d.py","--"]
   cmd+=["--final" if a.final else "--preview"]
   run(cmd)
  if a.action=="gemini-plan":
   run([sys.executable,ROOT/"gemini_full_voice.py","--plan"])
  if a.action=="master-voice":
   run([sys.executable,ROOT/"audio"/"master_urdu_voice.py","--input",a.input,"--output",a.output])
  if a.action=="motion-preview":
   npm=shutil.which("npm.cmd" if os.name=="nt" else "npm")
   if not npm:raise RuntimeError("Node/npm not installed")
   run([npm,"run","preview"],cwd=ROOT/"motion")
  if a.action=="render-full-browser":
   if not Path(a.base).exists() or not Path(a.srt).exists():
    raise FileNotFoundError("Need the verified 6-7 minute base video AND matching Urdu subtitles")
   node=shutil.which("node")
   if not node:raise RuntimeError("Install Node.js 18+ first")
   for idx in range(8):
    motiondir=ROOT/a.motion_dir
    motiondir.mkdir(parents=True,exist_ok=True)
    path=motiondir/("scene_%02d.mp4"%idx)
    if not path.exists():
     run([node,ROOT/"browser_motion"/"render.mjs",
          ROOT/"browser_motion"/"full_documentary_scenes.html",
          "--out",path,"--scene",idx,"--width",1920,"--height",1080,"--fps",25,"--seconds",7.5])
   run([sys.executable,ROOT/"browser_motion"/"full_documentary_assemble.py",
       "--base",a.base,"--srt",a.srt,"--motion-dir",motiondir,"--out",a.out])
  if a.action=="render-premium-pearl":
   if not Path(a.base).exists() or not Path(a.srt).exists():
    raise FileNotFoundError("Need the full 410-second documentary and its synchronized SRT")
   node=shutil.which("node")
   if not node:raise RuntimeError("Node.js not found")
   folder=ROOT/a.motion_dir
   folder.mkdir(parents=True,exist_ok=True)
   for i in range(24):
    mp4=folder/("premium_%02d.mp4"%i)
    if mp4.exists() and mp4.stat().st_size>100000:continue
    run([node,ROOT/"browser_motion"/"render.mjs",
        ROOT/"browser_motion"/"premium_pearl_motion.html",
        "--scene",str(i),"--out",mp4,"--width","1920","--height","1080",
        "--fps","25","--seconds","6","--pixel-format","yuv444p"])
   run([sys.executable,ROOT/"browser_motion"/"premium_full_assemble.py",
        "--base",a.base,"--srt",a.srt,"--motion-dir",folder,
        "--out",a.out,"--cache",ROOT/"premium_edited_segments"])
  if a.action=="export-otio":
   run([sys.executable,ROOT/"editorial"/"export_otio.py","--decisions",a.decisions,"--out",a.out])
  if a.action=="render-stock":
   if not a.approve_voice:
    raise RuntimeError("Explicit approval required: --approve-voice. No unreviewed synthetic TTS film.")
   for f in (a.voice,a.subtitles,a.music):
    if not Path(f).is_file():raise FileNotFoundError(f)
   run([sys.executable,ROOT/"documentary_editor.py","render",
        "--voice",a.voice,"--subtitles",a.subtitles,"--music",a.music])
 except (OSError,RuntimeError,subprocess.CalledProcessError) as e:
  print("STUDIO ERROR:",e,file=sys.stderr);sys.exit(2)
if __name__=="__main__":
 # Backwards-compatible v4 conductor: no dependencies or re-render until
 # the invoked subcommand explicitly requires them.
 if len(sys.argv)>1 and sys.argv[1] in ("documentary","studio-v4"):
  sys.exit(subprocess.call([sys.executable,str(ROOT/"production"/"studio_pipeline.py"),*sys.argv[2:]],cwd=str(ROOT)))
 main()
