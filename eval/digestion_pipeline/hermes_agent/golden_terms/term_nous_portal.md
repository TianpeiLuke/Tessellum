---
tags:
  - resource
  - terminology
  - agentic_ai
  - inference_providers
  - authentication
keywords:
  - Nous Portal
  - Nous subscription gateway
  - Tool Gateway
  - Nous Research subscription
  - hermes setup --portal
  - inference provider
topics:
  - Inference Providers
  - Subscription Gateways
  - Agent Tooling
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Nous Portal

## Definition

**Nous Portal** is Nous Research's unified subscription gateway — a single OAuth-authenticated service
that proxies access to a curated catalog of 300+ frontier agentic models plus a bundle of agent tooling backends, billed against one subscription instead of a separate account, API key, and billing relationship per model lab and tool provider. It is the **recommended way to run [Hermes Agent](term_hermes_agent.md)**: one `hermes setup --portal` command runs the Portal OAuth flow, selects a model, sets `nous` as the inference provider in `config.yaml`, and turns on the Tool Gateway.

Conceptually, Nous Portal is a *consumer-facing aggregation/billing layer* in front of an upstream multi-provider router. Model traffic routes through OpenRouter under the hood (so model availability and failover behavior match an OpenRouter key), but is billed against the Nous subscription rather than per-provider credit balances. It solves the credential-sprawl problem of agentic workflows, where a useful agent otherwise needs a model key, a web-search key, an image-generation key, a TTS key, and a browser key — five separate signups, dashboards, and top-up flows.

## Context

Nous Portal is a concept from the Hermes Agent inference-provider ecosystem (digested under `resources/documentation/hermes_agent/`). It is referenced corpus-wide as the default provider option in the Hermes Agent docs and is the subject of the `hermes_nous_portal_subscription` documentation note. It sits in the agent's provider layer alongside cloud providers (Anthropic, Gemini, AWS Bedrock), self-hosted servers (vLLM, Ollama), and multi-provider proxies (LiteLLM, OpenRouter). Day-to-day it is inspected and managed via `hermes portal info` / `hermes portal tools` and configured under `model.provider: nous` with `base_url: https://inference-api.nousresearch.com/v1`.

Within the broader knowledge graph it is an instance of the *subscription-gateway* pattern — analogous to, but distinct from, an [API Gateway](term_api_gateway.md) (AWS request-routing front door), an [MCP Gateway](term_mcp_gateway.md) (tool-server fronting), or a generic auth portal: those are infrastructure/routing concepts, whereas Nous Portal is a commercial subscription + tooling-aggregation gateway specific to the Nous/Hermes stack.

## Key Characteristics

- **One OAuth login, no dotfile credentials.** `hermes setup --portal` runs the browser OAuth flow and stores only a refresh token at `~/.hermes/auth.json` (kept separate from `config.yaml` by design). No long-lived per-provider API keys accumulate in a `.env` file.
- **Short-lived JWT minting.** Hermes mints a short-lived JWT from the stored refresh token on *each* inference call rather than replaying a long-lived key. The lifecycle (refresh, mint, retry on transient 401) is fully automatic and invisible to the user.
- **Token quarantine.** If the Portal invalidates a refresh token (password change, manual revoke, session expiry), the invalid token is *quarantined locally* so Hermes stops replaying it and the user gets one clear "re-authentication required" message instead of a stream of identical 401s; re-login clears it.
- **300+ model catalog, one bill.** Proxies a curated agentic-model catalog across labs (Claude, GPT, Gemini, DeepSeek, Qwen, Kimi, GLM, MiniMax, Grok, NVIDIA, and more) — switchable mid-session with `/model`, with no new credentials or top-ups.
- **OpenRouter under the hood.** Routing happens through OpenRouter, so model availability and failover match an OpenRouter key; any OpenRouter-supported model is generally reachable via its slug.
- **Tool Gateway (five backends, one login).** The same subscription unlocks managed backends — web search/extract (Firecrawl), image generation (FAL), text-to-speech (OpenAI TTS), cloud browser automation (Browser Use), and optional cloud terminal sandbox (Modal) — that route the agent's tool calls through Nous-managed infrastructure.
- **Opt-in per tool, not all-or-nothing.** Via `hermes tools`, a user can mix Portal-managed backends with their own keys per tool (e.g. keep an existing Browserbase account while routing web search through Nous).
- **Registers as the `nous` provider plugin.** The Portal is wired in as the `nous` [provider plugin](term_provider_plugin.md); it becomes one of several configurable providers, not the only one — existing providers stay configured and are switchable with `/model` or `hermes model`.
- **Cross-platform parity.** Smooths the highest-friction setup step (per-tool API keys) for native Windows users so they get the same one-OAuth experience as macOS/Linux.

## Related Terms


## References

- [Nous Portal](https://portal.nousresearch.com) — the subscription gateway's web home and management page.
- [Nous Portal integration (Hermes Agent docs)](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal) — subscription contents, model catalog, Tool Gateway backends, OAuth token handling, OpenRouter routing.
- [Hermes Agent (NousResearch/hermes-agent)](https://github.com/NousResearch/hermes-agent) — the open-source self-improving agent that consumes Nous Portal as its recommended provider.
- [OpenRouter docs](https://openrouter.ai/docs/quickstart) — the upstream unified OpenAI-compatible multi-provider API/router the Portal proxies model traffic through.
- [Nous Chat](https://chat.nousresearch.com) — the web chat interface covered by the same Portal subscription.
