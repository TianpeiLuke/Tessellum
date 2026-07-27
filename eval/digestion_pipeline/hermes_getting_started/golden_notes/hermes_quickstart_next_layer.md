---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - procedure
keywords:
  - try key features
  - add the next layer
  - slash commands
  - sandboxed terminal
  - skills and mcp servers
  - common failure modes
  - recovery toolkit
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
access_control_group: ["general"]
---

# Hermes Agent — Quickstart Part 2: The Next Layer

## Overview

This is the second half of the Hermes Agent Quickstart: it picks up *after* a clean base chat is working (see [Quickstart Part 1](hermes_quickstart_first_chat.md)) and walks through the in-chat features you get immediately, the optional layers you add on top, and how to recover when something breaks. The governing rule from the source is explicit — only layer on gateway, automation, sandboxing, voice, skills, MCP, or editor integration *after* a normal chat works. The page closes with a Common Failure Modes table and a Recovery Toolkit ordering so a broken setup gets back to a known state fast. Most layer sections here are deliberately thin link-outs to dedicated feature pages.

## 5. Try Key Features

These work in the base chat with no extra setup.

### Use the terminal

```
❯ What's my disk usage? Show the top 5 largest directories.
```

The agent runs terminal commands on your behalf and shows results.

### Slash commands

Type `/` to see an autocomplete dropdown of all commands:

| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands |
| `/tools` | List available tools |
| `/model` | Switch models interactively |
| `/personality pirate` | Try a fun personality |
| `/save` | Save the conversation |

### Multi-line input

Press `Alt+Enter`, `Ctrl+J`, or `Shift+Enter` to add a new line. Per the source, `Shift+Enter` requires a terminal that sends it as a distinct sequence (Kitty / foot / WezTerm / Ghostty by default; iTerm2 / Alacritty / VS Code terminal once the Kitty keyboard protocol is enabled). `Alt+Enter` and `Ctrl+J` work in every terminal.

### Interrupt the agent

If the agent is taking too long, type a new message and press Enter — it interrupts the current task and switches to your new instructions. `Ctrl+C` also works.

## 6. Add the Next Layer

Only after the base chat works. Pick what you need.

### Bot or shared assistant

```bash
hermes gateway setup    # Interactive platform configuration
```

Connect Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, or Microsoft Teams (see Messaging Overview).

### Automation and tools

- `hermes tools` — tune tool access per platform
- `hermes skills` — browse and install reusable workflows
- Cron — only after your bot or CLI setup is stable

### Sandboxed terminal

For safety, run the agent in a Docker container or on a remote server:

```bash
hermes config set terminal.backend docker    # Docker isolation
hermes config set terminal.backend ssh       # Remote server
```

### Voice mode

```bash
# From the Hermes install directory (the curl installer placed it at
# ~/.hermes/hermes-agent on Linux/macOS or %LOCALAPPDATA%\hermes\hermes-agent on Windows):
cd ~/.hermes/hermes-agent
uv pip install -e ".[voice]"
# Includes faster-whisper for free local speech-to-text
```

Then in the CLI: `/voice on`. Press `Ctrl+B` to record. See [Voice Mode](hermes_voice_mode_cli.md).

### Skills

Skills are on-demand instruction documents that teach Hermes how to do a specific task — deploy to Kubernetes, open a GitHub PR, fine-tune a model, search for GIFs. Each is a `SKILL.md` file with a name, a description, and a step-by-step procedure. The agent reads the short descriptions for free and only loads a skill's full content when a task actually calls for it, so adding skills doesn't bloat every request. Hermes ships with a catalog of bundled skills already installed in `~/.hermes/skills/`; you can add more from the Skills Hub or write your own.

Browse and install from the hub:

```bash
hermes skills browse                      # list everything available
hermes skills search kubernetes           # find skills by keyword
hermes skills install openai/skills/k8s   # install one (runs a security scan first)
```

The install argument is a `source/path` slug from the hub — `openai/skills/k8s` means the `k8s` skill from OpenAI's catalog. Every installed skill becomes a slash command automatically (e.g. `/k8s deploy the staging manifest`, or bare `/k8s` to load it and let Hermes ask what you need). This works in the CLI and in any connected messaging platform; you don't have to install everything up front, since the agent picks the right bundled skill on its own during normal conversation. See [Skills System](hermes_skills_system.md) for writing your own, external skill directories, and the full hub source list.

### MCP servers

```yaml
# Add to ~/.hermes/config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"
```

See [MCP](hermes_mcp_concept_config.md) for the full configuration surface.

### Editor integration (ACP)

ACP support ships with the standard `[all]` extras, so the curl installer already includes it. Just run `hermes acp`. (If you installed without `[all]`, run `cd ~/.hermes/hermes-agent && uv pip install -e ".[acp]"` first.) See [ACP Editor Integration](hermes_acp_editor_integration.md).

## Common Failure Modes

These are the problems that waste the most time:

| Symptom | Likely cause | Fix |
|---|---|---|
| Hermes opens but gives empty or broken replies | Provider auth or model selection is wrong | Run `hermes model` again and confirm provider, model, and auth |
| Custom endpoint "works" but returns garbage | Wrong base URL, model name, or not actually OpenAI-compatible | Verify the endpoint in a separate client first |
| Gateway starts but nobody can message it | Bot token, allowlist, or platform setup is incomplete | Re-run `hermes gateway setup` and check `hermes gateway status` |
| `hermes --continue` can't find old session | Switched profiles or session never saved | Check `hermes sessions list` and confirm you're in the right profile |
| Model unavailable or odd fallback behavior | Provider routing or fallback settings are too aggressive | Keep routing off until the base provider is stable |
| `hermes doctor` flags config problems | Config values are missing or stale | Fix the config, retest a plain chat before adding features |

## Recovery Toolkit

When something feels off, use this order:

1. `hermes doctor`
2. `hermes model`
3. `hermes setup`
4. `hermes sessions list`
5. `hermes --continue`
6. `hermes gateway status`

That sequence gets you from "broken vibes" back to a known state fast.

## Related Notes

**Terms**
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: §MCP servers config block.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled tasks; relevance: §Automation lists cron.
- [term_subagent](../../term_dictionary/term_subagent.md) — spawned sub-agents; relevance: delegation feature in this layer.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal isolation backend; relevance: §Sandboxed terminal (`terminal.backend docker/ssh`).
- [term_voice_wake](../../term_dictionary/term_voice_wake.md) — voice activation; relevance: §Voice mode (`/voice on`, Ctrl+B).
- [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — `SKILL.md` spec; relevance: §Skills describes SKILL.md docs.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — parallel agents; relevance: layering delegation/parallelism.
- [term_skills](../../term_dictionary/term_skills.md) — installable skill packages; relevance: §Skills browse/install/use.

**Code-Repos**
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — toolset config; relevance: `hermes tools` per-platform tuning.
- [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills system; relevance: `hermes skills browse/search/install` + slash-command skills.
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client/toolsets; relevance: §MCP servers `config.yaml` block.
- [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — ACP editor integration; relevance: §Editor integration (`hermes acp`).
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway + platforms; relevance: §Bot/shared assistant (`hermes gateway setup/status`, recovery toolkit).

**Snippets**
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — `hermes tools`; relevance: §Automation per-platform tool tuning.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — `hermes skills install`; relevance: §Skills browse/search/install.
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config; relevance: §MCP servers `config.yaml` block.
- [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — `hermes acp` entry; relevance: §Editor integration (ACP).
- [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — serve-as-MCP; relevance: MCP surface the §MCP-servers layer rides on.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron CRUD; relevance: §Automation "Cron — only after stable".
- [snippet_hermes_agent_cli_plugins_install](../../code_snippets/snippet_hermes_agent_cli_plugins_install.md) — plugin install; relevance: extending the feature layer with plugins.
- [snippet_hermes_agent_acp_server_prompt](../../code_snippets/snippet_hermes_agent_acp_server_prompt.md) — ACP server prompt; relevance: ACP editor session backing §Editor integration.
- [snippet_hermes_agent_cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — `/voice on` command; relevance: §Voice mode (record via Ctrl+B).
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — `hermes gateway` dispatch; relevance: §Bot/shared assistant (`gateway setup/status`) + recovery toolkit.

**Docs**
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — sibling part 1; relevance: prerequisite base chat.
- [hermes_skills](hermes_skills_system.md) — skills deep-dive; relevance: §Skills link-out.
- [hermes_mcp](hermes_mcp_concept_config.md) — MCP feature; relevance: §MCP servers link-out.
- [hermes_voice_mode](hermes_voice_mode_cli.md) — voice feature; relevance: §Voice mode link-out.
- hermes_messaging_overview — gateway setup; relevance: §Bot/assistant link-out.
- [hermes_acp](hermes_acp_editor_integration.md) — ACP feature; relevance: §Editor integration link-out.
- [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — analogous MCP setup; relevance: parallels §MCP servers.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — analogous skills; relevance: parallels §Skills.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — analogous delegation; relevance: parallels subagent spawning.
- [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — analogous scheduling; relevance: parallels the cron layering note.

**Source**: `inbox/hermes_agent_docs/getting-started/quickstart.md` · https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
**Last Updated**: 2026-06-19
**Status**: Active
