---
title: Sub-Plan B19B — Claude Code Docs: SDK Sessions & System Prompts
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/sessions", "agent-sdk/session-storage", "agent-sdk/modifying-system-prompts", "agent-sdk/todo-tracking"]
---

# Sub-Plan B19B: SDK Sessions & System Prompts

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted **PILOT** [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 Agent SDK pages that cover **session persistence** (how conversation history is written to disk,
and `continue` / `resume` / `fork`), **external session storage** (the `SessionStore` mirror adapter for
multi-host/serverless), **system-prompt modification** (preset vs append vs custom vs CLAUDE.md vs output
styles), and **todo/task tracking** (the in-stream progress signal and the `TodoWrite` → Task-tools
migration). P2 (Phase B) — builds on the SDK core/lifecycle vocabulary defined in B19A (agent loop,
`query()`, result messages) and on the existing vault agentic terms (context window, subagent, compaction).

**Source**: Claude Code docs (`code.claude.com/docs/en/agent-sdk`), 4 pages, 8,146 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the durable session model (persist / continue / resume / fork) and the four system-prompt
  customization methods — these are the cross-cutting SDK concepts later sub-plans (B19C streaming, B20*
  tools/skills/subagents, B21A hosting) reference.
- **Group**: split `sessions` (concept overview vs the `query()` option API procedure) and `session-storage`
  (the `SessionStore` interface/behavior concept vs the build-an-adapter procedure) by BB; split
  `modifying-system-prompts` (3,059w >2500 cap) into the choose-an-approach **concept** and the
  customize-the-prompt **procedure**; keep `todo-tracking` as one concept note (lifecycle + migration).
- **Skip / link-out (own other sub-plans)**: file checkpointing → B20C (`agent-sdk/file-checkpointing`);
  agent-loop turns/result-message handling → B19A (`agent-sdk/agent-loop`); user-input / `AskUserQuestion`
  in-loop → B19C (`agent-sdk/user-input`); multi-host hosting/deployment patterns → B21A
  (`agent-sdk/hosting`); CLAUDE.md *content* guidance → B02B memory (`/en/memory`); output-style *CLI*
  creation/format → B06 (`output-styles`); `settingSources`/settings.json reference → B03A; CLI
  `--exclude-dynamic-system-prompt-sections` flag → B03B (`cli-reference`); skills/hooks/permissions
  behavior → B20B/B20C. These are referenced via links, never duplicated.
- **Glossary / terms**: not re-digested into `cc_` notes — agentic terms route to existing term notes
  (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| sessions | /agent-sdk/sessions | 2,211 | 4 | 5 | 6 | concept/procedure |
| session-storage | /agent-sdk/session-storage | 1,660 | 4 | 7 | 7 | concept/procedure |
| modifying-system-prompts | /agent-sdk/modifying-system-prompts | 3,059 | 2 | 6 | 10 | concept/procedure |
| todo-tracking | /agent-sdk/todo-tracking | 1,216 | 0 | 3 | 4 | concept |

> **H2 lists (document order):**
> - **sessions**: Choose an approach (H3 Continue, resume, and fork) · Automatic session management (H3 Python `ClaudeSDKClient`, TypeScript `continue: true`) · Use session options with `query()` (H3 Capture the session ID, Resume by ID, Fork to explore alternatives) · Resume across hosts · Related resources
> - **session-storage**: The `SessionStore` interface · Quick start · Write your own adapter · Reference implementations (H3 Validate your adapter) · Behavior notes (H3 Dual-write architecture, Mirror writes are best-effort, `getSessionMessages` returns the post-compaction chain, `forkSession` is not a byte copy, Subagent transcripts, Retention) · Supported on · Related resources
> - **modifying-system-prompts**: How system prompts work (H3 Decide on a starting point) · Customize agent behavior (H3 CLAUDE.md files, Output styles, Append to the preset, Custom system prompts) · Compare the four approaches · Use cases and best practices (H3 When to use CLAUDE.md / output styles / append / custom) · Combine approaches (H3 Combine an output style with session-specific additions) · See also
> - **todo-tracking**: Todo Lifecycle · When Todos Are Used · Examples (H3 Monitoring Todo Changes, Real-time Progress Display) · Migrate to Task tools · Related Documentation

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **7 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_sessions_overview.md` | concept | sessions: intro, Choose an approach, Continue/resume/fork, Resume across hosts | 600 | What an SDK session is (the on-disk conversation transcript, not the filesystem); the decision table for one-shot vs multi-turn vs continue vs resume vs fork; how continue/resume/fork differ; cross-host limits + encoded-cwd `~/.claude/projects/<encoded-cwd>/*.jsonl` layout. file-checkpointing → B20C. |
| 2 | `cc_sdk_session_management_api.md` | procedure | sessions: Automatic session management, Use session options with `query()` (capture ID, resume, fork), listSessions/getSessionMessages | 700 | The `query()`/`ClaudeAgentOptions` session API: `ClaudeSDKClient` (Python) & `continue: true` (TS) for auto-tracking; capture `session_id` from the result message; `resume=` by ID; `fork_session=True`/`forkSession` to branch; enumerate/mutate via `list_sessions`/`get_session_messages`/`rename_session`/`tag_session`. ≤6 code (Python+TS pairs). |
| 3 | `cc_sdk_session_store.md` | concept | session-storage: intro, The `SessionStore` interface, Behavior notes, Supported on | 650 | The `SessionStore` mirror-adapter model: required `append`/`load` + optional `listSessions`/`delete`/`listSubkeys`; `SessionKey` (projectKey/sessionId/subpath); dual-write architecture (mirror not replacement); best-effort mirror writes + `mirror_error`; post-compaction chain from `getSessionMessages`; fork rewrite; subagent subpaths; retention; the `sessionStore`-accepting function list. |
| 4 | `cc_sdk_session_store_setup.md` | procedure | session-storage: Quick start, Write your own adapter, Reference implementations, Validate your adapter | 600 | Build/use a store: `InMemorySessionStore` quick start; implement `append`+`load` (opaque ordered JSON-safe entries, deep-equal load); S3/Redis/Postgres reference adapters + the S3 wiring example; run the conformance suite (`run_session_store_conformance`). ≤6 code. |
| 5 | `cc_sdk_system_prompts.md` | concept | modifying-system-prompts: intro, How system prompts work, Decide on a starting point, Compare the four approaches | 650 | The three SDK starting points (minimal default vs `claude_code` preset vs custom string) and the decision table; what "different from Claude Code" means (surface/identity/permission/non-coding); the four-method comparison matrix (persistence, default tools, safety, env context, scope). |
| 6 | `cc_sdk_customize_system_prompt.md` | procedure | modifying-system-prompts: Customize agent behavior (CLAUDE.md, output styles, append, custom), prompt-caching, Use cases & best practices, Combine approaches | 750 | How to apply each method: load CLAUDE.md via `settingSources`; create/activate an output style (`keep-coding-instructions`); `append` to the preset; provide a custom string; improve prompt-cache reuse with `excludeDynamicSections`; when-to-use guidance; compose a persistent style/CLAUDE.md with session-specific `append`. ≤6 code. |
| 7 | `cc_sdk_todo_and_task_tracking.md` | concept | todo-tracking: intro, Todo Lifecycle, When Todos Are Used, Examples, Migrate to Task tools | 600 | How the SDK surfaces task progress in the assistant stream: todo lifecycle (pending→in_progress→completed→removed); when the SDK auto-creates todos; monitoring `TodoWrite` `tool_use` blocks; the `TodoWrite` → `TaskCreate`/`TaskUpdate`/`TaskList`/`TaskGet` migration (default since TS SDK 0.3.142 / CC v2.1.142) and the keyed-map monitoring change. |

**Estimate: 7 notes** — concept ×4 (notes 1, 3, 5, 7), procedure ×3 (notes 2, 4, 6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (8,146 words). New `cc_` notes: 7. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,550 (avg ~650/note). Code blocks: notes 2/4/6 carry Python+TS pairs (≤6 each, verbatim); notes 1/3/5/7 are prose/table-dominant.
- **Building Block Distribution**: concept ×4 (notes 1, 3, 5, 7) · procedure ×3 (notes 2, 4, 6). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> dropped (`term_session_persistence` = LB sticky sessions; `term_sessionid` = browser/risk session;
> `term_sessionminer` = clickstream ML — all excluded).

### 1. `cc_sdk_sessions_overview` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — A Claude Code SDK session is the conversation history of a Claude Code agent run; this note documents the persistence model of that product's sessions.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — A session is the durable transcript the harness accumulates (prompt, tool calls, tool results, responses); resume reloads that harness state so the agent keeps full prior context.
- [Context Window](../../term_dictionary/term_context_window.md) — Returning to a session means restoring everything that was in the context window before (files read, analysis done); the note frames resume/fork as recovering context-window state.
- [Compaction](../../term_dictionary/term_compaction.md) — Resuming a long session restarts from the post-compaction message chain, so the note's "full context from before" depends on how compaction has summarized earlier turns.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — Sessions are written to disk as append-only JSONL transcripts under `~/.claude/projects/<encoded-cwd>/`, the immutable event-log model this term defines, which is what makes resume and fork possible.
- [Subagent](../../term_dictionary/term_subagent.md) — Subagent transcripts are stored alongside the main session and restored on resume; the note's cross-host caveats and `subpath` layout cover subagent transcript files too.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The note contrasts session persistence (the conversation) with file checkpointing (the filesystem snapshot) — the restore-point discipline this term defines for reverting agent work.

### 2. `cc_sdk_session_management_api` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the Claude Code Agent SDK's session-control surface (`query()`/`ClaudeAgentOptions`, `ClaudeSDKClient`), so the product term anchors the API being used.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `ClaudeSDKClient` and `continue: true` are harness-level controls that keep the same agent runtime and its accumulated state alive across calls without manual ID handling.
- [Context Window](../../term_dictionary/term_context_window.md) — `resume` and `fork` reload the prior context window so a follow-up query builds on earlier analysis instead of starting fresh; the note's whole purpose is preserving that context across calls.
- [Subagent](../../term_dictionary/term_subagent.md) — `fork_session` branches the conversation (and any subagent transcripts) into a new independent session ID; the note's enumeration helpers (`list_sessions`) also surface subagent-bearing sessions.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — A session's value is that it preserves every prior tool call and tool result; capturing the `session_id` from the result message lets a later `resume` reuse all that tool-use history.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Capturing the `session_id` before shutdown and resuming later (or after `error_max_turns`) is exactly the restore-point pattern this term defines, applied to conversation state rather than files.

### 3. `cc_sdk_session_store` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `SessionStore` adapter mirrors Claude Code SDK session transcripts to external backends; this note documents that product's storage-extension interface.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — The store contract is append-only: `append` writes ordered JSON-safe entries and `load` returns them in the same order, the immutable-log / event-sourcing model this term defines (well suited to append-only backends where `delete` is a no-op).
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — Subagent transcripts are mirrored under `subpath: "subagents/agent-<id>"`, and `listSubkeys` discovers them on resume — exactly the isolated subagent-transcript model this term names.
- [Subagent](../../term_dictionary/term_subagent.md) — `listSubagents`/`getSubagentMessages` and the cascade-delete rule depend on the store handling subagent session keys, so the note's behavior notes are about persisting subagent runs.
- [Compaction](../../term_dictionary/term_compaction.md) — A behavior note states `getSessionMessages` returns the post-compaction chain (e.g. 503 raw entries → 18 messages); understanding the store output requires understanding compaction's summarize-and-replace effect.
- [Redis](../../term_dictionary/term_redis.md) — Redis is one of the three reference backends the note lists for a `SessionStore` (RPUSH/LRANGE list per transcript plus a sorted-set index), grounding the multi-host-store use case.
- [S3](../../term_dictionary/term_s3.md) — S3 is a reference backend (one JSONL part per `append`, lifecycle-policy retention) and the canonical durable store for the note's "local containers are ephemeral" durability argument.
- [Key-Value Store](../../term_dictionary/term_key_value_store.md) — A `SessionStore` is keyed by `SessionKey` (projectKey + sessionId + optional subpath) addressing one transcript, the keyed-blob access pattern this term defines; Redis/S3 backends are concrete KV stores.

### 4. `cc_sdk_session_store_setup` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the build-an-adapter procedure for the Claude Code SDK's `SessionStore`, so the product term anchors the SDK whose store contract is being implemented.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — The adapter must persist `append`ed entries in order and return them deep-equal from `load`; this append-then-replay contract is the append-only-log discipline this term defines.
- [Redis](../../term_dictionary/term_redis.md) — `RedisSessionStore` is one of the runnable reference adapters the note shows copying into a project; the term grounds the `ioredis` list-backed implementation.
- [S3](../../term_dictionary/term_s3.md) — The note's worked wiring example builds `S3SessionStore` with a pre-configured `S3Client`; the term grounds the part-file-per-append S3 storage model the adapter uses.
- [PostgreSQL](../../term_dictionary/term_postgresql.md) — `PostgresSessionStore` (one `jsonb` row per entry ordered by `BIGSERIAL`) is a reference adapter, and the note notes key-reordering `jsonb` backends are fine because `load` need only be deep-equal — a Postgres-specific detail this term grounds.
- [In-Memory Database](../../term_dictionary/term_in_memory_database.md) — The quick-start uses the shipped `InMemorySessionStore` for development/testing; the term defines the volatile, RAM-resident store that backs it.

### 5. `cc_sdk_system_prompts` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `claude_code` preset IS the full Claude Code CLI system prompt; this note explains when to keep that product's prompt versus replace it, so the product term is central.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The system prompt is the instruction set the harness sends to the model; the note's whole decision is how much of the default harness behavior (tool guidance, safety rules) to keep versus override.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Choosing among preset/append/custom and deciding what tool-guidance and safety instructions a custom prompt must re-include is a prompt-engineering decision, the discipline this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note weighs what to put in the system prompt versus CLAUDE.md (injected as conversation context) versus the user message — a context-engineering trade-off about where instructions live and how much weight they carry.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The decision table keys on how closely the agent resembles a coding agent operating in a repo with a human steering; unattended coding automation still fits the preset, the autonomous-coding-agent profile this term defines.
- [Generative Agents](../../term_dictionary/term_generative_agents.md) — "Different identity" means giving the agent its own name, scope, and persona via a custom prompt — the persona-construction concern this term covers for agents that aren't Claude Code.
- [Agent SOP](../../term_dictionary/term_agent_sop.md) — A custom or preset-plus-append system prompt encodes the agent's standard operating procedure (role, rules, output format, safety constraints), the structured-instruction artifact this term defines.

### 6. `cc_sdk_customize_system_prompt` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the how-to for customizing the Claude Code SDK system prompt (preset/append/custom) and CLAUDE.md/output-style loading, so the product term anchors the configuration surface.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — CLAUDE.md gives the agent persistent project context injected into the conversation; the prompt-caching tradeoff also discusses auto-memory paths in the dynamic section — both are the persistent-memory mechanism this term defines.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — A core subsection (`excludeDynamicSections`) is about making the system prompt identical across sessions so different working directories can share a prompt-cache entry — precisely the cached-prefix optimization this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The note positions output styles, hooks, and skills as behavior shapers outside the system prompt; output styles are stored as markdown files like skills and loaded via the same setting sources, so the term grounds that comparison.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Writing the `append` block, the custom string, or an output-style persona is hands-on prompt engineering; the note's best-practice guidance is about crafting effective instructions, this term's domain.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note explains CLAUDE.md is injected into the conversation (not the system prompt) and that moving dynamic context to the first user message lowers its weight — context-placement decisions this term covers.
- [Agent SOP](../../term_dictionary/term_agent_sop.md) — An output style or CLAUDE.md encodes a reusable, versioned standard operating procedure (a code-reviewer persona, team coding standards) layered with session-specific `append`, the structured-procedure artifact this term defines.

### 7. `cc_sdk_todo_and_task_tracking` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Todo/Task tracking is a built-in Claude Code SDK feature that surfaces task progress in the message stream; this note documents that product's todo lifecycle and tooling.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — Todos/Tasks are how the agent organizes a complex multi-step run into discrete tracked items (pending→in_progress→completed) — the work-coordination pattern this term defines, here for a single agent's own plan.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The SDK exposes todo state through `tool_use` blocks (`TodoWrite`, then `TaskCreate`/`TaskUpdate`); monitoring code inspects those tool calls/results, so the note is fundamentally about reading tool-use signals.
- [Workflow Memory](../../term_dictionary/term_workflow_memory.md) — The todo list is the agent's running structured summary of a multi-step workflow's progress and remaining steps — the trajectory/workflow-state representation this term defines.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — Auto-creating todos for tasks needing 3+ distinct actions externalizes the agent's plan into visible steps, an explicit-reasoning-trace behavior aligned with the chain-of-thought decomposition this term defines.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — Real-time progress display and monitoring todo changes in the assistant stream are an observability mechanism for long-running agent runs, the visibility-into-agent-behavior concern this term defines.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — The SDK auto-creating and updating todos for complex tasks without being asked is autonomous task management, a defining behavior of the agentic-AI systems this term covers.

## Section Coverage Map

```
sessions.md
├── intro (session = on-disk conversation) ─ → note 1 (cc_sdk_sessions_overview)
├── Choose an approach (decision table) ──── → note 1
│   └── Continue, resume, and fork ───────── → note 1
├── Automatic session management ────────── → note 2 (cc_sdk_session_management_api)
│   ├── Python: ClaudeSDKClient ─────────── → note 2
│   └── TypeScript: continue: true ──────── → note 2
├── Use session options with query() ────── → note 2
│   ├── Capture the session ID ──────────── → note 2
│   ├── Resume by ID ────────────────────── → note 2
│   └── Fork to explore alternatives ────── → note 2
├── Resume across hosts ─────────────────── → note 1 (encoded-cwd, move-file vs re-derive)
│   └── (multi-host deployment patterns) ── → linked out (B21A hosting); list_sessions helpers → note 2
└── Related resources ───────────────────── → notes 1/2 (links: file-checkpointing→B20C, agent-loop→B19A)
session-storage.md
├── intro (SessionStore mirror) ─────────── → note 3 (cc_sdk_session_store)
├── The SessionStore interface ──────────── → note 3
├── Quick start (InMemorySessionStore) ──── → note 4 (cc_sdk_session_store_setup)
├── Write your own adapter ──────────────── → note 4
├── Reference implementations ───────────── → note 4
│   └── Validate your adapter (conformance) → note 4
├── Behavior notes ──────────────────────── → note 3
│   ├── Dual-write architecture ─────────── → note 3
│   ├── Mirror writes are best-effort ───── → note 3
│   ├── getSessionMessages post-compaction  → note 3
│   ├── forkSession is not a byte copy ──── → note 3
│   ├── Subagent transcripts ────────────── → note 3
│   └── Retention ───────────────────────── → note 3 (CLAUDE_CONFIG_DIR cleanup → B03A env-vars)
├── Supported on (function list) ────────── → note 3
└── Related resources ───────────────────── → notes 3/4 (links: hosting→B21A, sessions→note 1)
modifying-system-prompts.md
├── intro / How system prompts work ─────── → note 5 (cc_sdk_system_prompts)
│   └── Decide on a starting point ──────── → note 5
├── Customize agent behavior ────────────── → note 6 (cc_sdk_customize_system_prompt)
│   ├── CLAUDE.md files ──────────────────── → note 6 (content guidance → B02B /en/memory)
│   ├── Output styles ───────────────────── → note 6 (CLI format/storage → B06 output-styles)
│   │   └── Improve prompt caching ──────── → note 6 (--exclude-dynamic-… CLI flag → B03B)
│   ├── Append to the preset ─────────────── → note 6
│   └── Custom system prompts ───────────── → note 6
├── Compare the four approaches (matrix) ── → note 5
├── Use cases and best practices ────────── → note 6 (when-to-use CLAUDE.md/styles/append/custom)
├── Combine approaches ──────────────────── → note 6
│   └── Combine output style + append ───── → note 6
└── See also ────────────────────────────── → notes 5/6 (links: output-styles→B06, memory→B02B, settings→B03A)
todo-tracking.md
├── intro (built-in todo functionality) ─── → note 7 (cc_sdk_todo_and_task_tracking)
├── Todo Lifecycle ──────────────────────── → note 7
├── When Todos Are Used ─────────────────── → note 7
├── Examples ────────────────────────────── → note 7
│   ├── Monitoring Todo Changes ─────────── → note 7
│   └── Real-time Progress Display ──────── → note 7
├── Migrate to Task tools ───────────────── → note 7
└── Related Documentation ───────────────── → note 7 (links: typescript/python ref→B21B/B21C, streaming→B19C)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| sessions (2,211w, 5 H2 mixed) | notes 1 (concept) + 2 (procedure) + 2 link-outs | distinct BB: the *what/when* model (session/continue/resume/fork + cross-host) is concept; the `query()` option *how-to* (ClaudeSDKClient, capture ID, resume=, fork_session) is procedure with code. Hosting patterns owned by B21A. |
| session-storage (1,660w, 7 H2) | notes 3 (concept) + 4 (procedure) | the `SessionStore` interface + behavior-notes contract is concept; quick-start/write-adapter/reference-impls/conformance is a build procedure with code. |
| modifying-system-prompts (3,059w >2500) | notes 5 (concept) + 6 (procedure) | exceeds density cap; choose-an-approach + four-method comparison (concept) vs apply-each-method how-to + prompt-caching + combine (procedure) differ in BB and would blow the word/code caps if merged. |
| todo-tracking (1,216w, 3 H2) | note 7 only | small, single-topic; lifecycle + monitoring + Task-tools migration are one concept note (the migration is explanatory, not a separate procedure). |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_sessions_overview | concept | 600 | 0 | ✅ |
| 2 | cc_sdk_session_management_api | procedure | 700 | 6 | ✅ (= cap; Python+TS pairs for capture/resume/fork) |
| 3 | cc_sdk_session_store | concept | 650 | 2 | ✅ (interface TS+Py) |
| 4 | cc_sdk_session_store_setup | procedure | 600 | 4 | ✅ (quick-start TS+Py, S3 wiring, conformance) |
| 5 | cc_sdk_system_prompts | concept | 650 | 0 | ✅ (decision + comparison tables) |
| 6 | cc_sdk_customize_system_prompt | procedure | 750 | 6 | ✅ (= cap; preset/append/exclude-dynamic/custom/output-style/combine — trim to representative pairs) |
| 7 | cc_sdk_todo_and_task_tracking | concept | 600 | 3 | ✅ (monitoring + migration snippets, one language each) |

No note exceeds the caps. Notes 2 and 6 sit AT the 6-code-block cap — execution MUST keep to the representative
Python/TypeScript pairs listed (drop redundant duplicate examples) and SPLIT if a draft would need a 7th block.
No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_sessions_overview cc_sdk_session_management_api cc_sdk_session_store cc_sdk_session_store_setup cc_sdk_system_prompts cc_sdk_customize_system_prompt cc_sdk_todo_and_task_tracking"
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

Single phase (7 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (preset names, option fields, version gates verbatim) | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present (notes 2/6 ≤6 code) | per-note check + coverage map |
| G4-CrossRef | links resolve, `source_url` present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 7 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 7 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (in-degree ≥1) | verified by DB query that in-degree ≥1 for all 7 (anti-island) | sqlite3 in-degree on `note_links` |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes across the corpus), the series gets
`0_entry_points/entry_claude_code_docs.md`; this sub-plan **contributes its 7 rows** under an "Agent SDK"
cluster (Sessions & System Prompts) + increments the BB-distribution counts (concept ×4, procedure ×3).

## Undigested Terms Plan (Step 2d scan of the 4 pages)

b19b creates **no new `term_dictionary` notes** — every vocabulary term these pages use is covered by an
existing substantive term note (link), a b19b `cc_` note, or its home sub-plan (Pattern B; dedup checked
across **both** `term_dictionary/` AND `resources/documentation/`):

| Term surfaced on the pages | Disposition |
|---|---|
| Session (SDK conversation history) | note 1 `cc_sdk_sessions_overview` (doc concept) — NOT `term_session` (does not exist) and NOT `term_sessionid`/`term_session_persistence`/`term_sessionminer` (abuse/networking false positives, excluded) |
| Continue / Resume / Fork | note 1 + note 2 (doc concepts; `query()` options) |
| SessionStore / session store adapter | notes 3, 4 (doc concept + procedure) |
| `claude_code` preset / append / custom system prompt | notes 5, 6 (doc concepts/procedure) |
| Output style | link `term_skills` for the file-based-config analogy; full CLI definition owned by B06 (`output-styles`) — captured there |
| CLAUDE.md / auto memory | link `term_agentic_memory` (exists); content guidance owned by B02B (`memory.md`) |
| Todo / Task tools (`TodoWrite`/`TaskCreate`) | note 7 (doc concept) |
| Prompt caching | link `term_prompt_caching` (exists) |
| Compaction / Context window / Subagent / Agent harness / MCP | existing term notes (link) |
| Prompt engineering / Context engineering / Agent SOP / Agent orchestration / Multi-agent | existing term notes (link) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/code
comments for newly-surfaced terms. Candidates examined and routed: **"dual-write architecture / mirror"**
(session-storage) → explained inline in note 3, owned by `term_append_only_state` (link), no new capture;
**"encoded-cwd / project key"** (sessions, session-storage) → explained inline in notes 1/3, owned by
`term_key_value_store` framing (link), no new capture; **"`excludeDynamicSections` / dynamic system-prompt
sections"** (modifying-system-prompts) → explained inline in note 6, owned by `term_prompt_caching` (link);
**"conformance suite"** (session-storage) → procedure detail in note 4, no term. **0 new b19b
`term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b19b authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the SDK concepts duplicate existing notes?) was
performed across BOTH dirs: no existing `documentation/` coverage of SDK sessions/system-prompts/todos
(grep + bm25 returned 0 `documentation/` hits), and the agentic terms (`term_claude_code`, `term_mcp`,
`term_subagent`, `term_context_window`, `term_compaction`, `term_agent_harness`, `term_skills`,
`term_agentic_memory`, `term_prompt_caching`, `term_append_only_state`, `term_sidechain_transcript`,
`term_redis`, `term_s3`, `term_postgresql`, `term_key_value_store`, `term_in_memory_database`,
`term_agent_orchestration`, `term_function_calling`, `term_prompt_engineering`, `term_context_engineering`,
`term_agent_sop`, `term_generative_agents`, `term_autonomous_coding_agents`, `term_workflow_memory`,
`term_observability_agent_systems`, `term_agentic_ai`, `term_chain_of_thought`,
`term_regular_checkpointing`) all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b19b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8 discoverability) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim — copy Python/TypeScript exactly from the source (preset names, option fields,
  `CLAUDE_CODE_ENABLE_TASKS=0`, version-gate strings); one BB per note; each note ≤400 lines (split if a
  draft >350). Notes 2/6 are AT the 6-code cap — keep to the representative pairs.
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase
  (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 —
in-degree ≥1 for every note):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 5, 7 | product term → CC SDK session model / system-prompt customization / todo tracking |
| `term_dictionary/term_append_only_state.md` | notes 1, 3 | append-only JSONL term → SDK session persistence + SessionStore contract |
| `term_dictionary/term_prompt_caching.md` | note 6 | prompt-caching term → `excludeDynamicSections` cross-session cache reuse |
| `term_dictionary/term_sidechain_transcript.md` | note 3 | subagent-transcript term → SessionStore subagent `subpath` mirroring |
| `term_dictionary/term_agent_orchestration.md` | note 7 | orchestration term → SDK todo/Task progress tracking |
| `term_dictionary/term_s3.md` | notes 3, 4 | S3 term → reference SessionStore backend |

## Follow-up Recommendations

- After the 7 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify DB
  in-degree ≥1 per note — G7/G8); queue the 7 rows for `entry_claude_code_docs.md` under the Agent SDK
  cluster; add sibling cross-links once B19A (SDK core/lifecycle), B19C (streaming/I-O), B20A-C (tools/
  skills/hooks), and B21A (hosting) land; `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE 2026-06-13 |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B19B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/agent-sdk/`; measured words
  (sessions 2,211 · session-storage 1,660 · modifying-system-prompts 3,059 · todo-tracking 1,216 = 8,146)
  match the master's figure exactly. No >1.5× under-estimate; the one >2500w page
  (modifying-system-prompts) is split into a concept + procedure note (notes 5/6).
- **Notes**: 7 (concept 4, procedure 3) — equals master estimate. Three documented splits + one keep-whole.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–8 term notes per note (26 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
  positives (`term_session_persistence`, `term_sessionid`, `term_sessionminer`) explicitly excluded. Sibling
  `cc_*` cross-links (B19A/B19C/B20*/B21A) kept as prose forward-refs (those sub-plans not yet executed).
- **Dedup (Step 2b/4e across BOTH dirs)**: bm25 + grep returned **0** `documentation/` hits for SDK
  sessions/system-prompts/todos → no existing doc note to enrich; create new. All agentic terms exist →
  link, not recreate.
- **Step 2d new-term scan**: 4 candidates examined (dual-write/mirror, encoded-cwd, excludeDynamicSections,
  conformance suite) → all explained inline + routed to existing terms; **0 new b19b term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G7/G8 gate rows, Section Coverage Map, Split Decisions, Density Re-Assessment, Inlinks.
- **28-item checklist**: PASS (term-note items N/A — b19b authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed (below); set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 corpus notes → CREATE required); B19B contributes 7 rows under the Agent SDK cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 7 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | 3,059w page split (notes 5/6); notes 2/6 at the 6-code cap with explicit "keep representative pairs / split if 7th needed" rule; no other borderline note. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` per page: sessions 2,211 · session-storage 1,660 · modifying-system-prompts 3,059 · todo-tracking 1,216 = 8,146 = master figure (±0%). |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B19B authors 0 term notes; Undigested Terms Plan routes every term (Pattern B, dedup across both dirs); Authoring Requirements inherited from master. |
| CP9 | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); cross-dir collision check documented — 0 `documentation/` SDK-session/system-prompt/todo coverage, all 28 agentic terms linked not recreated; 3 false-positive session terms excluded with rationale. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
