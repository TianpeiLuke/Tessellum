---
title: Sub-Plan pl02 — OpenClaw Docs: Plugins (Codex Harness / Computer Use / Community / Compatibility)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/codex-computer-use", "plugins/codex-harness", "plugins/codex-harness-reference", "plugins/codex-harness-runtime", "plugins/codex-native-plugins", "plugins/community", "plugins/compatibility"]
---

# Sub-Plan pl02: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, `## Overview`/`## Related Notes`/`## References` body), dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), undigested-terms ownership (OpenClaw vocab → `oc_*` doc notes, 0 new term captures), 9-GATE validation, cross-refs, and the `entry_openclaw_docs.md` entry-point decision are ALL inherited from the master.

## Scope

The 7 Codex-harness / plugin-ecosystem pages of the OpenClaw `plugins/` section: how OpenClaw runs embedded
agent turns through the bundled **Codex app-server harness** (setup, deployment, policy, diagnostics, config
reference, runtime contract), the **Codex Computer Use** desktop-control MCP plugin, **native Codex plugins**
managed from chat, the **community** plugin discovery/publish workflow, and the **compatibility registry +
deprecation policy**. These pages define the Codex-runtime-on-OpenClaw vocabulary that the providers/CLI/concepts
sections reference. **Priority P3 (Phase C — plugin reference sprawl)**, but content overlaps heavily with the
P1 agent-runtime/runtime-boundary concepts, so cross-refs to the concepts/providers corpora are dense. The
code-side counterparts (`repo_openclaw_agents`, `repo_openclaw_extensions`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 15,957 measured words, 90 code fences. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Codex Computer Use | plugins/codex-computer-use | 1,937 | 8 | 13 | 0 | procedure |
| Codex harness | plugins/codex-harness | 5,249 | 16 | 11 | 3 | procedure (split ×3: setup / deploy+policy / diagnostics) |
| Codex harness reference | plugins/codex-harness-reference | 3,137 | 10 | 12 | 0 | model (split ×2: config-surface / runtime-exec reference) |
| Codex harness runtime | plugins/codex-harness-runtime | 2,290 | 0 | 11 | 0 | concept |
| Codex native plugins | plugins/codex-native-plugins | 1,673 | 5 | 10 | 0 | procedure |
| Community | plugins/community | 366 | 4 | 3 | 0 | procedure |
| Compatibility | plugins/compatibility | 1,305 | 2 | 7 | 3 | model |

> Code = raw `^```` fence lines ÷ 2. Source raw fence-line counts: 16/32/20/0/10/8/4 respectively (the table
> shows fence-pairs). `codex-harness-runtime.md` has 0 code blocks (pure prose runtime contract).

## Content Strategy

- **Prioritize**: the Codex-harness **ownership boundary** (what OpenClaw owns vs what Codex owns — the
  load-bearing concept the whole section turns on, in `codex-harness` Overview/Runtime-boundaries and the entire
  `codex-harness-runtime` page) and the **setup/quickstart procedure** (every Codex-mode deployment depends on
  it). These are the highest-relevance notes for downstream linking.
- **Split**: `codex-harness.md` (5,249w / 32 fences — 2.1× the word cap, 3 distinct task clusters) → setup
  procedure + deployment-patterns/app-server-policy procedure + commands/diagnostics/troubleshooting procedure.
  `codex-harness-reference.md` (3,137w / 20 fences, config-reference model BB) → plugin-config-surface reference
  + runtime/exec reference (sandbox/auth-isolation/dynamic-tools/timeouts/model-discovery/bootstrap/env). All
  other pages stay 1 note each (each ≤2,500w and single-BB).
- **Skip / link-out**: provider auth precedence detail → providers section (link `pi_provider_auth` analog +
  `term_oauth_token`); the QuickJS-WASI `/reference/code-mode` runtime is a *different* feature explicitly
  contrasted on the page → link out, do not redefine; ACP/acpx external-harness path → link
  `term_acp_agent_client_protocol` (covered in pl05 `plugins/reference/acpx` / cli `cli/acp`); Peekaboo bridge
  → link out to the platforms section. Provider/model names (OpenAI, ChatGPT, gpt-5.5) are documented as config,
  NOT promoted to term notes (link `term_llm`/`term_claude`/`term_autonomous_coding_agents`).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_codex_computer_use.md` | procedure | codex-computer-use.md (all 13 H2: Peekaboo distinction, iOS app, Direct cua-driver MCP, Quick setup, Commands, Marketplace choices, Bundled macOS marketplace, Remote catalog limit, Configuration reference, What OpenClaw checks, macOS permissions, Troubleshooting) | 650 | Setting up Codex Computer Use, the Codex-native desktop-control MCP plugin, for Codex-mode OpenClaw agents: how OpenClaw prepares (not vendors) the plugin, `/codex computer-use` commands, marketplace/catalog choices, `computerUse` config, and macOS permission + troubleshooting flow. |
| 2 | `oc_plugins_codex_harness_setup.md` | procedure | codex-harness.md: intro, Requirements, Quickstart, Configuration, Verify Codex runtime, Routing and model selection | 700 | Enabling the bundled `codex` plugin so OpenClaw runs embedded OpenAI agent turns through Codex app-server: requirements, OAuth quickstart, config-table options, runtime verification, and `openai/gpt-*`-vs-runtime-policy routing. |
| 3 | `oc_plugins_codex_harness_deployment.md` | procedure | codex-harness.md: Deployment patterns (Basic / Mixed provider / Fail-closed), App-server policy | 650 | Codex-harness deployment patterns — basic all-Codex, mixed-provider, and fail-closed (`agentRuntime.id: "codex"`) — plus the app-server policy controlling approvals, sandbox, and exec behavior per deployment. |
| 4 | `oc_plugins_codex_harness_diagnostics.md` | procedure | codex-harness.md: Commands and diagnostics (incl. Inspect Codex threads locally), Computer Use (pointer), Runtime boundaries (pointer), Troubleshooting | 600 | Operating a Codex-harness deployment: `/codex` chat commands, local Codex-thread inspection, diagnostics/feedback upload, the OpenClaw-owns-vs-Codex-owns runtime-boundary summary, and troubleshooting common Codex-harness failures. |
| 5 | `oc_plugins_codex_harness_reference_config.md` | model | codex-harness-reference.md: Plugin config surface, App-server transport, Approval and sandbox modes, Model discovery, Workspace bootstrap files, Environment overrides | 700 | The Codex-harness configuration reference: `plugins.entries.codex.config.*` surface, app-server transport options, approval/sandbox modes, model discovery, workspace bootstrap files, and environment overrides. |
| 6 | `oc_plugins_codex_harness_reference_runtime.md` | model | codex-harness-reference.md: Sandboxed native execution, Auth and environment isolation, Dynamic tools, Timeouts | 600 | The Codex-harness runtime-execution reference: sandboxed native exec, auth/environment isolation between OpenClaw and Codex home, OpenClaw dynamic-tool bridging into app-server, and per-phase timeouts. |
| 7 | `oc_plugins_codex_harness_runtime.md` | concept | codex-harness-runtime.md (all 11 H2: Overview, Thread bindings and model changes, Visible replies and heartbeats, Hook boundaries, V1 support contract, Native permissions and MCP elicitations, Queue steering, Codex feedback upload, Compaction and transcript mirror, Media and delivery) | 700 | The Codex-harness runtime contract — what changes when Codex owns the native model loop: ownership boundary, thread bindings, heartbeats, hook boundaries, the V1 support contract, native permissions/elicitations, queue steering, feedback upload, compaction + transcript mirror, and media delivery. |
| 8 | `oc_plugins_codex_native_plugins.md` | procedure | codex-native-plugins.md (all 10 H2: Requirements, Quickstart, Manage plugins from chat, How native plugin setup works, V1 support boundary, App inventory and ownership, Thread app config, Destructive action policy, Troubleshooting) | 600 | Configuring and managing native Codex (app-server) plugins from OpenClaw chat: requirements, quickstart, `/codex plugins` management, how native setup works, the V1 support boundary, app inventory/ownership, thread app config, destructive-action policy, and troubleshooting. |
| 9 | `oc_plugins_community.md` | procedure | community.md (all 3 H2: Find plugins, Publish plugins) | 350 | Discovering and publishing OpenClaw community plugins: finding plugins via the marketplace/registry and the publish workflow for sharing your own plugin. |
| 10 | `oc_plugins_compatibility.md` | model | compatibility.md: Compatibility registry, Plugin inspector package (incl. Maintainer acceptance lane), Deprecation policy, Release notes | 600 | The OpenClaw plugin compatibility model: the compatibility registry, the plugin-inspector package + maintainer acceptance lane, and the deprecation/release-notes policy that governs plugin lifecycle. |
| 11 | `oc_plugins_compatibility_areas.md` | model | compatibility.md: Current compatibility areas (incl. WhatsApp Inbound Callback Flat Aliases, WhatsApp Inbound Admission Fields) | 450 | The current per-area compatibility shims tracked by OpenClaw — notably the WhatsApp inbound callback flat-alias mappings and inbound admission fields — the concrete schema-level compatibility surface plugins must honor. |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_` (e.g. `plugins/codex-computer-use` →
`oc_plugins_codex_computer_use`); split notes append a short aspect suffix.

## Section Coverage Map

```
plugins/codex-computer-use.md
├── (intro)                                              → note 1 (oc_plugins_codex_computer_use)
├── OpenClaw.app and Peekaboo (link-out platforms)      → note 1
├── iOS app ───────────────────────────────────────────→ note 1
├── Direct cua-driver MCP ─────────────────────────────→ note 1
├── Quick setup ───────────────────────────────────────→ note 1
├── Commands ──────────────────────────────────────────→ note 1
├── Marketplace choices ───────────────────────────────→ note 1
├── Bundled macOS marketplace ─────────────────────────→ note 1
├── Remote catalog limit ──────────────────────────────→ note 1
├── Configuration reference ───────────────────────────→ note 1
├── What OpenClaw checks ───────────────────────────────→ note 1
├── macOS permissions ─────────────────────────────────→ note 1
├── Troubleshooting ───────────────────────────────────→ note 1
└── Related (source nav; not digested) ────────────────→ (drop — replaced by ## Related Notes)
plugins/codex-harness.md
├── (intro: ownership boundary, code-mode contrast) ───→ note 2 (oc_plugins_codex_harness_setup)
├── Requirements ──────────────────────────────────────→ note 2
├── Quickstart ────────────────────────────────────────→ note 2
├── Configuration ─────────────────────────────────────→ note 2
├── Verify Codex runtime ──────────────────────────────→ note 2
├── Routing and model selection ───────────────────────→ note 2
├── Deployment patterns ───────────────────────────────→ note 3 (oc_plugins_codex_harness_deployment)
│   ├── Basic Codex deployment ────────────────────────→ note 3
│   ├── Mixed provider deployment ─────────────────────→ note 3
│   └── Fail-closed Codex deployment ──────────────────→ note 3
├── App-server policy ─────────────────────────────────→ note 3
├── Commands and diagnostics ──────────────────────────→ note 4 (oc_plugins_codex_harness_diagnostics)
│   └── Inspect Codex threads locally ─────────────────→ note 4
├── Computer Use (pointer → note 1) ───────────────────→ note 4 (1-line pointer)
├── Runtime boundaries (pointer → note 7) ─────────────→ note 4 (summary; full in note 7)
├── Troubleshooting ───────────────────────────────────→ note 4
└── Related (source nav) ──────────────────────────────→ (drop)
plugins/codex-harness-reference.md
├── Plugin config surface ─────────────────────────────→ note 5 (oc_..._reference_config)
├── App-server transport ──────────────────────────────→ note 5
├── Approval and sandbox modes ────────────────────────→ note 5
├── Sandboxed native execution ────────────────────────→ note 6 (oc_..._reference_runtime)
├── Auth and environment isolation ────────────────────→ note 6
├── Dynamic tools ─────────────────────────────────────→ note 6
├── Timeouts ──────────────────────────────────────────→ note 6
├── Model discovery ───────────────────────────────────→ note 5
├── Workspace bootstrap files ─────────────────────────→ note 5
├── Environment overrides ─────────────────────────────→ note 5
└── Related (source nav) ──────────────────────────────→ (drop)
plugins/codex-harness-runtime.md
├── Overview (ownership boundary) ─────────────────────→ note 7 (oc_plugins_codex_harness_runtime)
├── Thread bindings and model changes ─────────────────→ note 7
├── Visible replies and heartbeats ────────────────────→ note 7
├── Hook boundaries ───────────────────────────────────→ note 7
├── V1 support contract ───────────────────────────────→ note 7
├── Native permissions and MCP elicitations ───────────→ note 7
├── Queue steering ────────────────────────────────────→ note 7
├── Codex feedback upload ─────────────────────────────→ note 7
├── Compaction and transcript mirror ──────────────────→ note 7
├── Media and delivery ────────────────────────────────→ note 7
└── Related (source nav) ──────────────────────────────→ (drop)
plugins/codex-native-plugins.md
├── Requirements ──────────────────────────────────────→ note 8 (oc_plugins_codex_native_plugins)
├── Quickstart ────────────────────────────────────────→ note 8
├── Manage plugins from chat ──────────────────────────→ note 8
├── How native plugin setup works ─────────────────────→ note 8
├── V1 support boundary ───────────────────────────────→ note 8
├── App inventory and ownership ───────────────────────→ note 8
├── Thread app config ─────────────────────────────────→ note 8
├── Destructive action policy ─────────────────────────→ note 8
├── Troubleshooting ───────────────────────────────────→ note 8
└── Related (source nav) ──────────────────────────────→ (drop)
plugins/community.md
├── Find plugins ──────────────────────────────────────→ note 9 (oc_plugins_community)
├── Publish plugins ───────────────────────────────────→ note 9
└── Related (source nav) ──────────────────────────────→ (drop)
plugins/compatibility.md
├── Compatibility registry ────────────────────────────→ note 10 (oc_plugins_compatibility)
├── Plugin inspector package ──────────────────────────→ note 10
│   └── Maintainer acceptance lane ────────────────────→ note 10
├── Deprecation policy ────────────────────────────────→ note 10
├── Release notes ─────────────────────────────────────→ note 10
├── Current compatibility areas ───────────────────────→ note 11 (oc_plugins_compatibility_areas)
│   ├── WhatsApp Inbound Callback Flat Aliases ────────→ note 11
│   └── WhatsApp Inbound Admission Fields ─────────────→ note 11
```
No orphaned sections. Source `## Related` nav blocks are dropped (replaced by each note's `## Related Notes`).
The `/reference/code-mode`, Peekaboo, ACP/acpx, and provider-auth-precedence pointers are link-outs, not
digested content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| codex-harness.md (5,249w, 11 H2 / 3 H3, 16 code) | notes 2 + 3 + 4 | 2.1× the 2,500w cap AND three distinct procedural task clusters: (a) enable+configure+verify (setup), (b) deployment patterns + app-server policy (deploy/policy), (c) commands/diagnostics/troubleshooting (operate). Splitting keeps each ≤700w, ≤6 code blocks, single-task. |
| codex-harness-reference.md (3,137w, 12 H2, 10 code) | notes 5 + 6 | exceeds 2,500w; cleanly separates *declarative config surface* (config fields, transport, approval/sandbox modes, model discovery, bootstrap, env overrides → note 5) from *runtime-execution reference* (sandboxed native exec, auth/env isolation, dynamic-tool bridging, timeouts → note 6). Both are model BB (reference schema). |
| compatibility.md (1,305w, 7 H2 / 3 H3, 2 code) | notes 10 + 11 | under the word cap but two distinct model surfaces: the *policy/lifecycle model* (registry, inspector, acceptance lane, deprecation, release notes → note 10) vs the *concrete per-area schema shims* (WhatsApp inbound callback aliases + admission fields → note 11). Split keeps each focused; matches the master's 11-note estimate. Borderline by size — split promoted per CP6 to avoid a mixed-topic note. |

The other 4 pages (codex-computer-use 1,937w; codex-harness-runtime 2,290w; codex-native-plugins 1,673w;
community 366w) are each ≤2,500w and single-BB → **1 note each, no split.**

## Summary Statistics & Building Block Distribution

- Source pages: **7** (15,957 words, 45 code-fence pairs). New `oc_*` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×6** (notes 1, 2, 3, 4, 8, 9) · **model ×4** (notes 5, 6, 10, 11) · **concept ×1** (note 7).
- Est. digest words: ~6,600 (avg ~600/note); none approaches the 2,500w cap. 45 source fence-pairs distribute
  across the procedure/model notes; each note kept ≤6 (config/CLI snippets reproduced selectively, verbatim).
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** every note maps **≥8 relevancy-selected
  `(planned, this series)`), PLUS relevant `repo_openclaw*`. Each link carries a per-link relevance statement.
  See **`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`** for the locked per-note table.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Relative paths from a note at `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`,
> snippet → `../../code_snippets/`, sibling `oc_*` (this series) → `oc_Y.md` `(planned, this series)`,
> cc/pi/hermes doc → `../<folder>/`, repo → `../../../areas/code_repos/`, entry → `../../../0_entry_points/`.

### oc_plugins_codex_computer_use (8t · 11s · 10d)

**Terms** (8)
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool/server interface; relevance: Computer Use is a Codex-native MCP plugin (`computer-use` MCP server) that OpenClaw checks for availability before a turn.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: desktop control runs under Codex permissions and the host's macOS permission grants, not OpenClaw's own exec.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of callable tools; relevance: OpenClaw verifies the MCP server exposes tools (`computer-use.list_apps`) and reloads MCP servers on install.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-issued structured tool calls; relevance: Codex owns the native MCP tool calls during Codex-mode turns; OpenClaw only prepares them.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text + image/screen modalities; relevance: desktop control inspects and acts on screen state — a multimodal capability requiring Screen Recording grants.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agentic coding tools (Codex/Claude Code); relevance: Computer Use extends a Codex-mode OpenClaw agent's action surface to the local desktop.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime executing agent turns; relevance: Computer Use is only available when OpenClaw runs the native Codex harness.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway; relevance: subject system — OpenClaw prepares (does not vendor/execute) the plugin and fails closed when `computerUse.enabled` is true.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_computer_use](../claude_code/cc_computer_use.md) — Anthropic's computer-use tool; relevance: closest sibling-tool analog (screenshot/click/type desktop control via a coding agent).
- [cc_computer_use_safety](../claude_code/cc_computer_use_safety.md) — computer-use safety/permission guidance; relevance: parallels the macOS Accessibility/Screen-Recording permission + fail-closed posture this note documents.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — Hermes macOS computer-use setup; relevance: the macOS-permission-gated desktop-control flow in a sibling coding-agent gateway.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managing MCP server config; relevance: analog for the `marketplaceSource`/`marketplacePath`/`marketplaceName` MCP-install config this note covers.
- [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — installing/enabling/reloading MCP servers; relevance: mirrors OpenClaw's install/re-enable/reload-MCP-servers status machine (`disabled`/`mcp_missing`/`ready`).
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — registering custom MCP/agent tools; relevance: analog for the `openclaw mcp set cua-driver` direct-MCP alternative path.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — enabling the native Codex harness; relevance: prerequisite — Computer Use needs the harness running first.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — native Codex plugin management; relevance: same Codex app-server plugin-install machinery, different plugin class.
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — the `computerUse` config surface lives in the harness config reference.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — `Native hook relay unavailable` troubleshooting ties to the native hook/relay runtime contract.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — Codex/agent runtime code; relevance: the agent-runtime side that drives Codex-mode turns where Computer Use is prepared.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the bundled `codex` plugin that hosts the `computerUse` setup lives here.

**Snippets** (11)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider wiring; relevance: Computer Use runs on `openai/gpt-*` Codex-mode turns.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog assembly; relevance: how the `computer-use` MCP tools enter the agent's available-tool set.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool gating policy; relevance: fail-closed gating when the required MCP server is unavailable.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP loopback transport; relevance: the MCP-server transport plane the `computer-use` server attaches to.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/install lifecycle; relevance: the install/re-enable/reload steps this note's setup machine performs.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: marketplace plugin shape that `pluginName`/`mcpServerName` select.
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — macOS app surface lifecycle; relevance: the macOS host context (permissions, app bundle) Computer Use depends on.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denial; relevance: the fail-closed safety posture around native desktop-control tools.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — registering agent tools; relevance: analog for exposing native plugin tools into the agent turn.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: contrasts with the iOS-node `canvas.*/camera.*/screen.*` path this note distinguishes from Computer Use.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS node pairing; relevance: the iOS-app-as-node path explicitly contrasted with desktop Computer Use.

### oc_plugins_codex_harness_setup (8t · 12s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway; relevance: the bundled `codex` plugin lets OpenClaw run embedded OpenAI turns through Codex app-server.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime executing agent turns; relevance: this note enables/configures the Codex app-server harness vs OpenClaw's built-in harness.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agentic coding tools; relevance: Codex is the OpenAI coding-agent runtime being enabled.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: quickstart signs in with ChatGPT/Codex OAuth via `openclaw models auth login --provider openai`.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: `auth.order.openai` subscription-first/API-key-backup ordering.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: `openai/gpt-*` is the model ref routed through Codex.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: contrasted as the non-Codex default in mixed deployments; provider/model names documented as config not terms.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin abstraction; relevance: `plugins.entries.codex` is the provider-plugin enabling Codex runtime.

**Docs** (10: 6 existing + 4 planned-sibling)
- [pi_provider_auth](../pi/pi_provider_auth.md) — subscription-vs-key provider auth; relevance: direct analog for the OAuth-subscription-first / API-key-backup auth ordering.
- [cc_model_selection](../claude_code/cc_model_selection.md) — selecting model refs; relevance: analog for `agents.defaults.model: "openai/gpt-5.5"` model-ref selection.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Hermes Codex runtime setup; relevance: the closest sibling-gateway Codex-runtime enable-and-verify quickstart.
- [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — provider/model config; relevance: analog for the provider-backed model-config quickstart pattern.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: analog for routing model refs to a specific provider runtime.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback model config; relevance: analog for the API-key-backup auth fallback (not a runtime switch).
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — full config-field reference for the fields introduced in setup.
- [oc_plugins_codex_harness_deployment](oc_plugins_codex_harness_deployment.md) `(planned, this series)` — deployment patterns building on the quickstart config.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — the runtime contract that the verified harness obeys.
- [oc_plugins_codex_harness_diagnostics](oc_plugins_codex_harness_diagnostics.md) `(planned, this series)` — `/codex status`/`/status` verification commands continue here.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/Codex runtime code; relevance: the runtime-resolution code that maps `openai/gpt-*` to the Codex harness.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/setup wizard; relevance: `openclaw models auth login` + `openclaw doctor --fix` live on the CLI side.

**Snippets** (12)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the provider whose `openai/gpt-*` refs resolve to Codex.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: how `agentRuntime.id`/`plugins.entries.codex.enabled` resolve the harness.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering; relevance: implements `auth.order.openai` subscription-first/API-key-backup.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: the ChatGPT/Codex OAuth profile the quickstart creates.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: Codex app-server account vs OpenClaw auth-profile precedence.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: `openai/gpt-*` model availability for agent config.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery normalize; relevance: `/codex models` live catalog the setup verifies.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: the Claude default in mixed-provider setups.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: gateway restart after plugin config change.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup-wizard config write; relevance: how `plugins.entries.codex` config is authored.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Hermes Codex runtime; relevance: sibling impl of resolving and running a Codex runtime.
- [snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md) — Codex CLI switch; relevance: analog for switching an agent to the Codex runtime.

### oc_plugins_codex_harness_deployment (8t · 11s · 10d)

**Terms** (8)
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent-turn runtime; relevance: deployments choose whether Codex or OpenClaw owns the harness.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: app-server policy sets `sandbox: danger-full-access`/`workspace-write`/`read-only` per deployment.
- [Model Router](../../term_dictionary/term_model_router.md) — routes refs to providers/runtimes; relevance: mixed-provider deployment routes `anthropic/*` and `openai/*` to different runtimes.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback across models; relevance: fail-closed vs auto-fallback runtime policy (`agentRuntime.id: "codex"`).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding-agent runtimes; relevance: per-agent Codex vs Claude assignment.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider abstraction; relevance: `models.providers.openai.agentRuntime` provider-level policy.
- [Guardian](../../term_dictionary/term_guardian.md) — review/approval gate; relevance: app-server policy maps `tools.exec.mode: "auto"` to Codex guardian-reviewed approvals.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — fail-closed means OpenClaw errors instead of embedded fallback.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_model_selection](../claude_code/cc_model_selection.md) — model-ref selection; relevance: analog for per-agent model assignment in mixed deployments.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud-provider config; relevance: mixed-provider deployment config analog.
- [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — permission/approval modes; relevance: analog for the app-server approval-policy posture per deployment.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — sandbox modes; relevance: analog for `danger-full-access`/`workspace-write` sandbox selection.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission policy; relevance: the approval-policy-vs-sandbox split the app-server policy section makes.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Hermes Codex runtime; relevance: sibling deployment of a Codex runtime alongside other providers.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — the base config these deployment shapes extend.
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — `appServer.mode`/`approvalPolicy`/`sandbox` field reference.
- [oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md) `(planned, this series)` — sandboxed-native-exec behavior under each deployment.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — runtime contract these deployments operate under.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: per-agent runtime assignment and fail-closed resolution code.

**Snippets** (11)
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config resolution; relevance: implements `agentRuntime.id` fail-closed vs auto.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — per-agent scope; relevance: mixed-provider per-agent (`main` Claude, `codex` GPT) config.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: contrast with fail-closed (no fallback) Codex deployment.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: usage-limit reset/cooldown handling per auth profile.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error path; relevance: the fail-closed error surfaced when Codex is unavailable.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: app-server policy maps `tools.exec.mode` to approval behavior.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: sandbox modes (`workspace-write`/`read-only`) the policy section selects.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: the Claude default in mixed-provider deployment.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the Codex-routed `openai/*` provider.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy gating; relevance: sandbox-active turns disable native code mode / route through `sandbox_exec`.
- [snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md) — Codex runtime switch; relevance: analog for selecting the Codex runtime for an agent.

### oc_plugins_codex_harness_diagnostics (8t · 11s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: `/codex` chat commands and `/diagnostics` are OpenClaw runtime surfaces.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: diagnostics inspect a Codex-harness deployment.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript compaction; relevance: `/codex compact` starts native Codex compaction.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding-agent runtime; relevance: `codex resume <thread-id>` inspects native Codex threads.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: `/codex mcp`/`/codex skills` list the tool surfaces of a thread.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: `/codex status` reports MCP servers and skills.
- [MCP](../../term_dictionary/term_mcp.md) — MCP servers; relevance: `/codex mcp` lists Codex app-server MCP server status.
- [Trajectory](../../term_dictionary/term_trajectory.md) — recorded agent run trace; relevance: diagnostics/feedback upload and app-server trajectory capture for debugging. (`term_session`/`term_transcript` appear in source but are NOT in DB — link existing terms only; see Undigested Terms Plan.)

**Docs** (10: 5 existing + 5 planned-sibling)
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Hermes Codex runtime tools; relevance: sibling `/codex`-style command/tool inspection surface.
- [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — session management; relevance: analog for resuming/inspecting agent threads.
- [cc_sessions](../claude_code/cc_sessions.md) — session model; relevance: the thread/session inspection (`/codex threads`, `codex resume`) maps to session lifecycle.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session lifecycle events; relevance: `/new`/`/reset` recovery flow referenced in troubleshooting.
- [hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md) — CLI session ops; relevance: analog for the `/codex`/`/diagnostics` chat-command surface.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — runtime-boundary summary; the full boundary contract lives here.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — `/status`/`/codex status` verification originate in setup.
- [oc_plugins_codex_computer_use](oc_plugins_codex_computer_use.md) `(planned, this series)` — `/codex computer-use status` is part of the diagnostics surface.
- [oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md) `(planned, this series)` — timeout diagnostics fields reference.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — `/codex plugins list` diagnostics overlap.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: `/codex` command + diagnostics handlers live here.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/thread state; relevance: thread binding and transcript-mirror inspection.

**Snippets** (11)
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: registration of `/codex` slash commands.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: `/new`/`/reset` thread-binding refresh.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: the transcript-mirror inspection surface.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compact/reset; relevance: `/codex compact` and `/reset` mechanics.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — reset helpers; relevance: clearing stale native thread bindings on reset.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair; relevance: `openclaw doctor --fix` legacy-ref repair referenced in troubleshooting.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency status; relevance: `/codex status` rate-limit/account reporting.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — event ledger; relevance: app-server trajectory/event capture for diagnostics.
- [snippet_hermes_agent_cli_codex_migrate](../../code_snippets/snippet_hermes_agent_cli_codex_migrate.md) — Codex CLI migrate; relevance: analog for Codex thread/diagnostics CLI ops.
- [snippet_hermes_agent_cli_hermescli_session_handlers](../../code_snippets/snippet_hermes_agent_cli_hermescli_session_handlers.md) — CLI session handlers; relevance: analog for `/codex threads`/`resume` session handlers.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — chat abort; relevance: interrupting a stale native turn (timeout/abort) during diagnostics.

### oc_plugins_codex_harness_reference_config (8t · 12s · 10d)

**Terms** (8)
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin abstraction; relevance: all settings live under `plugins.entries.codex.config`.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin config/manifest schema; relevance: the declarative config-field surface this reference enumerates.
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: `approvalPolicy`/`sandbox`/`mode` (YOLO vs guardian) fields.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: `authToken`/SecretInput for WebSocket transport.
- [WebSocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: `transport: "websocket"` + `url`/`headers` app-server transport.
- [Model Router](../../term_dictionary/term_model_router.md) — model routing/discovery; relevance: `discovery` model-list config and bundled fallback catalog.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — the OpenClaw config surface for the Codex harness.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: every field tunes the Codex app-server harness.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugin config; relevance: analog for the plugin-config-surface schema this note documents.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component structure; relevance: analog for the structured `config.*` field hierarchy.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — provider registration/config reference; relevance: config-reference analog (fields, defaults, enums).
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed MCP config; relevance: analog for transport/auth config of an app-server-style service.
- [cc_sandbox_settings](../claude_code/cc_sandbox_settings.md) — sandbox settings; relevance: analog for `sandbox`/`approvalPolicy`/`mode` config fields.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — config precedence; relevance: analog for `mode` preset vs individual-field override precedence.
- [oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md) `(planned, this series)` — the runtime-execution half of the reference (exec/isolation/timeouts).
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — the minimal config this reference expands.
- [oc_plugins_codex_harness_deployment](oc_plugins_codex_harness_deployment.md) `(planned, this series)` — deployment shapes that combine these fields.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — runtime contract the config governs.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the bundled `codex` plugin config schema lives here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: app-server transport/discovery consumed by the runtime.

**Snippets** (12)
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: `plugins.entries.codex.config` shape.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config wiring; relevance: how the codex plugin config is loaded.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: config changes requiring restart/reload.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload plan; relevance: planning a config-change reload.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalize; relevance: `discovery` model-list config and bundled fallback catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model manifest planner; relevance: how discovered/fallback models populate the catalog.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: `authToken`/`headers` SecretInput resolution before app-server start.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WebSocket connection; relevance: `transport: "websocket"` app-server connect.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen; relevance: the WS transport plane for a remote app-server.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — workspace bootstrap injection; relevance: `SOUL.md`/`IDENTITY.md`/`TOOLS.md`/`USER.md` bootstrap-file forwarding.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity; relevance: workspace personality/identity files forwarded as developer instructions.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `OPENCLAW_CODEX_APP_SERVER_*` environment overrides.

### oc_plugins_codex_harness_reference_runtime (8t · 12s · 10d)

**Terms** (8)
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: sandboxed native exec — active OpenClaw sandboxing disables native Codex exec surfaces / `experimental.sandboxExecServer`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: auth-selection order and ChatGPT-subscription key stripping.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: subscription auth profile vs `CODEX_API_KEY`/`OPENAI_API_KEY` env fallback.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: OpenClaw dynamic-tool bridging into the app-server `item/tool/call`.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: `searchable` vs `direct` dynamic-tool loading and excluded native-duplicate tools.
- [Guardian](../../term_dictionary/term_guardian.md) — review gate; relevance: guardian-reviewed approvals and bwrap/AppArmor host-policy notes.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — auth/env isolation between OpenClaw and Codex home (`CODEX_HOME`).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: runtime-execution reference for the Codex harness.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — custom tool definition; relevance: analog for OpenClaw dynamic-tool registration/bridging into the harness.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox FS/network isolation; relevance: analog for `networkProxy`/sandboxed-exec network/filesystem isolation.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime/containers; relevance: analog for the sandbox-backed exec-server preview path.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Hermes Codex runtime tools; relevance: sibling dynamic-tool/native-tool runtime surface.
- [pi_security_model](../pi/pi_security_model.md) — security/isolation model; relevance: analog for auth/env isolation and key-stripping posture.
- [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — tool approval handling; relevance: analog for per-call timeout/approval and dynamic-tool watchdog.
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — the declarative config half of the reference.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — the prose runtime contract these mechanics implement.
- [oc_plugins_codex_harness_deployment](oc_plugins_codex_harness_deployment.md) `(planned, this series)` — deployments that toggle sandboxed exec/isolation.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — `clearEnv`/`CODEX_HOME` isolation introduced from setup auth.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: dynamic-tool bridging + timeout watchdog code.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox/exec security; relevance: sandboxed-native-exec, `sandbox_exec`/`sandbox_process`, env isolation.

**Snippets** (12)
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: `searchable` vs `direct` dynamic-tool loading and the `openclaw` namespace.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: excluded native-duplicate tools (`read`/`write`/`exec`/`apply_patch`).
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: sandbox-active disables native Code Mode / routes through sandbox tools.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: fail-closed when sandbox exec cannot register.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestrator; relevance: `sandbox_exec`/`sandbox_process` execution path.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: sandboxed native execution boundary.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: auth-profile vs env-key selection and stripping.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering; relevance: the 3-step auth-selection order this note documents.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: `CODEX_HOME`/`HOME`/`clearEnv` child-process env normalization.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP loopback; relevance: local loopback exec-server registration with app-server.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window/timeout guard; relevance: per-phase timeout watchdog semantics.
- [snippet_hermes_agent_core_tool_dispatch_helpers](../../code_snippets/snippet_hermes_agent_core_tool_dispatch_helpers.md) — tool dispatch helpers; relevance: analog for dynamic-tool dispatch/timeout into a runtime.

### oc_plugins_codex_harness_runtime (9t · 11s · 10d)

**Terms** (9)
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the OpenClaw-owns-vs-Codex-owns boundary is the core of this concept note.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — mid-run steering; relevance: queue steering maps onto Codex app-server `turn/steer`.
- [Compaction](../../term_dictionary/term_compaction.md) — transcript compaction; relevance: Codex owns native compaction; OpenClaw keeps only a transcript mirror.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — wake/heartbeat turns; relevance: heartbeat turns get `heartbeat_respond` and collaboration-mode instructions.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: native tool continuation owned by Codex; OpenClaw dynamic tools still execute.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: hook layers and supported native-tool block/observe surfaces.
- [MCP](../../term_dictionary/term_mcp.md) — MCP elicitations; relevance: Codex MCP tool approval elicitations route through OpenClaw's plugin approval flow.
- [Message Queue](../../term_dictionary/term_message_queue.md) — queued messages; relevance: queue steering batches steer-mode chat messages into one `turn/steer`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — what OpenClaw still owns (channels, sessions, delivery, mirror) vs Codex.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_computer_use](../claude_code/cc_computer_use.md) — native tool/elicitation; relevance: analog for native MCP elicitation/approval handling.
- [cc_hook_events_catalog](../claude_code/cc_hook_events_catalog.md) — hook events catalog; relevance: analog for the three hook layers (`PreToolUse`/`PostToolUse`/`PermissionRequest`/`Stop`).
- [cc_async_hooks](../claude_code/cc_async_hooks.md) — async hook observations; relevance: analog for `after_tool_call` async observations that cannot block.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — ACP runtime internals; relevance: sibling native-runtime boundary contract (what the host owns vs the agent).
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Hermes Codex runtime tools; relevance: sibling Codex native-loop tool/permission boundary.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool surface; relevance: native shell/patch/MCP tools Codex owns vs OpenClaw dynamic tools.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — setup of the harness whose runtime contract this defines.
- [oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md) `(planned, this series)` — the config-field mechanics behind these contract points.
- [oc_plugins_codex_harness_diagnostics](oc_plugins_codex_harness_diagnostics.md) `(planned, this series)` — runtime-boundary summary + feedback-upload pointer.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — native-plugin elicitations route through this runtime's approval path.

**Repos** (3)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the harness adapter implementing the ownership boundary.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/transcript; relevance: the transcript mirror OpenClaw keeps for channel history.

**Snippets** (11)
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript; relevance: the transcript-mirror contract for native turns.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hooks request handler; relevance: OpenClaw plugin-hook layer around native turns.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hook config payload; relevance: per-thread native hook config injection (`PreToolUse`/`Stop`).
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: native permission/approval bridge after Codex review.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — permission relay; relevance: analog for the native-hook permission relay (`PermissionRequest` opt-in).
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat buffering; relevance: heartbeat turns + visible-reply delivery contract.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: `messages.visibleReplies` automatic-final vs `message_tool` delivery.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compact/reset; relevance: native compaction start (`thread/compact/start`) without OpenClaw waiting.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media/transcript pipeline; relevance: OpenClaw-owned media delivery for native image-gen items.
- [snippet_openclaw_acp_manager_turn_stream](../../code_snippets/snippet_openclaw_acp_manager_turn_stream.md) — turn stream; relevance: analog for queue steering / turn-level event streaming.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Codex runtime; relevance: sibling native-model-loop ownership impl.

### oc_plugins_codex_native_plugins (8t · 11s · 10d)

**Terms** (8)
- [MCP](../../term_dictionary/term_mcp.md) — MCP execution; relevance: Codex app-server owns the app-backed MCP execution for native plugins.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin identity/manifest; relevance: migration writes explicit `marketplaceName`/`pluginName` plugin identities.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin framework; relevance: native Codex plugin/app capabilities vs OpenClaw plugin SDK.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin abstraction; relevance: `codexPlugins` is the native-plugin enablement surface inside `plugins.entries.codex`.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool catalog; relevance: thread app config (`config.apps`) controls which plugin app tools are exposed.
- [Guardian](../../term_dictionary/term_guardian.md) — approval gate; relevance: destructive-action policy + ownership-proven MCP approval elicitations.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — managing native Codex plugins from OpenClaw chat (`/codex plugins`).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding-agent runtime; relevance: native plugins run inside the same Codex thread as the OpenClaw turn.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugins; relevance: analog for enabling/configuring plugins for an agent runtime.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: analog for plugin/app inventory and ownership mapping.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin policy; relevance: analog for enable/disable + destructive-action policy.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in plugins; relevance: sibling native-plugin enablement model.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — plugin tutorial; relevance: analog for plugin install/eligibility flow.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace install; relevance: analog for `openai-curated` marketplace install/migration.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — the base harness this builds on.
- [oc_plugins_codex_computer_use](oc_plugins_codex_computer_use.md) `(planned, this series)` — Computer Use uses the same Codex plugin-install machinery.
- [oc_plugins_community](oc_plugins_community.md) `(planned, this series)` — community/marketplace plugin discovery counterpart.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — plugin approval elicitations route through the runtime contract.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the `codexPlugins` config + migration code lives here.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app inventory/packaging; relevance: `app/list` inventory, ownership mapping, app config patches.

**Snippets** (11)
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: installed/enabled/accessible state machine.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: plugin identity (`marketplaceName`/`pluginName`).
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: `codexPlugins.plugins.*` config entries.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: thread-app-config computation at session establish.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config impl; relevance: `/codex plugins enable/disable` writes to OpenClaw config only.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolver; relevance: ownership-proven mapping (exact app id / MCP server name).
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — trust findings; relevance: ambiguous-ownership exclusion until inventory refresh.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: destructive-action elicitation → OpenClaw plugin approval.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: `openclaw migrate codex` plugin-eligibility migration.
- [snippet_hermes_agent_cli_codex_migrate](../../code_snippets/snippet_hermes_agent_cli_codex_migrate.md) — Codex migrate CLI; relevance: analog for the migrate-plugins-from-Codex-home flow.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command catalog; relevance: `/codex plugins` chat-command registration.

### oc_plugins_community (8t · 10s · 10d)

**Terms** (8)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest; relevance: publishing requires package metadata + a plugin manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin framework; relevance: community plugins are built on the plugin SDK / building-plugins workflow.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — community plugins extend OpenClaw with channels/tools/providers/hooks.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding-agent runtime; relevance: plugins extend the coding-agent gateway's capability set.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin abstraction; relevance: community plugins can add providers/channels/tools.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — package/skill manifest; relevance: ClawHub validates owner scope, package name, version, file limits, source metadata.
- [Deprecation](../../term_dictionary/term_deprecation.md) — lifecycle policy; relevance: ClawHub release review/verification gating before public install.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugins; relevance: analog for the plugin packaging/build workflow.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: analog for the package shape (manifest, metadata, docs).
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace install; relevance: analog for ClawHub `install`/`search` discovery surface.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin source selection; relevance: analog for `clawhub:`/`npm:` install source prefixes.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — publishing skills/packages; relevance: sibling publish-workflow contract (owner, review, release).
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — build plugin tutorial; relevance: analog for the build-before-publish plugin workflow.
- [oc_plugins_compatibility](oc_plugins_compatibility.md) `(planned, this series)` — the compatibility/inspector gate published plugins must pass.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — native-plugin install counterpart.
- [oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md) `(planned, this series)` — bundled-plugin enablement context for community plugins.
- [oc_plugins_compatibility_areas](oc_plugins_compatibility_areas.md) `(planned, this series)` — concrete compatibility shims published plugins must honor.

**Repos** (1)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the SDK/package shape community plugins build against.

**Snippets** (10)
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: the package metadata/manifest a publish requires.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: install/enable/uninstall after discovery.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the SDK entrypoints a community plugin implements.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command catalog; relevance: `openclaw plugins search/install` CLI commands.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: routing of `plugins`/source-prefixed install subcommands.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — plugin runtime load; relevance: loading an installed community plugin into the gateway.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill/package scanner; relevance: ClawHub scan status / review-before-publish gating.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust; relevance: source/owner trust validation for installed plugins.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup imports; relevance: importing/registering an installed plugin during setup.

### oc_plugins_compatibility (8t · 10s · 10d)

**Terms** (8)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest; relevance: the inspector validates manifest/schema + contract compatibility version.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: SDK/manifest/setup/config/runtime contracts evolve behind compatibility adapters.
- [Deprecation](../../term_dictionary/term_deprecation.md) — deprecation policy; relevance: the 7-step migration sequence + ≤3-month removal window.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin abstraction; relevance: registry owner categories include provider/channel/plugin-execution.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — core compatibility registry at `src/plugins/compat/registry.ts`.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — package manifest; relevance: the plugin-inspector consumes manifest contracts/fixtures.
- [Guardian](../../term_dictionary/term_guardian.md) — review/acceptance gate; relevance: the Crabbox/Blacksmith Testbox maintainer acceptance lane.

**Docs** (10: 6 existing + 4 planned-sibling)
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: analog for plugin validation/structure the inspector checks.
- [cc_sdk_plugin_structure](../claude_code/cc_sdk_plugin_structure.md) — plugin structure; relevance: analog for manifest/schema validation surface.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — manifest schema; relevance: analog for the versioned manifest contract being validated.
- [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin caching/troubleshooting; relevance: analog for compatibility-warning + cold-path import checks.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: analog for the external-package acceptance/security lane.
- [hermes_creating_skill_format](../hermes_agent/hermes_creating_skill_format.md) — package/skill format contract; relevance: sibling versioned package-format/validation contract.
- [oc_plugins_compatibility_areas](oc_plugins_compatibility_areas.md) `(planned, this series)` — the concrete per-area shims this registry tracks.
- [oc_plugins_community](oc_plugins_community.md) `(planned, this series)` — publishing flow gated by inspector/compatibility.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — native-plugin contracts under the same compatibility regime.
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — config contracts that compatibility adapters migrate (`agentRuntime`, doctor).

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the compatibility registry + SDK export map live here.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/package surface; relevance: plugin-inspector package + bundled extension import boundaries.

**Snippets** (10)
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package contract; relevance: the manifest/contract the inspector validates.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entries; relevance: SDK export-map/import-boundary guards in compatibility.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: compatibility adapters keep old plugin behavior wired through lifecycle.
- [snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md) — registry compat shim; relevance: concrete named-compatibility-adapter pattern.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scanner; relevance: inspector-style manifest/schema validation.
- [snippet_openclaw_opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — compile/validate; relevance: analog for the CI validation/annotation (`--json`) the inspector emits.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime load; relevance: load-path/allowlist compatibility behavior.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — trust resolver; relevance: install/source metadata checks the inspector performs.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair; relevance: doctor migration/deprecation-compat tracked separately from runtime compat.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: migration-compat shims for old config/install shapes.

### oc_plugins_compatibility_areas (8t · 10s · 10d)

**Terms** (8)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — manifest/SDK aliases; relevance: compatibility areas include legacy SDK imports/aliases plugins migrate from.
- [Deprecation](../../term_dictionary/term_deprecation.md) — deprecation window; relevance: each flat-alias/admission-field set has a dated removal window (2026-08-30).
- [WebSocket](../../term_dictionary/term_websocket.md) — inbound transport; relevance: WhatsApp inbound runtime callbacks (`WebInboundMessage`) carry the flat-alias fields.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured RPC payloads; relevance: the nested callback envelope (`event`/`payload`/`platform`) is the structured contract shape.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/channel plugin; relevance: areas cover legacy provider/channel hooks and env-var manifest metadata.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway; relevance: subject — the concrete per-area compatibility shims OpenClaw tracks.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: areas include `openclaw/plugin-sdk/*` subpath/alias migrations.
- [Authentication](../../term_dictionary/term_authentication.md) — admission/access-control; relevance: WhatsApp inbound `admission` envelope wraps the access-control decision (`ingress.decision`).

**Docs** (10: 5 existing + 5 planned-sibling)
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: analog for compatibility-field/component migration.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — manifest schema; relevance: analog for legacy-vs-nested schema field migration.
- [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — channel permission relay; relevance: analog for channel admission/access-control field handling.
- [cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md) — channel reply tool; relevance: analog for the flat `reply(...)`/`sendMedia(...)` → `platform` context migration.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — platform/channel adapter plugin; relevance: sibling channel-adapter inbound-message contract.
- [oc_plugins_compatibility](oc_plugins_compatibility.md) `(planned, this series)` — the registry/policy parent this details the areas of.
- [oc_plugins_community](oc_plugins_community.md) `(planned, this series)` — published plugins must honor these schema-level shims.
- [oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md) `(planned, this series)` — native-plugin config under the same compatibility regime.
- [oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md) `(planned, this series)` — `agentRuntime` legacy-config migration is one tracked area.
- [oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md) `(planned, this series)` — runtime-alias compatibility (`api.runtime.*`) areas.

**Repos** (2)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel runtime; relevance: WhatsApp inbound `WebInboundMessage`/`admission` callback contract lives here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: the legacy SDK aliases/import-boundary areas.

**Snippets** (10)
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the inbound-message contract whose flat aliases are being migrated.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: `conversationId`/`chatId` → `admission.conversation.*` migration.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding/routing; relevance: callback routing across the nested vs flat envelope.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM allowlist/admission; relevance: `accessControlPassed`/`admission.ingress.decision` access-control field.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolver; relevance: resolving sender/group fields moving under `platform`/`group`.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — registry normalize; relevance: normalizing legacy vs registry-first channel config metadata (a tracked area).
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — kernel dispatch; relevance: dispatch over the inbound callback envelope.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread bindings; relevance: conversation/group context fields in callbacks.
- [snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md) — registry compat shim; relevance: the named-compatibility-adapter pattern these areas use.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entries; relevance: legacy `openclaw/plugin-sdk/*` alias subpaths being migrated.

> **DB-verification (lock time, 2026-06-21):** every EXISTING `note_id` above was confirmed present via
> `oc_*` docs are this-series planned (not yet in DB) and counted toward the 10-doc floor as
> **NOT in DB (deliberately NOT cited as existing — OpenClaw doc-page vocabulary digested as `oc_*` / linked to
> nearest existing term):** `term_codex`, `term_computer_use`, `term_agent_runtime`, `term_agent_loop`,
> `term_session`, `term_transcript`, `term_system_prompt`, `term_queue_steering`, `term_marketplace`,
> `term_plugin_registry`, `term_approval`, `term_permission_model`, `term_diagnostics`.

## Undigested Terms Plan (Step 4e)

pl02 creates **0 new `term_dictionary` notes** (per master's corpus-wide ownership decision — OpenClaw vocab is
the subject of doc pages, digested as `oc_*` concept/procedure notes, not promoted to term entries).

| Term (appearing in source) | Disposition |
|---|---|
| Codex harness / Codex app-server | → `oc_*` doc notes (notes 2–7); link `term_agent_harness`, `term_autonomous_coding_agents`. No new term. |
| Codex Computer Use / cua-driver MCP | → `oc_plugins_codex_computer_use` (note 1); link `term_mcp`, `term_multimodal`. No new term. |
| Agent runtime / native model loop / runtime boundary | → `oc_plugins_codex_harness_runtime` (note 7) concept note; link `term_agent_harness`. (`term_agent_runtime` not in DB — owned by concepts sub-plan `co01` `concepts/agent-runtimes`; do NOT pre-empt here.) |
| Queue steering | → note 7 body; link `term_message_queue` + `term_agent_steering`. (`term_queue_steering` not in DB — owned by concepts `co06` `concepts/queue-steering`.) |
| Native Codex plugins / native MCP plugin | → `oc_plugins_codex_native_plugins` (note 8); link `term_mcp`, `term_plugin_manifest`, `term_plugin_sdk`. No new term. |
| Compatibility registry / deprecation policy / acceptance lane | → notes 10–11; link `term_deprecation`, `term_plugin_manifest`. No new term. |
| Provider/model names (OpenAI, ChatGPT, gpt-5.5, Codex) | Documented as config only; link `term_llm`/`term_claude`/`term_autonomous_coding_agents`. Not promoted to term notes. |
| ACP / acpx external harness | Link `term_acp_agent_client_protocol` (existing); covered in pl05 / cli. Link-out, not digested here. |
| Session / transcript / system prompt / approval / diagnostics | Body vocabulary; link nearest existing term where one exists; otherwise plain prose. No new term (these have doc-page homes elsewhere in concepts/CLI). |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an
existing note. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — pl02 authors zero `term_dictionary` notes. (Inherited from master: any future new term

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P3). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order, `## Overview`/`## Related Notes`/`## References`, footer, one BB) | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to source page) | diff vs `inbox/openclaw_docs/plugins/<page>.md` |
| G3 | Density + Coverage (≤400L / ≤2,500w / ≤6 code; every H2/H3 mapped) | word/fence count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevancy terms + repo/sibling/doc, per-link relevance) | Related Notes audit |
| G6 | Broken-link fix (0 broken) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — outbound + indexed links present | `note_links` query |
| G8 | In-degree ≥1: each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | via `entry_openclaw_docs.md` + repo/term inlinks |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_codex_computer_use oc_plugins_codex_harness_setup oc_plugins_codex_harness_deployment oc_plugins_codex_harness_diagnostics oc_plugins_codex_harness_reference_config oc_plugins_codex_harness_reference_runtime oc_plugins_codex_harness_runtime oc_plugins_codex_native_plugins oc_plugins_community oc_plugins_compatibility oc_plugins_compatibility_areas"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G1 required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (body words, code-fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # G4 sibling cross-ref present
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) link in $n"
done

# G1 frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference sweep (every [text](x.md) target must exist)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"; [ -f "$f" ] || continue
  grep -oE '\]\([^)]+\.md\)' "$f" | sed -E 's/^\]\(|\)$//g' | while read -r tgt; do
    base=$(basename "$tgt")
  done
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2,500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_codex_computer_use | procedure | 650 | ≤6 | ✅ |
| 2 | oc_plugins_codex_harness_setup | procedure | 700 | ≤6 | ✅ |
| 3 | oc_plugins_codex_harness_deployment | procedure | 650 | ≤6 | ✅ |
| 4 | oc_plugins_codex_harness_diagnostics | procedure | 600 | ≤5 | ✅ |
| 5 | oc_plugins_codex_harness_reference_config | model | 700 | ≤6 | ✅ |
| 6 | oc_plugins_codex_harness_reference_runtime | model | 600 | ≤5 | ✅ |
| 7 | oc_plugins_codex_harness_runtime | concept | 700 | 0 | ✅ (source has 0 code) |
| 8 | oc_plugins_codex_native_plugins | procedure | 600 | ≤5 | ✅ |
| 9 | oc_plugins_community | procedure | 350 | ≤4 | ✅ |
| 10 | oc_plugins_compatibility | model | 600 | ≤2 | ✅ |
| 11 | oc_plugins_compatibility_areas | model | 450 | ≤2 | ✅ |

No note approaches caps. The two code-heavy source pages (codex-harness 16 fence-pairs, codex-harness-reference
10) are split so each derived note stays ≤6 code blocks (snippets reproduced selectively, verbatim).

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (CREATE'd as a master pre-step W1, >30-note series ⇒
required) under a "Plugins — Codex Harness & Ecosystem" cluster (sub-plan pl02). Each note receives its
entry-point back-link at finalization (satisfies G8). No new entry point created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; each EXISTING source below was

- `entry_openclaw_docs.md` `(planned, master pre-step)` → **all 11 notes** (primary G8 satisfier).
- `repo_openclaw_agents.md` → notes 1, 2, 3, 4, 5, 6, 7, 8 (Codex-harness agent runtime).
- `repo_openclaw_extensions.md` → notes 1, 5, 8, 9, 10, 11 (plugin/extension framework).
- `repo_openclaw_sessions.md` → notes 4, 7 (session/thread binding + diagnostics).
- `repo_openclaw_security.md` → note 6 (sandbox/auth isolation).
- `repo_openclaw_channels.md` → note 11 (WhatsApp inbound compatibility).
- `repo_openclaw_apps.md` → note 10 (plugin-inspector/app packaging).
- `term_mcp.md` → notes 1, 7, 8 (MCP plugin / native MCP elicitations).
- `term_agent_harness.md` → notes 2, 3, 5, 6, 7 (the harness concept).
- `term_provider_plugin.md` → notes 5, 8, 9, 10 (provider/plugin definition).
- `term_deprecation.md` → notes 10, 11 (deprecation policy / compatibility shims).

## Pacing Rules (inherited from master)

Single phase; cap dynamic-workflow fan-out at ~30 agents/run; embed the note manifest in the execution script
(`args` binding is unreliable). Re-read each source page before authoring; reproduce config/CLI snippets
+ G8 in-degree ≥1 before commit. `git pull --rebase --autostash origin main` before committing; commit + push
the wave in one cycle; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment, raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21 — 9/9 CP pass** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this run:** per-note Related Notes mapping LOCKED at the RAISED floors (≥8 `term_dictionary` terms ·
≥10 `code_snippets` · ≥10 docs under `resources/documentation/`, PLUS relevant `repo_openclaw*`), replacing the
prior pre-augment `## Candidate Cross-References` candidates. All 7 source pages were re-read

**What was locked — per-note counts (terms · snippets · docs[existing+planned-sibling] · repos):**

| # | Note | BB | Terms | Snippets | Docs (exist+sib) | Repos | Floors met (≥8t·≥10s·≥10d, ≥5 exist docs) |
|---|---|---|---:|---:|---|---:|---|
| 1 | oc_plugins_codex_computer_use | procedure | 8 | 11 | 10 (6+4) | 2 | ✅ |
| 2 | oc_plugins_codex_harness_setup | procedure | 8 | 12 | 10 (6+4) | 2 | ✅ |
| 3 | oc_plugins_codex_harness_deployment | procedure | 8 | 11 | 10 (6+4) | 2 | ✅ |
| 4 | oc_plugins_codex_harness_diagnostics | procedure | 8 | 11 | 10 (5+5) | 2 | ✅ |
| 5 | oc_plugins_codex_harness_reference_config | model | 8 | 12 | 10 (6+4) | 2 | ✅ |
| 6 | oc_plugins_codex_harness_reference_runtime | model | 8 | 12 | 10 (6+4) | 2 | ✅ |
| 7 | oc_plugins_codex_harness_runtime | concept | 9 | 11 | 10 (6+4) | 3 | ✅ |
| 8 | oc_plugins_codex_native_plugins | procedure | 8 | 11 | 10 (6+4) | 2 | ✅ |
| 9 | oc_plugins_community | procedure | 8 | 10 | 10 (6+4) | 1 | ✅ |
| 10 | oc_plugins_compatibility | model | 8 | 10 | 10 (6+4) | 2 | ✅ |
| 11 | oc_plugins_compatibility_areas | model | 8 | 10 | 10 (5+5) | 2 | ✅ |

`term_agent_harness`, `term_autonomous_coding_agents`, `term_function_calling`, `term_tool_registry`,
`term_sandbox`, `term_multimodal`, `term_llm`, `term_claude`, `term_oauth_token`, `term_authentication`,
`term_provider_plugin`, `term_model_router`, `term_model_failover`, `term_guardian`, `term_compaction`,
`term_agent_steering`, `term_heartbeat`, `term_message_queue`, `term_trajectory`, `term_plugin_manifest`,
`term_plugin_sdk`, `term_skill_manifest`, `term_deprecation`, `term_websocket`, `term_json_rpc`. (`term_guardian`,
candidate list.)

`_gateway_*`, `_sessions_*`, `_security_*`, `_channels_*`, `_plugin_*`, `_provider_*`, `_acp_*`, `_wizard_*`,
`_cli_*`, `_context_engine_*`, `_model_catalog_*`, `_macos_*`, `_ios_*`), plus
`snippet_hermes_agent_core_codex_runtime` / `_cli_codex_switch` / `_cli_codex_migrate` /
`_cli_hermescli_session_handlers` / `_core_tool_dispatch_helpers` / `_acp_tools_register` and

**Doc corpus used:** EXISTING `cc_*` (claude_code — sandbox/hooks/MCP/computer-use/plugins/model-selection/
sessions/subagents/channel), `pi_*` (provider auth/cloud-providers/custom-provider/extensions/security),
`hermes_*` (codex_runtime_setup/codex_runtime_tools/computer_use_macos/acp_internals/built_in_plugins/
creating_skill_*/config_precedence/build_plugin_tutorial/cli_commands_session_ops) — the rich coding-agent
doc corpora the master's Dedup Policy points at; PLUS the 11 sibling `oc_*` docs of this series
`(planned, this series)`, each counted toward the 10-doc floor with ≥5 existing docs guaranteed per note.

**New-term candidates:** **NONE.** Re-scan (augment Step 2d) of all 7 pages confirms every OpenClaw-specific
term that is the subject of a doc page (Codex harness, Codex app-server, Codex Computer Use / cua-driver,
agent runtime, native model loop, queue steering, native Codex plugins, compatibility registry, deprecation
policy, plugin inspector, app inventory, thread app config, WhatsApp inbound callback/admission) is digested
as an `oc_*` doc note per the master's corpus-wide ownership decision — NOT promoted to a `term_dictionary`
entry — and links the nearest existing term. Body vocabulary lacking an existing term (`session`, `transcript`,
`system_prompt`, `approval`, `diagnostics`, `marketplace`, `service_tier`) is plain prose / linked to the
nearest existing term; doc-page homes exist elsewhere (concepts co01/co06, cli, reference). Best-fit glossary
if any future term WERE captured: the agentic/LLM glossary (`acronym_glossary_ai_ml.md` analog) — but **0
captures triggered here.** No `## Term-Note Authoring Requirements` work required (N/A, 0 new terms).

**Issues found + fixed at this run:** one duplicated link-text typo (note 3 deployment list used
`snippet_openclaw_agents_runtime_config` text on the `snippet_openclaw_agents_tool_policy` path) — corrected so
link text matches target. No other issues; density caps unchanged (no note approaches 2,500w / 6 code / 400L);
measured source word counts re-confirmed equal to the plan's Source table (CP7).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review per `skill_tessellum_review_digestion_plan` canonical. Source pages re-read for CP7.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step — ≥8 terms + raised floors (≥10 snippets · ≥10 docs), each link w/ relevance | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; programmatic count confirms every note ≥8t / ≥10s / ≥10d with ≥5 existing docs (8t·10–12s·10d each; note 7 = 9t); every bullet carries a `; relevance:` clause. |
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+sqlite3, G6 broken-link-fix, G7 outbound/indexed, G8 in-degree ≥1 from outside the folder — single phase, all 8 present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` cites `entry_openclaw_docs.md` CREATE'd as master pre-step W1 (>30-note series ⇒ required); 11 rows under a "Plugins — Codex Harness & Ecosystem" cluster; per-note back-link at finalization satisfies G8. `entry_openclaw_docs` confirmed NOT yet in DB (correctly planned, not ghost-cited). |
| CP4 | Plan size manageable | **PASS** | 11 notes ≤ 30; single execution phase. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master `## Format Definition`, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) corpora: `## Overview` opener + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer; YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; same forbidden-field list. Target dir `resources/documentation/openclaw/` exists. |
| CP6 | Borderline density → split promoted | **PASS** | `## Split Decisions` promotes codex-harness (5,249w→notes 2/3/4), codex-harness-reference (3,137w→notes 5/6), compatibility (1,305w→notes 10/11 by topic, borderline-by-size split per CP6). `## Density Re-Assessment` shows no derived note approaches caps (≤700w / ≤6 code each). |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21 (`wc -w`/`grep`): codex-computer-use 1,937 · codex-harness 5,249 · codex-harness-reference 3,137 · codex-harness-runtime 2,290 · codex-native-plugins 1,673 · community 366 · compatibility 1,305 — **exact match** to the plan's Source table (ratio 1.00). (Minor: codex-harness measured 13 H2/4 H3 vs plan's "11 H2/3 H3" — all sections still mapped in the Section Coverage Map; no note re-split needed.) |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan (Step 4e)` present; disposition table routes every OpenClaw term to an `oc_*` note / existing-term link; **0 new term captures** → `## Term-Note Authoring Requirements` correctly N/A (inherited from master); new-term re-scan at augment confirms NONE. |
| CP8f | Slug/collision + all-notes dedup audit | **PASS** | Master Dedup Policy three-way check (term_dictionary ∧ documentation/ ∧ repo_openclaw*) applied; no planned `oc_*` doc duplicates an existing term/doc/repo (the 295 code-side OpenClaw notes are LINKED, not recreated). 0 new term slugs ⇒ no specificity/collision renames needed; "NOT in DB" list documents 13 vocab terms deliberately NOT cited as existing (avoids ghost-as-existing). |

**RESULT: 9/9 CP pass → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
</content>
</invoke>
