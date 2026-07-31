---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - model_selection
keywords:
  - openclaw model selection
  - model ref provider model
  - agents.defaults.model primary fallbacks
  - selection source configured auto user cron
  - model allowlist agents.defaults.models
  - model is not allowed
  - models.json registry
  - provider/* dynamic provider entries
topics:
  - OpenClaw
  - Model Selection
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/models
access_control_group: ["general"]
---

# OpenClaw — How Model Selection Works

## Overview

This note models OpenClaw's **model-selection concept**: how a model ref maps to a provider and model, the primary → fallbacks → provider-auth-failover resolution order, what a "selection source" (configured / auto / user / cron) means, the allowlist/catalog under `agents.defaults.models`, the "Model is not allowed" failure mode that stops replies, and the `models.json` registry that persists custom providers. It mirrors the selection-concept half of the `concepts/models` source page (the intro, "How model selection works", "Selection source and fallback behavior", "Quick model policy", "Onboarding", "Config keys (overview)" / "Safe allowlist edits", "Model is not allowed", and "Models registry"). The CLI/UX commands (`/model`, `openclaw models …`, scan) are a sibling procedure note.

## Model Refs vs Runtime

A **model ref** chooses a provider and a model; it does **not** usually choose the low-level agent runtime. OpenAI agent refs are the main exception: `openai/gpt-5.5` runs through the Codex app-server runtime by default on the official OpenAI provider. Subscription Copilot refs (`github-copilot/*`) can additionally be opted into the external GitHub Copilot agent runtime plugin — that path stays explicit (no `auto` fallback). Explicit runtime overrides belong on provider/model policy, not on the whole agent or session. In Codex runtime mode, the `openai/gpt-*` ref does not imply API-key billing; auth can come from a Codex account or `openai` OAuth profile.

## How Model Selection Works

OpenClaw selects models in this order:

1. **Primary model** — `agents.defaults.model.primary` (or `agents.defaults.model`).
2. **Fallbacks** — `agents.defaults.model.fallbacks` (in order).
3. **Provider auth failover** — auth failover happens inside a provider before moving to the next model.

Several related model surfaces feed this selection:

- `agents.defaults.models` is the allowlist/catalog of models OpenClaw can use (plus aliases). Use `provider/*` entries to limit visible providers while keeping provider discovery dynamic.
- `agents.defaults.imageModel` is used **only when** the primary model can't accept images.
- `agents.defaults.pdfModel` is used by the `pdf` tool. If omitted, the tool falls back to `agents.defaults.imageModel`, then the resolved session/default model.
- `agents.defaults.imageGenerationModel` is used by the shared image-generation capability. If omitted, `image_generate` can still infer an auth-backed provider default — it tries the current default provider first, then the remaining registered image-generation providers in provider-id order. If a specific provider/model is set, that provider's auth/API key must also be configured.
- `agents.defaults.musicGenerationModel` and `agents.defaults.videoGenerationModel` behave the same way for `music_generate` and `video_generate` respectively (current default provider first, then remaining registered providers in provider-id order).
- Per-agent defaults can override `agents.defaults.model` via `agents.list[].model` plus bindings (see Multi-agent routing).

## Selection Source and Fallback Behavior

The same `provider/model` can mean different things depending on where it came from — its **selection source**:

- **Configured defaults** (`agents.defaults.model.primary` and agent-specific primaries) are the normal starting point and use `agents.defaults.model.fallbacks`.
- **Auto fallback selections** are temporary recovery state. They are stored with `modelOverrideSource: "auto"` so later turns can keep using the fallback chain without probing a known-bad primary every time; OpenClaw periodically probes the original primary again, clears the auto selection when it recovers, and announces fallback/recovery transitions once per state change.
- **User session selections** are exact. `/model`, the model picker, `session_status(model=...)`, and `sessions.patch` store `modelOverrideSource: "user"`; if that selected provider/model is unreachable, OpenClaw fails visibly instead of falling through to another configured model.
- **Changing `agents.defaults.model.primary` does not rewrite existing session selections.** If status says `This session is pinned to X; config primary Y will apply to new/unpinned sessions.`, clear the current session selection with `/model default` so it inherits the configured primary again.
- **Cron `--model` / payload `model`** is a per-job primary. It still uses configured fallbacks unless the job supplies explicit payload `fallbacks` (use `fallbacks: []` for a strict cron run).
- CLI default-model and allowlist pickers respect `models.mode: "replace"` by listing explicit `models.providers.*.models` instead of loading the full built-in catalog.
- The Control UI model picker asks the Gateway for its configured model view: `agents.defaults.models` when present (including provider-wide `provider/*` entries), otherwise explicit `models.providers.*.models` plus providers with usable auth. The full built-in catalog is reserved for explicit browse views such as `models.list` with `view: "all"` or `openclaw models list --all`.

## Quick Model Policy

- Set the primary to the strongest latest-generation model available.
- Use fallbacks for cost/latency-sensitive tasks and lower-stakes chat.
- For tool-enabled agents or untrusted inputs, avoid older/weaker model tiers.

## Onboarding (recommended)

If you don't want to hand-edit config, run onboarding:

```bash
openclaw onboard
```

It can set up model + auth for common providers, including **OpenAI Code (Codex) subscription** (OAuth) and **Anthropic** (API key or Claude CLI).

## Config Keys (overview)

The selection-relevant config keys are:

- `agents.defaults.model.primary` and `agents.defaults.model.fallbacks`
- `agents.defaults.imageModel.primary` and `agents.defaults.imageModel.fallbacks`
- `agents.defaults.pdfModel.primary` and `agents.defaults.pdfModel.fallbacks`
- `agents.defaults.imageGenerationModel.primary` and `agents.defaults.imageGenerationModel.fallbacks`
- `agents.defaults.videoGenerationModel.primary` and `agents.defaults.videoGenerationModel.fallbacks`
- `agents.defaults.models` (allowlist + aliases + provider params + `provider/*` dynamic provider entries)
- `models.providers` (custom providers written into `models.json`)

Model refs are normalized to lowercase. Provider IDs are otherwise exact; use the provider ID advertised by the plugin.

### Safe allowlist edits

Use additive writes when updating `agents.defaults.models` by hand:

```bash
openclaw config set agents.defaults.models '{"openai/gpt-5.4":{}}' --strict-json --merge
```

**Clobber protection rules:** `openclaw config set` protects model/provider maps from accidental clobbers. A plain object assignment to `agents.defaults.models`, `models.providers`, or `models.providers.<id>.models` is rejected when it would remove existing entries. Use `--merge` for additive changes; use `--replace` only when the provided value should become the complete target value. Interactive provider setup and `openclaw configure --section model` also merge provider-scoped selections into the existing allowlist, so adding Codex, Ollama, or another provider does not drop unrelated model entries. Configure preserves an existing `agents.defaults.model.primary` when provider auth is re-applied. Explicit default-setting commands such as `openclaw models auth login --provider <id> --set-default` and `openclaw models set <model>` still replace `agents.defaults.model.primary`.

## "Model is not allowed" (and why replies stop)

If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and for session overrides. When a user selects a model that isn't in that allowlist, OpenClaw returns:

```
Model "provider/model" is not allowed. Use /models to list providers, or /models <provider> to list models.
Add it with: openclaw config set agents.defaults.models '{"provider/model":{}}' --strict-json --merge
```

This happens **before** a normal reply is generated, so the message can feel like it "didn't respond." The fix is to either add the model to `agents.defaults.models`, clear the allowlist (remove `agents.defaults.models`), or pick a model from `/model list`. When the rejected command included a runtime override such as `/model openai/gpt-5.5 --runtime codex`, fix the allowlist first, then retry the same `/model ... --runtime ...` command; for native Codex execution the selected model is still `openai/gpt-5.5` (the `codex` runtime selects the harness and uses Codex auth separately).

For local/GGUF models, store the full provider-prefixed ref in the allowlist, for example `ollama/gemma4:26b`, `lmstudio/Gemma4-26b-a4-it-gguf`, or the exact provider/model shown by `openclaw models list --provider <provider>`. Bare local filenames or display names are not enough when the allowlist is active. To limit providers without manually listing every model, add `provider/*` entries to `agents.defaults.models`:

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/*": {},
        "vllm/*": {},
      },
    },
  },
}
```

With that policy, `/model`, `/models`, and model pickers show the discovered catalog for those providers only; new models from the selected providers can appear without editing the allowlist. Exact `provider/model` entries can be mixed with `provider/*` entries when you need one specific model from another provider. An example allowlist using aliases:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-sonnet-4-6" },
      models: {
        "anthropic/claude-sonnet-4-6": { alias: "Sonnet" },
        "anthropic/claude-opus-4-6": { alias: "Opus" },
      },
    },
  },
}
```

## Models Registry (`models.json`)

Custom providers in `models.providers` are written into `models.json` under the agent directory (default `~/.openclaw/agents/<agentId>/agent/models.json`). Provider-plugin catalogs are stored as generated plugin-owned catalog shards under the agent's plugin state and loaded automatically. This file is merged by default unless `models.mode` is set to `replace`. Merge-mode precedence for matching provider IDs: a non-empty `baseUrl` already present in the agent `models.json` wins; a non-empty `apiKey` in the agent `models.json` wins only when that provider is not SecretRef-managed in the current config/auth-profile context; SecretRef-managed provider `apiKey` values are refreshed from source markers (`ENV_VAR_NAME` for env refs, `secretref-managed` for file/exec refs) instead of persisting resolved secrets; SecretRef-managed header values are refreshed from source markers (`secretref-env:ENV_VAR_NAME` for env refs, `secretref-managed` for file/exec refs); empty or missing agent `apiKey`/`baseUrl` fall back to config `models.providers`; and other provider fields are refreshed from config and normalized catalog data. Marker persistence is source-authoritative — OpenClaw writes markers from the active source config snapshot (pre-resolution), not from resolved runtime secret values, whenever it regenerates `models.json`, including command-driven paths like `openclaw agent`.

**Source**: OpenClaw documentation — `concepts/models` (mirror `inbox/openclaw_docs/concepts/models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
