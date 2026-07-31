---
tags:
  - resource
  - documentation
  - hermes_agent
  - webhooks
  - security
keywords:
  - webhook route model
  - platforms.webhook.extra.routes
  - dot-notation prompt template
  - cross-platform delivery matrix
  - HMAC signature validation
  - rate limiting idempotency
  - body size limit
  - prompt injection risk
topics:
  - Hermes Agent
  - Webhooks
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
access_control_group: ["general"]
---

# Hermes Agent — Webhook Routes & Security Model

## Overview

This note is the **data model** behind Hermes' webhook adapter: how a webhook source maps to an agent run (or a direct push), and how that mapping is secured. The adapter runs an HTTP server that accepts POST requests, validates HMAC signatures, transforms payloads into agent prompts, and routes responses back to the source or to another configured platform. A **route** is the unit of that mapping — a named entry under `platforms.webhook.extra.routes` in `config.yaml` that declares which `events` it accepts, the `secret` that authenticates them, the `prompt` template applied to the payload, optional `skills` to load, and where to `deliver` the result.

Three things are modeled here: (1) the **route properties** that define a single source→agent→delivery binding; (2) the **delivery target matrix** — the set of platforms a response can be routed to (cross-platform delivery); and (3) the **security layers** — per-source HMAC validation, the required-secret rule, fixed-window rate limiting, idempotency, body-size limits, and the prompt-injection threat that webhook payloads carry. The operating procedure that *exercises* this model — setup wizard, GitHub/GitLab walkthroughs, `deliver_only` direct delivery, and `hermes webhook subscribe` dynamic subscriptions — lives in the sibling note [hermes_webhooks_routing_delivery](hermes_webhooks_routing_delivery.md); this note defines the shape those procedures fill in.

## Configuring Routes

Routes define how different webhook sources are handled. Each route is a named entry under `platforms.webhook.extra.routes` in `config.yaml`.

### Route properties

| Property | Required | Description |
|----------|----------|-------------|
| `events` | No | List of event types to accept (e.g. `["pull_request"]`). If empty, all events are accepted. Event type is read from `X-GitHub-Event`, `X-GitLab-Event`, or `event_type` in the payload. |
| `secret` | **Yes** | HMAC secret for signature validation. Falls back to the global `secret` if not set on the route. Set to `"INSECURE_NO_AUTH"` for testing only (skips validation). |
| `prompt` | No | Template string with dot-notation payload access (e.g. `{pull_request.title}`). If omitted, the full JSON payload is dumped into the prompt. |
| `skills` | No | List of skill names to load for the agent run. |
| `deliver` | No | Where to send the response (see Delivery Options); `log` is the default. |
| `deliver_extra` | No | Additional delivery config — keys depend on `deliver` type (e.g. `repo`, `pr_number`, `chat_id`). Values support the same `{dot.notation}` templates as `prompt`. |
| `deliver_only` | No | If `true`, skip the agent entirely — the rendered `prompt` template becomes the literal message that gets delivered. Zero LLM cost, sub-second delivery. Requires `deliver` to be a real target (not `log`). |

### Full example

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
            Author: {pull_request.user.login}
            URL: {pull_request.html_url}
            Diff URL: {pull_request.diff_url}
            Action: {action}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
        deploy-notify:
          events: ["push"]
          secret: "deploy-secret"
          prompt: "New push to {repository.full_name} branch {ref}: {head_commit.message}"
          deliver: "telegram"
```

### Prompt templates and `{__raw__}`

Prompts use dot-notation to access nested fields in the webhook payload: `{pull_request.title}` resolves to `payload["pull_request"]["title"]`, `{repository.full_name}` resolves to `payload["repository"]["full_name"]`. Missing keys are left as the literal `{key}` string (no error). Nested dicts and lists are JSON-serialized and truncated at 2000 characters.

The special token `{__raw__}` dumps the **entire payload** as indented JSON (truncated at 4000 characters) — useful for monitoring alerts or generic webhooks where the agent needs full context. It can be mixed with regular template variables, and the same dot-notation templates also work in `deliver_extra` values:

```yaml
prompt: "PR #{pull_request.number} by {pull_request.user.login}: {__raw__}"
```

If no `prompt` template is configured for a route, the entire payload is dumped as indented JSON (truncated at 4000 characters).

### Forum-topic delivery

When delivering webhook responses to Telegram, you can target a specific forum topic by including `message_thread_id` (or `thread_id`) in `deliver_extra`:

```yaml
webhooks:
  routes:
    alerts:
      events: ["alert"]
      prompt: "Alert: {__raw__}"
      deliver: "telegram"
      deliver_extra:
        chat_id: "-1001234567890"
        message_thread_id: "42"
```

If `chat_id` is not provided in `deliver_extra`, the delivery falls back to the home channel configured for the target platform.

## Delivery Options

The `deliver` field controls where the agent's response goes after processing the webhook event. The target matrix below is the cross-platform delivery surface: a route can route its response to any of these targets (the target platform must also be enabled and connected in the gateway). If no `chat_id` is provided in `deliver_extra`, the response is sent to that platform's configured home channel.

| Deliver Type | Description |
|-------------|-------------|
| `log` | Logs the response to the gateway log output. This is the default and is useful for testing. |
| `github_comment` | Posts the response as a PR/issue comment via the `gh` CLI. Requires `deliver_extra.repo` and `deliver_extra.pr_number`. The `gh` CLI must be installed and authenticated on the gateway host (`gh auth login`). |
| `telegram` | Routes to Telegram. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `discord` | Routes to Discord. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `slack` | Routes to Slack. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `signal` | Routes to Signal. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `sms` | Routes to SMS via Twilio. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `whatsapp` | Routes to WhatsApp. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `matrix` | Routes to Matrix. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `mattermost` | Routes to Mattermost. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `homeassistant` | Routes to Home Assistant. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `email` | Routes to Email. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `dingtalk` | Routes to DingTalk. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `feishu` | Routes to Feishu/Lark. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `wecom` | Routes to WeCom. Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `weixin` | Routes to Weixin (WeChat). Uses the home channel, or specify `chat_id` in `deliver_extra`. |
| `bluebubbles` | Routes to BlueBubbles (iMessage). Uses the home channel, or specify `chat_id` in `deliver_extra`. |

The `deliver` property also accepts `qqbot` as a target (per the route-properties enumeration). For cross-platform delivery the target platform must be enabled and connected in the gateway.

## Security

The webhook adapter includes multiple layers of security that all apply equally to agent-mode runs and `deliver_only` direct delivery.

### HMAC signature validation

The adapter validates incoming webhook signatures using the appropriate method for each source:

- **GitHub**: `X-Hub-Signature-256` header — HMAC-SHA256 hex digest prefixed with `sha256=`
- **GitLab**: `X-Gitlab-Token` header — plain secret string match
- **Generic**: `X-Webhook-Signature` header — raw HMAC-SHA256 hex digest

If a secret is configured but no recognized signature header is present, the request is rejected.

### Secret is required

Every route must have a secret — either set directly on the route or inherited from the global `secret`. Routes without a secret cause the adapter to fail at startup with an error. For development/testing only, you can set the secret to `"INSECURE_NO_AUTH"` to skip validation entirely. `INSECURE_NO_AUTH` is only accepted when the gateway is bound to a loopback host (`127.0.0.1`, `localhost`, `::1`). If it is combined with a non-loopback bind such as `0.0.0.0` or a LAN IP, the adapter refuses to start — this prevents accidentally exposing an unauthenticated endpoint on a public interface.

### Rate limiting

Each route is rate-limited to **30 requests per minute** by default (fixed-window). Requests exceeding the limit receive a `429 Too Many Requests` response. Configure this globally:

```yaml
platforms:
  webhook:
    extra:
      rate_limit: 60  # requests per minute
```

### Idempotency

Delivery IDs (from `X-GitHub-Delivery`, `X-Request-ID`, or a timestamp fallback) are cached for **1 hour**. Duplicate deliveries (e.g. webhook retries) are silently skipped with a `200` response, preventing duplicate agent runs.

### Body size limits

Payloads exceeding **1 MB** are rejected before the body is read. Configure this via `platforms.webhook.extra.max_body_bytes` (e.g. `2097152` for 2 MB).

### Prompt injection risk

Webhook payloads contain attacker-controlled data — PR titles, commit messages, issue descriptions, etc. can all contain malicious instructions. Run the gateway in a sandboxed environment (Docker, VM) when exposed to the internet. Consider using the Docker or SSH terminal backend for isolation.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/webhooks.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
**Last Updated**: 2026-06-19
**Status**: Active
