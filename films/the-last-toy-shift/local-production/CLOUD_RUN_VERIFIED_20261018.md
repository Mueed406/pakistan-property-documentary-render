# Actual cloud-generated English TTS and SFX — Verified 2026-10-18

## Real GitHub cloud execution

- **GitHub Actions:** [successful Run #39097760161](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39097760161).
- **Workflow:** `.github/workflows/last-toy-shift-cloud-kokoro-90s.yml`.
- **Executable engine:** `local-production/cloud_kokoro_90s.py` with [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx), CPU only on GitHub's standard Linux hosted runner. **No user's PC CPU or GPU was accessed. No remote GPU was used.**
- The model binary and voices were retrieved from the creator's official release and verified by SHA-256 before inference:
  - Kokoro v1.0 ONNX: `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a`.
  - Kokoro v1.0 voices: `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`.
- **Actual voice generation:** Six timed English phrases across three distinct model voices (`am_michael`, `am_adam`, `af_heart`). Separate 90-second 48kHz stereo WAV stems + an aligned SRT, plus a real 90-second AAC listening mix with the previously generated original Foley/music/SFX soundbed.
- FFprobe confirmed **90.000 seconds** exactly, **48kHz**, **2-channel AAC**. Separate role WAVs each contain **4,320,000 samples at 48kHz**, 90.000 seconds.
- Inference used `CPUExecutionProvider`, as independently captured by the generated QA manifest. Generation and mixing after model load finished in **7.2 seconds**. Entire workflow setup and download adds time.
- Combined audio SHA-256: `4e9054332da14b9c1789d666bea4934860defedb5c46a8bf69b1c5cc587f3be7` (3,075,572 bytes).
- Artifact ID `12125317661` stored in GitHub Actions, retention **14 days**. Download: [GitHub run artifacts](https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/39097760161).
- Source/model licensing: `kokoro-onnx` MIT; Kokoro model Apache-2.0. No licensed game music, scraped actor voices, or celebrity/character imitation were introduced.

## Actual spoken English cue durations

| Role | Cue start | Rendered spoken duration | Original dialogue |
|---|---:|---:|---|
| Hero | 7.2s | 2.3873s | It's just another shift. Right? |
| Tape | 22.5s | 1.662s | Don't follow the footsteps. |
| Hero | 31.2s | 1.0866s | Who's there? |
| Hero | 50.2s | 1.408s | Come on. Open! |
| Doll | 59.0s | 2.1153s | The door isn't locked to keep you out. |
| Hero | 71.1s | 1.5787s | Then what's inside? |

## Full film quality and release status

**Audio draft only.** No professional voice acting approval, no 1080×1920 finished VFX or completed 5,400-frame cinematic film. This cloud CPU TTS success DOES NOT clear final character asset rights, full video rendering, native resolution, or film delivery. PR remains draft. Do not misrepresent this voice-only M4A as the finished animated movie.

## Reproduction with no paid API

On any compatible Linux machine / GitHub cloud:
```
cd films/the-last-toy-shift
python3 -m pip install -r local-production/cloud-requirements.txt
python3 local-production/cloud_kokoro_90s.py --output output/cloud-kokoro
```
The first run downloads checksummed official Kokoro ONNX weights. A cache in GitHub Actions avoids repeated public model downloads. Read `CLOUD_TTS_QA.json` before publishing claims.

A genuinely expressive Chatterbox project with consented reference voices would require separately running its actual model with real authorizations. The current successful Kokoro audio is a fast baseline, not proof that Chatterbox, CUDA/DirectML or any local hardware has been exercised.
