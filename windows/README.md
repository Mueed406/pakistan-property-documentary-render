# AI Documentary Studio — Windows CLI

This folder contains an **actual scriptable local production stack**, not a GUI-only list.

To INSTALL on your own Windows 10/11 computer, open **PowerShell as yourself** (administrator only if your WinGet installation asks) at the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\windows\Install-Studio.ps1 -Install
```

To audit without changing anything:

```powershell
powershell -ExecutionPolicy Bypass -File .\windows\Verify-Studio.ps1
```

Optional GUI programs (manual review, not core AI automation): add `-WithShotcut` and/or `-WithAudacity`. Installers use signed/community-reviewed **WinGet** manifests where available; *not* random scripts or download mirrors.

## What runs headless

- Blender 4.5 LTS (version explicitly requested) — `blender -b scene.blend -a` and Python API (3D, cameras, high-quality lighting)
- FFmpeg/FFprobe — source ingest, trimming, color management, subtitle muxing, loudness/QC, exporting
- Node LTS + Remotion — React/TypeScript motion graphics and narration-driven animated overlays (individuals/teams <=3 free; verify eligibility).
- Python 3.11 + Spotify Pedalboard — EQ, compressor, true-peak-safe limiting, audio mastering
- OpenTimelineIO — editorial decisions and exportable structured timelines.
- Inkscape CLI — original vector elements and layout helpers, **not** unrelated icon packs.

### Avoid software that doesn't add dependable AI automation

DaVinci Resolve is valuable for a human colorist but **not** required for this no-GPU fully headless pipeline. Shotcut is optional for manual finishing, and its `melt` MLT XML export requires separate tests. Audacity's UI scripting is not a core dependable cross-platform renderer. Do not install paid Adobe, unlicensed plugins, or OS-specific binary effects for no reason.

### Important
This chat and the GitHub Linux runner cannot install programs on your PC directly. This installer runs only when you execute it locally. On GitHub, the `windows-latest` CI validates Python and Node compatibility separately and does not install arbitrary software into your computer.

**License**: Remotion is free for individuals and organizations of up to three people; larger organizations may need a company license. Confirm the eligibility before commercial video production. See https://www.remotion.dev/docs/license/pricing .

**No hidden costs**: no Gemini calls, subscriptions, or YouTube publication. Gemini key remains in GitHub Actions secrets; never paste in source.

**Creative QC**: A technical MP4 render is NOT proof of professional art direction; compare frames, listen to narration, and correct shots before publication.
