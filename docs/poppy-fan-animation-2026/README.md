# Poppy Playtime Fan Animation — NEW PROJECT HANDOFF (2026-10-17)

**Status: researched production concept and reusable documentation committed. NO video, official gameplay, character model or soundtrack has yet been created, downloaded or cleared for this new project.**

**User's intent:** start this film in a NEW chat. This repo handoff must not trigger filming, image generation, API spending, YouTube publication or an automatic skills/plugin upgrade.

## Concept and defaults
- Working title: **The Last Toy Shift — An Unofficial Poppy Playtime Fan Animation**.
- Format: a high-energy suspense / survival-horror fan animation, not a documentary, explainer, paper collage or PPT infographic.
- New script is in **English**; use English TTS actors or human voices with separate stems and performance approval.
- Default output: **90 seconds / 5,400 frames / vertical 9:16 1080×1920 / native 60fps** because this continues the user's last Shorts-style video. Change to cinematic 16:9 only if user specifically requests a horizontal cut. Do not presume the old V8 duration or property channel narration.
- Script premise is an **original non-canon fanfiction** set in an eerie toy factory. Protagonist finds a damaged VHS / tape clue, follows unnatural footsteps, escapes a moving toy-and-conveyor trap, glimpses Huggy Wuggy and hears Poppy before the lights go out. Treat the exact fan use as conditional on Mob Entertainment's policy, not an official chapter.
- Tone: cinematic, tense, uncanny, mysterious, with one strong reveal; avoid cheap jump scare after every cut or long static slideshow shots.
- Content rating: non-graphic horror suitable for general horror audiences; no harmful real-world instructions.

## Verified publisher context as of 2026-10-17
- Mob Entertainment released **Chapter 5: Broken Things** on 2026-02-18 per their official page and Steam. Avoid calling Chapter 5 unreleased.
- Official chapter background describes a deeper, dangerous factory and Huggy Wuggy in pursuit; original side-story should not fabricate an official Chapter 6 or use fan speculation as established canon.
- Rights holder fan content policy: https://www.mobentertainment.com/fan-content ; permits certain non-commercial fan-generated content including conditional game-asset use, with exceptions and constraints. Fan video must be independently labeled, not charged for viewing, and not claim official endorsement; no unauthorized resale of extracted models/game data.
- Relevant game page: https://poppyplaytime.com/pages/chapter-5-broken-things
- Studio official news: https://poppyplaytime.com/blogs/news

## Technical approach hierarchy (quality first)
1. **3D core:** Three.js (maintained current compatible version, pinned), TypeScript, glTF/GLB with skeletal animation via AnimationMixer, PBR materials, WebGL2 post-processing. Build real environments, rigs and camera movement. Prefer the high quality that a 3D interactive cinematic production warrants, not fake 3D planes.
2. **Hero shots and hard rigging:** Blender for character animation, facial/cloth/keyframe rigs, volumetrics, simulation and offline hero shots. Export compatible GLB or pre-rendered high-resolution plates as best suited to each shot. Mixamo may support humanoid skeletal actions only if compatible.
3. **Rendering control:** deterministic renderFrame(frameIndex), fixed 1/60-second stepping, browser Playwright/Chromium with GPU availability diagnostics and secure local scene/assets routing; preloading+camera/frustum/resolution/frame completeness checks.
4. **Asset prep/cut compositing:** Python Pillow/OpenCV/NumPy (where installed) for masks, depth maps, metadata, atlases, shot manifests, automated QC and track retiming. Generated images can inform environment textures, concept art, backdrop matte paintings, prop signs, and thumbnail but cannot substitute for animated GLB meshes.
5. **Encoding:** FFmpeg/FFprobe for H264/AAC or archival ProRes, final grade, audio, subtitles, stable MP4 and thumbnail extraction. FFmpeg is NOT the primary 3D animation engine.
6. **S3/PHP:** not needed by default. Introduce storage hosting only when rights, credentials and significant reproducible benefits justify it.

## Sound + video source selection
- Highest-quality path: **self-recorded Poppy Playtime gameplay** if the user owns/accesses game and usage follows publisher fan policy, or explicitly authorized captures. Gameplay recording should have no streamer face-cam, overlays, watermarks or borrowed commentary.
- Do NOT automatically download other YouTubers' gameplay or Mob trailers and assert reusable rights. Official public availability alone is not a license to reupload/re-edit every clip; record source, rights basis and transformation before use.
- Other stock: licensed atmospheric factory machinery, dust, industrial hallways, retro monitors and tape reels, used as transitions or image planes. Must match light and motion, never be presented as literal official gameplay.
- 3D source: original authored environment and character-specific fan assets consistent with rights. Use official fan-policy permissive scope responsibly; no public redistribution of extracted meshes in GitHub raw source packs.
- Stock textures: Poly Haven CC0 concrete, rusty metal, textiles, industrial HDRIs. Verify per-asset URL and hash after acquisition. Avoid defaulting to low-poly untextured walls.
- Performance: one original English narrator or restrained character dialogue with clean individual stems, no role labels, timed phonemes and proximity/location-specific sound effects. Original SFX/music or appropriately licensed library; no game soundtrack reuse without rights review.
- Video/stock templates are optional **only if the actual file can be downloaded under an appropriate license and transformed with our tools**. Do not claim a Premiere-only MOGRT ran inside Three.js.

## Document index
- [Full shot-by-shot frame plan](PRODUCTION_PLAN.md)
- [Asset and IP permissions ledger](ASSET_RIGHTS_LEDGER.md)
- [Technical and creative QA gates](QC_DELIVERY.md)
- [Reusable starter scene manifest](../../templates/fan-animation/poppy_90s_scene_manifest.json)
- [Complete new-chat master prompt](NEW_CHAT_MASTER_PROMPT.md)
- [V1–V8 lessons](../creative-video/REUSABLE_ENGINEERING_LESSONS_V1_TO_V8.md)

## Privacy / repo custody
Only reusable **documentation, manifests and original code** should be committed to this branch. No copyrighted extracted gameplay/models, hidden API credentials, purchased templates or the user's private ElevenLabs voice file in GitHub. Real source assets must be stored locally or in controlled licensed media storage; record URI + SHA without guessing paths. A future new chat can import user-provided files and rights manifests when actually available.

## Completion definition for the NEXT chat
Actually create and validate a full native-quality video; deliver a verified MP4, editable project, shot source, license/credits manifest, English transcript and caption SRT, technically tested QC, artistic caveats and actual media download link. Do not call a script, storyboard or GitHub branch an exported video.

**No skills were edited or installed in this documentation phase.**
