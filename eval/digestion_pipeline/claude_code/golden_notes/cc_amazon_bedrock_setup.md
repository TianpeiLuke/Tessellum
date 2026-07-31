---
tags:
  - resource
  - documentation
  - claude_code
  - amazon_bedrock
  - deployment
keywords:
  - amazon bedrock setup
  - claude_code_use_bedrock
  - setup-bedrock wizard
  - aws sdk credential chain
  - awsauthrefresh
  - awscredentialexport
  - bedrock api key
  - aws region resolution
  - submit use case details
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

# Claude Code on Amazon Bedrock — Setup and Authentication

## Overview

This note is the procedure for pointing Claude Code at **Amazon Bedrock** instead of the default Anthropic API: the prerequisites, the interactive `/setup-bedrock` sign-in wizard, and the manual environment-variable path used in CI or a scripted enterprise rollout. The manual path has three steps covered here — submitting use-case details (once per AWS account), configuring AWS credentials (five options plus advanced refresh hooks), and configuring Claude Code itself with `CLAUDE_CODE_USE_BEDROCK` and region resolution.

Pinning model versions is the fourth manual step and lives in [Bedrock model configuration](cc_amazon_bedrock_model_config.md). The IAM policy, 1M context window, service tiers, Guardrails, and most troubleshooting live in [Bedrock features](cc_amazon_bedrock_features.md), and the native-API-shape Mantle endpoint lives in [Bedrock Mantle endpoint](cc_amazon_bedrock_mantle_endpoint.md).

## Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

- An AWS account with Bedrock access enabled
- Access to desired Claude models (for example, Claude Sonnet 4.6) in Bedrock
- AWS CLI installed and configured (optional — only needed if you don't have another mechanism for getting credentials)
- Appropriate IAM permissions

To sign in with your own Bedrock credentials, follow the sign-in wizard below. To deploy Claude Code across a team, use the manual setup steps and [pin your model versions](cc_amazon_bedrock_model_config.md) before rolling out.

## Sign in with Bedrock

If you have AWS credentials and want to start using Claude Code through Bedrock, the login wizard walks you through it. You complete the AWS-side prerequisites once per account; the wizard handles the Claude Code side.

1. **Enable Anthropic models in your AWS account** — in the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), open the Model catalog, select an Anthropic model, and submit the use case form. Access is granted immediately after submission.
2. **Start Claude Code and choose Bedrock** — run `claude`. At the login prompt, select **3rd-party platform**, then **Amazon Bedrock**.
3. **Follow the wizard prompts** — choose how you authenticate to AWS: an AWS profile detected from your `~/.aws` directory, a Bedrock API key, an access key and secret, or credentials already in your environment. The wizard picks up your region, verifies which Claude models your account can invoke, and lets you pin them. It saves the result to the `env` block of your user settings file, so you don't need to export environment variables yourself.

After you've signed in, run `/setup-bedrock` any time to reopen the wizard and change your credentials, region, or model pins.

## Set up manually

To configure Bedrock through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### 1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per AWS account.

1. Ensure you have the right IAM permissions (see [Bedrock features](cc_amazon_bedrock_features.md))
2. Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
3. Select an Anthropic model from the **Model catalog**
4. Complete the use case form. Access is granted immediately after submission.

If you use AWS Organizations, you can submit the form once from the management account using the [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). This call requires the `bedrock:PutUseCaseForModelAccess` IAM permission. Approval extends to child accounts automatically.

### 2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:

- **Option A: AWS CLI configuration** — run `aws configure`.
- **Option B: Environment variables (access key)** — export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`.
- **Option C: Environment variables (SSO profile)** — run `aws sso login --profile=<your-profile-name>`, then export `AWS_PROFILE`.
- **Option D: AWS Management Console credentials** — run `aws login`.
- **Option E: Bedrock API keys** — export `AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key`. Bedrock API keys provide a simpler authentication method without needing full AWS credentials.

The exports for the most common scripted paths (Options B, C, and E):

```bash theme={null}
# Option B: access key
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token

# Option C: SSO profile
aws sso login --profile=<your-profile-name>
export AWS_PROFILE=your-profile-name

# Option E: Bedrock API key
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

#### Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file. The two settings have different trigger conditions:

- **`awsAuthRefresh`** — runs only when Claude Code detects that your AWS credentials are expired, either locally based on their timestamp or when Bedrock returns a credential error, then retries the request with refreshed credentials. Use it for commands that modify the `.aws` directory (updating credentials, SSO cache, or config files). The command's output is displayed to the user, but interactive input isn't supported. This works well for browser-based SSO flows where the CLI displays a URL or code and you complete authentication in the browser.
- **`awsCredentialExport`** — runs at session start and on each credential reload, even when the credentials in your AWS default credential provider chain are still valid. Use this when your Bedrock account requires cross-account credentials that differ from the ones the default provider chain would resolve, and you can't modify `.aws`. Output is captured silently and not shown to the user.

Example configuration:

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

`awsCredentialExport` must output JSON in this format:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configure Claude Code

Set the following environment variables to enable Bedrock:

```bash theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # optional if your AWS profile already sets a region

# Optional: Override the AWS region for the small/fast model (Bedrock and Mantle).
# On Bedrock, has no effect without ANTHROPIC_DEFAULT_HAIKU_MODEL
# or the deprecated ANTHROPIC_SMALL_FAST_MODEL set.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

When enabling Bedrock for Claude Code, keep the following in mind:

- As of v2.1.172, you only need to set `AWS_REGION` to override your AWS profile's region or when your profile has no region. Claude Code resolves the region in this order: `AWS_REGION`, then `AWS_DEFAULT_REGION`, then the `region` set on your active AWS profile (read from the AWS shared credentials file first and then the shared config file, matching AWS SDK precedence), then `us-east-1`. The active profile is `AWS_PROFILE` if set, otherwise `default`. Set `AWS_SHARED_CREDENTIALS_FILE` or `AWS_CONFIG_FILE` to point at non-default file paths. Run `/status` to see the resolved region; when it came from your AWS config files or the default fallback, `/status` also notes the source. On v2.1.171 and earlier, Claude Code does not read the AWS config files, so set `AWS_REGION` explicitly.
- When using Bedrock, the `/logout` command is unavailable since authentication is handled through AWS credentials.
- The WebSearch tool is not available on Bedrock. See WebSearch tool behavior at https://code.claude.com/docs/en/tools-reference#websearch-tool-behavior.
- You can use settings files for environment variables like `AWS_PROFILE` that you don't want to leak to other processes.

The full environment-variable catalog is at https://code.claude.com/docs/en/env-vars, and settings-file mechanics are at https://code.claude.com/docs/en/settings. The fourth manual step, [pinning model versions](cc_amazon_bedrock_model_config.md), should be completed before rolling out to a team.

**Source**: https://code.claude.com/docs/en/amazon-bedrock
**Last Updated**: 2026-06-13
**Status**: Active
