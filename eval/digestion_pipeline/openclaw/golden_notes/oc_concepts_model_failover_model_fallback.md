---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - model_failover
keywords:
  - openclaw model fallback
  - model candidate chain
  - fallbacksoverride
  - which errors advance fallback
  - cooldown skip vs probe
  - modeloverridesource auto
  - fallbacksummaryerror
  - live model switching
  - runwithmodelfallback
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

# OpenClaw — Model Fallback (Stage 2 of Model Failover)

## Overview

This note explains OpenClaw's **model fallback** — the second of the two failover stages described on the `concepts/model-failover` source page. Stage 1 (auth-profile rotation *within* the current provider) is covered by its sibling note; this note picks up at the moment a provider is exhausted with a failover-worthy error and OpenClaw must move *across models*. It covers the runtime flow's fallback half, how the candidate chain is built, which errors advance fallback versus stay terminal, the cooldown-skip-vs-probe per-candidate decision, how session overrides and live `/model` switching coordinate with fallback retries, and the `FallbackSummaryError` observability surface. Every claim is grounded in the mirror page `inbox/openclaw_docs/concepts/model-failover.md`.

## Runtime Flow (model-fallback half)

For a normal text run, after the active session state is resolved OpenClaw builds the **model candidate chain** from the current model selection and the fallback policy for that selection source, then tries the current provider with auth-profile rotation/cooldown rules. The fallback stage begins on failure: *"If that provider is exhausted with a failover-worthy error, move to the next model candidate."* Before the retry starts, OpenClaw **persists the selected fallback override** to the session entry so other session readers see the same provider/model the runner is about to use — *"The persisted model override is marked `modelOverrideSource: "auto"`."* If the fallback candidate itself fails, OpenClaw **rolls back narrowly**: only the fallback-owned session override fields are reverted, and only when they still match that failed candidate. If every candidate fails, OpenClaw throws a `FallbackSummaryError` with per-attempt detail and the soonest cooldown expiry when one is known.

The rollback is intentionally narrower than "save and restore the whole session". The reply runner only persists the model-selection fields it owns for fallback: `providerOverride`, `modelOverride`, `modelOverrideSource`, `authProfileOverride`, `authProfileOverrideSource`, and `authProfileOverrideCompactionCount`. Per source, *"That prevents a failed fallback retry from overwriting newer unrelated session mutations such as manual `/model` changes or session rotation updates that happened while the attempt was running."*

## Model Fallback

If all profiles for a provider fail, OpenClaw moves to the next model in `agents.defaults.model.fallbacks`. The source states this *"applies to auth failures, rate limits, and timeouts that exhausted profile rotation (other errors do not advance fallback)."* Provider errors that do not expose enough detail are still labeled precisely in fallback state: `empty_response` means the provider returned no usable message or status; `no_error_details` means the provider explicitly returned `Unknown error (no error details in response)`; and `unclassified` means OpenClaw preserved the raw preview but no classifier matched it yet.

Overloaded and rate-limit errors are handled more aggressively than billing cooldowns. By default OpenClaw allows **one same-provider auth-profile retry, then switches to the next configured model fallback without waiting**. Provider-busy signals such as `ModelNotReadyException` land in that overloaded bucket. This is tuned with `auth.cooldowns.overloadedProfileRotations`, `auth.cooldowns.overloadedBackoffMs`, and `auth.cooldowns.rateLimitedProfileRotations`.

Whether the configured fallback chain may be walked at all depends on the **selection source** (detailed in the auth-rotation sibling note). Per source, a run that starts from the configured default primary, a cron job primary, an agent primary with explicit fallbacks, or an auto-selected fallback override *can* walk the matching configured chain. By contrast, agent primaries without explicit fallbacks and explicit user selections — for example `/model ollama/qwen3.5:27b`, the model picker, `sessions.patch`, or one-off CLI provider/model overrides — are **strict**: if that provider/model is unreachable or fails before producing a reply, OpenClaw reports the failure instead of answering from an unrelated fallback.

### Candidate Chain Rules

OpenClaw builds the candidate list from the currently requested `provider/model` plus configured fallbacks, under these rules (verbatim from source):

- The requested model is always first.
- Explicit configured fallbacks are deduplicated but **not filtered by the model allowlist**. They are treated as explicit operator intent.
- If the current run is already on a configured fallback in the same provider family, OpenClaw keeps using the full configured chain.
- When no explicit fallback override is supplied, configured fallbacks are tried **before** the configured primary even if the requested model uses a different provider.
- When no explicit fallback override is supplied to the fallback runner, the configured primary is **appended at the end** so the chain can settle back onto the normal default once earlier candidates are exhausted.
- When a caller supplies `fallbacksOverride`, the runner uses exactly the requested model plus that override list. An **empty list disables model fallback** and prevents the configured primary from being appended as a hidden retry target.

### Which Errors Advance Fallback

A failover-worthy error advances to the next candidate; a terminal error surfaces immediately. The source splits them as follows.

**Continues on:** auth failures; rate limits and cooldown exhaustion; overloaded/provider-busy errors; timeout-shaped failover errors; billing disables; `LiveSessionModelSwitchError` (normalized into a failover path so a stale persisted model does not create an outer retry loop); and other unrecognized errors **when there are still remaining candidates**.

**Does not continue on:** explicit aborts that are not timeout/failover-shaped; context-overflow errors that should stay inside compaction/retry logic — for example `request_too_large`, `INVALID_ARGUMENT: input exceeds the maximum number of tokens`, `input token count exceeds the maximum number of input tokens`, `The input is too long for the model`, or `ollama error: context length exceeded`; and a final unknown error **when there are no candidates left**.

### Cooldown Skip vs Probe Behavior

When every auth profile for a provider is already in cooldown, OpenClaw does **not** automatically skip that provider forever — it makes a per-candidate decision (verbatim from source):

- Persistent auth failures skip the whole provider immediately.
- Billing disables usually skip, but the **primary candidate can still be probed on a throttle** so recovery is possible without restarting.
- The primary candidate may be probed near cooldown expiry, with a per-provider throttle.
- Same-provider fallback siblings can be attempted despite cooldown when the failure looks transient (`rate_limit`, `overloaded`, or unknown). This is especially relevant when a rate limit is model-scoped and a sibling model may still recover immediately.
- Transient cooldown probes are **limited to one per provider per fallback run** so a single provider does not stall cross-provider fallback.

## Session Overrides and Live Model Switching

Session model changes are shared state: the active runner, the `/model` command, compaction/session updates, and live-session reconciliation all read or write parts of the same session entry. Fallback retries therefore have to coordinate with live model switching (rules verbatim from source):

- Only **explicit user-driven** model changes mark a pending live switch. That includes `/model`, `session_status(model=...)`, and `sessions.patch`.
- System-driven model changes such as fallback rotation, heartbeat overrides, or compaction **never** mark a pending live switch on their own.
- User-driven model overrides are treated as exact selections for fallback policy, so an unreachable selected provider surfaces as a failure instead of being masked by `agents.defaults.model.fallbacks`.
- Before a fallback retry starts, the reply runner persists the selected fallback override fields to the session entry.
- Auto fallback overrides remain selected on subsequent turns so OpenClaw does not probe a known-bad primary on every message. OpenClaw periodically probes the configured origin again and clears the auto override when it recovers; `/new`, `/reset`, and `sessions.reset` clear auto-sourced overrides immediately.
- User replies announce fallback transitions and fallback-cleared recovery **once per state change**; sticky fallback turns do not repeat the notice.
- `/status` shows the selected model and, when fallback state differs, the active fallback model and reason.
- Live-session reconciliation **prefers persisted session overrides over stale runtime model fields**.
- If a live-switch error points at a later candidate in the active fallback chain, OpenClaw jumps directly to that selected model instead of walking unrelated candidates first.
- If the fallback attempt fails, the runner rolls back only the override fields it wrote, and only if they still match that failed candidate.

This ordering closes the classic race: the selected primary fails → a fallback candidate is chosen in memory → the session store still reflects the old primary → live-session reconciliation reads the stale session state → the retry gets snapped back to the old model before the fallback attempt starts. Per source, *"The persisted fallback override closes that window, and the narrow rollback keeps newer manual or runtime session changes intact."*

## Observability and Failure Summaries

`runWithModelFallback(...)` records per-attempt details that feed logs and user-facing cooldown messaging: the provider/model attempted; the reason (`rate_limit`, `overloaded`, `billing`, `auth`, `model_not_found`, and similar failover reasons); an optional status/code; and a human-readable error summary.

Structured `model_fallback_decision` logs also include flat `fallbackStep*` fields when a candidate fails, is skipped, or a later fallback succeeds. These fields make the attempted transition explicit — `fallbackStepFromModel`, `fallbackStepToModel`, `fallbackStepFromFailureReason`, `fallbackStepFromFailureDetail`, and `fallbackStepFinalOutcome` — so log and diagnostic exporters can reconstruct the primary failure even when the terminal fallback also fails.

When every candidate fails, OpenClaw throws `FallbackSummaryError`. The outer reply runner can use that to build a more specific message such as "all models are temporarily rate-limited" and include the soonest cooldown expiry when one is known. That cooldown summary is **model-aware**: unrelated model-scoped rate limits are ignored for the attempted provider/model chain, and if the remaining block is a matching model-scoped rate limit, OpenClaw reports the last matching expiry that still blocks that model.

The relevant config keys for this stage (from the page's "Related config" footer, pointing at Gateway configuration) are `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`, the `auth.cooldowns.overloaded*` and `auth.cooldowns.rateLimitedProfileRotations` knobs above, and `agents.defaults.imageModel` routing.

**Source**: OpenClaw documentation — `concepts/model-failover` (model-fallback half; mirror `inbox/openclaw_docs/concepts/model-failover.md`)
**Last Updated**: 2026-06-22
**Status**: Active
