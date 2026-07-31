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

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK Overview](cc_agent_sdk_overview.md) — relevance: this note's Overview links to it as the "what the SDK is and its capabilities" companion; install/auth is the prerequisite step before the capability tour that overview describes.
- [Agent SDK Quickstart — Build a Bug-Fixing Agent](cc_agent_sdk_quickstart_bug_fixer.md) — relevance: the explicit "Next steps" target — once the SDK is installed and authenticated by this note, the quickstart is the full end-to-end tutorial that builds on it.
- [Agent SDK (TypeScript) — Installation](cc_sdk_typescript_installation.md) — relevance: deep-dives the same `npm install @anthropic-ai/claude-agent-sdk` step this note summarizes, including the bundled-native-binary edge cases (`pathToClaudeCodeExecutable`, `extractFromBunfs()`) the general note only mentions.
- [Claude Code on Amazon Bedrock — Setup and Authentication](cc_amazon_bedrock_setup.md) — relevance: expands this note's one-line `CLAUDE_CODE_USE_BEDROCK=1` third-party-provider bullet into the full Bedrock credential/region procedure.
- [Claude Code on Claude Platform on AWS — Setup](cc_claude_platform_on_aws_setup.md) — relevance: expands the `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` + `ANTHROPIC_AWS_WORKSPACE_ID` provider bullet into its full setup procedure.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: this note installs and authenticates the Agent SDK, which is Claude Code packaged as a library; the TS package even bundles the native Claude Code binary, so the product term grounds the install.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: installing the SDK package is installing the agent harness runtime into your own process; the note's setup steps wire up that harness with credentials.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — relevance: authentication unlocks the SDK's MCP-connected tools; the note's provider/credential setup is the prerequisite for the SDK's MCP and tool capabilities to run.
- [Bedrock Agents](../../term_dictionary/term_bedrock_agents.md) — relevance: the note documents the `CLAUDE_CODE_USE_BEDROCK=1` provider path and AWS credential setup; Bedrock is one of the third-party auth backends, so the term grounds that provider option.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — relevance: the install/auth steps culminate in running a first autonomous agent that lists/edits files; the term defines the class of agent this setup enables.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — relevance: the run-first-agent snippet pre-approves built-in tools (`Bash`, `Glob`) so Claude can call them — the function-calling/tool-use loop this note's final step exercises.
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: an alternative AWS agents SDK to install-and-build-with; the model-driven counterpart you would compare against the Claude Agent SDK this note installs.
- [Tutorial: Installing an Agent CLI on a Restricted Host](../tutorials/tutorial_restricted_host_cli_installation.md) — relevance: a concrete organizational analog of this note's install + authenticate flow — installing Claude Code and doing headless (device-flow) auth on a restricted host where the API-key/browser path is unavailable.
- [Plugin Concepts — Plugin Behavior Differences: Claude Code](../org_docs/org_plugin_concepts_claude_code.md) — relevance: covers the organizational Bedrock-inference-profile model mapping and Claude Code install/plugin behavior, the org-context complement to this note's generic `CLAUDE_CODE_USE_BEDROCK` provider setup.
- [AgentCore Framework Integration](../aws_bedrock_agentcore/bedrock_agentcore_framework_integration.md) — relevance: shows the AWS-hosted wrap-and-deploy pattern (`BedrockAgentCoreApp` + `@app.entrypoint`) for agent SDKs including the OpenAI Agents SDK and Strands, the production-hosting counterpart to the locally-installed agent this note bootstraps.
- [Band Adapter Setup](../band/band_adapter_setup.md) — the Band platform's adapter install/credential-provisioning procedure; relevance: this Claude Agent SDK note documents the exact install -> set-credential -> run-first-agent procedure that Band setup mirrors (install band-sdk, write the LLM-provider/API key, run a verify script), giving a reader a clean side-by-side cross-ecosystem example of the same credential-provisioning step on the Band platform — the band note already cites this note as its closest external precedent, so the reverse link closes the pair.

*(No project note is closely relevant to installing/authenticating the Claude Agent SDK; the domain-specific agent projects are applications, not SDK-setup procedures.)*

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
