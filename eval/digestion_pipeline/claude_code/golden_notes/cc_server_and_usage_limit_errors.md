---
tags:
  - resource
  - documentation
  - claude_code
  - errors
  - usage_limits
keywords:
  - server errors
  - usage limits
  - automatic retries
  - exponential backoff
  - 529 overloaded
  - session limit
  - request rejected 429
  - auto mode safety classifier
topics:
  - Claude Code
  - Error Reference
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/errors
access_control_group: ["general"]
---

# Claude Code — Server and Usage Limit Errors

## Overview

Claude Code calls the Claude API for model responses, so most runtime errors map to an underlying API error code. This note covers two of the error families that the [error reference](https://code.claude.com/docs/en/errors) groups together: **server errors** that come from the inference provider (Anthropic infrastructure, or Bedrock / Vertex AI / Foundry / a custom gateway), and **usage limits** that come from a quota tied to your account or plan. The two families are deliberately distinguished — server errors affect everyone, while usage limits are specific to your account.

Both families are preceded by the same **automatic retry model**: Claude Code retries transient failures with exponential backoff before it ever shows you an error, so every message documented here appears only after those retries are exhausted. (Authentication and network errors are in [cc_authentication_and_network_errors](cc_authentication_and_network_errors.md); request-content and response-quality errors are in [cc_request_and_quality_errors](cc_request_and_quality_errors.md).)

## Automatic retries

Claude Code retries transient failures before showing you an error. Server errors, overloaded responses, request timeouts, temporary 429 throttles, and dropped connections are all retried up to 10 times with exponential backoff. While retrying, the spinner shows a `Retrying in Ns · attempt x/y` countdown.

When you see one of the errors on this page, those retries have already been exhausted. You can tune the behavior with two environment variables:

| Variable | Default | Effect |
| :--- | :--- | :--- |
| `CLAUDE_CODE_MAX_RETRIES` | 10 | Number of retry attempts. Lower it to surface failures faster in scripts; raise it to wait through longer incidents. |
| `API_TIMEOUT_MS` | 600000 | Per-request timeout in milliseconds. Raise it for slow networks or proxies. |

(These environment variables are documented in full in the [env vars reference](https://code.claude.com/docs/en/env-vars).)

## Server errors

These errors come from the inference provider rather than your account or request. On the Anthropic API that means Anthropic infrastructure. On Bedrock, Vertex AI, Foundry, or a custom gateway it means that provider's infrastructure. The trailing sentence in each message names where to check service health and varies by provider; a custom `ANTHROPIC_BASE_URL` names the gateway host.

### API Error: 500 Internal server error

Claude Code shows the status code and the API's error message for any 5xx response. This indicates an unexpected failure inside the API — it is **not** caused by your prompt, settings, or account.

```text theme={null}
API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
```

**What to do:** check [status.claude.com](https://status.claude.com) (or the provider status page named in the message) for active incidents; wait a minute and resend (your original message is still in the conversation, so for a long prompt you can type `try again` instead of pasting it again); if it persists with no posted incident, run `/feedback` so Anthropic can investigate.

### API Error: Repeated 529 Overloaded errors

The API is temporarily at capacity across all users. Claude Code has already retried several times before showing this message. A 529 is **not** your usage limit and does not count against your quota.

```text theme={null}
API Error: Repeated 529 Overloaded errors. The API is at capacity — this is usually temporary. Try again in a moment. If it persists, check https://status.claude.com.
```

**What to do:** check status; try again in a few minutes; run `/model` and switch to a different model to keep working, since capacity is tracked per model. Claude Code prompts you to do this when one model is under particularly high load, for example `Opus is experiencing high load, please use /model to switch to Sonnet`.

### Request timed out

The API did not respond before the connection deadline, shown as `Request timed out`. This can happen during periods of high load or when a very large response is being generated. The default request timeout is 10 minutes.

**What to do:** retry the request; for long-running tasks, break the work into smaller prompts; if a slow network or proxy is the cause, raise `API_TIMEOUT_MS` as described under [Automatic retries](#automatic-retries); if timeouts are frequent and your network is otherwise healthy, see [cc_authentication_and_network_errors](cc_authentication_and_network_errors.md).

### Auto mode cannot determine the safety of an action

The model that [auto mode](https://code.claude.com/docs/en/permission-modes) uses to classify actions could not produce a decision, so auto mode did not approve the action automatically. Reads, searches, and edits inside your working directory skip the classifier, so they keep working in all of these cases. The message you see depends on why the classifier failed:

- **Classifier model overloaded** — `<model> is temporarily unavailable, so auto mode cannot determine the safety of <tool> right now. Wait briefly and then try this action again.` Retry after a few seconds (Claude sees the same message and usually retries on its own); this is transient and unrelated to auto-mode eligibility, so you do not need to change settings.
- **Classifier returned an unparseable response** — `Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details`. Retry the action (usually succeeds next attempt); run `claude --debug` and repeat to see the underlying classifier response in the debug log.
- **Conversation larger than the classifier's context window** — `Auto mode classifier transcript exceeded context window — falling back to manual approval (try /compact to reduce conversation size)`. In an interactive session, auto mode falls back to a normal permission prompt for that action; in [non-interactive mode](https://code.claude.com/docs/en/headless) the run aborts because the transcript only grows and retrying cannot succeed. Approve or deny the prompt, then run `/compact` so subsequent actions fit within the classifier window again.

## Usage limits

These errors mean a quota tied to your account or plan has been reached. They are distinct from [server errors](#server-errors), which affect everyone.

### You've hit your session limit

Subscription plans include a rolling usage allowance. When it runs out, Claude Code blocks further requests until the reset time shown in the message:

```text theme={null}
You've hit your session limit · resets 3:45pm
You've hit your weekly limit · resets Mon 12:00am
You've hit your Opus limit · resets 3:45pm
```

**What to do:** wait for the reset time; run `/usage` to see your plan limits and reset times; run `/usage-credits` to buy additional usage on Pro and Max (or request it from your admin on Team and Enterprise); to upgrade your plan for higher base limits, see [claude.com/pricing](https://claude.com/pricing). To watch your remaining allowance before you hit the limit, add the `rate_limits` fields to a custom status line, or in the Desktop app click the usage ring next to the model picker.

### Usage credits required for 1M context

The selected model uses the 1M-token extended context window, and your plan only includes it through usage credits. This is an **entitlement check, not a quota exhaustion** — it fires even when your session and weekly allowances have capacity remaining.

```text theme={null}
API Error: Usage credits required for 1M context · run /usage-credits to turn them on, or /model to switch to standard context
```

When this error appears mid-conversation because the context grew past 200K tokens, Claude Code (v2.1.172+) automatically compacts the conversation back under the standard context limit and keeps the session at that limit afterward, so no action is needed. On versions before v2.1.172, the error repeated on every subsequent request including `/compact`; run `/clear` on those versions to recover. **What to do** when you explicitly selected a `[1m]` model: run `/model` and select the variant without the `[1m]` suffix; run `/usage-credits` to turn on metered billing for the 1M variant; if the error persists after `/model`, a 1M model ID may be set elsewhere (see [There's an issue with the selected model](cc_request_and_quality_errors.md)); to remove 1M variants from the model picker entirely, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`.

### Server is temporarily limiting requests

The API applied a short-lived throttle that is **unrelated to your plan quota**, shown as `API Error: Server is temporarily limiting requests (not your usage limit)`. This is [retried automatically](#automatic-retries) before being shown.

**What to do:** wait briefly and try again; check [status.claude.com](https://status.claude.com) if it persists.

### Request rejected (429)

You have hit the rate limit configured for your API key, Amazon Bedrock project, or Google Vertex AI project. The trailing sentence names where to check service health and varies by provider.

```text theme={null}
API Error: Request rejected (429) · this may be a temporary capacity issue. If it persists, check https://status.claude.com.
```

**What to do:** run `/status` and confirm the active credential is the one you expect (a stray `ANTHROPIC_API_KEY` in your environment can route requests through a low-tier key instead of your subscription); check your provider console for active limits and request a higher tier if needed; for Anthropic API keys, see the rate limits reference for how tiers work; reduce concurrency by lowering `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`, avoiding many parallel subagents, or switching to a smaller model with `/model` for high-volume scripted runs.

### Credit balance is too low

Your Console organization has run out of prepaid credits.

```text theme={null}
Credit balance is too low
```

**What to do:** add credits at [platform.claude.com/settings/billing](https://platform.claude.com/settings/billing) (and consider enabling auto-reload so the balance refills before it hits zero); switch to subscription authentication with `/login` if you have a Pro, Max, Team, or Enterprise plan; set per-workspace spend caps in the Console to prevent a single project from draining the org balance.

**Source**: https://code.claude.com/docs/en/errors
**Last Updated**: 2026-06-13
**Status**: Active
