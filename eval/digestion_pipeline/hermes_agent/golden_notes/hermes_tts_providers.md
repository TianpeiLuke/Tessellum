---
tags:
  - resource
  - documentation
  - hermes_agent
  - tts
  - media
keywords:
  - text-to-speech
  - TTS providers
  - Edge TTS
  - ElevenLabs
  - Gemini audio tags
  - register_tts_provider
  - command provider
topics:
  - Hermes Agent
  - Text-to-Speech
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/tts
access_control_group: ["general"]
---

# Hermes Agent — Text-to-Speech Provider Subsystem

## Overview

The Hermes Agent TTS subsystem is a **provider registry** that converts a reply's text into spoken audio, then delivers it across messaging platforms. It is a pluggable catalog: **ten built-in providers** (Edge TTS is the no-key default, plus ElevenLabs, OpenAI, MiniMax, Mistral/Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, and Piper), a **command-type provider** registry that wires in any CLI without writing Python, and a **Python plugin** path (`register_tts_provider()`) for SDK-only or streaming engines. The `text_to_speech` tool resolves the configured `tts.provider`, truncates input to that provider's per-request character cap, synthesizes the audio, and hands it to the gateway, which delivers it as a native voice bubble (Telegram/Discord) or audio-file attachment (WhatsApp/CLI).

This page documents the **outbound (text→audio) direction**. The mirror-image inbound direction (voice-message transcription / STT) is its own subsystem — see [hermes_stt_transcription](hermes_stt_transcription.md). The full `tts:` config block lives in [hermes_messaging_media_settings](hermes_messaging_media_settings.md) (SP02); paid OpenAI TTS is also reachable without a separate key through the Tool Gateway / Nous Portal billing path (`hermes setup --portal`).

## Text-to-Speech Providers

Hermes converts text to speech with ten providers, each with a quality/cost/key profile. Edge TTS is the default and needs no API key; NeuTTS, KittenTTS, and Piper are also free and run locally; the rest are paid or free-tier cloud providers authenticating via env-var keys.

| Provider | Quality | Cost | API Key |
|----------|---------|------|---------|
| **Edge TTS** (default) | Good | Free | None needed |
| **ElevenLabs** | Excellent | Paid | `ELEVENLABS_API_KEY` |
| **OpenAI TTS** | Good | Paid | `VOICE_TOOLS_OPENAI_KEY` |
| **MiniMax TTS** | Excellent | Paid | `MINIMAX_API_KEY` |
| **Mistral (Voxtral TTS)** | Excellent | Paid | `MISTRAL_API_KEY` |
| **Google Gemini TTS** | Excellent | Free tier | `GEMINI_API_KEY` |
| **xAI TTS** | Excellent | Paid | `XAI_API_KEY` |
| **NeuTTS** | Good | Free (local) | None needed |
| **KittenTTS** | Good | Free (local) | None needed |
| **Piper** | Good | Free (local) | None needed |

## Platform Delivery

Synthesized audio is delivered per platform as a native voice bubble where supported, otherwise as a file attachment:

| Platform | Delivery | Format |
|----------|----------|--------|
| Telegram | Voice bubble (plays inline) | Opus `.ogg` |
| Discord | Voice bubble (Opus/OGG), falls back to file attachment | Opus/MP3 |
| WhatsApp | Audio file attachment | MP3 |
| CLI | Saved to `~/.hermes/audio_cache/` | MP3 |

## Configuration

The `tts:` block (in `~/.hermes/config.yaml`) selects a provider and holds per-provider settings. A single block carries the knobs for all ten built-ins; the full reference (verbatim per-provider voice IDs, models, and ranges) is owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md). The canonical Gemini sub-block is shown here as the load-bearing example:

```yaml
# In ~/.hermes/config.yaml
tts:
  provider: "edge"              # "edge" | "elevenlabs" | "openai" | "minimax" | "mistral" | "gemini" | "xai" | "neutts" | "kittentts" | "piper"
  speed: 1.0                    # Global speed multiplier (provider-specific settings override this)
  gemini:
    model: "gemini-2.5-flash-preview-tts"  # or gemini-3.1-flash-tts-preview
    voice: "Kore"               # 30 prebuilt voices: Zephyr, Puck, Kore, Enceladus, Gacrux, etc.
    audio_tags: false           # Enable hidden Gemini 3.1 TTS audio-tag insertion
    persona_prompt_file: ""     # Optional Markdown/text file with Gemini voice direction
```

Other built-ins follow the same shape under their own key: `edge.voice` (`en-US-AriaNeural`; 322 voices, 74 languages), `elevenlabs.voice_id`/`model_id`, `openai.model`/`voice`/`base_url` (alloy, echo, fable, onyx, nova, shimmer), `minimax.model`/`voice_id`/`vol`/`pitch`, `mistral.model`/`voice_id`, `xai.voice_id`/`language`/`sample_rate`/`bit_rate`, `neutts.ref_audio`/`ref_text`/`model`/`device`, `kittentts.model`/`voice`/`speed`/`clean_text`, and `piper.voice`.

**Speed control.** The global `tts.speed` value applies to all providers by default. Each provider can
override it with its own `speed` setting (e.g., `tts.openai.speed: 1.5`); provider-specific speed takes precedence over the global value. Default is `1.0` (normal speed).

## Gemini Persona Prompts

Gemini TTS can follow natural-language performance direction. Setting `tts.gemini.persona_prompt_file` to a local Markdown or text file describes the voice persona; the file can include Gemini-style sections such as `AUDIO PROFILE`, `SCENE`, `DIRECTOR'S NOTES`, `SAMPLE CONTEXT`, and `TRANSCRIPT`. If the file contains `{transcript}` or `{{ transcript }}`, Hermes replaces that placeholder with the live TTS text; otherwise Hermes appends a labeled `TRANSCRIPT` section automatically. The persona prompt stays local and is not shown in the chat reply.

```yaml
tts:
  provider: gemini
  gemini:
    voice: Algieba
    persona_prompt_file: ~/.hermes/tts/butler-voice.md
```

## Gemini Audio Tags

Gemini 3.1 Flash TTS supports freeform square-bracket audio tags such as `[whispers]`, `[excitedly]`, `[very slow]`, `[laughs]`, and other expressive delivery notes. Enabling `tts.gemini.audio_tags` has Hermes run a **hidden rewrite pass** before Gemini TTS — the rewrite inserts inline tags into the TTS script only, while the visible chat reply stays unchanged. The rewrite uses `auxiliary.tts_audio_tags` and defaults to your main chat model; override that auxiliary task to have tag insertion handled by a cheaper or faster model.

## Input Length Limits

Each provider has a documented per-request input-character cap. Hermes **truncates text before calling the provider** so requests never fail with a length error: Edge TTS 5000, OpenAI 4096, xAI 15000, MiniMax 10000, Mistral 4000, Google Gemini 32000, NeuTTS 2000, KittenTTS 2000, Piper 5000. **ElevenLabs** picks a cap from the configured `model_id` — `eleven_flash_v2_5` 40000, `eleven_flash_v2` 30000, `eleven_multilingual_v2` (default) 10000, `eleven_v3`/`eleven_ttv_v3` 5000, and an unknown model falls back to the provider default (10000).

The cap is overridable per provider with `max_text_length:` under the provider section. Only positive integers are honored; zero, negative, non-numeric, or boolean values fall through to the provider default, so a broken config can't accidentally disable truncation.

```yaml
tts:
  openai:
    max_text_length: 8192   # raise or lower the provider cap
```

## Telegram Voice Bubbles & ffmpeg

Telegram voice bubbles require Opus/OGG audio. **OpenAI, ElevenLabs, and Mistral** produce Opus natively — no extra setup. **Edge TTS** (default) and **MiniMax** output MP3 and need **ffmpeg** to convert; **Google Gemini** outputs raw PCM and uses ffmpeg to encode Opus directly; **xAI** outputs MP3; and **NeuTTS / KittenTTS / Piper** output WAV — all need ffmpeg for the conversion. Install ffmpeg via `apt`/`brew`/`dnf`. Without ffmpeg, Edge/MiniMax/NeuTTS/KittenTTS/Piper audio is sent as regular audio files (playable, but shown as a rectangular player instead of a voice bubble). If you want voice bubbles without installing ffmpeg, switch to the OpenAI, ElevenLabs, or Mistral provider.

## xAI Custom Voices and Piper

**xAI custom voices (voice cloning).** xAI supports cloning your voice and using it with TTS. Create a
custom voice in the xAI Console, then set the resulting `voice_id` in your config (`tts.xai.voice_id`).

**Piper (local, 44 languages).** Piper is a fast, local neural TTS engine from the Open Home Foundation
(the Home Assistant maintainers). It runs entirely on CPU, supports 44 languages with pre-trained voices, and needs no API key. Install via `hermes tools` → Voice & TTS → Piper (runs `pip install piper-tts`) or manually. On the first TTS call for an uncached voice, Hermes runs `python -m piper.download_voices <name>` and downloads the model (~20–90MB depending on quality tier) into `~/.hermes/cache/piper-voices/`; subsequent calls reuse the cached model. A voice can also be a pre-downloaded absolute `.onnx` path. Advanced knobs (`length_scale` / `noise_scale` / `noise_w_scale` / `volume` / `normalize_audio`, `use_cuda`) correspond 1:1 to Piper's `SynthesisConfig` and are ignored on older `piper-tts` versions.

## Custom Command Providers

If a TTS engine you want isn't natively supported (VoxCPM, MLX-Kokoro, XTTS CLI, a voice-cloning script, anything that exposes a CLI), you can wire it in as a **command-type provider** without writing any Python. Hermes writes the input text to a temp UTF-8 file, runs your shell command, and reads the audio file the command produced. Declare one or more providers under `tts.providers.<name>` and switch between them with `tts.provider: <name>` — the same way you switch between built-ins like `edge` and `openai`.

```yaml
tts:
  provider: voxcpm                 # pick any name under tts.providers
  providers:
    voxcpm:
      type: command
      command: "voxcpm --ref ~/voice.wav --text-file {input_path} --out {output_path}"
      output_format: mp3
      timeout: 180
      voice_compatible: true       # try to deliver as a Telegram voice bubble
    mlx-kokoro:
      type: command
      command: "python -m mlx_kokoro --in {input_path} --out {output_path} --voice {voice}"
      voice: af_sky
      output_format: wav
```

**Example: Doubao (Chinese seed-tts-2.0).** For high-quality Chinese TTS via ByteDance's seed-tts-2.0
bidirectional-streaming API, install the `doubao-speech` PyPI package, export `VOLCENGINE_APP_ID` / `VOLCENGINE_ACCESS_TOKEN`, and declare a command provider running `doubao-speech say --text-file {input_path} --out {output_path}`. The same package bundles streaming ASR for the STT side.

**Placeholders.** The command template can reference `{input_path}` (the temp UTF-8 text file),
`{text_path}` (an alias for it), `{output_path}` (where the command must write audio), `{format}` (`mp3`/`wav`/`ogg`/`flac`), `{voice}`, `{model}`, and `{speed}` (the resolved multiplier). Hermes shell-quotes each value for its surrounding context, so paths with spaces are safe; use `{{`/`}}` for literal braces.

**Optional keys.** `timeout` (default `120`s; the process tree is killed on expiry), `output_format`
(default `mp3`, auto-inferred from the output extension), `voice_compatible` (default `false`; when `true` Hermes converts MP3/WAV to Opus/OGG via ffmpeg for a Telegram voice bubble), `max_text_length` (default `5000`), and `voice`/`model` (empty; passed to the command as placeholder values only).

**Behavior and security.** Built-in names always win — a `tts.providers.openai` entry never shadows the
native OpenAI provider. Command providers deliver as regular audio documents on every platform by default (opt into voice-bubble delivery with `voice_compatible: true`). Failures (non-zero exit, empty output, timeout) surface to the agent with stderr/stdout included. `type: command` is the default when `command:` is set. Command-type providers run whatever shell command you configure with your user's permissions: Hermes quotes placeholders and enforces the timeout, but the command template itself is trusted local input — treat it like a shell script on your PATH.

## Python Plugin Providers

For TTS engines that can't be expressed as a single shell command — Python SDKs without a CLI, streaming engines, voice-listing APIs, OAuth-refreshing auth — register a Python plugin via `ctx.register_tts_provider()`. The plugin **coexists with** (does not replace) the command-provider registry. The precedence rule is: **built-ins always win, and command providers win over a same-name plugin** — so plugins are safe to register against any non-built-in name without shadowing existing config. Pick the **command provider** for a single CLI (or a couple chained with shell pipes), and a
**plugin** for a Python-SDK-only backend, streaming bytes (override `stream()`), a voice-listing API for
`hermes setup` (override `list_voices()`), or an OAuth refresh flow.

A minimal plugin drops a `plugin.yaml` and `__init__.py` into `~/.hermes/plugins/my-tts/`, subclassing the `TTSProvider` ABC and registering it from `register(ctx)`:

```python
from agent.tts_provider import TTSProvider


class MyTTSProvider(TTSProvider):
    @property
    def name(self) -> str:
        return "my-tts"  # what tts.provider matches against

    def is_available(self) -> bool:
        # Return False when credentials/deps are missing — picker skips
        # this row but the dispatcher still routes here on explicit config.
        import os
        return bool(os.environ.get("MY_TTS_API_KEY"))

    def synthesize(self, text, output_path, *, voice=None, model=None,
                   speed=None, format="mp3", **extra) -> str:
        # Write audio bytes to output_path, return the path. Raise on
        # failure — the dispatcher converts exceptions to an error envelope.
        import my_tts_sdk
        audio_bytes = my_tts_sdk.Client().synthesize(text=text, voice=voice or "default")
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return output_path


def register(ctx):
    ctx.register_tts_provider(MyTTSProvider())
```

Enable it (`hermes plugins enable my-tts`), point `tts.provider` at it, and the `text_to_speech` tool routes through the plugin. **Optional hooks** for richer integration: `list_voices()` → `{id, display, language, gender, preview_url}` dicts shown in `hermes tools`; `list_models()` → `{id, display, languages, max_text_length}` dicts; `get_setup_schema()` → `{name, badge, tag, env_vars}` to power the picker row in `hermes tools` / `hermes setup`; `stream(text, *, voice, model, format, **extra)` → an iterator yielding audio bytes for streaming delivery (default raises `NotImplementedError`); and a `voice_compatible` property (set `True` for Opus-compatible output the gateway delivers as a voice bubble). See `agent/tts_provider.py` for the full ABC including docstrings.

**Source**: `inbox/hermes_agent_docs/user-guide/features/tts.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/tts
**Last Updated**: 2026-06-19
**Status**: Active
