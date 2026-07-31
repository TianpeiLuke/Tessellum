---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - getting_started
keywords:
  - openclaw getting started
  - openclaw quickstart install
  - openclaw onboard install-daemon
  - openclaw gateway status port 18789
  - openclaw dashboard control ui
  - install.sh powershell install.ps1
  - gateway.controlUi.root custom control ui
  - openclaw_home state_dir config_path env vars
topics:
  - OpenClaw
  - Getting Started
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/getting-started
access_control_group: ["general"]
---

# OpenClaw — Getting Started Quickstart (Install to First Chat)

## Overview

This note is the OpenClaw quickstart procedure: the ~5-minute path from a clean machine to a running Gateway, configured auth, and a working chat session — mirroring the `start/getting-started` source page. It covers the prerequisites (Node.js plus a model-provider API key), the five-step quick setup (install via shell/PowerShell script → run onboarding → verify the Gateway → open the dashboard → send the first message), the advanced custom Control UI mount, and the optional environment variables for service-account or custom-path installs. By the end you have a running Gateway, configured auth, and a working chat session.

## What you need

Two prerequisites are required before running the quickstart:

- **Node.js** — Node 24 recommended (Node 22.19+ also supported). Check your version with `node --version`. To install Node, see [Node setup](https://docs.openclaw.ai/install/node).
- **An API key** from a model provider (Anthropic, OpenAI, Google, etc.) — onboarding will prompt you for it.

**Windows users:** the native Windows Hub app is the easiest desktop path. The PowerShell installer and WSL2 Gateway paths are also supported (see [Windows](https://docs.openclaw.ai/platforms/windows)).

## Quick setup

The quickstart is a five-step `<Steps>` flow. Run the steps in order; the whole flow takes about 5 minutes (onboarding itself is ~2 minutes).

### Step 1 — Install OpenClaw

On macOS / Linux, install with the shell installer:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

On Windows, install with the PowerShell installer:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Other install methods (Docker, Nix, npm) are documented at [Install](https://docs.openclaw.ai/install).

### Step 2 — Run onboarding (`openclaw onboard --install-daemon`)

Run `openclaw onboard --install-daemon`. The wizard walks you through choosing a model provider, setting an API key, and configuring the Gateway. It takes about 2 minutes. See [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard) for the full reference.

### Step 3 — Verify the Gateway is running (`openclaw gateway status`)

Run `openclaw gateway status`. You should see the Gateway listening on port `18789`.

### Step 4 — Open the dashboard (`openclaw dashboard`)

Run `openclaw dashboard`. This opens the Control UI in your browser. If it loads, everything is working.

### Step 5 — Send your first message

Type a message in the Control UI chat and you should get an AI reply. Want to chat from your phone instead? The fastest channel to set up is [Telegram](https://docs.openclaw.ai/channels/telegram) (just a bot token). See [Channels](https://docs.openclaw.ai/channels) for all options.

## Advanced: mount a custom Control UI build

If you maintain a localized or customized dashboard build, point `gateway.controlUi.root` to a directory that contains your built static assets and `index.html`. First create the directory and copy your built static files into it:

```bash
mkdir -p "$HOME/.openclaw/control-ui-custom"
# Copy your built static files into that directory.
```

Then set the config:

```json
{
  "gateway": {
    "controlUi": {
      "enabled": true,
      "root": "$HOME/.openclaw/control-ui-custom"
    }
  }
}
```

Finally, restart the gateway and reopen the dashboard:

```bash
openclaw gateway restart
openclaw dashboard
```

## Advanced: environment variables

If you run OpenClaw as a service account or want custom paths, these environment variables override the default path resolution:

- `OPENCLAW_HOME` — home directory for internal path resolution
- `OPENCLAW_STATE_DIR` — override the state directory
- `OPENCLAW_CONFIG_PATH` — override the config file path

Full reference: [Environment variables](https://docs.openclaw.ai/help/environment).

## What to do next

After the first chat works, the source page offers four follow-up `<Card>` paths (covered in their home docs, not duplicated here):

- **Connect a channel** ([/channels](https://docs.openclaw.ai/channels)) — Discord, Feishu, iMessage, Matrix, Microsoft Teams, Signal, Slack, Telegram, WhatsApp, Zalo, and more.
- **Pairing and safety** ([/channels/pairing](https://docs.openclaw.ai/channels/pairing)) — control who can message your agent.
- **Configure the Gateway** ([/gateway/configuration](https://docs.openclaw.ai/gateway/configuration)) — models, tools, sandbox, and advanced settings.
- **Browse tools** ([/tools](https://docs.openclaw.ai/tools)) — browser, exec, web search, skills, and plugins.

**Source**: OpenClaw documentation — `start/getting-started` (mirror `inbox/openclaw_docs/start/getting-started.md`)
**Last Updated**: 2026-06-22
**Status**: Active
