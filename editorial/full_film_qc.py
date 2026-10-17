#!/usr/bin/env python3
"""Full documentary engineering QC: duration, audio, subtitles, 1080p, representative
frames, visual diversity, black frames, and artifact review contact sheet.
No perceptual claim of "flawless" video: human Urdu listening and art QC needed.
"""
import argparse,subprocess,json,re,hashlib
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageStat

def proc(argv):
 r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-2500:])
 return r.stdout

def media(path):
 return json.loads(proc(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))

def main(file,srt,out):
 path=Path(file);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 metadata=media(path);tracks=metadata.get("streams",[])
 v=next((x for x in tracks if x.get("codec_type")=="video"),None)
 a=next((x for x in tracks if x.get("codec_type")=="audio"),None)
 seconds=float(metadata["format"]["duration"])
 if not v or not a or not (359<=seconds<=428):raise RuntimeError("Missing streams / runtime invalid")
 if v.get("width")!=1920 or v.get("height")!=1080:raise RuntimeError("Invalid video frame dimensions")
 num,den=(int(x) for x in v.get("avg_frame_rate","25/1").split("/"))
 fps=num/den
 if not 24.9<=fps<=25.1:raise RuntimeError("Not 25fps constant master")
 if path.stat().st_size<22_000_000:raise RuntimeError("Encoded MP4 suspiciously tiny for full 1080p feature")
 subtitles=Path(srt).read_text(encoding="utf-8-sig")
 cues=subtitles.count("-->")
 if cues<35:raise RuntimeError("SRT missing most Urdu captions")
 images=[];hashes=[];black=[];low_contrast=[]
 for i in range(18):
  t=6+((seconds-15)*i/17)
  p=out/f"review_{i:02}.jpg"
  proc(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.3f}","-i",str(path),
        "-frames:v","1","-vf","scale=480:270:flags=lanczos","-q:v","2",str(p)])
  with Image.open(p) as raw:
   img=raw.convert("RGB")
   stat=ImageStat.Stat(img.convert("L"))
   if stat.mean[0]<11:black.append({"second":round(t,1),"luma":round(stat.mean[0],1)})
   if stat.stddev[0]<9:low_contrast.append({"second":round(t,1),"luma_std":round(stat.stddev[0],1)})
   digest=hashlib.sha256(img.resize((64,36)).tobytes()).hexdigest()
   hashes.append(digest);images.append((t,img.copy()))
 if len(set(hashes))<14:raise RuntimeError("Too many identical images in sampled footage")
 if len(black)>2:raise RuntimeError("Likely blank/black frames exceed safety threshold")
 sheet=Image.new("RGB",(4*480,5*304),(15,22,31))
 painter=ImageDraw.Draw(sheet)
 for j,(time,img) in enumerate(images):
  x=(j%4)*480;y=(j//4)*304
  sheet.paste(img,(x,y))
  painter.text((x+9,y+275),f"Time: {time/60:.2f} min / sample {j+1}",fill=(239,233,219))
 sheet_path=out/"full_review_contact_sheet.jpg"
 sheet.save(sheet_path,quality=94,subsampling=0)
 report={"file":str(path),"duration_seconds":seconds,"resolution":[1920,1080],
         "fps":fps,"audio_codec":a.get("codec_name"),"video_codec":v.get("codec_name"),
         "bitrate":int(metadata["format"].get("bit_rate","0")),"size_bytes":path.stat().st_size,
         "subtitle_cues":cues,"sample_frames":len(images),
         "unique_sampled_frames":len(set(hashes)),"dark_frame_samples":black,
         "low_contrast_samples":low_contrast,"contact_sheet":str(sheet_path),
         "creative_checks_still_needed":["Voice naturalness","Pakistani Urdu pronunciation",
          "Correctly attributed allegations","Shot-to-narration match","Professional art direction",
          "Stock imagery location authenticity","Subtitles timing during motion cutaways"]}
 (out/"full_engineering_qc.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
 print("PASS TECHNICAL FEATURE QC",json.dumps(report,ensure_ascii=False)[:1300],flush=True)

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--video",required=True);p.add_argument("--srt",required=True);p.add_argument("--out",default="renders/review_qc")
 a=p.parse_args()
 main(a.video,a.srt,a.out)
