# The Last Toy Shift — actual 90-second Cloud-rendered 3D VIDEO workprint QA (2026-10-18)

## Deliverable status

**THE ENTIRE 90-SECOND MOVING-3D FILM WORKPRINT IS NOW ACTUALLY RENDERED, WITH ENGLISH DIALOGUE AND SFX.** It is NOT production-quality final art, nor does an upscale equal native 1080p render. The earlier 16s and 2s clips have now been replaced by an authentic full-film video workprint, and that distinction matters.

### Actual successful independent rendering

- [Eleven cloud-rendered frames jobs in GitHub Actions run 39102572740](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39102572740) each completed **success** and stored all corresponding video clips with per-shot frame-index metadata and FFprobe validation. The earlier job's integrated assembly initially failed due a too-strict expectation of Blender's binary GLB fingerprint being identical across independent runners, **not a failure of rendered scenes**. The source-level assembler check was corrected in a subsequent commit; separate cloud-only assembly was initiated with no rerendering.
- Exact authoritative frame spans: **[0,300), [300,720), [720,1200), [1200,1680), [1680,2160), [2160,2760), [2760,3300), [3300,3900), [3900,4560), [4560,5100), [5100,5400)** = exactly 5,400 consecutive, nonoverlapping frames / 11 actual scenes.
- All 11 real moving 3D H264 assets were downloaded from successful GitHub jobs; individual metadata, start/end/frame count, resolution, 60fps, coded video frame count and no-release flag were independently cross-checked in the current session. Changes in binary fingerprint of independently generated GLBs were recorded rather than misinterpreted as scene/frame defects.
- Full film constructed with FFmpeg concat from all **5,400** actual 360×640 60fps 3D frames, muxed with the **previously generated, authentic** 90s cloud Kokoro three-character English soundtrack with original synthetic music/SFX. Original sound mix hash `4e9054332da14b9c1789d666bea4934860defedb5c46a8bf69b1c5cc587f3be7` reverified byte-for-byte before mux.
- FFprobe from the actual resulting full MP4: **90.000000 seconds**, **5400 decoded video frames**, H264, **360×640 source**, **60/1 fps**, AAC **48kHz stereo**.
- Native-source workprint file size **15,555,613 bytes**. SHA-256: `408011fa272a756d29c95342af5302e836c2c1299b2621141bc08f75a5acddda`.
- Current-session user download: `THE_LAST_TOY_SHIFT_FULL_90S_ORIGINAL_3D_360x640_60FPS_ENGLISH_WORKPRINT_NOT_FINAL.mp4`.

### Added enhanced viewing version

- Re-encoded the full 5,400 frames with Lanczos upscale, modest grading (gamma/contrast/saturation), mild sharpening and actual-dialogue-timed SRT subtitles placed in lower third. First subtitle-position test was **rejected** because large ASS font and vertical margin put words at top; corrected styles were tested on an actual 8.5-second timeline frame and verified visually BEFORE final encode.
- Final corrected 1080×1920 **UP-SCALED** 60fps full workprint, FFprobe **5400 frames**, **90.000000 sec**, AAC 48kHz stereo. **Not native 1080p**; upscale cannot create missing scene/fur/rig geometry.
- File size **77,634,102 bytes**. SHA-256: `283a52b75c7122a1f45dc5f5ca956cd55bb02da4fa2b3530394ed088e96daf2e`.
- Current-session user download: `THE_LAST_TOY_SHIFT_FULL_90S_1080x1920_UPSCALED_ENGLISH_CAPTIONS_WORKPRINT_NOT_FINAL.mp4`.
- Precise transcript exported as `THE_LAST_TOY_SHIFT_ENGLISH_SUBTITLES.srt`.
- All eleven scene-midpoint frames were sampled from the combined workprint to create a single `SCENE_CONTACT_SHEET_11_SHOTS.jpg`. Technical decode pass for all; artistic grade **FAIL**.

### Remaining real limitations

- This is 3D and visually coherent at a technical level, but its architecture/props and hand are plainly primitive and the film lacks natural, sophisticated contact blocking, physically observed shots and high-end character acting. Shadows/lighting and CRT typography also need artistic improvement. Some scenes contain deliberately dark environment/monster positioning; editor should visually review each scene rather than falsely calling the video cinematic.
- Original Threadjaw skinned GLB with 3 clips is authentic, but its appearance is an original fan toy design — **not a licensed proprietary Huggy Wuggy model**. Several minor toys are procedural stand-ins.
- Speech is Kokoro-generated open-source voices, not real hired actors or artistically approved final voice acting. Original SFX are synthetic/engineered, not a final Foley mix.
- The user's original request was a polished native 1080×1920 premium short; this **does not meet that higher subjective quality gate**. PR stays **draft** and the strict `RIGHTS_GATE.json` final-mode authorization remains closed, even though the 90-second technical workprint is now genuinely finished.
- The correct next milestone is professional reblocking, material/prop upgrades, and expressive/approved voices, then **actual native-resolution rerender**.

No assertion that a workprint is the final master or that the user's local GPU was accessed. All rendering was through GitHub cloud runners; postproduction/upscale was completed and independently QA-verified in the current environment.
