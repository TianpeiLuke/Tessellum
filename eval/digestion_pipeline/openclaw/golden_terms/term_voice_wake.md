---
tags:
  - resource
  - terminology
  - voice-wake
  - wake-word
  - keyword-spotting
  - macos-native
  - openclaw
keywords:
  - Voice Wake
  - wake word detection
  - SFSpeechRecognizer
  - AVAudioEngine
  - trigger word
  - silence timer
  - adaptive RMS noise floor
topics:
  - Wake-word detection
  - Voice interfaces
  - OpenClaw macOS app
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Voice Wake

## Definition

**Voice Wake** is OpenClaw's macOS-native wake-word state machine: an always-on listening pipeline that watches the system microphone for a configurable trigger word ("hey claw", etc.) and, on a match, hands off captured speech to the agent runtime as a turn. Wake-word detection (a specialized case of [keyword spotting](https://en.wikipedia.org/wiki/Keyword_spotting)) is the canonical activation primitive behind "Hey Siri", "Alexa", and "OK Google" — a tiny model continuously processes ambient audio locally so no audio leaves the device until the trigger phrase fires.

Unlike dedicated keyword-spotting engines that ship a sub-1 MB CNN/RNN tuned for a single phrase, OpenClaw's Voice Wake implementation runs Apple's stock [`SFSpeechRecognizer`](https://developer.apple.com/documentation/speech/sfspeechrecognizer) in continuous dictation mode and matches trigger phrases against the streaming transcript. This trades the latency / power efficiency of a purpose-built KWS engine for zero model-distribution overhead and full-vocabulary fallback (so a near-miss like "hey clawd" can still match via fuzzy text rules). The 837-line `VoiceWakeRuntime.swift` is the entire state machine — audio pipeline, recognition dispatcher, capture lifecycle, and push-to-talk coordination.

## Context

Industry KWS engines fall into two camps. **Dedicated engines** — [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) (commercial, sub-1 MB CNN, custom trigger via transfer learning), [OpenWakeWord](https://github.com/dscripka/openWakeWord) (open-source, actively maintained), and historically Snowboy (deprecated) — process raw audio with a tiny always-on neural network whose output is the likelihood of a single keyword. Apple's "Hey Siri" detector (see [Apple ML Research](https://machinelearning.apple.com/research/hey-siri)) is a two-stage DNN that runs continuously on the Always-On Processor at sub-50 ms latency. **Continuous ASR with text-matching** — what OpenClaw uses — streams audio through a general-purpose recognizer and matches the transcript; this is heavier but reuses the OS's installed dictation models.

Within OpenClaw, Voice Wake is one of two voice entry-points alongside [Push-to-Talk](term_pushtotalk.md): wake-word fires automatically on the trigger phrase, while PTT fires on a Right-Option hotkey. Both feed the same [Voice Call](term_voice_call.md) substrate downstream. The runtime is built on Swift `actor` isolation: `VoiceWakeRuntime` owns three lazy resources (`SFSpeechRecognizer`, `AVAudioEngine`, `SFSpeechAudioBufferRecognitionRequest`) and a `RuntimeConfig`-keyed idempotent refresh that reconciles against `AppState` mutations from the settings UI. The engine is allocated lazily because eagerly instantiating `AVAudioEngine` can flip a connected Bluetooth headset into the low-quality HFP profile even when Voice Wake is disabled.

## Key Characteristics

- **`AVAudioEngine` audio tap**: installs a tap on input bus 0 (buffer size 2048) per [Apple's continuous-recognition pattern](https://developer.apple.com/documentation/speech/sfspeechaudiobufferrecognitionrequest); each buffer is appended to the recognition request AND sampled for RMS energy via two detached child tasks.
- **`SFSpeechRecognizer` continuous-mode init**: locale-configured per `RuntimeConfig`; request has `shouldReportPartialResults = true` and `taskHint = .dictation` — uses Apple's stock speech framework, not a dedicated KWS model.
- **`RuntimeConfig` + refresh/start/stop lifecycle**: an `Equatable` struct (triggers, micID, localeID, chimes, talk-mode flag) is the equality key for idempotent refresh; a `MainActor` snapshot → five-rule short-circuit ladder → stop/start avoids tearing down audio resources on UI rebroadcasts.
- **Recognition handler with stale-generation rejection**: a monotonic `recognitionGeneration` counter is bumped on every restart and captured into each callback closure; callbacks whose generation is stale are dropped to prevent transcript mixing across superseded sessions.
- **Audio-tap level logging**: `noteAudioTap` is rate-limited to 1.0 s per log line (audio engine fires hundreds of times per second); each line logs raw RMS, derived dB (`20 * log10(max(rms, 1e-7))`), and the `isCapturing` flag.
- **Trigger-only + pre-detect silence timers**: two mutually-exclusive deferred-detection paths — `triggerOnlyTask` fires when the user said only the wake word and went silent, `preDetectTask` fires when streaming never produced an `isFinal` segment; each scheduler cancels the other so duplicate captures cannot fire.
- **`matchedTriggerWord`**: resolves WHICH configured trigger phrase matched the transcript at snapshot time; persisted into `activeTriggerWord` so the capture lifecycle can later trim "command after trigger" correctly.
- **`beginCapture` / `monitorCapture` / `finalizeCapture`**: three-phase capture lifecycle — begin flips `isCapturing = true` and spawns the monitor task; monitor polls every 200 ms and exits on hard-stop or silence-window expiry; finalize disarms before halting (sets `isCapturing = false` and stamps `cooldownUntil` BEFORE `haltRecognitionPipeline()` to defeat late-callback races).
- **Adaptive RMS noise floor**: asymmetric EMA — alpha 0.08 on energy drops (fast adapt to quiet rooms), alpha 0.01 on rises (slow adapt resists loud transients); speech threshold = `max(minSpeechRMS, noiseFloorRMS * speechBoostFactor)` so silent rooms cannot collapse the threshold to zero.
- **Scheduled recognizer restart**: 700 ms debounced restart after finalize via `scheduleRestartRecognizer` — cancels any prior scheduled task, then re-checks `isCapturing` before firing so a fresh capture started during the window cancels the restart.
- **PTT cooldown + pause**: two surface controls — `applyPushToTalkCooldown()` stamps `cooldownUntil` only (leaves recognizer running), `pauseForPushToTalk()` flips state to `.pushToTalk` and calls `stop(dismissOverlay: false)` so the PTT subsystem owns the mic without UI flicker.

## Related Terms


### Related Code Snippets

- **[Voice Wake — Audio Pipeline](../code_snippets/snippet_openclaw_macos_voice_wake_audio.md)**: split 1 of 3 — `AVAudioEngine` + `SFSpeechRecognizer` lazy allocation, `RuntimeConfig` equality, `refresh/start/stop` lifecycle, `haltRecognitionPipeline` generation bump.
- **[Voice Wake — State Transitions](../code_snippets/snippet_openclaw_macos_voice_wake_state.md)**: split 2 of 3 — `handleRecognition` dispatcher, stale-callback rejection, capturing/idle branch-and-cap, trigger-only / pre-detect silence timers, snapshot-then-revalidate.
- **[Voice Wake — Capture Lifecycle](../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md)**: split 3 of 3 — `beginCapture/monitorCapture/finalizeCapture`, adaptive RMS noise floor, scheduled recognizer restart, PTT cooldown + pause surfaces.

## References

- [Keyword spotting (Wikipedia)](https://en.wikipedia.org/wiki/Keyword_spotting) — definition of keyword spotting and its relationship to wake-word detection ("hot word") used by Alexa, Siri, and similar assistants.
- [SFSpeechAudioBufferRecognitionRequest (Apple Developer)](https://developer.apple.com/documentation/speech/sfspeechaudiobufferrecognitionrequest) — Apple's API for feeding `AVAudioPCMBuffer` data from `AVAudioEngine` into continuous speech recognition; the substrate Voice Wake's audio pipeline is built on.
- [SFSpeechRecognizer (Apple Developer)](https://developer.apple.com/documentation/speech/sfspeechrecognizer) — the speech-recognition class Voice Wake uses in continuous dictation mode.
- [Porcupine Wake Word (Picovoice)](https://picovoice.ai/platform/porcupine/) — commercial dedicated KWS engine; reference comparator showing the model-file / sub-1 MB approach Voice Wake deliberately does not take.
- [openWakeWord (dscripka)](https://github.com/dscripka/openWakeWord) — actively maintained open-source dedicated wake-word engine; reference comparator.
- [Hey Siri — Apple Machine Learning Research](https://machinelearning.apple.com/research/hey-siri) — Apple's two-stage DNN architecture for always-on wake-word detection on the Always-On Processor.
- [VoiceWakeRuntime.swift (OpenClaw)](https://github.com/openclaw/openclaw/blob/main/apps/macos/Sources/OpenClaw/VoiceWakeRuntime.swift) — the 837-LOC implementation file.
