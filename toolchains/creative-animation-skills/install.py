#!/usr/bin/env python3
"""Source-pinned skills installer. Copies only; never executes upstream scripts."""
import argparse, hashlib, json, re, shutil, subprocess, tempfile, zipfile
from pathlib import Path

PACKS={
"tiktok-video-skills":"2a775336b5a638cbf8a61dbd785f9a1b649be016",
"text-message-video-skills":"3a800e1e9b9635fa196a07b0143c80f7e9648558",
"youtube-video-skills":"f3df381d65abe5078f5ed410bbc3ed72e7cb92bd",
"ecommerce-video-skills":"2bd0dd19c9b2df5230f5d8f7453861b9681e49b4",
"ad-video-skills":"0de0f2a1c1f42a98103fc0ec436509276428372c",
"data-animation-skills":"8ce2709c3992490251e8a991535b1945f01c6865",
"explainer-video-skills":"3e2d411b725d9a72939cf8e5eb81579e751373e7",
"map-animation-skills":"390ca98bbcf2ea88a430a69c0dcbf423e43d075d",
"web-animation-skills":"b6dba3eb759726845a44163ff0bad70dd9e7fbb6",
"motion-design-skills":"3c129f769d90a1328c209c386492333c9ac62312",
"kinetic-typography-skills":"fccc94bd325d824235ee9e715e65abde57b6513a",
"freelance-motion-skills":"d85c2b484693d0387333c778d9c95230fa1856ce",
"webgl-animation-skills":"50697d659fbf70152f48f9f8aadf1efe78bbdde1",
"manim-skills":"a15833c44de5108a3ee68f178a1fca126aa7c6d8",
"generative-illustration-skills":"e7d62437c875fc8ad5eff6e90fe0e25b30e43933",
"javascript-animation-skills":"f7d0882a313249cbd43f0e4e9e209b1622870253",
"lower-thirds-skills":"aa8ef7ed9fa59d0a79fc57701e493cfd8197b5d8",
"b-roll-skills":"a51e34b0a8def533759373733bde1869c21075fb"}
BLENDER_SHA="b2f0f816d320b56ae86d52597a35284e0e6cc929"
HOSTS={"codex":".agents/skills","claude":".claude/skills",
       "antigravity":".agent/skills","gemini":".gemini/skills"}
BLOCK={".git","node_modules","__pycache__",".env",".DS_Store"}

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:raise RuntimeError("COMMAND FAILED "+repr(cmd)+" "+p.stderr[-1500:])
    return p.stdout.strip()

def checkout(repo,sha,work):
    root=work/repo.replace("/","_")
    root.mkdir(parents=True)
    run(["git","init","-q",str(root)])
    run(["git","-C",str(root),"remote","add","origin","https://github.com/"+repo+".git"])
    run(["git","-C",str(root),"fetch","--quiet","--depth=1","--no-tags","origin",sha])
    run(["git","-C",str(root),"checkout","--quiet","--detach","FETCH_HEAD"])
    assert run(["git","-C",str(root),"rev-parse","HEAD"])==sha
    print("PINNED",repo,sha,flush=True)
    return root

def copy(src,dest):
    if src.is_symlink():raise RuntimeError("Refuse symlink "+str(src))
    if src.is_file():
        if src.stat().st_size>12_000_000:raise RuntimeError("File too large "+str(src))
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dest)
    else:
        dest.mkdir(parents=True,exist_ok=True)
        for child in src.iterdir():
            if child.name in BLOCK or child.name.startswith(".env"):continue
            copy(child,dest/child.name)

def put_skill(src,dest,name):
    if dest.exists():raise RuntimeError("Refusing overwrite/collision "+str(dest))
    copy(src,dest)
    doc=dest/"SKILL.md"
    text=doc.read_text(encoding="utf8")
    if not text.startswith("---\n"):raise RuntimeError("Missing frontmatter "+str(doc))
    m=re.search(r"(?m)^name:\s*.+$",text.split("---",2)[1])
    if m and m.group().split(":",1)[1].strip()!=name:
        text=re.sub(r"(?m)^name:\s*.+$", "name: "+name, text,count=1)
        doc.write_text(text,encoding="utf8")

def gather(work,dest,blender):
    records=[]
    for pack,sha in PACKS.items():
        src=checkout("iart-ai/"+pack,sha,work)
        for f in sorted((src/"skills").glob("*/SKILL.md")):
            name="tiktok-lower-thirds" if pack=="tiktok-video-skills" and f.parent.name=="lower-thirds" else f.parent.name
            put_skill(f.parent,dest/"skills"/name,name)
            records.append({"name":name,"upstream":"iart-ai/"+pack,"sha":sha,
                            "kind":"motion","license":"MIT - umbrella project and pack documentation"})
        if (src/"LICENSE").is_file():
            copy(src/"LICENSE",dest/"notices"/(pack+".LICENSE"))
    if sum(r["kind"]=="motion" for r in records)!=55:
        raise RuntimeError("Expected all 55 motion skills")
    if blender:
        src=checkout("kevinbadi/blender-skills",BLENDER_SHA,work)
        # No repository LICENSE at this version. Only pull directly to requested
        # local project: never redistribute these files in the public artifact.
        for f in sorted(src.glob("*/SKILL.md")):
            put_skill(f.parent,dest/"skills"/f.parent.name,f.parent.name)
            records.append({"name":f.parent.name,"upstream":"kevinbadi/blender-skills",
                            "sha":BLENDER_SHA,"kind":"blender","license":"Unspecified"})
        if len(records)!=71:raise RuntimeError("Expected all 16 Blender skills")
    return records

def plugin_guide(path):
    path.mkdir(parents=True)
    (path/"SKILL.md").write_text("""---
name: blender-desktop-install-guide
description: Use for setup and verification of Blender, Sketchfab 1.8.0, Blender MCP, and third-party Blender skills.
---

# Blender installation guidance

This is an independently authored guide, not an active local Blender connection.
Source for 16 Blender workflow skills: https://github.com/kevinbadi/blender-skills
The upstream repository has no top-level LICENSE in the audited revision; use
the installer to fetch the original files directly to the authorized user's
machine, never redistribute them as part of this private ChatGPT skill bundle.

Sketchfab Blender plug-in 1.8.0 official release:
https://github.com/sketchfab/blender-plugin/releases/tag/1.8.0

ZIP SHA256: a6be9e8348a67b66faa236c7aba4c4980db0bda76ab5db17eddd077f66ca71d7
Install in Blender > Edit > Preferences > Add-ons > Install from Disk.
Then enable Sketchfab Plugin and authenticate within Blender. Never collect
Sketchfab credentials in prompts. Blender MCP server and add-on must be set up
separately on the user's own desktop, with their consent.
Image-to-3D in the kevinbadi pack requires a Meshy API key/possibly paid usage.
Do not pretend an external desktop tool is connected solely because a skill exists.
""",encoding="utf8")

def archive(root,out):
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():z.write(p,str(p.relative_to(root.parent)).replace("\\","/"))

def pack(work,out):
    folder=out/"creative-motion-skills-55"
    records=gather(work,folder,False)
    plugin_guide(folder/"skills"/"blender-desktop-install-guide")
    manifest={
      "$schema":"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
      "name":"creative-motion-skills-55","version":"1.0.0",
      "description":"55 iart.ai motion/animation workflow skills and an original Blender setup guide.",
      "author":{"name":"iart.ai (skills); private packaging by user"},
      "license":"MIT","homepage":"https://github.com/iart-ai/motion-skills",
      "extensions":{"com.openai":{"interface":{
        "displayName":"Creative Motion Skills 55",
        "shortDescription":"55 motion design workflows",
        "longDescription":"Reusable Three.js, video, motion graphics, editing, and verification skill files. Optional desktop software must be installed separately.",
        "developerName":"iart.ai / Private adaptation",
        "category":"Productivity","capabilities":[],
        "defaultPrompt":"Choose the appropriate creative motion skill and verify the output, preserving my licensed sources."
      }}}
    }
    (folder/"plugin.json").write_text(json.dumps(manifest,indent=2)+"\n")
    (folder/"SOURCE_LOCK.json").write_text(json.dumps(records,indent=2)+"\n")
    target=out/"creative-motion-skills-55.zip"
    archive(folder,target)
    return {"packaged_motion":55,"ChatGPT_blender_install_guide":1,
            "upstream_blender_skills_not_redistributed":16,
            "zip_bytes":target.stat().st_size}

def install(work,project,hosts):
    staging=work/"original-skills"
    rec=gather(work,staging,True)
    for host in hosts:
        if host not in HOSTS:raise ValueError("Unsupported agent: "+host)
        dest=project/HOSTS[host]
        for src in sorted((staging/"skills").iterdir()):
            if (dest/src.name).exists():raise RuntimeError("Skill already exists; leave untouched: "+str(dest/src.name))
            copy(src,dest/src.name)
        print("INSTALLED",len(rec),host,str(dest),flush=True)
    report={"installed":len(rec),"motion":55,"blender":16,"hosts":hosts,
            "sketchfab_addon":"Install the separately SHA256-verified official ZIP in Blender GUI",
            "blender_mcp":"Requires separate desktop add-on + MCP connection",
            "meshy":"Requires separate API key","sources":rec}
    (project/"creative-skill-install-audit.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    a=argparse.ArgumentParser()
    a.add_argument("command",choices=["package","install"])
    a.add_argument("--output",default="dist")
    a.add_argument("--project",default=".")
    a.add_argument("--hosts",default="codex,claude,antigravity,gemini")
    args=a.parse_args()
    if not shutil.which("git"):raise SystemExit("Git CLI required.")
    with tempfile.TemporaryDirectory(prefix="motion-skill-install-") as tmp:
        work=Path(tmp)
        if args.command=="package":
            out=Path(args.output).resolve()
            out.mkdir(parents=True,exist_ok=True)
            res=pack(work,out)
            (out/"install_audit.json").write_text(json.dumps(res,indent=2)+"\n")
        else:
            res=install(work,Path(args.project).resolve(),args.hosts.split(","))
        print("SUCCESS",json.dumps(res))
if __name__=="__main__":main()
