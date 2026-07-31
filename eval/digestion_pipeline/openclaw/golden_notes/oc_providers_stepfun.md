---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - stepfun
keywords:
  - openclaw stepfun provider
  - stepfun-provider plugin install
  - stepfun vs stepfun-plan
  - stepfun china global endpoint
  - STEPFUN_API_KEY auth
  - step-3.5-flash catalog
  - stepfun onboarding auth-choice
  - openai-completions provider config
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/stepfun
access_control_group: ["general"]
---

# OpenClaw — Connecting the StepFun Provider (Standard and Step Plan)

## Overview

This note is the procedure for connecting OpenClaw to **StepFun** via its official provider plugin, mirroring the `providers/stepfun` source page. The plugin exposes **two separate provider ids** — `stepfun` for the standard endpoint and `stepfun-plan` for the Step Plan endpoint — each with its own endpoint and model-ref prefix (`stepfun/...` vs `stepfun-plan/...`). It covers installing the external plugin, the China (`.com`) vs Global (`.ai`) endpoint matrix, the `STEPFUN_API_KEY` auth env var, the built-in `step-3.5-flash` catalog, region-matched `--auth-choice` onboarding for both surfaces, and the full `models.providers.*` config blocks. Both surfaces use the `openai-completions` API family.

## Provider Summary

Per the source intro, the StepFun provider plugin supports two provider ids: `stepfun` for the standard endpoint and `stepfun-plan` for the Step Plan endpoint. The source carries an explicit **warning**: Standard and Step Plan are **separate providers** with different endpoints and model-ref prefixes (`stepfun/...` vs `stepfun-plan/...`); use a **China key with the `.com` endpoints and a global key with the `.ai` endpoints**. The auth env var for both surfaces is `STEPFUN_API_KEY`, and both providers use `api: "openai-completions"` (per the Advanced configuration blocks). The provider is an official external package, so it must be installed before setup (it is not a bundled, enabled-by-default provider).

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/stepfun-provider
openclaw gateway restart
```

## Region and endpoint overview

StepFun splits each surface across a China (`.com`) and a Global (`.ai`) host. The endpoint matrix from the source is:

| Endpoint  | China (`.com`)                         | Global (`.ai`)                        |
| --------- | -------------------------------------- | ------------------------------------- |
| Standard  | `https://api.stepfun.com/v1`           | `https://api.stepfun.ai/v1`           |
| Step Plan | `https://api.stepfun.com/step_plan/v1` | `https://api.stepfun.ai/step_plan/v1` |

Auth env var: `STEPFUN_API_KEY`. Match the key to the region: a China key pairs with the `.com` endpoints and a global key pairs with the `.ai` endpoints.

## Built-in catalog

The plugin ships a built-in catalog per surface. Standard (`stepfun`):

| Model ref                | Context | Max output | Notes                  |
| ------------------------ | ------- | ---------- | ---------------------- |
| `stepfun/step-3.5-flash` | 262,144 | 65,536     | Default standard model |

Step Plan (`stepfun-plan`):

| Model ref                          | Context | Max output | Notes                      |
| ---------------------------------- | ------- | ---------- | -------------------------- |
| `stepfun-plan/step-3.5-flash`      | 262,144 | 65,536     | Default Step Plan model    |
| `stepfun-plan/step-3.5-flash-2603` | 262,144 | 65,536     | Additional Step Plan model |

Per the source Notes, `step-3.5-flash-2603` is currently exposed only on `stepfun-plan`.

## Getting started

Choose your provider surface and follow the setup steps. The source presents Standard and Step Plan as two tabs; both follow the same four-step flow (choose region → run onboarding → optional non-interactive → verify).

### Standard (`stepfun`)

Best for general-purpose use via the standard StepFun endpoint. First choose your endpoint region by `--auth-choice`:

| Auth choice                      | Endpoint                         | Region        |
| -------------------------------- | -------------------------------- | ------------- |
| `stepfun-standard-api-key-intl`  | `https://api.stepfun.ai/v1`      | International |
| `stepfun-standard-api-key-cn`    | `https://api.stepfun.com/v1`     | China         |

Run onboarding (international shown; use `stepfun-standard-api-key-cn` for the China endpoint), with an optional non-interactive variant that passes the key, then verify:

```bash
openclaw onboard --auth-choice stepfun-standard-api-key-intl
openclaw onboard --auth-choice stepfun-standard-api-key-intl \
  --stepfun-api-key "$STEPFUN_API_KEY"
openclaw models list --provider stepfun
```

Model refs — default model: `stepfun/step-3.5-flash`.

### Step Plan (`stepfun-plan`)

Best for the Step Plan reasoning endpoint. Choose your endpoint region by `--auth-choice`:

| Auth choice                  | Endpoint                                | Region        |
| ---------------------------- | --------------------------------------- | ------------- |
| `stepfun-plan-api-key-intl`  | `https://api.stepfun.ai/step_plan/v1`   | International |
| `stepfun-plan-api-key-cn`    | `https://api.stepfun.com/step_plan/v1`  | China         |

Run onboarding (use `stepfun-plan-api-key-cn` for the China endpoint), with the same optional non-interactive variant, then verify:

```bash
openclaw onboard --auth-choice stepfun-plan-api-key-intl
openclaw onboard --auth-choice stepfun-plan-api-key-intl \
  --stepfun-api-key "$STEPFUN_API_KEY"
openclaw models list --provider stepfun-plan
```

Model refs — default model: `stepfun-plan/step-3.5-flash`; alternate model: `stepfun-plan/step-3.5-flash-2603`.

## Advanced configuration

Both providers use `api: "openai-completions"`, `models.mode: "merge"`, and `apiKey: "${STEPFUN_API_KEY}"`; the `baseUrl` is region-matched (the `.ai` global host is shown). The full config block for the **Standard provider**:

```json5
{
  env: { STEPFUN_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "stepfun/step-3.5-flash" } } },
  models: {
    mode: "merge",
    providers: {
      stepfun: {
        baseUrl: "https://api.stepfun.ai/v1",
        api: "openai-completions",
        apiKey: "${STEPFUN_API_KEY}",
        models: [
          {
            id: "step-3.5-flash",
            name: "Step 3.5 Flash",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

The **Step Plan provider** block (`baseUrl` ends in `/step_plan/v1`, two models registered):

```json5
{
  env: { STEPFUN_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "stepfun-plan/step-3.5-flash" } } },
  models: {
    mode: "merge",
    providers: {
      "stepfun-plan": {
        baseUrl: "https://api.stepfun.ai/step_plan/v1",
        api: "openai-completions",
        apiKey: "${STEPFUN_API_KEY}",
        models: [
          {
            id: "step-3.5-flash",
            name: "Step 3.5 Flash",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 65536,
          },
          {
            id: "step-3.5-flash-2603",
            name: "Step 3.5 Flash 2603",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

The source **Notes** add four operational points: the provider is an official external package, so install it before setup; `step-3.5-flash-2603` is currently exposed only on `stepfun-plan`; a single auth flow writes region-matched profiles for both `stepfun` and `stepfun-plan`, so both surfaces can be discovered together; and use `openclaw models list` and `openclaw models set <provider/model>` to inspect or switch models. For the broader provider overview, the source points to Model providers.

**Source**: OpenClaw documentation — `providers/stepfun` (mirror `inbox/openclaw_docs/providers/stepfun.md`)
**Last Updated**: 2026-06-22
**Status**: Active
