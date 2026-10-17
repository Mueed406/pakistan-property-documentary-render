# Public YouTube Agent Studio skill sync — v4

The public skills repository at https://github.com/islamically85-byte/youtube-agent-skill is read-only through the currently connected GitHub installation. This change is **not deployed there yet**. The private ChatGPT YouTube Agent Toolkit was updated and separately verified at v0.4.0.

The local sync script in the production repository creates a safe portable patch for both editions of the public repository without deleting existing v3 skills.

## Authorized Antigravity instructions

1. Authenticate GitHub locally with the account that owns or can push to islamically85-byte/youtube-agent-skill. Do not paste passwords or tokens into a prompt.
2. Clone/check out the production repository feature/automated-documentary-studio-v4 branch. Clone the public skills repository main branch separately.
3. Ensure the public repository working tree is clean, and create a new branch, e.g. feature/editorial-documentary-v4. Never edit main directly.
4. Dry run sync from the production repository:

   python production/sync_public_skills_v4.py --target ../youtube-agent-skill

5. After inspecting the preview, apply once:

   python production/sync_public_skills_v4.py --target ../youtube-agent-skill --apply

6. Inspect git diff. It creates skills/yt-editorial-documentary/SKILL.md and chatgpt/skills/yt-editorial-documentary/SKILL.md, and adds a MARKED v4 editorial addendum to both master yt-studio skills, both motion skills, both upload-prep skills and root README. It preserves all existing skills.
7. Run tests and build both Claude/ChatGPT distributions:

   cd ../youtube-agent-skill
   python -m unittest discover -s tests -v
   python scripts/build-releases.py

8. Confirm the produced ZIPs contain new yt-editorial-documentary in both skills directories. Review license and attribution; preserve upstream Jake Schincariol MIT license and original authors, credit new extension to ABDUL MUEED LASHARY.
9. Commit on your feature branch and open a tested GitHub PR against the public repository. Do not claim an update has landed until the PR is merged.

## Repeatability
The sync script is idempotent: after a successful apply, rerunning it updates one marked section instead of adding duplicate instruction blocks. It refuses to mutate a dirty working tree. It never pushes commits or creates PRs without appropriate GitHub authorization.

## Future proofing
The full professional blueprint is docs/ANTIGRAVITY_DOCUMENTARY_V4_MASTER_PROMPT.md; generic video generation is a separate engineering phase. The current proven PPG full-length render remains case-specific and cannot be copied unmodified into new subject films. Preserve the exact source files, artistically approved 60fps scene library, source licenses, temporary masters, QA reports and private YouTube upload controls. Keep the YouTube private import guarded by a separate OAuth account connection.

## Current delivery
- Production feature PR: https://github.com/Mueed406/pakistan-property-documentary-render/pull/2
- Personal ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad233623ce08191a483a271fd2ed0c6 (v0.4.0)
- Working 410s documentary: https://github.com/Mueed406/pakistan-property-documentary-render/releases/tag/ppg-410s-editorial-1080p60-review-20261017
