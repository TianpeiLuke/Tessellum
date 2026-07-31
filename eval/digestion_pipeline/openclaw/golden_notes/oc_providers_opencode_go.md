---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - opencode_go
keywords:
  - opencode go catalog
  - opencode-go provider id
  - opencode_api_key shared catalog
  - openclaw onboard auth-choice opencode-go
  - opencode-go runtime model refs
  - glm kimi deepseek mimo minimax qwen go models
  - opencode-go routing convention
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/opencode-go
access_control_group: ["general"]
---

# OpenClaw — Configuring the OpenCode Go Catalog (`opencode-go`)

## Overview

This note is the procedure for using the **OpenCode Go catalog** in OpenClaw — the Go half of the [OpenCode](https://docs.openclaw.ai/providers/opencode) provider, exposed under the distinct runtime provider id `opencode-go`. It mirrors the `providers/opencode-go` source page in full: the intro property table, the bundled Go model lineup (GLM, Kimi, DeepSeek, MiMo, MiniMax, Qwen), the interactive and non-interactive onboarding steps, the JSON5 config example, and the three advanced-configuration notes (routing behavior, runtime-ref convention, shared credentials). The Go catalog reuses the same `OPENCODE_API_KEY` as the Zen catalog but keeps a separate runtime provider id so upstream per-model routing stays correct.

## Catalog and Auth at a Glance

OpenCode Go is the Go catalog within OpenCode. It uses the same `OPENCODE_API_KEY` as the Zen catalog, but keeps the runtime provider id `opencode-go` so upstream per-model routing stays correct. The source page summarizes the provider with this property table:

| Property         | Value                           |
| ---------------- | ------------------------------- |
| Runtime provider | `opencode-go`                   |
| Auth             | `OPENCODE_API_KEY`              |
| Parent setup     | [OpenCode](https://docs.openclaw.ai/providers/opencode) |

## Built-in catalog

OpenClaw sources most Go catalog rows from the bundled OpenClaw model registry and supplements current upstream rows while the registry catches up. Run `openclaw models list --provider opencode-go` for the current model list. The provider includes the following bundled model refs:

| Model ref                       | Name                  |
| ------------------------------- | --------------------- |
| `opencode-go/glm-5`             | GLM-5                 |
| `opencode-go/glm-5.1`           | GLM-5.1               |
| `opencode-go/glm-5.2`           | GLM-5.2               |
| `opencode-go/kimi-k2.5`         | Kimi K2.5             |
| `opencode-go/kimi-k2.6`         | Kimi K2.6 (3x limits) |
| `opencode-go/kimi-k2.7-code`    | Kimi K2.7 Code        |
| `opencode-go/deepseek-v4-pro`   | DeepSeek V4 Pro       |
| `opencode-go/deepseek-v4-flash` | DeepSeek V4 Flash     |
| `opencode-go/mimo-v2-omni`      | MiMo V2 Omni          |
| `opencode-go/mimo-v2-pro`       | MiMo V2 Pro           |
| `opencode-go/minimax-m2.5`      | MiniMax M2.5          |
| `opencode-go/minimax-m2.7`      | MiniMax M2.7          |
| `opencode-go/qwen3.5-plus`      | Qwen3.5 Plus          |
| `opencode-go/qwen3.6-plus`      | Qwen3.6 Plus          |

`opencode-go/glm-5.2` uses a 1M-token context window and supports up to 131K output tokens. (No other per-model context/output limits are specified in source.)

## Getting started

The source documents two onboarding paths — an interactive tab and a non-interactive tab.

**Interactive** — run onboarding for the Go auth choice, then set a Go model as the default and verify availability:

```bash
openclaw onboard --auth-choice opencode-go
openclaw config set agents.defaults.model.primary "opencode-go/kimi-k2.6"
openclaw models list --provider opencode-go
```

**Non-interactive** — pass the key directly, then verify models are available:

```bash
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
openclaw models list --provider opencode-go
```

## Config example

The page gives a JSON5 config that sets the shared key and a Go model ref as the default primary model:

```json5
{
  env: { OPENCODE_API_KEY: "YOUR_API_KEY_HERE" }, // pragma: allowlist secret
  agents: { defaults: { model: { primary: "opencode-go/kimi-k2.6" } } },
}
```

## Advanced configuration

The source's advanced-configuration accordion has three notes:

- **Routing behavior** — OpenClaw handles per-model routing automatically when the model ref uses `opencode-go/...`. No additional provider config is required.
- **Runtime ref convention** — Runtime refs stay explicit: `opencode/...` for Zen, `opencode-go/...` for Go. This keeps upstream per-model routing correct across both catalogs.
- **Shared credentials** — The same `OPENCODE_API_KEY` is used by both the Zen and Go catalogs. Entering the key during setup stores credentials for both runtime providers.

The page also points back to [OpenCode](https://docs.openclaw.ai/providers/opencode) for the shared onboarding overview and the full Zen + Go catalog reference.

**Source**: OpenClaw documentation — `providers/opencode-go` (mirror `inbox/openclaw_docs/providers/opencode-go.md`)
**Last Updated**: 2026-06-22
**Status**: Active
