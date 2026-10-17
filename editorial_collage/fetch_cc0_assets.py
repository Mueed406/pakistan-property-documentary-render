#!/usr/bin/env python3
"""Acquire reviewed CC0 illustrative stills with recorded provenance.
Photos are generic visual context, never case evidence.
"""
from pathlib import Path
import urllib.request, urllib.parse, hashlib, json, time
from PIL import Image

SOURCES = [
 ("islamabad_panorama_cc0.jpg","View of Islamabad.JPG",
  "https://commons.wikimedia.org/wiki/File:View_of_Islamabad.JPG","Fraz.khalid1"),
 ("construction_crane_cc0.jpg","Boom lift crane on construction site.jpg",
  "https://commons.wikimedia.org/wiki/File:Boom_lift_crane_on_construction_site.jpg","CaptainHisDudeness"),
 ("crane_night_cc0.jpg","Construction crane below night sky.jpg",
  "https://commons.wikimedia.org/wiki/File:Construction_crane_below_night_sky.jpg","Wikimedia Commons CC0"),
 ("crane_workers_cc0.jpg","Building construction, worker receives material from crane.jpg",
  "https://commons.wikimedia.org/wiki/File:Building_construction,_worker_receives_material_from_crane.jpg","Wikimedia Commons CC0")
]

def fetch(directory):
 directory.mkdir(parents=True,exist_ok=True)
 assets=[];failures=[]
 for name,filename,page,author in SOURCES:
  url="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(filename)
  try:
   error=None
   for attempt in range(3):
    try:
     req=urllib.request.Request(url,headers={"User-Agent":"PPG-Documentary-CC0-Fetcher/1.0 (+https://github.com/Mueed406/pakistan-property-documentary-render)"})
     with urllib.request.urlopen(req,timeout=45) as resp:
      final=resp.geturl()
      if not final.startswith("https://upload.wikimedia.org/"): raise RuntimeError("Unexpected host "+final)
      raw=resp.read(18_000_000)
     if not raw.startswith((b"\xff\xd8\xff",b"\x89PNG\r\n\x1a\n")): raise RuntimeError("Unexpected image type")
     temp=directory/(name+".temporary");temp.write_bytes(raw)
     with Image.open(temp) as image:image.verify()
     temp.replace(directory/name)
     assets.append({"name":name,"author":author,"source_page":page,"source_original":final,"license":"CC0 1.0","sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"usage":"Generic stock illustration, NOT actual investigated society"})
     print("OK",name,len(raw),flush=True)
     error=None;break
    except Exception as exc:
     error=str(exc);time.sleep(attempt+1)
   if error:raise RuntimeError(error)
  except Exception as exc:
   print("FAILED",name,str(exc),flush=True)
   failures.append({"name":name,"error":str(exc)})
 (directory/"CC0_LICENSE_MANIFEST.json").write_text(json.dumps({"assets":assets,"failures":failures},indent=2),encoding="utf-8")
 if not assets:raise RuntimeError("No CC0 assets obtained")
 print("Finished CC0 asset archive:",len(assets),"images;",len(failures),"failures")

if __name__=="__main__":
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument("--out",type=Path,default=Path("editorial_collage/cc0_downloads"))
 fetch(parser.parse_args().out)
