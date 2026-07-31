---
title: Hermes Agent Docs Digestion — Sub-Plan 12b — Messaging: SimpleX, iMessage, Photon, Home Assistant, Open WebUI, Webhooks, Raft
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
pages:
  - user-guide/messaging/simplex.md
  - user-guide/messaging/bluebubbles.md
  - user-guide/messaging/photon.md
  - user-guide/messaging/homeassistant.md
  - user-guide/messaging/open-webui.md
  - user-guide/messaging/webhooks.md
  - user-guide/messaging/msgraph-webhook.md
  - user-guide/messaging/raft.md
---

# Sub-Plan 12b: Messaging — SimpleX, BlueBubbles/iMessage, Photon, Home Assistant, Open WebUI, Webhooks (GitHub/GitLab), MS-Graph Webhook

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Part **b** of the SP12
> split (consumer + webhooks). Inherits shared Routing, Note Format Definition, Dedup Policy,
> Cross-References, 8-GATE, Pacing from [the master](plan_digest_hermes_agent_docs_master.md). This file is
> the ONLY place SP12b's note filenames/BBs/coverage are defined.

## Scope

The privacy/consumer + webhook tail of the messaging gateway: SimpleX Chat (private decentralised), Apple
iMessage via BlueBubbles (self-hosted Mac relay) and via Photon (managed line pool), Home Assistant
(smart-home gateway + 4 device tools), Open WebUI (OpenAI-compatible API-server frontend), the generic
webhook adapter (GitHub/GitLab/Stripe → agent runs + cross-platform delivery), the Microsoft Graph
change-notification listener, and the Raft external-agent wake-channel bridge. Source = 8 mirrored pages in
`inbox/hermes_agent_docs/` (all substantive).
**P2 / features.** All shared gateway concepts (messaging gateway, DM pairing, silence token) are
**SP11a-owned** → LINK as forward-refs (+fin). Existing verified terms (idempotency, oauth, prompt-injection,
session-persistence, authentication) are LINKED, not recreated.

## Content Strategy

- **One BB per note.** Each platform page is a self-contained setup procedure → 1 note each. `webhooks.md`
  (2756w, 17 code) exceeds the 2500w cap and mixes a config/route *model* (route properties, delivery
  targets, HMAC/idempotency/rate-limit security model) with two procedural arcs (static config + GitHub/GitLab
  walkthroughs; dynamic CLI subscriptions + direct-delivery) → SPLIT into 2 notes (see Split Decisions).
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the gateway
  core (pairing, ACL, delivery, session-keying), the messaging overview + Telegram/Discord/Slack platform
  pages (SP11a/SP11b), the API-server feature page + provider routing (SP09), the GitHub-PR-review/webhook
  guides (SP16), the MS-Graph app-registration guide + teams pipeline (SP17), the Teams bot platform (SP11b),
  config.yaml platform blocks (SP02), code-execution/Docker/SSH sandboxing (SP03/SP08).
- **Collision (audit): `term_photon.md` (active) is an Amazon investigation-automation "Photon"
  (Unit-of-Work / Paragon / HITL), NOT the Hermes Photon iMessage relay** — a textbook LIKE false-positive.
  The planned `hermes_photon_imessage` is NOT a duplicate; create it and do NOT link the unrelated term.
- **Collision: `term_simplex_method.md` (active) is the linear-programming simplex algorithm**, NOT SimpleX
  Chat — LIKE false-positive. `hermes_simplex_chat` is NOT a dup; do not link the unrelated term.
- **Collision: `term_api_gateway.md` (active) is the generic API-gateway pattern** — the planned notes
  describe Hermes' concrete platform adapters; LINK `term_api_gateway`/`term_reverse_proxy` as related where
  the note is HTTP-serving (webhooks/open-webui/msgraph), do NOT treat as duplicate.
- **Owned NEW term captures: 0.** Webhook/messaging-gateway concepts are SP11a-owned (`term_messaging_gateway`,
  `term_dm_pairing`, `term_silence_token`) → link as +fin. A `term_webhook_route` capture was CONSIDERED and
  REJECTED at audit: the concept is a Hermes-config-specific construct (route properties + HMAC + delivery)
  best documented in the `hermes_webhooks_routes_security` doc note itself, not a broadly-reusable

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/messaging/webhooks.md | 2756 | 17 | MIXED model+procedure | 2 (split) |
| user-guide/messaging/open-webui.md | 1898 | 16 | procedure | 1 |
| user-guide/messaging/homeassistant.md | 1227 | 12 | procedure | 1 |
| user-guide/messaging/photon.md | 1123 | 11 | procedure | 1 |
| user-guide/messaging/msgraph-webhook.md | 1094 | 5 | procedure | 1 |
| user-guide/messaging/bluebubbles.md | 833 | 9 | procedure | 1 |
| user-guide/messaging/simplex.md | 738 | 7 | procedure | 1 |
| user-guide/messaging/raft.md | 480 | 2 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_messaging_simplex.md` | procedure | simplex §Prerequisites, §Install simplex-chat, §Start the daemon, §Configure Hermes (wizard/env+table), §Find contact ID, §Authorization, §Group chats, §Attachments, §Cron jobs, §Privacy notes, §Troubleshooting | ~750 | Connect Hermes to SimpleX Chat (private, no-persistent-ID messenger): install the simplex-chat daemon + `websockets`, point `SIMPLEX_WS_URL` at the local WebSocket, allowlist contact IDs / DM-pair, opt-in groups via `group:` prefix, XFTP attachments, local-only E2E-encrypted transport. |
| 2 | `hermes_messaging_bluebubbles_imessage.md` | procedure | bluebubbles §Prerequisites, §Setup (1 install server, 2 URL+password, 3 configure + require_mention/mention_patterns, 4 authorize, 5 start), §How It Works, §Environment Variables, §Features, §Private API, §Troubleshooting | ~850 | Connect Hermes to Apple iMessage via the self-hosted BlueBubbles Mac server: server URL/password, webhook-push inbound + REST outbound, DM-pairing/allowlist auth, group mention-gating, tapback/typing/read-receipts via the Private API helper, chat-by-address resolution. |
| 3 | `hermes_photon_imessage.md` | procedure | photon §Architecture, §Prerequisites, §First-time setup (device login/project/Spectrum/number/sidecar), §Authorizing users, §Require mentions, §Start the gateway, §Status & troubleshooting, §Limits today, §Env vars | ~1050 | Connect Hermes to iMessage through Photon's managed line pool (no Mac relay): a Node `spectrum-ts` gRPC sidecar supervised over loopback, device-code login + Spectrum project/number provisioning, DM-pairing auth, free-tier quotas, outbound-only attachments today. |
| 4 | `hermes_messaging_homeassistant.md` | procedure | homeassistant §Setup (token, env, start), §Available Tools (ha_list_entities/get_state/list_services/call_service), §Gateway Platform real-time events (filtering, formatting, responses, connection mgmt), §Security (blocked domains, entity-ID validation), §Example Automations, §Troubleshooting | ~1150 | Integrate Hermes with Home Assistant two ways: a WebSocket gateway platform that forwards filtered `state_changed` events to the agent and four LLM-callable smart-home tools (list/get/call) gated by a Long-Lived Access Token, with blocked-domain + entity-ID-pattern security and persistent-notification replies. |
| 5 | `hermes_open_webui_integration.md` | procedure | open-webui §Architecture (+runtime-location callout), §Quick Setup (bootstrap script + 5 manual steps), §Docker Compose, §Configuring via Admin UI, §API Type (chat-completions vs responses), §How It Works, §Configuration Reference, §Troubleshooting, §Multi-User with Profiles, §Linux Docker | ~1100 | Use Open WebUI as a polished web frontend for Hermes via its built-in OpenAI-compatible API server: enable `API_SERVER_*`, point Open WebUI's `OPENAI_API_BASE_URL` at `:8642/v1`, chat-completions vs experimental Responses mode, inline tool-progress streaming, per-profile multi-user agents on distinct ports, Docker host-networking caveats. |
| 6 | `hermes_webhooks_routes_security.md` | model | webhooks §intro, §Configuring Routes (properties table, full example, prompt templates, forum-topic, `{__raw__}`), §Delivery Options (17-target table), §Security (HMAC validation, secret-required, rate limiting, idempotency, body-size, prompt-injection) | ~1300 | The webhook adapter's route + security model: named routes under `platforms.webhook.extra.routes` with `events`/`secret`/`prompt`/`skills`/`deliver`/`deliver_extra`/`deliver_only`, dot-notation prompt templates + `{__raw__}`, the cross-platform delivery target matrix, and the per-source HMAC validation / required-secret / 30-rpm rate-limit / 1-hr idempotency / 1MB body-size / prompt-injection security layers. |
| 7 | `hermes_webhooks_routing_delivery.md` | procedure | webhooks §Quick Start, §Setup (wizard/env, verify), §GitHub PR Review step-by-step, §GitLab Webhook Setup, §Direct Delivery Mode (when to use, benefits, examples, response codes, gotchas), §Dynamic Subscriptions (CLI subscribe/list/remove/test, hot-reload, agent-driven), §Troubleshooting, §Environment Variables | ~1450 | Operating the webhook adapter: enable via wizard/`WEBHOOK_*` env + `/health` verify, the GitHub-PR-review and GitLab-MR walkthroughs (incl. `gh` auth + `X-Gitlab-Token`), `deliver_only` zero-LLM direct delivery, `hermes webhook subscribe/list/remove/test` dynamic subscriptions hot-reloaded from `webhook_subscriptions.json`, status-code semantics, troubleshooting. |
| 8 | `hermes_msgraph_webhook_listener.md` | procedure | msgraph-webhook §intro, §Prerequisites, §Quick Start (config.yaml/env, endpoints), §Configuration (settings table), §Security Hardening (clientState, source-IP CIDR, HTTPS termination, response hygiene, status codes), §Troubleshooting, §Related Docs | ~900 | The `msgraph_webhook` inbound listener for Microsoft Graph change notifications (Teams-meeting transcripts, chat, calendar): `clientState` timing-safe auth, `accepted_resources` allowlist, the validation-handshake / notification endpoints, source-IP CIDR allowlisting for non-loopback binds, TLS-at-the-proxy, and the 202/200/403/400 status model. |
| 9 | `hermes_messaging_raft.md` | procedure | raft §intro (Division of Labor), §Prerequisites, §Setup, §How It Works (content-free wake contract), §Bridge, §Environment Variables | ~480 | Connect Hermes to Raft as an external agent via a local wake-channel bridge: setting `RAFT_PROFILE` auto-enables the adapter, which spawns the `raft agent bridge` child process and opens a loopback `POST /wake` endpoint authed by a per-session shared token; the bridge consumes SSE wake-hints (dedup/backoff/at-least-once), the adapter injects a content-free wake notice into the gateway session, and the agent reads/replies via the Raft CLI (`raft message check`/`send`) — the adapter holds no Raft credentials and never touches message bodies. |

**SP12b totals:** 9 notes · procedure 8 · model 1 · concept 0 (concepts owned by SP11a/SP09 term notes).
8 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 8 · model 1 · concept 0 (gateway/webhook concepts are SP11a-owned terms).
- Source: 8 digested pages (~10.2K words) → ~8.9K words of notes (modest compression via link-outs to SP11a gateway core + SP09 API-server + SP16/17 guides).
- BB mix: procedure 89%, model 11%.

## Section Coverage Map

```
simplex.md (738w) ── ALL sections ───────────────────────── → Note 1 (gateway core/pairing→SP11a)
bluebubbles.md (833w) ── ALL sections ───────────────────── → Note 2 (mention-gating shared w/ Photon Note 3; gateway core→SP11a)
photon.md (1123w) ── ALL sections ───────────────────────── → Note 3 (credential_pool→SP09; mention-gating model→Note 2)
homeassistant.md (1227w)
├── Setup (token / env / start) ───────────────────────── → Note 4
├── Available Tools (4 ha_* tools) ─────────────────────── → Note 4 (tool surface→SP05/SP08b features)
├── Gateway Platform real-time events (filter/format/resp/conn) → Note 4 (gateway core→SP11a)
├── Security (blocked domains, entity-ID validation) ───── → Note 4
└── Example Automations / Troubleshooting ──────────────── → Note 4
open-webui.md (1898w) ── ALL sections ───────────────────── → Note 5 (API-server feature→SP09; profiles→SP04; Docker→SP03)
webhooks.md (2756w)
├── intro / Configuring Routes (props / example / templates / forum-topic / __raw__) → Note 6 (model)
├── Delivery Options (17-target table) ─────────────────── → Note 6
├── Security (HMAC / secret-required / rate-limit / idempotency / body-size / prompt-injection) → Note 6 (sandboxing→SP03)
├── Quick Start / Setup (wizard/env/verify) ────────────── → Note 7
├── GitHub PR Review (step by step) / GitLab Webhook Setup → Note 7 (PR-review guide→SP16)
├── Direct Delivery Mode (deliver_only, codes, gotchas) ── → Note 7
├── Dynamic Subscriptions (CLI subscribe/list/remove/test, hot-reload, agent-driven) → Note 7
└── Troubleshooting / Environment Variables ────────────── → Note 7
msgraph-webhook.md (1094w) ── ALL sections ──────────────── → Note 8 (app-registration guide→SP17; teams bot→SP11b; teams pipeline→SP17)
raft.md (480w) ── ALL sections (intro/Division of Labor, Prerequisites, Setup, How It Works, Bridge, Environment Variables) → Note 9 (hermes_messaging_raft.md) (gateway session-inject/pairing→SP11a; child-process supervisor model shared w/ Photon Note 3)
```

No source H2/H3 orphaned. All 8 pages fully covered; gateway-core / feature-page / guide detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| webhooks.md (2756w, 17 code) | Note 6 (`hermes_webhooks_routes_security`, model) + Note 7 (`hermes_webhooks_routing_delivery`, procedure) | >2500w AND mixed BB: a route/delivery/security data-model (route-property table, 17-target delivery matrix, HMAC/rate-limit/idempotency model) vs the procedural setup/GitHub/GitLab/direct-delivery/dynamic-subscription workflow. Each half ≤6 curated code blocks. |

All other pages are single-BB and ≤2500w → 1 note each (no further splits).

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_photon_imessage` | `term_photon.md` (active — Amazon Unit-of-Work / Paragon / HITL investigation automation) | **NOT a dup** — unrelated concept (LIKE false-positive, master caution list) | CREATE; do NOT link `term_photon`. |
| `hermes_messaging_simplex` | `term_simplex_method.md` (active — linear-programming simplex algorithm) | **NOT a dup** — unrelated optimization concept | CREATE; do NOT link `term_simplex_method`. |
| `hermes_webhooks_routes_security`, `hermes_webhooks_routing_delivery`, `hermes_msgraph_webhook_listener`, `hermes_open_webui_integration` | `term_api_gateway.md`, `term_reverse_proxy.md`, `term_event_driven_architecture.md` (all active) | **NOT a dup** — generic patterns these notes USE; no doc/term note covers Hermes' concrete webhook/MS-Graph/Open-WebUI adapters | CREATE; LINK the generic patterns as related. |
| `hermes_messaging_bluebubbles_imessage`, `hermes_messaging_homeassistant` | no substantive same-concept term/doc note; `snippet_hermes_agent_gw_platform_homeassistant`/`skills_apple_imessage` are the implementation layer (linked, not dup) | NEW | CREATE; LINK the snippets. |


## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19** (master directive — supersedes every prior floor): each note's
> `## Related Notes` carries **FOUR COUNTED groups**, all relevancy-selected to that note's actual content
> and each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   Hermes SOURCE-CODE modules that implement what this doc note documents; relevance clause names the
>   module/role).
>   implementation corpus this note's documented code lives in). **The snippet group is NOW A COUNTED FLOOR,
>   raised from the prior ≥8 and promoted from its earlier "bonus" status** — no longer a bonus group.
> - **≥10 documentation notes** (sibling `hermes_*` in this series [allowed un-verified — created later,
>
> Relevancy first, never pad. The previous floor was ≥8 term + ≥8 snippet + ≥5 doc (with snippets later
> demoted to bonus in a partial run); this levelling-up keeps every existing relevant cross-ref and raises
> snippet→≥10 (counted) and doc→≥10.
>
> 2026-06-19; terms + snippets originally queried 2026-06-15). The 13 `repo_hermes_agent_*` notes are all
> allowed un-verified (they are created later in this same series).
> Hermes-specific terms owned by other SPs (`term_messaging_gateway`/`term_dm_pairing`/`term_silence_token`
> [own] in (+fin …), EXCLUDED from the ≥8 term floor.
>
> Relative paths from `resources/documentation/hermes_agent/`: terms `../../term_dictionary/`, code-repos
> `../../../areas/code_repos/`, snippets `../../code_snippets/`, `cc_*` docs `../claude_code/`, sibling docs
> `hermes_*.md` (same folder).

**Note 1 `hermes_messaging_simplex`**
- Terms (8): term_encryption, term_websocket, term_authentication, term_access_control, term_autonomous_coding_agents, term_agent_harness, term_cron, term_pii — relevance: SimpleX is E2E-encrypted over a local WebSocket daemon, with allowlist/DM-pairing access control, opaque-ID privacy (no PII), and cron delivery to the home channel. (+fin: term_messaging_gateway [own], term_dm_pairing [own], term_silence_token [own])
- Code-Repos (5): repo_hermes_agent_plugins — the plugin SDK package that houses the `plugins_platform_simplex` SimpleX adapter this page installs/configures; repo_hermes_agent_gateway_messaging — the gateway runner that pairs, ACL-gates, normalizes and delivers SimpleX messages; repo_hermes_agent_cron — the cron-job scheduler that delivers to `SIMPLEX_HOME_CHANNEL` (the page's cron example); repo_hermes_agent_cli — the `hermes gateway setup` / `hermes pairing approve simplex` CLI the setup walkthrough drives; repo_hermes_agent — the umbrella package the SimpleX channel ships within.
- Snippets (10): plugins_platform_simplex, gw_pairing, gw_runner_acl, gw_delivery, gw_platform_base_normalize, gw_platform_base_outbound, gw_runner_session_key, gw_runner_router, gw_runner_cron, tools_send_attach — relevance: the SimpleX adapter, DM-pairing handshake, ACL allowlist gate, outbound XFTP delivery, message normalization, the base outbound path, per-contact session-keying, the runner that routes inbound events, the cron-delivery runner targeting the home channel, and the attachment-send path for SimpleX media.
- Docs (10): hermes_messaging_bluebubbles_imessage, hermes_photon_imessage, hermes_messaging_homeassistant, hermes_webhooks_routing_delivery, hermes_msgraph_webhook_listener (sibling hermes_* — the other consumer/webhook platform setup docs in this series); cc_channels_setup — analogous "connect an agent to a messaging channel" setup walkthrough; cc_channels_overview — the channels model (platform↔agent bridge) SimpleX is one instance of; cc_authentication — agent-channel auth/allowlist analogue to SimpleX's allowed-users gate; cc_routine_triggers — scheduled-trigger analogue to the SimpleX cron-delivery example; cc_what_claude_can_access — privacy/data-access posture analogous to SimpleX's local-only, no-PII transport.

**Note 2 `hermes_messaging_bluebubbles_imessage`**
- Terms (8): term_authentication, term_access_control, term_websocket, term_autonomous_coding_agents, term_agent_harness, term_multimodal, term_persona, term_session_persistence — relevance: BlueBubbles uses webhook-push + REST, DM-pairing/allowlist auth, mention-gating (persona wake words), rich media (multimodal), and per-chat session tracking. (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — houses the `gw_platform_bluebubbles` adapter, pairing/ACL, the webhook-push listener and REST outbound this page wires up; repo_hermes_agent_skills — the `skills_apple_imessage` skill the page's tapback/typing/read-receipt media features exercise; repo_hermes_agent_tools — the `tools_send_attach` attachment-send path BlueBubbles rich media uses; repo_hermes_agent_cli — the `hermes gateway setup` / `hermes pairing approve bluebubbles` / `hermes logs gateway` CLI in the setup steps; repo_hermes_agent — the umbrella package the BlueBubbles channel ships within.
- Snippets (10): gw_platform_bluebubbles, gw_pairing, gw_runner_acl, gw_delivery, gw_platform_base_outbound, gw_platform_base_normalize, tools_send_attach, skills_apple_imessage, gw_runner_session_key, gw_status_health — relevance: the BlueBubbles adapter, pairing/ACL gate, outbound REST + attachment send, base outbound + normalization, the iMessage skill, the per-chat session-key the webhook events map to, and the readiness probe the gateway connection check uses.
- Docs (10): hermes_photon_imessage, hermes_messaging_simplex, hermes_messaging_homeassistant, hermes_webhooks_routing_delivery, hermes_open_webui_integration (sibling hermes_* — iMessage-via-Photon counterpart + the rest of this series); cc_channels_setup — analogous channel setup walkthrough; cc_channels_overview — channels model the BlueBubbles bridge is an instance of; cc_authentication — channel auth/allowlist analogue to BlueBubbles DM-pairing; cc_channel_reply_tool — agent-reply-into-a-channel analogue to BlueBubbles outbound REST; cc_channel_permission_relay — who-may-talk-to-the-agent gating analogue to BlueBubbles allowed-users.

**Note 3 `hermes_photon_imessage`**
- Terms (8): term_grpc, term_authentication, term_access_control, term_oauth_token, term_autonomous_coding_agents, term_agent_harness, term_multimodal, term_persona — relevance: Photon holds a long-lived gRPC stream via a Node sidecar, device-code (OAuth-style) login, DM-pairing/allowlist auth, mention-gating, and outbound multimodal attachments. (+fin: term_credential_pool [own], term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the Photon gateway adapter that supervises the `spectrum-ts` Node sidecar over loopback, pairs/ACL-gates and delivers; repo_hermes_agent_agent_core — the credential-pool / credential-sources core that stores the Photon device token + project secret in `auth.json`/`.env`; repo_hermes_agent_cli — the `hermes photon setup`/`status`/`install-sidecar` + `hermes pairing approve photon` CLI the first-time-setup flow drives; repo_hermes_agent_tools — the `tools_send_attach` outbound-attachment path Photon's `/send-attachment` sidecar endpoint uses; repo_hermes_agent — the umbrella package the Photon channel + sidecar ship within.
- Snippets (10): gw_pairing, gw_runner_acl, gw_delivery, gw_platform_base_outbound, gw_platform_base_normalize, gw_runner_session_key, core_credential_sources, core_credential_pool_selection, tools_send_attach, gw_runner_supervisor — relevance: the pairing/ACL gate, outbound delivery + base outbound, normalization, per-conversation session-keying, the credential-source + credential-pool-selection code the setup writes Photon creds into, the attachment-send path, and the runner supervisor that spawns/supervises the Node sidecar child process.
- Docs (10): hermes_messaging_bluebubbles_imessage, hermes_messaging_simplex, hermes_messaging_raft, hermes_webhooks_routing_delivery, hermes_msgraph_webhook_listener (sibling hermes_* — the other iMessage path BlueBubbles, the other sidecar/child-process bridge Raft, and the rest of this series); cc_channels_setup — analogous managed-channel setup walkthrough; cc_authentication — device-code/OAuth-style login analogue to Photon's `client_id=photon-cli` device login; cc_channel_permission_relay — allowlist/pairing gating analogue to Photon allowed-users; cc_background_session_hosting — managed-runtime/hosted-line analogue to Photon's managed line pool; cc_sdk_isolation_technologies — supervised-subprocess isolation analogue to the supervised Node sidecar.

**Note 4 `hermes_messaging_homeassistant`**
- Terms (8): term_websocket, term_function_calling, term_authentication, term_access_control, term_event_driven_architecture, term_autonomous_coding_agents, term_agent_harness, term_prompt_injection — relevance: HA connects via WebSocket event subscription, exposes 4 LLM-callable (function-calling) device tools authed by a long-lived token, and validates entity IDs + blocks code-exec domains against injection. (+fin: term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gw_platform_homeassistant` WebSocket gateway adapter that subscribes to `state_changed`, filters/formats and delivers persistent-notification replies; repo_hermes_agent_tools — the four `ha_*` smart-home tools registered in the tool registry and dispatched on call; repo_hermes_agent_skills — the `skills_smart_home` skill that drives the HA device tools; repo_hermes_agent_agent_core — the function-calling agent loop that selects/invokes the four `ha_*` tools; repo_hermes_agent — the umbrella package the HA integration ships within.
- Snippets (10): gw_platform_homeassistant, gw_runner_router, gw_delivery, gw_platform_base_normalize, tools_registry, tools_send_dispatch, gw_runner_acl, gw_status_health, skills_smart_home, gw_session_context — relevance: the HA gateway adapter, the inbound-event router, event delivery, normalization, the four-tool registration surface + tool dispatch, the always-authorized ACL path, the readiness probe, the smart-home skill, and the session-context the forwarded HA events are injected into.
- Docs (10): hermes_open_webui_integration, hermes_messaging_bluebubbles_imessage, hermes_photon_imessage, hermes_webhooks_routes_security, hermes_msgraph_webhook_listener (sibling hermes_* — other tool-surfacing/event-driven integration docs in this series); cc_built_in_tools — analogous catalog of LLM-callable built-in tools to the four `ha_*` tools; cc_tools_catalog — the tool-surface reference analogue; cc_computer_use — device-control-via-tool analogue to HA `ha_call_service`; cc_prompt_injection_defenses — injection-defense analogue to HA's blocked-domain + entity-ID validation; cc_channels_overview — the platform/channel model the HA gateway platform is an instance of.

**Note 5 `hermes_open_webui_integration`**
- Terms (8): term_openai_responses_api, term_converse_api, term_reverse_proxy, term_authentication, term_function_calling, term_autonomous_coding_agents, term_agent_harness, term_docker — relevance: Open WebUI talks OpenAI chat-completions/Responses to Hermes' API-server runtime (a reverse-proxy-fronted agent), bearer-key auth, inline tool-progress (function calls), run in Docker. (+fin: term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — houses the API-server gateway platform (`gw_platform_api_server_*`) that exposes `/v1/chat/completions`+`/v1/responses` and streams SSE to Open WebUI; repo_hermes_agent_agent_core — the server-side `AIAgent` init + api-mode resolution + conversation-loop api-dispatch that runs each request; repo_hermes_agent_tools — the terminal/file/web tools that run on the API-server host and stream inline tool-progress; repo_hermes_agent_cli — the `hermes config set API_SERVER_*` / `hermes gateway` / `hermes profile create` CLI the setup uses; repo_hermes_agent — the umbrella package whose built-in API server Open WebUI fronts.
- Snippets (10): gw_platform_api_server_connect, gw_platform_api_server_routes, gw_platform_api_server_middleware, core_agent_init_api_mode_resolution, core_conversation_loop_api_dispatch, gw_stream_consumer, gw_runner_init, gw_status_health, gw_stream_batching, gw_runtime_footer — relevance: the API-server connect/routes/auth-middleware, server-side AIAgent init + api-mode resolution + api-dispatch, the SSE stream consumer + batching that emits chat-completions/Responses chunks, the runner init, the `/health` probe Open WebUI's verify step hits, and the runtime footer/status.
- Docs (10): hermes_messaging_homeassistant, hermes_webhooks_routing_delivery, hermes_msgraph_webhook_listener, hermes_messaging_bluebubbles_imessage, hermes_photon_imessage (sibling hermes_* — the other HTTP-serving/integration docs in this series); cc_llm_gateway — analogous OpenAI-compatible gateway-in-front-of-an-agent pattern; cc_llm_gateway_litellm — concrete OpenAI-compatible proxy analogue to pointing Open WebUI at `:8642/v1`; cc_proxy_and_gateway_config — base-URL/key proxy config analogue to `OPENAI_API_BASE_URL`/`OPENAI_API_KEY`; cc_sdk_stream_text_and_tool_calls — streamed text + tool-call events analogue to the inline tool-progress + Responses `function_call` stream; cc_authentication — bearer-key auth analogue to `API_SERVER_KEY`.

**Note 6 `hermes_webhooks_routes_security`** (model)
- Terms (8): term_event_driven_architecture, term_api_gateway, term_idempotency, term_rate_limiting, term_prompt_injection, term_authentication, term_secure_delivery, term_access_control — relevance: the model is an event-driven HTTP gateway with HMAC auth, fixed-window rate limiting, 1-hr idempotency, prompt-injection-aware sandboxing guidance, and a cross-platform secure-delivery target matrix. (+fin: term_messaging_gateway [own], term_credential_pool [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gw_platform_webhook` adapter + delivery dispatcher + channel directory that implements routes, HMAC validation, rate-limit, idempotency and the 17-target delivery matrix; repo_hermes_agent_skills — the `skills` field's loadable skill names (e.g. github-code-review) the route model references; repo_hermes_agent_tools — the code-exec/sandbox terminal backends the prompt-injection guidance recommends isolating with; repo_hermes_agent_cli — the `hermes gateway setup` wizard that writes the route/secret config this model defines; repo_hermes_agent — the umbrella package the webhook adapter ships within.
- Snippets (10): gw_platform_webhook, gw_delivery, gw_channel_directory, gw_config_per_channel, gw_config_schema, gw_runner_outbound, gw_platform_base_outbound, gw_runner_acl, gw_config_load, skills_devops_webhook — relevance: the webhook adapter, the delivery dispatcher + channel directory the 17-target matrix routes through, the per-channel route config schema + config loader that parses `platforms.webhook.extra.routes`, the outbound/base-outbound + ACL paths, and the webhook-subscriptions skill the `skills` field loads.
- Docs (10): hermes_webhooks_routing_delivery, hermes_msgraph_webhook_listener, hermes_open_webui_integration, hermes_messaging_homeassistant, hermes_messaging_bluebubbles_imessage (sibling hermes_* — the operating-procedure half of this split + the other HTTP-listener/delivery docs); cc_github_actions — analogous event-driven CI trigger model to GitHub webhook routes; cc_gitlab_ci_cd — GitLab event-trigger analogue to the GitLab-token route auth; cc_prompt_injection_defenses — injection-defense model analogue to the attacker-controlled-payload warning; cc_sandbox_modes — sandboxed-execution analogue to the Docker/SSH isolation guidance; cc_security_architecture — defense-in-depth model analogue to the HMAC/rate-limit/idempotency/body-size layers.

**Note 7 `hermes_webhooks_routing_delivery`**
- Terms (8): term_event_driven_architecture, term_idempotency, term_api_gateway, term_secure_delivery, term_authentication, term_cron, term_autonomous_coding_agents, term_message_queue — relevance: operating the adapter is event-driven HTTP ingestion → idempotent agent runs or `deliver_only` push to a delivery target (queue-like), GitHub/GitLab auth, and agent/cron-driven dynamic subscriptions. (+fin: term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gw_platform_webhook` adapter that ingests POSTs, runs/skips the agent, and dispatches `deliver_only` direct delivery + the GitHub/GitLab walkthroughs; repo_hermes_agent_cli — the `hermes webhook subscribe/list/remove/test` + `hermes gateway setup`/`run` CLI the dynamic-subscription + setup flows drive; repo_hermes_agent_skills — the `skills_github`/`skills_devops_webhook` skills the GitHub-PR-review route + agent-driven subscriptions load; repo_hermes_agent_cron — the cron-job-completion → direct-delivery use case the page lists; repo_hermes_agent — the umbrella package the webhook adapter + CLI ship within.
- Snippets (10): gw_platform_webhook, gw_delivery, gw_channel_directory, gw_config_per_channel, gw_runner_outbound, gw_status_health, gw_pairing, gw_platform_base_outbound, skills_github, skills_devops_webhook — relevance: the webhook adapter, delivery dispatcher + channel directory, the route config the subscriptions hot-reload, outbound dispatch, the `/health` probe the verify step hits, the base outbound path, and the GitHub + webhook-subscriptions skills the PR-review route + agent-driven `subscribe` flow exercise.
- Docs (10): hermes_webhooks_routes_security, hermes_msgraph_webhook_listener, hermes_open_webui_integration, hermes_messaging_homeassistant, hermes_messaging_simplex (sibling hermes_* — the route/security-model half of this split + the other listener/integration docs); cc_github_actions — analogous GitHub-event-triggered agent run to the GitHub-PR-review walkthrough; cc_gitlab_ci_cd — GitLab-event-trigger analogue to the GitLab-MR setup; cc_code_review — automated-PR-review analogue to the github-code-review route; cc_pr_attribution — agent-posts-a-PR-comment analogue to `github_comment` delivery; cc_routine_triggers — scheduled/event-driven trigger analogue to dynamic webhook subscriptions.

**Note 8 `hermes_msgraph_webhook_listener`**
- Terms (8): term_event_driven_architecture, term_api_gateway, term_idempotency, term_authentication, term_access_control, term_oauth_token, term_reverse_proxy, term_autonomous_coding_agents — relevance: the listener is an event-driven HTTP endpoint with `clientState` timing-safe auth, dedupe (idempotency), source-IP allowlisting, OAuth-app (Graph) credentials, and TLS terminated at a reverse proxy. (+fin: term_messaging_gateway [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the `gw_platform_msgraph_webhook` inbound listener that validates `clientState`, dedupes, source-IP-allowlists and runs the validation handshake; repo_hermes_agent_mcp_toolsets — the Microsoft-Graph toolset (`tools_msgraph`) the meeting-transcript/chat consumers call; repo_hermes_agent_plugins — the Teams meeting-summary pipeline plugin (`plugins_teams_pipeline`) that is the listener's primary consumer; repo_hermes_agent_cli — the `hermes gateway run` + `hermes teams-pipeline subscribe --client-state` CLI the setup/troubleshooting references; repo_hermes_agent — the umbrella package the msgraph_webhook adapter ships within.
- Snippets (10): gw_platform_msgraph_webhook, tools_msgraph, gw_delivery, gw_runner_outbound, gw_config_schema, gw_runner_acl, gw_status_health, gw_platform_base_outbound, plugins_teams_pipeline, plugins_platform_teams — relevance: the MS-Graph webhook adapter, the Graph tool surface that fetches transcripts, delivery/outbound, the route config schema the `extra.*` settings map to, the source-IP ACL gate, the `/health` probe with accepted/duplicate counters, the base outbound path, the Teams meeting-summary pipeline (primary consumer), and the Teams chat platform the summary posts back into.
- Docs (10): hermes_webhooks_routes_security, hermes_webhooks_routing_delivery, hermes_open_webui_integration, hermes_messaging_homeassistant, hermes_messaging_bluebubbles_imessage (sibling hermes_* — the generic-webhook security/operating docs + the other HTTP-listener integrations); cc_authentication — shared-secret/`clientState` auth analogue; cc_network_tls_and_access — TLS-at-the-proxy + network-access analogue to terminate-TLS-at-reverse-proxy + source-IP allowlist; cc_cloud_network_access — egress/ingress allowlisting analogue to the Microsoft source-IP CIDR allowlist; cc_mcp_authentication — OAuth-app credential analogue to the Graph application credentials; cc_security_architecture — defense-in-depth analogue to the clientState + source-IP + TLS + response-hygiene layers.

**Note 9 `hermes_messaging_raft`** (re-sync 2026-06-19)
- Terms (8): term_event_driven_architecture, term_message_queue, term_idempotency, term_authentication, term_access_control, term_session_persistence, term_autonomous_coding_agents, term_agent_harness — relevance: Raft is an event-driven bridge that consumes SSE wake-hints and POSTs each to a loopback `/wake` (event-driven), the bridge owns dedup/backoff/at-least-once (queue + idempotency semantics), the adapter authenticates the bridge with a per-session shared token over localhost (authentication) and content-shape-rejects payloads (access control), injects a notice into the per-session pipeline (session persistence), and wakes the autonomous agent harness to pull/reply via the Raft CLI. (+fin: term_messaging_gateway [own], term_dm_pairing [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — the Raft adapter that owns the loopback `/wake` endpoint, validates the bridge token, content-shape-rejects payloads and injects the wake notice into the gateway session; repo_hermes_agent_cli — the `raft agent bridge` child process the adapter spawns + the `raft message check/send` CLI the agent uses; repo_hermes_agent_agent_core — the per-session pipeline + agent harness the content-free wake notice is injected into and wakes; repo_hermes_agent_providers_adapters — the external-agent integration layer Raft plugs into as a wake-channel adapter; repo_hermes_agent — the umbrella package the Raft adapter + bridge supervision ship within.
- Snippets (10): gw_runner_supervisor, gw_pairing, gw_runner_acl, gw_delivery, gw_runner_session_key, gw_session_context, gw_platform_signal_sse, gw_runner_router, gw_session_lifecycle, gw_status_health — relevance: the runner supervisor that spawns/terminates the `raft agent bridge` child process, the pairing/ACL gate the wake notice passes, outbound delivery, the per-session token/session-key the loopback endpoint validates, the session-context + session-lifecycle the wake notice is injected into, the SSE-consumption pattern (signal adapter analogue) the bridge uses, the runner router that routes the wake into the agent, and the `/health` readiness probe.
- Docs (10): hermes_photon_imessage, hermes_messaging_simplex, hermes_messaging_bluebubbles_imessage, hermes_messaging_homeassistant, hermes_msgraph_webhook_listener (sibling hermes_* — the other sidecar/child-process bridge Photon + the SSE/event-driven listener docs in this series); cc_dispatch_background_agents — analogous wake/dispatch-an-agent-on-an-event model; cc_background_session_hosting — background/hosted-agent-session analogue to the wake-channel-driven session; cc_routine_triggers — external-event-trigger analogue to the SSE wake-hints; cc_remote_control — external-system-controls-the-agent analogue to Raft waking Hermes; cc_sdk_isolation_technologies — supervised-child-process isolation analogue to the spawned `raft agent bridge`.


## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 8 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 simplex | procedure | 750 | ≤6 (from 7 short cmd/env blocks) | ✓ |
| 2 bluebubbles-imessage | procedure | 850 | ≤6 (from 9; curate env + require_mention YAML) | ✓ |
| 3 photon-imessage | procedure | 1050 | ≤6 (from 11; one canonical setup + status + env block) | ✓ |
| 4 homeassistant | procedure | 1150 | ≤6 (from 12; curate config YAML + ha_call_service examples) | ✓ |
| 5 open-webui | procedure | 1100 | ≤6 (from 16; curate enable + docker run + compose + verify) | ✓ |
| 6 webhooks-routes-security | model | 1300 | ≤6 (from webhooks route example + delivery/security YAML) | ✓ |
| 7 webhooks-routing-delivery | procedure | 1450 | ≤6 (from webhooks setup/github/gitlab/subscribe blocks) | ✓ |
| 8 msgraph-webhook-listener | procedure | 900 | ≤6 (from 5; config + hardening YAML) | ✓ |
| 9 messaging-raft | procedure | 480 | 2 (RAFT_PROFILE env + How-It-Works flow diagram) | ✓ |

No further splits needed — all 9 notes ≤2500w. The only over-cap source page (webhooks 2756w/17 code) is the
planned 2-way split; each half is ≤1450w and curated to ≤6 load-bearing blocks (kept blocks verbatim, the
rest summarized in prose). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP12b)

**SP12b owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes-specific
gateway/messaging concept SP12b touches is owned by another sub-plan (link at finalization) or is an existing
verified term. Augment re-read surfaced **0 new** undigested terms that SP12b should own.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_messaging_gateway`, `term_dm_pairing`, `term_silence_token` | LINK only (forward-ref, +fin [own]) | SP11a | platform↔agent bridge, pairing handshake, `[SILENT]` non-reply — gateway-core concepts owned by SP11a; SP12b's platform pages USE them. |
| `term_credential_pool` (rotation) | LINK only (+fin [own]) | SP09 | Photon/webhook credentials live in the pool; concept home is SP09 credential-pools. |

### Renamed (general → specific)

— (audit performed; SP12b owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the rejected `term_webhook_route` candidate — see Removed below — and to the master's forward-ref
slugs SP12b links; all forward-refs are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_webhook_route` | none substantive — rejected on specificity (Hermes-config-specific, not reusable) + reusable layer covered by `term_event_driven_architecture` (active) + `term_api_gateway` (active) | Not captured — concept documented in the `hermes_webhooks_routes_security` doc note; link the two generic terms instead. |
| `term_photon` (would collide) | `term_photon.md` (active — Amazon investigation-automation Photon / UoW / Paragon) | Not captured — LIKE false-positive, UNRELATED concept; the doc note `hermes_photon_imessage` created instead; do NOT link `term_photon`. |
| `term_simplex` (would collide) | `term_simplex_method.md` (active — LP simplex algorithm) | Not captured — UNRELATED; doc note `hermes_messaging_simplex` created instead; do NOT link `term_simplex_method`. |

## Term-Note Authoring Requirements

N/A (inherited) — SP12b owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP11a/SP09). The full Term-Note Authoring
fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12, backlink expansion,
>200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (consumer/private messengers + external-agent bridge, pilot):** Notes 1, 2, 3, 9. Pilot Note 1
  (`hermes_messaging_simplex`) first → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
  (Note 9 `hermes_messaging_raft` added in the 2026-06-19 re-sync — small wake-channel-bridge procedure.)
- **Phase 2 (smart-home + web frontend):** Notes 4, 5. GATE G1–G8.
- **Phase 3 (webhooks + MS-Graph):** Notes 6, 7, 8. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for
kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every
ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

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
# G8: in-degree ≥1 from outside the folder
for n in hermes_messaging_simplex hermes_messaging_bluebubbles_imessage hermes_photon_imessage hermes_messaging_homeassistant hermes_open_webui_integration hermes_webhooks_routes_security hermes_webhooks_routing_delivery hermes_msgraph_webhook_listener hermes_messaging_raft; do
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note
series) under a "Messaging: Consumer & Webhooks" section (shared with SP12a). Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP12b does NOT create a separate entry point — the
>30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_messaging_simplex`, `hermes_messaging_bluebubbles_imessage`, `hermes_photon_imessage`, `hermes_messaging_homeassistant`, `hermes_webhooks_routes_security`, `hermes_webhooks_routing_delivery`, `hermes_msgraph_webhook_listener`, `hermes_messaging_raft` | gateway/messaging repo ↔ platform usage docs |
| `snippet_hermes_agent_gw_runner_supervisor.md` | → `hermes_messaging_raft` | runner-supervisor (child-process spawn) code ↔ the Raft bridge it spawns |
| `repo_hermes_agent.md` | → `hermes_open_webui_integration` | implementation ↔ API-server frontend usage |
| `snippet_hermes_agent_gw_platform_homeassistant.md` | → `hermes_messaging_homeassistant` | HA adapter code ↔ HA usage doc |
| `snippet_hermes_agent_gw_platform_webhook.md` | → `hermes_webhooks_routes_security`, `hermes_webhooks_routing_delivery` | webhook adapter code ↔ webhook usage docs |
| `snippet_hermes_agent_gw_platform_msgraph_webhook.md` | → `hermes_msgraph_webhook_listener` | MS-Graph adapter code ↔ usage doc |
| `snippet_hermes_agent_gw_platform_bluebubbles.md` | → `hermes_messaging_bluebubbles_imessage` | BlueBubbles adapter code ↔ usage doc |
| `snippet_hermes_agent_plugins_platform_simplex.md` | → `hermes_messaging_simplex` | SimpleX adapter code ↔ usage doc |
| `snippet_hermes_agent_gw_platform_api_server_routes.md` | → `hermes_open_webui_integration` | API-server routes code ↔ Open WebUI doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_webhooks_routes_security`, `hermes_messaging_homeassistant`, `hermes_messaging_raft` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_messaging_simplex`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note —
do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes to ≤6 load-bearing
blocks, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If
multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP12b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 rows to the
  master-created entry point (shared "Messaging: Consumer & Webhooks" section with SP12a); backfill the
  `repo_hermes_agent_gateway_messaging.md` / `gw_platform_*` snippet inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After SP11a lands: backfill the `term_messaging_gateway`/`term_dm_pairing`/`term_silence_token` forward-refs
  into Notes 1-9 (currently +fin [own]); after SP09 lands, backfill `term_credential_pool` into Notes 3/6.
- Cross-link the webhook docs (Notes 6/7) from the SP16 GitHub-PR-review guide and the SP17 MS-Graph
  app-registration guide once those SPs land — bidirectional doc↔guide links.

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  docs raised to ≥10 (≥5 sibling `hermes_*` + ≥5 `cc_*` analogues). Re-read all 8 source pages from
  `inbox/hermes_agent_docs/` to ground every new relevance clause; no existing relevant cross-ref dropped.
- Sections added/updated: Collision&Dedup Audit (2 LIKE false-positives confirmed by reading note
  YAML/keywords — investigation-automation `term_photon`, LP `term_simplex_method`; 1 rejected term candidate
  `term_webhook_route`), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc,
  confirmed), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured; **1 split** (webhooks→2 by >2500w + mixed BB); all 9 notes ≤2500w;
  code-heavy notes curated to ≤6 blocks.
- Collision audit: **0 removals from a term-capture list** (SP12b owns 0 captures); `term_photon` and
  `term_simplex_method` are LINK-NOT-dup false-positives; `term_webhook_route` candidate rejected on
  specificity + reusable-layer coverage; no doc note duplicates an existing term/doc note (0 `hermes_agent/`
  doc notes exist yet).
- Snippet correction at finalization: SimpleX has no `gw_platform_simplex` snippet → replaced inline with the
- Undigested terms surfaced at augment: **0 new** (SP12b owns 0 captures; all concepts SP11a/SP09-owned).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (1 candidate
rejected on specificity; forward-refs scope-qualified) ✓ Slug Collision (2 LIKE false-positives + 1 rejected
candidate, term AND doc) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND
documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items
are N/A-pass (SP12b owns 0 captures); dedup/collision items are substantively PASS (audit performed on all 9
doc notes + the rejected term candidate).

## Review Sign-Off

**Re-reviewed 2026-06-19 (FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).** Independent
review re-verified every cited ID against the DB and re-measured source pages. Term (25 sampled), code-repo
active**; the 4 `[own]` forward-ref terms and the 9 sibling `hermes_*` docs are confirmed NOT-yet-existing
(correctly excluded / resolve at finalization per G5/G8). CP7 spot re-measure: raft ~475w/2c (plan 480/2),
webhooks ~2747w/17c (plan 2756/17), simplex 738w/7c, photon 1123w/11c — all match (ratio ≈1.00). `term_raft`
confirmed non-existent (raft = NEW, not a dup; `term_datacraft` is LIKE noise). No bare links; every group
carries a relevance clause. No stale 3-floor/"bonus" wording outside intentional historical context.

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows under a Messaging: Consumer & Webhooks section, shared w/ SP12a); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 notes ≤30; master holds the corpus-level split; SP12 split into a/b. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | webhooks→2 (>2500w + mixed BB); all 9 notes ≤2500w; code-heavy notes curated ≤6; single-BB platform pages KEPT (cohesive, ≤1150w); raft (480w/2c) is a small single-BB procedure (no split). |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: webhooks 2756, open-webui 1898, homeassistant 1227, photon 1123, msgraph 1094, bluebubbles 833, simplex 738 — measured == plan (ratio 1.00). Re-sync 2026-06-19: raft re-measured 480w/2c (== plan); the other 7 pages unchanged. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP12b owns 0 term captures (gateway/webhook concepts SP11a/SP09-owned); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 notes from repo_*/snippet_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.** (Re-confirmed 2026-06-19 against the FOUR-FLOOR standard — anti-fabrication DB spot-check + source re-measure clean; no link dropped, no floor below threshold.)

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-downloaded from upstream `main` (pin moved
`95715dc` → `c253b07`, byte-identical to upstream). Impact on SP12b:

- **1 NEW rendered page added:** `user-guide/messaging/raft.md` (re-measured **480w / 2 code**, BODY-only
  word count per the ledger convention). It is the Raft external-agent **wake-channel bridge** messaging
  integration — routed to SP12b alongside the other webhook/bridge adapters (webhooks, msgraph-webhook,
  photon, open-webui). BB = **procedure** (platform-setup procedure). Small page → exactly **ONE** planned
  note, no split.
- **New planned note:** `hermes_messaging_raft.md` (Note 9). Section coverage maps all of its H2s
  (Division of Labor intro, Prerequisites, Setup, How It Works, Bridge, Environment Variables) to the single
  note — **no source H2/H3 orphaned**.
- **Note count: 8 → 9** (procedure 7 → 8; model unchanged at 1; concept unchanged at 0). Source pages digested
  7 → 8.
- **All 7 pre-existing pages were re-measured and are UNCHANGED** (webhooks 2756, open-webui 1898,
  homeassistant 1227, photon 1123, msgraph 1094, bluebubbles 833, simplex 738) — measured == plan, ratio 1.00.
- **Cross-ref floor met for Note 9 (FOUR-FLOOR, levelled-up 2026-06-19):** ≥8 term (event_driven_architecture,
  message_queue, idempotency, authentication, access_control, session_persistence, autonomous_coding_agents,
  agent_harness) + ≥5 code-repo (gateway_messaging, cli, agent_core, providers_adapters, repo_hermes_agent) +
  ≥10 snippet (gw_runner_supervisor, gw_pairing, gw_runner_acl, gw_delivery, gw_runner_session_key,
  gw_session_context, gw_platform_signal_sse, gw_runner_router, gw_session_lifecycle, gw_status_health) + ≥10
  doc (5 sibling `hermes_*` + 5 `cc_*`: cc_dispatch_background_agents, cc_background_session_hosting,
  cc_routine_triggers, cc_remote_control, cc_sdk_isolation_technologies) — **all term + code-repo + snippet +
- **Collision/dedup:** Note 9 is **NEW** — no existing term/doc note covers this Hermes-specific wake-channel
  bridge (`term_raft` does NOT exist; "Raft" the consensus algorithm is unrelated; the only LIKE hit was
  `term_datacraft`, noise). Generic patterns it USES (`term_event_driven_architecture`, `term_message_queue`,
  `term_api_gateway`) are LINKED, not duplicated.
- **G8 inbound link:** `repo_hermes_agent_gateway_messaging.md`, `snippet_hermes_agent_gw_runner_supervisor.md`,
  `entry_code_snippets_hermes_agent.md`, and the master-created `entry_hermes_agent_docs.md` hub all point at
  Note 9 (in-degree ≥1 from outside the folder).
- **Plan remains READY** — all gates and the elevated cross-ref floor still satisfied; Note 9 added to
  Execution Phase 1 (consumer/private messengers + external-agent bridge).

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 to FOUR-FLOOR) · Review: **DONE** (2026-06-15, 9/9 READY; **re-reviewed 2026-06-19, 9/9 READY @ FOUR-FLOOR**) · Execute: pending · Re-synced 2026-06-19 (+1 note)

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/{simplex,bluebubbles,photon,homeassistant,open-webui,webhooks,msgraph-webhook,raft}.md`
**Last Updated**: 2026-06-15 (revised 2026-06-19, mirror c253b07 — +1 note from re-sync)
**Status**: Ready (augmented + reviewed)
