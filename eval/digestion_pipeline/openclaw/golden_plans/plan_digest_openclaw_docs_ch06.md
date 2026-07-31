---
title: Sub-Plan ch06 — OpenClaw Docs: Channels (WeChat, WhatsApp, Yuanbao, Zalo family)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/wechat", "channels/whatsapp", "channels/yuanbao", "channels/zalo", "channels/zaloclawbot", "channels/zalouser"]
---

# Sub-Plan ch06: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup-before-create, 9-GATE validation, undigested-terms
> ownership, cross-reference set, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master.

## Scope

The six tail-of-alphabet OpenClaw **chat-channel** pages: WeChat/Weixin (external Tencent plugin), WhatsApp
(production-ready via WhatsApp Web / Baileys — by far the largest, most operationally detailed channel page),
Tencent Yuanbao (WebSocket bot), and the three Zalo-family integrations — Zalo Bot API (`zalo`), Zalo ClawBot
(`zaloclawbot`, external owner-bound plugin), and Zalo Personal (`zalouser`, unofficial `zca-js`). These are
**procedure-dominant** channel onboarding/operations docs (install → login → access control → delivery →
troubleshooting), with WhatsApp adding a distinct runtime/delivery **behavior model**.

Priority **P2** (Phase B — features/integration). The conceptual channel vocabulary these pages reference
(channel docking, channel routing, pairing, groups, access groups, multi-agent routing) is owned by Phase-A/
earlier-channel sub-plans (co01, ch01–ch05) and by the code-side `repo_openclaw_channels*` notes — LINKED, not
recreated here.

**Source**: OpenClaw docs, 6 pages, 9,508 measured words. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| WeChat | `channels/wechat` | 725 | 11 | 9 | 0 | procedure |
| WhatsApp | `channels/whatsapp` | 4,162 | 16 | 21 | 0 | procedure + model (split ×3) |
| Yuanbao | `channels/yuanbao` | 1,423 | 14 | 9 | 23 | procedure |
| Zalo | `channels/zalo` | 1,527 | 2 | 14 | 3 | procedure |
| Zalo ClawBot | `channels/zaloclawbot` | 556 | 5 | 7 | 4 | procedure |
| Zalo personal | `channels/zalouser` | 1,115 | 5 | 12 | 1 | procedure |

Fence counts are raw `grep -c '^```'` ÷ 2 (WhatsApp 32/2=16, Yuanbao 28/2=14, WeChat 22/2=11, ZaloClawBot
10/2=5, Zalouser 10/2=5, Zalo 4/2=2). Total raw words across the six pages: 9,508.

## Content Strategy

- **Prioritize**: (1) the WhatsApp **runtime/delivery model** (reconnect watchdog, Baileys socket timings,
  session scoping, media/PTT pipeline, reactions/ack/lifecycle) — it is the richest, most reusable channel
  behavior in this set; (2) access-control/activation patterns (DM policy, group policy, mention gating,
  pairing) that recur across all six channels; (3) external-plugin install/login flows (WeChat, ZaloClawBot)
  which differ from bundled channels.
- **Split**: only `whatsapp.md` (4,162w, 21 H2, mixed procedure+model) splits — into 3 notes (setup/access
  procedure · runtime/delivery model · operations procedure). See Split Decisions. The other five pages each
  map to exactly 1 note (each ≤1,527w, single procedure BB).
- **Link-out (not duplicated)**: shared channel concepts → `repo_openclaw_channels*` + sibling/earlier `oc_*`
  channel notes + `term_*` (pairing/access-control/webhook/etc.); plugin install mechanics →
  `plugins/*` sub-plans (pl-series); gateway config-channels reference → `gw01`/`gw02`. Provider/model
  vocabulary (LLM, Claude) is LINKED via existing `term_*`, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_wechat.md` | procedure | wechat.md: Naming, How it works, Install, Login, Access control, Compatibility, Sidecar process, Troubleshooting, Related docs | 600 | Connecting OpenClaw to WeChat/Weixin via Tencent's external `@tencent-weixin/openclaw-weixin` channel plugin: id/naming, the plugin-vs-core contract, install/QR-login, pairing access control, version compatibility, sidecar-process cleanup, and troubleshooting. |
| 2 | `oc_channels_whatsapp_setup.md` | procedure | whatsapp.md: Install (on demand), Quick setup, Deployment patterns, Access control and activation, Plugin hooks and privacy, Personal-number and self-chat behavior | 700 | Installing and onboarding the WhatsApp (Baileys) channel: on-demand plugin install, QR setup, dedicated- vs personal-number deployment, DM/group access policies + mention/activation gating, plugin-hook privacy opt-in, and self-chat safeguards. |
| 3 | `oc_channels_whatsapp_runtime_delivery.md` | model | whatsapp.md: Runtime model, Message normalization and context, Delivery/chunking/media, Reply quoting, Reaction level, Acknowledgment reactions, Lifecycle status reactions | 750 | The WhatsApp runtime/delivery behavior model: Gateway-owned socket + reconnect watchdog, Baileys `web.whatsapp.*` timings, DM/group/newsletter session scoping, inbound envelope + media normalization, text chunking, PTT/Ogg-Opus media pipeline, reply quoting, and the reaction/ack/lifecycle-status emoji slot. |
| 4 | `oc_channels_whatsapp_operations.md` | procedure | whatsapp.md: Approval prompts, Configured ACP bindings, Multi-account and credentials, Tools/actions/config writes, Troubleshooting, System prompts, Configuration reference pointers | 700 | Operating WhatsApp at scale: exec/plugin approval reactions, persistent ACP `bindings[]`, multi-account credential paths + logout, action gates, the troubleshooting playbook (reconnect loops, proxy QR timeouts, ignored group messages, Bun warning), per-scope system-prompt resolution, and config-reference field map. |
| 5 | `oc_channels_yuanbao.md` | procedure | yuanbao.md: Quick start, Access control, Configuration examples, Common commands, Troubleshooting, Advanced configuration, Configuration reference, Supported message types, Related | 700 | Connecting Tencent Yuanbao bots over WebSocket: `appKey:appSecret` setup, DM/group access policies + mention gating, outbound queue/merge-text tuning, native slash-command menus, multi-account routing, streaming/markdown-hint/reply-to options, supported message types, and the full config reference. |
| 6 | `oc_channels_zalo.md` | procedure | zalo.md: Bundled plugin, Quick setup, What it is, Setup (fast path), How it works, Limits, Access control (DMs/Groups), Long-polling vs webhook, Supported message types, Capabilities, Delivery targets, Troubleshooting, Configuration reference | 700 | Configuring the Zalo Bot API channel (Marketplace/Bot-Creator bots): bundled-plugin status, bot-token setup, deterministic routing, DM pairing + group-policy schema (groups unavailable for Marketplace bots), long-polling vs webhook mode, the Marketplace-bot capability matrix, delivery targets, and the legacy-vs-accounts config reference. |
| 7 | `oc_channels_zaloclawbot.md` | procedure | zaloclawbot.md: Compatibility, Prerequisites, Install with onboard, Manual Installation, How It Works, Under the Hood, Troubleshooting | 550 | Setting up Zalo ClawBot via the external `@zalo-platforms/openclaw-zaloclawbot` plugin: Mini-App QR login, onboard vs manual install (catalog-integrity-verified), the owner-bound private-bot model on shared official OA infrastructure, the long-polling `getUpdates` runtime, and QR/version troubleshooting. |
| 8 | `oc_channels_zalouser.md` | procedure | zalouser.md: Bundled plugin, Quick setup, What it is, Naming, Finding IDs, Limits, Access control (DMs), Group access, Multi-account, Environment variables, Typing/reactions/acks, Troubleshooting, Related | 650 | Automating a personal Zalo account via in-process `zca-js` (unofficial, ban-risk): QR login, directory-CLI peer/group ID discovery, ID-only DM/group access control with the `dangerouslyAllowNameMatching` break-glass, mention gating, profile-based multi-account + env-var resolution, and typing/reaction/ack behavior. |

## Section Coverage Map

```
wechat.md (725w)
├── Naming ─────────────────────────────────────────── → note 1 (oc_channels_wechat)
├── How it works ───────────────────────────────────── → note 1
├── Install ────────────────────────────────────────── → note 1
├── Login ──────────────────────────────────────────── → note 1
├── Access control ─────────────────────────────────── → note 1
├── Compatibility ──────────────────────────────────── → note 1
├── Sidecar process ────────────────────────────────── → note 1
├── Troubleshooting ────────────────────────────────── → note 1
└── Related docs ───────────────────────────────────── → note 1 (## References)
whatsapp.md (4,162w) — SPLIT ×3
├── Install (on demand) ────────────────────────────── → note 2 (whatsapp_setup)
├── Quick setup ────────────────────────────────────── → note 2
├── Deployment patterns ────────────────────────────── → note 2
├── Access control and activation ──────────────────── → note 2
├── Plugin hooks and privacy ───────────────────────── → note 2
├── Personal-number and self-chat behavior ─────────── → note 2
├── Runtime model ──────────────────────────────────── → note 3 (whatsapp_runtime_delivery)
├── Message normalization and context ──────────────── → note 3
├── Delivery, chunking, and media ──────────────────── → note 3
├── Reply quoting ──────────────────────────────────── → note 3
├── Reaction level ─────────────────────────────────── → note 3
├── Acknowledgment reactions ───────────────────────── → note 3
├── Lifecycle status reactions ─────────────────────── → note 3
├── Approval prompts ───────────────────────────────── → note 4 (whatsapp_operations)
├── Configured ACP bindings ────────────────────────── → note 4
├── Multi-account and credentials ──────────────────── → note 4
├── Tools, actions, and config writes ──────────────── → note 4
├── Troubleshooting ────────────────────────────────── → note 4
├── System prompts ─────────────────────────────────── → note 4
├── Configuration reference pointers ───────────────── → note 4
└── Related ────────────────────────────────────────── → notes 2-4 (## References)
yuanbao.md (1,423w)
├── Quick start (+ Interactive setup) ──────────────── → note 5 (oc_channels_yuanbao)
├── Access control (Direct messages, Group chats) ──── → note 5
├── Configuration examples (6× H3) ─────────────────── → note 5
├── Common commands ────────────────────────────────── → note 5
├── Troubleshooting (4× H3) ────────────────────────── → note 5
├── Advanced configuration (8× H3) ─────────────────── → note 5
├── Configuration reference ────────────────────────── → note 5
├── Supported message types (Receive/Send/Threads) ─── → note 5
└── Related ────────────────────────────────────────── → note 5 (## References)
zalo.md (1,527w)
├── Bundled plugin ─────────────────────────────────── → note 6 (oc_channels_zalo)
├── Quick setup (beginner) ─────────────────────────── → note 6
├── What it is ─────────────────────────────────────── → note 6
├── Setup (fast path) (2× H3) ──────────────────────── → note 6
├── How it works (behavior) ────────────────────────── → note 6
├── Limits ─────────────────────────────────────────── → note 6
├── Access control (DMs / Groups) ──────────────────── → note 6
├── Long-polling vs webhook ────────────────────────── → note 6
├── Supported message types ────────────────────────── → note 6
├── Capabilities ───────────────────────────────────── → note 6
├── Delivery targets (CLI/cron) ────────────────────── → note 6
├── Troubleshooting ────────────────────────────────── → note 6
├── Configuration reference (Zalo) ─────────────────── → note 6
└── Related ────────────────────────────────────────── → note 6 (## References)
zaloclawbot.md (556w)
├── Compatibility ──────────────────────────────────── → note 7 (oc_channels_zaloclawbot)
├── Prerequisites ──────────────────────────────────── → note 7
├── Install with onboard (recommended) ─────────────── → note 7
├── Manual Installation (4× H3) ────────────────────── → note 7
├── How It Works ───────────────────────────────────── → note 7
├── Under the Hood ─────────────────────────────────── → note 7
└── Troubleshooting ────────────────────────────────── → note 7
zalouser.md (1,115w)
├── Bundled plugin ─────────────────────────────────── → note 8 (oc_channels_zalouser)
├── Quick setup (beginner) ─────────────────────────── → note 8
├── What it is ─────────────────────────────────────── → note 8
├── Naming ─────────────────────────────────────────── → note 8
├── Finding IDs (directory) ────────────────────────── → note 8
├── Limits ─────────────────────────────────────────── → note 8
├── Access control (DMs) ───────────────────────────── → note 8
├── Group access (optional) (+ mention gating H3) ──── → note 8
├── Multi-account ──────────────────────────────────── → note 8
├── Environment variables ──────────────────────────── → note 8
├── Typing, reactions, and delivery acknowledgements ─ → note 8
├── Troubleshooting ────────────────────────────────── → note 8
└── Related ────────────────────────────────────────── → note 8 (## References)
```
No orphaned sections. Shared channel concepts (pairing, groups, channel-routing, multi-agent) are referenced
via existing `repo_openclaw_channels*` / `term_*` / earlier-channel `oc_*`, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| whatsapp.md (4,162w, 21 H2, 16 fences, mixed procedure+model) | notes 2 + 3 + 4 | Exceeds the 2,500-word and 6-code-block caps and mixes three distinct task/BB clusters: a setup/access **procedure** (2), a runtime/delivery/reactions **behavior model** (3), and an operations/troubleshooting **procedure** (4). Splitting keeps one BB per note, each ≤750w and ≤6 code blocks, and isolates the reusable runtime-behavior model from the onboarding procedure. |
| wechat.md / yuanbao.md / zalo.md / zaloclawbot.md / zalouser.md | 1 note each | Each ≤1,527w, ≤14 fences, single procedure BB; no split needed. (Yuanbao at 14 raw fences and Zalo each map to one note but reproduce config snippets selectively to stay ≤6 fences — see Density Re-Assessment.) |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (9,508 measured words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (notes 1, 2, 4, 5, 6, 7, 8) · **model ×1** (note 3, WhatsApp runtime/delivery).
- Est. digest words ~5,350 (avg ~669/note); every note ≤750w, well under the 2,500w / 400-line cap.
- Source code fences (53 total across 6 pages) distribute across the 8 notes; each note reproduces config/CLI
  snippets selectively and verbatim to stay ≤6 fences (WhatsApp's 16 fences split across notes 2-4; Yuanbao's
  14 reduced to representative examples).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every planned note maps **≥8 terms · ≥10 snippets ·
  per-link relevance statement. Actual per-note: 10t/10–12s/10d (zalouser 11t). See **Per-Note Related Notes
  Mapping (LOCKED)**.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Every cited EXISTING note_id was `sqlite3`-verified against the unified DB. Sibling `oc_*` docs (this series)
> do NOT exist yet → cited as "(planned, this series)" toward the 10-doc floor; **≥5 of the 10 docs per note
> ACP corpus). `entry_openclaw_docs` is "(planned, master pre-step W1)". Relative paths from a note at
> `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`, sibling `oc_` → `./`,
> cc/hermes/band doc → `../<folder>/`, repo → `../../../areas/code_repos/`, snippet → `../../code_snippets/`,
> entry → `../../../0_entry_points/`. `term_environment_variable` confirmed MISSING (not cited; zalouser env
> vars covered in prose + `term_authentication`).

### oc_channels_wechat (10t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: WeChat is one OpenClaw channel; the external plugin registers channel id `openclaw-weixin` with the Gateway.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin discovery/metadata declaration; relevance: the Gateway discovers the external plugin's manifest and loads its entrypoint (How it works step 2).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — channel-plugin contract surface; relevance: the page's premise is OpenClaw's generic channel-plugin contract vs Tencent's external WeChat runtime.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel inbound→route→outbound dispatch core; relevance: WeChat inbound messages are normalized through the channel contract and routed by the kernel.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/login; relevance: QR login stores the WeChat account token locally before any access checks.
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: WeChat DMs reuse the standard pairing+allowlist model (`pairing list/approve`).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — unknown-sender pairing-code approval; relevance: the exact `openclaw pairing list/approve openclaw-weixin <CODE>` flow this page documents.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: install pulls `@tencent-weixin/openclaw-weixin` from npm; `legacy`/`latest` dist-tags by compatibility line.
- [Bot](../../term_dictionary/term_bot.md) — chat bot account; relevance: WeChat runs as an OpenClaw bot account, monitored per-account by the plugin.
- [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — sibling agent's plugin model; relevance: cross-ecosystem analog of the external-channel-plugin install/load contract WeChat uses.

**Docs**
- [Channels Overview](../claude_code/cc_channels_overview.md) — coding-agent chat-channel model; relevance: parallel "agent reachable from a chat platform" framing for the WeChat channel.
- [Build a Channel](../claude_code/cc_build_a_channel.md) — authoring a channel integration; relevance: the channel-plugin authoring contract WeChat's external plugin satisfies.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link procedure; relevance: install→enable→login→restart parallels the WeChat setup steps.
- [Plugin Marketplaces and Install](../claude_code/cc_plugin_marketplaces_and_install.md) — installing third-party plugins; relevance: external-package install analog to `openclaw plugins install`.
- [Hermes Weixin Gateway Setup](../hermes_agent/hermes_gateway_weixin_setup.md) — sibling agent's WeChat/Weixin gateway; relevance: closest existing doc — same WeChat platform, same QR-login + per-account-monitor pattern.
- [Hermes WeCom Setup](../hermes_agent/hermes_gateway_wecom_setup.md) — Tencent WeCom (enterprise WeChat) channel; relevance: adjacent Tencent messaging surface with the same plugin-credential model.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging-gateway inbound/outbound architecture; relevance: the normalize→route→outbound path WeChat's plugin plugs into.
- [Hermes Plugins Management](../hermes_agent/hermes_plugins_management.md) — plugin install/enable/version lifecycle; relevance: external-plugin install + enable + compatibility-version checks WeChat requires.
- [oc_channels_zaloclawbot](oc_channels_zaloclawbot.md) (planned, this series) — sibling external-plugin channel; relevance: same external-plugin-beside-the-Gateway QR-login install pattern.
- [Hermes WeCom Callback Setup](../hermes_agent/hermes_gateway_wecom_callback_setup.md) — Tencent WeCom callback/credential onboarding; relevance: adjacent Tencent messaging surface with the same plugin-credential + callback-registration onboarding model as the WeChat plugin.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: defines the generic channel-plugin contract the external WeChat plugin implements.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel impl; relevance: code-side analog of the inbound-normalize → route → outbound path this page describes.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding/CLI; relevance: `plugins install`, `channels login`, `gateway restart` are wizard/CLI surfaces.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: loads the external WeChat catalog plugin beside the Gateway.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract an external channel plugin (WeChat) satisfies to register and route.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the access-control model WeChat DMs reuse verbatim.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: normalizes the `openclaw-weixin` channel/account ids at registration.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: how a normalized WeChat inbound message reaches the routed agent.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/session resolution; relevance: maps an inbound WeChat DM to its session.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: the Gateway-discovers-manifest → load-entrypoint path (How it works step 2).
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: `gateway restart` re-loads the plugin and starts its per-account monitor.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile/respawn lifecycle; relevance: the sidecar/stale-Gateway cleanup bug (#68451) excludes self+ancestors to avoid restart loops.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: external-plugin trust/compatibility gating at load.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `plugins install/list`, `channels login/status`, `gateway restart` command surfaces.

### oc_channels_whatsapp_setup (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: WhatsApp is a first-class OpenClaw channel installed on demand.
- [Access Control](../../term_dictionary/term_access_control.md) — DM/group sender authorization; relevance: `dmPolicy`/`groupPolicy`/`allowFrom`/`groupAllowFrom` + mention/activation gating are this note's core.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM access policy enum; relevance: `pairing`/`allowlist`/`open`/`disabled` is the exact `channels.whatsapp.dmPolicy` schema.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing-code DM gate; relevance: default `pairing` mode + `pairing approve` first-contact flow.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — group/thread admission + sender policy; relevance: two-layer group membership allowlist + group sender policy + mention layering.
- [Authentication](../../term_dictionary/term_authentication.md) — channel linking; relevance: QR-based WhatsApp Web login links the session before policies apply.
- [PII](../../term_dictionary/term_pii.md) — personal data; relevance: plugin-hook privacy gates inbound `message_received` payloads carrying numbers/names/content.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — minimize data exposure; relevance: opt-in-only plugin-hook broadcast is a data-minimization control for untrusted plugins.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent routing; relevance: deployment patterns + activation route DMs/groups to agent-main vs isolated group sessions.
- [npm](../../term_dictionary/term_npm.md) — package source; relevance: install resolves `@openclaw/whatsapp` from ClawHub with npm fallback.

**Docs**
- [Hermes WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — sibling agent's Baileys WhatsApp channel; relevance: closest existing doc — same WhatsApp Web/Baileys QR-link + dedicated-number setup.
- [Hermes WhatsApp Cloud Setup](../hermes_agent/hermes_messaging_whatsapp_cloud_setup.md) — WhatsApp Cloud API channel onboarding; relevance: contrast Cloud-API vs Web/Baileys setup paths.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link procedure; relevance: install→link→approve parallels WhatsApp onboarding.
- [Channels Overview](../claude_code/cc_channels_overview.md) — chat-channel model; relevance: framing for a DM/group-gated agent channel.
- [Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access governance; relevance: allowlist/policy/privacy controls parallel to WhatsApp access config.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway inbound/outbound; relevance: the access-gate→route path WhatsApp setup wires.
- [Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — channel approval/permission relay; relevance: activation/approval gating layered on the channel.
- [oc_channels_whatsapp_runtime_delivery](oc_channels_whatsapp_runtime_delivery.md) (planned, this series) — runtime/delivery model; relevance: continues this note — once linked, runtime behavior takes over.
- [oc_channels_whatsapp_operations](oc_channels_whatsapp_operations.md) (planned, this series) — operations; relevance: ACP bindings + multi-account credentials build on this setup.
- [Slack Setup and Routing](../claude_code/cc_slack_setup_and_routing.md) — chat-channel install + DM/channel routing setup; relevance: parallel install→link→route + DM/channel access-gating onboarding for a chat channel.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements the DM/group policy + activation gating this note configures.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel impl; relevance: WhatsApp/Baileys lives in the messaging-channel family.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding; relevance: `onboard` / `channels add` / `channels login` install-and-link flow.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the exact pairing-vs-allowlist DM gate WhatsApp uses.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — group/thread policy; relevance: group membership allowlist + sender policy + mention activation layering.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract the on-demand WhatsApp plugin implements to register.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: `allowFrom` E.164 normalization + account-id normalization at registration.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: resolves DM/group/account matches against configured policy.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM access audit; relevance: audits the DM allowlist/pairing posture WhatsApp setup configures.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: audits group/sender source authorization.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: on-demand install loads the external WhatsApp runtime.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — plugin hook config payload; relevance: the opt-in `pluginHooks.messageReceived` privacy gate.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/session resolution; relevance: DM-main vs group-isolated session selection after admission.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `onboard`, `channels add/login`, `pairing list/approve` surfaces.

### oc_channels_whatsapp_runtime_delivery (10t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the Gateway owns the WhatsApp socket, reconnect loop, and session scoping described here.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent transport; relevance: WhatsApp Web (Baileys) runs over a long-lived socket whose transport activity drives the reconnect watchdog + `web.whatsapp.*` timings.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — persistent socket connection mode; relevance: the keep-alive/connect-timeout/query-timeout socket model for the linked-device session.
- [Push to Talk](../../term_dictionary/term_pushtotalk.md) — PTT voice-note delivery; relevance: outbound audio uses the Baileys `ptt: true` Ogg/Opus push-to-talk path.
- [Text to Speech](../../term_dictionary/term_text_to_speech.md) — TTS/voice output; relevance: `/tts latest`/`/tts chat` send replies as PTT voice notes (MP3/WebM transcoded to Ogg/Opus).
- [Speech to Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: authorized group voice notes are transcribed before mention gating.
- [Message Queue](../../term_dictionary/term_message_queue.md) — outbound buffering; relevance: text chunking + batched reply quoting + queued delivery are the outbound queue behavior.
- [Markdown](../../term_dictionary/term_markdown.md) — text formatting; relevance: `chunkMode` `length`/`newline` splits formatted text on paragraph boundaries.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — once-only delivery dedupe; relevance: a reply is "sent" only after Baileys returns an outbound message id; ack reactions are independent of delivery confirmation.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live voice-note transcription; relevance: inbound `<media:audio>` group notes are transcribed inline before mention/reply gating.

**Docs**
- [Hermes WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — sibling Baileys runtime; relevance: closest existing doc — same socket/reconnect/media-delivery behavior model.
- [Hermes WhatsApp Cloud Model](../hermes_agent/hermes_messaging_whatsapp_cloud_model.md) — WhatsApp Cloud delivery model; relevance: contrast Cloud-API delivery semantics with Web/Baileys delivery.
- [Hermes Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media delivery/transcode settings; relevance: media size caps, transcode, voice-note delivery analog.
- [Hermes STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text pipeline; relevance: the inbound voice-note transcription step before mention gating.
- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the outbound voice-note (PTT) generation path.
- [Band WebSocket Overview](../band/band_websocket_overview.md) — persistent agent WebSocket transport; relevance: reference model for a long-lived socket with keep-alive/reconnect.
- [Band WebSocket Agent Channels](../band/band_websocket_agent_channels.md) — agent channel events over WS; relevance: socket-borne inbound/outbound event scoping analog.
- [Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — channel outbound reply mechanics; relevance: outbound reply/quoting + delivery-confirmation parallel.
- [oc_channels_whatsapp_setup](oc_channels_whatsapp_setup.md) (planned, this series) — setup; relevance: the access/link layer this runtime sits on top of.
- [Hermes Platform Media Tools](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media/outbound-send tool reference; relevance: the outbound media/voice-note + chunked-text send tooling parallel to the WhatsApp delivery pipeline (PTT/Ogg-Opus, media normalization, chunking).

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements the reconnect watchdog, session-scope JIDs, and media normalization.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging impl; relevance: inbound-envelope + media-placeholder normalization + chunking live here.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/media path; relevance: the PTT/Ogg-Opus transcode + voice-note delivery is the voice-channel media pipeline.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session scoping; relevance: DM-main vs group-isolated vs newsletter-channel session metadata (`agent:<id>:whatsapp:...`).

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — lifecycle status reactions; relevance: the single bot-reaction-slot lifecycle (queued/thinking/tool/done/error) this note documents.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/session resolution; relevance: maps an inbound WhatsApp message to its DM/group/newsletter session.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — sibling socket transport; relevance: comparable keep-alive/reconnect transport for a long-lived messaging socket.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WebSocket connection management; relevance: the persistent-socket connect/keep-alive/reconnect machinery.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound chat send; relevance: the chunked/queued outbound send + delivery-id confirmation.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript/media pipeline; relevance: inbound media normalization (`<media:image>`…) + saved `MediaPath`.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — pending group-history injection; relevance: buffered group messages injected as context when the bot is triggered.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat/buffered delta; relevance: streaming/buffered outbound delta + heartbeat analog to the watchdog window.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: outbound image auto-optimization to fit media caps.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: voice-note → transcript relay before gating.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — audio media stream; relevance: Ogg/Opus audio handling for PTT voice-note delivery.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: the inbound audio→text transcription path.

### oc_channels_whatsapp_operations (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: operations (approvals, ACP bindings, multi-account, config writes) are OpenClaw Gateway features surfaced on WhatsApp.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client protocol; relevance: persistent `bindings[]` of `type: "acp"` route specific WhatsApp peers/groups to an ACP agent (`codex`).
- [Access Control](../../term_dictionary/term_access_control.md) — sender authorization; relevance: approval approvers + manual `/approve` still pass the WhatsApp sender-authorization path; ordered group checks.
- [Authentication](../../term_dictionary/term_authentication.md) — credentials; relevance: multi-account credential paths (`creds.json`/`.bak`), legacy migration, logout clearing auth state.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy fronting transport; relevance: QR login times out behind `HTTPS_PROXY`/`NO_PROXY`; standard proxy env on the Gateway host.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — per-account credential management; relevance: per-account `creds.json` auth dirs + default-account selection + migration.
- [Cron](../../term_dictionary/term_cron.md) — scheduled delivery; relevance: scheduled automation/heartbeat fallback uses explicit targets/`allowFrom`; doctor flags stale crontab `ensure-whatsapp.sh`.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent routing; relevance: a matched ACP binding owns the route; system-prompt maps resolve per group/peer/account.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: ACP-bound `codex` agent acts as a per-peer delegated runtime.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: ACP session existence is ensured after gating; per-scope system prompts attach to persisted sessions.

**Docs**
- [Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — channel approval/permission relay; relevance: the exec/plugin approval-reaction forwarding model.
- [Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel governance/controls; relevance: approval/config-write gates + sender authorization controls.
- [Hermes Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — command-approval flow; relevance: the exec-approval (`👍`/`👎`) reaction + `/approve` model.
- [Hermes Security Isolation Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: multi-account credential-path isolation + logout clearing auth.
- [Hermes Profiles Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-account/profile routing; relevance: per-account routing + per-scope prompt analog.
- [Hermes Subagent Delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating to a sub-runtime; relevance: ACP-bound agent ownership of a route.
- [Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway env config; relevance: `HTTPS_PROXY`/`NO_PROXY` proxy-env troubleshooting for QR login.
- [oc_channels_whatsapp_setup](oc_channels_whatsapp_setup.md) (planned, this series) — setup; relevance: access policies set up there gate the operations here.
- [oc_channels_whatsapp_runtime_delivery](oc_channels_whatsapp_runtime_delivery.md) (planned, this series) — runtime/delivery; relevance: the runtime layer the troubleshooting playbook diagnoses.
- [Hermes Credential Pools](../hermes_agent/hermes_credential_pools.md) — per-account credential pool management; relevance: the multi-account credential paths (`creds.json`/`.bak`), default-account selection, and logout-clears-auth model this note operates.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements binding match, approval forwarding, and config-write gating.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: ACP session existence ensured after gating; per-scope system prompts attach to sessions.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: approval prompts, config-write gates, sender authorization are security-surface controls.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding routing; relevance: the `bindings[]` match → route resolution WhatsApp ACP bindings use.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: resolves a channel/account/peer match (direct E.164 / group JID) to its binding.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP bindings; relevance: the exact persisted `type: "acp"` `bindings[]` this note configures.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: the exec/plugin approval prompt + reaction resolution path.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets handling; relevance: multi-account credential-path resolution + secret handling.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy-aware client connect; relevance: proxy-env handling for QR login behind a proxy.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload/apply; relevance: channel-initiated config writes (`configWrites`) applied at runtime.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — session send policy; relevance: per-scope send/system-prompt resolution attaching to sessions.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM access audit; relevance: audits the approval-approver allowlist posture.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor/cron repair; relevance: `openclaw doctor` flagging stale crontab `ensure-whatsapp.sh` entries.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP session handoff; relevance: ensuring the configured ACP session exists before the bound route runs.

### oc_channels_yuanbao (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the OpenClaw Yuanbao channel plugin connects Tencent Yuanbao bots over WebSocket.
- [WebSocket](../../term_dictionary/term_websocket.md) — transport; relevance: WebSocket is the only supported connection mode for Yuanbao.
- [Access Control](../../term_dictionary/term_access_control.md) — DM/group authorization; relevance: `dm.policy` (open/allowlist/pairing/disabled) + group `requireMention` gating.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM policy enum; relevance: the `dm.policy` `open`/`allowlist`/`pairing`/`disabled` schema and `allowFrom` list.
- [Authentication](../../term_dictionary/term_authentication.md) — credentials; relevance: `appKey:appSecret` signing/ticket generation, pre-signed token option, App-Secret-leak rotation.
- [Message Queue](../../term_dictionary/term_message_queue.md) — outbound delivery tuning; relevance: `outboundQueueStrategy` (immediate vs merge-text) with `minChars`/`maxChars`/`idleMs` buffering.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent routing; relevance: `bindings[]` route Yuanbao DMs/groups to different agents by peer kind/id.
- [Markdown](../../term_dictionary/term_markdown.md) — formatting; relevance: `markdownHintEnabled` injects anti-code-block-wrapping instructions.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: Yuanbao bots (created in-app) are the channel entities; multi-account `accounts.<id>`.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — chat-to-agent gateway; relevance: Yuanbao plugs into the messaging-gateway inbound→route→outbound model.

**Docs**
- [Hermes Yuanbao Gateway Setup](../hermes_agent/hermes_gateway_yuanbao_setup.md) — sibling agent's Yuanbao gateway; relevance: closest existing doc — same Yuanbao platform, appKey/appSecret + WebSocket setup.
- [Hermes Weixin Gateway Setup](../hermes_agent/hermes_gateway_weixin_setup.md) — Tencent Weixin gateway; relevance: adjacent Tencent bot-platform channel with the same credential/signing model.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway architecture; relevance: the normalize→policy→route→outbound path Yuanbao configures.
- [Channels Overview](../claude_code/cc_channels_overview.md) — chat-channel model; relevance: framing for a DM/group-gated bot channel.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link; relevance: add-token + restart-gateway onboarding parallel.
- [Band Chat Rooms and Routing](../band/band_chat_rooms_and_routing.md) — multi-room agent routing; relevance: DM/group routing + per-peer agent binding analog.
- [Band WebSocket Overview](../band/band_websocket_overview.md) — agent WebSocket transport; relevance: the persistent WS connection model Yuanbao requires.
- [Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — outbound reply mechanics; relevance: outbound chunking/merge + reply-to-quote behavior.
- [oc_channels_wechat](oc_channels_wechat.md) (planned, this series) — sibling Tencent channel; relevance: same Tencent vendor, contrasting external-plugin (WeChat) vs WebSocket-bot (Yuanbao).
- [Hermes DingTalk Gateway Setup](../hermes_agent/hermes_gateway_dingtalk_setup.md) — adjacent Chinese bot-platform gateway; relevance: comparable appKey/appSecret-signed bot-platform channel with DM/group access + token-based onboarding.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements the policy/mention gating + outbound strategy this note configures.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging impl; relevance: inbound normalization + supported message types (text/image/file/audio/video/sticker).

**Snippets**
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: normalizes the Yuanbao channel config/account ids at registration.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding routing; relevance: the multi-agent `bindings[]` routing Yuanbao uses by `match.peer.kind`.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the `dm.policy` pairing/allowlist gate Yuanbao reuses.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — group/thread policy; relevance: group `requireMention` + sender gating layering.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: dispatch of a normalized Yuanbao inbound to the routed agent.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WebSocket connection; relevance: the persistent WS connect/keep-alive the Yuanbao channel needs.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send handler; relevance: the merge-text/immediate outbound queue + 3000-char split.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets; relevance: `appKey:appSecret` signing + pre-signed token resolution.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: maps inbound Yuanbao DM/group to its session.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status reactions/streaming; relevance: block-level streaming + reply-to quoting outbound behavior.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `channels add/login`, `pairing list/approve`, native slash-command menus.

### oc_channels_zalo (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the Zalo Bot API channel is owned by the OpenClaw Gateway.
- [Webhook](../../term_dictionary/term_webhook.md) — webhook ingress; relevance: webhook mode (`webhookUrl`/`webhookSecret`/`webhookPath`, `X-Bot-Api-Secret-Token`, HTTPS, replay window) vs default long-polling.
- [Access Control](../../term_dictionary/term_access_control.md) — DM/group authorization; relevance: `dmPolicy` pairing default + group-policy schema (fail-closed `allowlist`) — groups unavailable for Marketplace bots.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing-code DM gate; relevance: default `pairing` mode; unknown senders ignored until approved (codes expire 1h).
- [Authentication](../../term_dictionary/term_authentication.md) — bot token; relevance: bot token (`numeric_id:secret`) from Zalo Bot Platform, `tokenFile` (symlinks rejected), env `ZALO_BOT_TOKEN`.
- [Replay Attack](../../term_dictionary/term_replay_attack.md) — duplicate-event defense; relevance: duplicate webhook events (`event_name + message_id`) are ignored for a short replay window.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — burst control; relevance: burst webhook traffic is rate-limited per path/source (HTTP 429).
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: Marketplace/Bot-Creator bots are the supported Zalo bot surface (vs OA bots).
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — once-only handling; relevance: getUpdates polling and webhook are mutually exclusive; deterministic routing back to the same chat.
- [WAF](../../term_dictionary/term_waf.md) — web-facing request filtering; relevance: HTTPS webhook ingress with secret-token verification + 429 rate-limiting is a web-edge control surface.

**Docs**
- [Hermes Webhooks Routes Security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook route + secret verification; relevance: closest existing doc — HTTPS webhook with secret-token header verification.
- [Hermes Webhooks Routing Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook routing/delivery; relevance: webhook event routing + delivery analog to Zalo's webhook mode.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link; relevance: bundled-plugin enable + bot-token + restart onboarding parallel.
- [Channels Overview](../claude_code/cc_channels_overview.md) — chat-channel model; relevance: framing for a DM-gated bot channel with deterministic routing.
- [Hermes Messaging Line](../hermes_agent/hermes_messaging_line.md) — LINE bot-token channel; relevance: comparable Asia-market bot-token + webhook/long-poll messaging channel.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway architecture; relevance: long-polling/webhook ingress → normalize → route path.
- [Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel governance; relevance: webhook-secret/HTTPS + token-file controls.
- [Hermes QQBot Setup](../hermes_agent/hermes_gateway_qqbot_setup.md) — Tencent QQ bot channel; relevance: adjacent bot-platform channel with token + webhook setup.
- [oc_channels_zalouser](oc_channels_zalouser.md) (planned, this series) — sibling Zalo personal channel; relevance: contrast official-bot-API (`zalo`) vs unofficial personal-account (`zalouser`).
- [Hermes Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — bot-token channel with long-polling vs webhook ingress; relevance: closest bot-token analog — `numeric_id:secret` token + long-polling/`getUpdates` vs webhook mode mirror Zalo's setup exactly.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements the DM/group policy + long-polling/webhook ingress for Zalo.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging impl; relevance: inbound envelope normalization + 2000-char chunking + capability matrix.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: webhook secret/HTTPS verification + symlink-rejecting token file are security controls.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the pairing-default DM gate Zalo reuses.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook signature verify; relevance: the `X-Bot-Api-Secret-Token` HTTPS webhook verification model.
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay cache; relevance: duplicate `event_name + message_id` ignored for a replay window.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS server listen; relevance: the Gateway HTTP endpoint handling webhook requests at `webhookPath`.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: routes inbound webhook POSTs to the Zalo plugin handler.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit policy; relevance: burst webhook traffic rate-limited per path/source (HTTP 429).
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: legacy flat-key vs `accounts.<id>` config normalization at registration.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: deterministic routing back to the same Zalo chat.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — group/thread policy; relevance: the schema-present (Marketplace-unavailable) group-policy/allowlist layering.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets; relevance: bot-token resolution from env/config/`tokenFile` (symlink-rejected).
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send; relevance: 2000-char outbound chunking + `message send --channel zalo` delivery target.

### oc_channels_zaloclawbot (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: OpenClaw connects to Zalo ClawBot via the external `@zalo-platforms/openclaw-zaloclawbot` plugin.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — catalog/plugin entry; relevance: install uses the official catalog with integrity-hash verification of the pinned package.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — supply-chain install attack; relevance: catalog integrity-hash pinning of the exact version defends against substituted packages.
- [Authentication](../../term_dictionary/term_authentication.md) — QR login; relevance: Mini-App QR login (token `zbsk`) binds the bot to the owner's Zalo User ID.
- [Access Control](../../term_dictionary/term_access_control.md) — owner-bound restriction; relevance: the bot communicates ONLY with its owner; other users' messages are dropped at the platform level.
- [npm](../../term_dictionary/term_npm.md) — package install; relevance: pinned npm install `@zalo-platforms/openclaw-zaloclawbot@0.1.4` against the catalog integrity hash.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped package namespace; relevance: the `@zalo-platforms/…` scoped package + npm-plugin install ledger.
- [Node.js](../../term_dictionary/term_node_js.md) — runtime prerequisite; relevance: requires Node.js >= 22 and OpenClaw >= 2026.4.10 for the npm-plugin ledger.
- [Bot](../../term_dictionary/term_bot.md) — personal assistant bot; relevance: an owner-bound private bot provisioned under shared official OA infrastructure.
- [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — sibling external-plugin model; relevance: cross-ecosystem analog of an external catalog plugin loaded beside the gateway.

**Docs**
- [Plugin Marketplaces and Install](../claude_code/cc_plugin_marketplaces_and_install.md) — installing from a marketplace; relevance: catalog-verified install of an external plugin.
- [Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest/metadata; relevance: the catalog entry + integrity hash + compatibility version the install verifies.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link; relevance: onboard-vs-manual install + QR login + restart parallel.
- [Hermes Plugins Management](../hermes_agent/hermes_plugins_management.md) — plugin install/enable/version; relevance: external-plugin install + enable + version-compatibility checks.
- [Hermes Weixin Gateway Setup](../hermes_agent/hermes_gateway_weixin_setup.md) — Tencent QR-login channel; relevance: comparable QR-login external-channel onboarding (different platform).
- [Hermes Security Isolation Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential-state isolation; relevance: the external plugin's sensitive credential-state directory handling.
- [Channels Overview](../claude_code/cc_channels_overview.md) — chat-channel model; relevance: framing for an owner-bound private-bot channel.
- [Hermes Messaging Line](../hermes_agent/hermes_messaging_line.md) — Asia-market bot-platform channel; relevance: adjacent bot-platform channel with managed onboarding.
- [oc_channels_wechat](oc_channels_wechat.md) (planned, this series) — sibling external-plugin channel; relevance: same external-plugin-beside-Gateway QR-login pattern (different platform).
- [Plugin Marketplace Walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — end-to-end marketplace plugin install walkthrough; relevance: the onboard-vs-manual catalog install + integrity-verified pinned-version flow this external plugin follows.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: hosts the external-channel-plugin load + long-poll `getUpdates` runtime.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding; relevance: `openclaw onboard` (recommended) and manual `plugins install` / `channels login` flow.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: loads the external catalog plugin beside the Gateway and manages its credential state directory.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract this external plugin satisfies to register the channel.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — QR/pairing-style binding; relevance: comparable QR-bound device/owner pairing flow (`zbsk` token).
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: catalog integrity-hash verification of the pinned package at install.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: surfaces trust/integrity issues for an external catalog plugin.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: loads the external `openclaw-zaloclawbot` entrypoint beside the Gateway.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: `gateway restart` brings the channel up after enable.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets; relevance: the plugin's bot-credential state under the OpenClaw state dir.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: owner-only inbound mapped directly to the local agent runtime.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `onboard`, `plugins install`, `config set`, `channels login`, `gateway restart` surfaces.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: long-poll `getUpdates` inbound dispatched client-side to the agent.

### oc_channels_zalouser (11t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host product; relevance: the personal-Zalo channel automates a user account in-process via `zca-js` inside OpenClaw.
- [Access Control](../../term_dictionary/term_access_control.md) — ID-only authorization; relevance: `dmPolicy`/`groupPolicy` use stable Zalo IDs; `dangerouslyAllowNameMatching` is the break-glass for name matching.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM policy enum; relevance: `channels.zalouser.dmPolicy` `pairing`/`allowlist`/`open`/`disabled` schema.
- [Authentication](../../term_dictionary/term_authentication.md) — QR login + profiles; relevance: QR login on the Gateway machine; profile names select saved login credentials in state.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent/group routing; relevance: accounts map to profiles; group/DM access gates which messages reach the agent.
- [Blocklist / Safelist](../../term_dictionary/term_blocklist_safelist.md) — allowlist authorization model; relevance: ID-only `allowFrom`/`groupAllowFrom` + `accessGroup:<name>` static sender access groups.
- [npm](../../term_dictionary/term_npm.md) — package install; relevance: bundled plugin, or `@openclaw/zalouser` install for older/custom builds.
- [TypeScript](../../term_dictionary/term_typescript.md) — JS/TS runtime library; relevance: runs fully in-process via the JS `zca-js` library (no external `zca`/`openzca` CLI binary).
- [Node.js](../../term_dictionary/term_node_js.md) — runtime; relevance: in-process Node runtime hosting `zca-js` event listeners + outbound sends.
- [Bot](../../term_dictionary/term_bot.md) — personal-account automation; relevance: automates a personal Zalo user (unofficial), distinct from the official `zalo` bot channel.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — privacy/ban-risk; relevance: an unofficial integration with account-suspension risk; ID-only auth limits exposure.

**Docs**
- [Hermes Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — account-linked personal messaging channel; relevance: comparable personal-account (vs bot-API) linked channel with QR/device login.
- [Hermes Messaging Line](../hermes_agent/hermes_messaging_line.md) — Asia-market messaging channel; relevance: adjacent platform; contrast official-API vs personal-account integration.
- [Channels Setup](../claude_code/cc_channels_setup.md) — channel install/link; relevance: bundled-plugin enable + QR login + restart onboarding parallel.
- [Channels Overview](../claude_code/cc_channels_overview.md) — chat-channel model; relevance: framing for a DM/group-gated personal-account channel.
- [Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel governance; relevance: ID-only allowlist + break-glass name-matching controls.
- [Hermes Profiles Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — profile/multi-account routing; relevance: accounts→profiles mapping + env-var profile selection.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway architecture; relevance: in-process event-listener inbound → policy → route path.
- [Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — outbound reply mechanics; relevance: outbound text/media/link sends + typing/reaction/ack behavior.
- [oc_channels_zalo](oc_channels_zalo.md) (planned, this series) — sibling official Zalo channel; relevance: contrast official-bot-API vs unofficial personal-account integration.
- [Hermes BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — personal-account, device-linked unofficial messaging integration; relevance: closest analog — an unofficial, account/device-linked personal-messaging channel (not a bot API) with QR/device login and ID-based addressing.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: implements the personal-account channel's policy/mention gating + reactions.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging impl; relevance: inbound event listeners + outbound text/media/link sends + typing/ack behavior.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: the bundled `zalouser` plugin's in-process load + profile state.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: the DM access model (pairing default, ID-only allowlist) zalouser reuses.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — group/thread policy; relevance: group allowlist + per-group `requireMention` resolution order.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: resolves ID-only sender/group matches; ignores raw names unless break-glass enabled.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalization; relevance: account→profile normalization + name→ID resolution at startup.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: maps inbound zalouser DM/group event to its session.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reactions; relevance: the `react` action + typing/delivered/seen ack behavior.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets; relevance: `ZALOUSER_PROFILE`/`ZCA_PROFILE` profile → saved-login-credential resolution.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM access audit; relevance: audits the ID-only DM allowlist posture + name-matching break-glass risk.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted external content; relevance: handling untrusted inbound from an unofficial personal-account integration.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: in-process load of the bundled `zalouser` (`zca-js`) plugin.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: `directory self/peers/groups`, `channels login/logout`, `pairing list/approve` surfaces.

## Undigested Terms Plan

> Per master: OpenClaw channel vocabulary is the subject of these doc pages, so it is digested as `oc_*`
> documentation notes, NOT promoted to new `term_dictionary` entries. The only `term_dictionary` interaction
> is LINKING existing terms. Expected new `term_dictionary` captures: **0**.

| Term (appears in source) | Disposition |
|---|---|
| WeChat / Weixin (`openclaw-weixin`) | Documented in `oc_channels_wechat` (channel-specific). Link `term_openclaw`. No new term (channel name, not a reusable cross-cutting concept). |
| WhatsApp / Baileys / WhatsApp Web | Documented across notes 2-4. Link `term_websocket` for the socket transport. No new term (vendor channel + library name). |
| Tencent Yuanbao | Documented in `oc_channels_yuanbao`. No new term (channel name). |
| Zalo / Zalo Bot API / Marketplace bot / OA | Documented in `oc_channels_zalo`. No new term (channel/product surface name). |
| Zalo ClawBot (`zaloclawbot`) / Zalo Mini App | Documented in `oc_channels_zaloclawbot`. No new term (channel name + platform feature). |
| Zalo personal (`zalouser`) / `zca-js` | Documented in `oc_channels_zalouser`. No new term (channel name + library). |
| ACP bindings | Link existing `term_acp_agent_client_protocol`. No new term. |
| reactions / ack reactions / lifecycle status reactions | Documented in note 3. Link `snippet_openclaw_channels_status_reactions`. No reusable-term gap that ch06 should own. |
| webhook / long-polling / `getUpdates` | Link existing `term_webhook` + `term_rate_limiting` + `term_replay_attack`. (`term_long_polling` MISSING but is channel-mechanism detail covered in-note; not ch06-owned.) |
| PTT / Ogg-Opus voice notes / TTS | Link existing `term_text_to_speech` + `term_speech_to_text`. No new term. |
| E.164 numbers / JIDs / chat ids | Channel-addressing detail; documented in-note. No reusable-term capture (no existing `term_e164`/`term_phone_number`; not cross-cutting enough for ch06 to own). |

**New-term candidates: none.** No genuinely reusable, cross-cutting term lacking a doc-page home AND an existing
note surfaced. The recurring access-control / pairing / webhook concepts are already covered by existing terms
or by Phase-A channel-concept sub-plans (co01, ch01–ch05) and `repo_openclaw_channels*`; ch06 LINKS them.

## Term-Note Authoring Requirements

**N/A (0 new terms).** ch06 authors zero `term_dictionary` notes. Requirement inherited from master: any new
`acronym_glossary_*.md`. No glossary edits required for ch06.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must pass before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean for all 8 notes (YAML field order, itemized keywords/topics, quoted year tags, `## Overview` + `## Related Notes` + `## References` + bold footer present). |
| G2 | Grounding | Each note diffs faithfully against `inbox/openclaw_docs/channels/<page>.md` (no invented config keys/CLI flags; config snippets reproduced verbatim). |
| G3 | Density + Coverage | Every note ≤400 lines / ≤2,500 words / ≤6 code blocks, one building_block; every source H2/H3 mapped (Section Coverage Map, no orphans). |
| G4 | Cross-Reference | Each note ≥6 relevance-selected `term_dictionary` links + relevant `repo_openclaw*` / sibling `oc_*` / `snippet_openclaw_channels_*`, each with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 | `note_links` query confirms in-degree ≥1 per new note (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_wechat oc_channels_whatsapp_setup oc_channels_whatsapp_runtime_delivery oc_channels_whatsapp_operations oc_channels_yuanbao oc_channels_zalo oc_channels_zaloclawbot oc_channels_zalouser"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format + link errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"
  done
  # source_url present
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"
  fi
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling-prefix discoverability (≥1 oc_ link)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING oc_ LINK: $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G8: ghost + in-degree (after incremental reindex)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_channels_wechat | procedure | 600 | ≤6 (11 src fences → selective) | ✅ |
| 2 | oc_channels_whatsapp_setup | procedure | 700 | ≤6 | ✅ |
| 3 | oc_channels_whatsapp_runtime_delivery | model | 750 | ≤6 | ✅ |
| 4 | oc_channels_whatsapp_operations | procedure | 700 | ≤6 | ✅ |
| 5 | oc_channels_yuanbao | procedure | 700 | ≤6 (14 src fences → representative examples) | ✅ |
| 6 | oc_channels_zalo | procedure | 700 | ≤6 (2 src fences) | ✅ |
| 7 | oc_channels_zaloclawbot | procedure | 550 | ≤6 (5 src fences) | ✅ |
| 8 | oc_channels_zalouser | procedure | 650 | ≤6 (5 src fences) | ✅ |

No note approaches the 2,500-word / 400-line cap. The only over-cap source page (whatsapp.md, 4,162w/16
fences) is split ×3 so each resulting note stays ≤750w and ≤6 fences. Code-heavy WeChat (11) and Yuanbao (14)
reproduce only representative config/CLI snippets to keep each ≤6.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as a master pre-step W1, `building_block:
navigation`) under the **Channels** section — a "Channels (ch06): WeChat, WhatsApp, Yuanbao, Zalo family"
cluster. Each new note receives its entry-point back-link at finalization (satisfies G7/G8). No new entry
point is created by ch06 (the docs hub already exceeds the >30-note threshold corpus-wide). Parent-hub wiring

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):

- `entry_openclaw_docs.md` (planned W1) → all 8 notes (primary anti-island inbound link).
- `repo_openclaw_channels.md` → all 8 (the code-side channel runtime ↔ docs cross-link).
- `repo_openclaw_channels_messaging.md` → notes 1, 2, 3, 5, 6, 8 (messaging-channel impl).
- `repo_openclaw_channels_voice_phone.md` → note 3 (WhatsApp PTT/voice-note media path).
- `repo_openclaw_extensions.md` → notes 1, 7 (external catalog plugins: WeChat, ZaloClawBot).
- `repo_openclaw_sessions.md` → notes 3, 4 (WhatsApp session scoping + ACP/system-prompt sessions).
- `repo_openclaw_security.md` → notes 4, 6 (approval/config-write gates; Zalo webhook secret/HTTPS).
- `term_openclaw.md` → all 8 (each is an OpenClaw channel).
- `term_acp_agent_client_protocol.md` → note 4 (WhatsApp ACP bindings).
- `term_webhook.md` → note 6 (Zalo webhook mode).
- `term_websocket.md` → notes 3, 5 (WhatsApp Web socket; Yuanbao WebSocket).

is the one planned (W1) target.

## Pacing Rules (inherited from master)

Single execution phase, 8 notes — one dynamic-workflow wave (well under the ~30-agent fan-out cap). Pilot one
note (`oc_channels_wechat`, smallest external-plugin page) + calibrate gates before fanning out. Re-read each
source page; reproduce config/CLI snippets verbatim; one BB per note. Incremental reindex; verify `note_links`
+ 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit+push after the
phase; no Claude co-author trailer.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced `## Candidate Cross-References` with `## Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)` carrying the raised standard **≥8 terms · ≥10 snippets · ≥10 docs per
note** (relevance-selected from a fresh re-read of all six source pages under
`inbox/openclaw_docs/channels/`; no padding). Every cited EXISTING note_id was `sqlite3`-verified against the
(256 existing-resolved + 18 planned `oc_*` siblings / `entry_openclaw_docs`). Relative paths were computed
from the note location `resources/documentation/openclaw/oc_X.md` and re-resolved during the ghost scan.
Updated the Summary Statistics cross-ref line to record the new floors + ghost-count.

**Per-note locked counts (terms / snippets / docs [existing-of-10] / repos · floors met).**

| Note | Terms | Snippets | Docs (existing) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_channels_wechat | 10 | 10 | 10 (8) | 4 | ✅ |
| oc_channels_whatsapp_setup | 10 | 11 | 10 (7) | 3 | ✅ |
| oc_channels_whatsapp_runtime_delivery | 10 | 12 | 10 (8) | 4 | ✅ |
| oc_channels_whatsapp_operations | 10 | 11 | 10 (7) | 3 | ✅ |
| oc_channels_yuanbao | 10 | 11 | 10 (8) | 3 | ✅ |
| oc_channels_zalo | 10 | 11 | 10 (8) | 3 | ✅ |
| oc_channels_zaloclawbot | 10 | 10 | 10 (8) | 3 | ✅ |
| oc_channels_zalouser | 11 | 11 | 10 (8) | 3 | ✅ |

remainder being planned `oc_*` siblings + the planned `entry_openclaw_docs` hub.

**Term-pool expansion (≥6 → ≥8+, raised).** The original draft floor (≥6 terms) was lifted by adding
`term_dm_pairing`, `term_channel_kernel`, `term_thread_binding_policy`, `term_socket_mode`,
`term_messaging_gateway`, `term_pushtotalk`, `term_realtime_transcription`, `term_idempotency_key`,
`term_credential_pool`, `term_subagent`, `term_session_persistence`, `term_blocklist_safelist`, `term_waf`,
`term_dependency_confusion`, `term_npm_scoping`, `term_hermes_plugin`. Snippet/doc floors were met by
voice-call / ACP snippet corpus and the `claude_code/cc_*` + `hermes_agent/hermes_*` + `band/band_*`
coding-agent doc corpora (e.g. `hermes_gateway_weixin_setup`, `hermes_gateway_yuanbao_setup`,
`hermes_messaging_whatsapp_baileys`, `hermes_webhooks_routes_security`).

**New-term candidates + best-fit glossary.** **None.** Re-read Step 2d surfaced no genuinely reusable,
cross-cutting term lacking BOTH a doc-page home AND an existing note. All recurring concepts (pairing, DM/group
policy, mention gating, webhook/long-polling, PTT/TTS, ACP bindings, reactions) are already owned by existing
terms (`term_access_control`, `term_dm_policy`, `term_dm_pairing`, `term_thread_binding_policy`, `term_webhook`,
`term_text_to_speech`, `term_speech_to_text`, `term_acp_agent_client_protocol`, `term_status`-via-snippet) or
by Phase-A channel-concept sub-plans + `repo_openclaw_channels*`. Channel-name terms (WeChat/WhatsApp/Yuanbao/
Zalo/Baileys/zca-js) remain digested as `oc_*` docs per the master's design decision, not promoted. Confirmed
`term_environment_variable` MISSING (NOT cited; zalouser `ZALOUSER_PROFILE`/`ZCA_PROFILE` covered in prose +
`term_authentication` + `snippet_openclaw_gateway_call_credentials_secrets`). Expected new `term_dictionary`
captures: **0** — best-fit glossary N/A (no captures), consistent with the master Undigested-Terms ownership rule.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors) | **PASS** | Per-Note Related Notes Mapping (LOCKED): all 8 notes 10–11 terms / 10–12 snippets / 10 docs, each link carries a `— desc; relevance: …` statement; floors ≥8t·≥10s·≥10d met (see Augmentation Report table). |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7 Discoverability, G8 In-degree ≥1; `grep` confirms rows G1–G8 all present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 8 rows to `entry_openclaw_docs.md` (master pre-step W1, `building_block: navigation`) under a Channels (ch06) cluster; each note gets its back-link at finalization (G7/G8). No new entry point created by ch06. |
| CP4 | Size (≤30 or split) | **PASS** | 8 notes, single execution phase — far under the 30-note / 30-agent fan-out cap. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master `## Format Definition`, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer; YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`). |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: every note ≤750w / ≤6 fences / 1 BB; the only over-cap source (whatsapp.md 4,162w/16 fences) is split ×3 (setup procedure / runtime model / operations procedure), each ≤750w ≤6 fences; code-heavy WeChat(11)/Yuanbao(14) reproduce representative snippets only. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured all six pages from `inbox/openclaw_docs/channels/`: wechat 725w/11f, whatsapp 4,162w/16f, yuanbao 1,423w/14f, zalo 1,527w/2f, zaloclawbot 556w/5f, zalouser 1,115w/5f — EXACT match to the plan's Source table (ratio 1.00 each). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (channel vocab digested as `oc_*`, link-existing-only, expected 0 new terms) + `## Term-Note Authoring Requirements` present (N/A 0 new terms, inherits `/tessellum-capture-term-note` mandate from master). New-term scan re-run at augment → 0 candidates. |
| CP8f | Slug specificity / collision (all-notes dedup) | **PASS** | No new `term_*` slugs to audit (0 captures). Doc-note collision audit: all 8 planned `oc_channels_*` slugs are channel-specific, no existing `documentation/openclaw/oc_*` notes (folder empty in DB) and no `term_*` duplicate of a planned doc-note concept (channel names link `term_openclaw` + channel snippets/repos, never recreated). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing → new)` maps ≥1 outside-folder inbound link to every new note (`entry_openclaw_docs` → all 8; `repo_openclaw_channels` → all 8; `repo_openclaw_channels_messaging` → 1/2/3/5/6/8; voice_phone → 3; extensions → 1/7; sessions → 3/4; security → 4/6; `term_openclaw` → all 8). G8 in-degree ≥1 check in the gate table + Validation Scripts. |

occurrences (256 existing-resolved + 18 planned). Status advanced `pending → ready`.
