---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - experimental_features
keywords:
  - openclaw experimental features
  - experimental config flags
  - localModelLean lean mode
  - tools.experimental.planTool
  - sessionMemory experimental
  - sandboxExecServer codex
  - tool search lean mode
  - opt-in preview surfaces
topics:
  - OpenClaw
  - Experimental Features
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/experimental-features
access_control_group: ["general"]
---

# OpenClaw — Experimental Features and the Opt-In Preview-Flag Policy

## Overview

This note captures OpenClaw's **experimental-features policy**: what an experimental flag *means*, how operators should treat it differently from normal config, the four currently documented experimental flags, and the one experimental flag the source page explains in depth — local-model lean mode. It mirrors the `concepts/experimental-features` source page. The central concept is that experimental features in OpenClaw are **opt-in preview surfaces** placed behind explicit `.experimental` config keys because they still need real-world mileage before they deserve a stable default or a long-lived public contract — and that an experimental feature is *documented*, not hidden.

## What Experimental Means in OpenClaw

Experimental features in OpenClaw are **opt-in preview surfaces**. They sit behind explicit flags because they still need real-world mileage before they deserve a stable default or a long-lived public contract. Because the contract is provisional, the source page tells operators to treat these flags differently from normal config along four rules: keep them **off by default** unless the related doc tells you to try one; expect **shape and behavior to change** faster than stable config; prefer the stable path first when one already exists; and, if you are rolling OpenClaw out broadly, test experimental flags in a smaller environment before baking them into a shared baseline. The flag's experimental status is signalled in the config path itself — every documented preview key lives under an `.experimental` (or `experimental:`) namespace.

## Currently Documented Flags

The page enumerates four experimental surfaces, each with its config key (copied verbatim), the situation it is meant for, and the "More" doc that owns it:

- **Local model runtime** — `agents.defaults.experimental.localModelLean`, `agents.list[].experimental.localModelLean`. Use it when a smaller or stricter local backend chokes on OpenClaw's full default tool surface. More: Local Models (`/gateway/local-models`).
- **Memory search** — `agents.defaults.memorySearch.experimental.sessionMemory`. Use it when you want `memory_search` to index prior session transcripts and accept the extra storage/indexing cost. More: Memory configuration reference (`/reference/memory-config#session-memory-search-experimental`).
- **Codex harness** — `plugins.entries.codex.config.appServer.experimental.sandboxExecServer`. Use it when you want native Codex app-server 0.132.0 or newer to target an OpenClaw sandbox-backed exec-server instead of disabling Code Mode. More: Codex harness reference (`/plugins/codex-harness-reference#sandboxed-native-execution`).
- **Structured planning tool** — `tools.experimental.planTool`. Use it when you want the structured `update_plan` tool exposed for multi-step work tracking in compatible runtimes and UIs. More: Gateway configuration reference (`/gateway/config-tools#toolsexperimental`).

## Local Model Lean Mode

`agents.defaults.experimental.localModelLean: true` is a pressure-release valve for weaker local-model setups. When it is on, OpenClaw drops three default tools — `browser`, `cron`, and `message` — from the agent's tool surface for every turn. It also defaults that run to structured Tool Search controls when `tools.toolSearch` is not explicitly configured, so larger plugin, MCP, or client tool catalogs stay behind `tool_search`, `tool_describe`, and `tool_call` instead of being dumped into the prompt. Runs that require direct `message` delivery keep that tool direct instead of enabling the lean-mode Tool Search default. To enable or disable the same behavior for one configured agent, use `agents.list[].experimental.localModelLean`.

### Why These Three Tools

The `browser`, `cron`, and `message` tools have the largest descriptions and the most parameter shapes in the default OpenClaw runtime. On a small-context or stricter OpenAI-compatible backend, removing them is the difference between: tool schemas fitting cleanly in the prompt vs. crowding out conversation history; the model picking the right tool vs. emitting malformed tool calls because there are too many similar-looking schemas; and the Chat Completions adapter staying inside the server's structured-output limits vs. tripping a 400 on tool-call payload size. Removing them does not silently rewire OpenClaw — it just makes the direct tool list shorter. The model still has `read`, `write`, `edit`, `exec`, `apply_patch`, web search/fetch (when configured), memory, and session/agent tools available, and extra catalogs remain callable through Tool Search unless you explicitly set `tools.toolSearch: false`.

### When to Turn It On

Enable lean mode when you have already proved the model can talk to the Gateway but full agent turns misbehave. The typical signal chain is: (1) `openclaw infer model run --gateway --model <ref> --prompt "Reply with exactly: pong"` succeeds; (2) a normal agent turn fails with malformed tool calls, oversized prompts, or the model ignoring its tools; (3) toggling `localModelLean: true` clears the failure.

### When to Leave It Off

If your backend handles the full default runtime cleanly, leave this off — lean mode is a workaround, not a default. It exists because some local stacks need a smaller tool surface to behave; hosted models and well-resourced local rigs do not. Lean mode also does not replace `tools.profile`, `tools.allow`/`tools.deny`, or the model `compat.supportsTools: false` escape hatch; if you need a permanent narrower tool surface for a specific agent, prefer those stable knobs over the experimental flag. Finally, if you already tune Tool Search globally, OpenClaw leaves that operator config alone — set `tools.toolSearch: false` to opt out of the lean-mode Tool Search default.

### Enable

Lean mode is enabled with a JSON5 config block under `agents.defaults`:

```json5
{
  agents: {
    defaults: {
      experimental: {
        localModelLean: true,
      },
    },
  },
}
```

For one agent only, set the flag inside that agent's `agents.list[]` entry:

```json5
{
  agents: {
    list: [
      {
        id: "local",
        model: "lmstudio/gemma-4-e4b-it",
        experimental: {
          localModelLean: true,
        },
      },
    ],
  },
}
```

Restart the Gateway after changing the flag, then confirm the trimmed tool list with:

```bash
openclaw status --deep
```

The deep status output lists the active agent tools; `browser`, `cron`, and `message` should be absent when lean mode is on unless the current delivery mode forces direct `message` replies.

## Experimental Does Not Mean Hidden

If a feature is experimental, OpenClaw should say so plainly in docs and in the config path itself. What it should **not** do is smuggle preview behavior into a stable-looking default knob and pretend that is normal — that is how config surfaces get messy. This config-hygiene principle is why every preview surface above is named under an explicit `.experimental` key rather than masquerading as a stable default.

**Source**: OpenClaw documentation — `concepts/experimental-features` (mirror `inbox/openclaw_docs/concepts/experimental-features.md`)
**Last Updated**: 2026-06-22
**Status**: Active
