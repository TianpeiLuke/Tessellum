---
title: Sub-Plan pl23 — OpenClaw Docs: Plugins (zai/zalo/zalouser reference + SDK agent-harness & channel APIs)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/zai", "plugins/reference/zalo", "plugins/reference/zalouser", "plugins/sdk-agent-harness", "plugins/sdk-channel-inbound", "plugins/sdk-channel-ingress", "plugins/sdk-channel-outbound"]
---

# Sub-Plan pl23: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + body + density caps), dedup
> (3-way across term_dictionary / documentation / `repo_openclaw*`), undigested-terms policy, 9-GATE, cross-ref
> floors, and entry-point wiring are ALL inherited from the master and not restated here.

## Scope

The tail of the Plugins section: the three smallest **plugin-reference manifest stubs** (`zai`, `zalo`,
`zalouser` — each ~60 words: package + surface + related-doc pointer) plus the four **plugin SDK pages** that
define the extension contracts plugins implement — the experimental **agent-harness** surface (the low-level
turn executor that lets a model family bring its own native session runtime, e.g. the bundled Codex harness)
and the three **channel pipeline** SDK subpaths (**inbound** receive/context/dispatch orchestration,
**ingress** inbound access-control/authorization, **outbound** send/receipt/durable-delivery). Priority **P3**
(Phase C — plugin reference sprawl); these SDK pages are the most reusable of pl23 because they document the
contracts every channel/harness plugin in pl01–pl25 implements. The code-side counterparts
(`repo_openclaw_channels`, `repo_openclaw_agents`, `repo_openclaw_extensions`, the `snippet_openclaw_channels_*`
+ `snippet_openclaw_plugin_*` snippets) are LINKED, never recreated.

**Source**: OpenClaw docs, 7 pages, 3,285 measured words (3 micro-stubs = 176w; 4 SDK pages = 3,109w). **Planned: 5 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Z.AI plugin | plugins/reference/zai | 56 | 0 | 3 | 0 | model (reference) |
| Zalo plugin | plugins/reference/zalo | 57 | 0 | 3 | 0 | model (reference) |
| Zalo Personal plugin | plugins/reference/zalouser | 63 | 0 | 3 | 0 | model (reference) |
| Agent harness plugins | plugins/sdk-agent-harness | 1,794 | 5 | 10 | 4 | concept |
| Channel inbound API | plugins/sdk-channel-inbound | 292 | 3 | 2 | 0 | procedure |
| Channel ingress API | plugins/sdk-channel-ingress | 598 | 3 | 7 | 0 | procedure |
| Channel outbound API | plugins/sdk-channel-outbound | 425 | 2 | 4 | 0 | procedure |

> Code counts are `grep -c '```' / 2` (raw fence counts halved): zai/zalo/zalouser 0; sdk-agent-harness
> 10/2=5; sdk-channel-inbound 6/2=3; sdk-channel-ingress 6/2=3; sdk-channel-outbound 4/2=2.

## Content Strategy

- **Prioritize**: the SDK contract pages. `sdk-agent-harness` is the conceptual centrepiece (when/why a harness,
  the host-vs-harness ownership split, the `runtimePlan` policy bundle, selection policy, Codex pairing, runtime
  strictness, transcript mirror) — the doc that the whole Codex/native-runtime story in pl02 (`codex-harness*`)
  references. The three channel pages define the receive→reply→send contract every channel plugin (pl01–pl25
  + ch01–ch06) implements.
- **Consolidate (anti-thin-note)**: `zai`, `zalo`, `zalouser` are ~60-word manifest stubs (Distribution / Surface
  / Related docs only). Each alone is far below any usable note density floor and carries no procedure/concept of
  its own — they are pointers into `/providers/zai` and `/channels/zalo` (whose substantive content is digested
  by `pr09` and `ch06`). The three are merged into ONE plugin-manifest reference note (model BB: a small
  package→surface→target table). This mirrors the master's "Most reference pages = 1 note" intent while honoring
  the density floor; the manifest table preserves every fact from all three pages losslessly.
- **No split**: `sdk-agent-harness` (1,794w) is under the 2,500w cap and is a single dominant concept (the harness
  contract); its "Register a harness" / "Runtime strictness" code is illustrative, not a separable procedure note.
  Keep as 1 concept note. The three channel pages are each well under cap → 1 procedure note each.
- **Link-out (do NOT redefine)**: provider/channel substance for zai/zalo/zalouser → `pr09`/`ch06` (planned);
  the Codex harness operator setup → `plugins/codex-harness` (pl02, planned); SDK overview/runtime/entrypoints/
  provider-plugins → pl24 (`sdk-overview`, `sdk-runtime`, `sdk-entrypoints`, `sdk-provider-plugins`, planned);
  `concepts/agent-runtimes` + `concepts/model-providers` → co01/co04 (planned). Terms `term_agent_harness`,
  `term_provider_plugin`, `term_plugin_sdk`, `term_channel_adapter`, `term_channel_kernel`, `term_access_control`,
  `term_codex` (n/a — absent; use `term_claude`/`term_autonomous_coding_agents`) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugin_reference_zai_zalo_zalouser.md` | model | reference/zai.md + reference/zalo.md + reference/zalouser.md (all H2: Distribution, Surface, Related docs) | 320 | Plugin-manifest reference for three OpenClaw plugins — Z.AI model provider (`@openclaw/zai-provider`), Zalo bot/webhook channel (`@openclaw/zalo`), Zalo Personal channel via zca-js (`@openclaw/zalouser`): package, install route, declared surface (providers/channels/contracts), and pointers to their provider/channel docs. |
| 2 | `oc_sdk_agent_harness.md` | concept | sdk-agent-harness.md: When to use a harness, What core still owns (`runtimePlan`), Register a harness, Selection policy, Provider+harness pairing (Codex), Runtime strictness, Native sessions & transcript mirror, Tool/media results, Current limitations | 700 | The experimental agent-harness SDK surface: the low-level executor for one prepared agent turn that lets a native model runtime (e.g. Codex) own threads/compaction while core keeps provider/model resolution, auth, transcript, sandbox, tool policy, and channel delivery — covering the host-vs-harness ownership split, the `runtimePlan` policy bundle, harness registration, selection policy, Codex provider pairing, runtime strictness, and the transcript-mirror contract. |
| 3 | `oc_sdk_channel_inbound.md` | procedure | sdk-channel-inbound.md: (intro receive-path model), Core Helpers, Migration | 380 | The channel inbound SDK API (`openclaw/plugin-sdk/channel-inbound`): how a channel plugin models its receive path (platform event → inbound context → agent reply → message delivery) via `buildChannelInboundEventContext`, `runChannelInboundEvent`, and `dispatchChannelInboundReply` (and their `runtime.channel.inbound.*` aliases), plus migration off the removed `runtime.channel.turn.*` helpers. |
| 4 | `oc_sdk_channel_ingress.md` | procedure | sdk-channel-ingress.md: (intro), Runtime Resolver, Result, Access Groups, Event Modes, Routes And Activation, Redaction, Verification | 520 | The experimental channel ingress SDK API (`openclaw/plugin-sdk/channel-ingress-runtime`): the access-control boundary for inbound events — `resolveChannelMessageIngress`/`defineStableChannelIngressIdentity`, the ordered gate result projections (ingress/senderAccess/routeAccess/commandAccess/activationAccess), access groups, the five `authMode` event modes, route descriptors + mention activation, and the input-only redaction rule for raw sender/allowlist values. |
| 5 | `oc_sdk_channel_outbound.md` | procedure | sdk-channel-outbound.md: (intro), Adapter, Existing Outbound Adapters, Durable Sends, Compatibility Dispatch | 420 | The channel outbound SDK API (`openclaw/plugin-sdk/channel-outbound`): defining a `message` adapter (`defineChannelMessageAdapter` + `createMessageReceiptFromOutboundResults`), deriving one from an existing outbound adapter, durable send helpers (`sendDurableMessageBatch` and its sent/suppressed/partial_failed/failed outcomes), and the core-vs-plugin ownership split for send/receipt/durability. |

## Section Coverage Map

```
plugins/reference/zai.md
├── Distribution (@openclaw/zai-provider, included in OpenClaw) → note 1 (oc_plugin_reference_zai_zalo_zalouser)
├── Surface (providers: zai; contracts: mediaUnderstandingProviders) → note 1
└── Related docs (/providers/zai) ───────────────────────────────── → note 1 (link-out → pr09)
plugins/reference/zalo.md
├── Distribution (@openclaw/zalo, npm; ClawHub) ──────────────────── → note 1
├── Surface (channels: zalo) ────────────────────────────────────── → note 1
└── Related docs (/channels/zalo) ───────────────────────────────── → note 1 (link-out → ch06)
plugins/reference/zalouser.md
├── Distribution (@openclaw/zalouser, npm; ClawHub) ─────────────── → note 1
├── Surface (channels: zalouser; contracts: tools) ──────────────── → note 1
└── Related docs (/channels/zalouser, /plugins/zalouser) ─────────── → note 1 (link-out → ch06, pl25)
plugins/sdk-agent-harness.md
├── (intro: harness definition; see /concepts/agent-runtimes) ────── → note 2 (oc_sdk_agent_harness)
├── When to use a harness ────────────────────────────────────────── → note 2
├── What core still owns (incl. params.runtimePlan bundle) ───────── → note 2
├── Register a harness (AgentHarness, definePluginEntry) ─────────── → note 2
├── Selection policy ─────────────────────────────────────────────── → note 2
├── Provider plus harness pairing (Codex pattern, app-server floor) → note 2
│   ├── Tool-result middleware ────────────────────────────────────── → note 2
│   ├── Terminal outcome classification ──────────────────────────── → note 2
│   ├── Agent-end side effects ───────────────────────────────────── → note 2
│   └── Native Codex harness mode ────────────────────────────────── → note 2 (link-out → pl02 codex-harness)
├── Runtime strictness (auto vs explicit agentRuntime.id) ───────── → note 2
├── Native sessions and transcript mirror ───────────────────────── → note 2
├── Tool and media results ──────────────────────────────────────── → note 2
├── Current limitations ─────────────────────────────────────────── → note 2
└── Related (links) ─────────────────────────────────────────────── → note 2 References (link-out → pl24, co01)
plugins/sdk-channel-inbound.md
├── (intro: receive-path noun model + inbound/outbound subpaths) ── → note 3 (oc_sdk_channel_inbound)
├── Core Helpers (build/run/dispatch + runtime.channel.inbound.*) ── → note 3
└── Migration (turn.* removed → inbound.*) ──────────────────────── → note 3
plugins/sdk-channel-ingress.md
├── (intro: experimental access-control boundary, deprecated facade) → note 4 (oc_sdk_channel_ingress)
├── Runtime Resolver (resolveChannelMessageIngress, identity) ────── → note 4
├── Result (ingress/senderAccess/routeAccess/commandAccess/activation) → note 4
├── Access Groups (redacted accessGroup:<name>, fail-closed) ─────── → note 4
├── Event Modes (inbound/command/origin-subject/route-only/none) ── → note 4
├── Routes And Activation (route descriptors, mention gating) ────── → note 4
├── Redaction (raw sender/allowlist input-only) ─────────────────── → note 4
└── Verification (pnpm test / plugin-sdk:api:check) ─────────────── → note 4 References
plugins/sdk-channel-outbound.md
├── (intro: outbound subpath; core vs plugin ownership) ─────────── → note 5 (oc_sdk_channel_outbound)
├── Adapter (defineChannelMessageAdapter, receipt helper) ───────── → note 5
├── Existing Outbound Adapters (createChannelMessageAdapterFromOutbound) → note 5
├── Durable Sends (sendDurableMessageBatch + 4 outcomes) ────────── → note 5
└── Compatibility Dispatch (dispatchChannelInboundReply pointer) ── → note 5 (cross-ref note 3)
```
No orphaned sections. Provider/channel substance for zai/zalo/zalouser (link-out → pr09/ch06/pl25), the Codex
harness operator config (link-out → pl02), and SDK overview/runtime/entrypoints/provider-plugins (link-out →
pl24) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| reference/zai.md + reference/zalo.md + reference/zalouser.md (56/57/63w) | **MERGED** into note 1 | Each is a ~60-word plugin-manifest stub (Distribution/Surface/Related-docs pointer only) far below any usable density floor; merging into one package→surface→target reference table is lossless and avoids three orphan-thin notes. Inverse of a split — a controlled consolidation per the master's "most reference pages = 1 note" + anti-thin-note intent. |
| sdk-agent-harness.md (1,794w, 10 H2 / 4 H3) | note 2 (no split) | Under the 2,500w cap and a single dominant concept (the harness contract). The H3 subsections (middleware/outcome/side-effects/Codex mode) elaborate one surface; the config JSON is illustrative, not a separable procedure. Keep atomic. |
| sdk-channel-inbound / -ingress / -outbound (292 / 598 / 425w) | notes 3 / 4 / 5 (1:1) | Three distinct SDK subpaths (receive orchestration vs access-control authorization vs send/durability); each is a separate import surface and a focused procedure note, all well under cap. No merge (distinct contracts) and no split (each small + atomic). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (3,285 measured words). New `oc_` notes: **5**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×1** (note 1, plugin-manifest reference) · **concept ×1** (note 2, harness contract) ·
  **procedure ×3** (notes 3–5, channel inbound/ingress/outbound APIs).
- Est. digest words ~2,340 (avg ~468/note); all ≤ caps (≤400 lines, ≤2,500 words, ≤6 code blocks each).
- Source code fences (13 total across the 4 SDK pages) distribute one-per-note for the SDK notes; note 1 has 0
  source fences (the manifest is rendered as a table). No note approaches the 6-fence cap.
- Note count (5) is below the master's uniform 11-note estimate for pl23 because the section's actual measured
  content is 3 micro-stubs (consolidated to 1) + 4 SDK pages (1 each); the 11 figure is the master's flat
  ~1.5-notes/page heuristic, superseded by these measured counts (locked at augment).
- **Cross-refs (LOCKED at xref-augment 2026-06-21, RAISED floors):** every note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (PLUS relevant `repo_openclaw*` / sibling `oc_*`
  planned sibling `oc_*`). The exact per-note locked mapping is in "## Per-Note Related Notes Mapping (LOCKED
  — xref-augment 2026-06-21)".

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read source 2026-06-21,
> the remainder are sibling `oc_*` of this series / other OpenClaw-docs sub-plans marked **(planned, …)**, counted
> toward the 10-doc floor. Relative paths from `resources/documentation/openclaw/oc_X.md`: term →
> `../../term_dictionary/`, snippet → `../../code_snippets/`, repo → `../../../areas/code_repos/`, other doc →
> `../<folder>/`, entry point → `../../../0_entry_points/`, sibling oc_ → `oc_Y.md`.

### oc_plugin_reference_zai_zalo_zalouser (8t · 11s · 10d)

**Terms (8)**
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the metadata contract declaring a plugin's package, surface, and contracts; relevance: the Distribution/Surface/Related-docs fields of all three pages ARE plugin-manifest rows.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model/provider surface; relevance: `@openclaw/zai-provider` exposes `providers: zai` — a model-provider plugin.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the plugin abstraction that connects a chat platform to the gateway; relevance: `@openclaw/zalo`/`@openclaw/zalouser` declare `channels:` surfaces — channel-adapter plugins.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the hub routing chat platforms to the agent runtime; relevance: the Zalo bot/webhook + Zalo Personal channels route inbound/outbound through the gateway.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway these plugins extend; relevance: all three are `@openclaw/*` packages, included-in or installed-into OpenClaw.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the zai plugin's `providers: zai` + `mediaUnderstandingProviders` contract exposes an LLM/media-model provider surface.
- [Bot](../../term_dictionary/term_bot.md) — an automated chat participant; relevance: the zalo plugin is "for bot and webhook chats" — the Zalo bot channel.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — one agent reachable across many chat platforms; relevance: zai/zalo/zalouser are three more entries in OpenClaw's multi-platform channel/provider surface.

**Docs (10: 5 existing + 5 planned)**
- [Hermes: messaging LINE](../hermes_agent/hermes_messaging_line.md) — analog regional (Asia) chat-channel plugin doc; relevance: closest existing parallel to the Zalo regional-channel plugin manifests. *(existing)*
- [Hermes: messaging WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — analog personal-account channel via an unofficial library; relevance: parallels `zalouser`'s native zca-js personal-account integration. *(existing)*
- [Hermes: messaging Teams bot](../hermes_agent/hermes_messaging_teams_bot.md) — analog bot/webhook channel plugin doc; relevance: parallels the `zalo` bot/webhook channel surface. *(existing)*
- [Hermes: adding a platform adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how a channel-adapter plugin is packaged and registered; relevance: the engineering view behind a channel plugin's declared `channels:` surface. *(existing)*
- [Hermes: adding an inference provider](../hermes_agent/hermes_adding_inference_provider.md) — how a model/provider plugin is added; relevance: the engineering view behind zai's `providers: zai` surface. *(existing)*
- [oc_provider_zai](oc_provider_zai.md) — the substantive /providers/zai provider doc; relevance: the manifest row for zai points here for full config. **(planned, pr09)**
- [oc_channel_zalo](oc_channel_zalo.md) — the substantive /channels/zalo channel doc; relevance: the zalo manifest row's Related-docs target. **(planned, ch06)**
- [oc_channel_zalouser](oc_channel_zalouser.md) — the substantive /channels/zalouser channel doc; relevance: the zalouser manifest row's Related-docs target. **(planned, ch06)**
- [oc_sdk_provider_plugins](oc_sdk_provider_plugins.md) — the provider-plugin SDK contract; relevance: the contract zai's provider surface implements. **(planned, pl24)**
- [oc_sdk_channel_plugins](oc_sdk_channel_plugins.md) — the channel-plugin SDK contract; relevance: the contract zalo/zalouser's channel surfaces implement. **(planned, pl24)**

**Repos (4)**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — where model-provider plugins live; relevance: the home of the zai provider plugin.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin framework; relevance: where channel plugins like zalo/zalouser live.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: the Zalo bot/webhook + personal channel impls.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework; relevance: the registration plumbing all three manifests plug into.

**Snippets (11)**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — the plugin package/manifest contract; relevance: the code shape behind every Distribution/Surface manifest row.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — how a channel plugin's declared surface is registered/normalized; relevance: how `channels: zalo`/`zalouser` enter the registry.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin register/load lifecycle; relevance: how an npm/ClawHub-installed plugin is loaded.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `definePluginEntry`/plugin entry registration; relevance: the entry each `@openclaw/*` package exports.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a bundled model-provider plugin impl; relevance: the structural analog of the zai provider surface.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — another bundled provider plugin impl; relevance: shows the provider-surface shape zai mirrors.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — how provider models surface in the model catalog; relevance: where zai's `mediaUnderstandingProviders` models become visible.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel adapter contract; relevance: the contract zalo/zalouser channel surfaces implement.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — a bot-channel transport impl; relevance: structural analog of the Zalo bot/webhook transport.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — a bot-channel socket/webhook receive impl; relevance: parallels Zalo webhook chat receipt.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution at install; relevance: how an npm/ClawHub-installed channel plugin is trusted before load.

### oc_sdk_agent_harness (11t · 12s · 11d)

**Terms (11)**
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the low-level executor for one prepared agent turn; relevance: the exact subject of the page (`openclaw/plugin-sdk/agent-harness`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin registering a model/provider surface; relevance: the page's central contrast — "do NOT register a harness just to add a new LLM API; build a provider plugin"; most harnesses also register a provider.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the OpenClaw plugin extension SDK; relevance: the `openclaw/plugin-sdk/agent-harness` + `agent-harness-runtime` import surfaces are SDK subpaths.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding-agent servers/CLIs; relevance: "a native coding-agent server that owns threads and compaction" is exactly what a harness wraps (Codex).
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the `anthropic/claude-opus-4-8` + `agentRuntime.id: "claude-cli"` CLI-backend example in Runtime strictness.
- [Compaction](../../term_dictionary/term_compaction.md) — shrinking conversation history to fit context; relevance: "Codex owns the native thread id, resume behavior, compaction" — the harness, not core, owns compaction.
- [Model Failover](../../term_dictionary/term_model_failover.md) — switching models on failure; relevance: `runtimePlan.outcome.classifyRunResult(...)` + `classifyAgentHarnessTerminalOutcome(...)` feed OpenClaw's fallback-to-another-model policy.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — keeping session state across turns; relevance: the harness keeps a native session/resume token bound to the OpenClaw session + implements `reset(...)`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-driven tool invocation; relevance: tool-result middleware (`api.registerAgentToolResultMiddleware`) + dynamic tool calls returned through the harness result shape.
- [Meta-Harness](../../term_dictionary/term_meta_harness.md) — a harness that orchestrates other harnesses/agents; relevance: contrast concept clarifying what an *agent* harness is vs a meta-orchestrator.
- [AgentCore Runtime](../../term_dictionary/term_agentcore_runtime.md) — AWS's hosted agent-runtime service; relevance: the closest hosted analog of OpenClaw's host-vs-runtime ownership split (cross-domain contrast).

**Docs (11: 9 existing + 2 planned)**
- [Claude Code: Agent SDK agent loop](../claude_code/cc_agent_sdk_agent_loop.md) — the agent-turn execution loop the SDK owns; relevance: the canonical "one prepared turn executor" the harness contract parallels. *(existing)*
- [Hermes: agent loop](../hermes_agent/hermes_agent_loop.md) — Hermes's embedded turn loop; relevance: the embedded-runtime analog OpenClaw falls back to when no harness matches. *(existing)*
- [Hermes: provider runtime](../hermes_agent/hermes_provider_runtime.md) — provider+runtime pairing in Hermes; relevance: directly analogous to the "Provider plus harness pairing" section. *(existing)*
- [Hermes: Codex runtime setup](../hermes_agent/hermes_codex_runtime_setup.md) — operator setup for the Codex native runtime; relevance: the Hermes analog of the bundled-Codex app-server harness setup. *(existing)*
- [Hermes: Codex runtime tools](../hermes_agent/hermes_codex_runtime_tools.md) — tool handling under the Codex runtime; relevance: parallels tool-result middleware + "tool and media results" sections. *(existing)*
- [Bedrock AgentCore: harness](../aws_bedrock_agentcore/bedrock_agentcore_harness.md) — AgentCore's hosted harness concept; relevance: hosted-runtime analog of the OpenClaw harness contract. *(existing)*
- [Bedrock AgentCore: runtime architecture](../aws_bedrock_agentcore/bedrock_agentcore_runtime_architecture.md) — the hosted agent-runtime architecture; relevance: cross-domain analog of the host-vs-runtime ownership split. *(existing)*
- [Band: Codex adapter](../band/band_adapter_codex.md) — a Codex coding-agent adapter; relevance: the adapter analog of the bundled Codex harness's app-server protocol pairing. *(existing)*
- [Hermes: fallback providers](../hermes_agent/hermes_fallback_providers.md) — provider/model fallback policy; relevance: the analog of `runtimePlan.outcome.classifyRunResult` fallback when a harness turn produces no visible text. *(existing)*
- [oc_codex_harness](oc_codex_harness.md) — the Codex-harness operator-setup doc; relevance: the page explicitly link-outs "For operator setup … see Codex Harness". **(planned, pl02)**
- [oc_sdk_provider_plugins](oc_sdk_provider_plugins.md) — the provider-plugin SDK contract; relevance: the page says register a provider alongside the harness — this is that contract. **(planned, pl24)**

**Repos (5)**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the embedded agent runtime + harness registry; relevance: the host code the harness SDK plugs into (`registerAgentHarness`, selection policy).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin framework; relevance: `definePluginEntry` + `register(api)` that wire a harness in.
- [repo_pi_agent_harness_coding_agent](../../../areas/code_repos/repo_pi_agent_harness_coding_agent.md) — a coding-agent harness package; relevance: a direct "agent harness for a coding agent" implementation analog.

**Snippets (12)**
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness ↔ transcript-mirror binding; relevance: the exact "native sessions and transcript mirror" contract.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `definePluginEntry`/plugin entry registration; relevance: the registration entry in the "Register a harness" example.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin register/load lifecycle; relevance: how a bundled/trusted harness plugin is loaded.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load surfacing a harness; relevance: where `registerAgentHarness` results become selectable at runtime.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config resolution; relevance: the `agentRuntime.id` (`codex`/`claude-cli`/`openclaw`) runtime-strictness config the page details.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error classification; relevance: parallels `classifyRunResult` / terminal-outcome classification driving fallback.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — the model fallback ladder; relevance: what `empty`/`reasoning-only`/`planning-only` terminal outcomes feed into.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: the native-vs-core compaction ownership boundary.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy resolution; relevance: core keeps tool policy even when a harness owns the turn ("what core still owns").
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — the OpenAI provider impl; relevance: `openai/gpt-*` refs select the Codex harness by default — the provider the harness claims.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Hermes Codex provider plugin; relevance: the provider+harness pairing analog (synthetic auth, app-server).
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session reset helpers/hooks; relevance: the `reset(...)` sidecar-binding clear the harness must implement on session reset.

### oc_sdk_channel_inbound (8t · 11s · 10d)

**Terms (8)**
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the platform-to-gateway plugin abstraction; relevance: the inbound `adapter` (`ingest`, `resolveTurn`) + delivery adapter the page's helpers consume.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the inbound orchestration kernel; relevance: `runChannelInboundEvent` drives ingest→classify→preflight→resolve→record→dispatch→finalize — the channel kernel.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the plugin extension SDK; relevance: `openclaw/plugin-sdk/channel-inbound` is the SDK subpath documented.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the chat-to-agent hub; relevance: the receive path "platform event -> inbound context -> agent reply" terminates in the gateway.
- [Session Data](../../term_dictionary/term_session_data.md) — per-conversation session state; relevance: `runChannelInboundEvent` "records the session" for one inbound event.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable message delivery queue; relevance: `dispatchChannelInboundReply` records and dispatches the reply via a delivery adapter into the queue.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: `runtime.channel.inbound.*` aliases are exposed by the OpenClaw plugin runtime.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: channel-plugin receive paths handle bot/webhook inbound platform events.

**Docs (10: 5 existing + 5 planned)**
- [Hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — the receive→reply→send channel architecture; relevance: the analog of the inbound noun-model the page defines. *(existing)*
- [Hermes: adding a platform adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how a plugin channel adapter is built; relevance: the engineering view of the inbound `adapter` (`ingest`/`resolveTurn`). *(existing)*
- [Hermes: adding a platform adapter (builtin)](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — builtin channel receive paths; relevance: the bundled-channel analog that already receives the runtime object (`runtime.channel.inbound.*`). *(existing)*
- [Hermes: messaging LINE](../hermes_agent/hermes_messaging_line.md) — a concrete channel receive/reply impl; relevance: shows a real inbound normalization + reply dispatch. *(existing)*
- [Hermes: messaging Teams bot](../hermes_agent/hermes_messaging_teams_bot.md) — a bot-channel receive impl; relevance: a concrete receive-path migration target for the inbound API. *(existing)*
- [oc_sdk_channel_outbound](oc_sdk_channel_outbound.md) — the outbound send/receipt SDK; relevance: the page pairs inbound with outbound ("use channel-outbound for native send"). **(note 5, this series)**
- [oc_sdk_channel_ingress](oc_sdk_channel_ingress.md) — the ingress access-control SDK; relevance: the preflight/admission gate inside `runChannelInboundEvent`. **(note 4, this series)**
- [oc_sdk_channel_plugins](oc_sdk_channel_plugins.md) — the channel-plugin SDK overview; relevance: the umbrella contract inbound is one subpath of. **(planned, pl24)**
- [oc_sdk_overview](oc_sdk_overview.md) — the plugin SDK overview; relevance: situates the channel subpaths in the SDK. **(planned, pl24)**
- [oc_concept_messages](oc_concept_messages.md) — the message lifecycle concept; relevance: the conceptual receive→reply→deliver lifecycle the inbound API implements. **(planned, co04)**

**Repos (3)**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin framework; relevance: where channel-plugin receive paths live.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel impls; relevance: concrete inbound implementations using these helpers.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — analog inbound messaging gateway; relevance: a parallel receive-path implementation.

**Snippets (11)**
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — inbound event dispatch; relevance: the `runChannelInboundEvent`/`dispatchChannelInboundReply` dispatch step.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — project channel facts into context; relevance: exactly `buildChannelInboundEventContext`'s job.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel adapter contract; relevance: the `adapter: { ingest, resolveTurn }` shape.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — resolve the inbound turn; relevance: the `resolveTurn`/`resolveInboundReply` resolution step.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — normalize a platform event into the registry; relevance: the `ingest: normalizePlatformEvent` step.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — a concrete channel inbound dispatcher; relevance: a real `runtime.channel.inbound.run` caller.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack inbound socket receive; relevance: a concrete platform-event receive feeding the inbound API.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — gateway agent dispatch handler; relevance: where the resolved inbound turn reaches the agent.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — session chat-type resolution; relevance: the session record `runChannelInboundEvent` writes.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — gateway runner reply dispatch; relevance: analog of `dispatchChannelInboundReply` reply delivery.
- [snippet_hermes_agent_gw_platform_telegram_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_normalize.md) — platform event normalization; relevance: the `ingest`/normalize step analog.

### oc_sdk_channel_ingress (9t · 11s · 10d)

**Terms (9)**
- [Access Control](../../term_dictionary/term_access_control.md) — authorization of who may act; relevance: ingress is "the experimental access-control boundary for inbound channel events" — DM/group allowlists, route/command/event gates.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing a direct-message sender to an account; relevance: "pairing-store DM entries" + `event.mayPair` are core ingress inputs.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the platform plugin abstraction; relevance: ingress is the channel plugin's authorization seam (plugins own platform facts, core owns policy).
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: `defineStableChannelIngressIdentity({ sensitivity: "pii" })` + redaction of raw sender values.
- [Session Sanitization](../../term_dictionary/term_session_sanitization.md) — stripping raw inputs from persisted/diagnostic state; relevance: the Redaction rule — raw sender/allowlist values are resolver input only, never in resolved state/diagnostics/snapshots.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the plugin extension SDK; relevance: `openclaw/plugin-sdk/channel-ingress-runtime` (and the deprecated `channel-ingress` facade) are SDK subpaths.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the chat-to-agent hub; relevance: ingress gates inbound message admission into the gateway.
- [Contingent Authorization](../../term_dictionary/term_contingent_authorization.md) — ordered/conditional grant of access; relevance: the ordered gate decision (`ingress.graph`/`reasonCode`) + fail-closed admission.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny security posture; relevance: "Missing, unsupported, and failed groups fail closed" — the fail-closed ingress default.

**Docs (10: 5 existing + 5 planned)**
- [Hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — receive-path architecture incl. admission; relevance: where ingress authorization sits in the channel pipeline. *(existing)*
- [Hermes: adding a platform adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel plugin; relevance: where a plugin supplies platform facts to the ingress resolver. *(existing)*
- [Hermes: messaging Simplex](../hermes_agent/hermes_messaging_simplex.md) — a privacy-focused channel with allowlist/pairing; relevance: concrete DM-allowlist + pairing access-control parallel. *(existing)*
- [Hermes: messaging WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — a personal-account channel with sender gating; relevance: concrete group/DM allowlist + sender-policy analog. *(existing)*
- [Bedrock AgentCore: runtime auth features](../aws_bedrock_agentcore/bedrock_agentcore_runtime_auth_features.md) — hosted-runtime inbound auth; relevance: cross-domain analog of fail-closed inbound authorization + identity. *(existing)*
- [oc_sdk_channel_inbound](oc_sdk_channel_inbound.md) — the inbound orchestration SDK; relevance: ingress runs inside `runChannelInboundEvent`'s preflight/resolve step. **(note 3, this series)**
- [oc_channel_access_groups](oc_channel_access_groups.md) — the access-groups channel doc; relevance: the `accessGroup:<name>` redaction + dynamic-group resolution the Result section describes. **(planned, ch01)**
- [oc_channel_pairing](oc_channel_pairing.md) — the channel pairing doc; relevance: the pairing-store DM entries + `mayPair` semantics. **(planned, ch04)**
- [oc_channel_channel_routing](oc_channel_channel_routing.md) — the channel-routing doc; relevance: route descriptors + route gates the "Routes And Activation" section uses. **(planned, ch01)**
- [oc_concept_presence](oc_concept_presence.md) — the presence/activation concept; relevance: mention-gating as an activation gate (`admission: "skip"`). **(planned, co05)**

**Repos (3)**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin framework; relevance: where channel ingress impls live.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel impls; relevance: concrete per-platform access gates.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — fail-closed authorization + redaction policy; relevance: the security posture behind the ingress fail-closed + redaction rules.

**Snippets (11)**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM/group allowlist + pairing resolution; relevance: the exact `resolveChannelMessageIngress` allowlist/pairing logic.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — route descriptors / route gates; relevance: the `route: { id, allowed, senderPolicy, … }` descriptor the page shows.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — route/thread policy + activation; relevance: `channelIngressRoutes(...)` precedence + activation gating.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — sender/conversation resolution; relevance: the `subject`/`conversation` resolution feeding `senderAccess`.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM access-control security audit; relevance: validates the fail-closed DM/group admission the page mandates.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance tracking; relevance: the input-only-raw-values redaction (raw sender/allowlist never leave input).
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — gateway authorize dispatch; relevance: the ordered authorization/admission decision analog.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method/command gating; relevance: the `command`/`commandAccess` command-gate analog.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — pairing flow; relevance: the pairing-store path behind `mayPair`.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — slash-command access control; relevance: command-gate / scoped-button auth (`authMode: "command"`) analog.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix channel ACL; relevance: a concrete per-platform allowlist/route ACL analog.

### oc_sdk_channel_outbound (8t · 11s · 10d)

**Terms (8)**
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the platform plugin abstraction; relevance: the page defines the `message` adapter (`defineChannelMessageAdapter`) + derivation from an existing outbound adapter.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the orchestration kernel; relevance: "core owns queueing, durability, generic retry policy, hooks, receipts" — the kernel the adapter feeds.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the chat-to-agent hub; relevance: the send path out of the gateway to the platform.
- [Message Queue](../../term_dictionary/term_message_queue.md) — durable delivery queue; relevance: `sendDurableMessageBatch(...)` and its sent/suppressed/partial_failed/failed outcomes.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the plugin extension SDK; relevance: `openclaw/plugin-sdk/channel-outbound` is the SDK subpath documented.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/send context; relevance: `withDurableMessageSendContext` + receipt persistence across the send batch.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: runtime send helpers live on the OpenClaw `channel-outbound` runtime surface.
- [Bot](../../term_dictionary/term_bot.md) — automated chat participant; relevance: channel send paths deliver bot replies/receipts to the platform.

**Docs (10: 5 existing + 5 planned)**
- [Hermes: messaging Slack](../hermes_agent/hermes_messaging_slack.md) — a concrete channel send/receipt impl; relevance: a real native send/edit/receipt path the adapter pattern abstracts. *(existing)*
- [Hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — receive→reply→send architecture; relevance: where outbound send/durability sits in the pipeline. *(existing)*
- [Hermes: messaging media settings](../hermes_agent/hermes_messaging_media_settings.md) — outbound media/delivery settings; relevance: the media-capable adapter capabilities (`media: true`) + delivery suppression. *(existing)*
- [Hermes: adding a platform adapter (plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel adapter; relevance: the engineering view of `defineChannelMessageAdapter` + capabilities. *(existing)*
- [Hermes: messaging Teams bot](../hermes_agent/hermes_messaging_teams_bot.md) — a bot-channel send impl; relevance: a concrete declared-capabilities send path analog. *(existing)*
- [oc_sdk_channel_inbound](oc_sdk_channel_inbound.md) — the inbound orchestration SDK; relevance: "Compatibility Dispatch" assembles `dispatchChannelInboundReply(...)` from channel-inbound. **(note 3, this series)**
- [oc_sdk_channel_ingress](oc_sdk_channel_ingress.md) — the ingress access-control SDK; relevance: the sibling channel subpath (admission before reply send). **(note 4, this series)**
- [oc_sdk_channel_plugins](oc_sdk_channel_plugins.md) — the channel-plugin SDK overview; relevance: the umbrella contract outbound is one subpath of. **(planned, pl24)**
- [oc_sdk_overview](oc_sdk_overview.md) — the plugin SDK overview; relevance: situates the channel subpaths in the SDK. **(planned, pl24)**
- [oc_concept_messages](oc_concept_messages.md) — the message lifecycle concept; relevance: the send/receipt/durability stage of the message lifecycle. **(planned, co04)**

**Repos (3)**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel-plugin framework; relevance: where channel-plugin send paths live.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel impls; relevance: durable messaging send implementations.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — analog outbound messaging delivery; relevance: a parallel durable-send implementation.

**Snippets (11)**
- [snippet_openclaw_channels_kernel_durable](../../code_snippets/snippet_openclaw_channels_kernel_durable.md) — durable send batch + outcomes; relevance: the `sendDurableMessageBatch` sent/suppressed/partial_failed/failed analog.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — native send/edit/receipt; relevance: the plugin-owned native send/edit + receipt creation.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the adapter capability contract; relevance: "only declare capabilities the native transport actually preserves".
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — delivery dispatch; relevance: the dispatch step the durable send batch drives.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy / silent-payload suppression; relevance: the `suppressed` outcome + `NO_REPLY`/silent-payload delivery rule.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — gateway chat send handler; relevance: where core's queue/durability hands a payload to the adapter `send`.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — target/conversation resolution; relevance: the `to`/`replyToId`/`threadId` target normalization in `send.text`.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — the send tool dispatch; relevance: the shared `message` tool path core owns.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — send payload formatting; relevance: payload shaping before the native send call.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — gateway runner outbound delivery; relevance: analog of `deliverInboundReplyWithMessageSendContext`.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — a native send transport impl; relevance: a concrete plugin-owned `send` call the adapter wraps.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT as new
> `term_dictionary` entries; the only term interaction is LINKING existing terms. pl23 introduces **0 new
> term_dictionary captures**.

| Term (appearing in pl23 source) | Disposition |
|---|---|
| runtimePlan / runtime policy bundle | Documented inline in note 2 as an OpenClaw-specific config object (not a reusable cross-cutting term). No capture. |
| channel inbound / outbound / ingress API | Subjects of notes 3/4/5. OpenClaw SDK surface names → `oc_*` notes; LINK existing `term_channel_adapter`, `term_channel_kernel`, `term_plugin_sdk`. |
| access mode / authMode / route gate / mention activation | Documented in note 4 as OpenClaw ingress mechanics; LINK existing `term_access_control`, `term_dm_pairing`, `term_contingent_authorization`. No capture. |
| durable send / message receipt / message adapter | Documented in note 5; LINK existing `term_message_queue`, `term_channel_adapter`. No capture. |
| Codex (harness / app-server / native mode) | `term_codex` ABSENT in DB (checked). Documented inline in note 2 as the bundled-plugin example; link-out to `plugins/codex-harness` (pl02, planned). LINK `term_autonomous_coding_agents` + `term_claude` as nearest existing terms. **Not** promoted to a new term here (it is a product/plugin name with a doc-page home in pl02, per the master's OpenClaw-vocab-as-doc-notes policy). |
| zai / zalo / zalouser (plugin names) | Plugin/provider/channel names → documented as note 1 manifest rows; not promoted to term notes (master policy: provider/channel names are config, link `term_llm`/`term_provider_plugin`/`term_channel_adapter`). |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and
an existing note appears in these 7 pages. Augment re-runs the Step 2d / Step 4e scan to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl23 authors zero `term_dictionary` notes; it only links existing terms (all

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (5 notes, P3). All gates must PASS before commit.

| Gate | Check | Tooling |
|---|---|---|
| G1 | Format: YAML field order + forbidden-field absence; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traceable to `inbox/openclaw_docs/plugins/<page>`; no invented surface names/fields | diff vs mirror page |
| G3 | Density + Coverage: ≤400 lines, ≤2,500 words, ≤6 code blocks; one BB/note; every mapped H2/H3 covered | `wc`, fence count, Section Coverage Map |
| G4 | Cross-Reference: ≥6 relevance-selected terms + repos/docs/snippets per note, each with a relevance statement | Related Notes section audit |
| G5 | Ghost-reference detect + redirect: every cited link resolves in DB | `scripts/` ghost scan / `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix: 0 broken relative links after reindex | `/tessellum-fix-broken-links` |
| G7 | Discoverability: each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | `entry_openclaw_docs.md` rows + inlinks below |
| G8 | In-degree ≥1 (anti-island) verified in `note_links` after reindex | DB query on `note_links` |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugin_reference_zai_zalo_zalouser oc_sdk_agent_harness oc_sdk_channel_inbound oc_sdk_channel_ingress oc_sdk_channel_outbound"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # sibling-prefix self-citation sanity (informational)
  grep -qE "\($SIBLING_PREFIX" "$f" || echo "$n: no sibling $SIBLING_PREFIX link (check Related Notes)"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb cb / $lines L)"
done

# YAML frontmatter validation across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Src fences | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugin_reference_zai_zalo_zalouser | model | 320 | 0 | ✅ (table-only) |
| 2 | oc_sdk_agent_harness | concept | 700 | ≤3 (of 5 src; config JSON selective) | ✅ |
| 3 | oc_sdk_channel_inbound | procedure | 380 | ≤3 | ✅ |
| 4 | oc_sdk_channel_ingress | procedure | 520 | ≤3 | ✅ |
| 5 | oc_sdk_channel_outbound | procedure | 420 | ≤2 | ✅ |

No note approaches the 2,500w / 6-fence / 400-line caps. The largest source page (sdk-agent-harness, 1,794w / 5
fences) is digested (not transcribed) to ~700w with ≤3 selective code blocks; channel-page code is reproduced
one illustrative fence at a time.

## Entry Point Decision (inherited from master)

Contributes **5 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step) under the **Plugins → SDK
& Reference** cluster: note 1 under "Plugin Reference (manifests)", notes 2–5 under "Plugin SDK contracts". Each
note receives its entry-point back-link at finalization (this is the primary G7/G8 inbound-link source). No new
entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):
- `entry_openclaw_docs.md` **(planned, W1)** → all 5 notes (primary anti-island inbound source).
- `repo_openclaw_agents` → note 2 (harness registry ↔ harness SDK contract).
- `repo_openclaw_channels` → notes 3, 4, 5 (channel receive/ingress/send impls ↔ their SDK contracts).
- `repo_openclaw_channels_messaging` → notes 1, 3, 5.
- `repo_openclaw_extensions_llm_providers` → note 1 (zai provider plugin).
- `term_agent_harness` → note 2; `term_channel_adapter` → notes 1, 3, 4, 5; `term_provider_plugin` → notes 1, 2;
  `term_access_control` → note 4 (reciprocal Related-Notes backlinks).

## Pacing Rules (inherited from master)

Single phase, 5 notes (well under the ~30-agent fan-out cap). Re-read each source page; reproduce code fences
verbatim and selectively (≤6/note). One BB per note. `git pull --rebase --autostash` first; commit + push after
the phase; no Claude co-author trailer. Reindex incrementally; verify `note_links` (in-degree ≥1) + 0 broken
links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Skill:** `/tessellum-augment-digestion-plan` (xref-augment pass). **Source re-read:** all 7 mirror pages under
`inbox/openclaw_docs/plugins/` re-read 2026-06-21 (zai 56w, zalo 57w, zalouser 63w, sdk-agent-harness 1,794w,
sdk-channel-inbound 292w, sdk-channel-ingress 598w, sdk-channel-outbound 425w — confirms the plan's Source
table; no >1.5× under-estimate).

**Locked:** replaced the candidate cross-reference lists with a `## Per-Note Related Notes Mapping (LOCKED —
xref-augment 2026-06-21)` at RAISED floors: **≥8 terms · ≥10 snippets · ≥10 docs per note**, relevance-selected
band/`band_*`, aws_bedrock_agentcore/`bedrock_*` coding-agent corpora); the remaining doc slots are sibling
`oc_*` of this series / other OpenClaw-docs sub-plans marked **(planned, …)**.

**Per-note counts (terms / snippets / docs[existing+planned] / repos — all floors met):**

| Note | Terms | Snippets | Docs (exist+plan) | Repos | Floors (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_plugin_reference_zai_zalo_zalouser | 8 | 11 | 10 (5+5) | 4 | MET |
| oc_sdk_agent_harness | 11 | 12 | 11 (9+2) | 5 | MET |
| oc_sdk_channel_inbound | 8 | 11 | 10 (5+5) | 3 | MET |
| oc_sdk_channel_ingress | 9 | 11 | 10 (5+5) | 3 | MET |
| oc_sdk_channel_outbound | 8 | 11 | 10 (5+5) | 3 | MET |

**New-term candidates:** **none.** Re-running the Step 2d / Step 4e scan over the 7 re-read pages surfaced no
genuinely cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note. All vocabulary
either (a) is the subject of an `oc_*` doc note (agent harness → note 2; channel inbound/ingress/outbound →
term that is LINKED (28 distinct terms used across the 5 notes, all verified), or (c) is OpenClaw-specific config
documented inline (`runtimePlan` bundle, `authMode` modes, `agentRuntime.id`). `term_codex` remains ABSENT and is
intentionally NOT promoted (product/plugin name with a doc-page home at pl02; nearest existing terms
`term_autonomous_coding_agents` + `term_claude` are linked). Best-fit glossary if a term ever WERE proposed:
`acronym_glossary_agentic_ai.md` / `acronym_glossary_llm.md` — but **0 captures planned for pl23**.

**Collision/dedup audit (generalized to ALL planned notes, term_dictionary AND documentation/):** the 5 planned
`oc_*` doc slugs were checked against existing notes — none duplicate an existing term or doc note. `term_agent_harness`,
`term_channel_adapter`, `term_channel_kernel`, `term_plugin_sdk`, `term_provider_plugin` already exist and are
LINKED (the doc notes document the OpenClaw SDK *surface*, distinct from the cross-cutting term concept). No
removals/renames required (0 new term slugs to audit).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review per the review-digestion-plan canonical (9 checkpoints). Source spot-check: re-read
sdk-agent-harness (1,794w), sdk-channel-ingress (598w), sdk-channel-outbound (425w) — all within ±30% of plan
estimates.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6, G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present (single phase) with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link, G7+G8 discoverability/in-degree. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision` contributes 5 rows to `entry_openclaw_docs.md` (master W1 pre-step); `## Inlinks` lists outside-folder inbound sources. No new entry point created here (correct — master owns W1). |
| CP4 | Plan size manageable | **PASS** | 5 notes, single phase — far ≤30. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format inherited verbatim from master Format Definition (derived from existing `claude_code/cc_*` + `pi/pi_*` corpora): YAML field order, `# OpenClaw — …` H1, `## Overview` + `## Related Notes`, bold footer; forbidden-field list present. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: largest note (oc_sdk_agent_harness ~700w / ≤3 fences) far under 2,500w/6-fence/400-line caps; no borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | `## Source Pages (Measured 2026-06-20)` table with per-page `wc -w` + fence counts; re-verified on 3 pages at review (within ±30%). |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (every row dispositioned); `## Term-Note Authoring Requirements` = N/A (0 new terms) per master OpenClaw-vocab-as-doc-notes policy — explicitly justified. |
| CP8f | Slug specificity + collision/dedup audit | **PASS** | 0 new term slugs (no specificity renames needed); collision audit generalized to the 5 `oc_*` doc slugs vs term_dictionary AND documentation/ — no duplicate of an existing term/doc note (Augmentation Report dedup audit). |
| CP9 | Discoverability / inlinks (G8, no graph island) | **PASS** | `## Inlinks` maps every new note to ≥1 outside-folder inbound source (entry_openclaw_docs + repo_openclaw_* + reciprocal term backlinks); G8 in-degree check in the gate table marks inlinks as EXECUTED at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
