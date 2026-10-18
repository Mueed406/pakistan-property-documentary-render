# 2026-10-18 — actual rigged animation / PBR / sound validation

**Status: engineering progress only. This is NOT the final 90-second fan film.**

## Actual completed / verified

1. **Rigging:** Acquired the real CC0 animated `RobotExpressive.glb` from the official three.js repository, pinned to commit `eba30de865cfbf31ac736f792defd9a60ff28d57`. SHA-256 checked: `047f5e5fb3bb6d378bd1df16ca6137f2a596c99b3a1b5690b4020c05aaf6f319`. Real `SkinnedMesh`, embedded `Running` clip and AnimationMixer. Author: Tomás Laulhé; edits: Don McCurdy. [Official asset license](https://github.com/mrdoob/three.js/blob/dev/examples/models/gltf/RobotExpressive/README.md) CC0 1.0.
2. **Working native skeletal motion:** [Hosted run](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39061155662) rendered/FFprobed **240 actual encoded frames at 60fps**, portrait 360×640, 4.000s. Contact sheet independently reviewed: true in-place character limb movement and changing camera perspective.
3. **Source PBR:** [Poly Haven official Rusty Metal Sheet](https://polyhaven.com/a/rusty_metal_sheet) diffuse/normal(OpenGL)/roughness maps (1K) by **Amal Kumar**, CC0. [Hosted verified run](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39061870320) downloaded all three from the official API, verified the provider's MD5 and recorded SHA-256 before use. Corrected three.js materials use true PBR maps on factory metal.
4. **PBR video:** same hosted run encoded **120 actual 360×640 frames at 60fps**, 2.000s, H264. Independent decoded-frame check passed. Original source image assets not committed; transient manifest in workflow artifact records provider URL and hashes.
5. **Original 90s sound:** [Hosted run](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39061495920) generated four isolated stereo WAVs: atmosphere, Foley/SFX, suspense score, temporary mix. Format 48kHz, 90.000s, AAC listening mix; 22 main events with additional footfall sequence, cue-positioned but NOT actor timed. Entire audio original mathematically synthesized, no game soundtrack or borrowed SFX. Tracks are available as workflow artifact.
6. **Video/SFX mux QA in conversation:** 4.000s rigproof with temporary stereo audio: H264/AAC, 240 frames, SHA-256 `1a43187b49d156acdc6545179a29d35feab7307ab1e8676779c15ffa79c0206e`. PBR 2.000s rigproof mux: H264/AAC, 120 frames, SHA-256 `6c7916ce8af05cd840c28358fed87e51b2f516fe5f0ac9631ae1957b857611f5`.
7. **Additional authored VFX code (build pending check):** deterministic world-space switch sparks and diegetic cassette safety text, not 2D static overlays.

## Recorded PBR binary manifest SHA256 (verified)

| Map | SHA256 | Bytes |
|---|---|---:|
| rusty_metal_sheet diff 1k JPG | `ecfacdea466b43162b63867b419576b7d35d34ea37c96969cf05e5a07faeb705` | 793,031 |
| rusty_metal_sheet nor_gl 1k JPG | `473e8ec4079a8be8c9bef59df8d95f61fd43f9961f4ec42421f21dee07713a5d` | 409,291 |
| rusty_metal_sheet rough 1k JPG | `8d40e8422a234ecc036ad17be6669f9544e66c9a80816e159b9a5a7ac06a4a65` | 626,838 |

## Artistic QA: STILL FAILING

- RobotExpressive is a **yellow stylized robot**, deliberately not Huggy Wuggy or a viable final horror character.
- Shot blocking remains excessively centered/close; visual continuity needs professional direction and character sizes calibrated to human/monster anatomy.
- 1K rusted metal textures improve a few factory structural objects but do not make the concrete/factory architecture film-quality. Real set dressing, decals, texture atlases, damaged props, cinematic shafts, occlusion and light continuity still required.
- **English character voices not produced.** HeyGen attempt for a short line failed with incompatible account-selected speech engine; service requested alternate engine. Do not make false dialogue-performance claims.
- The 90s score/Foley stems have not undergone final subjective mastering or mixing with dialogue; they are drafts.
- Real hero 12–18-second moving/voiced test at **1080×1920** remains **NOT MADE**; 90s native master and all 5,400 frames are **NOT RENDERED**.
- Mob Entertainment fan policy and third-party model licenses must be checked for eventual publication; the CC0 technical robot does not grant rights to official proprietary fan characters.

## Next execution gate

Acquire a high-quality legally usable noncommercial fan-character rig with full skeletal clips and adequate surface textures, or have it professionally authored. Private-source handling only for conditional game assets (never redistributed in public repo). Obtain three authorized expressive voice stems. Reblock proof with finished scale, studio lighting and material details at true 1080×1920, render 12–18s with full sound and audit before scaling to 5400 frames. Keep PR #13 **draft** and full-export rights gate locked until complete. No reusable skill modification.
