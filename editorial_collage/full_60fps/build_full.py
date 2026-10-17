#!/usr/bin/env python3
"""Full PPG documentary editorial V3: original 2.5D paper cutout 60fps chapters.
Reuses licensed illustrative photos (NOT real case evidence), real narration+SRT,
and original 410s stock-film. No paid API or remote resources used here.
"""
import os,sys,math,random,re,json,subprocess,time,hashlib
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance,ImageFilter
ROOT=Path(os.environ.get('PPG_FULL_ROOT','/mnt/data/ppg_full_production'));ART=ROOT/'art';CLIPS=ROOT/'motion';ART.mkdir(exist_ok=True);CLIPS.mkdir(exist_ok=True)
SRC=ROOT/'base/renders/Pakistan_Property_Stock_Documentary_FINAL.mp4'
SRT=ROOT/'base/urdu_timed.srt'
ASSETS=ROOT/'assets';W,H,FPS=1920,1080,60
FNT='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf';COND='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf';MONO='/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf';SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Bold.ttf';ARABIC='/usr/share/fonts/truetype/noto/NotoSansArabic-SemiBold.ttf'
BLACK=(28,28,25);RED=(174,29,26);YELLOW=(248,194,21);CREAM=(239,232,209);PAPER=(250,244,226);SILVER=(151,146,133)
# Every shot is narrated context, NOT evidence from the accused cooperative society.
# Each planned insert is anchored in the original SRT by its exact cue number.
SCENES=[
 (1,'THE PROMISE','A PLOT. A FUTURE.','HOME'),
 (4,'BUT WHERE IS','THE ACTUAL','LAND?'),
 (6,'YOUR PURCHASE','BEGINS ON','PAPER'),
 (8,'A FILE NUMBER','IS NOT A','PLOT'),
 (10,'42,000','REPORTED','PLOT FILES'),
 (11,'6,000','INDICATED LAND','CAPACITY'),
 (12,'36,000','REPORTED','DIFFERENCE'),
 (13,'ALLEGATIONS','ARE NOT A','COURT VERDICT'),
 (15,'42,000 FILES','VERSUS','6,000 PLOTS'),
 (17,'UNDER','INVESTIGATION','NOT A VERDICT'),
 (20,'THE MASTER','PLAN','ON PAPER'),
 (23,'THE DREAM','OF A','HOME'),
 (24,'A FILE','IS NOT','THE LAND'),
 (25,'OWNERSHIP','PLOT ID &','APPROVAL'),
 (27,'BOOKING','IS NOT THE','TITLE'),
 (28,'PAPER RECORDS','CANNOT CREATE','MORE LAND'),
 (29,'CHECK','KHASRA AND','LEGAL MAPS'),
 (30,'FOLLOW','THE MONEY','AND RECORDS'),
 (31,'MORE THAN','RS 16 BILLION','REPORTED'),
 (32,'AN ARREST','IS NOT A','CONVICTION'),
 (35,'MISSING','PAYMENT','RECORDS'),
 (37,'VERIFY','EVERY','RECEIPT'),
 (38,'ONLY EVIDENCE','CAN ESTABLISH','RESPONSIBILITY'),
 (40,'BEFORE','YOU BUY','A PLOT'),
 (41,'REGISTRATION','IS NOT','NOC APPROVAL'),
 (43,'CHECK','OFFICIAL CDA','RECORDS'),
 (46,'A CERTIFICATE','DOES NOT','PROVE LAND'),
 (47,'A BROCHURE','IS NOT','POSSESSION'),
 (48,'CROSS CHECK','AUTHORITY','APPROVAL'),
 (49,'VERIFY','CURRENT','DOCUMENTS'),
 (51,'STEP 01','CHECK THE','AUTHORITY'),
 (53,'STEP 02','MATCH PLOT','AND OWNER'),
 (55,'STEP 03','VISIT THE','ACTUAL LAND'),
 (58,'STEP 04','INDEPENDENT','LEGAL REVIEW'),
 (59,'PAYMENT','RECORDS','MATTER'),
 (61,'READ EVERY','REFUND AND','CANCEL CLAUSE'),
 (62,'PRESSURE','TO BUY FAST?','CHECK AGAIN'),
 (64,'FAKE','INVESTMENT','WARNINGS'),
 (65,'A COMPANY ID','IS NOT A','PLOT NOC'),
 (67,'ALREADY','PURCHASED','A FILE?'),
 (68,'PRESERVE','ALL YOUR','DOCUMENTS'),
 (69,'REQUEST','A WRITTEN','RESPONSE'),
 (70,'SEEK','INDEPENDENT','LEGAL ADVICE'),
 (72,'MORE THAN','JUST AN','INVESTMENT'),
 (74,'DECIDE','WITH','EVIDENCE'),
 (76,'PAPER CANNOT','CREATE','LAND'),
 (78,'TRUST','MUST FOLLOW','THE FACTS'),
 (80,'VERIFY','THE LAND','BEFORE PAYING'),
 (81,'PAKISTAN','PROPERTY','GROUP'),
 (83,'THE FILE EXISTS','WHERE IS','THE LAND?')
]

def parse_srt():
 s=SRT.read_text(encoding='utf-8-sig');out={}
 for block in re.split(r'\n\s*\n',s):
  ls=block.strip().splitlines()
  if len(ls)<3 or '-->' not in ls[1]:continue
  def parse(st):
   h,m,ss=st.strip().replace(',','.').split(':');return int(h)*3600+int(m)*60+float(ss)
  a,b=ls[1].split('-->');out[int(ls[0])]=(parse(a),parse(b),' '.join(ls[2:]))
 return out
CUES=parse_srt();length=410.48
# Each clip starts on the exact source cue and avoids the following clip.
STORY=[]
for j,(cue,title,sub,base) in enumerate(SCENES):
 start=CUES[cue][0]
 nxt=CUES[SCENES[j+1][0]][0] if j+1<len(SCENES) else length
 duration=min(5.0,max(2.5,nxt-start-.35),length-start-.35)
 STORY.append(dict(i=j,subtitle_cue=cue,start=round(start,3),end=round(start+duration,3),duration=round(duration,3),title=title,second=sub,third=base,spoken=CUES[cue][2]))
(root:=ROOT/'storyboard.json').write_text(json.dumps(STORY,ensure_ascii=False,indent=2),encoding='utf-8')

rng=np.random.default_rng(1552)
# Frame grabs from original video are generic stock; do not pretend actual footage of suspects.
STILLS=ROOT/'stills';STILLS.mkdir(exist_ok=True)
DEF_PHOTOS=[ASSETS/'cc0_downloads'/'islamabad_panorama_cc0.jpg',ASSETS/'cc0_downloads'/'construction_crane_cc0.jpg',ASSETS/'cc0_downloads'/'crane_workers_cc0.jpg',ASSETS/'cc0_downloads'/'crane_night_cc0.jpg']
IMAGE_SOURCE=ASSETS/'reference_previous.png'

def cover(im,w,h):
 ratio=max(w/im.width,h/im.height); w2=max(w,math.ceil(im.width*ratio));h2=max(h,math.ceil(im.height*ratio))
 im=im.resize((w2,h2),Image.Resampling.LANCZOS);return im.crop(((w2-w)//2,(h2-h)//2,(w2+w)//2,(h2+h)//2))

def asset_still(i,sec):
 path=STILLS/f'{i:02}.jpg'
 if path.exists():return path
 p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{max(0,sec-2):.2f}','-i',str(SRC),'-frames:v','1','-q:v','3',str(path)],capture_output=True)
 if p.returncode or not path.exists():return DEF_PHOTOS[i%len(DEF_PHOTOS)]
 return path

def ftext(draw,xy,text,font,max_w,color,sz,stroke=0):
 # auto-fit headline without clipping; avoids abbreviated or cropped facts
 while sz>30:
  fonto=ImageFont.truetype(font,sz)
  bounds=draw.textbbox((0,0),text,font=fonto,stroke_width=stroke)
  if bounds[2]-bounds[0]<=max_w:break
  sz-=2
 draw.text(xy,text,font=fonto,fill=color,stroke_width=stroke)
 return sz

def generate_art(item):
 i=item['i'];out_dir=ART/f'{i:02}';out_dir.mkdir(exist_ok=True)
 if (out_dir/'ready').exists():return
 rr=random.Random(71206+i)
 base=cover(Image.open(ASSETS/'paper.png').convert('RGB'),W,H)
 # printed-grain archival noise + paper fold lines and perforation marks
 a=np.array(base,dtype=np.int16);noise=np.random.default_rng(i+10).normal(0,6,(H,W,1)).astype('int16')
 a=np.clip(a+noise,0,255).astype('uint8');base=Image.fromarray(a)
 dr=ImageDraw.Draw(base,'RGBA')
 for n in range(9):
  xx=rr.randint(0,W);yy=rr.randint(0,H)
  dr.line((xx,yy,xx+rr.randint(80,380), yy+rr.randint(-15,15)),fill=(56,49,37,rr.randint(9,25)),width=rr.randint(1,3))
 for x in range(0,W,83):dr.line((x,0,x,H),fill=(30,25,21,11),width=1)
 for y in range(0,H,83):dr.line((0,y,W,y),fill=(30,25,21,10),width=1)
 # 4 background treatments rotated through chapters, + original reference treatment on hero chapter
 motif=i%8
 bgphoto=asset_still(i,item['start']+1.0)
 try:photo=Image.open(bgphoto).convert('RGB')
 except:photo=Image.open(DEF_PHOTOS[i%len(DEF_PHOTOS)]).convert('RGB')
 if Path(bgphoto).parent==STILLS:
  photo=photo.crop((0,0,photo.width,round(photo.height*.72)))  # remove subtitle-burn region from stock still
 photo=ImageEnhance.Contrast(ImageOps.grayscale(photo).convert('RGB')).enhance(1.28)
 photo=cover(photo,760,545)
 # archival photo print is separate foreground piece with generous tactile paper border
 frame=Image.new('RGBA',(812,600),(251,244,225,255))
 frame.paste(photo,(26,24));pd=ImageDraw.Draw(frame,'RGBA')
 pd.rectangle((26,24,785,569),outline=(27,23,23,210),width=3)
 pd.rectangle((8,588,800,598),fill=(52,48,42,17))
 frame=frame.rotate([-3,2,-2,4][i%4],expand=True,resample=Image.Resampling.BICUBIC)
 frame.save(out_dir/'photo.png')
 # background archival paper with ghosted context photos in selected motifs
 if motif in (1,3,5):
  backing=ImageEnhance.Contrast(cover(photo,W,620)).enhance(.8)
  base.paste(backing,(0,460))
  overlay=Image.new('RGBA',(W,H),(246,233,209,0));od=ImageDraw.Draw(overlay,'RGBA');od.rectangle((0,450,W,H),fill=(242,229,202,118))
  base=Image.alpha_composite(base.convert('RGBA'),overlay).convert('RGB')
  dr=ImageDraw.Draw(base,'RGBA')
 else:dr=ImageDraw.Draw(base,'RGBA')
 if motif in (2,6):
  # conceptual cartographic grid, not actual land map
  for row in range(7):
   for col in range(11):
    x=120+col*140+(row%2)*20;y=240+row*84
    dr.rectangle((x,y,x+120,y+60),outline=(50,48,43,70),width=2)
    if (row*11+col+i)%7==0:dr.rectangle((x,y,x+120,y+60),fill=(225,191,96,46))
 dr.rectangle((100,69,630,142),fill=(248,194,21,255))
 dr.text((121,87),'PAKISTAN PROPERTY GROUP',font=ImageFont.truetype(COND,42),fill=BLACK)
 dr.text((1516,93),'REPORTED · MAY 2026',font=ImageFont.truetype(MONO,29),fill=BLACK)
 dr.line((109,166,1810,166),fill=(52,50,45,140),width=3)
 # motifs alternate headline left/right, photo right/left, newspaper timeline, map, dark-photo split
 photo_right=motif not in (1,3,6)
 title_x=105 if photo_right else 990
 # gradient not used; ripped paper strips with hand-generated irregular outlines
 if photo_right:
  dr.polygon([(86,218),(1101,212),(1090,865),(91,886)],fill=(251,245,225,205))
 else:dr.polygon([(950,218),(1870,206),(1830,865),(947,879)],fill=(251,245,225,205))
 # simulated document typography surrounding top and bottom of page
 stamp=ImageFont.truetype(MONO,21)
 for j in range(7):
  x=rr.choice([50,1300]);y=185+j*90
  dr.text((x,y),f'RECORD / {i:02d} / REF {j+1:03d}',font=stamp,fill=(78,69,57,48))
 base.save(out_dir/'background.jpg',quality=90,subsampling=0)
 # Primary title as separate alpha-animated paper layer
 title=Image.new('RGBA',(1130,710),(0,0,0,0));td=ImageDraw.Draw(title,'RGBA')
 # jagged mustard strip and underlaid newsprint broken lines
 coords=[(12,20),(1060,8),(1094,195),(9,213)]
 td.polygon(coords,fill=(249,197,25,245))
 td.line([(22,217),(1050,217)],fill=RED+(255,),width=12)
 num=item['title'] in ('42,000','6,000','36,000','42,000 FILES')
 ftext(td,(40,38),item['title'],FNT,1010,BLACK,190 if num else 111)
 td.polygon([(22,254),(1030,240),(1074,431),(23,455)],fill=(249,244,224,255))
 ftext(td,(40,284),item['second'],COND,975,RED if (i%3==0) else BLACK,105)
 td.polygon([(22,470),(1022,462),(1062,661),(21,669)],fill=(249,243,223,255))
 ftext(td,(40,492),item['third'],FNT,985,BLACK,111)
 td.line((38,654,995,654),fill=RED+(255,),width=11)
 title.save(out_dir/'title.png')
 # ink scribbles/underlines drawn in transparent layer; slide/fade/reveal in 60fps
 marks=Image.new('RGBA',(W,H),(0,0,0,0));md=ImageDraw.Draw(marks,'RGBA')
 arrow_start=(870,660) if photo_right else (1115,670)
 arrow_end=(1180,492) if photo_right else (790,465)
 steps=[]
 for n in range(41):
  t=n/40;x=arrow_start[0]+(arrow_end[0]-arrow_start[0])*t
  y=arrow_start[1]+(arrow_end[1]-arrow_start[1])*t-140*math.sin(math.pi*t)
  steps.append((x,y))
 md.line(steps,fill=RED+(235,),width=9,joint='curve')
 md.line([arrow_end,(arrow_end[0]-38 if photo_right else arrow_end[0]+38,arrow_end[1]-8)],fill=RED+(235,),width=9)
 md.line([arrow_end,(arrow_end[0]-8 if photo_right else arrow_end[0]+8,arrow_end[1]-37)],fill=RED+(235,),width=9)
 # red circles and double underline + tape bars at gallery edges
 md.arc((60,120,400,238),-10,170,fill=RED+(220,),width=8)
 md.line((125,960,1740,960),fill=RED+(220,),width=5)
 marks.save(out_dir/'marks.png')
 footer=Image.new('RGBA',(W,145),(0,0,0,0));fd=ImageDraw.Draw(footer,'RGBA')
 fd.polygon([(0,13),(W,7),(W,130),(0,142)],fill=(246,237,210,250))
 fd.rectangle((0,0,1920,10),fill=(33,30,24,122))
 fd.text((75,32),'ILLUSTRATIVE STOCK FOOTAGE · REPORTED ALLEGATIONS, NOT COURT FINDINGS',font=ImageFont.truetype(MONO,28),fill=BLACK)
 fd.text((1500,92),f'CASE STUDY  /  {i+1:02}/{len(STORY):02}',font=ImageFont.truetype(MONO,22),fill=(91,76,60))
 footer.save(out_dir/'footer.png')
 (out_dir/'ready').write_text('ok')

def over(f,img,x,y,alpha=1.0,scale=1):
 if alpha<.005:return
 if scale!=1:
  img=cv2.resize(img,(max(4,int(img.shape[1]*scale)),max(4,int(img.shape[0]*scale))),interpolation=cv2.INTER_LINEAR)
 h,w=img.shape[:2];x=round(x);y=round(y)
 lx=max(0,x);ly=max(0,y);rx=min(W,x+w);ry=min(H,y+h)
 if rx<=lx or ry<=ly:return
 sub=img[ly-y:ry-y,lx-x:rx-x];dest=f[ly:ry,lx:rx]
 af=(sub[:,:,3].astype('float32')/255*alpha)[:,:,None]
 dest[:]=(sub[:,:,:3]*af+dest*(1-af)).astype('uint8')

def smooth(v):v=np.clip(v,0,1);return v*v*(3-2*v)
def shot(item,threads=2):
 i=item['i'];dd=ART/f'{i:02}';output=CLIPS/f'shot_{i:02}.mp4'
 if output.exists() and output.stat().st_size>100000:return str(output)
 generate_art(item)
 bkg=cv2.imread(str(dd/'background.jpg'))
 photo=cv2.imread(str(dd/'photo.png'),cv2.IMREAD_UNCHANGED)
 title=cv2.imread(str(dd/'title.png'),cv2.IMREAD_UNCHANGED)
 mark=cv2.imread(str(dd/'marks.png'),cv2.IMREAD_UNCHANGED)
 footer=cv2.imread(str(dd/'footer.png'),cv2.IMREAD_UNCHANGED)
 if any(x is None for x in [bkg,photo,title,mark,footer]):raise Exception('missing visual layer '+str(i))
 dur=item['duration'];n=max(3,round(dur*FPS));photo_right=i%8 not in (1,3,6)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p','-g','120','-threads',str(threads),'-t',str(n/FPS),str(output)+'.partial.mp4']
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for z in range(n):
   t=z/FPS; u=t/max(.001,dur)
   # camera move independent of subject planes; vary position every frame
   f=bkg.copy()
   s=.8*math.sin(t*.73+i);pt=math.sin(t*1.05+i)
   px=(1070 if photo_right else 60)+18*math.sin(t*.8+i*.3)
   py=220+12*math.sin(t*1.4+i*.7)
   titlex=(65 if photo_right else 915) + 34*(1-smooth(t/.7))*(1 if photo_right else -1)
   titley=192+8*math.sin(t*.78+i*.6)
   photo_zoom=1+0.018*math.sin(t*.65+i)
   over(f,photo,px,py,alpha=smooth(t/.65),scale=photo_zoom)
   over(f,title,titlex,titley,alpha=smooth((t-.22)/.65),scale=1+(.02*(1-smooth(t/1.2))))
   # Framing marks are late-stage annotations, not unexplained motion
   over(f,mark,0,0,alpha=.85*smooth((t-1.7)/1.1))
   over(f,footer,0,935,alpha=smooth((t-1)/.65))
   # animated analog exposure texture at 60fps, not duplicated frames
   l=2.0*math.sin(t*2.2+i)+1.0*math.sin(t*3.7+i)
   if abs(l)>1.4:f=cv2.convertScaleAbs(f,alpha=1.0,beta=l)
   proc.stdin.write(f.tobytes())
  proc.stdin.close();code=proc.wait()
  if code:raise RuntimeError(proc.stderr.read().decode(errors='replace')[-600:])
  Path(str(output)+'.partial.mp4').replace(output)
 except Exception:
  proc.kill();proc.wait();raise
 return str(output)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int,default=len(STORY));p.add_argument('--threads',type=int,default=2);p.add_argument('--only-art',action='store_true')
 a=p.parse_args()
 for item in STORY[a.start:a.end]:
  t=time.time()
  if a.only_art:generate_art(item)
  else:shot(item,a.threads)
  print('EDITED',item['i']+1,'/',len(STORY),'cue',item['subtitle_cue'],'sec',item['start'],'elapsed',round(time.time()-t,1),flush=True)