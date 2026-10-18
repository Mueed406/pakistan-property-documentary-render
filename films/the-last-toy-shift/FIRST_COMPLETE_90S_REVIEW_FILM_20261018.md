# First ACTUAL complete 90-second moving 3D film cut — 2026-10-18

## Produced and independently verified

- All **11 actual moving 3D narrative scenes**, exact **5,400 frames** at **60 FPS**, actual source WebGL2 render **540 × 960 portrait**.
- Full score, industrial Foley/SFX, and six audible English script lines in three distinct Kokoro ONNX TTS voices. **48 kHz stereo AAC audio**.
- Runtime independently verified **90.000 seconds** by FFprobe for BOTH MP4 encodes, exact **5400 decoded H264 video frames** in both.
- Delivery variants:
  - `The_Last_Toy_Shift_COMPLETE_90S_540x960_60FPS_REVIEW_ONLY.mp4` — 30,713,826 bytes, SHA256 `db45f8cd616897ce28a2bd7621786ba6d227618838373262d95f665faf60d383` — actual native source.
  - `The_Last_Toy_Shift_COMPLETE_90S_1080x1920_UPSCALED_DRAFT.mp4` — 49,548,678 bytes, SHA256 `001f06a695b24d7297315d0b625aef97229c80b8056f769a00ef8537afc87cc1` — upscaled from 540p source using FFmpeg Lanczos, contrast, saturation and sharpening. **NOT a 1080p-native render.**
- Original-source parent: [GitHub Cloud 11-scene render #39098919788](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39098919788). All 11 scene jobs completed successfully; its optional assembler job failed because the recovered Blender asset artifact also contained an unrelated 120-frame rigproof clip. No render shots lost.
- Successful isolated [Cloud assembly job #39099200899](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39099200899) correctly removed the extra rigproof, assembled all 11 scene files and uploaded the final two draft videos with `CLOUD_FILM_90S_QA_NOT_FINAL.json`. Artifact name: `The-Last-Toy-Shift-90S-5400-FRAMES-VOICE-SFX-FULL-REVIEW-MP4`. GitHub retention 14 days.
- English soundtrack: [previous verified cloud Kokoro 90s job #39097760161](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39097760161).
- Original Blender Threadjaw model: [verified source job #39063523037](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39063523037).
- Source edits, reusable render scripts and rights ledger preserved in draft PR #13. No publicity, public release, or skill package modifications.

## Honest artistic assessment / release gate

**NOT APPROVED AS THE PREMIUM FINAL FILM.** Full contact sheet inspection showed visibly simplified procedural industrial geometry, stylized toy model, and severe framing failure in scenes **7 and 8** (camera directly faces a rusted security door at extreme close range). Shot **10** had inadequate creature visibility. The urgent corrective camera/light edits are separately being rendered in 3 GitHub cloud scenes; these will feed a revised V2 cut if validated. Stage 4 close-up CRT text sometimes clipped in the original framing and should be re-directed before release. The six English lines are synthesized draft voices, not approved dramatic voice-actor performances. Motion is genuine 3D, but there has been no professional facial performance, full-body physics choreography, or studio-cinematic quality approval.

The requested 1080×1920 **native** 60 FPS premium finished render and unrestricted distribution authorization are not delivered here. The rights gate remains `release_authorized: false`. Mob Entertainment proprietary IP concerns and model/audio licensing remain review items before public release. Do not label this technical/visual-cut milestone as final cinematic quality.

## Reproduction

Run 11 sharded real frames via `.github/workflows/last-toy-shift-complete-cloud-film.yml` and use `.github/workflows/last-toy-shift-assemble-cloud-review.yml` on finished cloud artifacts. The old original workflow's optional assembly step should not be re-used without filtering the unrelated recovered `120FRAMES_1800_1920` rigproof. The dedicated assembler is verified successful.

Artifacts are also in the conversation as user-downloadable MP4s and a frame contact sheet. The original 3D source and editable model remain in the GitHub project.
