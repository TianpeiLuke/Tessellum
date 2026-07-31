---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - image_generation
keywords:
  - openclaw image_generate tool
  - image generation async background task
  - imageGenerationModel primary fallbacks
  - provider selection order auto-detection
  - image editing reference images
  - openai gpt-image-2 codex oauth
  - aspectRatio resolution size hints
topics:
  - OpenClaw
  - Image Generation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/image-generation
access_control_group: ["general"]
---

# OpenClaw — Using the `image_generate` Tool

## Overview

This note is the **how-to-use** procedure for OpenClaw's `image_generate` tool: how the agent creates and edits images through configured providers, how chat-session generation runs asynchronously, how to authenticate and pick a default model, and the full tool-parameter and configuration surface. It mirrors the usage half of the `tools/image-generation` source page — the intro async-task model, Quick start, Common routes, Tool parameters, Configuration (Model selection, Provider selection order, Image editing), and Examples. The companion `oc_tools_image_generation_providers` note (model BB) owns the per-provider Supported-providers list, the capability matrix, and the provider deep dives; here every claim is the tool-usage contract.

## The async background-task model

The `image_generate` tool lets the agent create and edit images using your configured providers. In chat sessions, image generation runs asynchronously: OpenClaw records a background task, returns the task id immediately, and wakes the agent when the provider finishes. The completion agent follows the session's normal visible-reply mode — automatic final reply delivery when configured, or `message(action="send")` when the session requires the message tool. If the requester session is inactive or its active wake fails, and some generated images are still missing from the completion reply, OpenClaw sends an idempotent direct fallback with only the missing images.

The tool only appears when at least one image-generation provider is available. If you do not see `image_generate` in your agent's tools, configure `agents.defaults.imageGenerationModel`, set up a provider API key, or sign in with OpenAI ChatGPT/Codex OAuth.

## Quick start

Three steps bring the tool online:

1. **Configure auth** — set an API key for at least one provider (for example `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`) or sign in with OpenAI Codex OAuth.
2. **Pick a default model (optional)** — set `agents.defaults.imageGenerationModel`:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "openai/gpt-image-2",
        timeoutMs: 180_000,
      },
    },
  },
}
```

ChatGPT/Codex OAuth uses the same `openai/gpt-image-2` model ref. When an `openai` OAuth profile is configured, OpenClaw routes image requests through that OAuth profile instead of first trying `OPENAI_API_KEY`. Explicit `models.providers.openai` config (API key, custom/Azure base URL) opts back into the direct OpenAI Images API route.

3. **Ask the agent** — for example, _"Generate an image of a friendly robot mascot."_ The agent calls `image_generate` automatically. No tool allow-listing is needed — it is enabled by default when a provider is available. The tool returns a background task id, then the completion agent sends the generated attachment through the `message` tool when it is ready.

For OpenAI-compatible LAN endpoints such as LocalAI, keep the custom `models.providers.openai.baseUrl` and explicitly opt in with `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork: true`. Private and internal image endpoints remain blocked by default.

## Common routes

These provider/model refs cover the most frequent setups (model ref → required auth):

| Goal | Model ref | Auth |
| --- | --- | --- |
| OpenAI image generation with API billing | `openai/gpt-image-2` | `OPENAI_API_KEY` |
| OpenAI image generation with Codex subscription auth | `openai/gpt-image-2` | OpenAI ChatGPT/Codex OAuth |
| OpenAI transparent-background PNG/WebP | `openai/gpt-image-1.5` | `OPENAI_API_KEY` or OpenAI Codex OAuth |
| DeepInfra image generation | `deepinfra/black-forest-labs/FLUX-1-schnell` | `DEEPINFRA_API_KEY` |
| fal Krea 2 expressive/style-directed generation | `fal/krea/v2/medium/text-to-image` | `FAL_KEY` |
| OpenRouter image generation | `openrouter/google/gemini-3.1-flash-image-preview` | `OPENROUTER_API_KEY` |
| LiteLLM image generation | `litellm/gpt-image-2` | `LITELLM_API_KEY` |
| Microsoft Foundry MAI image generation | `microsoft-foundry/<deployment-name>` | `AZURE_OPENAI_API_KEY` or Entra ID |
| Google Gemini image generation | `google/gemini-3.1-flash-image-preview` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |

The same `image_generate` tool handles text-to-image and reference-image editing. Use `image` for one reference or `images` for multiple references. For Krea 2 models on fal, those references are sent as style references instead of edit inputs. Provider-supported output hints such as `quality`, `outputFormat`, and `background` are forwarded when available and reported as ignored when a provider does not support them. Bundled transparent-background support is OpenAI-specific; other providers may still preserve PNG alpha if their backend emits it.

## Tool parameters

The cross-provider parameter surface (verbatim from source):

- **`prompt`** (`string`, required) — image generation prompt; required for `action: "generate"`.
- **`action`** (`"generate" | "status" | "list"`, default `generate`) — use `"status"` to inspect the active session task or `"list"` to inspect available providers and models at runtime.
- **`model`** (`string`) — provider/model override (e.g. `openai/gpt-image-2`); use `openai/gpt-image-1.5` for transparent OpenAI backgrounds.
- **`image`** (`string`) — single reference image path or URL for edit mode.
- **`images`** (`string[]`) — multiple reference images for edit mode or style-reference models (up to 10 through the shared tool; provider-specific limits still apply).
- **`size`** (`string`) — size hint: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `3840x2160`.
- **`aspectRatio`** (`string`) — `1:1`, `2:3`, `3:2`, `2.35:1`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `4:1`, `1:4`, `8:1`, `1:8`; providers validate their model-specific subset.
- **`resolution`** (`"1K" | "2K" | "4K"`) — resolution hint.
- **`quality`** (`"low" | "medium" | "high" | "auto"`) — quality hint when the provider supports it.
- **`outputFormat`** (`"png" | "jpeg" | "webp"`) — output format hint when the provider supports it.
- **`background`** (`"transparent" | "opaque" | "auto"`) — background hint when the provider supports it; use `transparent` with `outputFormat: "png"` or `"webp"` for transparency-capable providers.
- **`count`** (`number`) — number of images to generate (1-4).
- **`timeoutMs`** (`number`) — optional provider request timeout in milliseconds; when Codex calls `image_generate` through dynamic tools, this per-call value still overrides the configured default and is capped at 600000 ms.
- **`filename`** (`string`) — output filename hint.
- **`openai`** (`object`) — OpenAI-only hints: `background`, `moderation`, `outputCompression`, and `user`.
- **`fal.creativity`** (`"raw" | "low" | "medium" | "high"`) — fal Krea 2 creativity control; defaults to `medium`.

Not all providers support all parameters. When a fallback provider supports a nearby geometry option instead of the exact requested one, OpenClaw remaps to the closest supported size, aspect ratio, or resolution before submission. Unsupported output hints are dropped for providers that do not declare support and reported in the tool result. Tool results report the applied settings; `details.normalization` captures any requested-to-applied translation.

## Configuration

### Model selection

Configure a primary model plus an ordered list of fallbacks under `agents.defaults.imageGenerationModel`:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "openai/gpt-image-2",
        timeoutMs: 180_000,
        fallbacks: [
          "openrouter/google/gemini-3.1-flash-image-preview",
          "google/gemini-3.1-flash-image-preview",
          "fal/fal-ai/flux/dev",
        ],
      },
    },
  },
}
```

### Provider selection order

OpenClaw tries providers in this order:

1. **`model` parameter** from the tool call (if the agent specifies one).
2. **`imageGenerationModel.primary`** from config.
3. **`imageGenerationModel.fallbacks`** in order.
4. **Auto-detection** — auth-backed provider defaults only: the current default provider first, then the remaining registered image-generation providers in provider-id order.

If a provider fails (auth error, rate limit, etc.), the next configured candidate is tried automatically. If all fail, the error includes details from each attempt. Three rules refine this order. **Per-call model overrides are exact**: a per-call `model` override tries only that provider/model and does not continue to configured primary/fallback or auto-detected providers. **Auto-detection is auth-aware**: a provider default only enters the candidate list when OpenClaw can actually authenticate that provider; set `agents.defaults.mediaGenerationAutoProviderFallback: false` to use only explicit `model`, `primary`, and `fallbacks` entries. **Timeouts** are layered: set `agents.defaults.imageGenerationModel.timeoutMs` for slow image backends; a per-call `timeoutMs` tool parameter overrides the configured default, and configured defaults override plugin-authored provider defaults — Google and OpenRouter hosted image providers use 180-second defaults, while Microsoft Foundry MAI, xAI, and Azure OpenAI image generation use 600 seconds, and Codex dynamic-tool calls use a 120-second `image_generate` bridge default (honoring the same timeout budget when configured, bounded by OpenClaw's 600000 ms dynamic-tool bridge maximum). Use `action: "list"` to inspect the currently registered providers, their default models, and auth env-var hints.

### Image editing

OpenAI, OpenRouter, Google, DeepInfra, fal, Microsoft Foundry, MiniMax, ComfyUI, and xAI support editing reference images. Krea 2 models on fal use the same `image` / `images` fields as style references instead of edit inputs. Pass a reference image path or URL alongside the prompt:

```text
"Generate a watercolor version of this photo" + image: "/path/to/photo.jpg"
```

OpenAI, OpenRouter, Google, and xAI support up to 5 reference images via the `images` parameter. fal supports 1 reference image for Flux image-to-image, up to 10 for GPT Image 2 edits, up to 10 style references for Krea 2, and up to 14 for Nano Banana 2 edits. Microsoft Foundry, MiniMax, and ComfyUI support 1.

## Examples

Common invocations as `/tool` calls (the CLI equivalents use `openclaw infer image generate`/`edit` with matching `--model`, `--output-format`, `--background`, `--quality`, and `--openai-moderation` flags; `--openai-background` remains an OpenAI-specific alias):

```text
/tool image_generate action=generate model=openai/gpt-image-2 prompt="A clean editorial poster for OpenClaw image generation" size=3840x2160 count=1
/tool image_generate action=generate model=openai/gpt-image-1.5 prompt="A simple red circle sticker on a transparent background" outputFormat=png background=transparent
/tool image_generate action=generate model=openai/gpt-image-2 prompt="Low-cost draft poster for a quiet productivity app" quality=low openai='{"moderation":"low"}'
/tool image_generate action=generate model=openai/gpt-image-2 prompt="Keep the subject, replace the background with a bright studio setup" image=/path/to/reference.png size=1024x1536
/tool image_generate action=generate model=openai/gpt-image-2 prompt="Combine the character identity from the first image with the color palette from the second" images='["/path/to/character.png","/path/to/palette.jpg"]' size=1536x1024
/tool image_generate action=generate model=fal/krea/v2/medium/text-to-image prompt="An expressive editorial portrait using this color palette and print texture" images='["/path/to/palette.png","/path/to/texture.jpg"]' aspectRatio=9:16 fal='{"creativity":"high"}'
```

Bundled providers other than OpenAI do not declare explicit background control today, so `background: "transparent"` is reported as ignored for them.

**Source**: OpenClaw documentation — `tools/image-generation` (mirror `inbox/openclaw_docs/tools/image-generation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
