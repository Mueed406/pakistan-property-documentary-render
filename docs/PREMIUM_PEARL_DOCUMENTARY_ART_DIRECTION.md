# Pakistan Property Group — Premium Pearl Film Art Direction (v4)

## Visual objective

Replace the old AI-like dark navy, glowing-grid animations with the restrained editorial elegance of premium investigative documentary editing. **Live moving licensed stock footage remains visible behind every motion sequence.** During information-heavy shots, soften/defocus the video but never erase source context. White/pearl documentary graphics appear over it. Never call 2.5D illustrations real site imagery.

### Official palette — restrained neutrals

| Token | Hex | Editorial use |
|---|---|---|
| Pearl | `#F8F8F5` | Primary animation paper / storytelling surface |
| Studio White | `#FFFFFF` | Diagram panels and printed legal documents |
| Platinum | `#EBEDF0` | Secondary architectural / bar chart material |
| Soft Mist | `#DCE1E4` | Keyline dividers, muted map boundaries |
| Silver | `#B7BEC5` | Technical survey lines |
| Graphite | `#252B32` | Numerals and large headlines |
| Slate | `#626D77` | Supporting text, factual qualifiers |
| Warm Bronze | `#9A8061` | Single, restrained accent for report claims |

Absolutely no neon purple, cyber-gradient or fake glass-dashboard cards. Chroma key `#FF00FF` is an **internal transparent video matte only**, never a user-facing design color.

Use one clear subject per animation shot, roughly 60–70% of frame as the editorial stage. Preserve the bottom 295 pixels from the original unblurred footage, keeping already-rendered RTL Urdu subtitles readable.

### 24 narration-matched conceptual motion chapters

1. Original file promises
2. Who owns the actual land
3. File != physical parcel
4. Reported 42,000 files / 6,000-plot capacity comparison
5. Geographically UNGROUNDED conceptual plot-lattice
6. Reported discrepancy (36,000), explicitly alleged
7. Plot supply finite
8. Physical plot identity
9. Approved layouts / buildings
10. Construction evidence
11. Legal document originals
12. Payment documentation
13. Investigative questions
14. Evidence trail
15. Differentiating approvals
16. Certificate versus NOC
17. Map and paperwork checks
18. Comparing supporting evidence
19. Before paying
20. Verify official records
21. Match ownership to plot ID
22. Physical site visit
23. Independent qualified lawyer
24. Conclusion: proof before payment

Never claim shot 5/17 is an actual satellite map of the investigated Islamabad site; it's an **illustrative diagram**. There are no fictional charts implying actual year-over-year datasets. Only use the reported 42,000/6,000/36,000 figures with attribution.

### Production implementation

- `browser_motion/premium_pearl_motion.html` contains the original source for 24 scene-by-scene animated plates. 1920 × 1080 @25fps.
- `browser_motion/render.mjs` captures frame-exact images from Chrome/Edge and sends H264 yuv444p footage to FFmpeg.
- `browser_motion/premium_full_assemble.py` reuses the verified real-stock 410-second master; softly blurs/desaturates moving footage only while the graphic is present, keeps subtitle strip crisp, uses matte transparency, re-assembles time-coded shots with original complete soundtrack/audio.
- `.github/workflows/render-premium-pearl-full.yml` parallelizes motion rendering across 4 runners (six new chapters each), then exports the feature film at actual Full HD resolution, preserves source code and SRT, runs engineering QC.
- Windows CLI: `python studio_cli.py render-premium-pearl --base baseline/renders/Pakistan_Property_Stock_Documentary_FINAL.mp4 --srt baseline/urdu_timed.srt`

### Required agent skills, available for opt-in Windows installation

```powershell
.\windows\Install-MotionSkills.ps1 -Install -Global -Advanced
```

Specific new skills validated in a GitHub runner (separate from real PC): `color-motion`, `animation-principles`, `chart-animation`, `animated-infographic`, `map-animation`, `cinematic-camera`. Sources and licenses must be maintained from their upstream repositories. Use the skills to govern palette, actual data geometry, map integrity and timing.

### Creative acceptance

A technical MP4 codec pass does not prove top-notch quality. Human review must verify:
- Arabic/Urdu glyph shape and visual alignment; no clipping; original subtitle legibility over new clips.
- **No raw chroma-magenta leakage**; no burnt white blocks eliminating actual stock context.
- Graph meaning exact; correct text; no invented measurements; legible numbers; adequate pacing.
- 410–411 seconds, 1920x1080 25fps, AAC audio and 83 subtitle cues.
- No slideshow/repetitive filler; each animated chapter has a distinct claim and tailored visual metaphor.
- Existing Piper narrator retains robotic artifacts. Do not label the film a final master until improved Gemini narration is approved.
- Export visual contact sheet and source provenance, no YouTube publication until approval.

### Honest limits

Current base footage may contain locations outside Pakistan (stock is illustrative). Full Gemini natural voice replacement has not yet been done; voice is unchanged in this render. No paid account or services are enabled. The browser animation is sophisticated 2D/2.5D, **not photoreal 3D**; true architecture 3D requires a separate licensed Blender render. Our color grading is restrained and cannot make unrelated stock location-accurate.
