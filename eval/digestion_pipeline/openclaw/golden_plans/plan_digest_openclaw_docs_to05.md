---
title: Sub-Plan to05 — OpenClaw Docs: Tools (Loop Detection, Media, Search Providers, Multi-Agent Sandbox)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - tools/loop-detection
  - tools/media-overview
  - tools/minimax-search
  - tools/multi-agent-sandbox-tools
  - tools/music-generation
  - tools/ollama-search
  - tools/parallel-search
---

# Sub-Plan to05: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order + `## Overview`/source-body/`## Related Notes`/`## References`/bold footer), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), the 9-GATE (G1–G9), cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are all INHERITED from the master and not re-justified here.

## Scope

The 7 `tools/` pages in this sub-plan cover a heterogeneous slice of OpenClaw's agent-facing tool surface:
(1) the **loop-detection / post-compaction guardrail** that bounds runaway tool-call loops, (2) the
**media-overview** index that maps image/video/music/TTS/STT/understanding capabilities to providers,
(3) three **`web_search` provider** setup pages (MiniMax, Ollama, Parallel), (4) the **multi-agent sandbox +
tool-policy precedence** reference, and (5) the **`music_generate` tool** end-to-end. Priority **P2 (Phase B —
features/integration)** per master; these reference/how-to pages describe runtime tool behavior the gateway,
provider, and concept layers depend on, but they sit below the P1 architecture/runtime core. Heavily linked to
the existing code-side `repo_openclaw*` notes (extensions, gateway, sessions) rather than duplicating them.

**Source**: OpenClaw docs, 7 pages, 6,727 measured words. **Planned: 7 notes (1 note per page; no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Tool-loop detection | `tools/loop-detection` | 978 | 3 | 6 | 1 | procedure |
| Media overview | `tools/media-overview` | 1,129 | 0 | 6 | 0 | concept |
| MiniMax search | `tools/minimax-search` | 394 | 1 | 5 | 0 | procedure |
| Multi-agent sandbox and tools | `tools/multi-agent-sandbox-tools` | 1,248 | 1 | 8 | 2 | procedure |
| Music generation | `tools/music-generation` | 1,682 | 11 | 9 | 4 | procedure |
| Ollama web search | `tools/ollama-search` | 521 | 4 | 4 | 0 | procedure |
| Parallel search | `tools/parallel-search` | 775 | 2 | 8 | 0 | procedure |

Total: **6,727 words**, **22 code fences**, single-BB per page. No page exceeds the 2,500-word cap; none mixes
building blocks → **no splits** (see Split Decisions). Note the highest code-fence page (music-generation = 11
fences) is reduced to ≤6 in its note by reproducing config/CLI snippets selectively (see Density Re-Assessment).

## Content Strategy

- **Prioritize**: `loop-detection` (runtime guardrail referenced by the concepts/compaction + gateway/config
  layers — the `tools.loopDetection` schema + post-compaction guard semantics are load-bearing) and
  `multi-agent-sandbox-tools` (the per-agent sandbox/tool-policy precedence chain that the sandboxing, tool-policy,
  and elevated docs all funnel into). `music-generation` is the most complete tool how-to (config → providers →
  async lifecycle → live tests) and anchors the media cluster.
- **Split**: **None.** Every page is single-BB and ≤1,682 words; one note per page (master "most reference
  pages = 1 note").
- **Link-out (not duplicate)**: `media-overview` is a capability index — its per-tool detail (image/video/tts/
  understanding/audio) lives on sibling pages digested by **to04** (`tools/image-generation`), **to08**
  (`tools/tts`, `tools/video-generation`, `tools/web`, `tools/web-fetch`), **nd01/nd02** (`nodes/audio`,
  `nodes/media-understanding`, `nodes/talk`); link those (planned) rather than restate. The three search
  providers all reference the **`tools/web`** Web-Search overview (to08, planned) for auto-detection and the
  generic `web_search` contract — link, do not re-explain provider auto-selection. Sandbox **modes/backends**
  detail lives in `gateway/sandboxing` + `gateway/sandbox-vs-tool-policy-vs-elevated` (gw05, planned) and
  `tools/elevated` (to03, planned); per-provider model/auth detail lives in `providers/*` (pr05 minimax,
  pr06 ollama, pr04 google, pr08 together, etc.) — link. Term vocabulary (loop, sandbox, web search, TTS,
  multimodal, compaction) → link existing `term_dictionary` notes; no term definition is inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_loop_detection.md` | procedure | `tools/loop-detection`: Why this exists, Configuration block + Field behavior, Recommended setup, Post-compaction guard, Logs and expected behavior | 700 | Enabling and tuning OpenClaw's two repetitive-tool-call guardrails — the rolling-history loop detector (`tools.loopDetection`, disabled by default) and the always-on post-compaction guard — with the full field schema, per-agent override, threshold-ordering guidance, and the `compaction_loop_persisted` abort behavior. |
| 2 | `oc_tools_media_overview.md` | concept | `tools/media-overview`: Capabilities, Provider capability matrix, Async vs synchronous, Speech-to-text and Voice Call, Provider mappings | 650 | The index of OpenClaw's media capabilities (image / video / music generation, TTS, STT, media understanding), how they are tool-driven and provider-gated, the provider capability matrix, the async-vs-sync model, and how Talk-mode live speech differs from the one-shot media tool path. |
| 3 | `oc_tools_minimax_search.md` | procedure | `tools/minimax-search`: Get a Token Plan credential, Config, Region selection, Supported parameters | 450 | Configuring MiniMax as a `web_search` provider via the Token Plan search API — credential env aliases (`MINIMAX_CODE_PLAN_KEY`/OAuth), the plugin + `tools.web.search` config block, CN/global region resolution order, and the supported `query`/`count` parameters. |
| 4 | `oc_tools_multi_agent_sandbox_tools.md` | procedure | `tools/multi-agent-sandbox-tools`: Configuration examples, Configuration precedence (Sandbox config, Tool restrictions), Migration from single agent, Tool restriction examples, Common pitfall "non-main", Testing, Troubleshooting | 750 | Per-agent sandbox and tool-policy overrides in a multi-agent gateway — worked `agents.list[]` examples, the sandbox + 8-step tool-filtering precedence chain (restrict-only, never grant-back), per-agent `agentDir` auth scoping, the `non-main` pitfall, and testing/troubleshooting commands. |
| 5 | `oc_tools_music_generation.md` | procedure | `tools/music-generation`: Quick start, Supported providers + Capability matrix, Tool parameters, Async behavior + Task lifecycle, Configuration (Model selection, Provider selection order), Provider notes, Choosing the right path, Provider capability modes, Live tests | 750 | Generating music with the `music_generate` tool — shared-provider vs ComfyUI-workflow quick starts, the provider/model table, tool parameters, the background-task async lifecycle (queued/running/succeeded/failed), `musicGenerationModel` selection order + failover, and provider `generate`/`edit` capability modes. |
| 6 | `oc_tools_ollama_search.md` | procedure | `tools/ollama-search`: Setup, Config, Notes | 450 | Configuring Ollama Web Search as a key-free (local/self-hosted) or hosted (`OLLAMA_API_KEY` against `ollama.com`) `web_search` provider — `ollama signin`, the `tools.web.search.provider: "ollama"` + base-URL reuse from the model provider, bearer-auth reuse, and the local-proxy vs hosted-endpoint behavior. |
| 7 | `oc_tools_parallel_search.md` | procedure | `tools/parallel-search`: Install plugin, API key (paid provider), Config, Base URL override, Tool parameters, Notes | 550 | Configuring Parallel's two `web_search` providers (`parallel-free` key-free Search MCP and the paid `parallel` API), plugin install, `PARALLEL_API_KEY` + base-URL override, the `objective`/`search_queries`/`count`/`session_id`/`client_model` parameters, and the dense LLM-optimized excerpt/result-count behavior. |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_` (e.g. `tools/loop-detection` → `oc_tools_loop_detection.md`,
`tools/multi-agent-sandbox-tools` → `oc_tools_multi_agent_sandbox_tools.md`). One BB per note; 1 note per page.

## Section Coverage Map

```
tools/loop-detection.md  → note 1 (oc_tools_loop_detection)
├── (intro: two cooperating guardrails) ───────────── → note 1 Overview
├── ## Why this exists ─────────────────────────────── → note 1
├── ## Configuration block ─────────────────────────── → note 1
│   └── ### Field behavior (field table) ───────────── → note 1
├── ## Recommended setup ───────────────────────────── → note 1
├── ## Post-compaction guard ───────────────────────── → note 1
├── ## Logs and expected behavior ──────────────────── → note 1
└── ## Related (Card links → to03/to07/gw02) ───────── → note 1 Related Notes / References

tools/media-overview.md  → note 2 (oc_tools_media_overview)
├── (intro: tool-driven, provider-gated media) ─────── → note 2 Overview
├── ## Capabilities (6 Cards) ──────────────────────── → note 2 (link-out per-tool detail to siblings)
├── ## Provider capability matrix ──────────────────── → note 2
├── ## Async vs synchronous ────────────────────────── → note 2
├── ## Speech-to-text and Voice Call ───────────────── → note 2
├── ## Provider mappings ───────────────────────────── → note 2
└── ## Related (links → image/video/music/tts/nodes) ─ → note 2 Related Notes / References

tools/minimax-search.md  → note 3 (oc_tools_minimax_search)
├── (intro: MiniMax web_search via Token Plan) ─────── → note 3 Overview
├── ## Get a Token Plan credential ─────────────────── → note 3
├── ## Config ──────────────────────────────────────── → note 3
├── ## Region selection ────────────────────────────── → note 3
├── ## Supported parameters ────────────────────────── → note 3
└── ## Related (→ tools/web, providers/minimax) ────── → note 3 Related Notes / References

tools/multi-agent-sandbox-tools.md  → note 4 (oc_tools_multi_agent_sandbox_tools)
├── (intro + agentDir auth Warning) ────────────────── → note 4 Overview
├── ## Configuration examples (Ex1/2/2b/3) ─────────── → note 4
├── ## Configuration precedence ────────────────────── → note 4
│   ├── ### Sandbox config ──────────────────────────── → note 4
│   └── ### Tool restrictions (8-step order) ────────── → note 4
├── ## Migration from single agent ─────────────────── → note 4
├── ## Tool restriction examples ───────────────────── → note 4
├── ## Common pitfall: "non-main" ──────────────────── → note 4
├── ## Testing ─────────────────────────────────────── → note 4
├── ## Troubleshooting ─────────────────────────────── → note 4
└── ## Related (→ elevated/multi-agent/sandboxing) ── → note 4 Related Notes / References

tools/music-generation.md  → note 5 (oc_tools_music_generation)
├── (intro: music_generate, background-task model) ── → note 5 Overview
├── ## Quick start (shared / ComfyUI tabs) ─────────── → note 5
├── ## Supported providers ─────────────────────────── → note 5
│   └── ### Capability matrix ───────────────────────── → note 5
├── ## Tool parameters ─────────────────────────────── → note 5
├── ## Async behavior ──────────────────────────────── → note 5
│   └── ### Task lifecycle ──────────────────────────── → note 5
├── ## Configuration ───────────────────────────────── → note 5
│   ├── ### Model selection ─────────────────────────── → note 5
│   └── ### Provider selection order ────────────────── → note 5
├── ## Provider notes ──────────────────────────────── → note 5
├── ## Choosing the right path ─────────────────────── → note 5
├── ## Provider capability modes ───────────────────── → note 5
├── ## Live tests ──────────────────────────────────── → note 5
└── ## Related (→ tasks/comfy/models/providers) ────── → note 5 Related Notes / References

tools/ollama-search.md  → note 6 (oc_tools_ollama_search)
├── (intro: Ollama Web Search, key-free local) ────── → note 6 Overview
├── ## Setup ───────────────────────────────────────── → note 6
├── ## Config ──────────────────────────────────────── → note 6
├── ## Notes ───────────────────────────────────────── → note 6
└── ## Related (→ tools/web, providers/ollama) ────── → note 6 Related Notes / References

tools/parallel-search.md  → note 7 (oc_tools_parallel_search)
├── (intro: two Parallel providers) ────────────────── → note 7 Overview
├── ## Install plugin ──────────────────────────────── → note 7
├── ## API key (paid provider) ─────────────────────── → note 7
├── ## Config ──────────────────────────────────────── → note 7
├── ## Base URL override ───────────────────────────── → note 7
├── ## Tool parameters ─────────────────────────────── → note 7
├── ## Notes ───────────────────────────────────────── → note 7
└── ## Related (→ tools/web, exa, perplexity) ──────── → note 7 Related Notes / References
```
No orphaned sections: every H2/H3 of all 7 pages maps to a planned note. Per-tool media detail, sandbox
modes/backends, the Web-Search overview, and per-provider model/auth pages are **linked out** (planned siblings
in to03/to04/to08/gw05/nd01/nd02 + `providers/*` in pr04/pr05/pr06/pr08), never duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | No page exceeds 2,500 words (max = music-generation at 1,682 w) and none mixes building blocks. Per master "most reference pages = 1 note"; all 7 are single-BB, kept 1:1. The high-fence music-generation page stays 1 note but reproduces ≤6 of its 11 fences (see Density Re-Assessment). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (6,727 measured words, 22 code fences). New `oc_*` notes: **7**. New `term_dictionary`
  notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×6** (notes 1, 3, 4, 5, 6, 7) · **concept ×1** (note 2 media-overview — a
  capability index, not a task). No model/argument notes in this sub-plan.
- Est. digest words: **~4,300** (avg ~615/note); all notes ≤750 words, ≤6 code blocks, single BB — within caps.
- Cross-refs (LOCKED at xref-augment 2026-06-21): see **Per-Note Related Notes Mapping** below — each note
  carries **≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `documentation/`** (plus relevant
  (this series / other OpenClaw-docs sub-plans) are clearly marked "(planned, …)".

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** >=8 terms · >=10 snippets · >=10 docs per note, relevance-selected (source re-read 2026-06-21),
> docs; the remaining slots are sibling `oc_*` (this series) / other planned OpenClaw-docs siblings marked
> "(planned, …)". Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`:
> term `../../term_dictionary/…`, snippet `../../code_snippets/…`, other doc `../<folder>/…`, repo
> `../../../areas/code_repos/…`, sibling `oc_Y.md`, entry `../../../0_entry_points/entry_openclaw_docs.md`.

### oc_tools_loop_detection (8t · 12s · 11d)

**Terms**
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — fail-fast pattern that trips after a threshold of failures; relevance: `globalCircuitBreakerThreshold` is the global no-progress breaker across all detectors.
- [Compaction](../../term_dictionary/term_compaction.md) — context-overflow summarization/retry of agent history; relevance: the post-compaction guard arms after every compaction-retry and aborts persistent loops.
- [Context Window](../../term_dictionary/term_context_window.md) — bounded token budget for a model turn; relevance: the guard exists to break the context-overflow → compaction → same-loop cycle from running unbounded.
- [Context Compression](../../term_dictionary/term_context_compression.md) — shrinking conversation state to fit the window; relevance: compaction-retry is the compression event that arms the guard.
- [Retry Pattern](../../term_dictionary/term_retry_pattern.md) — bounded re-attempt of a failed operation; relevance: detectors block repeated no-progress retries (unknown-tool, same-result) before they spin forever.
- [Idempotency](../../term_dictionary/term_idempotency.md) — operation producing the same effect when repeated; relevance: the guard fires only on byte-identical `(tool, argsHash, resultHash)` triples within the window.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: detectors operate on the rolling tool-call history of `(tool, args, result)` invocations.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of callable agent tools; relevance: `unknownToolThreshold` blocks repeated calls to an unregistered/unavailable tool.

**Docs**
- [Pi — Compaction & Branch Summarization Mechanics](../pi/pi_compaction.md) — Pi's compaction internals; relevance: parallel coding-agent's compaction event, the same trigger OpenClaw's post-compaction guard watches.
- [Pi — Custom Summarization via Extensions](../pi/pi_compaction_extensions.md) — extension-driven compaction; relevance: shows the compaction-retry hook that arms loop guards.
- [Agent SDK — The Context Window](../claude_code/cc_agent_sdk_context_window.md) — Claude Code context-budget management; relevance: the overflow condition that drives compaction → loop cycles.
- [Claude Code Hooks — Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — runtime guardrail hooks; relevance: peer guardrail surface for bounding agent tool behavior.
- [Claude Code — Performance and Stability Troubleshooting](../claude_code/cc_performance_and_stability.md) — diagnosing stuck/looping agents; relevance: same operator symptom ("agent stuck repeating") loop-detection addresses.
- [Hermes Agent — Context Compression and Caching](../hermes_agent/hermes_context_compression_caching.md) — Hermes compression path; relevance: cross-harness compaction analogue feeding the loop cycle.
- [Hermes Agent — Runtime & Context-Window Settings](../hermes_agent/hermes_runtime_context_settings.md) — runtime/context-window knobs; relevance: peer config surface for thresholds analogous to `loopDetection`.
- [oc_concepts_compaction](oc_concepts_compaction.md) — (planned, co02) the compaction concept note; relevance: the compaction event that arms the post-compaction guard.
- [oc_gateway_configuration_reference](oc_gateway_configuration_reference.md) — (planned, gw02) full config schema; relevance: the authoritative `tools.loopDetection` schema + merge semantics.
- [oc_tools_multi_agent_sandbox_tools](oc_tools_multi_agent_sandbox_tools.md) — (planned, this series) per-agent tool overrides; relevance: per-agent `tools.loopDetection` override lives in the same `agents.list[].tools` block.
- [oc_tools_thinking](oc_tools_thinking.md) — (planned, to07) reasoning-effort levels; relevance: the page's own Related card — reasoning effort interacts with loop-prone behavior.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: hosts `tool-loop-detection.ts` and `context-window-guard.ts` that implement this page.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — per-session/run state; relevance: run-id history scoping so fresh runs do not inherit stale loop counts.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: where the `post-compaction guard armed` and loop-event log lines surface.

**Snippets**
- [OpenClaw tool-loop-detection.ts — Circuit Breaker + PingPong Detector](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — the breaker + ping-pong detector code; relevance: direct implementation of `globalCircuitBreakerThreshold` + `detectors.pingPong`.
- [OpenClaw tool-loop-detection.ts — Repeat + Poll Detectors + History Scoping](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_repeat.md) — generic-repeat + known-poll detectors; relevance: implements `detectors.genericRepeat` / `knownPollNoProgress` + `historySize` scoping.
- [OpenClaw context-window-guard.ts — 4-Source Resolver and Threshold Model](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — overflow-threshold resolver; relevance: the context-overflow detection that precedes compaction → guard.
- [OpenClaw compaction.ts (2/2) — Identifier Preservation and Leader-Handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction retry internals; relevance: the compaction-retry that arms the post-compaction guard.
- [OpenClaw compaction.ts — Chunk Safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk guards; relevance: companion compaction-path code that feeds the loop-persisted check.
- [Hermes conversation_loop — Retry Handler](../../code_snippets/snippet_hermes_agent_core_conversation_loop_retry_handler.md) — bounded retry in the agent loop; relevance: cross-harness analogue of no-progress retry bounding.
- [Hermes conversation_loop — Context Overflow](../../code_snippets/snippet_hermes_agent_core_conversation_loop_context_overflow.md) — overflow recovery; relevance: the overflow → compaction trigger this guard sits downstream of.
- [Hermes conversation_loop — Post Error Hints](../../code_snippets/snippet_hermes_agent_core_conversation_loop_post_error_hints.md) — post-error guidance injection; relevance: peer mechanism for steering an agent out of repeated-error loops.
- [Hermes conversation_loop — Max Retries Exhausted](../../code_snippets/snippet_hermes_agent_core_conversation_loop_max_retries_exhausted.md) — terminal retry abort; relevance: analogue of the `compaction_loop_persisted` abort.
- [Hermes conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression decision logic; relevance: cross-harness compaction analogue.
- [Hermes trajectory_compressor — overlap suppression](../../code_snippets/snippet_hermes_agent_trajectory_overlap_suppression.md) — dedupes repeated trajectory steps; relevance: detecting/suppressing repeated identical tool steps mirrors generic-repeat detection.

### oc_tools_media_overview (8t · 13s · 11d)

**Terms**
- [Multimodal](../../term_dictionary/term_multimodal.md) — models/systems handling text+image+audio+video; relevance: the page is the index of OpenClaw's image/video/audio media capabilities.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesize speech from text; relevance: the `tts` tool + `messages.tts` synchronous capability listed in the matrix.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribe audio to text; relevance: batch STT + Voice Call streaming STT surfaces enumerated here.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live streaming transcription; relevance: Voice Call streaming STT forwards live phone audio to vendors without waiting for a recording.
- [Voice Call](../../term_dictionary/term_voice_call.md) — OpenClaw telephony/voice surface; relevance: the page distinguishes one-shot media tools from the Talk/Voice-Call live path.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model for image/audio synthesis; relevance: the backing generation tech for image/video/music providers in the matrix.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI vendors; relevance: the provider capability matrix enumerates 20+ external vendors per surface.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: vision-capable LLM providers do media understanding when set as the active reply model.

**Docs**
- [Hermes Agent — Built-in Tools Reference: Platform & Media](../hermes_agent/hermes_tools_reference_platform_media.md) — peer media tool catalog; relevance: the same image/video/tts/stt tool surface from the Hermes harness.
- [Hermes Agent — Voice Message Transcription (STT)](../hermes_agent/hermes_stt_transcription.md) — batch STT subsystem; relevance: directly mirrors the batch STT path in the matrix.
- [Hermes Agent — Text-to-Speech Provider Subsystem](../hermes_agent/hermes_tts_providers.md) — TTS provider layer; relevance: peer TTS capability + provider mapping.
- [Hermes Gateway Voice Reply & Discord Voice Channels](../hermes_agent/hermes_voice_gateway_discord_vc.md) — realtime voice reply; relevance: analogue of OpenClaw's realtime-voice / Voice Call surface.
- [Hermes Image Generation](../hermes_agent/hermes_image_generation.md) — image-gen subsystem; relevance: peer image-generation capability indexed in the matrix.
- [Claude Code — Voice Dictation](../claude_code/cc_voice_dictation.md) — STT dictation in a coding agent; relevance: cross-harness STT capability comparison.
- [Hermes Agent — Built-in Tools Reference: Toolsets](../hermes_agent/hermes_toolsets_reference.md) — full tool taxonomy; relevance: how media tools sit among the agent's tool surfaces.
- [oc_nodes_media_understanding](oc_nodes_media_understanding.md) — (planned, nd02) inbound media understanding; relevance: the "Media understanding" capability card links here.
- [oc_nodes_talk](oc_nodes_talk.md) — (planned, nd02) live speech contract; relevance: the Talk session contract that live speech uses instead of one-shot media tools.
- [oc_tools_tts](oc_tools_tts.md) — (planned, to08) the `tts` tool detail; relevance: per-tool detail this index links out to.
- [oc_tools_music_generation](oc_tools_music_generation.md) — (planned, this series) the `music_generate` tool; relevance: one of the media tools indexed here, on the shared async lifecycle.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/TTS/STT extensions; relevance: the provider plugins behind the TTS/STT/voice columns of the matrix.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM/media provider registry; relevance: registers the multimodal providers that gate each media tool's appearance.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony/Voice Call path; relevance: the streaming STT / live-audio surface distinguished from batch media.

**Snippets**
- [OpenClaw media-stream.ts — Realtime Transcription Wiring (2/3)](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — Voice Call streaming STT wiring; relevance: the streaming-STT surface in the matrix.
- [OpenClaw media-stream.ts — Bidirectional Mu-Law Audio (1/3)](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — live audio relay; relevance: the realtime-voice audio path the page contrasts with batch media.
- [OpenClaw talk-transcription-relay.ts — STT Session Lifecycle + Audio Relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — Talk-mode STT relay; relevance: implements the Talk session contract for live speech.
- [OpenClaw swabble/ — Speech Pipeline Orchestrator](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline orchestrator; relevance: the realtime/stt-tts modes shared with telephony/meetings.
- [OpenClaw extensions/elevenlabs — TTS Speech Provider](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: a TTS provider plugin in the matrix.
- [OpenClaw extensions/deepgram — Streaming STT Provider](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram streaming STT; relevance: a Voice-Call streaming-STT provider in the matrix.
- [OpenClaw MLXAudioTTS — Apple Silicon On-Device TTS Daemon](../../code_snippets/snippet_openclaw_mlx_tts.md) — local TTS daemon; relevance: the Local CLI TTS provider row.
- [Hermes tools/tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: peer TTS routing among providers.
- [Hermes tools/transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — STT transcription tool; relevance: peer batch-STT media path.
- [Hermes tools/image_generation_tool — _submit_fal_request](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen submission; relevance: the async image-generation capability indexed here.
- [Hermes tools/video_generation_tool — provider resolution](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: the async video-generation capability indexed here.
- [Hermes plugins/video_gen/xai — constants](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video provider dispatch; relevance: provider-gated video surface.
- [Hermes tools/send_message_tool — text_kwargs](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — outbound media attachment; relevance: the `message(action="send")` completion path that delivers generated media.

### oc_tools_minimax_search (8t · 10s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity/credentials; relevance: Token-Plan key / env-alias credential resolution (`MINIMAX_CODE_PLAN_KEY` etc.).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential from an OAuth flow; relevance: `MINIMAX_OAUTH_TOKEN` satisfies the MiniMax Search bearer credential.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored per-provider credential record; relevance: OAuth `minimax-portal` provider base URL is used as a region hint for the search credential.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI vendor; relevance: MiniMax is an external search/GenAI vendor integrated as a provider.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: `web_search` is the agent tool MiniMax backs.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server that forwards to an upstream host; relevance: `MINIMAX_API_HOST` / baseUrl acts as the CN/global region-hint routing target.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — front-door routing/host selection; relevance: CN (`api.minimaxi.com`) vs global (`api.minimax.io`) host selection order.
- [LLM](../../term_dictionary/term_llm.md) — large language model service; relevance: MiniMax fronts an LLM/search service whose Token-Plan endpoint returns structured results.

**Docs**
- [Hermes Agent — Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — peer web-search subsystem; relevance: the generic `web_search` contract a provider like MiniMax plugs into.
- [Hermes Agent — Building a Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — search-provider plugin authoring; relevance: how a `web_search` provider (MiniMax) is registered.
- [Hermes Agent — Environment Variables: Providers, Auth & Tool APIs](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: the env-alias credential pattern mirrors `MINIMAX_*` keys.
- [Hermes Agent — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — base-URL/host routing; relevance: region/host resolution analogous to `MINIMAX_API_HOST` ordering.
- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — provider credential resolution; relevance: cross-harness env-alias / OAuth credential resolution model.
- [oc_tools_web](oc_tools_web.md) — (planned, to08) Web-Search overview; relevance: all providers + auto-detection + the generic `web_search` contract.
- [oc_providers_minimax](oc_providers_minimax.md) — (planned, pr05) MiniMax provider; relevance: MiniMax model/image/speech/auth setup the search config reuses.
- [oc_tools_ollama_search](oc_tools_ollama_search.md) — (planned, this series) sibling search provider; relevance: another `web_search` provider with the same `tools.web.search.provider` switch.
- [oc_tools_parallel_search](oc_tools_parallel_search.md) — (planned, this series) sibling search provider; relevance: another `web_search` provider selection path.
- [oc_gateway_secrets](oc_gateway_secrets.md) — (planned, gw05) gateway secret handling; relevance: where `MINIMAX_*` keys live (`~/.openclaw/.env`).

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/plugin registry; relevance: registers the `minimax` provider id (web search + model surfaces).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin entries; relevance: the `plugins.entries.minimax.config.webSearch` plugin config lives here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime/env; relevance: the Gateway environment where `MINIMAX_CODE_PLAN_KEY` is read.

**Snippets**
- [OpenClaw extensions/openrouter — Aggregator Provider](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider plugin shape; relevance: the `extensions/<provider>` plugin pattern MiniMax follows.
- [OpenClaw plugin-sdk — Entry Factory Helpers](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `plugins.entries` factory; relevance: the entry/config wiring for `plugins.entries.minimax`.
- [OpenClaw provider openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider auth/baseUrl resolution; relevance: provider baseUrl/region resolution analogue.
- [OpenClaw model-catalog.ts — Three-Source Catalog Assembler](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — provider discovery; relevance: how registered providers (incl. minimax) are discovered.
- [OpenClaw runtime.ts — RuntimeEnv Type Contract](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env-var typing; relevance: the Gateway-environment read path for `MINIMAX_*` aliases.
- [Hermes plugins/web/tavily — capability-flag docstring](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web-search provider plugin; relevance: the `web_search` provider plugin pattern.
- [Hermes tools/web_tools — process_content_with_llm](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web-search tool result handling; relevance: result post-processing analogue to MiniMax's structured results.
- [Hermes hermes_cli/tools_config — Provider Setup Flow](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — interactive provider setup; relevance: analogue of `openclaw configure --section web`.
- [Hermes hermes_cli/tools_config — Per-Tool Provider Config Schema](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — per-tool provider schema; relevance: the `tools.web.search.provider` config shape.
- [Hermes agent/redact.py — Vendor-Prefix Token Table](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret masking incl. `sk-`/vendor prefixes; relevance: protecting `sk-cp-…` Token-Plan keys in logs.

### oc_tools_multi_agent_sandbox_tools (8t · 12s · 10d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: per-agent `sandbox.mode`/`scope` overrides are the page's core subject.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — concrete isolation engine (Docker etc.); relevance: `sandbox.docker.*` per-agent overrides and one-container-per-agent behavior.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: `mode: "all"` runs each agent in its own Docker container (`docker ps --filter name=openclaw-sbx-`).
- [Deny First](../../term_dictionary/term_deny_first.md) — restrict-by-default policy posture; relevance: the 8-step filter can only further restrict, never grant back denied tools.
- [Authentication](../../term_dictionary/term_authentication.md) — credential scoping; relevance: each agent has its own `agentDir` auth store; never reuse across agents.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — refreshable bearer credential; relevance: OAuth refresh tokens are NOT cloned into secondary agent auth stores.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of callable tools; relevance: `tools.allow`/`deny` + `group:*` shorthands filter which registered tools an agent can call.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: the empty-allowlist guard stops the run rather than degrade to a text-only agent.

**Docs**
- [Hermes Agent — Tool Gateway / Nous Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — tool policy/gateway layer; relevance: peer allow/deny tool-policy surface for an agent gateway.
- [Working With Subagents](../claude_code/cc_work_with_subagents.md) — isolated subagent runs; relevance: subagent tool-policy is the 8th precedence level (`tools.subagents.tools`).
- [Claude Code Hooks — Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — restricting agent tool behavior; relevance: cross-harness allow/deny guardrail pattern.
- [Pi — Sessions](../pi/pi_sessions.md) — session keying; relevance: `non-main` mode keys off `session.mainKey`, so group sessions get sandboxed.
- [Hermes Agent — Cloud & First-Class Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — provider scoping; relevance: per-agent provider tool-policy (`tools.byProvider[provider]`) levels.
- [oc_gateway_sandboxing](oc_gateway_sandboxing.md) — (planned, gw05) full sandbox reference; relevance: backends, scopes, modes, images the per-agent overrides specialize.
- [oc_gateway_sandbox_vs_tool_policy_vs_elevated](oc_gateway_sandbox_vs_tool_policy_vs_elevated.md) — (planned, gw05) "why is this blocked?"; relevance: the debugging companion + `group:*` tool-groups shorthands.
- [oc_tools_elevated](oc_tools_elevated.md) — (planned, to03) elevated exec; relevance: `agents.list[].tools.elevated` per-agent elevated restriction.
- [oc_concepts_multi_agent](oc_concepts_multi_agent.md) — (planned, co05) multi-agent routing; relevance: the routing/bindings model agents are matched through.
- [oc_tools_loop_detection](oc_tools_loop_detection.md) — (planned, this series) per-agent `tools.*` overrides; relevance: loop detection is another per-agent `agents.list[].tools` override.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — multi-agent runtime; relevance: implements `agents.defaults`/`agents.list[]` merge + per-agent tool policy.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox + policy enforcement; relevance: hosts `tool-policy.ts`, `exec-filesystem-policy.ts`, dangerous-tool deny.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session-scoped containers; relevance: `scope: "session"` vs `"agent"` container lifetime + send-policy gating.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway config + routing; relevance: config merge and `[tools] filtering tools for agent` log lines.

**Snippets**
- [OpenClaw tool-policy.ts — Runtime Authorization + Owner-Only Gates](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — runtime tool authorization; relevance: directly implements the allow/deny + per-agent restriction chain.
- [OpenClaw exec-filesystem-policy.ts — Drift Detection Rules](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: `workspaceAccess: "ro"/"none"` filesystem controls for read-only agents.
- [OpenClaw dangerous-tools.ts — Gateway HTTP Tool Deny Constant](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — default deny list; relevance: the gateway-tier deny set the per-agent policy further restricts.
- [OpenClaw send-policy.ts — Rule-Based Outbound Message Gating](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — cross-context send gating; relevance: implements `message.crossContext.allowWithinProvider/allowAcrossProviders`.
- [OpenClaw acp-spawn.ts — Spawn Policy Orchestration + Delivery](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — agent spawn policy; relevance: how a secondary agent is spawned under its own policy/sandbox.
- [OpenClaw thread-bindings-policy.ts — Spawn and Idle Policy Model](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — binding spawn policy; relevance: the `bindings[]` that route a peer/group to a restricted agent.
- [OpenClaw binding-routing.ts — Declarative + Runtime Route Rewrite](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding routing; relevance: implements `bindings[].match.{provider,peer}` agent resolution.
- [OpenClaw channel-config.ts — Three-Tier Match Resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match precedence; relevance: the precedence model for resolving which agent a message hits.
- [Hermes tools/environments/docker — find_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker sandbox backend; relevance: the container-per-agent backend implementation.
- [Hermes tools/code_execution_tool — check_sandbox_requirements](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandbox gating for exec; relevance: combining shell `exec` with sandbox filesystem controls.
- [Hermes agent/auxiliary_client — auth resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — per-context auth resolution; relevance: read-through-to-default auth-profile scoping analogue.

### oc_tools_music_generation (8t · 11s · 11d)

**Terms**
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model for audio/image synthesis; relevance: the backing tech for Lyria / ace-step / stable-audio music backends.
- [Generative Model](../../term_dictionary/term_generative_model.md) — model that synthesizes new content; relevance: `music_generate` produces novel audio tracks from prompts.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI vendors; relevance: ComfyUI/fal/Google/MiniMax/OpenRouter are the configured external providers.
- [Failover](../../term_dictionary/term_failover.md) — switch to a backup on failure; relevance: provider selection order tries the next candidate automatically when one fails.
- [Model Router](../../term_dictionary/term_model_router.md) — selects model/provider per request; relevance: `musicGenerationModel.primary`/`fallbacks` + auto-detection routing.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — enumerable registry of models/providers; relevance: `action: "list"` inspects available shared providers and models at runtime.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: `music_generate` is the agent tool (auto-called, no allow-listing).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the OpenRouter path uses chat-completions audio output with streaming.

**Docs**
- [Hermes Agent — Provider Routing](../hermes_agent/hermes_provider_routing.md) — provider selection/order; relevance: peer primary/fallback provider selection model.
- [Hermes Agent — Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — automatic provider failover; relevance: the `fallbacks[]` + auto-detect-on-failure behavior.
- [Hermes Agent — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model/provider catalog; relevance: analogue of `action=list` provider/model enumeration.
- [Hermes Agent — Building a Video Generation Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — media-gen provider plugin authoring; relevance: same `generate`/`edit` capability-mode contract as music providers.
- [Hermes Image Generation](../hermes_agent/hermes_image_generation.md) — async media-gen tool; relevance: the shared async media-generation task lifecycle music shares.
- [Hermes Agent — Google Gemini Provider Setup](../hermes_agent/hermes_provider_google_gemini.md) — Google/Gemini auth; relevance: the Google Lyria provider auth (`GEMINI_API_KEY`/`GOOGLE_API_KEY`).
- [oc_automation_tasks](oc_automation_tasks.md) — (planned, au01) background-task tracking; relevance: the task ledger (`openclaw tasks list/show/cancel`) that tracks detached `music_generate`.
- [oc_concepts_models](oc_concepts_models.md) — (planned, co04) model config + failover; relevance: the model-configuration/failover concept music selection builds on.
- [oc_providers_comfy](oc_providers_comfy.md) — (planned, pr02) ComfyUI provider; relevance: the workflow-graph music path.
- [oc_providers_openrouter](oc_providers_openrouter.md) — (planned, pr06) OpenRouter provider; relevance: the chat-completions audio music path.
- [oc_tools_media_overview](oc_tools_media_overview.md) — (planned, this series) media index; relevance: the capability index that points to `music_generate`.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — music/media provider registry; relevance: registers the ComfyUI/fal/Google/MiniMax/OpenRouter music providers.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: background-task wake + completion-event injection back into the session.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/task ledger; relevance: session-backed async task tracking + duplicate-prevention while queued/running.

**Snippets**
- [OpenClaw model-fallback.ts — Failover Ladder Entry and Summary Envelope](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — failover ladder; relevance: the primary → fallbacks → auto-detect selection order.
- [OpenClaw model-fallback.ts — Cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — failover cooldown; relevance: provider-failure handling before trying the next candidate.
- [OpenClaw failover-error.ts — Typed FailoverError and Signal Classifier](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error typing; relevance: the per-attempt error details surfaced when all providers fail.
- [OpenClaw model-catalog.ts — Three-Source Catalog Assembler with Plugin Discovery](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model/provider discovery; relevance: how `action=list` discovers registered music providers/models.
- [OpenClaw extensions/openrouter — Aggregator Provider](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter provider; relevance: the OpenRouter music path (chat-completions audio).
- [OpenClaw manager.core.ts — Detached Task Runtime (4/4)](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached background task runtime; relevance: the background-task model `music_generate` runs under.
- [Hermes tools/image_generation_tool — _submit_fal_request](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — fal media submission; relevance: the fal provider path (`fal-ai/minimax-music`).
- [Hermes plugins/image_gen/openai — virtual-model catalog](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — media provider dispatch; relevance: provider/model dispatch analogue for media generation.
- [Hermes plugins/model-providers/openrouter — build_extra_body](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter request build; relevance: OpenRouter audio-output request construction.
- [Hermes tools/send_message_tool — text_kwargs](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — outbound attachment; relevance: the completion-wake `message(action="send")` that posts the finished track.

### oc_tools_ollama_search (8t · 10s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — caller credential verification; relevance: `ollama signin` + bearer-auth reuse from the model provider.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — forward to an upstream host; relevance: the local proxy `/api/experimental/web_search` signs and forwards to Ollama Cloud.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — front-door routing; relevance: local-daemon-vs-`ollama.com` endpoint selection + forwarding.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI; relevance: the hosted `ollama.com` web-search API path with `OLLAMA_API_KEY`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: `web_search` is the agent tool Ollama backs.
- [LLM](../../term_dictionary/term_llm.md) — local/hosted model host; relevance: Ollama is the local model host whose configured host is reused for web search.
- [Model Router](../../term_dictionary/term_model_router.md) — host/base-URL resolution; relevance: base-URL resolution + fallback to the hosted endpoint when the local host lacks web search.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — selecting/configuring a provider; relevance: explicit `tools.web.search.provider: "ollama"` selection (no auto-select).

**Docs**
- [Hermes Agent — Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — web-search subsystem; relevance: the generic `web_search` contract Ollama plugs into.
- [Hermes Agent — Building a Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — search-provider plugin authoring; relevance: how a bundled `web_search` provider registers.
- [Hermes Agent — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — base-URL/host routing; relevance: the `baseUrl` reuse from `models.providers.ollama` for web search.
- [Hermes Agent — Environment Variables: Providers, Auth & Tool APIs](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars; relevance: `OLLAMA_API_KEY` and host env config pattern.
- [Pi — Provider Authentication](../pi/pi_provider_auth.md) — provider credential resolution; relevance: cross-harness bearer/host credential reuse model.
- [oc_tools_web](oc_tools_web.md) — (planned, to08) Web-Search overview; relevance: all providers + auto-detection (Ollama is NOT auto-selected).
- [oc_providers_ollama](oc_providers_ollama.md) — (planned, pr06) Ollama provider; relevance: Ollama model setup + cloud/local modes whose host this reuses.
- [oc_gateway_secrets](oc_gateway_secrets.md) — (planned, gw05) gateway secrets; relevance: where `OLLAMA_API_KEY` / host config lives.
- [oc_tools_minimax_search](oc_tools_minimax_search.md) — (planned, this series) sibling search provider; relevance: same `tools.web.search.provider` switch, paid/key path.
- [oc_tools_parallel_search](oc_tools_parallel_search.md) — (planned, this series) sibling search provider; relevance: another `web_search` provider selection path.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/plugin registry; relevance: registers the `ollama` provider id (model + web-search surfaces).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin entries; relevance: `plugins.entries.ollama.config.webSearch.baseUrl` plugin config.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime/env; relevance: gateway host config + reachability warning during setup.

**Snippets**
- [OpenClaw extensions/ollama — Local-LLM Provider](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: the local host (`http://127.0.0.1:11434`) whose config web search reuses.
- [Hermes plugins/model-providers/ollama-cloud — Ollama Cloud HOSTED provider](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — hosted Ollama Cloud provider; relevance: the `https://ollama.com` hosted path with bearer API-key auth.
- [OpenClaw plugin-sdk — Entry Factory Helpers](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `plugins.entries` factory; relevance: the `plugins.entries.ollama` web-search config wiring.
- [OpenClaw extensions/openrouter — Aggregator Provider](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider plugin shape; relevance: the provider-plugin pattern Ollama follows.
- [OpenClaw runtime.ts — RuntimeEnv Type Contract](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env-var typing; relevance: the `OLLAMA_API_KEY` / host env read path.
- [OpenClaw model-catalog.ts — Three-Source Catalog Assembler](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — provider discovery; relevance: discovery of the `ollama` provider for reuse by web search.
- [Hermes plugins/web/tavily — capability-flag docstring](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web-search provider plugin; relevance: the bundled `web_search` provider pattern.
- [Hermes tools/web_tools — process_content_with_llm](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web-search result handling; relevance: structured-result (title/URL/snippet) handling analogue.
- [Hermes hermes_cli/tools_config — Provider Setup Flow](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — interactive provider setup; relevance: analogue of `openclaw configure --section web` selecting Ollama.
- [Hermes hermes_cli/tools_config — Per-Tool Provider Config Schema](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — per-tool provider schema; relevance: the `tools.web.search.provider` config shape.

### oc_tools_parallel_search (8t · 10s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — caller credential verification; relevance: the paid `parallel` provider needs `PARALLEL_API_KEY` (free `parallel-free` needs none).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: `parallel-free` is Parallel's hosted Search MCP (`https://search.parallel.ai/mcp`).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI/search vendor; relevance: Parallel is an external web-index vendor built for AI agents.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: `web_search` with `objective`/`search_queries` parameters is the agent tool.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — forward to an upstream host; relevance: base-URL override routes requests through a compatible proxy (e.g. Cloudflare AI Gateway).
- [API Gateway](../../term_dictionary/term_api_gateway.md) — front-door routing/caching; relevance: the resolved endpoint is part of the per-endpoint search cache key.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — capping request throughput; relevance: the paid `parallel` provider offers higher rate limits than `parallel-free`.
- [LLM](../../term_dictionary/term_llm.md) — large language model consumer; relevance: results are ranked/compressed for LLM reasoning utility (dense excerpts), not human click-through.

**Docs**
- [Hermes Agent — Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — web-search subsystem; relevance: the generic `web_search` contract excerpts/description map onto.
- [Hermes Agent — Building a Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — search-provider plugin authoring; relevance: how `@openclaw/parallel-plugin` registers two providers.
- [Hermes Agent — X (Twitter) Search](../hermes_agent/hermes_x_search_grok.md) — vendor-specific search provider; relevance: peer external-vendor `web_search` provider with its own params.
- [Hermes Agent — Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — base-URL/proxy routing; relevance: the compatible-proxy base-URL override behavior.
- [Hermes Agent — Environment Variables: Providers, Auth & Tool APIs](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `PARALLEL_API_KEY` env-config pattern.
- [oc_tools_web](oc_tools_web.md) — (planned, to08) Web-Search overview; relevance: all providers + auto-detection (incl. OpenAI Responses bypass note).
- [oc_tools_exa_search](oc_tools_exa_search.md) — (planned, to03) Exa neural search; relevance: the page's own Related card — sibling neural-search tool.
- [oc_tools_perplexity_search](oc_tools_perplexity_search.md) — (planned, to06) Perplexity search; relevance: the page's own Related card — sibling structured-search tool.
- [oc_tools_minimax_search](oc_tools_minimax_search.md) — (planned, this series) sibling search provider; relevance: another `web_search` provider selection path.
- [oc_tools_ollama_search](oc_tools_ollama_search.md) — (planned, this series) sibling search provider; relevance: another `web_search` provider selection path.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin install/registration; relevance: `openclaw plugins install @openclaw/parallel-plugin` registers the two providers.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — search-provider registry; relevance: the `web_search` provider registry the plugin plugs into.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime/env; relevance: `openclaw gateway restart` + `PARALLEL_API_KEY` env + result cache (15 min default).

**Snippets**
- [Hermes plugins/web/tavily — capability-flag docstring](../../code_snippets/snippet_hermes_agent_plugins_web.md) — bundled web-search provider; relevance: the `web_search` provider plugin pattern Parallel follows.
- [Hermes tools/web_tools — process_content_with_llm](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — result post-processing; relevance: joining `excerpts` into `description` for the generic contract.
- [OpenClaw plugin-sdk — Entry Factory Helpers](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — `plugins.entries` factory; relevance: the `plugins.entries.parallel.config.webSearch` config wiring.
- [OpenClaw extensions/openrouter — Aggregator Provider](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider plugin shape; relevance: the installable provider-plugin pattern.
- [OpenClaw runtime.ts — RuntimeEnv Type Contract](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env-var typing; relevance: the `PARALLEL_API_KEY` env read path.
- [OpenClaw server.impl.ts — Config Snapshot + Lazy Modules + Plugin Wiring](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin wiring on startup; relevance: how an installed plugin is wired after `gateway restart`.
- [OpenClaw model-catalog.ts — Three-Source Catalog Assembler with Plugin Discovery](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — plugin discovery; relevance: discovery of installed plugin providers.
- [Hermes acp_adapter/tools.py — Tool Registration + Kind Mapping](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration; relevance: how a tool/provider exposes its parameter shape (`objective`/`search_queries`).
- [Hermes hermes_cli/tools_config — Provider Setup Flow](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — interactive provider setup; relevance: analogue of `openclaw configure --section web` for the paid key.
- [Hermes hermes_cli/tools_config — Per-Tool Provider Config Schema](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — per-tool provider schema; relevance: the `tools.web.search.{provider,maxResults}` config shape.

**DB verification (2026-06-21):** every EXISTING note_id cited above — **127 distinct existing targets**
(terms + snippets + docs + repos across the 7 notes; 154 distinct links total, 27 of them planned siblings /
**Absent (NOT cited as existing):** `term_session`, `term_web_search`, `term_async`, `term_bearer_token`,
`term_guardrails`, `term_agentic_workflow`, `term_voice_agent`, `term_telephony`, `term_container`,
`term_task_queue`, `term_background_job`, `term_polling`, `term_environment_variable` — replaced by
`term_generative_model`, `term_auth_profile`, etc.). `entry_openclaw_docs.md` is created as a master W1
pre-step — cited as the entry back-link, not yet in DB at plan time.

## Undigested Terms Plan (Step 4e)

Per the master design decision, OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT as
new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms. This
sub-plan expects **0 new `term_dictionary` captures**.

| Term (source vocabulary) | Disposition |
|---|---|
| loop detection / post-compaction guard | Digested as note 1 (`oc_tools_loop_detection`); link `term_circuit_breaker`, `term_guardrails`, `term_compaction`. No new term. |
| circuit breaker / `globalCircuitBreakerThreshold` | Link existing `term_circuit_breaker`. No new term. |
| compaction / context-overflow retry | Link existing `term_compaction` + `term_context_window`. No new term. |
| media generation / media understanding | Digested as note 2 (`oc_tools_media_overview`); link `term_multimodal`, `term_diffusion_model`. No new term. |
| text-to-speech (TTS) / speech-to-text (STT) | Link existing `term_text_to_speech` / `term_speech_to_text`. No new term. |
| Talk mode / realtime voice / Voice Call | OpenClaw-specific feature → home in `oc_nodes_talk` (nd02) / `oc_tools_media_overview`; link `term_voice_call`. No new term. |
| `web_search` tool / web search provider | OpenClaw tool surface → home in `oc_tools_web` (to08, planned) + the three provider notes (3, 6, 7); link `term_function_calling`. No new `term_web_search` (currently absent, but a provider-config concept owned by doc notes, not a vault-reusable cross-cutting term). |
| MiniMax / Ollama / Parallel (provider names) | Documented as config in notes 3/6/7 + `oc_providers_*` (pr05/pr06); not promoted to term notes. Link `term_third_party_genai_services` / `term_llm`. No new term. |
| `music_generate` tool / `musicGenerationModel` | Digested as note 5; link `term_diffusion_model`, `term_failover`, `term_model_router`. No new term. |
| async task / task ledger / task lifecycle | Background-task vocabulary → home in `oc_automation_tasks` (au01) + note 5; link `term_idempotency`. No new term (`term_task_queue`/`term_background_job` absent but doc-owned, not promoted). |
| multi-agent sandbox / tool policy / precedence | Digested as note 4; link `term_sandbox`, `term_docker`, `term_tool_registry`. No new term. |
| `agentDir` / auth-profiles | OpenClaw config concept → note 4; link `term_authentication`, `term_oauth_token`. No new term. |
| Search MCP (`parallel-free`) | Link existing `term_mcp`. No new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an
existing note. (`term_web_search`, `term_async`, `term_task_queue`, `term_voice_agent`, `term_telephony` are
either provider-config concepts owned by `oc_*` doc notes or already covered by adjacent existing terms —
`term_function_calling`, `term_idempotency`, `term_voice_call`, `term_speech_to_text`.) Augment Step 2d
re-scans to confirm.

## Term-Note Authoring Requirements

**N/A for to05 — authors zero `term_dictionary` notes.** Inherited from master (Undigested Terms — Corpus-Wide
Inventory + Ownership). If augment's Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no
doc-page home AND no existing note, it would be captured via `/tessellum-capture-term-note` and added to its
acronym glossary per master W5 — but none is expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All gates must pass before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format (YAML field order + forbidden-field absence; H1/`## Overview`/`## Related Notes`/`## References`/bold footer; ≤400 lines, ≤2500 words, ≤6 code blocks, single BB) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (each note's claims diff against `inbox/openclaw_docs/tools/<page>.md`; no fabricated config keys/params) | manual diff vs mirror source |
| G3 | Density + Coverage (every mapped H2/H3 represented; no over-compression; within caps) | Section Coverage Map cross-check |
| G4 | Cross-Reference (≥6 relevance-selected term links + repo_openclaw*/sibling oc_* per note, each with relevance statement, indexed link format) | locked Related-Notes mapping (augment) |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note; planned siblings created in-series or redirected) | `/tessellum-fix-ghost-references` + DB existence check |
| G6 | Broken-link fix (relative paths resolve) | `/tessellum-fix-broken-links` |
| G7 | Discoverability (each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/`) | inlink mapping (via `entry_openclaw_docs.md` + repo/term inlinks) |
| G8 | In-degree ≥1 (anti-island) per new note | `note_links` query after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_loop_detection oc_tools_media_overview oc_tools_minimax_search oc_tools_multi_agent_sandbox_tools oc_tools_music_generation oc_tools_ollama_search oc_tools_parallel_search"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"
  done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_* link (SIBLING_PREFIX)
  grep -qE "\]\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$f" || echo "NO SIBLING oc_* LINK in $n"
  # density caps (≤2500 words body, ≤6 code blocks, ≤400 lines)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w | tr -d ' ')
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  lines=$(wc -l < "$f" | tr -d ' ')
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb lines=$lines)"
done

# YAML frontmatter validation across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G8: ghost + in-degree verification after incremental reindex
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "$indeg" -ge 1 ] || echo "ISLAND (in-degree 0): $n"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Fences in note | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_tools_loop_detection | procedure | 700 | 3 | ≤3 (default config block + per-agent override + guard block) | ✅ |
| 2 | oc_tools_media_overview | concept | 650 | 0 | 0 (matrices reproduced as markdown tables) | ✅ |
| 3 | oc_tools_minimax_search | procedure | 450 | 1 | ≤1 (config block) | ✅ |
| 4 | oc_tools_multi_agent_sandbox_tools | procedure | 750 | 1 | ≤3 (1–2 representative agent examples + tool-policy excerpt; precedence shown as prose/list) | ✅ |
| 5 | oc_tools_music_generation | procedure | 750 | 11 | ≤6 (model-selection + provider-order config + key CLI/`/tool` examples; drop redundant prompt/live-test fences, summarize as prose) | ✅ |
| 6 | oc_tools_ollama_search | procedure | 450 | 4 | ≤4 (signin + provider config + host-override/hosted blocks) | ✅ |
| 7 | oc_tools_parallel_search | procedure | 550 | 2 | ≤2 (install + config blocks) | ✅ |

No note approaches the 2,500-word / 400-line caps. The only fence-heavy page (music-generation, 11 fences)
stays a single note by reproducing ≤6 load-bearing snippets and summarizing the rest (example prompts, live-test
invocations) as prose. All other pages are at or below 6 fences natively.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before the first sub-plan
executes) under the **Tools** section (sub-plan to05). Each new note receives its entry-point back-link at
finalization (satisfies G7/G8 outside-folder inbound link). No standalone entry point is created by this
sub-plan; the master hub is the single navigation surface.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfy G7/G8). Each new note RECEIVES ≥1
inbound link from outside `documentation/openclaw/`:

- `entry_openclaw_docs.md` (master W1 pre-step) → **all 7 notes** (guaranteed outside-folder inbound).
- `repo_openclaw_agents` → notes 1, 4, 5 (agent runtime: loop detection, multi-agent sandbox, music task wake).
- `repo_openclaw_security` → note 4 (sandbox + tool-policy enforcement).
- `repo_openclaw_sessions` → notes 1, 4, 5 (per-run history scoping, session sandbox, task ledger).
- `repo_openclaw_gateway` → notes 1, 3, 4, 6, 7 (gateway log/config + env for search-provider keys).
- `repo_openclaw_extensions_llm_providers` → notes 2, 3, 5, 6, 7 (provider registry: media, MiniMax, music, Ollama, Parallel).
- `repo_openclaw_extensions` → notes 3, 6, 7 (plugin entry/install for the three search providers).
- `repo_openclaw_extensions_voice_speech` → note 2 (TTS/STT/media-understanding surface).
- `repo_openclaw_channels_voice_phone` → note 2 (Voice Call streaming STT path).
- `term_circuit_breaker` → note 1; `term_compaction` → note 1; `term_sandbox` / `term_docker` → note 4;
  `term_multimodal` → note 2; `term_diffusion_model` → notes 2, 5; `term_failover` → note 5;
  `term_mcp` → note 7; `term_third_party_genai_services` → notes 2, 3, 5, 6, 7.

## Pacing Rules (inherited from master)

One execution phase (7 notes, P2). Cap dynamic-workflow fan-out at ~30 agents/run. Re-read each source page
during execution; reproduce config/CLI snippets verbatim from the mirror. One BB per note; 8 gates pass before
commit. `git pull --rebase --autostash origin main` first; commit + push per wave; no Claude co-author trailer.
Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment — Related Notes locked at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21 (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this pass (xref-augment):** Re-read all 7 source pages under `inbox/openclaw_docs/tools/` and
replaced the plan-stage "Candidate Cross-References" with a LOCKED **Per-Note Related Notes Mapping** at the
raised floors **≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `documentation/`** per note

**What was locked — per-note counts (all floors met):**

| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met? |
|---|---:|---:|---|---:|---|
| oc_tools_loop_detection | 8 | 12 | 11 (7 / 4) | 3 | ✅ |
| oc_tools_media_overview | 8 | 13 | 11 (7 / 4) | 3 | ✅ |
| oc_tools_minimax_search | 8 | 10 | 10 (5 / 5) | 3 | ✅ |
| oc_tools_multi_agent_sandbox_tools | 8 | 12 | 10 (5 / 5) | 4 | ✅ |
| oc_tools_music_generation | 8 | 11 | 11 (6 / 5) | 3 | ✅ |
| oc_tools_ollama_search | 8 | 10 | 10 (5 / 5) | 3 | ✅ |
| oc_tools_parallel_search | 8 | 10 | 10 (5 / 5) | 3 | ✅ |

27 planned-sibling / entry-back-link references (marked "(planned, …)"). ALL snippets are existing
+ `_repeat` and `snippet_openclaw_agents_context_window_guard` are the literal implementation of note 1, and
`snippet_openclaw_agents_tool_policy` / `_security_*_policy` / `_sessions_send_policy` underpin note 4.

**New-term candidates: none.** The Undigested Terms Plan's "0 new term_dictionary captures" holds. Step-2d
re-scan during this pass surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home
captured: `term_guardrails`→`term_retry_pattern`/`term_idempotency`+`term_circuit_breaker`;
`term_agentic_workflow`→`term_function_calling`/`term_tool_registry`; `term_async`/`term_task_queue`/
`term_background_job`→`term_idempotency`+`term_model_catalog` (+ planned `oc_automation_tasks`);
`term_session`→`term_auth_profile`/`term_provider_routing` (+ `repo_openclaw_sessions`);
`term_bearer_token`→`term_authentication`/`term_oauth_token`. Best-fit glossary for any future capture would
be `acronym_glossary_gen_ai_dev.md` — **but none is required for to05.**

**Issues / notes:** (a) `entry_openclaw_docs.md` is cited as each note's outside-folder entry back-link but
does not yet exist in the DB — it is created as the master **W1** pre-step before the first sub-plan executes;
this is expected and is the G7/G8 discoverability anchor. (b) Sibling `oc_*` docs (this series + to03/to04/
to06/to08/co02/co04/co05/gw02/gw05/nd02/au01/pr02/pr05/pr06) do not exist yet; they count toward the 10-doc
real notes today. (c) multi-agent-sandbox-tools measures 677 body words (`wc -w`, YAML-stripped) vs the plan's
1,248 (raw page incl. JSX/JSON) — still single-BB and far under the 2,500-word cap, so no re-split.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of the augmented plan. CP7 source-word spot-check performed against the mirror
(`wc -w` on YAML-stripped bodies): loop-detection 927w, media-overview 1,086w, minimax 352w, multi-agent 677w,
music-generation 1,639w, ollama 466w, parallel 733w — all within the CP7 ±30% band of the Source table (and
all under the 2,500-word cap), so no under-estimation / re-split is triggered.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present with G5 ghost-detect, G6 broken-link-fix, G7/G8 discoverability + in-degree; Validation Scripts implement the ghost + in-degree checks. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "Entry Point Decision (inherited from master)": 7 rows into `entry_openclaw_docs.md` (master W1 pre-step) under Tools/to05; each new note gets the entry back-link at finalization. |
| CP4 | Plan size manageable | **PASS** | 7 notes, single execution phase — well under the ≤30 cap. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited verbatim from master Format Definition, derived from the existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) corpora; `## Overview` / source-body / `## Related Notes` / `## References` / bold footer; forbidden-field list present. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: max 750 est. words, ≤6 fences/note (music-generation reduces 11→≤6); no note approaches the 2,500-word / 400-line caps; no borderline cases. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Spot-checked all 7 pages (table above); measured within ±30% of the Source table, all < 2,500w cap. |
| CP8 | Undigested Terms Plan + Authoring Reqs | **PASS** | "Undigested Terms Plan (Step 4e)" table present with per-row disposition; "Term-Note Authoring Requirements" present (N/A — 0 term captures, with the conditional capture path stated); New-term candidates: none (re-confirmed this pass). |
| CP8f | Term-slug specificity + collision / all-notes dedup audit | **PASS** | Master dedup policy applied; no `oc_*` doc note duplicates an existing substantive term/doc/repo (each planned note maps 1:1 to a distinct source page; vocabulary linked, never re-defined). Absent slugs documented + routed to existing equivalents, not captured. |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | "Inlinks (existing → new notes)" maps every one of the 7 notes to ≥1 outside-folder inbound source (`entry_openclaw_docs` + repo/term inlinks); G8 in-degree ≥1 is a gated check in the Validation Scripts. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
