---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - tencent
keywords:
  - openclaw tencent provider
  - tencent cloud tokenhub
  - tencent-tokenhub provider id
  - TOKENHUB_API_KEY
  - hy3-preview model
  - tokenhub-api-key auth choice
  - tokenhub-intl endpoint override
  - hy3 preview moe reasoning
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/tencent
access_control_group: ["general"]
---

# OpenClaw — Configuring the Tencent Cloud TokenHub Provider

## Overview

This note is the step-by-step procedure for connecting OpenClaw to **Tencent Cloud TokenHub** so it can run Tencent's **Hy3 preview** model, mirroring the `providers/tencent` source page. Tencent Cloud ships as a **bundled provider plugin** (`enabledByDefault: true`) exposing the provider id `tencent-tokenhub` over an OpenAI-compatible (`openai-completions`) API. The procedure covers: creating and supplying the `TOKENHUB_API_KEY`, interactive and non-interactive onboarding via `--auth-choice tokenhub-api-key`, verifying the bundled `hy3-preview` catalog entry, the tiered cost metadata that ships with the catalog, and advanced configuration for the China-vs-international endpoint override and daemon environment-variable availability.

## Provider properties

The page's property table fixes the identifiers you configure against (reproduced verbatim):

| Property         | Value                                                 |
| ---------------- | ----------------------------------------------------- |
| Provider id      | `tencent-tokenhub`                                    |
| Plugin           | bundled, `enabledByDefault: true`                     |
| Auth env var     | `TOKENHUB_API_KEY`                                    |
| Onboarding flag  | `--auth-choice tokenhub-api-key`                      |
| Direct CLI flag  | `--tokenhub-api-key <key>`                            |
| API              | OpenAI-compatible (`openai-completions`)              |
| Default base URL | `https://tokenhub.tencentmaas.com/v1`                 |
| Global base URL  | `https://tokenhub-intl.tencentmaas.com/v1` (override) |
| Default model    | `tencent-tokenhub/hy3-preview`                        |

Because the plugin is bundled and enabled by default, no separate plugin install is required — supplying the key is enough to make the provider usable.

## Quick start

Three steps onboard the provider.

1. **Create a TokenHub API key** — create an API key in Tencent Cloud TokenHub. If you choose a limited access scope for the key, include **Hy3 preview** in the allowed models.
2. **Run onboarding** — choose one of the three forms below (interactive onboarding, the direct non-interactive flag, or env-only).
3. **Verify the model** — list the provider's catalog to confirm the key resolved.

The onboarding step offers three equivalent ways to supply the credential:

```bash Onboarding
openclaw onboard --auth-choice tokenhub-api-key
```

```bash Direct flag
openclaw onboard --non-interactive \
  --auth-choice tokenhub-api-key \
  --tokenhub-api-key "$TOKENHUB_API_KEY"
```

```bash Env only
export TOKENHUB_API_KEY=...
```

Verify that the key resolved and the model is visible:

```bash
openclaw models list --provider tencent-tokenhub
```

## Non-interactive setup

For scripted/headless onboarding, run the full non-interactive form, which sets local mode, supplies the key, and skips the health check and risk prompt:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice tokenhub-api-key \
  --tokenhub-api-key "$TOKENHUB_API_KEY" \
  --skip-health \
  --accept-risk
```

## Built-in catalog

The bundled catalog ships one model entry (reproduced verbatim):

| Model ref                      | Name                   | Input | Context | Max output | Notes                      |
| ------------------------------ | ---------------------- | ----- | ------- | ---------- | -------------------------- |
| `tencent-tokenhub/hy3-preview` | Hy3 preview (TokenHub) | text  | 256,000 | 64,000     | Default; reasoning-enabled |

Hy3 preview is Tencent Hunyuan's large MoE language model for reasoning, long-context instruction following, code, and agent workflows. Tencent's OpenAI-compatible examples use `hy3-preview` as the model id and support standard chat-completions tool calling plus `reasoning_effort`.

**Hy3 vs HY-3D disambiguation tip (from source):** the model id is `hy3-preview`. Do not confuse it with Tencent's `HY-3D-*` models, which are 3D generation APIs and are not the OpenClaw chat model configured by this provider.

## Tiered pricing

The bundled catalog ships tiered cost metadata that scales with input window length, so cost estimates are populated without manual overrides. The three input-token tiers (reproduced verbatim) are:

| Input tokens range | Input rate | Output rate | Cache read |
| ------------------ | ---------- | ----------- | ---------- |
| 0 - 16,000         | 0.176      | 0.587       | 0.059      |
| 16,000 - 32,000    | 0.235      | 0.939       | 0.088      |
| 32,000+            | 0.293      | 1.173       | 0.117      |

Rates are per million tokens in USD as advertised by Tencent. Override pricing under `models.providers.tencent-tokenhub` only when you need a different surface.

## Advanced configuration

**Endpoint override.** OpenClaw defaults to Tencent Cloud's `https://tokenhub.tencentmaas.com/v1` endpoint. Tencent also documents an international TokenHub endpoint; switch to it with a single config-set command. Only override the endpoint when your TokenHub account or region requires it.

```bash
openclaw config set models.providers.tencent-tokenhub.baseUrl "https://tokenhub-intl.tencentmaas.com/v1"
```

**Environment availability for the daemon.** If the Gateway runs as a managed service (launchd, systemd, Docker), `TOKENHUB_API_KEY` must be visible to that process. Set it in `~/.openclaw/.env` or via `env.shellEnv` so launchd, systemd, or Docker exec environments can read it. The source warns that keys exported only in an interactive shell are not visible to managed gateway processes — use the env file or config seam for persistent availability.

**Source**: OpenClaw documentation — `providers/tencent` (mirror `inbox/openclaw_docs/providers/tencent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
