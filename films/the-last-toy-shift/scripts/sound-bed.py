#!/usr/bin/env python3
"""Original synthetic machine ambience for INTERNAL TECHNICAL PROOFS ONLY.
No dialogue, copyrighted samples, cloned performer, or game soundtrack.
"""
import argparse
from pathlib import Path
import wave
import numpy as np

def synth(seconds: float, offset: float, seed: int = 20261017):
    sr = 48000
    n = round(seconds * sr)
    t = np.arange(n, dtype=np.float64) / sr + offset
    rng = np.random.default_rng(seed + int(offset))
    left = np.zeros(n, dtype=np.float64)
    right = np.zeros(n, dtype=np.float64)
    # Low industrial motor, detuned mechanical rotation and long room hum.
    bed = (0.085*np.sin(2*np.pi*54*t + .12*np.sin(2*np.pi*.19*t))
           +0.040*np.sin(2*np.pi*89.7*t)
           +0.024*np.sin(2*np.pi*181.4*t+.7*np.sin(2*np.pi*.23*t)))
    air = rng.standard_normal(n)*0.015
    filt = np.convolve(air[:min(n,120000)], np.ones(55)/55, mode='same')
    # Avoid costly full-length convolution; use difference-equation IIR filtering.
    scratch = np.cumsum(air)*.00014
    scratch = np.clip(scratch,-.04,.04)
    left += bed+scratch
    right += bed*.89-np.roll(scratch,31)*.9
    # Physical cue times in absolute story seconds: footsteps, switch sparks, heavy impacts.
    cues = [(2.7,.22,48),(6.9,.16,1200),(7.4,.25,1700),
            (30.8,.25,71),(34.4,.36,49),(50.7,.43,96),
            (76.3,.55,52),(82.1,.88,44)]
    cues += [(x,.15,63) for x in np.arange(36.0,46.0,.48)]
    for when,amp,freq in cues:
        first=max(0,round((when-offset)*sr))
        last=min(n,round((when-offset+.28)*sr))
        if last<=first:continue
        relative=np.arange(first,last)/sr-(when-offset)
        env=np.exp(-np.maximum(relative,0)*16)*(relative>=0)
        impact=np.sin(2*np.pi*freq*relative)*env
        noise=rng.standard_normal(len(relative))*env*.25
        left[first:last] += amp*(impact+noise)
        right[first:last] += amp*.84*(impact-noise*.4)
    # Decorrelation for wider atmos; controlled peak, reserved headroom for future voices.
    stereo=np.stack([left,right],axis=1)
    peak=np.max(np.abs(stereo))
    if peak>0:stereo*=min(1.0,.64/peak)
    return sr,(stereo*32767).astype('<i2')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seconds',type=float,default=16)
    p.add_argument('--offset',type=float,default=30)
    p.add_argument('--out',default='output/proof-ambient.wav')
    args=p.parse_args()
    if not (0<args.seconds<=90 and 0<=args.offset<=90-args.seconds):p.error('Invalid passage')
    sr,pcm=synth(args.seconds,args.offset)
    path=Path(args.out);path.parent.mkdir(exist_ok=True,parents=True)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
    print('Original stereo ambience (NO VOICES):',path,pcm.shape[0]/sr,'seconds')
if __name__=='__main__':main()
