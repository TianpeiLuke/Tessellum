---
title: Sub-Plan ch04 — OpenClaw Docs: Channels (MS Teams, Nextcloud Talk, Nostr, Pairing, QA Channel, QQ Bot, Signal)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/msteams", "channels/nextcloud-talk", "channels/nostr", "channels/pairing", "channels/qa-channel", "channels/qqbot", "channels/signal"]
---

# Sub-Plan ch04: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*` prefix), format (YAML order + `## Overview` … `## Related Notes` …
> `## References` + bold footer), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), the
> Undigested-Terms ownership rule (OpenClaw vocab → `oc_*` doc notes, not new `term_dictionary`), the 9-GATE, and the
> cross-reference link set are ALL inherited from the master. This file holds the measured source, per-note table,
> section coverage map, split decisions, candidate cross-refs, and the single-phase gate.

## Scope

The 7 chat-channel integration pages assigned to ch04 — six platform connectors (Microsoft Teams, Nextcloud Talk,
Nostr, QA Channel, QQ Bot, Signal) plus the cross-channel **pairing** page (DM access approval + node device pairing).
Each platform page is operator-facing setup + configuration + access-control + behavior reference for connecting that
chat surface to the OpenClaw gateway; `pairing` is the shared inbound-access/device-trust procedure those channels
reference. Priority **P2** (Phase B — features/integration). The code-side counterparts
`repo_openclaw_channels` / `repo_openclaw_channels_messaging` / `repo_openclaw_channels_voice_phone` are LINKED, not
recreated; this sub-plan adds the **product/user documentation** for these channels.

**Source**: OpenClaw docs, 7 pages, **12,862 measured words**. **Planned: 9 notes** (msteams splits 3-way; the other 6
pages = 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| MS Teams | channels/msteams | 5,883 | 36 | 30 | 35 | procedure (3-way split: setup / federated-auth / messaging+access) |
| Nextcloud Talk | channels/nextcloud-talk | 715 | 8 | 8 | 0 | procedure |
| Nostr | channels/nostr | 896 | 11 | 13 | 9 | procedure |
| Pairing | channels/pairing | 1,155 | 4 | 3 | 9 | procedure |
| QA Channel | channels/qa-channel | 509 | 4 | 4 | 0 | procedure |
| QQ Bot | channels/qqbot | 1,498 | 10 | 9 | 4 | procedure |
| Signal | channels/signal | 2,206 | 14 | 20 | 0 | procedure |

> Code = `grep -c '```' ÷ 2`. msteams 72/2=36 · nextcloud-talk 16/2=8 · nostr 22/2=11 · pairing 8/2=4 ·
> qa-channel 8/2=4 · qqbot 20/2=10 · signal 28/2=14. Total source words **12,862**; total fences **87**.

## Content Strategy

- **Prioritize**: connect-this-channel setup procedures (credentials, gateway config, access control) — the operational
  payload every channel page leads with — and the cross-channel **pairing** approval/device-trust flow these pages
  reference for inbound DM access.
- **Split**: `msteams.md` (5,883 w, 30 H2 / 35 H3, **far over the 2,500-word cap**) → THREE procedure notes along its
  natural task clusters: (a) install + quick setup + config + env vars, (b) federated authentication (certificate /
  managed identity / AKS workload identity), (c) messaging behavior + access control + manifest/RSC/Graph + files +
  troubleshooting. See Split Decisions.
- **Keep 1 note**: nextcloud-talk (715 w), nostr (896 w), pairing (1,155 w), qa-channel (509 w), qqbot (1,498 w),
  signal (2,206 w) — each under the cap and single-BB (procedure).
- **Link-out (don't redefine)**: provider/plugin install mechanics → plugins sub-plans (pl-series); gateway
  webhook/secrets/tunnel internals → gw-series; voice STT/TTS for QQ Bot → nodes/tools series; cross-channel
  access-groups/group-messages/bot-loop-protection (ch01–ch02) → those sibling notes. Existing terms
  (`term_oauth_token`, `term_iam`, `term_encryption`, `term_webhook`, `term_qr_code`→absent so link `term_authentication`,
  `term_docker`, `term_tls`, `term_vpn`) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_msteams_setup.md` | procedure | msteams.md: Bundled plugin, Quick setup (Teams CLI, devtunnel, app create, configure, install, verify), Config writes, Local development (tunneling), Testing the Bot, Environment variables, Configuration | 650 | Connecting Microsoft Teams to OpenClaw: bundled-plugin install, the `@microsoft/teams.cli` quick-setup flow (login, devtunnel/ngrok/tailscale tunnel, app create → CLIENT_ID/SECRET/TENANT_ID, configure `channels.msteams`, install in Teams, `teams app doctor`), config-write paths, local-dev tunneling, and the `MSTEAMS_*` env vars. |
| 2 | `oc_channels_msteams_federated_auth.md` | procedure | msteams.md: Federated authentication (certificate plus managed identity) — How it works, Steps 1–7 (Azure Bot, credentials, endpoint, Teams channel, manifest, configure, run), Option A certificate-based, Option B Azure Managed Identity, AKS Workload Identity Setup, Auth type comparison | 600 | Production-grade Teams auth without client secrets: certificate-based authentication and Azure Managed Identity (workload identity), the 7-step Azure Bot registration path, AKS workload-identity setup, and the auth-type comparison (secret vs certificate vs managed identity). |
| 3 | `oc_channels_msteams_messaging.md` | procedure | msteams.md: Access control (DMs + groups), Member info action, History context, Current Teams RSC permissions (manifest), Example Teams manifest, Capabilities RSC vs Graph, Graph-enabled media + history, Known limitations, Routing and sessions, Reply style threads vs posts, Attachments and images, Sending files in group chats (+ SharePoint), Polls (Adaptive Cards), Presentation cards, Target formats, Proactive messaging, Team and Channel IDs, Private channels, Troubleshooting | 700 | Teams messaging behavior + access model: DM/group access control, RSC-only vs Microsoft Graph capabilities (+ manifest permissions), routing/sessions, thread-vs-post reply style, attachments/images, SharePoint-backed group-chat file sending, Adaptive-Card polls + presentation cards, proactive messaging, team/channel ID gotchas, and troubleshooting. |
| 4 | `oc_channels_nextcloud_talk.md` | procedure | nextcloud-talk.md: Bundled plugin, Quick setup (beginner), Notes, Access control (DMs), Rooms (groups), Capabilities, Configuration reference | 450 | Connecting a Nextcloud Talk instance to OpenClaw: bundled-plugin install, beginner quick setup (bot account + app password + base URL), DM access control, room/group handling, capability matrix, and the full Nextcloud Talk configuration reference. |
| 5 | `oc_channels_nostr.md` | procedure | nostr.md: Bundled plugin (+ older/custom installs), Quick setup (+ non-interactive), Configuration reference, Profile metadata, Access control (DM policies, allowlist), Key formats, Relays (local relay), Protocol support, Testing (local relay, manual test), Troubleshooting, Security, Limitations (MVP) | 550 | Running OpenClaw as a Nostr bot: bundled-plugin install, interactive vs non-interactive key setup, configuration reference, profile metadata, DM-policy/allowlist access control, key formats (nsec/npub), relay configuration, supported NIPs, testing against a local relay, security notes, and MVP limitations. |
| 6 | `oc_channels_pairing.md` | procedure | pairing.md: 1) DM pairing (Approve a sender, Reusable sender groups, Where the state lives), 2) Node device pairing (Pair via Telegram, Approve a node device, Optional trusted-CIDR auto-approve, Node pairing state storage, Notes), Related docs | 600 | The two OpenClaw pairing flows: DM pairing (approving an inbound sender, reusable sender groups, where approval state lives) and node device pairing (iOS/Android/macOS/headless nodes — pair via Telegram, approve a device, trusted-CIDR auto-approve, and pairing-state storage). |
| 7 | `oc_channels_qa_channel.md` | procedure | qa-channel.md: What it does, Config, Runners, Related | 350 | The QA Channel: a synthetic/test channel for end-to-end QA automation of OpenClaw — what it does, its configuration, and the runner model that drives scripted conversations against the gateway. |
| 8 | `oc_channels_qqbot.md` | procedure | qqbot.md: Install, Setup, Configure (Multi-account setup, Group chats, Voice STT/TTS), Target formats, Slash commands, Engine architecture, QR-code onboarding, Troubleshooting, Related | 600 | Connecting QQ (Tencent QQ Bot) to OpenClaw: install + setup (AppID/secret), configuration including multi-account and group-chat handling, voice STT/TTS, target formats, slash commands, the engine architecture, QR-code onboarding, and troubleshooting. |
| 9 | `oc_channels_signal.md` | procedure | signal.md: Prerequisites, Quick setup, What it is, Config writes, The number model, Setup path A (link existing account via QR), Setup path B (register dedicated bot number via SMS, Linux), External daemon mode (httpUrl), Container mode (signal-cli-rest-api), Access control (DMs + groups), How it works, Media + limits, Typing + read receipts, Reactions, Approval reactions, Delivery targets, Troubleshooting, Security notes, Configuration reference | 700 | Connecting Signal to OpenClaw via signal-cli: the dedicated-number model, two setup paths (QR-link an existing account vs register a bot number by SMS), external-daemon and Docker container (`signal-cli-rest-api`) modes, DM/group access control, media limits, reactions + approval reactions, delivery targets, security notes, and the full Signal configuration reference. |

## Section Coverage Map

Every H2/H3 of every source page maps to a planned note; no orphans.

```
channels/msteams.md (5,883 w · 30 H2 · 35 H3)
├── Bundled plugin ─────────────────────────────────────────── → note 1 (oc_channels_msteams_setup)
├── Quick setup ────────────────────────────────────────────── → note 1
├── Goals ──────────────────────────────────────────────────── → note 1 (intro/Overview material)
├── Config writes ──────────────────────────────────────────── → note 1
├── Federated authentication (certificate plus managed identity) → note 2 (oc_channels_msteams_federated_auth)
│   ├── How it works / Step 1–7 / Option A cert / Option B MI / AKS Workload Identity / Auth type comparison → note 2
├── Local development (tunneling) ──────────────────────────── → note 1
├── Testing the Bot ────────────────────────────────────────── → note 1
├── Environment variables ──────────────────────────────────── → note 1
├── Configuration ──────────────────────────────────────────── → note 1
├── Access control (DMs + groups) ──────────────────────────── → note 3 (oc_channels_msteams_messaging)
├── Member info action / History context ───────────────────── → note 3
├── Current Teams RSC permissions (manifest) ───────────────── → note 3
│   ├── Manifest caveats / Updating an existing app ────────── → note 3
├── Example Teams manifest (redacted) ──────────────────────── → note 3
├── Capabilities: RSC only vs Graph (RSC only / RSC+Graph / RSC vs Graph API) → note 3
├── Graph-enabled media + history (required for channels) ───── → note 3
├── Known limitations (Webhook timeouts / cloud + service URL) → note 3
├── Routing and sessions / Reply style: threads vs posts (Formatting/Resolution precedence/Thread context) → note 3
├── Attachments and images ─────────────────────────────────── → note 3
├── Sending files in group chats (Why SharePoint / Setup / Sharing / Fallback / Files stored) → note 3
├── Polls (Adaptive Cards) / Presentation cards / Target formats → note 3
├── Proactive messaging ────────────────────────────────────── → note 3
├── Team and Channel IDs (Common Gotcha) / Private channels ─── → note 3
├── Troubleshooting (Common issues / Manifest upload errors / RSC permissions not working) → note 3
├── References ─────────────────────────────────────────────── → note 1/2/3 ## References (external URLs split by topic)
└── Related ────────────────────────────────────────────────── → all 3 notes' ## Related Notes

channels/nextcloud-talk.md (715 w · 8 H2)
├── Bundled plugin / Quick setup (beginner) / Notes ────────── → note 4 (oc_channels_nextcloud_talk)
├── Access control (DMs) / Rooms (groups) / Capabilities ───── → note 4
└── Configuration reference (Nextcloud Talk) / Related ─────── → note 4

channels/nostr.md (896 w · 13 H2 · 9 H3)
├── Bundled plugin (Older/custom installs) ─────────────────── → note 5 (oc_channels_nostr)
├── Quick setup (Non-interactive setup) / Configuration reference / Profile metadata → note 5
├── Access control (DM policies / Allowlist example) / Key formats → note 5
├── Relays (Local relay) / Protocol support ────────────────── → note 5
├── Testing (Local relay / Manual test) ────────────────────── → note 5
├── Troubleshooting (Not receiving / Not sending / Duplicate) ─ → note 5
└── Security / Limitations (MVP) / Related ─────────────────── → note 5

channels/pairing.md (1,155 w · 3 H2 · 9 H3)
├── 1) DM pairing (Approve a sender / Reusable sender groups / Where the state lives) → note 6 (oc_channels_pairing)
├── 2) Node device pairing (Pair via Telegram / Approve a node device / Trusted-CIDR auto-approve /
│   Node pairing state storage / Notes) ────────────────────── → note 6
└── Related docs ───────────────────────────────────────────── → note 6 ## Related Notes

channels/qa-channel.md (509 w · 4 H2)
├── What it does / Config / Runners / Related ──────────────── → note 7 (oc_channels_qa_channel)

channels/qqbot.md (1,498 w · 9 H2 · 4 H3)
├── Install / Setup / Configure (Multi-account / Group chats / Voice STT-TTS) → note 8 (oc_channels_qqbot)
├── Target formats / Slash commands / Engine architecture ──── → note 8
└── QR-code onboarding / Troubleshooting / Related ─────────── → note 8

channels/signal.md (2,206 w · 20 H2)
├── Prerequisites / Quick setup / What it is / Config writes / The number model → note 9 (oc_channels_signal)
├── Setup path A (link via QR) / Setup path B (register bot number, SMS, Linux) → note 9
├── External daemon mode (httpUrl) / Container mode (signal-cli-rest-api) → note 9
├── Access control (DMs + groups) / How it works / Media + limits → note 9
├── Typing + read receipts / Reactions / Approval reactions / Delivery targets → note 9
└── Troubleshooting / Security notes / Configuration reference (Signal) / Related → note 9
```

No orphaned sections. Cross-channel topics (access-groups, group-messages, bot-loop-protection) and gateway/plugin
internals are linked to their owning sub-plans, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| msteams.md (5,883 w, 30 H2 / 35 H3, 36 code fences) | notes 1 + 2 + 3 | **2.35× the 2,500-word cap** and 36 fences (6× the 6-fence cap). Three distinct task clusters: (1) get-it-running setup/config/env (procedure), (2) production federated authentication — certificate / managed identity / AKS (a self-contained Azure-auth procedure), (3) day-to-day messaging behavior + access/manifest/RSC-Graph/files/troubleshooting (procedure). Splitting keeps each note ≤700 w, ≤6 fences, single-BB, single task focus. |
| nextcloud-talk.md (715 w) | note 4 (1 note) | under cap, single procedure BB — no split. |
| nostr.md (896 w) | note 5 (1 note) | under cap, single procedure BB — no split. |
| pairing.md (1,155 w) | note 6 (1 note) | under cap; DM-pairing and node-device-pairing are two halves of one coherent "approve inbound access / trust a device" procedure — kept together for a complete pairing reference. |
| qa-channel.md (509 w) | note 7 (1 note) | small, single procedure BB — no split. |
| qqbot.md (1,498 w) | note 8 (1 note) | under cap, single procedure BB — no split. |
| signal.md (2,206 w) | note 9 (1 note) | under cap (≤2,500 w) and single procedure BB; setup paths A/B + daemon/container modes are alternatives within one connect-Signal procedure, kept together. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (12,862 measured words). New `oc_*` notes: **9**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×9** (all notes). No model/argument notes — these are operator setup/config references.
- Est. digest words ≈ **5,200** (avg ~580/note; range 350–700). 87 source code fences distribute across the 9 notes;
  the code-heavy msteams page (36 fences) splits 3-way and signal (14) stays 1 note — each note kept ≤6 fences by
  reproducing only the load-bearing config/CLI snippets verbatim.
- Cross-refs **LOCKED at xref-augment 2026-06-21** (see Per-Note Related Notes Mapping): every planned note meets the
  raised floor of **≥8 relevance-selected `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (≥5 EXISTING
  messaging 10/10/10 · nextcloud 8/10/10 · nostr 9/10/10 · pairing 10/11/10 · qa 8/10/10 · qqbot 10/10/10 ·
  signal 11/11/10.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21;
sibling `oc_*` "(planned, this series)". Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`:
term → `../../term_dictionary/term_Y.md`; sibling oc → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
`../../../areas/code_repos/repo_Y.md`; entry → `../../../0_entry_points/entry_Y.md`. `entry_openclaw_docs.md` is the
master **W1 pre-step** (created before execution). All EXISTING note_ids below were `sqlite3`-verified against the
notes table on 2026-06-21 (0 missing; only `term_session`/`term_nostr`/`term_qr_code`/`term_signal_protocol`/
`term_telegram`/`term_kubernetes`/`term_managed_identity`/`term_microsoft_graph`/`term_self_hosted`/`term_tunnel`/
`term_ngrok`/`term_tailscale` confirmed ABSENT — described in-note, never linked).

### oc_channels_msteams_setup (10t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: the product this note connects Microsoft Teams to.
- [Chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent on a chat surface; relevance: the Teams bot the gateway registers via `teams app create`.
- [Bot](../../term_dictionary/term_bot.md) — non-human messaging identity; relevance: the bot identity (App ID) Teams routes inbound activities to.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for delegated/app access; relevance: the `CLIENT_SECRET`/`appPassword` minted by the Entra ID app registration.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: the App ID + secret + tenant ID credential auth the bot uses against Bot Framework.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback for inbound events; relevance: the `/api/messages` endpoint (port 3978) Teams posts activities to.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — service bridging chat platforms to an agent backend; relevance: OpenClaw IS the gateway listening for Bot Framework webhook traffic.
- [M365 - Microsoft 365](../../term_dictionary/term_m365.md) — Microsoft's cloud productivity suite; relevance: Teams is an M365 surface; the bot lives in an Entra ID (Azure AD) tenant.
- [TLS](../../term_dictionary/term_tls.md) — transport-layer encryption; relevance: Teams requires an HTTPS tunnel endpoint (devtunnel/ngrok/tailscale funnel) — plaintext localhost is unreachable.
- [VPN](../../term_dictionary/term_vpn.md) — secure network tunnel; relevance: `tailscale funnel 3978` is one of the documented local-dev tunnel options to expose the bot.

**Docs**
- [Hermes: Microsoft Teams Bot Setup](../hermes_agent/hermes_messaging_teams_bot.md) — sibling coding-agent's Teams connector setup; relevance: the closest parallel connect-Teams procedure (app registration, webhook, credentials).
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how a channel ships as a bundled/installable plugin; relevance: msteams ships as a bundled plugin (`@openclaw/msteams`) — same install model.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/channel runtime architecture; relevance: explains the webhook-listener + channel-startup model this setup wires up.
- [Hermes: Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — token-based bot setup with tunneling; relevance: parallel token/tunnel quick-setup flow for a different channel.
- [Claude Code: Channels Setup](../claude_code/cc_channels_setup.md) — coding-agent channel-connection setup; relevance: the cross-tool analog of OpenClaw's connect-this-channel quick setup.
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — channel concepts + supported surfaces; relevance: situates Teams among coding-agent chat channels.
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — channel-plugin authoring; relevance: documents the channel-adapter boundary the msteams bundled plugin implements.
- [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md) — (planned, this series) production Teams auth; relevance: the secret-based setup here points to federated auth for production.
- [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md) — (planned, this series) Teams messaging/access; relevance: continuation once the bot is connected (access control, manifest, RSC/Graph).
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) DM pairing flow; relevance: `dmPolicy: "pairing"` (the default) gates unknown Teams senders.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channels code package; relevance: implements the Teams channel adapter documented here.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-connector subpackage; relevance: the msteams send/receive code path.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: hosts the `/api/messages` webhook listener and channel startup.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella repo; relevance: ships the bundled `@openclaw/msteams` plugin + CLI.

**Snippets**
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — Teams adapter config schema; relevance: the code-side of the `channels.msteams` config keys (appId/appPassword/tenantId/webhook).
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — Graph subscription handshake; relevance: the inbound webhook validation handshake Teams/Bot-Framework requires.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — generic webhook listener; relevance: the `/api/messages`-style HTTP intake pattern.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — per-platform build dispatch; relevance: how a bundled channel plugin is discovered + started.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — BasePlatformAdapter ABC; relevance: the channel-adapter interface the Teams adapter implements.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — interactive setup wizard; relevance: the `openclaw configure`/wizard path that writes `channels.msteams`.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential precedence + secret expansion; relevance: how `MSTEAMS_*` env vars vs config credentials resolve.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound send dispatch; relevance: the send path validated by `teams app doctor` / a test DM.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — tri-token socket-mode adapter; relevance: a sibling tunnel-free channel-connect adapter for contrast.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect handshake; relevance: parallel bot-connect/registration code path.

### oc_channels_msteams_federated_auth (10t · 10s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: the note's entire subject — secret vs certificate vs managed-identity bot auth.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer access token; relevance: federated auth replaces the static client secret with token acquisition from Entra ID / IMDS.
- [IAM](../../term_dictionary/term_iam.md) — identity & access management; relevance: Azure managed identity / AKS workload identity are IAM constructs the bot assumes.
- [Encryption](../../term_dictionary/term_encryption.md) — cryptographic protection; relevance: certificate-based auth uses a PEM keypair instead of a shared secret.
- [TLS](../../term_dictionary/term_tls.md) — transport security + certificates; relevance: the PEM certificate registered with the app registration is TLS-class credential material.
- [PKCE - Proof Key for Code Exchange](../../term_dictionary/term_pkce.md) — secretless OAuth code-exchange proof; relevance: federated/workload-identity auth is the bot-side analog of avoiding a stored client secret.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential/auth configuration; relevance: `authType: "secret"|"federated"` selects the bot's auth profile.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — managed set of rotating credentials; relevance: managed identity removes secret rotation — contrast with pooled static secrets.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization posture; relevance: passwordless auth is a hardening/access-posture choice for production deployments.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: OpenClaw uses `@azure/identity` to acquire IMDS tokens for the Teams SDK.

**Docs**
- [Hermes: Microsoft Graph App Registration](../hermes_agent/hermes_msgraph_app_registration.md) — Entra ID app registration + permissions; relevance: the same app-registration surface where you upload the certificate / create the federated credential.
- [Hermes: Azure Foundry Entra ID Provider](../hermes_agent/hermes_provider_azure_foundry_entra_id.md) — Entra ID / managed-identity auth for an Azure service; relevance: parallel managed-identity / workload-identity auth pattern on Azure.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential management for connectors; relevance: the secret-rotation problem federated auth eliminates.
- [Hermes: Secrets (Bitwarden)](../hermes_agent/hermes_secrets_bitwarden.md) — external secret storage; relevance: alternative to in-config secrets — contrast with passwordless managed identity.
- [Hermes: Env Vars — Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — auth env-var reference; relevance: the `MSTEAMS_AUTH_TYPE`/`MSTEAMS_CERTIFICATE_PATH`/`MSTEAMS_USE_MANAGED_IDENTITY` env-var family.
- [Claude Code: Authentication](../claude_code/cc_authentication.md) — coding-agent auth flows; relevance: the cross-tool view of credential-vs-token auth choices.
- [Claude Code: Amazon Bedrock Setup](../claude_code/cc_amazon_bedrock_setup.md) — cloud-IAM-backed credential setup; relevance: parallel cloud-IAM (instance/role) credentials vs static keys.
- [oc_channels_msteams_setup.md](oc_channels_msteams_setup.md) — (planned, this series) Teams quick setup; relevance: the secret-based default this note upgrades to federated for production.
- [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md) — (planned, this series) messaging + Graph permissions; relevance: Graph app permissions also live on the same app registration.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/auth code; relevance: implements the federated-auth + credential-handling code path.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: the msteams adapter's `authType` resolution lives here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: acquires IMDS tokens at runtime for bot authentication.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + auth profiles; relevance: hosts the auth-profile/credential ordering logic.

**Snippets**
- [snippet_hermes_agent_tools_msgraph](../../code_snippets/snippet_hermes_agent_tools_msgraph.md) — `MicrosoftGraphTokenProvider`; relevance: the Graph/Bot token-acquisition provider federated auth feeds.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth-mode resolution + authorization; relevance: the code that selects secret vs federated auth mode.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering + credential state; relevance: how the chosen `authType` credential is resolved.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth credential portability; relevance: token-based (vs secret) auth portability across deployments.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI credential source; relevance: the `@azure/identity`-style external token source pattern.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential-pool upsert; relevance: managing rotating secrets — the problem managed identity removes.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: certificate-path vs env-var vs managed-identity source selection.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential precedence + secret expansion; relevance: how cert path / MI client ID / secret precedence resolves.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helper functions; relevance: utility layer behind `authType` mode resolution.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE secretless OAuth flow; relevance: code analog of secretless (federated) credential acquisition.

### oc_channels_msteams_messaging (10t · 10s · 10d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: DM/group policy, allowlists, and team/channel scoping are this note's access model.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — direct-message access policy; relevance: `dmPolicy` (pairing/allowlist/open/disabled) + `allowFrom`/`groupAllowFrom` are core to Teams access control.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: this note documents the Teams bot's day-to-day messaging behavior.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: Teams markdown is limited (no tables/nested lists) — affects target-format rendering.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP event callback; relevance: webhook timeouts cause Teams retries/duplicates; proactive sends use stored `serviceUrl`.
- [Thread-Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — how replies bind to threads/sessions; relevance: `replyStyle` thread-vs-post resolution + thread-context preservation.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered message routing (`term_session` absent); relevance: routing/sessions deliver replies back to the originating conversation key.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling/timeout control; relevance: webhook processing timeouts and proactive-send constraints.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — app access token; relevance: Microsoft Graph Application permissions (file/history/media) require admin-consented tokens.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: OpenClaw renders Adaptive Cards, manages SharePoint file sends, and stores conversation references.

**Docs**
- [Hermes: Microsoft Teams Bot](../hermes_agent/hermes_messaging_teams_bot.md) — Teams messaging behavior + manifest; relevance: parallel coverage of RSC permissions, manifest, and Teams messaging.
- [Hermes: Microsoft Graph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — Graph change-notification listener; relevance: the Graph path enabling channel media/history this note describes.
- [Hermes: Teams Meetings Pipeline](../hermes_agent/hermes_messaging_teams_meetings_pipeline.md) — advanced Teams Graph/media pipeline; relevance: deeper Graph-backed Teams capabilities (media/history).
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — inbound routing + outbound delivery; relevance: the routing/sessions + proactive-delivery model.
- [Hermes: Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — attachments/media handling; relevance: attachments/images + SharePoint file-send behavior.
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — reply/send tool semantics; relevance: the cross-tool analog of the `message`/`presentation` send tool.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access/enterprise gating; relevance: the access-control posture parallel (allowlists, scopes).
- [Claude Code: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — per-channel permission propagation; relevance: per-team/per-channel tool-policy overrides documented here.
- [oc_channels_msteams_setup.md](oc_channels_msteams_setup.md) — (planned, this series) Teams setup; relevance: prerequisite connection these messaging behaviors run on.
- [oc_channels_msteams_federated_auth.md](oc_channels_msteams_federated_auth.md) — (planned, this series) Teams auth; relevance: Graph app permissions for media/history live on the same app registration.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements Teams access control, replyStyle, target formats.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging subpackage; relevance: the send/attach/poll/card delivery paths.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/routing code; relevance: routing/sessions + conversation-key derivation.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/manifest tooling; relevance: Teams app manifest + RSC permissions surface.

**Snippets**
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — Teams adapter config; relevance: the messaging-config keys (replyStyle, teams allowlist, actions).
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound format detection; relevance: markdown/HTML target-format rendering the note warns about.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch + retries; relevance: proactive-send + webhook-timeout retry behavior.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — attachment send; relevance: attachments/images + SharePoint file-send path.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — target-string DSL parse; relevance: the `user:`/`conversation:` target-format grammar.
- [snippet_hermes_agent_gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — session-key derivation; relevance: `agent:<id>:msteams:channel:<conv>` routing keys.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type classifier; relevance: DM-vs-channel-vs-group classification driving routing.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread spawn/idle policy; relevance: replyStyle thread vs top-level + thread-context preservation.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: the `allowFrom`/`dangerouslyAllowNameMatching` access logic.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash/command access policy; relevance: per-team/per-channel/per-sender tool-policy gating.

### oc_channels_nextcloud_talk (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: connects a Nextcloud Talk instance as a webhook bot.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: the Talk bot installed via `occ talk:bot:install`.
- [Bot](../../term_dictionary/term_bot.md) — messaging identity; relevance: the bot account that cannot initiate DMs (user must message first).
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: bot setup uses a shared secret + optional `apiUser`/`apiPassword` for room lookups.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: Talk is a webhook bot — `webhookPublicUrl`/port/path config is central.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: `dmPolicy`/`groupPolicy`/`allowFrom`/`rooms` allowlists.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — DM access policy; relevance: `dmPolicy: "pairing"` default + Nextcloud-user-ID allowlists.
- [Docker](../../term_dictionary/term_docker.md) — container runtime (`term_self_hosted` absent); relevance: Nextcloud is typically a self-hosted/containerized instance the gateway reaches.

**Docs**
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — bundled-plugin channel model; relevance: Talk ships as a bundled plugin (`@openclaw/nextcloud-talk`).
- [Hermes: Messaging Mattermost](../hermes_agent/hermes_messaging_mattermost.md) — self-hosted team-chat connector; relevance: closest parallel (self-hosted, room-based, webhook) channel.
- [Hermes: Messaging SimpleX](../hermes_agent/hermes_messaging_simplex.md) — self-hosted/decentralized chat connector; relevance: another self-hosted-server channel setup parallel.
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook intake + delivery; relevance: the webhook-bot inbound/outbound model.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/channel runtime; relevance: how a webhook channel is registered + started.
- [Claude Code: Channels Setup](../claude_code/cc_channels_setup.md) — channel connection setup; relevance: cross-tool analog of the beginner quick-setup flow.
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — channel-adapter authoring; relevance: the adapter boundary the Talk plugin implements.
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) DM pairing; relevance: `dmPolicy: "pairing"` issues a code unknown Talk senders must clear.
- [oc_channels_signal.md](oc_channels_signal.md) — (planned, this series) self-hosted-cli channel; relevance: sibling self-hosted/external-service channel with the same access-control shape.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the Nextcloud Talk adapter.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging subpackage; relevance: Talk send/receive (URL-only media) path.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: hosts the Talk webhook listener.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships the bundled `@openclaw/nextcloud-talk` plugin.

**Snippets**
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — BasePlatformAdapter ABC; relevance: the adapter interface the Talk webhook bot implements.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound message normalization; relevance: Talk webhook payloads normalized into the shared envelope.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — webhook listener; relevance: the inbound webhook intake Talk uses.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — per-platform build dispatch; relevance: how the bundled Talk plugin is discovered + started.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM policy + allowlist enforcement; relevance: `dmPolicy`/`allowFrom` matching by Nextcloud user ID.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: access-control resolution for Talk DMs.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — source-config + account metadata; relevance: per-account base-URL/secret config resolution.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — target-string DSL parse; relevance: room/DM target addressing for outbound sends.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — interactive setup; relevance: the `openclaw channels add --channel nextcloud-talk` setup path.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret expansion; relevance: `botSecret`/`botSecretFile`/env resolution.

### oc_channels_nostr (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: runs as a Nostr DM bot via a bundled plugin.
- [Encryption](../../term_dictionary/term_encryption.md) — cryptographic protection; relevance: NIP-04 encrypted DMs (NIP-44 planned) are the channel's core.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: Nostr relays are `wss://`/`ws://` WebSocket endpoints.
- [WebSocket Framing](../../term_dictionary/term_websocket_framing.md) — WS message framing; relevance: relay event delivery rides WebSocket frames.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the `nsec` private key IS the bot's cryptographic identity; inbound signatures verified before policy.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: DM policies (pairing/allowlist/open/disabled) + `allowFrom` pubkey allowlist.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — DM access policy; relevance: `dmPolicy` + npub-pubkey allowlist gate inbound DMs.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the local test relay runs as a `strfry` Docker container.

**Docs**
- [Hermes: Messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — decentralized/federated chat connector; relevance: closest parallel — a decentralized, relay/homeserver-based channel.
- [Hermes: Messaging Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — end-to-end encrypted messaging; relevance: the encrypted-DM analog of NIP-04/44.
- [Hermes: Messaging SimpleX](../hermes_agent/hermes_messaging_simplex.md) — decentralized private-messaging connector; relevance: another decentralized/private channel parallel.
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — bundled-plugin channel model; relevance: Nostr ships as an optional bundled plugin (`@openclaw/nostr`).
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/channel runtime; relevance: how a relay-connected channel is started + normalized.
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — channel concepts; relevance: situates Nostr among supported coding-agent channels.
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — channel-adapter authoring; relevance: the adapter boundary the Nostr plugin implements.
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) DM pairing; relevance: `dmPolicy: "pairing"` issues a code unknown npub senders must clear.
- [oc_channels_signal.md](oc_channels_signal.md) — (planned, this series) encrypted DM channel; relevance: sibling encrypted-DM channel with the same access-control model.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the Nostr relay adapter.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging subpackage; relevance: Nostr DM send/receive + NIP-04 decrypt path.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code; relevance: signature verification before policy + decrypt; key handling.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships the bundled `@openclaw/nostr` plugin.

**Snippets**
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — WebSocket socket-mode adapter; relevance: a sibling persistent-WebSocket inbound adapter (like the Nostr relay socket).
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — streaming event consumer; relevance: the relay event-stream consumption pattern.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — BasePlatformAdapter ABC; relevance: the adapter interface the Nostr channel implements.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound normalization; relevance: Nostr `kind:4` events normalized into the shared envelope.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — per-platform build dispatch; relevance: discovery/start of the bundled Nostr plugin.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM policy + allowlist; relevance: `dmPolicy`/`allowFrom` pubkey allowlist enforcement.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: access-control resolution for Nostr DMs.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret/key redaction; relevance: never-commit-private-key security guidance (nsec handling).
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret expansion; relevance: `${NOSTR_PRIVATE_KEY}` env/SecretRef resolution.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — target-string DSL parse; relevance: pubkey/npub DM target addressing.

### oc_channels_pairing (10t · 11s · 10d)

**Terms**
- [DM Pairing - Direct-Message Authorization Handshake](../../term_dictionary/term_dm_pairing.md) — the inbound-DM approval handshake; relevance: this note's primary subject (8-char code, 1h expiry, 3-pending cap, approve flow).
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: sender approval and node-device approval ARE access grants.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: pairing establishes who-may-DM and device-trust.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — DM access policy; relevance: `dmPolicy: "pairing"` triggers the code flow; `open` needs `allowFrom: ["*"]`.
- [Blocklist / Safelist](../../term_dictionary/term_blocklist_safelist.md) — allowlist/safelist model; relevance: approved senders land in `<channel>-allowFrom.json` (a per-channel safelist).
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: unknown senders are NOT processed until explicitly approved.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: the gateway issues pairing codes + node device-pairing requests.
- [Bonjour / mDNS Discovery](../../term_dictionary/term_bonjour_discovery.md) — local network device discovery; relevance: `.local` Bonjour hosts are accepted for plaintext `ws://` setup-code pairing.
- [VPN](../../term_dictionary/term_vpn.md) — secure network tunnel (`term_telegram` absent); relevance: Tailscale Serve/Funnel `wss://` for remote mobile node pairing; trusted-CIDR network trust.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: `wss://` required for remote pairing; plaintext `ws://` fails closed for public hosts.

**Docs**
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — approval-gated command access; relevance: the closest parallel approve/owner-bootstrap model (`commands.ownerAllowFrom`).
- [Hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway device/operator operations; relevance: node device pairing + operator scopes are gateway operations.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway device/connection model; relevance: nodes connect as `role: node` devices needing approval.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access controls; relevance: cross-tool analog of DM access-grant gating.
- [Claude Code: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — permission propagation; relevance: how an approved sender's access propagates (vs group authorization staying separate).
- [oc_channels_msteams_setup.md](oc_channels_msteams_setup.md) — (planned, this series) Teams setup; relevance: Teams `dmPolicy: "pairing"` references this flow.
- [oc_channels_signal.md](oc_channels_signal.md) — (planned, this series) Signal channel; relevance: Signal DMs default to pairing and reference this page.
- [oc_channels_nostr.md](oc_channels_nostr.md) — (planned, this series) Nostr channel; relevance: Nostr DMs default to pairing and reference this page.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/auth code; relevance: implements pairing-code issuance, allowlist stores, trusted-CIDR auto-approve.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: node device-pairing requests + operator-scope validation.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: per-channel DM pairing state + allowFrom files.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships `openclaw pairing`/`openclaw devices` CLIs.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM policy + allowlist enforcement; relevance: the exact code behind `dmPolicy`/`allowFrom` + pairing gating.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — pairing-code generation; relevance: the 8-char code, expiry, and pending-cap logic.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing lifecycle + identity; relevance: node device-pairing request/approve/reject lifecycle.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command allowlist; relevance: approved-role/scope bounding for node devices.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invocation (iOS push); relevance: iOS node pairing + device command path.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: browser/Control-UI pairing still requires manual approval (contrast with node auto-approve).
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: fail-closed behavior for unapproved/insufficient-scope pairing.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: where approved senders are read for access decisions.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash/command access policy; relevance: owner-bootstrap (`commands.ownerAllowFrom`) gating after first approval.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: operator-scope/role checks for approving devices.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: bootstrap-token + setup-code (base64 payload) handling.

### oc_channels_qa_channel (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: qa-channel is a bundled synthetic transport for OpenClaw QA.
- [QA (Quality Assurance)](../../term_dictionary/term_qa.md) — quality-assurance discipline; relevance: this channel exists for deterministic end-to-end QA automation.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered message routing; relevance: an HTTP-backed synthetic bus injects inbound messages + captures outbound transcripts.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: exercises the same bot/channel-plugin boundary real transports use.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: `allowFrom`/`groupPolicy`/`groupAllowFrom`/`requireMention` on synthetic senders.
- [Bot](../../term_dictionary/term_bot.md) — messaging identity; relevance: `botUserId`/`botDisplayName` synthetic bot identity.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: synthetic sender IDs stand in for authenticated senders in the test harness.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/channel runtime; relevance: qa-channel exercises the same channel-plugin boundary this describes.
- [Hermes: Adding a Platform Adapter (built-in)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — built-in channel adapter authoring; relevance: qa-channel is a bundled Slack-class transport adapter.
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — channel-plugin model; relevance: the synthetic transport mirrors the real channel-plugin interface.
- [Hermes: FAQ — Messaging Perf/Profiles/Workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — messaging profiles + workflows; relevance: scenario/profile/provider-mode concepts the QA suite uses.
- [Hermes: Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — Slack channel config; relevance: qa-channel uses Slack-class target grammar (`dm:`/`channel:`/`group:`/`thread:`).
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — channel-adapter authoring; relevance: the channel boundary the synthetic transport replicates for testing.
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — channel concepts; relevance: situates the synthetic transport against real channels.
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) pairing; relevance: real channels gate access via pairing — the synthetic channel allowlists synthetic senders instead.
- [oc_channels_signal.md](oc_channels_signal.md) — (planned, this series) a real channel under test; relevance: example of a production channel the QA harness validates against.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the bundled qa-channel synthetic transport.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/routing code; relevance: shared `channel:`/`group:` room-turn routing the QA suite exercises.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: the QA gateway lane the scenario suite runs against.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships `pnpm openclaw qa suite` + `qa:lab` runners.

**Snippets**
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — BasePlatformAdapter ABC; relevance: the channel-plugin boundary the synthetic transport mirrors.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound normalization; relevance: synthetic injected messages normalized like real transport payloads.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — per-platform build dispatch; relevance: how the bundled qa-channel runtime slice is booted.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type classifier; relevance: `dm`/`channel`/`group`/`thread` grammar classification.
- [snippet_hermes_agent_gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — session-key derivation; relevance: synthetic room turns get the same session keys real channels do.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — target-string DSL parse; relevance: the Slack-class `dm:`/`channel:`/`group:`/`thread:` target grammar.
- [snippet_hermes_agent_gw_mirror](../../code_snippets/snippet_hermes_agent_gw_mirror.md) — transcript/mirror capture; relevance: outbound transcript capture for QA inspection.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — streaming event consumer; relevance: the long-poll/synthetic-bus inbound consumption pattern.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: `allowFrom`/`groupAllowFrom` on synthetic senders.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash/command + per-action gating; relevance: `actions.messages`/`reactions`/`search`/`threads` per-action tool gating.

### oc_channels_qqbot (10t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: connects QQ via the official QQ Bot API (WebSocket gateway).
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: the QQ bot handling C2C/group/guild messages.
- [Bot](../../term_dictionary/term_bot.md) — messaging identity; relevance: each QQ bot has isolated OpenIDs + its own WebSocket connection.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: AppID/AppSecret (or file/SecretRef) credentials authenticate each bot.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: group-chat policy, `allowFrom`/`groupAllowFrom`, admin-command allowlists.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: each account opens its own QQ Bot API WebSocket gateway connection.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text; relevance: inbound QQ voice attachments routed to STT (`channels.qqbot.stt`).
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — text→audio; relevance: `[[audio_as_voice]]` replies synthesize TTS native QQ voice messages.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: target-format rendering for QQ message types.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — duplicate-suppression key; relevance: QQ outbound ref-index dedup prevents echo/self-reply loops.

**Docs**
- [Hermes: QQ Bot Gateway Setup](../hermes_agent/hermes_gateway_qqbot_setup.md) — sibling QQ Bot connector setup; relevance: the closest parallel connect-QQ procedure (AppID/secret, gateway).
- [Hermes: WeCom Gateway Setup](../hermes_agent/hermes_gateway_wecom_setup.md) — Tencent WeCom connector; relevance: parallel Tencent-platform bot setup (AppID/secret model).
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — installable-plugin channel model; relevance: QQ Bot is a downloadable plugin (`@openclaw/qqbot`).
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text wiring; relevance: the STT path QQ voice attachments use.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: the TTS provider/voice config for QQ native voice replies.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/attachment settings; relevance: rich media (images/voice/video/files) + chunked upload behavior.
- [Claude Code: Voice Dictation](../claude_code/cc_voice_dictation.md) — voice input handling; relevance: cross-tool voice-input analog for STT.
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) pairing; relevance: QQ is a pairing-supported channel for DM access approval.
- [oc_channels_signal.md](oc_channels_signal.md) — (planned, this series) media-capable channel; relevance: sibling channel with the same multi-account + media-handling shape.
- [oc_channels_msteams_messaging.md](oc_channels_msteams_messaging.md) — (planned, this series) messaging behavior; relevance: parallel group-chat policy + target-format + media model.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the QQ Bot engine/adapter.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging subpackage; relevance: C2C/group/guild send + chunked media upload.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone code; relevance: the STT/TTS voice path for QQ voice messages.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships the `@openclaw/qqbot` plugin + `openclaw channels add`.

**Snippets**
- [snippet_hermes_agent_gw_platform_qqbot_adapter](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_adapter.md) — QQ Bot 4-step connect; relevance: the code-side of QQ Bot setup/connect (AppID/secret, WebSocket).
- [snippet_hermes_agent_gw_platform_qqbot_keyboards](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_keyboards.md) — QQ button-data parsers; relevance: QQ interactive button/approval handling.
- [snippet_hermes_agent_gw_platform_qqbot_chunked_upload](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_chunked_upload.md) — QQ chunked media upload; relevance: large-file chunked upload for QQ rich media.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: inbound QQ voice → STT transcription.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: TTS provider/voice routing for QQ voice replies.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — streaming STT provider; relevance: an STT provider behind `channels.qqbot.stt`.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — TTS speech provider; relevance: a TTS provider behind `channels.qqbot.tts`.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash/command access policy; relevance: QQ `/bot-*` admin slash commands + non-wildcard allowlist gating.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM/group allowlist resolution; relevance: `allowFrom`/`groupAllowFrom` openid matching.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret expansion; relevance: AppSecret via plaintext/file/SecretRef/env resolution.

### oc_channels_signal (11t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: talks to `signal-cli` over HTTP (native daemon or container) to connect Signal.
- [Encryption](../../term_dictionary/term_encryption.md) — cryptographic protection; relevance: Signal is end-to-end encrypted; `signal-cli` holds the account keys locally.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: linked-device (QR) vs registered-number (SMS) account auth paths.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization gating; relevance: `dmPolicy`/`groupPolicy`/`allowFrom`/`groupAllowFrom` access model.
- [DM Policy / Allowlist](../../term_dictionary/term_dm_policy.md) — DM access policy; relevance: `dmPolicy: "pairing"` default + E.164/`uuid:` allowlists.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: container mode runs `bbernhard/signal-cli-rest-api` via docker-compose.
- [SMS](../../term_dictionary/term_sms.md) — short-message service; relevance: Setup path B registers a dedicated bot number via SMS verification.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent; relevance: the Signal bot identity bound to the bot number/device.
- [Bot](../../term_dictionary/term_bot.md) — messaging identity; relevance: the separate bot number model (avoid using a personal account — loop protection).
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling/limits; relevance: media byte caps (`mediaMaxMb`) + text chunking (`textChunkLimit`) limits.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC protocol; relevance: native mode uses `signal-cli` JSON-RPC (+ SSE); container uses `MODE=json-rpc`.

**Docs**
- [Hermes: Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — sibling Signal connector; relevance: the closest parallel connect-Signal-via-signal-cli procedure.
- [Hermes: Messaging SMS (Twilio)](../hermes_agent/hermes_messaging_sms_twilio.md) — SMS-based connector; relevance: the SMS-verification/number path parallel.
- [Hermes: Messaging Matrix E2EE](../hermes_agent/hermes_messaging_matrix_e2ee.md) — end-to-end encrypted messaging; relevance: the E2E-encrypted-channel analog.
- [Hermes: Adding a Platform Adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — external-service channel model; relevance: Signal is an external-CLI-backed channel adapter.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/attachment settings; relevance: attachments + media caps + voice-note handling.
- [Claude Code: Channels Setup](../claude_code/cc_channels_setup.md) — channel connection setup; relevance: cross-tool analog of the Signal quick-setup flow.
- [oc_channels_pairing.md](oc_channels_pairing.md) — (planned, this series) DM pairing; relevance: Signal DMs default to pairing and reference this page.
- [oc_channels_qa_channel.md](oc_channels_qa_channel.md) — (planned, this series) QA transport; relevance: Signal is one of the real channels validated by the QA harness.
- [oc_channels_nostr.md](oc_channels_nostr.md) — (planned, this series) encrypted DM channel; relevance: sibling encrypted-DM channel with the same access-control shape.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the Signal adapter (native + container modes).
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging subpackage; relevance: Signal send/receive, reactions, typing/read receipts.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code; relevance: signal-cli account-key handling + number/credential safety.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: ships `openclaw pairing`/`openclaw doctor`/`channels status` used in Signal setup.

**Snippets**
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — signal-cli init; relevance: the code-side of native daemon init / connect.
- [snippet_hermes_agent_gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal group V1/V2 + media; relevance: group handling + attachment/media path.
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — SMS platform connect; relevance: the SMS-registration/number-path analog.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — inbound normalization; relevance: Signal events normalized into the shared envelope.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — target-string DSL parse; relevance: `signal:+E164`/`uuid:`/`signal:group:` delivery targets.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM policy + allowlist; relevance: `dmPolicy`/`allowFrom` E.164/uuid enforcement.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist resolution; relevance: access-control resolution for Signal DMs/groups.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — BasePlatformAdapter ABC; relevance: the adapter interface the Signal channel implements.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — streaming event consumer; relevance: SSE (native) / WebSocket (container) receive-stream consumption.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret expansion; relevance: `httpUrl`/`account`/`cliPath` config resolution.
- [snippet_hermes_agent_gw_mirror](../../code_snippets/snippet_hermes_agent_gw_mirror.md) — transcript/mirror capture; relevance: inbound→outbound reply routing back to the same number/group.

> **Floors met for ALL 9 notes** (≥8 terms · ≥10 snippets · ≥10 docs). Notes meet/exceed: msteams_setup 10/10/10,
> msteams_federated_auth 10/10/10, msteams_messaging 10/10/10, nextcloud_talk 8/10/10, nostr 9/10/10, pairing
> (`term_session`, `term_nostr`, `term_qr_code`, `term_signal_protocol`, `term_telegram`, `term_kubernetes`,
> `term_managed_identity`, `term_microsoft_graph`, `term_self_hosted`, `term_tunnel`, `term_ngrok`, `term_tailscale`)
> are described in-note, never linked.

## Undigested Terms Plan

Per master ownership rule: OpenClaw channel vocabulary is documented IN the `oc_*` channel notes themselves (subjects of
doc pages), NOT promoted to new `term_dictionary` entries. The only `term_dictionary` interaction is **linking existing**
terms. **Expected 0 new `term_dictionary` captures.** Augment re-runs Step 2d.

| Term (appearing in source) | Disposition |
|---|---|
| Microsoft Teams / MS Teams | Documented in `oc_channels_msteams_*` (the connector docs); not a vault term. Link `term_chatbot`. |
| Entra ID / Azure AD app, client secret | Documented in note 1; link existing `term_oauth_token` + `term_authentication`. |
| Federated authentication / certificate auth / managed identity / AKS workload identity | Documented in note 2; link `term_iam` + `term_authentication` + `term_encryption`. No new term. |
| Microsoft Graph API / RSC permissions / Teams manifest | Documented in note 3 (`term_microsoft_graph` absent — describe in-note; link `term_oauth_token` for Graph app permissions). No new term. |
| Adaptive Cards / presentation cards | Documented in note 3 (rendering surface); not a reusable vault concept. No new term. |
| devtunnel / ngrok / tailscale funnel (tunneling) | Documented in note 1; link `term_tls` / `term_vpn`. `term_tunnel`/`term_ngrok` absent — describe in-note, not promoted. |
| Nextcloud Talk | Documented in `oc_channels_nextcloud_talk`; link `term_chatbot`. No new term. |
| Nostr / nsec / npub / NIP / relay | Documented in `oc_channels_nostr`; `term_nostr` absent — described in-note as the page subject; link `term_encryption` + `term_websocket`. No new term (page is its own home). |
| Pairing / sender approval / node device pairing / trusted-CIDR | Documented in `oc_channels_pairing`; link `term_access_control` + `term_authentication`. No new term. |
| QA Channel / runners / e2e automation | Documented in `oc_channels_qa_channel`; link `term_chatbot` + `term_message_queue`. No new term. |
| QQ Bot (Tencent QQ) / AppID-secret | Documented in `oc_channels_qqbot`; link `term_chatbot` + `term_authentication`. No new term. |
| Signal / signal-cli / signal-cli-rest-api / linked device | Documented in `oc_channels_signal`; `term_signal_protocol` absent — described in-note; link `term_encryption` + `term_docker` + `term_sms`. No new term. |
| STT / TTS (QQ voice) | Link existing `term_speech_to_text` + `term_text_to_speech`. No new term. |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term lacking a doc-page home appears in these
7 pages; every channel concept is the subject of its own `oc_*` note or maps to an existing term. (If augment's
re-scan surfaces one, capture via `/tessellum-capture-term-note` + add to the agentic/LLM `acronym_glossary_*.md`;
none expected.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** ch04 authors zero `term_dictionary` notes (inherited from master — OpenClaw vocab → `oc_*` doc
notes; existing terms linked, not redefined). If augment proposes a new term, the master's multi-source-research +
glossary-add requirement applies; none expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (9 notes, P2). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean: YAML field order, tags `resource/documentation/openclaw/<area>`, `## Overview` + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer, one `building_block`. |
| G2 | Grounding | Each note diffs faithfully vs `inbox/openclaw_docs/channels/<page>.md` (no invented config keys/CLI flags; config snippets verbatim). |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks per note; every assigned H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥8 relevance-selected existing `term_dictionary` links + ≥10 `code_snippets` + ≥10 docs (≥5 EXISTING) + `repo_openclaw*` + sibling `oc_*` + `entry_openclaw_docs.md`, each with a relevance statement (per locked Per-Note Related Notes Mapping). |
| G5 | Ghost-reference | No link to a non-existent note; ghost matches redirected/removed (run after reindex). |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken relative paths. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 | `note_links` query confirms in-degree ≥1 per new note (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_msteams_setup oc_channels_msteams_federated_auth oc_channels_msteams_messaging oc_channels_nextcloud_talk oc_channels_nostr oc_channels_pairing oc_channels_qa_channel oc_channels_qqbot oc_channels_signal"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # sibling-prefix cross-ref present
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO sibling $SIBLING_PREFIX ref in $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6/G8 after incremental reindex
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  indeg=$(sqlite3 "$DB" "SELECT COUNT(*) FROM note_links WHERE target_id='$did'")
  echo "$n in-degree=$indeg"; [ "${indeg:-0}" -ge 1 ] || echo "G8 FAIL (island): $n"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2,500 w / ≤6 cb / ≤400 L)? |
|---|---|---|---:|---:|---|
| 1 | oc_channels_msteams_setup | procedure | 650 | ≤6 | ✅ |
| 2 | oc_channels_msteams_federated_auth | procedure | 600 | ≤6 | ✅ |
| 3 | oc_channels_msteams_messaging | procedure | 700 | ≤6 | ✅ |
| 4 | oc_channels_nextcloud_talk | procedure | 450 | ≤6 | ✅ |
| 5 | oc_channels_nostr | procedure | 550 | ≤6 | ✅ |
| 6 | oc_channels_pairing | procedure | 600 | ≤4 | ✅ |
| 7 | oc_channels_qa_channel | procedure | 350 | ≤4 | ✅ |
| 8 | oc_channels_qqbot | procedure | 600 | ≤6 | ✅ |
| 9 | oc_channels_signal | procedure | 700 | ≤6 | ✅ |

No note approaches caps. The 5,883-word / 36-fence msteams page was split 3-way precisely so each derived note stays
≤700 w and ≤6 fences; the remaining 6 pages are each comfortably single-note.

## Entry Point Decision (inherited from master)

ch04 contributes **9 rows** to `0_entry_points/entry_openclaw_docs.md` under a "Channels" cluster (one row per note,
with the source slug + 1-line description). `entry_openclaw_docs.md` is CREATED as the master **W1 pre-step** (>30
notes corpus-wide) before the first sub-plan executes; each ch04 note gets its entry-point back-link at finalization
(this satisfies G7/G8 inbound-link requirement).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution — all sources below confirmed EXISTS):
- `entry_openclaw_docs.md` (W1 pre-step) → **all 9 notes** (primary discoverability source).
- `areas/code_repos/repo_openclaw_channels.md` → all 9 (the channels code package ↔ channel docs).
- `areas/code_repos/repo_openclaw_channels_messaging.md` → notes 1, 3, 4, 5, 8, 9 (messaging connectors).
- `areas/code_repos/repo_openclaw_channels_voice_phone.md` → note 8 (QQ voice STT/TTS).
- `areas/code_repos/repo_openclaw_security.md` → notes 2, 6, 9 (federated auth / pairing / Signal number+creds).
- `areas/code_repos/repo_openclaw_sessions.md` → notes 3, 6, 7 (routing/sessions / pairing / QA).
- `resources/term_dictionary/term_openclaw.md` → all 9 (product term → its channel docs).
- `resources/term_dictionary/term_chatbot.md` → notes 1, 3, 4, 7, 8 (bot connectors).
- `resources/term_dictionary/term_access_control.md` → notes 3, 4, 5, 6, 9 (access-control sections).
- `resources/term_dictionary/term_encryption.md` → notes 5, 9 (Nostr / Signal encryption).
- `resources/term_dictionary/term_iam.md` → note 2 (Azure managed identity / workload identity).
- `resources/term_dictionary/term_speech_to_text.md` + `term_text_to_speech.md` → note 8 (QQ voice).

`repo_openclaw_channels_messaging`, `repo_openclaw_channels_voice_phone`, `repo_openclaw_gateway`,
`term_chatbot`, `term_bot`, `term_access_control`, `term_authentication`, `term_oauth_token`, `term_oauth`,
`term_webhook`, `term_encryption`, `term_iam`, `term_docker`, `term_tls`, `term_vpn`, `term_websocket`,
`term_speech_to_text`, `term_text_to_speech`, `term_sms`, `term_markdown`, `term_message_queue`, `term_rate_limiting`,
`term_mcp`, `term_acp_agent_client_protocol`. Absent (NOT linked — described in-note instead): `term_qr_code`,
`term_signal_protocol`, `term_nostr`, `term_telegram`, `term_session`, `term_kubernetes`, `term_managed_identity`,
`term_microsoft_graph`, `term_self_hosted`, `term_tunnel`, `term_ngrok`, `term_tailscale`. `entry_openclaw_docs.md`
= master W1 pre-step (not yet in DB; created before execution).

## Pacing Rules (inherited from master)

One execution phase (9 notes). Cap dynamic-workflow fan-out ≤30 agents/run (well under). Re-read each source page at
execute; reproduce config/CLI snippets verbatim; one BB per note. `git pull --rebase --autostash` before committing;
commit + push per wave; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links +
G8 in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 checkpoints PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (status: ready) |

## Augmentation Report (2026-06-21)

**Scope.** xref-augmentation of ch04 (Channels: MS Teams ×3 / Nextcloud Talk / Nostr / Pairing / QA Channel /
QQ Bot / Signal). Re-read all 7 source pages under `inbox/openclaw_docs/channels/` (measured 12,862 words — matches
plan: msteams 5,883 · signal 2,206 · qqbot 1,498 · pairing 1,155 · nostr 896 · nextcloud-talk 715 · qa-channel 509).
No density re-split needed: the only over-cap page (msteams, 2.35× the 2,500 cap) is already split 3-way; all 9
planned notes stay ≤700 w / ≤6 cb.

**What was LOCKED.** Replaced "## Candidate Cross-References" with "## Per-Note Related Notes Mapping (LOCKED —
xref-augment 2026-06-21)" at RAISED floors (≥8 terms · ≥10 snippets · ≥10 docs per note), relevance-selected from a
**Terms / Docs / Repos / Snippets** per note with a what-it-is + per-note relevance statement on every link.

**Per-note counts (terms / snippets / docs / repos · floorsMet):**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_channels_msteams_setup | 10 | 10 | 10 (7+3) | 4 | ✅ |
| oc_channels_msteams_federated_auth | 10 | 10 | 10 (8+2) | 4 | ✅ |
| oc_channels_msteams_messaging | 10 | 10 | 10 (8+2) | 4 | ✅ |
| oc_channels_nextcloud_talk | 8 | 10 | 10 (8+2) | 4 | ✅ |
| oc_channels_nostr | 9 | 10 | 10 (8+2) | 4 | ✅ |
| oc_channels_pairing | 10 | 11 | 10 (7+3) | 4 | ✅ |
| oc_channels_qa_channel | 8 | 10 | 10 (8+2) | 4 | ✅ |
| oc_channels_qqbot | 10 | 10 | 10 (7+3) | 4 | ✅ |
| oc_channels_signal | 11 | 11 | 10 (7+3) | 4 | ✅ |

the already-known absent term slugs.

**Verification corpus richness vs original plan.** The original plan under-counted the available coding-agent corpus.
The re-search surfaced a much richer term set than the plan's `term_chatbot`/`term_oauth_token` defaults — notably
`term_dm_pairing`, `term_dm_policy`, `term_channel_kernel`, `term_messaging_gateway`, `term_socket_mode`,
`term_auth_profile`, `term_pkce`, `term_credential_pool`, `term_m365`, `term_thread_binding_policy`,
`term_websocket_framing`, `term_bonjour_discovery`, `term_deny_first`, `term_qa`, `term_json_rpc`, `term_idempotency_key`
`snippet_hermes_agent_gw_platform_*` / `snippet_openclaw_*` snippet corpus (direct teams/signal/qqbot/pairing/voice
adapters). False positives discarded on relevance (abuse/CS/ML: `term_voice_bot` [CS-AI], `term_channel_adapter`
[CS transformation layer], `term_test_plan`/`term_uat` [generic QA docs], aws_sns/sms unless on-point).

**New-term candidates.** NONE. Per master ownership rule, OpenClaw channel vocabulary (Teams, Nextcloud Talk, Nostr,
QQ Bot, Signal, pairing, qa-channel, RSC/Graph, Adaptive Cards, signal-cli, NIP-04, devtunnel) is documented IN the
`oc_*` channel notes (subjects of their own doc pages), not promoted to `term_dictionary`; existing terms are linked.
Step 2d re-scan of all 7 pages surfaced no genuinely cross-cutting, vault-reusable term lacking a doc-page home AND an
existing note. Best-fit glossary if one ever arose: the agentic/LLM `acronym_glossary_agentic_coding.md`. **Expected
0 new `term_dictionary` captures stands.**

**Issues.** None blocking. One label fix applied (`term_blocklist_safelist` link mislabeled "Access Control" →
"Blocklist / Safelist"). `term_session` / `term_nostr` / `term_qr_code` / `term_signal_protocol` / `term_telegram` /
`term_kubernetes` / `term_managed_identity` / `term_microsoft_graph` / `term_self_hosted` / `term_tunnel` /
`term_ngrok` / `term_tailscale` confirmed ABSENT and described in-note, never linked.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets, ≥10 docs) | **PASS** | Per-Note Related Notes Mapping (LOCKED) has all 9 notes at ≥8t/≥10s/≥10d, each link with a what-it-is + relevance statement; lowest term count is 8 (nextcloud_talk, qa_channel). |
| CP2 | 9-GATE present (G1-G6 + G7/G8 + G9) per phase | **PASS** | Per-Phase Validation Gate table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (raised to ≥8t/≥10s/≥10d), G5 Ghost, G6 Broken-link, G7 Discoverability, G8 in-degree ≥1 for the single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | Entry Point Decision: 9 rows to `entry_openclaw_docs.md` under a "Channels" cluster; entry point CREATED as master W1 pre-step (>30-note corpus); each note back-linked at finalization (satisfies G7/G8). |
| CP4 | Size (≤30 notes or split) | **PASS** | 9 notes — well under 30; single execution phase. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, itself derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` … `## Related Notes` … `## References` + bold footer; YAML field order; forbidden-field list). |
| CP6 | Density / borderline → split | **PASS** | Density Re-Assessment: all 9 notes ≤700 w / ≤6 cb / ≤400 L; the only over-cap page (msteams 5,883 w) already split 3-way at natural task clusters; no borderline note left unsplit. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured all 7 pages 2026-06-21 (`wc -w`): 5,883 / 715 / 896 / 1,155 / 509 / 1,498 / 2,206 = 12,862 total — exact match to plan's Source table (ratio 1.00). |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | Undigested Terms Plan present with per-term disposition (all → documented in owning `oc_*` note or link existing term); Term-Note Authoring Requirements marked N/A (0 new terms, per master ownership rule); 0 `TBD` rows. |

**RESULT: 9/9 (10/10 incl. CP8f) checkpoints PASS → READY FOR EXECUTION.**
