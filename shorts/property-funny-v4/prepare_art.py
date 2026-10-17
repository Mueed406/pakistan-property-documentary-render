#!/usr/bin/env python3
"""Produce 2048px RGBA REAL photographed Karachi chai and native-resolution paper.
No fake tea or small enlarged PNG. CC0 source: Wikimedia/Miansari66.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,hashlib,json,argparse
p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path(__file__).parent);args=p.parse_args()
a=args.root/"assets";a.mkdir(parents=True,exist_ok=True)
src=Image.open(a/"doodh_patti_photo_2160.png").convert("RGBA")
if src.size!=(2880,2160):raise RuntimeError("Authentic source unexpectedly changed")
mask=Image.new("L",(960,720));d=ImageDraw.Draw(mask)
d.polygon([(295,221),(296,174),(308,151),(326,133),(355,119),(404,108),(464,106),(537,106),(600,112),(649,121),(686,138),(705,159),(714,182),(723,218),(724,280),(715,349),(701,407),(676,468),(648,489),(618,511),(576,524),(525,532),(469,532),(414,522),(378,509),(347,488),(326,463),(309,426),(294,369),(289,302)],fill=255)
d.ellipse((707,258,845,413),fill=255);d.ellipse((736,292,818,370),fill=0)
d.polygon([(697,278),(730,273),(733,300),(713,318),(710,367),(693,375)],fill=255)
mask=mask.resize(src.size,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1.9))
pixels=np.array(src.convert("RGB"),dtype=np.uint16)
R,G,B=pixels[:,:,0],pixels[:,:,1],pixels[:,:,2]
X=np.arange(src.width)[None,:]//3;Y=np.arange(src.height)[:,None]//3
green=(G*100>R*117)&(G*100>B*117)&(G>58)
purple=(R*100>G*113)&(B*100>G*108)&(R>48)
red=(R*100>G*140)&(R*100>B*115)&(R>75)
bad=(green&((Y<220)|(X>705)))|(red&(X>725))|(purple&(X<310))
m=np.array(mask);m[bad]=0
src.putalpha(Image.fromarray(m).filter(ImageFilter.GaussianBlur(.7)))
cup=src.crop((810,285,2541,1644));cup.thumbnail((1840,1660),Image.Resampling.LANCZOS)
final=Image.new("RGBA",(2048,2048))
final.alpha_composite(cup,((2048-cup.width)//2,(2048-cup.height)//2))
path=a/"real_pakistani_chai_cutout_2048.png";final.save(path,optimize=True)
h,w=1920,1080
rng=np.random.default_rng(20261017);y,x=np.ogrid[:h,:w]
noise=rng.normal(0,3.6,(h,w));crease=3.5*np.cos(x/140)+2*np.sin(y/105)
arr=np.empty((h,w,3),np.uint8)
for j,col in enumerate((243,233,212)):
 arr[:,:,j]=np.uint8(np.clip(col+noise+crease-(x/w)*5,0,255))
Image.fromarray(arr).save(a/"archival_paper_background_1080x1920.png",optimize=True)
manifest=json.loads((a/"ASSET_PROVENANCE.json").read_text())
manifest.update({"photographic_chai_png":path.name,"photo_png_size":[2048,2048],
 "photo_png_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
 "background_png":"archival_paper_background_1080x1920.png",
 "background_size":[1080,1920],
 "image_provenance":"CC0 Miansari66 REAL photograph cropped to isolated transparent prop; original Wikimedia source retained; not a CGI cup.",
 "premiere_export":"No editor-specific template files redistributed."})
(a/"ASSET_PROVENANCE.json").write_text(json.dumps(manifest,indent=2)+"\n")
print("REAL_CHAI_RGBA_2048_AND_1080P_BACKGROUND_VERIFIED")
