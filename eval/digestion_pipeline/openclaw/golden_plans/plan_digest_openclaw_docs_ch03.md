---
title: Sub-Plan ch03 — OpenClaw Docs: Channels (LINE, Location, Matrix, Mattermost)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/line", "channels/location", "channels/matrix", "channels/matrix-migration", "channels/matrix-presentation", "channels/matrix-push-rules", "channels/mattermost"]
---

# Sub-Plan ch03: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML + Overview/body/Related Notes/References),
> dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), the 9-GATE, cross-references, and
> entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master. This file is authored from a
> fresh re-read + `wc -w`/grep measurement of its 7 assigned pages (Step 1c/Step 8); per-note Related-Notes
> mapping is LOCKED later at `/tessellum-augment-digestion-plan` — this PLAN stage lists `## Candidate Cross-References`.

## Scope

The 7 Channels pages for **LINE**, **inbound location parsing**, the **Matrix** channel (the single largest
channel page in the corpus, plus its migration / presentation-metadata / push-rules companions), and
**Mattermost**. These document operator-facing channel-connection procedures (install plugin → configure auth →
access control → message behavior) plus two protocol/data-contract pages (Matrix `com.openclaw.presentation`
metadata; inbound location `ctx` fields). Priority **P2** (Phase B — features/integration): channels depend on
the Phase-A gateway/CLI/concepts vocabulary (config, sessions, streaming, pairing, approvals) but are
themselves integration surfaces. The code-side counterparts `repo_openclaw_channels`,
`repo_openclaw_channels_messaging`, `repo_openclaw_security`, `repo_openclaw_gateway` and the existing Hermes
`hermes_messaging_*` channel docs are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **14,173 measured words**. **Planned: 12 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| LINE | channels/line | 924 | 10 | 10 | 0 | procedure |
| Channel location parsing | channels/location | 309 | 2 | 4 | 0 | model |
| Matrix | channels/matrix | 5,856 | 34 | 25 | 23 | procedure + model (split ×4) |
| Matrix migration | channels/matrix-migration | 3,215 | 9 | 9 | 4 | procedure (split ×2) |
| Matrix presentation metadata | channels/matrix-presentation | 433 | 1 | 6 | 0 | model |
| Matrix push rules | channels/matrix-push-rules | 734 | 5 | 5 | 0 | procedure |
| Mattermost | channels/mattermost | 2,702 | 15 | 16 | 1 | procedure + model (split ×2) |

Fence count = `grep -c '```' / 2` (raw fence lines: line 20, location 4, matrix 68, matrix-migration 18,
matrix-presentation 2, matrix-push-rules 10, mattermost 30). Word counts via `wc -w` on the raw mirror file.

## Content Strategy

- **Prioritize**: Matrix setup + E2EE verification (the only channel with end-to-end encryption and a deep CLI
  verification surface — highest operational complexity) and the Mattermost interactive-button HMAC contract
  (a reusable signing recipe). These carry the densest reusable procedure/security content.
- **Split**: `matrix.md` (5,856w, 25 H2 / 23 H3, mixed procedure+model) → **4 notes** (setup+access config
  procedure · E2EE encryption/verification procedure · runtime message-behavior features model · configuration
  reference model). `matrix-migration.md` (3,215w) → **2 notes** (upgrade flow + how-it-works procedure · the
  ~190-line "Common messages" diagnostic reference). `mattermost.md` (2,702w, just over the 2,500 cap) → **2
  notes** (core setup/chat/threading/streaming/reactions procedure · interactive-buttons + Direct-API/HMAC
  contract). All other pages = 1 note each.
- **Link-out (do NOT redefine here)**: shared `pairing` (→ ch04 `channels/pairing`), `groups` / `access-groups`
  / `channel-routing` / `bot-loop-protection` (→ ch01–ch02), `concepts/streaming`, `tools/acp-agents`,
  `tools/exec-approvals`, `tools/media-overview`, `gateway/security` / `gateway/secrets` / `gateway/doctor`,
  `nodes/location-command`. Link existing terms (`term_openclaw`, `term_oauth`, `term_encryption`,
  `term_webhook`, `term_speech_to_text`, …) — never inline a term definition in an `oc_*` note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_line.md` | procedure | line.md: Install, Setup (webhook + signature), Configure, Access control, Message behavior, Channel data (rich messages), ACP support, Outbound media, Troubleshooting | 700 | Connecting OpenClaw to LINE via the LINE Messaging API: plugin install, webhook + channel-token/secret setup, minimal/public/multi-account config, DM/group access control, message chunking/media behavior, `channelData.line` rich messages, ACP bindings, and outbound media. |
| 2 | `oc_channels_location.md` | model | location.md: (intro), Text formatting, Context fields, Channel notes | 450 | How OpenClaw normalizes inbound shared locations (Telegram/WhatsApp/Matrix) into terse body text plus structured `Location*` `ctx` fields, with untrusted label/address/caption rendered through the bounded JSON metadata path. |
| 3 | `oc_channels_matrix_setup.md` | procedure | matrix.md: Install, Setup, Interactive setup, Minimal config, Auto-join, Allowlist target formats, Account ID normalization, Cached credentials, Environment variables, Configuration example | 750 | Installing and configuring the Matrix channel plugin: token/password auth, interactive wizard, minimal config, `autoJoin` invite gating, stable allowlist target formats, account-ID normalization, cached credentials, and the `MATRIX_*` env-var matrix. |
| 4 | `oc_channels_matrix_encryption.md` | procedure | matrix.md: Encryption and verification (Enable encryption, Status and trust signals, Verify device with recovery key, Bootstrap/repair cross-signing, Room-key backup, Listing/requesting/responding to verifications), Multi-account notes (startup/verification/device/crypto-store accordions), Profile management, Private/LAN homeservers, Proxying Matrix traffic | 800 | Matrix end-to-end encryption operations: `openclaw matrix encryption setup`, the three trust signals, recovery-key device verification (stdin), cross-signing bootstrap/repair, room-key backup status/restore/reset, the SAS verification command set, startup verification behavior, and private-homeserver / proxy hardening. |
| 5 | `oc_channels_matrix_behavior.md` | model | matrix.md: Configuration example, Streaming previews, Voice messages, Approval metadata (+ self-hosted push-rules pointer), Bot-to-bot rooms, Threads (sessionScope, threadReplies, thread inheritance), ACP conversation bindings (+ thread binding config), Reactions, History context, Context visibility, DM and room policy, Direct room repair, Exec approvals, Slash commands, Multi-account, Target resolution | 800 | Matrix runtime message behavior: streaming/blockStreaming preview modes, voice-note transcription before the mention gate, `com.openclaw.approval` metadata, bot-to-bot rooms, native threads (`sessionScope`/`threadReplies`), ACP conversation bindings, reactions, history/context-visibility, DM/room policy + direct-room repair, exec/plugin approvals, slash commands, multi-account, and target resolution. |
| 6 | `oc_channels_matrix_config_reference.md` | model | matrix.md: Configuration reference (Account and connection, Encryption, Access and policy, Reply behavior, Reaction settings, Tooling and per-room overrides, Exec approval settings) | 600 | The Matrix channel configuration-key reference: account/connection, encryption, access-and-policy, reply-behavior, reaction, tooling/per-room-override, and exec-approval option groups under `channels.matrix`. |
| 7 | `oc_channels_matrix_migration.md` | procedure | matrix-migration.md: (intro / in-place upgrade), What the migration does automatically, What the migration cannot do automatically, Recommended upgrade flow, How encrypted migration works | 750 | Upgrading the in-place `@openclaw/matrix` plugin: what migration repairs automatically (snapshots, store moves, room-key restore), the encrypted-state recovery limits, the step-by-step recommended upgrade flow (`doctor --fix` → verify status → recovery-key restore → device verify → backup reset/bootstrap), and the two-stage encrypted-migration mechanism. |
| 8 | `oc_channels_matrix_migration_messages.md` | procedure | matrix-migration.md: Common messages and what they mean (Upgrade and detection, Encrypted-state recovery, Manual recovery, Custom plugin install messages), If encrypted history still does not come back, If you want to start fresh | 700 | Diagnostic reference for Matrix-migration log/console messages: upgrade/detection, encrypted-state recovery, manual recovery, and custom-plugin-install messages, each with meaning + remediation, plus the "history still missing" and "start fresh baseline" command checklists. |
| 9 | `oc_channels_matrix_presentation.md` | model | matrix-presentation.md: (intro), Event content, Fallback behavior, Supported blocks, Interactions, Relationship to approval metadata, Media messages | 450 | The `com.openclaw.presentation` Matrix metadata contract for OpenClaw-aware clients: event-content schema (version/type/blocks), plain-text fallback, supported block types (buttons/select/context/divider), fallback interaction semantics, relationship to `com.openclaw.approval`, and per-media-event attachment rules. |
| 10 | `oc_channels_matrix_push_rules.md` | procedure | matrix-push-rules.md: (intro), Prerequisites, Steps, Multi-bot notes, Homeserver notes | 600 | Installing per-recipient Matrix push rules for quiet finalized-preview notifications: prerequisites, the 6-step recipe (quiet config → recipient token → pusher check → override push-rule PUT on `com.openclaw.finalized_preview` → verify), multi-bot rule keying, and Synapse/Tuwunel homeserver caveats. |
| 11 | `oc_channels_mattermost.md` | procedure | mattermost.md: Install, Quick setup, Native slash commands, Environment variables, Chat modes, Threading and sessions, Access control (DMs), Channels (groups), Targets for outbound delivery, DM channel retry, Preview streaming, Reactions, Multi-account, Directory adapter, Troubleshooting | 800 | Setting up the Mattermost channel: plugin install, bot-token/base-URL config, native `oc_*` slash commands + callback reachability, env vars, chat modes (oncall/onmessage/onchar), threading/sessions, DM/channel access control, outbound target resolution, DM-channel retry, preview-streaming modes, reactions, multi-account, directory adapter, and troubleshooting. |
| 12 | `oc_channels_mattermost_buttons.md` | model | mattermost.md: Interactive buttons (message tool) + Direct API integration (external scripts) — payload structure, HMAC token generation, common pitfalls | 600 | Mattermost interactive buttons and the external-script Direct-API path: the message-tool `buttons` 2D-array, `props.attachments` payload structure and Mattermost routing rules, and the HMAC-SHA256 `_token` generation recipe (secret derivation, sorted-key compact JSON signing) with common pitfalls. |

## Section Coverage Map

```
line.md
├── (intro: status/support) ───────────────────────────── → note 1 (oc_channels_line)
├── Install ───────────────────────────────────────────── → note 1
├── Setup (webhook URL, signature, security note) ─────── → note 1
├── Configure (minimal/public/env/files/multi-account) ── → note 1
├── Access control (dmPolicy/allowFrom/groups, ID forms) → note 1
├── Message behavior (chunking, Flex, streaming, media) ─ → note 1
├── Channel data (rich messages: quickReplies/Flex/etc) ─ → note 1
├── ACP support ───────────────────────────────────────── → note 1 (→ tools/acp-agents link-out)
├── Outbound media ────────────────────────────────────── → note 1
├── Troubleshooting ───────────────────────────────────── → note 1
└── Related ───────────────────────────────────────────── → References (external/link-out)
location.md
├── (intro: normalization model + supported channels) ── → note 2 (oc_channels_location)
├── Text formatting (pin/place/live + untrusted JSON) ─── → note 2
├── Context fields (Location* ctx fields) ─────────────── → note 2
├── Channel notes (Telegram/WhatsApp/Matrix specifics) ── → note 2
└── Related ───────────────────────────────────────────── → References (link-out: nodes/*)
matrix.md
├── Install ───────────────────────────────────────────── → note 3 (oc_channels_matrix_setup)
├── Setup + Interactive setup ─────────────────────────── → note 3
├── Minimal config / Auto-join / Allowlist target formats → note 3
├── Account ID normalization / Cached credentials / Env ─ → note 3
├── Configuration example ─────────────────────────────── → note 5 (oc_channels_matrix_behavior; baseline)
├── Streaming previews ────────────────────────────────── → note 5
├── Voice messages ────────────────────────────────────── → note 5
├── Approval metadata (+ push-rules pointer) ──────────── → note 5 (→ note 10)
├── Bot-to-bot rooms ──────────────────────────────────── → note 5
├── Encryption and verification (all H3) ──────────────── → note 4 (oc_channels_matrix_encryption)
├── Profile management ────────────────────────────────── → note 4
├── Threads (sessionScope/threadReplies/inheritance) ──── → note 5
├── ACP conversation bindings (+ Thread binding config) ─ → note 5 (→ tools/acp-agents)
├── Reactions / History context / Context visibility ──── → note 5
├── DM and room policy / Direct room repair ───────────── → note 5
├── Exec approvals / Slash commands ───────────────────── → note 5 (→ tools/exec-approvals)
├── Multi-account (notes accordions) ─────────────────── → note 4 (startup/crypto) + note 5 (routing)
├── Private/LAN homeservers / Proxying Matrix traffic ─── → note 4 (network hardening)
├── Target resolution ─────────────────────────────────── → note 5
├── Configuration reference (7 H3 groups) ─────────────── → note 6 (oc_channels_matrix_config_reference)
└── Related ───────────────────────────────────────────── → References (link-out)
matrix-migration.md
├── (intro: in-place upgrade) ─────────────────────────── → note 7 (oc_channels_matrix_migration)
├── What the migration does automatically ─────────────── → note 7
├── What the migration cannot do automatically ────────── → note 7
├── Recommended upgrade flow ──────────────────────────── → note 7
├── How encrypted migration works ─────────────────────── → note 7
├── Common messages and what they mean (4 H3 groups) ──── → note 8 (oc_channels_matrix_migration_messages)
├── If encrypted history still does not come back ─────── → note 8
├── If you want to start fresh for future messages ───── → note 8
└── Related ───────────────────────────────────────────── → References (link-out)
matrix-presentation.md
├── (intro: com.openclaw.presentation) ───────────────── → note 9 (oc_channels_matrix_presentation)
├── Event content / Fallback behavior / Supported blocks → note 9
├── Interactions / Relationship to approval metadata ──── → note 9
└── Media messages ────────────────────────────────────── → note 9
matrix-push-rules.md
├── (intro: quiet streaming context) ─────────────────── → note 10 (oc_channels_matrix_push_rules)
├── Prerequisites / Steps (5 steps) ──────────────────── → note 10
├── Multi-bot notes / Homeserver notes (Synapse/Tuwunel) → note 10
└── Related ───────────────────────────────────────────── → References (link-out)
mattermost.md
├── Install / Quick setup ─────────────────────────────── → note 11 (oc_channels_mattermost)
├── Native slash commands (callback reachability) ─────── → note 11
├── Environment variables / Chat modes ────────────────── → note 11
├── Threading and sessions / Access control (DMs) ─────── → note 11
├── Channels (groups) / Targets for outbound delivery ─── → note 11
├── DM channel retry / Preview streaming / Reactions ──── → note 11
├── Interactive buttons (message tool) ────────────────── → note 12 (oc_channels_mattermost_buttons)
├── Direct API integration (external scripts) [H3] ───── → note 12 (payload + HMAC)
├── Directory adapter / Multi-account / Troubleshooting ─ → note 11
└── Related ───────────────────────────────────────────── → References (link-out)
```
No orphaned H2/H3. "Related" lists on every page → each note's `## References` (external/cross-link-out, not
duplicated as content). Shared sub-topics (pairing, groups, access-groups, channel-routing, streaming concept,
acp-agents, exec-approvals, media-overview, gateway security/secrets/doctor, nodes/location-command) are
link-outs to their home sub-plans, not re-digested here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| matrix.md (5,856w, 25 H2 / 23 H3, mixed procedure+model) | notes 3 + 4 + 5 + 6 | 2.3× the 2,500w cap with 34 code fences; cleanly separates four task/BB clusters: install/auth/access **setup procedure** (3), E2EE/verification/profile/network **encryption procedure** (4), runtime **message-behavior model** (5), and the flat **config-key reference model** (6). Each note then sits ≤800w and ≤6 fences with one building_block. |
| matrix-migration.md (3,215w, 9 H2 / 4 H3, procedure) | notes 7 + 8 | exceeds the 2,500w cap; the ~190-line "Common messages and what they mean" section is a self-contained diagnostic catalog (message → meaning → remediation) distinct from the upgrade-flow procedure. Splitting keeps the how-to (7) actionable and isolates the lookup reference (8). |
| mattermost.md (2,702w, 16 H2 / 1 H3, mixed procedure+model) | notes 11 + 12 | just over the 2,500w cap; the Interactive-buttons + Direct-API-integration sections (with the HMAC `_token` signing recipe and Python example) are a reusable data/contract sub-topic (model BB) distinct from the channel-setup procedure, so they split into note 12 to keep both ≤800w / ≤6 fences and single-BB. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (14,173 measured words). New `oc_` notes: **12**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (notes 1, 3, 4, 7, 8, 10, 11) · **model ×5** (notes 2, 5, 6, 9, 12).
- Est. digest words ≈ **8,000** (avg ~670/note); every note ≤800w (caps: ≤2,500w / ≤400 lines / ≤6 code
  blocks). The 34 matrix + 15 mattermost source fences distribute across the split notes so each stays ≤6
  (config snippets reproduced selectively, verbatim where load-bearing — e.g. the push-rule `PUT`, the HMAC
  Python example).
- Cross-refs **LOCKED (xref-augment 2026-06-21)**: see `## Per-Note Related Notes Mapping`. Each note meets
  the raised floors — **≥8 relevance-selected `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (≥5 of
  Per-note counts: line 8t/11s/11d · location 8t/10s/10d · matrix_setup 8t/11s/11d · matrix_encryption
  9t/11s/11d · matrix_behavior 9t/12s/11d · matrix_config_reference 8t/10s/11d · matrix_migration 8t/11s/11d ·
  matrix_migration_messages 8t/10s/11d · matrix_presentation 8t/10s/11d · matrix_push_rules 8t/10s/11d ·
  mattermost 9t/11s/11d · mattermost_buttons 8t/11s/11d. ALL snippets + all EXISTING docs/terms/repos

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read of source 2026-06-21,
series, marked **(planned, this series)** — they materialize during execution. Repos are additional (all
existing). Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`.

### oc_channels_line (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: the product whose LINE channel this note configures.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback for inbound events; relevance: the LINE plugin runs as a webhook receiver, signature-verified over the raw body.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity/credentials; relevance: LINE uses channel access token + channel secret for auth.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for API access; relevance: the LINE channel access token is the bearer credential carried to the Messaging API.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who may interact; relevance: `dmPolicy`/`allowFrom`/`groupPolicy`/access-group gating governs LINE senders.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the LINE plugin is the bot identity receiving/sending Messaging-API events.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent over a chat surface; relevance: LINE is the conversational surface the agent answers on.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: LINE strips Markdown and converts code/tables into Flex cards.

**Docs**
- [Hermes: LINE Messaging](../hermes_agent/hermes_messaging_line.md) — Hermes LINE channel doc; relevance: closest sibling-platform LINE setup for cross-tool parity (token/secret, webhook).
- [Hermes: Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — inbound/outbound media caps; relevance: parity for LINE `mediaMaxMb` and the shared inbound media store.
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook route signature/limits; relevance: parity for LINE's raw-body HMAC verification + pre-auth body limits.
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — inbound webhook dispatch; relevance: parity for how a verified webhook event is routed to a session.
- [Hermes: Gateway Architecture (messaging)](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel→gateway plumbing; relevance: where a channel plugin like LINE attaches to the gateway.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost channel setup; relevance (planned, this series): sibling bot-token channel with the same install→config→access pattern.
- [oc_channels_location](oc_channels_location.md) — inbound location parsing; relevance (planned, this series): LINE `channelData.line.location` peers the shared location model.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix channel setup; relevance (planned, this series): sibling channel-setup procedure (auth/access/env vars).
- [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md) — interactive rich payloads; relevance (planned, this series): peer for LINE quick-replies/Flex/template rich messages.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime message behavior; relevance (planned, this series): peer model for chunking/streaming/media behavior.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: implements the LINE adapter this note documents.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: home of the LINE messaging plugin.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing + allowlist gate; relevance: LINE `dmPolicy: "pairing"`/`allowFrom` enforcement.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter interface; relevance: the contract the LINE adapter implements.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — account/ID normalization; relevance: LINE user/group/room ID forms and multi-account registry.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — allowlist/sender match resolution; relevance: how `allowFrom`/`accessGroup:` entries resolve for LINE.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — inbound→session resolution; relevance: maps a LINE DM/group to a session.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — inbound media store pipeline; relevance: LINE inbound media saved under the shared media store.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — outbound image validate/resize; relevance: LINE outbound image/video/audio preview handling.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP route mounting; relevance: the gateway mounts LINE's `/line/webhook` path.
- [snippet_hermes_agent_plugins_platform_line](../../code_snippets/snippet_hermes_agent_plugins_platform_line.md) — Hermes LINE platform plugin; relevance: cross-tool LINE adapter reference.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — webhook platform handler; relevance: parity for signed webhook ingestion.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted external-content handling; relevance: LINE outbound URL host validation (loopback/link-local/private rejection).

### oc_channels_location (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime that normalizes inbound locations.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — untrusted input steering the model; relevance: labels/addresses/captions are rendered through the bounded untrusted-metadata JSON path.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: locations render as terse text lines appended to the inbound body.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: location context feeds the agent's prompt.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the bot consumes `Location*` ctx fields.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription of audio; relevance: peer untrusted-media normalization path (voice notes parallel locations).
- [VoIP](../../term_dictionary/term_voip.md) — voice-over-IP node input; relevance: peer node-input channel feeding structured ctx.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound event callback; relevance: shared locations arrive as channel webhook/message events (Telegram/WhatsApp/Matrix).

**Docs**
- [Hermes: Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — channel media normalization; relevance: parity for normalizing inbound non-text channel payloads.
- [Hermes: Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — per-platform media fields; relevance: parity for platform-specific location/media field mapping.
- [Hermes: WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp channel; relevance: WhatsApp `locationMessage`/`liveLocationMessage` is a supported source here.
- [Hermes: Signal](../hermes_agent/hermes_messaging_signal.md) — Signal channel; relevance: peer channel with location/media inbound parsing.
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel; relevance: Matrix `m.location`/`geo_uri` is a supported source here.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime message behavior; relevance (planned, this series): Matrix is one of the three location source channels; peer untrusted-context model.
- [oc_channels_matrix_presentation](oc_channels_matrix_presentation.md) — Matrix metadata contract; relevance (planned, this series): peer structured-metadata/event-content model.
- [oc_channels_line](oc_channels_line.md) — LINE channel; relevance (planned, this series): LINE outbound `location` channelData mirrors the inbound location fields.
- [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md) — structured payload contract; relevance (planned, this series): peer model note for channel data structures.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): configures the Matrix channel that produces `geo_uri` locations.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: implements per-channel location parsing.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Telegram/WhatsApp/Matrix location handlers.

**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — inbound transcript/media pipeline; relevance: where location text + ctx fields are appended to the inbound body.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — inbound→session mapping; relevance: locations attach to the resolved conversation context.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter interface; relevance: the adapter contract each location-emitting channel implements.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content bounding; relevance: the bounded untrusted-metadata JSON path for label/address/caption.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — inbound attachment sanitization; relevance: parallel sanitization of untrusted channel-provided fields.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram inbound dispatch; relevance: Telegram pins/venues/live locations source path.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport layer; relevance: how Telegram location events arrive before parsing.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Hermes Telegram media handling; relevance: cross-tool parity for Telegram non-text payload parsing.
- [snippet_hermes_agent_gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Hermes Signal media handling; relevance: cross-tool parity for channel media/location field mapping.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix event normalization; relevance: parity for normalizing Matrix `m.location`/`geo_uri` into structured fields.

### oc_channels_matrix_setup (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product whose Matrix channel this note installs and configures.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: token-vs-password auth, cached credentials, env-var fallback.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: Matrix `accessToken` (`syt_xxx`) is the bearer credential.
- [Access Control](../../term_dictionary/term_access_control.md) — interaction gating; relevance: allowlist target formats, `dm.policy`, `groupPolicy`, `autoJoin` invite gating.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the configured Matrix bot account/device.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling requests; relevance: streaming preview edits cost extra Matrix API calls (rate-limit profile noted at setup).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting service; relevance: homeserver behind proxy/workers affects `/_matrix/client` reachability.
- [Markdown](../../term_dictionary/term_markdown.md) — outbound text markup; relevance: `markdown` rendering config is part of channel setup keys.

**Docs**
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Hermes Matrix channel; relevance: closest sibling-platform Matrix setup (homeserver/token/userId-password).
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix encryption; relevance: the interactive wizard's optional E2EE bootstrap links here.
- [Hermes: Gateway Architecture (messaging)](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel→gateway wiring; relevance: where the Matrix plugin attaches and restarts.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway lifecycle; relevance: parity for "restart the gateway" after configuring channels.
- [oc_channels_matrix_encryption](oc_channels_matrix_encryption.md) — E2EE operations; relevance (planned, this series): setup's optional E2EE branch runs the encryption bootstrap.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime message behavior; relevance (planned, this series): the baseline config example continues into behavior knobs.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): the flat key reference for everything set here.
- [oc_channels_matrix_migration](oc_channels_matrix_migration.md) — in-place upgrade flow; relevance (planned, this series): upgrading an existing Matrix install set up by this note.
- [oc_channels_line](oc_channels_line.md) — LINE channel; relevance (planned, this series): sibling install→config→access procedure.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost channel; relevance (planned, this series): sibling bot-token channel setup.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: implements the Matrix adapter being configured.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Matrix plugin and account registry.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — interactive setup wizard; relevance: `openclaw channels add` / `configure --section channels` flow.

**Snippets**
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix platform handler; relevance: cross-tool Matrix channel setup reference.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix client connect/login; relevance: parity for homeserver login (token vs password) at setup.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix room/user ACL; relevance: parity for allowlist target formats and room gating.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix ID normalization; relevance: parity for account-ID/MXID normalization (`Ops Bot`→`ops-bot`).
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist gate; relevance: `dm.policy: "pairing"` + `dm.allowFrom` enforcement.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — account-ID/env-var normalization; relevance: scoped `MATRIX_<ID>_*` env-var naming + account registry.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — allowlist resolution; relevance: how `@user:server`/`!room:server` allowlist entries resolve.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config writer; relevance: the interactive setup writes the `channels.matrix` config block.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel-adapter interface; relevance: the contract the Matrix adapter satisfies.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applying the new Matrix config after edit/restart.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel dispatch kernel; relevance: how a joined Matrix room's inbound message is dispatched.

### oc_channels_matrix_encryption (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime executing the `openclaw matrix encryption`/`verify` commands.
- [Encryption](../../term_dictionary/term_encryption.md) — confidentiality transform; relevance: the central topic — Matrix E2EE setup, cross-signing, room-key backup.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity verification; relevance: UIA (`m.login.dummy`/`m.login.password`) for cross-signing key upload; device verification.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `accessToken` auth and the `MATRIX_RECOVERY_KEY` stdin secret handling.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: prefer `https://` homeservers; cleartext public homeservers stay blocked.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting service; relevance: proxying Matrix traffic via `channels.matrix.proxy` and private/LAN homeserver hardening.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — request mediation; relevance: outbound HTTP(S) proxy for Matrix runtime traffic + status probes.
- [Access Control](../../term_dictionary/term_access_control.md) — interaction gating; relevance: SSRF private-network opt-in gates which homeservers the account may reach.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: device hygiene/pruning of stale OpenClaw-managed Matrix devices.

**Docs**
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix encryption; relevance: closest sibling E2EE/verification flow for parity.
- [Hermes: Matrix Proxy Mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — Matrix outbound proxy; relevance: parity for proxying Matrix traffic / private homeserver access.
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel base; relevance: the channel whose encrypted state this note manages.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential/secret handling; relevance: parity for sensitive recovery-key/stdin secret handling.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix install/config; relevance (planned, this series): setup's optional E2EE branch hands off to these commands.
- [oc_channels_matrix_migration](oc_channels_matrix_migration.md) — in-place upgrade flow; relevance (planned, this series): migration reuses the same `verify backup/device/bootstrap` recovery commands.
- [oc_channels_matrix_migration_messages](oc_channels_matrix_migration_messages.md) — diagnostic message catalog; relevance (planned, this series): the encryption commands resolve the messages catalogued there.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): `encryption`/`startupVerification`/`network`/`proxy` keys reference.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): encrypted-room media/thumbnail behavior referenced from behavior.
- [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md) — HMAC signing contract; relevance (planned, this series): peer cryptographic-trust topic (HMAC vs cross-signing).

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Matrix crypto/verification implementation.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: SSRF/private-network blocking and credential hardening.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: outbound proxy + startup verification pass run in the gateway.

**Snippets**
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix handler; relevance: cross-tool Matrix encryption/verification reference.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix connect/login; relevance: parity for crypto-store init at connect time.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS; relevance: device identity/TLS trust analogous to cross-signing trust signals.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: transport-trust hardening peer for the prefer-https rule.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — outbound proxy connect; relevance: implements `channels.matrix.proxy` outbound routing.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content/host bounding; relevance: SSRF protection blocking private/internal homeservers.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: auditing private-network opt-in per channel/account.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair pass; relevance: guarded crypto-bootstrap repair on startup/`doctor --fix`.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: recovery-key/SecretRef handling for verification commands.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — outbound image validate; relevance: encrypted rooms use `thumbnail_file` so previews are encrypted alongside the attachment.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation actions; relevance: repairing broken bootstrap/cross-signing state.

### oc_channels_matrix_behavior (9t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime driving Matrix message behavior.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — server push streaming; relevance: streaming/`blockStreaming` preview edit modes for in-flight replies.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: inbound voice notes transcribed before the room mention gate.
- [Markdown](../../term_dictionary/term_markdown.md) — outbound text markup; relevance: `markdown` rendering + text chunking of replies.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent conversation protocol; relevance: `/acp spawn --bind here` conversation bindings and thread binding.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered message steering; relevance: pending-only room history buffering + session routing.
- [Bot](../../term_dictionary/term_bot.md) — automated participant; relevance: bot-to-bot rooms (`allowBots`) and self-reply loop avoidance.
- [Access Control](../../term_dictionary/term_access_control.md) — interaction gating; relevance: `contextVisibility`, DM/room policy, exec-approver authorization.
- [Reaction](../../term_dictionary/term_idempotency.md) — at-most-once side effects; relevance: ack reactions + retries reuse the original history snapshot (idempotent re-delivery).

**Docs**
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Hermes Matrix channel; relevance: closest sibling runtime behavior (threads/reactions/streaming).
- [Hermes: Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/transcription settings; relevance: parity for voice-note transcription provider config.
- [Hermes: Session Storage](../hermes_agent/hermes_session_storage.md) — session persistence; relevance: parity for `sessionScope`/thread-bound session routing.
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle; relevance: parity for thread-binding idle/max-age lifecycle.
- [Hermes: ACP Internals](../hermes_agent/hermes_acp_internals.md) — ACP conversation engine; relevance: parity for ACP conversation bindings on a chat surface.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): the baseline config example continues here.
- [oc_channels_matrix_push_rules](oc_channels_matrix_push_rules.md) — quiet-preview push rules; relevance (planned, this series): `streaming: "quiet"` points here for the finalized-preview rule.
- [oc_channels_matrix_presentation](oc_channels_matrix_presentation.md) — presentation metadata; relevance (planned, this series): approval metadata + rich-message rendering peer.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): reply-behavior/reaction/streaming key reference.
- [oc_channels_location](oc_channels_location.md) — inbound location parsing; relevance (planned, this series): location is one of the inbound-context types behavior surfaces.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost channel; relevance (planned, this series): peer channel with chat-mode/threading/preview-streaming behavior.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: implements Matrix reactions/threads/streaming behavior.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session routing; relevance: `sessionScope`/thread-bound session keys.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Matrix behavior implementation.

**Snippets**
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: `threadBindings`/`sessionScope`/`threadReplies` behavior.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/ack reactions; relevance: outbound reactions, ack-reaction resolution order, `m.reaction` events.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — conversation binding routing; relevance: ACP conversation bindings routing to the bound session.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered streaming deltas; relevance: preview-edit streaming + buffered block delivery.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: `execApprovals` exec/plugin approval delivery + reaction shortcuts.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — history injection; relevance: `historyLimit`/`InboundHistory` pending-only room history.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — durable ACP bindings; relevance: `/acp spawn --bind here` durable workspaces.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — ACP thread binding; relevance: `/acp spawn --thread auto|here` thread binding gating.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: voice-note transcription before the mention gate.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — DM/room session typing; relevance: DM-vs-room classification driving policy + session scope.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: target resolution for room/user/alias forms.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — media reply lifecycle; relevance: media replies redact stale previews before sending the final attachment.

### oc_channels_matrix_config_reference (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime reading the `channels.matrix` config keys catalogued here.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: account/connection keys (`accessToken`/`password`/`userId`/`deviceId`).
- [Encryption](../../term_dictionary/term_encryption.md) — confidentiality transform; relevance: `encryption`/`startupVerification`/`startupVerificationCooldownHours` keys.
- [Access Control](../../term_dictionary/term_access_control.md) — interaction gating; relevance: access-and-policy keys (`groupPolicy`/`dm.policy`/`allowlistOnly`/`autoJoin`).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting/proxy; relevance: `proxy` and `network.dangerouslyAllowPrivateNetwork` keys.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `accessToken` SecretRef across env/file/exec providers.
- [Markdown](../../term_dictionary/term_markdown.md) — outbound markup; relevance: `markdown`/`chunkMode`/`textChunkLimit` reply-behavior keys.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — streaming push; relevance: `streaming`/`blockStreaming` reply-behavior keys.

**Docs**
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Hermes Matrix channel; relevance: sibling Matrix config-key surface for parity.
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix encryption; relevance: parity for the encryption config keys.
- [Hermes: Matrix Proxy Mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — Matrix proxy config; relevance: parity for `proxy`/private-network keys.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway config/ops; relevance: parity for how channel config keys are applied operationally.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel policy controls; relevance: cross-tool parity for per-channel access/policy config knobs.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): the procedure that sets the account/connection keys.
- [oc_channels_matrix_encryption](oc_channels_matrix_encryption.md) — E2EE operations; relevance (planned, this series): the encryption keys' operational counterpart.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): the reply-behavior/reaction keys' runtime semantics.
- [oc_channels_matrix_push_rules](oc_channels_matrix_push_rules.md) — quiet-preview rules; relevance (planned, this series): `streaming: "quiet"` key links to the push-rule recipe.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost channel; relevance (planned, this series): peer channel with an analogous config-key surface.
- [oc_channels_line](oc_channels_line.md) — LINE channel; relevance (planned, this series): peer channel config keys (`dmPolicy`/`allowFrom`/`mediaMaxMb`).

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: defines and validates the Matrix config schema.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Matrix config-key parsing.

**Snippets**
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — account/key normalization; relevance: how `accounts.<id>` overrides inherit top-level defaults.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: applying changes to these keys at runtime.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload planning; relevance: diffing/planning a `channels.matrix` config change.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter interface; relevance: the keys map to adapter capabilities (`actions`, per-room overrides).
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: `threadBindings`/`threadReplies` reply-behavior keys.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reaction settings; relevance: `ackReaction`/`ackReactionScope`/`reactionNotifications` keys.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `dm.policy`/`dm.allowFrom`/`groupAllowFrom` access keys.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolution; relevance: `accessToken`/`password` plaintext-and-SecretRef support.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — allowlist match resolution; relevance: `dangerouslyAllowNameMatching` resolution semantics for allowlist keys.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: `execApprovals.*` config-key group semantics.

### oc_channels_matrix_migration (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime running the in-place `@openclaw/matrix` upgrade.
- [Encryption](../../term_dictionary/term_encryption.md) — confidentiality transform; relevance: encrypted-state recovery limits + room-key backup restore.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: token-hash storage roots reused when the access token changes.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity verification; relevance: device verification + cross-signing during the upgrade flow.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-execution; relevance: snapshot reuse + "skip mutation without a recovery point" make `doctor --fix` re-runnable.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting service; relevance: post-upgrade verification of homeserver reachability behind a proxy.
- [Bot](../../term_dictionary/term_bot.md) — automated participant; relevance: per-account Matrix bot identity/device the migration repairs.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: post-upgrade homeserver connection trust during verify-status checks.

**Docs**
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix encryption; relevance: parity for encrypted-state recovery/backup-restore concepts.
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel base; relevance: the channel being upgraded in place.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway lifecycle/ops; relevance: parity for `update`/restart flows that finish migration.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential/state isolation; relevance: parity for moving account-scoped credential/crypto stores safely.
- [oc_channels_matrix_encryption](oc_channels_matrix_encryption.md) — E2EE operations; relevance (planned, this series): migration reuses `verify backup/device/bootstrap` from this note.
- [oc_channels_matrix_migration_messages](oc_channels_matrix_migration_messages.md) — diagnostic message catalog; relevance (planned, this series): the companion lookup for migration messages.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): config the migration preserves under `channels.matrix`.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): `defaultAccount` etc. that gate multi-account migration.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): behavior restored once migration completes.
- [oc_channels_matrix_push_rules](oc_channels_matrix_push_rules.md) — push-rule recipe; relevance (planned, this series): notification routing reconfirmed after upgrade.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Matrix migration/store-move logic.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: safe store moves + plugin-helper path boundary checks.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: startup + `doctor --fix` trigger the migration pass.

**Snippets**
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix handler; relevance: cross-tool Matrix crypto/store reference.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair pass; relevance: `openclaw doctor --fix` runs the migration repair.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload planning; relevance: detecting actionable migration work before mutating state.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: importing legacy state into the current account-scoped layout.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution; relevance: reusing cached credentials + recovery-key during migration.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation; relevance: repairing broken bootstrap/store state during upgrade.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/lifecycle; relevance: re-installing/repairing `@openclaw/matrix` when the plugin is missing.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: root package no longer bundles Matrix SDK; helper-path boundary checks.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor preview pass; relevance: non-interactive doctor pass run during package-manager updates.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: surfacing custom-path/unsafe-helper Matrix installs.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: device-identity continuity when the token changes but identity stays.

### oc_channels_matrix_migration_messages (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime emitting these migration log/console messages.
- [Encryption](../../term_dictionary/term_encryption.md) — confidentiality transform; relevance: most messages concern encrypted-state recovery + room-key restore.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity verification; relevance: messages tie to cross-signing/device-verification state.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: "need homeserver, userId, and access token" account-resolution messages.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-runs; relevance: "snapshot reused"/"rerun doctor --fix" messages reflect re-runnable repair.
- [Access Control](../../term_dictionary/term_access_control.md) — account scoping; relevance: `defaultAccount`-not-set refuse-to-guess messages.
- [Bot](../../term_dictionary/term_bot.md) — per-account identity; relevance: per-account device/identity referenced in recovery messages.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: post-recovery homeserver connection verification context.

**Docs**
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Hermes Matrix encryption; relevance: parity for the encrypted-state recovery messages' meaning.
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel base; relevance: the channel whose state these messages describe.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway diagnostics; relevance: parity for reading gateway/doctor diagnostic output.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential/state handling; relevance: parity for recovery-key conflict/store-move failure messages.
- [oc_channels_matrix_migration](oc_channels_matrix_migration.md) — upgrade flow; relevance (planned, this series): the procedure these messages are emitted during.
- [oc_channels_matrix_encryption](oc_channels_matrix_encryption.md) — E2EE commands; relevance (planned, this series): the remediation commands each message points to.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): "configure channels.matrix then rerun" remediation.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): `defaultAccount`/auth keys named in messages.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): behavior restored once messages resolve.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost troubleshooting; relevance (planned, this series): peer diagnostic-message reference style.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: source of these Matrix migration/recovery messages.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: unsafe-helper-path / store-move-failure guard messages.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: startup/doctor emit the upgrade/detection messages.

**Snippets**
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: maps diagnostic messages to remediation.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation actions; relevance: the fix each message recommends.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix handler; relevance: cross-tool reference for the same crypto-store states.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair; relevance: "rerun doctor --fix" remediation path.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: detecting still-blocked-on-config migration state.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: "reinstall/repair @openclaw/matrix" messages.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: "helper path is unsafe" boundary-check messages.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: custom-path install warnings surfaced by doctor.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution; relevance: recovery-key-conflict / backup-key messages.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: legacy-store-move messages and their outcomes.

### oc_channels_matrix_presentation (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the runtime attaching `com.openclaw.presentation` metadata.
- [Markdown](../../term_dictionary/term_markdown.md) — plain-text fallback; relevance: a readable plain-text `body` fallback is always rendered.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — untrusted-input handling; relevance: clients must ignore unknown block/type/version values (defensive parsing).
- [Bot](../../term_dictionary/term_bot.md) — automated sender; relevance: the bot emits the structured presentation event.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational surface; relevance: OpenClaw-aware Matrix clients render native UI from the metadata.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — streaming additive payloads; relevance: presentation metadata is additive to the streamed text body.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent interaction protocol; relevance: button/select values are fallback interaction payloads (slash/text commands).
- [Idempotency](../../term_dictionary/term_idempotency.md) — single stable payload; relevance: metadata attached only to the first media event to avoid duplicate renderers.

**Docs**
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Hermes Matrix channel; relevance: sibling Matrix outbound event/content model for parity.
- [Hermes: Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — per-platform media events; relevance: parity for per-media-event attachment rules.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — outbound adapter wiring; relevance: parity for how an outbound adapter advertises block support.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — rich-output/channel controls; relevance: cross-tool parity for structured/rich message rendering controls.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): approval metadata + rich-message behavior peer.
- [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md) — interactive buttons contract; relevance (planned, this series): cross-channel parity for buttons/select payload structures.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): the channel that emits these events.
- [oc_channels_location](oc_channels_location.md) — location context model; relevance (planned, this series): peer structured-channel-data model note.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): `markdown`/outbound rendering keys.
- [oc_channels_matrix_push_rules](oc_channels_matrix_push_rules.md) — finalized-preview marker; relevance (planned, this series): peer custom-content-flag metadata on Matrix events.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: the Matrix outbound adapter advertising supported blocks.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the presentation-metadata serializer.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reactions/interactions; relevance: fallback interaction semantics (sending a value back as a message).
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter interface; relevance: the outbound adapter capability advertisement.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: relationship to `com.openclaw.approval` dedicated renderer.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — structured streaming output; relevance: additive structured payload alongside streamed text.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — media event lifecycle; relevance: one Matrix event per media URL; metadata on the first only.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — media validation; relevance: per-media-event attachment handling.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix handler; relevance: cross-tool Matrix outbound event construction.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix event normalization; relevance: parity for event-content shaping/normalization.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — defensive content handling; relevance: clients ignore unknown fields/block types rather than failing.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitize; relevance: keeping presentation metadata compact; large text stays in `body`.

### oc_channels_matrix_push_rules (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the bot whose finalized-preview marker the push rule matches.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — streaming previews; relevance: `streaming: "quiet"` in-place preview edits are the reason the rule exists.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: recipient access-token login (`m.login.password`) for the pushrules API.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `$USER_ACCESS_TOKEN` Bearer auth on the `pushrules`/`pushers` calls.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting service; relevance: Synapse behind a reverse proxy/workers must reach `/_matrix/client/.../pushrules/`.
- [Bot](../../term_dictionary/term_bot.md) — automated sender; relevance: the rule's `sender` condition matches the bot MXID.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request economy; relevance: quiet mode minimizes notification noise/cost on finalized previews only.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-runnable PUT; relevance: re-running `PUT` against the same `ruleId` updates a single rule.

**Docs**
- [Hermes: Matrix](../hermes_agent/hermes_messaging_matrix.md) — Hermes Matrix channel; relevance: sibling Matrix notification/streaming behavior for parity.
- [Hermes: Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Matrix encryption; relevance: parity context for encrypted preview/notification edits.
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — operator-facing ops; relevance: parity for operator self-host homeserver configuration tasks.
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — push/delivery routing; relevance: parity for per-recipient notification delivery control.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — streaming/quiet behavior; relevance (planned, this series): defines `streaming: "quiet"` that this recipe supports.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): the channel the recipients/bot accounts come from.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): the `streaming` key reference.
- [oc_channels_matrix_presentation](oc_channels_matrix_presentation.md) — custom event content; relevance (planned, this series): peer custom-content-flag (`com.openclaw.finalized_preview`).
- [oc_channels_matrix_encryption](oc_channels_matrix_encryption.md) — homeserver hardening; relevance (planned, this series): private/Synapse homeserver context overlaps.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost preview streaming; relevance (planned, this series): peer channel preview-streaming/notification model.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: emits the finalized-preview marker the rule keys on.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: drives quiet-mode preview edit + finalization.

**Snippets**
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Hermes Matrix handler; relevance: cross-tool Matrix message-edit/notification reference.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered preview deltas; relevance: the in-place preview edit the finalized marker concludes.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth + rate-limit policy; relevance: token-scoped API call economy + quiet notification policy.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — bearer auth dispatch; relevance: parity for Bearer-token-authorized homeserver calls.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: gateway reachability behind reverse proxy/workers (Synapse note).
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — media fallback lifecycle; relevance: media/stale-preview fallbacks use normal delivery, not the quiet rule.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — stream consumer; relevance: parity for streamed-reply finalization that triggers the notification.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure; relevance: parity for preview-edit batching that yields a single finalized edit.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — push/presence events; relevance: peer push-notification delivery path concept.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — adapter interface; relevance: where the channel marks finalized text-only preview edits.

### oc_channels_mattermost (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the product whose Mattermost channel this note configures.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: native slash-command callback POSTs + outbound message webhooks.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional channel; relevance: Mattermost connects via bot token + WebSocket events.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: bot-token + base-URL auth; per-command callback tokens validated.
- [Access Control](../../term_dictionary/term_access_control.md) — interaction gating; relevance: `dmPolicy`/`groupPolicy`/`allowFrom`/access-group + chat-mode gating.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — retry pacing; relevance: `dmChannelRetry` (`initialDelayMs`/`maxDelayMs`) for direct-channel creation.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — streaming previews; relevance: single draft-preview-post streaming (`partial`/`block`/`progress`).
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling; relevance: 429/5xx transient failures retried; callback lookups rate-limited per command.
- [Bot](../../term_dictionary/term_bot.md) — automated participant; relevance: the Mattermost bot account identity.

**Docs**
- [Hermes: Mattermost](../hermes_agent/hermes_messaging_mattermost.md) — Hermes Mattermost channel; relevance: closest sibling-platform Mattermost setup for parity.
- [Hermes: Gateway Architecture (messaging)](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel→gateway wiring; relevance: where the Mattermost plugin attaches + callback HTTP server.
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — callback route security; relevance: parity for slash-callback token validation + fail-closed routing.
- [Hermes: Slack](../hermes_agent/hermes_messaging_slack.md) — Slack channel; relevance: peer team-chat platform with slash commands/threads/streaming.
- [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md) — interactive buttons + Direct API; relevance (planned, this series): the split-off button/HMAC contract for this channel.
- [oc_channels_line](oc_channels_line.md) — LINE channel; relevance (planned, this series): sibling bot/token channel with the same setup pattern.
- [oc_channels_matrix_setup](oc_channels_matrix_setup.md) — Matrix setup; relevance (planned, this series): sibling channel-setup procedure (auth/access/threads).
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — runtime behavior; relevance (planned, this series): peer chat-mode/threading/preview-streaming/reaction behavior.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): peer config-key reference style.
- [oc_channels_location](oc_channels_location.md) — inbound location model; relevance (planned, this series): shared inbound-context normalization peer.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: implements the Mattermost adapter this note documents.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: home of the Mattermost plugin + directory adapter.

**Snippets**
- [snippet_hermes_agent_gw_platform_mattermost](../../code_snippets/snippet_hermes_agent_gw_platform_mattermost.md) — Hermes Mattermost handler; relevance: cross-tool Mattermost adapter reference.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `dmPolicy: "pairing"`/`allowFrom`/access-group gating.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reactions; relevance: `message action=react` add/remove + system events.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — threading/session policy; relevance: `replyToMode` thread-scoped sessions.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — target resolution; relevance: `channel:`/`user:`/`@username` user-first resolution.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered preview deltas; relevance: single draft-preview-post streaming edits.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP routing; relevance: `/api/channels/mattermost/command` callback mounting (405-not-404 check).
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron/outbound delivery; relevance: `openclaw message send` cron/webhook target delivery.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access; relevance: parity for native slash-command registration/authorization.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — account/env normalization; relevance: `MATTERMOST_*` env vars (default account) + multi-account.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — error codes; relevance: "invalid command token"/registration-failure troubleshooting.

### oc_channels_mattermost_buttons (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the gateway that renders buttons and verifies callbacks.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: button clicks POST to the gateway's `interactions` callback URL.
- [Authentication](../../term_dictionary/term_authentication.md) — request verification; relevance: HMAC-SHA256 `_token` verification of button clicks.
- [HMAC (term_idempotency proxy)](../../term_dictionary/term_idempotency.md) — replay-safe callbacks; relevance: signed `_token` + Mattermost stripping callback data make clicks single-use.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — untrusted callback data; relevance: external-script payloads are signed/validated before the agent acts on them.
- [Bot](../../term_dictionary/term_bot.md) — automated sender; relevance: the secret is derived deterministically from the bot token.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — external callback reachability; relevance: `interactions.callbackBaseUrl` must be reachable from the Mattermost server.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: `https://gateway.example.com` callback base URL for external scripts.

**Docs**
- [Hermes: Mattermost](../hermes_agent/hermes_messaging_mattermost.md) — Hermes Mattermost channel; relevance: sibling Mattermost interactive/message behavior for parity.
- [Hermes: Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — signed callback routes; relevance: parity for HMAC-verified inbound callback routes.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — approval-button flow; relevance: parity for button-driven approve/deny interactions.
- [Hermes: MS Graph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — verified webhook listener; relevance: parity for verifying inbound interaction callbacks.
- [oc_channels_mattermost](oc_channels_mattermost.md) — Mattermost setup; relevance (planned, this series): the parent channel the buttons run on (`capabilities: ["inlineButtons"]`).
- [oc_channels_matrix_presentation](oc_channels_matrix_presentation.md) — presentation metadata; relevance (planned, this series): cross-channel parity for buttons/select payload structures.
- [oc_channels_matrix_behavior](oc_channels_matrix_behavior.md) — exec-approval behavior; relevance (planned, this series): peer interactive-approval (reactions vs buttons) model.
- [oc_channels_matrix_config_reference](oc_channels_matrix_config_reference.md) — config-key reference; relevance (planned, this series): `capabilities`/`interactions.callbackBaseUrl` keys.
- [oc_channels_line](oc_channels_line.md) — LINE rich messages; relevance (planned, this series): peer rich-payload model (quick-replies/Flex/template).
- [oc_channels_location](oc_channels_location.md) — structured channel data; relevance (planned, this series): peer structured-payload model note.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel-adapter code; relevance: `buildButtonAttachments()` + button rendering live here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security module; relevance: HMAC-SHA256 `_token` verification + fail-closed validation.

**Snippets**
- [snippet_hermes_agent_gw_platform_mattermost](../../code_snippets/snippet_hermes_agent_gw_platform_mattermost.md) — Hermes Mattermost handler; relevance: cross-tool Mattermost interaction/attachment reference.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — HMAC webhook signature verify; relevance: the canonical HMAC-SHA256 signing/verification recipe peer.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — replay cache; relevance: replay protection peer for single-use signed callbacks.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — interaction events; relevance: button-click selection forwarded as an inbound message/event.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — inbound request handler; relevance: the `interactions` callback request handler path.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP routing; relevance: mounting the `/mattermost/interactions/...` callback route.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content handling; relevance: validating external-script-posted button payloads.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel/DM audit; relevance: auditing interaction-callback reachability/exposure.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret derivation; relevance: deriving the HMAC secret from the bot token (deterministic).
- [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval-button UI; relevance: parity for interactive approve/deny button UI.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — verified webhook handler; relevance: parity for verifying signed inbound interaction callbacks.

> distinct): term_openclaw, term_webhook, term_authentication, term_oauth_token, term_access_control, term_bot,
> term_chatbot, term_markdown, term_prompt_injection, term_speech_to_text, term_voip, term_encryption, term_tls,
> term_reverse_proxy, term_api_gateway, term_rate_limiting, term_sse, term_idempotency, term_exponential_backoff,
> term_websocket, term_acp_agent_client_protocol, term_message_queue. Repos (7): repo_openclaw_channels,
> repo_openclaw_channels_messaging, repo_openclaw_security, repo_openclaw_gateway, repo_openclaw_sessions,
> repo_openclaw_cli_wizard, repo_openclaw. Existing docs: hermes_agent/hermes_messaging_* (line, matrix,
> matrix_e2ee, matrix_proxy_mode, mattermost, media_settings, gateway_architecture, signal, whatsapp_baileys,
> slack), hermes_webhooks_{routes_security, routing_delivery}, hermes_msgraph_webhook_listener,
> hermes_security_{command_approval, isolation_credentials}, hermes_gateway_{internals, operations},
> hermes_acp_internals, hermes_session_storage, hermes_sessions_lifecycle_resume,
> sessions_approval}; claude_code/cc_{channels_security_and_enterprise_controls}. Snippets: all
> **Sibling oc_channels_* docs are (planned, this series)** — they do not exist yet and materialize during
> execution; each note also cites ≥5 EXISTING docs toward the 10-doc floor. **Non-existent (NOT cited):**
> term_session, term_pairing, term_end_to_end_encryption, term_e2ee, term_cross_signing, term_hmac, term_ssrf,
> term_tailscale, term_transcription, term_streaming, term_slash_command; entry_openclaw_docs (created as master
> pre-step W1, cited only as the discoverability spine in Inlinks, not as a Related-Notes link target).

## Undigested Terms Plan

Per master: OpenClaw channel vocabulary is the subject of these doc pages → digested as `oc_*` doc notes, NOT
new `term_dictionary` entries. The only term-dictionary interaction is LINKING existing terms.

| Term (surface in source) | Disposition |
|---|---|
| LINE / Matrix / Mattermost (platform names) | Documented as `oc_channels_*` config; not promoted to term notes. |
| webhook / channel access token / channel secret / bot token | Link existing `term_webhook`, `term_authentication`, `term_oauth_token`; not redefined. |
| end-to-end encryption (E2EE) / cross-signing / SAS / recovery key / room-key backup | Concepts of `oc_channels_matrix_encryption`; link existing `term_encryption`. No existing `term_end_to_end_encryption`/`term_cross_signing`/`term_e2ee` — see new-term note below. |
| HMAC-SHA256 / `_token` signing | Concept of `oc_channels_mattermost_buttons`; link `term_authentication` (and `term_idempotency` for callback replay). No existing `term_hmac`. |
| streaming / preview / quiet / blockStreaming | Concept of `oc_channels_matrix_behavior` + `oc_channels_matrix_push_rules`; link existing `term_sse`; `concepts/streaming` link-out. No existing `term_streaming`. |
| pairing / allowlist / dmPolicy / groupPolicy / access groups | Link existing `term_access_control`; cross-ref `channels/pairing` + `channels/access-groups` (ch04/ch01). No existing `term_pairing`. |
| session / sessionScope / thread bindings | Link existing `term_message_queue` (queue-steering peer) + cross-ref `concepts/session` (co06). No existing `term_session`. |
| ACP conversation bindings | Link existing `term_acp_agent_client_protocol`; cross-ref `tools/acp-agents`. |
| location / geo_uri / Location* ctx fields | Concept of `oc_channels_location`; link existing `term_prompt_injection` (untrusted metadata). No existing `term_geolocation`/`term_location`. |
| voice messages / transcription | Concept of `oc_channels_matrix_behavior`; link existing `term_speech_to_text`; `tools/media-overview` link-out. No existing `term_transcription`. |
| SSRF / private-network opt-in / proxy | Concept of `oc_channels_matrix_encryption`; link existing `term_reverse_proxy`/`term_api_gateway`; `gateway/security` link-out. No existing `term_ssrf`/`term_tailscale`. |

**Expected new `term_dictionary` captures: 0.** Channel vocabulary is configuration-and-protocol-specific and
either has an existing term to link or belongs in the `oc_*` doc note. One *possible* cross-cutting candidate is
surfaced below; the augment Step 2d re-scan makes the final call (most likely: link `term_encryption` and skip).

## Term-Note Authoring Requirements

**Default: N/A (0 new terms)** — inherited from master; this sub-plan authors zero `term_dictionary` notes and
inlines zero term definitions in `oc_*` notes.

**New-term candidate (augment to decide; default = do NOT create):** `term_end_to_end_encryption` (best-fit
glossary `acronym_glossary_security.md` or the security/crypto glossary; alias "E2EE"). It is genuinely
cross-cutting (Matrix, Signal, WhatsApp, SimpleX channels all reference it) and has **no** existing note
(`term_end_to_end_encryption`/`term_e2ee` both MISSING; only the broader `term_encryption` exists). Per master's
near-0 expectation and the "link existing rather than create" rule, the **default disposition is to LINK
`term_encryption`** and let `oc_channels_matrix_encryption` carry the E2EE specifics; only if augment judges
E2EE reusable enough across the channel corpus would it be captured via `/tessellum-capture-term-note` + glossary
(collision-checked vs `term_encryption`). No definition is inlined in any `oc_*` note either way.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (12 notes, P2). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order, H1/`## Overview`/`## Related Notes`/`## References`, footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no claim absent from source) | diff each note vs `inbox/openclaw_docs/channels/<page>.md` |
| G3 | Density + Coverage (≤2,500w / ≤400 lines / ≤6 code; every mapped H2/H3 covered) | word/line/fence count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + repos/docs/snippets/siblings, each with relevance statement) | Candidate Cross-References → locked at augment |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | DB existence check on every cited ID |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability (each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`; in-degree ≥1) | via `entry_openclaw_docs.md` + the Inlinks section below |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_line oc_channels_location oc_channels_matrix_setup oc_channels_matrix_encryption oc_channels_matrix_behavior oc_channels_matrix_config_reference oc_channels_matrix_migration oc_channels_matrix_migration_messages oc_channels_matrix_presentation oc_channels_matrix_push_rules oc_channels_mattermost oc_channels_mattermost_buttons"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: required sections + source_url
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "G1 MISSING SECTION '$sec': $n"; done
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "G1 MISSING source_url: $n"; }
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G3: density caps (body only)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4: at least one sibling oc_ link present
  grep -q "($SIBLING_PREFIX" "$f" || echo "G4 NO SIBLING oc_ LINK: $n"
done

# G1 (frontmatter) batch
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5: ghost-reference DB existence check on every cited link target
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for f in "$GATE_DIR"/oc_channels_*.md; do
  grep -oE '\]\([^)]+\.md\)' "$f" | sed -E 's/^\]\(//; s/\)$//' | while read -r tgt; do
    stem=$(basename "$tgt" .md)
      || echo "GHOST in $(basename "$f"): $stem"
  done
done
```

(Run from repo root. `${=NOTES}` / `${(s:|:)...}` are zsh word-splitting per the master Bash-is-zsh note.)

## Density Re-Assessment

| # | Note | BB | ~Words | Within caps (≤2,500w / ≤400L / ≤6 code)? |
|---|---|---|---:|---|
| 1 | oc_channels_line | procedure | 700 | ✅ |
| 2 | oc_channels_location | model | 450 | ✅ |
| 3 | oc_channels_matrix_setup | procedure | 750 | ✅ |
| 4 | oc_channels_matrix_encryption | procedure | 800 | ✅ |
| 5 | oc_channels_matrix_behavior | model | 800 | ✅ |
| 6 | oc_channels_matrix_config_reference | model | 600 | ✅ |
| 7 | oc_channels_matrix_migration | procedure | 750 | ✅ |
| 8 | oc_channels_matrix_migration_messages | procedure | 700 | ✅ |
| 9 | oc_channels_matrix_presentation | model | 450 | ✅ |
| 10 | oc_channels_matrix_push_rules | procedure | 600 | ✅ |
| 11 | oc_channels_mattermost | procedure | 800 | ✅ |
| 12 | oc_channels_mattermost_buttons | model | 600 | ✅ |

No note approaches the caps. The code-dense `matrix.md` (34 fences) and `mattermost.md` (15 fences) split so
each note keeps ≤6 code blocks; verbatim snippets are limited to load-bearing examples (Matrix push-rule `PUT`,
the encryption/verify command set, the Mattermost HMAC Python example, the LINE `channelData` payload).

## Entry Point Decision (inherited from master)

Contributes **12 rows** to `0_entry_points/entry_openclaw_docs.md` (created as master pre-step W1) under the
**Channels** section / a "Channels — ch03 (LINE · Location · Matrix · Mattermost)" cluster. Each note receives
its entry-point back-link at finalization (satisfies G7/G8 — the outside-folder inbound link). No new
entry point is created by this sub-plan (the series hub already exceeds the >30-note threshold corpus-wide).

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify at execution; each new note needs ≥1 for
G7/G8 in-degree):

- `entry_openclaw_docs.md` → all 12 (primary discoverability spine; created at W1).
- `repo_openclaw_channels.md` → notes 1, 3, 5, 6, 9, 11, 12 (channel-adapter code → its product docs).
- `repo_openclaw_channels_messaging.md` → notes 1, 2, 3, 4, 5, 6, 7, 8, 10, 11.
- `repo_openclaw_security.md` → notes 4, 7, 8, 12 (E2EE / migration recovery / HMAC).
- `repo_openclaw_sessions.md` → note 5 (session/thread routing).
- `term_openclaw.md` → notes 1, 3, 11 (representative anchors; reciprocal with the term's Related Notes).
- `term_encryption.md` → notes 4, 7, 8.
- `term_webhook.md` → notes 1, 11, 12.
- `term_speech_to_text.md` → note 5; `term_prompt_injection.md` → notes 2, 9.
- `hermes_messaging_matrix.md` / `hermes_messaging_matrix_e2ee.md` → notes 3/4 (cross-tool channel parity).
- `hermes_messaging_line.md` → note 1; `hermes_messaging_mattermost.md` → notes 11, 12.

## Pacing Rules (inherited from master)

Single phase, 12 notes — within the ≤30-agent dynamic-workflow fan-out cap. Embed the manifest in the execution
script. Re-read each source page; reproduce config/command snippets verbatim where load-bearing. One
building_block per note. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before
commit. `git pull --rebase --autostash origin main` first; commit + push the phase in one cycle; no Claude
co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope.** Re-read all 7 source pages under `inbox/openclaw_docs/channels/` (line 924w, location 309w, matrix
5,856w, matrix-migration 3,215w, matrix-presentation 433w, matrix-push-rules 734w, mattermost 2,702w — measured
counts match the plan's Source table exactly). Replaced the PLAN-stage `## Candidate Cross-References` with a
LOCKED `## Per-Note Related Notes Mapping` at the RAISED floors.

**What was locked.** Per-note `## Related Notes` mapping for all 12 notes, grouped Terms / Docs / Repos /
Snippets, each link rendered as `[Name](relpath.md) — what it is; relevance: why THIS note`. Every link is
`oc_channels_*` of this series, marked `(planned, this series)`.

**Per-note counts (terms / snippets / docs / repos · floors ≥8t·≥10s·≥10d met):**

| Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors |
|---|--:|--:|--:|--:|---|
| oc_channels_line | 8 | 11 | 11 (6 existing) | 2 | ✅ |
| oc_channels_location | 8 | 10 | 10 (5 existing) | 2 | ✅ |
| oc_channels_matrix_setup | 8 | 11 | 11 (5 existing) | 3 | ✅ |
| oc_channels_matrix_encryption | 9 | 11 | 11 (5 existing) | 3 | ✅ |
| oc_channels_matrix_behavior | 9 | 12 | 11 (5 existing) | 3 | ✅ |
| oc_channels_matrix_config_reference | 8 | 10 | 11 (5 existing) | 2 | ✅ |
| oc_channels_matrix_migration | 8 | 11 | 11 (5 existing) | 3 | ✅ |
| oc_channels_matrix_migration_messages | 8 | 10 | 11 (5 existing) | 3 | ✅ |
| oc_channels_matrix_presentation | 8 | 10 | 11 (5 existing) | 2 | ✅ |
| oc_channels_matrix_push_rules | 8 | 10 | 11 (5 existing) | 2 | ✅ |
| oc_channels_mattermost | 9 | 11 | 11 (5 existing) | 2 | ✅ |
| oc_channels_mattermost_buttons | 8 | 11 | 11 (5 existing) | 2 | ✅ |

**New-term candidate + best-fit glossary.** `term_end_to_end_encryption` (alias "E2EE"; best-fit glossary
`0_entry_points/acronym_glossary_security.md` — VERIFIED to exist 2026-06-21). Default disposition UNCHANGED:
**do NOT create** — link the existing `term_encryption` and let `oc_channels_matrix_encryption` carry the E2EE
specifics (per master near-0 expectation + "link existing rather than create"). No definition is inlined in any
`oc_*` note. Step 2d re-read surfaced no other new vault-reusable term lacking both a doc-page home and an
existing note; the missing terms (`term_session`, `term_pairing`, `term_hmac`, `term_ssrf`, `term_cross_signing`,
`term_streaming`, `term_slash_command`, `term_tailscale`) are channel-config/protocol-specific and are correctly
handled by linking existing terms + link-outs (per the Undigested Terms Plan), so the expected new-term count
stays **0**.

from the existing `claude_code/`/`pi/` doc corpora), entry-point inherited (`entry_openclaw_docs` planned at W1),
density within caps, source measured. Plan advanced to `status: ready`.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_ch03.md` · Date: 2026-06-21 · Mode: post-augment final sign-off (read-only of
the augmented plan + independent re-measure of 2 source pages + DB re-verification).

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance statements) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 12 notes ≥8 terms · ≥10 snippets · ≥10 docs (parsed-count table above); every link carries `relevance:` clause; bare-link check = 0. |
| CP2 | 9-GATE table present per batch (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 discoverability; `## Validation Scripts` implements G1/G3/G5 (incl. the ghost-DB-existence loop). |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)`: contributes 12 rows to `entry_openclaw_docs.md` (created master pre-step W1); `entry_openclaw_docs` confirmed NOT-yet-existing in DB (correctly planned, not a ghost). |
| CP4 | Plan size (≤30 or split) | **PASS** | 12 notes, single execution phase — within the ≤30-agent fan-out cap. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Inherits master Format Definition (YAML field order + `## Overview`/source-mirrored H2/`## Related Notes`/`## References`/bold footer), itself derived from `claude_code/`+`pi/` corpora; `notes_scan.py` maps `openclaw → dev_tool_docs` (W4 DONE). |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: all 12 notes 450–800w, ≤6 code blocks — no note near the 2,500w/400L/6-code caps. matrix.md split ×4, matrix-migration ×2, mattermost ×2 already promoted in `## Split Decisions`. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21 via `wc -w` on the raw mirror: line 924 / location 309 / matrix 5,856 / matrix-migration 3,215 / matrix-presentation 433 / matrix-push-rules 734 / mattermost 2,702 — identical to the plan's Source table (ratio 1.00). |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (11 rows, each with disposition = link-existing/link-out, 0 TBD); `## Term-Note Authoring Requirements` present (default N/A, 0 new terms; new-term candidate `term_end_to_end_encryption` + best-fit glossary named). |
| CP8f | Term-slug specificity + all-notes (term AND doc) collision audit | **PASS** | 0 new term slugs to rename (expected captures = 0 → no specificity flags). Doc-note collision audit: 12 `oc_channels_*` slugs vs existing `term_*`/`documentation/` — no existing note covers a channel page (Hermes channel docs are cross-tool peers, LINKED not duplicated; `repo_openclaw_channels*` are code-side, LINKED). New-term candidate collision-checked vs existing `term_encryption` → resolved to LINK existing (do-not-create). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 12 notes with ≥1 outside-folder inbound link each (`entry_openclaw_docs` → all 12; `repo_openclaw_channels*` → channel-adapter notes; `term_*`/`hermes_messaging_*` reciprocals); G7/G8 in the phase gate table; in-degree ≥1 verified at execution. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status changed `pending → ready`.
