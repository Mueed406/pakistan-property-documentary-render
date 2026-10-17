# Production modes and accurate cost quotation policy

When a ChatGPT user requests a rendered video, show **exactly THREE options** only if they have not selected a production mode and mode choice affects workflow/cost. Avoid an intrusive form. The system must still answer their current request.

### Option 1 — Local / Open-Source (default, $0 paid API spending)
- Headless Chrome/Edge + original HTML Canvas renderer or MIT-licensed motion skills.
- FFmpeg, Blender, Python, local licensed/CC0 assets, original or user-supplied narration. A Piper voice may sound robotic; never claim natural narrator quality without evaluation.
- Remotion only if user meets its free-license terms (individual/small team); otherwise use plain HTML/CSS/Canvas+FFmpeg.
- Real local hardware/runtime/storage/internet costs may apply; $0 means no extra paid-API charge, not zero compute cost.
- No vidIQ credit spend.

### Option 2 — Free-tier / Budget Hybrid (estimated charge only after live quote)
- Browser motion/Blender baseline + approved free-tier Gemini TTS (when access and quota actually work), or budget-approved licensed premium voices/assets.
- Assess provider state/region/billing/credits. Quote per scene/minute or token amounts only from provider's current available price sheet. Default maximum extra monetary spend $0 without explicit creator authorization.
- Fallback automatically to Option 1 if service cannot be used, unless user explicitly requires natural TTS and quality would suffer; then pause for voice choice.
- Never silently create an Azure subscription or enable Google billing.

### Option 3 — vidIQ-assisted / Premium (credit budget required)
- vidIQ may provide voiceover, music, research, videos and optimization through a connected plugin with user credits. It is NOT required to produce the MP4: the open-source renderer stays the assembly engine.
- Before using vidIQ, call its balance tool and check exact costs. The Free plan advertises 150 credits/month; account balances differ.
- Official current action examples: research 5 credits/call, voiceover 14 credits per 1,000 characters, music 25 credits/track, script 1 credit/min, thumbnail 22 credits; generated videos vary per model, duration, resolution, and MUST be quoted from the tool before execution.
- Never invent a price or use credits without confirming the available balance and user's budget. No auto refills, retries or subscription upgrades.
- On insufficient credits, present a comparable hybrid or free version with disclosed quality trade-offs.

## UI contract for ChatGPT
When three-option presentation is useful, show three compact choices with:
- name, "included engines", cost status (confirmed/estimated/unknown), credit quote if available, privacy/licensing notes and quality trade-offs.
- Recommend the appropriate tier but never assume user has credits/paid providers.
- Connectors work only when installed and authorized in ChatGPT; a SKILL.md or plugin manifest does **not** install Windows executables or grant secret API access.
- If real external execution tool available and user authorizes execution, perform the production. Otherwise deliver a CLI pipeline/render project and explain what must be executed externally.
- Slash commands are optional on ChatGPT; route by natural-language intent; Claude Code can offer /motion.
- Deliver actual MP4 only after verified file creation, duration/audio/resolution/visual inspection checks.
- Never market vidIQ as fully free unlimited or conflate vidIQ plan price with incremental per-video charge.

Sources checked October 2026:
- https://support.vidiq.com/en/articles/15082430-vidiq-mcp
- https://support.vidiq.com/en/articles/13928456-features-credits-by-plan
- https://www.remotion.dev/docs/license/pricing
- https://github.com/abhimahamkali/claude-motion-skill
- https://github.com/JakeB-5/motion-graphic-skill
- https://github.com/haidrrrry/claude-remotion-skill
