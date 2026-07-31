---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - migration
keywords:
  - openclaw migration guide
  - move openclaw new machine
  - openclaw state directory
  - auth-profiles.json credentials
  - openclaw doctor restart
  - tar czf openclaw-state
  - openclaw_state_dir profile
  - upgrade plugin in place
topics:
  - OpenClaw
  - Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/migrating
access_control_group: ["general"]
---

# OpenClaw — Migration Guide (Import, Machine Move, In-Place Plugin Upgrade)

## Overview

This note is the procedural runbook for OpenClaw's migration hub, mirroring the `install/migrating` source page. OpenClaw supports three migration paths: importing from another agent system, moving an existing install to a new machine, and upgrading a plugin in place. The bulk of the page — and of this note — is the machine-to-machine move: which parts of the **state directory** (`~/.openclaw/` by default) and workspace to copy, the four-step stop/install/copy/doctor flow, common pitfalls (profile or state-dir mismatch, copying `openclaw.json` alone, permissions, remote mode, secrets in backups), and a post-move verification checklist. The cross-system import and the in-place plugin upgrade are summarized here and link out to the dedicated provider/channel pages.

## Import from another agent system

Use the bundled migration providers to bring instructions, MCP servers, skills, model config, and (opt-in) API keys into OpenClaw. Plans are previewed before any change, secrets are redacted in reports, and apply is backed by a verified backup. Two import sources are documented as cards on the source page: **Migrating from Claude** (`/install/migrating-claude`) imports Claude Code and Claude Desktop state, including `CLAUDE.md`, MCP servers, skills, and project commands; **Migrating from Hermes** (`/install/migrating-hermes`) imports Hermes config, providers, MCP servers, memory, skills, and supported `.env` keys. The CLI entry point is `openclaw migrate` (`/cli/migrate`). Onboarding can also offer migration when it detects a known source, via `openclaw onboard --flow import`.

## Move OpenClaw to a new machine

Copy the **state directory** (`~/.openclaw/` by default) and your **workspace** to preserve the following, per the source page:

- **Config** — `openclaw.json` and all gateway settings.
- **Auth** — per-agent `auth-profiles.json` (API keys plus OAuth), plus any channel or provider state under `credentials/`.
- **Sessions** — conversation history and agent state.
- **Channel state** — WhatsApp login, Telegram session, and similar.
- **Workspace files** — `MEMORY.md`, `USER.md`, skills, and prompts.

Run `openclaw status` on the old machine to confirm your state directory path. Custom profiles use `~/.openclaw-<profile>/` or a path set via the `OPENCLAW_STATE_DIR` environment variable.

### Migration steps

The source page lays out a four-step `<Steps>` flow. **Step 1 — Stop the gateway and back up:** on the **old** machine, stop the gateway so files are not changing mid-copy, then archive the state directory.

```bash
openclaw gateway stop
cd ~
tar -czf openclaw-state.tgz .openclaw
```

If you use multiple profiles (for example `~/.openclaw-work`), archive each separately. **Step 2 — Install OpenClaw on the new machine:** install the CLI (and Node if needed) on the new machine; it is fine if onboarding creates a fresh `~/.openclaw/`, because you will overwrite it next. **Step 3 — Copy state directory and workspace:** transfer the archive via `scp`, `rsync -a`, or an external drive, then extract it on the new machine.

```bash
cd ~
tar -xzf openclaw-state.tgz
```

Ensure hidden directories were included and file ownership matches the user that will run the gateway. **Step 4 — Run doctor and verify:** on the new machine, run Doctor to apply config migrations and repair services, then restart the gateway and check status.

```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

### Verifying env-fallback tokens

If Telegram or Discord uses the default env fallback (`TELEGRAM_BOT_TOKEN` or `DISCORD_BOT_TOKEN`), verify the migrated state-dir `.env` contains those keys without printing the secret values.

```bash
awk -F= '/^(TELEGRAM_BOT_TOKEN|DISCORD_BOT_TOKEN)=/ { print $1 "=present" }' ~/.openclaw/.env
```

`openclaw doctor` also warns when an enabled default Telegram or Discord account has no configured token and the matching env variable is unavailable to the doctor process.

### Common pitfalls

The source page lists five common pitfalls as an `<AccordionGroup>`:

- **Profile or state-dir mismatch** — if the old gateway used `--profile` or `OPENCLAW_STATE_DIR` and the new one does not, channels will appear logged out and sessions will be empty. Launch the gateway with the **same** profile or state-dir you migrated, then rerun `openclaw doctor`.
- **Copying only `openclaw.json`** — the config file alone is not enough. Model auth profiles live under `agents/<agentId>/agent/auth-profiles.json`, and channel and provider state lives under `credentials/`. Always migrate the **entire** state directory.
- **Permissions and ownership** — if you copied as root or switched users, the gateway may fail to read credentials. Ensure the state directory and workspace are owned by the user running the gateway.
- **Remote mode** — if your UI points at a **remote** gateway, the remote host owns sessions and workspace. Migrate the gateway host itself, not your local laptop (see the FAQ at `/help/faq#where-things-live-on-disk`).
- **Secrets in backups** — the state directory contains auth profiles, channel credentials, and other provider state. Store backups encrypted, avoid insecure transfer channels, and rotate keys if you suspect exposure.

### Verification checklist

On the new machine, confirm: `openclaw status` shows the gateway running; channels are still connected (no re-pairing needed); the dashboard opens and shows existing sessions; and workspace files (memory, configs) are present.

## Upgrade a plugin in place

In-place plugin upgrades preserve the same plugin id and config keys but may move on-disk state into the current layout. Plugin-specific upgrade guides live alongside their channels — for example **Matrix migration** (`/channels/matrix-migration`) covers encrypted-state recovery limits, automatic snapshot behavior, and manual recovery commands.

**Source**: OpenClaw documentation — `install/migrating` (mirror `inbox/openclaw_docs/install/migrating.md`)
**Last Updated**: 2026-06-22
**Status**: Active
