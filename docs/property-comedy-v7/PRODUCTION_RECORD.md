# Property Comedy V7 — HTML Canvas production record
**Status:** local MP4 rendered and FFprobe-verified; artistic and narration review required. **Not uploaded to YouTube or GitHub Releases.** Previous V1–V5 movie versions remain preserved.

## User request, execution and distinction
The user rejected V6's full-frame poster movement, poor face expression overlays and low-energy commentary. V7 replaces flattened poster animation with source PNG layers independently composited in HTML5 Canvas. It adds actual stock-video excerpts already in the PPG documentary, a new user-supplied ElevenLabs voice track, Urdu captions, kinetic type, original paper/ink animations, parallax, and an extra five-second subscribe outro for **Pakistan Property Group**.

## Verified final output
- `PPG_Property_Comedy_Layered_V7_1080p60.mp4`, 34,236,307 bytes.
- 63.699 seconds. 1080×1920, 9:16. H.264, 60/1 fps, 3,821 frames. AAC stereo, 48kHz.
- Initial 720×1280, true 60-timestamp-per-second HTML Canvas scene animation, exported via high-quality Lanczos upscaling to 1080×1920.
- **Captured stock was originally 25fps and sampled to 12fps for animated photo-card windows**; never market as captured 60fps video.
- Accompanying 720p review cut is ~16MB.

## Tools: what did which work
- **HTML Canvas + JS:** actual entire independent layer animation, camera motion, stock-photo-card movement, captions, animated arrows, paper-mask transitions, branding. No duplicated face overlays; one character sprite is active per side.
- **CSS:** Inter Display headline and Noto Sans Arabic subtitles with local fonts, no redistributed font binaries.
- **Python / Playwright / Chromium:** code-controlled frame-accurate viewport and image exports; downloaded assets embedded as in-memory data URIs because local file:// browsing is restricted.
- **Python/Pydub/NumPy:** pause-bounded cut of the user-provided ElevenLabs audio, 12 role-timed dialogue cues, original synthetic effects, mastered original soundtrack.
- **FFmpeg / FFprobe:** decoding inherited stock once; media encoding, final mix/mux, upscale and QA. It does not author the visual animation.
- **PHP and Amazon S3:** NOT used. No credentials, hosting account or server need was provided; including them would create unnecessary complexity.

## Assets
- 23 V6 user-approved generated PNG source layers, including dealer pitch/tea/point/shock/celebrate, buyer thinking/skeptical/documents/smirk/surprise, tea/saucer/splash, torn-paper variants, paper-fiber texture and office background.
- 252 scene frames from the previously generated PPG baseline documentary source, in three distinct ~7s illustrative stock clips.
- All used media rights from earlier projects still need a final publication license audit.
- Character PNG source sizes are smaller than the 1080p output; V7 improves the *animation pipeline* but does not falsely claim every source sticker was redrawn at 2K.

## Audio-specific caveat
The uploaded ElevenLabs Zafar MP3 was **95.399 seconds** and included spoken role labels and section numbers. The project uses approximate pause-bounded cropping to select 12 content windows, yielding ~58.699s of spoken beats plus 5 seconds of music-led subscribe outro. This is not speech-to-text-confirmed alignment. **Manual listening must confirm that no unwanted direction, clipped word or wrong text remains before public publishing.** The user was not charged for another ElevenLabs generation.

## How to reproduce
The complete portable source package was delivered in the ChatGPT conversation as `PPG_Property_Comedy_Layered_V7_Editable_Project.zip`. Main scripts:
`build_audio.py`, `mix_audio.py`, `premium_canvas.html`, `render_html.py`, `export_final.sh`, `qa_video.py`, `Urdu_Captions_V7.srt`, `docs/assets_manifest.json`.

Run:
```bash
python build_audio.py
python mix_audio.py
python render_html.py --scale .6666667 --fps 60 --output short_canvas_720p60_silent.mp4
bash export_final.sh
python qa_video.py
```

## Story beat guide
1. Property hype + real construction/stock card
2. Dealer's rate-double joke
3. Buyer asking where the plot is
4. Brochure versus reality with real footage context
5. Animated NOC, ownership, possession questions
6. Dealer's genuine tea gag with one cup only
7. Buyer's skeptical “plot kab asli hoga?” punchline
8. Research/location check with film cutaway
9. Three staggered paperwork/checklist annotations
10. Pakistan Property Group branding
11. Subscribe call with buyer
12. Dealer's chai callback
13. Extra five-second animated subscribe ending

## QA and known limitations
Technical QA passed: correct duration, dimension, codec, audio stream and expected frame count. Sampled-frame motion and a contact sheet exist. Distinguish this from creative approval. Existing stickers contain prerendered poses (not a skeletal 3D/2D rig), so this is **layered pose animation, NOT phoneme-perfect face lip sync**. Physical paper textures are stock-style generated assets, not a copied commercial template. No new template vendor commercial media was ingested into V7 without source/rights clearance.

## Deferred reusable skill work
**Do NOT update ChatGPT/Claude/Antigravity/Gemini skills based on this alone.** User explicitly asked for a future separate approval after video review. Store the methods and limitations here; when asked, prepare an Antigravity prompt to update the user's separate YouTube skills repo, ChatGPT-first, and use Gemini-specific additions only if real value is demonstrated.
