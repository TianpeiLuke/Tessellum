---
tags:
  - resource
  - documentation
  - hermes_agent
  - image_generation
  - media
keywords:
  - image generation
  - FAL.ai
  - text-to-image
  - FLUX 2 Klein
  - image_generate tool
  - Clarity Upscaler
topics:
  - Hermes Agent
  - Image Generation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation
access_control_group: ["general"]
---

# Hermes Image Generation

## Overview

Image generation is Hermes Agent's **text-to-image** (and optionally image-to-image) capability: the agent turns a text prompt into a rendered image via [FAL.ai](https://fal.ai/). Eleven models ship out of the box — each with a different speed / quality / cost tradeoff — and the active model is user-configurable via the `hermes tools` picker, persisting in `config.yaml` under `image_gen.model`. The agent-facing tool (`image_generate`) is deliberately minimal: the user picks a model once, and the agent just describes what to draw. Internally a resolve → build-payload → submit → (optional) upscale → deliver pipeline maps the agent's one-word aspect ratio onto each model's native size spec, routes the request through either a direct FAL key or the managed Nous gateway, and emits a `MEDIA:<url>` tag that per-platform adapters convert to native media. This page documents the model catalog, setup, the editing path, aspect-ratio mapping, per-model upscaling, the internal pipeline, debugging, delivery, and limitations.

## Supported Models

Eleven models are supported, defaulting to `fal-ai/flux-2/klein/9b` (fast, sub-second, crisp text). The full catalog spans fast/cheap (`z-image/turbo`, Klein 9B), studio photorealism (`flux-2-pro`, `gpt-image-2`, Krea V2 Large), best-typography (`ideogram/v3`, `gpt-image-2`), reasoning-depth text rendering (`nano-banana-pro`), design/brand-system (`recraft/v4/pro`), and illustration/anime (`krea/v2/medium`):

| Model | Speed | Strengths | Price |
|---|---|---|---|
| `fal-ai/flux-2/klein/9b` *(default)* | `<1s` | Fast, crisp text | $0.006/MP |
| `fal-ai/flux-2-pro` | ~6s | Studio photorealism | $0.03/MP |
| `fal-ai/z-image/turbo` | ~2s | Bilingual EN/CN, 6B params | $0.005/MP |
| `fal-ai/nano-banana-pro` | ~8s | Gemini 3 Pro, reasoning depth, text rendering | $0.15/image (1K) |
| `fal-ai/gpt-image-1.5` | ~15s | Prompt adherence | $0.034/image |
| `fal-ai/gpt-image-2` | ~20s | SOTA text rendering + CJK, world-aware photorealism | $0.04–0.06/image |
| `fal-ai/ideogram/v3` | ~5s | Best typography | $0.03–0.09/image |
| `fal-ai/recraft/v4/pro/text-to-image` | ~8s | Design, brand systems, production-ready | $0.25/image |
| `fal-ai/qwen-image` | ~12s | LLM-based, complex text | $0.02/MP |
| `fal-ai/krea/v2/medium/text-to-image` | ~15-25s | Illustration, anime, painting, expressive/artistic styles | $0.030–0.035/image |
| `fal-ai/krea/v2/large/text-to-image` | ~25-60s | Photorealism, raw textured looks (motion blur, grain, film) | $0.060–0.065/image |

Prices are FAL's pricing at time of writing (as of 2026); the source directs readers to [fal.ai](https://fal.ai/) for current numbers.

## Setup

Two backend paths exist. **Nous Subscribers** with a paid [Nous Portal](https://portal.nousresearch.com) subscription can use image generation through the **Tool Gateway** without a FAL API key — model selection persists across both paths. New installs run `hermes setup --portal` to log in and enable every gateway tool at once; existing installs select **Nous Subscription** as the image-gen backend via `hermes tools`. If the managed gateway returns `HTTP 4xx` for a specific model, that model isn't yet proxied on the portal side — the agent reports this with remediation steps (set `FAL_KEY` for direct access, or pick a different model).

For direct FAL access: sign up at [fal.ai](https://fal.ai/) and generate an API key from the dashboard. Then run the tools command, navigate to **🎨 Image Generation**, pick the backend (Nous Subscription or FAL.ai), and select a model from the column-aligned picker (arrow keys to navigate, Enter to select):

```bash
hermes tools
```

The selection is saved to `config.yaml`:

```yaml
image_gen:
  model: fal-ai/flux-2/klein/9b
  use_gateway: false            # true if using Nous Subscription
```

**GPT-Image quality** is pinned: `fal-ai/gpt-image-1.5` and `fal-ai/gpt-image-2` request quality is fixed to `medium` (~$0.034–$0.06/image at 1024×1024). The `low` / `high` tiers are not exposed as a user-facing option so that Nous Portal billing stays predictable across all users — the cost spread between tiers is 3–22×. For a cheaper option pick Klein 9B or Z-Image Turbo; for higher quality use Nano Banana Pro or Recraft V4 Pro.

## Usage

The agent-facing schema is intentionally minimal — the model picks up whatever the user has configured, so the prompt is just natural language describing the desired image (optionally hinting at orientation or a specialized model):

```
Generate an image of a serene mountain landscape with cherry blossoms
```

```
Create a square portrait of a wise old owl — use the typography model
```

## Image-to-Image / Editing

The same `image_generate` tool also **edits existing images** when the active model supports it — pass a source image and the backend routes to its editing endpoint automatically (mirroring how `video_generate` handles image-to-video). Omit the source image and it is plain text-to-image. Two inputs drive the edit: **`image_url`** (the primary source image to edit/transform — public URL or local path) and **`reference_image_urls`** (additional style/composition references, capped per-model).

Which backends support editing:

| Backend | Image-to-image | Reference cap | How |
|---|---|---|---|
| **FAL.ai** (edit-capable models below) | ✓ | up to 9 | routes to the model's `/edit` endpoint |
| **OpenAI** (`gpt-image-2`) | ✓ | up to 16 | `images.edit()` |
| **xAI** (Grok Imagine) | ✓ | 1 | `/v1/images/edits` (`grok-imagine-image-quality`) |
| **Krea** (`Krea 2`) | ✓ | up to 10 | reference-guided generation (`image_style_references`) |
| **OpenAI (Codex auth)** | ✗ | — | text-to-image only |

FAL models with an editing endpoint: `flux-2/klein/9b`, `flux-2-pro`, `nano-banana-pro`, `gpt-image-1.5`, `gpt-image-2`, `ideogram/v3`, and `qwen-image`. Pure text-to-image FAL models (`z-image/turbo`, `recraft`, `krea/*`) reject image inputs with a clear error pointing at an edit-capable model. The active model's editing capability is surfaced in the tool description at runtime, so the agent knows whether `image_url` will be honored before it calls the tool.

## Aspect Ratios

Every model accepts the same three aspect ratios (`landscape` / `square` / `portrait`) from the agent's perspective; internally each model's native size spec is filled in automatically:

| Agent input | image_size (flux/z-image/qwen/recraft/ideogram) | aspect_ratio (nano-banana-pro) | image_size (gpt-image-1.5) | image_size (gpt-image-2) |
|---|---|---|---|---|
| `landscape` | `landscape_16_9` | `16:9` | `1536x1024` | `landscape_4_3` (1024×768) |
| `square` | `square_hd` | `1:1` | `1024x1024` | `square_hd` (1024×1024) |
| `portrait` | `portrait_16_9` | `9:16` | `1024x1536` | `portrait_4_3` (768×1024) |

GPT Image 2 maps to 4:3 presets rather than 16:9 because its minimum pixel count is 655,360 — the `landscape_16_9` preset (1024×576 = 589,824) would be rejected. This translation happens in `_build_fal_payload()`, so agent code never has to know about per-model schema differences.

## Automatic Upscaling

Upscaling via FAL's **Clarity Upscaler** is gated per-model: only `fal-ai/flux-2-pro` upscales (backward-compat, as it was the pre-picker default). All other models do not — fast models would lose their sub-second value proposition, and hi-res models don't need it. When upscaling runs it uses an upscale factor of 2×, creativity 0.35, resemblance 0.6, guidance scale 4, and 18 inference steps. If upscaling fails (network issue, rate limit), the original image is returned automatically.

## How It Works Internally

The image-generation pipeline runs five steps:

1. **Model resolution** — `_resolve_fal_model()` reads `image_gen.model` from `config.yaml`, falls back to the `FAL_IMAGE_MODEL` env var, then to `fal-ai/flux-2/klein/9b`.
2. **Payload building** — `_build_fal_payload()` translates the `aspect_ratio` into the model's native format (preset enum, aspect-ratio enum, or GPT literal), merges the model's default params, applies any caller overrides, then filters to the model's `supports` whitelist so unsupported keys are never sent.
3. **Submission** — `_submit_fal_request()` routes via direct FAL credentials or the managed Nous gateway.
4. **Upscaling** — runs only if the model's metadata has `upscale: True`.
5. **Delivery** — the final image URL is returned to the agent, which emits a `MEDIA:<url>` tag that platform adapters convert to native media.

## Debugging

Enable debug logging with an environment variable; debug logs go to `./logs/image_tools_debug_<session_id>.json` with per-call details (model, parameters, timing, errors):

```bash
export IMAGE_TOOLS_DEBUG=true
```

## Platform Delivery

Per-platform delivery of the generated image:

| Platform | Delivery |
|---|---|
| **CLI** | Image URL printed as markdown `![](url)` — click to open |
| **Telegram** | Photo message with the prompt as caption |
| **Discord** | Embedded in a message |
| **Slack** | URL unfurled by Slack |
| **WhatsApp** | Media message |
| **Others** | URL in plain text |

## Limitations

- **Requires credentials** for the active backend (FAL `FAL_KEY` / Nous Subscription, `OPENAI_API_KEY`, xAI OAuth, `KREA_API_KEY`).
- **Editing is model-dependent** — image-to-image works only on edit-capable models (see the editing table); text-to-image-only models reject image inputs with a clear error.
- **Temporary URLs** — backends return hosted URLs that expire after hours/days; Hermes materializes them to the local cache so delivery still works after expiry.
- **Per-model constraints** — some models don't support `seed`, `num_inference_steps`, etc. The `supports` / `edit_supports` filter silently drops unsupported params; this is expected behavior.

**Source**: `inbox/hermes_agent_docs/user-guide/features/image-generation.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation
**Last Updated**: 2026-06-19
**Status**: Active
