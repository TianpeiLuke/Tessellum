---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - providers
keywords:
  - openclaw image_generate providers
  - image generation provider capabilities matrix
  - openai gpt-image-2 codex oauth
  - microsoft foundry mai image models
  - openrouter image models
  - fal krea 2
  - minimax dual-auth image
  - xai grok-imagine-image
  - provider default models edit support
  - provider auth env vars
topics:
  - OpenClaw
  - Image Generation Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/tools/image-generation
access_control_group: ["general"]
---

# OpenClaw — image_generate Provider & Capability Reference

## Overview

This note is the provider/capability reference half of the OpenClaw `image_generate` tool, modeling the per-provider backends the tool dispatches to — mirroring the **Supported providers**, **Provider capabilities**, and **Provider deep dives** sections of the `tools/image-generation` source page. It catalogs the 11 supported image-generation providers with their default models and auth, the per-provider capability matrix (max generate count, edit/reference limits, size/aspect/resolution support), and the six provider deep dives (OpenAI, Microsoft Foundry, OpenRouter, fal Krea 2, MiniMax, xAI). The how-to-use-the-tool half (async task model, quick start, common routes, tool parameters, configuration, image editing, examples) lives in the sibling note **[oc_tools_image_generation](oc_tools_image_generation.md)**.

## Supported providers

The `image_generate` tool routes to eleven providers. Each has a provider id (used as a `provider/model` prefix), a default model, an edit/reference-support level, and an auth path:

| Provider          | Default model                           | Edit support                       | Auth                                                  |
| ----------------- | --------------------------------------- | ---------------------------------- | ----------------------------------------------------- |
| ComfyUI           | `workflow`                              | Yes (1 image, workflow-configured) | `COMFY_API_KEY` or `COMFY_CLOUD_API_KEY` for cloud    |
| DeepInfra         | `black-forest-labs/FLUX-1-schnell`      | Yes (1 image)                      | `DEEPINFRA_API_KEY`                                   |
| fal               | `fal-ai/flux/dev`                       | Yes (model-specific limits)        | `FAL_KEY`                                             |
| Google            | `gemini-3.1-flash-image-preview`        | Yes                                | `GEMINI_API_KEY` or `GOOGLE_API_KEY`                  |
| LiteLLM           | `gpt-image-2`                           | Yes (up to 5 input images)         | `LITELLM_API_KEY`                                     |
| Microsoft Foundry | `<deployment-name>`                     | Yes (MAI-Image-2.5 models only)    | `AZURE_OPENAI_API_KEY` or Entra ID (`az login`)       |
| MiniMax           | `image-01`                              | Yes (subject reference)            | `MINIMAX_API_KEY` or MiniMax OAuth (`minimax-portal`) |
| OpenAI            | `gpt-image-2`                           | Yes (up to 4 images)               | `OPENAI_API_KEY` or OpenAI ChatGPT/Codex OAuth        |
| OpenRouter        | `google/gemini-3.1-flash-image-preview` | Yes (up to 5 input images)         | `OPENROUTER_API_KEY`                                  |
| Vydra             | `grok-imagine`                          | No                                 | `VYDRA_API_KEY`                                       |
| xAI               | `grok-imagine-image`                    | Yes (up to 5 images)               | `XAI_API_KEY`                                         |

Microsoft Foundry has no provider-level default model (the `<deployment-name>` placeholder reflects that the MAI API expects your deployment name in the `model` field — see the deep dive). The runtime `action: "list"` inspects the currently registered providers, their default models, and auth env-var hints; `action: "status"` inspects the active image-generation task for the current session (both are documented in the usage sibling note).

## Provider capabilities

The cross-provider capability matrix records, per provider, the maximum generate count, the edit/reference-image limit, and whether explicit size, aspect-ratio, and resolution hints are supported. A dash (`-`) means the provider does not declare support for that capability (so a requested hint is reported in `ignoredOverrides` rather than sent):

| Capability            | ComfyUI            | DeepInfra | fal                                            | Google         | Microsoft Foundry | MiniMax               | OpenAI         | Vydra | xAI            |
| --------------------- | ------------------ | --------- | ---------------------------------------------- | -------------- | ----------------- | --------------------- | -------------- | ----- | -------------- |
| Generate (max count)  | Workflow-defined   | 4         | 4                                              | 4              | 1                 | 9                     | 4              | 1     | 4              |
| Edit / reference      | 1 image (workflow) | 1 image   | Flux: 1; GPT: 10; Krea style refs: 10; NB2: 14 | Up to 5 images | 1 image           | 1 image (subject ref) | Up to 5 images | -     | Up to 5 images |
| Size control          | -                  | ✓         | ✓                                              | ✓              | ✓                 | -                     | Up to 4K       | -     | -              |
| Aspect ratio          | -                  | -         | ✓                                              | ✓              | -                 | ✓                     | -              | -     | ✓              |
| Resolution (1K/2K/4K) | -                  | -         | ✓                                              | ✓              | -                 | -                     | -              | -     | 1K, 2K         |

The capability differences here drive the provider-selection fallback behavior: when a fallback provider supports a *nearby* geometry option instead of the exact requested one, OpenClaw remaps to the closest supported size, aspect ratio, or resolution before submission, and `details.normalization` captures any requested-to-applied translation.

## Provider deep dives

### OpenAI gpt-image-2 (and gpt-image-1.5)

OpenAI image generation defaults to `openai/gpt-image-2`. If an `openai` OAuth profile is configured, OpenClaw reuses the same OAuth profile used by Codex subscription chat models and sends the image request through the Codex Responses backend; legacy Codex base URLs such as `https://chatgpt.com/backend-api` are canonicalized to `https://chatgpt.com/backend-api/codex` for image requests. OpenClaw does **not** silently fall back to `OPENAI_API_KEY` for that request — to force direct OpenAI Images API routing, configure `models.providers.openai` explicitly with an API key, custom base URL, or Azure endpoint.

The `openai/gpt-image-1.5`, `openai/gpt-image-1`, and `openai/gpt-image-1-mini` models can still be selected explicitly. Use `gpt-image-1.5` for transparent-background PNG/WebP output; the current `gpt-image-2` API rejects `background: "transparent"`. `gpt-image-2` supports both text-to-image generation and reference-image editing through the same `image_generate` tool. OpenClaw forwards `prompt`, `count`, `size`, `quality`, `outputFormat`, and reference images to OpenAI; OpenAI does **not** receive `aspectRatio` or `resolution` directly — when possible OpenClaw maps those into a supported `size`, otherwise the tool reports them as ignored overrides.

OpenAI-specific options live under the `openai` object:

```json
{
  "quality": "low",
  "outputFormat": "jpeg",
  "openai": {
    "background": "opaque",
    "moderation": "low",
    "outputCompression": 60,
    "user": "end-user-42"
  }
}
```

`openai.background` accepts `transparent`, `opaque`, or `auto`; transparent outputs require `outputFormat` `png` or `webp` and a transparency-capable OpenAI image model, and OpenClaw routes default `gpt-image-2` transparent-background requests to `gpt-image-1.5`. `openai.outputCompression` applies to JPEG/WebP outputs and is ignored for PNG outputs. The top-level `background` hint is provider-neutral and currently maps to the same OpenAI `background` request field when the OpenAI provider is selected; providers that do not declare background support return it in `ignoredOverrides` instead of receiving the unsupported parameter. To route OpenAI image generation through an Azure OpenAI deployment instead of `api.openai.com`, see the Azure OpenAI endpoints reference linked from the source page's `/providers/openai#azure-openai-endpoints`.

### Microsoft Foundry MAI image models

Microsoft Foundry image generation uses deployed MAI image deployment names under the `microsoft-foundry/` provider prefix. There is no provider-level default model because the MAI API expects your deployment name in the `model` field:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "microsoft-foundry/<deployment-name>",
        timeoutMs: 600_000,
      },
    },
  },
}
```

The provider uses Microsoft Foundry's MAI API, not the OpenAI Images API. The generation endpoint is `/mai/v1/images/generations` and the edit endpoint is `/mai/v1/images/edits`; auth is `AZURE_OPENAI_API_KEY` / provider API key, or Entra ID through `az login`. Output is one PNG image. Size defaults to `1024x1024`, where width and height must each be at least 768 px and total pixels must be at most 1,048,576. Edits accept one PNG or JPEG reference image, supported only by `MAI-Image-2.5-Flash` and `MAI-Image-2.5` deployments. Prompt-only generation can use a custom deployment name with just the Foundry endpoint configured, but edits with custom deployment names need onboarding/model metadata so OpenClaw can verify that the deployment is backed by `MAI-Image-2.5-Flash` or `MAI-Image-2.5`. Current MAI image models are `MAI-Image-2.5-Flash`, `MAI-Image-2.5`, `MAI-Image-2e`, and `MAI-Image-2`.

### OpenRouter image models

OpenRouter image generation uses the same `OPENROUTER_API_KEY` and routes through OpenRouter's chat completions image API. OpenRouter image models are selected with the `openrouter/` prefix; OpenClaw forwards `prompt`, `count`, reference images, and Gemini-compatible `aspectRatio` / `resolution` hints to OpenRouter. Current built-in OpenRouter image model shortcuts include `google/gemini-3.1-flash-image-preview`, `google/gemini-3-pro-image-preview`, and `openai/gpt-5.4-image-2`; use `action: "list"` to see what your configured plugin exposes.

### fal Krea 2

Krea 2 models on fal use fal's native Krea schema instead of the generic `image_size` schema used by Flux. For Krea 2, OpenClaw sends `aspect_ratio` for aspect-ratio hints, `creativity` (defaulting to `medium`), and `image_style_references` when `image` or `images` are supplied — that is, references are treated as style references rather than edit inputs. Select Krea 2 Medium for faster expressive illustration and Krea 2 Large for slower, more detailed photoreal and textured looks. Krea 2 currently returns one image per request. Prefer `aspectRatio` for Krea: OpenClaw maps `size` to the closest supported Krea aspect ratio and *rejects* `resolution` for Krea rather than dropping it. Use the `fal.creativity` hint when you want a native Krea creativity level:

```json
{
  "model": "fal/krea/v2/medium/text-to-image",
  "prompt": "A cyber zine portrait with risograph texture",
  "aspectRatio": "9:16",
  "fal": {
    "creativity": "high"
  }
}
```

### MiniMax dual-auth

MiniMax image generation is available through both bundled MiniMax auth paths: `minimax/image-01` for API-key setups and `minimax-portal/image-01` for OAuth setups. (Per the capability matrix, MiniMax supports up to 9 generated images and 1 subject-reference edit image.)

### xAI grok-imagine-image

The bundled xAI provider uses `/v1/images/generations` for prompt-only requests and `/v1/images/edits` when `image` or `images` is present. Its models are `xai/grok-imagine-image` and `xai/grok-imagine-image-quality`; generate count is up to 4, references are one `image` or up to five `images`, supported aspect ratios are `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`, supported resolutions are `1K` and `2K`, and outputs are returned as OpenClaw-managed image attachments. OpenClaw intentionally does **not** expose xAI-native `quality`, `mask`, `user`, or extra native-only aspect ratios until those controls exist in the shared cross-provider `image_generate` contract.

**Source**: OpenClaw documentation — `tools/image-generation` (mirror `inbox/openclaw_docs/tools/image-generation.md`), Supported providers / Provider capabilities / Provider deep dives sections
**Last Updated**: 2026-06-22
**Status**: Active
