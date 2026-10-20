#!/usr/bin/env python3
"""Generate a measured Urdu narration and editorial music, using an open Piper voice.
Generates one voice file only; no retrying paid APIs. Voice needs human artistic approval.
"""
from __future__ import annotations
from pathlib import Path
import json, wave, os, subprocess, math, hashlib
import numpy as np
from scipy.signal import butter,sosfilt
ROOT=Path(__file__).resolve().parent
SAMPLE=48000;TARGET=45.0
VOICE_MODEL='https://huggingface.co/rhasspy/piper-voices/resolve/main/ur/ur_PK/fasih/medium/ur_PK-fasih-medium.onnx'
CONFIG_MODEL='https://huggingface.co/rhasspy/piper-voices/resolve/main/ur/ur_PK/fasih/medium/ur_PK-fasih-medium.onnx.json'

def run(cmd,inp=None):
 p=subprocess.run(list(map(str,cmd)),input=inp,capture_output=True,timeout=160)
 if p.returncode:raise RuntimeError(str(cmd[:3])+': '+p.stderr.decode('utf8','replace')[-1000:])
 return p.stdout

def fetch(url,path):
 if path.is_file() and path.stat().st_size>15000:return
 import requests
 r=requests.get(url,timeout=110,stream=True)
 r.raise_for_status()
 if int(r.headers.get('content-length','0'))>120_000_000:raise RuntimeError('Model too large')
 with path.open('wb') as f:
  size=0
  for chunk in r.iter_content(1024*512):
   size+=len(chunk)
   if size>120_000_000:raise RuntimeError('Model size over limit')
   f.write(chunk)

def wavarr(path):
 with wave.open(str(path),'rb') as w:
  rate=w.getframerate(); raw=w.readframes(w.getnframes()); channels=w.getnchannels();width=w.getsampwidth()
 if width!=2:raise ValueError('Expected 16bit PCM')
 arr=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
 if channels>1:arr=arr.reshape(-1,channels).mean(axis=1)
 if rate!=SAMPLE:
  from scipy.signal import resample_poly
  arr=resample_poly(arr,SAMPLE,rate)
 return arr

def writewave(path,arr):
 arr=np.clip(arr,-1,1);pcm=(arr*32767).astype(np.int16)
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SAMPLE);w.writeframes(pcm.tobytes())

def speech():
 m=ROOT/'models';m.mkdir(exist_ok=True)
 model=m/'ur_PK-fasih-medium.onnx';cfg=m/'ur_PK-fasih-medium.onnx.json'
 fetch(VOICE_MODEL,model);fetch(CONFIG_MODEL,cfg)
 d=json.loads(cfg.read_text(encoding='utf8'))
 d.setdefault('inference',{}).update({'length_scale':0.91,'noise_scale':0.51,'noise_w':0.45})
 cfg.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8')
 src=json.loads((ROOT/'script.json').read_text(encoding='utf8'))
 voiceparts=[]
 for i,v in enumerate(src['sections']):
  p=ROOT/f'speech_{i:02}.wav'
  if not p.exists():run(['piper','--model',model,'--config',cfg,'--output_file',p],(v['urdu']+'\n').encode('utf-8'))
  data=wavarr(p)
  # Silence trim only, leave a small human-readable breath margin.
  inds=np.where(np.abs(data)>.005)[0]
  if len(inds)>0:data=data[max(0,inds[0]-1200):min(len(data),inds[-1]+1600)]
  voiceparts.append(data)
 dur=sum(len(x)/SAMPLE for x in voiceparts)
 # If the waveform exceeds 44.2 sec, speed up gently, never drop clauses.
 if dur>42.2:
  import scipy.signal
  ratio=min(1.19,dur/41.4)
  if ratio>1.0:
   # ffmpeg atempo keeps pitch while adjusting duration.
   for i,x in enumerate(voiceparts):
    f=ROOT/f'tmp{i}.wav';g=ROOT/f'tmp{i}_fast.wav';writewave(f,x)
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',f,'-af',f'atempo={ratio:.5f}',g]);voiceparts[i]=wavarr(g)
   dur=sum(len(x)/SAMPLE for x in voiceparts)
 if dur>43.3:raise RuntimeError(f'Narration still too long for 45-second Short: {dur:.2f}. Edit script first.')
 # Spread the remaining time into expressive pauses, favor jokes and closing.
 gaps=[.21,.28,.18,.25,.25,.35,.20,.23,.20,0.]
 spare=TARGET-dur-sum(gaps)-.7
 if spare<0:
  gaps=[max(.06,x+spare/9) for x in gaps]
 elif spare>0:
  gaps=[x+spare/9.0 if i<9 else x for i,x in enumerate(gaps)]
 timeline=[];buff=[];cursor=0.0
 for i,(q,x) in enumerate(zip(src['sections'],voiceparts)):
  start=cursor;end=start+len(x)/SAMPLE
  timeline.append({'scene':q['scene'],'start':round(start,6),'speech_end':round(end,6),'urdu':q['urdu'],'roman':q['roman']})
  buff.append(x.astype(np.float32));cursor=end
  if i<9:
   buff.append(np.zeros(int(gaps[i]*SAMPLE),np.float32));cursor+=gaps[i]
 for i,q in enumerate(timeline):q['end']=round(timeline[i+1]['start'] if i<9 else TARGET,6)
 raw=np.concatenate(buff)
 if len(raw)>int(TARGET*SAMPLE):raw=raw[:int(TARGET*SAMPLE)]
 if len(raw)<int(TARGET*SAMPLE):raw=np.pad(raw,(0,int(TARGET*SAMPLE)-len(raw)))
 writewave(ROOT/'narration.wav',raw)
 (ROOT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
 print('SPEECH DURATION',round(dur,2),'FULL',round(len(raw)/SAMPLE,2),flush=True)
 return raw, timeline

def music(timeline):
 N=int(TARGET*SAMPLE);sr=SAMPLE
 music=np.zeros(N,dtype=np.float32)
 # 118 BPM light plucked keyboard / cartoon pizzicato composition, original notes.
 bpm=118;step=60/bpm/2
 lead=[0,4,7,9,7,4,2,0,5,9,12,7,4,7,2,0]
 bass=[0,0,5,5,7,7,0,0]
 for n in range(math.ceil(TARGET/step)):
  pos=int(n*step*sr);secs=min(int(.36*sr),N-pos)
  if secs<=0:break
  x=np.arange(secs)/sr
  note=lead[n%len(lead)];f=246.94*2**(note/12)
  env=np.exp(-x*12)*(1-np.exp(-x*85))
  tone=(np.sin(2*np.pi*f*x)+.35*np.sin(4*np.pi*f*x)+.16*np.sin(6*np.pi*f*x))*env*.042
  music[pos:pos+secs]+=tone
  if n%2==0:
   f2=82.41*2**(bass[(n//2)%len(bass)]/12)
   music[pos:pos+secs]+=.060*np.sin(2*np.pi*f2*x)*np.exp(-x*10)
  if n%4==2:
   rng=np.random.default_rng(n*111);noise=rng.standard_normal(secs)
   music[pos:pos+secs]+=(noise*.015*np.exp(-x*44)).astype(np.float32)
 # Cartoon zips at narration scene boundaries, tea-ding on 5, and soft bubble pops.
 effects=np.zeros(N,dtype=np.float32)
 for i,q in enumerate(timeline[1:],1):
  at=int(q['start']*sr);duration=min(int(.22*sr),N-at)
  if duration<=0:continue
  z=np.arange(duration)/sr;rng=np.random.default_rng(i*37)
  whoosh=(rng.standard_normal(duration)*np.exp(-z*16)*np.sin(np.pi*z/.22)**2).astype(np.float32)
  effects[at:at+duration]+=.060*whoosh
  if i in (1,3,5,7,9):
   bell=.065*np.sin(2*np.pi*(880+200*z)*z)*np.exp(-z*25)
   effects[at:at+duration]+=bell
 # Sidechain-style attenuation under Urdu narration based on local RMS envelope.
 voice=wavarr(ROOT/'narration.wav')[:N]
 if len(voice)<N:voice=np.pad(voice,(0,N-len(voice)))
 mix=np.clip(voice*.88+music*.75+effects,-.96,.96)
 # Gentle limiting, non-destructive.
 mix=np.tanh(mix*1.12)/np.tanh(1.12)
 writewave(ROOT/'soundtrack.wav',mix)
 print('SOUNDTRACK DURATION',len(mix)/SAMPLE,'peak',max(abs(mix)),flush=True)

if __name__=='__main__':
 voice,timeline=speech();music(timeline)