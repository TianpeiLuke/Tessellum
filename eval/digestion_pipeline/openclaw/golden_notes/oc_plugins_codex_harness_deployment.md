---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness deployment patterns
  - basic codex deployment
  - mixed provider deployment
  - fail-closed codex agentRuntime
  - app-server policy approval sandbox
  - tools.exec.mode auto guardian
  - danger-full-access workspace-write
  - openclaw codex deployment
topics:
  - OpenClaw
  - Codex Harness Deployment
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Deployment Patterns and App-Server Policy

## Overview

This note is the deployment-shape procedure for the bundled `codex` plugin: the three deployment patterns OpenClaw documents — **Basic Codex**, **Mixed provider**, and **Fail-closed Codex** — plus the **app-server policy** that controls approvals, sandbox, and exec behavior per deployment. It mirrors the `plugins/codex-harness` source page sections "Deployment patterns" (Basic / Mixed provider / Fail-closed) and "App-server policy." Enabling, OAuth quickstart, and routing/model selection are covered in the setup note; the full declarative `appServer.*` field reference (transport, timeouts, discovery, env isolation) lives in the harness reference notes. Use this note when choosing how a deployment routes OpenAI agent turns through Codex and what approval/sandbox posture each shape gets.

## Deployment Patterns

The Codex harness supports three deployment shapes you choose between. All three assume the bundled `codex` plugin is enabled and (where `plugins.allow` is configured) allowlisted. The shapes differ in whether Codex is the default runtime, one named agent among several, or a forced fail-closed requirement.

### Basic Codex deployment

Use the quickstart config when all OpenAI agent turns should use Codex by default. This is the minimum viable shape — enable the plugin and point the default agent model at a canonical `openai/gpt-*` ref:

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

### Mixed provider deployment

This shape keeps Claude as the default agent and adds a named Codex agent. The `main` agent uses its normal provider path and the `codex` agent uses Codex app-server:

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
      model: "anthropic/claude-opus-4-6",
    },
    list: [
      {
        id: "main",
        default: true,
        model: "anthropic/claude-opus-4-6",
      },
      {
        id: "codex",
        name: "Codex",
        model: "openai/gpt-5.5",
      },
    ],
  },
}
```

With this config, the `main` agent uses its normal provider path and the `codex` agent uses Codex app-server.

### Fail-closed Codex deployment

For OpenAI agent turns, `openai/gpt-*` already resolves to Codex when the bundled plugin is available. Add explicit runtime policy when you want a written fail-closed rule via provider- (or model-) level `agentRuntime.id: "codex"`:

```json5
{
  models: {
    providers: {
      openai: {
        agentRuntime: {
          id: "codex",
        },
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
    },
  },
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

With Codex forced, OpenClaw fails early if the Codex plugin is disabled, the app-server is too old, or the app-server cannot start — instead of silently falling back to the OpenClaw embedded runtime. Use this shape for Codex-only deployments.

## App-Server Policy

By default, the plugin starts OpenClaw's managed Codex binary locally with stdio transport. Set `appServer.command` only when you intentionally want to run a different executable. Use WebSocket transport only when an app-server is already running elsewhere:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            transport: "websocket",
            url: "ws://gateway-host:39175",
            authToken: "${CODEX_APP_SERVER_TOKEN}",
          },
        },
      },
    },
  },
}
```

Local stdio app-server sessions default to the trusted local operator posture: `approvalPolicy: "never"`, `approvalsReviewer: "user"`, and `sandbox: "danger-full-access"`. If local Codex requirements disallow that implicit YOLO posture, OpenClaw selects allowed guardian permissions instead. When an OpenClaw sandbox is active for the session, OpenClaw disables Codex native Code Mode, user MCP servers, and app-backed plugin execution for that turn instead of relying on Codex host-side sandboxing. Shell access is exposed through OpenClaw sandbox-backed dynamic tools such as `sandbox_exec` and `sandbox_process` when the normal exec/process tools are available.

### Guardian-reviewed exec mode

Use normalized OpenClaw exec mode when you want Codex native auto-review before sandbox escapes or extra permissions:

```json5
{
  tools: {
    exec: {
      mode: "auto",
    },
  },
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

For Codex app-server sessions, OpenClaw maps `tools.exec.mode: "auto"` to Codex Guardian-reviewed approvals, usually `approvalPolicy: "on-request"`, `approvalsReviewer: "auto_review"`, and `sandbox: "workspace-write"` when the local requirements allow those values. In `tools.exec.mode: "auto"`, OpenClaw does not preserve legacy unsafe Codex `approvalPolicy: "never"` or `sandbox: "danger-full-access"` overrides; use `tools.exec.mode: "full"` for an intentional no-approval Codex posture. The legacy `plugins.entries.codex.config.appServer.mode: "guardian"` preset still works, but `tools.exec.mode: "auto"` is the normalized OpenClaw surface. For the mode-level comparison with host exec approvals and ACPX permissions, see [Permission modes](https://docs.openclaw.ai/tools/permission-modes).

For every app-server field, auth order, environment isolation, discovery, and timeout behavior, see [Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference).

**Source**: OpenClaw documentation — `plugins/codex-harness` (mirror `inbox/openclaw_docs/plugins/codex-harness.md`), sections "Deployment patterns" + "App-server policy"
**Last Updated**: 2026-06-22
**Status**: Active
