---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - skill_management
keywords:
  - agent-managed skills
  - skill_manage tool
  - skills hub
  - skill install sources
  - security scanning trust levels
  - skills write approval
  - hermes skills reset
topics:
  - Hermes Agent
  - Skills System
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
access_control_group: ["general"]
---

# Hermes Skills Hub & Agent-Managed Skills

## Overview

This is the **procedural surface of the Hermes skill library** — how skills get created, installed, secured, and maintained, as opposed to what a skill *is* (concept) or its SKILL.md file *model*. It covers three machineries: the agent's `skill_manage` tool (its procedural memory, optionally gated by `skills.write_approval`), the **Skills Hub** that browses/installs skills across nine online sources with a security scanner and trust levels, and `hermes skills reset` for re-baselining bundled skills against upstream. Every command works both from the CLI (`hermes skills ...`) and inside a chat session as a `/skills` slash command.

## Agent-Managed Skills (skill_manage tool)

The agent can create, update, and delete its own skills via the `skill_manage` tool. This is the agent's **procedural memory** — when it figures out a non-trivial workflow, it saves the approach as a skill for future reuse.

**When the agent creates skills:**

- After completing a complex task (5+ tool calls) successfully
- When it hit errors or dead ends and found the working path
- When the user corrected its approach
- When it discovered a non-trivial workflow

**Actions** (the SKILL.md file model these write is documented in `hermes_skill_md_format_bundles`):

| Action | Use for | Key params |
|--------|---------|------------|
| `create` | New skill from scratch | `name`, `content` (full SKILL.md), optional `category` |
| `patch` | Targeted fixes (preferred) | `name`, `old_string`, `new_string` |
| `edit` | Major structural rewrites | `name`, `content` (full SKILL.md replacement) |
| `delete` | Remove a skill entirely | `name` |
| `write_file` | Add/update supporting files | `name`, `file_path`, `file_content` |
| `remove_file` | Remove a supporting file | `name`, `file_path` |

The `patch` action is preferred for updates — it is more token-efficient than `edit` because only the changed text appears in the tool call.

### Gating agent skill writes (`skills.write_approval`)

By default the agent writes skills freely — including from the background self-improvement review that runs after a turn. To approve every skill write first (small models that misjudge what they learned, secure environments, or just wanting eyes on the self-improvement loop), turn on the write-approval gate:

```yaml
skills:
  write_approval: false     # false = write freely (default) | true = require approval
```

When `write_approval: true`, every `skill_manage` write (create / edit / patch / delete / write_file / remove_file) is **staged** instead of committed — a SKILL.md is too large to review inline, so staging applies regardless of whether the write came from a foreground turn or the background review. Staged writes survive restarts under `~/.hermes/pending/skills/` and are reviewed with the same approve/deny flow as dangerous commands:

```
/skills pending             # list staged skill writes + a one-line gist each
/skills diff <id>           # full unified diff (best viewed in CLI or dashboard)
/skills approve <id>        # apply it (or 'all')
/skills reject <id>         # drop it (or 'all')
/skills approval on         # turn the gate on (or 'off') and persist it
```

The review surface works in the interactive CLI and on messaging platforms (diff output is truncated for chat bubbles — read the full diff on the CLI or in the pending JSON file). Memory writes have the same gate under `memory.write_approval` (see `hermes_persistent_memory`). The separate `skills.guard_agent_created` setting is a content scanner (dangerous-pattern heuristics), not an approval gate — the two are independent (config detail → SP02).

## Skills Hub

Browse, search, install, and manage skills from online registries, `skills.sh`, direct well-known skill endpoints, and official optional skills.

### Common commands

```bash
hermes skills browse                              # Browse all hub skills (official first)
hermes skills search kubernetes                   # Search all sources
hermes skills inspect openai/skills/k8s           # Preview before installing
hermes skills install openai/skills/k8s           # Install with security scan
hermes skills install official/security/1password
hermes skills install https://sharethis.chat/SKILL.md              # Direct URL (single-file SKILL.md)
hermes skills list --source hub                   # List hub-installed skills
hermes skills check                               # Check installed hub skills for upstream updates
hermes skills update                              # Reinstall hub skills with upstream changes when needed
hermes skills audit                               # Re-scan all hub skills for security
hermes skills uninstall k8s                       # Remove a hub skill
hermes skills reset google-workspace              # Un-stick a bundled skill from "user-modified" (see below)
hermes skills publish skills/my-skill --to github --repo owner/repo
hermes skills tap add myorg/skills-repo           # Add a custom GitHub source
```

### Supported hub sources

Hermes integrates nine skills ecosystems / discovery sources:

| Source | Example | Notes |
|--------|---------|-------|
| `official` | `official/security/1password` | Optional skills shipped with Hermes; maintained in the repo (`optional-skills/`), install with built-in trust. |
| `skills-sh` | `skills-sh/vercel-labs/agent-skills/...` | Vercel's public skills directory; searchable, resolves alias-style slugs, installs from the underlying source repo. |
| `well-known` | `well-known:https://mintlify.com/docs/.well-known/skills/mintlify` | URL-based discovery from sites that publish `/.well-known/skills/index.json` — a web convention, not a centralized hub. |
| `github` | `openai/skills/k8s` | Direct GitHub repo/path installs and custom taps; default browsable taps include openai/anthropics/huggingface/NVIDIA/garrytan skills. |
| `clawhub` | source-specific | Third-party skills marketplace integrated as a community source. |
| `claude-marketplace` | `anthropics/skills`, `aiskillstore/marketplace` | Repos publishing Claude-compatible plugin/marketplace manifests. |
| `lobehub` | source-specific | Search/convert LobeHub public-catalog agent entries into installable Hermes skills. |
| `browse-sh` | `browse-sh/airbnb.com/search-listings-ddgioa` | Browserbase catalog of 200+ site-specific browser-automation SKILL.md files; identifiers `browse-sh/<hostname>/<task-id>`; trust `community`. |
| `url` | `https://sharethis.chat/SKILL.md` | Direct HTTP(S) URL to a single-file SKILL.md; name resolves frontmatter → URL slug → interactive prompt → `--name`; trust `community`. |

A GitHub tap may ship a `skills.sh.json` at its repo root; its `groupings` (each a `title` + skill-name list) are read at index time and become the category labels shown in the Skills Hub page — generic, no Hermes-side changes required.

### Security scanning and `--force`

All hub-installed skills go through a **security scanner** that checks for data exfiltration, prompt injection, destructive commands, supply-chain signals, and other threats. `hermes skills inspect ...` also surfaces upstream metadata (repo URL, skills.sh detail page, install command, weekly installs, upstream audit statuses, well-known endpoints).

Use `--force` when you have reviewed a third-party skill and want to override a non-dangerous policy block — e.g. `hermes skills install skills-sh/anthropics/skills/pdf --force`.

Important behavior:
- `--force` can override policy blocks for caution/warn-style findings.
- `--force` does **not** override a `dangerous` scan verdict.
- Official optional skills (`official/...`) are treated as built-in trust and do not show the third-party warning panel.

### Trust levels

| Level | Source | Policy |
|-------|--------|--------|
| `builtin` | Ships with Hermes | Always trusted |
| `official` | `optional-skills/` in the repo | Built-in trust, no third-party warning |
| `trusted` | Trusted registries/repos such as `openai/skills`, `anthropics/skills`, `huggingface/skills`, `NVIDIA/skills` | More permissive policy than community sources |
| `community` | Everything else (`skills.sh`, well-known endpoints, custom GitHub repos, most marketplaces) | Non-dangerous findings can be overridden with `--force`; `dangerous` verdicts stay blocked |

### Update lifecycle

The hub tracks enough provenance to re-check upstream copies of installed skills, using the stored source identifier plus the current upstream bundle content hash to detect drift:

```bash
hermes skills check          # Report which installed hub skills changed upstream
hermes skills update         # Reinstall only the skills with updates available
hermes skills update react   # Update one specific installed hub skill
```

GitHub-backed operations use the GitHub API (60 requests/hour unauthenticated); set `GITHUB_TOKEN` in `.env` to raise the limit to 5,000 requests/hour.

### Publishing a custom skill tap

To share a curated set of skills — for a team, an org, or publicly — publish them as a **tap**: a GitHub repository other Hermes users add with `hermes skills tap add <owner/repo>`. No server, no registry sign-up, no release pipeline — just a directory of SKILL.md files. A tap is any GitHub repo (public, or private with `GITHUB_TOKEN`):

- Each skill lives in its own directory under the tap's root path (default `skills/`); the directory name becomes the skill's install slug.
- Each skill directory must contain a `SKILL.md` with standard frontmatter; `references/`, `templates/`, `scripts/`, `assets/` subdirs download alongside it at install time.
- Directories starting with `.` or `_` are ignored. Hermes discovers skills by listing every subdirectory of the tap path and probing each for `SKILL.md`.

After pushing a tap to GitHub, any Hermes user subscribes and installs from it: `hermes skills tap add my-org/hermes-skills`, then `hermes skills search deploy`, then `hermes skills install my-org/hermes-skills/deploy-runbook`.

**Non-default paths** — if skills don't live under `skills/`, edit the tap entry in `~/.hermes/.hub/taps.json` (the `tap add` CLI defaults new taps to `path: "skills/"`; `tap list` shows the effective path):

```json
{
  "taps": [
    {"repo": "my-org/platform-docs", "path": "internal/skills/"}
  ]
}
```

**Individual installs (without adding a tap)** — install a single skill from any public GitHub repo directly: `hermes skills install owner/repo/skills/my-workflow`. **Trust for taps** — new taps default to `community` trust; for higher trust, add the repo to `TRUSTED_REPOS` in `tools/skills_hub.py` (a Hermes core PR). Taps are stored in `~/.hermes/.hub/taps.json` (created on demand); `tap list` / `tap add` / `tap remove` work both as CLI and `/skills tap ...` slash commands.

## Bundled skill updates (`hermes skills reset`)

Hermes ships bundled skills in `skills/` inside the repo. On install and on every `hermes update`, a sync pass copies those into `~/.hermes/skills/` and records a manifest at `~/.hermes/skills/.bundled_manifest` mapping each skill name to the content hash at the time it was synced (the **origin hash**). On each sync, Hermes recomputes the hash of the local copy and compares it to the origin hash:

- **Unchanged** → safe to pull upstream changes, copy the new bundled version in, record the new origin hash.
- **Changed** → treated as **user-modified** and skipped forever, so edits are never stomped.

The sharp edge: if you edit a bundled skill, then later abandon your changes and copy-paste the bundled version back, the manifest still holds the *old* origin hash, so your fresh copy (current bundled hash) won't match it and sync keeps flagging the skill as user-modified. `hermes skills reset` is the escape hatch:

```bash
# Safe: clears the manifest entry for this skill. Your current copy is preserved,
# but the next sync re-baselines against it so future updates work normally.
hermes skills reset google-workspace

# Full restore: also deletes your local copy and re-copies the current bundled
# version. Use this when you want the pristine upstream skill back.
hermes skills reset google-workspace --restore

# Non-interactive (e.g. in scripts or TUI mode) — skip the --restore confirmation.
hermes skills reset google-workspace --restore --yes
```

The same command works in chat as a slash command (`/skills reset google-workspace`, optionally `--restore`). Each profile has its own `.bundled_manifest` under its own `HERMES_HOME`, so `hermes -p coder skills reset <name>` only affects that profile.

## Slash commands (inside chat)

All the same hub commands work with the `/skills` prefix inside a chat session — e.g. `/skills browse`, `/skills search react --source skills-sh`, `/skills inspect skills-sh/vercel-labs/json-render/json-render-react`, `/skills install openai/skills/skill-creator --force`, `/skills check`, `/skills update`, `/skills reset google-workspace`, and `/skills list`. Official optional skills still use identifiers like `official/security/1password` and `official/migration/openclaw-migration`.

**Source**: `inbox/hermes_agent_docs/user-guide/features/skills.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
**Last Updated**: 2026-06-19
**Status**: Active
