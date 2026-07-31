---
tags:
  - resource
  - documentation
  - hermes_agent
  - vision
  - multimodal
keywords:
  - vision image paste
  - multimodal vision
  - clipboard image attach
  - vision_analyze
  - image routing vision-capable text-only
  - base64 image content block
topics:
  - Hermes Agent
  - Multimodal Vision
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/vision
access_control_group: ["general"]
---

# Hermes Vision & Image Paste

## Overview

Vision & Image Paste is the **multimodal image-input surface of the Hermes CLI** — the procedure for attaching clipboard images into a chat and the runtime routing that decides how each image reaches the model. You copy an image (screenshot, browser image, etc.), attach it via `/paste`, layered `Cmd/Ctrl+V`, or a referenced file path, and it surfaces as a `[📎 Image #1]` badge above the input; on submit the image is sent to the model as a base64-encoded data URL in the OpenAI vision content format, so any vision-capable model can process it. Because terminals are text-only and have no escape sequence for binary image bytes, Hermes reads the clipboard out-of-band via OS-level subprocess tools (`osascript`, `powershell.exe`, `xclip`, `wl-paste`) rather than through the terminal paste event. At runtime Hermes looks up the current model's vision capability in provider metadata and automatically routes each image one of two ways: vision-capable models get **raw pixels**; text-only models get a **text description** produced by the `auxiliary.vision` describer model via the `vision_analyze` tool. Images land in `~/.hermes/images/` as timestamped PNGs. This page owns the paste procedure, per-OS clipboard setup, SSH limits, and the routing model; the full `auxiliary.vision` config block lives in the SP02 config note, and the bundled vision-capable Portal models are documented in the Nous Portal note.

## How It Works

The basic attach loop, mirroring the source:

1. Copy an image to your clipboard (screenshot, browser image, etc.)
2. Attach it using one of the methods below
3. Type your question and press Enter
4. The image appears as a `[📎 Image #1]` badge above the input
5. On submit, the image is sent to the model as a vision content block

You can attach **multiple images** before sending — each gets its own badge. Press `Ctrl+C` to clear all attached images. Attached images are saved to `~/.hermes/images/` as PNG files with timestamped filenames.

## Paste Methods

How you attach an image depends on your terminal environment; not all methods work everywhere.

- **`/paste` command** — the most reliable explicit image-attach fallback. Type `/paste` and press Enter; Hermes checks your clipboard for an image and attaches it. This is the safest option when your terminal rewrites `Cmd+V`/`Ctrl+V`, or when you copied only an image and there is no bracketed-paste text payload to inspect.
- **`Ctrl+V` / `Cmd+V`** — Hermes treats paste as a **layered flow**: normal text paste first; native clipboard / OSC52 text fallback if the terminal did not deliver text cleanly; image attach when the clipboard or pasted payload resolves to an image or image path. This means pasted macOS screenshot temp paths and `file://...` image URIs attach immediately instead of sitting in the composer as raw text. If your clipboard has **only an image** (no text), terminals still cannot send binary image bytes directly — use `/paste`.
- **`/terminal-setup` for VS Code / Cursor / Windsurf** — when running the TUI inside a local VS Code-family integrated terminal on macOS, this installs the recommended `workbench.action.terminal.sendSequence` bindings for better multiline and undo/redo parity (useful when `Cmd+Enter`, `Cmd+Z`, or `Shift+Cmd+Z` are intercepted by the IDE). Run it on the **local machine only** — not inside an SSH session.

## Platform Compatibility

| Environment | `/paste` | Cmd/Ctrl+V | `/terminal-setup` | Notes |
|---|:---:|:---:|:---:|---|
| **macOS Terminal / iTerm2** | ✅ | ✅ | n/a | Best experience — native clipboard + screenshot-path recovery |
| **Apple Terminal** | ✅ | ✅ | n/a | If Cmd+←/→/⌫ gets rewritten, use Ctrl+A / Ctrl+E / Ctrl+U fallbacks |
| **Linux X11 desktop** | ✅ | ✅ | n/a | Requires `xclip` (`apt install xclip`) |
| **Linux Wayland desktop** | ✅ | ✅ | n/a | Requires `wl-paste` (`apt install wl-clipboard`) |
| **WSL2 (Windows Terminal)** | ✅ | ✅ | n/a | Uses `powershell.exe` — no extra install needed |
| **VS Code / Cursor / Windsurf (local)** | ✅ | ✅ | ✅ | Recommended for better Cmd+Enter / undo / redo parity |
| **VS Code / Cursor / Windsurf (SSH)** | ❌ | ❌ | ❌ | Run `/terminal-setup` on the local machine instead |
| **SSH terminal (any)** | ❌ | ❌ | n/a | Remote clipboard not accessible |

## Platform-Specific Setup

- **macOS** — no setup required; Hermes uses built-in `osascript` to read the clipboard. For faster performance, optionally `brew install pngpaste`.
- **Linux (X11)** — install `xclip` (`sudo apt install xclip` / `sudo dnf install xclip` / `sudo pacman -S xclip`).
- **Linux (Wayland)** — modern desktops (Ubuntu 22.04+, Fedora 34+) often default to Wayland; install `wl-clipboard`. Check your session type with `echo $XDG_SESSION_TYPE` (`wayland` = Wayland, `x11` = X11, `tty` = no display server).
- **WSL2** — no extra setup; Hermes detects WSL2 via `/proc/version` and uses `powershell.exe` to reach the Windows clipboard through .NET's `System.Windows.Forms.Clipboard`. Data transfers as base64-encoded PNG over stdout (no temp files). Under **WSLg**, Hermes tries PowerShell first then falls back to `wl-paste`; WSLg's bridge only supports BMP, so Hermes auto-converts BMP→PNG via Pillow or ImageMagick's `convert`.

To verify WSL2 clipboard access:

```bash
# 1. Check WSL detection
grep -i microsoft /proc/version

# 2. Check PowerShell is accessible
which powershell.exe

# 3. Copy an image, then check
powershell.exe -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::ContainsImage()"
# Should print "True"
```

## SSH & Remote Sessions

**Clipboard image paste does not fully work over SSH.** When you SSH into a remote machine, the Hermes CLI runs on the remote host; clipboard tools (`xclip`, `wl-paste`, `powershell.exe`, `osascript`) read the clipboard of the machine they run on — the remote server, not your local machine — so your local clipboard image is inaccessible from the remote side. Text can sometimes still bridge through terminal paste or OSC52, but image clipboard access and local screenshot temp paths remain tied to the machine running Hermes.

**Workarounds:**

1. **Upload the image file** — save it locally, transfer it via `scp` / VS Code drag-and-drop / any file transfer, then reference it by path. *(A `/attach <filepath>` command is planned for a future release.)*
2. **Use a URL** — paste an online image URL in your message; the agent can use `vision_analyze` on any image URL directly.
3. **X11 forwarding** — connect with `ssh -X` so `xclip` on the remote can access your local X11 clipboard (needs a local X server — XQuartz on macOS; slow for large images).
4. **Use a messaging platform** — send images via Telegram, Discord, Slack, or WhatsApp, which handle image upload natively and are unaffected by clipboard/terminal limits.

## Why Terminals Can't Paste Images

Terminals are **text-based** interfaces. On `Ctrl+V`/`Cmd+V` the emulator reads the clipboard for **text content**, wraps it in bracketed-paste escape sequences, and sends it through the terminal's text stream. If the clipboard contains only an image, the terminal has nothing to send — there is no standard terminal escape sequence for binary image data, so it does nothing. This is why Hermes uses a **separate clipboard check**: instead of receiving image data through the paste event, it calls OS-level tools (`osascript`, `powershell.exe`, `xclip`, `wl-paste`) directly via subprocess to read the clipboard independently.

## Supported Models

Image paste works with any vision-capable model. The image is sent as a base64-encoded data URL in the OpenAI vision content format:

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/png;base64,..."
  }
}
```

Most modern models support this format, including GPT-4 Vision, Claude (with vision), Gemini, and open-source multimodal models served through OpenRouter. Portal subscribers get vision-capable models (Claude, GPT-5, Gemini) in the same catalog with no extra credentials.

## Image Routing (Vision-Capable vs Text-Only Models)

When a user attaches an image — from the CLI clipboard, the gateway (Telegram/Discord photo), or any other entry point — Hermes routes it based on whether the current model actually supports vision:

| Your model | What happens to the image |
|---|---|
| **Vision-capable** (GPT-4V, Claude with vision, Gemini, Qwen-VL, MiMo-VL, etc.) | Sent as **real pixels** using the provider's native image content format above. No text summary layer. |
| **Text-only** (DeepSeek V3, smaller open-source models, older chat-only endpoints) | Routed through the `vision_analyze` auxiliary tool — an auxiliary vision model describes the image, and the text description is injected into the conversation. |

You don't configure this — Hermes looks up the current model's capability in provider metadata and picks the right path automatically. The practical effect: you can switch between vision and non-vision models mid-session and image handling "just works" without changing your workflow; text-only models get coherent context about the image rather than a broken multimodal payload they'd reject. Which auxiliary model handles the text-description path is configurable under `auxiliary.vision` (see `hermes_messaging_media_settings`).

### `vision_analyze` has the same dual behavior

The `vision_analyze` tool itself follows the same routing. When the active main model is vision-capable **and** its provider supports image content inside tool results (currently the Anthropic, OpenAI, Azure-OpenAI, and Gemini 3.x stacks), `vision_analyze` short-circuits the auxiliary describer and returns the raw image pixels as a multimodal tool-result envelope — the main model sees the image natively on its next turn, with no aux call, no text-summary information loss, and no extra latency. For text-only main models (or providers whose tool-result channel doesn't carry images), `vision_analyze` falls back to the legacy path: it asks the configured auxiliary vision model to describe the image and returns the description as plain text. Either way the calling tool signature is the same — the tool decides which path to take at runtime based on the active model.

**Source**: `inbox/hermes_agent_docs/user-guide/features/vision.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/vision
**Last Updated**: 2026-06-19
**Status**: Active
