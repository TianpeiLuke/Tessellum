---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - structured_output
keywords:
  - type-safe schemas
  - zod tojsonschema
  - pydantic model_json_schema
  - safeparse model_validate
  - todo tracking agent
  - error_max_structured_output_retries
  - structured output error handling
  - multi-step tool use
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/structured-outputs
access_control_group: ["general"]
---

# Agent SDK — Type-Safe Schemas & Structured-Output Error Handling

## Overview

This procedure covers how to produce structured output in practice: define a typed schema with **Zod** (TypeScript) or **Pydantic** (Python), convert it to JSON Schema, pass it to `query()`, and validate the returned `structured_output` back into a fully-typed object. It then walks a multi-step example — a TODO-tracking agent that autonomously calls Grep and Bash before returning one schema-validated response — and finishes with **error handling**: the `error_max_structured_output_retries` result subtype, the model-fallback retraction edge case, and tips for avoiding validation failures.

The conceptual basis (what structured outputs are, the `outputFormat`/`output_format` config, supported JSON Schema features) lives in the sibling note [cc_sdk_structured_outputs](cc_sdk_structured_outputs.md); this note is the hands-on recipe layered on top of it.

## Type-safe schemas with Zod and Pydantic

Instead of writing JSON Schema by hand, use [Zod](https://zod.dev/) (TypeScript) or [Pydantic](https://docs.pydantic.dev/latest/) (Python). These libraries generate the JSON Schema for you and let you parse the response into a fully-typed object you can use throughout your codebase with autocomplete and type checking.

The steps:

1. **Define the schema** with `z.object(...)` (Zod) or a `BaseModel` subclass (Pydantic).
2. **Convert to JSON Schema** — `z.toJSONSchema(Schema)` (TypeScript) or `Schema.model_json_schema()` (Python).
3. **Pass it** to `query()` via `outputFormat` / `output_format` with `type: "json_schema"`.
4. **Validate the result** — call `Schema.safeParse(message.structured_output)` (TypeScript) or `Schema.model_validate(message.structured_output)` (Python) to get the strongly-typed object.

The example below defines a schema for a feature implementation plan (a summary, a list of steps each with a complexity level, and potential risks). The agent plans the feature and returns a typed `FeaturePlan` object; you can then access `plan.summary` and iterate `plan.steps` with full type safety.

```typescript TypeScript
import { z } from "zod";
import { query } from "@anthropic-ai/claude-agent-sdk";

// Define schema with Zod
const FeaturePlan = z.object({
  feature_name: z.string(),
  summary: z.string(),
  steps: z.array(
    z.object({
      step_number: z.number(),
      description: z.string(),
      estimated_complexity: z.enum(["low", "medium", "high"])
    })
  ),
  risks: z.array(z.string())
});

type FeaturePlan = z.infer<typeof FeaturePlan>;

// Convert to JSON Schema
const schema = z.toJSONSchema(FeaturePlan);

// Use in query
for await (const message of query({
  prompt:
    "Plan how to add dark mode support to a React app. Break it into implementation steps.",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: schema
    }
  }
})) {
  if (message.type === "result" && message.subtype === "success" && message.structured_output) {
    // Validate and get fully typed result
    const parsed = FeaturePlan.safeParse(message.structured_output);
    if (parsed.success) {
      const plan: FeaturePlan = parsed.data;
      console.log(`Feature: ${plan.feature_name}`);
      console.log(`Summary: ${plan.summary}`);
      plan.steps.forEach((step) => {
        console.log(`${step.step_number}. [${step.estimated_complexity}] ${step.description}`);
      });
    }
  }
}
```

```python Python
import asyncio
from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


class Step(BaseModel):
    step_number: int
    description: str
    estimated_complexity: str  # 'low', 'medium', 'high'


class FeaturePlan(BaseModel):
    feature_name: str
    summary: str
    steps: list[Step]
    risks: list[str]


async def main():
    async for message in query(
        prompt="Plan how to add dark mode support to a React app. Break it into implementation steps.",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": FeaturePlan.model_json_schema(),
            }
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            # Validate and get fully typed result
            plan = FeaturePlan.model_validate(message.structured_output)
            print(f"Feature: {plan.feature_name}")
            print(f"Summary: {plan.summary}")
            for step in plan.steps:
                print(
                    f"{step.step_number}. [{step.estimated_complexity}] {step.description}"
                )


asyncio.run(main())
```

**Benefits:**

- Full type inference (TypeScript) and type hints (Python)
- Runtime validation with `safeParse()` or `model_validate()`
- Better error messages
- Composable, reusable schemas

## Example: TODO tracking agent

This example demonstrates how structured outputs work with **multi-step tool use**. The agent needs to find TODO comments in the codebase, then look up git blame information for each one. It autonomously decides which tools to use (Grep to search, Bash to run git commands) and combines the results into a single structured response.

The schema includes optional fields (`author` and `date`) since git blame information might not be available for all files. The agent fills in what it can find and omits the rest. The TypeScript handler reads `message.structured_output` and prints each TODO with its location, plus author/date when present.

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# Define structure for TODO extraction
todo_schema = {
    "type": "object",
    "properties": {
        "todos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "number"},
                    "author": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["text", "file", "line"],
            },
        },
        "total_count": {"type": "number"},
    },
    "required": ["todos", "total_count"],
}


async def main():
    # Agent uses Grep to find TODOs, Bash to get git blame info
    async for message in query(
        prompt="Find all TODO comments in this codebase and identify who added them",
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": todo_schema}
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            data = message.structured_output
            print(f"Found {data['total_count']} TODOs")
            for todo in data["todos"]:
                print(f"{todo['file']}:{todo['line']} - {todo['text']}")
                if "author" in todo:
                    print(f"  Added by {todo['author']} on {todo['date']}")


asyncio.run(main())
```

The TypeScript form is identical in shape — the same `todoSchema` passed via `outputFormat`, with the result cast to `{ total_count: number; todos: Array<{ file: string; line: number; text: string; author?: string; date?: string }> }` before iterating.

## Error handling

Structured output generation can fail when the agent cannot produce valid JSON matching your schema. This typically happens when the schema is too complex for the task, the task itself is ambiguous, or the agent hits its retry limit trying to fix validation errors. It can also happen **without any validation failure**: a [model fallback](https://code.claude.com/docs/en/model-config#automatic-model-fallback) can retract an already-completed output mid-stream, and if no retry replaces it the run ends with the same error. Check the result's `errors` text to tell the two causes apart before debugging your schema.

When an error occurs, the result message has a `subtype` indicating what went wrong:

| Subtype | Meaning |
| --- | --- |
| `success` | Output was generated and validated successfully |
| `error_max_structured_output_retries` | No valid output survived after multiple attempts (validation failures, or a model-fallback retraction with no successful retry) |

Check the `subtype` field to determine whether the output was generated successfully or whether you need to handle a failure:

```typescript TypeScript
for await (const msg of query({
  prompt: "Extract contact info from the document",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: contactSchema
    }
  }
})) {
  if (msg.type === "result") {
    if (msg.subtype === "success" && msg.structured_output) {
      // Use the validated output
      console.log(msg.structured_output);
    } else if (msg.subtype === "error_max_structured_output_retries") {
      // Handle the failure - retry with simpler prompt, fall back to unstructured, etc.
      console.error("Could not produce valid output");
    }
  }
}
```

```python Python
async for message in query(
    prompt="Extract contact info from the document",
    options=ClaudeAgentOptions(
        output_format={"type": "json_schema", "schema": contact_schema}
    ),
):
    if isinstance(message, ResultMessage):
        if message.subtype == "success" and message.structured_output:
            # Use the validated output
            print(message.structured_output)
        elif message.subtype == "error_max_structured_output_retries":
            # Handle the failure
            print("Could not produce valid output")
```

**Tips for avoiding errors:**

- **Keep schemas focused.** Deeply nested schemas with many required fields are harder to satisfy. Start simple and add complexity as needed.
- **Match schema to task.** If the task might not have all the information your schema requires, make those fields optional.
- **Use clear prompts.** Ambiguous prompts make it harder for the agent to know what output to produce.

**Source**: https://code.claude.com/docs/en/agent-sdk/structured-outputs
**Last Updated**: 2026-06-13
**Status**: Active
