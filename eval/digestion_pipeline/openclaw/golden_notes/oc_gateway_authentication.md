---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - authentication
keywords:
  - openclaw model authentication
  - models auth login
  - anthropic claude cli reuse
  - api key rotation provider keys
  - models status probe check
  - auth profile sqlite store
  - per-session per-agent credential
  - removing provider auth auth-revoked
topics:
  - OpenClaw
  - Gateway Authentication
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/authentication
access_control_group: ["general"]
---

# OpenClaw — Authenticating to Model Providers

## Overview

This note is the procedure for authenticating an OpenClaw gateway to its **model providers** — putting credentials on the gateway host, reusing a local Claude CLI login, checking auth status, rotating keys, removing provider auth, and pinning which credential a run uses. It mirrors the `gateway/authentication` source page. OpenClaw supports OAuth and API keys for model providers; for always-on gateway hosts, API keys are usually the most predictable option, while subscription/OAuth flows are supported when they match the provider account model. This page is the model-provider authentication reference; **gateway connection** authentication (token, password, trusted-proxy) is a separate concern covered by `Configuration` and `Trusted Proxy Auth`.

## Recommended setup (API key, any provider)

For a long-lived gateway, start with an API key for the chosen provider. For Anthropic specifically, API key auth is still the most predictable server setup, but OpenClaw also supports reusing a local Claude CLI login.

1. Create an API key in the provider console.
2. Put it on the **gateway host** (the machine running `openclaw gateway`):

```bash
export <PROVIDER>_API_KEY="..."
openclaw models status
```

3. If the Gateway runs under systemd/launchd, prefer putting the key in `~/.openclaw/.env` so the daemon can read it, then restart the daemon (or the Gateway process) and re-check:

```bash
cat >> ~/.openclaw/.env <<'EOF'
<PROVIDER>_API_KEY=...
EOF

openclaw models status
openclaw doctor
```

If you'd rather not manage env vars yourself, onboarding can store API keys for daemon use via `openclaw onboard`. Env inheritance details (`env.shellEnv`, `~/.openclaw/.env`, systemd/launchd) are documented on the Help page.

## Anthropic: Claude CLI and token compatibility

Anthropic setup-token auth is still available as a supported token path. Anthropic staff has since told the project that OpenClaw-style Claude CLI usage is allowed again, so OpenClaw treats Claude CLI reuse and `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy. When Claude CLI reuse is available on the host, that is now the preferred path. For long-lived gateway hosts, an Anthropic API key is still the most predictable setup; to reuse an existing Claude login on the same host, use the Anthropic Claude CLI path in onboarding/configure.

Recommended host setup for Claude CLI reuse:

```bash
# Run on the gateway host
claude auth login
claude auth status --text
openclaw models auth login --provider anthropic --method cli --set-default
```

This is a two-step setup: (1) log Claude Code itself into Anthropic on the gateway host, and (2) tell OpenClaw to switch Anthropic model selection to the local `claude-cli` backend and store the matching OpenClaw auth profile. If `claude` is not on `PATH`, either install Claude Code first or set `agents.defaults.cliBackends.claude-cli.command` to the real binary path.

Manual token entry (any provider; writes the per-agent SQLite auth store + updates config) uses `openclaw models auth paste-token --provider openrouter`. The auth profile store keeps credentials only. Legacy `auth-profiles.json` files used this canonical shape — `{ "version": 1, "profiles": { "openrouter:default": { "type": "api_key", "provider": "openrouter", "key": "OPENROUTER_API_KEY" } } }`.

OpenClaw now reads auth profiles from each agent's `openclaw-agent.sqlite`. If an older install still has `auth-profiles.json`, `auth-state.json`, or a flat auth profile file such as `{ "openrouter": { "apiKey": "..." } }`, run `openclaw doctor --fix` to import it into SQLite; doctor keeps timestamped backups beside the original JSON files. Endpoint details such as `baseUrl`, `api`, model ids, headers, and timeouts belong under `models.providers.<id>` in `openclaw.json` or `models.json`, not in auth profiles. External auth routes such as Bedrock `auth: "aws-sdk"` are also not credentials; for a named Bedrock route, put `auth.profiles.<id>.mode: "aws-sdk"` in `openclaw.json` rather than writing `type: "aws-sdk"` into the auth profile store (`openclaw doctor --fix` moves legacy AWS SDK markers from the credential store into config metadata).

Auth profile refs are also supported for static credentials: `api_key` credentials can use `keyRef: { source, provider, id }`; `token` credentials can use `tokenRef: { source, provider, id }`. OAuth-mode profiles do not support SecretRef credentials — if `auth.profiles.<id>.mode` is set to `"oauth"`, SecretRef-backed `keyRef`/`tokenRef` input for that profile is rejected.

## Checking model auth status

The basic status checks are `openclaw models status` and `openclaw doctor`. For automation, `openclaw models status --check` exits `1` when a profile is expired/missing and `2` when it is expiring. Live auth probes run with `openclaw models status --probe`.

Probe behavior notes: probe rows can come from auth profiles, env credentials, or `models.json`. If explicit `auth.order.<provider>` omits a stored profile, probe reports `excluded_by_auth_order` for that profile instead of trying it. If auth exists but OpenClaw cannot resolve a probeable model candidate for that provider, probe reports `status: no_model`. Rate-limit cooldowns can be model-scoped — a profile cooling down for one model can still be usable for a sibling model on the same provider. Optional ops scripts (systemd/Termux) are documented under Auth monitoring scripts on the Help page.

## Anthropic note

The Anthropic `claude-cli` backend is supported again. Anthropic staff told the project this OpenClaw integration path is allowed again, so OpenClaw treats Claude CLI reuse and `claude -p` usage as sanctioned for Anthropic-backed runs unless Anthropic publishes a new policy. Anthropic API keys remain the most predictable choice for long-lived gateway hosts and explicit server-side billing control.

## API key rotation behavior (gateway)

Some providers support retrying a request with alternative keys when an API call hits a provider rate limit. The priority order is:

- `OPENCLAW_LIVE_<PROVIDER>_KEY` (single override)
- `<PROVIDER>_API_KEYS`
- `<PROVIDER>_API_KEY`
- `<PROVIDER>_API_KEY_*`

Google providers also include `GOOGLE_API_KEY` as an additional fallback. The same key list is deduplicated before use. OpenClaw retries with the next key only for rate-limit errors (for example `429`, `rate_limit`, `quota`, `resource exhausted`, `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, or `workers_ai ... quota limit exceeded`). Non-rate-limit errors are not retried with alternate keys. If all keys fail, the final error from the last attempt is returned.

## Removing provider auth while the gateway is running

When provider auth is removed through the Gateway control plane, OpenClaw deletes the saved auth profiles for that provider and aborts active chat or agent runs whose selected model provider matches the removed provider. The aborted runs emit the normal chat cancellation and lifecycle events with `stopReason: "auth-revoked"`, so connected clients can show that the run was stopped because credentials were removed. Removing saved auth does not revoke keys at the provider — rotate or revoke the key in the provider dashboard when you need provider-side invalidation.

## Controlling which credential is used

### OpenAI and legacy `openai-codex` ids

OpenAI API-key profiles and ChatGPT/Codex OAuth profiles both use the canonical provider id `openai`. New config should use `openai:*` profile ids and `auth.order.openai`. If you see `openai-codex` in older config, auth profile ids, or `auth.order.openai-codex`, treat it as legacy migration input; do not create new `openai-codex` profiles. Run:

```bash
openclaw doctor --fix
openclaw models auth list --provider openai
```

Doctor rewrites legacy `openai-codex:*` profile ids and `auth.order.openai-codex` entries to the canonical `openai` auth route. For OpenAI-specific model/runtime routing, see the OpenAI provider page.

### During login (CLI)

Use `openclaw models auth login --provider <id> --profile-id <profileId>` for providers that support named auth profiles during login:

```bash
openclaw models auth login --provider openai --profile-id openai:ritsuko
openclaw models auth login --provider openai --profile-id openai:lain
```

This is the easiest way to keep multiple OAuth logins for the same provider separate inside one agent. Use `--force` (e.g. `openclaw models auth login --provider anthropic --force`) when a saved provider profile is stuck, expired, or tied to the wrong account and the normal login command keeps reusing it. `--force` deletes the saved auth profiles for that provider in the selected agent directory, then runs the same provider auth flow again; it does not revoke credentials at the provider (rotate or revoke them in the provider dashboard when you need provider-side invalidation).

### Per-session (chat command)

Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session (example profile ids: `anthropic:default`, `anthropic:work`). Use `/model` (or `/model list`) for a compact picker; use `/model status` for the full view (candidates + next auth profile, plus provider endpoint details when configured).

### Per-agent (CLI override)

Set an explicit auth profile order override for an agent (stored in that agent's SQLite auth state):

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use `--agent <id>` to target a specific agent; omit it to use the configured default agent. When you debug order issues, `openclaw models status --probe` shows omitted stored profiles as `excluded_by_auth_order` instead of silently skipping them. When you debug cooldown issues, remember that rate-limit cooldowns can be tied to one model id rather than the whole provider profile. If you change auth order or profile pinning for a chat that is already running, send `/new` or `/reset` in that chat to start a fresh session — existing sessions can keep their current model/profile selection until reset.

## Troubleshooting

### "No credentials found"

If the Anthropic profile is missing, configure an Anthropic API key on the **gateway host** or set up the Anthropic setup-token path, then re-check with `openclaw models status`.

### Token expiring/expired

Run `openclaw models status` to confirm which profile is expiring. If an Anthropic token profile is missing or expired, refresh that setup via setup-token or migrate to an Anthropic API key.

**Source**: OpenClaw documentation — `gateway/authentication` (mirror `inbox/openclaw_docs/gateway/authentication.md`)
**Last Updated**: 2026-06-22
**Status**: Active
