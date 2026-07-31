---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - install
keywords:
  - openclaw first-run install
  - hackable git install --install-method git
  - openclaw onboard --install-daemon
  - node 22 runtime requirement
  - raspberry pi vps vm hosting
  - stable beta dev channels openclaw update
  - migrate openclaw state dir mac mini
  - docs.openclaw.ai ssl xfinity block
  - openclaw npm vs git install switch
topics:
  - OpenClaw
  - First-run FAQ
  - Install & Hosting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq-first-run
access_control_group: ["general"]
---

# OpenClaw — First-Run FAQ: Install, Runtime & Hosting

## Overview

This note is the **install / runtime / hosting** half of the OpenClaw first-run FAQ (`help/faq-first-run`, the "Quick start and first-run setup" `<AccordionGroup>`): how to install and onboard, what runtime and hardware you need, the git-vs-npm install choice and how to switch between them, recovering a stuck onboarding, self-updating across stable/beta/dev channels, migrating an existing setup to a new machine, and the common Windows / docs-SSL / Bun gotchas. The auth, subscription, provider, and dashboard Q&As from the same page are covered in the sibling note [oc_help_faq_first_run_auth](oc_help_faq_first_run_auth.md); everyday operations live in the main FAQ cluster (notes `oc_help_faq_*`).

## Recommended install and onboarding path

The repo recommends running from source and using onboarding. The fastest supported path is the install one-liner followed by `onboard`:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

The wizard can also build UI assets automatically. After onboarding you typically run the Gateway on port **18789**. For contributors / dev, install from a manual clone instead: `git clone https://github.com/openclaw/openclaw.git`, then `cd openclaw`, `pnpm install`, `pnpm build`, `pnpm ui:build`, `openclaw onboard`. If you do not have a global install yet, run it via `pnpm openclaw onboard`. Install ≈ **2–5 minutes**; onboarding ≈ **5–15 minutes** depending on how many channels/models you configure.

**What onboarding does:** `openclaw onboard` is the recommended setup path; in **local mode** it walks you through model/auth setup (provider OAuth, API keys, Anthropic setup-token, plus local-model options such as LM Studio), workspace location + bootstrap files, Gateway settings (bind/port/auth/tailscale), channels (WhatsApp, Telegram, Discord, Mattermost, Signal, iMessage, plus bundled channel plugins like QQ Bot), daemon install (LaunchAgent on macOS; systemd user unit on Linux/WSL2), and health checks + skills selection. It also warns if your configured model is unknown or missing auth.

## Hackable (git) install vs npm install

- **Hackable (git) install** — full source checkout, editable, best for contributors; you run builds locally and can patch code/docs.
- **npm install** — global CLI install, no repo, best for "just run it"; updates come from npm dist-tags.

The git install is also the recommended debugging posture: it gives a local AI agent (Claude Code, OpenAI Codex) the full source + docs so it can reason about the exact version you are running. Force the git checkout with the installer flag:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

**Switching between modes later** is non-destructive — it only changes the OpenClaw code install; your state (`~/.openclaw`) and workspace (`~/.openclaw/workspace`) stay untouched. Use `openclaw update --channel dev` to move from npm to git, and `openclaw update --channel stable` to move from git back to npm. Add `--dry-run` to preview the planned mode switch first; the updater runs Doctor follow-ups, refreshes plugin sources for the target channel, and restarts the gateway unless you pass `--no-restart`. The installer can also force either mode directly with `--install-method git` or `--install-method npm`.

## Runtime requirements

Node **>= 22** is required; `pnpm` is recommended. **Bun is not recommended** for the Gateway — there are runtime bugs, especially with WhatsApp and Telegram, so use Node for stable gateways; if you still want to experiment with Bun, do it on a non-production gateway without WhatsApp/Telegram. On Linux, if you run OpenClaw via systemd, ensure the service PATH includes Homebrew's prefix (e.g. `/home/linuxbrew/.linuxbrew/bin`) so `brew`-installed tools resolve in non-login shells; recent builds also prepend common user bin dirs (`~/.local/bin`, `~/.npm-global/bin`, `~/.local/share/pnpm`, `~/.bun/bin`) and honor `PNPM_HOME`, `NPM_CONFIG_PREFIX`, `BUN_INSTALL`, `VOLTA_HOME`, `ASDF_DATA_DIR`, `NVM_DIR`, and `FNM_DIR` when set.

## Hardware and hosting choices

The Gateway is lightweight. Docs list **512MB–1GB RAM, 1 core, and about 500MB disk** as enough for personal use, and note that a **Raspberry Pi 4 can run it**; **2GB is recommended** for extra headroom (logs, media, other services) but is not a hard minimum. For VPS hosting, the absolute minimum is **1 vCPU / 1GB RAM / ~500MB disk** and the recommendation is **1–2 vCPU / 2GB RAM or more** (Node tools and browser automation can be resource-hungry); use **Ubuntu LTS** (or any modern Debian/Ubuntu) as the best-tested Linux path. A VM follows the same guidance as a VPS — always on, reachable, enough RAM — with a baseline of 1 vCPU/1GB minimum and 2GB recommended.

**Where to run the Gateway** — for 24/7 reliability use a VPS; for lowest friction (and if sleep/restarts are acceptable) run it locally:

- **Laptop (local Gateway):** pros — no server cost, direct local-file access, live browser window; cons — sleep/network drops disconnect, OS updates/reboots interrupt, the machine must stay awake.
- **VPS / cloud:** pros — always-on, stable network, no laptop-sleep issues, easier to keep running; cons — often headless (use screenshots), remote file access only, must SSH for updates. WhatsApp/Telegram/Slack/Mattermost/Discord all work fine from a VPS; the only real trade-off is headless browser vs a visible window.

A dedicated host (VPS / Mac mini / Raspberry Pi) is **not required but recommended** for reliability and isolation. **No Mac mini is required** — OpenClaw runs on macOS or Linux (Windows via WSL2); you only need a Mac for macOS-only tools. For iMessage you need *some* macOS device signed into Messages (any Mac, not specifically a mini): run the Gateway on that Mac, or run it elsewhere and set `channels.imessage.cliPath` to an SSH wrapper that runs `imsg` on the Mac. In any of these hosting layouts you can pair **nodes** (Mac/iOS/Android/headless) on your laptop/phone to a remote Gateway for local screen/camera/canvas or `system.run` command execution, while keeping the Gateway always-on elsewhere; check them with `openclaw nodes status` / `openclaw nodes list`. Raspberry Pi installs work but expect rough edges: use a **64-bit** OS, keep Node >= 22, prefer the hackable (git) install for fast logs/updates, start without channels/skills then add them one by one, and treat weird binary failures as likely **ARM compatibility** problems.

## Update channels: stable, beta, and dev

**Stable** and **beta** are **npm dist-tags, not separate code lines** — `latest` = stable, `beta` = early build for testing. A stable release usually lands on `beta` first, then an explicit promotion step moves that same version to `latest` (maintainers can also publish straight to `latest`), which is why beta and stable can point at the **same version** after promotion. **Dev** is the moving head of `main` (git); when published it uses the npm dist-tag `dev`. Install one-liners (macOS/Linux):

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
openclaw update --channel dev   # dev channel: switches to the main branch, updates from source
```

The Windows installer is the PowerShell script at `https://openclaw.ai/install.ps1`.

**Asking OpenClaw to update itself** is *possible but not recommended* — the update flow can restart the Gateway (dropping the active session), may need a clean git checkout, and can prompt for confirmation; running updates from a shell as the operator is safer. The CLI surface is `openclaw update`, `openclaw update status`, `openclaw update --channel stable|beta|dev`, `openclaw update --tag <dist-tag|version>`, and `openclaw update --no-restart`. If you must automate from an agent, run `openclaw update --yes --no-restart` followed by `openclaw gateway restart`. To see what changed, read the GitHub `CHANGELOG.md` (newest at top; if the top section is **Unreleased**, the next dated section is the latest shipped version; entries are grouped **Highlights / Changes / Fixes**).

## Recovering a stuck onboarding or install

If onboarding is stuck on "wake up my friend" / "will not hatch", the screen depends on the Gateway being reachable and authenticated (the TUI auto-sends "Wake up, my friend!" on first hatch). If you see that line with **no reply** and tokens stay at 0, the agent never ran. The recovery loop is: (1) `openclaw gateway restart`; (2) check status + auth with `openclaw status`, `openclaw models status`, `openclaw logs --follow`; (3) if it still hangs, `openclaw doctor`. If the Gateway is remote, ensure the tunnel/Tailscale connection is up and the UI points at the right Gateway.

The general "I am stuck" remedy is to use a local AI agent that can **see your machine** (Claude Code or OpenAI Codex) rather than asking in Discord, because most "I'm stuck" cases are local config/environment issues a remote helper cannot inspect. Give the agent the full source via the hackable git install (`--install-method git`), ask it to plan and supervise the fix step-by-step, and share these outputs: `openclaw status` (gateway/agent health + basic config), `openclaw models status` (provider auth + model availability), `openclaw doctor` (validates and repairs common config/state issues). Other useful checks: `openclaw status --all`, `openclaw logs --follow`, `openclaw gateway status`, `openclaw health --verbose`.

**Installer stuck — get more feedback** by re-running with `--verbose` (e.g. `curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose`, or add `--beta --verbose` / `--install-method git --verbose`). On Windows (PowerShell) there is no dedicated `-Verbose` flag yet; wrap the run with `Set-PSDebug -Trace 1` … `Set-PSDebug -Trace 0` around the `install.ps1` script block invoked with `-NoOnboard`.

## Heartbeat skip reasons

When the heartbeat keeps skipping, the common skip reasons are: `quiet-hours` (outside the configured active-hours window); `empty-heartbeat-file` (`HEARTBEAT.md` exists but only contains blank, comment, header, fence, or empty-checklist scaffolding); `no-tasks-due` (task mode is active but no task intervals are due yet); and `alerts-disabled` (all heartbeat visibility is disabled — `showOk`, `showAlerts`, and `useIndicator` are all off). In task mode, due timestamps advance only after a real heartbeat run completes; skipped runs do not mark tasks as completed.

## Migrating to a new machine without redoing onboarding

You can migrate to a new machine (e.g. a Mac mini) without redoing onboarding by copying the **state directory** and **workspace**, then running Doctor once. The steps: (1) install OpenClaw on the new machine; (2) copy `$OPENCLAW_STATE_DIR` (default `~/.openclaw`) from the old machine; (3) copy your workspace (default `~/.openclaw/workspace`); (4) run `openclaw doctor` and restart the Gateway service. That preserves config, auth profiles, WhatsApp creds, sessions, and memory. **Important:** if you only commit/push your workspace to GitHub you are backing up memory + bootstrap files, **not** session history or auth — those live under `~/.openclaw/` (for example `~/.openclaw/agents/<agentId>/sessions/`). In remote mode the gateway host owns the session store and workspace.

## Windows and docs-access gotchas

- **`git not found` / `openclaw not recognized` on Windows** — install **Git for Windows** and ensure `git` is on PATH, then close/reopen PowerShell and re-run the installer. If `openclaw` is unrecognized after install, your npm global bin folder is not on PATH: check it with `npm config get prefix`, add that directory to your user PATH (no `\bin` suffix needed on Windows; usually `%AppData%\npm`), then close/reopen PowerShell. For desktop setup use the native **Windows Hub** app; for terminal-only setup the PowerShell installer and WSL2 Gateway paths are both supported.
- **Garbled Chinese (mojibake) in Windows exec output** — usually a console code-page mismatch on native Windows shells. Quick PowerShell workaround: run `chcp 65001` and set `[Console]::InputEncoding`, `[Console]::OutputEncoding`, and `$OutputEncoding` to a no-BOM `UTF8Encoding`, then `openclaw gateway restart` and retry. If it still reproduces on latest, track Issue #30640.
- **Cannot access `docs.openclaw.ai` (SSL error)** — some Comcast/Xfinity connections incorrectly block `docs.openclaw.ai` via Xfinity Advanced Security; disable it or allowlist the host and retry. The docs are also mirrored on GitHub at `github.com/openclaw/openclaw/tree/main/docs`.
- **Docs did not answer your question** — use the hackable (git) install so the full source + docs are local, then ask your bot (or Claude/Codex) *from that folder* so it can read the repo and answer precisely.

**Source**: OpenClaw documentation — `help/faq-first-run` (install/runtime/hosting cluster; mirror `inbox/openclaw_docs/help/faq-first-run.md`)
**Last Updated**: 2026-06-22
**Status**: Active
