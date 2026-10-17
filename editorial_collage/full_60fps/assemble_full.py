#!/usr/bin/env python3
"""Frame-locked 410-second PPG editorial film assembler @ 1920x1080/60.
Movie creation checks each excerpt and does not claim real approved 60fps source footage.
Original 25fps stock is conformed to 60fps; new 2.5D graphics are animated at native 60fps.
"""
from pathlib import Path
import re,subprocess,json,math,os,time,sys,hashlib,shutil
ROOT=Path(os.environ.get('PPG_FULL_ROOT',Path(__file__).parent));SRC=ROOT/'base/renders/Pakistan_Property_Stock_Documentary_FINAL.mp4';SRT=ROOT/'base/urdu_timed.srt';OUT=ROOT/'master';PIECES=OUT/'pieces';PIECES.mkdir(parents=True,exist_ok=True)
FPS=60;TOTAL_FRAMES=round(410.4*60);STORY=json.loads((ROOT/'storyboard.json').read_text())
VIDEO=OUT/'PPG_Editorial_Documentary_FULL_410s_1080p60.mp4'

def run(cmd):
 r=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(' '.join(str(q) for q in cmd[:6])+' : '+r.stderr[-1700:])
 return r.stdout

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-of','json','-show_format','-show_streams',str(path)]))

def secs(st):
 a=st.strip().replace(',','.').split(':');return int(a[0])*3600+int(a[1])*60+float(a[2])
def timecode(t):
 i=int(round(t*1000));hh,i=divmod(i,3600000);mm,i=divmod(i,60000);ss,ms=divmod(i,1000);return f'{hh:02}:{mm:02}:{ss:02},{ms:03}'
def cues():
 blocks=re.split(r'\n\s*\n',SRT.read_text(encoding='utf-8-sig'))
 out=[]
 for b in blocks:
  ln=b.strip().splitlines()
  if len(ln)<3 or '-->' not in ln[1]:continue
  a,z=ln[1].split('-->');out.append((secs(a),secs(z),' '.join(ln[2:])))
 return out
CUES=cues()

def local_srt(start,end,path):
 chunks=[];k=1
 for a,b,text in CUES:
  aa=max(a,start);bb=min(b,end)
  if bb-aa <.12:continue
  chunks.append(f'{k}\n{timecode(aa-start)} --> {timecode(bb-start)}\n{text}\n\n');k+=1
 path.write_text('\n'.join(chunks),encoding='utf-8-sig')

def comp_norm(source,dest,startframe,frames,motion=False):
 if dest.exists() and dest.stat().st_size>100000:
  info=probe(dest);num=int(next(x for x in info['streams'] if x['codec_type']=='video').get('nb_frames',0))
  if num==frames:return
  dest.unlink()
 if motion:
  starttime=startframe/FPS
  srt=dest.with_suffix('.srt');local_srt(starttime,(startframe+frames)/FPS,srt)
  # Reposition original documentary's Urdu subtitles above the bottom of the paper collage.
  # Burn within each scene, no invisible black/magenta key.
  fmt="FontName=Noto Sans Arabic,FontSize=23,Alignment=2,MarginV=41,Outline=2,Shadow=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00151515"
  sf=str(srt).replace(':',r'\:').replace("'",r"\'")
  filt=f"fps=60,trim=end_frame={frames},setpts=N/(60*TB),drawbox=x=0:y=932:w=iw:h=148:color=0x171411@0.90:t=fill,subtitles=filename='{sf}':force_style='{fmt}',format=yuv420p"
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-vf',filt,'-an','-frames:v',str(frames),'-r',str(FPS),'-c:v','libx264','-preset','ultrafast','-crf','21','-pix_fmt','yuv420p','-threads','2',dest]
 else:
  starttime=startframe/FPS
  filt=f'fps=60,trim=end_frame={frames},setpts=N/(60*TB),format=yuv420p'
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{starttime:.7f}','-i',source,'-vf',filt,'-an','-frames:v',str(frames),'-r',str(FPS),'-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p','-threads','2',dest]
 run(cmd)
 actual=int(next(x for x in probe(dest)['streams'] if x['codec_type']=='video').get('nb_frames',0))
 if actual!=frames: raise RuntimeError(f'Wrong frame count {actual} != {frames} for {dest}')

def main():
 cursor=0;parts=[];info=[]
 for i,q in enumerate(STORY):
  s=round(q['start']*FPS);n=round(q['duration']*FPS)
  if s<cursor:raise ValueError(f'Overlap at {i}')
  gap=s-cursor
  if gap>0:
   p=PIECES/f'part_{len(parts):03}_stock.mp4'
   comp_norm(SRC,p,cursor,gap)
   parts.append(p);info.append({'kind':'stock','start':cursor,'frames':gap})
  src=ROOT/'motion'/f'shot_{i:02}.mp4'
  if not src.exists():raise FileNotFoundError(src)
  p=PIECES/f'part_{len(parts):03}_collage.mp4'
  comp_norm(src,p,s,n,motion=True)
  parts.append(p);info.append({'kind':'collage','start':s,'frames':n,'theme':q['title']})
  cursor=s+n
  print('ASSEMBLED',i+1,'/',len(STORY),'frame',cursor,'/',TOTAL_FRAMES,flush=True)
 if cursor<TOTAL_FRAMES:
  p=PIECES/f'part_{len(parts):03}_stock.mp4'
  comp_norm(SRC,p,cursor,TOTAL_FRAMES-cursor)
  parts.append(p);info.append({'kind':'stock','start':cursor,'frames':TOTAL_FRAMES-cursor})
 if sum(x['frames'] for x in info)!=TOTAL_FRAMES:raise ValueError('Frame gap')
 concat=OUT/'concat.txt'
 concat.write_text(''.join("file '"+p.resolve().as_posix()+"'\n" for p in parts),encoding='utf-8')
 silent=OUT/'silent_full.mp4'
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,'-c','copy','-movflags','+faststart',silent])
 # Source audio is mapped once from the original master, uninterrupted.
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',silent,'-i',SRC,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',f'{TOTAL_FRAMES/FPS:.3f}','-movflags','+faststart',VIDEO])
 data=probe(VIDEO);v=next(x for x in data['streams'] if x['codec_type']=='video');aud=next(x for x in data['streams'] if x['codec_type']=='audio')
 seconds=float(data['format']['duration'])
 if not (410<=seconds<=410.6):raise RuntimeError(f'bad duration {seconds}')
 if (v['width'],v['height'],v['r_frame_rate'])!=(1920,1080,'60/1'):raise RuntimeError('not 1080p60')
 report={'film':str(VIDEO),'duration_seconds':seconds,'codec':v['codec_name'],'resolution':'1920x1080','fps':'60/1','audio_codec':aud['codec_name'],'original_narration_preserved':True,'gemini_full_narration_unavailable':'API returned HTTP 429 after 7 of 17 sections','new_native_60fps_motion_chapters':len(STORY),'stock_footage_source_fps':25,'stock_motion_conformed_to_60':True,'frame_count_expected':TOTAL_FRAMES,'parts':info,'review_required':True,'illustrative_photos':True}
 (OUT/'MASTER_TECHNICAL_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print('FULL_FILM_COMPLETE',json.dumps({k:v for k,v in report.items() if k!='parts'}),flush=True)

if __name__=='__main__':main()