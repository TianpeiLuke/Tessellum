---
tags:
  - resource
  - documentation
  - hermes_agent
  - best_practices
  - cost_optimization
keywords:
  - hermes tips and best practices
  - prompt specificity tool autonomy
  - cli power user shortcuts
  - context files agents soul cursorrules
  - prompt cache compress delegate cost levers
  - messaging tips security allowlists
  - docker untrusted code command approval
topics:
  - Hermes Agent
  - Best Practices
  - Performance and Cost
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/tips
access_control_group: ["general"]
---

# Hermes Agent — Tips & Best Practices

## Overview

Tips & Best Practices is the **quick-wins playbook** for getting the most out of Hermes Agent — a scan-and-jump collection of practical advice grouped by the aspect it improves: how to phrase requests, CLI keystroke shortcuts, the context files Hermes auto-loads, how memory and skills divide labor, the levers that cut token cost, messaging-platform conveniences, and the security do's. It is not a feature deep-dive: each tip points at a feature whose mechanics live in its own page (cron, skills, SOUL.md, the messaging gateway, the Docker/sandbox terminal backends), so this note is the practitioner's index of "small habits that compound." The through-line is leverage — be specific, let the agent use its tools, keep the prompt prefix stable so the provider cache hits, and gate anything that touches a terminal behind an allowlist or container.

## Getting the Best Results

The prompting tips trade clarification rounds for up-front context:

- **Be specific.** Vague prompts produce vague results. "Fix the `TypeError` in `api/handlers.py:47` — `process_request()` receives `None` from `parse_body()`" beats "fix the code." More context = fewer iterations.
- **Provide context up front.** Front-load file paths, error messages, and expected behavior. One well-crafted message beats three rounds of back-and-forth. Paste error tracebacks directly — the agent can parse them.
- **Use context files for recurring instructions.** Repeated rules ("use tabs," "we use pytest," "the API is at `/api/v2`") belong in an `AGENTS.md` — the agent reads it automatically every session, zero effort after setup.
- **Let the agent use its tools.** Say "find and fix the failing test," not a step-by-step hand-hold. The agent has file search, terminal access, and code execution — let it explore and iterate.
- **Use skills for complex workflows.** Before writing a long how-to prompt, check `/skills` for an existing one and invoke it directly (e.g. `/axolotl`, `/github-pr-workflow`).

## CLI Power User Tips

- **Multi-line input.** `Alt+Enter`, `Ctrl+J`, or `Shift+Enter` insert a newline without sending. `Shift+Enter` only works when the terminal sends it as a distinct keystroke (Kitty / foot / WezTerm / Ghostty by default; iTerm2 / Alacritty / VS Code once the Kitty keyboard protocol is enabled); the other two work everywhere.
- **Paste detection.** The CLI auto-detects multi-line pastes — a pasted code block or traceback is buffered and sent as one message, not line-by-line.
- **Interrupt and redirect.** `Ctrl+C` once interrupts the agent mid-response so you can retype; double-press within 2 seconds force-exits. Invaluable when it heads down the wrong path.
- **Resume sessions.** `hermes -c` resumes exactly where you left off with full history; `hermes -r "my research project"` resumes by title.
- **Clipboard image paste.** `Ctrl+V` pastes a clipboard image straight into chat; the agent uses vision on screenshots, diagrams, error popups, or mockups — no save-to-file step.
- **Slash command autocomplete.** Type `/` and press `Tab` to list all commands — built-ins (`/compress`, `/model`, `/title`) plus every installed skill. `/verbose` cycles tool-output display through **off → new → all → verbose** ("all" to watch the agent work, "off" for clean Q&A).

## Context Files

Hermes auto-injects several context files so you don't repeat yourself. `AGENTS.md` is your project's brain — architecture decisions, conventions, and project-specific rules, injected into every session:

```markdown
# Project Context
- This is a FastAPI backend with SQLAlchemy ORM
- Always use async/await for database operations
- Tests go in tests/ and use pytest-asyncio
- Never commit .env files
```

`SOUL.md` (`~/.hermes/SOUL.md`, or `$HERMES_HOME/SOUL.md`) is the instance-wide **personality** source — Hermes seeds a starter automatically:

```markdown
# Soul
You are a senior backend engineer. Be terse and direct.
Skip explanations unless asked. Prefer one-liners over verbose solutions.
Always consider error handling and edge cases.
```

Use `SOUL.md` for durable personality, `AGENTS.md` for project instructions (full walkthrough: [Use SOUL.md with Hermes](hermes_use_soul_md_guide.md)). Existing `.cursorrules` / `.cursor/rules/*.mdc` files are read too — no need to duplicate conventions. **Discovery:** the top-level `AGENTS.md` loads at session start; subdirectory `AGENTS.md` files are discovered lazily during tool calls (via `subdirectory_hints.py`) and injected into tool results, not loaded upfront. Keep context files concise — every character counts against the token budget since they ship in every message.

## Memory & Skills

- **What goes where.** **Memory** is for facts — your environment, preferences, project locations, things learned about you. **Skills** are for procedures — multi-step workflows, tool-specific instructions, reusable recipes. Memory for "what," skills for "how."
- **When to create a skill.** A 5+-step task you'll repeat should become a skill: "save what you just did as a skill called `deploy-staging`," then `/deploy-staging` reloads the full procedure.
- **Manage capacity.** Memory is bounded (~2,200 chars for `MEMORY.md`, ~1,375 for `USER.md`); when full the agent consolidates — help with "clean up your memory" or "replace the old Python 3.9 note — we're on 3.12 now."
- **Let the agent remember.** "Remember this for next time" saves key takeaways; you can be specific ("save to memory that our CI uses GitHub Actions with the `deploy.yml` workflow").

Note that memory is a **frozen snapshot** — changes made mid-session don't appear in the system prompt until the next session starts (written to disk immediately, but the prompt cache isn't invalidated mid-session).

## Performance & Cost

The cost levers all hinge on token economics:

- **Don't break the prompt cache.** Providers cache the system-prompt prefix; keeping it stable (same context files, same memory, same model) earns cheaper **cache hits** on later messages. Avoid changing the model or system prompt mid-session.
- **`/compress` before hitting limits.** Long sessions accumulate tokens; when responses slow or truncate, `/compress` summarizes history, preserving key context while cutting token count. `/usage` shows where you stand.
- **Delegate for parallel work.** `delegate_task` runs subtasks as independent subagents, each with its own context, returning only final summaries — slashing the main conversation's token usage.
- **`execute_code` for batch operations.** A one-shot script ("rename all `.jpeg` to `.jpg` and run it") is cheaper and faster than per-file terminal commands.
- **Choose the right model.** `/model` switches mid-session — a frontier model (Claude Sonnet/Opus, GPT-4o) for reasoning/architecture, a faster model for formatting/renaming/boilerplate. Run `/usage` periodically and `/insights` for a 30-day usage view.

## Messaging Tips

- **Set a home channel.** `/sethome` in your preferred Telegram/Discord chat designates where cron results and scheduled-task outputs are delivered; without it the agent has nowhere to send proactive messages.
- **Use `/title` to organize sessions.** Name sessions (`/title auth-refactor`) so they're findable via `hermes sessions list` and resumable with `hermes -r "auth-refactor"`; unnamed sessions become indistinguishable.
- **DM pairing for team access.** Instead of hand-collecting user IDs, enable DM pairing — a teammate DMs the bot, gets a one-time code, you approve with `hermes pairing approve telegram XKGH5N7P`.
- **Tool progress display.** `/verbose` controls visible tool activity; on messaging keep it "new" (just new tool calls), in the CLI "all" gives a live view. Sessions auto-reset after idle (default 24h) or daily at 4 AM — adjust per-platform in `~/.hermes/config.yaml`.

## Security

For untrusted repositories or unfamiliar code, run a container terminal backend so destructive commands can't reach the host:

```bash
# In your .env:
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

The remaining security do's are guardrails-as-defaults:

- **Review before choosing "Always."** Dangerous-command approvals (`rm -rf`, `DROP TABLE`, …) offer **once / session / always / deny** — "always" permanently allowlists the pattern, so start with "session."
- **Command approval is your safety net.** Hermes checks every command against a curated dangerous-pattern list (recursive deletes, SQL drops, `curl | sh`, …); don't disable it in production. In a container backend (Docker, Singularity, Modal, Daytona) these checks are **skipped** because the container is the boundary — lock those images down.
- **Use allowlists for messaging bots.** Never set `GATEWAY_ALLOW_ALL_USERS=true` on a bot with terminal access; use per-platform allowlists or DM pairing:

```bash
# Recommended: explicit allowlists per platform
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=123456789012345678

# Or use cross-platform allowlist
GATEWAY_ALLOWED_USERS=123456789,987654321
```

On Windows, prefer explicit UTF-8 file encoding (`open(..., encoding="utf-8")`) to avoid `cp125x`-driven `UnicodeEncodeError` in tests/scripts.

## Related Notes

**Terms**
- [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — provider system-prompt prefix caching; relevance: the "don't break the prompt cache" cost tip depends on a stable prefix earning cache hits.
- [term_context_window](../../term_dictionary/term_context_window.md) — the model's token budget; relevance: `/compress` and concise context files exist to stay inside it.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated child agent with isolated context; relevance: `delegate_task` fans parallel work out to subagents to cut main-conversation tokens.
- [term_progressive_summarization](../../term_dictionary/term_progressive_summarization.md) — incremental history summarization; relevance: `/compress` is the progressive-summarization lever this page recommends.
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — the agent's persistent fact store; relevance: the memory-vs-skills routing + capacity tips.
- [term_skills](../../term_dictionary/term_skills.md) — on-demand procedural knowledge; relevance: the when-to-create-a-skill + "skills for complex workflows" tips.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — container/isolated terminal backend; relevance: the "Docker for untrusted code" security tip selects this backend.
- [term_access_control](../../term_dictionary/term_access_control.md) — who-can-do-what gating; relevance: the messaging-bot allowlist + review-before-"always" security do's. (+fin: term_messaging_gateway [own SP11], term_dm_pairing [own SP11])

**Code-Repos**
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — prompt cache + `/compress` compression + context-file loaders; relevance: the "don't break the prompt cache" and `/compress`-before-limits cost tips are implemented here.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `delegate_task` + `execute_code` + Docker sandbox; relevance: the parallel-delegate and batch-execute cost levers + untrusted-code Docker tip.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI power-user surface (`-c`/`-r`, paste, `/verbose`, autocomplete); relevance: the CLI shortcut tips type into this surface.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — `/sethome`/`/title`/DM-pairing + allowlists; relevance: the messaging tips + bot allowlist security live here.
- [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills + memory routing; relevance: the memory-vs-skills "what goes where" tips.

**Snippets**
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt-cache boundary code; relevance: the stable-prefix cache-hit mechanism the cost tip exploits.
- [snippet_hermes_agent_core_conversation_compression_entry](../../code_snippets/snippet_hermes_agent_core_conversation_compression_entry.md) — `/compress` entry point; relevance: how the compress tip is invoked.
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression summarization strategy; relevance: what `/compress` preserves vs drops.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — subagent spawn for `delegate_task`; relevance: the parallel-delegate cost lever.
- [snippet_hermes_agent_tools_delegate_prompt](../../code_snippets/snippet_hermes_agent_tools_delegate_prompt.md) — delegated subtask prompt assembly; relevance: how delegated work is framed in isolation.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — `execute_code` sandbox; relevance: the batch-script cost lever.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker terminal backend; relevance: the `TERMINAL_BACKEND=docker` untrusted-code security tip.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skills install path; relevance: the create/use-a-skill workflow tips.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — context-file loaders (`AGENTS.md`/`SOUL.md`/`.cursorrules`); relevance: the auto-injected context-file discovery tips.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential/secret sources; relevance: the `.env`/allowlist env-driven security tips.

**Docs**
- [hermes_use_soul_md_guide](hermes_use_soul_md_guide.md) — SOUL.md identity; relevance: the SOUL/AGENTS context-file tips.
- [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: the when-to-create-a-skill + memory-vs-skills routing tips.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the scoped MCP allowlist security tips.
- [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — scheduled blueprints; relevance: cost tips that apply to unattended cron runs.
- [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the cost levers (`delegate_task`/`execute_code`) used programmatically.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — CC cost-reduction; relevance: closest analogue to the cost tips.
- [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — CC prompt cache; relevance: analogue to "don't break the cache".
- [cc_effective_prompting](../claude_code/cc_effective_prompting.md) — CC prompting best practices; relevance: analogue to "be specific / provide context".
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — CC security model; relevance: analogue to the security do's.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — CC sandbox; relevance: analogue to "Docker for untrusted code".
- [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — CC security guidance layers/rules; relevance: analogue to the allowlist/review-before-"always" security do's.
- [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — CC per-feature context cost; relevance: analogue to the `/compress`-before-limits + prompt-cache cost levers.

**Source**: `inbox/hermes_agent_docs/guides/tips.md` · https://hermes-agent.nousresearch.com/docs/guides/tips
**Last Updated**: 2026-06-19
**Status**: Active
