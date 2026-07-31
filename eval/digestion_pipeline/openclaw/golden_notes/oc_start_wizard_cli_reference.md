---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - onboarding
keywords:
  - openclaw onboard reference
  - wizard cli reference
  - auth and model options
  - secret-input-mode ref
  - gateway-token-ref-env
  - auth-profiles.json
  - wizard rpc start next cancel status
  - openclaw.json outputs
  - remote mode gateway url
  - custom provider onboarding
topics:
  - OpenClaw
  - Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/wizard-cli-reference
access_control_group: ["general"]
---

# OpenClaw — `openclaw onboard` CLI Reference

## Overview

This note is the complete reference procedure for `openclaw onboard`, OpenClaw's local-or-remote onboarding wizard, mirroring the `start/wizard-cli-reference` source page. It documents what the wizard configures, the per-step local flow (existing-config detection and reset scopes, model/auth, workspace, gateway token vs SecretRef, channels and DM pairing, per-OS daemon install, health, skills, finish), remote mode, the full auth/model option matrix (Anthropic, OpenAI Code OAuth / device pairing / API key, xAI Grok ×3, OpenCode, generic key, Vercel/Cloudflare AI Gateway, MiniMax, StepFun, Synthetic, Ollama, Moonshot/Kimi, Custom, Skip), the credential-storage modes (plaintext vs `ref`), and the config outputs in `~/.openclaw/openclaw.json` plus the `wizard.*` gateway RPC internals. For the short guide see the onboarding hub; for the scripted equivalents see the CLI automation note.

## What the wizard does

`openclaw onboard` has two modes. **Local mode (default)** walks you through: model and auth setup (OpenAI Code subscription OAuth, Anthropic Claude CLI or API key, plus MiniMax, GLM, Ollama, Moonshot, StepFun, and AI Gateway options); workspace location and bootstrap files; gateway settings (port, bind, auth, tailscale); channels and providers (Telegram, WhatsApp, Discord, Google Chat, Mattermost, Signal, iMessage, and other bundled channel plugins); daemon install (LaunchAgent, systemd user unit, or native Windows Scheduled Task with Startup-folder fallback); a health check; and skills setup. **Remote mode** configures this machine to connect to a gateway elsewhere — it does not install or modify anything on the remote host.

## Local flow details

The local flow runs as an ordered sequence of steps:

- **Existing config detection** — If `~/.openclaw/openclaw.json` exists, choose Keep, Modify, or Reset. Re-running the wizard does not wipe anything unless you explicitly choose Reset (or pass `--reset`). CLI `--reset` defaults to `config+creds+sessions`; use `--reset-scope full` to also remove workspace. If config is invalid or contains legacy keys, the wizard stops and asks you to run `openclaw doctor` before continuing. Reset uses `trash` and offers scopes: Config only; Config + credentials + sessions; Full reset (also removes workspace).
- **Model and auth** — The full option matrix is in the [Auth and model options](#auth-and-model-options) section below.
- **Workspace** — Default `~/.openclaw/workspace` (configurable). Seeds workspace files needed for first-run bootstrap ritual. Workspace layout is documented at `/concepts/agent-workspace`.
- **Gateway** — Prompts for port, bind, auth mode, and tailscale exposure. Recommended: keep token auth enabled even for loopback so local WS clients must authenticate. In token mode, interactive setup offers **Generate/store plaintext token** (default) or **Use SecretRef** (opt-in). In password mode, interactive setup also supports plaintext or SecretRef storage. The non-interactive token SecretRef path is `--gateway-token-ref-env <ENV_VAR>`, which requires a non-empty env var in the onboarding process environment and cannot be combined with `--gateway-token`. Disable auth only if you fully trust every local process. Non-loopback binds still require auth.
- **Channels** — WhatsApp (`channels/whatsapp`): optional QR login; Telegram (`channels/telegram`): bot token; Discord (`channels/discord`): bot token; Google Chat (`channels/googlechat`): service account JSON + webhook audience; Mattermost (`channels/mattermost`): bot token + base URL; Signal (`channels/signal`): optional `signal-cli` install + account config; iMessage (`channels/imessage`): `imsg` CLI path + Messages DB access (use an SSH wrapper when the Gateway runs off-Mac). DM security defaults to pairing: the first DM sends a code; approve via `openclaw pairing approve <channel> <code>` or use allowlists.
- **Daemon install** — macOS uses a LaunchAgent (requires a logged-in user session; for headless, use a custom LaunchDaemon, which is not shipped). Linux and Windows via WSL2 use a systemd user unit; the wizard attempts `loginctl enable-linger <user>` so the gateway stays up after logout, and may prompt for sudo (writes `/var/lib/systemd/linger`) but tries without sudo first. Native Windows uses a Scheduled Task first; if task creation is denied, OpenClaw falls back to a per-user Startup-folder login item and starts the gateway immediately (Scheduled Tasks remain preferred because they provide better supervisor status). Runtime selection: Node (recommended; required for WhatsApp and Telegram). Bun is not recommended.
- **Health check** — Starts the gateway (if needed) and runs `openclaw health`. `openclaw status --deep` adds the live gateway health probe to status output, including channel probes when supported.
- **Skills** — Reads available skills and checks requirements. Lets you choose node manager: npm, pnpm, or bun. Installs optional dependencies (some use Homebrew on macOS).
- **Finish** — Summary and next steps, including iOS, Android, and macOS app options.

If no GUI is detected, the wizard prints SSH port-forward instructions for the Control UI instead of opening a browser. If Control UI assets are missing, the wizard attempts to build them; the fallback is `pnpm ui:build` (auto-installs UI deps).

## Remote mode details

Remote mode configures this machine to connect to a gateway elsewhere and does not install or modify anything on the remote host. What you set: the remote gateway URL (`ws://...`), and a token if remote gateway auth is required (recommended). If the gateway is loopback-only, use SSH tunneling or a tailnet. Discovery hints: macOS uses Bonjour (`dns-sd`); Linux uses Avahi (`avahi-browse`).

## Auth and model options

The Model-and-auth step presents this option matrix:

- **Anthropic API key** — Uses `ANTHROPIC_API_KEY` if present or prompts for a key, then saves it for daemon use.
- **OpenAI Code subscription (OAuth)** — Browser flow; paste `code#state`. Sets `agents.defaults.model` to `openai/gpt-5.5` through the Codex runtime when model is unset or already OpenAI-family.
- **OpenAI Code subscription (device pairing)** — Browser pairing flow with a short-lived device code. Sets `agents.defaults.model` to `openai/gpt-5.5` through the Codex runtime when model is unset or already OpenAI-family.
- **OpenAI API key** — Uses `OPENAI_API_KEY` if present or prompts for a key, then stores the credential in auth profiles. Sets `agents.defaults.model` to `openai/gpt-5.5` when model is unset, `openai/*`, or legacy Codex model refs.
- **xAI (Grok) OAuth** — Browser sign-in for eligible SuperGrok or X Premium accounts. This is the recommended xAI path for most users. OpenClaw stores the resulting auth profile for Grok models, Grok `web_search`, `x_search`, and `code_execution`.
- **xAI (Grok) device code** — Remote-friendly browser sign-in with a short code instead of a localhost callback. Use this from SSH, Docker, or VPS hosts.
- **xAI (Grok) API key** — Prompts for `XAI_API_KEY` and configures xAI as a model provider. Use this when you want an xAI Console API key instead of subscription OAuth.
- **OpenCode** — Prompts for `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`) and lets you choose the Zen or Go catalog. Setup URL: `opencode.ai/auth`.
- **API key (generic)** — Stores the key for you.
- **Vercel AI Gateway** — Prompts for `AI_GATEWAY_API_KEY`. More detail at `/providers/vercel-ai-gateway`.
- **Cloudflare AI Gateway** — Prompts for account ID, gateway ID, and `CLOUDFLARE_AI_GATEWAY_API_KEY`. More detail at `/providers/cloudflare-ai-gateway`.
- **MiniMax** — Config is auto-written. Hosted default is `MiniMax-M3`; API-key setup uses `minimax/...`, and OAuth setup uses `minimax-portal/...`. More detail at `/providers/minimax`.
- **StepFun** — Config is auto-written for StepFun standard or Step Plan on China or global endpoints. Standard currently includes `step-3.5-flash`, and Step Plan also includes `step-3.5-flash-2603`. More detail at `/providers/stepfun`.
- **Synthetic (Anthropic-compatible)** — Prompts for `SYNTHETIC_API_KEY`. More detail at `/providers/synthetic`.
- **Ollama (Cloud and local open models)** — Prompts for `Cloud + Local`, `Cloud only`, or `Local only` first. `Cloud only` uses `OLLAMA_API_KEY` with `https://ollama.com`. The host-backed modes prompt for base URL (default `http://127.0.0.1:11434`), discover available models, and suggest defaults. `Cloud + Local` also checks whether that Ollama host is signed in for cloud access. More detail at `/providers/ollama`.
- **Moonshot and Kimi Coding** — Moonshot (Kimi K2) and Kimi Coding configs are auto-written. More detail at `/providers/moonshot`.
- **Custom provider** — Works with OpenAI-compatible and Anthropic-compatible endpoints. Interactive onboarding supports the same API-key storage choices as other provider flows: **Paste API key now** (plaintext) or **Use secret reference** (env ref or configured provider ref, with preflight validation). Its non-interactive flags are listed below.
- **Skip** — Leaves auth unconfigured.

The Custom-provider non-interactive flags are:

```text
--auth-choice custom-api-key
--custom-base-url
--custom-model-id
--custom-api-key            (optional; falls back to CUSTOM_API_KEY)
--custom-provider-id        (optional)
--custom-compatibility <openai|openai-responses|anthropic>  (optional; default openai)
--custom-image-input / --custom-text-input  (optional; override inferred model input capability)
```

**Model behavior:** pick a default model from detected options, or enter provider and model manually. Custom-provider onboarding infers image support for common model IDs and asks only when the model name is unknown. When onboarding starts from a provider auth choice, the model picker prefers that provider automatically; for Volcengine and BytePlus the same preference also matches their coding-plan variants (`volcengine-plan/*`, `byteplus-plan/*`). If that preferred-provider filter would be empty, the picker falls back to the full catalog instead of showing no models. The wizard runs a model check and warns if the configured model is unknown or missing auth.

**Credential and profile paths:** Auth profiles (API keys + OAuth) live at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`; the legacy OAuth import source is `~/.openclaw/credentials/oauth.json`.

**Credential storage mode:** Default onboarding behavior persists API keys as plaintext values in auth profiles. `--secret-input-mode ref` enables reference mode instead of plaintext key storage. In interactive setup you can choose either an environment-variable ref (for example `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`) or a configured provider ref (`file` or `exec`) with provider alias + id. Interactive reference mode runs a fast preflight validation before saving: env refs validate the variable name + non-empty value in the current onboarding environment; provider refs validate provider config and resolve the requested id; if preflight fails, onboarding shows the error and lets you retry. In non-interactive mode, `--secret-input-mode ref` is env-backed only — set the provider env var in the onboarding process environment; inline key flags (for example `--openai-api-key`) require that env var to be set, otherwise onboarding fails fast. For custom providers, non-interactive `ref` mode stores `models.providers.<id>.apiKey` as `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`, and in that case `--custom-api-key` requires `CUSTOM_API_KEY` to be set or onboarding fails fast. Gateway auth credentials support plaintext and SecretRef choices in interactive setup (Token mode: Generate/store plaintext token (default) or Use SecretRef; Password mode: plaintext or SecretRef), with the non-interactive token SecretRef path `--gateway-token-ref-env <ENV_VAR>`. Existing plaintext setups continue to work unchanged.

Headless/server tip: complete OAuth on a machine with a browser, then copy that agent's `auth-profiles.json` (for example `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`, or the matching `$OPENCLAW_STATE_DIR/...` path) to the gateway host. `credentials/oauth.json` is only a legacy import source.

## Outputs and internals

Typical fields written into `~/.openclaw/openclaw.json`:

```text
agents.defaults.workspace
agents.defaults.skipBootstrap        (when --skip-bootstrap is passed)
agents.defaults.model / models.providers  (if Minimax chosen)
tools.profile                        (local onboarding defaults to "coding" when unset; existing explicit values preserved)
gateway.*                            (mode, bind, auth, tailscale)
session.dmScope                      (local onboarding defaults to "per-channel-peer" when unset; existing values preserved)
channels.telegram.botToken, channels.discord.token, channels.matrix.*, channels.signal.*, channels.imessage.*
Channel allowlists (Slack, Discord, Matrix, Microsoft Teams)  (when you opt in; names resolve to IDs when possible)
skills.install.nodeManager
wizard.lastRunAt
wizard.lastRunVersion
wizard.lastRunCommit
wizard.lastRunCommand
wizard.lastRunMode
```

The `setup --node-manager` flag accepts `npm`, `pnpm`, or `bun`; manual config can still set `skills.install.nodeManager: "yarn"` later. `openclaw agents add` writes `agents.list[]` and optional `bindings`. WhatsApp credentials go under `~/.openclaw/credentials/whatsapp/<accountId>/`, and sessions are stored under `~/.openclaw/agents/<agentId>/sessions/`. Some channels are delivered as plugins; when selected during setup, the wizard prompts to install the plugin (npm or local path) before channel configuration.

**Gateway wizard RPC** — the wizard exposes a gateway RPC surface so clients (the macOS app and Control UI) can render steps without re-implementing onboarding logic:

```text
wizard.start
wizard.next
wizard.cancel
wizard.status
```

**Signal setup behavior** — onboarding downloads the appropriate release asset, stores it under `~/.openclaw/tools/signal-cli/<version>/`, and writes `channels.signal.cliPath` in config. JVM builds require Java 21; native builds are used when available. Windows uses WSL2 and follows the Linux `signal-cli` flow inside WSL.

**Source**: OpenClaw documentation — `start/wizard-cli-reference` (mirror `inbox/openclaw_docs/start/wizard-cli-reference.md`)
**Last Updated**: 2026-06-22
**Status**: Active
