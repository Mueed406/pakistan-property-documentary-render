# Documentary Studio v4 — Reusable Production Playbook
Maintainer: **ABDUL MUEED LASHARY**
State: original full 410.4s PPG release **verified**; v4 generic project manifest/CLI and upload integration are software work, not an already fully generalized rendering engine.

## What changed from the long PPG process

| Pain point | Reusable improvement |
|---|---|
| Constantly repeated visual direction | yt-editorial-documentary SKILL, required collage visual design and scene QA |
| Endless token consumption | single manifest, source hash caching, deterministic scene recipe, status ledger |
| Re-downloading/coding earlier work | find GitHub Release / reusable asset/scene manifests before creating anything |
| Misaligned numbers/arrows | SRT-linked cues, fixed reported numbers, arrow-target coordinates, review gate |
| 25 FPS motion mislabeled 60 | renderer makes 60 true graphics frames, source footage cadences disclosed |
| Long rerenders for one tiny fix | keep independently encoded segments, only rerun invalidated batches |
| Voice overrun | per-segment paid quota check and pause on 429; preserve successful chunks |
| Broken chat MP4 downloads | verified GitHub Release actual MP4 |
| Confused vidIQ upload vs YouTube | direct API private upload separately authorized |

## Canonical known-good case

- Production repo: https://github.com/Mueed406/pakistan-property-documentary-render
- Full film release: https://github.com/Mueed406/pakistan-property-documentary-render/releases/tag/ppg-410s-editorial-1080p60-review-20261017
- Target: 410.4 seconds, 1920x1080, 60fps, 24,624 frames, H.264 + AAC.
- Fifty 2.5D native-graphics-60fps insert sections and ordinary 25fps source stock conformed onto that timeline.
- Original longer film reused rather than regenerated.
- Original Piper narration retained: full Gemini TTS was stopped at HTTP 429 in segment 8. Do not claim approved Gemini full voice.

## New project kickoff: ONE short user brief

Example user: "Create a six-minute investigative documentary in Pakistani Urdu about property scams. Follow our premium PPG editorial style. Use budget-free production and prepare private YouTube upload."

To prepare a new reusable project:

    python studio_cli.py documentary init --project projects/property-scams --title "Property Scams Explained" --minutes 6 --mode free
    python studio_cli.py documentary status --project projects/property-scams

This creates project.json, rights.json, storyboard.json, state.json, output/.
**The command does NOT create a film.** Research, story, voice and approved assets are still required.

To review inputs:

    python studio_cli.py documentary preflight --project projects/property-scams

Blocked conditions are intentional (no actual narration, timed SRT, licenses or storyboard). Do not bypass gates by writing false booleans.

Once a real matching MP4 exists:

    python studio_cli.py documentary qc --project projects/property-scams --video /absolute/path/to/full.mp4

For advanced reproducible cache decisions:

    python studio_cli.py documentary reuse --project projects/property-scams --stage render --inputs project.json storyboard.json --output full.mp4 --recipe editorial60-v4

Cache "reuse" must only be true with same SHA-based recipe and a healthy output. Code and recipe changes invalidate it.

## Visual storyboard per scene (sample only; adapt to actual facts)

{
 "cue": "urdu-srt-cue-22",
 "start": 123.12,
 "duration": 7.6,
 "visual": "Large reported-number title unfolds over ripped newspaper texture; two cutout property documents reveal in parallax",
 "fact_source": "https://example.com/verified-primary-document",
 "asset_ids": ["licensed-photo-012", "paper-texture-cc0-002"],
 "style": "archival-editorial-2.5d",
 "text_labels": ["REPORTED", "ALLEGATION"],
 "motion": {"camera": "push", "arrow_target": [1320, 460]},
 "conceptual_not_evidence": true
}

No guessed facts or filler; this example is only a schema shape. User-specified duration drives creative timing. Existing PPG scene list contains specific facts and must never be transplanted into a new unrelated video.

## Content quality

1. Research original news/official sources first; maintain claim ledger with uncertain/alleged status.
2. Source assets from commercially permitted licensed sources, record actual URLs, author, terms and local SHA256. Never use another YouTuber's screenshot/template as a literal scene asset.
3. Use multiple archival types within a film: torn-paper editorial, photographic collage, professionally sourced aerial overlays, document-based explainer, sophisticated timelines, cutout parallax, restrained cartographic diagrams and real moving footage.
4. High-contrast headline font + editorial serif + mono metadata and proper Urdu RTL shaping. Do not ship font binaries to the user.
5. Build only scenes that the narration supports. No fake official logo, building, court verdict or real site map.
6. Audio audition early, then paragraph/master generate with strict API quota; QC actual spoken output, not just waveform size.
7. For the main movie run segmented true 60fps render, separate original source 25fps, clean chroma/transparent compositing and soundtrack.
8. FFprobe report, visual contact sheet, full audio check, source+licenses, subtitle QA, professional title and description.
9. Release on GitHub first, ensuring actual file uploaded. YouTube PRIVATE import only afterward with authorized account and final approval.

## Existing PPG execution adapter (source-specific)

The proven renderer is:
- editorial_collage/full_60fps/build_full.py
- editorial_collage/full_60fps/assemble_full.py
- .github/workflows/ppg-editorial-full-60fps.yml

Use exact source artifacts and project assets it expects; do not invoke for a brand-new topic. It uses 50 specifically hand-authored Urdu source cues and an existing stock film, not generic AI scene interpretation.

## Quota and provider behavior

A: Free-only → bundled/local audio + licensed material + local/GitHub FFmpeg/Canvas/Python.
B: Hybrid → prompt audition, available Gemini key, budget approval, bounded requests; pause on quota or 429; preserve partial WAV clips.
C: Premium → credit estimate, current balance, user approval; no surprise charges. vidIQ balance was 0 when reviewed on 17 Oct 2026; retrieve live status before future use.

Flow subscription credit balance does not grant Gemini API quota. Never ask user to paste passwords in chat.

## YouTube private upload

The connected vidIQ channel in this project is **Pakistan Property Group**, ID UCdQu7MU5dHhaClhkCdG2BKg. vidIQ token cannot be assumed to authorize third-party GitHub Actions YouTube Data API access.

A native YouTube upload pipeline exists:
- production/youtube_private_upload.py
- .github/workflows/youtube-private-upload.yml

Requires an OAuth 2.0 client, a refresh token granted using the account that owns the target channel, and GitHub Actions Secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN. Separate setup document: docs/YOUTUBE_PRIVATE_UPLOAD_SETUP.md.

In GitHub Actions manually choose **YouTube — Verified PRIVATE Documentary Upload** and provide the exact Release tag, channel ID, approved title, source-cited description, audience classification, and approval phrase UPLOAD PRIVATE. No credentials are printed. The workflow checks ownership, downloads the actual MP4 from its Release, checks file size, then uses the official resumable videos.insert upload and records a YouTube video ID. Private videos require user's separate approval before becoming public; the helper does not change visibility to public.

**Safety:** A media upload or generated video in vidIQ is NOT a YouTube video; a GitHub Release is NOT a YouTube upload.

## Documentation maintenance

Update the skill when:
- new licensed art/media technique passes 60fps QA
- a voice provider or API changes documented pricing/quota
- a render failure reveals a new checkpoint/recovery pattern
- a verified YouTube OAuth upload reaches PRIVATE status and actual video ID

Record change/date, affected renderer version, source license, tests and exact reproducible command. Preserve last working film & branch.
