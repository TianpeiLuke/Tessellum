---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - model_failover
keywords:
  - openclaw auth profile rotation
  - model failover auth stage
  - auth profile cooldown
  - billing disable backoff
  - auth.order auth.profiles
  - oauth profile ids
  - session stickiness auth profile
  - codex subscription api-key backup
  - rate limit cooldown bucket
topics:
  - OpenClaw
  - Model Failover
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/model-failover
access_control_group: ["general"]
---

# OpenClaw — Model Failover: Auth-Profile Rotation

## Overview

This note models the **auth-profile rotation** stage of OpenClaw model failover — the first of the two stages the `concepts/model-failover` source page defines (auth-profile rotation *within* the current provider, then model fallback to the next configured model). It covers the auth half of the runtime flow, the selection-source policy that decides whether failover is even allowed, the opt-in auth-failure skip cache, the user-visible fallback notices, where auth profiles (API keys and OAuth tokens) are stored, profile IDs, the rotation order (including session stickiness and the OpenAI Codex subscription + API-key backup pattern), and the cooldown / billing-disable backoff schedules. The companion model-fallback stage (candidate chains, which errors advance fallback, session overrides) lives in its sibling note; here the focus is entirely on rotating credentials inside one provider.

## Two Failover Stages (and where this note sits)

OpenClaw handles failures in two stages: **(1) auth-profile rotation** within the current provider, then **(2) model fallback** to the next model in `agents.defaults.model.fallbacks`. This note documents stage 1. The page frames the data behind both stages, but auth rotation is the inner loop tried *before* a run ever advances to a different model.

## Runtime Flow (auth-profile half)

For a normal text run, OpenClaw resolves the active session model and auth-profile preference, builds the model candidate chain, then **tries the current provider with auth-profile rotation/cooldown rules** before advancing. Only when that provider is *exhausted with a failover-worthy error* does the run move to the next model candidate (the stage-2 model-fallback path documented in the sibling note). Within stage 1, profiles are tried in rotation order, failing profiles are placed in cooldown or disabled, and the next eligible profile is attempted — all without switching the model.

The reply runner persists only the narrow set of model-selection fields it owns for fallback, which includes the two auth-profile fields `authProfileOverride` and `authProfileOverrideSource` (alongside `authProfileOverrideCompactionCount`, `providerOverride`, `modelOverride`, and `modelOverrideSource`). Persisting only these owned fields prevents a failed retry from overwriting newer unrelated session mutations such as a manual `/model` change made while the attempt was running.

## Selection Source Policy

OpenClaw separates the selected provider/model from *why* it was selected, and that source controls whether the fallback chain is allowed at all. A **configured default** (`agents.defaults.model.primary`) uses `agents.defaults.model.fallbacks`. An **agent primary** (`agents.list[].model`) is strict unless that agent model object includes its own `fallbacks` (use `fallbacks: []` to make the strict behavior explicit). An **auto fallback override** writes `providerOverride`, `modelOverride`, `modelOverrideSource: "auto"`, and the selected origin model before retrying. A **user session override** (`/model`, the model picker, `session_status(model=...)`, `sessions.patch`) writes `modelOverrideSource: "user"` and is an exact selection — a failed user-selected provider/model is reported, not masked by a configured fallback. A **legacy session override** (a `modelOverride` with no `modelOverrideSource`) is treated as a user override so an old explicit selection is not silently converted into fallback behavior. A **cron payload model** (`payload.model` / `--model`) is a job primary that uses configured fallbacks unless the job supplies `payload.fallbacks`.

The auto fallback primary-probe interval is **five minutes and is not configurable**. OpenClaw remembers recent probes per session and primary model so a failing primary is not retried on every turn.

## Auth Failure Skip Cache

By default every new turn keeps the existing fallback retry behavior: OpenClaw retries each configured fallback candidate again, including non-primary candidates that recently failed with `auth` or `auth_permanent`. Operators who prefer to suppress those repeat auth failures can opt in with the environment variable:

```bash
OPENCLAW_FALLBACK_SKIP_TTL_MS=60000
```

When enabled, OpenClaw records an in-memory, session-scoped skip marker for a non-primary fallback candidate after an auth-class failure. The marker is keyed by **session id, provider, and model**. Primary candidates are never skipped, so an explicit user model selection still surfaces the real auth error. The cache is process-local and clears on Gateway restart. The value is a TTL in milliseconds: `0` or an unset value disables the cache, and positive values are clamped between **1 second and 10 minutes**.

## User-Visible Fallback Notices

When a session moves onto an auto-selected fallback, OpenClaw sends a status notice in the same reply surface:

```text
↪️ Model Fallback: <fallback> (selected <primary>; <reason>)
```

When a later probe succeeds and the session returns to the selected primary, OpenClaw sends:

```text
↪️ Model Fallback cleared: <primary> (was <fallback>)
```

These notices are operational messages, not assistant content. They are delivered **once per state change** (including side-effect-only turns when feasible), but sticky fallback turns do not repeat them. Delivery bypasses normal source-reply suppression, the notice does not consume the first assistant reply slot for threaded channels, and it is excluded from text-to-speech and commitment extraction.

## Auth Storage (keys + OAuth)

OpenClaw uses **auth profiles** for both API keys and OAuth tokens. Secrets and runtime auth-routing state live in `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`. Config `auth.profiles` / `auth.order` are **metadata + routing only** (no secrets). A legacy import-only OAuth file `~/.openclaw/credentials/oauth.json` is imported into the per-agent auth store on first use, and legacy `auth-profiles.json`, `auth-state.json`, and per-agent `auth.json` files are imported by `openclaw doctor --fix`.

Credential types are recorded as `type: "api_key"` → `{ provider, key }`, or `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (plus `projectId` / `enterpriseUrl` for some providers).

## Profile IDs

OAuth logins create distinct profiles so multiple accounts can coexist. The default profile id is `provider:default` when no email is available; an OAuth login with an email produces `provider:<email>` (for example `google-antigravity:user@gmail.com`). Profiles live in the per-agent `openclaw-agent.sqlite` auth profile store.

## Rotation Order

When a provider has multiple profiles, OpenClaw chooses an order from: **(1) explicit config** `auth.order[provider]` (if set), then **(2) configured profiles** — `auth.profiles` filtered by provider, then **(3) stored profiles** — the per-agent SQLite auth-profile entries for the provider.

If no explicit order is configured, OpenClaw uses a round-robin order with **primary key = profile type (OAuth before API keys)** and **secondary key = `usageStats.lastUsed` (oldest first, within each type)**. Cooldown/disabled profiles are moved to the end, ordered by soonest expiry.

### Session Stickiness (cache-friendly)

OpenClaw **pins the chosen auth profile per session** to keep provider caches warm and does **not** rotate on every request. The pinned profile is reused until the session is reset (`/new` / `/reset`), a compaction completes (the compaction count increments), or the profile is in cooldown/disabled. Manual selection via `/model …@<profileId>` sets a **user override** for that session and is not auto-rotated until a new session starts. Auto-pinned profiles (selected by the session router) are treated as a *preference* — tried first but possibly rotated away from on rate limits/timeouts, then preferred again once available — whereas user-pinned profiles stay locked: if a user-pinned profile fails and model fallbacks are configured, OpenClaw moves to the next *model* instead of switching profiles.

### OpenAI Codex Subscription plus API-Key Backup

For OpenAI agent models, auth and runtime are separate: `openai/gpt-*` stays on the Codex harness while auth can rotate between a Codex subscription profile and an OpenAI API-key backup. Use `auth.order.openai` for the user-facing order, with `openai:*` ids covering both ChatGPT/Codex OAuth profiles and OpenAI API-key profiles:

```json5
{
  auth: {
    order: {
      openai: ["openai:user@example.com", "openai:api-key-backup"],
    },
  },
}
```

When the subscription hits a Codex usage limit, OpenClaw records the exact reset time when Codex provides one, tries the next ordered auth profile, and keeps the run inside the Codex harness. Once the reset time passes, the subscription profile is eligible again and the next automatic selection can return to it. Use a user-pinned profile only to force one account/key for that session — user-pinned profiles are intentionally strict and do not silently jump to another profile.

## Cooldowns

When a profile fails due to auth/rate-limit errors (or a timeout that looks like rate limiting), OpenClaw marks it **in cooldown** and moves to the next profile. The rate-limit bucket is broader than plain `429`: it also includes provider messages such as `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`, `throttled`, `resource exhausted`, and periodic usage-window limits such as `weekly/monthly limit reached`. Format/invalid-request errors are usually terminal (retrying the same payload fails the same way) so OpenClaw surfaces them instead of rotating auth profiles, though known retry-repair paths can opt in via the `allowFormatRetry` policy. Generic server text can land in the timeout bucket when it matches a known transient pattern — the bare stream-wrapper message `An unknown error occurred` is treated as failover-worthy for every provider (it is emitted when provider streams end with `stopReason: "aborted"` or `stopReason: "error"` without detail), and JSON `api_error` payloads such as `internal server error`, `unknown error, 520`, `upstream error`, or `backend error` are also treated as failover-worthy. OpenRouter-specific `Provider returned error` is treated as timeout only in OpenRouter context, and the generic internal `LLM request failed with an unknown error.` stays conservative and does not trigger failover by itself.

For Stainless-based SDKs such as Anthropic and OpenAI, OpenClaw caps SDK-internal `retry-after-ms` / `retry-after` waits at **60 seconds** by default and surfaces longer retryable responses immediately so the failover path can run; tune or disable the cap with `OPENCLAW_SDK_RETRY_MAX_WAIT_SECONDS`. Rate-limit cooldowns can also be **model-scoped**: OpenClaw records `cooldownModel` for rate-limit failures when the failing model id is known, a sibling model on the same provider can still be tried when the cooldown is scoped to a different model, and billing/disabled windows still block the whole profile across models.

Cooldowns use exponential backoff: **1 minute → 5 minutes → 25 minutes → 1 hour (cap)**. State is stored in the per-agent SQLite auth state under `usageStats`:

```json
{
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## Billing Disables

Billing/credit failures (for example "insufficient credits" / "credit balance too low") are treated as failover-worthy but are usually not transient, so instead of a short cooldown OpenClaw marks the profile as **disabled** (with a longer backoff) and rotates to the next profile/provider. Not every billing-shaped response is `402`, and not every HTTP `402` lands here: OpenClaw keeps explicit billing text in the billing lane even when a provider returns `401` or `403`, but provider-specific matchers stay scoped to the provider that owns them (for example OpenRouter `403 Key limit exceeded`). Temporary `402` usage-window and organization/workspace spend-limit errors are instead classified as `rate_limit` when the message looks retryable (for example `weekly usage limit exhausted`, `daily limit reached, resets tomorrow`, or `organization spending limit exceeded`), keeping them on the short cooldown path. Disabled state is stored in the per-agent SQLite auth state:

```json
{
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

Defaults for the billing/overloaded backoff: billing backoff starts at **5 hours**, doubles per billing failure, and caps at **24 hours**; backoff counters reset if the profile hasn't failed for **24 hours** (configurable); overloaded retries allow **1 same-provider profile rotation** before model fallback; and overloaded retries use **0 ms backoff** by default. The related config keys (`auth.profiles`, `auth.order`, `auth.cooldowns.billingBackoffHours`, `auth.cooldowns.billingBackoffHoursByProvider`, `auth.cooldowns.billingMaxHours`, `auth.cooldowns.failureWindowHours`, `auth.cooldowns.overloadedProfileRotations`, `auth.cooldowns.overloadedBackoffMs`, `auth.cooldowns.rateLimitedProfileRotations`) are documented under Gateway configuration.

**Source**: OpenClaw documentation — `concepts/model-failover` (mirror `inbox/openclaw_docs/concepts/model-failover.md`)
**Last Updated**: 2026-06-22
**Status**: Active
