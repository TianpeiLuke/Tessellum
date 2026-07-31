---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - system_prompt
keywords:
  - workspace bootstrap injection
  - bootstrapMaxChars bootstrapTotalMaxChars
  - MEMORY.md injection
  - skills list injection
  - formatSkillsForPrompt
  - system prompt time handling
  - documentation section
  - native codex bootstrap forwarding
topics:
  - OpenClaw
  - System Prompt
language: markdown
date of note: 2026-06-23
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/system-prompt
access_control_group: ["general"]
---

# OpenClaw — System Prompt Injection (Bootstrap, Skills, Time, Docs)

## Overview

This note is the operator-facing procedure half of the `concepts/system-prompt` page (split from the structure/assembly concept in [oc_concepts_system_prompt_structure](oc_concepts_system_prompt_structure.md)). It covers how workspace bootstrap files are injected and bounded, how time handling is configured, how the available-skills list is injected and budgeted, and what the Documentation section points the agent at.

## Workspace Bootstrap Injection

Bootstrap files are resolved from the active workspace, then routed to the prompt surface that matches their lifetime:

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (only on brand-new workspaces)
- `MEMORY.md` when present

On the **native Codex harness**, OpenClaw avoids repeating stable workspace files in every user turn: Codex loads `AGENTS.md` through its own project-doc discovery; `SOUL.md`, `IDENTITY.md`, `TOOLS.md`, and `USER.md` are forwarded as Codex developer instructions; the compact OpenClaw skills list is forwarded as turn-scoped collaboration developer instructions; `HEARTBEAT.md` content is not injected (heartbeat turns get a collaboration-mode note pointing to the file when it exists and is non-empty); and `MEMORY.md` is not pasted into every native Codex turn — when memory tools are available, turns get a small workspace-memory note and should use `memory_search` / `memory_get`, otherwise `MEMORY.md` falls back to the normal bounded turn-context path. Active `BOOTSTRAP.md` keeps the normal turn-context role for now.

On **non-Codex harnesses**, bootstrap files are composed into the OpenClaw prompt according to their existing gates. `HEARTBEAT.md` is omitted on normal runs when heartbeats are disabled for the default agent or `agents.defaults.heartbeat.includeSystemPromptSection` is false. Keep injected files concise, especially non-Codex `MEMORY.md`: it should stay a curated long-term summary, with detailed daily notes in `memory/*.md` where `memory_search` and `memory_get` retrieve them on demand. Oversized non-Codex `MEMORY.md` files increase prompt usage and can be partially injected because of the bootstrap limits below.

> `memory/*.md` daily files are **not** part of the normal bootstrap Project Context. On ordinary turns they are accessed on demand via `memory_search` / `memory_get`, so they do not count against the context window unless the model explicitly reads them. Bare `/new` and `/reset` turns are the exception: the runtime can prepend recent daily memory as a one-shot startup-context block for that first turn.

### Bootstrap size limits

Large files are truncated with a marker. The per-file max is `agents.defaults.bootstrapMaxChars` (default `20000`); total injected bootstrap content across files is capped by `agents.defaults.bootstrapTotalMaxChars` (default `60000`). Missing files inject a short missing-file marker. When truncation occurs, OpenClaw can inject a concise system-prompt warning, controlled by `agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always`; default `always`). Detailed raw/injected counts stay in diagnostics such as `/context`, `/status`, doctor, and logs.

For memory files, truncation is **not** data loss — the file stays intact on disk. On native Codex, `MEMORY.md` is read on demand through memory tools (with bounded prompt fallback when tools cannot run); on other harnesses the model only sees the shortened injected copy until it reads or searches memory directly. If `MEMORY.md` is repeatedly truncated, distill it into a shorter durable summary and move history into `memory/*.md`, or intentionally raise the bootstrap limits. Sub-agent sessions only inject `AGENTS.md` and `TOOLS.md` (other bootstrap files are filtered to keep sub-agent context small). Internal hooks can intercept this step via `agent:bootstrap` to mutate or replace injected bootstrap files (for example swapping `SOUL.md` for an alternate persona). To inspect how much each injected file contributes (raw vs injected, truncation, plus tool-schema overhead), use `/context list` or `/context detail`.

## Time Handling

The prompt includes a dedicated **Current Date & Time** section when the user timezone is known. To stay cache-stable, it now includes only the **time zone** (no dynamic clock or time format). Use `session_status` when the agent needs the current time — the status card includes a timestamp line, and the same tool can optionally set a per-session model override (`model=default` clears it). Configure with `agents.defaults.userTimezone` and `agents.defaults.timeFormat` (`auto` | `12` | `24`); see Date & Time for full behavior.

## Skills List Injection

When eligible skills exist, OpenClaw injects a compact **available skills list** (`formatSkillsForPrompt`) that includes the **file path** and a content-derived `<version>` marker per skill. The prompt instructs the model to use `read` to load the `SKILL.md` at the listed location (workspace, managed, or bundled) and to re-read a skill when its `<version>` differs from a previous turn. If no skills are eligible, the Skills section is omitted. Native Codex turns receive this list as turn-scoped collaboration developer instructions instead of per-turn user input, except lightweight cron turns that preserve the exact scheduled prompt. The location can point at a nested skill (e.g. `skills/personal/foo/SKILL.md`); nesting is only organizational and the prompt still uses the flat skill name from frontmatter. Eligibility includes skill metadata gates, runtime environment/config checks, and the effective agent skill allowlist when `agents.defaults.skills` or `agents.list[].skills` is configured; plugin-bundled skills are eligible only when their owning plugin is enabled.

The injected block has the shape:

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
    <version>sha256:...</version>
  </skill>
</available_skills>
```

The skills-list budget is owned by the skills subsystem: global default `skills.limits.maxSkillsPromptChars`, per-agent override `agents.list[].skillsLimits.maxSkillsPromptChars`. Generic bounded runtime excerpts (memory_get, live tool results, post-compaction `AGENTS.md` refreshes) use a different surface — `agents.defaults.contextLimits.*` / `agents.list[].contextLimits.*` — keeping skills sizing separate from runtime read/injection sizing.

## Documentation Section

The prompt includes a **Documentation** section pointing at the local OpenClaw docs directory (`docs/` in a Git checkout or the bundled npm package docs), falling back to `https://docs.openclaw.ai` when local docs are unavailable. The same section includes the OpenClaw source location: Git checkouts expose the local source root so the agent can inspect code directly, and package installs include the GitHub source URL and tell the agent to review source there when docs are incomplete or stale. The prompt also notes the public docs mirror, community Discord, and ClawHub (`https://clawhub.ai`) for skills discovery. It frames docs as the authority for OpenClaw self-knowledge (memory/daily notes, sessions, tools, Gateway, config, commands, project context) before the model relies on its own assumptions, and tells the model to treat `AGENTS.md`, project context, workspace/profile/memory notes, and `memory_search` as instruction context / user memory rather than OpenClaw design knowledge. If docs are silent or stale, the model should say so and inspect source, and should run `openclaw status` itself when possible. For configuration specifically, it points agents to the `gateway` tool action `config.schema.lookup` for exact field-level docs and constraints, then to `docs/gateway/configuration.md` and `docs/gateway/configuration-reference.md` for broader guidance.

**Source**: OpenClaw documentation — `concepts/system-prompt` (injection/skills/docs half; mirror `inbox/openclaw_docs/concepts/system-prompt.md`)
**Last Updated**: 2026-06-23
**Status**: Active
