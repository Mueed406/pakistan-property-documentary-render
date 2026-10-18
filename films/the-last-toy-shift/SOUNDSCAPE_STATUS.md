# Soundscape / Foley production — no voice lines yet

An **original deterministic 90-second stereo soundscape** can now be generated locally or in CI as four **separate 48 kHz WAV files**: factory ambience, time-coded industrial/toy/footstep Foley, restrained tension score, and a temporary combined mix. It uses only NumPy and mathematical synthesis, not proprietary game samples, original Poppy music or third-party clips.

```bash
cd films/the-last-toy-shift
python3 -m pip install numpy
python3 scripts/soundscape_90s.py --out output/soundscape
ffmpeg -i output/soundscape/TEMP_90S_MIX_NO_VOICES_NOT_FINAL.wav -c:a aac -b:a 192k output/TEMP_90S_MIX_NO_VOICES_NOT_FINAL.m4a
```

Events cover machinery, sparks, toy necks, cassette tape, electrical malfunctions, collision/door strikes, stylized pursuit footfalls, an impact sting and deliberate blackout. Music ducks around **anticipated dialogue windows**, but these are guides only: actual approved actor takes must be aligned to each final shot and ducking adjusted to each word.

The temporary synthesized sound is **not professionally recorded English dialogue** and cannot be substituted for the requested multiple expressive performances. A draft mix passing FFprobe does not pass a human listening assessment.

Separate stems must be kept so SFX/music can be revised without rerendering the 3D shots. Rights/source record: 100% original programmatically authored soundtrack; source is this repository's `scripts/soundscape_90s.py`. No official soundtrack or voice actors used.

The existing final-rights and media validation remain locked. There is no full 90-second completed animated MP4.
