# Poppy Playtime 2D Short V2 — production handoff

Owner: ABDUL MUEED LASHARY | Fan animation | Reference: https://youtube.com/shorts/Fgjda1vEAkA

## Status, not a claim of final delivery

A new motion-comic review, AI-generated 2D storyboard/character art and original timed SFX exist in the companion conversation package **Poppy_Playtime_V2_Asset_Project.zip**. A new natural-sounding 16.431-second male narration has been generated with HeyGen (Marco voice, Orca engine), but the hosted WAV could not be mounted in the local render container, so **the review MP4 is SFX-only** and must not be published as the finished version. It is not yet an exact reproduction of the external reference: that Short could not be inspected frame-by-frame.

Do **not** reuse the previous robotic narrator or represent the old v1 as final.

## Creative specification

- Format: original 2D comedy fan animation, vertical 9:16, target 1080x1920, 30fps, approximately 17–18 seconds.
- Style: punchy frame-by-frame or 2D cutout animation; thick ink lines, cel shading, deliberately crude expressive motion; no glossy AI/photorealistic visual style, no fake 3D.
- Characters: blue wide-mouthed Huggy with yellow palms, purple sleepy CatNap with yellow moon accent; keep eye and mouth shapes consistent between shots.
- Plot: Huggy discovers CatNap’s alarm, ignores the red “DO NOT PRESS” button, triggers beeps, CatNap snaps awake, brief chase, Huggy trips, then becomes CatNap’s pillow.
- Sound: original male narration, no voice cloning of the source creator; physical button click, 3 alarm beeps, room tone, sprint footsteps, bass hit, splat and punchline.
- User channel: Abdul Mueed Lashary YouTube. **Do not publish without explicit approval.**

## Narration, voice and precise events

HeyGen Marco/Orca 16.431s male voice exists in the conversation with downloadable audio. Source must be saved locally to `male_narration.wav` before muxing. Never publish a version with the previous synthetic robotic voice.

| Time (sec) | Event |
| ---: | --- |
| 0.22 | Huggy hook begins |
| 1.61 | alarm clock mentioned |
| 3.67 | “DO NOT PRESS” |
| 5.84 | Huggy presses it |
| 6.44 | “BEEP!” and impact cue |
| 7.41 | CatNap wakes |
| 8.72 | “RUN!” |
| 9.28 | “FASTER!” |
| 10.70 | behind-you chase |
| 11.19 | shocked scream / slip |
| 13.77 | pillow reveal |
| 15.79 | final “Alarm!” |

Script: “Huggy Wuggy found CatNap's alarm clock. Big red button... says DO NOT PRESS. So OBVIOUSLY, he presses it! BEEP! ... Oh no. CatNap's awake. HUGGY, RUN! FASTER, BRO! He's RIGHT behind you! AHH! ... And that's how Huggy became CatNap's personal pillow. Never. Touch. The. Alarm.”

## Asset manifest

- AI-generated character sprite pose sheet — original newly generated art, multiple expressive Huggy / CatNap poses.
- AI-generated storyboard panels — original newly generated art.
- Kinetic 2D animatic generator, extracted artwork, SFX WAV and caption guide — in downloadable conversation ZIP (assets not yet pushed as GitHub binary files).
- No third-party game models, SFX or reference audio were downloaded or redistributed. If obtaining any later, record source, license and attribution; never claim third-party character use is automatically cleared.

## Render procedure

1. Download and unpack `Poppy_Playtime_V2_Asset_Project.zip` from the corresponding ChatGPT conversation. Keep `generated_assets/` adjacent to `render_v2.py`.
2. Download the **Marco** WAV from the embedded HeyGen player as `generated_assets/male_narration.wav`.
3. Run `python render_v2.py`; it will render its generated animated 2D comic visuals and mux voice only when this file is present.
4. For instant voice swap against the existing SFX review, use `scripts/poppy_voice_mux.py` from this PR (requires FFmpeg) and pass `--video` and `--narration`; it will preserve the visuals and mix the narration with the existing SFX.
5. Check audio (intelligibility, speech levels, effects ducking, no clipped peaks), typography and motion at frames ~5%, 25%, 50%, 75%, 95%; verify portrait dimensions and codec before any release.
6. Refuse publishing if male narration is missing, if visual glitches remain or if source-reference similarity has not been personally reviewed.

## Limitations/next pass

The user's exact external reference Short could not be viewed with available tooling. Uploading that clip into the workspace would enable actual shot-by-shot timing and artistic comparison. The current image assets are freshly generated but an improved hand-directed character animation pass and final synchronized audio merge remain required before final sign-off.

This branch is intentionally a non-destructive handoff + offline-ready utility. It does not overwrite any working documentary/video production pipeline.