# ANTIGRAVITY: YouTube Agent Studio v3.0 Motion-First Upgrade (Implementation Prompt)

Act as a senior AI motion graphics engineer and multi-platform agent skills maintainer. IMPLEMENT the requested upgrade: source code, tests, packaging, docs and an unmerged PR. This is not just a spec-writing task.

PRIMARY SOURCE (v2.0, PR #1 already merged):
https://github.com/islamically85-byte/youtube-agent-skill
https://github.com/islamically85-byte/youtube-agent-skill/pull/1

VERIFIED ENGINEERING REFERENCE (already working code):
https://github.com/Mueed406/pakistan-property-documentary-render
Working Windows HTML Canvas browser -> FFmpeg MP4 proof:
https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38994187546
Working Remotion + Pedalboard + OTIO Windows test:
https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38991035946
Real motion skill install test:
https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38994372728
Gemini Urdu TTS API success:
https://github.com/Mueed406/pakistan-property-documentary-render/actions/runs/38973775642

TARGET: create a fresh feature branch and follow-up PR against v2.0 main. Do not edit merged PR #1. If your GitHub identity lacks push access, use an authorized fork-and-PR or ask for access. Never fabricate commit/PR success.

MANDATORY:
1. AUDIT v2.0 first. Preserve all 17 Claude workflows and ChatGPT yt-studio orchestrator, tests, LICENSE, dual packages and script-based release build. Avoid duplicate systems and breaking integrations.
2. Implement browser motion support as a reusable skill: HTML/CSS/SVG/Canvas with time-based deterministic frame functions, 25/30fps 16:9 and 9:16, headless Chrome/Edge via Node/Puppeteer, frame capture -> FFmpeg H264 MP4. Use our already tested original browser_motion directory from reference repo. Add storyboard timing, source media provenance, contact sheets, output checks and rapid preview. NEVER claim static page screenshots are professional 3D animation.
3. Use physically detailed licensed Blender 3D models for actual environment shots and moving cameras. Put browser-motion overlays over relevant real moving video. Remotion/React is OPTIONAL second compositor; respect its free license (individual/teams <=3, otherwise confirm terms). Avoid web-dashboard aesthetics or lazy flat cards.
4. Skill sources: optional externally installed /motion from abhimahamkali/claude-motion-skill (its repo lacked a visible LICENSE in our audit: DO NOT COPY/RELICENSE); MIT sources JakeB-5/motion-graphic-skill and haidrrrry/claude-remotion-skill. Preserve original authors' attribution and required license copies for any adapted MIT code. Use Vercel skills CLI for install, not manual unauthorized redistribution.
5. Windows setup must cover Node LTS, Chrome/Edge, FFmpeg, Python3.11, Blender CLI and optional Remotion, Spotify Pedalboard, OpenTimelineIO. Provide opt-in safe installer, avoid extra paid apps and random download mirrors. Reference tested windows/Install-MotionSkills.ps1 and studio_cli.py.
6. Narration: preferred approved Gemini Flash TTS with native Pakistani Urdu and explicit steady voice direction, check actual speech pacing/pronunciation, no sobbing voice. Keep human/offline voice fallback. Use measured WAV cue timings. Never promise DSP makes robotic voice fully human. Subtitles must be RTL and not obstruct subject.
7. Build synchronized sequence: script claim -> narrator phrase -> relevant video shot -> 3D animation -> caption/source cue. Actual buildings when discussing buildings; physical files when discussing files; official map or explicitly conceptual parcel-grid (never pretend a fake diagram is real Islamabad map); real documentary B-roll background.
8. Sound: source-licensed score/SFX or original score, 48kHz voice mastering, safe compressor/EQ, LUFS and true-peak QC, voice/music ducking. Color: matched exposure/contrast, controlled saturation, soft sharpness, Rec.709 and no fake native 4K.

CRITICAL THREE-OPTION PRODUCT UX in ChatGPT yt-studio:
Show the following THREE compact production choices on first actual video-render request without a preselected mode. Do not ask on script-only or simple YouTube metadata requests.

A. FREE STUDIO — $0 additional paid API spending:
HTML Canvas browser motion + FFmpeg + eligible free licensed Blender/stock assets; local/open-source narration or user-recorded voice; optional Remotion only if its license allows. Clarify local compute/network costs are not zero. Never secretly consume credits.
B. HYBRID VALUE — Free quota OR explicit monetary cap:
Same open-source renderer; Gemini TTS if authorized free-tier quota actually works; budget provider only when user approves specific quoted amount. If unavailable use free fallback or pause when fallback fails creative/quality requirements. No auto billing.
C. vidIQ / PREMIUM — verified credits or approved payments:
If the vidIQ plugin is connected, READ real balance and current action credit rates. As of official docs examples: research 5 credits/call, voice 14/1000 characters, music 25/track, thumbnail 22 credits, script 1 credit/min, clips 9 credits/source minute; AI video varies and must be priced by tool BEFORE calling. No stale/fake balances, no auto-refill. If credits are zero, label this path unavailable and propose A/B. Never convert credits to fake dollar cost.

Implement tier selection in a capability/budget router with states AVAILABLE, NOT_CONNECTED, OUT_OF_CREDITS, NO_FREE_QUOTA, PAID_APPROVAL_REQUIRED, UNSUPPORTED, LICENSE_BLOCKED, FAILED and QUALITY_REJECTED. Show exact price/credits when genuinely quoted, otherwise "price unconfirmed." Never use premium tools without explicit approval. Do not force a large form; a natural compact 3-choice menu is sufficient. ChatGPT skills cannot install local executables or invoke disconnected tools; don't imply they can.

REQUIRED NEW CAPABILITIES:
- Skill(s): yt-motion, yt-browser-render, yt-3d, yt-voice, yt-audio, yt-cost-router, yt-render-qc, OR a minimal non-duplicative architecture achieving same outcomes. Mirror compatible instructions under Claude skills/ and chatgpt/skills/.
- yt-studio routes by intent; yt-produce directs authentic rendering rather than stopping at copy-ready prompts whenever actual execution tools are available.
- Provide authoring templates for scene.html, Blender scene.py, editable Remotion TSX, cue JSON/OTIO, soundtrack manifest and source attribution.
- Tests on Windows and Linux, exact frame counts, source imports, UTF8 Urdu/RTL, 3 tier choice behavior, vidIQ zero balance fallback, no-credit voice fallback, unlicensed skill exclusion, no-pay policy, 1080p+ H264 output and artifact verification.
- Build all three existing release ZIPs, run current 100% tests + new tests, update manifests/docs/changelog, maintain plugin deploy instructions; GitHub merge DOES NOT update a private ChatGPT plugin automatically.
- Produce real 12-15s 16:9 property-documentary motion proof and inspect stills/video with no static dashboard look before calling it accepted.
- Save final 6-7min full video as a separate review rendition only AFTER narration, visuals, licensing and budget approved. Do not upload to YouTube.

SECURITY / INTEGRITY:
Do not expose Gemini keys or other secrets in public code, CI logs, screenshots, skill ZIPs or issue comments. Do not claim paid providers are free, outputs are rendered before they exist, or actual site maps are creative reconstructions. Original context alleges files-versus-plots discrepancy; preserve allegation wording and reliable source citations.

DELIVERY:
Return summary of concrete changes; provider/credits matrix and actual quotations; exact tests; links to real MP4 and source files only if generated; complete reproducible Windows install commands; the new pull request URL; what cannot run without explicit account connection; how to separately deploy the ChatGPT plugin after reviewing source.

Begin with the audit, then implement and test. Do not ask for routine engineering decisions.
