---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - configure
keywords:
  - openclaw configure
  - interactive configuration wizard
  - section filter
  - agents.defaults.models allowlist
  - provider preference picker
  - daemon install secretref
  - web search provider setup
  - model allowlist merge
topics:
  - OpenClaw
  - CLI Configure Wizard
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/configure
access_control_group: ["general"]
---

# OpenClaw — `openclaw configure` Interactive Wizard

## Overview

This note documents the `openclaw configure` command, OpenClaw's interactive prompt for targeted changes to an existing setup — credentials, devices, agent defaults, gateway, channels, plugins, skills, and health checks. It mirrors the `cli/configure` source page: the intro and its sibling-command guidance, the Model-section allowlist merge and primary-model preservation semantics, the provider-preference defaults, the web-search provider follow-up prompts, the repeatable `--section` filter and its available sections, the daemon-install behavior notes (including SecretRef token handling), and the worked examples. The non-interactive analog is `openclaw config get|set|unset`; running `openclaw config` with no subcommand opens this same wizard.

## What `configure` Does

`openclaw configure` is an **interactive prompt for targeted changes to an existing setup**: credentials, devices, agent defaults, gateway, channels, plugins, skills, and health checks. It is distinct from the other setup entry points:

- Use `openclaw onboard` for the full guided first-run journey.
- Use `openclaw setup` for the baseline config/workspace only.
- Use `openclaw channels add` when you only need channel account setup.

Per the source page's Tip, `openclaw config` without a subcommand opens the same wizard, while `openclaw config get|set|unset` performs non-interactive edits.

## Model Section — Allowlist Merge and Primary Preservation

The **Model** section includes a multi-select for the `agents.defaults.models` allowlist (what shows up in `/model` and the model picker). Provider-scoped setup choices **merge** their selected models into the existing allowlist instead of replacing unrelated providers already in the config.

Re-running provider auth from configure **preserves an existing `agents.defaults.model.primary`**, even when the provider's auth step returns a config patch with its own recommended default model. That means adding or reauthing xAI, OpenRouter, or another provider should make the new model available without taking over from your current primary model. To intentionally change the default model, the source page directs the operator to `openclaw models auth login --provider <id> --set-default` or `openclaw models set <model>`.

## Provider Preference When Starting From Auth

When configure starts from a provider auth choice, the default-model and allowlist pickers **prefer that provider automatically**. For paired providers such as Volcengine and BytePlus, the same preference also matches their coding-plan variants (`volcengine-plan/*`, `byteplus-plan/*`). If the preferred-provider filter would produce an empty list, configure **falls back to the unfiltered catalog** instead of showing a blank picker.

## Web Section — Provider Follow-Up Prompts

For web search, `openclaw configure --section web` lets you choose a provider and configure its credentials. Some providers also show provider-specific follow-up prompts:

- **Grok** can offer optional `x_search` setup with the same xAI OAuth profile or API key and let you pick an `x_search` model.
- **Kimi** can ask for the Moonshot API region (`api.moonshot.ai` vs `api.moonshot.cn`) and the default Kimi web-search model.

The source page's Related links point to the gateway configuration reference (`/gateway/configuration`) and the Config CLI (`/cli/config`).

## Options

- `--section <section>`: repeatable section filter.

Available sections:

- `workspace`
- `model`
- `web`
- `gateway`
- `daemon`
- `channels`
- `plugins`
- `skills`
- `health`

The source page documents these behavioral notes for the sections:

- The full wizard and gateway-related sections ask where the Gateway runs and update `gateway.mode`. Section filters that do not include `gateway`, `daemon`, or `health` go directly to the requested setup.
- After local config writes, configure installs selected downloadable plugins when the chosen setup path requires them. Remote gateway config does not install local plugin packages.
- Channel-oriented services (Slack/Discord/Matrix/Microsoft Teams) prompt for channel/room allowlists during setup. You can enter names or IDs; the wizard resolves names to IDs when possible.
- If you run the daemon install step, token auth requires a token, and `gateway.auth.token` is SecretRef-managed, configure validates the SecretRef but does **not** persist resolved plaintext token values into supervisor service environment metadata.
- If token auth requires a token and the configured token SecretRef is unresolved, configure **blocks** daemon install with actionable remediation guidance.
- If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, configure **blocks** daemon install until mode is set explicitly.

## Examples

```bash
openclaw configure
openclaw configure --section web
openclaw configure --section model --section channels
openclaw configure --section gateway --section daemon
```

**Source**: OpenClaw documentation — `cli/configure` (mirror `inbox/openclaw_docs/cli/configure.md`)
**Last Updated**: 2026-06-22
**Status**: Active
