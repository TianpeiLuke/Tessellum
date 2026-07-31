---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - google_chat
keywords:
  - hermes google chat bot setup
  - cloud pub sub pull subscription
  - chat rest api outbound
  - service account json iam
  - per user oauth attachment delivery
  - google_chat_allowed_users allowlist
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/google_chat
access_control_group: ["general"]
---

# Hermes Messaging — Google Chat Setup

## Overview

This is the platform-setup procedure for connecting Hermes Agent to **Google Chat** as a bot. The integration uses **Cloud Pub/Sub pull subscriptions** for inbound events and the **Chat REST API** (`chat.googleapis.com`) for outbound messages. It has the same ergonomics as Slack Socket Mode or Telegram long-polling: the Hermes process does **not** need a public URL, a tunnel, or a TLS certificate — it connects, authenticates, and listens on a subscription the same way a Telegram bot listens on a token.

Google Chat is part of Google Workspace. The integration works with a personal Workspace (`@yourdomain.com` registered through Google) or a work Workspace where you have Admin rights to publish an app; Gmail-only accounts cannot host Chat apps. Authentication is a **Service Account JSON** with `roles/pubsub.subscriber` on the subscription, and users are identified by Chat resource names (`users/{id}`) plus email. Running `hermes gateway setup` and picking **Google Chat** gives a guided walk-through.

| Component | Value |
|-----------|-------|
| **Libraries** | `google-cloud-pubsub`, `google-api-python-client`, `google-auth` |
| **Inbound transport** | Cloud Pub/Sub pull subscription (no public endpoint) |
| **Outbound transport** | Chat REST API (`chat.googleapis.com`) |
| **Authentication** | Service Account JSON with `roles/pubsub.subscriber` on the subscription |
| **User identification** | Chat resource names (`users/{id}`) + email |

## Steps 1–8: GCP project, APIs, Service Account, Pub/Sub, IAM, app config, install

1. **Create or pick a GCP project** to host the Pub/Sub topic ([console.cloud.google.com](https://console.cloud.google.com)). Note the project ID (e.g., `my-chat-bot-123`) — it is used in every subsequent step.
2. **Enable two APIs** under **APIs & Services → Library**: the **Google Chat API** and the **Cloud Pub/Sub API**. Both are free at personal-bot volumes.
3. **Create a Service Account** (`IAM & Admin → Service Accounts → Create Service Account`), name it `hermes-chat-bot`, and **skip** the project-access step — IAM on the specific subscription is all you need; do **NOT** grant project-level Pub/Sub roles. Then **Keys → Add Key → Create new key → JSON**, download it, and save where only Hermes can read it (e.g., `~/.hermes/google-chat-sa.json`, `chmod 600`).
4. **Create the Pub/Sub topic** (`Pub/Sub → Topics → Create topic`, ID `hermes-chat-events`), then on the topic's **Subscriptions** tab create a subscription: ID `hermes-chat-events-sub`, **Pull** delivery, **7 days** message retention (so backlog survives a hermes restart).
5. **IAM binding on the topic** (critical): add principal `chat-api-push@system.gserviceaccount.com` with role `Pub/Sub Publisher`. Without this, Google Chat cannot publish events to the topic and the bot never receives anything.
6. **IAM binding on the subscription**: add your own SA (`hermes-chat-bot@<your-project>.iam.gserviceaccount.com`) with `Pub/Sub Subscriber`, and also grant `Pub/Sub Viewer` on the same subscription — Hermes calls `subscription.get()` at startup as a reachability check.
7. **Configure the Chat app** (`APIs & Services → Google Chat API → Configuration`): set app name/avatar/description, enable **Receive 1:1 messages** and **Join spaces and group conversations**, set **Connection settings → Cloud Pub/Sub** with topic `projects/<your-project>/topics/hermes-chat-events`, and restrict **Visibility** to your workspace while testing.
8. **Install the bot in a test space**: open Google Chat, start a DM via **+ New Chat**. The first message sends an `ADDED_TO_SPACE` event that Hermes uses to cache the bot's own `users/{id}` for self-message filtering.

> **The "Chat Bot Caller" role gotcha** — a common mistake is searching for a Chat-specific IAM role and granting it at the project level. That role does not exist. Chat bot authority comes from being **installed in a space**, not from IAM; all the SA needs is Pub/Sub subscriber on the subscription.

## Step 9: Configure Hermes

Add the Google Chat section to `~/.hermes/.env`:

```bash
# Required
GOOGLE_CHAT_PROJECT_ID=my-chat-bot-123
GOOGLE_CHAT_SUBSCRIPTION_NAME=projects/my-chat-bot-123/subscriptions/hermes-chat-events-sub
GOOGLE_CHAT_SERVICE_ACCOUNT_JSON=/home/you/.hermes/google-chat-sa.json

# Authorization — paste the emails of people allowed to talk to the bot
GOOGLE_CHAT_ALLOWED_USERS=you@yourdomain.com,coworker@yourdomain.com

# Optional
GOOGLE_CHAT_HOME_CHANNEL=spaces/AAAA...         # default delivery destination for cron jobs
GOOGLE_CHAT_MAX_MESSAGES=1                      # Pub/Sub FlowControl; 1 serializes commands per session
GOOGLE_CHAT_MAX_BYTES=16777216                  # 16 MiB — cap on in-flight message bytes
```

The project ID also falls back to `GOOGLE_CLOUD_PROJECT`, and the SA path falls back to `GOOGLE_APPLICATION_CREDENTIALS`. No Hermes extra is currently published for the Google Chat adapter, so install its dependencies directly:

```bash
pip install google-cloud-pubsub google-api-python-client google-auth google-auth-oauthlib
```

Then start the gateway with `hermes gateway`. On success a log line appears: `[GoogleChat] Connected; project=my-chat-bot-123, subscription=<redacted>, bot_user_id=users/XXXX, flow_control(msgs=1, bytes=16777216)`. Sending "hola" in the test DM makes the bot post a "Hermes is thinking…" marker, then **edit that same message in place** with the real response — no "message deleted" tombstones.

## Formatting and capabilities

Google Chat renders a limited markdown subset:

| Supported | Not supported |
|-----------|---------------|
| `*bold*`, `_italic_`, `~strike~`, `` `code` `` | Headings, lists |
| Inline images via URL | Interactive Card v2 buttons (v1 of this gateway) |
| Native file attachments (after `/setup-files` — see Step 10) | Native voice notes / circular video notes |

The agent's system prompt includes a Google Chat–specific hint so it avoids formatting that won't render. The **message size limit is 4000 characters**; longer agent responses are automatically split across multiple messages. For **thread support**, when a user replies inside a thread, Hermes detects the `thread.name` and posts its reply in the same thread, so **each thread gets a separate Hermes session**.

## Step 10: Native attachment delivery (optional, per-user OAuth)

Out of the box the bot posts text, inline images via URL, and download cards for audio/video/documents. To deliver **native** Chat attachments (the same file widget a human gets from drag-and-drop), each user authorizes the bot once via a per-user OAuth flow. The reason a separate flow is needed: Google Chat's `media.upload` endpoint hard-rejects service-account auth ("This method doesn't support app authentication with a service account. Authenticate with a user account."). No IAM role or scope fixes this — the endpoint only accepts user credentials, so the bot must act *as the user who asked for the file*.

**One-time setup (per profile):** in the same GCP project, **APIs & Services → Credentials → Create credentials → OAuth client ID → Desktop app**, download the JSON to the Hermes host, then register the client under the target profile:

```bash
# Default profile:
python -m plugins.platforms.google_chat.oauth \
    --client-secret /path/to/client_secret.json

# A named profile gets its own separate registration:
hermes -p <profile> python -m plugins.platforms.google_chat.oauth \
    --client-secret /path/to/client_secret.json
```

That writes the client secret into the active profile's Hermes home (e.g. `~/.hermes/google_chat_user_client_secret.json` for the default profile). The client secret is **profile-scoped, not shared across profiles** — profiles are isolated auth boundaries, so two profiles can point at different Google OAuth apps/accounts. Register it once per profile that needs attachment delivery.

**Per-user authorization (in chat):** each user runs the flow once in their own DM. They send `/setup-files`, then `/setup-files start` (the bot replies with an OAuth URL); they open it, click **Allow**, and watch the browser fail to load `http://localhost:1/?...&code=...` (that failure is **expected** — the auth code is in the URL bar); they paste it back as `/setup-files <PASTED_URL>` and the bot exchanges it for a refresh token. The token lands at `~/.hermes/google_chat_user_tokens/<sanitized_email>.json`, so subsequent file requests in that user's DM upload as them. `/setup-files revoke` deletes only that user's token.

**Scope:** the flow requests exactly one scope — `chat.messages.create` — covering both `media.upload` and the `messages.create` that references the uploaded `attachmentDataRef`. No Drive, no broader Chat scopes (least-privilege on purpose). **Multi-user behavior:** with no per-user token, the bot falls back to a legacy single-user token at `~/.hermes/google_chat_user_token.json` (if present from a pre-multi-user install); when neither is available it posts a clear notice telling the asker to run `/setup-files`. A revoke clears only that user's slot, and a 401/403 from one user's token evicts only that user's cache — users don't disrupt each other.

## Troubleshooting

- **Bot stays silent after "hola."** If the Pub/Sub subscription shows undelivered messages, Hermes isn't authenticated — verify `GOOGLE_CHAT_SERVICE_ACCOUNT_JSON` and that the SA is `Pub/Sub Subscriber` on the subscription. If the subscription has zero messages, Google Chat isn't publishing — recheck the **topic** IAM binding (`chat-api-push@system.gserviceaccount.com` needs `Pub/Sub Publisher`). Check `hermes gateway` logs for `[GoogleChat] Connected`; a `[GoogleChat] Config validation failed` line names the env var to fix.
- **Bot replies with an error instead of the answer.** Check logs for repeating `[GoogleChat] Pub/Sub stream died` — SA credentials may have been rotated or the subscription deleted. After **10 attempts** the adapter marks itself fatal.
- **"403 Forbidden" on every outbound message.** The bot was removed from the space (or revoked in the Chat API console). Re-install it — the next `ADDED_TO_SPACE` event re-enables messaging automatically.
- **Too many "Rate limit hit" warnings.** The Chat API default quota is 60 messages per space per minute; long streaming responses that exceed it are retried with exponential backoff (still user-visible latency). Use concise responses or raise the quota.
- **Bot keeps posting the "/setup-files" notice.** The asker has no per-user OAuth token and no legacy fallback — run `/setup-files` (Step 10); the next file request uploads natively without a restart.
- **`/setup-files start` says "No client credentials stored."** The one-time setup wasn't done *for this profile* (client secret is profile-scoped) — re-run `python -m plugins.platforms.google_chat.oauth --client-secret ...` (or `hermes -p <profile> ...`) under the profile the gateway uses, then retry.
- **`/setup-files <PASTED_URL>` says "Token exchange failed."** The auth code is single-use and short-lived — send `/setup-files start` for a fresh URL and retry.

## Security notes

- **Service Account scope** — the adapter requests `chat.bot` and `pubsub` scopes, but IAM should be the actual enforcement: grant the SA the minimum (`roles/pubsub.subscriber` + `roles/pubsub.viewer` on the subscription), not project- or org-level Pub/Sub roles.
- **Attachment download protection** — Hermes attaches the SA bearer token only to URLs whose host matches a short allowlist of Google-owned domains (`googleapis.com`, `drive.google.com`, `lh[3-6].googleusercontent.com`, and a few others). Any other host is rejected before the HTTP request, to protect against SSRF scenarios where a crafted event could redirect the bearer token to the GCE metadata service.
- **Redaction** — Service Account emails, subscription paths, and topic paths are stripped from log output by `agent/redact.py`. The debug envelope dump (`GOOGLE_CHAT_DEBUG_RAW=1`) routes through the same redaction filter and logs at DEBUG level.
- **Compliance** — to connect the bot to a regulated workspace (anything with a data-residency or AI-governance policy), get that approval **before** the first install.
- **User OAuth scope** — the per-user attachment flow requests *only* `chat.messages.create`. Tokens are persisted as plain JSON at `~/.hermes/google_chat_user_tokens/<sanitized_email>.json` (filesystem permissions are the protection — same model as the SA key file); each token is owned by exactly one user, and revoke is scoped to that user.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/google_chat.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/google_chat
**Last Updated**: 2026-06-19
**Status**: Active
