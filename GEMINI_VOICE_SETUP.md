# Gemini Urdu narrator experiment — no Azure needed

**Goal:** Fix rushed connector words, uneven syllable length, unnatural pitch and crying-like Piper delivery by auditioning a different neural TTS model with natural-language direction.

1. Open https://aistudio.google.com/api-keys and create an API key in a **free-tier** project. Check whether your account is eligible, and confirm no paid billing will be used.
2. Open https://github.com/Mueed406/pakistan-property-documentary-render/settings/secrets/actions
3. Under Repository secrets, select **New repository secret**, enter name `GEMINI_API_KEY`, and paste its value privately. **Never paste the API key into this chat, issues, or source code.**
4. Open https://github.com/Mueed406/pakistan-property-documentary-render/actions/workflows/gemini-urdu-voice-test.yml and click **Run workflow**.
5. Download the artifact `gemini-urdu-documentary-auditions`, listen to `urdu_charon.wav` and `urdu_schedar.wav`, and compare against the earlier Piper B.

The selected model is `gemini-2.5-flash-preview-tts`. Google's documentation lists Urdu support and a free tier, but availability and quota depend on your account and region. The workflow intentionally generates only two short samples (two calls) and is **manual-only**. It does not charge automatically, subscribe to anything, or publish to YouTube. If the account has paid billing enabled, API usage may be billed according to your project's pricing; verify before running.

**What changes:** Gemini TTS accepts style and cadence guidance, so we can direct broadcast speech, natural phrasing, and a steady Pakistani Urdu accent. It may still fail to pronounce some words or produce an authentic regional accent; listen first.

**What does not change automatically:** Creating a key does not make the video render with Gemini. The full narration engine and captions must be migrated after audio approval, with measured duration and text verification. Piper B remains available offline.

Reference: https://ai.google.dev/gemini-api/docs/speech-generation
Pricing: https://ai.google.dev/gemini-api/docs/pricing

Only 2 auditions; no retries after errors; no premium fallback. The test includes offline validation and a fail-closed no-key check.