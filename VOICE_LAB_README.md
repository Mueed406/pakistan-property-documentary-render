# Free Urdu Narrator Quality Lab

No Azure or ElevenLabs account required. GitHub Actions synthesizes **three variants of the same Pakistani Urdu narration** with the openly licensed Piper `ur_PK-fasih-medium` model.

- **A** — reference settings from the existing documentary.
- **B** — calmer pacing, reduced phoneme-duration variation, subtle dynamics processing.
- **C** — controlled pacing and slightly gentler spectral balance.

Download the `free-urdu-piper-voice-a-b-c` artifact from the latest **Compare free Pakistani Urdu voices** workflow, listen to A/B/C, and choose the least artificial version. Be aware: no DSP setting can fully correct a "crying" tone originating from the underlying trained model. If all fail, choose a better licensed Urdu TTS model or human narration.

The seven-minute render workflow is **manual trigger only** while voice evaluation is underway, to avoid accidentally publishing or rerendering the bad voice on every commit. It can be started from GitHub Actions when a profile is approved.

These are review previews, not publishable voiceovers.