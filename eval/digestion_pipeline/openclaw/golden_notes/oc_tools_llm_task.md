---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - llm_task
keywords:
  - openclaw llm-task tool
  - json-only llm step
  - llm-task plugin enable
  - tools.alsoAllow llm-task
  - llm-task schema validation
  - details.json structured output
  - lobster openclaw.invoke limitation
  - llm-task allowedModels
topics:
  - OpenClaw
  - Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/llm-task
access_control_group: ["general"]
---

# OpenClaw — Enabling and Calling the `llm-task` Plugin Tool

## Overview

This note is the procedure for using OpenClaw's **`llm-task`** tool: an **optional plugin tool** that runs a single JSON-only LLM task and returns structured output, optionally validated against a JSON Schema. It mirrors the `tools/llm-task` source page — enabling the plugin and allowing the optional tool, the optional defaults config block, the full tool-parameter surface, the `details.json` output contract, the worked Lobster-workflow-step example (including the embedded-runner `openclaw.invoke` limitation), and the JSON-only safety notes. `llm-task` is designed to add a single LLM step inside workflow engines like Lobster without writing custom OpenClaw code for each workflow.

## Enable the plugin

`llm-task` is not on by default; it must be enabled as a plugin and then allowed as an optional tool. First, enable the plugin entry:

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}
```

Then allow the optional tool so the agent may call it:

```json
{
  "tools": {
    "alsoAllow": ["llm-task"]
  }
}
```

Use `tools.allow` only when you want restrictive allowlist mode (otherwise `tools.alsoAllow` adds the tool on top of the default set rather than replacing it).

## Config (optional)

The plugin entry accepts an optional `config` block of defaults applied to every call:

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai",
          "defaultModel": "gpt-5.5",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai/gpt-5.5"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` is an allowlist of `provider/model` strings. If set, any request outside the list is rejected.

## Tool parameters

When the agent calls `llm-task`, the tool accepts these parameters (only `prompt` is required):

- `prompt` (string, required)
- `input` (any, optional)
- `schema` (object, optional JSON Schema)
- `provider` (string, optional)
- `model` (string, optional)
- `thinking` (string, optional)
- `authProfileId` (string, optional)
- `temperature` (number, optional)
- `maxTokens` (number, optional)
- `timeoutMs` (number, optional)

`thinking` accepts the standard OpenClaw reasoning presets, such as `low` or `medium`.

## Output

The tool returns `details.json` containing the parsed JSON, and validates that JSON against `schema` when a `schema` parameter is provided.

## Example: Lobster workflow step

### Important limitation

The example below assumes the **standalone Lobster CLI** is running in an environment where `openclaw.invoke` already has the correct gateway URL/auth context. For the bundled **embedded** Lobster runner inside OpenClaw, this nested CLI pattern is **not currently reliable**:

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{ ... }'
```

Until embedded Lobster has a supported bridge for this flow, prefer either direct `llm-task` tool calls outside Lobster, or Lobster steps that do not rely on nested `openclaw.invoke` calls.

A standalone Lobster CLI example calling `llm-task` with an `input`, a `thinking` preset, and an output `schema`:

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "thinking": "low",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## Safety notes

The tool is **JSON-only** and instructs the model to output only JSON (no code fences, no commentary). No tools are exposed to the model for this run. Treat the output as untrusted unless you validate it with `schema`. Put approvals before any side-effecting step (send, post, exec).

**Source**: OpenClaw documentation — `tools/llm-task` (mirror `inbox/openclaw_docs/tools/llm-task.md`)
**Last Updated**: 2026-06-22
**Status**: Active
