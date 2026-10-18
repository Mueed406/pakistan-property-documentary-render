# Animation production tools: 55 Motion + 16 Blender + Sketchfab 1.8.0

Status (2026-10-18): **Verified in GitHub Actions**, NOT automatically installed in your Windows machine. Your Poppy Playtime fan-film production branch and other repo files are preserved.

## Tested and packaged

- 55 reusable skill folders from the **18** iart.ai motion-skill pack repos, fetched from individually pinned commits. Includes Three.js/WebGL, shaders, cinematic shots, Remotion, sound, editing, 60fps and QC.
- 16 Blender skills from kevinbadi/blender-skills, fetched DIRECTLY from its pinned original repository into a local agent workspace. The source does not have a repo-level LICENSE at the tested revision: no original Blender skill files are repackaged as public downloads.
- One official **Sketchfab For Blender 1.8.0** addon downloaded separately. Published original SHA-256:
  a6be9e8348a67b66faa236c7aba4c4980db0bda76ab5db17eddd077f66ca71d7
- All 71 agent skill folders were copied into an isolated GitHub CI workspace and audited. This is not evidence they have been installed in your personal Codex, Claude, Antigravity or Gemini instances.

## Install the 71 skills on your Windows project

**Requirements:** Git for Windows and Python 3. No third-party scripts are automatically executed.

Clone or update this repository, switch to branch feature/last-toy-shift-cinematic-production-20261017, then use a PowerShell terminal in the repository root:

    py -3 toolchains/creative-animation-skills/install.py install --project "." --hosts codex,claude,antigravity,gemini

This fetches all 19 repositories by fixed Git commit, checks out the SHA, and copies every skill's SKILL.md plus references/scripts/templates into the conventional per-agent project folders:

- Codex: .agents/skills/
- Claude Code: .claude/skills/
- Antigravity: .agent/skills/
- Gemini CLI: .gemini/skills/

Each destination gets 71 unique skill names. The only upstream name collision is lower-thirds; TikTok's is renamed to tiktok-lower-thirds. Existing folders are NOT overwritten; fail-closed. Read creative-skill-install-audit.json for source provenance and completion.

Or run the included all-in-one PowerShell helper, which stages and verifies the Sketchfab ZIP too:

    powershell -File toolchains/creative-animation-skills/install-windows.ps1 -ProjectPath "C:\path\to\your\project"

Choose your actual project path. For portability you can use the current repo root with -ProjectPath ".".

## Sketchfab 1.8.0: official Blender addon

Verified upstream: https://github.com/sketchfab/blender-plugin/releases/tag/1.8.0

Download or use the hash-verified ZIP produced by install-windows.ps1:

    https://github.com/sketchfab/blender-plugin/releases/download/1.8.0/sketchfab-plugin-1-8-0.zip

**Install in Blender:** Edit > Preferences > Add-ons > Install from Disk... > select the ZIP > enable Sketchfab Plugin. Log in from the addon UI using your own Sketchfab account. Never share API tokens/credentials in chat. Meshy is NOT Sketchfab and not required for this addon.

To automatically run the Blender addon installer in a background Blender process, use the explicitly opted-in PowerShell switch after identifying your own Blender executable:

    powershell -File toolchains/creative-animation-skills/install-windows.ps1 -ProjectPath "." -BlenderExecutable "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" -InstallSketchfabAddon

This helper attempts the installation and shows errors instead of silently claiming success. It does not configure a Sketchfab login.

## What is separate / not installed by these skills

The kevinbadi Blender camera/model workflows refer to **Blender MCP** and a Blender addon/WebSocket connection. Installing SKILL.md files alone does not connect to Blender. Follow the verified tool's own setup: Blender installed and running, trusted blender-mcp addon installed, the MCP server configured in your chosen agent, and the Blender addon connected. Before executing addons or downloads, review source and licenses. No external API keys are included. Meshy image-to-3D features require your own key and may incur charges. After Effects/Remotion/Manim/GSAP are not auto-installed; install only the tool needed for each selected workflow.

## For ChatGPT

A separate private ChatGPT skills-only plugin was created with the **55 iart.ai** motion skills (MIT umbrella license and upstream source attribution) plus a project-authored Blender/Sketchfab setup guide.

https://chatgpt.com/plugins/plugins_6ad4446c19408191ad156edddba8db4d

A saved plugin is not the same as a locally connected Blender desktop MCP tool. Enable/select the plugin when working on motion tasks.

## GitHub CI / source inventory

The reproducible GitHub Actions installer:
.github/workflows/creative-skills-and-sketchfab-install.yml

CI checks exactly 55 motion + 16 Blender folders, validates pinned commits, verifies the published Sketchfab ZIP SHA-256 and safe archive paths, then actually installs and enables the official Sketchfab add-on inside a disposable Blender runner (module sketchfab-plugin-1-8-0). The add-on is NOT installed on your local Windows machine until you run the installer or use Blender's GUI. It exports ZIPs as short-retention GitHub Actions artifacts (not a permanent public release).

All motion-skill recipes remain credited to **iart.ai**. Blender skill files remain in and are downloaded directly from **kevinbadi/blender-skills**. Official Sketchfab addon is Apache-2.0. Do not upload third-party files from a repository without confirming redistribution rights.

No automatic skill installs, MCP servers, 3D API calls, or addon execution happen merely by checking out this repo. No Google Play or public video publishing is performed.
