#!/usr/bin/env python3
"""Locally executed English film TTS. CUDA GPU when PyTorch detects it; CPU for
phonemization, resampling, stitching and FFmpeg mixing. No cloud TTS calls.
No copyrighted actor cloning, no voice model binaries committed to GitHub.
"""
import argparse, hashlib, json, os, subprocess, sys, wave
from pathlib import Path

RATE=48000
def process(args,stdin=None):
    p=subprocess.run(args,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(str(args)+"\n"+p.stderr.decode(errors="replace")[-1000:])
    return p.stdout

def hardware():
    try:
        import torch
        torch.set_num_threads(min(8,max(1,os.cpu_count() or 1)))
        if torch.cuda.is_available():
            # Quadro Maxwell and some older cards can be visible to the driver
            # but unsupported by recently built CUDA PyTorch kernels.
            try:
                test=torch.ones((32,32),device="cuda")
                checksum=float((test@test).sum().item())
                torch.cuda.synchronize()
                if checksum<=0:raise RuntimeError("Invalid CUDA computation")
                return {"device":"cuda","name":torch.cuda.get_device_name(0),
                        "compute_capability":list(torch.cuda.get_device_capability(0)),
                        "compiled_cuda_arches":torch.cuda.get_arch_list(),
                        "vram_gb":round(torch.cuda.get_device_properties(0).total_memory/2**30,2),
                        "cuda_kernel_smoke":"PASS","torch":torch.__version__}
            except Exception as exc:
                return {"device":"cpu","name":"GPU present but CUDA PyTorch compute failed",
                        "cuda_kernel_smoke":"FAIL","failure":str(exc),
                        "torch":torch.__version__,"vram_gb":None}
        if getattr(torch.backends,"mps",None) and torch.backends.mps.is_available():
            return {"device":"mps","name":"Apple Metal","vram_gb":None,"torch":torch.__version__}
        return {"device":"cpu","name":"CPU","vram_gb":None,"torch":torch.__version__}
    except ImportError:
        return {"device":"cpu","name":"CPU / install PyTorch","vram_gb":None,"torch":None}

def references(folder,roles):
    if not folder:return None
    path=Path(folder)
    f=path/"consent.json"
    if not f.is_file():return None
    manifest=json.loads(f.read_text(encoding="utf8"))
    found={}
    for role in roles:
        c=manifest.get(role,{})
        sound=path/(role+".wav")
        if not (c.get("speaker_consent") is True and c.get("authorized_for_this_film") is True and sound.is_file()):
            return None
        found[role]=sound
    return found

def to_48k(raw,source_rate):
    import numpy as np
    a=np.asarray(raw,dtype="float32").reshape(-1)
    if not a.size or not np.isfinite(a).all():raise RuntimeError("Invalid generated TTS audio")
    binary=process(["ffmpeg","-hide_banner","-loglevel","error","-f","f32le","-ar",str(source_rate),"-ac","1","-i","pipe:0","-ar",str(RATE),"-ac","1","-f","f32le","pipe:1"],a.astype("<f4").tobytes())
    return np.frombuffer(binary,dtype="<f4").copy()

def wav(path,mono):
    import numpy as np
    samples=np.clip(mono,-.96,.96)
    stereo=np.stack((samples,samples),axis=1)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes((stereo*32767).astype("<i2").tobytes())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["probe","generate"])
    p.add_argument("--backend",choices=["auto","kokoro","chatterbox-original","chatterbox-turbo","chatterbox-nano"],default="auto")
    p.add_argument("--references",default="")
    p.add_argument("--require-gpu",action="store_true")
    p.add_argument("--output",default="output/local-voice")
    p.add_argument("--no-mix",action="store_true")
    args=p.parse_args()
    hw=hardware()
    if args.action=="probe":
        try:
            hw["nvidia_smi"]=process(["nvidia-smi","--query-gpu=name,memory.total,driver_version","--format=csv,noheader"]).decode(errors="replace").strip()
        except (OSError,RuntimeError):hw["nvidia_smi"]=None
        print(json.dumps(hw,indent=2));return
    import numpy as np
    import torch
    if args.require_gpu and hw["device"]=="cpu":raise RuntimeError("CUDA/MPS unavailable. GPU not used: "+str(hw))
    base=Path(__file__).resolve().parent
    plan=json.loads((base/"dialogue_plan.json").read_text(encoding="utf8"))
    assert plan["timeline_seconds"]==90 and len(plan["cues"])==6 and len(plan["characters"])==3
    refs=references(args.references,plan["characters"])
    backend=args.backend
    if backend=="auto":
        backend="chatterbox-turbo" if refs and hw["device"]=="cuda" and (hw["vram_gb"] or 0)>=6 else "kokoro"
    if backend.startswith("chatterbox") and not refs:
        raise RuntimeError("Chatterbox requires consented hero.wav, tape.wav, doll.wav and consent.json in --references")
    if backend=="kokoro":
        from kokoro import KPipeline
        try:engine=KPipeline(lang_code="a",device=hw["device"])
        except TypeError:
            if hw["device"]!="cpu":raise RuntimeError("Installed Kokoro does not accept device. Update it before claiming GPU use.")
            engine=KPipeline(lang_code="a")
    elif backend=="chatterbox-original":
        from chatterbox.tts import ChatterboxTTS
        engine=ChatterboxTTS.from_pretrained(device=hw["device"])
    else:
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        engine=ChatterboxTurboTTS.from_pretrained(device=hw["device"],nano=backend=="chatterbox-nano")
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    tracks={name:np.zeros(RATE*90,dtype=np.float32) for name in plan["characters"]}
    cues=[]
    for role,start,slot,words in plan["cues"]:
        if backend=="kokoro":
            chunks=[]
            with torch.inference_mode():
                for gs,ps,data in engine(words,voice=plan["characters"][role]["voice"],speed=1,split_pattern=r"\n+"):
                    chunks.append(np.asarray(data,dtype=np.float32).reshape(-1))
            if not chunks:raise RuntimeError("Kokoro gave empty utterance: "+words)
            signal=to_48k(np.concatenate(chunks),24000)
        else:
            with torch.inference_mode():
                if backend=="chatterbox-original":
                    result=engine.generate(words,audio_prompt_path=str(refs[role]),exaggeration=.65,cfg_weight=.3)
                else:result=engine.generate(words,audio_prompt_path=str(refs[role]))
            signal=to_48k(result.detach().cpu().numpy(),engine.sr)
        allowed=int(slot*RATE)
        if len(signal)>allowed:
            factor=len(signal)/allowed
            if factor>1.18:raise RuntimeError(f"Line too long for scene: {words} ({len(signal)/RATE:.2f}s > {slot:.2f}s). Fix acting or scene timing; do not truncate.")
            binary=process(["ffmpeg","-hide_banner","-loglevel","error","-f","f32le","-ar",str(RATE),"-ac","1","-i","pipe:0","-af","atempo="+str(round(factor+.01,4)),"-f","f32le","pipe:1"],signal.astype("<f4").tobytes())
            signal=np.frombuffer(binary,dtype="<f4").copy()
            if len(signal)>allowed:raise RuntimeError("Tempo adjusted but cue still overruns")
        fade=min(800,len(signal)//3)
        if fade:
            signal[:fade]*=np.linspace(0,1,fade,dtype=np.float32)
            signal[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)
        begin=round(start*RATE)
        tracks[role][begin:begin+len(signal)]+=signal
        cues.append({"role":role,"start_seconds":start,"duration_seconds":round(len(signal)/RATE,3),"text":words})
    joined=sum(tracks.values())
    peak=float(np.max(np.abs(joined)))
    if peak>.88:
        scale=.88/peak
        joined*=scale
        for role in tracks:tracks[role]*=scale
    files={}
    for role,signal in tracks.items():
        dest=out/("english_"+role+"_90s_48k.wav")
        wav(dest,signal)
        files[role]={"name":dest.name,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest()}
    voices=out/"ENGLISH_DIALOGUE_DRAFT_48K_NOT_FINAL.wav"
    wav(voices,joined)
    if not args.no_mix:
        project=base.parent
        bed=project/"output/soundscape/TEMP_90S_MIX_NO_VOICES_NOT_FINAL.wav"
        if not bed.is_file():
            process([sys.executable,str(project/"scripts/soundscape_90s.py"),"--out",str(bed.parent)])
        process(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(bed),"-i",str(voices),
                 "-filter_complex","[0:a]volume=0.86[bed];[1:a]asplit=2[v][key];[bed][key]sidechaincompress=threshold=0.018:ratio=8:attack=20:release=400[duck];[duck][v]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.85[out]",
                 "-map","[out]","-ar","48000","-ac","2","-c:a","aac","-b:a","256k","-t","90",str(out/"ENGLISH_VOICE_SFX_DRAFT_NOT_FINAL.m4a")])
    qa={"backend":backend,"actual_hardware":hw,"gpu_used":hw["device"]!="cpu",
        "film_seconds":90,"english_cues":cues,"tracks":files,
        "reference_sources":{role:hashlib.sha256(p.read_bytes()).hexdigest() for role,p in (refs or {}).items()},
        "release_approved":False,"voice_approval":"Pending human artistic and licensing review"}
    (out/"voice_render_qa.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"DRAFT","backend":backend,"hardware":hw,"cues":len(cues),"output":str(out)},indent=2))
if __name__=="__main__":main()
