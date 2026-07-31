---
tags:
  - resource
  - documentation
  - claude_code
  - model_config
  - fallback
keywords:
  - fallback model chains
  - automatic model fallback
  - opusplan
  - fallbackmodel setting
  - fable 5 safety classifier
  - content-based fallback
  - availability-based fallback
  - plan execute hybrid
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

# Claude Code — Model Fallback (Chains, Automatic Fallback, opusplan)

## Overview

Claude Code provides **two distinct fallback systems** plus one **plan-to-execute hybrid alias**, and the model-config docs are careful to keep them separate. **Fallback model chains** are *availability-based*: when the primary model is overloaded or unavailable, Claude Code switches to a configured backup for the current turn only. **Automatic model fallback** is *content-based*: when Fable 5's safety classifiers flag a request (most often cybersecurity or biology), Claude Code re-runs that request on the default Opus model. The **`opusplan`** alias is neither — it is an automated hybrid that uses `opus` reasoning in plan mode and `sonnet` for execution. This note covers all three; effort/thinking controls are in `cc_effort_level_and_thinking`, model aliases and the four ways to set a model are in `cc_model_selection`, and the `availableModels` allowlist that governs which fallback elements survive is in `cc_restrict_model_selection`.

## The `opusplan` model setting

The `opusplan` model alias provides an automated hybrid approach:

- **In plan mode** — uses `opus` for complex reasoning and architecture decisions.
- **In execution mode** — automatically switches to `sonnet` for code generation and implementation.

This gives the best of both worlds: Opus's superior reasoning for planning, and Sonnet's efficiency for execution.

The plan-mode Opus phase uses the same context window as the `opus` model setting. On subscription tiers where Opus is automatically upgraded to 1M context (see `cc_extended_context_1m`), `opusplan` receives the upgrade in plan mode as well. To force 1M context for both phases when you are not on an auto-upgrade tier, set the model to `opusplan[1m]`.

When `availableModels` excludes Opus (see `cc_restrict_model_selection`), `opusplan` stays on Sonnet in plan mode instead of switching. The same applies to the implicit Haiku-to-Sonnet plan-mode upgrade when Sonnet is excluded.

For a hybrid approach where Claude decides mid-task when to consult a second model rather than switching at the plan boundary, the docs point to the [advisor tool](https://code.claude.com/docs/en/advisor).

## Fallback model chains (availability-based)

When the primary model is overloaded, unavailable, or returns another non-retryable server error, Claude Code can switch to a fallback model instead of failing the request. Authentication, billing, rate-limit, request-size, and transport errors **never** trigger a switch; those follow their normal retry and error handling.

Configure one or more fallback models and Claude Code tries them in order, showing a notice when it switches. The switch lasts for the **current turn only**, so the next message tries the primary model first again. Chains are **capped at three models** after duplicate removal, and extra entries are ignored.

Set a chain for one session with the `--fallback-model` flag, which accepts a comma-separated list:

```bash theme={null}
claude --fallback-model sonnet,haiku
```

To persist a chain across sessions, set `fallbackModel` in settings as an array. The `--fallback-model` flag takes precedence over the `fallbackModel` setting. Each element accepts a model name or alias, and `"default"` expands to the default model.

Two cases cause an element to be **skipped**:

- **Unavailable model** — a model that can't be reached, such as a retired model pinned in settings, is skipped and Claude Code continues to the next element.
- **Outside the allowlist** — an element not permitted by `availableModels` (see `cc_restrict_model_selection`) is dropped when the chain is read and never tried.

## Automatic model fallback (content-based)

This system covers **content-based** fallback from Fable 5; it is distinct from the availability-based chains above. Fable 5 runs with safety classifiers for cybersecurity and biology content. When a classifier flags a request, Claude Code re-runs that request on the **default Opus model** and shows a notice in the transcript: Opus 4.8 on the Anthropic API and LLM gateway deployments, or Opus 4.7 on Claude Platform on AWS. The session then continues on that Opus model. To return to Fable 5, run `/model fable`.

### Check what triggered fallback

Fallback can trigger on the **first request** of a session, before you send anything unusual, because the first request carries workspace context such as your CLAUDE.md content and git status. A repository that contains security or biology material can trip the classifier on that context alone.

To check whether customizations are the trigger, start a session with `claude --safe-mode`, which disables customizations such as CLAUDE.md, skills, MCP servers, and hooks. Git status and directory names are not customizations and are still included.

### Ask before switching

To decide what happens each time a request is flagged, rather than switching automatically, run `/config` and turn off "switch models when a message is flagged". A flagged request then pauses the session with two options: switch to the Opus model, or edit the prompt and retry on Fable 5. Some cases behave differently:

- If both models flag the same request, you can edit the prompt and retry, or start a new session.
- On mobile Claude Code on the web sessions, editing and retrying is not supported. Switch models, or continue from a desktop browser or the desktop app.
- In non-interactive mode and SDK integrations that can't show the prompt, a flagged request ends the turn with a refusal instead.

### Enable fallback on Bedrock, Vertex AI, and Foundry

On Amazon Bedrock, Google Vertex AI, and Microsoft Foundry, model IDs are provider-specific, so automatic fallback only operates when Claude Code can identify **both** models involved:

- Claude Code must recognize the current model as Fable 5: the model ID contains `claude-fable-5`, matches the value of `ANTHROPIC_DEFAULT_FABLE_MODEL`, or is mapped with `modelOverrides`.
- The fallback target must resolve to an Opus model: the value of `ANTHROPIC_DEFAULT_OPUS_MODEL` if set, otherwise an Opus 4.8 entry in the provider's model list.

If either model can't be identified, Claude Code does not switch automatically — the flagged request ends with a refusal, and you can switch models with `/model` and retry. To enable automatic fallback on these providers, set `ANTHROPIC_DEFAULT_FABLE_MODEL` to your Fable 5 model ID and `ANTHROPIC_DEFAULT_OPUS_MODEL` to your Opus 4.8 model ID.

### Security research and biology workloads

Workloads in offensive security or biology — including penetration testing, Capture the Flag (CTF) exercises, and biology-adjacent codebases — trigger fallback frequently, often on the first request. For substantive biology work, expect nearly all requests to reroute. This is expected routing for these domains, not an account flag. If your organization needs Fable-class capability for this work, the docs say to ask your Anthropic account team about trusted access programs.

**Source**: https://code.claude.com/docs/en/model-config
**Last Updated**: 2026-06-13
**Status**: Active
