#!/usr/bin/env python3
"""Resumable v2 concatenation and actual media metadata validation."""
import hashlib,json,math,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=120)
 if p.returncode:raise RuntimeError(p.stderr[-1500:])
 return p.stdout

def main():
 tl=json.loads((ROOT/'timeline.json').read_text(encoding='utf8'))
 expected=round(float(tl[-1]['end'])*60)
 parts=sorted(ROOT.glob('part_*.mp4'),key=lambda p:int(p.stem.split('_')[1]))
 if len(parts)<3:raise RuntimeError('Need all rendered segments')
 frames=0
 for i,p in enumerate(parts):
  if p.stem!=f'part_{i}':raise RuntimeError('Missing numbered scene segment')
  d=json.loads(run(['ffprobe','-v','error','-of','json','-show_streams',p]))
  v=next(s for s in d['streams'] if s['codec_type']=='video')
  frames+=int(v.get('nb_frames','0'))
  if (v['width'],v['height'],v['r_frame_rate'])!=(1080,1920,'60/1'):
   raise RuntimeError('Unexpected source video specs: '+p.name)
 if frames!=expected:raise RuntimeError(f'FRAME_COUNT_GAP {frames} vs {expected}')
 path=ROOT/'concat_v2.txt'
 path.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in parts))
 silent=ROOT/'silent_v2.mp4'
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',path,'-c','copy',silent])
 voice=ROOT/'soundtrack.wav'
 if not voice.is_file():raise FileNotFoundError(voice)
 video=ROOT/'Pakistan_Property_Funny_Short_V2_9x16_1080p60.mp4'
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',silent,'-i',voice,'-map','0:v:0','-map','1:a:0',
  '-c:v','copy','-c:a','aac','-ar','48000','-b:a','192k','-t',f'{expected/60:.6f}',
  '-movflags','+faststart',video])
 d=json.loads(run(['ffprobe','-v','error','-of','json','-show_streams','-show_format',video]))
 v=next(s for s in d['streams'] if s['codec_type']=='video')
 a=next(s for s in d['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1080,1920,'60/1','h264')
 assert a['codec_name']=='aac' and int(v['nb_frames'])==expected
 report={'output':str(video.name),'seconds':float(d['format']['duration']),'frames':expected,
  'resolution':'1080x1920','fps':60,'video_codec':'h264','audio_codec':'aac',
  'voice':json.loads((ROOT/'voice_quality_report.json').read_text()),
  'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
  'publication_status':'REVIEW_ONLY, must approve voice acting and art'}
 (ROOT/'technical_report_v2.json').write_text(json.dumps(report,indent=2)+'\n')
 print('V2_FULL_VIDEO_TECHNICAL_PASS',json.dumps(report),flush=True)

if __name__=='__main__':main()