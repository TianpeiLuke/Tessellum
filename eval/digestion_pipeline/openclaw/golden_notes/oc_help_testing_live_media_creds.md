---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - testing
keywords:
  - openclaw live media tests
  - live test credentials never commit
  - deepgram byteplus comfyui live
  - image music video generation live
  - OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS
  - auth-profiles.json profile keys
  - staged temp test home
  - pnpm test:live:media harness
topics:
  - OpenClaw
  - Live Tests
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/testing-live
access_control_group: ["general"]
---

# OpenClaw — Live Media-Provider Suites & Live-Test Credential Resolution

## Overview

This procedure note covers the **media-provider** half of OpenClaw's live (network-touching) test surface plus the **credential-resolution** rules that govern every live test, mirroring the `Credentials (never commit)` through `Media live harness` sections of the `help/testing-live` source page. It documents how live tests discover credentials (the same path the CLI uses — profile store vs env fallbacks, the staged temp test home, and the `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS` enforcement), then walks the bundled media live suites: Deepgram audio transcription, BytePlus coding plan, ComfyUI workflow media, the shared image / music / video generation runtimes, and the `pnpm test:live:media` harness that runs all three through one entrypoint. The live model/agent smoke layers (direct/gateway/CLI/ACP/Codex, recipes, and the model matrix) live in the sibling note `oc_help_testing_live_models`.

## Credentials (never commit)

Live tests discover credentials **the same way the CLI does**, so two practical implications hold: if the CLI works, live tests should find the same keys; and if a live test reports "no creds", debug it exactly as you would debug `openclaw models list` / model selection. Credentials are never committed to the repo.

The credential sources, in the locations the source page names verbatim:

- **Per-agent auth profiles**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` — this is what "profile keys" means in the live tests.
- **Config**: `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`).
- **Legacy state dir**: `~/.openclaw/credentials/` — copied into the staged live home when present, but it is not the main profile-key store.

Live local runs **stage a temp test home** to keep probes off your real host: they copy the active config, per-agent `auth-profiles.json` files, the legacy `credentials/` dir, and supported external CLI auth dirs into a temp test home by default. The staged live homes **skip `workspace/` and `sandboxes/`**, and `agents.*.workspace` / `agentDir` path overrides are stripped so probes stay off your real host workspace. If you want to rely on env keys instead, export them before local tests, or use the Docker runners with an explicit `OPENCLAW_PROFILE_FILE`.

Several media suites add a uniform credential-precedence rule: they **use live/env API keys ahead of stored auth profiles by default**, so stale test keys in `auth-profiles.json` do not mask real shell credentials. To invert that and force the profile store, set `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1`, which forces profile-store auth and ignores env-only overrides (the image, music, and video generation suites all honor this flag).

## Deepgram live (audio transcription)

- **Test**: `extensions/deepgram/audio.live.test.ts`
- **Enable**: `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live extensions/deepgram/audio.live.test.ts`

## BytePlus coding plan live

- **Test**: `extensions/byteplus/live.test.ts`
- **Enable**: `BYTEPLUS_API_KEY=... BYTEPLUS_LIVE_TEST=1 pnpm test:live extensions/byteplus/live.test.ts`
- **Optional model override**: `BYTEPLUS_CODING_MODEL=ark-code-latest`

## ComfyUI workflow media live

- **Test**: `extensions/comfy/comfy.live.test.ts`
- **Enable**: `OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts`
- **Scope**: exercises the bundled comfy image, video, and `music_generate` paths; skips each capability unless `plugins.entries.comfy.config.<capability>` is configured; useful after changing comfy workflow submission, polling, downloads, or plugin registration.

## Image generation live

- **Test**: `test/image-generation.runtime.live.test.ts`
- **Command**: `pnpm test:live test/image-generation.runtime.live.test.ts`
- **Harness**: `pnpm test:live:media image`

This suite enumerates **every registered image-generation provider plugin**, uses already-exported provider env vars before probing, uses live/env API keys ahead of stored auth profiles by default (so stale test keys in `auth-profiles.json` do not mask real shell credentials), and skips providers with no usable auth/profile/model. It runs each configured provider through the shared image-generation runtime as `<provider>:generate`, and `<provider>:edit` when the provider declares edit support.

Currently bundled providers covered: `deepinfra`, `fal`, `google`, `minimax`, `openai`, `openrouter`, `vydra`, `xai`.

Optional narrowing (verbatim env knobs):

- `OPENCLAW_LIVE_IMAGE_GENERATION_PROVIDERS="openai,google,openrouter,xai"`
- `OPENCLAW_LIVE_IMAGE_GENERATION_PROVIDERS="deepinfra"`
- `OPENCLAW_LIVE_IMAGE_GENERATION_MODELS="openai/gpt-image-2,google/gemini-3.1-flash-image-preview,openrouter/google/gemini-3.1-flash-image-preview,xai/grok-imagine-image"`
- `OPENCLAW_LIVE_IMAGE_GENERATION_CASES="google:flash-generate,google:pro-edit,openrouter:generate,xai:default-generate,xai:default-edit"`
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to force profile-store auth and ignore env-only overrides.

For the shipped CLI path, add an `infer` smoke after the provider/runtime live test passes:

```bash
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_INFER_CLI_TEST=1 pnpm test:live -- test/image-generation.infer-cli.live.test.ts
openclaw infer image providers --json
openclaw infer image generate \
  --model google/gemini-3.1-flash-image-preview \
  --prompt "Minimal flat test image: one blue square on a white background, no text." \
  --output ./openclaw-infer-image-smoke.png \
  --json
```

This CLI smoke covers CLI argument parsing, config/default-agent resolution, bundled plugin activation, the shared image-generation runtime, and the live provider request. Plugin dependencies are expected to be present before runtime load.

## Music generation live

- **Test**: `extensions/music-generation-providers.live.test.ts`
- **Enable**: `OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/music-generation-providers.live.test.ts`
- **Harness**: `pnpm test:live:media music`

This suite exercises the shared bundled music-generation provider path (currently covering Google and MiniMax), uses already-exported provider env vars before probing, uses live/env API keys ahead of stored auth profiles by default, and skips providers with no usable auth/profile/model. It runs both declared runtime modes when available: `generate` with prompt-only input, and `edit` when the provider declares `capabilities.edit.enabled`. The current shared-lane coverage is `google`: `generate`, `edit`; `minimax`: `generate`; `comfy` uses a separate Comfy live file, not this shared sweep.

Optional narrowing:

- `OPENCLAW_LIVE_MUSIC_GENERATION_PROVIDERS="google,minimax"`
- `OPENCLAW_LIVE_MUSIC_GENERATION_MODELS="google/lyria-3-clip-preview,minimax/music-2.6"`
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to force profile-store auth and ignore env-only overrides.

## Video generation live

- **Test**: `extensions/video-generation-providers.live.test.ts`
- **Enable**: `OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/video-generation-providers.live.test.ts`
- **Harness**: `pnpm test:live:media video`

This suite exercises the shared bundled video-generation provider path. It **defaults to the release-safe smoke path**: non-FAL providers, one text-to-video request per provider, a one-second lobster prompt, and a per-provider operation cap from `OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS` (`180000` by default). It **skips FAL by default** because provider-side queue latency can dominate release time — pass `--video-providers fal` or `OPENCLAW_LIVE_VIDEO_GENERATION_PROVIDERS="fal"` to run it explicitly. Like the other media suites it uses already-exported provider env vars before probing, uses live/env API keys ahead of stored auth profiles by default, skips providers with no usable auth/profile/model, and runs only `generate` by default.

Set `OPENCLAW_LIVE_VIDEO_GENERATION_FULL_MODES=1` to also run declared transform modes when available: `imageToVideo` when the provider declares `capabilities.imageToVideo.enabled` and the selected provider/model accepts buffer-backed local image input in the shared sweep; and `videoToVideo` when the provider declares `capabilities.videoToVideo.enabled` and the selected provider/model accepts buffer-backed local video input.

The source page enumerates the shared-sweep coverage and skip reasons precisely:

- Declared-but-skipped `imageToVideo` in the shared sweep: `vydra` (bundled `veo3` is text-only and bundled `kling` requires a remote image URL).
- Provider-specific Vydra coverage: `OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_VYDRA_VIDEO=1 pnpm test:live -- extensions/vydra/vydra.live.test.ts` — that file runs `veo3` text-to-video plus a `kling` lane that uses a remote image URL fixture by default.
- `videoToVideo` live coverage: `runway` only when the selected model is `runway/gen4_aleph`.
- Declared-but-skipped `videoToVideo` in the shared sweep: `alibaba`, `qwen`, `xai` (those paths currently require remote `http(s)` / MP4 reference URLs); `google` (the current shared Gemini/Veo lane uses local buffer-backed input, not accepted in the shared sweep); `openai` (the current shared lane lacks org-specific video edit access guarantees).

Optional narrowing:

- `OPENCLAW_LIVE_VIDEO_GENERATION_PROVIDERS="deepinfra,google,openai,runway"`
- `OPENCLAW_LIVE_VIDEO_GENERATION_MODELS="google/veo-3.1-fast-generate-preview,openai/sora-2,runway/gen4_aleph"`
- `OPENCLAW_LIVE_VIDEO_GENERATION_SKIP_PROVIDERS=""` to include every provider in the default sweep, including FAL.
- `OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS=60000` to reduce each provider operation cap for an aggressive smoke run.
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to force profile-store auth and ignore env-only overrides.

## Media live harness

The single entrypoint that ties the three shared media suites together is `pnpm test:live:media`. It runs the shared image, music, and video live suites through one repo-native entrypoint, uses already-exported provider env vars, auto-narrows each suite to providers that currently have usable auth by default, and reuses `scripts/test-live.mjs` so heartbeat and quiet-mode behavior stay consistent. Example invocations from the source page:

```bash
pnpm test:live:media
pnpm test:live:media image video --providers openai,google,minimax
pnpm test:live:media video --video-providers openai,runway --all-providers
pnpm test:live:media music --quiet
```

**Source**: OpenClaw documentation — `help/testing-live` (mirror `inbox/openclaw_docs/help/testing-live.md`), sections Credentials through Media live harness
**Last Updated**: 2026-06-22
**Status**: Active
