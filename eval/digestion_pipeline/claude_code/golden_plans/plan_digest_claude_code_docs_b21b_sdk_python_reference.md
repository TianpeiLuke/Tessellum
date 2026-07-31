---
title: Sub-Plan B21B — Claude Code Docs: SDK Python Reference
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/python"]
---

# Sub-Plan B21B: SDK Python Reference

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The single `agent-sdk/python.md` page — the **complete Python Agent SDK API reference** (`claude-agent-sdk`):
the two entry points (`query()`, `ClaudeSDKClient`), all module-level functions, the `ClaudeAgentOptions`
configuration dataclass plus its companion config types, message / content-block / error types, hook
types, built-in tool input/output schemas, and sandbox configuration. P3 (Phase C) — a specialized
language-reference page; the conceptual SDK material (agent loop, sessions, streaming, custom tools,
hooks, permissions) is owned by B19A–B20C and is **linked, not re-digested** here. This note set is the
Python-typed mirror of those concepts.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 1 page, 15,226 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the two interaction entry points (`query()` vs `ClaudeSDKClient`) and the
  `ClaudeAgentOptions` config surface — the parts a Python developer touches first and most.
- **Group**: the page's 12 H2 sections collapse into 7 BB-atomic notes by API surface area —
  (1) entry functions, (2) session-management functions, (3) the client class, (4) options + config types,
  (5) message / content-block / error types, (6) hook types, (7) tool I/O schemas + sandbox config. The
  source is a flat reference (~74 code blocks), so notes split on *what the developer is configuring*, not
  on narrative.
- **Skip / link-out (own other sub-plans)**: the *behavioral* SDK guides — agent loop → B19A; sessions /
  session storage / system prompts → B19B; streaming / structured outputs / user input → B19C; custom
  tools / MCP / tool search → B20A; skills / slash commands / subagents / plugins → B20B; hooks /
  permissions / file checkpointing → B20C; cost tracking / hosting / observability → B21A; TypeScript
  mirror → B21C. These are referenced via the source's own deep links, never duplicated.
- **Glossary / terms**: no new `term_dictionary` notes — SDK vocabulary maps to existing term notes
  (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

The 1 page re-read from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of
`code.claude.com/docs/en/agent-sdk/python.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| python | /agent-sdk/python | 15,226 | ~74 | 12 | ~62 | procedure (API reference) |

> **H2 lists (document order):**
> - **Installation** — `pip install claude-agent-sdk`
> - **Choosing between `query()` and `ClaudeSDKClient`** (H3 Quick comparison · When to use query() · When to use ClaudeSDKClient)
> - **Functions** (H3 `query()` · `tool()` + ToolAnnotations · `create_sdk_mcp_server()` · `list_sessions()` + SDKSessionInfo · `get_session_messages()` + SessionMessage · `get_session_info()` · `rename_session()` · `tag_session()`)
> - **Classes** (H3 `ClaudeSDKClient` — methods, context-manager support, conversation/streaming/interrupt/permission examples)
> - **Types** (H3 SdkMcpTool · Transport · `ClaudeAgentOptions` + timeout env vars · OutputFormat · SystemPromptPreset · SettingSource · AgentDefinition · PermissionMode · EffortLevel · CanUseTool · ToolPermissionContext · PermissionResult/Allow/Deny · PermissionUpdate · PermissionRuleValue · ToolsPreset · ThinkingConfig · SdkBeta · McpSdkServerConfig · McpServerConfig · McpServerStatusConfig · McpStatusResponse · McpServerStatus · SdkPluginConfig)
> - **Message Types** (H3 Message · UserMessage · AssistantMessage · AssistantMessageError · SystemMessage · ResultMessage · StreamEvent · RateLimitEvent · RateLimitInfo · TaskStartedMessage · TaskUsage · TaskProgressMessage · TaskNotificationMessage)
> - **Content Block Types** (H3 ContentBlock · TextBlock · ThinkingBlock · ToolUseBlock · ToolResultBlock)
> - **Error Types** (H3 ClaudeSDKError · CLINotFoundError · CLIConnectionError · ProcessError · CLIJSONDecodeError)
> - **Hook Types** (H3 HookEvent · HookCallback · HookContext · HookMatcher · HookInput + 11 per-event input types · HookJSONOutput · Hook Usage Example)
> - **Tool Input/Output Types** (H3 ~26 built-in tools: Agent · AskUserQuestion · Bash · Monitor · Edit · Read · Write · Glob · Grep · NotebookEdit · WebFetch · WebSearch · TodoWrite · TaskCreate · TaskUpdate · TaskGet · TaskList · BashOutput · KillBash · ExitPlanMode · ListMcpResources · ReadMcpResource)
> - **Advanced Features with ClaudeSDKClient** (H3 Continuous Conversation Interface · Hooks for Behavior Modification · Real-time Progress Monitoring)
> - **Example Usage** (H3 Basic file operations · Error handling · Streaming mode · Custom tools)
> - **Sandbox Configuration** (H3 SandboxSettings · SandboxNetworkConfig · SandboxIgnoreViolations · Permissions Fallback for Unsandboxed Commands)
> - **See also** — cross-links to overview / streaming / permissions / MCP / custom-tools / TypeScript

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **7 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_python_entry_points.md` | procedure | Installation; Choosing between query() and ClaudeSDKClient; Functions: query(); Example Usage (basic/error/streaming) | 600 | Install `claude-agent-sdk`; `query()` vs `ClaudeSDKClient` decision table; `query()` signature/params/returns + async-iterator usage; basic file-ops / error-handling / streaming examples (≤6 code blocks). Concept depth → B19A agent-loop. |
| 2 | `cc_sdk_python_session_functions.md` | procedure | Functions: list_sessions() + SDKSessionInfo; get_session_messages() + SessionMessage; get_session_info(); rename_session(); tag_session() | 500 | The 5 synchronous session-management functions + their `SDKSessionInfo` / `SessionMessage` return shapes (filter by directory, page messages, rename/tag). Behavior → B19B sessions / session-storage. |
| 3 | `cc_sdk_python_client.md` | procedure | Classes: ClaudeSDKClient (methods, context-manager, examples); Advanced Features with ClaudeSDKClient | 650 | The stateful `ClaudeSDKClient`: `__init__`/`connect`/`query`/`receive_response`/`interrupt`/`set_permission_mode`/`set_model`/`rewind_files`/MCP-control/`disconnect`; async-context-manager usage; interrupt buffer-drain caveat; continuous-conversation / progress-monitoring patterns (≤6 code blocks). |
| 4 | `cc_sdk_python_options_and_config_types.md` | procedure | Types: ClaudeAgentOptions (+ timeout env vars) + OutputFormat, SystemPromptPreset, SettingSource, AgentDefinition, PermissionMode, EffortLevel, ToolsPreset, ThinkingConfig, SdkBeta, McpServerConfig family, SdkPluginConfig, Transport, SdkMcpTool, CanUseTool, ToolPermissionContext, PermissionResult/Allow/Deny, PermissionUpdate, PermissionRuleValue | 750 | The `ClaudeAgentOptions` configuration dataclass field-by-field + the companion config/permission/MCP-config types it references; timeout/stall env-var passthrough. Reference only — semantics → B19B/B20A/B20C. |
| 5 | `cc_sdk_python_message_and_error_types.md` | procedure | Message Types (Message…TaskNotificationMessage); Content Block Types; Error Types | 700 | The message union (`UserMessage`/`AssistantMessage`/`SystemMessage`/`ResultMessage`/`StreamEvent`/`RateLimitEvent` + task messages), the `ResultMessage` cost/usage/subtype fields, content blocks (text/thinking/tool-use/tool-result), and the 5 SDK exception classes. `@dataclass` vs `TypedDict` runtime access note. |
| 6 | `cc_sdk_python_hook_types.md` | procedure | Hook Types (HookEvent, HookCallback, HookContext, HookMatcher, HookInput + 11 per-event inputs, HookJSONOutput, Hook Usage Example) | 600 | The 10 `HookEvent` values, `HookCallback`/`HookContext`/`HookMatcher` signatures, the per-event `*HookInput` shapes, the `HookJSONOutput` decision schema, and the registration example. Hook concepts/usage → B20C. |
| 7 | `cc_sdk_python_tool_io_and_sandbox.md` | procedure | Tool Input/Output Types (~26 built-in tools); Sandbox Configuration (SandboxSettings, SandboxNetworkConfig, SandboxIgnoreViolations, Permissions Fallback) | 700 | The input/output dict schemas for the built-in tools (Agent/Bash/Monitor/Read/Write/Edit/Grep/Glob/Web*/Task*/Mcp*…) and the `SandboxSettings` family (network allow/deny, ignore-violations, unsandboxed-command permission fallback). |

**Estimate: 7 notes** — all `procedure` (this is an API reference; every note documents how to call/configure something). All single-BB, all within caps (code-block count managed per note, see Density Re-Assessment).

## Summary Statistics & Building Block Distribution

- Source pages: 1 (15,226 words). New `cc_` notes: 7. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,500 (avg ~640/note). Code blocks: heavy source (~74) compressed to ≤6/note via representative-signature selection (full signatures kept verbatim; repetitive per-tool/per-type dict schemas summarized in tables).
- **Building Block Distribution**: procedure ×7 (notes 1–7). No concept/model/argument/empirical_observation — a pure API reference is procedural (how to call/configure). Conceptual SDK material is owned by B19A–B20C and linked out.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_sdk_python_entry_points` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `claude-agent-sdk` package wraps the same Claude Code engine; this note's `query()`/`ClaudeSDKClient` are the Python entry points into that product, so the product term anchors the note.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `query()` and `ClaudeSDKClient` are the programmatic handles onto the agentic harness (model + tools + context + execution env); the note's two entry points are how a Python program drives that harness.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The SDK is the way to build autonomous coding agents in Python; `query()` runs a fresh one-off agent and `ClaudeSDKClient` runs a continuous one, exactly the autonomous-agent operating modes this term defines.
- [ReAct](../../term_dictionary/term_react.md) — Each `query()` call returns an async iterator yielding messages as the agent reasons, acts via tools, and observes results — the interleaved reason-act-observe loop ReAct formalizes.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The streamed messages this note iterates over carry tool-use requests and tool results, the function-calling mechanism that makes each `query()` agentic.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Choosing `query()` (fresh context each call) vs `ClaudeSDKClient` (retained context across exchanges) is a context-engineering decision the note's comparison table makes explicit.
- [Context Window](../../term_dictionary/term_context_window.md) — `query()` starts each call with no memory unless `continue_conversation`/`resume` is passed, so what is (or isn't) reloaded into the context window is the behavioral pivot of the note's entry-point comparison.

### 2. `cc_sdk_python_session_functions` (6 term notes)
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — The 5 functions (`list_sessions`/`get_session_messages`/`get_session_info`/`rename_session`/`tag_session`) read and annotate persisted session transcripts, the exact session-persistence mechanism this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — These functions enumerate and inspect Claude Code's on-disk session store from Python, so the product term grounds what a "session" here is.
- [Context Window](../../term_dictionary/term_context_window.md) — A resumed/forked session restores the prior conversation into the context window; the note's `SDKSessionInfo`/`SessionMessage` are the metadata and contents that get reloaded.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Listing, tagging, and reopening past sessions is the durable-checkpoint workflow this term describes — each session file is a recoverable checkpoint of agent work.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Session metadata (cwd, git branch, summary) is harness state captured per run; these functions expose that harness bookkeeping to the host program.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Long-running autonomous agents accumulate many sessions; these listing/tagging functions are how a host triages and resumes that autonomous work.

### 3. `cc_sdk_python_client` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — `ClaudeSDKClient` is the stateful Python handle onto a Claude Code session; the product term anchors what the client connects to and controls.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The client's lifecycle methods (`connect`/`query`/`interrupt`/`set_model`/`set_permission_mode`/`disconnect`) are direct controls over the running harness, making the client the harness's programmatic remote.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `set_permission_mode()` flips the session between default/acceptEdits/plan/bypass modes mid-run, the graduated-trust escalation this term defines.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — `rewind_files(user_message_id)` restores files to an earlier message's state (requires `enable_file_checkpointing`), the file-checkpoint-and-rewind capability this term describes.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The client exposes `get_mcp_status`/`reconnect_mcp_server`/`toggle_mcp_server` to inspect and hot-swap MCP servers mid-session, runtime control over the note's MCP layer.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `ClaudeSDKClient` retains conversation context across `query()` calls and supports interrupts, so managing that continuous context is the core context-engineering concern of the note.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The continuous-conversation and real-time progress-monitoring patterns in the note are how you build a long-lived, steerable autonomous coding agent on the client.

### 4. `cc_sdk_python_options_and_config_types` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — `ClaudeAgentOptions` is the master configuration object for a Claude Code SDK run; nearly every Claude Code feature surfaces as a field here, so the product term anchors the note.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `permission_mode`, `allowed_tools`, `disallowed_tools`, `can_use_tool`, `PermissionResultAllow/Deny`, and `PermissionUpdate` are the graduated-trust controls this note documents field-by-field.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `mcp_servers`, `strict_mcp_config`, and the `McpServerConfig`/`McpSdkServerConfig` family configure which MCP servers the run loads, a central block of the options surface.
- [Subagent](../../term_dictionary/term_subagent.md) — The `agents: dict[str, AgentDefinition]` field and the `AgentDefinition` type programmatically define subagents, so the subagent term grounds that part of the config.
- [Skills](../../term_dictionary/term_skills.md) — The `skills` option (`"all"` or a name list) selects which skills the session can invoke and auto-adds the Skill tool, the skill-loading control this note covers.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — `thinking`/`ThinkingConfig`, `max_thinking_tokens`, and `effort`/`EffortLevel` tune extended-thinking depth, the chain-of-thought budget knobs in the options object.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The `sandbox: SandboxSettings` field configures programmatic sandbox isolation; the sandbox term grounds that option (full settings in note 7).
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `system_prompt`/`SystemPromptPreset` (incl. `exclude_dynamic_sections` for cache reuse) and `setting_sources` shape what context the agent starts with, a context-engineering surface.

### 5. `cc_sdk_python_message_and_error_types` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — These message/content/error types are the Python shapes the Claude Code SDK yields from its message stream, so the product term anchors what produces them.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `ToolUseBlock` and `ToolResultBlock` are the content blocks carrying tool-call requests and their results, the function-calling round-trip this note types.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — `ThinkingBlock` (with `thinking` text + `signature`) is the content block that surfaces the model's extended reasoning, the chain-of-thought output this note documents.
- [Context Window](../../term_dictionary/term_context_window.md) — `ResultMessage.usage` / `model_usage` report input/output and cache-read/creation token counts, the context-window consumption this note tabulates.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — The usage dict's `cache_creation_input_tokens` and `cache_read_input_tokens` fields measure prompt-cache hits, the caching mechanism this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — `parent_tool_use_id` on messages and the `Task*Message` family track subagent and background-task lifecycle, the subagent execution this note's task messages report.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `RateLimitEvent`/`RateLimitInfo` and the error classes surface harness-level runtime conditions (rate limits, CLI failures), the harness state this note types.

### 6. `cc_sdk_python_hook_types` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Hooks fire on Claude Code lifecycle events; these `Hook*` types are the Python contract for registering interceptors in the SDK, so the product term anchors the note.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `PreToolUse`/`PostToolUse`/`PostToolUseFailure` hooks intercept tool calls before/after execution, gating the function-calling round-trip this note's input types describe.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The `PermissionRequest` hook and the `HookJSONOutput` allow/deny/ask decision schema let hooks make graduated-trust permission decisions, a core use of these types.
- [Compaction](../../term_dictionary/term_compaction.md) — The `PreCompact` hook event fires before message compaction; the note types its `PreCompactHookInput`, tying the hook surface to the compaction mechanism this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — `SubagentStart`/`SubagentStop` hook events and their input types fire on subagent lifecycle, the subagent orchestration this note's hook set observes.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `UserPromptSubmit` and `PreCompact` hooks can rewrite or trim what enters the context window, making hooks a programmatic context-engineering lever.

### 7. `cc_sdk_python_tool_io_and_sandbox` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — These are the input/output schemas of Claude Code's built-in tools plus its sandbox config; the product term anchors the toolset and isolation model the note documents.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Every entry (Bash/Read/Write/Edit/Grep/Web*/Task*…) is a tool whose input/output dict shape is the function-calling contract Claude fills and reads, the core of this note.
- [Sandbox](../../term_dictionary/term_sandbox.md) — `SandboxSettings` (+ network config, ignore-violations, unsandboxed-command fallback) is the programmatic sandbox-isolation surface this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The `Agent` tool (formerly `Task`) spawns a typed subagent with `description`/`prompt`/`subagent_type` input and a `result`/`usage` output, the subagent invocation this note types.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `ListMcpResources`/`ReadMcpResource` are the built-in tools for reading MCP server resources, tying the note's tool catalog to the MCP layer.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The "Permissions Fallback for Unsandboxed Commands" subsection routes commands the sandbox can't run through the permission system, the graduated-trust fallback this term covers.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The built-in file/exec/search/web tools are precisely the capabilities that make an autonomous coding agent; this note's schemas define what each can do.

## Section Coverage Map

```
agent-sdk/python.md
├── Installation ──────────────────────────────── → note 1 (cc_sdk_python_entry_points)
├── Choosing between query() and ClaudeSDKClient ─ → note 1
│   ├── Quick comparison (table) ──────────────── → note 1
│   ├── When to use query() ───────────────────── → note 1
│   └── When to use ClaudeSDKClient ───────────── → note 1
├── Functions
│   ├── query() ───────────────────────────────── → note 1
│   ├── tool() + ToolAnnotations ──────────────── → linked out (B20A custom-tools); signature in note 4 (SdkMcpTool)
│   ├── create_sdk_mcp_server() ───────────────── → linked out (B20A custom-tools/mcp); McpSdkServerConfig in note 4
│   ├── list_sessions() + SDKSessionInfo ──────── → note 2 (cc_sdk_python_session_functions)
│   ├── get_session_messages() + SessionMessage ─ → note 2
│   ├── get_session_info() ────────────────────── → note 2
│   ├── rename_session() ──────────────────────── → note 2
│   └── tag_session() ─────────────────────────── → note 2
├── Classes
│   └── ClaudeSDKClient (methods/ctx-mgr/examples) → note 3 (cc_sdk_python_client)
├── Types
│   ├── SdkMcpTool · Transport ────────────────── → note 4 (cc_sdk_python_options_and_config_types)
│   ├── ClaudeAgentOptions (+ timeout env vars) ── → note 4
│   ├── OutputFormat · SystemPromptPreset · SettingSource · AgentDefinition → note 4
│   ├── PermissionMode · EffortLevel · CanUseTool · ToolPermissionContext → note 4
│   ├── PermissionResult/Allow/Deny · PermissionUpdate · PermissionRuleValue → note 4
│   ├── ToolsPreset · ThinkingConfig · SdkBeta ── → note 4
│   └── McpSdkServerConfig · McpServerConfig · McpServerStatusConfig · McpStatusResponse · McpServerStatus · SdkPluginConfig → note 4
├── Message Types (Message … TaskNotificationMessage) → note 5 (cc_sdk_python_message_and_error_types)
├── Content Block Types (ContentBlock … ToolResultBlock) → note 5
├── Error Types (ClaudeSDKError … CLIJSONDecodeError) → note 5
├── Hook Types (HookEvent … HookJSONOutput + Hook Usage Example) → note 6 (cc_sdk_python_hook_types)
├── Tool Input/Output Types (~26 built-in tools) ─ → note 7 (cc_sdk_python_tool_io_and_sandbox)
├── Advanced Features with ClaudeSDKClient ────── → note 3 (continuous-conversation / hooks-for-behavior / progress-monitoring)
├── Example Usage (basic/error/streaming/custom-tools) → notes 1 (basic/error/streaming) + 3 (custom-tools w/ client)
├── Sandbox Configuration (SandboxSettings family) → note 7
└── See also (cross-links) ────────────────────── → distributed as links across notes 1/3/4/7 (+ B19/B20/B21/B21C)
```
No orphaned sections. (`tool()` / `create_sdk_mcp_server()` *function semantics* are owned by B20A; their
*Python type shapes* — `SdkMcpTool`, `McpSdkServerConfig` — are documented as types in note 4, with a
link-out to B20A for the authoring guide.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| python.md (15,226w >2500 cap, ~74 code blocks, 12 H2) | notes 1–7 | single page far exceeds density caps; splits on API surface (entry funcs / session funcs / client / options+config types / message+error types / hook types / tool-IO+sandbox) — each independently usable and ≤6 code blocks after table-compression of repetitive schemas |
| Functions H2 (8 functions) | note 1 (query) + note 2 (5 session funcs) + link-out (tool / create_sdk_mcp_server → B20A) | session functions form a coherent read/annotate cluster; the 2 MCP-tool factories belong with the custom-tools guide (B20A), only their type shapes stay here |
| Types H2 (~25 types) | note 4 (all config/permission/MCP-config types) | one big config cluster centered on `ClaudeAgentOptions`; message/content/error/hook types are separated into notes 5/6 because they are runtime outputs, not configuration inputs |
| Example Usage H2 (4 examples) | note 1 (basic/error/streaming) + note 3 (custom-tools-with-client) | examples attach to the entry point they demonstrate; the custom-tools example is client-centric |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_python_entry_points | procedure | 600 | 5 | ✅ |
| 2 | cc_sdk_python_session_functions | procedure | 500 | 4 | ✅ |
| 3 | cc_sdk_python_client | procedure | 650 | 6 | ✅ |
| 4 | cc_sdk_python_options_and_config_types | procedure | 750 | 4 | ✅ |
| 5 | cc_sdk_python_message_and_error_types | procedure | 700 | 5 | ✅ |
| 6 | cc_sdk_python_hook_types | procedure | 600 | 5 | ✅ |
| 7 | cc_sdk_python_tool_io_and_sandbox | procedure | 700 | 6 | ✅ |

No note exceeds 750w / 6 code blocks / 400 lines. **Code-block discipline (load-bearing):** the source has
~74 code blocks; each note keeps the *primary signatures verbatim* (≤6 blocks) and renders the repetitive
per-type field lists / per-tool dict schemas as **markdown tables** (matching the source's own table style),
so no note approaches the 6-code-block cap from raw copying. If a draft would exceed 6 code blocks, convert
the lowest-value dict-schema block to a table; if it would exceed 2,500 words, the note splits further
(e.g. note 4 → options vs config-types; note 7 → tool-IO vs sandbox) — not anticipated at these sizes.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_python_entry_points cc_sdk_python_session_functions cc_sdk_python_client cc_sdk_python_options_and_config_types cc_sdk_python_message_and_error_types cc_sdk_python_hook_types cc_sdk_python_tool_io_and_sandbox"
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

Single phase (7 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, signatures verbatim, no hallucinated fields | diff vs `inbox/claude_code_docs/agent-sdk/python.md` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present or linked out | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G6-Broken | 0 broken links touching the 7 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 7 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | same anti-island check verified by DB after inlinks land | DB in-degree query (G8 = G7 confirmation post-reindex) |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 7 rows** under an "Agent SDK — Python reference" cluster + increments the
BB-distribution counts (procedure ×7). The entry-point back-link is added to each note at finalization (G7/G8).

## Undigested Terms Plan (Step 4e)

B21B creates **no new `term_dictionary` notes** — `agent-sdk/python.md` is a typed API reference whose
vocabulary is either (a) covered by an existing substantive term note (link, Pattern B), or (b) a
Python-specific symbol name (`ClaudeAgentOptions`, `ResultMessage`, `HookJSONOutput`, etc.) that is a
*documentation subject*, digested into the `cc_sdk_python_*` notes themselves — never a term note (per the
master's CC-specific design decision). Dedup checked across **both** `term_dictionary/` AND
`resources/documentation/` (no existing `claude_code/` folder yet; no Python-SDK doc note exists).

| Source vocabulary | Disposition |
|---|---|
| MCP / in-process MCP server | link `term_mcp` (exists); SDK shape `McpSdkServerConfig` → note 4 |
| Subagent / agent (Agent tool) | link `term_subagent` (exists); `AgentDefinition` → note 4, `Agent` tool I/O → note 7 |
| Permission mode / can_use_tool / permission rules | link `term_graduated_trust` (exists); `PermissionMode`/`CanUseTool`/`PermissionResult*` → note 4 |
| Sandbox / sandbox settings | link `term_sandbox` (exists); `SandboxSettings` family → note 7 |
| Skill(s) | link `term_skills` (exists); `skills` option → note 4 |
| Compaction (PreCompact hook) | link `term_compaction` (exists); `PreCompactHookInput` → note 6 |
| Extended thinking / effort | link `term_chain_of_thought` (exists); `ThinkingConfig`/`EffortLevel` → note 4 |
| Prompt caching (cache tokens) | link `term_prompt_caching` (exists); `usage` cache keys → note 5 |
| Session / resume / fork | link `term_session_persistence` (exists); session functions → note 2 |
| Tool use / function calling | link `term_function_calling` (exists); `ToolUseBlock`/tool I/O → notes 5/7 |
| Agentic harness / agentic coding | link `term_agent_harness` / `term_autonomous_coding_agents` (exist) |
| query()/ClaudeSDKClient/options/messages/hooks/tool-IO symbols | `cc_sdk_python_*` doc notes (this sub-plan) — not term notes |

**Augmentation Step 2d re-scan (2026-06-13):** re-read the full page scanning code-block symbols, table
captions, and `<Note>`/`<Warning>` callouts for newly-surfaced terms. Candidate Python-runtime concepts
considered for new term capture — `@dataclass` vs `TypedDict` runtime distinction, `RateLimitInfo`,
fully documented inline in the `cc_sdk_python_*` notes. No genuine cross-cutting vocabulary term with no
doc-page home AND no existing note surfaced. **0 new B21B `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B21B authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the SDK concepts duplicate existing notes?) was
`term_context_window`, `term_compaction`, `term_sandbox`, `term_skills`, `term_agent_harness`,
`term_autonomous_coding_agents`, `term_regular_checkpointing`, `term_graduated_trust`,
`term_context_engineering`, `term_chain_of_thought`, `term_react`, `term_function_calling`,

## Term-Note Authoring Requirements

**N/A for B21B** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim for signatures; repetitive per-type/per-tool dict schemas rendered as tables to
  stay ≤6 code blocks per note. One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 3 | product term → Python SDK entry points + client (also satisfies master's "link docs series from term_claude_code") |
| `term_dictionary/term_session_persistence.md` | note 2 | session-persistence term → SDK session-management functions |
| `term_dictionary/term_graduated_trust.md` | note 4 | permission-mode term → `ClaudeAgentOptions` permission config |
| `term_dictionary/term_function_calling.md` | notes 5, 7 | tool-use term → message tool blocks + built-in tool I/O schemas |
| `term_dictionary/term_sandbox.md` | note 7 | sandbox term → `SandboxSettings` family |
| `term_dictionary/term_mcp.md` | note 4 | MCP term → `McpServerConfig` family in options |
| sibling B19A `cc_sdk_*` (when present) / B21C `cc_sdk_typescript_*` | notes 1, 5 | SDK-core + TypeScript-mirror cross-links (added when those sub-plans land) |

## Follow-up Recommendations

- After the 7 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 7
  rows for `entry_claude_code_docs.md` (Agent SDK — Python reference cluster); add cross-links to the
  TypeScript reference (B21C) and SDK-concept sub-plans (B19A–B20C/B21A) once those execute;
  `/tessellum-check-broken-links`; verify G7/G8 in-degree ≥1 for all 7 notes.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B21B, 2026-06-13)

- **Source re-read (Step 2)**: `agent-sdk/python.md` re-read in full from `inbox/claude_code_docs/`; measured
  15,226 words (matches the master's figure exactly) with 12 H2, ~62 H3, ~74 code blocks. No >1.5×
  under-estimate; the page far exceeds density caps, forcing the 7-way split (documented in Split Decisions).
- **Notes**: 7 (procedure ×7) — matches master estimate. Splits on API surface area, each ≤6 code blocks
  after table-compression of repetitive per-type/per-tool schemas.
- **Per-Note Related Notes Mapping (Step 8)**: ≥6 relevancy-selected term notes per note (6–8 each; 12
  distinct `term_dictionary/` terms used across the 7 notes), each with a per-link relevancy statement.
- **Step 2d new-term scan**: re-scanned code symbols / callouts; all SDK symbols are doc-note subjects
  (digested into `cc_sdk_python_*`) or existing term links; **0 new B21B term captures**.
- **Sections added/confirmed during augment**: Content Strategy, Summary Statistics & BB Distribution,
  Validation Scripts (bash), Density Re-Assessment with code-block-compression rule, G5 ls-verification note,
  G7/G8 rows, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B21B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed → set to `ready` (9/9 review checkpoints PASS below).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B21B contributes 7 rows under the Agent SDK — Python reference cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 7 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 7 notes 500–750w, ≤6 code blocks (repetitive schemas tabled). None borderline after split; further-split triggers documented in Density Re-Assessment. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w agent-sdk/python.md` = 15,226 = master figure = plan figure (±0%). H2/H3/code-block counts from `grep -nE '^#{2,3} '`. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B21B authors 0 term notes; Undigested Terms Plan routes all SDK vocabulary (existing-term link or `cc_sdk_python_*` doc subject); Authoring Requirements inherited. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
