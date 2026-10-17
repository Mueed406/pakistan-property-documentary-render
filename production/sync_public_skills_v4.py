#!/usr/bin/env python3
"""Copy the reviewed editorial documentary skill into the separately maintained
public Claude+ChatGPT repository without overwriting the 34 v3 skills.

Use on a checkout of islamically85-byte/youtube-agent-skill that YOU own, with
a clean working tree and an authenticated GitHub account authorized to push.
Defaults to no writes. Does NOT push/publish by itself.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

BEGIN="<!-- YOUTUBE_AGENT_STUDIO_V4_EDITORIAL_BEGIN -->"
END="<!-- YOUTUBE_AGENT_STUDIO_V4_EDITORIAL_END -->"
ADDENDUM=BEGIN+"""
## v4 Native 60 FPS Mixed-Media Editorial Documentary Extension

When the user asks to PRODUCE a documentary video, load
yt-editorial-documentary first, then use yt-studio for all pre-existing research,
audio, motion, render and packaging skills. A motion-first documentary may
intercut complete full-screen archival-collage graphics with sharp licensed
footage; do NOT require a constant footage background or a fixed >85% stock
ratio. Standard visual identity is textured paper, layered cutout photos,
cinematic parallax, type variety, factual arrows and purposeful transitions.
Native generated graphics default to 60fps; original stock retains its actual
captured motion cadence. Run license, citation, narration synchronization,
real-file FFprobe and artistic checks before calling production complete.

Use one project.json for exact duration, versioned cache, asset/right ledger,
narration-aligned scene cues, approval and upload permissions. Avoid repeatedly
researching and regenerating already successful sources and clips. A 5, 6, or
9-minute new project MUST use a script/storyboard for its own subject, not
the previous 410-second PPG case's hardcoded cue list. Use free assets unless
paid spend/credits were explicitly approved.

First YouTube upload is PRIVATE-only through separately authorized YouTube
OAuth with exact channel identity and final user approval. vidIQ media import
is NOT YouTube video publication. No automatic public visibility.
"""+END+"\n"

PUBLIC_SKILL_TARGETS=(
 "skills/yt-editorial-documentary/SKILL.md",
 "chatgpt/skills/yt-editorial-documentary/SKILL.md",
)
TARGET_ADDENDA=(
 "skills/yt-studio/SKILL.md",
 "chatgpt/skills/yt-studio/SKILL.md",
 "skills/yt-motion-graphics/SKILL.md",
 "chatgpt/skills/yt-motion-graphics/SKILL.md",
 "skills/yt-upload-prep/SKILL.md",
 "chatgpt/skills/yt-upload-prep/SKILL.md",
)


def git_clean(path:Path)->bool:
    result=subprocess.run(["git","status","--porcelain"],cwd=path,
                          text=True,capture_output=True,check=True)
    return not result.stdout.strip()


def update_between(text:str)->str:
    if BEGIN in text or END in text:
        if text.count(BEGIN)!=1 or text.count(END)!=1:
            raise RuntimeError("Previously written v4 markers corrupted; inspect manually")
        head, rest=text.split(BEGIN,1)
        _, tail=rest.split(END,1)
        return head+ADDENDUM+tail
    return text.rstrip()+"\n\n"+ADDENDUM


def synchronize(target:Path, skill:Path, apply:bool):
    if not skill.is_file():
        raise FileNotFoundError(f"Original skill source not found: {skill}")
    must=(target/"README.md",target/"skills/yt-studio/SKILL.md",
          target/"chatgpt/skills/yt-studio/SKILL.md")
    absent=[str(p) for p in must if not p.is_file()]
    if absent:
        raise RuntimeError("Not the expected dual-platform public repo: "+", ".join(absent))
    files={}
    source=skill.read_text(encoding="utf8")
    if not source.startswith("---\nname: yt-editorial-documentary"):
        raise RuntimeError("Unrecognized source skill; refusing update")
    for p in PUBLIC_SKILL_TARGETS:
        files[target/p]=source
    for p in TARGET_ADDENDA:
        file=target/p
        if not file.is_file():
            raise RuntimeError("Missing existing v3 skill "+str(file))
        files[file]=update_between(file.read_text(encoding="utf8"))
    intro=target/"README.md"
    current=intro.read_text(encoding="utf8")
    if BEGIN in current:
        files[intro]=update_between(current)
    else:
        files[intro]=current.rstrip()+"\n\n"+ADDENDUM
    report=[str(p.relative_to(target)) for p in files]
    print("Target:",target)
    print("Preview: would create/overlay",len(files),"files")
    for p in report:print(" -",p)
    if not apply:
        print("No files changed. To apply, rerun with --apply on a CLEAN checkout.")
        return
    if not git_clean(target):
        raise RuntimeError("Repository has uncommitted changes; branch/commit or stash before --apply")
    for path,body in files.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(body,encoding="utf8")
    print("Applied to local target only. Run tests, review diff, and open your own PR. Nothing pushed.")


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",type=Path,required=True,
                   help="Existing local clone of public youtube-agent-skill repository")
    p.add_argument("--skill",type=Path,
                   default=Path(__file__).resolve().parents[1]/
                   "skills/yt-editorial-documentary/SKILL.md")
    p.add_argument("--apply",action="store_true")
    x=p.parse_args(argv)
    synchronize(x.target.resolve(),x.skill.resolve(),x.apply)


if __name__=="__main__":main()
