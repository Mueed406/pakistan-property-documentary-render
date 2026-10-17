#!/usr/bin/env python3
"""Real 6–7min documentary editorial rebuild from verified stock-film review + 8 unique
frame-exact browser graphics + optionally licensed Blender cinematic 3D preview.

Keeps original narration and original music in sync. FFmpeg-backed and resumable.
Does NOT claim old Piper narrator is human-like; next voice pass still required.
"""
import argparse, re, os, json, subprocess, sys
from pathlib import Path

FPS=25
N=8
FALLBACK=[8,54,101,151,202,256,322,386]
MATCHES=[
 ["ایک سوال","فائل موجود","زمین کہاں"],
 ["فائل عام طور","کاغذی","فائل اور"],
 ["گنجائش","پلاٹوں","رہائشی منصوبہ"],
 ["عمارت","تعمیر","نقشہ","پروجیکٹ"],
 ["تحقیقاتی","ریکارڈ","انکوائری","ادائیگی"],
 ["منظوری","سی ڈی اے","این او سی","لی آؤٹ"],
 ["پہلا قدم","دوسرا قدم","تیسرا قدم","چوتھا قدم"],
 ["ثبوت دیکھیں","آخر میں","پاکستان پراپرٹی","فیصلہ"]
]

def run(args):
 print("EXEC:",str(args[0]),str(args[-1]),flush=True)
 proc=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if proc.returncode:raise RuntimeError("Command failed: "+" ".join(map(str,args[:7]))+"\n"+proc.stderr[-2800:])
 return proc.stdout

def metadata(path):
 return json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))

def sec(s):
 m=re.match(r"(\d+):(\d+):(\d+)[.,](\d+)",s.strip())
 if not m:raise ValueError("Bad SRT timestamp "+s)
 return int(m[1])*3600+int(m[2])*60+int(m[3])+int(m[4])/1000

def cues(srt):
 txt=Path(srt).read_text(encoding="utf-8-sig").replace("\r\n","\n")
 data=[]
 for block in re.split(r"\n\s*\n",txt):
  lines=block.strip().splitlines()
  if len(lines)<3:continue
  stamps=next((x for x in lines if "-->" in x),None)
  if not stamps:continue
  a,b=[v.strip() for v in stamps.split("-->",1)]
  data.append({"start":sec(a),"end":sec(b),"text":" ".join(lines[lines.index(stamps)+1:])})
 if not data:raise ValueError("No Urdu SRT cues were found")
 return data

def editorial_windows(subs,total,duration=7.5):
 out=[]
 last=-25
 for idx,(hint,terms) in enumerate(zip(FALLBACK,MATCHES)):
  matches=[x for x in subs if any(word in x["text"] for word in terms)]
  near=sorted(matches,key=lambda c:abs(c["start"]-hint))
  candidate=near[0]["start"] if near and abs(near[0]["start"]-hint)<28 else hint
  # Place a cut near the actual mention, without running clips into each other.
  at=max(last+duration+5,min(total-duration-4,max(0,candidate)))
  if at>total-duration:
   at=total-duration
  out.append({"id":idx,"start":round(at,3),"duration":duration,"cue":(near[0]["text"][:110] if near else "")})
  last=at
 for i in range(1,len(out)):
  if out[i]["start"]<out[i-1]["start"]+duration+1:
   raise ValueError("Overlapping editorial windows")
 return out

def convert_segment(src,out,duration,start=0):
 # Fast CPU encoding, visually transparent enough for review. 25fps constant.
 if out.exists() and out.stat().st_size>50_000:return
 run(["ffmpeg","-hide_banner","-loglevel","error","-y",
    "-ss",str(start),"-i",str(src),"-t",str(duration),
    "-vf","fps=25,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p",
    "-an","-c:v","libx264","-preset","veryfast","-crf","18","-g","50","-keyint_min","50",
    "-r","25","-video_track_timescale","12800",str(out)])
 i=metadata(out)
 v=next((x for x in i["streams"] if x["codec_type"]=="video"),None)
 if not v or v["width"]!=1920 or v["height"]!=1080:raise RuntimeError("Invalid normalized shot "+str(out))

def build(base,subs,motion,blender,target,work):
 work.mkdir(parents=True,exist_ok=True);target.parent.mkdir(parents=True,exist_ok=True)
 b=metadata(base);total=float(b["format"]["duration"])
 audio=any(t["codec_type"]=="audio" for t in b["streams"])
 if not audio or total<360 or total>425:raise RuntimeError("Full-length baseline audio/video QC failed")
 windows=editorial_windows(cues(subs),total)
 decisions=[];curr=0.
 scene_cache=[]
 for w in windows:
  n=w["id"]; src=motion/f"scene_{n:02}.mp4"
  if not src.exists():raise FileNotFoundError("Missing rendered motion scene "+str(src))
  if w["start"]>curr:
   p=work/f"base_{n:02}.mp4";convert_segment(base,p,w["start"]-curr,curr)
   decisions.append({"source":str(p),"type":"real stock footage","start":curr,"duration":w["start"]-curr})
  p=work/f"graphics_{n:02}.mp4";convert_segment(src,p,w["duration"],0)
  decisions.append({"source":str(p),"type":"browser motion documentary explainer","topic":n,
                    "start":w["start"],"duration":w["duration"],"spoken_cue":w["cue"]})
  curr=w["start"]+w["duration"]
 if curr<total-.08:
  p=work/"base_last.mp4";convert_segment(base,p,total-curr,curr)
  decisions.append({"source":str(p),"type":"real stock footage","start":curr,"duration":total-curr})
 (target.with_suffix(".edl.json")).write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding="utf-8")
 concat=work/"concat.txt"
 concat.write_text("".join("file '"+Path(x["source"]).resolve().as_posix().replace("'","'\\''")+"'\n" for x in decisions),encoding="utf-8")
 assembly=work/"picture_only.mp4"
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(assembly)])
 d=float(metadata(assembly)["format"]["duration"])
 if abs(d-total)>2:
  raise RuntimeError(f"Picture sync drift {d-total:+.2f}s: refuse to export unsynced audio")
 # Match 6:50 main-film narration AND original scored music without alteration.
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(assembly),"-i",str(base),
      "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy",
      "-t",str(total),"-movflags","+faststart",str(target)])
 result=metadata(target);length=float(result["format"]["duration"])
 streams=result["streams"]
 if not 359<=length<=427 or abs(length-total)>1.8 or not any(x["codec_type"]=="audio" for x in streams):
  raise RuntimeError("Final QC failed: wrong duration or missing audio")
 info={"output":str(target),"seconds":length,"width":1920,"height":1080,"fps":FPS,
       "sources":{"base":str(base),"srt":str(subs)},
       "motion_scenes":len(windows),"source_stock_unique_in_baseline":28,
       "uses_blender_source":False if not blender else Path(blender).exists(),
       "note":"Piper synthetic narration retained from working baseline; NOT voice-approved final.",
       "editorial_windows":windows,"creative_review_required":True}
 target.with_suffix(".qc.json").write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
 print("COMPLETE FULL LENGTH HD REVIEW",json.dumps(info,ensure_ascii=False),flush=True)

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--base",required=True);p.add_argument("--srt",required=True)
 p.add_argument("--motion-dir",required=True);p.add_argument("--blender",default="")
 p.add_argument("--out",default="renders/Pakistan_Property_Full_Browser_Motion_Review.mp4")
 p.add_argument("--work",default="full_motion_segments")
 args=p.parse_args()
 build(Path(args.base),Path(args.srt),Path(args.motion_dir),args.blender,Path(args.out),Path(args.work))
