---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - compaction
keywords:
  - openclaw compaction
  - auto-compaction overflow recovery
  - reserveTokens keepRecentTokens
  - pluggable compaction provider
  - pre-compaction memory flush
  - NO_REPLY silent turn
  - compaction chunk tool pairing
  - midTurnPrecheck maxActiveTranscriptBytes
  - compaction troubleshooting checklist
topics:
  - OpenClaw
  - Compaction
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/session-management-compaction
access_control_group: ["general"]
---

# OpenClaw — Compaction Operation, Settings, and Troubleshooting

## Overview

This note is the OpenClaw **compaction procedure**: what compaction persists, the chunk-boundary tool-pairing rules, the two auto-compaction triggers (overflow recovery and threshold maintenance) plus the preflight byte-size and mid-turn precheck guards, the `reserveTokens` / `keepRecentTokens` / `reserveTokensFloor` settings, pluggable compaction providers, the user-visible observability surfaces, the `NO_REPLY` silent-turn convention, the implemented pre-compaction memory flush, and the troubleshooting checklist. It mirrors the compaction half of the `reference/session-management-compaction` source page (the session-store / transcript / lifecycle **data model** that compaction reads and writes lives in the sibling note `oc_reference_session_management_store`). The higher-level concept is owned by `/concepts/compaction`; this page is the runtime operation and config reference.

## Compaction: what it is

Compaction summarizes older conversation into a persisted `compaction` entry in the transcript and keeps recent messages intact. After compaction, future turns see (a) the compaction summary, and (b) messages after `firstKeptEntryId`. AGENTS.md section reinjection after compaction is opt-in via `agents.defaults.compaction.postCompactionSections`; when unset or `[]`, OpenClaw does not append AGENTS.md excerpts on top of the compaction summary. Compaction is **persistent** (unlike session pruning).

## Compaction chunk boundaries and tool pairing

When OpenClaw splits a long transcript into compaction chunks, it keeps assistant tool calls paired with their matching `toolResult` entries. The boundary rules are:

- If the token-share split lands between a tool call and its result, OpenClaw shifts the boundary to the assistant tool-call message instead of separating the pair.
- If a trailing tool-result block would otherwise push the chunk over target, OpenClaw preserves that pending tool block and keeps the unsummarized tail intact.
- Aborted/error tool-call blocks do not hold a pending split open.

## When auto-compaction happens (OpenClaw runtime)

In the embedded OpenClaw agent, auto-compaction triggers in two cases.

**1. Overflow recovery** — the model returns a context overflow error (`request_too_large`, `context length exceeded`, `input exceeds the maximum number of tokens`, `input token count exceeds the maximum number of input tokens`, `input is too long for the model`, `ollama error: context length exceeded`, and similar provider-shaped variants) → compact → retry. When the provider reports the attempted token count, OpenClaw forwards that observed count into overflow recovery compaction; if the provider confirms overflow but does not expose a parseable count, OpenClaw passes a minimally over-budget synthetic count to compaction engines and diagnostics. If overflow recovery still fails, OpenClaw surfaces explicit guidance to the user and preserves the current session mapping instead of silently rotating the session key to a fresh session id — the next step is operator-controlled: retry the message, run `/compact`, or run `/new` when a fresh session is preferred.

**2. Threshold maintenance** — after a successful turn, when `contextTokens > contextWindow - reserveTokens`, where `contextWindow` is the model's context window and `reserveTokens` is headroom reserved for prompts plus the next model output. These are OpenClaw runtime semantics.

OpenClaw can also trigger a **preflight local compaction** before opening the next run when `agents.defaults.compaction.maxActiveTranscriptBytes` is set and the active transcript file reaches that size. This is a file-size guard for local reopen cost, not raw archival: OpenClaw still runs normal semantic compaction, and it requires `truncateAfterCompaction` so the compacted summary can become a new successor transcript.

For embedded OpenClaw runs, `agents.defaults.compaction.midTurnPrecheck.enabled: true` adds an opt-in **tool-loop guard**. After a tool result is appended and before the next model call, OpenClaw estimates the prompt pressure using the same preflight budget logic used at turn start. If the context no longer fits, the guard does not compact inside OpenClaw runtime's `transformContext` hook — it raises a structured mid-turn precheck signal, stops the current prompt submission, and lets the outer run loop use the existing recovery path: truncate oversized tool results when that is enough, or trigger the configured compaction mode and retry. The option is disabled by default and works with both `default` and `safeguard` compaction modes, including provider-backed safeguard compaction. This is independent of `maxActiveTranscriptBytes`: the byte-size guard runs before a turn opens, while mid-turn precheck runs later in the embedded OpenClaw tool loop after new tool results have been appended.

## Compaction settings (`reserveTokens`, `keepRecentTokens`)

OpenClaw runtime's compaction settings live in agent settings:

```json5
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw also enforces a safety floor for embedded runs:

- If `compaction.reserveTokens < reserveTokensFloor`, OpenClaw bumps it. The default floor is `20000` tokens. Set `agents.defaults.compaction.reserveTokensFloor: 0` to disable the floor. If it's already higher, OpenClaw leaves it alone.
- Manual `/compact` honors an explicit `agents.defaults.compaction.keepRecentTokens` and keeps OpenClaw runtime's recent-tail cut point. Without an explicit keep budget, manual compaction remains a hard checkpoint and rebuilt context starts from the new summary.
- Set `agents.defaults.compaction.midTurnPrecheck.enabled: true` to run the optional tool-loop precheck after new tool results and before the next model call. This is a trigger only; summary generation still uses the configured compaction path. It is independent of `maxActiveTranscriptBytes`, which is a turn-start active-transcript byte-size guard.
- Set `agents.defaults.compaction.maxActiveTranscriptBytes` to a byte value or string such as `"20mb"` to run local compaction before a turn when the active transcript gets large. This guard is active only when `truncateAfterCompaction` is also enabled. Leave it unset or set `0` to disable.
- When `agents.defaults.compaction.truncateAfterCompaction` is enabled, OpenClaw rotates the active transcript to a compacted successor JSONL after compaction. Branch/restore checkpoint actions use that compacted successor; legacy pre-compaction checkpoint files remain readable while referenced.

Why these defaults: leave enough headroom for multi-turn "housekeeping" (like memory writes) before compaction becomes unavoidable. Implementation: `applyAgentCompactionSettingsFromConfig()` in `src/agents/agent-settings.ts` (called from embedded-runner turn and compaction setup paths).

## Pluggable compaction providers

Plugins can register a compaction provider via `registerCompactionProvider()` on the plugin API. When `agents.defaults.compaction.provider` is set to a registered provider id, the safeguard extension delegates summarization to that provider instead of the built-in `summarizeInStages` pipeline. The provider rules are:

- `provider`: id of a registered compaction provider plugin. Leave unset for default LLM summarization.
- Setting a `provider` forces `mode: "safeguard"`.
- Providers receive the same compaction instructions and identifier-preservation policy as the built-in path.
- The safeguard still preserves recent-turn and split-turn suffix context after provider output.
- Built-in safeguard summarization re-distills prior summaries with new messages instead of preserving the full previous summary verbatim.
- Safeguard mode enables summary quality audits by default; set `qualityGuard.enabled: false` to skip retry-on-malformed-output behavior.
- If the provider fails or returns an empty result, OpenClaw falls back to built-in LLM summarization automatically.
- Abort/timeout signals are re-thrown (not swallowed) to respect caller cancellation.

Source: `src/plugins/compaction-provider.ts`, `src/agents/agent-hooks/compaction-safeguard.ts`.

## User-visible surfaces

You can observe compaction and session state via: `/status` (in any chat session); `openclaw status` (CLI); `openclaw sessions` / `sessions --json`; Gateway logs (`pnpm gateway:watch` or `openclaw logs --follow`), which emit `embedded run auto-compaction start` plus `complete`; and verbose mode, which prints `🧹 Auto-compaction complete` plus the compaction count.

## Silent housekeeping (`NO_REPLY`)

OpenClaw supports "silent" turns for background tasks where the user should not see intermediate output. The convention is:

- The assistant starts its output with the exact silent token `NO_REPLY` / `no_reply` to indicate "do not deliver a reply to the user".
- OpenClaw strips/suppresses this in the delivery layer.
- Exact silent-token suppression is case-insensitive, so `NO_REPLY` and `no_reply` both count when the whole payload is just the silent token.
- This is for true background/no-delivery turns only; it is not a shortcut for ordinary actionable user requests.

As of `2026.1.10`, OpenClaw also suppresses **draft/typing streaming** when a partial chunk begins with `NO_REPLY`, so silent operations don't leak partial output mid-turn.

## Pre-compaction "memory flush" (implemented)

Goal: before auto-compaction happens, run a silent agentic turn that writes durable state to disk (e.g. `memory/YYYY-MM-DD.md` in the agent workspace) so compaction can't erase critical context. OpenClaw uses the **pre-threshold flush** approach:

1. Monitor session context usage.
2. When it crosses a "soft threshold" (below OpenClaw runtime's compaction threshold), run a silent "write memory now" directive to the agent.
3. Use the exact silent token `NO_REPLY` / `no_reply` so the user sees nothing.

The flush config lives under `agents.defaults.compaction.memoryFlush`:

- `enabled` (default: `true`)
- `model` (optional exact provider/model override for the flush turn, for example `ollama/qwen3:8b`)
- `softThresholdTokens` (default: `4000`)
- `prompt` (user message for the flush turn)
- `systemPrompt` (extra system prompt appended for the flush turn)

Operational notes for the flush:

- The default prompt/system prompt include a `NO_REPLY` hint to suppress delivery.
- When `model` is set, the flush turn uses that model without inheriting the active session fallback chain, so local-only housekeeping does not silently fall back to a paid conversation model.
- The flush runs once per compaction cycle (tracked in `sessions.json`).
- The flush runs only for embedded OpenClaw sessions (CLI backends skip it).
- The flush is skipped when the session workspace is read-only (`workspaceAccess: "ro"` or `"none"`).

OpenClaw also exposes a `session_before_compact` hook in the extension API, but OpenClaw's flush logic lives on the Gateway side today.

## Troubleshooting checklist

- **Session key wrong?** Start with `/concepts/session` and confirm the `sessionKey` in `/status`.
- **Store vs transcript mismatch?** Confirm the Gateway host and the store path from `openclaw status`.
- **Compaction spam?** Check the model context window (too small), the compaction settings (`reserveTokens` too high for the model window can cause earlier compaction), and tool-result bloat (enable/tune session pruning).
- **Silent turns leaking?** Confirm the reply starts with `NO_REPLY` (case-insensitive exact token) and you're on a build that includes the streaming suppression fix.

**Source**: OpenClaw documentation — `reference/session-management-compaction` (mirror `inbox/openclaw_docs/reference/session-management-compaction.md`)
**Last Updated**: 2026-06-22
**Status**: Active
