---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - media_generation
keywords:
  - openclaw fal provider
  - fal image generation
  - fal video generation
  - fal music generation
  - fal_key auth
  - flux krea seedance heygen
  - imagegenerationmodel videogenerationmodel musicgenerationmodel
  - music_generate image_generate video_generate
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/fal
access_control_group: ["general"]
---

# OpenClaw — Configure the Bundled fal Generation Provider

## Overview

This note is the procedure for configuring OpenClaw's bundled `fal` provider, which delivers hosted image, video, and music generation. It mirrors the `providers/fal` source page: the `FAL_KEY` authentication flow, setting a default image model, the image-generation capability matrix (Flux/Krea 2/GPT Image 2/Nano Banana 2 with edit and aspect-ratio rules), the queue-backed video models (Seedance 2.0 and HeyGen), and the music-generation defaults for the shared `music_generate` tool. fal is a *generation* provider (not a chat LLM provider); its models are selected through the `agents.defaults.imageGenerationModel` / `videoGenerationModel` / `musicGenerationModel` config, and invoked through the shared `image_generate` / `video_generate` / `music_generate` agent tools.

The provider identity is fixed: provider id `fal`, auth via `FAL_KEY` (canonical; `FAL_API_KEY` also works as a fallback), and the API is fal's model endpoints.

## Getting started

Two steps onboard fal. First set the API key, then select a default image model.

1. Set the API key with the onboarding flow:

```bash
openclaw onboard --auth-choice fal-api-key
```

2. Set a default image model in your agent config:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "fal/fal-ai/flux/dev",
      },
    },
  },
}
```

Authentication resolves from `FAL_KEY` (canonical), with `FAL_API_KEY` accepted as a fallback. To enumerate every available fal model — including any recently added entries — run `openclaw models list --provider fal`.

## Image generation

The bundled `fal` image-generation provider defaults to `fal/fal-ai/flux/dev`. Its capability matrix:

| Capability | Value |
| --- | --- |
| Max images | 4 per request; Krea 2: 1 per request |
| Edit mode | Flux: 1 reference image; GPT Image 2: 10; Nano Banana 2: 14 |
| Style refs | Krea 2: up to 10 style references via `image` / `images` |
| Size overrides | Supported |
| Aspect ratio | Supported for generate, Krea 2, and GPT Image 2/Nano Banana 2 edit |
| Resolution | Supported |
| Output format | `png` or `jpeg` |

Aspect-ratio rules differ by model. Flux image-to-image requests do **not** support `aspectRatio` overrides. GPT Image 2 and Nano Banana 2 edit requests use fal's `/edit` endpoint and accept aspect-ratio hints. Nano Banana 2 also accepts extra-native wide/tall ratios such as `4:1`, `1:4`, `8:1`, and `1:8`; Krea 2 validates its own smaller aspect-ratio subset.

Krea 2 models use fal's native Krea payload schema. OpenClaw sends `aspect_ratio`, `creativity`, and `image_style_references` instead of the generic `image_size` / edit-endpoint payload used by Flux. The Krea 2 model refs are `fal/krea/v2/medium/text-to-image` and `fal/krea/v2/large/text-to-image`. Use Medium for faster expressive illustration, anime, painting, and artistic styles; use Large for slower photoreal, raw texture, film grain, and detailed looks. Krea defaults to `fal.creativity: "medium"`; supported values are `raw`, `low`, `medium`, and `high`. Because Krea 2 exposes aspect ratio (not `image_size`) in fal's request schema, prefer `aspectRatio`; OpenClaw maps `size` to the closest supported Krea aspect ratio and rejects `resolution` for Krea rather than dropping it.

Output-format handling has fal-specific limits. Use `outputFormat: "png"` when you want PNG output from fal models that expose `output_format`. fal does not declare an explicit transparent-background control in OpenClaw, so `background: "transparent"` is reported as an ignored override for fal models. Krea 2 endpoints do not expose an `output_format` request field through fal, so OpenClaw rejects `outputFormat` overrides for Krea requests.

To use Krea 2 Medium as the default image provider:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "fal/krea/v2/medium/text-to-image",
      },
    },
  },
}
```

## Video generation

The bundled `fal` video-generation provider defaults to `fal/fal-ai/minimax/video-01-live`.

| Capability | Value |
| --- | --- |
| Modes | Text-to-video, single-image reference, Seedance reference-to-video |
| Runtime | Queue-backed submit/status/result flow for long-running jobs |

The available video models are the HeyGen video-agent (`fal/fal-ai/heygen/v2/video-agent`) and the Seedance 2.0 family: `fal/bytedance/seedance-2.0/fast/text-to-video`, `fal/bytedance/seedance-2.0/fast/image-to-video`, `fal/bytedance/seedance-2.0/fast/reference-to-video`, `fal/bytedance/seedance-2.0/text-to-video`, `fal/bytedance/seedance-2.0/image-to-video`, and `fal/bytedance/seedance-2.0/reference-to-video`.

Set a Seedance 2.0 model as the default video provider:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "fal/bytedance/seedance-2.0/fast/text-to-video",
      },
    },
  },
}
```

Reference-to-video (e.g. `fal/bytedance/seedance-2.0/fast/reference-to-video`) accepts up to 9 images, 3 videos, and 3 audio references through the shared `video_generate` `images`, `videos`, and `audioRefs` parameters, with at most 12 total reference files. HeyGen is selected the same way by setting `videoGenerationModel.primary` to `fal/fal-ai/heygen/v2/video-agent`.

## Music generation

The bundled `fal` plugin also registers a music-generation provider for the shared `music_generate` tool.

| Capability | Value |
| --- | --- |
| Default model | `fal/fal-ai/minimax-music/v2.6` |
| Models | `fal-ai/minimax-music/v2.6`, `fal-ai/ace-step/prompt-to-audio`, `fal-ai/stable-audio-25/text-to-audio` |
| Runtime | Synchronous request plus generated audio download |

Set fal as the default music provider:

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "fal/fal-ai/minimax-music/v2.6",
      },
    },
  },
}
```

`fal-ai/minimax-music/v2.6` supports explicit lyrics and instrumental mode. ACE-Step and Stable Audio are prompt-to-audio endpoints; choose them with the `model` override when you want those model families.

**Source**: OpenClaw documentation — `providers/fal` (mirror `inbox/openclaw_docs/providers/fal.md`)
**Last Updated**: 2026-06-22
**Status**: Active
