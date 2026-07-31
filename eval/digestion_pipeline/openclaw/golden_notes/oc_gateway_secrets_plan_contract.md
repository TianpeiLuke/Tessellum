---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - secrets
keywords:
  - openclaw secrets apply plan contract
  - secrets plan targets schema
  - providerupserts providerdeletes
  - invalid plan target path
  - auth-profiles.json target agentid
  - exec provider allow-exec consent
  - secretref credential path validation
  - secrets apply dry-run
topics:
  - OpenClaw
  - Secrets Apply Plan Contract
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/secrets-plan-contract
access_control_group: ["general"]
---

# OpenClaw — Secrets Apply Plan Contract

## Overview

This note models the strict contract that `openclaw secrets apply` enforces on a plan file — the typed schema and validation rules a plan must satisfy before any credential is written. It mirrors the `gateway/secrets-plan-contract` source page: the `targets` plan-file shape, the optional `providerUpserts`/`providerDeletes` provider-map mutations, the supported credential-path scope, target-type-to-path matching, the per-target path validation rules, fail-before-mutate failure behavior, exec-provider `--allow-exec` consent, runtime/audit scope notes, and the operator dry-run/apply commands. The contract exists so that "if a target does not match these rules, apply fails before mutating configuration."

## Plan File Shape

`openclaw secrets apply --from <plan.json>` expects a plan object whose `targets` field is an array of plan targets. Each plan target declares its `type`, dot-`path`, optional `pathSegments`, the id it scopes (`providerId` for provider keys, `agentId` for auth-profile targets), and a `ref` SecretRef describing where the secret value is sourced. The plan envelope carries `version: 1` and `protocolVersion: 1`. The source documents this shape with two targets — a `models.providers.apiKey` provider key and an `auth-profiles.api_key.key` per-agent profile key:

```json5
{
  version: 1,
  protocolVersion: 1,
  targets: [
    {
      type: "models.providers.apiKey",
      path: "models.providers.openai.apiKey",
      pathSegments: ["models", "providers", "openai", "apiKey"],
      providerId: "openai",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
    {
      type: "auth-profiles.api_key.key",
      path: "profiles.openai:default.key",
      pathSegments: ["profiles", "openai:default", "key"],
      agentId: "main",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
  ],
}
```

## Provider Upserts and Deletes

A plan may also include two optional top-level fields that mutate the `secrets.providers` map alongside the per-target writes. `providerUpserts` is an object keyed by provider alias; each value is a provider definition with the same shape accepted under `secrets.providers.<alias>` in `openclaw.json` (for example an `exec` or `file` provider). `providerDeletes` is an array of provider aliases to remove.

`providerUpserts` runs before `targets`, so a `target.ref.provider` may reference a provider alias that the same plan introduces in `providerUpserts`. Without this ordering, plans that reference an alias not yet configured in `openclaw.json` fail with `provider "<alias>" is not configured`. The source illustrates this with a plan that upserts an exec provider, deletes a legacy alias, and then references the new alias from a target's `ref`:

```json5
{
  version: 1,
  protocolVersion: 1,
  providerUpserts: {
    onepassword_anthropic: {
      source: "exec",
      command: "/usr/bin/op",
      args: ["read", "op://Vault/Anthropic/credential"],
    },
  },
  providerDeletes: ["legacy_unused_alias"],
  targets: [
    {
      type: "models.providers.apiKey",
      path: "models.providers.anthropic.apiKey",
      pathSegments: ["models", "providers", "anthropic", "apiKey"],
      providerId: "anthropic",
      ref: { source: "exec", provider: "onepassword_anthropic", id: "credential" },
    },
  ],
}
```

Exec providers introduced via `providerUpserts` are still subject to the exec consent rules described below: plans containing exec providers require `--allow-exec` in write mode.

## Supported Target Scope

Plan targets are accepted for the supported credential paths enumerated in the SecretRef Credential Surface reference (`/reference/secretref-credential-surface`). A target whose path is outside that supported set is not a valid plan target.

## Target Type Behavior

The general rule is that `target.type` must be recognized and must match the normalized `target.path` shape. The source also lists compatibility aliases that remain accepted for existing plans: `models.providers.apiKey`, `skills.entries.apiKey`, and `channels.googlechat.serviceAccount`.

## Path Validation Rules

Each target is validated against all of the following rules:

- `type` must be a recognized target type.
- `path` must be a non-empty dot path.
- `pathSegments` can be omitted; if provided, it must normalize to exactly the same path as `path`.
- Forbidden segments are rejected: `__proto__`, `prototype`, `constructor`.
- The normalized path must match the registered path shape for the target type.
- If `providerId` or `accountId` is set, it must match the id encoded in the path.
- `auth-profiles.json` targets require `agentId`.
- When creating a new `auth-profiles.json` mapping, include `authProfileProvider`.

## Failure Behavior

If a target fails validation, apply exits with an error of this form, and no writes are committed for an invalid plan:

```text
Invalid plan target path for models.providers.apiKey: models.providers.openai.baseUrl
```

This is the fail-before-mutate guarantee from the overview: an invalid plan never partially writes credentials.

## Exec Provider Consent Behavior

Exec SecretRefs and exec providers — which run an external command to source a secret — are gated by an explicit consent flag:

- `--dry-run` skips exec SecretRef checks by default.
- Plans containing exec SecretRefs/providers are rejected in write mode unless `--allow-exec` is set.
- When validating/applying exec-containing plans, pass `--allow-exec` in both the dry-run and the write commands.

## Runtime and Audit Scope Notes

Ref-only `auth-profiles.json` entries (`keyRef`/`tokenRef`) are included in runtime resolution and audit coverage. `secrets apply` writes supported `openclaw.json` targets, supported `auth-profiles.json` targets, and optional scrub targets.

## Operator Checks

The recommended operator workflow is to validate the plan with `--dry-run` first, then apply for real; exec-containing plans opt into `--allow-exec` explicitly in both modes:

```bash
# Validate plan without writes
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run

# Then apply for real
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json

# For exec-containing plans, opt in explicitly in both modes
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run --allow-exec
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --allow-exec
```

If apply fails with an invalid target path message, regenerate the plan with `openclaw secrets configure` or fix the target path to a supported shape from the rules above.

**Source**: OpenClaw documentation — `gateway/secrets-plan-contract` (mirror `inbox/openclaw_docs/gateway/secrets-plan-contract.md`)
**Last Updated**: 2026-06-22
**Status**: Active
