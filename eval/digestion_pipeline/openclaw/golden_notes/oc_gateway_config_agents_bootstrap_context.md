---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - config_agents
keywords:
  - openclaw agents.defaults workspace
  - agents.defaults bootstrap config
  - contextInjection continuation-skip
  - bootstrapMaxChars bootstrapTotalMaxChars
  - skipBootstrap skipOptionalBootstrapFiles
  - bootstrapPromptTruncationWarning
  - context budget ownership map
  - per-agent bootstrap profile overrides
  - openclaw skills allowlist
topics:
  - OpenClaw
  - Gateway Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Agent Defaults: Workspace, Bootstrap, and Context Budgets

## Overview

This note documents the workspace/bootstrap/context cluster of OpenClaw's `agents.defaults.*` configuration surface, from the `gateway/config-agents` reference page. It is a procedure note: the config keys an operator sets to control where an agent works, which workspace bootstrap files are created and injected, and how much bootstrap/context material is allowed into the system prompt. Covered keys are `workspace`, `repoRoot`, `skills`, `skipBootstrap`, `skipOptionalBootstrapFiles`, `contextInjection`, `bootstrapMaxChars`, `bootstrapTotalMaxChars`, the per-agent bootstrap profile overrides, `bootstrapPromptTruncationWarning`, and the Context budget ownership map (plus its `startupContext`, `contextLimits`, and `skills.limits` sub-keys). The `model`, media, runtime-policy, backends, resilience, routing, session, messages, and talk keys on the same page belong to sibling notes in this `config-agents` split.

## Workspace and Repository Root

`agents.defaults.workspace` sets the default working directory for agents that do not set `agents.list[].workspace`. Default: `OPENCLAW_WORKSPACE_DIR` when set, otherwise `~/.openclaw/workspace`. An explicit `agents.defaults.workspace` value takes precedence over `OPENCLAW_WORKSPACE_DIR`; use the environment variable to point default agents at a mounted workspace when you do not want to write that path into config.

`agents.defaults.repoRoot` is an optional repository root shown in the system prompt's Runtime line. If unset, OpenClaw auto-detects by walking upward from the workspace.

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      repoRoot: "~/Projects/openclaw",
    },
  },
}
```

## Skills Allowlist

`agents.defaults.skills` is an optional default skill allowlist for agents that do not set `agents.list[].skills`. Behavior rules from source: omit `agents.defaults.skills` for unrestricted skills by default; omit `agents.list[].skills` to inherit the defaults; set `agents.list[].skills: []` for no skills; a non-empty `agents.list[].skills` list is the final set for that agent and does not merge with defaults.

```json5
{
  agents: {
    defaults: { skills: ["github", "weather"] },
    list: [
      { id: "writer" }, // inherits github, weather
      { id: "docs", skills: ["docs-search"] }, // replaces defaults
      { id: "locked-down", skills: [] }, // no skills
    ],
  },
}
```

## Bootstrap File Creation Flags

`agents.defaults.skipBootstrap`, when `true`, disables automatic creation of workspace bootstrap files: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, and `BOOTSTRAP.md`.

`agents.defaults.skipOptionalBootstrapFiles` skips creation of selected optional workspace files while still writing required bootstrap files. Valid values: `SOUL.md`, `USER.md`, `HEARTBEAT.md`, and `IDENTITY.md`.

```json5
{
  agents: {
    defaults: {
      skipBootstrap: true,
      skipOptionalBootstrapFiles: ["SOUL.md", "USER.md"],
    },
  },
}
```

## Context Injection

`agents.defaults.contextInjection` controls when workspace bootstrap files are injected into the system prompt. Default: `"always"`. Modes from source:

- `"continuation-skip"`: safe continuation turns (after a completed assistant response) skip workspace bootstrap re-injection, reducing prompt size. Heartbeat runs and post-compaction retries still rebuild context.
- `"never"`: disable workspace bootstrap and context-file injection on every turn. Use this only for agents that fully own their prompt lifecycle (custom context engines, native runtimes that build their own context, or specialized bootstrap-free workflows). Heartbeat and compaction-recovery turns also skip injection.

```json5
{
  agents: { defaults: { contextInjection: "continuation-skip" } },
}
```

Per-agent override: `agents.list[].contextInjection`. Omitted values inherit `agents.defaults.contextInjection`.

## Bootstrap Character Budgets

`agents.defaults.bootstrapMaxChars` is the max characters per workspace bootstrap file before truncation. Default: `20000`. `agents.defaults.bootstrapTotalMaxChars` is the max total characters injected across all workspace bootstrap files. Default: `60000`. Each has a per-agent override (`agents.list[].bootstrapMaxChars` and `agents.list[].bootstrapTotalMaxChars`) whose omitted values inherit the corresponding default.

```json5
{
  agents: {
    defaults: {
      bootstrapMaxChars: 20000,
      bootstrapTotalMaxChars: 60000,
    },
  },
}
```

### Per-agent bootstrap profile overrides

Use per-agent bootstrap profile overrides when one agent needs different prompt injection behavior from the shared defaults. Omitted fields inherit from `agents.defaults`.

```json5
{
  agents: {
    defaults: {
      contextInjection: "continuation-skip",
      bootstrapMaxChars: 20000,
      bootstrapTotalMaxChars: 60000,
    },
    list: [
      {
        id: "strict-worker",
        contextInjection: "always",
        bootstrapMaxChars: 50000,
        bootstrapTotalMaxChars: 300000,
      },
    ],
  },
}
```

### `agents.defaults.bootstrapPromptTruncationWarning`

Controls the agent-visible system-prompt notice when bootstrap context is truncated. Default: `"always"`. Values: `"off"` never injects truncation notice text into the system prompt; `"once"` injects a concise notice once per unique truncation signature; `"always"` (recommended) injects a concise notice on every run when truncation exists. Per source, detailed raw/injected counts and config tuning fields stay in diagnostics such as context/status reports and logs, while routine WebChat user/runtime context only gets the concise recovery notice.

## Context Budget Ownership Map

OpenClaw has multiple high-volume prompt/context budgets, and they are intentionally split by subsystem instead of all flowing through one generic knob. The ownership map from source:

- `agents.defaults.bootstrapMaxChars` / `agents.defaults.bootstrapTotalMaxChars`: normal workspace bootstrap injection.
- `agents.defaults.startupContext.*`: one-shot reset/startup model-run prelude, including recent daily `memory/*.md` files. Bare chat `/new` and `/reset` commands are acknowledged without invoking the model.
- `skills.limits.*`: the compact skills list injected into the system prompt.
- `agents.defaults.contextLimits.*`: bounded runtime excerpts and injected runtime-owned blocks.
- `memory.qmd.limits.*`: indexed memory-search snippet and injection sizing.

Use the matching per-agent override only when one agent needs a different budget: `agents.list[].skillsLimits.maxSkillsPromptChars`, `agents.list[].contextInjection`, `agents.list[].bootstrapMaxChars`, `agents.list[].bootstrapTotalMaxChars`, and `agents.list[].contextLimits.*`.

### `agents.defaults.startupContext`

Controls the first-turn startup prelude injected on reset/startup model runs. Its fields (from source) are `enabled`, `applyOn` (e.g. `["new", "reset"]`), `dailyMemoryDays` (e.g. `2`), `maxFileBytes` (e.g. `16384`), `maxFileChars` (e.g. `1200`), and `maxTotalChars` (e.g. `2800`). Per source, bare chat `/new` and `/reset` commands acknowledge the reset without invoking the model, so they do not load this prelude.

### `agents.defaults.contextLimits`

Shared defaults for bounded runtime context surfaces. Field semantics from source: `memoryGetMaxChars` is the default `memory_get` excerpt cap before truncation metadata and continuation notice are added (e.g. `12000`); `memoryGetDefaultLines` is the default `memory_get` line window when `lines` is omitted (e.g. `120`); `toolResultMaxChars` is an advanced live tool-result ceiling used for persisted results and overflow recovery — leave unset for the model-context auto cap (`16000` chars below 100K tokens, `32000` chars at 100K+ tokens, `64000` chars at 200K+ tokens), with the effective cap still limited to about 30% of the model context window, where `openclaw doctor --deep` prints the effective cap and doctor warns only when an explicit override is stale or has no effect; `postCompactionMaxChars` is the `AGENTS.md` excerpt cap used during post-compaction refresh injection (e.g. `1800`). The per-agent override `agents.list[].contextLimits` inherits omitted fields from `agents.defaults.contextLimits`.

### Skills prompt budget

`skills.limits.maxSkillsPromptChars` (e.g. `18000`) is the global cap for the compact skills list injected into the system prompt. Per source, this does not affect reading `SKILL.md` files on demand. The per-agent override is `agents.list[].skillsLimits.maxSkillsPromptChars`.

**Source**: OpenClaw documentation — `gateway/config-agents` (Agent defaults: workspace/bootstrap/context cluster; mirror `inbox/openclaw_docs/gateway/config-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
