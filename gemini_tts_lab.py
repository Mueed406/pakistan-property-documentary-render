#!/usr/bin/env python3
"""Two short, opt-in Gemini Urdu TTS auditions; no full-film or recurring API calls."""
import argparse, base64, json, os, re, sys, wave
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"gemini_voice_output"
MODEL="gemini-2.5-flash-preview-tts"
PASSAGE=("آپ نے زندگی بھر کی کمائی سے ایک پلاٹ خریدا۔ رسید بھی موجود ہے، فائل پر نمبر بھی لکھا ہے۔ "
"لیکن جب آپ زمین دیکھنے جاتے ہیں، تو ایک اہم سوال سامنے آتا ہے۔ "
"کیا یہ کاغذ واقعی کسی موجود اور قانونی پلاٹ کا ثبوت ہے؟ "
"آٹھ مئی دو ہزار چھبیس کی ایک تحقیقاتی رپورٹ میں تقریباً بیالیس ہزار فائلوں اور چھ ہزار پلاٹوں کی گنجائش کا ذکر ہوا۔ "
"یہ رپورٹ میں بیان کیے گئے الزامات ہیں، کسی عدالت کا حتمی فیصلہ نہیں۔")
STYLES={
"Charon":"Mature male Pakistani Urdu investigative documentary narrator. Even, professional broadcast register and natural pronunciation. Use measured connected speech, moderate pace, consistent volume. Important numbers are slightly slower. No crying, wavering, sudden rushed words, tremble, singing, whispering, grand theatrical emotions or Hindi-style diction. Pause naturally at commas and full stops.",
"Schedar":"Warm, experienced male Pakistani Urdu news/documentary narrator. Very steady and conversational with fluid phrase-level timing. Normal words must be audible rather than rushed, natural vowel lengths and clear Urdu consonants. Subtle emphasis for figures and questions, never sobbing, shaky, robotic, theatrical or breathy. Maintain consistent volume and grounded pace."
}

def prompt(voice):
 if voice not in STYLES:raise ValueError("Unapproved voice")
 return ("DIRECTOR NOTES (these are NOT spoken): "+STYLES[voice]+
 "\nRead the following Urdu transcript VERBATIM, without reading these English directions. "
 "Do not add or omit anything, especially qualifiers. Speak only the Urdu words below.\n"
 "TRANSCRIPT:\n"+PASSAGE)

def payload(voice):
 return {"contents":[{"parts":[{"text":prompt(voice)}]}],
 "generationConfig":{"responseModalities":["AUDIO"],
 "speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voice}}}}}

def save_response(data,path):
 items=((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
 for item in items:
  inline=item.get("inlineData") or item.get("inline_data") or {}
  if inline.get("data"):
   pcm=base64.b64decode(inline["data"],validate=True)
   if len(pcm)<2000:raise ValueError("Audio was too short")
   path.parent.mkdir(parents=True,exist_ok=True)
   if pcm.startswith(b"RIFF"):path.write_bytes(pcm)
   else:
    if len(pcm)%2:raise ValueError("PCM size is odd")
    with wave.open(str(path),"wb") as f:
     f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(pcm)
   with wave.open(str(path),"rb") as f:
    secs=f.getnframes()/f.getframerate()
   if not (12<secs<115):raise ValueError(f"Unexpected duration: {secs:.1f}s")
   return round(secs,1)
 diag={"candidate_count":len(data.get("candidates") or []),
 "finish_reasons":[c.get("finishReason") for c in data.get("candidates",[])],
 "part_types":[list((p or {}).keys()) for c in data.get("candidates",[]) for p in ((c.get("content") or {}).get("parts") or [])],
 "prompt_feedback":data.get("promptFeedback"),"usage_keys":list((data.get("usageMetadata") or {}).keys())}
 print("TTS RESPONSE SHAPE (no content/audio/key):",json.dumps(diag,ensure_ascii=False)[:1500],flush=True)
 raise ValueError("Gemini HTTP 200 but returned no inline audio; inspect candidate finishReason and response format above")

def main():
 a=argparse.ArgumentParser()
 a.add_argument("--dry-run",action="store_true")
 a.add_argument("--voices",default="Charon,Schedar")
 args=a.parse_args()
 voices=[v.strip() for v in args.voices.split(",") if v.strip()]
 if not 1<=len(voices)<=2 or any(v not in STYLES for v in voices):
  raise SystemExit("Approved voices: Charon,Schedar (max 2 API calls)")
 if args.dry_run:
  print(json.dumps({"model":MODEL,"voices":voices,"prompts":[prompt(v) for v in voices]},
   ensure_ascii=False,indent=2))
  return
 key=os.environ.get("GEMINI_API_KEY","").strip()
 if not key:raise SystemExit("Missing GEMINI_API_KEY in repository secrets. No requests sent.")
 OUT.mkdir(exist_ok=True)
 results=[]
 for voice in voices:
  url="https://generativelanguage.googleapis.com/v1beta/models/"+MODEL+":generateContent"
  result=requests.post(url,headers={"x-goog-api-key":key,
   "Content-Type":"application/json"},json=payload(voice),timeout=(15,180))
  if result.status_code!=200:
   try:detail=(result.json().get("error") or {}).get("message","")
   except ValueError:detail=""
   if result.status_code==403 and "project has been denied access" in str(detail).lower():
    raise RuntimeError("GEMINI PROJECT ACCESS DENIED (403): Google rejected this project's access to the Gemini API. This is not a Node.js, Ubuntu, GitHub Secrets, or TTS prompt error. Do not retry or buy credits. Check Google AI Studio Projects/Billing and Google Cloud Console for an account/project restriction or appeal banner, then contact Google support if needed. No further Gemini calls made.")
   if result.status_code==403:
    raise RuntimeError("GEMINI PERMISSION DENIED (403): Check the API key's project permissions and supported model access in Google AI Studio. No automatic retries.")
   if result.status_code==429:
    raise RuntimeError("GEMINI QUOTA/RESOURCE LIMIT (429): Check free-tier limits in Google AI Studio. No automatic paid fallback.")
   raise RuntimeError(f"Gemini {result.status_code}: {str(detail)[:250]}. No paid fallback or auto-retry.")
  wav=OUT/("urdu_"+voice.lower()+".wav")
  sec=save_response(result.json(),wav)
  results.append({"voice":voice,"file":str(wav),"seconds":sec})
 (OUT/"report.json").write_text(json.dumps({"model":MODEL,"results":results,
 "transcript":PASSAGE,"note":"Human listening and exact-Urdu-word verification required."},
 ensure_ascii=False,indent=2),encoding="utf-8")
 (OUT/"LISTEN_FIRST.txt").write_text(
 "Compare these two Gemini samples with the earlier Piper B. "
 "Check authentic Pakistani Urdu, normal connecting-word speed, smooth syllables, "
 "no sobbing, and exact reported-claims wording. "
 "Never claim the voice is approved until listening.\n",encoding="utf-8")
 print(json.dumps(results,ensure_ascii=False))

if __name__=="__main__":main()
