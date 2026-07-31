---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - anthropic
keywords:
  - openclaw anthropic provider
  - claude api key
  - claude cli backend
  - claude -p billing
  - prompt caching cacheretention
  - thinking defaults fable opus
  - fast mode service_tier
  - 1m context window claude
topics:
  - OpenClaw
  - Anthropic Claude Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/anthropic
access_control_group: ["general"]
---

# OpenClaw — Anthropic Claude Provider Setup

## Overview

This note is the setup procedure for using Anthropic's **Claude** model family in OpenClaw, mirroring the `providers/anthropic` source page. Anthropic supports two auth routes: an **API key** for direct Anthropic API access with usage-based billing (the `anthropic/*` models), and the **Claude CLI** backend that reuses an existing Claude Code login on the same host. It walks the two onboarding flows and config examples, the `claude -p` billing caveat, per-model thinking defaults (Fable 5 / Opus 4.8 / 4.6), the `cacheRetention` prompt-caching table, the advanced-configuration knobs (fast mode, image/PDF media understanding, 1M context window), and the four auth-troubleshooting cases.

## Getting started

OpenClaw exposes Anthropic through `openclaw onboard`, then verifies a model is resolvable with `openclaw models list --provider anthropic`. Pick the API-key route for standard usage-based billing and the Claude CLI route to reuse an existing Claude CLI login without a separate API key.

### API key route

Best for standard API access and usage-based billing. Create an API key in the [Anthropic Console](https://console.anthropic.com/), then run `openclaw onboard` and choose **Anthropic API key**, or pass the key directly with `openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"`. Verify with `openclaw models list --provider anthropic`. The config example sets the `ANTHROPIC_API_KEY` env var and a primary model:

```json5
{
  env: { ANTHROPIC_API_KEY: "example-anthropic-key-not-real" },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-8" } } },
}
```

### Claude CLI route

Best for reusing an existing Claude CLI login without a separate API key. First ensure the Claude CLI is installed and logged in (verify with `claude --version`), then run `openclaw onboard` and choose **Claude CLI** — OpenClaw detects and reuses the existing Claude CLI credentials. Setup and runtime details for the Claude CLI backend live in the `gateway/cli-backends` doc. Claude CLI reuse expects the OpenClaw process to run on the **same host** as the Claude CLI login: container installs such as Podman do not mount host `~/.claude` into setup or runtime, so there use an Anthropic API key, or choose a provider with OpenClaw-managed OAuth such as OpenAI Codex. The canonical config prefers the `anthropic/*` model ref plus a CLI runtime override:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-8" },
      models: {
        "anthropic/claude-opus-4-8": {
          agentRuntime: { id: "claude-cli" },
        },
      },
    },
  },
}
```

Legacy `claude-cli/claude-opus-4-7` model refs still work for compatibility, but new config should keep provider/model selection as `anthropic/*` and put the execution backend in provider/model runtime policy. For shared production automation, the source recommends an Anthropic API key instead of Claude CLI; OpenClaw also supports subscription-style options from OpenAI Codex, Qwen Cloud, MiniMax, and Z.AI / GLM.

### Billing and `claude -p`

OpenClaw's Claude CLI backend runs the installed Claude Code CLI in non-interactive print mode, using Claude Code's `claude -p` path, which Anthropic currently treats as Agent SDK / programmatic usage. Until June 15, 2026, subscription-plan handling follows Anthropic's active Claude Code rules for the signed-in account. Starting June 15, 2026, subscription-plan `claude -p` usage no longer draws from normal Claude plan limits — it draws from the user's monthly **Agent SDK credit** first, then from usage credits at standard API rates if usage credits are enabled. Console / API-key logins use pay-as-you-go API billing and do not receive the subscription Agent SDK credit; interactive Claude Code still draws from the signed-in Claude plan limits. Anthropic can change Claude Code billing and rate-limit behavior without an OpenClaw release, so check `claude auth status`, `/status`, and Anthropic's linked docs when billing predictability matters — for long-lived gateway hosts, shared automation, and predictable production spend, use an Anthropic API key.

## Thinking defaults (Claude Fable 5, 4.8, and 4.6)

`anthropic/claude-fable-5` always uses adaptive thinking and defaults to `high` effort; because Anthropic does not allow thinking to be disabled for this model, `/think off` and `/think minimal` use `low` effort, and OpenClaw also omits custom temperature values for Fable 5 requests. Claude Opus 4.8 keeps thinking off by default in OpenClaw — when you explicitly enable adaptive thinking with `/think high|xhigh|max`, OpenClaw sends Anthropic's Opus 4.8 effort values; Claude 4.6 models default to `adaptive`. Override per-message with `/think:<level>`, or set it in model params:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-8": {
          params: { thinking: "high" },
        },
      },
    },
  },
}
```

## Prompt caching

OpenClaw supports Anthropic's prompt caching feature for API-key auth, selected via the `cacheRetention` model param. The three values are:

| Value               | Cache duration | Description                            |
| ------------------- | -------------- | -------------------------------------- |
| `"short"` (default) | 5 minutes      | Applied automatically for API-key auth |
| `"long"`            | 1 hour         | Extended cache                         |
| `"none"`            | No caching     | Disable prompt caching                 |

Set `cacheRetention` at the model level, then optionally override per agent. The config merge order is: (1) `agents.defaults.models["provider/model"].params`, then (2) `agents.list[].params` (matching `id`, overriding by key) — so one agent can keep a long-lived cache (`cacheRetention: "long"`) while another agent on the same model disables caching (`cacheRetention: "none"`) for bursty / low-reuse traffic:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" },
        },
      },
    },
    list: [
      { id: "research", default: true },
      { id: "alerts", params: { cacheRetention: "none" } },
    ],
  },
}
```

For **Bedrock Claude**, the source notes three rules: Anthropic Claude models on Bedrock (`amazon-bedrock/*anthropic.claude*`) accept `cacheRetention` pass-through when configured; non-Anthropic Bedrock models are forced to `cacheRetention: "none"` at runtime; and API-key smart defaults also seed `cacheRetention: "short"` for Claude-on-Bedrock refs when no explicit value is set.

## Advanced configuration

### Fast mode

OpenClaw's shared `/fast` toggle supports direct Anthropic traffic (API-key and OAuth to `api.anthropic.com`). `/fast on` maps to `service_tier: "auto"` and `/fast off` maps to `service_tier: "standard_only"`; it can also be set as `params: { fastMode: true }` on a model (e.g. `anthropic/claude-sonnet-4-6`). It is only injected for direct `api.anthropic.com` requests — proxy routes leave `service_tier` untouched — and explicit `serviceTier` or `service_tier` params override `/fast` when both are set. On accounts without Priority Tier capacity, `service_tier: "auto"` may resolve to `standard`.

### Media understanding (image and PDF)

The bundled Anthropic plugin registers image and PDF understanding, and OpenClaw auto-resolves media capabilities from the configured Anthropic auth — no additional config is needed. The default model is `claude-opus-4-8`, and supported input is images and PDF documents. When an image or PDF is attached to a conversation, OpenClaw automatically routes it through the Anthropic media understanding provider.

### 1M context window

Anthropic's 1M context window is available on GA-capable Claude 4.x models such as Opus 4.8, Opus 4.7, Opus 4.6, and Sonnet 4.6, and OpenClaw sizes those models at 1M automatically (an empty `models["anthropic/claude-opus-4-6"]: {}` block is sufficient). Older configs can keep `params.context1m: true`, but OpenClaw no longer sends the retired `context-1m-2025-08-07` beta header — older `anthropicBeta` config entries with that value are ignored during request header resolution, and unsupported older Claude models stay on their normal context window. `params.context1m: true` also applies to the Claude CLI backend (`claude-cli/*`) for eligible GA-capable Opus and Sonnet models, preserving the runtime context window for those CLI sessions to match the direct-API behavior. This requires long-context access on your Anthropic credential; OAuth / subscription token auth keeps its required Anthropic beta headers, but OpenClaw strips the retired 1M beta header if it remains in older config.

### Claude Opus 4.8 1M context

`anthropic/claude-opus-4-8` and its `claude-cli` variant have a 1M context window **by default** — no `params.context1m: true` is needed.

## Troubleshooting

The source page documents four auth-related failure cases:

- **401 errors / token suddenly invalid** — Anthropic token auth expires and can be revoked; for new setups, use an Anthropic API key instead.
- **`No API key found for provider "anthropic"`** — Anthropic auth is **per agent**, so new agents do not inherit the main agent's keys; re-run onboarding for that agent (or configure an API key on the gateway host), then verify with `openclaw models status`.
- **`No credentials found for profile "anthropic:default"`** — run `openclaw models status` to see which auth profile is active, then re-run onboarding or configure an API key for that profile path.
- **No available auth profile (all in cooldown)** — check `openclaw models status --json` for `auth.unusableProfiles`; Anthropic rate-limit cooldowns can be model-scoped, so a sibling Anthropic model may still be usable — add another Anthropic profile or wait for cooldown.

**Source**: OpenClaw documentation — `providers/anthropic` (mirror `inbox/openclaw_docs/providers/anthropic.md`)
**Last Updated**: 2026-06-22
**Status**: Active
