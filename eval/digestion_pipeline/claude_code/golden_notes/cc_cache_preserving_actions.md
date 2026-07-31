---
tags:
  - resource
  - documentation
  - claude_code
  - prompt_caching
  - cache_preservation
keywords:
  - cache-preserving actions
  - append to conversation
  - edit claude.md mid-session
  - change output style
  - permission mode cache-safe
  - rewind cache hit
  - subagents and the cache
  - cache_read_input_tokens
  - disable prompt caching
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

# Claude Code — Actions That Keep the Cache

## Overview

This note documents the actions that **keep Claude Code's prompt cache intact** — the inverse-list companion to [cache invalidation](cc_cache_invalidation_actions.md). These actions either append to the end of the conversation or don't touch the request at all, so the cached prefix (system prompt + project context + prior conversation) stays valid and the next turn reads from cache. Some of these same actions — editing CLAUDE.md, changing output style — are *also* why certain settings wait for a restart to apply: the content is read once at session start, so a mid-session edit neither invalidates the cache nor takes effect.

It also covers how subagents relate to the cache (a subagent builds its own; a fork inherits the parent's), the two token fields that measure cache performance, and the environment variables that disable caching for debugging.

## Actions that keep the cache

These actions append to the conversation (which leaves the system prompt and project-context prefix cached) or don't change the request text at all:

- **Editing files in your repository** — file contents enter context only when Claude reads them, and reads append to the conversation. Editing a file Claude previously read does not retroactively change the earlier read in history; instead Claude Code appends a `<system-reminder>` noting the file changed, and Claude re-reads it if needed.
- **Editing CLAUDE.md mid-session** — your project-root and user-level CLAUDE.md files are read once at session start and held in memory. Editing them mid-session does not invalidate the cache, but the edit also **doesn't apply** — Claude keeps working with the version loaded at session start, and the new content loads on the next `/clear`, `/compact`, or restart. Nested CLAUDE.md files in subdirectories and rules with `paths:` frontmatter load later (when Claude first reads a matching file), so editing one *before* it loads does take effect; after it loads, a mid-session edit doesn't retroactively change it.
- **Changing output style** — output style is part of the system prompt, read once at session start. Changing it via `/config` or the `outputStyle` setting mid-session does not invalidate the cache, but the change also **doesn't apply** until the next `/clear` or restart.
- **Changing permission mode** — switching between permission modes (e.g. from default to accept edits) does not change the system prompt or tool definitions, so mode changes are cache-safe. The exception is plan mode with the `opusplan` model setting, which switches the model between Opus and Sonnet on entering/leaving plan mode, making that toggle a model switch (which does invalidate the cache).
- **Invoking skills and commands** — skills and commands inject their instructions as user messages at the point of invocation; nothing earlier in the conversation changes.
- **Running `/recap`** — `/recap` generates a summary for display in the terminal. Unlike `/compact`, it appends the summary as command output rather than replacing the message history, so the cached prefix stays intact.
- **Rewinding the conversation** — `/rewind` truncates the conversation back to an earlier turn. The remaining history is the same content the cache was built from at that point, and the system prompt and project-context layers are unchanged, so the next request hits the earlier cache entry. Every turn since then has read through that prefix, which kept the entry warm even if the original turn was longer ago than the TTL. Restoring file checkpoints alongside the conversation has no separate effect on the cache (file contents enter context only when Claude reads them, the same as editing files).

## Subagents and the cache

A **subagent** starts its own conversation with its own system prompt and tool set, separate from the parent's. It builds its own cache — starting with no cache hits on its first call and warming up across its own turns. Subagents use the five-minute TTL even on a subscription, since the automatic one-hour TTL applies to the main conversation.

The parent's cache is unaffected: from the parent's side, the subagent's call and result append to the conversation, leaving the parent's prefix intact.

A **fork**, by contrast, inherits the parent's system prompt, tools, and conversation history exactly, so its first request reads the parent's cache. (The compaction summarization call uses the same prefix-sharing approach.)

## Check cache performance

Cache performance shows up as two token counts the API reports on every response. The most direct way to watch them live is a statusline script that reads the `current_usage` object:

| Field | Meaning |
| --- | --- |
| `cache_creation_input_tokens` | Tokens written to the cache on this turn, billed at the cache write rate |
| `cache_read_input_tokens` | Tokens served from cache on this turn, billed at roughly 10% of the standard input rate |

A high read-to-creation ratio means caching is working well. If creation stays high turn after turn, something is changing in your prefix — the [actions that invalidate the cache](cc_cache_invalidation_actions.md) are the usual causes. For visibility across an organization, the OpenTelemetry exporter reports cache read and creation tokens per user and session.

## Disable prompt caching

Disabling caching is occasionally useful when debugging caching behavior with a specific model or provider. To turn it off, set one of these environment variables to `1`: `DISABLE_PROMPT_CACHING` (all models), or the per-model variants `DISABLE_PROMPT_CACHING_HAIKU`, `DISABLE_PROMPT_CACHING_SONNET`, `DISABLE_PROMPT_CACHING_OPUS`, and `DISABLE_PROMPT_CACHING_FABLE`. To set caching policy across an organization, put any of these (or the TTL variables) in the `env` block of managed settings. For normal use, leave caching enabled.

**Source**: https://code.claude.com/docs/en/prompt-caching
**Last Updated**: 2026-06-13
**Status**: Active
