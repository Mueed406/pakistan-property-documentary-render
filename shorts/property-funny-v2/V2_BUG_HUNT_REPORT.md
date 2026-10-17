# PPG Funny Short V2 — Animation and Voice QA

## Verified defects in V1 source

1. **Scene wipe was nonfunctional:** the transition clipped and redrew the incoming scene twice, never the outgoing shot. **Fixed in V2** with a jagged paper matte preserving the last outgoing scene until the reveal reaches each pixel.
2. **No speech-driven mouth articulation:** faces held a static smile/confused/panic mouth through dialogue. **Fixed in V2** using 50Hz RMS measured from the actual generated narration with role-matched mouth movement.
3. **Crowded question slide:** the original buyer's face/body disappeared behind all three oversized labels. **Rearranged in V2** with reduced labels and buyer to the lower-right.
4. **Synthetic monotone acting:** Piper ur-PK voice was generated with one delivery speed; automatic 1.19× atempo compressed awkwardly long lines. **Replaced in V2** with individual Urdu neural lines; dealer and buyer have distinct pitch/rate settings. No automatic atempo. Provider and measured speech/total duration are recorded.
5. **Unverified musical clarity:** original synthesized score played across speech without proper RMS sidechain despite code's “Sidechain-style” comment. **Improved in V2** with voice-envelope-reactive attenuation, lower instrumental mix and punctuated comedic stings.
6. **Timestamps determined by approximation:** scene lengths in V1 depended on gap spreading and unverified pace. **Improved** with actual line audio lengths and an exported SRT and per-scene voice envelope. Visual release remains subject to human pronunciation and joke timing approval.
7. **Flat lifeless motion:** characters oscillated but did not react to speaking. **Improved** with restrained idle head movement, blink timing and speech-specific acting, plus mild time-dependent impact shakes.
8. **No frame-accurate cache validation:** V1 part rendering simply overwrote files. **Improved** with ffprobe frame count, geometry and fps check before reusing segments.
9. **Only 45s hardcoded partitioning:** V1 couldn't adapt if a better voice took longer. **Fixed** by computing actual duration from timed audio and rendering up to four 15s chunks (44–58s).
10. **No voice-provider trace:** V1 technical report was static on Piper. **Fixed** with a provider/length/paid-usage/approval quality report recorded in the final verified output.

## V2 release gates

- 10/10 new narrative lines synthesized to Urdu neural speech.
- Voice must be consistent with a casual, energetic Pakistani local comedy delivery, not an artificial caricature or a mono robotic narrator.
- Inspect every cut, in particular the scene 3→4 paper wipe and scenes 4→5 tea punchline. All animated characters must remain fully visible except intentional transitions.
- H.264, 1080×1920, 60 fps with exact total frames and AAC audio.
- Manually review Urdu sentence pronunciation, voice loudness, graphic overlap and role-specific mouth timing. Technical success does NOT certify artistic approval.

## Future premium TTS

ElevenLabs v4 supports Urdu, speaker/dialogue acting and emotional audio tags. Exact model/voice support, prices and available account credit must be verified before use. This repository includes an opt-in implementation **only** when ALLOW_PAID_TTS=1, ELEVENLABS_API_KEY and compatible voice IDs are explicitly configured as GitHub Secrets. No paid API key or credential is required for the review default. The default Edge-compatible route uses an unofficial cloud client; review provider terms before monetized use. Do not conceal provider limitations.

## Provenance

Source inspiration: general Pakistani real-estate sales comedy. Dealer and buyer characters are fictional. The skit is not a claim of misconduct against any identifiable broker or society. Buyer guidance is general information, not legal or investment advice.

## Status

Original V1 is preserved. V2 code changes are committed to its own branch, but may only be called *rendered* after a successful actual GitHub Release contains an MP4 and technical report. It should be shared as REVIEW ONLY until acting and animation earn human signoff.
