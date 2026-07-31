---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - voice
keywords:
  - openclaw voice overlay
  - macos voice overlay lifecycle
  - wake-word push-to-talk overlap
  - voicesessioncoordinator voicesession
  - per-capture session token
  - voicewake overlay logging
  - push-to-talk adopt overlay text
  - send-or-dismiss cooldown
topics:
  - OpenClaw
  - Voice Overlay
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/voice-overlay
access_control_group: ["general"]
---

# OpenClaw — macOS Voice Overlay Lifecycle (Wake-Word ↔ Push-to-Talk)

## Overview

This note covers the OpenClaw macOS app's **voice overlay lifecycle** — the design that keeps the on-screen voice overlay predictable when wake-word capture and push-to-talk (PTT) capture overlap. It mirrors the `platforms/mac/voice-overlay.md` source page, whose stated goal is "keep the voice overlay predictable when wake-word and push-to-talk overlap" for macOS app contributors. The note explains the current intent (PTT adopting an existing wake overlay instead of resetting it), what was implemented Dec 9, 2025 (per-capture session tokens that drop stale callbacks, PTT text adoption, `voicewake.*` logging), the planned `VoiceSessionCoordinator` / `VoiceSession` / `VoiceSessionPublisher` actor model and unified send path, the `log stream` debugging checklist, and the suggested migration steps. Wake-word runtime internals proper are documented separately (linked, not duplicated here).

## Current Intent

The page states two behaviors. First, **if the overlay is already visible from wake-word and the user presses the hotkey, the hotkey session _adopts_ the existing text instead of resetting it**: the overlay stays up while the hotkey is held, and on release it will *send if there is trimmed text, otherwise dismiss*. Second, the two capture sources keep distinct send triggers — **wake-word alone still auto-sends on silence, push-to-talk sends immediately on release**.

## Implemented (Dec 9, 2025)

As of Dec 9, 2025 the source records three implemented behaviors. (1) **Overlay sessions now carry a token per capture** (wake-word or push-to-talk); partial / final / send / dismiss / level updates are *dropped when the token doesn't match*, avoiding stale callbacks. (2) **Push-to-talk adopts any visible overlay text as a prefix** — pressing the hotkey while the wake overlay is up keeps the text and appends new speech — and it *waits up to 1.5s for a final transcript before falling back to the current text*. (3) **Chime/overlay logging is emitted at `info`** in categories `voicewake.overlay`, `voicewake.ptt`, and `voicewake.chime`, logging session start, partial, final, send, dismiss, and chime reason.

## Next Steps (Planned Session Model)

The page proposes a planned actor-based session model, broken into five parts.

**1. `VoiceSessionCoordinator` (actor).** Owns exactly one `VoiceSession` at a time. Its token-based API is `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, and `applyCooldown`. It *drops callbacks that carry stale tokens*, preventing old recognizers from reopening the overlay.

**2. `VoiceSession` (model).** Its fields are `token`, `source` (`wakeWord` | `pushToTalk`), committed/volatile text, chime flags, timers (auto-send, idle), `overlayMode` (`display` | `editing` | `sending`), and a cooldown deadline.

**3. Overlay binding.** `VoiceSessionPublisher` (an `ObservableObject`) mirrors the active session into SwiftUI. `VoiceWakeOverlayView` renders only via the publisher — *it never mutates global singletons directly*. Overlay user actions (`sendNow`, `dismiss`, `edit`) call back into the coordinator with the session token.

**4. Unified send path.** On `endCapture`: if trimmed text is empty → dismiss; else `performSend(session:)` (plays the send chime once, forwards, dismisses). Push-to-talk applies no delay; wake-word applies an optional delay for auto-send. After push-to-talk finishes, a *short cooldown* is applied to the wake runtime so wake-word doesn't immediately retrigger.

**5. Logging.** The coordinator emits `.info` logs in subsystem `ai.openclaw`, categories `voicewake.overlay` and `voicewake.chime`. Key events: `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, and `cooldown`.

## Debugging Checklist

The page gives a contributor checklist for diagnosing a sticky/stuck overlay. First, stream logs while reproducing the issue:

```bash
sudo log stream --predicate 'subsystem == "ai.openclaw" AND category CONTAINS "voicewake"' --level info --style compact
```

Then verify the invariants: there should be **only one active session token** (stale callbacks should be dropped by the coordinator); and a push-to-talk release should *always* call `endCapture` with the active token — if the text is empty, the expected outcome is `dismiss` *without* a chime or send.

## Migration Steps (Suggested)

The page lists a suggested migration sequence to move the existing code onto the planned model. (1) Add `VoiceSessionCoordinator`, `VoiceSession`, and `VoiceSessionPublisher`. (2) Refactor `VoiceWakeRuntime` to create/update/end sessions instead of touching `VoiceWakeOverlayController` directly. (3) Refactor `VoicePushToTalk` to adopt existing sessions and call `endCapture` on release, applying the runtime cooldown. (4) Wire `VoiceWakeOverlayController` to the publisher and remove direct calls from the runtime and PTT. (5) Add integration tests for session adoption, cooldown, and empty-text dismissal.

**Source**: OpenClaw documentation — `platforms/mac/voice-overlay` (mirror `inbox/openclaw_docs/platforms/mac/voice-overlay.md`)
**Last Updated**: 2026-06-22
**Status**: Active
