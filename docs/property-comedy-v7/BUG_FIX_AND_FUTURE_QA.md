# Layered video improvements backlog and QA

Status: review-only documentation. No skill was modified.

## Timing and role choreography
Narration is a user-uploaded 95.399s ElevenLabs Zafar clip containing meta-labels and all 12 scripted lines, not a clean multi-character master. Approximate content cuts (source seconds) used, with 12 independent clips:
```
01 narrator 08.52–15.10
02 dealer   17.81–23.64
03 buyer    25.45–27.75
04 dealer   30.54–36.93
05 buyer    39.40–43.50
06 dealer   46.85–50.99
07 buyer    53.38–57.83
08 narrator 60.45–69.12
09 narrator 70.97–77.05
10 narrator 80.46–84.83
11 buyer    87.63–90.68
12 dealer   93.55–95.30
```
Transitions are grounded on the newly assembled ~58.7-second dialogue track; final five-second subscribe/music bumper brings length to 63.699 seconds. These boundaries were inferred from pause detection and order of the full user transcript, **not validated by voice-recognition alignment**.

## Fixed or improved
- Full-frame AI poster motion replaced with independent PNG actors, paper, marks, type and small moving stock-film windows.
- Chai gag deliberately uses a single real object: during the dealer's tea-pose, no second tea PNG is drawn on top.
- One face/character sprite at a time per side; no stacked double-face blend.
- Poor blue scanner mockup replaced with three tactile-paper document checks.
- More varied duration, kinetic scaling, cutout-parallax and abrupt/soft paper-mask effects.
- Channel branding spelled consistently PAKISTAN PROPERTY GROUP.
- Extra full five-second subscribe card independent of the dialog.
- Real original project stock frames appear in scenes 1, 4 and 8; do not misstate them as verified footage of an accused individual or development.

## Remaining creative risks
- The V6 cartoon source PNGs are relatively low resolution; their faces can look soft when scaled to 1080p. Replace with 2K+ character-specific expression and joint-layer sprites using approved image generation or authentic artist illustration.
- Motion is an independent pose/sprite rig, not advanced mouth/arm/eye skeletal animation. Genuine professional acting requires mouth phonemes, hand rigging, eye darts, torso arcs and independently designed joint pivots.
- Source 25fps footage was resampled to 12fps within stock-card windows for this lightweight edition. Future film should use full source native 25fps 2D video planes and sample at destination's 60fps timeline, or preserve 25fps aesthetics intentionally.
- CSS/browser animations are at 60 rendered timestamps. Export is Lanczos 720→1080; creating all graphics natively at 1080 or 4K can improve edge quality at higher compute.
- ElevenLabs file may still include words from audible headings because trim boundaries were selected without an ASR service. Perform careful human listening and re-edit before posting.
- Tone remains an illustrated comedy explainer. A genuinely professional final needs 3 distinct approved Pakistani Urdu roles and expressive/comedic direction, not just pitch settings on one voice.
- Inherited stock footage rights need the earlier source manifest to be rechecked before public commercial upload.
- No GitHub Release MP4 or YouTube upload was performed for V7; MP4 exists in ChatGPT's sandbox with verified paths.

## Acceptance before public posting
1. View complete 63.699s MP4 with sound and verify **every** cue.
2. Check physical chai object continuity, eyes/mouth, at 24–36s.
3. Check legibility of Urdu caption baseline on mobile and all headline safe margins.
4. Confirm correct channel logo/naming, CTA and final 5s music/visual outro.
5. Fact-check buyer advice and commercial stock license audit.
6. If artistic review passes, publish exact MP4 through an approved private YouTube channel OAuth upload, then user approves public visibility.
7. **Only after the user's future instruction** create Antigravity/ChatGPT skills update prompt using this documented work; do not execute a skills update now.
