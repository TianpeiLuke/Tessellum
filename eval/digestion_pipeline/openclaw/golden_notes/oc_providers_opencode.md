---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - opencode
keywords:
  - openclaw opencode provider
  - opencode zen catalog
  - opencode go catalog
  - opencode_api_key shared credentials
  - opencode runtime provider split
  - gemini replay behavior opencode
  - openclaw onboard opencode-zen
  - opencode multi-model proxy
topics:
  - OpenClaw
  - OpenCode Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/opencode
access_control_group: ["general"]
---

# OpenClaw — Configuring the OpenCode Provider (Zen + Go Catalogs)

## Overview

This note is the procedure for connecting OpenClaw to **OpenCode**, a hosted model service that exposes two catalogs — **Zen** (a curated multi-model proxy over Claude, GPT, and Gemini) and **Go** (the OpenCode-hosted Kimi, GLM, and MiniMax lineup). It mirrors the `providers/opencode` source page end to end: the catalog/prefix/runtime-provider table, the two onboarding tabs (Zen and Go), the JSON5 config example, the per-catalog built-in model tables, and the advanced configuration (API-key aliases, shared credentials across both catalogs, billing/dashboard, and the Gemini vs non-Gemini replay behavior). The key operational fact is that **both catalogs share one OpenCode API key**, but OpenClaw deliberately keeps two distinct runtime provider ids (`opencode` and `opencode-go`) so upstream per-model routing stays correct, while onboarding and docs treat them as one OpenCode setup.

## Catalogs, Prefixes, and Runtime Providers

OpenCode exposes two hosted catalogs in OpenClaw. Each catalog has its own model-ref prefix and its own runtime provider id, summarized verbatim from the source table:

| Catalog | Prefix | Runtime provider |
| ------- | ----------------- | ---------------- |
| **Zen** | `opencode/...` | `opencode` |
| **Go** | `opencode-go/...` | `opencode-go` |

Both catalogs use the **same OpenCode API key**. OpenClaw keeps the runtime provider ids split so upstream per-model routing stays correct, but onboarding and docs treat them as one OpenCode setup. Choose the **Zen** catalog for the curated OpenCode multi-model proxy (Claude, GPT, Gemini); choose the **Go** catalog for the OpenCode-hosted Kimi, GLM, and MiniMax lineup.

## Getting Started

### Zen catalog (curated multi-model proxy)

Run onboarding for the Zen catalog, optionally passing the key directly instead of using the interactive auth choice:

```bash
openclaw onboard --auth-choice opencode-zen
# Or pass the key directly:
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

Then set a Zen model as the default and verify the catalog is available:

```bash
openclaw config set agents.defaults.model.primary "opencode/claude-opus-4-6"
openclaw models list --provider opencode
```

### Go catalog (Kimi / GLM / MiniMax lineup)

Onboarding for the Go catalog follows the same shape, with the `opencode-go` auth choice and key flag:

```bash
openclaw onboard --auth-choice opencode-go
# Or pass the key directly:
openclaw onboard --opencode-go-api-key "$OPENCODE_API_KEY"
```

Set a Go model as the default and verify with the Go provider id:

```bash
openclaw config set agents.defaults.model.primary "opencode-go/kimi-k2.6"
openclaw models list --provider opencode-go
```

Note that both `--opencode-zen-api-key` and `--opencode-go-api-key` accept the same `$OPENCODE_API_KEY` value — there is one underlying credential (see Shared Credentials below), so a single onboarding pass is sufficient.

## Config Example

The minimal file config supplies the shared key via `env.OPENCODE_API_KEY` and selects a default model by its prefixed ref (verbatim from source):

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

## Built-in Catalogs

OpenClaw ships built-in catalog rows for each runtime provider; the source documents the runtime provider id plus example model refs for each:

| Catalog | Runtime provider | Example models |
| ------- | ---------------- | -------------- |
| **Zen** | `opencode` | `opencode/claude-opus-4-6`, `opencode/gpt-5.5`, `opencode/gemini-3-pro` |
| **Go** | `opencode-go` | `opencode-go/kimi-k2.6`, `opencode-go/glm-5`, `opencode-go/minimax-m2.5` |

The Go catalog is documented in fuller depth on its own sibling page; see [oc_providers_opencode_go](oc_providers_opencode_go.md).

## Advanced Configuration

The source page's advanced section is a five-item accordion plus a tip; each item is reproduced faithfully below.

- **API key aliases** — `OPENCODE_ZEN_API_KEY` is also supported as an alias for `OPENCODE_API_KEY`.
- **Shared credentials** — Entering one OpenCode key during setup stores credentials for **both** runtime providers; you do not need to onboard each catalog separately. (The closing tip restates this: entering one OpenCode key during setup stores credentials for both the Zen and Go runtime providers, so you only need to onboard once.)
- **Billing and dashboard** — You sign in to OpenCode, add billing details, and copy your API key. Billing and catalog availability are managed from the OpenCode dashboard.
- **Gemini replay behavior** — Gemini-backed OpenCode refs stay on the **proxy-Gemini path**, so OpenClaw keeps Gemini thought-signature sanitation there *without* enabling native Gemini replay validation or bootstrap rewrites.
- **Non-Gemini replay behavior** — Non-Gemini OpenCode refs keep the minimal **OpenAI-compatible replay policy**.

These replay distinctions are why the two runtime provider ids stay split even though they share one key: routing must know whether a given OpenCode ref is Gemini-backed (proxy-Gemini sanitation) or not (minimal OpenAI-compatible replay).

**Source**: OpenClaw documentation — `providers/opencode` (mirror `inbox/openclaw_docs/providers/opencode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
