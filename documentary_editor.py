#!/usr/bin/env python3
"""Pexels-sourced HD documentary renderer, with voice-first editorial timeline.
Requires FFmpeg, ffprobe, requests; keeps all decisions editable in CSV.
No TTS or footage is fabricated. Won't export without narration and real clips.
"""
import argparse,csv,json,os,random,subprocess,sys,time,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CSV=ROOT/'Stock_Footage_Manifest_47.csv'
FOOTAGE=ROOT/'footage'
OUT=ROOT/'renders'

def cmd(args):
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode: raise RuntimeError(' '.join(map(str,args))+'\n'+r.stderr[-1500:])
 return r.stdout

def probe(path):
 return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def media_seconds(path):
 return float(probe(path)['format']['duration'])

def get_rows():
 with CSV.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def download(args):
 try: import requests
 except ImportError: raise SystemExit('Install requests: python -m pip install requests')
 FOOTAGE.mkdir(exist_ok=True)
 items=get_rows()
 if args.ids:items=[x for x in items if x['id'] in args.ids.split(',')]
 seen=0
 for item in items:
  dest=FOOTAGE/(item['id']+'.mp4')
  if dest.exists() and dest.stat().st_size>150_000:print('KEEP',dest.name);continue
  if '_640_360_' in item['video_url']:
   print('SKIP low-resolution option',item['id']);continue
  print('GET',item['id'],item['description'],flush=True)
  try:
   r=requests.get(item['video_url'],timeout=55,stream=True,headers={'User-Agent':'Mozilla/5.0 (documentary editor)'})
   r.raise_for_status()
   if int(r.headers.get('Content-Length','0'))>180_000_000:raise ValueError('File exceeds 180 MB limit')
   n=0
   with open(str(dest)+'.partial','wb') as f:
    for chunk in r.iter_content(1<<16):
     n+=len(chunk)
     if n>180_000_000:raise ValueError('Downloaded clip exceeds limit')
     f.write(chunk)
   Path(str(dest)+'.partial').replace(dest)
   data=probe(dest)
   if not any(x['codec_type']=='video' for x in data['streams']):raise ValueError('No video stream')
   seen+=1
  except Exception as e:
   print('FAILED',item['id'],str(e)[:160]); dest.unlink(missing_ok=True);Path(str(dest)+'.partial').unlink(missing_ok=True)
 print('New downloads:',seen,'Total verified:',len(list(FOOTAGE.glob('S*.mp4'))))

def render(args):
 if not shutil.which('ffmpeg') or not shutil.which('ffprobe'): raise SystemExit('Need ffmpeg and ffprobe on PATH')
 voice=Path(args.voice)
 if not voice.is_file():raise SystemExit('STOP: natural Urdu voice WAV/MP3 absent. No robotic TTS substitutions.')
 if not args.subtitles or not Path(args.subtitles).is_file():raise SystemExit('STOP: synchronized Urdu .srt subtitles absent. Do not reuse unaligned subtitles.')
 tracks=media_seconds(voice)
 if not (360 <= tracks <= 425): raise SystemExit('DURATION QC FAILED: documentary must contain 360–425 sec of actual narrated content; got %.1fs. Revise script and regenerate voice; never pad with filler.'%tracks)
 rows=get_rows(); verified=[]
 for item in rows:
  v=FOOTAGE/(item['id']+'.mp4')
  if not v.exists():continue
  try:
   pr=probe(v); video=next(t for t in pr['streams'] if t['codec_type']=='video')
   if video['width']<1180 or video['height']<650:continue
   duration=float(pr['format']['duration']);
   if duration<4.0:continue
   verified.append(dict(**item,file=v,duration=duration))
  except Exception:continue
 if len(verified)<18:raise SystemExit('STOP: only %s eligible real-HD clips. Download at least 18 before export.'%len(verified))
 OUT.mkdir(exist_ok=True)
 # Act allocation: opening 12%, discrepancy 15%, paper 16%, investigation 16%, legality 16%, verification 16%, end 9%.
 acts=[('opening',.12,['city','handover','document']),('numbers',.15,['survey','bureaucracy','document']),
       ('transaction',.16,['handover','document','finance']),('investigation',.16,['investigation','bureaucracy','finance']),
       ('approval',.16,['survey','verification','bureaucracy']),('checklist',.16,['verification','construction','survey']),
       ('closing',.09,['city','handover','construction'])]
 shots=[]; rng=random.Random(2026); last=[]; cursor=0; ti=0
 while ti < tracks-.1:
  ratio=ti/tracks;z=0
  for label,frac,cats in acts:
   z+=frac
   if ratio<z:break
  avail=[r for r in verified if r['category'] in cats and r['id'] not in last[-6:]]
  if not avail:avail=[r for r in verified if r['category'] in cats] or verified
  avail.sort(key=lambda r:(r['id'] in last[-8:],r['duration']<8.0, rng.random()))
  item=avail[0];span=min(5.3 if label!='investigation' else 4.8,tracks-ti,item['duration']-.2)
  if span<3:span=min(tracks-ti,4.0);item=next((r for r in verified if r['duration']>6),item)
  span=max(.1,span)
  start=max(0.0, rng.uniform(0,max(0,item['duration']-span-.2)))
  shots.append(dict(id=item['id'],description=item['description'],category=label,source=str(item['file']),start=round(start,2),duration=round(span,2),from_time=round(ti,2)))
  last.append(item['id']);ti+=span
 (OUT/'edit_decisions.json').write_text(json.dumps(shots,indent=2,ensure_ascii=False),encoding='utf-8')
 print('Selected',len(shots),'moving HD shots from',len(set(x['id'] for x in shots)),'distinct verified real sources, narration',round(tracks,1),'s')
 fns=[]
 for i,s in enumerate(shots):
  output=OUT/f'seg_{i:03d}.mp4';fns.append(output)
  # Mild cinematic color and vignette, avoid fake camera pans or heavy filters.
  vf=f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=contrast=1.06:saturation=0.91:brightness=-0.008,format=yuv420p"
  if output.is_file():continue
  run=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(s['start']),'-i',s['source'],'-t',str(s['duration']),'-an','-vf',vf,'-r','25','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',str(output)]
  cmd(run); print('SHOT',i+1,'/',len(shots),s['id'],flush=True)
 concat=OUT/'shots.txt';concat.write_text(''.join("file '"+str(f.resolve()).replace("'","'\\''")+"'\n" for f in fns))
 base=OUT/'picture_lock.mp4'
 cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(base)])
 # ASS style fonts checked; subtitle sync still needs listening and human review.
 music=args.music
 mix=['-i',str(base),'-i',str(voice)]
 filters=['[1:a]aresample=48000,loudnorm=I=-17:TP=-1.5:LRA=10[voice]']
 if music and Path(music).is_file():
  mix+=['-stream_loop','-1','-i',str(music)]
  filters+=['[voice]asplit=2[vo][side]','[2:a]aresample=48000,volume=0.12[bg]','[bg][side]sidechaincompress=threshold=0.045:ratio=8:attack=30:release=400[duck]','[vo][duck]amix=inputs=2:duration=first:dropout_transition=2[mix]']
 else:filters+=['[voice]anull[mix]']
 # Subtitles + minimalist broadcast graphics over real video B-roll.
 from editorial_motion import make as build_motion
 motion=build_motion(tracks)
 from pathlib import Path as P
 sub=P(args.subtitles).resolve().as_posix().replace(':','\\:')
 vf="subtitles='"+sub+"':force_style='FontName=Noto Naskh Arabic,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H70000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=28',ass='"+motion.resolve().as_posix().replace(':','\\:')+"'"
 out=OUT/'Pakistan_Property_Stock_Documentary_FINAL.mp4'
 args2=['ffmpeg','-hide_banner','-loglevel','error','-y',*mix,'-filter_complex',';'.join(filters),'-map','0:v','-map','[mix]','-vf',vf,'-t',str(tracks),'-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
 cmd(args2)
 print('RENDERED',out,round(media_seconds(out),2),'seconds. Manual Urdu pronunciation and factual checks still required.')

def qc(args):
 p=Path(args.file);info=probe(p);v=[x for x in info['streams'] if x['codec_type']=='video'];a=[x for x in info['streams'] if x['codec_type']=='audio'];d=float(info['format']['duration'])
 result={'path':str(p),'duration_seconds':d,'video':bool(v),'audio':bool(a),'width':v[0]['width'] if v else 0,'height':v[0]['height'] if v else 0,'size_bytes':p.stat().st_size}
 print(json.dumps(result,indent=2));valid=(result['video'] and result['audio'] and result['width']>=1920 and result['height']>=1080 and 359<=d<=428);sys.exit(0 if valid else 2)

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
 a=sub.add_parser('download');a.add_argument('--ids',default='');a.set_defaults(func=download)
 a=sub.add_parser('render');a.add_argument('--voice',required=True);a.add_argument('--subtitles',required=True);a.add_argument('--music');a.set_defaults(func=render)
 a=sub.add_parser('qc');a.add_argument('--file',required=True);a.set_defaults(func=qc)
 args=parser.parse_args()
 try:args.func(args)
 except (RuntimeError,ValueError) as e:print('ERROR:',e,file=sys.stderr);sys.exit(1)
