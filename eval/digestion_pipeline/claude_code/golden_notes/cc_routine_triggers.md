---
tags:
  - resource
  - documentation
  - claude_code
  - routines
  - triggers
keywords:
  - routine triggers
  - schedule trigger
  - api trigger
  - github trigger
  - fire endpoint
  - cron expression routine
  - pull request filters
  - combined triggers
topics:
  - Claude Code
  - Routines
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/routines
access_control_group: ["general"]
---

# Configure Routine Triggers

## Overview

A cloud [routine](https://code.claude.com/docs/en/routines) starts when one of its triggers matches. Claude Code supports three trigger types — **schedule**, **API**, and **GitHub** — and you can attach any combination of them to the same routine, adding or removing them at any time from the **Select a trigger** section of the routine's edit form. A single routine might run nightly, fire from a deploy script, and react to every new PR all at once.

This note covers configuring each of the three trigger types. The creation form that wires them in is in [Creating a Routine](cc_create_routine.md); the routine concept and example use cases are in [Routines Overview](cc_routines_overview.md).

## Add a schedule trigger

A schedule trigger runs the routine on a recurring cadence, or once at a specific future time. Pick a preset frequency in the **Select a trigger** section: **hourly**, **daily**, **weekdays**, or **weekly**. Times are entered in your local zone and converted automatically, so the routine runs at that wall-clock time regardless of where the cloud infrastructure is located.

Runs may start a few minutes after the scheduled time due to **stagger**. The offset is consistent for each routine.

For a custom interval such as every two hours or the first of each month, pick the closest preset in the form, then run `/schedule update` in the CLI to set a specific cron expression. **The minimum interval is one hour; expressions that run more frequently are rejected.**

### Schedule a one-off run

A one-off schedule fires the routine a single time at a specific timestamp — to remind yourself later in the week, open a cleanup PR after a rollout, or kick off a follow-up when an upstream change lands. After the routine fires, it auto-disables and the web UI marks it as **Ran**; to run it again, edit the routine and set a new one-off time. Create one from the CLI by describing the time in natural language (Claude resolves the phrase against the current time and confirms the absolute timestamp before saving), for example `/schedule in 2 weeks, open a cleanup PR that removes the feature flag`. The same local-to-UTC conversion as recurring schedules applies. One-off runs do **not** count against the daily routine run cap, but they consume your plan's regular subscription usage like any other session.

## Add an API trigger

An API trigger gives a routine a dedicated HTTP endpoint. POSTing to the endpoint with the routine's bearer token starts a new session and returns a session URL — use it to wire Claude Code into alerting systems, deploy pipelines, internal tools, or anywhere you can make an authenticated HTTP request. API triggers are added to an existing routine **from the web**; the CLI cannot currently create or revoke tokens.

To configure: open the routine for editing, scroll to **Select a trigger**, click **Add another trigger**, and choose **API**. The modal shows the URL plus a sample curl command. Copy the URL, click **Generate token**, and copy the token immediately — **the token is shown once and cannot be retrieved later**, so store it in a secret store. Each routine has its own token, scoped to triggering that routine only; return to the same modal and click **Regenerate** or **Revoke** to rotate it.

### Trigger a routine

Send a POST request to the `/fire` endpoint with the bearer token in the `Authorization` header. The request body accepts an optional `text` field for run-specific context (an alert body, a failing log) passed alongside the routine's saved prompt. The value is freeform and is not parsed: JSON or other structured payloads are received as a literal string.

```bash theme={null}
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01ABCDEFGHJKLMNOPQRSTUVW/fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

A successful request returns a JSON body with the new session ID and URL:

```json theme={null}
{
  "type": "routine_fire",
  "claude_code_session_id": "session_01HJKLMNOPQRSTUVWXYZ",
  "claude_code_session_url": "https://claude.ai/code/session_01HJKLMNOPQRSTUVWXYZ"
}
```

The `/fire` endpoint ships under the `experimental-cc-routine-2026-04-01` beta header; request/response shapes, rate limits, and token semantics may change. Breaking changes ship behind new dated beta header versions, and the two most recent previous versions keep working so callers have time to migrate. The endpoint is available to claude.ai users only and is not part of the Claude Platform API surface. For the full API reference (error responses, validation rules, field limits), see [Trigger a routine via API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) in the Claude Platform documentation.

## Add a GitHub trigger

A GitHub trigger starts a new session automatically when a matching event occurs on a connected repository. GitHub triggers are configured **from the web UI only**. During the research preview, GitHub webhook events are subject to per-routine and per-account hourly caps; events beyond the limit are dropped until the window resets.

To configure: open the routine for editing, scroll to **Select a trigger**, click **Add another trigger**, and choose **GitHub event**. The **Claude GitHub App** must be installed on the target repository — the trigger setup prompts you to install it if needed. (Running `/web-setup` grants repository access for cloning but does **not** install the GitHub App or enable webhook delivery.) Then select the repository, choose an event from the supported list, optionally add filters, and save.

### Supported events

Triggers subscribe to either event category, and within each you can pick a specific action (such as `pull_request.opened`) or react to all actions in the category:

| Event        | Triggers when                                                                 |
| :----------- | :---------------------------------------------------------------------------- |
| Pull request | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated |
| Release      | A release is created, published, edited, or deleted                           |

### Filter pull requests

Use filters to narrow which pull requests start a session. **All filter conditions must match** for the routine to trigger. The available filter fields are Author, Title, Body, Base branch, Head branch, Labels, Is draft, and Is merged. Each filter pairs a field with an operator: equals, contains, starts with, is one of, is not one of, or matches regex. The `matches regex` operator tests the **entire** field value, not a substring — to match any title containing `hotfix`, write `.*hotfix.*`; for literal substring matching use the `contains` operator instead.

### How sessions map to events

Each matching GitHub event starts a **new session**. Session reuse across events is not available for GitHub-triggered routines, so two PR updates produce two independent sessions.

**Source**: https://code.claude.com/docs/en/routines
**Last Updated**: 2026-06-13
**Status**: Active
