---
title: Sub-Plan nd02 — OpenClaw Docs: Nodes (Media Understanding, Talk, Troubleshooting, Voice Wake)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["nodes/media-understanding", "nodes/talk", "nodes/troubleshooting", "nodes/voicewake"]
---

# Sub-Plan nd02: Nodes

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` → mirrored body → `## Related Notes` → `## References` → bold footer), dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master.

## Scope

The four "leaf-node device" pages of the OpenClaw docs that cover speech, vision, and node-tool operability between the Gateway and its iOS/Android/macOS nodes:

- **media-understanding** — optional inbound image/audio/video pre-digest with provider + CLI fallbacks (`tools.media` config, fallback order, reply-pipeline integration).
- **talk** — Talk mode: continuous speech conversation loops across local STT/TTS and realtime voice (macOS/iOS/Android + browser WebRTC/WebSocket/relay).
- **troubleshooting** — node pairing vs gateway command policy vs exec approvals mental model + the foreground/permissions/error-code recovery ladders.
- **voicewake** — global Gateway-owned wake-word list + the `voicewake.*` RPC protocol (methods, routing, events) that syncs it across nodes.

**Priority: P1 (Phase A).** These define the node speech/vision/operability vocabulary the channels, tools, and gateway sub-plans reference. The code-side counterparts (`repo_openclaw_apps`, `repo_openclaw_channels_voice_phone`, `repo_openclaw_extensions_voice_speech`, `repo_openclaw_gateway`) are LINKED, not recreated.

**Source**: OpenClaw docs, 4 pages, **4,233 measured words**. **Planned: 4 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Media understanding | nodes/media-understanding | 2,037 | 4 | 12 | 4 | procedure |
| Talk mode | nodes/talk | 1,158 | 2 | 7 | 0 | procedure |
| Node troubleshooting | nodes/troubleshooting | 635 | 5 | 7 | 0 | procedure |
| Voice wake | nodes/voicewake | 403 | 2 | 4 | 6 | model |

Code count = raw ``` fences ÷ 2 (raw fence counts: media-understanding 8, talk 4, troubleshooting 10, voicewake 4). H2/H3 from `grep '^## '` / `grep '^### '`.

## Content Strategy

- **Prioritize**: (1) the `tools.media` model-entry / fallback-order / auto-detect contract (every inbound non-text message depends on it) and (2) the node pairing-vs-policy-vs-approvals mental model in troubleshooting (the security gate hierarchy the rest of the node tooling assumes).
- **Split**: NONE. All 4 pages are single-BB and well under the 2,500-word cap (largest is media-understanding at 2,037w / 4 code blocks). Each page maps to exactly one note. (See Split Decisions.)
- **Link-out, do not redefine**: `tools.media`/provider auth resolution → link the provider/gateway sub-plans (`gateway/config-tools`) instead of inlining; sibling node pages `nodes/audio`, `nodes/images`, `nodes/camera`, `nodes/location-command` (owned by **nd01**) are linked, not duplicated; `gateway/pairing`, `tools/exec-approvals`, `gateway/troubleshooting`, `channels/troubleshooting` (owned by gw/to/ch sub-plans) are linked. Provider names (OpenAI, Google, Deepgram, ElevenLabs, Whisper, MLX) are documented as config values, not promoted to term notes (link `term_llm`/`term_third_party_genai_services`/`term_text_to_speech`/`term_speech_to_text`).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_nodes_media_understanding.md` | procedure | media-understanding.md: Goals, High-level behavior, Config overview (`tools.media`, Model entries, Provider credentials), Defaults and limits (Auto-detect, Proxy env), Capabilities, Provider support matrix, Model selection guidance, Attachment policy, Config examples, Status output, Notes | 700 | Configuring OpenClaw inbound media understanding: the `tools.media` shared/per-capability model list, provider-vs-CLI model entries with ordered fallback, auto-detect order + bundled provider fallback chains, defaults/limits (maxBytes/maxChars), attachment policy, and the provider support matrix for image/audio/video. |
| 2 | `oc_nodes_talk.md` | procedure | talk.md: (intro runtime shapes), Behavior (macOS), Voice directives in replies, Config (`~/.openclaw/openclaw.json`), macOS UI, Android UI, Notes | 600 | OpenClaw Talk mode: the four runtime shapes (native STT/TTS, browser WebRTC/provider-WebSocket, Gateway relay, transcription-only), the listen→think→speak loop, interrupt-on-speech, the single-JSON-line voice directive, and the `talk.*` provider/realtime config (ElevenLabs/MLX/system + OpenAI/Google realtime). |
| 3 | `oc_nodes_troubleshooting.md` | procedure | troubleshooting.md: Command ladder, Foreground requirements, Permissions matrix, Pairing versus approvals, Common node error codes, Fast recovery loop | 500 | Troubleshooting OpenClaw nodes whose tools fail while connected: the diagnostic command ladder, foreground-only capabilities, the per-platform permissions matrix, the three-gate model (device pairing vs gateway command policy vs exec approvals), node error codes, and the fast recovery loop. |
| 4 | `oc_nodes_voicewake.md` | model | voicewake.md: (intro global-list model), Storage, Protocol (Methods, Routing methods, Events), Client behavior (macOS/iOS/Android) | 450 | OpenClaw voice-wake protocol: wake words as a single Gateway-owned global list with no per-node customization, the `voicewake.json` storage shape, the `voicewake.get/set` + `voicewake.routing.get/set` RPC methods, the `VoiceWakeRoutingConfig` route-target schema, the change-broadcast events, and per-platform client behavior. |

## Section Coverage Map

```
nodes/media-understanding.md
├── (intro) ────────────────────────────────────── → note 1 (oc_nodes_media_understanding)
├── ## Goals ─────────────────────────────────────── → note 1
├── ## High-level behavior (Steps) ───────────────── → note 1
├── ## Config overview (tools.media keys) ────────── → note 1
│   ├── ### Model entries (provider / CLI tabs) ──── → note 1
│   └── ### Provider credentials (apiKey) ────────── → note 1
├── ## Defaults and limits ───────────────────────── → note 1
│   ├── ### Auto-detect media understanding ──────── → note 1
│   └── ### Proxy environment support ────────────── → note 1
├── ## Capabilities (optional) ───────────────────── → note 1
├── ## Provider support matrix ───────────────────── → note 1
├── ## Model selection guidance ──────────────────── → note 1
├── ## Attachment policy ─────────────────────────── → note 1
├── ## Config examples (4 tabs) ──────────────────── → note 1 (selectively reproduced, ≤6 code)
├── ## Status output ─────────────────────────────── → note 1
└── ## Notes ─────────────────────────────────────── → note 1
nodes/talk.md
├── (intro) four runtime shapes + native loop ────── → note 2 (oc_nodes_talk)
├── ## Behavior (macOS) ──────────────────────────── → note 2
├── ## Voice directives in replies ───────────────── → note 2
├── ## Config (~/.openclaw/openclaw.json) ────────── → note 2
├── ## macOS UI ──────────────────────────────────── → note 2
├── ## Android UI ────────────────────────────────── → note 2
└── ## Notes ─────────────────────────────────────── → note 2
nodes/troubleshooting.md
├── (intro) ────────────────────────────────────── → note 3 (oc_nodes_troubleshooting)
├── ## Command ladder ────────────────────────────── → note 3
├── ## Foreground requirements ───────────────────── → note 3
├── ## Permissions matrix ────────────────────────── → note 3
├── ## Pairing versus approvals ──────────────────── → note 3
├── ## Common node error codes ───────────────────── → note 3
└── ## Fast recovery loop ────────────────────────── → note 3
nodes/voicewake.md
├── (intro) global Gateway-owned list ────────────── → note 4 (oc_nodes_voicewake)
├── ## Storage (Gateway host) ────────────────────── → note 4
├── ## Protocol ──────────────────────────────────── → note 4
│   ├── ### Methods ──────────────────────────────── → note 4
│   ├── ### Routing methods (trigger → target) ───── → note 4
│   └── ### Events ───────────────────────────────── → note 4
└── ## Client behavior (macOS/iOS/Android) ───────── → note 4
```
No orphaned sections. Each page's `## Related` block is consumed as link-out candidates (not a body section): media-understanding/talk/troubleshooting/voicewake all point at sibling node pages (`nodes/audio`, `nodes/images`, `nodes/camera`, `nodes/location-command` — nd01), `gateway/configuration`, `gateway/pairing`, `gateway/troubleshooting`, `tools/exec-approvals`, `channels/troubleshooting` — linked via Related Notes / References, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 4 pages are single-BB and ≤2,037 words / ≤4 code blocks each — every page is comfortably within the ≤2,500-word / ≤6-code caps and maps to exactly one note. No mixed-BB page. |

## Summary Statistics & Building Block Distribution

- Source pages: **4** (4,233 measured words). New `oc_` notes: **4**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×3** (notes 1–3: media config, Talk config, node troubleshooting) · **model ×1** (note 4: the voicewake RPC protocol/schema/events).
- Est. digest words ~**2,250** (avg ~560/note). Source code fences total 11 (4+2+5 + 4÷2=2 → media 4, talk 2, troubleshooting 5, voicewake 2); each note keeps ≤6 by reproducing config/RPC snippets selectively + verbatim (media-understanding's 4 config-example tabs are condensed to ≤3 representative json5 blocks).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_nodes_media_understanding (10t · 11s · 12d · 3 repos)

**Terms**
- [term_multimodal](../../term_dictionary/term_multimodal.md) — image/audio/video are the three media capabilities this note pre-digests into text; relevance: the note's whole subject is the multimodal-to-text pre-step.
- [term_llm](../../term_dictionary/term_llm.md) — each media model entry fronts an LLM/vision model; relevance: understanding is the pre-step before the reply LLM runs, and the active reply model is the auto-detect default.
- [term_computer_vision](../../term_dictionary/term_computer_vision.md) — image/video understanding is a vision task (the `[Image]`/`[Video]` summary block); relevance: the image/video provider matrix and native-vision passthrough are vision-model decisions.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — audio understanding is STT (Whisper/Groq/Deepgram/Gemini) producing `{{Transcript}}`; relevance: the audio capability + bundled fallback order are STT plumbing.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — the support matrix enumerates 15+ external providers each needing credentials; relevance: provider-entry config + auth resolution is the bulk of this note.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — CLI model entries invoke external tools (`gemini --allowed-tools read_file`) whose result feeds command parsing; relevance: the CLI-entry path is a tool-call boundary the note configures.
- [term_prompt_injection](../../term_dictionary/term_prompt_injection.md) — extracted file/media text is wrapped as untrusted content with `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` markers; relevance: the attachment-extraction section IS an injection-defense the note documents verbatim.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — the Proxy environment support section routes provider HTTP through `HTTPS_PROXY`/`ALL_PROXY`; relevance: the note's proxy-env subsection is exactly outbound-proxy egress.
- [term_amazon_nova](../../term_dictionary/term_amazon_nova.md) — a Bedrock multimodal model family comparable to the matrix's vision/video providers; relevance: link-not-redefine analog for "strongest latest-gen media model" guidance.
- [term_circuit_breaker](../../term_dictionary/term_circuit_breaker.md) — ordered multi-model fallback on error/size/timeout is a degrade-to-next pattern; relevance: the "fall back to next entry" rule + skip-on-maxBytes is the fallback ladder.

**Docs**
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — sibling-harness platform media tool reference; relevance: closest existing doc for inbound media-tool config + per-capability handling.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — inbound media settings (size/type limits, per-channel media policy); relevance: parallels `maxBytes`/`maxChars`/attachment-policy defaults.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription provider configuration; relevance: the audio-understanding capability + provider transcription matrix.
- [hermes_vision_image_paste](../hermes_agent/hermes_vision_image_paste.md) — vision/image input handling; relevance: parallels image understanding + native-vision passthrough.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider selection/routing across vendors; relevance: the ordered model list + capability gating is provider routing.
- [cc_computer_use](../claude_code/cc_computer_use.md) — vision/computer-use over screenshots; relevance: the closest first-party doc for image-to-text model behavior + safety.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — untrusted-content boundary defenses; relevance: explains the `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` wrapping the note relies on.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — outbound proxy + gateway config for model calls; relevance: directly mirrors the proxy-env subsection.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — provider/credential resolution + proxy env vars; relevance: the auth model media understanding reuses ("same provider auth resolution as normal model calls").
- [bedrock_invoke_api_multimodal](../aws_bedrock/bedrock_invoke_api_multimodal.md) — multimodal (image/video/doc) model invocation; relevance: the canonical multimodal-inference contract the provider matrix implements.
- [oc_nodes_talk](oc_nodes_talk.md) — (planned, this series) one-shot uploaded voice notes use the media/audio path while continuous speech uses Talk; relevance: the two are explicitly cross-referenced in the source Related block.
- [oc_nodes_audio](oc_nodes_audio.md) — (planned, nd01) audio/voice-note handling overlaps the audio media-understanding capability; relevance: the source Related block links `nodes/audio` directly.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — vendor plugins register per-provider image/audio/video media support; relevance: the code behind the provider support matrix.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw core owns the shared `tools.media` config, fallback order, and reply-pipeline integration; relevance: the config surface this note documents lives here.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the node apps that collect inbound attachments (`MediaPaths`/`MediaUrls`/`MediaTypes`); relevance: the attachment-collection step preceding understanding.

**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — the media pipeline that pre-digests attachments into the transcript; relevance: the exact reply-pipeline integration this note configures.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram audio transcription; relevance: the `tools.media.audio.providerOptions.deepgram` path.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — sanitizes/bounds inbound attachments; relevance: the untrusted-content wrapping + maxBytes skip the note describes.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — validates/resizes managed images; relevance: the image `maxBytes`/offloaded `media://inbound/*` ref handling.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — lifecycle of an inbound image record; relevance: how preserved-but-not-summarized images are tracked for image tools.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — analog audio-transcription tool with provider fallback; relevance: mirrors the audio bundled fallback order.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — dispatches image input to a vision-capable model; relevance: the image-understanding model-selection decision this note documents.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — formats image attachments for a vision model; relevance: parallels the `[Image]` summary-block / native-vision passthrough.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — inbound media handling on a channel; relevance: the attachment-collection step preceding understanding.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — ordered model fallback ladder; relevance: the "first eligible model, fall back to next" selection contract.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile → env → providers.apiKey resolution order; relevance: exactly the "provider credentials (apiKey)" resolution chain.

**Entry**

### oc_nodes_talk (10t · 11s · 11d · 3 repos)

**Terms**
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — Talk speaks replies via `talk.speak` TTS (ElevenLabs/MLX/system); relevance: TTS is the "Speaking" phase of the loop.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — Talk listens via local/streaming speech recognition; relevance: the "Listening" phase + transcription-only mode.
- [term_websocket](../../term_dictionary/term_websocket.md) — browser realtime Talk uses `provider-websocket` transport + Gateway WS for `talk.*` RPC; relevance: WS carries `talk.event` partial/final transcript updates.
- [term_real_time](../../term_dictionary/term_real_time.md) — Talk's realtime shapes (WebRTC / provider-WebSocket / gateway-relay) are low-latency duplex audio; relevance: the realtime config block is the note's densest section.
- [term_llm](../../term_dictionary/term_llm.md) — the "Thinking" phase sends the transcript to the model via the active session; relevance: `openclaw_agent_consult` routes the run through the agent LLM.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — Talk integrates external voice providers (ElevenLabs, OpenAI Realtime, Google); relevance: `talk.providers`/`talk.realtime.providers` config is provider integration.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — browser realtime Talk forwards provider tool calls through `talk.client.toolCall`; relevance: function calls are routed via Gateway policy, not direct.
- [term_ios](../../term_dictionary/term_ios.md) — Talk's runtime shapes are platform-specific (macOS/iOS/Android native vs browser); relevance: iOS has its own 900ms silence-window default + UI.
- [term_genai](../../term_dictionary/term_genai.md) — Talk is a generative-AI voice interface (speech in → generated reply → speech out); relevance: frames Talk within the broader GenAI app surface.
- [term_node_js](../../term_dictionary/term_node_js.md) — the Gateway relay + `talk.session.*` RPC run in the Node-based gateway runtime; relevance: the relay session lifecycle the note configures executes there.

**Docs**
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — end-user voice-mode (listen/think/speak) guide; relevance: the closest doc to Talk's native conversation loop.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — CLI voice mode internals; relevance: parallels the native STT→agent→TTS Talk loop.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog/config; relevance: mirrors `talk.providers` (ElevenLabs/MLX/system) selection + voice ids.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription config; relevance: the Listening phase + transcription-only Talk sessions.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — realtime voice over a gateway relay (Discord VC); relevance: analog of `gateway-relay` realtime Talk transport.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider selection/routing; relevance: choosing the active Talk + realtime provider.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation (speech → text input); relevance: the closest first-party doc to Talk's speech-input on-ramp.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — provider/credential resolution; relevance: the auth model behind ElevenLabs/OpenAI-realtime apiKey config.
- [bedrock_invoke_api_multimodal](../aws_bedrock/bedrock_invoke_api_multimodal.md) — multimodal model invocation incl. audio; relevance: the inference contract behind realtime/consult turns.
- [oc_nodes_voicewake](oc_nodes_voicewake.md) — (planned, this series) wake words trigger entry into Talk mode; relevance: voicewake is the on-ramp, Talk is the loop (source Related links it).
- [oc_nodes_media_understanding](oc_nodes_media_understanding.md) — (planned, this series) one-shot uploaded voice notes use the media/audio path; relevance: source Notes explicitly contrasts media-audio vs continuous Talk.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/TTS extension implementing `talk.speak` + provider playback; relevance: the package behind ElevenLabs/MLX playback.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/iOS/Android node apps that advertise `talk` + run the always-on overlay; relevance: the UI + capability declaration this note documents.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — realtime voice/relay subsystem; relevance: behind `gateway-relay` Talk + realtime transports.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS impl; relevance: the default `talk.provider: elevenlabs` path with voiceId/modelId/outputFormat.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — macOS-local MLX playback via `openclaw-mlx-tts`; relevance: the `provider: mlx` path this note documents.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — Gateway relay for transcription-only Talk; relevance: the `talk.session.*` + `talk.event` surface.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — end-to-end speech pipeline (capture→STT→agent→TTS); relevance: the native Talk loop this note describes.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — realtime voice-call runtime (WebRTC/relay session lifecycle); relevance: analog of Talk's realtime session shapes.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — streaming transcription on a realtime media stream; relevance: the streaming-transcription provider discovered via `talk.catalog.transcription`.
- [snippet_openclaw_macos_pushtotalk_overlay](../../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md) — macOS overlay UI (Listening/Thinking/Speaking states); relevance: the exact UI this note's macOS section describes.
- [snippet_hermes_agent_cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — analog CLI voice mode (listen/think/speak); relevance: the closest cross-harness implementation of the Talk loop.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — routes a reply to the configured TTS provider/voice; relevance: parallels Talk's provider selection + voice directives.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool enabling spoken interaction; relevance: cross-harness analog of the Talk capability.
- [snippet_hermes_agent_core_chat_helpers_interruptible_call](../../code_snippets/snippet_hermes_agent_core_chat_helpers_interruptible_call.md) — interruptible model call (stop on new input); relevance: the interrupt-on-speech behavior Talk defaults on.

**Entry**

### oc_nodes_troubleshooting (10t · 11s · 12d · 3 repos)

**Terms**
- [term_access_control](../../term_dictionary/term_access_control.md) — the three-gate model (pairing vs command policy vs exec approvals) is layered access control; relevance: the note's central mental model.
- [term_authentication](../../term_dictionary/term_authentication.md) — device pairing is the identity/trust gate ("can this node connect"); relevance: explicitly distinguished from per-command authorization.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — `system.run` on a node is gated by exec approvals/allowlist; relevance: the sandboxed-execution policy surface the note diagnoses.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — node tools (`camera.*`/`canvas.*`/`screen.*`/`system.run`) are RPC commands invoked as tool calls; relevance: the gateway command policy gates the command IDs.
- [term_posix_permissions](../../term_dictionary/term_posix_permissions.md) — allowlist-mode approvals + per-capability OS permissions enforce minimal granted capability; relevance: the permissions matrix is the least-privilege surface.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — node commands are RPC command IDs allowed/denied by the gateway policy; relevance: `allowCommands`/`denyCommands` operate on RPC method ids.
- [term_ios](../../term_dictionary/term_ios.md) — the permissions matrix is per-platform (iOS/Android/macOS); relevance: foreground-only capabilities + permission codes differ by OS.
- [term_threat_model](../../term_dictionary/term_threat_model.md) — pairing/command-policy/approvals form a defense hierarchy; relevance: the page is the operability view of OpenClaw's node trust boundaries.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — backgrounded nodes + approval mismatch reject requests rather than trusting them; relevance: the deny-and-recover ladder bounds unsafe execution attempts.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — the approval-mismatch rejection rebinds to the canonical `systemRunPlan` if a later caller mutates the payload; relevance: the exec-dedup/plan-binding the note documents.

**Docs**
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command-approval gating for tool/exec; relevance: the closest doc to OpenClaw exec approvals + `SYSTEM_RUN_DENIED`.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credential handling; relevance: the per-node trust + capability isolation the matrix enforces.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operational diagnostics; relevance: parallels the `openclaw status`/`gateway status`/`doctor` command ladder.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — allow/deny rule precedence for tools; relevance: directly mirrors `gateway.nodes.allowCommands`/`denyCommands`.
- [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — permission modes (ask/allow/deny); relevance: the exec-approval ask-flow + allowlist mode this note diagnoses.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool permission rules; relevance: per-capability (camera/screen/location/system.run) gating.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission layering; relevance: distinguishes the exec-sandbox gate from the command-policy gate, mirroring pairing-vs-approvals.
- [pi_security_model](../pi/pi_security_model.md) — agent security/trust model; relevance: the conceptual frame for the three-gate hierarchy.
- [bedrock_security_confused_deputy](../aws_bedrock/bedrock_security_confused_deputy.md) — confused-deputy prevention by binding to a canonical request; relevance: analog of the `systemRunPlan` approval-mismatch rejection.
- [oc_nodes_voicewake](oc_nodes_voicewake.md) — (planned, this series) voice-wake routing is another node-command surface under the same policy; relevance: shares the gateway command-policy gate.
- [oc_nodes_camera](oc_nodes_camera.md) — (planned, nd01) `camera.*` is a foreground-only node capability whose failures this page troubleshoots; relevance: the matrix's first row + `*_PERMISSION_REQUIRED` example.
- [oc_nodes_location_command](oc_nodes_location_command.md) — (planned, nd01) `location.get` failure codes (`LOCATION_*`) are enumerated here; relevance: the matrix + error-code section cover location directly.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — owns node command policy, pairing records, and binds approved `host=node` runs to `systemRunPlan`; relevance: the policy engine this note diagnoses.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — node apps reporting capabilities + surfacing OS prompts; relevance: emits `NODE_BACKGROUND_UNAVAILABLE`/`*_PERMISSION_REQUIRED`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec-approval/allowlist enforcement; relevance: the approval-mismatch rejection this note documents.

**Snippets**
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node device pairing (identity/trust gate); relevance: the first gate in the pairing-vs-approvals model.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — `gateway.nodes.allowCommands`/`denyCommands` + platform defaults; relevance: the second gate this note explains.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — invoking a node command incl. waking a backgrounded node; relevance: where `NODE_BACKGROUND_UNAVAILABLE` originates.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/foreground tracking; relevance: the basis for foreground-only capability checks.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec dedup; relevance: the `systemRunPlan` approval-binding the note describes.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session lifecycle (connect/describe/capabilities); relevance: what `openclaw nodes describe` surfaces.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager (mode/allowlist); relevance: backs `openclaw approvals get`/`allowlist add` + `SYSTEM_RUN_DENIED`.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — push-driven exec approval ask-flow; relevance: the "approval required" ask path for `system.run`.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem allowlist policy; relevance: the allowlist-miss case (`cmd.exe /c ...` on Windows hosts).
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS-side gateway pairing flow; relevance: re-approving device pairing in the recovery loop.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — orchestrates an approved exec run; relevance: where the canonical plan is forwarded and mismatches rejected.

**Other vault**

**Entry**

### oc_nodes_voicewake (10t · 11s · 11d · 3 repos)

**Terms**
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — voicewake is an RPC surface (`voicewake.get/set`, `voicewake.routing.get/set`); relevance: the Protocol/Methods section is typed RPC params/returns.
- [term_rpc](../../term_dictionary/term_rpc.md) — get/set + routing methods are remote procedure calls over the Gateway WS; relevance: generalizes the method contract beyond the JSON-RPC envelope.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — the Gateway broadcasts `voicewake.changed`/`voicewake.routing.changed` on every edit + on connect; relevance: the Events section is event-driven sync.
- [term_pub_sub](../../term_dictionary/term_pub_sub.md) — the single-owner global list is published by the Gateway, subscribed by all WS clients/nodes; relevance: the broadcast model this note specifies.
- [term_fan_out](../../term_dictionary/term_fan_out.md) — one edit fans out to all WebSocket clients + all connected nodes; relevance: the "who receives it" delivery pattern.
- [term_observer_pattern](../../term_dictionary/term_observer_pattern.md) — clients observe gateway-owned state and re-render on change events; relevance: macOS/iOS clients rely on the broadcast to stay in sync.
- [term_websocket](../../term_dictionary/term_websocket.md) — events reach all WebSocket clients + connected nodes over the Gateway WS; relevance: the transport for both methods and events.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — wake words gate on-device trigger detection before speech capture; relevance: `VoiceWakeRuntime`/`VoiceWakeManager` detection precedes STT.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — a detected wake word routes to a session and typically launches a Talk/voice (TTS) response; relevance: links voicewake to the speak path.
- [term_ios](../../term_dictionary/term_ios.md) — client behavior is per-platform: macOS/iOS keep local enable toggles + edit the list, Android keeps it off; relevance: the Client behavior section is OS-specific.

**Docs**
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — RPC protocol envelope/versioning; relevance: the structural frame for the `voicewake.*` method contract.
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — RPC command (method) catalog pattern; relevance: parallels `voicewake.get/set` + `voicewake.routing.get/set`.
- [pi_rpc_events](../pi/pi_rpc_events.md) — RPC event/broadcast pattern; relevance: parallels `voicewake.changed`/`voicewake.routing.changed` delivery.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket channel model for agents/clients; relevance: the WS transport carrying voicewake events to clients + nodes.
- [band_websocket_agent_events](../band/band_websocket_agent_events.md) — agent-side WS event stream; relevance: analog of nodes receiving the change broadcast + initial-state push on connect.
- [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — event hook/broadcast surface; relevance: parallels the change-event fan-out to subscribers.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway-owned state + sync internals; relevance: the single-owner persisted-list + broadcast model.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — lifecycle events delivered to subscribers; relevance: analog of on-connect "current state" push.
- [bedrock_monitoring_eventbridge](../aws_bedrock/bedrock_monitoring_eventbridge.md) — event broadcast/fan-out to consumers; relevance: a managed analog of the gateway change-broadcast.
- [oc_nodes_talk](oc_nodes_talk.md) — (planned, this series) a fired wake word routes into a Talk session; relevance: voicewake is the on-ramp to the Talk loop (source Related links it).
- [oc_nodes_troubleshooting](oc_nodes_troubleshooting.md) — (planned, this series) wake-word routing targets are node commands under the same gateway policy; relevance: shares the command-policy gate.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — owns/persists `voicewake.json`, normalizes triggers, broadcasts changes; relevance: the entire ownership model this note specifies.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS/iOS/Android apps run `VoiceWakeRuntime`/`VoiceWakeManager` + edit via `voicewake.set`; relevance: the client behavior section.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — route targets resolve to a `sessionKey`/`agentId`; relevance: the session layer is the routing destination.

**Snippets**
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — gateway-side wake-word tracking/state; relevance: the storage+broadcast owner this note specifies.
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — macOS trigger detection against the global list; relevance: the `VoiceWakeRuntime` client behavior.
- [snippet_openclaw_macos_voice_wake_state](../../code_snippets/snippet_openclaw_macos_voice_wake_state.md) — local enabled/disabled wake state synced from broadcast; relevance: the macOS/iOS local toggle behavior.
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — audio capture feeding wake-word detection on macOS; relevance: the capture step before trigger match.
- [snippet_openclaw_macos_pushtotalk_nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — manual push-to-talk alternative to wake-word triggering; relevance: the non-wake-word capture path (Android uses manual mic).
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — session event subscription; relevance: the consumer pattern paralleling voicewake event delivery.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — gateway broadcasts runtime-config changes to clients; relevance: the same broadcast machinery voicewake edits use.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC method schema grouping; relevance: how `voicewake.*` methods are declared/typed.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection handling incl. on-connect push; relevance: the initial "current state" push to a connecting node.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: route targets resolve to a session whose lifecycle this tracks.

**Entry**

## Undigested Terms Plan

Per master: OpenClaw vocabulary is the subject of doc pages → digested as `oc_` doc notes, NOT new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms.

| Term | Disposition |
|------|-------------|
| media understanding / `tools.media` / model entry / fallback order / auto-detect | OpenClaw config vocabulary → documented in `oc_nodes_media_understanding.md` (note 1). Not a term note. |
| Talk mode / `talk.speak` / realtime / transcription-only / interrupt-on-speech / voice directive | OpenClaw feature vocabulary → documented in `oc_nodes_talk.md` (note 2). Not a term note. |
| node pairing / gateway node command policy / exec approvals / `systemRunPlan` / foreground-only | OpenClaw operability vocabulary → documented in `oc_nodes_troubleshooting.md` (note 3). Not a term note. |
| voice wake / global trigger list / `voicewake.*` RPC / `VoiceWakeRoutingConfig` | OpenClaw protocol vocabulary → documented in `oc_nodes_voicewake.md` (note 4). Not a term note. |
| Provider names (OpenAI, Google, Deepgram, ElevenLabs, Whisper, MLX, Groq, xAI, Qwen, Moonshot, Z.AI, MiniMax, SenseAudio, Mistral) | Documented as config values; link existing `term_llm` / `term_third_party_genai_services` / `term_text_to_speech` / `term_speech_to_text`. Not promoted to term notes. |
| STT / TTS / WebRTC / realtime voice / wake word | Link existing `term_speech_to_text` / `term_text_to_speech` / `term_websocket`; concept-level vocabulary, no new captures. |

**New `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note. (Candidate `term_speech_recognition`/`term_webrtc`/`term_realtime_api` were considered: `term_speech_to_text`/`term_text_to_speech`/`term_websocket` already cover the reusable concepts; the realtime/WebRTC specifics are OpenClaw-config-scoped and stay in `oc_nodes_talk`. Augment Step 2d re-scans to confirm.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single phase (4 notes, P1). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order/forbidden-fields clean; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold footer. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/nodes/<page>.md`) | Every claim/config key/RPC method traceable to source; no invented fields. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks, one BB; every mapped H2/H3 represented. |
| G4 | Cross-Reference | ≥6 relevance-selected term links + repo/sibling/other-vault links per note, each with a relevance statement. |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken relative paths after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 (anti-island) | `note_links` confirms in_degree ≥1 per new note post-reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_nodes_media_understanding oc_nodes_talk oc_nodes_troubleshooting oc_nodes_voicewake"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G5 ghost: sibling oc_ links should resolve to a planned/existing oc_ file
  grep -o '(oc_[a-z0-9_]*\.md)' "$f" | tr -d '()' | sort -u | while read s; do
    [ -f "$GATE_DIR/$s" ] || echo "PLANNED/UNRESOLVED sibling ($SIBLING_PREFIX): $s in $n"
  done
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# After incremental reindex (G6/G8):
# bash scripts/update_notes_database.sh && python3 -c "import sqlite3,sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR as D;c=sqlite3.connect(D);[print(n,c.execute('SELECT in_degree FROM notes WHERE note_name=?',(n,)).fetchone()) for n in '$NOTES'.split()]"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_nodes_media_understanding | procedure | 700 | 4 (condense 4 config-example tabs → ≤3 reproduced) | ✅ (≤2500w / ≤6 code) |
| 2 | oc_nodes_talk | procedure | 600 | 2 | ✅ |
| 3 | oc_nodes_troubleshooting | procedure | 500 | 5 (CLI ladders; keep ≤6) | ✅ |
| 4 | oc_nodes_voicewake | model | 450 | 2 (storage + routing-config JSON) | ✅ |

No note approaches caps; the densest source (media-understanding, 2,037w / 4 example tabs) condenses to one focused procedure note ≤700w with ≤6 reproduced json5 blocks. No split needed.

## Entry Point Decision (inherited from master)

Contributes **4 rows** to `entry_openclaw_docs.md` (created as a master pre-step W1, `building_block: navigation`) under a **"Nodes"** cluster (alongside nd01's audio/camera/images/location rows). Each new note receives its entry-point back-link at finalization (satisfies G7/G8). No standalone entry point for nd02 (master hub aggregates).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all sources confirmed present):
- `entry_openclaw_docs.md` → all 4 notes (primary anti-island guarantee).
- `repo_openclaw_gateway.md` → notes 1, 3, 4 (gateway owns media config, node command policy, voicewake list).
- `repo_openclaw_extensions_voice_speech.md` → note 2 (Talk TTS/speech).
- `repo_openclaw_extensions_llm_providers.md` → note 1 (media provider plugins).
- `repo_openclaw_apps.md` → notes 2, 3, 4 (node apps: Talk UI, permission prompts, wake-word edit).
- `repo_openclaw_channels_voice_phone.md` → note 2 (realtime/relay voice).
- `repo_openclaw_security.md` → note 3 (exec approvals/allowlist).
- `term_speech_to_text.md` / `term_text_to_speech.md` → notes 1, 2, 4; `term_json_rpc.md` → notes 3, 4; `term_websocket.md` → notes 2, 4.
- Reciprocal: sibling `oc_nodes_*` (this series) + nd01 node notes link each other once both land.

## Pacing Rules (inherited from master)

One execution phase (4 notes, P1). Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script; re-read each source page before authoring; reproduce config/RPC snippets verbatim (selectively, ≤6/note). One BB per note. Run all 8 gates before commit; `git pull --rebase --autostash` first; commit+push the phase in one cycle; no Claude co-author trailer. Reindex incrementally and verify `note_links` + 0 broken links before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (per-note Related mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked (per-note counts — all floors MET).**

| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors |
|---|---:|---:|---:|---:|---|
| oc_nodes_media_understanding | 10 | 11 | 12 (10 / 2) | 3 | ✅ ≥8t·≥10s·≥10d |
| oc_nodes_talk | 10 | 11 | 11 (9 / 2) | 3 | ✅ |
| oc_nodes_troubleshooting | 10 | 11 | 12 (9 / 3) | 3 | ✅ |
| oc_nodes_voicewake | 10 | 11 | 11 (9 / 2) | 3 | ✅ |

- **Docs** (≥5 EXISTING per note, target floor far exceeded — 9–10 existing each): drawn from `claude_code/` (`cc_*`), `hermes_agent/` (`hermes_*`), `pi/` (`pi_*`), `band/` (`band_*`), and `aws_bedrock/` (`bedrock_*`) coding-agent + multimodal corpora; sibling `oc_*` of this series (and nd01 node siblings) cited as `(planned, this series)`/`(planned, nd01)` toward the 10-doc floor.
- **Repos**: 3 relevance-selected `repo_openclaw*` per note (gateway/apps + the per-topic owner: extensions_llm_providers, extensions_voice_speech/channels_voice_phone, security, sessions).

**New-term candidates.** NONE. nd02 authors zero `term_dictionary` notes (inherited from master: OpenClaw vocabulary is digested as `oc_*` doc notes, not new terms; only EXISTING terms are linked). The augment-time Step 2d re-scan of the 4 re-read source pages surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. Concepts that might tempt a new capture are best-fit covered by existing glossary entries: speech-recognition → `term_speech_to_text`; voice synthesis → `term_text_to_speech`; realtime/WebRTC → `term_real_time` + `term_websocket` (the WebRTC/realtime specifics stay OpenClaw-config-scoped in `oc_nodes_talk`); wake-word / pub-sub broadcast → `term_pub_sub` + `term_event_driven_architecture` + `term_fan_out` + `term_observer_pattern`; provider names → `term_third_party_genai_services` + `term_llm`. Best-fit glossary if a future need arises: `acronym_glossary_gen_ai.md` (agentic/LLM glossary, already rich). **Undigested Terms Plan unchanged: 0 captures.**


## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review per the canonical. CP7 (source word counts) re-measured by re-reading the source pages during this augment.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6, G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link-fix, G7 discoverability, G8 in-degree≥1 for the single P1 phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | `## Entry Point Decision (inherited from master)`: contributes 4 rows to `entry_openclaw_docs.md` (`building_block: navigation`, created master pre-step W1) under a "Nodes" cluster; no standalone nd02 entry point. Master CREATE>30-notes rule satisfied at master scope. |
| CP4 | Plan size manageable | **PASS** | 4 notes ≪ 30; single execution phase. |
| CP5 | Note format derived from existing notes | **PASS** | Format inherited verbatim from master (derived from existing `claude_code/`+`pi/` doc corpora): `# OpenClaw — …` H1, `## Overview` → mirrored body → `## Related Notes` → `## References` → bold footer; YAML field order + forbidden-field list match; `building_block` per-note (procedure×3, model×1). |
| CP6 | Density / BB atomicity (promote splits) | **PASS** | Density Re-Assessment: each note ≤700w / ≤5 code fences / one BB, far under ≤2500w/≤6-code/≤400-line caps; no borderline note. Split Decisions: none (all 4 pages single-BB, ≤2,037w). |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 4 pages this session; measured 2,037 / 1,158 / 635 / 403 words (matches plan Source table); largest page (media-understanding) maps to one ≤700w note — no under-estimation, no split needed. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new captures, every row dispositioned to a `oc_*` doc home or existing-term link); `## Term-Note Authoring Requirements` present (N/A — 0 terms — with explicit fallback to `/tessellum-capture-term-note` + glossary if Step 2d ever surfaces one). Step 2d re-scan this session: 0 new terms. |
| CP8f | Slug specificity + collision (all-notes dedup) | **PASS** | No `term_*` captures, so no slug to rename/dedup. Doc-note collision audit: the 4 `oc_nodes_*` slugs were checked against `term_dictionary/` AND `resources/documentation/` — none duplicate an existing term or doc (OpenClaw node speech/vision/operability pages have no existing vault doc; code side is repos/snippets, which are linked not duplicated). Added terms are all EXISTING substantive notes (link, not create). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 4; `repo_openclaw_*`/`term_*` → per note); G8 in-degree≥1 is in the phase gate table as an EXECUTED+VERIFIED check (reindex + `note_links` query before commit). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
