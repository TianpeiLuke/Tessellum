---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - android
keywords:
  - openclaw android node commands
  - android chat history normalization
  - gateway canvas host android
  - canvas camera node commands
  - android mic talk voice mode
  - foreground service microphone promotion
  - android device command families
  - google assistant app actions
  - notification forwarding quiet hours
topics:
  - OpenClaw
  - Android Node Surface
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/android
access_control_group: ["general"]
---

# OpenClaw — Android Node Command Surface (Chat, Canvas, Voice, Notifications)

## Overview

This note is the procedure for driving the OpenClaw Android companion node's command surface **once it is already paired and connected** — the post-connection half of the `platforms/android` source page (sections 6 Chat + history, 7 Canvas + camera, 8 Voice + expanded command surface, plus Assistant entrypoints and Notification forwarding). It covers the Chat tab's session/history normalization, the Gateway-hosted Canvas plus camera commands, the Mic-vs-Talk voice capture modes and foreground-service microphone promotion, the expanded Android device command families, the Google-Assistant App-Actions launch entrypoint, and scoped notification forwarding. The connection/pairing/discovery prerequisite (Connect tab, mDNS/NSD, Tailscale, device approval) lives in its sibling note `oc_platforms_android_connection.md` — this note begins where that one ends.

## Chat + history

The Android **Chat tab** supports session selection (default `main`, plus other existing sessions). History is fetched with the `chat.history` command and is **display-normalized**: inline directive tags are stripped from visible text; plain-text tool-call XML payloads (including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks) and leaked ASCII/full-width model control tokens are stripped; pure silent-token assistant rows such as the exact `NO_REPLY` / `no_reply` are omitted; and oversized rows can be replaced with placeholders. Messages are sent with `chat.send`. Push updates are best-effort via `chat.subscribe`, which delivers an `event:"chat"` stream.

## Canvas + camera

### Gateway Canvas Host (recommended for web content)

To have the node show real HTML/CSS/JS that the agent can edit on disk, point the node at the **Gateway canvas host**. Nodes load canvas from the Gateway HTTP server (same port as `gateway.port`, default `18789`). The flow is: (1) create `~/.openclaw/workspace/canvas/index.html` on the gateway host, then (2) navigate the node to it over LAN:

```bash
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18789/__openclaw__/canvas/"}'
```

For tailnet use (both devices on Tailscale), use a MagicDNS name or tailnet IP instead of `.local`, e.g. `http://<gateway-magicdns>:18789/__openclaw__/canvas/`. This server injects a live-reload client into HTML and reloads on file changes. The Gateway also serves `/__openclaw__/a2ui/`, but the Android app treats **remote A2UI pages as render-only**; action-capable A2UI commands use the bundled app-owned A2UI page before applying messages.

### Canvas and camera commands (foreground only)

Canvas commands are foreground-only: `canvas.eval`, `canvas.snapshot`, and `canvas.navigate` (use `{"url":""}` or `{"url":"/"}` to return to the default scaffold). `canvas.snapshot` returns `{ format, base64 }` with default `format="jpeg"`. A2UI canvas commands are `canvas.a2ui.push` and `canvas.a2ui.reset` (`canvas.a2ui.pushJSONL` is a legacy alias); these use the bundled app-owned A2UI page for action-capable rendering. Camera commands are foreground-only and permission-gated: `camera.snap` (jpg) and `camera.clip` (mp4). See the upstream Camera node page for parameters and CLI helpers.

## Voice + expanded Android command surface

The **Voice tab** has two explicit capture modes. **Mic** is a manual Voice-tab session that sends each pause as a chat turn and stops when the app leaves the foreground or the user leaves the Voice tab. **Talk** is continuous Talk Mode and keeps listening until toggled off or the node disconnects. Talk Mode promotes the existing foreground service from `connectedDevice` to `connectedDevice|microphone` before capture starts, then demotes it when Talk Mode stops. The node service declares `FOREGROUND_SERVICE_CONNECTED_DEVICE` with `CHANGE_NETWORK_STATE`; Android 14+ also requires the `FOREGROUND_SERVICE_MICROPHONE` declaration, the `RECORD_AUDIO` runtime grant, and the microphone service type at runtime.

By default, Android Talk uses native speech recognition, Gateway chat, and `talk.speak` through the configured gateway Talk provider; local system TTS is used only when `talk.speak` is unavailable. Android Talk uses realtime Gateway relay only when `talk.realtime.mode` is `realtime` and `talk.realtime.transport` is `gateway-relay`. Voice wake remains disabled in the Android UX/runtime.

### Expanded device command families

Availability of these command families depends on device, permissions, and user settings:

- `device.status`, `device.info`, `device.permissions`, `device.health`
- `device.apps` — only when **Settings > Phone Capabilities > Installed Apps** is enabled; it lists launcher-visible apps by default.
- `notifications.list`, `notifications.actions` (see Notification forwarding below)
- `photos.latest`
- `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `callLog.search`
- `sms.search`
- `motion.activity`, `motion.pedometer`

## Assistant entrypoints

Android supports launching OpenClaw from the system assistant trigger (**Google Assistant**). When configured, holding the home button or saying "Hey Google, ask OpenClaw..." opens the app and hands the prompt into the chat composer. This uses Android **App Actions** metadata declared in the app manifest; no extra configuration is needed on the gateway side — the assistant intent is handled entirely by the Android app and forwarded as a normal chat message. App Actions availability depends on the device, Google Play Services version, and whether the user has set OpenClaw as the default assistant app.

## Notification forwarding

Android can forward device notifications to the gateway as events, scoped by several controls over which notifications are forwarded and when:

| Key | Type | Description |
| --- | --- | --- |
| `notifications.allowPackages` | string[] | Only forward notifications from these package names. If set, all other packages are ignored. |
| `notifications.denyPackages` | string[] | Never forward notifications from these package names. Applied after `allowPackages`. |
| `notifications.quietHours.start` | string (HH:mm) | Start of quiet hours window (local device time). Notifications are suppressed during this window. |
| `notifications.quietHours.end` | string (HH:mm) | End of quiet hours window. |
| `notifications.rateLimit` | number | Maximum forwarded notifications per package per minute. Excess notifications are dropped. |

The notification picker also uses safer behavior for forwarded notification events, preventing accidental forwarding of sensitive system notifications. Example configuration:

```json5
{
  notifications: {
    allowPackages: ["com.slack", "com.whatsapp"],
    denyPackages: ["com.android.systemui"],
    quietHours: {
      start: "22:00",
      end: "07:00",
    },
    rateLimit: 5,
  },
}
```

Notification forwarding requires the Android Notification Listener permission, which the app prompts for during setup.

**Source**: OpenClaw documentation — `platforms/android` (mirror `inbox/openclaw_docs/platforms/android.md`), sections 6–8 + Assistant entrypoints + Notification forwarding
**Last Updated**: 2026-06-22
**Status**: Active
