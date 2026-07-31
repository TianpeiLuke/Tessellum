---
tags:
  - resource
  - documentation
  - claude_code
  - network
  - proxy
keywords:
  - corporate proxy
  - llm gateway
  - https_proxy http_proxy no_proxy
  - proxy basic authentication
  - anthropic_base_url
  - per-provider gateway env vars
  - claude code skip auth
  - status verification
topics:
  - Claude Code
  - Network Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/network-config
access_control_group: ["general"]
---

# Claude Code — Proxy and Gateway Configuration

## Overview

Claude Code supports two distinct outbound-network configurations that an organization can apply independently or **together**: a **corporate proxy** (routes all HTTP/HTTPS traffic through a proxy server for security monitoring, compliance, or network-policy enforcement) and an **LLM gateway** (a service that sits between Claude Code and the cloud provider to handle authentication and routing — used for centralized usage tracking, custom rate limiting or budgets, or centralized auth management). Most organizations can use a cloud provider directly without either; these are only needed when the organization has specific network or management requirements.

This note covers the proxy and gateway *environment variables*: the standard proxy variables and basic-auth pattern, plus the per-provider proxy/gateway recipes for Amazon Bedrock, Microsoft Foundry, and Google Vertex AI, and how to verify the result. Full LLM-gateway setup lives at [LLM gateway configuration](https://code.claude.com/docs/en/llm-gateway). All environment variables shown here can also be configured in [`settings.json`](https://code.claude.com/docs/en/settings).

## Corporate proxy: environment variables

Claude Code respects the standard proxy environment variables. `HTTPS_PROXY` is recommended; use `HTTP_PROXY` only if HTTPS is not available. `NO_PROXY` lists destinations to bypass the proxy and accepts either space- or comma-separated format (or `*` to bypass all):

```bash
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Bypass proxy for specific requests - space-separated format
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Bypass proxy for specific requests - comma-separated format
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Bypass proxy for all requests
export NO_PROXY="*"
```

Claude Code does **not** support SOCKS proxies.

## Proxy basic authentication

If the proxy requires basic authentication, include the credentials in the proxy URL:

```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

Avoid hardcoding passwords in scripts — use environment variables or secure credential storage instead. For proxies requiring advanced authentication (NTLM, Kerberos, etc.), consider using an LLM Gateway service that supports the required authentication method instead of embedding credentials in the proxy URL.

## Corporate proxy vs LLM gateway

These are different configurations that can be used together:

- **Corporate proxy** — Routes traffic through an HTTP/HTTPS proxy. Use it when the organization requires all outbound traffic to pass through a proxy server for security monitoring, compliance, or network policy enforcement. Configure with the `HTTPS_PROXY` or `HTTP_PROXY` environment variables.
- **LLM Gateway** — A service that sits between Claude Code and the cloud provider to handle authentication and routing. Use it when you need centralized usage tracking across teams, custom rate limiting or budgets, or centralized authentication management. Configure with the `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, `ANTHROPIC_AWS_BASE_URL`, or `ANTHROPIC_VERTEX_BASE_URL` environment variables.

The per-provider examples below show variables to set in the shell or shell profile (`.bashrc`, `.zshrc`).

## Per-provider proxy and gateway recipes

For each cloud provider, two interchangeable patterns are documented. The **corporate-proxy** pattern enables the provider and sets `HTTPS_PROXY` (model traffic still goes to the provider, just via the proxy). The **LLM-gateway** pattern enables the provider, points its `*_BASE_URL` at the gateway, and sets the matching `CLAUDE_CODE_SKIP_*_AUTH=1` flag when the gateway handles the provider's cloud authentication.

**Amazon Bedrock** — corporate proxy enables Bedrock plus `AWS_REGION` and `HTTPS_PROXY`; the gateway variant uses `ANTHROPIC_BEDROCK_BASE_URL` with `CLAUDE_CODE_SKIP_BEDROCK_AUTH=1` (if the gateway handles AWS auth):

```bash
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configure LLM gateway
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
```

**Microsoft Foundry** — corporate proxy enables Foundry (`CLAUDE_CODE_USE_FOUNDRY=1`, `ANTHROPIC_FOUNDRY_RESOURCE`, optional `ANTHROPIC_FOUNDRY_API_KEY` — omit for Entra ID auth) plus `HTTPS_PROXY`; the gateway variant uses `ANTHROPIC_FOUNDRY_BASE_URL` with `CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1` (if the gateway handles Azure auth).

**Google Vertex AI** — corporate proxy enables Vertex (`CLAUDE_CODE_USE_VERTEX=1`, `CLOUD_ML_REGION`, `ANTHROPIC_VERTEX_PROJECT_ID`) plus `HTTPS_PROXY`; the gateway variant uses `ANTHROPIC_VERTEX_BASE_URL` with `CLAUDE_CODE_SKIP_VERTEX_AUTH=1` (if the gateway handles GCP auth):

```bash
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configure LLM gateway
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
```

## Verify the configuration

Use `/status` in Claude Code to verify the proxy and gateway configuration is applied correctly.

**Source**: https://code.claude.com/docs/en/network-config
**Last Updated**: 2026-06-13
**Status**: Active
