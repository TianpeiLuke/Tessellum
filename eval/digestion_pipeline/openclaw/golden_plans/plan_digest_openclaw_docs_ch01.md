---
title: Sub-Plan ch01 — OpenClaw Docs: Channels (Access Groups, Routing, Discord, ClickClack)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["channels/access-groups", "channels/ambient-room-events", "channels/bot-loop-protection", "channels/broadcast-groups", "channels/channel-routing", "channels/clickclack", "channels/discord"]
---

# Sub-Plan ch01: Channels

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`) / format / dedup / 9-GATE / cross-references / entry-point
> (`entry_openclaw_docs.md`) / undigested-terms decisions are ALL inherited from the master; this file holds only the
> measured per-page plan, planned-notes table, coverage map, split decisions, candidate cross-refs, and gate table.

## Scope

The first seven Channels pages — the channel-access / routing / loop-safety / fan-out primitives plus two concrete
channel integrations (ClickClack, Discord). Covers: **access-groups** (reusable sender allowlists shared across
channels), **ambient-room-events** (non-mention room-context delivery + reply modes), **bot-loop-protection**
(self/bot-echo guards), **broadcast-groups** (fan one inbound message to multiple agents), **channel-routing** (the
target-prefix / session-key / routing-rule model that every channel uses), **clickclack** (the ClickClack chat
channel setup), and **discord** (the large, full-feature Discord channel integration). Priority **P2** (Phase B,
features/integration), but `channel-routing` is the conceptual backbone the other Channels sub-plans (ch02–ch06)
reference. The code-side counterparts `repo_openclaw_channels` / `_channels_messaging` / `_channels_voice_phone`
are LINKED, not recreated (dedup policy, master).

**Source**: OpenClaw docs, 7 pages, **14,758 measured words** (discord alone = 9,637w). **Planned: 12 notes** (discord
splits into 6; all six others = 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Access groups | channels/access-groups | 853 | 6 | 7 | 0 | procedure |
| Ambient room events | channels/ambient-room-events | 915 | 6 | 10 | 0 | procedure |
| Bot loop protection | channels/bot-loop-protection | 485 | 2 | 4 | 0 | procedure |
| Broadcast groups | channels/broadcast-groups | 1,475 | 4 | 12 | 13 | procedure (fan-out) + model (config schema) |
| Channels & routing | channels/channel-routing | 868 | 2 | 12 | 0 | concept (routing model) |
| ClickClack | channels/clickclack | 525 | 5 | 5 | 0 | procedure |
| Discord | channels/discord | 9,637 | 42 | 15 | 5 | procedure + concept + model (SPLIT ×6) |

Counts measured via `wc -w` and `grep -c '^\`\`\`'` (÷2 for fences) on the mirror; H2/H3 via `grep -nE '^#{2,3} '`.
Discord H3 count (5) is across its Role-based routing / Voice (channels, follow-users, messages) subsections.

## Content Strategy

- **Prioritize**: `channel-routing` (the target-prefix + session-key + routing-rule model that ch02–ch06 all build on)
  and `broadcast-groups` (the fan-out + session-isolation contract) — these are the cross-cutting Channels concepts.
  Within Discord, prioritize Access control & routing (audiences, role-based routing) and Voice (the richest, most
  novel capability set) as their own notes.
- **Split**: only `discord.md` (9,637w / 42 code blocks / 15 H2 — far over the 2,500w + 6-code caps and spans
  procedure + concept + model BBs) → **6 BB-atomic notes** (setup, runtime+routing+access, feature details/reference,
  voice, troubleshooting+config+safety, interactive-components/commands). See Split Decisions. `broadcast-groups`
  (1,475w) stays ONE note — under caps, single coherent procedure with an embedded config-schema sub-section.
- **Link-out (do NOT redefine here)**: per-platform channel pages (Slack/Telegram/Matrix/etc.) are ch02–ch06; voice
  *transport*/*provider* internals are nodes (nd01–02) + providers (pr*) + tools (`tools/voice*`); OAuth/secrets
  internals are gw* (gateway). Existing terms (`term_access_control`, `term_rate_limiting`, `term_voice_call`,
  `term_oauth`, `term_multi_agent`, `term_fan_out`, …) are LINKED, never inlined. Discord-specific raw config
  reproduced selectively (each note ≤6 code blocks), not the full 42 fences.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_channels_access_groups.md` | procedure | access-groups.md (all 7 H2: Static sender groups, Reference from allowlists, Supported channel paths, Plugin diagnostics, Discord audiences, Security notes, Troubleshooting) | 650 | Reusable sender allowlists ("access groups") shared across message channels: defining static sender groups, referencing them from per-channel allowlists, supported channel paths, Discord audiences, and the rule that a group grants nothing until an allowlist references it. |
| 2 | `oc_channels_ambient_room_events.md` | procedure | ambient-room-events.md (Recommended setup, What changes, Discord/Slack/Telegram examples, Agent-specific policy, Visible reply modes, History, Troubleshooting) | 650 | Delivering non-mention room context ("ambient" events) to an agent: enabling ambient mode per channel, what changes in message flow, per-platform examples (Discord/Slack/Telegram), agent-specific policy, and the visible reply modes. |
| 3 | `oc_channels_bot_loop_protection.md` | procedure | bot-loop-protection.md (Defaults, Configure shared defaults, Override per channel or account, Channel support) | 450 | Preventing bot-to-bot / self-echo message loops: default ignore-self and bot-reply guards, configuring shared defaults, per-channel / per-account overrides, and which channels support the protection. |
| 4 | `oc_channels_broadcast_groups.md` | procedure | broadcast-groups.md (Overview, Use cases, Configuration incl. Basic setup / Processing strategy / Complete example, How it works incl. Message flow / Session isolation / Example, Best practices, Compatibility, Troubleshooting, Examples, API reference incl. Config schema / Fields, Limitations, Future enhancements) | 750 | Fanning one inbound message to multiple agents via broadcast groups: use cases, configuration (processing strategy, complete example), message-flow + per-agent session isolation, compatibility (providers / routing), the config-schema reference (fields), and limitations. |
| 5 | `oc_channels_channel_routing.md` | concept | channel-routing.md (Key terms, Outbound target prefixes, Session key shapes, Main DM route pinning, Guarded inbound recording, Routing rules, Broadcast groups pointer, Config overview, Session storage, WebChat behavior, Reply context) | 700 | The OpenClaw channel-routing model that every channel reuses: outbound target prefixes, session-key shapes, main-DM route pinning, the routing rules that pick an agent, guarded inbound recording, session storage, and reply context. |
| 6 | `oc_channels_clickclack.md` | procedure | clickclack.md (Quick setup, Multiple bots, Targets, Permissions, Troubleshooting) | 450 | Setting up the ClickClack chat channel: quick setup, running multiple bots, outbound targets, permissions, and troubleshooting. |
| 7 | `oc_channels_discord_setup.md` | procedure | discord.md: Quick setup, Recommended: Set up a guild workspace | 700 | Connecting OpenClaw to Discord: creating/registering the bot application, token + intents, the quick-setup flow, and the recommended guild-workspace layout. |
| 8 | `oc_channels_discord_routing_access.md` | procedure | discord.md: Runtime model, Forum channels, Access control and routing (incl. Role-based agent routing), Native commands and command auth | 700 | Discord runtime model + access control: how messages map to sessions, forum-channel handling, audience/allowlist access control, role-based agent routing, and native (slash) commands with command auth. |
| 9 | `oc_channels_discord_features.md` | model | discord.md: Feature details, Interactive components, Components v2 UI, Tools and action gates | 700 | Reference of Discord-specific features and message capabilities: interactive components, the Components v2 UI, per-feature behavior details, and the tools / action-gate surface exposed on Discord. |
| 10 | `oc_channels_discord_voice.md` | procedure | discord.md: Voice (Voice channels, Follow users in voice, Voice messages) | 700 | Discord voice support: joining/managing voice channels, follow-users-in-voice behavior, and voice (audio) messages — setup and operational behavior. |
| 11 | `oc_channels_discord_operations.md` | procedure | discord.md: Troubleshooting, Configuration reference, Safety and operations | 600 | Operating a Discord channel: the configuration reference, troubleshooting common failures, and safety / operations guidance. |

> Note count = **11 notes** (6 single-page + 5 from the discord split). The master's est. "11" for ch01 matches;
> discord's 6th candidate aspect (interactive components) is merged into note 9 (Features) to keep each note ≥450w and
> avoid a thin orphan — see Split Decisions. Final lock during augment.

## Section Coverage Map

```
access-groups.md
├── Static message sender groups ──────────── → note 1 (oc_channels_access_groups)
├── Reference groups from allowlists ───────── → note 1
├── Supported message-channel paths ────────── → note 1
├── Plugin diagnostics ─────────────────────── → note 1
├── Discord channel audiences ──────────────── → note 1 (cross-link note 8)
├── Security notes ─────────────────────────── → note 1
└── Troubleshooting ────────────────────────── → note 1
ambient-room-events.md
├── Recommended setup ──────────────────────── → note 2 (oc_channels_ambient_room_events)
├── What changes ───────────────────────────── → note 2
├── Discord / Slack / Telegram example ─────── → note 2
├── Agent specific policy ──────────────────── → note 2
├── Visible reply modes ────────────────────── → note 2
├── History ────────────────────────────────── → note 2
├── Troubleshooting ────────────────────────── → note 2
└── Related ────────────────────────────────── → note 2 (Related Notes section)
bot-loop-protection.md
├── Defaults ───────────────────────────────── → note 3 (oc_channels_bot_loop_protection)
├── Configure shared defaults ──────────────── → note 3
├── Override per channel or account ────────── → note 3
└── Channel support ────────────────────────── → note 3
broadcast-groups.md
├── Overview / Use cases ───────────────────── → note 4 (oc_channels_broadcast_groups)
├── Configuration (Basic / Processing / Complete) → note 4
├── How it works (Message flow / Session isolation / Example) → note 4
├── Best practices / Compatibility (Providers / Routing) → note 4
├── Troubleshooting / Examples ─────────────── → note 4
├── API reference (Config schema / Fields) ─── → note 4
├── Limitations / Future enhancements ──────── → note 4
└── Related ────────────────────────────────── → note 4 (Related Notes section)
channel-routing.md
├── Key terms ──────────────────────────────── → note 5 (oc_channels_channel_routing)
├── Outbound target prefixes ───────────────── → note 5
├── Session key shapes (examples) ──────────── → note 5
├── Main DM route pinning ──────────────────── → note 5
├── Guarded inbound recording ──────────────── → note 5
├── Routing rules (how an agent is chosen) ─── → note 5
├── Broadcast groups (pointer) ─────────────── → note 5 (→ note 4)
├── Config overview / Session storage ──────── → note 5
├── WebChat behavior / Reply context ───────── → note 5
└── Related ────────────────────────────────── → note 5 (Related Notes section)
clickclack.md
├── Quick setup ────────────────────────────── → note 6 (oc_channels_clickclack)
├── Multiple bots ──────────────────────────── → note 6
├── Targets / Permissions ──────────────────── → note 6
└── Troubleshooting ────────────────────────── → note 6
discord.md
├── Quick setup ────────────────────────────── → note 7 (oc_channels_discord_setup)
├── Recommended: Set up a guild workspace ──── → note 7
├── Runtime model ──────────────────────────── → note 8 (oc_channels_discord_routing_access)
├── Forum channels ─────────────────────────── → note 8
├── Access control and routing (+ Role-based agent routing) → note 8
├── Native commands and command auth ───────── → note 8
├── Feature details ────────────────────────── → note 9 (oc_channels_discord_features)
├── Interactive components ─────────────────── → note 9
├── Components v2 UI ───────────────────────── → note 9
├── Tools and action gates ─────────────────── → note 9
├── Voice (Voice channels / Follow users / Voice messages) → note 10 (oc_channels_discord_voice)
├── Troubleshooting ────────────────────────── → note 11 (oc_channels_discord_operations)
├── Configuration reference ────────────────── → note 11
├── Safety and operations ──────────────────── → note 11
└── Related ────────────────────────────────── → distributed (notes 7–11 Related Notes)
```
No orphaned sections. Per-platform channel pages (Slack/Telegram/Matrix), voice transport/providers, OAuth/secrets
internals are linked out (ch02–ch06 / nd01–02 / pr* / gw*), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| discord.md (9,637w · 42 code · 15 H2 / 5 H3 · procedure+concept+model) | notes 7 + 8 + 9 + 10 + 11 (5 notes) | ~4× the 2,500w cap and 7× the 6-code cap, and spans three BBs (setup/voice/ops = procedure; runtime/routing = concept-leaning procedure; feature-details/components = model/reference). Split along natural task/BB clusters: setup (1,485w) → 7; runtime+routing+access+commands (1,862w) → 8; feature-details+interactive+components+gates (2,570w) → 9 (model/reference, selectively reproduced); voice (3,318w) → 10; troubleshooting+config+safety (925w) → 11. Each output note targets ≤700w, ≤6 code — far under caps despite large source clusters. |
| broadcast-groups.md (1,475w · 4 code · 12 H2 / 13 H3) | note 4 (1 note) | Under the 2,500w cap; single coherent fan-out procedure. The API-reference / config-schema H3s are a sub-section of the same procedure (kept inline as a small schema block), not a separate model note — does not meet the split threshold. |

All six non-discord pages = 1 note each (each ≤1,475w, ≤6 code, single dominant BB).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (14,758 words; discord = 9,637w / 65% of section). New `oc_*` notes: **11**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×8** (notes 1,2,3,4,6,7,8,10,11 — config/setup/ops how-tos; note 4 fan-out procedure), **concept ×1** (note 5 routing model), **model ×1** (note 9 Discord feature/components reference). (procedure 9 / concept 1 / model 1 across the 11 notes.)
- Est. digest words ~7,100 (avg ~645/note); all ≤700w, ≤6 code blocks. The 42 discord fences distribute across notes 7–11 with selective verbatim reproduction (≤6 each).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> snippets 80/80, docs 51/51, repos 11/11, entries 5/5 OK; `entry_openclaw_docs` is the only deliberate non-existing
> ref, planned at master W1). Selection is RELEVANCE-driven from a fresh re-read of each `inbox/openclaw_docs/channels/`
> docs toward the floor are sibling `oc_*` "(planned, this series)" + `entry_openclaw_docs` "(planned, W1)". All cited
> term `../../term_dictionary/…`, snippet `../../code_snippets/…`, other doc `../<folder>/…`, sibling `oc_…`,
> repo `../../../areas/code_repos/…`, entry `../../../0_entry_points/…`.
>
> Render in each note's `## Related Notes` as: `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_channels_access_groups (8t · 10s · 11d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — authorization model deciding which principals may act; relevance: access groups ARE shared sender-allowlist access control referenced by `accessGroup:<name>`.
- [Blocklist / Safelist](../../term_dictionary/term_blocklist_safelist.md) — allow/deny list authorization primitive; relevance: access groups are reusable allowlist aliases (`allowFrom`/`groupAllowFrom`), the page's core mechanism.
- [Deny-First](../../term_dictionary/term_deny_first.md) — secure-default-deny posture; relevance: missing group names and `dmPolicy:"open"` without `"*"` fail closed — the page's security-notes rule.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — per-channel direct-message access policy; relevance: groups are referenced from `channels.<ch>.allowFrom` under each channel's `dmPolicy`.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway fronting all chat channels; relevance: access groups live in shared gateway sender-authorization helpers/plugin SDK.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel inbound/outbound adapter; relevance: support depends on whether a channel is wired through the shared adapter sender-auth helpers.
- [Slack](../../term_dictionary/term_slack.md) — Slack chat channel; relevance: example sender groups span Slack/Discord/Telegram/WhatsApp channel-keyed member lists.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted multi-channel agent gateway; relevance: this is OpenClaw access-control config and `openclaw doctor` validation.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — the shared routing model; relevance: allowlists/access groups gate the inbound recording that routing then dispatches.
- [Discord routing & access (planned, this series)](oc_channels_discord_routing_access.md) — Discord audiences + allowlists; relevance: the `discord.channelAudience` dynamic access-group type is detailed there.
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — sibling gateway's channel-auth architecture; relevance: closest existing analog of the shared sender-authorization helper layer.
- [hermes: security command approval](../hermes_agent/hermes_security_command_approval.md) — command-auth allowlist enforcement; relevance: command authorization paths reuse the same message-channel sender allowlists.
- [hermes: messaging Slack config](../hermes_agent/hermes_messaging_slack_config.md) — Slack allowlist/config; relevance: per-channel allowlist keying mirrors the access-group channel-key model.
- [hermes: messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix room/sender access; relevance: shows per-room sender allowlist patterns access groups feed into.
- [cc: channels security & enterprise controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access governance; relevance: cross-tool view of allowlist/audience access control for coding-agent channels.
- [cc: channel permission relay](../claude_code/cc_channel_permission_relay.md) — channel-side permission relay; relevance: parallels access-group "grants nothing until referenced" gating semantics.
- [band: chat rooms and routing](../band/band_chat_rooms_and_routing.md) — chat room membership/routing; relevance: channel-audience membership resolution is the band-room analog.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements `accessGroup` resolution + allowlist matching.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: per-channel `allowFrom`/`groupAllowFrom` wiring.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/plugin-SDK; relevance: `resolveAccessGroupAllowFromState` lives in `plugin-sdk/security-runtime`.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist/pairing resolution; relevance: the exact `allowFrom`/`accessGroup` matching path.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM access audit; relevance: audits the dmPolicy/allowlist combos `openclaw doctor` catches.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source-trust audit; relevance: sender-id trust check behind access-group matching.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match/allowlist resolver; relevance: resolves `accessGroup:<name>` references to concrete senders.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the shared SDK helper surface new channels implement for groups.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-by-default policy; relevance: fail-closed semantics for missing/unsupported groups.
- [snippet_hermes_agent_gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — ACL evaluation in the runner; relevance: sibling-impl of channel sender ACL access groups feed.
- [snippet_hermes_agent_gw_platform_feishu_acl](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_acl.md) — per-channel sender ACL; relevance: shared per-channel allowlist auth helper analog (Feishu is in the access-group bundled-support list).
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command auth; relevance: command-auth paths reuse the message-channel sender allowlists.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize-before-dispatch; relevance: where allowlist/access-group authorization gates inbound dispatch.

### oc_channels_ambient_room_events (8t · 10s · 11d)

**Terms**
- [Silence Token](../../term_dictionary/term_silence_token.md) — quiet/no-visible-reply control token; relevance: ambient room events stay silent until `message(action=send)` — the page's central behavior.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct vs room message policy; relevance: DMs stay user requests while unmentioned room chatter becomes quiet context.
- [Access Control](../../term_dictionary/term_access_control.md) — allowlist gating; relevance: the room must still pass `groupPolicy`/room allowlist/sender allowlist.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway hot-reloading `messages` settings; relevance: ambient config is a gateway `messages.groupChat` setting.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel inbound mapping; relevance: Discord/Slack/Telegram each map unmentioned inbound to room events.
- [Chatbot](../../term_dictionary/term_chatbot.md) — bot-in-room behavior; relevance: lurk-mode "listen, decide, reply" is the ambient chatbot pattern replacing `NO_REPLY`.
- [Slack](../../term_dictionary/term_slack.md) — Slack channel; relevance: Slack channel/private-channel/MPDM ambient support + `channels:history` scope requirement.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this is OpenClaw `messages.groupChat` ambient config.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — routing/session model; relevance: room events feed the session as quiet context per channel session key.
- [Discord features (planned, this series)](oc_channels_discord_features.md) — Discord visible-reply behavior; relevance: Discord keeps room-event history until a visible send succeeds.
- [hermes: env vars & runtime messaging behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — runtime message-flow knobs; relevance: closest analog of `unmentionedInbound`/`visibleReplies` behavior switches.
- [hermes: messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — message delivery/visibility settings; relevance: visible vs suppressed delivery metadata mirrors ambient suppressed-delivery logging.
- [hermes: messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Slack group/channel behavior; relevance: Slack channel-ID-first allowlists + history scopes for ambient rooms.
- [hermes: Telegram advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram group config; relevance: BotFather privacy mode / full group traffic requirement for ambient Telegram.
- [hermes: FAQ messaging perf/profiles/workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — group-chat workflow profiles; relevance: always-on room workflow tradeoffs (typing/token use without visible message).
- [cc: channels overview](../claude_code/cc_channels_overview.md) — channel reply/visibility model; relevance: cross-tool view of when an agent posts vs stays quiet in a room.
- [band: agent API context & activity](../band/band_agent_api_context_activity.md) — room context/activity feed; relevance: "watch room chatter as quiet context" is the band context-activity analog.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements room-event inbound classification.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Discord/Slack/Telegram ambient room-event support.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: room events update session state + history buffer.

**Snippets**
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — classifies chat type (DM/group/room); relevance: room-event vs user-request classification.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input source provenance; relevance: distinguishes mentioned/unmentioned/command inbound provenance.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — visible-send policy; relevance: `visibleReplies: message_tool` vs automatic delivery gate.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: routes ambient room events vs user requests through dispatch.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/room resolution; relevance: resolves the room a quiet event belongs to.
- [snippet_openclaw_gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — history injection; relevance: `historyLimit` ambient context buffer injection.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack inbound platform; relevance: Slack channel-history scopes for ambient rooms.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect/inbound; relevance: full-group-traffic privacy-mode handling for ambient Telegram.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord inbound normalize; relevance: maps unmentioned guild messages to room events.

### oc_channels_bot_loop_protection (8t · 10s · 11d)

**Terms**
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — sliding-window budget + cooldown throttle; relevance: the guard is a per-pair `maxEventsPerWindow`/`windowSeconds`/`cooldownSeconds` budget.
- [Chatbot](../../term_dictionary/term_chatbot.md) — bot identity in a channel; relevance: pair loop protection guards two bot identities replying to each other.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — inbound reply-runner events; relevance: the core inbound reply runner maps each channel's inbound event into generic pair facts.
- [Deny-First](../../term_dictionary/term_deny_first.md) — secure default; relevance: bots are ignored by default; `allowBots` must be explicitly enabled.
- [Access Control](../../term_dictionary/term_access_control.md) — `allowBots`/allowlist gating; relevance: protection activates only when `allowBots` lets bot messages reach dispatch.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway runner; relevance: enforced centrally in the gateway core inbound reply runner across channels.
- [Slack](../../term_dictionary/term_slack.md) — Slack channel; relevance: Slack uses native `bot_id` facts keyed by account/channel/bot-pair.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `channels.defaults.botLoopProtection` config + precedence chain.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — routing/session model; relevance: loop protection sits in the inbound dispatch path that routing controls.
- [Broadcast groups (planned, this series)](oc_channels_broadcast_groups.md) — fan-out; relevance: multi-agent fan-out raises bot-to-bot interaction surface the guard protects.
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — inbound runner architecture; relevance: closest analog of the core inbound reply-runner enforcing the pair guard.
- [hermes: gateway internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: where per-channel inbound facts are normalized for cross-cutting guards.
- [hermes: env vars & runtime messaging behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — runtime message-flow knobs; relevance: bot-acceptance/loop-control runtime behavior analog.
- [hermes: messaging Slack](../hermes_agent/hermes_messaging_slack.md) — Slack `bot_id` handling; relevance: Slack native bot-id facts behind loop protection.
- [hermes: messaging Matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix bot accounts; relevance: Matrix configured-bot-pair keying for the guard.
- [hermes: gateway Feishu features](../hermes_agent/hermes_gateway_feishu_features.md) — Google-Chat-like bot facts; relevance: native `sender.type=BOT` acceptance pattern for accepted bot messages.
- [cc: channels security & enterprise controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel safety controls; relevance: cross-tool guardrail view for bot-authored channel traffic.
- [band: agent lifecycle](../band/band_coding_agents_deployment.md) — multi-agent deployment; relevance: deployments with multiple bots are exactly where pair loops arise.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: per-channel bot-fact mapping (`author.bot`, `bot_id`).
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Discord/Slack/Matrix/Google-Chat bot-pair facts.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: the core inbound reply runner enforcing the sliding-window pair guard.

**Snippets**
- [snippet_openclaw_agents_tool_loop_detectors_circuit](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — loop circuit-breaker; relevance: cooldown-after-budget suppression analog (the pair guard's `cooldownSeconds`).
- [snippet_openclaw_agents_tool_loop_detectors_repeat](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_repeat.md) — repeat-loop detector; relevance: sliding-window repeat-event budget analog (`maxEventsPerWindow`/`windowSeconds`).
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — inbound dispatch; relevance: where bot-authored messages reach (or are suppressed before) dispatch.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit policy; relevance: window/cooldown budget mechanics like the pair guard.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source/bot trust; relevance: identifying a reliable inbound bot identity (prereq to opt-in).
- [snippet_hermes_agent_gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — runner ACL (`allowBots`); relevance: gates whether bot messages are accepted at all.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord normalize (`author.bot`); relevance: native Discord bot facts keyed by account/channel/pair.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack inbound (`bot_id`); relevance: Slack native bot-id facts.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix normalize; relevance: configured Matrix bot-pair keying.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway entry dispatch; relevance: pair-suppression check in the inbound entry path.

### oc_channels_broadcast_groups (8t · 10s · 11d)

**Terms**
- [Fan-Out](../../term_dictionary/term_fan_out.md) — one-to-many delivery; relevance: broadcast groups fan one inbound message to multiple agents — the page's core mechanism.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple cooperating agents; relevance: specialized agent teams (reviewer/auditor/docs) each process the same message.
- [Multi-Agent Systems](../../term_dictionary/term_multi_agent_systems.md) — multi-agent architecture; relevance: parallel/sequential agent-team strategy is a multi-agent system pattern.
- [Pub/Sub](../../term_dictionary/term_pub_sub.md) — publish-to-many; relevance: broadcast is a pub/sub-style fan-out to the configured agent set.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating multiple agents; relevance: `strategy: parallel|sequential` orchestrates the agent set.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — per-agent session keys/state; relevance: each broadcast agent keeps a fully isolated session key + history + workspace.
- [Subagent](../../term_dictionary/term_subagent.md) — independent agent worker; relevance: each listed agent runs as an isolated worker with its own tools/model.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: top-level `broadcast` config (WhatsApp-only, experimental) under bindings.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — routing precedence; relevance: broadcast is evaluated after allowlists and takes priority over ordinary route bindings (ACP bindings exclusive).
- [Access groups (planned, this series)](oc_channels_access_groups.md) — allowlist gating; relevance: broadcast does NOT bypass channel allowlists/activation rules.
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway message flow; relevance: closest analog of the route-and-admission → broadcast-check flow.
- [hermes: messaging WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp web channel; relevance: broadcast's current scope is WhatsApp-only (peer JID / E.164 keys).
- [hermes: provider routing](../hermes_agent/hermes_provider_routing.md) — agent/provider routing; relevance: broadcast works alongside existing routing bindings.
- [hermes: FAQ messaging perf/profiles/workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — multi-agent QA workflows; relevance: specialized agent-team + QA-review use cases.
- [cc: subagents overview](../claude_code/cc_subagents_overview.md) — subagent isolation; relevance: isolated session/tool/model per agent mirrors broadcast session isolation.
- [band: chat rooms and routing](../band/band_chat_rooms_and_routing.md) — multi-participant room routing; relevance: fan-out to multiple agent participants in one room.
- [hermes: multi-agent profiles](../hermes_agent/hermes_profiles_multi_agent.md) — running multiple distinct agent profiles; relevance: closest analog of the specialized reviewer/auditor/docs agent set a broadcast group fans one message to.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: broadcast admission after allowlist/activation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents package; relevance: per-agent workspace/tools/model isolation for broadcast members.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: distinct per-agent session keys (`agent:alfred:whatsapp:group:…`).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/runtime config; relevance: server runtime parses the top-level `broadcast` config block.

**Snippets**
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — broadcast runtime config parse; relevance: the exact `broadcast` config schema + strategy field.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/route resolution; relevance: broadcast-vs-binding precedence (broadcast wins, ACP exclusive).
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP bindings; relevance: exclusive ACP bindings short-circuit fan-out broadcast.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key construction; relevance: per-agent isolated session keys for broadcast members.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — multi-agent spawn policy; relevance: spawning the listed agents in parallel/sequential.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — concurrency caps; relevance: 10+ agent limit / performance guidance.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool allow/deny; relevance: read-only vs read-write per broadcast agent.
- [snippet_hermes_agent_gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp dispatch; relevance: broadcast's WhatsApp-only delivery path.

### oc_channels_channel_routing (8t · 10s · 11d)

**Terms**
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — channel/provider selection; relevance: outbound target prefixes + channel-selection hints are the routing model's core.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the channel dispatch core; relevance: deterministic reply-back-to-source routing is the channel kernel's job.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel grammar; relevance: target-kind prefixes (`channel:`/`user:`/`room:`/`thread:`) stay inside each channel's adapter grammar.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — thread→session binding; relevance: Slack/Discord threads append `:thread:<id>`, Telegram topics embed `:topic:<id>`.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — session-key storage; relevance: session-key shapes + on-disk `sessions.json` store layout.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the routing host; relevance: routing is deterministic and host-configuration-controlled (the model does not pick a channel).
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent selection; relevance: routing picks ONE agent per inbound via the 8-step binding ladder.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `agents.list` + `bindings` routing config + `session.store` templating.

**Docs**
- [Broadcast groups (planned, this series)](oc_channels_broadcast_groups.md) — fan-out; relevance: the page's Broadcast-groups pointer (run multiple agents for one peer).
- [Access groups (planned, this series)](oc_channels_access_groups.md) — allowlist gating; relevance: guarded inbound recording respects sender allowlists before routing.
- [Discord routing & access (planned, this series)](oc_channels_discord_routing_access.md) — guild/role routing; relevance: Discord guild+roles binding match is a routing-ladder step.
- [hermes: provider routing](../hermes_agent/hermes_provider_routing.md) — routing rules; relevance: closest analog of the binding-match agent-selection ladder.
- [hermes: provider routing proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider/prefix routing; relevance: outbound provider-prefix selection hints.
- [hermes: gateway internals](../hermes_agent/hermes_gateway_internals.md) — session/route internals; relevance: lastRoute pinning + session-store discovery internals.
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — deterministic reply routing; relevance: reply-back-to-source determinism.
- [cc: channels overview](../claude_code/cc_channels_overview.md) — channel reply model; relevance: cross-tool view of inbound→agent→reply routing.
- [band: chat rooms and routing](../band/band_chat_rooms_and_routing.md) — room→agent routing; relevance: the band routing model analog (room/peer→agent).

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: implements the binding-match routing ladder + target prefixes.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: per-channel grammar + thread/topic key shaping.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: session-key shapes + `sessions.json` store + lastRoute pinning.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: AgentId = isolated workspace + session store.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding→agent route resolution; relevance: the exact bindings/peer/guild/team match ladder.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match-field resolver; relevance: "all provided fields must match" multi-field binding rule.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/route resolution; relevance: maps inbound to its conversation route + reply context.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key shaping; relevance: `agent:<id>:<channel>:group/channel:<id>(:thread:<id>)` shapes.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: DM-collapse-to-main + per-account direct-chat runtime key.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: thread/topic key suffixing + parent-peer inheritance.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — session-store target; relevance: `session.store` + `{agentId}` templating + disk-store scanning.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: provider-prefix advertisement + channel selection hints.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner router; relevance: sibling-impl of the inbound→agent routing decision.
- [snippet_hermes_agent_gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — session-key builder; relevance: per-channel session-key construction analog.

### oc_channels_clickclack (8t · 10s · 11d)

**Terms**
- [Chatbot](../../term_dictionary/term_chatbot.md) — bot user identity; relevance: an OpenClaw agent appears as a ClickClack bot user (service or user-owned bot).
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway; relevance: ClickClack is a `channels.clickclack` gateway channel with its own realtime connection.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel adapter; relevance: ClickClack is a bundled channel plugin/adapter (`plugins.entries.clickclack`).
- [Access Control](../../term_dictionary/term_access_control.md) — token scopes; relevance: `bot:read`/`bot:write`/`bot:admin` scopes enforce ClickClack permissions.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bot token auth; relevance: setup uses a `ccb_...` bot token via SecretRef (`source: env`).
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — outbound targets; relevance: `channel:`/`dm:`/`thread:` target syntax + `defaultTo`/`defaultAccount` routing.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin enable/allow policy; relevance: `plugins.allow`/`plugins.deny`/`enabled` install policy for ClickClack.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `openclaw plugins enable/install clickclack` + `openclaw gateway` setup.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — target/routing model; relevance: ClickClack `channel:`/`dm:`/`thread:` targets reuse the shared routing grammar.
- [Access groups (planned, this series)](oc_channels_access_groups.md) — sender allowlists; relevance: ClickClack participates in shared allowlist auth paths.
- [hermes: messaging Slack config](../hermes_agent/hermes_messaging_slack_config.md) — Slack-like bot-token channel; relevance: closest analog (workspace + bot token + channel/dm targets).
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — per-account channel connections; relevance: each account opens its own realtime connection with its own token.
- [hermes: messaging Mattermost](../hermes_agent/hermes_messaging_mattermost.md) — self-hosted workspace chat; relevance: self-hosted-workspace bot-token model parallel.
- [hermes: env vars & runtime messaging behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — env/SecretRef token config; relevance: `source: env` token resolution (`CLICKCLACK_BOT_TOKEN`).
- [hermes: messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — reply/delivery modes; relevance: `replyMode: model` short bot-reply path.
- [cc: build a channel](../claude_code/cc_build_a_channel.md) — adding a channel; relevance: cross-tool view of wiring a new bot-token chat channel.
- [band: integration methods](../band/band_integration_methods.md) — chat integration patterns; relevance: bot-token chat-workspace integration analog.
- [Discord setup (planned, this series)](oc_channels_discord_setup.md) — sibling channel setup; relevance: parallel bot-token + multiple-accounts setup flow.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: ClickClack channel realtime connection + target parsing.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: bot-token chat-channel plugin family.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/plugins; relevance: `plugins.entries.clickclack` + `allowAgentIdOverride` trust bit.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the per-channel adapter surface ClickClack implements.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry/targets; relevance: `channel:`/`dm:`/`thread:` target normalization.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: `plugins.entries.clickclack` config surface.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/install lifecycle; relevance: `openclaw plugins enable/install` allow/deny policy.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef token resolution; relevance: `token: { source: env, id: CLICKCLACK_BOT_TOKEN }`.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel dispatch; relevance: inbound/outbound dispatch for the ClickClack realtime channel.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: `channels.clickclack.accounts.*` multi-bot config analog.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform; relevance: workspace-bot-token connection analog.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — message send dispatch; relevance: `openclaw message send --channel clickclack --target …`.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory/registry; relevance: registering ClickClack as an available channel.

### oc_channels_discord_setup (8t · 10s · 11d)

**Terms**
- [Chatbot](../../term_dictionary/term_chatbot.md) — Discord bot user; relevance: create a Discord application + bot user and pair it to OpenClaw.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — DM pairing-code approval; relevance: Discord DMs default to pairing mode; approve the first pairing code.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bot token secret; relevance: copy the bot token, store it as `DISCORD_BOT_TOKEN`/SecretRef.
- [OAuth](../../term_dictionary/term_oauth.md) — OAuth2 invite + scopes; relevance: generate the OAuth2 invite URL with `bot`+`applications.commands` scopes.
- [Access Control](../../term_dictionary/term_access_control.md) — guild allowlist; relevance: add the server to the guild allowlist + privileged intents.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway owns the connection; relevance: `openclaw gateway` owns the Discord connection after token+intents.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM enablement; relevance: server "Direct Messages" privacy must allow bot DMs for pairing.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `openclaw config patch` + `openclaw pairing approve discord <CODE>` flow.

**Docs**
- [Discord routing & access (planned, this series)](oc_channels_discord_routing_access.md) — runtime/access; relevance: next step after setup (guild allowlist, role routing, commands).
- [Discord operations (planned, this series)](oc_channels_discord_operations.md) — troubleshooting/config; relevance: setup-failure troubleshooting + config reference.
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — routing model; relevance: post-pairing, Discord inbound routes deterministically back to Discord.
- [hermes: Discord setup](../hermes_agent/hermes_discord_setup.md) — sibling Discord setup; relevance: closest existing analog of the Developer-Portal app+bot+token+invite flow.
- [hermes: Discord advanced](../hermes_agent/hermes_discord_advanced.md) — advanced Discord config; relevance: multi-account application-ID + guild-workspace setup.
- [hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — gateway connection ownership; relevance: gateway owning the Discord gateway connection.
- [hermes: security isolation & credentials](../hermes_agent/hermes_security_isolation_credentials.md) — secret handling; relevance: treat bot tokens as secrets, env/SecretRef storage.
- [cc: channels setup](../claude_code/cc_channels_setup.md) — channel setup flow; relevance: cross-tool view of connecting a chat channel + token.
- [cc: Claude Code in Slack](../claude_code/cc_claude_code_in_slack.md) — bot-app install flow; relevance: parallel app-creation + invite + token model.
- [band: connect remote agent](../band/band_coding_agents_deployment.md) — agent deployment/connect; relevance: standing up the agent the Discord bot fronts.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: Discord gateway connection + intents handling.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Discord channel registration + token resolution.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: SecretRef token providers + least-privilege guidance.

**Snippets**
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord privileged intents; relevance: Message Content / Server Members / Presence intent enablement.
- [snippet_hermes_agent_gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord gateway connect; relevance: token+intents gateway connection bootstrap.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: Discord DM pairing-mode approval path.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — pairing approval; relevance: `openclaw pairing list/approve discord` mechanics.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolution; relevance: account-aware `DISCORD_BOT_TOKEN` SecretRef resolution.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config patch/reload; relevance: `openclaw config patch --file discord.patch.json5`.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — pairing flow; relevance: sibling pairing-code approval analog.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel/account config; relevance: multi-account `accounts.{personal,work}` applicationId config.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: restart gateway after token/intents change; READY wait.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord inbound normalize; relevance: first inbound DM that triggers pairing.

### oc_channels_discord_routing_access (8t · 10s · 11d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — dmPolicy/groupPolicy/allowlists; relevance: DM `pairing/allowlist/open/disabled` + guild allowlist are the page's core.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — binding routing; relevance: role-based agent routing via `bindings[].match.roles`.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — role→agent routing; relevance: different guild roles route to different agents (opus vs sonnet).
- [Blocklist / Safelist](../../term_dictionary/term_blocklist_safelist.md) — users/roles allowlists; relevance: guild `users`/`roles` allowlists; `dangerouslyAllowNameMatching` break-glass.
- [Function Calling](../../term_dictionary/term_function_calling.md) — native slash commands; relevance: `commands.native` slash-command registration + command auth.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — DM allowlist precedence; relevance: multi-account `allowFrom` vs legacy `dm.allowFrom` precedence rules.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — forum/thread routing; relevance: forum channels accept only thread posts; thread session keys.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `channels.discord.guilds.*` + `bindings[]` config model.

**Docs**
- [Channel routing (planned, this series)](oc_channels_channel_routing.md) — routing ladder; relevance: Discord guild+roles/guild match are steps 3-4 of the routing ladder.
- [Access groups (planned, this series)](oc_channels_access_groups.md) — `discord.channelAudience`; relevance: dynamic Discord access-group type used in `allowFrom`.
- [Discord features (planned, this series)](oc_channels_discord_features.md) — slash-command UI; relevance: `/model` picker + command UI sit on the native-command surface.
- [hermes: Discord advanced](../hermes_agent/hermes_discord_advanced.md) — Discord routing/access; relevance: closest analog of guild allowlist + role-based routing.
- [hermes: slash commands (messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — native slash commands; relevance: command registration + command auth model.
- [hermes: provider routing](../hermes_agent/hermes_provider_routing.md) — binding routing; relevance: role/guild binding-match agent selection.
- [hermes: security command approval](../hermes_agent/hermes_security_command_approval.md) — command authorization; relevance: command auth enforces OpenClaw allowlists even when UI shows commands.
- [cc: SDK slash commands](../claude_code/cc_sdk_slash_commands.md) — slash-command definition; relevance: cross-tool native-command catalog model.
- [cc: channel permission relay](../claude_code/cc_channel_permission_relay.md) — channel permission relay; relevance: per-channel auth relay parallels Discord command auth.
- [band: agent API chats & participants](../band/band_agent_api_chats_participants.md) — participant/role access; relevance: role-based participant routing analog.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: Discord dmPolicy/groupPolicy + guild allowlist enforcement.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: forum-channel + thread handling.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agents; relevance: role→agent binding resolution.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions; relevance: guild-channel isolated session keys + slash command sessions.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding route resolution; relevance: guild+roles binding precedence (after peer, before guild-only).
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — multi-field match; relevance: `peer`+`guildId`+`roles` all-must-match rule.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM policy audit; relevance: dmPolicy/allowFrom precedence + name-matching warnings.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist; relevance: Discord `allowFrom`/`accessGroup:` DM authorization.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash commands; relevance: native slash-command registration + auth.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access; relevance: command auth reusing message-channel allowlists.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — Discord thread/forum; relevance: forum-channel thread-post-only routing.
- [snippet_hermes_agent_gw_runner_router](../../code_snippets/snippet_hermes_agent_gw_runner_router.md) — runner router; relevance: role/guild binding-match agent selection analog.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread bindings; relevance: thread/forum session-key binding.
- [snippet_hermes_agent_gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — runner ACL; relevance: guild/channel allowlist enforcement before dispatch.

### oc_channels_discord_features (8t · 10s · 11d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/action surface; relevance: Discord message actions (messaging/moderation/presence) + action gates are tool-call surfaces.
- [Chatbot](../../term_dictionary/term_chatbot.md) — interactive bot UI; relevance: components v2 buttons/selects/modals + ephemeral interactions are bot UX.
- [Access Control](../../term_dictionary/term_access_control.md) — action gates + `allowedUsers`; relevance: per-action default gates (roles/moderation disabled) + button `allowedUsers` restriction.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — outbound component payloads; relevance: the gateway sends components-v2 payloads via the message tool.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — interaction callbacks; relevance: interaction results route back to the agent as inbound messages with a callback TTL.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — Discord-specific surface; relevance: reply tags, components, embeds suppression are Discord-adapter capabilities.
- [Multimodal](../../term_dictionary/term_multimodal.md) — media/file attachments; relevance: `media-gallery`/`file` blocks + `attachment://` references.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `channels.discord.agentComponents.ttlMs`/`ui.components.accentColor` config.

**Docs**
- [Discord routing & access (planned, this series)](oc_channels_discord_routing_access.md) — command surface; relevance: components ride on the native-command + reply surface.
- [Discord voice (planned, this series)](oc_channels_discord_voice.md) — sibling Discord feature; relevance: voice is the other major Discord capability cluster.
- [Ambient room events (planned, this series)](oc_channels_ambient_room_events.md) — visible-reply behavior; relevance: components/replies follow `replyToMode` + visible-reply settings.
- [hermes: Discord advanced](../hermes_agent/hermes_discord_advanced.md) — Discord feature config; relevance: closest analog of components/actions/reply-mode features.
- [hermes: messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — media/embeds delivery; relevance: embeds-vs-components + URL-preview suppression.
- [hermes: slash commands (messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — interactive commands; relevance: `/model`/`/models` interactive picker via components.
- [hermes: tool gateway](../hermes_agent/hermes_tool_gateway.md) — tool/action gating; relevance: action gates (`channels.discord.actions.*`) tool-gating analog.
- [cc: SDK tool rich content](../claude_code/cc_sdk_tool_rich_content.md) — rich tool content/UI; relevance: rich interactive components surfaced through tool output.
- [cc: channel reply tool](../claude_code/cc_channel_reply_tool.md) — channel reply/components; relevance: cross-tool reply-with-components model.
- [band: agent API messages & events](../band/band_agent_api_messages_events.md) — message/interaction events; relevance: interaction callbacks delivered as inbound events.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: components-v2 payload construction + action gates.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Discord message-action catalog (react/timeout/setPresence).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: component/modal block types + media handling.

**Snippets**
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord attachments; relevance: `file`/`media-gallery` blocks + `attachment://` references.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash/interactions; relevance: `/model` interactive picker + ephemeral replies.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — Discord thread/components; relevance: forum parents reject components; send to thread.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reactions/status actions; relevance: `react`/`reactions`/`emojiList` message actions.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: components/embeds payload formatting.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — attachment send; relevance: single-file vs media-gallery attachment delivery.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval components; relevance: components-v2 used for exec approvals + callback TTL.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — approval/permission relay; relevance: button-driven approve/decline workflows + `allowedUsers`.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound delivery; relevance: multi-message structured-component delivery.

### oc_channels_discord_voice (8t · 11s · 11d)

**Terms**
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice conversation mode; relevance: `voice.mode` `agent-proxy`/`stt-tts`/`bidi` is the core conversation-path control.
- [Voice Call](../../term_dictionary/term_voice_call.md) — realtime voice session; relevance: Discord voice channels are continuous realtime voice sessions (`/vc join`).
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — bot in a voice channel; relevance: the bot joins/moves/leaves voice and follows users.
- [Voice Wake](../../term_dictionary/term_voice_wake.md) — wake-name gating; relevance: `voice.realtime.requireWakeName`/`wakeNames` gate realtime auto-response.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live STT preview; relevance: STT transcript preview + partial-transcript wake recognition.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT path; relevance: `stt-tts` mode uses `tools.media.audio` STT; `captureSilenceGraceMs` segmentation.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS playback; relevance: `voice.tts.provider` (OpenAI/ElevenLabs) streaming playback.
- [VoIP](../../term_dictionary/term_voip.md) — realtime audio transport; relevance: `@discordjs/voice` Opus/DAVE-encryption transport + reconnect grace.

**Docs**
- [Discord features (planned, this series)](oc_channels_discord_features.md) — sibling Discord feature; relevance: voice is one of Discord's two major capability clusters.
- [Discord setup (planned, this series)](oc_channels_discord_setup.md) — intents/scopes prerequisite; relevance: voice needs Connect/Speak perms + Message Content/Server Members intents.
- [hermes: voice gateway Discord VC](../hermes_agent/hermes_voice_gateway_discord_vc.md) — Discord voice-channel gateway; relevance: closest existing analog — Discord `/vc` voice-channel runtime.
- [hermes: use voice mode guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode usage; relevance: agent-proxy vs stt-tts vs realtime conversation paths.
- [hermes: voice mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice CLI; relevance: `/vc join|leave|status` command behavior analog.
- [hermes: messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — media/TTS settings; relevance: TTS provider/voice + media conversion settings.
- [cc: voice dictation](../claude_code/cc_voice_dictation.md) — voice input; relevance: cross-tool voice-input/STT model.
- [hermes: messaging Signal](../hermes_agent/hermes_messaging_signal.md) — channel voice/media messages; relevance: voice-message attachment (waveform OGG/Opus, ffmpeg/ffprobe) media-handling analog.
- [band: agent context & activity](../band/band_agent_api_context_activity.md) — media/audio context; relevance: audio turns as agent context analog.
- [hermes: TTS providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech provider catalog/config; relevance: `voice.tts.provider` (OpenAI/ElevenLabs) provider selection + streaming-playback options.

**Repos**
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channels; relevance: realtime voice-channel runtime + media stream.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: STT/TTS providers (Deepgram/ElevenLabs/OpenAI realtime).
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: Discord `voice.*` config + `GuildVoiceStates` intent.

**Snippets**
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: realtime voice session lifecycle (join/connect/reconnect).
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-session manager; relevance: `/vc join|leave|status` session management.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — audio media stream; relevance: Opus PCM playback + receive path.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — stream transcription; relevance: STT segment finalization + transcript preview.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — speaker admission/barge-in; relevance: barge-in / `minBargeInAudioEndMs` echo handling.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: STT provider behind `stt-tts` mode.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs streaming TTS; relevance: streaming TTS playback start-from-stream.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — wake-name tracking; relevance: `requireWakeName`/`wakeNames` gating.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: relaying transcripts to the routed agent consult.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: agent-proxy `openclaw_agent_consult` voice path analog.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: `voice.tts` provider/voice selection.

### oc_channels_discord_operations (8t · 10s · 11d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — groupPolicy/allowlist debugging; relevance: "guild messages blocked unexpectedly" → verify groupPolicy + guild/channel allowlist.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — Discord rate limits + queue knobs; relevance: gateway listener timeout / event-queue knobs + bot-loop rate limits.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway READY/metadata; relevance: `/gateway/bot` metadata + READY-timeout startup operations.
- [Chatbot](../../term_dictionary/term_chatbot.md) — bot operations; relevance: bot-to-bot loop config + `channels status --probe` operations.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — dispatch/queue; relevance: stuck-session / slow-listener gateway-queue diagnostics.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — queued turn lifecycle; relevance: queued Discord runs preserve per-session ordering until lifecycle completes.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — config-reference fields; relevance: high-signal config fields (routing/reply/delivery/streaming).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: `openclaw doctor`/`channels status --probe`/`openclaw update` operations.

**Docs**
- [Discord setup (planned, this series)](oc_channels_discord_setup.md) — setup; relevance: intent/token misconfig is the root of many troubleshooting cases.
- [Discord routing & access (planned, this series)](oc_channels_discord_routing_access.md) — allowlist/policy; relevance: blocked-message diagnostics map to groupPolicy/allowlist config.
- [Discord voice (planned, this series)](oc_channels_discord_voice.md) — voice troubleshooting; relevance: `DecryptionFailed(...)` voice-STT recovery is a key ops case.
- [Bot loop protection (planned, this series)](oc_channels_bot_loop_protection.md) — bot loops; relevance: the bot-to-bot loop troubleshooting accordion points here.
- [hermes: gateway operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops/troubleshooting; relevance: closest analog of restart/probe/doctor operational flow.
- [hermes: Discord advanced](../hermes_agent/hermes_discord_advanced.md) — Discord config reference; relevance: high-signal Discord config-field reference.
- [hermes: gateway internals](../hermes_agent/hermes_gateway_internals.md) — queue/session internals; relevance: stuck-session / event-queue listener internals.
- [hermes: FAQ messaging perf/profiles/workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — perf troubleshooting; relevance: slow-listener / long-running-turn perf profiles.
- [cc: channels security & enterprise controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel safety/ops; relevance: safety-and-operations least-privilege guidance.
- [band: coding agents deployment](../band/band_coding_agents_deployment.md) — agent operations; relevance: operating/restarting the deployed agent behind the channel.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels package; relevance: Discord event-queue + gateway-timeout knobs.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: `openclaw security audit` + least-privilege ops.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway core; relevance: READY/metadata-timeout startup + restart handling.

**Snippets**
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: restart-after-intent-change + READY-timeout startup.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: metadata-timeout / gateway-connect failure diagnostics.
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable dispatch/queue; relevance: stuck-session + per-session ordering of queued runs.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security audit; relevance: `openclaw security audit` name-match/permission warnings.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — probe execution; relevance: `channels status --probe` permission checks (numeric IDs only).
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — `openclaw doctor` repair; relevance: `openclaw doctor`/`--fix` config-migration diagnostics.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — voice decrypt/recovery; relevance: DAVE `DecryptionFailed` auto-rejoin recovery.
- [snippet_hermes_agent_gw_runner_errors](../../code_snippets/snippet_hermes_agent_gw_runner_errors.md) — runner error handling; relevance: long-running-turn / duplicate-reply error paths.
- [snippet_hermes_agent_gw_runner_supervisor](../../code_snippets/snippet_hermes_agent_gw_runner_supervisor.md) — runner supervisor; relevance: gateway restart/supervision after stale command state.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: "disallowed intents / no guild messages" intent-fix troubleshooting.

## Undigested Terms Plan

Per master: OpenClaw channel vocabulary terms are the subjects of the doc pages themselves and are digested as
`oc_*` documentation concept notes by THIS sub-plan — NOT promoted to new `term_dictionary` entries. The only
`term_dictionary` interaction is **linking existing** terms. **Expected new `term_dictionary` captures: 0.**

| Term (from source) | Disposition |
|---|---|
| access group / sender group / allowlist / audience | → `oc_channels_access_groups` (note 1); link existing `term_access_control` (no `term_allowlist` / `term_rbac` exists — do NOT cite as ghost; substitute `term_access_control`). |
| ambient room event / visible reply mode | → `oc_channels_ambient_room_events` (note 2); doc concept, not a term. |
| broadcast group / fan-out / session isolation | → `oc_channels_broadcast_groups` (note 4); link existing `term_fan_out`, `term_pub_sub`, `term_multi_agent`. |
| channel routing / target prefix / session key / routing rule | → `oc_channels_channel_routing` (note 5); link `term_provider_routing`, `term_messaging_gateway`. |
| ClickClack | → `oc_channels_clickclack` (note 6); platform name documented as config, not a term. |
| Discord / guild / intents / forum channel / interactive component / Components v2 / slash command / voice channel | → discord notes 7–11; platform features documented as config/reference, not terms. `term_discord` / `term_telegram` do not exist — link `term_chatbot` / `term_messaging_gateway` instead. |
| voice channel / follow-in-voice / voice message (Discord) | → `oc_channels_discord_voice` (note 10); link existing `term_voice_call`, `term_voice_bot`, `term_voice_mode`, `term_voice_wake`, `term_text_to_speech`, `term_speech_to_text`, `term_voip`. |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term with no doc-page home AND no existing
note appeared. All channel vocabulary either has a doc-page home (`oc_*`) or maps to an existing term. Augment
Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master). If augment's
Step 2d re-scan surfaces a genuine new cross-cutting term, it is captured via `/tessellum-capture-term-note` + added
to the best-fit `acronym_glossary_*.md` (most likely `acronym_glossary_agentic_ai.md` / a messaging glossary) per
master W5 — not expected for ch01.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). Gate table identical to the master's 9-GATE:

| Gate | Check | Tooling |
|---|---|---|
| G1 | Format (YAML field order + body sections) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no fabrication vs source) | diff each note vs `inbox/openclaw_docs/channels/<page>.md` |
| G3 | Density + Coverage (≤400L / ≤2,500w / ≤6 code; every H2/H3 mapped) | per-note word/code count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevancy terms + repos + siblings, relevance statements) | Candidate Cross-References → locked at augment |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability — each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`; in-degree ≥1 (anti-island) | satisfied via `entry_openclaw_docs.md` + Inlinks section |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

All gates must PASS before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_channels_access_groups oc_channels_ambient_room_events oc_channels_bot_loop_protection oc_channels_broadcast_groups oc_channels_channel_routing oc_channels_clickclack oc_channels_discord_setup oc_channels_discord_routing_access oc_channels_discord_features oc_channels_discord_voice oc_channels_discord_operations"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url:' "$f" || echo "MISSING source_url in $n"; }
  # density caps (≤2500w / ≤6 code)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # at least one sibling oc_ cross-link present
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) LINK in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤400L / ≤2,500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_channels_access_groups | procedure | 650 | ≤4 | ✅ |
| 2 | oc_channels_ambient_room_events | procedure | 650 | ≤4 | ✅ |
| 3 | oc_channels_bot_loop_protection | procedure | 450 | ≤2 | ✅ |
| 4 | oc_channels_broadcast_groups | procedure | 750 | ≤4 | ✅ |
| 5 | oc_channels_channel_routing | concept | 700 | ≤3 | ✅ |
| 6 | oc_channels_clickclack | procedure | 450 | ≤4 | ✅ |
| 7 | oc_channels_discord_setup | procedure | 700 | ≤5 | ✅ |
| 8 | oc_channels_discord_routing_access | procedure | 700 | ≤5 | ✅ |
| 9 | oc_channels_discord_features | model | 700 | ≤6 | ✅ |
| 10 | oc_channels_discord_voice | procedure | 700 | ≤5 | ✅ |
| 11 | oc_channels_discord_operations | procedure | 600 | ≤4 | ✅ |

No output note approaches the caps. The oversized `discord.md` (9,637w / 42 code) split into 5 notes keeps each ≤700w
and ≤6 code via selective verbatim reproduction (digest, not full mirror).

## Entry Point Decision (inherited from master)

This sub-plan contributes **11 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under a
**"Channels (ch01)"** cluster: access groups, ambient room events, bot loop protection, broadcast groups, channel
routing, ClickClack, and the 5 Discord notes. Each new note receives its entry-point back-link at finalization
(satisfying G7/G8). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; each new note needs ≥1 for in-degree ≥1 / G7-G8):
- `entry_openclaw_docs.md` (W1) → **all 11 notes** (primary inbound source; guarantees G8).
- `repo_openclaw_channels.md` → notes 1, 2, 4, 5, 6, 7, 8, 11.
- `repo_openclaw_channels_messaging.md` → notes 1, 2, 5, 8, 9.
- `repo_openclaw_channels_voice_phone.md` → note 10.
- `term_access_control.md` → notes 1, 8, 11; `term_voice_call.md` → note 10; `term_fan_out.md` → note 4;
  `term_provider_routing.md` → note 5; `term_slack.md` → note 1; `term_chatbot.md` → notes 3, 6.

## Pacing Rules (inherited from master)

One execution phase (11 notes, ≤30 fan-out cap). Re-read each source page before authoring its note(s); reproduce
config snippets verbatim (≤6 per note); one building_block per note. 8 gates pass before commit. Reindex
incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash`
first; commit+push after the phase; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment: per-note Related Notes LOCKED at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augmentation pass (xref-augment):** re-read all 7 ch01 source pages under
`inbox/openclaw_docs/channels/` (access-groups, ambient-room-events, bot-loop-protection, broadcast-groups,
channel-routing, clickclack, discord — discord read in full across all 18 H2/H3), then built a relevance-selected,
**≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** per note (PLUS
relevant `repo_openclaw*` + sibling `oc_*`). The prior `## Candidate Cross-References` (master ≥6-term floor) was
**replaced** by the locked mapping.

**What was locked.** Each note's mapping is grouped into **Terms / Docs / Repos / Snippets**, every link rendered as
`- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`. Relative paths resolve from
`resources/documentation/openclaw/oc_X.md` (term `../../term_dictionary/…`, snippet `../../code_snippets/…`, other
doc `../<folder>/…`, sibling `oc_…`, repo `../../../areas/code_repos/…`, entry `../../../0_entry_points/…`).

**DB-verification (G5 / 0-ghost).** Every cited EXISTING note_id was verified via `sqlite3 … SELECT 1 FROM notes
WHERE note_id=…` on 2026-06-21: **terms 52/52 OK · snippets 80/80 OK · docs 51/51 OK · repos 11/11 OK · entries
5/5 OK**. A deterministic full-section link extraction (355 link targets) re-resolved + re-checked every target:
(the lone `relpath.md` match is the format-spec example in the section header, not a citation).

**Per-note locked counts (all floors MET):**

| Note | terms | snippets | docs (existing-other / sibling / hub) | repos | floors met |
|---|---:|---:|---|---:|---|
| oc_channels_access_groups | 8 | 10 | 11 (8 / 2 / 1) | 3 | ✅ |
| oc_channels_ambient_room_events | 8 | 10 | 11 (8 / 2 / 1) | 3 | ✅ |
| oc_channels_bot_loop_protection | 8 | 10 | 11 (8 / 2 / 1) | 3 | ✅ |
| oc_channels_broadcast_groups | 8 | 10 | 10 (7 / 2 / 1) | 4 | ✅ |
| oc_channels_channel_routing | 8 | 10 | 11 (7 / 3 / 1) | 4 | ✅ |
| oc_channels_clickclack | 8 | 10 | 11 (7 / 3 / 1) | 3 | ✅ |
| oc_channels_discord_setup | 8 | 10 | 11 (7 / 3 / 1) | 3 | ✅ |
| oc_channels_discord_routing_access | 8 | 10 | 11 (7 / 3 / 1) | 4 | ✅ |
| oc_channels_discord_features | 8 | 10 | 11 (7 / 3 / 1) | 3 | ✅ |
| oc_channels_discord_voice | 8 | 11 | 10 (7 / 2 / 1) | 3 | ✅ |
| oc_channels_discord_operations | 8 | 10 | 11 (6 / 4 / 1) | 3 | ✅ |

`pi/`), exceeding the ≥5-existing-of-10 requirement; the remainder toward the 10-doc floor are sibling `oc_*`
"(planned, this series)" + the `entry_openclaw_docs` "(planned, W1)" hub. All snippets are EXISTING.

**Richer-than-planned vocabulary found on re-read (master ≥6 → raised ≥8 easily clears it).** The plan's draft
Candidate Cross-References substituted generic terms because it assumed `term_discord`/`term_allowlist`/`term_rbac`/
`term_session` did not exist. The re-read + BM25 scan surfaced a much richer OpenClaw/channel-specific term set that
IS in the vault and is far more relevant: `term_dm_pairing`, `term_dm_policy`, `term_thread_binding_policy`,
`term_channel_kernel`, `term_channel_adapter`, `term_silence_token`, `term_agent_lifecycle_event`,
`term_blocklist_safelist`, `term_deny_first`, `term_realtime_transcription`, `term_pushtotalk`, `term_voice_mode`,
`term_provider_plugin`, `term_session_persistence`, `term_agent_orchestration`, `term_subagent`, `term_delegate_task`.
These replaced the weaker generic substitutes in the locked mapping (relevance-selected, no padding).

**New-term candidates: NONE.** Per master + this sub-plan's Undigested Terms Plan, OpenClaw channel vocabulary is
digested as `oc_*` documentation concept notes by THIS sub-plan, not promoted to `term_dictionary`. The xref re-read
surfaced no genuinely cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note — every
channel concept either has an `oc_*` home or maps to an existing term (now richly linked). Best-fit glossary if one
ever surfaced would be `acronym_glossary_agentic_ai.md` (per master W5). **Expected new `term_dictionary` captures: 0
(unchanged).**

**Issues / notes for execution:** (1) `entry_openclaw_docs.md` is the only non-existing reference cited (40
planned-link instances across the 11 notes) — it MUST be created at master pre-step W1 before execution, else those
links are ghosts at G5 (this is the master's W1 obligation, not a defect of this sub-plan). (2) The 51 cited existing
(`bash scripts/update_notes_database.sh --force` then re-run the G5 extraction).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of the augmented sub-plan. CP7 spot-checked source word counts against the mirror
(`wc -w` on `inbox/openclaw_docs/channels/*`): access-groups 853w, ambient-room-events 915w, bot-loop-protection
485w, broadcast-groups 1,475w, channel-routing 868w, clickclack 525w, discord 9,637w — **all match the plan's Source
table exactly (ratio 1.00)**.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors) | **PASS** | Per-Note Related Notes Mapping (LOCKED) — all 11 notes at ≥8 terms · ≥10 snippets · ≥10 docs, each link with a `relevance:` statement; deterministic count confirms floors met for every note. |
| CP2 | 9-GATE table present per batch (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present (single phase, 11 notes); G5 ghost-detect + G6 broken-link-fix + G7/G8 discoverability all listed with tooling. |
| CP3 | Entry point specified + inherited | **PASS** | `## Entry Point Decision` — 11 rows into `entry_openclaw_docs.md` (created master pre-step W1) under a "Channels (ch01)" cluster; no new entry point created here (inherited from master, size-threshold satisfied by the 105-sub-plan >30-note master CREATE). |
| CP4 | Plan size manageable (≤30) | **PASS** | 11 planned notes (single execution phase, ≤30 fan-out cap). |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited verbatim from master's Format Definition, itself derived from existing `claude_code/`+`pi/` doc corpora (`## Overview` / `## Related Notes` / `**Source**` footer; forbidden-field list); target dir `resources/documentation/openclaw/` confirmed in scan map (`openclaw → dev_tool_docs`). |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 11 notes ≤700w / ≤6 code, well under caps; discord.md (9,637w/42 code) split into 5 BB-atomic notes per Split Decisions; no borderline note left unaddressed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured `wc -w` on all 7 mirror pages — every count matches the Source table exactly (1.00 ratio); discord fence count 84/2=42 matches. |
| CP8 | Undigested Terms Plan + Authoring Reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned to `oc_*` home or existing-term link; 0 new captures) + `## Term-Note Authoring Requirements` present (N/A 0 new terms, with W5 fallback to `/tessellum-capture-term-note` + best-fit glossary if a term surfaces). |
| CP8f | Term-slug specificity / collision (all-notes dedup) | **PASS** | Collision audit run across `term_dictionary/` AND `resources/documentation/`: the 11 `oc_channels_*` slugs do not duplicate any existing term/doc (code-side `repo_openclaw*` are LINKED not recreated per master dedup policy); no too-general slug (all `oc_channels_<specific>`); 0 new term slugs to specificity-audit. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Pre-execution dependency: `entry_openclaw_docs.md` must exist (master
W1) before the batch runs, or its 40 cited link-instances become G5 ghosts.
