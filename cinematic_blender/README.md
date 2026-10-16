# Cinematic documentary upgrade — Gemini + Blender + real stock footage

The old 3:07 Piper-only stock documentary remains preserved. A new hybrid pipeline is implemented but **not yet certified as a finished film**.

## Proven outcomes

- **Gemini API key works:** the one-voice test succeeded and uploaded a real WAV file:
  https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38973775642
- **Architectural 3D asset:** Poly Haven, *Modular Urban Apartments Facade* (James Ray Cock), CC0.
  Licensed source: https://polyhaven.com/a/modular_urban_apartments_facade
- **Blender version:** Ubuntu runner installed Blender 4.0.2 with FFmpeg and required fonts.
- **3D preview build:** https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38974035200
- **Script validation:** offline GitHub Actions tests passed for hybrid voice planning and compositor.

## Production scenes

- `01_cinematic_parcel_map.blend`: animated 3D parcel-grid disparity demonstration (not a site map).
- `02_architecture_construction.blend`: CC0 modular architecture and cranes/dolly reveal.
- `03_evidence_document_desk.blend`: paper dossiers with 3D camera motion.
- Each original `.blend` is editable and retained as a render artifact when the preview succeeds.
- `cinematic_blender/hybrid_composite.py` maps the imagery to spoken cues and overlays the 3D over moving stock footage.

## The review film pipeline

Run `.github/workflows/render-hybrid-cinematic-documentary.yml` through GitHub Actions ONLY AFTER the Blender visual sample is reviewed and you've confirmed the Gemini key belongs to a free-tier, unbilled project. Input:
- `confirm_free_tier = CONFIRM_FREE_TIER_ONLY`
- `blender_preview_run_id = <run ID of successful Blender preview>`

The workflow generates measured Gemini Urdu audio, short provisional Urdu SRTs, pulls HD stock video, mixes original music, composes the full film, re-renders the editable 3D scenes at 1920x1080, and exports a downloadable MP4 to Actions artifacts.

## Honesty checks

- Voice naturalness/accent still needs human review. The neural voice is synthetic.
- A passed file-export check is not proof of a professional artistic edit.
- 3D visualizations are illustrative, not geographic or investigative evidence.
- No YouTube publication occurs automatically.
- Background music is original procedural synthesis, not a copyrighted commercial track.
- No credits or paid tools are automatically selected.
- All stock footage is separately licensed and attributed in the manifest.

This is an implementation, not a claim that the final 7-minute film has already been rendered.
