---
title: Sub-Plan B20C — Claude Code Docs: SDK Hooks, Permissions & Checkpointing
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/hooks", "agent-sdk/permissions", "agent-sdk/file-checkpointing"]
---

# Sub-Plan B20C: SDK Hooks, Permissions & Checkpointing

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted exemplar [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / 8-GATE / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The three Agent-SDK control-and-safety pages: **hooks** (intercept/customize agent behavior at execution
points), **permissions** (modes + declarative allow/deny rules that gate tool use), and **file
checkpointing** (rewind file changes made via Write/Edit/NotebookEdit). P2 (Phase B) — these are
SDK-application features built on the P1 SDK cores (B19A) and the Claude Code permission/hook concepts
(B05A, B07A/B07B). These are the **SDK** treatments of hooks/permissions; the non-SDK Claude Code hook
reference (B07A/B07B) and permission docs (B05A) are sibling sub-plans and are linked, never duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en/agent-sdk`), 3 pages, 9,625 measured words.
**Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the safety/control mechanisms an SDK app author must wire in — the hook event model,
  the permission evaluation order, and the rewind/restore lifecycle. These are the load-bearing decisions.
- **Group / split**: `hooks.md` (4,541w, 26 code pairs, 1 page) is far over caps → split by BB into
  overview (concept), configuration (procedure), examples (procedure), troubleshooting (procedure).
  `file-checkpointing.md` (3,327w, 21 code) → split into concepts (concept) + implementation (procedure).
  `permissions.md` (1,757w) → split into evaluation/rules (concept) + modes (concept). The binding cap is
  **≤6 code blocks/note**: source pairs every example as Python+TypeScript inside `<CodeGroup>`; digest
  notes keep ONE representative language (Python) per example to respect the cap.
- **Skip / link-out (own other sub-plans)**: `canUseTool` runtime-approval callback → B19C/`user-input`
  (referenced, not digested here); the Claude Code (non-SDK) hooks reference + matcher-pattern schema →
  B07A `hooks.md` / B07B `hooks-guide.md`; non-SDK permission modes / `settings.json` permission rules →
  B05A `permissions.md` + B03A `settings.md`; sessions/resume (needed for post-stream rewind) → B19B
  `sessions.md`; SDK type defs (`HookInput`, `synchookjsonoutput`) → B21B/B21C language refs. Referenced
  via links, never duplicated.
- **Terms**: not re-digested into `cc_` notes — SDK vocabulary routes to existing term notes / its home
  sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of
`code.claude.com/docs/en/agent-sdk/<slug>.md`). Code-block count is fenced pairs counted as displayed
(Python+TypeScript via `<CodeGroup>`); digest notes keep one representative language per example.

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| hooks | /agent-sdk/hooks | 4,541 | 26 | 6 | 19 | concept + procedure |
| permissions | /agent-sdk/permissions | 1,757 | 5 | 4 | 3 | concept |
| file-checkpointing | /agent-sdk/file-checkpointing | 3,327 | 21 | 7 | 6 | concept + procedure |

> **H2 lists (document order):**
> - **hooks**: How hooks work · Available hooks (events table) · Configure hooks (H3 Matchers, Callback
>   functions [H4 Inputs, Outputs, Asynchronous output]) · Examples (H3 Modify tool input, Add context
>   and block a tool, Auto-approve specific tools, Register multiple hooks, Filter with multi-tool
>   matchers, Track subagent activity, Make HTTP requests from hooks, Forward notifications to Slack) ·
>   Fix common issues (H3 Hook not firing, Matcher not filtering, Hook timeout, Tool blocked
>   unexpectedly, Modified input not applied, Session hooks not available in Python, Subagent permission
>   prompts multiplying, Recursive hook loops with subagents, systemMessage not appearing) · Related resources
> - **permissions**: How permissions are evaluated (5-step flow) · Allow and deny rules · Permission
>   modes (H3 Available modes, Set permission mode, Mode details [H4 acceptEdits, dontAsk,
>   bypassPermissions, plan]) · Related resources
> - **file-checkpointing**: How checkpointing works · Implement checkpointing (3-step) · Common patterns
>   (H3 Checkpoint before risky operations, Multiple restore points) · Try it out · Limitations ·
>   Troubleshooting (H3 options not recognized, no UUIDs, no checkpoint found, ProcessTransport not
>   ready) · Next steps

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Target dir:
`resources/documentation/claude_code/`, prefix `cc_`. **8 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_hooks_overview.md` | concept | hooks: How hooks work, Available hooks | 450 | What SDK hooks are (callbacks on agent events); the 5-step fire→collect→match→execute→decide flow; the 20-event table (Pre/PostToolUse, Stop, Subagent*, PreCompact, Notification, Session*, etc.) with Python/TS availability. Full JSON schema → B07A `hooks.md` (link-out). |
| 2 | `cc_sdk_hooks_configuration.md` | procedure | hooks: Configure hooks, Matchers, Callback functions (Inputs/Outputs/Async) | 550 | How to register hooks via `options.hooks`; matcher rules (exact vs glob vs regex, `mcp__` naming); callback inputs (session_id/cwd/tool_use_id/context), outputs (`hookSpecificOutput`, `permissionDecision` allow/deny/ask/defer, `updatedInput`, `additionalContext`); precedence deny>defer>ask>allow; async outputs. |
| 3 | `cc_sdk_hooks_examples.md` | procedure | hooks: Examples (8 patterns) | 550 | Recipe patterns: modify tool input (sandbox redirect), block a tool + systemMessage, auto-approve read-only tools, register multiple parallel hooks, multi-tool matchers, track subagent activity, HTTP/webhook from hooks, forward notifications to Slack. One representative Python block per pattern. |
| 4 | `cc_sdk_hooks_troubleshooting.md` | procedure | hooks: Fix common issues | 400 | Diagnostics: hook not firing (case-sensitive event names, max_turns), matcher not filtering (tool name only), timeouts, unexpected blocks, modified-input placement, Python-only session-hook gap, subagent permission multiplication, recursive subagent loops, systemMessage not surfacing (`includeHookEvents`). |
| 5 | `cc_sdk_permissions_evaluation.md` | concept | permissions: How permissions are evaluated, Allow and deny rules | 500 | The 5-step evaluation order (hooks → deny → ask → permission mode → allow → `canUseTool`); allow vs deny rule semantics (bare-name deny removes tool from context; scoped `Bash(rm *)` deny holds even in bypass; `mcp__<server>__*` globs); `settings.json` declarative rules. `canUseTool` runtime callback → B19C `user-input` (link-out). |
| 6 | `cc_sdk_permission_modes.md` | concept | permissions: Permission modes (Available, Set, Mode details) | 550 | The 6 modes (default, dontAsk, acceptEdits, bypassPermissions, plan, auto-TS-only) with tool behavior; setting at query time vs dynamically (`set_permission_mode`); per-mode detail (acceptEdits filesystem ops scope, dontAsk hard-deny, bypass cautions, plan read-only); subagent mode inheritance warning. |
| 7 | `cc_sdk_file_checkpointing_concepts.md` | concept | file-checkpointing: How checkpointing works, Limitations | 400 | What the checkpoint system tracks (created/modified files + original content via Write/Edit/NotebookEdit only); checkpoint UUID = user-message UUID; rewind restores files on disk, NOT the conversation; the 4 limitations (tool-scope, same-session, file-content-only, local-files). |
| 8 | `cc_sdk_file_checkpointing_implementation.md` | procedure | file-checkpointing: Implement, Common patterns, Try it out, Troubleshooting | 600 | The 3-step flow (enable `enable_file_checkpointing` + `replay-user-messages`, capture UUID + session_id, resume-with-empty-prompt then `rewind_files()`); CLI `--rewind-files`; patterns (checkpoint-before-risky-op, multiple restore points); troubleshooting (no UUIDs, no-checkpoint-found, ProcessTransport-not-ready). Resume dependency → B19B `sessions.md`. |

**Estimate: 8 notes** — concept ×4 (notes 1,5,6,7), procedure ×4 (notes 2,3,4,8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (9,625 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,000 (avg ~500/note). Code blocks: ≤6 per note (one representative language
  per source example pair); source has 52 fenced blocks total (26 Python+TS pairs) across hooks +
  checkpointing — the split into 8 notes keeps every note within the ≤6-code cap.
- **Building Block Distribution**: concept ×4 (notes 1,5,6,7) · procedure ×4 (notes 2,3,4,8). No
  model/argument/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (16 distinct `term_dictionary/` terms across

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_sdk_hooks_overview` (7 term notes)
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — A behavioral design pattern where observers register to be notified of events on a subject; relevance: SDK hooks ARE the observer pattern — callbacks register for agent events (PreToolUse, Stop, SubagentStop) and the SDK notifies each registered hook when the event fires.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — A software style where components communicate by producing/consuming events; relevance: the note's whole model is event-driven — "something happens during agent execution and the SDK fires an event," with the 20-event table enumerating the producible event types.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Encapsulates a request/operation as an object that can be intercepted, queued, or vetoed; relevance: each tool call the hook intercepts is a reified command the callback can inspect and approve/deny before execution, the command-pattern interception point.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool whose Agent SDK this page documents; relevance: hooks are a customization surface of the Claude Code agent runtime, so the product term anchors what these callbacks extend.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — The orchestration layer wrapping the LLM with tools, context, and execution control; relevance: hooks fire at the harness's execution points (tool dispatch, compaction, session start/stop), making the harness the thing whose lifecycle these events expose.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The mechanism by which an LLM invokes tools and consumes their results; relevance: PreToolUse/PostToolUse/PostToolUseFailure — the most-used hook events — wrap exactly the tool-use request/result cycle this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — A spawned worker agent with its own isolated context; relevance: the SubagentStart/SubagentStop events in the table fire on subagent lifecycle, so the subagent concept grounds two of the documented hook events.

### 2. `cc_sdk_hooks_configuration` (7 term notes)
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — Observers register against a subject's event types; relevance: `options.hooks` is the registration map keyed by event name with arrays of matcher+callback observers — the concrete observer-registration API this note documents.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — Event producers, dispatch, and matchers/filters route events to handlers; relevance: matchers (exact/glob/regex against tool name) are the event-routing filter layer, and callback inputs/outputs are the event-handler contract this note specifies.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Tools are invoked with typed inputs and return outputs; relevance: callback inputs carry `tool_name`/`tool_input` and outputs set `permissionDecision`/`updatedInput`/`updatedToolOutput` — the note configures interception of the function-calling payload.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The protocol exposing external servers' tools to the agent; relevance: matcher rules have special `mcp__<server>__<action>` naming semantics (e.g. `^mcp__` regex matches all MCP tools), so MCP tool naming is load-bearing for matcher configuration.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — Supplies tools, context management, and execution control; relevance: the callback's `context`, `session_id`, `cwd`, and `tool_use_id` correlation are values the harness threads into each hook, and the deny>defer>ask>allow precedence is a harness arbitration rule.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agent runtime configured via `ClaudeAgentOptions`; relevance: hook configuration is passed through Claude Code's options object, the same options surface that configures the rest of the agent.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — The metadata/name by which a tool is identified to the agent; relevance: matchers filter strictly by tool name (the descriptor identity), not by file paths or arguments — a distinction this note makes explicit.

### 3. `cc_sdk_hooks_examples` (7 term notes)
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Programmatic constraints that block unsafe model actions; relevance: the block-/etc-writes and protect-.env examples are textbook guardrails — code that vetoes dangerous tool calls before they execute, the note's core use case.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — A policy posture where actions are blocked unless explicitly permitted; relevance: the "deny takes priority; a single deny blocks regardless of other hooks" rule the multi-hook example relies on is the deny-first arbitration this term names.
- [Safelist](../../term_dictionary/term_safelist.md) — An explicit allow-list of permitted entities; relevance: the auto-approve-read-only example builds a `["Read","Glob","Grep"]` safelist that returns `permissionDecision:"allow"` only for listed tools, the canonical safelist mechanism.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — Confining operations to an isolated, restricted environment; relevance: the modify-tool-input example rewrites `file_path` to prepend `/sandbox`, redirecting all writes into a sandboxed directory — a hook-implemented sandbox.
- [Subagent](../../term_dictionary/term_subagent.md) — A spawned worker agent reporting back to a coordinator; relevance: the track-subagent-activity example registers a SubagentStop hook to log each subagent's transcript and id when it finishes, monitoring subagent fan-out.
- [Pub/Sub (Publish-Subscribe)](../../term_dictionary/term_pub_sub.md) — A messaging pattern broadcasting events to subscribers; relevance: the webhook and Slack-notification examples publish agent events outward to external services (HTTP endpoint, Slack channel), the fan-out-to-subscribers half of pub/sub.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agent runtime these recipes customize; relevance: every example is a customization of Claude Code's tool-execution behavior via the SDK hook surface.

### 4. `cc_sdk_hooks_troubleshooting` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — Spawned workers with their own permission/hook context; relevance: two of the documented issues — "subagent permission prompts multiplying" (subagents don't inherit parent permissions) and "recursive hook loops with subagents" — are subagent-specific failure modes.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The tool-invocation cycle hooks intercept; relevance: "matcher not filtering" and "tool blocked unexpectedly" are diagnosed by inspecting tool name vs `tool_input` arguments and `permissionDecision:'deny'` returns — the tool-use payload.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — Owns turn limits, session lifecycle, and message surfacing; relevance: "hooks may not fire at max_turns" and "systemMessage not appearing" are harness-behavior quirks (session ends before hooks run; SDK doesn't surface hook output without `includeHookEvents`).
- [Claude Code](../../term_dictionary/term_claude_code.md) — The runtime whose hook behavior is being debugged; relevance: every diagnostic targets Claude Code SDK hook registration (case-sensitive event names, `options.hooks` placement).
- [Multi-Agent (Multi-Agent Systems)](../../term_dictionary/term_multi_agent.md) — Multiple coordinating agents sharing/contending for resources; relevance: the multiplying-prompts and recursive-loop issues arise specifically when one session spawns many subagents — the multi-agent operating regime where these bugs surface.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Progressively widening what an agent may do without asking; relevance: the recommended fix for repeated subagent prompts (auto-approve specific tools via PreToolUse, or configure permission rules for subagent sessions) is a graduated-trust allowance applied to delegated agents.

### 5. `cc_sdk_permissions_evaluation` (7 term notes)
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Block by default; require explicit allow; relevance: deny rules are checked before allow rules and hold even in `bypassPermissions`, and bare-name deny removes the tool from context entirely — the deny-first ordering this note's 5-step flow encodes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — A spectrum of how much autonomy is granted; relevance: the evaluation flow ends in the permission mode, the dial that moves an agent from prompt-everything to bypass-everything — the graduated-trust axis the rule layers feed into.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Hard constraints on agent actions; relevance: scoped deny rules like `Bash(rm *)` that hold in every mode are non-overridable guardrails the note shows surviving even `bypassPermissions`.
- [Contingent Authorization](../../term_dictionary/term_contingent_authorization.md) — Permission granted conditionally pending a check; relevance: `ask` rules route a matching call to the `canUseTool` callback for runtime confirmation — authorization made contingent on an interactive decision, exactly this concept.
- [Safelist](../../term_dictionary/term_safelist.md) — An explicit allow-list; relevance: `allowed_tools=["Read","Grep"]` is a tool safelist that auto-approves listed tools; the note also warns the safelist does NOT constrain `bypassPermissions`.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The tool requests being authorized; relevance: every rule (`allowed_tools`/`disallowed_tools`/globs) is matched against a tool-use request, the unit of authorization the evaluation flow processes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agent whose tool access these rules gate; relevance: the rules are SDK options + `.claude/settings.json` entries read by the Claude Code runtime, anchoring the permission system to the product.

### 6. `cc_sdk_permission_modes` (8 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Progressive autonomy from ask-always to full bypass; relevance: the 6 modes (default → acceptEdits → plan → dontAsk → bypassPermissions → auto) are precisely a graduated-trust ladder, and `set_permission_mode` lets you climb it mid-session "as trust builds."
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Default-block posture; relevance: `dontAsk` mode converts any would-be prompt into a hard denial — the strictest deny-first stance the note offers for locked-down headless agents.
- [Human in the Loop - Interactive ML System Design](../../term_dictionary/term_human_in_the_loop.md) — System designs that route decisions to a human; relevance: `default` and `plan` modes route unmatched/file-edit calls to the `canUseTool` callback for human approval — the human-in-the-loop gate these modes implement.
- [HITL - Human in the Loop](../../term_dictionary/term_hitl.md) — Human-approval checkpoints in an automated flow; relevance: the modes are the dial controlling HOW MUCH stays under human approval vs auto-approved — `acceptEdits`/`bypass` remove HITL gates, `default`/`plan` keep them.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Agents that act across files/commands with minimal supervision; relevance: `bypassPermissions` grants the agent full autonomous system access — the maximal-autonomy operating mode of an autonomous coding agent, with the note's explicit caution.
- [Subagent](../../term_dictionary/term_subagent.md) — Spawned workers that inherit configuration; relevance: the prominent inheritance warning — subagents inherit `bypassPermissions`/`acceptEdits`/`auto` and it cannot be overridden per subagent — is a subagent-specific safety caveat of mode selection.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Weighting how much autonomy to grant by how reversible the action is; relevance: `acceptEdits` auto-approves reversible file ops while leaving non-reversible Bash subject to prompts — the reversibility-weighted granting this term formalizes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The runtime these modes configure; relevance: modes are set via `ClaudeAgentOptions.permission_mode`, the same mode dial Claude Code exposes interactively, grounding the SDK modes in the product.

### 7. `cc_sdk_file_checkpointing_concepts` (7 term notes)
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Periodically saving recoverable state so work can be restored; relevance: this note IS the checkpointing concept page for the SDK — it defines what a checkpoint captures (created/modified files + original content) and that each user-message UUID is a restore point.
- [Memento Pattern](../../term_dictionary/term_memento_pattern.md) — Captures an object's state externally so it can be restored later without violating encapsulation; relevance: the checkpoint stores files' original content as an opaque snapshot the SDK later restores via `rewindFiles()` — a file-level memento.
- [Write-Ahead Log (WAL)](../../term_dictionary/term_write_ahead_log.md) — Recording prior state/changes before mutation to enable recovery; relevance: the SDK "creates backups of files before modifying them" through Write/Edit/NotebookEdit — the write-ahead-before-mutate principle this term names, enabling rollback.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — Accumulating immutable state entries rather than overwriting; relevance: checkpoint UUIDs accumulate per user message (multiple restore points) as an append-only history of restorable states, the model the multi-checkpoint concept relies on.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Reasoning about action risk by how reversible it is; relevance: checkpointing exists to make agent file edits reversible, and the note's limitations (Bash writes not tracked, dirs not undone) define exactly which actions remain irreversible.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Encapsulating operations as objects supporting undo; relevance: rewind = the undo half of the command pattern applied to tool-issued file mutations, with each tracked Write/Edit being a reversible command.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agent whose file edits are checkpointed; relevance: checkpointing tracks edits made by Claude Code's Write/Edit/NotebookEdit tools during a session, anchoring the feature to the product runtime.

### 8. `cc_sdk_file_checkpointing_implementation` (7 term notes)
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Saving recoverable state at intervals; relevance: this note implements the regular-checkpointing loop — capture a UUID before each agent turn (checkpoint-before-risky-op) so you can roll back to the last safe state.
- [Memento Pattern](../../term_dictionary/term_memento_pattern.md) — Externalized state snapshots restored on demand; relevance: `rewind_files(checkpoint_id)` is the memento restore call, and the multiple-restore-points pattern stores an array of memento UUIDs with metadata.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Agents that edit code across turns largely unsupervised; relevance: the patterns pair checkpointing with `permission_mode="acceptEdits"` so an autonomous agent can edit freely while the app keeps a safe rollback point — the core operating recipe here.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Granting autonomy proportional to reversibility; relevance: checkpoint-before-risky-operations makes risky edits reversible so the app can let the agent proceed and revert on a failure/validation condition.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Operations as undoable objects; relevance: the rewind call (and CLI `--rewind-files`) is the executed undo over the sequence of file-edit commands the session issued.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — Immutable accumulating history; relevance: the multiple-restore-points pattern appends each turn's checkpoint UUID to a list, building an append-only restore-point history to selectively rewind into.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The runtime whose session is resumed and rewound; relevance: implementation hinges on Claude Code session IDs (`resume=session_id`) and the `enable_file_checkpointing` option of `ClaudeAgentOptions`.

## Section Coverage Map

```
agent-sdk/hooks.md
├── How hooks work (5-step Steps + intro example) ─ → note 1 (cc_sdk_hooks_overview)
├── Available hooks (20-event table) ────────────── → note 1
├── Configure hooks (options.hooks) ─────────────── → note 2 (cc_sdk_hooks_configuration)
│   ├── Matchers (exact/glob/regex, mcp__ naming) ─ → note 2
│   └── Callback functions ───────────────────────  → note 2
│       ├── Inputs (session_id/cwd/tool_use_id) ─── → note 2
│       ├── Outputs (hookSpecificOutput, decision)  → note 2
│       └── Asynchronous output (async_/asyncTimeout)→ note 2
├── Examples (8 H3 patterns) ────────────────────── → note 3 (cc_sdk_hooks_examples)
├── Fix common issues (9 H3 issues) ─────────────── → note 4 (cc_sdk_hooks_troubleshooting)
└── Related resources ──────────────────────────── → notes 1-4 (links: B07A hooks ref, B07B guide, B19C user-input)
agent-sdk/permissions.md
├── How permissions are evaluated (5-step) ──────── → note 5 (cc_sdk_permissions_evaluation)
├── Allow and deny rules ────────────────────────── → note 5
├── Permission modes ────────────────────────────── → note 6 (cc_sdk_permission_modes)
│   ├── Available modes (6-mode table) ──────────── → note 6
│   ├── Set permission mode (query-time/dynamic) ── → note 6
│   └── Mode details (acceptEdits/dontAsk/bypass/plan)→ note 6
└── Related resources ──────────────────────────── → notes 5/6 (links: B19C user-input, B05A permissions, B03A settings)
agent-sdk/file-checkpointing.md
├── How checkpointing works ─────────────────────── → note 7 (cc_sdk_file_checkpointing_concepts)
├── Limitations ─────────────────────────────────── → note 7
├── Implement checkpointing (3-step) ────────────── → note 8 (cc_sdk_file_checkpointing_implementation)
├── Common patterns (risky-op, multiple restore) ── → note 8
├── Try it out (interactive example) ────────────── → note 8
├── Troubleshooting (4 H3 issues) ───────────────── → note 8
└── Next steps ──────────────────────────────────── → notes 7/8 (links: B19B sessions, B05A permissions)
```
No orphaned sections. `canUseTool` runtime callback, the non-SDK hooks/permissions schemas, sessions/resume,
and SDK language type defs are linked out to their owning sub-plans (B19B/B19C, B05A, B07A/B07B, B03A, B21B/B21C), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| hooks.md (4,541w >2500, 26 code, 6 H2 mixed) | notes 1,2,3,4 + link-outs | exceeds word + code caps; distinct BBs — event model/table (concept) vs registration mechanics (procedure) vs recipe patterns (procedure) vs diagnostics (procedure); JSON schema + matcher reference owned by B07A |
| permissions.md (1,757w, 4 H2) | notes 5,6 | evaluation order + rule semantics (concept) vs the mode catalog (concept) are separable; keeps each note focused and ≤6 code; `canUseTool` owned by B19C |
| file-checkpointing.md (3,327w >2500, 21 code, 7 H2) | notes 7,8 | exceeds word + code caps; what-it-tracks + limitations (concept) vs enable/capture/rewind + patterns + try-it + troubleshooting (procedure) differ in BB; resume/session machinery owned by B19B |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_hooks_overview | concept | 450 | 1 | ✅ |
| 2 | cc_sdk_hooks_configuration | procedure | 550 | 3 | ✅ |
| 3 | cc_sdk_hooks_examples | procedure | 550 | 6 | ✅ |
| 4 | cc_sdk_hooks_troubleshooting | procedure | 400 | 2 | ✅ |
| 5 | cc_sdk_permissions_evaluation | concept | 500 | 1 | ✅ |
| 6 | cc_sdk_permission_modes | concept | 550 | 3 | ✅ |
| 7 | cc_sdk_file_checkpointing_concepts | concept | 400 | 0 | ✅ |
| 8 | cc_sdk_file_checkpointing_implementation | procedure | 600 | 6 | ✅ |

No note exceeds caps. The binding constraint is **≤6 code/note**: notes 3 and 8 cap at 6 (one
representative Python block per source example pair; the parallel TypeScript blocks are dropped, with a
one-line "TS equivalent available" prose pointer to the B21C reference). No over-compression — every
H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_hooks_overview cc_sdk_hooks_configuration cc_sdk_hooks_examples cc_sdk_hooks_troubleshooting cc_sdk_permissions_evaluation cc_sdk_permission_modes cc_sdk_file_checkpointing_concepts cc_sdk_file_checkpointing_implementation"
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

Single phase (8 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (esp. mode/event names, option flags) | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (sibling) | intra-cluster sibling `cc_*` links resolve; cluster not internally orphaned | DB in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md`; this sub-plan **contributes its 8 rows** under an "Agent SDK —
Hooks / Permissions / Checkpointing" cluster + increments the BB-distribution counts (concept ×4,
procedure ×4). The entry-point back-link is added to each note at finalization.

## Undigested Terms Plan (Step 2d)

b20c creates **no new `term_dictionary` notes** — SDK control/safety vocabulary is covered by a b20c `cc_`
concept note, an existing substantive term note (link), or its home sub-plan (Pattern B):

| Term surfaced in pages | Disposition |
|---|---|
| Hook / hook event (PreToolUse, PostToolUse, Stop, …) | note 1 `cc_sdk_hooks_overview` (doc concept); non-SDK hook reference owned by B07A |
| Matcher / matcher pattern | note 2 `cc_sdk_hooks_configuration`; full schema → B07A `hooks.md` |
| Permission mode (default/dontAsk/acceptEdits/bypassPermissions/plan/auto) | note 6 `cc_sdk_permission_modes`; non-SDK modes owned by B05A |
| Allow / deny / ask rule | note 5 `cc_sdk_permissions_evaluation`; `settings.json` rule syntax → B03A/B05A |
| `canUseTool` callback | linked to B19C `user-input` (owns interactive approval); referenced, not defined here |
| Checkpoint / rewind / restore point | notes 7,8; concept also links existing `term_regular_checkpointing` |
| Subagent / MCP / Compaction / Context window / Sandboxing / Permission mode (trust) | existing term notes (link) — `term_subagent`, `term_mcp`, `term_compaction`, `term_context_window`, `term_sandbox`, `term_graduated_trust` |
| Session / resume | owned by B19B (`sessions.md` / `session-storage.md`) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code
comments for newly-surfaced terms. Candidates considered: "defer" (a `permissionDecision` value — a field
value, not a vocabulary term; folded into note 2), "elicitation" (notification subtype — folded into note
3, owned conceptually by B19C user-input), "PostToolBatch / MessageDisplay / TeammateIdle / WorktreeCreate"
(TS-only hook events — enumerated in note 1's table, no separate term; worktree concept owned by B10B). All
map to an existing note/term/home sub-plan. **0 new b20c `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b20c authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the SDK concepts duplicate existing notes?) was
performed: `term_subagent`, `term_mcp`, `term_compaction`, `term_context_window`, `term_sandbox`,
`term_graduated_trust`, `term_regular_checkpointing`, `term_claude_code`, `term_guardrails`, `term_deny_first`,
`term_human_in_the_loop`, `term_hitl`, and the 5 design-pattern terms (observer/command/memento/WAL/pub-sub)
all exist → linked, not recreated. Dedup against `documentation/` confirmed no existing Claude Code SDK

## Term-Note Authoring Requirements

**N/A for b20c** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source (keep ONE representative language — Python — per `<CodeGroup>` pair;
  drop the parallel TypeScript block with a one-line "TS equivalent in the TypeScript SDK reference"
  pointer). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_regular_checkpointing.md` | notes 7, 8 | checkpointing term → CC SDK file-checkpointing concept + implementation |
| `term_dictionary/term_graduated_trust.md` | notes 5, 6 | permission-mode term → CC SDK permission evaluation + modes |
| `term_dictionary/term_guardrails.md` | notes 3, 5 | guardrails term → CC SDK hook block-patterns + deny rules |
| `term_dictionary/term_observer_pattern.md` | notes 1, 2 | observer-pattern term → CC SDK hook event model + registration |
| `term_dictionary/term_claude_code.md` | notes 1, 5, 8 | product term → CC SDK hooks/permissions/checkpointing surfaces |
| `term_dictionary/term_subagent.md` | notes 1, 4 | subagent term → CC SDK subagent hooks + subagent permission troubleshooting |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8
  rows for `entry_claude_code_docs.md` (Agent SDK cluster); `/tessellum-check-broken-links`.
- Once sibling SDK/Claude-Code sub-plans land (B05A permissions, B07A/B07B hooks, B19B sessions, B19C
  user-input, B21B/B21C language refs), upgrade the prose link-outs in these 8 notes to resolvable
  `cc_*`/sibling links and add reciprocal cross-links.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-13** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-13** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B20C, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/agent-sdk/`; measured words
  match the master's figures (hooks 4,541 · permissions 1,757 · file-checkpointing 3,327 = 9,625). H2/H3/H4
  structure extracted by grep and mapped 1:1 in the Section Coverage Map. Code-fence audit: hooks 26 pairs,
  checkpointing 21, permissions 5 — the binding constraint that forced the hooks 4-way and checkpointing
  2-way splits to respect ≤6 code/note. No >1.5× under-estimate; the master's 8-note estimate holds.
- **Notes**: 8 (concept 4, procedure 4) — matches master estimate. 3 splits documented.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard
  — 6-8 term notes per note (16 distinct `term_dictionary/` terms), each with a per-link what-it-is +
  positives discarded. Sibling/forward-ref link-outs (B05A/B07A/B07B/B19B/B19C/B21B/B21C) kept as prose.
- **Dedup-before-create (Step 2b)**: searched `term_dictionary/` AND `resources/documentation/` — no
  existing Claude Code SDK hooks/permissions/checkpointing note exists; `claude_code/` dir not yet created.
  All 8 `cc_` notes are new; no over-merge risk.
- **Step 2d new-term scan**: candidates (defer/elicitation/PostToolBatch/MessageDisplay/worktree-events)
  all route to existing notes/home sub-plans; **0 new b20c term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5 verification note, G7/G8 discoverability rows.
- **28-item checklist**: PASS (term-note items N/A — b20c authors no terms; entry-point + undigested-terms
  inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), including G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B20C contributes 8 rows under the Agent SDK cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body (`## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer) match the master Format Definition verbatim. |
| CP6 | Borderline density → split | ✅ PASS | hooks (4,541w/26 code) and file-checkpointing (3,327w/21 code) both split below caps; notes 3 & 8 hold exactly 6 code (representative language). No borderline note left un-split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w`: hooks 4,541 · permissions 1,757 · file-checkpointing 3,327 = 9,625 = master figure. H2/H3/H4 + code-fence counts grep-verified. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B20C authors 0 term notes; Undigested Terms Plan routes SDK vocabulary; Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (17 existing terms linked not recreated; documentation/ dedup confirmed no existing SDK hooks/permissions/checkpointing note). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
