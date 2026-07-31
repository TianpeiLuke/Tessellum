---
tags:
  - resource
  - documentation
  - claude_code
  - llm_gateway
  - litellm
keywords:
  - litellm proxy
  - llm gateway configuration
  - anthropic_auth_token
  - apikeyhelper
  - unified endpoint
  - pass-through endpoint
  - claude_code_skip_bedrock_auth
  - dynamic api key
topics:
  - Claude Code
  - LLM Gateway
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/llm-gateway
access_control_group: ["general"]
---

# Claude Code — Configuring LiteLLM as the Gateway

## Overview

LiteLLM is a third-party proxy server that can act as the centralized [LLM gateway](https://code.claude.com/docs/en/llm-gateway) layer between Claude Code and one or more model providers. This procedure covers how to point Claude Code at a deployed LiteLLM Proxy Server: the prerequisites, the two authentication methods (a static API key versus a dynamic, helper-supplied rotating key), and the two endpoint styles (the recommended unified Anthropic-format endpoint versus provider-specific pass-through endpoints for the Claude API, Amazon Bedrock, Google Vertex AI, and Claude Platform on AWS).

LiteLLM is a third-party service that Anthropic does not endorse, maintain, or audit; this guidance is informational and may become outdated. For the gateway-abstraction concepts (API formats, attribution headers, gateway model discovery) see the sibling note [cc_llm_gateway.md](cc_llm_gateway.md).

## Malware version warning

LiteLLM **PyPI versions 1.82.7 and 1.82.8 were compromised with credential-stealing malware. Do not install these versions.** If you have already installed them:

- Remove the package
- Rotate all credentials on affected systems
- Follow the remediation steps in [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

## Prerequisites

- Claude Code updated to the latest version
- LiteLLM Proxy Server deployed and accessible
- Access to Claude models through your chosen provider

## Authentication methods

### Static API key

The simplest method uses a fixed API key set as `ANTHROPIC_AUTH_TOKEN`, either in the environment or in Claude Code settings:

```bash theme={null}
# Set in environment
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Or in Claude Code settings
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

This value will be sent as the `Authorization` header.

### Dynamic API key with helper

For rotating keys or per-user authentication, supply the key from a helper script rather than a fixed value.

1. Create an API key helper script (for example, fetching the key from a vault or generating a JWT):

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configure Claude Code settings to use the helper:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Set the token refresh interval with `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`:

```bash theme={null}
# Refresh every hour (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

This value will be sent as the `Authorization` and `X-Api-Key` headers. The `apiKeyHelper` has **lower precedence** than `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`.

## Endpoint configuration

### Unified endpoint (recommended)

The recommended setup uses LiteLLM's [Anthropic format endpoint](https://docs.litellm.ai/docs/anthropic_unified) by pointing `ANTHROPIC_BASE_URL` at the LiteLLM server:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

Benefits of the unified endpoint over pass-through endpoints:

- Load balancing
- Fallbacks
- Consistent support for cost tracking and end-user tracking

### Provider-specific pass-through endpoints (alternative)

As an alternative, route through a provider-specific LiteLLM pass-through endpoint. Each provider sets its own base-URL variable, a `CLAUDE_CODE_SKIP_*_AUTH=1` flag (so LiteLLM, not Claude Code, supplies the upstream provider credentials), and the corresponding `CLAUDE_CODE_USE_*` flag:

```bash theme={null}
# Claude API (https://docs.litellm.ai/docs/pass_through/anthropic_completion)
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic

# Amazon Bedrock (https://docs.litellm.ai/docs/pass_through/bedrock)
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1

# Google Vertex AI (https://docs.litellm.ai/docs/pass_through/vertex_ai)
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5

# Claude Platform on AWS (gateway that forwards to the Claude Platform on AWS endpoint)
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

For more detailed information, refer to the [LiteLLM documentation](https://docs.litellm.ai/).

**Source**: https://code.claude.com/docs/en/llm-gateway
**Last Updated**: 2026-06-13
**Status**: Active
