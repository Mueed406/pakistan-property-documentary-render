#!/usr/bin/env python3
"""Mix an expressive male narration into an existing SFX-only Poppy short.

Requires: ffmpeg and ffprobe on PATH. No voice cloning. Does not publish.
Example:
  python scripts/poppy_voice_mux.py --video review.mp4 --narration male_narration.wav --output voiced.mp4
"""
import argparse
import pathlib
import subprocess
import sys

def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode:
        raise SystemExit(proc.stderr[-3000:])
    return proc.stdout

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--narration", required=True)
    p.add_argument("--output", default="Poppy_Playtime_V2_WITH_MALE_VOICE.mp4")
    args = p.parse_args()
    video, voice, output = (pathlib.Path(v) for v in (args.video,args.narration,args.output))
    for f in [video,voice]:
        if not f.is_file(): p.error(f"Missing file: {f}")
    if output.resolve() in [video.resolve(),voice.resolve()]: p.error("Output must differ from inputs")
    # Review cut is expected to contain already-designed original sound effects in track 0:a.
    filter_complex = (
        "[0:a]volume=0.22[effects];"
        "[1:a]volume=1.0[narrator];"
        "[effects][narrator]amix=inputs=2:duration=first:dropout_transition=0,"
        "alimiter=limit=0.88[a]"
    )
    run(["ffmpeg","-hide_banner","-y","-i",str(video),"-i",str(voice),
         "-filter_complex",filter_complex,"-map","0:v:0","-map","[a]",
         "-c:v","copy","-c:a","aac","-b:a","192k",
         "-movflags","+faststart","-shortest",str(output)])
    print(f"Voiced review: {output}")
    print(run(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height:format=duration",
               "-of","default=noprint_wrappers=1",str(output)]))
    print("Review voice timing, caption alignment and loudness manually before publication.")

if __name__=="__main__":main()
