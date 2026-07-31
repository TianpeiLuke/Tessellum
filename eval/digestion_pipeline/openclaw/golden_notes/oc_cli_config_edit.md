---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - config
keywords:
  - openclaw config set
  - openclaw config patch
  - config schema
  - secretref builder mode
  - provider builder mode
  - config get unset
  - openclaw.json edit
  - dot bracket path
  - strict-json merge replace
  - config file path
topics:
  - OpenClaw
  - CLI Config Editing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/config
access_control_group: ["general"]
---

# OpenClaw — `config` Non-Interactive Editing of `openclaw.json`

## Overview

This note covers the editing half of `openclaw config`, the non-interactive command for getting, setting, patching, unsetting, and inspecting values in `openclaw.json` by path. It mirrors the `cli/config` source page sections for root options, examples, `config schema`, paths, values, the four `config set` modes, `config patch`, provider-builder flags, and the `config file` subcommand — the editing-operations surface every operator change flows through. The validation, dry-run reporting, and write-safety half of the same page (`--dry-run` JSON report, `config validate`, write-safety / `.rejected.*`, the TUI repair loop) is documented in the sibling note **oc_cli_config_validate**; this note links those points rather than re-documenting them. Running `openclaw config` with no subcommand opens the configure wizard (same as `openclaw configure`).

## Nix-mode immutability

When the environment variable `OPENCLAW_NIX_MODE=1` is set, OpenClaw treats `openclaw.json` as immutable. Read-only commands such as `config get`, `config file`, `config schema`, and `config validate` still work, but config writers (`config set`, `config patch`, `config unset`) refuse. Agents should edit the Nix source for the install instead; for the first-party nix-openclaw distribution, set values under `programs.openclaw.config` or `instances.<name>.config`.

## Root options

`--section <section>` is a repeatable guided-setup section filter that applies when you run `openclaw config` without a subcommand (which opens the configure wizard). The supported guided sections are `workspace`, `model`, `web`, `gateway`, `daemon`, `channels`, `plugins`, `skills`, and `health`. Pass `--section` more than once to drive multiple guided sections in one run.

## Examples

The page's representative example set, copied verbatim, exercises every editing surface — `config file`, the guided `--section` wizard, `config schema`, `config get`/`set`, bracket-indexed agent paths, JSON5 values with `--strict-json --merge`, SecretRef-builder and provider-builder modes, `config patch`, and `config unset`.

```bash
openclaw config file
openclaw config --section model
openclaw config --section gateway --section daemon
openclaw config schema
openclaw config get browser.executablePath
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set browser.profiles.work.executablePath "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config set 'agents.list[0].tools.exec.node' "node-id-or-name"
openclaw config set agents.defaults.models '{"openai/gpt-5.4":{}}' --strict-json --merge
openclaw config set channels.discord.token --ref-provider default --ref-source env --ref-id DISCORD_BOT_TOKEN
openclaw config set secrets.providers.vaultfile --provider-source file --provider-path /etc/openclaw/secrets.json --provider-mode json
openclaw config patch --file ./openclaw.patch.json5 --dry-run
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

### `config schema`

`openclaw config schema` prints the generated JSON schema for `openclaw.json` to stdout as JSON. The emitted schema includes: the current root config schema plus a root `$schema` string field for editor tooling; field `title` and `description` docs metadata used by the Control UI; nested object, wildcard (`*`), and array-item (`[]`) nodes that inherit the same `title` / `description` metadata when matching field documentation exists; `anyOf` / `oneOf` / `allOf` branches that inherit the same docs metadata too when matching field documentation exists; best-effort live plugin + channel schema metadata when runtime manifests can be loaded; and a clean fallback schema even when the current config is invalid. Pipe it into a file to inspect or validate it with other tools (`openclaw config schema > openclaw.schema.json`). For path-scoped drill-down (in Control UI or custom clients), the related runtime RPC `config.schema.lookup` returns one normalized config path with a shallow schema node (`title`, `description`, `type`, `enum`, `const`, common bounds), matched UI hint metadata, and immediate child summaries.

### Paths

Paths use dot or bracket notation. Quote bracket-notation paths in shell examples so shells such as zsh do not expand `[0]` as a glob before OpenClaw receives the path. Use the agent list index to target a specific agent:

```bash
openclaw config get agents.defaults.workspace
openclaw config get 'agents.list[0].id'
openclaw config get agents.list
openclaw config set 'agents.list[1].tools.exec.node' "node-id-or-name"
```

## Values

Values are parsed as JSON5 when possible; otherwise they are treated as strings. Use `--strict-json` to require JSON5 parsing; `--json` remains supported as a legacy alias. `config get <path> --json` prints the raw value as JSON instead of terminal-formatted text. Object assignment replaces the target path by default. Protected map/list paths that commonly hold user-added entries — `agents.defaults.models`, `models.providers`, `models.providers.<id>.models`, `plugins.entries`, and `auth.profiles` — refuse replacements that would remove existing entries unless you pass `--replace`. Use `--merge` when adding entries to those maps, and use `--replace` only when you intentionally want the provided value to become the complete target value.

```bash
openclaw config set gateway.port 19001 --strict-json
openclaw config set channels.whatsapp.groups '["*"]' --strict-json
openclaw config set agents.defaults.models '{"openai/gpt-5.4":{}}' --strict-json --merge
openclaw config set models.providers.ollama.models '[{"id":"llama3.2","name":"Llama 3.2"}]' --strict-json --merge
```

## `config set` modes

`openclaw config set` supports four assignment styles. **Value mode** is `openclaw config set <path> <value>`. **SecretRef builder mode** writes a credential reference (instead of a plaintext secret) using `--ref-provider`, `--ref-source`, and `--ref-id`. **Provider builder mode** targets `secrets.providers.<alias>` paths only and uses the `--provider-*` flags. **Batch mode** applies many operations from a JSON payload via `--batch-json` or `--batch-file`; batch parsing always uses the batch payload as the source of truth, and `--strict-json` / `--json` do not change batch parsing behavior. JSON path/value mode also remains supported for both SecretRefs and providers (pass the full ref/provider object as a `--strict-json` value).

```bash
openclaw config set channels.discord.token \
  --ref-provider default \
  --ref-source env \
  --ref-id DISCORD_BOT_TOKEN

openclaw config set --batch-json '[
  {
    "path": "secrets.providers.default",
    "provider": { "source": "env" }
  },
  {
    "path": "channels.discord.token",
    "ref": { "source": "env", "provider": "default", "id": "DISCORD_BOT_TOKEN" }
  }
]'
openclaw config set --batch-file ./config-set.batch.json --dry-run
```

SecretRef assignments are rejected on unsupported runtime-mutable surfaces (for example `hooks.token`, `commands.ownerDisplaySecret`, Discord thread-binding webhook tokens, and WhatsApp creds JSON); keep SecretRefs on supported surfaces only (see the SecretRef Credential Surface reference).

## `config patch`

Use `config patch` when you want to paste or pipe a config-shaped patch instead of running many path-based `config set` commands. The input is a JSON5 object: objects merge recursively, arrays and scalar values replace the target value, and `null` deletes the target path. You can supply the patch via `--file`, or pipe it over stdin with `--stdin` (useful for remote setup scripts, e.g. `ssh openclaw-host 'openclaw config patch --stdin' < ./openclaw.patch.json5`). Use `--replace-path <path>` when one object or array must become exactly the provided value instead of being recursively patched (for example `openclaw config patch --file ./discord.patch.json5 --replace-path 'channels.discord.guilds["123"].channels'`). The `config patch` `--dry-run` / `--allow-exec` resolvability behavior is shared with `config set` and documented in **oc_cli_config_validate**.

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "socket",
      botToken: { source: "env", provider: "default", id: "SLACK_BOT_TOKEN" },
      appToken: { source: "env", provider: "default", id: "SLACK_APP_TOKEN" },
      groupPolicy: "open",
      requireMention: false,
    },
    discord: {
      enabled: true,
      token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN" },
      dmPolicy: "disabled",
      dm: { enabled: false },
      groupPolicy: "allowlist",
    },
  },
  agents: {
    defaults: {
      model: { primary: "openai/gpt-5.5" },
      models: {
        "openai/gpt-5.5": { params: { fastMode: true } },
      },
    },
  },
}
```

## Provider builder flags

Provider builder targets must use `secrets.providers.<alias>` as the path. The common flags apply across sources, and each source (`env`, `file`, `exec`) adds its own flags.

- Common: `--provider-source <env|file|exec>`; `--provider-timeout-ms <ms>` (`file`, `exec`).
- Env provider (`--provider-source env`): `--provider-allowlist <ENV_VAR>` (repeatable).
- File provider (`--provider-source file`): `--provider-path <path>` (required); `--provider-mode <singleValue|json>`; `--provider-max-bytes <bytes>`; `--provider-allow-insecure-path`.
- Exec provider (`--provider-source exec`): `--provider-command <path>` (required); `--provider-arg <arg>` (repeatable); `--provider-no-output-timeout-ms <ms>`; `--provider-max-output-bytes <bytes>`; `--provider-json-only`; `--provider-env <KEY=VALUE>` (repeatable); `--provider-pass-env <ENV_VAR>` (repeatable); `--provider-trusted-dir <path>` (repeatable); `--provider-allow-insecure-path`; `--provider-allow-symlink-command`.

```bash
openclaw config set secrets.providers.vault \
  --provider-source exec \
  --provider-command /usr/local/bin/openclaw-vault \
  --provider-arg read \
  --provider-arg openai/api-key \
  --provider-json-only \
  --provider-pass-env VAULT_TOKEN \
  --provider-trusted-dir /usr/local/bin \
  --provider-timeout-ms 5000
```

## Subcommands — `config file`

`config file` prints the active config file path, resolved from `OPENCLAW_CONFIG_PATH` or the default location. The path should name a regular file, not a symlink. Restart the gateway after edits.

**Source**: OpenClaw documentation — `cli/config` (mirror `inbox/openclaw_docs/cli/config.md`)
**Last Updated**: 2026-06-22
**Status**: Active
