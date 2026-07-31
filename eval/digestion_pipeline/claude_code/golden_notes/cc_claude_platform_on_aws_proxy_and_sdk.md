---
tags:
  - resource
  - documentation
  - claude_code
  - claude_platform_on_aws
  - proxy
keywords:
  - claude platform on aws
  - agent sdk
  - corporate proxy
  - llm gateway
  - anthropic_aws_base_url
  - claude_code_skip_anthropic_aws_auth
  - anthropic_auth_token
  - status provider check
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

# Claude Platform on AWS — Agent SDK and Proxy Routing

## Overview

Once Claude Code is configured to use Claude Platform on AWS (the Anthropic-operated Claude API with AWS authentication and AWS Marketplace billing), the same configuration can be reused from the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) and routed through a corporate proxy or LLM gateway. This note covers those two integration paths plus the troubleshooting steps for confirming and fixing provider routing. For the underlying enable + authenticate + pin-models procedure, see the sibling note [Claude Platform on AWS — Setup](cc_claude_platform_on_aws_setup.md).

Because the Agent SDK reads the same environment variables as the CLI, and proxy routing is just a base-URL override plus optional auth delegation, this material builds directly on the setup note's env vars (`CLAUDE_CODE_USE_ANTHROPIC_AWS`, `ANTHROPIC_AWS_WORKSPACE_ID`, AWS credentials or `ANTHROPIC_AWS_API_KEY`).

## Use the Agent SDK

The Agent SDK reads the same environment variables as the CLI, so any program that spawns the Claude Code subprocess can target Claude Platform on AWS by exporting `CLAUDE_CODE_USE_ANTHROPIC_AWS`, `ANTHROPIC_AWS_WORKSPACE_ID`, and either `ANTHROPIC_AWS_API_KEY` or AWS credentials before the call.

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

process.env.CLAUDE_CODE_USE_ANTHROPIC_AWS = "1";
process.env.ANTHROPIC_AWS_WORKSPACE_ID = "wrkspc_01ABCDEFGHIJKLMN";
process.env.AWS_REGION = "us-east-1";

for await (const msg of query({ prompt: "What's in this repo?" })) {
  console.log(msg);
}
```

This example relies on the ambient AWS credential chain for SigV4. To authenticate with a workspace API key instead, set `ANTHROPIC_AWS_API_KEY` the same way. For the broader Agent SDK surface, see the [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview).

## Route through a corporate proxy

To route traffic through a proxy or [LLM gateway](cc_llm_gateway.md), set `ANTHROPIC_AWS_BASE_URL` to the proxy's address. Claude Code sends requests to that URL with the same workspace and authentication headers, so any gateway that forwards them unchanged works.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

If your gateway signs requests itself, set `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1` so Claude Code sends unsigned requests and lets the gateway add SigV4 headers before forwarding to AWS. If the gateway requires its own token, set it in `ANTHROPIC_AUTH_TOKEN`.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

## Troubleshooting

Run `/status` to see the resolved provider and any explicitly configured workspace ID, region, base URL override, and auth-skip setting. This is the fastest way to confirm Claude Code is targeting Claude Platform on AWS at all.

### `403 Forbidden` or `AccessDenied` on every request

The IAM principal Claude Code resolved likely lacks permission to invoke the Anthropic service in your workspace. Check the role attached to your AWS profile or the runner that started Claude Code, and verify it has the `aws-external-anthropic` actions documented in the [IAM action reference](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions).

If you set `ANTHROPIC_AWS_API_KEY`, the key takes precedence over SigV4 and a stale key produces the same error. Regenerate the key in the AWS Console under **Claude Platform on AWS → API keys** or unset the variable to fall back to your AWS credentials.

### Requests fail with a missing-workspace error

`ANTHROPIC_AWS_WORKSPACE_ID` is likely unset or empty. Every Claude Platform on AWS request must include the workspace ID. It is not implied by your AWS credentials. Find the ID under **Workspaces** on the AWS Console service page and export it before starting Claude Code.

### Requests still go to `api.anthropic.com`

`CLAUDE_CODE_USE_ANTHROPIC_AWS` is likely unset or set to a value that doesn't parse as truthy. Set it to `1` and run `/status` to confirm the resolved provider. If `CLAUDE_CODE_USE_BEDROCK` or `CLAUDE_CODE_USE_FOUNDRY` is also set, those take precedence over Claude Platform on AWS.

**Source**: https://code.claude.com/docs/en/claude-platform-on-aws
**Last Updated**: 2026-06-13
**Status**: Active
