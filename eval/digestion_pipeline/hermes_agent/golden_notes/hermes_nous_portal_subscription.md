---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_providers
  - nous_portal
keywords:
  - nous portal subscription
  - hermes setup --portal
  - tool gateway
  - one oauth login
  - 300+ frontier models
  - jwt token handling
  - provider nous config
topics:
  - Hermes Agent
  - Inference Providers
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/integrations/nous-portal
access_control_group: ["general"]
---

# Hermes Agent — Nous Portal Subscription

## Overview

The Nous Portal is Nous Research's unified subscription gateway and **the recommended way to run Hermes Agent**: one OAuth login replaces separate accounts, API keys, and billing relationships across every model lab, search API, image generator, and browser provider you would otherwise wire up by hand. A single `hermes setup --portal` command runs the OAuth flow, lets you pick a Nous model, sets Nous as your inference provider in `config.yaml`, and turns on the Tool Gateway — leaving you ready to `hermes chat` immediately. Under the hood the Portal proxies a curated catalog of 300+ agentic models through OpenRouter (billed against your Nous subscription) and unlocks the five-backend Tool Gateway. This note is the config-side procedure for the subscription; the Tool Gateway *feature* page is owned by SP05 and the per-provider OAuth-over-SSH setup guide by SP15 (link-outs, not duplicated here).

## What's in the subscription

The subscription bundles four things behind one OAuth login:

- **300+ frontier models, one bill** — the Portal proxies a curated catalog of agentic models from across the ecosystem (Anthropic Claude, OpenAI GPT, Google Gemini, DeepSeek, Qwen, Kimi/Moonshot, GLM/Zhipu, MiniMax, xAI Grok, [NVIDIA Nemotron](../../term_dictionary/term_nemotron.md), Tencent Hunyuan, Xiaomi MiMo, StepFun, plus Nous's own Hermes 4 chat models and 280+ more), billed against your Nous subscription instead of one credit balance per lab. Routing happens through OpenRouter under the hood, so availability and failover match an OpenRouter key. You switch between models with `/model` mid-session — "no new credentials, no top-ups, no surprise zero-balance errors."
- **The Nous Tool Gateway** — the same subscription unlocks five tool backends behind one login: Web search & extract (Firecrawl), Image generation (FAL — nine image models under one endpoint), Text-to-speech (OpenAI TTS, enabling voice mode), Cloud browser automation (Browser Use — headless Chromium for `browser_navigate`/`browser_click`/`browser_type`/`browser_vision`), and Cloud terminal sandbox (Modal, optional add-on). Without the gateway, hooking each up means five separate signups, dashboards, and top-up flows. The gateway is opt-in per tool — see Mixing the gateway below.
- **Nous Chat** — the Portal account also covers `chat.nousresearch.com`, the web chat interface with the same model catalog, for when you are away from the terminal or doing non-agent work.
- **No credentials in your dotfiles** — because everything routes through one OAuth-authenticated session, you do not accumulate a `.env` of long-lived API keys. The refresh token at `~/.hermes/auth.json` is the only credential on disk, and Hermes mints short-lived JWTs from it per request (see Token handling). Native Windows benefits most: one OAuth covers the model and every gateway tool, giving Windows users parity with macOS/Linux without manually configuring four backends.

## A note on Hermes 4

Nous Research's own **Hermes 4** family (Hermes-4-70B, Hermes-4-405B) is available through the Portal at heavily discounted rates. These are frontier hybrid-reasoning chat models — strong at math, science, instruction following, schema adherence, roleplay, and long-form writing. They are **not recommended for use inside Hermes Agent**: Hermes 4 is tuned for chat and reasoning, not the rapid-fire tool-calling loop the agent relies on. For agent work, pick a frontier agentic model from the catalog instead:

```bash
/model anthropic/claude-sonnet-4.6     # best general-purpose agentic model
/model openai/gpt-5.5-pro              # strong reasoning + tool calling
/model google/gemini-3-pro-preview     # huge context window
/model deepseek/deepseek-v4-pro        # cost-effective coder
```

The Portal's own model info page carries the same warning, so this is the official guidance from Nous Research, not a Hermes-side opinion.

## Setup

**Fresh install — one command:**

```bash
hermes setup --portal
```

This runs the full setup in one shot: (1) opens your browser to portal.nousresearch.com for OAuth login, (2) stores the refresh token at `~/.hermes/auth.json`, (3) lets you pick a Nous model from the curated list (or skip to keep your current one), (4) sets Nous as your inference provider in `~/.hermes/config.yaml` (when you pick a model), (5) turns on the Tool Gateway (web, image, TTS, browser routing), and (6) returns you to your terminal ready to `hermes chat`. If you do not have a subscription yet, sign up at portal.nousresearch.com/manage-subscription first.

**Existing install — add Portal alongside other providers:** if you already have Hermes configured with OpenRouter, Anthropic, or any other provider, run `hermes model` and pick "Nous Portal" from the provider list. Your existing providers stay configured; the Portal becomes one of your available providers, not your only one, switchable with `/model` mid-session or `hermes model` between sessions.

**Headless / SSH / remote setup:** OAuth needs a browser, but the loopback callback runs on the machine where Hermes is running. For remote hosts, the same patterns work for the Portal as for any other OAuth-based provider (`ssh -L` port forwarding, `--manual-paste` for browser-only environments like Cloud Shell / Codespaces) — see the OAuth over SSH guide (SP15).

**Profile setup:** if you use Hermes profiles, the Portal refresh token is automatically shared across all profiles via a shared token store. Sign in once on any profile and the rest pick it up automatically — no need to repeat the OAuth flow per profile.

## Using the Portal day-to-day

**Inspecting what's wired up** — the `hermes portal` subcommand family:

```bash
hermes portal            # log in to Nous Portal + set it up (one-shot onboarding)
hermes portal info       # login status, subscription info, model + gateway routing
hermes portal status     # alias for `portal info`
hermes portal tools      # detailed Tool Gateway catalog with per-tool routing
hermes portal open       # open the subscription management page in your browser
```

`hermes portal` (no subcommand) is the human-readable alias for `hermes auth add nous --type oauth` — it logs you in, lets you pick a Nous model, sets Nous as your inference provider, and offers the Tool Gateway opt-in (identical to `hermes setup --portal`). `hermes portal info` shows the high-level overview: auth status, Portal URL, whether Nous is the active inference provider, and per-tool Tool Gateway routing (web search, image generation, TTS, browser automation, cloud terminal).

**Switching models** — inside a session use `/model anthropic/claude-sonnet-4.6` (or `/model` to open the arrow-key picker); outside a session use the full setup wizard via `hermes model`.

**Mixing the gateway with your own backends** — the Tool Gateway is opt-in per tool, not all-or-nothing. Use `hermes tools` to pick backends per tool (e.g. route web search and image generation through "Nous Subscription" while keeping your own Browserbase key for the browser). The managed backends show up in `hermes tools` whether or not you are logged into Nous Portal — picking "Nous Subscription" before authenticating runs the Portal login inline without changing your inference provider or touching other tools. Full per-tool config matrix → Tool Gateway docs (SP05).

**Subscription management** — manage your plan, view usage, or upgrade/cancel via the web at portal.nousresearch.com/manage-subscription or the CLI shortcut `hermes portal open`.

## Configuration reference

After `hermes setup --portal`, `~/.hermes/config.yaml` will look like:

```yaml
model:
  provider: nous
  default: anthropic/claude-sonnet-4.6     # or whatever model you picked
  base_url: https://inference-api.nousresearch.com/v1
```

The Tool Gateway settings live under their respective tool sections:

```yaml
web:
  backend: nous       # web search/extract routes through Tool Gateway

image_gen:
  provider: nous

tts:
  provider: nous

browser:
  backend: nous
```

The OAuth refresh token is stored separately at `~/.hermes/auth.json` (not in `config.yaml` — credentials and configuration are kept separate by design).

## Token handling

Hermes mints a short-lived JWT from your stored Portal refresh token on each inference call rather than reusing a long-lived API key. The token lifecycle is fully automatic — refresh, mint, retry on transient 401 — and you never see it. If the Portal invalidates the refresh token (password change, manual revoke, session expiry), the invalid refresh token is **quarantined locally** so Hermes stops replaying it and you do not see a stream of identical 401s. The next call surfaces a clear "re-authentication required" message; run `hermes auth add nous` to log in again, and the quarantine clears on the next successful login.

## Troubleshooting

- **`hermes portal info` shows "not logged in"** — you have not completed the OAuth flow, or your refresh token was wiped. Run `hermes portal`, or use `hermes model` and re-select Nous Portal.
- **"re-authentication required" mid-session** — your Portal refresh token was invalidated (password change, manual revoke, session expiry). Run `hermes auth add nous`; your next request uses the new credentials and any quarantine on the old token clears automatically on successful re-login.
- **Want a specific provider model the Portal doesn't expose** — the Portal proxies through OpenRouter, so any OpenRouter-supported model is generally available. If a model is not appearing in `/model`, try the OpenRouter-style slug directly (e.g. `/model anthropic/claude-opus-4.6`). If genuinely missing, open an issue.
- **Bills not appearing on my Portal account** — check `hermes portal info` first; if it shows a different provider (`Model: currently openrouter` instead of `using Nous as inference provider`), your local config has drifted. Run `hermes model`, pick Nous Portal, and the next request routes through your subscription.

## See also

The source closes with link-outs to the Tool Gateway feature page (full per-tool config + pricing), the Subscription proxy (use your Portal subscription from non-Hermes tools), Voice mode (Portal's OpenAI TTS), AI Providers (full provider catalog), OAuth over SSH (remote/browser-only login), and Profiles (multiple configs sharing one Portal login) — each owned by its respective sub-plan (SP05/SP08/SP09/SP15).

**Source**: `inbox/hermes_agent_docs/integrations/nous-portal.md` · https://hermes-agent.nousresearch.com/docs/integrations/nous-portal
**Last Updated**: 2026-06-19
**Status**: Active
