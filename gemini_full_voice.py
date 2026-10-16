#!/usr/bin/env python3
"""Generate natural Pakistani Urdu documentary audio with the approved Gemini voice.

NO automatic paid fallback. All audio requests must be explicitly authorized
via the manually triggered Github workflow; set GEMINI_API_KEY as a secret.
Produces editable per-paragraph WAV clips, a consistent 48k master, measured
cue timings, and provisional SRT for independent subtitle alignment review.
"""
import argparse, base64, json, os, re, subprocess, sys, time, wave
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"gemini_full_voice"
MODEL="gemini-2.5-flash-preview-tts"
SCRIPT=ROOT/"Pakistani_Urdu_Narration.txt"
VOICE_NAME="Charon"
STYLE=("Mature male Pakistani Urdu investigative documentary presenter. Unhurried but not slow. "
 "Natural every-day Karachi/Islamabad television Urdu diction. Calm, confident and warm, never crying "
 "or tremulous. Smooth ordinary words, clear factual numbers, and moderate pauses only at natural "
 "clause boundaries. Gentle curiosity during questions, serious neutrality during allegations. "
 "Never rush conjunctions or small words. No news-anchor shouting or artificial overdrama. "
 "Stable microphone distance and stable vocal volume. No Hindi-heavy vocabulary.")
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/models/"+MODEL+":generateContent"

def chunks(text,max_chars=390):
 # End at real sentence boundaries, not arbitrary token counts.
 units=[x.strip() for x in re.split(r"(?<=[۔؟!])\s+",text.replace("\r"," ")) if x.strip()]
 results=[];buff=""
 for item in units:
  if len(item)>max_chars:
   if buff:results.append(buff);buff=""
   sub=[x.strip() for x in item.split("،") if x.strip()]
   tmp=""
   for part in sub:
    if tmp and len(tmp)+len(part)+1>max_chars:
     results.append(tmp);tmp=part
    else:tmp=(tmp+"، "+part).strip("، ")
   if tmp:results.append(tmp)
   continue
  if buff and len(buff)+len(item)+1>max_chars:
   results.append(buff);buff=item
  else:buff=(buff+" "+item).strip()
 if buff:results.append(buff)
 return results

def request_one(key,text):
 prompt=("VOICE PERFORMANCE INSTRUCTIONS (not spoken): "+STYLE+
 "\nRead Urdu TRANSCRIPT below exactly, without adding or omitting words. "
 "Do not read the instructions. Do not introduce any English. "
 "Keep breathing and syllable pacing naturally varied but consistent overall.\nTRANSCRIPT:\n"+text)
 data={"contents":[{"parts":[{"text":prompt}]}],
       "generationConfig":{"responseModalities":["AUDIO"],
                           "speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":VOICE_NAME}}}}}
 r=requests.post(ENDPOINT,headers={"x-goog-api-key":key,"Content-Type":"application/json"},
                 json=data,timeout=(15,180))
 if r.status_code!=200:
  try:err=(r.json().get("error") or {}).get("message","")
  except ValueError:err=""
  raise RuntimeError(f"Gemini speech service {r.status_code}: {str(err)[:160]}. No retry, no paid fallback.")
 parts=((r.json().get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
 for p in parts:
  inline=p.get("inlineData") or p.get("inline_data") or {}
  if inline.get("data"):
   raw=base64.b64decode(inline["data"],validate=True)
   if len(raw)<2000:raise ValueError("Audio too short")
   return raw
 raise RuntimeError("Gemini returned 200 without generated audio; stop and inspect response.")

def pcm_wav(raw,out):
 # Gemini 2.5 Flash Preview TTS returns 24k mono PCM16 or 24k WAV.
 if raw[:4]==b"RIFF":out.write_bytes(raw)
 else:
  if len(raw)%2:raise ValueError("PCM odd byte count")
  with wave.open(str(out),"wb") as w:
   w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(raw)
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(out),
   "-ar","48000","-ac","1","-c:a","pcm_s16le",str(out.with_suffix(".normalized.wav"))],check=True)
 out.with_suffix(".normalized.wav").replace(out)
 with wave.open(str(out),"rb") as w:return w.getnframes()/w.getframerate()

def timestamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f"{h:02}:{m:02}:{s:02},{ms:03}"

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--plan",action="store_true")
 ap.add_argument("--max-chunks",type=int,default=40)
 a=ap.parse_args()
 text=SCRIPT.read_text(encoding="utf-8-sig")
 segments=chunks(text)
 if not segments or len(segments)>a.max_chunks:raise SystemExit(f"Unsafe chunk count: {len(segments)}")
 print("PLANNED GEMINI TTS SEGMENTS",len(segments),flush=True)
 if a.plan:
  print(json.dumps({"chunks":len(segments),"chars":[len(x) for x in segments],
     "total_characters":sum(map(len,segments))},indent=2))
  return
 key=os.getenv("GEMINI_API_KEY","").strip()
 if not key:raise SystemExit("No Gemini secret available, stopping before any calls")
 OUT.mkdir(parents=True,exist_ok=True)
 all_cues=[]; t=0.;errors=[]
 for i,line in enumerate(segments):
  wav=OUT/f"narration_{i:03}.wav"
  if not wav.exists() or wav.stat().st_size<2000:
   raw=request_one(key,line)
   d=pcm_wav(raw,wav)
  else:
   with wave.open(str(wav),"rb") as w:d=w.getnframes()/w.getframerate()
  all_cues.append({"start":round(t,3),"end":round(t+d,3),"text":line,
                   "source":"Gemini Charon raw segment","file":wav.name})
  t+=d+.26
  print("Gemini segment",i+1,"/",len(segments),"seconds",round(d,1),flush=True)
  # Free-tier respecting delay; no retries.
  time.sleep(6)
 if not (360<=t<=435):
  raise SystemExit(f"Narration duration {t:.1f}s is outside intended 6-7:15 minutes. Check transcript/voice; no padding.")
 master=ROOT/"urdu_voice_gemini.wav"
 with wave.open(str(master),"wb") as writer:
  writer.setnchannels(1);writer.setsampwidth(2);writer.setframerate(48000)
  for cue in all_cues:
   path=OUT/cue["file"]
   with wave.open(str(path),"rb") as src:writer.writeframes(src.readframes(src.getnframes()))
   writer.writeframes(b"\0\0"*int(48000*.26))
 # Provisional SRT timings at paragraph/cue level. Subtitles require alignment QA.
 srt="".join(f"{i}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}\n\n"
   for i,c in enumerate(all_cues,1))
 (ROOT/"urdu_timed_gemini_review.srt").write_text(srt,encoding="utf-8-sig")
 (ROOT/"voice_cue_times_gemini.json").write_text(json.dumps(all_cues,ensure_ascii=False,indent=2),encoding="utf-8")
 print("CREATED GEMINI NARRATION",round(t,2),"seconds",len(all_cues),"clips. Subtitle time cues need manual split/alignment.",flush=True)

if __name__=="__main__":main()
