---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - fireworks
keywords:
  - openclaw fireworks provider
  - fireworks api key onboarding
  - kimi k2.5 turbo fire pass router
  - fireworks forced off thinking
  - custom fireworks model id resolution
  - thinking-policy.ts kimi
  - route kimi through moonshot reasoning
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/fireworks
access_control_group: ["general"]
---

# OpenClaw — Configure the Fireworks Provider

## Overview

This note is the procedure for wiring the bundled **Fireworks** provider into OpenClaw, mirroring the `providers/fireworks` source page. Fireworks exposes open-weight and routed models through an OpenAI-compatible API; the bundled provider plugin ships `enabledByDefault: true` with two pre-cataloged Kimi models and accepts any Fireworks model or router id at runtime. It covers authenticating with `FIREWORKS_API_KEY` (interactive and non-interactive onboarding), verifying the catalog, the two pre-cataloged Kimi entries and their contexts, custom `fireworks/<id>` model refs with dynamic resolution, and the central runtime caveat — Kimi thinking is **forced off** on Fireworks (route the same model through Moonshot for reasoning).

The provider's fixed properties from the source page header table are: provider id `fireworks` (alias `fireworks-ai`), bundled plugin with `enabledByDefault: true`, auth env var `FIREWORKS_API_KEY`, onboarding flag `--auth-choice fireworks-api-key`, direct CLI flag `--fireworks-api-key <key>`, API `openai-completions` (OpenAI-compatible), base URL `https://api.fireworks.ai/inference/v1`, default model `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo`, and default alias `Kimi K2.5 Turbo`.

## Getting started

Setup is two steps: set the API key, then verify the model is available.

**Step 1 — Set the Fireworks API key.** Onboarding stores the key against the `fireworks` provider in your auth profiles and sets the **Fire Pass** Kimi K2.5 Turbo router as the default model. Three equivalent ways to supply the key:

```bash
# Onboarding (interactive)
openclaw onboard --auth-choice fireworks-api-key

# Direct flag
openclaw onboard --non-interactive \
  --auth-choice fireworks-api-key \
  --fireworks-api-key "$FIREWORKS_API_KEY"

# Env only
export FIREWORKS_API_KEY=fw-...
```

**Step 2 — Verify the model is available.** Run `openclaw models list --provider fireworks`. The list should include `Kimi K2.6` and `Kimi K2.5 Turbo (Fire Pass)`. If `FIREWORKS_API_KEY` is unresolved, `openclaw models status --json` reports the missing credential under `auth.unusableProfiles`.

```bash
openclaw models list --provider fireworks
```

## Non-interactive setup

For scripted or CI installs, pass everything on the command line:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice fireworks-api-key \
  --fireworks-api-key "$FIREWORKS_API_KEY" \
  --skip-health \
  --accept-risk
```

## Built-in catalog

The bundled plugin pre-catalogs two Kimi models. Both take **text + image** input, and both have **thinking forced off**:

| Model ref | Name | Input | Context | Max output | Thinking |
| --- | --- | --- | --- | --- | --- |
| `fireworks/accounts/fireworks/models/kimi-k2p6` | Kimi K2.6 | text + image | 262,144 | 262,144 | Forced off |
| `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo` | Kimi K2.5 Turbo (Fire Pass) | text + image | 256,000 | 256,000 | Forced off (default) |

OpenClaw pins all Fireworks Kimi models to `thinking: off` because Fireworks rejects Kimi thinking parameters in production. Routing the same model through Moonshot directly preserves Kimi reasoning output (see Thinking modes for switching between providers).

## Custom Fireworks model ids

OpenClaw accepts any Fireworks model or router id at runtime. Use the exact id shown by Fireworks and prefix it with `fireworks/`. Dynamic resolution clones the Fire Pass template (text + image input, OpenAI-compatible API, default cost zero) and disables thinking automatically when the id matches the Kimi pattern. GLM dynamic ids are marked text-only unless you configure a custom model entry with image input.

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "fireworks/accounts/fireworks/models/<your-model-id>",
      },
    },
  },
}
```

### How model id prefixing works

Every Fireworks model ref in OpenClaw starts with `fireworks/` followed by the exact id or router path from the Fireworks platform. For example, a router model is `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo` and a direct model is `fireworks/accounts/fireworks/models/<model-name>`. OpenClaw strips the `fireworks/` prefix when constructing the API request and sends the remaining path to the Fireworks endpoint as the OpenAI-compatible `model` field.

### Why thinking is forced off for Kimi

Fireworks K2.6 returns a 400 if the request carries `reasoning_*` parameters even though Kimi supports thinking through Moonshot's own API. The bundled policy (`extensions/fireworks/thinking-policy.ts`) advertises only the `off` thinking level for Kimi model ids, so manual `/think` switches and provider-policy surfaces stay aligned with the runtime contract. To use Kimi reasoning end-to-end, configure the Moonshot provider and route the same model through it.

### Environment availability for the daemon

If the Gateway runs as a managed service (launchd, systemd, Docker), the Fireworks key must be visible to that process — not just to your interactive shell. A key exported only in an interactive shell will not help a launchd or systemd daemon unless that environment is imported there too. Set the key in `~/.openclaw/.env` or via `env.shellEnv` to make it readable from the gateway process. On macOS, `openclaw gateway install` already wires `~/.openclaw/.env` into the LaunchAgent environment file; re-run install (or `openclaw doctor --fix`) after rotating the key.

**Source**: OpenClaw documentation — `providers/fireworks` (mirror `inbox/openclaw_docs/providers/fireworks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
