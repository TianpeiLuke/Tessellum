---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - zai
keywords:
  - openclaw zai provider
  - zai glm models
  - ZAI_API_KEY bearer auth
  - zai endpoint auto-detect
  - zai coding plan regional onboarding
  - glm-5.2 forward resolution
  - preserved thinking reasoning_content
  - tool_stream tool-call streaming
  - glm-4.6v image understanding
topics:
  - OpenClaw
  - Providers
  - Z.AI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/zai
access_control_group: ["general"]
---

# OpenClaw — Configuring the Z.AI (GLM) Provider

## Overview

This note is the setup procedure for the bundled `zai` provider in OpenClaw — the integration for **Z.AI**, the API platform for the **GLM** model family. It mirrors the `providers/zai` source page: the provider header table, what "GLM models" means as a ref, the two onboarding paths (auto-detect endpoint vs explicit regional Coding-Plan/general choices), the config-file example, the manifest-backed built-in GLM catalog, and the advanced-configuration accordions (GLM-5 forward-resolution, `tool_stream` tool-call streaming, `/think`-driven thinking and preserved thinking, `glm-4.6v` image understanding, and Bearer auth details). Z.AI provides REST APIs for GLM and uses API keys for authentication; OpenClaw drives it through the `zai` provider with a Z.AI API key created in the Z.AI console.

## Provider Summary

The `zai` provider is configured with a single API key and Bearer authentication against the Z.AI Chat Completions API:

| Property | Value |
| -------- | -------------------------------------------- |
| Provider | `zai` |
| Auth | `ZAI_API_KEY` (legacy alias: `Z_AI_API_KEY`) |
| API | Z.AI Chat Completions (Bearer auth) |

**GLM models** are a model *family*, not a separate provider. In OpenClaw, GLM models use refs such as `zai/glm-5.2` — provider `zai`, model id `glm-5.2`. Every GLM model is therefore reachable as `zai/<model>` (for example, `zai/glm-5`).

## Getting Started

OpenClaw offers two onboarding paths, selected by the `--auth-choice` passed to `openclaw onboard`. After either path, verify the provider is registered with the read-only model listing.

### Path A — Auto-detect endpoint (recommended for most users)

OpenClaw probes the supported Z.AI endpoints with your API key and applies the correct base URL automatically:

```bash
openclaw onboard --auth-choice zai-api-key
openclaw models list --all --provider zai
```

The `zai-api-key` choice lets OpenClaw detect the matching Z.AI endpoint from the key and apply the correct base URL automatically.

### Path B — Explicit regional endpoint

Use the explicit regional choices when you want to *force* a specific Coding Plan or general API surface rather than relying on auto-detection. Pick the onboarding choice for your plan and region, then verify:

```bash
# Coding Plan Global (recommended for Coding Plan users)
openclaw onboard --auth-choice zai-coding-global

# Coding Plan CN (China region)
openclaw onboard --auth-choice zai-coding-cn

# General API
openclaw onboard --auth-choice zai-global

# General API CN (China region)
openclaw onboard --auth-choice zai-cn
```

The four explicit choices are `zai-coding-global`, `zai-coding-cn`, `zai-global`, and `zai-cn`. After onboarding, run `openclaw models list --all --provider zai` to confirm the GLM rows are listed.

## Config Example

Instead of (or in addition to) onboarding, the provider can be configured directly in the OpenClaw config file. The `env.ZAI_API_KEY` carries the key, `models.providers.zai.baseUrl` pins an explicit endpoint, and `agents.defaults.model.primary` sets the default model ref:

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  models: {
    providers: {
      zai: {
        // GLM-5.2 uses the Coding Plan endpoint.
        baseUrl: "https://api.z.ai/api/coding/paas/v4",
      },
    },
  },
  agents: { defaults: { model: { primary: "zai/glm-5.2" } } },
}
```

## Built-in Catalog

OpenClaw ships the bundled `zai` provider catalog in the **plugin manifest**, so read-only listing can show known GLM rows without loading the provider runtime — `openclaw models list --all --provider zai` returns the manifest-backed catalog. The catalog currently includes:

| Model ref | Notes |
| -------------------- | ------------------------------- |
| `zai/glm-5.2` | Coding Plan default; 1M context |
| `zai/glm-5.1` | General API default |
| `zai/glm-5` | |
| `zai/glm-5-turbo` | |
| `zai/glm-5v-turbo` | |
| `zai/glm-4.7` | |
| `zai/glm-4.7-flash` | |
| `zai/glm-4.7-flashx` | |
| `zai/glm-4.6` | |
| `zai/glm-4.6v` | |
| `zai/glm-4.5` | |
| `zai/glm-4.5-air` | |
| `zai/glm-4.5-flash` | |
| `zai/glm-4.5v` | |

Default-model behavior depends on the plan: Coding Plan setup defaults to `zai/glm-5.2`, while general API setup keeps `zai/glm-5.1`. Endpoint auto-detection falls back to `glm-5.1` or `glm-4.7` when the selected plan does not expose GLM-5.2. GLM-5.2 also supports `off`, `low`, `high`, and `max` thinking levels — OpenClaw maps `low` and `high` to Z.AI **high** reasoning effort and `max` to **max** effort. GLM versions and availability can change, so re-run `openclaw models list --all --provider zai` to see the catalog known to your installed version.

## Advanced Configuration

**Forward-resolving unknown GLM-5 models.** Unknown `glm-5*` ids still forward-resolve on the bundled provider path by synthesizing provider-owned metadata from the `glm-4.7` template when the id matches the current GLM-5 family shape.

**Tool-call streaming.** `tool_stream` is enabled by default for Z.AI tool-call streaming. To disable it per model, set `params.tool_stream: false`:

```json5
{
  agents: {
    defaults: {
      models: {
        "zai/<model>": {
          params: { tool_stream: false },
        },
      },
    },
  },
}
```

**Thinking and preserved thinking.** Z.AI thinking follows OpenClaw's `/think` controls. With thinking off, OpenClaw sends `thinking: { type: "disabled" }` to avoid responses that spend the output budget on `reasoning_content` before visible text. Preserved thinking is opt-in because Z.AI requires the full historical `reasoning_content` to be replayed, which increases prompt tokens; enable it per model with `params.preserveThinking: true`:

```json5
{
  agents: {
    defaults: {
      models: {
        "zai/glm-5.2": {
          params: { preserveThinking: true },
        },
      },
    },
  },
}
```

When preserved thinking is enabled and thinking is on, OpenClaw sends `thinking: { type: "enabled", clear_thinking: false }` and replays prior `reasoning_content` for the same OpenAI-compatible transcript. Advanced users can still override the exact provider payload with `params.extra_body.thinking`.

**Image understanding.** The bundled Z.AI plugin registers image understanding via model `glm-4.6v`. Image understanding is auto-resolved from the configured Z.AI auth — no additional config is needed.

**Auth details.** Z.AI uses Bearer auth with your API key. The `zai-api-key` onboarding choice auto-detects the matching Z.AI endpoint by probing supported endpoints with your key, while the explicit regional choices (`zai-coding-global`, `zai-coding-cn`, `zai-global`, `zai-cn`) force a specific API surface. The legacy env var `Z_AI_API_KEY` is still accepted: OpenClaw copies it to `ZAI_API_KEY` at startup if `ZAI_API_KEY` is unset.

**Source**: OpenClaw documentation — `providers/zai` (mirror `inbox/openclaw_docs/providers/zai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
