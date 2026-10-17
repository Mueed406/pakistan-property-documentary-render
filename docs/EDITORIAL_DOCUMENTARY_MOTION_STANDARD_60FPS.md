# Editorial Documentary Motion Standard — 60 FPS archival collage

**Working outcome (17 October 2026):** a real 25.6-second 1920×1080 H.264/AAC 60fps moving-graphics documentary segment, and a 43.235-second continuity test mixing original source footage with the new full-screen paper animation. The sample reuses the original Urdu narration from 00:33.672 to 00:59.272. These are **review cuts, not the final 410-second release**.

The original successful 6:50 Premium Pearl movie remains unmodified. The tested standalone Python animation source and cleared-asset manifests are included in the user's portable `PPG_60FPS_Editorial_Source_Project.zip` delivery; that ZIP also includes the user-preferred earlier AI collage image as an illustrative source asset.

## Mandatory production direction for future documentary skill updates

Every documentary production must evaluate story-driven mixed-media motion as a core available visual treatment instead of producing generic dashboard cards or requiring continuous background stock video. Use editorial judgment: select full-screen paper collage, real moving footage, maps with verified data, document demonstrations, licensed still images, photographic cutouts, true 3D or hybrids based on the spoken passage. Do not mechanically overlay stock footage behind all animation.

### Identity and hierarchy

- Cream archival paper, genuine texture, worn fiber, subtle grain, halftone and Xerox artifacts; graphite text, warm mustard-yellow evidence highlights, restrained red ink and underline marks.
- Primary numerical display: **Inter Display Black** (major headlines). Narrow chapters: **Roboto Condensed Bold**. Editorial serif contrast: EB Garamond / approved local serif. Archival metadata: approved monospaced type. Urdu captions: Noto Sans Arabic with correct RTL shaping and readable contrast.
- The Inter font family is openly licensed under SIL OFL; check each other font's actual licensing terms before redistribution. Never send proprietary font binaries to users.
- A background must itself communicate editorial context. Avoid large empty black rectangles, cheap generic gradients, unexplained futuristic neon, flat web dashboard layouts and fake document reproductions.

### Actual animation grammar

- Render 60 distinct frames per second for newly created motion; do not relabel duplicated legacy 25fps footage as newly animated 60fps.
- Layered paper cutouts must have independent scale, translation, rotation, depth shadow, micro-jitter and carefully motivated parallax.
- Retained-motion choices: torn-paper reveals; newspaper clipping slide; photo-plane camera moves; 2- and 3-frame held stop-motion cycles over smooth 60fps camera and ink; animated scribbles with **correct target anchoring**; yellow paint-swipe reveal; tape/marker underlines; masked cutaway; full-frame paper-to-footage transitions; documentary camera push-ins and kinetic type.
- Reveal large numeral and accompanying qualifier together. For the reported 42,000 / 6,000 / 36,000 scene, numbers must never be mistaken for verified legal findings. Preserve the approximate/alleged context on screen.
- Narration-led cues must be tied to real Urdu SRT timestamps, never evenly distributed to fill the runtime.
- Avoid unnecessary effects. Support the evidence and make explanatory motion more legible than a motionless card.

### Source and accuracy

- Original investigative subject: reported May 2026 Islamabad cooperative housing controversy. The figures are allegations, **not court findings**.
- All externally acquired photography needs license, creator/source URL, acquisition time and digest, with attribution when required. Generic stock photographs are **not** evidence of the investigated site or an alleged suspect.
- Illustrative maps, boundaries, approval papers and ownership documents must be labeled as conceptual rather than disguised as official records.
- Never copy Vox or another creator's brand identity, logo or proprietary animation templates. Emulate general editorial design methods through original art and code.
- Full-film Piper narration remains to be replaced only after approved natural Pakistani Urdu audio samples and authorized TTS usage.

### Reproducible 60fps animation pipeline

- Python 3.11+, OpenCV, Pillow, NumPy for frame-accurate 2.5D art and text layer preparation.
- FFmpeg 7+ and FFprobe for H.264/AAC encoding, video join, subtitle burn, uninterrupted original audio and complete engineering QC.
- Four proven story beats: approximately 42,000 alleged issued files; approximately 6,000 stated capacity; approximately 36,000 reported discrepancy; clear non-verdict disclaimer.
- Project outputs: 25.6s moving sample and 43.235s stock → full-screen collage → stock continuity test.
- One canonical source file `build_premium.py` builds true 60fps 1080p documentary sequence, then aligns source SRT/voice from 00:33.672. `integrate_existing_master.sh` is the continuity assembly driver.
- Documentary runner should be deterministic: once assets are approved, cache originals, create separate timeline segments, render in parallel, join at 60fps, rebuild timed subtitles on any audio change, check every section and mix sound with safe peak/loudness.
- Native source film was produced at 25fps: when included in a 60fps timeline, mention that existing captured footage's motion does not magically gain 60 unique captured frames.
- Store the source image, texture assets, licenses and executable scripts with each finished video; retain the proven original master alongside all revisions.

## Acceptance gate for 410-second replacement

Do **not** claim a final 410-second upgraded documentary is complete until all editorial sections are redesigned to the agreed quality bar, licensed assets are audited, clean Urdu narration is approved, subtitles/sound are synchronized, technical FPS/codec checks and scene-by-scene creative QC pass, and a final playable master MP4 actually exists.

## Official research

- Inter font and SIL OFL: https://github.com/rsms/inter
- Wikimedia Commons: https://commons.wikimedia.org
- Existing fact source: https://www.geo.tv/latest/663415-major-housing-fraud-exposed-in-islamabad-society
