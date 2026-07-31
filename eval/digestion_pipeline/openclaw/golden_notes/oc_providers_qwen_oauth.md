---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - qwen_oauth
keywords:
  - qwen-oauth provider id
  - qwen portal token
  - portal.qwen.ai/v1
  - auth-choice qwen-oauth
  - QWEN_API_KEY
  - qwen-oauth/qwen3.5-plus
  - qwen portal oauth migration
  - dashscope vs portal
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/qwen-oauth
access_control_group: ["general"]
---

# OpenClaw — Configuring the Qwen OAuth / Portal Provider (`qwen-oauth`)

## Overview

This note is the setup procedure for `qwen-oauth`, OpenClaw's **Qwen Portal provider id** — the second Qwen-facing provider id exposed by the Qwen plugin (alongside the canonical `qwen` provider). `qwen-oauth` targets the Qwen Portal endpoint at `https://portal.qwen.ai/v1` and keeps older Qwen OAuth / portal setups addressable through a distinct provider id. It mirrors the `providers/qwen-oauth` source page: when to choose this provider id vs the canonical `qwen` provider, onboarding via `openclaw onboard --auth-choice qwen-oauth` (or the `QWEN_API_KEY` env var), the documented defaults, the seeded `qwen-oauth/qwen3.5-plus` default model, and migration plus troubleshooting for legacy Qwen Portal OAuth / Qwen CLI credentials. The deeper Qwen provider surface (plan types, full catalog, multimodal add-ons) lives in the sibling `oc_providers_qwen` note.

`qwen-oauth` is **not the recommended first choice for new Qwen users.** Use it specifically when you already hold a current Qwen Portal token for `https://portal.qwen.ai/v1`, or when you are migrating an older Qwen Portal / Qwen CLI setup and want to keep those credentials separate from the canonical Qwen Cloud provider. For new Qwen Cloud setups, the source page directs you to the [Qwen](https://docs.openclaw.ai/providers/qwen) provider with the Standard ModelStudio endpoint unless you specifically have a current Qwen Portal token.

## Setup

Provide your portal token through onboarding, which stores the credential under the selected provider id:

```bash
openclaw onboard --auth-choice qwen-oauth
```

Or set the env var directly:

```bash
export QWEN_API_KEY="<your-qwen-portal-token>" # pragma: allowlist secret
```

## Defaults

The `qwen-oauth` provider id ships with these documented defaults:

- Provider: `qwen-oauth`
- Aliases: `qwen-portal`, `qwen-cli`
- Base URL: `https://portal.qwen.ai/v1`
- Env var: `QWEN_API_KEY`
- API style: OpenAI-compatible
- Default model: `qwen-oauth/qwen3.5-plus`

## How this differs from Qwen

OpenClaw has two Qwen-facing provider ids:

| Provider     | Endpoint family                                          | Best for                                                                               |
| ------------ | -------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `qwen`       | Qwen Cloud / Alibaba DashScope and Coding Plan endpoints | New API-key setups, Standard pay-as-you-go, Coding Plan, multimodal DashScope features |
| `qwen-oauth` | Qwen Portal endpoint at `portal.qwen.ai/v1`              | Existing Qwen Portal tokens and legacy Qwen OAuth / CLI setups                         |

Both providers use OpenAI-compatible request shapes, but they are **separate auth surfaces.** A token stored for `qwen-oauth` should not be treated as a DashScope or ModelStudio key, and a new DashScope key should use the canonical `qwen` provider instead.

## When to choose Qwen OAuth / Portal

Choose the `qwen-oauth` provider id when:

- You already have a working Qwen Portal token.
- You are preserving a legacy Qwen OAuth or Qwen CLI workflow while moving to OpenClaw's provider model.
- You need to test compatibility with the Qwen Portal endpoint specifically.

Choose [Qwen](https://docs.openclaw.ai/providers/qwen) for new setup, broader endpoint choices, Standard ModelStudio, Coding Plan, and the full Qwen plugin catalog.

## Models

The Qwen plugin catalog seeds the Qwen Portal default model:

- `qwen-oauth/qwen3.5-plus`

Availability depends on the current Qwen Portal account and token. If your account uses ModelStudio / DashScope API keys instead, configure the canonical `qwen` provider rather than `qwen-oauth`:

```bash
openclaw onboard --auth-choice qwen-standard-api-key
openclaw models set qwen/qwen3-coder-plus
```

## Migration

Legacy Qwen Portal OAuth profiles **may not be refreshable.** If a portal profile stops working, re-authenticate with a current token or switch to the Standard Qwen provider via `openclaw onboard --auth-choice qwen-standard-api-key`. Standard global ModelStudio uses the endpoint `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.

## Troubleshooting

The source page documents three failure modes for `qwen-oauth`:

- **Portal OAuth refresh failures:** legacy Qwen Portal OAuth profiles may not be refreshable. Re-run onboarding with a current token.
- **Wrong endpoint errors:** confirm the model ref starts with `qwen-oauth/` when using a portal token. Use `qwen/` refs only for the canonical Qwen provider.
- **`QWEN_API_KEY` confusion:** both Qwen pages mention this env var, but onboarding stores credentials under the selected provider id. Prefer onboarding when you keep both `qwen` and `qwen-oauth` available on the same machine.

**Source**: OpenClaw documentation — `providers/qwen-oauth` (mirror `inbox/openclaw_docs/providers/qwen-oauth.md`)
**Last Updated**: 2026-06-22
**Status**: Active
