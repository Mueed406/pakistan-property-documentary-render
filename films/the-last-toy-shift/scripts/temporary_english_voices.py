#!/usr/bin/env python3
"""FREE offline DRAFT English dialogue pipeline. NOT approved final voice acting.
Piper voice models have PER-MODEL licences; verify independent SHA256 and
MODEL_CARD before use. No copyrighted game audio, actor cloning, public model
redistribution or paid external API needed. 48kHz WAV per-character stems.
"""
import argparse, subprocess, json, os, io, wave, math, hashlib, urllib.request
from pathlib import Path
import numpy as np
BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US"
MODELS={
"hero":{"voice":"ryan","sha":"abf4c274862564ed647ba0d2c47f8ee7c9b717d27bdad9219100eb310db4047a",
        "license":"CC-BY-NC-SA-4.0","url":"https://www.kaggle.com/datasets/roholazandie/ryanspeech"},
"tape":{"voice":"sam","sha":"56417b3b4afe8ec6bb4cabf06e17d67261fdd5bf334592abcfc80052fba11163",
        "license":"Apache-2.0","url":"https://github.com/Sam-Accenture-Non-Binary-Voice/non-binary-voice-files"},
"doll":{"voice":"hfc_female","sha":"914c473788fc1fa8b63ace1cdcdb44588f4ae523d3ab37df1536616835a140b7",
        "license":"CC-BY-NC-SA-4.0","url":"https://ast-astrec.nict.go.jp/en/release/hi-fi-captain/"}
}
SCRIPT=[
 ("hero",7.2,3.45,"It's just another shift. Right?"),
 ("tape",22.5,3.55,"Don't follow the footsteps."),
 ("hero",31.2,2.30,"Who's there?"),
 ("hero",50.2,2.40,"Come on. Open!"),
 ("doll",59.0,4.65,"The door isn't locked to keep you out."),
 ("hero",71.1,2.60,"Then what's inside?")
]
SR=48000
DURATION=90
def run(argv,input=None):
 r=subprocess.run(argv,input=input,text=isinstance(input,str),capture_output=True)
 if r.returncode!=0:raise RuntimeError("Command failed: "+str(argv)+"\n"+str(r.stderr)[-1300:])
 return r

def acquire(role,modeldir):
 entry=MODELS[role]
 name="en_US-"+entry["voice"]+"-medium"
 base=BASE+"/"+entry["voice"]+"/medium/"+name+".onnx"
 target=modeldir/(name+".onnx")
 if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=entry["sha"]:
  req=urllib.request.Request(base,headers={"User-Agent":"TheLastToyShift/0.1-original-noncommercial-film"})
  with urllib.request.urlopen(req,timeout=140) as response:
   data=response.read()
  if hashlib.sha256(data).hexdigest()!=entry["sha"]:raise RuntimeError("Model SHA mismatch "+role)
  target.write_bytes(data)
 # Config and model card both must actually be available.
 cfg=target.with_suffix(".onnx.json")
 card=modeldir/(name+"-MODEL_CARD")
 for ext,destination in [(".onnx.json",cfg),("/MODEL_CARD",card)]:
  url=base[:-5]+ext if ext.startswith(".") else BASE+"/"+entry["voice"]+"/medium/MODEL_CARD"
  if not destination.exists():
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"TheLastToyShift/0.1"}),timeout=60) as resp:
    destination.write_bytes(resp.read())
 cardtext=card.read_text(errors="replace")
 if entry["license"]=="CC-BY-NC-SA-4.0" and "NC-SA" not in cardtext.lower().upper():
  raise RuntimeError("Non-commercial voice license not verified "+role+": "+cardtext)
 if entry["license"]=="Apache-2.0" and "apache" not in cardtext.lower():
  raise RuntimeError("Apache voice license not verified "+role+": "+cardtext)
 info={"model":name,"sha256":entry["sha"],"model_card":f"https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/{entry['voice']}/medium/MODEL_CARD",
       "license":entry["license"],"dataset":entry["url"],"credit":"Piper voice "+name+" (noncommercial demo usage)"}
 return target,info

def wavread(path):
 with wave.open(str(path),"rb") as w:
  sr=w.getframerate();channels=w.getnchannels();n=w.getnframes()
  pcm=np.frombuffer(w.readframes(n),dtype="<i2")
  return sr,pcm.reshape(-1,channels).astype(np.float32)/32768.

def place(destination,recording,start,duration):
 first=int(round(start*SR))
 max_count=int(round(duration*SR))
 arr=recording[:max_count]
 if arr.ndim==2:arr=arr.mean(axis=1)
 length=min(max_count,len(arr))
 # 80ms safety fades avoid transient hard clipping, preserve spoken words.
 fade=min(int(SR*.06),length//3)
 if fade:
  arr[:fade]*=np.linspace(0,1,fade)
  arr[length-fade:length]*=np.linspace(1,0,fade)
 destination[first:first+length]+=arr[:length]

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--out",default="output/voices_draft")
 args=parser.parse_args()
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 temp=out/"temp";temp.mkdir(exist_ok=True)
 models=out/"private_model_cache";models.mkdir(exist_ok=True)
 info={}
 for role in MODELS:_,info[role]=acquire(role,models)
 stems={role:np.zeros((DURATION*SR,),np.float32) for role in MODELS}
 cues=[]
 for j,(role,start,duration,line) in enumerate(SCRIPT):
  model=models/("en_US-"+MODELS[role]["voice"]+"-medium.onnx")
  raw=temp/("cue_%02d_raw.wav"%j)
  normalized=temp/("cue_%02d_48k.wav"%j)
  run(["piper","--model",str(model),"--output_file",str(raw)],input=line+"\n")
  sr,dat=wavread(raw)
  actual=len(dat)/sr
  if actual<=.05:raise RuntimeError("Empty spoken line "+line)
  # Speech aligned to slot without pitch shifting.
  ratio=actual/(duration-.18)
  if not .5<=ratio<=2:
   raise RuntimeError(f"Voice cue {j} {role} requires excessive time stretch {ratio}")
  filters=("highpass=f=250,lowpass=f=3200," if role=="tape" else "")+f"atempo={ratio:.5f}"
  run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(raw),
       "-af",filters,"-ar",str(SR),"-ac","1",str(normalized)])
  sr,pcm=wavread(normalized)
  if sr!=SR:raise RuntimeError("Incorrect resampling rate")
  place(stems[role],pcm,start,duration)
  cues.append({"character":role,"start_s":start,"max_duration_s":duration,"text":line,
               "original_duration":round(actual,3),"stretch_factor":round(ratio,4),
               "actual_file_sha256":hashlib.sha256(normalized.read_bytes()).hexdigest()})
 def writewav(path,mono):
  with wave.open(str(path),"wb") as w:
   w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
   left=np.clip(mono,-.95,.95);right=left
   interleaved=np.stack([left,right],axis=1)
   w.writeframes((interleaved*32767).astype("<i2").tobytes())
 for role,signal in stems.items():writewav(out/("DRAFT_"+role+"_english_90s.wav"),signal)
 total=sum(stems.values())
 peak=float(np.max(np.abs(total)))
 if peak>0.95:total*=0.75/peak
 writewav(out/"DRAFT_ALL_ENGLISH_DIALOGUE_NOT_FINAL.wav",total)
 metadata={"purpose":"Non-commercial INTERNAL English TTS audition ONLY; NOT final emotional acting.",
           "samples":DURATION*SR,"sample_rate":SR,"cues":cues,"voices":info,
           "release_authorized":False,
           "licence_notice":"Ryan/hfc_female CC-BY-NC-SA, Sam Apache-2.0; check current upstream terms before release. No raw voice models redistributed.",
           "artistic_warning":"Performance is standard neural TTS; no verified expressive acting, phoneme review or audience-ready dialogue mix."}
 (out/"VOICE_PROVENANCE.json").write_text(json.dumps(metadata,indent=2)+"\n")
 print(json.dumps({"results":"SUCCESS: draft stems only","cues":len(cues),
                   "samples":DURATION*SR,"voices":list(MODELS),"peak":peak}))
if __name__=="__main__":main()
