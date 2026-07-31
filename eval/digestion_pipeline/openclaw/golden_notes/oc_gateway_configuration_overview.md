---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw configuration overview
  - openclaw.json json5 config
  - openclaw config edit paths
  - strict schema validation refuse to start
  - openclaw config schema lookup
  - config wizard onboard configure
  - control ui config tab
  - last-known-good config
  - dmpolicy allowfrom access control
topics:
  - OpenClaw
  - Gateway Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/configuration
access_control_group: ["general"]
---

# OpenClaw — Gateway Configuration Overview

## Overview

This note is the task-oriented procedure for configuring an OpenClaw Gateway through its optional JSON5 config file at `~/.openclaw/openclaw.json`. It mirrors the `gateway/configuration` source page sections that cover first-time setup: the minimal config, the four edit paths (interactive wizard, CLI one-liners, Control UI, direct file edit), the strict schema validation that makes the Gateway refuse to start on a bad config, the common-task accordion of pointers, and the deferral to the full field reference. Runtime concerns from the same page — config hot reload, the Config RPC, and environment variables — are the companion procedure `oc_gateway_config_reload_rpc_env` and are not duplicated here.

## Config file location

OpenClaw reads an optional <strong>JSON5</strong> config from `~/.openclaw/openclaw.json` (JSON5 supports comments and trailing commas). The active config path must be a regular file: symlinked `openclaw.json` layouts are unsupported for OpenClaw-owned writes, because an atomic write may replace the path instead of preserving the symlink. If you keep config outside the default state directory, point `OPENCLAW_CONFIG_PATH` directly at the real file. If the file is missing, OpenClaw uses safe defaults. Common reasons to add a config are: connect channels and control who can message the bot; set models, tools, sandboxing, or automation (cron, hooks); and tune sessions, media, networking, or UI.

## Minimal config

The smallest useful config sets a workspace and a single channel allowlist:

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

For tooling, agents and automation should use `config.schema.lookup` for exact field-level docs before editing config; this configuration page is for task-oriented guidance, and the [Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference) is for the broader field map and defaults. New users should start with `openclaw onboard` for interactive setup, or the [Configuration Examples](https://docs.openclaw.ai/gateway/configuration-examples) guide for complete copy-paste configs.

## Editing config (four edit paths)

There are four ways to edit the config. They all write the same `~/.openclaw/openclaw.json` (or its `$include` files) and all pass through the schema gate.

1. **Interactive wizard** — `openclaw onboard` runs the full onboarding flow; `openclaw configure` runs the config wizard.

   ```bash
   openclaw onboard       # full onboarding flow
   openclaw configure     # config wizard
   ```

2. **CLI (one-liners)** — `openclaw config get`, `openclaw config set`, and `openclaw config unset` edit individual paths.

   ```bash
   openclaw config get agents.defaults.workspace
   openclaw config set agents.defaults.heartbeat.every "2h"
   openclaw config unset plugins.entries.brave.config.webSearch.apiKey
   ```

3. **Control UI** — open `http://127.0.0.1:18789` and use the **Config** tab. The Control UI renders a form from the live config schema, including field `title` / `description` docs metadata plus plugin and channel schemas when available, with a **Raw JSON** editor as an escape hatch. For drill-down UIs and other tooling, the gateway also exposes `config.schema.lookup` to fetch one path-scoped schema node plus immediate child summaries.

4. **Direct edit** — edit `~/.openclaw/openclaw.json` directly. The Gateway watches the file and applies changes automatically (see hot reload, documented in `oc_gateway_config_reload_rpc_env`).

## Strict validation and refuse-to-start

OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start**. The only root-level exception is `$schema` (string), so editors can attach JSON Schema metadata. `openclaw config schema` prints the canonical JSON Schema used by Control UI and validation, while `config.schema.lookup` fetches a single path-scoped node plus child summaries for drill-down tooling. Field `title`/`description` docs metadata carries through nested objects, wildcard (`*`), array-item (`[]`), and `anyOf`/`oneOf`/`allOf` branches; runtime plugin and channel schemas merge in when the manifest registry is loaded.

When validation fails: the Gateway does not boot; only diagnostic commands work (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`); run `openclaw doctor` to see exact issues; and run `openclaw doctor --fix` (or `--yes`) to apply repairs. The Gateway keeps a trusted last-known-good copy after each successful startup, but startup and hot reload do not restore it automatically. If `openclaw.json` fails validation (including plugin-local validation), Gateway startup fails or the reload is skipped and the current runtime keeps the last accepted config. Run `openclaw doctor --fix` (or `--yes`) to repair prefixed/clobbered config or restore the last-known-good copy. Promotion to last-known-good is skipped when a candidate contains redacted secret placeholders such as `***`.

## Common tasks (pointer accordion)

The source page's "Common tasks" accordion is a set of task-scoped pointers into channel, agent, and reference pages rather than a full field reference. The common tasks and where each is configured are:

- **Set up a channel (WhatsApp, Telegram, Discord, etc.)** — each channel has its own section under `channels.<provider>`; all channels share the same `dmPolicy` pattern (`pairing | allowlist | open | disabled`). See the dedicated channel pages.
- **Choose and configure models** — set `agents.defaults.model.primary` and `agents.defaults.model.fallbacks`; `agents.defaults.models` defines the model catalog and acts as the allowlist for `/model`. Model refs use `provider/model` format (e.g. `anthropic/claude-opus-4-6`).
- **Control who can message the bot** — DM access is controlled per channel via `dmPolicy`: `"pairing"` (default; unknown senders get a one-time pairing code), `"allowlist"` (only `allowFrom` or the paired allow store), `"open"` (requires `allowFrom: ["*"]`), `"disabled"`. For groups use `groupPolicy` + `groupAllowFrom`.
- **Set up group chat mention gating** — group messages default to require-mention; configure `mentionPatterns` per agent and `messages.visibleReplies` / `messages.groupChat.visibleReplies` for visible reply modes.
- **Restrict skills per agent** — use `agents.defaults.skills` for a shared baseline, then override with `agents.list[].skills` (`[]` for no skills; omit to inherit).
- **Tune gateway channel health monitoring** — `gateway.channelHealthCheckMinutes` / `channelStaleEventThresholdMinutes` / `channelMaxRestartsPerHour`; set `channelHealthCheckMinutes: 0` to disable global health-monitor restarts.
- **Tune gateway WebSocket handshake timeout** — `gateway.handshakeTimeoutMs` (default `15000` ms); `OPENCLAW_HANDSHAKE_TIMEOUT_MS` takes precedence for one-off overrides.
- **Configure sessions and resets** — `session.dmScope` (`main | per-peer | per-channel-peer | per-account-channel-peer`), `session.threadBindings`, and `session.reset`.
- **Enable sandboxing** — `agents.defaults.sandbox.mode` (`off | non-main | all`) and `sandbox.scope` (`session | agent | shared`); build the image first via `scripts/sandbox-setup.sh` or the inline `docker build`.
- **Enable relay-backed push for official iOS builds** — defaults to the hosted relay `https://ios-push-relay.openclaw.ai`; override with `gateway.push.apns.relay.baseUrl`.
- **Set up heartbeat (periodic check-ins)** — `agents.defaults.heartbeat.every` (duration string; `0m` disables) and `target` (`last | none | <channel-id>`).
- **Configure cron jobs** — `cron.enabled`, `cron.maxConcurrentRuns`, `cron.sessionRetention`, `cron.runLog`.
- **Set up webhooks (hooks)** — `hooks.enabled`, `hooks.token`, `hooks.path`, `hooks.mappings`; treat all hook payloads as untrusted and use a dedicated `hooks.token`.
- **Configure multi-agent routing** — `agents.list[]` with per-agent `workspace`, plus `bindings[]` matching channel/account to `agentId`.
- **Split config into multiple files (`$include`)** — `$include` a single file (replaces the object) or an array (deep-merged in order); the `$include` deep surface is documented in `oc_gateway_config_reference_ops`.

The DM-policy pattern that every channel shares is shown verbatim in the source's first accordion:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",   // pairing | allowlist | open | disabled
      allowFrom: ["tg:123"], // only for allowlist/open
    },
  },
}
```

## Full reference (pointer)

For the complete field-by-field reference, the configuration page defers to **[Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)**. Here that reference is split by subsystem cluster across three companion notes: `oc_gateway_config_reference_runtime` (channels / agents / tools / models / MCP / skills / plugins / commitments), `oc_gateway_config_reference_platform` (browser / UI / gateway / hooks / canvas / discovery / environment), and `oc_gateway_config_reference_ops` (secrets / auth storage / logging / diagnostics / update / ACP / CLI / wizard / identity / cron / media template variables / `$include`). When config fails strict validation, the recovery path is `oc_gateway_doctor` (`openclaw doctor --fix`).

**Source**: OpenClaw documentation — `gateway/configuration` (mirror `inbox/openclaw_docs/gateway/configuration.md`)
**Last Updated**: 2026-06-22
**Status**: Active
