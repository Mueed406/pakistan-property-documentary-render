#!/usr/bin/env python3
"""Free Urdu Piper TTS voice lab: 3 controlled candidates for listening review.
This does not retrain a voice or pretend signal processing can erase learned prosody.
"""
from __future__ import annotations
import json
import shutil
import subprocess
import wave
from pathlib import Path
from free_voice import piper_setup

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"voice_lab_output"
TEST_LINES=[
    "آپ نے پلاٹ خریدا۔ رسید بھی موجود ہے۔ لیکن زمین کا درست ثبوت کہاں ہے؟",
    "آٹھ مئی دو ہزار چھبیس کو اسلام آباد کی ایک کوآپریٹو ہاؤسنگ سوسائٹی کے بارے میں تحقیقاتی خبر سامنے آئی۔",
    "رپورٹ کے مطابق تقریباً بیالیس ہزار فائلوں کا ذکر ہوا، جبکہ زمین پر لگ بھگ چھ ہزار پلاٹوں کی گنجائش بتائی گئی۔",
    "یہ فرق سنجیدہ سوالات پیدا کرتا ہے۔ مگر یاد رکھیے، یہ الزامات ہیں، کسی عدالت کا حتمی فیصلہ نہیں۔"
]
PROFILES={
    "A_current_reference":{"length_scale":1.00,"noise_scale":0.50,"noise_w":0.42,"pause":0.25},
    "B_calm_broadcast":{"length_scale":0.94,"noise_scale":0.40,"noise_w":0.20,"pause":0.18},
    "C_clear_measured":{"length_scale":0.97,"noise_scale":0.32,"noise_w":0.26,"pause":0.22}
}

def run(args,**kwargs):
    print("RUN",Path(args[0]).name,flush=True)
    subprocess.run(args,check=True,**kwargs)

def synthesize(model,config,profile,slug):
    rawdir=OUT/("raw_"+slug)
    rawdir.mkdir(parents=True,exist_ok=True)
    fragments=[]
    for i,line in enumerate(TEST_LINES):
        dest=rawdir/f"{i:02d}.wav"
        if not dest.exists() or dest.stat().st_size<2000:
            args=["piper","--model",str(model),"--config",str(config),
                  "--length-scale",str(profile["length_scale"]),
                  "--noise-scale",str(profile["noise_scale"]),
                  "--noise-w",str(profile["noise_w"]),
                  "--sentence-silence","0",
                  "--output-file",str(dest)]
            run(args,input=(line+"\n").encode("utf-8"),stdout=subprocess.DEVNULL)
        fragments.append(dest)
    dest=OUT/(slug+"_raw.wav")
    rate=None
    with wave.open(str(dest),"wb") as w:
        for f in fragments:
            with wave.open(str(f),"rb") as rd:
                if rate is None:
                    rate=rd.getframerate()
                    w.setframerate(rate);w.setnchannels(rd.getnchannels());w.setsampwidth(rd.getsampwidth())
                assert (rd.getframerate(),rd.getnchannels(),rd.getsampwidth())==(rate,1,2),"Piper sample format changed"
                w.writeframes(rd.readframes(rd.getnframes()))
                w.writeframes(b"\0\0"*round(rate*profile["pause"]))
    return dest

def process(src,slug,style):
    dst=OUT/(slug+".mp3")
    if style=="reference":
        fx="highpass=f=72,lowpass=f=9000,loudnorm=I=-17:TP=-2:LRA=10"
    elif style=="calm":
        fx="highpass=f=78,lowpass=f=8700,equalizer=f=260:t=q:w=1.0:g=-1.4,equalizer=f=3300:t=q:w=1:g=0.6,acompressor=threshold=0.15:ratio=1.8:attack=12:release=160:makeup=1.1,loudnorm=I=-17:TP=-2:LRA=10"
    else:
        fx="highpass=f=82,lowpass=f=8300,equalizer=f=300:t=q:w=1.0:g=-1.0,equalizer=f=4000:t=q:w=1.0:g=-0.65,acompressor=threshold=0.12:ratio=2.0:attack=14:release=190:makeup=1.15,loudnorm=I=-17:TP=-2:LRA=10"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-af",fx,
         "-ar","48000","-ac","1","-c:a","libmp3lame","-b:a","192k",str(dst)])
    return dst

def duration(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration",
                     "-of","default=noprint_wrappers=1:nokey=1",str(f)],text=True).strip())

def main():
    if not shutil.which("piper") or not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("Requires piper, FFmpeg and FFprobe")
    OUT.mkdir(exist_ok=True)
    model,config=piper_setup()
    records=[]
    for name,profile in PROFILES.items():
        src=synthesize(model,config,profile,name)
        variant="reference" if name.startswith("A_") else ("calm" if name.startswith("B_") else "measured")
        sample=process(src,name,variant)
        records.append({"name":name,"filename":sample.name,"duration_seconds":round(duration(sample),2),
                        "profile":profile,"mastering":variant})
        print("SAMPLE READY",sample.name,records[-1]["duration_seconds"],"seconds",flush=True)
    (OUT/"LISTEN_FIRST.txt").write_text(
        "Listen in order, ideally with headphones and the same volume.\n"
        "A: previous Piper parameter baseline.\n"
        "B: slightly brisker, less pitch/duration jitter, gentle compression.\n"
        "C: restrained variation and softer EQ.\n"
        "Focus: Does it still sound like crying? Are Urdu vowels and numbers clear? Do pauses sound natural?\n"
        "Do NOT treat loudness/EQ improvements as proof the model has human prosody.\n"
        "If NONE passes, request a new authorized Urdu TTS model or a human voice recording.\n",
        encoding="utf-8")
    (OUT/"comparison.json").write_text(json.dumps({"language":"ur-PK","engine":"Piper fasih medium",
            "text":TEST_LINES,"profiles":records},ensure_ascii=False,indent=2),encoding="utf-8")
    print("Voice lab complete:",OUT,flush=True)

if __name__=="__main__":
    main()
