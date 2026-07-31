---
tags:
  - resource
  - documentation
  - claude_code
  - amazon_bedrock
  - model_config
keywords:
  - pin model versions
  - bedrock inference profile id
  - anthropic_default_opus_model
  - cross-region inference profile
  - application inference profile arn
  - modeloverrides
  - startup model checks
  - small/fast model fallback
topics:
  - Claude Code
  - Amazon Bedrock
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/amazon-bedrock
access_control_group: ["general"]
---

# Claude Code on Amazon Bedrock — Pin Model Versions and Startup Checks

## Overview

Once Bedrock is enabled (see [Bedrock setup](cc_amazon_bedrock_setup.md)), this procedure controls **which Claude model each alias resolves to** on Bedrock. Without pinning, aliases such as `sonnet` and `opus` resolve to Claude Code's built-in Bedrock default, which can lag the newest release and may not yet be available in your account. Pinning the `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` environment variables to specific Bedrock model IDs — cross-region inference-profile IDs (`us.` prefix; `us-gov.` for GovCloud) or application-inference-profile ARNs — lets you control exactly when users move to a new model, which is important when deploying to multiple users.

This note covers the pin step, mapping multiple versions of a family to distinct inference profiles via `modelOverrides`, the small/fast-model-to-primary fallback, and the **startup model check** that prompts to update stale pins or falls back when an unpinned default is unavailable. The full environment-variable list lives in [Model configuration](https://code.claude.com/docs/en/model-config#pin-models-for-third-party-deployments).

## 4. Pin model versions

Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code's built-in default for Bedrock, which can lag the newest release and may not yet be available in your account. Claude Code [falls back](#startup-model-checks) to the previous version at startup when the default is unavailable, but pinning lets you control when your users move to a new model.

Set these environment variables to specific Bedrock model IDs. Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Bedrock resolves to Opus 4.6 — set it to the Opus 4.8 ID to use the latest model:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

These variables use cross-region inference profile IDs (with the `us.` prefix). If you use a different region prefix or application inference profiles, adjust accordingly. In AWS GovCloud regions, use the `us-gov.` prefix. For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](https://code.claude.com/docs/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.

### Default models and the small/fast-model fallback

Claude Code uses these default models when no pinning variables are set:

| Model type       | Default value                                  |
| :--------------- | :--------------------------------------------- |
| Primary model    | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Small/fast model | Same as primary model                          |

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Bedrock, Claude Code defaults this to the primary model because Haiku may not be enabled in every account or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID that is available in your account.

### Customizing the model further

To customize models further, use one of these methods — an inference profile ID or an application-inference-profile ARN:

```bash
# Using inference profile ID
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'
```

The same block also exposes the prompt-caching toggles `DISABLE_PROMPT_CACHING=1` (disable caching) and `ENABLE_PROMPT_CACHING_1H=1` (request a 1-hour cache TTL instead of the 5-minute default; billed at a higher rate). Prompt caching may not be available in all Bedrock regions; if cache token counts stay at zero, check the supported models, regions, and limits in the Bedrock documentation. The caching mechanism and cache-lifetime detail are covered in [prompt caching](https://code.claude.com/docs/en/prompt-caching#cache-lifetime).

### Map each model version to an inference profile

The `ANTHROPIC_DEFAULT_*_MODEL` environment variables configure **one inference profile per model family**. If your organization needs to expose several versions of the same family in the `/model` picker, each routed to its own application inference profile ARN, use the `modelOverrides` setting in your settings file instead.

This example maps four Opus versions to distinct ARNs so users can switch between them without bypassing your organization's inference profiles:

```json
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

When a user selects one of these versions in `/model`, Claude Code calls Bedrock with the mapped ARN. Versions without an override fall back to the built-in Bedrock model ID or any matching inference profile discovered at startup. See [Override model IDs per version](https://code.claude.com/docs/en/model-config#override-model-ids-per-version) for details on how overrides interact with `availableModels` and other model settings.

## Startup model checks

When Claude Code starts with Bedrock configured, it verifies that the models it intends to use are accessible in your account. This check requires Claude Code v2.1.94 or later.

- **Pinned version older than the current default:** if you have pinned a model version that is older than the current Claude Code default, and your account can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your user settings file and restarts Claude Code. Declining is remembered until the next default version change. Pins that point to an application inference profile ARN are skipped, since those are managed by your administrator.
- **No pin and default unavailable:** if you have not pinned a model and the current default is unavailable in your account, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in your Bedrock account or pin a version to make the choice permanent.

**Source**: https://code.claude.com/docs/en/amazon-bedrock
**Last Updated**: 2026-06-13
**Status**: Active
