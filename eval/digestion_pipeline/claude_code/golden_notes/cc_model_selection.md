---
tags:
  - resource
  - documentation
  - claude_code
  - model_config
  - model_selection
keywords:
  - model alias
  - model selection
  - opus sonnet haiku fable
  - opusplan
  - setting your model
  - default model
  - provider resolution
  - checking current model
topics:
  - Claude Code
  - Model Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/model-config
access_control_group: ["general"]
---

# Claude Code — Model Selection

## Overview

The `model` setting in Claude Code accepts either a **model alias** (a convenient shorthand like `opus` or `sonnet` that points to the recommended version and updates over time) or an explicit **model name** (a full Anthropic API name like `claude-opus-4-8`, a Bedrock inference profile ARN, a Foundry deployment name, or a Vertex version name). Aliases free you from remembering exact version numbers, but the version an alias resolves to depends on your **provider** and **account type** — so the same `opus` alias maps to different concrete models on the Anthropic API versus Bedrock.

This note covers the alias catalog, the special-purpose Fable 5 model, the four prioritized ways to set a model (and how resumed sessions keep theirs), and how to check which model is active. Restricting which models users may pick is a separate admin concern (allowlists, enforcement, Mantle IDs) covered in the [restrict-model-selection note](cc_restrict_model_selection.md); reasoning controls (effort, thinking) are in [effort & thinking](cc_effort_level_and_thinking.md), the 1M window in [extended context](cc_extended_context_1m.md), and the `opusplan` hybrid plus fallback chains in [fallback models](cc_fallback_models.md).

> Note: `ANTHROPIC_BASE_URL` changes *where* requests are sent, not *which* model answers them. To route Claude through an LLM gateway, see [LLM gateway configuration](https://code.claude.com/docs/en/llm-gateway).

## Model aliases

Model aliases provide a convenient way to select model settings without remembering exact version numbers:

| Model alias | Behavior |
| --- | --- |
| **`default`** | Special value that clears any model override and reverts to the recommended model for your account type. Not itself a model alias. |
| **`best`** | Uses Fable 5 where your organization has access to it, otherwise the latest Opus model. |
| **`fable`** | Uses Claude Fable 5 for your hardest and longest-running tasks. |
| **`sonnet`** | Uses the latest Sonnet model for daily coding tasks. |
| **`opus`** | Uses the latest Opus model for complex reasoning tasks. |
| **`haiku`** | Uses the fast and efficient Haiku model for simple tasks. |
| **`sonnet[1m]`** | Uses Sonnet with a 1 million token context window for long sessions. |
| **`opus[1m]`** | Uses Opus with a 1 million token context window for long sessions. |
| **`opusplan`** | Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution. |

The `[1m]` aliases select the 1M-token context variants (see [extended context](cc_extended_context_1m.md)); `opusplan` is the plan→execute hybrid covered in [fallback models](cc_fallback_models.md).

### Alias resolution by provider and account type

Aliases point to the recommended version *for your provider* and update over time. The same alias resolves differently across providers:

- On the **Anthropic API**, `opus` resolves to Opus 4.8 and `sonnet` resolves to Sonnet 4.6.
- On **Claude Platform on AWS**, `opus` resolves to Opus 4.7 and `sonnet` resolves to Sonnet 4.6.
- On **Bedrock, Vertex, and Foundry**, `opus` resolves to Opus 4.6 and `sonnet` resolves to Sonnet 4.5. Newer models are available there only by selecting the full model name explicitly or by setting `ANTHROPIC_DEFAULT_OPUS_MODEL` / `ANTHROPIC_DEFAULT_SONNET_MODEL`.

The `default` value also resolves by **account type**:

- **Max, Team Premium, Enterprise pay-as-you-go, and Anthropic API**: Opus 4.8
- **Claude Platform on AWS**: Opus 4.7
- **Pro, Team Standard, and Enterprise subscription seats**: Sonnet 4.6
- **Bedrock, Vertex, and Foundry**: Sonnet 4.5

("Enterprise pay-as-you-go" means an Enterprise organization billed by usage rather than by subscription seat.)

To **pin** to a specific version regardless of how the alias drifts over time, use the full model name (for example, `claude-opus-4-8`) or set the corresponding environment variable. The family-level variables `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL` control what each alias (and the Default option) resolves to. (`ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of `ANTHROPIC_DEFAULT_HAIKU_MODEL`.) Claude Code also automatically uses prompt caching, which can be disabled globally or per model tier (`DISABLE_PROMPT_CACHING`, `DISABLE_PROMPT_CACHING_HAIKU/SONNET/OPUS/FABLE`); the cost mechanics of caching are covered separately under [prompt caching](https://code.claude.com/docs/en/prompt-caching).

> Note: Opus 4.8 requires Claude Code v2.1.154 or later. Run `claude update` to upgrade.

## Work with Fable 5

Claude Fable 5 is the most capable model in Claude Code, suited to tasks larger than a single sitting. It sustains long autonomous sessions, investigates before acting, and verifies its work more often than smaller models.

Fable 5 is **not the default model** on any account type. Select it with `/model fable`, a `model` setting, or the `best` alias where Fable 5 is available. Choosing it with `/model` saves it as the selected model in user settings, so later sessions start on Fable 5 until you change models. Requests that its safety classifiers flag — most often in cybersecurity and biology domains — trigger automatic content-based model fallback to Opus (see [fallback models](cc_fallback_models.md)).

To get the most from Fable 5:

- **Describe the outcome, not the steps**: hand it the result you want and let it plan the path.
- **Hand it ambiguous problems**: root-cause investigations, outage debugging, and architecture decisions are where the extra investigation and verification pay off.
- **Skip the verification reminders**: it verifies its own work with less prompting, so reminders to test or check are usually unnecessary.
- **Size up larger tasks**: give it work you would normally break into pieces; it holds long sessions without losing the thread.

> Note: Fable 5 requires Claude Code v2.1.170 or later — older versions do not show it in the model picker. It is not available under zero data retention, where the `/model` picker either omits it or shows it disabled.

## Setting your model

You can configure your model in several ways, listed in **order of priority**:

1. **During session** — Use `/model <alias|name>` to switch immediately, or run `/model` with no argument to open the picker. The picker asks for confirmation when the conversation has prior output, since the next response re-reads the full history without cached context.
2. **At startup** — Launch with `claude --model <alias|name>`.
3. **Environment variable** — Set `ANTHROPIC_MODEL=<alias|name>`.
4. **Settings** — Configure permanently in your settings file using the `model` field.

```bash
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

As of v2.1.153, `/model` saves your choice as the default for new sessions by writing the `model` field in your user settings. In the picker, `Enter` switches model and saves it as your default, while `s` switches for this session only; typing `/model <name>` directly behaves like `Enter`. **Project and managed settings still take precedence and reapply on the next launch.** (In v2.1.144 through v2.1.152, `/model` applied to the current session only and `d` saved a default.)

The `--model` flag and `ANTHROPIC_MODEL` apply only to the session launched with them, so to run different models in different terminals simultaneously, launch each with its own `--model` flag rather than switching with `/model`.

**Resumed sessions** started with `claude --resume`, `--continue`, or the `/resume` picker keep the model they were using when the transcript was saved, regardless of the current `model` setting. This prevents another session's `/model` choice from changing the model on resume. If that model has been retired, the session falls through to the normal precedence order.

When the active model at startup comes from project or managed settings rather than your own selection, the startup header shows which settings file set it. Run `/model` to override (the project or managed setting reapplies on the next launch).

```json
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Add a custom model option

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` to add a single custom entry to the `/model` picker without replacing the built-in aliases — useful for testing model IDs that Claude Code does not list by default. The optional `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` and `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` control its display (defaulting to the model ID and `Custom model (<model-id>)`). The custom entry appears at the bottom of the picker, and Claude Code skips validation for its model ID so you can use any string your API endpoint accepts.

## Checking your current model

You can see which model you're currently using in two ways:

1. In the status line, if configured.
2. In `/status`, which also displays your account information.

**Source**: https://code.claude.com/docs/en/model-config
**Last Updated**: 2026-06-13
**Status**: Active
