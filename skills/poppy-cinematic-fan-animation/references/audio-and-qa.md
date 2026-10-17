# English Dialogue, Horror Sound and Final Film Quality Gates

The example film is **90 seconds, 5,400 frames, 1080×1920 vertical 60fps**. These values change when the user's explicit requested runtime or ratio changes. The narrative and performance direction below are ORIGINAL fan fiction, not official Poppy Playtime canon or copied game dialogue.

## Original vocal roles — audition separately

1. **Hero / player** — adult English-speaking protagonist with low, natural conversational register, tension carried by breath, clipped hesitation and genuine panic rather than continuous yelling.
2. **VHS / factory recording** — distinct voice, slightly narrowband and eerie but intelligible. Effects only after a clean original stem is secured.
3. **Mysterious doll-like voice** — original voice performance. Do **not** clone or imitate an identifiable game actor without authorization.
4. **Creature / toy movement** — original breaths, toy creaks and nonverbal voice/SFX, never another creator's copyrighted sound pack without license.

### Sample English lines for ORIGINAL story

- Hero (quiet, uneasily amused): “It's just another shift. Right?”
- Tape voice (dry, degraded recording): “Don't follow the footsteps.”
- Hero (under breath): “Who's there?”
- Hero (urgently): “Come on. Open!”
- Mysterious voice (close, calm): “The door isn't locked to keep you out.”
- Hero (almost silent): “Then what's inside?”

For any generated speech, store **only the words meant to be spoken** in the TTS text input. Actor direction belongs in a separate metadata field or in supported voice direction controls, NOT in the narration string. This prevents the previous project's issue where voices spoke line numbers, role tags and instructions.

Each exported stem should have file name, actor ID, source/rights, engine/version and approved preset, scripted words, actual length in samples, waveform peak and session rate, waveform-derived timing, and timestamp/phoneme or viseme alignment if the actor's lips are visible.

## 3D performance synchronizes TO approved sound

- Record/choose best actor takes first; actual time boundaries determine movement and scene length.
- Lip sync uses phoneme/viseme alignment or human keyframes. Audio amplitude can drive mouth-open *rough drafts* but isn't accurate lip sync.
- Allow reaction anticipation, breath pauses and cut-to-silence to enhance horror. No filler narration over every shot.
- Use environmental sound perspective: approaching footsteps gain proximity, impacts have material-dependent timbre, reverberation fits hallway geometry, industrial machinery has spatial movement.
- Mix distinct stems for hero, tape, eerie voice, footsteps, ambience, tension, impact, music. Check for clipping and intelligibility at smartphone volume.

## Original music and sound sources

Build an original tension bed or use rights-verified library audio. Avoid unlicensed official game soundtrack, streamer reaction audio, ripped game sound effects and generic copyright-unclear marketplace samples. If video has sponsorship, monetization, public posting or downstream reuse, verify each source's license for that use.

Suggested cue arc:
- 0–20s: distant machinery, low electrical hum, uncomfortable quiet.
- 20–36s: tape whir / abrupt crackle and distant metal footstep.
- 36–55s: accelerating multi-channel chase, differentiated footsteps, conveyor rumble, cable swing.
- 55–76s: controlled near silence, close whisper, subtle low-frequency tone.
- 76–85s: short action payoff and sharp synchronized transient, **not** wall-to-wall distorted noise.
- 85–90s: restrained original tail, unofficial fan credits.

## Technical validation (non-negotiable)

Validate a real final video with FFprobe:
- duration equals manifest within 1 frame (for 90s at 60fps, 90.000 ± 0.01667s nominal, with codec padding tolerances noted).
- dimensions 1080×1920 (for default vertical).
- frame rate 60/1 for **generated visual motion**, 5,400 expected video frames when output duration is exactly 90s.
- H.264 yuv420p (or another format explicitly approved), AAC audio at 48kHz with proper duration and no clipping.
- Verify each render shot file and frame count independently; detect missing or duplicate boundaries.

Creative QC:
- Review every scene at full resolution and at smartphone size.
- Capture at least one contact frame from each shot AND frames −2, 0, +2 near every cut.
- Inspect for clipping, broken depth sorting, overly dark frames, texture seams, spurious bright pixels and shader-loading artifacts.
- Watch full film with sound and verify identity/character continuity, tense pacing, animation energy and role correctness.
- Test skeletal hand/foot/prop contact and ensure props don't teleport.
- Check dialogue not cut mid-word, speaker roles genuinely distinct, meaningful long silences intentional, no spoken TTS instructions.
- Review copyright/asset receipts before posting; technical QC does NOT equal artistic or legal approval.

## Technical vs publication status

Machine validation should label the export `FULL_MP4_VALIDATED` only if it exists and passed. The movie becomes `CREATIVE_APPROVED` only after visual/listening review. Uploading a file to GitHub is NOT posting it to YouTube; publishing a video publicly additionally requires account authorization and explicit user approval.

Output package should contain clean master MP4, validated low-size viewing copy, English script and captions, separated audio stems, scene/frame manifest, asset ledger, original coding project and dependency lock, QC report and known issues. If a GitHub Release hosts the MP4, verify the asset's existence and size via API before linking.

## Runtime and budgeting

Before downloading or calling paid model APIs, inspect quotas and user permissions. Prefer high-quality asset research and one key hero-shot test over repeated full-length low-quality renders. Do not claim “100× better” from a single aesthetic tweak. Preserve complete healthy sections for repairs.

## Fan-content disclaimer

Use a clear end credit and upload description:
`An unofficial Poppy Playtime fan animation. Not affiliated with or endorsed by Mob Entertainment.`

Check the [rights-holder's current fan content policy](https://www.mobentertainment.com/fan-content) before monetization, sponsorship or distribution. Do not assume normal YouTube monetization is allowed.
