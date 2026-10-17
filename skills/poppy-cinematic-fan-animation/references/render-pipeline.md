# Professional 3D Production and Reproducible Render Architecture

This is a production template, **not a prebuilt movie engine**. Every physical scene, character rig and source media file must actually exist and be inspectable before rendering.

## Technology selection

Primary route: Three.js (pinned compatible revision), TypeScript, glTF/GLB meshes, AnimationMixer, real lights, physically-based materials and dedicated camera paths. Use Blender for authored character animation, retargeting, high-quality custom models, physics/rigging, cloth, hair and hero shots. Use a different runtime only when a small comparative proof yields better visible results.

Use HTML/CSS for an offscreen render interface and precise overlays, **not as fake 3D visuals**. WebGL2 / Three.js renders the 3D content. Python controls capture, asset checks, sound, and production checkpoints. FFmpeg encodes and joins video/audio; it does not create the 3D acting. Do not use PHP, databases, S3 or remote worker farms unless the production has a real need and available access.

## Actual asset readiness

For each shot, require:
1. All mesh and skeleton files on disk, hash-matched and license-checked.
2. Scale and axis orientation proof. Factory doors, toys, hands, machinery must have believable real-world relative proportions.
3. Mesh material audit with base color, normal and roughness/metallic textures. No unexpectedly missing pink/default materials.
4. Lighting and environment checks at a target resolution and grade in color-managed output.
5. Asset copyright review, especially extracted official Poppy Playtime models, voice clips, game music and publisher branding.
6. Rig bone/morph target inspection and clips verified in a tiny test before long-frame rendering.

## Deterministic frame clock

The production engine should implement an explicit **renderFrame(frameIndex)** callback, with fixed `fps = 60` for the example project.

Example architecture (adapt to actual mesh/animation graph):

```ts
// Conceptual renderer interface; this is NOT a full browser/capture program.
interface Shot {
  startFrame: number;
  endFrameExclusive: number;
  renderAt(localSeconds: number): void;
}

const FPS = 60;

async function renderFrame(frame: number, shot: Shot) {
  if (frame < shot.startFrame || frame >= shot.endFrameExclusive) {
    throw new Error("Requested frame lies outside shot");
  }
  const localTime = (frame - shot.startFrame) / FPS;
  // Must set the entire scene deterministically from this frame time:
  // camera transforms, AnimationMixer clips, lighting, particles and props.
  shot.renderAt(localTime);
  renderer.render(scene, camera);
  // Capture after GPU/webfont/asset readiness barrier, not rAF wall clock.
}
```

Use THREE.AnimationMixer.setTime(seconds) when appropriate for absolute clip evaluation, handling local shot offsets and clip blending. Animations involving physics/particles either need fixed-step deterministic caches or closed-form sample functions; do not skip earlier frames and expect stateful physics to produce identical results.

**Hard frame arithmetic:** shot start/end must be integers. Last sample is frame 5399 for 90s/60fps, time 89.983333... seconds; scene boundaries are exclusive on the end. Never duplicate a boundary frame or let rounding add a 5401st frame. Use audio timeline anchored in integer samples (48kHz recommended) and map to frames.

## Cinematography

- 3D geometry and physically coherent camera movement, no static illustrated poster as a substitute.
- PBR materials with realistic reflections, contact shadows and readable textured surface detail.
- Actor blocking with weight, smooth anticipation, hands interacting with physical props, foot contacts, sensible camera focal lengths.
- Horror lighting is **dark but readable**, with local industrial fixtures, emergency indicators, controlled smoke/fog/dust and shadow falloff.
- Use subtle, motivated effects: atmospheric shafts, projection jitter or VHS screen noise only on the diegetic CRT, not random glitch on every cut.
- Avoid excessive shadows causing black frames, ambient-light washouts, default flat game-website look, overdone bloom, perspective distortion, duplicated meshes or auto-generated gibberish text.

## Source video windows

If licensed game capture or industrial stock is useful, use it as a coherent world-space visual or true editorial insert. Store source fps/codec/license and honor it: converting 25fps footage to a 60fps container does not produce 60 originally captured frames. Do not automatically download or repurpose another creator's game stream.

## Efficient frame capture

Playwright/Chromium can coordinate headless rendering if reliable GPU support exists. In software-only environments, calculate expected throughput and adjust rendering approach rather than claiming browser visuals equal Blender Cycles hero shots. Confirm:
- WebGL2 active, no context loss, shader compile complete.
- All glTF/texture/audio/titles loaded before capture.
- Correct 1080×1920 crop, no browser chrome or responsive website UI.
- 100% of expected frames exist, each with exact source-frame provenance.
- Capture a first proof scene including a moving rigged mesh, physically shaded environment, active camera, real sound, codec-verified MP4.

Shot cache key includes source commit SHA, engine version, shot manifest, 3D mesh hashes, materials, animation files, audio timestamps, lighting and codec/color settings. Healthy rendered shots can be reused; edited clips must invalidate only their affected shots.

## Optional high-end path

If actual machine GPU/render budget warrants it, use Blender EEVEE or Cycles for hero frames and complex animated models/volumetric work; composite faithfully with real-time footage. Prefer an honestly high-quality film over rigid dedication to one tech stack. Do not promise 4K or photorealism without visually testing the real renderer.

## Reference documentation

- [Three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader)
- [Three.js animation guide](https://threejs.org/manual/pages/animation-system.html)
- [Three.js post-processing](https://threejs.org/manual/pages/post-processing.html)
- [Blender glTF exporting](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)
- [Playwright screenshots](https://playwright.dev/docs/screenshots)
