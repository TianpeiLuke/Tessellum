---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - github_copilot
keywords:
  - github copilot openclaw provider
  - models auth login-github-copilot
  - copilot device flow login
  - copilot sdk harness agentRuntime
  - copilot proxy plugin
  - copilot_github_token gh_token github_token order
  - non-interactive onboarding github-copilot-token
  - anthropic messages transport copilot
topics:
  - OpenClaw
  - GitHub Copilot Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/github-copilot
access_control_group: ["general"]
---

# OpenClaw — Use GitHub Copilot as a Model Provider / Agent Runtime

## Overview

This note is the **model-provider / agent-runtime** half of the OpenClaw `providers/github-copilot` source page: it covers the three ways to wire GitHub Copilot in as a model provider, the optional auth-login flags, and the non-interactive (headless) onboarding path including env-var resolution, transport selection, and on-demand catalog refresh. GitHub Copilot is GitHub's AI coding assistant; it provides access to Copilot models for your GitHub account and plan, and OpenClaw can use Copilot as a model provider or agent runtime in three different ways. The companion note `oc_providers_github_copilot_memory_search` covers using a logged-in Copilot subscription as the embedding provider for memory search (the source page's "Memory search embeddings" section) — that surface is intentionally NOT duplicated here.

## Three ways to use Copilot in OpenClaw

OpenClaw exposes three distinct integration paths for Copilot. Each is a different config surface; pick by whether you want OpenClaw's built-in agent loop, GitHub's Copilot CLI/SDK to own the loop, or a local VS Code proxy bridge.

### Built-in provider (`github-copilot`)

This is the **default** and simplest path because it does not require VS Code. It uses the native device-login flow to obtain a GitHub token, then exchanges it for Copilot API tokens when OpenClaw runs. Step 1 — run the login command; you will be prompted to visit a URL and enter a one-time code, and you must keep the terminal open until it completes:

```bash
openclaw models auth login-github-copilot
```

Step 2 — set a default model, either via the CLI (`openclaw models set github-copilot/claude-opus-4.7`) or in config:

```json5
{
  agents: {
    defaults: { model: { primary: "github-copilot/claude-opus-4.7" } },
  },
}
```

### Copilot SDK harness plugin (`copilot`)

Install the external `@openclaw/copilot` plugin when you want GitHub's Copilot CLI and SDK to own the low-level agent loop for selected `github-copilot/*` models. Choose this when you want native Copilot CLI sessions, SDK-managed thread state, and Copilot-owned compaction for those agent turns; see the `/plugins/copilot` page for the full runtime contract. Install the plugin from ClawHub, then opt a model or provider into the `copilot` runtime via `agentRuntime`:

```bash
openclaw plugins install clawhub:@openclaw/copilot
```

```json5
{
  agents: {
    defaults: {
      model: "github-copilot/gpt-5.5",
      models: {
        "github-copilot/gpt-5.5": {
          agentRuntime: { id: "copilot" },
        },
      },
    },
  },
}
```

### Copilot Proxy plugin (`copilot-proxy`)

Use the **Copilot Proxy** VS Code extension as a local bridge: OpenClaw talks to the proxy's `/v1` endpoint and uses the model list you configure there. Choose this when you already run Copilot Proxy in VS Code or need to route through it. You must enable the plugin and keep the VS Code extension running. (No config snippet is given on the source page for this option.)

## Optional flags

The device-login command accepts two optional flags:

| Flag | Description |
| --- | --- |
| `--yes` | Skip the confirmation prompt |
| `--set-default` | Also apply the provider's recommended default model |

To skip the confirmation prompt: `openclaw models auth login-github-copilot --yes`. To log in and set the default model in one step: `openclaw models auth login --provider github-copilot --method device --set-default`.

## Non-interactive onboarding

If you already have a GitHub OAuth access token for Copilot, import it during headless setup with `openclaw onboard --non-interactive`:

```bash
openclaw onboard --non-interactive --accept-risk \
  --auth-choice github-copilot \
  --github-copilot-token "$COPILOT_GITHUB_TOKEN" \
  --skip-channels --skip-health
```

You can also omit `--auth-choice`; passing `--github-copilot-token` infers the GitHub Copilot provider auth choice. If the flag is omitted, onboarding falls back to `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, then `GITHUB_TOKEN`. Use `--secret-input-mode ref` with `COPILOT_GITHUB_TOKEN` set to store an env-backed `tokenRef` instead of plaintext in `auth-profiles.json`.

### Interactive TTY requirement

The device-login flow requires an interactive TTY. Run it directly in a terminal, not in a non-interactive script or CI pipeline; use non-interactive onboarding when you need headless setup.

### Environment variable resolution order

OpenClaw resolves Copilot auth from environment variables in the following priority order; when multiple variables are set, OpenClaw uses the highest-priority one:

| Priority | Variable | Notes |
| --- | --- | --- |
| 1 | `COPILOT_GITHUB_TOKEN` | Highest priority, Copilot-specific |
| 2 | `GH_TOKEN` | GitHub CLI token (fallback) |
| 3 | `GITHUB_TOKEN` | Standard GitHub token (lowest) |

The device-login flow (`openclaw models auth login-github-copilot`) stores its token in the auth profile store and takes precedence over all environment variables. **Token storage:** the login stores a GitHub token in the auth profile store and exchanges it for a Copilot API token when OpenClaw runs — you do not need to manage the token manually.

### Model availability, transport, and request compatibility

Copilot model availability depends on your GitHub plan; if a model is rejected, try another ID (for example `github-copilot/gpt-5.5`). For transport selection, Claude model IDs use the Anthropic Messages transport automatically, while GPT, o-series, and Gemini models keep the OpenAI Responses transport — OpenClaw selects the correct transport based on the model ref. For request compatibility, OpenClaw sends Copilot IDE-style request headers on Copilot transports, including built-in compaction, tool-result, and image follow-up turns, and it does not enable provider-level Responses continuation for Copilot unless that behavior has been verified against Copilot's API.

### Live catalog refresh from the Copilot API

Once the device-login (or env-var) auth path has resolved a GitHub token, OpenClaw refreshes the model catalog on demand from `${baseUrl}/models` (the same endpoint VS Code Copilot uses) so the runtime tracks per-account entitlement and accurate context windows without manifest churn. Newly published Copilot models become visible without an OpenClaw upgrade, and context windows reflect the real per-model limits (e.g. 400k for the gpt-5.x series, 1M for the internal `claude-opus-*-1m` variants). The bundled static catalog stays as the visible fallback when discovery is disabled, the user has no GitHub auth profile, the token-exchange fails, or the `/models` HTTPS call errors. To opt out and rely entirely on the static manifest catalog (offline / air-gapped scenarios):

```json5
{
  plugins: {
    entries: {
      "github-copilot": {
        config: { discovery: { enabled: false } },
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `providers/github-copilot` (mirror `inbox/openclaw_docs/providers/github-copilot.md`), model-provider/runtime half
**Last Updated**: 2026-06-22
**Status**: Active
