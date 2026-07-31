---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - compaction
keywords:
  - openclaw compaction
  - auto-compaction context overflow
  - manual compaction /compact
  - agents.defaults.compaction config
  - compaction model override
  - identifier preservation policy
  - successor transcripts byte guard
  - pluggable compaction providers
  - compaction vs pruning
topics:
  - OpenClaw
  - Compaction
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/compaction
access_control_group: ["general"]
---

# OpenClaw — Compaction (Summarizing Old Turns to Fit the Context Window)

## Overview

This note is the procedure for **compaction** in OpenClaw: how the gateway summarizes older conversation turns into a compact entry so a chat can keep running once it approaches the model's context window. It mirrors the `concepts/compaction` source page end to end — the three-step mechanism and tool-pair chunk safety, automatic compaction plus its recognized overflow signatures, the manual `/compact` command, the `agents.defaults.compaction.*` configuration knobs (separate model, identifier preservation, active-transcript byte guard, successor transcripts, compaction notices, memory flush), pluggable compaction providers, the compaction-vs-pruning contrast, and the troubleshooting paths. Every context window has a maximum token count; when a conversation nears that limit OpenClaw compacts older messages into a summary so the chat can continue.

## How it works

Compaction proceeds in three steps: (1) older conversation turns are summarized into a compact entry; (2) the summary is saved in the session transcript; (3) recent messages are kept intact. When OpenClaw splits history into compaction chunks, it keeps assistant tool calls paired with their matching `toolResult` entries — if a split point lands inside a tool block, OpenClaw moves the boundary so the pair stays together and the current unsummarized tail is preserved. The full conversation history stays on disk; compaction only changes what the model sees on the next turn.

## Auto-compaction

Auto-compaction is on by default. It runs when the session nears the context limit, or when the model returns a context-overflow error (in which case OpenClaw compacts and retries). You will see `embedded run auto-compaction start` / `complete` in normal Gateway logs, `🧹 Auto-compaction complete` in verbose mode, and `/status` showing `🧹 Compactions: <count>`. Before compacting, OpenClaw automatically reminds the agent to save important notes to memory files, which prevents context loss.

OpenClaw detects context overflow from these provider error patterns (recognized overflow signatures):

- `request_too_large`
- `context length exceeded`
- `input exceeds the maximum number of tokens`
- `input token count exceeds the maximum number of input tokens`
- `input is too long for the model`
- `ollama error: context length exceeded`

## Manual compaction

Type `/compact` in any chat to force a compaction. Add instructions to guide the summary, for example `/compact Focus on the API design decisions`. When `agents.defaults.compaction.keepRecentTokens` is set, manual compaction honors that OpenClaw cut-point and keeps the recent tail in rebuilt context; without an explicit keep budget, manual compaction behaves as a hard checkpoint and continues from the new summary alone.

## Configuration

Configure compaction under `agents.defaults.compaction` in your `openclaw.json`. The most common knobs are below; for the full reference (reserve tokens, identifier preservation, custom context engines, OpenAI server-side compaction), see the Session management deep dive.

### Using a different model

By default, compaction uses the agent's primary model. Set `agents.defaults.compaction.model` to delegate summarization to a more capable or specialized model. The override accepts a `provider/model-id` string or a bare alias configured under `agents.defaults.models`:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "openrouter/anthropic/claude-sonnet-4-6"
      }
    }
  }
}
```

Bare configured aliases resolve to their canonical provider and model before compaction starts. If a bare value matches both an alias and a configured literal model ID, the literal model ID wins; an unmatched bare value remains a model ID on the active provider. This works with local models too — for example a second Ollama model dedicated to summarization, `"model": "ollama/llama3.1:8b"`. When unset, compaction starts with the active session model. If summarization fails with a model-fallback-eligible provider error, OpenClaw retries that compaction attempt through the session's existing model fallback chain; the fallback choice is temporary and is not written back to session state, and an explicit `agents.defaults.compaction.model` override remains exact and does not inherit the session fallback chain.

### Identifier preservation

Compaction summarization preserves opaque identifiers by default (`identifierPolicy: "strict"`). Override with `identifierPolicy: "off"` to disable, or `identifierPolicy: "custom"` plus `identifierInstructions` for custom guidance.

### Active transcript byte guard

When `agents.defaults.compaction.maxActiveTranscriptBytes` is set, OpenClaw triggers normal local compaction before a run if the active JSONL reaches that size. This is useful for long-running sessions where provider-side context management may keep model context healthy while the local transcript keeps growing. It does not split raw JSONL bytes; it asks the normal compaction pipeline to create a semantic summary. The byte guard requires `truncateAfterCompaction: true` — without transcript rotation, the active file would not shrink and the guard remains inactive.

### Successor transcripts

When `agents.defaults.compaction.truncateAfterCompaction` is enabled, OpenClaw does not rewrite the existing transcript in place. It creates a new active successor transcript from the compaction summary, preserved state, and unsummarized tail, then records checkpoint metadata that points branch/restore flows at that compacted successor. Successor transcripts also drop exact duplicate long user turns that arrive inside a short retry window, so channel retry storms are not carried into the next active transcript after compaction. OpenClaw no longer writes separate `.checkpoint.*.jsonl` copies for new compactions; existing legacy checkpoint files can still be used while referenced and are pruned by normal session cleanup.

### Compaction notices

By default, compaction runs silently. Set `notifyUser` to show brief status messages when compaction starts and completes:

```json5
{
  agents: {
    defaults: {
      compaction: {
        notifyUser: true,
      },
    },
  },
}
```

### Memory flush

Before compaction, OpenClaw can run a **silent memory flush** turn to store durable notes to disk. Set `agents.defaults.compaction.memoryFlush.model` when this housekeeping turn should use a local model instead of the active conversation model:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "model": "ollama/qwen3:8b"
        }
      }
    }
  }
}
```

The memory-flush model override is exact and does not inherit the active session fallback chain. See the Memory page for details and config.

## Pluggable compaction providers

Plugins can register a custom compaction provider via `registerCompactionProvider()` on the plugin API. When a provider is registered and configured, OpenClaw delegates summarization to it instead of the built-in LLM pipeline. To use a registered provider, set its id in your config:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "provider": "my-provider"
      }
    }
  }
}
```

Setting a `provider` automatically forces `mode: "safeguard"`. Providers receive the same compaction instructions and identifier-preservation policy as the built-in path, and OpenClaw still preserves recent-turn and split-turn suffix context after provider output. If the provider fails or returns an empty result, OpenClaw falls back to built-in LLM summarization.

## Compaction vs pruning

|                  | Compaction                    | Pruning                          |
| ---------------- | ----------------------------- | -------------------------------- |
| **What it does** | Summarizes older conversation | Trims old tool results           |
| **Saved?**       | Yes (in session transcript)   | No (in-memory only, per request) |
| **Scope**        | Entire conversation           | Tool results only                |

Session pruning is a lighter-weight complement that trims tool output without summarizing.

## Troubleshooting

**Compacting too often?** The model's context window may be small, or tool outputs may be large — try enabling session pruning. **Context feels stale after compaction?** Use `/compact Focus on <topic>` to guide the summary, or enable the memory flush so notes survive. **Need a clean slate?** `/new` starts a fresh session without compacting. For advanced configuration (reserve tokens, identifier preservation, custom context engines, OpenAI server-side compaction), see the Session management deep dive.

**Source**: OpenClaw documentation — `concepts/compaction` (mirror `inbox/openclaw_docs/concepts/compaction.md`)
**Last Updated**: 2026-06-22
**Status**: Active
