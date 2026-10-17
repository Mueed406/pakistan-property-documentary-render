#!/usr/bin/env python3
"""Combine three verified exact-frame 15s render parts and one Urdu audio master."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
parts=[ROOT/f'part_{i}.mp4' for i in range(3)]
assert all(p.exists() and p.stat().st_size>20000 for p in parts),parts
sound=ROOT/'soundtrack.wav';assert sound.exists()
manifest=ROOT/'concat.txt';manifest.write_text(''.join(f"file '{p.as_posix()}'\n" for p in parts))
raw=ROOT/'silent.mp4';dest=ROOT/'Pakistan_Property_Funny_Short_9x16_1080p60.mp4'
def run(args):
 proc=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stderr[-1500:])
 return proc.stdout
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',manifest,'-c','copy',raw])
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',raw,'-i',sound,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart','-t','45',dest])
info=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',dest]));v=next(x for x in info['streams'] if x['codec_type']=='video');a=next(x for x in info['streams'] if x['codec_type']=='audio')
frames=int(v.get('nb_frames',0));dur=float(info['format']['duration'])
assert (v['width'],v['height'],v['r_frame_rate'])==(1080,1920,'60/1')
assert frames==2700,frames
assert 44.99<=dur<=45.2,dur
assert v['codec_name']=='h264' and a['codec_name']=='aac'
sha=hashlib.sha256(dest.read_bytes()).hexdigest()
report={'file':dest.name,'duration':dur,'resolution':'1080x1920','fps':60,'frames':frames,'codec':v['codec_name'],'audio_codec':a['codec_name'],'size':dest.stat().st_size,'sha256':sha,'audio_source':'Open Piper Urdu local neural TTS, human QC recommended','music':'original synthesized soundtrack','art':'original coded vector cartoon, no proprietary templates','publication_status':'review-only, not published to YouTube'}
(ROOT/'technical_report.json').write_text(json.dumps(report,indent=2))
print('SHORT_VERIFIED',json.dumps(report),flush=True)