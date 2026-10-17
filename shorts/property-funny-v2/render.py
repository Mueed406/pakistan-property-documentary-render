#!/usr/bin/env python3
"""V2 native 60fps cartoon renderer; audio RMS -> mouth rigs; variable duration.
Produces complete video segments without audio for later lossless concatenation.
"""
import argparse, json, math, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--part',type=int,required=True)
 p.add_argument('--seconds',type=int,default=15)
 p.add_argument('--scale',type=float,default=2)
 a=p.parse_args()
 timeline=json.loads((ROOT/'timeline.json').read_text(encoding='utf8'))
 duration=float(timeline[-1]['end'])
 start=a.part*a.seconds; end=min(duration,(a.part+1)*a.seconds)
 if start>=end-.005:
  print('NO_FRAMES_NEEDED',a.part,flush=True);return
 fps=60;width=int(540*a.scale);height=int(960*a.scale)
 count=round(end*fps)-round(start*fps)
 out=ROOT/f'part_{a.part}.mp4'
 if out.exists() and out.stat().st_size>30000:
  d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',out]))
  stream=next(x for x in d['streams'] if x['codec_type']=='video')
  if int(stream.get('nb_frames',0))==count and (stream['width'],stream['height'])==(width,height):
   print('REUSE_VALIDATED_PART',a.part,flush=True);return
  out.unlink()
 command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate','60',
  '-vcodec','mjpeg','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','17',
  '-pix_fmt','yuv420p','-r','60','-g','120','-threads','2',str(out)]
 html=(ROOT/'cartoon.html').read_text(encoding='utf8')
 envelope=json.loads((ROOT/'mouth_envelope.json').read_text(encoding='utf8'))
 with sync_playwright() as playwright:
  browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':540,'height':960},device_scale_factor=a.scale)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load');page.wait_for_function('window.__ready',timeout=18000)
  page.evaluate('(t)=>window.__setTimeline(t)',timeline)
  page.evaluate('(e)=>window.__setAudioEnvelope(e)',envelope)
  process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  try:
   at=round(start*fps);t0=time.time()
   for n in range(count):
    t=(at+n)/fps
    page.evaluate('(t)=>window.renderFrame(t)',t)
    pixels=page.locator('#stage').screenshot(type='jpeg',quality=90,timeout=17000,animations='disabled')
    process.stdin.write(pixels)
    if n%300==0:print('RENDER_PART',a.part,n,'/',count,'seconds',round(time.time()-t0,1),flush=True)
   process.stdin.close();rc=process.wait(timeout=120)
   if rc:raise RuntimeError(process.stderr.read().decode(errors='replace')[-1500:])
   if errors:raise RuntimeError('Javascript '+repr(errors))
  finally:
   if process.poll() is None:process.kill();process.wait()
   browser.close()
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',out]))
 v=next(x for x in d['streams'] if x['codec_type']=='video')
 assert v.get('r_frame_rate')=='60/1' and int(v.get('nb_frames',0))==count
 assert (v.get('width'),v.get('height'))==(width,height)
 print('V2_PART_VERIFIED',out,count,flush=True)

if __name__=='__main__':
 try:main()
 except Exception as exc:print('RENDER_FAIL',exc,file=sys.stderr);sys.exit(2)