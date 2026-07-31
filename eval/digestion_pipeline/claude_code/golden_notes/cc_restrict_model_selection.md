---
tags:
  - resource
  - documentation
  - claude_code
  - model_config
  - administration
keywords:
  - restrict model selection
  - availablemodels allowlist
  - enforceavailablemodels
  - managed settings model governance
  - merge behavior
  - mantle model ids
  - modeloverrides pinning
  - custom model option
topics:
  - Claude Code
  - Model Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/model-config
access_control_group: ["general"]
---

# Restrict Model Selection in Claude Code

## Overview

Enterprise administrators restrict which models users can select by setting `availableModels` (an allowlist) in managed or policy settings. The allowlist applies to every surface where a user can name a model, and a companion `enforceAvailableModels` flag extends it to the picker's Default option. This note covers how the allowlist behaves across surfaces, how blocked selections are handled, the precedence/merge rules between settings levels, Mantle model IDs on Bedrock, adding a single custom picker entry, and the model-pinning settings (`modelOverrides`, capability declarations) used for governance on third-party deployments. The settings files themselves (managed/policy/user/project precedence) are documented at [settings](https://code.claude.com/docs/en/settings).

## The `availableModels` Allowlist

Set `availableModels` in [managed or policy settings](https://code.claude.com/docs/en/settings#settings-files) to restrict which models users can select. When set, the allowlist applies to every surface where a user can name a model:

- **Main session model**: `/model`, the `--model` flag, and the `ANTHROPIC_MODEL` environment variable.
- **Subagent models**: the `model` field in subagent frontmatter, the Agent tool's `model` parameter, the model picker in `/agents`, and `CLAUDE_CODE_SUBAGENT_MODEL`.
- **Advisor model**: the configured `advisorModel` setting.
- **Fallback chains**: elements of a fallback model chain outside the list are dropped.

```json
{
  "availableModels": ["sonnet", "haiku"]
}
```

How blocked selections are handled differs by surface:

- Switching to a blocked model with `/model` is **rejected with an error**.
- A blocked `--model` flag or `ANTHROPIC_MODEL` value is **replaced at startup with a warning** naming both the requested and substituted models; the session starts on the default model.
- A blocked subagent or advisor override **falls back to the inherited or default model** rather than failing the request.

## Default Model Behavior

By default, the **Default** option in the model picker is not affected by `availableModels`. It remains available and represents the system's runtime default based on the user's subscription tier.

To extend the allowlist to the Default option, set `enforceAvailableModels` to `true` in managed or policy settings alongside a non-empty `availableModels` list. When the tier default is not in the allowlist, Default resolves to the **first allowed entry** instead of the tier default. This requires Claude Code v2.1.175 or later.

An empty `availableModels` array never engages enforcement: even with `availableModels: []`, users can still use Claude Code with the Default model for their tier regardless of `enforceAvailableModels`.

## Control the Model Users Run On

The `model` setting is an initial selection, **not enforcement**. It sets which model is active when a session starts, but users can still open `/model` and pick Default, which resolves to the system default for their tier regardless of what `model` is set to. To fully control the model experience, combine:

- **`availableModels`**: restricts which named models users can switch to.
- **`enforceAvailableModels`**: extends the allowlist to the Default option so Default cannot resolve to a model outside the list.
- **`model`**: sets the initial model selection when a session starts.
- **`ANTHROPIC_DEFAULT_SONNET_MODEL` / `_OPUS_MODEL` / `_HAIKU_MODEL` / `_FABLE_MODEL`**: control what the Default option and the `sonnet`, `opus`, `haiku`, and `fable` aliases resolve to.

```json
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "enforceAvailableModels": true,
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Without `enforceAvailableModels` or the `env` block, a user who picks Default would get the latest release for their tier, bypassing the version pin. The two settings cover different scopes: `enforceAvailableModels` makes Default obey the allowlist, while the `env` block pins which version a permitted alias such as `sonnet` resolves to. Use `enforceAvailableModels` alone when restricting model families is enough; add the `env` block when you also need to pin a specific version.

## Merge Behavior

When `availableModels` is set in user, project, and local settings only, arrays are **merged and deduplicated** across those levels. When set in managed or policy settings, the managed/policy value **replaces the merged result entirely**: entries added in user or project settings cannot widen it. Managed and policy settings replace lower-precedence values for `enforceAvailableModels` the same way. As of v2.1.175 this is the only way to enforce a strict allowlist; earlier versions merge the managed list with lower-precedence entries.

## Mantle Model IDs

When the [Bedrock Mantle endpoint](https://code.claude.com/docs/en/amazon-bedrock#use-the-mantle-endpoint) is enabled, entries in `availableModels` that start with `anthropic.` are added to the `/model` picker as custom options and routed to the Mantle endpoint. The setting still restricts the picker to listed entries, so include the standard aliases alongside any Mantle IDs.

## Add a Custom Model Option

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` to add a single custom entry to the `/model` picker without replacing the built-in aliases — useful for testing model IDs Claude Code does not list by default. The custom entry appears at the bottom of the picker. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` and `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` are optional; if omitted, the model ID is used as the name and the description defaults to `Custom model (<model-id>)`. Claude Code skips validation for this model ID, so any string the API endpoint accepts works. For LLM gateway deployments, Claude Code can instead populate the picker from the gateway's `/v1/models` endpoint when `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` is set.

## Pin and Override Model IDs (Third-Party Governance)

On Bedrock, Vertex AI, Foundry, or Claude Platform on AWS, pin model versions before rolling out to users — without pinning, aliases resolve to a provider default that can lag the newest release or be unavailable in an account. Set the `ANTHROPIC_DEFAULT_*_MODEL` variables to version-specific IDs so admins control when users move to a new model. Companion `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` variables override the picker display and declare which features (effort, thinking, etc.) a provider-specific ID supports, since provider IDs often don't match Claude Code's built-in capability detection.

When several versions of one family must map to distinct provider IDs, use the `modelOverrides` setting, which maps individual Anthropic model IDs to provider-specific strings (Bedrock inference profile ARN, Vertex version name, Foundry deployment name) for governance, cost allocation, or regional routing:

```json
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

`modelOverrides` works alongside `availableModels`: the allowlist is evaluated against the **Anthropic model ID, not the override value**, so an entry like `"opus"` still matches even when Opus versions are mapped to ARNs. Values supplied directly through `ANTHROPIC_MODEL`, `--model`, or the `ANTHROPIC_DEFAULT_*_MODEL` variables are passed to the provider as-is and are not transformed by `modelOverrides`. Note that the allowlist's filtering strips any `[1m]` suffix from both the allowlist entry and the requested model before matching, but does not strip provider-specific prefixes such as `us.anthropic.`.

**Source**: https://code.claude.com/docs/en/model-config
**Last Updated**: 2026-06-13
**Status**: Active
