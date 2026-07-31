---
tags:
  - resource
  - documentation
  - hermes_agent
  - voice
  - cli
keywords:
  - voice mode
  - push-to-talk
  - CLI voice
  - silence detection
  - streaming TTS
  - hallucination filter
  - Whisper STT
topics:
  - Hermes Agent
  - Voice
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode
access_control_group: ["general"]
---

# Hermes Voice Mode — CLI Push-to-Talk

## Overview

CLI voice mode is the local-microphone half of Hermes Agent voice: a continuous push-to-talk loop where you press a key, speak, and the agent transcribes your speech, answers, and (optionally) speaks the reply back — all from the terminal. It runs identically in the **classic CLI** (`hermes chat`) and the **TUI** (`hermes --tui`): same `/voice` slash commands, same VAD silence detection, same sentence-by-sentence streaming TTS, and the same Whisper hallucination filter. The TUI additionally forwards crash-forensic logs to `~/.hermes/logs/` so push-to-talk failures on exotic audio backends report a full stack trace rather than failing silently.

This note covers the CLI-side procedure: installing the audio extras and system dependencies, configuring STT/TTS keys, the `/voice` commands, the Ctrl+B record loop with two-stage silence detection, streaming TTS, and the hallucination filter. The gateway voice-reply and Discord voice-channel pipelines are a separate procedure — see [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md). The full `voice:`/`stt:`/`tts:` config blocks are owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md) (this note shows the relevant knobs and link-outs there).

## Prerequisites

Before enabling voice you need: Hermes Agent installed (`pip install hermes-agent`); an LLM provider configured (`hermes model` or credentials in `~/.hermes/.env`); and a working base setup verified by running `hermes` to confirm the agent responds to text. The `~/.hermes/` directory and default `config.yaml` are created automatically the first time you run `hermes` — you only create `~/.hermes/.env` manually for API keys.

A paid Nous Portal subscription supplies both the LLM and OpenAI TTS via the Tool Gateway (no separate OpenAI key needed); on a fresh install `hermes setup --portal` wires both up at once. The portal/gateway billing path is documented in the Tool Gateway / Nous Portal notes (link-outs).

## Requirements

Install the CLI voice extra (microphone + audio playback) and the supporting system libraries:

```bash
# CLI voice mode (microphone + audio playback)
pip install "hermes-agent[voice]"

# Premium TTS (ElevenLabs)
pip install "hermes-agent[tts-premium]"

# Local TTS (NeuTTS, optional) — downloads the model on first use
python -m pip install -U neutts[all]
```

The `voice` extra pulls `sounddevice` + `numpy`; `tts-premium` pulls `elevenlabs`. The CLI loop also needs OS-level audio tooling:

```bash
# macOS
brew install portaudio ffmpeg opus
brew install espeak-ng   # for NeuTTS

# Ubuntu/Debian
sudo apt install portaudio19-dev ffmpeg libopus0
sudo apt install espeak-ng   # for NeuTTS
```

**PortAudio** provides microphone input and audio playback (required for CLI voice mode); **ffmpeg** handles audio format conversion (MP3 → Opus, PCM → WAV); **Opus** is the Discord voice codec; **espeak-ng** is the phonemizer backend for the local NeuTTS provider.

For STT (speech-to-text), the local `faster-whisper` provider needs **no key at all** — install it and voice mode works with zero API keys (the `base` model, ~150 MB, downloads automatically on first use). Cloud STT/TTS keys go in `~/.hermes/.env`:

```bash
# Speech-to-Text — local provider needs NO key
# pip install faster-whisper          # Free, runs locally, recommended
GROQ_API_KEY=your-key                 # Groq Whisper — fast, free tier (cloud)
VOICE_TOOLS_OPENAI_KEY=your-key       # OpenAI Whisper — paid (cloud)

# Text-to-Speech (optional — Edge TTS and NeuTTS work without any key)
ELEVENLABS_API_KEY=***                # ElevenLabs — premium quality
# VOICE_TOOLS_OPENAI_KEY above also enables OpenAI TTS
```

## CLI Voice Mode

### Quick Start

Start the interactive CLI with `hermes`, then drive voice mode from inside it with these slash commands:

```
/voice          Toggle voice mode on/off
/voice on       Enable voice mode
/voice off      Disable voice mode
/voice tts      Toggle TTS output
/voice status   Show current state
```

### How It Works

Once `/voice on` is set, the loop is:

1. Start the CLI with `hermes` and enable voice mode with `/voice on`.
2. **Press Ctrl+B** — a beep plays (880 Hz), recording starts.
3. **Speak** — a live audio level bar shows your input: `● [▁▂▃▅▇▇▅▂] ❯`.
4. **Stop speaking** — after 3 seconds of silence, recording auto-stops.
5. **Two beeps** play (660 Hz) confirming the recording ended.
6. Audio is transcribed via Whisper and sent to the agent.
7. If TTS is enabled, the agent's reply is spoken aloud.
8. Recording **automatically restarts** — speak again without pressing any key.

This loop continues until you press **Ctrl+B** during recording (exits continuous mode) or 3 consecutive recordings detect no speech. The record key is configurable via `voice.record_key` in `~/.hermes/config.yaml` (default `ctrl+b`).

### Silence Detection

A two-stage algorithm detects when you have finished speaking:

1. **Speech confirmation** — waits for audio above the RMS threshold (200) for at least 0.3s, tolerating brief dips between syllables.
2. **End detection** — once speech is confirmed, triggers after 3.0 seconds of continuous silence.

If no speech is detected at all for 15 seconds, recording stops automatically. Both `silence_threshold` and `silence_duration` are configurable in `config.yaml`, and the record start/stop beeps can be disabled with `voice.beep_enabled: false`.

### Streaming TTS

When TTS is enabled, the agent speaks its reply **sentence-by-sentence** as it generates text — you don't wait for the full response. The pipeline: buffers text deltas into complete sentences (min 20 chars); strips markdown formatting and `<think>` blocks; then generates and plays audio per sentence in real time.

### Hallucination Filter

Whisper sometimes generates phantom text from silence or background noise ("Thank you for watching", "Subscribe", etc.). The agent filters these out using a set of **26 known hallucination phrases** across multiple languages, plus a regex pattern that catches repetitive variations.

## Configuration Reference

The CLI loop reads three `~/.hermes/config.yaml` blocks. The full schema (all platforms) is owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md); the CLI-relevant knobs are:

```yaml
# Voice recording (CLI)
voice:
  record_key: "ctrl+b"             # Key to start/stop recording
  max_recording_seconds: 120       # Maximum recording length
  auto_tts: false                  # Auto-enable TTS when voice mode starts
  beep_enabled: true               # Play record start/stop beeps
  silence_threshold: 200           # RMS level (0-32767) below which counts as silence
  silence_duration: 3.0            # Seconds of silence before auto-stop

# Speech-to-Text
stt:
  enabled: true                    # false to skip auto-transcription (audio still cached + path passed to agent)
  provider: "local"                # "local" (free) | "groq" | "openai" | "mistral" | "xai"
  local:
    model: "base"                  # tiny, base, small, medium, large-v3

# Text-to-Speech
tts:
  provider: "edge"                 # "edge" (free) | "elevenlabs" | "openai" | "neutts" | ...
  edge:
    voice: "en-US-AriaNeural"      # 322 voices, 74 languages
```

**STT provider comparison** — `local` runs faster-whisper offline (models `base`/`small`/`large-v3`, free, no key, increasing quality/latency); `groq` (`whisper-large-v3-turbo`, ~0.5s, free tier, key required) and `openai` (`whisper-1`/`gpt-4o-transcribe`, paid, key required) are cloud options; `mistral` (`voxtral-mini-latest`) and `xai` (`grok-stt`) are additional paid cloud providers. Provider priority (automatic fallback) is **local > groq > openai**.

**TTS provider comparison** — `edge` (Edge TTS) is Good quality, Free, ~1s latency, no key (the default fallback); `elevenlabs` is Excellent/Paid/~2s/key; `openai` TTS is Good/Paid/~1.5s/key; `neutts` is Good/Free, latency depends on CPU/GPU, no key (uses the `tts.neutts` config block). The full `stt:`/`tts:` provider subsystems are documented in [hermes_stt_transcription](hermes_stt_transcription.md) and [hermes_tts_providers](hermes_tts_providers.md).

## Troubleshooting

CLI-side issues from the source page:

- **"No audio device found" (CLI)** — PortAudio is not installed: `brew install portaudio` (macOS) / `sudo apt install portaudio19-dev` (Ubuntu). Running Hermes inside Docker on a Linux desktop additionally requires host audio-socket access (see the Docker audio bridge notes for a PulseAudio/PipeWire-compatible setup).
- **Whisper returns garbage text** — the hallucination filter catches most cases automatically; if phantom transcripts persist, use a quieter environment, raise `silence_threshold` in config (higher = less sensitive), or try a different STT model.

(Gateway/Discord-VC troubleshooting rows — "Bot doesn't respond in server channels", "Bot joins VC but doesn't hear me", etc. — live in [hermes_voice_gateway_discord_vc](hermes_voice_gateway_discord_vc.md).)

**Source**: `inbox/hermes_agent_docs/user-guide/features/voice-mode.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode
**Last Updated**: 2026-06-19
**Status**: Active
