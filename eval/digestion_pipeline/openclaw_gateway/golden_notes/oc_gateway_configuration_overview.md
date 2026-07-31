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

For the complete field-by-field reference, the configuration page defers to **[Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)**. In this vault that reference is split by subsystem cluster across three companion notes: `oc_gateway_config_reference_runtime` (channels / agents / tools / models / MCP / skills / plugins / commitments), `oc_gateway_config_reference_platform` (browser / UI / gateway / hooks / canvas / discovery / environment), and `oc_gateway_config_reference_ops` (secrets / auth storage / logging / diagnostics / update / ACP / CLI / wizard / identity / cron / media template variables / `$include`). When config fails strict validation, the recovery path is `oc_gateway_doctor` (`openclaw doctor --fix`).

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the self-hosted gateway product; relevance: the product being configured via `~/.openclaw/openclaw.json`.
- **[JSON Schema](../../term_dictionary/term_json_schema.md)** — schema-validation standard; relevance: strict validation / `openclaw config schema` rejects unknown keys.
- **[Structured Output](../../term_dictionary/term_structured_output.md)** — schema-constrained output; relevance: the JSON5 config is a schema-validated structured document.
- **[Agentic Workflow](../../term_dictionary/term_agentic_workflow.md)** — agent-driven task flow; relevance: config drives the agent's behavior/channels/tools.
- **[Chatbot](../../term_dictionary/term_chatbot.md)** — conversational bot; relevance: `channels.*`/`allowFrom` control who can message the bot.
- **[Cron](../../term_dictionary/term_cron.md)** — scheduled jobs; relevance: automation config (`cron`/`hooks`) is a common-task accordion item.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolated execution; relevance: sandboxing is a top-level config concern in the overview.
- **[Access Control](../../term_dictionary/term_access_control.md)** — authorization policy; relevance: `allowFrom`/who-can-message is the core access policy set here.

**Docs**

- **[Claude Code — Settings Files](../claude_code/cc_settings_files.md)** — settings file locations + precedence; relevance: analog to `~/.openclaw/openclaw.json` + the edit-paths model.
- **[Claude Code — Settings Reference](../claude_code/cc_settings_reference.md)** — full settings field map; relevance: the "full reference" pointer this overview defers to.
- **[Claude Code — Debug Your Configuration](../claude_code/cc_debug_your_configuration.md)** — diagnosing bad config; relevance: parallels "validation fails → run doctor" recovery path.
- **[Claude Code — Server-Managed Settings](../claude_code/cc_server_managed_settings.md)** — managed/locked config; relevance: strict-schema/managed-config posture analog.
- **[Hermes — Config Files Precedence](../hermes_agent/hermes_config_files_precedence.md)** — config layering/precedence; relevance: the edit-paths (wizard/CLI/UI/direct) + precedence model.
- **[Pi — Settings Reference](../pi/pi_settings_reference.md)** — settings reference; relevance: cross-tool full-reference analog.
- **[oc_gateway_config_reload_rpc_env](oc_gateway_config_reload_rpc_env.md)** — runtime-edit companion (planned, this series); relevance: the operate-while-running half of configuration.md.
- **[oc_gateway_configuration_examples](oc_gateway_configuration_examples.md)** — copy-paste recipes (planned, this series); relevance: the worked configs that realize this overview.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — runtime field reference (planned, this series); relevance: the "full reference" the overview points to.
- **[oc_gateway_doctor](oc_gateway_doctor.md)** — repair/migration tool (planned, this series); relevance: `doctor --fix` repairs configs that fail strict validation.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: loads/validates `~/.openclaw/openclaw.json` and refuses to start on schema failure.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: the config surface + JSON Schema source.
- **[repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md)** — onboarding/config wizard; relevance: `openclaw onboard`/`configure` interactive edit path.

**Snippets**

- **[snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md)** — wizard-driven config write; relevance: the interactive edit path this overview lists.
- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — runtime config assembly; relevance: how the validated config becomes runtime state.
- **[snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md)** — config validation command; relevance: analog of `openclaw config validate`/strict-schema refusal.
- **[snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md)** — startup auth/config load; relevance: the refuse-to-start-on-invalid-config behavior.
- **[snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md)** — CLI command routing; relevance: routes `config get/set/unset` one-liner edit path.
- **[snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md)** — schema group definitions; relevance: the `config.schema.lookup` schema surface Control UI renders.
- **[snippet_example_engine_agent_config_builder](../../code_snippets/snippet_example_engine_agent_config_builder.md)** — config builder; relevance: cross-engine view of building a validated agent config.
- **[snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md)** — config migration; relevance: the legacy-config path doctor handles when validation fails.
- **[snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md)** — wizard import flow; relevance: importing existing config into the validated wizard model.
- **[snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md)** — apply config changes; relevance: how a direct edit is validated then applied (links to note 4).

## References

- [OpenClaw Docs — Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Docs — Configuration examples](https://docs.openclaw.ai/gateway/configuration-examples)
- [OpenClaw Docs — Doctor](https://docs.openclaw.ai/gateway/doctor)
- [OpenClaw Docs — Environment](https://docs.openclaw.ai/help/environment)

**Source**: OpenClaw documentation — `gateway/configuration` (mirror `inbox/openclaw_docs/gateway/configuration.md`)
**Last Updated**: 2026-06-22
**Status**: Active
