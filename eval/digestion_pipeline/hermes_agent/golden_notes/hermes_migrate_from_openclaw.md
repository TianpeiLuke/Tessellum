---
tags:
  - resource
  - documentation
  - hermes_agent
  - migration
  - openclaw
keywords:
  - hermes claw migrate
  - openclaw to hermes
  - config key mapping
  - migrate secrets
  - secretref resolution
  - api key resolution
topics:
  - Hermes Agent
  - Migration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw
access_control_group: ["general"]
---

# Migrate from OpenClaw

## Overview

This is the reference procedure for `hermes claw migrate`, the command that imports an existing OpenClaw (or legacy Clawdbot/Moltbot) setup into Hermes. It is a how-to: it documents the exact flags, the OpenClaw→Hermes config-key mapping tables, how secrets are resolved, what gets archived for manual review, and the post-migration checklist — not the conceptual comparison of the two agents (that is `thought_hermes_agent_vs_openclaw`). The migration reads from `~/.openclaw/` by default (auto-detecting `~/.clawdbot/` and `~/.moltbot/` and the legacy `clawdbot.json`/`moltbot.json` filenames), always shows a full preview before touching anything, and writes a pre-migration zip restore-point under `~/.hermes/backups/` unless `--no-backup` is passed. Secrets are never imported silently — `--migrate-secrets` is required even under `--preset full`. If the old setup was multi-provider, `hermes setup --portal` can collapse it to one OAuth (300+ models plus the Tool Gateway).

## Quick start

```bash
# Preview then migrate (always shows a preview first, then asks to confirm)
hermes claw migrate

# Preview only, no changes
hermes claw migrate --dry-run

# Full migration including API keys, skip confirmation
hermes claw migrate --preset full --migrate-secrets --yes
```

The migration always shows a full preview of what will be imported before making any changes — review the list, then confirm. Workspace files are looked up at `workspace/`, then the fallbacks `workspace.default/` and `workspace-main/` (OpenClaw renamed `workspace/` to `workspace-main/` in recent versions, and uses `workspace-{agentId}` for multi-agent setups).

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview only — stop after showing what would be migrated. |
| `--preset <name>` | `full` (all compatible settings) or `user-data` (excludes infrastructure config). Neither preset imports secrets by default. |
| `--overwrite` | Overwrite existing Hermes files on conflicts (default: refuse to apply when the plan has conflicts). |
| `--migrate-secrets` | Include API keys. Required even under `--preset full`. |
| `--no-backup` | Skip the pre-migration zip snapshot of `~/.hermes/` (default writes one restore-point archive, restorable with `hermes import`). |
| `--source <path>` | Custom OpenClaw directory. |
| `--workspace-target <path>` | Where to place `AGENTS.md`. |
| `--skill-conflict <mode>` | `skip` (default), `overwrite`, or `rename`. |
| `--yes` | Skip the confirmation prompt after preview. |

## What gets migrated

**Persona, memory, and instructions.** `workspace/SOUL.md` → `~/.hermes/SOUL.md` (direct copy); `workspace/AGENTS.md` → `AGENTS.md` in `--workspace-target` (requires the flag); `workspace/MEMORY.md` → `~/.hermes/memories/MEMORY.md` (parsed into entries, merged with existing, deduped, using the `§` delimiter); `workspace/USER.md` → `~/.hermes/memories/USER.md` (same entry-merge logic); daily `workspace/memory/*.md` files all merged into the main memory.

**Skills (4 sources)** all land in `~/.hermes/skills/openclaw-imports/`: workspace skills (`workspace/skills/`), managed/shared (`~/.openclaw/skills/`), personal cross-project (`~/.agents/skills/`), and project-level shared (`workspace/.agents/skills/`). Conflicts honor `--skill-conflict`: `skip` keeps the existing skill, `overwrite` replaces it, `rename` writes a `-imported` copy.

**Model and provider configuration.** `agents.defaults.model` → `config.yaml` `model` (string or `{primary, fallbacks}`); `models.providers.*` → `config.yaml` `custom_providers` (maps `baseUrl`, `apiType`/`api`, handling both short and hyphenated provider values); `models.providers.*.apiKey` → `~/.hermes/.env` (requires `--migrate-secrets`).

**Agent behavior** mappings (selected): `agents.defaults.timeoutSeconds` → `agent.max_turns` (`timeoutSeconds / 10`, capped at 200); `verboseDefault` → `agent.verbose`; `thinkingDefault` → `agent.reasoning_effort` (always/high/xhigh → high, auto/medium/adaptive → medium, off/low/none/minimal → low); `compaction.mode` → `compression.enabled` (off → false, else true); `humanDelay.*` → `human_delay.*`; `userTimezone` → `timezone`; `tools.exec.timeoutSec` → `terminal.timeout`; `sandbox.backend`/`sandbox.docker.image` → `terminal.backend`/`terminal.docker_image`.

**Session reset policies.** `session.reset.mode` → `session_reset.mode` (daily/idle/both), `session.reset.atHour` → `session_reset.at_hour`, `session.reset.idleMinutes` → `session_reset.idle_minutes`. If structured `session.reset` is absent, the migration falls back to inferring from the `session.resetTriggers` string array.

**MCP servers.** Each `mcp.servers.*` field maps 1:1 to `mcp_servers.*`: `command`/`args`/`env`/`cwd` (stdio), `url` (HTTP/SSE), and `tools.include`/`tools.exclude` (tool filtering).

**TTS (text-to-speech)** is read from two OpenClaw locations by priority — `messages.tts.providers.{provider}.*` (canonical), top-level `talk.providers.{provider}.*` (fallback), then legacy flat `messages.tts.{provider}.*`. It writes `tts.provider`, the ElevenLabs `voice_id`/`model_id`, the OpenAI `model`/`voice`, the `edge.voice` (OpenClaw renamed "edge" to "microsoft" — both recognized), and copies TTS assets to `~/.hermes/tts/`.

**Messaging platforms.** Tokens (string, env-template, or SecretRef; both flat and `accounts.default` layouts) map to `.env` variables: Telegram (`TELEGRAM_BOT_TOKEN`, plus `TELEGRAM_ALLOWED_USERS` comma-joined from `allowFrom[]`), Discord (`DISCORD_BOT_TOKEN`/`DISCORD_ALLOWED_USERS`), Slack (`SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN`/`SLACK_ALLOWED_USERS`), WhatsApp (`WHATSAPP_ALLOWED_USERS` — auth is Baileys QR pairing, so re-pair after migration), Signal (`SIGNAL_ACCOUNT`/`SIGNAL_HTTP_URL`/`SIGNAL_ALLOWED_USERS`), Matrix (`MATRIX_ACCESS_TOKEN` — uses `accessToken`, not `botToken`), and Mattermost (`MATTERMOST_BOT_TOKEN`).

**Other config.** `approvals.exec.mode` → `approvals.mode` (auto→off, always→manual, smart→smart); `exec-approvals.json` → `command_allowlist` (patterns merged + deduped); `browser.cdpUrl`/`browser.headless` → `browser.cdp_url`/`browser.headless`; `tools.web.search.brave.apiKey` → `.env` `BRAVE_API_KEY`; `gateway.auth.token` → `.env` `HERMES_GATEWAY_TOKEN`; `agents.defaults.workspace` → `terminal.cwd`.

## Archived (no direct Hermes equivalent)

Items with no Hermes equivalent are saved to `~/.hermes/migration/openclaw/<timestamp>/archive/` for manual review, each with a recreate path: `IDENTITY.md` (merge into `SOUL.md`), `TOOLS.md` (Hermes has built-in tool instructions), `HEARTBEAT.md` (use cron jobs), `BOOTSTRAP.md` (use context files or skills), cron jobs (`hermes cron create`), plugins (the plugins guide), hooks/webhooks (`hermes webhook` or gateway hooks), the memory backend (`hermes honcho`), the skills registry (`hermes skills config`), UI/identity (`/skin`), logging (`config.yaml` logging section), the multi-agent list (Hermes profiles), and channel bindings / complex channels (manual per-platform setup).

## API key resolution

When `--migrate-secrets` is enabled, keys are collected from **four sources** in priority order: (1) config values — `models.providers.*.apiKey` and TTS provider keys in `openclaw.json`; (2) the env file `~/.openclaw/.env`; (3) the config env sub-object (`openclaw.json` → `"env"` or `"env"."vars"`); (4) auth profiles (`~/.openclaw/agents/main/agent/auth-profiles.json`). Config values take priority; each subsequent source fills remaining gaps. Only an allowlist of targets is ever copied — `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `ZAI_API_KEY`, `MINIMAX_API_KEY`, `ELEVENLABS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `VOICE_TOOLS_OPENAI_KEY` — keys outside it are never copied.

## SecretRef handling

OpenClaw token/key values come in three formats, all resolved by the migration:

```json
// Plain string
"channels": { "telegram": { "botToken": "123456:ABC-DEF..." } }

// Environment template
"channels": { "telegram": { "botToken": "${TELEGRAM_BOT_TOKEN}" } }

// SecretRef object
"channels": { "telegram": { "botToken": { "source": "env", "id": "TELEGRAM_BOT_TOKEN" } } }
```

For env templates and `source: "env"` SecretRefs, the value is looked up in `~/.openclaw/.env` and the `openclaw.json` env sub-object. SecretRefs with `source: "file"` or `source: "exec"` cannot be resolved automatically — the migration warns, and those values must be added manually via `hermes config set`.

## After migration

1. **Check the migration report** — printed on completion with migrated/skipped/conflicting counts.
2. **Review archived files** — anything under `~/.hermes/migration/openclaw/<timestamp>/archive/` needs manual attention.
3. **Start a new session** — imported skills and memory take effect in new sessions, not the current one.
4. **Verify API keys** — run `hermes status` to check provider authentication.
5. **Test messaging** — restart the gateway: `systemctl --user restart hermes-gateway`.
6. **Check session policies** — run `hermes config show` and verify `session_reset`.
7. **Re-pair WhatsApp** — QR pairing (Baileys), not token migration: run `hermes whatsapp`.
8. **Archive cleanup** — once everything works, run `hermes claw cleanup` to rename leftover OpenClaw directories to `.pre-migration/`.

## Troubleshooting

- **"OpenClaw directory not found"** — checks `~/.openclaw/`, then `~/.clawdbot/`, then `~/.moltbot/`; use `--source /path` if elsewhere.
- **"No provider API keys found"** — keys may be inline in `openclaw.json`, in `~/.openclaw/.env`, in the `"env"` sub-object, or in `auth-profiles.json` (all four checked); `source: "file"`/`"exec"` SecretRefs must be added via `hermes config set`.
- **Skills not appearing** — imported skills land in `~/.hermes/skills/openclaw-imports/`; start a new session or run `/skills` to verify.
- **TTS voice not migrated** — settings live in `messages.tts.providers.*` and top-level `talk` (both checked); a UI-set voice ID may need `hermes config set tts.elevenlabs.voice_id YOUR_VOICE_ID`.

**Source**: `inbox/hermes_agent_docs/guides/migrate-from-openclaw.md` · https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw
**Last Updated**: 2026-06-19
**Status**: Active
