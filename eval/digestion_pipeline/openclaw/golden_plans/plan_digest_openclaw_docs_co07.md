---
title: Sub-Plan co07 — OpenClaw Docs: Concepts (soul, streaming, system-prompt, timezone, typebox, typing-indicators, usage-tracking)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/soul", "concepts/streaming", "concepts/system-prompt", "concepts/timezone", "concepts/typebox", "concepts/typing-indicators", "concepts/usage-tracking"]
---

# Sub-Plan co07: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create, the 9-GATE,
> cross-references, undigested-terms ownership, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited
> from the master; this file re-measures its 7 assigned pages from the local mirror and locks the per-note plan.

## Scope

The seven "concepts" leaf pages that document OpenClaw's **agent-personality / prompt / runtime-presentation
surfaces**: the `SOUL.md` personality file (`soul`), outbound streaming + chunking behavior (`streaming`), how the
system prompt is assembled and what it contains (`system-prompt`), timezone handling across envelopes/tool/prompt
(`timezone`), the TypeBox-defined Gateway WebSocket protocol + codegen (`typebox`), typing-indicator config
(`typing-indicators`), and provider usage/quota tracking + the usage-bar template (`usage-tracking`). **Priority P1
(Phase A)** — these establish prompt/streaming/protocol/usage vocabulary that the CLI, gateway, channels, and
providers sub-plans reference. Code-side counterparts (`repo_openclaw`, `_gateway`, `_agents`, `_channels`,
`_channels_messaging`, `_sessions`, `_extensions_llm_providers`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 8,264 measured words. **Planned: 8 notes** (typebox splits 1→2).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| soul | concepts/soul | 628 | 1 | 6 | 0 | concept |
| streaming | concepts/streaming | 1,957 | 3 | 7 | 4 | concept |
| system-prompt | concepts/system-prompt | 2,390 | 1 | 8 | 0 | concept |
| timezone | concepts/timezone | 390 | 1 | 4 | 0 | concept |
| typebox | concepts/typebox | 1,108 | 13 | 13 | 0 | model (protocol) + procedure (codegen) — **SPLIT** |
| typing-indicators | concepts/typing-indicators | 405 | 2 | 5 | 0 | procedure |
| usage-tracking | concepts/usage-tracking | 1,386 | 4 | 5 | 5 | concept (surfaces + usage-bar template model) |

**Total: 8,264 words, 25 code blocks, 48 H2, 9 H3.**

## Content Strategy

- **Prioritize**: the system-prompt assembly contract (every agent run depends on it; the most-referenced page),
  the streaming/chunking + preview-streaming behavior (channel delivery semantics), and the TypeBox Gateway-protocol
  frame model (the WS contract the CLI/SDK/macOS app all consume).
- **Split**: `typebox.md` (1,108w but **13 code blocks**, far over the ≤6 cap, and mixes a *protocol frame model*
  with a *codegen/add-a-method procedure*) → **note 5 (model: protocol frames/schemas)** + **note 6 (procedure: codegen
  pipeline + add-a-method-end-to-end workflow)**. No other page splits: all are single-BB and ≤2,500w / ≤6 code after
  selective snippet inclusion.
- **Link-out, do not duplicate**: provider auth/credential mechanics → providers sub-plans (`pr01`–`pr09`); `gateway`
  tool / config (`config.schema.lookup`, `config.patch`) → gateway sub-plans (`gw01`–`gw07`); Date & Time full
  reference → top-level `date-time` (`rt02`); message lifecycle / progress drafts / retry / presence / context-engine
  → sibling concepts sub-plans (`co01`–`co06`); SOUL/templates starter → reference templates (`rf04`). Terms
  (`term_websocket`, `term_json_rpc`, `term_llm`, `term_claude`, `term_oauth_token`, `term_prompt_caching`, …) are
  LINKED, never redefined inline.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_soul.md` | concept | soul.md: all (What belongs in SOUL.md, Why this works, The Molty prompt, What good looks like, One warning) | 450 | The `SOUL.md` personality file: what voice/tone/opinion/brevity content belongs (vs what does not), why a high-priority instruction layer works, the Molty rewrite prompt, and the SOUL-vs-AGENTS boundary. |
| 2 | `oc_concepts_streaming.md` | concept | streaming.md: Block streaming, Media delivery, Chunking algorithm, Coalescing, Human-like pacing, "Stream chunks or everything", Preview streaming modes (+ channel mapping, runtime behavior, tool-progress) | 700 | OpenClaw's two outbound streaming layers — block streaming (channel messages) and preview streaming (Telegram/Discord/Slack/etc.) — chunking bounds, coalescing, human-like pacing, per-channel mode mapping, and tool-progress preview updates. |
| 3 | `oc_concepts_system_prompt.md` | concept | system-prompt.md: assembly layers, Structure, Prompt modes, Prompt snapshots, Workspace bootstrap injection, Time handling, Skills, Documentation | 750 | How OpenClaw assembles its OpenClaw-owned system prompt: the 3-layer renderer, fixed sections + cache boundary, prompt modes (full/minimal/none), workspace bootstrap file injection + limits, skills list injection, and the documentation section. |
| 4 | `oc_concepts_timezone.md` | concept | timezone.md: Three timezone surfaces, Setting the user timezone, When to override | 350 | The three OpenClaw timezone surfaces — message envelopes, tool payloads, and the cache-stable system-prompt time-zone block — plus how to set `userTimezone`/`envelopeTimezone` and when to override (UTC, fixed IANA zone, timestamp off). |
| 5 | `oc_concepts_typebox_protocol.md` | model | typebox.md: intro, Mental model (req/res/event frames + connection flow), Common methods + events, Where schemas live, Runtime use, Example frames, Swift codegen behavior, Versioning, Schema patterns/conventions | 650 | The TypeBox-defined Gateway WebSocket protocol as a data model: the three frame types (req/res/event), the connect handshake, method/event inventory, AJV runtime validation, generated JSON-Schema/Swift models, version negotiation, and schema conventions. |
| 6 | `oc_concepts_typebox_codegen.md` | procedure | typebox.md: Current pipeline (`protocol:gen`/`:swift`/`:check`), Worked example: add a method end-to-end (schema → validation → handler → register → regenerate → tests/docs), When you change schemas | 500 | The TypeBox protocol codegen workflow: the `pnpm protocol:gen`/`gen:swift`/`check` pipeline, the end-to-end "add a `system.echo` method" procedure (schema, AJV validator, handler, registration, scope, regenerate), and the schema-change checklist. |
| 7 | `oc_concepts_typing_indicators.md` | procedure | typing-indicators.md: Defaults, Modes, Configuration, Notes | 400 | Tuning OpenClaw typing indicators: the legacy default behavior, the four `typingMode` modes (`never`/`message`/`thinking`/`instant`) ordered by how early they fire, agent vs session config, `typingIntervalSeconds` cadence, and heartbeat-typing rules. |
| 8 | `oc_concepts_usage_tracking.md` | concept | usage-tracking.md: What it is, Where it shows up, Custom `/usage full` footer (Shape, Contract Paths, Verbs, Piece forms, Example), Providers + credentials | 700 | OpenClaw usage tracking: provider-reported quota/`X% left` windows, the surfaces it appears on (`/status`, `/usage`, CLI, menu bar), the `messages.usageTemplate` usage-bar template (schema/scales/aliases/contract-paths/verbs/pieces), and per-provider credential requirements. |

## Section Coverage Map

```
soul.md
├── (intro: SOUL.md is your agent's voice) ─────────── → note 1 (oc_concepts_soul)
├── What belongs in SOUL.md ────────────────────────── → note 1
├── Why this works (OpenAI prompt guidance refs) ───── → note 1
├── The Molty prompt ───────────────────────────────── → note 1 (the 1 md code block)
├── What good looks like ───────────────────────────── → note 1
└── One warning (SOUL vs AGENTS boundary) ──────────── → note 1
streaming.md
├── (intro: two streaming layers) ──────────────────── → note 2 (oc_concepts_streaming)
├── Block streaming (channel messages) [+ Media delivery H3] → note 2 (1 ascii code block)
├── Chunking algorithm (low/high bounds) ───────────── → note 2
├── Coalescing (merge streamed blocks) ─────────────── → note 2
├── Human-like pacing between blocks ───────────────── → note 2
├── "Stream chunks or everything" ──────────────────── → note 2
└── Preview streaming modes [Channel mapping, Runtime behavior,
    Tool-progress preview updates H3s] ──────────────── → note 2 (2 json code blocks)
system-prompt.md
├── (intro + assembly layers: build/resolve/runtime) ─ → note 3 (oc_concepts_system_prompt)
├── Structure (fixed sections + cache boundary) ────── → note 3
├── Prompt modes (full/minimal/none) ───────────────── → note 3
├── Prompt snapshots (Codex happy-path fixtures) ───── → note 3
├── Workspace bootstrap injection (files + limits) ─── → note 3
├── Time handling ──────────────────────────────────── → note 3 (→ links note 4)
├── Skills (available-skills list, 1 code block) ───── → note 3
└── Documentation (local docs/source location) ─────── → note 3
timezone.md
├── Three timezone surfaces (envelope/tool/prompt) ─── → note 4 (oc_concepts_timezone)
├── Setting the user timezone (1 json5 code block) ─── → note 4
└── When to override (UTC / fixed IANA / off) ──────── → note 4
typebox.md
├── (intro: TypeBox = one source of truth) ─────────── → note 5 (oc_concepts_typebox_protocol)
├── Mental model (req/res/event frames, conn flow) ─── → note 5 (ascii flow block)
├── (Common methods + events table) ────────────────── → note 5
├── Where the schemas live ─────────────────────────── → note 5
├── How the schemas are used at runtime ────────────── → note 5
├── Example frames (connect/hello-ok/req/res/event) ── → note 5 (json blocks)
├── Minimal client (Node.js) ───────────────────────── → note 5 (ts block) [reference impl]
├── Swift codegen behavior ─────────────────────────── → note 5
├── Versioning + compatibility ─────────────────────── → note 5
├── Schema patterns and conventions ────────────────── → note 5
├── Live schema JSON ───────────────────────────────── → note 5 (→ References)
├── Current pipeline (protocol:gen/:swift/:check) ──── → note 6 (oc_concepts_typebox_codegen)
├── Worked example: add a method end-to-end ────────── → note 6 (schema/validation/handler/register/regen blocks)
└── When you change schemas (5-step checklist) ─────── → note 6
typing-indicators.md
├── (intro: typingMode + typingIntervalSeconds) ────── → note 7 (oc_concepts_typing_indicators)
├── Defaults (unset legacy behavior) ───────────────── → note 7
├── Modes (never/instant/thinking/message + order) ─── → note 7
├── Configuration (agent + session, 2 json5 blocks) ── → note 7
└── Notes (silent token, thinking, heartbeat rules) ── → note 7
usage-tracking.md
├── What it is (provider quota, X% left normalize) ─── → note 8 (oc_concepts_usage_tracking)
├── Where it shows up (/status, /usage, CLI, menu) ─── → note 8
├── Custom /usage full footer [Shape, Contract Paths,
│   Verbs, Piece forms, Example H3s] ───────────────── → note 8 (json/jsonc blocks)
└── Providers + credentials (per-provider auth) ────── → note 8
```
No orphaned sections. The Molty prompt (note 1), Node.js minimal client (note 5), and usage-bar template
(note 8) are reproduced selectively, ≤6 code blocks per note. Provider auth detail → providers sub-plans;
Date & Time full reference → `rt02`; gateway tool/config → gateway sub-plans; sibling concept pages (message
lifecycle, progress drafts, retry, presence, context-engine, agent, agent-workspace) → `co01`–`co06`.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| typebox.md (1,108w, **13 code blocks**, 13 H2) | note 5 `oc_concepts_typebox_protocol` (model) + note 6 `oc_concepts_typebox_codegen` (procedure) | Exceeds the ≤6 code-block density cap (13 fences) AND mixes two building blocks: the WS frame/schema **model** (req/res/event frames, methods/events, AJV validation, conventions) vs the codegen **procedure** (`protocol:gen` pipeline + the step-by-step add-a-method workflow + schema-change checklist). Split per mixed-BB + code-density rules; each note then holds ≤6 code blocks. |

All other pages: single BB, ≤2,500w, ≤6 code after selective inclusion → **1 note each**.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (8,264 words, 25 code blocks). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×5** (notes 1, 2, 3, 4, 8) · **model ×1** (note 5) · **procedure ×2** (notes 6, 7).
- Est. digest words ~4,500 (avg ~560/note); each note ≤750w, ≤6 code blocks, single building_block.
  ≥10 code_snippets · ≥10 docs** + relevant `repo_openclaw*` + sibling `oc_*` (this series, planned) +
  **Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)** section.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> (the `claude_code`/`cc_*`, `hermes_agent`/`hermes_*`, `pi`/`pi_*`, `band`/`band_*` coding-agent corpora +
> Bedrock + context-engineering); sibling `oc_*` docs (this series) and `entry_openclaw_docs.md` are marked
> **(planned, this series)** / **(planned, W1)** and count toward the 10-doc floor. Relevance is the selection
> `resources/documentation/openclaw/oc_X.md`. `term_system_prompt` and `term_token_usage` confirmed MISSING in DB
> (any variant) — NOT cited; substitutes used per the Undigested Terms Plan.

### note 1 — oc_concepts_soul (9t · 10s · 10d)

**Terms**
- [SOUL.md](../../term_dictionary/term_soul_md.md) — the OpenClaw personality/voice file; relevance: this note IS the doc page for SOUL.md, so the term note is its primary glossary anchor.
- [AGENTS.md](../../term_dictionary/term_agents_md.md) — the operating-rules workspace file; relevance: the page's "One warning" draws the SOUL-vs-AGENTS boundary (voice vs operating rules).
- [Virtual Persona](../../term_dictionary/term_virtual_persona.md) — agent personality/character abstraction; relevance: SOUL.md is how an OpenClaw agent's persona is authored.
- [Persona](../../term_dictionary/term_persona.md) — adopted role/voice for an LLM; relevance: SOUL.md sets tone, opinions, bluntness — the persona layer.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — designing high-priority instruction layers; relevance: the page grounds SOUL.md in OpenAI's prompt-engineering guidance (high-level behavior/tone belong in the instruction layer).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: SOUL.md shapes the LLM's surface behavior/voice.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family commonly driving OpenClaw; relevance: the "Molty prompt" rewrites SOUL.md for a Claude-backed agent.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: OpenClaw is one, and SOUL.md tunes its conversational stance.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime wrapping an LLM into an agent; relevance: OpenClaw injects SOUL.md into the harness on normal sessions, giving it real weight.

**Docs**
- [hermes — Personality / SOUL](../hermes_agent/hermes_personality_soul.md) — Hermes' personality-file concept; relevance: direct sibling-ecosystem analog of the same SOUL.md mechanism.
- [hermes — Use SOUL.md Guide](../hermes_agent/hermes_use_soul_md_guide.md) — Hermes how-to for authoring SOUL.md; relevance: parallel authoring guidance for the same file.
- [hermes — Context Files](../hermes_agent/hermes_context_files.md) — the workspace files injected into context (AGENTS/SOUL/etc.); relevance: situates SOUL.md among the injected context files.
- [hermes — Prompt Assembly](../hermes_agent/hermes_prompt_assembly.md) — how Hermes composes its system prompt; relevance: explains where SOUL.md lands in the prompt (the system-prompt note's analog).
- [hermes — Features Overview](../hermes_agent/hermes_features_overview.md) — Hermes capability surface; relevance: cross-ecosystem orientation for where personality config sits.
- [cc — Customize System Prompt (SDK)](../claude_code/cc_sdk_customize_system_prompt.md) — Claude Code system-prompt customization; relevance: closest Claude Code analog to a voice/persona layer.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) — how SOUL.md is composed into runtime context (planned, this series); relevance: primary tie — note 3 details SOUL.md's injection.
- [oc_concepts_typing_indicators](oc_concepts_typing_indicators.md) — sibling concept page (planned, this series); relevance: same Concepts cluster.
- [cc — Output Styles](../claude_code/cc_output_styles.md) — Claude Code output-style/voice presets; relevance: closest Claude Code analog to SOUL.md's voice/tone/persona layer (how the agent's surface style is tuned).

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime that injects SOUL.md; relevance: implements SOUL.md weighting on normal sessions.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: home of the workspace-file injection path.

**Snippets**
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — bootstrap-file/context injection into the prompt; relevance: the exact code that injects SOUL.md.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap-file size/budget gating; relevance: SOUL.md is a bootstrap file subject to these limits.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity resolution; relevance: identity/persona resolution alongside SOUL.md.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — full/minimal/none prompt modes; relevance: SOUL.md is filtered out for sub-agents (minimal mode).
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — stable-vs-volatile prompt sections; relevance: SOUL.md sits in the stable, cache-friendly Project Context.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads workspace/context files for the prompt; relevance: Hermes analog of SOUL.md loading.
- [snippet_hermes_agent_core_prompt_builder_context_helpers](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_helpers.md) — prompt context-assembly helpers; relevance: how personality/context files are stitched in.
- [snippet_hermes_agent_core_prompt_builder_subscription_truncate](../../code_snippets/snippet_hermes_agent_core_prompt_builder_subscription_truncate.md) — truncates oversized injected files; relevance: SOUL.md/MEMORY.md truncation behavior parallel.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt cache boundary handling; relevance: SOUL.md placement relative to the cache boundary.

### note 2 — oc_concepts_streaming (8t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway/runtime; relevance: this is OpenClaw's outbound streaming behavior.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events streaming; relevance: contrasts with OpenClaw's block/preview (message-based) streaming — no true token-delta to channels.
- [Real-Time](../../term_dictionary/term_real_time.md) — low-latency interactive delivery; relevance: human-like pacing + preview updates create the real-time feel.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent over chat channels; relevance: streaming targets chat-channel messages.
- [Slack](../../term_dictionary/term_slack.md) — a supported channel; relevance: Slack native streaming + draft-preview modes are called out explicitly.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning trace; relevance: `/reasoning stream` writes reasoning into a transient preview.
- [Context Engine](../../term_dictionary/term_context_engine.md) — OpenClaw context subsystem; relevance: streamed blocks/coalescing feed the same message lifecycle.
- [LLM](../../term_dictionary/term_llm.md) — model emitting text deltas; relevance: block chunking consumes model `text_delta` events.
- [WebSocket](../../term_dictionary/term_websocket.md) — gateway transport; relevance: preview updates/edits ride the gateway WS to channels.

**Docs**
- [hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel delivery architecture; relevance: sibling-ecosystem analog of the block/preview delivery path.
- [hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media delivery config; relevance: parallels OpenClaw's streamed-media single-delivery/dup-suppression rules.
- [hermes — Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram preview/edit behavior; relevance: maps to OpenClaw's Telegram preview-streaming runtime.
- [hermes — Slash Commands (Messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — channel command surface; relevance: `/reasoning stream` and streaming toggles are command-driven.
- [cc — Channels Overview](../claude_code/cc_channels_overview.md) — Claude Code channel model; relevance: cross-tool view of channel message delivery.
- [cc — Build a Channel](../claude_code/cc_build_a_channel.md) — implementing a channel adapter; relevance: where per-channel streaming/chunk caps are enforced.
- [pi — Custom Streaming API](../pi/pi_custom_streaming_api.md) — Pi's streaming surface; relevance: closest coding-agent analog to outbound streaming control.
- [band — WebSocket Human Channels](../band/band_websocket_human_channels.md) — WS channel delivery to humans; relevance: parallel preview/streamed delivery transport.
- [cc — SDK Stream Text and Tool Calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed text + tool events; relevance: analog of tool-progress preview updates.
- [oc_concepts_typing_indicators](oc_concepts_typing_indicators.md) — typing vs preview streaming (planned, this series); relevance: typing indicators interleave with preview streaming.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-channel streaming modes + caps live here.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging delivery; relevance: block replies / preview edits delivery path.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `EmbeddedBlockChunker` + coalescing implementation.

**Snippets**
- [snippet_hermes_agent_gw_stream_batching](../../code_snippets/snippet_hermes_agent_gw_stream_batching.md) — batching streamed output; relevance: analog of block-chunk coalescing.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — consumes model stream events; relevance: analog of consuming `text_delta` for chunking.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — backpressure on stream flush; relevance: parallels idle/min/max flush bounds.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered delta over chat; relevance: buffered block-delta delivery on the gateway.
- [snippet_hermes_agent_core_chat_helpers_streaming_loop](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_loop.md) — the streaming loop; relevance: analog of the stream-blocks-as-you-go path.
- [snippet_hermes_agent_core_chat_helpers_streaming_setup](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_setup.md) — streaming setup/config; relevance: analog of `blockStreaming*` defaults wiring.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: maps to per-channel `*.blockStreaming`/`*.chunkMode` overrides.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound delivery path; relevance: final block-reply send + media single-delivery.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP SSE streaming; relevance: shows where true SSE exists (HTTP API) vs message-based channel streaming.

### note 3 — oc_concepts_system_prompt (9t · 12s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime that owns the prompt; relevance: the prompt is OpenClaw-owned for every agent run.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — designing prompt structure; relevance: the page is the OpenClaw system-prompt design.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reusing a cached prompt prefix; relevance: the fixed cache boundary keeps stable Project Context above it.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned helper agent; relevance: `promptMode: minimal` renders smaller prompts for sub-agents.
- [Skills](../../term_dictionary/term_skills.md) — on-demand instruction modules; relevance: the Skills section injects the available-skills list.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: bootstrap-file limits + cache split manage context usage.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning trace; relevance: the Reasoning section + `/reasoning` toggle control visibility.
- [LLM](../../term_dictionary/term_llm.md) — the model receiving the prompt; relevance: provider overlays tune per-model-family prompt text.
- [Claude](../../term_dictionary/term_claude.md) — a target model family; relevance: provider-owned cache-aware prompt contributions (vs GPT-5 overlay).

**Docs**
- [hermes — Prompt Assembly](../hermes_agent/hermes_prompt_assembly.md) — Hermes prompt-assembly model; relevance: direct sibling analog of the 3-layer renderer + sections.
- [hermes — Context Files](../hermes_agent/hermes_context_files.md) — injected workspace files; relevance: AGENTS/SOUL/TOOLS/IDENTITY/USER bootstrap injection analog.
- [hermes — Persistent Memory](../hermes_agent/hermes_persistent_memory.md) — MEMORY.md handling; relevance: parallels MEMORY.md injection vs on-demand memory tools.
- [hermes — Runtime Context Settings](../hermes_agent/hermes_runtime_context_settings.md) — context-limit knobs; relevance: analog of `contextLimits.*` / bootstrap caps.
- [cc — Customize System Prompt (SDK)](../claude_code/cc_sdk_customize_system_prompt.md) — programmatic prompt customization; relevance: closest Claude Code analog of prompt assembly.
- [cc — SDK System Prompts](../claude_code/cc_sdk_system_prompts.md) — system-prompt construction; relevance: parallel of fixed sections + overrides.
- [cc — CLI System Prompt Flags](../claude_code/cc_cli_system_prompt_flags.md) — CLI prompt flags; relevance: analog of prompt modes / append behavior.
- [cc — Skills Overview](../claude_code/cc_skills_overview.md) — skills injection model; relevance: analog of the available-skills list injection.
- [oc_concepts_soul](oc_concepts_soul.md) — SOUL.md as a prompt layer (planned, this series); relevance: SOUL.md is a bootstrap file injected by this prompt.
- [oc_concepts_timezone](oc_concepts_timezone.md) — the Current Date & Time section (planned, this series); relevance: the prompt's cache-stable time-zone block.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — prompt builder + bootstrap injection; relevance: `buildAgentSystemPrompt` / context injection live here.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: runtime adapters + provider overlays.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: owns the skills-list budget + `formatSkillsForPrompt`.

**Snippets**
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — full/minimal/none prompt modes; relevance: the exact prompt-mode logic the page describes.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — workspace/context injection; relevance: bootstrap-file injection into the prompt.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — stable-vs-volatile section split; relevance: the cache-boundary section ordering.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap size budget; relevance: `bootstrapMaxChars`/`bootstrapTotalMaxChars` enforcement.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — sub-agent spawn caps; relevance: ties to the minimal-mode sub-agent prompt + delegation guidance.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — loads context files; relevance: analog of bootstrap-file resolution.
- [snippet_hermes_agent_core_prompt_builder_skills_snapshot](../../code_snippets/snippet_hermes_agent_core_prompt_builder_skills_snapshot.md) — snapshots the skills list; relevance: analog of the available-skills injection + version markers.
- [snippet_hermes_agent_core_prompt_builder_subscription_truncate](../../code_snippets/snippet_hermes_agent_core_prompt_builder_subscription_truncate.md) — truncates oversized injected content; relevance: analog of bootstrap truncation markers.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt cache prefix handling; relevance: the prompt cache boundary mechanics.
- [snippet_hermes_agent_skills_index_cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — skills index/version cache; relevance: analog of the `<version>` skill markers re-read rule.
- [snippet_slipbox_scan_skills](../../code_snippets/snippet_slipbox_scan_skills.md) — scans/formats skills for a prompt; relevance: analog of `formatSkillsForPrompt` available-skills block.

### note 4 — oc_concepts_timezone (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime normalizing timestamps; relevance: this is OpenClaw's timezone-surface model.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cache-stable prompt prefix; relevance: the system-prompt time-zone block omits the live clock to keep caching stable.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: cron expressions use the configured timezone for scheduling.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — cron schedule syntax; relevance: schedule evaluation is timezone-dependent.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — active-hours/liveness scheduling; relevance: active hours use timezone for scheduling windows.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: dropping the live clock keeps the cached prefix stable, conserving the window.
- [LLM](../../term_dictionary/term_llm.md) — model consuming the prompt; relevance: standardized single reference time avoids mixed provider-local clocks for the model.
- [Caching](../../term_dictionary/term_caching.md) — general cache behavior; relevance: cache stability is the reason the clock value is omitted.

**Docs**
- [hermes — Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron scheduling; relevance: timezone-aware schedule analog.
- [hermes — Cron Internals](../hermes_agent/hermes_cron_internals.md) — cron evaluation internals; relevance: how timezone enters schedule computation.
- [hermes — Runtime Context Settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime/context knobs; relevance: envelope/time-format settings analog.
- [hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — message envelope/delivery; relevance: where inbound-message timestamp envelopes are stamped.
- [cc — Scheduled Task Execution Model](../claude_code/cc_scheduled_task_execution_model.md) — scheduled-task timing; relevance: cross-tool analog of timezone-bound scheduling.
- [cc — Scheduling Options Comparison](../claude_code/cc_scheduling_options_comparison.md) — scheduling options; relevance: timezone is a scheduling input across options.
- [band — WebSocket Overview](../band/band_websocket_overview.md) — WS event/envelope model; relevance: analog of normalized timestamp fields on events.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) — the Current Date & Time section + `session_status` (planned, this series); relevance: the system-prompt time-zone surface this note feeds.
- [oc_rt_date_time (date-time)](../openclaw/oc_rt_date_time.md) — full Date & Time reference (planned, rt02 this series); relevance: the page's link-out for full per-provider behavior.
- [hermes — Cron Advanced Jobs](../hermes_agent/hermes_cron_advanced_jobs.md) — advanced timezone-bound cron job config; relevance: parallels OpenClaw's timezone-driven schedule evaluation (active hours / cron in the configured zone).

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: host-timezone resolution + system-prompt time block.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging/envelopes; relevance: envelope timestamping + `envelopeTimezone`.

**Snippets**
- [snippet_hermes_agent_cron_job_schema](../../code_snippets/snippet_hermes_agent_cron_job_schema.md) — cron-job schema incl. timezone; relevance: analog of timezone-bound cron config.
- [snippet_hermes_agent_cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — cron-job state/next-run; relevance: next-run computation depends on timezone.
- [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — cron runner; relevance: schedule firing uses configured zone.
- [snippet_otf_text_date_parsing_utils](../../code_snippets/snippet_otf_text_date_parsing_utils.md) — date/time parsing utilities; relevance: IANA-zone/format parsing analog (`timeFormat` auto/12/24).
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound delivery + envelope; relevance: where envelope timestamp prefixes are applied.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cache-stable prompt sections; relevance: the time-zone-only Current Date & Time block sits above the cache boundary.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — prompt section injection; relevance: injects the Current Date & Time section when `userTimezone` is known.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt cache prefix; relevance: the cache-stability reason for omitting the live clock.

### note 5 — oc_concepts_typebox_protocol (9t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime defining the protocol; relevance: this is OpenClaw's Gateway WS protocol model.
- [WebSocket](../../term_dictionary/term_websocket.md) — the transport; relevance: every frame is a Gateway WS message.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC over JSON; relevance: the req/res frame model is JSON-RPC-shaped (id/method/params).
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema format; relevance: TypeBox exports draft-07 JSON Schema for the protocol.
- [TypeScript](../../term_dictionary/term_typescript.md) — TypeBox's host language; relevance: schemas are TypeScript-first, source of truth in `schema.ts`.
- [Discriminated Union](../../term_dictionary/term_discriminated_union.md) — tagged-union typing; relevance: `GatewayFrame` uses a discriminator on `type` (req/res/event).
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedupe key for side-effecting calls; relevance: methods with side effects require `idempotencyKey`.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: methods (`health`, `chat.send`) are RPCs over the frame protocol.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — feature/version handshake; relevance: `hello-ok` advertises `features.methods`/`events` + protocol-version negotiation.

**Docs**
- [pi — RPC Protocol](../pi/pi_rpc_protocol.md) — Pi's RPC protocol; relevance: direct coding-agent analog of a schema-defined RPC/event protocol.
- [pi — RPC Events](../pi/pi_rpc_events.md) — Pi's server-push events; relevance: analog of the event-frame inventory (`tick`/`presence`/`agent`).
- [band — WebSocket Agent Events](../band/band_websocket_agent_events.md) — WS agent event model; relevance: analog of server-push event frames.
- [band — WebSocket Human Events](../band/band_websocket_human_events.md) — WS human-side events; relevance: parallel event-frame contract.
- [band — A2A Overview](../band/band_a2a_overview.md) — agent-to-agent protocol; relevance: a sibling schema-first WS/RPC protocol.
- [band — A2A Gateway](../band/band_a2a_gateway.md) — A2A gateway endpoint; relevance: gateway-mediated protocol analog.
- [cc — LLM Gateway](../claude_code/cc_llm_gateway.md) — gateway/proxy protocol surface; relevance: cross-tool gateway-protocol framing.
- [oc_concepts_typebox_codegen](oc_concepts_typebox_codegen.md) — the codegen procedure half (planned, this series); relevance: regenerates the artifacts this model defines.
- [oc_concepts_streaming](oc_concepts_streaming.md) — channel delivery over the gateway (planned, this series); relevance: event frames carry streamed updates.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server/protocol; relevance: handshake + method dispatch + AJV validation.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: `packages/gateway-protocol` schemas + validators.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS app; relevance: consumes generated Swift `GatewayModels`.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — req/res/event frame envelope; relevance: the exact three-frame model the note documents.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — protocol schema grouping; relevance: how `ProtocolSchemas` organizes methods/events.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — error codes + protocol version; relevance: `PROTOCOL_VERSION` + `ErrorCode` + min/max negotiation.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect handshake; relevance: the `connect`-must-be-first flow.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: connect/hello-ok/tick connection flow.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method scope gating; relevance: scope enforcement + `hello-ok` feature advertising alignment.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — server event broadcast; relevance: server-push event frames.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — `chat.send` method handler; relevance: a concrete side-effecting method requiring `idempotencyKey`.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — client-kit WS channel; relevance: a client consuming the frame protocol.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node-session over gateway WS; relevance: node-action methods (`node.*`) over the protocol.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — JSON-RPC server; relevance: sibling JSON-RPC frame validation analog.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP server; relevance: a parallel schema-validated protocol surface in OpenClaw.

### note 6 — oc_concepts_typebox_codegen (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime owning the pipeline; relevance: this is OpenClaw's `protocol:gen`/`check` codegen workflow.
- [Code Generation](../../term_dictionary/term_code_generation.md) — generating code/artifacts from a source; relevance: TypeBox schemas generate JSON Schema + Swift models.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — generated schema artifact; relevance: `pnpm protocol:gen` writes draft-07 JSON Schema.
- [WebSocket](../../term_dictionary/term_websocket.md) — the protocol being generated; relevance: the codegen targets the Gateway WS protocol.
- [TypeScript](../../term_dictionary/term_typescript.md) — schema source language; relevance: the worked example edits `schema.ts`/`index.ts` in TS.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — side-effect dedupe; relevance: new side-effecting methods must declare `idempotencyKey` during the add-a-method flow.
- [RPC](../../term_dictionary/term_rpc.md) — remote procedure; relevance: the worked example adds a `system.echo` RPC handler.
- [Schema Evolution](../../term_dictionary/term_schema_evolution.md) — versioned schema change; relevance: the "When you change schemas" checklist is schema-evolution discipline.

**Docs**
- [pi — RPC Protocol](../pi/pi_rpc_protocol.md) — Pi RPC protocol; relevance: analog of a generated/validated RPC surface.
- [pi — SDK Run Modes](../pi/pi_sdk_run_modes.md) — SDK build/run modes; relevance: parallel to the build/regenerate pipeline.
- [band — A2A Adapter](../band/band_a2a_adapter.md) — protocol adapter wiring; relevance: registering/handling a method end-to-end analog.
- [band — Integration Methods](../band/band_integration_methods.md) — adding integration methods; relevance: parallels add-a-method registration steps.
- [cc — LLM Gateway](../claude_code/cc_llm_gateway.md) — gateway protocol surface; relevance: where generated protocol artifacts are consumed.
- [oc_concepts_typebox_protocol](oc_concepts_typebox_protocol.md) — the model half it regenerates from (planned, this series); relevance: codegen reads these schemas as source of truth.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) — the `gateway` tool / config self-update (planned, this series); relevance: agents invoke generated methods via the gateway tool.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — server-methods + dispatch; relevance: where handlers/registration/scopes are edited.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the protocol package + `pnpm protocol:*` scripts.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS app; relevance: the Swift codegen target regenerated by `protocol:gen:swift`.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — schema grouping/registration; relevance: where a new schema gets added to `ProtocolSchemas`.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — a method handler; relevance: the handler-implementation step of add-a-method.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method scope classification; relevance: the `method-scopes.ts` classification step.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — registering/broadcasting server behavior; relevance: registering the new method server-side.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — frame envelope; relevance: the req/res shape the generated validators enforce.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — version + error codes; relevance: regenerated `GATEWAY_PROTOCOL_VERSION` artifacts.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — client consuming generated types; relevance: downstream consumer of regenerated models.
- [snippet_hermes_agent_tui_server_jsonrpc](../../code_snippets/snippet_hermes_agent_tui_server_jsonrpc.md) — JSON-RPC server registration; relevance: sibling analog of register-a-method.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entrypoint registration; relevance: parallel registration/export pattern.
- [snippet_hermes_agent_acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — ACP protocol auth wiring; relevance: parallel protocol-surface method wiring.

### note 7 — oc_concepts_typing_indicators (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime sending typing; relevance: this is OpenClaw's typing-indicator config.
- [Chatbot](../../term_dictionary/term_chatbot.md) — chat-channel agent; relevance: typing is a chat-channel liveness signal.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning trace; relevance: `thinking` mode starts typing on the first reasoning delta (`reasoningLevel: "stream"`).
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — liveness/active-hours runs; relevance: heartbeat typing starts at heartbeat run start, a special liveness case.
- [Slack](../../term_dictionary/term_slack.md) — a typing-capable channel; relevance: typing delivery depends on channel typing support (e.g. Slack).
- [Real-Time](../../term_dictionary/term_real_time.md) — interactive feedback; relevance: typing indicators keep the turn visually alive in real time.
- [LLM](../../term_dictionary/term_llm.md) — model emitting deltas; relevance: `message`/`thinking` modes key off the model's text/reasoning deltas.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned helper; relevance: session-level overrides + silent-token rules interact with sub-agent runs.

**Docs**
- [hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel delivery; relevance: where typing signals are delivered per channel.
- [hermes — Telegram Advanced](../hermes_agent/hermes_telegram_advanced.md) — Telegram channel behavior; relevance: typing-capable channel behavior analog.
- [hermes — Slash Commands (Messaging)](../hermes_agent/hermes_slash_commands_messaging.md) — channel command/config surface; relevance: typing-mode is an agent/session config knob.
- [cc — Effort Level and Thinking](../claude_code/cc_effort_level_and_thinking.md) — reasoning/thinking levels; relevance: `thinking` typing mode requires streamed reasoning.
- [cc — SDK Stream Text and Tool Calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed deltas; relevance: `message` mode keys off the first non-silent text delta.
- [band — Agent API Context Activity](../band/band_agent_api_context_activity.md) — activity/status surface; relevance: analog of liveness/activity indicators.
- [pi — Custom Models](../pi/pi_custom_models.md) — model config incl. reasoning; relevance: reasoning-stream availability gates `thinking` typing.
- [oc_concepts_streaming](oc_concepts_streaming.md) — typing vs preview streaming (planned, this series); relevance: typing interleaves with preview streaming; shared compact-progress channels.
- [oc_concepts_presence (presence)](../openclaw/oc_concepts_presence.md) — presence/liveness (planned, co05 this series); relevance: typing is a presence-adjacent liveness signal.
- [hermes — Slack Messaging](../hermes_agent/hermes_messaging_slack.md) — Slack channel delivery/behavior; relevance: Slack is the typing-capable channel this note calls out, and typing delivery depends on per-channel typing support.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-channel typing-capability + delivery.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging delivery; relevance: typing-indicator send + refresh cadence.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status/reactions; relevance: closest analog of channel-side status/typing signals.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat-buffered delta; relevance: heartbeat typing/liveness at run start.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — presence/event push; relevance: presence-adjacent liveness signaling.
- [snippet_hermes_agent_core_chat_helpers_streaming_loop](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_loop.md) — streaming loop with first-delta detection; relevance: where `message`/`thinking` start triggers fire.
- [snippet_hermes_agent_core_chat_helpers_streaming_setup](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_setup.md) — streaming/typing setup; relevance: analog of wiring typing-mode start timing.
- [snippet_hermes_agent_core_think_scrubber](../../code_snippets/snippet_hermes_agent_core_think_scrubber.md) — reasoning-delta handling; relevance: `thinking` typing keys off reasoning deltas.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound delivery; relevance: typing send rides the same delivery path.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: analog of agent vs session typing-mode/cadence config.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — a channel platform adapter; relevance: per-platform typing-capability gating.

### note 8 — oc_concepts_usage_tracking (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the runtime surfacing usage; relevance: this is OpenClaw's usage-tracking model + usage-bar template.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — model key-value cache; relevance: usage footer reports `cache_hit_pct` / cache counters (substitute for the missing `term_token_usage`).
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cached prompt prefix; relevance: cache reads are part of the per-turn usage contract + `/status` cache counters.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: the usage bar renders `context.max_tokens` / `pct_used` (substitute for missing `term_token_usage`).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — provider OAuth credential; relevance: usage polling needs OAuth tokens in auth profiles (Anthropic/Copilot/Gemini/Codex).
- [DeepSeek](../../term_dictionary/term_deepseek.md) — a provider; relevance: DeepSeek shows a balance via API key instead of a percent-left window.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic provider; relevance: Anthropic usage uses OAuth tokens in auth profiles.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — provider quota windows; relevance: usage normalizes provider quota to `X% left` windows.
- [Throttling](../../term_dictionary/term_throttling.md) — quota/limit enforcement; relevance: provider quota windows reflect throttle/limit state.

**Docs**
- [cc — SDK Cost and Usage Tracking](../claude_code/cc_sdk_cost_and_usage_tracking.md) — usage/cost tracking; relevance: direct coding-agent analog of usage surfaces.
- [cc — Cost Tracking](../claude_code/cc_cost_tracking.md) — cost reporting; relevance: parallels the `/usage cost` local summary.
- [cc — Reduce Token Usage](../claude_code/cc_reduce_token_usage.md) — token-usage reduction; relevance: same token/usage accounting domain.
- [cc — Cache Lifetime and Scope](../claude_code/cc_cache_lifetime_and_scope.md) — prompt-cache behavior; relevance: `cache_hit_pct` semantics in the usage bar.
- [cc — Server and Usage Limit Errors](../claude_code/cc_server_and_usage_limit_errors.md) — usage-limit errors; relevance: provider quota-window exhaustion analog.
- [cc — Statusline JSON Fields](../claude_code/cc_statusline_json_fields.md) — statusline field contract; relevance: direct analog of the usage-bar contract-path/verb DSL.
- [cc — Statusline Advanced Examples](../claude_code/cc_statusline_advanced_examples.md) — statusline templating examples; relevance: analog of the usage-template piece/verb composition.
- [hermes — Credential Pools](../hermes_agent/hermes_credential_pools.md) — provider credential management; relevance: usage falls back to OAuth/API-key credentials from profiles.
- [hermes — Context Compression / Caching](../hermes_agent/hermes_context_compression_caching.md) — caching/usage interplay; relevance: cache counters feed usage reporting.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) — cost/usage runtime context (planned, this series); relevance: `session_status` + `/status` usage interplay.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: per-provider usage auth + quota polling.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: usage-bar render + `/usage` + `/status` surfaces.

**Snippets**
- [snippet_hermes_agent_core_account_usage](../../code_snippets/snippet_hermes_agent_core_account_usage.md) — account usage polling; relevance: direct analog of pulling provider usage/quota.
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — per-turn usage accounting; relevance: the turn-aggregate token/cache counters the bar reads.
- [snippet_hermes_agent_core_rate_limit_tracker](../../code_snippets/snippet_hermes_agent_core_rate_limit_tracker.md) — rate-limit/quota tracking; relevance: provider quota-window state behind `X% left`.
- [snippet_hermes_agent_core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — quota recovery; relevance: how exhausted windows recover/normalize.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: usage auth resolution order (OAuth → API key → env).
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth token portability; relevance: OAuth tokens in auth profiles for provider usage.
- [snippet_hermes_agent_core_credential_pool_dataclass](../../code_snippets/snippet_hermes_agent_core_credential_pool_dataclass.md) — credential pool model; relevance: per-provider credential fallback for usage polling.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider plugin; relevance: provider-specific usage auth (Claude OAuth).
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — provider fallback activation; relevance: `model.is_fallback` usage-bar flag source.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cache section accounting; relevance: cache counters that the usage bar reports.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt-cache hit accounting; relevance: `usage.cache_hit_pct` source.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary is digested as `oc_*` documentation concept notes by their home sub-plan, NOT as
> new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms. **co07 creates
> 0 new `term_dictionary` notes.**

| Term | Disposition |
|---|---|
| SOUL.md / personality file / "voice" | Documented in `oc_concepts_soul` (note 1); link existing `term_persona`, `term_prompt_engineering`. Not a term note. |
| block streaming / preview streaming / chunking / coalescing | Documented in `oc_concepts_streaming` (note 2); link existing `term_sse`, `term_real_time`. Streaming mechanics are doc content, not a term. |
| system prompt assembly / prompt modes / bootstrap injection / prompt cache boundary | Documented in `oc_concepts_system_prompt` (note 3); link existing `term_prompt_engineering`, `term_prompt_caching`, `term_context_window`. |
| envelope timezone / userTimezone / IANA zone | Documented in `oc_concepts_timezone` (note 4); link existing `term_cron`, `term_heartbeat`. Config knobs, not terms. |
| TypeBox / Gateway WS protocol / req-res-event frames / codegen | Documented in `oc_concepts_typebox_protocol` + `_codegen` (notes 5/6); link existing `term_websocket`, `term_json_rpc`, `term_json_schema`, `term_typescript`, `term_discriminated_union`, `term_code_generation`. TypeBox is a third-party library name (config/impl detail), not promoted. |
| typing indicators / typingMode | Documented in `oc_concepts_typing_indicators` (note 7); link existing `term_chatbot`, `term_heartbeat`. UI/config behavior, not a term. |
| usage tracking / quota window / usage-bar template / contract paths / verbs | Documented in `oc_concepts_usage_tracking` (note 8); link existing `term_kv_cache`, `term_prompt_caching`, `term_context_window`, `term_rate_limiting`. Template DSL is doc content. |

**New-term candidate scan (Step 2d):** No genuinely cross-cutting, vault-reusable term lacks an existing note here.
Three plausible-but-rejected slugs surfaced during DB-verify and are intentionally NOT captured:
- `term_system_prompt` — MISSING in DB, but "system prompt" is a doc-page subject (note 3 owns it); the reusable
  umbrella concept is already `term_prompt_engineering` (existing). **Do not capture** (master: vocab → `oc_*` notes).
- `term_token_usage` — MISSING, but usage/quota is note 8's doc subject; `term_kv_cache` + `term_context_window` +
  `term_rate_limiting` (all existing) cover the reusable pieces. **Do not capture.**
- `term_typebox` — third-party library proper noun; documented as impl detail in note 5. **Do not capture.**

Expected new `term_dictionary` captures from co07: **0**.

## Term-Note Authoring Requirements

**N/A (0 new terms).** co07 authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from
master Step 4e / W5). Should a future re-scan promote a genuine cross-cutting term, it would be captured via
`/tessellum-capture-term-note` + added to its best-fit `acronym_glossary_*.md` (for the candidates above the closest
glossaries are `acronym_glossary_machine_learning.md` / an agentic/LLM glossary) — but none are warranted now.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must pass before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean (YAML field order/itemized lists/quoted years; `## Overview` + `## Related Notes` present; bold footer). |
| G2 | Grounding | Each note diffed vs `inbox/openclaw_docs/concepts/<page>.md`; no invented behavior; config keys/commands verbatim. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks; single `building_block`; every mapped H2/H3 represented. |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` links + sibling `oc_*` + `repo_openclaw*` + `entry_openclaw_docs`, each indexed `[text](path.md)` with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links`; 0 broken links after incremental reindex. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` + the inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_soul oc_concepts_streaming oc_concepts_system_prompt oc_concepts_timezone oc_concepts_typebox_protocol oc_concepts_typebox_codegen oc_concepts_typing_indicators oc_concepts_usage_tracking"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density: words (body only) + code blocks
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb)"
  # sibling-prefix cross-ref present (≥1 oc_ link)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) LINK in $n"
done

# YAML frontmatter sweep for the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code blocks (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_concepts_soul | concept | 450 | 1 (Molty prompt) | ✅ |
| 2 | oc_concepts_streaming | concept | 700 | ≤4 (block-flow ascii + 2 json, select) | ✅ |
| 3 | oc_concepts_system_prompt | concept | 750 | ≤2 (available_skills block + 0–1) | ✅ |
| 4 | oc_concepts_timezone | concept | 350 | 1 (json5 userTimezone) | ✅ |
| 5 | oc_concepts_typebox_protocol | model | 650 | ≤6 (frame examples + conn-flow + minimal client, select) | ✅ |
| 6 | oc_concepts_typebox_codegen | procedure | 500 | ≤6 (pipeline + add-method snippets, select) | ✅ |
| 7 | oc_concepts_typing_indicators | procedure | 400 | 2 (json5 agent + session) | ✅ |
| 8 | oc_concepts_usage_tracking | concept | 700 | ≤4 (usageTemplate + Shape + Example, select) | ✅ |

No note approaches the word cap. The code-heavy `typebox.md` (13 fences) split into notes 5+6 so each stays ≤6;
`usage-tracking.md` (4 fences) reproduces the usage-bar template selectively to remain ≤6.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (CREATED as master pre-step W1; required since the corpus is
>30 notes) under the **Concepts** section / a "Personality, Prompt & Presentation" cluster. Each note receives its
entry-point back-link at finalization. No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all repo/term targets below were

- `entry_openclaw_docs.md` (planned) → **all 8 notes** (primary anti-island guarantee).
- `repo_openclaw_agents` → note 1 (SOUL.md), note 3 (prompt builder).
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → note 2 (streaming), note 7 (typing).
- `repo_openclaw_gateway` → notes 5, 6 (gateway protocol + codegen).
- `repo_openclaw_skills` → note 3 (skills-list injection).
- `repo_openclaw_extensions_llm_providers` → note 8 (provider usage auth).
- `term_websocket` → notes 5, 6; `term_prompt_engineering` → notes 1, 3; `term_prompt_caching` → notes 3, 4, 8;
  `term_kv_cache` → note 8; `term_persona` → note 1; `term_heartbeat` → notes 4, 7; `term_cron` → note 4;
  `term_json_schema` / `term_typescript` → notes 5, 6.

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page at execute; reproduce config keys / commands /
schema snippets verbatim; one `building_block` per note; ≤6 code blocks. Dynamic-workflow fan-out capped at ~30
agents/run (8 notes is well under). Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1
before commit. `git pull --rebase --autostash` first; commit+push after the phase; no Claude co-author trailer.

## Augmentation Report (2026-06-21)

**What was locked.** The old `## Candidate Cross-References` section (candidate pools, ≥6-term floor) was replaced
with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` at RAISED floors: **≥8
`term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs per note**, plus relevant `repo_openclaw*` + sibling
`oc_*` + `entry_openclaw_docs`. All 7 source pages were re-read from the local mirror (`inbox/openclaw_docs/concepts/`)
on 2026-06-21; measured words/code match the plan's Source table exactly (soul 628/1, streaming 1957/3,
system-prompt 2390/1, timezone 390/1, typebox 1108/13, typing-indicators 405/2, usage-tracking 1386/4). Selection
was relevance-driven (BM25 across `terminology`/`code_snippet`/`dev_tool_docs`/`aws_docs`/`platform_docs`/`tutorial`

note_name='<id>'"`. Independent G5 sweep over the LOCKED section: **250 cited `.md` links — 240 EXISTING

**Per-note locked counts** (all clear ≥8t · ≥10s · ≥10d):

| Note | BB | terms | snippets | docs | repos | floors |
|---|---|---:|---:|---:|---:|---|
| oc_concepts_soul | concept | 9 | 10 | 10 | 2 | ✅ |
| oc_concepts_streaming | concept | 9 | 12 | 11 | 3 | ✅ |
| oc_concepts_system_prompt | concept | 9 | 12 | 12 | 3 | ✅ |
| oc_concepts_timezone | concept | 8 | 10 | 10 | 2 | ✅ |
| oc_concepts_typebox_protocol | model | 9 | 12 | 11 | 3 | ✅ |
| oc_concepts_typebox_codegen | procedure | 8 | 11 | 10 | 3 | ✅ |
| oc_concepts_typing_indicators | procedure | 8 | 10 | 10 | 2 | ✅ |
| oc_concepts_usage_tracking | concept | 9 | 11 | 11 | 2 | ✅ |

**New-term candidates + best-fit glossary.** Re-read (Step 2d) surfaced NO genuinely cross-cutting, vault-reusable
term lacking an existing note. Two slugs are confirmed MISSING in the DB (any variant) but intentionally NOT
captured (master decision: OpenClaw vocab → `oc_*` doc notes, not `term_dictionary`); both have existing-term
substitutes wired into the mapping:
- `term_system_prompt` — MISSING; doc-page subject owned by note 3 (`oc_concepts_system_prompt`). Reusable umbrella =
  existing `term_prompt_engineering`. Best-fit glossary IF ever promoted: `acronym_glossary_machine_learning.md`
  (or an agentic/LLM glossary). **Do not capture now.**
- `term_token_usage` — MISSING; doc-page subject owned by note 8 (`oc_concepts_usage_tracking`). Reusable pieces
  covered by existing `term_kv_cache` + `term_context_window` + `term_rate_limiting`. Best-fit glossary IF promoted:
  `acronym_glossary_machine_learning.md`. **Do not capture now.**
`term_typebox` — third-party library proper noun, documented as impl detail in note 5; **do not capture**.
**Expected new `term_dictionary` captures from co07: 0** (unchanged).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance + descriptions) | **PASS** | LOCKED section: every note ≥8 terms / ≥10 snippets / ≥10 docs; each link rendered `- [Name](relpath.md) — what it is; relevance: …`. Counts table above; min observed = 8t/10s/10d (notes 4, 7). |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision`: 8 rows into `entry_openclaw_docs.md` (CREATE at master pre-step W1, >30-note corpus); every note back-linked at finalization. Decision matches >30 threshold (master = ~1,053 notes). |
| CP4 | Size | **PASS** | 8 planned notes ≤30. Sub-plan of a master+sub-plan structure; co07 is independently executable. |
| CP5 | Format derived (not invented) | **PASS** | Format inherited from master `## Format Definition`, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `## Overview` + source-mirrored H2/H3 + `## Related Notes` + `## References` + bold footer; YAML field order + forbidden-field list match. Target dir `resources/documentation/openclaw/` (W4 scan-mapping done). |
| CP6 | Density / BB atomicity (borderline → split) | **PASS** | `## Density Re-Assessment`: all 8 notes ≤750w / ≤6 code / single BB. typebox.md (13 fences, mixed model+procedure) split into notes 5+6 per code-density + mixed-BB rule; no other borderline. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages from the local mirror 2026-06-21 via `wc -w` / `grep -c '^\`\`\`'`; values match the plan's Source table exactly (ratio 1.0). Densest pages (system-prompt 2390w, streaming 1957w, usage-tracking 1386w, typebox 1108w) confirmed. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new terms, all rows = link-existing disposition); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; falls back to `/tessellum-capture-term-note` + best-fit glossary if a future re-scan promotes one). Master Step 4e ownership: OpenClaw vocab → `oc_*` doc notes. |
| CP8f | Slug specificity / collision audit (all notes, term + doc) | **PASS** | New-term scan (Step 2d) ran specificity + collision audit: 3 plausible slugs (`term_system_prompt`, `term_token_usage`, `term_typebox`) rejected with rationale; collision audit confirmed no planned `oc_concepts_*` doc note duplicates an existing substantive term/doc note (no `term_*`/doc covers soul/streaming/system-prompt/timezone/typebox/typing/usage as a vault note — `term_soul_md`/`term_agents_md` are LINKED, not duplicated; they are distinct term concepts, not the doc page). 0 removals required. |
| CP9 | Discoverability / inlinks (G8, in-degree ≥1 outside folder) | **PASS** | `## Inlinks (existing → new)` maps outside-folder inbound links for all 8 notes (`entry_openclaw_docs` → all 8; repo_openclaw* + terms per note); G7/G8 is in the gate table as a gated execution phase. |

**RESULT: 9/9 + CP8f PASS → READY FOR EXECUTION.** All notes meet the raised floors (≥8t · ≥10s · ≥10d), 0
ghosts, format derived, entry point + inlinks specified. Status advanced `pending → ready`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** (9/9 + CP8f PASS → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Plan Amendments (by master agent during execution)

| Date | Section | Original | Amended | Rationale |
|---|---|---|---|---|
| 2026-06-23 | Planned Notes | oc_concepts_system_prompt (1 concept note, full system-prompt page) | SPLIT into oc_concepts_system_prompt_structure (concept: prompt ownership, 3-layer assembly, provider contributions, fixed Structure sections, prompt modes, prompt snapshots) + oc_concepts_system_prompt_injection (procedure: workspace bootstrap injection + per-file limits, time handling, skills list injection, Documentation section) | Source `system-prompt.md` is ~3,000w; the single note was being compressed to fit ≤2500w, losing bootstrap-injection + skills + documentation detail. User directive: split, do not compress/omit. co07 note count 8 → 9. |
