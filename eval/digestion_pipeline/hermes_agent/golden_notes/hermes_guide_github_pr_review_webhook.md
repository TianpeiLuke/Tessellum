---
tags:
  - resource
  - documentation
  - hermes_agent
  - webhooks
  - automation
keywords:
  - github pr review webhook
  - platforms.webhook route
  - hmac signature verification
  - github_comment delivery
  - prompt injection sandbox
  - idempotency dedup cache
  - ngrok local testing
  - gitlab webhook support
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review
access_control_group: ["general"]
---

# Hermes Agent — GitHub PR Reviews via Webhook

## Overview

This is the **real-time, event-driven recipe** for an automated GitHub PR reviewer: when a pull request is opened or updated, GitHub sends a webhook `POST` to your Hermes instance, Hermes runs the agent against a templated prompt that fetches the diff via the `gh` CLI, and the agent's review is posted straight back to the PR thread — no manual prompting, no polling. It is the lower-latency counterpart to the cron-polling variant ([hermes_guide_github_pr_review_cron](hermes_guide_github_pr_review_cron.md)): the webhook reacts the instant a PR event fires, but it requires a publicly reachable URL, whereas the cron poller works behind NAT and firewalls.

The whole integration lives in a single `platforms.webhook` route in `~/.hermes/config.yaml` — `secret` (HMAC), `events` (header filter), a `prompt` template with `{field}` substitutions resolved from the GitHub payload, and `deliver: github_comment`. Because the webhook endpoint is exposed to the internet and PR titles/descriptions/commit messages are **attacker-controlled**, the source carries a standing prompt-injection warning: run the gateway in a sandboxed environment (Docker, VM, SSH backend). For the full webhook platform reference (all config options, delivery types, dynamic subscriptions, the complete security model) this guide links out to the dedicated Webhooks reference rather than duplicating it.

## Prerequisites

- Hermes Agent installed and the gateway running (`hermes gateway`).
- The [`gh` CLI](https://cli.github.com/) installed and authenticated on the gateway host (`gh auth login`) — the agent shells out to `gh pr diff` / `gh pr comment`.
- A publicly reachable URL for your Hermes instance (use ngrok for local testing — see below).
- Admin access to the GitHub repository (required to manage webhooks).

## Step 1 — Enable the webhook platform

Add a `platforms.webhook` block with one named route to `~/.hermes/config.yaml`. The crucial detail: **the payload does not contain the diff** — only PR metadata (title, description, branch names, URLs) — so the prompt instructs the agent to run `gh pr diff` to fetch the actual changes. The `terminal` tool ships in the default `hermes-webhook` toolset, so no extra config is needed for that.

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644          # default; change if another service occupies this port
      rate_limit: 30      # max requests per minute per route (not a global cap)

      routes:
        github-pr-review:
          secret: "your-webhook-secret-here"   # must match the GitHub webhook secret exactly
          events:
            - pull_request

          # {number} and {repository.full_name} are resolved from the GitHub payload.
          prompt: |
            A pull request event was received (action: {action}).

            PR #{number}: {pull_request.title}
            Author: {pull_request.user.login}
            Branch: {pull_request.head.ref} → {pull_request.base.ref}
            Description: {pull_request.body}
            URL: {pull_request.html_url}

            If the action is "closed" or "labeled", stop here and do not post a comment.

            Otherwise:
            1. Run: gh pr diff {number} --repo {repository.full_name}
            2. Review the code changes for correctness, security issues, and clarity.
            3. Write a concise, actionable review comment and post it.

          deliver: github_comment
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
```

Key fields, per the source: a route-level `secret` is the HMAC secret (falls back to the global `extra.secret` if omitted); `events` lists the `X-GitHub-Event` header values to accept (empty list = accept all); `prompt` is a template where `{field}` and `{nested.field}` resolve from the payload; `deliver: github_comment` posts via `gh pr comment` (vs `log`, which just writes to the gateway log); `deliver_extra.repo` and `deliver_extra.pr_number` resolve from the payload.

## Step 2 — Start the gateway

Start the gateway and confirm the webhook listener is up:

```bash
hermes gateway
# [webhook] Listening on 0.0.0.0:8644 — routes: github-pr-review

curl http://localhost:8644/health
# {"status": "ok", "platform": "webhook"}
```

## Step 3 — Register the webhook on GitHub

In the repository, go to **Settings → Webhooks → Add webhook** and set: **Payload URL** = `https://your-public-url.example.com/webhooks/github-pr-review`; **Content type** = `application/json`; **Secret** = the same value as the route's `secret`; **Which events?** → select individual events and check **Pull requests**. GitHub immediately sends a `ping` event to confirm the connection — it is safely ignored (not in your `events` list), returns `{"status": "ignored", "event": "ping"}`, and is only logged at DEBUG level so it won't appear at the default log level.

## Step 4 — Open a test PR

Create a branch, push a change, and open a PR. Within 30–90 seconds (depending on PR size and model), Hermes posts a review comment. Follow the agent's progress in real time with `tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"`.

## Local testing with ngrok

If Hermes runs on your laptop, expose it with [ngrok](https://ngrok.com/) (`ngrok http 8644`) and use the `https://...ngrok-free.app` URL as the GitHub Payload URL. On the free tier the URL changes each restart, so update the GitHub webhook every session; paid accounts get a static domain. You can smoke-test a static route directly with `curl` — no GitHub account or real PR needed. While testing, switch `deliver: github_comment` to `deliver: log` so the agent doesn't try to comment on the fake `org/repo#99` repo in the test payload (switch back once satisfied).

```bash
SECRET="your-webhook-secret-here"
BODY='{"action":"opened","number":99,"pull_request":{"title":"Test PR","body":"Adds a feature.","user":{"login":"testuser"},"head":{"ref":"feat/x"},"base":{"ref":"main"},"html_url":"https://github.com/org/repo/pull/99"},"repository":{"full_name":"org/repo"}}'
SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$SECRET" -hex | awk '{print "sha256="$2}')

curl -s -X POST http://localhost:8644/webhooks/github-pr-review \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -H "X-Hub-Signature-256: $SIG" \
  -d "$BODY"
# Expected: {"status":"accepted","route":"github-pr-review","event":"pull_request","delivery_id":"..."}
```

Note that `hermes webhook test <name>` works only for **dynamic subscriptions** created with `hermes webhook subscribe` — it does not read routes from `config.yaml`.

## Filtering to specific actions

GitHub sends `pull_request` events for many actions (`opened`, `synchronize`, `reopened`, `closed`, `labeled`, …). The crucial caveat: the `events` list filters **only by the `X-GitHub-Event` header value** — it cannot filter by action sub-type at the routing level. The Step 1 prompt handles this by instructing the agent to stop early for `closed`/`labeled`, but **the agent still runs to completion (and consumes tokens) for every `pull_request` event regardless of action**. For high-volume repos, accept that cost or filter upstream with a GitHub Actions workflow that calls your webhook URL conditionally. There is also no Jinja2 or conditional template syntax — `{field}` and `{nested.field}` are the only substitutions; anything else is passed verbatim to the agent.

## Using a skill for consistent review style

Load a Hermes skill to give the agent a consistent review persona by adding `skills` to the route. Only the **first matching skill found is loaded** — Hermes does not stack multiple skills; subsequent entries are ignored.

```yaml
# Inside platforms.webhook.extra.routes.github-pr-review:
          skills:
            - review
```

## Sending responses to Slack or Discord instead

Replace the `deliver`/`deliver_extra` fields in the route with the target platform (which must also be enabled and connected in the gateway). For `deliver: slack` set `deliver_extra.chat_id` to the Slack channel ID; for `deliver: discord` set the Discord channel ID. Omitting `chat_id` sends to that platform's configured home channel. Valid `deliver` values: `log` · `github_comment` · `telegram` · `discord` · `slack` · `signal` · `sms`.

## GitLab support

The same adapter works with GitLab. GitLab authenticates with `X-Gitlab-Token` (plain string match, not HMAC) — Hermes handles both automatically. For event filtering, GitLab sets `X-GitLab-Event` to values like `Merge Request Hook`, `Push Hook`, `Pipeline Hook`; use the exact header value in `events`. GitLab payload fields differ from GitHub's (e.g. `{object_attributes.title}` for the MR title, `{object_attributes.iid}` for the MR number). To discover the payload structure, use GitLab's **Test** button plus the **Recent Deliveries** log, or omit `prompt` so Hermes passes the full payload as formatted JSON directly to the agent.

## Security notes

The source's standing rules for an internet-exposed endpoint: **never use `INSECURE_NO_AUTH` in production** (it disables signature validation entirely; local development only); **rotate the webhook secret periodically** and update it in both GitHub and `config.yaml`; **rate limiting** is 30 req/min per route by default (configurable via `extra.rate_limit`, `429` on exceed); **duplicate deliveries** (webhook retries) are deduplicated via a 1-hour idempotency cache keyed on `X-GitHub-Delivery`, then `X-Request-ID`, then a millisecond timestamp — when neither delivery-ID header is set, retries are **not** deduplicated; and **prompt injection** — PR titles, descriptions, and commit messages are attacker-controlled, so run the gateway in a sandboxed environment (Docker, VM) when exposed to the public internet.

## Troubleshooting & full config reference

By symptom: `401 Invalid signature` → config secret doesn't match the GitHub webhook secret; `404 Unknown route` → URL route name doesn't match the `routes:` key; `429 Rate limit exceeded` → 30 req/min per route exceeded (common when re-delivering test events from GitHub's UI); no comment posted → `gh` not installed/on PATH/authenticated; agent runs but no comment → check the gateway log; port already in use → change `extra.port`; agent reviews only the PR description → the prompt isn't including the `gh pr diff` instruction (the diff is not in the payload). **GitHub's Recent Deliveries tab** (repo → Settings → Webhooks → your webhook) shows the exact headers, payload, HTTP status, and response body for every delivery — the fastest way to diagnose failures without touching server logs. The full route reference:

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: "0.0.0.0"         # bind address (default: 0.0.0.0)
      port: 8644               # listen port (default: 8644)
      secret: ""               # optional global fallback secret
      rate_limit: 30           # requests per minute per route
      max_body_bytes: 1048576  # payload size limit in bytes (default: 1 MB)

      routes:
        <route-name>:
          secret: "required-per-route"
          events: []            # [] = accept all; otherwise list X-GitHub-Event values
          prompt: ""            # {field} / {nested.field} resolved from payload
          skills: []            # first matching skill is loaded (only one)
          deliver: "log"        # log | github_comment | telegram | discord | slack | signal | sms
          deliver_extra: {}     # repo + pr_number for github_comment; chat_id for others
```

**Source**: `inbox/hermes_agent_docs/guides/webhook-github-pr-review.md` · https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review
**Last Updated**: 2026-06-19
**Status**: Active
