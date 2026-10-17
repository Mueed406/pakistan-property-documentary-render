#!/usr/bin/env python3
"""Build documentary collage source stills from an EXISTING licensed PPG film.
Never claim these extracted stock stills portray the actual accused society.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageEnhance,ImageFont
import argparse,subprocess,json
import numpy as np
parser=argparse.ArgumentParser()
parser.add_argument("--base",required=True,help="Local path to previously approved documentary MP4")
parser.add_argument("--out",default="editorial_collage/assets")
args=parser.parse_args()
root=Path(args.out);root.mkdir(parents=True,exist_ok=True)
sources={"islamabad":34.6,"sold_sign":42.0,"consultation":49.3,
         "paperwork":56.1,"filing":159.0,"development":325.0}
for name,second in sources.items():
 out=root/(name+".jpg")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(second),"-i",args.base,
   "-vf","crop=1920:770:0:0,scale=1500:600:flags=lanczos","-frames:v","1","-q:v","3",str(out)],check=True)
 im=Image.open(out).convert("RGB")
 im=ImageEnhance.Contrast(ImageOps.grayscale(im).convert("RGB")).enhance(1.13)
 im.save(out,quality=91,subsampling=0)
# Procedural, license-independent paper and halftone; no copied illustration.
rng=np.random.default_rng(20261017);h,w=800,1400
y,x=np.ogrid[:h,:w];noise=rng.normal(0,5,(h,w))
t=np.uint8(np.clip(243+noise-6*x/w-8*y/h,0,255))
Image.fromarray(np.stack([t,np.clip(t.astype("int16")-4,0,255).astype("uint8"),np.clip(t.astype("int16")-15,0,255).astype("uint8")],axis=2)).save(root/"paper.png")
im=Image.new("RGBA",(500,340),(0,0,0,0));d=ImageDraw.Draw(im)
for yy in range(5,340,11):
 for xx in range(5,500,11):
  r=1+(xx//11+yy//11)%3
  d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(30,31,30,38))
im.save(root/"halftone.png")
im=Image.new("RGBA",(720,610),(248,244,232,255));d=ImageDraw.Draw(im)
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fb="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
d.text((28,24),"PROPERTY RECORDS",font=ImageFont.truetype(fb,34),fill=(39,38,37))
d.line((26,76,685,76),fill=(44,43,41),width=3)
d.text((28,92),"AN EXPLAINER / ILLUSTRATIVE DOCUMENT",font=ImageFont.truetype(font,16),fill=(113,105,95))
for row in range(13):
 for col in range(2):
  xx=32+col*342;yy=145+row*31
  d.rounded_rectangle((xx,yy,xx+260-(row%5)*21+col*7,yy+6),2,fill=(80,79,75,125))
im.save(root/"newsprint.png")
(root/"ASSET_PROVENANCE.json").write_text(json.dumps({"assets":[{"file":n+".jpg","derived_from":"Existing PPG stock-film master","at_second":t,"usage":"Generic stock illustration, not case evidence"} for n,t in sources.items()], "original_procedural_assets":["paper.png","halftone.png","newsprint.png"],"publication_check":"Audit upstream stock licenses before publishing."},indent=2),encoding="utf-8")
print("Prepared nine image assets at",root)
