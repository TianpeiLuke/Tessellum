---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - transcript_hygiene
keywords:
  - openclaw transcript hygiene
  - provider-specific transcript sanitization
  - tool call id sanitization
  - thinking signature cleanup
  - inter-session input provenance
  - bedrock converse empty assistant repair
  - openai responses call_id fc_id pairing
  - session file repair
topics:
  - OpenClaw
  - Transcript Hygiene
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/transcript-hygiene
access_control_group: ["general"]
---

# OpenClaw — Transcript Hygiene (Provider Sanitization Matrix)

## Overview

This note models OpenClaw's **transcript hygiene** contract: the provider-specific sanitization and repair rules applied to a session transcript before a run builds model context, mirroring the `reference/transcript-hygiene` source page. Most fixes are **in-memory** adjustments made to satisfy strict provider requirements; a separate **session-file repair pass** may also rewrite stored JSONL before the session is loaded, but only for malformed lines or persisted turns that are invalid durable records. The note captures the global rules (runtime-context separation, image sanitization, malformed-tool-call dropping, incomplete reasoning-only turn omission, inter-session input provenance), the per-provider behavior matrix, and the historical pre-`2026.1.22` behavior — so it serves as the single source of truth for which repair applies to which provider.

Delivered assistant replies are preserved on disk; provider-specific assistant-prefill stripping happens only while constructing outbound payloads. When a repair occurs, the original file is written to a transient `*.bak-<pid>-<ts>` sibling before the atomic replace and removed once the replace succeeds; the backup is only retained if cleanup itself fails (in which case the path is reported back). The full scope of hygiene includes: runtime-only prompt context staying out of user-visible transcript turns, tool call id sanitization, tool call input validation, tool result pairing repair, turn validation / ordering, thought signature cleanup, thinking signature cleanup, image payload sanitization, blank text-block cleanup before provider replay, incomplete reasoning-only length-turn cleanup before provider replay, user-input provenance tagging (for inter-session routed prompts), and empty assistant error-turn repair for Bedrock Converse replay.

## Global rule: runtime context is not user transcript

Runtime/system context can be added to the model prompt for a turn, but it is not end-user-authored content. OpenClaw keeps a separate transcript-facing prompt body for Gateway replies, queued followups, ACP, CLI, and embedded OpenClaw runs. Stored visible user turns use that transcript body instead of the runtime-enriched prompt. For legacy sessions that already persisted runtime wrappers, Gateway history surfaces apply a **display projection** before returning messages to WebChat, TUI, REST, or SSE clients.

## Where this runs

All transcript hygiene is centralized in the **embedded runner**. Policy selection lives in `src/agents/transcript-policy.ts`, and sanitization/repair application is `sanitizeSessionHistory` in `src/agents/embedded-agent-runner/replay-history.ts`. The policy uses `provider`, `modelApi`, and `modelId` to decide what to apply. Separate from transcript hygiene, session files are repaired (if needed) before load: `repairSessionFileIfNeeded` in `src/agents/session-file-repair.ts`, called from `run/attempt.ts` and `compact.ts` (embedded runner).

## Global rule: image sanitization

Image payloads are always sanitized to prevent provider-side rejection due to size limits (downscale/recompress oversized base64 images). This also helps control image-driven token pressure for vision-capable models — lower max dimensions generally reduce token usage; higher dimensions preserve detail. Implementation: `sanitizeSessionMessagesImages` in `src/agents/embedded-agent-helpers/images.ts` and `sanitizeContentBlocksImages` in `src/agents/tool-images.ts`. Max image side is configurable via `agents.defaults.imageMaxDimensionPx` (default: `1200`). Blank text blocks are removed while this pass walks replay content: assistant turns that become empty are dropped from the replay copy; user and tool-result turns that become empty receive a non-empty omitted-content placeholder.

## Global rule: malformed tool calls

Assistant tool-call blocks that are missing **both** `input` and `arguments` are dropped before model context is built. This prevents provider rejections from partially persisted tool calls (for example, after a rate limit failure). Implementation: `sanitizeToolCallInputs` in `src/agents/session-transcript-repair.ts`, applied in `sanitizeSessionHistory` in `src/agents/embedded-agent-runner/replay-history.ts`.

## Global rule: incomplete reasoning-only turns

Assistant turns that hit the provider output limit with **only** thinking or redacted-thinking content are omitted from the in-memory replay copy. Such turns contain incomplete provider state and may carry a partial thinking signature. Empty length turns remain unchanged, as do length turns with visible text, tool calls, or unknown content blocks. Stored transcripts are not rewritten. Implementation: `normalizeAssistantReplayContent` in `src/agents/embedded-agent-runner/replay-history.ts`.

## Global rule: inter-session input provenance

When an agent sends a prompt into another session via `sessions_send` (including agent-to-agent reply/announce steps), OpenClaw persists the created user turn with `message.provenance.kind = "inter_session"`. OpenClaw also prepends a same-turn `[Inter-session message ... isUser=false]` marker before the routed prompt text so the active model call can distinguish foreign session output from external end-user instructions. This marker includes the source session, channel, and tool when available. The transcript still uses `role: "user"` for provider compatibility, but the visible text and provenance metadata both mark the turn as inter-session data. During context rebuild, OpenClaw applies the same marker to older persisted inter-session user turns that only have provenance metadata.

## Provider matrix (current behavior)

The policy keys on `provider` / `modelApi` / `modelId`; the rules below are the **current** (post-`2026.1.22`) per-provider behavior.

### OpenAI / OpenAI Codex

- Image sanitization only.
- Drop orphaned reasoning signatures (standalone reasoning items without a following content block) for OpenAI Responses/Codex transcripts, and drop replayable OpenAI reasoning after a model route switch.
- Preserve replayable OpenAI Responses reasoning item payloads, including encrypted empty-summary items, so manual/WebSocket replay keeps required `rs_*` state paired with assistant output items.
- Native ChatGPT Codex Responses follows Codex wire parity by replaying prior Responses reasoning/message/function payloads without prior item IDs while preserving session `prompt_cache_key`.
- OpenAI Responses-family replay preserves canonical `call_*|fc_*` same-model reasoning pairs, but deterministically normalizes malformed or overlong `call_id` / function-call item ids before pi-ai payload conversion.
- Tool result pairing repair may move real matched outputs and synthesize Codex-style `aborted` outputs for missing tool calls; missing OpenAI Responses-family tool outputs are synthesized as `aborted` to match Codex replay normalization.
- No turn validation or reordering. No thought signature stripping.

### OpenAI-compatible Chat Completions

- Historical assistant thinking/reasoning blocks are stripped before replay so local and proxy-style OpenAI-compatible servers do not receive prior-turn reasoning fields such as `reasoning` or `reasoning_content`.
- Current same-turn tool-call continuations keep the assistant reasoning block attached to the tool call until the tool result has been replayed.
- Custom/self-hosted model entries with `reasoning: true` preserve replayed reasoning metadata.
- Provider-owned exceptions can opt out when their wire protocol requires replayed reasoning metadata.

### Google (Generative AI / Gemini CLI / Antigravity)

- Tool call id sanitization: strict alphanumeric.
- Tool result pairing repair and synthetic tool results.
- Turn validation (Gemini-style turn alternation).
- Google turn ordering fixup (prepend a tiny user bootstrap if history starts with assistant).
- Antigravity Claude: normalize thinking signatures; drop unsigned thinking blocks.

### Anthropic / Minimax (Anthropic-compatible)

- Tool result pairing repair and synthetic tool results.
- Turn validation (merge consecutive user turns to satisfy strict alternation).
- Trailing assistant prefill turns are stripped from outgoing Anthropic Messages payloads when thinking is enabled, including Cloudflare AI Gateway routes.
- Pre-compaction assistant thinking signatures are stripped before provider replay when a session has been compacted. Thinking signatures are cryptographically bound to the conversation prefix at generation time; after compaction the prefix changes (summarized content is replaced by a compaction summary), so replaying the original signatures causes Anthropic to reject the request with "Invalid signature in thinking block". The thinking text is preserved as an unsigned block and is then handled by the rule below.
- Thinking blocks with missing, empty, or blank replay signatures are stripped before provider conversion. If that empties an assistant turn, OpenClaw keeps turn shape with non-empty omitted-reasoning text.
- Older thinking-only assistant turns that must be stripped are replaced with non-empty omitted-reasoning text so provider adapters do not drop the replay turn.

### Amazon Bedrock (Converse API)

- Empty assistant stream-error turns are repaired to a non-empty fallback text block before replay. Bedrock Converse rejects assistant messages with `content: []`, so persisted assistant turns with `stopReason: "error"` and empty content are also repaired **on disk** before load.
- Assistant stream-error turns that contain only blank text blocks are dropped from the in-memory replay copy instead of replaying an invalid blank block.
- Pre-compaction assistant thinking signatures are stripped before Converse replay when a session has been compacted, for the same reason as Anthropic above.
- Claude thinking blocks with missing, empty, or blank replay signatures are stripped before Converse replay. If that empties an assistant turn, OpenClaw keeps turn shape with non-empty omitted-reasoning text.
- Older thinking-only assistant turns that must be stripped are replaced with non-empty omitted-reasoning text so the Converse replay keeps strict turn shape.
- Replay filters OpenClaw delivery-mirror and gateway-injected assistant turns.
- Image sanitization applies through the global rule.

### Mistral (including model-id based detection)

- Tool call id sanitization: strict9 (alphanumeric length 9).

### OpenRouter Gemini

- Thought signature cleanup: strip non-base64 `thought_signature` values (keep base64).

### OpenRouter Anthropic

- Trailing assistant prefill turns are stripped from verified OpenRouter OpenAI-compatible Anthropic model payloads when reasoning is enabled, matching direct Anthropic and Cloudflare Anthropic replay behavior.

### Everything else

- Image sanitization only.

## Historical behavior (pre-2026.1.22)

Before the `2026.1.22` release, OpenClaw applied multiple layers of transcript hygiene. A **transcript-sanitize extension** ran on every context build and could repair tool use/result pairing and sanitize tool call ids (including a non-strict mode that preserved `_`/`-`). The runner also performed provider-specific sanitization, which duplicated work. Additional mutations occurred outside the provider policy, including stripping `<final>` tags from assistant text before persistence, dropping empty assistant error turns, and trimming assistant content after tool calls. This complexity caused cross-provider regressions (notably `openai-responses` `call_id|fc_id` pairing). The `2026.1.22` cleanup removed the extension, centralized logic in the runner, and made OpenAI **no-touch** beyond image sanitization.

**Source**: OpenClaw documentation — `reference/transcript-hygiene` (mirror `inbox/openclaw_docs/reference/transcript-hygiene.md`)
**Last Updated**: 2026-06-22
**Status**: Active
