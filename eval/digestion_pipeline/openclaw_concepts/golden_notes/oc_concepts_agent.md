---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_runtime
keywords:
  - openclaw embedded agent runtime
  - single agent per gateway
  - bootstrap files agents soul tools
  - agents.defaults.workspace
  - skills load precedence
  - jsonl session store sessionid
  - steering while streaming queue
  - provider model ref parsing
topics:
  - OpenClaw
  - Agent Runtime
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/agent
access_control_group: ["general"]
---

# OpenClaw — The Embedded Agent Runtime Contract

## Overview

This note defines OpenClaw's **embedded agent runtime** contract: the single agent process per Gateway, with its own workspace, injected bootstrap files, and session store. It mirrors the `concepts/agent` source page — what the workspace must contain, which user-editable files get injected into the system prompt, the built-in tool surface, the skill-load precedence order, the runtime ownership boundary, the JSONL session store, mid-run steering and block-streaming defaults, `provider/model` ref parsing, and the minimal configuration. Full workspace layout, the agent loop lifecycle, and the runtime taxonomy are documented separately and linked below.

## Workspace (required)

OpenClaw uses a single agent workspace directory (`agents.defaults.workspace`) as the agent's **only** working directory (`cwd`) for tools and context. The recommended way to bootstrap it is to run `openclaw setup`, which creates `~/.openclaw/openclaw.json` if it is missing and initializes the workspace files. If `agents.defaults.sandbox` is enabled, non-main sessions can override this with per-session workspaces under `agents.defaults.sandbox.workspaceRoot` (a Gateway configuration concern). The full workspace layout and backup guide live on the dedicated Agent workspace page.

## Bootstrap files (injected)

Inside `agents.defaults.workspace`, OpenClaw expects these user-editable files: `AGENTS.md` (operating instructions + "memory"), `SOUL.md` (persona, boundaries, tone), `TOOLS.md` (user-maintained tool notes, e.g. `imsg`, `sag`, conventions), `BOOTSTRAP.md` (one-time first-run ritual, deleted after completion), `IDENTITY.md` (agent name/vibe/emoji), and `USER.md` (user profile + preferred address). On the first turn of a new session, OpenClaw injects the contents of these files into the system prompt's Project Context.

Blank files are skipped, and large files are trimmed and truncated with a marker so prompts stay lean. If a file is missing, OpenClaw injects a single "missing file" marker line, and `openclaw setup` will create a safe default template. `BOOTSTRAP.md` is only created for a **brand new workspace** (no other bootstrap files present); while it is pending, OpenClaw keeps it in Project Context and adds system-prompt bootstrap guidance for the initial ritual instead of copying it into the user message, and if you delete it after completing the ritual it should not be recreated on later restarts.

After a workspace has been observed, OpenClaw also keeps a state-dir attestation marker for the workspace path. If a recently attested workspace disappears or is wiped, startup refuses to silently re-seed `BOOTSTRAP.md`; restore the workspace or use a full onboard reset so the workspace and marker are cleared together. To disable bootstrap file creation entirely (for pre-seeded workspaces), set:

```json5
{ agents: { defaults: { skipBootstrap: true } } }
```

## Built-in tools

Core tools (read/exec/edit/write and related system tools) are always available, subject to tool policy. `apply_patch` is optional and gated by `tools.exec.applyPatch`. `TOOLS.md` does **not** control which tools exist — it is guidance for how _you_ want them used.

## Skills

OpenClaw loads skills from these locations, highest precedence first:

- Workspace: `<workspace>/skills`
- Project agent skills: `<workspace>/.agents/skills`
- Personal agent skills: `~/.agents/skills`
- Managed/local: `~/.openclaw/skills`
- Bundled (shipped with the install)
- Extra skill folders: `skills.load.extraDirs`

Skill roots can contain grouped folders such as `<workspace>/skills/personal/foo/SKILL.md`; the skill is still exposed by its flat frontmatter name, for example `foo`. Skills can be gated by config/env (the `skills` section in Gateway configuration).

## Runtime boundaries

The embedded agent runtime is OpenClaw-owned: model discovery, tool wiring, prompt assembly, session management, and channel delivery share one integrated runtime surface.

## Sessions

Session transcripts are stored as JSONL at `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`. The session ID is stable and chosen by OpenClaw. Legacy session folders from other tools are not read.

## Steering while streaming

Inbound prompts that arrive mid-run are steered into the current run by default. Steering is delivered **after the current assistant turn finishes executing its tool calls**, before the next LLM call, and no longer skips remaining tool calls from the current assistant message. `/queue steer` is the default active-run behavior; `/queue followup` and `/queue collect` make messages wait for a later turn instead of steering; `/queue interrupt` aborts the active run instead. The Queue and Steering queue pages describe queue and boundary behavior.

Block streaming sends completed assistant blocks as soon as they finish; it is **off by default** (`agents.defaults.blockStreamingDefault: "off"`). Tune the boundary via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end`; defaults to `text_end`). Control soft block chunking with `agents.defaults.blockStreamingChunk` (defaults to 800-1200 chars; prefers paragraph breaks, then newlines, then sentences last). Coalesce streamed chunks with `agents.defaults.blockStreamingCoalesce` to reduce single-line spam (idle-based merging before send). Non-Telegram channels require explicit `*.blockStreaming: true` to enable block replies. Verbose tool summaries are emitted at tool start (no debounce), and the Control UI streams tool output via agent events when available.

## Model refs

Model refs in config (for example `agents.defaults.model` and `agents.defaults.models`) are parsed by splitting on the **first** `/`. Use `provider/model` when configuring models. If the model ID itself contains `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`). If you omit the provider, OpenClaw tries an alias first, then a unique configured-provider match for that exact model id, and only then falls back to the configured default provider; if that provider no longer exposes the configured default model, OpenClaw falls back to the first configured provider/model instead of surfacing a stale removed-provider default.

## Configuration (minimal)

At minimum, set `agents.defaults.workspace` and `channels.whatsapp.allowFrom` (strongly recommended).

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway product; relevance: the embedded runtime is OpenClaw's core agent contract.
- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — harness that runs an agent loop; relevance: the embedded runtime is OpenClaw's harness implementation.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — self-driving coding agents; relevance: the agent process this contract defines is a coding agent.
- **[Skills](../../term_dictionary/term_skills.md)** — loadable agent capabilities; relevance: the skill-load precedence order this page specifies.
- **[Persona](../../term_dictionary/term_persona.md)** — agent personality/SOUL; relevance: SOUL.md persona injected via bootstrap files.
- **[Steering Files](../../term_dictionary/term_steering_files.md)** — AGENTS/TOOLS/USER guidance files; relevance: the injected bootstrap files this page enumerates.
- **[Session ID](../../term_dictionary/term_sessionid.md)** — stable session identifier; relevance: OpenClaw-chosen SessionId for the JSONL store.
- **[Session Persistence](../../term_dictionary/term_session_persistence.md)** — durable session state; relevance: the JSONL transcript store described here.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolation boundary; relevance: `agents.defaults.sandbox` per-session workspace override.

**Docs**

- **[oc_concepts_agent_workspace](oc_concepts_agent_workspace.md)** — full workspace layout (this series); relevance: the workspace this contract requires.
- **[oc_concepts_agent_loop](oc_concepts_agent_loop.md)** — loop lifecycle (this series); relevance: how sessions run against this runtime.
- **[oc_concepts_agent_runtimes](oc_concepts_agent_runtimes.md)** — runtime families (this series); relevance: where the embedded openclaw runtime sits in the taxonomy.
- **[oc_concepts_architecture](oc_concepts_architecture.md)** — gateway architecture (this series); relevance: one agent runtime per Gateway.
- **[oc_concepts_session](oc_concepts_session.md)** — session model (planned, co06); relevance: the session store this contract uses.
- **[cc_claude_md_files](../claude_code/cc_claude_md_files.md)** — CLAUDE.md project files; relevance: the closest analog to AGENTS.md bootstrap injection.
- **[cc_skills_overview](../claude_code/cc_skills_overview.md)** — Claude Code skills; relevance: comparable skill-loading precedence model.
- **[hermes_personality_soul](../hermes_agent/hermes_personality_soul.md)** — Hermes SOUL.md; relevance: the persona-file equivalent of OpenClaw SOUL.md.
- **[hermes_context_files](../hermes_agent/hermes_context_files.md)** — Hermes context/bootstrap files; relevance: AGENTS/USER/TOOLS-equivalent injected files.
- **[pi_sessions](../pi/pi_sessions.md)** — Pi session model; relevance: sibling-harness session/runtime contract.
- **[band_agent_lifecycle](../band/band_agent_lifecycle.md)** — Band agent lifecycle; relevance: cross-platform agent-process lifecycle analog.
- **[band_sdk_reference_agent_core](../band/band_sdk_reference_agent_core.md)** — Band agent-core SDK; relevance: the agent-runtime contract counterpart.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — embedded agent runtime; relevance: implements this contract.
- **[repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md)** — session store; relevance: the JSONL transcript store.
- **[repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md)** — skill loader; relevance: skill-load precedence implementation.

**Snippets**

- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — runtime config; relevance: the agent runtime configuration surface.
- **[snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md)** — agent identity; relevance: IDENTITY.md / agent id wiring.
- **[snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md)** — bootstrap budget; relevance: bootstrapMaxChars/total trimming of injected files.
- **[snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md)** — system-prompt injection; relevance: how bootstrap files enter Project Context.
- **[snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md)** — skills planner; relevance: skill load + precedence resolution.
- **[snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md)** — skill availability; relevance: config/env skill gating.
- **[snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md)** — tool catalog; relevance: built-in tools available to the runtime.
- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool policy; relevance: apply_patch gating / tool availability subject to policy.
- **[snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md)** — session-key utils; relevance: stable SessionId derivation.
- **[snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md)** — session lifecycle; relevance: bootstrap-on-first-turn lifecycle.
- **[snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md)** — agent scope; relevance: single-runtime-per-Gateway boundary.
- **[snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md)** — system-prompt modes; relevance: prompt assembly the bootstrap files feed.

## References

- [OpenClaw Docs — Agent runtime](https://docs.openclaw.ai/concepts/agent)
- [OpenClaw Docs — Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)
- [OpenClaw Docs — Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw Docs — Session management](https://docs.openclaw.ai/concepts/session)
- [OpenClaw Docs — Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docs — Queue](https://docs.openclaw.ai/concepts/queue)
- [OpenClaw Docs — Steering queue](https://docs.openclaw.ai/concepts/queue-steering)
- [OpenClaw Docs — Streaming + chunking](https://docs.openclaw.ai/concepts/streaming)
- [OpenClaw Docs — Group Chats](https://docs.openclaw.ai/channels/group-messages)

**Source**: OpenClaw documentation — `concepts/agent` (mirror `inbox/openclaw_docs/concepts/agent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
