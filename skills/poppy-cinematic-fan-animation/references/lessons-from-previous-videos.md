# Reusable Video Engineering Lessons — PPG V1 through V8
**Recorded:** 2026-10-17. **Maintainer:** ABDUL MUEED LASHARY. This is documentation, **not an installed skill**.

## Verified previous work — avoid fictional status claims
- PPG property documentary: 410.4 seconds, 1920×1080 at 60fps, H264/AAC review film, 50 new motion scenes alongside 25fps source stock. [GitHub Release](https://github.com/Mueed406/pakistan-property-documentary-render/releases/tag/ppg-410s-editorial-1080p60-review-20261017).
- Property Comedy V7: 63.699s, 1080×1920 at 60fps H264/AAC review MP4. HTML Canvas/JS used 23 separate source PNG layers and inherited movie frames; Python for tooling, FFmpeg for mux/encode. Some graphics were initially drawn at 720×1280 then upscaled. [V7 production record](../property-comedy-v7/PRODUCTION_RECORD.md).
- Property Comedy V8: 54.695s, 1080×1920 at 60fps with separate Urdu narrator (Uzma), dealer (Asad) and user-supplied ElevenLabs Zafar buyer tracks. 12 timed voice cues, 5-second subscribe ending, 3,281 encoded frames; audio peak approximately -1.3 dB. [V8 voice record](../property-comedy-v8/VOICE_FIRST_PRODUCTION_AND_QA.md). [Real free TTS run](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39048260080).
- V7/V8 project ZIPs and completed MP4s were ChatGPT conversation artifacts, **not uploaded as binary assets to this repo**. Do not invent GitHub release paths for them.
- The private buyer MP3, fonts, paid templates and other restricted media have **not** been redistributed here.

## Lessons to reuse across projects
1. Research the content, production needs and asset licenses before designing scenes. Make a clear license and provenance ledger per source.
2. A timecoded storyboard is executable input: start_frame, frame_count, camera, rig, models, lights, SFX, dialogue, layers, transition and QA expectation.
3. Independent PNG layers are better than moving flattened posters; **for cinematic 3D go further with skeletal GLB/glTF meshes, procedural rigs and full camera/lighting animation**, not billboard characters.
4. Only one face/mouth rig should be active per actor. Avoid duplicate lips, mismatched eye masks, double faces, strange prop intersections and incorrect arm pivots.
5. Generate, name and independently retain every character dialogue stem; never put directions, numbering or character IDs in spoken text.
6. Actual phoneme/viseme alignment is needed for strong lip-sync. Audio amplitude alone is not accurate mouth animation.
7. Render native resolution when possible. 720p upscaling does not create 1080p source texture detail. Record true animation FPS separately from captured source video FPS.
8. HTML/CSS/Canvas/TypeScript and browser-driven Three.js can create true camera and environment motion; Playwright frame exports must use deterministic frame-index time rather than uncontrolled browser wall-clock timing.
9. Use Python for asset prep, hash manifest, SRT/audio timing, scene orchestration, and resumable local/GitHub build steps; FFmpeg/FFprobe are excellent for decode/mux/encode/QA but needn't author the visuals.
10. Blender is appropriate for professionally rigged characters, cloth, volumetric effects, simulated interactions and hero-shots that exceed a browser-render quality/performance budget.
11. Inspect every scene in context, not just ten static contact-sheet frames. QA every transition, freeze, texture loading, continuity, foot contact, realistic depth, 3D occlusion, captions, audio clipping and jokes/scares.
12. Cache sources with SHA256 and exact render settings. Repair only affected scenes rather than rerendering 50+ complete clips for one error. Record render resume state.
13. Image generation can provide reference art, material patterns, environmental concepts, original matte-painted elements, thumbnail candidates and masks. Generated **images are not editable 3D characters or mesh rigs** by default.
14. Use real licensed footage rather than scraping copyrighted YouTube video. Game fan-video permissions belong to each rightsholder's current policy. Never assume an asset is reusable because it is freely viewable.
15. A GitHub PR containing scripts is not a successful film upload. Delivery is only complete when an actual MP4 is verified and the exact file path or actual GitHub Release asset is available.
16. Stop paid voice/video calls when budgets or quotas fail. Earlier Gemini full Urdu voice stopped at HTTP 429. User-provided ElevenLabs audio does not imply connected ElevenLabs API credits.
17. Distinguish states: research / assets sourced / audio generated / shots rendered / full MP4 validated / artistically approved / YouTube private upload / public published.
18. Keep ChatGPT conversations in English while films use the requested speech language.

## Strict genre separation
The new Poppy Playtime fan film must NOT inherit the property documentary's paper-evidence diagrams, Urdu characters, generic dashboard cards, slow stock-overlays or rigid factual-claim cards. Reuse the engineering and QC methods, not the prior genre's look or story.

## Skill policy
The user previously directed us NOT to create/update the general reusable skills until a later explicit instruction. These notes are a skill-ready record only. No ChatGPT or Gemini plugin was modified by this document.

## New project source
See [Poppy fan animation handoff](../poppy-fan-animation-2026/README.md), its production plan, rights ledger, QA plan, asset manifest and new-chat prompt for the next production.
