---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - comfy
keywords:
  - openclaw comfy provider
  - comfyui workflow image generation
  - comfy cloud setup
  - comfy/workflow model
  - workflowPath promptNodeId outputNodeId
  - COMFY_API_KEY COMFY_CLOUD_API_KEY
  - image video music generate
  - reference image editing inputImageNodeId
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/comfy
access_control_group: ["general"]
---

# OpenClaw — Configuring the `comfy` Workflow Provider (Image / Video / Music)

## Overview

This note is the setup procedure for the bundled OpenClaw `comfy` provider — a workflow-driven ComfyUI integration that drives image, video, and music/audio generation from ComfyUI workflow JSON files. It mirrors the `providers/comfy` source page: the provider properties, what it supports, the two `Getting started` paths (Local and Comfy Cloud), the `Configuration` block with its shared and per-capability keys, and the `Workflow details` accordions (image / video / music / backward-compatibility / live tests). Because the plugin is entirely workflow-driven, OpenClaw does NOT map generic `size`, `aspectRatio`, `resolution`, `durationSeconds`, or TTS-style controls onto your graph — every shape/length/quality decision lives inside the ComfyUI workflow JSON you supply.

## Provider Properties

The bundled `comfy` plugin registers one model across three media surfaces.

| Property | Detail |
| --- | --- |
| Provider | `comfy` |
| Models | `comfy/workflow` |
| Shared surfaces | `image_generate`, `video_generate`, `music_generate` |
| Auth | None for local ComfyUI; `COMFY_API_KEY` or `COMFY_CLOUD_API_KEY` for Comfy Cloud |
| API | ComfyUI `/prompt` / `/history` / `/view` and Comfy Cloud `/api/*` |

## What It Supports

- Image generation from a workflow JSON.
- Image editing with 1 uploaded reference image.
- Video generation from a workflow JSON.
- Video generation with 1 uploaded reference image.
- Music or audio generation through the shared `music_generate` tool.
- Output download from a configured node or all matching output nodes.

## Getting Started

Choose between running ComfyUI on your own machine (Local) or using Comfy Cloud.

### Local mode

Best for running your own ComfyUI instance on your machine or LAN. The steps are: (1) start your local ComfyUI instance (defaults to `http://127.0.0.1:8188`); (2) export or create a ComfyUI workflow JSON file and note the node IDs for the prompt input node and the output node you want OpenClaw to read from; (3) set `mode: "local"` and point at your workflow file; (4) set the default model to `comfy/workflow` for the capability you configured; (5) verify with the CLI. The minimal local image configuration:

```json5
{
  plugins: {
    entries: {
      comfy: {
        config: {
          mode: "local",
          baseUrl: "http://127.0.0.1:8188",
          image: {
            workflowPath: "./workflows/flux-api.json",
            promptNodeId: "6",
            outputNodeId: "9",
          },
        },
      },
    },
  },
}
```

### Comfy Cloud mode

Best for running workflows on Comfy Cloud without managing local GPU resources. The steps are: (1) sign up at `comfy.org` and generate an API key from your account dashboard; (2) provide the key (preferred env var `COMFY_API_KEY`, alternative `COMFY_CLOUD_API_KEY`, or inline via `openclaw config set plugins.entries.comfy.config.apiKey "your-key"`); (3) prepare the workflow JSON and note the prompt/output node IDs; (4) set `mode: "cloud"` and point at the workflow file; (5) set the default model; (6) verify. Cloud mode defaults `baseUrl` to `https://cloud.comfy.org` — you only need to set `baseUrl` if you use a custom cloud endpoint. Set the API key by any of:

```bash
# Environment variable (preferred)
export COMFY_API_KEY="your-key"

# Alternative environment variable
export COMFY_CLOUD_API_KEY="your-key"

# Or inline in config
openclaw config set plugins.entries.comfy.config.apiKey "your-key"
```

### Set the default model and verify

For both modes, point OpenClaw at the `comfy/workflow` model for the capability you configured (e.g. `agents.defaults.imageGenerationModel.primary: "comfy/workflow"`; see the Workflow details accordions below for the per-capability keys) and then verify the provider is registered:

```bash
openclaw models list --provider comfy
```

## Configuration

Comfy supports shared top-level connection settings plus per-capability workflow sections (`image`, `video`, `music`). A full config wiring all three capabilities in local mode:

```json5
{
  plugins: {
    entries: {
      comfy: {
        config: {
          mode: "local",
          baseUrl: "http://127.0.0.1:8188",
          image: {
            workflowPath: "./workflows/flux-api.json",
            promptNodeId: "6",
            outputNodeId: "9",
          },
          video: {
            workflowPath: "./workflows/video-api.json",
            promptNodeId: "12",
            outputNodeId: "21",
          },
          music: {
            workflowPath: "./workflows/music-api.json",
            promptNodeId: "3",
            outputNodeId: "18",
          },
        },
      },
    },
  },
}
```

### Shared keys

These keys live at the top level of `plugins.entries.comfy.config`.

| Key | Type | Description |
| --- | --- | --- |
| `mode` | `"local"` or `"cloud"` | Connection mode. |
| `baseUrl` | string | Defaults to `http://127.0.0.1:8188` for local or `https://cloud.comfy.org` for cloud. |
| `apiKey` | string | Optional inline key, alternative to `COMFY_API_KEY` / `COMFY_CLOUD_API_KEY` env vars. |
| `allowPrivateNetwork` | boolean | Allow a private/LAN `baseUrl` in cloud mode. |

### Per-capability keys

These keys apply inside the `image`, `video`, or `music` sections.

| Key | Required | Default | Description |
| --- | --- | --- | --- |
| `workflow` or `workflowPath` | Yes | -- | Path to the ComfyUI workflow JSON file. |
| `promptNodeId` | Yes | -- | Node ID that receives the text prompt. |
| `promptInputName` | No | `"text"` | Input name on the prompt node. |
| `outputNodeId` | No | -- | Node ID to read output from. If omitted, all matching output nodes are used. |
| `pollIntervalMs` | No | -- | Polling interval in milliseconds for job completion. |
| `timeoutMs` | No | -- | Timeout in milliseconds for the workflow run. |

The `image` and `video` sections also support reference-image input keys:

| Key | Required | Default | Description |
| --- | --- | --- | --- |
| `inputImageNodeId` | Yes (when passing a reference image) | -- | Node ID that receives the uploaded reference image. |
| `inputImageInputName` | No | `"image"` | Input name on the image node. |

## Workflow Details

**Image workflows** — set `agents.defaults.imageGenerationModel.primary: "comfy/workflow"`. To enable image editing with an uploaded reference image, add `inputImageNodeId` (and optionally `inputImageInputName`, default `"image"`) to your image config so the reference image is routed into the named input of that node:

```json5
{
  plugins: {
    entries: {
      comfy: {
        config: {
          image: {
            workflowPath: "./workflows/edit-api.json",
            promptNodeId: "6",
            inputImageNodeId: "7",
            inputImageInputName: "image",
            outputNodeId: "9",
          },
        },
      },
    },
  },
}
```

**Video workflows** — set `agents.defaults.videoGenerationModel.primary: "comfy/workflow"`. Comfy video workflows support text-to-video and image-to-video through the configured graph. OpenClaw does NOT pass input videos into Comfy workflows: only text prompts and single reference images are supported as inputs.

**Music workflows** — the bundled plugin registers a music-generation provider for workflow-defined audio or music outputs, surfaced through the shared `music_generate` tool (e.g. `/tool music_generate prompt="Warm ambient synth loop with soft tape texture"`). Use the `music` config section to point at your audio workflow JSON and output node.

**Backward compatibility** — existing top-level image config (`workflowPath` / `promptNodeId` / `outputNodeId` placed directly in `config`, without the nested `image` section) still works; OpenClaw treats that legacy flat shape as the image workflow config. You do not need to migrate immediately, but the nested `image` / `video` / `music` sections are recommended for new setups. If you only use image generation, the legacy flat config and the new nested `image` section are functionally equivalent.

**Live tests** — opt-in live coverage exists for the bundled plugin: `OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts`. The live test skips individual image, video, or music cases unless the matching Comfy workflow section is configured.

**Source**: OpenClaw documentation — `providers/comfy` (mirror `inbox/openclaw_docs/providers/comfy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
