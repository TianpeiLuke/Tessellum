---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - cost_tracking
keywords:
  - total_cost_usd
  - modelusage
  - per-step token usage
  - deduplicate by message id
  - cache token tracking
  - enable_prompt_caching_1h
  - client-side cost estimate
  - accumulate cost across calls
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/cost-tracking
access_control_group: ["general"]
---

# SDK Cost and Usage Tracking

## Overview

The Claude Agent SDK reports detailed token usage for every interaction, and this note is the procedure for reading and accumulating that data correctly. The SDK exposes the same data in TypeScript and Python with different field names: per-step token breakdowns on each assistant message, per-model cost via `modelUsage`/`model_usage` on the result message, and a cumulative total on the result message. The recurring pitfalls this procedure solves are double-counting parallel tool calls (multiple assistant messages share one ID and one usage object), the absence of any session-level total (you accumulate across `query()` calls yourself), and treating client-side estimates as billing data.

The `total_cost_usd` and `costUSD` fields are **client-side estimates, not authoritative billing data** — the SDK computes them locally from a price table bundled at build time, so they can drift from your actual bill when pricing changes, the installed SDK version does not recognize a model, or billing rules apply that the client cannot model. Use these fields for development insight and approximate budgeting; for authoritative billing use the Usage and Cost API or the Claude Console Usage page. Do not bill end users or trigger financial decisions from these fields.

## Understand token usage

Cost tracking depends on how the SDK scopes usage data across three levels:

- **`query()` call** — one invocation of the SDK's `query()` function. A single call can involve multiple steps (Claude responds, uses tools, gets results, responds again). Each call produces one `result` message at the end.
- **Step** — a single request/response cycle within a `query()` call. Each step produces assistant messages with token usage.
- **Session** — a series of `query()` calls linked by a session ID (using the `resume` option). Each `query()` call within a session reports its own cost independently.

Within a single `query()` call the message stream reports token usage at each step plus a cumulative estimate at the end. When Claude responds it sends one or more assistant messages. In TypeScript each assistant message contains a nested `BetaMessage` (accessed via `message.message`) with an `id` and a `usage` object holding token counts (`input_tokens`, `output_tokens`); in Python the `AssistantMessage` dataclass exposes the same data directly via `message.usage` and `message.message_id`. When Claude uses multiple tools in one turn, all messages in that turn share the same ID, so **deduplicate by ID to avoid double-counting**. When the `query()` call completes, the SDK emits a result message with `total_cost_usd` and cumulative `usage` (`SDKResultMessage` in TypeScript, `ResultMessage` in Python). If you only need the estimated total, ignore the per-step usage and read this single value.

## Get the total cost of a query

The result message marks the end of the agent loop for a `query()` call. It includes `total_cost_usd`, the cumulative estimated cost across all steps in that call, for both success and error results. With sessions, each result reflects only that individual call's cost. Iterate over the stream and read the field when the `result` message arrives:

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type === "result") {
    console.log(`Total cost: $${message.total_cost_usd}`);
  }
}
```

The Python equivalent checks `isinstance(message, ResultMessage)` and reads `message.total_cost_usd or 0`.

## Track per-step and per-model usage

The examples below use TypeScript field names. In Python the equivalent fields are `AssistantMessage.usage` and `AssistantMessage.message_id` for per-step usage, and `ResultMessage.model_usage` for per-model breakdowns.

### Track per-step usage

Each assistant message carries a nested `BetaMessage` (via `message.message`) with an `id` and a `usage` object. When Claude uses tools in parallel, multiple messages share the same `id` with identical usage data, so track which IDs you have already counted and skip duplicates to avoid inflated totals. The following example accumulates input and output tokens across all steps, counting each unique message ID only once:

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const seenIds = new Set<string>();
let totalInputTokens = 0;
let totalOutputTokens = 0;

for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type === "assistant") {
    const msgId = message.message.id;

    // Parallel tool calls share the same ID, only count once
    if (!seenIds.has(msgId)) {
      seenIds.add(msgId);
      totalInputTokens += message.message.usage.input_tokens;
      totalOutputTokens += message.message.usage.output_tokens;
    }
  }
}

console.log(`Steps: ${seenIds.size}`);
console.log(`Input tokens: ${totalInputTokens}`);
console.log(`Output tokens: ${totalOutputTokens}`);
```

### Break down usage per model

The result message includes `modelUsage`, a map of model name to per-model token counts and cost. This is useful when you run multiple models (for example, Haiku for subagents and Opus for the main agent) and want to see where tokens are going:

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type !== "result") continue;

  for (const [modelName, usage] of Object.entries(message.modelUsage)) {
    console.log(`${modelName}: $${usage.costUSD.toFixed(4)}`);
    console.log(`  Input tokens: ${usage.inputTokens}`);
    console.log(`  Output tokens: ${usage.outputTokens}`);
    console.log(`  Cache read: ${usage.cacheReadInputTokens}`);
    console.log(`  Cache creation: ${usage.cacheCreationInputTokens}`);
  }
}
```

## Accumulate costs across multiple calls

Each `query()` call returns its own `total_cost_usd`. The SDK does **not** provide a session-level total, so if your application makes multiple `query()` calls (for example, in a multi-turn session or across different users), accumulate the totals yourself by adding each result's `total_cost_usd` to a running total:

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Track cumulative cost across multiple query() calls
let totalSpend = 0;

const prompts = [
  "Read the files in src/ and summarize the architecture",
  "List all exported functions in src/auth.ts"
];

for (const prompt of prompts) {
  for await (const message of query({ prompt })) {
    if (message.type === "result") {
      totalSpend += message.total_cost_usd;
      console.log(`This call: $${message.total_cost_usd}`);
    }
  }
}

console.log(`Total spend: $${totalSpend.toFixed(4)}`);
```

The Python version maintains `total_spend = 0.0`, loops the same prompts, and adds `message.total_cost_usd or 0` for each `ResultMessage`.

## Handle errors, caching, and token discrepancies

For accurate cost tracking, account for failed conversations, cache token pricing, and occasional reporting inconsistencies.

- **Resolve output token discrepancies** — in rare cases you might observe different `output_tokens` values for messages with the same ID. When this occurs: (1) **use the highest value** — the final message in a group typically contains the accurate total; (2) **prefer the result message** — the `total_cost_usd` in the result message reflects the SDK's accumulated estimate across all steps, so it is more reliable than summing per-step values yourself (it is still an estimate and may differ from your actual bill); (3) **report inconsistencies** at the Claude Code GitHub repository.
- **Track costs on failed conversations** — both success and error result messages include `usage` and `total_cost_usd`. If a conversation fails mid-way, you still consumed tokens up to the point of failure, so always read cost data from the result message regardless of its `subtype`.

### Track cache tokens

The Agent SDK automatically uses prompt caching to reduce costs on repeated content — you do not configure caching yourself. The usage object adds two cache-tracking fields:

- `cache_creation_input_tokens` — tokens used to create new cache entries (charged at a **higher** rate than standard input tokens).
- `cache_read_input_tokens` — tokens read from existing cache entries (charged at a **reduced** rate).

Track these separately from `input_tokens` to understand caching savings. In TypeScript these are typed on the `Usage` object; in Python they appear as keys in the `ResultMessage.usage` dict (for example, `message.usage.get("cache_read_input_tokens", 0)`).

### Extend the prompt cache TTL to one hour

Cache entries written by the SDK use a 5-minute TTL by default when you authenticate with an API key or run on Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry. If your workload runs many short sessions against the same system prompt and context with gaps longer than 5 minutes between them, the cache expires between sessions and each new session pays full input price. To request a 1-hour TTL on cache writes, set the `ENABLE_PROMPT_CACHING_1H` environment variable — export it in your shell or container environment, or pass it through `options.env`:

```python theme={null}
from claude_agent_sdk import ClaudeAgentOptions, query
import asyncio


async def main():
    options = ClaudeAgentOptions(
        env={
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "ENABLE_PROMPT_CACHING_1H": "1",
        },
    )

    async for message in query(prompt="Summarize this project", options=options):
        print(message)


asyncio.run(main())
```

Cache writes with a 1-hour TTL are billed at a higher rate than 5-minute writes, so enabling this trades higher write cost for more cache reads. Claude subscription users already receive 1-hour TTL automatically and do not need to set this variable. For the underlying caching feature and pricing, see [prompt caching](https://code.claude.com/docs/en/prompt-caching) (B02A); for the Bedrock/Vertex/Foundry providers referenced here, see the [provider configuration docs](https://code.claude.com/docs/en/bedrock-vertex-proxies) (B14A).

**Source**: https://code.claude.com/docs/en/agent-sdk/cost-tracking
**Last Updated**: 2026-06-13
**Status**: Active
