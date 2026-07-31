---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - custom_tools
keywords:
  - custom tool
  - create_sdk_mcp_server
  - in-process mcp server
  - tool decorator
  - mcpservers query option
  - tool annotations
  - readonlyhint
  - input schema handler
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

# Agent SDK — Defining a Custom Tool

## Overview

Custom tools extend the Agent SDK by letting you define your own functions that Claude can call during a conversation. Using the SDK's **in-process MCP server**, you give Claude access to databases, external APIs, domain-specific logic, or any other capability your application needs. This note covers the procedure to define a tool from its four parts, bundle it into a server with `create_sdk_mcp_server` / `createSdkMcpServer`, pass it to `query` via the `mcpServers` option, add more tools, and attach behavioral annotations.

The server runs **in-process inside your application**, not as a separate process — the contrast with external MCP servers is covered in [Connect MCP servers](cc_sdk_connect_mcp_servers.md). Tool-name addressing and access control are in [Tool access control](cc_sdk_tool_access_control.md), error returns in [Tool error handling](cc_sdk_tool_error_handling.md), and non-text returns in [Tool rich content](cc_sdk_tool_rich_content.md).

## Quick reference

| If you want to... | Do this |
| :--- | :--- |
| Define a tool | Use `@tool` (Python) or `tool()` (TypeScript) with a name, description, schema, and handler. |
| Register a tool with Claude | Wrap in `create_sdk_mcp_server` / `createSdkMcpServer` and pass to `mcpServers` in `query()`. |
| Pre-approve a tool | Add to your allowed tools. See [Tool access control](cc_sdk_tool_access_control.md). |
| Remove a built-in tool from Claude's context | Pass a `tools` array listing only the built-ins you want. See [Tool access control](cc_sdk_tool_access_control.md). |
| Let Claude call tools in parallel | Set `readOnlyHint: true` on tools with no side effects (see Add tool annotations below). |
| Handle errors without stopping the loop | Return `isError: true` instead of throwing. See [Tool error handling](cc_sdk_tool_error_handling.md). |
| Return images or files | Use `image` or `resource` blocks in the content array. See [Tool rich content](cc_sdk_tool_rich_content.md). |
| Return a machine-readable JSON result | Set `structuredContent` on the result. See [Tool rich content](cc_sdk_tool_rich_content.md). |
| Scale to many tools | Use [tool search](cc_sdk_tool_search.md) to load tools on demand. |

## The four parts of a tool

A tool is defined by four parts, passed to the `tool()` helper (TypeScript) or the `@tool` decorator (Python):

- **Name:** a unique identifier Claude uses to call the tool.
- **Description:** what the tool does. Claude reads this to decide when to call it.
- **Input schema:** the arguments Claude must provide. In TypeScript this is always a [Zod schema](https://zod.dev/), and the handler's `args` are typed from it automatically. In Python this is a dict mapping names to types, like `{"latitude": float}`, which the SDK converts to JSON Schema. The Python decorator also accepts a full JSON Schema dict directly when you need enums, ranges, optional fields, or nested objects.
- **Handler:** the async function that runs when Claude calls the tool. It receives the validated arguments and must return an object with `content` (required) — an array of result blocks, each typed `"text"`, `"image"`, `"audio"`, `"resource"`, or `"resource_link"`; `structuredContent` (optional) — a JSON object of machine-readable data; and `isError` (optional) — set `true` to signal a tool failure so Claude can react.

After defining a tool, wrap it in a server with `createSdkMcpServer` (TypeScript) or `create_sdk_mcp_server` (Python).

To make a parameter optional: in TypeScript, add `.default()` to the Zod field. In Python, the dict schema treats every key as required, so leave the parameter out of the schema, mention it in the description string, and read it with `args.get()` in the handler. Full parameter details (JSON Schema input formats, return-value structure) are in the [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python) and [TypeScript SDK reference](https://code.claude.com/docs/en/agent-sdk/typescript).

## Define a tool and wrap it in a server

This example defines a `get_temperature` tool and wraps it in an MCP server. It only sets up the tool; to pass it to `query` and run it, see Call a custom tool below.

```python Python theme={null}
from typing import Any
import httpx
from claude_agent_sdk import tool, create_sdk_mcp_server


# Define a tool: name, description, input schema, handler
@tool(
    "get_temperature",
    "Get the current temperature at a location",
    {"latitude": float, "longitude": float},
)
async def get_temperature(args: dict[str, Any]) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": args["latitude"],
                "longitude": args["longitude"],
                "current": "temperature_2m",
                "temperature_unit": "fahrenheit",
            },
        )
        data = response.json()

    # Return a content array - Claude sees this as the tool result
    return {
        "content": [
            {
                "type": "text",
                "text": f"Temperature: {data['current']['temperature_2m']}°F",
            }
        ]
    }


# Wrap the tool in an in-process MCP server
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature],
)
```

```typescript TypeScript theme={null}
import { tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

// Define a tool: name, description, input schema, handler
const getTemperature = tool(
  "get_temperature",
  "Get the current temperature at a location",
  {
    latitude: z.number().describe("Latitude coordinate"), // .describe() adds a field description Claude sees
    longitude: z.number().describe("Longitude coordinate")
  },
  async (args) => {
    // args is typed from the schema: { latitude: number; longitude: number }
    const response = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${args.latitude}&longitude=${args.longitude}&current=temperature_2m&temperature_unit=fahrenheit`
    );
    const data: any = await response.json();

    // Return a content array - Claude sees this as the tool result
    return {
      content: [{ type: "text", text: `Temperature: ${data.current.temperature_2m}°F` }]
    };
  }
);

// Wrap the tool in an in-process MCP server
const weatherServer = createSdkMcpServer({
  name: "weather",
  version: "1.0.0",
  tools: [getTemperature]
});
```

## Call a custom tool

Pass the MCP server you created to `query` via the `mcpServers` option. The key in `mcpServers` becomes the `{server_name}` segment in each tool's fully qualified name: `mcp__{server_name}__{tool_name}`. List that name in `allowedTools` so the tool runs without a permission prompt (the name format is detailed in [Tool access control](cc_sdk_tool_access_control.md)).

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_temperature"],
    )

    async for message in query(
        prompt="What's the temperature in San Francisco?",
        options=options,
    ):
        # ResultMessage is the final message after all tool calls complete
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

The TypeScript form mirrors this: pass `mcpServers: { weather: weatherServer }` and `allowedTools: ["mcp__weather__get_temperature"]` in the `query` options, then read `message.result` when `message.type === "result"` and `message.subtype === "success"`.

## Add more tools

A server holds as many tools as you list in its `tools` array. With more than one tool on a server, you can list each one in `allowedTools` individually or use the wildcard `mcp__weather__*` to cover every tool the server exposes. To add a second tool (for example `get_precipitation_chance`), define it the same way and rebuild the server with both tools in the array:

```python Python theme={null}
# Rebuild the server with both tools in the array
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature, get_precipitation_chance],
)
```

Every tool in this array consumes context window space on every turn. If you're defining dozens of tools, see [tool search](cc_sdk_tool_search.md) to load them on demand instead. The same `Example: unit converter` in the source folds the define/register pattern (full JSON Schema for an `enum` constraint) with the error pattern (`isError: true` on an unsupported conversion pair, see [Tool error handling](cc_sdk_tool_error_handling.md)).

## Add tool annotations

[Tool annotations](https://modelcontextprotocol.io/docs/concepts/tools#tool-annotations) are optional metadata describing how a tool behaves. Pass them as the fifth argument to the `tool()` helper in TypeScript or via the `annotations` keyword argument for the `@tool` decorator in Python. All hint fields are Booleans.

| Field | Default | Meaning |
| :--- | :--- | :--- |
| `readOnlyHint` | `false` | Tool does not modify its environment. Controls whether the tool can be called in parallel with other read-only tools. |
| `destructiveHint` | `true` | Tool may perform destructive updates. Informational only. |
| `idempotentHint` | `false` | Repeated calls with the same arguments have no additional effect. Informational only. |
| `openWorldHint` | `true` | Tool reaches systems outside your process. Informational only. |

Annotations are metadata, not enforcement. A tool marked `readOnlyHint: true` can still write to disk if that's what the handler does. Keep the annotation accurate to the handler.

```python Python theme={null}
from claude_agent_sdk import tool, ToolAnnotations


@tool(
    "get_temperature",
    "Get the current temperature at a location",
    {"latitude": float, "longitude": float},
    annotations=ToolAnnotations(
        readOnlyHint=True
    ),  # Lets Claude batch this with other read-only calls
)
async def get_temperature(args):
    return {"content": [{"type": "text", "text": "..."}]}
```

In TypeScript the equivalent passes `{ annotations: { readOnlyHint: true } }` as the fifth argument to `tool()`. See `ToolAnnotations` in the [Python](https://code.claude.com/docs/en/agent-sdk/python) or [TypeScript](https://code.claude.com/docs/en/agent-sdk/typescript) reference.

**Source**: https://code.claude.com/docs/en/agent-sdk/custom-tools
**Last Updated**: 2026-06-13
**Status**: Active
