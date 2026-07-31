---
title: Sub-Plan B21C — Claude Code Docs: SDK TypeScript Reference
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/typescript", "agent-sdk/typescript-v2-preview"]
---

# Sub-Plan B21C: SDK TypeScript Reference

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The two TypeScript Agent-SDK pages: the **full V1 API reference** (`agent-sdk/typescript.md` — install,
functions, `Options`, the `Query`/`WarmQuery` objects, message/hook/tool/permission/sandbox type
catalogs) and the short **removed-V2 session-API reference** (`agent-sdk/typescript-v2-preview.md`).
P3 (Phase C) — a language-specific API reference that *consumes* the cross-cutting SDK concepts already
owned by B19A–B21A (agent loop, sessions, custom tools, MCP, hooks, permissions, structured outputs,
file checkpointing, sandboxing, cost tracking). Those concept pages are **linked, not duplicated**; this
sub-plan documents only the **TypeScript-surface shape** (function signatures, option keys, type names,
method tables) that the language reference adds on top.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 15,815 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the TS-specific API surface a developer needs to write SDK code — the `query()` entry
  point + async-generator return shape, the `Options` configuration keys, the runtime control methods on
  the `Query` object, and the type-name catalogs (messages / hooks / tools / permissions). These have no
  language-agnostic home elsewhere.
- **Group**: split the giant reference page by **API surface area**, not by source H2 order, because one
  source H2 ("Types", "Message Types", "Tool Input Types"+"Tool Output Types") is a flat catalog of 50+
  type names that a single note can summarize as a reference index without re-listing every field. Keep
  the removed-V2 page as one standalone deprecation note.
- **Reference-note compression**: this is a vendor API reference, so each digest note is a **navigable
  summary/index** (signatures, key option keys, method table, type-name catalog with one-line gloss + a
  pointer back to the live source for exhaustive field tables), NOT a verbatim re-dump of all 352 code
  fences. This keeps every note inside the density caps while staying faithful (G2).
- **Skip / link-out (own other sub-plans)**: the *concepts* behind each surface — agent loop → B19A;
  sessions / `sessionStore` / session-storage → B19B; streaming + structured outputs + user input → B19C;
  custom tools (`tool()`) concept + MCP → B20A; skills / slash commands / subagents → B20B; hooks /
  permissions / file checkpointing → B20C; hosting / secure deployment / observability / cost tracking →
  B21A; the Python mirror → B21B. Referenced via links, never duplicated.
- **Glossary / terms**: no new `term_dictionary` captures — TS API symbols are documented in the `cc_`
  notes; existing concept terms (MCP, subagent, structured output, function calling, …) are linked (Pattern B).

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of `code.claude.com/docs/en/agent-sdk/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| typescript | /agent-sdk/typescript | 14,376 | 176 | 11 | 134 (+55 H4) | procedure (API reference) |
| typescript-v2-preview | /agent-sdk/typescript-v2-preview | 1,439 | 11 | 5 | 9 | procedure (deprecated/migration) |

> Code count is `grep -c '^```' / 2` (352 fences ÷ 2 = 176 for typescript.md; 22 ÷ 2 = 11 for v2-preview).

> **H2 lists (document order):**
> - **typescript**: Installation (H3 Compile to a single executable) · Functions (H3 `query()`, `startup()`, `tool()`, `createSdkMcpServer()`, `listSessions()`, `getSessionMessages()`, `getSessionInfo()`, `renameSession()`, `tagSession()`, `resolveSettings()`) · Types (H3 `Options`, `Query` object, `WarmQuery`, `SDKControlInitializeResponse`, `AgentDefinition`, `AgentMcpServerSpec`, `SettingSource`, `PermissionMode`, `CanUseTool`, `PermissionResult`, `ToolConfig`, `McpServerConfig`, `SdkPluginConfig`) · Message Types (H3 `SDKMessage` + ~14 variants) · Hook Types (H3 `HookEvent`, `HookCallback`, `HookCallbackMatcher`, `HookInput`, `BaseHookInput`, `HookJSONOutput`) · Tool Input Types (H3 `ToolInputSchemas` + ~28 per-tool schemas) · Tool Output Types (H3 `ToolOutputSchemas` + ~28 per-tool schemas) · Permission Types (H3 `PermissionUpdate`, `PermissionBehavior`, `PermissionUpdateDestination`, `PermissionRuleValue`) · Other Types (H3 `ApiKeySource`, `SdkBeta`, `SlashCommand`, `ModelInfo`, `AgentInfo`, `McpServerStatus`, `Usage`, `ModelUsage`, `CallToolResult`, `ThinkingConfig`, `SpawnedProcess`, `RewindFilesResult`, + ~20 streaming/event message types) · Sandbox Configuration (H3 `SandboxSettings`, `SandboxNetworkConfig`, `SandboxFilesystemConfig`, Permissions Fallback for Unsandboxed Commands) · See also
> - **typescript-v2-preview**: Installation · Quick start (H3 One-shot prompt, Basic session, Multi-turn conversation, Session resume, Cleanup) · API reference (H3 `unstable_v2_createSession()`, `unstable_v2_resumeSession()`, `unstable_v2_prompt()`, SDKSession interface) · Feature availability · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_typescript_installation.md` | procedure | typescript: Installation, Compile to a single executable | 450 | `npm install @anthropic-ai/claude-agent-sdk`; bundled native binary as optional dep; `Native CLI binary not found` recovery via `pathToClaudeCodeExecutable`; `bun build --compile` + `extractFromBunfs()` single-executable workaround; cross-compile/Windows notes. ≤3 code blocks. |
| 2 | `cc_sdk_typescript_query_function.md` | procedure | typescript: Functions → `query()`, `startup()`, `WarmQuery` | 500 | The `query()` entry point: signature, `prompt: string \| AsyncIterable<SDKUserMessage>`, returns a `Query` async-generator; `startup()` pre-warm + `WarmQuery` handle to move spawn/init cost off the critical path; `await using` cleanup. Loop concept → B19A. ≤4 code blocks. |
| 3 | `cc_sdk_typescript_options.md` | procedure | typescript: Types → `Options` (+ Handle slow/stalled API responses) | 650 | The `Options` config object: the high-traffic option keys grouped by purpose (model/effort/thinking; tools/allowedTools/disallowedTools; agents/agent; mcpServers/strictMcpConfig; permissionMode/canUseTool; hooks; sessionId/resume/forkSession/persistSession; sandbox; settings/settingSources; maxTurns/maxBudgetUsd). `env` replace-not-merge gotcha + the API-timeout/stall env vars. Exhaustive table → live source. ≤4 code blocks. |
| 4 | `cc_sdk_typescript_query_object.md` | procedure | typescript: Types → `Query` object, Methods, `applyFlagSettings()`, `WarmQuery` methods | 600 | The runtime control surface on the returned `Query`: `interrupt()`, `rewindFiles()`, `setPermissionMode()`/`setModel()`, `applyFlagSettings()` (flag-settings layer, mid-session which-keys-apply rules), MCP server control (`reconnectMcpServer`/`toggleMcpServer`/`setMcpServers`), introspection (`supportedCommands/Models/Agents`, `mcpServerStatus`, `accountInfo`), `streamInput()`, `stopTask()`, `close()`. Streaming-input-only constraints. ≤3 code blocks. |
| 5 | `cc_sdk_typescript_sdk_functions.md` | procedure | typescript: Functions → `tool()`, `createSdkMcpServer()`, `listSessions()`, `getSessionMessages()`, `getSessionInfo()`, `renameSession()`, `tagSession()`, `resolveSettings()` | 600 | The non-`query()` exported helpers: in-process MCP tool authoring (`tool()` with Zod schema + `ToolAnnotations`, `createSdkMcpServer()`); session discovery/mutation (`listSessions`/`getSessionMessages`/`getSessionInfo` → `SDKSessionInfo`/`SessionMessage`; `renameSession`/`tagSession`); `resolveSettings()` settings-merge inspector (alpha). Concepts → B20A/B19B. ≤4 code blocks. |
| 6 | `cc_sdk_typescript_message_and_hook_types.md` | model | typescript: Message Types, Hook Types | 550 | Type-name catalog #1: the `SDKMessage` discriminated union (assistant/user/result/system/partial/compact-boundary/permission-denied/… variants) a consumer pattern-matches on, plus the streaming/event message types from "Other Types" (status, task-progress, hook-lifecycle, rate-limit). Hook types: `HookEvent`, `HookCallback`, `HookCallbackMatcher`, `HookInput`/`BaseHookInput`, `HookJSONOutput`. Hooks concept → B20C. One-line gloss per type + source pointer. ≤2 code blocks. |
| 7 | `cc_sdk_typescript_tool_and_permission_types.md` | model | typescript: Tool Input Types, Tool Output Types, Permission Types, Other Types (Agent/Model/Mcp metadata) | 600 | Type-name catalog #2: the per-tool `ToolInputSchemas`/`ToolOutputSchemas` keyed maps (Bash/Edit/Read/Write/Glob/Grep/Agent/WebFetch/WebSearch/Workflow/Task*/…), the permission types (`PermissionMode`, `CanUseTool`, `PermissionResult`, `PermissionUpdate`, `PermissionBehavior`, `PermissionRuleValue`, `ToolConfig`), and config/metadata types (`AgentDefinition`, `McpServerConfig`, `SdkPluginConfig`, `ModelInfo`, `AgentInfo`, `Usage`, `CallToolResult`, `ThinkingConfig`). Tools/permissions concepts → B20A/B20C. Catalog + source pointer. ≤2 code blocks. |
| 8 | `cc_sdk_typescript_v2_session_api_removed.md` | procedure | typescript-v2-preview: whole page (Installation, Quick start, API reference, Feature availability) | 450 | The removed V2 session API: `unstable_v2_createSession/resumeSession/prompt`, `SDKSession` interface, send()/stream() split; removed in SDK 0.3.142; pin `@0.2` only for legacy 0.2.x maintenance; migration path = `query()` + `AsyncIterable<SDKUserMessage>` + `options.resume` (→ note 2, B19B). ≤4 code blocks. |

**Estimate: 8 notes** — procedure ×6 (notes 1–5, 8), model ×2 (notes 6, 7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (15,815 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,400 (avg ~550/note). Code blocks per note ≤4 (curated representative snippets, not the 176/11 source fences).
- **Building Block Distribution**: procedure ×6 (notes 1,2,3,4,5,8 — install/usage API surface) · model ×2 (notes 6,7 — the type-catalog "shape of the data" notes). No concept/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_sdk_typescript_installation` (6 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — the language the package targets; this note is the install/build procedure for the TypeScript edition of the Agent SDK, so the language term is its direct anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the SDK bundles the native Claude Code CLI binary as an optional dependency, so this install note is fundamentally about packaging the Claude Code runtime for embedding.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the SDK is the programmatic form of the Claude Code agent harness; installing it is installing the harness as a library dependency.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the SDK is how developers embed an autonomous coding agent into their own applications, the category this install procedure enables.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — a comparable "install an SDK to embed agent capability" workflow; contextualizes the npm-package + native-binary install pattern this note documents.
- [Strands Agents SDK](../../term_dictionary/term_strands_agents_sdk.md) — a sibling agent-building SDK with its own install/dependency model, contextualizing the package-manager + optional-dependency approach used here.

### 2. `cc_sdk_typescript_query_function` (7 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — the note documents a TypeScript async-generator function signature (`query(): Query extends AsyncGenerator`), so the language's type-system features are central to how the entry point is used.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `query()` is the single programmatic entry point into the Claude Code agent harness; calling it spins up the harness loop, making this the term it instantiates.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `query()` spawns and drives the Claude Code subprocess; the note is the API door to the Claude Code engine from TypeScript.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the streamed `SDKMessage` sequence from `query()` is the agent autonomously gathering context, acting, and verifying — the autonomous-agent behavior surfaced as an async generator.
- [ReAct](../../term_dictionary/term_react.md) — each yielded message is one observe/act step of the reason-act-observe loop the `query()` generator streams; ReAct formalizes that interleaving.
- [Context Window](../../term_dictionary/term_context_window.md) — `startup()`/`WarmQuery` pre-warm the subprocess and its context state so the first prompt avoids cold init; the note's latency optimization sits on top of context-window setup cost.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — the message stream `query()` returns interleaves `tool_use`/`tool_result` blocks (the function-calling round trips), which the consumer iterates over turn by turn.

### 3. `cc_sdk_typescript_options` (7 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — `Options` is a TypeScript interface with ~50 typed keys; the note documents that typed configuration surface, anchored by the language.
- [Claude Code](../../term_dictionary/term_claude_code.md) — every `Options` key tunes a Claude Code behavior (model, tools, permissions, MCP, sandbox), so this is the configuration map of the Claude Code engine from TypeScript.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `permissionMode`, `allowedTools`/`disallowedTools`, `canUseTool`, and `allowDangerouslySkipPermissions` in `Options` are exactly the graduated-trust controls governing how much the agent may do without asking.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — the `mcpServers`/`strictMcpConfig` option keys wire MCP servers into the session, a first-class capability this `Options` note configures.
- [Subagent](../../term_dictionary/term_subagent.md) — the `agents`/`agent`/`agentProgressSummaries`/`forwardSubagentText` keys programmatically define and surface subagents, so the subagent term grounds those option rows.
- [Context Window](../../term_dictionary/term_context_window.md) — `maxTurns`, `maxBudgetUsd`, `thinking`/`maxThinkingTokens`, and `systemPrompt` (`excludeDynamicSections` for prompt-cache reuse) are all context/budget-shaping options, tying the note to the context-window trade-off lens.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — the permission options, `disallowedTools` context removal, `sandbox`, and the stall/timeout env vars are the runtime guardrails an embedding app sets via `Options`.

### 4. `cc_sdk_typescript_query_object` (6 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — the `Query` object is a TypeScript interface extending `AsyncGenerator` with extra methods; the note documents that typed control surface.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the `Query` methods (`interrupt`, `setModel`, `setMcpServers`, `accountInfo`, …) are the live runtime-control API of a running Claude Code session.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `setPermissionMode()` and `applyFlagSettings({ permissions })` let the host tighten or loosen the trust level mid-session, the dynamic side of graduated trust this note exposes.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — `rewindFiles(userMessageId)` restores files to a prior message state (with `enableFileCheckpointing`), the SDK's file-checkpoint/rewind capability the term describes.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — `reconnectMcpServer`, `toggleMcpServer`, and `setMcpServers` dynamically manage the session's MCP servers, so the MCP term grounds those control methods.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `streamInput()` feeds user messages and `stopTask()` halts a running tool/task; the object mediates the tool-use round-trip stream, the function-calling mechanism.

### 5. `cc_sdk_typescript_sdk_functions` (7 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — these are the SDK's exported TypeScript helper functions with typed signatures and return types (`SDKSessionInfo`, `SessionMessage`, `ResolvedSettings`), anchored by the language.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — `tool()` and `createSdkMcpServer()` author an in-process MCP server exposing custom tools to the agent, making MCP the core mechanism these functions implement.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `tool()` defines a callable tool (name, Zod input schema, handler returning `CallToolResult`); this is precisely a function/tool-use definition the model can invoke.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — `tool()`'s (name, description, input schema, annotations) tuple is a tool descriptor — the structured declaration that tells the model what a tool does and how to call it.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `listSessions`/`getSessionMessages`/`renameSession`/`tagSession`/`resolveSettings` read and mutate Claude Code's own session store and settings, so the product term grounds these management helpers.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — the session-discovery functions read persisted JSONL transcripts and metadata (`SDKSessionInfo`, `fileSize`, `lastModified`), the persistence mechanism these helpers query.
- [Structured Output](../../term_dictionary/term_structured_output.md) — `tool()` uses a Zod schema to constrain tool input shape and `resolveSettings()` returns a typed `ResolvedSettings`/provenance object, the schema-constrained structured-output discipline these functions apply.

### 6. `cc_sdk_typescript_message_and_hook_types` (6 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — `SDKMessage` is a TypeScript discriminated union consumers narrow by `type`; this catalog note documents that union and the hook callback types, anchored by the language's tagged-union feature.
- [Claude Code](../../term_dictionary/term_claude_code.md) — every message variant (assistant/result/system/compact-boundary/permission-denied/task-progress) is an event Claude Code emits over the SDK stream, so the product term grounds the catalog.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — the streaming/event message types (status, task-started/progress/updated, hook-started/progress/response, rate-limit) are agent lifecycle/state-transition signals, exactly the category this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — assistant messages carry `tool_use` blocks and user/result messages carry `tool_result`/usage; pattern-matching these variants is how a consumer reads the function-calling round trips.
- [Compaction](../../term_dictionary/term_compaction.md) — the `SDKCompactBoundaryMessage` variant marks where the SDK auto-compacted the context, so the compaction term grounds that specific message type in the catalog.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — the SDK surfaces work as a stream of typed event messages the host reacts to (hooks fire on `HookEvent`s), the event-driven pattern this note's types implement.

### 7. `cc_sdk_typescript_tool_and_permission_types` (6 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — `ToolInputSchemas`/`ToolOutputSchemas` are keyed TypeScript maps and the permission/config types are unions/interfaces; this catalog documents that typed shape, anchored by the language.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — the per-tool input/output schema maps (Bash/Edit/Read/Grep/WebSearch/Agent/Task*) are the typed argument and result shapes of each callable tool — the function-calling contract surface this note catalogs.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — each `ToolInputSchemas[Name]` entry is the typed input descriptor for a built-in tool, the structured tool-declaration this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `PermissionMode`, `CanUseTool`, `PermissionResult`, `PermissionUpdate`, `PermissionBehavior`, and `PermissionRuleValue` are the typed primitives of the graduated-trust permission system the note catalogs.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — `McpServerConfig`, `CallToolResult`, and `SdkPluginConfig` are the typed config/result shapes for wiring MCP servers and plugins, grounding those rows of the catalog.
- [Subagent](../../term_dictionary/term_subagent.md) — `AgentDefinition`, `AgentInfo`, and the `Agent`/`TaskCreate`/`TaskOutput` tool schemas are the typed shapes for programmatic subagents, so the subagent term grounds those catalog entries.

### 8. `cc_sdk_typescript_v2_session_api_removed` (6 term notes)
- [TypeScript](../../term_dictionary/term_typescript.md) — this is the TypeScript-only removed V2 session API (`SDKSession`, `unstable_v2_*` functions, `await using`); the language grounds the deprecation note.
- [Claude Code](../../term_dictionary/term_claude_code.md) — V2 was an experimental session interface to the Claude Code engine; the note documents its removal and the supported `query()` replacement for driving Claude Code.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — V2's `createSession`/`resumeSession` + session-ID resume is a session-persistence pattern; the migration path (`options.resume`) preserves that persistence on the V1 API.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — both V2 sessions and the replacement `query()` are ways to drive the agent harness across multiple turns, the runtime this deprecated API wrapped.
- [Idempotency](../../term_dictionary/term_idempotency.md) — the migration note documents a version-boundary change (V2 removed at 0.3.142, pin `@0.2` for legacy); idempotency/safe-repeat discipline frames the deterministic version-pinning the note prescribes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the V2 and V1 multi-turn session patterns both run an autonomous coding agent across exchanges, the category this API served before removal.

## Section Coverage Map

```
typescript.md
├── Installation ──────────────────────── → note 1 (cc_sdk_typescript_installation)
│   └── Compile to a single executable ── → note 1
├── Functions
│   ├── query() ───────────────────────── → note 2 (cc_sdk_typescript_query_function)
│   ├── startup() ─────────────────────── → note 2
│   ├── tool() ────────────────────────── → note 5 (cc_sdk_typescript_sdk_functions)
│   ├── createSdkMcpServer() ──────────── → note 5
│   ├── listSessions() / getSessionMessages() / getSessionInfo() → note 5
│   ├── renameSession() / tagSession() ── → note 5
│   └── resolveSettings() ─────────────── → note 5
├── Types
│   ├── Options (+ slow/stalled responses) → note 3 (cc_sdk_typescript_options)
│   ├── Query object / Methods / applyFlagSettings() → note 4 (cc_sdk_typescript_query_object)
│   ├── WarmQuery ─────────────────────── → note 2 (returned by startup) / methods in note 4
│   ├── SDKControlInitializeResponse ──── → note 4 (initializationResult return)
│   ├── AgentDefinition / AgentMcpServerSpec → note 7 (tool & permission/config types)
│   ├── SettingSource ─────────────────── → note 3 (Options.settingSources) / note 5 (resolveSettings)
│   ├── PermissionMode / CanUseTool / PermissionResult / ToolConfig → note 7
│   ├── McpServerConfig / SdkPluginConfig → note 7
├── Message Types (SDKMessage + variants) → note 6 (cc_sdk_typescript_message_and_hook_types)
├── Hook Types (HookEvent/Callback/Input/Output) → note 6 (concept → B20C)
├── Tool Input Types (ToolInputSchemas) ─ → note 7 (cc_sdk_typescript_tool_and_permission_types)
├── Tool Output Types (ToolOutputSchemas) → note 7
├── Permission Types (PermissionUpdate/Behavior/RuleValue) → note 7 (concept → B20C)
├── Other Types
│   ├── streaming/event messages (SDKStatusMessage … SDKPromptSuggestionMessage) → note 6
│   ├── ModelInfo/AgentInfo/Usage/ModelUsage/CallToolResult/ThinkingConfig/SpawnedProcess → note 7
│   └── SlashCommand/ApiKeySource/SdkBeta/RewindFilesResult/McpSetServersResult → note 4 (Query returns) / note 7
├── Sandbox Configuration (SandboxSettings/Network/Filesystem/Fallback) → note 3 (Options.sandbox) (concept → B05B sandboxing / B21A secure-deployment)
└── See also ──────────────────────────── → link-out (B21B python.md, cli-reference B03B, common-workflows B01B)
typescript-v2-preview.md
├── Installation ──────────────────────── → note 8 (cc_sdk_typescript_v2_session_api_removed)
├── Quick start (one-shot/basic/multi-turn/resume/cleanup) → note 8
├── API reference (unstable_v2_* + SDKSession) → note 8
├── Feature availability ──────────────── → note 8
└── See also ──────────────────────────── → link-out (note 2 query(), B19B sessions)
```
No orphaned sections. (The Sandbox-Configuration **concept** is owned by B05B/B21A; this sub-plan covers only its `Options.sandbox` TS-shape, linked out for the rest.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| typescript.md (14.4Kw, 11 H2, 134 H3 — far over 2,500w cap) | notes 1–7 + link-outs | one mega API-reference page; split by API surface area: install (1), `query()` entry (2), `Options` config (3), `Query` runtime control (4), exported helper functions (5), message/hook type catalog (6), tool/permission/config type catalog (7). Concepts behind each surface link out to B19A–B21A. |
| typescript.md "Types"+"Message"+"Tool Input"+"Tool Output"+"Permission"+"Other" (6 catalog H2, 50+ type names) | notes 6 (model) + 7 (model) + folded config/return types into notes 3/4 | a flat type catalog is one BB (`model` = shape of the data); split into runtime-event types (6) vs tool/permission/config types (7) by usage role; per-`query()`-call config types fold into the Options/Query notes that use them. Avoids a single 50-type note exceeding caps. |
| typescript-v2-preview.md (1.4Kw, removed API) | note 8 (single procedure note) | small + self-contained deprecation/migration page; one BB (procedure: pin-version + migrate). Below all caps as one note; no split. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_typescript_installation | procedure | 450 | 3 | ✅ |
| 2 | cc_sdk_typescript_query_function | procedure | 500 | 4 | ✅ |
| 3 | cc_sdk_typescript_options | procedure | 650 | 4 | ✅ |
| 4 | cc_sdk_typescript_query_object | procedure | 600 | 3 | ✅ |
| 5 | cc_sdk_typescript_sdk_functions | procedure | 600 | 4 | ✅ |
| 6 | cc_sdk_typescript_message_and_hook_types | model | 550 | 2 | ✅ |
| 7 | cc_sdk_typescript_tool_and_permission_types | model | 600 | 2 | ✅ |
| 8 | cc_sdk_typescript_v2_session_api_removed | procedure | 450 | 4 | ✅ |

The source is a 176-code-fence reference page; the digest deliberately curates ≤4 representative code blocks per note (signature + one usage example), summarizing exhaustive field/type tables as indexed catalogs with a pointer back to the live `source_url`. This keeps every note ≤650 words / ≤4 code / well under 400 lines — no over-compression (every H2/H3 maps to a note or explicit link-out), no cap breach.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_typescript_installation cc_sdk_typescript_query_function cc_sdk_typescript_options cc_sdk_typescript_query_object cc_sdk_typescript_sdk_functions cc_sdk_typescript_message_and_hook_types cc_sdk_typescript_tool_and_permission_types cc_sdk_typescript_v2_session_api_removed"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (8 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source (signatures/option keys/type names verbatim; no invented APIs) | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present or linked out | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed; in-degree ≥1) | DB in-degree query at finalization |
| G8-Discoverability (entry-point) | each note linked from `entry_claude_code_docs.md` (the SDK cluster rows) | entry-point row present + DB link |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under an "Agent SDK — TypeScript reference" cluster (alongside B19A–B21B SDK rows) + increments the BB-distribution counts (procedure +6, model +2).

## Undigested Terms Plan (Step 4e)

B21C creates **no new `term_dictionary` notes** — TypeScript API symbols are documented in B21C `cc_`
notes; conceptual terms are existing substantive term notes (link) or owned by a home sub-plan (Pattern B):

| Term / symbol surfaced on the pages | Disposition |
|---|---|
| `query()` / `startup()` / `WarmQuery` / `Query` object | B21C notes 2, 4 (doc API surface) |
| `Options` config keys | B21C note 3 |
| `tool()` / `createSdkMcpServer()` / session helpers / `resolveSettings()` | B21C note 5 |
| `SDKMessage` & variants / Hook types | B21C note 6 |
| `ToolInputSchemas`/`ToolOutputSchemas` / Permission types / config types | B21C note 7 |
| `unstable_v2_*` / `SDKSession` (removed V2) | B21C note 8 |
| TypeScript | link `term_typescript` (exists) |
| MCP / Subagent / Function calling-tool use / Structured output | link existing term notes |
| Compaction / Context window / Graduated trust / Regular checkpointing | link existing term notes |
| Sandbox / sandboxing concept | link `term_sandbox`; full concept owned by B05B / B21A (link-out) |
| Agent loop / sessions / hosting / hooks / permissions concepts | owned by home sub-plan (B19A/B19B/B20C/B21A) — captured there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages scanning emphasis/tables/captions/code
identifiers for newly-surfaced terms. No new non-glossary vocabulary term lacks a doc-page home AND an
existing note: candidates considered — "async generator" (TS language feature → `term_typescript`),
"Zod schema" (library detail → folded into note 5's `tool()` description; not a standalone vault concept),
"prompt caching" (→ existing `term_prompt_caching` / owned by B02A, linked where the `excludeDynamicSections`
caching note appears), "elicitation" (MCP detail → folded into note 3 `Options.onElicitation`; concept
owned by B20A). **0 new B21C `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B21C authors zero term notes, so there are
no slugs to audit. The collision check that matters here (do the API symbols duplicate existing notes?)
was performed: `term_typescript`, `term_mcp`, `term_subagent`, `term_function_calling`,
`term_structured_output`, `term_prompt_caching`, `term_sandbox`, `term_compaction`, `term_context_window`,
`term_graduated_trust`, `term_regular_checkpointing`, `term_claude_code`, `term_agent_harness`,
`term_autonomous_coding_agents`, `term_plugin_sdk`, `term_strands_agents_sdk`, `term_tool_descriptor`,
`term_session_persistence`, `term_idempotency`, `term_guardrails`, `term_agent_lifecycle_event`,
`term_event_driven_architecture` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B21C** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks reproduced verbatim from source (signatures + representative usage examples only — curate to
  ≤4/note, never the full 176 source fences). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 in-degree ≥1 each):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_typescript.md` | notes 1, 2, 3 | TS language term → the TS Agent-SDK install/entry/config surface |
| `term_dictionary/term_claude_code.md` | notes 2, 4 | product term → the TS API door (`query()`) + runtime control object |
| `term_dictionary/term_mcp.md` | notes 5, 7 | MCP term → `tool()`/`createSdkMcpServer()` authoring + MCP config types |
| `term_dictionary/term_function_calling.md` | notes 5, 7 | tool-use term → `tool()` definitions + per-tool schema catalog |
| `term_dictionary/term_structured_output.md` | note 5 | structured-output term → Zod-schema tool input + `ResolvedSettings` |
| `term_dictionary/term_strands_agents_sdk.md` | note 1 | sibling agent SDK → contextualizes the Claude Agent SDK install |
| `term_dictionary/term_idempotency.md` | note 8 | version-pin/safe-repeat term → V2-removal migration boundary |
| `documentation/claude_code/cc_sdk_python_*` (B21B, when present) | notes 2, 3, 6, 7 | Python reference siblings → TS counterparts (added if B21B notes exist at finalization) |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8 rows for `entry_claude_code_docs.md` (Agent SDK cluster); cross-link to the B21B Python-reference notes (TS↔Python parity); `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B21C, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read from `inbox/claude_code_docs/agent-sdk/`; measured words match the master's figure (typescript 14,376 + typescript-v2-preview 1,439 = 15,815). Heading inventory measured by grep: typescript.md = 11 H2 / 134 H3 / 55 H4 / 176 code fences; v2-preview = 5 H2 / 9 H3 / 11 code fences. No >1.5× under-estimate vs the master's 8-note budget; reference-page summary strategy keeps all notes within caps, so no re-split forced beyond the 3 documented splits.
- **Notes**: 8 (procedure 6, model 2) — matches master estimate. Split the 14.4Kw mega-reference by API surface area (install / `query()` / `Options` / `Query` object / helper functions / message+hook type catalog / tool+permission type catalog) + 1 standalone removed-V2 note.
- **Step 2d new-term scan**: candidates "async generator", "Zod schema", "prompt caching", "elicitation" considered → all map to an existing term (`term_typescript`/`term_prompt_caching`) or are folded into a note description; **0 new B21C term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G8 entry-point discoverability gate row, G5 verification note, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B21C authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and reviewed; set to `ready` (see Review Sign-Off).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B21C contributes 8 rows under the Agent-SDK TypeScript cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` (indexed links) / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–650w, ≤4 code; the 14.4Kw mega-reference proactively split into 7 surface-area notes + the type catalogs into 2 model notes — none borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w`: typescript 14,376 + typescript-v2-preview 1,439 = 15,815 = master figure (±0%). Heading/code counts grep-measured. |
| CP8 | Undigested Terms Plan + Authoring Requirements present | ✅ PASS (N/A scope) | B21C authors 0 term notes; Undigested Terms Plan routes all API symbols + concept terms; Authoring Requirements inherited. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
