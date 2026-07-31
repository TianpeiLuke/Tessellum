---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_runtime
keywords:
  - openclaw embedded agent runtime
  - single agent per gateway
  - bootstrap files agents soul tools
  - agents.defaults.workspace
  - skills load precedence
  - jsonl session store sessionid
  - steering while streaming queue
  - provider model ref parsing
topics:
  - OpenClaw
  - Agent Runtime
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/agent
access_control_group: ["general"]
---

# OpenClaw — The Embedded Agent Runtime Contract

## Overview

This note defines OpenClaw's **embedded agent runtime** contract: the single agent process per Gateway, with its own workspace, injected bootstrap files, and session store. It mirrors the `concepts/agent` source page — what the workspace must contain, which user-editable files get injected into the system prompt, the built-in tool surface, the skill-load precedence order, the runtime ownership boundary, the JSONL session store, mid-run steering and block-streaming defaults, `provider/model` ref parsing, and the minimal configuration. Full workspace layout, the agent loop lifecycle, and the runtime taxonomy are documented separately and linked below.

## Workspace (required)

OpenClaw uses a single agent workspace directory (`agents.defaults.workspace`) as the agent's **only** working directory (`cwd`) for tools and context. The recommended way to bootstrap it is to run `openclaw setup`, which creates `~/.openclaw/openclaw.json` if it is missing and initializes the workspace files. If `agents.defaults.sandbox` is enabled, non-main sessions can override this with per-session workspaces under `agents.defaults.sandbox.workspaceRoot` (a Gateway configuration concern). The full workspace layout and backup guide live on the dedicated Agent workspace page.

## Bootstrap files (injected)

Inside `agents.defaults.workspace`, OpenClaw expects these user-editable files: `AGENTS.md` (operating instructions + "memory"), `SOUL.md` (persona, boundaries, tone), `TOOLS.md` (user-maintained tool notes, e.g. `imsg`, `sag`, conventions), `BOOTSTRAP.md` (one-time first-run ritual, deleted after completion), `IDENTITY.md` (agent name/vibe/emoji), and `USER.md` (user profile + preferred address). On the first turn of a new session, OpenClaw injects the contents of these files into the system prompt's Project Context.

Blank files are skipped, and large files are trimmed and truncated with a marker so prompts stay lean. If a file is missing, OpenClaw injects a single "missing file" marker line, and `openclaw setup` will create a safe default template. `BOOTSTRAP.md` is only created for a **brand new workspace** (no other bootstrap files present); while it is pending, OpenClaw keeps it in Project Context and adds system-prompt bootstrap guidance for the initial ritual instead of copying it into the user message, and if you delete it after completing the ritual it should not be recreated on later restarts.

After a workspace has been observed, OpenClaw also keeps a state-dir attestation marker for the workspace path. If a recently attested workspace disappears or is wiped, startup refuses to silently re-seed `BOOTSTRAP.md`; restore the workspace or use a full onboard reset so the workspace and marker are cleared together. To disable bootstrap file creation entirely (for pre-seeded workspaces), set:

```json5
{ agents: { defaults: { skipBootstrap: true } } }
```

## Built-in tools

Core tools (read/exec/edit/write and related system tools) are always available, subject to tool policy. `apply_patch` is optional and gated by `tools.exec.applyPatch`. `TOOLS.md` does **not** control which tools exist — it is guidance for how _you_ want them used.

## Skills

OpenClaw loads skills from these locations, highest precedence first:

- Workspace: `<workspace>/skills`
- Project agent skills: `<workspace>/.agents/skills`
- Personal agent skills: `~/.agents/skills`
- Managed/local: `~/.openclaw/skills`
- Bundled (shipped with the install)
- Extra skill folders: `skills.load.extraDirs`

Skill roots can contain grouped folders such as `<workspace>/skills/personal/foo/SKILL.md`; the skill is still exposed by its flat frontmatter name, for example `foo`. Skills can be gated by config/env (the `skills` section in Gateway configuration).

## Runtime boundaries

The embedded agent runtime is OpenClaw-owned: model discovery, tool wiring, prompt assembly, session management, and channel delivery share one integrated runtime surface.

## Sessions

Session transcripts are stored as JSONL at `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`. The session ID is stable and chosen by OpenClaw. Legacy session folders from other tools are not read.

## Steering while streaming

Inbound prompts that arrive mid-run are steered into the current run by default. Steering is delivered **after the current assistant turn finishes executing its tool calls**, before the next LLM call, and no longer skips remaining tool calls from the current assistant message. `/queue steer` is the default active-run behavior; `/queue followup` and `/queue collect` make messages wait for a later turn instead of steering; `/queue interrupt` aborts the active run instead. The Queue and Steering queue pages describe queue and boundary behavior.

Block streaming sends completed assistant blocks as soon as they finish; it is **off by default** (`agents.defaults.blockStreamingDefault: "off"`). Tune the boundary via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end`; defaults to `text_end`). Control soft block chunking with `agents.defaults.blockStreamingChunk` (defaults to 800-1200 chars; prefers paragraph breaks, then newlines, then sentences last). Coalesce streamed chunks with `agents.defaults.blockStreamingCoalesce` to reduce single-line spam (idle-based merging before send). Non-Telegram channels require explicit `*.blockStreaming: true` to enable block replies. Verbose tool summaries are emitted at tool start (no debounce), and the Control UI streams tool output via agent events when available.

## Model refs

Model refs in config (for example `agents.defaults.model` and `agents.defaults.models`) are parsed by splitting on the **first** `/`. Use `provider/model` when configuring models. If the model ID itself contains `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`). If you omit the provider, OpenClaw tries an alias first, then a unique configured-provider match for that exact model id, and only then falls back to the configured default provider; if that provider no longer exposes the configured default model, OpenClaw falls back to the first configured provider/model instead of surfacing a stale removed-provider default.

## Configuration (minimal)

At minimum, set `agents.defaults.workspace` and `channels.whatsapp.allowFrom` (strongly recommended).

**Source**: OpenClaw documentation — `concepts/agent` (mirror `inbox/openclaw_docs/concepts/agent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
