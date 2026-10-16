#!/usr/bin/env python3
"""Print verifiable installation prerequisites; never claim the media is present when it isn't."""
import importlib.util, shutil, os, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
for exe in ['ffmpeg','ffprobe','piper']:
 path=shutil.which(exe);print(f'{exe}: {path or "MISSING"}')
for name in ['requests','edge_tts']:
 print(f'{name}: {"INSTALLED" if importlib.util.find_spec(name) else "MISSING"}')
files=['urdu_voice.wav','urdu_timed.srt','licensed_score.mp3']
for name in files: print(f'{name}: {"PRESENT" if (root/name).is_file() else "not created / optional"}')
print('Available downloaded stock MP4 files:',len(list((root/'footage').glob('S*.mp4'))))
print('Source manifest exists:',(root/'Stock_Footage_Manifest_47.csv').is_file())
print('Report generated for actual current machine, not ChatGPT sandbox.')
