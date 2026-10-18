#!/usr/bin/env python3
"""Deterministic original 90-second spatial ambience/Foley/score.
Engineering audio, not a final master. NO dialogue, sampled copyrighted
game audio, cloned voice, borrowed song or third-party library.
Requires only Python 3 and numpy. 48 kHz stereo separated stems.
"""
import argparse
import json
from pathlib import Path
import wave
import numpy as np

FS=48000
DURATION=90
CUES=[
    (2.6,"heavy_step"), (5.4,"glove_cable"), (7.8,"electric_spark"),
    (11.6,"power_down"), (13.5,"toy_turn"), (15.1,"toy_turn"),
    (17.2,"toy_turn"), (20.4,"vhs_insert"), (21.5,"vhs_hiss"),
    (28.5,"light_flicker"), (34,"heavy_step"),
    (39.2,"conveyor_collision"), (42.3,"conveyor_collision"),
    (47.7,"door_strike"), (51.8,"door_strike"), (56,"lock_alarm"),
    (66.5,"door_open"), (73.4,"wall_slide"), (76.6,"reveal_riser"),
    (81.8,"impact_sting"), (84.9,"power_down"), (89.2,"last_creak")
]
rng=np.random.default_rng(20261018)

def ramp(t,a,b):
    v=np.clip((t-a)/max(.001,b-a),0,1)
    return v*v*(3-2*v)

def impact(dst,when,duration=.55,pitch=85,amp=.25,pan=0,noise=.3,decay=12):
    i=max(0,round(when*FS)); j=min(len(dst),round((when+duration)*FS))
    if j<=i:return
    q=np.arange(j-i,dtype=np.float32)/FS
    env=(1-np.exp(-q*280))*np.exp(-q*decay)
    wave1=(np.sin(2*np.pi*pitch*q)+.25*np.sin(2*np.pi*2.015*pitch*q))
    sound=env*amp*(wave1+noise*rng.standard_normal(len(q)))
    dst[i:j,0]+=sound*np.sqrt((1-pan)/2)
    dst[i:j,1]+=sound*np.sqrt((1+pan)/2)

def save(path,signal):
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(FS)
        w.writeframes((np.clip(signal,-.999,.999)*32767).astype("<i2").tobytes())

def synth(directory):
    t=np.arange(FS*DURATION,dtype=np.float32)/FS
    ambient=np.zeros((t.size,2),dtype=np.float32)
    foley=np.zeros_like(ambient);score=np.zeros_like(ambient)
    motor=(.11*np.sin(2*np.pi*(53.4*t+.13*np.sin(2*np.pi*.12*t)))
          +.067*np.sin(2*np.pi*84.1*t)
          +.042*np.sin(2*np.pi*119.3*t))
    air=rng.standard_normal(t.size).astype(np.float32)
    low=np.repeat(air.reshape(-1,64).mean(axis=1),64)
    fade=np.minimum(1.,ramp(t,0,2)+.14)
    ambient[:,0]=(motor+low*.3)*fade
    ambient[:,1]=(.94*motor+.25*np.roll(low,43))*fade
    for when in np.arange(.75,85,.94):
        impact(ambient,float(when),.12,580,.035,np.sin(when)*.5,.28,18)

    # Dark minor-second progression. Speech windows receive music ducking.
    progression=[(0,55,77.78),(20,51.91,73.42),(36,58.27,82.41),
                 (55,55,69.3),(65,49,73.42),(76,55,77.78)]
    for i,(start,a,b) in enumerate(progression):
        end=progression[i+1][0] if i+1<len(progression) else 90
        m=(t>=start)&(t<end);time=t[m]-start
        e=(.4+.6*ramp(time,0,2))*(1-.55*ramp(time,end-start-1,end-start))
        score[m,0]=.048*e*(np.sin(2*np.pi*a*time)+.34*np.sin(2*np.pi*b*time)+.22*np.sin(2*np.pi*2.01*a*time))
        score[m,1]=.049*e*(np.sin(2*np.pi*1.003*a*time+.5)+.32*np.sin(2*np.pi*.997*b*time)+.19*np.sin(2*np.pi*2.01*a*time+.7))
    speech=[(7,10.6),(22,26.3),(30,33.9),(49,53),(58,64),(70,74.1)]
    duck=np.ones(t.size,dtype=np.float32)
    for a,b in speech:
        duck*=1-.64*ramp(t,a-.65,a)*(1-ramp(t,b,b+.85))
    energy=(.78+.75*ramp(t,34,36)*(1-ramp(t,46,48))
                +.38*ramp(t,74,76)*(1-ramp(t,83,85)))
    score*=((duck*energy)*(1-ramp(t,84.4,85)))[:,None]

    # True time-coded material contacts and footfalls; no 3rd-party sounds.
    for when in np.arange(36.08,45.9,.48):
        impact(foley,float(when),.19,63,.22,np.sin(when*1.3)*.65,.55,19)
        impact(foley,float(when+.26),.14,96,.10,-np.sin(when*1.3)*.65,.38,26)
    for when in np.arange(76,83.5,.45):
        impact(foley,float(when),.24,54,.26,np.sin(when*2)*.65,.28,13)
    for when,name in CUES:
        if name=="heavy_step":
            impact(foley,when,.85,58,.43,-.7 if when<30 else .6,.22,5)
        elif name in ("door_strike","impact_sting","conveyor_collision"):
            impact(foley,when,.72,68,.78 if name=="impact_sting" else .49,-.18,.5,6)
            impact(foley,when+.03,.66,211,.38,.35,.8,9)
        elif name in ("electric_spark","light_flicker","vhs_hiss","lock_alarm","power_down"):
            impact(foley,when,.7,780,.22,.6,2.2,12)
        elif name in ("wall_slide","door_open","glove_cable","vhs_insert"):
            impact(foley,when,1.3,98,.35,-.42,.38,3)
        elif name=="reveal_riser":
            for q in np.arange(0,4.6,.19):
                impact(foley,when+float(q),.6,130+65*q,.02+.035*q,np.sin(q*3),.25,11)
        elif name=="last_creak":
            impact(foley,when,.56,233,.14,.8,.2,6)
        else:
            impact(foley,when,.3,330,.13,np.sin(when),.35,15)
    dry=foley.copy()
    for delay,gain in [(.067,.13),(.145,.11),(.24,.065)]:
        n=int(delay*FS)
        foley[n:,0]+=gain*dry[:-n,1]
        foley[n:,1]+=gain*dry[:-n,0]
    mix=ambient+foley+score
    peak=float(np.max(np.abs(mix)))
    scale=min(1,.69/max(peak,1e-9))
    out=Path(directory)
    stems={
        "factory_ambience":ambient,
        "original_foley_sfx":foley,
        "original_suspense_score":score,
        "TEMP_90S_MIX_NO_VOICES_NOT_FINAL":mix
    }
    for name,signal in stems.items():
        save(out/(name+".wav"),signal*scale)
    report={"seconds":90,"sample_frames":int(t.size),"sample_rate":FS,
            "stems":list(stems),"cues":len(CUES),"peak":round(peak*scale,6),
            "speech_ducked_windows":speech,
            "warning":"Original, synthetic soundscape. NO English dialogue or artistic approval; NOT a final film."}
    out.mkdir(parents=True,exist_ok=True)
    (out/"audio_qa.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="output/soundscape")
    synth(ap.parse_args().out)
