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

## If GitHub Gemini audition fails with HTTP 403 "Your project has been denied access"

This is a Google project/account access denial, **not** an audio script bug, unsupported Urdu text, GitHub runner OS, or a missing secret. On Run #38970266120, GitHub found the secret and passed all five offline tests. The first Gemini API generation call returned this exact denial.

Official Google API errors documentation calls HTTP 403 `permission_denied` and advises reviewing API key permissions and project access. Google's developer forum has staff instructions to:
- Open Google AI Studio **Dashboard → Projects**, and review **Billing** for any account/project warning or "Unavailable" status.
- Open https://console.cloud.google.com/ and select the Google Cloud project associated with this API key. Inspect the console home page for a denial/review/appeal banner.
- Use Google's indicated appeal route or contact Google support; report the 403, region, sanitized timestamp, and project ID privately (never paste API key).
- Do not automatically retry a 403, create multiple keys to evade a restriction, or enable paid billing as a speculative fix.

The job now uses `actions/checkout@v5` and `ubuntu-24.04` to remove unrelated Node 20 / migration warnings. It remains manually triggered and makes no further calls until you explicitly start it.

Helpful guidance:
https://ai.google.dev/gemini-api/docs/api-errors
https://discuss.ai.google.dev/t/403-permission-denied-your-project-has-been-denied-access-new-account/143684
