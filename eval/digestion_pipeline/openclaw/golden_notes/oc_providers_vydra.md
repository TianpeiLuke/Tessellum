---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - media_generation
keywords:
  - openclaw vydra provider
  - vydra api key
  - vydra grok-imagine image generation
  - vydra veo3 kling video generation
  - vydra elevenlabs speech tts
  - vydra www base url authorization redirect
  - vydra-api-key onboarding
  - image video speech provider plugin
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/vydra
access_control_group: ["general"]
---

# OpenClaw — Vydra Media Provider (Image / Video / Speech)

## Overview

This note is the setup procedure for enabling the bundled **Vydra** media-generation plugin in OpenClaw, mirroring the `providers/vydra` source page. Vydra is a single bundled provider plugin (provider id `vydra`, `enabledByDefault: true`) that registers three media contracts — `imageGenerationProviders`, `videoGenerationProviders`, and `speechProviders` — all powered by one `VYDRA_API_KEY`. The procedure covers the header property table and the `www`-host base-URL caveat, the `## Setup` onboarding/env-var steps, and the `## Capabilities` accordions for image generation, video generation, provider-specific live tests, and ElevenLabs-backed speech synthesis. Shared media-tool semantics (parameters, provider selection, failover) live on the `tools/image-generation` and `tools/video-generation` pages and are linked, not duplicated here.

## Provider Properties

The bundled Vydra plugin adds image generation via `vydra/grok-imagine`, video generation via `vydra/veo3` and `vydra/kling`, and speech synthesis via Vydra's ElevenLabs-backed TTS route. OpenClaw uses the same `VYDRA_API_KEY` for all three capabilities. The provider's key properties from the source header table are:

| Property | Value |
| --- | --- |
| Provider id | `vydra` |
| Plugin | bundled, `enabledByDefault: true` |
| Auth env var | `VYDRA_API_KEY` |
| Onboarding flag | `--auth-choice vydra-api-key` |
| Direct CLI flag | `--vydra-api-key <key>` |
| Contracts | `imageGenerationProviders`, `videoGenerationProviders`, `speechProviders` |
| Base URL | `https://www.vydra.ai/api/v1` (use the `www` host) |

### Base-URL `www`-host Caveat (Warning)

Use `https://www.vydra.ai/api/v1` as the base URL. Vydra's apex host (`https://vydra.ai/api/v1`) currently redirects to `www`. Some HTTP clients drop `Authorization` on that cross-host redirect, which turns a valid API key into a misleading auth failure. The bundled plugin uses the `www` base URL directly to avoid that.

## Setup

The setup is a two-step procedure: authenticate, then choose which capability (or capabilities) to make default.

**Step 1 — Run interactive onboarding.** Either run interactive onboarding with the Vydra auth choice, or set the env var directly:

```bash
openclaw onboard --auth-choice vydra-api-key
```

Or set the env var directly:

```bash
export VYDRA_API_KEY="vydra_live_..."
```

**Step 2 — Choose a default capability.** Pick one or more of the capabilities below (image, video, or speech) and apply the matching configuration. The direct CLI flag `--vydra-api-key <key>` is the non-onboarding alternative to the env var for supplying the key.

## Capabilities

The three Vydra capabilities are configured independently. Each is selected by setting the matching agent-default or messages-TTS provider; all three share the single `VYDRA_API_KEY`.

### Image Generation

Default image model: `vydra/grok-imagine`. Set it as the default image provider:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "vydra/grok-imagine",
      },
    },
  },
}
```

Current bundled support is text-to-image only. Vydra's hosted edit routes expect remote image URLs, and OpenClaw does not add a Vydra-specific upload bridge in the bundled plugin yet. See the shared image-generation tool docs (linked under References) for shared tool parameters, provider selection, and failover behavior.

### Video Generation

Registered video models: `vydra/veo3` for text-to-video and `vydra/kling` for image-to-video. Set Vydra as the default video provider:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "vydra/veo3",
      },
    },
  },
}
```

The source records these video notes: `vydra/veo3` is bundled as text-to-video only; `vydra/kling` currently requires a remote image URL reference, and local file uploads are rejected up front; Vydra's current `kling` HTTP route has been inconsistent about whether it requires `image_url` or `video_url`, so the bundled provider maps the same remote image URL into both fields; and the bundled plugin stays conservative and does not forward undocumented style knobs such as aspect ratio, resolution, watermark, or generated audio. See the shared video-generation tool docs (linked under References) for shared tool parameters, provider selection, and failover behavior.

### Video Live Tests

Provider-specific live coverage is gated behind live-test env flags:

```bash
OPENCLAW_LIVE_TEST=1 \
OPENCLAW_LIVE_VYDRA_VIDEO=1 \
pnpm test:live -- extensions/vydra/vydra.live.test.ts
```

The bundled Vydra live file now covers `vydra/veo3` text-to-video and `vydra/kling` image-to-video using a remote image URL. Override the remote image fixture when needed by exporting `OPENCLAW_LIVE_VYDRA_KLING_IMAGE_URL="https://example.com/reference.png"`.

### Speech Synthesis

Set Vydra as the speech provider via the `messages.tts` block:

```json5
{
  messages: {
    tts: {
      provider: "vydra",
      providers: {
        vydra: {
          apiKey: "${VYDRA_API_KEY}",
          speakerVoiceId: "21m00Tcm4TlvDq8ikWAM",
        },
      },
    },
  },
}
```

Defaults are model `elevenlabs/tts` and voice id `21m00Tcm4TlvDq8ikWAM`. The bundled plugin currently exposes one known-good default voice and returns MP3 audio files.

**Source**: OpenClaw documentation — `providers/vydra` (mirror `inbox/openclaw_docs/providers/vydra.md`)
**Last Updated**: 2026-06-22
**Status**: Active
