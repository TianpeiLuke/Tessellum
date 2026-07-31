---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - onboarding
keywords:
  - openclaw onboard
  - cli onboarding wizard
  - quickstart vs advanced
  - what onboarding configures
  - openclaw agents add
  - onboarding locale
  - openclaw configure
  - reset scope onboarding
topics:
  - OpenClaw
  - CLI Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/wizard
access_control_group: ["general"]
---

# OpenClaw — CLI Onboarding Hub (`openclaw onboard`)

## Overview

This note documents the OpenClaw **CLI onboarding hub** — the `openclaw onboard` guided flow that is the **recommended** terminal setup path for OpenClaw on macOS, Linux, or Windows. It configures a local Gateway (or a remote Gateway connection) plus channels, skills, and workspace defaults in one guided flow, mirroring the `start/wizard` source page. It covers locale resolution, the QuickStart-vs-Advanced choice, the seven things local-mode onboarding configures (Model/Auth → Workspace → Gateway → Channels → Daemon → Health → Skills), remote mode, adding another agent with `openclaw agents add`, and the pointers to the deeper references. The detailed per-step breakdown lives in the companion reference note ([oc_start_wizard_cli_reference](oc_start_wizard_cli_reference.md)), and the scripted equivalents live in ([oc_start_wizard_cli_automation](oc_start_wizard_cli_automation.md)).

## Starting onboarding

CLI onboarding is launched with a single command. Windows desktop users can also start with the Windows Hub (`/platforms/windows`).

```bash
openclaw onboard
```

To reconfigure later (without re-running the full first-time flow) or to add a second agent:

```bash
openclaw configure
openclaw agents add <name>
```

Two flag notes from the source apply across the flow: `--json` does **not** imply non-interactive mode — for scripts you must use `--non-interactive`; and the fastest first chat needs no channel setup at all — run `openclaw dashboard` and chat in the browser Control UI (Docs: `/web/dashboard`). CLI onboarding also includes a **web search step** where you can pick a provider such as Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax Search, Ollama Web Search, Perplexity, SearXNG, or Tavily; some require an API key and others are key-free, and it can be configured later with `openclaw configure --section web` (Docs: `/tools/web`).

## Locale

The CLI wizard localizes fixed onboarding copy. It resolves locale from `OPENCLAW_LOCALE`, then `LC_ALL`, then `LC_MESSAGES`, then `LANG`, and falls back to English. Supported wizard locales are `en`, `zh-CN`, and `zh-TW`. To force a locale for one run:

```bash
OPENCLAW_LOCALE=zh-CN openclaw onboard
```

Names and stable identifiers stay literal and are **not** translated: `OpenClaw`, `Gateway`, `Tailscale`, commands, config keys, URLs, provider IDs, model IDs, and plugin/channel labels.

## QuickStart vs Advanced

Onboarding starts by asking you to choose between **QuickStart** (defaults) and **Advanced** (full control). The QuickStart defaults, taken verbatim from the source, are: a local gateway (loopback); the workspace default (or an existing workspace); Gateway port **18789**; Gateway auth **Token** (auto-generated, even on loopback); tool policy default for new local setups of `tools.profile: "coding"` (an existing explicit profile is preserved); a DM isolation default where local onboarding writes `session.dmScope: "per-channel-peer"` when unset (details: `/start/wizard-cli-reference#outputs-and-internals`); Tailscale exposure **Off**; and Telegram + WhatsApp DMs defaulting to **allowlist** (you will be prompted for your phone number). The **Advanced** path instead exposes every step — mode, workspace, gateway, channels, daemon, and skills.

## What onboarding configures

**Local mode (the default)** walks you through these seven steps in order:

1. **Model/Auth** — choose any supported provider/auth flow (API key, OAuth, or provider-specific manual auth), including a Custom Provider (OpenAI-compatible, Anthropic-compatible, or Unknown auto-detect), then pick a default model. Security note from the source: if this agent will run tools or process webhook/hooks content, prefer the strongest latest-generation model available and keep tool policy strict, because weaker/older tiers are easier to prompt-inject. For non-interactive runs, `--secret-input-mode ref` stores env-backed refs in auth profiles instead of plaintext API-key values, and in `ref` mode the provider env var must be set (passing inline key flags without that env var fails fast). In interactive runs, choosing secret reference mode lets you point at either an environment variable or a configured provider ref (`file` or `exec`), with a fast preflight validation before saving. For Anthropic specifically, interactive onboarding/configure offers **Anthropic Claude CLI** as the preferred local path and **Anthropic API key** as the recommended production path; Anthropic setup-token also remains available as a supported token-auth path.
2. **Workspace** — the location for agent files (default `~/.openclaw/workspace`). Seeds bootstrap files.
3. **Gateway** — port, bind address, auth mode, and Tailscale exposure. In interactive token mode, choose default plaintext token storage or opt into SecretRef; the non-interactive token SecretRef path is `--gateway-token-ref-env <ENV_VAR>`.
4. **Channels** — built-in and official plugin chat channels such as iMessage, Discord, Feishu, Google Chat, Mattermost, Microsoft Teams, QQ Bot, Signal, Slack, Telegram, WhatsApp, and more.
5. **Daemon** — installs a LaunchAgent (macOS), systemd user unit (Linux/WSL2), or native Windows Scheduled Task with a per-user Startup-folder fallback. If token auth requires a token and `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist the resolved token into supervisor service environment metadata; if that token SecretRef is unresolved, daemon install is blocked with actionable guidance; and if both `gateway.auth.token` and `gateway.auth.password` are configured while `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly.
6. **Health check** — starts the Gateway and verifies it is running.
7. **Skills** — installs recommended skills and optional dependencies.

Re-running onboarding does **not** wipe anything unless you explicitly choose **Reset** (or pass `--reset`). CLI `--reset` defaults to config, credentials, and sessions; use `--reset-scope full` to include the workspace. If the config is invalid or contains legacy keys, onboarding asks you to run `openclaw doctor` first.

**Remote mode** only configures the local client to connect to a Gateway elsewhere; it does **not** install or change anything on the remote host.

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running it without `--workspace` launches onboarding. What it sets: `agents.list[].name`, `agents.list[].workspace`, and `agents.list[].agentDir`. Per the source notes, default workspaces follow `~/.openclaw/workspace-<agentId>`; add `bindings` to route inbound messages (onboarding can do this); and the non-interactive flags are `--model`, `--agent-dir`, `--bind`, and `--non-interactive`.

## Full reference

For detailed step-by-step breakdowns and config outputs, see the CLI Setup Reference (`/start/wizard-cli-reference`); for non-interactive examples, see CLI Automation (`/start/wizard-cli-automation`); and for the deeper technical reference including RPC details, see the Onboarding Reference (`/reference/wizard`). The source page also links the CLI command reference for `openclaw onboard` (`/cli/onboard`), the Onboarding Overview (`/start/onboarding-overview`), the macOS app onboarding (`/start/onboarding`), and the agent first-run ritual / Agent Bootstrapping (`/start/bootstrapping`).

**Source**: OpenClaw documentation — `start/wizard` (mirror `inbox/openclaw_docs/start/wizard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
