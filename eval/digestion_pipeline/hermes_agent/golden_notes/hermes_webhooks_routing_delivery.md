---
tags:
  - resource
  - documentation
  - hermes_agent
  - webhooks
  - messaging
keywords:
  - webhook adapter setup
  - github pr review webhook
  - gitlab merge request webhook
  - direct delivery deliver_only
  - dynamic webhook subscriptions
  - webhook environment variables
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
access_control_group: ["general"]
---

# Hermes Agent — Webhooks: Routing & Delivery

## Overview

This is the **operating procedure** for the Hermes webhook adapter: how to enable it, point external services (GitHub, GitLab, JIRA, Stripe, monitoring tools) at it, and route their events into agent runs or direct deliveries. The adapter runs an HTTP server (default port `8644`) that accepts POST requests at `http://your-server:8644/webhooks/<route-name>`, validates HMAC signatures, transforms payloads into agent prompts, and routes responses back to the source or to another connected platform.

This note covers the **how-to**: the `hermes gateway setup` wizard / `WEBHOOK_*` env enablement and `/health` verification, the step-by-step GitHub-PR-review and GitLab-merge-request walkthroughs, `deliver_only` direct-delivery mode (zero-LLM push), the `hermes webhook subscribe/list/remove/test` dynamic-subscription CLI hot-reloaded from `webhook_subscriptions.json`, the response-code semantics, and troubleshooting. The **route + security data model** that these procedures configure — route properties, the cross-platform delivery target matrix, HMAC validation, rate limiting, idempotency, body-size limits, and prompt-injection guidance — is documented separately in [hermes_webhooks_routes_security](hermes_webhooks_routes_security.md); this note links out to it rather than duplicating it.

## Quick Start

1. Enable via `hermes gateway setup` or environment variables
2. Define routes in `config.yaml` **or** create them dynamically with `hermes webhook subscribe`
3. Point your service at `http://your-server:8644/webhooks/<route-name>`

## Setup

There are two ways to enable the webhook adapter. **Via the setup wizard**, run `hermes gateway setup` and follow the prompts to enable webhooks, set the port, and set a global HMAC secret. **Via environment variables**, add the following to `~/.hermes/.env`:

```bash
# Option A — wizard: hermes gateway setup  (follow the prompts)
# Option B — ~/.hermes/.env:
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644        # default
WEBHOOK_SECRET=your-global-secret
```

### Verify the server

Once the gateway is running, confirm the HTTP server is listening with `curl http://localhost:8644/health`. The expected response is `{"status": "ok", "platform": "webhook"}`.

## GitHub PR Review (Step by Step)

This walkthrough sets up automatic code review on every pull request.

1. **Create the webhook in GitHub** — Repository → **Settings** → **Webhooks** → **Add webhook**. Set **Payload URL** to `http://your-server:8644/webhooks/github-pr`, **Content type** to `application/json`, and **Secret** to match your route config (e.g. `github-webhook-secret`). Under **Which events?**, choose **Let me select individual events** and check **Pull requests**, then **Add webhook**.
2. **Add the route config** — add the `github-pr` route (with `events: ["pull_request"]`, the `{pull_request.*}` prompt template, `skills: ["github-code-review"]`, and `deliver: "github_comment"`) to `~/.hermes/config.yaml`. The route schema is defined in [hermes_webhooks_routes_security](hermes_webhooks_routes_security.md).
3. **Ensure `gh` CLI is authenticated** — the `github_comment` delivery type uses the GitHub CLI to post comments:

```bash
gh auth login
```

4. **Test it** — open a pull request on the repository. The webhook fires, Hermes processes the event, and posts a review comment on the PR.

## GitLab Webhook Setup

GitLab webhooks work similarly but use a different authentication mechanism: GitLab sends the secret as a plain `X-Gitlab-Token` header (exact string match, **not** HMAC).

1. **Create the webhook in GitLab** — Project → **Settings** → **Webhooks**. Set the **URL** to `http://your-server:8644/webhooks/gitlab-mr`, enter your **Secret token**, select **Merge request events** (plus any others you want), and **Add webhook**.
2. **Add the route config** — the GitLab route reads `object_attributes.*` fields from the merge-request payload:

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      routes:
        gitlab-mr:
          events: ["merge_request"]
          secret: "your-gitlab-secret-token"
          prompt: |
            Review this merge request:
            Project: {project.path_with_namespace}
            MR !{object_attributes.iid}: {object_attributes.title}
            Author: {object_attributes.last_commit.author.name}
            URL: {object_attributes.url}
            Action: {object_attributes.action}
          deliver: "log"
```

## Direct Delivery Mode

By default, every webhook POST triggers an agent run — the payload becomes a prompt, the agent processes it, and the agent's response is delivered, costing LLM tokens on every event. For use cases where you just want to **push a plain notification** — no reasoning, no agent loop — set `deliver_only: true` on the route. The rendered `prompt` template becomes the literal message body and the adapter dispatches it directly to the configured delivery target.

**When to use direct delivery:**

- **External service push** — a Supabase/Firebase webhook fires on a database change → notify a user in Telegram instantly
- **Monitoring alerts** — a Datadog/Grafana alert webhook → push to a Discord channel
- **Inter-agent pings** — Agent A notifies Agent B's user that a long-running task finished
- **Background job completion** — a cron job finishes → post the result to Slack

**Benefits:** zero LLM tokens (the agent is never invoked); sub-second delivery (a single adapter call); the same security as agent mode (HMAC auth, rate limits, idempotency, and body-size limits all still apply); and a synchronous response — the POST returns `200 OK` once delivery succeeds, or `502` if the target rejects it, so the upstream service can retry intelligently.

The same `deliver_only` route can be created statically in `config.yaml` or on the fly via the CLI:

```bash
hermes webhook subscribe antenna-matches \
  --deliver telegram \
  --deliver-chat-id "123456789" \
  --deliver-only \
  --prompt "🎉 New match: {match.user_name} matched with you!" \
  --description "Antenna match notifications"
```

### Response codes

The webhook endpoint returns standard HTTP status codes:

| Status | Meaning |
|--------|---------|
| `200 OK` | Delivered successfully. Body: `{"status": "delivered", "route": "...", "target": "...", "delivery_id": "..."}` |
| `200 OK` (status=duplicate) | Duplicate `X-GitHub-Delivery` ID within the idempotency TTL (1 hour). Not re-delivered. |
| `401 Unauthorized` | HMAC signature invalid or missing. |
| `400 Bad Request` | Malformed JSON body. |
| `404 Not Found` | Unknown route name. |
| `413 Payload Too Large` | Body exceeded `max_body_bytes`. |
| `429 Too Many Requests` | Route rate limit exceeded. |
| `502 Bad Gateway` | Target adapter rejected the message or raised. The error is logged server-side; the response body is a generic `Delivery failed` to avoid leaking adapter internals. |

### Configuration gotchas

- `deliver_only: true` requires `deliver` to be a real target. `deliver: log` (or omitting `deliver`) is rejected at startup — the adapter refuses to start if it finds a misconfigured route.
- The `skills` field is ignored in direct delivery mode (no agent runs, so there is nothing to inject skills into).
- Template rendering uses the same `{dot.notation}` syntax as agent mode, including the `{__raw__}` token (see [hermes_webhooks_routes_security](hermes_webhooks_routes_security.md)).
- Idempotency uses the same `X-GitHub-Delivery` / `X-Request-ID` header — retries with the same ID return `status=duplicate` and do NOT re-deliver.

## Dynamic Subscriptions (CLI)

In addition to static routes in `config.yaml`, you can create webhook subscriptions dynamically using the `hermes webhook` CLI command. This is especially useful when the agent itself needs to set up event-driven triggers.

```bash
# Create a subscription (returns the webhook URL + an auto-generated HMAC secret)
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New issue #{issue.number}: {issue.title}\nBy: {issue.user.login}\n\n{issue.body}" \
  --deliver telegram \
  --deliver-chat-id "-100123456789" \
  --description "Triage new GitHub issues"

hermes webhook list                 # list subscriptions
hermes webhook remove github-issues # remove a subscription
hermes webhook test github-issues   # test against a stored or supplied payload
hermes webhook test github-issues --payload '{"issue": {"number": 42, "title": "Test"}}'
```

**How dynamic subscriptions work:**

- Subscriptions are stored in `~/.hermes/webhook_subscriptions.json`.
- The webhook adapter hot-reloads this file on each incoming request (mtime-gated, negligible overhead) — no gateway restart required; subscribe and it is immediately live.
- Static routes from `config.yaml` always take precedence over dynamic ones with the same name.
- Dynamic subscriptions use the same route format and capabilities as static routes (events, prompt templates, skills, delivery).

**Agent-driven subscriptions:** the agent can create subscriptions via the terminal tool when guided by the `webhook-subscriptions` skill. Ask the agent to "set up a webhook for GitHub issues" and it will run the appropriate `hermes webhook subscribe` command.

## Troubleshooting

- **Webhook not arriving** — verify the port is exposed and accessible from the webhook source; check firewall rules (port `8644` or your configured port must be open); verify the URL path matches `http://your-server:8644/webhooks/<route-name>`; use the `/health` endpoint to confirm the server is running.
- **Signature validation failing** — ensure the route-config secret exactly matches the secret in the webhook source; for GitHub the secret is HMAC-based (check `X-Hub-Signature-256`); for GitLab it is a plain token match (check `X-Gitlab-Token`); check gateway logs for `Invalid signature` warnings.
- **Event being ignored** — check that the event type is in the route's `events` list. GitHub uses values like `pull_request`, `push`, `issues` (the `X-GitHub-Event` header); GitLab uses `merge_request`, `push` (the `X-GitLab-Event` header). If `events` is empty or unset, all events are accepted.
- **Agent not responding** — run the gateway in foreground to see logs (`hermes gateway run`); check that the prompt template renders correctly; verify the delivery target is configured and connected.
- **Duplicate responses** — the idempotency cache should prevent this; check that the source is sending a delivery-ID header (`X-GitHub-Delivery` or `X-Request-ID`). Delivery IDs are cached for 1 hour.
- **`gh` CLI errors (GitHub comment delivery)** — run `gh auth login` on the gateway host; ensure the authenticated user has write access to the repo; check that `gh` is installed and on the PATH.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WEBHOOK_ENABLED` | Enable the webhook platform adapter | `false` |
| `WEBHOOK_PORT` | HTTP server port for receiving webhooks | `8644` |
| `WEBHOOK_SECRET` | Global HMAC secret (used as fallback when routes don't specify their own) | _(none)_ |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/webhooks.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
**Last Updated**: 2026-06-19
**Status**: Active
