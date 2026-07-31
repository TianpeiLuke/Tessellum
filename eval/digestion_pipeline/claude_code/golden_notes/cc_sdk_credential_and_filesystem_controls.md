---
tags:
  - resource
  - documentation
  - claude_code
  - secure_deployment
  - credentials
keywords:
  - credential proxy pattern
  - anthropic_base_url
  - http_proxy https_proxy
  - tls-terminating proxy
  - read-only code mount
  - sensitive file exclusion
  - tmpfs writable locations
  - mcp custom tool credentials
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/secure-deployment
access_control_group: ["general"]
---

# Agent SDK — Credential and Filesystem Controls

## Overview

When you deploy a Claude Code / Agent SDK agent in production, two recurring concerns are how to give the agent credentials without exposing them and how to mount code so the agent can read it without leaking secrets or persisting unwanted changes. This note is the how-to for both: the **credential proxy pattern** (run a proxy outside the agent's boundary that injects credentials into outgoing requests), the two ways to point Claude Code at that proxy (`ANTHROPIC_BASE_URL` vs `HTTP_PROXY`/`HTTPS_PROXY`), the two ways to authenticate non-Claude services (a custom tool/MCP server vs a TLS-terminating proxy), and the filesystem controls for read-only code mounts and writable scratch space.

These procedures sit downstream of the [security principles](cc_sdk_secure_deployment_principles.md) (boundaries / least privilege / defense in depth) and complement the [isolation technologies](cc_sdk_isolation_technologies.md) catalog, which provides the container/sandbox boundary the proxy lives outside of.

## Credential management

Agents often need credentials to call APIs, access repositories, or interact with cloud services. The challenge is providing this access without exposing the credentials themselves.

### The proxy pattern

The recommended approach is to run a proxy outside the agent's security boundary that injects credentials into outgoing requests. The agent sends requests without credentials, the proxy adds them, and forwards the request to its destination. This pattern has several benefits:

1. The agent never sees the actual credentials.
2. The proxy can enforce an allowlist of permitted endpoints.
3. The proxy can log all requests for auditing.
4. Credentials are stored in one secure location rather than distributed to each agent.

### Configuring Claude Code to use a proxy

Claude Code supports two methods for routing sampling requests through a proxy.

**Option 1 — `ANTHROPIC_BASE_URL` (simple, but only for sampling API requests).** This tells Claude Code and the Agent SDK to send sampling requests to your proxy instead of the Claude API directly. Your proxy receives plaintext HTTP requests, can inspect and modify them (including injecting credentials), then forwards to the real API.

```bash
export ANTHROPIC_BASE_URL="http://localhost:8080"
```

**Option 2 — `HTTP_PROXY` / `HTTPS_PROXY` (system-wide).** Claude Code and the Agent SDK respect these standard environment variables, routing all HTTP traffic through the proxy. For HTTPS, the proxy creates an encrypted CONNECT tunnel: it cannot see or modify request contents without TLS interception.

```bash
export HTTP_PROXY="http://localhost:8080"
export HTTPS_PROXY="http://localhost:8080"
```

### Implementing a proxy

You can build your own proxy or use an existing one: **Envoy Proxy** (production-grade, with a `credential_injector` filter for adding auth headers), **mitmproxy** (TLS-terminating proxy for inspecting/modifying HTTPS traffic), **Squid** (caching proxy with access control lists), and **LiteLLM** (LLM gateway with credential injection and rate limiting).

### Credentials for other services

Beyond sampling from the Claude API, agents often need authenticated access to other services such as git repositories, databases, and internal APIs. There are two main approaches.

**Custom tools.** Provide access through an MCP server or custom tool that routes requests to a service running outside the agent's security boundary. The agent calls the tool, but the actual authenticated request happens outside — the tool calls to a proxy which injects the credentials. For example, a git MCP server could accept commands from the agent but forward them to a git proxy running on the host, which adds authentication before contacting the remote repository; the agent never sees the credentials. Advantages: **no TLS interception** (the external service makes authenticated requests directly) and **credentials stay outside** (the agent only sees the tool interface).

**Traffic forwarding.** For Claude API calls, `ANTHROPIC_BASE_URL` lets you route requests to a proxy that can inspect and modify them in plaintext. But for other HTTPS services (GitHub, npm registries, internal APIs), the traffic is often encrypted end-to-end; even routed through a proxy via `HTTP_PROXY`, the proxy only sees an opaque TLS tunnel and can't inject credentials. To modify HTTPS traffic to arbitrary services without a custom tool, you need a **TLS-terminating proxy** that decrypts traffic, inspects/modifies it, then re-encrypts before forwarding. This requires:

1. Running the proxy outside the agent's container.
2. Installing the proxy's CA certificate in the agent's trust store (so the agent trusts the proxy's certificates).
3. Configuring `HTTP_PROXY`/`HTTPS_PROXY` to route traffic through the proxy.

Note that not all programs respect `HTTP_PROXY`/`HTTPS_PROXY`. Most tools (curl, pip, npm, git) do, but some may bypass these variables and connect directly. For example, Node.js `fetch()` ignores them by default; in Node 24+ you can set `NODE_USE_ENV_PROXY=1` to enable support. For comprehensive coverage, you can use `proxychains` to intercept network calls, or configure iptables to redirect outbound traffic to a **transparent proxy** (one that intercepts traffic at the network level, so the client doesn't need to be configured to use it). Both approaches still require the TLS-terminating proxy and trusted CA certificate; they just ensure traffic actually reaches the proxy.

## Filesystem configuration

Filesystem controls determine what files the agent can read and write.

### Read-only code mounting

When the agent needs to analyze code but not modify it, mount the directory read-only:

```bash
docker run -v /path/to/code:/workspace:ro agent-image
```

Even read-only access to a code directory can expose credentials. Common files to **exclude or sanitize before mounting** (each carries a secret-exposure risk):

| File | Risk |
| ---- | ---- |
| `.env`, `.env.local` | API keys, database passwords, secrets |
| `~/.git-credentials` | Git passwords/tokens in plaintext |
| `~/.aws/credentials` | AWS access keys |
| `~/.config/gcloud/application_default_credentials.json` | Google Cloud ADC tokens |
| `~/.azure/` | Azure CLI credentials |
| `~/.docker/config.json` | Docker registry auth tokens |
| `~/.kube/config` | Kubernetes cluster credentials |
| `.npmrc`, `.pypirc` | Package registry tokens |
| `*-service-account.json` | GCP service account keys |
| `*.pem`, `*.key` | Private keys |

Consider copying only the source files needed, or using `.dockerignore`-style filtering.

### Writable locations

If the agent needs to write files, the options depend on whether you want changes to persist. For ephemeral workspaces in containers, use `tmpfs` mounts that exist only in memory and are cleared when the container stops:

```bash
docker run \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --tmpfs /workspace:rw,noexec,size=500m \
  agent-image
```

If you want to review changes before persisting them, an **overlay filesystem** lets the agent write without modifying underlying files — changes are stored in a separate layer you can inspect, apply, or discard. For fully persistent output, mount a **dedicated volume** but keep it separate from sensitive directories.

**Source**: https://code.claude.com/docs/en/agent-sdk/secure-deployment
**Last Updated**: 2026-06-13
**Status**: Active
