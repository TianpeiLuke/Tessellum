---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - video_generation
keywords:
  - openclaw runway provider
  - runway video generation
  - runwayml api secret
  - runway gen4.5 default video model
  - videoGenerationProviders contract
  - runway mode allowlist
  - text-to-video image-to-video video-to-video
  - runway task polling
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/runway
access_control_group: ["general"]
---

# OpenClaw — Configuring the Runway Video-Generation Provider

## Overview

This note is the setup procedure for the bundled OpenClaw `runway` video-generation provider, mirroring the `providers/runway` source page. The `runway` plugin ships bundled and is enabled by default (`enabledByDefault: true`), registering the `runway` provider against the `videoGenerationProviders` contract, so the steps below are about authenticating and selecting it rather than installing it. The note covers the provider's identity table, the three-step getting-started flow (set the API key, make Runway the default video provider, generate), the seven models split across text-to-video / image-to-video / video-to-video modes with their per-mode allowlist validation and aspect-ratio limits, the `json5` default-video-model configuration, and the advanced-configuration details (environment-variable aliases and task-based polling).

## Provider identity

The page's header table fixes the provider's identity and entry points verbatim:

| Property        | Value                                                             |
| --------------- | ----------------------------------------------------------------- |
| Provider id     | `runway`                                                          |
| Plugin          | bundled, `enabledByDefault: true`                                 |
| Auth env vars   | `RUNWAYML_API_SECRET` (canonical) or `RUNWAY_API_KEY`             |
| Onboarding flag | `--auth-choice runway-api-key`                                    |
| Direct CLI flag | `--runway-api-key <key>`                                          |
| API             | Runway task-based video generation (`GET /v1/tasks/{id}` polling) |
| Default model   | `runway/gen4.5`                                                   |

## Getting started

Because the plugin is bundled and enabled by default there is no install step; setup is the three `<Steps>` from the source page. First, set the API key by running the onboarding wizard with the Runway auth choice:

```bash
openclaw onboard --auth-choice runway-api-key
```

Second, make Runway the default video provider by setting the primary video-generation model:

```bash
openclaw config set agents.defaults.videoGenerationModel.primary "runway/gen4.5"
```

Third, generate a video — the source states: "Ask the agent to generate a video. Runway will be used automatically." (i.e., once it is the default video provider, no explicit provider selection is required at call time).

## Supported modes and models

The provider exposes seven Runway models split across three modes. The same model id can serve more than one mode — for example `gen4.5` works for both text-to-video and image-to-video. The per-mode model lists and their reference inputs are:

| Mode           | Models                                                                 | Reference input         |
| -------------- | ---------------------------------------------------------------------- | ----------------------- |
| Text-to-video  | `gen4.5` (default), `veo3.1`, `veo3.1_fast`, `veo3`                    | None                    |
| Image-to-video | `gen4.5`, `gen4_turbo`, `gen3a_turbo`, `veo3.1`, `veo3.1_fast`, `veo3` | 1 local or remote image |
| Video-to-video | `gen4_aleph`                                                           | 1 local or remote video |

Local image and video references are supported via data URIs.

### Aspect ratios

Allowed aspect ratios differ by mode:

| Aspect ratios         | Allowed values                              |
| --------------------- | ------------------------------------------- |
| Text-to-video         | `16:9`, `9:16`                              |
| Image and video edits | `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `21:9` |

### Mode-allowlist validation

Video-to-video currently requires `runway/gen4_aleph` (a `<Warning>` on the source page); other Runway model ids reject video reference inputs. Picking a Runway model id from the wrong column produces an explicit error before the API request leaves OpenClaw: the provider validates `model` against the mode's allowlist (`TEXT_ONLY_MODELS`, `IMAGE_MODELS`, `VIDEO_MODELS`) in `extensions/runway/video-generation-provider.ts`.

## Configuration

The default video model is configured under `agents.defaults.videoGenerationModel` (the `json5` form equivalent to the `config set` command above):

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "runway/gen4.5",
      },
    },
  },
}
```

## Advanced configuration

The source page's `<AccordionGroup>` documents two advanced details. For environment-variable aliases, OpenClaw recognizes both `RUNWAYML_API_SECRET` (canonical) and `RUNWAY_API_KEY`; either variable will authenticate the Runway provider. For task polling, Runway uses a task-based API: after submitting a generation request, OpenClaw polls `GET /v1/tasks/{id}` until the video is ready, and no additional configuration is needed for the polling behavior.

The source page's `## Related` card group links out to the shared **Video generation** tool reference (`/tools/video-generation`, for shared tool parameters, provider selection, and async behavior) and to the **Configuration reference** (`/gateway/config-agents#agent-defaults`, for agent default settings including the video-generation model); both are surfaced under Docs in Related Notes below.

**Source**: OpenClaw documentation — `providers/runway` (mirror `inbox/openclaw_docs/providers/runway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
