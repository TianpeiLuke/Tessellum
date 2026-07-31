---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - token_use
keywords:
  - openclaw token use
  - context window accounting
  - system prompt assembly
  - prompt caching cache ttl
  - status usage cost estimation
  - bootstrap max chars
  - tool result max chars
  - anthropic 1m context
topics:
  - OpenClaw
  - Token Use and Costs
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/reference/token-use
access_control_group: ["general"]
---

# OpenClaw — Token Use and Costs

## Overview

This note explains the OpenClaw token-accounting **concept**: how the gateway builds its system prompt on every run, what counts toward the model context window, how to read live token usage and estimated cost (`/status`, `/usage`, `openclaw status --usage`), how cost is estimated from per-model pricing config, and how cache-TTL pruning plus heartbeat cache-warming reduce token pressure (including Anthropic 1M context sizing). It mirrors the `reference/token-use` source page. OpenClaw tracks **tokens, not characters**; tokens are model-specific, but most OpenAI-style models average **~4 characters per token** for English text.

## How the system prompt is built

OpenClaw assembles its own system prompt on every run. The prompt includes the tool list plus short descriptions; the skills list (metadata only — instructions are loaded on demand with `read`); self-update instructions; workspace + bootstrap files; time (UTC + user timezone); reply tags + heartbeat behavior; and runtime metadata (host/OS/model/thinking). For native Codex turns the compact skills block is delivered as turn-scoped collaboration developer instructions; other harnesses receive it in the normal prompt surface. The skills block is bounded by `skills.limits.maxSkillsPromptChars`, with an optional per-agent override at `agents.list[].skillsLimits.maxSkillsPromptChars`.

The bootstrap/workspace files injected are `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` (when new), plus `MEMORY.md` when present. Native Codex turns do not paste raw `MEMORY.md` from the configured agent workspace when memory tools are available for that workspace; instead they include a small memory pointer in turn-scoped collaboration developer instructions and use memory tools on demand. If tools are disabled, memory search is unavailable, or the active workspace differs from the agent memory workspace, `MEMORY.md` falls back to the normal bounded turn-context path. Lowercase root `memory.md` is not injected — it is legacy repair input for `openclaw doctor --fix` when paired with `MEMORY.md`.

Large injected files are truncated by `agents.defaults.bootstrapMaxChars` (default: `20000`), and total bootstrap injection is capped by `agents.defaults.bootstrapTotalMaxChars` (default: `60000`). The `memory/*.md` daily files are not part of the normal bootstrap prompt; they remain on-demand via memory tools on ordinary turns, but reset/startup model runs can prepend a one-shot startup-context block with recent daily memory for that first turn. Bare chat `/new` and `/reset` commands are acknowledged without invoking the model. The startup prelude is controlled by `agents.defaults.startupContext`, and post-compaction `AGENTS.md` excerpts are separate, requiring explicit `agents.defaults.compaction.postCompactionSections` opt-in. The full breakdown lives in the System Prompt concepts page; when documenting credentials or auth snippets, the Secret Placeholder Conventions reference avoids secret-scanner false positives in docs-only changes.

## What counts in the context window

Everything the model receives counts toward the context limit: the system prompt (all sections above), conversation history (user + assistant messages), tool calls and tool results, attachments/transcripts (images, audio, files), compaction summaries and pruning artifacts, and provider wrappers or safety headers (not visible, but still counted). Some runtime-heavy surfaces have their own explicit caps under `agents.defaults.contextLimits`: `memoryGetMaxChars`, `memoryGetDefaultLines`, `toolResultMaxChars`, and `postCompactionMaxChars`. Per-agent overrides live under `agents.list[].contextLimits`. These knobs are for bounded runtime excerpts and injected runtime-owned blocks, and are separate from bootstrap limits, startup-context limits, and skills prompt limits.

`toolResultMaxChars` is an advanced ceiling. When it is unset, OpenClaw chooses the live tool-result cap from the effective model context window: `16000` chars below 100K tokens, `32000` chars at 100K+ tokens, and `64000` chars at 200K+ tokens — still bounded by the runtime context-share guard. For images, OpenClaw downscales transcript/tool image payloads before provider calls; `agents.defaults.imageMaxDimensionPx` (default: `1200`) tunes this — lower values usually reduce vision-token usage and payload size, while higher values preserve more visual detail for OCR/UI-heavy screenshots. For a practical per-injected-file breakdown (tools, skills, and system prompt size), use `/context list` or `/context detail` (see the Context concepts page).

## How to see current token usage

Three in-chat surfaces report usage. `/status` shows an **emoji-rich status card** with the session model, context usage, last response input/output tokens, and **estimated cost** when local pricing is configured for the active model. `/usage off|tokens|full` appends a **per-response usage footer** to every reply — it persists per session (stored as `responseUsage`), and `/usage full` shows estimated cost only when OpenClaw has usage metadata and local pricing for the active model (otherwise tokens only). `/usage cost` shows a local cost summary from OpenClaw session logs. Other surfaces: the TUI/Web TUI support `/status` + `/usage`; the CLI `openclaw status --usage` and `openclaw channels list` show normalized provider quota windows (`X% left`, not per-response costs). Current usage-window providers are Anthropic, GitHub Copilot, Gemini CLI, OpenAI Codex, MiniMax, Xiaomi, and z.ai.

Usage surfaces normalize common provider-native field aliases before display. For OpenAI-family Responses traffic that includes both `input_tokens` / `output_tokens` and `prompt_tokens` / `completion_tokens`, so transport-specific field names do not change `/status`, `/usage`, or session summaries. Gemini CLI usage is normalized too: the default `stream-json` parser reads assistant `message` events, and `stats.cached` maps to `cacheRead` with `stats.input_tokens - stats.cached` used when the CLI omits an explicit `stats.input` field (legacy JSON overrides still read reply text from `response`). For native OpenAI-family Responses traffic, WebSocket/SSE usage aliases are normalized the same way, and totals fall back to normalized input + output when `total_tokens` is missing or `0`.

When the current session snapshot is sparse, `/status` and `session_status` can recover token/cache counters and the active runtime model label from the most recent transcript usage log; existing nonzero live values still take precedence over transcript fallback values, and larger prompt-oriented transcript totals can win when stored totals are missing or smaller. Usage auth for provider quota windows comes from provider-specific hooks when available; otherwise OpenClaw falls back to matching OAuth/API-key credentials from auth profiles, env, or config. Assistant transcript entries persist the same normalized usage shape, including `usage.cost` when the active model has pricing configured and the provider returns usage metadata, giving `/usage cost` and transcript-backed session status a stable source even after live runtime state is gone. OpenClaw keeps provider usage accounting separate from the current context snapshot: provider `usage.total` can include cached input, output, and multiple tool-loop model calls (useful for cost/telemetry but it can overstate the live context window), so context displays and diagnostics use the latest prompt snapshot (`promptTokens`, or the last model call when no prompt snapshot is available) for `context.used`.

## Cost estimation (when shown)

Costs are estimated from your model pricing config at `models.providers.<provider>.models[].cost`:

```
models.providers.<provider>.models[].cost
```

These are **USD per 1M tokens** for `input`, `output`, `cacheRead`, and `cacheWrite`. If pricing is missing, OpenClaw shows tokens only. Cost display is not limited to API-key auth: non-API-key providers such as `aws-sdk` can show estimated cost when their configured model entry includes local pricing and the provider returns usage metadata. After sidecars and channels reach the Gateway ready path, OpenClaw starts an optional background pricing bootstrap for configured model refs that do not already have local pricing — that bootstrap fetches remote **OpenRouter** and **LiteLLM** pricing catalogs. Set `models.pricing.enabled: false` to skip those catalog fetches on offline or restricted networks; explicit `models.providers.*.models[].cost` entries continue to drive local cost estimates.

## Cache TTL and pruning impact

Provider prompt caching only applies within the cache TTL window. OpenClaw can optionally run **cache-ttl pruning**: it prunes the session once the cache TTL has expired, then resets the cache window so subsequent requests re-use the freshly cached context instead of re-caching the full history — keeping cache write costs lower when a session goes idle past the TTL. It is configured in Gateway configuration with behavior details in the Session pruning concepts page. Heartbeat can keep the cache **warm** across idle gaps: if the model cache TTL is `1h`, setting the heartbeat interval just under that (e.g., `55m`) can avoid re-caching the full prompt, reducing cache write costs. In multi-agent setups you can keep one shared model config and tune cache behavior per agent with `agents.list[].params.cacheRetention`. For Anthropic API pricing, cache reads are significantly cheaper than input tokens, while cache writes are billed at a higher multiplier (see Anthropic's prompt caching pricing for the latest rates and TTL multipliers).

### Example: keep 1h cache warm with heartbeat

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

### Example: mixed traffic with per-agent cache strategy

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long" # default baseline for most agents
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m" # keep long cache warm for deep sessions
    - id: "alerts"
      params:
        cacheRetention: "none" # avoid cache writes for bursty notifications
```

`agents.list[].params` merges on top of the selected model's `params`, so you can override only `cacheRetention` and inherit other model defaults unchanged.

### Anthropic 1M context

OpenClaw sizes GA-capable Claude 4.x models such as Opus 4.8, Opus 4.7, Opus 4.6, and Sonnet 4.6 with Anthropic's 1M context window. You do not need `params.context1m: true` for those models:

```yaml
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        alias: opus
```

Older configs can keep `context1m: true`, but OpenClaw no longer sends Anthropic's retired `context-1m-2025-08-07` beta header for this setting and does not expand unsupported older Claude models to 1M. Requirement: the credential must be eligible for long-context usage — if not, Anthropic responds with a provider-side rate limit error for that request. If you authenticate Anthropic with OAuth/subscription tokens (`sk-ant-oat-*`), OpenClaw preserves the OAuth-required Anthropic beta headers while stripping the retired `context-1m-*` beta if it remains in older config.

## Tips for reducing token pressure

Use `/compact` to summarize long sessions; trim large tool outputs in your workflows; lower `agents.defaults.imageMaxDimensionPx` for screenshot-heavy sessions; keep skill descriptions short (the skill list is injected into the prompt); and prefer smaller models for verbose, exploratory work. The Skills tools page documents the exact skill-list overhead formula.

**Source**: OpenClaw documentation — `reference/token-use` (mirror `inbox/openclaw_docs/reference/token-use.md`)
**Last Updated**: 2026-06-22
**Status**: Active
