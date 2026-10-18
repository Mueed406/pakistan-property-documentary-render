# The Last Toy Shift — Local NVIDIA GPU / CPU Voice and Sketchfab Setup

These scripts are meant to run on the USER'S OWN WINDOWS COMPUTER. Having them on GitHub does not grant ChatGPT or GitHub Actions access to that computer or its GPU. The runtime probe, not a claim in chat, establishes whether CUDA acceleration is available.

## Setup

Requirements: Windows, Python 3.11, Git for Windows, FFmpeg in PATH. Run PowerShell from the films/the-last-toy-shift project directory:

    powershell -File .\local-production\setup-tts-windows.ps1 -FilmPath "." -InstallNoizSkill
    .\.venv-tts\Scripts\python.exe .\local-production\voice_gpu.py probe
    .\.venv-tts\Scripts\python.exe .\local-production\voice_gpu.py generate --backend kokoro --output output\local-voice

If the device probe says CPU despite an NVIDIA GPU, install a CUDA-enabled PyTorch wheel selected for your driver at https://pytorch.org/get-started/locally/ into the same virtual environment, and run probe again. Avoid claiming the GPU is in use until torch.cuda.is_available() is actually true.

Kokoro Apache-2.0 voices are the baseline: am_michael for hero, am_adam for the warning tape, af_heart for the doll. The voice engine generates six lines placed at actual moments on the 90-second film timeline, producing distinct 48kHz WAV voice stems and a draft mix. CPU FFmpeg handles sample-rate conversion and ducking; PyTorch device handles inference. Short lines retain the intended silence rather than being stretched unnaturally. Source clips, exact cue durations and hardware are recorded in the local voice_render_qa.json manifest.

## Expressive Chatterbox option

Chatterbox MIT: https://github.com/resemble-ai/chatterbox . The latest family contains Chatterbox Turbo 350M, Nano 110M, and original expressive model. Turbo allows documented paralinguistic tags; original exposes exaggeration and cfg_weight controls. Install:

    powershell -File .\local-production\setup-tts-windows.ps1 -FilmPath "." -Engine chatterbox

To maintain three distinct voices, the script requires permissioned hero.wav, tape.wav and doll.wav and a local voice-references/consent.json confirming both speaker_consent and authorized_for_this_film for each role. All source WAV files stay PRIVATE on the user's machine. No scraped game audio, actor impersonation or celebrity cloning.

    .\.venv-tts\Scripts\python.exe .\local-production\voice_gpu.py generate --backend chatterbox-turbo --references voice-references --require-gpu --output output\local-voice

Auto backend selects Turbo when all three consented references are present and CUDA has at least 6GiB VRAM, otherwise Kokoro. This is a conservative routing heuristic, not a guarantee of GPU RAM fit. You may need different Python environments for Kokoro and Chatterbox if upstream dependencies conflict. First model use downloads official model weights; cached models can run locally without cloud TTS.

## Optional NoizAI skills

Source: https://github.com/NoizAI/skills , pinned commit 779f30af588ebf4dd17fc0acaa590ae147a0d3f5. The project provides a local pinned-source installer for the upstream TTS skill:

    powershell -File .\local-production\install-noiz-skill.ps1 -ProjectPath "."

It adds the skill to Codex/Claude/Antigravity/Gemini project directories without repackaging its source into the public repository. Specify --backend kokoro if executing Noiz scripts, because without a Noiz API key the backend may use cloud guest service. Noiz emotion/cloning and exact server-side duration features require a separate online Noiz API key, and are not automatically GPU-local.

## Sketchfab 1.8.0 account login for 3D model imports

The official Sketchfab add-on was previously SHA256 verified and actually installed inside an isolated GitHub Blender runner, NOT on your Windows desktop. Release page:
https://github.com/sketchfab/blender-plugin/releases/tag/1.8.0

To get and import models: install in Windows Blender, open 3D viewport, press N > Sketchfab, and log in there with the API token from your own Sketchfab account settings. This login is mandatory for imports in the official addon. DO NOT share the token or password in chat. The plugin then searches and imports permitted downloadable models; it creates an sf_attributions Blender Text block listing original creators and license details. Keep it when saving/exporting the scene.

For The Last Toy Shift, search for independently created industrial equipment, conveyor machinery, old CRT, factory props, lights, toy shelving and security doors. Check EACH model URL, author, license, textures and allowed uses; downloadable does NOT mean unrestricted. Prefer CC0 or CC-BY with proper credits for wide reuse, and do not silently reuse noncommercial or game-extracted meshes in monetized content. Keep a local license ledger; no authenticated downloads or token scraping are built into these scripts.

The existing Sketchfab download/installer and pinned 71-skill project installer are documented at toolchains/creative-animation-skills/README.md.

## Unsupported or limited options

Microsoft VibeVoice's upstream repository reports removal of the original long-form TTS code and research/development limitations. Coqui XTTS v2 has model-weight restrictions separate from its engine; Piper models have distinct per-voice licenses. Neither substitutes for the local Kokoro/Chatterbox work without review.

**Status:** GitHub can test script syntax, licensing notes and timing contracts, not the user's NVIDIA GPU. Voice audition outputs are not artistically approved actor performances. No final 5400-frame/1080x1920 film has been produced.
