---
tags:
  - resource
  - documentation
  - claude_code
  - llm_gateway
  - enterprise_deployment
keywords:
  - llm gateway
  - centralized proxy layer
  - gateway requirements
  - api format
  - attribution headers
  - gateway model discovery
  - centralized authentication
  - usage tracking
topics:
  - Claude Code
  - LLM Gateway
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/llm-gateway
access_control_group: ["general"]
---

# Claude Code — LLM Gateway

## Overview

An **LLM gateway** is a centralized proxy layer that sits between Claude Code and the model providers it talks to. Routing all model traffic through a gateway gives an organization a single point to manage API keys, track usage, enforce cost controls, audit interactions, and switch providers without changing client configuration. This note describes what a gateway provides, the requirements a gateway must satisfy to work with Claude Code (the supported API formats and header-forwarding rules), the per-request attribution headers Claude Code emits, and how Claude Code can discover models exposed by a gateway.

This is the conceptual half of the gateway story. The concrete configuration of LiteLLM as the gateway — authentication methods, unified vs. pass-through endpoints — lives in the sibling note [LiteLLM Configuration](cc_llm_gateway_litellm.md). Enterprise Desktop deployments configure gateway providers via [managed settings](https://support.claude.com/en/articles/12622667-enterprise-configuration); the Claude Desktop app can run against a self-hosted gateway through the Cowork on 3P research preview, which uses its own configuration keys.

## What a Gateway Provides

LLM gateways provide a centralized proxy layer between Claude Code and model providers, often providing:

- **Centralized authentication** — Single point for API key management.
- **Usage tracking** — Monitor usage across teams and projects.
- **Cost controls** — Implement budgets and rate limits.
- **Audit logging** — Track all model interactions for compliance.
- **Model routing** — Switch between providers without code changes.

## Gateway Requirements

For an LLM gateway to work with Claude Code, it must meet the following requirements.

### API format

The gateway must expose to clients at least one of the following API formats:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   - Must forward request headers: `anthropic-beta`, `anthropic-version`
2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   - Must preserve request body fields: `anthropic_beta`, `anthropic_version`
3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   - Must forward request headers: `anthropic-beta`, `anthropic-version`

Failure to forward headers or preserve body fields may result in reduced functionality or inability to use Claude Code features.

Claude Code determines which features to enable based on the API format. When using the Anthropic Messages format with Bedrock or Vertex, you may need to set environment variable `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.

### Request headers

Claude Code includes the following headers on API requests:

| Header | Description |
| :--- | :--- |
| `X-Claude-Code-Session-Id` | A unique identifier for the current Claude Code session. Proxies can use this to aggregate all API requests from a single session without parsing the request body. |
| `X-Claude-Code-Agent-Id` | Identifier of the subagent or teammate that issued the request. Your proxy can use this to attribute API cost to individual parallel subagents within a session, without parsing the request body. Present only for requests made by an in-process subagent or teammate. |
| `X-Claude-Code-Parent-Agent-Id` | Identifier of the agent that spawned the agent making the request. Use this with `X-Claude-Code-Agent-Id` to attribute API costs across nested agents in your proxy. Present only when the requesting agent was itself spawned by another agent. |

Both agent ID headers are ephemeral per-spawn identifiers, not persistent user or device IDs.

Claude Code also prepends a short **attribution block** to the system prompt containing the client version and a fingerprint derived from the conversation. The Anthropic API strips this block before processing, so it does not affect first-party prompt caching. If your gateway implements its own prompt cache keyed on the full request body, set `CLAUDE_CODE_ATTRIBUTION_HEADER=0` (see [env-vars](https://code.claude.com/docs/en/env-vars)) to omit it.

## Configuration

### Model selection

By default, Claude Code uses standard model names for the selected API format.

When `ANTHROPIC_BASE_URL` points at a gateway that exposes the Anthropic Messages format, Claude Code can query the gateway's `/v1/models` endpoint at startup and add the returned models to the `/model` picker. Set `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` to enable this. Discovery is off by default so that gateways backed by a shared API key do not surface every model the key can access to every user. Each discovered entry is labeled "From gateway" and uses the `display_name` field from the response when one is provided. This requires Claude Code v2.1.129 or later.

Discovery applies only to the Anthropic Messages format. It does not run for Bedrock or Vertex pass-through endpoints, and it does not run when `ANTHROPIC_BASE_URL` is unset or points at `api.anthropic.com`.

The discovery request authenticates the same way as inference requests: it sends `ANTHROPIC_AUTH_TOKEN` as a bearer token, or `ANTHROPIC_API_KEY` as the `x-api-key` header when no auth token is set, along with any headers from `ANTHROPIC_CUSTOM_HEADERS`. Only models whose ID begins with `claude` or `anthropic` are added to the picker. Results are cached to `~/.claude/cache/gateway-models.json` and refreshed on each startup. If the request fails or the gateway does not implement `/v1/models`, the picker falls back to the cached list from the previous startup or to the built-in model list.

If your gateway uses model names that do not match the discovery filter, use the environment variables documented in [Model configuration](https://code.claude.com/docs/en/model-config) to add them manually.

**Source**: https://code.claude.com/docs/en/llm-gateway
**Last Updated**: 2026-06-13
**Status**: Active
