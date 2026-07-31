---
tags:
  - resource
  - documentation
  - hermes_agent
  - credential_pools
  - provider_resilience
keywords:
  - credential pool
  - api key rotation
  - oauth token rotation
  - rate limit recovery
  - same-provider failover
  - hermes auth
topics:
  - Hermes Agent
  - Provider Integration
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools
access_control_group: ["general"]
---

# Hermes Agent — Credential Pools

## Overview

A credential pool is Hermes' **same-provider, multi-key rotation** mechanism: you register multiple API keys or OAuth tokens for the *same* provider, and when one key hits a rate limit or billing quota Hermes automatically rotates to the next healthy key — keeping the session alive without switching providers. This is the first of Hermes' three resilience layers and is tried before [fallback providers](hermes_fallback_providers.md) (which switch to a *different* provider) and [provider routing](hermes_provider_routing.md). Pools are mainly for API-key providers (OpenRouter, Anthropic); a single Nous Portal OAuth covers 300+ models, so most Portal users don't need a pool. Pool state lives in `~/.hermes/auth.json` and rotation strategies live in `config.yaml`.

## Pools vs. Fallback Providers

Credential pools are **same-provider rotation**; fallback providers are **cross-provider failover**. Pools are tried first — if all pool keys are exhausted, *then* the fallback provider activates. Because pools are mainly useful for API-key providers (OpenRouter, Anthropic), most users on a single Nous Portal OAuth (which covers 300+ models) don't need a pool at all.

## How It Works

The rotation decision flow keys off the HTTP error returned by the provider — a transient 429 retries once, a plan/usage-limit 429 or a 402 rotates immediately, and a 401 attempts an OAuth refresh before rotating:

```
Your request
  → Pick key from pool (round_robin / least_used / fill_first / random)
  → Send to provider
  → 429 rate limit?
      → Plan/usage limit reached (e.g. ChatGPT/Codex "usage limit reached")?
          → Rotate to next pool key immediately (no retry — the cap won't clear on retry)
      → Generic / transient 429?
          → Retry same key once (transient blip)
          → Second 429 → rotate to next pool key
      → All keys exhausted → fallback_model (different provider)
  → 402 billing error?
      → Immediately rotate to next pool key (24h cooldown)
  → 401 auth expired?
      → Try refreshing the token (OAuth)
      → Refresh failed → rotate to next pool key
  → Success → continue normally
```

## Quick Start

If you already have an API key set in `.env`, Hermes auto-discovers it as a 1-key pool. To benefit from pooling, add more keys. OAuth credentials open a browser for login:

```bash
# Add a second OpenRouter key
hermes auth add openrouter --api-key sk-or-v1-your-second-key

# Add a second Anthropic key
hermes auth add anthropic --type api-key --api-key sk-ant-api03-your-second-key

# Add an Anthropic OAuth credential (requires Claude Max plan + extra usage credits)
hermes auth add anthropic --type oauth
# Opens browser for OAuth login
```

`hermes auth list` shows the pools; the `←` marks the currently selected credential (e.g. `openrouter (2 credentials)` and `anthropic (3 credentials)` with each entry's label, `auth_type`, and source).

## Interactive Management

Running `hermes auth` with no subcommand opens an interactive wizard that shows full pool status and offers a menu:

```
What would you like to do?
  1. Add a credential
  2. Remove a credential
  3. Reset cooldowns for a provider
  4. Set rotation strategy for a provider
  5. Exit
```

For providers that support both API keys and OAuth (Anthropic, Nous, Codex), the add flow asks which type to use (paste a dashboard key vs. authenticate via browser).

## CLI Commands

| Command | Description |
|---------|-------------|
| `hermes auth` | Interactive pool management wizard |
| `hermes auth list` | Show all pools and credentials |
| `hermes auth list <provider>` | Show a specific provider's pool |
| `hermes auth add <provider>` | Add a credential (prompts for type and key) |
| `hermes auth add <provider> --type api-key --api-key <key>` | Add an API key non-interactively |
| `hermes auth add <provider> --type oauth` | Add an OAuth credential via browser login |
| `hermes auth remove <provider> <index>` | Remove credential by 1-based index |
| `hermes auth reset <provider>` | Clear all cooldowns/exhaustion status |

## Rotation Strategies

Configure via `hermes auth` → "Set rotation strategy" or in `config.yaml`:

```yaml
credential_pool_strategies:
  openrouter: round_robin
  anthropic: least_used
```

| Strategy | Behavior |
|----------|----------|
| `fill_first` (default) | Use the first healthy key until it's exhausted, then move to the next |
| `round_robin` | Cycle through keys evenly, rotating after each selection |
| `least_used` | Always pick the key with the lowest request count |
| `random` | Random selection among healthy keys |

## Error Recovery

The pool handles different errors differently, each with its own cooldown:

| Error | Behavior | Cooldown |
|-------|----------|----------|
| **429 Rate Limit** | Retry same key once (transient). Second consecutive 429 rotates to next key | 1 hour |
| **402 Billing/Quota** | Immediately rotate to next key | 24 hours |
| **401 Auth Expired** | Try refreshing the OAuth token first. Rotate only if refresh fails | — |
| **All keys exhausted** | Fall through to `fallback_model` if configured | — |

The `has_retried_429` flag resets on every successful API call, so a single transient 429 doesn't trigger rotation.

## Custom Endpoint Pools

Custom OpenAI-compatible endpoints (Together.ai, RunPod, local servers) get their own pools, keyed by the endpoint name from `custom_providers` in `config.yaml`. When you set up a custom endpoint via `hermes model`, it auto-generates a name like "Together.ai" or "Local (localhost:8080)" that becomes the pool key. These pools are stored in `auth.json` under `credential_pool` with a `custom:` prefix:

```json
{
  "credential_pool": {
    "openrouter": [...],
    "custom:together.ai": [...]
  }
}
```

## Auto-Discovery

Hermes automatically discovers credentials from multiple sources and seeds the pool on startup:

| Source | Example | Auto-seeded? |
|--------|---------|-------------|
| Environment variables | `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY` | Yes |
| OAuth tokens (auth.json) | Codex device code, Nous device code | Yes |
| Claude Code credentials | `~/.claude/.credentials.json` | Yes (Anthropic) |
| Hermes PKCE OAuth | `~/.hermes/auth.json` | Yes (Anthropic) |
| Custom endpoint config | `model.api_key` in config.yaml | Yes (custom endpoints) |
| Manual entries | Added via `hermes auth add` | Persisted in auth.json |

Auto-seeded entries are updated on each pool load — if you remove an env var, its pool entry is automatically pruned. Manual entries (added via `hermes auth add`) are never auto-pruned.

Borrowed runtime secrets (for example env vars, Bitwarden/Vault/keyring/systemd references, and custom config values) are **reference-only** at the `auth.json` boundary. Hermes can use the resolved value in memory for the current run, but it persists only metadata such as the source ref, label, status, request counters, and a non-reversible fingerprint. Manual entries and Hermes-owned OAuth/device-code state keep the durable tokens they need to refresh.

## Delegation & Subagent Sharing

When the agent spawns subagents via `delegate_task`, the parent's credential pool is automatically shared with children:

- **Same provider** — the child receives the parent's full pool, enabling key rotation on rate limits
- **Different provider** — the child loads that provider's own pool (if configured)
- **No pool configured** — the child falls back to the inherited single API key

Subagents benefit from the same rate-limit resilience as the parent with no extra configuration. Per-task credential leasing ensures children don't conflict with each other when rotating keys concurrently.

## Thread Safety

The credential pool uses a threading lock for all state mutations (`select()`, `mark_exhausted_and_rotate()`, `try_refresh_current()`, `mark_used()`). This ensures safe concurrent access when the gateway handles multiple chat sessions simultaneously.

## Architecture

The credential pool integrates at the provider resolution layer across four modules:

1. **`agent/credential_pool.py`** — Pool manager: storage, selection, rotation, cooldowns
2. **`hermes_cli/auth_commands.py`** — CLI commands and interactive wizard
3. **`hermes_cli/runtime_provider.py`** — Pool-aware credential resolution
4. **`run_agent.py`** — Error recovery: 429/402/401 → pool rotation → fallback

## Storage

Pool state is stored in `~/.hermes/auth.json` under the `credential_pool` key. Each entry carries an `id`, `label`, `auth_type`, `priority`, `source`, status, and request counters; borrowed secrets store only a `secret_source` + non-reversible `secret_fingerprint`, while manually added entries persist their `access_token`:

```json
{
  "version": 1,
  "credential_pool": {
    "openrouter": [
      {
        "id": "abc123",
        "label": "OPENROUTER_API_KEY",
        "auth_type": "api_key",
        "priority": 0,
        "source": "env:OPENROUTER_API_KEY",
        "secret_source": "bitwarden",
        "secret_fingerprint": "sha256:12ab34cd56ef7890",
        "last_status": "ok",
        "request_count": 142
      }
    ],
    "anthropic": [
      {
        "id": "manual1",
        "label": "personal-api-key",
        "auth_type": "api_key",
        "priority": 0,
        "source": "manual",
        "access_token": "sk-ant-api03-..."
      }
    ]
  }
}
```

The OpenRouter entry above was borrowed from an external source, so the raw key is not stored in `auth.json`; the manual Anthropic entry was intentionally added to Hermes' credential store, so its token remains persistable. Rotation strategies are stored separately in `config.yaml` (not `auth.json`).

## Related Notes

**Terms**
- [term_round_robin](../../term_dictionary/term_round_robin.md) — cyclic selection; relevance: one of the 4 rotation strategies (`fill_first`/`round_robin`/`least_used`/`random`).
- [term_failover](../../term_dictionary/term_failover.md) — switch on exhaustion; relevance: when all pool keys exhaust, fall through to `fallback_model`.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — provider switchover; relevance: pools are the same-provider layer tried before cross-provider model failover.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — 429/402 handling; relevance: rotation decision flow keys off 429 retry-once / 402 immediate / 401 refresh.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: pools rotate API keys AND OAuth tokens; 401 triggers token refresh.
- [term_authentication](../../term_dictionary/term_authentication.md) — credential auth; relevance: auto-discovery seeds pools from env/OAuth/Claude-Code/PKCE sources.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: parent's pool is shared with `delegate_task` subagents (per-task leasing).
- [term_thread_binding_policy](../../term_dictionary/term_thread_binding_policy.md) — concurrency control; relevance: a threading lock guards all pool mutations for concurrent sessions.
- [term_provisioned_concurrency](../../term_dictionary/term_provisioned_concurrency.md) — concurrency provisioning; relevance: analogous concurrent-access guarantees for the gateway's parallel sessions.
- [term_aws_sdk_credential_chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — ordered credential lookup; relevance: analogous ordered credential lookup across multiple sources.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — multi-key/OAuth-token rotation per provider; relevance: the SP09-owned concept term this note documents (+Phase 0).
- [term_fallback_provider](../../term_dictionary/term_fallback_provider.md) — cross-provider failover chain; relevance: the next resilience layer below pools (+Phase 0).
- [term_provider_routing](../../term_dictionary/term_provider_routing.md) — OpenRouter sub-provider selection; relevance: third resilience layer (+Phase 0).
- [term_nous_portal](../../term_dictionary/term_nous_portal.md) — Nous Portal subscription; relevance: a single Portal OAuth covers 300+ models so most users don't need a pool (+fin).

**Code-Repos**
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — `agent/credential_pool.py` + `runtime_provider.py`; relevance: the pool manager (storage, selection, rotation, cooldowns) + pool-aware resolution.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes auth` commands; relevance: `auth_commands.py` add/list/remove/reset + interactive wizard + strategy selection.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `run_agent.py` error recovery; relevance: 429/402/401 → pool rotation → fallback handoff.
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — subagent/delegation sharing; relevance: spawned children inherit the parent pool for rate-limit resilience.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties auto-discovery seeding into startup, `auth.json` storage.

**Snippets**
- [snippet_hermes_agent_core_credential_pool_dataclass](../../code_snippets/snippet_hermes_agent_core_credential_pool_dataclass.md) — pool dataclass; relevance: the per-provider pool model (keys/OAuth tokens, strategy, cooldowns).
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — pool entry; relevance: per-key entry state (429/402/401 cooldown + exhausted flags).
- [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — rotation decision flow; relevance: the 4 strategies (`fill_first`/`round_robin`/`least_used`/`random`) + thread-safe selection.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — auto-discovery seeding; relevance: seeds pools from env/OAuth/Claude-Code/PKCE sources + reference-only secrets.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source order; relevance: the discovery sources feeding the pool.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — `hermes auth` add/remove; relevance: the interactive add/list/remove/reset wizard.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — `auth.json` storage; relevance: reference-only secret storage shape this page documents.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — pool→fallback handoff; relevance: when all pool keys exhaust, fall through to `fallback_model`.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider resolution; relevance: resolves which provider's pool a request uses (incl. custom-endpoint pools).
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: 401 refresh-then-rotate token state for OAuth-token pool entries.

**Docs**
- [hermes_fallback_providers](hermes_fallback_providers.md) — cross-provider layer; relevance: pools are tried first, then fallback (+fin).
- [hermes_provider_routing](hermes_provider_routing.md) — sub-provider routing; relevance: third layer of the resilience stack (+fin).
- [hermes_subscription_proxy](hermes_subscription_proxy.md) — Portal OAuth; relevance: Portal OAuth seeds pools; proxy shares `auth.json` (+fin).
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — `credential_pool_strategies:` keys; relevance: strategies stored in config.yaml not auth.json (+fin).
- [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — secret storage; relevance: SP03 owns Bitwarden/Vault/keyring reference-only secret storage (+fin).
- [cc_authentication](../claude_code/cc_authentication.md) — auth/credentials; relevance: analogous credential management.
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential controls; relevance: analogous credential-source resolution + reference-only secrets.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — 429/quota errors; relevance: the error taxonomy that drives rotation.
- [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — multi-credential provider; relevance: analogous multi-key provider configuration.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth refresh issues; relevance: analogous 401 refresh-then-rotate handling.
- **[OpenClaw — Models FAQ (Selection, Aliases, Failover, Auth Profiles)](../openclaw/oc_help_faq_models.md)** — This is the procedural Models FAQ for OpenClaw: setting defaults, selecting/switching models, defining aliases, adding provider models, understanding failover…

**Source**: `inbox/hermes_agent_docs/user-guide/features/credential-pools.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools
**Last Updated**: 2026-06-19
**Status**: Active
