---
tags:
  - resource
  - documentation
  - hermes_agent
  - skill_curator
  - agent_maintenance
keywords:
  - skill curator
  - agent-created skills
  - usage telemetry
  - stale archived lifecycle
  - aux-model consolidation
  - backups and rollback
topics:
  - Hermes Agent
  - Skills
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
access_control_group: ["general"]
---

# Hermes Agent — Skill Curator

## Overview

The curator is a **background maintenance pass for agent-created skills**. It tracks how often each skill is viewed, used, and patched in a `.usage.json` sidecar, moves long-unused skills through an `active → stale → archived` lifecycle, and periodically spawns a short auxiliary-model review that proposes consolidations or patches drift. It exists so that skills produced by the [self-improvement loop](hermes_skills_hub_agent_managed.md) (every time the agent solves a novel problem and saves a skill into `~/.hermes/skills/`) do not pile up into dozens of narrow near-duplicates that pollute the catalog and waste tokens. The curator **never auto-deletes** — the worst outcome is archival into a recoverable `.archive/` directory, and every real pass is preceded by a tar.gz snapshot.

## How It Runs

The curator is triggered by an **inactivity check, not a cron daemon**. On CLI session start, and on a recurring tick inside the gateway's cron-ticker thread, Hermes checks whether (1) enough time has passed since the last run (`interval_hours`, default **7 days**) and (2) the agent has been idle long enough (`min_idle_hours`, default **2 hours**). If both are true, it spawns a **background fork of `AIAgent`** — the same pattern used by the memory/skill self-improvement nudges — running in its own prompt cache, never touching the active conversation.

On a brand-new install (or the first tick of a pre-curator install after `hermes update`), the curator **does not run immediately**: the first observation seeds `last_run_at` to "now" and defers the first real pass by one full `interval_hours`, giving you an interval to review, pin, or opt out. `hermes curator run --dry-run` previews what a run would do without mutating the library.

A run has **two phases**:

1. **Automatic transitions** (deterministic, no LLM). Skills unused for `stale_after_days` (30) become `stale`; skills unused for `archive_after_days` (90) move to `~/.hermes/skills/.archive/`. This always-on pruning runs whenever the curator is enabled, with no aux-model cost.
2. **LLM consolidation** (single aux-model pass, `max_iterations=8`) — **OFF by default**. When `curator.consolidate: true`, the forked agent surveys agent-created skills, can read any with `skill_view`, and decides per-skill whether to keep, patch (via `skill_manage`), consolidate overlapping skills into class-level umbrellas, or archive. Consolidation treats a skill as a full package: if it has `references/`, `templates/`, `scripts/`, `assets/`, or relative links, the curator must keep it standalone, re-home support files and rewrite paths, or archive the whole package — never flatten only `SKILL.md` into another skill's `references/`.

By default the curator only **prunes**; the opinionated LLM consolidation pass is opt-in because it costs aux-model tokens on every run. Pinned skills are off-limits to both the auto-transitions and the agent's own `skill_manage` tool.

## Configuration

All settings live in `config.yaml` under `curator:` (not `.env` — not a secret). Defaults:

```yaml
curator:
  enabled: true
  interval_hours: 168          # 7 days
  min_idle_hours: 2
  stale_after_days: 30
  archive_after_days: 90
  consolidate: false           # LLM umbrella-building pass — opt-in (prune-only by default)
  prune_builtins: true         # archive unused bundled built-in skills too (hub skills always exempt)
```

To disable entirely, set `curator.enabled: false`. To keep always-on pruning but opt into LLM consolidation, set `curator.consolidate: true`. By default (`prune_builtins: true`) the curator can also archive **unused bundled built-in skills** after `archive_after_days` of non-use; hub-installed skills (from agentskills.io) are always off-limits. Set `curator.prune_builtins: false` to restore agent-created-only behavior.

### Running the Review on a Cheaper Aux Model

The LLM review pass is a regular auxiliary task slot — `auxiliary.curator` — alongside Vision, Compression, Session Search, etc. "Auto" means "use my main chat model"; override the slot to pin a specific provider + model for the review pass:

```yaml
auxiliary:
  curator:
    provider: openrouter
    model: google/gemini-3-flash-preview
    timeout: 600               # generous — reviews can take several minutes
```

The same picker is available via `hermes model` ("Auxiliary models — side-task routing" → "Curator") and in the web dashboard's Models tab. Leaving `provider: auto` routes the review through the main chat model. (Earlier releases used a one-off `curator.auxiliary.{provider,model}` block; that path still works but emits a deprecation log line — migrate to `auxiliary.curator` so the curator shares the same plumbing as every other aux task.)

## CLI

```bash
hermes curator status         # last run, counts, pinned list, LRU top 5
hermes curator run            # trigger a run now (blocks until done). Prune-only unless curator.consolidate: true
hermes curator run --consolidate # force the LLM consolidation pass on for this run, overriding the config default
hermes curator run --background  # fire-and-forget: start the run in a background thread
hermes curator run --dry-run  # preview only — report without any mutations
hermes curator backup         # take a manual snapshot of ~/.hermes/skills/
hermes curator rollback       # restore from the newest snapshot
hermes curator rollback --list     # list available snapshots
hermes curator rollback --id <ts>  # restore a specific snapshot
hermes curator rollback -y         # skip the confirmation prompt
hermes curator pause          # stop runs until resumed
hermes curator resume
hermes curator pin <skill>    # never auto-transition this skill
hermes curator unpin <skill>
hermes curator restore <skill>  # move an archived skill back to active
hermes curator list-archived    # list skills currently in ~/.hermes/skills/.archive/
hermes curator archive <skill>  # manually archive a single skill now
hermes curator prune [--days N] # bulk-archive agent-created skills idle >= N days (default 90)
```

The same subcommands are available as the `/curator` slash command inside a running session (CLI or gateway platforms).

## Backups and Rollback

Before every real curator pass, Hermes takes a tar.gz snapshot of `~/.hermes/skills/` at `~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz`. If a pass archives or consolidates something you didn't want touched, undo the whole run with one command — `hermes curator rollback` restores the newest snapshot (with confirmation), `rollback -y` skips the prompt, and `rollback --list` shows all snapshots with reason + size (see the CLI table above).

The rollback itself is reversible: before replacing the skills tree, Hermes takes another snapshot tagged `pre-rollback to <target-id>`, so a mistaken rollback can be undone by rolling forward with `--id`. Manual snapshots are taken any time with `hermes curator backup --reason "before-refactor"`; the `--reason` string lands in the snapshot's `manifest.json` and shows in `--list`. Snapshots are pruned to `curator.backup.keep` (default 5) to bound disk usage. Setting `curator.backup.enabled: false` disables automatic snapshotting; the flag gates both manual and pre-run paths symmetrically, so there is no way to accidentally skip the pre-run snapshot on mutating runs. `hermes curator status` also lists the five least-recently-used skills — a quick way to see what's likely to become stale next.

## What "Agent-Created" Means

The curator only manages skills explicitly marked as **agent-created** in `~/.hermes/skills/.usage.json`. A skill qualifies when ALL of the following are true: (1) its name is **not** in `~/.hermes/skills/.bundled_manifest` (bundled skills); (2) its name is **not** in `~/.hermes/skills/.hub/lock.json` (hub-installed skills); (3) its `.usage.json` entry has `"created_by": "agent"` or `"agent_created": true`.

Currently, only the **background self-improvement review fork** sets this marker — when it creates a new umbrella skill during its periodic review pass (~every 10 agent turns). The fork runs with a write origin of `"background_review"` (via `tools/skill_provenance.py`), the only path that triggers the `mark_agent_created()` call in `skill_manage`. Skills the **foreground** agent creates via `skill_manage(action="create")` during a conversation are **not** marked agent-created — they are user-directed and the curator leaves them alone. Hand-written `SKILL.md` files or external skill directories have `created_by: null` (or the field absent) and are also untouched. To see which skills the curator manages, run `hermes curator status`; if the agent-created count is 0, the LLM review is skipped.

Agent-created skills follow the full lifecycle: `active` → (30d unused) `stale` → (90d unused) `archived`; pinned skills bypass all auto-transitions; archives are recoverable via `hermes curator restore <name>`.

## Pinning a Skill

Pinning protects a skill from deletion — both the curator's automated archive passes and the agent's `skill_manage(action="delete")` tool call:

```bash
hermes curator pin <skill>
hermes curator unpin <skill>
```

Once pinned, the **curator** skips it during auto-transitions and the LLM review is instructed to leave it alone; the **agent's `skill_manage` tool** refuses `delete` on it (pointing the user at `hermes curator unpin`), while patches and edits still go through. The flag is stored as `"pinned": true` on the skill's `.usage.json` entry, so it survives sessions. Only **agent-created** skills can be pinned — `pin` refuses on bundled and hub-installed skills with an explanatory message.

A small set of **protected built-ins** is hardcoded as never-archivable and never-consolidatable, regardless of `curator.prune_builtins`, pin state, or LLM judgment — these back load-bearing UX (e.g., `plan` powers the `/plan` slash-command flow), so they are filtered out of the candidate list entirely. For a stronger guarantee than "no deletion" (freezing content while the agent still reads it), edit `~/.hermes/skills/<name>/SKILL.md` directly — the pin guards tool-driven deletion, not your own filesystem access.

## Usage Telemetry

The curator maintains a sidecar at `~/.hermes/skills/.usage.json` with one entry per skill:

```json
{
  "my-skill": {
    "use_count": 12,
    "view_count": 34,
    "last_used_at": "2026-04-24T18:12:03Z",
    "last_viewed_at": "2026-04-23T09:44:17Z",
    "patch_count": 3,
    "last_patched_at": "2026-04-20T22:01:55Z",
    "created_at": "2026-03-01T14:20:00Z",
    "state": "active",
    "pinned": false,
    "archived_at": null
  }
}
```

Counters increment when: `view_count` — the agent calls `skill_view` on the skill; `use_count` — the skill is loaded into a conversation's prompt; `patch_count` — `skill_manage patch/edit/write_file/remove_file` runs on the skill. Bundled and hub-installed skills are explicitly excluded from telemetry writes.

## Per-Run Reports

Every curator run writes a timestamped directory under `~/.hermes/logs/curator/`:

```
~/.hermes/logs/curator/
└── 20260429-111512/
    ├── run.json      # machine-readable: full fidelity, stats, LLM output
    └── REPORT.md     # human-readable summary
```

`REPORT.md` is a quick way to see what a run did — which skills transitioned, what the LLM reviewer said, which skills it patched — for auditing without grepping `agent.log`. When the curator has **no agent-created skills**, the LLM pass is skipped entirely and the report header shows `Model: (not resolved) via (not resolved)` with `Duration: 0s`; this is **not** a configuration error — there were simply no candidates. The auto-transition phase still runs and reports its counts normally.

If a run consolidated multiple skills under an umbrella (or merged near-duplicates), the user-visible end-of-run summary includes an explicit **rename map** showing every `old-name → new-name` pair, in addition to per-skill transition lines, and the hint surfaces under `hermes curator pin` so you can pin the umbrella name immediately.

## Restoring and Disabling

To restore an archived skill, `hermes curator restore <skill-name>` moves it from `~/.hermes/skills/.archive/` back to the active tree and resets its state to `active`; the restore refuses if a bundled or hub-installed skill has since been installed under the same name (would shadow upstream).

The curator is on by default. To turn it off **for one profile**, edit `~/.hermes/config.yaml` (or the active profile's config) and set `curator.enabled: false`. To pause **just one run**, `hermes curator pause` — the pause persists across sessions; use `resume` to re-enable. The curator also refuses to run if `min_idle_hours` hasn't elapsed, so on an active dev machine it naturally only runs during quiet stretches.

**Source**: `inbox/hermes_agent_docs/user-guide/features/curator.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
**Last Updated**: 2026-06-19
**Status**: Active
