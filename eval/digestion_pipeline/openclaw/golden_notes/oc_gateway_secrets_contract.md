---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - secrets
keywords:
  - openclaw secretref contract
  - secrets runtime snapshot
  - active-surface filtering
  - secretref source env file exec
  - ref-over-plaintext precedence
  - degraded recovered secrets signals
  - one-way safety policy no rollback
  - agent-access boundary secrets
topics:
  - OpenClaw
  - Gateway Secrets
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/secrets
access_control_group: ["general"]
---

# OpenClaw — Gateway SecretRef Contract and Runtime Model

## Overview

This note models the **SecretRef secrets-management contract** that lets OpenClaw resolve supported credentials without storing them as plaintext in configuration — the conceptual + runtime half of the `gateway/secrets` source page. It covers the eager in-memory runtime snapshot, the agent-access boundary (why SecretRefs are not a process-isolation boundary), active-surface filtering, the single `SecretRef` object shape and per-`source` validation, the supported credential surface, the required behavior and precedence rules, the activation triggers, the degraded/recovered signals, the one-way (no-plaintext-rollback) safety policy, and the legacy-auth compatibility notes. The operational procedure that *applies* this contract — provider config, file-backed keys, exec/MCP/sandbox-SSH wiring, command-path resolution, and the `secrets audit`/`configure`/`apply` workflow — lives in the sibling note **[oc_gateway_secrets_operations](oc_gateway_secrets_operations.md)**.

OpenClaw supports additive SecretRefs so supported credentials do not need to be stored as plaintext in configuration. Plaintext still works — SecretRefs are opt-in per credential.

## Goals and Runtime Model

Secrets are resolved into an **in-memory runtime snapshot**, with these properties:

- Resolution is **eager during activation**, not lazy on request paths.
- Startup **fails fast** when an effectively active SecretRef cannot be resolved.
- Reload uses **atomic swap**: full success, or keep the last-known-good snapshot.
- SecretRef policy violations (for example OAuth-mode auth profiles combined with SecretRef input) fail activation **before** runtime swap.
- Runtime requests read from the **active in-memory snapshot only**.
- After the first successful config activation/load, runtime code paths keep reading that active in-memory snapshot until a successful reload swaps it.
- Outbound delivery paths also read from that active snapshot (for example Discord reply/thread delivery and Telegram action sends); they do **not** re-resolve SecretRefs on each send.

This keeps secret-provider outages off hot request paths.

## Agent-Access Boundary

SecretRefs protect credentials from being persisted in supported config and generated model surfaces, but they are **not a process-isolation boundary**. If a plaintext credential remains on disk in a path the agent can read, the agent can bypass API-level redaction by using file or shell tools to inspect that file.

For production deployments where agent-accessible files are in scope, treat SecretRef migration as complete only when all of these are true:

- supported credentials use SecretRefs instead of plaintext values
- legacy plaintext residue has been scrubbed from `openclaw.json`, `auth-profiles.json`, `.env`, and generated `models.json` files
- `openclaw secrets audit --check` is clean after the migration
- any remaining unsupported or rotating credentials are protected by operating system isolation, container isolation, or an external credential proxy

This is why the audit/configure/apply workflow is a **security migration gate**, not just a convenience helper. SecretRefs do not make arbitrary readable files safe: backups, copied configs, old generated model catalogs, and unsupported credential classes must be treated as production secrets until they are deleted, moved outside the agent trust boundary, or protected by a separate isolation layer.

## Active-Surface Filtering

SecretRefs are validated only on **effectively active surfaces**:

- **Enabled surfaces**: unresolved refs block startup/reload.
- **Inactive surfaces**: unresolved refs do not block startup/reload.
- Inactive refs emit non-fatal diagnostics with code `SECRETS_REF_IGNORED_INACTIVE_SURFACE`.

Examples of **inactive surfaces** (refs ignored until the surface becomes active):

- Disabled channel/account entries.
- Top-level channel credentials that no enabled account inherits.
- Disabled tool/feature surfaces.
- Web search provider-specific keys that are not selected by `tools.web.search.provider`. In auto mode (provider unset), keys are consulted by precedence for provider auto-detection until one resolves; after selection, non-selected provider keys are treated as inactive until selected.
- Sandbox SSH auth material (`agents.defaults.sandbox.ssh.identityData`, `certificateData`, `knownHostsData`, plus per-agent overrides) is active only when the effective sandbox backend is `ssh` for the default agent or an enabled agent.
- `gateway.remote.token` / `gateway.remote.password` SecretRefs are active if one of these is true: `gateway.mode=remote`; `gateway.remote.url` is configured; `gateway.tailscale.mode` is `serve` or `funnel`; or, in local mode without those remote surfaces, `gateway.remote.token` is active when token auth can win and no env/auth token is configured, and `gateway.remote.password` is active only when password auth can win and no env/auth password is configured.
- `gateway.auth.token` SecretRef is inactive for startup auth resolution when `OPENCLAW_GATEWAY_TOKEN` is set, because env token input wins for that runtime.

## SecretRef Contract

Use one object shape everywhere:

```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

The three `source` kinds differ in their `id` format and validation rules:

- **`env`** — e.g. `{ source: "env", provider: "default", id: "OPENAI_API_KEY" }`. Supported `SecretInput` fields also accept exact string shorthands `"${OPENAI_API_KEY}"` and `"$OPENAI_API_KEY"`. Validation: `provider` must match `^[a-z][a-z0-9_-]{0,63}$`; `id` must match `^[A-Z][A-Z0-9_]{0,127}$`.
- **`file`** — e.g. `{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }`. Validation: `provider` must match `^[a-z][a-z0-9_-]{0,63}$`; `id` must be an absolute JSON pointer (`/...`); RFC6901 escaping in segments: `~` => `~0`, `/` => `~1`.
- **`exec`** — e.g. `{ source: "exec", provider: "vault", id: "providers/openai/apiKey#value" }`. Validation: `provider` must match `^[a-z][a-z0-9_-]{0,63}$`; `id` must match `^[A-Za-z0-9][A-Za-z0-9._:/#-]{0,255}$` (supports selectors such as `secret#json_key`); `id` must not contain `.` or `..` as slash-delimited path segments (for example `a/../b` is rejected).

The wiring of providers (`secrets.providers`), file-backed keys, and exec resolvers against this shape is documented in **[oc_gateway_secrets_operations](oc_gateway_secrets_operations.md)**.

## Supported Credential Surface

Canonical supported and unsupported credentials are listed in the [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface) reference page. Runtime-minted or rotating credentials and OAuth refresh material are **intentionally excluded** from read-only SecretRef resolution.

## Required Behavior and Precedence

- **Field without a ref**: unchanged.
- **Field with a ref**: required on active surfaces during activation.
- If both plaintext and ref are present, the **ref takes precedence** on supported precedence paths.
- The redaction sentinel `__OPENCLAW_REDACTED__` is reserved for internal config redaction/restore and is rejected as literal submitted config data.

Warning and audit signals:

- `SECRETS_REF_OVERRIDES_PLAINTEXT` (runtime warning).
- `REF_SHADOWED` (audit finding when `auth-profiles.json` credentials take precedence over `openclaw.json` refs).

Google Chat compatibility behavior: `serviceAccountRef` takes precedence over plaintext `serviceAccount`, and the plaintext value is ignored when the sibling ref is set.

## Activation Triggers

Secret activation runs on:

- Startup (preflight plus final activation).
- Config reload hot-apply path.
- Config reload restart-check path.
- Manual reload via `secrets.reload`.
- Gateway config write RPC preflight (`config.set` / `config.apply` / `config.patch`) for active-surface SecretRef resolvability within the submitted config payload before persisting edits.

Activation contract:

- Success swaps the snapshot **atomically**.
- Startup failure aborts gateway startup.
- Runtime reload failure keeps the **last-known-good snapshot**.
- Write-RPC preflight failure rejects the submitted config and keeps both disk config and active runtime snapshot unchanged.
- Providing an explicit per-call channel token to an outbound helper/tool call does **not** trigger SecretRef activation; activation points remain startup, reload, and explicit `secrets.reload`.

## Degraded and Recovered Signals

When reload-time activation fails after a healthy state, OpenClaw enters a **degraded secrets state**. The one-shot system event and log codes are `SECRETS_RELOADER_DEGRADED` and `SECRETS_RELOADER_RECOVERED`.

Behavior:

- **Degraded**: runtime keeps the last-known-good snapshot.
- **Recovered**: emitted once after the next successful activation.
- Repeated failures while already degraded log warnings but do not spam events.
- Startup fail-fast does **not** emit degraded events because the runtime never became active.

## One-Way Safety Policy

OpenClaw intentionally does **not** write rollback backups containing historical plaintext secret values. The safety model is:

- preflight must succeed before write mode
- runtime activation is validated before commit
- apply updates files using atomic file replacement and best-effort restore on failure

## Legacy Auth Compatibility Notes

For static credentials, runtime no longer depends on plaintext legacy auth storage:

- The runtime credential source is the resolved in-memory snapshot.
- Legacy static `api_key` entries are scrubbed when discovered.
- OAuth-related compatibility behavior remains separate.

**Source**: OpenClaw documentation — `gateway/secrets` (mirror `inbox/openclaw_docs/gateway/secrets.md`)
**Last Updated**: 2026-06-22
**Status**: Active
