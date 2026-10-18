# Actual production QA — 2026-10-17

This records **actual executed GitHub Actions and inspected media**. It is not a claim that a 90-second film exists.

## Tests

| Gate | Result |
|---|---|
| TypeScript build with pinned Three.js 0.180.0 / Vite | **PASS**, Actions build on 2026-10-17 |
| Manifest contiguous 11 shots / 5,400 frames / 60 fps | **PASS**, structural check only |
| WebGL2 headless scene initialized | **PASS**, hosted Playwright Chromium/SwiftShader |
| First hardware smoke encoded 60 frames | **PASS** after installing FFmpeg; exactly 1.000 second, 270x480, H.264, 60/1, **no audio** |
| First smoke artistic read | **FAIL**: underexposed and obviously primitive geometry |
| Lighting + creature stand-in repair | **PASS technically**: second video decoded 60 frames and visually inspected |
| Second smoke artistic read | **FAIL**: character visibly resembles a cartoon stand-in with spherical head, synthetic fur-spikes and simple segment pivots; not acceptable as final cinematic fan character |
| Native 1080x1920 cinematic hero proof, 12–18 seconds | **NOT RENDERED** |
| 90s 5400-frame MP4 with English voices and music | **NOT RENDERED** |
| Professional real skinned GLB character and facial acting | **NOT ACQUIRED / NOT VERIFIED** |
| Voice/dialogue/audio mixes, full temporal QC, copyright signoff | **NOT DONE** |

### Actual artifact evidence

- First successful hosted smoke: https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39058443995
- Original technical artifact had the misleading prefix `PROOF_16S_NOT_FINAL` despite containing only **60 frames = 1 second**. The naming bug has been corrected in subsequent capture source to embed **exact start, end and frame count**.
- Later corrected-image smoke (also 60 frames): https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39058803281
- Actual FFprobe checks: 270x480, H264, 60/1, 60 decoded video frames, exactly 1.0s.
- Inspected at t = 0.65s: first version mean RGB ~[5.6, 5.8, 10.2]; lighting-repair version ~[20.4, 32.4, 43.0] (8-bit channel averages). This records one sampled frame, not a full-scene perceptual assessment.
- Actual preview is **not** 1080p and has no recorded English voice; DO NOT upload as a completed film or claim full 16-second proof.

## 16-second motion-and-sound diagnostic — VERIFIED (technical only)

- GitHub Actions: https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39059236627
- File: `DIAGNOSTIC_16S_LOWRES_WITH_ORIGINAL_AMBIENCE_NOT_FINAL.mp4` (download as a GitHub Actions artifact or the verified ChatGPT conversation copy).
- Final validated by local FFprobe, OpenCV decode, and audio volume check: **960 actual decoded frames**, 270 × 480, **60/1 fps**, H.264 video + AAC stereo 48,000 Hz, exact 16.000 seconds, 2,072,321 bytes.
- SHA-256 of that actual MP4: `62442a612a9a7834cab09f959bd39080fd358ef36d48629e615c53d5d92aedba`.
- Frame-by-frame change scan: 960 frames, average decoded grayscale brightness **34.80/255**, zero frames with whole-frame brightness under 5, zero adjacent pairs below 0.07 mean absolute grayscale difference. This checks movement, not visual quality, geometry correctness or lighting approval.
- Audio loudness analysis via FFmpeg volumedetect: mean **−23.2 dBFS**, peak **−5.3 dBFS**. Original synthesized mechanical atmosphere only; **NO English dialogue or music mix**.
- Human-reviewed 11-frame contact sheet: real 3D parallax and movement, but **ARTISTIC GATE FAILED**. Character is visibly simplified round/segment geometry, conveyor is repetitive, camera work stays dominated by a straight-on view, and environments/materials/acting are below requested premium quality. No approved official/fan skinned GLBs are present.
- **Important:** 16-second result is **270 × 480 only**. It is a diagnostic and never fulfills the mandatory native 1080 × 1920 film deliverable.
- No 90-second film, actual English voice stems, gameplay, proprietary assets, or release-ready content was generated. Rights gating remains fail-closed.

## Defects requiring artistic work

1. Replace all procedural character stand-ins with professionally sculpted, licensed, weighted skinned GLB models. Animate facial expression, gaze, feet and arms without clipping. Verified rights and proven 60fps motion required.
2. Replace 256px noise textures with properly sourced 2K/4K PBR material maps (metal, rough, normal, suitable UV scale and lighting) and inspect in native portrait resolution.
3. Reblock 11 camera stages around genuine character scale / environmental geography; make opening, factory tape, GrabPack interactions and chase visually coherent. Current scene graph is an engineering foundation.
4. Acquire/record original English actor stems with human approval; mix separate footsteps, breath, machinery, original music and foley at 48kHz; no official actor impersonation.
5. Produce full 12–18-second final-quality moving *skinned* GLB shot before attempting all scenes. Review complete movement, contact, lighting, sound and frame boundaries, not only a sampled PNG.
6. Source/licensing registry and actual GLB/voice files must pass strict hash/rights gates before final 5400-frame render.

**Capacity caveat:** The 60-frame 270x480 runner render took roughly 18 seconds after scene initialization. Do not linearly promise a 1080x1920/5400-frame job will finish on an unaccelerated GitHub runner; test suitable GPU hardware first.

## Provenance

The standalone smoke contained **original procedural meshes/materials** only. No game models, footage, voice performances or soundtrack were acquired. Original environment and synthetic non-dialogue soundtrack script are in the feature branch. Mob policy remains applicable before a Poppy-related publication. Reusable ChatGPT/Gemini skills were not changed.
