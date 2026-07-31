---
tags:
  - resource
  - documentation
  - hermes_agent
  - providers
  - setup
keywords:
  - nemotron 3 ultra free
  - nvidia/nemotron-3-ultra:free
  - nous portal free tier
  - desktop app one-click setup
  - cli quick setup
  - free model walkthrough
topics:
  - Hermes Agent
  - Providers & Setup
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/run-nemotron-3-ultra-free
access_control_group: ["general"]
---

# Run Nemotron 3 Ultra Free in Hermes Agent

## Overview

This is the time-boxed walkthrough for running **NVIDIA Nemotron 3 Ultra free** inside Hermes Agent via [Nous Portal](https://portal.nousresearch.com). Nous Research was inducted into the **Nemotron Coalition** of leading AI labs working with NVIDIA on open frontier foundation models; to mark it, Nous partnered with **Nebius** to offer Nemotron 3 Ultra at no cost for two weeks (**June 4th – June 18th**). The model has **day-0 support** in Hermes. The key detail the whole guide turns on: the free tier is the variant tagged `nvidia/nemotron-3-ultra:free` — the `:free` suffix is what keeps it on the no-cost plan, so you must pick that exact variant.

The page gives two install-and-connect paths to the same end state (chatting with the model): **Option A**, the point-and-click **desktop app** (recommended, no terminal); and **Option B**, the **command-line** install + Quick Setup. It then covers switching to the model later from another setup, and troubleshooting the two common snags (model not in the list, browser/remote-host issues). It is a task script, not a concept page: the Portal subscription, the `nous` provider, and the Tool Gateway it routes through are owned by the [full Portal walkthrough](hermes_setup_with_nous_portal.md) and the Nous Portal integration concept; this note links out rather than re-explaining them.

## Option A — Desktop app (recommended)

The simplest path: a one-click installer with a guided, point-and-click setup. No terminal needed.

1. **Download and install.** [Download the Hermes Desktop installer](https://hermes-agent.nousresearch.com/) for macOS or Windows and open it. On first launch it finishes setting itself up (usually under a minute).
2. **Connect Nous Portal.** On the "Let's get you set up" screen, click **Nous Portal** (marked **Recommended**). Your browser opens — create a [Nous Portal](https://portal.nousresearch.com) account (or sign in), choose the **Free** plan, and authorize Hermes. The app connects automatically.
3. **Pick the free Nemotron 3 Ultra model.** After connecting, the app shows a **Default model** card. Click **Change**, search for **nemotron 3 ultra**, and select the variant tagged **Free tier**:

```
nvidia/nemotron-3-ultra:free
```

The `:free` tag is what keeps it on the no-cost tier — pick that variant.

4. **Start chatting.** Click **Start chatting** — you're now talking to Nemotron 3 Ultra, free.

## Option B — Command line

The terminal path: install, run Quick Setup, connect a free Portal account, and select the model.

1. **Install Hermes Agent.** On macOS/Linux/WSL2/Android:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On Windows:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Prefer to review first? Download [`install.sh`](https://hermes-agent.nousresearch.com/install.sh), inspect it, then run it. After it finishes, reload your shell:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

2. **Run Quick Setup.** Run `hermes setup` and select **Quick Setup**. Hermes opens a browser tab and waits for you to finish the next steps.
3. **Create a Nous Portal account.** In the browser, create a [Nous Portal](https://portal.nousresearch.com) account (or sign in) and choose the **Free** plan.
4. **Connect your account.** When prompted to connect your account to Hermes Agent, click **Connect**. You'll see a confirmation once it's linked.
5. **Select the free Nemotron 3 Ultra model.** Return to your terminal and select `nvidia/nemotron-3-ultra:free` from the model list — again, the `:free` tag is what keeps it on the no-cost tier.
6. **Start chatting.** Complete the remaining Quick Setup prompts, then run `hermes`. You're now talking to Nemotron 3 Ultra, free.

## Switching to it later

Already set up with another model?

- **Desktop app:** open the model picker, search for **nemotron 3 ultra**, and select the **Free tier** variant.
- **CLI / TUI:** switch any time from inside a session with `/model nvidia/nemotron-3-ultra:free`, or run `/model` to open the picker and choose it from the list.

## Troubleshooting

- **Don't see the model in the list?** Make sure you finished the Nous Portal connection and that you're on the **Free** plan. In the CLI, `hermes portal info` confirms you're logged in and routing through Nous.
- **Picked the wrong variant?** Re-select `nvidia/nemotron-3-ultra:free` — the `:free` suffix is required to stay on the no-cost tier.
- **Browser didn't open / you're on a remote host (CLI)?** See [OAuth over SSH / Remote Hosts](hermes_oauth_over_ssh.md) for port-forwarding and manual-paste workarounds.

## See also

- **[Desktop App](hermes_desktop_app.md)** — the native one-click app (macOS, Windows, Linux).
- **[Run Hermes Agent with Nous Portal](hermes_setup_with_nous_portal.md)** — full Portal walkthrough: models, Tool Gateway, and verification.
- **[Nous Portal integration](hermes_nous_portal_subscription.md)** — what's in the subscription.
- **[Quickstart](hermes_quickstart_first_chat.md)** — install-to-chat in under 5 minutes.

**Source**: `inbox/hermes_agent_docs/guides/run-nemotron-3-ultra-free.md` · https://hermes-agent.nousresearch.com/docs/guides/run-nemotron-3-ultra-free
**Last Updated**: 2026-06-19
**Status**: Active
