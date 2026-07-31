---
tags:
  - resource
  - documentation
  - hermes_agent
  - voice
  - transcription
keywords:
  - speech-to-text
  - STT
  - voice message transcription
  - faster-whisper
  - transcription provider plugin
  - automatic fallback chain
topics:
  - Hermes Agent
  - Voice & Audio
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/tts
access_control_group: ["general"]
---

# Hermes Agent — Voice Message Transcription (STT)

## Overview

Voice Message Transcription (STT) is the **inbound-audio half** of Hermes Agent's voice surface: voice messages sent on Telegram, Discord, WhatsApp, Slack, or Signal are automatically transcribed to text and injected into the conversation, so the agent sees the transcript as ordinary text with no extra prompting. It is the mirror image of the [TTS provider subsystem](hermes_tts_providers.md) (the outbound direction) and shares the same three extension layers: a set of built-in providers, a no-Python `stt.providers.<name>: type: command` registry, and a Python plugin path via `register_transcription_provider()`.

STT is **zero-config by default** — local transcription runs out of the box via `faster-whisper`, with an automatic fallback chain to cloud providers (Groq, OpenAI, Mistral, xAI) when a local engine or a configured provider is unavailable. This page is the procedure for setting up, configuring, extending, and reasoning about the fallback behavior of that subsystem. The full `stt:` config block itself is owned by the SP02 messaging-media settings note — this note link-outs to it rather than duplicating it.

## Built-in Providers

Three built-in providers are documented in the headline table; the resolver also recognizes `mistral` and `xai` (configured below):

| Provider | Quality | Cost | API Key |
|----------|---------|------|---------|
| **Local Whisper** (default) | Good | Free | None needed |
| **Groq Whisper API** | Good–Best | Free tier | `GROQ_API_KEY` |
| **OpenAI Whisper API** | Good–Best | Paid | `VOICE_TOOLS_OPENAI_KEY` or `OPENAI_API_KEY` |

**Zero config:** local transcription works out of the box when `faster-whisper` is installed. If that is unavailable, Hermes can also use a local `whisper` CLI from common install locations (like `/opt/homebrew/bin`) or a custom command via `HERMES_LOCAL_STT_COMMAND`.

## Configuration

The `stt:` block selects the active provider and its per-provider model (full block owned by [hermes_messaging_media_settings](hermes_messaging_media_settings.md)):

```yaml
# In ~/.hermes/config.yaml
stt:
  provider: "local"           # "local" | "groq" | "openai" | "mistral" | "xai"
  local:
    model: "base"             # tiny, base, small, medium, large-v3
  openai:
    model: "whisper-1"        # whisper-1, gpt-4o-mini-transcribe, gpt-4o-transcribe
  mistral:
    model: "voxtral-mini-latest"  # voxtral-mini-latest, voxtral-mini-2602
  xai:
    model: "grok-stt"         # xAI Grok STT
```

## Provider Details

- **Local (faster-whisper)** — runs Whisper locally via [faster-whisper](https://github.com/SYSTRAN/faster-whisper), CPU by default and GPU if available. Model sizes range from `tiny` (~75 MB, fastest, basic) through `base` (~150 MB, the default), `small` (~500 MB), `medium` (~1.5 GB), to `large-v3` (~3 GB, slowest, best quality).
- **Groq API** — requires `GROQ_API_KEY`; a good free hosted-STT fallback.
- **OpenAI API** — accepts `VOICE_TOOLS_OPENAI_KEY` first, falls back to `OPENAI_API_KEY`; supports `whisper-1`, `gpt-4o-mini-transcribe`, and `gpt-4o-transcribe`.
- **Mistral API (Voxtral Transcribe)** — requires `MISTRAL_API_KEY`; supports 13 languages, speaker diarization, and word-level timestamps; install with `pip install hermes-agent[mistral]`.
- **xAI Grok STT** — requires `XAI_API_KEY`; posts to `https://api.x.ai/v1/stt` as multipart/form-data. Auto-detection puts it after Groq, so explicitly set `stt.provider: xai` to force it.
- **Custom local CLI fallback** — set `HERMES_LOCAL_STT_COMMAND` to call a local transcription command directly. The template supports `{input_path}`, `{output_dir}`, `{language}`, and `{model}` placeholders; the command must write a `.txt` transcript somewhere under `{output_dir}`.

The `doubao-speech` package (the same one used for Doubao TTS) handles Volcengine ASR over the local-command surface — export `VOLCENGINE_APP_ID` / `VOLCENGINE_ACCESS_TOKEN` plus `HERMES_LOCAL_STT_COMMAND='doubao-speech transcribe {input_path} --out {output_dir}/transcript.txt'` and set `stt.provider: local_command`. Language is auto-detected by the Volcengine bigmodel endpoint.

## Fallback Behavior

If the configured provider isn't available, Hermes automatically falls back along this chain:

- **Local faster-whisper unavailable** → tries a local `whisper` CLI or `HERMES_LOCAL_STT_COMMAND` before cloud providers.
- **Groq key not set** → falls back to local transcription, then OpenAI.
- **OpenAI key not set** → falls back to local transcription, then Groq.
- **Mistral key/SDK not set** → skipped in auto-detect; falls through to the next available provider.
- **Nothing available** → voice messages pass through with an accurate note to the user (instead of a hard error).

## STT Custom Command Providers

For an STT engine that isn't natively supported (Doubao ASR, NVIDIA Parakeet, a whisper.cpp build, a SenseVoice CLI, anything else with a shell command), wire it in as a **command-type provider** with no Python. Hermes runs the shell command against the audio file and reads back the transcript. Declare providers under `stt.providers.<name>` and switch via `stt.provider: <name>` — the same shape as the TTS command-provider registry, adapted for the input=audio → output=transcript direction:

```yaml
stt:
  provider: parakeet                # pick any name under stt.providers
  providers:
    parakeet:
      type: command
      command: "parakeet-asr --model nvidia/parakeet-tdt-0.6b-v2 --in {input_path} --out {output_path}"
      format: txt
      language: en
      timeout: 300

    whispercpp:
      type: command
      command: "whisper-cli -m ~/models/ggml-large-v3.bin -f {input_path} -otxt -of {output_dir}/transcript"
      format: txt

    sensevoice:
      type: command
      command: "sensevoice-cli {input_path} --json | tee {output_path}"
      format: json
```

This complements the legacy `HERMES_LOCAL_STT_COMMAND` escape hatch (still served untouched via the built-in `local_command` path). Use `stt.providers.<name>` when you want **multiple** shell-driven engines, a name selectable via `stt.provider`, or per-provider `language` / `model` / `timeout`.

**Placeholders** (render-time substituted, shell-quoted for bare / single- / double-quoted context, so paths with spaces are safe): `{input_path}` (absolute path to the read-only input audio file), `{output_path}` (where the command writes the transcript), `{output_dir}` (parent of `{output_path}`, handy for whisper-style tools), `{format}` (`txt` / `json` / `srt` / `vtt`), `{language}` (defaults to `en`), and `{model}` (`stt.providers.<name>.model`, empty when unset). Use `{{` and `}}` for literal braces.

**Transcript read-back** after a successful exit: (1) if `{output_path}` exists and is non-empty → read it as UTF-8 text; (2) else if the command wrote to stdout → use that; (3) else → error `"Command STT provider wrote no output file and produced no stdout"`. This supports both file-writing CLIs (`whisper-cli`, `parakeet-asr`) and curl-style one-liners that emit transcript to stdout (`curl … | jq -r .text`). For `format: json` / `srt` / `vtt`, Hermes returns the raw file content as the `transcript` field — extracting `.text` from JSON is out of scope for the runner.

**Optional keys:** `timeout` (default `300` s; the entire process tree is killed on expiry — Unix `start_new_session`, Windows `taskkill /T`), `format` (default `txt`; sets the `{output_path}` extension), `language` (default `en`; defaults to `stt.language` then `en`), and `model` (empty; the `model=` argument to `transcribe_audio()` overrides it).

**Behavior notes:** built-in names always win — declaring `stt.providers.openai: type: command` does NOT override the real OpenAI Whisper handler (the built-in name is short-circuited before the command-provider resolver runs). Process-tree cleanup reaps long-running ASR pipelines that fork model-loading subprocesses. Shell-quoting is automatic: placeholders inside `'…'` get single-quote-safe escaping, inside `"…"` get `$`/`` ` ``/`"` escaping, and outside quotes get `shlex.quote` — don't pre-quote values.

**Security:** the shell command runs under the same user as Hermes with full filesystem access — the same trust model as `tts.providers.<name>: type: command` and `HERMES_LOCAL_STT_COMMAND`. Only declare command providers from sources you trust.

## Python Plugin Providers (STT)

For STT engines that aren't built-in AND can't be a single shell command (need a Python SDK, OAuth-refreshing auth, streaming chunks, etc.), register a Python plugin via `ctx.register_transcription_provider()`. The plugin **coexists with** the 6 built-in providers (`local`, `local_command`, `groq`, `openai`, `mistral`, `xai`) and the command-provider registry: built-ins keep their native implementations and always win on name collision; command providers win over a same-name plugin (config is more local than a plugin install).

**When to pick which:** a single shell command that takes audio and emits text → `stt.providers.<name>: type: command`; only the legacy single-command escape hatch → `HERMES_LOCAL_STT_COMMAND`; a Python SDK with no CLI, OAuth-refresh, streaming chunks, or voice-list metadata → `register_transcription_provider()` plugin; a built-in already covers it → just set `stt.provider: <name>`.

**Resolution order:** (1) `stt.provider` is a built-in name → built-in dispatch, **always wins**; (2) matches `stt.providers.<name>` with `command:` set → command-provider runner, wins over a same-name plugin; (3) matches a plugin-registered `TranscriptionProvider` → plugin dispatch — if `is_available()` returns `False` (missing creds/SDK) the call surfaces an unavailability error envelope identifying the plugin (not the generic "No STT provider available"), otherwise the plugin's `transcribe()` is called with `model` (from the `model=` arg, falling back to `stt.<provider>.model`) and `language` (from `stt.<provider>.language`); (4) no match → "No STT provider available" error.

**Per-provider config namespace:** plugins read their config from `stt.<provider>` in `config.yaml`, mirroring how built-ins read `stt.openai.model` / `stt.mistral.model`. The dispatcher forwards `model` and `language` from this section; everything else the plugin reads itself. The minimal plugin returns the standard transcribe envelope rather than raising:

```python
from agent.transcription_provider import TranscriptionProvider


class MySTTProvider(TranscriptionProvider):
    @property
    def name(self) -> str:
        return "my-stt"  # what stt.provider matches against

    @property
    def display_name(self) -> str:
        return "My Custom STT"

    def is_available(self) -> bool:
        # Return False when credentials/deps are missing — picker skips
        # this row but the dispatcher still routes here on explicit config.
        import os
        return bool(os.environ.get("MY_STT_API_KEY"))

    def transcribe(self, file_path, *, model=None, language=None, **extra):
        # Return the standard transcribe envelope:
        #   {"success": bool, "transcript": str, "provider": str, "error": str}
        # Do NOT raise — convert exceptions to the error envelope so the
        # gateway/CLI caller sees a consistent shape on failure.
        try:
            import my_stt_sdk
            client = my_stt_sdk.Client()
            text = client.transcribe(open(file_path, "rb"))
            return {
                "success": True,
                "transcript": text,
                "provider": "my-stt",
            }
        except Exception as exc:
            return {
                "success": False,
                "transcript": "",
                "error": f"my-stt failed: {exc}",
                "provider": "my-stt",
            }


def register(ctx):
    ctx.register_transcription_provider(MySTTProvider())
```

Drop this in `~/.hermes/plugins/my-stt/` alongside a `plugin.yaml` (`name` / `version` / `description`), enable it (`hermes plugins enable my-stt`), set `stt.provider: my-stt` in `config.yaml`, and voice-message transcription routes through your plugin. **Optional hooks** for richer integration: `list_models()` → `{id, display, languages, max_audio_seconds}` dicts; `default_model()` → string returned when the user doesn't override the model; `get_setup_schema()` → `{name, badge, tag, env_vars: [...]}` to power picker rows in `hermes tools` / `hermes setup` (the STT picker category isn't shipped yet — this metadata is forward-compatible). See `agent/transcription_provider.py` for the full ABC including docstrings.

**Source**: `inbox/hermes_agent_docs/user-guide/features/tts.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/tts
**Last Updated**: 2026-06-19
**Status**: Active
