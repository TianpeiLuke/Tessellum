---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - auth
keywords:
  - openclaw auth credential semantics
  - resolveAuthProfileOrder resolveApiKeyForProfile
  - stable probe reason codes
  - token credentials eligibility resolution
  - agent copy portability copyToAgents
  - config-only aws-sdk auth routes
  - oauth secretref policy guard
  - external cli credential discovery
  - models status probe doctor-auth
topics:
  - OpenClaw
  - Auth Credential Semantics
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/auth-credential-semantics
access_control_group: ["general"]
---

# OpenClaw — Auth Credential Eligibility and Resolution Semantics

## Overview

This note models the **canonical credential eligibility and resolution semantics** that OpenClaw shares across four surfaces — the runtime order resolver `resolveAuthProfileOrder`, the per-profile key resolver `resolveApiKeyForProfile`, the diagnostic `models status --probe`, and `doctor-auth` — mirroring the `auth-credential-semantics` source page. The page's stated goal is to keep selection-time and runtime behavior aligned, so the same eligibility judgement that selects a profile at runtime is the judgement the probe reports. It covers the stable probe reason-code set, token-credential eligibility and resolution (including `expires` validation), agent copy portability defaults, config-only `aws-sdk` routes, explicit `auth.order` filtering, probe target resolution, external-CLI credential discovery modes, the OAuth SecretRef policy guard, and the legacy-compatible probe error message.

## Stable probe reason codes

The page defines a fixed set of reason codes that `models status --probe` (and the aligned resolvers) emit:

- `ok`
- `excluded_by_auth_order`
- `missing_credential`
- `invalid_expires`
- `expired`
- `unresolved_ref`
- `no_model`

These codes are described as "stable" — they are the contract scripts and tooling can depend on, and the rest of this model maps each failure path to one of them.

## Token credentials

Token credentials (`type: "token"`) support an inline `token` and/or a `tokenRef`. The page splits the contract into eligibility rules (whether a profile is allowed to be selected at all) and resolution rules (how the actual token material is produced for an eligible profile), and it stresses that the two stay aligned for `expires`.

### Eligibility rules

1. A token profile is ineligible when both `token` and `tokenRef` are absent.
2. `expires` is optional.
3. If `expires` is present, it must be a finite number greater than `0`.
4. If `expires` is invalid (`NaN`, `0`, negative, non-finite, or wrong type), the profile is ineligible with `invalid_expires`.
5. If `expires` is in the past, the profile is ineligible with `expired`.
6. `tokenRef` does not bypass `expires` validation.

A profile that fails rule 1 surfaces as `missing_credential` (no token material at all), while rules 4 and 5 surface as `invalid_expires` and `expired` respectively — distinguishing a malformed expiry from a correctly-formed but elapsed one.

### Resolution rules

1. Resolver semantics match eligibility semantics for `expires` — the resolver applies the same `expires` validation as the eligibility check, so it cannot resolve material for a profile the eligibility pass would reject.
2. For eligible profiles, token material may be resolved from the inline value or from `tokenRef`.
3. Unresolvable refs produce `unresolved_ref` in `models status --probe` output — i.e. a `tokenRef` that cannot be dereferenced is not silently treated as missing; it is reported with its own distinct code.

## Agent copy portability

Agent auth inheritance is **read-through**: when an agent has no local profile, it can resolve profiles from the default/main agent store at runtime without copying secret material into its own `auth-profiles.json`. This means inheritance never requires duplicating secrets — a sub-agent borrows the parent's credentials at resolution time.

Explicit copy flows, such as `openclaw agents add`, use a distinct portability policy that governs whether secret material is physically copied into the new agent:

- `api_key` profiles are portable unless `copyToAgents: false`.
- `token` profiles are portable unless `copyToAgents: false`.
- `oauth` profiles are **not portable by default** because refresh tokens can be single-use or rotation-sensitive.
- Provider-owned OAuth flows may opt in with `copyToAgents: true` only when copying refresh material across agents is known safe.

Non-portable profiles remain available through read-through inheritance unless the target agent signs in separately and creates its own local profile. The portability default therefore restricts *copying* (especially of rotation-sensitive OAuth refresh material) while still allowing *use* via inheritance.

## Config-only auth routes

`auth.profiles` entries with `mode: "aws-sdk"` are **routing metadata, not stored credentials**. They are valid when the target provider uses `models.providers.<id>.auth: "aws-sdk"` or a plugin-owned Amazon Bedrock setup AWS SDK route. Because they carry no secret material, these profile ids may appear in `auth.order` and session overrides even when no matching entry exists in `auth-profiles.json` — the absence of a credential-store entry is not a failure for this mode.

The page is explicit about the inverse anti-pattern: do **not** write `type: "aws-sdk"` into `auth-profiles.json`. If a legacy install has such a marker, `openclaw doctor --fix` moves it to `auth.profiles` and removes the marker from the credential store — separating the routing declaration (config) from the credential store.

## Explicit auth order filtering

- When `auth.order.<provider>` or the auth-store order override is set for a provider, `models status --probe` only probes profile ids that remain in the resolved auth order for that provider.
- A stored profile for that provider that is omitted from the explicit order is **not silently tried later**. Probe output reports it with `reasonCode: excluded_by_auth_order` and the detail `Excluded by auth.order for this provider.`

This makes an explicit `auth.order` an allowlist: profiles outside the resolved order are reported (so they remain visible/diagnosable) rather than being attempted as a fallback.

## Probe target resolution

- Probe targets can come from three sources: auth profiles, environment credentials, or `models.json`.
- If a provider has credentials but OpenClaw cannot resolve a probeable model candidate for it, `models status --probe` reports `status: no_model` with `reasonCode: no_model`.

The `no_model` outcome is therefore distinct from a credential failure: the credential exists and is valid, but there is no model candidate to probe against.

## External CLI credential discovery

Some credentials are runtime-only and owned by external CLIs. The page constrains when those are discovered:

- Runtime-only credentials owned by external CLIs are discovered only when the provider, runtime, or auth profile is in scope for the current operation, or when a stored local profile for that external source already exists.
- Auth-store callers should choose an explicit external-CLI discovery **mode**: `none` for persisted/plugin auth only, `existing` for refreshing already-stored external CLI profiles, or `scoped` for a concrete provider/profile set.
- Read-only/status paths pass `allowKeychainPrompt: false`; they use file-backed external CLI credentials only and do not read or reuse macOS Keychain results.

The three discovery modes (`none` / `existing` / `scoped`) and the `allowKeychainPrompt: false` gate together keep diagnostic/status calls from triggering interactive Keychain prompts or pulling in out-of-scope external credentials.

## OAuth SecretRef Policy Guard

- SecretRef input is for **static credentials only**.
- If a profile credential is `type: "oauth"`, SecretRef objects are not supported for that profile credential material.
- If `auth.profiles.<id>.mode` is `"oauth"`, SecretRef-backed `keyRef`/`tokenRef` input for that profile is rejected.
- Violations are **hard failures** in startup/reload auth resolution paths.

The guard prevents pinning dynamic OAuth material (which rotates) behind a static SecretRef, and it enforces this at gateway startup and config reload rather than deferring to first use.

## Legacy-Compatible Messaging

For script compatibility, probe errors keep this first line unchanged:

`Auth profile credentials are missing or expired.`

Human-friendly detail and stable reason codes may be added on subsequent lines. This preserves a parseable first line for existing scripts while still surfacing the richer reason-code contract above on later lines.

**Source**: OpenClaw documentation — `auth-credential-semantics` (mirror `inbox/openclaw_docs/auth-credential-semantics.md`)
**Last Updated**: 2026-06-22
**Status**: Active
