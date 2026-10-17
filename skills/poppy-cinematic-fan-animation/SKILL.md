---
name: poppy-cinematic-fan-animation
description: Produce original cinematic 3D horror fan-animation videos using Three.js, TypeScript, Blender, English character voices, permission-checked gameplay or stock footage, and frame-accurate production QA. Use when asked to plan, build, animate, render, or repair a Poppy Playtime-inspired unofficial fan movie, teaser, or animated scene.
license: MIT
metadata:
  author: Abdul Mueed Lashary
  version: 1.0.0
---

# Poppy Cinematic Fan Animation — Production Skill

**Creator/maintainer:** ABDUL MUEED LASHARY  
**Purpose:** An installable production workflow, NOT a package of copyrighted Poppy Playtime game assets or a finished animation.

## When to activate

Use this skill for an **original English 3D fan animation**, cinematic teaser, atmospheric toy-factory action scene, character-animation repair, or technical audit. It is **not** a documentary style, 2D slideshow, static poster generator, gameplay download tool, or claim that a game studio has approved our work.

If a user gives a particular length, aspect ratio, language, animation engine, existing project, or rights restrictions, **honor those over example defaults**. For an otherwise unspecified short, the supplied example is 90 seconds, 9:16, 1080×1920, true animated 60fps (5,400 timeline frames).

**Read in order:** [Story and shot plan](references/shot-storyboard.md), [Source rights and assets](references/asset-rights.md), [3D architecture](references/render-pipeline.md), [English voice and cinematic finishing](references/audio-and-qa.md), [Prior projects' tested lessons](references/lessons-from-previous-videos.md).

## Deliverable contract — don't mistake code for a movie

A completed task must supply **an actually rendered, verified playable video** or disclose why no render was possible. The presence of a `SKILL.md`, storyboard, frame manifest, PR, or generated image does not constitute a film.

Stages have strict names: `PLANNED` → `ASSETS_ACQUIRED` → `3D_PROOF_RENDERED` → `SCENES_RENDERED` → `FULL_MP4_VALIDATED` → `CREATIVE_APPROVED` → `PUBLISHED`. Never skip stages or claim downstream success from upstream files.

Deliver: MP4 and exact verified download path/URL, editable 3D+TS/JS project, actual asset-and-license ledger, per-scene frame manifest, voice stems/English script and SRT (if used), FFprobe data, visual/contact QA and clear outstanding limitations. Publish only through user-approved accounts.

## Mandatory sequence

1. **Inspect what exists.** Review given GitHub branches, source code, files, actual video output, assets and prior QA. Do not regenerate working shots or pretend local conversation attachments are in GitHub.
2. **Research accurately.** Distinguish canonical game lore from our own original non-canon story. Read [Mob Entertainment fan-content policy](https://www.mobentertainment.com/fan-content) before using official likenesses, gameplay, models, logos, sounds, or deciding monetization. Creator gameplay uploads are NOT automatically free-to-reuse.
3. **Write an original story** with varied shot sizes, stakes, spatial continuity, plausible interactions, and English acting. The provided 11-shot 90-second example is editable inspiration, not the official plot of any chapter.
4. **Create and audit an asset registry** containing legal source, author, per-file rights, filename, SHA256, technical traits and permitted use. Prefer original factory models, author-created elements, and appropriately licensed PBR/HDRI materials. Do not redistribute game-extracted source models or another creator's footage.
5. **Prove genuine 3D.** Make a 12–18s test containing actual imported rigged geometry, camera motion, material/lighting, physical toy/hand/prop depth, soundtrack and native animation frames. A picture billboard drifting in space fails this gate.
6. **Build a real scene-driven renderer.** Use pinned Three.js/TypeScript + glTF and AnimationMixer for appropriate browser scenes; use Blender for rigging, authored hero shots, simulations and physically sophisticated movement when visibly better. Code the scene around a deterministic integer frame clock rather than uncontrolled wall time. Author effects to support clarity, not distract.
7. **Separate English voice acting.** Give narrator/hero/creature/tape/Poppy-inspired voice parts individual stems and performance directions. Never put stage directions or role labels in spoken text. Do not clone official actors without authorization. Do human audition on key lines before generating whole film.
8. **Render shot batches with checkpoints.** Hash source/asset/config + shot bounds; skip only validated identical outputs. Target native resolution, true 60fps animation frames, controlled bloom/shadows, and spatially coherent 3D movement. Use Python for automation, and FFmpeg for final mux/encode, not as a substitute for scene animation.
9. **QA every boundary and actor.** Check all transitions, geometry clipping, double faces, pupils, hand pivots, foot contact, shadow persistence, source texture resolution, caption timing, waveform sync, black/frozen frames, duplicate frame count and sudden light exposure shifts.
10. **Verify final release.** FFprobe must confirm duration/frame count/resolution/fps/H264/AAC. Human creative review is separate. Provide an actual downloadable artifact through the runtime or verified GitHub Release, *never* a guessed release link. Label fan animation as independently created and not endorsed by Mob Entertainment.

## Visual standard

- Dark but readable toy-factory horror: aged metal and colored plastic PBR, authentic grime, worn painted concrete, believable scale, industrial lighting and deep physical parallax.
- Strong cinematic blocking: low-angle camera pushes, purposeful focus racks, physically possible chase choreography, locked screen direction, anticipation/payoff; no jittery pose teleportation.
- One coherent mesh/face/skeleton per character; no doubled head or floating mouth. Real head/eyes/limbs animation and proper contact.
- Keep source footage's original captured cadence truthful. Upsampling 25/30fps gameplay into a 60fps timeline does not create 60 newly captured source frames.
- For generated concepts/textures: image generation is useful for concepts, matte shots and bespoke texture references, **not a replacement for rigged 3D characters or arbitrary copyrighted 3D models**.
- Select engine by final result and available GPU; Three.js is not mandatory if Blender rendering wins an actual comparative proof. Avoid unnecessary PHP/S3/backend setup.

## Rights and safety

Clearly label the movie as **“Unofficial Poppy Playtime fan animation. Not affiliated with or endorsed by Mob Entertainment.”** Verify the exact fan-policy terms for commercial uploads, gameplay capture, model reuse, music and imagery. Do not post proprietary game data or restricted raw assets in a public repo. Third-party templates (Jitter, Mixkit, Motion Array, etc.) require an actual licensed export and format compatibility; referencing a template page is not importing it.

No unapproved paid generation, credentials pasted into source, or unauthorized account uploads. Preserve rights and provenance in the asset manifest.

## Install/usage

See [README](README.md). The example shot plan is [examples/last-toy-shift.json](examples/last-toy-shift.json); run `python scripts/validate_project.py examples/last-toy-shift.json` for structural checks. Passing a **plan** check does NOT mean copyrighted game assets exist or are cleared, and strict media-readiness must fail until actual files are attached and verified.

## Relation to earlier production

The prior Pakistan Property Group 60fps documentary and property shorts establish **engineering lessons** (layered sprites, separate audio cues, accurate frame timing, GitHub QA); their props, scripts, stock footage, Urdu voice or documentary art direction are NOT part of this fan-film workflow. Read the references, but do not copy prior films' look into cinematic 3D.

## Improvement philosophy

Measure successful outputs, not claims of “100× quality.” Preserve useful learnings as skill-ready notes; edits to shared skills or public release still require authorization and correct repo permissions. When tools/rights/media are unavailable, report the concrete blocker and produce reproducible code/docs without claiming a finished video.
