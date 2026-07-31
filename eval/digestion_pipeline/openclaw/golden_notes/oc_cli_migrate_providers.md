---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - migrate
keywords:
  - openclaw migrate providers
  - claude provider import
  - codex provider import
  - hermes provider import
  - migrate supported env keys
  - codex native plugin activation
  - manual-review migration state
  - openclaw migrate apply
topics:
  - OpenClaw
  - CLI migrate providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/migrate
access_control_group: ["general"]
---

# OpenClaw — `openclaw migrate` Per-Provider Import Matrix (Claude / Codex / Hermes)

## Overview

This note is the per-provider import matrix for `openclaw migrate`: exactly what each bundled migration provider (Claude, Codex, Hermes) imports into OpenClaw, what is copied or flagged as manual-review instead, and the provider-specific gating that controls credential and plugin import. It mirrors the **Claude provider**, **Codex provider**, and **Hermes provider** sections of the `cli/migrate` source page. The generic command surface, flag reference, preview-first safety model, plugin contract, and onboarding integration are documented separately in the sibling note `oc_cli_migrate` — this note assumes that workflow and only enumerates the provider-by-provider behavior. Each provider detects a default source directory (`--from <path>` overrides it) and imports via the shared `detect`/`plan`/`apply` contract, so everything below is what lands in OpenClaw on apply versus what is preserved for manual review.

## Claude provider

The bundled Claude provider detects Claude Code state at `~/.claude` by default. Use `--from <path>` to import a specific Claude Code home or project root. A user-facing walkthrough lives at `/install/migrating-claude` (owned by the Install sub-plans, referenced not duplicated here).

### What Claude imports

- Project `CLAUDE.md` and `.claude/CLAUDE.md` into the OpenClaw agent workspace.
- User `~/.claude/CLAUDE.md` appended to workspace `USER.md`.
- MCP server definitions from project `.mcp.json`, Claude Code `~/.claude.json`, and Claude Desktop `claude_desktop_config.json`.
- Claude skill directories that include `SKILL.md`.
- Claude command Markdown files converted into OpenClaw skills with manual invocation only.

### Archive and manual-review state

Claude hooks, permissions, environment defaults, local memory, path-scoped rules, subagents, caches, plans, and project history are preserved in the migration report or reported as manual-review items. OpenClaw does **not** execute hooks, copy broad allowlists, or import OAuth/Desktop credential state automatically.

## Codex provider

The bundled Codex provider detects Codex CLI state at `~/.codex` by default, or at `CODEX_HOME` when that environment variable is set. Use `--from <path>` to inventory a specific Codex home. Use this provider when moving to the OpenClaw Codex harness and you want to promote useful personal Codex CLI assets deliberately. Local Codex app-server launches use a per-agent `CODEX_HOME`, so they do not read your personal `~/.codex` by default; the normal process `HOME` is still inherited, so Codex can see shared `$HOME/.agents/*` skills/plugin marketplace entries and subprocesses can find user-home config and tokens.

Running `openclaw migrate codex` in an interactive terminal previews the full plan, then opens checkbox selectors before the final apply confirmation. Skill copy items are prompted first; use `Toggle all on` or `Toggle all off` for bulk selection, press Space to toggle rows, or Enter to activate the highlighted row and continue. Planned skills start checked, conflict skills start unchecked, and `Skip for now` skips skill copies for this run while still continuing to plugin selection. When source-installed curated Codex plugins are migratable and `--plugin` was not supplied, migration then prompts for native Codex plugin activation by plugin name; plugin items start checked unless the target OpenClaw Codex plugin config already has that plugin. Existing target plugins start unchecked and show a conflict hint such as `conflict: plugin exists`; choose `Toggle all off` to migrate no native Codex plugins in that run, or `Skip for now` to stop before applying. For scripted or exact runs, pass `--skill <name>` once per skill, or `--plugin <name>` to limit native Codex plugin migration non-interactively to one or more source-installed curated plugins:

```bash
openclaw migrate codex --dry-run --skill gog-vault77-google-workspace
openclaw migrate apply codex --yes --skill gog-vault77-google-workspace
openclaw migrate codex --dry-run --plugin google-calendar
openclaw migrate apply codex --yes --plugin google-calendar
```

### What Codex imports

- Codex CLI skill directories under `$CODEX_HOME/skills`, excluding Codex's `.system` cache.
- Personal AgentSkills under `$HOME/.agents/skills`, copied into the current OpenClaw agent workspace when you want per-agent ownership.
- Source-installed `openai-curated` Codex plugins discovered through Codex app-server `plugin/list`. Planning reads `plugin/read` for each enabled installed plugin. App-backed plugins require the source Codex app-server account response to be a ChatGPT subscription account; non-ChatGPT or missing account responses are skipped with `codex_subscription_required`. By default, migration does not call source `app/list`, so app-backed plugins that pass the account gate are planned without source app accessibility verification, and account lookup transport failures skip with `codex_account_unavailable`. Pass `--verify-plugin-apps` when you want migration to force a fresh source `app/list` snapshot and require every owned app to be present, enabled, and accessible before planning native activation; in that mode, account lookup transport failures fall through to source app inventory verification. The source app inventory snapshot is kept in memory for the current process — it is not written to migration output or target config. Disabled plugins, unreadable plugin details, subscription-gated source accounts, and (when verification is requested) missing apps, disabled apps, inaccessible apps, or source app inventory failures become manual skipped items with typed reasons instead of target config entries. Apply calls app-server `plugin/install` for each selected eligible plugin, even if the target app-server already reports that plugin as installed and enabled. Migrated Codex plugins are usable only in sessions that select the native Codex harness; they are not exposed to OpenClaw provider runs, ACP conversation bindings, or other harnesses.

### Manual-review Codex state

Codex `config.toml`, native `hooks/hooks.json`, non-curated marketplaces, cached plugin bundles that are not source-installed curated plugins, and source-installed plugins that fail the source subscription gate are not activated automatically. When `--verify-plugin-apps` is set, plugins that fail the source app-inventory gate are also skipped. These are copied or reported in the migration report for manual review.

For migrated source-installed curated plugins, apply writes the following config entries verbatim:

```yaml
plugins.entries.codex.enabled: true
plugins.entries.codex.config.codexPlugins.enabled: true
plugins.entries.codex.config.codexPlugins.allow_destructive_actions: true
# plus one explicit plugin entry with marketplaceName: "openai-curated"
# and pluginName for each selected plugin
```

Migration never writes `plugins["*"]` and never stores local marketplace cache paths. Source-side subscription failures are reported on manual items with typed reasons such as `codex_subscription_required`, `codex_account_unavailable`, `plugin_disabled`, or `plugin_read_unavailable`. With `--verify-plugin-apps`, source app-inventory failures can also appear as `app_inaccessible`, `app_disabled`, `app_missing`, or `app_inventory_unavailable`. Skipped plugins are not written to target config. Target-side auth-required installs are reported on the affected plugin item with `status: "skipped"`, `reason: "auth_required"`, and sanitized app identifiers; their explicit config entries are written disabled until you reauthorize and enable them. Other install failures are item-scoped `error` results. If Codex app-server plugin inventory is unavailable during planning, migration falls back to cached bundle advisory items instead of failing the whole migration.

## Hermes provider

The bundled Hermes provider detects state at `~/.hermes` by default. Use `--from <path>` when Hermes lives elsewhere. A user-facing walkthrough lives at `/install/migrating-hermes` (Install sub-plans).

### What Hermes imports

- Default model configuration from `config.yaml`.
- Configured model providers and custom OpenAI-compatible endpoints from `providers` and `custom_providers`.
- MCP server definitions from `mcp_servers` or `mcp.servers`.
- `SOUL.md` and `AGENTS.md` into the OpenClaw agent workspace.
- `memories/MEMORY.md` and `memories/USER.md` appended to workspace memory files.
- Memory config defaults for OpenClaw file memory, plus archive or manual-review items for external memory providers such as Honcho.
- Skills that include a `SKILL.md` file under `skills/<name>/`.
- Per-skill config values from `skills.config`.
- OpenCode OpenAI OAuth credentials from OpenCode `auth.json` when interactive credential migration is accepted, or when `--include-secrets` is set. Hermes `auth.json` OAuth entries are legacy state reported for manual OpenAI reauth or doctor repair.
- Supported API keys and tokens from Hermes `.env` and OpenCode `auth.json` when interactive credential migration is accepted, or when `--include-secrets` is set.

### Supported `.env` keys

The Hermes provider imports these credential environment-variable keys verbatim from Hermes `.env`:

```text
AI_GATEWAY_API_KEY        ALIBABA_API_KEY            ANTHROPIC_API_KEY
ARCEEAI_API_KEY           CEREBRAS_API_KEY           CHUTES_API_KEY
CLOUDFLARE_AI_GATEWAY_API_KEY                        COPILOT_GITHUB_TOKEN
DASHSCOPE_API_KEY         DEEPINFRA_API_KEY          DEEPSEEK_API_KEY
FIREWORKS_API_KEY         GEMINI_API_KEY             GH_TOKEN
GITHUB_TOKEN              GLM_API_KEY                GOOGLE_API_KEY
GROQ_API_KEY              HF_TOKEN                   HUGGINGFACE_HUB_TOKEN
KILOCODE_API_KEY          KIMICODE_API_KEY           KIMI_API_KEY
MINIMAX_API_KEY           MINIMAX_CODING_API_KEY     MISTRAL_API_KEY
MODELSTUDIO_API_KEY       MOONSHOT_API_KEY           NVIDIA_API_KEY
OPENAI_API_KEY            OPENCODE_API_KEY           OPENCODE_GO_API_KEY
OPENCODE_ZEN_API_KEY      OPENROUTER_API_KEY         QIANFAN_API_KEY
QWEN_API_KEY              TOGETHER_API_KEY           VENICE_API_KEY
XAI_API_KEY               XIAOMI_API_KEY             ZAI_API_KEY
Z_AI_API_KEY
```

### Archive-only state

Hermes state that OpenClaw cannot safely interpret is copied into the migration report for manual review, but it is **not** loaded into live OpenClaw config or credentials. This preserves opaque or unsafe state without pretending OpenClaw can execute or trust it automatically:

- `plugins/`
- `sessions/`
- `logs/`
- `cron/`
- `mcp-tokens/`
- `state.db`

### After applying

After a Hermes (or any) migration is applied, run the health check:

```bash
openclaw doctor
```

**Source**: OpenClaw documentation — `cli/migrate` (mirror `inbox/openclaw_docs/cli/migrate.md`), provider sections (Claude / Codex / Hermes)
**Last Updated**: 2026-06-22
**Status**: Active
