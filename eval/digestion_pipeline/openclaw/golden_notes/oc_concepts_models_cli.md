---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - models_cli
keywords:
  - openclaw models cli
  - switch model in chat /model
  - openclaw models list
  - openclaw models status
  - openclaw models scan openrouter
  - models aliases fallbacks
  - model ref parsing
  - free model probe tools images
topics:
  - OpenClaw
  - Models CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/models
access_control_group: ["general"]
---

# OpenClaw — Models CLI and `/model` Switching

## Overview

This note is the **procedure** for the OpenClaw Models CLI/UX surface, mirroring the `concepts/models` source page sections "Switching models in chat (`/model`)", "CLI commands", and "Scanning (OpenRouter free models)". It covers the in-chat `/model` picker and live-switch behavior, the `openclaw models` command family (`list`, `status`, `set`, `aliases`, `fallbacks`, `image-fallbacks`) with their flags and output, and `openclaw models scan` for discovering OpenRouter free models with optional tool/image capability probes. The selection-policy concepts these commands operate on (allowlist, `agents.defaults.models`, the `models.json` registry, selection-source semantics) live in the sibling selection note; this note is the hands-on command reference.

## Switching models in chat (`/model`)

You can switch models for the current session without restarting. The chat slash commands are:

```
/model
/model list
/model 3
/model openai/gpt-5.4
/model default
/model status
```

**Picker behavior.** `/model` (and `/model list`) is a compact, numbered picker showing the model family plus available providers; `/model <#>` selects from that picker. On Discord, `/model` and `/models` open an interactive picker with provider and model dropdowns plus a Submit step. On Telegram, `/models` picker selections are session-scoped — they do not change the agent's persistent default in `openclaw.json`. `/models add` is deprecated and now returns a deprecation message instead of registering models from chat.

**Persistence and live switching.** `/model` persists the new session selection immediately. If the agent is idle, the next run uses the new model right away. If a run is already active, OpenClaw marks a live switch as pending and only restarts into the new model at a clean retry point; if tool activity or reply output has already started, the pending switch can stay queued until a later retry opportunity or the next user turn. `/model default` clears the session selection and returns the session to the configured default model. A user-selected `/model` ref is **strict** for that session: if the selected provider/model is unreachable, the reply fails visibly instead of silently answering from `agents.defaults.model.fallbacks` — this differs from configured defaults and cron job primaries, which can still use fallback chains. `/model status` is the detailed view (auth candidates and, when configured, the provider endpoint `baseUrl` + `api` mode).

**Ref parsing.** Model refs are parsed by splitting on the **first** `/`, so type `provider/model` when using `/model <ref>`. If the model ID itself contains `/` (OpenRouter-style), you must include the provider prefix (example: `/model openrouter/moonshotai/kimi-k2`). If you omit the provider, OpenClaw resolves the input in this order: (1) alias match; (2) unique configured-provider match for that exact unprefixed model id; (3) a deprecated fallback to the configured default provider — and if that provider no longer exposes the configured default model, OpenClaw instead falls back to the first configured provider/model to avoid surfacing a stale removed-provider default. Full command behavior/config lives in the Slash commands page (see References).

## CLI commands

The `openclaw models` command family manages the resolved model, aliases, and fallback chains from the shell:

```bash
openclaw models list
openclaw models status
openclaw models set <provider/model>
openclaw models set-image <provider/model>

openclaw models aliases list
openclaw models aliases add <alias> <provider/model>
openclaw models aliases remove <alias>

openclaw models fallbacks list
openclaw models fallbacks add <provider/model>
openclaw models fallbacks remove <provider/model>
openclaw models fallbacks clear

openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

`openclaw models` with no subcommand is a shortcut for `models status`.

### `models list`

`models list` shows configured/auth-available models by default. Useful flags:

- `--all` (boolean) — full catalog. Includes bundled provider-owned static catalog rows before auth is configured, so discovery-only views can show models that are unavailable until you add matching provider credentials.
- `--local` (boolean) — local providers only.
- `--provider <id>` (string) — filter by provider id, for example `moonshot`. Display labels from interactive pickers are not accepted.
- `--plain` (boolean) — one model per line.
- `--json` (boolean) — machine-readable output.

### `models status`

`models status` shows the resolved primary model, fallbacks, image model, and an auth overview of configured providers. It also surfaces OAuth expiry status for profiles found in the auth store (warns within 24h by default). `--plain` prints only the resolved primary model.

**Auth and probe behavior.** OAuth status is always shown (and included in `--json` output); if a configured provider has no credentials, `models status` prints a **Missing auth** section. JSON includes `auth.oauth` (warn window + profiles) and `auth.providers` (effective auth per provider, including env-backed credentials) — `auth.oauth` is auth-store profile health only, so env-only providers do not appear there. Use `--check` for automation (exit `1` when missing/expired, `2` when expiring). Use `--probe` for live auth checks; probe rows can come from auth profiles, env credentials, or `models.json`. If explicit `auth.order.<provider>` omits a stored profile, probe reports `excluded_by_auth_order` instead of trying it; if auth exists but no probeable model can be resolved for that provider, probe reports `status: no_model`. Auth choice is provider/account dependent — for always-on gateway hosts, API keys are usually the most predictable, while Claude CLI reuse and existing Anthropic OAuth/token profiles are also supported.

A typical Claude CLI status flow:

```bash
claude auth login
openclaw models status
```

## Scanning (OpenRouter free models)

`openclaw models scan` inspects OpenRouter's **free model catalog** and can optionally probe models for tool and image support. Flags:

- `--no-probe` (boolean) — skip live probes (metadata only).
- `--min-params <b>` (number) — minimum parameter size (billions).
- `--max-age-days <days>` (number) — skip older models.
- `--provider <name>` (string) — provider prefix filter.
- `--max-candidates <n>` (number) — fallback list size.
- `--set-default` (boolean) — set `agents.defaults.model.primary` to the first selection.
- `--set-image` (boolean) — set `agents.defaults.imageModel.primary` to the first image selection.

The OpenRouter `/models` catalog is public, so metadata-only scans can list free candidates without a key, but probing and inference still require an OpenRouter API key (from auth profiles or `OPENROUTER_API_KEY`). If no key is available, `openclaw models scan` falls back to metadata-only output and leaves config unchanged; use `--no-probe` to request metadata-only mode explicitly.

**Ranking.** Scan results are ranked by: (1) image support; (2) tool latency; (3) context size; (4) parameter count.

**Inputs.** The OpenRouter `/models` list filtered to `:free`; live probes require an OpenRouter API key from auth profiles or `OPENROUTER_API_KEY`; optional filters `--max-age-days`, `--min-params`, `--provider`, `--max-candidates`; and request/probe controls `--timeout` and `--concurrency`.

When live probes run in a TTY you can select fallbacks interactively; in non-interactive mode, pass `--yes` to accept defaults. Metadata-only results are informational — `--set-default` and `--set-image` require live probes so OpenClaw does not configure an unusable keyless OpenRouter model.

**Source**: OpenClaw documentation — `concepts/models` (mirror `inbox/openclaw_docs/concepts/models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
