---
title: Hermes Agent Docs Digestion — Sub-Plan 13 — Messaging: Chinese Platforms
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/
pages:
  - user-guide/messaging/feishu.md
  - user-guide/messaging/weixin.md
  - user-guide/messaging/wecom.md
  - user-guide/messaging/wecom-callback.md
  - user-guide/messaging/dingtalk.md
  - user-guide/messaging/yuanbao.md
  - user-guide/messaging/qqbot.md
---

# Sub-Plan 13: Messaging: Chinese Platforms (Feishu/Lark, WeChat/Weixin, WeCom + callback, DingTalk, Yuanbao, QQ Bot)

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP13's note
> filenames/BBs/coverage are defined.

## Scope

Platform-setup procedures for the six Chinese / Tencent-and-Alibaba-ecosystem messaging surfaces Hermes
bridges through its gateway: **Feishu/Lark** (Lark SDK WebSocket + webhook, doc-comment intelligent reply,
meeting-invite auto-join), **WeChat/Weixin** (Tencent iLink Bot long-poll, AES-128-ECB CDN), **WeCom /
Enterprise WeChat** (AI Bot WebSocket gateway) **+ WeCom Callback** (self-built-app encrypted-XML webhook,
multi-corp routing), **DingTalk** (Stream-Mode WebSocket, AI Cards), **Yuanbao** (HMAC-signed WebSocket,
COS media), and **QQ Bot** (Official QQ Bot API v2, voice STT). Source = 7 mirrored pages in
`inbox/hermes_agent_docs/`. **P2 / messaging.** Each note documents *how to configure and run* one platform
adapter and **cross-links down** to the existing `snippet_hermes_agent_gw_platform_*` implementation layer.

## Content Strategy

- **One BB per note.** Each platform page is a self-contained `procedure` (create app → grant scopes →
  pick transport → configure env/`config.yaml` → start gateway → secure). `feishu.md` (3934w) also carries
  three distinct *feature* arcs (doc-comment reply, meeting invites, media/batching/rate-limiting) on top of
  base setup → split into 2 procedure notes (see Split Decisions). The other six pages are 1 note each.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the messaging
  *gateway concept* + DM-pairing + silence-token + group-session-isolation model (SP11), the `hermes gateway
  setup`/`hermes gateway` CLI (SP02 `hermes_cli_interface`), session keys + per-platform session tracking
  (SP02 `hermes_session_search_storage`), cron home-channel delivery (SP06), voice STT subsystem (SP08
  `term_speech_to_text`+`term_voice_mode`), config.yaml `platforms.*` blocks + group-session isolation
  (SP02 `hermes_messaging_media_settings`), the `adding-platform-adapters` developer internals (SP19).
- **Owned NEW term captures: 0.** Every reusable concept SP13 touches (messaging gateway, DM pairing,
  silence token) is SP11-owned (link at finalization, +fin). Platform-specific surfaces (Feishu app,
  iLink bot, WeCom AI Bot, DingTalk Stream Mode, Yuanbao HMAC gateway, QQ Bot API v2) are too platform-narrow
  to be reusable standalone terms — they are documented IN the notes, not captured as `term_*`. Collision
  audit (below) confirms 0 platform-named term notes exist → no false re-capture risk.
- **EXISTING → LINK (verified active 2026-06-15):** `term_session_persistence`, `term_oauth_token`,
  `term_authentication`, `term_autonomous_coding_agents`, `term_subagent`, plus the protocol/security terms
  used per-note (`term_websocket`, `term_api_gateway`, `term_encryption`, `term_rate_limiting`, etc.).

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/messaging/feishu.md | 3934 | 21 | procedure | 2 (split) |
| user-guide/messaging/weixin.md | 2657 | 7 | procedure | 1 |
| user-guide/messaging/wecom.md | 1862 | 7 | procedure | 1 |
| user-guide/messaging/dingtalk.md | 1649 | 12 | procedure | 1 |
| user-guide/messaging/yuanbao.md | 1451 | 14 | procedure | 1 |
| user-guide/messaging/wecom-callback.md | 952 | 4 | procedure | 1 |
| user-guide/messaging/qqbot.md | 638 | 4 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **8 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_gateway_feishu_setup.md` | procedure | feishu §How Hermes Behaves, §Step 1 Create App (+scan-to-create, manual, permissions, events, publish), §Step 2 Connection Mode (websocket/webhook), §Step 3 Configure, §Step 4 Start, §Home Chat, §Security (allowlist/encrypt-key/verification-token), §Group Message Policy, §Per-Group Access Control, §Troubleshooting | ~1700 | Feishu/Lark base setup: scan-to-create vs manual app creation, required/recommended scopes, event subscription, WebSocket vs webhook transport (with `FEISHU_ENCRYPT_KEY` SHA256 signature + verification-token), user allowlist + `FEISHU_GROUP_POLICY` + per-group `group_rules`, home chat, troubleshooting. |
| 2 | `hermes_gateway_feishu_features.md` | procedure | feishu §Bot Identity, §Bot-to-Bot Messaging, §Interactive Card Actions (+required app config, command approval), §Document Comment Intelligent Reply (+3-tier access control, app config), §Meeting Invitation Events, §Media Support (in/out), §Markdown Rendering and Post Fallback, §Processing Status Reactions, §Burst Protection and Batching, §Rate Limiting (Webhook), §WebSocket Tuning, §Deduplication, §All Environment Variables, §Toolset | ~1500 | Feishu advanced features: interactive-card command approval, `drive.notice.comment_add_v1` doc-comment reply via `feishu_doc`/`feishu_drive` toolsets with 3-tier (exact/wildcard/top-level) ACL + pairing, `vc.bot.meeting_invited_v1` auto-join, inbound/outbound media, post-fallback markdown, text/media batching, per-IP webhook rate limiting + anomaly tracking, dedup. |
| 3 | `hermes_gateway_weixin_setup.md` | procedure | weixin §iLink bot identity warning, §Prerequisites, §Setup (QR wizard, env vars, start), §Features, §Configuration Options, §Access Policies (DM/group), §Media Support (+AES-128-ECB CDN), §Context Token Persistence, §Markdown, §Message Chunking, §Typing, §Long-Poll Connection (+retry, dedup, token lock), §Env Vars, §Troubleshooting | ~1700 | WeChat/Weixin personal-account adapter via Tencent iLink Bot API: QR-login wizard, the iLink-bot-identity group-delivery limitation, long-poll transport, AES-128-ECB encrypted-CDN media, disk-backed `context_token` reply continuity, `WEIXIN_DM_POLICY`/`group_policy` (default `disabled`), chunking, typing tickets, token lock. |
| 4 | `hermes_gateway_wecom_setup.md` | procedure | wecom §Prerequisites, §Setup (Step 1 create AI Bot, Step 2 configure, Step 3 start), §Features (+no-streaming note), §Configuration Options, §Access Policies (DM/group + per-group sender allowlists), §Media Support (+AES-256-CBC, outbound size limits/downgrade), §Reply-Mode Responses, §Connection and Reconnection (+lifecycle, backoff, dedup), §Env Vars, §Troubleshooting | ~1300 | WeCom (Enterprise WeChat) AI-Bot WebSocket adapter: scan-to-create bot, `aibot_subscribe` auth + 30s heartbeat, `dm_policy`/`group_policy` + per-group `groups.<id>.allow_from` wildcards, AES-256-CBC inbound media + chunked upload + size-based downgrade, `aibot_respond_msg` reply correlation, exponential-backoff reconnection. |
| 5 | `hermes_gateway_wecom_callback_setup.md` | procedure | wecom-callback §How It Works, §Prerequisites, §Setup (create self-built app, env vars, start), §Configuration Reference, §Multi-App Routing, §Access Control, §Endpoints, §Encryption, §Limitations, §Troubleshooting | ~950 | WeCom self-built-app callback (webhook) adapter: encrypted-XML callback over a public HTTP endpoint, Corp ID/Secret/Agent ID/Token/EncodingAESKey, AES-CBC + SHA1-signature crypto (WXBizMsgCrypt-compatible), `corp_id:user_id` multi-corp routing, GET-verify/POST-message/health endpoints, text-only + no-streaming limitations. |
| 6 | `hermes_gateway_dingtalk_setup.md` | procedure | dingtalk §How Hermes Behaves (+session model), §Prerequisites, §Step 1 Create App, §Step 2 Enable Robot (Stream Mode), §Step 3 Find User ID, §Step 4 Configure (interactive QR/manual, openClaw branding note, config.yaml), §Start, §Features (AI Cards, Emoji Reactions, Display Settings), §Troubleshooting, §Security, §Notes | ~1400 | DingTalk Stream-Mode chatbot: `hermes-agent[dingtalk]` SDK trio, QR device-flow vs manual credentials (openClaw consent-screen disclosure), `DINGTALK_ALLOWED_USERS` deny-by-default + `require_mention` group gating, AI Cards with streaming, 🤔/🥳 emoji status reactions, per-platform display settings, exponential-backoff reconnect, session-webhook reply model. |
| 7 | `hermes_gateway_yuanbao_setup.md` | procedure | yuanbao §Prerequisites, §Setup (create bot, wizard, env vars, start), §Features, §Configuration Options (chat-id formats, media uploads), §Home Channel (+auto-sethome, examples), §Usage Tips, §Troubleshooting, §Access Control, §Advanced Configuration (chunking, connection params, verbose logging), §Integration with Other Features | ~1400 | Yuanbao (Tencent enterprise) WebSocket adapter: HMAC-signed handshake with APP_ID/APP_SECRET, C2C `direct:` + `group:` chat-id scheme, COS (Tencent Cloud Object Storage) media with SSRF validation, `/sethome` + auto-sethome home channel for cron delivery, `dm_policy`/`group_policy`, built-in connection tuning, cross-platform message routing. |
| 8 | `hermes_gateway_qqbot_setup.md` | procedure | qqbot §Overview, §Prerequisites (QQ Bot App + intents), §Configuration (interactive/manual), §Environment Variables, §Advanced Configuration, §Voice Messages (STT two-stage), §Troubleshooting | ~700 | QQ Bot adapter on the Official QQ Bot API v2: WebSocket-gateway receive + REST send across C2C/group/guild/DM, required intents, `QQ_APP_ID`/`QQ_CLIENT_SECRET`, sandbox vs production routing, two-stage voice transcription (QQ built-in `asr_refer_text` → OpenAI-compatible STT fallback), `dm_policy`/`group_policy` allowlists, QQ markdown. |

**SP13 totals:** 8 notes · procedure 8 · concept 0 (gateway/pairing concepts are SP11-owned term notes).
7 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 8 · procedure 8 · concept 0 (messaging-gateway / DM-pairing / silence-token concepts owned by SP11 term notes; platform-specific surfaces documented in-note, not captured).
- Source: 7 digested pages (~13.1K words) → ~10.6K words of notes (modest compression via link-outs to SP02/SP06/SP08/SP11 owners).
- BB mix: procedure 100% (uniform platform-setup procedures).

## Section Coverage Map

```
feishu.md (3934w)
├── intro + How Hermes Behaves (DM/group/shared-chat + group_sessions_per_user) → Note 1 (group-session isolation model→SP02/SP11)
├── Step 1 Create App (scan-to-create / manual / Configure Permissions / Configure Events / Publish) → Note 1
├── Step 2 Connection Mode (WebSocket / Webhook + challenge/verification-token) → Note 1
├── Step 3 Configure (interactive / manual env) / Step 4 Start / Home Chat → Note 1 (home-chat cron→SP06)
├── Security (User Allowlist / Webhook Encryption Key SHA256 / Verification Token) → Note 1
├── Group Message Policy (FEISHU_GROUP_POLICY / require_mention) → Note 1
├── Per-Group Access Control (group_rules) → Note 1
├── Troubleshooting → Note 1
├── Bot Identity / Bot-to-Bot Messaging (A2A) ───────────────── → Note 2
├── Interactive Card Actions (+required app config / command approval) → Note 2 (command approval=human-in-loop→SP02)
├── Document Comment Intelligent Reply (+3-Tier Access Control / app config) → Note 2 (feishu_doc/feishu_drive toolsets)
├── Meeting Invitation Events (+required app config) ─────────── → Note 2
├── Media Support (Inbound / Outbound) ──────────────────────── → Note 2 (multimodal→SP08)
├── Markdown Rendering and Post Fallback / Processing Status Reactions → Note 2
├── Burst Protection and Batching (text / media / per-chat serialization) → Note 2
├── Rate Limiting (Webhook) (+anomaly tracking) / WebSocket Tuning / Deduplication → Note 2
├── All Environment Variables ───────────────────────────────── → Note 2 (full table; Note 1 lists Step-1 subset)
└── Toolset (hermes-feishu preset) ──────────────────────────── → Note 2 (toolset internals→SP05/SP19)
weixin.md (2657w) ── ALL sections ──────────────────────────────── → Note 3 (AES/CDN media→SP08 link; iLink limitation in-note)
wecom.md (1862w) ─── ALL sections ──────────────────────────────── → Note 4 (per-group allowlist + AES-256 in-note)
wecom-callback.md (952w) ── ALL sections ───────────────────────── → Note 5 (xref Note 4 bot-vs-callback)
dingtalk.md (1649w) ── ALL sections ────────────────────────────── → Note 6 (AI Cards / display settings→SP02; STT vision→SP08)
yuanbao.md (1451w) ── ALL sections ─────────────────────────────── → Note 7 (cron/background→SP06; slash→SP20)
qqbot.md (638w) ──── ALL sections ──────────────────────────────── → Note 8 (STT→SP08 link)
```

No source H2/H3 orphaned. All 7 pages fully covered; gateway-concept / cron / voice-STT / config-block detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| feishu.md (3934w, 21 code) | Note 1 (`hermes_gateway_feishu_setup`, base setup + security + group policy) + Note 2 (`hermes_gateway_feishu_features`, card/doc-comment/meeting/media/batching/rate-limit) | >2500w → MUST split into ≥2 (plan-digestion Step 3c). Two cohesive arcs: get-the-bot-running (app/scopes/transport/allowlist) vs the advanced feature surface (interactive cards, doc-comment reply with `feishu_doc`/`feishu_drive` toolsets, meeting auto-join, media, batching). Both single-BB procedure; each kept ≤6 curated code blocks. |

The other six pages (weixin 2657w is just over the 2500w cap but is a single uninterrupted setup procedure with only 7 code blocks; per plan-digestion Step 3c "2500–4000w MUST split" — see Density Re-Assessment for the keep/split call) → reviewed at CP6.

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / candidate term | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_gateway_feishu_setup`, `hermes_gateway_feishu_features`, `hermes_gateway_weixin_setup`, `hermes_gateway_wecom_setup`, `hermes_gateway_wecom_callback_setup`, `hermes_gateway_dingtalk_setup`, `hermes_gateway_yuanbao_setup`, `hermes_gateway_qqbot_setup` | DB scan for `term_%feishu%`/`%wechat%`/`%dingtalk%`/`%lark%`/`%wecom%`/`%qq%` → **0 rows**; no `resources/documentation/hermes_agent/%` notes exist yet | NEW (no term/doc note covers any of these platform procedures) | CREATE all 8. |
| (would-be) `term_messaging_gateway` | SP11-owned; not yet in DB (MISSING 2026-06-15); `term_api_gateway` (active) is a DIFFERENT concept (HTTP API gateway, not platform↔agent bridge) — master false-positive caution | **NOT SP13-owned** | LINK as +fin (SP11 owner); link `term_api_gateway` only where the webhook/HTTP-endpoint angle is genuinely relevant. |
| (would-be) `term_dm_pairing`, `term_silence_token` | SP11-owned; MISSING in DB 2026-06-15 | **NOT SP13-owned** | LINK as +fin (SP11). |
| (would-be) `term_ilink_bot` / `term_wecom_ai_bot` / `term_dingtalk_stream_mode` / `term_qq_bot_api` | none exist; platform-narrow, not reusable | **DO NOT capture** | Documented in-note; not a standalone term (fails reusability test). |

DB synonym scan run across `term_dictionary/` AND `documentation/` for every planned slug's keywords; **0
substantive same-concept duplicates** and **0 platform-named term notes** exist. SP13 owns **0** new term
captures. New `hermes_agent/` folder → no doc-doc collisions (SP01/SP02 not yet executed; intra-series links
resolve at finalization, verified by G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> Cross-ref floor raised 2026-06-19 (master, FOUR-FLOOR standard, supersedes the prior ≥8 term / ≥8 snippet /
> ≥5 doc wording): each note's `## Related Notes` carries **four counted, relevancy-selected groups** —
> whose modules implement what this doc describes), **≥10 snippet notes**
> (`../../code_snippets/snippet_hermes_agent_gw_*`, gw bucket primary — the implementation layer the note
> ≥10), and **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in this series + analogous
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`. **All term, code-repo, and snippet IDs below
> IDs are forward-refs in this same series that resolve at finalization (G5/G8). SP11/SP08/SP14-owned
> not-yet-existing terms are marked `[own]` in `(+fin …)`, ADDITIONAL forward-refs EXCLUDED from the ≥8 floor.

**Note 1 `hermes_gateway_feishu_setup`**
- Terms (8): term_oauth_token, term_authentication, term_websocket, term_access_control, term_encryption, term_rate_limiting, term_session_persistence, term_autonomous_coding_agents — relevance: Feishu app-credential auth, WebSocket/webhook transport choice, allowlist/group-policy access control, encrypt-key signature + verification-token, per-IP rate limiting, per-user shared-chat session isolation. (+fin: term_messaging_gateway[own], term_dm_pairing[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the gateway/messaging package whose Feishu adapter this doc configures), repo_hermes_agent (top-level repo — overall agent the gateway fronts), repo_hermes_agent_cli (`hermes gateway setup`/`hermes gateway` commands that create the app + start the adapter), repo_hermes_agent_agent_core (per-user session isolation + turn loop the bound chat drives), repo_hermes_agent_providers_adapters (provider boot wired up when the gateway starts).
- Snippets (10): gw_platform_feishu_connect, gw_platform_feishu_acl, gw_platform_base_abstract, gw_platform_registry, gw_platform_helpers, gw_pairing, gw_runner_session_key, gw_config_per_channel, gw_config_schema, gw_start_gateway_main — relevance: the Feishu connect/ACL adapter code, the base-adapter + registry the preset plugs into, the pairing/allowlist + session-key + per-channel config + config-schema paths this setup drives, and the gateway-main entrypoint `hermes gateway` invokes.
- Docs (10): hermes_gateway_feishu_features, hermes_gateway_wecom_setup, hermes_gateway_dingtalk_setup, hermes_messaging_overview, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_cli_interface, hermes_security_command_approval, cc_channels_setup (Claude Code channel-setup analogue — create/configure a messaging channel), cc_claude_code_in_slack (analogous chat-platform bot setup).

**Note 2 `hermes_gateway_feishu_features`**
- Terms (8): term_human_in_the_loop, term_multimodal, term_a2a, term_subagent, term_throttling, term_idempotency, term_access_control, term_function_calling — relevance: interactive-card command approval is human-in-the-loop, media is multimodal, bot-to-bot is A2A, doc-comment reply spawns scoped agent sessions, webhook rate limiting throttles, 15-min/24h dedup is idempotency, 3-tier doc ACL, `feishu_doc`/`feishu_drive` toolset invocation is function calling. (+fin: term_text_to_speech[own], term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (Feishu adapter's card/comment/meeting feature code), repo_hermes_agent_tools (the `feishu_doc`/`feishu_drive` toolsets the doc-comment handler runs), repo_hermes_agent_agent_core (scoped agent session the comment/meeting events spawn + command-approval loop), repo_hermes_agent_mcp_toolsets (toolset preset resolution backing `hermes-feishu`), repo_hermes_agent (top-level repo the A2A/command-approval features belong to).
- Snippets (10): gw_platform_feishu_comment, gw_platform_feishu_message_card, gw_platform_feishu_connect, gw_platform_base_outbound, gw_platform_base_normalize, gw_delivery, gw_stream_batching, gw_runner_outbound, gw_runner_acl, gw_stream_consumer — relevance: the doc-comment handler, interactive-message-card, outbound/normalize base paths, delivery + batching + outbound-runner + ACL + stream-consumer code these features (cards, media, batching, rate-limit) exercise.
- Docs (10): hermes_gateway_feishu_setup, hermes_messaging_media_settings, hermes_messaging_overview, hermes_gateway_wecom_setup, hermes_gateway_qqbot_setup, hermes_security_command_approval, hermes_tools_reference_platform_media, hermes_toolsets_reference, cc_channel_reply_tool (Claude Code channel reply-tool analogue — bot replies in a channel), cc_voice_dictation (voice/media handling analogue for inbound voice attachments).

**Note 3 `hermes_gateway_weixin_setup`**
- Terms (8): term_authentication, term_encryption, term_cdn, term_session_persistence, term_access_control, term_idempotency, term_exponential_backoff, term_ssrf_guard — relevance: QR-login auth, AES-128-ECB encrypted CDN media, disk-backed `context_token` reply continuity, DM/group allowlist policy, 5-min dedup window, long-poll retry/backoff, SSRF validation of outbound media URLs. (+fin: term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the Weixin iLink long-poll adapter this doc configures), repo_hermes_agent_cli (`hermes gateway setup` QR-login wizard + `hermes gateway` start), repo_hermes_agent (top-level agent the iLink bot fronts), repo_hermes_agent_agent_core (session continuity + per-peer context the `context_token` store backs), repo_hermes_agent_providers_adapters (provider boot on gateway start).
- Snippets (10): gw_platform_weixin, gw_platform_base_abstract, gw_platform_base_outbound, gw_platform_registry, gw_platform_helpers, gw_runner_router, gw_runner_acl, gw_session_lifecycle, gw_runner_init, gw_config_per_channel — relevance: the Weixin iLink adapter (long-poll/CDN/context-token) plus the base-adapter, registry, router, ACL, session-lifecycle, runner-init, and per-channel config code its DM/group routing depends on.
- Docs (10): hermes_gateway_wecom_setup, hermes_gateway_feishu_setup, hermes_messaging_overview, hermes_messaging_media_settings, hermes_gateway_yuanbao_setup, hermes_messaging_gateway_architecture, hermes_session_search_storage, hermes_tools_reference_platform_media, cc_claude_code_in_slack (analogous personal-account chat-platform bot setup), cc_channels_setup (channel-configuration analogue).

**Note 4 `hermes_gateway_wecom_setup`**
- Terms (8): term_websocket, term_authentication, term_encryption, term_access_control, term_heartbeat, term_exponential_backoff, term_idempotency, term_autonomous_coding_agents — relevance: AI-Bot WebSocket + `aibot_subscribe` auth, AES-256-CBC inbound media, DM/group + per-group sender allowlists, 30s heartbeat keepalive, exponential-backoff reconnection, 5-min dedup. (+fin: term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the WeCom AI-Bot WebSocket adapter this doc configures), repo_hermes_agent_cli (`hermes gateway setup` scan-to-create + `hermes gateway` start), repo_hermes_agent (top-level agent the AI Bot fronts), repo_hermes_agent_agent_core (the agent turn the reply-correlation path delivers), repo_hermes_agent_providers_adapters (provider boot on gateway start).
- Snippets (10): gw_platform_wecom_connect, gw_platform_wecom_message, gw_platform_base_abstract, gw_platform_base_outbound, gw_platform_registry, gw_runner_acl, gw_runner_outbound, gw_delivery, gw_runner_supervisor, gw_runner_init — relevance: the WeCom connect (WebSocket/heartbeat/reconnect) + message (media/reply-correlation) adapters and the base/registry/ACL/outbound/delivery + runner-supervisor + runner-init code they route through.
- Docs (10): hermes_gateway_wecom_callback_setup, hermes_gateway_feishu_setup, hermes_gateway_weixin_setup, hermes_messaging_overview, hermes_messaging_media_settings, hermes_gateway_yuanbao_setup, hermes_messaging_gateway_architecture, hermes_gateway_operations, cc_channels_setup (channel-setup analogue), cc_remote_control (remote bidirectional connection analogue).

**Note 5 `hermes_gateway_wecom_callback_setup`**
- Terms (8): term_api_gateway, term_encryption, term_authentication, term_tls, term_access_control, term_replay_attack, term_webhook, term_autonomous_coding_agents — relevance: encrypted-XML callback served on a public HTTP gateway/webhook endpoint, AES-CBC + SHA1-signature crypto, Corp-secret auth, HTTPS-only (TLS) callback URL, `corp_id:user_id` scoping prevents cross-corp collisions, signature defends against replayed payloads, agent processes the queued message. (+fin: term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the WeCom-callback webhook adapter this doc configures), repo_hermes_agent (top-level agent the self-built app fronts), repo_hermes_agent_cli (`hermes gateway setup`/`hermes gateway` walk-through + service install), repo_hermes_agent_agent_core (the queued agent session that processes the decrypted message), repo_hermes_agent_acp (the agent-control HTTP-server plane analogous to the callback listener).
- Snippets (10): gw_platform_wecom_callback, gw_platform_webhook, gw_platform_base_abstract, gw_platform_registry, gw_platform_helpers, gw_runner_router, gw_status_health, gw_runner_acl, gw_platform_msgraph_webhook, gw_config_per_channel — relevance: the WeCom-callback adapter, the shared webhook adapter, base/registry, router + health-endpoint + ACL + the sibling msgraph-webhook callback pattern + per-channel config code the encrypted-callback flow uses.
- Docs (10): hermes_gateway_wecom_setup, hermes_messaging_overview, hermes_gateway_feishu_setup, hermes_messaging_media_settings, hermes_gateway_dingtalk_setup, hermes_messaging_gateway_architecture, hermes_messaging_teams_bot, hermes_security_isolation_credentials, cc_network_tls_and_access (TLS/HTTPS endpoint reachability analogue), cc_channels_security_and_enterprise_controls (callback-endpoint security analogue).

**Note 6 `hermes_gateway_dingtalk_setup`**
- Terms (8): term_websocket, term_oauth_token, term_authentication, term_access_control, term_human_in_the_loop, term_exponential_backoff, term_computer_vision, term_autonomous_coding_agents — relevance: Stream-Mode WebSocket, QR device-flow OAuth credential exchange, deny-by-default `DINGTALK_ALLOWED_USERS` + `require_mention`, approval gating, exponential-backoff reconnect, vision-tool media resolution, AI-Card streaming. (+fin: term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the DingTalk Stream-Mode adapter this doc configures), repo_hermes_agent_cli (`hermes gateway setup` QR device-flow + `hermes gateway` start), repo_hermes_agent (top-level agent the chatbot fronts), repo_hermes_agent_agent_core (per-user session model + AI-Card streaming turn), repo_hermes_agent_tools (vision tools that resolve inbound media).
- Snippets (10): gw_platform_dingtalk, gw_platform_base_abstract, gw_platform_base_outbound, gw_platform_registry, gw_platform_helpers, gw_runner_acl, gw_runner_session_key, gw_stream_batching, gw_display_config, gw_runner_supervisor — relevance: the DingTalk Stream-Mode adapter (AI Cards/reactions/reconnect) and the base/registry/ACL/session-key/streaming + display-config (per-platform display settings) + runner-supervisor code its session-webhook reply path drives.
- Docs (10): hermes_gateway_feishu_setup, hermes_gateway_wecom_setup, hermes_messaging_overview, hermes_messaging_media_settings, hermes_gateway_yuanbao_setup, hermes_messaging_gateway_architecture, hermes_security_command_approval, hermes_security_skill_memory_settings, cc_remote_control (Stream-Mode no-public-URL bidirectional analogue), cc_channels_setup (channel-setup analogue).

**Note 7 `hermes_gateway_yuanbao_setup`**
- Terms (8): term_websocket, term_authentication, term_cdn, term_heartbeat, term_exponential_backoff, term_cron, term_access_control, term_ssrf_guard — relevance: WebSocket gateway, HMAC-signed handshake auth, COS (cloud object storage) media with SSRF validation, 30s heartbeat + 100-attempt backoff reconnection, `/sethome` cron home-channel delivery, DM/group policy. (+fin: term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the Yuanbao WebSocket adapter this doc configures), repo_hermes_agent_cron (the cron subsystem whose results `/sethome` home-channel delivery routes), repo_hermes_agent_cli (`hermes gateway setup` wizard + `/sethome`/`/cron` slash commands), repo_hermes_agent (top-level agent the bot fronts), repo_hermes_agent_agent_core (background-task + agent turn the cross-platform routing drives).
- Snippets (10): gw_platform_yuanbao_connect, gw_platform_yuanbao_proto, gw_platform_yuanbao_media, gw_platform_base_abstract, gw_platform_registry, gw_runner_cron, gw_runner_acl, gw_channel_directory, gw_runner_init, gw_session_state — relevance: the Yuanbao connect/protocol/media adapters and the base/registry, cron-runner (home-channel cron delivery), ACL, channel-directory, runner-init, and session-state code its routing relies on.
- Docs (10): hermes_messaging_overview, hermes_gateway_wecom_setup, hermes_gateway_weixin_setup, hermes_gateway_dingtalk_setup, hermes_messaging_media_settings, hermes_messaging_gateway_architecture, hermes_cron_scheduling, hermes_cron_advanced_jobs, cc_loop_scheduled_tasks (scheduled-task delivery analogue for cron home-channel), cc_channels_setup (channel-setup analogue).

**Note 8 `hermes_gateway_qqbot_setup`**
- Terms (8): term_websocket, term_authentication, term_realtime_transcription, term_access_control, term_oauth_token, term_idempotency, term_multimodal, term_autonomous_coding_agents — relevance: WebSocket gateway receive + REST send, App-ID/Secret auth, QQ built-in ASR → OpenAI-compatible STT (real-time transcription) fallback, DM/group allowlists + required intents, sandbox/production credential routing, media/voice processing. (+fin: term_speech_to_text[own], term_messaging_gateway[own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging (the QQ Bot adapter this doc configures), repo_hermes_agent_cli (`hermes gateway setup` interactive flow + `hermes gateway` start), repo_hermes_agent (top-level agent the bot fronts), repo_hermes_agent_agent_core (the agent turn the transcribed voice/text drives), repo_hermes_agent_providers_adapters (the OpenAI-compatible STT provider fallback the adapter calls).
- Snippets (10): gw_platform_qqbot_adapter, gw_platform_qqbot_chunked_upload, gw_platform_qqbot_keyboards, gw_platform_base_abstract, gw_platform_base_outbound, gw_platform_registry, gw_runner_acl, gw_runner_router, gw_runner_init, gw_config_per_channel — relevance: the QQ Bot adapter (WebSocket/REST/STT), chunked-upload + keyboards code, and the base/registry/ACL/router/runner-init/per-channel-config code its C2C/group/guild routing uses.
- Docs (10): hermes_gateway_feishu_features, hermes_messaging_overview, hermes_messaging_media_settings, hermes_gateway_dingtalk_setup, hermes_gateway_yuanbao_setup, hermes_messaging_gateway_architecture, hermes_voice_mode_cli, hermes_tools_reference_platform_media, cc_voice_dictation (voice-to-text analogue for the two-stage STT), cc_channels_setup (channel-setup analogue).

All 8 notes meet the FOUR-FLOOR standard: **≥8 term + ≥5 code-repo + ≥10 snippet (gw bucket primary) + ≥10 doc**.
`resources/term_dictionary/`; code-repo notes under `areas/code_repos/repo_hermes_agent_*`; snippet notes under
under `resources/documentation/claude_code/`; sibling `hermes_*` doc links resolve in
`resources/documentation/hermes_agent/` (intra-series forward-refs land at finalization, verified by G5/G8).
Sibling doc targets such as `hermes_messaging_overview` / `hermes_messaging_gateway_architecture` (SP11) and
`hermes_messaging_media_settings` (SP02) are forward-refs that resolve when those SPs land; the ≥10-doc floor

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 7 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 feishu-setup | procedure | 1700 | ≤6 (curate from feishu setup/security YAML; tables in prose) | ✓ |
| 2 feishu-features | procedure | 1500 | ≤6 (curate from card/comment/batching blocks) | ✓ |
| 3 weixin-setup | procedure | 1700 | ≤6 (curate from 7 blocks) | ✓ |
| 4 wecom-setup | procedure | 1300 | ≤6 (from 7 blocks) | ✓ |
| 5 wecom-callback-setup | procedure | 950 | 4 | ✓ |
| 6 dingtalk-setup | procedure | 1400 | ≤6 (curate from 12 blocks) | ✓ |
| 7 yuanbao-setup | procedure | 1400 | ≤6 (curate from 14 blocks) | ✓ |
| 8 qqbot-setup | procedure | 700 | 4 | ✓ |

No further splits needed beyond feishu→2. **weixin.md (2657w) keep-as-1 justification (CP6):** although
2657w nominally trips the "2500–4000w → split" page rule, the page is a *single uninterrupted platform-setup
procedure* (one BB, no mixing) with only 7 code blocks; the surface beyond core setup (media/CDN, chunking,
typing, long-poll) is link-out detail summarized in prose, not a second BB arc. The note targets ~1700w
written (link-outs to SP08 media + SP11 gateway compress the source) and stays ≤2500w / ≤6 code / ≤400
lines. KEEP (per review CP6 default — single topically-cohesive cluster, no BB mixing). Code-heavy pages
(dingtalk/yuanbao): keep ≤6 load-bearing blocks, summarize the rest in prose (verbatim for kept blocks).
If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder): YAML field order `tags → keywords → topics → language →
date of note → status → building_block → source_url → access_control_group`; body `# Title → ## Overview
(opener leading with what it IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed
markdown links, each `- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10
snippet + ≥10 doc) →
footer **Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps
≤2500w /≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`,
`source`, `parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown
links in YAML. Not invented — matches existing `cc_` notes and the SP01/SP02 sibling plans.

## Undigested Terms Plan (SP13)

**SP13 owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every reusable concept
SP13 touches is owned by another sub-plan (link at finalization) or is an existing verified term. Augment
re-read surfaced **0 new** undigested terms that SP13 should own — the platform pages each document a
platform-specific adapter (Feishu app, iLink bot, WeCom AI Bot, WeCom self-built callback, DingTalk Stream
Mode, Yuanbao HMAC gateway, QQ Bot API v2) whose shared *concept* (the messaging gateway / DM pairing /
silence token / group-session isolation) is SP11-owned, and whose protocol/security/voice concepts are
existing active term notes or SP08-owned.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_messaging_gateway` | LINK only (forward-ref, +fin) | SP11 | the platform↔agent bridge concept; SP13 documents per-platform adapters that plug into it. ≠ `term_api_gateway` (master false-positive caution). |
| `term_dm_pairing`, `term_silence_token` | LINK only (+fin) | SP11 | DM-authorization handshake + `[SILENT]` non-reply; SP13's `pairing` DM policies link the concept. |
| `term_text_to_speech`, `term_speech_to_text`, `term_voice_mode` | LINK only (+fin) | SP08 | QQ Bot STT + Feishu/DingTalk voice media reference the concept; concept home is SP08 media. |
| (would-be) `term_ilink_bot`, `term_wecom_ai_bot`, `term_dingtalk_stream_mode`, `term_qq_bot_api`, `term_yuanbao_gateway` | DO NOT capture | — | Platform-narrow surfaces; fail the reusability test. Documented in-note, never standalone terms. |

### Renamed (general → specific)

— (audit performed; SP13 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP13 links; all are already scope-qualified by their owners.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_messaging_gateway` | none yet (SP11-owned; MISSING in DB 2026-06-15); `term_api_gateway.md` is the UNRELATED HTTP-API-gateway concept | No removal — SP13 was never going to capture this; link SP11's term at finalization (+fin). |
| `term_feishu` / `term_wecom` / `term_dingtalk` / `term_weixin` / `term_yuanbao` / `term_qq_bot` | none (DB scan → 0 platform-named term notes) | Not captured — platform surfaces documented inside the doc notes; not reusable standalone terms. |

## Term-Note Authoring Requirements

N/A (inherited) — SP13 owns 0 new term notes. Forward-referenced terms (`term_messaging_gateway`,
`term_dm_pairing`, `term_silence_token`, `term_text_to_speech`, `term_speech_to_text`, `term_voice_mode`)
follow the master's `/tessellum-capture-term-note` spec under their owning sub-plans (SP08/SP11). The full
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12,
backlink expansion, >200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (Feishu pilot — largest page):** Notes 1, 2. Pilot Note 1 (`hermes_gateway_feishu_setup`)
  first → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (Tencent WebSocket adapters):** Notes 4, 7, 3. GATE G1–G8.
- **Phase 3 (callback + DingTalk + QQ):** Notes 5, 6, 8. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_gateway_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_gateway_feishu_setup hermes_gateway_feishu_features hermes_gateway_weixin_setup hermes_gateway_wecom_setup hermes_gateway_wecom_callback_setup hermes_gateway_dingtalk_setup hermes_gateway_yuanbao_setup hermes_gateway_qqbot_setup; do
```

## Entry Point Decision (inherited)

Contributes 8 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Messaging: Chinese Platforms" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP13 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_gateway_messaging.md` | → all 8 notes | gateway/messaging repo ↔ per-platform usage docs |
| `repo_hermes_agent.md` | → `hermes_gateway_feishu_setup`, `hermes_gateway_wecom_setup` | implementation ↔ representative platform setup |
| `snippet_hermes_agent_gw_platform_feishu_connect.md` | → `hermes_gateway_feishu_setup` | Feishu adapter code ↔ Feishu setup doc |
| `snippet_hermes_agent_gw_platform_feishu_comment.md` | → `hermes_gateway_feishu_features` | doc-comment handler code ↔ feature doc |
| `snippet_hermes_agent_gw_platform_weixin.md` | → `hermes_gateway_weixin_setup` | Weixin adapter code ↔ Weixin setup doc |
| `snippet_hermes_agent_gw_platform_wecom_connect.md` | → `hermes_gateway_wecom_setup` | WeCom adapter code ↔ WeCom setup doc |
| `snippet_hermes_agent_gw_platform_wecom_callback.md` | → `hermes_gateway_wecom_callback_setup` | callback adapter code ↔ callback setup doc |
| `snippet_hermes_agent_gw_platform_dingtalk.md` | → `hermes_gateway_dingtalk_setup` | DingTalk adapter code ↔ DingTalk setup doc |
| `snippet_hermes_agent_gw_platform_yuanbao_connect.md` | → `hermes_gateway_yuanbao_setup` | Yuanbao adapter code ↔ Yuanbao setup doc |
| `snippet_hermes_agent_gw_platform_qqbot_adapter.md` | → `hermes_gateway_qqbot_setup` | QQ Bot adapter code ↔ QQ Bot setup doc |
| `term_session_persistence.md` | → `hermes_gateway_feishu_setup`, `hermes_gateway_weixin_setup` | concept term → per-platform session-isolation docs |
| `term_websocket.md` | → `hermes_gateway_wecom_setup`, `hermes_gateway_yuanbao_setup` | concept term → WebSocket-transport platform docs |
| `entry_code_snippets_hermes_agent.md` | → `hermes_gateway_feishu_setup`, `hermes_gateway_wecom_setup` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 8 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_gateway_feishu_setup`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes
(dingtalk/yuanbao/feishu) to ≤6 load-bearing blocks, summarize the rest in prose. If a note exceeds 350
lines during writing, STOP and split. If multi-agent: agents return note content, master writes serially
where there is write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP13 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 8 rows to
  the master-created entry point; backfill the `repo_hermes_agent_gateway_messaging` / `gw_platform_*` /
  `term_*` inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After the SP11/SP12 messaging waves land: backfill the `term_messaging_gateway`/`term_dm_pairing`/
  `term_silence_token`/`term_webhook` forward-refs and the `hermes_messaging_overview` doc link into each
  SP13 note (bidirectional gateway↔platform links).
- Consider one `thought_` note comparing the seven Chinese-platform adapters' transport models
  (WebSocket-outbound vs long-poll vs public-webhook-callback) and their auth/crypto schemes.

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  code-repos added as a new ≥5 floor (the `repo_hermes_agent_*` source-code repo notes whose modules implement
  each platform adapter — gateway_messaging primary, plus cli / agent_core / providers_adapters / tools / cron /
  acp / mcp_toolsets per note); docs raised 5→≥10 (sibling `hermes_*` series + cross-SP `hermes_*` forward-refs +
  `term_realtime_transcription`; `term_function_calling` / `term_ssrf_guard` / `term_webhook` added where the
  page content warrants.
- Sections added/updated: Collision&Dedup Audit (0 platform-named term notes; `term_messaging_gateway` ≠
  `term_api_gateway` false-positive confirmed), four-floor Per-Note Mapping (≥8 term + ≥5 code-repo + ≥10 snippet
  Re-Assessment (re-read confirmed; weixin keep-as-1 justified), G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured; **1 split** (feishu→2); weixin 2657w reviewed → KEEP-as-1
  (single-BB, link-out-compressed, ≤2500w written target). All 8 notes ≤2500w; code-heavy notes curated ≤6.
- Collision audit: **0 removals** — 0 platform-named term notes exist; `term_messaging_gateway` is SP11-owned
  (+fin), `term_api_gateway` is the unrelated HTTP-API-gateway concept (LINK only where relevant, not a dup).
- Term placeholder catch: per-term DB verification done 2026-06-15; every cited term ID is active. Master
  candidate `term_messaging_gateway` confirmed MISSING (SP11-owned forward-ref, excluded from the ≥8 floor).
- Undigested terms surfaced at augment: **0 new** (SP13 owns 0 captures; all concepts owned by SP08/SP11 or
  existing active terms).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
audit noted) ✓ Slug Collision (0 platform-named term notes; `term_messaging_gateway`≠`term_api_gateway`
caught) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every
phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP13 owns 0
captures); dedup/collision items are substantively PASS (audit performed on all 8 doc notes).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**
**Re-reviewed 2026-06-19 (FOUR-FLOOR independent review) — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (8 rows under a Chinese-Platforms section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 8 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` + SP01/SP02 siblings; not invented. |
| CP6 | Borderline density → split | PASS | feishu.md→2; weixin 2657w borderline → KEEP-as-1 justified (single-BB, link-out-compressed, ≤2500w written, ≤6 code); all notes ≤2500w; code-heavy notes curated ≤6. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: feishu 3934, weixin 2657, wecom 1862, wecom-callback 952, dingtalk 1649, yuanbao 1451, qqbot 638 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP13 owns 0 term captures (all concepts owned by SP08/SP11 or existing active terms); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 8 doc notes (term_dictionary AND documentation/); 0 platform-named term notes; `term_messaging_gateway`≠`term_api_gateway` false-positive confirmed; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 8 notes from repo_*/snippet_gw_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT (2026-06-15): 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
`website/docs/` — moved from pinned commit `95715dc` to `c253b07` on 2026-06-19 (now byte-identical to
upstream main). All seven of this sub-plan's owned pages were independently re-measured against the fresh
mirror using the ledger's measurement convention (BODY word count after stripping YAML frontmatter; code
blocks = lines matching `^\s*```` divided by 2). **Word/code counts are UNCHANGED** for every owned page:

- user-guide/messaging/feishu.md — 3934w / 21code (unchanged)
- user-guide/messaging/weixin.md — 2657w / 7code (unchanged)
- user-guide/messaging/wecom.md — 1862w / 7code (unchanged)
- user-guide/messaging/wecom-callback.md — 952w / 4code (unchanged)
- user-guide/messaging/dingtalk.md — 1649w / 12code (unchanged)
- user-guide/messaging/yuanbao.md — 1451w / 14code (unchanged)
- user-guide/messaging/qqbot.md — 638w / 4code (unchanged)

Because no source counts moved, **no planned-note, split, density, or cross-ref decision is affected**: the
feishu→2 split still holds (3934w > 2500w), the weixin keep-as-1 call still holds (2657w single-BB
procedure), all 8 notes remain within the ≤2500w / ≤6 code / ≤400 line caps, and the cross-ref floor
(subsequently raised 2026-06-19 to the FOUR-FLOOR ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note) is
content-grounded against this same mirror. **Plan remains READY.** (PROVENANCE re-verification only — no
substantive plan change.)

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 FOUR-FLOOR) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed 2026-06-19 FOUR-FLOOR, 9/9 READY) · Execute: pending · Re-synced 2026-06-19 (counts unchanged)

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/{feishu,weixin,wecom,wecom-callback,dingtalk,yuanbao,qqbot}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
