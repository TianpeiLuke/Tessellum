---
title: Hermes Agent Docs Digestion — Sub-Plan 08a — Media (Voice / TTS / STT / Vision / Image-Gen / Spotify / Deliverable)
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/voice-mode.md
  - user-guide/features/tts.md
  - user-guide/features/vision.md
  - user-guide/features/image-generation.md
  - user-guide/features/spotify.md
  - user-guide/features/deliverable-mode.md
---

# Sub-Plan 08a: Media (Voice / TTS / STT / Vision / Image-Gen / Spotify / Deliverable)

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP08a's note
> filenames/BBs/coverage are defined. **Part `a` of the SP08 split** (master Sub-Plans Index row 08
> "split a/b"): SP08a owns the media/voice/audio/visual surface; the web/browser/lsp/computer-use/skins/
> worker-lanes/tool-search/overview pages go to SP08b (the `b` half) — NOT this file.

## Scope

The audio + visual + artifact surface of Hermes Agent: real-time **voice conversations** (CLI
push-to-talk + Telegram/Discord auto-reply + Discord voice-channel listen-and-speak), the
**text-to-speech** provider subsystem (ten built-ins + command/Python-plugin providers), **voice-message
transcription (STT)**, **multimodal vision / image-paste**, FAL.ai **image generation**, the **Spotify**
toolset (PKCE OAuth, 7 tools, cron control), and **deliverable mode** (native file attachments in
messaging gateways). Source = 6 mirrored pages in `inbox/hermes_agent_docs/` (all substantive). **P2 /
features.** Downstream/upstream sub-plans link back: SP02 `hermes_messaging_media_settings` holds the
config blocks these notes document; SP11–13 messaging notes consume voice/TTS/deliverable delivery.

## Content Strategy

- **One BB per note.** `voice-mode.md` (2850w, 18 code) mixes a CLI-side procedure and a gateway/Discord-VC
  procedure → split 2. `tts.md` (4341w, 20 code) mixes a TTS-provider model + an STT transcription procedure
  → split 2. The four remaining pages are each one BB → 1 note each. Total **8 notes**.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the
  `config.yaml` `tts:` / `stt:` / `voice:` / `display:` blocks (SP02 `hermes_messaging_media_settings`),
  the Tool Gateway / Nous Portal billing path (SP05 `term_tool_gateway` / SP14 `term_nous_portal`),
  per-platform delivery threading (SP11–13 messaging), MCP server install for deliverable connectors
  (SP09 `hermes_mcp`), `execute_code` chart generation (SP06 `term_code_execution_tool`), kanban
  `kanban_complete` artifacts (SP06 `term_kanban_multi_agent`), the `auxiliary.vision` slot (SP02/SP09).
- **Collision (augment): `term_voice_wake.md` (10162b, active) is the UNRELATED wake-word/voice-activation
  concept**, NOT Hermes real-time voice mode — a master-listed LIKE false-positive (`voice mode ≠
  term_voice_wake`). The planned `term_voice_mode` is NOT a duplicate; capture it and LINK `term_voice_wake`
  only as a contrast term.
- **Collision: `term_realtime_transcription.md` (11060b, active) covers the generic real-time-transcription
  concept.** The planned `term_speech_to_text` documents Hermes' STT subsystem (provider fallback chain,
  command/plugin providers, gateway voice-message injection) — a different scope → LINK, do not drop.
- **Collision: Hermes `vision` ≠ generic `term_computer_vision.md` (13127b, active)** (master caution list).
  SP08a does NOT capture a vision term — the planned `hermes_vision_image_paste` doc note LINKS the existing
  `term_computer_vision` + `term_multimodal`.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — wc)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/tts.md | 4341 | 20 | MIXED model(TTS)+procedure(STT) | 2 (split) |
| user-guide/features/voice-mode.md | 2850 | 18 | MIXED procedure(CLI)+procedure(gateway/VC) | 2 (split) |
| user-guide/features/spotify.md | 2198 | 12 | procedure | 1 |
| user-guide/features/vision.md | 1606 | 8 | procedure | 1 |
| user-guide/features/image-generation.md | 1309 | 9 | procedure | 1 |
| user-guide/features/deliverable-mode.md | 850 | 1 | concept | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **8 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_voice_mode_cli.md` | procedure | voice-mode §Prerequisites, §Requirements (Python pkgs, system deps, API keys), §CLI Voice Mode (Quick Start, How It Works, Silence Detection, Streaming TTS, Hallucination Filter), §Configuration Reference (voice/stt/tts yaml, STT/TTS comparison), §Troubleshooting (CLI rows) | ~1400 | CLI/TUI push-to-talk voice: install extras + PortAudio/ffmpeg/Opus deps + STT keys, `/voice` slash commands, Ctrl+B record loop, two-stage silence detection, sentence-by-sentence streaming TTS, the 26-phrase Whisper hallucination filter, and the `voice:`/`stt:`/`tts:` config knobs. |
| 2 | `hermes_voice_gateway_discord_vc.md` | procedure | voice-mode §Gateway Voice Reply (Telegram & Discord) (Discord channels-vs-DMs, commands, modes, platform delivery), §Discord Voice Channels (bot permissions, gateway intents, opus, env vars, how-it-works, text-channel integration, echo prevention, access control), §Troubleshooting (gateway/VC rows) | ~1400 | Gateway voice: auto voice-reply on Telegram/Discord (`/voice on`/`tts`/`off` modes, Opus/OGG delivery), and the Discord voice-channel pipeline — re-invite permissions integer, three privileged intents, Opus codec, per-user SSRC mapping, listen→transcribe→agent→speak loop, echo prevention, `DISCORD_ALLOWED_USERS` access control. |
| 3 | `hermes_tts_providers.md` | model | tts §Text-to-Speech (10-provider table), §Platform Delivery, §Configuration (full yaml), §Gemini Persona Prompts, §Gemini Audio Tags, §Input length limits, §Telegram Voice Bubbles & ffmpeg, §xAI Custom Voices, §Piper, §Custom command providers (+Doubao, placeholders, optional keys, behavior, security), §Python plugin providers | ~2400 | The TTS subsystem model: ten built-in providers (Edge default → ElevenLabs/OpenAI/MiniMax/Mistral/Gemini/xAI/NeuTTS/KittenTTS/Piper) with quality/cost/key matrix + per-provider input caps + ffmpeg/Opus delivery; Gemini persona prompts + audio tags; xAI voice cloning; the command-type provider registry (placeholders/keys/security) and the `register_tts_provider()` Python plugin ABC. |
| 4 | `hermes_stt_transcription.md` | procedure | tts §Voice Message Transcription (STT) (provider table, zero-config), §Configuration (stt yaml), §Provider Details (local/groq/openai/mistral/xai/custom CLI + Doubao ASR), §Fallback Behavior, §STT custom command providers (placeholders, read-back, keys, behavior, security), §Python plugin providers (STT) (when-to-pick, resolution order, namespace, minimal plugin, hooks) | ~1700 | Voice-message transcription: auto-transcribe inbound voice on Telegram/Discord/WhatsApp/Slack/Signal, the local-faster-whisper default + Groq/OpenAI/Mistral/xAI cloud providers, the automatic fallback chain, the `stt.providers.<name>: type: command` registry (placeholders, transcript read-back, security), and the `register_transcription_provider()` plugin resolution order. |
| 5 | `hermes_vision_image_paste.md` | procedure | vision §How It Works, §Paste Methods (`/paste`, Ctrl/Cmd+V, `/terminal-setup`), §Platform Compatibility, §Platform-Specific Setup (macOS/X11/Wayland/WSL2), §SSH & Remote Sessions (+workarounds), §Why Terminals Can't Paste Images, §Supported Models, §Image Routing (vision-capable vs text-only), §`vision_analyze` dual behavior | ~1400 | Multimodal image paste into the CLI: `/paste` / Cmd+V layered-paste / `/terminal-setup`, per-OS clipboard tooling (osascript/xclip/wl-paste/powershell.exe), SSH limits + workarounds, base64 vision content blocks, and the automatic vision-capable-vs-text-only image routing (`vision_analyze` returns raw pixels or aux-model description). |
| 6 | `hermes_image_generation.md` | procedure | image-generation §Supported Models (11-model table), §Setup (FAL key, Nous Subscription, pick model, GPT-Image quality pin), §Usage, §Aspect Ratios, §Automatic Upscaling, §How It Works Internally (resolve/payload/submit/upscale/deliver), §Debugging, §Platform Delivery, §Limitations | ~1350 | FAL.ai text-to-image: 11 selectable models (FLUX 2 Klein default → Nano Banana Pro / GPT-Image / Ideogram / Recraft / Krea), `hermes tools` picker + `image_gen` config, three aspect ratios mapped per-model, per-model Clarity upscaling, the resolve→`_build_fal_payload`→submit→upscale→`MEDIA:` delivery pipeline, and text-to-image-only limits. |
| 7 | `hermes_spotify_integration.md` | procedure | spotify §intro, §Prerequisites, §Setup (one-shot + two-step, app creation, SSH/headless), §Verify, §Using it (7 tools: playback/devices/queue/search/playlists/albums/library + Home Assistant speakers), §Feature matrix Free vs Premium, §Scheduling: Spotify + cron, §Sign out, §Advanced (custom scopes / client-id), §Where things live | ~1500 | Spotify control via PKCE OAuth: register a personal dev app, `hermes auth spotify` login (auto-refresh on 401), the 7 opt-in tools (playback/devices/queue/search/playlists/albums/library), Free-vs-Premium matrix, Connect/Home-Assistant device targeting, cron-driven playback, custom scopes/redirect, and `auth.json`/`.env` storage. |
| 8 | `hermes_deliverable_mode.md` | concept | deliverable-mode §intro, §How it works (3 pieces), §Supported file extensions, §Encouraging the agent to produce artifacts, §Kanban: artifacts ride completion notifications, §Connecting more services with MCP, §Comparison to Perplexity Computer in Slack | ~850 | Deliverable mode: how the gateway turns absolute file paths mentioned in a reply into native chat attachments — file-producing tools (`execute_code`, latex-pdf/powerpoint skills, `image_generate`, `text_to_speech`), the extension→delivery dispatch table, code-block exclusion, per-session/project nudges, kanban `kanban_complete` artifacts, MCP connector breadth, and the local-token Perplexity-Computer comparison. |

**SP08a totals:** 8 notes · procedure 6 · model 1 · concept 1. 6 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 8 · procedure 6 · model 1 (TTS provider subsystem) · concept 1 (deliverable mode).
- Source: 6 digested pages (~13.2K words; image-gen grew +279w on 2026-06-19) → ~10.8K words of notes
  (modest compression via link-outs to the SP02 config blocks + SP05/14 portal/gateway + SP11–13 messaging
  delivery).
- BB mix: procedure 75%, model 12.5%, concept 12.5%.
- New term notes owned: **3** (`term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`).

## Section Coverage Map

```
voice-mode.md (2850w, 18 code)
├── Prerequisites / Requirements (Python pkgs, system deps, API keys) ── → Note 1
├── CLI Voice Mode (Quick Start / How It Works / Silence Detection / Streaming TTS / Hallucination Filter) → Note 1
├── Configuration Reference (voice/stt/tts yaml + STT/TTS comparison tables) → Note 1 (full config→SP02 link-out)
├── Gateway Voice Reply (Telegram & Discord: channels-vs-DMs / commands / modes / platform delivery) → Note 2 (platform setup→SP11)
├── Discord Voice Channels (permissions / intents / opus / env vars / how-it-works / text-channel / echo / access control) → Note 2
└── Troubleshooting ──────────────────────────────────────── → Note 1 (CLI rows) + Note 2 (gateway/VC rows)
tts.md (4341w, 20 code)
├── Text-to-Speech (10-provider table) / Platform Delivery / Configuration yaml → Note 3
├── Gemini Persona Prompts / Gemini Audio Tags / Input length limits ─── → Note 3
├── Telegram Voice Bubbles & ffmpeg / xAI Custom Voices / Piper ──────── → Note 3
├── Custom command providers (+Doubao / placeholders / optional keys / behavior / security) → Note 3
├── Python plugin providers (TTS: when-to-pick / minimal plugin / hooks) → Note 3
├── Voice Message Transcription (STT) (provider table / zero-config) ─── → Note 4
├── Configuration (stt yaml) / Provider Details (local/groq/openai/mistral/xai/custom CLI + Doubao ASR) → Note 4
├── Fallback Behavior ──────────────────────────────────────── → Note 4
├── STT custom command providers (placeholders / read-back / keys / behavior / security) → Note 4
└── Python plugin providers (STT: when-to-pick / resolution order / namespace / minimal plugin / hooks) → Note 4
vision.md (1606w, 8 code) ── ALL sections ──────────────────── → Note 5 (auxiliary.vision config→SP02; Nous Portal→SP14)
image-generation.md (1309w, 9 code) ── ALL sections ───────── → Note 6 (Tool Gateway→SP05; Nous Portal→SP14)
spotify.md (2198w, 12 code) ── ALL sections ──────────────── → Note 7 (PKCE→SP09 term_pkce; oauth-over-ssh→SP15; cron→SP06; Home Assistant→SP12)
deliverable-mode.md (850w, 1 code) ── ALL sections ────────── → Note 8 (execute_code→SP06; kanban→SP06; MCP→SP09; personality/SOUL/AGENTS→SP05)
```

No source H2/H3 orphaned. All 6 pages fully covered; config blocks + feature-detail intentionally routed
to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| voice-mode.md (2850w, 18 code) | Note 1 (CLI push-to-talk, proc) + Note 2 (gateway voice-reply + Discord VC, proc) | >2500w; two distinct procedural arcs — local-microphone CLI loop vs gateway/Discord-voice-channel pipeline (different setup, deps, and runtime). |
| tts.md (4341w, 20 code, MIXED) | Note 3 (TTS provider subsystem, model) + Note 4 (STT transcription, proc) | >4000w + BB mixing: the TTS half is a `model` enumerating ten providers + the command/plugin registry; the STT half is a `procedure` for inbound voice-message transcription + its own provider/fallback/registry. Each ≤2500w with ≤6 curated code blocks (20 source blocks → keep the load-bearing yaml/plugin examples). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note / owned slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `term_voice_mode` (owned) | `term_voice_wake.md` (10162b, active), `term_voice_call.md` (10719b, active) | **NOT a dup** — `term_voice_wake` is the wake-word/voice-activation concept (master LIKE false-positive `voice mode ≠ term_voice_wake`); `term_voice_call` is the telephony concept | CAPTURE `term_voice_mode`; LINK both as contrast/related. |
| `term_text_to_speech` (owned) | none substantive (no `term_tts`, no `term_text_to_speech`) | **NEW** | CAPTURE. |
| `term_speech_to_text` (owned) | `term_realtime_transcription.md` (11060b, active) | **NOT a dup** — that is the generic real-time-transcription concept; this is Hermes' STT subsystem scope (fallback chain + command/plugin registry + gateway voice-message injection) | CAPTURE `term_speech_to_text`; LINK `term_realtime_transcription`. |
| `hermes_vision_image_paste` | `term_computer_vision.md` (13127b, active), `term_multimodal.md` (7385b, active) | **NOT a dup** — Hermes `vision ≠ term_computer_vision` (master caution); those are the generic concepts this doc note documents the *usage* of | CREATE doc note; LINK both terms; SP08a captures NO vision term. |
| `hermes_image_generation` | `term_text_to_image`? (ABSENT), `term_diffusion_model`? | no substantive same-concept term/doc note | CREATE; link generic ML terms if relevant. |
| `hermes_spotify_integration` | `term_pkce` (ABSENT→SP09), `term_oauth` (active), `term_oauth_token` (active) | no Spotify doc/term note exists | CREATE; LINK oauth terms; `term_pkce` is +fin (SP09). |
| `hermes_deliverable_mode` | `term_api_gateway` (active, generic), no deliverable-mode note | **NOT a dup** of `term_api_gateway` (master: `messaging gateway ≠ term_api_gateway`) | CREATE; LINK only relevant terms. |
| `hermes_voice_mode_cli`, `hermes_voice_gateway_discord_vc`, `hermes_tts_providers`, `hermes_stt_transcription` | no substantive doc note covers these; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the LIKE hits `term_voice_wake` / `term_voice_call` /
`term_realtime_transcription` / `term_computer_vision` / `term_api_gateway` are confirmed-different
concepts, LINK-not-dup). New `hermes_agent/` folder → no doc-doc collisions (intra-series links resolve at
finalization). The 3 owned slugs were verified ABSENT in the DB (2026-06-15) — clean to create.

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19** (user directive, supersedes both the 2026-06-14 master floor of
> ≥8 term + ≥8 snippet + ≥5 doc AND the earlier-same-day 3-floor wording of ≥8 term + ≥5 code-repo + ≥10 doc
> with snippets as a bonus): each note's `## Related Notes` now carries **FOUR counted, relevancy-selected
> implement what this doc note describes), ≥10 SNIPPET notes (`../../code_snippets/snippet_hermes_agent_*`,
> COUNTED floor and raised from the prior 8 to ≥10), and ≥10 DOCUMENTATION notes (`../claude_code/cc_*`
> — each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`.
> 2026-06-19; the 13 `repo_hermes_agent_*` notes, the 517-note `snippet_hermes_agent_*` corpus selections, and
> the cc_* analogues all exist + active). Intra-series doc links (sibling `hermes_*`) resolve at finalization
> (G5/G8) and are allowed un-verified. Owned/other-SP not-yet-existing terms are marked `[own]` in the
> (`term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`) are captured in Phase 0 and additionally

**Note 1 `hermes_voice_mode_cli`** (procedure)
- Terms (8): [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — Whisper transcription of recorded speech; relevance: the CLI loop transcribes each push-to-talk recording via Whisper STT before sending to the agent. · [term_voice_bot](../../term_dictionary/term_voice_bot.md) — conversational voice-agent pattern; relevance: CLI voice mode IS the local voice-bot loop (record → transcribe → respond → speak). · [term_multimodal](../../term_dictionary/term_multimodal.md) — non-text input/output channels; relevance: voice is the audio multimodal surface alongside vision. · [term_persona](../../term_dictionary/term_persona.md) — agent personality config; relevance: persona shapes the spoken/streamed reply content. · [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class Hermes belongs to; relevance: voice is one I/O modality of the autonomous agent. · [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the loop that runs tools/model; relevance: transcribed speech feeds the harness, which streams text back to TTS. · [term_context_window](../../term_dictionary/term_context_window.md) — the model's input budget; relevance: transcripts are injected as turns into the context window. · [term_voice_wake](../../term_dictionary/term_voice_wake.md) — wake-word voice-activation (CONTRAST); relevance: explicitly distinguished from Hermes real-time voice mode (master LIKE false-positive). (+fin: [term_voice_mode](../../term_dictionary/term_voice_mode.md) [own], [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) [own], [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) [own])
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the `hermes chat`/TUI client; relevance: implements the Ctrl+B record loop, `/voice` slash commands, live audio-level bar, and beep cues. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tools layer; relevance: houses the voice-mode tool, the streaming-TTS sentence buffer, and the 26-phrase hallucination filter. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — STT/TTS provider adapters; relevance: drives the `local`/`groq`/`openai` Whisper STT and the streaming TTS provider this loop calls. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent runtime; relevance: receives the transcript, runs the pipeline, and emits text deltas the CLI converts to speech. · [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — the umbrella repo; relevance: ships the `hermes-agent[voice]` extra + PortAudio/ffmpeg/Opus system-dep wiring this page installs.
- Docs (10): [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md) — the gateway/Discord-VC sibling; relevance: the other half of the voice split (gateway voice-reply vs local CLI loop). · [hermes_tts_providers](hermes_tts_providers.md) — TTS subsystem; relevance: the streaming-TTS step picks a provider from this subsystem. · [hermes_stt_transcription](hermes_stt_transcription.md) — STT subsystem; relevance: the transcription step uses the STT provider chain documented there. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config note; relevance: owns the full `voice:`/`stt:`/`tts:` config blocks this page link-outs to. · [hermes_cli_interface](hermes_cli_interface.md) — CLI/TUI doc; relevance: voice mode is a CLI/TUI feature reached via `hermes`/`hermes --tui`. · [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — Claude Code voice-input analogue; relevance: closest external-agent push-to-talk voice-input feature for comparison. · [cc_interactive_mode_keyboard_shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — CC keybindings; relevance: analogous to the configurable `voice.record_key` Ctrl+B binding. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tool catalog; relevance: the voice-mode tool is one of Hermes' built-in tools. · [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — CC streaming output; relevance: analogous to the sentence-by-sentence streaming TTS deltas. · [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: the LLM that answers voice turns is chosen via `hermes model`, the analogue.
- Snippets (10): [tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — the voice-mode tool; relevance: implements the Ctrl+B record→silence-detect→transcribe→speak loop this page documents. · [cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — CLI voice slash-command surface; relevance: the `/voice on/off/tts/status` toggles + live audio-level bar. · [tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — STT transcription; relevance: each push-to-talk recording is Whisper-transcribed here before going to the agent. · [tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: the streaming sentence-by-sentence TTS step routes through this. · [core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — provider fallback activation; relevance: the local>groq>openai STT auto-fallback the loop relies on. · [tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy audio-dep install; relevance: the `hermes-agent[voice]` + PortAudio/ffmpeg/Opus deps this page installs. · [core_prompt_builder_environment](../../code_snippets/snippet_hermes_agent_core_prompt_builder_environment.md) — prompt environment; relevance: voice transcripts are injected as turns into the built prompt. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: the voice-mode tool is registered here. · [cli_attachment_input_bindings](../../code_snippets/snippet_hermes_agent_cli_attachment_input_bindings.md) — CLI key-binding layer; relevance: the configurable `voice.record_key` (Ctrl+B) recording binding lives in the CLI input layer. · [cli_hermescli_process_command](../../code_snippets/snippet_hermes_agent_cli_hermescli_process_command.md) — slash-command dispatch; relevance: dispatches the `/voice*` slash commands that toggle CLI voice mode.

**Note 2 `hermes_voice_gateway_discord_vc`** (procedure)
- Terms (8): [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — live speech-to-text; relevance: the VC pipeline transcribes each user's audio stream via Whisper before processing. · [term_voice_bot](../../term_dictionary/term_voice_bot.md) — voice-conversation bot; relevance: the Discord-VC listen→transcribe→agent→speak loop is a voice-bot in a voice channel. · [term_multimodal](../../term_dictionary/term_multimodal.md) — audio I/O channel; relevance: voice-reply delivers spoken audio alongside text. · [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bot bearer credential; relevance: the gateway connects via the `DISCORD_BOT_TOKEN`. · [term_authentication](../../term_dictionary/term_authentication.md) — bot auth + access control; relevance: `DISCORD_ALLOWED_USERS` gates who the VC bot will process. · [term_session_persistence](../../term_dictionary/term_session_persistence.md) — per-platform session state; relevance: voice-mode setting persists across gateway restarts, and the agent pipeline keeps session/tools/memory per user. · [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent class; relevance: the VC pipeline runs the full autonomous agent. · [term_websocket](../../term_dictionary/term_websocket.md) — persistent socket transport; relevance: Discord voice/SPEAKING opcode + SSRC→user mapping ride the voice websocket. (+fin: [term_voice_mode](../../term_dictionary/term_voice_mode.md) [own], [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) [own], [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) [own], [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) [own])
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the messaging gateway; relevance: implements Telegram/Discord voice-reply modes, the Discord voice-channel join/listen/speak loop, SSRC→user_id mapping, echo prevention, and Opus/OGG voice-bubble delivery. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: provides the transcription + TTS tools the VC loop drives per turn. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — STT/TTS adapters; relevance: the VC pipeline transcribes via Whisper STT and speaks via the configured TTS provider. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent runtime; relevance: the "Processes through the full agent pipeline (session, tools, memory)" step. · [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — gateway/TUI surface; relevance: hosts the `hermes gateway` entry point + setup wizard that connects configured platforms.
- Docs (10): [hermes_voice_mode_cli](hermes_voice_mode_cli.md) — CLI voice sibling; relevance: the local-microphone half of the voice split. · [hermes_tts_providers](hermes_tts_providers.md) — TTS subsystem; relevance: the "Speaks the reply back" step routes through it. · [hermes_stt_transcription](hermes_stt_transcription.md) — STT subsystem; relevance: VC audio is transcribed via the STT provider chain. · [hermes_deliverable_mode](hermes_deliverable_mode.md) — gateway artifact delivery sibling; relevance: shares the gateway delivery dispatch (voice bubble vs file attachment fallback). · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: owns the `voice:` mode + per-platform delivery config. · [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — CC messaging-platform agent; relevance: closest analogue of an agent driven over a chat platform. · [cc_slack_setup_and_routing](../claude_code/cc_slack_setup_and_routing.md) — CC platform setup/routing; relevance: analogous to the Discord bot permissions/intents/channel-routing setup. · [cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md) — CC channel reply; relevance: analogous to the gateway auto voice-reply behavior. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC tool catalog; relevance: voice/transcription are built-in tools invoked in the VC loop. · [cc_authentication](../claude_code/cc_authentication.md) — CC auth doc; relevance: analogue for the bot-token auth + allowed-users access control.
- Snippets (10): [gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord connect/intents; relevance: the bot connect with the three privileged intents + voice-channel join. · [gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord media; relevance: native voice-bubble (Opus/OGG) delivery + file-attachment fallback. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media; relevance: the Telegram Opus/OGG voice-bubble delivery path. · [gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal media; relevance: per-platform voice/audio delivery for Signal. · [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery dispatch; relevance: routes the spoken reply to the right per-platform delivery format. · [tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the listen→transcribe→agent→speak VC loop drives this tool per turn. · [tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription; relevance: each user's VC audio stream is Whisper-transcribed here. · [tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: the "speaks the reply back" step routes through this. · [gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash commands; relevance: implements `/voice join`/`channel`/`leave`/`status` in the text channel. · [gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — per-user session keying; relevance: keys the SSRC→user_id per-user session/tools/memory the full-pipeline step needs.

**Note 3 `hermes_tts_providers`** (model)
- Terms (8): [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider abstraction; relevance: the TTS subsystem IS a provider registry — ten built-ins + command/Python-plugin providers via `register_tts_provider()`. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin authoring surface; relevance: the `TTSProvider` ABC + `ctx.register_tts_provider()` is the TTS plugin SDK. · [term_model_catalog](../../term_dictionary/term_model_catalog.md) — selectable model/provider set; relevance: the ten-provider table + per-provider model IDs form a catalog the picker selects from. · [term_llm](../../term_dictionary/term_llm.md) — the chat model; relevance: Gemini audio-tag rewrite uses `auxiliary.tts_audio_tags` (defaults to the main chat LLM). · [term_persona](../../term_dictionary/term_persona.md) — voice/personality direction; relevance: Gemini persona-prompt files drive natural-language voice direction. · [term_multimodal](../../term_dictionary/term_multimodal.md) — audio output channel; relevance: TTS is the audio-out half of multimodal. · [term_authentication](../../term_dictionary/term_authentication.md) — provider API keys; relevance: paid providers (ElevenLabs/OpenAI/MiniMax/etc.) authenticate via env-var keys. · [term_failover](../../term_dictionary/term_failover.md) — provider fallback; relevance: Edge TTS is the free no-key default fallback when premium providers fail. (+fin: [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) [own], [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) [own], [term_nous_portal](../../term_dictionary/term_nous_portal.md) [own], [term_tool_gateway](../../term_dictionary/term_tool_gateway.md) [own])
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: implements the ten built-in TTS provider adapters (Edge/ElevenLabs/OpenAI/MiniMax/Mistral/Gemini/xAI/NeuTTS/KittenTTS/Piper) + the command-provider runner. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: hosts the `text_to_speech` tool, the TTS routing/dispatch, input-length truncation, and ffmpeg Opus conversion. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin system; relevance: provides the `TTSProvider` ABC + `register_tts_provider()` plugin resolution and `hermes plugins enable`. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway; relevance: implements Telegram/Discord voice-bubble delivery + the WhatsApp/CLI audio-file fallback for TTS output. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: `hermes tools` Voice & TTS picker + `hermes setup` provider rows (`get_setup_schema`) select the TTS provider.
- Docs (10): [hermes_stt_transcription](hermes_stt_transcription.md) — STT sibling; relevance: the mirror-image provider/plugin/command registry for the inbound direction. · [hermes_voice_mode_cli](hermes_voice_mode_cli.md) — CLI voice; relevance: streaming-TTS consumer of this subsystem. · [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md) — gateway voice; relevance: the gateway/VC "speak the reply" consumer. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: owns the full `tts:` config block this model link-outs to. · [hermes_deliverable_mode](hermes_deliverable_mode.md) — artifact delivery; relevance: `text_to_speech` is a file-producing tool whose audio is delivered as an attachment. · [cc_model_selection](../claude_code/cc_model_selection.md) — CC model picker; relevance: analogous to selecting a TTS provider/model from the catalog. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — CC extension surfaces; relevance: analogous to the command-provider + Python-plugin extension paths. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — CC plugin model; relevance: analogue for the `register_tts_provider()` plugin coexistence/precedence rules. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: `text_to_speech` is a built-in name that always wins over user-declared providers. · [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — CC voice; relevance: closest external-agent audio feature for cross-reference.
- Snippets (10): [tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing/dispatch; relevance: the `text_to_speech` tool routes to the selected one of ten providers + truncates to per-provider caps. · [plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — plugin dispatch pattern; relevance: parallel example of the plugin-provider dispatch the `register_tts_provider()` path uses. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media; relevance: the ffmpeg MP3→Opus voice-bubble conversion for Telegram delivery. · [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: dispatches TTS audio to per-platform delivery (voice bubble vs file). · [core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: Edge TTS is the free no-key default fallback this implements. · [tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dep install; relevance: `hermes-agent[tts-premium]` (elevenlabs) + NeuTTS deps installed on demand. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: `text_to_speech` is a built-in name that always wins over a same-name command/plugin provider. · [tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — send formatting; relevance: formats the audio output for the outbound message. · [plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — plugin ABCs; relevance: defines the `TTSProvider` ABC + `register_tts_provider()` surface the command/Python providers implement. · [cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — `hermes tools` picker config; relevance: the Voice & TTS provider picker + `get_setup_schema()` rows that select the provider.

**Note 4 `hermes_stt_transcription`** (procedure)
- Terms (8): [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — generic real-time transcription (CONTRAST/parent); relevance: Hermes STT is the scoped subsystem of this generic concept (master LIKE — LINK not dup). · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: STT is a provider registry (local/groq/openai/mistral/xai + command + plugin) via `register_transcription_provider()`. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin surface; relevance: the `TranscriptionProvider` ABC + resolution order is the STT plugin SDK. · [term_failover](../../term_dictionary/term_failover.md) — automatic fallback chain; relevance: the documented local→groq→openai fallback when a provider key/SDK is missing. · [term_voice_bot](../../term_dictionary/term_voice_bot.md) — voice-message bot intake; relevance: inbound voice messages on Telegram/Discord/WhatsApp/Slack/Signal are auto-transcribed and injected. · [term_multimodal](../../term_dictionary/term_multimodal.md) — audio-in channel; relevance: STT is the audio-input half of multimodal. · [term_authentication](../../term_dictionary/term_authentication.md) — provider keys; relevance: cloud STT providers (Groq/OpenAI/Mistral/xAI) authenticate via env-var keys. · [term_llm](../../term_dictionary/term_llm.md) — the model; relevance: the transcript is injected as text into the LLM conversation. (+fin: [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) [own], [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) [own], [term_voice_mode](../../term_dictionary/term_voice_mode.md) [own], [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) [own])
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — STT adapters; relevance: implements the local-faster-whisper default + Groq/OpenAI/Mistral/xAI cloud adapters and the auto-fallback chain. · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: hosts `transcribe_audio()`, the `stt.providers.<name>: type: command` runner, and transcript read-back logic. · [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin system; relevance: provides the `TranscriptionProvider` ABC + `register_transcription_provider()` resolution order. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway; relevance: receives inbound voice messages per-platform and injects the transcript into the conversation. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: the CLI voice loop and the local `whisper` CLI / `HERMES_LOCAL_STT_COMMAND` escape hatch run here.
- Docs (10): [hermes_tts_providers](hermes_tts_providers.md) — TTS sibling; relevance: the mirror provider/plugin/command registry for the outbound direction. · [hermes_voice_mode_cli](hermes_voice_mode_cli.md) — CLI voice; relevance: the CLI push-to-talk loop transcribes via this STT subsystem. · [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md) — gateway/VC; relevance: VC audio + inbound voice messages are transcribed here. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: owns the full `stt:` config block this page link-outs to. · [hermes_cli_interface](hermes_cli_interface.md) — CLI doc; relevance: STT is reachable from the CLI voice surface. · [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — CC voice dictation; relevance: closest external-agent speech-to-text feature. · [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — CC extension surfaces; relevance: analogue for the command-provider + plugin extension paths. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — CC plugins; relevance: analogue for the plugin coexistence/precedence (built-in > command > plugin) rules. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: built-in STT names short-circuit before the command-provider resolver. · [cc_fallback_models](../claude_code/cc_fallback_models.md) — CC fallback models; relevance: analogous to the local→groq→openai STT fallback behavior.
- Snippets (10): [tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: implements `transcribe_audio()`, the local-whisper default + cloud adapters, and the `stt.providers.<name>: type: command` runner. · [tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode integration; relevance: the CLI push-to-talk loop transcribes via this STT path. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media intake; relevance: inbound Telegram voice messages are routed to STT. · [gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal media intake; relevance: inbound Signal voice messages are auto-transcribed. · [core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: the documented local→groq→openai auto-fallback chain. · [tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dep install; relevance: `faster-whisper` / `hermes-agent[mistral]` deps installed on demand. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: built-in STT names short-circuit before the command-provider resolver. · [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: the gateway injects the transcript text back into the conversation flow. · [cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — CLI voice surface; relevance: the local `whisper` CLI / `HERMES_LOCAL_STT_COMMAND` escape hatch is driven here. · [plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — plugin ABCs; relevance: defines the `TranscriptionProvider` ABC + `register_transcription_provider()` resolution order.

**Note 5 `hermes_vision_image_paste`** (procedure)
- Terms (8): [term_multimodal](../../term_dictionary/term_multimodal.md) — multimodal input; relevance: pasted images are sent as base64 multimodal vision content blocks. · [term_computer_vision](../../term_dictionary/term_computer_vision.md) — generic vision concept (master: Hermes vision ≠ this); relevance: this doc documents the USAGE of vision-capable models, LINKing the generic term. · [term_clip](../../term_dictionary/term_clip.md) — vision-language embedding model family; relevance: foundational to the vision-capable model class that processes pasted images. · [term_model_catalog](../../term_dictionary/term_model_catalog.md) — selectable models; relevance: Hermes routes based on the current model's vision capability looked up in provider metadata. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider abstraction; relevance: `auxiliary.vision` selects the describer model/provider for text-only routing. · [term_llm](../../term_dictionary/term_llm.md) — the model; relevance: vision-capable LLMs get raw pixels; text-only LLMs get an injected description. · [term_base64](../../term_dictionary/term_base64.md) — binary-to-text encoding; relevance: images are sent as `data:image/png;base64,...` data URLs in OpenAI vision format. · [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent loop; relevance: the `vision_analyze` tool returns raw pixels or a text description into the harness at runtime. (+fin: [term_nous_portal](../../term_dictionary/term_nous_portal.md) [own])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: implements the `vision_analyze` tool and its dual native-pixels-vs-aux-describer routing. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI/TUI; relevance: implements `/paste`, layered Cmd/Ctrl+V, `/terminal-setup`, image badges, and the per-OS clipboard subprocess (osascript/xclip/wl-paste/powershell.exe). · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: holds the per-provider vision-capability metadata + the native image-content format per provider stack. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent runtime; relevance: injects image content blocks (or text descriptions) into the conversation and resolves the `auxiliary.vision` model. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway; relevance: gateway Telegram/Discord photo intake is another entry point routed through the same vision path.
- Docs (10): [hermes_image_generation](hermes_image_generation.md) — image-gen sibling; relevance: the output counterpart to vision input (and shares the FAL/portal model-capability routing). · [hermes_tts_providers](hermes_tts_providers.md) — TTS subsystem; relevance: sibling media subsystem under the same media surface. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: owns the `auxiliary.vision` config slot this page link-outs to. · [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — model config; relevance: vision-capability lookup depends on the configured model/provider. · [hermes_cli_interface](hermes_cli_interface.md) — CLI doc; relevance: image paste is a CLI/TUI clipboard feature. · [cc_computer_use](../claude_code/cc_computer_use.md) — CC computer-use (screenshots); relevance: closest external-agent feature that feeds image pixels to a vision model. · [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: analogue for selecting a vision-capable vs text-only model. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: `vision_analyze` is a built-in tool with runtime-decided behavior. · [cc_terminal_configuration](../claude_code/cc_terminal_configuration.md) — CC terminal setup; relevance: analogue for the `/terminal-setup` VS Code keybinding install + terminal paste limits. · [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — CC rich tool results; relevance: analogous to `vision_analyze` returning a multimodal image-tool-result envelope.
- Snippets (10): [tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision input capture; relevance: builds the base64 `data:image/png;base64,...` OpenAI vision content block from a pasted image. · [tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — `vision_analyze` dispatch; relevance: the dual native-pixels-vs-aux-describer routing this page documents. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram photo intake; relevance: gateway Telegram photos are another entry point into the same vision path. · [gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord photo intake; relevance: gateway Discord image attachments route through the same vision routing. · [core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auxiliary model resolution; relevance: resolves the `auxiliary.vision` describer model for text-only routing. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: `vision_analyze` is a built-in tool with runtime-decided behavior. · [core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — context loaders; relevance: injects the image content block (or text description) into the conversation. · [tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: returns the multimodal image-tool-result envelope. · [cli_attachment_input_bindings](../../code_snippets/snippet_hermes_agent_cli_attachment_input_bindings.md) — CLI paste bindings; relevance: implements `/paste`, layered Cmd/Ctrl+V, and the `[📎 Image #N]` badge attach. · [model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — model capability probe; relevance: looks up the current model's vision capability in provider metadata to pick the pixels-vs-describe path.

**Note 6 `hermes_image_generation`** (procedure)
- Terms (8): [term_multimodal](../../term_dictionary/term_multimodal.md) — non-text output; relevance: image generation is a visual-output multimodal capability. · [term_diffusion_model](../../term_dictionary/term_diffusion_model.md) — generative image model class; relevance: most FAL models (FLUX/Krea/Recraft/Ideogram) are diffusion-family text-to-image models. · [term_stable_diffusion](../../term_dictionary/term_stable_diffusion.md) — canonical diffusion image generator; relevance: the foundational text-to-image lineage the FAL model catalog descends from. · [term_model_catalog](../../term_dictionary/term_model_catalog.md) — selectable model set; relevance: the 11-model `hermes tools` picker + `image_gen.model` persistence IS a model catalog. · [term_authentication](../../term_dictionary/term_authentication.md) — backend credentials; relevance: routing requires FAL `FAL_KEY` / Nous Subscription / OpenAI / xAI OAuth / Krea credentials. · [term_idempotency](../../term_dictionary/term_idempotency.md) — deterministic per-model mapping; relevance: `_build_fal_payload()` deterministically maps aspect-ratio + applies the `supports` whitelist per model. · [term_failover](../../term_dictionary/term_failover.md) — graceful degradation; relevance: failed upscaling returns the original image; expired temp URLs fall back to the local cache. · [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-call interface; relevance: the agent invokes `image_generate` with a minimal schema and gets a `MEDIA:` tag back. (+fin: [term_nous_portal](../../term_dictionary/term_nous_portal.md) [own], [term_tool_gateway](../../term_dictionary/term_tool_gateway.md) [own])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: implements the `image_generate` tool, `_resolve_fal_model()`, `_build_fal_payload()`, `_submit_fal_request()`, Clarity-upscaler gating, and the `MEDIA:` emit. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: the FAL/OpenAI/xAI/Krea backend adapters + per-model `supports`/`edit_supports` metadata and edit-endpoint routing. · [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway; relevance: platform adapters convert the `MEDIA:<url>` tag into per-platform native media (Telegram photo, Discord embed, Slack unfurl, WhatsApp media). · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: `hermes tools` → 🎨 Image Generation picker selects backend + model and persists to `config.yaml`. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent runtime; relevance: surfaces the active model's editing capability in the tool description at runtime and routes the returned media.
- Docs (10): [hermes_vision_image_paste](hermes_vision_image_paste.md) — vision sibling; relevance: the image-input counterpart sharing model-capability routing. · [hermes_deliverable_mode](hermes_deliverable_mode.md) — artifact delivery; relevance: `image_generate` is a file-producing tool whose output is delivered as a native attachment. · [hermes_tts_providers](hermes_tts_providers.md) — TTS subsystem; relevance: sibling provider-backed media subsystem with the same Portal/Gateway billing path. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: holds related media/display config; the `image_gen:` block lives in config. · [hermes_configuring_models_dashboard](hermes_configuring_models_dashboard.md) — model config; relevance: backend + model selection persists like other model config. · [cc_model_selection](../claude_code/cc_model_selection.md) — CC model selection; relevance: analogue for picking among generation models with cost/quality tradeoffs. · [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — CC LLM gateway; relevance: analogous to the managed Nous gateway proxying generation without a direct key. · [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — CC proxy/gateway config; relevance: analogue for direct-key vs managed-gateway backend routing + 4xx remediation. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: `image_generate` is a built-in agent tool with a minimal schema. · [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — CC rich tool results; relevance: analogous to returning a media URL/blob from a tool the platform renders.
- Snippets (10): [tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: implements `_resolve_fal_model()`, `_build_fal_payload()`, `_submit_fal_request()`, Clarity-upscaler gating, and the `MEDIA:` emit. · [plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — backend dispatch; relevance: routes to the FAL/OpenAI/xAI/Krea backend adapter per the selected model. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media; relevance: converts the `MEDIA:<url>` tag into a Telegram photo message with caption. · [gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord media; relevance: embeds the generated image in a Discord message. · [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: dispatches `MEDIA:<url>` to the right per-platform native media. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: `image_generate` is a built-in tool with a minimal agent-facing schema. · [tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential lookup; relevance: resolves `FAL_KEY` / `OPENAI_API_KEY` / xAI OAuth / `KREA_API_KEY` for the active backend. · [tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: returns the media URL/blob the platform renders. · [cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — `hermes tools` picker; relevance: the 🎨 Image Generation backend+model picker that persists `image_gen.model` to `config.yaml`. · [model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — model capability probe; relevance: surfaces the active model's editing capability in the tool description at runtime.

**Note 7 `hermes_spotify_integration`** (procedure)
- Terms (8): [term_oauth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: Spotify control uses PKCE OAuth against the official Web API. · [term_oauth_token](../../term_dictionary/term_oauth_token.md) — access/refresh tokens; relevance: tokens are stored under `providers.spotify` in `auth.json` and refreshed automatically on 401. · [term_auth_profile](../../term_dictionary/term_auth_profile.md) — stored per-provider auth state; relevance: the `providers.spotify` auth profile (token/expiry/scope/redirect) lives in `auth.json`. · [term_authentication](../../term_dictionary/term_authentication.md) — login + scopes; relevance: `hermes auth spotify` performs the consent flow with requested scopes. · [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — API quota; relevance: Spotify returns `429 Too Many Requests` on quota exhaustion (resets ~every 30s). · [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: a `hermes cron add` job can trigger Spotify playback on a schedule. · [term_cron_expression](../../term_dictionary/term_cron_expression.md) — schedule syntax; relevance: the wake-up/wind-down examples use `0 7 * * 1-5` / `30 22 * * *` cron expressions. · [term_idempotency](../../term_dictionary/term_idempotency.md) — safe-retry behavior; relevance: a 401 triggers a single refresh-and-retry; 204 on `get_currently_playing` surfaces as a benign empty result. (+fin: [term_pkce](../../term_dictionary/term_pkce.md) [own], [term_token_refresh](../../term_dictionary/term_token_refresh.md) [own])
- Code-Repos (5): [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — plugin/toolset system; relevance: implements the opt-in Spotify toolset (the 7 tools registered only after enabling). · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: hosts `spotify_playback`/`devices`/`queue`/`search`/`playlists`/`albums`/`library` + device-targeting and Free-vs-Premium gating. · [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI; relevance: implements `hermes auth spotify` (PKCE wizard, inline app registration, port-43827 loopback listener), `hermes auth status/logout spotify`, and the `hermes tools` 🎵 toggle. · [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron subsystem; relevance: runs the headless `skip_memory=True` Spotify-playback cron sessions. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/auth adapters; relevance: the Spotify OAuth client + 401-refresh-and-retry token exchange against the Web API.
- Docs (10): [hermes_deliverable_mode](hermes_deliverable_mode.md) — artifact delivery; relevance: sibling tool-integration doc sharing the local-`auth.json`/`.env` token-storage model. · [hermes_image_generation](hermes_image_generation.md) — image gen; relevance: sibling opt-in tool with credential-backed external API. · [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md) — gateway voice; relevance: shares the OAuth-over-SSH / headless-environment auth patterns. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: related config-blocks doc for toolset enablement. · [hermes_config_files_precedence](hermes_config_files_precedence.md) — config precedence; relevance: `auth.json` / `.env` (`HERMES_SPOTIFY_CLIENT_ID`/`REDIRECT_URI`) storage + precedence. · [cc_authentication](../claude_code/cc_authentication.md) — CC auth; relevance: closest external-agent OAuth-login analogue. · [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — CC MCP OAuth; relevance: analogue for OAuth + token refresh against an external service. · [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — CC scheduled tasks; relevance: analogous to cron-scheduled Spotify playback. · [cc_scheduling_options_comparison](../claude_code/cc_scheduling_options_comparison.md) — CC scheduling options; relevance: analogue for choosing scheduled-job mechanics. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: the 7 Spotify tools are opt-in tools exposed to the agent.
- Snippets (10): [plugins_spotify](../../code_snippets/snippet_hermes_agent_plugins_spotify.md) — Spotify toolset plugin; relevance: implements the opt-in 7-tool Spotify toolset (playback/devices/queue/search/playlists/albums/library). · [cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE auth flow; relevance: `hermes auth spotify` PKCE wizard + inline app registration + 401-refresh-and-retry. · [tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — cron registration; relevance: `hermes cron add` schedules the Spotify-playback prompt. · [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: the 7 Spotify tools register only after the toolset is enabled. · [tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential storage; relevance: `HERMES_SPOTIFY_CLIENT_ID`/`REDIRECT_URI` in `.env` and tokens in `auth.json`. · [core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential resolution; relevance: resolves the Spotify client-id/redirect-uri from env vs config. · [tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: returns the tool result (track/device state) to the agent. · [tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — schema sanitizer; relevance: sanitizes the per-tool action schemas (Free-vs-Premium gated). · [cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — loopback callback server; relevance: the local port-43827 HTTP listener that catches the OAuth redirect during login. · [cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — cron job execution; relevance: runs the headless `skip_memory=True` Spotify-playback cron session.

**Note 8 `hermes_deliverable_mode`** (concept)
- Terms (8): [term_multimodal](../../term_dictionary/term_multimodal.md) — mixed file types; relevance: deliverable mode ships images/video/audio/docs as native attachments. · [term_api_gateway](../../term_dictionary/term_api_gateway.md) — generic gateway (master: messaging gateway ≠ this); relevance: LINK-not-dup — the messaging gateway is the delivery surface, distinguished from the generic API gateway concept. · [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: connector breadth (Notion/GitHub/Linear/Slack/Gmail/etc.) comes via MCP servers in `mcp_servers`. · [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP connector aggregation; relevance: MCP is how Hermes "connects more services" beyond the file-delivery pipeline. · [term_kanban](../../term_dictionary/term_kanban.md) — task-board workflow; relevance: kanban workers attach artifacts to `kanban_complete` that ride the completion notification. · [term_oauth_token](../../term_dictionary/term_oauth_token.md) — local credentials; relevance: OAuth tokens stay on-device in `auth.json`/`.env` (no hosted token storage). · [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — local execution sandbox; relevance: file generation happens in the user's own venv/sandbox (no remote tenant). · [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent loop; relevance: file-producing tools (`execute_code`/skills/`image_generate`/`text_to_speech`) run in the harness, which mentions the path the gateway extracts. (+fin: [term_code_execution_tool](../../term_dictionary/term_code_execution_tool.md) [own], [term_kanban_multi_agent](../../term_dictionary/term_kanban_multi_agent.md) [own], [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) [own])
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway; relevance: implements the path-scan, code-block exclusion, extension→delivery dispatch table, and native per-platform attachment upload (Slack `files.uploadV2` etc.). · [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tools layer; relevance: hosts the file-producing tools (`execute_code`, `image_generate`, `text_to_speech`) and `kanban_complete` artifact attachment. · [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — skills system; relevance: the `latex-pdf-report` and `powerpoint` artifact-producing skills referenced by this page. · [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP toolsets; relevance: implements the `mcp_servers` connector ecosystem (Notion/GitHub/Linear/Slack/Gmail/...) that broadens deliverable reach. · [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent runtime; relevance: the agent biased (via persona/AGENTS.md/SOUL.md) to render artifacts and mention their absolute paths.
- Docs (10): [hermes_image_generation](hermes_image_generation.md) — image gen; relevance: `image_generate` is one of the file-producing tools feeding deliverable mode. · [hermes_tts_providers](hermes_tts_providers.md) — TTS subsystem; relevance: `text_to_speech` audio is one of the deliverable file types. · [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md) — gateway voice; relevance: shares the gateway delivery/attachment dispatch path. · [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — SP02 config; relevance: related personality/display/media gateway config. · [hermes_mcp](hermes_mcp.md) — MCP integration sibling; relevance: deliverable mode link-outs to MCP for connector breadth. · [cc_claude_code_in_slack](../claude_code/cc_claude_code_in_slack.md) — CC in Slack; relevance: direct analogue — an agent posting deliverables into a chat thread. · [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — CC MCP overview; relevance: analogue for adding service connectors via MCP. · [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — CC MCP server mgmt; relevance: analogue for installing/managing the MCP connector servers. · [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — CC rich tool content; relevance: analogous to tools returning files/media for native rendering. · [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC built-in tools; relevance: the file-producing tools are built-ins whose output deliverable mode dispatches.
- Snippets (10): [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery dispatch; relevance: the path-scan, code-block exclusion, and extension→delivery dispatch table this page documents. · [gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord attachment; relevance: native per-platform attachment upload for Discord. · [gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram attachment; relevance: native media/file delivery for Telegram. · [gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal attachment; relevance: native file/audio delivery for Signal. · [gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp dispatch; relevance: native media-message delivery for WhatsApp. · [tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — send-attach path; relevance: the Slack `files.uploadV2`-style native attachment upload. · [tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: routes file-producing-tool output into the delivery pipeline. · [tools_kanban_mutate](../../code_snippets/snippet_hermes_agent_tools_kanban_mutate.md) — kanban mutation; relevance: `kanban_complete(artifacts=[...])` rides the completion notification with attachments. · [tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: `image_generate` is one of the file-producing tools whose output deliverable mode ships. · [tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — MCP tool call; relevance: the MCP-connector breadth (Notion/GitHub/Linear/Slack/Gmail/...) this page link-outs to.

All 8 notes meet the **FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**. Every term ID, code-repo
ID (13 `repo_hermes_agent_*`), snippet ID (`snippet_hermes_agent_*` selections from the 517-note corpus), and
`resources/documentation/hermes_agent/` at finalization (verified by G5/G8). The SNIPPET group is now a COUNTED
floor (≥10, promoted from the prior bonus/8). The 3 SP08a-owned terms are captured in Phase 0 and additionally
placeholders counted toward any floor. Smallest per-note counts are exactly 8 term / 5 repo / 10 snippet / 10 doc.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 6 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages table
(no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 voice-mode-cli | procedure | 1400 | ≤6 (curate from voice/stt/tts yaml + slash-command blocks; comparison tables in prose) | ✓ |
| 2 voice-gateway-discord-vc | procedure | 1400 | ≤6 (curate from env-var / permissions / command blocks) | ✓ |
| 3 tts-providers | model | 2400 | ≤6 (curate from ~20 yaml/plugin blocks; one canonical block per provider-class + 1 command + 1 plugin) | ✓ |
| 4 stt-transcription | procedure | 1700 | ≤6 (curate from stt yaml + command-registry + minimal-plugin blocks) | ✓ |
| 5 vision-image-paste | procedure | 1400 | ≤6 (from 8 paste/setup/json blocks) | ✓ |
| 6 image-generation | procedure | 1350 | ≤6 (from 9 picker/config/aspect blocks) | ✓ |
| 7 spotify-integration | procedure | 1500 | ≤6 (curate from 12 setup/cron/scope blocks) | ✓ |
| 8 deliverable-mode | concept | 850 | 1 (kanban_complete block kept verbatim) | ✓ |

No further splits needed beyond the planned 2 (voice→2, tts→2). All 8 notes ≤2500w. Code-heavy notes
(3 tts-providers at ~2400w, 7 spotify) curated to ≤6 load-bearing blocks, rest summarized in prose (kept
blocks verbatim). Borderline Note 3 (~2400w) checked for further split: it is one topically-cohesive
provider-subsystem `model` (no BB mixing) → KEEP (review CP6 default-to-keep justification). If any note
exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc — set 2026-06-19) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP08a)

**SP08a owns 3 new term captures** (per the master's corpus-wide ownership sweep): `term_voice_mode`,
`term_text_to_speech`, `term_speech_to_text`. Augment re-read confirmed these are the right ownership set —
the master assigned them to SP08 and they belong to the media (`a`) half. The browser/web/computer-use terms
(`term_browser_automation`) are SP08b's. Each owned slug was verified ABSENT in the DB (2026-06-15); each
collision-audited against the master's caution list (below).

| Term slug | Concept | Owner | Capture Phase | Stub/Full | Best-fit glossary | Source page |
|---|---|---|---|---|---|---|
| `term_voice_mode` | real-time voice conversation mode (CLI push-to-talk + gateway voice-reply + Discord VC); ≠ voice_wake | SP08a | Phase 0 (before Notes 1–4) | full | acronym_glossary_llm | voice-mode.md |
| `term_text_to_speech` | TTS subsystem: ten providers + command/Python-plugin registry | SP08a | Phase 0 (before Note 3) | full | acronym_glossary_llm | tts.md |
| `term_speech_to_text` | STT / voice-message transcription: provider fallback chain + command/plugin registry + gateway injection | SP08a | Phase 0 (before Note 4) | full | acronym_glossary_llm | tts.md |
| `term_browser_automation` | LINK only (forward-ref, +fin) | SP08b | — | — | acronym_glossary_tools | (SP08b owns) |
| `term_nous_portal`, `term_tool_gateway` | LINK only (+fin) | SP14 / SP05 | — | — | acronym_glossary_tools | TTS/vision/image-gen reference the portal billing path |
| `term_code_execution_tool`, `term_kanban_multi_agent` | LINK only (+fin) | SP06 | — | — | acronym_glossary_developer / workflows | deliverable mode artifacts |
| `term_pkce`, `term_token_refresh` | LINK only (+fin) | SP09 | — | — | acronym_glossary_security | spotify PKCE OAuth |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | — | — | acronym_glossary_systems | gateway voice/deliverable delivery |

Capture each owned term via **`/tessellum-capture-term-note <term>`** (NOT inline) in Phase 0, with
below. The 3 owned full term notes target the **moderate (80-150 lines) → ≥10 Related Terms** depth tier.

### Renamed (general → specific)

| Original slug | Renamed to | Reason |
|---|---|---|
| (none from master) | — | Master's slugs (`term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`) are already scope-specific. Specificity audit applied: `term_voice_mode` is explicitly qualified (≠ generic `voice`/`term_voice_wake`/`term_voice_call`); `term_text_to_speech`/`term_speech_to_text` use the canonical full-form domain names (avoid bare `term_tts`/`term_stt` which would be cryptic). No renames needed. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, size, status) | Action |
|---|---|---|
| `term_vision` / Hermes vision | `term_computer_vision.md` (13127b, active) + `term_multimodal.md` (7385b, active) | Not captured — master caution `vision ≠ term_computer_vision`; the `hermes_vision_image_paste` doc note LINKS both existing terms. SP08a captures NO vision term. |
| `term_voice` (would over-generalize) | `term_voice_wake.md` (10162b, active), `term_voice_call.md` (10719b, active) | Not captured — both are different concepts; capture the specific `term_voice_mode` instead and LINK these as contrast. |
| `term_transcription` (would duplicate) | `term_realtime_transcription.md` (11060b, active) | Not captured — generic real-time transcription already covered; capture the Hermes-scoped `term_speech_to_text` instead and LINK the existing term. |
| `term_image_gen` / FAL image gen | none substantive | No removal — SP08a does not capture an image-gen term; the `hermes_image_generation` doc note is sufficient (product-specific procedure, low conceptual reuse). |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Every owned term (`term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`) MUST be authored via
**`/tessellum-capture-term-note <term>`** (interactive or via ENRICHER_INPUTS), NOT inline-authored within a
digest note. The capture skill enforces the requirements below; this plan invokes them.

### YAML Frontmatter (Required Fields)

```yaml
---
tags:
  - resource
  - terminology
  - llm                       # domain tag 1 (voice/speech sit under llm/multimodal)
  - multimodal                # domain tag 2 (narrower)
keywords:
  - <ACRONYM or short form>   # e.g., TTS, STT
  - <Full Name>               # e.g., Text-to-Speech
  - <variant_spellings>
topics:
  - <topic_1>
  - <topic_2>
language: markdown
date of note: 2026-06-15
status: active
building_block: concept       # MUST be concept for term notes
access_control_group: ["general"]
related_wiki: null
---
```

### Required H1 + H2 Sections (in order)

| Section | Required | Content |
|---|---|---|
| `# <ACRONYM> - <Full Name>` H1 | Yes | e.g. `# TTS - Text-to-Speech`; `# STT - Speech-to-Text`; `# Voice Mode` (no acronym → plain title) |
| `## Definition` | Yes | 1–2 paragraphs; what it is, what problem it solves, agent/multimodal context |
| `## Context` | Yes | Which systems/agents/platforms use it (Hermes CLI/gateway/Discord-VC; cross-domain: agent harnesses generally) |
| `## Key Characteristics` | Yes | Distinctive properties (provider-fallback chain, command/plugin registry, streaming, silence detection, etc.) |
| `## Performance / Metrics` | Optional | Include ONLY if found; omit otherwise (no fabricated latency numbers) |
| `## Related Terms` | Yes | **≥10 vault term-note links** (moderate depth) — INDEXED markdown link format `**[Term Name](term_X.md)** — one-line description`; ≥3 in-domain + ≥3 cross-domain |
| `## References` | Yes | EXTERNAL URLs ONLY (Hermes docs page, Whisper/ElevenLabs/Edge-TTS docs, Wikipedia TTS/STT); NO `term_*.md` links here |


The Hermes source page is ONE viewpoint. Each capture MUST research across multiple sources:
4. **External (≥2 of):** Wikipedia (Text-to-speech / Speech recognition), OpenAI Whisper paper/repo,
   ElevenLabs/Edge-TTS official docs, the Hermes `tts.md`/`voice-mode.md` source pages. Even when the digest
   doc covers the term richly, an external source provides definition orthogonality.
5. **Vault cross-reference:** `/tessellum-search-notes <term>` + DB query for in-domain (multimodal/voice) +
   cross-domain (agent/provider/fallback) related term notes.

### Cross-Domain Diversity for Related Terms (≥10 links, moderate depth)

Per capture-term-note canonical Step 3e, Related Terms MUST include cross-domain connections — NOT just
same-domain siblings: Foundation (e.g. `term_multimodal` → vision/voice), Application
(`term_voice_mode` → `term_messaging_gateway` consumption), Contrast (`term_voice_mode` vs `term_voice_wake`,
`term_speech_to_text` vs `term_realtime_transcription`), Component (`term_provider_plugin`,
`term_failover`), Successor/Predecessor where applicable. Target ≥3 in-domain + ≥3 cross-domain = ≥10 total
verified links.

### Math Notation, Fleeting Content, Glossary, Naming, Backlinks, Decomposition

- **MathJax** for any formula (none expected for these three; if a latency/RMS-threshold formula is written,
  use `$...$`/`$$...$$`, never plain-text).
- **Fleeting-content guard:** strip person aliases, bare ETAs, bare dollar/headcount; qualify provider
  pricing as "(as of 2026)" if cited at all (prefer NOT citing volatile FAL/ElevenLabs prices in the term).
- **Glossary update:** add a 4–5-sentence Description (no metrics) entry to `acronym_glossary_llm.md` using
  the exact `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template.
- **File naming:** `term_voice_mode.md`, `term_text_to_speech.md`, `term_speech_to_text.md` (full domain
  forms — canonical; NOT cryptic `term_tts`/`term_stt`).
- **Backlink expansion (Step 6e):** add the new terms to 5–10 existing in/cross-domain term notes' Related
  Terms (e.g. `term_multimodal`, `term_voice_wake`, `term_realtime_transcription`, `term_voice_call`,
  `term_provider_plugin`, `term_failover`); plus 1–2 plain-text backlinks from non-term notes if any exist.
- **>200-line decomposition:** if any owned note exceeds 200 lines, decompose per Step 7 (procedure→`sop_*`,
  model/argument→`thought_*`); expected to stay moderate (80–150 lines), so unlikely.

### Acceptance — term-note authoring is NOT done if

Single-source (digest-doc-only) scope; Related Terms < 10 (moderate depth) or lacks cross-domain diversity;
no inlink expansion (Step 6e missed); `## References` contains `term_*.md` links or `## Related Terms`
contains external URLs; section ordering violated; YAML uses a forbidden field; `building_block` ≠ `concept`;
fleeting content without temporal qualifier; glossary Description > 5 sentences or has metrics; non-canonical
filename; substantive note overwritten instead of redirected; plain-text math instead of MathJax. (Full
acceptance list inherited from the capture-term-note canonical.)

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (owned term captures — BEFORE any digest note):** capture `term_voice_mode`,
  ≥10 Related Terms + glossary entry + Step-6e backlinks) → reindex → G1/G5 verify. These must exist before
  Notes authored after them cite them.
- **Phase 1 (voice pilot):** Note 1 (`hermes_voice_mode_cli`) FIRST — pilot → reindex → verify
  format/ghost/in-degree BEFORE the rest. Then Note 2. GATE G1–G8.
- **Phase 2 (TTS/STT model + procedure):** Notes 3, 4. GATE G1–G8.
- **Phase 3 (vision / image-gen / spotify / deliverable):** Notes 5, 6, 7, 8. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, G8):** add the inlinks from the Inlinks table; verify every new note +
  every owned term has DB in-degree ≥1 from outside the folder.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim for
kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify every
ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder (8 doc notes + 3 owned terms)
for n in hermes_voice_mode_cli hermes_voice_gateway_discord_vc hermes_tts_providers hermes_stt_transcription hermes_vision_image_paste hermes_image_generation hermes_spotify_integration hermes_deliverable_mode; do
for t in term_voice_mode term_text_to_speech term_speech_to_text; do
  echo -n "$t indeg(ext): "; sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM note_links WHERE target_id='resources/term_dictionary/$t.md';"; done
```

## Entry Point Decision (inherited)

Contributes 8 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c, >30-note
series) under a "Media (Voice / TTS / STT / Vision / Image-Gen / Spotify / Deliverable)" section. Parent hub
back-link in `entry_research_and_ai_hub.md` is handled at master level. SP08a does NOT create a separate
entry point — the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the
>30 threshold). The 3 owned term notes are indexed by their glossary (`acronym_glossary_llm.md`), not the
docs entry point.

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `snippet_hermes_agent_tools_voice_mode.md` | → `hermes_voice_mode_cli`, `hermes_voice_gateway_discord_vc` | voice-mode tool code ↔ voice usage docs |
| `snippet_hermes_agent_tools_tts_routing.md` | → `hermes_tts_providers` | TTS routing code ↔ TTS provider doc |
| `snippet_hermes_agent_tools_transcription.md` | → `hermes_stt_transcription` | transcription code ↔ STT doc |
| `snippet_hermes_agent_tools_vision_dispatch.md` | → `hermes_vision_image_paste` | vision dispatch code ↔ vision doc |
| `snippet_hermes_agent_tools_image_gen.md` | → `hermes_image_generation` | image-gen code ↔ image-gen doc |
| `snippet_hermes_agent_plugins_spotify.md` | → `hermes_spotify_integration` | Spotify plugin code ↔ Spotify doc |
| `snippet_hermes_agent_gw_delivery.md` | → `hermes_deliverable_mode` | gateway delivery code ↔ deliverable-mode doc |
| `term_voice_wake.md` | → `term_voice_mode` (contrast) | wake-word concept → real-time voice-mode (disambiguation) |
| `term_realtime_transcription.md` | → `term_speech_to_text` | generic transcription → Hermes STT subsystem |
| `term_multimodal.md` | → `term_text_to_speech`, `hermes_vision_image_paste` | multimodal concept → media term + vision doc |
| `repo_hermes_agent_tools.md` | → `hermes_tts_providers`, `hermes_image_generation`, `hermes_vision_image_paste` | tools repo ↔ media tool docs |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_voice_gateway_discord_vc`, `hermes_deliverable_mode` | gateway repo ↔ gateway media docs |
| `repo_hermes_agent_plugins.md` | → `hermes_spotify_integration`, `hermes_tts_providers` | plugins repo ↔ plugin-provider docs |
| `entry_code_snippets_hermes_agent.md` | → `hermes_voice_mode_cli`, `hermes_image_generation` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 8 notes | navigation hub |

Guarantees every new note (8 docs + 3 owned terms) in-degree ≥1 from outside the folder (G8). Inlink
addition is gated execution Phase 3b, not a recommendation. (Owned-term inlinks land via the Step-6e backlink
expansion during Phase 0 capture + the explicit term→term rows above.)

## Pacing Rules (inherited)

Phase 0 owned-term captures FIRST (so Notes citing them aren't ghosts). Pilot Note 1 (`hermes_voice_mode_cli`)
→ reindex → verify format/ghost/in-degree BEFORE authoring the rest. Commit per phase (per-wave commits for
multi-agent runs). Re-read the source page before writing each note — do NOT work from memory. Code blocks
verbatim for kept blocks; curate code-heavy notes (Note 3 from 20 blocks, Note 7 from 12) to ≤6 load-bearing
examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and split. If
multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP08a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 8 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `snippet_*` / `term_*` inlinks (G8);
  run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P2 wave: bidirectional-link the SP02 config note (`hermes_messaging_media_settings`) ↔ Notes 1–6
  (config block ↔ feature page) and SP11–13 messaging notes ↔ Notes 2/8 (gateway voice/deliverable delivery).
- Coordinate with SP08b (the `b` half): cross-link `hermes_overview` (SP08b) ↔ all SP08a notes once SP08b lands.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (LIKE false-positives `term_voice_wake`/`term_voice_call`/
  `term_realtime_transcription`/`term_computer_vision`/`term_api_gateway` confirmed by DB + master caution
  list), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc, all
  2026-06-19), Undigested Terms Plan (3 owned captures + specificity/collision audit), Term-Note Authoring
  Requirements (multi-source mandate, ≥10 Related Terms, Step-6e backlinks), Doc-Note Authoring Spec (derived
  from `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts (docs + owned terms), Inlinks.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  the interim 3-floor wording (≥8 term / ≥5 code-repo / ≥10 doc with snippets as a bonus): the SNIPPET group is
  PROMOTED from bonus to a COUNTED floor and raised from 8 to ≥10. Re-read all 6 source pages from
  `inbox/hermes_agent_docs/`; each note carries a Code-Repos (≥5) line from the 13 `repo_hermes_agent_*`
  source-code notes, a Snippets (≥10) line from the 517-note `snippet_hermes_agent_*` corpus, and a Docs (≥10)
  8 term / 5 repo / 10 snippet / 10 doc; smallest counts per note are exactly 8 / 5 / 10 / 10.
- Density re-read: counts match measured; **2 splits** (voice-mode→2, tts→2), no additional beyond planned.
  All 8 notes ≤2500w; code-heavy notes (3,7) curated to ≤6 blocks.
- Collision audit: **0 removals from the owned set** — all 3 owned slugs ABSENT in DB; the 4 LIKE hits are
  confirmed-different concepts (LINK not dup); SP08a captures NO vision/image-gen/transcription term (those
  concepts are existing or out-of-scope).
- Owned captures: **3** (`term_voice_mode`, `term_text_to_speech`, `term_speech_to_text`), all Phase 0.
- Undigested terms surfaced at augment: **0 new beyond the master inventory's SP08 set** (browser term →
  SP08b).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs
Inlinks (all 8 docs + 3 owned terms) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format
Def (derived) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms
Plan (3 owned) ✓ Capture Phase per term (Phase 0) ✓ best-fit glossary (acronym_glossary_llm) ✓ Term-Note Auth
Reqs (multi-source + ≥10 Related Terms) ✓ invokes capture-term-note (Phase 0) ✓ Entry-Point Decision ✓ matches
size threshold ✓ Slug Specificity (audit performed; no renames — master slugs already specific) ✓ Slug
Collision (4 LIKE false-positives + owned-slug absence confirmed) ✓ dedup generalized to ALL notes incl doc,
searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED (Phase 3b + Step-6e) ✓
Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 phases + Phase 3b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (8 rows under a Media section); parent hub at master level (matches >30 threshold); owned terms indexed by glossary. |
| CP4 | Plan size manageable | PASS | 8 notes ≤30; master holds the corpus-level split (SP08 split a/b — SP08a is the `a` half). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); term spec derived from capture-term-note canonical; not invented. |
| CP6 | Borderline density → split | PASS | voice-mode→2, tts→2; all notes ≤2500w; code-heavy notes (3 tts at ~2400w, 7 spotify) curated ≤6; Note 3 checked → cohesive single-BB model, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 (mirror c253b07): tts 4341, voice-mode 2850, spotify 2198, vision 1606, image-gen 1309 (was 1030; +279w/+2 code upstream growth), deliverable 850 — measured == master ledger. |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP08a owns 3 term captures (`term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`), each Phase 0 with best-fit glossary `acronym_glossary_llm`; Undigested Terms Plan + Term-Note Authoring Requirements sections present with multi-source MUST-language + ≥10 Related Terms + Step-6e backlinks. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 8 doc notes + 3 owned slugs (term_dictionary AND documentation/); 4 LIKE false-positives confirmed (voice_wake/voice_call/realtime_transcription/computer_vision/api_gateway = LINK not dup); owned slugs verified ABSENT; Renamed (none — already specific) + Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 8 docs + 3 owned terms from snippet_*/repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b + Step-6e, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

### Independent Re-Review (2026-06-19, FOUR-FLOOR re-augmentation)

Independent read-only review of the re-augmented sub-plan against the FOUR-FLOOR standard
(≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per planned note). All 8 notes machine-counted:
exactly 8 term (floor, excl. `+fin` owned) / 5 code-repo / 10 snippet / 10 doc each; every floor link
carries a `relevance:` clause (no bare links). Anti-fabrication: all 35 cited existing term IDs, the
active (`note_status LIKE 'active%'`); the 3 owned terms (`term_voice_mode`/`term_text_to_speech`/
`term_speech_to_text`) confirmed ABSENT (created Phase 0, correctly excluded from the floor). CP7 source
counts re-measured: tts 4341/20, spotify 2198/12, vision 1606/8, image-generation 1309/9, deliverable-mode
850/1 match the table exactly; voice-mode 2850w confirmed (raw 2874w − ~24w YAML frontmatter; the page's
5 in-body `---` horizontal rules trip a naive sed-range strip but the recorded body count is correct).

| CP | Result | Note |
|----|--------|------|
| CP2 | PASS | G1–G8 per phase incl G5-ghost (Script 4 DB-verify) + G6-broken + G8-indegree. |
| CP3 | PASS | Shares master-created `entry_hermes_agent_docs.md`; 8 Media rows. |
| CP4 | PASS | 8 notes ≤30. |
| CP5 | PASS | Authoring Spec derived from `cc_*` (cc_admin_enforcement_controls / cc_sandbox_modes verified active). |
| CP6 | PASS | voice→2, tts→2; all ≤2500w; code-heavy (3,7) curated ≤6. |
| CP7 | PASS | Re-measured; 5/6 exact, voice-mode 2850 confirmed correct. |
| CP8 / CP8f | PASS | 3 owned captures (ABSENT in DB), collision/specificity audit over term_dictionary + documentation/. |
| CP9 | PASS | Inlinks table covers all 8 docs + 3 owned terms from outside the folder. |

**RE-REVIEW RESULT: 9/9 → READY FOR EXECUTION (FOUR-FLOOR standard met; 0 fabricated links).**

## Re-Sync Note (2026-06-19)

Mirror re-downloaded from upstream `main` HEAD (commit c253b07, was pinned 95715dc); the inbox is
byte-identical to upstream. All 6 owned pages independently re-measured with the ledger convention
(body-only word count after stripping YAML frontmatter; code-block count = `^\s*```` lines / 2). One page in
this sub-plan's COUNTS scope changed upstream:

- `user-guide/features/image-generation.md` — 1030w/7code -> 1309w/9code (+279w, +2 code blocks).

The other 5 owned pages re-measured stable (spot-checked tts 4341w/20, voice-mode 2850w/18, spotify
2198w/12; vision 1606w/8 and deliverable-mode 850w/1 unchanged), matching the locked Source Pages table.

**Density re-decision:** NONE — no split added. Note 6 (`hermes_image_generation`, procedure) derives from
image-generation.md. The raw page grew ~27% but remains a single topically-cohesive procedure with heavy
link-outs (Tool Gateway→SP05, Nous Portal→SP14); re-estimated note body bumped ~1100→~1350w, still far below
the ≤2500w cap, and curated code stays ≤6 of 9 source blocks (≤6 cap intact). No cap breach, so the planned
note set, filenames, BB types, and split decisions (voice-mode→2, tts→2) are unchanged.

**Cross-ref floor (FOUR-FLOOR, set later same day, 2026-06-19):** The mirror re-measure left the source counts
(only image-generation grew) but the per-note cross-ref floor was subsequently **set to the FOUR-FLOOR
standard** by user directive: from the original ≥8 term + ≥8 snippet + ≥5 doc → **≥8 term + ≥5 code-repo +
≥10 snippet + ≥10 doc (all four COUNTED)**. The Per-Note Related Notes Mapping was re-built accordingly: a
Code-Repos (≥5) line per note (from the 13 `repo_hermes_agent_*` source-code notes), the Snippets line PROMOTED
from a bonus group to a COUNTED floor and raised from 8 to ≥10 (`snippet_hermes_agent_*` corpus), and each Docs
(`term_voice_mode`/`term_text_to_speech`/`term_speech_to_text`) are unaffected.

**Verdict:** plan remains **READY** for execution; only the image-generation counts (and its derived Note 6
estimate) and the provenance stamps were updated.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented FOUR-FLOOR 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; independent FOUR-FLOOR re-review 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/user-guide/features/{voice-mode,tts,vision,image-generation,spotify,deliverable-mode}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
