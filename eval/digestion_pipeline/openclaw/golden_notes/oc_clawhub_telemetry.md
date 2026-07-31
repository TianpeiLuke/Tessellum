---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - telemetry
keywords:
  - clawhub install telemetry
  - clawhub disable telemetry
  - clawhub_disable_telemetry
  - install counts installsalltime installscurrent
  - what clawhub does not collect
  - clawhub install event slug version
  - clawhub telemetry opt out
topics:
  - OpenClaw
  - ClawHub Telemetry
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/telemetry
access_control_group: ["general"]
---

# OpenClaw — ClawHub Install Telemetry and Opt-Out

## Overview

This note documents ClawHub's CLI install telemetry: the minimal, best-effort signal the ClawHub CLI sends to compute aggregate install counts, the exact conditions under which an event is sent, the precise payload, what is explicitly NOT collected, the aggregate counters maintained per skill, the transparency/user-control posture, and the single environment variable that disables it. It mirrors the `clawhub/telemetry` source page in full — every section of that page (intro, When telemetry is collected, What we collect + What we do not collect, Install counts, Transparency + user controls, How to disable telemetry) is covered here.

## When telemetry is collected

ClawHub uses **minimal CLI telemetry** whose only purpose is to compute aggregate install counts. Telemetry is only sent when ALL three conditions hold: you are logged in in the CLI; you run `clawhub install <slug>`; and telemetry is **not disabled** (see "How to disable telemetry" below). If you are not logged in, nothing is reported — the logged-in state is the precondition for any event. There is no telemetry on browsing, searching, or any command other than `clawhub install`.

## What we collect

On each reported `clawhub install`, the CLI sends **one best-effort install event** — "best-effort" meaning the event is not retried or guaranteed and a failure to send does not block the install. The event includes exactly two fields:

- `slug`: the installed skill slug.
- `version`: the installed version, when known.

### What we do not collect

The source page is explicit about what is NOT collected on an install event. None of the following is sent:

- No folder paths or folder-derived identifiers.
- No file contents.
- No per-run logs, prompts, or other CLI output.

## Install counts

ClawHub maintains **aggregate counters per skill** computed from the reported install events. Two counters are defined:

- `installsAllTime`: unique users who have reported at least one CLI install for the skill.
- `installsCurrent`: unique users who have reported an install and have not deleted their telemetry.

Both counters are per-skill and count **unique users** (not raw install events). The difference between the two is data-deletion: `installsAllTime` keeps every user who ever reported an install, whereas `installsCurrent` excludes users who have since deleted their telemetry.

## Transparency + user controls

The transparency posture is that **everyone only sees aggregated install counters** — no per-user or per-install detail is exposed. For data removal, deleting your account also deletes your telemetry data (which is what removes a user from the `installsCurrent` count described above).

## How to disable telemetry

To opt out, set the environment variable `CLAWHUB_DISABLE_TELEMETRY` to `1`:

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

With this variable set, the CLI will not send install telemetry — this satisfies the "telemetry is not disabled" precondition in reverse, so no install event is sent even when you are logged in and run `clawhub install <slug>`.

**Source**: OpenClaw documentation — `clawhub/telemetry` (mirror `inbox/openclaw_docs/clawhub/telemetry.md`)
**Last Updated**: 2026-06-22
**Status**: Active
