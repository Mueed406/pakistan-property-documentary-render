#!/usr/bin/env python3
"""Repeatable, voice-first mastering for human or neural Urdu narration.

Free Windows/Linux/Mac headless tools: Spotify Pedalboard + FFmpeg EBU R128.
This improves tonal balance and dynamics, NOT learned robotic prosody.
"""
import argparse,subprocess,json,sys
from pathlib import Path

def call(argv):
 print("AUDIO EXEC",argv[0],argv[-1],flush=True)
 subprocess.run(argv,check=True)

def master(source,dest):
 from pedalboard import Pedalboard,HighpassFilter,Compressor,Limiter
 from pedalboard.io import AudioFile
 inp=Path(source)
 if not inp.is_file():raise FileNotFoundError(inp)
 dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
 intermediate=dest.parent/(dest.stem+"_pedalboard.wav")
 # Realtime-capable VST-style DSP, cross-platform, no paid plugins.
 chain=Pedalboard([
  HighpassFilter(cutoff_frequency_hz=77),
  Compressor(threshold_db=-21.5,ratio=1.85,attack_ms=13,release_ms=175),
  Limiter(threshold_db=-1.7)
 ])
 with AudioFile(str(inp)).resampled_to(48000) as f:
  with AudioFile(str(intermediate),"w",48000,f.num_channels) as dst:
   while f.tell()<f.frames:
    x=f.read(min(48000*8,f.frames-f.tell()))
    dst.write(chain(x,48000))
 # Final EBU R128 loudness and true-peak limiting, preserve dry close-up narration.
 call(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(intermediate),
       "-af","loudnorm=I=-17:TP=-1.5:LRA=8",
       "-ar","48000","-c:a","pcm_s24le",str(dest)])
 info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format",
   "-show_streams","-of","json",str(dest)]))
 audio=[s for s in info["streams"] if s["codec_type"]=="audio"]
 assert audio and int(audio[0]["sample_rate"])==48000,"Mastering output stream invalid"
 duration=float(info["format"]["duration"])
 if duration<4:raise RuntimeError("Mastering unexpectedly short")
 meta={"input":str(inp),"output":str(dest),"duration_seconds":duration,
       "sample_rate_hz":48000,"target_integrated_lufs":-17,"true_peak_target_dbtp":-1.5,
       "warning":"EQ/compression do not fix robotic or incorrect Urdu voice performance"}
 dest.with_suffix(".json").write_text(json.dumps(meta,indent=2),encoding="utf8")
 intermediate.unlink(missing_ok=True)
 print("MASTERED",dest,round(duration,2),"seconds")

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--input",required=True)
 p.add_argument("--output",required=True)
 a=p.parse_args()
 master(a.input,a.output)
