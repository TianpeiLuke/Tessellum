---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - onboarding
keywords:
  - openclaw onboard
  - guided onboarding flow
  - non-interactive onboarding
  - secret-ref mode
  - gateway token options
  - flow quickstart manual import
  - zai endpoint choices
  - install-daemon health gating
topics:
  - OpenClaw
  - CLI Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/onboard
access_control_group: ["general"]
---

# OpenClaw — `openclaw onboard` (Guided Onboarding)

## Overview

This note documents the `openclaw onboard` CLI command — OpenClaw's full guided onboarding for local or remote Gateway setup, walking through model auth, workspace, gateway, channels, skills, and health in one flow. It mirrors the `cli/onboard` source page: the interactive classic flow vs the `--modern` Crestodian preview, the three flow types (`quickstart` / `manual` / `import`), locale resolution, and the non-interactive flag surface (custom provider, secret-ref mode, gateway token options, health gating, and the Z.AI / Ollama / LM Studio / Mistral provider examples), plus flow notes and common follow-up commands. This is a single `procedure` building_block.

## Synopsis and Flow Selection

`openclaw onboard` runs the full guided onboarding for local or remote Gateway setup. Use it when you want OpenClaw to walk through model auth, workspace, gateway, channels, skills, and health in one flow. The headline forms:

```bash
openclaw onboard
openclaw onboard --modern
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --flow import
openclaw onboard --import-from hermes --import-source ~/.hermes
openclaw onboard --skip-bootstrap
openclaw onboard --mode remote --remote-url wss://gateway-host:18789
```

`--modern` starts the **Crestodian conversational onboarding preview**; without `--modern`, `openclaw onboard` keeps the classic onboarding flow. On a fresh install where the active config file is missing or has no authored settings (empty or metadata-only), bare `openclaw` also starts the classic onboarding flow; once a config file has authored settings, bare `openclaw` opens Crestodian instead. The remote form (`--mode remote --remote-url wss://...`) writes only connection info for the remote Gateway. Plaintext `ws://` is accepted for loopback, private IP literals, `.local`, and Tailnet `*.ts.net` gateway URLs; for other trusted private-DNS names, set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` in the onboarding process environment.

`--flow import` uses plugin-owned migration providers such as Hermes. It only runs against a fresh OpenClaw setup; if existing config, credentials, sessions, or workspace memory/identity files are present, reset or choose a fresh setup before importing.

## Flow Types

The flow types (set via `--flow`) are:

- `quickstart`: minimal prompts, auto-generates a gateway token.
- `manual`: full prompts for port, bind, and auth (alias of `advanced`).
- `import`: runs a detected migration provider, previews the plan, then applies after confirmation.

**Provider prefiltering**: when an auth choice implies a preferred provider, onboarding prefilters the default-model and allowlist pickers to that provider. For Volcengine and BytePlus, this also matches the coding-plan variants (`volcengine-plan/*`, `byteplus-plan/*`). If the preferred-provider filter yields no loaded models yet, onboarding falls back to the unfiltered catalog instead of leaving the picker empty.

**Web-search follow-ups**: some web-search providers trigger provider-specific follow-up prompts. **Grok** can offer optional `x_search` setup with the same xAI OAuth profile or API key and an `x_search` model choice. **Kimi** can ask for the Moonshot API region (`api.moonshot.ai` vs `api.moonshot.cn`) and the default Kimi web-search model.

**Other behaviors**: local onboarding DM scope behavior is documented in the CLI setup reference (`/start/wizard-cli-reference#outputs-and-internals`). The fastest first chat is `openclaw dashboard` (Control UI, no channel setup). The custom-provider path connects any OpenAI- or Anthropic-compatible endpoint, including hosted providers not listed (use Unknown to auto-detect). If Hermes state is detected, onboarding offers a migration flow; use `openclaw migrate` for dry-run plans, overwrite mode, reports, and exact mappings.

## Locale

Interactive onboarding uses the CLI wizard locale for fixed setup copy. The resolve order is: `OPENCLAW_LOCALE` → `LC_ALL` → `LC_MESSAGES` → `LANG` → English fallback. Supported wizard locales are `en`, `zh-CN`, and `zh-TW`. Locale values may use underscore or POSIX suffix forms such as `zh_CN.UTF-8`. Product names, command names, config keys, URLs, provider IDs, model IDs, and plugin/channel labels remain literal. Example:

```bash
OPENCLAW_LOCALE=zh-CN openclaw onboard
```

## Non-Interactive Provider Auth

In non-interactive mode (`--non-interactive`), a custom provider is configured with `--auth-choice custom-api-key` plus base URL, model id, and key flags:

```bash
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --secret-input-mode plaintext \
  --custom-compatibility openai \
  --custom-image-input
```

`--custom-api-key` is optional in non-interactive mode; if omitted, onboarding checks `CUSTOM_API_KEY`. OpenClaw marks common vision model IDs as image-capable automatically — pass `--custom-image-input` for unknown custom vision IDs, or `--custom-text-input` to force text-only metadata. Use `--custom-compatibility openai-responses` for OpenAI-compatible endpoints that support `/v1/responses` but not `/v1/chat/completions`.

Provider-specific non-interactive examples follow the same shape with a provider-specific `--auth-choice` and key flag. **LM Studio** uses `--auth-choice lmstudio` with a `--lmstudio-api-key` flag. **Ollama** uses `--auth-choice ollama`; `--custom-base-url` defaults to `http://127.0.0.1:11434`, `--custom-model-id` is optional (Ollama's suggested defaults are used if omitted), and cloud model IDs such as `kimi-k2.5:cloud` also work. **Mistral** uses `--auth-choice mistral-api-key` with `--mistral-api-key "$MISTRAL_API_KEY"`.

### Non-interactive Z.AI endpoint choices

`--auth-choice zai-api-key` auto-detects the best Z.AI endpoint and model for your key: Coding Plan endpoints prefer `zai/glm-5.2`; general API endpoints use `zai/glm-5.1`. To force a Coding Plan endpoint, pick `zai-coding-global` or `zai-coding-cn`. The full endpoint choices are promptless:

```bash
# Promptless endpoint selection
openclaw onboard --non-interactive \
  --auth-choice zai-coding-global \
  --zai-api-key "$ZAI_API_KEY"

# Other Z.AI endpoint choices:
# --auth-choice zai-coding-cn
# --auth-choice zai-global
# --auth-choice zai-cn
```

## Secret-Ref Mode

To store provider keys as refs instead of plaintext, pass `--secret-input-mode ref` (e.g. `--auth-choice openai-api-key --secret-input-mode ref --accept-risk`). With ref mode, onboarding writes env-backed refs instead of plaintext key values: for auth-profile backed providers this writes `keyRef` entries; for custom providers this writes `models.providers.<id>.apiKey` as an env ref (for example `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`).

The non-interactive `ref` mode contract: set the provider env var in the onboarding process environment (for example `OPENAI_API_KEY`); do not pass inline key flags (for example `--openai-api-key`) unless that env var is also set; if an inline key flag is passed without the required env var, onboarding fails fast with guidance. Interactive ref-mode behavior: choose **Use secret reference** when prompted, then choose either an environment variable or a configured secret provider (`file` or `exec`); onboarding performs a fast preflight validation before saving the ref, and if validation fails it shows the error and lets you retry.

## Gateway Token Options and Health Gating

Gateway token options in non-interactive mode: `--gateway-auth token --gateway-token <token>` stores a plaintext token; `--gateway-auth token --gateway-token-ref-env <name>` stores `gateway.auth.token` as an env SecretRef. `--gateway-token` and `--gateway-token-ref-env` are mutually exclusive, and `--gateway-token-ref-env` requires a non-empty env var in the onboarding process environment. With `--install-daemon`, SecretRef-managed gateway tokens are validated but not persisted as resolved plaintext in supervisor service environment metadata; if token mode requires a token and the configured token SecretRef is unresolved, onboarding fails closed with remediation guidance; and if both `gateway.auth.token` and `gateway.auth.password` are configured while `gateway.auth.mode` is unset, onboarding blocks install until mode is set explicitly. Local onboarding writes `gateway.mode="local"` into the config — a later config file missing `gateway.mode` is config damage or an incomplete manual edit, not a valid local-mode shortcut; local onboarding installs selected downloadable plugins when the chosen setup path requires them, while remote onboarding only writes connection info and does not install local plugin packages. `--allow-unconfigured` is a separate gateway runtime escape hatch and does not mean onboarding may omit `gateway.mode`. Example:

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk
```

Non-interactive local gateway health: unless you pass `--skip-health`, onboarding waits for a reachable local gateway before it exits successfully. `--install-daemon` starts the managed gateway install path first; without it, you must already have a local gateway running (for example `openclaw gateway run`). If you only want config/workspace/bootstrap writes in automation, use `--skip-health`. If you manage workspace files yourself, pass `--skip-bootstrap` to set `agents.defaults.skipBootstrap: true` and skip creating `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, and `BOOTSTRAP.md`. On native Windows, `--install-daemon` tries Scheduled Tasks first and falls back to a per-user Startup-folder login item if task creation is denied. Note that `--json` does not imply non-interactive mode — use `--non-interactive` for scripts.

## Common Follow-Up Commands

After onboarding, the common follow-up commands are:

```bash
openclaw channels add
openclaw configure
openclaw agents add <name>
```

Use `openclaw setup` instead when you only need the baseline config/workspace. Use `openclaw configure` later for targeted changes and `openclaw channels add` for channel-only setup.

**Source**: OpenClaw documentation — `cli/onboard` (mirror `inbox/openclaw_docs/cli/onboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
