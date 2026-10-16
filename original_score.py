#!/usr/bin/env python3
"""Compose an ORIGINAL instrumental documentary score with NumPy; no sampled/third-party music.
Copyright released to public domain (CC0-equivalent dedication) for this project.
Deterministic synthesis, 32 kHz stereo, softly evolving minor-key ambient pads and restrained bass pulses.
"""
import argparse, wave, math
from pathlib import Path
import numpy as np
def compose(voice_file, out):
 import subprocess
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(voice_file)]).decode())
 sr=32000; duration=dur+2.0
 chords=[(146.83,174.61,220.00),(116.54,146.83,174.61),(130.81,164.81,196.00),(130.81,164.81,220.00)]
 rng=np.random.default_rng(20261017)
 with wave.open(str(out),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
  for begin in np.arange(0,duration,6.0):
   n=int(min(6.0,duration-begin)*sr);t=begin+np.arange(n,dtype=np.float64)/sr
   prog=t/24.0; idx=np.floor(prog).astype(int)%4; nxt=(idx+1)%4
   shift=np.clip((prog-np.floor(prog)-.77)/.23,0,1); mix=shift*shift*(3-2*shift)
   pad=np.zeros(n,dtype=np.float64)
   for j in range(3):
    fs=np.array([c[j] for c in chords],dtype=np.float64)
    f0=fs[idx];f1=fs[nxt]
    # Melody is a composed, gently changing chord voice; crossfade to prevent pops.
    phi0=2*np.pi*f0*t;phi1=2*np.pi*f1*t
    pad+=(np.sin(phi0+0.15*np.sin(.09*t))+0.32*np.sin(2*phi0+.31))* (1-mix)/5
    pad+=(np.sin(phi1+0.15*np.sin(.09*t))+0.32*np.sin(2*phi1+.31))* mix/5
   pad*=.3*(.7+.3*np.sin(np.pi*t/9)**2)
   # Slow drone and soft breath-like granular texture; remains below speech.
   bass_freq=np.array([c[0]/4 for c in chords])[idx]
   beat=np.exp(-((t%6.0)/.75)**2)
   bass=.16*np.sin(2*np.pi*bass_freq*t)*beat
   shimmer=.03*np.sin(2*np.pi*293.66*t+0.9*np.sin(.06*t))*np.sin(np.pi*t/31)**2
   air=rng.standard_normal(n)*.0015
   body=pad+bass+shimmer+air
   head=np.minimum(1,t/3.0);tail=np.minimum(1,(duration-t)/3.5)
   envelope=np.maximum(0,np.minimum(head,tail))
   body=np.tanh(body*1.3)*envelope
   # Tiny time-varying stereo width; safe peak and no heavy subsonic signal.
   left=body
   right=(pad*.97 + bass + shimmer*.9 + air)*envelope
   pcm=np.stack([left,right],axis=1)
   peak=np.max(np.abs(pcm))
   if peak>0.93:pcm*=0.93/peak
   w.writeframes((np.clip(pcm,-1,1)*32767).astype('<i2').tobytes())
 print('ORIGINAL SCORE',out,'duration',round(duration,1),'seconds')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--voice',required=True);p.add_argument('--output',default='licensed_score.wav');a=p.parse_args();compose(a.voice,a.output)
