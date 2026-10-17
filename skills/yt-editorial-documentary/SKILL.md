---
name: yt-editorial-documentary
description: Produce verified full-length documentary MP4 files with original 60fps editorial motion, factual source records, licensed art, checkpoints, visual QA and private YouTube upload safety gates.
---

# YouTube Agent Studio v4 — Editorial Documentary
**Extension maintainer:** ABDUL MUEED LASHARY. Preserve upstream authorship and third-party licenses.

## Contract
When asked for a documentary, deliver a verified playable video, not only script, storyboard, code or static AI image. If executing a new render is unavailable, explicitly say what is blocked and provide a reproducible project. Never pretend to have uploaded a YouTube video without a real YouTube video ID.

## Default creative direction
Use original archival newspaper collage, photocopied textures, physical torn paper, illustrative photographic cutouts, layered shadow, graphite and cream, mustard highlights, purposeful red annotations and arrowheads landing on the correct fact or subject. Animate with true full-screen sequences intercut with original licensed footage; stock footage behind every graphic is NOT mandatory. Choose professional type variation: Inter Display Black, editorial condensed sans, EB Garamond serif, IBM Plex Mono and accurately shaped Noto Arabic variants where licensed and installed. Do not redistribute font files.

Use original animated photo planes, 2.5D parallax, cinematic pushes, paper-tape holds, cutaway/ink reveals, dynamic numbers that remain qualified as alleged/reported, selective 2- or 3-frame stop-motion holds while the camera continues at 60 distinct frames/second. Reject flat black rectangles, cheap web-style cards, fake government stamps or ungrounded maps. Motion must make a narration point intelligible. Every asset source and photo depiction must be correctly licensed and identified as genuine evidence or merely illustrative.

By default export 1920x1080 16:9 at 60fps, H264/AAC. Original 25fps stock remains 25fps captured material conformed to the output rate; don't call duplicated original footage native 60fps.

## User interaction
Do not ask repeatedly for information already known. User ordinarily supplies topic and requested minutes; recover established art direction and production defaults. Any 5/6/9-minute request gets that target runtime, not a 410-second reused story. Audio language comes from request; Pakistani Urdu in PPG work, English conversation unless requested otherwise. If missing one critical new fact, ask once.

## Mandatory workflow
1. Inspect GitHub Releases and reusable sources before generating. Preserve finished masters.
2. Initialize a new independent project with python studio_cli.py documentary init --project projects/slug --title "Title" --minutes N.
3. Build a claim/source/date ledger and fact-check allegations, authorities and numbers. Mark conceptual maps or staging.
4. Inventory licensed stills, stock footage, fonts, textures, voice/music. Record source URL, license, author, SHA and usage rights in rights.json; cache originals and avoid downloading repeatedly.
5. Script true narrative with timestamps and chapter acts. Generate the specific project's scene plan tied to real narration/SRT. Never reuse the PPG 50-cue list in an unrelated film.
6. Voice audition before full API usage; keep provider approval and quote cost. HTTP 429: stop retries and preserve produced chunks. Re-time subtitles after audio changes; do not pad unnatural pauses.
7. Storyboard using full-screen paper animation, meaningful maps/charts, photographs, licensed stock and occasional Blender. Do not force any arbitrary amount of stock footage.
8. Render a 10-25s first-pass test, inspect real movement, typography, Urdu shaping, arrow anchoring and chroma/artifact failures. Then render only changed segments through SHA256 configuration caching and resumable scene batches.
9. Assemble at 60fps; preserve soundtrack with broadcast-normalized dialogue. Recheck total duration against actual audio and scene timings. Keep source projects editable.
10. Automated FFprobe QC of real MP4 + human review frames from every animated chapter and full film; actual H264/AAC, exact FPS/dimensions/runtime, clipped audio, readability, allegedly reported numbers, asset manifest, missing/wrong frames.
11. Deliver MP4 via verified GitHub Release download link, report QC, caption SRT, source credits, thumbnail idea, title, description, chapters and decisions. Never invent files or paths.
12. YouTube first upload is PRIVATE-only, authorized against exact channel through YouTube Data API OAuth. vidIQ media import is NOT YouTube publication. Do not publish publicly without user approval.

## Three provider modes
A FREE: authorized local voice, open tools, licensed stock, browser animation, Python, Blender and FFmpeg.
B HYBRID: Gemini TTS only with a known API quota and budget approval; on 429 switch to previously approved audio without hiding the substitution.
C PREMIUM: check current provider balance and quote exact generation costs before charging; no unapproved repeat generations.

## Optimized engineering and truthful milestone labels
Avoid rerendering an unchanged film or repeatedly downloading assets. Cache by source SHA, narration cues, renderer revision and render settings. Check intermediate MP4 integrity before reusing. Keep deterministic frame boundaries and safe final-frame hold to prevent end-of-film frame deficit. Don't start 50 parallel workers when five batches suffice. Don't rerun a full render because of an isolated visual error. Always mark separately: script ready, assets obtained, audio generated, animated scenes rendered, full movie verified, YouTube PRIVATE uploaded, PUBLIC published.

Use ppg repo example: 410.4s / 1080p60 / 50 editorial scenes, GitHub release ppg-410s-editorial-1080p60-review-20261017. This is proven PPG footage ONLY, not a generic engine for all new topics.

## CLI and automation
- python studio_cli.py documentary init --project projects/new --title "..." --minutes 6
- python studio_cli.py documentary status --project projects/new
- python studio_cli.py documentary preflight --project projects/new
- python studio_cli.py documentary qc --project projects/new --video verified.mp4
- python studio_cli.py documentary package --project projects/new --video verified.mp4
- Use approved CI workflow for the subject; PPG's existing workflow is a project-specific template.
- Required separate manual YouTube OAuth upload workflow. Default upload is private, has explicit upload phrase and channel verification.

## Skill continuation
For Antigravity/Claude Code, use docs/ANTIGRAVITY_DOCUMENTARY_V4_MASTER_PROMPT.md and docs/DOCUMENTARY_V4_PLAYBOOK.md; do not claim installing this skill itself installs software or gives API access. For ChatGPT, invoke connected app actions only when available. User credentials must be held in authorized GitHub Actions secrets, not in chat. Preserve editable history, sources, and licenses. Return exact facts on what is COMPLETE vs INCOMPLETE.

## Premium transition rules (v5 extension — 17 October 2026)

The default documentary transition library is `editorial_collage/transitions/premium_transitions.py` (original, no external paid dependency). Five presets: `paper-tear`, `ink-print`, `newspaper-slide`, `film-splice`, `photo-match`. Each composites BOTH true preceding/incoming video plates through textured masks at the actual frame-locked cut. The transition is not a separate stock clip, full-screen image generator output or generic wipe pasted over video.

Choose transitions only at meaningful shot/act boundaries—typically a small curated subset, never every cut—and preserve voice/music timing and source duration. At 60 FPS use short 0.3–0.6-second bridges, inspect middle frames and edge artifacts. Final process **uses the existing master MP4**; never spend quota recreating fifty scenes to repair a few transitions.

A proven 15s/60fps motion test and full GitHub Release upgrade workflow are documented in `editorial_collage/transitions/README.md`. The external license-researched Mixkit, ProductionCrate, Motion Array links and export compatibility details are in `editorial_collage/transitions/TEMPLATE_CATALOG.md`.

Third-party free site templates may require actual DaVinci Resolve/Premiere/After Effects and per-item license verification. Do not claim their template project ZIP was downloaded when only an online listing was researched, and never redistribute source archives forbidden by the license. When an external editor template is approved, export licensed transition media to a compatible format before the FFmpeg pipeline imports it.

For skill updates, cache key must include transition-plan JSON, executable source revision and source-video digest; sample-first QA and versioned GitHub Releases protect prior masters.
