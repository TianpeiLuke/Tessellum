---
tags:
  - resource
  - documentation
  - claude_code
  - interactive_mode
  - voice_dictation
keywords:
  - voice dictation
  - push to talk
  - hold to record
  - tap to record
  - dictation language
  - voice pushtotalk binding
  - microphone permission
  - speech to text
topics:
  - Claude Code
  - Interactive Mode
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/voice-dictation
access_control_group: ["general"]
---

# Claude Code — Voice Dictation

## Overview

Voice dictation lets you **speak prompts instead of typing them** in the Claude Code CLI. Speech is transcribed live into the prompt input, dimmed until finalized, so you can mix voice and typing in the same message. You enable it with `/voice`, then either **hold a key while you speak** (hold mode, push-to-talk) or **tap once to start and again to send** (tap mode). Recorded audio is streamed to Anthropic's servers for transcription — it is not processed locally.

This note is the procedure for setting up and using dictation: requirements, enabling, the two recording modes, language selection, rebinding the dictation key, and troubleshooting. Voice dictation requires Claude Code v2.1.69 or later; tap mode requires v2.1.116 or later (check with `claude --version`). It also works in agent view — hold or tap your push-to-talk key while the dispatch input or a peek-panel reply is focused to dictate to a background session.

## Requirements

Voice dictation streams recorded audio to Anthropic's servers for transcription (audio is **not** processed locally). The speech-to-text service is only available when you authenticate with a **Claude.ai account**. It is **not** available when Claude Code is configured to use an Anthropic API key directly, Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, and it is not available when your organization has HIPAA compliance enabled. Transcription does not consume Claude messages or tokens and does not count toward the limits shown in `/usage`. See [data usage](https://code.claude.com/docs/en/data-usage) for how Anthropic handles your data.

It also needs **local microphone access**, so it does not work in remote environments such as [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) or SSH sessions. In WSL, it requires WSLg for audio access (WSLg ships with WSL2 installed from the Microsoft Store on Windows 10/11); on WSL1, run Claude Code in native Windows instead. Audio recording uses a built-in native module on macOS, Linux, and Windows. On Linux, if the native module cannot load, Claude Code falls back to `arecord` (ALSA utils) or `rec` (SoX); if neither is available, `/voice` prints an install command for your package manager. The [VS Code extension](https://code.claude.com/docs/en/vs-code) also supports voice dictation with the same Claude.ai requirement, but not in VS Code Remote sessions (SSH, Dev Containers, Codespaces), because the microphone is on your local machine while the extension runs on the remote host.

## Enable voice dictation

Run `/voice` to enable dictation. The first time you enable it, Claude Code runs a microphone check; on macOS this triggers the system microphone permission prompt for your terminal if it has never been granted.

```
/voice
Voice mode enabled (hold). Hold Space to record. Dictation language: en (/config to change).
```

`/voice` accepts an optional mode argument:

| Command | Effect |
| :------ | :----- |
| `/voice` | Toggle on or off, keep the current mode |
| `/voice hold` | Enable in hold mode |
| `/voice tap` | Enable in tap mode |
| `/voice off` | Disable |

Voice dictation persists across sessions; set it directly in your [user settings file](https://code.claude.com/docs/en/settings) instead of running `/voice`:

```json
{
  "voice": {
    "enabled": true,
    "mode": "tap"
  }
}
```

While enabled, the input footer shows a `hold Space to speak` hint when the prompt is empty (the hint reflects your current `voice:pushToTalk` binding and updates if you rebind it; it does not appear with a [custom status line](https://code.claude.com/docs/en/statusline)). Transcription is tuned for coding vocabulary in both modes — terms like `regex`, `OAuth`, `JSON`, and `localhost` are recognized correctly, and your current project name and git branch name are added as recognition hints automatically.

## Hold to record

Hold mode is push-to-talk (the default): recording runs while you hold the key and stops when you release. Hold `Space` to start. Claude Code detects a held key by watching for **rapid key-repeat events** from your terminal, so there is a brief warmup before recording begins — the footer shows `keep holding…` during warmup, then switches to a live waveform once active. The first couple of key-repeat characters type into the input during warmup and are removed automatically when recording activates; a single `Space` tap still types a space, since hold detection only triggers on rapid repeat. (To skip the warmup, switch to tap mode or rebind to a modifier combination like `meta+k`, which starts recording on the first keypress.)

Your speech appears in the prompt as you speak, dimmed until finalized. Release `Space` to stop recording and finalize; the transcript is inserted at your cursor position and the cursor stays at the end of the inserted text, so you can mix typing and dictation in any order:

```
> refactor the auth middleware to ▮
  # hold Space, speak "use the new token validation helper"
> refactor the auth middleware to use the new token validation helper▮
```

By default, releasing the key inserts the transcript and waits for you to press `Enter`. Set `"autoSubmit": true` in the `voice` settings object to send automatically on release, as long as the transcript is at least three words long.

## Tap to record and send

Tap mode toggles recording with a single keypress: tap once to start, speak, then tap again to send. There is **no warmup**, and you do not keep the key held. Enable it with `/voice tap`. With the prompt input empty, tap `Space` to start (the footer shows a live waveform); tap `Space` again to stop. Claude Code inserts the transcript and submits the prompt automatically when it is at least three words long — shorter transcripts are inserted but not submitted, so an accidental tap does not send a stray word. The first tap only starts recording when the prompt input is empty (so you can still type spaces while composing); the second tap stops recording regardless of input contents. Recording also stops automatically after **15 seconds of silence** or **two minutes** total.

## Change the dictation language

Voice dictation uses the same [`language` setting](https://code.claude.com/docs/en/settings) that controls Claude's response language. If that setting is empty, dictation defaults to English (in the VS Code extension, an empty `language` falls back to VS Code's `accessibility.voice.speechLanguage` before defaulting to English). Set the language in `/config` or directly in settings, using either the [BCP 47 language code](https://en.wikipedia.org/wiki/IETF_language_tag) or the language name:

```json
{
  "language": "japanese"
}
```

Supported dictation languages (code in parentheses): Czech (`cs`), Danish (`da`), Dutch (`nl`), English (`en`), French (`fr`), German (`de`), Greek (`el`), Hindi (`hi`), Indonesian (`id`), Italian (`it`), Japanese (`ja`), Korean (`ko`), Norwegian (`no`), Polish (`pl`), Portuguese (`pt`), Russian (`ru`), Spanish (`es`), Swedish (`sv`), Turkish (`tr`), Ukrainian (`uk`). If your `language` setting is not in the supported list, `/voice` warns you on enable and falls back to English for dictation; Claude's text responses are not affected by this fallback.

## Rebind the dictation key

The dictation key is bound to `voice:pushToTalk` in the `Chat` context and defaults to `Space`; the same binding controls both hold and tap modes. Rebind it in [`~/.claude/keybindings.json`](https://code.claude.com/docs/en/keybindings):

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "meta+k": "voice:pushToTalk",
        "space": null
      }
    }
  ]
}
```

The `voice:pushToTalk` action uses one key at a time. When you bind a custom key, it replaces the default `Space` binding rather than adding a second trigger, so the `"space": null` line above is for clarity and can be omitted without changing behavior. In hold mode, avoid binding a bare letter key like `v`, since hold detection relies on key-repeat and the letter types into the prompt during warmup — use `Space` or a modifier combination like `meta+k` (no warmup). Tap mode has no warmup, so most keys work. Some keys are not delivered to terminal applications and cannot be bound at all (e.g. `Caps Lock` shows an error). See [customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings) for the full keybinding syntax and the list of reserved shortcuts.

## Troubleshooting

Common issues when dictation does not activate or record:

- **`Voice mode requires a Claude.ai account`** — you are authenticated with an API key or a third-party provider. Run `/login` to sign in with a Claude.ai account.
- **`Microphone access is denied`** — grant microphone permission to your terminal in system settings. macOS: System Settings → Privacy & Security → Microphone, enable your terminal app, then run `/voice` again. Windows: Settings → Privacy & security → Microphone, turn on access for desktop apps, then run `/voice` again. If your terminal isn't listed on macOS, see the section below.
- **`No audio recording tool found` on Linux** — the native module could not load and no fallback is installed. Install SoX with the command shown in the error, e.g. `sudo apt-get install sox`.
- **`Voice mode could not find a working audio recorder in WSL`** — WSLg routes audio through PulseAudio, so SoX needs its PulseAudio backend: `sudo apt install sox libsox-fmt-pulse`. Installing `sox` alone pulls in the ALSA backend, which cannot record on WSL (no `/dev/snd` device).
- **`Voice input is failing repeatedly and has been paused`** — dictation hit several start-up failures in a row and stopped attempting new sessions until one succeeds. This usually means the host can't capture audio (headless server, remote shell with no passthrough, or denied permission). Confirm a working input device, fix the underlying cause, then trigger voice again.
- **Nothing happens when holding `Space` in hold mode** — watch the input while you hold. Spaces accumulating means dictation is off (`/voice hold`). One or two spaces then nothing means hold detection isn't triggering: it requires terminal key-repeat events, so it fails if key-repeat is disabled at the OS level — switch to tap mode (`/voice tap`).
- **Tapping `Space` types a space instead of recording in tap mode** — the first tap only starts recording when the input is empty. Clear the input first, or confirm tap mode with `/voice tap`.
- **`No audio detected from microphone`** — recording started but captured silence. Confirm the correct input device is the system default and its level is not muted (Windows: Settings → System → Sound → Input; macOS: System Settings → Sound → Input).
- **`No speech detected`** — audio reached the service but no words were recognized. Speak closer to the mic, reduce noise, and confirm your dictation language matches what you're speaking.
- **Transcription is garbled or in the wrong language** — dictation defaults to English; set your language in `/config` first.

### Terminal not listed in macOS Microphone settings

If your terminal does not appear under System Settings → Privacy & Security → Microphone, there is no toggle to enable; reset the permission state so the next `/voice` run triggers a fresh prompt:

1. **Reset the microphone permission** — run `tccutil reset Microphone <bundle-id>` with your terminal's identifier: `com.apple.Terminal` for the built-in Terminal, `com.googlecode.iterm2` for iTerm2; for others, look up the ID with `osascript -e 'id of app "AppName"'`. (Running `tccutil reset Microphone` *without* a bundle ID revokes microphone access from every app on your Mac, including Zoom or Slack, so each must re-request access — don't run it during an active call.)
2. **Quit and relaunch your terminal** — macOS won't re-prompt a running process. Quit with Cmd+Q (not just closing windows), then reopen.
3. **Trigger a fresh prompt** — start Claude Code and run `/voice`; macOS prompts for microphone access, allow it.

**Source**: https://code.claude.com/docs/en/voice-dictation
**Last Updated**: 2026-06-13
**Status**: Active
