---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - cli_backends
keywords:
  - openclaw cli backends
  - cli backend fallback
  - claude-cli backend
  - agents.defaults.cliBackends
  - cli backend quick start
  - bundleMcp loopback bridge
  - cli backend images pass-through
  - cli backend troubleshooting
topics:
  - OpenClaw
  - CLI Backends
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/cli-backends
access_control_group: ["general"]
---

# OpenClaw — Setting Up CLI Backends as a Model Fallback

## Overview

This note is the user-facing setup-and-operation procedure for OpenClaw **CLI backends** — running a local AI CLI (e.g. Claude Code CLI) as a **text-only fallback** when API providers are down, rate-limited, or temporarily misbehaving. It covers the beginner-friendly quick start, wiring a backend into the model fallback list, the `agents.defaults.cliBackends` configuration overview with a worked example, image pass-through, input/output modes, limitations, and troubleshooting — mirroring the user-facing half of the `gateway/cli-backends` source page. The internal mechanics (the JSONL streaming loop, MCP loopback bridge, session reuse, claude-cli fallback prelude, plugin-owned defaults, native-compaction ownership, bundle MCP overlays, and the reseed history cap) live in the sibling note **[oc_gateway_cli_backends_internals](oc_gateway_cli_backends_internals.md)**.

CLI backends are intentionally conservative and designed as a **safety net** rather than a primary path: OpenClaw tools are not injected directly (backends with `bundleMcp: true` can receive gateway tools via a loopback MCP bridge), JSONL streaming is used for CLIs that support it, sessions are supported so follow-up turns stay coherent, and images can be passed through if the CLI accepts image paths. CLI backends are **not ACP** — for a full harness runtime with ACP session controls, background tasks, thread/conversation binding, and persistent external coding sessions, use ACP Agents instead. To build a new backend plugin (rather than configure an already-registered one), use CLI backend plugins.

## Beginner-friendly quick start

You can use Claude Code CLI **without any config** — the bundled Anthropic plugin registers a default backend:

```bash
openclaw agent --agent main --message "hi" --model claude-cli/claude-sonnet-4-6
```

`main` is the default agent id when no explicit agent list is configured; if you use multiple agents, replace it with the agent id you want to run. If your gateway runs under launchd/systemd and PATH is minimal, add just the command path:

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
      },
    },
  },
}
```

That's it — no keys, no extra auth config needed beyond the CLI itself. If you use a bundled CLI backend as the **primary message provider** on a gateway host, OpenClaw auto-loads the owning bundled plugin when your config explicitly references that backend in a model ref or under `agents.defaults.cliBackends`.

## Using it as a fallback

Add a CLI backend to your fallback list so it only runs when primary models fail:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["claude-cli/claude-sonnet-4-6"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "claude-cli/claude-sonnet-4-6": {},
      },
    },
  },
}
```

Two operating notes apply. If you use `agents.defaults.models` (an allowlist), you must include your CLI backend models there too. If the primary provider fails (auth, rate limits, timeouts), OpenClaw will try the CLI backend next.

## Configuration overview

All CLI backends live under `agents.defaults.cliBackends`. Each entry is keyed by a **provider id** (e.g. `claude-cli`, `my-cli`), and the provider id becomes the left side of your model ref, in the form `<provider>/<model>`.

### Example configuration

The worked example below shows the full set of per-backend keys a custom CLI backend (`my-cli`) can declare:

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          input: "arg",
          modelArg: "--model",
          modelAliases: {
            "claude-opus-4-6": "opus",
            "claude-sonnet-4-6": "sonnet",
          },
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptArg: "--system",
          // For CLIs with a dedicated prompt-file flag:
          // systemPromptFileArg: "--system-file",
          // Codex-style CLIs can point at a prompt file instead:
          // systemPromptFileConfigArg: "-c",
          // systemPromptFileConfigKey: "model_instructions_file",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          // Opt in only if this backend may reseed safe invalidated sessions
          // from bounded raw OpenClaw transcript history before compaction.
          reseedFromRawTranscriptWhenUncompacted: true,
          serialize: true,
        },
      },
    },
  },
}
```

The session, serialization, and reseed semantics behind keys such as `sessionMode`, `serialize`, and `reseedFromRawTranscriptWhenUncompacted` are documented in the internals sibling **[oc_gateway_cli_backends_internals](oc_gateway_cli_backends_internals.md)**.

## Images (pass-through)

If your CLI accepts image paths, set `imageArg`:

```json5
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw will write base64 images to temp files. If `imageArg` is set, those paths are passed as CLI args. If `imageArg` is missing, OpenClaw appends the file paths to the prompt (path injection), which is enough for CLIs that auto-load local files from plain paths.

## Inputs / outputs

Output parsing modes are selected with the `output` key:

- `output: "json"` (default) tries to parse JSON and extract text + session id.
- For Gemini CLI JSON output, OpenClaw reads reply text from `response` and usage from `stats` when `usage` is missing or empty. The bundled Gemini CLI default uses `stream-json`, but old `--output-format json` overrides still use the JSON parser.
- `output: "jsonl"` parses JSONL streams and extracts the final agent message plus session identifiers when present.
- `output: "text"` treats stdout as the final response.

Input modes are selected with the `input` key:

- `input: "arg"` (default) passes the prompt as the last CLI arg.
- `input: "stdin"` sends the prompt via stdin.
- If the prompt is very long and `maxPromptArgChars` is set, stdin is used.

## Limitations

- **No direct OpenClaw tool calls.** OpenClaw does not inject tool calls into the CLI backend protocol. Backends only see gateway tools when they opt into `bundleMcp: true`.
- **Streaming is backend-specific.** Some backends stream JSONL; others buffer until exit.
- **Structured outputs** depend on the CLI's JSON format.

## Troubleshooting

- **CLI not found**: set `command` to a full path.
- **Wrong model name**: use `modelAliases` to map `provider/model` → CLI model.
- **No session continuity**: ensure `sessionArg` is set and `sessionMode` is not `none`.
- **Images ignored**: set `imageArg` (and verify CLI supports file paths).

**Source**: OpenClaw documentation — `gateway/cli-backends` (mirror `inbox/openclaw_docs/gateway/cli-backends.md`)
**Last Updated**: 2026-06-22
**Status**: Active
