---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - setup
keywords:
  - agent sdk install
  - npm install claude-agent-sdk
  - pip install claude-agent-sdk
  - anthropic_api_key
  - third-party providers
  - bedrock vertex azure
  - run first agent
  - python 3.10
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/overview
access_control_group: ["general"]
---

# Agent SDK — Install and Authenticate

## Overview

This procedure covers the "Get started" steps for the Claude Agent SDK: install the package (TypeScript via npm or Python via pip), set your authentication credentials (an Anthropic API key, or a third-party provider such as Amazon Bedrock, the Claude Platform on AWS, Google Vertex AI, or Microsoft Azure), and run a first agent that uses built-in tools. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript; this note gets that runtime installed and authenticated before you build anything with it.

After these three steps you have a working agent that can list files in your current directory using built-in tools. For the full end-to-end tutorial, see the sibling [Quickstart bug-fixer](cc_agent_sdk_quickstart_bug_fixer.md); for what the SDK is and its capabilities, see the [Agent SDK overview](cc_agent_sdk_overview.md).

## Step 1 — Install the SDK

Install the package for your language:

```bash
# TypeScript
npm install @anthropic-ai/claude-agent-sdk

# Python
pip install claude-agent-sdk
```

The Python package requires **Python 3.10 or later**. If pip reports `No matching distribution found for claude-agent-sdk`, your interpreter is older than 3.10 — run `python3 --version` on macOS or Linux, or `py --version` on Windows, to check.

The TypeScript SDK bundles a native Claude Code binary for your platform as an optional dependency, so you do not need to install Claude Code separately.

## Step 2 — Set your API key

Get an API key from the [Console](https://platform.claude.com/), then set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=your-api-key
```

### Third-party API providers

The SDK also supports authentication via third-party API providers. Set the corresponding environment variable and configure that provider's credentials:

- **Amazon Bedrock**: set `CLAUDE_CODE_USE_BEDROCK=1` and configure AWS credentials.
- **Claude Platform on AWS**: set `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` and `ANTHROPIC_AWS_WORKSPACE_ID`, then configure AWS credentials.
- **Google Vertex AI**: set `CLAUDE_CODE_USE_VERTEX=1` and configure Google Cloud credentials.
- **Microsoft Azure**: set `CLAUDE_CODE_USE_FOUNDRY=1` and configure Azure credentials.

See the provider setup guides for [Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Claude Platform on AWS](https://code.claude.com/docs/en/claude-platform-on-aws), [Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Azure AI Foundry](https://code.claude.com/docs/en/microsoft-foundry) for details.

Unless previously approved, Anthropic does not allow third-party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods described here instead.

## Step 3 — Run your first agent

This example creates an agent that lists files in your current directory using built-in tools. `allowed_tools` (Python) / `allowedTools` (TypeScript) pre-approves `Bash` and `Glob` so Claude can call them without an approval prompt:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="What files are in this directory?",
        options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"]),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

The equivalent TypeScript iterates the async generator returned by `query({ prompt, options: { allowedTools: ["Bash", "Glob"] } })` and prints `message.result` when `"result" in message`. The full dual-language API references live in the TypeScript and Python SDK reference pages (linked from the [overview](cc_agent_sdk_overview.md)).

## Next steps

Once installed and authenticated, follow the [Quickstart bug-fixer](cc_agent_sdk_quickstart_bug_fixer.md) to create an agent that finds and fixes bugs, or review the [Agent SDK overview](cc_agent_sdk_overview.md) for the full capability tour.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
