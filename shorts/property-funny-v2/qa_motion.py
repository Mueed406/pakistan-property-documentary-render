#!/usr/bin/env python3
"""Independent frame-motion and technical QA. Fails on long freeze scenes.

Do not conflate a low-motion aesthetic with a missing render; animations that are
intended to be totally still need an explicit documented exclusion.
"""
import json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILE=ROOT/'Pakistan_Property_Funny_Short_V2_9x16_1080p60.mp4'
if len(sys.argv)>1:FILE=Path(sys.argv[1])
if not FILE.is_file():raise SystemExit('Missing video '+str(FILE))

def cmd(parts,timeout=160):
 r=subprocess.run(parts,capture_output=True,text=True,timeout=timeout)
 if r.returncode:raise RuntimeError((r.stderr or r.stdout)[-1000:])
 return (r.stdout or '')+(r.stderr or '')

metadata=json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(FILE)]))
v=next(x for x in metadata['streams'] if x['codec_type']=='video')
a=next(x for x in metadata['streams'] if x['codec_type']=='audio')
dur=float(metadata['format']['duration'])
if (v['width'],v['height'],v['avg_frame_rate'],v['codec_name'])!=(1080,1920,'60/1','h264'):
 raise RuntimeError('Technical video validation failed')
if a['codec_name']!='aac' or not 44.0<=dur<=58.0:raise RuntimeError('Invalid audio/duration')
freeze_log=cmd(['ffmpeg','-hide_banner','-nostats','-i',str(FILE),'-vf',
    'freezedetect=n=-55dB:d=1.2','-an','-f','null','-'],timeout=240)
starts=[float(x) for x in re.findall(r'lavfi\.freezedetect\.freeze_start:\s*([\d.]+)',freeze_log)]
ends=[float(x) for x in re.findall(r'lavfi\.freezedetect\.freeze_end:\s*([\d.]+)',freeze_log)]
intervals=[]
for i,start in enumerate(starts):
 end=ends[i] if i<len(ends) else dur
 intervals.append({'start':round(start,3),'end':round(end,3),'seconds':round(end-start,3)})
# Audio signal quality: warn about silence/clipping; human review separately.
audio_out=cmd(['ffmpeg','-hide_banner','-nostats','-i',str(FILE),'-af','volumedetect',
               '-vn','-f','null','-'],timeout=90)
peak=re.search(r'max_volume:\s*([-\d.]+) dB',audio_out)
peak_db=float(peak.group(1)) if peak else None
report={'source':str(FILE),'duration_seconds':round(dur,3),'fps':60,'size':'1080x1920',
        'long_freeze_intervals':intervals,'long_freeze_count':len(intervals),
        'audio_max_db':peak_db,'voice_human_approval_required':True,
        'passed':len(intervals)==0 and peak_db is not None and peak_db<=0.0}
path=FILE.parent/'motion_quality_report.json'
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if not report['passed']:raise SystemExit('MOTION/AUDIO QA FAILED. Review report and do not publish.')