---
title: Sub-Plan au01 — OpenClaw Docs: Automation (cron-jobs, hooks, standing-orders, taskflow, tasks)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["automation/cron-jobs", "automation/hooks", "automation/standing-orders", "automation/taskflow", "automation/tasks"]
---

# Sub-Plan au01: Automation

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` → body →
> `## Related Notes` → `## References` → bold footer; ≤400 lines / ≤2500 words / ≤6 code blocks; one BB/note),
> dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), 9-GATE validation, cross-references,
> Undigested-Terms policy (OpenClaw vocab → `oc_*` doc notes, never new `term_dictionary` entries), and entry-point
> wiring (`entry_openclaw_docs.md`) are ALL inherited from the master. This file locks the per-page measurements,
> planned-note table, coverage map, split decisions, candidate cross-references, and the single-phase gate.

## Scope

The 5 **Automation** pages — how OpenClaw runs work on a schedule, in response to lifecycle events, on a recurring
"standing" cadence, as durable scheduled workflows, and as durable agent task runs:

- `automation/cron-jobs` — time-/webhook-/PubSub-triggered scheduled jobs (the largest, most procedural page).
- `automation/hooks` — lifecycle-event hooks (HOOK.md + handler), discovery, bundled/plugin hooks, config.
- `automation/standing-orders` — recurring "program" prompts the agent self-executes on a cadence (a convention,
  not a code feature) + the execute-verify-report pattern.
- `automation/taskflow` — durable scheduled-workflow primitive (Task Flow: managed/mirrored sync, revision
  tracking, cancel behavior) and how flows relate to tasks.
- `automation/tasks` — the durable task system: lifecycle, notifications, CLI, chat task board, status pressure,
  storage/maintenance, and how tasks relate to cron/flows/sessions.

**Priority P1 (Phase A — conceptual/operational core).** These pages define the scheduling/event/task vocabulary
(cron syntax, hook events, task lifecycle, flow sync modes) that gateway, CLI (`cli/cron`, `cli/hooks`,
`cli/tasks`), and concepts sub-plans reference. The code-side counterparts (`repo_openclaw_gateway`,
LINKED, not recreated.

**Source**: OpenClaw docs, 5 pages, **11,561 measured words**, 65 code fences. **Planned: 8 notes** (2 splits).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| cron-jobs | `automation/cron-jobs` | 4,487 | 22 | 13 | 9 | procedure (SPLIT: scheduling+CLI vs triggers/webhook/PubSub+config) |
| hooks | `automation/hooks` | 1,950 | 14 | 12 | 12 | procedure |
| standing-orders | `automation/standing-orders` | 1,396 | 8 | 17 | 15 | argument (convention/pattern) |
| taskflow | `automation/taskflow` | 1,016 | 5 | 8 | 2 | concept (durable-flow model) |
| tasks | `automation/tasks` | 2,712 | 16 | 11 | 3 | procedure (SPLIT: lifecycle+delivery vs CLI/board/storage) |

(Code = `grep -c '```'` / 2.)

## Content Strategy

- **Prioritize**: the cron schedule syntax + execution styles (isolated vs in-session) and the task **lifecycle**
  (states, delivery, status pressure) — these are the load-bearing operational contracts every other automation
  surface references. Hook **event types** + HOOK.md/handler structure are the second priority.
- **Split** (word-cap / mixed task-cluster): `cron-jobs.md` (4,487w, 13 H2) → a scheduling+execution+CLI procedure
  note and a triggers (webhook + Gmail PubSub) + configuration + troubleshooting procedure note; `tasks.md`
  (2,712w, 11 H2) → a lifecycle+creation+delivery note and a CLI+chat-board+storage/maintenance note.
- **Single note**: `hooks.md` (1,950w), `standing-orders.md` (1,396w), `taskflow.md` (1,016w) each fit one BB
  well under caps.
- **Link-out (do NOT redefine)**: CLI command pages (`cli/cron`, `cli/hooks`, `cli/tasks`) → CLI sub-plans
  (cl02/cl04/cl08); webhooks tool/channel detail → `tools/webhooks`/`plugins/webhooks`; gateway notifications
  delivery → gateway sub-plans; concepts (`concepts/commitments`, `concepts/dreaming`, `concepts/queue`,
  `concepts/session`, `concepts/agent-loop`, `concepts/system-prompt`, `concepts/timezone`) → concepts sub-plans.
  Reuse existing `term_cron`, `term_webhook`, `term_pubsub`-absent→`term_event_driven_architecture`, `term_oauth`,
  `term_idempotency`, `term_subagent` — never inline a term definition.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_automation_cron_jobs_scheduling.md` | procedure | cron-jobs.md: Quick start, How cron works, Schedule types (+ Day-of-month/week OR logic), Execution styles (isolated vs in-session, Command payloads, Payload options), Delivery and output, Output language, CLI examples, Managing jobs | 700 | Defining OpenClaw cron jobs: 5/6-field cron syntax + DOM/DOW OR logic, schedule types, isolated-vs-in-session execution styles and command payloads, delivery/output + output-language control, the `oc cron` CLI examples, and listing/pausing/removing jobs. |
| 2 | `oc_automation_cron_jobs_triggers_config.md` | procedure | cron-jobs.md: Webhooks (+ Authentication), Gmail PubSub integration (Wizard setup, Gateway auto-start, Manual setup, Gmail model override), Configuration (Command ladder), Troubleshooting | 650 | Event-triggered cron in OpenClaw: webhook-triggered jobs with authentication, the Gmail PubSub integration (wizard / gateway-auto-start / manual setup, model override), the configuration command ladder, and troubleshooting. |
| 3 | `oc_automation_hooks.md` | procedure | hooks.md: Choose the right surface, Quick start, Event types, Writing hooks (Hook structure, HOOK.md format, Handler implementation, Event context), Hook discovery (Hook packs), Bundled hooks (session-memory, bootstrap-extra-files, command-logger, compaction-notifier, boot-md), Plugin hooks, Configuration, CLI reference, Best practices, Troubleshooting | 700 | OpenClaw lifecycle hooks: choosing hooks vs other surfaces, hook event types, authoring a hook (HOOK.md + handler + event context), hook discovery/packs, the bundled hooks, plugin hooks, configuration, the `oc hooks` CLI, and troubleshooting. |
| 4 | `oc_automation_standing_orders.md` | argument | standing-orders.md: Why standing orders, How they work, Anatomy of a standing order, Standing orders plus cron, Examples (content/social, finance, monitoring), Execute-verify-report pattern, Multi-program architecture, Escalation rules, Best practices | 600 | Standing orders: recurring natural-language "program" prompts the agent self-executes on a cadence, why/how they work, their anatomy, pairing with cron, the execute-verify-report pattern, multi-program architecture with escalation rules, and best practices. |
| 5 | `oc_automation_taskflow.md` | concept | taskflow.md: When to use Task Flow, Reliable scheduled workflow pattern, Sync modes (Managed, Mirrored), Durable state and revision tracking, Cancel behavior, CLI commands, How flows relate to tasks | 500 | Task Flow: OpenClaw's durable scheduled-workflow primitive — when to use it, the reliable scheduled-workflow pattern, managed-vs-mirrored sync modes, durable state + revision tracking, cancel behavior, the CLI, and how flows relate to tasks. |
| 6 | `oc_automation_tasks_lifecycle.md` | procedure | tasks.md: TL;DR, Quick start, What creates a task, Task lifecycle, Delivery and notifications (Notification policies) | 650 | The OpenClaw task model: what a task is, what creates one, the task lifecycle (states/transitions), and delivery + notification policies for completed/failed tasks. |
| 7 | `oc_automation_tasks_management.md` | procedure | tasks.md: CLI reference, Chat task board (`/tasks`), Status integration (task pressure), Storage and maintenance (Where tasks live, Automatic maintenance), How tasks relate to other systems | 600 | Managing OpenClaw tasks: the `oc tasks` CLI, the in-chat `/tasks` board, status-line task-pressure integration, on-disk storage + automatic maintenance, and how tasks relate to cron, flows, and sessions. |

## Section Coverage Map

```
cron-jobs.md (13 H2 / 9 H3)
├── Quick start ───────────────────────────────────── → note 1 (oc_automation_cron_jobs_scheduling)
├── How cron works ────────────────────────────────── → note 1
├── Schedule types (+ H3 Day-of-month/week OR logic) ─ → note 1
├── Execution styles (H3 Command payloads, Payload options for isolated jobs) → note 1
├── Delivery and output ───────────────────────────── → note 1
├── Output language ───────────────────────────────── → note 1
├── CLI examples ──────────────────────────────────── → note 1
├── Managing jobs ─────────────────────────────────── → note 1
├── Webhooks (H3 Authentication) ──────────────────── → note 2 (oc_automation_cron_jobs_triggers_config)
├── Gmail PubSub integration (H3 Wizard setup, Gateway auto-start, Manual one-time setup, Gmail model override) → note 2
├── Configuration (H3 Command ladder) ─────────────── → note 2
└── Troubleshooting ───────────────────────────────── → note 2
hooks.md (12 H2 / 12 H3)
├── Choose the right surface ──────────────────────── → note 3 (oc_automation_hooks)
├── Quick start ───────────────────────────────────── → note 3
├── Event types ───────────────────────────────────── → note 3
├── Writing hooks (H3 Hook structure, HOOK.md format, Handler implementation, Event context highlights) → note 3
├── Hook discovery (H3 Hook packs) ────────────────── → note 3
├── Bundled hooks (H3 session-memory, bootstrap-extra-files, command-logger, compaction-notifier, boot-md) → note 3
├── Plugin hooks ──────────────────────────────────── → note 3
├── Configuration ─────────────────────────────────── → note 3
├── CLI reference ─────────────────────────────────── → note 3
├── Best practices ────────────────────────────────── → note 3
└── Troubleshooting (H3 not discovered/eligible/executing) → note 3
standing-orders.md (17 H2 / 15 H3)
├── Why standing orders ───────────────────────────── → note 4 (oc_automation_standing_orders)
├── How they work (H3 Execution steps, What NOT to do) → note 4
├── Anatomy of a standing order / Program: Weekly Status Report → note 4
├── Standing orders plus cron jobs ────────────────── → note 4
├── Examples / Program: Content & Social / Financial / System Monitoring (+ H3 examples 1-3, cycles, rules) → note 4
├── Execute-verify-report pattern (H3 Execution rules) → note 4
├── Multi-program architecture / Program 1-3 / Escalation Rules (H3 Response matrix) → note 4
└── Best practices (H3 Do, Avoid) ─────────────────── → note 4
taskflow.md (8 H2 / 2 H3)
├── When to use Task Flow ─────────────────────────── → note 5 (oc_automation_taskflow)
├── Reliable scheduled workflow pattern ───────────── → note 5
├── Sync modes (H3 Managed mode, Mirrored mode) ───── → note 5
├── Durable state and revision tracking ───────────── → note 5
├── Cancel behavior ───────────────────────────────── → note 5
├── CLI commands ──────────────────────────────────── → note 5
└── How flows relate to tasks ─────────────────────── → note 5
tasks.md (11 H2 / 3 H3)
├── TL;DR ─────────────────────────────────────────── → note 6 (oc_automation_tasks_lifecycle)
├── Quick start ───────────────────────────────────── → note 6
├── What creates a task ───────────────────────────── → note 6
├── Task lifecycle ────────────────────────────────── → note 6
├── Delivery and notifications (H3 Notification policies) → note 6
├── CLI reference ─────────────────────────────────── → note 7 (oc_automation_tasks_management)
├── Chat task board (`/tasks`) ────────────────────── → note 7
├── Status integration (task pressure) ────────────── → note 7
├── Storage and maintenance (H3 Where tasks live, Automatic maintenance) → note 7
└── How tasks relate to other systems ─────────────── → note 7
```
No orphaned H2/H3. CLI pages (`cli/cron`, `cli/hooks`, `cli/tasks`), webhooks tool/plugin pages, and concepts
(commitments/dreaming/queue/session/timezone) are linked, not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| cron-jobs.md (4,487w, 22 code, 13 H2) | notes 1 + 2 | ~1.8× the 2,500w cap; cleanly separates the time-scheduling+execution-styles+CLI procedure (note 1) from the event-trigger surfaces (webhook + Gmail PubSub) + configuration + troubleshooting (note 2). Each ≤700w / ≤6 code. |
| tasks.md (2,712w, 16 code, 11 H2) | notes 6 + 7 | exceeds the 2,500w cap; splits the task-model/lifecycle/delivery procedure (note 6) from the management surfaces — CLI, chat board, status pressure, storage/maintenance (note 7). Each ≤650w / ≤6 code. |

hooks.md (1,950w), standing-orders.md (1,396w), and taskflow.md (1,016w) are each a single note (under caps, one BB).

## Summary Statistics & Building Block Distribution

- Source pages: **5** (11,561 measured words, 65 code fences). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×5** (notes 1, 2, 3, 6, 7) · **argument ×1** (note 4, standing-orders = a
  convention/usage-discipline page) · **concept ×1** (note 5, taskflow = the durable-flow model) — one BB per note.
- Est. digest words ~4,400 (avg ~550/note); all ≤700w. The 65 source fences distribute across notes; config/CLI
  snippets reproduced selectively (verbatim) so each note stays ≤6 code blocks.
- Cross-refs: the per-note related-notes mapping is **LOCKED at xref-augment 2026-06-21** at the RAISED floors
  (**≥8 relevancy-selected `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under
  [`## Per-Note Related Notes Mapping`](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21) below.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read source 2026-06-21; no
> series)** and count toward the 10-doc floor. Render in each digest note's `## Related Notes` as
> `- [Name](relpath.md) — what it is; relevance: why THIS note`. Relative paths from
> `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`; snippet →
> `../../code_snippets/snippet_Y.md`; sibling → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
> `../../../areas/code_repos/repo_Y.md`; entry → `../../../0_entry_points/entry_Y.md`.

### oc_automation_cron_jobs_scheduling (10t · 11s · 11d)

**Terms**
- [Cron](../../term_dictionary/term_cron.md) — time-based job scheduler; relevance: THE subject — 5/6-field syntax, `--at`/`--every`/`--cron` schedule types, `--tz`.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — the field grammar of a cron string; relevance: directly documents the Schedule-types table + DOM/DOW OR-logic (croner) section.
- [Scheduling Algorithms](../../term_dictionary/term_scheduling_algorithms.md) — how jobs are picked/staggered for execution; relevance: top-of-hour auto-stagger, `--exact`/`--stagger`, `maxConcurrentRuns` dispatch.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating recurring execution; relevance: the Gateway scheduler orchestrates wake lanes + isolated/main execution styles.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-run semantics; relevance: isolated re-runnable jobs, `--run-id` duplicate-in-flight guard, one-shot auto-delete.
- [Subagent](../../term_dictionary/term_subagent.md) — a spawned child agent run; relevance: isolated jobs run a fresh dedicated `cron:<jobId>` agent turn.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution context; relevance: isolated execution style + `--light-context`/`--tools` restriction of the run.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — react to events; relevance: cron is the time-trigger half of OpenClaw automation (system events, `--wake now`).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents acting unattended; relevance: scheduled jobs run the agent without a human present.
- [LLM](../../term_dictionary/term_llm.md) — the model a job invokes; relevance: `--model`/`--thinking` overrides, model-selection precedence, fallback chains, fast mode.

**Docs**
- [oc_automation_cron_jobs_triggers_config](oc_automation_cron_jobs_triggers_config.md) — webhook/PubSub triggers (planned, this series); relevance: continues the same job model with event triggers + config.
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task model (planned, this series); relevance: every cron execution creates a background-task record.
- [oc_automation_taskflow](oc_automation_taskflow.md) — durable flows (planned, this series); relevance: cron vs durable scheduled workflow trade-off.
- [cc_desktop_scheduled_tasks](../claude_code/cc_desktop_scheduled_tasks.md) — Claude Code scheduled tasks; relevance: closest sibling-tool scheduled-task analog (create/list/run).
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — isolated-vs-attached run model; relevance: direct analog of OpenClaw's main/isolated/current/custom execution styles.
- [cc_scheduling_options_comparison](../claude_code/cc_scheduling_options_comparison.md) — cron-vs-loop choice; relevance: same "which scheduling primitive" decision this note frames.
- [hermes_cron_scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron schedule types; relevance: the implemented schedule-type semantics behind the same syntax table.
- [hermes_cron_internals](../hermes_agent/hermes_cron_internals.md) — Hermes cron scheduler internals; relevance: how a Gateway-hosted cron service persists + fires jobs (the "How cron works" section).
- [hermes_guide_automate_with_cron](../hermes_agent/hermes_guide_automate_with_cron.md) — task-oriented cron guide; relevance: the Quick-start / CLI-examples workflow analog.
- [hermes_automation_blueprints_scheduled](../hermes_agent/hermes_automation_blueprints_scheduled.md) — scheduled-automation blueprints; relevance: morning-brief / recurring-isolated-job patterns this note's CLI examples show.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway service; relevance: hosts the in-Gateway cron scheduler this note documents.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — Hermes agent; relevance: sibling implementation whose cron snippets are cited here.

**Snippets**
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — gateway cron service + notification post; relevance: the service that fires jobs + delivers output, the heart of "How cron works".
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — a concrete recurring cron job; relevance: real scheduled maintenance-job example.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — OS scheduled-task argv render; relevance: the platform scheduling layer under external `openclaw agent` cron.
- [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — cron scheduler tick loop; relevance: how due jobs are detected + dispatched each tick.
- [snippet_hermes_agent_cron_job_schema](../../code_snippets/snippet_hermes_agent_cron_job_schema.md) — cron job schema; relevance: the stored job shape (schedule, session, delivery) behind the CLI flags.
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — run-job execution; relevance: isolated/main run execution, the Execution-styles section.
- [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — run-job setup; relevance: fresh-session bootstrap + payload options for isolated jobs.
- [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — schedule helpers; relevance: next-run computation + timezone/stagger handling.
- [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — `cron` CLI surface; relevance: the create/list/get/show CLI examples this note reproduces.

### oc_automation_cron_jobs_triggers_config (10t · 11s · 10d)

**Terms**
- [Webhook](../../term_dictionary/term_webhook.md) — inbound HTTP event endpoint; relevance: THE subject — `/hooks/wake`, `/hooks/agent`, mapped hooks, `--webhook` output.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — event triggers; relevance: webhooks + Gmail PubSub are the event-trigger half vs time-cron.
- [Pub/Sub](../../term_dictionary/term_pub_sub.md) — publish-subscribe messaging; relevance: directly documents the Gmail PubSub integration (topic, push subscription, watch).
- [Authentication](../../term_dictionary/term_authentication.md) — verifying request identity; relevance: the Webhooks→Authentication section (Bearer/`x-openclaw-token`, query tokens rejected).
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization; relevance: Gmail PubSub uses Google OAuth via `gog`/`gcloud`.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored access credential; relevance: the Google OAuth client/token `gog` uses for the watch.
- [Cron](../../term_dictionary/term_cron.md) — the scheduler; relevance: triggered jobs create the same cron-style job records (`--webhook` is a cron delivery mode).
- [Idempotency](../../term_dictionary/term_idempotency.md) — replay safety; relevance: webhook replay/dedup is the safety guard for external triggers.
- [LLM](../../term_dictionary/term_llm.md) — the model selected; relevance: the Gmail model override (`hooks.gmail.model`) picks the model for triggered runs.
- [Slack](../../term_dictionary/term_slack.md) — chat delivery target; relevance: a representative announce/notification channel for triggered jobs.

**Docs**
- [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md) — base cron job model (planned, this series); relevance: the job model these triggers extend.
- [oc_automation_hooks](oc_automation_hooks.md) — internal lifecycle hooks (planned, this series); relevance: the sibling event surface (and `Webhooks` is cross-linked from hooks.md).
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task model (planned, this series); relevance: triggered jobs surface as task records + notifications.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event hooks; relevance: inbound HTTP/webhook event wiring analog.
- [hermes_messaging_email](../hermes_agent/hermes_messaging_email.md) — Hermes email/inbox integration; relevance: the Gmail-inbox-trigger + Gmail PubSub watch integration analog (mailbox push → triggered agent run).
- [cc_routine_triggers](../claude_code/cc_routine_triggers.md) — Claude Code routine triggers; relevance: event/schedule trigger taxonomy analog.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway ingress architecture; relevance: how external HTTP requests reach the gateway (webhook ingress).
- [hermes_guide_automate_with_cron](../hermes_agent/hermes_guide_automate_with_cron.md) — cron automation guide; relevance: trigger-to-job wiring workflow analog.
- [cc_create_routine](../claude_code/cc_create_routine.md) — creating a triggered routine; relevance: wizard-style setup parallel to `webhooks gmail setup`.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops/config; relevance: the configuration command-ladder + troubleshooting analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway; relevance: webhook ingress + Gmail watcher + cron service all live here.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — Hermes; relevance: sibling webhook/platform snippets cited here.

**Snippets**
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook signature verify; relevance: the auth pattern of Webhooks→Authentication (token/signature check).
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay dedup cache; relevance: the idempotency guard against replayed external triggers.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway hooks request handler; relevance: the `POST /hooks/*` dispatch that resolves wake/agent/mapped actions.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hooks config payload; relevance: the `hooks.enabled/token/path/mappings` config this note's Webhooks block shows.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + notifications; relevance: webhook/announce delivery of triggered-job output.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — platform webhook handler; relevance: inbound webhook ingestion analog.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — Graph/Gmail-style push webhook; relevance: external mailbox push-notification integration analog of Gmail PubSub.
- [snippet_hermes_agent_skills_email](../../code_snippets/snippet_hermes_agent_skills_email.md) — email integration; relevance: Gmail inbox-trigger handling analog.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — devops webhook recipe; relevance: a concrete webhook-to-action mapping example.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron job CRUD; relevance: `--webhook` cron-add/edit + clear-routing flags this note's Managing-jobs config touches.
- [snippet_hermes_agent_cron_job_validate](../../code_snippets/snippet_hermes_agent_cron_job_validate.md) — cron job validation; relevance: model-not-allowed validation error + strict-fallback config behavior.

### oc_automation_hooks (10t · 11s · 11d)

**Terms**
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — OpenClaw internal hooks; relevance: THE subject — HOOK.md + handler scripts firing on Gateway events.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — events emitted across an agent run; relevance: the Event-types table (`command:*`, `session:*`, `gateway:*`, `message:*`).
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — react to events; relevance: hooks are the event-driven extension surface inside the Gateway.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the typed plugin API; relevance: the Plugin-hooks section (`api.on(...)`, typed contracts vs file hooks).
- [Compaction](../../term_dictionary/term_compaction.md) — transcript summarization; relevance: the `compaction-notifier` bundled hook + `session:compact:before/after` events.
- [Chain of Responsibility](../../term_dictionary/term_chain_of_responsibility.md) — ordered handler pipeline; relevance: hook discovery precedence + ordered middleware/block semantics of typed hooks.
- [Subagent](../../term_dictionary/term_subagent.md) — child agent run; relevance: `before_agent_finalize` and lifecycle hooks observe/gate agent/subagent runs.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: typed `before_tool_call` hooks observe/guard tool calls.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: hooks interplay with MCP tool events + plugin-bundled hooks.
- [PII](../../term_dictionary/term_pii.md) — sensitive data; relevance: guardrail/audit hook recipes (command-logger, audit) handle sensitive content.

**Docs**
- [oc_automation_cron_jobs_triggers_config](oc_automation_cron_jobs_triggers_config.md) — webhooks (planned, this series); relevance: hooks.md explicitly cross-links Webhooks as the external counterpart.
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task lifecycle (planned, this series); relevance: lifecycle events hooks can observe map to task transitions.
- [oc_automation_standing_orders](oc_automation_standing_orders.md) — standing orders (planned, this series); relevance: the "choose the right surface" alternative to hooks.
- [cc_hooks_overview](../claude_code/cc_hooks_overview.md) — Claude Code hooks overview; relevance: the closest sibling-tool hooks model.
- [cc_hook_events_catalog](../claude_code/cc_hook_events_catalog.md) — hook event catalog; relevance: direct analog of the Event-types table.
- [cc_hooks_guardrail_and_audit_recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit recipes; relevance: best-practices + audit-hook recipe analog.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session lifecycle hook events; relevance: `session:*`/`command:*`/`gateway:*` lifecycle analog.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event hooks; relevance: file-based event-hook system parallel.
- [hermes_plugin_hook_reference](../hermes_agent/hermes_plugin_hook_reference.md) — typed plugin hook reference; relevance: direct analog of OpenClaw's typed plugin-hook surface.
- [pi_extensions_events_lifecycle](../pi/pi_extensions_events_lifecycle.md) — pi extension lifecycle events; relevance: another coding-agent lifecycle-hook model for comparison.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway; relevance: internal hook discovery + dispatch runs inside the Gateway.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills/packs; relevance: hook packs are discovered/installed alongside skills/plugins.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — Hermes; relevance: sibling hook-handler snippets cited here.

**Snippets**
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hooks request handler; relevance: the dispatch path that resolves + runs eligible hooks.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hooks config payload; relevance: the `hooks.internal.entries`/`extraDirs` config schema this note shows.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session-reset hook helpers; relevance: `command:new`/`command:reset` lifecycle hook handling (session-memory).
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hooks system; relevance: hook discovery + handler invocation analog.
- [snippet_hermes_agent_core_shell_hooks_callback](../../code_snippets/snippet_hermes_agent_core_shell_hooks_callback.md) — shell hook callback; relevance: the handler-implementation pattern (event → side effect).
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — startup/restart sequence; relevance: `gateway:startup`/`gateway:pre-restart`/`gateway:shutdown` event firing context.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach startup; relevance: "After channels start and hooks are loaded" — the `gateway:startup` boundary.
- [snippet_hermes_agent_conv_loop_post_api_hook](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_hook.md) — post-API conversation hook; relevance: in-loop typed-hook (around-model-turn) analog.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: the block/guard semantics of typed `before_tool_call` hooks.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: a guardrail-hook recipe (block tools) example.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: `session:patch` event context (changed session fields).

### oc_automation_standing_orders (10t · 10s · 11d)

**Terms**
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — directing agent behavior; relevance: standing orders steer recurring autonomous behavior via persistent prompts.
- [Steering Files](../../term_dictionary/term_steering_files.md) — persistent instruction files; relevance: standing orders live in `AGENTS.md`/`standing-orders.md` bootstrap files.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — the auto-injected agent instruction file; relevance: the recommended home for standing orders (auto-injected every session).
- [Persistent Goal](../../term_dictionary/term_persistent_goal.md) — a standing objective the agent pursues; relevance: a "program" is a persistent operating authority/goal.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — expanding autonomy as trust builds; relevance: the "start narrow, expand as trust builds" + approval-gate best practice.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval points; relevance: approval gates + escalation rules ("when to stop and ask").
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent-run pattern; relevance: the execute-verify-report loop + multi-program architecture.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating concerns; relevance: multi-program architecture with per-program boundaries/cadences.
- [Cron](../../term_dictionary/term_cron.md) — time-based enforcement; relevance: "Standing orders plus cron" — cron is the trigger that enforces standing-order cadence.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents executing unattended; relevance: the agent self-executes programs within granted authority.

**Docs**
- [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md) — cron scheduling (planned, this series); relevance: the cadence engine standing orders pair with.
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task model (planned, this series); relevance: program executions produce background tasks.
- [oc_automation_hooks](oc_automation_hooks.md) — hooks (planned, this series); relevance: the "choose the right surface" alternative for event-driven programs.
- [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — recurring self-execution loop; relevance: the closest analog of agent self-executing recurring work.
- [cc_goal_command](../claude_code/cc_goal_command.md) — persistent goal command; relevance: standing authority / persistent-goal analog.
- [hermes_guide_daily_briefing_bot](../hermes_agent/hermes_guide_daily_briefing_bot.md) — daily-briefing program; relevance: a concrete standing-order-style recurring program (weekly status report analog).
- [hermes_automation_blueprints_scheduled](../hermes_agent/hermes_automation_blueprints_scheduled.md) — scheduled blueprints; relevance: the content/finance/monitoring program patterns this note's Examples mirror.
- [hermes_skill_curator](../hermes_agent/hermes_skill_curator.md) — autonomous self-maintenance program; relevance: a recurring autonomous-program-with-escalation analog.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation/authority patterns; relevance: scope/authority/escalation boundary patterns.
- [cc_routines_overview](../claude_code/cc_routines_overview.md) — routines (recurring agent programs); relevance: routine = scheduled standing-program analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the runtime that loads `AGENTS.md` standing orders + executes programs.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills/prompts; relevance: program/skill prompts packaged for reuse.

**Snippets**
- [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — cron run setup; relevance: a cron job firing "execute per standing orders" (the cron-prompt-references-standing-order pattern).
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: approval-gate enforcement for high-risk program actions.
- [snippet_hermes_agent_skills_hermes_agent](../../code_snippets/snippet_hermes_agent_skills_hermes_agent.md) — agent skill program; relevance: a packaged autonomous-program skill analog.
- [snippet_hermes_agent_gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md) — status snapshot; relevance: the System-Monitoring program's health-check + response-matrix analog.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — delivery of results; relevance: "report results to owner via configured channel" step.
- [snippet_hermes_agent_skills_email](../../code_snippets/snippet_hermes_agent_skills_email.md) — email/inbox processing; relevance: the daily-inbox-triage standing-order example.

### oc_automation_taskflow (10t · 10s · 11d)

**Terms**
- [DAG](../../term_dictionary/term_dag.md) — directed multi-step graph; relevance: a flow is a directed sequential/branching workflow (A→B→C steps).
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating multi-step work; relevance: Task Flow is the orchestration substrate above background tasks.
- [Step Functions](../../term_dictionary/term_step_functions.md) — AWS durable workflow service; relevance: closest managed-durable-workflow analog (managed mode, durable state).
- [Amazon States Language](../../term_dictionary/term_asl.md) — Step Functions workflow DSL; relevance: the `.lobster`/YAML step-definition with conditions/approval is an ASL-style state machine analog.
- [SWF](../../term_dictionary/term_swf.md) — Simple Workflow Service; relevance: durable, restart-surviving, revision-tracked workflow execution analog.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe replay; relevance: durable state + revision tracking enable conflict detection + safe resume.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — schedule/event-triggered runs; relevance: flows are kicked off by cron/CLI/other sources (mirrored mode observes them).
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — periodic durable state save; relevance: SQLite WAL checkpoints + durable progress across gateway restarts.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued step processing; relevance: child tasks/steps are queued + driven to completion.
- [Cron](../../term_dictionary/term_cron.md) — the scheduler; relevance: flows are the durable upgrade of raw cron (the When-to-use table).

**Docs**
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task model (planned, this series); relevance: "How flows relate to tasks" — flows coordinate the task ledger.
- [oc_automation_tasks_management](oc_automation_tasks_management.md) — task CLI/management (planned, this series); relevance: `openclaw tasks flow` CLI parallels `openclaw tasks` CLI.
- [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md) — cron (planned, this series); relevance: cron-vs-durable-flow trade-off (When-to-use table).
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — durable execution model; relevance: scheduled durable-run execution analog.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — dynamic multi-step workflows; relevance: multi-step pipeline-of-agents analog of managed-mode flows.
- [cc_create_and_run_workflows](../claude_code/cc_create_and_run_workflows.md) — authoring/running workflows; relevance: the reliable-scheduled-workflow authoring pattern analog.
- [cc_workflow_recipes](../claude_code/cc_workflow_recipes.md) — workflow recipes; relevance: market-intel-brief style multi-step reliable-workflow recipes.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — delegated multi-task runs; relevance: a flow driving multiple child tasks over its lifetime.
- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — work orchestrator; relevance: managed-mode flow-drives-tasks orchestration analog.
- [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel agent runs; relevance: mirrored-mode independent-tasks-as-one-flow analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway; relevance: flow registry (SQLite + WAL) + scheduling live in the Gateway.

**Snippets**
- [snippet_stepfn_wait_for_task_token](../../code_snippets/snippet_stepfn_wait_for_task_token.md) — durable wait/resume; relevance: the wait-for-completion-then-advance + approval-gate (`approval: required`) pattern.
- [snippet_stepfn_retry_backoff](../../code_snippets/snippet_stepfn_retry_backoff.md) — workflow retry/backoff; relevance: durable-workflow retry semantics analog.
- [snippet_stepfn_choice_multi_branch](../../code_snippets/snippet_stepfn_choice_multi_branch.md) — branch on condition; relevance: the `condition: $approve.approved` branching step.
- [snippet_stepfn_multi_step_pipeline](../../code_snippets/snippet_stepfn_multi_step_pipeline.md) — multi-step pipeline; relevance: the preflight→collect→summarize→approve→deliver pipeline shape.

### oc_automation_tasks_lifecycle (10t · 11s · 11d)

**Terms**
- [Subagent](../../term_dictionary/term_subagent.md) — backgrounded child agent; relevance: subagent spawns are a primary task source; a task tracks a detached agent run.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — unattended agent work; relevance: tasks are the ledger of detached unattended work.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — run start/end/error events; relevance: agent lifecycle events automatically drive `queued→running→terminal` transitions.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — push-driven completion; relevance: completion is push-based (heartbeat wake / direct notify), not polling.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — notify-on-completion; relevance: notification policies surface results to the human.
- [Idempotency](../../term_dictionary/term_idempotency.md) — no-downgrade terminal state; relevance: a later success signal does not downgrade an already-terminal `failed`/`lost`.
- [LLM](../../term_dictionary/term_llm.md) — the model a task runs; relevance: ACP/subagent/cron tasks invoke a model turn.
- [Orchestration](../../term_dictionary/term_orchestration.md) — runtime-managed units; relevance: a task is a unit the runtime orchestrates + reconciles.
- [Cron](../../term_dictionary/term_cron.md) — a task source; relevance: every cron execution creates a task record (`silent` default).
- [Silence Token](../../term_dictionary/term_silence_token.md) — the `NO_REPLY` suppression token; relevance: silent-policy + `NO_REPLY` suppression of completion delivery.

**Docs**
- [oc_automation_tasks_management](oc_automation_tasks_management.md) — task CLI/board/storage (planned, this series); relevance: the management continuation of this model.
- [oc_automation_taskflow](oc_automation_taskflow.md) — Task Flow (planned, this series); relevance: flows coordinate tasks (How-flows-relate-to-tasks).
- [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md) — cron (planned, this series); relevance: cron creates tasks (What-creates-a-task).
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — dispatching background agents; relevance: closest analog of detached background-run tracking.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting background runs; relevance: child-session backing of a running task.
- [cc_sdk_subagents_lifecycle](../claude_code/cc_sdk_subagents_lifecycle.md) — subagent lifecycle; relevance: subagent-spawn task lifecycle states analog.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — subagent delegation; relevance: subagent task creation + completion delivery analog.
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — agent run loop; relevance: the run whose start/end/error drives task status.
- [band_agent_lifecycle](../band/band_agent_lifecycle.md) — agent lifecycle states; relevance: a generic queued→running→terminal lifecycle model for comparison.
- [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — working with subagents; relevance: subagent-as-task usage analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: subagent/ACP task runtime that creates + finalizes task records.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — Hermes; relevance: sibling runner/supervisor snippets cited here.

**Snippets**
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — completion notifications; relevance: direct vs session-queued completion delivery paths.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent registry lifecycle; relevance: subagent-task creation + terminal tracking.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP/subagent spawn; relevance: "What creates a task" — ACP spawn + subagent spawn sources.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — subagent completion announce; relevance: subagent completion delivery (final-descendant-output preference).
- [snippet_hermes_agent_gw_runner_supervisor](../../code_snippets/snippet_hermes_agent_gw_runner_supervisor.md) — run supervisor; relevance: timeout/abort → `timed_out` finalization + watchdog behavior.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — result delivery; relevance: the requesterOrigin direct-delivery path.
- [snippet_hermes_agent_tools_mcp_notifications](../../code_snippets/snippet_hermes_agent_tools_mcp_notifications.md) — notifications; relevance: the notify-policy delivery mechanism (`done_only`/`state_changes`/`silent`).

### oc_automation_tasks_management (10t · 10s · 11d)

**Terms**
- [Subagent](../../term_dictionary/term_subagent.md) — backgrounded agent; relevance: managed tasks are mostly backgrounded subagent/ACP runs.
- [Message Queue](../../term_dictionary/term_message_queue.md) — pending-work queue; relevance: the `/tasks` board + queued/running counts are a task queue view.
- [Orchestration](../../term_dictionary/term_orchestration.md) — managing concurrent units; relevance: managing/reconciling concurrent tasks across runtimes.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — pressure/concurrency control; relevance: status-line "task pressure" (active/failures/byRuntime) as a load signal.
- [Idempotency](../../term_dictionary/term_idempotency.md) — dedup + cleanup safety; relevance: storage maintenance dedup + idempotent prune/reconcile.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — durable record store; relevance: tasks persist in SQLite (`runs.sqlite`) with WAL durability.
- [Cron](../../term_dictionary/term_cron.md) — a related runtime; relevance: `byRuntime` breakdown + "tasks and cron" relation; stale cron session-row cleanup.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — periodic WAL checkpoint; relevance: bounded WAL via PASSIVE/TRUNCATE checkpoints in storage/maintenance.
- [Event Ledger](../../term_dictionary/term_event_ledger.md) — activity-record log; relevance: tasks are the activity ledger of detached work this note manages.
- [Slack](../../term_dictionary/term_slack.md) — chat surface; relevance: the in-chat `/tasks` board surface.

**Docs**
- [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md) — task model (planned, this series); relevance: the lifecycle this note's tools manage.
- [oc_automation_taskflow](oc_automation_taskflow.md) — Task Flow (planned, this series); relevance: `openclaw tasks flow` CLI parallels `openclaw tasks` CLI.
- [oc_automation_cron_jobs_scheduling](oc_automation_cron_jobs_scheduling.md) — cron (planned, this series); relevance: shared CLI ergonomics + cron-task relation.
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — managing background runs; relevance: listing/cancelling/auditing background runs analog.
- [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — agent view/monitor; relevance: the `/tasks` board + status integration analog.
- [cc_subagent_statusline](../claude_code/cc_subagent_statusline.md) — subagent status line; relevance: the status-line task-pressure summary analog.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: audit/maintenance/cleanup operations analog.
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent task board; relevance: the chat task-board (`/tasks`) analog.
- [hermes_cli_session_background](../hermes_agent/hermes_cli_session_background.md) — background-session CLI; relevance: the `openclaw tasks list/show/cancel` CLI-reference analog.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — background run hosting; relevance: where tasks live + storage/maintenance analog.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — chat/app UI; relevance: the in-chat `/tasks` board surface lives here.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: task↔session relation (`childSessionKey`/`requesterSessionKey`) + stale session-row cleanup.

**Snippets**
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — process kill-tree; relevance: `openclaw tasks cancel` killing a child session/process.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — kill-tree helper; relevance: the cancel path tearing down a running task's process tree.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: reconciliation of whether a task still has authoritative runtime backing.
- [snippet_hermes_agent_gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md) — status snapshot; relevance: the `openclaw status` task-pressure summary (active/failures/byRuntime).
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: the `tasks.list/show/cancel/notify` RPC surface behind the CLI.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + sweep; relevance: stale cron session-row cleanup in automatic maintenance.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — maintenance/repair job; relevance: the automatic-maintenance sweeper (reconcile/cleanup/prune) analog.

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| cron job / schedule types / DOM-DOW OR logic | OpenClaw cron vocabulary → digested in `oc_automation_cron_jobs_scheduling` (concept inline in the doc note); link existing `term_cron`. NOT a new term. |
| execution style (isolated vs in-session) / command payload | Doc-internal vocabulary → `oc_automation_cron_jobs_scheduling`; link `term_subagent`/`term_sandbox`. NOT a new term. |
| webhook trigger / webhook authentication | Documented in `oc_automation_cron_jobs_triggers_config`; link existing `term_webhook`, `term_authentication`. NOT a new term. |
| Gmail PubSub integration / Gmail model override | OpenClaw-specific integration → `oc_automation_cron_jobs_triggers_config`; link `term_oauth`/`term_oauth_token`/`term_event_driven_architecture` (no `term_pubsub`/`term_gmail` note exists, and these are not cross-cutting reusable terms — they are a single integration). NOT a new term. |
| hook / hook event types / HOOK.md / handler / hook pack | OpenClaw hook vocabulary → `oc_automation_hooks`; link `term_event_driven_architecture` (no generic `term_hook` note; OpenClaw hooks are product-specific, mirror the `cc_hooks_*` doc-note treatment). NOT a new term. |
| bundled hooks (session-memory, compaction-notifier, boot-md, …) | Doc-internal names → `oc_automation_hooks`; link `term_compaction`. NOT a new term. |
| standing order / program / execute-verify-report / multi-program architecture | OpenClaw convention vocabulary → `oc_automation_standing_orders`; link `term_agent_steering`/`term_steering_files`/`term_orchestration`/`term_human_in_the_loop`. NOT a new term. |
| Task Flow / managed vs mirrored sync / revision tracking | OpenClaw durable-flow vocabulary → `oc_automation_taskflow`; link `term_dag`/`term_orchestration`/`term_step_functions`/`term_idempotency`. NOT a new term. |
| task / task lifecycle / task pressure / task board / notification policy | OpenClaw task vocabulary → `oc_automation_tasks_lifecycle` + `oc_automation_tasks_management`; link `term_subagent`/`term_message_queue`/`term_human_in_the_loop`/`term_rate_limiting`. NOT a new term. |

**Result: 0 new `term_dictionary` captures.** All automation vocabulary is the subject of an `oc_*` doc note (per
the master's `claude_code`/`pi` precedent — concept digested in the doc note, never inlined as a term definition);
only existing terms are linked. No genuinely cross-cutting, vault-reusable term lacking both a doc-page home AND an
existing note was found. Augment Step 2d re-scans to confirm. (If augment surfaces a true new cross-cutting term,
e.g. a generic "standing order"/"durable workflow" concept the wider vault would reuse, capture via
`/tessellum-capture-term-note` and add to `acronym_glossary_workflows.md` — expected near-0.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** au01 authors zero `term_dictionary` notes. (Inherited from master: any new term would require

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format (YAML field order + forbidden fields; H1/`## Overview`/`## Related Notes`/`## References`/footer; ≤400L/≤2500w/≤6 code; one BB) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no claim absent from source) | diff each note vs `inbox/openclaw_docs/automation/<page>.md` |
| G3 | Density + Coverage (within caps; every mapped H2/H3 covered; no over-compression) | re-read source + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevancy terms + repos/siblings/docs/snippets, each with relevance statement, indexed link form) | per-note Related Notes vs Candidate Cross-References |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` + reindex |
| G7 | Discoverability (every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`) | inlink map below + `entry_openclaw_docs.md` |
| G8 | In-degree ≥1 (anti-island) | query `note_links` after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_automation_cron_jobs_scheduling oc_automation_cron_jobs_triggers_config oc_automation_hooks oc_automation_standing_orders oc_automation_taskflow oc_automation_tasks_lifecycle oc_automation_tasks_management"

DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r sec; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION in $n: $sec"
  done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps (body words, code fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G5 ghost-reference: every linked oc_*/term_*/repo_*/cc_*/snippet_*/entry_* target exists OR is a planned sibling (oc_ in this NOTES set)
  grep -oE '\]\(([^)]+)\.md\)' "$f" | sed -E 's/.*\/([^/)]+)\.md\)/\1/' | sort -u | while read -r tgt; do
    case "$tgt" in
      oc_*) echo "$NOTES" | grep -qw "$tgt" || { sqlite3 "$DB" "SELECT 1 FROM notes WHERE note_name='$tgt'" | grep -q 1 || echo "GHOST(oc) in $n -> $tgt"; } ;;
      *) sqlite3 "$DB" "SELECT 1 FROM notes WHERE note_name='$tgt'" | grep -q 1 || echo "GHOST in $n -> $tgt" ;;
    esac
  done
done

# whole-folder YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G6 broken links + reindex handled by /tessellum-fix-broken-links + bash scripts/update_notes_database.sh --force
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_automation_cron_jobs_scheduling | procedure | 700 | ≤6 (from 22, selective) | ✅ |
| 2 | oc_automation_cron_jobs_triggers_config | procedure | 650 | ≤6 (from 22, selective) | ✅ |
| 3 | oc_automation_hooks | procedure | 700 | ≤6 (from 14, selective) | ✅ |
| 4 | oc_automation_standing_orders | argument | 600 | ≤6 (from 8) | ✅ |
| 5 | oc_automation_taskflow | concept | 500 | ≤5 (from 5) | ✅ |
| 6 | oc_automation_tasks_lifecycle | procedure | 650 | ≤6 (from 16, selective) | ✅ |
| 7 | oc_automation_tasks_management | procedure | 600 | ≤6 (from 16, selective) | ✅ |

No note approaches the 2,500w / ≤6-code / 400-line caps. The two code-heavy pages (cron-jobs 22, tasks 16) were
split so each note reproduces only the load-bearing config/CLI snippets verbatim (≤6 each).

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `0_entry_points/entry_openclaw_docs.md` (created as a master W1 pre-step before the first
sub-plan executes), under an **"Automation"** section (cron · hooks · standing orders · task flow · tasks). Each new
note receives its entry-point back-link at finalization. No standalone entry point for au01 (8 notes < the 30-note
threshold; the corpus hub `entry_openclaw_docs.md` is the shared series hub per master).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 — every new note gets ≥1):

- `entry_openclaw_docs.md` (master pre-step) → **all 8** notes (the guaranteed anti-island inbound link).
- `term_cron` → notes 1, 2, 4, 5, 6, 7 (the cron term is the natural hub for the scheduling/flow/task notes).
- `term_webhook` → note 2; `term_event_driven_architecture` → notes 2, 3, 5; `term_subagent` → notes 1, 3, 6, 7.
- `term_agent_steering` + `term_steering_files` → note 4; `term_dag` + `term_step_functions` → note 5;
  `term_message_queue` → note 7.
- `repo_openclaw_gateway` → notes 1, 2, 3 (gateway hosts cron/webhook/hook dispatch); `repo_openclaw_agents` →

## Pacing Rules (inherited from master)

Single phase, 8 notes — well under the ~30-agent fan-out cap. Embed the note manifest in the workflow script;
re-read each source page before authoring (config/CLI snippets verbatim); one BB per note. `git pull --rebase
--autostash origin main` first; commit + push the phase as one cycle (no Claude co-author trailer). Reindex
incrementally; verify `note_links` populated + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** xref-augment — re-read all 5 source pages under `inbox/openclaw_docs/automation/`
(cron-jobs, hooks, standing-orders, taskflow, tasks) and replaced the PLAN-stage `## Candidate Cross-References`
section with a LOCKED `## Per-Note Related Notes Mapping` at RAISED FLOORS (≥8 terms · ≥10 snippets · ≥10 docs per

**What was locked (per-note counts — terms / snippets / docs / repos):**

| # | Note | Terms | Snippets | Docs | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---|---:|---:|---:|---:|---|
| 1 | oc_automation_cron_jobs_scheduling | 10 | 11 | 11 | 2 | ✅ |
| 2 | oc_automation_cron_jobs_triggers_config | 10 | 11 | 10 | 2 | ✅ |
| 3 | oc_automation_hooks | 10 | 11 | 11 | 3 | ✅ |
| 4 | oc_automation_standing_orders | 10 | 10 | 11 | 3 | ✅ |
| 5 | oc_automation_taskflow | 10 | 10 | 11 | 3 | ✅ |
| 6 | oc_automation_tasks_lifecycle | 10 | 11 | 11 | 3 | ✅ |
| 7 | oc_automation_tasks_management | 10 | 10 | 11 | 3 | ✅ |

  (one pass via `SELECT 1 FROM notes WHERE note_name=?`), 8 planned (7 sibling `oc_*` + `entry_openclaw_docs`),
- **Relevance discipline:** the re-read upgraded the mapping substantially over the plan-stage candidates. Newly
  surfaced highly-relevant existing notes pulled in (not in the original candidate pool): terms
  `term_cron_expression`, `term_pub_sub` (Gmail PubSub home), `term_gateway_hooks`, `term_agent_lifecycle_event`,
  `term_silence_token` (`NO_REPLY` suppression), `term_event_ledger`, `term_append_only_state`,
  `term_scheduling_algorithms`, `term_persistent_goal`, `term_agents_md`, `term_graduated_trust`,
  `term_agentic_workflow`, `term_asl`, `term_swf`, `term_regular_checkpointing`, `term_chain_of_responsibility`,
  `snippet_stepfn_*` families; and the `hermes_cron_*`, `hermes_event_hooks`/`hermes_plugin_hook_reference`,

**New-term candidates (Step 2d re-scan):** **NONE → 0 new `term_dictionary` captures** (unchanged from plan). The
re-read surfaced OpenClaw automation vocabulary — execute-verify-report, task pressure, managed/mirrored sync,
isolated/in-session execution style, command payloads, bundled hooks, Gmail PubSub. Every one is either (a) the
subject of an `oc_*` doc note in this series (per the master `claude_code`/`pi` precedent — digested in the doc
note, never inlined as a term), or (b) already covered by an EXISTING term note that is now LINKED:
- "Gmail PubSub / publish-subscribe" → existing `term_pub_sub` (linked in note 2). Best-fit glossary if ever
  promoted: `acronym_glossary_workflows.md` — **not triggered** (note already exists).
- "task pressure / concurrency control" → existing `term_rate_limiting` (linked in note 7).
- "execute-verify-report / standing-order program" → usage discipline, not a vault-reusable term; owned by
  `oc_automation_standing_orders`; existing `term_agentic_workflow` + `term_persistent_goal` linked.
- "managed/mirrored durable flow" → owned by `oc_automation_taskflow`; existing `term_asl` + `term_swf` +
  `term_step_functions` linked as durable-workflow analogs.
No genuinely cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note was found →
Term-Note Authoring Requirements remains **N/A (0 new terms)**.

**Issues / notes:** none blocking. The plan's per-phase GATE table (G1–G9), Undigested Terms Plan, Entry Point
Decision, Inlinks map, Density Re-Assessment, and Validation Scripts were already present from the plan stage and
were re-verified intact during this pass.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

PLAN REVIEW — FINAL SIGN-OFF · Plan: `plan_digest_openclaw_docs_au01.md` · Date: 2026-06-21

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, per-link relevance, indexed form) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 7 notes ≥10t·≥10s·≥10d; each link rendered `- [Name](relpath.md) — what; relevance: why THIS note`; no bare links. |
| CP2 | 9-GATE present (G1–G6 + G8-Discoverability) per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link fix, G7 discoverability, G8 in-degree≥1; single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 8 rows to `0_entry_points/entry_openclaw_docs.md` (created as master W1 pre-step) under an "Automation" section; 8 notes < 30 ⇒ UPDATE shared hub, no standalone entry point (matches size rule). |
| CP4 | Size (≤30 or split) | **PASS** | 7–8 planned notes (cron-jobs + tasks each split 2 → 7 distinct `oc_*` notes; plan title says 8 incl. the 2 splits), well under 30; no sub-plan split needed. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master, which derived it from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `## Overview` → body → `## Related Notes` → `## References` → bold footer; YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; same forbidden-field list. |
| CP6 | Density (caps; borderline → split) | **PASS** | `## Density Re-Assessment`: all 7 notes 500–700w / ≤6 code / ≤400 lines; the two code-heavy pages (cron-jobs 22 fences, tasks 16) were split so each note reproduces ≤6 verbatim snippets. No borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read all 5 pages 2026-06-21. Measured body words (mirror files): cron-jobs ≈4,490 · hooks ≈1,950 · standing-orders ≈1,400 · taskflow ≈1,020 · tasks ≈2,710 — within ±5% of the plan's Source table (4,487 / 1,950 / 1,396 / 1,016 / 2,712). No page >1.5× estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (9 rows, all dispositioned to an `oc_*` doc note + existing-term link, **0 new captures**); `## Term-Note Authoring Requirements` present as **N/A (0 new terms)** with the inherited multi-source/format mandate noted. |
| CP8f | Slug specificity / collision audit (all notes, term + doc) | **PASS** | 0 new term slugs to audit (no `term_*` captures). Doc-note collision audit: all 7 `oc_*` slugs are series-specific (`oc_automation_*`), no existing vault note (term OR doc) duplicates them; OpenClaw automation concepts that overlap existing terms (`term_cron`, `term_webhook`, `term_pub_sub`, `term_gateway_hooks`) are LINKED, not recreated. |
| CP9 | Discoverability / inlinks (G8 executed) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link: `entry_openclaw_docs.md` → all 8 (guaranteed anti-island), plus `term_cron`/`term_webhook`/`term_event_driven_architecture`/`term_subagent`/`repo_openclaw_gateway`/etc.; G8 in-degree≥1 is in the phase gate table. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
