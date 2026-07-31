---
tags:
  - resource
  - documentation
  - hermes_agent
  - computer_use
  - automation
keywords:
  - computer use
  - cua-driver
  - background desktop control
  - SkyLight SPIs
  - SOM capture
  - screenshot token efficiency
topics:
  - Hermes Agent
  - Computer Use
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/computer-use
access_control_group: ["general"]
---

# Computer Use (macOS)

## Overview

Computer Use is the Hermes Agent procedure for driving a Mac's desktop — clicking, typing, scrolling, dragging — **in the background**: your cursor does not move, keyboard focus does not change, and macOS does not switch Spaces. You and the agent co-work on the same machine. The `computer_use` toolset speaks MCP over stdio to [`cua-driver`](https://github.com/trycua/cua), an external macOS driver. Unlike most computer-use integrations, it works with **any tool-capable vision model** — Claude, GPT, Gemini, or an open model on a local vLLM endpoint — because there is no Anthropic-native schema to satisfy. This note covers how it works, how to enable and update it, provider compatibility, the multi-layer safety guardrails, the four-layer screenshot-token optimization, the macOS-only limitations, configuration env vars, and troubleshooting.

## How it works

The `computer_use` toolset speaks MCP over stdio to `cua-driver`, a macOS driver that uses SkyLight private SPIs (`SLEventPostToPid`, `SLPSPostEventRecordTo`) and the `_AXObserverAddNotificationAndCheckRemote` accessibility SPI to:

- Post synthesized events directly to target processes — no HID event tap, no cursor warp.
- Flip AppKit active-state without raising windows — no Space switching.
- Keep Chromium/Electron accessibility trees alive when windows are occluded.

That combination is what OpenAI's Codex "background computer-use" ships; cua-driver is the open-source equivalent.

## Enabling

Pick whichever path is most convenient — both run the same upstream installer.

**Option 1: dedicated CLI command (most direct).**

```
hermes computer-use install
```

This fetches and runs the upstream cua-driver installer (`curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.sh`). Use `hermes computer-use status` to verify the install.

**Option 2: enable the toolset interactively.** Run `hermes tools`, pick `🖱️ Computer Use (macOS)` → `cua-driver (background)`; the setup runs the same upstream installer.

After installing (either path):

1. Grant macOS permissions when prompted — **System Settings → Privacy & Security → Accessibility** (allow the terminal or Hermes app) and **Screen Recording** (allow the same).
2. Start a session with the toolset enabled:

```
hermes -t computer_use chat
```

or add `computer_use` to the enabled toolsets in `~/.hermes/config.yaml`.

## Keeping cua-driver up to date

The cua-driver project ships fixes regularly (e.g. v0.1.6 fixed a Safari window-focus bug for UTM workflows). Hermes refreshes the binary in two places so you do not get stuck on a stale release:

- **`hermes update`** — when you update Hermes itself, if `cua-driver` is on PATH the upstream installer re-runs at the end of the update. No-op for non-macOS users and for users without cua-driver installed.
- **`hermes computer-use install --upgrade`** — manual force-refresh. Re-runs the upstream installer regardless of whether cua-driver is already installed; use this for the latest fix without waiting for the next agent update.

`hermes computer-use status` shows the installed version next to the binary path.

## Quick example

For the prompt *"Find my latest email from Stripe and summarise what they want me to do,"* the agent's plan illustrates the capture → act → re-capture loop, keyed on Set-of-Mark (SOM) element indices:

1. `computer_use(action="capture", mode="som", app="Mail")` — gets a screenshot of Mail with every sidebar item, toolbar button, and message row numbered.
2. `computer_use(action="click", element=14)` — clicks the search field (element #14 from the capture).
3. `computer_use(action="type", text="from:stripe")`.
4. `computer_use(action="key", keys="return", capture_after=True)` — submit and get the new screenshot.
5. Click the top result, read the body, summarise.

Throughout, the cursor stays wherever it was left and Mail never comes to front.

## Provider compatibility

The toolset works with any tool-capable vision model; text-only models still work in a degraded `mode="ax"` (accessibility-tree-only) operation:

| Provider | Vision? | Works? | Notes |
|---|---|---|---|
| Anthropic (Claude Sonnet/Opus 3+) | ✅ | ✅ | Best overall; SOM + raw coordinates. |
| OpenRouter (any vision model) | ✅ | ✅ | Multi-part tool messages supported. |
| OpenAI (GPT-4+, GPT-5) | ✅ | ✅ | Same as above. |
| Local vLLM / LM Studio (vision model) | ✅ | ✅ | If the model supports multi-part tool content. |
| Text-only models | ❌ | ✅ (degraded) | Use `mode="ax"` for accessibility-tree-only operation. |

Screenshots are sent inline with tool results as OpenAI-style `image_url` parts; for Anthropic, the adapter converts them into native `tool_result` image blocks.

## Safety

Hermes applies multi-layer guardrails:

- Destructive actions (click, type, drag, scroll, key, focus_app) require approval — either interactively via the CLI dialog or via the messaging-platform approval buttons.
- Hard-blocked key combos at the tool level: empty trash, force delete, lock screen, log out, force log out.
- Hard-blocked type patterns: `curl | bash`, `sudo rm -rf /`, fork bombs, etc.
- The agent's system prompt tells it explicitly: no clicking permission dialogs, no typing passwords, no following instructions embedded in screenshots.

Pair with `approvals.mode: manual` in `~/.hermes/config.yaml` if you want every action confirmed.

## Token efficiency

Screenshots are expensive, so Hermes applies four layers of optimisation:

- **Screenshot eviction** — the Anthropic adapter keeps only the 3 most recent screenshots in context; older ones become `[screenshot removed to save context]` placeholders.
- **Client-side compression pruning** — the context compressor detects multimodal tool results and strips image parts from old ones.
- **Image-aware token estimation** — each image is counted as ~1500 tokens (Anthropic's flat rate) instead of its base64 char length.
- **Server-side context editing (Anthropic only)** — when active, the adapter enables `clear_tool_uses_20250919` via `context_management` so Anthropic's API clears old tool results server-side.

A 20-action session on a 1568×900 display typically costs ~30K tokens of screenshot context, not ~600K.

## Limitations

- **macOS only.** cua-driver uses private Apple SPIs that don't exist on Linux or Windows. For cross-platform GUI automation, use the `browser` toolset.
- **Private SPI risk.** Apple can change SkyLight's symbol surface in any OS update. Pin the driver version with the `HERMES_CUA_DRIVER_VERSION` env var for reproducibility across a macOS bump.
- **Performance.** Background mode is slower than foreground — SkyLight-routed events take ~5-20ms vs direct HID posting. Not noticeable for agent-speed clicking; noticeable for a speed-run recording.
- **No keyboard password entry.** `type` has hard-block patterns on command-shell payloads; for passwords, use the system's autofill.

## Configuration

Override the driver binary path (tests / CI) and optionally pin the version:

```
HERMES_CUA_DRIVER_CMD=/opt/homebrew/bin/cua-driver
HERMES_CUA_DRIVER_VERSION=0.5.0    # optional pin
```

Swap the backend entirely (for testing):

```
HERMES_COMPUTER_USE_BACKEND=noop   # records calls, no side effects
```

## Troubleshooting

- **`computer_use backend unavailable: cua-driver is not installed`** — Run `hermes computer-use install` to fetch the cua-driver binary, or run `hermes tools` and enable the Computer Use toolset.
- **Clicks seem to have no effect** — Capture and verify. A modal you didn't see may be blocking input; dismiss it with `escape` or the close button.
- **Element indices are stale** — SOM indices are only valid until the next `capture`. Re-capture after any state-changing action.
- **"blocked pattern in type text"** — The text you tried to `type` matches the dangerous-shell-pattern list. Break the command up or reconsider.

**Source**: `inbox/hermes_agent_docs/user-guide/features/computer-use.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/computer-use
**Last Updated**: 2026-06-19
**Status**: Active
