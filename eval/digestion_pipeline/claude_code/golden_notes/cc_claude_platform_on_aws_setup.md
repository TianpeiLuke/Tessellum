---
tags:
  - resource
  - documentation
  - claude_code
  - cloud_providers
  - claude_platform_on_aws
keywords:
  - claude platform on aws
  - aws marketplace billing
  - workspace api key
  - sigv4 authentication
  - anthropic-workspace-id header
  - claude_code_use_anthropic_aws
  - pin model versions
  - provider routing precedence
topics:
  - Claude Code
  - Cloud Model Providers
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/claude-platform-on-aws
access_control_group: ["general"]
---

# Claude Code on Claude Platform on AWS — Setup

## Overview

**Claude Platform on AWS** is the Anthropic-operated Claude API fronted with **AWS authentication, IAM access control, and AWS Marketplace billing**. Requests reach Anthropic's API directly, so you get the same models and features as the direct Claude API on the same release schedule; you authenticate with AWS credentials or a workspace API key and pay through AWS Marketplace. This note is the operational setup procedure for pointing Claude Code at a workspace already provisioned through Claude Platform on AWS — prerequisites, the two authentication methods (Setup step 1), the routing environment variables (step 2), and model pinning (step 3).

Subscribing through AWS Marketplace provisions a **new** Anthropic organization tied to your AWS account, separate from any existing Anthropic organization; credentials do not transfer between them. Use the workspace ID and API keys from the AWS-linked organization, not from a pre-existing Claude Console account. The AWS subscription and workspace setup that comes *before* this is covered by the platform documentation. Routing through a corporate proxy / LLM gateway, targeting this provider from the Agent SDK, and troubleshooting are documented in the sibling note [Claude Platform on AWS — Proxy and SDK](cc_claude_platform_on_aws_proxy_and_sdk.md).

## Prerequisites

Before configuring Claude Code, you need:

- An active Claude Platform on AWS subscription through AWS Marketplace
- A workspace in your AWS-linked Anthropic organization, with its workspace ID
- An IAM principal with permission to invoke the Anthropic service, or an API key scoped to the workspace
- AWS credentials in your environment, in `~/.aws/credentials`, or from an attached IAM role if you want SigV4 authentication. The AWS CLI is required only for the SSO login flow.

## Setup

### 1. Configure AWS credentials

Claude Code supports two authentication methods for Claude Platform on AWS. Choose the method that fits how your team manages access.

**Option A: AWS credentials with SigV4.** Claude Code signs requests with SigV4 using the standard AWS credential chain: environment variables, shared credentials in `~/.aws/credentials`, IAM roles, AWS SSO sessions, and any other sources the AWS SDK supports. For local use, log in with the AWS CLI before starting Claude Code — the example below uses an SSO profile, but any method that produces credentials in the standard locations works:

```bash theme={null}
aws sso login --profile my-profile
export AWS_PROFILE=my-profile
```

For CI and automation, give the runner an IAM role with permission to invoke the Anthropic service and set `AWS_REGION`; the credential chain picks the role up automatically. If your SSO credentials expire mid-session, configure `awsAuthRefresh` (see [Amazon Bedrock advanced credential configuration](https://code.claude.com/docs/en/amazon-bedrock)) so Claude Code re-runs your login command and retries instead of failing. Add the command to your `settings.json`:

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile my-profile"
}
```

**Option B: Workspace API key.** A workspace API key is a long-lived secret, useful when you don't want to manage federated AWS credentials. Generate one in the AWS Console under **Claude Platform on AWS → API keys** and set it as `ANTHROPIC_AWS_API_KEY`:

```bash theme={null}
export ANTHROPIC_AWS_API_KEY=sk-ant-xxxxx
```

The key is sent as `x-api-key` and **takes precedence over SigV4**, so any AWS credentials in your environment are ignored. API keys from a separate Claude Console organization won't work here. Treat workspace API keys like any other production credential; the [user settings file](https://code.claude.com/docs/en/settings) `env` block is a convenient way to scope the key to your machine without exporting it globally.

The `/login` and `/logout` commands do not change Claude Platform on AWS authentication. Authentication runs through your AWS credentials or workspace API key, not through a Claude.ai subscription.

### 2. Configure Claude Code

Set the environment variables that route Claude Code through Claude Platform on AWS instead of the default Anthropic API:

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export AWS_REGION=us-east-1
```

`ANTHROPIC_AWS_WORKSPACE_ID` is **required** and is sent on every request as the `anthropic-workspace-id` header. The base URL is computed from `AWS_REGION` as `https://aws-external-anthropic.{region}.api.aws`; to override the URL directly, set `ANTHROPIC_AWS_BASE_URL`.

Claude Platform on AWS is **opt-in even when AWS credentials are present** in your environment. Bedrock and Foundry take precedence in provider routing, so unset `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_FOUNDRY` if they're set.

### 3. Pin model versions

Claude Platform on AWS uses the same model IDs as the direct Claude API. The default aliases `fable`, `opus`, `sonnet`, and `haiku` resolve to Claude Code's built-in defaults for Claude Platform on AWS, which can lag the newest release. Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias resolves to Opus 4.7. If you deploy Claude Code to a team, pin the model IDs explicitly so a new release doesn't move everyone at once:

```bash theme={null}
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5
```

For other model-related variables, see [Model configuration](https://code.claude.com/docs/en/model-config).

[Prompt caching](https://code.claude.com/docs/en/prompt-caching) is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set `ENABLE_PROMPT_CACHING_1H=1`. The API bills 1-hour cache writes at a higher rate.

## Additional resources

The Claude Platform on AWS subscription, workspace, and IAM setup that comes before configuring Claude Code is covered in the platform documentation: the [Claude Platform on AWS overview](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws) (subscription, workspace setup, product reference) and the [IAM action reference](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions) (permissions and managed policies). Once configured, see [Claude Platform on AWS — Proxy and SDK](cc_claude_platform_on_aws_proxy_and_sdk.md) for proxy routing, Agent SDK targeting, and troubleshooting.

**Source**: https://code.claude.com/docs/en/claude-platform-on-aws
**Last Updated**: 2026-06-13
**Status**: Active
