---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - voice
keywords:
  - openclaw voice wake macos
  - push to talk right option
  - swabbletriggerwords wake word
  - voicewakeruntime recognizer
  - voicewakeforwarder transcript
  - voice settings macos 26
  - forward transcript active gateway
  - last-used main provider reply
topics:
  - OpenClaw
  - macOS Voice Wake
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/voicewake
access_control_group: ["general"]
---

# OpenClaw — macOS Voice Wake and Push-to-Talk

## Overview

This note covers OpenClaw's macOS **Voice Wake & Push-to-Talk** feature: the two hands-free voice-capture modes the mac app exposes, the recognizer runtime behavior, lifecycle invariants, settings, and how captured transcripts forward to the agent and replies route back. It mirrors the `platforms/mac/voicewake` source page. The feature lets a user speak to the agent either via an always-on wake word or by holding a hotkey, transcribing the spoken command and forwarding it to the active gateway/agent over the same local-vs-remote mode the rest of the mac app uses.

## Requirements

Voice Wake and push-to-talk require **macOS 26 or newer**. On older macOS versions the controls are hidden from the Voice settings page, which instead shows the macOS 26 requirement.

## Modes

The feature offers two capture modes:

- **Wake-word mode** (default): an always-on Speech recognizer waits for trigger tokens (`swabbleTriggerWords`). On a match it starts capture, shows the overlay with partial text, and auto-sends after silence.
- **Push-to-talk (Right Option hold)**: hold the right Option key to capture immediately — no trigger word needed. The overlay appears while the key is held; releasing finalizes and forwards after a short delay so the user can tweak the text first.

## Runtime behavior (wake-word)

The wake-word path is governed by a recognizer with several timing and restart invariants:

- The Speech recognizer lives in `VoiceWakeRuntime`.
- The trigger only fires when there is a **meaningful pause** between the wake word and the next word (~0.55s gap). The overlay/chime can start on the pause even before the command itself begins.
- Silence windows: **2.0s** when speech is flowing, **5.0s** if only the trigger was heard.
- Hard stop: **120s**, to prevent runaway sessions.
- Debounce between sessions: **350ms**.
- The overlay is driven via `VoiceWakeOverlayController` with committed/volatile coloring of the partial text.
- After a send, the recognizer restarts cleanly to listen for the next trigger.

## Lifecycle invariants

Two invariants keep the recognizer reliably available:

- If Voice Wake is enabled and permissions are granted, the wake-word recognizer should be listening (except during an explicit push-to-talk capture).
- Overlay visibility — including a manual dismiss via the X button — must never prevent the recognizer from resuming.

## Sticky overlay failure mode (previous)

Previously, if the overlay got stuck visible and the user manually closed it, Voice Wake could appear "dead": the runtime's restart attempt could be blocked by overlay visibility and no subsequent restart was scheduled. The hardening that addresses this is:

- Wake-runtime restart is no longer blocked by overlay visibility.
- Overlay-dismiss completion triggers a `VoiceWakeRuntime.refresh(...)` via `VoiceSessionCoordinator`, so a manual X-dismiss always resumes listening.

## Push-to-talk specifics

The push-to-talk (PTT) path has its own capture and permission details:

- Hotkey detection uses a global `.flagsChanged` monitor for **right Option** (`keyCode 61` + `.option`). The app only observes events (no swallowing).
- The capture pipeline lives in `VoicePushToTalk`: it starts Speech immediately, streams partials to the overlay, and calls `VoiceWakeForwarder` on release.
- When push-to-talk starts, the wake-word runtime is paused to avoid dueling audio taps; it restarts automatically after release.
- Permissions: PTT requires Microphone + Speech; seeing the key events additionally needs Accessibility / Input Monitoring approval.
- External keyboards: some may not expose right Option as expected — offer a fallback shortcut if users report misses.

## User-facing settings

The Voice settings page exposes these controls:

- **Voice Wake** toggle: enables the wake-word runtime.
- **Hold Right Option to talk**: enables the push-to-talk monitor.
- Language and mic pickers, a live level meter, a trigger-word table, and a tester (local-only; does **not** forward).
- The mic picker preserves the last selection if a device disconnects, shows a disconnected hint, and temporarily falls back to the system default until the device returns.
- **Sounds**: chimes on trigger-detect and on send, defaulting to the macOS "Glass" system sound. The user can pick any `NSSound`-loadable file (e.g. MP3/WAV/AIFF) for each event, or choose **No Sound**.

## Forwarding behavior

Once a transcript is captured it is routed to the agent and a reply comes back through the user's messaging provider:

- When Voice Wake is enabled, transcripts are forwarded to the active gateway/agent — the same local-vs-remote mode used by the rest of the mac app.
- Replies are delivered to the **last-used main provider** (WhatsApp / Telegram / Discord / WebChat). If delivery fails, the error is logged and the run is still visible via WebChat / session logs.

## Forwarding payload

`VoiceWakeForwarder.prefixedTranscript(_:)` prepends the machine hint before sending. This forwarder is shared between the wake-word and push-to-talk paths.

## Quick verification

To verify the feature works:

- Toggle push-to-talk on, hold Right Option, speak, then release: the overlay should show partials and then send.
- While holding, the menu-bar "ears" should stay enlarged (uses `triggerVoiceEars(ttl:nil)`); they drop back down after release.

**Source**: OpenClaw documentation — `platforms/mac/voicewake` (mirror `inbox/openclaw_docs/platforms/mac/voicewake.md`)
**Last Updated**: 2026-06-22
**Status**: Active
