#!/usr/bin/env python3
"""Evidence-first animated motion graphics over real footage, timed using spoken Urdu cue data."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def tc(t):
 h=int(t//3600);m=int(t%3600//60);s=t%60
 return f'{h}:{m:02}:{s:05.2f}'
def esc(s):return str(s).replace('\\',r'\\').replace('{',r'\{').replace('}',r'\}').replace('\n',r'\N')
def make(total,path=None):
 path=Path(path or ROOT/'editorial_motion.ass')
 try:cues=json.loads((ROOT/'voice_cue_times.json').read_text(encoding='utf-8'))
 except (FileNotFoundError,ValueError):cues=[]
 def moment(*terms,ratio=.1):
  for c in cues:
   if any(k in c.get('text','') for k in terms):return float(c['start'])
  return total*ratio
 events=[]
 def emit(start,duration,style,tags,txt,layer=2):
  start=max(0.,float(start));end=min(total,start+float(duration))
  if end<=start:return
  events.append(f'Dialogue: {layer},{tc(start)},{tc(end)},{style},,0,0,0,,{tags}{esc(txt)}')
 def text(start,dur,label,style='Headline',x=1650,y=250):
  tag=r'{\move('+f'{x+25},{y},{x},{y},0,480'+r')\fad(260,450)}'
  emit(start,dur,style,tag,label)
 def rect(start,dur,x,y,w,h,color='&H00211D17&',alpha='&H50&',layer=0,scale=False):
  drawing=f'm 0 0 l {w} 0 l {w} {h} l 0 {h}'
  tags=r'{\an7\pos('+f'{x},{y}'+r')\bord0\shad0\1c'+color+r'\1a'+alpha+r'\p1'
  if scale:tags+=r'\fscx4\t(0,950,\fscx100)'
  tags+=r'\fad(260,370)}'
  emit(start,dur,'Vector',tags,drawing,layer)
 def slate(start,dur):
  rect(start,dur,125,180,1670,565,alpha='&H39&')
 start=moment('فرض کیجیے',ratio=.01)
 slate(start,10)
 text(start+.7,8,'فائل موجود ہے... زمین کہاں ہے؟','Main')
 text(start+5,5,'پاکستان پراپرٹی گروپ | خصوصی رپورٹ','Evidence',y=365)
 n=moment('بیالیس ہزار',ratio=.13)
 slate(n-1,22)
 text(n,18,'رپورٹ میں بتایا گیا: فائلوں اور زمین کا فرق','Headline',y=235)
 rect(n+3,12,240,362,320,44,'&H00C5BE70&','&H00&',1,True)
 rect(n+7,10,240,482,1140,44,'&H008B89EA&','&H00&',1,True)
 text(n+3.6,11,'تقریباً 6,000 پلاٹ','Number',y=338)
 text(n+7.5,9,'تقریباً 42,000 فائلیں','Number',y=464)
 text(n+14,7,'تقریباً 36,000 کا مبینہ فرق | حتمی عدالتی فیصلہ نہیں','Warning',y=620)
 files=moment('کاغذی فائل','فائل عام طور',ratio=.30)
 slate(files-1,17)
 text(files+1,10,'فائل اور زمین ایک چیز نہیں','Main',y=285)
 text(files+6,9,'کاغذی دعویٰ  ⇦  ملکیت  ⇦  منظور شدہ نقشہ','Headline',y=410)
 text(files+11,6,'ثبوت کہاں ہے؟ پلاٹ نمبر کہاں ہے؟','Evidence',y=565)
 investigation=moment('مالی ریکارڈ','تحقیقاتی','قومی احتساب',ratio=.43)
 slate(investigation-1,16)
 text(investigation+1,10,'تحقیقات میں اٹھنے والے تین سوال','Main',y=265)
 for i,label in enumerate(['ادائیگیوں کا مکمل ریکارڈ','الاٹمنٹ کی اصل دستاویز','پلاٹ کی حقیقی شناخت']):
  rect(investigation+2+i*3.5,9,240,360+i*94,75,15,'&H00EFAE7C&','&H00&',1,True)
  text(investigation+2+i*3.5,9,label,'Headline',y=340+i*94)
 text(investigation+11,6,'حوالہ: جیو نیوز، 8 مئی 2026','Foot',y=680)
 approved=moment('لی آؤٹ پلان','رجسٹریشن سرٹیفکیٹ','سی ڈی اے',ratio=.59)
 slate(approved-1,21)
 text(approved+.6,11,'قانونی منظوری کی تین الگ منزلیں','Main',y=245)
 for i,label in enumerate(['1 — سوسائٹی کا منظور شدہ نقشہ','2 — ترقیاتی کام کا این او سی','3 — اصل پلاٹ اور ملکیت کی تصدیق']):
  rect(approved+2+i*4.5,9,230,385+i*82,75,14,'&H00C5BE70&','&H00&',1,True)
  text(approved+2+i*4.5,9,label,'Headline',y=360+i*82)
 text(approved+13.7,7,'ماخذ: سی ڈی اے — ہاؤسنگ سکیموں کی سرکاری رہنمائی','Foot',y=680)
 for i,(needle,label) in enumerate([('پہلا قدم','سرکاری منظوری چیک کریں'),('دوسرا قدم','پلاٹ اور اصل ملکیت ملائیں'),('تیسرا قدم','موقع پر جا کر زمین دیکھیں'),('چوتھا قدم','آزاد وکیل سے جانچ کروائیں')]):
  t=moment(needle,ratio=.70+i*.038)
  slate(t,6)
  text(t+.6,5.4,f'0{i+1}     {label}','Main',y=390)
  rect(t+.2,5.5,260,520,900,12,'&H00BCB9A2&','&H00&',1,True)
 end=moment('آپ دیکھ رہے تھے',ratio=.94)
 slate(end,8)
 text(end+1,6.5,'ثبوت دیکھیں، پھر فیصلہ کریں','Main',y=365)
 text(end+4,4,'پاکستان پراپرٹی گروپ','Headline',y=480)
 header='''[Script Info]
Title: Pakistan Property Group | investigative motion graphics
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Noto Naskh Arabic,76,&H00FFFFFF,&H00FFFFFF,&H002D241B,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,9,65,65,0,1
Style: Headline,Noto Naskh Arabic,54,&H00FFFFFF,&H00FFFFFF,&H002D241B,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,9,65,65,0,1
Style: Number,Noto Naskh Arabic,62,&H00FFFFFF,&H00FFFFFF,&H002D241B,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,9,65,65,0,1
Style: Evidence,Noto Naskh Arabic,45,&H00EEEFF1,&H00FFFFFF,&H002D241B,&H00000000,0,0,0,0,100,100,0,0,1,2,1,9,65,65,0,1
Style: Foot,Noto Naskh Arabic,31,&H00E8E8E8,&H00FFFFFF,&H002D241B,&H00000000,0,0,0,0,100,100,0,0,1,1,1,9,65,65,0,1
Style: Warning,Noto Naskh Arabic,38,&H00FFFFFF,&H00FFFFFF,&H002D241B,&H00000000,0,0,0,0,100,100,0,0,1,2,1,9,65,65,0,1
Style: Vector,Noto Naskh Arabic,25,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 path.write_text(header+'\n'.join(events)+'\n',encoding='utf-8-sig')
 print('Built',len(events),'timed graphics events',path)
 return path
if __name__=='__main__':
 import sys
 make(float(sys.argv[1]) if len(sys.argv)>1 else 390)
