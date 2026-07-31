---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - video_generation
keywords:
  - openclaw pixverse provider
  - pixverse video generation setup
  - PIXVERSE_API_KEY
  - pixverse/v6 default video model
  - text-to-video image-to-video
  - videoGenerationProviders contract
  - pixverse region international cn
  - video_id task polling
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/pixverse
access_control_group: ["general"]
---

# OpenClaw — Setting Up the PixVerse Video-Generation Provider

## Overview

This note is the setup procedure for OpenClaw's `pixverse` external video-generation provider, mirroring the `providers/pixverse` source page. OpenClaw ships `pixverse` as an official external plugin for hosted PixVerse video generation; the plugin registers the `pixverse` provider against the `videoGenerationProviders` contract. The note walks through install/enable, setting the `PIXVERSE_API_KEY`, choosing the International or CN region, making `pixverse/v6` the default video model, and then covers the supported text/image-to-video modes and output options, provider-specific option keys, the JSON5 default-model config, and the advanced region/baseUrl/task-polling behavior.

## Provider Reference (header table)

The source page opens with a property table identifying the provider. Reproduced verbatim:

| Property           | Value                                                                |
| ------------------ | -------------------------------------------------------------------- |
| Provider id        | `pixverse`                                                           |
| Plugin package     | `@openclaw/pixverse-provider`                                        |
| Auth env var       | `PIXVERSE_API_KEY`                                                   |
| Onboarding flag    | `--auth-choice pixverse-api-key`                                     |
| Direct CLI flag    | `--pixverse-api-key <key>`                                           |
| API                | PixVerse Platform API v2 (`video_id` submission plus result polling) |
| Default model      | `pixverse/v6`                                                        |
| Default API region | International                                                        |

## Getting started

The source page documents a four-step `<Steps>` flow:

1. **Install the plugin** — install from ClawHub and restart the gateway:

```bash
openclaw plugins install clawhub:@openclaw/pixverse-provider
openclaw gateway restart
```

2. **Set the API key** — run the onboarding wizard with the PixVerse auth choice:

```bash
openclaw onboard --auth-choice pixverse-api-key
```

The wizard asks whether to use the International endpoint (`https://app-api.pixverse.ai/openapi/v2`) or the CN endpoint (`https://app-api.pixverseai.cn/openapi/v2`) before writing `region` and `baseUrl` into the provider config.

3. **Set PixVerse as the default video provider** — point the agent default video model at `pixverse/v6`:

```bash
openclaw config set agents.defaults.videoGenerationModel.primary "pixverse/v6"
```

4. **Generate a video** — ask the agent to generate a video; PixVerse will be used automatically.

## Supported modes and models

The provider exposes PixVerse generation models through OpenClaw's shared video tool. Two generation modes are supported:

| Mode           | Models               | Reference input         |
| -------------- | -------------------- | ----------------------- |
| Text-to-video  | `v6` (default), `c1` | None                    |
| Image-to-video | `v6` (default), `c1` | 1 local or remote image |

Local image references are uploaded to PixVerse before the image-to-video request. Remote image URLs are passed through the PixVerse image upload endpoint as `image_url`.

Output options exposed to the shared video tool:

| Option          | Supported values                                                            |
| --------------- | --------------------------------------------------------------------------- |
| Duration        | 1-15 seconds                                                                |
| Resolution      | `360P`, `540P`, `720P`, `1080P`                                             |
| Aspect ratio    | `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `2:3`, `3:2`, `21:9` for text-to-video |
| Generated audio | `audio: true`                                                               |

The source adds a note that PixVerse image template generation is not exposed through `image_generate` yet — that API is template-id driven, while OpenClaw's shared image-generation contract does not currently have a PixVerse-specific typed option bag.

## Provider options

The video provider accepts these optional provider-specific keys (each with its alias form, per the source):

| Option                               | Type   | Effect                            |
| ------------------------------------ | ------ | --------------------------------- |
| `seed`                               | number | Deterministic seed when supported |
| `negativePrompt` / `negative_prompt` | string | Negative prompt                   |
| `quality`                            | string | PixVerse quality such as `720p`   |
| `motionMode` / `motion_mode`         | string | Image-to-video motion mode        |
| `cameraMovement` / `camera_movement` | string | PixVerse camera movement preset   |
| `templateId` / `template_id`         | number | Activated PixVerse template id    |

## Configuration

The minimal config to make PixVerse the default video model (JSON5, verbatim from source):

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "pixverse/v6",
      },
    },
  },
}
```

## Advanced configuration

The source page nests three `<Accordion>` items under Advanced configuration.

**API region.** OpenClaw defaults to the international PixVerse API. Set `models.providers.pixverse.region` manually when your key belongs to a specific PixVerse platform region, or use `openclaw onboard --auth-choice pixverse-api-key` to choose one in the setup wizard. The region-to-base-URL mapping is:

| Region value    | PixVerse API base URL                         |
| --------------- | --------------------------------------------- |
| `international` | `https://app-api.pixverse.ai/openapi/v2`      |
| `cn`            | `https://app-api.pixverseai.cn/openapi/v2`    |

A region/baseUrl override example (JSON5, verbatim from source):

```json5
{
  models: {
    providers: {
      pixverse: {
        region: "cn", // "international" or "cn"
        baseUrl: "https://app-api.pixverseai.cn/openapi/v2",
        models: [],
      },
    },
  },
}
```

**Custom base URL.** Set `models.providers.pixverse.baseUrl` only when routing through a trusted compatible proxy. `baseUrl` takes precedence over `region`.

**Task polling.** PixVerse returns a `video_id` from the generation request. OpenClaw polls `/openapi/v2/video/result/{video_id}` until the task succeeds, fails, or times out.

The page's `## Related` card group links out to the shared video tool (`/tools/video-generation`) and the agent-defaults configuration reference (`/gateway/config-agents#agent-defaults`) — captured as Related Notes / References below, not duplicated here.

**Source**: OpenClaw documentation — `providers/pixverse` (mirror `inbox/openclaw_docs/providers/pixverse.md`)
**Last Updated**: 2026-06-22
**Status**: Active
