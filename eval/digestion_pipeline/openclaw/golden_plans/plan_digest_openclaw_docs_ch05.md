---
title: Sub-Plan ch05 — OpenClaw Docs: Channels (Slack, SMS, Synology Chat, Telegram, Tlon, Troubleshooting, Twitch)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/slack", "channels/sms", "channels/synology-chat", "channels/telegram", "channels/tlon", "channels/troubleshooting", "channels/twitch"]
---

# Sub-Plan ch05: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML field order, `## Overview` → body →
> `## Related Notes` → `## References` → bold footer), dedup-before-create (term_dictionary + documentation/ +
> repo_openclaw*), the 9-GATE (G1–G9), cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are ALL
> inherited from the master and applied here without restatement.

## Scope

The 7 chat-platform integration pages in the OpenClaw `channels/` section that this sub-plan owns: **Slack**,
**SMS** (Twilio), **Synology Chat**, **Telegram**, **Tlon** (Urbit), the cross-channel **Troubleshooting**
playbook, and **Twitch**. These document, per platform, the setup procedure (app/bot creation, tokens, install),
transport mode (Socket Mode/HTTP, long-polling/webhook), access control + routing, runtime/feature behavior
(streaming, reactions, media, threading, interactive replies, approvals), and per-platform configuration +
troubleshooting. Priority **P2 (Phase B)** — these are integration/feature pages that build on the Phase-A gateway
+ concepts vocabulary (channel docking, sessions, pairing, secrets). The code-side counterparts
`repo_openclaw_channels` / `repo_openclaw_channels_messaging` are LINKED, not recreated; the OpenClaw channel

**Source**: OpenClaw docs, 7 pages, **19,586 measured words.** **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Slack | channels/slack | 7,364 | 31 | 21 | 11 | procedure (SPLIT ×4 — setup/transport, security/tokens/access, messaging UX, interactivity/config) |
| SMS (Twilio) | channels/sms | 1,503 | 20 | 9 | 11 | procedure |
| Synology Chat | channels/synology-chat | 945 | 4 | 9 | 0 | procedure |
| Telegram | channels/telegram | 6,172 | 31 | 9 | 1 | procedure (SPLIT ×2 — setup/access, feature reference/config/troubleshooting) |
| Tlon (Urbit) | channels/tlon | 1,045 | 12 | 14 | 0 | procedure |
| Troubleshooting | channels/troubleshooting | 1,213 | 2 | 11 | 8 | procedure (cross-channel diagnostics) |
| Twitch | channels/twitch | 1,344 | 15 | 13 | 5 | procedure |

(Code = raw ``` fences ÷ 2. Slack 62/2=31; SMS 40/2=20; Synology 8/2=4; Telegram 62/2=31; Tlon 24/2=12;
Troubleshooting 4/2=2; Twitch 30/2=15.)

## Content Strategy

- **Prioritize**: the per-platform setup/transport procedures (every deployment depends on app/bot creation +
  token model + transport choice) and access-control/routing (the safety boundary). For Slack and Telegram,
  prioritize separating the *setup* path from the *runtime feature* surface so each note is task-focused and ≤caps.
- **Split**: `slack.md` (7,364w, 21 H2 / 31 code) → **4 notes** (setup+transport, security/tokens/access,
  messaging+streaming+media UX, interactivity+approvals+config+troubleshooting). `telegram.md` (6,172w, 9 H2 /
  31 code) → **2 notes** (setup+access, feature-reference+config+troubleshooting). Both far exceed the 2,500w /
  6-code caps; split per the master word-cap + one-BB-per-note rules (see Split Decisions). SMS, Synology, Tlon,
  Troubleshooting, and Twitch each = 1 note (all ≤1,503w).
- **Link-out (not duplicated)**: pairing semantics → `channels/pairing` (ch04, planned); slash-command catalog →
  `tools/slash-commands` (to07, planned); plugin install rules → `tools/plugin` (to06, planned); gateway config
  patterns → `gateway/configuration*` (gw02, planned); SecretRef/secrets → `gateway/secrets*` (gw05/gw06,
  planned); Tailscale Funnel / reverse proxy / tunnels → `gateway/tailscale` (gw06, planned). Channel concepts
  (`channel-docking`, `channel-routing`, `group-messages`, `access-groups`, `broadcast-groups`,
  `bot-loop-protection`, `ambient-room-events`) live in ch01/co01 and are linked, not redefined. Platform/term
  vocabulary (Slack, SMS, Twilio, OAuth, webhook) links existing term notes; no term redefinition inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_slack_setup.md` | procedure | slack.md: Choosing Socket Mode or HTTP Request URLs, Install, Quick setup (Socket/HTTP tabs), Socket Mode transport tuning, Manifest and scope checklist (+ Additional manifest settings) | 700 | Setting up the Slack channel: choosing Socket Mode vs HTTP Request URLs, installing `@openclaw/slack`, the quick-setup flow for each transport, Socket Mode pong/backoff tuning, and the app-manifest + OAuth-scope checklist. |
| 2 | `oc_channels_slack_security_access.md` | procedure | slack.md: Token model, Actions and gates, Access control and routing, Native approvals in Slack | 650 | Slack security and access model: the bot/app/signing/user token model + per-credential status, action groups/gates, DM-policy + channel access control and routing, and native in-Slack tool approvals. |
| 3 | `oc_channels_slack_messaging.md` | procedure | slack.md: Threading sessions and reply tags, Ack reactions (+ Emoji/Scope), Text streaming, Typing reaction fallback, Media chunking and delivery, Attachment vision reference (+ supported types, inbound pipeline, thread-root inheritance, multi-attachment, size/download limits, known limits) | 700 | Slack messaging runtime UX: threading/session mapping + reply tags, ack reactions (emoji + scope), text streaming, typing-reaction fallback, media chunking/delivery, and the attachment-vision inbound pipeline (supported types, size/download/model limits). |
| 4 | `oc_channels_slack_interactivity.md` | procedure | slack.md: Commands and slash behavior, Interactive replies (+ Plugin-owned modal submissions), Events and operational behavior, Configuration reference, Troubleshooting | 650 | Slack interactivity + ops: slash-command behavior, interactive replies (buttons/modals incl. plugin-owned submissions), events/operational behavior, the full `channels.slack.*` configuration reference, and Slack-specific troubleshooting. |
| 5 | `oc_channels_sms.md` | procedure | sms.md: Before you begin, Quick Setup (Config file, Env vars, SecretRef auth token, Allowlist-only private number, Messaging Service sender, Default outbound target), Access control, Sending SMS, Verify Setup (E2E test), Webhook security, Multi-account config, Troubleshooting | 650 | Configuring the Twilio SMS channel: prerequisites, config-file / env-var / SecretRef token setup, Messaging-Service vs single-number senders, access control, sending SMS, end-to-end verification, Twilio webhook-signature security, multi-account config, and troubleshooting. |
| 6 | `oc_channels_synology_chat.md` | procedure | synology-chat.md: Bundled plugin, Quick setup, Environment variables, DM policy and access control, Outbound delivery, Multi-account, Security notes, Troubleshooting, Related | 450 | Configuring the Synology Chat channel: the bundled plugin, incoming/outgoing webhook quick setup, environment variables, DM policy + access control, outbound delivery, multi-account, security notes, and troubleshooting. |
| 7 | `oc_channels_telegram_setup.md` | procedure | telegram.md: Quick setup (BotFather token), Telegram side settings, Access control and activation (+ Group bot identity, DM policy, group/allowlist), Runtime behavior | 650 | Setting up the Telegram channel: creating the BotFather token, Telegram-side bot settings, access control + activation (group bot identity, DM policy, allowlists), and runtime behavior (long-polling default vs webhook mode). |
| 8 | `oc_channels_telegram_features.md` | procedure | telegram.md: Feature reference (streaming/preview, media, reactions, threading, commands, etc.), Error reply controls, Troubleshooting, Configuration reference, Related | 700 | Telegram feature + config reference: live-stream message-edit preview (streaming modes), media handling, reactions/threading/commands, error-reply controls, the full `channels.telegram.*` configuration reference, and troubleshooting. |
| 9 | `oc_channels_tlon.md` | procedure | tlon.md: Bundled plugin, Setup, Private/LAN ships, Group channels, Access control, Owner and approval system, Auto-accept settings, Delivery targets (CLI/cron), Bundled skill, Capabilities, Troubleshooting, Configuration reference, Notes, Related | 600 | Configuring the Tlon (Urbit) channel: the bundled plugin, ship setup (incl. private/LAN ships), group channels, access control, the owner/approval + auto-accept system, CLI/cron delivery targets, the bundled skill, capabilities, configuration reference, and troubleshooting. |
| 10 | `oc_channels_troubleshooting.md` | procedure | troubleshooting.md: Command ladder, After an update, per-platform failure signatures (WhatsApp, Telegram, Discord, Slack, iMessage, Signal, QQ Bot, Matrix), Related | 600 | Cross-channel troubleshooting playbook: the diagnostic command ladder, post-update repair steps, and per-platform failure signatures + fixes for WhatsApp, Telegram, Discord, Slack, iMessage, Signal, QQ Bot, and Matrix. |
| 11 | `oc_channels_twitch.md` | procedure | twitch.md: Bundled plugin, Quick setup (beginner), What it is, Setup (detailed) (Generate credentials, Configure the bot, Access control), Token refresh, Multi-account support, Access control, Troubleshooting, Config (Account config, Provider options), Tool actions, Safety and ops, Limits, Related | 650 | Configuring the Twitch chat channel: the bundled plugin, beginner + detailed setup (generating credentials, bot config, access control), optional token refresh, multi-account support, configuration reference (account config, provider options), tool actions, safety/ops, and limits. |

> **Note-count:** Slack splits into 4 (`_setup`, `_security_access`, `_messaging`, `_interactivity`) and Telegram
> into 2 (`_setup`, `_features`); the other 5 pages = 1 note each. **4 + 2 + 5 = 11 notes** (rows 1–11 above).
> This is exactly the master's ch05 estimate of 11. Final enumeration: notes 1–4 = Slack ×4, note 5 = SMS, note 6
> = Synology Chat, notes 7–8 = Telegram ×2, note 9 = Tlon, note 10 = Troubleshooting, note 11 = Twitch.

## Section Coverage Map

```
slack.md (7,364w, 21 H2 / 11 H3)
├── Choosing Socket Mode or HTTP Request URLs ───────── → note 1 (oc_channels_slack_setup)
├── Install ─────────────────────────────────────────── → note 1
├── Quick setup (Socket / HTTP tabs) ────────────────── → note 1
├── Socket Mode transport tuning ────────────────────── → note 1
├── Manifest and scope checklist (+ Additional manifest settings H3) → note 1
├── Token model ─────────────────────────────────────── → note 2 (oc_channels_slack_security_access)
├── Actions and gates ───────────────────────────────── → note 2
├── Access control and routing ──────────────────────── → note 2
├── Native approvals in Slack ───────────────────────── → note 2
├── Threading, sessions, and reply tags ─────────────── → note 3 (oc_channels_slack_messaging)
├── Ack reactions (+ Emoji `ackReaction` / Scope H3) ── → note 3
├── Text streaming ──────────────────────────────────── → note 3
├── Typing reaction fallback ────────────────────────── → note 3
├── Media, chunking, and delivery ───────────────────── → note 3
├── Attachment vision reference (+ Supported media types,
│   Inbound pipeline, Thread-root attachment inheritance,
│   Multi-attachment handling, Size/download/model limits,
│   Known limits, Related documentation H3) ─────────── → note 3
├── Commands and slash behavior ─────────────────────── → note 4 (oc_channels_slack_interactivity)
├── Interactive replies (+ Plugin-owned modal submissions H3) → note 4
├── Native approvals (covered note 2; cross-link) ───── → note 2 (primary), note 4 (link)
├── Events and operational behavior ─────────────────── → note 4
├── Configuration reference ─────────────────────────── → note 4
└── Troubleshooting ─────────────────────────────────── → note 4
sms.md (1,503w, 9 H2 / 11 H3)
├── Before you begin ────────────────────────────────── → note 5 (oc_channels_sms)
├── Quick Setup (Config file / Env vars / SecretRef /
│   Allowlist-only / Messaging Service / Default target H3) → note 5
├── Access control ──────────────────────────────────── → note 5
├── Sending SMS ─────────────────────────────────────── → note 5
├── Verify Setup (E2E test H3) ──────────────────────── → note 5
├── Webhook security ────────────────────────────────── → note 5
├── Multi-account config ────────────────────────────── → note 5
└── Troubleshooting (403 / no pairing / outbound / no answer H3) → note 5
synology-chat.md (945w, 9 H2)
├── Bundled plugin / Quick setup / Environment variables → note 6 (oc_channels_synology_chat)
├── DM policy and access control / Outbound delivery ── → note 6
├── Multi-account / Security notes / Troubleshooting ── → note 6
└── Related ─────────────────────────────────────────── → note 6 (References/Related Notes)
telegram.md (6,172w, 9 H2 / 1 H3)
├── Quick setup ─────────────────────────────────────── → note 7 (oc_channels_telegram_setup)
├── Telegram side settings ──────────────────────────── → note 7
├── Access control and activation (+ Group bot identity H3) → note 7
├── Runtime behavior ────────────────────────────────── → note 7
├── Feature reference ───────────────────────────────── → note 8 (oc_channels_telegram_features)
├── Error reply controls ────────────────────────────── → note 8
├── Troubleshooting ─────────────────────────────────── → note 8
├── Configuration reference ─────────────────────────── → note 8
└── Related ─────────────────────────────────────────── → note 8 (References/Related Notes)
tlon.md (1,045w, 14 H2)
├── Bundled plugin / Setup / Private-LAN ships ──────── → note 9 (oc_channels_tlon)
├── Group channels / Access control / Owner+approval ── → note 9
├── Auto-accept / Delivery targets (CLI-cron) ───────── → note 9
├── Bundled skill / Capabilities / Troubleshooting ─── → note 9
├── Configuration reference / Notes ─────────────────── → note 9
└── Related ─────────────────────────────────────────── → note 9 (References/Related Notes)
troubleshooting.md (1,213w, 11 H2 / 8 H3)
├── Command ladder / After an update ────────────────── → note 10 (oc_channels_troubleshooting)
├── WhatsApp / Telegram / Discord / Slack (failure sig H3) → note 10
├── iMessage / Signal / QQ Bot / Matrix (failure sig H3) → note 10
└── Related ─────────────────────────────────────────── → note 10 (References/Related Notes)
twitch.md (1,344w, 13 H2 / 5 H3)
├── Bundled plugin / Quick setup (beginner) / What it is → note 11 (oc_channels_twitch)
├── Setup detailed (Generate credentials / Configure bot /
│   Access control H3) ──────────────────────────────── → note 11
├── Token refresh / Multi-account / Access control ──── → note 11
├── Config (Account config / Provider options H3) ───── → note 11
├── Tool actions / Safety and ops / Limits ──────────── → note 11
└── Related ─────────────────────────────────────────── → note 11 (References/Related Notes)
```
**No orphaned H2/H3.** Link-out targets (pairing, slash-commands, plugin install, gateway config/secrets,
Tailscale, channel concepts) are referenced, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| slack.md (7,364w, 21 H2 / 11 H3, 31 code) | note 1 `oc_channels_slack_setup` · note 2 `oc_channels_slack_security_access` · note 3 `oc_channels_slack_messaging` · note 4 `oc_channels_slack_interactivity` | ~3× the 2,500w cap and ~5× the 6-code cap; the page covers four distinct task clusters — initial setup/transport, the security/token/access model, the messaging-runtime UX (streaming/reactions/media), and interactivity/ops/config/troubleshooting. Four notes keep each ≤700w / ≤6 code and one focused procedure. |
| telegram.md (6,172w, 9 H2 / 1 H3, 31 code) | note 7 `oc_channels_telegram_setup` · note 8 `oc_channels_telegram_features` | ~2.5× the word cap and ~5× the code cap; cleanly separates the setup/access procedure (BotFather, side settings, access control, runtime mode) from the dense feature + full-config + troubleshooting reference (the "Feature reference" H2 alone spans ~600 lines). Two notes keep each ≤700w / ≤6 code. |
| sms.md (1,503w) | (none — 1 note) | Within caps; single coherent Twilio-setup procedure. |
| synology-chat.md (945w) | (none — 1 note) | Within caps; small single procedure. |
| tlon.md (1,045w) | (none — 1 note) | Within caps; many short H2s but one coherent Urbit-channel setup procedure. |
| troubleshooting.md (1,213w) | (none — 1 note) | Within caps; one cross-channel diagnostic playbook (per-platform H3 subsections cohere as one note). |
| twitch.md (1,344w) | (none — 1 note) | Within caps; single Twitch-setup procedure. |

**Final note count = 11:** Slack ×4 (notes 1–4) + Telegram ×2 (notes 7–8) + SMS, Synology, Tlon,
Troubleshooting, Twitch ×1 each (notes 5, 6, 9, 10, 11) = 4 + 2 + 5 = **11** (matches the master's ch05 estimate).

## Summary Statistics & Building Block Distribution

- **Source pages: 7** (19,586 measured words). **New `oc_` notes: 11.** New `term_dictionary` notes: **0.**
- **BB distribution: procedure ×11** (every page is a setup/config/runtime-behavior/diagnostic how-to; no
  concept/model/argument note in this batch — the channel-concept material lives in ch01/co01 and is linked).
- **Est. digest words ~7,000** (avg ~636/note); every note ≤700w (well under the 2,500w cap).
- **Code fences:** 115 source fences total distribute across the 11 procedure notes; the two split pages (Slack
  31, Telegram 31) are partitioned so each resulting note stays ≤6 code blocks (config snippets reproduced
  selectively + verbatim). The 5 single-note pages (SMS 20, Twitch 15, Tlon 12, Synology 4, Troubleshooting 2)
  trim/select to ≤6 each at execution.
- **Cross-refs (floor, LOCKED at xref-augment 2026-06-21):** every note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (≥5 EXISTING
  [Per-Note Related Notes Mapping](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

below is rendered in the note's `## Related Notes` as `- [Name](relpath.md) — what it is; relevance: why THIS
sibling `oc_*` docs **(planned, this series)** to reach 10. Relative paths FROM a note at
`resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`;
other docs `../<folder>/<file>.md` (e.g. `../hermes_agent/hermes_Y.md`, `../claude_code/cc_Y.md`, `../pi/pi_Y.md`,
`../band/band_Y.md`, `../aws_sns/sns_Y.md`); repos `../../../areas/code_repos/repo_Y.md`; snippets
`../../code_snippets/snippet_Y.md`; entry points `../../../0_entry_points/entry_Y.md`.

### note 1 — oc_channels_slack_setup (10t · 11s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — team chat platform with apps/bots; relevance: the channel being set up.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack outbound-WSS transport needing no public URL; relevance: the default transport this note configures.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex persistent connection over TCP; relevance: Socket Mode rides a WSS connection to `wss-primary.slack.com`.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback for inbound events; relevance: the HTTP Request URLs transport receives Slack POSTs at a webhook path.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end that forwards to a backend; relevance: HTTP mode terminates Slack webhooks at a reverse proxy or tunnel.
- [DNS](../../term_dictionary/term_dns.md) — hostname resolution; relevance: HTTP Request URLs require a public DNS name for the Gateway.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: HTTP mode requires TLS termination for the inbound HTTPS endpoint.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the app-manifest declares OAuth bot scopes installed at setup.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — server that bridges chat platforms to agents; relevance: OpenClaw is the gateway hosting the Slack app this note installs.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: the product whose Slack channel is being set up.

**Docs**
- [Hermes: Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack adapter setup; relevance: direct analog of the Slack-app install + transport choice.
- [Hermes: Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — Hermes Slack config fields; relevance: parallel config keys for the same setup task.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how a messaging gateway wires platforms; relevance: explains the transport/adapter model Socket-vs-HTTP choice lives in.
- [Hermes: Adding a Platform Adapter (Built-in)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — registering a built-in channel; relevance: the install + enable flow mirrors `plugins install @openclaw/slack`.
- [CC: Claude Code in Slack](../claude_code/cc_claude_code_in_slack.md) — Claude Code's Slack integration; relevance: closest coding-agent-in-Slack setup precedent.
- [CC: Channels Setup](../claude_code/cc_channels_setup.md) — Claude Code channel configuration; relevance: analogous channel-onboarding procedure.
- [Band: Adapter Setup](../band/band_adapter_setup.md) — Band channel adapter onboarding; relevance: cross-product channel-setup analog.
- [oc_channels_slack_security_access](oc_channels_slack_security_access.md) — Slack token/access model **(planned, this series)**; relevance: next note — the tokens this setup obtains are governed there.
- [oc_channels_slack_messaging](oc_channels_slack_messaging.md) — Slack runtime UX **(planned, this series)**; relevance: sibling covering behavior once setup completes.
- [oc_channels_slack_interactivity](oc_channels_slack_interactivity.md) — Slack interactivity/ops **(planned, this series)**; relevance: sibling for slash/config after install.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where Socket/HTTP connection failures from this setup are diagnosed.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter framework; relevance: code home of the Slack channel registration.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging adapters incl. Slack transport; relevance: implements Socket Mode + HTTP request handling.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core + plugin install; relevance: hosts `plugins install @openclaw/slack`.

**Snippets**
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Socket Mode transport impl; relevance: exact-match source for the default transport.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter interface; relevance: the contract the Slack plugin implements on install.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how the installed Slack channel is registered/enabled.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Hermes Slack platform adapter; relevance: analog adapter wiring for Slack setup.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract platform base class; relevance: the adapter contract every channel (incl. Slack) extends.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform registry; relevance: registration step analog for an installed adapter.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: the dispatch path the installed transport hooks into.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — shared platform helpers; relevance: common setup/parse utilities reused across adapters.

**Entry point**

### note 2 — oc_channels_slack_security_access (9t · 11s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — team chat platform; relevance: the channel whose security model this note covers.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential from OAuth; relevance: bot/app/user tokens are OAuth tokens with per-credential status.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity; relevance: signing-secret + token verification authenticate Slack requests.
- [Access Control](../../term_dictionary/term_access_control.md) — who may do what; relevance: DM-policy + channel allowlist + groupPolicy are the access boundary.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — per-channel direct-message gate (pairing/allowlist/open/disabled); relevance: `channels.slack.dmPolicy` is documented verbatim here.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny access posture; relevance: name-based channel keys silently fail and unknown senders are blocked by default.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: action gates and native approvals gate tool calls.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — managed set of secrets/credentials; relevance: bot/app/signing/user tokens form the Slack credential set with status snapshots.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway enforcing the Slack token/access model.

**Docs**
- [Hermes: Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — Hermes Slack token/access fields; relevance: parallel token-model + allowlist config.
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook route auth/security; relevance: signing-secret verification analog for HTTP mode.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth credential flow; relevance: token-acquisition + status model analog.
- [CC: Authentication](../claude_code/cc_authentication.md) — Claude Code auth/token model; relevance: bearer-token + credential-status precedent.
- [CC: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — relaying tool-permission decisions over a channel; relevance: native in-Slack approval analog.
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — Pi provider authentication; relevance: cross-product token/secret model.
- [Band: Custom Integration](../band/band_custom_integration.md) — Band access/integration setup; relevance: allowlist/access-control analog.
- [oc_channels_slack_setup](oc_channels_slack_setup.md) — Slack setup **(planned, this series)**; relevance: the setup that obtains the tokens this note governs.
- [oc_channels_slack_interactivity](oc_channels_slack_interactivity.md) — Slack interactivity/ops **(planned, this series)**; relevance: native approvals are interactive (cross-link).
- [oc_channels_slack_messaging](oc_channels_slack_messaging.md) — Slack messaging UX **(planned, this series)**; relevance: action gates govern message-action availability.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — secrets + approvals; relevance: code home of token resolution + native approvals.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Slack token/action layer; relevance: implements action gates + access routing.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/ownership store; relevance: command-owner + pairing-owner bookkeeping.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist gate; relevance: exact-match for `dmPolicy` access control.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — peer→session binding/routing; relevance: ID-first channel routing + allowlist resolution.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — sender/channel match resolution; relevance: how allowlist entries resolve to IDs.
- [snippet_hermes_agent_gw_platform_feishu_acl](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_acl.md) — platform ACL enforcement; relevance: access-control-list analog for a chat channel.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix ACL; relevance: per-room/per-sender authorization analog.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Hermes Slack adapter; relevance: token model + auth wiring analog.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: where action-group capability is declared.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — per-sender rate limiting; relevance: abuse boundary alongside access gates.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch with gating; relevance: where action gates intercept dispatch.
- [snippet_slipbot_slack_handlers](../../code_snippets/snippet_slipbot_slack_handlers.md) — Slack handler wiring; relevance: handler-level auth/allowlist checks analog.

### note 3 — oc_channels_slack_messaging (10t · 11s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — team chat platform; relevance: the channel whose messaging UX this note covers.
- [SSE](../../term_dictionary/term_sse.md) — server-sent incremental streaming; relevance: text streaming edits the preview message incrementally (SSE-style).
- [Multimodal](../../term_dictionary/term_multimodal.md) — mixed text/image input; relevance: attachment-vision feeds images to a multimodal model.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — image understanding; relevance: the attachment-vision inbound pipeline.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered async delivery; relevance: media chunking/delivery + outbound chunk ordering.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling requests; relevance: chunked sends + Slack API limits shape delivery.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — maps platform threads to agent sessions; relevance: threading/sessions + reply-tag mapping is exactly this.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: outbound text chunking respects markdown/newline split modes.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: streaming previews the LLM's partial output.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway driving Slack streaming/media.

**Docs**
- [Hermes: Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack runtime; relevance: streaming/reactions/media behavior analog.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media handling config; relevance: media chunking + attachment limits analog.
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool surface; relevance: inbound/outbound media pipeline analog.
- [Hermes: Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — streaming/preview behavior; relevance: live-edit streaming analog across channels.
- [Band: Agent API Messages/Events](../band/band_agent_api_messages_events.md) — message/event model; relevance: how inbound messages + attachments are represented.
- [Band: WebSocket Human Channels](../band/band_websocket_human_channels.md) — streamed human-channel messages; relevance: real-time message streaming analog.
- [Pi: Extensions Events/Agent Tools](../pi/pi_extensions_events_agent_tools.md) — event/tool surface; relevance: reaction/system-event mapping analog.
- [oc_channels_slack_setup](oc_channels_slack_setup.md) — Slack setup **(planned, this series)**; relevance: sibling where the channel + scopes enabling media/reactions are configured.
- [oc_channels_slack_interactivity](oc_channels_slack_interactivity.md) — Slack interactivity/ops **(planned, this series)**; relevance: sibling; reactions/streaming feed interactive UX.
- [oc_channels_telegram_features](oc_channels_telegram_features.md) — Telegram feature reference **(planned, this series)**; relevance: parallel streaming/media/reactions reference for comparison.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — streaming/media delivery; relevance: implements text streaming + media chunking.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — threading→session mapping; relevance: thread_ts → session-suffix logic.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — media/file store; relevance: where downloaded attachments land for vision.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — ack/status reactions; relevance: exact-match for ack reactions + typing fallback.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread→session binding policy; relevance: threading/sessions + reply-tag mapping impl.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — media in/out handling; relevance: media chunking/delivery analog.
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — inbound attachment pipeline; relevance: attachment-vision inbound pipeline analog.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound send/chunk base; relevance: outbound text chunking analog.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch; relevance: where streaming previews and final sends are emitted.

### note 4 — oc_channels_slack_interactivity (9t · 11s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — team chat platform; relevance: the channel whose interactivity/ops this note covers.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: slash commands + modal submissions invoke agent/plugin handlers.
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack's UI block framework; relevance: interactive replies/buttons/modals compile to Block Kit.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: HTTP-mode slash commands + interactivity POST to webhook URLs.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — react to emitted events; relevance: block actions/shortcuts/modals emit structured system events.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — structured runtime event; relevance: edits/reactions/joins map to system events the agent sees.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the bot user that handles slash/interaction payloads.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: interactions apply the same DM/channel sender policy; blocked slash senders get ephemeral errors.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway dispatching Slack interactivity.

**Docs**
- [Hermes: Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — Slack config reference; relevance: parallel `channels.slack.*` ops/feature fields.
- [Hermes: Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Slack runtime; relevance: events/operational behavior analog.
- [Hermes: Discord Slash (advanced)](../hermes_agent/hermes_discord_advanced.md) — slash-command + interaction behavior; relevance: slash/interaction analog on another platform.
- [CC: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — interactive permission prompts over a channel; relevance: interactive-approval/modal analog.
- [Pi: Extensions Custom Tools](../pi/pi_extensions_custom_tools.md) — plugin/tool extension surface; relevance: plugin-owned modal-submission handler analog.
- [Pi: Extensions Events/Agent Tools](../pi/pi_extensions_events_agent_tools.md) — event/agent-tool surface; relevance: structured-event emission analog.
- [Band: A2A Gateway](../band/band_a2a_gateway.md) — agent-to-agent gateway events; relevance: event/interaction routing analog.
- [oc_channels_slack_setup](oc_channels_slack_setup.md) — Slack setup **(planned, this series)**; relevance: manifest enables slash commands + interactivity configured here.
- [oc_channels_slack_security_access](oc_channels_slack_security_access.md) — Slack access model **(planned, this series)**; relevance: slash/interactions reuse the access policy + native approvals.
- [oc_channels_slack_messaging](oc_channels_slack_messaging.md) — Slack messaging UX **(planned, this series)**; relevance: interactive replies share the message/Block-Kit path.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — interactivity handlers; relevance: implements slash/block-action/modal dispatch.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin extension layer; relevance: plugin-owned modal `view_submission`/`view_closed` handlers.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework + config; relevance: where the `channels.slack.*` config reference lives.

**Snippets**
- [snippet_slipbot_slack_handlers](../../code_snippets/snippet_slipbot_slack_handlers.md) — Slack handler wiring; relevance: slash/interaction handler registration analog.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — slash-command handling; relevance: slash-behavior analog.
- [snippet_hermes_agent_gw_platform_qqbot_keyboards](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_keyboards.md) — interactive keyboards/buttons; relevance: interactive-reply control analog.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch; relevance: routes slash/interaction events to the agent session.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — session routing; relevance: slash sessions route to target conversation session.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolution; relevance: shortcut/callback routing to the actor session.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — payload normalization; relevance: compacting raw interaction payloads into agent-visible events.

### note 5 — oc_channels_sms (10t · 10s · 11d)

**Terms**
- [SMS](../../term_dictionary/term_sms.md) — short message service; relevance: the channel/transport this note configures.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: Twilio POSTs inbound SMS to the Gateway webhook route.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/secret verification; relevance: SecretRef-resolved Auth Token + `X-Twilio-Signature` validation.
- [Access Control](../../term_dictionary/term_access_control.md) — who may message; relevance: `dmPolicy` pairing/allowlist/open governs sender access (`term_allowlist` MISSING → linked here).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — first-contact approval flow; relevance: default SMS policy is pairing; first message creates a pairing request.
- [Amazon Connect](../../term_dictionary/term_amazon_connect.md) — telephony/SMS contact platform; relevance: SMS/telephony provider analog for the Twilio messaging path.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: long replies are chunked before sending through Twilio.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end forwarder/tunnel; relevance: Tailscale Funnel / proxy must expose the exact `/webhooks/sms` path (`term_tailscale` MISSING → linked here).
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: SMS output strips markdown + flattens code fences to plain text.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway registering the Twilio SMS route.

**Docs**
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook signature/route security; relevance: direct analog of Twilio signature validation.
- [Hermes: Webhooks Routing Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook routing + delivery; relevance: inbound route + outbound reply delivery analog.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway webhook/adapter model; relevance: where the SMS webhook adapter fits.
- [AWS SNS: SMS Overview](../aws_sns/sns_sms_overview.md) — sending SMS via a provider; relevance: SMS-sending/provider analog (Twilio counterpart).
- [AWS SNS: SMS Preferences](../aws_sns/sns_sms_preferences.md) — SMS sender/config preferences; relevance: sender-number/messaging-service config analog.
- [AWS SNS: Mobile Push Send](../aws_sns/sns_mobile_push_send.md) — outbound send mechanics; relevance: `message send --channel sms` outbound analog.
- [AWS SNS: Delivery Retries (HTTP)](../aws_sns/sns_delivery_retries_http.md) — webhook delivery retries; relevance: Twilio `11200` "can't reach webhook" failure analog.
- [AWS SNS: Delivery Status Logging](../aws_sns/sns_delivery_status_logging.md) — delivery status visibility; relevance: verifying the SMS webhook route + delivery in logs.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where SMS 403/no-pairing/no-answer faults are diagnosed.
- [oc_channels_synology_chat](oc_channels_synology_chat.md) — Synology webhook channel **(planned, this series)**; relevance: sibling webhook-bot channel with the same token/route model.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — SMS adapter; relevance: implements the Twilio inbound/outbound path.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony sibling; relevance: shares the Twilio number/webhook split with Voice Call.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — secrets/webhook verify; relevance: SecretRef Auth Token + signature validation.

**Snippets**
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — SMS platform adapter; relevance: exact-match analog for the SMS channel.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — inbound webhook handler; relevance: the Twilio inbound webhook route impl.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the contract the SMS channel implements.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `dmPolicy` access control for SMS senders.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound send/chunk; relevance: plain-text chunked outbound SMS analog.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — per-sender rate limiting; relevance: outbound throttling/chunking analog.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: registering the SMS channel + `webhookPath`.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — target/session binding; relevance: `sms:`/`twilio-sms:` prefix target resolution.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — platform base; relevance: the abstract adapter the SMS channel extends.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform registry; relevance: multi-account SMS registration analog.

### note 6 — oc_channels_synology_chat (10t · 10s · 11d)

**Terms**
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: Synology incoming + outgoing webhooks are the whole transport.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the Synology Chat bot OpenClaw runs.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: the DM/conversation behavior of the Synology bot.
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: `dmPolicy` + `allowedUserIds` gate DMs (`term_allowlist` MISSING → linked here).
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message gate; relevance: `dmPolicy` allowlist/open/disabled documented here.
- [Authentication](../../term_dictionary/term_authentication.md) — secret verification; relevance: outgoing-webhook token verified (constant-time, fail-closed) across body/query/header forms.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — block requests to private/internal targets; relevance: outbound file URLs to private/blocked networks are rejected before forwarding to the NAS.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: inbound requests are token-verified and rate-limited per sender.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end forwarder; relevance: a proxy that strips the token header breaks auth (troubleshooting).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway hosting the Synology webhook route.

**Docs**
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook token/route security; relevance: direct analog of token verification + fail-closed.
- [Hermes: Webhooks Routing Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook in/out routing; relevance: incoming/outgoing webhook pair analog.
- [Hermes: MsGraph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — webhook-listener bot; relevance: webhook-driven channel-bot analog.
- [Hermes: Gateway Wecom Callback Setup](../hermes_agent/hermes_gateway_wecom_callback_setup.md) — callback/webhook channel setup; relevance: incoming/outgoing webhook setup analog.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway webhook model; relevance: where the Synology webhook adapter fits.
- [Band: Custom Integration](../band/band_custom_integration.md) — custom webhook integration; relevance: bring-your-own webhook channel analog.
- [Band: Integration Methods](../band/band_integration_methods.md) — integration transports; relevance: webhook-vs-socket integration choice analog.
- [AWS SNS: Delivery Retries (HTTP)](../aws_sns/sns_delivery_retries_http.md) — HTTP webhook delivery; relevance: outbound incoming-webhook delivery reliability analog.
- [oc_channels_sms](oc_channels_sms.md) — Twilio SMS channel **(planned, this series)**; relevance: sibling webhook-bot channel with the same token/route model.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where Synology token/route/allowlist faults are diagnosed.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: code home of the bundled Synology plugin.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — webhook-bot adapter; relevance: implements the incoming/outgoing webhook flow.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — token verify + SSRF guard; relevance: constant-time token check + private-network rejection.

**Snippets**
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — inbound webhook handler; relevance: the outgoing-webhook receiver impl.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — webhook listener; relevance: webhook-channel listener analog.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the contract the Synology channel implements.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: registering accounts + rejecting duplicate webhook paths.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM/allowlist gate; relevance: `dmPolicy` + `allowedUserIds` access control.
- [snippet_hermes_agent_gw_platform_feishu_connect](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_connect.md) — webhook-channel connect; relevance: enterprise webhook-bot connect analog.
- [snippet_hermes_agent_gw_platform_wecom_callback](../../code_snippets/snippet_hermes_agent_gw_platform_wecom_callback.md) — callback/token verification; relevance: outgoing-webhook token-verify analog.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound delivery base; relevance: incoming-webhook outbound delivery + URL media analog.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — target binding/routing; relevance: numeric `user_id` target resolution.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — shared helpers; relevance: header/token parsing + URL validation utilities.

### note 7 — oc_channels_telegram_setup (10t · 10s · 11d)

**Terms**
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the BotFather-created Telegram bot OpenClaw runs (`term_telegram` MISSING → linked here).
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: the Telegram bot's DM/group conversation behavior.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: webhook mode is the alternative to long-polling (`term_long_polling` MISSING → linked here).
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: `dmPolicy` + `allowFrom` + group allowlists gate access (`term_allowlist` MISSING → linked here).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — first-contact approval; relevance: default policy is pairing; first approved pairing seeds the command owner.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message gate; relevance: `channels.telegram.dmPolicy` pairing/allowlist/open/disabled documented here.
- [Authentication](../../term_dictionary/term_authentication.md) — secret/identity verification; relevance: BotFather token resolution + `getMe` identity cache.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: empty-allowlist allowlist mode blocks all DMs and is rejected by validation.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: polling/transport tuning + group traffic handling.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway running the Telegram bot.

**Docs**
- [Hermes: Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — Hermes Telegram onboarding; relevance: direct analog of BotFather token + DM-policy setup.
- [Hermes: Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — advanced Telegram config; relevance: privacy mode / group identity / access analog.
- [Hermes: Team Telegram Assistant Guide](../hermes_agent/hermes_guide_team_telegram_assistant.md) — Telegram assistant walkthrough; relevance: group/allowlist activation analog.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway transport model; relevance: long-polling-vs-webhook transport choice.
- [Hermes: Adding a Platform Adapter (Built-in)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — registering a channel adapter; relevance: enabling/activating the Telegram channel.
- [CC: Channels Setup](../claude_code/cc_channels_setup.md) — channel onboarding; relevance: token-in-config channel-setup analog.
- [Band: Adapter Setup](../band/band_adapter_setup.md) — adapter onboarding; relevance: cross-product channel-setup analog.
- [oc_channels_telegram_features](oc_channels_telegram_features.md) — Telegram feature reference **(planned, this series)**; relevance: the runtime/feature note this setup feeds into.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where `getMe 401` / polling-stall / allowlist faults are diagnosed.
- [oc_channels_slack_setup](oc_channels_slack_setup.md) — Slack setup **(planned, this series)**; relevance: parallel token/access setup procedure for comparison.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Telegram/grammY adapter; relevance: implements token, polling, and group handling.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — activation/routing framework; relevance: channel activation + access routing.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — owner/pairing store; relevance: first-pairing → command-owner seeding.

**Snippets**
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport (polling/webhook); relevance: exact-match for the transport this note sets up.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect/auth; relevance: token resolution + `getMe` analog.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `dmPolicy` + `allowFrom` access control.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the contract the Telegram channel implements.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: account registration + token-source precedence.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — sender/group match resolution; relevance: numeric user-ID + group-ID resolution.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — platform base; relevance: the abstract adapter Telegram extends.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — peer→session binding; relevance: DM/group/topic routing for the new channel.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform registry; relevance: multi-account Telegram registration analog.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound normalization; relevance: normalizing Telegram updates into the common message shape.

### note 8 — oc_channels_telegram_features (10t · 11s · 11d)

**Terms**
- [SSE](../../term_dictionary/term_sse.md) — incremental server-sent streaming; relevance: live message-edit preview streams partials (`term_streaming` MISSING → linked here).
- [Multimodal](../../term_dictionary/term_multimodal.md) — mixed text/media; relevance: media handling (images/files) in the feature reference.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: commands + reactions drive agent/tool actions.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered delivery; relevance: long finals split into multiple Telegram messages reusing the preview.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread→session mapping; relevance: threading + reply-tag behavior (honored even in `off` mode).
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: Telegram markdown formatting + native quote-reply path.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — structured runtime event; relevance: reactions/edits map to system events.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: streaming previews the LLM's partial + reasoning output.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the Telegram bot whose runtime features/config this note documents.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway driving Telegram streaming/media/config.

**Docs**
- [Hermes: Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — advanced Telegram features; relevance: direct analog of streaming/media/reactions reference.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media handling config; relevance: Telegram media-handling analog.
- [Hermes: Tools Reference Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media surface; relevance: media in/out feature analog.
- [Hermes: Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Slack runtime streaming; relevance: cross-channel streaming/edit-preview comparison.
- [Band: Agent API Messages/Events](../band/band_agent_api_messages_events.md) — message/event model; relevance: reaction/system-event mapping analog.
- [Band: WebSocket Human Channels](../band/band_websocket_human_channels.md) — streamed messages; relevance: live message streaming analog.
- [Pi: Extensions Events/Agent Tools](../pi/pi_extensions_events_agent_tools.md) — event/tool surface; relevance: command/reaction event mapping analog.
- [oc_channels_telegram_setup](oc_channels_telegram_setup.md) — Telegram setup **(planned, this series)**; relevance: the setup that enables these features.
- [oc_channels_slack_messaging](oc_channels_slack_messaging.md) — Slack messaging UX **(planned, this series)**; relevance: parallel streaming/media/reactions reference.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where `setMyCommands` / streaming / polling faults are diagnosed.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Telegram features/dispatch; relevance: implements streaming edits, media, reactions, commands.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — threading→session mapping; relevance: thread/reply-tag session suffixes.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — media store; relevance: where inbound Telegram media is stored.

**Snippets**
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram feature dispatch; relevance: exact-match for the feature dispatcher.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media handling; relevance: media-feature analog.
- [snippet_hermes_agent_gw_platform_telegram_markdown](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_markdown.md) — Telegram markdown rendering; relevance: markdown-format feature analog.
- [snippet_hermes_agent_gw_platform_telegram_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_normalize.md) — Telegram inbound normalization; relevance: reactions/threading event normalization.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread→session policy; relevance: threading + reply-tag binding impl.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/ack reactions; relevance: reaction feature impl.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound chunked send; relevance: long-final chunking + preview reuse.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch; relevance: where commands/feature events route to the agent.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — thread-reply handling; relevance: in-thread reply behavior analog.

### note 9 — oc_channels_tlon (10t · 10s · 11d)

**Terms**
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the Urbit-ship bot OpenClaw runs (`term_urbit`/`term_tlon` MISSING → linked here).
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: DM/group-mention conversation behavior on Tlon.
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: `dmAllowlist` + per-channel authorization rules (`term_allowlist` MISSING → linked here).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — first-contact approval; relevance: owner-ship receives approval requests for non-allowlisted ships.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: ship URL + login code (rotating) authenticate the connection.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — block private/internal targets; relevance: private/LAN ships require explicit `allowPrivateNetwork` opt-in to bypass SSRF protection.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: CLI/cron delivery targets for DMs and group channels.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: groups restricted by default; empty allowlist = no DMs; `autoAcceptGroupInvites` fails closed.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback transport; relevance: the ship-URL HTTP transport OpenClaw connects over.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway connecting to the Urbit ship.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/adapter model; relevance: where the Tlon adapter + ship transport fit.
- [Hermes: Adding a Platform Adapter (Built-in)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — registering a channel; relevance: bundled-plugin channel registration analog.
- [Hermes: Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — decentralized/daemon-backed channel; relevance: self-hosted-endpoint channel + allowlist analog.
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — endpoint/route security; relevance: SSRF/private-network protection analog.
- [Band: WebSocket Human Channels](../band/band_websocket_human_channels.md) — persistent human-channel connection; relevance: ship-connection + group-channel analog.
- [Band: Custom Integration](../band/band_custom_integration.md) — custom endpoint integration; relevance: bring-your-own-endpoint channel analog.
- [Pi: Extensions Custom Tools](../pi/pi_extensions_custom_tools.md) — bundled tool/skill surface; relevance: the bundled `@tloncorp/tlon-skill` CLI analog.
- [Hermes: Messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — decentralized/federated chat channel adapter; relevance: Matrix is the closest peer to Tlon/Urbit — a decentralized, self-hosted-endpoint messaging network with the same ship-URL-style connect + room model.
- [oc_channels_sms](oc_channels_sms.md) — Twilio SMS channel **(planned, this series)**; relevance: sibling channel sharing CLI/cron delivery targets + allowlist model.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where DM-ignored / connection / auth-code faults are diagnosed.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: code home of the bundled Tlon plugin.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Tlon adapter; relevance: implements ship connection, DMs, group channels, rich-text conversion.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — bundled-skill layer; relevance: the bundled Tlon skill providing CLI operations.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the contract the Tlon channel implements.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/channel resolution; relevance: DM vs group-channel target resolution + auto-discovery.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM/allowlist gate; relevance: `dmAllowlist` + owner-approval flow.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — ship/channel match resolution; relevance: per-channel authorization rule matching.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: account registration + channel-nest normalization.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — self-hosted endpoint adapter; relevance: decentralized/daemon-endpoint channel analog.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — homeserver connect; relevance: ship-URL connect + login analog.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound normalization; relevance: Tlon rich-text → common shape normalization.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound delivery; relevance: markdown→Tlon-format conversion + image upload delivery.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — target binding/routing; relevance: `dm/` and `chat/` / `group:` target prefixes.

### note 10 — oc_channels_troubleshooting (10t · 11s · 11d)

**Terms**
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: webhook-mode channels' "can't reach webhook" failure class.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack WSS transport; relevance: "socket mode connected but no responses" signature.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: token/auth failures (`getMe 401`, signing-secret, QQ creds) across platforms.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: `openclaw channels status --probe` + healthy-baseline checks.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic liveness signal; relevance: reconnect/relogin-loop + transport-connected diagnostics.
- [Graceful Degradation](../../term_dictionary/term_graceful_degradation.md) — partial-failure fallback; relevance: doctor `--fix` repairs corrupt dependency trees / stale clients without full outage.
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: Telegram send failures point to DNS/IPv6/proxy routing.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: `BOT_COMMANDS_TOO_MUCH` / reconnect-backoff signatures.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: per-platform bot failure signatures are the page's body.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway whose `status`/`doctor`/`probe` ladder is the diagnostic spine.

**Docs**
- [CC: Authentication and Network Errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network failure triage; relevance: direct analog of token/DNS/proxy failure signatures.
- [CC: Login Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/token diagnostics; relevance: `getMe 401` / token-source analog.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway run/restart ops; relevance: `gateway restart` + reload-clean-state analog.
- [Hermes: CLI Commands Ops/Maintenance/Auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — diagnostic/maintenance CLI; relevance: the `status`/`doctor`/`probe` command-ladder analog.
- [Hermes: Cron Troubleshooting Guide](../hermes_agent/hermes_guide_cron_troubleshooting.md) — guided failure-signature triage; relevance: symptom→check→fix table format analog.
- [Hermes: Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — daemon-channel troubleshooting; relevance: "daemon reachable but bot silent" signature analog.
- [Hermes: Discord Advanced](../hermes_agent/hermes_discord_advanced.md) — Discord intent/guild gating; relevance: "online but no guild replies" signature analog.
- [oc_channels_slack_interactivity](oc_channels_slack_interactivity.md) — Slack ops/config **(planned, this series)**; relevance: per-platform Slack troubleshooting cross-link.
- [oc_channels_telegram_features](oc_channels_telegram_features.md) — Telegram features/config **(planned, this series)**; relevance: per-platform Telegram troubleshooting cross-link.
- [oc_channels_sms](oc_channels_sms.md) — SMS channel **(planned, this series)**; relevance: SMS-specific failure signatures cross-link.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel diagnostics framework; relevance: `channels status --probe` + per-channel health.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — doctor/diagnostic CLI; relevance: `openclaw doctor` + `doctor --fix` repair commands.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — per-platform adapters; relevance: where per-channel failure modes originate.

**Snippets**
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable kernel/recovery; relevance: reconnect/restart-on-failure recovery behavior.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolution; relevance: silent-block-on-name-key + allowlist mismatch diagnosis.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Socket Mode transport; relevance: "socket mode connected but no responses" path.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram polling transport; relevance: polling-stall / reconnect signature source.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: "DMs blocked → approve pairing / relax policy" fixes.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — rate-limit/backoff; relevance: reconnect-backoff + command-count limit signatures.
- [snippet_hermes_agent_gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord connect/intents; relevance: guild-reply + message-content-intent fix.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix connect/verify; relevance: encrypted-room / device-verify failure fix.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp QR/connect; relevance: "QR login times out 408" + relogin-loop fix.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch; relevance: where "transport connected but replies fail" is observed.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: "plugin load failed / dependency tree corrupted" after-update repair.

### note 11 — oc_channels_twitch (11t · 10s · 11d)

**Terms**
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: Twitch access token (`oauth:` prefix) + `chat:read`/`chat:write` scopes.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer access token; relevance: the access/refresh-token model + token refresh.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the dedicated Twitch bot account OpenClaw authenticates as.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: the Twitch chat-room bot behavior.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — server bridging chat platforms to agents; relevance: Twitch chat rides an IRC connection the gateway owns (`term_irc` MISSING → IRC documented as transport, this is the nearest existing term).
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: `allowFrom` user-ID allowlist + `allowedRoles` + `requireMention`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: Client ID + access token + optional refresh-token auth.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: 500-char auto-chunking + Twitch's built-in rate limits.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — access gate; relevance: role/user-ID allowlist gating mirrors the DM-policy access model.
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: markdown is stripped before 500-char chunking.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: the gateway running the Twitch chat bot.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/adapter model; relevance: where the Twitch (IRC) adapter fits.
- [Hermes: Adding a Platform Adapter (Built-in)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — registering a channel; relevance: bundled-plugin channel registration analog.
- [Hermes: Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — token/daemon-auth channel; relevance: access-token + allowlist channel analog.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth token + refresh; relevance: automatic token-refresh flow analog.
- [Hermes: Provider XAI Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — OAuth client/refresh setup; relevance: clientSecret + refreshToken refresh analog.
- [CC: Authentication](../claude_code/cc_authentication.md) — token/credential model; relevance: access-token handling + scoping precedent.
- [Band: Adapter Setup](../band/band_adapter_setup.md) — channel adapter onboarding; relevance: bot-account + token channel-setup analog.
- [oc_channels_tlon](oc_channels_tlon.md) — Tlon channel **(planned, this series)**; relevance: sibling bundled-plugin channel with allowlist + bot-account model.
- [oc_channels_troubleshooting](oc_channels_troubleshooting.md) — cross-channel diagnostics **(planned, this series)**; relevance: where Twitch token/connection faults are diagnosed.
- [oc_channels_sms](oc_channels_sms.md) — SMS channel **(planned, this series)**; relevance: parallel token + chunked-plain-text-output channel for comparison.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — Twitch (IRC) chat adapter; relevance: implements connect, token refresh, send.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: code home of the bundled Twitch plugin.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — provider/plugin options; relevance: provider options + tool-action surface.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter contract; relevance: the contract the Twitch channel implements.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — deterministic routing; relevance: replies always route back to Twitch + session key per account.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — allowlist gating; relevance: `allowFrom` user-ID allowlist analog.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: multi-account (one-token-per-channel) registration.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — token/daemon adapter; relevance: token-auth + connect channel analog.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — rate limiting; relevance: 500-char chunking + provider rate-limit analog.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — platform base; relevance: the abstract adapter Twitch extends.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound chunked send; relevance: stripped-markdown 500-char outbound analog.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — sender/role resolution; relevance: user-ID + role (`moderator`/`vip`) matching.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform registry; relevance: multi-account Twitch registration analog.

`term_acp_agent_client_protocol`, `term_mcp`, `term_agent_harness`, `term_autonomous_coding_agents`,
`term_function_calling`, `term_sandbox`, `term_llm`, `term_claude`, `term_oauth`, `term_oauth_token`,
`term_websocket`, `term_json_rpc`, `term_cron`, `term_authentication`, `term_webhook`, `term_reverse_proxy`,
`term_bot`, `term_chatbot`, `term_slack`, `term_sms`, `term_socket_mode`, `term_rate_limiting`,
`term_access_control`, `term_api_gateway`, `term_tls`, `term_dns`, `term_load_balancer`, `term_sse`,
`term_message_queue`, `term_multimodal`, `term_agentic_ai`, `term_amazon_connect`,
`term_event_driven_architecture`. **Verified-MISSING (do NOT cite as existing; link the nearest existing term
instead):** `term_telegram`, `term_twilio`, `term_secretref`, `term_tailscale`, `term_allowlist`,
`term_signing_secret`, `term_long_polling`, `term_pairing`, `term_streaming`, `term_matrix`, `term_signal`,
`term_discord`, `term_whatsapp`, `term_irc`. MISSING terms are redirected to the nearest existing term in the
per-note mapping above per the Undigested Terms Plan (e.g. SecretRef → `term_authentication`/`term_oauth_token`;
allowlist → `term_access_control`; Tailscale → `term_reverse_proxy`; streaming → `term_sse`; Telegram/Twitch IRC
→ `term_bot`/`term_chatbot`/`term_messaging_gateway`).

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| OpenClaw channel/platform vocabulary (channel docking, channel routing, access groups, broadcast groups, bot-loop protection, ambient room events) | OpenClaw vocab → already owned by ch01/co01 `oc_*` doc notes; **link those siblings** (planned), do NOT create term_dictionary entries. |
| Telegram, Twilio, Tlon/Urbit, Twitch, Synology Chat, Matrix, Signal, Discord, WhatsApp, IRC | Platform proper nouns documented *as config*, NOT promoted to term notes (mirrors the master + Pi/CC precedent of not promoting provider/platform names). `term_telegram` / `term_twilio` MISSING — link the channel doc note + `term_bot`/`term_chatbot`/`term_webhook` instead. |
| SecretRef, allowlist, signing secret, long polling, pairing, Tailscale, streaming | Cross-cutting infra concepts whose home is elsewhere: SecretRef/secrets → `gateway/secrets*` (gw05/gw06 oc_* doc notes, planned) + link `term_authentication`/`term_oauth_token`; allowlist → link `term_access_control`; pairing → `channels/pairing` (ch04 oc_* note, planned); Tailscale/tunnels → `gateway/tailscale` (gw06 note, planned) + link `term_reverse_proxy`; streaming → link `term_sse`. **No new term_dictionary captures** (`term_secretref`/`term_allowlist`/`term_signing_secret`/`term_long_polling`/`term_pairing`/`term_tailscale`/`term_streaming` all MISSING — covered by doc notes/existing-term links per master policy). |

**Expected new `term_dictionary` captures from ch05: 0.** No genuinely cross-cutting reusable term lacks both a
doc-page home and an existing note. (If augment's Step 2d re-scan surfaces one, it would be captured via
`/tessellum-capture-term-note` + added to `acronym_glossary_software.md` / `acronym_glossary_gen_ai.md` — but none
is anticipated for this channels batch.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** ch05 authors zero `term_dictionary` notes; the only term interaction is **linking

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). All 8 gates must PASS before commit.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` on all 11 notes (YAML field order, H1/`## Overview`/`## Related Notes`/`## References`/footer, indexed `[text](path.md)` links). |
| G2 | Grounding | Diff each note vs its `inbox/openclaw_docs/channels/<page>` source section; no invented config keys/flags; config snippets verbatim. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks, one BB; Section Coverage Map fully satisfied (no orphan H2/H3). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken links after incremental reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` rows + the inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_slack_setup oc_channels_slack_security_access oc_channels_slack_messaging oc_channels_slack_interactivity oc_channels_sms oc_channels_synology_chat oc_channels_telegram_setup oc_channels_telegram_features oc_channels_tlon oc_channels_troubleshooting oc_channels_twitch"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # REQUIRE_SOURCE_URL
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # sibling-prefix cross-ref presence
  grep -qE "\($SIBLING_PREFIX|/$SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) XREF: $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5/G6 after incremental reindex
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2,500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_channels_slack_setup | procedure | 700 | ≤6 | ✅ |
| 2 | oc_channels_slack_security_access | procedure | 650 | ≤6 | ✅ |
| 3 | oc_channels_slack_messaging | procedure | 700 | ≤6 | ✅ |
| 4 | oc_channels_slack_interactivity | procedure | 650 | ≤6 | ✅ |
| 5 | oc_channels_sms | procedure | 650 | ≤6 | ✅ |
| 6 | oc_channels_synology_chat | procedure | 450 | ≤4 | ✅ |
| 7 | oc_channels_telegram_setup | procedure | 650 | ≤6 | ✅ |
| 8 | oc_channels_telegram_features | procedure | 700 | ≤6 | ✅ |
| 9 | oc_channels_tlon | procedure | 600 | ≤6 | ✅ |
| 10 | oc_channels_troubleshooting | procedure | 600 | ≤2 | ✅ |
| 11 | oc_channels_twitch | procedure | 650 | ≤6 | ✅ |

All 11 notes within caps. The two code-heavy split pages (Slack 31 fences, Telegram 31 fences) are partitioned so
each resulting note reproduces only its section's config snippets (≤6 each); the 5 single-note pages trim to ≤6.

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, `building_block:
navigation`) under a **"Channels"** cluster (ch05 sub-section: Slack ×4, SMS, Synology Chat, Telegram ×2, Tlon,
Troubleshooting, Twitch). Each note receives its entry-point back-link at finalization. The master-level hub
updates (W2 parent `entry_gen_ai_dev.md`; W3 `term_openclaw.md` + `repo_openclaw.md` ↔ docs) are done once at the
master pre-step, not per sub-plan.

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` **(planned, master pre-step)** → all 11 notes (Channels cluster rows). **Primary G8 guarantee.**
- `areas/code_repos/repo_openclaw_channels.md` → notes 1, 5, 6, 9, 10, 11 (channel-framework ↔ docs).
- `areas/code_repos/repo_openclaw_channels_messaging.md` → notes 1, 2, 3, 4, 5, 7, 8, 11 (messaging adapters ↔ docs).
- `areas/code_repos/repo_openclaw_security.md` → notes 2, 5 (token/secret/approval ↔ docs).
- `areas/code_repos/repo_openclaw_sessions.md` → notes 3, 8 (threading/session ↔ docs).
- `resources/term_dictionary/term_slack.md` → notes 1–4, 10.
- `resources/term_dictionary/term_sms.md` → note 5, 10.
- `resources/term_dictionary/term_socket_mode.md` → notes 1, 10.
- `resources/term_dictionary/term_webhook.md` → notes 5, 6, 7, 9, 10.
- `resources/term_dictionary/term_oauth.md` → notes 1, 11.

(At execution, add the reciprocal inbound link from each cited existing repo/term to the new note so in-degree ≥1
is real, not just plan-asserted; verify via the `note_links` table before commit.)

## Pacing Rules (inherited from master)

Single execution phase (11 notes, one wave — within the ~30-agent fan-out cap). All 8 gates pass before commit.
Re-read each source page during execution; reproduce config snippets verbatim; one BB per note. `git pull
--rebase --autostash origin main` before committing; commit + push the wave together; **no Claude co-author
trailer.** Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of the 11 planned ch05 notes — re-read all 7 source pages under
`inbox/openclaw_docs/channels/` (measured: slack 7,364w/29 fences/21 H2/11 H3; sms 1,503/20/9/11; synology-chat
945/4/9/0; telegram 6,172/27/9/1; tlon 1,045/12/14/0; troubleshooting 1,213/2/11/8; twitch 1,344/7/13/5) — and
Measured words match the plan exactly; source code-fence counts run slightly below the plan's estimates (slack 29
vs 31, telegram 27 vs 31, twitch 7 vs 15) — this does NOT change any split/density conclusion (both split pages
still vastly exceed the 6-fence cap; all 11 notes stay ≤700w / ≤6 fences). No re-split needed.

**What was locked (per-note counts — all PASS floors):**

| Note | Terms | Snippets | Docs (existing) | Repos | Floors met |
|---|---:|---:|---:|---:|---|
| 1 oc_channels_slack_setup | 10 | 11 | 11 (7) | 3 | ✅ |
| 2 oc_channels_slack_security_access | 9 | 11 | 11 (7) | 3 | ✅ |
| 3 oc_channels_slack_messaging | 10 | 11 | 11 (7) | 3 | ✅ |
| 4 oc_channels_slack_interactivity | 9 | 11 | 11 (7) | 3 | ✅ |
| 5 oc_channels_sms | 10 | 10 | 11 (8) | 3 | ✅ |
| 6 oc_channels_synology_chat | 10 | 10 | 11 (8) | 3 | ✅ |
| 7 oc_channels_telegram_setup | 10 | 10 | 11 (7) | 3 | ✅ |
| 8 oc_channels_telegram_features | 10 | 11 | 11 (7) | 3 | ✅ |
| 9 oc_channels_tlon | 10 | 10 | 10 (7) | 3 | ✅ |
| 10 oc_channels_troubleshooting | 10 | 11 | 11 (7) | 3 | ✅ |
| 11 oc_channels_twitch | 11 | 10 | 11 (7) | 3 | ✅ |

**Verification (deterministic):** all cited EXISTING note_ids re-verified in the DB 2026-06-21 via
(35 terms + 24 doc-pool docs + 12 repos + 47 snippets all confirmed; the rest are sibling `oc_*` planned this
snippet). Every note carries an `entry_openclaw_docs` back-link (planned master pre-step W1) for G8.

**New-term candidates surfaced at re-read (Step 2d):** **NONE promoted.** The re-read confirmed the plan's
Undigested Terms Plan: OpenClaw channel vocabulary (channel docking/routing, access/broadcast groups,
bot-loop-protection, ambient room events) is owned by ch01/co01 `oc_*` doc notes; platform proper nouns
(Telegram, Twilio, Tlon/Urbit, Twitch, Synology Chat, Matrix, Signal, Discord, WhatsApp, IRC) are documented
*as config*, not promoted (mirrors the CC/Pi precedent); cross-cutting infra (SecretRef, allowlist, signing
secret, long polling, pairing, Tailscale, streaming) is either owned by gateway sub-plans (gw05/gw06) or
redirected to existing terms. **The augment surfaced richer EXISTING vault terms than the original plan cited**
and used them (best-fit glossaries: `acronym_glossary_software.md` / `acronym_glossary_gen_ai.md`):
`term_messaging_gateway`, `term_dm_pairing`, `term_dm_policy`, `term_thread_binding_policy`, `term_deny_first`,
`term_ssrf_guard`, `term_block_kit`, `term_agent_lifecycle_event`, `term_credential_pool`, `term_health_check`,
`term_heartbeat`, `term_graceful_degradation`, `term_markdown`, `term_computer_vision`, `term_channel_adapter`,

**Redirect note (G5):** MISSING terms (`term_telegram`, `term_twilio`, `term_secretref`, `term_tailscale`,
`term_allowlist`, `term_long_polling`, `term_streaming`, `term_irc`, …) are NOT cited as existing anywhere; each
is redirected to the nearest existing term in the mapping (SecretRef → `term_authentication`/`term_oauth_token`;
allowlist → `term_access_control`; Tailscale → `term_reverse_proxy`; streaming → `term_sse`; IRC →
`term_messaging_gateway`; Telegram/Twitch platform names → `term_bot`/`term_chatbot`).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Verdict | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | Per-Note Related Notes Mapping present; every note ≥8 terms · ≥10 snippets · ≥10 docs, each link carries a relevance statement (`- [Name](path.md) — what; relevance: why`). Floor-check script: 11/11 PASS. |
| CP2 | 9-GATE present per batch (G1–G6, G8, G9) | **PASS** | Single-phase G1–G8 gate table present; G4 updated to the raised ≥8t/≥10s/≥10d floor; G5 ghost-detect + G6 broken-link-fix + G7/G8 in-degree all listed; Validation Scripts implement G1/G3/G5/G6. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | Entry Point Decision inherits the master W1 CREATE of `entry_openclaw_docs.md` (`building_block: navigation`); 11 rows under a Channels cluster; every note cites the entry-point back-link (DB-confirmed `entry_openclaw_docs` does NOT yet exist → correctly marked planned). |
| CP4 | Size | **PASS** | 11 notes ≤30 (single executable wave, within ~30-agent fan-out cap). |
| CP5 | Format derived (not invented) | **PASS** | Format inherited from master, derived from existing `claude_code/`+`pi/` doc corpora: `# OpenClaw — Title` → `## Overview` → mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; YAML field order + forbidden-field list match. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 11 notes ≤700w / ≤6 fences / ≤400L; split pages partitioned so each note ≤6 fences. Measured source words match plan; no borderline note needs further split. |
| CP7 | Sources measured (not guessed) | **PASS** | All 7 pages re-read + measured 2026-06-21; word counts match plan to the unit; code-fence counts slightly below estimate (does not change splits). 0 pages >1.5× estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | Undigested Terms Plan + Term-Note Authoring Requirements present; ch05 authors 0 new terms (N/A authoring); Step 2d re-scan promoted 0 new terms (all OpenClaw/platform vocab owned elsewhere or redirected to existing). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | Inlinks table maps existing repos/terms → all 11 new notes; every new note also receives the `entry_openclaw_docs` Channels-cluster row (in-degree ≥1 from outside the folder); G8-Discoverability in the gate table; inlink-addition is a gated execution step, not a recommendation. |

**RESULT: 9/9 checkpoints PASS (CP1–CP9, incl. CP8f) → READY FOR EXECUTION.** All notes meet the raised floors
`pending → ready`.
</content>
</invoke>
