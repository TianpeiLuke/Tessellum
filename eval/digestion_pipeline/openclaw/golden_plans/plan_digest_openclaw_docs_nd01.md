---
title: Sub-Plan nd01 — OpenClaw Docs: Nodes (Audio, Camera, Images, Location)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["nodes/audio", "nodes/camera", "nodes/images", "nodes/location-command"]
---

# Sub-Plan nd01: Nodes

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup, the 9-GATE, cross-references,
> Undigested-Terms ownership, and entry-point decision are ALL inherited from the master; only this sub-plan's
> page-specific decisions are recorded here (authored from a fresh re-read + measurement of its 4 source pages).

## Scope

The 4 **device-node media/sensor command** pages of the OpenClaw docs: inbound audio/voice-note transcription
(`nodes/audio`), camera photo/video capture on iOS/Android/macOS nodes (`nodes/camera`), the WhatsApp-web
image/media send-and-reply pipeline (`nodes/images`), and the `location.get` node command + permission model
(`nodes/location-command`). **Priority P1 (Phase A)** — these define how paired device nodes capture and feed
media/sensor data through the Gateway `node.invoke` surface that the CLI, tools, and channels docs reference.
The code-side counterparts (`repo_openclaw_extensions_voice_speech`, `repo_openclaw_channels_messaging`,
`repo_openclaw_gateway`) are LINKED, not recreated.

**Source**: OpenClaw docs, 4 pages, **2,820 measured words** (frontmatter excluded). **Planned: 4 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| audio | nodes/audio | 1,094 | 6 | 6 | 8 | procedure |
| camera | nodes/camera | 801 | 3 | 6 | 9 | procedure |
| images | nodes/images | 554 | 0 | 7 | 0 | procedure |
| location-command | nodes/location-command | 371 | 2 | 9 | 0 | procedure (+ model: `location.get` request/response schema) |

(Word counts exclude YAML frontmatter; `Code` = raw ``` fences ÷ 2.)

## Content Strategy

- **Prioritize**: the audio transcription auto-detection order + provider/CLI fallback (every voice note
  depends on it, including the group-mention preflight gate) and the camera `node.invoke` command surface
  (`camera.list`/`snap`/`clip` params, payload guards, foreground/permission rules) — the most reused,
  highest-density material.
- **Split**: **none.** All 4 pages are well under the 2,500-word cap (largest = audio at 1,094 w) and each is a
  single procedure building block; 1 page → 1 note. (Master estimated 6 notes for nd01; the measured pages
  are small and single-BB, so the true count is **4** — locked at augment.)
- **Link-out (not duplicated)**: provider setup pages (`/providers/groq`, `/providers/deepgram`,
  `/providers/mistral`, `/providers/senseaudio`) → providers sub-plans (pr01–pr09); `nodes/media-understanding`,
  `nodes/talk`, `nodes/voicewake` → sibling sub-plan **nd02**; `channels/location` → channels sub-plan ch03;
  Gateway `node.invoke` mechanics → gateway sub-plans (gw0x); model-auth order (`models.providers.*.apiKey`,
  auth profiles, env vars) → existing `term_authentication`/`term_oauth_token` + providers sub-plans.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_nodes_audio.md` | procedure | nodes/audio.md (all H2/H3) | 700 | Inbound audio/voice-note transcription: the media-understanding flow (download → maxBytes → first eligible model → fallback → `{{Transcript}}`), auto-detection order (active model / local CLIs / provider fallback), config examples (provider + CLI), scope gating, echo-transcript, proxy support, and the group mention-detection preflight. |
| 2 | `oc_nodes_camera.md` | procedure | nodes/camera.md (all H2/H3) | 600 | Camera capture on iOS / Android / macOS nodes via Gateway `node.invoke`: `camera.list`/`camera.snap`/`camera.clip` params and response payloads, per-platform user settings + runtime permissions, foreground requirement, payload guards, the `openclaw nodes camera` CLI helper, and macOS OS-level screen recording. |
| 3 | `oc_nodes_images.md` | procedure | nodes/images.md (all H2) | 500 | Image and media send/reply pipeline on the WhatsApp-web (Baileys) channel: `openclaw message send --media` CLI surface, per-type send caps (image/audio/video/document), auto-reply media fan-out, inbound-media-to-command templating (`{{MediaPath}}`/`{{MediaUrl}}`, sandbox rewrite), and media-understanding caps. |
| 4 | `oc_nodes_location_command.md` | procedure | nodes/location-command.md (all H2) | 450 | The `location.get` node command: en/whileUsing selector + precise toggle, OS-permission mapping, request params and response schema, stable error codes, Android foreground/background behavior, and the `nodes` tool `location_get` action + CLI. |

Filename rule applied (master): `oc_` + full slug with `/` and `-` → `_` (e.g. `nodes/location-command` →
`oc_nodes_location_command`). One BB per note (all procedure; note 4 embeds a request/response model as a
sub-section, but the dominant BB is the procedure of invoking the command).

## Section Coverage Map

```
nodes/audio.md
├── What works ─────────────────────────────────────────── → note 1 (oc_nodes_audio)
├── Auto-detection (default) ───────────────────────────── → note 1
├── Config examples ────────────────────────────────────── → note 1
│   ├── Provider + CLI fallback (OpenAI + Whisper CLI) ──── → note 1
│   ├── Provider-only with scope gating ────────────────── → note 1
│   ├── Provider-only (Deepgram) ───────────────────────── → note 1
│   ├── Provider-only (Mistral Voxtral) ────────────────── → note 1
│   ├── Provider-only (SenseAudio) ─────────────────────── → note 1
│   └── Echo transcript to chat (opt-in) ───────────────── → note 1
├── Notes and limits ───────────────────────────────────── → note 1
│   └── Proxy environment support ──────────────────────── → note 1
├── Mention detection in groups ────────────────────────── → note 1
├── Gotchas ────────────────────────────────────────────── → note 1
└── Related ────────────────────────────────────────────── → note 1 (→ nd02: media-understanding/talk/voicewake)
nodes/camera.md
├── iOS node (User setting / Commands / Foreground / CLI helper) → note 2 (oc_nodes_camera)
├── Android node (user setting / Permissions / foreground / commands / Payload guard) → note 2
├── macOS app (User setting / CLI helper) ──────────────── → note 2
├── Safety + practical limits ──────────────────────────── → note 2
├── macOS screen video (OS-level) ──────────────────────── → note 2
└── Related ────────────────────────────────────────────── → note 2 (→ note 3 images, nd02 media-understanding, note 4 location)
nodes/images.md
├── Goals ──────────────────────────────────────────────── → note 3 (oc_nodes_images)
├── CLI Surface ────────────────────────────────────────── → note 3
├── WhatsApp Web channel behavior ──────────────────────── → note 3
├── Auto-Reply Pipeline ────────────────────────────────── → note 3
├── Inbound Media To Commands ──────────────────────────── → note 3
├── Limits and errors ──────────────────────────────────── → note 3
├── Notes for Tests ────────────────────────────────────── → note 3
└── Related ────────────────────────────────────────────── → note 3 (→ note 2 camera, nd02 media-understanding, note 1 audio)
nodes/location-command.md
├── TL;DR ──────────────────────────────────────────────── → note 4 (oc_nodes_location_command)
├── Why a selector (not just a switch) ─────────────────── → note 4
├── Settings model ─────────────────────────────────────── → note 4
├── Permissions mapping (node.permissions) ─────────────── → note 4
├── Command: location.get (params/response/errors) ─────── → note 4
├── Background behavior ────────────────────────────────── → note 4
├── Model/tooling integration ──────────────────────────── → note 4
├── UX copy (suggested) ────────────────────────────────── → note 4
└── Related ────────────────────────────────────────────── → note 4 (→ ch03 channels/location, note 2 camera, nd02 talk)
```

No orphaned sections. Provider setup pages, `nodes/media-understanding`/`talk`/`voicewake` (nd02),
`channels/location` (ch03), and Gateway `node.invoke` mechanics (gw0x) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 4 pages ≤ 1,094 words (well under the 2,500-word cap), each a single procedure BB; 1 page → 1 note. No mixed-BB or oversize page. |

## Summary Statistics & Building Block Distribution

- Source pages: **4** (2,820 measured words, frontmatter excluded). New `oc_` notes: **4**. New
  `term_dictionary` notes: **0** (expected; see Undigested Terms Plan).
- BB distribution: **procedure ×4** (notes 1–4). Note 4 embeds a small request/response schema as a
  sub-section but the dominant, page-level BB is procedure.
- Est. digest words ~2,250 (avg ~560/note); all ≤ caps (≤400 lines / ≤2,500 words / ≤6 code blocks).
- Source code fences (11 total: audio 6, camera 3, images 0, location 2) distribute 1:1 into the
  corresponding note; each note stays ≤6 (config/CLI/schema snippets reproduced selectively, verbatim).
- Cross-refs (LOCKED at xref-augment 2026-06-21 — see Per-Note Related Notes Mapping): every planned note
  meets the raised floors — **≥8 relevance-selected `term_dictionary` terms · ≥10 code_snippets · ≥10 docs**

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> 2026-06-21). RELEVANCE was the selection criterion: each link was kept only after re-reading the source page
> false-positives from BM25 (`term_floodgates`, `term_stylometry`, `term_idv_verification_methods`,
> `term_content_moderation`, `term_geographic_risk`, `term_coppa`, `bedrock_guardrails_*` for non-PII pages,
> SageMaker/Glue results) were discarded. Sibling `oc_*` notes in this nd01 series and `oc_nodes_media_understanding`
> (nd02) do not exist yet → cited as **(planned, this series)** toward the 10-doc floor; ≥5 of each note's 10
> `../../term_dictionary/`, snippet → `../../code_snippets/`, repo → `../../../areas/code_repos/`, sibling doc →
> `../<folder>/`, sibling oc_ → `oc_Y.md`, entry point → `../../../0_entry_points/`.

### oc_nodes_audio (16t · 12s · 11d)

**Terms** (16)
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — ASR / converting spoken audio into text; relevance: the entire media-understanding flow is STT on the inbound voice note, replacing `Body` with `[Audio]` + `{{Transcript}}`.
- [Real-Time Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming / low-latency speech transcription; relevance: the group mention-detection "preflight" transcribes the first audio attachment before the reply pipeline runs (latency-sensitive gate).
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — chat agent that ingests/acts on voice messages; relevance: this page is exactly the voice-note → agent-reply behavior of a voice bot over a chat channel.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — voice interaction mode for a coding/chat agent; relevance: voice-note transcription is the inbound half of OpenClaw's voice interaction surface.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing audio from text (the reverse modality); relevance: `echoTranscript`/`echoFormat` send a transcript confirmation back to chat, and the page sits beside the talk/voicewake TTS surface (sibling modality contrast).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider integration; relevance: `models.providers.*` audio entries and CLI model entries are the configurable transcription backends.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI APIs; relevance: the auto-detect fallback chain (OpenAI → Groq → xAI → Deepgram → Google → SenseAudio → ElevenLabs → Mistral) is exactly third-party ASR services.
- [Model Failover](../../term_dictionary/term_model_failover.md) — automatic switch to a backup model on failure; relevance: "runs the first eligible model entry in order; if it fails or skips (size/timeout), tries the next entry" is provider/CLI failover.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — designated backup provider in a routing chain; relevance: the ordered provider-fallback list is the fallback-provider pattern for ASR.
- [Failover](../../term_dictionary/term_failover.md) — general resilience pattern of switching to a standby; relevance: the per-entry "fails or skips → next entry" loop is the underlying failover mechanism.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — intermediary forwarding outbound requests; relevance: provider-based transcription honors `HTTPS_PROXY`/`HTTP_PROXY`/`ALL_PROXY` outbound proxy env vars.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity/credentials; relevance: provider auth follows the standard model auth order (auth profiles, env vars, `models.providers.*.apiKey`).
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named stored credential set for a provider; relevance: "auth profiles" are the first tier of the documented provider auth order.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: auto-detect tier 1 is the "active reply model when its provider supports audio understanding" — the agent's LLM doubles as the transcriber.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway mediating agent tool/model calls; relevance: audio understanding is configured under `tools.media.audio.*`, mediated by the OpenClaw gateway tool surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: parent product whose `tools.media.audio` subsystem this page documents.

**Docs** (11)
- [Hermes — STT / Transcription](../hermes_agent/hermes_stt_transcription.md) — Hermes speech-to-text/transcription setup; relevance: direct sibling-ecosystem equivalent of OpenClaw's audio transcription config + provider order.
- [Hermes — Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — CLI for Hermes voice mode; relevance: parallel CLI surface for voice-note handling in the upstream Hermes agent.
- [Hermes — Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — end-user voice-mode guide; relevance: cross-references the same inbound-voice → transcript → reply workflow.
- [Hermes — TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech provider config; relevance: the echo-transcript / talk-mode reverse modality uses the same provider-plugin model.
- [Hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — per-channel media handling settings; relevance: `tools.media.*` caps/enable flags map 1:1 to Hermes media settings.
- [Hermes — Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool reference; relevance: documents the media-attachment tool surface analogous to `tools.media.audio`.
- [Claude Code — Voice Dictation](../claude_code/cc_voice_dictation.md) — voice dictation in Claude Code; relevance: closest coding-agent precedent for inbound-speech → text injection.
- [Bedrock — BDA Media Analysis](../aws_bedrock/bedrock_bda_media_analysis.md) — Bedrock Data Automation audio/video analysis; relevance: managed-service analogue of provider-based media (audio) understanding.
- [`oc_nodes_media_understanding`](oc_nodes_media_understanding.md) **(planned, nd02)** — the shared media-understanding flow; relevance: audio is one modality of the media-understanding pipeline this page invokes.
- [`oc_nodes_images`](oc_nodes_images.md) **(planned, this series)** — image/media send-and-reply; relevance: audio attachments share the inbound-media → templating → `{{Transcript}}` path.
- [`oc_nodes_talk`](oc_nodes_talk.md) **(planned, nd02)** — talk-mode voice interaction; relevance: linked "Related" target; the TTS/echo counterpart to inbound transcription.

**Repos** (3)
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/transcription extension; relevance: implements the provider + local-CLI ASR backends this page configures.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: where inbound voice notes arrive (incl. Telegram group preflight).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: runs the media pipeline that downloads, transcribes, and rewrites `Body`.

**Snippets** (12)
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — send-side media persist + transcript-rewrite pipeline; relevance: implements the exact `Body`→`[Audio]` + `{{Transcript}}` rewrite this page describes.
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — harness transcript handling; relevance: how the agent harness consumes the transcript / `CommandBody` for slash-command parsing.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call media-stream transcription; relevance: same ASR-of-audio mechanics in the streaming voice-call path.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream handling; relevance: audio buffer ingestion + size handling parallels `maxBytes` enforcement.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk-mode transcription relay; relevance: relays transcripts to the agent, the talk-mode sibling of voice-note transcription.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT integration; relevance: implements the `provider: "deepgram"` / `nova-3` config example verbatim.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: end-to-end speech-processing pipeline matching the download→model→transcript flow.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider integration; relevance: the `gpt-4o-mini-transcribe` / `gpt-4o-transcribe` default provider path.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — voice/exec event dedup; relevance: dedups overlapping ASR transcripts on the node event stream (preflight + main phase both transcribe).
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — Hermes transcription tool; relevance: upstream-ecosystem implementation of the same provider/CLI transcription dispatch.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — Hermes voice-mode tool; relevance: parallel voice-note → transcript handling in Hermes.

### oc_nodes_camera (12t · 12s · 11d)

**Terms** (12)
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — extracting meaning from images/video; relevance: camera photos/clips are captured precisely to feed vision/multimodal models.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models over multiple input modalities; relevance: `camera.snap` (jpg) + `camera.clip` (mp4+audio) produce the image/video inputs a multimodal agent consumes.
- [Video Processing](../../term_dictionary/term_video_processing.md) — handling/encoding video; relevance: `camera.clip` captures mp4 with a `durationMs` clamp (≤60s) + base64 payload caps.
- [Vision-Language Model](../../term_dictionary/term_vlm.md) — model jointly over images + text; relevance: the captured photo is the image half passed to a VLM for description/reasoning.
- [Access Control](../../term_dictionary/term_access_control.md) — gating who/what may perform an action; relevance: all camera access is gated behind user-controlled `camera.enabled` + the node-command allowlist.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS-level permission bits/grants; relevance: Android runtime `CAMERA`/`RECORD_AUDIO` grants and macOS TCC Screen-Recording permission are the OS permission layer here.
- [Base64](../../term_dictionary/term_base64.md) — binary-to-text encoding; relevance: `camera.snap`/`camera.clip` return media as `base64`, recompressed to keep payloads <5 MB.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC over JSON; relevance: `node.invoke` carries the `camera.list`/`snap`/`clip` command + response payload as an RPC call.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex node↔server transport; relevance: paired iOS/Android/macOS nodes reach the Gateway over a WebSocket for `node.invoke`.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway mediating agent tool calls; relevance: camera commands are dispatched through the Gateway's `node.invoke` tool surface.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution/file workspace; relevance: the CLI helper writes decoded media to OS-temp files that feed the agent's sandboxed media workflow.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: parent product whose node-camera command surface this page documents.

**Docs** (11)
- [Hermes — Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool reference; relevance: documents node/platform media-capture tool surface analogous to `camera.*`.
- [Hermes — Vision Image Paste](../hermes_agent/hermes_vision_image_paste.md) — pasting images into the agent; relevance: captured photos enter the same image-input path a pasted image does.
- [Hermes — Computer Use (macOS)](../hermes_agent/hermes_computer_use_macos.md) — macOS screen/computer-use capture; relevance: directly parallels OpenClaw's macOS screen-recording (TCC) helper.
- [Hermes — Browser Automation Backends](../hermes_agent/hermes_browser_automation_backends.md) — screenshot/visual capture backends; relevance: another visual-capture-to-vision-model path in the same ecosystem.
- [Hermes — Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image provider plugin; relevance: provider-plugin model for image media, the format `camera.snap` outputs feed.
- [Hermes — Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video provider plugin; relevance: provider-plugin model for video media analogous to `camera.clip` mp4 output.
- [Bedrock — Invoke API: Images](../aws_bedrock/bedrock_invoke_api_images.md) — passing images to a model; relevance: managed-service analogue of submitting a captured photo to a vision model.
- [Bedrock — Invoke API: Multimodal](../aws_bedrock/bedrock_invoke_api_multimodal.md) — multimodal model input; relevance: how image+video capture is consumed by a multimodal model downstream.
- [`oc_nodes_images`](oc_nodes_images.md) **(planned, this series)** — image/media send-and-reply; relevance: the "Related" sibling; captured media flows into the image/media pipeline.
- [`oc_nodes_media_understanding`](oc_nodes_media_understanding.md) **(planned, nd02)** — media-understanding flow; relevance: linked "Related"; captured photos/clips are understood via this flow.
- [`oc_nodes_location_command`](oc_nodes_location_command.md) **(planned, this series)** — `location.get` node command; relevance: linked "Related"; same `node.invoke` + foreground/permission node-command model.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: implements `node.invoke` dispatch + the node-command policy that gates `camera.*` and the foreground-only rule.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — iOS/Android/macOS companion apps; relevance: the paired device nodes that own `camera.enabled` settings, capture, and foreground enforcement.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: paired device-node media capture sibling.

**Snippets** (12)
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke via APNs; relevance: the `node.invoke` wake-and-dispatch path for iOS `camera.*` commands.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node-command allowlist policy; relevance: implements the allowlist/deny gating + foreground-only rule for `camera.*`.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — Android node-command dispatcher; relevance: dispatches `camera.list`/`snap`/`clip` on the Android node with permission checks.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/foreground events; relevance: foreground/background presence drives `NODE_BACKGROUND_UNAVAILABLE`.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session management; relevance: the per-node session a camera command is invoked against.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image limits + resize + path resolution; relevance: the recompress-to-keep-base64-under-5MB payload-guard for captured photos.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image persistence lifecycle; relevance: persists captured-image variants to temp/on-disk like the CLI helper does.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android↔gateway WebSocket session; relevance: the WS transport carrying Android `camera.*` invocations.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — iOS push approval for exec; relevance: the iOS push/permission-prompt mechanism camera/mic access triggers.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI→gateway dispatch; relevance: the `openclaw nodes camera ...` CLI helper dispatches through this path.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision tool image validation; relevance: validates/sniffs the captured image before it reaches a vision model.
- [snippet_brp_agent_tools_screenshot](../../code_snippets/snippet_brp_agent_tools_screenshot.md) — agent screenshot tool; relevance: the screen-capture analogue of `openclaw nodes screen record` / camera capture.

### oc_nodes_images (12t · 12s · 11d)

**Terms** (12)
- [Multimodal](../../term_dictionary/term_multimodal.md) — models over multiple modalities; relevance: this pipeline carries image/audio/video media in one inbound/outbound path for a multimodal agent.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — image understanding; relevance: media understanding inserts an `[Image]` description block (or passes the original image to a native-vision model).
- [Vision-Language Model](../../term_dictionary/term_vlm.md) — joint image+text model; relevance: "if the active primary image model already supports vision natively, OpenClaw skips the `[Image]` summary and passes the original image" — a VLM.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio→text; relevance: audio attachments are transcribed and set `{{Transcript}}` used for command parsing.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video handling/caps; relevance: video passes through up to 16 MB send / 50 MB understanding caps with `[Video]` description blocks.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model provider; relevance: media understanding runs via `tools.media.*` / shared `tools.media.models` provider entries.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: the vision/description/understanding models are third-party GenAI providers.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated workspace; relevance: with a per-session Docker sandbox enabled, inbound media is copied in and `MediaPath`/`MediaUrl` rewritten to `media/inbound/<filename>`.
- [Base64](../../term_dictionary/term_base64.md) — binary-to-text encoding; relevance: media buffers are loaded/encoded and size-bounded before send/understanding.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-platform messaging adapter; relevance: the WhatsApp Baileys-Web channel adapter builds the correct per-type media payload.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway mediating tools; relevance: media understanding + send run through the gateway's `tools.media.*` surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway; relevance: parent product whose media send/reply rules this page documents.

**Docs** (11)
- [Hermes — Messaging WhatsApp Cloud Model](../hermes_agent/hermes_messaging_whatsapp_cloud_model.md) — WhatsApp channel media handling; relevance: directly parallel WhatsApp media send/reply behavior in the upstream ecosystem.
- [Hermes — Messaging WhatsApp Baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — Baileys-Web WhatsApp integration; relevance: same Baileys-Web channel this page's media rules apply to.
- [Hermes — Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool reference; relevance: the media send/attachment tool surface analogous to `message send --media`.
- [Hermes — Vision Image Paste](../hermes_agent/hermes_vision_image_paste.md) — image input to the agent; relevance: inbound images enter the same vision/templating path.
- [Hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — per-channel media settings; relevance: per-type caps (`mediaMaxMb`, audio/video/document) map 1:1 to Hermes media settings.
- [Hermes — Messaging Signal](../hermes_agent/hermes_messaging_signal.md) — Signal channel media; relevance: another channel adapter with media send/reply fan-out for cross-reference.
- [Hermes — Image Generation](../hermes_agent/hermes_image_generation.md) — generating images for replies; relevance: generated media is sent via the same auto-reply media fan-out.
- [Bedrock — KB Multimodal](../aws_bedrock/bedrock_kb_multimodal.md) — multimodal knowledge handling; relevance: managed-service analogue of image/media understanding.
- [`oc_nodes_camera`](oc_nodes_camera.md) **(planned, this series)** — camera capture; relevance: linked "Related"; captured media feeds this send/reply + understanding pipeline.
- [`oc_nodes_media_understanding`](oc_nodes_media_understanding.md) **(planned, nd02)** — media-understanding flow; relevance: linked "Related"; the `[Image]`/`[Audio]`/`[Video]` block insertion this page invokes.
- [`oc_nodes_audio`](oc_nodes_audio.md) **(planned, this series)** — audio/voice notes; relevance: linked "Related"; audio attachments share the `{{Transcript}}` + inbound-media templating path.

**Repos** (3)
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: implements the WhatsApp/Baileys-Web channel media send + auto-reply fan-out.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: downloads inbound media to a temp file, runs understanding, rewrites `MediaPath`/`MediaUrl`.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session management; relevance: the per-session Docker sandbox workspace media is copied into.

**Snippets** (12)
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment validation + MIME sniff + sanitize; relevance: the magic-bytes-then-headers-then-extension MIME detection + size-ceiling routing this page describes.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media persist + transcript rewrite; relevance: inserts `[Image]`/`[Audio]`/`[Video]` blocks and builds `MediaPath` transcript fields.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image limits + resize; relevance: the resize-&-recompress-to-JPEG (max side 2048px) targeting `mediaMaxMb`.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: persisting inbound/outbound media records to temp/disk.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: the send path `openclaw message send --media` resolves through.
- [snippet_hermes_agent_gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp dispatch; relevance: builds the WhatsApp media payload (image/voice-note/document) like the Baileys-Web sender.
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — WhatsApp platform handler; relevance: the WhatsApp channel media send/reply implementation.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — send-with-attachment tool; relevance: the attach-media-to-reply path analogous to auto-reply media fan-out.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — send dispatch; relevance: sequential multi-media reply dispatch ("multiple media entries sent sequentially").
- [snippet_hermes_agent_gw_platform_signal_media](../../code_snippets/snippet_hermes_agent_gw_platform_signal_media.md) — Signal media handling; relevance: per-type media-kind detection + send caps in a sibling channel.
- [snippet_hermes_agent_gw_platform_telegram_media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media handling; relevance: inbound-media → temp file → templating in a sibling channel.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision input validation; relevance: validates inbound images for the native-vision pass-through path.

### oc_nodes_location_command (12t · 10s · 10d)

**Terms** (12)
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: precise GPS coordinates (`lat`/`lon`/`isPrecise`) are sensitive personal data, the core privacy concern of this command.
- [Privacy by Design](../../term_dictionary/term_privacy_by_design.md) — building privacy into defaults; relevance: `location.get` is off-by-default, uses a selector (not just a switch), a separate Precise toggle, and a scope-aware agent guideline.
- [Access Control](../../term_dictionary/term_access_control.md) — gating actions; relevance: `location.enabledMode` (`off`/`whileUsing`) + the `node.permissions` map gate whether the command runs at all.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS permission grants; relevance: iOS/macOS While-Using/Always + Android fine/coarse OS grants override the in-app selector.
- [Geofence](../../term_dictionary/term_geofence.md) — geographic boundary on location data; relevance: the lat/lon/accuracy fix is the location datum geofencing operates on (geo-data context).
- [Geohash](../../term_dictionary/term_geohash.md) — encoding lat/lon into a string; relevance: the `lat`/`lon`/`accuracyMeters` response is the coordinate datum a geohash encodes.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — collect only what's needed; relevance: the `desiredAccuracy: coarse|balanced|precise` + Precise toggle let callers request approximate-only location.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON request/response RPC; relevance: `location.get` is invoked via `node.invoke` with a JSON params/response/error-code schema.
- [WebSocket](../../term_dictionary/term_websocket.md) — node↔gateway transport; relevance: the node command travels over the WebSocket node session.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway mediating tools; relevance: the `nodes` tool exposes a `location_get` action through the gateway tool surface.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — the agent's core model; relevance: the model/tooling integration lets the agent call `location_get` only within enabled scope (agent-guideline gating).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway; relevance: parent product whose node `location.get` command + permission model this page documents.

**Docs** (10)
- [Hermes — Tools Reference: Core](../hermes_agent/hermes_tools_reference_core.md) — core agent tool reference; relevance: the `nodes` tool `location_get` action sits in the core tool surface.
- [Hermes — Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform/node tool reference; relevance: documents the node-command tool family `location_get` belongs to.
- [Hermes — Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — command approval/permission gating; relevance: parallels the off-by-default + permission-required gating of `location.get`.
- [Hermes — Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: the `node.invoke` + `node.permissions` mechanics location commands ride on.
- [Claude Code — Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — permission relay across channels; relevance: the OS-grant-vs-app-selector relay model parallels CC's permission relay.
- [Claude Code — Security Architecture](../claude_code/cc_security_architecture.md) — agent security model; relevance: scope-gating a sensitive capability (location) behind explicit user enablement.
- [Bedrock — Guardrails: Sensitive Info](../aws_bedrock/bedrock_guardrails_sensitive_info.md) — sensitive-data (PII) controls; relevance: managed-service analogue for handling sensitive location PII.
- [`oc_nodes_camera`](oc_nodes_camera.md) **(planned, this series)** — camera capture; relevance: linked "Related"; same `node.invoke` + foreground/permission/error-code node-command model.
- [`oc_nodes_talk`](oc_nodes_talk.md) **(planned, nd02)** — talk mode; relevance: linked "Related" target; sibling node-command surface.
- [`oc_channels_location`](oc_channels_location.md) **(planned, ch03)** — channel location parsing; relevance: linked "Related"; the inbound-channel counterpart to the node `location.get` command.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: implements `node.invoke` + the `node.permissions` map that gates `location.get`.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — iOS/Android/macOS apps; relevance: own the location selector settings + Android foreground-only behavior.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: permission/scope enforcement for the sensitive location capability.

**Snippets** (10)
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node-command allowlist policy; relevance: the allowlist/declaration/deny gating that authorizes `location.get`.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke via APNs; relevance: the `node.invoke` dispatch path for `location.get`.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — Android node-command dispatcher; relevance: dispatches `location.get` and enforces the Android foreground/background denial.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/foreground events; relevance: foreground/background presence drives `LOCATION_BACKGROUND_UNAVAILABLE`.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android↔gateway WebSocket session; relevance: the WS node session carrying the location command.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session management; relevance: the per-node session `location.get` is invoked against.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny policy; relevance: deny-by-default gating model for sensitive capabilities like location.
- [snippet_hermes_agent_gw_slash_access](../../code_snippets/snippet_hermes_agent_gw_slash_access.md) — access/scope gating; relevance: scope/permission gating of an agent capability, parallel to the location agent-guideline.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI→gateway dispatch; relevance: the `openclaw nodes location get --node <id>` CLI helper dispatches through this path.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: the user-must-enable + scope-understood approval gate the agent guideline mandates.

> **Excluded as relevance/ghost false-positives (DB-checked):** `term_image_generation`, `term_whatsapp`,
> `term_telegram`, `term_transcription`, `term_geolocation`, `term_gps` do NOT exist in the DB — excluded
> (no ghost references). Relevance-discarded existing notes (real but off-topic for these media/sensor pages):
> `term_content_moderation`, `term_geographic_risk`, `term_coppa`, `term_age_verification`, `term_pii` was
> KEPT only for the location note; abuse-detection terms (`term_floodgates`, `term_stylometry`), and
> SageMaker/Glue/Neptune docs were discarded as BM25 domain false-positives.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary terms are documented as `oc_*` doc concept notes by their home sub-plan;
> the only `term_dictionary` interaction is **linking existing** terms. Expected **0 new** `term_dictionary`
> captures. No term definition is ever inlined in an `oc_*` note.

| Term (vocab encountered) | Disposition |
|---|---|
| media understanding (audio/image/video) | OpenClaw doc concept; documented in `oc_nodes_audio`/`oc_nodes_images` + nd02 `oc_nodes_media_understanding`; NOT a new term note. |
| auto-detection / provider fallback order | Documented in `oc_nodes_audio` (procedure); NOT a term. |
| `node.invoke` / node command | OpenClaw Gateway primitive; documented across nd01 notes + gateway sub-plans; link `term_json_rpc`. |
| `camera.list` / `camera.snap` / `camera.clip` | OpenClaw command names; documented in `oc_nodes_camera`; NOT terms. |
| `location.get` / `enabledMode` / precise location | OpenClaw command + settings; documented in `oc_nodes_location_command`; NOT terms. |
| transcription / ASR / Whisper / Voxtral / nova-3 | Link existing `term_speech_to_text`, `term_realtime_transcription`; provider/model names are config, not promoted to term notes (link `term_third_party_genai_services`/`term_llm`). |
| transcription (general STT concept) | Link existing `term_speech_to_text` (do NOT create `term_transcription` — would duplicate). |
| MediaPath / MediaUrl / Transcript templating | OpenClaw template variables; documented in `oc_nodes_images`/`oc_nodes_audio`; NOT terms. |
| scope gating / `requireMention` preflight | OpenClaw config behavior; documented in `oc_nodes_audio`; link `term_access_control`. |
| WhatsApp / Baileys-web / Telegram / Deepgram / Groq / Mistral / SenseAudio | Channel/provider names = config, documented as config; link `term_third_party_genai_services` (no `term_whatsapp`/`term_telegram` exist; do NOT create — provider/channel names are not promoted). |
| geolocation / GPS / precise location | Link existing `term_geofence`/`term_geohash`/`term_pii`/`term_privacy_by_design`; do NOT create `term_geolocation`/`term_gps` (generic, low reuse; geo terms already cover the concept). |
| camera / photo / video capture | Link existing `term_computer_vision`/`term_multimodal`/`term_video_processing`; do NOT create `term_camera`. |

**New-term candidates:** **none.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home
and an existing note was found; the agentic/LLM/security/geo glossaries already cover the relevant concepts.
(Collision/dedup audit: `term_transcription`, `term_geolocation`, `term_gps`, `term_whatsapp`, `term_telegram`,
`term_image_generation` were each considered and rejected — either generic/low-reuse or duplicative of an
existing substantive note; `term_speech_to_text` + `term_realtime_transcription` + geo terms suffice.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master). If augment
Step 2d surfaces a genuinely reusable cross-cutting term with no doc-page home AND no existing note, it would be
`acronym_glossary_*.md` (candidate glossary for any media/voice term: `acronym_glossary_llm` or
`acronym_glossary_tools`) per master W5 — but none is expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (4 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` (YAML field order/forbidden fields; `## Overview` + `## Related Notes` present; `**Source**`/`**Last Updated**`/`**Status**` footer). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/nodes/<page>.md` (no hallucinated commands/params/error codes; config snippets verbatim). |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks; every mapped H2/H3 represented (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + other vault notes, each an indexed link with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links`; 0 broken links after incremental reindex. |
| G7 | Discoverability (inbound) | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island). |
| G8 | In-degree ≥1 | Verified via `note_links` after reindex (satisfied via `entry_openclaw_docs.md` + repo/term inlinks). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
NOTES="oc_nodes_audio oc_nodes_camera oc_nodes_images oc_nodes_location_command"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  grep -qE "$REQ_SECTIONS" "$f" || echo "MISSING REQUIRED SECTION: $n"
  # source_url present (REQUIRE_SOURCE_URL)
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps (G3): words exclude frontmatter; code blocks = fences/2
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # G4: at least one sibling oc_ cross-link
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING ${SIBLING_PREFIX} LINK: $n"
done

# YAML frontmatter sweep for the whole subfolder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (source) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_nodes_audio | procedure | 700 | 6 | ✅ (≤2,500w / ≤6 code) |
| 2 | oc_nodes_camera | procedure | 600 | 3 | ✅ |
| 3 | oc_nodes_images | procedure | 500 | 0 | ✅ |
| 4 | oc_nodes_location_command | procedure | 450 | 2 | ✅ |

No note approaches caps. The largest source page (audio, 1,094 w, 6 fences) compresses comfortably into one
≤700-word note keeping ≤6 selectively-reproduced config snippets; no split needed.

## Entry Point Decision (inherited from master)

Contributes **4 rows** to `entry_openclaw_docs.md` (CREATED as a master W1 pre-step before the first sub-plan
executes) under a **"Nodes"** section cluster (shared with nd02). Each note gets its entry-point back-link at
finalization; this satisfies G7/G8 (≥1 outside-folder inbound link). No separate entry point is created by this
sub-plan (size threshold handled at the master/series level).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution):

- `entry_openclaw_docs.md` **(planned, master pre-step)** → all 4 notes (primary anti-island guarantee).
- `repo_openclaw_extensions_voice_speech` → `oc_nodes_audio` (the ASR extension this note documents).
- `repo_openclaw_channels_messaging` → `oc_nodes_audio`, `oc_nodes_images` (inbound media channel).
- `repo_openclaw_gateway` → `oc_nodes_camera`, `oc_nodes_location_command`, `oc_nodes_images` (`node.invoke` + media pipeline).
- `repo_openclaw_apps` → `oc_nodes_camera`, `oc_nodes_location_command` (iOS/Android/macOS node settings).
- `term_speech_to_text` → `oc_nodes_audio`; `term_computer_vision` / `term_multimodal` → `oc_nodes_camera`, `oc_nodes_images`;
  `term_geofence` / `term_pii` → `oc_nodes_location_command`.
- Sibling reciprocal: nd02 `oc_nodes_media_understanding` **(planned)** → all 4 (shared "Related" cluster).

## Pacing Rules (inherited from master)

Single phase; all 8 gates pass before commit. Re-read each source page during execution; reproduce config/CLI/
schema snippets verbatim. One BB per note. `git pull --rebase --autostash` before commit; no Claude co-author
trailer; reindex incrementally and verify `note_links` + 0 broken links before commit; commit+push after the
phase (snippet/DB-update/commit/push is one indivisible cycle).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this augment:** xref-augment of all 4 planned notes — re-read the 4 source pages
(`inbox/openclaw_docs/nodes/{audio,camera,images,location-command}.md`), built a relevance-selected,
note), replaced the PLAN-stage Candidate Cross-References section, and locked counts.


| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met (≥8t·≥10s·≥10d) |
|---|---:|---:|---|---:|---|
| oc_nodes_audio | 16 | 12 | 11 (8 existing / 3 planned) | 3 | ✅ |
| oc_nodes_camera | 12 | 12 | 11 (8 existing / 3 planned) | 3 | ✅ |
| oc_nodes_images | 12 | 12 | 11 (8 existing / 3 planned) | 3 | ✅ |
| oc_nodes_location_command | 12 | 10 | 10 (7 existing / 3 planned) | 3 | ✅ |

- **Terms**: all from `term_dictionary/`, relevance-selected by re-reading each page. Audio is term-rich
  audio 8, camera 8, images 8, location 7 existing).
  node-command/vision snippets selected by component match to the page (e.g.
  `snippet_openclaw_gateway_chat_transcript_media_pipeline` implements the `Body`→`[Audio]`+`{{Transcript}}`
  rewrite; `snippet_openclaw_gateway_node_command_policy` implements the `camera.*`/`location.get` allowlist).
- **Docs**: ≥5 EXISTING per note from the `hermes_agent/`, `claude_code/`, `aws_bedrock/` corpora; the
  remaining 3 are planned sibling `oc_*` docs (this nd01 series + nd02 media-understanding/talk + ch03
  channels/location), cited `(planned)` toward the 10-doc floor per the master series design.
- **Repos**: relevant `repo_openclaw*` (gateway/apps/extensions_voice_speech/channels_messaging/
  channels_voice_phone/sessions/security) per note.

**New-term candidates:** **NONE.** The re-read (Step 2d) surfaced no genuinely cross-cutting, vault-reusable
term lacking BOTH a doc-page home AND an existing note. All media/voice/sensor concepts are already covered by
existing terms (`term_speech_to_text`, `term_realtime_transcription`, `term_voice_mode`, `term_multimodal`,
`term_computer_vision`, `term_vlm`, `term_video_processing`, geo terms `term_geofence`/`term_geohash`/`term_pii`/
`term_privacy_by_design`, RPC/transport `term_json_rpc`/`term_websocket`). Slugs considered + REJECTED in the
collision/specificity audit: `term_transcription` (dup of `term_speech_to_text`), `term_geolocation`/`term_gps`
(generic; geo terms cover it), `term_whatsapp`/`term_telegram` (channel/provider names, not promoted),
`term_image_generation` (not in DB; not needed by these pages), `term_camera`/`term_node_command` (OpenClaw
command names, documented as `oc_*` doc concepts, not term notes). Best-fit glossary IF any future media/voice
term were captured (none expected): `acronym_glossary_llm` or `acronym_glossary_tools` (per master W5).

**Plan-digestion quality flag:** none (<3 new terms surfaced; the original Step 4e was complete for these pages).

note_name='<id>'`); 108 distinct link targets extracted from the mapping — every non-`(planned)` target
resolve from `resources/documentation/openclaw/`; source word/code/heading counts re-measured (audio
1,067w/6c, camera 760w/3c, images 537w/0c, location 337w/2c) and within ±10% of the plan's Source table.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_nd01.md
Date: 2026-06-21
```

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, per-link relevance) | **PASS** | Per-Note Related Notes Mapping present; every note ≥8 terms (16/12/12/12), ≥10 snippets (12/12/12/10), ≥10 docs (11/11/11/10), each link rendered `- [Name](relpath.md) — what; relevance: why`. ≥1 entry-point back-link (`entry_openclaw_docs`, planned W1) per Inlinks/Entry-Point sections. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | Single-phase 8-row gate table (`grep -cE '^\| G[1-8] '` = 8) covering G1 Format / G2 Grounding / G3 Density+Coverage / G4 Cross-Ref / G5 Ghost / G6 Broken-link / G7 Discoverability / G8 In-degree; G5/G6/G1 consolidated via `/tessellum-validate-note-gates` in Validation Scripts. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | Entry Point Decision section: contributes 4 rows to `entry_openclaw_docs.md` under a "Nodes" cluster (created as master W1 pre-step); per-note back-link satisfies G7/G8. No separate per-sub-plan entry point (handled at series level — correct for a 4-note sub-plan of a >30-note series). |
| CP4 | Plan size (≤30 or split) | **PASS** | 4 planned notes (well under 30); no split needed (all source pages ≤1,067w, single procedure BB each). |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master, derived from existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) doc corpora: `## Overview` opener, `## Related Notes` reference section, `**Source**`/`**Last Updated**`/`**Status**` footer, fixed YAML field order, `language: markdown`, `access_control_group: ["general"]`, forbidden-field list — matches existing target-type notes. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: largest note (audio) ~700w/≤6 code, no note approaches the ≤400-line / ≤2,500-word / ≤6-code caps; no borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21: audio 1,067w (plan 1,094), camera 760w (801), images 537w (554), location 337w (371) — all within ±10% (≪ the 1.5× fail threshold); code fences exact (6/3/0/2). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | Both sections present; 0 new terms (expected per master corpus-ownership design — OpenClaw vocab = `oc_*` doc concepts, link existing terms only); Term-Note Authoring Requirements section present as N/A-with-fallback (multi-source mandate inherited from master W5 if any term ever surfaces). |
| CP8f | Slug specificity + all-notes (term AND doc) collision/dedup audit | **PASS** | Collision/dedup audit recorded in Undigested Terms Plan + Augmentation Report: `term_transcription`/`term_geolocation`/`term_gps`/`term_whatsapp`/`term_telegram`/`term_image_generation`/`term_camera`/`term_node_command` each considered + rejected (generic, channel-name, or duplicative). Planned `oc_*` doc notes checked vs existing term notes (no doc duplicates a substantive term note — `term_speech_to_text` etc. are LINKED, not recreated). |
| CP9 | Discoverability / inlinks executed (G8, no islands) | **PASS** | Inlinks section maps every new note to ≥1 outside-`documentation/openclaw/` inbound link (`entry_openclaw_docs` W1 + `repo_openclaw*` + relevant `term_*`); G7/G8 in the gate table mark inlink-addition as a gated execution step (DB in-degree ≥1 verified at execution). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
