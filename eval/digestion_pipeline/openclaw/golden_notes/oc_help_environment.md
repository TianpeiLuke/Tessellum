---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - environment
keywords:
  - openclaw environment variables
  - env var precedence
  - workspace .env credentials ignored
  - OPENCLAW_HOME state dir config path
  - config env block json5
  - shell env import shellEnv
  - secret ref vs ${ENV} substitution
  - nvm NODE_EXTRA_CA_CERTS tls
  - legacy CLAWDBOT MOLTBOT prefixes
topics:
  - OpenClaw
  - Environment Variables
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/environment
access_control_group: ["general"]
---

# OpenClaw — Loading Environment Variables and Precedence

## Overview

This note is the operational procedure for how the OpenClaw Gateway loads environment variables: the five-source precedence chain (highest → lowest), why workspace `.env` is a lower-trust source, the config `env` block, login-shell import, exec shell snapshots, runtime-injected markers, UI palette vars, `${ENV}` substitution vs SecretRef objects, the path-related vars (including `OPENCLAW_HOME`), logging-diagnostic vars, the nvm `web_fetch` TLS fix, and the silently-ignored legacy prefixes. It mirrors the `help/environment` source page and covers every H2/H3 the sub-plan's coverage map assigns to this note. The governing rule throughout is **never override existing values** — each lower source fills only keys still missing.

## Precedence (highest → lowest)

OpenClaw pulls env vars from multiple sources and never overrides a value already set by a higher source. The order is:

1. **Process environment** — what the Gateway process already has from the parent shell/daemon.
2. **`.env` in the current working directory** — dotenv default; does not override; provider credentials and protected runtime controls are ignored from this workspace `.env`.
3. **Global `.env`** at `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`; recommended for provider API keys; does not override).
4. **Config `env` block** in `~/.openclaw/openclaw.json` — applied only if missing.
5. **Optional login-shell import** (`env.shellEnv.enabled` or `OPENCLAW_LOAD_SHELL_ENV=1`) — applied only for missing expected keys.

On Ubuntu fresh installs that use the default state dir, OpenClaw also treats `~/.config/openclaw/gateway.env` as a compatibility fallback *after* the global `.env`; if both files exist and disagree, OpenClaw keeps `~/.openclaw/.env` and prints a warning. If the config file is missing entirely, step 4 is skipped while shell import still runs if enabled.

## Provider credentials and workspace `.env`

Do not keep provider API keys only in a workspace `.env`: OpenClaw ignores provider credential environment variables from workspace `.env` files, including `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `PERPLEXITY_API_KEY`, `BRAVE_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY`, and `FIRECRAWL_API_KEY`. Use a trusted source instead: the Gateway process environment (shell, launchd/systemd unit, container secret, or CI secret); the global runtime dotenv at `~/.openclaw/.env` or `$OPENCLAW_STATE_DIR/.env`; the config `env` block in `~/.openclaw/openclaw.json`; or the optional login-shell import. If you previously stored keys only in a workspace `.env`, move them to one of those sources. Workspace `.env` may still provide ordinary project variables that are not credentials, endpoint redirects, host overrides, or `OPENCLAW_*` runtime controls.

## Config `env` block

The config `env` block has two equivalent, non-overriding ways to set inline env vars, and it accepts **literal string values only** — it does not expand `file:...` values (e.g. `XAI_API_KEY: "file:secrets/xai-api-key.txt"` is passed to providers as that exact string):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

For file-backed provider keys, use a SecretRef on the credential field that supports it (the `env` block itself does not resolve SecretRefs or `file:...` shorthand):

```json5
{
  secrets: {
    providers: {
      xai_key_file: {
        source: "file",
        path: "~/.openclaw/secrets/xai-api-key.txt",
        mode: "singleValue",
      },
    },
  },
  models: {
    providers: {
      xai: {
        apiKey: { source: "file", provider: "xai_key_file", id: "value" },
      },
    },
  },
}
```

## Shell env import

`env.shellEnv` runs your login shell and imports only **missing** expected keys; the equivalent env vars are `OPENCLAW_LOAD_SHELL_ENV=1` and `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`:

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

## Exec shell snapshots

On non-Windows Gateway hosts, bash and zsh `exec` commands use a startup snapshot by default. Set `OPENCLAW_EXEC_SHELL_SNAPSHOT=0` in the Gateway process environment to disable this path; the values `false`, `no`, and `off` also disable it. Per-call `exec.env` values cannot toggle snapshots or redirect the snapshot cache.

## Runtime-injected env vars

OpenClaw injects context markers into spawned child processes (runtime markers, not required user config — usable in shell/profile logic to apply context-specific rules): `OPENCLAW_SHELL=exec` for commands run through the `exec` tool; `OPENCLAW_SHELL=acp` for ACP runtime backend process spawns (e.g. `acpx`); `OPENCLAW_SHELL=acp-client` for `openclaw acp client` when it spawns the ACP bridge process; `OPENCLAW_SHELL=tui-local` for local TUI `!` shell commands; and `OPENCLAW_CLI=1` for child processes spawned by the CLI entry point.

## UI env vars

`OPENCLAW_THEME=light` forces the light TUI palette (use when your terminal has a light background) and `OPENCLAW_THEME=dark` forces the dark palette; if your terminal exports `COLORFGBG`, OpenClaw uses that background-color hint to auto-pick the TUI palette.

## Env var substitution in config

You can reference env vars directly in config string values using `${VAR_NAME}` syntax — for example pointing a provider `apiKey` at `${VERCEL_GATEWAY_API_KEY}`:

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

## Secret refs vs `${ENV}` strings

OpenClaw supports two env-driven patterns, both resolving from process env at activation time: `${VAR}` string substitution in config values, and SecretRef objects (`{ source: "env", provider: "default", id: "VAR" }`) for fields that support secrets references. The config `env` block itself does not resolve SecretRefs or `file:...` shorthand values.

## Path-related env vars

| Variable | Purpose |
| --- | --- |
| `OPENCLAW_HOME` | Override the home directory used for internal OpenClaw path defaults (`~/.openclaw/`, agent dirs, sessions, credentials, installer onboarding, and the default dev checkout). Useful when running OpenClaw as a dedicated service user. |
| `OPENCLAW_STATE_DIR` | Override the state directory (default `~/.openclaw`). |
| `OPENCLAW_CONFIG_PATH` | Override the config file path (default `~/.openclaw/openclaw.json`). |
| `OPENCLAW_INCLUDE_ROOTS` | Path-list of directories where `$include` directives may resolve files outside the config directory (default: none — `$include` is confined to the config dir). Tilde-expanded. |

### `OPENCLAW_HOME`

When set, `OPENCLAW_HOME` replaces the system home directory (`$HOME` / `os.homedir()`) for internal OpenClaw path defaults: the default state directory, config path, agent directories, credentials, installer onboarding workspace, and the default dev checkout used by `openclaw update --channel dev`. Its precedence is `OPENCLAW_HOME` > `$HOME` > `USERPROFILE` > Termux `PREFIX` home fallback on Android > `os.homedir()`. It can be a tilde path (e.g. `~/svc`), expanded using the same OS home fallback chain before use. A macOS LaunchDaemon sets it via the plist `EnvironmentVariables` dict (`<key>OPENCLAW_HOME</key><string>/Users/user</string>`). Explicit path variables such as `OPENCLAW_STATE_DIR`, `OPENCLAW_CONFIG_PATH`, and `OPENCLAW_GIT_DIR` still take precedence over `OPENCLAW_HOME`; OS-account tasks such as shell startup file detection, package-manager setup, and host `~` expansion may still use the real system home.

## Logging

| Variable | Purpose |
| --- | --- |
| `OPENCLAW_LOG_LEVEL` | Override log level for both file and console (e.g. `debug`, `trace`). Takes precedence over `logging.level` and `logging.consoleLevel` in config. Invalid values are ignored with a warning. |
| `OPENCLAW_DEBUG_MODEL_TRANSPORT` | Emit targeted model request/response timing diagnostics at `info` level without enabling global debug logs. |
| `OPENCLAW_DEBUG_MODEL_PAYLOAD` | Model payload diagnostics: `summary`, `tools`, or `full-redacted`. `full-redacted` is capped and redacted but may include prompt/message text. |
| `OPENCLAW_DEBUG_SSE` | Streaming diagnostics: `events` for first/done timing, `peek` to include the first five redacted SSE events. |
| `OPENCLAW_DEBUG_CODE_MODE` | Code-mode model-surface diagnostics, including provider-tool hiding and exec/wait-only enforcement. |

## nvm users: web_fetch TLS failures

If Node.js was installed via **nvm** (not the system package manager), the built-in `fetch()` uses nvm's bundled CA store, which may be missing modern root CAs (ISRG Root X1/X2 for Let's Encrypt, DigiCert Global Root G2, etc.), causing `web_fetch` to fail with `"fetch failed"` on most HTTPS sites. On Linux, OpenClaw automatically detects nvm and applies the fix in the actual startup environment: `openclaw gateway install` writes `NODE_EXTRA_CA_CERTS` into the systemd service environment, and the `openclaw` CLI entrypoint re-execs itself with `NODE_EXTRA_CA_CERTS` set before Node startup. For older versions or direct `node ...` launches, export the variable manually before starting OpenClaw — do not rely on writing only to `~/.openclaw/.env`, because Node reads `NODE_EXTRA_CA_CERTS` at process startup:

```bash
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
openclaw gateway run
```

## Legacy environment variables

OpenClaw only reads `OPENCLAW_*` environment variables; the legacy `CLAWDBOT_*` and `MOLTBOT_*` prefixes from earlier releases are silently ignored. If any are still set on the Gateway process at startup, OpenClaw emits a single Node deprecation warning (`OPENCLAW_LEGACY_ENV_VARS`) listing the detected prefixes and the total count. Rename each value by replacing the legacy prefix with `OPENCLAW_` (for example `CLAWDBOT_GATEWAY_TOKEN` → `OPENCLAW_GATEWAY_TOKEN`); the old names take no effect.

**Source**: OpenClaw documentation — `help/environment` (mirror `inbox/openclaw_docs/help/environment.md`)
**Last Updated**: 2026-06-22
**Status**: Active
