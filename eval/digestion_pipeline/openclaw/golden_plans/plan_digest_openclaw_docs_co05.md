---
title: Sub-Plan co05 — OpenClaw Docs: Concepts (multi-agent, OAuth, specialist lanes, benchmark pack, presence, progress drafts, QA E2E)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/multi-agent", "concepts/oauth", "concepts/parallel-specialist-lanes", "concepts/personal-agent-benchmark-pack", "concepts/presence", "concepts/progress-drafts", "concepts/qa-e2e-automation"]
---

<!-- status: pending -> ready (xref-augment + review 2026-06-21: per-note mapping locked at raised floors, 9/9 checkpoints PASS) -->


# Sub-Plan co05: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order, `## Overview`/`## Related Notes`/`## References` + bold footer), dedup (3-way across term_dictionary + documentation/ + repo_openclaw*), 9-GATE, cross-references, and entry-point (`entry_openclaw_docs.md`) are ALL inherited from the master — not re-derived here.

## Scope

The seven `concepts/` pages that document OpenClaw's **multi-tenant / operational** runtime behaviors:
multi-agent routing + bindings, OAuth subscription/token-sink auth, parallel specialist-lane design, the
local personal-agent QA benchmark pack, gateway/client presence, in-chat progress drafts, and the private
QA end-to-end automation stack. **Priority P1 (Phase A)** — these define the agent-isolation, auth, and QA
vocabulary that the CLI, gateway, channels, and tools sub-plans reference. The CODE-side counterparts
(`repo_openclaw_agents`, `repo_openclaw_gateway`, `repo_openclaw_sessions`, the `snippet_openclaw_*` corpus)
are LINKED, never recreated.

**Source**: OpenClaw docs, 7 pages, **13,449 measured words** (re-measured 2026-06-20 on the mirror).
**Planned: 10 notes** (2 pages split: multi-agent → 2, qa-e2e-automation → 3).

## Source Pages (Measured 2026-06-20, mirror inbox/openclaw_docs/)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| multi-agent | concepts/multi-agent | 2,466 | 6 | 14 | 1 | concept + procedure (split: isolation concept vs routing/binding config) |
| oauth | concepts/oauth | 1,196 | 3 | 8 | 4 | concept (OAuth token-sink + exchange + multi-account) |
| parallel-specialist-lanes | concepts/parallel-specialist-lanes | 576 | 2 | 9 | 3 | argument (scarce-resource lane design + rollout) |
| personal-agent-benchmark-pack | concepts/personal-agent-benchmark-pack | 436 | 1 | 3 | 0 | concept (repo-backed QA pack + privacy model) |
| presence | concepts/presence | 584 | 0 | 8 | 6 | model (presence entry schema + producers/merge/TTL) |
| progress-drafts | concepts/progress-drafts | 1,798 | 13 | 8 | 0 | procedure (configure visible in-progress chat drafts) |
| qa-e2e-automation | concepts/qa-e2e-automation | 6,393 | 30 | 10 | 8 | concept + procedure + model (split: overview vs live-transport reference vs architecture) |

**Total: 13,449 words, 55 code fences.**

## Content Strategy

- **Prioritize**: the multi-agent isolation model (`agentId`/`agentDir`/binding) and deterministic routing
  order — every channel/CLI doc references it; the OAuth token-sink + PKCE exchange (auth correctness); and
  the QA command surface + live-transport contract (the operational test-harness vocabulary).
- **Split**:
  - `multi-agent.md` (2,466w, near the 2,500 cap, 6 fences, mixes a *concept* (what one agent is, isolation,
    routing-rule precedence) with a *procedure* (per-channel binding config + platform/account examples +
    per-agent sandbox/tool config)) → **note 1 (routing concept) + note 2 (binding/sandbox config procedure)**.
  - `qa-e2e-automation.md` (6,393w — 2.5× the word cap, 30 fences, three distinct BBs) → **note 8 (overview +
    command surface + operator flow, concept) + note 9 (live transport reference: Telegram/Discord/Slack/
    WhatsApp + Convex pool, procedure) + note 10 (architecture: seeds, provider mocks, transport adapters,
    reporting, model)**.
- **Link-out (do NOT redefine)**: channel-specific setup (Discord/Telegram/WhatsApp/Slack) → `ch*` sub-plans;
  `concepts/queue`, `concepts/session`, `concepts/streaming`, `concepts/model-failover`, `concepts/mantis`,
  `concepts/qa-matrix`, `channels/qa-channel` → siblings in co01/co06/co07/co03 + ch04 (cited as planned or
  via existing terms); `gateway/secrets`, `gateway/authentication`, `gateway/configuration-reference` → `gw*`;
  `tools/subagents`, `tools/skills`, `tools/multi-agent-sandbox-tools` → `to*`. Existing terms
  (`term_oauth`, `term_pkce`, `term_oauth_token`, `term_qa`, `term_slack`, `term_credential_pool`, …) are
  LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_multi_agent_routing.md` | concept | multi-agent.md: What is "one agent"?, Paths (quick map) + Single-agent mode, Multiple agents = multiple people, Cross-agent QMD memory search, Routing rules (how messages pick an agent), Concepts | 650 | What an isolated OpenClaw agent is (workspace + `agentDir` + auth profiles + session store), single vs multi-agent mode, cross-agent QMD memory search, and the deterministic most-specific-wins binding routing order. |
| 2 | `oc_concepts_multi_agent_bindings_config.md` | procedure | multi-agent.md: Agent helper, Quick start, One WhatsApp number multiple people (DM split), Multiple accounts / phone numbers, Platform examples (Discord/Telegram/WhatsApp), Common patterns, Per-agent sandbox and tool configuration | 700 | Configuring multiple agents and bindings: `openclaw agents add`, per-channel account bindings (Discord/Telegram/WhatsApp), one-number DM split, multi-account routing, and per-agent sandbox + tool allow/deny config. |
| 3 | `oc_concepts_oauth.md` | concept | oauth.md (full): token sink, storage, Anthropic legacy/CLI migration, OAuth exchange (Anthropic setup-token, OpenAI Codex PKCE), refresh + expiry, multiple accounts (profiles) + routing | 700 | OpenClaw OAuth subscription auth end-to-end: the `auth-profiles.json` token sink, where credentials live, the PKCE login exchange for OpenAI Codex, automatic refresh/expiry under a lock, and multi-account profile routing. |
| 4 | `oc_concepts_parallel_specialist_lanes.md` | argument | parallel-specialist-lanes.md (full): first principles, recommended rollout (3 phases), minimal lane contract template | 550 | The design argument for parallel specialist agent lanes as a scarce-resource problem (session locks, model/tool capacity, context budget), the three-phase rollout, and the minimal per-lane contract template. |
| 5 | `oc_concepts_personal_agent_benchmark_pack.md` | concept | personal-agent-benchmark-pack.md (full): pack overview, Scenarios, Privacy Model, Extending The Pack | 450 | The repo-backed `personal-agent` QA scenario pack for local personal-assistant reliability checks: scenario coverage, `--pack` invocation, the fake-data privacy model, and how to extend the catalog. |
| 6 | `oc_concepts_presence.md` | model | presence.md (full): presence fields, producers (self/WS/system-event/node), merge + dedupe (`instanceId`), TTL + bounded size, remote/tunnel caveat, consumers, debugging | 500 | The OpenClaw presence model: the presence-entry field schema, the four producer sources, `instanceId`-keyed merge/dedupe, 5-minute TTL + 200-entry bound, loopback-IP caveat, and the macOS Instances-tab consumer. |
| 7 | `oc_concepts_progress_drafts.md` | procedure | progress-drafts.md (full): quick start, what users see, choose a mode, configure labels, control progress lines, channel behavior, finalization, troubleshooting | 700 | Configuring progress drafts (one self-updating in-progress chat message): enabling `streaming.mode: "progress"`, choosing partial/block/progress modes, label pools, progress-line controls, per-channel transport, finalization, and troubleshooting. |
| 8 | `oc_concepts_qa_e2e_automation_overview.md` | concept | qa-e2e-automation.md: intro/current pieces, Command surface, Operator flow, Live transport coverage (matrix table) | 750 | Overview of the private OpenClaw QA stack (qa-channel, qa-lab, qa-matrix, repo seeds, Mantis), the `openclaw qa <subcommand>` command surface, the two-pane operator flow + observability smokes, and the shared live-transport coverage matrix. |
| 9 | `oc_concepts_qa_e2e_automation_live_transports.md` | procedure | qa-e2e-automation.md: Telegram/Discord/Slack/WhatsApp QA reference (shared CLI flags, per-lane env + scenarios + artifacts, Slack workspace setup, Convex credential pool) | 800 | Running live-transport QA lanes against real Telegram, Discord, Slack, and WhatsApp accounts: shared CLI flags, per-lane required env + scenario catalogs + output artifacts, the Slack driver/SUT app setup, and the shared Convex credential pool. |
| 10 | `oc_concepts_qa_e2e_automation_architecture.md` | model | qa-e2e-automation.md: Repo-backed seeds, Provider mock lanes, Transport adapters (qa-lab vs runner split, Adding a channel, Scenario helper names), Reporting | 650 | The QA stack architecture: repo-backed YAML scenario seeds, the `mock-openai`/`aimock` provider lanes, the qa-lab-host vs transport-runner contract (adding a channel, decision rule, helper names), and the Markdown evidence reporting. |

## Section Coverage Map

```
concepts/multi-agent.md (2,466w)
├── (intro: agent + agentDir + binding) ───────────── → note 1 (oc_concepts_multi_agent_routing)
├── What is "one agent"? ──────────────────────────── → note 1
├── Paths (quick map) + ### Single-agent mode ─────── → note 1
├── Agent helper (`openclaw agents add`) ──────────── → note 2 (oc_concepts_multi_agent_bindings_config)
├── Quick start (Steps: workspace/accounts/bindings) → note 2
├── Multiple agents = multiple people ─────────────── → note 1
├── Cross-agent QMD memory search ─────────────────── → note 1
├── One WhatsApp number, multiple people (DM split) ─ → note 2
├── Routing rules (how messages pick an agent) ────── → note 1
├── Multiple accounts / phone numbers ─────────────── → note 2
├── Concepts (agentId/accountId/binding glossary) ── → note 1
├── Platform examples (Discord/Telegram/WhatsApp) ── → note 2
├── Common patterns (Tabs) ────────────────────────── → note 2
└── Per-agent sandbox and tool configuration ──────── → note 2
concepts/oauth.md (1,196w)
├── (intro: subscription auth, canonical openai id) ─ → note 3 (oc_concepts_oauth)
├── The token sink (why it exists) ────────────────── → note 3
├── Storage (where tokens live) ───────────────────── → note 3
├── Anthropic legacy token compatibility ──────────── → note 3
├── Anthropic Claude CLI migration ────────────────── → note 3
├── OAuth exchange (### setup-token, ### Codex PKCE) ─ → note 3
├── Refresh + expiry ──────────────────────────────── → note 3
└── Multiple accounts (### separate agents / profiles) → note 3
concepts/parallel-specialist-lanes.md (576w)
├── First principles ──────────────────────────────── → note 4 (oc_concepts_parallel_specialist_lanes)
├── Recommended rollout (### Phase 1/2/3) ─────────── → note 4
└── Minimal lane contract template + Owns/Does not own/Chat budget/Handoff/Tool posture → note 4
concepts/personal-agent-benchmark-pack.md (436w)
├── (intro: repo-backed pack) ─────────────────────── → note 5 (oc_concepts_personal_agent_benchmark_pack)
├── Scenarios ─────────────────────────────────────── → note 5
├── Privacy Model ─────────────────────────────────── → note 5
└── Extending The Pack ────────────────────────────── → note 5
concepts/presence.md (584w)
├── (intro: gateway + client presence) ────────────── → note 6 (oc_concepts_presence)
├── Presence fields (what shows up) ───────────────── → note 6
├── Producers (### self / WS / system-event / node) ─ → note 6
├── Merge + dedupe rules (why instanceId matters) ─── → note 6
├── TTL and bounded size ──────────────────────────── → note 6
├── Remote/tunnel caveat (loopback IPs) ───────────── → note 6
├── Consumers (### macOS Instances tab) ───────────── → note 6
└── Debugging tips ────────────────────────────────── → note 6
concepts/progress-drafts.md (1,798w)
├── (intro + Quick start) ─────────────────────────── → note 7 (oc_concepts_progress_drafts)
├── What users see ────────────────────────────────── → note 7
├── Choose a mode (off/partial/block/progress) ────── → note 7
├── Configure labels (auto pool / fixed / hide) ───── → note 7
├── Control progress lines (toolProgressDetail/maxLines/render) → note 7
├── Channel behavior (per-channel transport table) ── → note 7
├── Finalization ──────────────────────────────────── → note 7
└── Troubleshooting ───────────────────────────────── → note 7
concepts/qa-e2e-automation.md (6,393w)
├── (intro: current pieces) ───────────────────────── → note 8 (qa_e2e_automation_overview)
├── Command surface (qa run/suite/coverage/...) ───── → note 8
├── Operator flow (two-pane site + observability smokes) → note 8
├── Live transport coverage (lane×capability matrix) → note 8
├── Telegram/Discord/Slack/WhatsApp QA reference ──── → note 9 (qa_e2e_automation_live_transports)
│   ├── ### Shared CLI flags ───────────────────────── → note 9
│   ├── ### Telegram QA / Discord QA / Slack QA / WhatsApp QA → note 9
│   ├── #### Setting up the Slack workspace ────────── → note 9
│   └── ### Convex credential pool ─────────────────── → note 9
├── Repo-backed seeds ─────────────────────────────── → note 10 (qa_e2e_automation_architecture)
├── Provider mock lanes (mock-openai / aimock) ────── → note 10
├── Transport adapters (### Adding a channel, ### Scenario helper names) → note 10
└── Reporting (qa coverage / character-eval / evidence) → note 10
```
No orphaned sections. Channel-specific setup, queue/session/streaming/model-failover/mantis/qa-matrix/
qa-channel are linked (siblings or existing terms), not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| multi-agent.md (2,466w, 6 fences, 14 H2) | note 1 (`oc_concepts_multi_agent_routing`, concept) + note 2 (`oc_concepts_multi_agent_bindings_config`, procedure) | Near the 2,500-word cap AND mixed BB: a *concept* cluster (what an agent is, isolation, routing-rule precedence, glossary) vs a *procedure* cluster (agent wizard, per-channel binding config, platform/account examples, per-agent sandbox/tool config). Splitting keeps one BB per note and each ≤700w / ≤6 fences. |
| qa-e2e-automation.md (6,393w, 30 fences, 10 H2 / 8 H3, mixed BB) | note 8 (`_overview`, concept) + note 9 (`_live_transports`, procedure) + note 10 (`_architecture`, model) | 2.5× the word cap and 30 fences (far over the 6-fence cap) across three distinct BBs: a stack-overview/command-surface *concept*, a four-channel live-lane *procedure* (the bulk, ~3,000w), and a qa-lab/runner-contract + seeds + reporting *architecture model*. Three notes keep each ≤800w and ≤6 reproduced fences. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (13,449 words, 55 code fences). New `oc_*` notes: **10**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×4 (notes 1, 3, 5, 8) · procedure ×3 (notes 2, 7, 9) · argument ×1 (note 4) ·
  model ×2 (notes 6, 10).
- Est. digest words ~6,450 (avg ~645/note). The 55 source fences distribute across the procedure/model notes;
  each note reproduces selectively (verbatim) and stays ≤6 — the 30-fence QA page splits 3 ways and the
  13-fence progress-drafts page reproduces only the representative config examples.
- **Cross-refs (LOCKED at raised floors, xref-augment 2026-06-21):** every note maps **≥8 relevancy-selected
  `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** (PLUS relevant
  `repo_openclaw*` / sibling `oc_*`), each with a relevance statement, relevance-selected (no padding). ALL
  marked "(planned, this series)". See **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)**.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read each source page;
Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: terms →
`../../term_dictionary/term_Y.md`; sibling `oc_*` (this co05 series, planned W1) → `oc_Y.md`; other doc →
`../<folder>/<file>.md` (`../claude_code/cc_Y.md`, `../hermes_agent/hermes_Y.md`, `../pi/pi_Y.md`,
`../band/band_Y.md`); repo → `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`

### oc_concepts_multi_agent_routing (10t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: the routing concept is core OpenClaw runtime vocabulary.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — selecting which provider/model serves a request; relevance: binding routing is the request-to-agent analog of provider routing.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — how chat threads attach to a persistent agent context; relevance: `parentPeer` thread-inheritance is the second-tier binding rule.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: each `agentId` is one fully-scoped autonomous agent persona.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime scaffold around an LLM agent; relevance: an agent = workspace + agentDir + model registry + session store harness.
- [Session Data](../../term_dictionary/term_session_data.md) — per-conversation state and history; relevance: each agent owns an isolated session store under `agents/<agentId>/sessions`.
- [Session Features](../../term_dictionary/term_session_features.md) — session keying, mainKey, routing state; relevance: direct chats collapse to `agent:<agentId>:<mainKey>`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: workspace is default-cwd not a hard sandbox (the isolation caveat).
- [Persona](../../term_dictionary/term_persona.md) — a distinct agent identity/personality; relevance: multiple agents = multiple isolated personas (AGENTS.md/SOUL.md per agent).
- [Multi-Tenancy → Access Control](../../term_dictionary/term_access_control.md) — gating who/what may act; relevance: DM access control is global-per-account, a routing-isolation boundary.

**Docs**
- [oc_concepts_multi_agent_bindings_config](oc_concepts_multi_agent_bindings_config.md) — sibling config procedure (planned, this series); relevance: the routing concept's how-to companion.
- [oc_concepts_presence](oc_concepts_presence.md) — agent/client presence (planned, this series); relevance: the multi-agent page links Presence for availability.
- [oc_concepts_oauth](oc_concepts_oauth.md) — per-agent auth profiles (planned, this series); relevance: auth profiles are part of agent isolation.
- [oc_concepts_parallel_specialist_lanes](oc_concepts_parallel_specialist_lanes.md) — lane design (planned, this series); relevance: routing chats to dedicated agents is the lane primitive.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — defining an isolated subagent; relevance: cross-tool analog of per-agent scoping/isolation.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — subagent model overview; relevance: agent-isolation concept parallel in Claude Code.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — Hermes multi-agent profiles; relevance: same multi-persona-in-one-gateway pattern in the sibling fork.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating to sub-agents; relevance: cross-agent handoff analog.
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: per-agent session-store isolation analog.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — room-to-agent routing; relevance: deterministic chat-to-agent binding analog.
- [band_agent_lifecycle](../band/band_agent_lifecycle.md) — agent identity/lifecycle; relevance: agentId-as-brain identity parallel.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agents package; relevance: implements agentId/agentDir/scope/identity.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: per-agent session keying + isolation.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway dispatch; relevance: routes inbound messages to the bound agent.

**Snippets**
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — routes inbound to an agent; relevance: the routing-rule implementation.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding match logic; relevance: most-specific-wins binding resolution.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — peer/guild/team match resolver; relevance: the deterministic tier ordering.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — resolves conversation→agent; relevance: accountId/peer routing.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist gate; relevance: global-per-account DM access control.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity resolution; relevance: agentId-as-brain identity.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope resolution; relevance: workspace/agentDir/session scope.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — identity reset on switch; relevance: no-cross-talk isolation.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key builder; relevance: `agent:<id>:<mainKey>` keying.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — resolves session id; relevance: direct-chat collapse to main session.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — tracks message provenance; relevance: which agent/account produced input.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — cross-agent QMD search; relevance: `memorySearch.qmd.extraCollections` cross-agent recall.

### oc_concepts_multi_agent_bindings_config (9t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: config procedure for OpenClaw bindings.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — per-agent model selection; relevance: `agents.list[].model` (Sonnet vs Opus lanes).
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread-to-agent attachment; relevance: peer/group binding `match` config.
- [Slack](../../term_dictionary/term_slack.md) — Slack chat platform; relevance: `teamId` Slack binding tier + per-account tokens.
- [Sandbox](../../term_dictionary/term_sandbox.md) — per-agent execution isolation; relevance: `sandbox.mode`/`scope`/`docker.setupCommand` config.
- [Session Features](../../term_dictionary/term_session_features.md) — session keying; relevance: bindings determine the per-agent session set.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — provider auth credential; relevance: per-agent auth profiles configured alongside bindings.
- [Cron](../../term_dictionary/term_cron.md) — scheduled tasks; relevance: per-agent tool allow/deny lists `cron` among gated tools.
- [Access Control](../../term_dictionary/term_access_control.md) — tool/DM gating; relevance: tools.allow/deny + group allowlists per agent.

**Docs**
- [oc_concepts_multi_agent_routing](oc_concepts_multi_agent_routing.md) — routing concept (planned, this series); relevance: the concept this procedure configures.
- [oc_concepts_oauth](oc_concepts_oauth.md) — per-agent auth (planned, this series); relevance: bindings + per-agent OAuth go together.
- [oc_concepts_parallel_specialist_lanes](oc_concepts_parallel_specialist_lanes.md) — lane rollout (planned, this series); relevance: bindings implement specialist lanes.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — Hermes multi-agent profile config; relevance: closest sibling-fork binding/profile config doc.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack channel setup; relevance: per-account Slack token/binding config analog.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel→agent gateway wiring; relevance: account-to-agent binding architecture.
- [hermes_kanban_worker_lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — per-lane worker config; relevance: per-agent tool/concurrency config analog.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — subagent definition file; relevance: per-agent config-file analog.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — sandbox mode selection; relevance: `sandbox.mode` per-agent config analog.
- [cc_subagent_configuration_reference](../claude_code/cc_subagent_configuration_reference.md) — subagent config keys; relevance: per-agent allow/deny tool config analog.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi config keys; relevance: agent config-key reference analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents package; relevance: `openclaw agents add` wizard + agent config.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels core; relevance: account bindings + match resolution.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Discord/Telegram/WhatsApp adapters; relevance: per-channel account config.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding wizard; relevance: `agents add` interactive binding setup.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: per-agent session set.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding match; relevance: implements `bindings[].match`.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — tier resolver; relevance: account-scope upgrade behavior.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: peer/group binding override.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist; relevance: `dmPolicy: allowlist` + `allowFrom`.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents/token; relevance: per-bot Message Content Intent + token.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport; relevance: BotFather token + group policy.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard writes config; relevance: `agents add` produces the agents/bindings config.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool allow/deny; relevance: tools.allow/deny config.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: model/workspace/agentDir resolution.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — per-session model override; relevance: per-agent `model` selection.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — level overrides; relevance: per-agent config layering.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — dispatch handler; relevance: bindings drive dispatch.

### oc_concepts_oauth (10t · 11s · 12d)

**Terms**
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the page's subject (subscription auth via OAuth).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — access/refresh token pair; relevance: token sink stores access+refresh+expires+accountId.
- [PKCE](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange; relevance: the Codex login exchange flow.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity/credentials; relevance: provider auth overview.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored per-agent credential profile; relevance: `auth-profiles.json` is the central object.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: OpenClaw-specific token-sink design.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model/CLI; relevance: Anthropic Claude CLI reuse + setup-token path.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external LLM providers; relevance: OpenAI Codex/ChatGPT, Qwen, MiniMax, Z.AI subscription auth.
- [Pi Agent](../../term_dictionary/term_pi_agent.md) — sibling coding-agent tool; relevance: provider-auth analog (`pi_provider_auth`).
- [Secrets Management → Access Control](../../term_dictionary/term_access_control.md) — credential gating; relevance: read-through inheritance from main agent store.

**Docs**
- [oc_concepts_multi_agent_routing](oc_concepts_multi_agent_routing.md) — agent isolation (planned, this series); relevance: auth profiles are per-agent.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code auth; relevance: subscription vs API-key auth split parallel.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — MCP OAuth; relevance: OAuth exchange + token storage analog.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/logout issues; relevance: token-invalidation "randomly logged out" symptom.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth; relevance: sibling-tool subscription/OAuth auth analog.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth on headless/remote hosts; relevance: callback-can't-bind paste-redirect remote flow.
- [hermes_provider_minimax_oauth](../hermes_agent/hermes_provider_minimax_oauth.md) — MiniMax coding-plan OAuth; relevance: a named subscription-OAuth provider.
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — xAI Grok OAuth; relevance: another provider-plugin OAuth flow.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: API-key vs OAuth credential config analog.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: per-agent credential isolation/inheritance.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — gateway/proxy auth; relevance: provider-id canonicalization analog.
- [pi_security_model](../pi/pi_security_model.md) — Pi security/credentials; relevance: secret-store + token-handling analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents package; relevance: holds `auth-profiles.json` per agent.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: each provider ships its OAuth/API-key flow.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — Hermes CLI auth; relevance: `auth login/logout` + OAuth callback server analog.

**Snippets**
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — `auth.order` profile resolution; relevance: global profile ordering.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth refresh-token portability; relevance: refresh tokens not cloned to secondary agents.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external CLI fallback; relevance: Codex CLI runtime-only fallback token.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: auth-mode resolution at the gateway.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: auth gating at request time.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: where the runtime reads the token sink.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: Claude CLI reuse + setup-token path.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: canonical `openai` id + Codex OAuth.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout CLI; relevance: `models auth login --provider` analog.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — local callback server; relevance: `127.0.0.1:1455/auth/callback` capture.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE verifier/challenge; relevance: the PKCE exchange mechanics.

### oc_concepts_parallel_specialist_lanes (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: lanes route one gateway's chats to specialist agents.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered async work dispatch; relevance: the command-queue caps global parallelism.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned background agent run; relevance: long tasks acknowledge then run in a background sub-agent.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — model-capacity selection; relevance: global model capacity is a shared bottleneck.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — independent coding agents; relevance: each lane is a specialist autonomous agent.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime scaffold; relevance: each lane has its own workspace + system prompt contract.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget per turn; relevance: long transcripts (context budget) are a named bottleneck.
- [Sandbox](../../term_dictionary/term_sandbox.md) — tool-surface isolation; relevance: tool-risk rule = smallest tool surface per lane.
- [Throttling](../../term_dictionary/term_throttling.md) — rate/concurrency limiting; relevance: `maxConcurrent` + queue debounce/cap controls.
- [Concurrency → Idempotency](../../term_dictionary/term_idempotency.md) — safe repeated handling; relevance: detect duplicate requests across groups (coordinator).

**Docs**
- [oc_concepts_multi_agent_routing](oc_concepts_multi_agent_routing.md) — routing concept (planned, this series); relevance: lanes build on most-specific-wins routing.
- [oc_concepts_multi_agent_bindings_config](oc_concepts_multi_agent_bindings_config.md) — binding config (planned, this series); relevance: lanes are implemented as bindings + per-agent config.
- [oc_concepts_qa_e2e_automation_overview](oc_concepts_qa_e2e_automation_overview.md) — QA stack (planned, this series); relevance: concurrency/worker isolation shows up in QA suite lanes.
- [hermes_kanban_worker_lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — worker lanes; relevance: direct specialist-lane analog (per-lane ownership/concurrency).
- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — lane orchestrator; relevance: the Phase-3 coordinator/traffic-controller pattern.
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent board; relevance: multiple lanes/owners coordination.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — delegation patterns; relevance: handoff rule + background task delegation.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — delegation guide; relevance: chat-budget/handoff design argument.
- [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — orchestrating agent teams; relevance: coordinator-of-lanes analog.
- [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — parallel agent runs; relevance: scarce-resource parallelism argument analog.
- [cc_agent_teams_overview](../claude_code/cc_agent_teams_overview.md) — agent-team model; relevance: lane ownership/non-goals contract analog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents + subagent registry; relevance: `subagents.maxConcurrent`/delegationMode.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session serialization; relevance: per-session run serialization (lock bottleneck).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — command queue; relevance: global parallelism cap.

**Snippets**
- [snippet_hermes_agent_batch_runner_queue](../../code_snippets/snippet_hermes_agent_batch_runner_queue.md) — queue caps concurrency; relevance: the global-parallelism cap mechanic.
- [snippet_hermes_agent_batch_runner](../../code_snippets/snippet_hermes_agent_batch_runner.md) — batch runner core; relevance: background heavy-work dispatch.
- [snippet_hermes_agent_batch_runner_spawn](../../code_snippets/snippet_hermes_agent_batch_runner_spawn.md) — spawns background workers; relevance: acknowledge-then-background pattern.
- [snippet_hermes_agent_batch_runner_aggregate](../../code_snippets/snippet_hermes_agent_batch_runner_aggregate.md) — aggregates results; relevance: return result when complete.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — subagent concurrency caps; relevance: `subagents.maxConcurrent` enforcement.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — spawn policy; relevance: delegationMode prefer/own-work decision.
- [snippet_openclaw_agents_subagent_registry_run_manager](../../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md) — tracks active runs; relevance: coordinator tracks active lane tasks/owners.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: per-session run serialization (lock).
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/queue policy; relevance: `messages.queue` collect/debounce/cap/drop.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: tool-posture/smallest-surface rule.
- [snippet_tattletale_queue_deduplication](../../code_snippets/snippet_tattletale_queue_deduplication.md) — queue dedup; relevance: detect-duplicate-requests coordinator behavior.

### oc_concepts_personal_agent_benchmark_pack (9t · 10s · 11d)

**Terms**
- [QA](../../term_dictionary/term_qa.md) — quality assurance / test stack; relevance: a repo-backed QA scenario pack.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: pack reuses OpenClaw's private QA stack.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — small-blast-radius reliability check; relevance: per-scenario reliability smoke checks.
- [Hypothesis Testing](../../term_dictionary/term_hypothesis_testing.md) — assertion-driven verification; relevance: each scenario asserts a specific assistant behavior.
- [Synthetic Data](../../term_dictionary/term_synthetic_data.md) — fake test data; relevance: privacy model uses only fake users/prefs/secrets.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared leased credentials; relevance: pack avoids real credentials (privacy model contrast).
- [Cron](../../term_dictionary/term_cron.md) — scheduled delivery; relevance: fake reminders via local cron delivery scenario.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated workspace; relevance: temporary QA gateway workspace isolation.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned helper run; relevance: subagent-handoff is a baseline behavior under test.

**Docs**
- [oc_concepts_qa_e2e_automation_overview](oc_concepts_qa_e2e_automation_overview.md) — QA stack overview (planned, this series); relevance: the pack reuses this stack.
- [oc_concepts_qa_e2e_automation_live_transports](oc_concepts_qa_e2e_automation_live_transports.md) — live lanes (planned, this series); relevance: pack stays mock-only (explicit contrast).
- [oc_concepts_qa_e2e_automation_architecture](oc_concepts_qa_e2e_automation_architecture.md) — scenario architecture (planned, this series); relevance: pack adds YAML cases under `qa/scenarios/`.
- [band_testing_agents](../band/band_testing_agents.md) — testing agents; relevance: scenario-based agent reliability testing analog.
- [hermes_guide_daily_briefing_bot](../hermes_agent/hermes_guide_daily_briefing_bot.md) — personal-assistant bot; relevance: personal-agent reminder/recall workflow analog.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — proof-backed verification; relevance: proof-backed completion-claim scenarios.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — output handling; relevance: safe tool-followthrough/no-echo checks analog.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — memory recall; relevance: fake preference-recall from workspace memory.
- [hermes_security_skill_memory_settings](../hermes_agent/hermes_security_skill_memory_settings.md) — memory/secret settings; relevance: secret no-echo + redaction privacy checks.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — skill authoring; relevance: pack metadata lives in scenario-packs.ts (extending pattern).
- [pi_sdk_run_modes](../pi/pi_sdk_run_modes.md) — run modes; relevance: mock-openai deterministic local run analog.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills/extensions; relevance: pack lives under `extensions/qa-lab`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the agent-under-test.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory backend; relevance: fake preference-recall from QA workspace memory.

**Snippets**
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript capture; relevance: scenario evidence/transcript checks.
- [snippet_tattletale_queue_deduplication](../../code_snippets/snippet_tattletale_queue_deduplication.md) — dedup logic; relevance: dedup of pack scenarios (`QA_PERSONAL_AGENT_SCENARIO_IDS` order, dups removed).
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — scenario/skill manifest; relevance: `scenario-packs.ts` pack metadata shape.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — availability gating; relevance: pack-selector additive with `--scenario`.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron delivery; relevance: fake reminders via local cron.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM source audit; relevance: fake DM/thread reply routing through qa-channel.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: fake preference recall.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool gating; relevance: approval-denial stop behavior for a sensitive read.
- [snippet_openclaw_agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — output sanitization; relevance: redaction checks use fake markers.

### oc_concepts_presence (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: presence is gateway + connected-clients view.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent duplex transport; relevance: every WS `connect` upserts a presence entry.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — publish/observe state changes; relevance: producers push, consumers (Instances tab) observe.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/method wire protocol; relevance: `connect`/`system-event`/`system-presence` methods.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic liveness beacon; relevance: `system-event` periodic beacons report host/IP/lastInputSeconds.
- [Session Data](../../term_dictionary/term_session_data.md) — connection/runtime state; relevance: in-memory presence map keyed by instanceId.
- [Data Observability](../../term_dictionary/term_data_observability.md) — operational visibility; relevance: presence gives quick operator visibility.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent-runtime observability; relevance: Active/Idle/Stale status indicators.
- [Tunneling](../../term_dictionary/term_tunneling.md) — SSH/port-forward transport; relevance: loopback-IP caveat over SSH tunnels.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell forwarding; relevance: remote `127.0.0.1` addresses ignored.

**Docs**
- [oc_concepts_multi_agent_routing](oc_concepts_multi_agent_routing.md) — agent isolation (planned, this series); relevance: presence shows agent/client availability.
- [oc_concepts_progress_drafts](oc_concepts_progress_drafts.md) — in-progress UI (planned, this series); relevance: both are gateway→client UI side channels.
- [band_websocket_overview](../band/band_websocket_overview.md) — WS channels; relevance: WS connect→presence-style client tracking analog.
- [band_websocket_agent_events](../band/band_websocket_agent_events.md) — agent WS events; relevance: connect/event-driven presence upsert analog.
- [pi_rpc_events](../pi/pi_rpc_events.md) — RPC event stream; relevance: `system-event` beacon analog.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — RPC wire protocol; relevance: connect/method envelope analog.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: gateway-side client connection tracking.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/client wiring; relevance: gateway-and-clients topology.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard; relevance: remote/tunnel client connection caveat analog.
- [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — monitoring active agents; relevance: Instances-tab consumer analog.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosted sessions; relevance: tracking connected client instances analog.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway WS + presence map; relevance: produces/merges/prunes presence entries.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS app; relevance: renders the Instances tab consumer.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent-side presence context.

**Snippets**
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — presence/node events; relevance: node-connect presence upsert.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection handler; relevance: connect→presence entry on handshake.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: loopback-IP caveat over forwarded connections.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity; relevance: `instanceId`-keyed client identity.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: connect handshake outcomes feeding presence.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node-event dedup; relevance: instanceId merge/dedupe analog.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: `system-presence`/`system-event` method wire shape.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: role:node connect → presence entry.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — client-kit WS; relevance: client-side connect handshake (mac/WebChat/CLI).
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android WS session; relevance: another client mode producing presence.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat buffering; relevance: periodic beacon / TTL freshness.

### oc_concepts_progress_drafts (9t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: progress drafts are an OpenClaw chat-UX feature.
- [SSE](../../term_dictionary/term_sse.md) — server-sent streaming; relevance: progress/partial/block modes stream in-progress updates.
- [Slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: Slack Block-Kit `render: "rich"` progress fields.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — per-agent model lane; relevance: `toolProgressDetail` is `agents.defaults` config.
- [Session Features](../../term_dictionary/term_session_features.md) — per-turn run state; relevance: one draft per turn, finalized at turn end.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread/reply targeting; relevance: quote-reply/thread paths disable draft preview.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: progress lines come from tool starts/results.
- [Webhook → Chatbot](../../term_dictionary/term_chatbot.md) — chat-bot message surface; relevance: drafts are one self-updating chat message.
- [Graceful Degradation](../../term_dictionary/term_graceful_degradation.md) — safe fallback; relevance: finalization falls back to fresh send when edit unsafe.

**Docs**
- [oc_concepts_presence](oc_concepts_presence.md) — gateway→client UI (planned, this series); relevance: both are gateway-to-client visual side channels.
- [oc_concepts_multi_agent_bindings_config](oc_concepts_multi_agent_bindings_config.md) — channel config (planned, this series); relevance: `channels.<channel>.streaming.mode` is per-channel config.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming output; relevance: token/block streaming modes analog.
- [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — stream text + tool calls; relevance: progress lines from tool-call events analog.
- [cc_sdk_streaming_input_example](../claude_code/cc_sdk_streaming_input_example.md) — streaming example; relevance: partial-update rendering analog.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — custom streaming API; relevance: partial/progress streaming surface analog.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Slack config; relevance: Slack rich/block rendering config analog.
- [hermes_messaging_discord_advanced](../hermes_agent/hermes_discord_advanced.md) — Discord behavior; relevance: send-one-message-then-edit transport analog.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/chunk settings; relevance: media replies force fresh final send (fallback).
- [cc_statusline_setup](../claude_code/cc_statusline_setup.md) — status line; relevance: compact in-progress status display analog.
- [hermes_messaging_teams_bot](../hermes_agent/hermes_messaging_teams_bot.md) — Teams bot; relevance: Teams native-stream behavior differs (page callout).

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — per-channel transports; relevance: send/edit per Discord/Telegram/Slack/Matrix.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel core; relevance: streaming.mode resolution per channel.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — chat/stream pipeline; relevance: buffered deltas + finalization.

**Snippets**
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — SSE stream; relevance: streaming-delta source for progress.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — session SSE; relevance: per-turn streaming pipeline.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered delta; relevance: compaction of progress-line edits.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send/edit; relevance: send-one-message-then-edit transport.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status reactions; relevance: alternative in-progress status surface.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack Socket Mode; relevance: Slack rich Block-Kit progress fields.
- [snippet_hermes_agent_core_chat_helpers_streaming_loop](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_loop.md) — streaming loop; relevance: emits per-event progress updates.
- [snippet_hermes_agent_core_chat_helpers_streaming_setup](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_setup.md) — streaming setup; relevance: configure streaming mode per channel.
- [snippet_hermes_agent_gw_stream_batching](../../code_snippets/snippet_hermes_agent_gw_stream_batching.md) — stream batching; relevance: maxLines/compaction of progress lines.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — backpressure; relevance: delay/scheduleToolProgress before showing a line.

### oc_concepts_qa_e2e_automation_overview (10t · 11s · 12d)

**Terms**
- [QA](../../term_dictionary/term_qa.md) — quality-assurance test stack; relevance: the page's subject (private QA stack overview).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway under test; relevance: QA exercises OpenClaw channel-shaped behavior.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — smoke/baseline check; relevance: `smoke-ci` deterministic no-live-service proof.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent-runtime observability; relevance: OTel/Prometheus observability smokes.
- [Data Observability](../../term_dictionary/term_data_observability.md) — operational visibility; relevance: evidence/scorecard + coverage inventory.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — observe a bus timeline; relevance: qa-lab observes the transcript/QA bus.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared leased creds; relevance: `qa credentials doctor/add/list/remove` Convex pool.
- [Subagent](../../term_dictionary/term_subagent.md) — handoff under test; relevance: subagent-handoff in the baseline scenario list.
- [Distributed Tracing → Heartbeat](../../term_dictionary/term_heartbeat.md) — liveness/timing signals; relevance: RTT timing + lease heartbeat in evidence.
- [Scenario-Driven Documentation](../../term_dictionary/term_scenario_driven_documentation.md) — scenario-as-spec; relevance: taxonomy coverage IDs are exact proof targets.

**Docs**
- [oc_concepts_qa_e2e_automation_live_transports](oc_concepts_qa_e2e_automation_live_transports.md) — live lanes (planned, this series); relevance: the command surface's live `qa <transport>` lanes.
- [oc_concepts_qa_e2e_automation_architecture](oc_concepts_qa_e2e_automation_architecture.md) — stack architecture (planned, this series); relevance: qa-lab/qa-channel pieces detailed there.
- [oc_concepts_personal_agent_benchmark_pack](oc_concepts_personal_agent_benchmark_pack.md) — benchmark pack (planned, this series); relevance: reuses this stack via `--pack`.
- [band_testing_agents](../band/band_testing_agents.md) — agent testing; relevance: end-to-end agent test-harness analog.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel setup; relevance: `qa:otel:smoke` OTLP trace/metric/log assertions.
- [cc_otel_traces](../claude_code/cc_otel_traces.md) — OTel traces; relevance: `openclaw.run`/`openclaw.harness.run` span shape checks.
- [cc_otel_metrics_reference](../claude_code/cc_otel_metrics_reference.md) — OTel metrics; relevance: Prometheus scrape metric-family checks.
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK observability; relevance: GenAI semantic-convention span checks.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: operator two-pane dashboard flow analog.
- [hermes_web_dashboard_overview](../hermes_agent/hermes_web_dashboard_overview.md) — dashboard UI; relevance: Control-UI / QA-Lab two-pane site analog.
- [cc_dynamic_workflows](../claude_code/cc_dynamic_workflows.md) — workflow orchestration; relevance: profile-backed `qa run` dispatch analog.
- [cc_verification_loop](../claude_code/cc_verification_loop.md) — verification loop; relevance: what-worked/failed/blocked reporting analog.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — extensions (qa-lab/qa-channel); relevance: the QA stack pieces live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway lane; relevance: child QA gateway + Control-UI dashboard.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent under test; relevance: the agent the QA mission drives.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — Control UI / QA site; relevance: the two-pane operator site.

**Snippets**
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript; relevance: observed-bus transcript for the report.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect outcomes; relevance: readiness/connect checks per lane.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — probe execution; relevance: observability smokes assert exported signals.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: scrape rejects unauth + checks metric families.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost summary; relevance: token-efficiency / parity-report data.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — latency/cache status; relevance: runtime-axis parity + RTT timing.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — scenario availability; relevance: `--surface`/`--category` profile filtering.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — scenario manifest; relevance: taxonomy.yaml profile membership.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth; relevance: two-pane QA site dashboard access.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: approval-metadata delivery under test.
- [snippet_hermes_agent_core_credential_pool_dataclass](../../code_snippets/snippet_hermes_agent_core_credential_pool_dataclass.md) — credential-pool shape; relevance: `qa credentials` Convex pool analog.

### oc_concepts_qa_e2e_automation_live_transports (10t · 12s · 11d)

**Terms**
- [QA](../../term_dictionary/term_qa.md) — quality-assurance lanes; relevance: live-transport QA against real accounts.
- [Slack](../../term_dictionary/term_slack.md) — Slack platform; relevance: Slack QA lane + driver/SUT app setup.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared leased creds; relevance: Convex pool kinds telegram/discord/slack/whatsapp.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway under test; relevance: child QA gateway runs the real plugin.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — baseline smoke; relevance: `*-canary` is the first scenario per lane.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bot/app tokens; relevance: `xoxb-`/`xapp-` Slack tokens, BotFather tokens.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack event delivery; relevance: SUT app needs `connections:write` Socket Mode.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread/reply behavior; relevance: thread-follow-up + thread-isolation scenarios.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound event delivery; relevance: SUT app event subscriptions/inbound observation.
- [Idempotency](../../term_dictionary/term_idempotency.md) — restart-safe replay; relevance: `*-restart-resume`/replay-dedupe scenarios.

**Docs**
- [oc_concepts_qa_e2e_automation_overview](oc_concepts_qa_e2e_automation_overview.md) — QA overview (planned, this series); relevance: the command surface that launches these lanes.
- [oc_concepts_qa_e2e_automation_architecture](oc_concepts_qa_e2e_automation_architecture.md) — adapter architecture (planned, this series); relevance: live runners plug into the qa-lab seam.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack setup; relevance: Slack app/scope/token provisioning analog.
- [hermes_messaging_slack_config](../hermes_agent/hermes_messaging_slack_config.md) — Slack config; relevance: bot/app token + channel id config analog.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram setup; relevance: BotFather bot-to-bot + group-id env analog.
- [hermes_discord_setup](../hermes_agent/hermes_discord_setup.md) — Discord setup; relevance: guild/channel/bot-token env analog.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp Web; relevance: WhatsApp Web account/auth-archive lane analog.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pools; relevance: direct Convex-pool lease/heartbeat/release analog.
- [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — Claude in Slack; relevance: Slack bot app setup analog.
- [cc_slack_setup_and_routing](../claude_code/cc_slack_setup_and_routing.md) — Slack routing; relevance: channel/bot routing setup analog.
- [band_chat_rooms_and_routing](../band/band_chat_rooms_and_routing.md) — chat routing; relevance: driver/SUT two-bot channel routing analog.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: real Telegram/Discord/Slack/WhatsApp transports under test.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging adapters; relevance: per-transport inbound/outbound observation.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — child QA gateway; relevance: hosts the SUT bot per lane.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/credentials; relevance: token handling + content redaction in artifacts.

**Snippets**
- [snippet_hermes_agent_core_credential_pool_dataclass](../../code_snippets/snippet_hermes_agent_core_credential_pool_dataclass.md) — pool payload shape; relevance: broker `admin/add` payload schema per kind.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — pool seeding; relevance: `qa credentials add --payload-file`.
- [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — lease selection; relevance: exclusive lease acquisition per run.
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — pool entry/lease; relevance: lease heartbeat + release on shutdown.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack Socket Mode; relevance: SUT app `connections:write` event delivery.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: driver/SUT bot tokens + intents.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport; relevance: two-bot group + BotFather config.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: shared live-transport contract checklist.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel/DM audit; relevance: content-redaction in observed-message artifacts.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: `--credential-source env|convex` resolution.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval; relevance: native Slack/WhatsApp approval scenarios.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status reactions; relevance: Discord status-reaction Mantis scenario.

### oc_concepts_qa_e2e_automation_architecture (10t · 11s · 11d)

**Terms**
- [QA](../../term_dictionary/term_qa.md) — QA test stack; relevance: the architecture of the QA stack.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: qa-lab/runner sit around the OpenClaw gateway.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — observe inbound/outbound; relevance: adapter owns inbound/outbound observation.
- [Adapter Pattern](../../term_dictionary/term_adapter_pattern.md) — pluggable transport adapter; relevance: qa-channel is the first transport adapter on the seam.
- [Scenario-Driven Documentation](../../term_dictionary/term_scenario_driven_documentation.md) — scenario-as-spec; relevance: YAML scenario files are the source of truth per run.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — inbound/outbound event flow; relevance: inject inbound / observe outbound events.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — provider lane selection; relevance: mock-openai vs aimock provider mock lanes.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared creds; relevance: transport adapters lease pool credentials.
- [Data Observability](../../term_dictionary/term_data_observability.md) — evidence/reporting; relevance: Markdown evidence report from the bus timeline.
- [Canary Testing](../../term_dictionary/term_canary_testing.md) — baseline coverage; relevance: scenario packs exercise the channel contract.

**Docs**
- [oc_concepts_qa_e2e_automation_overview](oc_concepts_qa_e2e_automation_overview.md) — QA overview (planned, this series); relevance: this details the overview's pieces.
- [oc_concepts_qa_e2e_automation_live_transports](oc_concepts_qa_e2e_automation_live_transports.md) — live lanes (planned, this series); relevance: live runners are adapters on this seam.
- [oc_concepts_personal_agent_benchmark_pack](oc_concepts_personal_agent_benchmark_pack.md) — benchmark pack (planned, this series); relevance: a scenario pack added under `qa/scenarios/`.
- [band_creating_adapters_patterns](../band/band_creating_adapters_patterns.md) — adapter patterns; relevance: transport-adapter design / decision-rule analog.
- [band_creating_adapters_implementation](../band/band_creating_adapters_implementation.md) — adapter implementation; relevance: adding-a-channel two-step (adapter + scenario pack) analog.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — platform adapter plugin; relevance: runner-plugin mounting analog.
- [hermes_adding_platform_adapter_builtin](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — built-in adapter; relevance: built-in vs plugin transport split analog.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surfaces; relevance: `qaRunners` declaration in plugin manifest analog.
- [cc_build_a_channel](../claude_code/cc_build_a_channel.md) — building a channel; relevance: adding-a-channel adapter contract analog.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: runner-plugin entrypoint/registration analog.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — provider registration; relevance: provider-registry (mock-openai/aimock) routing analog.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — extensions (qa-lab/providers); relevance: qa-lab host + provider lanes live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway seam; relevance: `browser.request` Control-UI seam + child gateway config.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: transport adapters reuse channel plugins.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/plugins; relevance: runner plugins + provider registry.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the transport-adapter seam definition.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry; relevance: mount runner without a competing root command.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: runner-plugin load/register lifecycle.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: `openclaw.plugin.json` `qaRunners` declaration.
- [snippet_openclaw_context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — registry factories; relevance: provider registry instead of name-branching.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator; relevance: mock-openai/aimock provider-lane pattern.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model-catalog normalize; relevance: per-provider model config/defaults.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — scenario manifest; relevance: YAML scenario file fields (title/scenario/flow).
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — transcript capture; relevance: observed-bus timeline → Markdown report.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — dispatch handler; relevance: inject-inbound → agent dispatch in scenarios.

> ONLY non-existing targets; they are explicitly marked "(planned, this series)" and are created by this
> sub-plan (entry point `entry_openclaw_docs` is created at master W1). Missing-term substitutions confirmed:
> `term_session` → `term_session_features`/`term_session_data`; `term_observability`/`term_opentelemetry`/
> `term_prometheus`/`term_discord`/`term_telegram`/`term_whatsapp` are absent and were NOT cited (substituted
> with `term_observability_agent_systems`/`term_data_observability`/`term_slack`/`term_qa`/`term_socket_mode`/
> `term_webhook`). `term_scenario_driven_documentation` CONFIRMED present (used in notes 8 + 10).

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are digested as `oc_*` doc notes by this sub-plan, NOT as new
`term_dictionary` entries; the only term interaction is **linking existing** terms. **Expected 0 new
`term_dictionary` captures for co05.**

| Term (from source) | Disposition |
|---|---|
| agent / agentId / agentDir | Documented in note 1/2 (`oc_concepts_multi_agent_*`); link existing `term_openclaw`, `term_autonomous_coding_agents`, `term_agent_harness`. No new term. |
| binding / routing rules / accountId / peer match | Documented in note 1/2; link `term_provider_routing`, `term_thread_binding_policy`. No new term. |
| auth profiles / token sink / auth-profiles.json | Documented in note 3 (`oc_concepts_oauth`); link `term_auth_profile`, `term_oauth_token`, `term_authentication`. No new term. |
| OAuth / PKCE / setup-token / refresh+expiry | Documented in note 3; link existing `term_oauth`, `term_pkce`, `term_oauth_token`. No new term. |
| OpenAI Codex / ChatGPT OAuth / Anthropic Claude CLI | Provider/product names — documented as config, link `term_claude`, `term_third_party_genai_services`. Not promoted. |
| specialist lane / lane contract / coordinator | Documented in note 4 (`oc_concepts_parallel_specialist_lanes`); link `term_message_queue`, `term_subagent`. No new term. |
| presence / instanceId / system-presence / system-event | Documented in note 6 (`oc_concepts_presence`); link `term_websocket`, `term_observer_pattern`. No new term. |
| progress draft / streaming mode (partial/block/progress) | Documented in note 7 (`oc_concepts_progress_drafts`); link `term_sse`. No new term. |
| qa-lab / qa-channel / qa-matrix / mock-openai / aimock | Documented in notes 8–10 (`oc_concepts_qa_e2e_automation_*`); link `term_qa`. No new term. |
| Convex credential pool / lease | Documented in note 9; link existing `term_credential_pool` (verified present). No new term. |
| Mantis / Crabbox / character-eval / personal-agent pack | Documented in notes 5/8/9 + sibling `concepts/mantis` (co03); link `term_qa`, `term_canary_testing`. No new term. |
| transport adapter / runner plugin / scenario helper | Documented in note 10; link `term_observer_pattern`. No new term. |

**New-term candidates: NONE.** Every cross-cutting concept either has an existing term note (verified above)
or is OpenClaw-product vocabulary whose home is an `oc_*` doc note. If augment's Step-2d re-scan surfaces a
genuinely reusable cross-cutting term with no existing note (e.g. a generic "token sink" auth pattern), it
would be captured via `/tessellum-capture-term-note` + added to `acronym_glossary_ai_agents.md` (or the
auth/security glossary) — not expected.

## Term-Note Authoring Requirements

**N/A (0 new terms).** co05 authors zero `term_dictionary` notes. Inherited from master: any new term (none

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + body sections (`## Overview`/`## Related Notes`/`## References` + bold footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: each note faithful to its `inbox/openclaw_docs/concepts/<page>.md` section(s); no invented config keys | diff vs mirror; spot-check config snippets verbatim |
| G3 | Density + Coverage: ≤400 lines / ≤2500 words / ≤6 code blocks per note; every mapped H2/H3 covered | `wc -w`, fence count; Section Coverage Map |
| G4 | Cross-Reference: ≥6 relevancy-selected terms + repo/sibling/doc links per note, each with relevance statement | manual review vs Candidate Cross-References |
| G6 | Broken-link fix: 0 broken relative links after reindex | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | `entry_openclaw_docs.md` rows + Inlinks section |
| G8 | In-degree ≥1 (anti-island) per new note | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_multi_agent_routing oc_concepts_multi_agent_bindings_config oc_concepts_oauth oc_concepts_parallel_specialist_lanes oc_concepts_personal_agent_benchmark_pack oc_concepts_presence oc_concepts_progress_drafts oc_concepts_qa_e2e_automation_overview oc_concepts_qa_e2e_automation_live_transports oc_concepts_qa_e2e_automation_architecture"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
# (per-target existence checks run here before commit)
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source fences | Reproduced fences (≤6) | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_concepts_multi_agent_routing | concept | 650 | (shares 6) | ≤3 (QMD memory + routing-order config) | ✅ |
| 2 | oc_concepts_multi_agent_bindings_config | procedure | 700 | (shares 6) | ≤6 (agents add + per-channel binding + sandbox/tools) | ✅ |
| 3 | oc_concepts_oauth | concept | 700 | 3 | ≤3 (provider auth login, Codex login, session override) | ✅ |
| 4 | oc_concepts_parallel_specialist_lanes | argument | 550 | 2 | ≤2 (queue/concurrency config + lane contract template) | ✅ |
| 5 | oc_concepts_personal_agent_benchmark_pack | concept | 450 | 1 | 1 (`qa suite --pack personal-agent`) | ✅ |
| 6 | oc_concepts_presence | model | 500 | 0 | 0 | ✅ |
| 7 | oc_concepts_progress_drafts | procedure | 700 | 13 | ≤6 (enable, mode table is prose, labels, progress JSON, render, maxLines) | ✅ |
| 8 | oc_concepts_qa_e2e_automation_overview | concept | 750 | (shares 30) | ≤4 (qa run profile, qa:lab:up, observability smoke, multipass) | ✅ |
| 9 | oc_concepts_qa_e2e_automation_live_transports | procedure | 800 | (shares 30) | ≤6 (per-lane invoke + Slack manifest excerpt + Convex creds) | ✅ |
| 10 | oc_concepts_qa_e2e_automation_architecture | model | 650 | (shares 30) | ≤4 (scenario YAML shape, mock lanes, helper names, character-eval) | ✅ |

No note approaches caps. The fence-heavy pages (`progress-drafts` 13, `qa-e2e-automation` 30) are kept ≤6 per
note by selective verbatim reproduction (and by the 3-way QA split). All notes ≤800w, ≤400 lines.

## Entry Point Decision (inherited from master)

co05 contributes **10 rows** to `entry_openclaw_docs.md` (the >30-note series hub CREATED as a master
pre-step W1) under the **Concepts** section, grouped as: "Multi-agent & routing" (notes 1–2), "Auth" (note 3),
"Operations & UX" (notes 4, 6, 7), "QA & benchmarking" (notes 5, 8, 9, 10). Each note receives its
entry-point back-link at finalization (satisfies G7/G8 — ≥1 outside-folder inbound link). Parent-hub wiring
not re-done per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; each new note needs ≥1 for G7/G8):
- `entry_openclaw_docs.md` (planned master pre-step) → ALL 10 notes (primary G8 satisfier).
- `term_openclaw.md` → notes 1, 3 (agent isolation + OAuth are core OpenClaw concepts).
- `term_oauth.md` + `term_pkce.md` + `term_oauth_token.md` → note 3.
- `term_qa.md` → notes 5, 8, 9, 10.
- `term_credential_pool.md` → note 9.
- `term_websocket.md` → note 6 (presence over WS).
- `term_sse.md` → note 7 (streaming/progress).
- `term_message_queue.md` → note 4 (lane contention/queue).
- `repo_openclaw_agents.md` → notes 1, 2, 3, 4 (code↔docs cross-link).
- `repo_openclaw_gateway.md` → notes 6, 8, 9.
- `repo_openclaw_sessions.md` → notes 1, 2, 4.
- `pi_provider_auth.md` (existing pi doc) → note 3 (sibling-tool auth analog).

## Pacing Rules (inherited from master)

One execution phase (10 notes). Cap dynamic-workflow fan-out ≤30 agents/run; embed the per-note contract
manifest in the dispatch script. Re-read each source page before authoring its note(s); reproduce config
snippets verbatim; one building_block per note. Reindex incrementally; verify `note_links` (in-degree ≥1)
in the same turn after the phase; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment:** per-note Related-Notes mapping locked to RAISED floors (**≥8 `term_dictionary`
terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** per note, PLUS relevant
`repo_openclaw*` and sibling `oc_*`). All seven source pages were re-read in full from the mirror
(`inbox/openclaw_docs/concepts/`); measured words re-confirmed identical to the plan's Source table
(multi-agent 2,466 / oauth 1,196 / parallel-specialist-lanes 576 / personal-agent-benchmark-pack 436 /
presence 584 / progress-drafts 1,798 / qa-e2e-automation 6,393 = **13,449 total**). Selection is by content

**Per-note locked counts** (terms / snippets / docs; repos additional):

| # | Note | BB | Terms | Snippets | Docs | Repos | Floors met |
|---|---|---|---:|---:|---:|---:|---|
| 1 | oc_concepts_multi_agent_routing | concept | 10 | 12 | 11 (6 existing + 4 sibling + 1 band) | 3 | ✅ |
| 2 | oc_concepts_multi_agent_bindings_config | procedure | 9 | 12 | 11 (8 existing + 3 sibling) | 5 | ✅ |
| 3 | oc_concepts_oauth | concept | 10 | 11 | 12 (11 existing + 1 sibling) | 3 | ✅ |
| 4 | oc_concepts_parallel_specialist_lanes | argument | 10 | 11 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 5 | oc_concepts_personal_agent_benchmark_pack | concept | 9 | 10 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| 6 | oc_concepts_presence | model | 10 | 11 | 11 (9 existing + 2 sibling) | 3 | ✅ |
| 7 | oc_concepts_progress_drafts | procedure | 9 | 12 | 11 (9 existing + 2 sibling) | 3 | ✅ |
| 8 | oc_concepts_qa_e2e_automation_overview | concept | 10 | 11 | 12 (9 existing + 3 sibling) | 4 | ✅ |
| 9 | oc_concepts_qa_e2e_automation_live_transports | procedure | 10 | 12 | 11 (9 existing + 2 sibling) | 4 | ✅ |
| 10 | oc_concepts_qa_e2e_automation_architecture | model | 10 | 11 | 11 (8 existing + 3 sibling) | 4 | ✅ |

All 10 notes meet **terms ≥8, snippets ≥10, docs ≥10**.

**Step-2d re-scan (newly-surfaced undigested terms):** NONE that need a NEW `term_dictionary` capture. The
re-read confirmed every cross-cutting concept either (a) has an existing term note now linked
(`term_socket_mode`, `term_webhook`, `term_tunneling`, `term_ssh`, `term_synthetic_data`, `term_heartbeat`,
`term_adapter_pattern`, `term_event_driven_architecture`, `term_scenario_driven_documentation`,
`term_persona`, `term_access_control`, `term_chatbot`, `term_graceful_degradation`, `term_throttling`,
vocabulary whose home is an `oc_*` doc note in this sub-plan. **New-term candidates: NONE** — consistent with
the master's corpus-wide design decision (OpenClaw vocabulary → `oc_*` doc notes, not `term_dictionary`). Best-fit
glossary if a future term were ever needed: `0_entry_points/acronym_glossary_ai_agents.md` (agentic/LLM) or the
auth/security glossary; not expected for co05.

**Verified missing-target substitutions (carried from plan-digestion, re-confirmed):** `term_session` absent →
`term_session_features`/`term_session_data`; `term_observability`/`term_opentelemetry`/`term_prometheus`/
`term_discord`/`term_telegram`/`term_whatsapp` absent → NOT cited (used `term_observability_agent_systems`/
`term_data_observability`/`term_slack`/`term_qa` instead). `term_scenario_driven_documentation` CONFIRMED
present (the plan-digestion soft candidate) — used in notes 8 and 10.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_co05.md   Date: 2026-06-21
```

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step — ≥8 terms + floors (≥10 snippets, ≥10 docs), relevance-selected, each link has a relevance statement | **PASS** | "## Per-Note Related Notes Mapping (LOCKED)" present; all 10 notes meet ≥8t/≥10s/≥10d (see Augmentation Report table); every link rendered `- [Name](relpath.md) — what it is; relevance: …`. |
| CP2 | 9-GATE present per execution phase (G1-G6 + G7/G8 discoverability) | **PASS** | "## Per-Phase Validation Gate (G1–G9)" table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7 discoverability, G8 in-degree — for the single P1 phase (10 notes). |
| CP3 | Entry point inherited — `entry_openclaw_docs` created at master W1 | **PASS** | "## Entry Point Decision (inherited from master)": co05 contributes 10 rows to `entry_openclaw_docs.md` (created as master pre-step W1, >30-note series ⇒ CREATE required); per-note back-link at finalization. `entry_openclaw_docs` confirmed NOT yet in DB (correctly planned). |
| CP4 | Size — ≤30 notes (or split) | **PASS** | 10 planned notes (well under 30). 2 source pages split (multi-agent→2, qa-e2e→3) per "## Split Decisions". |
| CP5 | Format derived from existing target-dir notes (not invented) | **PASS** | Master Format Definition derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) corpora: `## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → bold `**Source**/**Last Updated**/**Status**` footer; YAML field order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group. Matches the verified existing `cc_*`/`pi_*` notes used as cross-refs. |
| CP6 | Density — borderline → split promoted | **PASS** | "## Density Re-Assessment": all 10 notes ≤800w, ≤400 lines, ≤6 reproduced fences; the two fence-heavy pages (progress-drafts 13, qa-e2e 30) kept ≤6/note via selective verbatim + the 3-way QA split. No borderline unaddressed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 pages from `inbox/openclaw_docs/concepts/` at augment; `wc -w` re-confirmed each (multi-agent 2466, oauth 1196, lanes 576, benchmark-pack 436, presence 584, progress-drafts 1798, qa-e2e 6393 = 13449) — identical to the plan's Source table (ratio 1.0). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + multi-source mandate | **PASS** | "## Undigested Terms Plan" present (disposition per source term = link existing, 0 new captures); "## Term-Note Authoring Requirements" present (N/A — 0 new terms; master multi-source mandate inherited if any term were ever added). |
| CP8f | Slug specificity / collision audit (all notes, term AND doc) | **PASS** | Step-10.5f generalized to all 10 planned `oc_*` doc notes: dedup ran across `term_dictionary/` AND `resources/documentation/` AND `repo_openclaw*` (master dedup policy). No `oc_*` doc duplicates an existing term/doc/repo (all 10 are new `oc_concepts_*` slugs; series-prefix collision-free, confirmed `entry_openclaw_docs`/no `oc_concepts_*` in DB). 0 new term slugs ⇒ no slug-rename needed. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | "## Inlinks (existing notes → new notes)" maps ≥1 outside-folder inbound link per note (`entry_openclaw_docs` → all 10 = primary G8 satisfier; plus term/repo inlinks); G7/G8 in the gate table; inlink-add is a finalization execution step, not "recommended". |

**RESULT: 9/9 (CP1-CP9 incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.

## Plan Amendments (by master agent during execution)

| Date | Section | Original | Amended | Rationale |
|---|---|---|---|---|
| 2026-06-23 | Planned Notes | oc_concepts_qa_e2e_automation_live_transports (1 procedure note, all live-transport content) | SPLIT into oc_concepts_qa_e2e_automation_live_transports (operator flow + observability smokes + live-transport coverage matrix + Multipass) + oc_concepts_qa_e2e_automation_transport_reference (the per-channel Telegram/Discord/Slack/WhatsApp env+scenario+app-setup reference + Convex credential pool) | Source `qa-e2e-automation.md` is ~5,000w; the single note was being compressed to fit ≤2500w, losing the per-channel setup reference. User directive: split, do not compress/omit. Both halves are procedure BB. co05 note count 10 → 11. |
