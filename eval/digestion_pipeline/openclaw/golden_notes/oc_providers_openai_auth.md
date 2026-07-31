---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - openai
keywords:
  - openclaw openai provider
  - openai provider id auth
  - codex app-server runtime
  - codex subscription oauth
  - openai api key onboarding
  - auth.order.openai profile ordering
  - device-code oauth login
  - openai context window cap
  - openai memory embeddings
  - openclaw doctor --fix codex
topics:
  - OpenClaw
  - OpenAI Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/openai
access_control_group: ["general"]
---

# OpenClaw — OpenAI Provider Auth and Codex Runtime Setup

## Overview

This note is the procedure for authenticating and routing the OpenAI provider in OpenClaw, mirroring the auth/runtime half of the `providers/openai` source page (intro, Quick choice, Naming map, OpenClaw feature coverage, Memory embeddings, Getting started tabs, and Native Codex app-server auth). It covers the single `openai` provider id serving two auth shapes, the canonical `openai/*` model route, how embedded OpenAI agent turns run through the native Codex app-server runtime versus direct OpenAI API-key auth, the provider/runtime/auth/channel naming map, API-key and Codex-subscription onboarding (including device-code OAuth), `auth.order.openai` profile ordering and rotation, the context-window cap, catalog recovery, and OpenAI memory embeddings. The OpenAI media surfaces (image/video/voice/GPT-5 overlay) live in [oc_providers_openai_media](oc_providers_openai_media.md) and the Azure + transport/compaction tuning in [oc_providers_openai_advanced](oc_providers_openai_advanced.md).

## Provider id, model route, and auth shapes

OpenAI provides developer APIs for GPT models, and Codex is also available as a ChatGPT-plan coding agent through OpenAI's Codex clients; OpenClaw uses one provider id, `openai`, for both auth shapes, with `openai/*` as the canonical OpenAI model route. Embedded agent turns on OpenAI models run through the native Codex app-server runtime by default; direct OpenAI API-key auth remains available for non-agent OpenAI surfaces such as images, embeddings, speech, and realtime. The three usage classes are:

- **Agent models** — `openai/*` models through the Codex runtime; sign in with Codex auth for ChatGPT/Codex subscription use, or configure a Codex-compatible OpenAI API-key backup for API-key auth.
- **Non-agent OpenAI APIs** — direct OpenAI Platform access with usage-based billing through `OPENAI_API_KEY` or API-key onboarding.
- **Legacy config** — legacy Codex model refs are repaired by `openclaw doctor --fix` to `openai/*` plus the Codex runtime.

OpenAI explicitly supports subscription OAuth usage in external tools and workflows like OpenClaw. Provider, model, runtime, and channel are separate layers; if those labels are getting mixed together, read [Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes) before changing config.

## Quick choice

The source page recommends a setup per goal:

- **ChatGPT/Codex subscription with native Codex runtime** → `openai/gpt-5.5` (default OpenAI agent setup; sign in with Codex auth).
- **Direct API-key billing for agent models** → `openai/gpt-5.5` plus a Codex-compatible API-key profile (use `auth.order.openai` to place the backup after subscription auth).
- **Direct API-key billing through explicit OpenClaw** → `openai/gpt-5.5` plus provider/model runtime `openclaw` (select a normal `openai` API-key profile).
- **Latest ChatGPT Instant API alias** → `openai/chat-latest` (direct API-key only; a moving alias, not the default).
- **ChatGPT/Codex subscription auth through OpenClaw** → `openai/gpt-5.5` plus provider/model runtime `openclaw` (select an `openai` OAuth profile for the compatibility route).
- **Image generation / transparent-background images** → `openai/gpt-image-2` / `openai/gpt-image-1.5` (see [oc_providers_openai_media](oc_providers_openai_media.md)).

## Naming map

The names are similar but not interchangeable; the source maps each to its layer:

- `openai` → **Provider prefix** — canonical OpenAI model route; agent turns use the Codex runtime.
- legacy OpenAI Codex prefix → **Legacy prefix** — older model/profile namespace; `openclaw doctor --fix` migrates it to `openai`.
- `codex` plugin → **Plugin** — bundled OpenClaw plugin that provides native Codex app-server runtime and `/codex` chat controls.
- provider/model `agentRuntime.id: codex` → **Agent runtime** — force the native Codex app-server harness for matching embedded turns.
- `/codex ...` → **Chat command set** — bind/control Codex app-server threads from a conversation.
- `runtime: "acp", agentId: "codex"` → **ACP session route** — explicit fallback path that runs Codex through ACP/acpx.

This means a config can intentionally contain `openai/*` model refs while auth profiles point at either API-key or ChatGPT/Codex OAuth credentials. Use `auth.order.openai` for config; `openclaw doctor --fix` rewrites legacy Codex model refs, legacy Codex auth profile ids, and legacy Codex auth order to the canonical OpenAI route. GPT-5.5 is available through both direct API-key access and subscription/OAuth routes — for ChatGPT/Codex subscription plus native Codex execution use `openai/gpt-5.5`, since an unset runtime config now selects the Codex harness for OpenAI agent turns; use OpenAI API-key profiles only when you want direct API-key auth for an agent model. OpenAI agent model turns require the bundled Codex app-server plugin; when OpenClaw is explicitly selected with an `openai` OAuth profile, OpenClaw keeps the public model ref as `openai/*` and routes internally through the Codex-auth transport.

## OpenClaw feature coverage

The source enumerates which OpenAI capabilities map to which OpenClaw surface. The auth/runtime rows relevant to this note are: **Chat / Responses** → the `openai/<model>` model provider; **Codex subscription models** → `openai/<model>` with OpenAI OAuth; **Legacy Codex model refs** → legacy Codex model refs or `codex-cli/<model>`, repaired by doctor to `openai/<model>`; **Codex app-server harness** → `openai/<model>` with omitted runtime or `agentRuntime.id: codex`; **Server-side web search** → native OpenAI Responses tool (Yes, when web search is enabled and no provider pinned); **Embeddings** → the memory embedding provider. The media rows (Images, Videos, Text-to-speech, Batch/Streaming speech-to-text, Realtime voice) are documented in [oc_providers_openai_media](oc_providers_openai_media.md).

## Memory embeddings

OpenClaw can use OpenAI, or an OpenAI-compatible embedding endpoint, for `memory_search` indexing and query embeddings. The canonical config sets `memorySearch.provider` to `openai` and `model` to `text-embedding-3-small`:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",
        model: "text-embedding-3-small",
      },
    },
  },
}
```

For OpenAI-compatible endpoints that require asymmetric embedding labels, set `queryInputType` and `documentInputType` under `memorySearch`; OpenClaw forwards those as provider-specific `input_type` request fields (query embeddings use `queryInputType`; indexed memory chunks and batch indexing use `documentInputType`). See the [Memory configuration reference](https://docs.openclaw.ai/reference/memory-config#provider-specific-config) for the full example.

## Getting started — API key (OpenAI Platform)

Best for direct API access and usage-based billing. Steps: (1) create or copy an API key from the [OpenAI Platform dashboard](https://platform.openai.com/api-keys); (2) run onboarding; (3) verify the model is available.

```bash
openclaw onboard --auth-choice openai-api-key
# or pass the key directly:
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
# then verify:
openclaw models list --provider openai
```

**Route summary (API-key tab):** `openai/gpt-5.5` and `openai/gpt-5.4-mini` with omitted runtime or `agentRuntime.id: "codex"` → the Codex app-server harness (Codex-compatible OpenAI profile); `openai/gpt-5.5` with `agentRuntime.id: "openclaw"` → the OpenClaw embedded runtime (selected `openai` profile). `openai/*` agent models use the Codex app-server harness; to use API-key auth for an agent model, create a Codex-compatible API-key profile and order it with `auth.order.openai` — `OPENAI_API_KEY` remains the direct fallback for non-agent OpenAI API surfaces. The minimal config example sets `env: { OPENAI_API_KEY: "..." }` and `agents.defaults.model.primary: "openai/gpt-5.5"` (the same `primary` shown in the Codex config example below). To try ChatGPT's current Instant model, set the model to `openai/chat-latest` — a moving alias OpenAI documents as the latest Instant model in ChatGPT; OpenAI recommends `gpt-5.5` for production, so keep `openai/gpt-5.5` as the stable default, and note the alias accepts only `medium` text verbosity (OpenClaw normalizes incompatible text-verbosity overrides). OpenClaw does **not** expose `gpt-5.3-codex-spark` on the direct OpenAI API-key route — it is available only through Codex subscription catalog entries when your signed-in account exposes it.

## Getting started — Codex subscription

Best for using your ChatGPT/Codex subscription with native Codex app-server execution instead of a separate API key (Codex cloud requires ChatGPT sign-in). Steps: (1) run Codex OAuth; (2) use the canonical OpenAI model route; (3) verify Codex auth is available. For headless or callback-hostile setups, add `--device-code` to sign in with a ChatGPT device-code flow instead of the localhost browser callback.

```bash
openclaw onboard --auth-choice openai
# or run OAuth directly:
openclaw models auth login --provider openai
# headless / callback-hostile setups:
openclaw models auth login --provider openai --device-code
# set the canonical model route (no runtime config required for the default path):
openclaw config set agents.defaults.model.primary openai/gpt-5.5
# verify; then in chat send `/codex status` or `/codex models`:
openclaw models list --provider openai
```

No runtime config is required for the default path: OpenAI agent turns select the native Codex app-server runtime automatically, and OpenClaw installs or repairs the bundled Codex plugin when this route is chosen. **Route summary (Codex tab):** `openai/gpt-5.5` with omitted runtime / `agentRuntime.id: "codex"` → native Codex app-server harness (Codex sign-in or ordered `openai` auth profile); `openai/gpt-5.5` with `agentRuntime.id: "openclaw"` → OpenClaw embedded runtime with internal Codex-auth transport (selected `openai` OAuth profile); a legacy Codex GPT-5.5 ref and `codex-cli/gpt-5.5` → repaired by doctor to `openai/gpt-5.5`. Prefer `openai/gpt-5.5` for new subscription-backed agent config; `gpt-5.3-codex-spark` is limited to accounts whose Codex subscription catalog advertises it, and direct OpenAI API-key and Azure refs for it remain suppressed.

The Codex config example enables the bundled `codex` plugin, pins the model to `openai/gpt-5.5`, and (with an API-key backup) orders auth under `openai` so OpenClaw tries the subscription first, then the API key, while staying on the Codex harness:

```json5
{
  plugins: { entries: { codex: { enabled: true } } },
  agents: { defaults: { model: { primary: "openai/gpt-5.5" } } },
  auth: {
    order: {
      openai: [
        "openai:user@example.com",
        "openai:api-key-backup",
      ],
    },
  },
}
```

Onboarding no longer imports OAuth material from `~/.codex` — sign in with browser OAuth (default) or the device-code flow, and OpenClaw manages the resulting credentials in its own agent auth store.

### Check and recover Codex OAuth routing

Use these commands to inspect the active model/runtime/auth route, repair stale legacy refs/pins, re-login when no usable profile exists, and register multiple named OAuth logins:

```bash
openclaw models status
openclaw models auth list --provider openai
openclaw config get agents.defaults.model --json
openclaw config get models.providers.openai.agentRuntime --json
# repair stale legacy Codex GPT refs / runtime session pins:
openclaw doctor --fix && openclaw config validate
# re-login + probe if no usable profile:
openclaw models auth login --provider openai
openclaw models status --probe --probe-provider openai
# multiple named OAuth logins (controlled later via auth ordering or `/model ...@<profileId>`):
openclaw models auth login --provider openai --profile-id openai:ritsuko
```

For a specific agent, add `--agent <id>`. Run `openclaw doctor --fix` to migrate older legacy OpenAI Codex prefix profile ids and order entries before relying on ordering. Chat `/status` shows which model runtime is active — the bundled Codex app-server harness appears as `Runtime: OpenAI Codex` for OpenAI agent model turns. If legacy Codex model refs or stale OpenAI runtime pins remain in config or session state, `openclaw doctor --fix` rewrites them to `openai/*` with the Codex runtime unless OpenClaw is explicitly configured.

### Context window cap

OpenClaw treats model metadata and the runtime context cap as separate values. For `openai/gpt-5.5` through the Codex OAuth catalog the native `contextWindow` is `1000000` and the default runtime `contextTokens` cap is `272000` (the smaller default cap has better latency and quality in practice). Override it with `contextTokens` — use `contextWindow` to declare native model metadata and `contextTokens` to limit the runtime context budget:

```json5
{
  models: {
    providers: {
      openai: {
        models: [{ id: "gpt-5.5", contextTokens: 160000 }],
      },
    },
  },
}
```

### Catalog recovery

OpenClaw uses upstream Codex catalog metadata for `gpt-5.5` when present. If live Codex discovery omits the `gpt-5.5` row while the account is authenticated, OpenClaw synthesizes that OAuth model row so cron, sub-agent, and default-model runs do not fail with `Unknown model`.

## Native Codex app-server auth

The native Codex app-server harness uses `openai/*` model refs plus omitted runtime config or `agentRuntime.id: "codex"`, but its auth is still account-based. OpenClaw selects auth in this order:

1. Ordered OpenAI auth profiles for the agent, preferably under `auth.order.openai`. Run `openclaw doctor --fix` to migrate older legacy Codex auth profile ids and legacy Codex auth order.
2. The app-server's existing account, such as a local Codex CLI ChatGPT sign-in.
3. For local stdio app-server launches only, `CODEX_API_KEY`, then `OPENAI_API_KEY`, when the app-server reports no account and still requires OpenAI auth.

That means a local ChatGPT/Codex subscription sign-in is not replaced just because the gateway process also has `OPENAI_API_KEY` for direct OpenAI models or embeddings; env API-key fallback is only the local stdio no-account path and is not sent to WebSocket app-server connections. When a subscription-style Codex profile is selected, OpenClaw keeps `CODEX_API_KEY` and `OPENAI_API_KEY` out of the spawned stdio app-server child and sends the selected credentials through the app-server login RPC. When that subscription profile is blocked by a Codex usage limit, OpenClaw can rotate to the next ordered `openai:*` API-key profile without changing the selected model or dropping out of the Codex harness; once the subscription reset time passes, the subscription profile is eligible again.

**Source**: OpenClaw documentation — `providers/openai` (mirror `inbox/openclaw_docs/providers/openai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
