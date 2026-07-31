---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - custom_tools
keywords:
  - tool content blocks
  - image block base64
  - resource block uri
  - structured content
  - structuredcontent json result
  - audio resource_link blocks
  - mcp calltoolresult
  - rich tool output
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/custom-tools
access_control_group: ["general"]
---

# Agent SDK — Returning Rich Tool Content (Images, Resources, Structured Data)

## Overview

A custom-tool handler in the Claude Agent SDK does not have to return plain text. Its `content` array accepts several block types — `text`, `image`, `audio`, `resource`, and `resource_link` — and these can be mixed in a single response. Beyond `content`, a handler may set `structuredContent`, a separate JSON object holding the result as exact machine-readable fields. These block shapes come from the MCP `CallToolResult` type, so what a tool returns is governed by the MCP tool-result specification.

This note covers the three richer return paths: **image** blocks (base64-encoded bytes processed as visual input), **resource** blocks (content addressed by a URI label), and **`structuredContent`** (raw JSON Claude reads instead of parsing text). It does not cover defining the tool, access control, or the error contract — those are sibling notes.

## Content block types

The `content` array accepts five block types, mixable in one response:

- `text` — a plain text result block.
- `image` — image bytes inline as base64 (see below).
- `audio` — audio blocks are **saved to disk**, and Claude receives a text block with the saved file path.
- `resource` — content embedded under a URI label (see below).
- `resource_link` — converted to a text block containing the link's name, URI, and description.

## Images

An image block carries the image bytes **inline, encoded as base64**. There is no URL field. To return an image that lives at a URL, fetch it in the handler, read the response bytes, and base64-encode them before returning. The result is processed as visual input.

| Field      | Type      | Notes                                                                      |
| :--------- | :-------- | :------------------------------------------------------------------------- |
| `type`     | `"image"` |                                                                            |
| `data`     | `string`  | Base64-encoded bytes. Raw base64 only, no `data:image/...;base64,` prefix  |
| `mimeType` | `string`  | Required. For example `image/png`, `image/jpeg`, `image/webp`, `image/gif` |

```python Python
import base64
import httpx


# Define a tool that fetches an image from a URL and returns it to Claude
@tool("fetch_image", "Fetch an image from a URL and return it to Claude", {"url": str})
async def fetch_image(args):
    async with httpx.AsyncClient() as client:  # Fetch the image bytes
        response = await client.get(args["url"])

    return {
        "content": [
            {
                "type": "image",
                "data": base64.b64encode(response.content).decode(
                    "ascii"
                ),  # Base64-encode the raw bytes
                "mimeType": response.headers.get(
                    "content-type", "image/png"
                ),  # Read MIME type from the response
            }
        ]
    }
```

## Resources

A resource block embeds a piece of content identified by a **URI**. The URI is a *label* for Claude to reference; the actual content rides in the block's `text` or `blob` field. Use this when your tool produces something that makes sense to address by name later, such as a generated file or a record from an external system.

| Field               | Type         | Notes                                                       |
| :------------------ | :----------- | :---------------------------------------------------------- |
| `type`              | `"resource"` |                                                             |
| `resource.uri`      | `string`     | Identifier for the content. Any URI scheme                  |
| `resource.text`     | `string`     | The content, if it's text. Provide this or `blob`, not both |
| `resource.blob`     | `string`     | The content base64-encoded, if it's binary                  |
| `resource.mimeType` | `string`     | Optional                                                    |

The URI such as `file:///tmp/report.md` is a label that Claude can reference later; the **SDK does not read from that path** — the content is supplied inline.

```typescript TypeScript
return {
  content: [
    {
      type: "resource",
      resource: {
        uri: "file:///tmp/report.md", // Label for Claude to reference, not a path the SDK reads
        mimeType: "text/markdown",
        text: "# Report\n..." // The actual content, inline
      }
    }
  ]
};
```

These block shapes come from the MCP `CallToolResult` type; see the MCP specification for the full definition.

## Return structured data

`structuredContent` is an optional JSON object on the result, **separate from the `content` array**. Use it to return raw values that Claude reads as exact fields instead of parsing them out of a text string or image.

When `structuredContent` is set, Claude receives the JSON **plus** any image or resource blocks from `content`. **Text blocks in `content` are not forwarded**, since they are assumed to duplicate the structured data. The example below renders a chart as an image block and returns the data points behind it in `structuredContent` from the same handler.

```typescript TypeScript
return {
  content: [
    {
      type: "image",
      data: chartPngBuffer.toString("base64"),
      mimeType: "image/png"
    }
  ],
  structuredContent: {
    series: "temperature_2m",
    unit: "fahrenheit",
    points: [62.1, 63.4, 65.0, 64.2]
  }
};
```

**Python in-process limitation:** the Python `@tool` decorator forwards only `content` and `is_error` from the handler's return dict. To return `structuredContent` from Python, run a [standalone MCP server](https://code.claude.com/docs/en/agent-sdk/mcp) instead of an in-process SDK server.

**Source**: https://code.claude.com/docs/en/agent-sdk/custom-tools
**Last Updated**: 2026-06-13
**Status**: Active
