#!/usr/bin/env python3
"""Download an authorized CC0 architectural kit from Poly Haven's public asset API.

No scraped session / hidden tokens. Require a proper downloadable Blender file
and record source/provenance. Abort when unavailable rather than quietly
substituting a cheap model.
"""
import os, sys, json, hashlib, zipfile, tarfile
from pathlib import Path
from urllib.parse import urlparse
import requests

ROOT=Path(__file__).resolve().parent
DEST=ROOT/"cinematic_assets"
ASSET="modular_urban_apartments_facade"
API="https://api.polyhaven.com/files/"+ASSET
PAGE="https://polyhaven.com/a/"+ASSET
UA={"User-Agent":"PakistanPropertyGroup-Documentary/1.0 (CC0 footage visualization)"}
ALLOWED={"dl.polyhaven.org","cdn.polyhaven.com","polyhaven.com","api.polyhaven.com","download.polyhaven.com"}

def url_allowed(s):
 p=urlparse(s)
 return p.scheme=="https" and (p.hostname in ALLOWED or (p.hostname or "").endswith(".polyhaven.org"))

def candidates(tree,trail=()):
 found=[]
 if isinstance(tree,dict):
  if isinstance(tree.get("url"),str):
   name="/".join(str(x) for x in trail).lower()
   u=tree["url"]
   if url_allowed(u):
    ext=(".blend" if ".blend" in name else ".zip" if ".zip" in name else "")
    prefer=0
    if ("blend" in name or "blender" in name):prefer+=100
    if any(x in name for x in ("1k","2k","low","4k")):prefer+=12
    if "8k" in name:prefer-=24
    found.append((prefer,u,name,tree))
  for k,v in tree.items():
   found.extend(candidates(v,trail+(str(k),)))
 elif isinstance(tree,list):
  for i,v in enumerate(tree): found.extend(candidates(v,trail+(str(i),)))
 return found

def download(url, dest, max_bytes=270_000_000):
 print("Downloading licensed asset:",url.split("?")[0],flush=True)
 with requests.get(url,headers=UA,stream=True,timeout=(30,180),allow_redirects=True) as r:
  r.raise_for_status()
  if not url_allowed(r.url):raise RuntimeError("Unexpected asset CDN redirect")
  length=int(r.headers.get("Content-Length") or 0)
  if length>max_bytes:raise RuntimeError("CC0 archive over permitted size")
  size=0;sha=hashlib.sha256()
  with dest.open("wb") as f:
   for block in r.iter_content(1<<19):
    if not block:continue
    size+=len(block)
    if size>max_bytes:raise RuntimeError("Asset over limit")
    f.write(block);sha.update(block)
 return {"size":size,"sha256":sha.hexdigest(),"url":r.url.split("?")[0]}

def safe_extract(src,where):
 files=[]
 if zipfile.is_zipfile(src):
  with zipfile.ZipFile(src) as z:
   for m in z.infolist():
    name=Path(m.filename)
    if name.is_absolute() or ".." in name.parts:continue
    if m.file_size>350_000_000:raise RuntimeError("Unsafe extracted file size")
    if m.is_dir():continue
    p=where.joinpath(*name.parts)
    p.parent.mkdir(parents=True,exist_ok=True)
    with z.open(m) as f,p.open("wb") as out:
     import shutil
     shutil.copyfileobj(f,out)
    files.append(str(p))
 else:
  if src.suffix==".blend":
   p=where/src.name;src.replace(p);files.append(str(p))
  else: raise RuntimeError("Asset download was not a supported BLEND or ZIP package")
 return files

def main():
 DEST.mkdir(exist_ok=True,parents=True)
 r=requests.get(API,headers=UA,timeout=(15,60));r.raise_for_status()
 data=r.json()
 choices=candidates(data)
 print("Poly Haven permitted URL candidate types:",[(x[0],x[2]) for x in choices[:12]],flush=True)
 choices=[x for x in choices if "blend" in x[2] or "blender" in x[2]]
 if not choices:raise SystemExit("No Blender file in CC0 API manifest; manual license review needed.")
 choices.sort(key=lambda c:(c[0],"-8k" not in c[2]),reverse=True)
 info=None; files=[]
 for score,url,name,meta in choices:
  try:
   file=DEST/("source"+(".zip" if ".zip" in name else ".blend"))
   info=download(url,file)
   files=safe_extract(file,DEST)
   break
  except Exception as e:
   print("Try next official asset variant:",str(e)[:120],flush=True)
 if not files:raise SystemExit("No licensed CC0 Blender asset could be downloaded.")
 blends=[Path(x) for x in files if x.lower().endswith(".blend")]
 if not blends:raise SystemExit("Asset downloaded, but does not contain a usable .blend file.")
 out={"provider":"Poly Haven","asset":ASSET,"source_page":PAGE,"license":"CC0",
      "file":str(sorted(blends,key=lambda p:p.stat().st_size,reverse=True)[0].resolve()),"download":info,
      "all_blend_files":[str(x) for x in blends]}
 (DEST/"asset_provenance.json").write_text(json.dumps(out,indent=2),encoding="utf8")
 print("READY LICENSED 3D ASSET",out["file"],flush=True)

if __name__=="__main__":main()
