---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - menu_bar_icon
keywords:
  - openclaw menu bar icon states
  - critter icon animation macos
  - triggervoiceears stopvoiceears
  - earboostactive big ears voice trigger
  - isworking tail leg scurry
  - crittericonrenderer makeicon earscale earholes
  - appearsdisabled paused icon
  - short ttl reset defer
topics:
  - OpenClaw
  - macOS Menu Bar Icon
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/platforms/mac/icon
access_control_group: ["general"]
---

# OpenClaw — macOS Menu Bar Icon States

## Overview

This note models the OpenClaw macOS app's menu-bar **critter-icon state model**: the four visual states the status-item icon renders (Idle, Paused, Voice trigger, Working), the `AppState` signals and wiring calls that drive each state, the `CritterIconRenderer.makeIcon(...)` shape/size parameters, and the behavioral guidance for keeping the animation safe. It mirrors the `platforms/mac/icon.md` source page (scope: macOS app `apps/macos`, author steipete, updated 2025-12-06), whose body is a state enumeration under the page H1 `# Menu Bar Icon States` plus the "Wiring points", "Shapes & sizes", and "Behavioral notes" subsections. It is a UI state-model reference (one `building_block: model`), not a procedure.

## Icon States

The menu-bar icon renders one of four states, each driven by the in-app `AppState` signals:

- **Idle:** Normal icon animation — blink and occasional wiggle. This is the baseline the icon returns to when no work or voice activity is in flight.
- **Paused:** The status item uses `appearsDisabled`; no motion is rendered.
- **Voice trigger (big ears):** When the wake word is heard, the voice-wake detector calls `AppState.triggerVoiceEars(ttl: nil)`, keeping `earBoostActive=true` while the utterance is captured. The ears scale up (1.9x) and get circular ear holes for readability, then drop back via `stopVoiceEars()` after 1s of silence. This state is **only fired from the in-app voice pipeline**.
- **Working (agent running):** `AppState.isWorking=true` drives a "tail/leg scurry" micro-motion — a faster leg wiggle and a slight offset while work is in-flight. It is currently toggled around WebChat agent runs; the source notes that the same toggle should be added around other long tasks when they are wired.

## Wiring Points

The state model is driven by two explicit wiring calls into `AppState` / `AppStateStore`:

- **Voice wake:** The runtime (or a tester) calls `AppState.triggerVoiceEars(ttl: nil)` on trigger and `stopVoiceEars()` after 1s of silence, so the boosted-ears window matches the audio capture window.
- **Agent activity:** Callers set `AppStateStore.shared.setWorking(true/false)` around work spans (already done in the WebChat agent call). The source instructs keeping spans short and resetting state in `defer` blocks to avoid stuck animations.

## Shapes and Sizes

The icon geometry is produced by `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)`:

- The base icon is drawn through `CritterIconRenderer.makeIcon(...)` with the parameters above.
- The ear scale defaults to `1.0`; the voice boost sets `earScale=1.9` and toggles `earHoles=true` **without changing the overall frame** — an 18×18 pt template image rendered into a 36×36 px Retina backing store.
- The Working "scurry" uses a leg wiggle up to ~1.0 with a small horizontal jiggle, and it is **additive** to any existing idle wiggle (the two motions compose rather than replace each other).

## Behavioral Notes

The source constrains how the icon signals are wired:

- There is **no external CLI/broker toggle** for the ears or working states; these are kept internal to the app's own signals to avoid accidental flapping.
- TTLs are kept short (`<10s`) so the icon returns to its baseline quickly if a job hangs.

**Source**: OpenClaw documentation — `platforms/mac/icon` (mirror `inbox/openclaw_docs/platforms/mac/icon.md`)
**Last Updated**: 2026-06-22
**Status**: Active
