#!/usr/bin/env bash
# Editorial 60 FPS continuity proof: original master -> new full screen paper collage -> original master.
# Audio is sourced as one unbroken range of original narration to preserve timing.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORIGINAL="$DIR/source/renders/Pakistan_Property_Premium_Pearl_24_Motion_FullHD_Review.mp4"
COLLAGE="$DIR/out/PPG_Premium_Editorial_60FPS_Review.mp4"
OUT="$DIR/out/PPG_Editorial_60FPS_Continuity_43s.mp4"
ffmpeg -hide_banner -loglevel warning -stats -y -i "$ORIGINAL" -i "$COLLAGE" \
 -filter_complex "
[0:v]trim=start=27.765:end=33.672,setpts=PTS-STARTPTS,fps=60,scale=1920:1080,fade=t=out:st=5.72:d=0.17:color=white,format=yuv420p[intro];
[1:v]setpts=PTS-STARTPTS,fps=60,fade=t=in:st=0:d=0.17:color=white,fade=t=out:st=25.43:d=0.17:color=white,format=yuv420p[paper];
[0:v]trim=start=59.272:end=71,setpts=PTS-STARTPTS,fps=60,scale=1920:1080,fade=t=in:st=0:d=0.17:color=white,format=yuv420p[outro];
[intro][paper][outro]concat=n=3:v=1:a=0[v];
[0:a]atrim=start=27.765:end=71,asetpts=PTS-STARTPTS[a]" \
 -map '[v]' -map '[a]' -c:v libx264 -threads 4 -preset veryfast -crf 19 -r 60 \
 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "CONTINUITY_MP4_COMPLETE: $OUT"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,avg_frame_rate -of json "$OUT"