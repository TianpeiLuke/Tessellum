---
title: Hermes Agent Docs Digestion — Sub-Plan 11b — Messaging: Slack, Matrix, Mattermost, Teams, Google Chat
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
pages:
  - user-guide/messaging/slack.md
  - user-guide/messaging/matrix.md
  - user-guide/messaging/mattermost.md
  - user-guide/messaging/teams.md
  - user-guide/messaging/teams-meetings.md
  - user-guide/messaging/google_chat.md
---

# Sub-Plan 11b: Messaging — Slack, Matrix, Mattermost, Teams, Google Chat

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP11b's note
> filenames/BBs/coverage are defined. **Part b of the SP11 split** — SP11a owns the gateway concepts
> (index + telegram + discord) and the gateway concept-term captures (`term_messaging_gateway`,
> `term_dm_pairing`, `term_silence_token`); SP11b owns the remaining team-chat platform-setup procedures.

## Scope

The "team chat" platform-setup procedures for the Hermes messaging gateway: connecting Hermes as a bot to
**Slack** (Socket Mode), **Matrix** (federated, with E2EE + macOS proxy mode), **Mattermost** (self-hosted),
**Microsoft Teams** (webhook bot + the Graph meeting-summary pipeline), and **Google Chat** (Cloud Pub/Sub).
Source = 6 mirrored pages in `inbox/hermes_agent_docs/user-guide/messaging/` (all substantive). **P2 / features.**
These are all platform-setup procedures that share the gateway architecture, session model, allowlist gating,
and `~/.hermes/config.yaml` `platforms.<name>` surface — so they reuse the same gateway snippet pool
(`snippet_hermes_agent_gw_*`) and the gateway concept terms owned by SP11a (linked as forward-refs).

## Content Strategy

- **One BB per note.** All six pages are procedure-dominant (setup → token → config → run → troubleshoot).
  `slack.md` mixes the step-by-step app-creation procedure with a large config-options reference → split into
  2 (setup procedure / config reference). `matrix.md` (5393w, 45 code) mixes base setup, an E2EE subsystem,
  and a separate macOS proxy-mode deployment architecture → split into 3 (>4000w → 3+ per the density rule).
  mattermost/teams/teams-meetings/google_chat → 1 note each.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the gateway
  index/concepts + telegram/discord (SP11a), consumer/webhook platforms (SP12), Chinese platforms (SP13),
  the `msgraph-webhook` listener reference page (SP12), the config.yaml `platforms.*` reference cluster (SP02
  `hermes_messaging_media_settings`), voice/TTS/STT (SP08), MCP/ACP (SP09), the Graph app-registration guide
  (SP17), and the Teams-meeting-pipeline day-2 operator guide (SP16).
- **Collision (augment): `term_slack.md` (65L, active) is the GENERIC Slack messaging-platform concept** —
  NOT the Hermes Slack adapter procedure. The planned `hermes_messaging_slack` is the Hermes setup procedure,
  a different BB → LINK `term_slack`, do not recreate.
  is an access-control concept — a classic LIKE false-positive, NOT Microsoft Teams. Do NOT link it from the
  MISSING 2026-06-19 — so there is no `term_teams` note to link or mis-link either.)
- **Collision: no `term_matrix` exists** (`term_adjacency_matrix`/`term_precision_matrix` etc. are
  linear-algebra terms — unrelated). The planned Matrix notes capture the Matrix-protocol setup procedure;
  no term collision.
- **Owned NEW term captures: 0.** Every gateway concept these pages touch is owned by SP11a
  (`term_messaging_gateway`, `term_dm_pairing`, `term_silence_token`) — LINK as forward-refs (+fin). No
  platform here introduces a genuinely-new reusable concept after a collision audit (Socket Mode = existing
  `term_socket_mode`; E2EE/proxy/Pub-Sub/service-account are platform-specific setup details, not vault-wide
  reusable concepts beyond the already-active `term_encryption`/`term_websocket`/`term_pub_sub`).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/messaging/matrix.md | 5393 | 45 | procedure (base + E2EE + proxy) | 3 (split) |
| user-guide/messaging/slack.md | 3626 | 23 | procedure (setup + config) | 2 (split) |
| user-guide/messaging/google_chat.md | 2107 | 6 | procedure | 1 |
| user-guide/messaging/mattermost.md | 1982 | 14 | procedure | 1 |
| user-guide/messaging/teams.md | 1343 | 14 | procedure | 1 |
| user-guide/messaging/teams-meetings.md | 935 | 12 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_messaging_slack.md` | procedure | slack §Overview, §Step 1 Create App (manifest/manual), §Step 2 Bot Token Scopes, §Step 3 Socket Mode, §Step 4 Subscribe to Events, §Step 5 Messages Tab, §Step 6 Install, §Step 7 Find User IDs, §Step 8 Configure Hermes, §Step 9 Invite Bot, §Slash Commands (`!cmd` prefix), §How the Bot Responds, §Troubleshooting (+Quick Checklist), §Security | ~1700 | Connect Hermes as a Slack bot over Socket Mode: generate/paste the manifest, the 11 bot-token scopes, App-Level + Bot tokens, the four required event subscriptions, the Messages Tab gate, install/invite, the `!cmd` thread workaround, mention behavior, and the channel-not-working checklist. |
| 2 | `hermes_messaging_slack_config.md` | procedure | slack §Configuration Options (Thread & Reply Behavior, Session Isolation, Mention & Trigger, `allowed_channels`, Unauthorized User Handling, Voice Transcription, Full Example), §Home Channel, §Multi-Workspace Support (+OAuth Token File), §Voice Messages, §Per-Channel Prompts, §Per-Channel Skill Bindings | ~1500 | Slack `config.yaml` reference: reply/threading modes, per-user session isolation, mention/strict-mention/free-response gating, channel allowlist, unauthorized-DM behavior, multi-workspace token lists + `slack_tokens.json`, home channel, voice in/out, per-channel prompts, and per-channel skill bindings. |
| 3 | `hermes_messaging_matrix.md` | procedure | matrix §intro, §How Hermes Behaves, §Capability Matrix (+Session Model, Mention/Threading config, Project Room Isolation), §Step 1 Bot Account, §Step 2 Access Token, §Step 3 Find User ID, §Step 4 Configure, §Private Deployment Hardening, §Home Room, §Room allowlist, §Commands in Matrix, §Matrix Tools and Controls, §Media Limits, §Troubleshooting, §Security, §Notes | ~2000 | Base Matrix bot setup (any homeserver via `mautrix`): account + access-token/password auth, allowed-users/rooms hardening, session-scope + auto-threading, the six Matrix-scoped tools + reaction approvals, media limits, the clock-skew/auth troubleshooting, and federation/bridge-ghost handling. |
| 4 | `hermes_messaging_matrix_e2ee.md` | procedure | matrix §End-to-End Encryption (Requirements, Enable E2EE, modes, key storage), §Synapse Integration Tests, §Cross-Signing Verification, §Deleting the crypto store recovery, §Upgrading from a previous version with E2EE | ~1300 | Matrix end-to-end encryption: `mautrix[encryption]` + `libolm`, the off/optional/required modes, device-key upload, cross-signing via `MATRIX_RECOVERY_KEY`, the stale-one-time-key failure mode, and the new-access-token migration to the SQLite crypto store. |
| 5 | `hermes_messaging_matrix_proxy_mode.md` | model | matrix §Proxy Mode (E2EE on macOS) (How It Works diagram, Step 1 Configure Host, Step 2 Configure Container, Step 3 Start Both, Configuration Reference, Works for Any Platform, v1 limitations, sync troubleshooting) | ~1100 | The macOS E2EE proxy-mode deployment model: a thin Linux Docker container runs only the Matrix adapter + E2EE and HTTP-forwards decrypted text to the host's `api_server` running the real agent; host/container env split, session continuity via `X-Hermes-Session-Id`, and the platform-agnostic generalization. |
| 6 | `hermes_messaging_mattermost.md` | procedure | mattermost §intro, §How Hermes Behaves (+Session Model), §Step 1 Enable Bot Accounts, §Step 2 Create Bot, §Step 3 Add to Channels, §Step 4 Find User ID, §Step 5 Configure, §Home Channel, §Reply Mode, §Mention Behavior, §`allowed_channels`, §Troubleshooting, §Per-Channel Prompts, §Security, §Notes | ~1300 | Connect Hermes to self-hosted Mattermost over REST v4 + WebSocket: enable + create the bot account, add to channels, the 26-char user ID, reply-mode thread/off, require-mention + free-response, channel allowlist, the nginx WebSocket-upgrade fix, and per-channel prompts. |
| 7 | `hermes_messaging_teams_bot.md` | procedure | teams §intro, §How the Bot Responds, §Step 1 Teams CLI, §Step 2 Expose Webhook Port, §Step 3 Create the Bot, §Step 4 Env Vars, §Step 5 Start Gateway, §Step 6 Install in Teams, §Configuration Reference, §Features (Interactive Approval Cards, Meeting Summary Delivery), §Production Deployment, §Troubleshooting, §Security | ~1000 | Connect Hermes as a Microsoft Teams bot via public HTTPS webhook: `@microsoft/teams.cli` registration, dev-tunnel/ngrok/cloudflared exposure of port 3978, Azure client/secret/tenant credentials, AAD-object-ID allowlist, Adaptive-Card approvals, and the JWT-authenticated Bot Framework endpoint. |
| 8 | `hermes_messaging_teams_meetings_pipeline.md` | procedure | teams-meetings §What This Feature Does, §Prerequisites, §Step 1 Graph Credentials, §Step 2 Enable Graph Webhook Listener, §Step 3 Configure Teams Delivery + Pipeline, §Teams Delivery Modes (incoming_webhook/graph), §Step 4 Start Gateway, §Step 5 Create Graph Subscriptions, §Validation, §Troubleshooting | ~900 | Enable the Teams meeting-summary pipeline: Microsoft Graph app credentials, the `msgraph_webhook` listener, `teams.extra.meeting_pipeline` config, transcript-first-then-recording+STT, the two delivery modes, `hermes teams-pipeline` subscribe/validate, and the 72-hour subscription-renewal requirement. |
| 9 | `hermes_messaging_google_chat.md` | procedure | google_chat §Overview, §Steps 1–9 (GCP project, enable APIs, Service Account, Pub/Sub topic+subscription, topic+subscription IAM, Chat app config, install in space, configure Hermes), §Formatting and capabilities, §Step 10 Native attachment delivery (per-user OAuth), §Troubleshooting, §Security notes | ~1500 | Connect Hermes to Google Chat via Cloud Pub/Sub pull subscription + Chat REST API (no public URL): GCP project + two APIs, service-account JSON, topic/subscription with the publisher + subscriber IAM bindings, the no-"Chat Bot Caller"-role gotcha, the markdown subset, and the per-user OAuth `/setup-files` flow for native attachments. |

**SP11b totals:** 9 notes · procedure 8 · model 1 · concept 0 (gateway concepts are SP11a-owned terms).
6 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 8 · model 1 · concept 0 (messaging-gateway/dm-pairing/silence-token concepts are SP11a term notes).
- Source: 6 digested pages (~15.4K words) → ~12.3K words of notes (modest compression via link-outs to gateway concepts + config reference).
- BB mix: procedure 89%, model 11%.

## Section Coverage Map

```
slack.md (3626w)
├── Overview / Step 1 Create App (manifest/manual) / Step 2 Scopes / Step 3 Socket Mode → Note 1
├── Step 4 Events / Step 5 Messages Tab / Step 6 Install / Step 7 User IDs / Step 8 Configure / Step 9 Invite → Note 1
├── Slash Commands (manifest, !cmd prefix, --slashes-only) / How the Bot Responds / Troubleshooting / Quick Checklist / Security → Note 1
├── Configuration Options (Thread&Reply, Session Isolation, Mention&Trigger, allowed_channels, Unauthorized DM, Voice Transcription, Full Example) → Note 2
├── Home Channel / Multi-Workspace Support (+OAuth Token File) / Voice Messages → Note 2 (voice→SP08; gateway session→SP02)
└── Per-Channel Prompts / Per-Channel Skill Bindings ─────── → Note 2 (skills→SP05)
matrix.md (5393w)
├── intro / How Hermes Behaves / Capability Matrix / Session Model / Mention&Threading / Project Room Isolation → Note 3
├── Step 1 Bot Account / Step 2 Access Token / Step 3 User ID / Step 4 Configure / Private Deployment Hardening → Note 3
├── Start the Gateway / Home Room / Room allowlist / Commands in Matrix / Matrix Tools and Controls / Media Limits → Note 3
├── Troubleshooting (clock skew, auth, mautrix, bridge loop) / Security / Notes → Note 3 (voice MSC3245→SP08)
├── End-to-End Encryption (Requirements, Enable, modes, key storage) / Synapse Integration Tests → Note 4
├── Cross-Signing Verification / Deleting the crypto store / Upgrading from a previous version with E2EE → Note 4
└── Proxy Mode (E2EE on macOS) (diagram, host/container config, start, Config Reference, Any Platform, limitations, sync TS) → Note 5 (api_server→SP09)
mattermost.md (1982w) ── ALL sections ───────────────────── → Note 6 (gateway session→SP02; voice→SP08)
teams.md (1343w)
├── intro / How the Bot Responds / Steps 1–6 / Configuration Reference → Note 7
├── Features (Interactive Approval Cards) ───────────────── → Note 7
├── Features (Meeting Summary Delivery) ─────────────────── → Note 7 (pipeline detail→Note 8; Graph reg→SP17)
└── Production Deployment / Troubleshooting / Security ───── → Note 7
teams-meetings.md (935w) ── ALL sections ─────────────────── → Note 8 (msgraph-webhook page→SP12; day-2 operator guide→SP16; STT→SP08)
google_chat.md (2107w) ── ALL sections ───────────────────── → Note 9 (profiles→SP04; cron home-channel delivery→SP06)
```

No source H2/H3 orphaned. All 6 pages fully covered; cross-cutting detail (voice/STT, msgraph-webhook reference,
Graph app registration, day-2 operator runbook, gateway concepts) intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| slack.md (3626w, 23 code) | Note 1 (setup procedure) + Note 2 (config reference) | >2500w; two arcs — the one-time Slack-app creation/scopes/events/install procedure vs the ongoing `config.yaml` behavior reference (reply/mention/multi-workspace/per-channel). |
| matrix.md (5393w, 45 code) | Note 3 (base setup, proc) + Note 4 (E2EE, proc) + Note 5 (macOS proxy-mode, model) | >4000w → 3 notes; E2EE is a self-contained subsystem (libolm/cross-signing/crypto-store recovery) and proxy mode is a distinct deployment *model* (thin container ↔ host api_server), both BB-separable from base bot setup. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_messaging_slack`, `hermes_messaging_slack_config` | `term_slack.md` (65L active); `cc_claude_code_in_slack.md`, `cc_slack_setup_and_routing.md` (Claude Code Slack docs); `tutorial_slackbot_regionflex_*` (RegionFlex Slack bot) | **NOT a dup** — `term_slack` is the generic platform concept; the cc_/tutorial notes are a *different* product's Slack integration | CREATE; LINK `term_slack` + the analogous `cc_*` doc notes. |
| `hermes_messaging_matrix`, `hermes_messaging_matrix_e2ee`, `hermes_messaging_matrix_proxy_mode` | `term_adjacency_matrix`, `term_precision_matrix`, `term_time_management_matrix` (linear-algebra/PM) | **NOT a dup** — no `term_matrix` (Matrix protocol) exists; the hits are unrelated "matrix" homonyms | CREATE; no Matrix-protocol term to link (forward-ref gateway concepts instead). |
| `hermes_messaging_mattermost`, `hermes_messaging_google_chat` | no term/doc note covers these platforms | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0 substantive
are the Amazon-Teams false-positive (do NOT link), visually confirmed by reading the notes. New `hermes_agent/`

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note; FOUR-FLOOR)

> **Cross-ref FOUR-FLOOR standard set 2026-06-19** (master directive; supersedes the 2026-06-14 floor and the
> earlier 2026-06-19 three-floor revision): each note's `## Related Notes` carries FOUR COUNTED floors — **≥8 term
> modules that implement what each doc note documents), **≥10 snippet notes**
> pick the code each note documents), and **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in
> this series + the analogous `claude_code/cc_*` agent-tool docs + other genuinely-relevant existing doc notes). Each
> rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`, all relevancy-selected (never padded).
> **The snippet group is now a COUNTED floor (≥10), promoted from the prior BONUS group and raised from the earlier
> ≥8** — the already-mapped `snippet_hermes_agent_gw_*` / `plugins_*` / `tools_*` snippets are the implementation
> layer each note documents and now satisfy a floor. **All term IDs, all code-repo IDs, and all snippet IDs below are
> `hermes_*`) resolve at finalization (G5/G8) and are allowed un-verified; `cc_*` and the SP02/SP09/SP11a `hermes_*`
> (`term_messaging_gateway`, `term_dm_pairing`, `term_silence_token`) are ADDITIONAL forward-refs (+fin [own]), NOT

**Note 1 `hermes_messaging_slack`**
- Terms (8): term_socket_mode, term_websocket, term_oauth_token, term_authentication, term_bot, term_access_control, term_autonomous_coding_agents, term_agent_harness — relevance: Slack uses Socket Mode WebSockets + the `xoxb-`/`xapp-` OAuth bot/app tokens; `SLACK_ALLOWED_USERS` is access control; the Slack bot fronts the autonomous-coding-agent harness. (+fin [own]: term_messaging_gateway, term_dm_pairing)
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gateway/` package that implements the Slack Socket-Mode adapter (Bolt/`slack_sdk`) this page configures; repo_hermes_agent_cli — `hermes slack manifest --write/--slashes-only`, `hermes gateway setup`, and `hermes gateway [install]` subcommands the steps invoke; repo_hermes_agent_agent_core — the `AIAgent` turn loop the Slack bot routes each message into; repo_hermes_agent_plugins — the slash-command/`COMMAND_REGISTRY` surface that the generated manifest declares as native Slack commands; repo_hermes_agent — repo root/README that frames the messaging-first gateway design and the `!cmd`/`/cmd` command parity.
- Docs (10): hermes_messaging_slack_config — the companion config.yaml reference for this same Slack adapter; hermes_messaging_mattermost — a sibling self-hosted-chat bot-setup procedure with the same allowlist/mention model; hermes_messaging_matrix — sibling Matrix bot-setup procedure sharing the gateway/session model; hermes_messaging_teams_bot — sibling Teams bot-setup with the same allowlist gate; hermes_messaging_gateway_index — the SP11a gateway-concepts hub this platform note hangs off; cc_claude_code_in_slack — the directly-analogous Claude-Code Slack integration doc; cc_slack_setup_and_routing — Claude-Code Slack app/scope/routing setup, the closest external-agent sibling; cc_channels_overview — Claude-Code's "channels" surface, the conceptual analogue of a chat-platform front-end; cc_channels_setup — analogous channel-onboarding procedure (app creation, scopes, install); cc_remote_control — controlling an agent over a chat surface, the same bot-fronts-agent pattern.
- Snippets (10): snippet_hermes_agent_gw_platform_slack — the Slack Socket-Mode adapter (Bolt/`slack_sdk`, `xoxb-`/`xapp-` tokens, event subscriptions) this page configures; snippet_hermes_agent_gw_platform_base_abstract — the platform-adapter ABC the Slack adapter subclasses; snippet_hermes_agent_gw_platform_base_normalize — inbound message normalization (mention stripping, DM/channel detection) the Slack flow uses; snippet_hermes_agent_gw_platform_registry — the platform registry that registers/discovers the `slack` adapter; snippet_hermes_agent_gw_runner_acl — the `SLACK_ALLOWED_USERS`/`allowed_channels` allowlist gating this page's Security section drives; snippet_hermes_agent_gw_pairing — the unauthorized-DM pairing-code handshake (`unauthorized_dm_behavior: "pair"`); snippet_hermes_agent_gw_slash_access — the `/cmd` vs `!cmd` slash-command + admin/user access split this page's Slash Commands section documents; snippet_hermes_agent_gw_start_gateway_main — the `hermes gateway` boot entrypoint the Step 8 start command invokes; snippet_hermes_agent_gw_runner_router — the runner that routes each inbound Slack event to the agent turn; snippet_hermes_agent_gw_runner_session_key — the per-user/thread session-key derivation behind channel-thread isolation.

**Note 2 `hermes_messaging_slack_config`**
- Terms (8): term_socket_mode, term_session_persistence, term_oauth_token, term_access_control, term_multimodal, term_skills, term_persona, term_authentication — relevance: config controls per-user session isolation, multi-workspace `xoxb-` OAuth token lists + `slack_tokens.json`, `allowed_channels` access control, multimodal STT voice transcription (`stt_enabled`), per-channel skill bindings + persona `channel_prompts`. (+fin [own]: term_messaging_gateway, term_silence_token)
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the Slack adapter whose `platforms.slack` config surface (reply/thread/mention/multi-workspace) this page documents; repo_hermes_agent_cli — config load/`hermes gateway setup` plumbing that reads `~/.hermes/config.yaml`; repo_hermes_agent_agent_core — session-keying + `group_sessions_per_user` isolation the AIAgent enforces; repo_hermes_agent_skills — the skill loader behind `channel_skill_bindings` (auto-load a skill at session start); repo_hermes_agent_providers_adapters — the STT provider adapters (faster-whisper/Groq/OpenAI Whisper) `stt_enabled` voice transcription routes to.
- Docs (10): hermes_messaging_slack — the setup procedure this config reference extends; hermes_messaging_matrix — sibling with parallel `require_mention`/`free_response`/session knobs; hermes_messaging_mattermost — sibling reply-mode/mention/allowlist config; hermes_messaging_media_settings — the SP02 `platforms.*` media/voice config-reference cluster this links into; hermes_messaging_gateway_index — SP11a gateway concepts (session model, allowlist, pairing); cc_slack_setup_and_routing — Claude-Code Slack routing/config analogue; cc_channels_setup — analogous channel config (reply behavior, permissions); cc_channel_permission_relay — Claude-Code per-channel permission gating, parallel to `allowed_channels`; cc_voice_dictation — the Claude-Code voice/STT analogue for `stt_enabled`; cc_settings_files — Claude-Code config-file model, analogous to `config.yaml` knob layering.
- Snippets (10): snippet_hermes_agent_gw_platform_slack — the Slack adapter whose `platforms.slack` reply/thread/mention/multi-workspace knobs this page documents; snippet_hermes_agent_gw_config_per_channel — the per-channel config (`channel_prompts`, `channel_skill_bindings`) load path; snippet_hermes_agent_gw_config_load — the `~/.hermes/config.yaml` loader that reads these knobs; snippet_hermes_agent_gw_config_schema — the config schema that defines/defaults `reply_to_mode`, `require_mention`, `strict_mention`, `stt_enabled`; snippet_hermes_agent_gw_runner_session_key — the `group_sessions_per_user` per-user session-key isolation this config toggles; snippet_hermes_agent_gw_runner_acl — the `allowed_channels` channel-allowlist gating; snippet_hermes_agent_gw_channel_directory — the channel-directory cache backing `allowed_channels`/home-channel resolution; snippet_hermes_agent_gw_display_config — the display/reply-prefix config the `reply_prefix`/threading knobs map to; snippet_hermes_agent_gw_runner_provider_boot — the provider boot that wires the STT provider (`faster-whisper`/Groq/OpenAI Whisper) behind `stt_enabled`; snippet_hermes_agent_gw_pairing — the `unauthorized_dm_behavior: "pair"`/"ignore" handling this page configures.

**Note 3 `hermes_messaging_matrix`**
- Terms (8): term_websocket, term_authentication, term_oauth_token, term_access_control, term_bot, term_multimodal, term_session_persistence, term_agent_harness — relevance: Matrix syncs over a long-lived `client.handle_sync()` connection; the access token / password login + `MATRIX_ALLOWED_USERS`/`ALLOWED_ROOMS` gate access; media (images/audio/video) is multimodal; each DM/thread/room is its own session (`MATRIX_SESSION_SCOPE`); the bot fronts the agent harness across any homeserver. (+fin [own]: term_messaging_gateway, term_dm_pairing)
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gateway/` Matrix bridge (`mautrix` SDK) implementing connect/normalize/ACL + the explicit sync loop this page documents; repo_hermes_agent_cli — `hermes gateway setup`/`hermes gateway` start commands and `/sethome`,`/status`,`/resume --cross-room`; repo_hermes_agent_agent_core — the AIAgent + `group_sessions_per_user` room/thread session lanes; repo_hermes_agent_tools — the six `matrix_*` scoped tools (send_reaction/redact/create_room/invite/fetch_history/set_presence) and their gating flags; repo_hermes_agent — repo root/README framing the messaging-first, any-homeserver gateway.
- Docs (10): hermes_messaging_matrix_e2ee — the E2EE subsystem split out of this page; hermes_messaging_matrix_proxy_mode — the macOS E2EE proxy deployment model split out of this page; hermes_messaging_mattermost — sibling self-hosted bot-setup with the same mention/allowlist/session model; hermes_messaging_slack — sibling no-public-URL bot-setup procedure; hermes_messaging_gateway_index — SP11a gateway concepts (session scope, allowlist, auto-threading); hermes_security_skill_memory_settings — SP11a/SP02 security-settings sibling for allowlist hardening; cc_channels_overview — Claude-Code chat-surface analogue; cc_channels_setup — analogous bot/account onboarding procedure; cc_remote_control — bot-fronts-agent remote-control analogue; cc_mcp_authentication — token-based auth analogue for the access-token/password login model.
- Snippets (10): snippet_hermes_agent_gw_platform_matrix — the `mautrix` Matrix adapter (sync loop, the six `matrix_*` tools, reaction approvals) this page documents; snippet_hermes_agent_gw_platform_matrix_connect — the access-token/password login + `handle_sync()` connect path; snippet_hermes_agent_gw_platform_matrix_normalize — inbound Matrix event normalization (mention/thread/`m.notice`/bridge-ghost handling); snippet_hermes_agent_gw_platform_matrix_acl — the `MATRIX_ALLOWED_USERS`/`ALLOWED_ROOMS` + `ignore_user_patterns` gating; snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the Matrix adapter subclasses; snippet_hermes_agent_gw_runner_acl — the shared allowlist runner the Matrix ACL plugs into; snippet_hermes_agent_gw_runner_router — the runner that routes each Matrix event to an agent turn; snippet_hermes_agent_gw_session_lifecycle — the per-DM/thread/room session lifecycle (`MATRIX_SESSION_SCOPE`); snippet_hermes_agent_gw_runner_init — the explicit sync-loop startup (clock-skew startup-grace filter, `handle_sync()` registration) this page's troubleshooting describes; snippet_hermes_agent_gw_runner_session_key — the room/thread session-key derivation behind project-room isolation.

**Note 4 `hermes_messaging_matrix_e2ee`**
- Terms (8): term_encryption, term_authentication, term_idempotency, term_access_control, term_oauth_token, term_bot, term_autonomous_coding_agents, term_agent_harness — relevance: E2EE (`mautrix[encryption]` + `libolm`) encrypts room traffic; cross-signing via `MATRIX_RECOVERY_KEY` is idempotent device self-signing on each startup; access token + allowlist gate the bot identity fronting the coding-agent harness.
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the Matrix adapter's E2EE init, crypto-store (`crypto.db`), device-key upload + stale-one-time-key detection this page documents; repo_hermes_agent_cli — `hermes gateway run` startup that imports cross-signing keys, plus the migration/recovery flows; repo_hermes_agent_agent_core — the AIAgent turn loop that decrypts inbound / encrypts outbound around; repo_hermes_agent_tools — the Matrix-scoped tools that still operate inside encrypted rooms; repo_hermes_agent — repo root/README + the `hermes-agent[matrix]` extra and Synapse integration-test harness.
- Docs (10): hermes_messaging_matrix — the base Matrix setup this E2EE subsystem extends; hermes_messaging_matrix_proxy_mode — the macOS deployment model that exists specifically to run this E2EE on `libolm`-incompatible hosts; hermes_messaging_mattermost — sibling self-hosted bot-setup; hermes_messaging_slack — sibling bot-setup procedure; hermes_messaging_gateway_index — SP11a gateway concepts hub; hermes_security_skill_memory_settings — SP11a/SP02 security-settings sibling (token/recovery-key handling); cc_security_architecture — Claude-Code security-architecture analogue for credential/key handling; cc_zero_data_retention — encrypted-data-handling analogue; cc_network_tls_and_access — transport-encryption analogue; cc_mcp_authentication — token/identity-trust analogue for the device-key/cross-signing trust model.
- Snippets (10): snippet_hermes_agent_gw_platform_matrix — the Matrix adapter whose E2EE init, crypto-store (`crypto.db`), device-key upload + stale-one-time-key detection this page documents; snippet_hermes_agent_gw_platform_matrix_connect — the connect path that initializes the `libolm` crypto store and imports cross-signing keys (`MATRIX_RECOVERY_KEY`); snippet_hermes_agent_gw_platform_matrix_normalize — the decrypt-inbound/encrypt-outbound normalization around encrypted rooms; snippet_hermes_agent_gw_platform_matrix_acl — the allowlist gating that still applies inside encrypted rooms; snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the encrypted Matrix adapter subclasses; snippet_hermes_agent_gw_runner_init — the startup that detects stale-one-time-key conditions and fail-closes `required` mode; snippet_hermes_agent_gw_runner_supervisor — the supervisor that imports cross-signing keys on each startup (idempotent device self-sign); snippet_hermes_agent_gw_runner_errors — the `could not decrypt event` error handling this page's troubleshooting describes; snippet_hermes_agent_gw_session_state — the session state preserved across the crypto-store migration; snippet_hermes_agent_gw_shutdown_forensics — the forensic shutdown that redacts recovery keys/device IDs from diagnostics.

**Note 5 `hermes_messaging_matrix_proxy_mode`** (model)
- Terms (8): term_encryption, term_reverse_proxy, term_authentication, term_docker, term_session_persistence, term_idempotency, term_autonomous_coding_agents, term_agent_harness — relevance: the model is a thin Docker (Linux VM) container doing E2EE + HTTP-forward to the host's `API_SERVER_KEY`-authenticated `api_server` (port 8642); the container acts as a reverse-proxy front; sessions persist via the idempotent `X-Hermes-Session-Id` header so the host coding-agent harness keeps continuity. (+fin [own]: term_messaging_gateway)
- Code-Repos (5): repo_hermes_agent_gateway_messaging — both the thin Matrix adapter AND the host `api_server` adapter (`/v1/chat/completions`, `GATEWAY_PROXY_URL` forward) this model wires together; repo_hermes_agent_tui_gateway — the WebSocket-decoupled gateway where the front-end and agent back-end are physically separated, the same host↔container decoupling pattern; repo_hermes_agent_agent_core — the host-side `AIAgent` that is the "single source of truth" the container forwards into; repo_hermes_agent_cli — the `hermes gateway` start on host + container and the `API_SERVER_*`/`GATEWAY_PROXY_*` env split; repo_hermes_agent_acp — another "agent backend over a transport" decoupling (ACP server), architecturally analogous to the proxy-mode forward.
- Docs (10): hermes_messaging_matrix — the base Matrix bot the container runs; hermes_messaging_matrix_e2ee — the E2EE this proxy mode exists to host on macOS; hermes_api_server — the SP09 api_server doc the container HTTP-forwards into (decrypted text → host agent); hermes_messaging_mattermost — sibling platform that can also use `GATEWAY_PROXY_URL` ("Works for Any Platform"); hermes_terminal_backends — SP11a sibling on decoupled front-end/back-end terminal transports; hermes_messaging_gateway_index — SP11a gateway concepts hub; cc_proxy_and_gateway_config — the directly-analogous Claude-Code proxy/gateway deployment config; cc_background_session_hosting — hosting an agent back-end separately from the front-end, the same split; cc_devcontainer_hardening — the container-side hardening analogue for the thin Docker adapter; cc_sandbox_filesystem_network_isolation — the network-isolation rationale (run the adapter in a different env from the agent) this model is built around.
- Snippets (10): snippet_hermes_agent_gw_platform_matrix — the thin Matrix adapter the Docker container runs (E2EE only, no inference); snippet_hermes_agent_gw_platform_matrix_connect — the container-side connect path that decrypts then HTTP-forwards via `GATEWAY_PROXY_URL`; snippet_hermes_agent_gw_platform_api_server_connect — the host `api_server` adapter (`0.0.0.0:8642`, `API_SERVER_KEY`) the container forwards into; snippet_hermes_agent_gw_platform_api_server_routes — the `/v1/chat/completions` + `/health` routes the container POSTs to; snippet_hermes_agent_gw_platform_api_server_middleware — the bearer-token (`API_SERVER_KEY`) auth middleware on the host endpoint; snippet_hermes_agent_gw_session_context — the `X-Hermes-Session-Id` header handling that maintains session continuity across the proxy; snippet_hermes_agent_gw_session_lifecycle — the host-side unified session lifecycle (CLI/Matrix/Telegram share one memory); snippet_hermes_agent_gw_runner_outbound — the outbound path that streams the host's response back to the container for re-encryption; snippet_hermes_agent_gw_runner_provider_boot — the provider boot that runs ONLY on the host (the container has no LLM keys); snippet_hermes_agent_gw_start_gateway_main — the `hermes gateway` boot entrypoint started on both host and container.

**Note 6 `hermes_messaging_mattermost`**
- Terms (8): term_websocket, term_message_queue, term_authentication, term_oauth_token, term_access_control, term_bot, term_session_persistence, term_reverse_proxy — relevance: Mattermost uses REST v4 + a WebSocket real-time event stream on self-hosted infra (the nginx reverse-proxy `Upgrade` fix); bot-account / personal-access tokens authenticate; `MATTERMOST_ALLOWED_USERS`/`allowed_channels` gate; sessions isolate per user; events stream queue-style with exponential-backoff reconnect.
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gateway/` Mattermost adapter (`aiohttp` REST v4 + WebSocket consumer, reconnect/backoff) this page documents; repo_hermes_agent_cli — `hermes gateway setup`/`hermes gateway` start + `/sethome` and `MATTERMOST_*` config; repo_hermes_agent_agent_core — the AIAgent + per-user `group_sessions_per_user` channel/thread session isolation; repo_hermes_agent_plugins — the per-channel-prompt / command-handling surface; repo_hermes_agent — repo root/README that notes the adapter reuses the already-bundled `aiohttp` (no extra dependency).
- Docs (10): hermes_messaging_slack — the closest sibling (Mattermost is the self-hosted Slack alternative); hermes_messaging_matrix — sibling self-hosted bot-setup with the same model; hermes_messaging_google_chat — sibling no-public-URL pull-based bot; hermes_messaging_media_settings — SP02 `platforms.*` config-reference cluster; hermes_messaging_gateway_index — SP11a gateway concepts hub; hermes_security_skill_memory_settings — SP11a/SP02 security-settings sibling (token/allowlist); cc_channels_overview — Claude-Code chat-surface analogue; cc_channels_setup — analogous bot/account onboarding; cc_channel_permission_relay — per-channel permission analogue for `allowed_channels`; cc_remote_control — bot-fronts-agent remote-control analogue.
- Snippets (10): snippet_hermes_agent_gw_platform_mattermost — the `aiohttp` REST v4 + WebSocket Mattermost adapter (bot/personal-access token, reconnect/backoff) this page documents; snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the Mattermost adapter subclasses; snippet_hermes_agent_gw_platform_base_normalize — inbound normalization (mention stripping, DM/channel detect, 26-char user ID); snippet_hermes_agent_gw_platform_base_outbound — the outbound post path (flat vs `MATTERMOST_REPLY_MODE=thread`); snippet_hermes_agent_gw_runner_acl — the `MATTERMOST_ALLOWED_USERS`/`allowed_channels` gating; snippet_hermes_agent_gw_runner_session_key — per-user `group_sessions_per_user` channel/thread session isolation; snippet_hermes_agent_gw_config_per_channel — the `channel_prompts` per-channel config load path; snippet_hermes_agent_gw_stream_consumer — the WebSocket real-time event stream consumer (nginx `Upgrade` fix context); snippet_hermes_agent_gw_runner_errors — the WebSocket reconnect (2s→60s exponential backoff) + 403/auth error handling this page's troubleshooting describes; snippet_hermes_agent_gw_runner_router — the runner that routes each inbound Mattermost event to the agent turn.

**Note 7 `hermes_messaging_teams_bot`**
- Terms (8): term_authentication, term_oauth_token, term_access_control, term_reverse_proxy, term_bot, term_human_in_the_loop, term_autonomous_coding_agents, term_agent_harness — relevance: Teams delivers via a public HTTPS `/api/messages` webhook (port 3978) JWT-authenticated by the Bot Framework, behind a dev-tunnel/ngrok/cloudflared reverse-proxy; the `TEAMS_CLIENT_ID`/`SECRET`/`TENANT_ID` are Azure-AD credentials; `TEAMS_ALLOWED_USERS` (AAD object IDs) is access control; Adaptive-Card approvals are human-in-the-loop; the bot fronts the coding-agent harness.
- Code-Repos (5): repo_hermes_agent_plugins — the Teams adapter lives in the plugins layer (`plugins.platforms.teams`), implementing the webhook server + Adaptive-Card approvals this page documents; repo_hermes_agent_gateway_messaging — the gateway base (platform registry, outbound delivery, `/health`) the Teams adapter plugs into; repo_hermes_agent_cli — `@microsoft/teams.cli` is external, but `hermes gateway setup`/`hermes gateway` (docker compose) start commands + `TEAMS_*` env config are CLI-driven; repo_hermes_agent_agent_core — the AIAgent the Teams bot routes turns into; repo_hermes_agent — repo root/README + the `teams` extra (`uv sync --extra teams`) and Bot-Framework SDK import.
- Docs (10): hermes_messaging_teams_meetings_pipeline — the companion meeting-summary pipeline that shares this same Teams platform entry; hermes_messaging_slack — sibling bot-setup (contrasted: Socket Mode vs public webhook); hermes_messaging_mattermost — sibling allowlist/mention bot-setup; hermes_messaging_matrix — sibling bot-setup procedure; hermes_messaging_gateway_index — SP11a gateway concepts hub; hermes_security_skill_memory_settings — SP11a/SP02 security-settings sibling (client-secret/allowlist); cc_channels_overview — Claude-Code chat-surface analogue; cc_channels_security_and_enterprise_controls — Teams/AAD enterprise allowlist analogue; cc_network_tls_and_access — public-HTTPS-endpoint/TLS analogue (Teams rejects self-signed certs); cc_remote_control — bot-fronts-agent + interactive-approval analogue.
- Snippets (10): snippet_hermes_agent_plugins_platform_teams — the Teams adapter plugin (`plugins.platforms.teams`) implementing the JWT-authed `/api/messages` webhook server + Adaptive-Card approvals this page documents; snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the Teams plugin adapter subclasses; snippet_hermes_agent_gw_platform_base_normalize — inbound normalization that strips the `<at>BotName</at>` mention tags Teams delivers; snippet_hermes_agent_gw_platform_base_outbound — the outbound delivery path the Teams adapter uses; snippet_hermes_agent_gw_platform_registry — the registry the Teams adapter registers into; snippet_hermes_agent_gw_runner_acl — the `TEAMS_ALLOWED_USERS` (AAD object ID) allowlist gating; snippet_hermes_agent_gw_delivery — the outbound delivery surface (incl. meeting-summary delivery) shared with the pipeline; snippet_hermes_agent_gw_status_health — the `/health` endpoint (`curl http://localhost:3978/health`) this page checks; snippet_hermes_agent_gw_start_gateway_main — the `hermes gateway` / docker-compose boot entrypoint; snippet_hermes_agent_gw_runner_router — the runner that routes each Bot-Framework webhook event to an agent turn.

**Note 8 `hermes_messaging_teams_meetings_pipeline`**
- Terms (8): term_authentication, term_oauth_token, term_multimodal, term_idempotency, term_access_control, term_message_queue, term_human_in_the_loop, term_bot — relevance: the pipeline ingests Microsoft Graph webhook notifications (`/msgraph/webhook`, `MSGRAPH_WEBHOOK_CLIENT_STATE` shared secret), prefers transcripts then falls back to recording + multimodal STT (`ffmpeg`), stores durable idempotent job/sink state, and delivers summaries; Graph app-only credentials auth-gate it; subscriptions queue events and expire at 72h.
- Code-Repos (5): repo_hermes_agent_plugins — the `teams_pipeline` plugin that registers the `hermes teams-pipeline` subcommand and binds to the webhook ingress; repo_hermes_agent_gateway_messaging — the `msgraph_webhook` gateway platform (listener exposing `/msgraph/webhook` + `/health`); repo_hermes_agent_tools — the Microsoft Graph tool/client foundation (meeting resolution, transcript/recording artifact fetch); repo_hermes_agent_cron — the scheduled `maintain-subscriptions` renewal that beats the 72h Graph subscription cap; repo_hermes_agent_cli — `hermes teams-pipeline subscribe/validate/list/maintain-subscriptions/token-health` subcommands this page runs.
- Docs (10): hermes_messaging_teams_bot — the prerequisite Teams bot/credential setup + the outbound delivery surface this pipeline reuses; hermes_messaging_slack — sibling bot-setup; hermes_messaging_matrix — sibling bot-setup; hermes_messaging_mattermost — sibling bot-setup; hermes_messaging_google_chat — sibling pull/subscription-based event ingest; hermes_messaging_gateway_index — SP11a gateway concepts hub; cc_scheduled_task_execution_model — the directly-analogous scheduled-execution model (the 72h subscription-renewal cron); cc_loop_scheduled_tasks — recurring scheduled-task analogue for `maintain-subscriptions`; cc_mcp_transports — webhook/event-transport analogue for the Graph notification path; cc_voice_dictation — STT/transcription analogue for the recording-fallback transcription step.
- Snippets (10): snippet_hermes_agent_gw_platform_msgraph_webhook — the `msgraph_webhook` gateway platform exposing `/msgraph/webhook` + `/health` (`MSGRAPH_WEBHOOK_CLIENT_STATE`, `allowed_source_cidrs`) this page enables; snippet_hermes_agent_plugins_teams_pipeline — the `teams_pipeline` plugin registering the `hermes teams-pipeline` subcommand + transcript-first/recording-fallback pipeline; snippet_hermes_agent_plugins_platform_teams — the Teams adapter the pipeline reuses for `delivery_mode: graph`/`incoming_webhook` outbound; snippet_hermes_agent_tools_msgraph — the Microsoft Graph client (meeting resolution, transcript/recording artifact fetch); snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the webhook listener subclasses; snippet_hermes_agent_gw_runner_cron — the scheduled `maintain-subscriptions` renewal beating the 72h Graph subscription cap; snippet_hermes_agent_gw_delivery — the summary outbound-delivery path (`graph`/`incoming_webhook`); snippet_hermes_agent_gw_runner_init — the listener init that binds the webhook ingress + validates client-state; snippet_hermes_agent_gw_status_health — the listener `/health` check (`curl http://localhost:8646/health`); snippet_hermes_agent_gw_platform_registry — the registry that registers the `msgraph_webhook` platform.

**Note 9 `hermes_messaging_google_chat`**
- Terms (8): term_pub_sub, term_authentication, term_oauth_token, term_iam, term_access_control, term_pii, term_bot, term_data_residency — relevance: Google Chat uses Cloud Pub/Sub pull subscriptions (inbound) + Chat REST API (outbound) with a service-account JSON authenticated by least-privilege subscription-scoped IAM (`roles/pubsub.subscriber`+`viewer`); the per-user OAuth flow (`/setup-files`, `chat.messages.create`) for native attachments; `GOOGLE_CHAT_ALLOWED_USERS` (emails) is access control; logs are PII/SA-email-redacted; the compliance note gates regulated/data-residency workspaces.
- Code-Repos (5): repo_hermes_agent_plugins — the Google Chat adapter + its `plugins.platforms.google_chat.oauth` module (Pub/Sub pull consumer, Chat REST, per-user OAuth) this page documents; repo_hermes_agent_gateway_messaging — the gateway base (platform registry, outbound delivery, session keying) the adapter plugs into; repo_hermes_agent_cli — `hermes gateway setup`/`hermes gateway` start + `GOOGLE_CHAT_*` config and the `/setup-files` slash command; repo_hermes_agent_agent_core — the AIAgent the bot routes turns into + the redaction (`agent/redact.py`) that strips SA emails/paths; repo_hermes_agent_cron — the home-channel (`GOOGLE_CHAT_HOME_CHANNEL`) proactive/cron-job delivery destination.
- Docs (10): hermes_messaging_slack — sibling no-public-URL bot (the page explicitly compares to Slack Socket Mode); hermes_messaging_matrix — sibling bot-setup; hermes_messaging_mattermost — sibling self-hosted bot; hermes_messaging_teams_bot — sibling Azure/Graph-credentialed bot; hermes_messaging_teams_meetings_pipeline — sibling subscription/event-ingest pipeline; hermes_messaging_gateway_index — SP11a gateway concepts hub; hermes_security_skill_memory_settings — SP11a/SP02 security-settings sibling (SA-key/allowlist); cc_channels_security_and_enterprise_controls — IAM/least-privilege + compliance-gate analogue; cc_legal_and_compliance — the data-residency/AI-governance approval analogue; cc_zero_data_retention — PII-redaction/data-handling analogue.
- Snippets (10): snippet_hermes_agent_plugins_platform_google_chat — the Google Chat adapter + `plugins.platforms.google_chat.oauth` module (Pub/Sub pull consumer, Chat REST, per-user OAuth `/setup-files`) this page documents; snippet_hermes_agent_gw_platform_base_abstract — the platform ABC the Google Chat plugin adapter subclasses; snippet_hermes_agent_gw_platform_base_normalize — inbound normalization (`ADDED_TO_SPACE`/self-message filtering, `thread.name` detection); snippet_hermes_agent_gw_platform_base_outbound — the outbound Chat REST post + in-place edit (`Hermes is thinking…`) path; snippet_hermes_agent_gw_runner_acl — the `GOOGLE_CHAT_ALLOWED_USERS` (email) allowlist gating; snippet_hermes_agent_gw_runner_session_key — the per-thread session-key isolation (each `thread.name` its own session); snippet_hermes_agent_gw_delivery — the outbound message-split (4000-char cap) delivery path; snippet_hermes_agent_gw_stream_consumer — the Cloud Pub/Sub pull-subscription consumer (FlowControl `GOOGLE_CHAT_MAX_MESSAGES`/`MAX_BYTES`); snippet_hermes_agent_gw_runner_cron — the `GOOGLE_CHAT_HOME_CHANNEL` proactive/cron-job delivery destination; snippet_hermes_agent_gw_runner_errors — the `Pub/Sub stream died`/403/rate-limit exponential-backoff handling this page's troubleshooting describes.

All 9 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (FOUR-FLOOR) — every term ID, every code-repo ID, and
`snippet_hermes_agent_*` + all `cc_*` doc targets re-verified active 2026-06-19). No placeholders, no fallback markers (the eight non-existent term slugs caught at the 2026-06-15
finalization — `term_secret_management`, `term_rest_api`, `term_self_hosted`, `term_webhook`, `term_jwt`, `term_ssrf`,
`term_speech_to_text`, `term_federation` — were already replaced inline before lock-in; post-grep re-verify confirmed
0 failing IDs). `hermes_*` doc links resolve in `resources/documentation/hermes_agent/` (intra-series + SP11a
`hermes_messaging_gateway_index`/`hermes_security_skill_memory_settings`/`hermes_terminal_backends` and SP09
`hermes_api_server` / SP02 `hermes_messaging_media_settings` siblings land at finalization, verified by G5/G8); `cc_*`

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 6 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 slack (setup) | procedure | 1700 | ≤6 (curate from ~12 short cmd/yaml blocks; tables in prose) | ✓ |
| 2 slack-config | procedure | 1500 | 6 (canonical yaml per config block) | ✓ |
| 3 matrix (base) | procedure | 2000 | ≤6 (curate from ~20 env/yaml blocks; one canonical per surface) | ✓ |
| 4 matrix-e2ee | procedure | 1300 | ≤6 (from install/recovery blocks) | ✓ |
| 5 matrix-proxy-mode | model | 1100 | 5 (host env, container compose, dockerfile, diagram, config table) | ✓ |
| 6 mattermost | procedure | 1300 | ≤6 (curate from 14; nginx + env blocks) | ✓ |
| 7 teams-bot | procedure | 1000 | 6 | ✓ |
| 8 teams-meetings | procedure | 900 | ≤6 (from 12; pipeline yaml + subscribe blocks) | ✓ |
| 9 google-chat | procedure | 1500 | 6 (env + pip + oauth blocks) | ✓ |

No further splits needed — all 9 notes ≤2500w. Matrix base (Note 3 at ~2000w) is the densest single note; checked for
further split → it is one cohesive base-setup procedure (account→token→config→hardening→tools→troubleshoot) with no
BB mixing (E2EE + proxy already split out) → KEEP (per review CP6 default-to-keep justification). Code-heavy pages
curate to ≤6 load-bearing blocks (verbatim for kept blocks), rest summarized in prose. If any note exceeds 350 lines
during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`, the
closest sibling external-agent-docs folder — verified field order against `cc_slack_setup_and_routing.md` and
`cc_claude_code_in_slack.md`, the directly-analogous Slack-integration doc notes): YAML field order `tags → keywords
→ topics → language → date of note → status → building_block → source_url → access_control_group`; body `# Title →
## Overview (opener leading with what it IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w/≤6 code/≤400
lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`, `parent`, `author`,
`related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML. Not invented — matches
existing `cc_` notes.

## Undigested Terms Plan (SP11b)

**SP11b owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes gateway concept
SP11b touches is owned by SP11a (the gateway-concepts part of the SP11 split) or is an existing verified term.
Augment re-read surfaced **0 new** undigested terms that SP11b should own after a collision audit — each platform's
setup detail (Socket Mode, E2EE, Pub/Sub, service account, proxy mode) either maps to an already-active vault term
or is a platform-specific implementation detail, not a vault-wide reusable concept warranting a standalone capture.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_messaging_gateway` | LINK only (forward-ref, +fin [own]) | SP11a | platform↔agent bridge concept; SP11a owns the capture, SP11b links it from every platform note. |
| `term_dm_pairing` | LINK only (+fin [own]) | SP11a | the unauthorized-DM pairing-code handshake; concept home is SP11a. |
| `term_silence_token` | LINK only (+fin [own]) | SP11a | the `[SILENT]` intentional non-reply; concept home is SP11a. |
| `term_speech_to_text`, `term_text_to_speech` | LINK only (+fin) | SP08 | Slack/Matrix/Teams voice in/out config; concept homes are SP08 media/web tools (use active `term_multimodal` to the ≥8 floor). |
| `term_provider_routing`, `term_fallback_provider` | LINK only (+fin) | SP09 | Matrix `!model --provider` switching references; conceptually owned by SP09. |
| `term_hermes_profile` | LINK only (+fin) | SP04 | Google Chat per-profile OAuth client scoping; concept home is SP04. |

### Renamed (general → specific)

— (audit performed; SP11b owns 0 new term captures, so no slugs to rename. The specificity heuristic was applied to
the master's forward-ref slugs SP11b links; all are already scope-qualified by their owning sub-plans.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_slack` (would duplicate) | `term_slack.md` (65L, active) — generic Slack platform concept | Not captured — link the existing term from the Slack doc notes. |
| `term_socket_mode` (would duplicate) | `term_socket_mode.md` (active) | Not captured — link the existing term from the Slack note. |
| `term_matrix_protocol` (would-be) | none substantive (`term_*_matrix` hits are linear-algebra homonyms) | No removal — SP11b documents the Matrix protocol as a doc note, not a term capture; gateway concept owned by SP11a. |

## Term-Note Authoring Requirements

N/A (inherited) — SP11b owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP04/08/09/11a). The full Term-Note Authoring
guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion, >200-line decomposition) apply to
those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (Slack + Mattermost, pilot):** Notes 1, 2, 6. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (Matrix family):** Notes 3, 4, 5. GATE G1–G8.
- **Phase 3 (Teams + Google Chat):** Notes 7, 8, 9. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for kept
blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every ref)** ·
**G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB · **G8 in-degree ≥1
from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_messaging_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_messaging_slack hermes_messaging_slack_config hermes_messaging_matrix hermes_messaging_matrix_e2ee hermes_messaging_matrix_proxy_mode hermes_messaging_mattermost hermes_messaging_teams_bot hermes_messaging_teams_meetings_pipeline hermes_messaging_google_chat; do
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note
series) under a "Messaging: Team Chat (Slack, Matrix, Mattermost, Teams, Google Chat)" sub-section of the master's
Messaging section (alongside SP11a's gateway-concepts rows). Parent hub back-link in `entry_research_and_ai_hub.md`
is handled at master level. SP11b does NOT create a separate entry point — the >30-note corpus shares the single
master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_messaging_slack`, `hermes_messaging_matrix`, `hermes_messaging_mattermost`, `hermes_messaging_teams_bot`, `hermes_messaging_google_chat` | gateway/messaging repo ↔ platform setup docs |
| `snippet_hermes_agent_gw_platform_slack.md` | → `hermes_messaging_slack`, `hermes_messaging_slack_config` | Slack adapter code ↔ Slack usage docs |
| `snippet_hermes_agent_gw_platform_matrix.md` | → `hermes_messaging_matrix`, `hermes_messaging_matrix_e2ee`, `hermes_messaging_matrix_proxy_mode` | Matrix adapter code ↔ Matrix usage docs |
| `snippet_hermes_agent_gw_platform_mattermost.md` | → `hermes_messaging_mattermost` | Mattermost adapter code ↔ usage doc |
| `snippet_hermes_agent_plugins_platform_teams.md` | → `hermes_messaging_teams_bot` | Teams adapter plugin ↔ usage doc |
| `snippet_hermes_agent_gw_platform_msgraph_webhook.md` | → `hermes_messaging_teams_meetings_pipeline` | Graph webhook listener ↔ meeting-pipeline doc |
| `snippet_hermes_agent_plugins_platform_google_chat.md` | → `hermes_messaging_google_chat` | Google Chat adapter plugin ↔ usage doc |
| `term_slack.md` | → `hermes_messaging_slack` | concept term → Hermes Slack setup doc |
| `term_socket_mode.md` | → `hermes_messaging_slack` | concept term → Socket Mode setup doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_messaging_slack`, `hermes_messaging_matrix` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution phase
(Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_messaging_slack`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT
work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6 load-bearing blocks, summarize
the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If multi-agent: agents return note
content, master writes serially where there is write-contention; ≤30 agents/run; embed the manifest in the workflow
script.

## Follow-up Recommendations

- After SP11b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 rows to the
  master-created entry point; backfill the `repo_hermes_agent_gateway_messaging` / `snippet_hermes_agent_gw_platform_*`
  / `term_*` inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After SP11a lands: cross-link the gateway-concept terms (`term_messaging_gateway`/`term_dm_pairing`/`term_silence_token`)
  into all 9 SP11b notes' Related Notes (the +fin forward-refs); bidirectional concept↔platform links.
- Consider one `thought_` note comparing Hermes' docs-stated gateway design vs the code-digestion findings in
  `snippet_hermes_agent_gw_platform_*`.

## Augmentation Report

  false-positive NOT-linked; no `term_matrix`), finalized Per-Note Mapping (≥8 term + ≥5 code-repo + ≥10 snippet +
  Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  517-note Hermes implementation corpus, all relevance-clause-justified against the code the page documents).
- Density re-read: counts match measured; **no additional splits** beyond the planned 3 (slack→2, matrix→3). All 9
  notes ≤2500w; code-heavy notes curated to ≤6 blocks.
  are the Amazon-Teams false-positive (NOT linked); no `term_matrix` exists; no doc note duplicates an existing term/doc note.
- Term placeholder catch: **8 non-existent term slugs caught at finalization** (`term_secret_management`, `term_rest_api`,
  `term_self_hosted`, `term_webhook`, `term_jwt`, `term_ssrf`, `term_speech_to_text`, `term_federation`) and replaced
- Undigested terms surfaced at augment: **0 new** (SP11b owns 0 captures; all gateway concepts owned by SP11a, voice
  by SP08, profile by SP04, provider-routing/fallback by SP09).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split Decisions ✓
Points ✓ Inlinks (all 9) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓ Validation Scripts ✓ Pacing ✓
Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture Phase per term (N/A — 0 owned) ✓ best-fit
glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches
size threshold ✓ Slug Specificity (N/A — 0 owned; audit noted) ✓ Slug Collision (`term_slack` LINK + `term_teams`
false-positive + 7 placeholders caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND
documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items are
N/A-pass (SP11b owns 0 captures); dedup/collision items are substantively PASS (audit performed on all 9 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY (9/9).** **Re-reviewed 2026-06-19 (FOUR-FLOOR) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes step (FOUR-FLOOR) | PASS | All 9 planned notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (programmatic count: every note = 8/5/10/10, no duplicate IDs within a group). Each code-repo/doc/snippet item carries an inline `— relevance:` clause (Code-Repos 5 clauses, Docs 10, Snippets 10 per note); Terms carry a group-level relevance clause covering all 8 — no bare links. Anti-fab DB-verify 2026-06-19: 22/22 distinct terms active, 11/11 code-repos active, 42/42 distinct snippet IDs active, 21/21 cited `cc_*` doc IDs active (the two "missing" grep hits were the `snippet_hermes_agent_gw_*` / `_platform_*` WILDCARD glob text in the preamble/follow-ups, not cited links). Sibling `hermes_*` doc IDs exempt (created later). 0 fabricated/missing cited IDs. |
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows under the Messaging/Team-Chat section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 notes ≤30; master holds the corpus-level split. |
| CP6 | Borderline density → split | PASS | slack→2, matrix→3 (>4000w); all notes ≤2500w; code-heavy notes curated ≤6; matrix base (Note 3 ~2000w) checked → cohesive single-BB, KEEP justified. |
| CP7 | Source counts measured | PASS | Spot re-measured 2026-06-19 (mirror c253b07, `wc`): teams 1360w/14code (plan 1343/14), google_chat 2127w/6code (plan 2107/6), matrix 5408w/45code (plan 5393/45 — the 45 counts all fenced incl. indented blocks, 90 fence lines÷2). All ratios ~1.00 (≤±1.5% words). matrix >4000w → 3-note split confirmed. measured ≈ plan. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP11b owns 0 term captures (gateway concepts SP11a; voice SP08; profile SP04; routing/fallback SP09); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 notes from repo_*/snippet_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION (FOUR-FLOOR confirmed 2026-06-19).**

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from NousResearch/hermes-agent `website/docs/` at main HEAD (catalog `c253b07`; the local
`inbox/hermes_agent_docs/` mirror is byte-identical to upstream main). Re-measured all 6 owned pages with the ledger
convention (body words; ```-fence lines ÷ 2). Changed pages:

- user-guide/messaging/teams.md — 1308w/13code -> 1343w/14code

The other 5 owned pages are unchanged and re-confirmed stable: matrix.md 5393w/45code, slack.md 3626w/23code,
google_chat.md 2107w/6code, mattermost.md 1982w/14code, teams-meetings.md 935w/12code (3 spot-re-measured: matrix,
slack, google_chat — all identical to the 2026-06-15 ledger).

**Density re-decision:** none. The teams.md growth is +35w / +1 code block, entirely immaterial — Note 7
(`hermes_messaging_teams_bot`, ~1000w via link-outs) stays well under the 2500w / 6-code / 400-line caps, and its
Density Re-Assessment row already pins code to a curated `6` (not the raw page count), so no split is triggered. No
other note derives a count from teams.md. Outcome: **no-split**, all 9 planned notes remain within caps.

**Cross-ref floor (updated 2026-06-19 to FOUR-FLOOR):** now >=8 term + >=5 code-repo + >=10 snippet + >=10 doc per

**Plan remains READY** for execution (9/9 checkpoints still pass; no re-review required for a sub-cap count drift).

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented FOUR-FLOOR 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed FOUR-FLOOR 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/{slack,matrix,mattermost,teams,teams-meetings,google_chat}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
