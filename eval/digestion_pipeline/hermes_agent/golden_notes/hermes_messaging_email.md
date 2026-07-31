---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - email
keywords:
  - hermes email gateway
  - imap smtp adapter
  - app password
  - email allowed users
  - email poll interval
  - threaded smtp replies
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email
access_control_group: ["general"]
---

# Hermes Messaging — Email Setup (IMAP/SMTP)

## Overview

The Email gateway is the Hermes messaging adapter that lets people **email the agent and get replies in-thread** over standard IMAP and SMTP — no special client or bot API needed. It works with Gmail, Outlook, Yahoo, Fastmail, or any provider that supports IMAP/SMTP, and it is built entirely on Python's standard-library `imaplib`, `smtplib`, and `email` modules, so it needs **no additional packages or external services** beyond an email account.

This is a "connect Hermes to platform X" setup runbook: pick a dedicated account, generate an app password, drop credentials into `~/.hermes/.env`, set an allowlist, and start the gateway. The adapter then polls the inbox for unseen mail, feeds each message to the agent, and replies via threaded SMTP. It is **separate** from the bundled Himalaya email skill (which manages a mailbox through terminal commands and requires the external `himalaya` CLI); the table below distinguishes the two use cases.

| Use case | What to configure | External dependency |
|---|---|---|
| Let people email the Hermes agent and receive replies | Email gateway adapter on this page | None beyond an IMAP/SMTP email account |
| Let the agent inspect, compose, move, and manage mailbox messages from terminal tools | Himalaya email skill | `himalaya` CLI and `~/.config/himalaya/config.toml` |

## Prerequisites

- **A dedicated email account** for your Hermes agent (don't use your personal email).
- **IMAP enabled** on the email account.
- **An app password** if using Gmail or another provider with 2FA.

**Gmail Setup** — Enable 2-Factor Authentication on the Google Account, go to [App Passwords](https://myaccount.google.com/apppasswords), create a new App Password (select "Mail" or "Other"), and copy the 16-character password to use instead of the regular password.

**Outlook / Microsoft 365** — Enable 2FA in [Security Settings](https://account.microsoft.com/security), create an App Password under "Additional security options", and use IMAP host `outlook.office365.com`, SMTP host `smtp.office365.com`.

**Other Providers** — Most providers support IMAP/SMTP. Check the provider's docs for the IMAP host and port (usually port 993 with SSL), the SMTP host and port (usually port 587 with STARTTLS), and whether app passwords are required.

## Step 1: Configure Hermes

The easiest way runs the wizard, which prompts for the email address, password, IMAP/SMTP hosts, and allowed senders after you select **Email** from the platform menu:

```bash
hermes gateway setup
```

### Manual Configuration

Add to `~/.hermes/.env`:

```bash
# Required
EMAIL_ADDRESS=hermes@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop    # App password (not your regular password)
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com

# Security (recommended)
EMAIL_ALLOWED_USERS=your@email.com,colleague@work.com

# Optional
EMAIL_IMAP_PORT=993                    # Default: 993 (IMAP SSL)
EMAIL_SMTP_PORT=587                    # Default: 587 (SMTP STARTTLS)
EMAIL_POLL_INTERVAL=15                 # Seconds between inbox checks (default: 15)
EMAIL_HOME_ADDRESS=your@email.com      # Default delivery target for cron jobs
```

## Step 2: Start the Gateway

```bash
hermes gateway              # Run in foreground
hermes gateway install      # Install as a user service
sudo hermes gateway install --system   # Linux only: boot-time system service
```

On startup, the adapter (1) tests the IMAP and SMTP connections, (2) marks all existing inbox messages as "seen" so only **new** emails are processed, and (3) starts polling for new messages.

## How It Works

### Receiving Messages

The adapter polls the IMAP inbox for **UNSEEN** messages at a configurable interval (default 15 seconds). For each new email:

- The **subject line** is included as context (e.g., `[Subject: Deploy to production]`).
- **Reply emails** (subject starting with `Re:`) skip the subject prefix — the thread context is already established.
- **Attachments** are cached locally: images (JPEG, PNG, GIF, WebP) become available to the vision tool, and documents (PDF, ZIP, etc.) become available for file access.
- **HTML-only emails** have their tags stripped for plain-text extraction.
- **Self-messages** are filtered out to prevent reply loops.
- **Automated/noreply senders** are silently ignored — `noreply@`, `mailer-daemon@`, `bounce@`, `no-reply@`, and emails carrying `Auto-Submitted`, `Precedence: bulk`, or `List-Unsubscribe` headers.

### Sending Replies

Replies go out via SMTP with proper email threading: **In-Reply-To** and **References** headers maintain the thread, the **subject line** is preserved with a `Re:` prefix (no double `Re: Re:`), a **Message-ID** is generated with the agent's domain, and responses are sent as plain text (UTF-8).

### File Attachments

The agent can attach files in replies. Include `MEDIA:/path/to/file` in the response and the file is attached to the outgoing email.

### Skipping Attachments

To ignore all incoming attachments (for malware protection or bandwidth savings), add to `config.yaml`:

```yaml
platforms:
  email:
    skip_attachments: true
```

When enabled, attachment and inline parts are skipped before payload decoding; the email body text is still processed normally.

## Access Control

Email access follows the same pattern as all other Hermes platforms:

1. **`EMAIL_ALLOWED_USERS` set** → only emails from those addresses are processed.
2. **No allowlist set** → unknown senders get a pairing code.
3. **`EMAIL_ALLOW_ALL_USERS=true`** → any sender is accepted (use with caution).

**Always configure `EMAIL_ALLOWED_USERS`.** Without it, anyone who knows the agent's email address could send commands — and the agent has terminal access by default.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"IMAP connection failed"** at startup | Verify `EMAIL_IMAP_HOST` and `EMAIL_IMAP_PORT`. Ensure IMAP is enabled on the account. For Gmail, enable it in Settings → Forwarding and POP/IMAP. |
| **"SMTP connection failed"** at startup | Verify `EMAIL_SMTP_HOST` and `EMAIL_SMTP_PORT`. Check the password is correct (use App Password for Gmail). |
| **Messages not received** | Check `EMAIL_ALLOWED_USERS` includes the sender's email. Check spam folder — some providers flag automated replies. |
| **"Authentication failed"** | For Gmail, use an App Password, not the regular password. Ensure 2FA is enabled first. |
| **Duplicate replies** | Ensure only one gateway instance is running. Check `hermes gateway status`. |
| **Slow response** | The default poll interval is 15 seconds. Reduce with `EMAIL_POLL_INTERVAL=5` for faster response (but more IMAP connections). |
| **Replies not threading** | The adapter uses In-Reply-To headers. Some web-based clients may not thread correctly with automated messages. |

## Security

**Use a dedicated email account.** Don't use your personal email — the agent stores the password in `.env` and has full inbox access via IMAP.

- Use **App Passwords** instead of the main password (required for Gmail with 2FA).
- Set `EMAIL_ALLOWED_USERS` to restrict who can interact with the agent.
- The password is stored in `~/.hermes/.env` — protect this file (`chmod 600`).
- IMAP uses SSL (port 993) and SMTP uses STARTTLS (port 587) by default — connections are encrypted.

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_ADDRESS` | Yes | — | Agent's email address |
| `EMAIL_PASSWORD` | Yes | — | Email password or app password |
| `EMAIL_IMAP_HOST` | Yes | — | IMAP server host (e.g., `imap.gmail.com`) |
| `EMAIL_SMTP_HOST` | Yes | — | SMTP server host (e.g., `smtp.gmail.com`) |
| `EMAIL_IMAP_PORT` | No | `993` | IMAP server port |
| `EMAIL_SMTP_PORT` | No | `587` | SMTP server port |
| `EMAIL_POLL_INTERVAL` | No | `15` | Seconds between inbox checks |
| `EMAIL_ALLOWED_USERS` | No | — | Comma-separated allowed sender addresses |
| `EMAIL_HOME_ADDRESS` | No | — | Default delivery target for cron jobs |
| `EMAIL_ALLOW_ALL_USERS` | No | `false` | Allow all senders (not recommended) |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/email.md`
**Last Updated**: 2026-06-19
**Status**: Active
