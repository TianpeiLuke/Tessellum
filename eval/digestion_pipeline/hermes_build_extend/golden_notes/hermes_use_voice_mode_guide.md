---
tags:
  - resource
  - documentation
  - hermes_agent
  - voice_mode
  - how_to
keywords:
  - hermes voice mode
  - cli microphone loop
  - voice replies telegram discord
  - discord voice channel bot
  - stt tts providers
  - voice config yaml
  - silence threshold tuning
  - voice failure modes
topics:
  - Hermes Agent
  - Voice Mode
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes
access_control_group: ["general"]
---

# Use Voice Mode with Hermes

## Overview

This is the practical **how-to guide** for setting up and running Hermes voice mode end-to-end — the operational companion to the Voice Mode feature reference, which explains *what* voice mode can do while this guide shows how to actually use it well. Voice mode turns Hermes into a hands-free assistant, and the page frames it as three genuinely different voice experiences rather than one feature: an interactive CLI microphone loop, spoken voice replies inside a chat platform, and a live Discord voice-channel bot. Each experience is the same underlying STT → agent → TTS pipeline behind a different front-end. The guide's spine is a deliberate "get text working first, add voice replies second, move to Discord voice channels last" progression, layered through extras installation, system dependencies, STT/TTS provider selection, a recommended config, then per-use-case operation, tuning, and failure-mode triage. Nous Portal is called out as the zero-extra-credential path because it bundles both the LLM and TTS through one OAuth.

## What voice mode is good for

Voice mode is especially useful when you want a hands-free CLI workflow, spoken responses in Telegram or Discord, Hermes sitting in a Discord voice channel for live conversation, or quick idea capture / debugging / back-and-forth while walking around instead of typing.

## Choose your voice mode setup

There are three different voice experiences in Hermes:

| Mode | Best for | Platform |
|---|---|---|
| Interactive microphone loop | Personal hands-free use while coding or researching | CLI |
| Voice replies in chat | Spoken responses alongside normal messaging | Telegram, Discord |
| Live voice channel bot | Group or personal live conversation in a VC | Discord voice channels |

A good path is: (1) get text working first, (2) enable voice replies second, (3) move to Discord voice channels last if you want the full experience.

## Step 1: make sure normal Hermes works first

Before touching voice mode, verify Hermes starts, your provider is configured, and the agent can answer text prompts normally. Run `hermes`, then ask something simple like *"What tools do you have available?"*. If text mode is not solid yet, fix it first before layering voice on top.

## Step 2: install the right extras

The voice experiences depend on extras for the relevant capability — CLI microphone + playback, messaging platforms, or premium TTS:

```bash
pip install "hermes-agent[voice]"        # CLI microphone + playback
pip install "hermes-agent[messaging]"    # Messaging platforms
pip install "hermes-agent[tts-premium]"  # Premium ElevenLabs TTS
pip install "hermes-agent[all]"          # Everything
```

Local NeuTTS is an optional add-on installed separately with `python -m pip install -U neutts[all]`.

## Step 3: install system dependencies

```bash
# macOS
brew install portaudio ffmpeg opus
brew install espeak-ng

# Ubuntu / Debian
sudo apt install portaudio19-dev ffmpeg libopus0
sudo apt install espeak-ng
```

Why these matter: `portaudio` → microphone input / playback for CLI voice mode; `ffmpeg` → audio conversion for TTS and messaging delivery; `opus` → Discord voice codec support; `espeak-ng` → phonemizer backend for NeuTTS.

## Step 4: choose STT and TTS providers

Hermes supports both local and cloud speech stacks. The **easiest / cheapest** start is local STT with free Edge TTS (`stt` provider `local`, `tts` provider `edge`). Add cloud STT keys (`GROQ_API_KEY`, `VOICE_TOOLS_OPENAI_KEY`) and premium TTS (`ELEVENLABS_API_KEY`) to `~/.hermes/.env` only if you need them.

Speech-to-text picks: `local` → best default for privacy and zero-cost use; `groq` → very fast cloud transcription; `openai` → good paid fallback.

Text-to-speech picks: `edge` → free and good enough for most users; `neutts` → free local/on-device TTS; `elevenlabs` → best quality; `openai` → good middle ground; `mistral` → multilingual, native Opus.

If you run `hermes setup` and choose NeuTTS, the wizard checks whether `neutts` is installed; if it is missing it offers to install it (and `espeak-ng` via your platform package manager) by running `python -m pip install -U neutts[all]`, and falls back to Edge TTS if you skip or it fails.

## Step 5: recommended config

A conservative default for most people uses local STT and free Edge TTS:

```yaml
voice:
  record_key: "ctrl+b"
  max_recording_seconds: 120
  auto_tts: false
  beep_enabled: true
  silence_threshold: 200
  silence_duration: 3.0

stt:
  provider: "local"
  local:
    model: "base"

tts:
  provider: "edge"
  edge:
    voice: "en-US-AriaNeural"
```

To switch to local TTS instead, replace the `tts` block with a `neutts` provider block (`ref_audio`/`ref_text` empty, `model: neuphonic/neutts-air-q4-gguf`, `device: cpu`).

## Use case 1: CLI voice mode

Start Hermes (`hermes`), then inside the CLI turn it on with `/voice on`. The recording flow with the default `Ctrl+B` key is: press `Ctrl+B` → speak → wait for silence detection to stop recording automatically → Hermes transcribes and responds → if TTS is on it speaks the answer → the loop can automatically restart for continuous use. The useful command set is `/voice`, `/voice on`, `/voice off`, `/voice tts`, `/voice status`. Strong CLI workflows include walk-up debugging (continue hands-free with follow-ups like "Read the last error again", "Explain the root cause in simpler terms", "Now give me the exact fix"), research/brainstorming while walking around, and accessibility / low-typing sessions.

## Tuning CLI behavior

Three knobs in the `voice` config block tune the mic loop. If Hermes starts/stops too aggressively, raise `silence_threshold` (higher = less sensitive). If you pause a lot between sentences, raise `silence_duration`. If `Ctrl+B` conflicts with your terminal or tmux habits, change `record_key`:

```yaml
voice:
  silence_threshold: 250
  silence_duration: 4.0
  record_key: "ctrl+space"
```

## Use case 2: voice replies in Telegram or Discord

This mode is simpler than full voice channels — Hermes stays a normal chat bot but can speak replies. Start the gateway with `hermes gateway`, then inside Telegram or Discord turn on voice replies with `/voice on` or `/voice tts`. The three reply modes are: `off` (text only), `voice_only` (speak only when the user sent voice), and `all` (speak every reply). Use `/voice on` if you want spoken replies only for voice-originating messages, and `/voice tts` if you want a full spoken assistant all the time. This powers a Telegram phone assistant (send voice notes, get quick spoken replies while away from your machine) and Discord DMs with spoken output for private interaction.

## Use case 3: Discord voice channels

This is the most advanced mode: Hermes joins a Discord VC, listens to user speech, transcribes it, runs the normal agent pipeline, and speaks replies back into the channel. In addition to the normal text-bot setup, the bot needs the **Connect**, **Speak**, and preferably **Use Voice Activity** permissions, plus the privileged **Presence**, **Server Members**, and **Message Content** intents enabled in the Developer Portal.

In a text channel where the bot is present, control it with `/voice join`, `/voice leave`, and `/voice status`. When joined, users speak in the VC, Hermes detects speech boundaries, transcripts are posted in the associated text channel (the one where `/voice join` was issued), and Hermes responds in text and audio. Best practices: keep `DISCORD_ALLOWED_USERS` tight, use a dedicated bot/testing channel at first, and verify STT/TTS work in ordinary text-chat voice mode before trying VC mode.

## Voice quality recommendations

- **Best quality:** STT local `large-v3` or Groq `whisper-large-v3`; TTS ElevenLabs.
- **Best speed / convenience:** STT local `base` or Groq; TTS Edge.
- **Best zero-cost:** STT local; TTS Edge.

## Common failure modes

- **"No audio device found"** → install `portaudio`.
- **"Bot joins but hears nothing"** → check your Discord user ID is in `DISCORD_ALLOWED_USERS`, you are not muted, privileged intents are enabled, and the bot has Connect/Speak permissions.
- **"It transcribes but does not speak"** → check TTS provider config, API key / quota for ElevenLabs or OpenAI, and the `ffmpeg` install for Edge conversion paths.
- **"Whisper outputs garbage"** → try a quieter environment, higher `silence_threshold`, a different STT provider/model, and shorter, clearer utterances.
- **"It works in DMs but not in server channels"** → that is often mention policy; by default the bot needs an `@mention` in Discord server text channels unless configured otherwise.

## Suggested first-week setup

The shortest path to success: (1) get text Hermes working, (2) install `hermes-agent[voice]`, (3) use CLI voice mode with local STT + Edge TTS, (4) then enable `/voice on` in Telegram or Discord, (5) only after that, try Discord VC mode. That progression keeps the debugging surface small.

## Related Notes

**Terms**
- [term_voice_wake](../../term_dictionary/term_voice_wake.md) — wake-word / voice-activation concept; relevance: voice mode is a multimodal STT→agent→TTS loop over the harness; the CLI mic loop and Discord-VC bot are alternate front-ends to the same session pipeline.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-input/output modeling; relevance: voice mode is a multimodal STT→agent→TTS loop.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agent class; relevance: the transcribed prompt runs the same autonomous agent loop.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the agent runtime harness; relevance: the CLI mic loop and Discord-VC bot are alternate front-ends to the same harness session pipeline.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session/conversation state; relevance: the voice front-ends share one persisted session pipeline.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — LLM tool/function invocation; relevance: the spoken prompt drives the same tool-calling loop a text prompt would.
- [term_persona](../../term_dictionary/term_persona.md) — agent identity/persona; relevance: the persona shapes spoken voice replies.
- [term_computer_vision](../../term_dictionary/term_computer_vision.md) — vision input modality; relevance: a sibling multimodal input mode to the STT voice input. (+fin: term_voice_mode, term_text_to_speech, term_speech_to_text [own SP08])

**Code-Repos**
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — voice-mode tool + transcription (STT) + TTS routing; relevance: `tools_voice_mode`/`tools_transcription`/`tools_tts_routing` (the STT/TTS provider picks) live here.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `/voice` CLI command + mic loop + silence tuning; relevance: Use-case-1 CLI mic loop and the `/voice` command set are implemented here.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — Discord/Telegram voice replies + Discord-VC; relevance: Use-cases 2–3 (messaging voice replies, Discord voice channel) route through the gateway.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — STT/TTS provider adapters (groq/openai/edge/elevenlabs/neutts); relevance: the Step-4 provider-pick matrix maps to these adapters.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the agent run between STT and TTS; relevance: the transcribed prompt runs the AIAgent loop, then the reply is spoken.

**Snippets**
- [cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — CLI `/voice` command implementation; relevance: the `/voice` command set the three voice experiences drive.
- [tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the core voice tool behind the mic loop.
- [tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — STT transcription path; relevance: the speech-to-text step the provider picks select.
- [tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: the text-to-speech step the provider picks select.
- [core_run_agent_cli](../../code_snippets/snippet_hermes_agent_core_run_agent_cli.md) — agent-run entry point; relevance: the transcribed prompt runs the agent here.
- [gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: spoken replies are delivered through the gateway.
- [gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord connect / VC join; relevance: Use-case-3 `/voice join` connects to the voice channel.
- [cli_setup_skills](../../code_snippets/snippet_hermes_agent_cli_setup_skills.md) — setup wizard skill step; relevance: the `hermes setup` NeuTTS install path.
- [cli_setup_verify](../../code_snippets/snippet_hermes_agent_cli_setup_verify.md) — setup verify step; relevance: the Step-1 "make sure normal Hermes works first" verification.
- [core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session-persist conversation loop; relevance: the persisted session the voice front-ends share.

**Docs**
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the messaging/voice tips (`/sethome`, DM pairing) that apply to voice replies.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the MCP tools the agent calls inside a voice session.
- [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: skills invoked by a voice command.
- [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — the surface map; relevance: the TTS/STT command-template drop-in surface this guide configures.
- [hermes_python_library_guide](hermes_python_library_guide.md) — embedding `AIAgent`; relevance: the programmatic alternative to the CLI mic loop.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — CC voice dictation (STT front-end); relevance: closest analogue to the CLI mic loop.
- [cc_computer_use](../claude_code/cc_computer_use.md) — CC multimodal input; relevance: analogue to the multimodal STT→agent loop.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — CC tool catalog; relevance: analogue to the voice/transcription tools.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — front-ends sharing one agent session; relevance: analogue to the CLI/Discord/messaging front-ends over one pipeline.
- [cc_effective_prompting](../claude_code/cc_effective_prompting.md) — spoken-prompt clarity; relevance: analogue to the voice quality/failure-mode guidance.
- [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — CC full tool catalog; relevance: analogue to the STT/TTS provider/tool catalog this guide selects from.
- [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — CC input modes; relevance: analogue to the voice vs text input mode choice + silence tuning.
- **[OpenClaw — macOS Voice Wake and Push-to-Talk](../openclaw/oc_platforms_mac_voicewake.md)** — This note covers OpenClaw's macOS **Voice Wake & Push-to-Talk** feature: the two hands-free voice-capture modes the mac app exposes, the recognizer runtime…

**Source**: https://hermes-agent.nousresearch.com/docs/guides/use-voice-mode-with-hermes
**Last Updated**: 2026-06-19
**Status**: Active
