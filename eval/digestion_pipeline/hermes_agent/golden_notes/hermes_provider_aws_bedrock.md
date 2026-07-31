---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - aws_bedrock
keywords:
  - aws bedrock provider
  - converse api
  - boto3 credential chain
  - cross-region inference profile
  - bedrock guardrails
  - iam authentication
topics:
  - Hermes Agent
  - Inference Providers
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock
access_control_group: ["general"]
---

# Hermes Agent — AWS Bedrock Provider Setup

## Overview

This guide is the step-by-step procedure for wiring Hermes Agent to **Amazon Bedrock as a native provider**. Bedrock is not configured as an OpenAI-compatible endpoint — Hermes talks to it over the **Converse API**, which unlocks the full Bedrock ecosystem: IAM authentication (via the boto3 credential chain), Bedrock Guardrails applied to every invocation, cross-region inference profiles, and the complete Bedrock foundation-model catalog (Claude, Amazon Nova, DeepSeek, Llama). The setup is deliberately low-config on AWS compute — attach an IAM role and Hermes detects it automatically, with no API keys or `.env` editing.

The shortest path is `pip install hermes-agent[bedrock]` (pulls in boto3), then `hermes model` → "More providers..." → "AWS Bedrock" → pick a region and model, then `hermes chat`. The two recurring gotchas the page warns about are (1) you must use an **inference-profile ID** (e.g. `us.anthropic.claude-sonnet-4-6`), not a bare foundation-model ID, because on-demand throughput is only supported through profiles, and (2) `ThrottlingException` means a per-model rate limit — Hermes retries with backoff, and a quota increase is requested through AWS Service Quotas.

## Prerequisites

- **AWS credentials** — any source supported by the boto3 credential chain:
  - IAM instance role (EC2, ECS, Lambda — zero config)
  - `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` environment variables
  - `AWS_PROFILE` for SSO or named profiles
  - `aws configure` for local development
- **boto3** — install with `pip install hermes-agent[bedrock]`.
- **IAM permissions** — at minimum: `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` (for inference), plus `bedrock:ListFoundationModels` and `bedrock:ListInferenceProfiles` (for model discovery).

On AWS compute (EC2 / ECS / Lambda) the simplest setup is to attach an IAM role with `AmazonBedrockFullAccess` — Hermes detects the instance role automatically, so no API keys or `.env` configuration are needed.

## Quick Start

```bash
# Install with Bedrock support
pip install hermes-agent[bedrock]

# Select Bedrock as your provider
hermes model
# → Choose "More providers..." → "AWS Bedrock"
# → Select your region and model

# Start chatting
hermes chat
```

## Configuration

After running `hermes model`, your `~/.hermes/config.yaml` will contain a `model` block (provider `bedrock`, a `base_url` pointing at the regional `bedrock-runtime` endpoint, and an inference-profile `default`) plus a `bedrock` block:

```yaml
model:
  default: us.anthropic.claude-sonnet-4-6
  provider: bedrock
  base_url: https://bedrock-runtime.us-east-2.amazonaws.com

bedrock:
  region: us-east-2
```

### Region

The AWS region resolves in priority order (highest first): `bedrock.region` in `config.yaml` → `AWS_REGION` env var → `AWS_DEFAULT_REGION` env var → default `us-east-1`.

### Guardrails

To apply Amazon Bedrock Guardrails to **all** model invocations, add a `guardrail` block under `bedrock` — identifier and version come from the Bedrock console; `stream_processing_mode` is `sync`/`async`, and `trace` is `enabled`/`disabled`/`enabled_full`:

```yaml
bedrock:
  region: us-east-2
  guardrail:
    guardrail_identifier: "abc123def456"  # From the Bedrock console
    guardrail_version: "1"                # Version number or "DRAFT"
    stream_processing_mode: "async"       # "sync" or "async"
    trace: "disabled"                     # "enabled", "disabled", or "enabled_full"
```

### Model Discovery

Hermes auto-discovers available models via the Bedrock control plane (`ListFoundationModels` / `ListInferenceProfiles`). Discovery can be tuned with a `discovery` block — toggle it, restrict to a `provider_filter`, and cache the result via `refresh_interval`:

```yaml
bedrock:
  discovery:
    enabled: true
    provider_filter: ["anthropic", "amazon"]  # Only show these providers
    refresh_interval: 3600                     # Cache for 1 hour
```

## Available Models

Bedrock models use **inference-profile IDs** for on-demand invocation; the `hermes model` picker shows these automatically with recommended models at the top. Representative entries: `us.anthropic.claude-sonnet-4-6` (recommended — best balance of speed and capability), `us.anthropic.claude-opus-4-6-v1` (most capable), `us.anthropic.claude-haiku-4-5-20251001-v1:0` (fastest Claude), `us.amazon.nova-pro-v1:0` (Amazon's flagship), `us.amazon.nova-micro-v1:0` (fastest, cheapest), `deepseek.v3.2` (strong open model), and `us.meta.llama4-scout-17b-instruct-v1:0` (Meta's latest).

Models prefixed with `us.` use cross-region inference profiles, which provide better capacity and automatic failover across AWS regions; models prefixed with `global.` route across all available regions worldwide.

## Switching Models Mid-Session

Use the `/model` command during a conversation to switch the active inference profile:

```
/model us.amazon.nova-pro-v1:0
/model deepseek.v3.2
/model us.anthropic.claude-opus-4-6-v1
```

## Diagnostics

Run `hermes doctor` to verify the Bedrock setup. The doctor checks whether AWS credentials are available (env vars, IAM role, SSO), whether `boto3` is installed, whether the Bedrock API is reachable (`ListFoundationModels`), and the number of available models in your region.

## Gateway (Messaging Platforms)

Bedrock works with all Hermes gateway platforms (Telegram, Discord, Slack, Feishu, etc.). Configure Bedrock as your provider, then start the gateway normally — it reads `config.yaml` and reuses the same Bedrock provider configuration:

```bash
hermes gateway setup
hermes gateway start
```

## Troubleshooting

- **"No API key found" / "No AWS credentials"** — Hermes checks for credentials in this order: `AWS_BEARER_TOKEN_BEDROCK` → `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` → `AWS_PROFILE` → EC2 instance metadata (IMDS) → ECS container credentials → Lambda execution role. If none are found, run `aws configure` or attach an IAM role to your compute instance.
- **"Invocation of model ID ... with on-demand throughput isn't supported"** — use an inference-profile ID (prefixed with `us.` or `global.`) instead of the bare foundation-model ID: `anthropic.claude-sonnet-4-6` is wrong; `us.anthropic.claude-sonnet-4-6` is correct.
- **"ThrottlingException"** — you've hit the Bedrock per-model rate limit. Hermes automatically retries with backoff; to raise limits, request a quota increase in the AWS Service Quotas console.

## One-Click AWS Deployment

For a fully automated deployment on EC2 with CloudFormation, the **sample-hermes-agent-on-aws-with-bedrock** sample creates a VPC, IAM role, EC2 instance, and configures Bedrock automatically — deployable in any region with one click.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock
**Last Updated**: 2026-06-19
**Status**: Active
