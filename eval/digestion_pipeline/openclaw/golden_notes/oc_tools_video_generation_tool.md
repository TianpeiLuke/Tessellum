---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - video_generation
keywords:
  - video_generate tool
  - openclaw video generation
  - async video task lifecycle
  - imageToVideo videoToVideo modes
  - videoGenerationModel config
  - video model selection fallback
  - video_generate parameters actions
topics:
  - OpenClaw
  - Video Generation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/video-generation
access_control_group: ["general"]
---

# OpenClaw — The `video_generate` Agent Tool (Lifecycle, Parameters, Model Selection)

## Overview

This note is the operational procedure for the OpenClaw `video_generate` agent tool — how an agent generates videos from text prompts, reference images, or existing videos, the async task lifecycle that backs every generation, and the parameter / action / model-selection / config surface. It mirrors the operator/agent-facing half of the `tools/video-generation` source page: the intro and three runtime modes, Quick start, how async generation works, the task lifecycle states, the full tool parameter set (Required, Content inputs, Style controls, Advanced) plus fallback/typed-option handling, the three actions, model resolution order, and configuration. The companion split sibling **oc_tools_video_generation_providers** covers the 16-backend provider/capability-matrix reference (Supported providers, Capability matrix, Provider notes, Provider capability modes, Live tests) — referenced here, not duplicated.

## What `video_generate` Is and Its Three Runtime Modes

OpenClaw agents can generate videos from text prompts, reference images, or existing videos. Sixteen provider backends are supported, each with different model options, input modes, and feature sets; the agent picks the right provider automatically based on your configuration and available API keys. The `video_generate` tool only appears when at least one video-generation provider is available — if you do not see it in your agent tools, set a provider API key or configure `agents.defaults.videoGenerationModel`.

OpenClaw treats video generation as three runtime modes: `generate` (text-to-video requests with no reference media), `imageToVideo` (request includes one or more reference images), and `videoToVideo` (request includes one or more reference videos). Providers can support any subset of those modes. The tool validates the active mode before submission and reports supported modes in `action=list`.

## Quick Start

Enable and exercise the tool in three steps:

1. **Configure auth** — set an API key for any supported provider: `export GEMINI_API_KEY="your-key"`.
2. **Pick a default model (optional)** — `openclaw config set agents.defaults.videoGenerationModel.primary "google/veo-3.1-fast-generate-preview"`.
3. **Ask the agent** — e.g. "Generate a 5-second cinematic video of a friendly lobster surfing at sunset." The agent calls `video_generate` automatically; **no tool allowlisting is needed**.

## How Async Generation Works

Video generation is asynchronous. When the agent calls `video_generate` in a session:

1. OpenClaw submits the request to the provider and immediately returns a task id.
2. The provider processes the job in the background (typically 30 seconds to several minutes depending on the provider and resolution; slow queue-backed providers can run up to the configured timeout).
3. When the video is ready, OpenClaw wakes the same session with an internal completion event.
4. The agent tells the user through the session's normal visible-reply mode: final reply delivery when automatic, or `message(action="send")` when the session requires the message tool. If the requester session is inactive or its active wake fails, and some generated video is still missing from the completion reply, OpenClaw sends an idempotent direct fallback with only the missing video.

While a job is in flight, duplicate `video_generate` calls in the same session return the current task status instead of starting another generation. Use `openclaw tasks list` or `openclaw tasks show <taskId>` to check progress from the CLI. Outside of session-backed agent runs (for example, direct tool invocations), the tool falls back to inline generation and returns the final media path in the same turn.

Generated video files are saved under OpenClaw-managed media storage when the provider returns bytes. The default generated-video save cap follows the video media limit, and `agents.defaults.mediaMaxMb` raises it for larger renders. When a provider also returns a hosted output URL, OpenClaw can deliver that URL instead of failing the task if local persistence rejects an oversized file.

### Task Lifecycle

A generation task moves through four states:

| State | Meaning |
| --- | --- |
| `queued` | Task created, waiting for the provider to accept it. |
| `running` | Provider is processing (typically 30 seconds to several minutes depending on provider and resolution). |
| `succeeded` | Video ready; the agent wakes and posts it to the conversation. |
| `failed` | Provider error or timeout; the agent wakes with error details. |

Check or manage status from the CLI:

```bash
openclaw tasks list
openclaw tasks show <taskId>
openclaw tasks cancel <taskId>
```

If a video task is already `queued` or `running` for the current session, `video_generate` returns the existing task status instead of starting a new one. Use `action: "status"` to check explicitly without triggering a new generation.

## Tool Parameters

### Required

- `prompt` (`string`, required) — text description of the video to generate. Required for `action: "generate"`.

### Content Inputs

- `image` (`string`) — single reference image (path or URL).
- `images` (`string[]`) — multiple reference images (up to 9).
- `imageRoles` (`string[]`) — optional per-position role hints parallel to the combined image list. Canonical values: `first_frame`, `last_frame`, `reference_image`.
- `video` (`string`) — single reference video (path or URL).
- `videos` (`string[]`) — multiple reference videos (up to 4).
- `videoRoles` (`string[]`) — optional per-position role hints parallel to the combined video list. Canonical value: `reference_video`.
- `audioRef` (`string`) — single reference audio (path or URL). Used for background music or voice reference when the provider supports audio inputs.
- `audioRefs` (`string[]`) — multiple reference audios (up to 3).
- `audioRoles` (`string[]`) — optional per-position role hints parallel to the combined audio list. Canonical value: `reference_audio`.

Role hints are forwarded to the provider as-is. Canonical values come from the `VideoGenerationAssetRole` union but providers may accept additional role strings. `*Roles` arrays must not have more entries than the corresponding reference list; off-by-one mistakes fail with a clear error. Use an empty string to leave a slot unset. For xAI, set every image role to `reference_image` to use its `reference_images` generation mode; omit the role or use `first_frame` for single-image image-to-video.

### Style Controls

- `aspectRatio` (`string`) — aspect-ratio hint such as `1:1`, `16:9`, `9:16`, `adaptive`, or a provider-specific value. OpenClaw normalizes or ignores unsupported values per provider.
- `resolution` (`string`) — resolution hint such as `480P`, `720P`, `768P`, `1080P`, `4K`, or a provider-specific value. OpenClaw normalizes or ignores unsupported values per provider.
- `durationSeconds` (`number`) — target duration in seconds (rounded to nearest provider-supported value).
- `size` (`string`) — size hint when the provider supports it.
- `audio` (`boolean`) — enable generated audio in the output when supported. Distinct from `audioRef*` (inputs).
- `watermark` (`boolean`) — toggle provider watermarking when supported.

`adaptive` is a provider-specific sentinel: it is forwarded as-is to providers that declare `adaptive` in their capabilities (e.g. BytePlus Seedance uses it to auto-detect the ratio from the input image dimensions). Providers that do not declare it surface the value via `details.ignoredOverrides` in the tool result so the drop is visible.

### Advanced

- `action` (`"generate" | "status" | "list"`, default `generate`) — `"status"` returns the current session task; `"list"` inspects providers.
- `model` (`string`) — provider/model override (e.g. `runway/gen4.5`).
- `filename` (`string`) — output filename hint.
- `timeoutMs` (`number`) — optional provider operation timeout in milliseconds. When omitted, OpenClaw uses `agents.defaults.videoGenerationModel.timeoutMs` if configured, otherwise the plugin-authored provider default when one exists.
- `providerOptions` (`object`) — provider-specific options as a JSON object (e.g. `{"seed": 42, "draft": true}`). Providers that declare a typed schema validate the keys and types; unknown keys or mismatches skip the candidate during fallback. Providers without a declared schema receive the options as-is. Run `video_generate action=list` to see what each provider accepts.

Not all providers support all parameters. OpenClaw normalizes duration to the closest provider-supported value, and remaps translated geometry hints such as size-to-aspect-ratio when a fallback provider exposes a different control surface. Truly unsupported overrides are ignored on a best-effort basis and reported as warnings in the tool result. Hard capability limits (such as too many reference inputs) fail before submission. Tool results report applied settings; `details.normalization` captures any requested-to-applied translation.

Reference inputs select the runtime mode: no reference media → `generate`; any image reference → `imageToVideo`; any video reference → `videoToVideo`. Reference audio inputs **do not** change the resolved mode — they apply on top of whatever mode the image/video references select, and only work with providers that declare `maxInputAudios`. Mixed image and video references are not a stable shared capability surface; prefer one reference type per request.

### Fallback and Typed Options

Some capability checks are applied at the fallback layer rather than the tool boundary, so a request that exceeds the primary provider's limits can still run on a capable fallback:

- An active candidate declaring no `maxInputAudios` (or `0`) is skipped when the request contains audio references; the next candidate is tried.
- An active candidate's `maxDurationSeconds` below the requested `durationSeconds` with no declared `supportedDurationSeconds` list → skipped.
- A request containing `providerOptions` against a candidate that explicitly declares a typed `providerOptions` schema → skipped if supplied keys are not in the schema or value types do not match. Providers without a declared schema receive options as-is (backward-compatible pass-through). A provider can opt out of all provider options by declaring an empty schema (`capabilities.providerOptions: {}`), which causes the same skip as a type mismatch.

The first skip reason in a request logs at `warn` so operators see when their primary provider was passed over; subsequent skips log at `debug` to keep long fallback chains quiet. If every candidate is skipped, the aggregated error includes the skip reason for each.

## Actions

| Action | What it does |
| --- | --- |
| `generate` | Default. Create a video from the given prompt and optional reference inputs. |
| `status` | Check the state of the in-flight video task for the current session without starting another generation. |
| `list` | Show available providers, models, and their capabilities. |

## Model Selection

OpenClaw resolves the model in this order:

1. **`model` tool parameter** — if the agent specifies one in the call.
2. **`videoGenerationModel.primary`** from config.
3. **`videoGenerationModel.fallbacks`** in order.
4. **Auto-detection** — providers that have valid auth, starting with the current default provider, then remaining providers in alphabetical order.

If a provider fails, the next candidate is tried automatically. If all candidates fail, the error includes details from each attempt. Set `agents.defaults.mediaGenerationAutoProviderFallback: false` to use only the explicit `model`, `primary`, and `fallbacks` entries.

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "google/veo-3.1-fast-generate-preview",
        fallbacks: ["runway/gen4.5", "qwen/wan2.6-t2v"],
      },
    },
  },
}
```

## Configuration

Set the default video-generation model in your OpenClaw config:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "qwen/wan2.6-t2v",
        fallbacks: ["qwen/wan2.6-r2v-flash"],
      },
    },
  },
}
```

Or via the CLI: `openclaw config set agents.defaults.videoGenerationModel.primary "qwen/wan2.6-t2v"`.

**Source**: OpenClaw documentation — `tools/video-generation` (mirror `inbox/openclaw_docs/tools/video-generation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
