---
tags:
  - resource
  - documentation
  - hermes_agent
  - kanban
  - multi_agent
keywords:
  - hermes kanban dashboard
  - kanban CLI command reference
  - kanban slash command
  - bundled dashboard plugin
  - auto manual orchestration
  - REST WebSocket task_events
topics:
  - Hermes Agent
  - Kanban
  - Multi-Agent Coordination
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
access_control_group: ["general"]
---

# Hermes Kanban — Dashboard, CLI & Slash Command

## Overview

This note is the operator's reference for the three **human/automation surfaces** over the Hermes Kanban board: the bundled web **dashboard plugin**, the `hermes kanban …` **CLI verb set**, and the `/kanban …` **slash command**. All three are distinct from the model-facing `kanban_*` tool surface workers use, but every surface routes through the same `kanban_db` layer over `~/.hermes/kanban.db`, so reads stay consistent and writes can't drift. Use this note when you (a human), a script, or cron needs to set up a board, watch it, create or move tasks, decompose triage ideas, or drive the board from a messaging chat. The board data model these surfaces operate on (tasks/links/runs/events/boards) is in [hermes_kanban_multi_agent_board](hermes_kanban_multi_agent_board.md); the worker/orchestrator tool lifecycle is in [hermes_kanban_worker_orchestrator](hermes_kanban_worker_orchestrator.md).

## Dashboard (GUI)

The `/kanban` CLI and slash command are enough to run the board headlessly, but a visual board is often the right interface for humans-in-the-loop. Hermes ships the dashboard as a **bundled dashboard plugin** at `plugins/kanban/` — not a core feature, not a separate service — following the dashboard-plugin contract (see [hermes_built_in_plugins](hermes_built_in_plugins.md) and the Extending the Dashboard guide). Open it with:

```bash
hermes kanban init      # one-time: create kanban.db if not already present
hermes dashboard        # "Kanban" tab appears in the nav, after "Skills"
```

### What the plugin gives you

- A **Kanban** tab with one column per status (`triage`, `todo`, `ready`, `running`, `blocked`, `done`, plus `archived` when toggled on). `triage` is the parking column for rough ideas; by default (`kanban.auto_decompose: true`) the dispatcher auto-runs the decomposer on tasks landing there.
- Cards show task id, title, priority badge, tenant tag, assigned profile, comment/link counts, a **progress pill** (`N/M` children done), and "created N ago"; a per-card checkbox enables multi-select.
- **Per-profile lanes inside Running** (toolbar toggle), **live updates via WebSocket** (tails the append-only `task_events` table; reloads debounced), **drag-drop** between columns (a `PATCH /api/plugins/kanban/tasks/:id` routing through the same `kanban_db` code, with confirmation on destructive moves and a touch fallback), **inline create** (`+` on a column header), and **multi-select with bulk actions** (batch status transitions, archive, reassign; per-id failures reported without aborting).
- **Click a card** opens a side drawer with editable title/assignee/priority/description (XSS-safe markdown renderer), a dependency editor (server-side cycle rejection), a status action row, a result section, the comment thread (Enter-to-submit), and the last 20 events.
- **Toolbar filters** — free-text search, tenant dropdown (defaults to `dashboard.kanban.default_tenant`), assignee dropdown, "show archived", "lanes by profile", and a **Nudge dispatcher** button to skip the 60 s tick. The plugin reads only theme CSS vars, so it reskins with the active dashboard theme.

### Auto vs Manual orchestration

Two ways to handle a task dropped into Triage. **Auto (default, `kanban.auto_decompose: true`)** — the gateway-embedded dispatcher runs the decomposer each tick (capped by `kanban.auto_decompose_per_tick`, default 3, so a bulk load doesn't burst-spend the auxiliary LLM); it uses `auxiliary.kanban_decomposer`, reads installed profiles + descriptions, and produces a JSON task graph. The triage task becomes parent of every leaf and promotes back to `ready` so its assignee (`kanban.orchestrator_profile`, or the active default) judges completion. **Manual (`auto_decompose: false`)** — triage tasks stay put until you click **⚗ Decompose**, run `hermes kanban decompose <id>` (or `--all`), or use `/kanban decompose <id>`. Flip modes from the **Orchestration: Auto/Manual** pill or by editing `config.yaml`; both coexist with `hermes kanban specify` (single-task spec rewrite). The config knobs under `kanban:`:

| Key | Default | Purpose |
|---|---|---|
| `auto_decompose` | `true` | Dispatcher auto-runs the decomposer every tick. |
| `auto_decompose_per_tick` | `3` | Cap on decompositions per dispatcher tick; excess defers. |
| `orchestrator_profile` | `""` | Profile assigned to the root/orchestration task after fan-out. Empty = active default. |
| `default_assignee` | `""` | Where a child lands when the LLM picks an unknown profile. Empty = active default. |
| `auto_subscribe_on_create` | `true` | Auto-subscribe the originating session to a `kanban_create`d task's completion/block events. |

Two auxiliary LLM slots back this: `auxiliary.kanban_decomposer` (produces the task graph) and `auxiliary.profile_describer` (auto-generates profile descriptions for routing). The decomposer NEVER lands a child with `assignee=None`: unknown picks route to `kanban.default_assignee`.

### Architecture and REST surface

The GUI is strictly a **read-through-the-DB + write-through-`kanban_db`** layer with no domain logic of its own — a React SPA over a FastAPI router (`plugins/kanban/dashboard/plugin_api.py`) over the shared WAL-mode `~/.hermes/kanban.db`, with a WebSocket tailing `task_events`. All routes mount under `/api/plugins/kanban/`, protected by the dashboard's ephemeral session token:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/board?tenant=…&include_archived=…` | Full board grouped by status column, plus tenants + assignees for filters |
| `GET` / `PATCH` / `POST` | `/tasks/:id`, `/tasks`, `/tasks/bulk` | Read task+comments+events+links; create; per-field patch; bulk patch |
| `POST` | `/tasks/:id/specify`, `/tasks/:id/decompose` | Triage specifier / decomposer (200-on-LLM-error convention) |
| `GET`/`PATCH`/`POST` | `/profiles`, `/profiles/:name`, `/profiles/:name/describe-auto` | List profiles + descriptions; set/clear; auto-generate via `profile_describer` |
| `GET` / `PUT` | `/orchestration` | Read/update `orchestrator_profile`, `default_assignee`, `auto_decompose` (validates profiles exist) |
| `POST` / `DELETE` | `/links` | Add / remove a `parent_id → child_id` dependency |
| `POST` | `/dispatch?max=…&dry_run=…` | Nudge the dispatcher — skip the 60 s wait |
| `GET` | `/config` | Read `dashboard.kanban` preferences |
| `WS` | `/events?since=<event_id>` | Live stream of `task_events` rows |

Every handler is a thin wrapper — the plugin is ~700 lines of Python (router + WebSocket tail + bulk batcher + config reader) and adds no business logic; a `_conn()` helper auto-initializes `kanban.db` on every read/write.

### Dashboard config, security, live updates, extending, scope

Keys under `dashboard.kanban` in `~/.hermes/config.yaml` change the tab's defaults (read at load via `GET /config`):

```yaml
dashboard:
  kanban:
    default_tenant: acme              # preselects the tenant filter
    lane_by_profile: true             # default for the "lanes by profile" toggle
    include_archived_by_default: false
    render_markdown: true             # set false for plain <pre> rendering
```

**Security model.** The dashboard's HTTP auth middleware explicitly skips `/api/plugins/` — plugin routes are unauthenticated by design because the dashboard binds to localhost by default, so the kanban REST surface is reachable from any process on the host. The WebSocket additionally requires the ephemeral session token as a `?token=…` query parameter. Running `hermes dashboard --host 0.0.0.0` exposes every plugin route to the network — **"Don't do that on a shared host."** Tasks in `kanban.db` are profile-agnostic on purpose: `hermes -p <profile> dashboard` still shows tasks from any other profile on the host.

**Live updates.** `task_events` is an append-only table with a monotonic `id`; the WebSocket holds each client's last-seen id and pushes new rows. Bursts trigger a single cheap board refetch; WAL mode means the read loop never blocks the dispatcher's `BEGIN IMMEDIATE` claim transactions.

**Extending / scope.** The plugin uses the standard Hermes dashboard plugin contract (manifest, shell slots, page-scoped slots, Plugin SDK) — extra columns, custom card chrome, or `tab.override` replacements are expressible without forking. Disable without removing via `dashboard.plugins.kanban.enabled: false` (or delete `plugins/kanban/dashboard/manifest.json`). The GUI is deliberately thin: everything it does is reachable from the CLI; auto-assignment, budgets, governance gates, and org-chart views stay user-space.

## CLI command reference

This is the surface you (or scripts, cron, the dashboard) use to drive the board. Workers running inside the dispatcher use the `kanban_*` tool surface for the same operations — both route through `kanban_db`, so the surfaces agree by construction.

```
hermes kanban init                                     # create kanban.db + print daemon hint
hermes kanban create "<title>" [--body ...] [--assignee <profile>]
                                [--parent <id>]... [--tenant <name>]
                                [--workspace scratch|worktree|worktree:<path>|dir:<path>]
                                [--branch <name>] [--priority N] [--triage]
                                [--idempotency-key KEY] [--max-runtime 30m|2h|1d|<seconds>]
                                [--max-retries N] [--goal] [--goal-max-turns N]
                                [--skill <name>]... [--json]
hermes kanban list [--mine] [--assignee P] [--status S] [--tenant T] [--archived] [--json]
hermes kanban show <id> [--json]
hermes kanban assign <id> <profile>                    # or 'none' to unassign
hermes kanban reassign <id>... <profile>               # bulk re-assign
hermes kanban edit <id> [--title ...] [--body ...] [--priority N]
hermes kanban promote <id>...                          # move todo/blocked tasks to ready (recovery)
hermes kanban schedule <id> --at <ISO8601>             # set/clear scheduled_at start time
hermes kanban diagnostics [--json]                     # board health snapshot (alias: diag)
hermes kanban link <parent_id> <child_id>
hermes kanban unlink <parent_id> <child_id>
hermes kanban complete <id>... [--result "..."]        # bulk verb
hermes kanban block <id> "<reason>" [--ids <id>...]    # bulk verb
hermes kanban unblock <id>...                          # bulk verb
hermes kanban archive <id>...                          # bulk verb
hermes kanban watch [--assignee P] [--tenant T] [--kinds completed,blocked,…] [--interval SECS]
hermes kanban runs <id> [--json]                       # attempt history (one row per run)
hermes kanban specify [<id> | --all] [--tenant T]      # flesh out a triage idea into a full spec
hermes kanban swarm "<goal>" --workers a,b,c --verifier r --synthesizer w
hermes kanban gc [--event-retention-days N] [--log-retention-days N]
```

`--max-retries` is a per-task circuit-breaker override: `--max-retries 1` blocks on the first non-successful attempt, `--max-retries 3` allows two retries and blocks on the third; omit it to use `kanban.failure_limit`.

### Concurrency, scheduling, and respawn-guard config

| Config key | Default | What it does |
|---|---|---|
| `kanban.max_in_progress` | unset (unlimited) | Caps simultaneously running tasks; below-1 values warn and behave as unlimited. |
| `kanban.max_in_progress_per_profile` | unset (unlimited) | Per-profile cap; applies alongside `max_in_progress` (both must allow a spawn). |
| `kanban.auto_promote_children` | `true` | Auto-promotes decomposed children with no parent-blocker to `ready`. |
| `kanban.default_workdir` | unset | Board-level default working dir; per-task `workspace:` still wins. |

**Scheduled starts.** Set `scheduled_at` (`--scheduled-at "2026-06-01T03:00:00Z"`) to delay dispatch; the dispatcher skips future-dated ready tasks and picks them up on the first tick after that timestamp. **Respawn guard.** The dispatcher refuses to re-spawn a ready task that hit a quota/auth/429 error (`blocker_auth`), completed within the guard window (`recent_success`), or whose recent comment links a GitHub PR (`active_pr`) — preventing repeat storms.

### Drag-to-delete and worker-visibility endpoints (dashboard)

The dashboard exposes a **trash drop zone** — drag a card in to delete the task (cascades through `task_events`, child links, subscriptions; confirmation-protected). Bulk delete via `DELETE /api/plugins/kanban/tasks` with `{"ids": [...]}`. Read-only monitor endpoints (same plugin auth): `GET /workers/active` (spawned workers with PID, profile, task id, heartbeat), `GET /runs/{id}` (single-run detail), `POST /runs/{run_id}/terminate` (stop a reclaimable run), and `GET /inspect` (combined dispatcher snapshot — backlog, in-progress vs `max_in_progress`, recent events). The **Kanban Swarm v1** helper (`hermes kanban swarm`) creates a graph in one shot: a completed blackboard root, N parallel workers, a verifier gated on all workers, and a synthesizer gated on the verifier.

## `/kanban` slash command

Every `hermes kanban <action>` verb is also reachable as `/kanban <action>` — from inside an interactive `hermes chat` session and from any gateway platform (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, email, SMS). Both surfaces call the same `hermes_cli.kanban.run_slash()` entry point that reuses the `hermes kanban` argparse tree, so flags and output format are identical across CLI, `/kanban`, and `hermes kanban`. Quote multi-word arguments as on a shell — `run_slash` parses with `shlex.split`.

```
/kanban list
/kanban show t_abcd
/kanban create "write launch post" --assignee writer --parent t_research
/kanban comment t_abcd "looks good, ship it"
/kanban unblock t_abcd
/kanban specify --all --tenant engineering
```

**Mid-run usage.** The gateway normally queues slash commands while an agent is thinking; **`/kanban` is explicitly exempted from this guard** because the board lives in `~/.hermes/kanban.db`, not in the running agent's state — reads and writes go through immediately, even mid-turn (e.g. `/kanban unblock t_abcd` from your phone, or `/kanban comment` to leave human context the next run reads in `kanban_show()`). **Auto-subscribe (gateway only).** Creating a task with `/kanban create "…"` auto-subscribes the originating chat (platform + chat id + thread id) to that task's terminal events (`completed`, `blocked`, `gave_up`, `crashed`, `timed_out`) — one message back per event, including the first line of the worker's result on `completed`. Subscriptions auto-remove on `done`/`archived`; scripted `--json` creates skip it. **Output truncation.** `/kanban list`/`show`/`tail` over ~3800 chars are truncated with a "use `hermes kanban …` in your terminal" footer (the CLI has no cap). **Autocomplete.** Typing `/kanban ` + Tab cycles a built-in subcommand list; the remaining verbs work but aren't in the hint list yet.

**Source**: `inbox/hermes_agent_docs/user-guide/features/kanban.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
**Last Updated**: 2026-06-19
**Status**: Active
