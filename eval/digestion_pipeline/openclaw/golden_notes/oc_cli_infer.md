---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - infer
keywords:
  - openclaw infer
  - headless inference cli
  - model run thinking
  - image generate edit describe
  - audio transcribe tts convert
  - video web embedding capability
  - infer json envelope
  - local vs gateway transport
topics:
  - OpenClaw
  - Inference CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/infer
access_control_group: ["general"]
---

# OpenClaw — `openclaw infer` Headless Inference CLI

## Overview

This note is the procedure reference for `openclaw infer`, OpenClaw's canonical headless surface for provider-backed inference workflows. It mirrors the `cli/infer` source page in full: the command tree, the common-task map, model/image/audio/TTS/video/web/embedding capability families, run behavior (local vs `--gateway` transport defaults, `--thinking` levels, image attach via `--file`), the stable `--json` output envelope, common pitfalls, and notes. `openclaw infer` intentionally exposes capability families rather than raw gateway RPC names or raw agent tool ids, and `openclaw capability ...` is an alias for `openclaw infer ...`.

## Why use infer

`openclaw infer` provides one consistent CLI for provider-backed inference tasks inside OpenClaw. Its benefits are: use the providers and models already configured in OpenClaw instead of wiring up one-off wrappers for each backend; keep model, image, audio transcription, TTS, video, web, and embedding workflows under one command tree; use a stable `--json` output shape for scripts, automation, and agent-driven workflows; prefer a first-party OpenClaw surface when the task is fundamentally "run inference"; and use the normal local path without requiring the gateway for most infer commands. For end-to-end provider checks, prefer `openclaw infer ...` once lower-level provider tests are green — it exercises the shipped CLI, config loading, default-agent resolution, bundled plugin activation, and the shared capability runtime before the provider request is made.

## Turn infer into a skill

The source recommends turning infer into an agent skill by pasting an instruction to an agent telling it to read `https://docs.openclaw.ai/cli/infer` and create a skill that routes common workflows (model runs, image generation, video generation, audio transcription, TTS, web search, embeddings) to `openclaw infer`. A good infer-based skill should: map common user intents to the correct infer subcommand; include a few canonical infer examples for the workflows it covers; prefer `openclaw infer ...` in examples and suggestions; and avoid re-documenting the entire infer surface inside the skill body. Typical infer-focused skill coverage spans `openclaw infer model run`, `openclaw infer image generate`, `openclaw infer audio transcribe`, `openclaw infer tts convert`, `openclaw infer web search`, and `openclaw infer embedding create`.

## Command tree

`openclaw infer` exposes top-level `list` and `inspect`, plus seven capability families — `model`, `image`, `audio`, `tts`, `video`, `web`, and `embedding` — each with its own subcommands.

```text
 openclaw infer
  list
  inspect

  model
    run
    list
    inspect
    providers
    auth login
    auth logout
    auth status

  image
    generate
    edit
    describe
    describe-many
    providers

  audio
    transcribe
    providers

  tts
    convert
    voices
    providers
    status
    enable
    disable
    set-provider

  video
    generate
    describe
    providers

  web
    search
    fetch
    providers

  embedding
    create
    providers
```

## Common tasks

The source maps common inference tasks to infer commands: run a text/model prompt → `openclaw infer model run --prompt "..." --json` (uses the normal local path by default); run a model prompt on images → `openclaw infer model run --prompt "Describe this" --file ./image.png --model provider/model` (repeat `--file` for multiple image inputs); generate an image → `openclaw infer image generate --prompt "..." --json` (use `image edit` when starting from an existing file); describe an image file or URL → `openclaw infer image describe --file ./image.png --prompt "..." --json` (`--model` must be an image-capable `<provider/model>`); transcribe audio → `openclaw infer audio transcribe --file ./memo.m4a --json` (`--model` must be `<provider/model>`); synthesize speech → `openclaw infer tts convert --text "..." --output ./speech.mp3 --json` (`tts status` is gateway-oriented); generate a video → `openclaw infer video generate --prompt "..." --json` (supports provider hints such as `--resolution`); describe a video file → `openclaw infer video describe --file ./clip.mp4 --json`; search the web → `openclaw infer web search --query "..." --json`; fetch a web page → `openclaw infer web fetch --url https://example.com --json`; and create embeddings → `openclaw infer embedding create --text "..." --json`.

## Behavior (transport, thinking, image attach)

`openclaw infer ...` is the primary CLI surface for these workflows. Use `--json` when the output will be consumed by another command or script, and use `--provider` or `--model provider/model` when a specific backend is required. Use `model run --thinking <level>` to pass a one-shot thinking/reasoning level (`off`, `minimal`, `low`, `medium`, `high`, `adaptive`, `xhigh`, or `max`) while keeping the run raw; the local path uses the lean provider-completion path and maps provider-specific levels such as `adaptive` and `max` to the closest portable simple-completion level. Transport defaults split by command class: stateless execution commands default to local, gateway-managed state commands default to gateway, and the normal local path does not require the gateway to be running.

Local `model run` is a lean one-shot provider completion: it resolves the configured agent model and auth, but does not start a chat-agent turn, load tools, or open bundled MCP servers. `model run --file` accepts image files, detects their MIME type, and sends them with the supplied prompt to the selected model (repeat `--file` for multiple images); it rejects non-image inputs — use `infer audio transcribe` for audio files and `infer video describe` for video files. For `image describe`, `audio transcribe`, and `video describe`, `--model` must use the form `<provider/model>`; for `image describe`, `--file` accepts local paths and HTTP(S) image URLs, and remote URLs use the normal media-fetch SSRF policy. For `image describe`, an explicit `--model` runs that provider/model directly and the model must be image-capable in the model catalog or provider config — `codex/<model>` runs a bounded Codex app-server image-understanding turn, while `openai/<model>` uses the OpenAI provider path with either API-key or ChatGPT/Codex OAuth auth.

`model run --gateway` exercises Gateway routing, saved auth, provider selection, and the embedded runtime, but still runs as a raw model probe: it sends the supplied prompt and any image attachments without prior session transcript, bootstrap/AGENTS context, context-engine assembly, tools, or bundled MCP servers. `model run --gateway --model <provider/model>` requires a trusted operator gateway credential because the request asks the Gateway to run a one-off provider/model override.

## Model

Use `model` for provider-backed text inference and model/provider inspection. Canonical runs cover prompt completion, explicit `--model <provider/model>` selection, image-attach via `--file`, `--thinking`, plus `model providers` and `model inspect`:

```bash
openclaw infer model run --prompt "Reply with exactly: smoke-ok" --json
openclaw infer model run --prompt "Summarize this changelog entry" --model openai/gpt-5.4 --json
openclaw infer model run --prompt "Describe this image in one sentence" --file ./photo.jpg --model google/gemini-2.5-flash --json
openclaw infer model run --prompt "Use more reasoning here" --thinking high --json
openclaw infer model providers --json
openclaw infer model inspect --name gpt-5.5 --json
```

Use full `<provider/model>` refs with `--local` to smoke-test a specific provider without starting the Gateway or loading the full agent tool surface (e.g. `anthropic/claude-sonnet-4-6`, `cerebras/zai-glm-4.7`, `google/gemini-2.5-flash`, `groq/llama-3.1-8b-instant`, `mistral/mistral-medium-3-5`, `openai/gpt-5.5`, `ollama/qwen2.5vl:7b`). Key model-run notes from source: local `model run` is the narrowest CLI smoke for provider/model/auth health because, for non-Codex providers, it sends only the supplied prompt; local `model run --model <provider/model>` can use exact bundled static catalog rows from `models list --all` before that provider is written to config, but provider auth is still required (missing credentials fail as auth errors, not `Unknown model`). For Mistral Medium 3.5 reasoning probes, leave temperature unset/default (Mistral rejects `reasoning_effort="high"` plus `temperature: 0`; use default temperature or a non-zero value such as `0.7`). Codex Responses local probes are the narrow exception — OpenClaw adds a minimal system instruction so the transport can populate its required `instructions` field, without adding full agent context, tools, memory, or session transcript. Local `model run --file` keeps the lean path and attaches image content directly to the single user message (PNG/JPEG/WebP work when MIME is detected as `image/*`; unsupported files fail before the provider is called), and the selected model must support image input. `model run --prompt` must contain non-whitespace text (empty prompts are rejected before providers or the Gateway are called), and local `model run` exits non-zero when the provider returns no text output so unreachable providers and empty completions do not look like successful probes. `model auth login`, `model auth logout`, and `model auth status` manage saved provider auth state.

## Image

Use `image` for generation, edit, and description. Representative commands:

```bash
openclaw infer image generate --prompt "friendly lobster illustration" --json
openclaw infer image generate --model openai/gpt-image-1.5 --output-format png --background transparent --prompt "simple red circle sticker on a transparent background" --json
openclaw infer image edit --file ./logo.png --model openai/gpt-image-1.5 --output-format png --background transparent --prompt "keep the logo, remove the background" --json
openclaw infer image describe --file ./receipt.jpg --prompt "Extract the merchant, date, and total" --json
openclaw infer image describe-many --file ./before.png --file ./after.png --prompt "Compare the screenshots and list visible UI changes" --json
```

Image notes from source: use `image edit` when starting from existing input files; use `--size`, `--aspect-ratio`, or `--resolution` with `image edit` for providers/models that support geometry hints on reference-image edits; use `--output-format png --background transparent` with `--model openai/gpt-image-1.5` for transparent-background OpenAI PNG output (`--openai-background` remains available as an OpenAI-specific alias, and providers that do not declare background support report the hint as an ignored override); use `--quality low|medium|high|auto` for providers that support image quality hints including OpenAI, which also accepts `--openai-moderation low|auto`. Use `image providers --json` to verify which bundled image providers are discoverable, configured, selected, and which generation/edit capabilities each exposes; use `image generate --model <provider/model> --json` as the narrowest live CLI smoke for image generation changes (the JSON response reports `ok`, `provider`, `model`, `attempts`, and written output paths, and when `--output` is set the final extension may follow the provider's returned MIME type). For `image describe`/`image describe-many`, use `--prompt` to give the vision model a task-specific instruction (OCR, comparison, UI inspection, concise captioning); use `--timeout-ms` with slow local vision models or cold Ollama starts; `--model` must be an image-capable `<provider/model>`; and for local Ollama vision models, pull the model first and set `OLLAMA_API_KEY` to any placeholder value (for example `ollama-local`).

## Audio, TTS, Video, Web, Embedding

Use `audio` for file transcription (not realtime session management; `--model` must be `<provider/model>`):

```bash
openclaw infer audio transcribe --file ./memo.m4a --json
openclaw infer audio transcribe --file ./team-sync.m4a --language en --prompt "Focus on names and action items" --json
openclaw infer audio transcribe --file ./memo.m4a --model openai/whisper-1 --json
```

Use `tts` for speech synthesis and TTS provider state — `tts convert`, `tts providers`, `tts voices`, `tts set-provider`, and `tts status` (which defaults to gateway because it reflects gateway-managed TTS state). Use `video` for generation and description: `video generate` accepts `--size`, `--aspect-ratio`, `--resolution`, `--duration`, `--audio`, `--watermark`, and `--timeout-ms` and forwards them to the video-generation runtime, and `--model` must be `<provider/model>` for `video describe`. Use `web` for `web search`, `web fetch`, and `web providers` (use `web providers` to inspect available, configured, and selected providers). Use `embedding` for vector creation and embedding provider inspection — `embedding create` (optionally with `--model openai/text-embedding-3-large`) and `embedding providers`.

## JSON output

Infer commands normalize JSON output under a shared envelope. The top-level fields are stable: `ok`, `capability`, `transport`, `provider`, `model`, `attempts`, `outputs`, and `error`.

```json
{
  "ok": true,
  "capability": "image.generate",
  "transport": "local",
  "provider": "openai",
  "model": "gpt-image-2",
  "attempts": [],
  "outputs": []
}
```

For generated media commands, `outputs` contains files written by OpenClaw; use the `path`, `mimeType`, `size`, and any media-specific dimensions in that array for automation instead of parsing human-readable stdout.

## Common pitfalls

The source flags two common mistakes: there is no `media` subcommand level (`openclaw infer media image generate ...` is wrong; use `openclaw infer image generate ...`), and transcription `--model` must be the fully-qualified `<provider/model>` form (`--model whisper-1` is wrong; use `--model openai/whisper-1`).

```bash
# Bad
openclaw infer media image generate --prompt "friendly lobster"

# Good
openclaw infer image generate --prompt "friendly lobster"
```

**Source**: OpenClaw documentation — `cli/infer` (mirror `inbox/openclaw_docs/cli/infer.md`)
**Last Updated**: 2026-06-22
**Status**: Active
