#!/usr/bin/env python3
"""Generate segment-aligned Pakistani Urdu TTS and subtitles using free routes.
Choices: Piper ur-PK offline (MIT voice), Edge online (verify terms), Fish free-tier API (needs key).
No speech is relabelled as human narration. Voice files are generated ONLY from user-approved text.
"""
import argparse, asyncio, json, os, re, shutil, subprocess, sys
from pathlib import Path
import wave, contextlib
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT/'Pakistani_Urdu_Narration.txt'
VOICE=ROOT/'urdu_voice.wav'; CAPTIONS=ROOT/'urdu_timed.srt'


def call(cmd,inp=None):
 r=subprocess.run(cmd,input=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if r.returncode:raise RuntimeError(f'{cmd[0]} error: {r.stderr.decode("utf-8","replace")[-1500:]}')
 return r.stdout

def segments(text):
 text=re.sub(r'\r\n?', '\n', text)
 # Split the narration at sentence boundaries, keeping Urdu stops, and then breath commas.
 sentences=re.findall(r'[^۔؟!\n]+[۔؟!]?|\n+',text)
 out=[]
 for sentence in sentences:
  sentence=sentence.strip()
  if not sentence:continue
  if len(sentence)>220:
   bits=re.split(r'(?<=،)\s+',sentence)
   buf=''
   for b in bits:
    if buf and len(buf)+len(b)>155:
     out.append(buf.strip());buf=b
    else:buf=(buf+' '+b).strip()
   if buf:out.append(buf)
  else:out.append(sentence)
 return [x for x in out if len(x)>1]

def srt_time(s):
 ms=round(s*1000); h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000); sec,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{sec:02},{ms:03}'

def duration(file):
 r=call(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(file)])
 return float(r.strip())

def fetch(url,dest,limit=120_000_000):
 import requests
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size>2000: return
 with requests.get(url,stream=True,timeout=120,headers={'User-Agent':'Mozilla/5.0'}) as r:
  r.raise_for_status();total=0
  with open(str(dest)+'.part','wb') as f:
   for chunk in r.iter_content(1<<17):
    total+=len(chunk)
    if total>limit:raise RuntimeError('Download exceeded safety size cap')
    f.write(chunk)
 Path(str(dest)+'.part').replace(dest)


def piper_setup():
 models=ROOT/'models';models.mkdir(exist_ok=True)
 base='https://huggingface.co/rhasspy/piper-voices/resolve/main/ur/ur_PK/fasih/medium/'
 for ext in ('.onnx','.onnx.json'):
  file=models/('ur_PK-fasih-medium'+ext)
  if not file.exists():
   print('Downloading free Urdu Piper voice',file.name,flush=True)
   fetch(base+file.name,file)
 return models/'ur_PK-fasih-medium.onnx',models/'ur_PK-fasih-medium.onnx.json'

async def make_edge(segs,where,rate):
 import edge_tts
 for n,line in enumerate(segs):
  dest=where/f'speech_{n:03}.mp3'
  if not dest.exists():
   comm=edge_tts.Communicate(line,voice='ur-PK-AsadNeural',rate=rate)
   await comm.save(str(dest))
   if not dest.exists() or dest.stat().st_size<2000:raise RuntimeError('Cloud TTS returned no useful audio')
  print('VOICE',n+1,'/',len(segs),flush=True)

def make_piper(segs,where):
 model,config=piper_setup()
 executable=shutil.which('piper')
 if not executable:raise RuntimeError('Piper is not installed. Run: python -m pip install piper-tts')
 for n,line in enumerate(segs):
  dest=where/f'speech_{n:03}.wav'
  if not dest.exists():
   call([executable,'--model',str(model),'--config',str(config),'--output_file',str(dest)],(line+'\n').encode('utf-8'))
   if dest.stat().st_size<2000:raise RuntimeError(f'Piper made empty audio {n}')
  print('VOICE',n+1,'/',len(segs),flush=True)

def make_fish(segs,where):
 import requests
 key=os.getenv('FISH_API_KEY')
 if not key:raise RuntimeError('Set FISH_API_KEY in your system before using Fish free API. Do not paste secret in ChatGPT.')
 for n,line in enumerate(segs):
  dest=where/f'speech_{n:03}.mp3'
  if not dest.exists():
   response=requests.post('https://api.fish.audio/v1/tts',headers={'Authorization':f'Bearer {key}','model':'s2.1-pro-free','Content-Type':'application/json'},json={'text':line,'format':'mp3'},timeout=180)
   response.raise_for_status()
   if not response.headers.get('Content-Type','').startswith('audio/'):
    raise RuntimeError('Fish API did not return audio; check account/free tier and Urdu voice availability')
   dest.write_bytes(response.content)
  print('VOICE',n+1,'/',len(segs),flush=True)

def assemble(segs,where,pause):
 pcm=where/'pcm';pcm.mkdir(exist_ok=True)
 # Convert ALL segments to one consistent mono 48kHz PCM format; concatenate with natural small pauses.
 starts=[];t=0.0
 with wave.open(str(VOICE),'wb') as output:
  output.setnchannels(1);output.setsampwidth(2);output.setframerate(48000)
  for n,line in enumerate(segs):
   source=where/f'speech_{n:03}.mp3'
   if not source.exists():source=where/f'speech_{n:03}.wav'
   local=pcm/f'{n:03}.wav'
   if not local.exists(): call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-ar','48000','-ac','1','-c:a','pcm_s16le',str(local)])
   with wave.open(str(local),'rb') as wave_in:
    frames=wave_in.readframes(wave_in.getnframes());secs=len(frames)/(48000*2)
   starts.append((t,t+secs,line));output.writeframes(frames)
   output.writeframes(b'\0\0'*int(48000*pause));t+=secs+pause
 subtitles=''.join(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{line}\n\n' for i,(a,b,line) in enumerate(starts,1))
 CAPTIONS.write_text(subtitles,encoding='utf-8-sig')
 (ROOT/'voice_cue_times.json').write_text(json.dumps([{'start':round(a,3),'end':round(b,3),'text':text} for a,b,text in starts],ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'CREATED {VOICE} ({t:.1f} seconds), {CAPTIONS} ({len(starts)} timed cues)')
 if t<260 or t>660:print('QUALITY WARNING: narration duration differs significantly from the intended 6-8 minute story. Review voice settings and pace.',file=sys.stderr)

if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--engine',choices=['piper','edge','fish'],default='piper');a.add_argument('--pause',type=float,default=.23);a.add_argument('--rate',default='-6%',help='For Edge online neural voice, e.g. -6%')
 args=a.parse_args();where=ROOT/'voice_segments'/args.engine;where.mkdir(parents=True,exist_ok=True)
 segs=segments(SCRIPT.read_text(encoding='utf-8-sig'))
 print('Urdu sentences',len(segs),'Engine',args.engine,flush=True)
 if args.engine=='piper':make_piper(segs,where)
 elif args.engine=='edge':asyncio.run(make_edge(segs,where,args.rate))
 else:make_fish(segs,where)
 assemble(segs,where,args.pause)
