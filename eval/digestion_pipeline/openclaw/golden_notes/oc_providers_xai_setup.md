---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - xai
keywords:
  - openclaw xai provider setup
  - grok oauth device code
  - openclaw models auth login xai
  - xai api key XAI_API_KEY
  - grok-4.3 grok-build-0.1 catalog
  - xai oauth callback 127.0.0.1:56121
  - openclaw models set xai
  - grok legacy slug forward-resolve
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/xai
access_control_group: ["general"]
---

# OpenClaw — xAI / Grok Provider Setup

## Overview

This note is the setup **procedure** for the bundled `xai` provider plugin that brings xAI Grok models into OpenClaw, mirroring the setup half of the `providers/xai` source page (intro + OAuth notes, `## Choose your setup path`, `## OAuth troubleshooting`, and `## Built-in catalog`). It covers the recommended Grok OAuth path (browser callback + device-code) versus the API-key path, the new-install versus existing-install onboarding choices, the `openclaw models auth login` / `openclaw models set` commands, OAuth-callback / device-code troubleshooting, and the built-in Grok chat-model catalog with its forward-resolved legacy slugs. The xAI media/search/code-execution capability surface that the same credential powers is documented in the sibling feature note, not here.

## Provider Overview and Auth Modes

OpenClaw ships a bundled `xai` provider plugin for Grok models. For most users the recommended path is **Grok OAuth** with an eligible **SuperGrok or X Premium** subscription. OpenClaw stays local-first: the Gateway, config, routing, and tools run on your machine, while Grok model requests authenticate through xAI and are sent to xAI's API. OAuth does not require an xAI API key, and it does not require the Grok Build app — xAI may still show Grok Build on the consent screen because OpenClaw uses xAI's shared OAuth client.

The same credential obtained from `openclaw models auth login --provider xai --method oauth`, `openclaw models auth login --provider xai --device-code`, or `openclaw models auth login --provider xai --method api-key` can also power first-class `web_search`, `x_search`, remote `code_execution`, and xAI image/video generation. Speech and transcription currently require `XAI_API_KEY` or provider config. Grok-backed `web_search` prefers xAI OAuth and falls back to `XAI_API_KEY` or plugin web-search config; if you store an xAI key under `plugins.entries.xai.config.webSearch.apiKey`, the bundled xAI model provider reuses that key as a fallback too.

## Choose Your Setup Path

Use the path that matches your OpenClaw install state.

### New OpenClaw install

Run onboarding with daemon install when you are setting up a new local Gateway, then choose the xAI/Grok OAuth option in the model/auth step:

```bash
openclaw onboard --install-daemon
```

On a VPS or over SSH, use device-code during onboarding instead:

```bash
openclaw onboard --install-daemon --auth-choice xai-device-code
```

OAuth does not require an xAI API key, and OpenClaw does not require the Grok Build app. xAI may still label the consent app as Grok Build because OpenClaw uses xAI's shared OAuth client.

### Existing OpenClaw install

If OpenClaw is already configured, sign in to xAI only — do not rerun full onboarding or reinstall the daemon just to connect Grok:

```bash
openclaw models auth login --provider xai --method oauth
```

Use the device-code flow instead when the Gateway runs over SSH, Docker, or a VPS and a localhost browser callback is awkward:

```bash
openclaw models auth login --provider xai --device-code
```

Rerun full onboarding only if you intentionally want to change Gateway, daemon, channel, workspace, or other setup choices.

### API-key path

API-key setup still works for xAI Console keys and for media surfaces that require key-backed provider config:

```bash
openclaw models auth login --provider xai --method api-key
export XAI_API_KEY=xai-...
```

### Pick a model

To make Grok the default model after signing in, either apply it from the CLI with `openclaw models set xai/grok-4.3`, or pin it in `json5` config under `agents.defaults.model.primary: "xai/grok-4.3"` (the form shown on the source page). OpenClaw uses the xAI Responses API as the bundled xAI transport. Operators can set `plugins.entries.xai.config.webSearch.baseUrl` to route Grok `web_search` and, by default, `x_search` through an operator xAI Responses proxy; `code_execution` tuning lives under `plugins.entries.xai.config.codeExecution`. (Those capability surfaces are documented in [oc_providers_xai_features](oc_providers_xai_features.md).)

## OAuth Troubleshooting

- If browser OAuth cannot reach `127.0.0.1:56121`, use `openclaw models auth login --provider xai --device-code`.
- If sign-in succeeds but Grok is not the default model, run `openclaw models set xai/grok-4.3`.
- To inspect saved xAI auth profiles, run:

```bash
openclaw models auth list --provider xai
openclaw models status
```

- xAI decides which accounts can receive OAuth API tokens. If an account is not eligible, try the API-key path or check the subscription on xAI's side.

Use `xai-device-code` when signing in from SSH, Docker, or a VPS: OpenClaw prints an xAI URL and short code, and you finish sign-in in any local browser while the remote process polls xAI for the completed token exchange.

## Built-in Catalog

OpenClaw includes the current xAI chat models out of the box, ordered newest first in model pickers:

| Family         | Model ids                                                                |
| -------------- | ------------------------------------------------------------------------ |
| Grok Build 0.1 | `grok-build-0.1`                                                         |
| Grok 4.3       | `grok-4.3`                                                               |
| Grok 4.20 Beta | `grok-4.20-beta-latest-reasoning`, `grok-4.20-beta-latest-non-reasoning` |

The plugin still forward-resolves older Grok 3, Grok 4, Grok 4 Fast, Grok 4.1 Fast, and Grok Code slugs for existing configs. Official Grok Code Fast aliases normalize to `grok-build-0.1`; OpenClaw no longer shows the other retired upstream slugs in the selectable catalog. Use `grok-4.3` for general chat and `grok-build-0.1` for build/coding-focused workloads unless you explicitly need a Grok 4.20 beta alias.

**Source**: OpenClaw documentation — `providers/xai` (mirror `inbox/openclaw_docs/providers/xai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
