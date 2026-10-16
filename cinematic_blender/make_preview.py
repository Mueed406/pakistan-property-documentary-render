#!/usr/bin/env python3
"""Finish an original 3D documentary-look test with justified cinematic transitions.

This is an illustrative 3D reconstruction, never footage of the actual site.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"cinematic_output"
CLIPS=[OUT/f"{x}.mp4" for x in ("01_cinematic_parcel_map","02_architecture_construction","03_evidence_document_desk")]
FINAL=OUT/"property_documentary_3d_visual_preview.mp4"

def call(args):
 print("EXEC",args[0],str(args[-1]),flush=True)
 subprocess.run(args,check=True)
def probe(p):
 r=subprocess.check_output(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(p)])
 return json.loads(r)

def main():
 for path in CLIPS:
  if not path.is_file():raise RuntimeError("Missing 3D animation "+str(path))
  meta=probe(path)
  v=next((s for s in meta["streams"] if s["codec_type"]=="video"),None)
  if not v or v["width"]<960 or float(meta["format"]["duration"])<4.7:
   raise RuntimeError("A 3D animation was invalid: "+str(path))
 # The score is an entirely original synthesis, no copyright tracks or samples.
 with wave.open(str(OUT/"reference_silence.wav"),"wb") as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
  w.writeframes(b"\0\0"*int(16000*14.3))
 call([sys.executable,str(ROOT/"original_score.py"),"--voice",str(OUT/"reference_silence.wav"),
       "--output",str(OUT/"original_investigative_score.wav")])
 w=1280;h=720
 filters=("[0:v]fps=20,scale=1280:720,setsar=1,format=yuv420p[v0];"
 "[1:v]fps=20,scale=1280:720,setsar=1,format=yuv420p[v1];"
 "[2:v]fps=20,scale=1280:720,setsar=1,format=yuv420p[v2];"
 "[v0][v1]xfade=transition=fade:duration=0.5:offset=4.5[x1];"
 "[x1][v2]xfade=transition=fade:duration=0.5:offset=9.0[x2];"
 "[x2]eq=contrast=1.05:saturation=0.93,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
 "text='CONCEPTUAL 3D - NOT ACTUAL SITE':fontcolor=white@0.72:fontsize=16:"
 "box=1:boxcolor=black@0.35:boxborderw=8:x=25:y=25[outv];"
 "[3:a]volume=0.75,afade=t=in:st=0:d=0.8,afade=t=out:st=12.7:d=1.2[outa]")
 call(["ffmpeg","-hide_banner","-y","-loglevel","error",
       "-i",str(CLIPS[0]),"-i",str(CLIPS[1]),"-i",str(CLIPS[2]),
       "-i",str(OUT/"original_investigative_score.wav"),
       "-filter_complex",filters,"-map","[outv]","-map","[outa]",
       "-c:v","libx264","-preset","medium","-crf","18",
       "-c:a","aac","-b:a","160k","-t","14.0","-movflags","+faststart",str(FINAL)])
 info=probe(FINAL)
 (OUT/"preview_technical_qc.json").write_text(json.dumps(
   {"video":str(FINAL),"duration":info["format"]["duration"],
    "resolution":"1280x720","stockfootage_used":0,"3d_assets":"Poly Haven modular apartments facade CC0",
    "animated_scenes":3,"music":"Original generated music",
    "narration":"No TTS added until improved Gemini voice is tested",
    "disclaimer":"All visual scenes are illustrative conceptual reconstruction"},
   indent=2),encoding="utf-8")
 print("SUCCESS",FINAL,str(FINAL.stat().st_size),flush=True)
if __name__=="__main__":main()
