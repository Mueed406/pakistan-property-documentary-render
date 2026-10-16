#!/usr/bin/env python3
"""Composite actual rendered Blender motion scenes over real stock-film footage.

Uses speech-cue matches: file discrepancy -> 3D parcel map;
building / approved layout -> architectural reveal;
investigative records -> 3D physical evidence dossier.

The 3D picture appears in a big animated picture-in-picture over moving stock,
preserving both documentary realism and visual explanation (not static cards).
Run against a NEW review copy; do not overwrite the base render.
"""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SCENES=["01_cinematic_parcel_map","02_architecture_construction","03_evidence_document_desk"]

def run(c):
 print("RUN:",c[0],c[-1],flush=True)
 subprocess.run(c,check=True)

def cue(segments,words,fallback,target_length):
 for item in segments:
  if any(w in item["text"] for w in words):
   return max(3.,min(target_length-7.,float(item["start"])))
 return target_length*fallback

def seconds(file):
 data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-of","json",str(file)]))
 return float(data["format"]["duration"])

def compose(source,clips,cues,out):
 duration=seconds(source)
 matched=[
  cue(cues,["بیالیس ہزار","چھتیس ہزار","گنجائش"],.18,duration),
  cue(cues,["لے آؤٹ","منظور شدہ","عمارت","تعمیر"],.56,duration),
  cue(cues,["تحقیقاتی","تحقیقات","ادائیگیوں","فائلوں"],.39,duration),
 ]
 matched=sorted([(t,clips[i],SCENES[i]) for i,t in enumerate(matched)],key=lambda x:x[0])
 # Preserve spacing; avoid 3D overlays stacking on top of each other.
 for k in range(1,len(matched)):
  if matched[k][0]-matched[k-1][0]<8.0:
   matched[k]=(min(duration-7,matched[k-1][0]+12),matched[k][1],matched[k][2])
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source)]
 for t,f,_ in matched:
  cmd+=["-i",str(f)]
 n=0
 labels="[0:v]"
 filters=[]
 for i,(t,f,name) in enumerate(matched):
  overlay=f"[p{i}]";output=f"[m{i}]"
  filters.append(f"[{i+1}:v]setpts=PTS-STARTPTS,fps=25,scale=1480:832:flags=lanczos,format=yuva420p,"
    f"fade=t=in:st=0:d=0.45:alpha=1,fade=t=out:st=4.2:d=0.7:alpha=1,"
    f"setpts=PTS+{round(t,3)}/TB{overlay}")
  # The source is STILL moving on the left and around the 3D reconstruction.
  filters.append(f"{labels}{overlay}overlay=x=360:y=112:"
    f"eof_action=pass:repeatlast=0:shortest=0{output}")
  labels=output
 # End on source footage and untouched original narration/music.
 filters.append(f"{labels}format=yuv420p[outv]")
 cmd+=["-filter_complex",";".join(filters),"-map","[outv]","-map","0:a:0",
       "-c:v","libx264","-preset","medium","-crf","18","-c:a","copy",
       "-t",str(round(duration,3)),"-movflags","+faststart",str(out)]
 run(cmd)
 qc={"input":str(source),"output":str(out),
     "3d_segments":[{"start":round(t,2),"type":name,"scene":str(f),
      "provenance":"Illustrative reconstruction; Poly Haven CC0 source"} for t,f,name in matched],
     "narration_source":"Gemini synthetic Urdu review, human listening required",
     "subtitle_source":"Current base video subtitle burn-in",
     "original_stock_footage_preserved":True,
     "duration_seconds":round(duration,2)}
 out.with_suffix(".json").write_text(json.dumps(qc,indent=2,ensure_ascii=False),encoding="utf8")
 print("HYBRID REAL VIDEO + 3D COMPOSITE CREATED:",out,flush=True)

def main():
 a=argparse.ArgumentParser()
 a.add_argument("--base",required=True);a.add_argument("--scenes-dir",required=True)
 a.add_argument("--cues",required=True);a.add_argument("--out",required=True)
 x=a.parse_args()
 d=Path(x.scenes_dir)
 clips=[d/(s+".mp4") for s in SCENES]
 if not all(x.is_file() for x in clips):raise RuntimeError("Missing original Blender footage")
 cue_data=json.loads(Path(x.cues).read_text(encoding="utf8"))
 compose(Path(x.base),clips,cue_data,Path(x.out))
if __name__=="__main__":main()
