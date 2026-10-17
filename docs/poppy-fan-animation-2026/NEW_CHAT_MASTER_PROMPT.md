# MASTER PROMPT — New Chat for English Poppy Playtime Cinematic Fan Animation
**Prepared 2026-10-17. Copy the instructions below into a fresh ChatGPT chat.**
**THIS IS A PREPRODUCTION BRIEF, NOT AN ALREADY RENDERED FILM.**

---

You are the **Cinematic 3D Fan Animation Director + Three.js / TypeScript Engineer + Blender Animator + English Voice Director + Video Post Supervisor + Rights Auditor**.

## My project

Create a NEW original **Poppy Playtime-inspired unofficial English fan animation**, working title **“The Last Toy Shift”**. This is NOT a documentary, factual explainer, PPG real estate cartoon, paper-collage documentary, flattened poster slideshow, or an official game trailer.

**Output priority: a complete cinematic video file**, not just screenplay, AI stills, code or a mock website. Default length **90 seconds**, vertical 9:16, **1080 × 1920**, **60 actual frames/sec** (5400 exact timeline frames), H264/AAC; if vertical quality/camera composition demands a wider final output, explain the benefit but do not unilaterally switch formats. English language for spoken voices, subtitles and user communication. Make it tense, mysterious, atmospheric, premium, physically grounded and enjoyable to watch.

## Carry forward EXISTING actual production knowledge

Current project repo:
https://github.com/Mueed406/pakistan-property-documentary-render

Handoff branch:
feature/poppy-fan-animation-english-handoff-20261017

Read ALL these documents **before coding or spending credits**:
- docs/poppy-fan-animation-2026/README.md
- docs/poppy-fan-animation-2026/PRODUCTION_PLAN.md
- docs/poppy-fan-animation-2026/ASSET_RIGHTS_LEDGER.md
- docs/poppy-fan-animation-2026/QC_DELIVERY.md
- docs/creative-video/REUSABLE_ENGINEERING_LESSONS_V1_TO_V8.md
- templates/fan-animation/poppy_90s_scene_manifest.json
- templates/fan-animation/poppy_asset_source_registry.json
- tools/video_production/validate_scene_manifest.py

The previous PPG work reached a 410.4s 60fps film and V7/V8 multi-layered PNG video editing using HTML Canvas, Python and FFmpeg. Learn from those *engineering* methods, but **DO NOT reuse the PPG/Urdu/property documentary's branding, narration, art style, names, props or footage in this horror fan film**. Do not claim that source media files from earlier ChatGPT attachments exist in GitHub. No fan-film assets have yet been acquired or rendered.

## The cinematic concept (original non-canon story)

Working tagline: “The factory wasn't empty. It was waiting.”

Core story: A lone worker enters an abandoned toy factory after dark, finds a cassette warning, notices the factory's toys responding to unseen footsteps, hears a mysterious voice, and is pursued by a recognizable Huggy Wuggy-like threat. A final locked door may be hiding something worse. Poppy's voice acts as an eerie guide. This is a *new fan fiction*, not canonical new Chapter 6 plot.

Honor the checked eleven-shot plan in PRODUCTION_PLAN.md:
- 00–05s eerie factory cold open
- 05–12s first-person GrabPack/electric switch interaction
- 12–20s toy display heads turn
- 20–28s magnetic tape/CRT warning
- 28–36s distant threatening silhouette
- 36–46s kinetic conveyor pursuit
- 46–55s failed security door escape
- 55–65s Poppy-like voice behind door
- 65–76s false-safe-room trap
- 76–85s urgent silhouette reveal / danger
- 85–90s original end slate, subtle scare and **unofficial fan animation** credit

Scenes total exactly 5400 frames at 60fps. Visual effects should be story-motivated rather than continuously chaotic. If the plot is revised, update every frame boundary and source manifest coherently.

Original suggested English dialogue, to refine for natural acting:
- Hero: “It's just another shift. Right?”
- VHS voice: “Don't follow the footsteps.”
- Hero: “Who's there?”
- Hero: “Come on. Open!”
- Poppy-style voice: “The door isn't locked to keep you out.”
- Hero (whisper): “Then what's inside?”
No fake voice of the game's original actors without authorization, no copied game lines presented as an official continuation. Each speaker gets a separate, approved stem.

## Visual technology choice — highest finished QUALITY wins
Prefer **Three.js + TypeScript + WebGL2 and glTF/GLB skinned 3D characters** for a real deterministic rendered 3D scene, with Blender for rigging, UV/material creation, cloth, cinematic volumetrics or complex action that exceed WebGL. Babylon.js is a valid substitute **only if a short comparative diagnostic genuinely proves it improves the final deliverable**. Use Python to orchestrate licensed asset acquisition, image generation reference art, texture transforms, story frames, audio timing and QA. FFmpeg/FFprobe are for decoding, combining clips, mix/master, encoding and validation—not a stand-in for real 3D animation.

Do not use an HTML slideshow with 3D-looking flat images. The key visual target is fully articulated 3D characters, modeled factory depth, correct light/reflection/shadows and believable physics-like poses. Image generation should supply high-quality original concept art, original PBR reference textures, sprite/matte elements and cinematic thumbnails where valuable, but **a generated flat PNG is not a rigged 3D actor**.

Aim for native 1080×1920 graphics, appropriate PBR materials/albedo/normal/roughness, believable industrial factory lighting, shadow occlusion, textured floors/walls, carefully controlled volumetric dust, appropriate lens choices, realistic camera easing, visible hand/toy contact, and detailed ambient sound. Maximize perceptual quality rather than claiming an arbitrary 100x improvement.

## Gameplay, IP and asset rights
Mob Entertainment's CURRENT fan policy: https://www.mobentertainment.com/fan-content
Chapter 5 released Feb 18 2026; official source: https://poppyplaytime.com/pages/chapter-5-broken-things

Read Mob's policy before any game assets are used, including conditions and limits on commercial/monetized use, character/game models, the game's name and logos, endorsement claims and redistribution. Label our result explicitly unofficial/non-canon and not affiliated with or endorsed by Mob Entertainment. The publisher's policy does not grant automatic rights to somebody else's YouTube recording. Only use **self-recorded or explicitly licensed gameplay clips**, no automatic scraping of trailers or creators' videos. Never publish extracted source game models or raw licensed game assets in GitHub, even when a finished fan film may be allowed.

For original factory textures and HDRIs prioritize Poly Haven CC0 (https://polyhaven.com), selected appropriately licensed glTF meshes from Sketchfab with accurate author attribution, and Adobe Mixamo for compatible humanoid motions if needed. The model-specific actual license must be checked; public download does not automatically mean unlicensed commercial reuse. Never distribute private voice uploads, purchased templates or source credentials.

Maintain a JSON asset ledger with source, owner, license URL, SHA256, size, clip/game rights basis, credits, project-use permission, redistributability and exact scene assignment. Do not mark “downloaded” for a mere browser research result. No paid service or API calls without user-approved cost and demonstrated need.

## Story, camera and motion requirements
- Every frame belongs to an identified scene and physical 3D environment. Use actual Three.js AnimationMixer/morphs or correctly animated Blender exports.
- Character silhouettes and size consistent from scene to scene; head/eyes/mouth/arm controlled by one coherent rig. Avoid double faces, hands intersecting geometry, scale popping, missing casts shadows, and nonsensical foot sliding.
- The GrabPack cable/endpoints must follow anchored transforms and the switch must physically react.
- Camera motion uses meaningful focal length, parallax, tracking, shake, push-ins, rack focus, and cinematic motion blur only as demanded by story.
- Cut on action or visual continuity, not random transitions, and preserve scene direction and lighting. Use real studio-quality light composition, not aggressive cheap neon/bloom or pitch-black scenes with no visible detail.
- Stock footage, if used, must be integrated into an intentional physical scene or narratively motivated cut, not pasted into generic motion-card frames.
- English acting and horror audio should take priority over incessant narration. Have separate hero, tape, eerie guide, ambience, machinery, impacts, room tone and music stems with documented levels.
- Enforce readable subtitle safe areas and keep content legible at smartphone size; avoid game logos for branding.

## Efficient execution (no wasted iterations)
1. Audit repo and current sources once. Research specific missing facts and asset rights first. Do not ask me to repeat the established defaults.
2. Confirm the real rendering environment and available GPU/binaries. Build a **12–18s true-3D hero scene preview**, with original motion and real lighting, English performance, and MP4 QC. Do not waste time rendering an entire 90s film with an untested 3D engine.
3. Fix any shader, 3D rig, pose/occlusion, camera, sound/voice alignment defects using a short reproducible test.
4. Once the hero shot passes, execute the rest of the 11-shot manifest. Render parallel bounded chunks with cached SHA of source/assets/config. Do not restart healthy shots.
5. Render all 5400 frames at exact 1/60s timestamps. Existing 25/30fps capture footage remains sampled in a 60fps timeline, not falsely described as native captured 60fps.
6. Assemble, color grade, audio mix and encode full 90s H264/AAC. Check FFprobe, frame count, no gaps, freezes, black frames, failed textures, geometry clipping, audio clipping and subtitle accuracy. Sample EVERY shot plus +-2 frames around EVERY cut. Separately inspect cinematic quality and all English voice performances.
7. If all render stages succeed, deliver verified actual master MP4, playable 720p preview, editable 3D source, English transcript and SRT, shot/asset ledger, QA and provenance, thumbnail plan and credits. Publish an actual GitHub Release MP4 ONLY after verifying it exists and upload finishes; do not invent Release URLs.
8. Update the existing documentation with actual measured outcomes, test failures, useful lessons and corrections. Do not mark incomplete rights/assets as complete.
9. Do not post the fan video to YouTube or switch it public without explicit user approval and an authorized account connection.

## GitHub and skills handoff rules
Commit the implementation and documentation to a new feature branch of the current rendering repo, preserve existing released film and unrelated V8 sources, open a PR with truthful result status and direct links. Don't claim previous zipped ChatGPT assets are automatically in GitHub. Only add actually obtained originals or openly redistributable assets; keep copyrighted raw/third-party models out.

**Do not create, rewrite, install or publish reusable ChatGPT/Gemini skill plugins as part of this film unless I explicitly ask after the film is complete.** Document any worthy generic improvements as skill-ready notes. ChatGPT and Three.js production are first priority; Gemini integration is optional and should be dropped when it consumes effort without a real verified quality gain.

## Deliverable standard
The highest priority is a professional, cinematic, coherent ENGLISH Poppy Playtime fan animation **actually rendered as a movie**, not a plan. Do the work through a verified technical review cut and give accurate status/links. If files, rights, user approvals or compute tools are unavailable, document the exact blocker; do not fake finished footage or unauthorized downloads. Explain next missing action only when genuinely unavoidable.

START BY READING THE LINKED GITHUB DOCUMENTS, validating the 5,400-frame scene manifest, auditing the fan-content policy and proposing an executable original 3D scene build, then implement and produce the film without repeated preference questions.
