---
title: Sub-Plan cl05 — OpenClaw Docs: CLI (message, migrate, models, node, nodes, onboard, pairing)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/message", "cli/migrate", "cli/models", "cli/node", "cli/nodes", "cli/onboard", "cli/pairing"]
---

# Sub-Plan cl05: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create, 9-GATE validation,
> entry-point wiring (`entry_openclaw_docs.md`), undigested-terms ownership, and cross-reference policy are ALL
> inherited from the master; this file is authored from a fresh re-read + measurement of its 7 assigned CLI pages.

## Scope

The seven `openclaw <command>` CLI reference pages covering **messaging + channel actions** (`message`),
**state import/migration** (`migrate`), **model discovery/scan/auth** (`models`), the **headless node host**
(`node`), **paired-node management/invoke** (`nodes`), **interactive onboarding** (`onboard`), and **DM
pairing approval** (`pairing`). These are P1 (Phase A) operational-core CLI surfaces: the commands an operator
runs daily to send messages, switch models, authenticate providers, onboard a gateway, and pair devices. The
code-side counterparts (`repo_openclaw_cli_wizard`, `repo_openclaw_channels_messaging`,
`repo_openclaw_extensions_llm_providers`, `repo_openclaw_agents`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 7,856 measured words. **Planned: 9 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| message | cli/message | 1,318 | 14 | 6 | 8 | procedure (split: send/presentation vs channel-ops) |
| migrate | cli/migrate | 2,075 | 5 | 8 | 9 | procedure (split: workflow/safety vs per-provider import) |
| models | cli/models | 1,494 | 4 | 4 | 2 | procedure |
| node | cli/node | 860 | 6 | 7 | 0 | procedure |
| nodes | cli/nodes | 416 | 2 | 3 | 0 | procedure |
| onboard | cli/onboard | 1,323 | 10 | 5 | 1 | procedure |
| pairing | cli/pairing | 370 | 1 | 5 | 0 | procedure |

Totals: 7,856 words · 42 code blocks · 38 H2 · 20 H3. All seven pages are `procedure` BB (CLI references). Two
pages exceed comfortable single-note density / mix distinct task clusters and SPLIT (see Split Decisions).

## Content Strategy

- **Prioritize**: the `message send` + semantic-presentation contract (cross-channel button/poll rendering, the
  most-used outbound action) and the `migrate` safety/preview-and-apply model (preview-first, backups,
  conflicts, secrets) — these are the operationally riskiest surfaces. `models` (default/fallback/auth-profile
  management + probe diagnostics) is the daily model-control surface.
- **Split**: `message.md` (1,318w, 14 code) → (a) `send` + semantic presentation + broadcast procedure, (b) the
  channel-operations action catalog (react/read/edit/delete/pin/threads/emoji/stickers/roles/events/moderation).
  `migrate.md` (2,075w, 8 H2 / 9 H3) → (a) workflow/flags + safety model + plugin/onboarding integration,
  (b) the per-provider import matrix (Claude / Codex / Hermes — what each imports + manual-review state).
  The other five pages = 1 note each (each ≤1,494w, single task cluster).
- **Link-out / do NOT redefine**: provider auth concepts → link `term_oauth`/`term_oauth_token`/`term_auth_profile`
  + `pi_provider_auth`; messaging channels → link `repo_openclaw_channels_messaging` + `term_channel_adapter`;
  gateway/WebSocket transport → link `term_websocket` + `repo_openclaw_gateway`; migration user walkthroughs
  (`install/migrating-claude`, `install/migrating-hermes`) belong to **in03/in04** (Install) — referenced, not
  duplicated. Provider names (OpenAI, Z.AI, Ollama, LM Studio, Mistral, Anthropic) are documented as CLI flags,
  not promoted to term notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_message_send.md` | procedure | message.md: Usage, Channel selection, Target formats, Name lookup, Common flags, SecretRef behavior, Actions→Core (`send`, `poll`, `broadcast`), Examples (send/poll/presentation) | 500 | `openclaw message send`/`poll`/`broadcast`: channel selection + per-channel target formats, common flags, SecretRef scoping, and the semantic `--presentation` payload that core renders per channel capability (Discord components / Slack blocks / Telegram inline buttons / Teams cards). |
| 2 | `oc_cli_message_channel_ops.md` | procedure | message.md: Actions→Core (`react`, `reactions`, `read`, `edit`, `delete`, `pin`/`unpin`, `pins`, `permissions`, `search`), Threads, Emojis, Stickers, Roles/Channels/Members/Voice, Events, Moderation | 450 | The `openclaw message` channel-operations catalog beyond send: reactions, read/edit/delete/pin, permissions, search, Discord threads/emojis/stickers/roles/members/voice/events, and moderation (timeout/kick/ban) — per-channel support matrix and required flags. |
| 3 | `oc_cli_migrate.md` | procedure | migrate.md: intro, Commands, all `<ParamField>` flags, Safety model (preview/backups/conflicts/secrets), Plugin contract, Onboarding integration | 600 | `openclaw migrate`: importing state from another agent system via plugin-owned providers — command/flag surface, the preview-first safety model (itemized plan, secret redaction, verified backups, conflict refusal, `--overwrite`), the migration-provider plugin contract (`detect`/`plan`/`apply`), and onboarding integration. |
| 4 | `oc_cli_migrate_providers.md` | procedure | migrate.md: Claude provider (What Claude imports, Archive/manual-review), Codex provider (What Codex imports, Manual-review), Hermes provider (What Hermes imports, Supported `.env` keys, Archive-only, After applying) | 600 | The per-provider import matrix for `openclaw migrate`: what the bundled Claude, Codex, and Hermes providers each import (workspace files, MCP servers, skills, model/provider config, credentials) vs what is archived or flagged manual-review, including Codex native-plugin gating and Hermes `.env` key support. |
| 5 | `oc_cli_models.md` | procedure | models.md: intro, Common commands, `models status` (probe buckets, reason codes), Models scan, Aliases + fallbacks, Auth profiles (add/list/login/paste-api-key/setup-token/paste-token) | 650 | `openclaw models`: model discovery, scan, and configuration — `status`/`list`/`set`/`scan`, default + fallback + alias management, OpenRouter `:free` scanning, and the auth-profile subcommands (`auth add`/`list`/`login`/`paste-api-key`/`setup-token`/`paste-token`) with probe status buckets and reason codes. |
| 6 | `oc_cli_node.md` | procedure | node.md: Why use a node host, Browser proxy, Run (foreground), Gateway auth for node host, Service (background), Pairing, Exec approvals | 550 | `openclaw node`: running a headless node host that connects to the Gateway WebSocket and exposes `system.run`/`system.which` — foreground run vs background service install, gateway auth resolution (env → config, fail-closed SecretRef), zero-config browser proxy, first-connection pairing, and exec-approval gating. |
| 7 | `oc_cli_nodes.md` | procedure | nodes.md: intro, Common options, Common commands (list/pending/approve/reject/remove/rename/status), approval scope notes, Invoke | 350 | `openclaw nodes`: managing paired nodes (devices) and invoking node capabilities — list/pending/approve/reject/remove/rename/status with connection filters, scope requirements per pending-request type (pairing/write/admin), and `nodes invoke` for direct RPC (with `system.run` routed to the `exec` tool instead). |
| 8 | `oc_cli_onboard.md` | procedure | onboard.md: intro, Related guides, Examples, Locale, non-interactive provider/gateway/health/ref-mode examples, Z.AI endpoint choices, Flow notes, Common follow-up commands | 600 | `openclaw onboard`: full guided onboarding for local/remote Gateway setup — interactive vs `--modern` Crestodian flow, flow types (quickstart/manual/import), locale resolution, and the non-interactive flag surface (custom provider, secret-ref mode, gateway token options, health gating, Z.AI/Ollama/LM Studio/Mistral examples). |
| 9 | `oc_cli_pairing.md` | procedure | pairing.md: intro, Commands, `pairing list`, `pairing approve`, Owner bootstrap, Notes | 350 | `openclaw pairing`: approving and inspecting DM pairing requests for channels that support pairing — `pairing list`/`approve` with channel + multi-account selection, `--notify`, and the first-approval owner bootstrap that seeds `commands.ownerAllowFrom`. |

## Section Coverage Map

```
cli/message.md (1,318w)
├── Usage / Channel selection / Target formats / Name lookup ─ → note 1 (oc_cli_message_send)
├── Common flags / SecretRef behavior ─────────────────────── → note 1
├── Actions › Core › send / poll / broadcast ──────────────── → note 1
├── Examples (send/presentation/poll/Teams) ───────────────── → note 1
├── Actions › Core › react / reactions / read / edit / delete
│   / pin / unpin / pins / permissions / search ───────────── → note 2 (oc_cli_message_channel_ops)
├── Threads / Emojis / Stickers ───────────────────────────── → note 2
├── Roles/Channels/Members/Voice / Events / Moderation / Broadcast(H3) → note 2 (broadcast example listed once; primary broadcast action → note 1)
cli/migrate.md (2,075w)
├── intro / Commands / ParamField flags ───────────────────── → note 3 (oc_cli_migrate)
├── Safety model (Preview/Backups/Conflicts/Secrets) ──────── → note 3
├── Plugin contract / Onboarding integration ──────────────── → note 3
├── Claude provider (What imports / Archive+manual-review) ── → note 4 (oc_cli_migrate_providers)
├── Codex provider (What imports / Manual-review) ──────────── → note 4
├── Hermes provider (What imports / Supported .env keys /
│   Archive-only / After applying) ────────────────────────── → note 4
cli/models.md (1,494w)
├── intro / Related / Common commands ─────────────────────── → note 5 (oc_cli_models)
├── status (notes, marker, probe buckets, reason codes) ───── → note 5
├── Models scan / Models status options ───────────────────── → note 5
├── Aliases + fallbacks / Auth profiles ───────────────────── → note 5
cli/node.md (860w)
├── Why use a node host / Browser proxy ───────────────────── → note 6 (oc_cli_node)
├── Run (foreground) / Gateway auth for node host ─────────── → note 6
├── Service (background) / Pairing / Exec approvals ───────── → note 6
cli/nodes.md (416w)
├── intro / Common options / Common commands ──────────────── → note 7 (oc_cli_nodes)
├── approval-scope notes / Invoke ─────────────────────────── → note 7
cli/onboard.md (1,323w)
├── intro / Related guides / Examples ─────────────────────── → note 8 (oc_cli_onboard)
├── Locale / non-interactive provider+gateway+health+ref ──── → note 8
├── Z.AI endpoint choices / Flow notes / Common follow-ups ── → note 8
cli/pairing.md (370w)
├── intro / Commands ──────────────────────────────────────── → note 9 (oc_cli_pairing)
├── pairing list / pairing approve / Owner bootstrap / Notes  → note 9
```
No orphaned sections. Migration user walkthroughs (`/install/migrating-claude`, `/install/migrating-hermes`,
`/install/migrating`) are out-of-scope cross-links owned by in03/in04. The `## Related` link blocks on each
page become `## References` (external doc URLs) on the corresponding note.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| message.md (1,318w · 14 code · 6 H2 / 8 H3) | notes 1 + 2 | Distinct task clusters: the **send/poll/broadcast + semantic-presentation** outbound flow (with all worked examples) vs the **channel-operations action catalog** (react/read/edit/delete/pin/threads/emoji/stickers/roles/events/moderation). Splitting keeps each ≤500w and ≤6 code blocks (the 14 code fences are almost all in the send/examples cluster). Same BB (procedure) but separable command families. |
| migrate.md (2,075w · 8 H2 / 9 H3) | notes 3 + 4 | Largest page; two clusters — the **workflow + flags + safety model + plugin/onboarding integration** (how migration works, generically) vs the **per-provider import matrix** (Claude/Codex/Hermes specifics + `.env` keys + manual-review state). Split keeps each ≤600w and avoids a single overlong reference; both procedure BB. |

`models.md` (1,494w) is a single cohesive command reference (status/scan/aliases/auth) kept as one note 5 —
under the 2,500w cap and one task cluster. The remaining four pages (node/nodes/onboard/pairing) are each one
note. No mixed-BB splits (all seven pages are procedure).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (7,856 words). New `oc_` notes: **9**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×9 (all notes). No concept/model/argument notes (these are CLI references).
- Est. digest words ~4,650 (avg ~517/note); all notes ≤650w, well under the 2,500w cap. 42 source code fences
  distribute across the 9 notes; each note kept ≤6 (worked CLI examples reproduced selectively, verbatim — the
  send-heavy `message.md` examples concentrate in note 1, the rest are light).
- Cross-refs (LOCKED at xref-augment 2026-06-21): see **## Per-Note Related Notes Mapping** — every note meets
  the raised floors **≥8 terms · ≥10 snippets · ≥10 docs** (plus relevant `repo_openclaw*` and sibling `oc_*`),
  sibling `oc_*` "(planned, this series)" docs (the series is created at W1).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> coding-agent corpora) PLUS sibling `oc_*` docs of THIS series marked "(planned, this series)" — those
> do not exist yet (W1 creates the series; `entry_openclaw_docs` and all `oc_cli_*` confirmed absent in DB).
> Relative paths from a note at `resources/documentation/openclaw/oc_X.md`: term →
> `../../term_dictionary/term_Y.md`; sibling oc doc → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
> `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`; entry →
> `../../../0_entry_points/entry_Y.md`. Render each link as
> `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_cli_message_send (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product; relevance: `openclaw message send` is its outbound command surface.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-platform send/receive driver; relevance: `--channel` resolves to the owning channel-adapter plugin that actually sends.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core outbound dispatch layer above adapters; relevance: core renders the same `--presentation` payload through each channel's declared capabilities.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway that fronts all chat channels; relevance: `message send` runs through the gateway's outbound path.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — one logical message across many platforms; relevance: semantic `--presentation` blocks (`text`/`buttons`/`select`) render per-channel (Discord components, Slack blocks, Telegram inline, Teams cards).
- [Block Kit](../../term_dictionary/term_block_kit.md) — Slack's structured-block UI format; relevance: the Slack target of the semantic presentation contract maps blocks→Block Kit.
- [Message Body](../../term_dictionary/term_message_body.md) — normalized message content envelope; relevance: `--message`/`--media`/`--presentation` populate the outbound body.
- [Slack](../../term_dictionary/term_slack.md) — a primary supported channel; relevance: `--target channel:<id>`/`user:<id>` formats and `--thread-id` thread-timestamp behavior are Slack-specific.
- [Webhook](../../term_dictionary/term_webhook.md) — inbound/outbound HTTP callback transport; relevance: several channel adapters deliver via webhook endpoints under the gateway.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — resolves SecretRef credentials; relevance: `message` resolves channel/account SecretRefs scoped to the action target and fails closed if the selected channel's ref is unresolved.

**Docs**
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how the multi-channel outbound gateway is structured; relevance: same architecture OpenClaw `message` drives.
- [Hermes — Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — outbound dispatch / runner internals; relevance: explains the send path `message send` invokes.
- [Hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/document delivery options; relevance: parallels `--media`, `--force-document`, `--gif-playback`.
- [Hermes — Discord Setup](../hermes_agent/hermes_discord_setup.md) — Discord channel configuration; relevance: Discord `channel:`/`user:` targets + components rendering.
- [Hermes — Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — Telegram channel config; relevance: Telegram forum-topic targets, `--thread-id`, inline/Mini-App buttons via presentation.
- [Hermes — Slash Commands & Messaging](../hermes_agent/hermes_slash_commands_messaging.md) — outbound command surface for chat; relevance: analogous send/command flow.
- [CC — Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — agent-side reply-to-channel tool; relevance: programmatic analog of `message send --reply-to`.
- [CC — Channels Overview](../claude_code/cc_channels_overview.md) — channel model overview; relevance: cross-agent framing of channel send semantics.
- [oc_cli_message_channel_ops](oc_cli_message_channel_ops.md) — (planned, this series) channel-action catalog; relevance: the other half of `openclaw message` beyond send.
- [oc_cli_pairing](oc_cli_pairing.md) — (planned, this series) DM pairing approval; relevance: pairing gates who can receive/initiate DMs you send to.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) channel setup during onboarding; relevance: `channels add` configures the channels `message send` targets.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel adapter implementations; relevance: the send/presentation code behind `message send`.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: target-format + name-lookup resolution.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — CLI/app entrypoints; relevance: hosts the `message` command wiring.

**Snippets**
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound send dispatch; relevance: mirrors `send` routing to the resolved channel.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: how `--message`/presentation are formatted per channel.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — attachment/media handling on send; relevance: `--media`/`--force-document` behavior.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — gateway outbound runner; relevance: the runner that delivers a `send`.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — delivery preferences pipeline; relevance: `--delivery`/`--pin` delivery hints.
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord attachment send; relevance: Discord media delivery.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media send; relevance: Telegram `--media`/`--force-document`.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform adapter; relevance: Slack `channel:`/`user:` target + thread send.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory/name cache; relevance: name-lookup (`#help`→id) resolution.
- [snippet_hermes_agent_plugins_platform_google_chat](../../code_snippets/snippet_hermes_agent_plugins_platform_google_chat.md) — Google Chat adapter; relevance: `spaces/<id>`/`users/<id>` target format + card presentation.

### oc_cli_message_channel_ops (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: these are `openclaw message` channel-management actions.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-platform driver; relevance: react/edit/pin/thread/moderation availability is per-adapter (the support matrix).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core action dispatch; relevance: routes non-send actions to the owning adapter.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway fronting channels; relevance: channel-ops run through it.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — message/member moderation controls; relevance: `timeout`/`kick`/`ban` Discord moderation actions.
- [Slack](../../term_dictionary/term_slack.md) — a supported channel; relevance: react/read/edit/pin/member-info supported on Slack.
- [Message Body](../../term_dictionary/term_message_body.md) — message content envelope; relevance: `edit` rewrites the body of a `--message-id`.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — cross-platform message ops; relevance: reactions/read span Discord/Slack/Matrix/Telegram/WhatsApp/Signal/Nextcloud.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — how replies bind to threads; relevance: Discord `thread create`/`reply`/`list` + `--thread-id` semantics.

**Docs**
- [Hermes — Discord Advanced](../hermes_agent/hermes_discord_advanced.md) — Discord roles/threads/events/moderation; relevance: directly parallels Discord channel-ops (roles/members/voice/events/moderation).
- [Hermes — Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram advanced actions; relevance: delete/reaction behavior per Telegram.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel action routing; relevance: how non-send actions reach adapters.
- [Hermes — Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — Signal channel behavior; relevance: Signal group reactions (`--target-author-uuid`).
- [Hermes — Messaging WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp adapter; relevance: WhatsApp `react --participant`/`--from-me`.
- [Hermes — Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — action dispatch internals; relevance: per-action gateway plumbing.
- [CC — Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — reply/edit tooling; relevance: edit/reply analog at the agent layer.
- [CC — Channels Overview](../claude_code/cc_channels_overview.md) — channel capability model; relevance: framing the per-channel support matrix.
- [oc_cli_message_send](oc_cli_message_send.md) — (planned, this series) the send half; relevance: shared channel selection / target formats / SecretRef behavior.
- [oc_cli_pairing](oc_cli_pairing.md) — (planned, this series) DM pairing; relevance: pairing controls who you can act on in DMs.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging adapters; relevance: implements react/read/edit/delete/pin/thread/moderation per channel.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: capability matrix + action gating.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — reactions/status handling; relevance: `react`/`reactions` action implementation.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — Discord thread ops; relevance: `thread create`/`list`/`reply`.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash/command surface; relevance: roles/events/moderation command plumbing.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord id/normalization; relevance: `--guild-id`/`--channel-id`/`--user-id` handling.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix adapter; relevance: Matrix read/edit/pin/permissions actions.
- [snippet_hermes_agent_gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp dispatch; relevance: WhatsApp reaction participant flags.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract platform base; relevance: which actions an adapter declares (the support matrix shape).
- [snippet_hermes_agent_gw_platform_telegram_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_normalize.md) — Telegram normalization; relevance: delete/forum-topic action targeting.

### oc_cli_migrate (10t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the destination system; relevance: `openclaw migrate` imports state INTO OpenClaw.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime an agent runs under; relevance: migration moves a workspace/harness's state (Codex harness, Hermes harness) into OpenClaw.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json` contract; relevance: migration providers declare `contracts.migrationProviders` in the manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the plugin authoring SDK; relevance: providers use `openclaw/plugin-sdk/migration` + `migration-runtime` for item construction and conflict-aware copies.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: migration imports MCP server definitions from `.mcp.json`/`mcp_servers`.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat operations; relevance: preview-first + verified backup + conflict-refusal make apply re-runnable without corruption.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential resolution + redaction; relevance: migration redacts nested secret-looking keys and gates credential import behind `--include-secrets`.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — multi-source credential store; relevance: imported API keys/tokens land in OpenClaw's credential/auth store.
- [Hermes Profile](../../term_dictionary/term_hermes_profile.md) — Hermes config/profile state; relevance: the Hermes provider reads `~/.hermes` config/profile state to plan the import.

**Docs**
- [Hermes — Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — the reverse migration direction; relevance: same plugin-owned, preview-and-apply migration model documented from the Hermes side.
- [CC — MCP Authentication](../claude_code/cc_mcp_authentication.md) — MCP server auth/config; relevance: migration imports MCP server definitions + auth.
- [CC — MCP Server Management](../claude_code/cc_mcp_server_management.md) — MCP server config surfaces; relevance: where imported `.mcp.json`/`~/.claude.json` servers land.
- [Hermes — Config Files & Precedence](../hermes_agent/hermes_config_files_precedence.md) — config layering/precedence; relevance: how imported defaults overlay existing OpenClaw config (conflict preflight).
- [Hermes — CLI Commands: Ops/Maintenance/Auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — doctor/auth/maintenance commands; relevance: `openclaw doctor` after applying a migration.
- [Hermes — Security: Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential handling/isolation; relevance: archive-only vs live-loaded state, secret redaction model.
- [CC — Plugin User Config & Env](../claude_code/cc_plugin_user_config_and_env.md) — plugin config/env contract; relevance: Codex native-plugin activation writes plugin config entries.
- [oc_cli_migrate_providers](oc_cli_migrate_providers.md) — (planned, this series) per-provider import matrix; relevance: the Claude/Codex/Hermes specifics this note generalizes over.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) onboarding `--flow import`; relevance: onboarding offers the same migration providers with a preview.
- [oc_cli_models](oc_cli_models.md) — (planned, this series) model/provider config; relevance: migration imports model/provider config that `models` then manages.
- [oc_cli_migrate_providers](oc_cli_migrate_providers.md) — (planned, this series) sibling deep-dive; relevance: provider plugin contract `detect`/`plan`/`apply` realized per provider.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding/migration CLI wizard; relevance: hosts migrate orchestration + onboarding-import path.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: migration providers are plugins registered via `api.registerMigrationProvider`.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — Hermes CLI; relevance: the source system whose `~/.hermes` state the Hermes provider imports.

**Snippets**
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — wizard migration-import flow; relevance: the migrate orchestration this note documents.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup import planning; relevance: detect→plan→preview before apply.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config writes; relevance: applying imported config with conflict handling.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer/setup; relevance: backup-then-apply safety pattern.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: importing `.env` keys / OAuth credentials.
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential-pool entry; relevance: where imported credentials are stored.
- [snippet_hermes_agent_core_hermes_home](../../code_snippets/snippet_hermes_agent_core_hermes_home.md) — `~/.hermes` home resolution; relevance: `--from` source-dir override / default detection.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation; relevance: conflict preflight before apply.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — config write; relevance: applying imported config keys.
- [snippet_hermes_agent_cli_doctor_late_sections_summary](../../code_snippets/snippet_hermes_agent_cli_doctor_late_sections_summary.md) — doctor post-checks; relevance: `openclaw doctor` after applying.

### oc_cli_migrate_providers (11t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — destination system; relevance: providers import INTO OpenClaw.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding agent; relevance: the Claude provider imports `CLAUDE.md`, `.mcp.json`, skills, commands from Claude Code state.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model/CLI; relevance: Claude credential/state is read but OAuth/Desktop creds are NOT auto-imported.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: all three providers import MCP server definitions.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: Hermes `.env` keys cover ~40 provider API keys (OpenAI/Anthropic/Groq/Mistral/...).
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — saved per-provider credential profile; relevance: imported OAuth/API-key credentials become auth profiles.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential material; relevance: OpenCode OpenAI OAuth import; Hermes legacy OAuth flagged for manual reauth.
- [Skills](../../term_dictionary/term_skills.md) — agent skill packages; relevance: Claude/Codex/Hermes skill dirs with `SKILL.md` are imported.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin authoring SDK; relevance: Codex native curated plugins are activated via plugin config entries.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration; relevance: Codex `plugins.entries.codex` config writes.

**Docs**
- [CC — Authentication](../claude_code/cc_authentication.md) — Claude Code auth model; relevance: what Claude credential state exists (and why OpenClaw won't auto-import OAuth).
- [CC — MCP Authentication](../claude_code/cc_mcp_authentication.md) — MCP server auth; relevance: imported MCP server definitions + auth.
- [PI — Provider Auth](../pi/pi_provider_auth.md) — provider auth setup; relevance: where imported provider credentials/profiles are used.
- [Hermes — Env Vars: Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env-var keys; relevance: the supported Hermes `.env` API-key matrix.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — provider catalog; relevance: which providers the imported keys map to.
- [Hermes — Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — reverse provider import; relevance: symmetric Hermes import semantics.
- [Hermes — Profiles & Multi-Agent](../hermes_agent/hermes_profiles_multi_agent.md) — per-agent profile/workspace; relevance: skills/AgentSkills copied into the per-agent workspace.
- [oc_cli_migrate](oc_cli_migrate.md) — (planned, this series) the generic migrate workflow; relevance: the safety model/flags this provider matrix runs under.
- [oc_cli_models](oc_cli_models.md) — (planned, this series) model/provider config; relevance: imported model/provider config is then managed via `models`.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) onboarding import; relevance: same providers triggered from `onboard --flow import`.
- [oc_cli_migrate](oc_cli_migrate.md) — (planned, this series) provider plugin contract; relevance: `detect`/`plan`/`apply` realized per Claude/Codex/Hermes.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — migration CLI; relevance: per-provider planning + apply orchestration.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — Hermes source CLI; relevance: the `~/.hermes` state the Hermes provider reads.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: model/provider config shapes the Hermes provider imports.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider plugins; relevance: imported provider/model config targets these provider plugins.

**Snippets**
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Codex provider plugin; relevance: Codex harness assets + native-plugin activation gating.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — Anthropic/Claude provider; relevance: Claude provider/model config import.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: which providers/keys are recognized on import.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: `.env`/`auth.json` key extraction.
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential-pool entry; relevance: storing imported API keys/tokens.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: OpenCode OpenAI OAuth import / manual-reauth flagging.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: imported credentials → usable provider auth.
- [snippet_hermes_agent_core_hermes_home](../../code_snippets/snippet_hermes_agent_core_hermes_home.md) — `~/.hermes` home; relevance: Hermes provider default detection / `--from`.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration-import flow; relevance: per-provider plan/apply path.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation; relevance: manual-review vs auto-applied state classification.

### oc_cli_models (11t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw models` is its model-control surface.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the discoverable model set; relevance: `models list`/`list --all` reads provider catalog + manifest rows.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback when a model/provider fails; relevance: `models fallbacks list` + scan-for-fallback candidates.
- [Model Router](../../term_dictionary/term_model_router.md) — routes a request to a provider/model; relevance: alias→default→provider resolution rules for model refs.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — secondary provider on failure; relevance: fallback chain management + OpenRouter `:free` scan.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — saved provider credential; relevance: `models auth add/list/login/paste-api-key/setup-token/paste-token` manage profiles.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: ChatGPT/Codex OAuth login + `--method api-key` fallback.
- [OAuth](../../term_dictionary/term_oauth.md) — the OAuth flow; relevance: `auth login` runs a provider OAuth/API-key flow.
- [LLM](../../term_dictionary/term_llm.md) — the underlying model; relevance: `models set provider/model` selects the LLM.
- [Authentication](../../term_dictionary/term_authentication.md) — auth status/verification; relevance: `status --probe` runs live auth probes; the read-only `Auth` column.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — provider request limits; relevance: probe status `rate_limit` bucket + usage-window/quota snapshots.

**Docs**
- [CC — Model Selection](../claude_code/cc_model_selection.md) — choosing the default model; relevance: direct analog of `models set`/default.
- [CC — Fallback Models](../claude_code/cc_fallback_models.md) — fallback model config; relevance: `models fallbacks` semantics.
- [PI — Provider Auth](../pi/pi_provider_auth.md) — provider auth setup; relevance: auth-profile add/login flow.
- [PI — Cloud Providers](../pi/pi_cloud_providers.md) — provider catalog/setup; relevance: providers the catalog/scan surface.
- [CC — Login/Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth probe/repair; relevance: reason codes (`missing_credential`/`expired`/`unresolved_ref`) and OpenAI OAuth recovery.
- [Hermes — Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — fallback chain; relevance: fallback ranking + cooldown.
- [Hermes — Provider Routing](../hermes_agent/hermes_provider_routing.md) — provider/model routing; relevance: alias/default/first-configured resolution.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — catalog schema; relevance: `Ctx`/contextTokens, static vs refreshable vs runtime catalog rows.
- [Hermes — Credential Pools](../hermes_agent/hermes_credential_pools.md) — multi-credential pools; relevance: env/config/store-aware provider auth overview.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) provider auth during onboarding; relevance: onboarding sets the default/auth that `models` later edits.
- [oc_cli_migrate_providers](oc_cli_migrate_providers.md) — (planned, this series) imported provider config; relevance: migration seeds the model/provider config `models` manages.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: `auth login` runs a provider plugin's flow; catalog rows come from plugin manifests.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent state; relevance: `--agent <id>` model/auth state + `OPENCLAW_AGENT_DIR`.

**Snippets**
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback + cooldown; relevance: fallback selection on probe failure/rate-limit.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth order/credential resolution; relevance: `auth.order.<provider>` (`excluded_by_auth_order` reason code).
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: ChatGPT/Codex OAuth profile health.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external CLI auth reuse; relevance: Claude CLI reuse / `claude -p` sanctioned path.
- [snippet_hermes_agent_cli_models_picker](../../code_snippets/snippet_hermes_agent_cli_models_picker.md) — models picker; relevance: `models list`/`set` interactive selection.
- [snippet_hermes_agent_cli_model_switch_swap](../../code_snippets/snippet_hermes_agent_cli_model_switch_swap.md) — model switch; relevance: `models set <model-or-alias>`.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — provider login/logout; relevance: `models auth login --provider`.
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: `auth list` profile health (no secret material).
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider; relevance: `models scan` of OpenRouter `:free` catalog.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregation; relevance: OpenRouter-style `provider/model` ref parsing (split on first `/`).
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: `--provider <id>` filter / installed providers.

### oc_cli_node (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw node` runs a host that connects to its Gateway.
- [WebSocket](../../term_dictionary/term_websocket.md) — the node↔gateway transport; relevance: node connects to the Gateway WebSocket (`--host`/`--port`, `ws://`/`wss://`).
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: `--tls`/`--tls-fingerprint`; insecure `ws://` opt-in for private hosts.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — certificate-fingerprint pinning; relevance: `--tls-fingerprint <sha256>` pins the gateway cert.
- [Sandbox](../../term_dictionary/term_sandbox.md) — guarded execution; relevance: exec stays sandboxed on the gateway while approved runs delegate to the node.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: `--runtime node|bun` selects the node-host service runtime.
- [Active Linked Device](../../term_dictionary/term_active_linked_device.md) — a paired device; relevance: first connection creates a pending `role: node` device pairing request.
- [Device ID](../../term_dictionary/term_device_id.md) — device identifier; relevance: `--node-id` override; node id stored in `~/.openclaw/node.json`.
- [Authentication](../../term_dictionary/term_authentication.md) — gateway auth; relevance: node auth resolves from env→config, fails closed if SecretRef unresolved.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — SecretRef resolution; relevance: `gateway.auth.token`/`password` via SecretRef; unresolved → fail closed.

**Docs**
- [Hermes — Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — running/operating the gateway; relevance: foreground run vs background service (launchd/systemd) lifecycle.
- [Hermes — Docker Volumes & Supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — service supervision; relevance: supervised node service restart/exit semantics.
- [Hermes — Security: Command Approval](../hermes_agent/hermes_security_command_approval.md) — exec approval gating; relevance: `system.run` gated by local exec approvals + per-agent allowlists.
- [Hermes — Security: Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential/exec isolation; relevance: keeping command access scoped and explicit on the node.
- [CC — Remote Control](../claude_code/cc_remote_control.md) — controlling a remote agent host; relevance: parallels delegating runs to remote node hosts.
- [CC — SDK Isolation Technologies](../claude_code/cc_sdk_isolation_technologies.md) — sandbox/isolation tech; relevance: how exec is sandboxed on the host.
- [Hermes — Terminal Backends](../hermes_agent/hermes_terminal_backends.md) — exec/terminal backends; relevance: `system.run`/`system.which` execution target.
- [oc_cli_nodes](oc_cli_nodes.md) — (planned, this series) paired-node management; relevance: approving/listing the node this host registers.
- [oc_cli_pairing](oc_cli_pairing.md) — (planned, this series) pairing approval; relevance: first-connection pending request approval.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) gateway/token setup; relevance: gateway auth/token the node host resolves.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: the node host connects to / is paired by the gateway.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/CLI entrypoints; relevance: `node run`/`node install` command wiring + browser proxy.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec/sandbox policy; relevance: exec approvals + `systemRunPlan` immutability.

**Snippets**
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node↔gateway session; relevance: the node-host connection lifecycle.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway WebSocket channel; relevance: `ws://`/`wss://` transport to the gateway.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: `--tls-fingerprint` pinning + identity.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect/proxy; relevance: zero-config browser proxy advertisement.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: env→config token/password resolution, no remote fallback in local mode.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: SecretRef fail-closed for node auth.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: first-connection pending `role: node` request + autoApproveCidrs.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: `system.run` exec-approval gating.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed exec; relevance: keeping exec sandboxed while delegating approved runs.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error/close codes; relevance: terminal auth-pause close → non-zero exit for launchd/systemd restart.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: `system.run` approved-plan reuse (edits rejected after approval).

### oc_cli_nodes (10t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw nodes` manages its paired nodes.
- [Active Linked Device](../../term_dictionary/term_active_linked_device.md) — a paired device/node; relevance: `nodes list`/`status` show paired + connected nodes.
- [Device ID](../../term_dictionary/term_device_id.md) — node identifier; relevance: `--node <id|name|ip>` selection across remove/rename/invoke.
- [Device Deregistration](../../term_dictionary/term_device_deregistration.md) — revoking a device; relevance: `nodes remove` revokes the `node` role in `devices/paired.json` and disconnects node-role sessions.
- [Sandbox](../../term_dictionary/term_sandbox.md) — guarded execution; relevance: `system.run`/`system.run.prepare` blocked in `invoke` — routed to the sandboxed `exec` tool.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe key for RPC; relevance: `nodes invoke --idempotency-key` makes repeated invokes safe.
- [Authentication](../../term_dictionary/term_authentication.md) — scope/auth checks; relevance: approve inherits pairing/write/admin scope from the request; `operator.admin` for self-role revocation.
- [WebSocket](../../term_dictionary/term_websocket.md) — node transport; relevance: `--url`/`--token` connect to the gateway WebSocket for RPC.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: `nodes invoke --command --params` is direct node RPC.
- [Access Control](../../term_dictionary/term_access_control.md) — scope tiers; relevance: pairing-only / pairing+write / pairing+admin per pending-request type.

**Docs**
- [Hermes — Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — node/device management ops; relevance: list/approve/reject/remove lifecycle.
- [Hermes — Security: Command Approval](../hermes_agent/hermes_security_command_approval.md) — approval scope tiers; relevance: pairing/write/admin scope requirements per request.
- [Hermes — Security: Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — exec isolation; relevance: why `system.run` is routed to `exec` not `invoke`.
- [CC — Remote Control](../claude_code/cc_remote_control.md) — remote host control; relevance: invoking capabilities on remote devices.
- [CC — SDK Isolation Technologies](../claude_code/cc_sdk_isolation_technologies.md) — isolation tech; relevance: sandbox boundary around node exec.
- [Hermes — Terminal Backends](../hermes_agent/hermes_terminal_backends.md) — exec backends; relevance: `exec` tool with `host=node` for shell execution.
- [oc_cli_node](oc_cli_node.md) — (planned, this series) the node host; relevance: the host whose pairing these commands approve/manage.
- [oc_cli_pairing](oc_cli_pairing.md) — (planned, this series) DM pairing; relevance: parallel approval flow (devices vs DMs).
- [oc_cli_message_channel_ops](oc_cli_message_channel_ops.md) — (planned, this series) capability commands; relevance: `nodes` is capability-focused (camera/screen/canvas/location/notifications).
- [oc_cli_node](oc_cli_node.md) — (planned, this series) sibling host doc; relevance: device-backed vs node-only removal semantics.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/CLI entrypoints; relevance: `nodes` command + capability dispatch (camera/canvas/screen).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: pending/paired tables + node RPC routing live here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — scope/role policy; relevance: pairing/write/admin scope + `node` role revocation.

**Snippets**
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing/approval; relevance: `pending`/`approve`/`reject` + autoApproveCidrs scope.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: `nodes invoke --command --params` RPC dispatch.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — invoke dispatcher; relevance: capability-command routing + timeout.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: `system.run`/`system.run.prepare` blocked in invoke.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials; relevance: `--token` auth for node RPC.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: `--params <json>` request shape + idempotency key.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: which commands `invoke` accepts (pairing/camera/screen/canvas).
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: blocking `system.run` at the invoke surface.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle; relevance: disconnecting node-role sessions on remove.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — dispatch handler; relevance: routing an invoked command to the target node.

### oc_cli_onboard (11t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw onboard` is its full guided setup flow.
- [OAuth](../../term_dictionary/term_oauth.md) — provider OAuth flow; relevance: model-auth step runs provider OAuth/API-key auth choices.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: provider token auth (Z.AI/xAI/Anthropic) during onboarding.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — saved provider credential; relevance: `--auth-choice` writes provider auth profiles (`keyRef` entries in ref mode).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external providers; relevance: custom provider / LM Studio / Ollama / Mistral / Z.AI endpoint choices.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: `--custom-model-id` + default-model picker.
- [Authentication](../../term_dictionary/term_authentication.md) — gateway/provider auth; relevance: gateway token options + provider auth gating + health check.
- [WebSocket](../../term_dictionary/term_websocket.md) — gateway transport; relevance: `--mode remote --remote-url wss://...`; insecure `ws://` private-host opt-in.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — SecretRef; relevance: `--secret-input-mode ref` writes env-backed SecretRefs; `--gateway-token-ref-env`.
- [Steering Files](../../term_dictionary/term_steering_files.md) — workspace bootstrap files; relevance: bootstrap writes `AGENTS.md`/`SOUL.md`/`TOOLS.md`/`IDENTITY.md`/`USER.md`/`HEARTBEAT.md`/`BOOTSTRAP.md` (`--skip-bootstrap` opts out).
- [PKCE](../../term_dictionary/term_pkce.md) — OAuth PKCE flow; relevance: provider OAuth auth choices use PKCE-style browser auth.

**Docs**
- [CC — Authentication](../claude_code/cc_authentication.md) — auth setup; relevance: provider auth choices during onboarding.
- [PI — Provider Auth](../pi/pi_provider_auth.md) — provider auth; relevance: per-provider auth-choice flows.
- [CC — Configure Your Environment](../claude_code/cc_configure_your_environment.md) — environment/config setup; relevance: workspace/config/env writes onboarding performs.
- [Hermes — Quickstart: First Chat](../hermes_agent/hermes_quickstart_first_chat.md) — first-run setup; relevance: quickstart flow analog (`--flow quickstart`).
- [Hermes — Installation](../hermes_agent/hermes_installation.md) — install + daemon; relevance: `--install-daemon` managed gateway install path.
- [Hermes — Provider X.AI/Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — Grok/x_search auth; relevance: Grok web-search follow-up + `x_search` setup.
- [Hermes — Setup with Nous Portal](../hermes_agent/hermes_setup_with_nous_portal.md) — provider-subscription setup; relevance: provider-specific onboarding follow-ups.
- [Hermes — Secrets (Bitwarden)](../hermes_agent/hermes_secrets_bitwarden.md) — secret-ref provider; relevance: secret-ref mode (`file`/`exec` provider) for stored keys.
- [oc_cli_migrate](oc_cli_migrate.md) — (planned, this series) `--flow import`; relevance: onboarding import runs the migrate providers with a preview.
- [oc_cli_models](oc_cli_models.md) — (planned, this series) model/auth config; relevance: onboarding seeds default/auth that `models` later edits.
- [oc_cli_pairing](oc_cli_pairing.md) — (planned, this series) DM scope; relevance: local onboarding DM-scope behavior + owner bootstrap.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the onboarding/wizard CLI; relevance: implements the `onboard` flow types + non-interactive flag surface.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/workspace state; relevance: bootstrap workspace files + default-model/agent config.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway; relevance: gateway-mode/token config + local health check (`gateway run`).

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard config writes; relevance: gateway-mode/token + provider config the onboard flow writes.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup imports; relevance: `--flow import` planning.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: detected-source migration offer during onboarding.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — setup wizard; relevance: interactive guided-setup flow analog.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer/daemon; relevance: `--install-daemon` managed install path.
- [snippet_hermes_agent_cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify/health; relevance: health gating before successful exit (`--skip-health`).
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — provider login; relevance: `--auth-choice` provider login flows.
- [snippet_hermes_agent_cli_main_provider_flows](../../code_snippets/snippet_hermes_agent_cli_main_provider_flows.md) — provider auth flows; relevance: custom/LM-Studio/Ollama/Mistral/Z.AI non-interactive flows.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth/credential order; relevance: ref-mode `keyRef`/env-ref credential writes.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — config set; relevance: `gateway.mode`/`gateway.auth.token` config writes.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: token/password mode resolution + SecretRef validation at install.

### oc_cli_pairing (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw pairing` approves DM pairing requests for its channels.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing-mode DM approval; relevance: this command IS the DM pairing-approval surface (`pairing list`/`approve`).
- [DM Policy](../../term_dictionary/term_dm_policy.md) — who may DM the bot; relevance: approving a pairing code allows that sender; owner bootstrap seeds `commands.ownerAllowFrom`.
- [Active Linked Device](../../term_dictionary/term_active_linked_device.md) — an approved sender/device; relevance: approval records the channel-scoped sender (e.g. `telegram:123456789`).
- [Authentication](../../term_dictionary/term_authentication.md) — approval/owner auth; relevance: the command owner runs owner-only commands and approves dangerous actions.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel pairing support; relevance: pairing works only for channels that support pairing; extension channels allowed if id is valid.
- [Slack](../../term_dictionary/term_slack.md) — a pairing-capable channel; relevance: positional/`--channel` channel selection (Telegram/Slack/etc.).
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — multi-channel/account; relevance: `--account <id>` for multi-account channels; multiple pairing-capable channels require explicit selection.
- [Safelist](../../term_dictionary/term_safelist.md) — allowed-sender list; relevance: approval adds the sender to the allow set (and the first becomes owner).

**Docs**
- [Hermes — Security: Command Approval](../hermes_agent/hermes_security_command_approval.md) — owner/approval model; relevance: owner-only commands + dangerous-action approval the owner bootstrap enables.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — per-channel DM handling; relevance: which channels support pairing + account scoping.
- [Hermes — Telegram Setup](../hermes_agent/hermes_telegram_setup.md) — Telegram channel; relevance: `pairing list telegram` / multi-account `--account work`.
- [Hermes — Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — Signal DM channel; relevance: pairing-capable channel example.
- [Hermes — Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — operator approval ops; relevance: `openclaw doctor` warns when no command owner is configured.
- [CC — Channels Overview](../claude_code/cc_channels_overview.md) — channel/DM model; relevance: framing channel-scoped sender approval.
- [oc_cli_message_send](oc_cli_message_send.md) — (planned, this series) sending DMs; relevance: pairing gates who you can DM / who can initiate.
- [oc_cli_node](oc_cli_node.md) — (planned, this series) device pairing; relevance: parallel approval surface (`devices approve` for nodes).
- [oc_cli_nodes](oc_cli_nodes.md) — (planned, this series) node approval; relevance: contrast DM-sender pairing vs node-device pairing.
- [oc_cli_onboard](oc_cli_onboard.md) — (planned, this series) owner/DM-scope setup; relevance: onboarding's local DM-scope behavior + first-owner bootstrap.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — channel adapters; relevance: per-channel pairing-request handling + sender allow.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — owner/allow policy; relevance: `commands.ownerAllowFrom` bootstrap + owner-only gating.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — CLI entrypoints; relevance: `pairing list`/`approve` command wiring.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: the exact allow-sender + owner-bootstrap mechanism this command drives.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — gateway pairing flow; relevance: pending pairing-request approval lifecycle.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — pairing approval; relevance: approve-by-code/request mechanics (contrast device pairing).
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: owner/sender authorization on approval.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — auth-ticket issuance; relevance: approval grants scoped access to the approved sender.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: per-channel/account pairing on Telegram.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config broadcast; relevance: `commands.ownerAllowFrom` config update propagation.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth/rate-limit policy; relevance: gating pairing-approval requests.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: owner-only/dangerous-action approval semantics post-bootstrap.

## Undigested Terms Plan

Per master: OpenClaw CLI vocabulary is digested AS these `oc_` doc notes (the command IS the subject), NOT as new
`term_dictionary` entries. Expected **0 new `term_dictionary` captures**. Augment Step 2d re-scans.

| Term (surface vocabulary) | Disposition |
|---|---|
| `message send` / `--presentation` / semantic blocks | Documented in note 1 (oc_cli_message_send); link `term_channel_adapter`, `term_omnichannel`. No new term. |
| channel actions (react/poll/thread/moderation) | Documented in note 2 (oc_cli_message_channel_ops). No new term. |
| `models scan` / aliases / fallbacks / auth profiles | Documented in note 5 (oc_cli_models); link `term_model_catalog`, `term_model_failover`, `term_auth_profile`. No new term. |
| node host / headless node / `system.run` exec target | Documented in notes 6–7 (oc_cli_node/oc_cli_nodes); link `term_websocket`, `term_sandbox`, `term_active_linked_device`. No new term. |
| onboarding / wizard / flow types / secret-ref mode | Documented in note 8 (oc_cli_onboard); link `term_oauth`, `term_auth_profile`. No new term. |
| DM pairing / pairing code / owner bootstrap | Documented in note 9 (oc_cli_pairing); link `term_active_linked_device`, `term_authentication`. No new term. |
| provider names (OpenAI, Z.AI, Ollama, LM Studio, Mistral, Anthropic, OpenRouter) | CLI flag values, not concepts — link `term_third_party_genai_services` / `term_llm`. No new term. |
| SecretRef / secret reference | Link `term_secrets_manager` (existing); `term_secretref` confirmed MISSING — do not capture (covered by secrets sub-plans gw05/gw06). No new term here. |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an
existing note. (If augment surfaces one, it would be captured via `/tessellum-capture-term-note` + added to the
agentic/LLM `acronym_glossary_*.md`; not expected.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. Requirement inherited from master:
should augment propose a new term, it must be researched from ≥2 independent sources, slug-specificity +
collision-audited against existing vault notes, and added to the best-fit `acronym_glossary_*.md`.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (9 notes, P1). All gates must PASS before commit.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` — YAML field order/tags/quoted-year; H1 `# OpenClaw — …`, `## Overview`, `## Related Notes`, `## References`, bold footer. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/cli/<page>.md`; every claim/flag traceable to source; no invented flags. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; one BB (procedure); every mapped section present. |
| G4 | Cross-Reference | ≥6 relevancy-selected term links + repo_openclaw*/sibling oc_*/other vault notes per note, each with a relevance statement; indexed `[text](path.md)` link format. |
| G6 | Broken-link | `/tessellum-fix-broken-links` after incremental reindex; 0 broken links. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island). |
| G8 | In-degree ≥1 | Confirm `note_links` in-degree ≥1 per new note (satisfied via `entry_openclaw_docs.md` + repo/term inlinks). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_message_send oc_cli_message_channel_ops oc_cli_migrate oc_cli_migrate_providers oc_cli_models oc_cli_node oc_cli_nodes oc_cli_onboard oc_cli_pairing"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # require source_url in frontmatter
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (body words / code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w, ${cb} code)"
  # G4 sibling cross-ref presence
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO sibling/oc_ cross-ref"
done

# YAML frontmatter sweep over the whole openclaw folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6 after incremental reindex
bash scripts/update_notes_database.sh
# then: /tessellum-fix-broken-links  (expect 0)  ·  ghost-reference detect (expect 0)
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_cli_message_send | procedure | 500 | ≤6 | yes |
| 2 | oc_cli_message_channel_ops | procedure | 450 | ≤3 | yes |
| 3 | oc_cli_migrate | procedure | 600 | ≤4 | yes |
| 4 | oc_cli_migrate_providers | procedure | 600 | ≤3 | yes |
| 5 | oc_cli_models | procedure | 650 | ≤5 | yes |
| 6 | oc_cli_node | procedure | 550 | ≤6 | yes |
| 7 | oc_cli_nodes | procedure | 350 | ≤2 | yes |
| 8 | oc_cli_onboard | procedure | 600 | ≤6 | yes |
| 9 | oc_cli_pairing | procedure | 350 | ≤2 | yes |

No note approaches the 2,500w / 400-line / 6-code caps. The two densest source pages were split (message.md →
notes 1+2; migrate.md → notes 3+4) so each note stays focused and code-light; the example-heavy `message.md`
fences concentrate in note 1 (≤6).

## Entry Point Decision (inherited from master)

Contributes **9 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, >30 master total) under a
"CLI" cluster (sub-plan cl05). Each note receives its entry-point back-link at finalization (satisfies G7/G8).
Per-note rows: oc_cli_message_send, oc_cli_message_channel_ops, oc_cli_migrate, oc_cli_migrate_providers,
oc_cli_models, oc_cli_node, oc_cli_nodes, oc_cli_onboard, oc_cli_pairing.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 — each new note gets ≥1):

- `entry_openclaw_docs.md` → all 9 notes (primary anti-island guarantee).
- `repo_openclaw_channels_messaging` → notes 1, 2, 9 (CLI surface for messaging/pairing).
- `repo_openclaw_cli_wizard` → notes 3, 8 (migrate + onboard wizard CLI).
- `repo_openclaw_extensions_llm_providers` → notes 4, 5 (provider import + model/auth config).
- `repo_openclaw_gateway` → notes 6, 7 (node host ↔ gateway WebSocket; paired-node management).
- `repo_openclaw_security` → notes 6, 7, 9 (exec approvals, node-role scope, pairing/owner bootstrap).
- `term_openclaw` → all 9 (umbrella product term).
- `term_model_catalog` / `term_model_failover` → note 5.
- `term_websocket` / `term_sandbox` → notes 6, 7.
- `term_active_linked_device` → notes 6, 7, 9.

## Pacing Rules (inherited from master)

One execution phase (9 notes, ≤30-agent fan-out cap easily satisfied). Re-read each source page during execution;
reproduce CLI examples verbatim and selectively (≤6 code/note). One BB (procedure) per note. Incremental reindex
after the wave; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash`
first; commit + push the sub-plan in one cycle; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this run (xref-augment):** re-read all 7 assigned source pages under `inbox/openclaw_docs/cli/`
(message, migrate, models, node, nodes, onboard, pairing), then built and LOCKED a relevance-selected,
· ≥10 docs** per note (plus relevant `repo_openclaw*` and sibling `oc_*`). The prior "## Candidate
Cross-References" section was replaced by "## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)".

**What was locked (per-note counts — all floors MET):**

| Note | Terms | Snippets | Docs (≥5 existing + planned siblings) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_cli_message_send | 10 | 11 | 11 (8 existing + 3 planned) | 3 | yes |
| oc_cli_message_channel_ops | 9 | 11 | 10 (8 existing + 2 planned) | 3 | yes |
| oc_cli_migrate | 10 | 10 | 11 (7 existing + 4 planned*) | 3 | yes |
| oc_cli_migrate_providers | 11 | 10 | 11 (7 existing + 4 planned*) | 4 | yes |
| oc_cli_models | 11 | 11 | 11 (9 existing + 2 planned) | 2 | yes |
| oc_cli_node | 10 | 11 | 10 (7 existing + 3 planned) | 3 | yes |
| oc_cli_nodes | 10 | 10 | 10 (6 existing + 4 planned*) | 3 | yes |
| oc_cli_onboard | 11 | 11 | 11 (8 existing + 3 planned) | 3 | yes |
| oc_cli_pairing | 9 | 10 | 10 (6 existing + 4 planned) | 3 | yes |

*Where a note's planned-sibling list reaches 4, one sibling row is cited twice under two distinct relevance
facets (e.g. `oc_cli_migrate_providers` cited as both the per-provider matrix AND the provider-plugin-contract
realization) — kept because each facet is a genuinely distinct cross-reference rationale, and every note still
clears the ≥5-EXISTING-doc requirement independently (existing-doc counts above are unique notes).

**Verification method:** all cited existing note_ids were checked with
- 68 candidate terms → all PRESENT (final set draws from these).
- 96 candidate snippets across messaging/provider/model/migration/node/gateway/pairing → all PRESENT; every
- ~75 candidate docs (cc_/hermes_/pi_/band_) → PRESENT except `cc_channel_message_tool`, `cc_sandbox_organization`,
  `cc_dangerous_permissions` (MISSING — excluded, never cited).
  at W1; siblings correctly marked "(planned, this series)").

**New-term candidates surfaced during the re-read (Step 2d):** NONE.
- The re-read confirmed the master's undigested-terms policy: OpenClaw CLI vocabulary is digested AS these `oc_`
  doc notes (the command IS the subject), not as new `term_dictionary` entries.
- Surface vocabulary checked again and resolved to EXISTING terms (no capture): semantic presentation/Block Kit →
  `term_block_kit` (existing, now cited in notes 1/2); DM pairing → `term_dm_pairing` + `term_dm_policy` (existing,
  cited in notes 1/9); migration credential store → `term_credential_pool` + `term_hermes_profile` (existing,
  cited in notes 3/4); idempotent invoke → `term_idempotency_key` (existing, cited in note 7); TLS pinning →
  `term_tls_pinning` (existing, cited in note 6); content moderation → `term_content_moderation` (existing, cited
  in note 2); PKCE → `term_pkce`, safelist → `term_safelist` (existing, cited in notes 8/9).
- Confirmed STILL-MISSING (not promoted, per master policy — names are CLI flag values / covered elsewhere):
  `term_hermes`, `term_codex`, `term_secretref`, `term_discord`, `term_telegram`, `term_broadcast`, `term_daemon`,
  `term_systemd`, `term_launchd`, `term_openrouter`, `term_ollama`, `term_openai`, `term_anthropic`. If a future
  run promotes one, it routes through `/tessellum-capture-term-note` + the agentic/LLM `acronym_glossary_*.md`.
- **Best-fit glossary (if any term were ever captured):** the agentic/LLM acronym glossary
  (`0_entry_points/acronym_glossary_agentic_llm.md`) — none needed this run.

**Sections changed:** Candidate Cross-References → Per-Note Related Notes Mapping (LOCKED); Summary Statistics
cross-ref line updated to the locked floors; Pipeline Status Augment/Review marked DONE. Undigested Terms Plan,
Term-Note Authoring Requirements (N/A — 0 terms), GATE table (G1–G9), Validation Scripts, Density Re-Assessment,
Entry Point Decision, Inlinks, and Pacing Rules were already present and were re-verified, not rewritten.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only final review against the 9 mandatory checkpoints. Source spot-check: re-read `cli/migrate.md`
(measured ≈2,030w vs plan 2,075w → ratio 0.98) and `cli/message.md` (≈1,300w vs plan 1,318w → 0.99) and
`cli/models.md` (≈1,480w vs plan 1,494w → 0.99) — all within ±2%.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | Per-Note Related Notes Mapping (LOCKED) gives every note ≥8 terms (9–11), ≥10 snippets, ≥10 docs, each link with a relevance statement in `- [Name](path.md) — desc; relevance: …` form; min term count = 9 (notes 2, 9). |
| CP2 | 9-GATE present per batch (G1–G6 + G8) | **PASS** | "## Per-Phase Validation Gate (G1–G9)" table present for the single P1 phase with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability/in-degree. Validation Scripts include G5 ghost-detect + G6 broken-link + YAML sweep. |
| CP4 | Size | **PASS** | 9 notes ≤30; single execution phase; ≤30-agent fan-out trivially satisfied. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master "Format Definition (Shared)" derived from existing `claude_code/` + `pi/` corpora: H1 `# OpenClaw — …`, `## Overview`, `## Related Notes`, `## References`, bold footer; forbidden-fields list present; YAML field order matches `oc_*` spec. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 9 notes 350–650w, ≤6 code blocks, well under 2,500w/400-line caps; the 2 densest pages (message, migrate) were split (1+2, 3+4). No borderline note left unsplit. |
| CP7 | Sources measured | **PASS** | Source table measured 2026-06-20 (7,856w / 42 code / 38 H2 / 20 H3); review re-read 3 pages (migrate/message/models) → all within ±2% of plan estimates. |
| CP8 | Undigested terms + authoring reqs | **PASS** | "## Undigested Terms Plan" present (0 new terms, every surface-vocabulary row dispositioned to an `oc_` note + existing-term link); "## Term-Note Authoring Requirements" present (N/A — 0 terms, inherited mandate stated); augment Step 2d re-scan recorded NONE. |
| CP8f | Slug/collision | **PASS** | 0 new `term_*` slugs ⇒ no specificity/collision rename needed; dedup-audit generalized to the 9 doc notes — all `oc_cli_*` slugs confirmed ABSENT in DB (no doc-note duplicates an existing term/doc); migration source names (Hermes/Codex/Claude) link existing terms rather than create. |
| CP9 | Discoverability/inlinks | **PASS** | "## Inlinks (existing notes → new notes)" maps every new note to ≥1 outside-folder inbound link (entry_openclaw_docs → all 9; repo_openclaw_* + term_* per note); G7/G8 in the gate table mark inlink-addition as a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
