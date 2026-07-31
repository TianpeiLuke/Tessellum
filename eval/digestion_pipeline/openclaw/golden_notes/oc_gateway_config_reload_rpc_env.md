---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw config hot reload
  - reload modes hybrid hot restart off
  - hot-apply vs restart
  - reload planning include
  - config rpc config.patch config.apply
  - config.get config.schema.lookup
  - control-plane rate limit
  - openclaw environment variables
  - env var substitution
  - inline env vars config
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

# OpenClaw — Applying Config Changes at Runtime (Hot Reload, Config RPC, Env Vars)

## Overview

This note is the operate-while-running half of the OpenClaw `gateway/configuration` page: how a configuration change reaches the running Gateway after the JSON5 `~/.openclaw/openclaw.json` already exists. It covers the file-watcher hot-reload pipeline and its four reload modes, the table of what hot-applies versus what needs a restart, `$include`-aware reload planning, the programmatic Config RPC (`config.schema.lookup` / `config.get` / `config.patch` / `config.apply` / `update.run` / `update.status`) with its control-plane rate limits, and the environment-variable surface (`.env` files, inline `env`, `${VAR}` substitution, shell env import, SecretRef). The first-time-setup half of the same page — minimal config, the four edit paths, strict validation, and the common-task accordion — lives in the companion note `oc_gateway_configuration_overview`.

## Config hot reload

The Gateway watches `~/.openclaw/openclaw.json` and applies changes automatically — no manual restart is needed for most settings. Direct file edits are treated as untrusted until they validate: the watcher waits for editor temp-write/rename churn to settle, reads the final file, and rejects invalid external edits without rewriting `openclaw.json`. OpenClaw-owned config writes use the same schema gate before writing; destructive clobbers — such as dropping `gateway.mode` or shrinking the file by more than half — are rejected and saved as `.rejected.*` for inspection. If you see `config reload skipped (invalid config)` or startup reports `Invalid config`, inspect the config, run `openclaw config validate`, then run `openclaw doctor --fix` for repair (see Gateway troubleshooting for the checklist).

### Reload modes

The reload behavior is governed by `gateway.reload.mode`. There are four modes:

| Mode | Behavior |
| --- | --- |
| **`hybrid`** (default) | Hot-applies safe changes instantly. Automatically restarts for critical ones. |
| **`hot`** | Hot-applies safe changes only. Logs a warning when a restart is needed — you handle it. |
| **`restart`** | Restarts the Gateway on any config change, safe or not. |
| **`off`** | Disables file watching. Changes take effect on the next manual restart. |

The mode and a debounce window are set under `gateway.reload`:

```json5
{
  gateway: {
    reload: { mode: "hybrid", debounceMs: 300 },
  },
}
```

### What hot-applies vs what needs a restart

Most fields hot-apply without downtime. In `hybrid` mode, restart-required changes are handled automatically. The split by config category is:

| Category | Fields | Restart needed? |
| --- | --- | --- |
| Channels | `channels.*`, `web` (WhatsApp) — all built-in and plugin channels | No |
| Agent & models | `agent`, `agents`, `models`, `routing` | No |
| Automation | `hooks`, `cron`, `agent.heartbeat` | No |
| Sessions & messages | `session`, `messages` | No |
| Tools & media | `tools`, `browser`, `skills`, `mcp`, `audio`, `talk` | No |
| UI & misc | `ui`, `logging`, `identity`, `bindings` | No |
| Gateway server | `gateway.*` (port, bind, auth, tailscale, TLS, HTTP) | **Yes** |
| Infrastructure | `discovery`, `plugins` | **Yes** |

`gateway.reload` and `gateway.remote` are exceptions — changing them does **not** trigger a restart.

### Reload planning

When you edit a source file that is referenced through `$include`, OpenClaw plans the reload from the source-authored layout, not the flattened in-memory view. That keeps hot-reload decisions (hot-apply vs restart) predictable even when a single top-level section lives in its own included file such as `plugins: { $include: "./plugins.json5" }`. Reload planning fails closed if the source layout is ambiguous.

## Config RPC (programmatic updates)

For tooling that writes config over the gateway API, the preferred flow uses these RPC methods:

- `config.schema.lookup` — inspect one subtree (shallow schema node plus child summaries).
- `config.get` — fetch the current snapshot plus `hash`.
- `config.patch` — partial updates (JSON merge patch: objects merge, `null` deletes, arrays replace when explicitly confirmed with `replacePaths` if entries would be removed).
- `config.apply` — use only when you intend to replace the entire config.
- `update.run` — explicit self-update plus restart; include `continuationMessage` when the post-restart session should run one follow-up turn.
- `update.status` — inspect the latest update restart sentinel and verify the running version after a restart.

Agents should treat `config.schema.lookup` as the first stop for exact field-level docs and constraints, and use the Configuration reference when they need the broader config map, defaults, or links to dedicated subsystem references.

Control-plane writes (`config.apply`, `config.patch`, `update.run`) are rate-limited to **3 requests per 60 seconds per `deviceId+clientIp`**. Restart requests coalesce and then enforce a **30-second cooldown** between restart cycles. `update.status` is read-only but admin-scoped because the restart sentinel can include update step summaries and command output tails.

A partial patch is applied by first capturing `payload.hash` from `config.get`, then passing it as `baseHash`:

```bash
openclaw gateway call config.get --params '{}'  # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{ channels: { telegram: { groups: { \"*\": { requireMention: false } } } } }",
  "baseHash": "<hash>"
}'
```

Both `config.apply` and `config.patch` accept `raw`, `baseHash`, `sessionKey`, `note`, and `restartDelayMs`. `baseHash` is required for both methods when a config already exists. `config.patch` also accepts `replacePaths`, an array of config paths whose array replacement is intentional: if a patch would replace or delete an existing array with fewer entries, the Gateway rejects the write unless that exact path appears in `replacePaths`. Nested arrays under array entries use `[]`, such as `agents.list[].skills`. This prevents truncated `config.get` snapshots from silently clobbering routing or allowlist arrays. Use `config.apply` when you intend to replace the full config.

## Environment variables

OpenClaw reads env vars from the parent process plus two files: `.env` from the current working directory (if present), and `~/.openclaw/.env` (global fallback). Neither file overrides existing env vars. You can also set inline env vars in config under `env` (a flat key plus a `vars` map):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

**Shell env import (optional).** If enabled and expected keys aren't set, OpenClaw runs your login shell and imports only the missing keys via `env.shellEnv` (`{ enabled: true, timeoutMs: 15000 }`). The env-var equivalent is `OPENCLAW_LOAD_SHELL_ENV=1`.

**Env var substitution in config values.** Reference env vars in any config string value with `${VAR_NAME}`, for example `gateway.auth.token: "${OPENCLAW_GATEWAY_TOKEN}"` or `models.providers.custom.apiKey: "${CUSTOM_API_KEY}"`. The substitution rules are: only uppercase names matched (`[A-Z_][A-Z0-9_]*`); missing/empty vars throw an error at load time; escape with `$${VAR}` for literal output; substitution works inside `$include` files; and inline substitution composes, e.g. `"${BASE}/v1"` → `"https://api.example.com/v1"`.

**Secret refs (env, file, exec).** For fields that support SecretRef objects, the value is an object with `source`, `provider`, and `id` — `source` is one of `env`, `file`, or `exec`:

```json5
{
  models: {
    providers: {
      openai: { apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" } },
    },
  },
  channels: {
    googlechat: {
      serviceAccountRef: {
        source: "exec",
        provider: "vault",
        id: "channels/googlechat/serviceAccount",
      },
    },
  },
}
```

SecretRef details (including `secrets.providers` for `env`/`file`/`exec`) live in the Secrets Management reference, and supported credential paths are listed in the SecretRef Credential Surface reference; see the Environment help page for full precedence and sources.

**Source**: OpenClaw documentation — `gateway/configuration` (mirror `inbox/openclaw_docs/gateway/configuration.md`), sections "Config hot reload", "Config RPC (programmatic updates)", "Environment variables"
**Last Updated**: 2026-06-22
**Status**: Active
