---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - music_generation
keywords:
  - music_generate tool
  - openclaw music generation
  - musicGenerationModel primary fallbacks
  - comfyui fal google lyria minimax openrouter
  - background task music lifecycle
  - provider selection order failover
  - generate edit capability modes
topics:
  - OpenClaw
  - Music Generation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/music-generation
access_control_group: ["general"]
---

# OpenClaw — Generating Music with the `music_generate` Tool

## Overview

This note is the end-to-end procedure for generating music or audio in OpenClaw through the shared `music_generate` tool, mirroring the `tools/music-generation` source page. It covers the two quick-start paths (shared provider-backed and ComfyUI workflow), the supported-provider table and `generate`/`edit` capability matrix, the full tool-parameter set, the session-backed background-task async model and its four-state task lifecycle, model-selection + provider-selection-order configuration with automatic failover, per-provider notes, when to pick each path, the explicit provider capability-mode contract, and the opt-in live-test invocations. The tool exists only when at least one music-generation provider is available — ComfyUI, fal, Google, MiniMax, and OpenRouter today.

## Quick start

There are two configured paths. For the **shared provider-backed** path: (1) set an API key for at least one provider — for example `GEMINI_API_KEY` or `MINIMAX_API_KEY`; (2) optionally pick a default model under `agents.defaults.musicGenerationModel`; (3) ask the agent (e.g. _"Generate an upbeat synthpop track about a night drive through a neon city."_) — the agent calls `music_generate` automatically, with no tool allow-listing needed. The optional default-model config block is:

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "google/lyria-3-clip-preview",
      },
    },
  },
}
```

For the **ComfyUI workflow** path: (1) configure `plugins.entries.comfy.config.music` with a workflow JSON and prompt/output nodes; (2) for Comfy Cloud, optionally set `COMFY_API_KEY` or `COMFY_CLOUD_API_KEY`; (3) call the tool directly, for example `/tool music_generate prompt="Warm ambient synth loop with soft tape texture"`. For direct synchronous contexts without a session-backed agent run, the built-in tool still falls back to inline generation and returns the final media path in the tool result. Example natural-language prompts the source gives include "Generate a cinematic piano track with soft strings and no vocals." and "Generate an energetic chiptune loop about launching a rocket at sunrise."

## Supported providers

The five configured providers, their default models, reference-image limits, supported controls, and auth:

| Provider   | Default model                | Reference inputs | Supported controls                                    | Auth                                   |
| ---------- | ---------------------------- | ---------------- | ----------------------------------------------------- | -------------------------------------- |
| ComfyUI    | `workflow`                   | Up to 1 image    | Workflow-defined music or audio                       | `COMFY_API_KEY`, `COMFY_CLOUD_API_KEY` |
| fal        | `fal-ai/minimax-music/v2.6`  | None             | `lyrics`, `instrumental`, `durationSeconds`, `format` | `FAL_KEY` or `FAL_API_KEY`             |
| Google     | `lyria-3-clip-preview`       | Up to 10 images  | `lyrics`, `instrumental`, `format`                    | `GEMINI_API_KEY`, `GOOGLE_API_KEY`     |
| MiniMax    | `music-2.6`                  | None             | `lyrics`, `instrumental`, `format=mp3`                | `MINIMAX_API_KEY` or MiniMax OAuth     |
| OpenRouter | `google/lyria-3-pro-preview` | Up to 1 image    | `lyrics`, `instrumental`, `durationSeconds`, `format` | `OPENROUTER_API_KEY`                   |

### Capability matrix

The explicit mode contract used by `music_generate`, contract tests, and the shared live sweep:

| Provider   | `generate` | `edit` | Edit limit | Shared live lanes                                                         |
| ---------- | :--------: | :----: | ---------- | ------------------------------------------------------------------------- |
| ComfyUI    |     ✓      |   ✓    | 1 image    | Not in the shared sweep; covered by `extensions/comfy/comfy.live.test.ts` |
| fal        |     ✓      |   —    | None       | `generate`                                                                |
| Google     |     ✓      |   ✓    | 10 images  | `generate`, `edit`                                                        |
| MiniMax    |     ✓      |   —    | None       | `generate`                                                                |
| OpenRouter |     ✓      |   ✓    | 1 image    | `generate`, `edit`                                                        |

Use `action: "list"` to inspect available shared providers and models at runtime (`/tool music_generate action=list`), and `action: "status"` to inspect the active session-backed music task (`/tool music_generate action=status`). A direct generation example is `/tool music_generate prompt="Dreamy lo-fi hip hop with vinyl texture and gentle rain" instrumental=true`.

## Tool parameters

The `music_generate` tool accepts the following parameters (verbatim from the source `ParamField` declarations):

- `prompt` (`string`, required) — music generation prompt; required for `action: "generate"`.
- `action` (`"generate" | "status" | "list"`, default `"generate"`) — `"status"` returns the current session task; `"list"` inspects providers.
- `model` (`string`) — provider/model override (e.g. `google/lyria-3-pro-preview`, `comfy/workflow`).
- `lyrics` (`string`) — optional lyrics when the provider supports explicit lyric input.
- `instrumental` (`boolean`) — request instrumental-only output when the provider supports it.
- `image` (`string`) — single reference image path or URL.
- `images` (`string[]`) — multiple reference images (up to 10 on supporting providers).
- `durationSeconds` (`number`) — target duration in seconds when the provider supports duration hints.
- `format` (`"mp3" | "wav"`) — output format hint when the provider supports it.
- `filename` (`string`) — output filename hint.

Not all providers support all parameters. OpenClaw still validates hard limits such as input counts before submission. When a provider supports duration but uses a shorter maximum than the requested value, OpenClaw clamps to the closest supported duration. Truly unsupported optional hints are ignored with a warning when the selected provider or model cannot honor them. Tool results report applied settings, and `details.normalization` captures any requested-to-applied mapping. Provider request timeouts are operator configuration only: OpenClaw uses `agents.defaults.musicGenerationModel.timeoutMs` when configured, raises values below 120000ms to 120000ms, and otherwise defaults provider requests to 300000ms.

## Async behavior

Session-backed music generation runs as a background task. The behaviors are: **Background task** — `music_generate` creates a background task, returns a started/task response immediately, and posts the finished track later in a follow-up agent message; **Duplicate prevention** — while a task is `queued` or `running`, later `music_generate` calls in the same session return task status instead of starting another generation (use `action: "status"` to check explicitly); **Status lookup** — `openclaw tasks list` or `openclaw tasks show <taskId>` inspects queued, running, and terminal status; **Completion wake** — OpenClaw injects an internal completion event back into the same session so the model can write the user-facing follow-up itself; **Prompt hint** — later user/manual turns in the same session get a small runtime hint when a music task is already in flight, so the model does not blindly call `music_generate` again; **No-session fallback** — direct/local contexts without a real agent session run inline and return the final audio result in the same turn. (As stated in the page intro, if the requester session is inactive or its active wake fails and some generated audio is still missing from the completion reply, OpenClaw sends an idempotent direct fallback with only the missing audio.)

### Task lifecycle

| State       | Meaning                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------- |
| `queued`    | Task created, waiting for the provider to accept it.                                           |
| `running`   | Provider is processing (typically 30 seconds to 3 minutes depending on provider and duration). |
| `succeeded` | Track ready; the agent wakes and posts it to the conversation.                                 |
| `failed`    | Provider error or timeout; the agent wakes with error details.                                 |

Status can be checked from the CLI with `openclaw tasks list`, `openclaw tasks show <taskId>`, and `openclaw tasks cancel <taskId>`.

## Configuration

### Model selection

Configure a primary model and an ordered fallback list under `agents.defaults.musicGenerationModel`:

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: {
        primary: "google/lyria-3-clip-preview",
        fallbacks: ["fal/fal-ai/minimax-music/v2.6", "minimax/music-2.6"],
      },
    },
  },
}
```

### Provider selection order

OpenClaw tries providers in this order: (1) `model` parameter from the tool call (if the agent specifies one); (2) `musicGenerationModel.primary` from config; (3) `musicGenerationModel.fallbacks` in order; (4) auto-detection using auth-backed provider defaults only — current default provider first, then remaining registered music-generation providers in provider-id order. If a provider fails, the next candidate is tried automatically; if all fail, the error includes details from each attempt. Set `agents.defaults.mediaGenerationAutoProviderFallback: false` to use only explicit `model`, `primary`, and `fallbacks` entries.

## Provider notes

- **ComfyUI** — workflow-driven and depends on the configured graph plus node mapping for prompt/output fields; the bundled `comfy` plugin plugs into the shared `music_generate` tool through the music-generation provider registry.
- **fal** — uses fal model endpoints through the shared provider auth path; the bundled provider defaults to `fal-ai/minimax-music/v2.6` and also exposes `fal-ai/ace-step/prompt-to-audio` and `fal-ai/stable-audio-25/text-to-audio` for prompt-to-audio requests.
- **Google (Lyria 3)** — uses Lyria 3 batch generation; the current bundled flow supports prompt, optional lyrics text, and optional reference images.
- **MiniMax** — uses the batch `music_generation` endpoint; supports prompt, optional lyrics, instrumental mode, and mp3 output through either `minimax` API-key auth or `minimax-portal` OAuth.
- **OpenRouter** — uses OpenRouter chat completions audio output with streaming enabled; the bundled provider defaults to `google/lyria-3-pro-preview` and also exposes `openrouter/google/lyria-3-clip-preview`.

## Choosing the right path

Choose **shared provider-backed** when you want model selection, provider failover, and the built-in async task/status flow. Choose the **plugin path (ComfyUI)** when you need a custom workflow graph or a provider that is not part of the shared bundled music capability. For debugging ComfyUI-specific behavior, see the ComfyUI provider page; for shared-provider behavior, start with the fal, Google (Gemini), MiniMax, or OpenRouter provider pages.

## Provider capability modes

The shared music-generation contract supports explicit mode declarations — `generate` for prompt-only generation, and `edit` when the request includes one or more reference images. New provider implementations should prefer explicit mode blocks:

```typescript
capabilities: {
  generate: {
    maxTracks: 1,
    supportsLyrics: true,
    supportsFormat: true,
  },
  edit: {
    enabled: true,
    maxTracks: 1,
    maxInputImages: 1,
    supportsFormat: true,
  },
}
```

Legacy flat fields such as `maxInputImages`, `supportsLyrics`, and `supportsFormat` are **not** enough to advertise edit support. Providers should declare `generate` and `edit` explicitly so live tests, contract tests, and the shared `music_generate` tool can validate mode support deterministically.

## Live tests

Opt-in live coverage for the shared bundled providers is run with `OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/music-generation-providers.live.test.ts` (or the repo wrapper `pnpm test:live:media music`). This live file uses already-exported provider env vars ahead of stored auth profiles by default, and runs both `generate` and declared `edit` coverage when the provider enables edit mode. Coverage today is `google` (`generate` plus `edit`), `fal` (`generate` only), `minimax` (`generate` only), `openrouter` (`generate` plus `edit`), and `comfy` (separate Comfy live coverage, not the shared provider sweep). The bundled ComfyUI music path has its own opt-in live invocation `OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts`; that Comfy live file also covers comfy image and video workflows when those sections are configured.

**Source**: OpenClaw documentation — `tools/music-generation` (mirror `inbox/openclaw_docs/tools/music-generation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
