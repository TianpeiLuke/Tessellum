---
tags:
  - resource
  - documentation
  - claude_code
  - prompt_caching
  - context_window
keywords:
  - prompt caching mechanism
  - prefix matching
  - cache prefix
  - system prompt project context conversation layers
  - cache key model effort level
  - exact prefix match
  - claude code automatic caching
topics:
  - Claude Code
  - Prompt Caching
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/prompt-caching
access_control_group: ["general"]
---

# Claude Code — How Prompt Caching Works

## Overview

Prompt caching makes Claude Code faster and more cost-efficient: without it the API would reprocess the full conversation history on every turn, but with it the API reuses what it already processed and only does new work for what changed. Claude Code **manages prompt caching automatically** (unless you disable it), so understanding the mechanism matters mainly because some actions invalidate the cache and make the next response slower and more expensive while it rebuilds.

This note documents the underlying mechanism: how the cache is organized around an **exact prefix match**, how Claude Code orders each request into three layers so rarely-changing content comes first, and the two cache-key dimensions (model and effort level) that sit outside the prompt text entirely. The catalog of invalidating actions, cache-preserving actions, and cache lifetime/scope are covered in the sibling notes.

## How the cache is organized

Each time you send a message, Claude Code makes a **new API request**. The model doesn't remember anything between requests, so Claude Code re-sends the full context: the system prompt, your project context, every prior message and tool result, and your new message. New content is appended at the end, which means **most of each request is identical to the one before it**. Prompt caching is how the API avoids reprocessing the part that didn't change.

The API caches by matching the **start of each request, called the prefix**, against content it recently processed. On a normal turn, the prefix is the entire previous request and only the latest exchange is new. The **match is exact**, so a change anywhere in the prefix recomputes everything after it. There is **no per-file or per-segment caching**.

### The three request layers

To get the most out of prefix matching, Claude Code orders each request so content that rarely changes between turns comes first:

| Layer           | Content                                           | Changes when                                                           |
| --------------- | ------------------------------------------------- | ---------------------------------------------------------------------- |
| System prompt   | Core instructions, tool definitions, output style | The set of loaded tool definitions changes, or Claude Code is upgraded |
| Project context | CLAUDE.md, auto memory, unscoped rules            | Session starts, or after `/clear` or `/compact`                        |
| Conversation    | Your messages, Claude's responses, tool results   | Every turn                                                             |

A change to the **conversation layer** leaves the system prompt and project context cached. A change to the **system prompt invalidates everything**, because all later content now sits behind a different prefix. The third column gives common triggers rather than an exhaustive list (the [actions that invalidate the cache](cc_cache_invalidation_actions.md) and [actions that keep the cache](cc_cache_preserving_actions.md) cover the full set, including content such as output style that is fixed at session start).

The prefix-match rule explains most caching behaviors. Plan mode and skill loading, for example, append their instructions as conversation messages, so the cached prefix stays intact.

### Two cache-key dimensions outside the prompt text

Two settings aren't part of the prompt text at all, so they don't appear in the layer table, but both are part of the **cache key**:

- **Model**: each model has its own cache. Switching models recomputes the entire request even when the content is identical.
- **Effort level**: each effort level has its own cache for the same model. Changing it mid-session recomputes the entire request, and Claude Code asks you to confirm before applying the change.

Because each model and each effort level keys a separate cache, the per-action detail for switching either of these lives in [actions that invalidate the cache](cc_cache_invalidation_actions.md); the model/effort configuration itself is documented at the [model configuration page](https://code.claude.com/docs/en/model-config).

**Tip from the source**: pick your model and effort level at the top of a session, then save `/compact` for natural breaks between tasks. The fewer changes you make mid-task, the higher your cache hit rate.

> **Where the cache lives**: caching happens server-side, in whichever infrastructure serves your model, and the location depends on how you authenticate (Anthropic's infrastructure for an API key/subscription, your cloud provider's serving infrastructure for Bedrock or Vertex AI). That provider-location detail and the TTL/scope of the cache are documented in [cache lifetime and scope](cc_cache_lifetime_and_scope.md).

**Source**: https://code.claude.com/docs/en/prompt-caching
**Last Updated**: 2026-06-13
**Status**: Active
