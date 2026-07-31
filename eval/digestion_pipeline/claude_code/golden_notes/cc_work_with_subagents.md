---
tags:
  - resource
  - documentation
  - claude_code
  - subagents
  - delegation
keywords:
  - work with subagents
  - automatic delegation
  - invoke subagents explicitly
  - foreground background subagents
  - chain subagents
  - nested subagents
  - manage subagent context
  - auto-compaction
topics:
  - Claude Code
  - Subagents
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sub-agents
access_control_group: ["general"]
---

# Working With Subagents

## Overview

Once a subagent is defined, the day-to-day question is *how it gets invoked and how its context is managed*. Claude can **delegate automatically** based on task and `description`, or you can **invoke a subagent explicitly** through three escalating patterns (natural language, @-mention, session-wide `--agent`). Subagents run in the **foreground** (blocking, prompts passed through) or **background** (concurrent, auto-deny prompts), compose into **isolate / parallel-research / chain** patterns, and can **spawn nested subagents** up to a fixed depth limit.

Each subagent starts with a **fresh, isolated context window** — it does not see the main conversation history — and its transcript persists in a separate file so it survives main-conversation compaction and can be resumed. This note covers the delegation, invocation, foreground/background, common-pattern, subagent-vs-main-conversation, nesting, and context-management mechanics. Creating and configuring subagents is covered separately ([cc_create_a_subagent.md](cc_create_a_subagent.md), [cc_subagent_configuration_reference.md](cc_subagent_configuration_reference.md)); forks are covered in the [Fork the current conversation](https://code.claude.com/docs/en/sub-agents) section of the source page.

## Understand Automatic Delegation

Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like "use proactively" in your subagent's description field.

## Invoke Subagents Explicitly

When automatic delegation isn't enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

- **Natural language**: name the subagent in your prompt; Claude decides whether to delegate. There's no special syntax (e.g. "Use the test-runner subagent to fix failing tests").
- **@-mention**: guarantees the subagent runs for one task. Type `@` and pick the subagent from the typeahead, the same way you @-mention files. Your full message still goes to Claude, which writes the subagent's task prompt — the @-mention controls *which* subagent Claude invokes, not what prompt it receives. You can also type the mention manually: `@agent-<name>` for local subagents, or `@agent-` followed by the scoped name for plugin subagents. Named background subagents currently running in the session also appear in the typeahead with their status.
- **Session-wide**: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting.

```bash theme={null}
claude --agent code-reviewer
```

The subagent's system prompt replaces the default Claude Code system prompt entirely. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header, the choice persists when you resume the session, and this works with both built-in and custom subagents. The CLI flag overrides the `agent` setting if both are present. For plugin agents with name collisions, pass the scoped name (`my-plugin:security-reviewer`).

## Run Subagents in Foreground or Background

Subagents can run in the foreground (blocking) or background (concurrent):

- **Foreground subagents** block the main conversation until complete. Permission prompts are passed through to you as they come up.
- **Background subagents** run concurrently while you continue working. They run with the permissions already granted in the session and **auto-deny** any tool call that would otherwise prompt. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

If a background subagent fails due to missing permissions, you can start a new foreground subagent with the same task to retry with interactive prompts. Claude decides foreground vs. background based on the task; you can also ask Claude to "run this in the background" or press **Ctrl+B** to background a running task. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` to disable all background task functionality. When `CLAUDE_CODE_FORK_SUBAGENT=1`, every subagent spawn runs in the background regardless of the `background` field (see the [Fork the current conversation](https://code.claude.com/docs/en/sub-agents) section of the source page).

## Common Patterns

- **Isolate high-volume operations** — one of the most effective uses: delegate operations that produce large amounts of output (running tests, fetching documentation, processing log files) so the verbose output stays in the subagent's context while only the relevant summary returns. Example prompt: "Use a subagent to run the test suite and report only the failing tests with their error messages."
- **Run parallel research** — for independent investigations, spawn multiple subagents to work simultaneously ("Research the authentication, database, and API modules in parallel using separate subagents"). Each explores its area independently, then Claude synthesizes the findings. This works best when research paths don't depend on each other. Running many subagents that each return detailed results can itself consume significant context; for sustained parallelism or work exceeding the context window, [agent teams](https://code.claude.com/docs/en/agent-teams) give each worker its own independent context.
- **Chain subagents** — for multi-step workflows, ask Claude to use subagents in sequence. Each completes its task and returns results to Claude, which then passes relevant context to the next ("Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them").

## Choose Between Subagents and the Main Conversation

Use the **main conversation** when: the task needs frequent back-and-forth or iterative refinement; multiple phases share significant context (planning → implementation → testing); you're making a quick, targeted change; or latency matters (subagents start fresh and may need time to gather context).

Use **subagents** when: the task produces verbose output you don't need in your main context; you want to enforce specific tool restrictions or permissions; or the work is self-contained and can return a summary.

Consider [Skills](https://code.claude.com/docs/en/skills) instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context. For a quick question about something already in your conversation, use `/btw` instead of a subagent — it sees your full context but has no tool access, and the answer is discarded rather than added to history.

## Spawn Nested Subagents

As of Claude Code v2.1.172, a subagent can spawn its own subagents. Use this when a delegated task itself splits into parallel subtasks (such as a reviewer subagent that dispatches a verifier per finding), so the intermediate output never reaches your main conversation — only the top-level subagent's summary returns. A nested subagent is configured the same way as a top-level one and resolves from the same scopes. The subagent panel below the prompt input shows the full tree: each row displays a `(+N)` count of descendants, and opening a row shows that subagent's direct children with a path back to `main`.

Depth is the number of subagent levels below the main conversation, regardless of foreground/background:

- **Foreground subagents** can spawn at any depth. Each level blocks its parent until it returns, so the chain is self-limiting.
- **Background subagents**: a background subagent at depth five does not receive the Agent tool and cannot spawn further. The limit is fixed and not configurable, and exists to prevent runaway concurrent trees.

To prevent a specific subagent from spawning others, omit `Agent` from its `tools` list or add it to `disallowedTools`. A [fork](https://code.claude.com/docs/en/sub-agents) still cannot spawn another fork, but can spawn other subagent types (which count toward the depth limit).

## Manage Subagent Context

### What Loads at Startup

Each subagent starts with a fresh, isolated context window. It does not see your conversation history, the skills you've already invoked, or the files Claude has already read. Claude composes a delegation message summarizing the task. A non-fork subagent's initial context contains:

- **System prompt**: the agent's own prompt plus environment details Claude Code appends, not the full Claude Code system prompt.
- **Task message**: the delegation prompt Claude writes when it hands off the work.
- **CLAUDE.md and memory**: every level of the memory hierarchy the main conversation loads (`~/.claude/CLAUDE.md`, project rules, `CLAUDE.local.md`, managed policy files). The built-in Explore and Plan agents skip this.
- **Git status**: a snapshot taken at the start of the parent session; absent when not a Git repo or when `includeGitInstructions` is `false`. Explore and Plan skip it regardless.
- **Preloaded skills**: full content of any skill named in the agent's `skills` field. Built-in agents don't preload skills.

Explore and Plan are the only subagents that omit CLAUDE.md and git status, and there is no setting to change which agents skip them. The main conversation reads Explore/Plan results with full CLAUDE.md context, so most rules don't need to reach the subagent itself; if a rule must (such as "ignore the `vendor/` directory"), restate it in the prompt you give Claude when delegating.

### Resume Subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent's work, ask Claude to resume it — resumed subagents retain their full conversation history (all previous tool calls, results, and reasoning) and pick up exactly where they stopped. The built-in Explore and Plan agents are one-shot and return no agent ID, so they can't be resumed; use `general-purpose` or a custom subagent. Claude resumes via the `SendMessage` tool with the agent's ID as the `to` field — that tool is only available when agent teams are enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). If a stopped subagent receives a `SendMessage`, it auto-resumes in the background without a new `Agent` invocation. Transcripts live at `~/.claude/projects/{project}/{sessionId}/subagents/`, each stored as `agent-{agentId}.jsonl`.

Subagent transcripts persist independently of the main conversation: when the main conversation compacts, subagent transcripts are unaffected (stored in separate files); transcripts persist within their session so you can resume after restarting Claude Code by resuming the same session; and automatic cleanup follows the `cleanupPeriodDays` setting (default: 30 days).

### Auto-Compaction

Subagents support automatic compaction using the same logic as the main conversation. Compaction triggers under the same conditions, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` applies to subagents as well. Compaction events are logged in subagent transcript files as a `compact_boundary` system entry whose `compactMetadata.preTokens` value shows how many tokens were used before compaction occurred.

**Source**: https://code.claude.com/docs/en/sub-agents
**Last Updated**: 2026-06-13
**Status**: Active
