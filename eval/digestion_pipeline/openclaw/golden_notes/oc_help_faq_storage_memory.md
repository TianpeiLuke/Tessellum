---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - storage_memory
keywords:
  - openclaw sandboxing memory
  - where openclaw stores data
  - openclaw state dir layout
  - agent workspace memory files
  - sandbox bind mounts
  - semantic memory search openai key
  - soul.md bootstrap budget
  - openclaw backup strategy
topics:
  - OpenClaw
  - Storage and Memory
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: Sandboxing, Memory, and On-Disk Layout

## Overview

This note answers the OpenClaw FAQ's **"Sandboxing and memory"** and **"Where things live on disk"** sections, covering how sandboxing isolates tool execution, how OpenClaw memory works and what its limits are, whether semantic memory search needs an OpenAI key, and exactly where OpenClaw keeps state, sessions, auth, config, and the agent workspace on disk. It mirrors the `help/faq` source page (the `<Accordion>` Q&As under those two H2s); deeper sandboxing/memory how-tos and the full config reference are linked to their owning pages, not duplicated here.

## Sandboxing

There is a dedicated sandboxing doc at `/gateway/sandboxing`; for Docker-specific setup (the full gateway in Docker or sandbox images) see `/install/docker`. The default Docker image is **security-first** and runs as the `node` user, so it does not include system packages, Homebrew, or bundled browsers. To enable a fuller setup: persist `/home/node` with `OPENCLAW_HOME_VOLUME` so caches survive; bake system deps into the image with `OPENCLAW_IMAGE_APT_PACKAGES`; install Playwright browsers via the bundled CLI with `node /app/node_modules/playwright-core/cli.js install chromium`; and set `PLAYWRIGHT_BROWSERS_PATH`, ensuring the path is persisted.

You can keep DMs personal but make groups public/sandboxed under one agent — **if** private traffic is DMs and public traffic is groups. Set `agents.defaults.sandbox.mode: "non-main"` so group/channel sessions (non-main keys) run in the configured sandbox backend, while the main DM session stays on-host. Docker is the default backend if you do not choose one. Then restrict what tools are available in sandboxed sessions via `tools.sandbox.tools`.

To bind a host folder into the sandbox, set `agents.defaults.sandbox.docker.binds` to `["host:path:mode"]` (e.g., `"/home/user/src:/src:ro"`). Global and per-agent binds merge; per-agent binds are ignored when `scope: "shared"`. Use `:ro` for anything sensitive, and remember **binds bypass the sandbox filesystem walls**. OpenClaw validates bind sources against both the normalized path and the canonical path resolved through the deepest existing ancestor — so symlink-parent escapes still fail closed even when the last path segment does not exist yet, and allowed-root checks still apply after symlink resolution. See `/gateway/sandboxing#custom-bind-mounts` and `/gateway/sandbox-vs-tool-policy-vs-elevated#bind-mounts-security-quick-check` for examples and safety notes.

## How Memory Works

OpenClaw memory is just Markdown files in the agent workspace: daily notes in `memory/YYYY-MM-DD.md`, and curated long-term notes in `MEMORY.md` (main/private sessions only). OpenClaw also runs a **silent pre-compaction memory flush** that reminds the model to write durable notes before auto-compaction; this only runs when the workspace is writable (read-only sandboxes skip it).

If memory keeps forgetting things, ask the bot to **write the fact to memory** — long-term notes belong in `MEMORY.md`, short-term context goes into `memory/YYYY-MM-DD.md`. This is still an area being improved; it helps to remind the model to store memories (it will know what to do), and if it keeps forgetting, verify the Gateway is using the same workspace on every run.

### Persistence and Limits

Memory files live on disk and persist until you delete them — the limit is your storage, not the model. The **session context** is still limited by the model context window, so long conversations can compact or truncate; that is why memory search exists, pulling only the relevant parts back into context.

### Semantic Memory Search

Semantic memory search requires an OpenAI API key **only if you use OpenAI embeddings**. Codex OAuth covers chat/completions and does **not** grant embeddings access, so signing in with Codex (OAuth or the Codex CLI login) does not help for semantic memory search; OpenAI embeddings still need a real API key (`OPENAI_API_KEY` or `models.providers.openai.apiKey`). If you don't set a provider explicitly, OpenClaw uses OpenAI embeddings, and legacy configs that still say `memorySearch.provider = "auto"` resolve to OpenAI too; if no OpenAI API key is available, semantic memory search stays unavailable until you configure a key or choose another provider explicitly. To stay local, set `memorySearch.provider = "local"` (and optionally `memorySearch.fallback = "none"`); for Gemini embeddings, set `memorySearch.provider = "gemini"` and provide `GEMINI_API_KEY` (or `memorySearch.remote.apiKey`). Supported embedding models: **OpenAI, OpenAI-compatible, Gemini, Voyage, Mistral, Bedrock, Ollama, LM Studio, GitHub Copilot, DeepInfra, or local**.

## Where Things Live on Disk

OpenClaw's state is local, but external services still see what you send them. By default sessions, memory files, config, and workspace live on the Gateway host (`~/.openclaw` plus your workspace directory); messages sent to model providers (Anthropic/OpenAI/etc.) go to their APIs, and chat platforms (WhatsApp/Telegram/Slack/etc.) store message data on their servers. Using local models keeps prompts on your machine, but channel traffic still goes through the channel's servers.

### State Directory Layout

Everything lives under `$OPENCLAW_STATE_DIR` (default: `~/.openclaw`):

| Path | Purpose |
| --- | --- |
| `$OPENCLAW_STATE_DIR/openclaw.json` | Main config (JSON5) |
| `$OPENCLAW_STATE_DIR/credentials/oauth.json` | Legacy OAuth import (copied into auth profiles on first use) |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth-profiles.json` | Auth profiles (OAuth, API keys, and optional `keyRef`/`tokenRef`) |
| `$OPENCLAW_STATE_DIR/secrets.json` | Optional file-backed secret payload for `file` SecretRef providers |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth.json` | Legacy compatibility file (static `api_key` entries scrubbed) |
| `$OPENCLAW_STATE_DIR/credentials/` | Provider state (e.g. `whatsapp/<accountId>/creds.json`) |
| `$OPENCLAW_STATE_DIR/agents/` | Per-agent state (agentDir + sessions) |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/` | Conversation history & state (per agent) |
| `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/sessions.json` | Session metadata (per agent) |

The legacy single-agent path is `~/.openclaw/agent/*` (migrated by `openclaw doctor`). Your **workspace** (AGENTS.md, memory files, skills, etc.) is separate and configured via `agents.defaults.workspace` (default: `~/.openclaw/workspace`).

### Workspace vs State Dir

`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`, `memory/YYYY-MM-DD.md`, and optional `HEARTBEAT.md` live in the **agent workspace** (per agent), not `~/.openclaw`. The lowercase root `memory.md` is legacy repair input only; `openclaw doctor --fix` can merge it into `MEMORY.md` when both files exist. The **state dir** (`~/.openclaw`) holds config, channel/provider state, auth profiles, sessions, logs, and shared skills (`~/.openclaw/skills`). The default workspace is `~/.openclaw/workspace`, configurable via:

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

If the bot "forgets" after a restart, confirm the Gateway is using the same workspace on every launch — and remember that remote mode uses the **gateway host's** workspace, not your local laptop. To make a behavior or preference durable, ask the bot to **write it into `AGENTS.md` or `MEMORY.md`** rather than relying on chat history. Session state is owned by the **gateway host**: in remote mode, the session store you care about is on the remote machine, not your local laptop (see `/concepts/session`).

### Resizing Bootstrap Files (SOUL.md)

`SOUL.md` is one of the workspace bootstrap files injected into the agent context. The default per-file injection limit is `20000` characters, and the total bootstrap budget across files is `60000` characters. Change the shared defaults with `agents.defaults.bootstrapMaxChars` / `agents.defaults.bootstrapTotalMaxChars`, or override one agent under `agents.list[]`:

```json5
{
  agents: {
    defaults: {
      bootstrapMaxChars: 50000,
      bootstrapTotalMaxChars: 300000,
    },
  },
}
```

Use `/context` to check raw vs injected sizes and whether truncation happened. Keep `SOUL.md` focused on voice, stance, and personality; put operating rules in `AGENTS.md` and durable facts in memory.

### Backup, Uninstall, and Working Outside the Workspace

For backup, put your **agent workspace** in a **private** git repo and back it up somewhere private (e.g. a GitHub private repo) — this captures memory plus AGENTS/SOUL/USER files and lets you restore the assistant's "mind" later. Do **not** commit anything under `~/.openclaw` (credentials, sessions, tokens, or encrypted secrets payloads); for a full restore, back up the workspace and the state directory separately. To completely uninstall, see `/install/uninstall`. Agents can work outside the workspace: the workspace is the **default cwd** and memory anchor, not a hard sandbox — relative paths resolve inside the workspace, but absolute paths can reach other host locations unless sandboxing is enabled. For isolation use `agents.defaults.sandbox` or per-agent sandbox settings; to make a repo the default working directory, point that agent's `workspace` at the repo root (the OpenClaw repo is just source code — keep the workspace separate unless you intentionally want the agent to work inside it).

**Source**: OpenClaw documentation — `help/faq` (sections "Sandboxing and memory" + "Where things live on disk"; mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
