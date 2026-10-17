#!/usr/bin/env python3
"""Generate ONLY narrator and dealer as two distinct Pakistani Urdu neural voices.
The buyer is the EXISTING USER-PROVIDED ElevenLabs Zafar recording, selected
from the original. Do not substitute Zafar for other roles. Do not invent third
provider credit or upload user audio to GitHub.
"""
import asyncio, json, hashlib, time, sys
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"tts_edge"
OUT.mkdir(parents=True,exist_ok=True)
ROLES={
"narrator":{"voice":"ur-PK-UzmaNeural","rate":"+9%","pitch":"+0Hz",
  "direction":"Energetic witty off-screen Pakistani Urdu host; clear practical safety advice"},
"dealer":{"voice":"ur-PK-AsadNeural","rate":"+11%","pitch":"+3Hz",
  "direction":"Confident fast-talking Pakistani property salesman; dry punchline and tea gag"},
}
LINES=[
 {"id":1,"role":"narrator","text":"پاکستان میں پراپرٹی کا کاروبار؟ یہاں پلاٹ سے پہلے خوابوں کی بکنگ ہو جاتی ہے!"},
 {"id":2,"role":"dealer","text":"سر! آج فائل اٹھا لیں! کل ریٹ ڈبل! پرسوں آپ خود ڈیلر!"},
 {"id":3,"role":"buyer","text":"واہ! مگر پلاٹ کہاں ہے؟"},
 {"id":4,"role":"dealer","text":"سر، یہ نقشہ دیکھیں! اتنا خوبصورت کہ زمین بھی شرما جائے!"},
 {"id":5,"role":"buyer","text":"اچھا؟ این او سی کہاں ہے؟ ملکیت کس کے نام؟ قبضہ کب؟"},
 {"id":6,"role":"dealer","text":"ایک منٹ سر! ہماری چائے سو فیصد اصلی ہے!"},
 {"id":7,"role":"buyer","text":"چائے تو اصلی ہے، پلاٹ کب اصلی ہوگا باس؟"},
 {"id":8,"role":"narrator","text":"مذاق اپنی جگہ! پیسہ آپ کا ہے! لوکیشن خود دیکھیں، منظوری متعلقہ ادارے سے چیک کریں۔"},
 {"id":9,"role":"narrator","text":"ملکیت، رجسٹری اور سارے چارجز لکھ کر لیں! بڑا بورڈ گارنٹی نہیں!"},
 {"id":10,"role":"narrator","text":"پاکستان پراپرٹی گروپ! پہلے تحقیق، پھر سرمایہ کاری!"},
 {"id":11,"role":"buyer","text":"اگلا پلاٹ بھی چیک کروانا ہے؟ سبسکرائب کرو!"},
 {"id":12,"role":"dealer","text":"اور چائے میری طرف سے!"},
]

async def one(line):
 role=line["role"]
 if role=="buyer":return {"id":line["id"],"role":"buyer","status":"USER_ELEVENLABS_SOURCE_REQUIRED_LOCAL_ONLY"}
 opts=ROLES[role]
 path=OUT/f"line_{line['id']:02d}_{role}.mp3"
 if not path.exists() or path.stat().st_size<500:
  # Avoid paid services; standard Edge Urdu voices. A new voice is not proof
  # of human acting; all dialogue must be heard and approved.
  client=edge_tts.Communicate(line["text"],opts["voice"],rate=opts["rate"],pitch=opts["pitch"])
  await client.save(str(path))
 if path.stat().st_size<500:
  raise RuntimeError("Empty/generated voice at "+str(path))
 return {"id":line["id"],"role":role,"status":"generated","path":path.name,
  "bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
  "engine":"Microsoft Neural TTS via edge-tts","voice_id":opts["voice"],
  "text":line["text"],"delivery_direction":opts["direction"]}

async def main():
 results=[]
 for i,line in enumerate(LINES):
  # Generate sequentially to avoid rate limits and preserve exact receipts.
  result=await one(line);results.append(result)
  print("VOICE",i+1,"/",len(LINES),result["role"],result["status"],flush=True)
 report={"created_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
   "roles":{"narrator":"ur-PK-UzmaNeural (female, OFFSCREEN)",
           "dealer":"ur-PK-AsadNeural (male, ON SCREEN)",
           "buyer":"USER PROVIDED ElevenLabs Zafar (male, ON SCREEN, local only)"},
   "credits_spent":"No paid voice API; public Edge neural TTS generation",
   "line_count":len(LINES),"generated_edge_lines":len([x for x in results if x["status"]=="generated"]),
   "buyer_lines_need_original_user_recording":[3,5,7,11],
   "caution":"Needs human Urdu quality and voice performance review before public release.",
   "lines":results}
 (OUT/"VOICE_AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 assert len([x for x in results if x["status"]=="generated"])==8
 print("SUCCESS generated 8 independent Pakistani Urdu neural lines and role manifest")

if __name__=="__main__":
 try:asyncio.run(main())
 except Exception as exc:
  print("TTS_FAILED",repr(exc),file=sys.stderr)
  sys.exit(2)
