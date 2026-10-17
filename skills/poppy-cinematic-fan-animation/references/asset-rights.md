# Poppy Fan Animation — Asset, Source and IP Rights Ledger

**2026-10-17 research.** Everything below is a source candidate or legal reference, **not a downloaded model/clip unless its status explicitly says acquired**. No third-party proprietary media was uploaded to this GitHub branch.

## Rights-holder policy comes first

**Mob Entertainment — [Fan Content Policy](https://www.mobentertainment.com/fan-content)** is the governing source for Poppy-related use (together with applicable other agreements). It permits some fan generated content, even certain game asset use, subject to non-commercial limits and exceptions; prohibits implying official endorsement and prohibits redistribution/sale of game content. Verify **the exact contemplated video, monetization, sponsorship, model extraction, voice, reuse, third-party footage and publication plans** against that policy or obtain permission before release. Do not copy other YouTubers' gameplay without their permission. Mob's permission to make fan content does not transfer the independent rights of the creator of a recorded gameplay clip.

- Official [Chapter 5: Broken Things](https://poppyplaytime.com/pages/chapter-5-broken-things) establishes Feb 18, 2026 release.
- [Official news](https://poppyplaytime.com/blogs/news).
- No official studio/company logo as our logo, no deceptively official title/trailer claims, no ripped game binary posted as project/source ZIP.
- Credit and label: **“The Last Toy Shift — An Unofficial Poppy Playtime Fan Animation. Not affiliated with or endorsed by Mob Entertainment.”**
- Unless rights review says otherwise, **private/noncommercial original fan story** is the safest default; don't assert YouTube ads are approved just because views are free.
- Rights questions about game model use, passive video ad revenue and download distribution must be confirmed from the actual policy, not guessed.

## Asset source categories, with current status

| Asset category | Good source / technical use | Current permission assessment | Current status |
|---|---|---|---|
| Huggy Wuggy / Poppy/GrabPack likeness | User-created fan mesh/animation or authorized game model for an eligible fan video | **Mob fan policy conditional**, never redistribute extracted source model | **NOT ACQUIRED** |
| Gameplay footage | Direct clean capture from own authorized game session, subject to publisher rules | Capturer rights + Mob terms; official trailers/public uploads not a blanket footage license | **NOT CAPTURED** |
| Factory meshes and original props | Modeled uniquely in Blender or procedural Three.js primitives | Original asset license; suitable for rendered clip | **NOT BUILT** |
| PBR dirty concrete/rust/industrial HDRI | [Poly Haven](https://polyhaven.com) | [CC0 official confirmation](https://docs.polyhaven.com/en/faq), per-file integrity required | **RESEARCHED, NOT DOWNLOADED** |
| Humanoid mocap / skeletal motion | [Adobe Mixamo](https://www.mixamo.com) | [Adobe FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html): free royalty-free use in films, but their standard auto-rigger targets bipedal humanoids; *compatibility with toy shape unverified*. Don't redistribute raw clips as product | **RESEARCHED, NOT DOWNLOADED** |
| Artist-owned glTF factory sets | [Sketchfab](https://sketchfab.com) Creative Commons catalog | [Sketchfab CC attribution](https://sketchfab.com/developers/download-api/guidelines); model-specific license/author and forbidden brand infringements still apply | **RESEARCHED, NOT DOWNLOADED** |
| Original English voices | Authorized human actors, permitted TTS voices, clean separately produced sound | Audition / explicit provider terms / no cloning official actors without rights | **NOT GENERATED** |
| Ambience, factory machines, VHS, impact sound | Original sound design or individually licensed SFX libraries | No original game score or third-party copyrighted song without permission | **NOT ACQUIRED** |
| Generated artwork | Image generation for concepts, matte backgrounds, labels, rough maps, texture ideas, poster/thumbnail | Store generation origin and verify no trademarks/false official claims | **NOT GENERATED FOR THIS PROJECT** |
| Motion templates | Mixkit / Motion Array / Uppbeat / Jitter as optional references; original native 3D motion prioritized | Individual license, file access, editing compatibility, attribution requirements | **NOT ACQUIRED** |

## Reusable source libraries & authoritative tech references
- Poly Haven original CC0 materials and HDRI: https://polyhaven.com
- Adobe Mixamo bipedal animations: https://www.mixamo.com
- Sketchfab CC model download caveats: https://sketchfab.com/developers/download-api/guidelines
- Three.js GLTFLoader + PBR material support: https://threejs.org/docs/pages/GLTFLoader
- Three.js skeletal/morph AnimationMixer: https://threejs.org/manual/pages/animation-system.html
- Blender glTF pipeline: https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html
- Official publisher fan content conditions: https://www.mobentertainment.com/fan-content

## Concrete provenance structure
For EVERY acquired file: ID, type, origin URL, owner, title, license statement and full license URL, acquisition date, attribution text, stored local/private path, SHA256, width/height or mesh polycount/texture resolution, rig compatibility, intended shot, transform and permission-to-redistribute flag.

**DO NOT** commit raw game models, copyrighted trailers, user proprietary game captures, private ElevenLabs audio, vendor project templates or secret keys. Put authorized protected raw footage in a user-owned private asset store; the public repo should contain original code and non-sensitive manifests. Only upload freely redistributable assets when their own terms explicitly allow it.

## Audit gate
A source marked 'RESEARCHED' or 'NOT ACQUIRED' cannot be used in the final render. Block rendering of any shot whose required asset has no confirmed local file and verified SHA. Block publication until all visible/audio assets have confirmed rights for the *intended* use, even if technical video checks pass.
