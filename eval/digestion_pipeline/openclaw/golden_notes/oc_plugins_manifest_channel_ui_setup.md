---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - manifest
keywords:
  - openclaw plugin manifest channel metadata
  - commandAliases activation qaRunners
  - setup providers authEvidence
  - uiHints config field hints
  - channelConfigs preferOver
  - activation onStartup onProviders onCommands
  - manifest control-plane metadata
  - replacing another channel plugin
topics:
  - OpenClaw
  - Plugin manifest
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/manifest
access_control_group: ["general"]
---

# OpenClaw — Plugin Manifest: Channel, UI, Activation, and Setup Metadata

## Overview

This note models the control-plane metadata blocks of the native OpenClaw plugin manifest (`openclaw.plugin.json`) describing how a plugin participates in command routing, activation planning, QA, onboarding/setup, config UI, and channel ownership — all read cheaply **before OpenClaw loads plugin code**. It documents the `commandAliases`, `activation`, `qaRunners`, `setup` (with `setup.providers` and the `setup` fields table), `uiHints`, and `channelConfigs` (including channel-plugin replacement via `preferOver`) field references, mirroring those sections of the `plugins/manifest` source page. These are declarative metadata fields: the manifest narrows and describes; plugin runtime still owns actual behavior.

## commandAliases reference

Use `commandAliases` when a plugin owns a runtime command name that users may mistakenly put in `plugins.allow` or run as a root CLI command. OpenClaw uses this for diagnostics without importing plugin runtime code.

```json
{
  "commandAliases": [
    {
      "name": "dreaming",
      "kind": "runtime-slash",
      "cliCommand": "memory"
    }
  ]
}
```

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `name` | Yes | `string` | Command name that belongs to this plugin. |
| `kind` | No | `"runtime-slash"` | Marks the alias as a chat slash command rather than a root CLI command. |
| `cliCommand` | No | `string` | Related root CLI command to suggest for CLI operations, if one exists. |

## activation reference

Use `activation` when the plugin can cheaply declare which control-plane events should include it in an activation/load plan. This block is planner metadata, not a lifecycle API: it does not register runtime behavior, does not replace `register(...)`, and does not promise plugin code has executed. The planner uses these fields to narrow candidate plugins before falling back to existing manifest ownership metadata (`providers`, `channels`, `commandAliases`, `setup.providers`, `contracts.tools`, hooks). Prefer the narrowest metadata that already describes ownership; use `activation` only for extra planner hints those fields cannot represent. Use top-level `cliBackends` for CLI runtime aliases such as `claude-cli`; `activation.onAgentHarnesses` is only for embedded agent harness ids that lack an ownership field.

Every plugin should set `activation.onStartup` intentionally; omitting it no longer startup-loads the plugin implicitly, so use explicit activation metadata for startup, channel, config, agent-harness, memory, or other narrower triggers. Because this block is metadata only, missing non-startup activation metadata usually only costs performance and should not change correctness while manifest ownership fallbacks exist.

```json
{
  "activation": {
    "onStartup": false,
    "onProviders": ["openai"],
    "onCommands": ["models"],
    "onChannels": ["web"],
    "onRoutes": ["gateway-webhook"],
    "onConfigPaths": ["browser"],
    "onCapabilities": ["provider", "tool"]
  }
}
```

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `onStartup` | No | `boolean` | Explicit Gateway startup activation. Every plugin should set this. `true` imports the plugin during startup; `false` keeps it startup-lazy unless another matched trigger requires loading. |
| `onProviders` | No | `string[]` | Provider ids that should include this plugin in activation/load plans. |
| `onAgentHarnesses` | No | `string[]` | Embedded agent harness runtime ids that should include this plugin in activation/load plans. Use top-level `cliBackends` for CLI backend aliases. |
| `onCommands` | No | `string[]` | Command ids that should include this plugin in activation/load plans. |
| `onChannels` | No | `string[]` | Channel ids that should include this plugin in activation/load plans. |
| `onRoutes` | No | `string[]` | Route kinds that should include this plugin in activation/load plans. |
| `onConfigPaths` | No | `string[]` | Root-relative config paths that should include this plugin in startup/load plans when the path is present and not explicitly disabled. |
| `onCapabilities` | No | `Array<"provider" \| "channel" \| "tool" \| "hook">` | Broad capability hints used by control-plane activation planning. Prefer narrower fields when possible. |

Current live consumers: Gateway startup planning uses `activation.onStartup`; command-triggered CLI planning falls back to legacy `commandAliases[].cliCommand`/`commandAliases[].name`; agent-runtime startup planning uses `activation.onAgentHarnesses` for embedded harnesses and top-level `cliBackends[]` for CLI aliases; channel- and provider-triggered planning fall back to legacy `channels[]` and `providers[]`/`cliBackends[]` ownership when explicit activation metadata is missing; and startup plugin planning uses `activation.onConfigPaths` for non-channel root config surfaces such as the bundled browser plugin's `browser` block. Planner diagnostics distinguish explicit activation hints from ownership fallback (`activation-command-hint` vs `manifest-command-alias`); these labels are for host diagnostics and tests, and authors should declare the metadata that best describes ownership.

## qaRunners reference

Use `qaRunners` when a plugin contributes transport runners beneath the shared `openclaw qa` root. Keep this metadata cheap and static; runtime still owns CLI registration through a lightweight `runtime-api.ts` surface exporting `qaRunnerCliRegistrations`.

```json
{
  "qaRunners": [
    {
      "commandName": "matrix",
      "description": "Run the Docker-backed Matrix live QA lane against a disposable homeserver"
    }
  ]
}
```

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `commandName` | Yes | `string` | Subcommand mounted beneath `openclaw qa`, for example `matrix`. |
| `description` | No | `string` | Fallback help text used when the shared host needs a stub command. |

## setup reference

Use `setup` when onboarding surfaces need cheap plugin-owned metadata before runtime loads. Top-level `cliBackends` describes CLI inference backends; `setup.cliBackends` is the setup-specific descriptor surface for control-plane/setup flows that stay metadata-only.

```json
{
  "setup": {
    "providers": [
      {
        "id": "openai",
        "authMethods": ["api-key"],
        "envVars": ["OPENAI_API_KEY"],
        "authEvidence": [
          {
            "type": "local-file-with-env",
            "fileEnvVar": "OPENAI_CREDENTIALS_FILE",
            "requiresAllEnv": ["OPENAI_PROJECT"],
            "credentialMarker": "openai-local-credentials",
            "source": "openai local credentials"
          }
        ]
      }
    ],
    "cliBackends": ["openai-cli"],
    "configMigrations": ["legacy-openai-auth"],
    "requiresRuntime": false
  }
}
```

`setup.providers` and `setup.cliBackends` are the preferred descriptor-first lookup surface for setup discovery. If the descriptor only narrows the candidate plugin and setup still needs richer runtime hooks, set `requiresRuntime: true` and keep `setup-api` as the fallback execution path. OpenClaw also includes `setup.providers[].envVars` in generic provider auth/env-var lookups; deprecated `providerAuthEnvVars` still works through a compatibility adapter but emits a manifest diagnostic for non-bundled plugins, so new plugins put setup/status env metadata on `setup.providers[].envVars`. OpenClaw can derive simple setup choices from `setup.providers[].authMethods` when no setup entry exists or when `setup.requiresRuntime: false`; explicit `providerAuthChoices` entries stay preferred for custom labels, CLI flags, onboarding scope, and assistant metadata.

Explicit `requiresRuntime: false` is a descriptor-only contract: OpenClaw will not execute `setup-api` or `openclaw.setupEntry`, reporting an additive diagnostic if a descriptor-only plugin still ships such an entry; omitting it keeps legacy fallback behavior. Because setup lookup can execute plugin-owned `setup-api` code, normalized `setup.providers[].id` and `setup.cliBackends[]` values must stay unique across discovered plugins; ambiguous ownership fails closed. When setup runtime executes, registry diagnostics additively report descriptor drift between `setup-api` registrations and manifest descriptors.

### setup.providers reference

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `id` | Yes | `string` | Provider id exposed during setup or onboarding. Keep normalized ids globally unique. |
| `authMethods` | No | `string[]` | Setup/auth method ids this provider supports without loading full runtime. |
| `envVars` | No | `string[]` | Env vars that generic setup/status surfaces can check before plugin runtime loads. |
| `authEvidence` | No | `object[]` | Cheap local auth evidence checks for providers that can authenticate through non-secret markers. |

`authEvidence` is for provider-owned local credential markers verifiable without loading runtime code. These checks must stay cheap and local: no network calls, no keychain or secret-manager reads, no shell commands, no provider API probes. Supported evidence entries:

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `type` | Yes | `string` | Currently `local-file-with-env`. |
| `fileEnvVar` | No | `string` | Env var containing an explicit credential file path. |
| `fallbackPaths` | No | `string[]` | Local credential file paths checked when `fileEnvVar` is absent or empty. Supports `${HOME}` and `${APPDATA}`. |
| `requiresAnyEnv` | No | `string[]` | At least one listed env var must be non-empty before the evidence is valid. |
| `requiresAllEnv` | No | `string[]` | Every listed env var must be non-empty before the evidence is valid. |
| `credentialMarker` | Yes | `string` | Non-secret marker returned when the evidence is present. |
| `source` | No | `string` | User-facing source label for auth/status output. |

### setup fields

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `providers` | No | `object[]` | Provider setup descriptors exposed during setup and onboarding. |
| `cliBackends` | No | `string[]` | Setup-time backend ids used for descriptor-first setup lookup. Keep normalized ids globally unique. |
| `configMigrations` | No | `string[]` | Config migration ids owned by this plugin's setup surface. |
| `requiresRuntime` | No | `boolean` | Whether setup still needs `setup-api` execution after descriptor lookup. |

## uiHints reference

`uiHints` maps config field names to small rendering hints — for example `uiHints.apiKey` with `label: "API key"`, `help: "Used for OpenRouter requests"`, `placeholder: "sk-or-v1-..."`, `sensitive: true`. Each field hint can include:

| Field | Type | What it means |
| --- | --- | --- |
| `label` | `string` | User-facing field label. |
| `help` | `string` | Short helper text. |
| `tags` | `string[]` | Optional UI tags. |
| `advanced` | `boolean` | Marks the field as advanced. |
| `sensitive` | `boolean` | Marks the field as secret or sensitive. |
| `placeholder` | `string` | Placeholder text for form inputs. |

## channelConfigs reference

Use `channelConfigs` when a channel plugin needs cheap config metadata before runtime loads; read-only channel setup/status discovery can use it directly for configured external channels when no setup entry exists or when `setup.requiresRuntime: false`. It is plugin manifest metadata, not a new top-level user config section — users still configure instances under `channels.<channel-id>`, and OpenClaw reads the manifest to decide which plugin owns that channel before runtime executes. The two schemas differ: `configSchema` validates `plugins.entries.<plugin-id>.config`, while `channelConfigs.<channel-id>.schema` validates `channels.<channel-id>`. Non-bundled plugins declaring `channels[]` should declare matching `channelConfigs` entries; without them cold-path config schema, setup, and Control UI surfaces cannot know the channel-owned option shape until runtime executes. The `channelConfigs.<channel-id>.commands.nativeCommandsAutoEnabled`/`nativeSkillsAutoEnabled` fields declare static `auto` defaults for command config checks before channel runtime loads; bundled channels can also publish the same defaults through `package.json#openclaw.channel.commands`.

```json
{
  "channelConfigs": {
    "matrix": {
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "homeserverUrl": { "type": "string" }
        }
      },
      "uiHints": {
        "homeserverUrl": {
          "label": "Homeserver URL",
          "placeholder": "https://matrix.example.com"
        }
      },
      "label": "Matrix",
      "description": "Matrix homeserver connection",
      "commands": {
        "nativeCommandsAutoEnabled": true,
        "nativeSkillsAutoEnabled": true
      },
      "preferOver": ["matrix-legacy"]
    }
  }
}
```

Each channel entry can include:

| Field | Type | What it means |
| --- | --- | --- |
| `schema` | `object` | JSON Schema for `channels.<id>`. Required for each declared channel config entry. |
| `uiHints` | `Record<string, object>` | Optional UI labels/placeholders/sensitive hints for that channel config section. |
| `label` | `string` | Channel label merged into picker and inspect surfaces when runtime metadata is not ready. |
| `description` | `string` | Short channel description for inspect and catalog surfaces. |
| `commands` | `object` | Static native command and native skill auto-defaults for pre-runtime config checks. |
| `preferOver` | `string[]` | Legacy or lower-priority plugin ids this channel should outrank in selection surfaces. |

### Replacing another channel plugin

Use `preferOver` when your plugin is the preferred owner for a channel id another plugin can also provide — a renamed plugin id, a standalone plugin superseding a bundled one, or a maintained fork that keeps the same channel id for config compatibility.

```json
{
  "id": "acme-chat",
  "channels": ["chat"],
  "channelConfigs": {
    "chat": {
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "webhookUrl": { "type": "string" }
        }
      },
      "preferOver": ["chat"]
    }
  }
}
```

When `channels.chat` is configured, OpenClaw considers both the channel id and the preferred plugin id. If the lower-priority plugin was selected only because it is bundled or enabled by default, OpenClaw disables it in the effective runtime config so one plugin owns the channel and its tools. Explicit user selection still wins: if the user enables both plugins, OpenClaw preserves that choice and reports duplicate channel/tool diagnostics instead of silently changing the plugin set. Keep `preferOver` scoped to plugin ids that can really provide the same channel — it is not a general priority field and does not rename config keys.

**Source**: OpenClaw documentation — `plugins/manifest` (mirror `inbox/openclaw_docs/plugins/manifest.md`), channel/UI/activation/setup/QA/commandAliases sections
**Last Updated**: 2026-06-22
**Status**: Active
