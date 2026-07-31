---
tags:
  - resource
  - documentation
  - claude_code
  - amazon_bedrock
  - mantle
keywords:
  - mantle endpoint
  - claude_code_use_mantle
  - native anthropic api shape
  - bedrock invoke api
  - anthropic-prefixed model ids
  - run mantle alongside invoke
  - route mantle through gateway
  - claude_code_skip_mantle_auth
topics:
  - Claude Code
  - Amazon Bedrock
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/amazon-bedrock
access_control_group: ["general"]
---

# Claude Code — Amazon Bedrock Mantle Endpoint

## Overview

Mantle is an Amazon Bedrock endpoint that serves Claude models through the **native Anthropic API shape** rather than the Bedrock Invoke API. It uses the same AWS credentials, IAM permissions, and `awsAuthRefresh` configuration as the standard Bedrock setup, but is enabled and addressed separately. This note is the operational procedure for switching Claude Code to Mantle: enabling it, selecting a Mantle model, running Mantle alongside the Invoke API in one session, routing Mantle through a centralized gateway, the Mantle-specific environment variables, and the 403/400 errors you may hit.

Mantle requires Claude Code v2.1.94 or later (run `claude --version` to check). The base Bedrock enable + credential setup it builds on lives in [`cc_amazon_bedrock_setup`](cc_amazon_bedrock_setup.md); the model-pinning and startup-check mechanics live in [`cc_amazon_bedrock_model_config`](cc_amazon_bedrock_model_config.md).

## Enable Mantle

With AWS credentials already configured, set `CLAUDE_CODE_USE_MANTLE` to route requests to the Mantle endpoint:

```bash
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code constructs the endpoint URL from the AWS region. As of v2.1.172, the region is resolved with the same precedence as the standard Bedrock configuration (`AWS_REGION` → `AWS_DEFAULT_REGION` → active profile region → `us-east-1`); earlier versions use `AWS_REGION` only. To override the URL for a custom endpoint or gateway, set `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Run `/status` inside Claude Code to confirm. The provider line shows `Amazon Bedrock (Mantle)` when Mantle is active.

## Select a Mantle Model

Mantle uses model IDs prefixed with `anthropic.` and **without a version suffix**, for example `anthropic.claude-haiku-4-5`. The models available to your account depend on what your organization has been granted; additional model IDs are listed in your onboarding materials from AWS. Contact your AWS account team to request access to allowlisted models.

Set the model with the `--model` flag or with `/model` inside Claude Code:

```bash
claude --model anthropic.claude-haiku-4-5
```

## Run Mantle Alongside the Invoke API

The models available to you on Mantle may not include every model you use today. Setting both `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_MANTLE` lets Claude Code call both endpoints from the same session. Model IDs that match the Mantle format are routed to Mantle, and all other model IDs go to the Bedrock Invoke API.

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

To surface a Mantle model in the `/model` picker, list its ID in `availableModels` in your settings file. This setting also restricts the picker to the listed entries, so include every alias you want to keep available:

```json
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Entries with the `anthropic.` prefix are added as custom picker options and routed to Mantle. Replace `anthropic.claude-haiku-4-5` with the model ID your account has been granted. See [Restrict model selection](https://code.claude.com/docs/en/model-config) for how `availableModels` interacts with other model settings. When both providers are active, `/status` shows `Amazon Bedrock + Amazon Bedrock (Mantle)`.

## Route Mantle Through a Gateway

If your organization routes model traffic through a centralized [LLM gateway](cc_llm_gateway.md) that injects AWS credentials server-side, disable client-side authentication so Claude Code sends requests without SigV4 signatures or `x-api-key` headers:

```bash
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

## Mantle Environment Variables

These variables are specific to the Mantle endpoint. See the full catalog at [Environment variables](https://code.claude.com/docs/en/env-vars).

| Variable                                | Purpose                                                             |
| :-------------------------------------- | :------------------------------------------------------------------ |
| `CLAUDE_CODE_USE_MANTLE`                | Enable the Mantle endpoint. Set to `1` or `true`.                   |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Override the default Mantle endpoint URL                            |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Skip client-side authentication for proxy setups                    |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Override AWS region for the Haiku-class model (shared with Bedrock) |

## Troubleshooting: Mantle Endpoint Errors

If `/status` does not show `Amazon Bedrock (Mantle)` after you set `CLAUDE_CODE_USE_MANTLE`, the variable is not reaching the process. Confirm it is exported in the shell where you launched `claude`, or set it in the `env` block of your settings file.

A `403` from the Mantle endpoint with valid credentials means your AWS account has not been granted access to the model you requested. Contact your AWS account team to request access.

A `400` that names the model ID means that model is not served on Mantle. Mantle has its own model lineup separate from the standard Bedrock catalog, so inference profile IDs such as `us.anthropic.claude-sonnet-4-6` will not work. Use a Mantle-format ID, or enable both endpoints (set both `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_MANTLE`) so Claude Code routes each request to the endpoint where the model is available.

**Source**: https://code.claude.com/docs/en/amazon-bedrock
**Last Updated**: 2026-06-13
**Status**: Active
