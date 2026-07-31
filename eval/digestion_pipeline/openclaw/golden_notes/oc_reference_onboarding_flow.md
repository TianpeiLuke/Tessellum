---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - onboarding
keywords:
  - openclaw onboard wizard flow
  - interactive onboarding steps
  - non-interactive onboarding flags
  - openclaw onboard --non-interactive
  - openclaw agents add
  - gateway auth token secretref
  - model auth provider selection
  - daemon install launchagent systemd
topics:
  - OpenClaw
  - Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/wizard
access_control_group: ["general"]
---

# OpenClaw — The `openclaw onboard` Interactive Flow and Non-Interactive Automation

## Overview

This note documents the `openclaw onboard` reference flow as a step-by-step procedure: the ten interactive local-mode steps the wizard walks through, the non-interactive (`--non-interactive`) automation flag set, and the `openclaw agents add` sub-command for adding a second agent without prompts. It mirrors the `reference/wizard` source page sections **Flow details (local mode)** (the ten `<Step>` blocks), **Non-interactive mode**, and **Add agent (non-interactive)**. The companion outputs/integration surface — what onboarding writes to `~/.openclaw/openclaw.json`, the Gateway `wizard.*` RPC, and the `signal-cli` install — lives in the sibling note **oc_reference_onboarding_outputs**, not here. For the high-level overview the source page itself points at `/start/wizard`.

## Flow Details (Local Mode) — The Ten Steps

The interactive `openclaw onboard` flow runs ten ordered `<Step>` blocks. Each step is a configuration decision; the wizard then writes the resulting config (see the outputs note).

### Step 1 — Existing config detection

If `~/.openclaw/openclaw.json` exists, the wizard offers **Keep current values**, **Review and update**, or **Reset before setup**. Re-running onboarding does **not** wipe anything unless you explicitly choose **Reset** (or pass `--reset`). The CLI `--reset` defaults to `config+creds+sessions`; use `--reset-scope full` to also remove the workspace. If the config is invalid or contains legacy keys, the wizard stops and asks you to run `openclaw doctor` before continuing. Reset uses `trash` (never `rm`) and offers scopes: Config only; Config + credentials + sessions; Full reset (also removes workspace).

### Step 2 — Model/Auth

This step picks the model provider and stores its credentials; storage defaults to plaintext auth-profile values, and `--secret-input-mode ref` stores env-backed refs instead (for example `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`). The provider choices and their behaviors are:

- **Anthropic API key**: uses `ANTHROPIC_API_KEY` if present or prompts for a key, then saves it for daemon use; this is the preferred Anthropic assistant choice in onboarding/configure.
- **Anthropic setup-token**: still available in onboarding/configure, though OpenClaw now prefers Claude CLI reuse when available.
- **OpenAI Code (Codex) subscription (OAuth)**: browser flow; paste the `code#state`. Sets `agents.defaults.model` to `openai/gpt-5.5` through the Codex runtime when model is unset or already OpenAI-family.
- **OpenAI Code (Codex) subscription (device pairing)**: browser pairing flow with a short-lived device code; sets `agents.defaults.model` to `openai/gpt-5.5` through the Codex runtime when model is unset or already OpenAI-family.
- **OpenAI API key**: uses `OPENAI_API_KEY` if present or prompts for a key, then stores it in auth profiles; sets `agents.defaults.model` to `openai/gpt-5.5` when model is unset, `openai/*`, or legacy Codex model refs.
- **xAI (Grok) OAuth / API key**: signs in with xAI OAuth when chosen, or prompts for `XAI_API_KEY` on the API-key path, and configures xAI as a model provider.
- **OpenCode**: prompts for `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`) and lets you pick the Zen or Go catalog.
- **Ollama**: offers **Cloud + Local**, **Cloud only**, or **Local only** first. `Cloud only` prompts for `OLLAMA_API_KEY` and uses `https://ollama.com`; the host-backed modes prompt for the Ollama base URL, discover available models, and auto-pull the selected local model when needed; `Cloud + Local` also checks whether that Ollama host is signed in for cloud access.
- **API key**: stores the key for you.
- **Vercel AI Gateway (multi-model proxy)**: prompts for `AI_GATEWAY_API_KEY`.
- **Cloudflare AI Gateway**: prompts for Account ID, Gateway ID, and `CLOUDFLARE_AI_GATEWAY_API_KEY`.
- **MiniMax**: config is auto-written; hosted default is `MiniMax-M3`. API-key setup uses `minimax/...`, and OAuth setup uses `minimax-portal/...`.
- **StepFun**: config is auto-written for StepFun standard or Step Plan on China or global endpoints. Standard currently includes `step-3.5-flash`, and Step Plan also includes `step-3.5-flash-2603`.
- **Synthetic (Anthropic-compatible)**: prompts for `SYNTHETIC_API_KEY`.
- **Moonshot (Kimi K2)** and **Kimi Coding**: config is auto-written.
- **Skip**: no auth configured yet.

After provider selection you pick a default model from detected options (or enter `provider/model` manually); the source advises choosing the strongest latest-generation model available for best quality and lower prompt-injection risk. Onboarding then runs a model check and warns if the configured model is unknown or missing auth. Auth profiles live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (API keys + OAuth); `~/.openclaw/credentials/oauth.json` is legacy import-only. Headless/server tip: complete OAuth on a machine with a browser, then copy that agent's `auth-profiles.json` (or the matching `$OPENCLAW_STATE_DIR/...` path) to the gateway host.

### Step 3 — Workspace

Defaults to `~/.openclaw/workspace` (configurable) and seeds the workspace files needed for the agent bootstrap ritual. The source links the full workspace layout + backup guide at `/concepts/agent-workspace`.

### Step 4 — Gateway

Configures port, bind, auth mode, and tailscale exposure. The auth recommendation is to keep **Token** even for loopback so local WS clients must authenticate. In token mode, interactive setup offers **Generate/store plaintext token** (default) or **Use SecretRef** (opt-in); Quickstart reuses existing `gateway.auth.token` SecretRefs across `env`, `file`, and `exec` providers for the onboarding probe/dashboard bootstrap, and if that SecretRef is configured but cannot be resolved, onboarding fails early with a clear fix message instead of silently degrading runtime auth. In password mode, interactive setup also supports plaintext or SecretRef storage. The non-interactive token SecretRef path is `--gateway-token-ref-env <ENV_VAR>`, which requires a non-empty env var in the onboarding process environment and cannot be combined with `--gateway-token`. Disable auth only if you fully trust every local process; non-loopback binds still require auth.

### Step 5 — Channels

Optional messaging-channel setup: **WhatsApp** (optional QR login), **Telegram** (bot token), **Discord** (bot token), **Google Chat** (service account JSON + webhook audience), **Mattermost** (plugin: bot token + base URL), **Signal** (optional `signal-cli` install + account config), and **iMessage** (`imsg` CLI path + Messages DB access; use an SSH wrapper when the Gateway runs off-Mac). DM security defaults to pairing: the first DM sends a code, approved via `openclaw pairing approve <channel> <code>` or via allowlists.

### Step 6 — Web search

Pick a supported provider — Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax Search, Ollama Web Search, Perplexity, SearXNG, or Tavily — or skip. API-backed providers can use env vars or existing config for quick setup; key-free providers use their provider-specific prerequisites instead. Skip with `--skip-search`; configure later with `openclaw configure --section web`.

### Step 7 — Daemon install

On macOS the wizard installs a **LaunchAgent** (which requires a logged-in user session; for headless, use a custom LaunchDaemon, not shipped). On Linux (and Windows via WSL2) it installs a **systemd user unit**, attempting to enable lingering via `loginctl enable-linger <user>` so the Gateway stays up after logout (this may prompt for sudo to write `/var/lib/systemd/linger`; it tries without sudo first). Runtime selection: **Node** (recommended; required for WhatsApp/Telegram); **Bun is not recommended**. Token-auth interactions: if `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist resolved plaintext token values into supervisor service environment metadata; if the configured token SecretRef is unresolved, daemon install is blocked with actionable guidance; and if both `gateway.auth.token` and `gateway.auth.password` are configured while `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly.

### Step 8 — Health check

Starts the Gateway (if needed) and runs `openclaw health`. Tip: `openclaw status --deep` adds the live gateway health probe to status output, including channel probes when supported (requires a reachable gateway).

### Step 9 — Skills (recommended)

Reads the available skills and checks requirements, lets you choose a node manager — **npm / pnpm** (bun not recommended) — and installs optional dependencies (some use Homebrew on macOS).

### Step 10 — Finish

Prints a summary + next steps, including the **How do you want to hatch your agent?** prompt for Terminal, Browser, or later. If no GUI is detected, onboarding prints SSH port-forward instructions for the Control UI instead of opening a browser; if the Control UI assets are missing, onboarding attempts to build them, with fallback `pnpm ui:build` (auto-installs UI deps).

## Non-Interactive Mode

Use `--non-interactive` to automate or script onboarding. A representative full invocation:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Add `--json` for a machine-readable summary. To supply the Gateway token as a SecretRef in non-interactive mode, export the env var and pass `--gateway-token-ref-env`:

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
```

`--gateway-token` and `--gateway-token-ref-env` are mutually exclusive. Note that `--json` does **not** imply non-interactive mode — use `--non-interactive` (and `--workspace`) for scripts. Provider-specific command examples live in CLI Automation (`/start/wizard-cli-automation#provider-specific-examples`); this reference page is for flag semantics and step ordering.

### Add Agent (Non-Interactive)

To add a second agent without prompts, use `openclaw agents add`:

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.5 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

**Source**: OpenClaw documentation — `reference/wizard` (mirror `inbox/openclaw_docs/reference/wizard.md`), sections Flow details (local mode), Non-interactive mode, Add agent (non-interactive)
**Last Updated**: 2026-06-22
**Status**: Active
