---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - openclaw codex harness setup
  - bundled codex plugin enable
  - codex app-server quickstart
  - openai/gpt-5.5 model ref
  - openclaw models auth login --provider openai
  - auth.order.openai subscription-first
  - agentRuntime.id codex
  - verify codex runtime /status
  - routing and model selection
topics:
  - OpenClaw
  - Codex Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Setup (Enable, Configure, Verify, Route)

## Overview

This note is the setup procedure for the bundled `codex` plugin, which lets OpenClaw run embedded OpenAI agent turns through **Codex app-server** instead of the built-in OpenClaw harness. It covers the intro ownership boundary (what OpenClaw owns vs what Codex owns), requirements, the OAuth quickstart, the configuration-table options, runtime verification, and the routing/model-selection rules that keep `openai/gpt-*` provider refs separate from runtime policy — the first six sections of the `plugins/codex-harness` source page. Deployment patterns, app-server policy, commands/diagnostics, native Codex plugins, Computer Use, the full runtime-boundaries contract, and troubleshooting live in the sibling notes (see Related Notes). Full option lists, defaults, enums, discovery, environment isolation, and timeouts live in the Codex harness reference notes.

## What the Codex harness owns vs OpenClaw

Use the Codex harness when you want Codex to own the low-level agent session: native thread resume, native tool continuation, native compaction, and app-server execution. OpenClaw still owns chat channels, session files, model selection, OpenClaw dynamic tools, approvals, media delivery, and the visible transcript mirror. The normal setup uses canonical OpenAI model refs such as `openai/gpt-5.5` — do not configure legacy Codex GPT refs. Put OpenAI agent auth order under `auth.order.openai`; older legacy Codex auth profile ids and legacy Codex auth order entries are legacy state repaired by `openclaw doctor --fix`.

When no OpenClaw sandbox is active, OpenClaw starts Codex app-server threads with Codex native code mode enabled while leaving code-mode-only off by default, keeping Codex native workspace and code capabilities available while OpenClaw dynamic tools continue through the app-server `item/tool/call` bridge. Active OpenClaw sandboxing and restricted tool policies disable native code mode entirely unless you opt into the experimental sandbox exec-server path. This Codex-native feature is separate from OpenClaw code mode (the opt-in QuickJS-WASI runtime at `/reference/code-mode` for generic OpenClaw runs with a different `exec` input shape) — link out, not redefined here. The short version of the broader model/provider/runtime split (see Agent runtimes): `openai/gpt-5.5` is the model ref, `codex` is the runtime, and Telegram, Discord, Slack, or another channel remains the communication surface.

## Requirements

The bundled `codex` plugin needs the following available before setup:

- OpenClaw with the bundled `codex` plugin available.
- If your config uses `plugins.allow`, include `codex`.
- Codex app-server `0.125.0` or newer. The bundled plugin manages a compatible Codex app-server binary by default, so local `codex` commands on `PATH` do not affect normal harness startup.
- Codex auth available through `openclaw models auth login --provider openai`, an app-server account in the agent's Codex home, or an explicit Codex API-key auth profile.

For auth precedence, environment isolation, custom app-server commands, model discovery, and all config fields, see the Codex harness reference (`/plugins/codex-harness-reference`).

## Quickstart

Most users who want Codex in OpenClaw want this path: sign in with a ChatGPT/Codex subscription, enable the bundled `codex` plugin, and use a canonical `openai/gpt-*` model ref. First sign in with Codex OAuth:

```bash
openclaw models auth login --provider openai
```

Then enable the bundled `codex` plugin and select an OpenAI agent model:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
    },
  },
}
```

If your config uses `plugins.allow`, add `codex` there too:

```json5
{
  plugins: {
    allow: ["codex"],
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

Restart the gateway after changing plugin config. If an existing chat already has a session, use `/new` or `/reset` before testing runtime changes so the next turn resolves the harness from current config.

## Configuration

The quickstart config is the minimum viable Codex harness config. Set Codex harness options in OpenClaw config, and use the CLI only for Codex auth. The configuration-decision table maps each need to a setting and where it lives:

| Need | Set | Where |
| --- | --- | --- |
| Enable the harness | `plugins.entries.codex.enabled: true` | OpenClaw config |
| Keep an allowlisted plugin install | Include `codex` in `plugins.allow` | OpenClaw config |
| Route OpenAI agent turns through Codex | `agents.defaults.model` or `agents.list[].model` as `openai/gpt-*` | OpenClaw agent config |
| Sign in with ChatGPT/Codex OAuth | `openclaw models auth login --provider openai` | CLI auth profile |
| Add API-key backup for Codex runs | `openai:*` API-key profile listed after subscription auth in `auth.order.openai` | CLI auth profile + OpenClaw config |
| Fail closed when Codex is unavailable | Provider or model `agentRuntime.id: "codex"` | OpenClaw model/provider config |
| Use direct OpenAI API traffic | Provider or model `agentRuntime.id: "openclaw"` with normal OpenAI auth | OpenClaw model/provider config |
| Tune app-server behavior | `plugins.entries.codex.config.appServer.*` | Codex plugin config |
| Enable native Codex plugin apps | `plugins.entries.codex.config.codexPlugins.*` | Codex plugin config |
| Enable Codex Computer Use | `plugins.entries.codex.config.computerUse.*` | Codex plugin config |

Use `openai/gpt-*` model refs for Codex-backed OpenAI agent turns and prefer `auth.order.openai` for subscription-first/API-key-backup ordering. Existing legacy Codex auth profile ids and legacy Codex auth order are doctor-only legacy state; do not write new legacy Codex GPT refs.

Do not set `compaction.model` or `compaction.provider` on Codex-backed agents. Codex compacts through its native app-server thread state, so OpenClaw ignores those local summarizer overrides at runtime and `openclaw doctor --fix` removes them when the agent uses Codex. Lossless remains supported as a context engine for assembly, ingestion, and maintenance around Codex turns — configure it through `plugins.slots.contextEngine: "lossless-claw"` and `plugins.entries.lossless-claw.config.summaryModel`, not through `agents.defaults.compaction.provider`. `openclaw doctor --fix` migrates the old `compaction.provider: "lossless-claw"` shape to the Lossless context-engine slot when Codex is the active runtime, but native Codex still owns compaction. The native Codex app-server harness supports context engines that require pre-prompt assembly; generic CLI backends, including `codex-cli`, do not provide that host capability. For Codex-backed agents, `/compact` starts native Codex app-server compaction on the bound thread — OpenClaw does not wait for completion, impose an OpenClaw timeout, restart the shared app-server, or fall back to a context-engine or public OpenAI summarizer, and if the native Codex thread binding is missing or stale the command fails closed so the operator sees the real runtime boundary instead of silently switching compaction backends.

The subscription-first / API-key-backup auth order is configured as:

```json5
{
  auth: {
    order: {
      openai: ["openai:user@example.com", "openai:api-key-backup"],
    },
  },
}
```

In that shape, both profiles still run through Codex for `openai/gpt-*` agent turns — the API key is only an auth fallback, not a request to switch to OpenClaw or plain OpenAI Responses. The rest of the harness surface covers common variants users must choose between (deployment shape, fail-closed routing, guardian approval policy, native Codex plugins, and Computer Use); for full option lists, defaults, enums, discovery, environment isolation, timeouts, and app-server transport fields, see the Codex harness reference.

## Verify Codex runtime

Use `/status` in the chat where you expect Codex. A Codex-backed OpenAI agent turn shows:

```text
Runtime: OpenAI Codex
```

Then check Codex app-server state with `/codex status` and `/codex models`. `/codex status` reports app-server connectivity, account, rate limits, MCP servers, and skills. `/codex models` lists the live Codex app-server catalog for the harness and account. If `/status` is surprising, see the troubleshooting section of the source page (digested in the diagnostics sibling note).

## Routing and model selection

Keep provider refs and runtime policy separate:

- Use `openai/gpt-*` for OpenAI agent turns through Codex.
- Do not use legacy Codex GPT refs in config. Run `openclaw doctor --fix` to repair legacy refs and stale session route pins.
- `agentRuntime.id: "codex"` is optional for normal OpenAI auto mode, but useful when a deployment should fail closed if Codex is unavailable.
- `agentRuntime.id: "openclaw"` opts a provider or model into the OpenClaw embedded runtime when that is intentional.
- `/codex ...` controls native Codex app-server conversations from chat.
- ACP/acpx is a separate external harness path. Use it only when the user asks for ACP/acpx or an external harness adapter.

The common command-routing table maps a user intent to the chat command to use:

| User intent | Use |
| --- | --- |
| Attach the current chat | `/codex bind [--cwd <path>]` |
| Resume an existing Codex thread | `/codex resume <thread-id>` |
| List or filter Codex threads | `/codex threads [filter]` |
| List native Codex plugins | `/codex plugins list` |
| Enable or disable a configured native Codex plugin | `/codex plugins enable <name>`, `/codex plugins disable <name>` |
| Attach an existing Codex CLI session on a paired node | `/codex sessions --host <node> [filter]`, then `/codex resume <session-id> --host <node> --bind here` |
| Send Codex feedback only | `/codex diagnostics [note]` |
| Start an ACP/acpx task | ACP/acpx session commands, not `/codex` |

The use-case routing table maps a deployment goal to its config, verification, and notes:

| Use case | Configure | Verify | Notes |
| --- | --- | --- | --- |
| ChatGPT/Codex subscription with native Codex runtime | `openai/gpt-*` plus enabled `codex` plugin | `/status` shows `Runtime: OpenAI Codex` | Recommended path |
| Fail closed if Codex is unavailable | Provider or model `agentRuntime.id: "codex"` | Turn fails instead of embedded fallback | Use for Codex-only deployments |
| Direct OpenAI API-key traffic through OpenClaw | Provider or model `agentRuntime.id: "openclaw"` and normal OpenAI auth | `/status` shows OpenClaw runtime | Use only when OpenClaw is intentional |
| Legacy config | legacy Codex GPT refs | `openclaw doctor --fix` rewrites it | Do not write new config this way |
| ACP/acpx Codex adapter | ACP `sessions_spawn({ runtime: "acp" })` | ACP task/session status | Separate from native Codex harness |

`agents.defaults.imageModel` follows the same prefix split: use `openai/gpt-*` for the normal OpenAI route and `codex/gpt-*` only when image understanding should run through a bounded Codex app-server turn. Do not use legacy Codex GPT refs; doctor rewrites that legacy prefix to `openai/gpt-*`.

**Source**: OpenClaw documentation — `plugins/codex-harness` (intro, Requirements, Quickstart, Configuration, Verify Codex runtime, Routing and model selection; mirror `inbox/openclaw_docs/plugins/codex-harness.md`)
**Last Updated**: 2026-06-22
**Status**: Active
