---
title: Sub-Plan co06 — OpenClaw Docs: Concepts (QA Matrix, Queue, Steering, Retry, Session, Pruning, Session Tools)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/qa-matrix", "concepts/queue", "concepts/queue-steering", "concepts/retry", "concepts/session", "concepts/session-pruning", "concepts/session-tool"]
---

# Sub-Plan co06: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` →
> body → `## Related Notes` ≥6 terms + siblings + repos → `## References` → bold footer), dedup-before-create
> (term_dictionary + documentation/ + `repo_openclaw*`), the 9-GATE table, cross-references, and the
> entry-point (`entry_openclaw_docs.md`) decision are all INHERITED from the master. This file re-reads its 7
> assigned pages from the mirror and locks the planned-notes / coverage / candidate-cross-ref decisions.

## Scope

The 7 runtime-behavior concept pages covering OpenClaw's **session & message-execution model**: the
auto-reply command queue and its modes (`queue`), how same-turn steering batches prompts at runtime
boundaries (`queue-steering`), the outbound-provider retry policy (`retry`), session routing / isolation /
lifecycle / state (`session`), in-memory tool-result pruning for prompt-cache efficiency (`session-pruning`),
the agent-facing cross-session / sub-agent orchestration tools (`session-tool`), and the maintainer-only live
Matrix QA lane (`qa-matrix`). **Priority P1 (Phase A)** — these define the queue/session/retry vocabulary that
channels, gateway, tools, and automation sub-plans reference. The code-side counterparts
(`repo_openclaw_sessions`, `repo_openclaw_agents`, `repo_openclaw_gateway`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 6,079 measured words. **Planned: 7 notes (1 per page; no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Matrix QA | concepts/qa-matrix | 1,322 | 2 | 10 | 2 | procedure |
| Command queue | concepts/queue | 1,105 | 1 | 11 | 0 | concept |
| Steering queue | concepts/queue-steering | 634 | 0 | 6 | 0 | concept |
| Retry policy | concepts/retry | 319 | 1 | 6 | 3 | concept |
| Session management | concepts/session | 882 | 2 | 8 | 1 | concept |
| Session pruning | concepts/session-pruning | 542 | 1 | 8 | 0 | concept |
| Session tools | concepts/session-tool | 1,275 | 1 | 8 | 0 | procedure |

Totals: **6,079 words · 8 code fences · 57 H2 · 6 H3.** All pages are well under the 2,500-word split
threshold; each is single-BB. (Counts: `wc -w` on raw mirror files incl. frontmatter; fences = `grep -c '^```'` / 2.)

## Content Strategy

- **Prioritize**: the queue/steering execution model (`queue` + `queue-steering`) and session lifecycle/state
  (`session`) — these are the most cross-referenced runtime concepts and define the `/queue` mode vocabulary
  (steer/followup/collect/interrupt) and session-routing rules (DM isolation, daily/idle reset, gateway-owned
  state) that channels and gateway sub-plans depend on.
- **Split**: none. All 7 pages are ≤1,322 words and single-BB; each maps cleanly to exactly one note. (See
  Split Decisions.)
- **Link-out (do not duplicate)**:
  - `/steer <message>` explicit command → `oc_tools_steer` (to08, planned, this series); both queue pages
    point to it but do not redefine it.
  - `concepts/compaction` (summarization-based reduction) → `oc_concepts_compaction` (co02, planned); pruning
    and session pages reference compaction as the complementary mechanism, not its definition here.
  - `concepts/qa-e2e-automation` (QA overview / live-transport contract) → `oc_concepts_qa_e2e_automation`
    (co05, planned); `qa-matrix` is one of three live-transport lanes that share that overview's contract.
  - `concepts/model-failover` → `oc_concepts_model_failover` (co04, planned); retry references failover when a
    long `Retry-After` is rejected.
  - `concepts/multi-agent` / `concepts/channel-docking` / `concepts/messages` / `concepts/agent-loop` →
    sibling planned notes; linked, not redefined.
  - `gateway/configuration` (all pruning/session-tool config knobs) → gw02 (planned); the config-reference
    surface is owned there, this series links it.
  - `reference/session-management-compaction` (store schema / send policy deep dive) → rf03 (planned).
  - Term vocabulary (`term_session` does not exist; use `term_message_queue`, `term_subagent`, `term_compaction`,
    `term_prompt_caching`, `term_retry`/`term_rate_limiting`, `term_a2a`, etc.) → linked, never inlined.

## Planned Notes

Filenames at `resources/documentation/openclaw/`; rule `oc_ + slug with / and - → _`. One BB per note.

| # | Filename | BB | Source page / sections | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_qa_matrix.md` | procedure | concepts/qa-matrix.md: Quick start, What the lane does, CLI (Common/Provider flags), Profiles, Scenarios, Environment variables, Output artifacts, Triage tips, Live transport contract | 650 | Maintainer-only live Matrix QA lane: running `pnpm openclaw qa matrix`, profiles/scenarios, provider mode flags, env-var tuning, output artifacts, and triage of hangs/cleanup. Source-checkout-only (`qa-lab` omitted from releases). |
| 2 | `oc_concepts_queue.md` | concept | concepts/queue.md: Why, How it works, Defaults, Queue modes, Queue options, Steer and streaming, Precedence, Per-session overrides, Scope and guarantees, Troubleshooting | 600 | The lane-aware in-process auto-reply queue: per-session serialization with global-lane concurrency caps, the four `/queue` modes (steer/followup/collect/interrupt), debounce/cap/drop options, mode-resolution precedence, and per-session overrides. |
| 3 | `oc_concepts_queue_steering.md` | concept | concepts/queue-steering.md: Runtime boundary, Modes, Burst example, Scope, Debounce | 480 | How `steer`-mode delivers mid-run prompts at model boundaries (drain after the tool-call batch, append as user messages before the next LLM call); OpenClaw internal steering vs Codex `turn/steer` batching; burst behavior and debounce. |
| 4 | `oc_concepts_retry.md` | concept | concepts/retry.md: Goals, Defaults, Behavior (Model providers, Discord, Telegram), Configuration, Notes | 400 | Per-request outbound retry policy: attempts/delay-cap/jitter defaults, Stainless-SDK `retry-after` handling with the 60s `x-should-retry:false` cutoff to trigger model failover, Discord/Telegram channel retry rules, and per-provider config. |
| 5 | `oc_concepts_session.md` | concept | concepts/session.md: How messages are routed, DM isolation (Dock linked channels), Session lifecycle, Where state lives, Session maintenance, Inspecting sessions | 650 | OpenClaw's session model: per-source routing (DM shared vs group/room/cron/webhook isolated), `dmScope` DM-isolation options, daily/idle/manual reset lifecycle, gateway-owned state files (`sessions.json` + transcripts), maintenance/cleanup, and inspection commands. |
| 6 | `oc_concepts_session_pruning.md` | concept | concepts/session-pruning.md: Why it matters, How it works, Legacy image cleanup, Smart defaults, Enable or disable, Pruning vs compaction | 480 | In-memory pruning of old tool results before each LLM call to shrink prompt-cache writes (cache-TTL trigger, soft-trim/hard-clear, legacy-image replay cleanup); Anthropic smart-defaults; pruning-vs-compaction contrast. |
| 7 | `oc_concepts_session_tool.md` | procedure | concepts/session-tool.md: Available tools, Listing and reading sessions, Sending cross-session messages, Status and orchestration helpers, Spawning sub-agents, Visibility | 700 | The agent-facing session tools (`sessions_list/history/send/spawn/yield`, `subagents`, `session_status`): tool-profile gating, safety-filtered transcript recall, cross-session/A2A messaging, sub-agent spawning options, and the self/tree/agent/all visibility scoping. |

## Section Coverage Map

```
concepts/qa-matrix.md → oc_concepts_qa_matrix (note 1)
├── Quick start ───────────────────────────────── → note 1
├── What the lane does ────────────────────────── → note 1
├── CLI / ### Common flags / ### Provider flags ─ → note 1
├── Profiles ──────────────────────────────────── → note 1
├── Scenarios ─────────────────────────────────── → note 1
├── Environment variables ─────────────────────── → note 1
├── Output artifacts ──────────────────────────── → note 1
├── Triage tips ───────────────────────────────── → note 1
├── Live transport contract ───────────────────── → note 1 (links co05 qa-e2e-automation)
└── Related ───────────────────────────────────── → Related Notes / References

concepts/queue.md → oc_concepts_queue (note 2)
├── Why / How it works / Defaults ─────────────── → note 2
├── Queue modes ───────────────────────────────── → note 2 (steer→note 3 cross-link)
├── Queue options / Steer and streaming ───────── → note 2
├── Precedence / Per-session overrides ────────── → note 2
├── Scope and guarantees / Troubleshooting ────── → note 2
└── Related ───────────────────────────────────── → Related Notes

concepts/queue-steering.md → oc_concepts_queue_steering (note 3)
├── Runtime boundary / Modes / Burst example ──── → note 3
├── Scope / Debounce ──────────────────────────── → note 3
└── Related ───────────────────────────────────── → Related Notes

concepts/retry.md → oc_concepts_retry (note 4)
├── Goals / Defaults ──────────────────────────── → note 4
├── Behavior (### Model providers / ### Discord / ### Telegram) → note 4
├── Configuration / Notes ─────────────────────── → note 4
└── Related ───────────────────────────────────── → Related Notes (model-failover co04)

concepts/session.md → oc_concepts_session (note 5)
├── How messages are routed ───────────────────── → note 5
├── DM isolation / ### Dock linked channels ───── → note 5 (channel-docking co01 cross-link)
├── Session lifecycle / Where state lives ─────── → note 5
├── Session maintenance / Inspecting sessions ─── → note 5
├── Further reading ───────────────────────────── → Related Notes / References
└── Related ───────────────────────────────────── → Related Notes

concepts/session-pruning.md → oc_concepts_session_pruning (note 6)
├── Why it matters / How it works ─────────────── → note 6
├── Legacy image cleanup / Smart defaults ─────── → note 6
├── Enable or disable / Pruning vs compaction ─── → note 6
├── Further reading ───────────────────────────── → Related Notes / References
└── Related ───────────────────────────────────── → Related Notes

concepts/session-tool.md → oc_concepts_session_tool (note 7)
├── Available tools ───────────────────────────── → note 7
├── Listing and reading sessions ──────────────── → note 7
├── Sending cross-session messages ────────────── → note 7
├── Status and orchestration helpers ──────────── → note 7
├── Spawning sub-agents / Visibility ──────────── → note 7
├── Further reading ───────────────────────────── → Related Notes / References
└── Related ───────────────────────────────────── → Related Notes
```
No orphaned sections. Every H2/H3 maps to its note. `Related`/`Further reading` lists become Related Notes +
References. Link-out targets (steer, compaction, qa-e2e-automation, model-failover, gateway/configuration,
multi-agent, channel-docking, reference/session-management-compaction) are cross-linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ≤1,322 words (max qa-matrix 1,322; rest ≤1,275) and single-BB, well under the 2,500-word / mixed-BB split thresholds. 1 page → 1 note throughout. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (6,079 measured words). New `oc_` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×5** (notes 2 queue · 3 queue-steering · 4 retry · 5 session · 6 session-pruning)
  · **procedure ×2** (note 1 qa-matrix · note 7 session-tool).
- Estimated digest words ~3,960 (avg ~566/note); each note ≤700w and ≤6 code fences. Source has only 8 fences
  total (config JSON5 blocks + CLI), reproduced selectively per note (each note ends well under the 6-fence cap).
- Cross-refs: **LOCKED at augment (xref-augment 2026-06-21)** — each note's `## Per-Note Related Notes
  `- [Name](relpath.md) — what it is; relevance: why THIS note`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

Standard: **≥8 terms · ≥10 snippets · ≥10 docs per note**, relevance-selected (re-read source 2026-06-21,
series + other OpenClaw sub-plans, not yet in the DB) are marked **(planned, this series)** as forward refs
`resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`; snippet → `../../code_snippets/`;
repo → `../../../areas/code_repos/`; other doc → `../<folder>/`; sibling oc_ → `oc_Y.md`;
entry point → `../../../0_entry_points/`.

### oc_concepts_qa_matrix (12t · 10s · 11d)

**Terms** (8):
- [QA](../../term_dictionary/term_qa.md) — quality-assurance discipline; relevance: the Matrix lane IS OpenClaw's live-transport QA suite for the Matrix channel.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery pipeline; relevance: `--profile fast --fail-fast` is the release-gate invocation run in CI.
- [Docker](../../term_dictionary/term_docker.md) — OS-level container runtime; relevance: the lane provisions a disposable Tuwunel homeserver in Docker and tears it down via `docker compose ... down`.
- [UAT](../../term_dictionary/term_uat.md) — user/acceptance testing tier; relevance: live-transport scenarios are the acceptance gate distinct from synthetic unit tests.
- [Test Plan](../../term_dictionary/term_test_plan.md) — structured scenario/profile coverage spec; relevance: profiles (transport/media/e2ee-*) and the scenario id catalog ARE the test plan.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: `--provider-mode live-frontier|mock-openai` selects whether scenarios drive a real or mock model.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-issued tool calls; relevance: exec/plugin approval scenarios assert tool-call + approval-metadata delivery over the live transport.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product under test; relevance: the lane starts a child OpenClaw gateway scoped to the SUT account.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider adapter; relevance: provider flags switch the model provider behind the live Matrix transport.
- [DevOps](../../term_dictionary/term_devops.md) — build/test/operate automation culture; relevance: maintainer-only tooling (`qa-lab` omitted from releases) is a source-checkout dev/ops workflow.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the canary reply + `OPENCLAW_QA_MATRIX_CANARY_TIMEOUT_MS` gate is a startup health probe before scenario coverage.
- [Test On Demand](../../term_dictionary/term_test_on_demand.md) — selective targeted test execution; relevance: `--scenario <id>` (repeatable) runs a hand-picked subset on demand.

**Docs** (11; ≥5 existing):
- [hermes_messaging_matrix_e2ee](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix E2EE messaging guide; relevance: the QA `e2ee-*` profiles exercise exactly this encrypted-Matrix surface.
- [hermes_messaging_matrix_proxy_mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — Hermes Matrix proxy/transport setup; relevance: documents the same Matrix transport the lane runs real traffic over.
- [band_testing_agents](../band/band_testing_agents.md) — coding-agent test harness patterns; relevance: closest cross-corpus analog for scenario-driven agent E2E testing.
- [cc_build_a_channel](../claude_code/cc_build_a_channel.md) — building a Claude Code channel adapter; relevance: the SUT is a channel adapter under test; explains the adapter contract being validated.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container/sandbox runtime model; relevance: parallels the Docker-isolated disposable-homeserver execution environment.
- [bedrock_agentcore_observability_telemetry](../aws_bedrock_agentcore/bedrock_agentcore_observability_telemetry.md) — agent-runtime telemetry/observability; relevance: parallels the lane's report/summary/observed-events artifacts for CI dashboards.
- [aws_lambda_overview](../aws_lambda/aws_lambda_overview.md) — ephemeral execution-environment model; relevance: analog for spin-up/teardown of a disposable per-run environment.
- [oc_concepts_qa_e2e_automation](oc_concepts_qa_e2e_automation.md) (planned, this series) — QA overview + live-transport contract; relevance: the Matrix lane is one of three lanes sharing this contract checklist.
- [oc_channels_matrix](oc_channels_matrix.md) (planned, this series) — the Matrix channel plugin; relevance: the exact plugin under test in the lane.
- [oc_channels_qa_channel](oc_channels_qa_channel.md) (planned, this series) — synthetic repo-backed QA channel; relevance: the broad synthetic suite intentionally NOT in the live-transport matrix (contrast).
- [oc_help_testing](oc_help_testing.md) (planned, this series) — running tests / adding QA coverage; relevance: source `Related` links it as the testing how-to home.

**Repos**:
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter implementations; relevance: hosts the Matrix channel exercised by the lane.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel internals; relevance: code home of the Matrix transport asserted by scenarios.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway/CLI monorepo; relevance: hosts `openclaw qa matrix` and the bundled `qa-lab` runner.

**Snippets** (10):
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix platform adapter; relevance: implementation of the Matrix transport the lane validates.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix homeserver connect/login; relevance: parallels driver/SUT/observer account login against the Tuwunel homeserver.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix allowlist/ACL handling; relevance: the lane's mention-gating/allowlist scenarios assert this behavior.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter contract; relevance: the live-transport contract checklist the lane checks the SUT against.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup resume; relevance: backs the restart-resume / homeserver-restart scenarios.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reaction/status emission; relevance: the lane's reaction-observation scenarios assert this path.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — gateway health/status probe; relevance: parallels the canary-reply health gate before scenarios start.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — devops/CI webhook integration; relevance: parallels invoking the lane from a CI release gate.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord transport intents; relevance: Discord is a sibling live-transport lane sharing the contract.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract platform-adapter base; relevance: the common adapter surface all three live-transport lanes implement.

### oc_concepts_queue (10t · 11s · 12d)

**Terms** (10):
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered async work queue; relevance: the core abstraction — a lane-aware in-process FIFO queue for auto-reply runs.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-throttle policy; relevance: serialization reduces upstream provider rate-limit hits (stated goal of the queue).
- [Throughput](../../term_dictionary/term_throughput.md) — units processed per time; relevance: per-lane concurrency caps (`maxConcurrent`) trade serialization for controlled throughput.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — mid-run prompt injection; relevance: `steer` is the default queue mode; the queue routes mid-run prompts to the active runtime.
- [Throttling](../../term_dictionary/term_throttling.md) — deliberate slowing of work admission; relevance: `debounceMs`/`cap`/`drop` throttle queued delivery.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat operation property; relevance: per-session serialization ("only one active run per session") avoids colliding non-idempotent session writes.
- [Cron](../../term_dictionary/term_cron.md) — scheduled job trigger; relevance: `cron`/`cron-nested` lanes let background cron turns run parallel to inbound replies.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent run; relevance: the `subagent` lane (default cap 8) drains sub-agent runs separately.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — multi-channel message hub; relevance: the queue sits in the gateway reply pipeline draining all inbound channels.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host product; relevance: the queue is pure-TypeScript OpenClaw internals (no external broker).

**Docs** (12; ≥5 existing):
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — Hermes agent run loop; relevance: the auto-reply run the queue serializes is an agent loop.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway reply-pipeline internals; relevance: documents the analogous gateway pipeline the lanes drain.
- [hermes_cron_advanced_jobs](../hermes_agent/hermes_cron_advanced_jobs.md) — cron job configuration; relevance: parallels the `cron`/`cron-nested` queue lanes and `cron.maxConcurrentRuns`.
- [aws_lambda_concurrency_concepts](../aws_lambda/aws_lambda_concurrency_concepts.md) — concurrency model fundamentals; relevance: cross-corpus analog for per-lane concurrency caps.
- [aws_lambda_reserved_concurrency](../aws_lambda/aws_lambda_reserved_concurrency.md) — per-function concurrency reservation; relevance: analog for `agents.defaults.maxConcurrent` capping parallel sessions.
- [sqs_fifo_delivery_logic_receiving](../aws_sqs/sqs_fifo_delivery_logic_receiving.md) — FIFO ordered delivery + message groups; relevance: SQS message-group serialization mirrors per-session-key lane serialization.
- [pi_rpc_events](../pi/pi_rpc_events.md) — run lifecycle/event stream; relevance: parallels the queued-run notices and typing-indicator-on-enqueue events.
- [oc_concepts_queue_steering](oc_concepts_queue_steering.md) (planned, this series) — steer-mode runtime detail; relevance: queue mode `steer` delegates timing here (sibling note 3).
- [oc_concepts_session](oc_concepts_session.md) (planned, this series) — per-session guarantees; relevance: the queue keys lanes by session (note 5).
- [oc_concepts_retry](oc_concepts_retry.md) (planned, this series) — outbound retry policy; relevance: serialization complements retry in avoiding rate limits (note 4).
- [oc_tools_steer](oc_tools_steer.md) (planned, this series) — explicit `/steer` command; relevance: source links it as the manual-steer counterpart.
- [oc_automation_tasks](oc_automation_tasks.md) (planned, this series) — background task records; relevance: detached lane runs are tracked as background tasks.

**Repos**:
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store/runtime; relevance: `runEmbeddedAgent` enqueues by session key here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway reply pipeline; relevance: owns the reply pipeline the lanes drain.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/config; relevance: home of `agents.defaults.maxConcurrent` lane caps.

**Snippets** (11):
- [snippet_hermes_agent_batch_runner_queue](../../code_snippets/snippet_hermes_agent_batch_runner_queue.md) — in-process run queue; relevance: directly analogous lane-aware FIFO run queue.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key derivation; relevance: derives the `session:<key>` lane key the queue enqueues by.
- [snippet_hermes_agent_gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — runner session-key routing; relevance: maps inbound runs to their per-session lane.
- [snippet_hermes_agent_gw_runner_supervisor](../../code_snippets/snippet_hermes_agent_gw_runner_supervisor.md) — run supervisor/concurrency control; relevance: enforces the global-lane concurrency cap.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — inbound run routing; relevance: routes inbound messages to the correct queue lane.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound reply dispatch; relevance: the reply step downstream of queue drain.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel dispatch kernel; relevance: feeds inbound messages into the queued reply pipeline.
- [snippet_hermes_agent_batch_runner_spawn](../../code_snippets/snippet_hermes_agent_batch_runner_spawn.md) — runner spawn/lane allocation; relevance: parallels allocating subagent/cron lanes.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound delivery after run; relevance: drains queued reply to the channel after the run completes.

### oc_concepts_queue_steering (10t · 11s · 11d)

**Terms** (9):
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — mid-run prompt injection; relevance: the entire page IS runtime-boundary steering of an active run.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered work queue; relevance: queued steering messages drain at model boundaries.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-issued tool calls; relevance: steering drains AFTER the assistant's tool-call batch, before the next LLM call.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning turn; relevance: review/compaction reasoning turns reject same-turn steering.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: steered prompts are appended as user messages before the next model call.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — multi-channel message hub; relevance: in multi-user channels the gateway tags injected prompts with sender/route context.
- [A2A](../../term_dictionary/term_a2a.md) — agent-to-agent context; relevance: cross-actor message context is preserved when prompts are injected into the active run.
- [Throttling](../../term_dictionary/term_throttling.md) — admission slowing; relevance: Codex `turn/steer` batches over a debounce quiet window before sending.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host runtime; relevance: OpenClaw internal steering vs Codex `turn/steer` differ in delivery.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-actor session; relevance: multi-user burst (four senders) is the page's canonical steering example.

**Docs** (11; ≥5 existing):
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — agent run loop + model boundaries; relevance: the model-boundary loop steering hooks into.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — dynamic in-run workflow control; relevance: parallels injecting mid-run instructions at runtime boundaries.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — interactive in-run commands; relevance: same family as `/queue` steering directives.
- [pi_rpc_events](../pi/pi_rpc_events.md) — run lifecycle/turn events; relevance: turn-end events are the drain boundary for steering.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — streaming run API; relevance: steering visibility under `partial`/`block` streaming is the page's UX caveat.
- [cc_interactive_mode_keyboard_shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — interrupt/steer-while-running UX; relevance: cross-corpus analog for steering vs interrupting a running turn.
- [oc_concepts_queue](oc_concepts_queue.md) (planned, this series) — parent queue concept; relevance: defines the `steer` mode this page details (note 2).
- [oc_tools_steer](oc_tools_steer.md) (planned, this series) — explicit `/steer` command; relevance: the manual command vs queue-mode steering distinction.
- [oc_concepts_messages](oc_concepts_messages.md) (planned, this series) — message lifecycle; relevance: steered prompts become user messages in the lifecycle (co04).
- [oc_concepts_agent_loop](oc_concepts_agent_loop.md) (planned, this series) — the model-boundary loop; relevance: steering drains at the loop's turn boundary (co01).
- [oc_concepts_streaming](oc_concepts_streaming.md) (planned, this series) — channel streaming modes; relevance: `partial`/`block` streaming shape how steering appears (co07).

**Repos**:
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — active-run steering queue; relevance: holds the queued steering messages per active run.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the runtime loop; relevance: drains steering at the model boundary inside the run loop.

**Snippets** (11):
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — run lifecycle/turn-end events; relevance: emits the turn-end boundary where steering drains.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — sender/route provenance on input; relevance: injected prompts carry sender/route context for the next model call.
- [snippet_openclaw_acp_manager_turn_stream](../../code_snippets/snippet_openclaw_acp_manager_turn_stream.md) — ACP/Codex turn streaming; relevance: where `turn/steer` is batched and sent to the Codex app-server.
- [snippet_hermes_agent_core_conversation_loop_turn_setup](../../code_snippets/snippet_hermes_agent_core_conversation_loop_turn_setup.md) — per-turn setup in the loop; relevance: the boundary at which queued user input is appended before the next call.
- [snippet_hermes_agent_core_conversation_loop_turn_hydration](../../code_snippets/snippet_hermes_agent_core_conversation_loop_turn_hydration.md) — turn input hydration; relevance: appends drained steering messages as user messages.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — streaming backpressure; relevance: under `partial`/`block` streaming, governs how preview finalizes around steering.
- [snippet_hermes_agent_core_conversation_loop_main_loop_entry](../../code_snippets/snippet_hermes_agent_core_conversation_loop_main_loop_entry.md) — main loop entry; relevance: the loop that checks queued steering at each model boundary.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — inbound routing to active run; relevance: routes a mid-run prompt into the current active session run.
- [snippet_hermes_agent_tui_event_publisher](../../code_snippets/snippet_hermes_agent_tui_event_publisher.md) — run-event publishing; relevance: surfaces the turn-end / steering-accepted events.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached Codex runtime mgmt; relevance: the native Codex harness path that exposes `turn/steer` instead of internal steering.

### oc_concepts_retry (10t · 11s · 11d)

**Terms** (10):
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-throttle/429 policy; relevance: retry triggers on HTTP 429 and honors `retry_after`/`Retry-After`.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — geometrically growing retry delay; relevance: Discord/Telegram fall back to exponential backoff when no `retry_after` is provided.
- [Retry Pattern](../../term_dictionary/term_retry_pattern.md) — structured retry-with-limits design; relevance: the page IS the per-request retry policy (attempts/delay-cap/jitter).
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat property; relevance: retry is per-step to avoid duplicating non-idempotent operations.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe token for safe replay; relevance: the per-request granularity preserves ordering / avoids double-send.
- [Failover](../../term_dictionary/term_failover.md) — switch to a backup on failure; relevance: the 60s `Retry-After` cutoff surfaces the error so failover can act.
- [Model Failover](../../term_dictionary/term_model_failover.md) — rotate auth-profile/fallback model; relevance: `x-should-retry: false` injection triggers model failover to another profile/model.
- [Throttling](../../term_dictionary/term_throttling.md) — admission slowing; relevance: provider min-delays (Telegram 400ms, Discord 500ms) throttle send rate.
- [Fault Tolerance](../../term_dictionary/term_fault_tolerance.md) — resilience to transient failure; relevance: retries cover DNS failures, connection resets, socket closes, fetch failures.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: model-provider SDK retries are the primary retry surface.

**Docs** (11; ≥5 existing):
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — server/429/usage-limit error handling; relevance: same retryable-status family (429/5xx) the policy targets.
- [cc_request_and_quality_errors](../claude_code/cc_request_and_quality_errors.md) — request error classes; relevance: parallels the 408/409/429/5xx retryable taxonomy.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback-model selection; relevance: the fallback path model failover rotates to after the cutoff.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback ladder; relevance: the auth-profile/provider rotation triggered by `x-should-retry:false`.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing/retry config; relevance: where per-provider retry/route policy is configured.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime behavior; relevance: documents Stainless-SDK retry handling analog.
- [bedrock_agentcore_async_long_running](../aws_bedrock_agentcore/bedrock_agentcore_async_long_running.md) — long-running/async handling; relevance: parallels the long-`Retry-After` (>60s) handling decision.
- [oc_concepts_model_failover](oc_concepts_model_failover.md) (planned, this series) — auth-profile/fallback rotation; relevance: the failover the 60s cutoff hands off to (co04).
- [oc_concepts_queue](oc_concepts_queue.md) (planned, this series) — serialization for rate-limit avoidance; relevance: complementary rate-limit mitigation (note 2).
- [oc_channels_discord](oc_channels_discord.md) (planned, this series) — Discord channel; relevance: Discord send-retry rules (429/5xx/transport) are channel-specific here (ch01).
- [oc_channels_telegram](oc_channels_telegram.md) (planned, this series) — Telegram channel; relevance: Telegram retry + markdown-parse-error fallback to plain text (ch05).

**Repos**:
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider SDK adapters; relevance: the model-provider SDK retry surface (`OPENCLAW_SDK_RETRY_MAX_WAIT_SECONDS`).
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Discord/Telegram send-retry implementation.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent-core retry/failover loop; relevance: analogous retry + model-failover orchestration.

**Snippets** (11):
- [snippet_hermes_agent_core_retry_utils](../../code_snippets/snippet_hermes_agent_core_retry_utils.md) — attempts/backoff/jitter impl; relevance: the exact retry-policy primitives (attempts=3, jitter=0.1, max-delay cap).
- [snippet_hermes_agent_conv_loop_post_api_retry](../../code_snippets/snippet_hermes_agent_conv_loop_post_api_retry.md) — retryable-status detection + retry; relevance: classifies 408/409/429/5xx as retryable like the policy.
- [snippet_hermes_agent_core_error_classifier_backoff](../../code_snippets/snippet_hermes_agent_core_error_classifier_backoff.md) — backoff classification; relevance: maps errors to backoff vs immediate-surface (the 60s-cutoff decision).
- [snippet_hermes_agent_core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — error taxonomy; relevance: the retryable/non-retryable taxonomy behind the policy.
- [snippet_hermes_agent_core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — rate-limit recovery; relevance: honors `retry-after` then surfaces for failover when too long.
- [snippet_hermes_agent_core_conversation_loop_retry_handler](../../code_snippets/snippet_hermes_agent_core_conversation_loop_retry_handler.md) — retry handler; relevance: drives the per-request retry loop.
- [snippet_hermes_agent_tools_mcp_retry](../../code_snippets/snippet_hermes_agent_tools_mcp_retry.md) — MCP-call retry; relevance: per-request retry applied to tool/MCP calls.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — channel rate-limit handling; relevance: channel-level send-rate handling analogous to Discord/Telegram min-delays.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: the failover rotation the retry cutoff hands control to.

### oc_concepts_session (10t · 11s · 12d)

**Terms** (10):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: sessions are an OpenClaw-core conversation construct, all gateway-owned.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: sub-agent entries are synthetic session rows that age out under maintenance.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent routing; relevance: "Further reading" links multi-agent session isolation across agents.
- [Cron](../../term_dictionary/term_cron.md) — scheduled trigger; relevance: cron jobs get a fresh session per run (routing table) and age out separately.
- [Compaction](../../term_dictionary/term_compaction.md) — conversation summarization; relevance: linked as the complementary long-conversation mechanism to session lifecycle.
- [Slack](../../term_dictionary/term_slack.md) — chat platform; relevance: thread-scoped Slack/Discord chat sessions are preserved as durable pointers by maintenance.
- [A2A](../../term_dictionary/term_a2a.md) — agent-to-agent; relevance: linked via session-tools cross-session work and routing isolation.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — channel hub; relevance: the gateway owns all session state; UI clients query it.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness probe; relevance: heartbeat/system-event turns write metadata but don't extend idle freshness — the liveness vs freshness distinction.
- [Eviction Policy](../../term_dictionary/term_eviction_policy.md) — bounded-store cleanup rule; relevance: `session.maintenance` (`pruneAfter`, `maxEntries`) is a session-store eviction policy.

**Docs** (12; ≥5 existing):
- [bedrock_agentcore_sessions_model](../aws_bedrock_agentcore/bedrock_agentcore_sessions_model.md) — agent-runtime session model; relevance: cross-corpus analog for session identity, isolation, and lifecycle.
- [bedrock_agentcore_sessions_usage](../aws_bedrock_agentcore/bedrock_agentcore_sessions_usage.md) — session usage/lifecycle ops; relevance: parallels session reuse, reset, and inspection.
- [bedrock_agentcore_runtime_sessions_detail](../aws_bedrock_agentcore/bedrock_agentcore_runtime_sessions_detail.md) — runtime session isolation detail; relevance: parallels per-source isolation (DM/group/room).
- [pi_sessions](../pi/pi_sessions.md) — coding-agent session model; relevance: closest coding-agent analog for session routing/state.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway-owned state internals; relevance: documents the gateway-as-state-owner pattern OpenClaw uses.
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent session board; relevance: parallels multi-agent session routing/isolation.
- [eventbridge_scheduler_create](../aws_eventbridge/eventbridge_scheduler_create.md) — scheduled-run creation; relevance: analog for cron jobs spawning a fresh session per run.
- [oc_concepts_session_pruning](oc_concepts_session_pruning.md) (planned, this series) — tool-result trimming; relevance: complementary in-memory context mechanism (note 6).
- [oc_concepts_session_tool](oc_concepts_session_tool.md) (planned, this series) — agent session tools; relevance: tools that inspect/route across these sessions (note 7).
- [oc_concepts_compaction](oc_concepts_compaction.md) (planned, this series) — summarizing long conversations; relevance: "Further reading" complement (co02).
- [oc_concepts_channel_docking](oc_concepts_channel_docking.md) (planned, this series) — dock linked channels; relevance: dock reroutes a DM session's reply route (co01).
- [oc_reference_session_management_compaction](oc_reference_session_management_compaction.md) (planned, this series) — store-schema/send-policy deep dive; relevance: the `sessions.json` schema + advanced config home (rf03).

**Repos**:
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store/lifecycle owner; relevance: implements routing, `sessions.json`, transcripts, reset.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway state owner; relevance: gateway owns all session state and serves UI queries.

**Snippets** (11):
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — sessionId/key resolution; relevance: resolves the `sessionId`/key the routing table maps to.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — daily/idle reset hooks; relevance: implements the 4AM daily + idle-minutes reset lifecycle.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — dmScope key derivation; relevance: derives keys for `dmScope` (`per-channel-peer`, etc.).
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript/store layout scan; relevance: the `sessions.json` + `<sessionId>.jsonl` on-disk layout.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — reset mutation; relevance: performs the roll-the-session reset (discarding stale system-event notices).
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — lifecycle timestamp patches; relevance: maintains `sessionStartedAt`/`lastInteractionAt`/`updatedAt`.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — store index read; relevance: reads store rows without pruning at startup (the read-no-cap rule).
- [snippet_openclaw_gateway_session_fs_title_cache_archive](../../code_snippets/snippet_openclaw_gateway_session_fs_title_cache_archive.md) — title cache / archive; relevance: maintenance archives retired DM rows / keeps transcripts as deleted archives.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event records; relevance: the `<sessionId>.jsonl` transcript header used to resolve older rows.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM-scope security audit; relevance: `openclaw security audit` verifies DM-isolation setup.

### oc_concepts_session_pruning (9t · 10s · 11d)

**Terms** (9):
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — provider prompt-prefix cache; relevance: pruning's primary payoff is shrinking Anthropic prompt-cache writes after TTL expiry.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — key-value attention cache; relevance: prompt caching is the inference-time KV-prefix reuse pruning optimizes.
- [Compaction](../../term_dictionary/term_compaction.md) — conversation summarization; relevance: the page's explicit pruning-vs-compaction contrast (trims results vs summarizes conversation).
- [Context Window](../../term_dictionary/term_context_window.md) — bounded model input span; relevance: accumulated tool output inflates the context window pruning trims.
- [Context Compression](../../term_dictionary/term_context_compression.md) — shrinking in-context content; relevance: soft-trim/hard-clear is a per-request context-compression technique.
- [Eviction Policy](../../term_dictionary/term_eviction_policy.md) — cache-content removal rule; relevance: hard-clear/replace-with-placeholder is an in-memory eviction policy for old tool results.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: smart defaults auto-enable pruning for Anthropic OAuth/API-key profiles.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: pruning runs before each LLM call to reduce prompt size/cost.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: in-memory-only pruning (transcript preserved) is OpenClaw runtime behavior.

**Docs** (11; ≥5 existing):
- [cc_agent_sdk_context_window](../claude_code/cc_agent_sdk_context_window.md) — context-window management; relevance: same problem space — keeping the context window lean.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — token-usage reduction tactics; relevance: pruning tool results directly lowers tokens/cost.
- [cc_cache_preserving_actions](../claude_code/cc_cache_preserving_actions.md) — preserving prompt-cache prefixes; relevance: pruning + recent-turn byte preservation keeps cache prefixes stable.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — what fills the context window; relevance: tool outputs (exec/file/search) are the bloat pruning targets.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — context compression + caching; relevance: directly analogous compression-for-caching mechanism.
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime context knobs; relevance: parallels `contextPruning.*` mode/ttl settings.
- [pi_compaction](../pi/pi_compaction.md) — coding-agent compaction; relevance: the complementary summarization mechanism in a sibling tool.
- [oc_concepts_compaction](oc_concepts_compaction.md) (planned, this series) — summarization-based reduction; relevance: the complementary saved-in-transcript mechanism (co02).
- [oc_concepts_session](oc_concepts_session.md) (planned, this series) — session lifecycle/state; relevance: pruning operates within a session's per-request context (note 5).
- [oc_concepts_context_engine](oc_concepts_context_engine.md) (planned, this series) — context assembly engine; relevance: pruning is a stage in per-request context assembly (co02).
- [oc_gateway_configuration](oc_gateway_configuration.md) (planned, this series) — config reference; relevance: home of all `contextPruning.*` config knobs (gw02).

**Repos**:
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — per-request context assembly; relevance: assembles the pruned context before each LLM call.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — context/media handling; relevance: implements the legacy-image replay cleanup and media-ref handling.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-profile defaults; relevance: home of `contextPruning` smart-defaults per profile.

**Snippets** (10):
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compaction/cache reset interplay; relevance: the cache-TTL reset that pruning resets after trimming.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — media/image block classify; relevance: identifies raw image blocks / media markers for legacy-image cleanup.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — image-record lifecycle; relevance: tracks processed images for the `[image data removed]` replay view.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — prompt-cache section layout; relevance: the cache-prefix structure pruning keeps stable.
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression strategy; relevance: cross-corpus analog of trim-vs-summarize decisioning.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction handoff; relevance: the compaction cycle pruning runs between.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persist (transcript untouched); relevance: confirms the on-disk transcript is not rewritten by in-memory pruning.
- [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — loop-side session persist; relevance: parallels preserving full history while trimming the in-memory prompt.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — textual media-ref handling; relevance: replaces `[media attached: ...]`/`media://inbound/...` refs in the replay view.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — platform media/cache helpers; relevance: helpers for media-block handling around cache writes.

### oc_concepts_session_tool (10t · 12s · 11d)

**Terms** (10):
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: `sessions_spawn`/`subagents` create and inspect sub-agent runs.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent orchestration; relevance: session tools are the cross-agent orchestration surface.
- [Orchestration](../../term_dictionary/term_orchestration.md) — coordinating multiple runs/agents; relevance: `sessions_yield`/`subagents` are the orchestration helpers.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — agent-level coordination; relevance: depth-tiered tool grants (depth-1 orchestrators get spawn tools) define the orchestration topology.
- [A2A](../../term_dictionary/term_a2a.md) — agent-to-agent messaging; relevance: `sessions_send` + the reply-back loop (`maxPingPongTurns`, `REPLY_SKIP`) is A2A.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — gated tool catalog; relevance: tools are subject to the active tool profile and allow/deny policy.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — external-harness agent protocol; relevance: `runtime: "acp"` spawns external-harness sub-agents.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: `sandbox: "require"` enforces sandboxing on the child; sandboxed sessions clamp visibility to `tree`.
- [Delegate Task](../../term_dictionary/term_delegate_task.md) — handing work to a sub-agent; relevance: native spawns deliver the task in the child's first `[Subagent Task]` message.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: these are OpenClaw agent-facing session tools.

**Docs** (11; ≥5 existing):
- [cc_work_with_subagents](../claude_code/cc_work_with_subagents.md) — working with sub-agents; relevance: closest analog for the spawn/inspect/delegate tool surface.
- [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — orchestrating agent teams; relevance: parallels depth-tiered orchestration via session tools.
- [cc_forked_subagents](../claude_code/cc_forked_subagents.md) — forked-context sub-agents; relevance: `context: "fork"` vs `"isolated"` spawn options.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — sub-agent delegation; relevance: the delegate-and-yield pattern `sessions_spawn`/`sessions_yield` implement.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation patterns guide; relevance: cross-session delegation and reply-back patterns.
- [band_acp_client](../band/band_acp_client.md) — ACP client integration; relevance: the `runtime:"acp"` external-harness spawning path.
- [bedrock_agentcore_a2a_create](../aws_bedrock_agentcore/bedrock_agentcore_a2a_create.md) — A2A agent creation; relevance: cross-corpus analog for `sessions_send` agent-to-agent messaging.
- [oc_concepts_session](oc_concepts_session.md) (planned, this series) — session routing/lifecycle; relevance: the sessions these tools list/read/route across (note 5).
- [oc_concepts_multi_agent](oc_concepts_multi_agent.md) (planned, this series) — multi-agent architecture; relevance: the orchestration model these tools serve (co05).
- [oc_tools_acp_agents](oc_tools_acp_agents.md) (planned, this series) — ACP external-harness agents; relevance: ACP-specific spawn behavior (`runtime:"acp"`) lives here (to01).
- [oc_gateway_configuration](oc_gateway_configuration.md) (planned, this series) — session-tool config knobs; relevance: visibility/profile/`maxSpawnDepth` config home (gw02).

**Repos**:
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — sub-agent spawn/registry; relevance: implements `sessions_spawn`/`subagents` + depth/caps.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions list/history/send; relevance: implements the cross-session recall/messaging tools.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — config + visibility scoping; relevance: enforces tool-profile gating and `self/tree/agent/all` visibility.

**Snippets** (12):
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — spawn depth/caps; relevance: enforces `maxSpawnDepth` and depth-1 orchestrator tool grants.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — `subagents` status/lifecycle; relevance: backs the `subagents action:"list"` visibility helper.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP sub-agent handoff; relevance: the `runtime:"acp"` external-harness spawn path.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — `sessions_send` routing policy; relevance: inter-session send rules (thread-key rejection, fire-and-forget vs wait).
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — visibility/level scoping; relevance: implements `self/tree/agent/all` visibility clamping.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — spawn policy/options; relevance: `model`/`thinking`/`sandbox`/`context` spawn-option handling.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ACP spawn variant; relevance: spawning an ACP-runtime child via `sessions_spawn`.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — thread-bound spawn; relevance: `thread: true` binds the spawn to a chat thread.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: thread-key rules why `:thread:<id>` keys aren't valid send targets.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — completion announce; relevance: the announce step posting sub-agent results to the requester channel.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate spawn; relevance: cross-corpus analog of the spawn/delegate tool.
- [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — anti-recursion guard; relevance: parallels leaf sub-agents not receiving recursive orchestration tools.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes (these 7), NOT new `term_dictionary` entries.

| Term (surface in source) | Disposition |
|---|---|
| command queue / auto-reply queue / lane / FIFO | → `oc_concepts_queue` (note 2); link `term_message_queue` (exists). No new term. |
| queue modes: steer / followup / collect / interrupt | → notes 2 + 3 (documentation concepts); link `term_agent_steering` (exists). No new term. |
| same-turn steering / runtime boundary / `turn/steer` | → `oc_concepts_queue_steering` (note 3); link `term_agent_steering`. No new term. |
| debounce / cap / drop / precedence | → note 2 as config concepts; not promoted (config knobs, not reusable cross-cutting terms). |
| retry policy / attempts / jitter / backoff / `Retry-After` | → `oc_concepts_retry` (note 4); link `term_exponential_backoff`, `term_rate_limiting`, `term_idempotency`, `term_failover` (all exist). No new term. |
| session / session key / dmScope / DM isolation | → `oc_concepts_session` (note 5). NOTE: `term_session` does NOT exist in DB (verified). Per master, session vocabulary stays an `oc_*` doc concept; link adjacent `term_subagent`/`term_multi_agent`/`term_compaction`. Not captured as a new term (out of master scope; the doc note IS the home). |
| session lifecycle / daily reset / idle reset / maintenance | → note 5; not promoted (product-specific behavior). |
| session pruning / soft-trim / hard-clear / cache-TTL | → `oc_concepts_session_pruning` (note 6); link `term_prompt_caching`, `term_kv_cache`, `term_compaction` (exist). No new term. |
| session tools (`sessions_*`, `subagents`, `session_status`) | → `oc_concepts_session_tool` (note 7); link `term_tool_registry`, `term_subagent`, `term_a2a` (exist). No new term. |
| A2A / reply-back loop / `REPLY_SKIP` / inter-session message | → note 7; link `term_a2a` (exists). No new term. |
| Matrix QA / Tuwunel / live transport lane / profiles / scenarios | → `oc_concepts_qa_matrix` (note 1); link `term_qa`, `term_docker`, `term_ci_cd` (exist). No new term. |
| E2EE / homeserver / SAS-QR verification | → note 1 as QA-scenario vocabulary; not promoted (`term_e2ee`/`term_homeserver` absent, but these are Matrix-test scenario labels, not reusable cross-cutting terms — out of master scope). |

**New-term candidates: NONE.** No genuinely reusable, cross-cutting term lacking an existing note AND a
doc-page home surfaced; all vocabulary either has an existing `term_*` note (linked) or is product-specific
behavior owned by its `oc_*` doc note. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. (Inherited requirement from master:
added to its `acronym_glossary_*.md` — not applicable here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + body structure + footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no claim absent from source) | diff each note vs `inbox/openclaw_docs/concepts/<page>.md` |
| G3 | Density + Coverage (≤400L / ≤2,500w / ≤6 code; every H2/H3 covered) | word/line/fence count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + siblings/repos, each with relevance) | per-note Related Notes review |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` (planned siblings allowed as forward refs) |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + DB reindex |
| G7 | Discoverability (each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`) | via `entry_openclaw_docs.md` rows + term/repo inlinks |
| G8 | In-degree ≥1 (anti-island) | query `note_links` after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_qa_matrix oc_concepts_queue oc_concepts_queue_steering oc_concepts_retry oc_concepts_session oc_concepts_session_pruning oc_concepts_session_tool"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # at least one sibling oc_ link in Related Notes
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING ${SIBLING_PREFIX} LINK"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
done

# YAML frontmatter validation across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

(Ghost/broken-link gates G5/G6 run via `/tessellum-fix-ghost-references` and `/tessellum-fix-broken-links` after a
`bash scripts/update_notes_database.sh` reindex; forward-refs to planned sibling `oc_*` notes are expected and
either co-created or redirected at execution.)

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_concepts_qa_matrix | procedure | 650 | 2 | ✅ |
| 2 | oc_concepts_queue | concept | 600 | 1 | ✅ |
| 3 | oc_concepts_queue_steering | concept | 480 | 0 | ✅ |
| 4 | oc_concepts_retry | concept | 400 | 1 | ✅ |
| 5 | oc_concepts_session | concept | 650 | 2 | ✅ |
| 6 | oc_concepts_session_pruning | concept | 480 | 1 | ✅ |
| 7 | oc_concepts_session_tool | procedure | 700 | 1 | ✅ |

No note approaches any cap. Source is light on code (8 fences total across 7 pages); config JSON5 blocks are
reproduced verbatim but selectively (each note ≤2 fences). No splits required.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Concepts**
section / co06 sub-plan grouping. Each new note RECEIVES its back-link from `entry_openclaw_docs.md` at
finalization (satisfies G7/G8). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 — every note gets ≥1):

- `entry_openclaw_docs` → all 7 notes (primary anti-island guarantee).
- `repo_openclaw_sessions` → notes 2, 3, 5, 6, 7 (session/queue runtime).
- `repo_openclaw_agents` → notes 2, 3, 6, 7 (run loop, subagents, context pruning).
- `repo_openclaw_gateway` → notes 2, 5, 6, 7 (gateway-owned state / reply pipeline).
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → notes 1, 4 (Matrix QA, channel retries).
- `repo_openclaw_extensions_llm_providers` → note 4 (provider SDK retry).
- `term_message_queue` → note 2; `term_agent_steering` → notes 2, 3; `term_rate_limiting`/`term_exponential_backoff`/`term_failover` → note 4; `term_prompt_caching`/`term_kv_cache` → note 6; `term_subagent`/`term_a2a`/`term_tool_registry` → notes 5, 7; `term_qa`/`term_docker` → note 1.

## Pacing Rules (inherited from master)

One execution phase, 7 notes (≤30 fan-out cap). 8 gates must pass before commit. Re-read each source page;
reproduce config snippets verbatim. One BB per note. `git pull --rebase --autostash origin main` first; commit
per wave; no Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before
`git push origin main`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Skill**: `/tessellum-augment-digestion-plan` (xref-augment pass). **Scope**: re-read all 7 source pages from
the mirror (`inbox/openclaw_docs/concepts/{qa-matrix,queue,queue-steering,retry,session,session-pruning,session-tool}.md`;
measured words confirm the Source table exactly: 1322/1105/634/319/882/542/1275 = 6,079) and locked the
per-note Related Notes mapping at the raised floors.

**What was locked**: the `## Candidate Cross-References` section was replaced by `## Per-Note Related Notes
Mapping (LOCKED — xref-augment 2026-06-21)` — one H3 per planned note with grouped **Terms / Docs / Repos /
Snippets**, every link carrying a `— what it is; relevance: why THIS note` statement. Standard:

**Per-note locked counts** (all meet floors; floor = ≥8t / ≥10s / ≥10d):

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_concepts_qa_matrix | 12 | 10 | 11 (7 existing / 4 planned) | 3 | ✅ |
| oc_concepts_queue | 10 | 11 | 12 (7 existing / 5 planned) | 3 | ✅ |
| oc_concepts_queue_steering | 10 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| oc_concepts_retry | 10 | 11 | 11 (7 existing / 4 planned) | 3 | ✅ |
| oc_concepts_session | 10 | 11 | 12 (7 existing / 5 planned) | 3 | ✅ |
| oc_concepts_session_pruning | 9 | 10 | 11 (7 existing / 4 planned) | 3 | ✅ |
| oc_concepts_session_tool | 10 | 12 | 11 (7 existing / 4 planned) | 3 | ✅ |

  relevance to each re-read page. Note 6 (session-pruning) lands at 9 terms — above the ≥8 floor; no padding
  note where the in-process pure-TS queue is NOT a broker; discarded recsys "cumulative gain" / ranking
  false-positives entirely).
  aws_lambda_*, aws_sqs_*, aws_eventbridge_*) PLUS sibling `oc_*` (planned, this series) forward-refs toward
  the ≥10 floor. 65 existing docs verified.
  mapping section against `notes` table; `oc_*`/`entry_*` targets are expected forward refs).

**New-term candidates**: **NONE.** The augment-time re-read (Step 2d re-scan) surfaced no genuinely
reusable, cross-cutting term that (a) lacks an existing `term_*` note AND (b) lacks an `oc_*` doc-page home.
`term_agent_steering`, `term_retry_pattern`, `term_model_failover`, `term_prompt_caching`, `term_kv_cache`,
`term_subagent`, `term_a2a`, `term_tool_registry`, `term_eviction_policy`) or is product-specific behavior
owned by its `oc_*` doc note (queue modes, dmScope, soft-trim/hard-clear, `turn/steer`, E2EE scenario labels).
`term_session` confirmed absent and intentionally NOT captured (per master: session vocabulary is owned by
`oc_concepts_session`, not a term entry). **Best-fit glossary if any future term were promoted**:
`acronym_glossary_gen_ai_agentic.md` (the agentic/LLM glossary) — but no capture is required for co06.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints. Source pages spot-re-read (CP7) during this pass.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7+G8 discoverability/in-degree for the single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` + `## Inlinks` specify 7 rows into `entry_openclaw_docs.md` (created master pre-step W1); every note RECEIVES its back-link there (G7/G8). |
| CP4 | Size manageable | **PASS** | 7 notes (1 per page, no splits) — well under the 30-note cap. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format inherited verbatim from master `## Format Definition`, derived from existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) doc corpora: `## Overview` opener, `## Related Notes` reference section, bold `**Source**`/`**Last Updated**`/`**Status**` footer, fixed YAML field order. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment table: max est. 700w / 2 code (note 7); all ≤700w, ≤2 fences, ≤400L — no note within reach of any cap; no splits warranted. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 mirror pages 2026-06-21; `wc -w` = 1322/1105/634/319/882/542/1275 = 6,079, matching the Source table exactly (ratio 1.00). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (every surface-term dispositioned to an `oc_*` doc note + existing-term link); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, with the inherited capture procedure noted). New-term candidates: NONE (confirmed at augment Step 2d re-scan). |
| CP8f | Slug specificity / collision (all-notes dedup) | **PASS** | 0 new term slugs to audit (no term captures). Doc-note collision audit: all 7 `oc_concepts_*` slugs DB-confirmed ABSENT (no existing term/doc duplicates the planned concept notes); `term_session` absence verified (no `oc` vs `term` doc-duplicate risk). |
| CP9 | Discoverability / inlinks (G8 executed, no islands) | **PASS** | `## Inlinks (existing notes → new notes)` maps each new note to ≥1 outside-folder inbound link (entry_openclaw_docs → all 7; repo_openclaw_* / term_* per note); G8 in-degree≥1 is in the phase gate table as an executed/verified check. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
