---
tags:
  - resource
  - documentation
  - claude_code
  - remote_control
  - procedure
keywords:
  - remote control
  - continue local session from phone
  - claude remote-control server mode
  - --remote-control flag
  - connect from another device
  - mobile push notifications
  - outbound-only https
  - remote control troubleshooting
topics:
  - Claude Code
  - Remote Surfaces
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/remote-control
access_control_group: ["general"]
---

# Claude Code — Remote Control

## Overview

**Remote Control** connects [claude.ai/code](https://claude.ai/code) or the Claude mobile app (iOS/Android) to a Claude Code session running on *your machine*, letting you start a task at your desk and pick it up from your phone or another browser. Claude keeps running locally the entire time, so nothing moves to the cloud: the full local environment (filesystem, MCP servers, tools, project config, `@`-autocomplete of file paths) stays available, the conversation stays in sync across all connected devices, and the session reconnects automatically if your laptop sleeps or the network drops. The web and mobile interfaces are just a window into that local session — unlike [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), which runs in Anthropic-managed cloud infrastructure (compared in [Remote Control vs web and deep links](cc_remote_vs_web_and_deep_links.md)).

Remote Control is in research preview and available on all plans. It requires Claude Code **v2.1.51 or later** (`claude --version`). On Team and Enterprise it is off by default until an admin enables the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).

## Requirements

Before using Remote Control, confirm your environment meets these conditions:

- **Subscription**: available on Pro, Max, Team, and Enterprise plans. API keys are not supported. On Team and Enterprise, an admin must first enable the **Remote Control** toggle in admin settings.
- **Authentication**: run `claude` and use `/login` to sign in through claude.ai if you haven't already.
- **Workspace trust**: run `claude` in your project directory at least once to accept the workspace trust dialog.

## Start a Remote Control session

You can start a session from the CLI or the VS Code extension. The CLI offers three invocation modes; VS Code uses `/remote-control`.

**Server mode** — navigate to your project directory and run `claude remote-control`. The process stays running in your terminal in server mode, waiting for remote connections. It displays a session URL you can use to connect from another device, and you can press **spacebar to show a QR code** for quick phone access. While a remote session is active, the terminal shows connection status and tool activity.

```bash
claude remote-control
```

Server-mode flags: `--name "My Project"` (custom session title in the claude.ai/code list); `--remote-control-session-name-prefix <prefix>` (prefix for auto-generated names, defaults to your hostname producing names like `myhost-graceful-unicorn`; `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` does the same); `--spawn <mode>` (how the server creates sessions — `same-dir` default shares the cwd so sessions can conflict editing the same files, `worktree` gives each on-demand session its own [git worktree](https://code.claude.com/docs/en/worktrees) and needs a git repo, `session` serves exactly one session and rejects additional connections; press `w` at runtime to toggle `same-dir`↔`worktree`); `--capacity <N>` (max concurrent sessions, default 32, not usable with `--spawn=session`); `--verbose` (detailed logs); `--sandbox`/`--no-sandbox` (filesystem/network [sandboxing](https://code.claude.com/docs/en/sandboxing), off by default).

**Interactive session** — `claude --remote-control` (or `--rc`) gives a normal interactive terminal session with Remote Control enabled, optionally named via `claude --remote-control "My Project"`. Unlike server mode, you can type messages locally while it is also available remotely. As of v2.1.162 a Remote Control indicator stays in the footer; from v2.1.172 it reads `/rc active` (hidden when the terminal is too narrow; earlier versions always show `Remote Control active`). The indicator is a link to the session on claude.ai — select it with the down arrow and press Enter to open a status panel with the session URL and QR code.

**From an existing session** — run `/remote-control` (or `/rc`) inside a running session to continue it remotely, carrying over your current conversation history; pass a name as an argument to set a title. The `--verbose`, `--sandbox`, and `--no-sandbox` flags are not available with this command.

**VS Code** — in the [VS Code extension](https://code.claude.com/docs/en/vs-code) type `/remote-control` or `/rc` (requires v2.1.79+). A banner above the prompt box shows connection status; click **Open in browser** or find it in the session list. To disconnect, click the banner's close icon or run `/remote-control` again. Unlike the CLI, VS Code does not accept a name argument or display a QR code — the title is derived from conversation history or the first prompt.

### Connect from another device

Once a session is active, connect from another device by: **opening the session URL** in any browser; **scanning the QR code** to open it in the Claude app (with `claude remote-control`, press spacebar to toggle the QR display); or **opening claude.ai/code or the Claude app** and finding the session by name (in the mobile app tap **Code** to reach the session list — Remote Control sessions show a computer icon with a green status dot when online).

The remote session title is chosen in this order: (1) the name passed to `--name`, `--remote-control`, or `/remote-control`; (2) the title set with `/rename`; (3) the last meaningful message in conversation history; (4) an auto-generated name like `myhost-graceful-unicorn`. If you didn't set an explicit name, the title updates to reflect your prompt once you send one. Renaming from claude.ai or the app also updates the local title shown in `claude --resume`. If the environment already has an active session, you'll be asked whether to continue it or start a new one. If you don't have the Claude app yet, run `/mobile` inside Claude Code to display a download QR code.

### Enable Remote Control for all sessions

By default, Remote Control only activates when you explicitly run `claude remote-control`, `claude --remote-control`, or `/remote-control`. To enable it automatically for every interactive session, run `/config` and set **Enable Remote Control for all sessions** to `true` (set back to `false` to disable). In the Desktop app you can also toggle this from **Settings → Claude Code → Enable remote control by default**. With this on, each interactive process registers one remote session; running multiple instances gives each its own environment and session. To run multiple concurrent sessions from a single process, use server mode instead.

## Connection and security

Your local session makes **outbound HTTPS requests only and never opens inbound ports** on your machine. When you start Remote Control it registers with the Anthropic API and polls for work; when you connect from another device, the server routes messages between the web/mobile client and your local session over a streaming connection. All traffic travels through the Anthropic API over **TLS** (the same transport security as any Claude Code session), using **multiple short-lived credentials, each scoped to a single purpose and expiring independently**.

## Mobile push notifications

When Remote Control is active, Claude can send push notifications to your phone (requires v2.1.110+). Claude decides when to push — typically when a long-running task finishes or when it needs a decision to continue — and you can request a push in your prompt (e.g. `notify me when the tests finish`). Beyond the on/off toggle there is no per-event configuration. To set up: (1) install the Claude app for iOS/Android; (2) sign in with the same account and organization you use for Claude Code in the terminal; (3) accept the OS notification permission prompt; (4) run `/config` and enable **Push when Claude decides**.

If notifications don't arrive: if `/config` shows **No mobile registered**, open the Claude app so it can refresh its push token (the warning clears the next time Remote Control connects); on iOS, Focus modes and notification summaries can suppress/delay pushes (check Settings → Notifications → Claude); on Android, exempt the Claude app from battery optimization.

## Limitations

- **One remote session per interactive process** — outside server mode, each Claude Code instance supports one remote session at a time; use server mode for multiple concurrent sessions from a single process.
- **Local process must keep running** — Remote Control runs as a local process; closing the terminal, quitting VS Code, or otherwise stopping the `claude` process ends the session.
- **Extended network outage** — if your machine is awake but can't reach the network for more than ~10 minutes, the session times out and the process exits; run `claude remote-control` again to start a new session.
- **Ultraplan disconnects Remote Control** — starting an [ultraplan](https://code.claude.com/docs/en/ultraplan) session disconnects any active Remote Control session because both occupy the claude.ai/code interface and only one can connect at a time.
- **Some commands are local-only** — commands that open an interactive picker (`/plugin`, `/resume`) work only from the local CLI. Commands that produce text output (`/compact`, `/clear`, `/context`, `/usage`, `/exit`, `/usage-credits`, `/recap`, `/reload-plugins`) work from mobile and web. As of v2.1.166, `/mcp` also works from mobile/web: it returns a text summary of server status instead of opening the picker and accepts the same `reconnect`/`enable`/`disable` subcommands, with one difference — from mobile/web, `/mcp reconnect` with no server name reconnects every server that has failed or needs authentication, while the local CLI requires a server name.

## Troubleshooting

| Error | Cause and fix |
|---|---|
| "Remote Control requires a claude.ai subscription" | Not authenticated with a claude.ai account. Run `claude auth login` and choose the claude.ai option. If `ANTHROPIC_API_KEY` is set, unset it first. |
| "Remote Control requires a full-scope login token" | You're authenticated with a long-lived token from `claude setup-token` or `CLAUDE_CODE_OAUTH_TOKEN` — these are inference-only and cannot establish Remote Control. Run `claude auth login` to authenticate with a full-scope session token. |
| "Unable to determine your organization for Remote Control eligibility" | Cached account info is stale or incomplete. Run `claude auth login` to refresh. |
| "Remote Control is not yet enabled for your account" | The eligibility check can fail with certain env vars: unset `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` / `DISABLE_TELEMETRY`; `CLAUDE_CODE_USE_BEDROCK` / `CLAUDE_CODE_USE_VERTEX` / `CLAUDE_CODE_USE_FOUNDRY` won't work (Remote Control requires claude.ai auth, not third-party providers). If none are set, `/logout` then `/login`. |
| "Remote Control is disabled by your organization's policy" | Four distinct causes (run `/status` first): authenticated with an API key/Console account (use `/login` → claude.ai, unset `ANTHROPIC_API_KEY`); Team/Enterprise admin hasn't enabled the **Remote Control** toggle (a server-side org setting); the admin toggle is grayed out (a data-retention/compliance configuration incompatible with Remote Control — contact Anthropic support); the error mentions `disableRemoteControl` (your IT admin disabled it on this device via [managed settings](https://code.claude.com/docs/en/settings#settings-files)). |
| "Remote credentials fetch failed" | Claude Code couldn't obtain a short-lived credential. Re-run with `--verbose` to see the full error. Common causes: not signed in (run `claude` → `/login`); network/proxy issue (a firewall or proxy may block the outbound HTTPS request — Remote Control needs the Anthropic API on port 443); session creation failed earlier in setup (check your subscription is active). |

```bash
claude remote-control --verbose
```

**Source**: https://code.claude.com/docs/en/remote-control
**Last Updated**: 2026-06-13
**Status**: Active
