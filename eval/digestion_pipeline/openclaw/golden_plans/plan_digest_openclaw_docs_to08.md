---
title: Sub-Plan to08 — OpenClaw Docs: Tools (Tokenjuice, Tool Search, Trajectory, TTS, Video, Web)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/tokenjuice", "tools/tool-search", "tools/trajectory", "tools/tts", "tools/video-generation", "tools/web", "tools/web-fetch"]
---

# Sub-Plan to08: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*` prefix), format (YAML order, `## Overview`/`## Related Notes`/`## References`,
> density caps ≤400L/≤2500w/≤6 code, one BB/note), dedup (3-way across term_dictionary + documentation/ + repo_openclaw*),
> 9-GATE validation, cross-references, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master.

## Scope

The last alphabetical slice of the OpenClaw **Tools** section — seven agent-tool reference pages: the **Tokenjuice**
result-compaction plugin, the experimental **Tool Search** runtime (compact large tool catalogs behind search/describe/call),
**Trajectory** export bundles (per-session flight recorder for debugging), **Text-to-speech (TTS)** (14 speech providers,
personas, slash commands, per-channel output), **Video generation** (`video_generate` across 16 backends), **Web search**
(`web_search` + `x_search`, provider matrix, auto-detection, network safety), and **Web fetch** (`web_fetch` HTTP+Readability
extraction with Firecrawl fallback). Priority **P2** (Phase B — features/integration). The code-side counterparts
(`repo_openclaw_extensions_voice_speech`, `repo_openclaw_agents`, the `snippet_openclaw_*`/`snippet_hermes_agent_tools_*`
corpora) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **14,356 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Tokenjuice | tools/tokenjuice | 300 | 6 | 5 | 0 | procedure |
| Tool Search | tools/tool-search | 1,468 | 11 | 10 | 0 | concept |
| Trajectory bundles | tools/trajectory | 1,041 | 11 | 9 | 0 | procedure |
| Text-to-speech (TTS) | tools/tts | 4,709 | 23 | 13 | 6 | procedure (SPLIT ×3: setup vs personas/directives vs output/reference) |
| Video generation | tools/video-generation | 3,116 | 10 | 8 | 6 | procedure (SPLIT ×2: tool/lifecycle vs providers/capabilities) |
| Web search | tools/web | 2,824 | 12 | 11 | 6 | procedure (SPLIT ×2: web_search providers vs x_search/config/network) |
| Web fetch | tools/web-fetch | 898 | 5 | 6 | 0 | procedure |

(Code counts are fence-pairs: raw ``` lines ÷ 2 — tokenjuice 12/2, tool-search 22/2, trajectory 22/2, tts 46/2,
video-generation 20/2, web 24/2, web-fetch 10/2.)

## Content Strategy

- **Prioritize**: the operational decision surfaces that the rest of the OpenClaw tool/runtime corpus references —
  TTS provider+persona configuration, the `web_search` provider matrix + auto-detection precedence + network-safety
  (SSRF) policy, `video_generate` async task lifecycle, the Tool Search code-bridge runtime boundary, and the
  Trajectory bundle schema for debugging.
- **Split**: `tts.md` (4,709w / 23 fences) → 3 notes (setup+providers / personas+directives+commands / output-formats+field-reference);
  `video-generation.md` (3,116w / mixed tool-contract + provider-capability content) → 2 notes; `web.md` (2,824w / `web_search`
  vs `x_search` mixed) → 2 notes. Splits enforce the ≤2,500w / ≤6-code / one-BB caps (Tokenjuice, Tool Search, Trajectory,
  Web fetch each stay single).
- **Skip / link-out**: individual provider pages (`/providers/elevenlabs`, `/providers/openai`, `/tools/firecrawl`,
  `/tools/brave-search`, etc.) belong to `pr*`/sibling `to*` sub-plans — referenced, not redefined; the `exec`/`browser`/
  `media-overview`/`diffs`/`slash-commands` tools are other `to*` pages — linked; voice-vocabulary (`term_text_to_speech`,
  `term_speech_to_text`), `term_mcp`, `term_sandbox`, `term_function_calling`, `term_provider_plugin` are LINKED, not redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_tokenjuice.md` | procedure | tokenjuice.md (all: Enable, What it changes, Verify, Disable) | 350 | The optional Tokenjuice plugin: compacts noisy `exec`/`bash` `tool_result` output via tool-result middleware (without rerunning commands), how to install/enable/verify/disable it, and what it leaves raw. |
| 2 | `oc_tools_tool_search.md` | concept | tool-search.md (all: How a turn runs, Modes, Why this exists, API, Runtime boundary, Config, Prompt and telemetry, E2E validation, Failure behavior) | 700 | Experimental Tool Search runtime: exposes large tool catalogs (OpenClaw/plugin/MCP/client) through one compact search/describe/call surface; code/tools/directory modes, the isolated Node bridge runtime boundary, config, telemetry, and fail-closed behavior. |
| 3 | `oc_tools_trajectory.md` | procedure | trajectory.md (all: Quick start, Access, What gets recorded, Bundle files, Capture location, Disable, Tune flush, Privacy and limits, Troubleshooting) | 650 | Trajectory bundles — OpenClaw's per-session flight recorder: `/export-trajectory` packaging of a redacted support bundle, recorded runtime/transcript events, bundle file schema, capture location env vars, disable/flush tuning, redaction, and size limits. |
| 4 | `oc_tools_tts_setup.md` | procedure | tts.md: intro, Quick start, Supported providers, Configuration (provider tabs), Per-agent voice overrides, Per-user preferences | 700 | Enabling and configuring text-to-speech: the 14-provider matrix + auth, `messages.tts` provider config blocks, per-agent/channel/account override precedence, and per-user local prefs. |
| 5 | `oc_tools_tts_personas_directives.md` | procedure | tts.md: Personas (minimal/full/resolution/how providers use prompts/fallback policy), Model-driven directives, Slash commands | 650 | TTS personas (provider-neutral spoken identities, deterministic resolution, fallback policy), model-emitted `[[tts:...]]` directives, and the `/tts` slash-command surface. |
| 6 | `oc_tools_tts_output_reference.md` | model | tts.md: Output formats (fixed), Auto-TTS behavior, Output formats by channel, Field reference, Agent tool, Gateway RPC | 700 | TTS output contract: per-channel/per-provider audio formats (Opus/MP3/PCM transcoding), Auto-TTS decision flow, the `messages.tts.*` field reference, the `tts` agent tool, and gateway TTS RPC methods. |
| 7 | `oc_tools_video_generation_tool.md` | procedure | video-generation.md: intro/modes, Quick start, How async generation works, Task lifecycle, Tool parameters, Actions, Model selection, Configuration | 700 | The `video_generate` agent tool: async task lifecycle (queued/running/succeeded/failed + session wake), the three runtime modes, tool parameters (content inputs/style/advanced + fallback typed options), actions, model resolution order, and config. |
| 8 | `oc_tools_video_generation_providers.md` | model | video-generation.md: Supported providers, Capability matrix, Provider notes, Provider capability modes, Live tests | 600 | Video-generation provider reference: the 16-backend support + capability matrix (text/image/video modes), per-provider notes, the explicit mode-block capability contract, and live-test coverage. |
| 9 | `oc_tools_web_search.md` | procedure | web.md: intro, Quick start, Choosing a provider, Provider comparison, Auto-detection, Setting up web search, Config (search), Tool parameters, Examples, Tool profiles | 700 | The `web_search` tool: choosing among 14+ search providers, auto-detection precedence order, managed-vs-native (OpenAI/Codex) search, `tools.web.search` config, tool parameters, and tool-profile allowlisting. |
| 10 | `oc_tools_web_x_search_safety.md` | procedure | web.md: Native OpenAI/Codex web search, Network safety, Storing API keys, x_search (config/parameters/example) | 550 | Native OpenAI/Codex hosted web search, the guarded-fetch network-safety (SSRF/fake-IP) policy, API-key/SecretRef storage, and the `x_search` X-posts tool (config, parameters, examples). |
| 11 | `oc_tools_web_fetch.md` | procedure | web-fetch.md (all: Quick start, Tool parameters, How it works, Progress updates, Config, Firecrawl fallback, Trusted env proxy, Limits and safety, Tool profiles) | 600 | The `web_fetch` tool: HTTP GET + Readability main-content extraction (no JS), parameters, fetch/extract/fallback/cache flow, `tools.web.fetch` config, Firecrawl fallback, trusted-env-proxy mode, and SSRF limits/safety. |

## Section Coverage Map

```
tokenjuice.md
├── (intro: what tokenjuice is / tool_result middleware) ─ → note 1 (oc_tools_tokenjuice)
├── Enable the plugin ─────────────────────────────────── → note 1
├── What tokenjuice changes ───────────────────────────── → note 1
├── Verify it is working ──────────────────────────────── → note 1
├── Disable the plugin ────────────────────────────────── → note 1
└── Related (link-out) ────────────────────────────────── → note 1 (References)
tool-search.md
├── (intro: experimental runtime / code bridge example) ─ → note 2 (oc_tools_tool_search)
├── How a turn runs ───────────────────────────────────── → note 2
├── Modes (code/tools/directory) ──────────────────────── → note 2
├── Why this exists ───────────────────────────────────── → note 2
├── API (search/describe/call) ────────────────────────── → note 2
├── Runtime boundary ──────────────────────────────────── → note 2
├── Config ────────────────────────────────────────────── → note 2
├── Prompt and telemetry ──────────────────────────────── → note 2
├── E2E validation ────────────────────────────────────── → note 2
├── Failure behavior ──────────────────────────────────── → note 2
└── Related (link-out) ────────────────────────────────── → note 2 (References)
trajectory.md
├── (intro: per-session flight recorder) ──────────────── → note 3 (oc_tools_trajectory)
├── Quick start (/export-trajectory) ──────────────────── → note 3
├── Access ────────────────────────────────────────────── → note 3
├── What gets recorded ────────────────────────────────── → note 3
├── Bundle files ──────────────────────────────────────── → note 3
├── Capture location ──────────────────────────────────── → note 3
├── Disable capture ───────────────────────────────────── → note 3
├── Tune flush timeout ────────────────────────────────── → note 3
├── Privacy and limits ────────────────────────────────── → note 3
├── Troubleshooting ───────────────────────────────────── → note 3
└── Related (link-out) ────────────────────────────────── → note 3 (References)
tts.md
├── (intro: 14 providers / stt-tts mode) ──────────────── → note 4 (oc_tools_tts_setup)
├── Quick start ───────────────────────────────────────── → note 4
├── Supported providers ───────────────────────────────── → note 4
├── Configuration (provider tabs) ─────────────────────── → note 4
├── Per-agent voice overrides ─────────────────────────── → note 4
├── Personas (+ Minimal/Full/Resolution/How providers
│   use prompts/Fallback policy) ──────────────────────── → note 5 (oc_tools_tts_personas_directives)
├── Model-driven directives ───────────────────────────── → note 5
├── Slash commands ────────────────────────────────────── → note 5
├── Per-user preferences ──────────────────────────────── → note 4
├── Output formats (fixed) ────────────────────────────── → note 6 (oc_tools_tts_output_reference)
├── Auto-TTS behavior ─────────────────────────────────── → note 6
├── Output formats by channel ─────────────────────────── → note 6
├── Field reference ───────────────────────────────────── → note 6
├── Agent tool ────────────────────────────────────────── → note 6
├── Gateway RPC ───────────────────────────────────────── → note 6
├── Service links (link-out) ──────────────────────────── → note 6 (References)
└── Related (link-out) ────────────────────────────────── → notes 4/6 (References)
video-generation.md
├── (intro: 3 runtime modes / video_generate gating) ──── → note 7 (oc_tools_video_generation_tool)
├── Quick start ───────────────────────────────────────── → note 7
├── How async generation works ────────────────────────── → note 7
├── Task lifecycle ────────────────────────────────────── → note 7
├── Tool parameters (Required/Content/Style/Advanced +
│   Fallback and typed options) ───────────────────────── → note 7
├── Actions ───────────────────────────────────────────── → note 7
├── Model selection ───────────────────────────────────── → note 7
├── Supported providers ───────────────────────────────── → note 8 (oc_tools_video_generation_providers)
├── Capability matrix ─────────────────────────────────── → note 8
├── Provider notes ────────────────────────────────────── → note 8
├── Provider capability modes ─────────────────────────── → note 8
├── Live tests ────────────────────────────────────────── → note 8
├── Configuration ─────────────────────────────────────── → note 7
└── Related (link-out) ────────────────────────────────── → notes 7/8 (References)
web.md
├── (intro: web_search/x_search/web_fetch) ────────────── → note 9 (oc_tools_web_search)
├── Quick start ───────────────────────────────────────── → note 9
├── Choosing a provider ───────────────────────────────── → note 9
├── Provider comparison ───────────────────────────────── → note 9
├── Auto-detection (header) ───────────────────────────── → note 9
├── Native OpenAI web search ──────────────────────────── → note 10 (oc_tools_web_x_search_safety)
├── Native Codex web search ───────────────────────────── → note 10
├── Network safety ────────────────────────────────────── → note 10
├── Setting up web search (precedence list) ───────────── → note 9
├── Config (tools.web.search) ─────────────────────────── → note 9
├── Storing API keys ──────────────────────────────────── → note 10
├── Tool parameters ───────────────────────────────────── → note 9
├── x_search (+ config/parameters/example) ────────────── → note 10
├── Examples ──────────────────────────────────────────── → note 9
├── Tool profiles ─────────────────────────────────────── → note 9
└── Related (link-out) ────────────────────────────────── → notes 9/10 (References)
web-fetch.md
├── (intro: HTTP GET + Readability, no JS) ────────────── → note 11 (oc_tools_web_fetch)
├── Quick start ───────────────────────────────────────── → note 11
├── Tool parameters ───────────────────────────────────── → note 11
├── How it works ──────────────────────────────────────── → note 11
├── Progress updates ──────────────────────────────────── → note 11
├── Config ────────────────────────────────────────────── → note 11
├── Firecrawl fallback ────────────────────────────────── → note 11
├── Trusted env proxy ─────────────────────────────────── → note 11
├── Limits and safety ─────────────────────────────────── → note 11
├── Tool profiles ─────────────────────────────────────── → note 11
└── Related (link-out) ────────────────────────────────── → note 11 (References)
```
No orphaned sections. Provider pages, `exec`/`browser`/`media-overview`/`diffs`/`slash-commands` tool pages, and
voice-vocabulary terms are linked (References / Related Notes), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| tts.md (4,709w, 23 fences, 13 H2/6 H3) | notes 4 + 5 + 6 | Far exceeds the 2,500w / 6-code caps and mixes three task clusters: provider setup/config (procedure), personas+directives+commands (procedure), and the output-format/field-reference/RPC contract (model). Three notes keep each ≤700w / ≤6 code with one BB. |
| video-generation.md (3,116w, 10 fences, 8 H2/6 H3, mixed BB) | notes 7 + 8 | Exceeds 2,500w and mixes the `video_generate` tool procedure (lifecycle/parameters/model-selection/config) with the provider-capability reference data (16-backend matrix + capability modes = model BB). Split per word-cap + mixed-BB rules. |
| web.md (2,824w, 12 fences, 11 H2/6 H3) | notes 9 + 10 | Exceeds 2,500w and covers two distinct tools — `web_search` (provider selection/auto-detect/params, procedure) and `x_search` + the cross-cutting native-search / network-safety / key-storage policy. Split keeps each focused and ≤700w. |
| tokenjuice.md / tool-search.md / trajectory.md / web-fetch.md | 1 note each | Under caps (≤1,468w, ≤6 code per note after selective fence reproduction), single coherent BB — no split. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (14,356 words). New `oc_*` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (notes 1, 3, 4, 5, 7, 9, 10, 11) · **concept ×1** (note 2) · **model ×2** (notes 6, 8).
- Est. digest words ~6,900 (avg ~625/note); each note ≤700w, well under the 2,500w cap.
- 78 source code fences distribute across the 11 notes; the heavy config pages (tts 23, web 12, tool-search 11,
  trajectory 11) split / selectively reproduce so every note stays ≤6 code blocks.
- Cross-refs (LOCKED at augment 2026-06-21): each note maps **≥8 relevance-selected `term_dictionary` terms · ≥10

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> `hermes_*` / pi `pi_*` / band `band_*`) — **≥5 existing per note** — with sibling `oc_*` docs in THIS series, which do
> not exist yet and are marked `(planned, this series)`. `entry_openclaw_docs.md` is created as the master W1 pre-step
> (hub back-link, added at finalization, satisfies G7/G8). The executor copies each link + description + relevance verbatim
> false-positives discarded; no padding).

### oc_tools_tokenjuice (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: Tokenjuice is an OpenClaw plugin hooking OpenClaw's tool-result middleware.
- [Context Engine](../../term_dictionary/term_context_engine.md) — OpenClaw's context-budget/assembly subsystem; relevance: the page links Context engine and compaction is the budget motivation for trimming tool output.
- [Context Compression](../../term_dictionary/term_context_compression.md) — shrinking context content to fit budget; relevance: Tokenjuice compacts noisy `exec`/`bash` results, the canonical context-compression move.
- [Compaction](../../term_dictionary/term_compaction.md) — collapsing transcript/tool history to save tokens; relevance: Tokenjuice is a tool-result-level compaction applied before output re-enters the session.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM-emitted tool invocations + their results; relevance: Tokenjuice rewrites the returned `tool_result` payload, not the command.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — agent tool running shell/code; relevance: Tokenjuice targets `exec`/`bash` tool results specifically.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated runtime for tool execution; relevance: applies to OpenClaw embedded runs and Codex app-server dynamic tools where exec runs.
- [LLM](../../term_dictionary/term_llm.md) — the model consuming tool results; relevance: compacting output reduces the tokens the LLM ingests on the next turn.

**Docs**
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — how Claude Code executes tools + shapes results; relevance: parallels Tokenjuice's tool-result-middleware behavior.
- [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — built-in tool catalog incl. Bash; relevance: identifies the `exec`/`bash` tool family Tokenjuice compacts.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — Hermes tool-result/media handling; relevance: sibling-ecosystem tool-result post-processing analog.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — what tool I/O is captured; relevance: tool-result volume is what Tokenjuice reduces.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes/OpenClaw-family plugin install/enable model; relevance: Tokenjuice is installed/enabled as a plugin via the same `plugins.entries` config.
- [oc_tools_tool_search](oc_tools_tool_search.md) (planned, this series) — compacting tool catalogs behind search; relevance: sibling context-saving runtime feature.
- [oc_tools_trajectory](oc_tools_trajectory.md) (planned, this series) — per-session flight recorder; relevance: records the raw vs compacted tool results Tokenjuice changes.
- [oc_tools_exec](oc_tools_exec.md) (planned, to03) — the `exec` tool reference; relevance: Tokenjuice acts on `exec` output (page's primary link-out).
- [oc_concepts_context_engine](oc_concepts_context_engine.md) (planned, co02) — OpenClaw context-engine concept; relevance: the page's "Related" links Context engine as the budget rationale.
- [oc_tools_thinking](oc_tools_thinking.md) (planned, to07) — thinking-levels tool; relevance: page's "Related" cross-link.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw core; relevance: Tokenjuice hooks OpenClaw's tool-result middleware.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded agent runtime; relevance: tool-result trimming runs inside the embedded harness session.

**Snippets**
- [snippet_hermes_agent_core_tool_result_classification](../../code_snippets/snippet_hermes_agent_core_tool_result_classification.md) — classifies/normalizes tool results; relevance: the exact "which results to leave raw vs compact" decision Tokenjuice makes.
- [snippet_hermes_agent_tools_terminal_exec](../../code_snippets/snippet_hermes_agent_tools_terminal_exec.md) — terminal/exec tool implementation; relevance: produces the `exec`/`bash` results Tokenjuice trims.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — OpenClaw exec orchestration; relevance: the command-run path whose output is post-processed.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — shaping code-exec results; relevance: result-shaping analog to Tokenjuice's middleware.
- [snippet_hermes_agent_tools_terminal_bg](../../code_snippets/snippet_hermes_agent_tools_terminal_bg.md) — background terminal output handling; relevance: another exec-output stream subject to compaction.
- [snippet_hermes_agent_tools_terminal_session](../../code_snippets/snippet_hermes_agent_tools_terminal_session.md) — terminal session lifecycle; relevance: where noisy `git status`-style output originates.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows cmd shim for exec; relevance: another exec backend feeding tool results.
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — context-engine delegation; relevance: the budget subsystem Tokenjuice helps relieve.
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hook points; relevance: middleware/hook mechanism Tokenjuice plugs into.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset/tool definitions; relevance: identifies the exec/bash tools whose output is compacted.

### oc_tools_tool_search (9t · 11s · 11d)

**Terms**
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of available agent tools; relevance: Tool Search exposes a large catalog (OpenClaw/plugin/MCP/client) behind one surface.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — compact metadata describing a tool; relevance: Tool Search indexes compact descriptors and `describe()` loads the full schema.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool servers; relevance: the catalog includes MCP tools through the session MCP runtime.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `search`/`describe`/`call` reshape how the model selects + calls tools.
- [Agent as a Tool](../../term_dictionary/term_agent_as_a_tool.md) — exposing capability through a tool surface; relevance: client/app capabilities are passed to Codex as dynamic tools.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: the code bridge runs in an isolated Node subprocess with no FS/network grants.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integrations; relevance: per-provider modes (code/tools/directory) target providers that should not receive code.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: `openclaw.tools.call` crosses the bridge back into the Gateway where policy/approval apply.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent context; relevance: large-catalog runs (many MCP/client tools) are the subagent/orchestration use case.

**Docs**
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — Claude Code MCP tool search; relevance: direct cross-stack analog of OpenClaw Tool Search over MCP catalogs.
- [cc_sdk_tool_search](../claude_code/cc_sdk_tool_search.md) — SDK tool-search surface; relevance: the SDK-level discover/describe/call pattern Tool Search mirrors.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool inventory; relevance: the kind of catalog Tool Search compacts.
- [cc_agent_sdk_tool_execution](../claude_code/cc_agent_sdk_tool_execution.md) — how the SDK executes tools; relevance: parallels "every real tool call returns to OpenClaw."
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — defining custom tools/schemas; relevance: the schemas Tool Search defers loading until `describe`.
- [hermes_tools_toolsets](../hermes_agent/hermes_tools_toolsets.md) — toolset grouping/gating; relevance: policy-filtered catalog assembly that Tool Search indexes.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex-native tool surfaces; relevance: page contrasts OpenClaw Tool Search vs Codex-native code mode/tool search.
- [oc_tools_tokenjuice](oc_tools_tokenjuice.md) (planned, this series) — tool-result compaction; relevance: sibling context-saving runtime feature.
- [oc_tools_multi_agent_sandbox_tools](oc_tools_multi_agent_sandbox_tools.md) (planned, to05) — sandbox tools; relevance: page's "Related" link; shares the isolated-runtime boundary.
- [oc_tools_exec](oc_tools_exec.md) (planned, to03) — exec tool; relevance: page's "Related" link; an eligible catalog tool.
- [oc_plugins_building_plugins](oc_plugins_building_plugins.md) (planned, pl01) — building plugins; relevance: page's "Related" link; plugin tools are part of the catalog.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded runner; relevance: builds the effective catalog and exposes the code bridge.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension surface; relevance: plugin tools enter the searchable catalog.

**Snippets**
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — OpenClaw tool-catalog assembly; relevance: the exact effective-catalog build (resolve policy, list OpenClaw/plugin/MCP/client tools).
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry implementation; relevance: registry of eligible tools that Tool Search indexes.
- [snippet_hermes_agent_tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — calling an MCP tool; relevance: `openclaw.tools.call` dispatch to MCP tools through the bridge.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — registering tools over ACP; relevance: client-provided tools supplied for a run.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — isolated code-exec sandbox; relevance: the `tool_search_code` isolated Node subprocess boundary.
- [snippet_hermes_agent_core_tool_executor_concurrent](../../code_snippets/snippet_hermes_agent_core_tool_executor_concurrent.md) — concurrent tool execution; relevance: final calls still run through normal policy/execution.
- [snippet_hermes_agent_model_tools_introspection](../../code_snippets/snippet_hermes_agent_model_tools_introspection.md) — tool introspection/describe; relevance: the `describe(id)` exact-schema load step.
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — probing model/tool capabilities; relevance: mode fallback (code→tools) when the runtime cannot launch the child process.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: structured fallback tools (`tool_search`/`tool_describe`/`tool_call`).
- [snippet_openclaw_agents_tool_loop_detectors_repeat](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_repeat.md) — repeat/loop guards on tool calls; relevance: telemetry counts search/describe/call operations Tool Search records.

### oc_tools_trajectory (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: trajectory capture is OpenClaw's per-session flight recorder.
- [Agent Trajectory](../../term_dictionary/term_agent_trajectory.md) — recorded timeline of an agent run; relevance: the page IS the trajectory-bundle export feature.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — instrumenting agent runs for debugging; relevance: trajectory bundles answer "what prompt/tools/errors occurred."
- [Compaction](../../term_dictionary/term_compaction.md) — transcript compaction events; relevance: recorded transcript events include compactions + model changes.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable / secret data; relevance: bundles redact credentials, image data, workspace/home paths.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls + results; relevance: recorded events include tool calls, tool results, and tool schemas.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — provider prompt-cache metadata; relevance: `artifacts.json` records usage + prompt-cache metadata.
- [Model Router](../../term_dictionary/term_model_router.md) — model fallback/routing; relevance: `model.fallback_step` events record source/next model + failure reason.

**Docs**
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — what session data is captured; relevance: equivalent capture surface (prompts, tools, usage) in Claude Code.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel telemetry pipeline; relevance: structured runtime-event timeline analog.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry privacy/redaction; relevance: parallels trajectory redaction + privacy-and-limits guidance.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation/redaction; relevance: bundles redact credentials + secret-like fields before writing.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session lifecycle events; relevance: `session.started`/`session.ended` runtime events recorded.
- [oc_tools_diffs](oc_tools_diffs.md) (planned, to02) — diffs tool; relevance: page's "Related" link.
- [oc_concepts_session](oc_concepts_session.md) (planned, co06) — session management; relevance: page's "Related" link; sidecars pruned with session entries.
- [oc_gateway_diagnostics](oc_gateway_diagnostics.md) (planned, gw02) — Gateway diagnostics bundle; relevance: page contrasts `/diagnostics` (broad bundle) vs `/export-trajectory` (per-session).
- [oc_tools_tool_search](oc_tools_tool_search.md) (planned, this series) — runtime tool surface; relevance: sibling runtime/debug feature; tool schemas appear in `tools.json`.
- [oc_concepts_compaction](oc_concepts_compaction.md) (planned, co02) — compaction concept; relevance: compaction events appear in the recorded timeline.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session storage/lifecycle; relevance: trajectory sidecars are written beside session files + pruned with them.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: runtime events are emitted during agent runs + flushed at cleanup.

**Snippets**
- [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — trajectory event schema; relevance: the `traceSchema`/`schemaVersion` JSONL marker + event types.
- [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — redacted export pipeline; relevance: the exact redact-then-export bundle behavior.
- [snippet_hermes_agent_trajectory_canonicalize](../../code_snippets/snippet_hermes_agent_trajectory_canonicalize.md) — canonicalize trajectory records; relevance: building `events.jsonl`/`session-branch.json` consistently.
- [snippet_hermes_agent_trajectory_config_dataclasses](../../code_snippets/snippet_hermes_agent_trajectory_config_dataclasses.md) — trajectory config dataclasses; relevance: flush timeout, size caps, capture-dir env-var config.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redaction pattern matching; relevance: best-effort secret detection the page warns about.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event reconstruction; relevance: transcript events rebuilt from the active session branch.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: `session.started`/`session.ended` runtime events.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: runtime-event logging + flush-timeout logging.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — classifying host session files; relevance: locating/pruning `.trajectory.jsonl` + pointer files.
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — observability export; relevance: alternative trajectory/observability sink analog.

### oc_tools_tts_setup (9t · 11s · 11d)

**Terms**
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing audio from text; relevance: the page IS TTS setup across 14 providers.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integration; relevance: each speech provider (ElevenLabs/OpenAI/Azure…) is a configured provider plugin.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI APIs; relevance: most providers are external hosted TTS APIs requiring keys.
- [Persona](../../term_dictionary/term_persona.md) — stable spoken identity; relevance: setup includes per-agent persona pinning + global persona config.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent speech I/O mode; relevance: TTS is the speech-output half of Talk's `stt-tts` mode.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — spoken assistant interaction; relevance: TTS delivers spoken replies in chat/voice channels.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multiple I/O modalities; relevance: audio reply attachment alongside text output.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: TTS config lives under `messages.tts` in OpenClaw config.
- [LLM](../../term_dictionary/term_llm.md) — reply-generating model; relevance: auto-summary uses a summary model before synthesizing long replies.

**Docs**
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS provider matrix; relevance: directly parallel provider/auth setup in the sibling stack.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode enablement; relevance: enabling the speech-output mode TTS belongs to.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio reply settings; relevance: per-channel audio delivery configuration analog.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice I/O in Claude Code; relevance: cross-stack speech-feature setup reference.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider selection/auth; relevance: fallback-provider precedence when multiple TTS providers are configured.
- [oc_tools_tts_personas_directives](oc_tools_tts_personas_directives.md) (planned, this series) — personas + directives; relevance: split sibling covering persona resolution this note references.
- [oc_tools_tts_output_reference](oc_tools_tts_output_reference.md) (planned, this series) — output contract + field reference; relevance: split sibling with the `messages.tts.*` field reference.
- [oc_tools_media_overview](oc_tools_media_overview.md) (planned, to05) — media tools overview; relevance: page's "Related" link.
- [oc_concepts_models](oc_concepts_models.md) (planned, co04) — model/provider catalog; relevance: summary model + provider model ids used in setup.
- [oc_providers_elevenlabs](oc_providers_elevenlabs.md) (planned, pr03) — ElevenLabs provider page; relevance: most-reliable hosted provider; provider page link-out.
- [oc_providers_azure_speech](oc_providers_azure_speech.md) (planned, pr01) — Azure Speech provider; relevance: key-free/native-Opus provider documented in the matrix.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech extension code; relevance: implements the TTS provider integrations.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: provider auth/config plumbing reused by TTS.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS integration; relevance: the canonical provider block (`apiKey`/`model`/`speakerVoiceId`) shown in setup.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: Local CLI / key-free provider path in the matrix.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: provider selection + fallback precedence on enable.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: end-to-end synth pipeline the config drives.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram speech provider; relevance: sibling speech-provider config pattern (auth + model).
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: TTS as the output half of voice mode.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider integration; relevance: OpenAI is a primary TTS provider (also used for auto-summary).
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: OpenRouter TTS provider (`hexgrad/kokoro-82m`) in the matrix.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription/STT; relevance: the `stt-tts` mode counterpart of TTS.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call/Talk manager; relevance: Talk session provider selection referenced in setup precedence.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — sending media attachments; relevance: TTS attaches generated audio to the reply.

### oc_tools_tts_personas_directives (9t · 10s · 10d)

**Terms**
- [Persona](../../term_dictionary/term_persona.md) — stable spoken identity; relevance: the page defines personas, deterministic resolution, and fallback policy.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: personas + `[[tts:...]]` directives shape each TTS request.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: persona prompt fields are provider-neutral; each provider maps them differently.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — spoken assistant identity; relevance: personas give the assistant a consistent spoken character.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — speech I/O mode; relevance: persona/directive resolution applies on the TTS output path of voice mode.
- [LLM](../../term_dictionary/term_llm.md) — the model emitting directives; relevance: model-emitted `[[tts:...]]` directives override voice/model/speed per reply.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-controlled behavior; relevance: directives are a model-side control channel for the TTS path.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: `/tts` slash commands + persona prefs are OpenClaw-side surfaces.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modality output; relevance: `[[tts:text]]` expressive cues appear in audio only.

**Docs**
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — provider persona/prompt mapping; relevance: how providers consume persona prompt fields.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI/commands; relevance: slash-command surface analog to `/tts`.
- [hermes_slash_commands_messaging](../hermes_agent/hermes_slash_commands_messaging.md) — slash commands; relevance: the `/tts ...` command family + authorization rules.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — speech feature config; relevance: cross-stack speech persona/voice reference.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider selection order; relevance: explicit-first provider selection in persona resolution.
- [oc_tools_tts_setup](oc_tools_tts_setup.md) (planned, this series) — providers + config; relevance: split sibling defining the providers personas bind to.
- [oc_tools_tts_output_reference](oc_tools_tts_output_reference.md) (planned, this series) — output + field reference; relevance: split sibling with `modelOverrides`/persona field definitions.
- [oc_tools_slash_commands](oc_tools_slash_commands.md) (planned, to07) — slash-command framework; relevance: page's "Related" link; `/tts` is registered here.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) (planned, co07) — system prompt/identity; relevance: personas are a spoken-identity layer over the system identity.
- [oc_concepts_messages](oc_concepts_messages.md) (planned, co04) — message lifecycle; relevance: directive stripping from visible text during streaming block delivery.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech extension; relevance: implements persona resolution + directive parsing per provider.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: strips `[[tts:...]]` directives from streamed assistant text before the channel.

**Snippets**
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing + provider merge; relevance: the explicit-first provider selection + config-merge order persona resolution uses.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs provider binding; relevance: persona provider-specific bindings (voice id, seed, voiceSettings).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: persona fields map to OpenAI `instructions` only when none configured.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: persona/directive resolution on the speech-output path.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: where directive overrides are applied before synthesis.
- [snippet_hermes_agent_core_skill_preprocessing](../../code_snippets/snippet_hermes_agent_core_skill_preprocessing.md) — preprocessing assistant output; relevance: stripping inline directive tags before display, analog to `[[tts:...]]` handling.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregation; relevance: per-provider directive-key support varies; aggregator routes accordingly.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription pipeline; relevance: STT counterpart sharing the voice persona/config plane.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — Talk/voice-call manager; relevance: Talk session-scoped provider/persona selection.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound reply runner; relevance: streaming block delivery strips directives before the channel sees them.

### oc_tools_tts_output_reference (8t · 10s · 10d)

**Terms**
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the page is the TTS output contract + `messages.tts.*` field reference.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription counterpart; relevance: the `tts` tool + Talk path pair with STT in `stt-tts` mode.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: per-provider output formats (Opus/MP3/PCM) + field defaults.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC method protocol; relevance: gateway TTS RPC methods (`tts.status`, `tts.convert`, …).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw transcodes per-channel output formats with `ffmpeg`.
- [LLM](../../term_dictionary/term_llm.md) — reply model; relevance: Auto-TTS decision flow summarizes long model replies before synthesis.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — speech I/O; relevance: Talk/telephony PCM output is the realtime voice-mode delivery target.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modality; relevance: audio attachment vs native voice-note vs PCM stream per channel capability.

**Docs**
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — provider output formats; relevance: per-provider format/transcode contract analog.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — per-channel media output; relevance: channel-capability-driven voice-note vs audio-file selection.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice gateway streaming; relevance: streamed Opus playback for voice channels.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — speech I/O; relevance: cross-stack audio output reference.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool reference; relevance: the `tts` agent tool + media delivery contract.
- [oc_tools_tts_setup](oc_tools_tts_setup.md) (planned, this series) — provider config; relevance: split sibling defining the providers whose formats this note tabulates.
- [oc_tools_tts_personas_directives](oc_tools_tts_personas_directives.md) (planned, this series) — personas + directives; relevance: split sibling; directive keys appear in this field reference.
- [oc_channels_feishu](oc_channels_feishu.md) (planned, ch02) — Feishu channel; relevance: Feishu/WhatsApp Ogg/Opus transcoding behavior documented here.
- [oc_concepts_session](oc_concepts_session.md) (planned, co06) — session/Talk; relevance: Talk session-scoped provider selection for telephony PCM.
- [oc_gateway_protocol](oc_gateway_protocol.md) (planned, gw05) — gateway RPC protocol; relevance: gateway TTS RPC methods belong to the gateway protocol surface.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech extension; relevance: implements per-provider output formats + ffmpeg transcoding.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: telephony PCM/ulaw delivery target for TTS output.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs synth + format; relevance: Opus/MP3 output-format selection per channel.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: PCM/ulaw telephony output path.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing + fallback; relevance: `/tts status` fallback diagnostics + per-attempt detail.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: the STT side of the Talk media stream this contract serves.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media send; relevance: `sendVoice` OGG/MP3/M4A delivery format constraints.
- [snippet_hermes_agent_gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp dispatch; relevance: Baileys `ptt:true` Ogg/Opus voice-note payload.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — channel media normalization; relevance: media normalization applied to TTS attachments per channel.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: format/transcode stage producing the channel-appropriate output.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — send attachment; relevance: the `tts` tool returns an audio attachment for reply delivery.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: gateway RPC + Talk delivery of synthesized audio.

### oc_tools_video_generation_tool (8t · 11s · 11d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool invocation; relevance: `video_generate` is an agent tool with typed parameters/actions.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the tool resolves a provider/model and dispatches to it.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI; relevance: video backends are external hosted generation APIs.
- [Model Router](../../term_dictionary/term_model_router.md) — model resolution/fallback; relevance: model selection order (param→primary→fallbacks→auto-detect) with automatic fallback.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative video/image model class; relevance: the underlying generative method behind the providers.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modality I/O; relevance: text/image/video reference inputs select the runtime mode.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw submits the task, wakes the session on completion, and persists media.
- [LLM](../../term_dictionary/term_llm.md) — the calling agent; relevance: the agent decides params + reports completion through normal reply mode.

**Docs**
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: direct cross-stack analog of the `video_generate` tool + provider contract.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider plugin; relevance: sibling media-generation tool sharing the async dispatch model.
- [cc_agent_sdk_tool_execution](../claude_code/cc_agent_sdk_tool_execution.md) — async/long-running tool execution; relevance: parallels the async task lifecycle + session wake.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing/fallback; relevance: model resolution + automatic candidate fallback.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback chains; relevance: capability-based skip + fallback-layer typed-options checks.
- [oc_tools_video_generation_providers](oc_tools_video_generation_providers.md) (planned, this series) — provider/capability reference; relevance: split sibling with the 16-backend matrix this tool resolves.
- [oc_tools_image_generation](oc_tools_image_generation.md) (planned, to04) — image-generation tool; relevance: sibling media tool; page's "Related" via media overview.
- [oc_automation_tasks](oc_automation_tasks.md) (planned, au01) — background tasks; relevance: page's "Related" link; `openclaw tasks` tracks async video jobs.
- [oc_concepts_models](oc_concepts_models.md) (planned, co04) — model catalog; relevance: page's "Related" link; provider/model ids resolved here.
- [oc_gateway_config_agents](oc_gateway_config_agents.md) (planned, gw01) — agent-defaults config; relevance: `agents.defaults.videoGenerationModel` lives here (page's "Related").
- [oc_tools_media_overview](oc_tools_media_overview.md) (planned, to05) — media tools overview; relevance: video generation is one of the media tools.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: submits the async task + wakes the session on completion.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: implements the per-provider video backends.

**Snippets**
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: the `video_generate` tool params/actions/lifecycle implementation.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: provider resolution + dispatch + fallback on a video request.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: sibling media tool with the same async dispatch shape.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: parallel provider-fallback dispatch pattern.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision/reference image input; relevance: reference-image inputs that select `imageToVideo` mode.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — send media attachment; relevance: posting the generated video back to the conversation.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound reply runner; relevance: completion-event reply delivery + idempotent fallback send.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media transcript pipeline; relevance: managed media storage + size-cap handling for generated video.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — model catalog/resolution; relevance: provider/model resolution order for the tool.

### oc_tools_video_generation_providers (9t · 10s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the page is the 16-backend provider/capability reference.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI; relevance: every backend (Veo/Sora/Runway/Seedance/Kling…) is an external service.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of provider models; relevance: per-provider default models + model ids tabulated here.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative video model class; relevance: the generative method behind the listed video models.
- [Stable Diffusion](../../term_dictionary/term_stable_diffusion.md) — diffusion image/video gen exemplar; relevance: ComfyUI workflow-driven generation is diffusion-graph based.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modality; relevance: capability matrix covers text/image/video reference modes per provider.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — visual-content modeling; relevance: image/video reference inputs are vision-conditioned generation.
- [LLM](../../term_dictionary/term_llm.md) — provider model family; relevance: providers are configured like other model providers in OpenClaw.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw declares the explicit per-mode capability contract providers must implement.

**Docs**
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: the provider-capability contract analog in the sibling stack.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: the hosted-provider auth/model landscape.
- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider plugin model; relevance: how a provider declares models + capabilities.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider; relevance: parallel media-provider capability declaration.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: capability-driven candidate selection across the matrix.
- [oc_tools_video_generation_tool](oc_tools_video_generation_tool.md) (planned, this series) — the tool; relevance: split sibling that resolves + dispatches to these providers.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) (planned, co04) — model-provider concept; relevance: page's "Related" (BytePlus international) link.
- [oc_providers_runway](oc_providers_runway.md) (planned, pr07) — Runway provider; relevance: provider page link-out; `gen4_aleph` videoToVideo note.
- [oc_providers_google](oc_providers_google.md) (planned, pr04) — Google/Veo provider; relevance: provider page link-out; Veo capability notes.
- [oc_providers_fal](oc_providers_fal.md) (planned, pr03) — fal provider; relevance: queue-backed provider with Seedance reference-to-video.
- [oc_providers_minimax](oc_providers_minimax.md) (planned, pr05) — MiniMax provider; relevance: provider page link-out; resolution-normalization note.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: implements the 16 video backends + capability blocks.

**Snippets**
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: per-provider capability check + dispatch across the matrix.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: consumes the per-mode capability declarations.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: parallel media-provider capability/dispatch pattern.
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — capability probing; relevance: the per-mode (`generate`/`imageToVideo`/`videoToVideo`) capability contract.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregation; relevance: OpenRouter async `/videos` API backend in the matrix.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider integration pattern; relevance: canonical provider-config/auth shape reused by video backends.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — reference image/video input; relevance: per-provider reference-input limits in the matrix.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: routing image/video-conditioned requests to capable providers.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — model catalog; relevance: provider default-model + model-id catalog this note tabulates.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tool/provider config; relevance: `videoGenerationModel.primary`/`fallbacks` provider config.

### oc_tools_web_search (9t · 11s · 11d)

**Terms**
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation / web grounding; relevance: `web_search` grounds the agent in live web results.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→ranked results; relevance: the page is a web-search tool with a provider matrix + filters.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: 14+ search providers are configured provider plugins with auto-detection.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI; relevance: AI-synthesized providers (Gemini/Grok/Kimi/Perplexity) are external services.
- [Knowledge Base](../../term_dictionary/term_knowledge_base.md) — external grounded knowledge source; relevance: web search is the open-web knowledge source for the agent.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool call; relevance: `web_search` is an agent tool with structured parameters + tool-profile allowlisting.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw owns provider selection, caching, and managed-vs-native routing.
- [LLM](../../term_dictionary/term_llm.md) — consuming model; relevance: native OpenAI/Codex models use hosted `web_search` when no managed provider is pinned.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-modality; relevance: results feed the model alongside other context (and x_search image/video understanding).

**Docs**
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web search + extraction; relevance: direct cross-stack analog of the `web_search` tool.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: the provider-plugin model behind the search provider matrix.
- [cc_web_overview](../claude_code/cc_web_overview.md) — web tooling overview; relevance: cross-stack web-search/fetch feature overview.
- [cc_web_quickstart](../claude_code/cc_web_quickstart.md) — web tool quickstart; relevance: parallel enable/configure quick start.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tools incl. WebSearch; relevance: identifies the managed web-search tool family.
- [oc_tools_web_x_search_safety](oc_tools_web_x_search_safety.md) (planned, this series) — native search + network safety + x_search; relevance: split sibling covering native + SSRF policy.
- [oc_tools_web_fetch](oc_tools_web_fetch.md) (planned, this series) — web_fetch tool; relevance: split sibling; `group:web` includes both; page link-out.
- [oc_tools_brave_search](oc_tools_brave_search.md) (planned, to01) — Brave provider; relevance: page's provider card link.
- [oc_tools_exa_search](oc_tools_exa_search.md) (planned, to03) — Exa provider; relevance: page's provider card link.
- [oc_tools_browser](oc_tools_browser.md) (planned, to01) — web browser tool; relevance: page directs JS-heavy/login sites to the browser tool.
- [oc_plugins_codex_harness](oc_plugins_codex_harness.md) (planned, pl02) — Codex harness; relevance: Codex Hosted Search provider card link.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: exposes `web_search` as a managed dynamic tool and caches queries.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension surface; relevance: search providers are bundled/installed plugins declaring web-search contracts.

**Snippets**
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin; relevance: the web-search/fetch plugin implementation analog.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool definitions; relevance: `web_search`/`x_search`/`web_fetch` tool params + `group:web`.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog assembly; relevance: managed `web_search` enters the catalog via tool profiles/allowlists.
- [snippet_hermes_agent_skills_research_arxiv](../../code_snippets/snippet_hermes_agent_skills_research_arxiv.md) — research skill using web search; relevance: a downstream consumer of web-search grounding.
- [snippet_hermes_agent_skills_research_polymarket](../../code_snippets/snippet_hermes_agent_skills_research_polymarket.md) — research skill; relevance: another web-search-driven research workflow.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — model/provider catalog; relevance: provider-id validation against declared web-search providers.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tools config; relevance: `tools.web.search` config + provider selection.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP request build; relevance: native OpenAI hosted `web_search` request path.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound HTTP base; relevance: provider HTTP calls go through the guarded outbound path.
- [snippet_brp_agent_tools_crawl](../../code_snippets/snippet_brp_agent_tools_crawl.md) — crawl/search tool; relevance: structured web result-fetching pattern.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills/tool registry; relevance: tool-profile allowlisting (`group:web`) registration.

### oc_tools_web_x_search_safety (9t · 11s · 11d)

**Terms**
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — outbound proxy / DNS resolution control; relevance: trusted-env-proxy + fake-IP-range network-safety policy.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side request forgery defense; relevance: the guarded-fetch SSRF policy is the core of this note.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: native OpenAI/Codex hosted search + xAI `x_search` are provider-owned behaviors.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI; relevance: native OpenAI/Codex/xAI hosted search are external services.
- [RAG](../../term_dictionary/term_rag.md) — web grounding; relevance: native hosted + `x_search` ground the model in web/X content.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — controlled outbound API surface; relevance: managed provider calls + key storage via SecretRef pass through controlled paths.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw mediates native-vs-managed mutual exclusion + fail-closed allowlists.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool call; relevance: `x_search` is an agent tool with structured filters/parameters.
- [LLM](../../term_dictionary/term_llm.md) — model running hosted search; relevance: native OpenAI/Codex models run hosted `web_search` within bounded turns.

**Docs**
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web tool security/limits; relevance: direct cross-stack analog of the SSRF/network-safety policy.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — network access controls; relevance: outbound-network allow/deny + proxy parallels.
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — Grok/X search; relevance: the `x_search` X-posts tool + xAI credential reuse.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: storing API keys / SecretRef handling.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — network isolation; relevance: blocking private/loopback/metadata destinations.
- [oc_tools_web_search](oc_tools_web_search.md) (planned, this series) — web_search tool; relevance: split sibling; this note is the native-search + safety half.
- [oc_tools_web_fetch](oc_tools_web_fetch.md) (planned, this series) — web_fetch tool; relevance: the SSRF opt-ins here are referenced for `web_fetch` too.
- [oc_security_network_proxy](oc_security_network_proxy.md) (planned, se01) — network-proxy security; relevance: the trusted-proxy/SSRF policy in the security corpus.
- [oc_plugins_codex_harness](oc_plugins_codex_harness.md) (planned, pl02) — Codex harness; relevance: native Codex hosted search delegates to the app-server.
- [oc_gateway_secrets](oc_gateway_secrets.md) (planned, gw05) — secrets/SecretRef; relevance: API-key SecretRef storage for search providers.
- [oc_providers_xai](oc_providers_xai.md) (planned, pr09) — xAI provider; relevance: `x_search` uses the xAI Responses auth profile.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/guarded-fetch code; relevance: implements the SSRF guard + fake-IP-range allowances.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: native OpenAI/Codex + xAI `x_search` provider implementations.

**Snippets**
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — security audit of runtime; relevance: guarded-fetch / network-safety enforcement analog.
- [snippet_hermes_agent_skills_research_polymarket](../../code_snippets/snippet_hermes_agent_skills_research_polymarket.md) — research skill (X/web); relevance: an `x_search`/web-search-style research workflow.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool definitions; relevance: `x_search` parameters + `group:web` allowlisting.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — permission relay; relevance: native-vs-managed mutual exclusion + fail-closed domain restrictions.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel security audit; relevance: bounded-access enforcement pattern for sensitive surfaces.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound HTTP base; relevance: the guarded outbound fetch path for managed provider calls.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP build; relevance: native OpenAI hosted `web_search` request construction.
- [snippet_hermes_agent_skills_research_arxiv](../../code_snippets/snippet_hermes_agent_skills_research_arxiv.md) — research skill; relevance: web-grounding consumer paired with native/managed search.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: native OpenAI Responses hosted `web_search` provider path.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tools config; relevance: `tools.web.search.openaiCodex` + provider config.

### oc_tools_web_fetch (8t · 10s · 11d)

**Terms**
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — trusted outbound proxy + DNS; relevance: `useTrustedEnvProxy` lets the proxy resolve DNS instead of local pinning.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — SSRF defense; relevance: blocks private/internal hostnames, re-checks redirects, narrow fake-IP opt-ins.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — fetching/extracting content; relevance: `web_fetch` does HTTP GET + Readability main-content extraction.
- [RAG](../../term_dictionary/term_rag.md) — grounding via fetched content; relevance: extracted page content grounds the agent.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: Firecrawl fallback provider + provider auto-detection.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool call; relevance: `web_fetch` is an agent tool with params + tool-profile allowlisting.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host; relevance: OpenClaw applies SSRF checks, caching, and sandboxed-vs-non-sandboxed provider rules.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — controlled outbound surface; relevance: Firecrawl `baseUrl` lockdown + SecretRef API-key handling.

**Docs**
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web tool security/limits; relevance: direct analog of `web_fetch` limits + SSRF safety.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — network access controls; relevance: outbound proxy + private-host blocking parallels.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — fetch + content extraction; relevance: HTTP fetch + readable-content extraction analog.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation; relevance: page directs JS-heavy/login pages to the browser instead of `web_fetch`.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — browser backends; relevance: the full-browser fallback for sites `web_fetch` can't handle.
- [oc_tools_web_search](oc_tools_web_search.md) (planned, this series) — web_search tool; relevance: split sibling; `group:web` includes both; page link-out.
- [oc_tools_web_x_search_safety](oc_tools_web_x_search_safety.md) (planned, this series) — native search + SSRF; relevance: shared SSRF/network-safety policy.
- [oc_tools_firecrawl](oc_tools_firecrawl.md) (planned, to03) — Firecrawl tools; relevance: page's Firecrawl-fallback link-out.
- [oc_tools_browser](oc_tools_browser.md) (planned, to01) — web browser tool; relevance: page's "Related" link for JS-heavy sites.
- [oc_gateway_trusted_proxy_auth](oc_gateway_trusted_proxy_auth.md) (planned, gw07) — trusted proxy auth; relevance: the trusted-env-proxy mode in the gateway corpus.
- [oc_gateway_secrets](oc_gateway_secrets.md) (planned, gw05) — secrets/SecretRef; relevance: Firecrawl API-key SecretRef + fail-fast startup.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: exposes `web_fetch` (enabled by default) + cache.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/guarded-fetch; relevance: SSRF checks, redirect re-checks, private-host blocking.

**Snippets**
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin; relevance: the fetch/extract/fallback implementation analog.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool definitions; relevance: `web_fetch` parameters (`url`/`extractMode`/`maxChars`) + `group:web`.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session tool; relevance: the full-browser path for JS-heavy pages `web_fetch` punts to.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigate; relevance: fallback navigation for login/JS sites.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser dispatch; relevance: browser-fallback dispatch when fetch is insufficient.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime security audit; relevance: SSRF/network-safety enforcement analog.
- [snippet_hermes_agent_gw_platform_base_outbound](../../code_snippets/snippet_hermes_agent_gw_platform_base_outbound.md) — outbound HTTP base; relevance: the guarded HTTP GET path with DNS pinning + redirect checks.
- [snippet_brp_agent_tools_crawl](../../code_snippets/snippet_brp_agent_tools_crawl.md) — crawl/fetch tool; relevance: HTTP fetch + content-extraction pattern.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM extraction; relevance: main-content extraction analog to Readability.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| Tokenjuice | OpenClaw plugin name → digested as `oc_tools_tokenjuice.md` (doc note). Not a term. |
| Tool Search / tool catalog / `tool_search_code` | OpenClaw runtime feature → `oc_tools_tool_search.md`. Link existing `term_tool_registry`, `term_mcp`. Not new terms. |
| Trajectory bundle / `/export-trajectory` / flight recorder | OpenClaw debugging feature → `oc_tools_trajectory.md`. Link `term_compaction`. Not a term. |
| TTS / text-to-speech / persona / `[[tts:...]]` directive | Link existing `term_text_to_speech`, `term_persona`; feature specifics → `oc_tools_tts_*`. Not new terms. |
| Speech providers (ElevenLabs, Azure Speech, Inworld, MiniMax, Volcengine, …) | Provider names → documented as config in `oc_tools_tts_setup.md`; each has a `pr*` provider page. Not promoted to term notes. Link `term_provider_plugin`, `term_third_party_genai_services`. |
| `video_generate` / imageToVideo / videoToVideo / capability modes | OpenClaw tool feature → `oc_tools_video_generation_*`. Link `term_function_calling`, `term_model_catalog`. Not new terms. |
| Video providers (Veo/Sora/Runway/Seedance/Kling, …) | Provider/model names → config in `oc_tools_video_generation_providers.md`. Not term notes. |
| `web_search` / `x_search` / `web_fetch` / auto-detection / SSRF policy | OpenClaw tool features → `oc_tools_web_*`. Link `term_rag`, `term_reverse_proxy`, `term_provider_plugin`. Not new terms. |
| Web/search providers (Brave, Exa, Tavily, Firecrawl, Perplexity, SearXNG, …) | Provider names → config in `oc_tools_web_search.md`; each has a sibling `to*`/`pr*` page. Not term notes. |
| **token efficiency / context-budget compaction (cross-cutting)** | NEW-TERM CANDIDATE (low confidence): a reusable agent-engineering concept (compacting tool output to save context tokens) surfacing in tokenjuice + tool-search + trajectory. **Default disposition: link existing `term_context_engine` / `term_compaction`** rather than create. Augment Step 2d makes the final call; if promoted, capture `term_token_efficiency` via `/tessellum-capture-term-note` + add to `acronym_glossary_a.md` (agentic/AI glossary). Expected outcome: 0 new terms. |

Per master design decision: OpenClaw vocabulary terms are digested as `oc_*` doc notes by their home sub-plan, NOT as
new `term_dictionary` entries. The only `term_dictionary` interaction is **linking existing** terms. **Expected: 0 new
`term_dictionary` captures.** Augment re-runs Step 2d to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms expected).** to08 authors zero `term_dictionary` notes — all OpenClaw vocabulary is digested into
`oc_*` doc notes; existing terms are linked. If augment Step 2d promotes the lone `term_token_efficiency` candidate
2026-06-20), and an `acronym_glossary_a.md` entry. Inherited from master.

## Per-Phase Validation Gate (G1–G9)

Single execution phase (11 notes, P2). All gates must PASS before commit (inherited from master).

| Gate | Check | Tooling |
|---|---|---|
| G1 | Format: YAML field order/forbidden fields, `## Overview`/`## Related Notes`/`## References`, footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: each note's claims diff against `inbox/openclaw_docs/tools/<page>.md` (no invention) | manual diff vs source |
| G3 | Density + Coverage: ≤400L/≤2500w/≤6 code, one BB; every H2/H3 in Section Coverage Map mapped | density script (below) |
| G4 | Cross-Reference: ≥6 relevance-selected term links + sibling/repo/doc/snippet links, each with a relevance statement | manual + `note_links` query |
| G5 | Ghost-reference detect + redirect: 0 links to non-existent note_ids | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix: 0 broken relative paths | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + inlinks below) | `note_links` query |
| G8 | In-degree ≥1 (anti-island) for every new note | `notes.in_degree` after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_tokenjuice oc_tools_tool_search oc_tools_trajectory oc_tools_tts_setup oc_tools_tts_personas_directives oc_tools_tts_output_reference oc_tools_video_generation_tool oc_tools_video_generation_providers oc_tools_web_search oc_tools_web_x_search_safety oc_tools_web_fetch"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION: $n -> $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density (frontmatter-excluded word count + fence-pair count)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done
# G1 YAML frontmatter (whole folder)
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5/G6/G8 after incremental reindex
bash scripts/update_notes_database.sh --force
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "${indeg:-0}" -ge 1 ] || echo "ISLAND (in_degree<1): $n"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code (selective) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_tokenjuice | procedure | 350 | 3 | ✅ |
| 2 | oc_tools_tool_search | concept | 700 | 5 | ✅ |
| 3 | oc_tools_trajectory | procedure | 650 | 5 | ✅ |
| 4 | oc_tools_tts_setup | procedure | 700 | 6 | ✅ (split from 23-fence source; selective config blocks) |
| 5 | oc_tools_tts_personas_directives | procedure | 650 | 5 | ✅ |
| 6 | oc_tools_tts_output_reference | model | 700 | 4 | ✅ |
| 7 | oc_tools_video_generation_tool | procedure | 700 | 5 | ✅ |
| 8 | oc_tools_video_generation_providers | model | 600 | 3 | ✅ |
| 9 | oc_tools_web_search | procedure | 700 | 6 | ✅ |
| 10 | oc_tools_web_x_search_safety | procedure | 550 | 5 | ✅ |
| 11 | oc_tools_web_fetch | procedure | 600 | 4 | ✅ |

No note approaches the caps. The code-heavy `tts.md` (23 fences), `web.md` (12), `tool-search.md` (11), and
`trajectory.md` (11) split / selectively reproduce config so each note stays ≤6 code blocks (config snippets reproduced
verbatim where load-bearing, abbreviated where repetitive across provider tabs).

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step; `building_block: navigation`)
under a "Tools" section, "to08" cluster. Suggested grouping: Tokenjuice + Tool Search + Trajectory (runtime/debug),
TTS ×3 (speech output), Video generation ×2 (media), Web search/x_search/fetch ×3 (web). Each note receives its
entry-point back-link at finalization (satisfies G7/G8). No separate entry point is created for to08 (it rolls up
into the master hub).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; primary anchor is `entry_openclaw_docs.md`):

- `entry_openclaw_docs.md` (planned, W1) → **all 11 notes** (primary anti-island anchor).
- `repo_openclaw_extensions_voice_speech` → notes 4, 5, 6 (TTS).
- `repo_openclaw_extensions_llm_providers` → notes 7, 8 (video providers), 10 (web providers).
- `repo_openclaw_agents` → notes 2, 3, 9, 11 (runtime/tool catalog/web).
- `repo_openclaw_security` → notes 10, 11 (network safety / SSRF).
- `repo_openclaw_sessions` → note 3 (trajectory / session lifecycle).
- `term_text_to_speech` → notes 4, 5, 6; `term_tool_registry` → note 2; `term_reverse_proxy` → notes 10, 11;
  `term_rag` → notes 9, 10, 11; `term_persona` → notes 4, 5.
- Sibling docs (reciprocal): `cc_mcp_tool_search` → note 2; `cc_data_usage_and_telemetry` → note 3;
  `cc_web_security_and_limits` → notes 10, 11.

## Pacing Rules (inherited from master)

One execution phase (11 notes, ≤30 fan-out cap). Re-read each source page before authoring its note(s); reproduce
config snippets verbatim where load-bearing; one BB per note. Incremental reindex; verify `note_links` + 0 broken
links + in_degree ≥1 before commit. `git pull --rebase --autostash` first; commit + push after the phase; no Claude
co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the PLAN-stage `## Candidate Cross-References` with `## Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)` at the RAISED floors: **≥8 term_dictionary terms · ≥10 code_snippets · ≥10 docs under
`resources/documentation/` per note**, relevance-selected (all 7 source pages re-read 2026-06-21 from
plus sibling `oc_*` docs in this series marked `(planned, this series)` / cross-series `(planned, <sub-plan>)`. Repos
`- [Name](relpath.md) — what it is; relevance: why THIS note`. Summary Statistics cross-ref line updated to the new
floors. Source word counts re-measured (tokenjuice 248, tool-search 1,403, trajectory 985, tts 4,666, video-generation
3,074, web 2,766, web-fetch 849) — all within ±10% of the plan's Source table estimates; no re-split needed.

**Per-note counts (terms / snippets / docs; floors met):**

| Note | Terms | Snippets | Docs | Repos | Floors met (≥8/≥10/≥10) |
|---|---:|---:|---:|---:|---|
| oc_tools_tokenjuice | 8 | 10 | 10 (5 existing) | 2 | ✅ |
| oc_tools_tool_search | 9 | 11 | 11 (7 existing) | 2 | ✅ |
| oc_tools_trajectory | 8 | 11 | 10 (5 existing) | 2 | ✅ |
| oc_tools_tts_setup | 9 | 11 | 11 (5 existing) | 2 | ✅ |
| oc_tools_tts_personas_directives | 9 | 10 | 10 (5 existing) | 2 | ✅ |
| oc_tools_tts_output_reference | 8 | 10 | 10 (5 existing) | 2 | ✅ |
| oc_tools_video_generation_tool | 8 | 11 | 11 (5 existing) | 2 | ✅ |
| oc_tools_video_generation_providers | 9 | 10 | 11 (5 existing) | 2 | ✅ |
| oc_tools_web_search | 9 | 11 | 11 (5 existing) | 2 | ✅ |
| oc_tools_web_x_search_safety | 9 | 11 | 11 (5 existing) | 2 | ✅ |
| oc_tools_web_fetch | 8 | 10 | 11 (5 existing) | 2 | ✅ |

**New-term candidate + best-fit glossary.** The only candidate is `term_token_efficiency` (token-budget tool-output
augment promotes it, best-fit glossary is the agentic/AI `acronym_glossary_a.md`; capture via `/tessellum-capture-term-note`
with a collision check vs `term_context_engine`/`term_context_compression`/`term_compaction`. **Expected new
`term_dictionary` captures: 0.** Consistent with the master's design decision (OpenClaw vocabulary → `oc_*` doc notes, not
new term notes).

**Re-read findings (Step 2d).** No newly-surfaced undigested terms beyond the candidate above; the re-read confirmed the
section coverage map is complete (every H2/H3 mapped), no omission, no over-compression. The split decisions
(tts ×3, video-generation ×2, web ×2) hold against the measured word/fence counts.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets, ≥10 docs), relevance-selected | **PASS** | Per-Note Related Notes Mapping has all 11 notes at ≥8t/≥10s/≥10d, each link carries a `relevance:` statement; counts table above. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7/G8 Discoverability + in-degree anti-island. |
| CP4 | Size | **PASS** | 11 notes, single execution phase, ≤30 fan-out cap; well under the 30-note threshold. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master (derived from existing `cc_*`/`pi_*` doc corpora): YAML field order, `## Overview`/`## Related Notes`/`## References`, footer, one BB/note, density caps. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 11 notes ≤700w / ≤6 code; no borderline (>300-line) cases; splits (tts×3, video×2, web×2) keep each note one-BB and under caps. |
| CP7 | Sources measured | **PASS** | Re-measured 2026-06-21: 248/1,403/985/4,666/3,074/2,766/849 words vs plan estimates 300/1,468/1,041/4,709/3,116/2,824/898 — all ratios 0.92–1.0 (within ±30%); no under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned: link existing / digest as `oc_*` / 1 NEW-candidate rejected); `## Term-Note Authoring Requirements` present (N/A, 0 new terms; master mandate inherited if promoted). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 11 notes with outside-folder inbound links (primary anchor `entry_openclaw_docs.md` → all 11; plus repo/term/sibling-doc reciprocal inlinks); G8 in-degree ≥1 check in validation scripts. |

**RESULT: 9/9 CP pass → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
