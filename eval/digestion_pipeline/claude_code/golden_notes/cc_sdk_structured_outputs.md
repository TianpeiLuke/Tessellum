---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - structured_outputs
keywords:
  - structured outputs
  - json schema
  - output_format
  - structured_output result field
  - validated json
  - typed data
  - re-prompt on mismatch
  - free-form vs typed
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/structured-outputs
access_control_group: ["general"]
---

# Agent SDK — Structured Outputs

## Overview

**Structured outputs** let you define the exact shape of data you want back from an Agent SDK agent. The agent can use any tools it needs to complete the task, and you still get **validated JSON matching your schema** at the end. You define a [JSON Schema](https://json-schema.org/understanding-json-schema/about) describing the structure you need, and the SDK validates the agent's output against it, **re-prompting on mismatch**. If validation does not succeed within the retry limit, the result is an error instead of structured data (the error path and schema-definition recipes live in [`cc_sdk_structured_output_schemas`](cc_sdk_structured_output_schemas.md)).

This note covers what structured outputs are and why they exist, the quick-start contract, and the output-format configuration. The type-safe schema workflow (Zod / Pydantic), the multi-step TODO-tracking example, and error handling are the companion procedure note.

## Why structured outputs?

Agents return free-form text by default, which works for chat but not when you need to use the output programmatically. Structured outputs give you typed data you can pass directly to your application logic, database, or UI components.

The docs contrast a recipe agent: without structured outputs you get free-form text (e.g. a "Chocolate Chip Cookies" recipe) that you would have to parse yourself — extract the title, convert "15 minutes" to a number, separate ingredients from instructions, and handle inconsistent formatting across responses. With structured outputs you define the shape you want and get typed data (`name`, `prep_time_minutes`, an `ingredients` array of `{ item, amount, unit }` objects, etc.) you can use directly in your UI.

## Quick start

To use structured outputs, define a JSON Schema describing the shape of data you want, then pass it to `query()` via the `outputFormat` option (TypeScript) or `output_format` option (Python). When the agent finishes, the **result message includes a `structured_output` field** with validated data matching your schema. You read it off the result message (TypeScript checks `message.type === "result" && message.subtype === "success" && message.structured_output`; Python checks `isinstance(message, ResultMessage) and message.structured_output`).

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Define the shape of data you want back
const schema = {
  type: "object",
  properties: {
    company_name: { type: "string" },
    founded_year: { type: "number" },
    headquarters: { type: "string" }
  },
  required: ["company_name"]
};

for await (const message of query({
  prompt: "Research Anthropic and provide key company information",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: schema
    }
  }
})) {
  // The result message contains structured_output with validated data
  if (message.type === "result" && message.subtype === "success" && message.structured_output) {
    console.log(message.structured_output);
    // { company_name: "Anthropic", founded_year: 2021, headquarters: "San Francisco, CA" }
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# Define the shape of data you want back
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "founded_year": {"type": "number"},
        "headquarters": {"type": "string"},
    },
    "required": ["company_name"],
}


async def main():
    async for message in query(
        prompt="Research Anthropic and provide key company information",
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": schema}
        ),
    ):
        # The result message contains structured_output with validated data
        if isinstance(message, ResultMessage) and message.structured_output:
            print(message.structured_output)
            # {'company_name': 'Anthropic', 'founded_year': 2021, 'headquarters': 'San Francisco, CA'}


asyncio.run(main())
```

## Output format configuration

The `outputFormat` (TypeScript) or `output_format` (Python) option accepts an object with:

- `type`: Set to `"json_schema"` for structured outputs.
- `schema`: A JSON Schema object defining your output structure. You can generate this from a Zod schema with `z.toJSONSchema()` or a Pydantic model with `.model_json_schema()` (see [`cc_sdk_structured_output_schemas`](cc_sdk_structured_output_schemas.md)).

The SDK supports standard JSON Schema features including all basic types (object, array, string, number, boolean, null), `enum`, `const`, `required`, nested objects, and `$ref` definitions. For the full list of supported features and limitations, see [JSON Schema limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations).

For full type safety (TypeScript type inference or Python type hints, runtime validation, better error messages, composable schemas), use Zod or Pydantic to define the schema rather than writing JSON Schema by hand — covered in the companion procedure note. Structured output is *not* streamed: it appears only in the final result message, not as partial-message deltas (see [`cc_sdk_streaming_output`](cc_sdk_streaming_output.md)).

**Source**: https://code.claude.com/docs/en/agent-sdk/structured-outputs
**Last Updated**: 2026-06-13
**Status**: Active
