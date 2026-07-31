---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - video_generation
keywords:
  - openclaw alibaba provider
  - alibaba model studio dashscope
  - wan video generation
  - modelstudio_api_key dashscope_api_key qwen_api_key
  - videoGenerationModel primary
  - alibaba wan2.6-t2v default
  - dashscope base url override
  - qwen plugin overlapping auth
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/alibaba
access_control_group: ["general"]
---

# OpenClaw — Configuring the Alibaba Model Studio (Wan) Video Provider

## Overview

This note is the procedure for configuring OpenClaw's bundled `alibaba` provider plugin, which registers a video-generation provider for Wan models on Alibaba Model Studio (the international name for DashScope). It mirrors the `providers/alibaba` source page: the provider property table, setting an API key, selecting the default video model, verifying the provider, the five built-in Wan model refs, the per-mode capability/limit table, and the advanced-configuration knobs (base-URL override, auth env-var priority, and the relationship to the Qwen plugin). The plugin ships `enabledByDefault: true`, so the only required step is supplying an API key.

## Provider Properties

The bundled `alibaba` plugin registers a Wan video-generation provider against Alibaba Model Studio / DashScope. Its key properties, copied from the source page's property table, are:

| Property | Value |
| --- | --- |
| Provider id | `alibaba` |
| Plugin | bundled, `enabledByDefault: true` |
| Auth env vars | `MODELSTUDIO_API_KEY` → `DASHSCOPE_API_KEY` → `QWEN_API_KEY` (first match wins) |
| Onboarding flag | `--auth-choice alibaba-model-studio-api-key` |
| Direct CLI flag | `--alibaba-model-studio-api-key <key>` |
| Default model | `alibaba/wan2.6-t2v` |
| Default base URL | `https://dashscope-intl.aliyuncs.com` |

Because the plugin is enabled by default, you only need to set an API key to make the provider usable.

## Getting started

### Step 1 — Set an API key

Use onboarding to store the key against the `alibaba` provider, pass the key directly during install/onboarding, or export one of the accepted env vars before starting the Gateway. The three accepted env vars are resolved in priority order `MODELSTUDIO_API_KEY` → `DASHSCOPE_API_KEY` → `QWEN_API_KEY` (first non-empty match wins).

```bash
# Onboarding: store the key against the alibaba provider
openclaw onboard --auth-choice alibaba-model-studio-api-key

# Or pass the key directly during install/onboarding
openclaw onboard --alibaba-model-studio-api-key <your-key>

# Or export any accepted env var before starting the Gateway
export MODELSTUDIO_API_KEY=sk-...
# or DASHSCOPE_API_KEY=...
# or QWEN_API_KEY=...
```

### Step 2 — Set a default video model

Configure the agent default `videoGenerationModel.primary` to a Wan model ref (the default is `alibaba/wan2.6-t2v`):

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "alibaba/wan2.6-t2v",
      },
    },
  },
}
```

### Step 3 — Verify the provider is configured

List the provider's models; the list should include all five bundled Wan models:

```bash
openclaw models list --provider alibaba
```

If `MODELSTUDIO_API_KEY` is unresolved, `openclaw models status --json` reports the missing credential under `auth.unusableProfiles`.

Note that the Alibaba plugin and the Qwen plugin both authenticate against DashScope and accept overlapping env vars: use `alibaba/...` model ids to drive the dedicated Wan video surface, and use `qwen/...` ids when you want Qwen's chat, embedding, or media-understanding surface.

## Built-in Wan models

The provider registers five built-in Wan model refs (each prefixed `alibaba/`), spanning text-, image-, and reference-to-video modes:

| Model ref | Mode |
| --- | --- |
| `alibaba/wan2.6-t2v` | Text-to-video (default) |
| `alibaba/wan2.6-i2v` | Image-to-video |
| `alibaba/wan2.6-r2v` | Reference-to-video |
| `alibaba/wan2.6-r2v-flash` | Reference-to-video (fast) |
| `alibaba/wan2.7-r2v` | Reference-to-video |

## Capabilities and limits

The bundled provider mirrors DashScope's Wan video API caps. All three modes share the same per-request video count and duration cap; only the input shape differs:

| Mode | Max output videos | Max input images | Max input videos | Max duration | Supported controls |
| --- | --- | --- | --- | --- | --- |
| Text-to-video | 1 | n/a | n/a | 10 s | `size`, `aspectRatio`, `resolution`, `audio`, `watermark` |
| Image-to-video | 1 | 1 | n/a | 10 s | `size`, `aspectRatio`, `resolution`, `audio`, `watermark` |
| Reference-to-video | 1 | n/a | 4 | 10 s | `size`, `aspectRatio`, `resolution`, `audio`, `watermark` |

When a request omits `durationSeconds`, the provider sends DashScope's accepted default of **5 seconds**. Set `durationSeconds` explicitly on the video generation tool to extend up to 10 s. Reference image and video inputs must be remote `http(s)` URLs — local file paths are not accepted by DashScope's reference modes, so upload to object storage first or use the media-tool flow that already produces a public URL.

## Advanced configuration

### Override the DashScope base URL

The provider defaults to the international DashScope endpoint (`https://dashscope-intl.aliyuncs.com`). To target the China-region endpoint, set `models.providers.alibaba.baseUrl`. The provider strips trailing slashes before constructing AIGC task URLs.

```json5
{
  models: {
    providers: {
      alibaba: {
        baseUrl: "https://dashscope.aliyuncs.com",
      },
    },
  },
}
```

### Auth env priority

OpenClaw resolves the Alibaba API key from environment variables in this order, taking the first non-empty value: (1) `MODELSTUDIO_API_KEY`, (2) `DASHSCOPE_API_KEY`, (3) `QWEN_API_KEY`. Configured `auth.profiles` entries (set via `openclaw models auth login`) override env-var resolution; see the Auth profiles entry in the models FAQ for profile rotation, cooldown, and override mechanics.

### Relationship to the Qwen plugin

Both bundled plugins talk to DashScope and accept overlapping API keys. Use `alibaba/wan*.*` ids to drive the dedicated Wan video provider documented on this page, and use `qwen/*` ids for Qwen chat, embedding, and media understanding. Setting `MODELSTUDIO_API_KEY` once authenticates both plugins because the auth env-var list intentionally overlaps; you do not need to onboard each plugin separately.

**Source**: OpenClaw documentation — `providers/alibaba` (mirror `inbox/openclaw_docs/providers/alibaba.md`)
**Last Updated**: 2026-06-22
**Status**: Active
