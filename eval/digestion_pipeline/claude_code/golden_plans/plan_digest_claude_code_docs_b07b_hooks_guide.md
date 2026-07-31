---
title: Sub-Plan B07B — Claude Code Docs: Hooks Guide
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["hooks-guide"]
---

# Sub-Plan B07B: Hooks Guide

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The single `hooks-guide.md` page (`Automate actions with hooks`) — the **task-oriented guide** to Claude
Code hooks: how to set up a first hook, the seven common automation recipes, how hooks communicate
(events, types, stdin/stdout/exit codes, structured JSON, matchers, the `if` field), the three
non-command hook types (prompt / agent / HTTP), and limitations + troubleshooting. P1 (Phase A) — hooks
are a core extension layer that B05A (permissions), B06 (skills/commands), B09 (plugins), B10 (subagents/
teams), and B11 (automation) all reference. The companion `hooks.md` **reference** (full event schemas,
JSON I/O contracts, async/MCP-tool hooks) is owned by **B07A** and is *linked out*, never duplicated here.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 1 page, 6,580 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the lifecycle-event model + decision-control mechanics (exit codes, structured JSON,
  matchers, the `if` field, deny-precedence) that every downstream hook user must understand (P1).
- **Group**: split the page along its natural seams — setup (procedure) / recipes (procedure) / I/O +
  decision control (concept) / matchers + filtering (concept) / advanced non-command types (concept) /
  troubleshooting (procedure). The 7 recipes carry 14 code blocks, so they fan into 3 recipe notes to
  respect the ≤6-code-block cap; "How hooks work" is 2,783w (>2,500w cap), so it fans into an I/O note
  and a matchers note.
- **Skip / link-out (owned by B07A `hooks.md` reference)**: full event schemas (`#notification`,
  `#configchange`, `#cwdchanged`, `#filechanged`, `#pretooluse`, `#stopfailure`), JSON output contract,
  `exit-code-2-behavior-per-event`, `decision-control` summary table, async hooks, MCP-tool-hook fields,
  exec-form/shell-form, the `/hooks` menu reference page, `persist-environment-variables` /
  `CLAUDE_ENV_FILE` deep dive, `security-considerations`, `defer-a-tool-call-for-later`. These are
  referenced via links, never re-digested.
- **Skip / link-out (owned by other sub-plans)**: permission rules + modes → B05A
  (`permissions.md`/`permission-modes.md`); skills → B06 (`skills.md`); subagents/agent-teams → B10A;
  plugins → B09A; non-interactive/headless `-p` → B11 (`headless.md`); CLAUDE.md/memory → B02B
  (`memory.md`); env-vars (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) → B03A (`env-vars.md`).
- **Glossary**: no new `cc_` term-digest notes — hook vocabulary routes to existing term notes (link) or
  to B07A's reference notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

The page was re-read in full from `inbox/claude_code_docs/` (verbatim mirror of
`code.claude.com/docs/en/hooks-guide.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| hooks-guide | /hooks-guide | 6,580 | 30 | 8 | 18 | procedure/concept |

> **H2 lists (document order):**
> - **hooks-guide**: Set up your first hook · What you can automate (H3 Get notified when Claude needs input, Auto-format code after edits, Block edits to protected files, Re-inject context after compaction, Audit configuration changes, Reload environment when directory or files change, Auto-approve specific permission prompts) · How hooks work (H3 Combine results from multiple hooks, Read input and return output [H4 Hook input, Hook output, Structured JSON output], Filter hooks with matchers [H4 Filter by tool name and arguments with the `if` field], Configure hook location) · Prompt-based hooks · Agent-based hooks · HTTP hooks · Limitations and troubleshooting (H3 Limitations, Hooks and permission modes, Hook not firing, Hook error in output, `/hooks` shows no hooks configured, Stop hook hits the block cap, JSON validation failed, Debug techniques) · Learn more

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **8 notes** (master estimate was 4; density caps — ≤6 code
blocks and ≤2,500 words — force the documented splits below).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_hooks_overview_and_setup.md` | procedure | intro; Set up your first hook (Steps); Configure hook location; `/hooks` menu note | 550 | What hooks are (deterministic lifecycle shell commands; links `term_claude_code`); 3-step Notification walkthrough; scope/shareability table (user/project/local/managed/plugin/skill); `disableAllHooks`. Full menu/schema → `hooks.md` (B07A). |
| 2 | `cc_hooks_common_recipes.md` | procedure | What you can automate (intro + recipe index); Get notified when Claude needs input; Auto-format code after edits | 620 | Ready-to-use configs: cross-platform `Notification` (macOS/Linux/Windows) with the 6 matcher values; `PostToolUse`+`Edit\|Write` Prettier auto-format via `jq`. 5 code blocks. |
| 3 | `cc_hooks_guardrail_and_audit_recipes.md` | procedure | Block edits to protected files; Re-inject context after compaction; Audit configuration changes | 500 | `PreToolUse` exit-2 file-protection script; `SessionStart`+`compact` context re-injection; `ConfigChange` audit-log append. 5 code blocks. |
| 4 | `cc_hooks_environment_and_permission_recipes.md` | procedure | Reload environment when directory or files change; Auto-approve specific permission prompts | 700 | `SessionStart`+`CwdChanged`/`FileChanged` direnv reload via `CLAUDE_ENV_FILE`; `PermissionRequest` JSON auto-approve of `ExitPlanMode` with `setMode`; `bypassPermissions` caveat. 4 code blocks. |
| 5 | `cc_hooks_io_and_decision_control.md` | concept | How hooks work (events table + `type`); Combine results from multiple hooks; Read input and return output (Hook input, Hook output, Structured JSON output) | 1,500 | The lifecycle-event table (27 events); 5 hook `type`s; parallel-run + dedup; deny>defer>ask>allow merge; stdin JSON / stdout / stderr / exit-code contract (0/2/other); `permissionDecision` allow/deny/ask/defer; deny-rule precedence. Schema detail → `hooks.md` (B07A). |
| 6 | `cc_hooks_matchers_and_filtering.md` | concept | Filter hooks with matchers; Filter by tool name and arguments with the `if` field | 1,050 | Matcher semantics (empty=all, `Edit\|Write`, `mcp__.*`); per-event matcher field table; matcher examples (Bash log, MCP tools, SessionEnd `clear`); the `if` field (permission-rule syntax, subcommand/`$()` checking, fail-open, tool-events-only). |
| 7 | `cc_hooks_advanced_types.md` | concept | Prompt-based hooks; Agent-based hooks; HTTP hooks | 600 | The 3 non-command hook types: `prompt` (single-turn Haiku yes/no `ok`/`reason`); `agent` (experimental multi-turn subagent verify, 60s/50-turn); `http` (POST event JSON, `allowedEnvVars`). Full options → `hooks.md` (B07A). |
| 8 | `cc_hooks_troubleshooting.md` | procedure | Limitations and troubleshooting (Limitations, Hooks and permission modes, Hook not firing, Hook error in output, `/hooks` shows no hooks, Stop hook hits the block cap, JSON validation failed, Debug techniques) | 850 | Limitations (timeouts by type, PostToolUse can't undo, PermissionRequest not in `-p`); hooks-vs-permission-mode precedence; diagnosis recipes (not firing, hook error, no-hooks, Stop block cap + `stop_hook_active`, JSON-validation profile-echo bug, `--debug-file`/`Ctrl+O`). |

**Estimate: 8 notes** — procedure ×5 (notes 1,2,3,4,8), concept ×3 (notes 5,6,7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 1 (6,580 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~6,370 (avg ~796/note). Code blocks: ~32 across 8 notes (verbatim JSON/bash
  config from the source), ≤6 per note.
- **Building Block Distribution**: procedure ×5 (notes 1,2,3,4,8) · concept ×3 (notes 5,6,7). No
  model/argument/empirical_observation in this sub-plan (the page is how-to + mechanism, not advocacy).
- Cross-refs: **≥6 relevancy-selected term notes per note** (20 distinct `term_dictionary/` terms across
  (forward-refs) + entry-point back-link at finalization.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_hooks_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_hooks_overview_and_setup` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agentic coding tool whose lifecycle this note teaches you to hook into; hooks are configured in Claude Code's own settings files, so the product term is the host context.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Hooks are the harness-level extension point that fires user shell commands at points in the agent loop; this note frames hooks as deterministic harness wiring around the model.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — A hook fires on a platform-generated lifecycle signal (e.g. `Notification`, session start) — exactly the infrastructure-event-triggered-callback pattern this term defines for agent harnesses.
- [Skills](../../term_dictionary/term_skills.md) — The note's hook-location table lists skill frontmatter as one place hooks can be defined, and skills are the sibling extension layer hooks complement; the term grounds that row.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Hook scope (user / project / local / managed-policy) maps to the progressive-trust settings layering this term describes; managed-policy hooks are admin-enforced and cannot be overridden by a user.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — A configured hook encapsulates a request (a shell `command`) as a registerable, queueable object keyed to an event — the request-as-object design the Command pattern names.

### 2. `cc_hooks_common_recipes` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Every recipe is a ready-to-paste Claude Code settings block; the product term anchors what `~/.claude/settings.json` and the `Notification`/`PostToolUse` events belong to.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — The `Notification` recipe fires on lifecycle signals (`permission_prompt`, `idle_prompt`, `auth_success`) — the platform-generated, non-conversational events this term defines, handled by a callback.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — Auto-format-after-edit registers an observer (the Prettier command) that is notified whenever the `Edit`/`Write` subject changes state — the one-to-many notify-on-change dependency this pattern formalizes.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Each recipe wraps an operation (`osascript`, `prettier --write`) as a standalone command object bound to an event, the request-encapsulation this term describes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The recipes differ by where they live (`~/.claude` global vs `.claude` project), the trust-scope layering this term covers; a project hook is committable, a global one is machine-local.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Auto-formatting on every edit lets the agent keep coding without manual cleanup — the always-happens automation that supports unattended autonomous coding this term defines.

### 3. `cc_hooks_guardrail_and_audit_recipes` (7 term notes)
- [Guardrails](../../term_dictionary/term_guardrails.md) — The protect-files recipe is a runtime preventive safety control that intercepts and blocks edits to `.env`/`.git/` before they execute — precisely the policy-boundary enforcement this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — These recipes are Claude Code `PreToolUse`/`SessionStart`/`ConfigChange` settings blocks; the product term grounds the lifecycle hooks they register.
- [Compaction](../../term_dictionary/term_compaction.md) — The re-inject recipe uses a `SessionStart`+`compact` matcher to restore context lost when compaction summarizes the conversation — the context-summarization mechanism this term defines is the exact trigger.
- [Context Window](../../term_dictionary/term_context_window.md) — Re-injection writes critical project conventions back into the context window after compaction frees space; the term is the container the recipe refills.
- [Data Observability](../../term_dictionary/term_data_observability.md) — The audit-config recipe appends every configuration change to a log for compliance — the monitoring/logging-of-state-changes discipline this term covers.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — The protect-files script is a command object that can log requests and support a deny (exit 2) decision, the request-as-object behavior this pattern enables.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Blocking writes to protected paths and auditing config changes are trust-enforcement controls that constrain what the agent may do, the progressive-permission discipline this term describes.

### 4. `cc_hooks_environment_and_permission_recipes` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — These recipes register Claude Code `SessionStart`/`CwdChanged`/`FileChanged`/`PermissionRequest` hooks and use `CLAUDE_ENV_FILE`; the product term grounds those events and the env-file mechanism.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Auto-approving `ExitPlanMode` and switching the session to `acceptEdits`/`bypassPermissions` via `setMode` is exactly the staged permission-mode escalation this term defines.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — `CwdChanged` and `FileChanged` are platform-generated state-transition signals (directory change, file-on-disk change) that fire a callback — the lifecycle-event-triggered handling this term covers.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — `FileChanged` watches named files and notifies a reload command when they change on disk — the subject-notifies-observers-on-state-change dependency this pattern formalizes.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — The reload recipe manages the per-directory environment Claude's Bash tool runs in; environment isolation is the controlled-execution-context concern this term addresses.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Auto-approving routine prompts (plan exits) lets the agent proceed through long unattended runs without per-step approval — the autonomous-operation enablement this term defines.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The note's "keep the matcher as narrow as possible" warning is a guardrail caution: a broad auto-approve would disable the runtime safety controls this term defines.

### 5. `cc_hooks_io_and_decision_control` (8 term notes)
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — The note's core model is exactly EDA: lifecycle events are emitted by Claude Code (producer) and consumed by decoupled hook handlers (consumers) that react asynchronously — the event-flow-determines-control pattern this term defines.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — The note enumerates the 27-event lifecycle table (SessionStart, PreToolUse, Stop, etc.); each row is a platform-generated agent lifecycle event in the sense this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The events, hook `type`s, and the stdin-JSON/stdout/exit-code contract are all Claude Code's own mechanism; the product term is the host the I/O protocol belongs to.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — Multiple hooks subscribing to one event and all being notified in parallel when it fires is the one-to-many subject-to-observers dependency this pattern formalizes.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `PreToolUse`/`PostToolUse` hooks intercept the model's tool calls (with `tool_name`/`tool_input` on stdin) and can allow/deny them — they hook the function-calling/tool-use loop this term defines.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The exit-2 / `permissionDecision: deny` path is a runtime guardrail that cancels a tool call and feeds a reason back to the model — the intercept-and-block enforcement this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The deny>defer>ask>allow merge order and "deny rules always take precedence over hook approvals" are the layered permission-precedence rules this term describes; a hook can tighten but not loosen trust.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Each hook is a command object whose execution returns a structured decision (allow/deny/block), the request-as-object-with-result design this pattern names.

### 6. `cc_hooks_matchers_and_filtering` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Matchers and the `if` field are Claude Code settings-file constructs scoping which tool/event a hook fires on; the product term grounds the configuration surface.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Matchers filter by tool name (`Bash`, `Edit|Write`, `mcp__.*`) and the `if` field filters by tool name AND arguments — both operate on the function-calling/tool-use events this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note's MCP-tools tab shows matching `mcp__<server>__<tool>` names with regex (`mcp__github__.*`); MCP tools use this distinct naming convention the term defines.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — Matchers are the event-routing filter that decides which consumer (hook group) reacts to which event occurrence — the consumer-side filtering of an event-driven system this term describes.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The note warns the `if` filter "fails open" and is best-effort, so a hard allow/deny must use the permission system not a hook — the defense-in-depth distinction this term draws between policy enforcement and convenience filtering.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The `if` field reuses permission-rule syntax (`Bash(git *)`, `Edit(*.ts)`) to scope hooks, tying matcher filtering to the permission-rule trust model this term covers.

### 7. `cc_hooks_advanced_types` (7 term notes)
- [LLM as a Judge](../../term_dictionary/term_llm_as_a_judge.md) — A `prompt` hook sends the hook input to a Claude model (Haiku) for a single-pass yes/no `ok`/`reason` decision — precisely the LLM-as-a-judge evaluation methodology this term defines.
- [Agent as a Judge](../../term_dictionary/term_agent_as_a_judge.md) — An `agent` hook spawns a subagent that reads files, runs commands, and uses tools to verify a condition before returning `ok`/`reason` — the multi-step tool-augmented agentic-judge paradigm this term defines, extending LLM-as-a-Judge.
- [Subagent](../../term_dictionary/term_subagent.md) — The `agent` hook type literally spawns a subagent (60s / up-to-50-turn) to verify state; the term defines the isolated-context worker this hook type runs.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Prompt, agent, and HTTP are Claude Code hook `type`s configured in its settings; the product term grounds the mechanism.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Prompt/agent hooks are judgment-based runtime controls that can block an action (Stop/PreToolUse) when a model decides a condition fails — secondary-model guardrails the term explicitly lists.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — An HTTP hook POSTs event data to an external endpoint that reacts and returns a decision — a decoupled producer-to-remote-consumer event flow this term defines.
- [Data Observability](../../term_dictionary/term_data_observability.md) — The HTTP-hook example is a shared audit service logging tool-use events across a team — the centralized monitoring/observability use this term covers.

### 8. `cc_hooks_troubleshooting` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The failure modes (hook not firing, `/hooks` empty, Stop block cap, JSON-validation profile bug) are all Claude Code hook-execution issues; the product term grounds the `--debug-file`/`Ctrl+O`/`/debug` diagnostics.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — The debug-log + transcript-view techniques (which hooks matched, exit codes, stdout/stderr) are the trace-every-execution-step practice this term defines for diagnosing agent failures.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The "Hooks and permission modes" subsection explains a deny hook fires before any permission check and overrides `bypassPermissions` — the permission-mode precedence this term describes.
- [Guardrails](../../term_dictionary/term_guardrails.md) — The note documents that hooks can tighten but not loosen restrictions (deny rules always win) — the layered runtime-enforcement guarantee this term defines.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — Several failure modes turn on triggering the right lifecycle event (PreToolUse vs PostToolUse, Stop firing on every response not task completion) — the lifecycle-signal semantics this term covers.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Debug recipes test a hook by piping sample JSON to the script and checking its exit code — exercising the hook as a standalone command object the way this pattern intends.

## Section Coverage Map

```
hooks-guide.md
├── (intro: what hooks are, prompt/agent forecast, see-also) → note 1 (cc_hooks_overview_and_setup)
├── Set up your first hook (Steps: add/verify/test) ────────── → note 1
├── What you can automate (intro + recipe index) ──────────── → note 2 (cc_hooks_common_recipes)
│   ├── Get notified when Claude needs input ──────────────── → note 2
│   ├── Auto-format code after edits ──────────────────────── → note 2
│   ├── Block edits to protected files ────────────────────── → note 3 (cc_hooks_guardrail_and_audit_recipes)
│   ├── Re-inject context after compaction ────────────────── → note 3
│   ├── Audit configuration changes ───────────────────────── → note 3
│   ├── Reload environment when directory or files change ─── → note 4 (cc_hooks_environment_and_permission_recipes)
│   └── Auto-approve specific permission prompts ──────────── → note 4
├── How hooks work (events table + type field) ───────────── → note 5 (cc_hooks_io_and_decision_control)
│   ├── Combine results from multiple hooks ───────────────── → note 5
│   ├── Read input and return output (input/output/JSON) ──── → note 5
│   ├── Filter hooks with matchers ────────────────────────── → note 6 (cc_hooks_matchers_and_filtering)
│   │   └── Filter by tool name and arguments (`if` field) ── → note 6
│   └── Configure hook location (scope table) ─────────────── → note 1
├── Prompt-based hooks ────────────────────────────────────── → note 7 (cc_hooks_advanced_types)
├── Agent-based hooks ─────────────────────────────────────── → note 7
├── HTTP hooks ────────────────────────────────────────────── → note 7
├── Limitations and troubleshooting ──────────────────────── → note 8 (cc_hooks_troubleshooting)
│   ├── Limitations ───────────────────────────────────────── → note 8
│   ├── Hooks and permission modes ────────────────────────── → note 8
│   ├── Hook not firing / Hook error / no hooks ───────────── → note 8
│   ├── Stop hook hits the block cap ──────────────────────── → note 8
│   ├── JSON validation failed ────────────────────────────── → note 8
│   └── Debug techniques ──────────────────────────────────── → note 8
└── Learn more (cards) ───────────────────────────────────── → notes 1/8 (links → hooks.md B07A, security B16)
```

Inline cross-page references that **link out** (owned elsewhere, not duplicated):
`#hook-lifecycle`, `#notification`, `#configchange`, `#cwdchanged`, `#filechanged`, `#pretooluse`,
`#stopfailure`, `#decision-control`, `#json-output`, `#common-input-fields`,
`#exit-code-2-behavior-per-event`, `#mcp-tool-hook-fields`, `#exec-form-and-shell-form`,
`#persist-environment-variables`, `#defer-a-tool-call-for-later`, `#security-considerations`,
`#prompt-based-hooks`, `#agent-based-hooks`, `#http-hook-fields`, `the-/hooks-menu`, `#debug-hooks`
→ **B07A** `hooks.md`. `/en/permissions`, `#manage-permissions`, `#managed-settings` → **B05A**.
`/en/skills` → B06. `/en/sub-agents` → B10A. `/en/plugins` → B09A. `/en/memory` → B02B.
`/en/headless` → B11. `/en/env-vars` (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) → B03A. `/en/agent-teams` → B10A.
`/en/security-guidance` → B16. Bash-validator example URL → external `## References`.

No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| What you can automate (1,723w, 7 recipes, **14 code blocks** > 6 cap) | notes 2, 3, 4 | code-block cap: notify(4)+format(1)=5 → note 2; block(3)+reinject(1)+audit(1)=5 → note 3; reload(2)+approve(2)=4 → note 4. Grouped by theme (common / guardrail+audit / environment+permission). |
| How hooks work (2,783w **> 2,500w cap**, 12 code blocks) | notes 5, 6 (+ Configure-location → note 1) | word cap: I/O + decision-control (events table, type, combine, stdin/stdout/exit, structured JSON ≈1,540w / ~5 blocks) split from matchers + `if` field (≈1,074w / ~6 blocks); Configure-hook-location is setup → folded into note 1. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_hooks_overview_and_setup | procedure | 550 | 2 | ✅ |
| 2 | cc_hooks_common_recipes | procedure | 620 | 5 | ✅ |
| 3 | cc_hooks_guardrail_and_audit_recipes | procedure | 500 | 5 | ✅ |
| 4 | cc_hooks_environment_and_permission_recipes | procedure | 700 | 4 | ✅ |
| 5 | cc_hooks_io_and_decision_control | concept | 1,500 | 5 | ✅ |
| 6 | cc_hooks_matchers_and_filtering | concept | 1,050 | 6 | ✅ |
| 7 | cc_hooks_advanced_types | concept | 600 | 3 | ✅ |
| 8 | cc_hooks_troubleshooting | procedure | 850 | 4 | ✅ |

No note exceeds the caps (≤2,500w / ≤6 code blocks / ≤400 lines). Note 6 is at the 6-code-block ceiling
(matcher example + 3 tab examples + `if` example + `if`-syntax recap) — held at exactly 6, not over. No
over-compression: every H2/H3/H4 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_hooks_overview_and_setup cc_hooks_common_recipes cc_hooks_guardrail_and_audit_recipes cc_hooks_environment_and_permission_recipes cc_hooks_io_and_decision_control cc_hooks_matchers_and_filtering cc_hooks_advanced_types cc_hooks_troubleshooting"
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

Single phase (8 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to `hooks-guide.md`, no hallucination, code verbatim | diff vs `inbox/claude_code_docs/hooks-guide.md` |
| G3-Density+Coverage | caps met; every mapped H2/H3/H4 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (sibling) | the 8 notes are interlinked + reachable from `entry_claude_code_docs.md` (no intra-cluster island) | DB in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md` (created as a pre-step before the first sub-plan executes);
this sub-plan **contributes its 8 rows** under a "Hooks" cluster + increments the BB-distribution counts
(procedure +5, concept +3). The entry-point back-link is added to each note at finalization (G7/G8).

## Undigested Terms Plan (Step 2d)

B07B creates **0 new `term_dictionary` captures** — hook vocabulary is either (a) digested as a `cc_`
doc-concept note here, (b) owned by B07A's `hooks.md` reference, or (c) covered by an existing substantive
term note (link), per Pattern B. **Dedup performed across both `term_dictionary/` AND
`resources/documentation/`** (master Dedup Policy).

**Step 2d new-term scan (2026-06-13):** re-read all of `hooks-guide.md` scanning emphasis, the events
table, matcher tables, and code captions for newly-surfaced terms. Hook-specific vocabulary surfaced:

| Term surfaced | Disposition |
|---|---|
| Hook / hook event / hook type | digested as `cc_hooks_*` doc-concept notes (notes 1,5,7); **no** `term_dictionary` note (subject of doc pages, Pattern B) |
| Lifecycle event (SessionStart, PreToolUse, PostToolUse, Stop, …) | concept note 5 `cc_hooks_io_and_decision_control` + link `term_agent_lifecycle_event` (exists) |
| Matcher / `if` field | concept note 6 `cc_hooks_matchers_and_filtering` (doc concept) |
| Structured JSON output / `permissionDecision` / exit codes | concept note 5 (doc concept) |
| Prompt-based hook | note 7 + link `term_llm_as_a_judge` (exists) |
| Agent-based hook | note 7 + link `term_agent_as_a_judge` / `term_subagent` (exist) |
| HTTP hook / MCP-tool hook | note 7 (HTTP) / link-out to B07A (MCP-tool hook) |
| `CLAUDE_ENV_FILE`, `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`, `CLAUDE_PROJECT_DIR` | env-vars — owned by **B03A** (`env-vars.md`), link-out; not captured here |
| Permission mode / permission rule (`bypassPermissions`, `acceptEdits`, deny rules) | owned by **B05A** (`permissions.md`/`permission-modes.md`), link-out; link `term_graduated_trust` (exists) |
| Compaction / context window | existing term notes (link `term_compaction`, `term_context_window`) |
| Plugin / skill / agent-team / direnv | owned by B09A / B06 / B10A (link-out); direnv is an external tool → external `## References` |

**Collision dedup audit (master + Step 10.5f):** none of the surfaced concepts warrants a *new* term
note — `term_agent_lifecycle_event`, `term_llm_as_a_judge`, `term_agent_as_a_judge`, `term_subagent`,
`term_graduated_trust`, `term_compaction`, `term_context_window`, `term_guardrails`,
`term_event_driven_architecture`, `term_command_pattern`, `term_observer_pattern` all exist → linked,
not recreated. The `cc_hooks_*` doc notes do not duplicate any existing *doc* note (filename grep of
`resources/documentation/` for `*hook*` returned only `snippet_*`/`repo_*` code notes about unrelated
agent-harness shell hooks, a different sense). **0 new `term_dictionary` captures.**

## Term-Note Authoring Requirements

**N/A for B07B** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read `hooks-guide.md` before writing each note** — do NOT work from memory.
- **Code blocks verbatim** — JSON/bash config copied character-for-character from the source (this page
  is config-heavy; a paraphrased hook config is wrong). One BB per note. Each note ≤400 lines (split if
  a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase
  --autostash` first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | note 1 (`cc_hooks_overview_and_setup`) | product term → hooks extension overview |
| `term_dictionary/term_agent_lifecycle_event.md` | note 5 (`cc_hooks_io_and_decision_control`) | lifecycle-event term → CC hook event table |
| `term_dictionary/term_guardrails.md` | note 3 (`cc_hooks_guardrail_and_audit_recipes`) | guardrails term → hook-based file protection |
| `term_dictionary/term_llm_as_a_judge.md` | note 7 (`cc_hooks_advanced_types`) | judge term → prompt-based hook |
| `term_dictionary/term_graduated_trust.md` | note 4 (`cc_hooks_environment_and_permission_recipes`) | permission-mode term → auto-approve hook |
| `term_dictionary/term_event_driven_architecture.md` | note 5 | EDA term → CC event-driven hook model |
| `0_entry_points/entry_claude_code_docs.md` | notes 1–8 (Hooks cluster rows) | series entry point → all 8 hook notes (created pre-step) |

(Notes 2, 6, 8 also receive sibling inbound links from notes 1/5/7 within the cluster — counts toward G8;
G7 is satisfied by the out-of-folder term-note and entry-point inlinks above.)

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the
  8 rows for `entry_claude_code_docs.md` under a "Hooks" cluster; `/tessellum-check-broken-links`.
- Once **B07A** (`hooks.md` reference) executes, add reciprocal links between the B07B guide notes and the
  B07A reference notes (guide → reference for schemas; reference → guide for recipes).
- Verify DB in-degree ≥1 for each of the 8 notes (G7/G8) before marking the sub-plan complete.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B07B, 2026-06-13)

- **Source re-read (Step 2)**: `hooks-guide.md` re-read in full from `inbox/claude_code_docs/`; measured
  6,580 words = master's figure (±0%). Per-section word/code-block counts measured precisely (Set up 337w;
  recipes 1,723w/14 code blocks; How hooks work 2,783w/12 code blocks; prompt+agent+http 608w/3 blocks;
  troubleshooting 889w/~4 blocks). The 1.5× density rule fired twice → two documented re-splits.
- **Notes**: 8 (procedure 5, concept 3) — **exceeds the master's estimate of 4 because density caps force
  it**: recipes carry 14 code blocks (>6 cap) → 3 recipe notes; "How hooks work" is 2,783w (>2,500w cap)
  → 2 notes. Both splits documented in Split Decisions. (Master estimate updated implicitly; final count
  locks here per the pipeline.)
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–8 term notes per note (20 distinct `term_dictionary/` terms), each with a per-link relevancy
  statement; candidates sourced from BM25 + dense top-20 then filtered to genuinely-relevant terms;
  and B07A forward-refs kept as prose / link-outs.
- **Step 2d new-term scan**: hook vocabulary surfaced (events, matcher, `if`, prompt/agent/http hooks,
  env-vars) → all routed to a `cc_hooks_*` doc note, an existing term note (link), or another sub-plan
  (B03A/B05A/B06/B07A/B09A/B10A); **0 new B07B term captures**.
- **Dedup**: ran across `term_dictionary/` AND `resources/documentation/` (master Dedup Policy). No `cc_`
  hook doc note duplicates an existing doc note; the `*hook*` filename hits in `resources/documentation/`
  / `code_snippets/` are unrelated agent-harness shell-hook code (different sense). All 11 candidate hook
  concepts collide with existing substantive term notes → linked, not recreated.
- **Sections added during augment**: Content Strategy, Source Pages (measured), Summary Statistics & BB
  Distribution, Validation Scripts (bash), G5 verification note, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B07B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented → reviewed below; review sets `status: ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7 + G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B07B contributes 8 rows under a "Hooks" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer convention (master Format Definition, verbatim). |
| CP6 | Borderline density → split | ✅ PASS | Two over-cap sections split (recipes 14 code blocks → 3 notes; How-hooks-work 2,783w → 2 notes). Note 6 held at exactly the 6-code-block ceiling, not over. No remaining borderline note. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w hooks-guide.md` = 6,580 = plan 6,580. Per-section counts measured by script (recipes 1,723w/14cb; How-hooks-work 2,783w/12cb). Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B07B authors 0 term notes; Undigested Terms Plan routes all hook vocabulary (Step 2d scan); Authoring Requirements inherited from master. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (11 existing terms linked not recreated; `cc_hooks_*` doc notes do not duplicate any existing doc note; dedup spanned `term_dictionary/` AND `documentation/`). |
| CP9 | Building-block atomicity (one BB/note) | ✅ PASS | Each of the 8 notes is single-BB (procedure ×5, concept ×3); no mixed-BB note; recipes (procedure) cleanly separated from mechanism (concept). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
