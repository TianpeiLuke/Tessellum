---
tags:
  - resource
  - documentation
  - claude_code
  - prompt_caching
  - cache_invalidation
keywords:
  - cache invalidation
  - actions that invalidate the cache
  - switching models
  - changing effort level
  - turning on fast mode
  - mcp server connect disconnect
  - enabling disabling a plugin
  - denying an entire tool
  - compacting the conversation
  - upgrading claude code
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

# Claude Code — Actions That Invalidate the Cache

## Overview

Some actions in a Claude Code session cause the next request to miss part or all of the [prompt cache](cc_prompt_caching_mechanism.md). When that happens you see a one-time slower, more expensive turn, after which the new prefix is cached. Most of these actions are avoidable mid-task once you know they carry a cost — a model switch, for example, can feel free until you notice the slower turn that follows.

This note catalogs the **eight actions** the docs list as cache-invalidating, along with the "why" for each (which usually traces back to the prefix-match rule: a change anywhere in the prefix recomputes everything after it, and the model and effort level are also part of the cache key). The inverse list — [actions that keep the cache](cc_cache_preserving_actions.md) — is documented separately.

## The eight invalidating actions

1. Switching models
2. Changing effort level
3. Turning on fast mode
4. Connecting or disconnecting an MCP server
5. Enabling or disabling a plugin
6. Denying an entire tool
7. Compacting the conversation
8. Upgrading Claude Code

### Switching models

Each model has its own cache. Switching with `/model` (see [model config](https://code.claude.com/docs/en/model-config)) means the next request reads the entire conversation history with no cache hits, even though the content is identical.

The `opusplan` model setting resolves to Opus during plan mode and Sonnet during execution, so each plan-mode toggle is a model switch and starts a fresh cache. Automatic model fallback on Fable 5 is also a model switch: when a safety classifier flags a request, Claude Code re-runs it on the default Opus model and the session continues there.

### Changing effort level

The cache is keyed by effort level as well as model, so switching with `/effort` means the next request reads the entire conversation history with no cache hits. Once a conversation has started, Claude Code shows a confirmation dialog before applying an effort change that would invalidate the cache. A change that resolves to the same level already in effect — such as setting the model's default explicitly — skips the dialog and keeps the cache. (Effort-level detail is owned by [model config](https://code.claude.com/docs/en/model-config).)

### Turning on fast mode

Enabling [fast mode](https://code.claude.com/docs/en/fast-mode) adds a request header that is part of the cache key, so the next request reads the entire conversation history with no cache hits. Those uncached input tokens are billed at fast mode rates, which is why turning it on at the start of a session costs less than turning it on deep into a long one. Enabling fast mode from a non-Opus model also switches your model, which starts a fresh cache on its own.

The cost applies once per conversation. After the first fast mode turn, Claude Code keeps sending the header and varies only the request's speed setting, which is not part of the cache key. Turning fast mode off, the automatic fallback to standard speed after a rate limit, and turning it back on later all keep the cache. `/clear` and `/compact` reset this, since they rebuild the cache at those points anyway. Per the source, keeping the header across toggles requires Claude Code v2.1.86 or later; on earlier versions every fast mode toggle and rate-limit fallback invalidates the cache.

### Connecting or disconnecting an MCP server

Tool definitions sit in the system prompt layer, so the cache invalidates when the set of tool definitions in the request changes between turns. Whether an [MCP server](https://code.claude.com/docs/en/mcp) change does this depends on whether its tools are deferred by tool search or loaded into the prefix:

- **Deferred tools** (the default on supported models): a server connecting, disconnecting, or changing its tool list only appends new content and doesn't disturb anything already cached.
- **Tools loaded into the prefix**: any change to them invalidates the cache. This happens when tool search is unavailable or disabled — such as on Haiku models, on Vertex AI, or with a custom `ANTHROPIC_BASE_URL` gateway — and also for a server or tool marked `alwaysLoad` or kept upfront by threshold-based loading.

When tools load into the prefix, the most common cause of invalidation is a server connecting or disconnecting mid-session, which can happen without any action on your part: a stdio server's process exits, an HTTP session expires, or a server reconnects automatically after a transient failure. A connected server can also push a dynamic tool update that changes its tool list. Toggling the advisor tool is an exception — its definition sits after the cache breakpoint, so enabling or disabling `/advisor` keeps the cached prefix intact. Editing your MCP config does not by itself change the cache; the new config takes effect only after a restart, which is when the server connects or disconnects.

### Enabling or disabling a plugin

[Plugins](https://code.claude.com/docs/en/plugins) bundle several component types, and the cost of a change depends on which components the plugin provides. Skills, commands, agents, hooks, LSP servers, monitors, and themes **never** invalidate the cache: anything they add is appended after the existing conversation, so the next request pays for the new content but still reads everything before it from cache.

The exception is a plugin that provides MCP servers. Enabling or disabling one follows the same rules as connecting or disconnecting an MCP server above: the cache survives when the server's tools are deferred, and the next request re-reads the entire conversation when they load into the prefix. Plugin changes apply when you run `/reload-plugins` or start a new session — the cost shows up on the first turn after the reload, not when you run `/plugin install`, `/plugin enable`, or `/plugin disable`. As of v2.1.163, when a reload would trigger the full re-read, `/reload-plugins` shows a warning and does not apply the reload unless you pass `--force`. Disabling a plugin you enabled earlier in the session restores the previous request shape; if that prefix is still within its cache lifetime, the next request reads the older cache entry instead of rebuilding.

### Denying an entire tool

Adding a bare tool name like `Bash` or `WebFetch` as a [deny rule](https://code.claude.com/docs/en/permissions) removes that tool from Claude's context entirely. Built-in tool definitions load into the system prompt layer, so adding or removing one of these rules mid-session invalidates the cache. The change takes effect on the next turn whether you add it through `/permissions` or by editing a settings file directly.

Only a deny rule that matches in the tool-name position has this effect: a bare tool name, the equivalent `Bash(*)` form, or a tool-name glob like `"*"`. A glob that matches only MCP tools, such as `"mcp__*"`, removes those tools the same way but leaves the cache intact when the matched tools are deferred (the default), since deferred definitions were never in the cached prefix. Scoped deny rules like `Bash(rm *)`, and all allow and ask rules, don't change which tools Claude sees — Claude Code checks them when Claude attempts a call, leaving the prefix intact.

### Compacting the conversation

[Compaction](cc_what_survives_compaction.md) replaces your message history with a summary. By design, this invalidates the conversation layer, since the next request has a new, shorter history that doesn't share a prefix with the old one. Claude Code reuses the system prompt layer and reloads project context from disk, which cache-hits only if CLAUDE.md and memory are unchanged since the session started.

To produce the summary, Claude Code sends a one-off request with the same system prompt, tools, and history as your conversation, plus a summarization instruction appended as a final user message. Because it shares your prefix, that request reads the existing cache rather than reprocessing the full history. Most of compaction's time goes to generating the summary, not to a cache miss — the turn that follows rebuilds the conversation cache only for the much shorter summary, so the post-compaction turn is not the slow part. If you've gone down a path you want to abandon entirely, `/rewind` to an earlier turn instead, since rewinding truncates back to a prefix that is already cached rather than building a new one.

### Upgrading Claude Code

A new Claude Code version typically updates the system prompt or tool definitions, so the first request after an upgrade rebuilds the cache from the top. Auto-update downloads new versions in the background but applies them on the next launch, never mid-session, so you see this as an uncached first turn after restarting rather than a surprise during a session. Set `DISABLE_AUTOUPDATER=1` to control when upgrades apply. Note that resuming a session after an upgrade reprocesses the entire conversation history with no cache hits, since the history now sits behind a different system prompt; the cost scales with how long the resumed conversation is, so the first turn back into a long session can be the most expensive request you send.

**Source**: https://code.claude.com/docs/en/prompt-caching
**Last Updated**: 2026-06-13
**Status**: Active
