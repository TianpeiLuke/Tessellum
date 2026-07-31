---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness config reference
  - plugins.entries.codex.config
  - codex app-server transport
  - codex approval sandbox modes
  - codex guardian yolo mode
  - codex model discovery fallback catalog
  - workspace bootstrap files codex
  - openclaw_codex_app_server env overrides
topics:
  - OpenClaw
  - Codex Harness Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/codex-harness-reference
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Configuration Reference

## Overview

This note models the **declarative configuration surface** of the bundled `codex` plugin — the half of the `plugins/codex-harness-reference` source page that describes config fields, defaults, and the values they accept (the runtime-execution half — sandboxed native exec, auth/env isolation, dynamic tools, and timeouts — is documented separately). It covers the top-level `plugins.entries.codex.config` fields, the `appServer` transport options (stdio vs WebSocket), the approval/sandbox `mode` presets (YOLO vs guardian), `model/list` discovery and the bundled fallback catalog, the OpenClaw workspace bootstrap files forwarded to Codex, and the `OPENCLAW_CODEX_APP_SERVER_*` environment overrides. Every field name, default, and value below is reproduced verbatim from the source reference page.

## Plugin config surface

All Codex harness settings live under `plugins.entries.codex.config`. A minimal config enables discovery and selects the guardian preset:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          discovery: {
            enabled: true,
            timeoutMs: 2500,
          },
          appServer: {
            mode: "guardian",
          },
        },
      },
    },
  },
}
```

Supported top-level `config` fields:

| Field | Default | Meaning |
| --- | --- | --- |
| `discovery` | enabled | Model discovery settings for Codex app-server `model/list`. |
| `appServer` | managed stdio app-server | Transport, command, auth, approval, sandbox, and timeout settings. |
| `codexDynamicToolsLoading` | `"searchable"` | Use `"direct"` to put OpenClaw dynamic tools directly in the initial Codex tool context. |
| `codexDynamicToolsExclude` | `[]` | Additional OpenClaw dynamic tool names to omit from Codex app-server turns. |
| `codexPlugins` | disabled | Native Codex plugin/app support for migrated source-installed curated plugins. |
| `computerUse` | disabled | Codex Computer Use setup. |

## App-server transport

By default OpenClaw starts the managed Codex binary shipped with the bundled plugin (run as `codex app-server --listen stdio://`). This keeps the app-server version tied to the bundled `codex` plugin instead of whichever separate Codex CLI happens to be installed locally. Set `appServer.command` only when you intentionally want to run a different executable. For an already-running app-server, use WebSocket transport:

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
            requestTimeoutMs: 60000,
          },
        },
      },
    },
  },
}
```

Supported `appServer` fields (defaults verbatim from source):

| Field | Default | Meaning |
| --- | --- | --- |
| `transport` | `"stdio"` | `"stdio"` spawns Codex; `"websocket"` connects to `url`. |
| `command` | managed Codex binary | Executable for stdio transport. Leave unset to use the managed binary. |
| `args` | `["app-server", "--listen", "stdio://"]` | Arguments for stdio transport. |
| `url` | unset | WebSocket app-server URL. |
| `authToken` | unset | Bearer token for WebSocket transport. Accepts a literal string or SecretInput such as `${CODEX_APP_SERVER_TOKEN}`. |
| `headers` | `{}` | Extra WebSocket headers. Values accept literal strings or SecretInput, e.g. `x-codex-client-session-token: "${CODEX_CLIENT_SESSION_TOKEN}"`. |
| `clearEnv` | `[]` | Extra environment variable names removed from the spawned stdio app-server process after OpenClaw builds its inherited environment. |
| `remoteWorkspaceRoot` | unset | Remote Codex app-server workspace root; OpenClaw infers the local root from the resolved OpenClaw workspace, preserves the cwd suffix under this remote root, and sends only the final cwd to Codex. A cwd outside the resolved workspace root fails closed. |
| `requestTimeoutMs` | `60000` | Timeout for app-server control-plane calls. |
| `turnCompletionIdleTimeoutMs` | `60000` | Quiet window after Codex accepts a turn (or after a turn-scoped request) while OpenClaw waits for `turn/completed`. |
| `postToolRawAssistantCompletionIdleTimeoutMs` | `300000` | Completion-idle/progress guard after a tool handoff, native tool completion, post-tool raw assistant progress, raw reasoning completion, or reasoning progress while awaiting `turn/completed`. |
| `mode` | `"yolo"` unless local Codex requirements disallow YOLO | Preset for YOLO or guardian-reviewed execution. |
| `approvalPolicy` | `"never"` or an allowed guardian approval policy | Native Codex approval policy sent to thread start, resume, and turn. |
| `sandbox` | `"danger-full-access"` or an allowed guardian sandbox | Native Codex sandbox mode sent to thread start and resume. Active OpenClaw sandboxes narrow `danger-full-access` turns to Codex `workspace-write`; the turn network flag follows OpenClaw sandbox egress. |
| `approvalsReviewer` | `"user"` or an allowed guardian reviewer | Use `"auto_review"` to let Codex review native approval prompts when allowed. |
| `defaultWorkspaceDir` | current process directory | Workspace used by `/codex bind` when `--cwd` is omitted. |
| `serviceTier` | unset | Optional service tier. `"priority"` enables fast-mode routing, `"flex"` requests flex processing, `null` clears the override. Legacy `"fast"` is accepted as `"priority"`. |
| `networkProxy` | disabled | Opt into Codex permissions-profile networking for app-server commands. |
| `experimental.sandboxExecServer` | `false` | Preview opt-in registering an OpenClaw sandbox-backed Codex environment with Codex app-server 0.132.0 or newer. |

`appServer.networkProxy` is explicit because it changes the Codex sandbox contract. When enabled, OpenClaw also sets `features.network_proxy.enabled` and `default_permissions` in the Codex thread config so the generated permission profile can start Codex managed networking. By default OpenClaw generates a collision-resistant `openclaw-network-<fingerprint>` profile name from the profile body; use `profileName` only when a stable local name is required:

```js
export default {
  plugins: {
    entries: {
      codex: {
        config: {
          appServer: {
            sandbox: "workspace-write",
            networkProxy: {
              enabled: true,
              domains: {
                "api.openai.com": "allow",
                "blocked.example.com": "deny",
              },
              allowUpstreamProxy: true,
              proxyUrl: "http://127.0.0.1:3128",
            },
          },
        },
      },
    },
  },
};
```

If the normal app-server runtime would be `danger-full-access`, enabling `networkProxy` uses workspace-style filesystem access for the generated permission profile, because Codex managed network enforcement is sandboxed networking and a full-access profile would not protect outbound traffic. The plugin blocks older or unversioned app-server handshakes: Codex app-server must report stable version `0.125.0` or newer. OpenClaw treats non-loopback WebSocket app-server URLs as remote and requires identity-bearing WebSocket auth through `appServer.authToken` or an `Authorization` header; `appServer.authToken` and each `appServer.headers.*` value can be a SecretInput, with the secrets runtime resolving SecretRefs and env shorthand before start options are built, and unresolved structured SecretRefs failing before any token or header is sent. When native Codex plugins are configured, OpenClaw uses the connected app-server's plugin control plane to install or refresh those plugins and then refreshes app inventory, so only connect to remote app-servers trusted to accept OpenClaw-managed plugin installs and app-inventory refreshes.

## Approval and sandbox modes

Local stdio app-server sessions default to YOLO mode: `approvalPolicy: "never"`, `approvalsReviewer: "user"`, and `sandbox: "danger-full-access"`. This trusted local-operator posture lets unattended OpenClaw turns and heartbeats make progress without native approval prompts that nobody is around to answer. If Codex's local system-requirements file disallows implicit YOLO approval, reviewer, or sandbox values, OpenClaw treats the implicit default as guardian instead and selects allowed guardian permissions. `tools.exec.mode: "auto"` also forces guardian-reviewed Codex approvals and does not preserve unsafe legacy `approvalPolicy: "never"` or `sandbox: "danger-full-access"` overrides; set `tools.exec.mode: "full"` for an intentional no-approval posture. Hostname-matching `[[remote_sandbox_config]]` entries in the same requirements file are honored for the sandbox-default decision.

Set `appServer.mode: "guardian"` for Codex guardian-reviewed approvals:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            mode: "guardian",
            serviceTier: "priority",
          },
        },
      },
    },
  },
}
```

The `guardian` preset expands to `approvalPolicy: "on-request"`, `approvalsReviewer: "auto_review"`, and `sandbox: "workspace-write"` when those values are allowed. Individual policy fields override `mode`. The older `guardian_subagent` reviewer value is still accepted as a compatibility alias, but new configs should use `auto_review`. When an OpenClaw sandbox is active, the local Codex app-server process still runs on the Gateway host, so OpenClaw disables Codex native Code Mode, user MCP servers, and app-backed plugin execution for that turn rather than treating Codex host-side sandboxing as equivalent to the OpenClaw sandbox backend; shell access is then exposed through OpenClaw sandbox-backed dynamic tools such as `sandbox_exec` and `sandbox_process` when the normal exec/process tools are available. On Ubuntu/AppArmor hosts, Codex `bwrap` can fail under `workspace-write` before the shell command starts when you intentionally run native Codex `workspace-write` without active OpenClaw sandboxing; if you see `bwrap: setting up uid map: Permission denied` or `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, run `openclaw doctor` and fix the reported host namespace policy for the OpenClaw service user rather than granting broader Docker container privileges — prefer a scoped AppArmor profile, since the `kernel.apparmor_restrict_unprivileged_userns=0` fallback is host-wide and has security tradeoffs.

## Model discovery

By default the Codex plugin asks the app-server for available models. Model availability is owned by Codex app-server, so the list can change when OpenClaw upgrades the bundled `@openai/codex` version or when a deployment points `appServer.command` at a different Codex binary; availability can also be account-scoped. Use `/codex models` on a running gateway to see the live catalog for that harness and account. If discovery fails or times out, OpenClaw uses a bundled fallback catalog for **GPT-5.5**, **GPT-5.4 mini**, and **GPT-5.2**.

The current bundled harness is `@openai/codex` `0.139.0`. A `model/list` probe against that bundled app-server returned:

| Model id | Default | Hidden | Input modalities | Reasoning efforts |
| --- | --- | --- | --- | --- |
| `gpt-5.5` | Yes | No | text, image | low, medium, high, xhigh |
| `gpt-5.4` | No | No | text, image | low, medium, high, xhigh |
| `gpt-5.4-mini` | No | No | text, image | low, medium, high, xhigh |
| `gpt-5.3-codex` | No | No | text, image | low, medium, high, xhigh |
| `gpt-5.2` | No | No | text, image | low, medium, high, xhigh |

Hidden models can be returned by the app-server catalog for internal or specialized flows, but they are not normal model-picker choices. Tune discovery under `plugins.entries.codex.config.discovery`:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          discovery: {
            enabled: true,
            timeoutMs: 2500,
          },
        },
      },
    },
  },
}
```

Set `discovery.enabled: false` to make startup avoid probing Codex and use only the fallback catalog.

## Workspace bootstrap files

Codex handles `AGENTS.md` itself through native project-doc discovery. OpenClaw does not write synthetic Codex project-doc files or depend on Codex fallback filenames for persona files, because Codex fallbacks only apply when `AGENTS.md` is missing. For OpenClaw workspace parity the Codex harness resolves the other bootstrap files: `SOUL.md`, `IDENTITY.md`, `TOOLS.md`, and `USER.md` are forwarded as OpenClaw Codex developer instructions because they define the active agent, available workspace guidance, and user profile. The compact OpenClaw skills list is forwarded as turn-scoped collaboration developer instructions. `HEARTBEAT.md` content is not injected; heartbeat turns get a collaboration-mode pointer to read the file when it exists and is non-empty. `MEMORY.md` content from the configured agent workspace is not pasted into native Codex turn input when memory tools are available for that workspace — when it exists, the harness adds a small workspace-memory pointer to turn-scoped collaboration developer instructions and Codex should use `memory_search` or `memory_get` when durable memory is relevant; if tools are disabled, memory search is unavailable, or the active workspace differs from the agent memory workspace, `MEMORY.md` uses the normal bounded turn-context path. `BOOTSTRAP.md`, when present, is forwarded as OpenClaw turn input reference context.

## Environment overrides

Environment overrides remain available for local testing:

- `OPENCLAW_CODEX_APP_SERVER_BIN`
- `OPENCLAW_CODEX_APP_SERVER_ARGS`
- `OPENCLAW_CODEX_APP_SERVER_MODE=yolo|guardian`
- `OPENCLAW_CODEX_APP_SERVER_APPROVAL_POLICY`
- `OPENCLAW_CODEX_APP_SERVER_SANDBOX`

`OPENCLAW_CODEX_APP_SERVER_BIN` bypasses the managed binary when `appServer.command` is unset. `OPENCLAW_CODEX_APP_SERVER_GUARDIAN=1` was removed: use `plugins.entries.codex.config.appServer.mode: "guardian"` instead, or `OPENCLAW_CODEX_APP_SERVER_MODE=guardian` for one-off local testing. Config is preferred for repeatable deployments because it keeps the plugin behavior in the same reviewed file as the rest of the Codex harness setup.

**Source**: OpenClaw documentation — `plugins/codex-harness-reference` (mirror `inbox/openclaw_docs/plugins/codex-harness-reference.md`)
**Last Updated**: 2026-06-22
**Status**: Active
