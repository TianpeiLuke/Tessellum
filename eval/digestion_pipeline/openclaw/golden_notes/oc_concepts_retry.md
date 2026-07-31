---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - retry
keywords:
  - openclaw retry policy
  - per-request retry
  - retry-after handling
  - x-should-retry false cutoff
  - stainless sdk retry
  - discord telegram retry
  - exponential backoff jitter
  - OPENCLAW_SDK_RETRY_MAX_WAIT_SECONDS
topics:
  - OpenClaw
  - Retry Policy
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/retry
access_control_group: ["general"]
---

# OpenClaw — Outbound Provider Retry Policy

## Overview

This note describes the OpenClaw **retry policy** for outbound provider calls: a per-request (not per-flow) retry that preserves ordering and avoids duplicating non-idempotent operations, mirroring the `concepts/retry` source page. It covers the policy goals, the default attempt/delay-cap/jitter values, the per-channel behavior for model providers (Stainless-SDK `retry-after` handling and the 60-second cutoff that injects `x-should-retry: false` to trigger model failover), Discord, and Telegram, plus the per-provider configuration block and the per-request scoping notes.

## Goals

The retry policy is scoped deliberately narrow so that retries never corrupt session state or duplicate side effects:

- Retry per HTTP request, not per multi-step flow.
- Preserve ordering by retrying only the current step.
- Avoid duplicating non-idempotent operations.

## Defaults

The policy ships with the following default values:

- Attempts: 3
- Max delay cap: 30000 ms
- Jitter: 0.1 (10 percent)
- Provider defaults:
  - Telegram min delay: 400 ms
  - Discord min delay: 500 ms

## Behavior

Retry behavior differs by the outbound surface. Model-provider SDK retries are the primary surface, while the Discord and Telegram messaging channels apply their own send-retry rules.

### Model providers

OpenClaw lets provider SDKs handle normal short retries. For Stainless-based SDKs such as Anthropic and OpenAI, retryable responses (`408`, `409`, `429`, and `5xx`) can include `retry-after-ms` or `retry-after`. When that wait is longer than 60 seconds, OpenClaw injects `x-should-retry: false` so the SDK surfaces the error immediately and model failover can rotate to another auth profile or fallback model. Override the cap with `OPENCLAW_SDK_RETRY_MAX_WAIT_SECONDS=<seconds>`. Set it to `0`, `false`, `off`, `none`, or `disabled` to let SDKs honor long `Retry-After` sleeps internally.

### Discord

The Discord channel retries on rate-limit errors (HTTP 429), request timeouts, HTTP 5xx responses, and transient transport failures such as DNS lookup failures, connection resets, socket closes, and fetch failures. It uses Discord `retry_after` when available, otherwise exponential backoff.

### Telegram

The Telegram channel retries on transient errors (429, timeout, connect/reset/closed, temporarily unavailable). It uses `retry_after` when available, otherwise exponential backoff. Markdown parse errors are not retried; they fall back to plain text.

## Configuration

Set retry policy per provider in `~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

## Notes

The per-request scoping has two practical consequences for multi-step sends:

- Retries apply per request (message send, media upload, reaction, poll, sticker).
- Composite flows do not retry completed steps.

**Source**: OpenClaw documentation — `concepts/retry` (mirror `inbox/openclaw_docs/concepts/retry.md`)
**Last Updated**: 2026-06-22
**Status**: Active
