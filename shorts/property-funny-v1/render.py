#!/usr/bin/env python3
"""Produce genuine motion frames at 60fps from procedural original vector cartoon.
No AI still frames stretched into video. Last release only if full technical QC passes.
"""
from pathlib import Path
import argparse,subprocess,json,sys,time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--start',type=int,default=0)
 p.add_argument('--end',type=int,default=45)
 p.add_argument('--fps',type=int,default=60)
 p.add_argument('--scale',type=float,default=2)
 p.add_argument('--out',default='segment.mp4')
 a=p.parse_args()
 assert 0<=a.start<a.end<=45 and a.fps==60
 timeline=json.loads((ROOT/'timeline.json').read_text(encoding='utf8'))
 html=(ROOT/'cartoon.html').read_text(encoding='utf8')
 out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 width,height=round(540*a.scale),round(960*a.scale)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',str(a.fps),'-vcodec','mjpeg','-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(a.fps),'-g','120','-threads','2',str(out)]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--font-render-hinting=none'])
  ctx=browser.new_context(viewport={'width':540,'height':960},device_scale_factor=a.scale)
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load')
  page.wait_for_function('window.__ready',timeout=30000)
  page.evaluate('(v)=>window.__setTimeline(v)',timeline)
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  try:
   total=(a.end-a.start)*a.fps;t0=time.time()
   for n in range(total):
    t=a.start+n/a.fps
    page.evaluate('(t)=>window.renderFrame(t)',t)
    img=page.locator('#stage').screenshot(type='jpeg',quality=89,timeout=20000,animations='disabled')
    proc.stdin.write(img)
    if n%240==0:print('RENDER',a.start,a.end,n,'/',total,'elapsed',int(time.time()-t0),flush=True)
   proc.stdin.close();rc=proc.wait(timeout=180)
   if rc:raise RuntimeError(proc.stderr.read().decode(errors='replace')[-1200:])
   if errors:raise RuntimeError('Browser JS error: '+repr(errors))
  finally:
   if proc.poll() is None:proc.kill();proc.wait()
   browser.close()
 # Trust but verify actual encoded frames.
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]))
 video=next(s for s in info['streams'] if s['codec_type']=='video')
 if (video['width'],video['height'])!=(width,height) or video.get('r_frame_rate')!='60/1':raise RuntimeError('Wrong render metadata')
 if int(video.get('nb_frames',0)) != (a.end-a.start)*a.fps:raise RuntimeError('Wrong frame count')
 print('RENDER_OK',str(out),out.stat().st_size,flush=True)

if __name__=='__main__':main()