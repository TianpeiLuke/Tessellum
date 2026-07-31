---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - video_generation
keywords:
  - openclaw video generation providers
  - video_generate capability matrix
  - sixteen video backends
  - generate imageToVideo videoToVideo modes
  - provider capability blocks
  - veo sora runway seedance kling
  - maxInputImagesByModel
  - video provider default models
topics:
  - OpenClaw
  - Video Generation Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/tools/video-generation
access_control_group: ["general"]
---

# OpenClaw — Video Generation Provider Reference

## Overview

This note models the OpenClaw **video-generation provider reference**: the sixteen backends `video_generate` can dispatch to, their default models and auth env vars, the explicit per-mode capability contract (`generate` / `imageToVideo` / `videoToVideo`), per-provider behavioral notes, and the opt-in live-test sweep. It mirrors the `tools/video-generation` source page sections **Supported providers**, **Capability matrix**, **Provider notes**, **Provider capability modes**, and **Live tests**. The `video_generate` agent tool itself — async task lifecycle, parameters, actions, model-selection order, and config — is covered by its sibling note (see Related Notes); this note is the static provider/capability data the tool resolves against.

## Supported Providers

Sixteen provider backends are supported, each with different model options, input modes, and feature sets. The agent picks the right provider automatically based on configuration and available API keys. The default-model + reference-support + auth matrix from the source page:

| Provider | Default model | Text | Image ref | Video ref | Auth |
| --- | --- | :--: | --- | --- | --- |
| Alibaba | `wan2.6-t2v` | ✓ | Yes (remote URL) | Yes (remote URL) | `MODELSTUDIO_API_KEY` |
| BytePlus (1.0) | `seedance-1-0-pro-250528` | ✓ | Up to 2 images (I2V models only; first + last frame) | - | `BYTEPLUS_API_KEY` |
| BytePlus Seedance 1.5 | `seedance-1-5-pro-251215` | ✓ | Up to 2 images (first + last frame via role) | - | `BYTEPLUS_API_KEY` |
| BytePlus Seedance 2.0 | `dreamina-seedance-2-0-260128` | ✓ | Up to 9 reference images | Up to 3 videos | `BYTEPLUS_API_KEY` |
| ComfyUI | `workflow` | ✓ | 1 image | - | `COMFY_API_KEY` or `COMFY_CLOUD_API_KEY` |
| DeepInfra | `Pixverse/Pixverse-T2V` | ✓ | - | - | `DEEPINFRA_API_KEY` |
| fal | `fal-ai/minimax/video-01-live` | ✓ | 1 image; up to 9 with Seedance reference-to-video | Up to 3 videos with Seedance reference-to-video | `FAL_KEY` |
| Google | `veo-3.1-fast-generate-preview` | ✓ | 1 image | 1 video | `GEMINI_API_KEY` |
| MiniMax | `MiniMax-Hailuo-2.3` | ✓ | 1 image | - | `MINIMAX_API_KEY` or MiniMax OAuth |
| OpenAI | `sora-2` | ✓ | 1 image | 1 video | `OPENAI_API_KEY` |
| OpenRouter | `google/veo-3.1-fast` | ✓ | Up to 4 images (first/last frame or references) | - | `OPENROUTER_API_KEY` |
| Qwen | `wan2.6-t2v` | ✓ | Yes (remote URL) | Yes (remote URL) | `QWEN_API_KEY` |
| Runway | `gen4.5` | ✓ | 1 image | 1 video | `RUNWAYML_API_SECRET` |
| Together | `Wan-AI/Wan2.2-T2V-A14B` | ✓ | `Wan-AI/Wan2.2-I2V-A14B` only | - | `TOGETHER_API_KEY` |
| Vydra | `veo3` | ✓ | 1 image (`kling`) | - | `VYDRA_API_KEY` |
| xAI | `grok-imagine-video` | ✓ | 1 first-frame image or up to 7 `reference_image`s | 1 video | `XAI_API_KEY` |

Some providers accept additional or alternate API key env vars; see the individual provider pages for details. Run `video_generate action=list` to inspect available providers, models, and runtime modes at runtime.

## Capability Matrix

The explicit mode contract used by `video_generate`, contract tests, and the shared live sweep. Each provider declares which of the three runtime modes it supports, plus which lanes the shared live sweep actually exercises today and why some are skipped:

| Provider | `generate` | `imageToVideo` | `videoToVideo` | Shared live lanes today |
| --- | :--: | :--: | :--: | --- |
| Alibaba | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; `videoToVideo` skipped because this provider needs remote `http(s)` video URLs |
| BytePlus | ✓ | ✓ | - | `generate`, `imageToVideo` |
| ComfyUI | ✓ | ✓ | - | Not in the shared sweep; workflow-specific coverage lives with Comfy tests |
| DeepInfra | ✓ | - | - | `generate`; native DeepInfra video schemas are text-to-video in the plugin contract |
| fal | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; `videoToVideo` only when using Seedance reference-to-video |
| Google | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; shared `videoToVideo` skipped because the current buffer-backed Gemini/Veo sweep does not accept that input |
| MiniMax | ✓ | ✓ | - | `generate`, `imageToVideo` |
| OpenAI | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; shared `videoToVideo` skipped because this org/input path currently needs provider-side video edit access |
| OpenRouter | ✓ | ✓ | - | `generate`, `imageToVideo` |
| Qwen | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; `videoToVideo` skipped because this provider needs remote `http(s)` video URLs |
| Runway | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; `videoToVideo` runs only when the selected model is `runway/gen4_aleph` |
| Together | ✓ | ✓ | - | `generate`, `imageToVideo` |
| Vydra | ✓ | ✓ | - | `generate`; shared `imageToVideo` skipped because bundled `veo3` is text-only and bundled `kling` requires a remote image URL |
| xAI | ✓ | ✓ | ✓ | `generate`, `imageToVideo`; `videoToVideo` skipped because this provider currently needs a remote MP4 URL |

## Provider Notes

Per-provider behavioral details, additional model ids, transport endpoints, and `providerOptions` support taken verbatim from the source page's provider accordions:

- **Alibaba** — Uses DashScope / Model Studio async endpoint. Reference images and videos must be remote `http(s)` URLs.
- **BytePlus (1.0)** — Provider id: `byteplus`. Models: `seedance-1-0-pro-250528` (default), `seedance-1-0-pro-t2v-250528`, `seedance-1-0-pro-fast-251015`, `seedance-1-0-lite-t2v-250428`, `seedance-1-0-lite-i2v-250428`. T2V models (`*-t2v-*`) do not accept image inputs; I2V models and general `*-pro-*` models support a single reference image (first frame). Pass the image positionally or set `role: "first_frame"`. T2V model IDs are automatically switched to the corresponding I2V variant when an image is provided. Supported `providerOptions` keys: `seed` (number), `draft` (boolean — forces 480p), `camera_fixed` (boolean).
- **BytePlus Seedance 1.5** — Requires the `@openclaw/byteplus-modelark` plugin. Provider id: `byteplus-seedance15`. Model: `seedance-1-5-pro-251215`. Uses the unified `content[]` API. Supports at most 2 input images (`first_frame` + `last_frame`). All inputs must be remote `https://` URLs. Set `role: "first_frame"` / `"last_frame"` on each image, or pass images positionally. `aspectRatio: "adaptive"` auto-detects ratio from the input image. `audio: true` maps to `generate_audio`. `providerOptions.seed` (number) is forwarded.
- **BytePlus Seedance 2.0** — Requires the `@openclaw/byteplus-modelark` plugin. Provider id: `byteplus-seedance2`. Models: `dreamina-seedance-2-0-260128`, `dreamina-seedance-2-0-fast-260128`. Uses the unified `content[]` API. Supports up to 9 reference images, 3 reference videos, and 3 reference audios. All inputs must be remote `https://` URLs. Set `role` on each asset — supported values: `"first_frame"`, `"last_frame"`, `"reference_image"`, `"reference_video"`, `"reference_audio"`. `aspectRatio: "adaptive"` auto-detects ratio from the input image. `audio: true` maps to `generate_audio`. `providerOptions.seed` (number) is forwarded.
- **ComfyUI** — Workflow-driven local or cloud execution. Supports text-to-video and image-to-video through the configured graph.
- **fal** — Uses a queue-backed flow for long-running jobs. OpenClaw waits up to 20 minutes by default before treating an in-progress fal queue job as timed out. Most fal video models accept a single image reference. Seedance 2.0 reference-to-video models accept up to 9 images, 3 videos, and 3 audio references, with at most 12 total reference files.
- **Google (Gemini / Veo)** — Supports one image or one video reference. Generated-audio requests are ignored with a warning on the Gemini API path because that API rejects the `generateAudio` parameter for current Veo video generation.
- **MiniMax** — Single image reference only. MiniMax accepts `768P` and `1080P` resolutions; requests such as `720P` are normalized to the closest supported value before submission.
- **OpenAI** — Only `size` override is forwarded. Other style overrides (`aspectRatio`, `resolution`, `audio`, `watermark`) are ignored with a warning.
- **OpenRouter** — Uses OpenRouter's asynchronous `/videos` API. OpenClaw submits the job, polls `polling_url`, and downloads either `unsigned_urls` or the documented job content endpoint. The bundled `google/veo-3.1-fast` default advertises 4/6/8 second durations, `720P`/`1080P` resolutions, and `16:9`/`9:16` aspect ratios.
- **Qwen** — Same DashScope backend as Alibaba. Reference inputs must be remote `http(s)` URLs; local files are rejected upfront.
- **Runway** — Supports local files via data URIs. Video-to-video requires `runway/gen4_aleph`. Text-only runs expose `16:9` and `9:16` aspect ratios.
- **Together** — Single image reference only.
- **Vydra** — Uses `https://www.vydra.ai/api/v1` directly to avoid auth-dropping redirects. `veo3` is bundled as text-to-video only; `kling` requires a remote image URL.
- **xAI** — Supports text-to-video, single first-frame image-to-video, up to 7 `reference_image` inputs through xAI `reference_images`, and remote video edit/extend flows.

## Provider Capability Modes

The shared video-generation contract supports mode-specific capabilities instead of only flat aggregate limits. New provider implementations should prefer explicit mode blocks:

```typescript
capabilities: {
  generate: {
    maxVideos: 1,
    maxDurationSeconds: 10,
    supportsResolution: true,
  },
  imageToVideo: {
    enabled: true,
    maxVideos: 1,
    maxInputImages: 1,
    maxInputImagesByModel: { "provider/reference-to-video": 9 },
    maxDurationSeconds: 5,
  },
  videoToVideo: {
    enabled: true,
    maxVideos: 1,
    maxInputVideos: 1,
    maxDurationSeconds: 5,
  },
}
```

Flat aggregate fields such as `maxInputImages` and `maxInputVideos` are **not** enough to advertise transform-mode support. Providers should declare `generate`, `imageToVideo`, and `videoToVideo` explicitly so live tests, contract tests, and the shared `video_generate` tool can validate mode support deterministically. When one model in a provider has wider reference-input support than the rest, use `maxInputImagesByModel`, `maxInputVideosByModel`, or `maxInputAudiosByModel` instead of raising the mode-wide limit.

## Live Tests

Opt-in live coverage for the shared bundled providers runs through a release-safe smoke test:

```bash
OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/video-generation-providers.live.test.ts
```

A repo wrapper exists (`pnpm test:live:media video`). This live file uses already-exported provider env vars ahead of stored auth profiles by default, and runs a release-safe smoke by default: `generate` for every non-FAL provider in the sweep, a one-second lobster prompt, and a per-provider operation cap from `OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS` (`180000` by default). FAL is opt-in because provider-side queue latency can dominate release time (`pnpm test:live:media video --video-providers fal`). Set `OPENCLAW_LIVE_VIDEO_GENERATION_FULL_MODES=1` to also run declared transform modes the shared sweep can exercise safely with local media: `imageToVideo` when `capabilities.imageToVideo.enabled`, and `videoToVideo` when `capabilities.videoToVideo.enabled` and the provider/model accepts buffer-backed local video input in the shared sweep. Today the shared `videoToVideo` live lane covers `runway` only when you select `runway/gen4_aleph`.

**Source**: OpenClaw documentation — `tools/video-generation` (mirror `inbox/openclaw_docs/tools/video-generation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
