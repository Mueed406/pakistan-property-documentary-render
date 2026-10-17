# Poppy Cinematic Fan Animation Skill

**A shareable AI-agent skill for creating original, non-canon English cinematic 3D toy-factory horror fan animations.**

Maintainer: **ABDUL MUEED LASHARY** · License of THIS skill's original documentation/scripts: MIT.

> Not affiliated with Mob Entertainment. Contains **NO copyrighted Poppy Playtime models, gameplay clips, game music, extracted assets or finished videos**. An installable skill is a workflow, not an automatic movie generator.

## Install for an AI coding/production agent

Requires Node.js / npm for the Skills CLI. Run this in the project folder where your AI coding assistant operates:

```bash
npx skills add Mueed406/pakistan-property-documentary-render --skill poppy-cinematic-fan-animation
```

You can choose the supported AI agent interactively. To show available skills without installing:

```bash
npx skills add Mueed406/pakistan-property-documentary-render --list
```

To update it later, rerun the add command or run the Skills CLI's supported update flow.

**Direct skill location:**  
https://github.com/Mueed406/pakistan-property-documentary-render/tree/main/skills/poppy-cinematic-fan-animation

Manual installation alternative: clone this public repository and copy the whole `skills/poppy-cinematic-fan-animation/` directory into your supported coding agent's local skills directory. Copy subfolders `references/`, `scripts/` and `examples/` too.

A native consumer ChatGPT conversation cannot necessarily install Skills CLI packages as ChatGPT Plugins. A friend can open [SKILL.md](SKILL.md) as instructions, or use the skill in a compatible coding agent such as Codex or Claude Code. Agent-specific support and setup depend on current CLI capabilities; don't promise automatic installation in every app.

## What the skill provides

- A proper 3D horror-fan-animation production workflow, NOT documentary or flat poster animation.
- Three.js/TypeScript + Blender workflow with actual skinned GLB character animation, PBR textures, lighting, real depth and cinematic camera paths.
- Original **English** multi-character performance guidance, dialogue cues and sound design.
- Reproducible integer-frame 60fps timeline planning and reliable rendered-video validation.
- Original 11-scene, 90-second/5,400-frame example storyboard and JSON file.
- A rights-conscious asset ledger that clearly distinguishes **researched** assets from **downloaded / authorized** files.
- A dependency-free Python script for validating shot frame boundaries and asset-readiness states.
- Lessons carried forward from the actual PPG V1–V8 video projects, without reusing their property-related art or voices.

## Test the bundled example (no paid API, no video rendering)

From the installed skill directory:

```bash
python scripts/validate_project.py
```

Expected: `"ok": true`, `"mode": "PLAN_ONLY"`, `"frames": 5400`.

To check whether the project has REAL downloaded/created approved assets:

```bash
python scripts/validate_project.py --render-ready
```

This deliberately **fails** for the sample because the author has NOT bundled proprietary 3D characters, actual game capture or licensed source files. It is an honest safeguard, not a bug.

## Example request to an AI assistant

> Use the poppy-cinematic-fan-animation skill. Create an unofficial 90-second English toy-factory horror animation with a real rigged 3D chase sequence, believable lights and character acting, native 1080×1920 at 60 FPS, and original audio. Check the game rightsholder's fan policy and asset rights first; produce an actual MP4, editable Three.js/Blender source project, sound stems, and full technical and creative QA. Do not treat scripts or stills as a completed movie.

## Contents

- [SKILL.md](SKILL.md) — agent workflow and non-negotiable rules.
- [references/shot-storyboard.md](references/shot-storyboard.md) — 11-shot 90s horror fan story.
- [references/asset-rights.md](references/asset-rights.md) — game IP, models, stock, voices, texture rights.
- [references/render-pipeline.md](references/render-pipeline.md) — deterministic 3D/60fps rendering, Three.js and Blender.
- [references/audio-and-qa.md](references/audio-and-qa.md) — English voices, sound, video and creative QA.
- [references/lessons-from-previous-videos.md](references/lessons-from-previous-videos.md) — previously tested pipeline learnings.
- [examples/last-toy-shift.json](examples/last-toy-shift.json) — exactly 5,400 frame example.
- [examples/asset-ledger.json](examples/asset-ledger.json) — prospective assets with transparent NOT ACQUIRED status.
- [scripts/validate_project.py](scripts/validate_project.py) — standard-library preflight checker.
- [LICENSE](LICENSE) — MIT license for original instructions/code (NOT game assets).

## Copyright and disclaimer

*Poppy Playtime* and related names/characters are trademarks and/or protected works belonging to their rightsholders. This skill supplies original workflow instructions and does not claim rights in those works. Follow the rightsholder's [fan-content rules](https://www.mobentertainment.com/fan-content) and independently verify each source before distributing a finished film.

**Status:** This skill has been packaged for installation and testing; it does **not** imply that the planned 90-second example film has been rendered.
