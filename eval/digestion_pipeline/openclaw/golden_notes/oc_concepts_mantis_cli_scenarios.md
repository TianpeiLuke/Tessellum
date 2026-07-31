---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - mantis
keywords:
  - openclaw mantis cli
  - pnpm openclaw qa mantis
  - discord-smoke before after run
  - slack-desktop-smoke gateway-setup
  - telegram-desktop-builder
  - openclaw-mantis clawsweeper triggers
  - adding a mantis scenario
  - discord status reactions scenario
topics:
  - OpenClaw
  - Mantis QA
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/mantis
access_control_group: ["general"]
---

# OpenClaw — Running and Authoring Mantis Scenarios (CLI)

## Overview

This note is the **procedure** for running and authoring Mantis live-QA scenarios from the operator side — the `pnpm openclaw qa mantis` command surface, the GitHub workflows and PR-comment triggers that dispatch them, the Discord status-reactions MVP scenario, the existing QA pieces a new scenario builds on, and the checklist for declaring a new scenario. It mirrors the `Command shape`, `Discord MVP`, `Existing QA pieces`, and `Adding a scenario` sections of the `concepts/mantis` source page. The system design those commands operate (goals, ownership, run lifecycle, machines, secrets) is in `oc_concepts_mantis_architecture`; the `mantis-evidence.json` schema and artifact taxonomy they emit are in `oc_concepts_mantis_evidence_model`; the Slack-desktop lane's operator deep-dive is in `oc_concepts_mantis_slack_desktop_runbook`.

## The `pnpm openclaw qa mantis` command surface

All Mantis commands run under `pnpm openclaw qa mantis`. The first local command, **`discord-smoke`**, verifies the Discord bot, guild, channel, message send, reaction send, and artifact path:

```bash
pnpm openclaw qa mantis discord-smoke \
  --output-dir .artifacts/qa-e2e/mantis/discord-smoke
```

The before/after **`run`** subcommand is the local baseline-vs-candidate runner. It creates detached baseline and candidate worktrees under the output directory, installs dependencies, builds each ref, runs the scenario with `--allow-failures`, then writes `baseline/`, `candidate/`, `comparison.json`, and `mantis-report.md`. For the first Discord scenario a successful verification means baseline status is `fail` and candidate status is `pass`:

```bash
pnpm openclaw qa mantis run \
  --transport discord \
  --scenario discord-status-reactions-tool-only \
  --baseline origin/main \
  --candidate HEAD \
  --output-dir .artifacts/qa-e2e/mantis/local-discord-status-reactions
```

A second Discord before/after probe, `--scenario discord-thread-reply-filepath-attachment`, targets thread attachments: it posts a parent message with the driver bot, creates a real Discord thread, calls OpenClaw's `message.thread-reply` action with a repo-local `filePath`, then polls the thread for the SUT reply and attachment filename (baseline screenshot shows no attachment; candidate shows the expected `mantis-thread-report.md` attachment).

The **`desktop-browser-smoke`** subcommand (`pnpm openclaw qa mantis desktop-browser-smoke --output-dir .artifacts/qa-e2e/mantis/desktop-browser`) is the first VM/browser primitive — it leases or reuses a Crabbox desktop machine, starts a visible browser inside the VNC session, captures the desktop, pulls artifacts back, and writes the reconnect command into the report. It defaults to the **Hetzner** provider (the first provider with working desktop/VNC coverage), overridable with `--provider`, `--crabbox-bin`, or `OPENCLAW_MANTIS_CRABBOX_PROVIDER`. Useful desktop smoke flags: `--lease-id <cbx_...>` (or `OPENCLAW_MANTIS_CRABBOX_LEASE_ID`) reuses a warmed desktop; `--browser-url <url>` changes the opened page; `--html-file <path>` renders a repo-local HTML artifact (used to capture the Discord status-reaction timeline); `--browser-profile-dir <remote-path>` reuses a remote Chrome user-data-dir for a persistent logged-in viewer; `--browser-profile-archive-env <name>` restores a base64 `.tgz` Chrome profile from that env var (default `OPENCLAW_MANTIS_BROWSER_PROFILE_TGZ_B64`); `--video-duration <seconds>` controls MP4 length; `--keep-lease` (or `OPENCLAW_MANTIS_KEEP_VM=1`) keeps a passing lease open for VNC inspection (failed runs keep a created lease by default); `--class`, `--idle-timeout`, and `--ttl` tune machine size and lease lifetime. For Discord Web evidence Mantis uses a dedicated viewer account, not a bot token; `OPENCLAW_QA_DISCORD_CAPTURE_UI_METADATA=1` writes a Discord Web URL artifact and `OPENCLAW_QA_DISCORD_KEEP_THREADS=1` keeps the thread open long enough for a logged-in browser to record it.

The **`slack-desktop-smoke`** subcommand is the first full desktop transport primitive — the first Mantis shape where the SUT OpenClaw gateway and the browser both live inside one Linux desktop VM. It leases or reuses a Crabbox desktop, syncs the checkout into the VM, runs `pnpm openclaw qa slack` inside the VM, opens Slack Web in the VNC browser, and copies the Slack QA artifacts plus the VNC screenshot back:

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --output-dir .artifacts/qa-e2e/mantis/slack-desktop \
  --gateway-setup \
  --scenario slack-canary \
  --keep-lease
```

With `--gateway-setup`, the command prepares a persistent disposable OpenClaw home at `$HOME/.openclaw-mantis/slack-openclaw`, patches Slack Socket Mode configuration for the selected channel, starts `openclaw gateway run` on port `38973`, and keeps Chrome running in the VNC session (the "leave me a Linux desktop with Slack and a claw running" mode); without it, the bot-to-bot Slack QA lane is the default. The `--credential-source env` path requires `OPENCLAW_QA_SLACK_CHANNEL_ID`, `OPENCLAW_QA_SLACK_DRIVER_BOT_TOKEN`, `OPENCLAW_QA_SLACK_SUT_BOT_TOKEN`, `OPENCLAW_QA_SLACK_SUT_APP_TOKEN`, and `OPENCLAW_LIVE_OPENAI_KEY` for the remote model lane (if only `OPENAI_API_KEY` is set locally, Mantis maps it to `OPENCLAW_LIVE_OPENAI_KEY` before invoking Crabbox). With `--gateway-setup --credential-source convex`, Mantis leases the Slack SUT credential from the shared pool before creating the VM and forwards the leased channel id, Socket Mode app token, and bot token as `OPENCLAW_MANTIS_SLACK_*` runtime env inside the desktop, so GitHub workflows only need the Convex broker secret. Useful Slack desktop flags: `--lease-id <cbx_...>` reruns against a VM where an operator already logged in to Slack Web; `--keep-lease`/`--no-keep-lease` keep or stop the VM after artifacts; `--slack-url <url>` opens a specific URL (else Mantis derives `https://app.slack.com/client/<team>/<channel>` from Slack `auth.test`); `--slack-channel-id <id>` controls the gateway-setup allowlist; `OPENCLAW_MANTIS_SLACK_BROWSER_PROFILE_DIR` controls the VM Chrome profile (default `$HOME/.config/openclaw-mantis/slack-chrome-profile`); `--credential-source convex --credential-role ci` uses the shared pool; and `--provider-mode`, `--model`, `--alt-model`, `--fast` pass through to the Slack live lane. Approval-checkpoint runs render Slack API message snapshots into checkpoint PNGs for CI-safe proof; `slack-desktop-smoke.png` is only proof of Slack Web when the lease uses a warm, already-logged-in browser profile.

The **`telegram-desktop-builder`** subcommand (`pnpm openclaw qa mantis telegram-desktop-builder --credential-source convex --credential-role maintainer --keep-lease`) is the human-in-the-loop Telegram desktop setup — it leases or reuses a Crabbox desktop, installs the native Linux Telegram Desktop binary, optionally restores a user-session archive, configures OpenClaw with the leased Telegram SUT bot token, starts `openclaw gateway run` on port `38974`, posts a driver-bot readiness message to the leased private group, then captures a screenshot and MP4 from the VNC desktop (a bot token only configures OpenClaw; it never logs Telegram Desktop in). Useful builder flags: `--lease-id <cbx_...>` reruns against a VM where an operator logged in; `--telegram-profile-archive-env <name>` restores a base64 `.tgz` Telegram Desktop profile from that env var; `--telegram-profile-dir <remote-path>` controls the remote profile directory (default `$HOME/.local/share/TelegramDesktop`); `--no-gateway-setup` installs/opens Telegram Desktop without configuring OpenClaw; and `--credential-source convex --credential-role ci` uses the shared broker.

## GitHub workflows and PR-comment triggers

Mantis exposes named GitHub workflows. `Mantis Discord Smoke` is the GitHub smoke workflow; `Mantis Discord Status Reactions` is the before/after workflow for the first real scenario — it accepts `baseline_ref` (the ref expected to reproduce queued-only behavior) and `candidate_ref` (the ref expected to show `queued -> thinking -> done`), checks out the harness ref, builds separate baseline and candidate worktrees, runs `discord-status-reactions-tool-only` against each, and uploads `baseline/`, `candidate/`, `comparison.json`, and `mantis-report.md` as Actions artifacts (it also renders each lane's timeline HTML in a Crabbox desktop browser, embeds `crabbox media preview` GIF previews, links motion-trimmed MP4 clips, and keeps full desktop MP4s; it builds the Crabbox CLI from `openclaw/crabbox` main). `Mantis Scenario` is the generic, intentionally thin manual entrypoint — it takes a `scenario_id`, `candidate_ref`, optional `baseline_ref`, and optional `pr_number`, then dispatches the scenario-owned workflow (each scenario workflow still owns its transport setup, credentials, VM class, expected oracle, and artifact manifest). `Mantis Slack Desktop Smoke` is the first Slack VM workflow (defaults to AWS, with a manual provider input to switch to Hetzner). `Mantis Telegram Live` wraps the Telegram live QA lane in the PR evidence pipeline (QA-evidence visual, not logged-in Telegram Web proof). `Mantis Telegram Desktop Proof` is the agentic native-Telegram-Desktop before/after wrapper that hands the PR, refs, and maintainer instructions to Codex.

Runs can also be triggered from a PR comment. The Discord status-reactions trigger is intentionally narrow (only on pull-request comments from users with write, maintain, or admin access, and only Discord status-reaction requests); by default it uses the known-bad baseline ref and the current PR head SHA as candidate, with optional ref overrides:

```text
@openclaw-mantis discord status reactions
@openclaw-mantis discord status reactions baseline=origin/main candidate=HEAD
@openclaw-mantis telegram
@openclaw-mantis telegram scenario=telegram-status-command
@clawsweeper mantis discord discord-status-reactions-tool-only
@clawsweeper verify e2e discord
```

Telegram live QA defaults to the current PR head SHA as candidate running `telegram-status-command`; maintainers can override `candidate=...`, `provider=aws|hetzner`, and `lease=<cbx_...>`. For ClawSweeper, the first command (`mantis discord <scenario>`) is explicit and scenario-focused; the second (`verify e2e discord`) can later map a PR or issue to recommended scenarios from labels, changed files, and ClawSweeper review findings.

## The Discord status-reactions MVP scenario

The first scenario targets Discord status reactions in guild channels where the source reply delivery mode is `message_tool_only`. It is a good Mantis seed because it is visible in Discord as reactions on the triggering message, has a strong REST oracle through Discord message reaction state, exercises a real OpenClaw Gateway plus Discord bot auth, message dispatch, source reply delivery mode, status reaction state, and model turn lifecycle — and is narrow enough to keep the first implementation honest. The expected scenario shape:

```yaml
id: discord-status-reactions-tool-only
transport: discord
baseline:
  expect:
    reproduced: true
candidate:
  expect:
    fixed: true
config:
  messages:
    ackReaction: "👀"
    ackReactionScope: "group-mentions"
    groupChat:
      visibleReplies: "message_tool"
    statusReactions:
      enabled: true
      timing:
        debounceMs: 0
discord:
  requireMention: true
  notifyChannel: operator-notify
evidence:
  rest:
    messageReactions: true
  browser:
    screenshotMessageRow: true
```

Baseline evidence should show the queued acknowledgement reaction but no lifecycle transition in tool-only mode; candidate evidence should show lifecycle status reactions running when `messages.statusReactions.enabled` is explicitly true. The executable first slice is the opt-in Discord live QA scenario, which configures the SUT with always-on guild handling, `visibleReplies: "message_tool"`, `ackReaction: "👀"`, and explicit status reactions; the oracle polls the real Discord triggering message and expects the observed sequence `👀 -> 🤔 -> 👍`:

```bash
pnpm openclaw qa discord \
  --scenario discord-status-reactions-tool-only \
  --provider-mode live-frontier \
  --model openai/gpt-5.4 \
  --alt-model openai/gpt-5.4 \
  --fast \
  --output-dir .artifacts/qa-e2e/mantis/discord-status-reactions-candidate
```

Artifacts from that run include `discord-qa-reaction-timelines.json`, `discord-status-reactions-tool-only-timeline.html`, and `discord-status-reactions-tool-only-timeline.png`.

## Building on existing QA pieces

Mantis should build on the existing private QA stack instead of starting from zero. `pnpm openclaw qa discord` already runs a live Discord lane with driver and SUT bots; the live transport runner already writes reports, QA evidence, and transport-specific artifacts under `.artifacts/qa-e2e/`; Convex credential leases already provide exclusive access to shared live transport credentials; the browser control service already supports screenshots, snapshots, headless managed profiles, and remote CDP profiles; and QA Lab already has a debugger UI and bus for transport-shaped testing. The first Mantis implementation can therefore be a thin before/after runner over these pieces, plus one visual evidence layer.

## Adding a scenario (declaration checklist)

A Mantis scenario should declare: id and title; transport; required credentials; baseline ref policy; candidate ref policy; OpenClaw config patch; setup steps; stimulus; expected baseline oracle; expected candidate oracle; visual capture targets; timeout budget; and cleanup steps. Scenarios should prefer small, typed oracles: Discord reaction state for reaction bugs; Discord message references for threading bugs; Slack thread ts and reaction API state for Slack bugs; email message ids and headers for email bugs; and browser screenshots when UI is the only reliable observable. Vision checks should be additive — if a platform API can prove the bug, use the API as the pass/fail oracle and keep screenshots for human confidence.

**Source**: OpenClaw documentation — `concepts/mantis` (mirror `inbox/openclaw_docs/concepts/mantis.md`), sections Command shape / Discord MVP / Existing QA pieces / Adding a scenario
**Last Updated**: 2026-06-22
**Status**: Active
