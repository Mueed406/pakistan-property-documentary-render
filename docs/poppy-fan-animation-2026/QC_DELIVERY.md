# Cinematic Fan Animation — Production, Quality and Delivery Gates

**New film not rendered yet.** These are requirements for the next ChatGPT conversation's film implementation, not a retrospective claim of quality.

## A. One-time project setup
- Research Mob Entertainment official chapter and fan-content rights policy; confirm specific fan characters and allowed use. No false “official Chapter 6” claims.
- Choose the audio/camera/runtime at the beginning. Default: **90s, vertical 9:16 1080×1920, 60fps = 5,400 exact frames**; optional widescreen requested separately.
- Fix one art style: realistic toy-factory cinematic horror with polished character PBR textures, subtle fog and carefully motivated scares. No paper collage, documentary facts or website dashboard.
- Make 3D production master scene spec, 11 shots from the checked scene JSON manifest, with timed English lines, animatic and continuity diagram.
- Film sound should be genuinely performed or convincing voice-acted English, with separate hero/tape/Poppy cues and stems. Do not mimic protected voice actors without consent.

## B. Rendering-engine acceptance
- Implement Three.js or Babylon.js in current pinned versions, real imported rigged glTF models; prove skeleton bone animation, camera motion, lights, real geometry depth and responsive shadow mapping.
- Preload all scene textures and geometry before starting deterministic frame renders; fail if any 3D asset missing.
- Use current Three.js GLTFLoader / AnimationMixer. For complex character acting, use Blender animation and authored compatible skeletal GLB exports; render Blender shots separately only where visibly superior.
- For 60fps offline capture, define a deterministic renderFrame(frameIndex) function that sets scene state at frame/60, waits for shaders/assets, renders the scene and writes one frame. Avoid relying on wall clock, variable GPU frame pacing or time-of-day. Capture at native 1080×1920; 4K source optional when resources allow.
- Lighting and colors: PBR metal/rough/normal, practical overhead flicker, realistic HDRI/reflection probes (where appropriate), PCF shadow maps, volumetric-like fog only with readable contrast, tasteful depth of field/bloom/color-grade. No default oversaturated bloom, fireflies or aggressively crushed shadows.
- Integrate video captures as appropriately rights-cleared clips or physical screens / narrative cutaways; preserve original capture FPS and provenance, no misleading artificially claimed 60fps original footage.
- Camera motion design: storyboard focal lengths, dolly/whip/handheld stabilization, motion blur interpolation; maintain scale, screen direction, spatial continuity and object visibility through cuts.

## C. Iterative proof plan (no waste)
1. 12–18s **hero shot proof** including actual modeled/rigged actor + animated factory + light + sound. QC immediately.
2. Lock asset license status, character silhouettes, scale and cinematographic look before generating all 11 shots.
3. Produce scene batches with independent outputs, each identified by shot ID, frame range and source/settings SHA256.
4. On local failure or CI interruption, resume completed valid cached batches; never restart expensive shots because a README changed.
5. Assemble once from validated scene outputs, with separately mastered English stems, original licensed sound design, optional subtitle sidecar SRT and user-approved opening/end-card credits.
6. Generate both full movie and a 15s teaser only after full master exists; never substitute sample for full film.

## D. Automated technical QA
- Exact frame count 5400 for 90s/60fps; identify every frame 0–5399 once, continuous shot ranges without overlap or gap.
- Final video width 1080, height 1920, pixel format yuv420p, H264 60/1 avg and nominal fps; AAC 48kHz with stable sample rates; reasonable keyframe seeking; correct duration +/- one 60fps frame.
- No missing frames, broken PBR maps, black-screen errors, repeated intentional frame of 3+ seconds, lost alpha, texture popping, depth/Z fighting, geometry intersections, twitchy rig joins, duplicated face mesh, mismatched exposure or 3D hand teleporting.
- Audio: full listening check of every English role; no character labels spoken, no wrong word, clean breath/crossfade, no clipping, dialogue intelligible on smartphone with controlled bass, SFX peaks motivated and music ducked beneath speech.
- Subtitle word timing and safe-area; disclaimers avoid giving viewers the impression this is official content.
- 11-contact-sheet scene samples PLUS three frames near each cut (−2, 0, +2) PLUS automatically flagged low-change/black-frame intervals. Human look/listen signoff remains distinct from numerical FFprobe pass.
- Texture/readability: verify detail at both 100% and mobile display sizes, no flat low-poly boxes or repeated static PNG placeholder props.

## E. Genuine rights and policy gate
- Validate every on-screen game model, gameplay clip, voice, asset library and sound against rightsholder and source owner permissions. The parent game's fan policy is not a free blanket license to reuse other YouTubers' footage.
- No publisher logos or theatrical “official trailer” presentation; the credit slate should say **Unofficial fan animation — not affiliated with or endorsed by Mob Entertainment**.
- Poppy's game title may be referenced descriptively for audience discoverability only when compatible with Mob's restriction on dominating title branding. Main film title should be original: The Last Toy Shift.
- Recheck monetization / sponsorship separately. Do not assume YouTube revenue permitted by the game's fan-policy broad noncommercial framing.
- Proprietary raw models and source game audio must not be placed in public GitHub binaries or repos. Commit only original code + manifests plus redistributable CC0 assets with recorded licenses.

## F. Final artifact and GitHub handoff
- Verified master MP4, separate sound mix and stems, subtitle file, thumbnail (original artwork), project source and locked dependency versions, scene manifest, purchased/CC0 assets ledger, technical and creative QA, cut sheet and credits. Do not include restricted media in public downloadable source ZIP.
- If the user has trouble downloading from ChatGPT, use a GitHub **Release** for a verified file after upload is successful; verify release asset name, size, and actual download URL through GitHub API. Public raw asset licenses still govern release contents.
- Include a short proof of licensing, original art permissions and fan-content disclaimer in YouTube description.
- YouTube upload is not automatic: separate OAuth, final private review and user's explicit public approval.

## G. Status vocabulary (never misreport)
Research ready != files downloaded != scene graph running != hero-shot video != 11 scenes rendered != final MP4 technically verified != artistic approval != YouTube uploaded.

## H. Mechanical validation available now
Run the zero-cost manifest gate from repo root:

    python tools/video_production/validate_scene_manifest.py

It should pass the planning structure. Passing that command does NOT prove scenes or assets exist. The optional strict check:

    python tools/video_production/validate_scene_manifest.py --render-ready

**must fail** before assets have been genuinely downloaded/authored, approved and SHA256-matched. The separate GitHub Action only tests documentation/manifest consistency, not movie generation.

## I. Source documents
- https://www.mobentertainment.com/fan-content
- https://poppyplaytime.com/pages/chapter-5-broken-things
- https://threejs.org/docs/pages/WebGLRenderer
- https://threejs.org/docs/pages/GLTFLoader
- https://threejs.org/manual/pages/animation-system.html
- https://threejs.org/manual/pages/post-processing.html
- https://playwright.dev/docs/screenshots
- https://docs.polyhaven.com/en/faq
- https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
