#!/usr/bin/env python3
"""Genuine cloud Kokoro ONNX CPU synthesis with verified original model files.
90 second 3-role voice audition for The Last Toy Shift. NOT a final film.
Does not call any external speech API and does not use the user's local GPU.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import wave
from pathlib import Path
from urllib.request import Request, urlopen

MODEL_REPO="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/"
FILES={
 "kokoro-v1.0.onnx":"beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a",
 "voices-v1.0.bin":"bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}
RATE=48000
FILM=Path(__file__).resolve().parents[1]
STORY=Path(__file__).with_name("dialogue_plan.json")

def execute(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode!=0:
        raise RuntimeError("Command failed: "+str(args)+"\n"+p.stderr.decode(errors="replace")[-2200:])
    return p.stdout.decode(errors="replace").strip()

def fetch_models(root):
    root.mkdir(parents=True,exist_ok=True)
    for name,expected in FILES.items():
        dst=root/name
        if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest()==expected:
            print("CACHE VERIFIED:",name,flush=True);continue
        for attempt in range(1,4):
            temp=dst.with_suffix(dst.suffix+".partial")
            temp.unlink(missing_ok=True)
            sha=hashlib.sha256()
            try:
                req=Request(MODEL_REPO+name,headers={"User-Agent":"TheLastToyShift-OpenSourceTTS/1.0"})
                with urlopen(req,timeout=100) as response,open(temp,"wb") as handle:
                    while True:
                        chunk=response.read(2*1024*1024)
                        if not chunk:break
                        sha.update(chunk)
                        handle.write(chunk)
                if sha.hexdigest()!=expected:
                    raise RuntimeError("OFFICIAL MODEL SHA256 INVALID "+name+": "+sha.hexdigest())
                os.replace(temp,dst)
                break
            except Exception:
                temp.unlink(missing_ok=True)
                if attempt==3:raise
                time.sleep(attempt*2)
        print("MODEL CHECKSUM PASS",name,dst.stat().st_size,"bytes",flush=True)
    return root/"kokoro-v1.0.onnx",root/"voices-v1.0.bin"

def sound_write(path,sound):
    import numpy as np
    data=np.asarray(sound,dtype=np.float32)
    if not np.isfinite(data).all():raise ValueError("non-finite output")
    data=np.clip(data,-.96,.96)
    stereo=np.stack([data,data],axis=1)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes((stereo*32767).astype("<i2").tobytes())

def resample(samples,rate):
    import numpy as np
    samples=np.asarray(samples,dtype=np.float32).reshape(-1)
    if not samples.size or not np.isfinite(samples).all():
        raise RuntimeError("Empty / corrupt Kokoro speech")
    import scipy.signal
    from math import gcd
    div=gcd(int(rate),RATE)
    return scipy.signal.resample_poly(samples,RATE//div,int(rate)//div).astype(np.float32)

def fit(samples,length,words):
    import numpy as np
    available=round(length*RATE)
    if len(samples)>available:
        raw_ratio=len(samples)/available
        if raw_ratio>1.25:
            raise RuntimeError("CUE TOO LONG. No truncation permitted: "+words+
                               " was "+str(round(len(samples)/RATE,2))+" seconds, slot "+str(length))
        # Mild speed-up while preserving pitch. No time stretch of short dialogue.
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            old=Path(folder)/"before.wav";new=Path(folder)/"after.wav"
            sound_write(old,samples)
            execute(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(old),
                     "-filter:a","atempo="+str(round(raw_ratio+0.025,4)),
                     "-ar",str(RATE),"-ac","2",str(new)])
            with wave.open(str(new),"rb") as w:
                sig=np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").reshape(-1,2)
                samples=sig.mean(axis=1).astype(np.float32)/32768.
        if len(samples)>available:
            raise RuntimeError("Adjusted speech still overruns slot: "+words)
    f=min(len(samples)//3,int(.018*RATE))
    if f:
        samples[:f]*=np.linspace(0,1,f,dtype=np.float32)
        samples[-f:]*=np.linspace(1,0,f,dtype=np.float32)
    return samples

def srt_time(seconds):
    ms=int(round(seconds*1000))
    hh,ms=divmod(ms,3600000)
    mm,ms=divmod(ms,60000)
    ss,ms=divmod(ms,1000)
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",default=str(FILM/"output/cloud-kokoro"))
    a.add_argument("--cache",default=str(Path.home()/".cache/the-last-toy-shift/kokoro-onnx"))
    opts=a.parse_args()
    import numpy as np
    import onnxruntime as ort
    from kokoro_onnx import Kokoro
    plan=json.loads(STORY.read_text(encoding="utf8"))
    assert plan["timeline_seconds"]==90 and len(plan["characters"])==3 and len(plan["cues"])==6
    root=Path(opts.output);root.mkdir(parents=True,exist_ok=True)
    model,voices=fetch_models(Path(opts.cache))
    providers=ort.get_available_providers()
    print("Cloud inference ONNX providers:",providers,flush=True)
    if "CPUExecutionProvider" not in providers:
        raise RuntimeError("Cloud CPU provider unavailable")
    options=ort.SessionOptions()
    options.intra_op_num_threads=min(8,max(2,os.cpu_count() or 2))
    options.inter_op_num_threads=2
    session=ort.InferenceSession(str(model),sess_options=options,providers=["CPUExecutionProvider"])
    if session.get_providers()!=["CPUExecutionProvider"]:
        raise RuntimeError("Unexpected CPU cloud inference provider")
    model=Kokoro.from_session(session,str(voices))
    tracks={role:np.zeros(RATE*90,dtype=np.float32) for role in plan["characters"]}
    slots=[];srt=[]
    start_clock=time.monotonic()
    for idx,(role,start,slot,words) in enumerate(plan["cues"],1):
        voice=plan["characters"][role]["voice"]
        samples,rate=model.create(words,voice=voice,speed=1.0,lang="en-us")
        data=fit(resample(samples,rate),slot,words)
        start_sample=round(start*RATE)
        tracks[role][start_sample:start_sample+len(data)]+=data
        duration=round(len(data)/RATE,4)
        slots.append({"index":idx,"role":role,"voice":voice,"start":start,"slot":slot,"actual_duration":duration,"text":words})
        srt.append(f"{idx}\n{srt_time(start)} --> {srt_time(start+duration)}\n{words}\n")
        print("CUE PASS",idx,role,words,"duration",duration,flush=True)
    mixed=sum(tracks.values())
    peak=float(np.max(np.abs(mixed)))
    if peak>.83:
        factor=.83/peak
        for role in tracks:tracks[role]*=factor
        mixed*=factor
    for role,data in tracks.items():
        sound_write(root/f"ENGLISH_{role.upper()}_90S_CLOUD_CPU_DRAFT.wav",data)
    spoken=root/"ENGLISH_3VOICES_90S_CLOUD_CPU_DRAFT.wav"
    sound_write(spoken,mixed)
    (root/"ACTUAL_CUE_TIMES_DRAFT.srt").write_text("\n".join(srt),encoding="utf8")
    # Rebuild original in-repo synthetic Foley/score in this cloud job.
    bedroot=FILM/"output/soundscape"
    if not (bedroot/"TEMP_90S_MIX_NO_VOICES_NOT_FINAL.wav").exists():
        execute([sys.executable,str(FILM/"scripts/soundscape_90s.py"),"--out",str(bedroot)])
    bed=bedroot/"TEMP_90S_MIX_NO_VOICES_NOT_FINAL.wav"
    result=root/"LAST_TOY_SHIFT_90S_ENGLISH_SFX_CLOUD_CPU_AUDITION_NOT_FINAL.m4a"
    execute(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(bed),"-i",str(spoken),
             "-filter_complex",
             "[0:a]volume=0.78[b];[1:a]asplit=2[v][key];"
             "[b][key]sidechaincompress=threshold=0.018:ratio=7:attack=20:release=420[duck];"
             "[duck][v]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.87[out]",
             "-map","[out]","-ar","48000","-ac","2","-c:a","aac",
             "-b:a","256k","-t","90",str(result)])
    info=json.loads(execute(["ffprobe","-v","error","-show_entries",
                             "format=duration:stream=codec_name,sample_rate,channels",
                             "-of","json",str(result)]))
    duration=float(info["format"]["duration"])
    assert abs(duration-90.0)<.07,"AAC duration mismatch "+str(duration)
    assert any(x.get("codec_name")=="aac" and x.get("sample_rate")=="48000" and x.get("channels")==2 for x in info["streams"])
    qa={"result":"pass-engineering-draft","timeline_seconds":90,"codec":"aac","sample_rate":48000,
        "actual_export_duration":duration,"dialogue_characters":3,"cues":slots,
        "model_source":"thewh1teagle/kokoro-onnx official model-files-v1.1 release",
        "model_checksums":FILES,"license":"Kokoro weight Apache-2.0, kokoro-onnx MIT",
        "hardware":"GitHub Actions hosted Linux standard runner CPU, NO personal PC/GPU used",
        "onnx_inference_providers":session.get_providers(),"elapsed_tts_and_mix_s":round(time.monotonic()-start_clock,1),
        "mix_sha256":hashlib.sha256(result.read_bytes()).hexdigest(),
        "final_film":False,"human_voice_acting_approved":False,
        "comments":"Original code-generated music/SFX; three independent generated English voice roles, no voice cloning."}
    (root/"CLOUD_TTS_QA.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"result":"PASS cloud CPU genuine TTS 90s","duration":duration,"audio_sha256":qa["mix_sha256"],
                      "seconds_to_generate":qa["elapsed_tts_and_mix_s"],"model":"Kokoro ONNX","outputs":str(root)},indent=2),flush=True)

if __name__=="__main__":
    main()
