# Paper Collage Transitions — Original v1.0

A real 60fps editing pass that replaces hard joins with genuine two-plate
transitions. Built for the 410.4s, 1920x1080/60fps PPG documentary, but accepts
any 60fps 16:9 H264 MP4 when events are supplied. Produces a new H264/AAC MP4,
not a static illustration or a rendered project screenshot.

## Presets

1. `paper-tear`: rough-edged paper seam with texture and dark paper-shadow.
2. `ink-print`: spreading dark newsroom ink from paper center.
3. `newspaper-slide`: two moving printed-page edges with paper underside.
4. `film-splice`: monochrome archival film registration splice.
5. `photo-match`: parallax match-cut of old and new frames, soft paper seam.

The presets are **original authored code**, not redistributed proprietary
motion templates. External free-template vendors and import caveats are in
`TEMPLATE_CATALOG.md`.

## Try the included tests

    pip install numpy Pillow opencv-python-headless
    python -m unittest discover -s editorial_collage/transitions -p 'test_*.py' -v

## Existing PPG master — full V2 pass

    python editorial_collage/transitions/premium_transitions.py \
      plan-from-report --report MASTER_TECHNICAL_REPORT.json \
      --out transition_plan.json --max-events 20
    python editorial_collage/transitions/premium_transitions.py apply \
      --input PPG_Editorial_Documentary_FULL_410s_1080p60.mp4 \
      --plan transition_plan.json --output PPG_Editorial_Documentary_PREMIUM_TRANSITIONS_v2.mp4

Full source MP4 must be an actual 1080p60 stream. Audio stays continuous,
with original Urdu voice and music unchanged. Video is re-encoded CRF18 for
actual pixel-level transition re-compositing; encoder does not duplicate
or stretch the 410.4s timeline. Existing original full master remains intact.

## Status and verification

A local 15-second 960x540 60fps sample with TWO actual transitions was
rendered and FFprobe-checked: duration 15.0s, 900 frames, AAC soundtrack.
This is a **proof**, not proof that full V2 release passed. A separate CI
workflow recovers verified full 410s GitHub Release, builds a cue-based
transition plan, encodes, validates, and publishes only on success.

The full video quality upgrade remains subject to human audio/artistic QA,
particularly Urdu subtitle occlusion during transitions; avoid crossing a
claim-critical numeral reveal. Fonts, copyright, case evidence and source
truthfulness rules from the previous documentary skill remain mandatory.