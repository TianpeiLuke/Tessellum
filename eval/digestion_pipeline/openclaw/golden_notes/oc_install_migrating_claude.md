---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - migration
keywords:
  - openclaw migrate claude
  - import claude code into openclaw
  - claude migration provider
  - openclaw onboard import-from claude
  - claude.md agents.md user.md import
  - mcp server import openclaw
  - claude skills commands import
  - dry-run apply backup doctor
  - migration archive-only
topics:
  - OpenClaw
  - Install — Migrating from Claude
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/migrating-claude
access_control_group: ["general"]
---

# OpenClaw — Migrating from Claude (Claude Code / Claude Desktop Import)

## Overview

This note is the runbook for importing local Claude Code and Claude Desktop state into OpenClaw using the bundled **Claude migration provider**, mirroring the `install/migrating-claude` source page. The provider previews every item before changing state, redacts secrets in plans and reports, and creates a verified backup before apply. The note covers the two entry paths (onboarding wizard vs the `openclaw migrate` CLI), exactly what is auto-imported (instructions/memory, MCP servers, skills/commands) versus what stays archive-only, how `--from` selects the import source, the recommended preview → apply-with-backup → doctor → restart flow, conflict handling with `--overwrite`, the JSON-for-automation mode, and the documented troubleshooting cases.

## Two Ways to Import

OpenClaw imports local Claude state through the bundled Claude migration provider. There are two entry points.

**Onboarding wizard** — the wizard offers Claude when it detects local Claude state. Onboarding imports **require a fresh OpenClaw setup**: if you already have local OpenClaw state, reset config, credentials, sessions, and the workspace first, or use `openclaw migrate` directly with `--overwrite` after reviewing the plan. Run the import flow, or point it at a specific source:

```bash
openclaw onboard --flow import
openclaw onboard --import-from claude --import-source ~/.claude
```

**CLI** — use `openclaw migrate` for scripted or repeatable runs (see the [`openclaw migrate`](https://docs.openclaw.ai/cli/migrate) reference for the full plugin contract and JSON shapes). Add `--from <path>` to import a specific Claude Code home or project root.

```bash
openclaw migrate claude --dry-run
openclaw migrate apply claude --yes
```

## What Gets Imported

The provider auto-imports three categories of state into the live OpenClaw setup:

- **Instructions and memory** — project `CLAUDE.md` and `.claude/CLAUDE.md` content is copied or appended into the OpenClaw agent workspace `AGENTS.md`; user `~/.claude/CLAUDE.md` content is appended into the workspace `USER.md`.
- **MCP servers** — MCP server definitions are imported from project `.mcp.json`, Claude Code `~/.claude.json`, and Claude Desktop `claude_desktop_config.json` when present.
- **Skills and commands** — Claude skills with a `SKILL.md` file are copied into the OpenClaw workspace skills directory; Claude command Markdown files under `.claude/commands/` or `~/.claude/commands/` are converted into OpenClaw skills with `disable-model-invocation: true`.

## What Stays Archive-Only

The provider copies the following into the migration report for manual review, but does **not** load them into live OpenClaw config: Claude hooks; Claude permissions and broad tool allowlists; Claude environment defaults; `CLAUDE.local.md`; `.claude/rules/`; Claude subagents under `.claude/agents/` or `~/.claude/agents/`; Claude Code caches, plans, and project history directories; and Claude Desktop extensions and OS-stored credentials. OpenClaw refuses to execute hooks, trust permission allowlists, or decode opaque OAuth and Desktop credential state automatically. Move what you need by hand after reviewing the archive.

## Source Selection

Without `--from`, OpenClaw inspects the default Claude Code home at `~/.claude`, the sampled Claude Code `~/.claude.json` state file, and the Claude Desktop MCP config on macOS. When `--from` points at a project root, OpenClaw imports only that project's Claude files — such as `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`, `.claude/skills/`, and `.mcp.json` — and does **not** read your global Claude home during a project-root import.

## Recommended Flow

The recommended sequence is preview → apply-with-backup → doctor → restart-and-verify.

1. **Preview the plan** — the plan lists everything that will change, including conflicts, skipped items, and sensitive values redacted from nested MCP `env` or `headers` fields.
2. **Apply with backup** — OpenClaw creates and verifies a backup before applying.
3. **Run doctor** — [Doctor](https://docs.openclaw.ai/gateway/doctor) checks for config or state issues after the import.
4. **Restart and verify** — confirm the gateway is healthy and your imported instructions, MCP servers, and skills are loaded.

```bash
openclaw migrate claude --dry-run
openclaw migrate apply claude --yes
openclaw doctor
openclaw gateway restart
openclaw status
```

## Conflict Handling

Apply refuses to continue when the plan reports conflicts (a file or config value already exists at the target). Rerun with `--overwrite` **only** when replacing the existing target is intentional; providers may still write item-level backups for overwritten files in the migration report directory. For a fresh OpenClaw install, conflicts are unusual — they typically appear when you re-run the import on a setup that already has user edits.

## JSON Output for Automation

For scripted/CI use, the migration commands accept `--json`:

```bash
openclaw migrate claude --dry-run --json
openclaw migrate apply claude --json --yes
```

With `--json` and **no** `--yes`, apply prints the plan and does **not** mutate state. This is the safest mode for CI and shared scripts.

## Troubleshooting

- **Claude state lives outside `~/.claude`** — pass `--from /actual/path` (CLI) or `--import-source /actual/path` (onboarding).
- **Onboarding refuses to import on an existing setup** — onboarding imports require a fresh setup; either reset state and re-onboard, or use `openclaw migrate apply claude` directly, which supports `--overwrite` and explicit backup control.
- **MCP servers from Claude Desktop did not import** — Claude Desktop reads `claude_desktop_config.json` from a platform-specific path; point `--from` at that file's directory if OpenClaw did not detect it automatically.
- **Claude commands became skills with model invocation disabled** — this is by design: Claude commands are user-triggered, so OpenClaw imports them as skills with `disable-model-invocation: true`; edit each skill's frontmatter if you want the agent to invoke them automatically.

**Source**: OpenClaw documentation — `install/migrating-claude` (mirror `inbox/openclaw_docs/install/migrating-claude.md`)
**Last Updated**: 2026-06-22
**Status**: Active
