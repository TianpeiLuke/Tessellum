---
title: Sub-Plan cl08 — OpenClaw Docs: CLI (tasks, transcripts, tui, uninstall, update, voicecall, webhooks)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/tasks", "cli/transcripts", "cli/tui", "cli/uninstall", "cli/update", "cli/voicecall", "cli/webhooks"]
status_history:
  - "pending → ready (xref-augment + 9/9 review sign-off, 2026-06-21)"
---

# Sub-Plan cl08: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*` prefix), format, dedup (term_dictionary + documentation/ +
> repo_openclaw*), 9-GATE validation, cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are all
> inherited from the master; this file re-measures its 7 pages and locks notes, coverage, splits, and candidate xrefs.

## Scope

The seventh CLI slice (`cl08`) covers the alphabetical tail of the `openclaw <command>` reference:
**tasks** (background task ledger + Task Flow state), **transcripts** (read-only stored-transcript inspector),
**tui** (Gateway-backed / local embedded terminal UI; aliases `chat`/`terminal`), **uninstall** (remove the
gateway service + local data), **update** (safe source/package update + channel switching + gateway auto-restart),
**voicecall** (voice-call plugin command surface), and **webhooks** (Gmail Pub/Sub setup + runner).

Priority **P1 (Phase A)** — the CLI is the conceptual/operational core; these commands are the day-to-day
operator surface for lifecycle (update/uninstall), observability (tasks/transcripts), interactive use (tui), and
two plugin/integration command surfaces (voicecall/webhooks). The code-side counterparts
(`repo_openclaw_cli_wizard`, `repo_openclaw_channels_voice_phone`, `repo_openclaw_gateway`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **5,722 measured words**. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| tasks | /cli/tasks | 433 | 8 | 4 | 7 | procedure |
| transcripts | /cli/transcripts | 608 | 6 | 5 | 0 | procedure |
| tui | /cli/tui | 583 | 3 | 4 | 0 | procedure |
| uninstall | /cli/uninstall | 174 | 1 | 1 | 0 | procedure |
| update | /cli/update | 2,094 | 3 | 9 | 3 | procedure (split: command surface vs internal update flow) |
| voicecall | /cli/voicecall | 1,178 | 6 | 6 | 12 | procedure |
| webhooks | /cli/webhooks | 652 | 3 | 5 | 6 | procedure |

Word total: 433 + 608 + 583 + 174 + 2,094 + 1,178 + 652 = **5,722**. Code-fence counts are `grep -c '```' / 2`.

## Content Strategy

- **Prioritize**: the `update` command surface + channel/restart semantics (the highest-traffic, most
  failure-prone lifecycle operation), and the `voicecall`/`webhooks` integration command tables (full flag/default
  reference operators copy verbatim). `tasks` (background-task ledger + Task Flow audit/maintenance) and
  `transcripts` (state-dir layout + read-only inspection) round out observability.
- **Split**: `update.md` (2,094w, 9 H2 / 3 H3) → (a) the operator command/option surface
  (Usage, Options, `update status`, `update repair`, `update wizard`, `--update` shorthand) and (b) the internal
  update mechanics (What it does, Control-plane response shape, Git checkout flow / channel selection / update
  steps). Each half is a distinct task cluster and keeps each note focused and ≤6 code blocks. All other pages =
  1 note each (none exceeds 2,500w or mixes BB).
- **Link-out (not duplicated)**: Background Tasks lifecycle (`/automation/tasks` → au01); voice-call plugin
  config (`/plugins/voice-call` → pl21); webhook/cron automation + Gmail Pub/Sub backend (`/automation/cron-jobs`,
  `/automation/webhook` → au01); package-manager updating + dev channels (`/install/updating`,
  `/install/development-channels`, `/install/uninstall` → in01/in05); TUI web guide (`/web/tui` → wb01);
  `doctor`/`config`/`gateway`/`status`/`backup` sibling CLI commands (cl01–cl07); Gateway logging
  (`/gateway/logging` → gw03). Vocabulary terms (`term_cron`, `term_webhook`, `term_pub_sub`, `term_oauth`,
  `term_tunneling`, `term_voice_call`) are LINKED, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_tasks.md` | procedure | tasks.md: Usage, Root Options (`--json`/`--runtime`/`--status`), Subcommands (list, show, notify, cancel, audit, maintenance, flow) | 420 | The `openclaw tasks` command: inspecting/auditing/cancelling durable background tasks and Task Flow state, runtime/status filters, the audit and reconciliation/cleanup `maintenance` pass, and `tasks flow` subcommands. |
| 2 | `oc_cli_transcripts.md` | procedure | transcripts.md: state-dir artifact layout, Commands (list/show/path + `--json`), Output, Many meetings per day, Missing summaries, Configuration | 480 | The read-only `openclaw transcripts` inspector: state-directory layout (`$OPENCLAW_STATE_DIR/transcripts/YYYY-MM-DD/<session>/`), list/show/path selectors, JSON output fields, per-day grouping, missing-summary causes, and opt-in `transcripts.enabled`/`autoStart` config. |
| 3 | `oc_cli_tui.md` | procedure | tui.md: Options table, aliases + Notes, Examples, Config repair loop | 480 | The `openclaw tui` terminal UI: Gateway-backed vs `--local` embedded modes, the full option table (url/token/password/session/deliver/thinking/timeout/history), `chat`/`terminal` aliases, SecretRef auth resolution, agent-workspace auto-select, and the local-mode config-repair loop. |
| 4 | `oc_cli_uninstall.md` | procedure | uninstall.md: options, examples, notes | 200 | The `openclaw uninstall` command: removing the gateway service, state/config, workspace, and macOS app (`--service`/`--state`/`--workspace`/`--app`/`--all`), the `--dry-run`/`--yes`/`--non-interactive` flags, and the `backup create`-first recommendation. |
| 5 | `oc_cli_update_commands.md` | procedure | update.md: Usage, Options, `update status`, `update repair`, `update wizard`, `--update` shorthand | 600 | The `openclaw update` operator surface: usage + options (`--channel`/`--tag`/`--dry-run`/`--no-restart`/`--json`/`--timeout`/`--yes`), the `status`/`repair`/`wizard` subcommands, downgrade/Nix guards, and the `--update` shorthand. |
| 6 | `oc_cli_update_flow.md` | procedure | update.md: What it does, Control-plane response shape, Git checkout flow (Channel selection, Update steps) | 620 | How `openclaw update` works internally: channel→install-method alignment (dev git checkout / stable+beta npm), the staged-npm install + managed-service handoff + restart-and-verify sequence, control-plane `update.run` response shapes, and the git-checkout 9-step flow with post-core plugin convergence. |
| 7 | `oc_cli_voicecall.md` | procedure | voicecall.md: Subcommands table, Setup and smoke, Call lifecycle (call/start/continue/speak/dtmf/end/status), Logs and metrics (tail/latency), Exposing webhooks (expose) | 640 | The `openclaw voicecall` plugin command surface: setup/smoke readiness checks, call lifecycle (call/start/continue/speak/dtmf/end/status) with flag tables, `tail`/`latency` log+metric inspection, and `expose` Tailscale serve/funnel toggling for the voice webhook. |
| 8 | `oc_cli_webhooks.md` | procedure | webhooks.md: Subcommands, `webhooks gmail setup` (Required, Pub/Sub, OpenClaw delivery, gog serve, Tailscale, Output), `webhooks gmail run`, End-to-end flow | 520 | The `openclaw webhooks` command: Gmail Pub/Sub integration via the bundled `gog` watcher — `gmail setup` (Pub/Sub topic/subscription, delivery, `gog watch serve` + Tailscale exposure flags) and `gmail run` (foreground serve + auto-renew loop), with their flag/default tables. |

## Section Coverage Map

```
tasks.md
├── Usage ───────────────────────────────────────── → note 1 (oc_cli_tasks)
├── Root Options (--json/--runtime/--status) ─────── → note 1
├── Subcommands → list/show/notify/cancel/audit/
│   maintenance/flow ─────────────────────────────── → note 1
└── Related (link-out: /cli, /automation/tasks) ──── → note 1 (References)
transcripts.md
├── (intro) state-dir artifact layout ────────────── → note 2 (oc_cli_transcripts)
├── Commands (list/show/path + --json) ───────────── → note 2
├── Output (tab-sep cols, list/show/path --json) ─── → note 2
├── Many meetings per day ────────────────────────── → note 2
├── Missing summaries ────────────────────────────── → note 2
└── Configuration (transcripts.enabled/autoStart) ── → note 2
tui.md
├── Options (flag table) ─────────────────────────── → note 3 (oc_cli_tui)
├── (aliases + Notes) ────────────────────────────── → note 3
├── Examples ─────────────────────────────────────── → note 3
├── Config repair loop ───────────────────────────── → note 3
└── Related (link-out: /cli, /web/tui, /tools/goal) → note 3 (References)
uninstall.md
├── (options + examples + notes) ─────────────────── → note 4 (oc_cli_uninstall)
└── Related (link-out: /cli, /install/uninstall) ─── → note 4 (References)
update.md
├── (intro: npm/pnpm/bun pointer) ────────────────── → note 5 (oc_cli_update_commands)
├── Usage ───────────────────────────────────────── → note 5
├── Options ─────────────────────────────────────── → note 5
├── update status ───────────────────────────────── → note 5
├── update repair ───────────────────────────────── → note 5
├── update wizard ───────────────────────────────── → note 5
├── --update shorthand ──────────────────────────── → note 5
├── What it does ────────────────────────────────── → note 6 (oc_cli_update_flow)
│   └── Control-plane response shape ────────────── → note 6
├── Git checkout flow ──────────────────────────── → note 6
│   ├── Channel selection ──────────────────────── → note 6
│   └── Update steps (9 <Step>s incl. plugin sync) ─── → note 6
└── Related (link-out: doctor, dev-channels, updating, /cli) → notes 5/6 (References)
voicecall.md
├── (intro: plugin-provided, Gateway-vs-standalone routing) → note 7 (oc_cli_voicecall)
├── Subcommands (table) ──────────────────────────── → note 7
├── Setup and smoke (setup, smoke) ───────────────── → note 7
├── Call lifecycle (call/start/continue/speak/
│   dtmf/end/status) ─────────────────────────────── → note 7
├── Logs and metrics (tail, latency) ─────────────── → note 7
├── Exposing webhooks (expose) ───────────────────── → note 7
└── Related (link-out: /cli, /plugins/voice-call) ── → note 7 (References)
webhooks.md
├── (intro: Gmail Pub/Sub + gog) ─────────────────── → note 8 (oc_cli_webhooks)
├── Subcommands ──────────────────────────────────── → note 8
├── webhooks gmail setup (Required, Pub/Sub,
│   OpenClaw delivery, gog serve, Tailscale, Output) → note 8
├── webhooks gmail run ───────────────────────────── → note 8
├── End-to-end flow (link-out: /automation/cron-jobs) → note 8
└── Related (link-out: /cli, /automation/webhook) ── → note 8 (References)
```
No orphaned sections. All `## Related` blocks map to each note's `## References` (external/link-out URLs).
Linked-out targets (`/automation/tasks`, `/plugins/voice-call`, `/automation/cron-jobs`, `/install/updating`,
`/web/tui`, sibling CLI commands) are referenced, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| update.md (2,094w, 9 H2 / 3 H3, 3 code) | notes 5 (`oc_cli_update_commands`) + 6 (`oc_cli_update_flow`) | The page mixes an operator-facing command/option reference (usage, options, status/repair/wizard subcommands, shorthand) with a dense internal-mechanics narrative (channel↔install alignment, staged-npm install, managed-service handoff, control-plane response shapes, the 9-step git-checkout flow + post-core plugin convergence). Two distinct task clusters; splitting keeps each note focused, ≤6 code blocks, and well under the 2,500w cap. |
| (tasks / transcripts / tui / uninstall / voicecall / webhooks) | (none — 1 note each) | Each is a single command-reference procedure ≤1,178w with one BB; no split needed. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (5,722 measured words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (every CLI reference page documents a command-invocation task). No concept/
  model/argument notes in this slice.
- Est. digest words ~**3,960** (avg ~495/note); all 8 notes ≤640w. Source code fences (8+6+3+1+3+6+3 = 30 total)
  distribute across the 8 notes; each note keeps ≤6 (usage/example/config/flag-illustration snippets reproduced
  selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21): each note maps **≥8 relevance-selected `term_dictionary`
  terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** (≥5 of the 10 docs EXISTING +
  each with a per-link relevance statement. All snippets and all cited EXISTING term/repo/doc note_ids are

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> (`SELECT 1 FROM notes WHERE note_id='<path>'`) on 2026-06-21. Sibling `oc_*` notes in this series and the
> master pre-step `entry_openclaw_docs.md` are cited as "(planned, this series)" and count toward the 10-doc
> a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; snippets
> `../../code_snippets/snippet_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; repos
> `../../../areas/code_repos/repo_Y.md`; entry points `../../../0_entry_points/entry_Y.md`. Each link is rendered
> as `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_cli_tasks (8t · 10s · 10d)
Source: tasks.md — durable background-task ledger + Task Flow state; `list/show/notify/cancel/audit/maintenance/flow`; runtime kinds `subagent`/`acp`/`cron`/`cli`; cron run-registry pruning.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product whose CLI this is; relevance: `openclaw tasks` is its background-task command.
- [Cron](../../term_dictionary/term_cron.md) — time-scheduled job execution; relevance: `cron` is one of the `--runtime` kinds and maintenance prunes `cron:<jobId>:run:<uuid>` registry rows.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — the schedule syntax cron jobs use; relevance: the cron tasks this ledger tracks are driven by cron expressions.
- [Subagent](../../term_dictionary/term_subagent.md) — a delegated child agent; relevance: `subagent` is a `--runtime` kind in the task ledger.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol bridging external agent clients; relevance: `acp` is a `--runtime` kind for routed tasks.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable queued-work store; relevance: the task ledger is a queued/durable background-task store with statuses queued/running/succeeded/lost.
- [Delegate Task](../../term_dictionary/term_delegate_task.md) — handing work to a background runner; relevance: the ledger records delegated/background task runs the operator inspects and cancels.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/state storage; relevance: tasks are looked up by session key / child-session rows and the stale cron run-session registry is pruned.

**Docs**
- [Claude Code: Scheduled Task Execution Model](../claude_code/cc_scheduled_task_execution_model.md) — how a coding agent runs scheduled/background tasks; relevance: same background-task-runner concept `openclaw tasks` inspects.
- [Claude Code: Loop Scheduled Tasks](../claude_code/cc_loop_scheduled_tasks.md) — the `/loop` recurring-task surface; relevance: parallel operator view of scheduled background work.
- [Claude Code: Scheduling Options Comparison](../claude_code/cc_scheduling_options_comparison.md) — cron vs in-app schedulers; relevance: frames the `cron` runtime kind among scheduling options.
- [Hermes: Cron Internals](../hermes_agent/hermes_cron_internals.md) — internal cron job state/run model; relevance: the persisted run logs/job state the `maintenance` reconciliation reads before marking cron tasks `lost`.
- [Hermes: Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — defining cron jobs; relevance: the cron tasks surfaced by `--runtime cron`.
- [Hermes: Cron Troubleshooting Guide](../hermes_agent/hermes_guide_cron_troubleshooting.md) — diagnosing stuck/failed cron runs; relevance: mirrors `tasks audit` surfacing stale/lost/delivery-failed records.
- [Hermes: Subagent Delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating to child agents; relevance: the `subagent` runtime kind in the ledger.
- [Hermes: Kanban Multi-Agent Board](../hermes_agent/hermes_kanban_multi_agent_board.md) — board view of agent tasks; relevance: an alternative inspect/cancel surface over background tasks.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — operating the gateway runtime; relevance: the Gateway owns the live cron/run context offline CLI audit is not authoritative for.
- [oc_cli_status](oc_cli_status.md) — (planned, cl07) `openclaw status` shows pending update/task rows; relevance: sibling observability command that surfaces task state.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/task state subsystem; relevance: implements the durable task ledger + session-key lookups.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway runtime; relevance: owns the process-local cron active-job set the audit reconciles against.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: background tasks run agent work the ledger tracks.

**Snippets**
- [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — cron scheduler tick loop; relevance: the scheduled-run engine behind `--runtime cron` tasks.
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — executing a cron run; relevance: produces the run records `tasks list/show` display.
- [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — setting up a cron run context; relevance: the live run context audit checks for liveness.
- [snippet_hermes_agent_cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — persisted cron job state; relevance: the run logs/job state maintenance reads before marking tasks `lost`.
- [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — cron utility helpers; relevance: registry/run-id helpers around the cron run rows pruned by maintenance.
- [snippet_hermes_agent_tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — registering a cron job; relevance: creates the `cron:<jobId>` registry rows maintenance prunes.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — cron job handoff between runtimes; relevance: the in-memory-vs-persisted handoff the CLI audit cannot see authoritatively.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached ACP runtime manager; relevance: the `acp` runtime kind's detached background tasks.

### oc_cli_transcripts (8t · 10s · 10d)
Source: transcripts.md — read-only stored-transcript inspector; state-dir layout `$OPENCLAW_STATE_DIR/transcripts/YYYY-MM-DD/<session>/`; `list/show/path` + `--json`; per-day grouping; missing-summary causes; `transcripts.enabled`/`autoStart` config.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw transcripts` is its stored-transcript inspector.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable per-session storage; relevance: transcripts are stored per session under the state directory keyed by session id.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — a side-stored conversation transcript; relevance: directly names the append-only `transcript.jsonl` artifact the CLI locates.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text transcription; relevance: live transcript sources capture/summarize meeting audio into STT-derived utterances.
- [Real-time Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming transcription; relevance: live `autoStart` sources stream utterances into `transcript.jsonl`.
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice/phone interaction; relevance: Discord-voice / Slack-huddle `autoStart` sources are voice channels recorded here.
- [Compaction](../../term_dictionary/term_compaction.md) — summarizing long history; relevance: `summary.md` is a compacted summary of the append-only `transcript.jsonl`.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured machine output; relevance: closest structured-output term for the `--json` `list/show/path` fields.

**Docs**
- [Claude Code: Sessions](../claude_code/cc_sessions.md) — session storage and resumption; relevance: the per-session artifact model transcripts extend.
- [Claude Code: SDK Sessions Overview](../claude_code/cc_sdk_sessions_overview.md) — programmatic session model; relevance: session id → on-disk session directory mapping, like the transcripts layout.
- [Claude Code: SDK Session Store](../claude_code/cc_sdk_session_store.md) — where sessions persist; relevance: parallels `$OPENCLAW_STATE_DIR/transcripts/...` on-disk layout.
- [Claude Code: Checkpointing](../claude_code/cc_checkpointing.md) — periodic state snapshots; relevance: `summary.json`/`summary.md` are checkpoint-like session artifacts.
- [Claude Code: What Survives Compaction](../claude_code/cc_what_survives_compaction.md) — what a summary retains; relevance: explains why `summary.md` may be missing/partial.
- [Claude Code: Application Data](../claude_code/cc_claude_application_data.md) — on-disk app data dirs; relevance: the state-directory concept (`~/.openclaw`, `OPENCLAW_STATE_DIR`).
- [Pi: Session File Format](../pi/pi_session_file_format.md) — session-on-disk JSONL format; relevance: directly parallels `transcript.jsonl` / `metadata.json` / `summary.json`.
- [Pi: Sessions](../pi/pi_sessions.md) — session lifecycle; relevance: when sessions write summaries (stop vs import), mirroring "Missing summaries".
- [Hermes: Session Search & Storage](../hermes_agent/hermes_session_search_storage.md) — finding stored sessions; relevance: `transcripts list` is the equivalent stored-session finder.
- [oc_cli_tui](oc_cli_tui.md) — (planned, this series) same session-key selection model; relevance: sibling command that shares the session-id selector semantics.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/transcript storage; relevance: implements the state-dir transcript layout the CLI reads.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: transcript summaries feed long-term memory.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channels; relevance: the voice-channel `autoStart` transcript sources.

**Snippets**
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event records; relevance: the events appended to `transcript.jsonl`.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — scanning the FS for transcripts; relevance: exactly the date/session-dir scan `transcripts list` performs.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — reading the session FS index; relevance: how `list` enumerates per-day session folders.
- [snippet_openclaw_gateway_session_fs_title_cache_archive](../../code_snippets/snippet_openclaw_gateway_session_fs_title_cache_archive.md) — title cache for sessions; relevance: the `title` column in `list` output.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — classifying session files; relevance: distinguishing `metadata.json`/`transcript.jsonl`/`summary.md` artifacts.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — reading session file text; relevance: how `show` prints `summary.md`.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory event stream; relevance: transcript/summary ingestion into memory.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compacting/resetting a session; relevance: the summarization that produces `summary.md`.
- [snippet_hermes_agent_honcho_session_query](../../code_snippets/snippet_hermes_agent_honcho_session_query.md) — querying stored sessions; relevance: parallels the date-qualified `list`/`show` selector.
- [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — exporting a session trajectory; relevance: the "feed a transcript to another tool" read-only export use case.

### oc_cli_tui (9t · 10s · 10d)
Source: tui.md — Gateway-backed vs `--local` embedded terminal UI; option table (url/token/password/session/deliver/thinking/timeout/history); `chat`/`terminal` aliases; SecretRef auth; agent-workspace auto-select; config-repair loop; `/goal` footer.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw tui` is its terminal UI command.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex socket protocol; relevance: the TUI connects over the Gateway WebSocket URL (`--url ws://…`).
- [OAuth](../../term_dictionary/term_oauth.md) — token-based authorization; relevance: gateway token/password auth the TUI resolves.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret resolution; relevance: `tui` resolves configured gateway-auth SecretRefs for token/password (`env`/`file`/`exec`).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: `--local` runs the embedded agent runtime directly in the terminal.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `--session <key>` selection + agent-workspace auto-select + `--history-limit` attach.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: in-TUI tool calls; plugin approval gates prompt for tool use in local mode.
- [Persistent Goal](../../term_dictionary/term_persistent_goal.md) — a tracked session goal; relevance: session goals appear in the footer and are managed with `/goal`.
- [A2UI](../../term_dictionary/term_a2ui.md) — agent-to-UI rendering surface; relevance: the rendered terminal UI surface the TUI presents.

**Docs**
- [Hermes: TUI Interface](../hermes_agent/hermes_tui_interface.md) — a coding agent's terminal UI; relevance: direct counterpart to `openclaw tui`.
- [Hermes: CLI Interface](../hermes_agent/hermes_cli_interface.md) — the CLI surface; relevance: the `chat`/`terminal` aliases live on the CLI.
- [Hermes: Slash Commands in Interactive CLI](../hermes_agent/hermes_slash_commands_interactive_cli.md) — in-TUI slash commands; relevance: the `/auth`, `/goal`, `!openclaw …` in-TUI command surface.
- [Hermes: CLI Session Background](../hermes_agent/hermes_cli_session_background.md) — backgrounding a CLI session; relevance: gateway-backed vs local-embedded session modes.
- [Hermes: Quickstart First Chat](../hermes_agent/hermes_quickstart_first_chat.md) — first interactive chat; relevance: the `openclaw chat` entry experience.
- [Claude Code: Interactive Mode Keyboard Shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — interactive terminal controls; relevance: the interactive TUI keyboard surface.
- [Claude Code: Interactive Session Features](../claude_code/cc_interactive_session_features.md) — interactive-session features; relevance: the in-session features the embedded TUI exposes.
- [Pi: Interactive Usage](../pi/pi_interactive_usage.md) — interactive REPL usage; relevance: the local embedded interactive runtime model.
- [Pi: Keybindings](../pi/pi_keybindings.md) — TUI keybindings; relevance: terminal interaction layer of the embedded UI.
- [oc_cli_config](oc_cli_config.md) — (planned, cl02) `config set tui.footer.showRemoteHost`; `config validate`/repair; relevance: the config commands the TUI repair loop drives.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/TUI surface; relevance: implements `openclaw tui`/`chat`/`terminal`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the WebSocket endpoint the non-local TUI attaches to.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/Control-UI surfaces; relevance: sibling terminal/UI surfaces.

**Snippets**
- [snippet_hermes_agent_tui_entry](../../code_snippets/snippet_hermes_agent_tui_entry.md) — TUI entry point; relevance: the launch path of `openclaw tui`.
- [snippet_hermes_agent_tui_server_render](../../code_snippets/snippet_hermes_agent_tui_server_render.md) — TUI render loop; relevance: rendering the terminal UI incl. the footer/host label.
- [snippet_hermes_agent_tui_event_publisher](../../code_snippets/snippet_hermes_agent_tui_event_publisher.md) — TUI event publishing; relevance: streaming assistant events into the terminal.
- [snippet_hermes_agent_tui_ws_primitives](../../code_snippets/snippet_hermes_agent_tui_ws_primitives.md) — TUI WebSocket primitives; relevance: the `--url ws://` Gateway connection layer.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — TUI JSON-RPC server; relevance: the request/response protocol over the Gateway socket.
- [snippet_hermes_agent_tui_server_slash](../../code_snippets/snippet_hermes_agent_tui_server_slash.md) — TUI slash-command handler; relevance: `/auth`, `/goal`, `!`-prefixed shell-out commands.
- [snippet_hermes_agent_tui_server_interrupt](../../code_snippets/snippet_hermes_agent_tui_server_interrupt.md) — interrupting a TUI turn; relevance: interactive control in the terminal session.
- [snippet_hermes_agent_cli_web_websocket](../../code_snippets/snippet_hermes_agent_cli_web_websocket.md) — CLI→web WebSocket; relevance: the gateway-WebSocket attach `--url`/`--token` uses.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: token/password/SecretRef auth resolution for `--token`/`--password`.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive CLI prompter; relevance: the interactive prompts the TUI/`configure` repair flow uses.

### oc_cli_uninstall (8t · 10s · 10d)
Source: uninstall.md — remove gateway service / state+config / workspace / macOS app (`--service`/`--state`/`--workspace`/`--app`/`--all`); `--dry-run`/`--yes`/`--non-interactive`; `backup create`-first recommendation.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw uninstall` removes its gateway service + local data.
- [Health Check](../../term_dictionary/term_health_check.md) — service-liveness monitoring; relevance: uninstall removes the supervised gateway service whose health is otherwise monitored (lifecycle counterpart).
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — persisted state/config; relevance: `--state` removes persisted state/config, `--workspace` removes workspace dirs.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent product; relevance: the coding-agent gateway being removed.
- [npm](../../term_dictionary/term_npm.md) — the Node package manager; relevance: the global-install method uninstall complements (CLI remains; package uninstall is separate).
- [Node.js](../../term_dictionary/term_node_js.md) — the JS runtime; relevance: the runtime hosting the gateway service uninstall stops/removes.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — resolved-secret storage; relevance: state/config holding resolved secrets is removed with `--state`.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeatable safe operations; relevance: `--dry-run` previews removals and re-runnable uninstall flags make removal idempotent.

**Docs**
- [Claude Code: Uninstall](../claude_code/cc_uninstall.md) — uninstalling a coding agent CLI; relevance: direct counterpart describing service/data removal.
- [Hermes: Updating & Uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update + uninstall lifecycle; relevance: the install-lifecycle counterpart with the same service/state removal model.
- [Hermes: Profile Gateways & Services](../hermes_agent/hermes_profile_gateways_services.md) — gateway service profiles; relevance: the supervised gateway service `--service` removes.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — operating the gateway service; relevance: stopping/removing the managed service.
- [Hermes: Installation](../hermes_agent/hermes_installation.md) — install paths; relevance: the install whose artifacts uninstall reverses.
- [Hermes: CLI Ops/Maintenance/Auth Commands](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/maintenance CLI; relevance: the maintenance command family uninstall belongs to.
- [Claude Code: Install Diagnostics](../claude_code/cc_install_diagnostics.md) — diagnosing install state; relevance: what `--dry-run` inspects before removal.
- [Claude Code: CLI Commands](../claude_code/cc_cli_commands.md) — the CLI command set; relevance: places uninstall among lifecycle commands.
- [oc_cli_update_commands](oc_cli_update_commands.md) — (planned, this series) the update/install lifecycle command; relevance: install-lifecycle counterpart to uninstall.
- [oc_install_uninstall](oc_install_uninstall.md) — (planned, in05) install-side uninstall guide; relevance: the `/install/uninstall` page this CLI command links out to.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway service; relevance: the supervised service `--service`/`--all` removes.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: CLI itself remains after uninstall; implements the command.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level monorepo; relevance: the install whose artifacts uninstall removes.

**Snippets**
- [snippet_hermes_agent_cli_uninstall](../../code_snippets/snippet_hermes_agent_cli_uninstall.md) — CLI uninstall implementation; relevance: the directly analogous uninstall command.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway service lifecycle; relevance: stopping the service before removal.
- [snippet_hermes_agent_cli_gateway_systemd](../../code_snippets/snippet_hermes_agent_cli_gateway_systemd.md) — systemd unit management; relevance: removing the managed Linux service unit.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — render/parse systemd unit; relevance: the service definition `--service` tears down.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — macOS launchd handoff; relevance: the macOS LaunchAgent/`--app` removal path.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — kill a process tree; relevance: stopping the running gateway before file removal.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: the supervisor whose service uninstall disables.
- [snippet_hermes_agent_cli_gateway_pid_discovery](../../code_snippets/snippet_hermes_agent_cli_gateway_pid_discovery.md) — discovering the gateway PID; relevance: finding the running service to stop on uninstall.

### oc_cli_update_commands (8t · 10s · 10d)
Source: update.md command surface — Usage, Options (`--channel`/`--tag`/`--dry-run`/`--no-restart`/`--json`/`--timeout`/`--yes`), `update status`/`repair`/`wizard`, downgrade/Nix guards, `--update` shorthand.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw update` updates it and switches channels.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: stable/beta channels install from npm dist-tags; `--tag` overrides the package spec.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped/dist-tag package resolution; relevance: `--tag <dist-tag|version|spec>` resolves the package target.
- [Health Check](../../term_dictionary/term_health_check.md) — service-liveness verification; relevance: `update status` reports availability; restart verifies the gateway reports the expected version.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent core; relevance: the coding-agent core being updated.
- [Cron](../../term_dictionary/term_cron.md) — scheduled background runs; relevance: the gateway core auto-updater is a scheduled/background update path.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured machine output; relevance: `--json` prints the `UpdateRunResult` machine-readable result.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin install metadata; relevance: `update repair` reconverges tracked plugin install records/metadata after a core update.

**Docs**
- [Claude Code: Update & Release Channels](../claude_code/cc_update_and_release_channels.md) — update channels (stable/beta/dev); relevance: direct counterpart to `--channel stable|beta|dev`.
- [Hermes: Updating & Uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — the update command + flow; relevance: the closest agent-CLI update counterpart.
- [Claude Code: Advanced Install & Verification](../claude_code/cc_advanced_install_and_verification.md) — post-install verification; relevance: the restart-verify-version step `update` performs.
- [Claude Code: Install](../claude_code/cc_install.md) — install methods; relevance: the npm/pnpm/bun install path `update` complements.
- [Claude Code: Plugin Caching & Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin repair; relevance: `update repair`'s plugin sync/convergence.
- [Claude Code: Install Diagnostics](../claude_code/cc_install_diagnostics.md) — diagnosing install state; relevance: what `update status` surfaces.
- [Hermes: CLI Ops/Maintenance/Auth Commands](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/maintenance commands; relevance: the maintenance command family `update`/`update repair` belong to.
- [Pi: Settings Reference](../pi/pi_settings_reference.md) — config settings; relevance: the persisted `--channel` config field.
- [oc_cli_update_flow](oc_cli_update_flow.md) — (planned, this series) the internal update mechanics half; relevance: the same command split into command-surface vs flow.
- [oc_cli_doctor](oc_cli_doctor.md) — (planned, cl03) `update repair` runs `doctor --fix`; relevance: the doctor integration the command surface invokes.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: implements `update`/`update wizard`/`status`/`repair`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: restarted and version-verified after update.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo; relevance: the source/package updated.

**Snippets**
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — the CLI update command; relevance: directly analogous `update` command implementation.
- [snippet_hermes_agent_cli_banner_update](../../code_snippets/snippet_hermes_agent_cli_banner_update.md) — update-availability banner; relevance: the availability surfacing `update status` reports.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: the staged plugin install/sync after a core update.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor command; relevance: `update repair` runs `doctor --fix` over plugins.
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — plugin list/inspect; relevance: `openclaw plugins inspect <id> --runtime --json` guidance from repair.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applying a reloaded config; relevance: `--channel` persistence + config reload during repair.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart at startup; relevance: the post-update gateway restart `--no-restart` skips.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust/integrity findings; relevance: the integrity-drift abort on pinned plugin artifacts.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — CLI security advisories; relevance: the trust/verify gates around channel/plugin updates.

### oc_cli_update_flow (8t · 10s · 10d)
Source: update.md internals — What it does (channel↔install alignment, staged-npm install, managed-service handoff, restart-and-verify, LaunchAgent re-bootstrap), Control-plane `update.run` response shapes + sentinel, Git checkout flow (Channel selection + 9 Steps + post-core plugin convergence).

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the internal mechanics of `openclaw update`.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: staged-npm temp-prefix install + dist-tag resolution + integrity-drift abort.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped/dist-tag resolution; relevance: `latest`/`beta` dist-tag selection and the `main → github:openclaw/openclaw#main` mapping.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS compiled to a build; relevance: dev preflight runs the TypeScript build, walking back up to 10 commits to the newest buildable commit.
- [Health Check](../../term_dictionary/term_health_check.md) — service-liveness verification; relevance: restart-and-verify checks gateway health/version/channel readiness + LaunchAgent/launchd state.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured control-plane messages; relevance: `update.run` control-plane response shapes + sentinel JSON.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent core; relevance: the agent core whose package tree is staged-swapped.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-runnable operations; relevance: staged install + verify-then-swap + `update repair` make the update safely re-runnable.

**Docs**
- [Claude Code: Advanced Install & Verification](../claude_code/cc_advanced_install_and_verification.md) — verify-after-install mechanics; relevance: the staged-install-then-verify pattern.
- [Claude Code: Update & Release Channels](../claude_code/cc_update_and_release_channels.md) — channel→source mapping; relevance: dev=git, stable/beta=npm channel↔install alignment.
- [Claude Code: Install Failures Reference](../claude_code/cc_install_failures_reference.md) — install failure modes; relevance: the suspect-tree abort + non-zero exit + rollback instructions.
- [Claude Code: Plugin Caching & Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin sync/repair; relevance: the post-core plugin convergence pass.
- [Hermes: Updating & Uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update flow internals; relevance: the closest agent-CLI update-mechanics counterpart.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway restart/health ops; relevance: the managed-service stop/restart/verify handoff.
- [Hermes: Profile Distributions](../hermes_agent/hermes_profile_distributions.md) — distribution/channel profiles; relevance: stable/beta/dev distribution channels.
- [Pi: RPC Protocol](../pi/pi_rpc_protocol.md) — RPC request/response shape; relevance: the `update.run` control-plane request/response model.
- [oc_cli_update_commands](oc_cli_update_commands.md) — (planned, this series) the operator command surface half; relevance: the same command split into surface vs flow.
- [oc_cli_doctor](oc_cli_doctor.md) — (planned, cl03) `doctor` runs as the final safe-update check (Step 8); relevance: the doctor step inside the git-checkout flow.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: managed-service handoff, restart sentinel, control-plane `update.run` handler.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: the detached `openclaw update --yes --json` CLI path the handoff spawns.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo; relevance: the git-checkout build + plugin sync target.

**Snippets**
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache respawn; relevance: the build + respawn after a git-checkout rebuild.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: the macOS LaunchAgent re-bootstrap + detached restart handoff.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: the managed-service stop-before-swap / restart sequence.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart at startup; relevance: the verify-only plugin load on the restarted Gateway.
- [snippet_hermes_agent_cli_main_cmd_update](../../code_snippets/snippet_hermes_agent_cli_main_cmd_update.md) — the update command body; relevance: the staged-install + restart-verify control flow.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — gateway lifecycle; relevance: stop/refresh-metadata/restart/verify around the package swap.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway health status; relevance: the post-restart health/version readiness check.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install; relevance: the per-plugin sync step in the 9-step flow.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin integrity findings; relevance: the integrity-drift abort + post-core convergence validation.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI→gateway dispatch; relevance: the control-plane `update.run` dispatch + structured response.

### oc_cli_voicecall (8t · 12s · 10d)
Source: voicecall.md — voice-call plugin command surface; `setup`/`smoke` readiness; call lifecycle (`call`/`start`/`continue`/`speak`/`dtmf`/`end`/`status`); `tail`/`latency` logs+metrics; `expose` Tailscale serve/funnel toggling.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw voicecall` is its (plugin-provided) voice-call command surface.
- [Voice Call](../../term_dictionary/term_voice_call.md) — the voice/phone call concept; relevance: the exact subject — voice-call plugin commands.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — an automated voice agent; relevance: `--mode conversation` keeps the call open as an interactive voice bot.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — text→audio synthesis; relevance: `call`/`speak`/`continue` speak `--message` text (TTS on the call).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text; relevance: conversation mode listens for responses (STT on the call).
- [Tunneling](../../term_dictionary/term_tunneling.md) — exposing a local endpoint publicly; relevance: `expose` toggles Tailscale serve/funnel so carriers can reach the webhook.
- [Webhook](../../term_dictionary/term_webhook.md) — an inbound HTTP callback; relevance: external providers (twilio/telnyx/plivo) require a public webhook URL `expose` configures.
- [VoIP](../../term_dictionary/term_voip.md) — voice over IP / telephony; relevance: the outbound voice call to an E.164 number is a VoIP/telephony operation.

**Docs**
- [Hermes: Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — a CLI voice-call surface; relevance: direct counterpart command surface for voice calls.
- [Hermes: Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — operating voice mode; relevance: setup/smoke/lifecycle operator flow.
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text in calls; relevance: the listen side of `--mode conversation`.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the speak side of `call`/`speak`/`continue`.
- [Hermes: Voice Gateway Discord VC](../hermes_agent/hermes_voice_gateway_discord_vc.md) — gateway voice routing; relevance: operational commands routed to the Gateway voice runtime.
- [Hermes: SMS via Twilio](../hermes_agent/hermes_messaging_sms_twilio.md) — Twilio integration + webhooks; relevance: the `twilio` provider + public-webhook requirement.
- [Hermes: Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio config; relevance: the audio media-stream config behind a call.
- [Claude Code: Voice Dictation](../claude_code/cc_voice_dictation.md) — voice input to a coding agent; relevance: the STT/voice-input side of agent voice interaction.
- [oc_cli_webhooks](oc_cli_webhooks.md) — (planned, this series) sibling Tailscale-exposed integration command; relevance: shares the `expose`/Tailscale serve-funnel webhook-exposure pattern.
- [oc_plugins_voice_call](oc_plugins_voice_call.md) — (planned, pl21) the voice-call plugin guide; relevance: the `/plugins/voice-call` config page this command surface drives.

**Repos**
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: the channel this plugin drives.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: the TTS/STT providers used during a call.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: operational commands route to the Gateway voice-call runtime.

**Snippets**
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: the call-lifecycle manager behind `call`/`start`/`end`/`status`.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: the Gateway/standalone runtime operational commands route to.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — call media-stream audio; relevance: the audio path `speak`/`continue` drive.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — call media-stream transcription; relevance: the STT listen side of conversation mode.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — media-stream admission; relevance: call admission/`status` of active calls.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — verify webhook signatures; relevance: securing the exposed voice webhook endpoint.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay cache; relevance: the voice webhook `expose` makes reachable.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: a TTS provider for spoken `--message` text.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: a local TTS provider option for calls.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the STT/TTS pipeline turn-latency `latency` summarizes.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: relaying call transcription, logged to `calls.jsonl`.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the analogous voice-mode command tool.

### oc_cli_webhooks (8t · 10s · 10d)
Source: webhooks.md — Gmail Pub/Sub integration via bundled `gog` watcher; `gmail setup` (Pub/Sub topic/subscription, OpenClaw delivery, `gog watch serve`, Tailscale exposure) + `gmail run` (foreground serve + auto-renew loop); End-to-end flow.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw webhooks` configures its webhook delivery target.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP callback; relevance: the exact subject — webhook helpers + `--hook-url` delivery target.
- [Pub/Sub](../../term_dictionary/term_pub_sub.md) — publish/subscribe messaging; relevance: Gmail watch → GCP Pub/Sub topic/subscription/push.
- [OAuth](../../term_dictionary/term_oauth.md) — token-based authorization; relevance: `--project` is the OAuth client owner; Gmail watch is OAuth-scoped.
- [Tunneling](../../term_dictionary/term_tunneling.md) — public exposure of a local endpoint; relevance: `--tailscale funnel/serve` exposes the Pub/Sub push endpoint.
- [Cron](../../term_dictionary/term_cron.md) — periodic background runs; relevance: the watch auto-renew loop (`--renew-minutes 720`) pairs with cron-jobs automation.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: the public push endpoint Tailscale funnel exposes is an HTTPS/TLS endpoint Pub/Sub pushes to.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured machine output; relevance: `--json` prints a machine-readable setup summary.

**Docs**
- [Hermes: MS Graph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — a push-notification webhook listener; relevance: the same change-notification → webhook-delivery pattern as Gmail Pub/Sub.
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook routing/delivery; relevance: the OpenClaw `--hook-url`/`--hook-token` delivery target.
- [Hermes: Webhooks Routes & Security](../hermes_agent/hermes_webhooks_routes_security.md) — securing webhook routes; relevance: `--push-token`/`--hook-token` and trusted-endpoint exposure.
- [Hermes: Messaging Email](../hermes_agent/hermes_messaging_email.md) — email ingestion; relevance: the Gmail email source these webhooks ingest.
- [Hermes: Google Workspace Skill](../hermes_agent/hermes_google_workspace_skill.md) — Gmail/Google integration; relevance: the Gmail account/OAuth project the watch is scoped to.
- [Hermes: MS Graph App Registration](../hermes_agent/hermes_msgraph_app_registration.md) — OAuth app registration for push; relevance: parallels the GCP project + OAuth client setup for Gmail watch.
- [Hermes: Google Chat Messaging](../hermes_agent/hermes_messaging_google_chat.md) — GCP-side push integration; relevance: the Google Cloud project + Pub/Sub side of the integration.
- [Band: Integration Methods](../band/band_integration_methods.md) — integration patterns (webhook/poll/push); relevance: situates webhook+Pub/Sub among integration methods.
- [oc_cli_voicecall](oc_cli_voicecall.md) — (planned, this series) sibling Tailscale-exposed integration command; relevance: shares the `expose`/Tailscale-funnel public-endpoint pattern.
- [oc_automation_cron_jobs](oc_automation_cron_jobs.md) — (planned, au01) Gmail Pub/Sub backend + GCP/OAuth setup; relevance: the `/automation/cron-jobs#gmail-pubsub-integration` end-to-end page this CLI pairs with.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the OpenClaw webhook delivery target (`--hook-url`) that receives pushed events.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI surface; relevance: implements the `webhooks gmail setup`/`run` commands.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Gmail/email message ingestion the watcher feeds.

**Snippets**
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway hooks request handler; relevance: the `--hook-url` endpoint that receives Pub/Sub pushes.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — platform webhook handler; relevance: the generic inbound-webhook delivery path.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — MS Graph push webhook; relevance: the analogous push-notification webhook receiver.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — devops webhook skill; relevance: wiring an external event source to an agent webhook.
- [snippet_hermes_agent_plugins_platform_google_chat](../../code_snippets/snippet_hermes_agent_plugins_platform_google_chat.md) — Google Chat platform; relevance: the GCP Pub/Sub push integration on Google's side.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service notifications; relevance: the auto-renew loop + cron-jobs pairing.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize+dispatch; relevance: `--hook-token`/`--push-token` auth on inbound deliveries.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content handling; relevance: trust handling of externally-pushed Gmail bodies (`--include-body`/`--max-bytes`).
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay cache; relevance: the Tailscale-exposed webhook + replay-protection pattern shared with `expose`.
- [snippet_hermes_agent_tools_msgraph](../../code_snippets/snippet_hermes_agent_tools_msgraph.md) — MS Graph tool (Pub/Sub-like watch); relevance: the watch+renew lifecycle parallel to Gmail watch auto-renew.

**DB-verification (xref-augment 2026-06-21):** every snippet (80 distinct, all in `resources/code_snippets/`) and
every cited EXISTING term (33 distinct), repo (`repo_openclaw{,_sessions,_gateway,_agents,_memory,_cli_wizard,_apps,_channels_voice_phone,_extensions_voice_speech,_channels_messaging}`),
and doc (`claude_code/cc_*`, `hermes_agent/hermes_*`, `pi/pi_*`, `band/band_*`) note_id was verified present via
`SELECT 1 FROM notes WHERE note_id='<path>'`. Sibling `oc_*` docs and `entry_openclaw_docs.md` are the only

## Undigested Terms Plan (Step 4e)

cl08 creates **0 new `term_dictionary` notes**. CLI/command vocabulary surfaced by these pages is digested as the
`oc_*` doc notes themselves (the command IS the note subject), and all cross-cutting concepts already have
substantive existing term notes that are LINKED, not redefined.

| Term (as it appears in source) | Disposition |
|---|---|
| `openclaw tasks` / Task Flow / background task ledger | → note 1 `oc_cli_tasks` (doc note; not a term). Link `term_cron`, `term_message_queue`, `term_subagent`. |
| `openclaw transcripts` / summary.md / state directory | → note 2 `oc_cli_transcripts` (doc note). Link `term_session_persistence`, `term_speech_to_text`. |
| `openclaw tui` / chat / terminal / local embedded mode | → note 3 `oc_cli_tui` (doc note). Link `term_websocket`, `term_oauth`. |
| `openclaw uninstall` | → note 4 `oc_cli_uninstall` (doc note). Link `term_health_check`, `term_npm`. |
| `openclaw update` / channels (stable/beta/dev) / managed-service handoff | → notes 5/6 (doc notes). Link `term_npm`, `term_health_check`, `term_typescript`. |
| `openclaw voicecall` / DTMF / smoke / expose | → note 7 `oc_cli_voicecall` (doc note). Link `term_voice_call`, `term_text_to_speech`, `term_speech_to_text`, `term_tunneling`. DTMF is documented as a flag, not promoted to a term. |
| `openclaw webhooks` / Gmail Pub/Sub / `gog` watcher / Tailscale | → note 8 `oc_cli_webhooks` (doc note). Link `term_webhook`, `term_pub_sub`, `term_oauth`, `term_tunneling`. |
| SecretRef / `env`/`file`/`exec` providers | linked → `term_secrets_manager` (existing). Not a new term. |
| Control-plane / `update.run` / sentinel / JSON results | documented inline in note 6; link `term_json_rpc`. Not promoted. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term without an existing note appears in
this slice. (Augment Step 2d re-scans to confirm; expected 0 per master.) Were one to surface (e.g. a reusable
"managed-service handoff" pattern), it would be captured via `/tessellum-capture-term-note` and added to its best-fit
glossary — candidate fit: `acronym_glossary_agentic_ai.md` (agent/runtime ops vocabulary) — but no such term is
proposed here.

## Term-Note Authoring Requirements

glossary update) is inherited from the master and does not apply. All term interactions are LINKS to existing,

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit; verified independently, not from
agent self-report.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py`: YAML field order/forbidden-fields, `# OpenClaw — …` H1, `## Overview`, source-mirrored body, `## Related Notes`, `## References`, `**Source**`/`**Last Updated**`/`**Status**` footer. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/cli/<page>.md`: no invented flags/defaults/subcommands; command tables faithful to source. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; one BB (procedure); every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | `## Related Notes` ≥6 relevance-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + entry, each an indexed `[text](path.md)` link with a relevance statement. |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references`: 0 links to non-existent notes; planned siblings/entry resolve after the phase + entry-point creation. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + DB rebuild: 0 broken relative paths. |
| G7 | Discoverability (outbound→inbound) | Each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` rows + `repo_openclaw*`/`term_*` inlinks). |
| G8 | In-degree ≥1 (anti-island) | `note_links` confirms in_degree ≥1 for all 8 notes; no orphan/island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_tasks oc_cli_transcripts oc_cli_tui oc_cli_uninstall oc_cli_update_commands oc_cli_update_flow oc_cli_voicecall oc_cli_webhooks"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION ($sec): $n"
  done
  # source_url present in YAML
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # at least one sibling oc_ link (cross-ref health)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING oc_ LINK: $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done

# YAML frontmatter sweep across the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source Code Fences | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_cli_tasks | procedure | 420 | 8 (subset reproduced ≤6) | ✅ |
| 2 | oc_cli_transcripts | procedure | 480 | 6 | ✅ |
| 3 | oc_cli_tui | procedure | 480 | 3 | ✅ |
| 4 | oc_cli_uninstall | procedure | 200 | 1 | ✅ |
| 5 | oc_cli_update_commands | procedure | 600 | 3 (from update.md, split) | ✅ |
| 6 | oc_cli_update_flow | procedure | 620 | 3 (from update.md, split) | ✅ |
| 7 | oc_cli_voicecall | procedure | 640 | 6 | ✅ |
| 8 | oc_cli_webhooks | procedure | 520 | 3 | ✅ |

No note approaches caps. `update.md` (2,094w) is split into notes 5+6 so each stays ≤620w; `tasks.md`'s 8 source
fences are reproduced selectively to keep note 1 ≤6 code blocks.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (master W1 pre-step) under the **CLI** cluster (cl08 slice):
oc_cli_tasks, oc_cli_transcripts, oc_cli_tui, oc_cli_uninstall, oc_cli_update_commands, oc_cli_update_flow,
oc_cli_voicecall, oc_cli_webhooks. Each note receives its entry-point back-link at finalization (satisfies G7/G8).
No separate sub-plan entry point is created (the slice is <30 notes; the series-level `entry_openclaw_docs.md`
is the hub).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; reciprocal where the new note links out):

- `entry_openclaw_docs.md` (planned, master W1) → all 8 notes (primary anti-island guarantee).
- `repo_openclaw_cli_wizard.md` → notes 3, 4, 5, 6, 7, 8 (the CLI/wizard surface implementing these commands).
- `repo_openclaw_gateway.md` → notes 1, 3, 5, 6, 7, 8 (Gateway runtime: task ledger, TUI attach, update restart,
  voicecall routing, webhook delivery).
- `repo_openclaw_sessions.md` → notes 1, 2 (task/transcript session state).
- `repo_openclaw_channels_voice_phone.md` + `repo_openclaw_extensions_voice_speech.md` → note 7 (voicecall).
- `repo_openclaw_channels_messaging.md` → note 8 (Gmail/email ingestion).
- `term_cron.md` → notes 1, 8; `term_webhook.md` + `term_pub_sub.md` → note 8; `term_voice_call.md` → note 7;
  `term_npm.md` → notes 4, 5, 6; `term_health_check.md` → notes 4, 5, 6; `term_tunneling.md` → notes 7, 8;
  `term_websocket.md` → note 3.
- `term_openclaw.md` → (selectively) the highest-traffic notes (5, 6, 7) plus the docs hub link.

## Pacing Rules (inherited from master)

One execution phase; cap dynamic-workflow fan-out at ~30 agents/run (8 notes here — single wave). Re-read each
source page; reproduce command/flag/config snippets verbatim. One BB per note (all procedure). Commit + push after
the phase (`git pull --rebase --autostash` first; no Claude co-author trailer). Reindex incrementally; verify
`note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope.** xref-augment of sub-plan cl08 (7 CLI pages, 8 planned notes). Re-read all 7 source pages under
`inbox/openclaw_docs/cli/` (tasks 433w / transcripts 608w / tui 583w / uninstall 174w / update 2,094w /
voicecall 1,178w / webhooks 652w = 5,722w measured — matches the plan's Source table). Replaced the prior
`## Candidate Cross-References` (floors: ≥6 terms + repos + siblings, no snippets/docs) with
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at the raised floors
**≥8 terms · ≥10 snippets · ≥10 docs per note**.


| Note | Terms | Snippets | Docs (existing / planned-oc) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_cli_tasks | 8 | 10 | 10 (9 / 1) | 3 | ✅ |
| oc_cli_transcripts | 8 | 10 | 10 (9 / 1) | 3 | ✅ |
| oc_cli_tui | 9 | 10 | 10 (9 / 1) | 3 | ✅ |
| oc_cli_uninstall | 8 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_cli_update_commands | 8 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_cli_update_flow | 8 | 10 | 10 (8 / 2) | 3 | ✅ |
| oc_cli_voicecall | 8 | 12 | 10 (8 / 2) | 3 | ✅ |
| oc_cli_webhooks | 8 | 10 | 10 (8 / 2) | 3 | ✅ |

- **Terms (33 distinct, all existing):** beyond the original slugs, the relevance re-search surfaced and added
  `term_cron_expression`, `term_delegate_task`, `term_sidechain_transcript`, `term_realtime_transcription`,
  `term_persistent_goal`, `term_a2ui`, `term_node_js`, `term_idempotency`, `term_npm_scoping`,
  `term_plugin_manifest`, `term_voice_bot`, `term_voip`, `term_tls` — each tied to a concrete source feature
  (e.g. `--runtime cron` → `term_cron_expression`; `/goal` footer → `term_persistent_goal`;
  `--mode conversation` → `term_voice_bot`; staged install/verify-swap → `term_idempotency`).
  cover every theme richly — `voice_call_*` ×8 for voicecall, `cron_*`/`cronjob_*` for tasks,
  `session_fs_*`/`memory_host_session_*` for transcripts, `tui_server_*`/`tui_ws_*` for tui,
  `daemon_*`/`service_controller`/`process_supervisor` for uninstall/update-flow, `gateway_hooks_*`/
  `archives/code_snippets/`) was DROPPED to keep all snippet paths uniform at `../../code_snippets/`.
- **Docs (≥5 existing per note):** leaned on the direct coding-agent counterparts — `cc_uninstall`,
  `cc_update_and_release_channels`, `hermes_updating_uninstalling`, `hermes_tui_interface`,
  `hermes_cron_internals`, `cc_sessions`/`pi_session_file_format` (transcripts), `hermes_voice_mode_cli`/
  `hermes_tts_providers`/`hermes_stt_transcription` (voicecall), `hermes_webhooks_routing_delivery`/
  `hermes_msgraph_webhook_listener` (webhooks). Cradle/Datanet/AWS-pipeline `tutorial_*` hits were discarded
  as abuse/data-pipeline false positives (not relevant to a coding-agent CLI).

**New-term candidates: none.** Step 2d re-scan of all 7 re-read pages surfaced no genuinely cross-cutting,
vault-reusable term lacking an existing note. CLI/command vocabulary (`openclaw tasks`, `update repair`,
`voicecall expose`, `gog watcher`, DTMF, SecretRef) is digested as the `oc_*` doc-note subject itself (per the
master's documentation-concept-note ownership policy), and every cross-cutting concept already has a substantive
(agent/runtime ops vocabulary), but no term is proposed. cl08 authors **0 new `term_dictionary` notes**.

**Issues / notes:** none blocking. The 3 cross-sub-plan link targets (`oc_install_uninstall` in05,
`oc_plugins_voice_call` pl21, `oc_automation_cron_jobs` au01) are same-folder `oc_*.md` references (all `oc_*`
notes route to `resources/documentation/openclaw/` per master) — corrected to bare `oc_Y.md` form during augment.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review run after xref-augment. CP7 word counts re-measured against the re-read source pages.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)`: every note ≥8 terms (8–9), ≥10 snippets (10–12), ≥10 docs (≥5 existing). Each link carries a `relevance:` statement (programmatic tally confirms counts; 0 bare links). |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision`: 8 rows contributed to `entry_openclaw_docs.md` (master W1 pre-step), CLI cluster; no new sub-plan entry point (slice <30 notes). Matches master's >30-notes-series CREATE-once decision. |
| CP4 | Size (≤30 or split) | **PASS** | 8 planned notes — well under 30; single execution phase. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master's Format Definition, itself derived from existing `claude_code/cc_*` + `pi/pi_*` doc notes (`## Overview` / `## Related Notes`, YAML field order, forbidden fields). G1 uses `check_note_format.py` + `check_yaml_frontmatter.py`. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: all 8 notes ≤640w / ≤6 code / ≤400L; `update.md` (2,094w) already split into notes 5+6. No borderline note left unsplit. |
| CP7 | Sources measured | **PASS** | Re-read all 7 pages 2026-06-21: 433/608/583/174/2,094/1,178/652 = 5,722w — exactly matches the plan's Source table (ratio 1.00, within 0.7–1.3×). No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present with disposition per source term (all → doc-note subject or link existing); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, mandate inherited from master). New-term scan (Step 2d) = 0, consistent with master policy. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs.md` → all 8; `repo_openclaw_*`/`term_*` per note); G8 in-degree ≥1 is a gated execution check, not merely recommended. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
