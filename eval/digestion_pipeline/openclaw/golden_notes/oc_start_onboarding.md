---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - onboarding
keywords:
  - openclaw macos onboarding
  - first-run setup flow
  - local vs remote gateway
  - tools.profile coding
  - gateway.remote.token
  - tcc permissions macos
  - global openclaw cli install
  - onboarding chat session
topics:
  - OpenClaw
  - Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/onboarding
access_control_group: ["general"]
---

# OpenClaw — Onboarding (macOS App First-Run Flow)

## Overview

This note documents the **current first-run setup flow for the OpenClaw macOS app**, mirroring the `start/onboarding` source page. The page frames the goal as a smooth "day 0" experience: pick where the Gateway runs, connect auth, run the wizard, and let the agent bootstrap itself. The flow is authored as MDX `<Steps>`, and the seven step titles are the substantive sections of the page; this note walks each step in order — approving the macOS warning, approving find-local-networks, reading the welcome/security notice, choosing Local vs Remote Gateway, granting TCC permissions, optionally installing the global CLI, and the dedicated onboarding chat session. For the path-chooser overview (CLI vs macOS app), the page points to [Onboarding Overview](https://docs.openclaw.ai/start/onboarding-overview).

## First-Run Setup Steps (macOS App)

The macOS app presents the following steps in sequence on first run.

### Step 1 — Approve macOS warning

The first step displays a macOS warning screen that the user approves. The source shows only the macOS warning frame (`01-macos-warning.jpeg`) with no additional configuration text.

### Step 2 — Approve find local networks

The app then asks the user to approve the macOS "find local networks" prompt (`02-local-networks.jpeg`). As with Step 1, the source documents this as an approval-only step.

### Step 3 — Welcome and security notice

A welcome screen presents a security notice (`03-security-notice.png`) that the user should read and decide accordingly. The page enumerates the **security trust model**:

- By default, OpenClaw is a **personal agent**: one trusted operator boundary.
- Shared/multi-user setups require lock-down — split trust boundaries, keep tool access minimal, and follow [Security](https://docs.openclaw.ai/gateway/security).
- Local onboarding now defaults new configs to `tools.profile: "coding"` so fresh local setups keep filesystem/runtime tools without forcing the unrestricted `full` profile.
- If hooks/webhooks or other untrusted content feeds are enabled, use a strong modern model tier and keep strict tool policy/sandboxing.

### Step 4 — Local vs Remote

This step (`04-choose-gateway.png`) asks where the **Gateway** runs. The three options are:

- **This Mac (Local only):** onboarding can configure auth and write credentials locally.
- **Remote (over SSH/Tailnet):** onboarding does **not** configure local auth; credentials must exist on the gateway host. The remote gateway token field stores the token used by the macOS app to connect to that Gateway; existing non-plaintext `gateway.remote.token` values are preserved until you replace them.
- **Configure later:** skip setup and leave the app unconfigured.

The page also gives a **Gateway auth tip**: the wizard now generates a **token** even for loopback, so local WS clients must authenticate; if you disable auth, any local process can connect (use that only on fully trusted machines); and use a **token** for multi-machine access or non-loopback binds.

### Step 5 — Permissions (TCC)

The permissions step (`05-permissions.png`) lets the user choose what permissions to give OpenClaw. Onboarding requests the TCC permissions needed for:

- Automation (AppleScript)
- Notifications
- Accessibility
- Screen Recording
- Microphone
- Speech Recognition
- Camera
- Location

### Step 6 — CLI (optional)

This step is marked optional. The app can install the global `openclaw` CLI via **npm, pnpm, or bun**. It prefers **npm first, then pnpm, then bun** if that is the only detected package manager. For the Gateway runtime, **Node remains the recommended path**.

### Step 7 — Onboarding Chat (dedicated session)

After setup, the app opens a **dedicated onboarding chat session** so the agent can introduce itself and guide next steps. This keeps first-run guidance separate from the user's normal conversation. The page points to [Bootstrapping](https://docs.openclaw.ai/start/bootstrapping) for what happens on the gateway host during the first agent run.

**Source**: OpenClaw documentation — `start/onboarding` (mirror `inbox/openclaw_docs/start/onboarding.md`)
**Last Updated**: 2026-06-22
**Status**: Active
