---
tags:
  - resource
  - documentation
  - hermes_agent
  - memory
  - personalization
keywords:
  - memory providers
  - honcho
  - dialectic reasoning
  - two-layer context injection
  - cold warm prompt selection
  - per-peer multi-agent isolation
  - context cadence dialectic cadence
  - observation directional unified
topics:
  - Hermes Agent
  - Memory
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho
access_control_group: ["general"]
---

# Hermes Memory Providers & Honcho

## Overview

A **memory provider** is an external plugin that gives the Hermes agent persistent, cross-session knowledge beyond the built-in `MEMORY.md` / `USER.md` files. Hermes ships 8 such plugins, but **only one** can be active at a time — the built-in memory always runs alongside it, and the external provider is purely additive. **Honcho** is the flagship provider: an AI-native memory backend that does **dialectic reasoning** and deep user modeling, maintaining a running model of who the user is (preferences, communication style, goals, patterns) by reasoning about conversations *after* they happen rather than storing simple key-value facts. This note covers the provider-system model plus the full Honcho provider deep-dive; the other 8 providers are cataloged in [hermes_memory_provider_catalog](hermes_memory_provider_catalog.md).

## The Provider System

### Quick Start

```bash
hermes memory setup      # interactive picker + configuration
hermes memory status     # check what's active
hermes memory off        # disable external provider
```

You can also select the active provider via `hermes plugins` → Provider Plugins → Memory Provider, or set `memory.provider` manually in `~/.hermes/config.yaml`.

### How It Works (6-step lifecycle)

When a memory provider is active, Hermes automatically:

1. **Injects provider context** into the system prompt (what the provider knows)
2. **Prefetches relevant memories** before each turn (background, non-blocking)
3. **Syncs conversation turns** to the provider after each response
4. **Extracts memories on session end** (for providers that support it)
5. **Mirrors built-in memory writes** to the external provider
6. **Adds provider-specific tools** so the agent can search, store, and manage memories

The built-in memory (`MEMORY.md` / `USER.md`) continues to work exactly as before — the external provider is additive.

## Honcho: What It Adds

Honcho ([plastic-labs/honcho](https://github.com/plastic-labs/honcho)) is best for multi-agent systems with cross-session context and user-agent alignment. It requires `pip install honcho-ai` plus an API key from app.honcho.dev (or a self-hosted instance); data lives in Honcho Cloud or self-hosted. Relative to the built-in memory it adds automatic dialectic user profiling, session-summary injection, per-peer multi-agent isolation, directional/unified observation modes, server-side derived **conclusions**, and semantic search over those conclusions.

**Dialectic reasoning**: after each turn (gated by `dialecticCadence`), Honcho analyzes the exchange and derives insights about the user's preferences, habits, and goals. These accumulate, giving a deepening understanding beyond what the user explicitly stated, with multi-pass depth (1–3 passes) and automatic cold/warm prompt selection.

## Architecture

### Two-Layer Context Injection

Every turn (in `hybrid` or `context` mode), Honcho assembles two layers injected into the system prompt:

1. **Base context** — session summary, user representation, user peer card, AI self-representation, and AI identity card. Refreshed on `contextCadence`. The "who is this user" layer.
2. **Dialectic supplement** — LLM-synthesized reasoning about the user's current state and needs. Refreshed on `dialecticCadence`. The "what matters right now" layer.

Both layers are concatenated and truncated to the `contextTokens` budget (if set).

### Cold/Warm Prompt Selection

The dialectic automatically selects between two prompt strategies based on whether base context has been populated:

- **Cold start** (no base context yet): general query — "Who is this person? What are their preferences, goals, and working style?"
- **Warm session** (base context exists): session-scoped query — "Given what's been discussed in this session so far, what context about this user is most relevant?"

### Three Orthogonal Config Knobs

Cost and depth are controlled by three independent knobs:

| Knob | Controls | Default |
|------|----------|---------|
| `contextCadence` | Turns between `context()` API calls (base layer refresh) | `1` |
| `dialecticCadence` | Turns between `peer.chat()` LLM calls (dialectic layer refresh) | `2` (recommended 1–5) |
| `dialecticDepth` | Number of `.chat()` passes per dialectic invocation (1–3) | `1` |

These are orthogonal — e.g. frequent context refresh with infrequent deep dialectic.

### Dialectic Depth (Multi-Pass)

When `dialecticDepth` > 1, each dialectic invocation runs multiple `.chat()` passes: **Pass 0** = cold or warm prompt; **Pass 1** = self-audit (identifies gaps, synthesizes evidence from recent sessions); **Pass 2** = reconciliation (checks contradictions, produces final synthesis). Each pass uses a proportional reasoning level (override per-pass with `dialecticDepthLevels`). Passes bail out early if the prior pass returned strong signal, so depth 3 does not always mean 3 LLM calls.

### Session-Start Prewarm & Query-Adaptive Reasoning

On session init, Honcho fires a background dialectic call at the full configured `dialecticDepth` and hands the result directly to turn 1's context assembly; if prewarm hasn't landed by turn 1, turn 1 falls back to a synchronous bounded-timeout call. The auto-injected dialectic also scales `dialecticReasoningLevel` by query length: +1 level at ≥120 chars, +2 at ≥400, clamped at `reasoningLevelCap` (default `"high"`). Disable with `reasoningHeuristic: false`. Levels: `minimal`, `low`, `medium`, `high`, `max`.

## Recall Modes & Configuration

Honcho is configured in `~/.honcho/config.json` (global) or `$HERMES_HOME/honcho.json` (profile-local); resolution order is `$HERMES_HOME/honcho.json` > `~/.hermes/honcho.json` > `~/.honcho/config.json`.

**Recall mode** (`recallMode`) controls how memory flows into conversations:

- `hybrid` — context auto-injected into the system prompt AND tools available (model decides when to query).
- `context` — auto-injection only, tools hidden.
- `tools` — tools only, no auto-injection; the agent must explicitly call `honcho_reasoning`, `honcho_search`, etc.

**Session strategy** (`sessionStrategy`) controls how Honcho sessions map to your work: `per-session` (fresh session per run, recommended for new users), `per-directory` (one session per working directory, context accumulates), `per-repo` (one per git repo), `global` (single session across all directories).

The full config reference (`contextTokens`, `writeFrequency`, `saveMessages`, `messageMaxChars`, `dialecticMaxChars`, etc.) lives in the [plugin README](https://github.com/NousResearch/hermes-agent/blob/main/plugins/memory/honcho/README.md). A minimal cloud `honcho.json`:

```json
{
  "apiKey": "your-key-from-app.honcho.dev",
  "hosts": {
    "hermes": {
      "enabled": true,
      "aiPeer": "hermes",
      "peerName": "your-name",
      "workspace": "hermes"
    }
  }
}
```

For self-hosted servers, `hermes honcho setup` / `hermes memory setup` ask for a local JWT/bearer token after the base URL (signed with the server's `AUTH_JWT_SECRET`); leave it blank when `AUTH_USE_AUTH=false`. The local token is stored under `hosts.<host>.apiKey`, separate from any cloud `apiKey`.

## Multi-Peer Model & Observation

Honcho models conversations as **peers exchanging messages** — one user peer plus one AI peer per Hermes profile, all sharing a **workspace**. The user peer is global across profiles; each AI peer is its own identity that builds an independent representation/card from its own observations (a `coder` profile stays code-oriented while a `writer` profile stays editorial against the same user).

| Concept | What it is |
|---------|-----------|
| **Workspace** | Shared environment. All profiles under one workspace see the same user identity. |
| **User peer** (`peerName`) | The human. Shared across profiles in the workspace. |
| **AI peer** (`aiPeer`) | One per profile. Host key `hermes` → default; `hermes.<profile>` for others. |

`hermes profile create coder --clone` creates a `hermes.coder` host block with `aiPeer: "coder"`, shared `workspace`, inherited `peerName`/`recallMode`/etc., eagerly creating the AI peer. `hermes honcho sync` backfills host blocks for existing profiles (idempotent).

**Observation (directional vs. unified)** — each peer has two toggles mapping 1:1 to Honcho's `SessionPeerConfig`: `observeMe` (Honcho models this peer from its own messages) and `observeOthers` (this peer observes the other peer's messages, feeding cross-peer reasoning). Two peers × two toggles = four flags; `observationMode` is a shorthand preset:

| Preset | User flags | AI flags | Semantics |
|--------|-----------|----------|-----------|
| `"directional"` (default) | me: on, others: on | me: on, others: on | Full mutual observation; enables cross-peer dialectic. |
| `"unified"` | me: on, others: off | me: off, others: on | Shared-pool — AI observes user only, user peer only self-models. |

Override per-peer with an explicit `observation` block. Server-side toggles set via the Honcho dashboard win over local defaults — synced back at session init.

## Gateway Identity Mapping

These keys only matter on the [gateway](hermes_context_files.md), where users arrive with platform-native runtime IDs (Telegram UID, Discord snowflake, Slack user). CLI/TUI/desktop sessions have no runtime ID and always resolve to `peerName`. The setup wizard skips this step if no gateway is connected; otherwise it asks "who talks to this gateway?" and derives:

| Key | Effect |
|-----|--------|
| `pinUserPeer: true` | Every non-agent gateway user collapses to `peerName`. Checked first, overrides all aliases. |
| `userPeerAliases` | Maps specific runtime IDs to peers (`{"7654321": "alice"}`). Many-to-one; home for routing distinct identities. |
| `runtimePeerPrefix` | Namespaces any unmapped runtime ID (`telegram_7654321`) so same-shaped IDs don't collide. |

The resolver tries keys top-down, first match wins: `pinUserPeer` → `userPeerAliases[id]` → `runtimePeerPrefix + id` → raw runtime ID → `peerName` → session-key fallback. Flipping `pinUserPeer` from `true` to `false` does **not** migrate data — choose the pooled path to keep continuity. (`pinPeerName` is a deprecated legacy alias for `pinUserPeer`.)

## Tools & CLI

When Honcho is the active provider, five tools become available:

| Tool | Purpose |
|------|---------|
| `honcho_profile` | Read or update the peer card (pass `card` to update, omit to read) |
| `honcho_search` | Semantic search over context — raw excerpts, no LLM synthesis |
| `honcho_context` | Full session context — summary, representation, card, recent messages |
| `honcho_reasoning` | Synthesized answer from Honcho's LLM (pass `reasoning_level`) |
| `honcho_conclude` | Create or delete conclusions (`conclusion` to create, `delete_id` to remove, PII only) |

The `hermes honcho` subcommand is **only registered when Honcho is the active memory provider**. Selected commands:

```bash
hermes memory setup honcho    # configure directly (works before activation)
hermes honcho status          # connection status, config, key settings
hermes honcho strategy        # show/set session strategy
hermes honcho mode            # show/set recall mode (hybrid/context/tools)
hermes honcho sync            # sync config to all existing profiles
hermes honcho migrate         # migration guide from openclaw-honcho
```

The legacy `hermes honcho setup` redirects to `hermes memory setup`. **Migrating from `hermes honcho`**: existing config (`honcho.json` or `~/.honcho/config.json`) and server-side data (memories, conclusions, profiles) are preserved — set `memory.provider: honcho` to reactivate; no re-login needed.

**Source**: `inbox/hermes_agent_docs/user-guide/features/memory-providers.md` (§intro/Quick Start/How It Works/Honcho entry), `inbox/hermes_agent_docs/user-guide/features/honcho.md` (all sections) · https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho
**Last Updated**: 2026-06-19
**Status**: Active
