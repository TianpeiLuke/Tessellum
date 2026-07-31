---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - oauth
keywords:
  - openclaw oauth subscription auth
  - auth-profiles.json token sink
  - openai codex chatgpt oauth pkce
  - anthropic claude cli reuse setup-token
  - oauth refresh expiry file lock
  - multiple accounts profiles auth.order
  - per-session model profile override
  - read-through credential inheritance
topics:
  - OpenClaw
  - OAuth
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/oauth
access_control_group: ["general"]
---

# OpenClaw — OAuth Subscription Auth, Token Sink, and Multi-Account Routing

## Overview

This note explains the OpenClaw **OAuth subscription-auth** concept end-to-end, mirroring the `concepts/oauth` source page: why OpenClaw keeps `auth-profiles.json` as a single **token sink**, where credentials are stored, the PKCE OAuth exchange for OpenAI Codex (ChatGPT OAuth) and the Anthropic setup-token / Claude CLI paths, automatic refresh + expiry under a file lock, and how to run multiple accounts via separate agents or multiple profiles with deterministic routing. OpenClaw supports "subscription auth" via OAuth for providers that offer it — notably **OpenAI Codex (ChatGPT OAuth)** — while for Anthropic the practical split is now an Anthropic API key (normal Anthropic API billing) versus Anthropic Claude CLI / subscription auth inside OpenClaw (which Anthropic staff told the project is allowed again). For Anthropic in production, API key auth is the safer recommended path. OpenAI Codex OAuth is explicitly supported for use in external tools like OpenClaw. OpenClaw also supports **provider plugins** that ship their own OAuth or API-key flows, run via `openclaw models auth login --provider <id>`.

OpenClaw stores both OpenAI API-key auth and ChatGPT/Codex OAuth under the canonical provider id `openai`. Older `openai-codex:*` profile ids and `auth.order.openai-codex` entries are legacy state repaired by `openclaw doctor --fix`; use `openai:*` profile ids and `auth.order.openai` for new config.

## The Token Sink (Why It Exists)

OAuth providers commonly mint a **new refresh token** during login/refresh flows. Some providers (or OAuth clients) can invalidate older refresh tokens when a new one is issued for the same user/app. The practical symptom is that if you log in via OpenClaw *and* via Claude Code / Codex CLI, one of them randomly gets "logged out" later. To reduce that, OpenClaw treats `auth-profiles.json` as a **token sink**: the runtime reads credentials from one place; multiple profiles can be kept and routed deterministically; external CLI reuse is provider-specific (Codex CLI can bootstrap an empty `openai:default` profile, but once OpenClaw has a local OAuth profile the local refresh token is canonical — if that local refresh token is rejected, OpenClaw can use a usable same-account Codex CLI token as a runtime-only fallback, while other integrations can remain externally managed and re-read their CLI auth store); and status/startup paths that already know the configured provider set scope external CLI discovery to that set, so an unrelated CLI login store is not probed for a single-provider setup.

## Storage (Where Tokens Live)

Secrets are stored in agent auth stores. The auth profiles (OAuth + API keys + optional value-level refs) live at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`, and a legacy compatibility file `~/.openclaw/agents/<agentId>/agent/auth.json` is also read (static `api_key` entries are scrubbed when discovered). A legacy import-only file `~/.openclaw/credentials/oauth.json` is still supported but is not the main store — it is imported into `auth-profiles.json` on first use. All of the above also respect `$OPENCLAW_STATE_DIR` (state dir override); the full reference is the gateway configuration auth-storage section, and static secret refs plus runtime snapshot activation behavior are covered by Secrets Management.

When a secondary agent has no local auth profile, OpenClaw uses **read-through inheritance** from the default/main agent store — it does **not** clone the main agent's `auth-profiles.json` on read. OAuth refresh tokens are especially sensitive: normal copy flows skip them by default because some providers rotate or invalidate refresh tokens after use. Configure a separate OAuth login for an agent when it needs an independent account.

## Anthropic Legacy Token Compatibility

Anthropic's public Claude Code docs say direct Claude Code use stays within Claude subscription limits, and Anthropic staff told the project that OpenClaw-style Claude CLI usage is allowed again. OpenClaw therefore treats Claude CLI reuse and `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy. For other subscription-style options in OpenClaw, the page points to OpenAI Codex, Qwen Cloud Coding Plan, MiniMax Coding Plan, and Z.AI / GLM Coding Plan provider pages. OpenClaw also exposes Anthropic **setup-token** as a supported token-auth path, but it now prefers Claude CLI reuse and `claude -p` when available.

## Anthropic Claude CLI Migration

OpenClaw supports Anthropic Claude CLI reuse again. If you already have a local Claude login on the host, onboarding/configure can reuse it directly.

## OAuth Exchange (How Login Works)

OpenClaw's interactive login flows are implemented in `openclaw/plugin-sdk/llm` and wired into the wizards/commands. The page documents two exchange shapes — the Anthropic setup-token path and the OpenAI Codex PKCE path.

### Anthropic setup-token

The setup-token flow shape is: (1) start Anthropic setup-token or paste-token from OpenClaw; (2) OpenClaw stores the resulting Anthropic credential in an auth profile; (3) model selection stays on `anthropic/...`; (4) existing Anthropic auth profiles remain available for rollback/order control.

### OpenAI Codex (ChatGPT OAuth)

OpenAI Codex OAuth is explicitly supported for use outside the Codex CLI, including OpenClaw workflows. The login command still uses the canonical OpenAI provider id:

```bash
openclaw models auth login --provider openai
```

Use `--profile-id openai:<name>` for multiple ChatGPT/Codex OAuth accounts in one agent. Do not use `openai-codex:<name>` for new profiles. Doctor migrates that older prefix to a collision-free `openai:*` profile id; run `openclaw models auth list --provider openai` after repair before copying profile ids into `auth.order` or `/model ...@<profileId>`.

The login is a **PKCE** exchange with the following flow shape: (1) generate PKCE verifier/challenge + random `state`; (2) open `https://auth.openai.com/oauth/authorize?...`; (3) try to capture the callback on `http://127.0.0.1:1455/auth/callback`; (4) if the callback can't bind (or you're remote/headless), paste the redirect URL/code; (5) exchange at `https://auth.openai.com/oauth/token`; (6) extract `accountId` from the access token and store `{ access, refresh, expires, accountId }`. The wizard path is `openclaw onboard` → auth choice `openai`.

## Refresh + Expiry

Profiles store an `expires` timestamp. At runtime, if `expires` is in the future the stored access token is used; if expired, OpenClaw refreshes (under a **file lock**) and overwrites the stored credentials. If a secondary agent reads an inherited main-agent OAuth profile, refresh writes back to the **main agent store** instead of copying the refresh token into the secondary agent store. As an exception, some external CLI credentials stay externally managed: OpenClaw re-reads those CLI auth stores instead of spending copied refresh tokens. The Codex CLI bootstrap is intentionally narrower — it seeds an empty `openai:default` profile, then OpenClaw-owned refreshes keep the local profile canonical; if the local Codex refresh fails and Codex CLI has a usable token for the same account, OpenClaw may use that token for the current runtime request without writing it back to `auth-profiles.json`. The refresh flow is automatic; you generally don't need to manage tokens manually.

## Multiple Accounts (Profiles) + Routing

There are two patterns for running more than one account.

### 1) Preferred: separate agents

If you want "personal" and "work" to never interact, use isolated agents (separate sessions + credentials + workspace):

```bash
openclaw agents add work
openclaw agents add personal
```

Then configure auth per-agent (via the wizard) and route chats to the right agent.

### 2) Advanced: multiple profiles in one agent

`auth-profiles.json` supports multiple profile IDs for the same provider. You pick which profile is used either globally via config ordering (`auth.order`) or per-session via `/model ...@<profileId>` — for example the session override `/model Opus@anthropic:work`. To see what profile IDs exist, run `openclaw channels list --json` (it shows `auth[]`). The page links Model failover (rotation + cooldown rules) and Slash commands (command surface) as related docs.

**Source**: OpenClaw documentation — `concepts/oauth` (mirror `inbox/openclaw_docs/concepts/oauth.md`)
**Last Updated**: 2026-06-22
**Status**: Active
