#!/usr/bin/env python3
"""Official YouTube Data API v3, PRIVATE-only resumable upload for approved videos.

NOT a vidIQ video_upload call. Cannot reuse vidIQ's OAuth session. Requires
independently authorized YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and
YOUTUBE_REFRESH_TOKEN stored as encrypted GitHub Actions Secrets. No interactive
passwords, browser cookies, or credentials in the repository.

Never executes upload without --execute, --channel-id and an approved manifest.
For other visibility levels, review and publish in YouTube Studio manually.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys
import time


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",required=True)
    p.add_argument("--execute",action="store_true",
                   help="Authorize actual PRIVATE upload; omitted = safe dry run")
    p.add_argument("--channel-id",required=True,
                   help="Exact authorized target channel ID")
    p.add_argument("--receipt",default="youtube_private_upload_receipt.json")
    a=p.parse_args(argv)
    manifest=json.loads(Path(a.manifest).read_text(encoding="utf8"))
    video=Path(manifest["video_path"])
    if not video.is_file() or video.stat().st_size<500000:
        raise SystemExit("A real validated video file must exist before YouTube upload.")
    if manifest.get("channel_id")!=a.channel_id:
        raise SystemExit("Channel does not match approved manifest.")
    if manifest.get("privacyStatus")!="private":
        raise SystemExit("Safety restriction: initial uploads must be PRIVATE.")
    if manifest.get("approved_for_publish") is not True:
        raise SystemExit("Manifest needs explicit approval for upload; no publication.")
    if manifest.get("made_for_kids") is None:
        raise SystemExit("Set the real made-for-kids classification before upload.")
    title=manifest.get("title","").strip()
    if not 1<=len(title)<=100 or not manifest.get("description","").strip():
        raise SystemExit("A verified title and complete description are required.")
    receipt=Path(a.receipt)
    if receipt.is_file():
        raise SystemExit("Upload receipt already exists. Check the existing YouTube video; do not duplicate.")
    if not a.execute:
        print(json.dumps({"status":"dry-run", "video":str(video), "bytes":video.stat().st_size,
                          "channel":a.channel_id, "privacy":"private", "network_called":False},indent=2))
        return 0

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    env=("YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN")
    missing=[k for k in env if not os.environ.get(k)]
    if missing:
        raise SystemExit("Upload blocked: missing OAuth secrets "+", ".join(missing))
    creds=Credentials(
        token=None,refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.readonly"]
    )
    creds.refresh(Request())
    yt=build("youtube","v3",credentials=creds,cache_discovery=False)
    own=yt.channels().list(part="id,snippet",mine=True).execute()
    channels=[x["id"] for x in own.get("items",[])]
    if a.channel_id not in channels:
        raise SystemExit("Connected OAuth identity is not the approved YouTube channel.")

    body={
        "snippet":{"title":title,"description":manifest["description"],
                   "tags":manifest.get("tags") or [],
                   "categoryId":"25","defaultLanguage":"ur"},
        "status":{"privacyStatus":"private",
                  "selfDeclaredMadeForKids":bool(manifest["made_for_kids"])}
    }
    media=MediaFileUpload(str(video),chunksize=16*1024*1024,
                          mimetype="video/mp4",resumable=True)
    request=yt.videos().insert(part="snippet,status",body=body,media_body=media)
    result=None
    transient={429,500,502,503,504}
    consecutive_failures=0
    while result is None:
        try:
            progress,result=request.next_chunk()
            consecutive_failures=0
            if progress:
                print("YOUTUBE UPLOAD",round(progress.progress()*100,1),"percent",flush=True)
        except HttpError as exc:
            if exc.resp.status not in transient or consecutive_failures>=5:
                raise
            consecutive_failures+=1
            time.sleep(min(60,2**consecutive_failures))
    if not result or not result.get("id"):
        raise RuntimeError("YouTube upload returned no video ID; verify before retry.")
    data={"status":"uploaded","videoId":result["id"],
          "url":"https://www.youtube.com/watch?v="+result["id"],
          "channelId":a.channel_id,"privacy":"private",
          "receivedTitle":(result.get("snippet") or {}).get("title"),
          "sourceFile":str(video),"uploaded_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
    receipt.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    print(json.dumps(data,indent=2))
    return 0


if __name__=="__main__":
    sys.exit(main())
