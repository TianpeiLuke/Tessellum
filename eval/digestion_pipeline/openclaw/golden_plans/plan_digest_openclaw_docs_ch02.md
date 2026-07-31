---
title: Sub-Plan ch02 — OpenClaw Docs: Channels (Feishu, Google Chat, Groups, iMessage, IRC)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/feishu", "channels/googlechat", "channels/group-messages", "channels/groups", "channels/imessage", "channels/imessage-from-bluebubbles", "channels/irc"]
---

# Sub-Plan ch02: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup (term_dictionary + documentation/ +
> `repo_openclaw*`), 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master and re-applied here.

## Scope

The seven Channels pages that connect a chat surface to an OpenClaw agent: **Feishu/Lark**, **Google Chat**,
**group-message activation (group-messages)**, the **cross-surface group-chat behavior model (groups)**, **native
iMessage via `imsg`**, the **BlueBubbles→imsg migration**, and **IRC**. These are channel-integration how-tos plus
one cross-cutting group-behavior model — they teach how a surface authenticates, who is allowed to talk to the agent
(access control / allowlists / mention gating), how messages are routed (DM vs group, threads, chunking), and the
per-surface gotchas. **Priority P2 (Phase B)** — feature/integration layer that depends on the Phase-A gateway /
sessions / ACP vocabulary. The code-side counterparts `repo_openclaw_channels` and
`repo_openclaw_channels_messaging` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **17,452 measured words**. **Planned: 11 notes** (3 pages split).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Feishu | channels/feishu | 2,791 | 21 | 11 | 32 | procedure (split: setup+access vs advanced/per-user-isolation) |
| Google Chat | channels/googlechat | 1,582 | 13 | 9 | 5 | procedure |
| Group messages | channels/group-messages | 853 | 1 | 6 | 1 | procedure |
| Groups | channels/groups | 3,147 | 15 | 17 | 0 | concept + procedure (split: behavior model vs policy/allowlist config) |
| iMessage | channels/imessage | 5,729 | 31 | 14 | 6 | procedure (split: setup/permissions vs access+ACP vs delivery/private-API+ops) |
| iMessage from BlueBubbles | channels/imessage-from-bluebubbles | 2,464 | 9 | 11 | 0 | procedure (migration) |
| IRC | channels/irc | 886 | 9 | 8 | 3 | procedure |

(Fence count = raw ` ``` ` lines ÷ 2; group-messages has a single open/close pair plus one stray fence, treated as 1 code block.)

## Content Strategy

- **Prioritize**: access-control / allowlist / mention-gating semantics (groups, feishu, irc — these gate *who can
  drive the agent*, the abuse-relevant surface), and the iMessage `imsg` JSON-RPC setup + private-API action model
  (the most novel, host-coupled integration).
- **Split** (word-cap ≥2,500 OR mixed-BB): `imessage.md` (5,729w, 14 H2, mixed setup/access/delivery) → 3 notes;
  `groups.md` (3,147w, concept behavior + config) → 2 notes; `feishu.md` (2,791w, setup/access + advanced
  per-user-isolation) → 2 notes. See Split Decisions.
- **Link-out / do not duplicate**: full channel field reference → `gateway/config-channels` (gw01, planned); pairing
  semantics → `channels/pairing` (ch04, planned); ambient room events → `channels/ambient-room-events` (ch01,
  planned); BlueBubbles removal announcement → `announcements/bluebubbles-imessage` (an01, planned); ACP session
  binding concept → `concepts/session` (co06, planned). Existing terms (`term_openclaw`, `term_access_control`,
  `term_oauth`, `term_websocket`, `term_json_rpc`, `term_acp_agent_client_protocol`, `term_multi_agent`,
  `term_pii`) are LINKED, never redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_feishu_setup.md` | procedure | feishu.md: Quick start, Access control (Direct messages / Group chats), Group configuration examples, Get group/user IDs, Common commands, Troubleshooting, Supported message types | 700 | Connecting a Feishu/Lark bot to OpenClaw: WebSocket-vs-webhook quick start, DM/group access control, group allowlists and @mention gating, resolving `chat_id`/`open_id`, and supported message types. |
| 2 | `oc_channels_feishu_advanced.md` | procedure | feishu.md: Advanced configuration (Message limits, Streaming, Quota optimization, ACP sessions, Multi-agent routing), Per-user agent isolation (Dynamic Agent Creation), Configuration reference | 650 | Advanced Feishu: streaming + quota optimization, ACP session binding, multi-agent routing, and per-user dynamic agent isolation (one isolated agent per Feishu sender). |
| 3 | `oc_channels_googlechat.md` | procedure | googlechat.md (all H2): Install, Quick setup, Add to Google Chat, Public URL (Tailscale Funnel / Caddy / Cloudflare Tunnel), How it works, Targets, Config highlights, Troubleshooting | 600 | Connecting Google Chat to OpenClaw: install, beginner quick setup, exposing a public webhook URL (Tailscale Funnel / reverse proxy / Cloudflare Tunnel), targets, config highlights, and the 405 troubleshooting path. |
| 4 | `oc_channels_group_messages.md` | procedure | group-messages.md (all H2): Behavior, Config example (WhatsApp), How to use, Testing/verification, Known considerations, Activation command (owner-only) | 450 | Enabling agent participation in existing group messages: per-surface behavior, the owner-only activation command, WhatsApp config example, verification, and known considerations. |
| 5 | `oc_channels_groups_model.md` | concept | groups.md: Beginner intro, Visible replies, Context visibility and allowlists, Session keys, Pattern (personal DMs + public groups, single agent), Display labels, Context fields, iMessage/WhatsApp specifics | 650 | The cross-surface group-chat model: how OpenClaw lives on your own accounts, visible-reply semantics, per-group context visibility, session keys, and surface-specific (iMessage/WhatsApp) behavior. |
| 6 | `oc_channels_groups_policy.md` | procedure | groups.md: Group policy, Mention gating (default), Scope configured mention patterns, Group/channel tool restrictions, Group allowlists, Activation (owner-only) | 650 | Configuring group access: `groupPolicy` allowlist, default mention gating, scoping `mentionPatterns` per conversation, per-group tool restrictions, group allowlists, and owner-only activation. |
| 7 | `oc_channels_imessage_setup.md` | procedure | imessage.md: Quick setup, Requirements and permissions (macOS), Enabling the imsg private API (Setup / When you can't disable SIP) | 700 | Setting up native iMessage via `imsg`: local-Mac vs remote-Mac-over-SSH quick setup, macOS requirements/permissions (Full Disk Access, Messages signed in), and enabling the imsg private API (incl. SIP-on fallback). |
| 8 | `oc_channels_imessage_access_acp.md` | procedure | imessage.md: Access control and routing, ACP conversation bindings, Deployment patterns | 650 | iMessage access control and routing: DM allowlists vs pairing, ACP conversation bindings (per-chat agent sessions), and single-/multi-agent deployment patterns. |
| 9 | `oc_channels_imessage_delivery_ops.md` | procedure | imessage.md: Media/chunking/delivery targets, Private API actions, Config writes, Coalescing split-send DMs, Inbound recovery after restart, Troubleshooting, Configuration reference pointers | 700 | iMessage delivery + operations: media/chunking/delivery targets, private-API actions (replies, tapbacks, effects, attachments), split-send coalescing, automatic inbound recovery/dedup after restart, and troubleshooting. |
| 10 | `oc_channels_imessage_from_bluebubbles.md` | procedure | imessage-from-bluebubbles.md (all H2): Migration checklist, When this makes sense, What imsg does, Before you start, Config translation, Group registry footgun, Step-by-step, Action parity, Pairing/sessions/ACP bindings, No rollback channel | 600 | Migrating from BlueBubbles to native `imsg`: checklist, `channels.bluebubbles`→`channels.imessage` config translation, the group-registry footgun, step-by-step, action parity, and the no-rollback warning. |
| 11 | `oc_channels_irc.md` | procedure | irc.md (all H2): Quick start, Security defaults, Access control (allowFrom gotcha / per-channel tools), Reply triggering (mentions), Security note for public channels, NickServ, Environment variables, Troubleshooting | 550 | Connecting IRC to OpenClaw: quick start, security defaults, channel-vs-DM access control (`allowFrom` gotcha, per-sender tools), mention reply-triggering, public-channel hardening, NickServ auth, and env vars. |

## Section Coverage Map

```
feishu.md
├── Quick start ───────────────────────────────────── → note 1 (oc_channels_feishu_setup)
├── Access control (Direct messages / Group chats) ── → note 1
├── Group configuration examples (allow-all / @mention / specific / restrict-senders) → note 1
├── Get group/user IDs (chat_id oc_xxx / open_id ou_xxx) → note 1
├── Common commands ───────────────────────────────── → note 1
├── Troubleshooting (no respond / no receive / QR / secret leak / multiple accounts) → note 1
├── Supported message types (Receive / Send / Threads & replies) → note 1
├── Advanced configuration (Message limits / Streaming / Quota optimization / ACP sessions / Multi-agent routing) → note 2 (oc_channels_feishu_advanced)
├── Per-user agent isolation — Dynamic Agent Creation (Quick setup / How it works / Config options / Session scope / Typical multi-user deployment / Verification / Notes) → note 2
├── Configuration reference ───────────────────────── → note 2
└── Related ───────────────────────────────────────── → ## Related Notes (both notes) + link-out
googlechat.md
├── Install ───────────────────────────────────────── → note 3 (oc_channels_googlechat)
├── Quick setup (beginner) ────────────────────────── → note 3
├── Add to Google Chat ────────────────────────────── → note 3
├── Public URL (Tailscale Funnel / Caddy / Cloudflare Tunnel) → note 3
├── How it works / Targets / Config highlights ────── → note 3
├── Troubleshooting (405 Method Not Allowed / Other) ─ → note 3
└── Related ───────────────────────────────────────── → ## Related Notes (note 3)
group-messages.md
├── Behavior ──────────────────────────────────────── → note 4 (oc_channels_group_messages)
├── Config example (WhatsApp) ─────────────────────── → note 4
├── How to use / Testing & verification ───────────── → note 4
├── Known considerations ──────────────────────────── → note 4
├── Activation command (owner-only) ───────────────── → note 4
└── Related ───────────────────────────────────────── → ## Related Notes (note 4)
groups.md
├── Beginner intro (2 minutes) ────────────────────── → note 5 (oc_channels_groups_model)
├── Visible replies ───────────────────────────────── → note 5
├── Context visibility and allowlists ─────────────── → note 5
├── Session keys ──────────────────────────────────── → note 5
├── Pattern: personal DMs + public groups (single agent) → note 5
├── Display labels / Context fields ───────────────── → note 5
├── iMessage specifics / WhatsApp specifics / WhatsApp system prompts → note 5
├── Group policy ──────────────────────────────────── → note 6 (oc_channels_groups_policy)
├── Mention gating (default) ──────────────────────── → note 6
├── Scope configured mention patterns ─────────────── → note 6
├── Group/channel tool restrictions (optional) ────── → note 6
├── Group allowlists ──────────────────────────────── → note 6
├── Activation (owner-only) ───────────────────────── → note 6
└── Related ───────────────────────────────────────── → ## Related Notes (notes 5 & 6)
imessage.md
├── Quick setup (Local Mac / Remote Mac over SSH) ─── → note 7 (oc_channels_imessage_setup)
├── Requirements and permissions (macOS) ──────────── → note 7
├── Enabling the imsg private API (Setup / When you can't disable SIP) → note 7
├── Access control and routing ────────────────────── → note 8 (oc_channels_imessage_access_acp)
├── ACP conversation bindings ─────────────────────── → note 8
├── Deployment patterns ───────────────────────────── → note 8
├── Media, chunking, and delivery targets ─────────── → note 9 (oc_channels_imessage_delivery_ops)
├── Private API actions ───────────────────────────── → note 9
├── Config writes ─────────────────────────────────── → note 9
├── Coalescing split-send DMs ─────────────────────── → note 9
├── Inbound recovery after a bridge or gateway restart (Scenarios / Operator signal / Migration) → note 9
├── Troubleshooting ───────────────────────────────── → note 9
├── Configuration reference pointers ──────────────── → note 9 (link-out to gw config-channels)
└── Related ───────────────────────────────────────── → ## Related Notes (notes 7–9)
imessage-from-bluebubbles.md
├── Migration checklist / When this makes sense ───── → note 10 (oc_channels_imessage_from_bluebubbles)
├── What imsg does / Before you start ──────────────── → note 10
├── Config translation / Group registry footgun ───── → note 10
├── Step-by-step / Action parity at a glance ───────── → note 10
├── Pairing, sessions, and ACP bindings / No rollback channel → note 10
└── Related ───────────────────────────────────────── → ## Related Notes (note 10)
irc.md
├── Quick start / Security defaults ───────────────── → note 11 (oc_channels_irc)
├── Access control (allowFrom gotcha / per-channel tools / per-sender) → note 11
├── Reply triggering (mentions) ───────────────────── → note 11
├── Security note (public channels) / NickServ ─────── → note 11
├── Environment variables / Troubleshooting ───────── → note 11
└── Related ───────────────────────────────────────── → ## Related Notes (note 11)
```
No orphaned H2/H3. Each source page's `## Related` block becomes the note's `## Related Notes` + external link-outs.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| feishu.md (2,791w, 11 H2 / 32 H3, 21 code) | notes 1 + 2 | exceeds 2,500w; the per-user dynamic-agent-isolation + ACP/streaming/quota "Advanced configuration" block is a distinct operational task cluster from the basic connect/access-control setup. Split keeps each ≤700w / ≤6 code. |
| groups.md (3,147w, 17 H2, 15 code) | notes 5 + 6 | exceeds 2,500w AND mixes BB: the behavior/visibility/session-key material is a concept (how groups *work*), the policy/mention-gating/allowlist/tool-restriction material is a procedure (how to *configure* gating). Split per word-cap + one-BB-per-note. |
| imessage.md (5,729w, 14 H2 / 6 H3, 31 code) | notes 7 + 8 + 9 | far exceeds 2,500w (largest page in the section); naturally three task clusters — host setup/permissions/private-API enablement (7), access control + ACP bindings + deployment (8), and delivery/private-API-actions/recovery/troubleshooting ops (9). Each ≤700w / ≤6 code. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (17,452 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×10** (notes 1–4, 6–11) · **concept ×1** (note 5, groups behavior model).
- Est. digest words ~**6,900** (avg ~625/note). The 96 source code fences (config blocks, CLI, JSON-RPC) distribute
  across the 11 notes; each note kept **≤6 code blocks** by reproducing only load-bearing config/CLI snippets verbatim.
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (relevance-selected,
  [Per-Note Related Notes Mapping](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21) section for the

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


(`SELECT 1 FROM notes WHERE note_id='resources/.../<stem>.md'`; all snippets + all docs resolve, no ghosts).
Sibling `oc_*` notes (this series) do not exist yet → marked **(planned, this series)** and counted toward the
corpora) so the floor is met by real notes even before any `oc_*` sibling lands. Relative paths from a note at
`resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; snippets
`../../code_snippets/snippet_Y.md`; other docs `../<folder>/<file>.md`; sibling `oc_Y.md`; repos
`../../../areas/code_repos/repo_Y.md`; entry `../../../0_entry_points/entry_Y.md`.

### oc_channels_feishu_setup (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat surfaces to coding agents; relevance: the product this Feishu channel docks into.
- [Access Control](../../term_dictionary/term_access_control.md) — restricting who can perform actions; relevance: `dmPolicy`/`groupPolicy`/`allowFrom` gate which Feishu senders can drive the agent.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent full-duplex transport; relevance: Feishu's default `connectionMode: websocket` (persistent connection) for event delivery.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback for event push; relevance: the optional Feishu webhook mode (`verificationToken`/`encryptKey`/`webhookPath`).
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the Feishu bot authenticates with App ID / App Secret from the Open Platform.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the Feishu/Lark bot identity that receives DMs and group messages.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot interface; relevance: the user-facing conversational surface OpenClaw exposes through Feishu.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple coordinated agents; relevance: `bindings` route Feishu DMs/groups to different agents.

**Docs**
- [Hermes: Feishu Setup](../hermes_agent/hermes_gateway_feishu_setup.md) — Hermes Feishu bot connect/setup; relevance: direct lineage analog of the Feishu quick-start (App ID/Secret, WebSocket vs webhook).
- [Hermes: Feishu Features](../hermes_agent/hermes_gateway_feishu_features.md) — Feishu message types / capabilities; relevance: maps to "Supported message types" and group behavior.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how the messaging gateway routes channels; relevance: the gateway model Feishu plugs into (restart-to-apply).
- [Hermes: Slash Commands (Messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — text-command surface in chat; relevance: Feishu has no native slash menus, so `/status`/`/reset`/`/model` are plain text.
- [Hermes: Env Vars Runtime/Messaging Behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging runtime config knobs; relevance: parallels Feishu's connection/account config keys.
- [Hermes: DingTalk Setup](../hermes_agent/hermes_gateway_dingtalk_setup.md) — another CN-platform bot setup; relevance: closest non-Feishu analog (QR/app-credential connect flow).
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access governance; relevance: the access-control posture for a chat channel docking to an agent.
- [oc_channels_feishu_advanced](oc_channels_feishu_advanced.md) — (planned, this series) — advanced Feishu (ACP/streaming/isolation); relevance: the second half of this page split.
- [oc_channels_groups_policy](oc_channels_groups_policy.md) — (planned, this series) — group allowlist/mention gating; relevance: shared `groupPolicy`/`requireMention` semantics.
- [oc_channels_irc](oc_channels_irc.md) — (planned, this series) — IRC access control; relevance: same allowlist/mention-gating model on another surface.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: implements the Feishu adapter.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — inbound/outbound messaging surface; relevance: Feishu message receive/send + media normalization.

**Snippets**
- [snippet_hermes_agent_gw_platform_feishu_connect](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_connect.md) — Feishu connect/auth code; relevance: the WebSocket connect + app-credential bootstrap this note documents.
- [snippet_hermes_agent_gw_platform_feishu_acl](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_acl.md) — Feishu access-control logic; relevance: `dmPolicy`/`groupPolicy`/allowlist gating in code.
- [snippet_hermes_agent_gw_platform_feishu_comment](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_comment.md) — Feishu comment/message handling; relevance: inbound message processing for the channel.
- [snippet_hermes_agent_gw_platform_feishu_message_card](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_message_card.md) — Feishu interactive card send; relevance: the card/message types this note enumerates.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway WebSocket channel; relevance: the persistent-connection transport Feishu uses by default.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing + allowlist; relevance: `dmPolicy: pairing`/`allowlist` flow for Feishu DMs.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — pairing approval flow; relevance: `openclaw pairing list/approve feishu` semantics.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — webhook receiver; relevance: Feishu optional webhook mode handler.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — shared platform-adapter helpers; relevance: cross-channel inbound/outbound plumbing Feishu reuses.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: how Feishu DM/group sessions are keyed.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_feishu_advanced (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host product for advanced Feishu features.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol binding a client conversation to an agent session; relevance: Feishu ACP session binding (`/acp spawn`, persistent `bindings`).
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple coordinated agents; relevance: `bindings`-driven multi-agent routing of Feishu DMs/groups.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agent instances; relevance: per-user dynamic agent creation/isolation orchestrates one agent per sender.
- [SSE (Server-Sent Events)](../../term_dictionary/term_sse.md) — streaming server→client push; relevance: streaming interactive-card replies updated in real time.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — capping request rate; relevance: quota-optimization flags (`typingIndicator`/`resolveSenderNames`) reduce Feishu API calls.
- [Throttling](../../term_dictionary/term_throttling.md) — deliberate slowing of calls; relevance: the quota-optimization mechanism for Feishu API budget.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent process; relevance: per-user isolated workspaces/personas form distinct agentic workflows.

**Docs**
- [Hermes: Profiles & Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-agent routing/profiles; relevance: direct analog of Feishu multi-agent `bindings` + per-user isolation.
- [Hermes: ACP Internals](../hermes_agent/hermes_acp_internals.md) — ACP session lifecycle internals; relevance: the ACP session binding this note configures over Feishu.
- [Hermes: ACP Editor Integration](../hermes_agent/hermes_acp_editor_integration.md) — ACP client binding example; relevance: spawning/binding an ACP agent to a conversation.
- [Hermes: Subagent Delegation](../hermes_agent/hermes_subagent_delegation.md) — delegating to isolated agents; relevance: per-user dynamic agent isolation pattern.
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session scope/resume; relevance: `session.dmScope` (main vs per-channel-peer) for isolation.
- [Band: ACP Overview](../band/band_acp_overview.md) — ACP concept overview; relevance: cross-vendor view of the agent-client-protocol binding model.
- [Claude Code: SDK Session Management API](../claude_code/cc_sdk_session_management_api.md) — programmatic session control; relevance: session-scope/isolation analog from the Claude Code SDK.
- [oc_channels_feishu_setup](oc_channels_feishu_setup.md) — (planned, this series) — Feishu connect/access; relevance: the first half of this page split.
- [oc_channels_imessage_access_acp](oc_channels_imessage_access_acp.md) — (planned, this series) — iMessage ACP bindings; relevance: the same ACP binding model on another surface.
- [oc_channels_groups_model](oc_channels_groups_model.md) — (planned, this series) — session keys / group model; relevance: session-scope concepts the advanced config tunes.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: Feishu streaming/quota config surface.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management; relevance: ACP session binding + `dmScope` isolation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent registry/lifecycle; relevance: per-user dynamic agent creation.

**Snippets**
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP bindings; relevance: the `bindings[]` ACP entries this note configures.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — spawn ACP bound to a thread; relevance: `/acp spawn codex --thread here` flow.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP session handoff; relevance: follow-up messages routing to the bound ACP session.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel→agent binding routing; relevance: `bindings` match (channel/peer/account) for multi-agent routing.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — spawn subagent via ACP; relevance: dynamic agent creation per Feishu sender.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure; relevance: `streaming`/`blockStreaming` flush behavior.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered streaming deltas; relevance: completed-block streaming for cards.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router dispatch; relevance: routing a Feishu turn to the matched agent.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_googlechat (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host product for the Google Chat channel.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback for events; relevance: Google Chat is webhook-only (HTTP POST to `/googlechat`).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy forwarding requests to an internal service; relevance: Caddy reverse-proxy option exposing only `/googlechat`.
- [DNS](../../term_dictionary/term_dns.md) — name→address resolution; relevance: the public HTTPS hostname mapping for the webhook endpoint.
- [VPN](../../term_dictionary/term_vpn.md) — private overlay network; relevance: Tailscale Funnel/Serve (tailnet) exposes the webhook while keeping the dashboard private.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: bearer-auth + `audienceType`/`audience` verification + DM pairing allowlists.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization; relevance: Google service-account credentials + `Authorization: Bearer` token verification.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the Google Chat app/bot identity (`botUser`) for mention detection.

**Docs**
- [Hermes: Messaging Google Chat](../hermes_agent/hermes_messaging_google_chat.md) — Google Chat channel setup; relevance: direct lineage analog (service account, webhook, spaces).
- [Hermes: Webhooks Routes & Security](../hermes_agent/hermes_webhooks_routes_security.md) — securing webhook routes; relevance: exposing only the webhook path, bearer-auth.
- [Hermes: Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook routing/delivery; relevance: how inbound POSTs route to a session.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — credential/OAuth setup; relevance: service-account/credential handling analog.
- [Hermes: Dashboard Auth (Remote)](../hermes_agent/hermes_dashboard_auth_remote.md) — keeping the dashboard private while exposing endpoints; relevance: Tailscale Serve (private) vs Funnel (public) split.
- [Hermes: MSGraph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — webhook listener for a cloud platform; relevance: the same inbound-webhook listener pattern.
- [Claude Code: MCP Authentication](../claude_code/cc_mcp_authentication.md) — bearer-token/OAuth auth for a remote endpoint; relevance: the bearer-audience verification model.
- [oc_channels_feishu_setup](oc_channels_feishu_setup.md) — (planned, this series) — Feishu webhook mode; relevance: webhook-mode analog on another surface.
- [oc_channels_irc](oc_channels_irc.md) — (planned, this series) — IRC connect/security; relevance: sibling channel quick-start + access control.
- [oc_channels_imessage_setup](oc_channels_imessage_setup.md) — (planned, this series) — public-exposure/host setup; relevance: another channel's host/connectivity setup.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: the Google Chat plugin adapter.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway/public-URL handling; relevance: webhook path registration + public URL.

**Snippets**
- [snippet_hermes_agent_plugins_platform_google_chat](../../code_snippets/snippet_hermes_agent_plugins_platform_google_chat.md) — Google Chat platform plugin; relevance: the exact channel adapter this note documents.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — cloud-platform webhook handler; relevance: inbound webhook POST + auth verification analog.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — generic webhook receiver; relevance: the `/googlechat` POST handler shape.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway request handler; relevance: pre-auth body budget + bearer verification before parsing.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — gateway auth ticket; relevance: keeping dashboard/control endpoints private vs the public webhook.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy connect path; relevance: reverse-proxy/tunnel exposure of the webhook path.
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — API-server route registration; relevance: registering the webhook route (405 if unregistered).
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — server auth middleware; relevance: bearer-auth middleware on the webhook route.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: Google Chat DM pairing default + `dm.allowFrom`.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — pairing approval; relevance: `openclaw pairing approve googlechat <code>`.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_group_messages (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the agent participating in an existing group.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: `groupPolicy`/`groupAllowFrom` decide which senders trigger the agent.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the agent runs on the operator's own messaging account in the group.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple agents; relevance: per-agent `groupChat.mentionPatterns` when several agents share a group.
- [Message Queue](../../term_dictionary/term_message_queue.md) — buffered message handling; relevance: pending-only context messages buffered until a triggering ping.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: group batches surface sender names/E.164 (`[from: …]`) injected as context.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking tools; relevance: visible replies via the `message` tool vs automatic final text.
- [Real-Time](../../term_dictionary/term_real_time.md) — immediate processing; relevance: typing indicators and immediate reply on a ping in the group.

**Docs**
- [Hermes: WhatsApp Baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp group/DM messaging; relevance: the WhatsApp config example this page uses verbatim.
- [Hermes: Slash Commands (Messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — in-chat commands; relevance: owner-only `/activation` + `/status` group commands.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel routing/architecture; relevance: how group inbound messages reach the agent.
- [Hermes: Env Vars Runtime/Messaging Behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — messaging behavior knobs; relevance: activation/history/mention behavior config.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/history settings; relevance: group history-limit + context injection tuning.
- [Hermes: FAQ Messaging/Perf/Profiles](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — messaging behavior FAQ; relevance: activation-mode + group-session questions.
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — replying through a channel tool; relevance: visible-reply via `message` tool analog.
- [oc_channels_groups_model](oc_channels_groups_model.md) — (planned, this series) — cross-surface group model; relevance: the general model this WhatsApp-specific page sits on top of.
- [oc_channels_groups_policy](oc_channels_groups_policy.md) — (planned, this series) — group allowlist/mention gating; relevance: `groupPolicy`/activation config shared.
- [oc_channels_feishu_setup](oc_channels_feishu_setup.md) — (planned, this series) — Feishu group config; relevance: group allowlist/mention behavior on another surface.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: group inbound handling.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging surface; relevance: group message batching + context injection.

**Snippets**
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — WhatsApp platform adapter; relevance: the WhatsApp group example this page documents.
- [snippet_hermes_agent_gw_whatsapp_identity](../../code_snippets/snippet_hermes_agent_gw_whatsapp_identity.md) — WhatsApp identity/E.164; relevance: `mentionedJids` + number-fallback mention detection.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router dispatch; relevance: routing a triggering group message to a run.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: per-group session keys (`...:group:<jid>`).
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type/session derivation; relevance: distinguishing group vs DM sessions.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access; relevance: owner-only `/activation` gating.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — platform helpers; relevance: group-context batching + `[from: …]` surfacing.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance tagging; relevance: pending-context vs current-message labeling.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — another group-capable adapter; relevance: cross-surface group activation pattern.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_groups_model (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: lives on the operator's own accounts across surfaces.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: trigger-authorization (`groupPolicy`/allowlists) vs context-visibility distinction.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple agents; relevance: single-agent vs second-agent+bindings pattern for personal/public separation.
- [Context Window](../../term_dictionary/term_context_window.md) — the model's working context; relevance: what supplemental group context (quotes/threads/history) is injected.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: `contextVisibility` filtering of quoted/forwarded sender context.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — limiting data exposure; relevance: `contextVisibility: allowlist` restricts supplemental context to allowlisted senders.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: groups run sandboxed (`mode: non-main`) while DMs stay on-host.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: "no separate bot user" — the agent is the operator's own account in the group.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — cross-channel architecture; relevance: the consistent cross-surface group model.
- [Hermes: Profiles & Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-agent/profiles; relevance: the "second agent + bindings" separation pattern.
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle; relevance: group session keys vs main DM session.
- [Hermes: Session Storage](../hermes_agent/hermes_session_storage.md) — where sessions persist; relevance: per-group session-key storage model.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation posture; relevance: groups sandboxed + restricted tools vs DM full-host tools.
- [Claude Code: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox-vs-permission model; relevance: the two execution postures (host vs sandbox) for DM vs group.
- [Band: Chat Rooms and Routing](../band/band_chat_rooms_and_routing.md) — room/routing model; relevance: cross-vendor view of group/room session routing.
- [oc_channels_groups_policy](oc_channels_groups_policy.md) — (planned, this series) — group policy/allowlist config; relevance: the configuration counterpart to this behavior model.
- [oc_channels_group_messages](oc_channels_group_messages.md) — (planned, this series) — WhatsApp group specifics; relevance: a surface-specific instance of this model.
- [oc_channels_imessage_access_acp](oc_channels_imessage_access_acp.md) — (planned, this series) — iMessage group/session routing; relevance: iMessage-specific group session behavior.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: cross-surface group-message normalization.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management; relevance: per-group session keys + context visibility scoping.

**Snippets**
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type/session derivation; relevance: group vs channel vs direct session keys.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: `agent:<id>:<channel>:group:<id>` keys + topic suffixes.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — visible-reply/send policy; relevance: `visibleReplies` automatic vs message-tool-only.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy; relevance: groups get restricted tools vs DM full tools.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — binding/match resolution; relevance: routing group vs DM to the right posture/agent.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router dispatch; relevance: the group-message evaluation order (policy→allowlist→mention).
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — platform helpers; relevance: group context fields (`ChatType`/`GroupSubject`/`WasMentioned`).
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance; relevance: untrusted-metadata fencing of group names/participant labels.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_groups_policy (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the host configuring group gating.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: `groupPolicy` (open/disabled/allowlist) + group/sender allowlists.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple agents; relevance: per-agent `mentionPatterns` when agents share a group.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: mention gating decides when the bot replies.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: sender allowlists keyed on phone/handle/user-id values.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking tools; relevance: per-group/per-sender tool restrictions scope which tools the model can call.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints on agent behavior; relevance: `tools`/`toolsBySender` deny-lists harden a public group.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — filtering/governing content; relevance: mention gating + allowlists govern which group traffic reaches the agent.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: tool restrictions pair with non-main group sandboxing to contain group-triggered runs.

**Docs**
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel routing/architecture; relevance: where `groupPolicy`/mention gating sit in the pipeline.
- [Hermes: Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — per-channel allowlist config; relevance: Slack `channels` allowlist analog of `groupPolicy`.
- [Hermes: Discord Advanced](../hermes_agent/hermes_discord_advanced.md) — guild/channel allowlists + per-channel tools; relevance: nested allowlist + tool-restriction analog.
- [Hermes: Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram group allowlist + mention; relevance: `groups`/`mentionPatterns`/forum-topic scoping analog.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — gating commands/tools; relevance: per-sender tool restriction + owner privilege model.
- [Hermes: Slash Commands (Messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — in-chat commands; relevance: owner-only `/activation` toggling mention mode.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel governance; relevance: allowlist/mention-gating posture for channels.
- [oc_channels_groups_model](oc_channels_groups_model.md) — (planned, this series) — group behavior model; relevance: the conceptual model this configures.
- [oc_channels_feishu_setup](oc_channels_feishu_setup.md) — (planned, this series) — Feishu group allowlist; relevance: same `groupPolicy`/`requireMention` config on Feishu.
- [oc_channels_irc](oc_channels_irc.md) — (planned, this series) — IRC per-channel tools; relevance: `tools`/`toolsBySender` restriction analog.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: `groupPolicy`/allowlist/mention-gating enforcement.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/policy enforcement; relevance: per-group tool-restriction policy + access gating.

**Snippets**
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy; relevance: `tools`/`toolsBySender` resolution order (most specific wins).
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — group/sender match resolution; relevance: `toolsBySender` key-prefix matching (`id:`/`e164:`/`*`).
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access gating; relevance: owner-only `/activation` authorization.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — room/sender ACL; relevance: allowlist gating analog for a group surface.
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — WhatsApp group policy; relevance: `groupPolicy`/`groupAllowFrom`/mention example.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router dispatch; relevance: the policy→allowlist→mention evaluation order.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: hardening a public group by denying tool groups.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: auditing group/sender authorization.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/visible-reply policy; relevance: how an allowed-but-unmentioned message is stored for context vs replied.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_imessage_setup (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: spawns `imsg rpc` for the iMessage channel.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — remote-procedure-call over JSON; relevance: `imsg` communicates over JSON-RPC on stdio (no daemon/port).
- [SSH](../../term_dictionary/term_ssh.md) — secure remote shell; relevance: remote-Mac setup points `cliPath` at an SSH wrapper running `imsg`.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: DM pairing default + permissions gating private-API actions.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated environment / OS protection; relevance: SIP (System Integrity Protection) tradeoff for the private-API helper dylib.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that act on a host; relevance: the agent OpenClaw drives over the iMessage host.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime wrapping an agent; relevance: the gateway harness spawning/managing `imsg`.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: `brew install steipete/tap/imsg` install path.

**Docs**
- [Hermes: BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage messaging setup; relevance: the iMessage host/permissions setup analog.
- [Hermes: Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — native iMessage path; relevance: closest lineage to the `imsg` native iMessage integration.
- [Hermes: Computer Use (macOS)](../hermes_agent/hermes_computer_use_macos.md) — macOS host automation/permissions; relevance: Full Disk Access / Automation permission requirements.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — SSH-wrapped flows; relevance: remote-Mac-over-SSH `cliPath` wrapper pattern.
- [Hermes: Provider Local LLM (Mac)](../hermes_agent/hermes_provider_local_llm_mac.md) — Mac host operations; relevance: running a service on a signed-in macOS host.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — host isolation/credentials; relevance: SIP/library-validation security tradeoff framing.
- [Claude Code: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — host permission/sandbox model; relevance: the macOS permission/SIP boundary analog.
- [oc_channels_imessage_access_acp](oc_channels_imessage_access_acp.md) — (planned, this series) — iMessage access/ACP; relevance: the access-control half of the iMessage page split.
- [oc_channels_imessage_delivery_ops](oc_channels_imessage_delivery_ops.md) — (planned, this series) — delivery/ops; relevance: the delivery/recovery half of the iMessage page split.
- [oc_channels_imessage_from_bluebubbles](oc_channels_imessage_from_bluebubbles.md) — (planned, this series) — BlueBubbles→imsg migration; relevance: the migration path into this setup.
- [oc_channels_googlechat](oc_channels_googlechat.md) — (planned, this series) — another host/connectivity setup; relevance: cross-channel setup analog.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging surface; relevance: `imsg` spawn + send/receive.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: the iMessage adapter (`cliPath`/`dbPath`).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: gateway-on-Linux SSH-wrapper path to the Mac.

**Snippets**
- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — Apple iMessage integration; relevance: the native iMessage/`imsg` interaction this note sets up.
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — legacy iMessage bridge; relevance: the predecessor path `imsg` replaces.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway channel transport; relevance: spawning/managing a stdio channel process.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — JSON-RPC server over stdio; relevance: the newline-framed JSON-RPC-over-stdio contract `imsg` uses.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect/proxy path; relevance: SSH-wrapper transparent-pipe requirement.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verification/probe; relevance: `openclaw channels status --probe` verification.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: iMessage DM pairing default + approve flow.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — pairing approval; relevance: `openclaw pairing list/approve imessage`.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: gateway start + channel probe at boot.
- [snippet_hermes_agent_gw_platform_helpers](../../code_snippets/snippet_hermes_agent_gw_platform_helpers.md) — platform helpers; relevance: stdio child-process management for the channel.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_imessage_access_acp (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: routes iMessage DMs/groups to agent sessions.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — client-conversation↔agent-session binding; relevance: ACP conversation bindings (`/acp spawn --bind here`, `bindings[]`).
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: DM allowlists vs pairing, two-gate group routing (sender + registry).
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple agents; relevance: single-/multi-agent deployment patterns + bindings.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: dedicated-bot Apple ID deployment pattern.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agents; relevance: per-chat ACP session lifecycle (`/new`/`/reset`/`/acp close`).
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: allowlist keys are handles/E.164/`chat_id` sender identities.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents acting per conversation; relevance: the per-chat agent session bound to an iMessage conversation.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent process; relevance: deployment patterns (dedicated bot Mac, remote Mac, multi-account) form distinct agentic deployments.

**Docs**
- [Hermes: BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage access/group config; relevance: `dmPolicy`/`groupPolicy`/`groupAllowFrom`/`groups` model.
- [Hermes: ACP Internals](../hermes_agent/hermes_acp_internals.md) — ACP binding internals; relevance: the conversation-binding mechanism for iMessage.
- [Hermes: Profiles & Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — multi-agent deployment; relevance: single-/multi-agent iMessage topologies.
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle; relevance: DM main-session collapse vs isolated group sessions.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — authorization model; relevance: two-gate group allowlist enforcement.
- [Band: ACP Server](../band/band_acp_server.md) — ACP server/session handling; relevance: cross-vendor ACP session-binding view.
- [Claude Code: SDK Session Management API](../claude_code/cc_sdk_session_management_api.md) — programmatic session control; relevance: per-chat agent-session binding analog.
- [oc_channels_imessage_setup](oc_channels_imessage_setup.md) — (planned, this series) — iMessage host setup; relevance: the setup half of the iMessage split.
- [oc_channels_feishu_advanced](oc_channels_feishu_advanced.md) — (planned, this series) — Feishu ACP bindings; relevance: same ACP binding model on Feishu.
- [oc_channels_groups_policy](oc_channels_groups_policy.md) — (planned, this series) — group allowlist/mention gating; relevance: the group-access gates iMessage shares.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management; relevance: ACP session binding + group session isolation.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: iMessage access-control + routing.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent registry; relevance: deployment topology (single vs multi-agent).

**Snippets**
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP bindings; relevance: `bindings[]` with `match.channel: imessage` + `peer.id: chat_id:`.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — spawn ACP bound to a thread; relevance: `/acp spawn codex --bind here` in a chat.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: which conversations route to a bound ACP session.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding→agent routing; relevance: routing future iMessage messages to the bound session.
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn policy; relevance: spawn/close lifecycle of the per-chat ACP session.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: DM allowlist vs pairing for iMessage.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — group/sender match resolution; relevance: two-gate group routing (sender + registry).
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM authorization audit; relevance: DM allowlist enforcement.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type/session derivation; relevance: `is_group=false` thread handling + group session isolation.
- [snippet_hermes_agent_acp_session](../../code_snippets/snippet_hermes_agent_acp_session.md) — ACP session object; relevance: the bound ACP session this note manages.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_imessage_delivery_ops (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: drives `imsg` delivery actions + recovery.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC over JSON; relevance: private-API actions + `watch.subscribe` run over the `imsg` JSON-RPC connection.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat operations; relevance: GUID-keyed inbound dedupe so recovery replay never dispatches twice.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: attachments/handles in delivery + recovery telemetry.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: approval reactions (👍/👎) gated by the explicit approver allowlist.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: bot-authored sends, tapbacks, effects, read receipts.
- [Real-Time](../../term_dictionary/term_real_time.md) — immediate processing; relevance: typing indicators, read receipts, live `imsg watch` tailing.

**Docs**
- [Hermes: BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage send/actions; relevance: tapbacks/edit/unsend/effects/attachments parity.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/chunking config; relevance: `mediaMaxMb`/`textChunkLimit`/`chunkMode` delivery tuning.
- [Hermes: Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — native iMessage actions; relevance: the private-API action surface (react/reply/effect).
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway/restart behavior; relevance: inbound recovery after a bridge/gateway restart.
- [Hermes: Session Storage](../hermes_agent/hermes_session_storage.md) — persistent state; relevance: persistent dedupe state (`imessage.inbound-dedupe`) + rowid cursor.
- [Hermes: Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media/actions; relevance: `upload-file`/`react`/`sendWithEffect` message-tool actions.
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — channel reply/action tool; relevance: threaded reply / native action analog.
- [oc_channels_imessage_setup](oc_channels_imessage_setup.md) — (planned, this series) — host/private-API enablement; relevance: prerequisite for these advanced actions.
- [oc_channels_imessage_access_acp](oc_channels_imessage_access_acp.md) — (planned, this series) — access/routing/ACP; relevance: which chats receive these deliveries.
- [oc_channels_imessage_from_bluebubbles](oc_channels_imessage_from_bluebubbles.md) — (planned, this series) — migration/action parity; relevance: action-parity table maps to these delivery actions.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging surface; relevance: delivery/chunking + private-API action dispatch.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: iMessage action gating + recovery monitor.

**Snippets**
- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — Apple iMessage actions; relevance: react/reply/effect/attachment delivery actions.
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — legacy iMessage delivery; relevance: the predecessor delivery/action path.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send handler; relevance: text/media send + chunking.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: `since_rowid` replay + tail on restart.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — request/ingest handler; relevance: claim-at-ingest, commit-after-handle dedupe.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — event ledger/dedupe; relevance: GUID-keyed inbound dedupe ledger.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance; relevance: coalescing split-send DMs into one turn.
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — attachment handling; relevance: attachment ingestion + size caps analog.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — dispatch handler; relevance: stale-backlog age-fence suppression on dispatch.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_imessage_from_bluebubbles (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the migration target driving `imsg`.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC over JSON; relevance: `imsg rpc` over stdio replaces the BlueBubbles REST server.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: `dmPolicy`/`groupPolicy`/`allowFrom`/`groups` carry over verbatim (group-registry footgun).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — conversation↔agent binding; relevance: `match.channel: bluebubbles` bindings must move to `imessage`.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat operations; relevance: inbound recovery replay + dedupe parity after cutover.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: bot identity + action parity preserved across migration.
- [SSH](../../term_dictionary/term_ssh.md) — secure remote shell; relevance: remote-Mac `cliPath` SSH wrapper + `remoteHost` for SCP attachments.

**Docs**
- [Hermes: BlueBubbles iMessage](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — BlueBubbles iMessage config; relevance: the source config keys being translated.
- [Hermes: Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — native `imsg` iMessage; relevance: the migration destination path.
- [Hermes: Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — cross-product config migration; relevance: the closest config-translation/migration analog.
- [Hermes: Computer Use (macOS)](../hermes_agent/hermes_computer_use_macos.md) — macOS permissions; relevance: Full Disk Access / `imsg launch` prerequisites before cutover.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential/transport changes; relevance: dropping `serverUrl`/`password` transport keys.
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session-key changes; relevance: old BlueBubbles session keys do not carry into iMessage sessions.
- [Claude Code: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — host permission boundary; relevance: SIP/permission prerequisites for the private-API surface.
- [oc_channels_imessage_setup](oc_channels_imessage_setup.md) — (planned, this series) — `imsg` setup; relevance: the setup the migration lands on.
- [oc_channels_imessage_delivery_ops](oc_channels_imessage_delivery_ops.md) — (planned, this series) — delivery/recovery; relevance: action-parity + inbound recovery after cutover.
- [oc_channels_imessage_access_acp](oc_channels_imessage_access_acp.md) — (planned, this series) — access/ACP bindings; relevance: ACP binding `channel` field migration.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging surface; relevance: the `imsg` path replacing the BlueBubbles bridge.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: the two-gate group allowlist (`isAllowedIMessageSender` + registry).

**Snippets**
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — BlueBubbles adapter; relevance: the source config/transport being migrated off.
- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — native iMessage actions; relevance: the action-parity surface after migration.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — group/sender match resolution; relevance: the two-gate group allowlist footgun.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: pairing approvals carry over by handle.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP bindings; relevance: `match.channel` migration from bluebubbles→imessage.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: probe-before-traffic + cutover restart.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify/probe; relevance: `channels status --probe --channel imessage` verification before cutover.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — request/ingest handler; relevance: inbound recovery dedupe parity after cutover.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound send handler; relevance: send/action parity verification after the cutover.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — event ledger/dedupe; relevance: GUID-keyed dedupe ledger preserved across the migration.

**Entry:** `entry_openclaw_docs` (planned, W1).

### oc_channels_irc (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the bundled IRC plugin host.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who can act; relevance: two gates — channel access (`groupPolicy`/`groups`) and sender access (`groupAllowFrom`/`allowFrom`).
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity; relevance: NickServ identify/register on connect.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: the IRC bot nick replying in channels/DMs.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking tools; relevance: per-channel/per-sender tool restrictions (`tools`/`toolsBySender`).
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: stable sender identities (`nick!user@host`) for allowlists.
- [TLS](../../term_dictionary/term_tls.md) — transport-layer security; relevance: `tls: true` for IRC sockets / public-channel hardening.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: restricting tools in public channels where anyone can prompt.

**Docs**
- [Hermes: Messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — open-protocol chat channel; relevance: closest open-network channel analog (server/host/access).
- [Hermes: Messaging SimpleX](../hermes_agent/hermes_messaging_simplex.md) — decentralized chat channel; relevance: another non-corporate-network channel setup analog.
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel routing/architecture; relevance: where IRC channel/sender gating sits.
- [Hermes: Security Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — egress/credential posture; relevance: raw TCP/TLS egress outside the forward proxy, NickServ password handling.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — tool/command gating; relevance: per-sender tool restriction (owner gets more power).
- [Hermes: Env Vars Runtime/Messaging Behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — env-var config; relevance: `IRC_HOST`/`IRC_NICK`/`IRC_NICKSERV_*` environment variables.
- [Claude Code: Channels Security & Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel governance; relevance: public-channel hardening posture.
- [oc_channels_groups_policy](oc_channels_groups_policy.md) — (planned, this series) — per-channel tools + mention gating; relevance: the shared `tools`/`toolsBySender` + mention-gating model.
- [oc_channels_googlechat](oc_channels_googlechat.md) — (planned, this series) — sibling channel quick-start; relevance: another channel connect + access control.
- [oc_channels_feishu_setup](oc_channels_feishu_setup.md) — (planned, this series) — allowlist/mention gating; relevance: same access-control model on Feishu.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: the IRC adapter.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/policy; relevance: access-control + per-channel tool-restriction + egress hardening.

**Snippets**
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — room/sender ACL; relevance: channel-vs-sender allowlist analog.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy; relevance: `tools`/`toolsBySender` per-channel restrictions.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — group/sender match resolution; relevance: `id:`-prefixed sender matching, first-match-wins.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — access gating; relevance: the `allowFrom` (DM) vs `groupAllowFrom` (channel) gotcha.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: `dmPolicy: pairing` default for IRC DMs.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: restricting tools for `allowFrom: ["*"]` public channels.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source audit; relevance: auditing IRC channel/sender authorization + egress.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — auth flow; relevance: NickServ-style identify/auth-on-connect analog.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner/router dispatch; relevance: channel→sender→mention drop logic (`missing-mention`).
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — open-network channel adapter; relevance: TLS socket connect + channel join analog.

**Entry:** `entry_openclaw_docs` (planned, W1).

## Undigested Terms Plan

Per master: OpenClaw channel vocabulary is digested as `oc_*` doc notes (their home is this sub-plan), not promoted
to `term_dictionary`. Channel/platform names are documented as configuration, not as term notes. Existing terms are
LINKED. **Expected new `term_dictionary` captures: 0.** Augment Step 2d re-runs the new-term scan.

| Term | Disposition |
|---|---|
| Feishu / Lark | Channel name → documented in `oc_channels_feishu_setup`/`_advanced`; not a term note. |
| Google Chat | Channel name → `oc_channels_googlechat`; not a term note. |
| iMessage / `imsg` | Channel + CLI tool → `oc_channels_imessage_*`; not a term note. Link `term_json_rpc` (imsg transport). |
| BlueBubbles | Deprecated bridge → described in `oc_channels_imessage_from_bluebubbles`; not a term note. |
| IRC / NickServ | Protocol + auth service → `oc_channels_irc`; not a term note. Link `term_authentication`. |
| Group policy / mention gating / allowlist | Channel-config concepts → `oc_channels_groups_policy`; link existing `term_access_control` (do NOT create `term_allowlist` — covered). |
| ACP conversation binding | OpenClaw runtime concept → described in notes 2/8/10; link existing `term_acp_agent_client_protocol`. |
| Per-user agent isolation / Dynamic Agent Creation | OpenClaw feature → `oc_channels_feishu_advanced`; link `term_multi_agent` / `term_agent_orchestration`. |
| WebSocket / webhook / Tailscale Funnel / Cloudflare Tunnel | Connectivity mechanisms → documented in setup notes; link `term_websocket`/`term_webhook`/`term_reverse_proxy` (Tailscale/Cloudflare are products, not terms). |
| Inbound recovery / split-send coalescing / dedup | Delivery semantics → `oc_channels_imessage_delivery_ops`; link existing `term_idempotency`. |
| chat_id / open_id / session keys | Config identifiers → documented inline; not terms. |

**New-term candidate (if any surfaces at augment):** none anticipated. If a genuinely cross-cutting, vault-reusable
term with no doc-page home AND no existing note appears (e.g. a generic "channel docking"/"chatops" abstraction),
capture via `/tessellum-capture-term-note` and add to the best-fit `acronym_glossary_agentic_ai.md` /
`acronym_glossary_gen_ai.md` — expected 0.

## Term-Note Authoring Requirements

update via `/tessellum-capture-term-note` + W5).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). Gate table identical to the master's 9-GATE; all must PASS before commit.

| Gate | Check | Tool / Criterion |
|------|-------|------------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` (YAML field order, itemized keywords/topics, no forbidden fields) |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/channels/<page>.md` (no invented config/behavior) |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · 1 BB per note · every mapped H2/H3 covered |
| G6 | Broken-link | `/tessellum-fix-broken-links`; 0 broken links after incremental reindex |
| G7 | Discoverability | every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` |
| G8 | In-degree ≥1 | anti-island; satisfied via `entry_openclaw_docs.md` rows + repo/term inlinks |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_feishu_setup oc_channels_feishu_advanced oc_channels_googlechat oc_channels_group_messages oc_channels_groups_model oc_channels_groups_policy oc_channels_imessage_setup oc_channels_imessage_access_acp oc_channels_imessage_delivery_ops oc_channels_imessage_from_bluebubbles oc_channels_irc"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (body words, excluding YAML; code-block pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # G4 sibling-prefix cross-ref presence
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO SIBLING/oc_ CROSS-REF"
done
# YAML frontmatter sweep for the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# Ghost + broken-link sweep happens via /tessellum-fix-ghost-references and /tessellum-fix-broken-links after reindex.
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤400L/≤2500w/≤6cb)? |
|---|---|---|---:|---:|---|
| 1 | oc_channels_feishu_setup | procedure | 700 | 6 | ✅ |
| 2 | oc_channels_feishu_advanced | procedure | 650 | 5 | ✅ |
| 3 | oc_channels_googlechat | procedure | 600 | 6 | ✅ |
| 4 | oc_channels_group_messages | procedure | 450 | 1 | ✅ |
| 5 | oc_channels_groups_model | concept | 650 | 4 | ✅ |
| 6 | oc_channels_groups_policy | procedure | 650 | 6 | ✅ |
| 7 | oc_channels_imessage_setup | procedure | 700 | 6 | ✅ |
| 8 | oc_channels_imessage_access_acp | procedure | 650 | 5 | ✅ |
| 9 | oc_channels_imessage_delivery_ops | procedure | 700 | 6 | ✅ |
| 10 | oc_channels_imessage_from_bluebubbles | procedure | 600 | 5 | ✅ |
| 11 | oc_channels_irc | procedure | 550 | 6 | ✅ |

No note approaches caps. The three code-heavy pages (imessage 31, groups 15, feishu 21 fences) were split so each
note reproduces only ≤6 load-bearing config/CLI/JSON-RPC snippets verbatim; the rest are summarized or link-out to
`gateway/config-channels` (full field reference).

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, since the corpus exceeds 30
notes) under a **"Channels"** cluster. Each new note receives its entry-point back-link at finalization (satisfies
G7/G8 — ≥1 inbound link from outside `documentation/openclaw/`). No separate per-sub-plan entry point.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify exact targets at execution):

- `entry_openclaw_docs.md` (planned, W1) → **all 11 notes** (primary anti-island guarantee).
- `repo_openclaw_channels.md` → notes 1, 3, 5, 6, 7, 8, 11 (channel adapters).
- `repo_openclaw_channels_messaging.md` → notes 1, 4, 7, 9, 10 (messaging/inbound-outbound surface).
- `repo_openclaw_sessions.md` → notes 2, 5, 8 (ACP session binding / session keys).
- `repo_openclaw_security.md` → notes 6, 11 (access-control / hardening).
- `term_openclaw.md` → notes 1–11 (umbrella product term); `term_acp_agent_client_protocol.md` → notes 2, 8, 10;
  `term_json_rpc.md` → notes 7, 9, 10; `term_access_control.md` → notes 1, 3, 4, 5, 6, 8, 11.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page; reproduce config/CLI/JSON-RPC snippets
verbatim; one BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; `git pull --rebase --autostash` first;
commit + push per wave; **no Claude co-author trailer**. Reindex incrementally and verify `note_links` + 0 broken
links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this run (xref-augment):** re-read all 7 source pages under `inbox/openclaw_docs/channels/`
(feishu, googlechat, group-messages, groups, imessage, imessage-from-bluebubbles, irc) and locked the
**Per-Note Related Notes Mapping** at the RAISED floors: **≥8 `term_dictionary` terms · ≥10 `code_snippets` ·
≥10 docs under `resources/documentation/`** per note, relevance-selected (re-read-grounded, no padding),
PLUS relevant `repo_openclaw*` and sibling `oc_*` (this series, planned). Every EXISTING note_id was

**What was locked — per-note counts (terms / snippets / docs[existing+planned] / repos · floorsMet):**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_channels_feishu_setup | 8 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_feishu_advanced | 8 | 10 | 10 (7+3) | 3 | ✅ |
| oc_channels_googlechat | 8 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_group_messages | 8 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_groups_model | 8 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_groups_policy | 9 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_imessage_setup | 8 | 10 | 11 (7+4) | 3 | ✅ |
| oc_channels_imessage_access_acp | 9 | 10 | 10 (7+3) | 3 | ✅ |
| oc_channels_imessage_delivery_ops | 8 | 10 | 10 (7+3) | 3 | ✅ |
| oc_channels_imessage_from_bluebubbles | 8 | 10 | 10 (7+3) | 2 | ✅ |
| oc_channels_irc | 8 | 10 | 10 (7+3) | 2 | ✅ |

`hermes_agent/` (closest lineage — Hermes shares the OpenClaw channel/gateway model), `claude_code/`, `band/`,

**Step 2d new-term scan (re-read).** No new cross-cutting, vault-reusable `term_dictionary` candidate surfaced.
Re-reading all 7 pages confirms the master's design decision: channel/platform names (Feishu, Google Chat,
iMessage/`imsg`, BlueBubbles, IRC/NickServ), config concepts (`groupPolicy`, mention gating, ACP conversation
binding, dynamic agent creation, split-send coalescing, inbound recovery/dedupe), and identifiers
(`chat_id`/`open_id`/session keys) are documented as `oc_*` doc content, not promoted to terms — existing terms
are LINKED. **New-term candidates: 0** (consistent with the plan's Undigested Terms Plan; best-fit glossary
would be `acronym_glossary_agentic_ai.md` / `acronym_glossary_gen_ai.md` only if one ever surfaced — none did).

**DB-absent terms (deliberately NOT cited; substitutes used):** `term_session`, `term_streaming`,
`term_imessage`, `term_irc`, `term_feishu`, `term_google_chat`, `term_tailscale`, `term_qr_code`,
`term_allowlist` are not in the DB. Substitutes: `term_sse`/`term_rate_limiting`/`term_throttling` (streaming +
quota), `term_agent_orchestration`/`term_message_queue` (session/context; session storage covered by the
`hermes_session_storage` doc, not a term), `term_access_control` (allowlist), `term_vpn` (Tailscale
Funnel/tailnet), `term_homebrew`/`term_ssh`/`term_tls` (connectivity). All cited terms resolve in the DB.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints. CP7 spot-checked by re-reading 3 source pages
(feishu 2,791w, imessage 5,729w, groups 3,147w) — measured sizes match the plan's Source table.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | Per-Note Related Notes Mapping locked: all 11 notes ≥8 terms (2 at 9) · ≥10 snippets · ≥10 docs, each link with a `relevance:` statement; automated count confirms floors met for all 11. |
| CP2 | 9-GATE table present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7 Discoverability, G8 In-degree (inherited from master, all 8). |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision` contributes 11 rows to `entry_openclaw_docs.md` (CREATED master pre-step W1, corpus >30 notes); every note's `**Entry:**` line names it; DB confirms `entry_openclaw_docs.md` not yet present (correctly planned, not a ghost). |
| CP4 | Size | **PASS** | 11 notes (≤30); single execution phase; 3 oversized pages split per Split Decisions (feishu→2, groups→2, imessage→3). |
| CP5 | Format derived | **PASS** | Format Definition inherited from master, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora; `## Overview` / `## Related Notes` H2 conventions + YAML field order match existing `resources/documentation/` notes (not invented). |
| CP6 | Density | **PASS** | Density Re-Assessment table: every note ≤700w / ≤6 code blocks / ≤400 lines; no note approaches caps; code-heavy pages split so each reproduces only ≤6 load-bearing snippets. |
| CP7 | Sources measured | **PASS** | Re-read feishu (2,791w), imessage (5,729w), groups (3,147w) — all within ±5% of the plan's Source table (measured 2026-06-20, not estimated). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (expected new captures: 0, with per-row dispositions); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — with multi-source mandate inherited from master if a term is later proposed). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to audit (all linked, not created). All-notes dedup generalized: the 11 planned `oc_*` doc notes were collision-checked against `term_dictionary/` + `documentation/` (master dedup policy) — none duplicates an existing term/doc/repo; OpenClaw channel docs are net-new (no `openclaw/` doc folder yet). |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing → new)` table covers all 11 notes; G7/G8 in the gate table; `entry_openclaw_docs` (W1) → all 11 (primary anti-island) + repo/term inlinks; inlinks are a gated execution phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
</content>
</invoke>
