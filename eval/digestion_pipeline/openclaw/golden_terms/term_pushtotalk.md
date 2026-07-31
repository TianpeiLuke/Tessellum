---
tags:
  - resource
  - terminology
  - pushtotalk
  - ptt
  - macos-input
  - nsevent
  - openclaw
keywords:
  - Push-to-Talk
  - PTT
  - Right Option PTT
  - NSEvent global monitor
  - modifier-flag edge
  - overlay session token
topics:
  - Voice input
  - macOS input handling
  - OpenClaw voice surface
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Push-to-talk
access_control_group: ["general"]
---

# Push-to-Talk (PTT)

## Definition

**Push-to-Talk (PTT)**, also called press-to-transmit, is a half-duplex voice-input mode in which a user holds a dedicated button to open the microphone and releases it to close the channel. The pattern originated in 1930s two-way police radios and was popularized at scale during World War II walkie-talkies; it has since migrated from analog radio hardware to digital trunked radio, cellular PoC (Push-to-Talk over Cellular), and finally to software channels like Discord, Zello, and Apple's iOS `PushToTalk` framework, where the press-and-hold contract is overlaid on a keyboard key, touchscreen button, or hardware accessory.

In OpenClaw's macOS app, PTT is the manual counterpart to wake-word ([Voice Wake](term_voice_wake.md)): instead of always-listening hot-word detection, the user **holds Right-Option** (keyCode 61) to open a transcription session and releases it to seal-and-send. The capture surface is `VoicePushToTalkHotkey` — a `@unchecked Sendable` singleton that registers an `NSEvent` global + local monitor pair on `.flagsChanged` events, gates a modifier-flag edge state machine (`optionDown` ↔ `active`), and dispatches `beginAction` / `endAction` exactly once per press / release into the shared `VoiceWakeOverlayController` so the same floating panel and ASR pipeline can be driven either by wake-word or by the held key.

## Context

PTT recurs across multiple software ecosystems with similar semantics but different system-integration substrates:

- **Discord / Zello / TeamSpeak**: keyboard PTT for gaming and field-team voice chat, the canonical industry "press a key to talk" pattern.
- **Apple `PushToTalk` framework (iOS 16+)**: a system-level walkie-talkie API where `PTChannelManager` brokers system UI, lock-screen presence, and background wake — the iOS analog to OpenClaw's macOS approach.
- **Cellular PoC and trunked LMR**: hardware-radio PTT (Motorola APX, Hytera) that the software PTT pattern emulates in user expectation (zero "ring time", half-duplex, instant push-to-broadcast).

OpenClaw's macOS PTT complements [Voice Wake](term_voice_wake.md) by giving the user a **manual override** over always-on listening: wake-word can be disabled (privacy, battery, or noisy-environment) while PTT remains available, or both can coexist sharing the same overlay window — token discipline (`activeToken: UUID`) lets the latest session win. The capture is driven by `NSEvent.addGlobalMonitorForEvents`, which requires the **Input Monitoring** TCC permission to receive keystrokes from other-app focus, plus a paired local monitor that fires when OpenClaw itself is focused.

## Key Characteristics

- **Paired NSEvent monitors**: `addGlobalMonitorForEvents(matching: .flagsChanged)` (other-app focus, requires Input Monitoring permission) + `addLocalMonitorForEvents(matching: .flagsChanged)` (own-app focus, no permission). The local closure must `return event` so AppKit dispatch continues; the global closure is listen-only.
- **Modifier-flag edge gating**: `.flagsChanged` events carry no character payload, so the listener watches **keyCode 61** (right Option specifically; left Option is 58) and reads press state from `modifierFlags.contains(.option)`. Two booleans (`optionDown` raw, `active` derived) implement an edge-triggered state machine where only the rising and falling edges fire side effects.
- **Main-thread serialization**: every NSEvent callback hops to `DispatchQueue.main.async` before reading or mutating state, which is how the `@unchecked Sendable` class earns its claim without locks — every state-touching method runs on the same queue by convention.
- **Session-token mint + activeToken install**: each `beginAction` mints a fresh `UUID` and installs it as `activeToken` on the shared `VoiceWakeOverlayController`, cancelling any pending auto-send and returning the token so partials/finals can be correlated.
- **Partial-transcript guard with `isFinal` gate**: streaming ASR partials are accepted only when both the token matches AND `model.isFinal` is false — a late partial cannot clobber text the user is about to send.
- **`presentFinal` auto-send dispatch**: on release, `presentFinal` seals `isFinal = true`, derives `forwardEnabled` from a trimmed-whitespace empty check, then dispatches one of three branches — no auto-send (nil delay), immediate `sendNow` (delay ≤ 0), or `scheduleAutoSend` Task (delay > 0).
- **Post-stop fade with token-guard teardown**: dismiss animates frame + alpha to zero over 0.18 s, snapshots `activeToken` BEFORE clearing it (so the completion's `overlayDidDismiss` notification carries the correct correlation id), and runs the same model-clear contract regardless of whether the path was UI-off, headless-test, or animated.
- **Idempotent enable / teardown**: `setEnabled(true)` no-ops if monitors already exist; `stopMonitoring` removes both monitor tokens and resets `optionDown` / `active` so a chord held across a re-enable cycle starts clean (a release that occurred while disabled is forgiven, not replayed as a spurious `endAction`).

## Related Terms


### Related Code Snippets

- **[OpenClaw macOS PTT — NSEvent Hotkey Listener](../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md)**: the `VoicePushToTalkHotkey` singleton, paired global+local NSEvent monitor install, modifier-flag edge gating, main-thread serialization.
- **[OpenClaw macOS PTT — Overlay Session Lifecycle](../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md)**: the `VoiceWakeOverlayController+Session` extension — session-token mint, partial-with-`isFinal`-guard, `presentFinal` auto-send dispatch, animated dismiss.

## References

- [Push-to-talk — Wikipedia](https://en.wikipedia.org/wiki/Push-to-talk) — half-duplex two-way-radio origin, 1930s public-safety adoption, walkie-talkie evolution, cellular PoC and software-PTT lineage.
- [Push to Talk — Apple Developer Documentation](https://developer.apple.com/documentation/pushtotalk) — Apple's iOS `PushToTalk` framework; system-level walkie-talkie API with background wake and lock-screen presence; the iOS analog to OpenClaw's macOS NSEvent approach.
- [PTChannelManager — Apple Developer Documentation](https://developer.apple.com/documentation/pushtotalk/ptchannelmanager) — the iOS PTT channel-manager class; useful contrast for "how Apple solves the same problem" at the framework level vs OpenClaw's raw NSEvent global monitor.
- [NSEvent.addGlobalMonitorForEvents — Apple Developer Documentation](https://developer.apple.com/documentation/appkit/nsevent/addglobalmonitorforevents(matching:handler:)) — the global event-monitor API OpenClaw uses; documents the Input Monitoring / Accessibility TCC permission requirement.
- [Monitoring Events — Apple Cocoa Event Architecture](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/MonitoringEvents/MonitoringEvents.html) — the broader Cocoa event-monitoring guide that explains the global-vs-local monitor split.
