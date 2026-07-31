---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - config_agents
keywords:
  - openclaw cliBackends config
  - agents.defaults.cliBackends
  - agents.defaults.promptOverlays
  - cli backend text-only fallback
  - gpt5 prompt overlay personality
  - reseedFromRawTranscriptWhenUncompacted
  - sessionMode systemPromptWhen imageMode
topics:
  - OpenClaw
  - Agent Defaults Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Agent Defaults: CLI Backends and Prompt Overlays

## Overview

This note documents two `agents.defaults.*` configuration blocks from the OpenClaw `gateway/config-agents` reference page: `agents.defaults.cliBackends` (optional CLI backends used as text-only fallback runs when API providers fail) and `agents.defaults.promptOverlays` (provider-independent prompt overlays applied by model family). Both are agent-scoped defaults under `agents.*`; per-channel, tool, and other top-level keys live in the Configuration reference. This is a configuration procedure: each subsection gives the JSON5 config shape and the per-field behavior exactly as the source page states.

## `agents.defaults.cliBackends`

Optional CLI backends for **text-only fallback runs (no tool calls)**. They are useful as a backup when API providers fail. CLI backends are text-first and tools are always disabled.

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          // Or use systemPromptFileArg when the CLI accepts a prompt file flag.
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

The keys of the `cliBackends` map are backend ids (for example `claude-cli`, `my-cli`). Each backend value is an object describing how OpenClaw invokes that CLI:

- `command` — the executable to run (an absolute path such as `/opt/homebrew/bin/claude`, or a name resolved on `PATH` such as `my-cli`).
- `args` — extra command-line arguments passed to the CLI (for example `["--json"]`).
- `output` — output parsing mode for the CLI's stdout; the example uses `json`.
- `modelArg` — the flag the CLI uses to receive the model id (example `--model`).
- `sessionArg` — the flag used to pass a session id. Sessions are supported when `sessionArg` is set.
- `sessionMode` — how the backend reuses sessions; the example uses `existing`.
- `systemPromptArg` — the flag used to pass the system prompt inline (example `--system`). Alternatively use `systemPromptFileArg` when the CLI accepts a prompt-file flag instead of an inline prompt.
- `systemPromptWhen` — when the system prompt is sent; the example uses `first`.
- `imageArg` — the flag used to pass an image (example `--image`). Image pass-through is supported when `imageArg` accepts file paths.
- `imageMode` — how multiple images are passed; the example uses `repeat`.

The source states three behavior rules for CLI backends and one recovery flag:

- CLI backends are text-first; tools are always disabled.
- Sessions supported when `sessionArg` is set.
- Image pass-through supported when `imageArg` accepts file paths.
- `reseedFromRawTranscriptWhenUncompacted: true` lets a backend recover safe invalidated sessions from a bounded raw OpenClaw transcript tail before the first compaction summary exists. Auth profile or credential-epoch changes still never raw-reseed.

## `agents.defaults.promptOverlays`

Provider-independent **prompt overlays** applied by model family on OpenClaw-assembled prompt surfaces. The source states that GPT-5-family model ids receive the shared behavior contract across OpenClaw/provider routes; `personality` controls only the friendly interaction-style layer. Native Codex app-server routes keep Codex-owned base/model instructions instead of this OpenClaw GPT-5 overlay, and OpenClaw disables Codex's built-in personality for native threads.

```json5
{
  agents: {
    defaults: {
      promptOverlays: {
        gpt5: {
          personality: "friendly", // friendly | on | off
        },
      },
    },
  },
}
```

The `gpt5.personality` field accepts `friendly`, `on`, or `off`, with these behaviors per the source:

- `"friendly"` (default) and `"on"` enable the friendly interaction-style layer.
- `"off"` disables only the friendly layer; the tagged GPT-5 behavior contract remains enabled.
- Legacy `plugins.entries.openai.config.personality` is still read when this shared setting is unset.

**Source**: OpenClaw documentation — `gateway/config-agents` (mirror `inbox/openclaw_docs/gateway/config-agents.md`), sections `agents.defaults.cliBackends` and `agents.defaults.promptOverlays`
**Last Updated**: 2026-06-22
**Status**: Active
