---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - secrets
keywords:
  - openclaw secrets audit configure apply
  - secretref provider config env file exec
  - file-backed api key singlevalue json pointer
  - exec integration 1password vault bws sops pass
  - mcp server environment variables secretinput
  - sandbox ssh auth material identitydata
  - command-path resolution secrets.resolve
  - gateway auth surface diagnostics
topics:
  - OpenClaw
  - Secrets Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/secrets
access_control_group: ["general"]
---

# OpenClaw — Operating Secrets: Audit, Configure, and Provider Wiring

## Overview

This note is the operational procedure for running OpenClaw secrets in production: the `openclaw secrets audit` / `configure` / `apply` workflow, gateway-auth-surface diagnostics, onboarding-reference preflight, wiring SecretRefs into `secrets.providers` and provider `apiKey` config, file-backed API keys, exec-provider integration (1Password, Bitwarden `bws`, HashiCorp Vault, `sops`, `pass`), MCP-server env vars, sandbox SSH auth material, command-path resolution, and the Web UI note. It mirrors the operational half of the `gateway/secrets` source page; the runtime model and SecretRef contract (eager snapshot, active-surface filtering, precedence, one-way safety) are the model-BB companion **[oc_gateway_secrets_contract](oc_gateway_secrets_contract.md)** this procedure enacts.

## Gateway auth surface diagnostics

When a SecretRef is configured on `gateway.auth.token`, `gateway.auth.password`, `gateway.remote.token`, or `gateway.remote.password`, gateway startup/reload logs the surface state explicitly. The two states are: `active` — the SecretRef is part of the effective auth surface and must resolve; and `inactive` — the SecretRef is ignored for this runtime because another auth surface wins, or because remote auth is disabled/not active. These entries are logged with `SECRETS_GATEWAY_AUTH_SURFACE` and include the active-surface-policy reason, so you can see why a credential was treated as active or inactive (for example, `gateway.auth.token` is inactive for startup auth resolution when `OPENCLAW_GATEWAY_TOKEN` is set, because env token input wins for that runtime).

## Onboarding reference preflight

When onboarding runs in interactive mode and you choose SecretRef storage, OpenClaw runs preflight validation before saving. Env refs validate the env var name and confirm a non-empty value is visible during setup. Provider refs (`file` or `exec`) validate the provider selection, resolve `id`, and check the resolved value type. On the quickstart reuse path, when `gateway.auth.token` is already a SecretRef, onboarding resolves it before probe/dashboard bootstrap (for `env`, `file`, and `exec` refs) using the same fail-fast gate. If validation fails, onboarding shows the error and lets you retry.

## Provider config

Define providers under `secrets.providers`. Each provider has a `source` (`env`/`file`/`exec`) and source-specific fields; `defaults` maps each source to a default provider, and `resolution` bounds concurrency and batch size.

```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json", // or "singleValue"
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        args: ["--profile", "prod"],
        passEnv: ["PATH", "VAULT_ADDR"],
        jsonOnly: true,
      },
      "team-secrets": {
        source: "exec",
        pluginIntegration: {
          pluginId: "acme-secrets",
          integrationId: "secret-store",
        },
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
    resolution: {
      maxProviderConcurrency: 4,
      maxRefsPerProvider: 512,
      maxBatchBytes: 262144,
    },
  },
}
```

Per-source behavior: the **Env provider** takes an optional `allowlist`, and missing/empty env values fail resolution. The **File provider** reads a local file from `path`; `mode: "json"` expects a JSON object payload and resolves `id` as a pointer, `mode: "singleValue"` expects ref id `"value"` and returns the file contents; the path must pass ownership/permission checks. The **Exec provider** runs the configured absolute binary path with no shell; by default `command` must point to a regular file (not a symlink), but `allowSymlinkCommand: true` allows symlink command paths (e.g. Homebrew shims, validated against the resolved target) and should be paired with `trustedDirs` (e.g. `["/opt/homebrew"]`). Exec supports timeout, no-output timeout, output byte limits, env allowlist, and trusted dirs. Plugin-managed exec providers can use `pluginIntegration` instead of copied `command`/`args`; OpenClaw resolves the command details from the installed plugin manifest at startup/reload, and active SecretRefs fail closed if the plugin is disabled, removed, untrusted, or no longer declares the integration. On Windows both file and exec providers fail closed when ACL verification is unavailable; for trusted paths only, set `allowInsecurePath: true` to bypass path security checks.

The exec provider speaks a request/response protocol over stdin/stdout. Request (stdin): `{ "protocolVersion": 1, "provider": "vault", "ids": ["providers/openai/apiKey"] }`; response (stdout): `{ "protocolVersion": 1, "values": { "providers/openai/apiKey": "<openai-api-key>" } }`. Optional per-id errors are returned under an `errors` map, e.g. `{ "protocolVersion": 1, "values": {}, "errors": { "providers/openai/apiKey": { "message": "not found" } } }`.

## File-backed API keys

Do not put `file:...` strings in the config `env` block — the `env` block is literal and non-overriding, so `file:...` is not resolved. Use a file SecretRef on a supported credential field instead: define a `file` provider with `mode: "singleValue"` for the key file, then reference it from the field.

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

For `mode: "singleValue"`, the SecretRef `id` is `"value"`; for `mode: "json"`, use an absolute JSON pointer such as `"/providers/xai/apiKey"`. The canonical list of config fields that accept SecretRefs is the SecretRef Credential Surface reference (see References).

## Exec integration examples

The source page documents five exec-provider integrations. Each defines an `exec` provider under `secrets.providers` and points a `models.providers.<id>.apiKey` at it via a SecretRef.

- **1Password CLI (`op`)**: `command: "/opt/homebrew/bin/op"` with `allowSymlinkCommand: true` (required for Homebrew symlinked binaries), `trustedDirs: ["/opt/homebrew"]`, `args: ["read", "op://Personal/OpenClaw QA API Key/password"]`, `passEnv: ["HOME"]`, `jsonOnly: false`; the `apiKey` ref uses `id: "value"`.
- **Bitwarden Secrets Manager (`bws`)**: use a resolver wrapper so SecretRef ids map to Bitwarden item keys; the repo ships `scripts/secrets/openclaw-bws-resolver.mjs`, installed to an absolute trusted path. Requirements: the `bws` CLI on the Gateway host, `BWS_ACCESS_TOKEN` available to the service, `PATH` passed (or `BWS_BIN` set to the absolute `bws` path), and `BWS_SERVER_URL` set for self-hosted Bitwarden. The provider sets `command: "/usr/local/bin/openclaw-bws-resolver.mjs"`, `passEnv: ["BWS_ACCESS_TOKEN", "BWS_SERVER_URL", "PATH", "BWS_BIN"]`, `jsonOnly: true`; the `apiKey` id uses an exec-contract-valid key such as `openclaw/providers/openai/apiKey`. The resolver batches ids, runs `bws secret list`, returns values for matching secret `key` fields; env-var-style keys with underscores are rejected, and a duplicate visible key fails that id as ambiguous. Verify with `openclaw secrets audit --allow-exec`.
- **HashiCorp Vault CLI (`vault`)**: `command: "/opt/homebrew/bin/vault"` with `allowSymlinkCommand: true`, `trustedDirs: ["/opt/homebrew"]`, `args: ["kv", "get", "-field=OPENAI_API_KEY", "secret/openclaw"]`, `passEnv: ["VAULT_ADDR", "VAULT_TOKEN"]`, `jsonOnly: false`; the `apiKey` ref uses `id: "value"`.
- **password-store (`pass`)**: use a small resolver wrapper (an executable at an absolute path that passes exec-provider path checks, for example `/usr/local/bin/openclaw-pass-resolver`) mapping SecretRef ids to `pass` entries. The `#!/usr/bin/env node` shebang resolves `node` from the resolver process `PATH`, so include `PATH` in `passEnv`; if `pass` is not on that `PATH`, set `PASS_BIN` and include it in `passEnv` too. The provider sets `command: "/usr/local/bin/openclaw-pass-resolver"`, `passEnv: ["PATH", "HOME", "GNUPGHOME", "GPG_TTY", "PASSWORD_STORE_DIR", "PASS_BIN"]`, `jsonOnly: true`, and the `apiKey` id is e.g. `openclaw/providers/openai/apiKey`. Keep the secret on the first line of the `pass` entry (or customize the wrapper). Verify both `openclaw secrets audit --check` and `openclaw secrets audit --allow-exec`.
- **sops**: `command: "/opt/homebrew/bin/sops"` with `allowSymlinkCommand: true`, `trustedDirs: ["/opt/homebrew"]`, `args: ["-d", "--extract", '["providers"]["openai"]["apiKey"]', "/path/to/secrets.enc.json"]`, `passEnv: ["SOPS_AGE_KEY_FILE"]`, `jsonOnly: false`; the `apiKey` ref uses `id: "value"`.

## MCP server environment variables

MCP server env vars configured via `plugins.entries.acpx.config.mcpServers` support SecretInput, keeping API keys and tokens out of plaintext config.

```json5
{
  plugins: {
    entries: {
      acpx: {
        enabled: true,
        config: {
          mcpServers: {
            github: {
              command: "npx",
              args: ["-y", "@modelcontextprotocol/server-github"],
              env: {
                GITHUB_PERSONAL_ACCESS_TOKEN: {
                  source: "env",
                  provider: "default",
                  id: "MCP_GITHUB_PAT",
                },
              },
            },
          },
        },
      },
    },
  },
}
```

Plaintext string values still work. Env-template refs like `${MCP_SERVER_API_KEY}` and SecretRef objects are resolved during gateway activation before the MCP server process is spawned. As with other SecretRef surfaces, unresolved refs block activation only when the `acpx` plugin is effectively active.

## Sandbox SSH auth material

The core `ssh` sandbox backend also supports SecretRefs for SSH auth material — `identityData`, `certificateData`, and `knownHostsData` under `agents.defaults.sandbox.ssh`.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "ssh",
        ssh: {
          target: "user@gateway-host:22",
          identityData: { source: "env", provider: "default", id: "SSH_IDENTITY" },
          certificateData: { source: "env", provider: "default", id: "SSH_CERTIFICATE" },
          knownHostsData: { source: "env", provider: "default", id: "SSH_KNOWN_HOSTS" },
        },
      },
    },
  },
}
```

Runtime behavior: OpenClaw resolves these refs during sandbox activation, not lazily per SSH call; resolved values are written to temp files with restrictive permissions and used in generated SSH config; and if the effective sandbox backend is not `ssh`, these refs stay inactive and do not block startup. The backend is configured per **[oc_gateway_sandboxing_backends](oc_gateway_sandboxing_backends.md)**.

## Command-path resolution

Command paths can opt into supported SecretRef resolution via the gateway snapshot RPC. There are two broad behaviors. **Strict command paths** — e.g. `openclaw memory` remote-memory paths and `openclaw qr --remote` when it needs remote shared-secret refs — read from the active snapshot and fail fast when a required SecretRef is unavailable. **Read-only command paths** — e.g. `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, `openclaw security audit`, and read-only doctor/config repair flows — also prefer the active snapshot but degrade instead of aborting when a targeted SecretRef is unavailable.

The read-only behavior is: when the gateway is running, these commands read from the active snapshot first; if gateway resolution is incomplete or the gateway is unavailable, they attempt targeted local fallback for the command surface; if a targeted SecretRef is still unavailable, the command continues with degraded read-only output and explicit diagnostics such as "configured but unavailable in this command path". This degraded behavior is command-local only — it does not weaken runtime startup, reload, or send/auth paths. Snapshot refresh after backend secret rotation is handled by `openclaw secrets reload`; the gateway RPC method used by these command paths is `secrets.resolve`.

## Audit and configure workflow

The default operator flow is a three-step audit → configure-and-apply → re-audit cycle.

```bash
openclaw secrets audit --check
openclaw secrets configure --apply
openclaw secrets audit --check
```

Do not treat the migration as complete until the re-audit is clean: if the audit still reports plaintext values at rest, the agent-access risk persists even when runtime APIs return redacted values. If you save a plan instead of applying during `configure`, apply it with `openclaw secrets apply --from <plan-path>` before the re-audit.

**`secrets audit`** findings include plaintext values at rest (`openclaw.json`, `auth-profiles.json`, `.env`, generated `agents/*/agent/models.json`), plaintext sensitive provider header residues in generated `models.json`, unresolved refs, precedence shadowing (`auth-profiles.json` over `openclaw.json` refs), and legacy residues (`auth.json`, OAuth reminders). By default audit skips exec SecretRef resolvability checks to avoid command side effects; use `openclaw secrets audit --allow-exec` to execute exec providers during audit. Sensitive-provider-header detection is name-heuristic (fragments such as `authorization`, `x-api-key`, `token`, `secret`, `password`, `credential`).

**`secrets configure`** is an interactive helper that: configures `secrets.providers` first (`env`/`file`/`exec`, add/edit/remove); lets you select supported secret-bearing fields in `openclaw.json` plus `auth-profiles.json` for one agent scope; can create a new `auth-profiles.json` mapping in the target picker; captures SecretRef details (`source`, `provider`, `id`); runs preflight resolution; and can apply immediately. Preflight skips exec SecretRef checks unless `--allow-exec` is set; if you apply from `configure --apply` and the plan includes exec refs/providers, keep `--allow-exec` set for the apply step too. Helpful modes: `--providers-only`, `--skip-provider-setup`, `--agent <id>`. The `configure` apply defaults scrub matching static credentials from `auth-profiles.json` for targeted providers, legacy static `api_key` entries from `auth.json`, and matching known secret lines from `<config-dir>/.env`.

**`secrets apply`** applies a saved plan: `openclaw secrets apply --from /tmp/openclaw-secrets-plan.json` (add `--allow-exec` and/or `--dry-run` as needed). In dry-run, exec checks are skipped unless `--allow-exec` is set; in write mode, the command rejects plans containing exec SecretRefs/providers unless `--allow-exec` is set. Strict target/path contract details and exact rejection rules live in the Secrets Apply Plan Contract reference (see References).

## Web UI note

Some SecretInput unions are easier to configure in raw editor mode than in form mode.

**Source**: OpenClaw documentation — `gateway/secrets` (mirror `inbox/openclaw_docs/gateway/secrets.md`)
**Last Updated**: 2026-06-22
**Status**: Active
