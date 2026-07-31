---
title: Hermes Agent Docs Digestion — Sub-Plan 11a — Messaging Gateway + Telegram + Discord
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
pages:
  - user-guide/messaging/index.md
  - user-guide/messaging/telegram.md
  - user-guide/messaging/discord.md
---

# Sub-Plan 11a: Messaging Gateway concepts + Telegram + Discord

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP11a's note
> filenames/BBs/coverage are defined. **Part a of the SP11 split** (master row 11, split a/b): SP11a
> owns the cross-cutting GATEWAY concepts + the two richest team-chat platforms (Telegram, Discord);
> SP11b owns the remaining team-chat platforms (slack, matrix, mattermost, teams(+meetings), google_chat).

## Scope

The **Messaging Gateway** — the single background process that bridges 20+ chat platforms to the Hermes
agent — plus end-to-end setup for **Telegram** and **Discord**, the two most feature-complete platforms.
This is where the **cross-cutting gateway concepts** live (gateway architecture, the per-chat session
store + reset policies, intentional silence tokens, DM pairing, admin/user tiers, the circuit breaker,
multi-platform day-2 ops), so downstream messaging sub-plans (SP11b, SP12, SP13) link back to
`hermes_messaging_gateway_architecture` and `hermes_gateway_operations` rather than re-explaining the
gateway. Source = 3 mirrored pages in `inbox/hermes_agent_docs/` (all substantive). **P2 / features-messaging.**

## Content Strategy

- **One BB per note.** `index.md` mixes a model (gateway architecture + session/silence data model) with
  a long procedural ops surface (setup/commands/security/service-mgmt/multi-platform ops) → split into 2
  notes (1 model + 1 procedure). `telegram.md` (9147w, 56 code) and `discord.md` (6685w, 27 code) each far
  exceed the density caps → each splits into a setup procedure + an advanced/voice/topics(forum) procedure.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: voice/TTS/STT
  feature concepts (SP08), per-platform session-key + FTS5 storage internals (SP02 `hermes_session_search_storage`),
  cron scheduler (SP06), gateway-config knobs that live in `config.yaml` (SP02 `hermes_messaging_media_settings`),
  the API-server/webhook adapters (SP09 `api-server`, SP12 `webhooks`), the developer-side adapter-authoring
  guide (SP19 `adding-platform-adapters`), security model (SP03 `security`), and the remaining team-chat
  platforms (SP11b slack/matrix/mattermost/teams/google_chat).
- **Collision (augment): the "messaging gateway" concept is NOT covered by any existing term.** The master
  caution list flags `messaging gateway ≠ term_api_gateway`; the collision audit (below) confirms
  `term_api_gateway` (active), `term_mcp_gateway` (active), `term_agentcore_gateway` (active),
  `term_nat_gateway` (active) are all DIFFERENT concepts → SP11a OWNS `term_messaging_gateway`. `term_dm_pairing`
  and `term_silence_token` are ABSENT → SP11a owns both.
- `term_voice_wake` (active) is the CLI wake-word concept, NOT the Telegram/Discord voice-message flow → do
  NOT recreate; link only where genuinely relevant. Voice *mode* (`term_voice_mode`, SP08, not yet existing)
  is a forward-ref, not owned here.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/messaging/index.md | 4350 | 25 | MIXED model+procedure | 2 (split) |
| user-guide/messaging/telegram.md | 9147 | 56 | procedure | 2 (split) |
| user-guide/messaging/discord.md | 6685 | 27 | procedure | 2 (split) |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **6 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_messaging_gateway_architecture.md` | model | index §intro, §Platform Comparison (capability matrix), §Architecture (adapters→session store→AIAgent→cron mermaid), §Intentional Silence Tokens, §Session Management (Persistence, Reset Policies), §Platform-Specific Toolsets | ~1500 | The gateway model: one background process fanning 20+ platform adapters through a per-chat session store into the AIAgent + 60s cron tick; the platform capability matrix (voice/images/files/threads/reactions/typing/streaming); `[SILENT]`/`NO_REPLY` silence tokens; per-platform reset policies (daily/idle/both); per-platform toolset map. |
| 2 | `hermes_gateway_operations.md` | procedure | index §Quick Setup (`gateway setup`), §Gateway Commands, §Chat Commands, §Security (allowlists, GATEWAY_ALLOW_ALL_USERS), §DM Pairing, §Admins vs Regular Users (+config, `/whoami`), §Interrupting the Agent (+queue/steer busy-input), §Tool Progress Notifications, §Background Sessions (How It Works, notifications, use cases), §Service Management (systemd/launchd), §Operating a multi-platform gateway (`/platform`, circuit breaker, restart/resume notifications, mobile-friendly defaults, progress cleanup) | ~2400 | Day-2 gateway ops: interactive `hermes gateway setup`, the `gateway`/`install`/`start`/`stop`/`status` command set, in-chat slash commands, allowlist + `GATEWAY_ALLOW_ALL_USERS` security, DM pairing handshake, admin/user tier split + `/whoami`, interrupt/queue/steer, `/background` isolated sessions, systemd/launchd service install, and multi-platform ops (`/platform` pause/resume, circuit breaker, restart auto-resume). |
| 3 | `hermes_telegram_setup.md` | procedure | telegram §intro, §1 BotFather, §2 Customize, §3 Privacy Mode (+disable, observe-unmentioned, env), §4 Find User ID, §5 Configure Hermes (interactive/manual/start), §Webhook Mode (+config, Fly.io), §Proxy Support, §Home Channel (+cron topic), §DNS-over-HTTPS Fallback IPs, §Troubleshooting, §Security | ~2200 | End-to-end Telegram bot setup: create + customize a BotFather bot, the privacy-mode gotcha (and observe-unmentioned mode), find your numeric user ID, configure via wizard or `.env`, polling-vs-webhook deployment (incl. Fly.io secret + `fly.toml`), proxy + DoH fallback IPs, home channel + cron thread, troubleshooting + token security. |
| 4 | `hermes_telegram_advanced.md` | procedure | telegram §Sending Generated Files from Docker (+`MEDIA:` extensions), §Voice Messages (STT/TTS, skip-STT, local Bot API 2GB), §Large Files via Local Bot API Server (steps 1-6, `local_mode`), §Group Chat Usage (require_mention/mention_patterns/exclusive_bot_mentions/ignored_threads/multi-bot), §Private Chat Topics (Bot API 9.4), §Multi-session DM mode (`/topic`), §Group Forum Topic Skill Binding, §Recent Bot API Features (streaming transports, rich messages, link previews), §Group Allowlisting (+guest_mode), §Slash Command Access Control, §Interactive Model Picker, §Message Reactions, §Per-Channel Prompts, §Exec Approval, §clarify, §notifications/status-edits/pin | ~2400 | Advanced Telegram: `MEDIA:` attachment delivery (Docker-host path gotcha), voice STT/TTS + skip-STT, the local telegram-bot-api server for >20MB (2GB) files, group triggering (require_mention / mention_patterns / exclusive_bot_mentions / multi-bot fleets), DM/group forum topics + `/topic` multi-session mode + skill binding, Bot-API-9.5 streaming transports + rich messages, group allowlisting + guest_mode, slash-command access tiers, model picker, reactions, per-channel prompts, exec-approval/clarify, notification volume. |
| 5 | `hermes_discord_setup.md` | procedure | discord §intro, §How Hermes Behaves (DM/channel/free-response/thread/shared/ignore-no-mention), §Step 1 Create Application, §Step 2 Create Bot, §Step 3 Privileged Gateway Intents, §Step 4 Get Token, §Step 5 Invite URL (installation tab / manual / permissions / integers), §Step 6 Invite to Server, §Step 7 Find User ID, §Step 8 Configure Hermes, §Troubleshooting, §Security (+RBAC roles) | ~2000 | End-to-end Discord bot setup: create the application + bot, the critical Privileged Gateway Intents step (Message Content + Server Members), get the token, build the OAuth2 invite URL + permission integers, invite to a server, find your user ID, configure via wizard or `.env`, troubleshooting (the intent footgun), and security incl. role-based access (`DISCORD_ALLOWED_ROLES`) + mention control. |
| 6 | `hermes_discord_advanced.md` | procedure | discord §Discord Gateway Model, §Session Model in Discord (+`group_sessions_per_user`, interrupts/concurrency), §Configuration Reference (env vars table + config.yaml: require_mention/thread_require_mention/free_response_channels/auto_thread/reactions/ignored/no_thread/channel_prompts/history_backfill(+limit)/tool_progress), §Slash Command Access Control, §Interactive Model Picker, §Native Slash Commands for Skills (+disable), §Sending Media, §Receiving Arbitrary File Types, §clarify, §Home Channel, §Voice Messages (+voice_fx mixer), §Forum Channels | ~2300 | Advanced Discord: the full-gateway model (not a stateless webhook), per-user vs shared session isolation (`group_sessions_per_user`) + interrupt/concurrency semantics, the env-var + `config.yaml` configuration reference (mention/threading/backfill/tool-progress), slash-command access tiers, native skill slash-command registration, media send/receive (incl. arbitrary-file allowlist), `voice_fx` mixer for voice channels, and forum-channel handling. |

**SP11a totals:** 6 notes · model 1 · procedure 5 · concept 0 (concepts owned by existing/owned term notes).
3 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 6 · model 1 · procedure 5 · concept 0 (gateway/silence/pairing concepts are term notes — 3 owned by SP11a).
- Source: 3 digested pages (~19.8K words) → ~12.8K words of notes (compression via link-outs to SP02/08/09/12/19 + code curation).
- BB mix: procedure 83%, model 17%.
- New term notes owned by SP11a: **3** (`term_messaging_gateway`, `term_dm_pairing`, `term_silence_token`).

## Section Coverage Map

```
index.md (4350w)
├── intro (single background process, voice link, Nous Portal tip) ─ → Note 1 (voice→SP08; portal→SP14)
├── Platform Comparison (capability matrix) ──────────────────────── → Note 1
├── Architecture (adapters→store→AIAgent→cron mermaid) ───────────── → Note 1
├── Intentional Silence Tokens ([SILENT]/NO_REPLY) ───────────────── → Note 1 (owns term_silence_token)
├── Quick Setup / Gateway Commands / Chat Commands ──────────────── → Note 2
├── Session Management (Persistence, Reset Policies) ─────────────── → Note 1 (session storage internals→SP02)
├── Security (allowlists, GATEWAY_ALLOW_ALL_USERS) ──────────────── → Note 2
├── DM Pairing ──────────────────────────────────────────────────── → Note 2 (owns term_dm_pairing)
├── Admins vs Regular Users (+config, /whoami) ──────────────────── → Note 2
├── Interrupting the Agent (queue/steer busy-input) ─────────────── → Note 2
├── Tool Progress Notifications / Background Sessions ───────────── → Note 2 (compression→SP18)
├── Service Management (systemd/launchd) ───────────────────────── → Note 2
├── Operating a multi-platform gateway (/platform, breaker, notifications, mobile defaults, cleanup) → Note 2
└── Platform-Specific Toolsets (per-platform toolset map) ───────── → Note 1 (toolsets ref→SP21)
telegram.md (9147w)
├── intro / 1 BotFather / 2 Customize / 3 Privacy / 4 User ID / 5 Configure → Note 3
├── Webhook Mode (+Fly.io) / Proxy Support / Home Channel (+cron topic) → Note 3
├── DNS-over-HTTPS Fallback IPs / Troubleshooting / Security ────── → Note 3 (security→SP03)
├── Sending Files from Docker (+MEDIA: extensions) ─────────────── → Note 4 (docker backend→SP02)
├── Voice Messages (STT/TTS, skip-STT) / Large Files (Local Bot API) → Note 4 (voice/STT/TTS→SP08)
├── Group Chat Usage / multi-bot / Private Chat Topics / /topic / Group Forum Topic Skill Binding → Note 4 (skills→SP05)
├── Recent Bot API (streaming transports, rich messages, link previews) → Note 4 (streaming config→SP02)
└── Group Allowlisting (+guest_mode) / Slash Access / Model Picker / Reactions / Per-Channel Prompts / Exec Approval / clarify / notifications / status-edits / pin → Note 4
discord.md (6685w)
├── intro / How Hermes Behaves (DM/channel/free-response/thread/shared/ignore) → Note 5
├── Step 1-8 (Application, Bot, Intents, Token, Invite URL, Invite, User ID, Configure) → Note 5
├── Troubleshooting / Security (+RBAC roles, Mention Control) ───── → Note 5 (security→SP03)
├── Discord Gateway Model / Session Model (group_sessions_per_user, interrupts/concurrency) → Note 6 (session storage→SP02)
├── Configuration Reference (env vars + config.yaml all sub-sections + tool_progress) → Note 6 (config knobs→SP02)
├── Slash Access / Model Picker / Native Slash Commands for Skills (+disable) → Note 6 (skills→SP05)
├── Sending Media / Receiving Arbitrary File Types / clarify / Home Channel → Note 6
└── Voice Messages (+voice_fx mixer) / Forum Channels ───────────── → Note 6 (voice→SP08)
```

No source H2/H3 orphaned. All 3 pages fully covered; feature-page detail (voice/STT/TTS, session storage, cron,
config-block ownership, security, adapter authoring, remaining platforms) intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| index.md (4350w, 25 code, MIXED) | Note 1 (architecture/silence/session/toolset model) + Note 2 (ops procedure) | >2500w + BB mixing: the architecture/capability-matrix/silence-token/reset-policy material is a `model` BB; setup/commands/security/service-mgmt/multi-platform ops is a `procedure` BB → split by BB. |
| telegram.md (9147w, 56 code) | Note 3 (setup) + Note 4 (advanced/voice/topics) | >4000w; two arcs — first-bot setup (BotFather→config→webhook→proxy→home) vs advanced operation (media/voice/topics/groups/streaming/access-control). Each note curates from 56 source blocks to ≤6 load-bearing. |
| discord.md (6685w, 27 code) | Note 5 (setup) + Note 6 (advanced/voice/forum) | >4000w; setup (Developer-Portal→intents→token→invite→configure) vs advanced (session model/config reference/media/voice_fx/forum). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / owned slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_messaging_gateway` (owned) | `term_api_gateway` (active, 11604b), `term_mcp_gateway` (active), `term_agentcore_gateway` (active), `term_nat_gateway` (active) | **NOT a dup** — `api_gateway` is a network/HTTP API ingress, `mcp_gateway` is the MCP-server proxy, `agentcore_gateway`/`nat_gateway` are AWS-specific; none is the platform↔agent chat bridge (master caution: `messaging gateway ≠ term_api_gateway`) | CAPTURE owned; do NOT link `term_api_gateway` as a related/synonym term. |
| `term_dm_pairing` (owned) | none (ABSENT in DB) | NEW | CAPTURE owned. |
| `term_silence_token` (owned) | none (ABSENT in DB) | NEW | CAPTURE owned. |
| `hermes_messaging_gateway_architecture` | no `documentation/hermes_agent/` notes exist yet; `term_api_gateway`/`term_mcp_gateway` are component/contrast terms not dups | NEW doc | CREATE; LINK `term_mcp_gateway` (sibling gateway), `term_event_driven_architecture` as related. |
| `hermes_gateway_operations`, `hermes_telegram_setup`, `hermes_telegram_advanced`, `hermes_discord_setup`, `hermes_discord_advanced` | no substantive term/doc note covers these procedures | NEW doc | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug + each owned term slug;
**0 substantive same-concept duplicates** (the 4 `*_gateway` term hits are confirmed DIFFERENT concepts by name/scope;
`term_voice_wake` is the CLI wake-word, not the messaging voice flow). New `hermes_agent/` folder → no doc-doc collisions
(SP01 not yet executed; intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR standard 2026-06-19: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note, ALL counted)

> **FOUR-FLOOR standard, 2026-06-19 (user directive — supersedes the 2026-06-14 master floor AND the earlier
> 2026-06-19 three-floor wording).** Each note's `## Related Notes` now carries FOUR counted groups, all
> relevancy-selected and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; pick the modules that implement what THIS
>   doc note describes);
>   the Hermes implementation corpus; pick the code this note documents) — **promoted from BONUS to a COUNTED
>   floor and raised to ≥10**;
> - **≥10 DOCUMENTATION notes** (`../../documentation/`, relevancy-selected — sibling `hermes_*` in this series +
>   analogous `claude_code/cc_*` agent-tool docs + other relevant existing docs).
>
> The prior floors were ≥8 term + ≥8 snippet + ≥5 doc (2026-06-15) and then ≥8 term + ≥5 code-repo + ≥10 doc with
> snippets as a bonus (earlier 2026-06-19). **The snippet group (`snippet_hermes_agent_gw_*`, the `gw_` bucket) is
> NO LONGER a bonus — it is now a COUNTED floor at ≥10.** Relevancy first, never pad. **All term IDs, all repo IDs,
> un-verified. SP11a's own not-yet-existing owned terms (`term_messaging_gateway`, `term_dm_pairing`,
> `term_silence_token`) and other-SP forward-refs (`term_voice_mode`→SP08, `term_nous_portal`→SP14,
> `term_text_to_speech`/`term_speech_to_text`→SP08) are marked **[own]/+fin** and are EXCLUDED from the ≥8 term
> floor (they don't exist yet).

**Note 1 `hermes_messaging_gateway_architecture`** (model)
- Terms (9, ≥8 ✓): term_event_driven_architecture — the gateway is an event-driven adapter fan-in (each `<platform> --> store` edge in the architecture mermaid); term_message_queue — inbound messages buffer through the per-chat session store before dispatch; term_mcp_gateway — sibling-gateway contrast (MCP-server proxy vs platform↔agent chat bridge, per the collision audit); term_session_persistence — "Sessions persist across messages until they reset" + the reset-policy table (daily/idle/both); term_multi_agent_systems — one gateway fans 20+ platform adapters into one shared AIAgent; term_agent_orchestration — the gateway routes adapter → session store → `run_agent.py` AIAgent; term_cron — the architecture's "Cron scheduler ticks every 60s" node; term_stream_processing — progressive/streaming delivery is a capability-matrix column the model enumerates; term_conversational_ai — the gateway turns 20+ chat surfaces into one conversational agent. (+fin/[own]: term_messaging_gateway [own], term_silence_token [own])
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway runner + per-chat session store + adapter fan-in this model documents; [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the 20+ platform-adapter implementations behind the capability matrix; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `run_agent.py` AIAgent node the session store dispatches into; [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the 60s cron scheduler node in the architecture diagram; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the top-level package whose single background process is this gateway.
- Docs (16, ≥10 ✓): hermes_gateway_operations — the ops procedure that drives this model [sibling, +fin]; hermes_telegram_setup — a concrete adapter wired into the fan-in [sibling, +fin]; hermes_discord_setup — second concrete adapter [sibling, +fin]; hermes_session_search_storage — the per-chat session-key + FTS5 storage internals (SP02, link-out) [sibling, +fin]; hermes_messaging_media_settings — the `config.yaml` gateway knobs (reset policies, silence) (SP02) [sibling, +fin]; [cc_channels_overview](../claude_code/cc_channels_overview.md) — what-it-is: Claude Code's "agent reachable from chat surfaces" overview; relevance: the closest analogue to the gateway's "one process fans 20+ chat platforms into one agent" model. [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — what-it-is: per-session hosting/store model; relevance: mirrors the per-chat session store this model centers on. [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — what-it-is: the SDK session-store abstraction; relevance: analogous to the per-chat persistence layer adapters dispatch through. [cc_sessions](../claude_code/cc_sessions.md) — what-it-is: session lifecycle/persistence concepts; relevance: analogous to "sessions persist until they reset" + the reset-policy table. [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — what-it-is: scheduled-tick task model; relevance: analogue of the architecture's 60s cron-scheduler node. [cc_platforms_and_integrations](../claude_code/cc_platforms_and_integrations.md) — what-it-is: the catalog of surfaces Claude Code integrates with; relevance: analogous breadth to the gateway's 20+ platform capability matrix. [cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md) — what-it-is: the tool that emits a reply back to a chat channel; relevance: the inbound→agent→outbound edge this architecture diagrams. [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — what-it-is: reusable session-isolation patterns; relevance: analogous to the per-chat session-key partitioning of the store. [cc_sdk_sessions_overview](../claude_code/cc_sdk_sessions_overview.md) — what-it-is: SDK session-model overview; relevance: framing for the gateway's session-as-the-unit-of-state model. [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — what-it-is: how scheduled work is dispatched/executed; relevance: analogue of the cron tick fanning scheduled turns into the AIAgent. [cc_remote_control](../claude_code/cc_remote_control.md) — what-it-is: driving an agent from a remote surface; relevance: analogous "control the agent from a chat client" framing for the gateway model.

**Note 2 `hermes_gateway_operations`** (procedure)
- Terms (8, ≥8 ✓): term_access_control — allowlists + `GATEWAY_ALLOW_ALL_USERS` + the admin/regular-user tier split gating slash commands; term_authentication — the DM-pairing handshake authorizes unknown DMers; term_circuit_breaker — "Each adapter is wrapped in a circuit breaker … the adapter is auto-paused"; term_subagent — `/background <prompt>` "spawns a separate agent instance" with an isolated session; term_human_in_the_loop — the `/approve`/`/deny` exec-approval flow gates dangerous commands; term_session_persistence — session resume across gateway restarts (`restart_interrupted` auto-resume); term_failover — the breaker auto-pauses a failing adapter and notifies a live platform's home channel; term_rate_limiting — pairing codes are "rate-limited, … 1h expiry". (+fin/[own]: term_dm_pairing [own], term_messaging_gateway [own])
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway runner that owns the ACL gate, pairing, circuit breaker, `/platform`, and restart-resume; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes gateway setup/install/start/stop/status` and `hermes pairing` CLI commands this ops note drives; [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron scheduler whose 60s tick the gateway runs as part of day-2 ops; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent the `/background` subagent + interrupt/queue/steer logic wraps; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the systemd/launchd service install + the single-process lifecycle.
- Docs (16, ≥10 ✓): hermes_messaging_gateway_architecture — the model this ops note operates [sibling, +fin]; hermes_telegram_setup — platform-specific allowlist/security examples referenced here [sibling, +fin]; hermes_discord_setup — second platform's security/RBAC examples [sibling, +fin]; hermes_cli_session_background — the CLI-side `/background` + session controls (SP04) [sibling, +fin]; hermes_security_skill_memory_settings — the gateway security model link-out (SP03) [sibling, +fin]; [cc_channels_security_and_enterprise_controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — what-it-is: channel allowlist/admin-tier enterprise controls; relevance: analogous to the allowlist + `GATEWAY_ALLOW_ALL_USERS` + admin/user tier gate. [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — what-it-is: relaying a permission/approval decision through a channel; relevance: analogous to the `/approve`/`/deny` exec-approval relay this note drives. [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — what-it-is: hosting an isolated background session; relevance: analogous to `/background` isolated-session ops. [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — what-it-is: fire-and-forget background-agent dispatch; relevance: analogous to `/background <prompt>` spawning a separate agent instance. [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — what-it-is: admin-vs-user enforcement tiers; relevance: analogous to the admin/regular-user tier split + `/whoami`. [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — what-it-is: the rule-based permission system; relevance: analogous gating model for who can run which slash command. [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — what-it-is: programmatic tool-approval handling; relevance: analogous to the human-in-the-loop exec-approval before dangerous commands. [cc_remote_control](../claude_code/cc_remote_control.md) — what-it-is: interrupt/steer an agent from a remote surface; relevance: analogous to the interrupt/queue/steer busy-input controls. [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — what-it-is: scheduled-work execution model; relevance: analogous to the 60s cron tick the running gateway drives as day-2 ops. [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — what-it-is: auth + network failure handling; relevance: analogous to the circuit-breaker auto-pause + restart-resume failure path. [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — what-it-is: session resume/continue controls; relevance: analogous to `restart_interrupted` session auto-resume across gateway restarts.

**Note 3 `hermes_telegram_setup`** (procedure)
- Terms (9, ≥8 ✓): term_oauth_token — the BotFather-issued bot API token (`123456789:ABC…`); term_authentication — the token authenticates the bot + `TELEGRAM_ALLOWED_USERS` authorizes senders; term_access_control — numeric-user-ID allowlist gating who can reach the bot; term_reverse_proxy — webhook mode requires routing inbound HTTPS through a reverse proxy; term_webhook — the §Webhook Mode polling-vs-webhook deployment (`TELEGRAM_WEBHOOK_URL` + secret); term_dns — the DNS-over-HTTPS fallback-IP mechanism for `api.telegram.org`; term_tls — Telegram only delivers webhooks over HTTPS/TLS, and the fallback transport preserves SNI; term_idempotency — the one-shot `logOut` public-API migration step (run once, not per restart); term_chatbot — Telegram bot setup IS standing up a chatbot front-end for the agent. (+fin/[own]: term_messaging_gateway [own])
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Telegram adapter (python-telegram-bot client, polling/webhook, DoH fallback) this setup wires; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway runner + ACL gate the adapter registers into; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes gateway setup` interactive wizard that writes the Telegram config; [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron scheduler that delivers to the configured Telegram home channel/topic; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the top-level package + `.env`/`config.yaml` loading this setup edits.
- Docs (16, ≥10 ✓): hermes_messaging_gateway_architecture — the gateway model this adapter plugs into [sibling, +fin]; hermes_gateway_operations — the allowlist/security/service-mgmt ops that govern this bot [sibling, +fin]; hermes_telegram_advanced — the advanced/voice/topics continuation of this setup [sibling, +fin]; hermes_discord_setup — the parallel-platform setup procedure [sibling, +fin]; hermes_messaging_media_settings — the proxy/streaming `config.yaml` knobs referenced (SP02) [sibling, +fin]; [cc_channels_setup](../claude_code/cc_channels_setup.md) — what-it-is: step-by-step channel-bot setup; relevance: closest analogue to the BotFather→config→start Telegram setup arc. [cc_build_a_channel](../claude_code/cc_build_a_channel.md) — what-it-is: "build a chat channel" walkthrough; relevance: parallels standing up a new Telegram surface end-to-end. [cc_authentication](../claude_code/cc_authentication.md) — what-it-is: token/credential auth setup; relevance: analogous to the BotFather bot-token credential this setup configures. [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — what-it-is: TLS/network-access config; relevance: analogous to the HTTPS webhook + DNS-over-HTTPS fallback transport. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — what-it-is: proxy + gateway config; relevance: analogous to `TELEGRAM_PROXY`/`HTTPS_PROXY` proxy support. [cc_slack_setup_and_routing](../claude_code/cc_slack_setup_and_routing.md) — what-it-is: per-platform Slack channel setup + routing; relevance: analogous per-platform first-bot setup + message routing. [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — what-it-is: connecting the agent to a Slack workspace; relevance: analogous to connecting Hermes to a Telegram bot front-end. [cc_settings_files](../claude_code/cc_settings_files.md) — what-it-is: the settings/config-file layering; relevance: analogous to the `.env`/`config.yaml` files this setup edits. [cc_environment_variables](../claude_code/cc_environment_variables.md) — what-it-is: environment-variable configuration reference; relevance: analogous to the `TELEGRAM_*` env vars the manual path sets. [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — what-it-is: auth + network failure troubleshooting; relevance: analogous to the token/DoH-fallback troubleshooting section. [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — what-it-is: outbound network-access requirements; relevance: analogous to reaching `api.telegram.org` (incl. the fallback-IP mechanism).

**Note 4 `hermes_telegram_advanced`** (procedure)
- Terms (9, ≥8 ✓): term_session_persistence — DM/group forum topics each get an isolated persisted session (`agent:main:telegram:dm:{chat_id}:{thread_id}`); term_multimodal — voice memos (STT), `MEDIA:` attachments, and images are multimodal I/O; term_voice_wake — `mention_patterns` regex wake words trigger the bot in groups (CLI wake-word contrast noted); term_skill_manifest — topic `skill:` binding auto-loads a declared skill on new sessions; term_skills — group/DM forum-topic skill binding loads installed skills; term_access_control — group allowlisting (`group_allow_from`/`guest_mode`) + slash-command admin tiers; term_subagent — `/background <prompt>` inside a topic spawns a background agent; term_context_window — each topic "has its own conversation history … and context window"; term_regex — `mention_patterns` use Python regular expressions. (+fin: term_voice_mode, term_text_to_speech, term_speech_to_text)
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Telegram adapter's media/markdown/streaming/topic code these features exercise; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the per-topic session store + streaming-transport + slash-access runner; [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the skill loader behind topic skill binding (`skill: arxiv`); [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent the `/background` subagent + STT-injected turns run on; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the `clarify`/`send_message`/exec-approval tools surfaced as Telegram inline keyboards.
- Docs (16, ≥10 ✓): hermes_telegram_setup — the prerequisite first-bot setup [sibling, +fin]; hermes_messaging_gateway_architecture — the gateway/session model these features build on [sibling, +fin]; hermes_gateway_operations — interrupt/queue/steer + slash-tier ops shared with this note [sibling, +fin]; hermes_discord_advanced — the parallel-platform advanced features [sibling, +fin]; hermes_messaging_media_settings — the STT/TTS + streaming + `MEDIA:` config knobs (SP02/SP08) [sibling, +fin]; [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — what-it-is: voice→text input; relevance: analogous to Telegram voice-memo STT. [cc_sdk_slash_commands](../claude_code/cc_sdk_slash_commands.md) — what-it-is: slash-command access/registration; relevance: analogous to Telegram slash-command access tiers. [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — what-it-is: progressive/streaming output; relevance: analogous to the `gateway.streaming.transport` progressive-edit delivery. [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — what-it-is: skill invocation + auto-load lifecycle; relevance: analogous to topic `skill:` binding auto-loading a skill on a new session. [cc_sessions](../claude_code/cc_sessions.md) — what-it-is: parallel/isolated session concepts; relevance: analogous to `/topic` multi-session isolated DMs. [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — what-it-is: streaming text + tool-call events; relevance: analogous to the streaming-transport batching behind progressive Telegram edits. [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — what-it-is: rich/media tool content; relevance: analogous to `MEDIA:` attachment delivery + rich messages. [cc_skills_overview](../claude_code/cc_skills_overview.md) — what-it-is: the skills system overview; relevance: framing for group/DM forum-topic skill binding. [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — what-it-is: session-isolation patterns; relevance: analogous to the per-topic `agent:main:telegram:dm:{chat_id}:{thread_id}` session keying. [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — what-it-is: input modes + message editing; relevance: analogous to message-reaction/status-edit/per-channel-prompt interaction surface. [cc_sdk_clarifying_questions](../claude_code/cc_sdk_clarifying_questions.md) — what-it-is: agent-initiated clarifying-question flow; relevance: analogous to the Telegram `clarify` interactive prompt.

**Note 5 `hermes_discord_setup`** (procedure)
- Terms (9, ≥8 ✓): term_oauth_token — the Discord bot token from the Developer Portal; term_oauth — the OAuth2 invite-URL flow (`scope=bot+applications.commands`, permission integers); term_authentication — bot-token login + Privileged Gateway Intents to read message content; term_access_control — `DISCORD_ALLOWED_USERS`/`DISCORD_ALLOWED_ROLES` allowlist (default-deny); term_websocket — Discord runs over the persistent gateway WebSocket connection (not a stateless webhook); term_tls — the gateway WS + REST calls run over TLS; term_idempotency — `DISCORD_COMMAND_SYNC_POLICY=safe` diffs existing commands so startup sync is idempotent; term_chatbot — Discord setup stands up the agent's chatbot front-end; term_function_calling — the bot's slash commands + tool use are surfaced once intents are enabled (RBAC via `DISCORD_ALLOWED_ROLES` is folded into term_access_control above). (+fin/[own]: term_messaging_gateway [own])
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Discord adapter (discord.py gateway client, intents, slash-command sync) this setup wires; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway runner + ACL gate (`DISCORD_ALLOWED_USERS/ROLES`) the adapter registers into; [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes gateway setup` wizard that writes the Discord token + user ID; [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the skills auto-registered as native Discord application commands at startup; [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the top-level package + `.env`/`config.yaml` this setup edits.
- Docs (16, ≥10 ✓): hermes_messaging_gateway_architecture — the gateway model this adapter plugs into [sibling, +fin]; hermes_gateway_operations — the allowlist/security/service ops governing this bot [sibling, +fin]; hermes_discord_advanced — the advanced/session-model/voice continuation [sibling, +fin]; hermes_telegram_setup — the parallel-platform setup procedure [sibling, +fin]; hermes_messaging_media_settings — shared `config.yaml` gateway knobs (SP02) [sibling, +fin]; [cc_channels_setup](../claude_code/cc_channels_setup.md) — what-it-is: step-by-step channel-bot setup; relevance: closest analogue to the Developer-Portal→intents→token→invite→configure Discord arc. [cc_build_a_channel](../claude_code/cc_build_a_channel.md) — what-it-is: "build a chat channel" walkthrough; relevance: parallels standing up a Discord surface end-to-end. [cc_authentication](../claude_code/cc_authentication.md) — what-it-is: token/credential auth; relevance: analogous to the bot token + Privileged Gateway Intents login. [cc_channels_security_and_enterprise_controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — what-it-is: channel access controls; relevance: analogous to `DISCORD_ALLOWED_USERS`/`DISCORD_ALLOWED_ROLES` default-deny allowlist. [cc_sdk_slash_commands](../claude_code/cc_sdk_slash_commands.md) — what-it-is: slash-command registration; relevance: analogous to the startup native-Discord-app-command sync. [cc_slack_setup_and_routing](../claude_code/cc_slack_setup_and_routing.md) — what-it-is: per-platform setup + message routing; relevance: analogous per-platform first-bot setup + routing arc. [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — what-it-is: connecting the agent to a workspace; relevance: analogous to inviting/connecting the bot into a Discord server. [cc_settings_files](../claude_code/cc_settings_files.md) — what-it-is: settings/config-file layering; relevance: analogous to the `.env`/`config.yaml` this setup edits. [cc_environment_variables](../claude_code/cc_environment_variables.md) — what-it-is: env-var configuration reference; relevance: analogous to the `DISCORD_*` env vars the manual path sets. [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — what-it-is: rule-based permission system; relevance: analogous to role-based access (`DISCORD_ALLOWED_ROLES`) gating. [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — what-it-is: auth + network failure troubleshooting; relevance: analogous to the Privileged-Gateway-Intents footgun troubleshooting section.

**Note 6 `hermes_discord_advanced`** (procedure)
- Terms (9, ≥8 ✓): term_session_persistence — per-user-vs-shared session isolation (`group_sessions_per_user`) + history backfill recovering session transcript gaps; term_multimodal — `send_message`/`MEDIA:` media send + arbitrary-file receive (images/audio/video/docs); term_access_control — slash-command admin tiers + mention control + allowed-roles; term_skills — native skill slash-command registration in Discord; term_skill_manifest — installed skills declare themselves as Discord application commands; term_multi_agent_systems — shared-room concurrency / one running-agent slot per channel when `group_sessions_per_user: false`; term_context_window — per-channel context growth + backfill bounded by `history_backfill_limit`; term_persona — per-channel ephemeral system prompts (`channel_prompts`) set a per-room persona; term_voice_call — the `voice_fx` mixer for Discord voice-channel conversations. (+fin: term_voice_mode, term_text_to_speech, term_speech_to_text)
- Code-Repos (5, ≥5 ✓): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Discord adapter's thread/attachment/slash/voice_fx code these features exercise; [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the per-user session store + concurrency slot + display/tool-progress config; [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the skill registry behind native Discord slash-command registration; [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent + interrupt/concurrency semantics per session key; [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the `send_message`/`clarify` tools + media send/receive surface.
- Docs (16, ≥10 ✓): hermes_discord_setup — the prerequisite first-bot setup [sibling, +fin]; hermes_messaging_gateway_architecture — the gateway/session model these features build on [sibling, +fin]; hermes_gateway_operations — shared interrupt/slash-tier/session-resume ops [sibling, +fin]; hermes_telegram_advanced — the parallel-platform advanced features [sibling, +fin]; hermes_messaging_media_settings — the media/voice_fx/backfill config knobs (SP02/SP08) [sibling, +fin]; [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — what-it-is: voice→text input; relevance: analogous to Discord STT + voice-channel conversations. [cc_sdk_slash_commands](../claude_code/cc_sdk_slash_commands.md) — what-it-is: slash-command registration/access; relevance: analogous to Discord slash-command access tiers + native command registration. [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — what-it-is: skill-as-command lifecycle; relevance: analogous to native skill slash-command registration in Discord. [cc_sessions](../claude_code/cc_sessions.md) — what-it-is: per-session isolation concepts; relevance: analogous to `group_sessions_per_user` per-user-vs-shared isolation. [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — what-it-is: rich/media tool content; relevance: analogous to `send_message` + `MEDIA:` media send and arbitrary-file receive. [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — what-it-is: session-isolation patterns; relevance: analogous to per-channel/per-user session keying + concurrency slots. [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — what-it-is: running agents concurrently; relevance: analogous to shared-room concurrency / one running-agent slot per channel. [cc_skills_overview](../claude_code/cc_skills_overview.md) — what-it-is: the skills system overview; relevance: framing for installed-skill-as-Discord-application-command registration. [cc_sdk_clarifying_questions](../claude_code/cc_sdk_clarifying_questions.md) — what-it-is: agent-initiated clarifying-question flow; relevance: analogous to the Discord `clarify` interactive prompt. [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — what-it-is: input modes + per-surface editing; relevance: analogous to per-channel ephemeral prompts (`channel_prompts`) + mention control. [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — what-it-is: the catalog of built-in agent tools; relevance: analogous to the `send_message`/`clarify` tool surface exposed in Discord.

All 6 notes meet **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (FOUR-FLOOR standard, all counted). Term IDs
are under `resources/term_dictionary/`, repo IDs under `areas/code_repos/`, and snippet IDs under
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8). Per-note snippet
counts: 11/11/11/11/11/11. **Per-note doc counts (Docs-floor fix 2026-06-19): 16/16/16/16/16/16** — each is 5 sibling
added link carrying a specific `relevance:` clause. The earlier "Docs (10)" lines (5 sibling + 5 `cc_*`) were short of a
robust ≥10 rendered-markdown-link floor (siblings render as plain text, not links); each Docs line was expanded with 6
update 2026-06-19:** `term_webhook` is now ACTIVE in the DB (it was absent at the 2026-06-15 finalization) and is used
in Note 3; `term_text_to_speech`/`term_speech_to_text`/`term_voice_mode` remain ABSENT (SP08 forward-refs, +fin,
was checked and is MISSING → NOT used).

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 3 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (index 4350/25, telegram 9147/56, discord 6685/27; no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 messaging-gateway-architecture | model | 1500 | ≤6 (curate: mermaid arch block + reset-policy/silence-token blocks; tables in prose) | ✓ |
| 2 gateway-operations | procedure | 2400 | ≤6 (curate from gateway/pairing/admin/service blocks) | ✓ |
| 3 telegram-setup | procedure | 2200 | ≤6 (curate from BotFather/config/webhook/proxy blocks) | ✓ |
| 4 telegram-advanced | procedure | 2400 | ≤6 (curate from 56 source blocks: one canonical YAML per feature cluster) | ✓ |
| 5 discord-setup | procedure | 2000 | ≤6 (curate from intents/token/invite/.env blocks) | ✓ |
| 6 discord-advanced | procedure | 2300 | ≤6 (curate from 27 source blocks: config.yaml + voice_fx + media) | ✓ |

No further splits needed — all 6 notes are ≤2500w. Notes 2/4/6 (at ~2300-2400w) were checked for further split:
each is one topically-cohesive cluster (gateway ops / telegram-advanced / discord-advanced) with no BB mixing
→ KEEP (per review CP6 default-to-keep justification). The 56 telegram + 27 discord source code blocks are curated
to ≤6 load-bearing YAML/bash examples per note, with the rest summarized in prose (kept blocks verbatim). If any note
exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (all counted —
FOUR-FLOOR standard set 2026-06-19; supersedes both the 2026-06-15 ≥8 term + ≥8 snippet + ≥5 doc and the earlier
2026-06-19 three-floor wording) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP11a)

**SP11a owns 3 new term captures** (the cross-cutting gateway concepts). Each is captured via
`/tessellum-capture-term-note <term>` (NOT inline) BEFORE writing the digest notes that reference it. The
three-way existence check (filename + bm25 + dense) was re-run at augmentation: all 3 are ABSENT (no stub,
no substantive note). Specificity + collision audit performed per owned slug (below).

| Term slug | Concept | DF | Capture Phase | Stub/Full | Depth tier (Related min) | Best-fit glossary | Source page |
|---|---|---:|---|---|---|---|---|
| `term_messaging_gateway` | platform↔agent bridge: one background process fanning 20+ platform adapters through a per-chat session store into the AIAgent + cron tick (≠ `term_api_gateway`) | 30+ | Phase 0 (before Note 1) | Full | Moderate (10) | acronym_glossary_systems | index.md |
| `term_dm_pairing` | gateway user-authorization handshake: unknown DMers get a one-time pairing code, operator approves via `hermes pairing approve` (rate-limited, crypto-random, 1h expiry) | 8 | Phase 0 (before Note 2) | Full | Simple (8) | acronym_glossary_systems | index.md |
| `term_silence_token` | `[SILENT]`/`SILENT`/`NO_REPLY`/`NO REPLY` intentional non-reply: if the agent's whole final response is the token, the gateway suppresses outbound delivery but keeps the turn in transcript | 6 | Phase 0 (before Note 1) | Full | Simple (8) | acronym_glossary_workflows | index.md |

### Renamed (general → specific)

| Owned slug | Specificity check | Verdict |
|---|---|---|
| `term_messaging_gateway` | Two-word domain-qualified noun phrase; "messaging" disambiguates from the generic `gateway`/`api_gateway`/`nat_gateway`/`mcp_gateway` family already in the vault | KEEP — already specific + collision-disambiguated; do not rename. |
| `term_dm_pairing` | "dm" (direct-message) scope qualifier + "pairing" (the handshake) → specific to the gateway authorization flow, not the generic Bluetooth/device "pairing" | KEEP — scope-qualified. |
| `term_silence_token` | Compound naming the concrete `[SILENT]` sentinel mechanism; not a bare common-English noun | KEEP — specific. |

(No renames required — all 3 owned slugs passed the specificity heuristic at capture.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_gateway` / `term_chat_gateway` | `term_api_gateway.md` (active), `term_mcp_gateway.md` (active), `term_agentcore_gateway.md` (active), `term_nat_gateway.md` (active) | Not captured under a generic name — all 4 existing `*_gateway` notes are DIFFERENT concepts; SP11a captures the specific `term_messaging_gateway` and links `term_mcp_gateway` as a sibling-gateway contrast only. |
| `term_voice_message` / `term_voice_transcription` | `term_voice_wake.md` (active = CLI wake-word, different) | Not captured — voice STT/TTS concepts are owned by SP08 (`term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`); SP11a link-outs only. |
| `term_circuit_breaker` (adapter) | `term_circuit_breaker.md` (active) | Not captured — the existing generic term covers it; link from Note 2. |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Every term in the Undigested Terms Plan above MUST be authored via **`/tessellum-capture-term-note <term>`**
(interactive or via ENRICHER_INPUTS), NOT inline-authored within a digest note. The capture skill enforces the
requirements below; this plan invokes them.

### YAML Frontmatter (Required Fields)

```yaml
---
tags:
  - resource
  - terminology
  - <domain_tag_1>          # e.g., systems, messaging, agents
  - <domain_tag_2>
keywords:
  - <ACRONYM or short form>
  - <Full Name>
  - <variant_spellings>
topics:
  - <topic_1>
  - <topic_2>
language: markdown
date of note: 2026-06-15
status: active
building_block: concept       # MUST be concept for term notes
access_control_group: ["general"]
related_wiki: <primary_url_or_null>
---
```

### Required H1 + H2 Sections (in order)

`# <Name>` → `## Definition` (what it is, what problem it solves, who uses it) → `## Context` (which Hermes
systems/workflows use it) → `## Key Characteristics` (distinctive properties) → `## Performance / Metrics`
(optional, only if found) → `## Related Terms` (**depth-scaled minimum: 8 for simple, 10 for moderate** —
INDEXED markdown links `**[Term Name](term_X.md)** — one-line description`; ≥3 in-domain + ≥3 cross-domain) →
`## References` (EXTERNAL URLs ONLY — Hermes docs page, GitHub, no `term_*.md` links here).


The Hermes docs page is ONE viewpoint. Each capture MUST research across multiple sources (the capture skill
docs, the open-source `NousResearch/hermes-agent` repo, Wikipedia/standards for the generic concept — e.g.
"message gateway"/"chatbot gateway" patterns for `term_messaging_gateway`); (6) Vault cross-reference via
`/tessellum-search-notes` + DB query for in-domain + cross-domain related terms. Single-source (docs-only) capture → FAIL.

### Cross-Domain Diversity for Related Terms (8-10 links, ≥3 in-domain + ≥3 cross-domain)

- `term_messaging_gateway`: in-domain → `term_mcp_gateway`, `term_event_driven_architecture`, `term_message_queue`, `term_session_persistence`; cross-domain (contrast/foundation) → `term_api_gateway` (contrast: HTTP ingress vs chat bridge), `term_reverse_proxy`, `term_webhook`(if exists)→`term_websocket`, `term_circuit_breaker`.
- `term_dm_pairing`: in-domain → `term_messaging_gateway`, `term_access_control`, `term_authentication`; cross-domain → `term_oauth_token`, `term_rate_limiting`, `term_human_in_the_loop`.
- `term_silence_token`: in-domain → `term_messaging_gateway`, `term_session_persistence`; cross-domain → `term_state_machine`(if exists), `term_idempotency`, `term_event_driven_architecture`.

(Augmentation DB-verifies each Related Term at capture; substitute a verified sibling for any MISSING slug — same
catch applied to the digest-note mappings above.)

### Other capture requirements (inherited verbatim — apply at capture)

Math notation in MathJax (n/a for these systems terms unless a formula appears); Fleeting Content Guard (strip
aliases/ETAs/headcounts); Glossary entry = exact `**Full Name** / **Description** (4-5 sentences max, bold the
single most distinguishing fact, no metrics) / **Documentation** / **Wiki** / **Related**` template; Pre-Flight
Outcome Routing (all 3 ABSENT → create full); File Naming canonical (`term_messaging_gateway.md` etc.); Backlink
Expansion (Step 6: 1-2 non-term backlinks via `grep -rl` + 5-10 inlinks from existing term notes — e.g. add the
new terms to `term_api_gateway`/`term_mcp_gateway`/`term_session_persistence`/`term_access_control` Related Terms);
Section ordering (Related Terms before References, footer last); >200-line → Step-7 decomposition; Research
Dry-Fall Fallback (if all sources empty → ask user for URL OR `status: stub` + `research_pending: true`, never
silently emit docs-only). Acceptance: single-source / <depth-min Related / no cross-domain / no inlink expansion /
`References` containing `.md` links / forbidden YAML field / `building_block` ≠ concept → FAIL.

### ENRICHER_INPUTS Non-Interactive Pattern (for Phase-0 batch capture)

```yaml
ENRICHER_INPUTS:
  key_terms: ["Messaging Gateway"]          # / "DM Pairing" / "Silence Token"
  acronym: ""
  domain: "Hermes Agent messaging gateway platform adapters session store"
  summary_snippets:
    - "<first definition from index.md — verbatim>"
    - "<key characteristic from index.md — verbatim>"
  references:
    - https://hermes-agent.nousresearch.com/docs/user-guide/messaging
SOURCE CONTENT:
<relevant index.md excerpt(s) — verbatim>
```

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (owned term captures):** capture `term_messaging_gateway`, `term_silence_token`, `term_dm_pairing`
  them. Reindex. These resolve the [own] markers in the mappings. GATE: term-note acceptance criteria + G5 (the
  three new terms exist).
- **Phase 1 (gateway concepts, P-hub pilot):** Notes 1, 2. Pilot Note 1 (`hermes_messaging_gateway_architecture`)
  first → reindex → verify format/ghost/in-degree BEFORE Note 2. GATE G1–G8.
- **Phase 2 (Telegram):** Notes 3, 4. GATE G1–G8.
- **Phase 3 (Discord):** Notes 5, 6. GATE G1–G8.
- **Phase 3b (inlinks):** add the inlink table below; verify every new note in-degree ≥1 from outside the folder.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for kept
blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every ref)** ·
**G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB · **G8 in-degree ≥1
from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# Owned-term existence (Phase 0 gate)
for t in term_messaging_gateway term_dm_pairing term_silence_token; do
# G8: in-degree ≥1 from outside the folder
for n in hermes_messaging_gateway_architecture hermes_gateway_operations hermes_telegram_setup hermes_telegram_advanced hermes_discord_setup hermes_discord_advanced; do
```

## Entry Point Decision (inherited)

Contributes 6 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note
series) under a "Messaging: Gateway, Telegram & Discord" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP11a does NOT create a separate entry point — the
>30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_messaging_gateway_architecture`, `hermes_gateway_operations`, `hermes_telegram_setup`, `hermes_discord_setup` | gateway/messaging repo ↔ gateway usage + per-platform docs |
| `repo_hermes_agent.md` | → `hermes_messaging_gateway_architecture` | top-level implementation ↔ gateway architecture doc |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_telegram_setup`, `hermes_discord_setup` | platform/provider adapters ↔ adapter setup docs |
| `repo_hermes_agent_cron.md` | → `hermes_gateway_operations` | cron scheduler (60s tick) ↔ gateway ops |
| `term_messaging_gateway.md` (new, Phase 0) | → `hermes_messaging_gateway_architecture`, `hermes_gateway_operations` | concept term → user-facing gateway docs |
| `term_dm_pairing.md` (new, Phase 0) | → `hermes_gateway_operations` | concept term → the ops doc that documents the pairing flow |
| `term_silence_token.md` (new, Phase 0) | → `hermes_messaging_gateway_architecture` | concept term → the architecture doc that documents the token |
| `term_mcp_gateway.md` | → `hermes_messaging_gateway_architecture` | sibling-gateway term → gateway architecture doc (contrast) |
| `term_access_control.md` | → `hermes_gateway_operations` | concept term → allowlist/admin-tier ops doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_messaging_gateway_architecture`, `hermes_telegram_setup`, `hermes_discord_setup` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 6 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Phase 0 captures the 3 owned terms FIRST (reindex). Pilot Note 1 (`hermes_messaging_gateway_architecture`) →
reindex → verify format/ghost/in-degree BEFORE authoring the rest. Commit per phase (per-wave commits for
multi-agent runs). Re-read the source page before writing each note — do NOT work from memory. Code blocks
verbatim for kept blocks; curate code-heavy notes (telegram 56, discord 27 source blocks) to ≤6 load-bearing
examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If multi-agent:
agents return note content, master writes serially where there is write-contention; ≤30 agents/run; embed the
manifest in the workflow script.

## Follow-up Recommendations

- After SP11a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 6 rows to the
  master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- Cross-link from SP11b/SP12/SP13 messaging notes back to `hermes_messaging_gateway_architecture` +
  `hermes_gateway_operations` once those SPs land (the per-platform pages all assume the gateway concept).
- When SP08 captures `term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`, backfill the +fin voice
  forward-refs in Notes 4 and 6.

## Augmentation Report

- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  earlier 2026-06-19 three-floor wording (≥8 term / ≥5 code-repo / ≥10 doc with snippets as bonus). The snippet group
  (`snippet_hermes_agent_gw_*`) was **promoted from bonus to a counted floor and raised to ≥10** (per-note 11 each).
  active `snippet_hermes_agent_gw_*` notes selected by the page's code paths, and a Docs (≥10) line mixing sibling
  `term_webhook` re-checked and is now ACTIVE → used in Note 3.
- **Docs-floor fix 2026-06-19:** an independent audit found the Docs lines were short of a robust ≥10 floor (each was
  5 sibling `hermes_*` rendered as plain text + only 5 `cc_*` rendered-markdown links). Every note's Docs line was
  doc-link count alone is ≥10 per note; each added `cc_*` link carries a specific `relevance:` clause tied to the note's
  content. +66 doc links added total (6 notes × 11 `cc_*` now vs 5 before = +6 each, +36 added; +30 sibling/`cc_*`
  is MISSING → excluded. Terms/Code-Repos/Snippets lines untouched (they already pass the floor). No existing doc link
  dropped.
- Sections added/updated: Collision&Dedup Audit (4 `*_gateway` LIKE hits confirmed DIFFERENT concepts by reading
  names/scope; `term_voice_wake` confirmed ≠ messaging voice), finalized Per-Note Mapping (≥8 term + ≥5 code-repo
  silence_token, all ABSENT → full capture), Term-Note Authoring Requirements, Doc-Note Authoring Spec (derived
  from `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost + owned-term + G8 scripts, Inlinks.
- Density re-read: counts match measured (index 4350/25, telegram 9147/56, discord 6685/27); **no additional
  splits** beyond the planned (index→2, telegram→2, discord→2). All 6 notes ≤2500w; code-heavy notes curated ≤6.
- Collision audit: **0 removals** of planned doc notes; 4 `*_gateway` term hits + `term_voice_wake` confirmed
  LINK-not-dup; 3 owned terms confirmed ABSENT (safe to capture).
- Term DB-verify catch: **4 non-existent term slugs caught at finalization** (`term_webhook`, `term_text_to_speech`,
  `term_reverse_proxy`; TTS/STT moved to +fin SP08 forward-refs (excluded from floor).
- Undigested terms surfaced at augment: **3 owned** (cross-cutting gateway concepts).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (≥8 term/≥5
Inlinks (all 6) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan (3 owned) ✓
Capture Phase per term (Phase 0) ✓ best-fit glossary (systems/systems/workflows — all exist) ✓ Term-Note Auth
Reqs (full) ✓ invokes capture-term-note ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (3
owned audited, 0 renames) ✓ Slug Collision (4 `*_gateway` + `voice_wake` LIKE false-positives + 4 non-existent
cited terms caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8
in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 phases + Phase 3b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (6 rows under a Messaging section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 6 notes ≤30; master holds the corpus-level split (SP11 split a/b). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | index→2 (model+procedure BB split), telegram→2, discord→2; all notes ≤2500w; code-heavy notes curated ≤6; dense notes (2/4/6) checked → cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15; re-measured 2026-06-19 (mirror c253b07): index 4350/25, telegram 9147/56, discord 6685/27 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP11a owns 3 term captures (`term_messaging_gateway`, `term_dm_pairing`, `term_silence_token`), all ABSENT → Phase-0 full capture; Undigested Terms Plan + full Authoring Reqs (multi-source must-language) present. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 6 doc notes + 3 owned terms (term_dictionary AND documentation/); 4 `*_gateway` + `voice_wake` LIKE false-positives confirmed (DIFFERENT concepts = LINK not dup); 4 non-existent cited term slugs caught + replaced/moved-to-+fin; Renamed (0)/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 6 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b. |

**RESULT: 9/9 → READY FOR EXECUTION.**

### Independent Re-Review 2026-06-19 (FOUR-FLOOR standard — ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note)

Re-ran the canonical 9-checkpoint review against the FOUR-FLOOR cross-ref standard. CP1 re-counted per note
(parsed mapping): all 6 notes = 9 or 8 term / 5 code-repo / 11 snippet / 16 doc (Docs-floor fix 2026-06-19: 5
met, 0 bare links (every link carries a `— what-it-is; relevance: …` clause). Anti-fabrication DB spot-check (2026-06-19): all 34
cited terms, all 8 cited `repo_hermes_agent_*`, all 41 cited `snippet_hermes_agent_gw_*`, and all 19 cited
`term_dm_pairing`, `term_silence_token`) confirmed ABSENT (correctly [own]/excluded); SP08 forward-refs
(`term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`) confirmed ABSENT (+fin, excluded); the 4 collision
`*_gateway` terms confirmed active+DIFFERENT. `resources/documentation/hermes_agent/` is empty in the DB → sibling
`hermes_*` doc links resolve at finalization (G5/G8). CP7 source re-measure (mirror at inbox): index 4350w/25code
(==plan), discord 6685w/27code (==plan), telegram 9148w/56code (plan 9147/56, ±1 word same count-class).

| CP | Result | Evidence |
|----|--------|----------|
| CP2 | PASS | Phase 0 + Phases 1–3 + Phase 3b each run G1–G8 incl G5 ghost (Script 4, DB-verify every ref), G6 broken-link, G8 in-degree. |
| CP3 | PASS | Shares master-created `entry_hermes_agent_docs.md` (6 rows, Messaging section); matches >30-note threshold. |
| CP4 | PASS | 6 notes ≤30; corpus split held at master (SP11 a/b). |
| CP5 | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (FOUR-FLOOR minimum embedded); not invented. |
| CP6 | PASS | index→2 (model+procedure BB split), telegram→2, discord→2; all ≤2500w/≤6 code; dense notes 2/4/6 cohesive single-BB → KEEP. |
| CP7 | PASS | Re-measured at inbox: index 4350/25 ==plan, discord 6685/27 ==plan, telegram 9148/56 (±1w of plan 9147/56). |
| CP8 | PASS | 3 owned terms (all ABSENT → Phase-0 full capture); Undigested Terms Plan + full multi-source Authoring Reqs present. |
| CP8f | PASS | Collision/dedup audit over term_dictionary AND documentation/; 4 `*_gateway`+`voice_wake` confirmed DIFFERENT (link-not-dup); 0 same-concept dups; Renamed(0)/Removed sub-tables present. |
| CP9 | PASS | Inlinks table covers all 6 notes from repo_*/term_*/entry_* outside the folder; gated Phase 3b. |

**RE-REVIEW RESULT: 9/9 → READY FOR EXECUTION (FOUR-FLOOR standard verified).**

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from `NousResearch/hermes-agent` `website/docs/` at main HEAD `c253b07` (was pinned `95715dc`),
byte-identical to upstream main. Both owned SP11a pages were independently re-measured (BODY words after stripping
YAML frontmatter; code-fence lines ÷2) and the COUNTS-class deltas confirmed:

- user-guide/messaging/index.md — 4158w/24code -> 4350w/25code
- user-guide/messaging/telegram.md — 8932w/55code -> 9147w/56code
- user-guide/messaging/discord.md — 6685w/27code -> 6685w/27code (UNCHANGED; spot-re-measured stable, as were
  sibling unchanged pages slack.md 3626/23 and matrix.md 5393/45 — measurement convention reproduces the ledger).

My fresh measurements match the manifest's NEW numbers exactly (no discrepancy). Counts updated everywhere they
appear for the two changed pages: Source Pages table, Section Coverage Map fence headers, Split Decisions rationale,
Density Re-Assessment cited counts (incl. the 55→56 telegram block curation reference), Content Strategy line,
Pacing Rules block-count, Augmentation Report, and CP7.

**Density re-decision:** NONE. The deltas are small (index +192w/+1code, telegram +215w/+1code) and are absorbed by
each note's link-out + code-curation budget; every planned note remains ≤2500w / ≤6 code / ≤400 lines. index.md still
splits 2 (model+procedure BB), telegram.md still splits 2 (setup + advanced) — no cap breach, **no new split** added.
No planned-note filename, BB type, source-section routing, or gate changed.

**Cross-ref floor (re-measure pass, 2026-06-19):** at re-measure time the floor was ≥8 term + ≥8 snippet + ≥5 doc;
it was subsequently **set 2026-06-19 to the FOUR-FLOOR standard** — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per
note, all counted (snippets promoted from bonus to a counted floor and raised to ≥10) — see the Per-Note Related Notes
Mapping and Augmentation Report. Plan remains **READY** for execution (9/9 review checkpoints still hold; the changes
are re-measured counts + provenance + the four-floor cross-ref standard).

## Pipeline Status (Per-Sub-Plan)


**Source**: `inbox/hermes_agent_docs/user-guide/messaging/{index,telegram,discord}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
