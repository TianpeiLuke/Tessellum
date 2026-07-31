---
title: Sub-Plan B07A — Claude Code Docs: Hooks Reference
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["hooks"]
---

# Sub-Plan B07A: Hooks Reference

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The single but very large `hooks.md` reference page (21,959 measured words, 81 code blocks, 10 H2 / 54 H3 /
65 H4) — the complete reference for Claude Code's hook system: lifecycle, configuration schema, matcher
patterns, the five hook handler types (command/HTTP/MCP-tool/prompt/agent), JSON input/output, exit codes,
the 27-event catalog with per-event input + decision control, prompt-based and agent-based hooks, async
hooks, security, Windows PowerShell, and debugging. P1 (Phase A — a foundational core later sub-plans
reference). The companion **how-to / quickstart** material is owned by B07B (`hooks-guide.md`) and is
linked, never duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 1 page, 21,959 measured words. **Planned: 10 notes.**

## Content Strategy

- **Prioritize**: the cross-cutting mechanics every later sub-plan links — what a hook is, the five handler
  types, the matcher/`if` filter model, the JSON input/output + exit-code contract, and the event catalog.
- **Group**: the page is one giant reference, so the split is by *subsystem*, not by source H2 — (a) overview
  + config nesting, (b) the event catalog table, (c) matchers + handler-field schema, (d) command/HTTP/MCP-tool
  handler types, (e) input/output + exit codes + decision control, then the 27 events grouped into (f) tool-loop
  events and (g) session/turn/lifecycle events, plus (h) prompt+agent hooks, (i) async hooks, (j) security/debug.
- **Skip / link-out (own other sub-plans)**: the hooks *quickstart guide* (`hooks-guide.md`) → B07B; settings
  file resolution + `allowManagedHooksOnly` / `disableAllHooks` precedence → settings B03A; permission rule
  syntax → permissions B05A; MCP server connection → B08A; skills/subagent frontmatter → B06/B10A; plugin
  `hooks/hooks.json` → B09A; agent teams `TeammateIdle` semantics → B10A; worktree isolation → B10B;
  checkpointing → B02B; `--debug` / `/doctor` → B03B. Referenced via links, never duplicated.
- **Code**: the page is code-dense (81 blocks). Each note keeps ≤6 *representative* verbatim blocks; the rest
  are described in prose with a pointer to the source page, so no note breaches the ≤6-code cap.

## Source Pages (Measured 2026-06-13, re-read)

The page was re-read in full from `inbox/claude_code_docs/hooks.md` (verbatim mirror of
`code.claude.com/docs/en/hooks.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| hooks | /hooks | 21,959 | 81 | 10 | 54 | concept (mechanism) + procedure (config) + argument (security) |

> **H2 lists (document order):** Hook lifecycle · Configuration · Hook input and output · Hook events ·
> Prompt-based hooks · Agent-based hooks · Run hooks in the background · Security considerations ·
> Windows PowerShell tool · Debug hooks.
>
> **H3 lists (document order, grouped under their H2):**
> - **Hook lifecycle**: How a hook resolves
> - **Configuration**: Hook locations · Matcher patterns (H4 Match MCP tools) · Hook handler fields (H4 Common fields, Command hook fields [H5 Exec form and shell form], HTTP hook fields, MCP tool hook fields, Prompt and agent hook fields) · Reference scripts by path · Hooks in skills and agents · The `/hooks` menu · Disable or remove hooks
> - **Hook input and output**: Common input fields · Exit code output (H4 Exit code 2 behavior per event) · HTTP response handling · JSON output (H4 Emit terminal notifications, Add context for Claude, Decision control)
> - **Hook events** (27 events, each with `… input` and most with `… decision control`/`… output` H4): SessionStart (H4 input, decision control, Persist environment variables) · Setup · InstructionsLoaded · UserPromptSubmit · UserPromptExpansion · MessageDisplay · PreToolUse (H4 input, decision control, Defer a tool call for later) · PermissionRequest (H4 input, decision control, Permission update entries) · PostToolUse · PostToolUseFailure · PostToolBatch · PermissionDenied · Notification · SubagentStart · SubagentStop · TaskCreated · TaskCompleted · Stop · StopFailure · TeammateIdle · ConfigChange · CwdChanged · FileChanged · WorktreeCreate · WorktreeRemove · PreCompact · PostCompact · SessionEnd · Elicitation · ElicitationResult
> - **Prompt-based hooks**: How prompt-based hooks work · Prompt hook configuration · Response schema · Example: Multi-criteria Stop hook
> - **Agent-based hooks**: How agent hooks work · Agent hook configuration
> - **Run hooks in the background**: Configure an async hook · How async hooks execute · Example: run tests after file changes · Limitations
> - **Security considerations**: Disclaimer · Security best practices

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`,
target `resources/documentation/claude_code/`. **10 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_hooks_overview.md` | concept | Hook lifecycle (intro + How a hook resolves); Configuration (intro, 3-level nesting) | 550 | What hooks are (user-defined shell/HTTP/LLM handlers at lifecycle points); the three cadences (per-session/per-turn/per-tool-call); the 3-level config nesting (event → matcher group → handler); annotated `PreToolUse` resolution walkthrough; ≤4 code. Links B07B guide, `term_claude_code`. |
| 2 | `cc_hook_events_catalog.md` | concept | Hook lifecycle (event table); Matcher patterns (per-event matcher-field table); Prompt-based hooks (which events support which handler types) | 600 | The 27-event catalog: when each fires, its cadence, which field its matcher filters, and which of the 5 handler types it supports. The navigational index for notes 6–7. ≤1 code. |
| 3 | `cc_hook_matchers_and_filters.md` | procedure | Matcher patterns (incl. Match MCP tools); Hook handler fields → Common fields (`if`, Bash-if matching, `timeout`, `statusMessage`, `once`) | 600 | How to filter when hooks run: matcher evaluation (exact/`\|`-list/regex/match-all), per-event matched field, matching MCP `mcp__server__tool` names, the `if` permission-rule filter + Bash-subcommand matching table, common handler fields. ≤4 code. Links B05A permissions, B08A MCP. |
| 4 | `cc_hook_handler_types.md` | procedure | Hook handler fields (Command/HTTP/MCP-tool fields, Exec form and shell form); Reference scripts by path; Hooks in skills and agents; The `/hooks` menu; Disable or remove hooks | 750 | The 5 handler types and their type-specific fields: command (exec vs shell form, `args`/`shell`), HTTP (`url`/`headers`/`allowedEnvVars`), MCP-tool (`server`/`tool`/`input`); path placeholders (`CLAUDE_PROJECT_DIR`/`CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA`); defining hooks in skill/agent frontmatter; the read-only `/hooks` menu; disable/remove. ≤6 code. Links B06 skills, B09A plugins. |
| 5 | `cc_hook_io_and_exit_codes.md` | concept | Hook input and output (Common input fields, Exit code output incl. Exit-code-2-per-event, HTTP response handling, JSON output incl. terminal notifications, Add context for Claude, Decision control) | 750 | The full I/O contract: common stdin JSON fields (`session_id`/`cwd`/`permission_mode`/`effort`/…); exit-code semantics (0 success, 2 block, other non-blocking) + the per-event exit-2 table; HTTP status-code equivalents; JSON output universal fields (`continue`/`systemMessage`/`terminalSequence`); `additionalContext`; the decision-control field-pattern table. ≤6 code. Links `term_function_calling`. |
| 6 | `cc_hook_tool_loop_events.md` | concept | Hook events: PreToolUse (+Defer), PermissionRequest (+Permission update entries), PostToolUse, PostToolUseFailure, PostToolBatch, PermissionDenied | 800 | The agentic-loop (per-tool-call) events: input schemas + decision control for the 6 tool-cadence events — `permissionDecision` allow/deny/ask/defer, `updatedInput`/`updatedToolOutput` rewriting, permission-update entries, retry. ≤5 code. Links B05A permissions, `term_graduated_trust`, `term_deny_first`. |
| 7 | `cc_hook_session_lifecycle_events.md` | concept | Hook events: SessionStart (+Persist env vars), Setup, InstructionsLoaded, UserPromptSubmit, UserPromptExpansion, MessageDisplay, Notification, SubagentStart/Stop, TaskCreated/Completed, Stop, StopFailure, TeammateIdle, ConfigChange, CwdChanged, FileChanged, WorktreeCreate/Remove, PreCompact/PostCompact, SessionEnd, Elicitation/ElicitationResult | 850 | The session-, turn-, and non-tool lifecycle events: when each fires, input highlights, decision control (block/continue, `additionalContext`, `CLAUDE_ENV_FILE`, `reloadSkills`, `sessionTitle`, `displayContent`, worktree path, elicitation action). Grouped by cadence; per-event detail → source. ≤5 code. Links B02B sessions, B10A subagents, `term_compaction`. |
| 8 | `cc_prompt_and_agent_hooks.md` | concept | Prompt-based hooks (How it works, config, Response schema, Multi-criteria example); Agent-based hooks (How it works, config) | 600 | LLM-as-judge hooks: `type: "prompt"` (single-turn fast-model yes/no decision, `$ARGUMENTS`, `{ok, reason}` schema, `continueOnBlock`, per-event `ok:false` behavior) and `type: "agent"` (experimental subagent verifier with Read/Grep/Glob, up to 50 turns). ≤4 code. Links `term_llm_as_a_judge`, `term_agent_as_a_judge`. |
| 9 | `cc_async_hooks.md` | procedure | Run hooks in the background (Configure, How async hooks execute, Example, Limitations) | 450 | Background/async command hooks: `async: true` (command-only), `asyncRewake` exit-2 wake, output delivered next turn via `additionalContext`, no-deduplication + no-blocking limitations, timeout. ≤3 code. Links `term_observability_agent_systems`. |
| 10 | `cc_hook_security_and_debugging.md` | argument | Security considerations (Disclaimer, Best practices); Windows PowerShell tool; Debug hooks | 500 | Why hooks are a trust boundary (full user permissions) and how to operate them safely + observe them: validate/quote/block-traversal/skip-sensitive-files best practices, Windows `shell:"powershell"`, the debug log (`--debug-file`, `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose`). ≤3 code. Links `term_guardrails`, B07B troubleshooting. |

**Estimate: 10 notes** — concept ×6 (notes 1,2,5,6,7,8), procedure ×3 (notes 3,4,9), argument ×1 (note 10). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 1 (21,959 words — the largest single page in the corpus). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~6,450 (avg ~645/note). Code blocks: ~4 avg/note, ≤6 cap each (representative subset of the 81 source blocks; remainder described in prose).
- **Building Block Distribution**: concept ×6 (notes 1,2,5,6,7,8) · procedure ×3 (notes 3,4,9) · argument ×1 (note 10). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_hooks_overview` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Hooks are a Claude Code feature; this note is the entry point to Claude Code's hook subsystem, so the product term is its definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Hooks fire at lifecycle points the harness exposes (session/turn/tool-call); they are the harness's user-pluggable callback layer around the model loop.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The flagship hook example (`PreToolUse` blocking `rm -rf`) intercepts a tool call; hooks gate the tool-use mechanism this term defines.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Hooks are the deterministic-guardrail mechanism in Claude Code: shell/HTTP/LLM checks that run automatically to allow, block, or modify actions.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — A hook handler encapsulates a request (event JSON in, decision out) as a runnable object registered against a lifecycle point — the encapsulate-request-as-object intent the Command pattern describes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note frames hooks against the normal permission flow; a `PreToolUse` hook can deny but staying silent does not approve, tightening the progressive-trust permission model this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Hooks are how an autonomous coding agent is made safe and deterministic at scale — they enforce policy on the agent's autonomous tool calls without a human in every loop.

### 2. `cc_hook_events_catalog` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The catalog enumerates the 27 points in Claude Code's own session lifecycle where hooks fire, so it directly extends the Claude Code term.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Each catalog event is a callback site the harness exposes around its loop (session start, per-turn, per-tool-call, compaction), so the event list is a map of the harness's instrumentation points.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The largest event family (PreToolUse/PostToolUse/PostToolUseFailure/PermissionRequest/PostToolBatch) fires around tool calls and matches on `tool_name`, tying the catalog to the tool-use mechanism.
- [Subagent](../../term_dictionary/term_subagent.md) — `SubagentStart`/`SubagentStop` events fire when a subagent is spawned and finishes, and `Stop` hooks auto-convert to `SubagentStop` inside a subagent — catalog rows defined by the subagent concept.
- [Compaction](../../term_dictionary/term_compaction.md) — `PreCompact`/`PostCompact` are catalog events that fire around context compaction; the catalog's compaction matcher values (`manual`/`auto`) come straight from this term.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — `TeammateIdle`, `TaskCreated`, and `TaskCompleted` are catalog events from the agent-teams (multi-agent) execution model, where peer teammates coordinate over a shared task list.

### 3. `cc_hook_matchers_and_filters` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Matchers and the `if` field are Claude Code's hook-filtering syntax; the note documents that product behavior directly.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Tool-event matchers filter on `tool_name` and the `if` field matches against tool name + arguments together, so this filtering layer sits on top of the tool-use mechanism.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — MCP tools appear in matchers under the `mcp__<server>__<tool>` naming pattern — the stable per-tool name/identity the tool-descriptor contract assigns is exactly what regex matchers like `mcp__memory__.*` target.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The dedicated "Match MCP tools" subsection covers matching `mcp__server__tool` names with the required `.*` regex suffix, so MCP server-tool naming is central to the note.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — The note warns the `if` filter is best-effort and fails open, advising the permission system for hard allow/deny — i.e. use a deny-first permission rule, not a fail-open hook, to enforce policy.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The `if` field reuses permission-rule syntax (`Bash(git *)`, `Edit(*.ts)`) from Claude Code's progressive-trust permission model, so the matcher/filter layer borrows that term's vocabulary.

### 4. `cc_hook_handler_types` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The five handler types (command/HTTP/MCP-tool/prompt/agent) and the `/hooks` menu are Claude Code features the note documents.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Each handler object is a parameterized, registered command (command string + args, or URL, or server/tool) bound to a matcher — the encapsulate-and-parameterize-requests intent the Command pattern names.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The `mcp_tool` handler type calls a tool on an already-connected MCP server, and `${CLAUDE_PROJECT_DIR}` is also exported to stdio MCP servers, so MCP integration is a first-class handler type here.
- [REST](../../term_dictionary/term_rest.md) — The HTTP handler type POSTs the event JSON as a request body with `Content-Type: application/json` and reads a 2xx response body — a REST-style request/response integration the note specifies.
- [Skills](../../term_dictionary/term_skills.md) — Hooks can be declared in skill frontmatter (scoped to the skill's lifetime, with the `once` field only honored there), so the skill concept defines one of the handler-location scopes.
- [Subagent](../../term_dictionary/term_subagent.md) — Hooks can be declared in subagent frontmatter where `Stop` auto-converts to `SubagentStop`, making the subagent another component scope for handler definitions.

### 5. `cc_hook_io_and_exit_codes` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The stdin-JSON-in / exit-code-and-stdout-out contract is Claude Code's hook I/O protocol; the note specifies that product behavior.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The decision-control output (block/allow, `updatedInput`/`updatedToolOutput`) governs whether and how a tool call proceeds, hooking directly into the tool-use mechanism.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Exit code 2 + stderr is the canonical guardrail signal ("stop, don't do this"); the note's exit-code table is the deterministic enforcement contract guardrails rely on.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — The contract is deny-explicit, not deny-by-default: only exit 2 blocks and staying silent never approves, so the note's I/O semantics encode where deny-first does and does not apply.
- [Context Window](../../term_dictionary/term_context_window.md) — `additionalContext` injects a hook's output string into Claude's context window (capped at 10,000 chars, overflow spilled to a file), tying hook output to context-window management.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `additionalContext`, `systemMessage`, and the guidance to phrase context as factual statements (to avoid tripping prompt-injection defenses) are context-engineering decisions about what reaches the model and how.

### 6. `cc_hook_tool_loop_events` (7 term notes)
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Every event in this note (PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/Permission*) fires around a tool call and matches on `tool_name`, so they instrument the tool-use mechanism directly.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `PreToolUse.permissionDecision` (allow/deny/ask/defer) and `PermissionRequest.decision.behavior` (allow/deny) are how hooks participate in Claude Code's progressive-trust permission flow.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — These events are the deny-first enforcement points: a hook can deny a tool call before it runs (PreToolUse) or deny a permission (PermissionRequest), with silence never implying approval.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — `PreToolUse` "defer" and the deny/ask escalation let a hook gate irreversible tool calls (e.g. destructive Bash) more tightly than reversible ones — the reversibility-weighted approval threshold this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool-loop events are points in Claude Code's own agentic loop; the note documents that product behavior.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — These events are the harness's per-tool-call callback sites inside the agentic loop; `updatedInput`/`updatedToolOutput` let a hook rewrite what the harness passes to or returns from a tool.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Blocking a tool call, redacting its input at `PreToolUse`, or rewriting its output at `PostToolUse` are the deterministic guardrail patterns these events enable.

### 7. `cc_hook_session_lifecycle_events` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — These events span Claude Code's session, turn, instruction-load, and config lifecycle; the note documents that product behavior.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — SessionStart/Setup/Stop/SessionEnd and the `CLAUDE_ENV_FILE`/`reloadSkills`/`watchPaths` outputs are how a hook configures the harness's environment, skill discovery, and watch list around the loop.
- [Compaction](../../term_dictionary/term_compaction.md) — `PreCompact`/`PostCompact` fire around context compaction (`manual`/`auto` matchers), and `InstructionsLoaded` re-fires with `load_reason:"compact"` when instruction files reload after compaction.
- [Subagent](../../term_dictionary/term_subagent.md) — `SubagentStart`/`SubagentStop` fire as subagents spawn and finish, and Stop-decision-control `additionalContext` continues the subagent's turn — subagent-defined lifecycle events.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — `TeammateIdle`, `TaskCreated`, and `TaskCompleted` are the agent-teams (multi-agent) lifecycle events where exit-2 blocks a teammate going idle or a task transitioning.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `SessionStart`/`UserPromptSubmit`/`UserPromptExpansion` inject `additionalContext` and `initialUserMessage` to shape what enters the model's context at session/turn boundaries — context-engineering at lifecycle seams.
- [Context Window](../../term_dictionary/term_context_window.md) — `SessionStart` reloads context on resume, the compaction events bracket window-shrinking, and `additionalContext` adds to the window — all context-window-management touchpoints.

### 8. `cc_prompt_and_agent_hooks` (6 term notes)
- [LLM as a Judge](../../term_dictionary/term_llm_as_a_judge.md) — A `prompt` hook sends the hook input to a fast Claude model that returns a structured `{ok, reason}` allow/block decision — exactly the LLM-as-judge evaluation pattern this term defines.
- [Agent as a Judge](../../term_dictionary/term_agent_as_a_judge.md) — An `agent` hook spawns a subagent that uses Read/Grep/Glob over up to 50 turns to verify a condition before returning `{ok}` — the tool-using agent-as-judge generalization of the prompt judge.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Prompt and agent hooks are Claude Code handler types (`type:"prompt"`/`"agent"`); the note documents that product feature.
- [Subagent](../../term_dictionary/term_subagent.md) — The agent hook is implemented as a spawned subagent with multi-turn tool access, so the subagent concept is the execution model of an agent hook.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — The multi-criteria Stop-hook prompt asks the model to reason through completion/error/follow-up checks before emitting `{ok}` — a chain-of-thought evaluation step inside the hook.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Prompt/agent hooks are model-based guardrails (vs deterministic command hooks): they verify conditions like "all tests pass before Stop" and block on `ok:false`, complementing exit-code enforcement.

### 9. `cc_async_hooks` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — `async`/`asyncRewake` are Claude Code command-hook fields; the note documents that product behavior.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — Async hooks run long tests/deploys/API calls in the background and report results back via `additionalContext` on the next turn — a non-blocking observability/feedback channel into the agent.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Async hooks let the harness keep the model working while a background process runs, with `asyncRewake` exit-2 waking the loop on failure — a harness-level concurrency control.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The canonical async example runs a test suite after a `Write`/`Edit` tool call; async hooks fire around tool use but cannot block it since the call already completed.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Async output reaches the model only as `additionalContext` on the next turn (a `systemMessage` goes to the user, not Claude) — a deliberate choice about what background results enter the model's context.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The note's key constraint — async hooks cannot block tool calls or return decisions because the action already proceeded — is exactly why a guardrail that must enforce policy should be synchronous, not async.

### 10. `cc_hook_security_and_debugging` (6 term notes)
- [Guardrails](../../term_dictionary/term_guardrails.md) — Hooks are powerful guardrails that run with full user permissions; the note's security disclaimer and best practices are the safe-operation guidance for that guardrail mechanism.
- [Prompt Injection](../../term_dictionary/term_owasp_llm.md) — `additionalContext` text framed as out-of-band system commands can trip Claude's prompt-injection defenses; hook input must be validated/sanitized because untrusted tool data flows into a hook — OWASP-LLM prompt-injection risks the note guards against.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — The best-practices list (never trust input blindly, block `..` path traversal, skip `.env`/`.git`/keys) defends against adversarial inputs that try to weaponize a hook's full-permission shell.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The Windows `shell:"powershell"` field, the `/hooks` menu, and the `--debug-file`/`CLAUDE_CODE_DEBUG_LOG_LEVEL` debug log are Claude Code features the note documents.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — "Use the permission system rather than a hook to enforce a hard allow or deny" — the note steers enforcement to a deny-first permission model because the `if` filter fails open.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — The Debug hooks section (which hooks matched, exit codes, stdout/stderr to the debug log) is the observability surface for diagnosing hook behavior in an agent run.

## Section Coverage Map

Every source H2/H3/H4 maps to a note or an explicit link-out. Sections owned by other sub-plans are LINKED, not duplicated.

```
hooks.md
## Hook lifecycle ─────────────────────────────────── → note 1 (intro + cadences)
│   ├── (event table) ──────────────────────────────── → note 2 (cc_hook_events_catalog)
│   └── How a hook resolves (annotated walkthrough) ── → note 1 (cc_hooks_overview)
## Configuration ──────────────────────────────────── → note 1 (3-level nesting intro)
│   ├── Hook locations (scope table) ───────────────── → note 4 (handler scopes); settings precedence → B03A
│   ├── Matcher patterns ───────────────────────────── → note 3 (cc_hook_matchers_and_filters)
│   │   └── Match MCP tools ─────────────────────────── → note 3 (→ B08A MCP)
│   ├── Hook handler fields ─────────────────────────── → note 4 (intro: 5 types)
│   │   ├── Common fields (if, timeout, statusMessage, once, Bash-if) → note 3
│   │   ├── Command hook fields (+ Exec/shell form) ─── → note 4
│   │   ├── HTTP hook fields ────────────────────────── → note 4
│   │   ├── MCP tool hook fields ────────────────────── → note 4 (→ B08A)
│   │   └── Prompt and agent hook fields ────────────── → note 8 (cc_prompt_and_agent_hooks)
│   ├── Reference scripts by path (placeholders) ────── → note 4
│   ├── Hooks in skills and agents ──────────────────── → note 4 (→ B06 skills / B10A subagents)
│   ├── The /hooks menu ─────────────────────────────── → note 4
│   └── Disable or remove hooks ─────────────────────── → note 4 (disableAllHooks precedence → B03A settings)
## Hook input and output ──────────────────────────── → note 5 (cc_hook_io_and_exit_codes)
│   ├── Common input fields ─────────────────────────── → note 5
│   ├── Exit code output ────────────────────────────── → note 5
│   │   └── Exit code 2 behavior per event ──────────── → note 5
│   ├── HTTP response handling ──────────────────────── → note 5
│   └── JSON output ─────────────────────────────────── → note 5
│       ├── Emit terminal notifications ─────────────── → note 5
│       ├── Add context for Claude (additionalContext) → note 5 (static rules → B02B memory)
│       └── Decision control (field-pattern table) ──── → note 5
## Hook events ────────────────────────────────────── → notes 6 + 7 (intro in note 2)
│   ├── SessionStart (+input, decision, Persist env) ─ → note 7
│   ├── Setup ───────────────────────────────────────── → note 7
│   ├── InstructionsLoaded ──────────────────────────── → note 7 (CLAUDE.md → B02B memory)
│   ├── UserPromptSubmit ────────────────────────────── → note 7
│   ├── UserPromptExpansion ─────────────────────────── → note 7 (slash commands → B06)
│   ├── MessageDisplay ──────────────────────────────── → note 7
│   ├── PreToolUse (+input, decision, Defer) ────────── → note 6
│   ├── PermissionRequest (+input, decision, updates) ─ → note 6 (permission rules → B05A)
│   ├── PostToolUse ─────────────────────────────────── → note 6
│   ├── PostToolUseFailure ──────────────────────────── → note 6
│   ├── PostToolBatch ───────────────────────────────── → note 6
│   ├── PermissionDenied ────────────────────────────── → note 6 (auto-mode classifier → B05A)
│   ├── Notification ────────────────────────────────── → note 7
│   ├── SubagentStart / SubagentStop ────────────────── → note 7 (→ B10A subagents)
│   ├── TaskCreated / TaskCompleted ─────────────────── → note 7 (→ B10A agent teams)
│   ├── Stop / StopFailure ──────────────────────────── → note 7
│   ├── TeammateIdle ────────────────────────────────── → note 7 (agent teams → B10A)
│   ├── ConfigChange ────────────────────────────────── → note 7 (settings → B03A)
│   ├── CwdChanged ──────────────────────────────────── → note 7
│   ├── FileChanged ─────────────────────────────────── → note 7
│   ├── WorktreeCreate / WorktreeRemove ─────────────── → note 7 (worktree isolation → B10B)
│   ├── PreCompact / PostCompact ────────────────────── → note 7 (compaction → B02A)
│   ├── SessionEnd ──────────────────────────────────── → note 7
│   └── Elicitation / ElicitationResult ─────────────── → note 7 (MCP elicitation → B08A)
## Prompt-based hooks ─────────────────────────────── → note 8
│   ├── How prompt-based hooks work ─────────────────── → note 8
│   ├── Prompt hook configuration ───────────────────── → note 8
│   ├── Response schema ─────────────────────────────── → note 8
│   └── Example: Multi-criteria Stop hook ───────────── → note 8
## Agent-based hooks ──────────────────────────────── → note 8
│   ├── How agent hooks work ────────────────────────── → note 8
│   └── Agent hook configuration ────────────────────── → note 8
## Run hooks in the background ────────────────────── → note 9 (cc_async_hooks)
│   ├── Configure an async hook ─────────────────────── → note 9
│   ├── How async hooks execute ─────────────────────── → note 9
│   ├── Example: run tests after file changes ───────── → note 9
│   └── Limitations ─────────────────────────────────── → note 9
## Security considerations ────────────────────────── → note 10
│   ├── Disclaimer ──────────────────────────────────── → note 10
│   └── Security best practices ─────────────────────── → note 10
## Windows PowerShell tool ────────────────────────── → note 10
## Debug hooks ───────────────────────────────────── → note 10 (--debug / /doctor → B03B; troubleshooting → B07B)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| hooks.md (21,959w, 81 code — 8.8× the 2,500w cap and 13.5× the 6-code cap) | 10 notes | a single page far over every density cap; split by hook subsystem, not by source H2, so each note is BB-atomic |
| `## Hook events` (27 events, ~1,800w + many code) | notes 6 (6 tool-loop events) + 7 (21 session/turn/lifecycle events); index in note 2 | one BB-coherent group is the per-tool-call cadence (decision-heavy, permission-centric); the other is the session/turn/non-tool cadence; both reference the catalog (note 2) |
| `## Configuration` (matchers + 5 handler types + locations + menu) | notes 3 (matchers + filters = procedure) + 4 (handler types + locations + menu = procedure) | matcher/`if` filtering and handler-type schema are distinct procedures; keeping them together breached the code cap |
| `## Hook input and output` (input + exit codes + JSON output + decision control) | note 5 | kept whole as one concept (the I/O contract); ~750w + ≤6 representative code, within caps |
| Prompt-based + Agent-based hooks (two H2) | note 8 | both are LLM-judge handler types sharing the `{ok, reason}` schema; one coherent concept |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_hooks_overview | concept | 550 | 4 | ✅ |
| 2 | cc_hook_events_catalog | concept | 600 | 1 | ✅ |
| 3 | cc_hook_matchers_and_filters | procedure | 600 | 4 | ✅ |
| 4 | cc_hook_handler_types | procedure | 750 | 6 | ✅ |
| 5 | cc_hook_io_and_exit_codes | concept | 750 | 6 | ✅ |
| 6 | cc_hook_tool_loop_events | concept | 800 | 5 | ✅ |
| 7 | cc_hook_session_lifecycle_events | concept | 850 | 5 | ✅ |
| 8 | cc_prompt_and_agent_hooks | concept | 600 | 4 | ✅ |
| 9 | cc_async_hooks | procedure | 450 | 3 | ✅ |
| 10 | cc_hook_security_and_debugging | argument | 500 | 3 | ✅ |

No note exceeds the caps (≤2,500w / ≤6 code / ≤400 lines). Notes 4 and 5 sit at the 6-code cap by design — the executing agent keeps only the 6 most representative verbatim blocks and describes the remainder in prose with a source pointer. Notes 6 and 7 are the densest by word count (800/850) but stay well under 2,500 because per-event detail is summarized with a "full schema → source page" pointer rather than reproduced field-by-field.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_hooks_overview cc_hook_events_catalog cc_hook_matchers_and_filters cc_hook_handler_types cc_hook_io_and_exit_codes cc_hook_tool_loop_events cc_hook_session_lifecycle_events cc_prompt_and_agent_hooks cc_async_hooks cc_hook_security_and_debugging"
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

Single phase (10 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to `hooks.md`, no hallucinated fields/events | diff vs `inbox/claude_code_docs/hooks.md` |
| G3-Density+Coverage | caps met; every mapped H2/H3/H4 present or linked-out | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 10 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | post-reindex confirmation that in-degree ≥1 holds for all 10 notes after inlinks are written | `note_links` in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 10 rows** under a
"Hooks" cluster + increments the BB-distribution counts (concept ×6, procedure ×3, argument ×1). Parent hub
`entry_gen_ai_dev.md` is updated once at master finalization.

## Undigested Terms Plan (Step 4e)

b07a creates **0 new `term_dictionary` captures**. Per Pattern B (master), Claude Code vocabulary terms are
digested as `cc_*` doc concept notes by their home sub-plan; the only `term_dictionary` interaction is
**linking existing** terms. The hooks-specific vocabulary maps as follows:

| Hooks-page term | Disposition |
|---|---|
| Hook / hook event / matcher group / hook handler | owned by B07A `cc_*` notes (notes 1–10) — doc concepts, not term notes |
| Hook (master glossary term) | B07A is its home per master ("Hook→B07A/B07B") — digested as `cc_hooks_overview` |
| MCP / MCP tool | link `term_mcp` (exists) |
| Subagent | link `term_subagent` (exists) |
| Compaction | link `term_compaction` (exists) |
| Permission mode / permission rule | link `term_graduated_trust` (exists); permission-rule syntax owned by B05A |
| Context window / `additionalContext` | link `term_context_window` (exists) |
| Prompt-based hook / agent hook (LLM verifier) | folded into note 8; link `term_llm_as_a_judge` / `term_agent_as_a_judge` (exist) |
| Agent teams / teammate / task | events folded into note 7; link `term_multi_agent` (exists); team semantics owned by B10A |
| Worktree | event folded into note 7; worktree isolation owned by B10B |
| Skill / slash command | hook-in-frontmatter folded into note 4; owned by B06 |

**Augmentation Step 2d re-scan (2026-06-13):** re-read the full page scanning tables, code captions, and
emphasis for newly-surfaced non-glossary terms. Candidates considered and their disposition:
- **`CLAUDE_ENV_FILE` / `terminalSequence` / `additionalContext` / `asyncRewake`** — Claude-Code hook field/env-var
  names, not standalone vocabulary; documented inline in notes 5/7/9, **no term note**.
- **"prompt injection" / prompt-injection defenses** — surfaced in the `additionalContext` and Security sections;
  covered by existing **`term_owasp_llm`** (prompt injection is OWASP LLM01) + `term_adversarial_attack` (linked
  in note 10), **no new capture**.
- **"OSC escape sequence / terminal notification"** — terminal-protocol detail, not agent vocabulary; inline prose only.

**0 new B07A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B07A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the hooks concepts duplicate existing notes?) was
performed: `term_mcp`, `term_subagent`, `term_compaction`, `term_graduated_trust`, `term_context_window`,
`term_llm_as_a_judge`, `term_agent_as_a_judge`, `term_function_calling`, `term_guardrails`, `term_owasp_llm`,
`term_claude_code`, `term_agent_harness` all exist → linked, not recreated. No existing `cc_*` hook doc note
exists (folder is empty; B07A is the first hooks sub-plan), so no doc-note collision.

## Term-Note Authoring Requirements

**N/A for b07a** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read `hooks.md` before writing each note** — do NOT work from memory; the page is large and event
  schemas are easy to conflate.
- Code blocks **verbatim** from the source (this page is code-dense). One BB per note. Each note ≤6 code blocks
  (keep the most representative; describe the rest in prose with a source pointer). Each note ≤400 lines.
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase --autostash`
  first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 — each new note
receives ≥1 inbound link from outside `claude_code/`):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 2 | product term → CC hooks overview + event catalog |
| `term_dictionary/term_guardrails.md` | notes 1, 5, 10 | guardrails term → hooks as deterministic guardrails / I-O contract / security |
| `term_dictionary/term_graduated_trust.md` | note 6 | permission-mode term → tool-loop permission-decision events |
| `term_dictionary/term_llm_as_a_judge.md` | note 8 | LLM-judge term → prompt/agent hooks |
| `term_dictionary/term_observability_agent_systems.md` | note 9 | observability term → async hooks feedback channel |
| `term_dictionary/term_subagent.md` | note 7 | subagent term → SubagentStart/Stop lifecycle events |
| `term_dictionary/term_function_calling.md` | notes 3, 6 | tool-use term → matchers/filters + tool-loop events |

The sibling B07B (`hooks-guide.md`) notes, once they exist, will reciprocally link notes 1, 8, 9, 10 (guide ↔
reference); queued for B07B finalization.

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 10
  rows for `entry_claude_code_docs.md` under a "Hooks" cluster; `/tessellum-check-broken-links`.
- When B07B executes, add the guide↔reference reciprocal links.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-13** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B07A, 2026-06-13)

- **Source re-read (Step 2)**: `hooks.md` re-read in full from `inbox/claude_code_docs/`; measured 21,959 words
  = master figure (21,959). Confirmed 81 code blocks (162 fences / 2), 10 H2, 54 H3, 65 H4, and the 27-event
  catalog. The page is 8.8× the word cap and 13.5× the code cap, forcing a 10-way split (matches master estimate).
- **Notes**: 10 (concept 6, procedure 3, argument 1) — matches master estimate. Split is by hook *subsystem*,
  not source H2, so each note is BB-atomic; the 27 events split into tool-loop (note 6) vs session/lifecycle
  (note 7) with the catalog as the index (note 2).
- **Dedup (Step 2b/G-B)**: searched `documentation/claude_code/` (empty — B07A is the first hooks sub-plan) and
  `term_dictionary/`; no existing substantive hooks doc note. 0 doc-note collisions.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard via
  `term_xss`) discarded; `term_toolformer` dropped as too narrow in favor of `term_function_calling` +
  `term_tool_descriptor`.
- **Step 2d new-term scan**: 3 candidates considered (field/env-var names, prompt injection, OSC sequences) →
  prompt injection covered by existing `term_owasp_llm`/`term_adversarial_attack`; rest inline. **0 new captures.**
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts
  (bash), G7/G8 gate rows, Inlinks table, Undigested Terms Step-2d re-scan, this Augmentation Report.
- **28-item checklist**: PASS (term-note items N/A — B07A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed; set to `ready` after the 9/9 Review Sign-Off below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | ALL gates per batch (G1–G8 incl. G7/G8) | ✅ PASS | 8 gate rows present (single phase); G7 + G8 Discoverability (inbound in-degree ≥1) both included. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B07A contributes 10 rows under a Hooks cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes; overall is master + 40 sub-plans. |
| CP6 | Borderline density → split | ✅ PASS | All 10 notes 450–850w; notes 4/5 at the 6-code cap by design (representative-subset rule documented); notes 6/7 densest at 800/850w, still ≤2,500. None borderline-over. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w hooks.md` = 21,959 = master 21,959 (±0%); 81 code blocks and 27 events confirmed by grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements present | ✅ PASS (N/A scope) | B07A authors 0 term notes; Undigested Terms Plan routes hooks vocabulary (Pattern B); Authoring Requirements inherited. Step-2d re-scan documented → 0 new captures. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented — 12 existing terms linked not recreated; empty `claude_code/` folder → no doc-note collision. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
