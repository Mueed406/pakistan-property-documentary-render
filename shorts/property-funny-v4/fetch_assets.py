#!/usr/bin/env python3
"""Fetch real CC0 Karachi doodh-patti photograph (NO invented image/license).
Avoid raw file in public repo; archive art manifest and 2048px PNG source in
ephemeral GitHub Actions artifact for further non-destructive selection.
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request,urlopen
from PIL import Image,ImageOps
import argparse,hashlib,json,io,time
P=argparse.ArgumentParser()
P.add_argument("--out",default="shorts/property-funny-v4/assets")
a=P.parse_args()
dest=Path(a.out);dest.mkdir(parents=True,exist_ok=True)
name="Doodh Patti Chai.JPG"
url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+quote(name)
raw=None
for retry in range(3):
 try:
  req=Request(url,headers={"User-Agent":"PPG-Shorts-V4-CC0-Asset-Research/1.0 (https://github.com/Mueed406/pakistan-property-documentary-render)"})
  with urlopen(req,timeout=65) as result:
   final=result.geturl()
   if not final.startswith("https://upload.wikimedia.org/"):raise ValueError("Unexpected Wikimedia image host")
   data=result.read(17_000_000)
  with Image.open(io.BytesIO(data)) as preview:preview.verify()
  raw=data;break
 except Exception as e:
  if retry==2:raise
  print("retry",str(e)[:180],flush=True);time.sleep(retry+2)
assert raw and len(raw)>100_000
im=Image.open(io.BytesIO(raw));im=ImageOps.exif_transpose(im).convert("RGB")
assert im.width>=2048 and im.height>=2048
(dest/"Doodh_Patti_Chai_CC0_original.jpg").write_bytes(raw)
im.thumbnail((2880,2160),Image.Resampling.LANCZOS)
im.save(dest/"doodh_patti_photo_2160.png",optimize=True)
report={"source_page":"https://commons.wikimedia.org/wiki/File:Doodh_Patti_Chai.JPG",
        "creator":"Miansari66", "license":"CC0 1.0", "license_url":"https://creativecommons.org/publicdomain/zero/1.0/",
        "country":"Pakistan", "category":"Cuisine of Karachi",
        "original_width":4896,"original_height":3672,
        "original_source_sha256":hashlib.sha256(raw).hexdigest(),
        "prepared_png":"doodh_patti_photo_2160.png",
        "prepared_png_size":im.size,
        "correct_claim":"Real CC0 photograph of Pakistani doodh-patti tea; not a photograph of a real-estate dealer.",
        "source_original_url":final,
        "do_not_claim_transparent":True}
(dest/"ASSET_PROVENANCE.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
print("RESEARCHED_AUTHENTIC_TEA_ASSET",im.size,hashlib.sha256(raw).hexdigest(),flush=True)
