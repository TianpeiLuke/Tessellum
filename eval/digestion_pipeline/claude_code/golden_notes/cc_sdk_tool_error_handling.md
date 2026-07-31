---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - custom_tools
keywords:
  - tool error handling
  - iserror
  - is_error
  - uncaught exception
  - agent loop continues
  - return error as tool result
  - try except double catch
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/custom-tools
access_control_group: ["general"]
---

# Agent SDK — Handle Custom Tool Errors

## Overview

When a custom tool's handler hits a failure, *how* it reports that failure decides whether the agent loop keeps running or stops cold. Returning an error result (`isError: true` in TypeScript, `"is_error": True` in Python) hands the failure to Claude as data the loop can react to; letting the exception propagate uncaught stops the loop and fails the `query` call. This note covers that decision and the recommended double-catch handler pattern that keeps the loop alive on both HTTP-status errors and network/parse errors.

## Returned error vs. uncaught throw

How your handler reports errors determines whether the agent loop continues or stops:

| What happens | Result |
| :--- | :--- |
| Handler throws an uncaught exception | Agent loop stops. Claude never sees the error, and the `query` call fails. |
| Handler catches the error and returns `isError: true` (TS) / `"is_error": True` (Python) | Agent loop continues. Claude sees the error as data and can retry, try a different tool, or explain the failure. |

The practical rule: catch failures inside the handler and return them as an error result so Claude can recover, rather than letting them throw and abort the whole `query`.

## The double-catch handler pattern

The recommended pattern catches two kinds of failures inside the handler instead of letting them throw:

1. A non-200 HTTP status is caught from the response and returned as an error result.
2. A network error or invalid JSON is caught by the surrounding `try/except` (Python) or `try/catch` (TypeScript) and also returned as an error result.

In both cases the handler returns normally and the agent loop continues. Marking the result with `is_error` / `isError` signals a *failed call* rather than odd-looking data, so Claude treats it as a failure to react to rather than a strange-but-valid value.

### Python

```python Python theme={null}
import json
import httpx
from typing import Any


@tool(
    "fetch_data",
    "Fetch data from an API",
    {"endpoint": str},  # Simple schema
)
async def fetch_data(args: dict[str, Any]) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(args["endpoint"])
            if response.status_code != 200:
                # Return the failure as a tool result so Claude can react to it.
                # is_error marks this as a failed call rather than odd-looking data.
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"API error: {response.status_code} {response.reason_phrase}",
                        }
                    ],
                    "is_error": True,
                }

            data = response.json()
            return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
    except Exception as e:
        # Catching here keeps the agent loop alive. An uncaught exception
        # would end the whole query() call.
        return {
            "content": [{"type": "text", "text": f"Failed to fetch data: {str(e)}"}],
            "is_error": True,
        }
```

### TypeScript

```typescript TypeScript theme={null}
tool(
  "fetch_data",
  "Fetch data from an API",
  {
    endpoint: z.string().url().describe("API endpoint URL")
  },
  async (args) => {
    try {
      const response = await fetch(args.endpoint);

      if (!response.ok) {
        // Return the failure as a tool result so Claude can react to it.
        // isError marks this as a failed call rather than odd-looking data.
        return {
          content: [
            {
              type: "text",
              text: `API error: ${response.status} ${response.statusText}`
            }
          ],
          isError: true
        };
      }

      const data = await response.json();
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2)
          }
        ]
      };
    } catch (error) {
      // Catching here keeps the agent loop alive. An uncaught throw
      // would end the whole query() call.
      return {
        content: [
          {
            type: "text",
            text: `Failed to fetch data: ${error instanceof Error ? error.message : String(error)}`
          }
        ],
        isError: true
      };
    }
  }
);
```

## Applying it to unhandled inputs

The same `is_error` return covers logical failures, not just I/O errors. The [unit-converter example](https://code.claude.com/docs/en/agent-sdk/custom-tools) shows this: when a conversion pair isn't found, the handler returns `isError: true` so Claude can tell the user what went wrong rather than treating a failure as a normal result. Any predictable "this can't be done" branch in a handler should return an error result the same way.

**Source**: https://code.claude.com/docs/en/agent-sdk/custom-tools
**Last Updated**: 2026-06-13
**Status**: Active
