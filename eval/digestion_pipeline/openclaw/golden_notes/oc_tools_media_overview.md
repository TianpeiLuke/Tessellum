---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - media
keywords:
  - openclaw media overview
  - tool-driven media capabilities
  - provider capability matrix
  - async vs synchronous media
  - speech-to-text voice call
  - text-to-speech tts tool
  - media understanding
  - talk session contract
topics:
  - OpenClaw
  - Media Capabilities
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/media-overview
access_control_group: ["general"]
---

# OpenClaw — Media Capabilities Overview

## Overview

This note is the conceptual index of OpenClaw's media surface: it generates images, videos, and music, understands inbound media (images, audio, video), and speaks replies aloud with text-to-speech. The unifying idea, mirrored from the `tools/media-overview` source page, is that all media capabilities are **tool-driven** — the agent decides when to use them based on the conversation — and **provider-gated**: each tool only appears when at least one backing provider is configured. This note covers the six capability cards (image / video / music generation, TTS, media understanding, STT), the provider capability matrix, the async-vs-synchronous execution model, the batch STT plus Voice Call streaming distinction, and how the **Talk session contract** for live speech differs from the one-shot media tool path. Per-tool detail (image, video, music, TTS, audio, media-understanding) lives on sibling pages linked below rather than restated here.

## Tool-Driven, Provider-Gated Media

All media capabilities are tool-driven: the agent decides when to use them based on the conversation, and each tool only appears when at least one backing provider is configured. A separate axis is live speech, which uses the **Talk session contract** instead of the one-shot media tool path. Talk has three modes: provider-native `realtime`, local or streaming `stt-tts`, and `transcription` for observe-only speech capture. Those three modes share provider catalogs, event envelopes, and cancellation semantics with telephony, meetings, browser realtime, and native push-to-talk clients.

## Capabilities

The source page presents six capability cards, each mapping a media surface to its agent tool and detail page:

- **Image generation** (`/tools/image-generation`) — Create and edit images from text prompts or reference images via `image_generate`. Async in chat sessions: runs in the background and posts the result when ready.
- **Video generation** (`/tools/video-generation`) — Text-to-video, image-to-video, and video-to-video via `video_generate`. Async: runs in the background and posts the result when ready.
- **Music generation** (`/tools/music-generation`) — Generate music or audio tracks via `music_generate`. Async in chat sessions on the shared media-generation task lifecycle.
- **Text-to-speech** (`/tools/tts`) — Convert outbound replies to spoken audio via the `tts` tool plus `messages.tts` config. Synchronous.
- **Media understanding** (`/nodes/media-understanding`) — Summarize inbound images, audio, and video using vision-capable model providers and dedicated media-understanding plugins.
- **Speech-to-text** (`/nodes/audio`) — Transcribe inbound voice messages through batch STT or Voice Call streaming STT providers.

## Provider Capability Matrix

The source enumerates which providers back each media surface. Reproduced verbatim from the mirror (`✓` = supported):

| Provider          | Image | Video | Music | TTS | STT | Realtime voice | Media understanding |
| ----------------- | :---: | :---: | :---: | :-: | :-: | :------------: | :-----------------: |
| Alibaba           |       |   ✓   |       |     |     |                |                     |
| BytePlus          |       |   ✓   |       |     |     |                |                     |
| ComfyUI           |   ✓   |   ✓   |   ✓   |     |     |                |                     |
| DeepInfra         |   ✓   |   ✓   |       |  ✓  |  ✓  |                |          ✓          |
| Deepgram          |       |       |       |     |  ✓  |       ✓        |                     |
| ElevenLabs        |       |       |       |  ✓  |  ✓  |                |                     |
| fal               |   ✓   |   ✓   |   ✓   |     |     |                |                     |
| Google            |   ✓   |   ✓   |   ✓   |  ✓  |     |       ✓        |          ✓          |
| Gradium           |       |       |       |  ✓  |     |                |                     |
| Local CLI         |       |       |       |  ✓  |     |                |                     |
| Microsoft         |       |       |       |  ✓  |     |                |                     |
| Microsoft Foundry |   ✓   |       |       |     |     |                |                     |
| MiniMax           |   ✓   |   ✓   |   ✓   |  ✓  |     |                |                     |
| Mistral           |       |       |       |     |  ✓  |                |                     |
| OpenAI            |   ✓   |   ✓   |       |  ✓  |  ✓  |       ✓        |          ✓          |
| OpenRouter        |   ✓   |   ✓   |   ✓   |  ✓  |  ✓  |                |          ✓          |
| Qwen              |       |   ✓   |       |     |     |                |                     |
| Runway            |       |   ✓   |       |     |     |                |                     |
| SenseAudio        |       |       |       |     |  ✓  |                |                     |
| Together          |       |   ✓   |       |     |     |                |                     |
| Vydra             |   ✓   |   ✓   |       |  ✓  |     |                |                     |
| xAI               |   ✓   |   ✓   |       |  ✓  |  ✓  |                |          ✓          |
| Xiaomi MiMo       |   ✓   |       |       |  ✓  |     |                |          ✓          |

The source adds an important caveat about the media-understanding column: media understanding uses any vision-capable or audio-capable model registered in your provider config. The matrix above lists providers with **dedicated** media-understanding support; most multimodal LLM providers (Anthropic, Google, OpenAI, etc.) can also understand inbound media when configured as the active reply model.

## Async vs Synchronous

The source classifies each capability's execution mode and the reason for it:

| Capability     | Mode         | Why                                                                                                  |
| -------------- | ------------ | ---------------------------------------------------------------------------------------------------- |
| Image          | Asynchronous | Provider processing can outlive a chat turn; generated attachments use the shared completion path.   |
| Text-to-speech | Synchronous  | Provider responses return in seconds; attached to the reply audio.                                   |
| Video          | Asynchronous | Provider processing takes 30 s to several minutes; slow queues can run up to the configured timeout. |
| Music          | Asynchronous | Same provider-processing characteristic as video.                                                    |

For async tools, OpenClaw submits the request to the provider, returns a task id immediately, and tracks the job in the **task ledger**. The agent continues responding to other messages while the job runs. When the provider finishes, OpenClaw wakes the agent with the generated media paths so it can tell the user through the session's normal visible-reply mode: automatic final reply delivery when configured, or `message(action="send")` when the session requires the message tool. If the requester session is inactive or its active wake fails, and some generated media is still missing from the completion reply, OpenClaw sends an idempotent direct fallback with only the missing media; media already delivered by the completion reply is not posted again.

## Speech-to-Text and Voice Call

The source distinguishes two STT surfaces. Deepgram, DeepInfra, ElevenLabs, Mistral, OpenAI, OpenRouter, SenseAudio, and xAI can all transcribe inbound audio through the **batch** `tools.media.audio` path when configured. Channel plugins that preflight a voice note for mention gating or command parsing mark the transcribed attachment on the inbound context, so the shared media-understanding pass reuses that transcript instead of making a second STT call for the same audio.

Separately, Deepgram, ElevenLabs, Mistral, OpenAI, and xAI also register **Voice Call streaming STT** providers, so live phone audio can be forwarded to the selected vendor without waiting for a completed recording.

For live user conversations, the source recommends preferring Talk mode (`/nodes/talk`). Batch audio attachments stay on the media path; browser realtime, native push-to-talk, telephony, and meeting audio should use Talk events and the session-scoped catalogs returned by the Gateway.

## Provider Mappings

The source closes with a "how vendors split across surfaces" accordion, detailing which surfaces four notable providers register:

- **Google** — Image, video, music, batch TTS, backend realtime voice, and media-understanding surfaces.
- **OpenAI** — Image, video, batch TTS, batch STT, Voice Call streaming STT, backend realtime voice, and memory-embedding surfaces.
- **DeepInfra** — Chat/model routing, image generation/editing, text-to-video, batch TTS, batch STT, image media understanding, and memory-embedding surfaces. DeepInfra-native rerank/classification/object-detection models are not registered until OpenClaw has dedicated provider contracts for those categories.
- **xAI** — Image, video, search, code-execution, batch TTS, batch STT, and Voice Call streaming STT. xAI Realtime voice is an upstream capability but is not registered in OpenClaw until the shared realtime-voice contract can represent it.

**Source**: OpenClaw documentation — `tools/media-overview` (mirror `inbox/openclaw_docs/tools/media-overview.md`)
**Last Updated**: 2026-06-22
**Status**: Active
