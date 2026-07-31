---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - secrets
keywords:
  - openclaw secretref credential surface
  - secrets configure apply audit
  - openclaw.json supported secretref paths
  - auth-profiles.json keyref tokenref
  - oauth policy guard secretref
  - structured object secretref env source
  - web search provider key precedence
  - unsupported minted rotating oauth-durable credentials
topics:
  - OpenClaw
  - SecretRef Credential Surface
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/secretref-credential-surface
access_control_group: ["general"]
---

# OpenClaw — The SecretRef Credential Surface

## Overview

This note models the canonical **SecretRef credential surface**: the authoritative list of which OpenClaw config paths are eligible for SecretRef resolution by the `secrets configure` / `secrets apply` / `secrets audit` tooling, and which credential classes are explicitly out of scope. It mirrors the `reference/secretref-credential-surface` source page, covering the scope intent (in/out), the two supported config files (`openclaw.json` and `auth-profiles.json`), the structured-object SecretRef requirement, the OAuth policy guard, marker persistence, web-search precedence rules, and the unsupported (minted / rotating / OAuth-durable / session-like) credentials plus their rationale.

## Scope Intent

The page defines the canonical SecretRef credential surface by a single guiding distinction:

- **In scope** — strictly user-supplied credentials that OpenClaw does not mint or rotate.
- **Out of scope** — runtime-minted or rotating credentials, OAuth refresh material, and session-like artifacts.

A credential is therefore eligible for SecretRef management exactly when the operator supplies it and OpenClaw treats it as static external material; anything OpenClaw itself generates, refreshes, or that behaves like a session token falls outside the surface (see `## Unsupported credentials and Rationale`).

## Supported credentials

There are two supported config files, both fully covered by `secrets configure` + `secrets apply` + `secrets audit`: `openclaw.json` (the gateway config) and `auth-profiles.json` (the auth-profile store).

### `openclaw.json` targets

The `openclaw.json` supported paths (bounded by the `secretref-supported-list-start` / `secretref-supported-list-end` markers in source) group into the following categories. Representative verbatim paths are listed per category — see References for the full source list.

- **Model providers** — `models.providers.*.apiKey`, `models.providers.*.headers.*`, `models.providers.*.request.auth.token`, `models.providers.*.request.auth.value`, `models.providers.*.request.headers.*`. These are the provider API keys and request auth/header credentials for configured LLM providers.
- **Provider / proxy TLS material** — `models.providers.*.request.tls.ca`, `models.providers.*.request.tls.cert`, `models.providers.*.request.tls.key`, `models.providers.*.request.tls.passphrase`, plus the proxy equivalents `models.providers.*.request.proxy.tls.{ca,cert,key,passphrase}`. These secure the upstream (and proxy) TLS hop for a provider request.
- **Agent / talk / TTS / skills keys** — `skills.entries.*.apiKey`, `agents.defaults.memorySearch.remote.apiKey`, `agents.list[].tts.providers.*.apiKey`, `agents.list[].memorySearch.remote.apiKey`, `talk.providers.*.apiKey`, `talk.realtime.providers.*.apiKey`, `messages.tts.providers.*.apiKey`, `tools.web.fetch.firecrawl.apiKey`.
- **Plugin entries** — the canonical web-search and realtime/voice plugin keys, e.g. `plugins.entries.brave.config.webSearch.apiKey`, `plugins.entries.exa.config.webSearch.apiKey`, `plugins.entries.google.config.webSearch.apiKey`, `plugins.entries.perplexity.config.webSearch.apiKey`, `plugins.entries.tavily.config.webSearch.apiKey`, plus `plugins.entries.acpx.config.mcpServers.*.env.*`, `plugins.entries.codex.config.appServer.authToken`, `plugins.entries.codex.config.appServer.headers.*`, `plugins.entries.voice-call.config.{realtime,streaming,tts}.providers.*.apiKey`, and `plugins.entries.voice-call.config.twilio.authToken`. (Source enumerates brave/exa/google/xai/moonshot/perplexity/firecrawl/minimax/tavily/parallel/google-meet web-search/realtime keys.)
- **Legacy web search** — `tools.web.search.*.apiKey` and `tools.web.search.apiKey` (still resolved during the compatibility window — see Notes below).
- **Gateway auth** — `gateway.auth.password`, `gateway.auth.token`, `gateway.remote.token`, `gateway.remote.password`, and `cron.webhookToken`.
- **Messaging channels** — per-channel bot/app/user tokens, secrets, and passwords (and their `accounts.*` per-account variants), e.g. `channels.telegram.botToken` / `channels.telegram.webhookSecret`, `channels.slack.{botToken,appToken,userToken,signingSecret}`, `channels.sms.authToken`, `channels.discord.token` / `channels.discord.pluralkit.token` / `channels.discord.voice.tts.providers.*.apiKey`, `channels.irc.password` / `channels.irc.nickserv.password`, `channels.feishu.{appSecret,encryptKey,verificationToken}`, `channels.qqbot.clientSecret`, `channels.msteams.appPassword`, `channels.mattermost.botToken`, `channels.matrix.{accessToken,password}`, `channels.nextcloud-talk.{botSecret,apiPassword}`, and `channels.zalo.{botToken,webhookSecret}`.
- **Compatibility exception** — `channels.googlechat.serviceAccount` and `channels.googlechat.accounts.*.serviceAccount` are supported **via a sibling `serviceAccountRef`** (explicitly noted as a compatibility exception).

### `auth-profiles.json` targets

Two paths in `auth-profiles.json` are supported (also via `secrets configure` + `secrets apply` + `secrets audit`):

- `profiles.*.keyRef` — for `type: "api_key"`; **unsupported when `auth.profiles.<id>.mode = "oauth"`**.
- `profiles.*.tokenRef` — for `type: "token"`; **unsupported when `auth.profiles.<id>.mode = "oauth"`**.

### Notes (resolution rules)

The source `Notes` block captures the load-bearing resolution and persistence rules:

- **Auth-profile plan targets require `agentId`.** Plan entries target `profiles.*.key` / `profiles.*.token` and write sibling refs (`keyRef` / `tokenRef`). Auth-profile refs are included in runtime resolution and audit coverage.
- **Structured-object SecretRef requirement.** In `openclaw.json`, SecretRefs must use structured objects such as `{"source":"env","provider":"default","id":"DISCORD_BOT_TOKEN"}`. Legacy `secretref-env:<ENV_VAR>` marker strings are rejected on SecretRef credential paths; run `openclaw doctor --fix` to migrate valid markers.
- **OAuth policy guard.** `auth.profiles.<id>.mode = "oauth"` cannot be combined with SecretRef inputs for that profile. Startup/reload and auth-profile resolution fail fast when this policy is violated.
- **Marker persistence (model providers).** For SecretRef-managed model providers, generated `agents/*/agent/models.json` entries persist **non-secret markers (not resolved secret values)** for `apiKey`/header surfaces. Marker persistence is source-authoritative: OpenClaw writes markers from the active source config snapshot (pre-resolution), not from resolved runtime secret values.
- **Web-search precedence.** In explicit provider mode (`tools.web.search.provider` set), only the selected provider key is active. In auto mode (`tools.web.search.provider` unset), only the first provider key that resolves by precedence is active, and non-selected provider refs are treated as inactive until selected. Legacy `tools.web.search.*` provider paths still resolve during the compatibility window, but the canonical SecretRef surface is `plugins.entries.<plugin>.config.webSearch.*`.

## Unsupported credentials and Rationale

The following out-of-scope credentials are bounded in source by the `secretref-unsupported-list-start` / `secretref-unsupported-list-end` markers:

- `commands.ownerDisplaySecret`
- `hooks.token`
- `hooks.gmail.pushToken`
- `hooks.mappings[].sessionKey`
- `auth-profiles.oauth.*`
- `channels.discord.threadBindings.webhookToken`
- `channels.discord.accounts.*.threadBindings.webhookToken`
- `channels.whatsapp.creds.json`
- `channels.whatsapp.accounts.*.creds.json`

**Rationale:** these credentials are minted, rotated, session-bearing, or OAuth-durable classes that do not fit read-only external SecretRef resolution. This is the direct mirror of the scope-intent boundary — OpenClaw will not place its own minted/rotating or session-like material under operator-supplied SecretRef management.

**Source**: OpenClaw documentation — `reference/secretref-credential-surface` (mirror `inbox/openclaw_docs/reference/secretref-credential-surface.md`)
**Last Updated**: 2026-06-22
**Status**: Active
