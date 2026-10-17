#!/usr/bin/env python3
"""Visual QA for 24 premium pearl documentary overlays.

Checks actual decoded MOVING mp4 images, not just that FFmpeg exited 0.
Specifically flags pink/magenta chroma matte leaks and missing white/silver
editorial plates; creates a 24-scene review contact sheet. No OCR required.
"""
import argparse,json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageStat

def call(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-900:])

def qc(video,story,out):
 video=Path(video);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 story=json.loads(Path(story).read_text(encoding="utf-8-sig"))["story"]
 if len(story)!=24:raise ValueError("Expected exactly 24 rendered premium chapters")
 samples=[];failures=[];hashes=set()
 sheet=Image.new("RGB",(4*480,6*298),(245,247,248))
 d=ImageDraw.Draw(sheet)
 for i,q in enumerate(story):
  t=float(q["start"])+3
  dest=out/f"premium_{i:02}.png"
  call(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.3f}",
        "-i",video,"-frames:v","1","-vf","scale=960:540:flags=lanczos",dest])
  with Image.open(dest) as im:
   img=im.convert("RGB")
   # Matte leak check: near-pure fuchsia as opposed to natural skin or license-free footage.
   pixels=img.resize((240,135)).getdata()
   purple=sum(1 for r,g,b in pixels if r>200 and b>200 and g<86)
   magenta_pct=100*purple/(240*135)
   # The pearl plate occupies x=65:1855,y=60:706; at t+3 should be majority near-white.
   paper=img.crop((50,38,910,340)).resize((135,48))
   white=sum(1 for r,g,b in paper.getdata() if r>212 and g>212 and b>209)/ (135*48)
   key=hashlib.sha256(img.resize((56,32)).tobytes()).hexdigest()
   hashes.add(key)
   sample={"scene":i,"second":round(t,2),"magenta_percent":round(magenta_pct,4),
       "pearl_white_fraction":round(white,3),"short_caption":q["spoken_context"][:60]}
   samples.append(sample)
   if magenta_pct>.42:failures.append(f"Scene {i}: magenta key leakage {magenta_pct:.3f}%")
   if white<.18:failures.append(f"Scene {i}: missing light/paper animated foreground, whiteness={white:.3f}")
   thumb=img.resize((480,270))
   x=(i%4)*480;y=(i//4)*298
   sheet.paste(thumb,(x,y))
   d.text((x+8,y+274),f"Scene {i+1:02}/24 · {t:.1f}s",fill=(42,48,56))
 if len(hashes)<20:failures.append(f"Only {len(hashes)} distinct out of 24 sampled scenes")
 report={"movie":str(video),"scenes_checked":len(samples),"distinct_scene_samples":len(hashes),
  "checks":samples,"failures":failures,
  "note":"Technical palette/chroma check only; human Urdu and artistic review still required."}
 sheet.save(out/"premium_24_scene_contact_sheet.jpg",quality=94,subsampling=0)
 (out/"premium_color_motion_qc.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 if failures:raise RuntimeError("Premium color visual QC failed: "+"; ".join(failures))
 print("24 PREMIUM PEARL SHOT CHECKS PASS; no serious chroma leakage",flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--video",required=True);p.add_argument("--report",required=True);p.add_argument("--out",default="renders/pearl_palette_qc")
 a=p.parse_args();qc(a.video,a.report,a.out)
