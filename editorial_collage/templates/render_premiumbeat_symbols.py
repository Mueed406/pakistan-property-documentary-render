#!/usr/bin/env python3
"""Embed actually acquired PremiumBeat free hand-drawn MOVs in a licensed final video.

Raw third-party template files are kept only in a temporary directory, not uploaded
or committed. Video must already be an approved, fact-checked production.
"""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, zipfile

SOURCES={
 'Arrow Side.mov', 'Burst Circle.mov', 'Check Mark.mov',
 'Curly Arrow 2.mov', 'Curly Arrow 3.mov', 'Curly Arrow 4.mov',
 'Curly Arrow 5.mov', 'Chunky Exclamation Point.mov',
}
COLORS={'red':(173,33,35),'gold':(239,183,25),'charcoal':(32,31,28)}

def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('ffmpeg failed: '+p.stderr[-2200:])
 return p.stdout

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def alpha(fmt):
 return any(token in fmt.lower() for token in ('yuva','rgba','bgra','argb','gbrap','abgr'))

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--input',required=True)
 ap.add_argument('--pack',required=True)
 ap.add_argument('--plan',required=True)
 ap.add_argument('--output',required=True)
 ap.add_argument('--report',required=True)
 ap.add_argument('--preset',default='fast',choices=['ultrafast','veryfast','faster','fast','medium'])
 ap.add_argument('--crf',type=int,default=18)
 a=ap.parse_args()
 inp=pathlib.Path(a.input).resolve();pack=pathlib.Path(a.pack).resolve()
 for p in (inp,pack):
  if not p.is_file():raise FileNotFoundError(p)
 config=json.loads(pathlib.Path(a.plan).read_text())
 events=config.get('events',[])
 if not 1<=len(events)<=30:raise ValueError('Expected 1 to 30 artistic events')
 d=probe(inp);v=next(x for x in d['streams'] if x['codec_type']=='video')
 aud=next((x for x in d['streams'] if x['codec_type']=='audio'),None)
 if not aud:raise ValueError('Original continuous narration absent')
 if v.get('avg_frame_rate')!='60/1':raise ValueError('Source must really be 60fps')
 width,height=int(v['width']),int(v['height']);duration=float(d['format']['duration'])
 used={e['file'] for e in events}
 if used-SOURCES:raise ValueError('Unreviewed third-party template name in plan '+repr(used-SOURCES))
 for e in events:
  t=float(e['at']);length=float(e.get('duration',1.2));scale=float(e.get('scale',.22))
  if t<.25 or t+length>=duration-.25:raise ValueError('Invalid event time')
  if not .5<=length<=3.0 or not .07<=scale<=.60:raise ValueError('Unsafe motion dimensions')
  if e['color'] not in COLORS:raise ValueError('Invalid palette')
  if not .2<=float(e.get('opacity',.55))<=.9:raise ValueError('Unsafe opacity')
  if not 0<=float(e['x'])<=.92 or not 0<=float(e['y'])<=.76:raise ValueError('Unsafe location')
  if float(e['y'])+scale>0.86:raise ValueError('Overlay would obscure subtitles')
 with tempfile.TemporaryDirectory(prefix='template-private-') as temp:
  with zipfile.ZipFile(pack) as z:
   names={pathlib.PurePosixPath(x.filename).name:x for x in z.infolist() if not x.is_dir()}
   for name in used:
    if name not in names:raise FileNotFoundError(f'Pack is missing {name!r}')
    item=names[name]
    if item.file_size>60_000_000:raise ValueError('Too-large motion template')
    with z.open(item) as input_stream,open(pathlib.Path(temp)/name,'wb') as out:
     shutil.copyfileobj(input_stream,out)
  selected=[e['file'] for e in events]; input_args=['-i',str(inp)]
  for name in selected:input_args+=['-i',str(pathlib.Path(temp)/name)]
  source_info={}
  for name in selected:
   m=probe(pathlib.Path(temp)/name)
   s=next(x for x in m['streams'] if x['codec_type']=='video')
   source_info[name]={'codec':s['codec_name'],'pix_fmt':s['pix_fmt'],
                       'native_alpha':alpha(s.get('pix_fmt','')),'duration':float(m['format']['duration'])}
  filters=[]
  # trim avoids padding at the end; unmodified source audio remains a direct AAC copy.
  filters.append('[0:v]format=yuv420p[v0]')
  desc=[]
  for i,event in enumerate(events):
   name=event['file'];index=i+1
   t=float(event['at']);length=float(event.get('duration',1.2));scale=float(event.get('scale',.22))
   w=max(32,int(round(width*scale/2)*2))
   x=int(round(float(event['x'])*width));y=int(round(float(event['y'])*height))
   red,green,blue=COLORS[event['color']]
   # Native-alpha QuickTime MOV is preferred. If the alpha channel is absent,
   # use a restrained dark-colour key as the original pack advertises pre-keyed animations.
   matte='' if source_info[name]['native_alpha'] else 'colorkey=0x000000:0.13:0.08,'
   overlay_in=f'[{index}:v]fps=60,format=rgba,{matte}scale={w}:-2:flags=lanczos,format=rgba,'
   overlay_in+=f'lutrgb=r={red}:g={green}:b={blue},colorchannelmixer=aa={float(event.get("opacity",.55)):.2f},'
   overlay_in+=f'fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={length-.18:.3f}:d=0.18:alpha=1,'
   overlay_in+=f'trim=duration={length:.4f},setpts=PTS-STARTPTS+{t:.4f}/TB[o{i}]'
   filters.append(overlay_in)
   filters.append(f'[v{i}][o{i}]overlay={x}:{y}:eof_action=pass:repeatlast=0:format=auto:enable=\'between(t,{t:.4f},{t+length:.4f})\'[v{i+1}]')
   desc.append({'file':name,'at':t,'duration':length,'x':x,'y':y,'color':event['color'],'size_px':w,'opacity':float(event.get('opacity',.55))})
  outfile=pathlib.Path(a.output).resolve();outfile.parent.mkdir(parents=True,exist_ok=True)
  command=(['ffmpeg','-hide_banner','-loglevel','error','-y']+input_args+
      ['-filter_complex',';'.join(filters),'-map',f'[v{len(events)}]','-map','0:a:0','-c:v','libx264',
       '-preset',a.preset,'-crf',str(a.crf),'-r','60','-pix_fmt','yuv420p','-c:a','copy',
       '-movflags','+faststart',str(outfile)])
  run(command)
  final=probe(outfile);fv=next(x for x in final['streams'] if x['codec_type']=='video')
  fa=next(x for x in final['streams'] if x['codec_type']=='audio')
  if (int(fv['width']),int(fv['height']),fv['avg_frame_rate']) != (width,height,'60/1'):
   raise RuntimeError('Rendered output specification mismatch')
  if abs(float(final['format']['duration'])-duration)>0.12:
   raise RuntimeError('Render duration mismatch')
  if fa['codec_name']!=aud['codec_name']:raise RuntimeError('Audio was not preserved')
  report={'template_provider':'PremiumBeat / Film Bodega','source_license':'commercial derivative allowed; no source redistribution',
          'source_page':'https://www.premiumbeat.com/blog/free-hand-drawn-animated-shapes/',
          'source_sha256':hashlib.sha256(pack.read_bytes()).hexdigest(),
          'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
          'output':outfile.name,'output_bytes':outfile.stat().st_size,
          'duration_seconds':float(final['format']['duration']),'resolution':[width,height],
          'fps':60,'video_codec':fv['codec_name'],'audio_codec':fa['codec_name'],
          'third_party_motion_events':desc,'source_streams':source_info,
          'raw_source_assets_published':False,'creative_review_required':True}
  pathlib.Path(a.report).parent.mkdir(parents=True,exist_ok=True)
  pathlib.Path(a.report).write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps({k:v for k,v in report.items() if k not in ('input_sha256','source_sha256','source_streams')},indent=2))

if __name__=='__main__':
 try:main()
 except Exception as e:
  print('TEMPLATE RENDER FAILED:',str(e),file=sys.stderr)
  sys.exit(2)