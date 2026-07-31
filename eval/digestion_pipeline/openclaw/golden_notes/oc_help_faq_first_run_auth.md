---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - first_run
keywords:
  - openclaw first run auth
  - claude subscription vs api key
  - codex oauth openai
  - gemini cli oauth
  - aws bedrock converse provider
  - http 429 rate_limit_error
  - dashboard localhost remote auth
  - auth profiles gateway host
  - local model viability
  - region pinned hosted traffic
topics:
  - OpenClaw
  - First-run FAQ
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq-first-run
access_control_group: ["general"]
---

# OpenClaw — First-run FAQ: Authentication, Subscriptions & Dashboard

## Overview

This note is the **auth / subscriptions / dashboard** half of the OpenClaw first-run FAQ (`help/faq-first-run`, the single `## Quick start and first-run setup` accordion group; its install/runtime/hosting Q&As are the sibling note `oc_help_faq_first_run_install`). It is a procedure note: how to choose between subscription and API-key authentication across Anthropic Claude (Pro/Max), OpenAI Code (Codex) OAuth, Google Gemini CLI OAuth, and Amazon Bedrock; how to diagnose the `HTTP 429 rate_limit_error` from Anthropic; whether a local-only model is viable; how to keep hosted model traffic region-pinned; and how to authenticate the Control UI dashboard on localhost versus remote. Every config key, env var, and CLI command below is copied verbatim from the source page.

## Subscription vs API key (do I need a subscription?)

You do **not** need a Claude or OpenAI subscription to run OpenClaw. You can authenticate providers with **API keys** (Anthropic/OpenAI/others) or run **local-only models** so data stays on your device; subscriptions (Claude Pro/Max or OpenAI Codex) are optional ways to authenticate those providers. For Anthropic specifically the practical split is:

- **Anthropic API key**: normal Anthropic API billing.
- **Claude CLI / Claude subscription auth in OpenClaw**: Anthropic staff told the project this usage is allowed again, and OpenClaw is treating `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy.

For long-lived gateway hosts, Anthropic API keys are the more predictable setup. OpenClaw also supports other hosted subscription-style options including **Qwen Cloud Coding Plan**, **MiniMax Coding Plan**, and **Z.AI / GLM Coding Plan**.

## Anthropic Claude subscription auth (Pro / Max)

You **can** use a Claude Max subscription without an API key. Anthropic staff told the project OpenClaw-style Claude CLI usage is allowed again, so OpenClaw treats Claude subscription auth and `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy. Claude Pro and Max subscription auth are both supported (the source treats them together). The **Anthropic setup-token** remains a supported OpenClaw token path, but OpenClaw now **prefers Claude CLI reuse and `claude -p`** when available. For production or multi-user workloads, Anthropic API key auth is the safer, more predictable choice.

## OpenAI Code (Codex) auth

OpenClaw supports **OpenAI Code (Codex) via OAuth (ChatGPT sign-in)**, and OpenAI explicitly allows subscription OAuth usage in external tools/workflows like OpenClaw. Onboarding can run the OAuth flow for you. Use the model ref **`openai/gpt-5.5`** for the common setup: ChatGPT/Codex subscription auth plus native Codex app-server execution. To sign in with subscription OAuth, run `openclaw models auth login --provider openai`. Keep the model ref as `openai/gpt-5.5`; legacy Codex model refs are legacy config that `openclaw doctor --fix` rewrites.

Note that `openai` is the **provider and auth-profile id for both** OpenAI API keys and ChatGPT/Codex OAuth. Older configs used it as a model prefix, and you may still see a legacy OpenAI Codex prefix in legacy config and migration warnings. The mapping the page gives is:

- `openai/gpt-5.5` = ChatGPT/Codex subscription auth with native Codex runtime for agent turns.
- legacy Codex GPT-5.5 ref = legacy model route repaired by `openclaw doctor --fix`.
- `openai/gpt-5.5` **plus an ordered `openai` API-key profile** = API-key auth for an OpenAI agent model.
- legacy Codex auth-profile ids = legacy auth-profile id migrated by `openclaw doctor --fix`.

If you want the direct OpenAI Platform billing/limit path, set `OPENAI_API_KEY` (direct OpenAI API-key access remains available for non-agent OpenAI API surfaces and for agent models through an ordered `openai` API-key profile). Codex OAuth uses **OpenAI-managed, plan-dependent quota windows**, so those limits can differ from the ChatGPT website/app experience even on the same account. `openclaw models status` can show the currently visible provider usage/quota windows, but OpenClaw does not invent or normalize ChatGPT-web entitlements into direct API access — for the direct OpenAI Platform billing/limit path, use `openai/*` with an API key.

## Google Gemini CLI OAuth

Gemini CLI uses a **plugin auth flow**, not a client id or secret in `openclaw.json`. Steps:

1. Install Gemini CLI locally so `gemini` is on `PATH` — Homebrew: `brew install gemini-cli`; npm: `npm install -g @google/gemini-cli`.
2. Enable the plugin: `openclaw plugins enable google`.
3. Login: `openclaw models auth login --provider google-gemini-cli --set-default`.
4. Default model after login: `google-gemini-cli/gemini-3-flash-preview`.
5. If requests fail, set `GOOGLE_CLOUD_PROJECT` or `GOOGLE_CLOUD_PROJECT_ID` on the gateway host.

This stores **OAuth tokens in auth profiles on the gateway host**.

## Amazon Bedrock

AWS Bedrock is supported: OpenClaw has a bundled **Amazon Bedrock (Converse)** provider. With AWS env markers present, OpenClaw can **auto-discover** the streaming/text Bedrock catalog and merge it as an implicit `amazon-bedrock` provider; otherwise you can explicitly enable `plugins.entries.amazon-bedrock.config.discovery.enabled` or add a manual provider entry. If you prefer a managed key flow, an OpenAI-compatible proxy in front of Bedrock is still a valid option.

## HTTP 429 rate_limit_error from Anthropic

A `HTTP 429 rate_limit_error` means your **Anthropic quota/rate limit is exhausted for the current window**. If you use **Claude CLI**, wait for the window to reset or upgrade your plan. If you use an **Anthropic API key**, check the Anthropic Console for usage/billing and raise limits as needed. If the message is specifically `Extra usage is required for long context requests`, the request is trying to use Anthropic's **1M context window** (a GA-capable 1M Claude 4.x model or legacy `context1m: true` config); that only works when your credential is eligible for long-context billing (API-key billing or the OpenClaw Claude-login path with Extra Usage enabled). Tip: set a **fallback model** so OpenClaw can keep replying while a provider is rate-limited.

## Local-only models and region pinning

A local model is **usually not** OK for casual chats: OpenClaw needs large context plus strong safety, and small cards truncate and leak. If you must, run the **largest** model build you can locally (LM Studio); smaller/quantized models increase prompt-injection risk. To keep **hosted model traffic region-pinned**, pick region-pinned endpoints — OpenRouter exposes US-hosted options for MiniMax, Kimi, and GLM, so choose the US-hosted variant to keep data in-region. You can still list Anthropic/OpenAI alongside these by using `models.mode: "merge"` so fallbacks stay available while respecting the regioned provider you select.

## Authenticating the dashboard (localhost vs remote)

**Localhost (same machine):** open `http://127.0.0.1:18789/`. If it asks for shared-secret auth, paste the configured token or password into Control UI settings. Token source: `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`). Password source: `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`). If no shared secret is configured yet, generate a token with `openclaw doctor --generate-gateway-token`.

**Not on localhost:**

- **Tailscale Serve (recommended):** keep bind loopback, run `openclaw gateway --tailscale serve`, open `https://<magicdns>/`. If `gateway.auth.allowTailscale` is `true`, identity headers satisfy Control UI/WebSocket auth (no pasted shared secret, assumes trusted gateway host); HTTP APIs still require shared-secret auth unless you deliberately use private-ingress `none` or trusted-proxy HTTP auth.
- **Tailnet bind:** run `openclaw gateway --bind tailnet --token "<token>"` (or configure password auth), open `http://<tailscale-ip>:18789/`, then paste the matching shared secret in dashboard settings.
- **Identity-aware reverse proxy:** keep the Gateway behind a trusted proxy, configure `gateway.auth.mode: "trusted-proxy"`, then open the proxy URL. Same-host loopback proxies require explicit `gateway.auth.trustedProxy.allowLoopback = true`.
- **SSH tunnel:** `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/`. Shared-secret auth still applies over the tunnel; paste the configured token or password if prompted.

**Source**: OpenClaw documentation — `help/faq-first-run` (auth/subscriptions/dashboard cluster; mirror `inbox/openclaw_docs/help/faq-first-run.md`)
**Last Updated**: 2026-06-22
**Status**: Active
