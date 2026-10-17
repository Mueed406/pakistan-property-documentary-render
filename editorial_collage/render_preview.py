#!/usr/bin/env python3
"""Offline deterministic Chromium Canvas animation renderer.
Data URLs avoid blocked file:// and localhost policy in some sandboxes.
"""
from pathlib import Path
import argparse,subprocess,time,os,json,base64
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser()
p.add_argument("--seconds",type=float,default=26.0)
p.add_argument("--fps",type=int,default=25)
p.add_argument("--out",default="editorial_collage/editorial_matte_26s.mp4")
p.add_argument("--width",type=int,default=1280)
p.add_argument("--height",type=int,default=720)
p.add_argument("--chromium",default=os.environ.get("CHROMIUM_PATH","/usr/bin/chromium"))
a=p.parse_args()
root=Path(__file__).resolve().parent
images={}
for f in (root/"assets").iterdir():
 if f.suffix.lower() in (".jpg",".png"):
  mime="image/jpeg" if f.suffix.lower()==".jpg" else "image/png"
  images[f.stem]="data:"+mime+";base64,"+base64.b64encode(f.read_bytes()).decode()
html=(root/"editorial_motion.html").read_text(encoding="utf-8")
needle="im.src='assets/'+n+(n==='paper'||n==='halftone'||n==='newsprint'?'.png':'.jpg')"
if needle not in html:raise RuntimeError("Unexpected HTML image loader")
html=html.replace(needle,"im.src=window.__inline[n]")
html=html.replace("<script>","<script>window.__inline="+json.dumps(images)+";</script><script>",1)
target=Path(a.out).resolve();target.parent.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=a.chromium,headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 page=browser.new_page(viewport={"width":a.width,"height":a.height})
 page.set_content(html,wait_until="load")
 page.wait_for_function("window.__ready",timeout=20000)
 ff=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","image2pipe",
  "-framerate",str(a.fps),"-vcodec","mjpeg","-i","pipe:0","-c:v","libx264","-preset",
  "veryfast","-crf","17","-pix_fmt","yuv444p","-movflags","+faststart",str(target)],stdin=subprocess.PIPE)
 try:
  for i in range(round(a.seconds*a.fps)):
   page.evaluate("(t)=>window.renderAt(t)",i/a.fps)
   ff.stdin.write(page.locator("#stage").screenshot(type="jpeg",quality=92))
   if i%(a.fps*5)==0:print(i,"frames rendered",flush=True)
  ff.stdin.close()
  if ff.wait()!=0:raise RuntimeError("FFmpeg encoding failed")
 finally:
  browser.close()
print("MP4 delivered",target,target.stat().st_size)
