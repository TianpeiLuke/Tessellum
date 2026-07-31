---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - input_modes
keywords:
  - claudesdkclient streaming input
  - async generator messages
  - base64 image attachment
  - single message query
  - continue conversation session
  - generator exception gotchas
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode
access_control_group: ["general"]
---

# Claude Agent SDK — Streaming & Single-Message Input Examples

## Overview

This note is the implementation recipe for the Claude Agent SDK's two input modes (the mode-choice argument lives in [`cc_sdk_input_modes`](cc_sdk_input_modes.md)). The **streaming input** recipe drives `ClaudeSDKClient` (Python) / `query()` with an async-generator prompt (TypeScript) so a persistent session can yield multiple messages — including a base64-encoded image — and consume streamed assistant responses. The **single-message input** recipe uses a one-shot `query()` plus session continuation (`continue` / `continue_conversation`) for stateless environments. The note also captures the two generator-exception gotchas the SDK documents.

## Streaming input: async-generator messages (incl. image)

Define an async generator that yields `user` messages, hand it to the agent as the `prompt`, and iterate over the streamed responses. The follow-up message attaches an image by base64-encoding a PNG and wrapping it in a content block alongside a `text` block — a multimodal payload only streaming input mode accepts. The session stays alive across yielded messages, and `maxTurns` / `allowedTools` (`max_turns` / `allowed_tools` in Python) scope the run.

```typescript TypeScript theme={null}
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";
import { readFile } from "fs/promises";

async function* generateMessages(): AsyncGenerator<SDKUserMessage> {
  // First message
  yield {
    type: "user",
    message: {
      role: "user",
      content: "Analyze this codebase for security issues"
    },
    parent_tool_use_id: null
  };

  // Wait for conditions or user input
  await new Promise((resolve) => setTimeout(resolve, 2000));

  // Follow-up with image
  yield {
    type: "user",
    message: {
      role: "user",
      content: [
        {
          type: "text",
          text: "Review this architecture diagram"
        },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: await readFile("diagram.png", "base64")
          }
        }
      ]
    },
    parent_tool_use_id: null
  };
}

// Process streaming responses
for await (const message of query({
  prompt: generateMessages(),
  options: {
    maxTurns: 10,
    allowedTools: ["Read", "Grep"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
)
import asyncio
import base64


async def streaming_analysis():
    async def message_generator():
        # First message
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Analyze this codebase for security issues",
            },
        }

        # Wait for conditions
        await asyncio.sleep(2)

        # Follow-up with image
        with open("diagram.png", "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Review this architecture diagram"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data,
                        },
                    },
                ],
            },
        }

    # Use ClaudeSDKClient for streaming input
    options = ClaudeAgentOptions(max_turns=10, allowed_tools=["Read", "Grep"])

    async with ClaudeSDKClient(options) as client:
        # Send streaming input
        await client.query(message_generator())

        # Process responses
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)


asyncio.run(streaming_analysis())
```

## Single-message input: one-shot query + session continuation

For a one-shot response in a stateless environment, pass a plain string `prompt` to `query()`. To continue the conversation, issue a second `query()` with `continue: true` (TypeScript) / `continue_conversation=True` (Python), which resumes the prior session state rather than starting fresh. Single-message mode does not accept direct image attachments.

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Simple one-shot query
for await (const message of query({
  prompt: "Explain the authentication flow",
  options: {
    maxTurns: 1,
    allowedTools: ["Read", "Grep"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}

// Continue conversation with session management
for await (const message of query({
  prompt: "Now explain the authorization process",
  options: {
    continue: true,
    maxTurns: 1
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
import asyncio


async def single_message_example():
    # Simple one-shot query using query() function
    async for message in query(
        prompt="Explain the authentication flow",
        options=ClaudeAgentOptions(max_turns=1, allowed_tools=["Read", "Grep"]),
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

    # Continue conversation with session management
    async for message in query(
        prompt="Now explain the authorization process",
        options=ClaudeAgentOptions(continue_conversation=True, max_turns=1),
    ):
        if isinstance(message, ResultMessage):
            print(message.result)


asyncio.run(single_message_example())
```

## Generator-exception gotchas

- **TypeScript** — if your message generator throws (for example when a file it reads is missing), the stream ends with an error reading `Claude Code process aborted by user` instead of the original error, so check the code inside your generator first when you see that message. The error may also be preceded by a long minified line of bundled SDK source, so read to the end of the output for the error text.
- **Python** — a generator exception is logged at debug level and the session stalls without raising, so if a streaming session hangs with no output, enable debug logging and check your generator.
- **Single-message result errors** — if a single-message `query()` ends with an error result such as `error_max_turns`, the call raises an error including the failure text after yielding the final result message, so wrap the loop in a `try` block if your code needs to continue. See the [agent-loop result subtypes](https://code.claude.com/docs/en/agent-sdk/agent-loop) for the full list.

**Source**: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode
**Last Updated**: 2026-06-13
**Status**: Active
