---
tags:
  - resource
  - documentation
  - hermes_agent
  - subscription_proxy
  - provider_integration
keywords:
  - hermes subscription proxy
  - hermes proxy start
  - nous portal oauth proxy
  - credential-attaching pass-through
  - openai-compatible endpoint
  - upstreamadapter
topics:
  - Hermes Agent
  - Provider Integration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy
access_control_group: ["general"]
---

# Hermes Subscription Proxy

## Overview

The subscription proxy is a local HTTP server that lets external apps — OpenViking, Karakeep, Open WebUI, or anything that speaks OpenAI-compatible chat completions — use a Hermes-managed provider subscription as their LLM endpoint. The proxy attaches the right credentials (refreshing them automatically) so the app never needs a static API key. It is distinct from the [API server](hermes_api_server_endpoints.md): the proxy serves **raw model inference** through your subscription rather than serving the Hermes agent. You log in once with `hermes portal`, then `hermes proxy start` forwards a whitelist of OpenAI-compatible paths to your Nous Portal (or xAI) subscription as a credential-attaching pass-through.

## Subscription Proxy vs API Server

The page contrasts the two local servers Hermes can run:

| | API server | Subscription proxy |
|---|---|---|
| What it serves | Your agent (full toolset, memory, skills) | Raw model inference |
| Use case | "Use Hermes as a chat backend" | "Use my Portal sub from another app" |
| Auth | Your `API_SERVER_KEY` | Any bearer (proxy attaches the real one) |
| Tool calls | Yes — the agent runs tools | No — passthrough only |

Use the API server when you want the **agent** as a backend. Use the proxy when you just want **the model** through your subscription.

## Quick Start

### 1. Log into your provider (one-time)

```bash
hermes portal
```

This opens the browser for the Nous Portal OAuth flow. Hermes stores the refresh token in `~/.hermes/auth.json` — the same place all Hermes provider logins live.

### 2. Start the proxy

```bash
hermes proxy start
```

This prints a startup banner ("Starting Hermes proxy for Nous Portal"), reports `Listening on: http://127.0.0.1:8645/v1`, notes that it forwards to a target "resolved per-request from your subscription," and reminds you to "use any bearer token in the client — the proxy attaches your real credential." Leave this running in the foreground. Use `tmux`, `nohup`, or a systemd unit if you want it to survive logout.

### 3. Point your app at it

Any OpenAI-compatible app config takes the same triple:

```
Base URL:   http://127.0.0.1:8645/v1
API key:    anything (e.g. "sk-unused")
Model:      Hermes-4-70B    # or Hermes-4.3-36B, Hermes-4-405B
```

The proxy ignores the `Authorization` header from the app and attaches the real Portal credential to the upstream request. Refreshes happen automatically when the bearer approaches expiry.

## Available Providers

`hermes proxy providers` lists the shipped upstream adapters. Currently shipped: `nous` (Nous Portal) and `xai` (xAI / Grok). More OAuth providers can be added by implementing the `UpstreamAdapter` interface in `hermes_cli/proxy/adapters/`.

## Check Status

`hermes proxy status` reports each upstream adapter and its bearer state:

```
Hermes proxy upstream adapters

  [nous    ] Nous Portal — ready (bearer expires 2026-05-15T06:43:21Z)
```

If you see `not logged in`, run `hermes portal`. If you see `credentials need attention`, your refresh token was revoked (rare — happens if you signed out from the Portal web UI) — just re-run `hermes portal`.

## Allowed Paths

The proxy only forwards paths the upstream actually serves. For Nous Portal:

| Path | Purpose |
|------|---------|
| `/v1/chat/completions` | Chat completions (streaming + non-streaming) |
| `/v1/completions` | Legacy text completions |
| `/v1/embeddings` | Embeddings |
| `/v1/models` | Model list |

Other paths (`/v1/images/generations`, `/v1/audio/speech`, etc.) return 404 with a clear error pointing at the allowed paths. This keeps stray clients from leaking weird requests to the upstream.

## Configuring OpenViking to Use Portal

OpenViking is a context database that needs an LLM provider for its VLM (vision/language model used to extract memories) and embedding model. With the proxy, point its `vlm.api_base` at the local proxy by editing `~/.openviking/ov.conf`:

```json
{
  "vlm": {
    "provider": "openai",
    "model": "Hermes-4-70B",
    "api_base": "http://127.0.0.1:8645/v1",
    "api_key": "unused-proxy-attaches-real-creds"
  }
}
```

Then start the proxy in a terminal alongside `openviking-server` (Terminal 1: `hermes proxy start`; Terminal 2: `openviking-server`). OpenViking's VLM calls now flow through your Portal subscription. The embedding model side still needs its own provider — Portal does serve `/v1/embeddings` but the model selection depends on what your tier supports; check `portal.nousresearch.com/models`.

## Configuring Karakeep (or Any Bookmark/Summarizer App)

Karakeep takes an OpenAI-compatible API for bookmark summarization. In its `.env`, set `OPENAI_API_BASE_URL=http://127.0.0.1:8645/v1`, `OPENAI_API_KEY=any-non-empty-string`, and `INFERENCE_TEXT_MODEL=Hermes-4-70B`. The same pattern works for Open WebUI, LobeChat, NextChat, or any other OpenAI-compatible client.

## Exposing on LAN

By default the proxy binds `127.0.0.1` (localhost only). To let other machines on the network use it, bind to all interfaces:

```bash
hermes proxy start --host 0.0.0.0 --port 8645
```

Be aware: anyone on the network can now use your Portal subscription. The proxy has no auth of its own — it accepts any bearer. Use a firewall, VPN, or reverse proxy with proper auth if you expose this beyond a trusted network.

## Rate Limits

Your Portal tier's RPM/TPM limits apply across the whole proxy. The proxy doesn't fan out or pool — it's a single bearer with your full subscription quota. Monitor usage at `portal.nousresearch.com`.

## Architecture

The proxy is intentionally minimal. Per request it:

1. Receives `POST /v1/chat/completions` from the app.
2. Looks up the adapter's current credential (refresh if expiring).
3. Forwards the request body verbatim, with `Authorization: Bearer <minted-key>`.
4. Streams the response back unchanged (SSE preserved).

No transformation. No logging of request bodies. No agent loop. The proxy is a credential-attaching pass-through.

## Future: More OAuth Providers

The adapter system is pluggable. Adding a new provider (e.g. HuggingFace, GitHub Copilot's chat endpoint, Anthropic via OAuth) requires implementing `UpstreamAdapter` in `hermes_cli/proxy/adapters/<provider>.py` and registering it in `adapters/__init__.py`. Providers that aren't OpenAI-compatible at the protocol level (Anthropic Messages API, for example) would need a transformation layer, which is out of scope for the current shape.

## Related Notes

**Terms**
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — refreshing bearer; relevance: the proxy attaches a refreshing Portal OAuth bearer to every upstream request.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth flow; relevance: `hermes portal` runs the Nous Portal OAuth login.
- [term_authentication](../../term_dictionary/term_authentication.md) — credential attach; relevance: the proxy ignores the client bearer and attaches the real credential.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding server; relevance: the proxy is a credential-attaching pass-through forwarder.
- [term_proxy_pattern](../../term_dictionary/term_proxy_pattern.md) — proxy design pattern; relevance: minimal no-transformation forward of `POST /v1/chat/completions`.
- [term_rest](../../term_dictionary/term_rest.md) — OpenAI-compatible HTTP; relevance: only an allowed-path whitelist (`/v1/chat/completions`, `/v1/embeddings`, …) is forwarded.
- [term_embedding](../../term_dictionary/term_embedding.md) — embeddings endpoint; relevance: `/v1/embeddings` is an allowed forwarded path (OpenViking embedding model).
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — tier limits; relevance: the Portal tier's RPM/TPM limits apply across the whole single-bearer proxy.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: the proxy serves raw LLM inference through the subscription.
- [term_cross_region_proxy](../../term_dictionary/term_cross_region_proxy.md) — analogous forwarding-proxy topology; relevance: same forward-with-attached-credential shape.
- [term_pkce](../../term_dictionary/term_pkce.md) — OAuth 2.1 Proof Key for Code Exchange; relevance: the Portal OAuth login uses PKCE (+Phase 0).

**Code-Repos**
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes proxy start/status/providers` + `hermes portal`; relevance: implements `hermes_cli/proxy/` server + `UpstreamAdapter` registry + OAuth login.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — upstream credential mint/refresh; relevance: resolves + refreshes the Portal/xAI bearer the proxy attaches.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — HTTP serving + SSE forward; relevance: the verbatim request forward + unchanged SSE streaming path.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — runtime helpers; relevance: shares the client-switch/credential-resolution runtime used per request.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties `auth.json` refresh-token storage into the proxy.

**Snippets**
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback server; relevance: the `hermes portal` loopback OAuth login callback.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout; relevance: Portal OAuth login + credential persistence.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — `auth.json` store; relevance: the `~/.hermes/auth.json` refresh-token store the proxy reads.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider resolve; relevance: resolves the Portal/xAI upstream the proxy forwards to.
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: tracks the refreshing bearer state attached per request.
- [snippet_hermes_agent_core_anthropic_adapter_oauth](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_oauth.md) — adapter OAuth refresh; relevance: mints/refreshes the OAuth bearer the proxy attaches.
- [snippet_hermes_agent_core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — client/credential resolution; relevance: shared credential-resolution runtime used per proxied request.
- [snippet_hermes_agent_gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — HTTP serving/forward; relevance: the verbatim request forward + unchanged SSE streaming path.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — upstream URL resolution; relevance: resolves the allowed-path upstream base URL (`/v1/chat/completions`, `/v1/embeddings`, …).
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound forwarding; relevance: the minimal no-transformation pass-through forward to the upstream subscription.

**Docs**
- [hermes_api_server_setup_auth](hermes_api_server_setup_auth.md) — contrasting server; relevance: the page explicitly contrasts proxy vs API-server auth/use-case (+fin).
- [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — agent-backend surface; relevance: agent-as-backend vs raw-model passthrough (+fin).
- [hermes_fallback_providers](hermes_fallback_providers.md) — provider resilience; relevance: `nous`/`xai` are also fallback providers (+fin).
- [hermes_credential_pools](hermes_credential_pools.md) — OAuth storage; relevance: shares the `~/.hermes/auth.json` OAuth/refresh-token store (+fin).
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — config/auth files; relevance: where Portal logins live (+fin).
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: direct analogue of a credential-attaching upstream proxy.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — LLM gateway; relevance: analogous "front a subscription/endpoint for many clients."
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM proxy; relevance: analogous OpenAI-compatible passthrough proxy.
- [cc_authentication](../claude_code/cc_authentication.md) — auth; relevance: analogous OAuth-login + credential attach.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network access; relevance: analogous LAN-exposure / no-auth-of-its-own caveat.

**Source**: `inbox/hermes_agent_docs/user-guide/features/subscription-proxy.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy
**Last Updated**: 2026-06-19
**Status**: Active
