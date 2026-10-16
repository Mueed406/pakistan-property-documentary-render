#!/usr/bin/env python3
"""Build restrained native-script Urdu ASS motion-graphics overlays over actual B-roll.
No fabricated footage or 3D. Use source-accurate reported figures and disclaimers.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent

def tc(t):
 h=int(t//3600);m=int(t%3600//60);s=t%60
 return f'{h}:{m:02}:{s:05.2f}'

def esc(x):return x.replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n',r'\N')

def make(total,path=ROOT/'editorial_motion.ass'):
 # scale to the actual Urdu narration duration; no timecodes claimed to be manually synced.
 marks=[
  (.02,.083,'Headline','فائل موجود ہے۔۔۔ مگر زمین کہاں ہے؟',250,720),
  (.125,.19,'Stat','42,000 فائلیں؟',250,200),
  (.19,.24,'Stat','تقریباً 6,000 پلاٹوں کی گنجائش؟',250,200),
  (.24,.28,'Disclaimer','یہ رپورٹ کردہ الزامات ہیں، حتمی عدالتی فیصلہ نہیں',180,880),
  (.405,.43,'Evidence','8 مئی 2026  |  جیو نیوز کی تحقیقاتی رپورٹ',150,810),
  (.54,.575,'Evidence','منظور شدہ نقشہ  ≠  جاری شدہ این او سی',140,810),
  (.70,.735,'Evidence','1 — سرکاری منظوری کی تصدیق کریں',140,800),
  (.755,.79,'Evidence','2 — پلاٹ اور ملکیت کے کاغذات ملائیں',140,800),
  (.805,.84,'Evidence','3 — موقع پر جا کر زمین دیکھیں',140,800),
  (.85,.885,'Evidence','4 — آزاد وکیل سے جانچ کرائیں',140,800),
  (.955,.998,'Headline','پاکستان پراپرٹی گروپ',250,710)
 ]
 # These cards are brief overlays on REAL MOVING STOCK SHOTS; avoid full screen slides.
 content='''[Script Info]
Title: Pakistan Property Group Documentary Motion Graphics
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Headline,Noto Naskh Arabic,68,&H00FFFFFF,&H00FFFFFF,&H00303030,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,7,90,90,30,1
Style: Stat,Noto Naskh Arabic,84,&H00FFFFFF,&H00FFFFFF,&H00303030,&H70000000,-1,0,0,0,100,100,0,0,1,3,1,7,90,90,30,1
Style: Evidence,Noto Naskh Arabic,52,&H00FFFFFF,&H00FFFFFF,&H00303030,&H90000000,-1,0,0,0,100,100,0,0,1,2,1,7,90,90,30,1
Style: Disclaimer,Noto Naskh Arabic,40,&H00FFFFFF,&H00FFFFFF,&H00303030,&HA0000000,0,0,0,0,100,100,0,0,1,1,1,7,90,90,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 cues=[]
 f=ROOT/'voice_cue_times.json'
 if f.exists():
  try:cues=json.loads(f.read_text(encoding='utf-8'))
  except Exception:cues=[]
 keywords=['فرض کیجیے','بیالیس ہزار','چھ ہزار','الزامات','رپورٹس میں','رجسٹریشن','پہلا قدم','دوسرا قدم','تیسرا قدم','چوتھا قدم','پاکستان پراپرٹی گروپ']
 for idx,(st,en,style,label,x,y) in enumerate(marks):
  match=next((c for c in cues if keywords[idx] in c.get('text','')),None)
  a=round(max(0,match['start']-.2) if match else total*st,2)
  b=round(min(total,a+(7 if style=='Headline' else 5.5)) if match else total*en,2)
  # Motion is minimal: 22px vertical rise over .45s and a short fade, not a presentation-style graphic.
  motion=r'{\move('+f'{x},{y+22},{x},{y},0,470'+r')\fad(300,300)}'
  content+=f'Dialogue: 0,{tc(a)},{tc(b)},{style},,0,0,0,,{motion}{esc(label)}\n'
 path.write_text(content,encoding='utf-8-sig')
 return path
if __name__=='__main__':
 n=float(sys.argv[1]) if len(sys.argv)>1 else 420
 path=make(n)
 print(f'Created {path.name} for {n:.1f}s; motion graphics occur on the moving stock footage.')
