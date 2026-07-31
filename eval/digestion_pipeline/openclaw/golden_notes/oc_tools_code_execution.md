---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - code_execution
keywords:
  - openclaw code_execution tool
  - sandboxed remote python xai
  - xai responses api code execution
  - grok-4-1-fast code execution model
  - codeExecution.enabled config
  - missing_xai_api_key error
  - XAI_API_KEY auth
  - code_execution vs exec
topics:
  - OpenClaw
  - Tools
  - Code Execution
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/code-execution
access_control_group: ["general"]
---

# OpenClaw — Enabling and Using the `code_execution` Tool

## Overview

This note is the operational procedure for OpenClaw's `code_execution` tool, which runs sandboxed remote Python analysis on xAI's Responses API. It mirrors the `tools/code-execution` source page in full: providing xAI credentials, enabling and tuning the tool via `plugins.entries.xai.config.codeExecution`, restarting the Gateway, invoking the tool from natural-language prompts, the structured `missing_xai_api_key` error surface, and the remote-execution limits. `code_execution` is registered by the bundled `xai` plugin (under the `tools` contract) and dispatches to the same `https://api.x.ai/v1/responses` endpoint used by `x_search`. It is distinct from the local `exec` tool: `exec` runs shell commands on your machine or paired node, while `code_execution` runs Python in xAI's remote sandbox.

## Tool Properties

The bundled `xai` plugin contributes `code_execution` with the following defaults (verbatim from the source property table):

| Property | Value |
| --- | --- |
| Tool name | `code_execution` |
| Provider plugin | `xai` (bundled, `enabledByDefault: true`) |
| Auth | xAI auth profile, `XAI_API_KEY`, or `plugins.entries.xai.config.webSearch.apiKey` |
| Default model | `grok-4-1-fast` |
| Default timeout | 30 seconds |
| Default `maxTurns` | unset (xAI applies its own internal limit) |

Use `code_execution` for: calculations; tabulation; quick statistics; chart-style analysis; and analyzing data returned by `x_search` or `web_search`. Do **not** use it when you need local files, your shell, your repo, or paired devices — use `exec` for that.

## Setup

The source documents a three-step setup.

### Step 1 — Provide xAI credentials

Sign in with Grok OAuth using an eligible SuperGrok or X Premium subscription, use the remote-friendly device-code flow, or store an API key. OAuth works for `code_execution` and `x_search`; `XAI_API_KEY` or plugin web-search config can also power Grok `web_search`. The first two commands below sign in via the auth-login flow; during a fresh install the same auth choices are available inside onboarding (the `openclaw onboard` commands):

```bash
openclaw models auth login --provider xai --method oauth
openclaw models auth login --provider xai --device-code
openclaw onboard --install-daemon
openclaw onboard --install-daemon --auth-choice xai-device-code
```

Or use an API key (`export XAI_API_KEY=xai-...`), or supply it via config under `plugins.entries.xai.config.webSearch.apiKey`:

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          webSearch: {
            apiKey: "xai-...",
          },
        },
      },
    },
  },
}
```

### Step 2 — Enable and tune `code_execution`

`code_execution` is available when xAI credentials are available. Set `plugins.entries.xai.config.codeExecution.enabled` to `false` to disable it, or use the same block to tune the model and timeout.

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          codeExecution: {
            enabled: true,
            model: "grok-4-1-fast", // override the default xAI code-execution model
            maxTurns: 2,            // optional cap on internal tool turns
            timeoutSeconds: 30,     // request timeout (default: 30)
          },
        },
      },
    },
  },
}
```

### Step 3 — Restart the Gateway

Restart the Gateway so the change takes effect; `code_execution` shows up in the agent's tool list once the xAI plugin re-registers with `enabled: true`.

```bash
openclaw gateway restart
```

## How to use it

Ask naturally and make the analysis intent explicit. The tool takes a single `task` parameter internally, so the agent should send the full analysis request and any inline data in one prompt. The source gives these example prompts:

```text
Use code_execution to calculate the 7-day moving average for these numbers: ...
Use x_search to find posts mentioning OpenClaw this week, then use code_execution to count them by day.
Use web_search to gather the latest AI benchmark numbers, then use code_execution to compare percent changes.
```

## Errors

When the tool runs without auth, it returns a structured `missing_xai_api_key` error pointing at the auth-profile, env var, and config options. The error is JSON, not a thrown exception, so the agent can self-correct:

```json
{
  "error": "missing_xai_api_key",
  "message": "code_execution needs xAI credentials. Run `openclaw onboard --auth-choice xai-oauth` to sign in with Grok, run `openclaw onboard --auth-choice xai-api-key`, set `XAI_API_KEY` in the Gateway environment, or configure `plugins.entries.xai.config.webSearch.apiKey`.",
  "docs": "https://docs.openclaw.ai/tools/code-execution"
}
```

## Limits

The source lists four constraints on `code_execution`:

- This is remote xAI execution, not local process execution.
- Treat results as ephemeral analysis, not a persistent notebook session.
- Do not assume access to local files or your workspace.
- For fresh X data, use `x_search` first and pipe the result into `code_execution`.

**Source**: OpenClaw documentation — `tools/code-execution` (mirror `inbox/openclaw_docs/tools/code-execution.md`)
**Last Updated**: 2026-06-22
**Status**: Active
