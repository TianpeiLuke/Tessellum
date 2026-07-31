---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - cohere
keywords:
  - openclaw cohere provider
  - cohere compatibility api
  - cohere api key
  - auth-choice cohere-api-key
  - command-a-03-2025
  - openclaw onboard cohere
  - environment-only gateway setup
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/cohere
access_control_group: ["general"]
---

# OpenClaw — Configuring the Cohere Provider

## Overview

This note is the procedure for configuring the OpenClaw `cohere` provider, mirroring the `providers/cohere` source page (intro + property table, "Get started", and "Environment-only setup"). Cohere provides OpenAI-compatible inference through its Compatibility API; OpenClaw ships the Cohere provider during its externalization transition and also publishes it as an official external plugin with the Command A model catalog. The page covers two setup paths — an interactive/non-interactive `openclaw onboard` flow keyed off `COHERE_API_KEY`, and an environment-only setup that exports the key to the Gateway process and selects the model in config — plus the provider's identity facts (provider id, base URL, default model).

## Provider Facts

The page documents the `cohere` provider with these properties (verbatim from the source property table):

| Property | Value |
| --- | --- |
| Provider id | `cohere` |
| Plugin | bundled during transition; official external package |
| Auth env var | `COHERE_API_KEY` |
| Onboarding flag | `--auth-choice cohere-api-key` |
| Direct CLI flag | `--cohere-api-key <key>` |
| API | OpenAI-compatible (`openai-completions`) |
| Base URL | `https://api.cohere.ai/compatibility/v1` |
| Default model | `cohere/command-a-03-2025` |

## Get started

The onboarding procedure is four steps:

1. **Install (if needed).** Cohere is included in current OpenClaw packages. If it is unavailable, install the external package and restart the Gateway:

```bash
openclaw plugins install @openclaw/cohere-provider
openclaw gateway restart
```

2. **Create a Cohere API key.**
3. **Run onboarding** with the non-interactive flags, supplying the key via `--cohere-api-key`:

```bash
openclaw onboard --non-interactive \
  --auth-choice cohere-api-key \
  --cohere-api-key "$COHERE_API_KEY"
```

4. **Confirm the catalog is available:**

```bash
openclaw models list --provider cohere
```

Per the source, the default model (`cohere/command-a-03-2025`) is set only when no primary model is already configured — so onboarding will not override an existing primary model.

## Environment-only setup

For an environment-only path, make `COHERE_API_KEY` available to the Gateway process, then select the Cohere model in config:

```json5
{
  agents: {
    defaults: {
      model: { primary: "cohere/command-a-03-2025" },
    },
  },
}
```

The source raises a daemon/Docker caveat: if the Gateway runs as a daemon or in Docker, configure `COHERE_API_KEY` for that service. Exporting it only in an interactive shell does not make it available to an already-running Gateway.

**Source**: OpenClaw documentation — `providers/cohere` (mirror `inbox/openclaw_docs/providers/cohere.md`)
**Last Updated**: 2026-06-22
**Status**: Active
