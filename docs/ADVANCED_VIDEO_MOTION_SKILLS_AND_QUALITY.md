# Professional Motion Studio — Verified Skills and Hybrid Video QC

As of October 17, 2026, the repository has tested an actual HTML Canvas → headless Chrome/Edge → FFmpeg pipeline on Windows, a working 6:50 real-stock documentary baseline, and a **full-length browser-motion render workflow**.

## Existing completed integrations

1. `JakeB-5/motion-graphic-skill` — MIT, frame-exact HTML/CSS/Canvas, shot review, sound hints.
2. `haidrrrry/claude-remotion-skill` — MIT, Remotion cinematic compositions.
3. `iart-ai/motion-design-skills` → `motion-art-direction`, `shot-composition`, `beat-sync-editing` — MIT. All three installed and tested on an isolated GitHub runner.
4. `heygen-com/hyperframes` → `hyperframes-animation`, `hyperframes-cli`, `faceless-explainer` — Apache 2.0. All three installed and tested on the same isolated GitHub runner.
5. `abhimahamkali/claude-motion-skill` /motion — external optional upstream; **no LICENSE found** in the earlier repository audit, so DO NOT vendor, copy, or relicense its implementation.
6. `iart-ai/motion-design-skills` also supplies `color-motion` and `remotion-video` for cross-shot Rec.709/palette checks; optional future installs.
7. `drewharvey/claude-html-animation-skill` MIT — alternative HTML-to-video skill, no need to run concurrently with our existing working renderer.
8. `apoorvlathey/motion-canvas-skills` MIT — TypeScript Motion Canvas alternative for complex explainers.
9. `heygen-com/hyperframes` — complete HTML/GSAP frame-exact rendering engine with `hyperframes check/lint/snapshot/render` CLI. This is a good alternate when our browser renderer encounters layout/format limitations; its Apache 2.0 license must be respected.
10. `RFTaurus/motion-skill` MIT — another browser animation system; don't install all variants simultaneously without checking conflicts.

## Creative direction from installed skill guidance

- **One motion language:** calm, sharp, documentary. Use ease-out at 350–600ms rather than bouncy CSS dashboard transitions.
- **Hierarchy:** ONE primary focal point in each shot; strong negative space, a 12-column master grid, restrained teal/copper/neutral palette, visualizations tied to a spoken fact.
- **Pacing:** editorial cuts on narrator phrases, not random percentages; deliberate holds on numbers for comprehension; hard cuts or occasional motivated dissolves only.
- **Perceptual color:** avoid excessive saturation; use restrained palette and Rec.709-aware output.
- **Real assets:** at least half the documentary should be relevant, moving verified video rather than static cards. Source manifest and stock license checking remain mandatory.
- **3D:** use Blender for actual licensed architecture; label every conceptual map as a reconstruction, never as the real housing society geography.
- **Natural voice:** the working existing 6:50 baseline uses Piper, still requiring improved synthetic voice selection. Do not disguise known robotic problems with EQ and claim them solved.

## Actual complete-film build

```powershell
# From repo root after installing Windows Studio prerequisites:
python studio_cli.py render-full-browser --base baseline/renders/Pakistan_Property_Stock_Documentary_FINAL.mp4 --srt baseline/urdu_timed.srt --out renders/Pakistan_Property_Full_Browser_Motion_Review.mp4
```

Cloud workflow: `.github/workflows/render-full-browser-documentary.yml` automatically obtained baseline from 38962816235 and generates eight different browser scenes, then a real full-length H.264 MP4. Output is an unpublished review artifact, not a claim of voice/creative signoff.

Engineering QC after full render:
```powershell
python -m pip install Pillow
python editorial/full_film_qc.py --video renders/Pakistan_Property_Full_Browser_Motion_Review.mp4 --srt baseline/urdu_timed.srt --out renders/review_qc
```

This makes 18 sampled review frames, flags black/duplicate images, checks fps, runtime, audio presence, and subtitles. Human listening and visual review remain mandatory.

## Deployment separation

The actual public skills repository `islamically85-byte/youtube-agent-skill` is read-only to the currently connected GitHub identity. Updating this project does **not** update that repository or the private ChatGPT YouTube Toolkit plugin automatically. Use the master Antigravity prompt under `docs/ANTIGRAVITY_MOTION_SKILLS_V3_PROMPT.md` to create a new PR with an authorized account. Never claim a skills repo release occurred without a verified commit.
