#!/usr/bin/env python3
"""Read and inspect a creator-offered no-redistribution template archive safely.

No extraction or asset redistribution. The original creator remains the owner.
Use this to decide if a legally acquired pack has actual alpha-video material
that our FFmpeg pipeline can integrate, rather than merely a Premiere MOGRT.
"""
import argparse, collections, hashlib, io, json, pathlib, sys, urllib.request, zipfile
from datetime import datetime, timezone

DEFAULT = "https://pbblogassets.s3.amazonaws.com/uploads/freebies/PB-free-hand-drawn-symbols.zip"
MAX_DOWNLOAD = 600_000_000
MAX_EXPANDED = 1_500_000_000

def audit_archive(data: bytes) -> dict:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        entries=z.infolist()
        if len(entries)>1000: raise ValueError("Unusually large item count")
        expanded=sum(x.file_size for x in entries)
        if expanded>MAX_EXPANDED: raise ValueError("Expanded media exceeds size cap")
        extensions=collections.Counter(pathlib.PurePosixPath(x.filename).suffix.lower()
                                       for x in entries if not x.is_dir())
        media=[x for x in entries if pathlib.PurePosixPath(x.filename).suffix.lower()
               in (".mov",".mp4",".webm",".png",".jpg",".jpeg",".gif")]
        if not media:raise ValueError("No directly usable footage or graphics")
        for x in entries:
            if x.file_size>600_000_000: raise ValueError("Unsafe per-file size")
            p=pathlib.PurePosixPath(x.filename)
            if p.is_absolute() or ".." in p.parts:raise ValueError("Unsafe archive path")
        return {"archive_sha256":hashlib.sha256(data).hexdigest(),"entry_count":len(entries),
                "expanded_bytes":expanded,"media_count":len(media),
                "media_extensions":dict(extensions),
                "sample_media_filenames":[x.filename for x in media[:12]],
                "requires_editor":bool(extensions.get(".mogrt") or extensions.get(".prproj")),
                "licensed_for_finished_personal_commercial_video":True,
                "redistribution_of_raw_assets_allowed":False,
                "source":DEFAULT,"license_evidence":
                "https://www.premiumbeat.com/blog/free-hand-drawn-animated-shapes/"}

def safe_download(url: str) -> bytes:
    if url != DEFAULT:raise ValueError("Unapproved external URL")
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 PPG-template-compatibility-audit/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        length=r.headers.get("Content-Length")
        if length and int(length)>MAX_DOWNLOAD:
            raise ValueError("Archive larger than transfer cap")
        chunks=[];n=0
        while True:
            b=r.read(256*1024)
            if not b:break
            n+=len(b)
            if n>MAX_DOWNLOAD:raise ValueError("Exceeded bounded size cap")
            chunks.append(b)
        return b"".join(chunks)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive", help="Existing authorized ZIP file instead of downloading")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.archive:
        data=pathlib.Path(a.archive).read_bytes()
    else:data=safe_download(DEFAULT)
    report=audit_archive(data)
    report["downloaded_at"]=datetime.now(timezone.utc).isoformat()
    pathlib.Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0

if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:
        print("TEMPLATE COMPATIBILITY BLOCKED:",str(e),file=sys.stderr)
        sys.exit(2)
