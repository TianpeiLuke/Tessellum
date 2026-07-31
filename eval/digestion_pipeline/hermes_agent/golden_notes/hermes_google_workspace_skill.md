---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - productivity
keywords:
  - google workspace skill
  - gapi cli
  - gmail calendar drive sheets docs
  - oauth2 token refresh
  - bundled skill
  - custom from header
topics:
  - Hermes Agent
  - Skills
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace
access_control_group: ["general"]
---

# Hermes Agent — Google Workspace Skill

## Overview

The Google Workspace skill is a **bundled Hermes skill** (it lives at `skills/productivity/google-workspace/`) that gives the agent Gmail, Calendar, Drive, Contacts, Sheets, and Docs access through a single OAuth2-authenticated `$GAPI` CLI. It uses OAuth2 with automatic token refresh, and prefers the [Google Workspace CLI (`gws`)](https://github.com/googleworkspace/cli) when available for broader coverage, falling back to Google's Python client libraries otherwise. Setup is fully agent-driven — you ask Hermes to set up Google Workspace and it walks you through Google Cloud project creation, OAuth credentials, and the browser-authorize handshake. Every command returns JSON, so the agent can parse results and chain them into further actions.

## Setup

The setup is fully agent-driven — ask Hermes to set up Google Workspace and it walks you through each step. The flow:

1. **Create a Google Cloud project** and enable the required APIs (Gmail, Calendar, Drive, Sheets, Docs, People)
2. **Create OAuth 2.0 credentials** (Desktop app type) and download the client secret JSON
3. **Authorize** — Hermes generates an auth URL, you approve in the browser, paste back the redirect URL
4. **Done** — token auto-refreshes from that point on

Email-only users have a lighter alternative: if you only need email (no Calendar/Drive/Sheets), use the **himalaya** skill instead — it works with a Gmail App Password and takes 2 minutes, with no Google Cloud project needed.

## Gmail

Gmail support spans searching, reading, sending, replying, and label management, all through the `$GAPI gmail` subcommand.

**Searching** uses Gmail's native query syntax and returns JSON with `id`, `from`, `subject`, `date`, `snippet`, and `labels` per message:

```bash
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"
```

**Reading** a message by ID returns the full body as text (prefers plain text, falls back to HTML): `$GAPI gmail get MESSAGE_ID`.

**Sending** supports plain/HTML bodies, a custom `From` display name, and CC:

```bash
# Basic send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"

# HTML email
$GAPI gmail send --to user@example.com --subject "Report" \
  --body "<h1>Q4 Results</h1><p>Details here</p>" --html

# Custom From header (display name + email)
$GAPI gmail send --to user@example.com --subject "Hello" \
  --from '"Research Agent" <user@example.com>' --body "Message text"

# With CC
$GAPI gmail send --to user@example.com --cc "team@example.com" \
  --subject "Update" --body "FYI"
```

**Custom From header.** The `--from` flag customizes the sender display name on outgoing emails — useful when multiple agents share one Gmail account but recipients should see different names. The `--from` value is set as the RFC 5322 `From` header on the MIME message; Gmail allows customizing the display name on your own authenticated email address without additional configuration. If a *different email address* is used in `--from` (not the authenticated account), Gmail requires that address to be configured as a [Send As alias](https://support.google.com/mail/answer/22370) in Gmail Settings → Accounts → Send mail as. The flag works on both `send` and `reply`.

**Replying** with `$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."` automatically threads the reply (sets `In-Reply-To` and `References` headers and reuses the original thread ID).

**Labels** can be listed and applied/removed:

```bash
# List all labels
$GAPI gmail labels

# Add/remove labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

## Calendar

Calendar list defaults to the next 7 days; creating an event **requires a timezone**, and events can carry a location and attendees:

```bash
# List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# Create event (timezone required)
$GAPI calendar create --summary "Team Standup" \
  --start 2026-03-01T10:00:00-07:00 --end 2026-03-01T10:30:00-07:00

# With location and attendees
$GAPI calendar create --summary "Lunch" \
  --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z \
  --location "Cafe" --attendees "alice@co.com,bob@co.com"

# Delete event
$GAPI calendar delete EVENT_ID
```

Calendar times **must** include a timezone offset (e.g. `-07:00`) or use UTC (`Z`). Bare datetimes like `2026-03-01T10:00:00` are ambiguous and will be treated as UTC.

## Drive, Sheets, Docs & Contacts

**Drive** supports keyword search and raw Drive query syntax:

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

**Sheets** can read, write, and append A1-notation ranges:

```bash
# Read a range
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# Write to a range
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

**Docs** returns the title and full text content: `$GAPI docs get DOC_ID`. **Contacts** lists contacts: `$GAPI contacts list --max 20`.

## Output Format

All commands return JSON. Key fields per service:

| Command | Fields |
|---------|--------|
| `gmail search` | `id`, `threadId`, `from`, `to`, `subject`, `date`, `snippet`, `labels` |
| `gmail get` | `id`, `threadId`, `from`, `to`, `subject`, `date`, `labels`, `body` |
| `gmail send/reply` | `status`, `id`, `threadId` |
| `calendar list` | `id`, `summary`, `start`, `end`, `location`, `description`, `htmlLink` |
| `calendar create` | `status`, `id`, `summary`, `htmlLink` |
| `drive search` | `id`, `name`, `mimeType`, `modifiedTime`, `webViewLink` |
| `contacts list` | `name`, `emails`, `phones` |
| `sheets get` | 2D array of cell values |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup (ask Hermes to set up Google Workspace) |
| `REFRESH_FAILED` | Token revoked — re-run authorization steps |
| `HttpError 403: Insufficient Permission` | Missing scope — revoke and re-authorize with the right services |
| `HttpError 403: Access Not Configured` | API not enabled in Google Cloud Console |
| `ModuleNotFoundError` | Run setup script with `--install-deps` |

**Source**: `inbox/hermes_agent_docs/user-guide/skills/google-workspace.md` · https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace
**Last Updated**: 2026-06-19
**Status**: Active
