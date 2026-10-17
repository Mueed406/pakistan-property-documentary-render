# The Last Toy Shift — production continuation, 2026-10-18

**Verified state:** Original Threadjaw creature generated and edited in Blender, skinned to 16-bone armature with 3 exported clips (Idle/Lunge/Running). Tested in a real moving WebGL2 3D environment at 60 fps. Six English lines have been synthesized with 3 distinct rights-checked OFFLINE draft voices and mixed with original ambience/foley/score. **No completed 90-second animated MP4 has been produced.**

## Real executed outputs

- [First 1.5-second model proof](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39063177851) passed real frame count at **90 frames / 60 fps, 360×640**. The original model GLB is 2,171,412 bytes with SHA-256 `44bc4990cc3da52094e62f892a523a14abd931d47b81ad3b516d625a335237e1`, has **one 16-joint skin, three NLA clips and 73 mesh groups**.
- [Updated Blender + camera proof](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39063523037) passed **120 frames / 60 fps, 540×960**. Includes editable `Threadjaw_Original_Editable_Model.blend`, GLB and source manifest as one GitHub Actions artifact. Updated GLB SHA-256: `46520ab77450d86f2c6445d96f2b5577dce0067ec3626c83faeb8ab87cab2391`. Source manifest records **16 bones, 73 mesh groups, 19,704 polygons, 3 NLA clips**.
- Independent visual review of 8 frames from the updated render: genuine moving humanoid toy model, but the face/body are still stylistically toy-like; chase perspective remains predominantly frontal. Not approved for premium cinematic visual quality.
- Paired the 120-frame 540×960 H264 preview with the original 30–32s SFX segment. Verified H264/AAC 48kHz, exactly 120 frames and 2.000s, chat artifact only, SHA-256 `2cc6e5b749b11bd1d9d62496636de6e39934f00ebc6087107198ca5444a95055`.
- [Free English voice audition run](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39063978796) generated **6 cues for 3 characters** using Piper (offline) and [upstream per-model licence provenance](https://huggingface.co/rhasspy/piper-voices). English **temporary audition** only: Hero (Ryan, CC-BY-NC-SA 4.0), cassette voice (Sam, Apache 2.0 source dataset), doll voice (hfc_female, CC-BY-NC-SA 4.0 source dataset). All 3 voice ONNX source binaries SHA256-checked and NOT redistributed. Original music/SFX stem mixed to an AAC track exactly 90.000s, 48kHz stereo; 2,289,515 bytes. Actual audio cue durations and provenance in CI artifact `VOICE_PROVENANCE.json`.
- A 2.000-second local preview pairs the updated 540×960 Threadjaw render with the temporary English voice cue at 31.2s plus original SFX. H264/AAC 48kHz, exactly 120 encoded frames, SHA-256 `b125d668aa6729462dd5698d9aa73b03c494ed9d1cd2defead818a834cd1ac91`. Conversation artifact, **not uploaded to GitHub release**.
- `dialogue_draft.srt` uses **actual recorded draft TTS durations** and will need replacement/alignment once emotionally performed English takes are approved.

## Source and licence notes

- Original character: own Blender procedural sculpt, 16-bone skin, 3 keyframed NLA actions, per-mesh weights, face, fabric tufts and teeth. **Not a copied game mesh and not the official Huggy Wuggy model.**
- Poly Haven CC0 rusty-metal texture maps verified (albedo/normal/roughness), source URL and SHA in transient manifest.
- Piper Python package separate from voice ONNX models; per-model licenses matter. Ryan/hfc_female trained from **noncommercial ShareAlike** datasets. For safety, **all generated voice samples and resulting film remain NONCOMMERCIAL and publication approval is not granted**. Their training origins, use/attribution and licence compatibility should be checked before final distribution.
- Poppy Playtime is copyrighted by Mob Entertainment; consult its [fan-content policy](https://www.mobentertainment.com/fan-content). An original scene does not automatically allow an official-looking fan release or monetization.

## Quality failure / next gating tasks

1. **ARTISTIC FAIL:** creature still has stylized spherical eyes, visibly simplified geometry and plain factory geometry. Requires improved character sculpture/materials, facial expression and credible touch/contact animation, studio-quality lighting and set dressing.
2. **VOICE APPROVAL PENDING:** Piper voices are flat neutral auditions, **not** professional performances. No full listening/signoff for emotional delivery or voice actor consent/authenticity claims; test stems only.
3. 11-shot 5,400-frame native 1080×1920 60fps cinematic master **NOT RENDERED**. No 12–18-second premium final-resolution proof with dialogue and finished scenes; do not export final.
4. The final assets rights gate in `RIGHTS_GATE.json` remains intentionally closed. Keep public repository source copyright-safe, preserve all documentary material and don't modify reusable skills.

### Reproduction
```bash
cd films/the-last-toy-shift
blender -b --factory-startup --python scripts/blender_make_threadjaw.py
node scripts/acquire-cc0-pbr.mjs
npm run render -- --mode=threadjaw --start=1800 --end=1920 --width=540 --height=960
python scripts/temporary_english_voices.py --out output/voices_draft
```
See GH Actions workflows for exact dependencies, QC logs and download artifacts. Keep all WAVs/models local or restricted to the user's own workspace as appropriate. **A valid MP4 diagnostic is not a finished fan film.**
