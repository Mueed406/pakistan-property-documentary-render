#!/usr/bin/env python3
"""YouTube Agent Studio v4 -- checkpointed, truthful documentary production conductor.

Standard library only; FFprobe is required for media QC. This CLI prepares,
preflights, checks, and packages productions. The proven PPG scene renderer is
invoked only by an explicit, approved GitHub Actions workflow, NOT by 'init'.
Other subjects require authored factual scene packages; never silently reuse
PPG's 50 hardcoded cues, original narration or visuals.

Quick start:
 python studio_cli.py documentary init --project projects/new-film --title "Title" --minutes 7
 python studio_cli.py documentary status --project projects/new-film
 python studio_cli.py documentary preflight --project projects/new-film
 python studio_cli.py documentary qc --project projects/new-film --video film.mp4
 python studio_cli.py documentary package --project projects/new-film --video film.mp4
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

FORMAT_VERSION = 4
STAGES = ("research", "factcheck", "script", "rights", "narration", "storyboard",
          "preview", "render", "qc", "upload")
VALID_MODES = ("free", "hybrid", "premium")
STYLE = "archival-editorial-2.5d"
ROOT = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def load(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"Missing required project file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def project(root: str) -> tuple[Path, dict]:
    folder = Path(root).expanduser().resolve()
    p = load(folder / "project.json")
    if p.get("schema") != FORMAT_VERSION:
        raise ValueError("Project schema mismatch; never auto-rewrite a different schema")
    return folder, p


def sha(path: Path) -> str:
    dig = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            dig.update(block)
    return dig.hexdigest()


def fingerprint(inputs: list[Path], opts: dict) -> str:
    """Hash inputs+settings; never reuse a different render configuration."""
    dig = hashlib.sha256(json.dumps(opts, sort_keys=True).encode())
    for p in sorted(inputs, key=str):
        if not p.is_file():
            raise FileNotFoundError(f"Cannot fingerprint absent input {p}")
        dig.update(str(p.name).encode()); dig.update(sha(p).encode())
    return dig.hexdigest()


def ffprobe(video: Path) -> dict:
    if not video.is_file() or video.stat().st_size < 4096:
        raise FileNotFoundError(f"Actual playable media file absent or tiny: {video}")
    if not shutil.which("ffprobe"):
        raise RuntimeError("FFprobe not installed; media not verified")
    p = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                        "-of", "json", str(video)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=90)
    if p.returncode:
        raise RuntimeError(f"FFprobe failed: {p.stderr[-1000:]}")
    return json.loads(p.stdout)


def validate_video(path: Path, spec: dict, *, preview: bool = False) -> dict:
    meta = ffprobe(path)
    vs = [s for s in meta["streams"] if s.get("codec_type") == "video"]
    au = [s for s in meta["streams"] if s.get("codec_type") == "audio"]
    if len(vs) != 1 or not au:
        raise ValueError("Expected one video stream and at least one actual audio stream")
    v = vs[0]
    duration = float(meta["format"]["duration"])
    expected = int(spec["duration_seconds"])
    rawfps = v.get("avg_frame_rate") or v.get("r_frame_rate", "0/1")
    if "/" in rawfps:
        a, b = rawfps.split("/", 1)
        fps = float(a) / max(1.0, float(b))
    else:
        fps = float(rawfps)
    width, height = int(v.get("width", 0)), int(v.get("height", 0))
    issues = []
    if not preview and abs(duration - expected) > 1.0:
        issues.append(f"Duration {duration:.3f}s is not target {expected}s (+/-1s)")
    if (width, height) != (spec["width"], spec["height"]):
        issues.append(f"Output size {width}x{height} disagrees with project")
    if abs(fps - spec["fps"]) > 0.10:
        issues.append(f"Actual FPS {fps:.3f} disagrees with {spec['fps']}")
    if v.get("codec_name") != "h264":
        issues.append(f"Expected H.264, got {v.get('codec_name')}")
    if not any(s.get("codec_name") == "aac" for s in au):
        issues.append("AAC audio track missing")
    result = {"file": str(path.resolve()), "bytes": path.stat().st_size,
              "sha256": sha(path), "duration": round(duration, 3),
              "resolution": [width, height], "fps": round(fps, 3),
              "video_codec": v.get("codec_name"),
              "audio_codecs": [s.get("codec_name") for s in au],
              "observed_frames": v.get("nb_frames"), "issues": issues,
              "passed": not issues, "checked_at": now()}
    return result


def init(args) -> None:
    folder = Path(args.project).expanduser().resolve()
    if folder.exists() and any(folder.iterdir()):
        raise FileExistsError(f"Project directory isn't empty: {folder}")
    if not 1 <= args.minutes <= 90:
        raise ValueError("Choose a duration between 1 and 90 minutes")
    folder.mkdir(parents=True, exist_ok=True)
    spec = {
        "schema": FORMAT_VERSION, "id": re.sub(r"[^a-z0-9-]", "-",
                                                  folder.name.lower()).strip("-"),
        "title": args.title, "created_at": now(), "duration_seconds": args.minutes * 60,
        "width": 1920, "height": 1080, "fps": 60, "aspect_ratio": "16:9",
        "language": args.language, "production_mode": args.mode, "style": STYLE,
        "editing": {
            "motion_first": True, "full_screen_animation_allowed": True,
            "continuous_stock_overlay_required": False,
            "native_graphics_fps": 60, "paper_cutouts": True,
            "stop_motion_microcycles": True, "type_variation": True,
            "story_synced_arrows": True, "no_fabricated_evidence": True},
        "source_template": args.template, "voice_provider": "existing-or-approved",
        "premium_generation_allowed": False, "premium_budget_credits": 0,
        "youtube": {"channel_id": None, "visibility": "private",
                    "auto_publish": False, "title": args.title,
                    "description": "", "tags": [], "made_for_kids": None},
        "inputs": {"source_video": None, "transcript": None, "timed_srt": None,
                   "narration": None, "music": None, "license_manifest": "rights.json",
                   "scene_plan": "storyboard.json"},
        "release": {"approved_for_youtube": False, "artistic_qc_approved": False,
                    "factcheck_approved": False, "audio_approved": False}
    }
    write_json(folder / "project.json", spec)
    write_json(folder / "rights.json", {"assets": [], "verified": False,
                                        "notes": "Record source URL, license, attribution, SHA, illustrative status"})
    write_json(folder / "storyboard.json", {"chapters": [], "approved": False,
                                            "guidance": "Each chapter requires narration cue, source attribution, art, motion & time range"})
    write_json(folder / "state.json", {"stages": {x: "pending" for x in STAGES},
                                      "completed_hashes": {}, "warnings": []})
    (folder / "output").mkdir(exist_ok=True)
    print(json.dumps({"created": str(folder), "fps": 60, "minutes": args.minutes,
                      "production": "UNRENDERED", "next": "storyboard + rights + script"},
                     indent=2))


def stage_status(args):
    folder, spec = project(args.project)
    state = load(folder / "state.json")
    story = load(folder / "storyboard.json")
    rights = load(folder / "rights.json")
    counts = {k: list(state["stages"].values()).count(k) for k in ("pending", "passed", "failed")}
    print(json.dumps({"project": spec["title"], "duration": spec["duration_seconds"],
      "fps": spec["fps"], "stages": state["stages"], "counts": counts,
      "chapters": len(story.get("chapters", [])),
      "rights_assets": len(rights.get("assets", [])),
      "published": state["stages"]["upload"] == "passed"}, indent=2))


def audit_rights(rights: dict) -> list[str]:
    problems = []
    assets = rights.get("assets") or []
    if not assets:
        problems.append("No recorded licensed assets")
    for i, asset in enumerate(assets):
        for field in ("path", "source_url", "license", "sha256", "usage"):
            if not asset.get(field):
                problems.append(f"Rights asset {i} missing {field}")
        if asset.get("usage") == "actual-investigation-evidence" and not asset.get("evidence_source"):
            problems.append(f"Rights asset {i} falsely marked evidence without primary source")
    return problems


def preflight(args):
    folder, spec = project(args.project)
    rights = load(folder / "rights.json")
    story = load(folder / "storyboard.json")
    errors = audit_rights(rights)
    chapters = story.get("chapters", [])
    if not chapters:
        errors.append("No narration-anchored scene plan; storyboard must be authored")
    if not story.get("approved"):
        errors.append("Storyboard creative approval missing")
    for i, chapter in enumerate(chapters):
        for field in ("cue", "start", "duration", "visual", "fact_source"):
            if chapter.get(field) is None:
                errors.append(f"Chapter {i} lacks {field}")
    for key in ("timed_srt", "source_video", "narration"):
        path = spec["inputs"].get(key)
        if not path or not (folder / path).is_file():
            errors.append(f"Required real input unavailable: {key}")
    if args.for_publication:
        for gate, value in spec["release"].items():
            if value is not True:
                errors.append(f"Publication gate not approved: {gate}")
        if not spec["youtube"].get("channel_id"):
            errors.append("YouTube channel not selected")
    report = {"ready": not errors, "errors": errors, "checked_at": now(),
              "mode": spec["production_mode"], "premium_allowed":
              spec.get("premium_generation_allowed", False)}
    write_json(folder / "output" / "preflight.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise RuntimeError(f"Preflight blocked with {len(errors)} unmet requirements")


def qc(args):
    folder, spec = project(args.project)
    result = validate_video(Path(args.video), spec, preview=args.preview)
    write_json(folder / "output" / "technical_qc.json", result)
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise RuntimeError("Technical QC failed. Retain previous working master.")
    state = load(folder / "state.json")
    state["stages"]["qc"] = "passed"
    state["completed_hashes"]["qc"] = result["sha256"]
    write_json(folder / "state.json", state)


def package(args):
    folder, spec = project(args.project)
    report = load(folder / "output" / "technical_qc.json")
    video = Path(args.video)
    if not report.get("passed") or not video.is_file() or report["sha256"] != sha(video):
        raise RuntimeError("No valid matching technical QC report for exact selected video")
    rights = load(folder / "rights.json")
    problems = audit_rights(rights)
    if problems or not rights.get("verified"):
        raise RuntimeError("Cannot package for publication without verified rights: " + "; ".join(problems))
    if not all(spec["release"].values()):
        raise RuntimeError("Do not label publication-ready until each human release approval is recorded")
    youtube = spec["youtube"]
    if not youtube.get("channel_id"):
        raise RuntimeError("Choose the exact owned YouTube channel before upload packaging")
    bundle = {
        "video_path": str(video.resolve()), "video_sha256": report["sha256"],
        "channel_id": youtube["channel_id"], "privacyStatus": "private",
        "title": youtube["title"], "description": youtube["description"],
        "tags": youtube["tags"], "made_for_kids": youtube["made_for_kids"],
        "approved_for_publish": False,
        "manual_review_required": True, "created_at": now()
    }
    out = folder / "output" / "youtube_private_upload_manifest.json"
    write_json(out, bundle)
    print(json.dumps({"package": str(out), "status": "PRIVATE_UPLOAD_PREPARED",
                      "upload_executed": False}, indent=2))


def reuse(args):
    folder, spec = project(args.project)
    inputs = [Path(q) for q in args.inputs]
    recipe = {"style": STYLE, "fps": spec["fps"], "stage": args.stage,
              "mode": spec["production_mode"], "extra": args.recipe}
    key = fingerprint(inputs, recipe)
    state = load(folder / "state.json")
    prev = state["completed_hashes"].get(args.stage)
    output = Path(args.output)
    valid = output.is_file() and output.stat().st_size > 4096
    if valid and output.suffix.lower() == ".mp4":
        try:
            valid = ffprobe(output).get("format", {}).get("duration") is not None
        except Exception:
            valid = False
    print(json.dumps({"cache_key": key, "unchanged": bool(prev == key),
                      "output_exists_and_healthy": valid,
                      "reuse": bool(prev == key and valid)}, indent=2))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("init", help="Create reproducible production project; no generation")
    a.add_argument("--project", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--minutes", required=True, type=int)
    a.add_argument("--mode", choices=VALID_MODES, default="free")
    a.add_argument("--language", default="ur-PK")
    a.add_argument("--template", default="new-documentary",
                   choices=("new-documentary", "ppg-410s"))
    x = s.add_parser("status", help="Read checkpoints")
    x.add_argument("--project", required=True)
    x = s.add_parser("preflight", help="Check real assets/rights/scene plan")
    x.add_argument("--project", required=True)
    x.add_argument("--for-publication", action="store_true")
    x = s.add_parser("qc", help="Probe actual MP4, never infer render success")
    x.add_argument("--project", required=True)
    x.add_argument("--video", required=True)
    x.add_argument("--preview", action="store_true")
    x = s.add_parser("package", help="Prepare PRIVATE YouTube handoff; never publish")
    x.add_argument("--project", required=True)
    x.add_argument("--video", required=True)
    x = s.add_parser("reuse", help="Check SHA256+media before skipping a render")
    x.add_argument("--project", required=True)
    x.add_argument("--stage", choices=STAGES, required=True)
    x.add_argument("--inputs", nargs="+", required=True)
    x.add_argument("--output", required=True)
    x.add_argument("--recipe", default="v4")
    args = p.parse_args(argv)
    commands = {"init": init, "status": stage_status, "preflight": preflight,
                "qc": qc, "package": package, "reuse": reuse}
    try:
        commands[args.command](args)
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError,
            subprocess.SubprocessError, OSError) as exc:
        print("PPG STUDIO BLOCKED:", str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
