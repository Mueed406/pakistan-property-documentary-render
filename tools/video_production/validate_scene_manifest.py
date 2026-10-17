#!/usr/bin/env python3
"""Read-only, standard-library production planning and rights validator.

Usage:
  python tools/video_production/validate_scene_manifest.py
  python tools/video_production/validate_scene_manifest.py --render-ready

Default = validate plan only; --render-ready intentionally FAILS until actual
authorized media exists, hashes match and explicit rights approvals are set.
This script never downloads proprietary game data or calls paid services.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / "templates/fan-animation/poppy_90s_scene_manifest.json"
DEFAULT_ASSETS = ROOT / "templates/fan-animation/poppy_asset_source_registry.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()


def validate(plan, registry, *, render_ready=False, root=ROOT):
    errors = []
    fpsn = plan.get("framerate_num")
    fpsd = plan.get("framerate_den")
    frames = plan.get("frame_count")
    shots = plan.get("shots", [])
    if (fpsn, fpsd) != (60, 1):
        errors.append("Project should specify exact integer 60fps")
    if not isinstance(frames, int) or frames <= 0:
        errors.append("frame_count must be a positive integer")
    if not isinstance(shots, list) or not shots:
        errors.append("No shots specified")
    if plan.get("final_width") != 1080 or plan.get("final_height") != 1920:
        errors.append("Manifest must use requested vertical 1080x1920 output")
    if frames and plan.get("duration_seconds") != frames / 60:
        errors.append("Duration does not equal frames / 60")

    lookup = {a.get("id"): a for a in registry.get("assets", [])}
    if None in lookup or len(lookup) != len(registry.get("assets", [])):
        errors.append("Missing or duplicate asset registry IDs")
    expected = 0
    shot_ids = set()
    active = set()
    for shot in shots:
        sid = shot.get("id", "")
        if sid in shot_ids:
            errors.append("Duplicate shot ID " + sid)
        shot_ids.add(sid)
        start, count = shot.get("start_frame"), shot.get("frame_count")
        if not isinstance(start, int) or not isinstance(count, int) or count <= 0:
            errors.append(sid + " has invalid frame coordinates")
            continue
        if start != expected:
            errors.append(f"{sid} has gap or overlap at {expected} (found {start})")
        if shot.get("end_frame_exclusive") != start + count:
            errors.append(sid + " invalid exclusive end frame")
        if shot.get("start_seconds") != start / 60:
            errors.append(sid + " start_seconds not frame aligned")
        if shot.get("duration_seconds") != count / 60:
            errors.append(sid + " duration_seconds not frame aligned")
        if not shot.get("camera_intent") or not shot.get("animation_actions"):
            errors.append(sid + " missing camera/animation instructions")
        for key in shot.get("required_asset_keys", []):
            if key not in lookup:
                errors.append(sid + " references unknown asset " + key)
            active.add(key)
        if not shot.get("required_asset_keys"):
            errors.append(sid + " missing required asset keys")
        expected = start + count
    if expected != frames:
        errors.append(f"Timeline ends at frame {expected}; expected {frames}")

    if render_ready:
        for key in sorted(active):
            a = lookup.get(key, {})
            if not a.get("approved_for_project"):
                errors.append(key + " not approved for this project")
            if a.get("status") not in ("ACQUIRED", "ORIGINAL_CREATED"):
                errors.append(key + " has no acquired/created asset status")
            file_path = a.get("actual_file")
            expected_hash = a.get("sha256")
            if not file_path or not expected_hash:
                errors.append(key + " missing file and verified SHA256")
                continue
            path = (root / file_path).resolve()
            if not path.is_relative_to(root.resolve()):
                errors.append(key + " path outside the project")
            elif not path.is_file() or sha256(path) != expected_hash:
                errors.append(key + " missing file or SHA256 mismatch")
            if not a.get("license_url") and not a.get("owner"):
                errors.append(key + " license / creator source unverified")
    return {"ok": not errors, "mode": "RENDER_READY" if render_ready else "PLAN_ONLY",
            "frames": frames, "seconds": plan.get("duration_seconds"),
            "fps": "60/1", "shot_count": len(shots), "asset_keys_used": len(active),
            "errors": errors, "media_generated": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenes", type=Path, default=DEFAULT_PLAN)
    p.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    p.add_argument("--render-ready", action="store_true")
    opts = p.parse_args()
    report = validate(json.loads(opts.scenes.read_text(encoding="utf8")),
                      json.loads(opts.assets.read_text(encoding="utf8")),
                      render_ready=opts.render_ready)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
