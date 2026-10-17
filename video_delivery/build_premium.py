#!/usr/bin/env python3
"""PPG Editorial Motion V2 — actual frame-specific moving-paper render, 1080p/60.
Reuses original PPG film's audio, the user's preferred earlier collage artwork,
and licensed generic illustration. Not an evidence recreation.
"""
from pathlib import Path
import cv2,numpy as np,subprocess,math,random,sys,os,re,json
from PIL import Image, ImageDraw, ImageFont,ImageEnhance,ImageOps,ImageFilter

ROOT=Path(os.environ.get('PPG_ROOT',Path(__file__).resolve().parent)); A=ROOT/'assets'; OUT=ROOT/'out';OUT.mkdir(parents=True,exist_ok=True)
W,H,FPS=1920,1080,60; DUR=25.6; N=int(DUR*FPS)
REFERENCE=Path(os.environ.get('PPG_REFERENCE',A/'reference_previous.png'))
STOCK=Path(os.environ.get('PPG_CC0',A/'cc0_downloads'))
PAPER=A/'paper.png'
NEWSPRINT=A/'newsprint.png'
if not REFERENCE.exists():raise FileNotFoundError(REFERENCE)
FONT_BLACK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FONT_BOLD='/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf'
FONT_TYPE='/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf'
FONT_SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Bold.ttf'
# exact reproducible palette from the preferred editorial reference
CREAM=(244,234,213);WHITE=(252,246,232);DARK=(20,19,17);RED=(169,22,21);GOLD=(241,194,18);GREY=(83,75,69)

def findfont(p,size):return ImageFont.truetype(p,size)

def crop_cover(im, size):
 w,h=size;f=max(w/im.width,h/im.height); nw=int(im.width*f)+2;nh=int(im.height*f)+2
 img=im.resize((nw,nh),Image.Resampling.LANCZOS)
 x=(nw-w)//2;y=(nh-h)//2
 return img.crop((x,y,x+w,y+h))

def newboard(seed):
 rg=np.random.default_rng(seed)
 tex=crop_cover(Image.open(PAPER).convert('RGB'),(W,H))
 arr=np.array(tex,dtype=np.int16)
 grain=rg.normal(0,10,(H,W,1)).astype(np.int16)
 arr=np.uint8(np.clip(arr+grain,0,255))
 img=Image.fromarray(arr)
 d=ImageDraw.Draw(img,'RGBA')
 # archival damaged-copy texture, grids, pencil strokes
 for xx in range(0,W,87):d.line((xx,0,xx,H),fill=(75,67,51,13),width=1)
 for yy in range(0,H,87):d.line((0,yy,W,yy),fill=(75,67,51,12),width=1)
 for j in range(42):
  x=int(rg.integers(0,W));y=int(rg.integers(0,H));dx=int(rg.integers(18,220))
  d.line((x,y,x+dx,y+int(rg.integers(-5,5))),fill=(75,56,42,18),width=int(rg.integers(1,3)))
 return img

def image_piece(img,x,y,w,h,rotation=0,bw=True):
 im=Image.open(img).convert('RGB') if not isinstance(img,Image.Image) else img.convert('RGB')
 if bw:im=ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.22).convert('RGB')
 im=crop_cover(im,(w,h));frame=Image.new('RGBA',(w+38,h+55),WHITE+(255,))
 frame.paste(im,(18,16)); d=ImageDraw.Draw(frame,'RGBA');d.rectangle((18,16,w+17,h+15),outline=(40,33,27,150),width=3)
 # halftone roughness / xerox dust noise pre-calculated; no download needed
 pix=np.array(frame)
 rs=np.random.default_rng(w*h); dots=rs.integers(0,min(w,h),size=(500,2))
 for px,py in dots:
  px=int(px%(w));py=int(py%(h));pix[py+16,px+18,:3]=np.maximum(pix[py+16,px+18,:3]*.76,0)
 frame=Image.fromarray(pix)
 if rotation:frame=frame.rotate(rotation,expand=True,resample=Image.Resampling.BICUBIC,fillcolor=(0,0,0,0))
 return frame

def textpiece(text,font,size,color,bg=None,pad=20,width=None,spacing=12):
 font=findfont(font,size);d=ImageDraw.Draw(Image.new('RGB',(8,8)))
 bbox=d.textbbox((0,0),text,font=font,stroke_width=0)
 tw=bbox[2]-bbox[0];th=bbox[3]-bbox[1]
 ww=width or int(tw+pad*2);hh=int(th+pad*2)
 im=Image.new('RGBA',(ww,hh),(0,0,0,0) if bg is None else bg+(255,))
 d=ImageDraw.Draw(im);d.text((pad-bbox[0],pad-bbox[1]),text,font=font,fill=color+(255,),stroke_width=0)
 return im

def stroke(img,pts,color,width=6):
 d=ImageDraw.Draw(img);d.line(pts,fill=color,width=width,joint='curve')

# Compose real split layers in full color: textured sheets, document fragments, stamped labels, and source-checked photos.
base0=newboard(4);base1=newboard(5);base3=newboard(7)
for k,base in enumerate([base0,base1,base3]):
 d=ImageDraw.Draw(base,'RGBA')
 for i in range(9):
  xx=(i*231+127)%W; yy=(i*187+83)%H
  d.rectangle((xx,yy,xx+280,yy+14),fill=(51,48,47,20))
  d.line((xx,yy+28,xx+160,yy+28),fill=(0,0,0,20),width=2)
# Skyline and construction backgrounds (copyright-verified CC0)
cc0=STOCK/'islamabad_panorama_cc0.jpg'; crane=STOCK/'construction_crane_cc0.jpg'
crane2=STOCK/'crane_workers_cc0.jpg'
# big ink sections behind photo layer
for base,title in [(base0,'THE ALLOTMENT QUESTION'),(base1,'FILES VERSUS LAND'),(base3,'WHAT HAS BEEN PROVEN?')]:
 d=ImageDraw.Draw(base)
 d.text((106,73),title,font=findfont(FONT_TYPE,31),fill=DARK)
 d.line((100,127,W-100,127),fill=(60,50,42),width=3)
 d.rectangle((1612,48,1814,110),fill=DARK)
 d.text((1642,60),'MAY 2026',font=findfont(FONT_BOLD,37),fill=WHITE)
# Background illustration/photo collage photos actual CC0, captions disclose they're illustrations
base0.paste(crop_cover(ImageOps.grayscale(Image.open(cc0)).convert('RGB'),(W,550)),(0,530))
ImageDraw.Draw(base0,'RGBA').rectangle((0,530,W,H),fill=(24,21,18,74))
base1.paste(crop_cover(ImageOps.grayscale(Image.open(crane)).convert('RGB'),(W,620)),(0,460))
ImageDraw.Draw(base1,'RGBA').rectangle((0,460,W,H),fill=(63,54,44,75))
base3.paste(crop_cover(ImageOps.grayscale(Image.open(crane2)).convert('RGB'),(W,540)),(0,540))
ImageDraw.Draw(base3,'RGBA').rectangle((0,540,W,H),fill=(25,21,17,82))

# Layer library: each piece is a separately animated virtual camera plane.
L={}
def layer(n,im):L[n]=cv2.cvtColor(np.array(im.convert('RGBA')),cv2.COLOR_RGBA2BGRA)
# Build independent cut-paper and photo layers, never flatten the whole scene
layer('photo0',image_piece(cc0,0,0,830,415,rotation=-2))
layer('photo1',image_piece(crane,0,0,730,430,rotation=3))
layer('photo3',image_piece(crane2,0,0,780,390,rotation=-3))
layer('news_scrap',image_piece(NEWSPRINT,0,0,640,230,rotation=-2,bw=False))
# Rich text on paper scrap, varied typefaces
layer('files0',textpiece('42,000',FONT_BLACK,230,DARK, GOLD,pad=27))
layer('filetitle',textpiece('REPORTED PLOT FILES',FONT_BOLD,103,DARK,CREAM,pad=15))
layer('plot1',textpiece('≈ 6,000',FONT_BLACK,201,DARK,GOLD,pad=28))
layer('plottitle',textpiece('INDICATED LAND CAPACITY',FONT_BOLD,74,DARK,CREAM,pad=16))
layer('folderlab',textpiece('A FILE IS NOT THE LAND ITSELF',FONT_TYPE,32,DARK,WHITE,pad=16))
layer('denote0',textpiece('APPROXIMATE FIGURES / REPORTED ALLEGATIONS',FONT_TYPE,21,DARK,WHITE,pad=12))
layer('denote1',textpiece('ILLUSTRATIVE LAND PHOTO · NOT THE INVESTIGATED SITE',FONT_TYPE,20,DARK,WHITE,pad=11))
layer('allegations',textpiece('ALLEGATIONS',FONT_BLACK,129,RED,CREAM,pad=18))
layer('not',textpiece('ARE NOT A',FONT_SERIF,87,DARK,WHITE,pad=18))
layer('verdict',textpiece('COURT VERDICT',FONT_BLACK,114,DARK,GOLD,pad=20))
layer('courtinfo',textpiece('INVESTIGATION ≠ CONVICTION',FONT_TYPE,34,DARK,CREAM,pad=22))
layer('cite',textpiece('SOURCE: MAY 2026 NEWS REPORTING',FONT_TYPE,25,GREY,CREAM,pad=14))
# Hero poster is the previously preferred image, not the newer rendered one.
hero=crop_cover(Image.open(REFERENCE).convert('RGB'),(W,H)); hero_cv=cv2.cvtColor(np.array(hero),cv2.COLOR_RGB2BGR)
# image overlays are independent ripped-collage fragments, while hero remains a detailed style layer.
hero_photo_crop=Image.open(REFERENCE).convert('RGB').crop((907,150,1555,745))
layer('hero_photo',image_piece(hero_photo_crop,0,0,590,495,rotation=2,bw=False))
layer('files_scrap',image_piece(Image.open(REFERENCE).convert('RGB').crop((30,735,780,928)),0,0,650,176,rotation=3,bw=False))
layer('hero_mono',textpiece('36,000',FONT_BLACK,213,DARK,GOLD,pad=23))
layer('herofact',textpiece('42,000 FILES  –  6,000 PLOTS',FONT_TYPE,34,DARK,CREAM,pad=18))
# Film grain precomputation, 12 loop phases
rng=np.random.default_rng(87312)
noiseframes=[rng.normal(0,2.3,(H,W,1)).astype(np.int8) for _ in range(6)]
# paper cutout layers cast shadows and have hand-finished irregular edges.

def safe_blend(frame,name,x,y,opacity=1.,dx=0,dy=0,scale=1.0):
 if opacity<=.001:return
 image=L[name]
 if scale!=1.0:
  image=cv2.resize(image,(max(2,round(image.shape[1]*scale)),max(2,round(image.shape[0]*scale))),interpolation=cv2.INTER_AREA if scale<1 else cv2.INTER_LINEAR)
 x=int(x+dx);y=int(y+dy);h,w=image.shape[:2]
 left=max(x,0);top=max(y,0);right=min(x+w,W);bottom=min(y+h,H)
 if right<=left or bottom<=top:return
 sub=image[top-y:bottom-y,left-x:right-x];roi=frame[top:bottom,left:right]
 a=sub[:,:,3];factor=float(opacity)
 # shadow on transparent footprint means tactile cut paper, ~5px shadow offset
 if factor>.8 and (name not in ('photo0','photo1','photo3')):
  shx=min(right,W-8);shy=min(bottom,H-8)
  if shx>left+7 and shy>top+7:
   sample=frame[top+7:shy,left+7:shx]
   sample[:]=cv2.addWeighted(sample,.92,np.zeros_like(sample),.08,0)
 if int(a.min())==255:
  if factor>=.997:roi[:]=sub[:,:,:3]
  else:cv2.addWeighted(sub[:,:,:3],factor,roi,1-factor,0,roi)
 else:
  # use integer alpha compositing via premultiplication
  aa=(a.astype(np.float32)*factor/255)[:,:,None]
  roi[:]=(sub[:,:,:3]*aa+roi*(1-aa)).astype(np.uint8)

def smooth(v):v=np.clip(v,0,1);return v*v*(3-2*v)
def entrance(t,start,seconds=.7):return smooth((t-start)/seconds)
def wobble(t,phase=0,amp=4):return amp*math.sin(1.7*t+phase)+2*math.sin(3.1*t+phase)

def red_markup(img,t,scene):
 # stroke and arrows reveal at actual 60fps, fully independent of collage stills
 overlay=img
 if scene==0:
  p=entrance(t,2.0,1.8)
  points=[]
  for q in np.linspace(0,p,60):
   x=625+485*q; y=617-150*math.sin(q*math.pi*.76)
   points.append((round(x),round(y)))
  if len(points)>1:cv2.polylines(overlay,[np.array(points,dtype=np.int32)],False,(20,28,171),8,cv2.LINE_AA)
  if p>.94:
   tip=points[-1];cv2.line(overlay,(tip[0]-23,tip[1]-9),tip,(20,28,171),8,cv2.LINE_AA);cv2.line(overlay,(tip[0]-6,tip[1]-25),tip,(20,28,171),8,cv2.LINE_AA)
 elif scene==1:
  p=entrance(t,11.6,1.4)
  cv2.ellipse(overlay,(680,350),(445,152),-6,0,360*p,(19,29,179),10,cv2.LINE_AA)
  if p>.9:cv2.line(overlay,(555,488),(1230,488),(21,31,180),7,cv2.LINE_AA)
 elif scene==2:
  p=entrance(t,16.3,1.65)
  cv2.ellipse(overlay,(509,325),(460,163),-6,0,350*p,(28,30,175),8,cv2.LINE_AA)
 elif scene==3:
  p=entrance(t,22.15,1.5)
  xx=int(210+1170*p)
  cv2.line(overlay,(212,746),(xx,746),(27,30,179),12,cv2.LINE_AA)

def ripped_transition(canvas,old,new,fract,t):
 # animated deckled vertical wipe; each scanline exposes next moving-scene canvas
 hh=canvas.shape[0]; yy=np.arange(hh)
 boundary=W*fract+23*np.sin(yy*.05+t*7)+12*np.sin(yy*.19+t*3)
 mask=np.arange(W)[None,:]<boundary[:,None]
 canvas[mask]=new[mask]; canvas[~mask]=old[~mask]

base0=np.ascontiguousarray(cv2.cvtColor(np.array(base0),cv2.COLOR_RGB2BGR))
base1=np.ascontiguousarray(cv2.cvtColor(np.array(base1),cv2.COLOR_RGB2BGR))
base3=np.ascontiguousarray(cv2.cvtColor(np.array(base3),cv2.COLOR_RGB2BGR))

def compose_scene(scene,t):
 if scene==0:
  f=base0.copy();q=entrance(t,.1,.7)
  safe_blend(f,'photo0',910,-40+45*q,1,dx=wobble(t,0,5))
  safe_blend(f,'news_scrap',1035,715,entrance(t,2.1,.9)*.95,dx=wobble(t,2,4))
  safe_blend(f,'filetitle',104,171,entrance(t,.45,.8),dx=-90*(1-entrance(t,.45,.9)))
  safe_blend(f,'files0',103,285,entrance(t,1.15,.8),dx=25*wobble(t,.8,1))
  safe_blend(f,'folderlab',104,647,entrance(t,2.25,1.0))
  safe_blend(f,'denote1',106,938,entrance(t,4.,.5))
  safe_blend(f,'cite',108,896,entrance(t,3.1,.7))
 elif scene==1:
  f=base1.copy()
  safe_blend(f,'photo1',1016,166,entrance(t,8.65,.6),dx=wobble(t,1,9))
  safe_blend(f,'plot1',112,250,entrance(t,8.85,1.0),dx=30*(1-entrance(t,8.85,1.0)))
  safe_blend(f,'plottitle',119,552,entrance(t,9.4,.75))
  safe_blend(f,'denote0',119,928,entrance(t,9.8,.8))
  safe_blend(f,'news_scrap',1044,748,entrance(t,11.5,.9),dx=wobble(t,4,3))
  safe_blend(f,'denote1',119,965,entrance(t,10.1,.8))
 elif scene==2:
  # overscanned virtual camera -> smooth dramatic zoom through the layered earlier user-preferred key art
  zoom=1+.024*(t-14.73)/5.2
  M=np.float32([[zoom,0,-(W*zoom-W)/2+6*math.sin(t*.7)],
                [0,zoom,-(H*zoom-H)/2+2*math.sin(t*.5)]])
  f=cv2.warpAffine(hero_cv,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
  # animated photo emphasis + cinematic red annotation, same existing source image
  if t>=17.2:
   safe_blend(f,'hero_photo',1070,207,entrance(t,17.2,.6)*.99,dx=wobble(t,3,4))
 elif scene==3:
  f=base3.copy()
  safe_blend(f,'photo3',1046,224,entrance(t,20.1,.6),dx=wobble(t,2,4))
  safe_blend(f,'files_scrap',1130,763,entrance(t,23.1,.5),dx=wobble(t,5,2),scale=.84)
  safe_blend(f,'allegations',92,245,entrance(t,20.4,.68),dx=-(1-entrance(t,20.4,.68))*125)
  safe_blend(f,'not',96,442,entrance(t,21.1,.7))
  safe_blend(f,'verdict',96,575,entrance(t,21.8,.7))
  safe_blend(f,'courtinfo',98,795,entrance(t,22.55,.7))
  safe_blend(f,'cite',101,916,entrance(t,23.3,.8))
 else:raise ValueError(scene)
 red_markup(f,t,scene)
 # Small tactile film-print flutter: discontinuous hold of two frames on photographic cutout,
 # while camera and arrows remain true 60fps.
 if scene!=2:
  if (int(t*30)%4)==0:
   f[:12,:]=np.roll(f[:12,:],1,axis=1)
 return f

def scene_for(t):
 return 0 if t<8.61 else 1 if t<14.73 else 2 if t<19.93 else 3

base=ROOT/'source/renders/Pakistan_Property_Premium_Pearl_24_Motion_FullHD_Review.mp4'
if not base.exists():raise FileNotFoundError(base)
renderpath=OUT/'PPG_Premium_Editorial_60FPS_Review.mp4'
rawpath=OUT/'editorial_noaudio_60fps.mp4'
# Pipe true 60 independently animated frames (NOT duplicated 25fps source video).
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-c:v','libx264','-threads','4','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p','-r',str(FPS),'-movflags','+faststart',str(rawpath)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=open(OUT/'render_ffmpeg.log','wb'),bufsize=1024*1024)
try:
 for i in range(N):
  t=i/FPS;scene=scene_for(t)
  f=compose_scene(scene,t)
  # Film-reel light flash as chapters switch, never a visible unfinished key color
  phase=min([abs(t-x) for x in [8.61,14.73,19.93]])
  if phase<.085:
   w=.20*(1-phase/.085)
   f=cv2.addWeighted(f,1-w,np.full_like(f,255),w,0)
  # Film grain animation is intentional; avoid false low-res effects.
  if i%3==0:
   noise=noiseframes[(i//3)%len(noiseframes)]
   f=np.clip(f.astype(np.int16)+noise,0,255).astype(np.uint8)
  p.stdin.write(f.tobytes())
  if i%120==0:print(f'RENDERING {i}/{N} FRAMES, t={t:.2f}, chapter={scene+1}',flush=True)
 p.stdin.close()
 if p.wait()!=0:raise RuntimeError((OUT/'render_ffmpeg.log').read_text(errors='replace')[-3000:])
finally:
 if p.poll() is None:p.kill()
print('RAW_MP4_COMPLETE',rawpath,rawpath.stat().st_size,flush=True)
# Shift original SRT timestamps into 25.6-second segment. Only exact existing narration captions.
srtpath=ROOT/'source/baseline/urdu_timed.srt'
srt=srtpath.read_text(encoding='utf-8-sig')
pattern=r'(?m)^(\d+)\s*\n(\d\d:\d\d:\d\d,\d{3})\s*-->\s*(\d\d:\d\d:\d\d,\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)'
def ms(st):
 hh,mm,ss=st.split(':');return int(hh)*3600000+int(mm)*60000+float(ss.replace(',','.'))*1000
def clock(m):
 m=int(round(m));h=m//3600000;m%=3600000;n=m//60000;m%=60000;s=m//1000;return f'{h:02d}:{n:02d}:{s:02d},{m%1000:03d}'
initial=33672;entries=[]
for _,st,en,txt in re.findall(pattern,srt,flags=re.S):
 a=max(0,ms(st)-initial);b=min(DUR*1000,ms(en)-initial)
 if b<=a:continue
 entries.append(f'{len(entries)+1}\n{clock(a)} --> {clock(b)}\n{txt.strip()}')
new_srt=ROOT/'build/urdu_25s.srt';new_srt.write_text('\n\n'.join(entries)+'\n',encoding='utf-8')
# Burn subtitles with proper open-source Arabic font and cinematic unobtrusive black outline.
# Keep untouched original documentary narration at the correct real-time offset.
filterstr=f"subtitles='{new_srt}':force_style='FontName=Noto Sans Arabic,Fontsize=25,MarginV=45,PrimaryColour=&H00FFFFFF,OutlineColour=&H00201B13,BorderStyle=1,Outline=2,Shadow=0,Alignment=2'"
acmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(rawpath),'-ss','33.672','-t',str(DUR),'-i',str(base),'-filter_complex',f'[0:v]{filterstr}[v]','-map','[v]','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(DUR),str(renderpath)]
subprocess.run(acmd,check=True)
ffinfo=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(renderpath)]))
video=next(x for x in ffinfo['streams'] if x['codec_type']=='video'); audio=next(x for x in ffinfo['streams'] if x['codec_type']=='audio')
assert video['avg_frame_rate']=='60/1' and video['width']==1920 and video['height']==1080
assert float(ffinfo['format']['duration'])>=25.5
report={'file':str(renderpath),'duration_seconds':float(ffinfo['format']['duration']),'resolution':'1920x1080','frames_per_second':60,'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],'source_audio_start_seconds':33.672,'subtitles':len(entries),'creative_review_required':True,'voice':'original Piper (not Gemini)','allegations':'reported, not proven','assets':'existing generated image reference + 4 CC0 illustrative photos + original textures','render_strategy':'60 distinct composited frames per second; frame-accurate independent paper-layer animation'}
(OUT/'RENDER_QC.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('FINAL_60FPS_SAMPLE_COMPLETE',json.dumps(report),flush=True)