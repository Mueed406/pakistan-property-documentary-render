# Audio mastering and editorial timeline exporter

**Audio**: `python audio/master_urdu_voice.py --input urdu_voice_gemini.wav --output renders/urdu_voice_mastered.wav`. Uses Spotify's `pedalboard` for restrained EQ, compression and limiter, plus FFmpeg EBU loudness normalization. Do not re-master a voice repeatedly. Listening check is mandatory.

**Professional editor interchange**: `python editorial/export_otio.py --decisions renders/edit_decisions.json --out renders/review.otio`. Uses Academy Software Foundation's OpenTimelineIO. This is an editable decision list, not a promise that every effect from FFmpeg converts to another NLE.

**Why**: Audacity/Shotcut/DaVinci Resolve may be useful for hands-on finishing, but a command-line automation must rely on programmatic primitives. Paid software and untested VST binaries are unnecessary.
