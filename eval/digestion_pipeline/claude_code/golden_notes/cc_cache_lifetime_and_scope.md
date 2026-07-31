---
tags:
  - resource
  - documentation
  - claude_code
  - prompt_caching
  - cache_lifetime
keywords:
  - cache lifetime
  - cache scope
  - time to live
  - five-minute ttl
  - one-hour ttl
  - cache warm
  - enable_prompt_caching_1h
  - force_prompt_caching_5m
  - per-machine cache scope
  - worktree cache miss
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

# Claude Code — Cache Lifetime and Scope

## Overview

A Claude Code prompt cache entry does not live forever, and it is not shared by every session. **Cache lifetime** governs *how long* a cached prefix survives between requests — a time-to-live (TTL) that resets on every cache hit and, once it lapses, forces the next turn to recompute the full input. **Cache scope** governs *which* requests can read a given cache entry — in Claude Code the cache is effectively scoped to one machine and one directory, so sessions in different directories build different prefixes and miss each other's cache.

Together these two properties explain two everyday observations: the first turn after stepping away is slow (the TTL lapsed), and a session in a sibling worktree starts cold (different scope). This note documents both; the prefix-matching mechanism the TTL and scope sit on top of is covered in [Prompt Caching Mechanism](cc_prompt_caching_mechanism.md).

## Cache lifetime

Cached prefixes expire after a period of inactivity. Each request that hits the cache resets the timer, so the cache stays warm as long as you keep working. After a long enough gap, the next request recomputes the full input and re-establishes the cache, which is why the first turn back after stepping away can be noticeably slower.

The time to live (TTL) controls how long a gap the cache survives. The API offers two: a five-minute TTL, and a one-hour TTL that keeps the cache warm through longer breaks but bills cache writes at a higher rate. Claude Code picks the TTL for you based on how you authenticate, and you can override it with environment variables.

### On a Claude subscription

On a Claude subscription, Claude Code requests the one-hour TTL automatically. Usage is included in your plan rather than billed per token, so the longer TTL costs you nothing extra and only affects how long your cache stays warm.

If you've gone over your plan's usage limit and Claude Code is drawing on usage credits, you are billed for that usage, so Claude Code automatically drops the TTL to five minutes.

### On an API key or third-party provider

On an API key, Bedrock, Vertex, Foundry, or Claude Platform on AWS, you pay the per-token rates, so the TTL stays at the cheaper five minutes by default. To opt into the one-hour TTL, set `ENABLE_PROMPT_CACHING_1H=1`.

On Bedrock, prompt caching support, minimum cacheable prefix length, and one-hour TTL availability all vary by model. If cache token counts stay at zero, check the supported models, regions, and limits in the Bedrock documentation. (Provider-specific cache location and behavior is covered separately under [Claude Code on the LLM gateway / Bedrock-Vertex](https://code.claude.com/docs/en/llm-gateway).)

### Override the TTL

Set `FORCE_PROMPT_CACHING_5M=1` to force the five-minute TTL regardless of authentication. This is useful when you're debugging cache behavior, comparing the two TTLs, or overriding an `ENABLE_PROMPT_CACHING_1H` set in managed settings.

## Cache scope

In Claude Code, the cache is effectively scoped to one machine and directory. The system prompt embeds the working directory, platform, shell, OS version, and auto-memory paths, so two sessions in different directories build different prefixes and miss each other's cache. That includes worktrees of the same repository, since each worktree has its own working directory.

Sessions you run in parallel in the same directory build matching prefixes and read each other's cache. Sequential sessions share the prefix only when the git status snapshot at startup matches, since the system prompt also captures branch and recent commits.

The underlying API cache is broader. Caches are isolated between organizations, and on some providers, between workspaces within an organization. Within those boundaries, any two requests with the same model and prefix read the same cache. For Agent SDK callers running fleets of automated processes, the per-machine sections of the system prompt can be suppressed so the cache is shared across machines (see [Improve prompt caching across users and machines](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)).

**Source**: https://code.claude.com/docs/en/prompt-caching
**Last Updated**: 2026-06-13
**Status**: Active
