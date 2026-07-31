---
tags:
  - resource
  - documentation
  - claude_code
  - amazon_bedrock
  - features
keywords:
  - bedrock iam policy
  - 1m token context window
  - bedrock service tiers
  - aws guardrails
  - invoke api
  - prompt caching toggle
  - sso authentication loop
  - region issues
topics:
  - Claude Code
  - Amazon Bedrock
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/amazon-bedrock
access_control_group: ["general"]
---

# Claude Code on Amazon Bedrock — Server-Side Features

## Overview

Beyond the enable/authenticate/pin-models procedure, running Claude Code on Amazon Bedrock surfaces a set of **Bedrock-specific, server-side concerns**: the IAM policy that gates every model invocation, an opt-in **1M token context window**, **service tiers** that trade cost against latency, **AWS Guardrails** content filtering, and prompt-caching toggles — plus the platform constraints (Invoke API only, no Converse API, no WebSearch) and the two most common operational failures (the SSO authentication loop and region errors).

These are the capabilities and limits that exist *because* the backend is Bedrock rather than the default Anthropic API. The enable + credential setup lives in [`cc_amazon_bedrock_setup`](cc_amazon_bedrock_setup.md); model pinning and startup checks live in [`cc_amazon_bedrock_model_config`](cc_amazon_bedrock_model_config.md); the alternate native-shape endpoint lives in [`cc_amazon_bedrock_mantle_endpoint`](cc_amazon_bedrock_mantle_endpoint.md).

## IAM configuration

Claude Code on Bedrock requires an IAM policy granting model-invocation, inference-profile, and AWS Marketplace subscription permissions:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

For more restrictive permissions, you can limit the `Resource` to specific inference profile ARNs.

`bedrock:GetInferenceProfile` lets Claude Code resolve an application inference profile ARN to its backing foundation model, which is used to select the correct request shape for that model. If the token is missing this permission, Claude Code recovers automatically by retrying once with the alternate shape, so requests still succeed but each new model adds an extra round-trip; granting the permission avoids the retry. This applies most often to `AWS_BEARER_TOKEN_BEDROCK` deployments, where the token's policy is typically narrower than a full IAM role.

The docs recommend creating a **dedicated AWS account for Claude Code** to simplify cost tracking and access control.

## 1M token context window

Claude Opus 4.6 and later, and Sonnet 4.6, support the 1M token context window on Amazon Bedrock. Claude Code automatically enables the extended context window when you select a 1M model variant.

The setup wizard offers a 1M context option when it pins models. To enable it for a manually pinned model instead, append `[1m]` to the model ID. See [Pin models for third-party deployments](https://code.claude.com/docs/en/model-config) for details.

## Service tiers

Amazon Bedrock service tiers let you trade off cost against latency. Set `ANTHROPIC_BEDROCK_SERVICE_TIER` to `default`, `flex`, or `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code sends this as the `X-Amzn-Bedrock-Service-Tier` header on each request. Tier availability varies by model and region. Reserved capacity uses a provisioned throughput ARN as the model ID instead of this setting.

## AWS Guardrails

Amazon Bedrock Guardrails let you implement content filtering for Claude Code. Create a Guardrail in the Amazon Bedrock console, publish a version, then add the Guardrail headers to your settings file. Enable Cross-Region inference on your Guardrail if you're using cross-region inference profiles.

Example configuration:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Prompt caching

Prompt caching is enabled by default on Bedrock and is controlled by two environment variables set during model configuration:

```bash theme={null}
# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1
```

The 1-hour cache TTL is billed at a higher rate than the 5-minute default. Prompt caching may not be available in all Bedrock regions — if cache token counts stay at zero, check supported models, regions, and limits in the Bedrock documentation. The general caching mechanism and cache lifetime are documented at [prompt caching](https://code.claude.com/docs/en/prompt-caching).

## Platform constraints

Two Anthropic-API features are unavailable when the backend is Bedrock:

- **API shape**: Claude Code uses the Bedrock Invoke API (`InvokeModel` / `InvokeModelWithResponseStream`) and does **not** support the Converse API.
- **WebSearch tool**: The WebSearch tool is not available on Bedrock. See [WebSearch tool behavior](https://code.claude.com/docs/en/tools-reference) for details.

Additionally, when using Bedrock the `/logout` command is unavailable, since authentication is handled through AWS credentials.

## Troubleshooting

### Authentication loop with SSO and corporate proxies

If browser tabs spawn repeatedly when using AWS SSO, remove the `awsAuthRefresh` setting from your settings file. This can occur when corporate VPNs or TLS inspection proxies interrupt the SSO browser flow: Claude Code treats the interrupted connection as an authentication failure, re-runs `awsAuthRefresh`, and loops indefinitely.

If your network environment interferes with automatic browser-based SSO flows, use `aws sso login` manually before starting Claude Code instead of relying on `awsAuthRefresh`.

### Region issues

If you encounter region issues:

- Check model availability: `aws bedrock list-inference-profiles --region your-region`
- Switch to a supported region: `export AWS_REGION=us-east-1`
- Consider using inference profiles for cross-region access

If you receive an error "on-demand throughput isn't supported", specify the model as an inference profile ID.

**Source**: https://code.claude.com/docs/en/amazon-bedrock
**Last Updated**: 2026-06-13
**Status**: Active
