#!/usr/bin/env python3
"""Produce 410s documentary with 24 distinct pearl-white premium animated overlays
composited over moving, softened stock-footage shots. Preserve bottom subtitles
from crisp original master, and soundtrack+Urdu narration bit-for-bit.

The browser animation is a CHROMA MATTE, NOT a replacement dark background.
Every animated chapter has matching story timing and source attribution.
"""
import argparse,json,re,subprocess,sys
from pathlib import Path
FPS=25
CHAPTERS=24
DURATION=6.0
# Anchored to the ORIGINAL 83-cue Pakistani Urdu SRT from the 410-second stock film.
# Scene order is deliberately NOT numeric: editorial order follows spoken subject matter.
# Once full Gemini audio is approved, create a new aligned cue map instead of reusing this one.
CURATED_SCENE_CUES=[
 (0,"آپ کے ہاتھ میں خریداری کی رسید"),
 (1,"جب اصل زمین کی تصدیق کی باری"),
 (2,"لیکن ایک کاغذی فائل اور زمین"),
 (3,"مئی دو ہزار چھبیس کی رپورٹس"),
 (4,"اس فرق کو سمجھنے"),
 (5,"یعنی تقریباً چھتیس ہزار"),
 (6,"اگر ایک نقشے میں محدود جگہ"),
 (7,"اسی وجہ سے اصل ملکیتی"),
 (8,"ایک سوسائٹی کے نقشے پر سڑکیں"),
 (9,"اشتہار، نمائش، خوبصورت ماڈل"),
 (10,"خبر میں درج تفصیلات"),
 (11,"جب رقم ادا ہو جاتی ہے لیکن"),
 (12,"رپورٹس میں تحقیقاتی ذرائع"),
 (13,"تاہم مخصوص الزام کے بارے"),
 (14,"سوسائٹی کی رجسٹریشن"),
 (15,"رجسٹریشن سرٹیفکیٹ دکھائے"),
 (16,"اگر کوئی بروشر خوبصورت"),
 (17,"متعلقہ ادارے کی تازہ ترین حیثیت"),
 (18,"اگر سیلز نمائندہ جلدی"),
 (19,"سرکاری ویب سائٹ یا دفتر"),
 (20,"فائل اور پلاٹ کا نمبر مالک"),
 (21,"موقع پر جا کر زمین دیکھیں"),
 (22,"بڑی رقم دینے سے پہلے"),
 (23,"پہلے یہ معلوم کریں کہ زمین"),
]
def command(cmd):
 result=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,encoding="utf-8",errors="replace")
 if result.returncode:raise RuntimeError("FFmpeg/ffprobe exit "+str(result.returncode)+"\n"+result.stderr[-1800:])
 return result.stdout
def metadata(path):
 return json.loads(command(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
def srt_sec(s):
 m=re.search(r"(\d+):(\d+):(\d+)[.,](\d+)",s)
 if not m:raise ValueError("Unreadable subtitle timestamp")
 return int(m[1])*3600+int(m[2])*60+int(m[3])+int(m[4])/1000
def load_subtitles(srt):
 data=[]
 for chunk in re.split(r"\n\s*\n",Path(srt).read_text(encoding="utf-8-sig").replace("\r\n","\n")):
  lines=chunk.strip().split("\n")
  if len(lines)<3:continue
  hit=next((i for i,x in enumerate(lines) if "-->" in x),None)
  if hit is None:continue
  left,right=lines[hit].split("-->",1)
  data.append({"start":srt_sec(left),"end":srt_sec(right),"text":" ".join(lines[hit+1:])})
 if len(data)<40:raise RuntimeError("Not enough source-attributed Urdu subtitle cues")
 return data
def make_cues(cues,total):
 # Never silently fall back to uniformly spaced animations. Each segment MUST
 # match an actual voice/subtitle phrase, with a maximum 1.5s editorial shift.
 schedule=[]
 if len(CURATED_SCENE_CUES)!=CHAPTERS or len({s for s,_ in CURATED_SCENE_CUES})!=CHAPTERS:
  raise RuntimeError("Curated scene mapping must cover exactly 24 distinct chapters")
 for scene,phrase in CURATED_SCENE_CUES:
  matches=[q for q in cues if phrase in q["text"]]
  if len(matches)!=1:
   raise RuntimeError(f"Scene {scene}: expected one specific Urdu subtitle cue, got {len(matches)} for {phrase!r}")
  cue=matches[0]
  schedule.append({"scene":scene,"start":cue["start"],"duration":DURATION,
     "spoken_context":cue["text"][:100],"attribution":"conceptual graphic, not the actual investigated site",
     "subtitle_anchor":phrase,"sync_adjustment":0.0})
 schedule.sort(key=lambda q:q["start"])
 previous_end=0.0
 for q in schedule:
  actual=q["start"];aligned=max(actual,previous_end+0.08)
  if aligned-actual>1.5:
   raise RuntimeError(f"Scene {q['scene']} subtitle alignment collision ({aligned-actual:.2f}s)")
  if aligned+DURATION>total-1:
   raise RuntimeError(f"Scene {q['scene']} extends past actual film")
  q["start"]=round(aligned,3)
  q["sync_adjustment"]=round(aligned-actual,3)
  previous_end=aligned+DURATION
 return schedule
def clip_from(source,out,t,seconds):
 if out.exists() and out.stat().st_size>50000:return
 command(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.4f}","-i",source,
          "-t",f"{seconds:.4f}","-an","-vf","fps=25,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p",
          "-c:v","libx264","-preset","veryfast","-crf","19","-g","50","-r","25",out])
def composite(source,motion,out,start,length,smoke=False):
 if out.exists() and out.stat().st_size>40000:return
 # Keep source subtitles sharp at y>=785 while the area above them is blurred.
 # Browser animation background is #ff00ff and is keyed to transparency.
 filt=(
 "[0:v]fps=25,scale=1920:1080,split=2[stock][clean];"
 "[stock]eq=brightness=0.045:contrast=0.87:saturation=0.46,"
 "boxblur=luma_radius=10:luma_power=1:chroma_radius=10:chroma_power=1[soft];"
 "[clean]crop=1920:295:0:785[bottom];"
 "[soft][bottom]overlay=0:785:shortest=1[back];"
 "[1:v]fps=25,scale=1920:1080:flags=lanczos,format=yuva444p,"
 "colorkey=0xff00ff:0.14:0.015[art];"
 "[back][art]overlay=0:0:shortest=1:format=auto,format=yuv420p[out]"
 )
 command(["ffmpeg","-hide_banner","-loglevel","error","-y",
          "-ss",f"{start:.4f}","-i",source,"-i",motion,
          "-filter_complex",filt,"-map","[out]","-an","-t",f"{length:.4f}",
          "-c:v","libx264","-preset","veryfast" if smoke else "faster",
          "-crf","18","-g","50","-r","25",out])
def assemble(base,srt,graphics,out,cache,smoke=False):
 base=Path(base);srt=Path(srt);graphics=Path(graphics);out=Path(out);cache=Path(cache)
 cache.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
 original=metadata(base)
 total=float(original["format"]["duration"])
 if not smoke and not 400<=total<=425:raise RuntimeError("Not a verified six-to-seven-minute source film")
 if not any(x["codec_type"]=="audio" for x in original["streams"]):raise RuntimeError("Original narration/soundtrack absent")
 cues=load_subtitles(srt)
 schedule=make_cues(cues,total)
 if smoke:schedule=schedule[:1]
 parts=[];cursor=0
 for q in schedule:
  i=q["scene"];start=q["start"];end=start+q["duration"]
  motion=graphics/f"premium_{i:02d}.mp4"
  if not motion.is_file():raise FileNotFoundError("Premium browser scene missing: "+str(motion))
  if cursor+0.02<start:
   piece=cache/f"stock_{i:02d}.mp4";clip_from(base,piece,cursor,start-cursor);parts.append(piece)
  piece=cache/f"pearl_{i:02d}.mp4"
  composite(base,motion,piece,start,q["duration"],smoke=smoke)
  parts.append(piece);cursor=end
  print("Composited premium chapter",i+1,"/",len(schedule),"at",round(start,1),"sec",flush=True)
 if not smoke and cursor<total-.02:
  piece=cache/"outro_stock.mp4";clip_from(base,piece,cursor,total-cursor);parts.append(piece)
 lst=cache/"concatenate.txt"
 lst.write_text("".join("file '"+p.resolve().as_posix().replace("'","'\\''")+"'\n" for p in parts),encoding="utf-8")
 merged=cache/"silent_picture.mp4"
 command(["ffmpeg","-hide_banner","-loglevel","error","-y",
          "-f","concat","-safe","0","-i",lst,"-c","copy","-movflags","+faststart",merged])
 observed=float(metadata(merged)["format"]["duration"])
 expected=total if not smoke else schedule[0]["start"]+DURATION
 if abs(observed-expected)>2.1:raise RuntimeError(f"Sync drift {observed-expected:+.2f}s")
 # Original audio is mapped from the unchanged original full-length film.
 command(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",merged,"-i",base,
          "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy",
          "-t",f"{expected:.3f}","-movflags","+faststart",out])
 item=metadata(out);time=float(item["format"]["duration"])
 video=next(x for x in item["streams"] if x["codec_type"]=="video")
 assert (video["width"],video["height"])==(1920,1080)
 assert any(x["codec_type"]=="audio" for x in item["streams"])
 if not smoke and not 400<=time<=425:raise RuntimeError("Final full film duration invalid")
 report={"edition":"Premium Pearl / Silver 24-Chapter Documentary", "film":str(out),
  "seconds":time,"resolution":"1920x1080","motion_chapters":len(schedule),
  "story":schedule,"original_music_and_narration_preserved":True,
  "subtitle_lower_295px_kept_crisp":True,"stock_footage_softened_behind_animations":True,
  "voice":"Existing Piper synthetic narrator; full Gemini replacement not yet approved",
  "subtitle_alignment":"curated original Urdu SRT; no time-only fallbacks",
  "creative_review_required":True}
 out.with_suffix(".report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print("PREMIUM_FULL_FILM_COMPLETE",json.dumps({k:v for k,v in report.items() if k!="story"}),flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser()
 for arg in ["base","srt","motion-dir","out","cache"]:p.add_argument("--"+arg,required=True)
 p.add_argument("--smoke",action="store_true")
 a=p.parse_args()
 assemble(a.base,a.srt,a.motion_dir,a.out,a.cache,smoke=a.smoke)
