# Pakistan Property Group — V8 Three Real Voices

A new review cut of the 9:16 premium layered HTML Canvas property comedy animation. Distinct source performances: a female off-screen Urdu-PK narrator (Uzma), the male on-screen Urdu-PK dealer (Asad), and male ElevenLabs user-supplied Zafar for the on-screen buyer. The characters do **not** use three artificially pitch-shifted copies of one recording.

## Audio-first pipeline

1. Research official Pakistan Urdu voice availability. `ur-PK-UzmaNeural` narrator and `ur-PK-AsadNeural` dealer, via free GitHub Actions Edge speech; exact per-line results stored in the audio source archive.
2. Preserve the user's supplied 95.399-second ElevenLabs Zafar MP3 locally, trimming only buyer dialogue sections from original V7 edited timestamps; never upload that original private file to GitHub.
3. Assemble 12 numbered voice cues with actual durations, short comedic pause after chai and buyer punchline, five-second animated subscribe outro. Dynamically rebuild Urdu subtitles and timeline; balance voice loudness, reduce music under dialogue, and add small original cues.
4. Modify HTML5 Canvas captions to show exactly the spoken Urdu text and mark who is speaking. Keep separate dealer/buyer PNG sprites, real animated paper graphics and existing stock footage; no new full-frame AI slides.
5. Render 60 timestamps per second in Chromium Canvas at 720×1280, upscale to 1080×1920 with high-quality Lanczos output and mux with the separate WAV soundtrack via FFmpeg. Existing 25fps video stock inside animated photographic cards is **not** native 60fps captured footage.
6. Run FFprobe plus sampled video contact sheet and integrity verification. A passed engineering report does **not** mean an acting-quality / actual lip-sync / speech-performance approval.

## Source files

- `build_three_voice_audio.py` - local assembly using GitHub TTS assets and existing user MP3
- `role_audio/` - 8 generated narrator/dealer lines and audit receipt (from GitHub run #39048260080)
- `premium_canvas.html` - 2.5D motion graphics, speaking-role treatment
- `render_html.py` - HTML Canvas renderer
- `mix_audio.py` - soundtrack mixing
- `qa_three_voices.py` - final verified media QA
- `audio_timeline.json` - all exact cue durations, role/voice source provenance
- `Urdu_Captions_V8.srt` - subtitle sidecar
- `docs/` - technical and voice reports, contact sheet

## Voice and visual limitations

- ElevenLabs buyer performance is user-supplied Zafar. Only narrator and dealer were newly synthesized (free voices). No new ElevenLabs credits or Gemini/Flow quotas were consumed.
- This video uses sprite-pose motion, not true viseme-matched character mouth animation, and original PNG fidelity limits extreme 2K closeups.
- Buyer's originally trimmed 4 dialogue excerpts must be listened to for unwanted section tags before release; human listening is required.
- The short is a fictional property-dealer satire with basic document-checking advice, not an allegation against an identifiable real agent.
- The user explicitly deferred generic skill updates until after the film, so do not create or modify skills as part of this release.