---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - browser
keywords:
  - openclaw browser login
  - manual login host browser
  - openclaw chrome profile
  - profile user attach
  - browser-profile openclaw
  - x twitter posting flow
  - sandbox browser allowhostcontrol
  - host browser access sandbox
topics:
  - OpenClaw
  - Browser Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/browser-login
access_control_group: ["general"]
---

# OpenClaw — Manual Browser Login for Browser Automation

## Overview

This note is the OpenClaw procedure for logging into sites that the agent's `browser` tool needs to drive, mirroring the `tools/browser-login` source page. It covers the recommended manual-login flow (sign in yourself; never hand the model your credentials), which Chrome profile OpenClaw controls and when to override it with `profile="user"`, the X/Twitter read/post flow, and how to grant a sandboxed agent access to the host browser via `sandbox.browser.allowHostControl`. The throughline is that authenticated sessions are established by a human in the dedicated host `openclaw` browser profile and then reused by the agent, keeping raw credentials out of the model and reducing anti-bot lockouts.

## Manual Login (Recommended)

When a site requires login, **sign in manually** in the **host** browser profile (the openclaw browser). The page is explicit that you should **not** give the model your credentials: automated logins often trigger anti-bot defenses and can lock the account. The manual sign-in establishes the authenticated session on the dedicated profile, which the agent's later `browser` tool calls then reuse without ever holding the secret. The source links back to the main browser tool docs at `/tools/browser` for the broader tool reference.

## Which Chrome Profile Is Used?

OpenClaw controls a **dedicated Chrome profile** named `openclaw` (rendered with an orange-tinted UI), separate from your daily browser profile. For agent browser tool calls the profile-selection rules are:

- **Default choice:** the agent should use its isolated `openclaw` browser.
- Use `profile="user"` **only** when existing logged-in sessions matter **and** the user is at the computer to click/approve any attach prompt.
- If you have multiple user-browser profiles, specify the profile explicitly instead of guessing.

There are two easy ways to access the dedicated profile. First, **ask the agent to open the browser** and then log in yourself. Second, **open it via CLI**:

```bash
openclaw browser start
openclaw browser open https://x.com
```

If you have multiple profiles, pass `--browser-profile <name>`; the default is `openclaw`.

## X/Twitter: Recommended Flow

For X/Twitter specifically the source recommends the **host** browser (manual login) for both directions of work:

- **Read/search/threads:** use the **host** browser (manual login).
- **Post updates:** use the **host** browser (manual login).

## Sandboxing + Host Browser Access

Sandboxed browser sessions are **more likely** to trigger bot detection, so for X/Twitter and other strict sites the source says to prefer the **host** browser. If the agent is sandboxed, the `browser` tool defaults to the sandbox. To allow host control, set `agents.defaults.sandbox.browser.allowHostControl: true`:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Then open the host browser yourself — CLI invocations always run against the host browser:

```bash
openclaw browser open https://x.com --browser-profile openclaw
```

The agent's `browser` tool calls can then target the host once `sandbox.browser.allowHostControl: true` is set. As an alternative to granting host control, the source notes you can simply disable sandboxing for the agent that posts updates.

**Source**: OpenClaw documentation — `tools/browser-login` (mirror `inbox/openclaw_docs/tools/browser-login.md`)
**Last Updated**: 2026-06-22
**Status**: Active
