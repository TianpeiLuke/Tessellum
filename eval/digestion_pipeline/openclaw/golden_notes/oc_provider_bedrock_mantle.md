---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - bedrock_mantle
keywords:
  - openclaw bedrock mantle provider
  - amazon-bedrock-mantle openai-compatible
  - AWS_BEARER_TOKEN_BEDROCK auth
  - mantle bearer token iam credential chain
  - mantle automatic model discovery
  - anthropic-messages route claude opus
  - gpt-oss qwen kimi glm
  - openclaw models list mantle
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/bedrock-mantle
access_control_group: ["general"]
---

# OpenClaw — Configuring the Amazon Bedrock Mantle Provider

## Overview

This note is the setup procedure for OpenClaw's bundled **Amazon Bedrock Mantle** provider (provider ID `amazon-bedrock-mantle`): the OpenAI-compatible `/v1/chat/completions` endpoint, backed by Bedrock infrastructure, that hosts open-source and third-party models (GPT-OSS, Qwen, Kimi, GLM, and similar). It mirrors the `providers/bedrock-mantle` source page: the header property table, the two Getting-started auth routes (explicit `AWS_BEARER_TOKEN_BEDROCK` bearer token vs IAM-minted bearer token), automatic model discovery and supported regions, manual JSON5 configuration, and the advanced-configuration accordions (reasoning inference, endpoint unavailability, the Claude Opus 4.7 Anthropic Messages route, and the relationship to the native Amazon Bedrock provider).

## Provider Properties

The header property table fixes the provider's identity and defaults:

| Property | Value |
| --- | --- |
| Provider ID | `amazon-bedrock-mantle` |
| API | `openai-completions` (OpenAI-compatible) or `anthropic-messages` (Anthropic Messages route) |
| Auth | Explicit `AWS_BEARER_TOKEN_BEDROCK` or IAM credential-chain bearer-token generation |
| Default region | `us-east-1` (override with `AWS_REGION` or `AWS_DEFAULT_REGION`) |

## Getting Started

Choose your preferred auth method and follow the setup steps. The source page presents two tabs: **Explicit bearer token** and **IAM credentials**.

### Explicit bearer token route

**Best for:** environments where you already have a Mantle bearer token. First, set the bearer token on the gateway host (optionally set a region, which defaults to `us-east-1`):

```bash
export AWS_BEARER_TOKEN_BEDROCK="..."
export AWS_REGION="us-west-2"
```

Second, opt in to provider data sharing for Claude Fable 5: Claude Fable 5 and Claude Mythos-class Bedrock models require the Mantle Data Retention API mode `provider_data_share` before invocation. This opt-in allows Bedrock to share prompts and completions with Anthropic and retain them for up to 30 days for trust and safety review. Use another Bedrock model in the config if you cannot accept that retention mode.

```bash
AWS_REGION="${AWS_REGION:-us-east-1}"
curl -X PUT "https://bedrock-mantle.${AWS_REGION}.api.aws/v1/data_retention" \
  -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
  -H "Content-Type: application/json" \
  -d '{ "mode": "provider_data_share" }'
```

Third, verify models are discovered with `openclaw models list`; discovered models appear under the `amazon-bedrock-mantle` provider, and no additional config is required unless you want to override defaults.

### IAM credentials route

**Best for:** using AWS SDK-compatible credentials (shared config, SSO, web identity, instance or task roles). First, configure AWS credentials on the gateway host — any AWS SDK-compatible auth source works:

```bash
export AWS_PROFILE="default"
export AWS_REGION="us-west-2"
```

Second, verify models are discovered with `openclaw models list`; OpenClaw generates a Mantle bearer token from the credential chain automatically. As the page's tip notes, when `AWS_BEARER_TOKEN_BEDROCK` is not set, OpenClaw mints the bearer token for you from the AWS default credential chain, including shared credentials/config profiles, SSO, web identity, and instance or task roles.

## Automatic Model Discovery

When `AWS_BEARER_TOKEN_BEDROCK` is set, OpenClaw uses it directly; otherwise OpenClaw attempts to generate a Mantle bearer token from the AWS default credential chain. It then discovers available Mantle models by querying the region's `/v1/models` endpoint. The discovery behavior is summarized in the source page's table:

| Behavior | Detail |
| --- | --- |
| Discovery cache | Results cached for 1 hour |
| IAM token refresh | Hourly |

To keep the Mantle plugin enabled but suppress automatic discovery and IAM bearer-token generation, disable the plugin-owned discovery toggle:

```bash
openclaw config set plugins.entries.amazon-bedrock-mantle.config.discovery.enabled false
```

The source page notes that the bearer token is the same `AWS_BEARER_TOKEN_BEDROCK` used by the standard Amazon Bedrock (`/providers/bedrock`) provider.

### Supported regions

Mantle discovery and invocation are available in the following regions: `us-east-1`, `us-east-2`, `us-west-2`, `ap-northeast-1`, `ap-south-1`, `ap-southeast-3`, `eu-central-1`, `eu-west-1`, `eu-west-2`, `eu-south-1`, `eu-north-1`, `sa-east-1`.

## Manual Configuration

If you prefer explicit config instead of auto-discovery, define the provider under `models.providers["amazon-bedrock-mantle"]`. The provider uses the `openai-completions` API with `auth: "api-key"` and reads the key from the `AWS_BEARER_TOKEN_BEDROCK` env var, against the region-specific `/v1` base URL:

```json5
{
  models: {
    providers: {
      "amazon-bedrock-mantle": {
        baseUrl: "https://bedrock-mantle.us-east-1.api.aws/v1",
        api: "openai-completions",
        auth: "api-key",
        apiKey: "env:AWS_BEARER_TOKEN_BEDROCK",
        models: [
          {
            id: "gpt-oss-120b",
            name: "GPT-OSS 120B",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 32000,
            maxTokens: 4096,
          },
        ],
      },
    },
  },
}
```

## Advanced Configuration

The source page groups four advanced topics in an accordion group.

### Reasoning support

Reasoning support is inferred from model IDs containing patterns like `thinking`, `reasoner`, or `gpt-oss-120b`. OpenClaw sets `reasoning: true` automatically for matching models during discovery.

### Endpoint unavailability

If the Mantle endpoint is unavailable or returns no models, the provider is silently skipped. OpenClaw does not error; other configured providers continue to work normally.

### Claude Opus 4.7 via the Anthropic Messages route

Mantle also exposes an Anthropic Messages route that carries Claude models through the same bearer-authenticated streaming path. Claude Opus 4.7 (`amazon-bedrock-mantle/claude-opus-4.7`) is callable through this route with provider-owned streaming, so AWS bearer tokens are not treated like Anthropic API keys. When you pin an Anthropic Messages model on the Mantle provider, OpenClaw uses the `anthropic-messages` API surface instead of `openai-completions` for that model; auth still comes from `AWS_BEARER_TOKEN_BEDROCK` (or the minted IAM bearer token):

```json5
{
  models: {
    providers: {
      "amazon-bedrock-mantle": {
        models: [
          {
            id: "claude-opus-4.7",
            name: "Claude Opus 4.7",
            api: "anthropic-messages",
            reasoning: true,
            input: ["text", "image"],
            contextWindow: 1000000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

### Relationship to Amazon Bedrock provider

Bedrock Mantle is a separate provider from the standard Amazon Bedrock (`/providers/bedrock`) provider. Mantle uses an OpenAI-compatible `/v1` surface, while the standard Bedrock provider uses the native Bedrock API. Both providers share the same `AWS_BEARER_TOKEN_BEDROCK` credential when present.

**Source**: OpenClaw documentation — `providers/bedrock-mantle` (mirror `inbox/openclaw_docs/providers/bedrock-mantle.md`)
**Last Updated**: 2026-06-22
**Status**: Active
