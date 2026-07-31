---
title: Sub-Plan to01 — OpenClaw Docs: Tools (ACP, agent-send, apply-patch, search, browser)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/acp-agents", "tools/acp-agents-setup", "tools/agent-send", "tools/apply-patch", "tools/brave-search", "tools/browser", "tools/browser-control"]
---

# Sub-Plan to01: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order + `## Overview`/`## Related Notes`/`## References`/footer), dedup (term_dictionary AND documentation/ AND `repo_openclaw*`), 9-GATE, cross-refs, undigested-terms ownership, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master.

## Scope

The first 7 `tools/` pages (Phase B, P2): the **ACP external-harness path** (running Claude Code / Cursor /
Gemini CLI / Codex ACP / OpenCode through OpenClaw), the **`agent-send` CLI tool** for one-shot agent turns,
the **`apply-patch` file-edit tool**, the **Brave web-search tool**, and the **OpenClaw-managed browser**
automation surface (setup + control API). These pages document the agent-facing *tools* an OpenClaw agent
can call and the operator commands that wire them. Priority **P2** — the feature/integration layer that the
concepts (co0x), gateway (gw0x), and CLI (cl0x) sub-plans reference. The code-side counterparts
(`repo_openclaw_agents`, `repo_openclaw_extensions`, the `snippet_openclaw_acp_*` family) are LINKED, never
recreated; ACP itself is the FZ 15 integration target.

**Source**: OpenClaw docs, 7 pages, **16,655 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| acp-agents | tools/acp-agents | 6,068 | 6 | 15 | 5 | concept + procedure (SPLIT ×3) |
| acp-agents-setup | tools/acp-agents-setup | 1,483 | 14 | 5 | 8 | procedure |
| agent-send | tools/agent-send | 684 | 4 | 5 | 0 | procedure |
| apply-patch | tools/apply-patch | 269 | 2 | 4 | 0 | procedure |
| brave-search | tools/brave-search | 651 | 2 | 5 | 0 | procedure |
| browser | tools/browser | 5,028 | 17 | 17 | 4 | procedure + concept (SPLIT ×3) |
| browser-control | tools/browser-control | 2,472 | 10 | 8 | 3 | procedure |

Notes on measurement: `Code` = `grep -c '```' ÷ 2` (paired fences). `agent-send`'s `grep` for `^#` headers also
matched 4 `#`-prefixed bash comments inside the Examples block (lines 99/102/105/108/111); the real H2 set is
Quick start · Flags · Behavior · Examples · Related = **5 H2, 0 H3**. `apply-patch` (269w) is far below caps but
is a distinct agent tool with its own page → its own atomic note (no merge candidate of the same BB+topic).

## Content Strategy

- **Prioritize**: the ACP backend (the FZ 15 external-harness integration path) — its concept layer (what ACP
  is, ACP vs sub-agents, how it runs Claude Code/Codex), its operator runbook + spawn/bind procedure, and its
  delivery/sandbox/controls runtime — plus the browser automation surface (the most-used agent tool family).
- **Split**: `tools/acp-agents.md` (6,068w, mixed concept+procedure) → **3 notes** (concept · operator/spawn/bind
  procedure · runtime delivery/controls/troubleshooting). `tools/browser.md` (5,028w, mixed) → **3 notes**
  (overview+quickstart+config procedure · vision/remote-control procedure · security/isolation+CDP concept).
- **Link-out (do NOT redefine)**: ACP harness *install/plugin/permission* config lives on `tools/acp-agents-setup`
  (its own note here); `tools/browser-control` HTTP/CLI reference is its own note (browser pages cross-link it).
  Other-sub-plan targets linked, not duplicated: `/cli/acp` bridge mode (cl01), `/automation/tasks` background
  tasks (au01), `/gateway/cli-backends` (gw01), `/gateway/sandboxing` + `sandbox-vs-tool-policy-vs-elevated`
  (gw05), provider/search-plugin pages (pr0x / pl0x), `tools/exec`+`tools/web` (to03/to08). Terms
  `term_acp_agent_client_protocol` / `term_mcp` / `term_claude_code` / `term_browser_automation` / `term_cdp`
  are LINKED, never re-defined in an `oc_*` note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_acp_agents_overview.md` | concept | acp-agents.md: intro Note, Which page do I want?, Does this work out of the box?, Supported harness targets, ACP versus sub-agents, How ACP runs Claude Code, Bound sessions › Mental model | 650 | What the ACP backend is: running external coding harnesses (Claude Code, Cursor, Gemini CLI, explicit Codex ACP, OpenCode) through OpenClaw, ACP vs the native Codex path vs sub-agents, supported harness targets, and the bound-session mental model. |
| 2 | `oc_tools_acp_agents_spawn_bind.md` | procedure | acp-agents.md: Operator runbook, Bound sessions › Current-conversation binds, Persistent channel bindings (Binding model, Runtime defaults per agent, Example, Behavior), Start ACP sessions (`sessions_spawn` parameters), Spawn bind and thread modes | 700 | Operator procedure for ACP sessions: `/acp` runbook commands, current-conversation `--bind here` vs `--thread` binds, persistent `bindings[]` + per-agent `runtime` defaults, and `sessions_spawn({ runtime: "acp" })` parameters and bind/thread modes. |
| 3 | `oc_tools_acp_agents_runtime.md` | procedure | acp-agents.md: Delivery model, Sandbox compatibility, Session target resolution, ACP controls (Runtime options mapping), acpx harness/plugin setup/permissions pointer, Troubleshooting | 650 | ACP runtime behavior and operations: completion delivery model, sandbox compatibility gating, session target resolution, `/acp` controls + runtime-options mapping, and troubleshooting the ACP backend / plugin wiring / delivery. |
| 4 | `oc_tools_acp_agents_setup.md` | procedure | acp-agents-setup.md: acpx harness support, Required config, Plugin setup for acpx backend (command/version, dependency install, plugin-tools MCP bridge, OpenClaw-tools MCP bridge, timeout, health probe), Permission configuration (`permissionMode`, `nonInteractivePermissions`, Configuration) | 600 | Installing and configuring the `@openclaw/acpx` backend plugin: required config, acpx command/version + automatic dependency install, the two MCP bridges (plugin-tools and OpenClaw-tools), operation timeout, health-probe agent, and permission mode / non-interactive permissions. |
| 5 | `oc_tools_agent_send.md` | procedure | agent-send.md: Quick start, Flags, Behavior, Examples | 400 | The `agent-send` tool/CLI for sending a single turn to an agent session: quick start, flags (JSON output, thinking level, session key, agent scope, channel override), turn behavior, and worked examples. |
| 6 | `oc_tools_apply_patch.md` | procedure | apply-patch.md: intro, Parameters, Notes, Example | 300 | The `apply-patch` file-edit tool: the patch envelope format, parameters, behavior notes, and a worked add/update/delete example for agent-driven file edits. |
| 7 | `oc_tools_brave_search.md` | procedure | brave-search.md: Get an API key, Config example, Tool parameters, Notes | 450 | The Brave web-search tool: obtaining a Brave Search API key, the config example to enable it, the search tool parameters, and usage notes. |
| 8 | `oc_tools_browser_overview.md` | procedure | browser.md: intro/Beginner view, What you get, Quick start, Plugin control, Agent guidance, Missing browser command or tool, Profiles `openclaw` vs `user`, Configuration | 700 | The OpenClaw-managed browser: an isolated agent-controlled Chrome/Brave/Edge profile, what you get, quick-start CLI, plugin control, agent guidance, the `openclaw` vs `user` profile split, and core configuration. |
| 9 | `oc_tools_browser_vision_remote.md` | procedure | browser.md: Screenshot vision (text-only model support), Use Brave or another Chromium-based browser, Local vs remote control, Node browser proxy, Browserless (hosted remote CDP + Docker on same host), Direct WebSocket CDP providers (Browserbase, Notte), Profiles (multi-browser), Browser selection | 700 | Browser vision + remote control: screenshot-vision for text-only models, choosing a Chromium-based browser, local vs remote control, the zero-config Node browser proxy, Browserless and direct-WebSocket CDP providers (Browserbase, Notte), and multi-browser profiles. |
| 10 | `oc_tools_browser_security_isolation.md` | concept | browser.md: Security, Existing session via Chrome DevTools MCP (Custom Chrome MCP launch), Isolation guarantees, Control API (pointer), Troubleshooting (CDP startup failure vs navigation SSRF block), Agent tools + how control works | 650 | Browser security and isolation model: attaching to an existing signed-in session via Chrome DevTools MCP, isolation guarantees, the SSRF/navigation safety boundary, and how the agent browser tools map to the control runtime. |
| 11 | `oc_tools_browser_control.md` | procedure | browser-control.md: Control API (`/act` error contract, Playwright requirement), How it works (internal), CLI quick reference, Snapshots and refs, Wait power-ups, Debug workflows, JSON output, State and environment knobs, Security and privacy | 700 | The browser control reference: the loopback HTTP control API (endpoints, `/act` error contract, Playwright requirement), the `openclaw browser` CLI quick reference, snapshots/refs, wait power-ups, debug workflows, JSON output, and state/environment knobs. |

## Section Coverage Map

```
tools/acp-agents.md (6,068w)
├── intro Note (ACP = external-harness path, not default Codex) ─── → note 1 (overview)
├── ## Which page do I want? ─────────────────────────────────────── → note 1
├── ## Does this work out of the box? ───────────────────────────── → note 1
├── ## Supported harness targets ────────────────────────────────── → note 1
├── ## ACP versus sub-agents ────────────────────────────────────── → note 1
├── ## How ACP runs Claude Code ─────────────────────────────────── → note 1
├── ## Bound sessions › ### Mental model ─────────────────────────── → note 1
├── ## Bound sessions › ### Current-conversation binds ───────────── → note 2 (spawn_bind)
├── ## Operator runbook ─────────────────────────────────────────── → note 2
├── ## Persistent channel bindings › ### Binding model ──────────── → note 2
├── ## Persistent channel bindings › ### Runtime defaults per agent → note 2
├── ## Persistent channel bindings › ### Example ────────────────── → note 2
├── ## Persistent channel bindings › ### Behavior ──────────────── → note 2
├── ## Start ACP sessions › ### sessions_spawn parameters ───────── → note 2
├── ## Spawn bind and thread modes ─────────────────────────────── → note 2
├── ## Delivery model ──────────────────────────────────────────── → note 3 (runtime)
├── ## Sandbox compatibility ───────────────────────────────────── → note 3
├── ## Session target resolution ───────────────────────────────── → note 3
├── ## ACP controls › ### Runtime options mapping ──────────────── → note 3
├── ## acpx harness, plugin setup, and permissions (pointer) ───── → note 3 (→ note 4)
└── ## Troubleshooting ─────────────────────────────────────────── → note 3
tools/acp-agents-setup.md (1,483w)
├── ## acpx harness support (current) ──────────────────────────── → note 4 (setup)
├── ## Required config ─────────────────────────────────────────── → note 4
├── ## Plugin setup for acpx backend (+ 6 H3: command/version,
│   dependency install, plugin-tools MCP bridge, OpenClaw-tools MCP
│   bridge, operation timeout, health probe) ───────────────────── → note 4
└── ## Permission configuration (+ permissionMode,
    nonInteractivePermissions, Configuration) ──────────────────── → note 4
tools/agent-send.md (684w)
├── ## Quick start / ## Flags / ## Behavior / ## Examples ──────── → note 5 (agent_send)
tools/apply-patch.md (269w)
├── intro / ## Parameters / ## Notes / ## Example ─────────────── → note 6 (apply_patch)
tools/brave-search.md (651w)
├── ## Get an API key / ## Config example / ## Tool parameters /
│   ## Notes ───────────────────────────────────────────────────── → note 7 (brave_search)
tools/browser.md (5,028w)
├── intro / Beginner view ──────────────────────────────────────── → note 8 (browser_overview)
├── ## What you get / ## Quick start / ## Plugin control ───────── → note 8
├── ## Agent guidance / ## Missing browser command or tool ─────── → note 8
├── ## Profiles: openclaw vs user / ## Configuration ───────────── → note 8
├── ## Configuration › ### Screenshot vision (text-only model) ─── → note 9 (vision_remote)
├── ## Use Brave or another Chromium-based browser ─────────────── → note 9
├── ## Local vs remote control / ## Node browser proxy ────────── → note 9
├── ## Browserless (hosted remote CDP) › ### Docker same host ─── → note 9
├── ## Direct WebSocket CDP providers › ### Browserbase/Notte ─── → note 9
├── ## Profiles (multi-browser) / ## Browser selection ─────────── → note 9
├── ## Security ─────────────────────────────────────────────────── → note 10 (security_isolation)
├── ## Existing session via Chrome DevTools MCP › ### Custom Chrome
│   MCP launch ─────────────────────────────────────────────────── → note 10
├── ## Isolation guarantees ────────────────────────────────────── → note 10
├── ## Control API (optional) (pointer) ───────────────────────── → note 10 (→ note 11)
├── ## Troubleshooting › ### CDP startup failure vs SSRF block ── → note 10
└── ## Agent tools + how control works ─────────────────────────── → note 10
tools/browser-control.md (2,472w)
├── ## Control API (optional) › ### /act error contract,
│   ### Playwright requirement ─────────────────────────────────── → note 11 (browser_control)
├── ## How it works (internal) / ## CLI quick reference ───────── → note 11
├── ## Snapshots and refs / ## Wait power-ups / ## Debug workflows → note 11
└── ## JSON output / ## State and environment knobs /
    ## Security and privacy ───────────────────────────────────── → note 11
```
No orphaned sections. `## Related` blocks at each page's tail become each note's `## Related Notes`/`## References`.
Pointers (acp-agents → acp-agents-setup; browser → browser-control) become cross-links, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| acp-agents.md (6,068w, 15 H2 / 5 H3, mixed concept+procedure) | notes 1 + 2 + 3 | >2,500w (2.4× cap) AND mixes a concept layer (what ACP is, ACP-vs-sub-agents, how it runs Claude Code, mental model) with two distinct procedure clusters (spawn/bind operator workflow; runtime delivery/sandbox/controls/troubleshooting). Per-cap + mixed-BB rule → 3 atomic notes, each ≤700w, one BB each. |
| browser.md (5,028w, 17 H2 / 4 H3, mixed procedure+concept) | notes 8 + 9 + 10 | >2,500w (2.0× cap) AND mixes setup/config procedure, vision+remote-control procedure, and a security/isolation concept. Split per word-cap + mixed-BB into overview/config, vision/remote, and security/isolation; the HTTP/CLI control reference is its own page (note 11). |
| acp-agents-setup.md (1,483w, 14 fences) | note 4 (no split) | Single-BB procedure under caps; kept whole. Code-heavy (14 fences → 7 paired) but config snippets reproduced selectively so the note stays ≤6 code blocks. |
| browser-control.md (2,472w, 10 fences) | note 11 (no split) | Single-BB procedure just under the 2,500w cap; one coherent control-API/CLI reference. Reproduce CLI/JSON snippets selectively to stay ≤6 code blocks. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (16,655 measured words). New `oc_*` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×2** (notes 1, 10) · **procedure ×9** (notes 2, 3, 4, 5, 6, 7, 8, 9, 11).
- Est. digest words ≈ **6,500** (avg ~590/note; range 300–700). 55 source paired fences distribute across
  notes; each note kept ≤6 (config / CLI / JSON snippets reproduced selectively, verbatim).
- Cross-refs (**LOCKED at xref-augment 2026-06-21**): each note maps **≥8 relevance-selected `term_dictionary`
  marked "(planned, this series)". See `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> on 2026-06-21. All terms/snippets/repos cited are EXISTING. Docs floor = 10: each note cites ≥5 EXISTING
> coding-agent + agent corpora) plus sibling `oc_*` docs of THIS series marked "(planned, this series)".
> Relative paths are FROM `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`;
> sibling oc_ → `oc_Y.md`; cross-folder doc → `../<folder>/<file>.md`; repo → `../../../areas/code_repos/repo_Y.md`;
> snippet → `../../code_snippets/snippet_Y.md`; entry → `../../../0_entry_points/entry_Y.md`.

### oc_tools_acp_agents_overview (10t · 10s · 11d)

**Terms**
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — the JSON-RPC protocol an editor/host speaks to an external coding harness; relevance: this note IS the ACP backend concept (running Claude Code/Cursor/Gemini/Codex/OpenCode through ACP).
- [Agent Client Protocol (communication)](../../term_dictionary/term_acp_agent_communication_protocol.md) — the protocol's session/turn message surface; relevance: defines how OpenClaw's control plane talks to a spawned harness session.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's terminal coding agent; relevance: the canonical `claude` harness target the ACP backend runs and the page's "How ACP runs Claude Code" stack.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the class of CLI coding agents; relevance: ACP's whole purpose is running this class (Cursor, Gemini CLI, Codex, OpenCode, Droid) through OpenClaw.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime wrapper around a model that owns tools/loop; relevance: an ACP session IS a "harness session"; the page contrasts harness-owned vs OpenClaw-owned responsibilities.
- [Sub-agent](../../term_dictionary/term_subagent.md) — an OpenClaw-native delegated run; relevance: the page's "ACP versus sub-agents" comparison table is a core section of this note.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — the tool/context bridge protocol; relevance: the page distinguishes ACP from `openclaw mcp serve` (external MCP client connecting to channel conversations).
- [Cursor](../../term_dictionary/term_cursor.md) — the AI IDE/CLI; relevance: `cursor` (`cursor-agent acp`) is a named supported harness target with adapter notes.
- [LLM](../../term_dictionary/term_llm.md) — the underlying model each harness drives; relevance: harness model ids are non-portable across harnesses (a key gotcha in this note).
- [Kiro CLI](../../term_dictionary/term_kiro_cli.md) — the Kiro coding CLI; relevance: `kiro` is one of the supported acpx harness targets enumerated on this page.

**Docs**
- [oc_tools_acp_agents_spawn_bind](oc_tools_acp_agents_spawn_bind.md) — ACP spawn/bind operator procedure (planned, this series); relevance: the overview's mental model feeds directly into the spawn/bind workflow.
- [oc_tools_acp_agents_runtime](oc_tools_acp_agents_runtime.md) — ACP delivery/sandbox/controls runtime (planned, this series); relevance: the overview's "harness vs OpenClaw responsibilities" is detailed in the runtime note.
- [oc_tools_acp_agents_setup](oc_tools_acp_agents_setup.md) — acpx plugin install/config (planned, this series); relevance: "does this work out of the box?" points here for install.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — Claude Code sub-agents; relevance: the ACP-vs-sub-agents contrast mirrors CC's own native sub-agent model.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — Claude Code MCP; relevance: grounds the ACP-vs-`mcp serve` distinction the page draws.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes's ACP server internals; relevance: parallel implementation of the same external-harness ACP path.
- [hermes_acp_editor_integration](../hermes_agent/hermes_acp_editor_integration.md) — Hermes exposing a session as an ACP server; relevance: the inverse direction of this page's "bridge mode" pointer (`openclaw acp`).
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Codex harness runtime in Hermes; relevance: the page's native-Codex-vs-ACP-Codex distinction maps to Hermes's Codex runtime.
- [cc_agent_sdk_overview](../claude_code/cc_agent_sdk_overview.md) — the Claude Agent SDK; relevance: the SDK is the runtime layer an ACP `claude` adapter wraps.
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — Hermes agent loop; relevance: explains the harness-owned model/tool loop that ACP delegates to.
- [bedrock_agents_how_it_works](../aws_bedrock/bedrock_agents_how_it_works.md) — Bedrock Agents runtime model; relevance: cross-vendor view of an externally-orchestrated agent runtime vs OpenClaw's ACP orchestration.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — ACP runtime + sub-agent code; relevance: implements the ACP session control plane this note describes.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — product overview; relevance: positions ACP within OpenClaw's overall architecture.
- [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — Hermes ACP module; relevance: sibling-ecosystem implementation of the ACP harness path.

**Snippets**
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — ACP runtime interface contract; relevance: the code-level shape of the "ACP backend plugin" this note introduces.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — `sessions_spawn({runtime:"acp"})` impl; relevance: the spawn path behind "how ACP sessions start".
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — ACP `session/new` init; relevance: how a harness session is established (the "How ACP runs Claude Code" stack).
- [snippet_openclaw_acp_translator_prompt](../../code_snippets/snippet_openclaw_acp_translator_prompt.md) — prompt translation across the ACP boundary; relevance: how OpenClaw turns become harness prompts.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — OpenClaw-as-ACP-server (bridge mode); relevance: the `openclaw acp` bridge target listed in "Which page do I want?".
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — backend registration; relevance: "a runtime backend must be loaded" gate for ACP usability.
- [snippet_hermes_agent_acp_server_init](../../code_snippets/snippet_hermes_agent_acp_server_init.md) — Hermes ACP server init; relevance: parallel harness-session bootstrap.
- [snippet_hermes_agent_acp_session](../../code_snippets/snippet_hermes_agent_acp_session.md) — Hermes ACP session object; relevance: shows the durable harness-session state OpenClaw routes to.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — ACP harness registry; relevance: the "supported harness targets" table is a registry like this.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — sub-agent registry/announce; relevance: backs the ACP-vs-sub-agent runtime distinction.

### oc_tools_acp_agents_spawn_bind (9t · 11s · 11d)

**Terms**
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — external-harness protocol; relevance: spawn/bind operates ACP sessions (`/acp spawn`, `sessions_spawn({runtime:"acp"})`).
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — the rules governing thread↔session binding; relevance: this note IS the `--bind here` vs `--thread auto/here/off` binding model.
- [Sub-agent](../../term_dictionary/term_subagent.md) — delegated background run; relevance: `sessions_spawn` shares the spawn surface and background lane with sub-agents.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state across restarts; relevance: persistent `bindings[]` + `mode:"session"` persist across gateway restarts.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `claude` harness; relevance: a primary bind target (`/acp spawn claude --bind here`).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: spawn resolves a harness `agentId` and binds the conversation to its session.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/background task; relevance: each ACP spawn is tracked as a background task (parent-owned one-shot lane).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel routing core; relevance: persistent bindings route Discord/Slack/Telegram/WhatsApp/iMessage conversations to the bound ACP session.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the harness class; relevance: `--thread`/`--bind`/`resumeSessionId` apply across codex/gemini/opencode/droid spawns.

**Docs**
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept + mental model (planned, this series); relevance: defines the chat-surface/session/thread/workspace mental model this procedure uses.
- [oc_tools_acp_agents_runtime](oc_tools_acp_agents_runtime.md) — delivery/controls runtime (planned, this series); relevance: bound vs parent-owned delivery is detailed there.
- [oc_tools_acp_agents_setup](oc_tools_acp_agents_setup.md) — thread-binding config flags (planned, this series); relevance: `spawnSessions` channel flags are configured there.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — CC sub-agent creation; relevance: parallel spawn-a-delegated-run workflow.
- [cc_dispatch_background_agents](../claude_code/cc_dispatch_background_agents.md) — CC background agent dispatch; relevance: mirrors parent-owned one-shot ACP background spawns.
- [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — CC SDK session management; relevance: parallel to `resumeSessionId`/`session/load` resume.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP session lifecycle; relevance: parallel spawn/session machinery.
- [hermes_cli_session_background](../hermes_agent/hermes_cli_session_background.md) — Hermes background sessions; relevance: same background-task tracking model for spawned sessions.
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: cross-tool view of session keys/binding semantics.
- [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — CC session resume patterns; relevance: parallels persistent-vs-oneshot mode + resume.
- [bedrock_agents_test](../aws_bedrock/bedrock_agents_test.md) — Bedrock agent session test; relevance: cross-vendor session-binding/invocation reference.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — spawn policy + runtime; relevance: implements `sessions_spawn` and ACP spawn gating.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: holds the ACP session metadata + bindings this note configures.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — channel bindings; relevance: implements per-channel `match.peer.id` binding shapes.

**Snippets**
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn admission policy; relevance: the allowed-agents/sandbox gating behind `/acp spawn`.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — thread-bind impl; relevance: exact `--thread auto/here/off` binding logic.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — session handoff; relevance: parent→child spawn handoff for one-shot ACP runs.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — `bindings[].type="acp"` impl; relevance: exact persistent-channel-binding resolution + override precedence.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — `runtime:"acp"` spawn; relevance: the `sessions_spawn` parameter path documented here.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — spawn policy; relevance: shared spawn-policy lane for ACP + sub-agents.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding→route resolution; relevance: routes matched conversations to the configured ACP session.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread-binding policy; relevance: `spawnSessions` thread-binding gates per adapter.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — `match` resolver; relevance: resolves the per-channel `match.peer.id` shapes in `bindings[]`.
- [snippet_hermes_agent_acp_server_session_methods](../../code_snippets/snippet_hermes_agent_acp_server_session_methods.md) — ACP session methods; relevance: parallel `session/new`/`session/load` handling for spawn/resume.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — session init translation; relevance: what a spawn produces upstream in the harness.

### oc_tools_acp_agents_runtime (9t · 11s · 11d)

**Terms**
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — external-harness protocol; relevance: this note is the ACP delivery/controls runtime + transport.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: the page's "Sandbox compatibility" — ACP runs host-side, NOT inside the OpenClaw sandbox.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the sandbox runtime impl; relevance: `runtime:"subagent"` is the sandbox-enforced alternative this note contrasts.
- [Event Ledger](../../term_dictionary/term_event_ledger.md) — the ordered runtime event log; relevance: ACP turn/completion events flow through the ledger (delivery model).
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — ACP's wire protocol; relevance: ACP controls/turns are JSON-RPC requests to the harness.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: ACP/CDP transport for streamed turn progress (`streamTo:"parent"` JSONL relay).
- [Claude Code](../../term_dictionary/term_claude_code.md) — `claude` harness; relevance: model/permission/timeout controls map onto the running Claude/Codex session.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — mid-turn steer instruction; relevance: `/acp steer` is a runtime control documented in this note.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny security posture; relevance: ACP still enforces feature gates/allowed-agents/ownership even outside the sandbox.

**Docs**
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept (planned, this series); relevance: defines the harness-vs-OpenClaw responsibility split this runtime enforces.
- [oc_tools_acp_agents_spawn_bind](oc_tools_acp_agents_spawn_bind.md) — spawn/bind (planned, this series); relevance: session target resolution depends on the bindings created there.
- [oc_tools_acp_agents_setup](oc_tools_acp_agents_setup.md) — permission/timeout config (planned, this series); relevance: `permissionMode`/`timeoutSeconds` that the controls mapping writes are configured there.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — CC sandbox modes; relevance: contrasts CC's sandboxing with ACP's host-side execution.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — CC FS/network isolation; relevance: shows the isolation ACP does NOT apply to host-side harnesses.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — CC permission rules; relevance: parallel to ACP runtime permission/approval controls.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP runtime internals; relevance: parallel delivery/cancel/turn-stream machinery.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tools; relevance: harness-owned tools the runtime delegates to.
- [cc_agent_sdk_loop_controls](../claude_code/cc_agent_sdk_loop_controls.md) — SDK loop controls; relevance: cancel/steer/timeout parallels for an agent run.
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK telemetry; relevance: parallel to ACP turn-stream/event observability.
- [bedrock_agents_trace_structure](../aws_bedrock/bedrock_agents_trace_structure.md) — Bedrock agent trace; relevance: cross-vendor runtime event/trace delivery model.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — ACP runtime; relevance: implements delivery model, controls apply, and target resolution.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox/tool policy; relevance: the feature gates ACP still enforces host-side.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session resolution; relevance: backs the `/acp` session-target resolution order.

**Snippets**
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — apply runtime controls; relevance: the `/acp` controls + runtime-options mapping table.
- [snippet_openclaw_acp_manager_turn_stream](../../code_snippets/snippet_openclaw_acp_manager_turn_stream.md) — turn streaming; relevance: the delivery model + `streamTo:"parent"` progress stream.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: materializes completion events per target.
- [snippet_openclaw_acp_translator_cancel](../../code_snippets/snippet_openclaw_acp_translator_cancel.md) — cancel translation; relevance: `/acp cancel` aborts the active turn.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: policy still enforced even though ACP runs host-side.
- [snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md) — rate limit; relevance: runtime control over harness turn pacing.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached runtime worker; relevance: idle-worker cleanup after `acp.runtime.ttlMinutes`.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: the key/UUID/label resolution order documented here.
- [snippet_hermes_agent_acp_server_cancel_config](../../code_snippets/snippet_hermes_agent_acp_server_cancel_config.md) — Hermes cancel config; relevance: parallel cancel-capability handling.
- [snippet_hermes_agent_acp_events](../../code_snippets/snippet_hermes_agent_acp_events.md) — Hermes ACP events; relevance: parallel turn/completion event delivery.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: the `<<<BEGIN_OPENCLAW_INTERNAL_CONTEXT>>>` envelope must never cross the ACP boundary.

### oc_tools_acp_agents_setup (10t · 11s · 11d)

**Terms**
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — external-harness protocol; relevance: this note installs/configures the `@openclaw/acpx` ACP backend.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — tool/context bridge; relevance: the page's two MCP bridges (plugin-tools, OpenClaw-tools) expose tools to the harness.
- [MCP Gateway](../../term_dictionary/term_mcp_gateway.md) — an MCP server multiplexer; relevance: the injected `openclaw-plugin-tools`/`openclaw-tools` MCP servers act as a gateway to OpenClaw tools.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the plugin extension API; relevance: acpx is a runtime plugin installed/enabled via the plugin system.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — a tool's schema/metadata; relevance: the bridges register OpenClaw tool descriptors into the ACPX session.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `claude` harness; relevance: a primary acpx harness alias whose command/version is configured here.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: acpx command/version/args + probe-agent config target each harness.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation/permission boundary; relevance: ACP `permissionMode`/`nonInteractivePermissions` are the harness-level permission controls.
- [Break-Glass](../../term_dictionary/term_break_glass.md) — emergency full-access switch; relevance: ACPX `approve-all` is the harness-level break-glass for non-interactive writes/exec.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — adapter capability discovery; relevance: model control is adapter-capability dependent (ACP `models`/`session/set_model`).

**Docs**
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept (planned, this series); relevance: the setup page's "for overview/concepts, see ACP agents" pointer.
- [oc_tools_acp_agents_spawn_bind](oc_tools_acp_agents_spawn_bind.md) — spawn/bind (planned, this series); relevance: thread-binding config here enables the spawn flows there.
- [oc_tools_acp_agents_runtime](oc_tools_acp_agents_runtime.md) — runtime (planned, this series); relevance: `permissionMode`/`timeoutSeconds` set here drive the runtime controls there.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — CC managed MCP config; relevance: parallel to enabling MCP bridges for a harness.
- [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — CC SDK MCP servers; relevance: the injected MCP servers mirror SDK MCP wiring.
- [cc_sandboxed_bash_tool_setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — CC sandboxed exec setup; relevance: parallel to ACPX permission-mode setup for write/exec.
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Codex runtime setup; relevance: parallel external-harness backend install/config.
- [hermes_acp_editor_integration](../hermes_agent/hermes_acp_editor_integration.md) — Hermes ACP integration setup; relevance: parallel ACP backend wiring.
- [hermes_adding_built_in_tool](../hermes_agent/hermes_adding_built_in_tool.md) — adding a tool to the harness; relevance: parallel to exposing OpenClaw tools via the bridges.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tool registration; relevance: cross-tool view of exposing host tools to an agent.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — CC plugin policy; relevance: parallel to `plugins.allow`/`plugins.deny` gating acpx.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/backend code; relevance: home of the `@openclaw/acpx` backend plugin installed here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — ACP runtime; relevance: the backend the acpx plugin registers.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — permissions; relevance: ACPX permission modes integrate with the security policy layer.

**Snippets**
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — backend register; relevance: the acpx plugin registers the embedded ACP backend at startup.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached runtime; relevance: command/version override + startup-probe wiring.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — permission relay; relevance: how `permissionMode`/`nonInteractivePermissions` are enforced.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/enable lifecycle; relevance: `plugins install`/`config set ... enabled true` flow for acpx.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the `@openclaw/acpx` package shape.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: how `plugins.entries.acpx.config.*` keys are surfaced.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback MCP server; relevance: the injected MCP bridge servers run on loopback.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: which OpenClaw tools the bridges can expose.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — Hermes ACP tool register; relevance: parallel tool-bridge registration.
- [snippet_hermes_agent_acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — Hermes ACP tool permission; relevance: parallel non-interactive permission handling.
- [snippet_hermes_agent_acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — Hermes ACP auth; relevance: parallel harness-side vendor auth requirement.

### oc_tools_agent_send (8t · 10s · 10d)

**Terms**
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — CLI agents; relevance: `openclaw agent` runs a single agent turn from the command line.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: the turn executes through the Gateway agent runtime (or `--local` embedded).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel routing; relevance: `--deliver`/`--reply-channel`/`--reply-to` deliver the reply to a chat channel.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `--session-id`/`--session-key` reuse + thinking/verbose persist into the session store.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/scripted runs; relevance: agent-send is built for scripted workflows and programmatic delivery.
- [Sub-agent](../../term_dictionary/term_subagent.md) — delegated run; relevance: the "Related" block links sub-agents as the background counterpart of one-shot turns.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway dispatch hub; relevance: by default the CLI goes through the Gateway, falling back to local embedded.
- [Claude Code](../../term_dictionary/term_claude_code.md) — coding agent; relevance: the targeted agent is typically a coding agent driven by a configured model profile.

**Docs**
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept (planned, this series); relevance: agent-send targets the same agent/session model ACP sessions use.
- [oc_tools_acp_agents_spawn_bind](oc_tools_acp_agents_spawn_bind.md) — session keys/binding (planned, this series); relevance: `--session-key agent:<id>:<key>` shares the session-key scheme.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — CC headless/`-p` mode; relevance: directly parallel to running a single agent turn from the CLI non-interactively.
- [cc_headless_examples](../claude_code/cc_headless_examples.md) — CC headless examples; relevance: parallel scripted-invocation examples.
- [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — CC SDK session API; relevance: parallel to `--session-id` reuse + JSON output.
- [hermes_cli_session_background](../hermes_agent/hermes_cli_session_background.md) — Hermes background CLI sessions; relevance: parallel CLI-driven agent turns with delivery.
- [hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md) — Hermes session-ops CLI; relevance: parallel session-targeting CLI flags.
- [hermes_api_server_endpoints](../hermes_agent/hermes_api_server_endpoints.md) — Hermes API endpoints; relevance: programmatic agent invocation analog.
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: cross-tool view of session-key derivation from a target.
- [bedrock_agents_test](../aws_bedrock/bedrock_agents_test.md) — Bedrock agent invoke/test; relevance: cross-vendor single-turn agent invocation.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent dispatch; relevance: implements the `openclaw agent` turn dispatch.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session-key resolution; relevance: resolves `--to`/`--agent`/`--session-key` into a session key.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — delivery channels; relevance: implements `--deliver` channel/reply routing.

**Snippets**
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch; relevance: the Gateway path a CLI agent turn takes.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key utils; relevance: `agent:<id>:<key>` scoping/derivation logic.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: delivery gating for `--deliver`.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: `--session-id` reuse path.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: how a generated reply is sent to a channel.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — session chat-type; relevance: `--to` group/channel vs direct-chat session isolation.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/local fallback; relevance: `--local` embedded-runtime fallback when the Gateway is unreachable.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel routing; relevance: `--reply-channel`/`--reply-to` override routing.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — Hermes CLI→gateway dispatch; relevance: parallel CLI agent-turn dispatch.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — Hermes send dispatch; relevance: parallel reply-delivery to a channel.

### oc_tools_apply_patch (8t · 10s · 10d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `apply_patch` is an agent tool the model calls with a structured `input` envelope.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool schema; relevance: the `apply_patch` tool exposes a single `input` parameter schema.
- [Claude Code](../../term_dictionary/term_claude_code.md) — coding agent; relevance: structured multi-file patch edits are a core coding-agent operation.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — coding agents; relevance: apply_patch is "available by default for OpenAI and OpenAI Codex models".
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: the patch tool runs inside the agent's file-edit toolset.
- [Sandbox](../../term_dictionary/term_sandbox.md) — workspace boundary; relevance: `tools.exec.applyPatch.workspaceOnly` defaults true (workspace-contained writes).
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: writes outside the workspace are denied unless explicitly opted in.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: model gating via `tools.exec.applyPatch.allowModels`.

**Docs**
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept (planned, this series); relevance: apply_patch is one of the file-edit tools an ACP harness exposes.
- [cc_file_tool_behavior](../claude_code/cc_file_tool_behavior.md) — CC file tools (Edit/Write); relevance: directly parallel structured-edit tool behavior.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: positions a patch/edit tool in the built-in tool catalog.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — CC exec behavior; relevance: apply_patch config lives under `tools.exec`.
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — CC custom tool def; relevance: parallel single-input tool schema.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — CC per-tool permission; relevance: parallel to `allowModels`/`workspaceOnly` gating.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tools; relevance: native Codex `apply-patch` lives here in the sibling ecosystem.
- [hermes_adding_built_in_tool](../hermes_agent/hermes_adding_built_in_tool.md) — adding a built-in tool; relevance: parallel file-edit tool registration.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tools; relevance: cross-tool view of a file-edit agent tool.
- [bedrock_agents_action_handle_return_control](../aws_bedrock/bedrock_agents_action_handle_return_control.md) — Bedrock return-control; relevance: cross-vendor view of a structured tool-call envelope.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool catalog; relevance: registers the `apply_patch` agent tool.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — write-tool policy; relevance: enforces `workspaceOnly` filesystem boundary.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: where `apply_patch` is registered + model-gated.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: write-tool gating for out-of-workspace edits.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: the `tools.exec.*` workspace-containment policy apply_patch obeys.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: enable/allowModels gating for the patch tool.
- [snippet_hermes_agent_tools_patch_parser](../../code_snippets/snippet_hermes_agent_tools_patch_parser.md) — patch envelope parser; relevance: parses the exact `*** Begin/Update/Delete/End Patch` envelope this note documents.
- [snippet_hermes_agent_tools_file_tools](../../code_snippets/snippet_hermes_agent_tools_file_tools.md) — file tools; relevance: parallel multi-file edit tool family.
- [snippet_hermes_agent_tools_file_operations_a](../../code_snippets/snippet_hermes_agent_tools_file_operations_a.md) — file operations; relevance: add/update/delete/move file ops behind apply_patch.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: parallel tool registration/model-default availability.
- [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — tool input schema guardrails; relevance: validates the single `input` string parameter.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestrator; relevance: apply_patch is part of the `tools.exec` surface.

### oc_tools_brave_search (8t · 10s · 11d)

**Terms**
- [RAG (Retrieval-Augmented Generation)](../../term_dictionary/term_rag.md) — grounding via retrieved context; relevance: Brave `llm-context` mode returns pre-extracted text chunks + sources for grounding.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→ranked-results; relevance: web_search returns ranked titles/URLs/snippets for a query.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `web_search({query,...})` is an agent tool the model calls.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool schema; relevance: the note documents the web_search tool parameters (query/count/country/freshness/...).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin API; relevance: Brave is a `web_search` provider configured under `plugins.entries.brave.config.webSearch.*`.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — tool bridge; relevance: search results feed the agent like any tool/context source.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — base-URL override; relevance: `webSearch.baseUrl` points Brave at a trusted Brave-compatible proxy/gateway.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: `llm-context` grounds the LLM with extracted source text.

**Docs**
- [oc_tools_acp_agents_setup](oc_tools_acp_agents_setup.md) — plugin config pattern (planned, this series); relevance: parallel `plugins.entries.<id>.config` provider setup.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — Hermes web search/extract; relevance: directly parallel web-search-with-extraction tool.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes web-search provider plugin; relevance: parallel pluggable web_search provider (Brave-like).
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — Hermes built-in plugins; relevance: parallel provider-plugin registration model.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider; relevance: parallel API-key + config-block provider onboarding.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools (WebSearch); relevance: parallel built-in web-search tool.
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — CC tool search; relevance: search-tool surface analog in CC.
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — CC custom tool def; relevance: parallel parameterized tool schema.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tools; relevance: cross-tool view of a search tool.
- [bedrock_agents_kb_integration](../aws_bedrock/bedrock_agents_kb_integration.md) — Bedrock KB grounding; relevance: cross-vendor view of grounding an agent with retrieved sources (RAG).
- [oc_tools_acp_agents_overview](oc_tools_acp_agents_overview.md) — ACP concept (planned, this series); relevance: web_search is one tool an ACP harness session can be granted.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — search plugin; relevance: home of the Brave `web_search` provider plugin.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool catalog; relevance: registers `web_search` in the agent toolset.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: registers the `web_search` tool.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: enable/profile gating of web_search.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin entries config; relevance: `plugins.entries.brave.config.webSearch.*` surfacing.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin contract; relevance: the Brave provider plugin package shape.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: `BRAVE_API_KEY` env/secret handling.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — Hermes web tools; relevance: parallel web_search/web_fetch tool impl.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — Hermes web plugin; relevance: parallel pluggable web-search provider.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: provider-tool registration parallel.
- [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — tool schema guardrails; relevance: validates the search-tool parameter schema.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: a sibling retrieval/grounding tool surface in the same agent toolset.

### oc_tools_browser_overview (9t · 11s · 11d)

**Terms**
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — agent-driven browser control; relevance: this note is the OpenClaw-managed isolated agent browser.
- [CDP (Chrome DevTools Protocol)](../../term_dictionary/term_cdp.md) — Chromium control protocol; relevance: the managed profile is driven over CDP through a loopback control service.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: the agent gets one `browser` tool (open/click/type/snapshot/screenshot).
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: the browser is a "safe, isolated surface" separate from the personal profile; `target:"sandbox"` vs `host`.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool schema; relevance: the `browser` tool description carries the always-on contract + profile/target params.
- [Claude Code](../../term_dictionary/term_claude_code.md) — coding agent; relevance: a browser-capable agent added via `tools.alsoAllow:["browser"]`.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — harness runtime; relevance: profile/sub-agent tool gating applies after profile filtering.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image+text models; relevance: screenshots return image blocks a vision/multimodal model reads.
- [IDE](../../term_dictionary/term_ide.md) — developer environment; relevance: the `user` profile attaches to your real signed-in Chrome via Chrome DevTools MCP.

**Docs**
- [oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md) — vision + remote control (planned, this series); relevance: screenshot-vision + remote CDP are split into the sibling note.
- [oc_tools_browser_security_isolation](oc_tools_browser_security_isolation.md) — security/isolation (planned, this series); relevance: isolation guarantees + SSRF are detailed there.
- [oc_tools_browser_control](oc_tools_browser_control.md) — control API/CLI reference (planned, this series); relevance: the "Control API (optional)" pointer.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: directly parallel agent browser enablement/profiles.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — Hermes browser backends; relevance: parallel managed-vs-existing-session browser backends.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: parallel browser lifecycle/cleanup management.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: positions a browser tool in the agent toolset.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — Hermes computer-use; relevance: adjacent GUI-automation surface for agents.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — CC sandbox modes; relevance: parallel to the `target:"sandbox"|"host"` browser placement.
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — Pi agent tools/events; relevance: cross-tool view of an agent browser tool surface.
- [bedrock_agents_action_groups_overview](../aws_bedrock/bedrock_agents_action_groups_overview.md) — Bedrock action groups; relevance: cross-vendor view of granting an agent an action/tool surface.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin; relevance: the bundled `browser` plugin lives here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool catalog/profiles; relevance: implements `tools.profile`/`alsoAllow` browser gating.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — loopback control service; relevance: hosts the in-Gateway browser control service.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: registers the single `browser` agent tool.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: profile/`alsoAllow` gating applied after profile filtering.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/disable; relevance: `plugins.entries.browser.enabled` + restart-to-re-register.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session; relevance: parallel managed-profile session/tab lifecycle.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigate; relevance: parallel open/navigate tab control.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — supervisor lifecycle; relevance: parallel tab-cleanup/idle lifecycle (the `tabCleanup` config).
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser plugin dispatch; relevance: parallel browser-tool dispatch through the plugin.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM snapshot; relevance: parallel snapshot-then-act loop the browser skill teaches.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP routing; relevance: `browser.request` gateway method registration.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability; relevance: the bundled `browser-automation` skill is surfaced when the plugin is enabled.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — sub-agent tool caps; relevance: why `tools.subagents.tools.allow:["browser"]` alone is insufficient.

### oc_tools_browser_vision_remote (9t · 11s · 11d)

**Terms**
- [CDP (Chrome DevTools Protocol)](../../term_dictionary/term_cdp.md) — Chromium control protocol; relevance: remote control attaches to a browser via `cdpUrl` (HTTP discovery or direct WebSocket).
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — agent browser control; relevance: this note is remote/multi-browser-profile browser automation.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: direct-WebSocket CDP providers (`ws://`/`wss://` `/devtools/...`) and bare-root handshakes.
- [Multimodal](../../term_dictionary/term_multimodal.md) — vision+text models; relevance: screenshot-vision describes screenshots as text for text-only main models.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — image understanding; relevance: the image-understanding runtime turns a screenshot into a text description.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Browserless self-hosted in Docker on the same host (`attachOnly:true`).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy/node routing; relevance: the zero-config Node browser proxy auto-routes browser calls to a node host.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: the same `browser` tool drives local and remote profiles transparently.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial page content; relevance: vision descriptions are wrapped with `wrapExternalContent` (prompt-injection guard).

**Docs**
- [oc_tools_browser_overview](oc_tools_browser_overview.md) — overview/config (planned, this series); relevance: profiles + `browser` config introduced there.
- [oc_tools_browser_security_isolation](oc_tools_browser_security_isolation.md) — security/isolation (planned, this series); relevance: remote-CDP token handling + isolation are detailed there.
- [oc_tools_browser_control](oc_tools_browser_control.md) — control API/CLI (planned, this series); relevance: `doctor` discovery-first/WebSocket-fallback uses the same logic.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — Hermes browser backends; relevance: directly parallel local/remote/hosted CDP backends.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: parallel remote-browser profile config.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: parallel remote-session lifecycle handling.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — Hermes computer-use/vision; relevance: parallel screenshot-vision GUI control.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: positions vision-capable browser tooling.
- [hermes_code_execution](../hermes_agent/hermes_code_execution.md) — Hermes remote execution; relevance: parallel remote-host (Docker/node) execution model.
- [bedrock_agentcore_gateway_semantic_search](../aws_bedrock_agentcore/bedrock_agentcore_gateway_semantic_search.md) — AgentCore gateway; relevance: cross-vendor remote-gateway proxying of agent capabilities.
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — Pi agent tools/events; relevance: cross-tool view of remote tool routing.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin; relevance: implements remote-CDP profile handling + Browserless/Browserbase/Notte attach.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway proxy/node routing; relevance: the Node browser proxy + remote-control proxying.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — media/vision extensions; relevance: image-understanding runtime reused for screenshot-vision.

**Snippets**
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — browser CDP connect; relevance: parallel HTTP-discovery vs direct-WebSocket CDP attach logic.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: parallel screenshot → image-block pipeline.
- [snippet_hermes_agent_tools_browser_camofox](../../code_snippets/snippet_hermes_agent_tools_browser_camofox.md) — hosted/stealth browser backend; relevance: parallel to Browserbase/Notte stealth+residential-proxy hosted CDP.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — supervisor recovery; relevance: parallel remote-CDP reachability/recovery handling.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision input; relevance: parallel feeding a screenshot to a vision model.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: parallel image-understanding model selection/fallback.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed image lifecycle; relevance: screenshot image-block handling/storage.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect proxy; relevance: remote/node proxy routing for browser calls.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — SSE session transport; relevance: streamed-transport analog for remote browser/CDP relay.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: `wrapExternalContent` prompt-injection guard on vision descriptions.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — tool deny policy; relevance: remote-CDP token/SSRF gating before browser navigation.

### oc_tools_browser_security_isolation (9t · 11s · 11d)

**Terms**
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side-request-forgery protection; relevance: this note's navigation SSRF boundary + `ssrfPolicy`/`hostnameAllowlist`/`dangerouslyAllowPrivateNetwork`.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — agent browser; relevance: this note is the browser isolation/security model.
- [CDP (Chrome DevTools Protocol)](../../term_dictionary/term_cdp.md) — Chromium control; relevance: existing-session attach via Chrome DevTools MCP + custom Chrome MCP launch.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: dedicated user-data-dir + dedicated ports isolate the agent browser from the personal profile.
- [WebSocket](../../term_dictionary/term_websocket.md) — CDP transport; relevance: remote CDP WebSocket endpoints treated as secrets; strict-mode endpoint checks.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — tool bridge; relevance: the `user`/existing-session driver uses Chrome DevTools MCP to attach to a signed-in session.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy/identity headers; relevance: Tailscale Serve / trusted-proxy identity headers do NOT authenticate the loopback browser API.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: browser config defaults to a fail-closed SSRF policy object even when unset.
- [Identity Propagation](../../term_dictionary/term_identity_propagation.md) — auth identity flow; relevance: loopback browser API uses shared-secret auth only (token/password), not identity-bearing modes.

**Docs**
- [oc_tools_browser_overview](oc_tools_browser_overview.md) — overview/config (planned, this series); relevance: `ssrfPolicy` config block introduced there.
- [oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md) — vision/remote (planned, this series); relevance: remote-CDP token handling secured per this note.
- [oc_tools_browser_control](oc_tools_browser_control.md) — control API/CLI (planned, this series); relevance: the loopback HTTP API auth + CDP startup-vs-SSRF distinction.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — CC FS/network isolation; relevance: parallel network-isolation/egress-control model.
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — CC org sandbox enforcement; relevance: parallel default-deny network policy enforcement.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — CC permission rules; relevance: parallel allow/deny boundary for sensitive operations.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: parallel isolated-session safety + recovery.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — Hermes route security; relevance: parallel loopback/shared-secret HTTP route auth.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP internals; relevance: parallel host-side execution security boundary.
- [bedrock_agents_action_handle_user_confirm](../aws_bedrock/bedrock_agents_action_handle_user_confirm.md) — Bedrock user-confirm; relevance: cross-vendor view of consent/approval before a sensitive action (attach-prompt analog).
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — Pi agent tools/events; relevance: cross-tool view of tool-permission boundaries.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security model; relevance: implements SSRF guard + shared-secret auth for the browser API.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin; relevance: the existing-session/Chrome-MCP attach driver.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — loopback control + auth; relevance: hosts the auth-gated loopback browser control plane.

**Snippets**
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: the higher-risk existing-session browser is gated by tool-deny policy.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — dispatch authorization; relevance: auth check for browser-control dispatch.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: why trusted-proxy/none modes do NOT auto-authenticate the loopback browser API.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — filesystem policy; relevance: parallel isolation boundary for agent operations.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: page content read by the agent is untrusted (injection boundary).
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: encrypted endpoints + identity for remote CDP/control.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: treat remote CDP URLs/tokens as secrets.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: parallel audit of a host-side execution surface.
- [snippet_hermes_agent_tools_browser_intercept](../../code_snippets/snippet_hermes_agent_tools_browser_intercept.md) — request interception; relevance: parallel navigation/request control boundary.
- [snippet_hermes_agent_acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — tool permission; relevance: parallel attach-consent/permission flow for higher-risk tools.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing allowlist; relevance: node-pairing access flow the browser control inherits.

### oc_tools_browser_control (9t · 11s · 11d)

**Terms**
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — agent browser control; relevance: this note is the `openclaw browser` control API + CLI reference.
- [CDP (Chrome DevTools Protocol)](../../term_dictionary/term_cdp.md) — Chromium control; relevance: the loopback control server connects to Chromium via CDP.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: the CLI/HTTP actions back the single `browser` agent tool's act/snapshot.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured request/response; relevance: `POST /act` uses a structured error contract (`{error, code:"ACT_*"}`).
- [WebSocket](../../term_dictionary/term_websocket.md) — CDP transport; relevance: per-tab CDP WebSocket enables ARIA/role snapshots without Playwright.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — loopback/proxy boundary; relevance: the standalone loopback HTTP API is loopback-only and does not consume proxy identity headers.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial input; relevance: `evaluate`/`wait --fn` run arbitrary page JS steerable by injection (`evaluateEnabled=false`).
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Docker Playwright/Chromium install for the control runtime.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — request-forgery protection; relevance: the strict-mode `ssrfPolicy` example blocking private/internal destinations.

**Docs**
- [oc_tools_browser_overview](oc_tools_browser_overview.md) — overview/config (planned, this series); relevance: "for setup/config/troubleshooting, see Browser".
- [oc_tools_browser_vision_remote](oc_tools_browser_vision_remote.md) — vision/remote (planned, this series); relevance: remote/local profile swapping the control plane abstracts.
- [oc_tools_browser_security_isolation](oc_tools_browser_security_isolation.md) — security/isolation (planned, this series); relevance: the loopback API auth + SSRF model.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: parallel CLI/control-surface for the agent browser.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: parallel snapshot/ref + recovery debug workflows.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — Hermes backends; relevance: parallel Playwright-on-CDP action engine.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: positions a scripted browser-control tool surface.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — CC exec behavior; relevance: parallel CLI/structured-action execution semantics.
- [hermes_api_server_endpoints](../hermes_agent/hermes_api_server_endpoints.md) — Hermes HTTP endpoints; relevance: parallel loopback HTTP control-endpoint catalog.
- [bedrock_agents_action_handle_return_control](../aws_bedrock/bedrock_agents_action_handle_return_control.md) — Bedrock return-control; relevance: cross-vendor structured action-error/return contract.
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — Pi agent tools/events; relevance: cross-tool view of a scripted tool-action API.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin; relevance: implements the control API actions (snapshot/act/wait/state).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — loopback HTTP server; relevance: hosts the `OPENCLAW_EAGER_BROWSER_CONTROL_SERVER` loopback endpoints.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent tool surface; relevance: maps the single `browser` tool to control-plane actions.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: the `browser` tool that fronts these control actions.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — HTTP entry dispatch; relevance: how loopback control requests are dispatched.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen; relevance: the loopback control server + per-tab CDP WebSocket listeners.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP routing; relevance: routes the `/tabs`, `/act`, `/snapshot` endpoints.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — dispatch authorization; relevance: bearer/password auth for the control routes.
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — browser CDP; relevance: parallel CDP-on-Playwright action engine.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM/snapshot; relevance: parallel snapshot/ref styles (AI/role/ARIA refs).
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — navigate/act; relevance: parallel navigate/click/type action surface.
- [snippet_hermes_agent_tools_browser_intercept](../../code_snippets/snippet_hermes_agent_tools_browser_intercept.md) — request interception/network; relevance: parallel `requests`/`response/body`/cookies/storage knobs.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot; relevance: parallel screenshot/`--labels`/`--full-page` behavior.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: `evaluate`/`wait --fn` arbitrary-JS injection risk boundary.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT as new
`term_dictionary` entries; the only term_dictionary interaction is **linking existing** terms.

| Term (appears in source) | Disposition |
|---|---|
| acpx (backend plugin) | OpenClaw product vocab → digested in `oc_tools_acp_agents_setup`; link `term_mcp` / `term_plugin_sdk`. Not a reusable cross-cutting term. |
| sessions_spawn / `--bind here` / `--thread` | OpenClaw command/config vocab → digested in `oc_tools_acp_agents_spawn_bind`. Not a term note. |
| Claude Code / Cursor / Gemini CLI / Codex ACP / OpenCode / Droid | Harness names → documented as config; link existing `term_claude_code` / `term_cursor` / `term_autonomous_coding_agents` / `term_agent_harness`. Names NOT promoted to term notes. |
| agent-send | OpenClaw CLI tool → digested in `oc_tools_agent_send`. Not a term note. |
| apply-patch / patch envelope | OpenClaw tool + a generic patch format → digested in `oc_tools_apply_patch`; link `term_function_calling`. No standalone `term_apply_patch` (not vault-reusable beyond this tool). |
| Brave Search / web-search tool | Provider/tool name → digested in `oc_tools_brave_search`; link `term_rag` / `term_function_calling`. Name NOT promoted. |
| Browserless / Browserbase / Notte / Playwright | Tool/provider names → documented as config in `oc_tools_browser_vision_remote`/`_control`; not promoted to term notes (no existing note; not cross-cutting). |
| screenshot vision / SSRF / loopback | OpenClaw browser-feature/security vocab → digested in the browser notes; no existing term note and not broadly reusable → NOT captured as new terms. |

**New `term_dictionary` captures: 0 (expected).** No genuinely reusable, cross-cutting term lacks both a doc-page
home AND an existing note. (`apply-patch`, `SSRF`, `screenshot-vision`, `Browserless` were each considered and
rejected: each is either tool-specific OpenClaw vocab with a doc-note home, or too narrow to warrant a vault
term.) Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. (Inherited from master: any genuinely
new cross-cutting term would be captured via `/tessellum-capture-term-note` + added to the relevant
triggered here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). All gates must PASS before commit.

| Gate | Name | Check |
|------|------|-------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean (YAML field order; tags lead resource/documentation/openclaw; `## Overview`/`## Related Notes`/`## References`/`**Source**`/`**Last Updated**`/`**Status**` footer). |
| G2 | Grounding | Each note diffs faithfully against its `inbox/openclaw_docs/tools/<page>.md` section(s); no invented behavior/flags. |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks per note; one building_block per note; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevancy-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + other vault notes per note, each an indexed link with a relevance statement. |
| G5 | Ghost-reference | No links to non-existent notes; detect + redirect (the GHOST list above is avoided). |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after incremental reindex. |
| G7/G8 | Discoverability / in-degree | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` rows + the inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_acp_agents_overview oc_tools_acp_agents_spawn_bind oc_tools_acp_agents_runtime oc_tools_acp_agents_setup oc_tools_agent_send oc_tools_apply_patch oc_tools_brave_search oc_tools_browser_overview oc_tools_browser_vision_remote oc_tools_browser_security_isolation oc_tools_browser_control"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format-OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density (strip YAML frontmatter before counting)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb ${lines}L)"
  # G7/G8 sibling/outside inbound smoke (does at least one oc_ sibling or entry link the note?)
  grep -rql "$n.md" "$GATE_DIR" 0_entry_points 2>/dev/null || echo "G8 WARN no inbound for $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# ghost-reference + broken-link sweep after incremental reindex:
bash scripts/update_notes_database.sh
```

(`SIBLING_PREFIX=oc_` is used by augment/review to confirm intra-series cross-links resolve.)

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤400L / ≤2500w / ≤6cb)? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_acp_agents_overview | concept | 650 | 2 | YES |
| 2 | oc_tools_acp_agents_spawn_bind | procedure | 700 | 4 | YES |
| 3 | oc_tools_acp_agents_runtime | procedure | 650 | 3 | YES |
| 4 | oc_tools_acp_agents_setup | procedure | 600 | 6 | YES (cap-edge on code: reproduce config selectively) |
| 5 | oc_tools_agent_send | procedure | 400 | 3 | YES |
| 6 | oc_tools_apply_patch | procedure | 300 | 2 | YES |
| 7 | oc_tools_brave_search | procedure | 450 | 2 | YES |
| 8 | oc_tools_browser_overview | procedure | 700 | 4 | YES |
| 9 | oc_tools_browser_vision_remote | procedure | 700 | 5 | YES |
| 10 | oc_tools_browser_security_isolation | concept | 650 | 3 | YES |
| 11 | oc_tools_browser_control | procedure | 700 | 6 | YES (cap-edge on code: reproduce CLI/JSON selectively) |

No note approaches the word/line caps. The two code-heavy single-page notes (setup = 7 paired fences source;
browser-control = 10) reproduce snippets selectively to stay ≤6. The two oversize pages (acp-agents 6,068w;
browser 5,028w) were split 3-way to keep each note ≤700w.

## Entry Point Decision (inherited from master)

`entry_openclaw_docs.md` is CREATED as a master pre-step (W1, >30 notes corpus-wide). This sub-plan
**contributes its 11 rows** to that entry point under a "Tools" cluster (sub-section: "ACP agents" for notes
1–4, "Agent tools" for notes 5–7, "Browser" for notes 8–11). Each note receives its entry-point back-link at
finalization (this is the primary G7/G8 inbound-link source). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; primary source = `entry_openclaw_docs.md` → all 11):

| New note | Candidate inbound (outside documentation/openclaw/) |
|---|---|
| oc_tools_acp_agents_spawn_bind | `entry_openclaw_docs` · `repo_openclaw_agents` · `repo_openclaw_sessions` |
| oc_tools_acp_agents_runtime | `entry_openclaw_docs` · `repo_openclaw_agents` · `repo_openclaw_security` |
| oc_tools_acp_agents_setup | `entry_openclaw_docs` · `repo_openclaw_extensions` · `term_acp_agent_client_protocol` |
| oc_tools_agent_send | `entry_openclaw_docs` · `repo_openclaw_agents` |
| oc_tools_apply_patch | `entry_openclaw_docs` · `repo_openclaw_agents` · `term_function_calling` |
| oc_tools_brave_search | `entry_openclaw_docs` · `repo_openclaw_extensions` · `term_rag` |
| oc_tools_browser_overview | `entry_openclaw_docs` · `term_browser_automation` · `repo_openclaw_extensions` |
| oc_tools_browser_vision_remote | `entry_openclaw_docs` · `term_cdp` · `repo_openclaw_extensions` |
| oc_tools_browser_security_isolation | `entry_openclaw_docs` · `repo_openclaw_security` · `term_browser_automation` |
| oc_tools_browser_control | `entry_openclaw_docs` · `term_browser_automation` · `repo_openclaw_gateway` |

Plus reciprocal sibling inlinks within the series (notes 1↔2↔3↔4 ACP cluster; 8↔9↔10↔11 browser cluster).

## Pacing Rules (inherited from master)

One execution phase, 11 notes (≤ the ~30 dynamic-workflow fan-out cap). Re-read each source page; reproduce
config/CLI/JSON snippets verbatim and selectively (≤6 per note). One BB per note. Run all 8 gates before
commit; incremental reindex per wave; verify `note_links` + 0 broken links + in-degree ≥1 before committing.
`git pull --rebase --autostash` first; commit+push after the phase; **no Claude co-author trailer**.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass.** Re-read all 7 source pages under `inbox/openclaw_docs/tools/` (acp-agents,
acp-agents-setup, agent-send, apply-patch, brave-search, browser, browser-control) in full and re-measured
word counts (`sed`-strip-YAML `wc -w`): acp-agents **5,999w** (plan 6,068), acp-agents-setup **1,436w**
(1,483), agent-send **640w** (684), apply-patch **237w** (269), brave-search **621w** (651), browser
**4,989w** (5,028), browser-control **2,426w** (2,472). All within 0.7–1.3× of plan estimates → no density
re-split needed; the existing 11-note split (acp-agents ×3, browser ×3, 5 single-page) stands.

**What was locked.** Replaced `## Candidate Cross-References` with `## Per-Note Related Notes Mapping (LOCKED
RAISED floors: **≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (each link with a per-link
relevance statement), grouped **Terms / Docs / Repos / Snippets**. All terms, snippets, repos cited are
`hermes_agent/hermes_*`, `pi/pi_*`, `aws_bedrock/*`, `aws_bedrock_agentcore/*`) with the remaining docs being

**Per-note locked counts (terms / snippets / docs; all-existing repos additional):**

| # | Note | Terms | Snippets | Docs (≥5 existing) | Repos | Floors met |
|---|---|---:|---:|---:|---:|---|
| 1 | oc_tools_acp_agents_overview | 10 | 10 | 11 (8 existing + 3 planned) | 3 | YES |
| 2 | oc_tools_acp_agents_spawn_bind | 9 | 11 | 11 (8 + 3) | 3 | YES |
| 3 | oc_tools_acp_agents_runtime | 9 | 11 | 11 (8 + 3) | 3 | YES |
| 4 | oc_tools_acp_agents_setup | 10 | 11 | 11 (8 + 3) | 3 | YES |
| 5 | oc_tools_agent_send | 8 | 10 | 10 (8 + 2) | 3 | YES |
| 6 | oc_tools_apply_patch | 8 | 10 | 10 (9 + 1) | 2 | YES |
| 7 | oc_tools_brave_search | 8 | 10 | 11 (9 + 2) | 2 | YES |
| 8 | oc_tools_browser_overview | 9 | 11 | 11 (8 + 3) | 3 | YES |
| 9 | oc_tools_browser_vision_remote | 9 | 11 | 11 (8 + 3) | 3 | YES |
| 10 | oc_tools_browser_security_isolation | 9 | 11 | 11 (8 + 3) | 3 | YES |
| 11 | oc_tools_browser_control | 9 | 11 | 11 (8 + 3) | 3 | YES |

**Key corpus discovery (enabled the raised snippet/doc floors).** The vault's existing OpenClaw CODE side is
rich: `snippet_openclaw_acp_*` ×16, `snippet_openclaw_agents/security/gateway/sessions/channels_*` ×100+, plus
a full Hermes parallel-ecosystem family — `snippet_hermes_agent_acp_*` (server/session/events/tools), the
complete `snippet_hermes_agent_tools_browser_*` family (cdp/navigate/screenshot/session/dom/intercept/
supervisor/camofox) + `snippet_hermes_agent_tools_patch_parser` / `web_tools` / `file_tools` / `vision_*`. On
the docs side, `claude_code/cc_*` (mcp/subagent/sandbox/permission/tool/headless), `hermes_agent/hermes_*`
(acp_internals, browser_automation_backends/setup, browser_supervisor, codex_runtime_*, web_search_extract/
provider_plugin, computer_use_macos), `pi/pi_*` and `aws_bedrock/*` agent docs provided the ≥5-existing-doc
floor per note without padding. AWS opensearch `*_search*` docs were surfaced by keyword but **discarded as
ML/retrieval-infra false positives** (not agent web-search tools).

**New-term candidates: 0 (confirmed at re-read, Step 2d re-scan).** The master design decision holds: OpenClaw
vocabulary is digested as `oc_*` doc notes by their home sub-plan, NOT as new `term_dictionary` entries.
Re-scanning the 7 re-read pages for acronyms/method-names introduced after the first H2 / in code comments /
in figure captions surfaced only OpenClaw product/tool vocab that either (a) has an existing term to link
(ACP, MCP, sandbox, CDP, SSRF→`term_ssrf_guard`, browser-automation, websocket, json-rpc, function-calling,
break-glass, deny-first, thread-binding, capability-negotiation) or (b) is tool-specific config vocab with a
doc-note home (acpx, sessions_spawn, --bind/--thread, agent-send, apply-patch envelope, Brave, Browserless/
Browserbase/Notte/Playwright, screenshot-vision, permissionMode). Each was considered and rejected per the
Undigested Terms Plan table above. **Best-fit glossary if any genuinely cross-cutting term ever surfaces:** the
agentic/LLM glossary (already rich) — not triggered here.

**Collision / specificity audit (Step 10.5f, generalized to ALL planned notes).** Ran the doc-note dedup check:
each planned `oc_tools_*` slug is unique (no existing `documentation/openclaw/` folder yet — confirmed
`entry_openclaw_docs` itself is MISSING, planned at W1) and none duplicates an existing **term** note (the
term notes `term_acp_agent_client_protocol` / `term_browser_automation` / `term_mcp` etc. are CONCEPT
definitions; the `oc_tools_*` notes are tool/procedure pages that LINK them — different BB+scope, not
duplicates). No renames needed (these are tool-page slugs, not term slugs). 0 removals.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_to01.md` · Reviewed: 2026-06-21 · Read-only verification against the augmented plan + source re-read + DB.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step + ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 11 notes ≥8 terms (range 8–10), ≥10 snippets, ≥10 docs; every link carries a relevance statement; 0 bare links. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability; single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` — CREATE of `entry_openclaw_docs.md` is the master W1 pre-step (>30 corpus-wide); this sub-plan contributes 11 rows (Tools cluster) + each note gets the entry-point back-link (primary G7/G8 source). DB confirms `entry_openclaw_docs` not yet present (correctly planned). |
| CP4 | Plan size manageable | **PASS** | 11 notes ≤ 30 fan-out cap; single phase. |
| CP5 | Note format derived (not invented) | **PASS** | Format Definition inherited verbatim from master, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` / `## Related Notes` / `## References` / bold footer; YAML field order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group). Matches actual target-precedent dirs. |
| CP6 | Density / BB atomicity (promote splits) | **PASS** | Density Re-Assessment: all 11 notes ≤700w / ≤6cb / one BB; two cap-edge code notes (setup, browser-control) reproduce snippets selectively. No borderline note left un-split (oversize pages already split ×3). |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages this pass: acp-agents 5,999w (plan 6,068; ratio 0.99), browser 4,989w (5,028; 0.99), browser-control 2,426w (2,472; 0.98), acp-agents-setup 1,436w (1,483; 0.97), brave-search 621w (651; 0.95), agent-send 640w (684; 0.94), apply-patch 237w (269; 0.88). All within 0.7–1.3×. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (13 rows, each with a disposition); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, with the inherited multi-source mandate documented for any future term). 0 new captures expected (master design). |
| CP8f | Slug specificity / collision (all-notes dedup) | **PASS** | Step 10.5f generalized to doc notes performed (see Augmentation Report): all `oc_tools_*` slugs unique; no `oc_tools_*` note duplicates an existing term note (concept vs tool-page, link-not-recreate); 0 renames, 0 removals; `entry_openclaw_docs` confirmed MISSING (planned). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` table covers all 11 new notes with ≥1 outside-folder inbound link (primary = `entry_openclaw_docs` → all 11; plus repo/term backlinks + reciprocal sibling inlinks); G7/G8 present in the gate table as a gated execution step, not a recommendation. |

