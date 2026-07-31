---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - thinking
keywords:
  - openclaw thinking levels
  - /think directive
  - /fast service tier
  - /verbose tool summaries
  - /trace plugin debug
  - /reasoning visibility
  - thinking resolution order
  - resolveThinkingProfile provider profile
  - per-provider thinking mapping
topics:
  - OpenClaw
  - Thinking and Output Directives
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/thinking
access_control_group: ["general"]
---

# OpenClaw — Thinking, Fast, Verbose, Trace & Reasoning Directives

## Overview

This note documents OpenClaw's thinking/output directive system — the `/think`, `/fast`, `/verbose`, `/trace`, and `/reasoning` directives an operator types into a chat body to control an agent's reasoning effort and output shape — mirroring the `tools/thinking` source page. It covers the `/think` level ladder and its per-provider mapping, the 5-layer resolution order, setting/clearing a session default, application by agent backend, the `/fast` service-tier mapping, the `/verbose` tool-summary system, `/trace`, `/reasoning` visibility, heartbeats, the web chat UI selector, and the provider-profile hooks (`resolveThinkingProfile`) that declare per-model level sets. All levels, aliases, defaults, and payload mappings are copied verbatim from source.

## What `/think` does and its level ladder

`/think` is an inline directive that appears in any inbound body as `/t <level>`, `/think:<level>`, or `/thinking <level>`. The levels (with their reasoning aliases) are `off | minimal | low | medium | high | xhigh | adaptive | max`:

- `minimal` → "think"
- `low` → "think hard"
- `medium` → "think harder"
- `high` → "ultrathink" (max budget)
- `xhigh` → "ultrathink+" (GPT-5.2+ and Codex models, plus Anthropic Claude Opus 4.7+ effort)
- `adaptive` → provider-managed adaptive thinking (supported for Claude 4.6 on Anthropic/Bedrock, Anthropic Claude Opus 4.7+, and Google Gemini dynamic thinking)
- `max` → provider max reasoning (Anthropic Claude Opus 4.7+; Ollama maps this to its highest native `think` effort)

The spelling variants `x-high`, `x_high`, `extra-high`, `extra high`, and `extra_high` all map to `xhigh`; `highest` maps to `high`.

## Provider-profile mapping

Thinking menus and pickers are provider-profile driven: provider plugins declare the exact level set for the selected model, including labels such as binary `on`. `adaptive`, `xhigh`, and `max` are only advertised for profiles that support them; a typed directive for an unsupported level is rejected with that model's valid options. Existing stored unsupported levels are remapped by provider-profile rank — `adaptive` falls back to `medium` on non-adaptive models, while `xhigh` and `max` fall back to the largest supported non-off level. The per-provider behavior, copied from source:

- **Anthropic Claude 4.6** models default to `adaptive` when no explicit thinking level is set.
- **Anthropic Claude Opus 4.8 and Opus 4.7** keep thinking off unless you explicitly set a thinking level. Opus 4.8's provider-owned effort default is `high` after adaptive thinking is enabled.
- **Anthropic Claude Opus 4.7+** maps `/think xhigh` to adaptive thinking plus `output_config.effort: "xhigh"` (`/think` is a thinking directive, `xhigh` is the Opus effort setting), and also exposes `/think max`, mapping to the same provider-owned max effort path.
- **Direct DeepSeek V4** expose `/think xhigh|max`; both map to DeepSeek `reasoning_effort: "max"` while lower non-off levels map to `high`.
- **OpenRouter-routed DeepSeek V4** expose `/think xhigh` and send OpenRouter-supported `reasoning_effort` values; stored `max` overrides fall back to `xhigh`.
- **Ollama** thinking-capable models expose `/think low|medium|high|max`; `max` maps to native `think: "high"` because Ollama's native API accepts `low`, `medium`, and `high` effort strings.
- **OpenAI GPT** map `/think` through model-specific Responses API effort support; `/think off` sends `reasoning.effort: "none"` only when the target model supports it, otherwise OpenClaw omits the disabled reasoning payload rather than sending an unsupported value.
- **Custom OpenAI-compatible** catalog entries can opt into `/think xhigh` by setting `models.providers.<provider>.models[].compat.supportedReasoningEfforts` to include `"xhigh"`; this reuses the same compat metadata that maps outbound OpenAI reasoning-effort payloads, so menus, session validation, agent CLI, and `llm-task` agree with transport behavior.
- **Stale OpenRouter Hunter Alpha** refs skip proxy reasoning injection because that retired route could return final answer text through reasoning fields.
- **Google Gemini** maps `/think adaptive` to Gemini's dynamic thinking: Gemini 3 requests omit a fixed `thinkingLevel`, Gemini 2.5 requests send `thinkingBudget: -1`; fixed levels still map to the closest Gemini `thinkingLevel` or budget for that family.
- **MiniMax M2.x** (`minimax/MiniMax-M2*`) on the Anthropic-compatible streaming path defaults to `thinking: { type: "disabled" }` unless thinking is explicitly set in model/request params (avoiding leaked `reasoning_content` deltas from M2.x's non-native Anthropic stream format). **MiniMax-M3** (and M3.x) is exempt: M3 emits proper Anthropic thinking blocks and returns empty content when thinking is disabled, so OpenClaw keeps M3 on the provider's omitted/adaptive thinking path.
- **Z.AI** (`zai/*`) is binary (`on`/`off`) for most GLM models; GLM-5.2 is the exception, exposing `/think off|low|high|max`, mapping `low` and `high` to `reasoning_effort: "high"` and `max` to `reasoning_effort: "max"`.
- **Moonshot Kimi K2.7 Code** (`moonshot/kimi-k2.7-code`) always thinks — its profile exposes only `on`, and OpenClaw omits the outbound `thinking` field as required by Moonshot. Other `moonshot/*` map `/think off` to `thinking: { type: "disabled" }` and any non-`off` level to `thinking: { type: "enabled" }`; when thinking is enabled Moonshot only accepts `tool_choice` `auto|none`, so OpenClaw normalizes incompatible values to `auto`.

## Resolution order

The effective thinking level resolves through five layers, highest precedence first: (1) inline directive on the message (applies only to that message); (2) session override (set by a directive-only message); (3) per-agent default (`agents.list[].thinkingDefault`); (4) global default (`agents.defaults.thinkingDefault`); (5) fallback — the provider-declared default when available, otherwise reasoning-capable models resolve to `medium` (or the nearest supported non-`off` level) and non-reasoning models stay `off`.

## Setting a session default

To set a session default, send a message that is **only** the directive (whitespace allowed), e.g. `/think:medium` or `/t high` — this sticks for the current session (per-sender by default). Use `/think default` to clear the session override and inherit the configured/provider default; the aliases `inherit`, `clear`, `reset`, and `unpin` also work. `/think off` stores an explicit off override that disables thinking until you change or clear the session override. A confirmation reply is sent (`Thinking level set to high.` / `Thinking disabled.`); if the level is invalid (e.g. `/thinking big`) the command is rejected with a hint and session state is left unchanged. Send `/think` (or `/think:`) with no argument to see the current thinking level.

## Application by agent

The resolved level is applied per backend: for **Embedded OpenClaw** it is passed to the in-process agent runtime; for the **Claude CLI backend**, non-off levels are passed to Claude Code as `--effort` when using `claude-cli` (see the CLI backends docs).

## Fast mode (`/fast`)

`/fast` takes levels `on|off|default`. A directive-only message toggles a session fast-mode override and replies `Fast mode enabled.` / `Fast mode disabled.`; `/fast default` clears it and inherits the configured default (aliases `inherit`, `clear`, `reset`, `unpin`). `/fast` (or `/fast status`) with no mode shows the current effective state. Fast mode resolves: (1) inline/directive-only `/fast on|off` (`/fast default` clears this layer); (2) session override; (3) per-agent default (`agents.list[].fastModeDefault`); (4) per-model config `agents.defaults.models["<provider>/<model>"].params.fastMode`; (5) fallback `off`. The provider mappings:

- For `openai/*`, fast mode maps to OpenAI priority processing by sending `service_tier=priority` on supported Responses requests.
- For Codex-backed `openai/*` models, fast mode sends the same `service_tier=priority` flag on Codex Responses; OpenClaw keeps one shared `/fast` toggle across both auth paths.
- For direct public `anthropic/*` requests (including OAuth-authenticated traffic sent to `api.anthropic.com`), fast mode maps to Anthropic service tiers: `/fast on` sets `service_tier=auto`, `/fast off` sets `service_tier=standard_only`.
- For `minimax/*` on the Anthropic-compatible path, `/fast on` (or `params.fastMode: true`) rewrites `MiniMax-M2.7` to `MiniMax-M2.7-highspeed`.

Explicit Anthropic `serviceTier` / `service_tier` model params override the fast-mode default when both are set, and OpenClaw skips Anthropic service-tier injection for non-Anthropic proxy base URLs. `/status` shows `Fast` only when fast mode is enabled.

## Verbose directives (`/verbose` or `/v`)

`/verbose` (alias `/v`) takes levels `on` (minimal) | `full` | `off` (default). A directive-only message toggles session verbose and replies `Verbose logging enabled.` / `Verbose logging disabled.`; invalid levels return a hint without changing state. `/verbose off` stores an explicit session override (clear it via the Sessions UI by choosing `inherit`). Authorized external channel senders may persist the override, while internal gateway/webchat clients need `operator.admin` to persist it. An inline directive affects only that message; session/global defaults apply otherwise; `/verbose` with no argument shows the current level. When verbose is on, agents that emit structured tool results send each tool call back as its own metadata-only message, prefixed with `<emoji> <tool-name>: <arg>` when available — sent as soon as each tool starts (separate bubbles), not as streaming deltas. Tool failure summaries remain visible in normal mode, but raw error-detail suffixes are hidden unless verbose is `full`. When verbose is `full`, tool outputs are also forwarded after completion (separate bubble, truncated to a safe length); toggling `/verbose on|full|off` mid-run makes subsequent tool bubbles honor the new setting. `agents.defaults.toolProgressDetail` controls the shape of these summaries and progress-draft tool lines — use `"explain"` (default) for compact human labels, or `"raw"` to also append the raw command/detail for debugging; per-agent `agents.list[].toolProgressDetail` overrides the default. Example shapes: `explain` → `🛠️ Exec: check JS syntax for /tmp/app.js`; `raw` → `🛠️ Exec: check JS syntax for /tmp/app.js, node --check /tmp/app.js`.

## Plugin trace directives (`/trace`)

`/trace` takes levels `on` | `off` (default). A directive-only message toggles session plugin trace output and replies `Plugin trace enabled.` / `Plugin trace disabled.`. An inline directive affects only that message; session/global defaults apply otherwise; `/trace` with no argument shows the current level. `/trace` is narrower than `/verbose`: it only exposes plugin-owned trace/debug lines such as Active Memory debug summaries. Trace lines can appear in `/status` and as a follow-up diagnostic message after the normal assistant reply.

## Reasoning visibility (`/reasoning`)

`/reasoning` (alias `/reason`) takes levels `on|off|stream`. A directive-only message toggles whether thinking blocks are shown in replies. When enabled, reasoning is sent as a **separate message** prefixed with `Thinking`. The `stream` level streams reasoning while the reply is generating when the active channel supports reasoning previews, then sends the final answer without reasoning. Sending `/reasoning` (or `/reasoning:`) with no argument shows the current level. Resolution order: inline directive, then session override, then per-agent default (`agents.list[].reasoningDefault`), then global default (`agents.defaults.reasoningDefault`), then fallback `off`. Malformed local-model reasoning tags are handled conservatively: closed `<think>...</think>` blocks stay hidden on normal replies, and unclosed reasoning after already-visible text is also hidden; if a reply is fully wrapped in a single unclosed opening tag and would otherwise deliver as empty text, OpenClaw removes the malformed opening tag and delivers the remaining text.

## Heartbeats

The heartbeat probe body is the configured heartbeat prompt (default: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). Inline directives in a heartbeat message apply as usual, but avoid changing session defaults from heartbeats. Heartbeat delivery defaults to the final payload only; to also send the separate `Thinking` message (when available) set `agents.defaults.heartbeat.includeReasoning: true` or per-agent `agents.list[].heartbeat.includeReasoning: true`.

## Web chat UI

The web chat thinking selector mirrors the session's stored level from the inbound session store/config on page load. Picking a level writes the session override immediately via `sessions.patch` — it does not wait for the next send and is not a one-shot `thinkingOnce` override. The first option is always the clear-override choice, showing `Inherited: <resolved level>` (including `Inherited: Off` when inherited thinking is disabled). Explicit picker choices use their direct level labels while preserving provider labels when present (e.g. `Maximum` for a provider-labeled `max` option). The picker uses `thinkingLevels` from the gateway session row/defaults, with `thinkingOptions` kept as a legacy label list; the browser UI keeps no provider regex list, since plugins own model-specific level sets. `/think:<level>` still works and updates the same stored session level, so chat directives and the picker stay in sync.

## Provider profiles

Provider plugins can expose `resolveThinkingProfile(ctx)` to define a model's supported levels and default. Plugins that proxy Claude models should reuse `resolveClaudeThinkingProfile(modelId)` from `openclaw/plugin-sdk/provider-model-shared` so direct Anthropic and proxy catalogs stay aligned. Each profile level has a stored canonical `id` (`off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `adaptive`, or `max`) and may include a display `label`; binary providers use `{ id: "low", label: "on" }`. Profile hooks receive merged catalog facts when available — including `reasoning`, `compat.thinkingFormat`, and `compat.supportedReasoningEfforts` — and should use them to expose binary/custom profiles only when the configured request contract supports the matching payload. Tool plugins validating an explicit thinking override should use `api.runtime.agent.resolveThinkingPolicy({ provider, model })` plus `api.runtime.agent.normalizeThinkingLevel(...)` rather than keeping their own level lists, and can pass `catalog` into `resolveThinkingPolicy` so `compat.supportedReasoningEfforts` opt-ins are reflected in plugin-side validation. The published legacy hooks (`supportsXHighThinking`, `isBinaryThinking`, `resolveDefaultThinkingLevel`) remain as compatibility adapters, but new custom level sets should use `resolveThinkingProfile`. Gateway rows/defaults expose `thinkingLevels`, `thinkingOptions`, and `thinkingDefault` so ACP/chat clients render the same profile ids and labels that runtime validation uses.

**Source**: OpenClaw documentation — `tools/thinking` (mirror `inbox/openclaw_docs/tools/thinking.md`)
**Last Updated**: 2026-06-22
**Status**: Active
