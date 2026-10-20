# PPG editorial collage motion study (2026-10-17)

New original, editable documentary animation engine inspired by archival cutout editorial techniques. **Not a clone** of Vox branding or anyone else's templates.

## Included

- Four narrated editorial scenes within the existing 410-second Pakistan Property Group documentary: ≈42,000 files, ≈6,000 plot capacity, ≈36,000 difference, and *allegations are not a verdict*.
- `editorial_motion.html` — time-based HTML Canvas layer animation (26 s; 1280×720).
- `assets/` — reprocessed **generic stock footage from existing PPG render** and original procedural textures. The original stock footage rights must still be checked against the upstream source receipts before distribution.
- `render_preview.py` — local Chromium/Playwright matte renderer.
- `fetch_cc0_assets.py` — fetches reviewed CC0 illustrative photos from Wikimedia Commons, validates signatures, records SHA-256 and source URLs. These downloads are **not included until successfully fetched**.
- `PPG_Editorial_Collage_26s_720p_Review.mp4` — composed playable MP4 with the existing Piper Urdu voice/subtitles. Do **not** describe narration as Gemini or final voice.

## Reproduction

1. Use Python 3.11+ with `Pillow numpy playwright`, local Chromium, and FFmpeg. No paid API calls.
2. Ensure original approved PPG full film exists; update `FILM` in `prepare_assets.py` for your local path.
3. Run `python prepare_assets.py` to regenerate local derived images and textures.
4. Run `python render_preview.py --seconds 26 --fps 25 --out editorial_matte_26s.mp4`.
5. Composite matte over `00:33.672–00:59.672` of the original film with FFmpeg color key. Map the original film audio. Preserve crisp original Urdu subtitles.
6. Run `python fetch_cc0_assets.py` on an internet-connected environment to download external CC0 assets; verify license credits before insertion.

For Linux/macOS/Windows use the relevant installed Chromium path. The isolated ChatGPT render used data-URI inlining because its Chromium blocked both local files and localhost URLs; a typical local browser uses the original relative asset paths normally.

### Publication restrictions

- Source: https://www.geo.tv/latest/663415-major-housing-fraud-exposed-in-islamabad-society (published 2026-05-08); treat statistics as reported allegations.
- This is a **visual sample only**; the Piper voice remains the old original. Full-film transitions, stock licenses, consistent Urdu typography, true Gemini voice timing and legal/artistic QA are pending.
- All real-world stock images in this sample are illustration only, not photos of alleged culprits or locations.
- Do not include the reference thumbnails, brand logos or third-party tutorial images in distributed assets.