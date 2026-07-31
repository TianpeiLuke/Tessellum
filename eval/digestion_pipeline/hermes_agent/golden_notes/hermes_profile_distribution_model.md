---
tags:
  - resource
  - documentation
  - hermes_agent
  - profiles
  - security
keywords:
  - distribution-owned vs user-owned
  - never-shipped paths
  - unsigned distribution trust
  - distribution_owned manifest override
  - force-config reset
  - reserved profile names
topics:
  - Hermes Agent
  - Profile Distributions
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
access_control_group: ["general"]
---

# Hermes Agent — Profile Distribution Data & Trust Model

## Overview

This is the **data-ownership and trust model** behind a Hermes profile distribution — the rules that decide what a `hermes profile update` may overwrite, what it must never touch, and how much you implicitly trust an installed agent. A distribution is a git repo packaging an agent (SOUL/config/skills/cron/MCP), but installing and updating one is governed by a three-way path partition: **distribution-owned** paths (replaced from the new clone), a **config override** carve-out (`config.yaml`, preserved by default so your local tuning survives), and **user-owned** paths (memories, sessions, credentials — never touched). Layered on top is a **hard-excluded never-shipped invariant**: a regression-tested set of paths the installer strips even if an author accidentally commits them, so secrets and conversation data can never travel inside a distribution. Trust is **unsigned by default** — you trust the git host and the author — which makes the model deliberately conservative: cron jobs are not auto-scheduled, while SOUL and skills go active on first chat. This note documents that partition, the never-shipped list, the trust boundary, and the under-the-hood internals; for the step-by-step author→install→update workflow see the sibling lifecycle note.

## Distribution-owned vs user-owned

When an installer updates to a new version, some things get replaced (the author's domain) and some stay put (the installer's domain). The defaults partition every path into one of three categories:

| Category | Paths | On update |
|---|---|---|
| **Distribution-owned** | `SOUL.md`, `config.yaml`, `mcp.json`, `skills/`, `cron/`, `distribution.yaml` | Replaced from the new clone |
| **Config override** | `config.yaml` | Actually preserved by default — the installer may have tuned model or provider. Pass `--force-config` on update to reset. |
| **User-owned** | `memories/`, `sessions/`, `state.db*`, `auth.json`, `.env`, `logs/`, `workspace/`, `plans/`, `home/`, `*_cache/`, `local/` | Never touched |

The key subtlety is that `config.yaml` appears in two rows: it is nominally distribution-owned, but the **config override** carve-out preserves it on update by default, because the installer may have tuned the model, temperature, or provider. `--force-config` opts back into overwriting it. Everything in the user-owned row is idempotently preserved across every update — your conversation history, credentials, and scratch data are invariant under the update operation.

An author can override which paths count as distribution-owned via the manifest:

```yaml
distribution_owned:
  - SOUL.md
  - skills/research/            # only my research skills; other installed skills stay
  - cron/digest.json
```

When `distribution_owned` is omitted, the defaults above apply — which is what most distributions want. Narrowing the list lets an author ship only a subset (e.g. their research skills) while leaving the installer's other hand-added skills in place across updates.

## What's NOT in a distribution (ever)

The installer **hard-excludes** these paths even if an author accidentally ships them. No config option lets you override this — the safety guard is a regression-tested invariant:

- `auth.json` — OAuth tokens, platform credentials
- `.env` — API keys, secrets
- `memories/` — conversation memory
- `sessions/` — conversation history
- `state.db`, `state.db-shm`, `state.db-wal` — session metadata
- `logs/` — agent and error logs
- `workspace/` — generated working files
- `plans/` — scratch plans
- `home/` — user's home mount in Docker backends
- `*_cache/` — image / audio / document caches
- `local/` — user-reserved customization namespace

When you clone a distribution, these simply aren't there. When you update, they stay put. If you installed the same distribution on five machines, you have five isolated sets of this data — one per machine. This invariant is what makes the user-owned partition above safe: even an author who carelessly `git add`s their `.env` cannot leak it, because the installer drops these paths at clone time regardless of the manifest.

## Security and trust

Profile distributions are **unsigned by default**. You're trusting:

- **The git host** (GitHub / GitLab / wherever) to serve the bytes the author pushed.
- **The author** to not ship a malicious SOUL, skills, or cron jobs.

The trust posture is therefore conservative about *when* shipped content activates. Cron jobs from a distribution are **not auto-scheduled** — the installer prints `hermes -p <name> cron list` and you enable them explicitly. By contrast, `SOUL.md` and skills ARE active as soon as you start chatting with the profile, so read them before your first run if you're installing from someone you don't know.

The source frames the threat as analogous to installing a browser extension or a VS Code extension: low friction, high power, trust the source. For internal company distributions, use a private repo and your normal git auth — nothing new to configure. Future versions may add signing, a lockfile (`.distribution-lock.yaml`) with a resolved commit SHA, and a `--dry-run` flag that prints the diff before applying an update; none of those are shipping yet.

## Under the hood

For implementation details, precise CLI behavior, and all flags, the source points to the Profile Commands reference (distribution commands). The short version, as documented:

- `install`, `update`, `info` live inside `hermes profile` — not a parallel command tree.
- The manifest format is YAML with a tiny required schema (`name` only).
- The installer uses your local `git` binary for cloning, so any auth your shell already handles (SSH keys, credential helpers) works transparently.
- After clone, `.git/` is **stripped** — the installed profile isn't itself a git checkout, avoiding "oh my, I accidentally committed my `.env` to the distribution's git history" traps.
- Reserved profile names (`hermes`, `test`, `tmp`, `root`, `sudo`) are **rejected at install time** to avoid collisions with common binaries.

Stripping `.git/` also reinforces the never-shipped invariant from the other direction: because the installed profile has no git history, a later `git add` from inside the profile directory cannot accidentally re-publish excluded state.

## See also (source)

The source closes by pointing to the base concept ([Profiles: Running Multiple Agents](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)), the full [Profile Commands reference](https://hermes-agent.nousresearch.com/docs/reference/profile-commands), the distinct local-backup `hermes profile export` / `import` flow, and the SOUL/personality authoring guides — all captured as link-outs in the Related Notes below rather than duplicated here.

**Source**: `inbox/hermes_agent_docs/user-guide/profile-distributions.md` · https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
**Last Updated**: 2026-06-19
**Status**: Active
