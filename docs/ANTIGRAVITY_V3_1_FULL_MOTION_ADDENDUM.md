# V3.1 Antigravity addendum — actual 6m50 movie, eight HTML chapters, new skills and QA

Apply this addendum to the existing complete prompt:
https://github.com/Mueed406/pakistan-property-documentary-render/blob/main/docs/ANTIGRAVITY_MOTION_SKILLS_V3_PROMPT.md

DO NOT claim this file has updated islamically85-byte/youtube-agent-skill until an authorized push/PR actually succeeds.

## New VERIFIED production infrastructure

- Baseline 410.4-second 1080p documentary (79 moving shots / 28 real-stock sources): GitHub Actions run 38962816235, audio is *Piper* and requires narrator approval.
- Deterministic browser/FFmpeg engine: browser_motion/render.mjs + full_documentary_scenes.html, containing eight genuinely independent 7.5-second explainers (file-count reveal, land-vs-file, physical parcel map, building concept, evidence trail, approvals, buyer checks, conclusion).
- Full 6:50 motion-enhanced feature assembly: browser_motion/full_documentary_assemble.py + .github/workflows/render-full-browser-documentary.yml. It downloads source footage from old verified run, renders every motion clip at 1920×1080 / 25 fps, and composes the entire film while preserving original audio.
- Full film QC: editorial/full_film_qc.py and .github/workflows/qc-full-browser-documentary.yml. Auto-downloads successful master, tests subtitles, audio, dimensions, video diversity, black frames, timing, and produces an 18-frame contact sheet.
- Windows agent CLI: studio_cli.py render-full-browser with --base, --srt, --out; no need for proprietary After Effects/Adobe app to render.

## Six EXTRA skills, installation actually tested on GitHub

iart-ai/motion-design-skills (MIT):
1. motion-art-direction
2. shot-composition
3. beat-sync-editing

heygen-com/hyperframes (Apache 2.0):
4. hyperframes-animation
5. hyperframes-cli
6. faceless-explainer

Successful install verification: https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38995968666

Earlier two installed and tested:
- JakeB-5/motion-graphic-skill (MIT)
- haidrrrry/claude-remotion-skill (MIT)
Successful prior install: run 38994372728.

Optional /motion by abhimahamkali: repository contained no explicit LICENSE during audit, thus do not vendor source into MIT releases. Only optional upstream installation to local agent after user selects it.

Windows installer now supports:
```powershell
.\windows\Install-MotionSkills.ps1 -Install -Global -Advanced
```
This installs eight third-party skills in the local Claude/Codex environment, not inside ChatGPT cloud or automatically in the public skills repo.

## New production quality gates

- Stop treating 18-frame smoke tests as delivered videos. Publish duration, frame count and MP4 size accurately.
- Use “Premium” motion personality: one restrained easing family (350–600ms), no bouncy CSS dashboard effects; one hero focal point per frame, 12-column grid/safe title margins, 3-depth-layer composition, calm investigative pacing, purposeful cuts at actual narration cues.
- Avoid generic repeated cards; motion concepts must change with subject. 3D architecture from properly licensed Blender models; CSS perspective can illustrate numbers but may not be called photoreal architecture.
- Keep claims legally hedged; numbers are reported allegations, do not label conceptual maps as real sites. Preserve receipts/source evidence distinction.
- Voice: baseline uses Piper synthetic Urdu with audible robotic defects. Gemini 2.5 Flash TTS has passed ONE authorized sample in run 38973775642. Actual full-length Gemini replacement has not been approved or executed yet. Do not silently spend money on unverified billing-enabled keys.
- Quality verdict requires technical encoder success PLUS real voice listening, motion contact sheet, source license manifest and fact-check.
- Browser animation source remains editable HTML (deterministic per-frame time), film exports H.264/FFmpeg, keep 1080p 25fps original audio in picture lock.
- Prefer original/legally licensed sound over random Pixabay tracks that may produce Content ID claims.
- Show exactly 3 creator options only when selecting real video production: Free local $0 extra API spend, Hybrid value with Gemini free-tier/approved money, vidIQ Premium with real balance+credits check. Current account’s credit state must be retrieved at execution, never hardcoded.

## Deliverables for v3.1

Make a NEW pull request after old PR#1 merged. Integrate new browser-motion studio skills into BOTH Claude and ChatGPT editions, update release builder ZIPs, tests and docs. Preserve existing flows. Don't claim anything was deployed to ChatGPT until the private plugin actually updates. Use the new full-video workflow to verify the real MP4 before release.

Call out any missing permission/credit/licensing blocker, not fictional “finished” status.
