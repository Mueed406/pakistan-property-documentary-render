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


## AMD / older NVIDIA GPU: Kokoro ONNX DirectML

For Windows GPUs that cannot run the installed CUDA PyTorch kernels (for example, some legacy NVIDIA Maxwell GPUs) or for AMD Radeon hardware, choose the independently licensed Kokoro ONNX implementation (MIT wrapper / Apache Kokoro model) with the DirectML provider.

    powershell -File .\local-production\setup-tts-windows.ps1 -FilmPath "." -Engine directml
    .\.venv-tts\Scripts\python.exe .\local-production\voice_gpu.py generate --backend kokoro-directml --require-gpu --output output\local-voice

This downloads the official Kokoro ONNX 1.0 model (325.5MB) and voices (28.2MB) from https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1 with their developer-published SHA256 digests verified BEFORE the model loads. The script explicitly requires an ONNX DmlExecutionProvider, creates an ONNX session with that provider, and fails if the provider is unavailable rather than silently pretending GPU use. Some ONNX operations may still use CPU fallback; this is normal in hybrid GPU+CPU inference.

For AMD RX 560/RX 570, DirectML support depends on the actual Windows version, GPU driver, and model operators, so run it on the PC to establish compatibility. For NVIDIA Quadro M4000, modern CUDA builds may lack Maxwell kernels; DirectML is the alternative to test. The user has previously operated different PCs, so GPU identity MUST be confirmed on the machine that runs the film.

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
