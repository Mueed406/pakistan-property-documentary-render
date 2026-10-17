# The Last Toy Shift — original 3D production stage

**Status (2026-10-17): IMPLEMENTATION SOURCE ONLY. No movie or verified technical-proof MP4 exists.**

This folder is a new, isolated production project descended from the documented handoff on PR #11. It is **not** the older property/Urdu project, and should never be presented as a completed fan video. The working title is an **unofficial, non-canon Poppy Playtime fan animation**.

## What has actually been implemented

- Three.js WebGL2 scene with original procedural industrial geometry, a physically connected hallway, PBR material properties, real world-space depth, shadows, camera parallax, shelves, conveyors, animated rollers, packages, wiring, CRT player and sliding door.
- An **original segmented stand-in toy rig** with articulated pivot joints, animated limbs/head, moving camera, physically positioned props and lighting. **It is not a professionally skinned final GLB**. A final GLB importer with `GLTFLoader`, `SkinnedMesh` verification and `AnimationMixer` is wired but needs authorized models with animations.
- Eleven shot-specific cameras and state changes, sampled deterministically via `window.renderFrame(integerFrameIndex)`. Absolute integer frame timing prevents variable-browser-framerate drift.
- Resumable per-shot MP4 output via Playwright PNG screenshot capture into FFmpeg; inputs can remain at native 1080×1920/60; derived timestamp frames are 0 to 5399.
- A fail-closed final-delivery rights gate and separate automated MP4 metadata QA. No downloaded game audio, extracted models, third-party videos or credits have been fabricated.

### Local commands

Requirements: Node.js 22, npm, FFmpeg/FFprobe, GPU-enabled Chromium/WebGL2; Python with NumPy for optional **original non-dialogue** temporary ambience.

```bash
cd films/the-last-toy-shift
npm install
npx playwright install chromium
npm run build
# Internal structural check of original plan; does NOT validate media:
npm run validate
# 16s ORIGINAL TECHNICAL STAND-IN (30–46s chase); not a release film:
npm run render -- --proof --width=1080 --height=1920
# Inspect actual encoded file and fps:
node scripts/check_proof.mjs output/PROOF_16S_NOT_FINAL_<fingerprint>.mp4
# Optional original temporary non-dialogue ambience:
python scripts/sound-bed.py --seconds 16 --offset 30 --out output/proof-ambient.wav
```

Hardware render suitability must be assessed before a full 5400-frame job. Headless Chromium needs functioning WebGL2 and enough memory; the provided server environment did **not** have a functioning Chromium/WebGL renderer, Blender or preinstalled Three.js dependencies, and therefore **no render success is claimed**.

### Required replacement before an artistic approval

The segment-jointed procedural toy is a proof-only proxy. Replace it with professionally weighted, authored or appropriately licensed **skinned glTF/GLB** creatures, heroes and dolls, animation clips, custom PBR maps, directorial facial acting and legal voice recordings. Regenerate camera blocking after actual rig dimensions are measured. Build source quality must be assessed via real rendered frames, not by code inspection. No unsourced official character model is bundled.

### Completion and release gate

- Treat publisher policy and third-party source permissions independently.
- Complete `RIGHTS_GATE.json` with actual files, SHA-256, license/owner/source and individually approved uses. Keep copyrighted extracted/game models and private recorded voices OUT of public GitHub source.
- Complete the upstream `templates/fan-animation/poppy_asset_source_registry.json` and pass its `--render-ready` validator. Passing the *planning* validator alone is not an asset clearance.
- Replace temporary ambience with actual professionally performed English hero, tape and doll voices, separate stems; no actor voice cloning.
- For release render (once authorized): `npm run render -- --all --mode=final`; then `node scripts/assemble.mjs`; `npm run validate -- --final`; visually and audibly review **all** scenes and cut boundaries.
- Do not upload a release or publish automatically. Full resolution, 5400 actual encoded frames, lip sync, story/shot quality, copyright and monetization all require separate validation.

### Source ownership and safeguards

All new procedural geometry, shader/scene/camera code and original synthetic ambience were authored for this production, without downloaded proprietary 3D models. Official universe elements are conditional fan use under [Mob Entertainment fan-content policy](https://www.mobentertainment.com/fan-content). No external performer or music license is assumed. An original render is not proof of rights to unrelated branded properties.

**Known artistic limitation:** procedural stand-ins cannot satisfy the requested final premium film quality. This project is a technical production base, not a deliverable 90-second film.

The prior 90-second story/shot asset requirements remain authoritative:
- `../../docs/poppy-fan-animation-2026/PRODUCTION_PLAN.md`
- `../../docs/poppy-fan-animation-2026/ASSET_RIGHTS_LEDGER.md`
- `../../docs/poppy-fan-animation-2026/QC_DELIVERY.md`
- `../../templates/fan-animation/poppy_90s_scene_manifest.json`

No reusable ChatGPT/Gemini skills were modified.
