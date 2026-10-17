#!/usr/bin/env python3
"""High-energy Pakistani Urdu short narration director, 45s original music, real waveforms.

Providers: guarded ElevenLabs v4 (paid ONLY with ALLOW_PAID_TTS=1 + secret);
Azure ur-PK official (credentials required); or Edge Urdu neural (free unofficial
client, separate rights/terms check). No Piper fallback and no retry storms.
"""
from __future__ import annotations
import argparse,asyncio,json,os,math,subprocess,sys,wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT/'script.json'
SR=48000
ROLES={'narrator':('+13%','+4Hz'),'dealer':('+18%','+10Hz'),'buyer':('+5%','+14Hz')}
# ElevenLabs v4 understands tags; Azure and Edge do NOT speak inline English tags.
TAG={'narrator':'[excited]','dealer':'[mischievously]','buyer':'[curious]'}

def cmd(a):
 p=subprocess.run([str(x) for x in a],capture_output=True,text=True,timeout=150)
 if p.returncode:raise RuntimeError('command failed '+p.stderr[-900:])

def load_audio(path):
 temp=path.with_suffix('.normalized.wav')
 cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',path,'-ar',str(SR),'-ac','1','-c:a','pcm_s16le',temp])
 with wave.open(str(temp),'rb') as w:data=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
 temp.unlink(missing_ok=True)
 return data

def save_audio(path,data):
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())

def stamp(t):
 m=int(round(t*1000)); h,m=divmod(m,3600000);mn,m=divmod(m,60000);s,ms=divmod(m,1000)
 return f'{h:02}:{mn:02}:{s:02},{ms:03}'

def local_tags(row):
 return TAG[row.get('role','narrator')]+' '+row['urdu']

async def edge_speech(rows,where):
 import edge_tts
 for i,row in enumerate(rows):
  dest=where/f'line_{i:02}.mp3'
  if dest.exists() and dest.stat().st_size>1500:continue
  rate,pitch=ROLES.get(row.get('role','narrator'),ROLES['narrator'])
  speech=edge_tts.Communicate(row['urdu'],voice='ur-PK-AsadNeural',rate=rate,pitch=pitch,volume='+0%')
  await speech.save(str(dest))
  if dest.stat().st_size<1500:raise RuntimeError('Empty Edge Urdu narration at '+str(i))
  print('EDGE_URDU',i+1,'/',len(rows),flush=True)

def elevenlabs(rows,where):
 # Paid API gated explicitly. Eleven v4 models support Urdu; local voice choice
 # must have been validated for the Pakistani accent by an authorized owner.
 if os.getenv('ALLOW_PAID_TTS')!='1':raise RuntimeError('Paid ElevenLabs disabled: set ALLOW_PAID_TTS=1 after authorizing cost')
 key=os.environ.get('ELEVENLABS_API_KEY')
 if not key:raise RuntimeError('ELEVENLABS_API_KEY secret missing')
 voices={r:os.environ.get('ELEVENLABS_'+r.upper()+'_VOICE_ID') or os.environ.get('ELEVENLABS_VOICE_ID') for r in ('narrator','dealer','buyer')}
 if not all(voices.values()):raise RuntimeError('ElevenLabs verified voice ID(s) are not configured')
 import requests
 for i,row in enumerate(rows):
  dest=where/f'line_{i:02}.mp3'
  if dest.exists() and dest.stat().st_size>1500:continue
  role=row.get('role','narrator')
  url='https://api.elevenlabs.io/v1/text-to-speech/'+voices[role]
  payload={'text':local_tags(row),'model_id':'eleven_v4','language_code':'ur',
           'voice_settings':{'stability':0.4,'similarity_boost':0.75,'style':0.55,'use_speaker_boost':True}}
  response=requests.post(url,headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},json=payload,timeout=150)
  if response.status_code in (402,429):raise RuntimeError('ElevenLabs balance/quota blocked at segment '+str(i)+' HTTP '+str(response.status_code))
  response.raise_for_status()
  if not response.headers.get('content-type','').startswith('audio/') or len(response.content)<1500:
   raise RuntimeError('ElevenLabs did not return usable audio at segment '+str(i))
  dest.write_bytes(response.content)
  print('ELEVEN_V4',i+1,'/',len(rows),flush=True)

async def render_voice(rows,where,engine):
 if engine=='elevenlabs':elevenlabs(rows,where)
 elif engine=='edge':await edge_speech(rows,where)
 else:raise RuntimeError('Supported engines: edge/elevenlabs')

def audio_mix(rows,where,engine):
 chunks=[];durations=[]
 for i in range(len(rows)):
  part=where/f'line_{i:02}.mp3'
  if not part.is_file():raise FileNotFoundError(part)
  audio=load_audio(part)
  # trim silence without trimming plosives/breaths
  rms=np.convolve(np.abs(audio[::24]),np.ones(8)/8,'same')
  active=np.flatnonzero(rms>.009)
  if len(active):
   start=max(0,active[0]*24-int(.07*SR));end=min(len(audio),(active[-1]+1)*24+int(.11*SR))
   audio=audio[start:end]
  if len(audio)<.15*SR:raise RuntimeError('Unreasonably short narration scene '+str(i))
  # gentle upward compression; do NOT atempo robotic speech
  peak=np.max(np.abs(audio))+1e-6
  gain=min(2.0,.82/peak)
  audio=np.tanh(audio*gain*1.05)/np.tanh(1.05)
  chunks.append(audio.astype(np.float32));durations.append(len(audio)/SR)
 raw_speech=sum(durations)
 target=max(45.,math.ceil((raw_speech+3.5)*10)/10)
 if target>58.:raise RuntimeError(f'Narration {raw_speech:.1f}s is too long; shorten script rather than speed-squeeze it')
 gaps=[.34,.30,.25,.34,.35,.53,.22,.26,.30]  # longer comic tea-punchline pause
 leftover=target-raw_speech-sum(gaps)-.20
 if leftover<-.01:
  gaps=[max(.09,g+leftover/len(gaps)) for g in gaps]
 else:
  gaps=[x+leftover/len(gaps) for x in gaps]
 cursor=0.;samples=[];timeline=[]
 for i,(row,audio) in enumerate(zip(rows,chunks)):
  start=cursor;end=start+len(audio)/SR
  timeline.append({'scene':i,'start':round(start,6),'speech_end':round(end,6),
     'urdu':row['urdu'],'roman':row['roman'],'role':row.get('role','narrator')})
  samples.append(audio);cursor=end
  if i<len(gaps):
   samples.append(np.zeros(round(gaps[i]*SR),np.float32));cursor+=gaps[i]
 N=round(target*SR);voice=np.concatenate(samples)
 if len(voice)<N:voice=np.pad(voice,(0,N-len(voice)))
 else:voice=voice[:N]
 for i,row in enumerate(timeline):row['end']=timeline[i+1]['start'] if i<len(timeline)-1 else target
 save_audio(ROOT/'narration.wav',voice)
 (ROOT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 # 50Hz audio envelope = 20ms -> used for actual voice-synchronized mouth rigs
 energy=[]
 for start in range(0,N,960):
  sample=voice[start:start+960];energy.append(round(float(np.sqrt(np.mean(sample**2))) if len(sample) else 0.,5))
 (ROOT/'mouth_envelope.json').write_text(json.dumps(energy),encoding='utf8')
 subtitles=''.join(f"{i+1}\n{stamp(q['start'])} --> {stamp(q['speech_end'])}\n{q['urdu']}\n\n" for i,q in enumerate(timeline))
 (ROOT/'Urdu_Captions.srt').write_text(subtitles,encoding='utf-8-sig')
 # Music in the original code sat under the speech at too-high level with
 # constant synthesizer rhythm. V2 uses light arrangement + REAL RMS ducking.
 music=np.zeros(N,np.float32)
 bpm=128;beat=60/bpm;notes=[0,4,7,9,5,2,7,4];base=220.0
 for j in range(math.ceil(target/(beat/2))):
  pos=round(j*(beat/2)*SR);dur=min(round(.24*SR),N-pos)
  if dur<=0:continue
  tt=np.arange(dur)/SR;f=base*2**(notes[j%len(notes)]/12)
  env=np.exp(-tt*17)*(1-np.exp(-tt*90))
  music[pos:pos+dur]+=(.016*np.sin(2*np.pi*f*tt)+.005*np.sin(4*np.pi*f*tt))*env
  if j%2==0:music[pos:pos+dur]+=.015*np.sin(2*np.pi*(f/4)*tt)*np.exp(-tt*11)
 # Music is intentionally very low under VO; sparse comedic stings mark punchlines.
 sfx=np.zeros(N,np.float32)
 for i,q in enumerate(timeline):
  if i not in (1,2,3,5,8):continue
  at=round(q['start']*SR);d=min(round(.20*SR),N-at)
  if d<=0:continue
  t=np.arange(d)/SR
  rng=np.random.default_rng(i+190)
  chirp=(.028*np.sin(2*np.pi*(650+1300*t)*t)+.005*rng.standard_normal(d))*np.exp(-t*18)
  sfx[at:at+d]+=chirp.astype(np.float32)
 # Smooth voice-derived ducking envelope so music doesn't compete with punchlines.
 envelope=np.abs(voice)
 from scipy.ndimage import maximum_filter1d, gaussian_filter1d
 env=gaussian_filter1d(maximum_filter1d(envelope,size=3500),sigma=600)
 mix=voice*.98+music*(np.clip(.45-3.1*env,.12,.45))+sfx*.55
 mix=np.tanh(mix*1.10)/1.10
 save_audio(ROOT/'soundtrack.wav',mix)
 (ROOT/'voice_quality_report.json').write_text(json.dumps({
   'provider':engine,'total_seconds':target,'spoken_seconds':round(raw_speech,2),
   'script_clauses':len(rows),'sample_rate':SR,
   'pitch_speed_varies_by_character':engine=='edge',
   'audio_tag_acting':engine=='elevenlabs','paid_model_called':engine=='elevenlabs',
   'narration_needs_human_accent_approval':True,
   'original_piper_audio_reused':False},indent=2)+'\n')
 print('VO_FINISHED',round(raw_speech,2),'of',target,'seconds provider',engine,flush=True)

async def main():
 p=argparse.ArgumentParser()
 p.add_argument('--engine',choices=['edge','elevenlabs'],default='edge')
 a=p.parse_args()
 rows=json.loads(SCRIPT.read_text(encoding='utf8'))['sections'];where=ROOT/'voice_parts_v2'/a.engine
 where.mkdir(parents=True,exist_ok=True)
 await render_voice(rows,where,a.engine)
 audio_mix(rows,where,a.engine)

if __name__=='__main__':
 try:asyncio.run(main())
 except Exception as err:print('VOICE ERROR:',str(err),file=sys.stderr);sys.exit(2)