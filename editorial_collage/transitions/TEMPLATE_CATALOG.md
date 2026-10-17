# Licensed free transition resources — editorial documentary studio

Research reviewed 17 Oct 2026. This is a **source catalog**, not a claim that
third-party archives were downloaded or that their binaries are committed.
The executable 5-presets pack included with this project is ORIGINAL source.

| Site | Verified relevant items | Engine needed | Policy |
|---|---|---|---|
| Mixkit DaVinci Resolve | Motion Blur Swipe Transition; Horizontal Split Frame; Vertical Split Frame | Resolve Fusion `.comp` | Free per item under Mixkit Video Templates license; inspect before importing |
| Mixkit After Effects | Rough Shape Transition (single template); masks/split title reveal | Adobe After Effects | Free per applicable item; application is commercial software |
| Mixkit Premiere Pro | Ink Splash Transition; Film Burn Transition; Retro Interference Transition | Adobe Premiere Pro / `.mogrt` | Free Mixkit template license; distinct from Mixkit Stock Video license |
| ProductionCrate | Motion Graphic transition mattes; 4K matte packs on Free filter | Depends on downloaded format | Free tier exists; verify specific item license and free designation |
| Motion Array (Free filter) | Free motion titles and graphic effects; free-labelled templates only | AE/Premiere/Resolve depending | Free account + usage terms; never assume all search results are free. No redistribution of underlying templates. |

Primary official URLs:
- https://mixkit.co/free-davinci-resolve-templates/transitions/
- https://mixkit.co/free-after-effects-templates/rough/
- https://mixkit.co/free-premiere-pro-templates/transitions/?page=3
- https://mixkit.co/free-premiere-pro-templates/film/
- https://mixkit.co/license/
- https://motionarray.com/browse/search/free/
- https://help.motionarray.com/hc/en-us/articles/8995511586717-Can-I-Use-Free-Assets-Commercially
- https://vfx.productioncrate.com/vfx/motion-graphics/transitions

## Import protocol

1. Open the **individual template page**. Confirm exact license, app version,
   no-watermark status, and whether 'Free' is actually attached to that asset.
2. Download using site's intended interface in the owner's authorized account.
   Do not scrape logged-in downloads, bypass account restrictions or mirror
   copyright-protected source ZIPs in a GitHub repository.
3. Record title, source URL, author, license snapshot, version, download date,
   SHA-256 digest, dependency list in each project's rights.json.
4. If editor template is proprietary `.aep` / `.prproj` / `.comp`, render its
   licensed output in that actual editor before importing into the FFmpeg
   documentary pipeline. **Do not pretend these files load into Python/OpenCV.**
5. For the automated FFmpeg-only studio, use the 5 executable *original*
   templates in `premium_transitions.py`: paper-tear, ink-print, newspaper-slide,
   film-splice and photo-match. No external template archive is required.

## Style principles

Motion scenes must bridge actual prior and next footage with a physical
narrative visual link, preserve soundtrack and source runtime, not inject 2-5s
silence or random glitch transitions. A coherent brand uses two or three
transition motifs repeatedly and a rare accent effect. Avoid an effect at
all 100 stock-to-collage joins. Maintain clear Urdu subtitle readability.

**Licensing guard:** The free *template* license can differ from free *stock
video* and free *music* licenses. Never assume official availability alone
means commercial rights or download success. Do not redistribute acquired
Motion Array project files to clients or public repositories.