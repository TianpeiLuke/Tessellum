---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - acp
keywords:
  - openclaw acpx setup
  - acp backend plugin install
  - acpx harness aliases
  - plugin-tools mcp bridge
  - openclaw-tools mcp bridge
  - acpx permissionmode
  - noninteractivepermissions
  - acpx health probe agent
  - acpx runtime timeout
topics:
  - OpenClaw
  - ACP Agents Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/acp-agents-setup
access_control_group: ["general"]
---

# OpenClaw — Setting Up the ACP / acpx Backend

## Overview

This note is the operator procedure for installing and configuring the OpenClaw ACP backend — the `@openclaw/acpx` runtime plugin — so OpenClaw can run external coding harnesses (Claude Code, Codex, Gemini CLI, Cursor, and others) over the Agent Client Protocol. It mirrors the `tools/acp-agents-setup` source page and covers: the current acpx harness aliases, the required `acp` config baseline plus channel-adapter thread-binding config, plugin install/enable, the acpx command/version override, automatic dependency install, the two opt-in MCP bridges (plugin-tools and OpenClaw-tools), the runtime operation timeout, the health-probe agent, and ACP permission configuration (`permissionMode` and `nonInteractivePermissions`). The concept layer, operator runbook, and spawn/bind flows live on the sibling ACP notes; use this page only when wiring the ACP/acpx route itself. For native Codex app-server runtime config use the Codex harness page, and for OpenAI API keys or Codex OAuth provider config use the OpenAI provider page.

## acpx Harness Support (current)

Codex has two OpenClaw routes, and you should prefer the native route unless you explicitly need ACP/acpx behavior. The **Native Codex app-server** route uses `/codex ...` commands and `openai/gpt-*` agent refs (set up on the Codex harness page). The **Explicit Codex ACP adapter** route uses `/acp spawn codex` and `runtime: "acp", agentId: "codex"` (set up on this page).

The current acpx built-in harness aliases are: `claude`, `codex`, `copilot`, `cursor` (Cursor CLI: `cursor-agent acp`), `droid`, `gemini`, `iflow`, `kilocode`, `kimi`, `kiro`, `openclaw`, `opencode`, and `qwen`. When OpenClaw uses the acpx backend, prefer these values for `agentId` unless your acpx config defines custom agent aliases. If your local Cursor install still exposes ACP as `agent acp`, override the `cursor` agent command in your acpx config instead of changing the built-in default. Direct acpx CLI usage can also target arbitrary adapters via `--agent <command>`, but that raw escape hatch is an acpx CLI feature, not the normal OpenClaw `agentId` path.

Model control is adapter-capability dependent. Codex ACP model refs are normalized by OpenClaw before startup; other harnesses need ACP `models` plus `session/set_model` support, and if a harness exposes neither that ACP capability nor its own startup model flag, OpenClaw/acpx cannot force a model selection.

## Required Config

The core ACP baseline goes under the `acp` config key. `dispatch` is optional and defaults to `true`; set it `false` to pause ACP dispatch while keeping `/acp` controls.

```json5
{
  acp: {
    enabled: true,
    // Optional. Default is true; set false to pause ACP dispatch while keeping /acp controls.
    dispatch: { enabled: true },
    backend: "acpx",
    defaultAgent: "codex",
    allowedAgents: [
      "claude",
      "codex",
      "copilot",
      "cursor",
      "droid",
      "gemini",
      "iflow",
      "kilocode",
      "kimi",
      "kiro",
      "openclaw",
      "opencode",
      "qwen",
    ],
    maxConcurrentSessions: 8,
    stream: {
      coalesceIdleMs: 300,
      maxChunkChars: 1200,
    },
    runtime: {
      ttlMinutes: 120,
    },
  },
}
```

Thread binding config is channel-adapter specific. The Discord example sets a top-level `session.threadBindings` block (`enabled`, `idleHours: 24`, `maxAgeHours: 0`) plus a per-channel `channels.discord.threadBindings` block with `enabled: true` and `spawnSessions: true`. If thread-bound ACP spawn does not work, verify the adapter feature flag first — for Discord that is `channels.discord.threadBindings.spawnSessions=true`. Current-conversation binds do not require child-thread creation; they require an active conversation context and a channel adapter that exposes ACP conversation bindings. See the Configuration Reference for the full schema.

## Plugin Setup for the acpx Backend

Packaged installs use the official `@openclaw/acpx` runtime plugin for ACP. Install and enable it before using ACP harness sessions, then start with `/acp doctor` to verify backend health.

```bash
openclaw plugins install @openclaw/acpx
openclaw config set plugins.entries.acpx.enabled true
```

Source checkouts can also use the local workspace plugin after `pnpm install`. If you disabled `acpx`, denied it via `plugins.allow` / `plugins.deny`, or want to switch back to the packaged plugin, use the explicit package path (the same `openclaw plugins install @openclaw/acpx` + `openclaw config set plugins.entries.acpx.enabled true` pair). A local workspace install during development uses `openclaw plugins install ./path/to/local/acpx-plugin`. Then re-run `/acp doctor` to verify backend health. See the Plugins page for more.

### acpx Command and Version Configuration

By default the `acpx` plugin registers the embedded ACP backend during Gateway startup and waits for the embedded runtime startup probe before the gateway `ready` signal. Set `OPENCLAW_ACPX_RUNTIME_STARTUP_PROBE=0` or `OPENCLAW_SKIP_ACPX_RUNTIME_PROBE=1` only for scripts or environments that intentionally keep the startup probe disabled; run `/acp doctor` for an explicit on-demand probe.

Override the command or version in plugin config. `command` accepts an absolute path, a relative path (resolved from the OpenClaw workspace), or a command name; `expectedVersion: "any"` disables strict version matching; and custom `command` paths disable plugin-local auto-install.

```json
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "command": "../acpx/dist/cli.js",
          "expectedVersion": "any"
        }
      }
    }
  }
}
```

To override an individual ACP agent command with structured arguments when a path or flag value should remain one argv token, use `plugins.entries.acpx.config.agents.<id>` with `command` and an optional `args` array. `agents.<id>.command` is the executable or existing command string for that ACP agent, and each item in `agents.<id>.args` is shell-quoted before OpenClaw passes it through the current acpx command-string registry (for example, `"command": "node"` with `"args": ["/path/to/custom adapter.mjs", "--verbose"]`).

### Automatic Dependency Install

When you install OpenClaw globally with `npm install -g openclaw`, the acpx runtime dependencies (platform-specific binaries) are installed automatically via a postinstall hook. If the automatic install fails, the gateway still starts normally and reports the missing dependency through `openclaw acp doctor`.

### Plugin-Tools MCP Bridge

By default, ACPX sessions do **not** expose OpenClaw plugin-registered tools to the ACP harness. If you want ACP agents such as Codex or Claude Code to call installed OpenClaw plugin tools such as memory recall/store, enable the dedicated bridge:

```bash
openclaw config set plugins.entries.acpx.config.pluginToolsMcpBridge true
```

What this does: it injects a built-in MCP server named `openclaw-plugin-tools` into ACPX session bootstrap, exposes plugin tools already registered by installed and enabled OpenClaw plugins, and keeps the feature explicit and default-off. Security and trust notes: this expands the ACP harness tool surface; ACP agents get access only to plugin tools already active in the gateway; treat this as the same trust boundary as letting those plugins execute in OpenClaw itself; and review installed plugins before enabling it. Custom `mcpServers` still work as before — the built-in plugin-tools bridge is an additional opt-in convenience, not a replacement for generic MCP server config.

### OpenClaw-Tools MCP Bridge

By default, ACPX sessions also do **not** expose built-in OpenClaw tools through MCP. Enable the separate core-tools bridge when an ACP agent needs selected built-in tools such as `cron`:

```bash
openclaw config set plugins.entries.acpx.config.openClawToolsMcpBridge true
```

What this does: it injects a built-in MCP server named `openclaw-tools` into ACPX session bootstrap, exposes selected built-in OpenClaw tools (the initial server exposes `cron`), and keeps core-tool exposure explicit and default-off.

### Runtime Operation Timeout Configuration

The `acpx` plugin gives embedded runtime startup and control operations 120 seconds by default, which gives slower harnesses such as Gemini CLI enough time to complete ACP startup and initialization. Override it with `openclaw config set plugins.entries.acpx.config.timeoutSeconds 180` if your host needs a different operation limit. Runtime turns use OpenClaw agent/run timeouts, including `/acp timeout`; `sessions_spawn` does not accept per-call timeout overrides. Restart the gateway after changing this value.

### Health-Probe Agent Configuration

When `/acp doctor` or the startup probe checks the backend, the bundled `acpx` plugin probes one harness agent. If `acp.allowedAgents` is set, it defaults to the first allowed agent; otherwise it defaults to `codex`. If your deployment needs a different ACP agent for health checks, set the probe agent explicitly with `openclaw config set plugins.entries.acpx.config.probeAgent claude`. Restart the gateway after changing this value.

## Permission Configuration

ACP sessions run non-interactively — there is no TTY to approve or deny file-write and shell-exec permission prompts. The acpx plugin provides two config keys that control how permissions are handled. These ACPX harness permissions are separate from OpenClaw exec approvals and separate from CLI-backend vendor bypass flags such as Claude CLI `--permission-mode bypassPermissions`; ACPX `approve-all` is the harness-level break-glass switch for ACP sessions. For the broader comparison between OpenClaw `tools.exec.mode`, Codex Guardian approvals, and ACPX harness permissions, see the Permission modes page.

### `permissionMode`

`permissionMode` controls which operations the harness agent can perform without prompting. `approve-all` auto-approves all file writes and shell commands; `approve-reads` auto-approves reads only, while writes and exec require prompts; and `deny-all` denies all permission prompts.

### `nonInteractivePermissions`

`nonInteractivePermissions` controls what happens when a permission prompt would be shown but no interactive TTY is available (which is always the case for ACP sessions). `fail` aborts the session with `AcpRuntimeError` and is the **default**; `deny` silently denies the permission and continues (graceful degradation).

### Configuration

Set both via plugin config, then restart the gateway after changing these values:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
```

OpenClaw defaults to `permissionMode=approve-reads` and `nonInteractivePermissions=fail`. In non-interactive ACP sessions, any write or exec that triggers a permission prompt can fail with `AcpRuntimeError: Permission prompt unavailable in non-interactive mode`. If you need to restrict permissions, set `nonInteractivePermissions` to `deny` so sessions degrade gracefully instead of crashing.

**Source**: OpenClaw documentation — `tools/acp-agents-setup` (mirror `inbox/openclaw_docs/tools/acp-agents-setup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
