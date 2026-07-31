---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - cron
keywords:
  - script-only cron
  - no-agent mode
  - watchdog
  - exit code delivery mapping
  - hermes scripts directory
  - silent tick
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/cron-script-only
access_control_group: ["general"]
---

# Hermes Agent — Script-Only Cron Jobs (No LLM)

## Overview

Script-only cron is Hermes' **no-agent mode**: the cron system minus the LLM. A script runs on a schedule, and its stdout — if any — is delivered to a messaging platform (Telegram / Discord / Slack / Signal). There is no model call, no agent loop, and no token spend on a tick; the script itself decides whether to alert. It is the classic watchdog pattern (memory/disk/GPU alerts, CI pings, periodic metrics, external-event pollers, heartbeats) for cases where you already know exactly what message you want to send and only need it to run on a timer.

No-agent jobs live in the same `cronjob` scheduler as LLM-driven jobs, so pausing, resuming, listing, logs, schedule syntax, and delivery targeting all behave identically — the only difference is that on each tick the scheduler runs your script instead of waking an agent. Use the normal (LLM-driven) cron path instead when the agent must *decide* what to say (summarize a document, pick interesting feed items, draft a human-friendly message); no-agent mode is for when the script's stdout already IS the message. This note is the recipe; the full schedule grammar and lifecycle live in the [cron feature reference](../../term_dictionary/term_cron.md).

The scheduler tick → run script → delivery router flow:

```
   ┌──────────────────┐          ┌──────────────────┐
   │ scheduler tick   │  every   │ run script       │
   │ (every N minutes)│ ──────▶ │ (bash or python) │
   └──────────────────┘          └──────────────────┘
                                          │
                                          │ stdout
                                          ▼
                                 ┌──────────────────┐
                                 │ delivery router  │
                                 │ (telegram/disc…) │
                                 └──────────────────┘
```

## When to Use It

Use no-agent mode for tasks whose output is fully determined by the script — no reasoning required:

- **Memory / disk / GPU watchdogs.** Run every 5 minutes, alert only when a threshold is breached.
- **CI hooks.** Deploy finished → post the commit SHA. Build failed → send the last 100 lines of the log.
- **Periodic metrics.** "Daily Stripe revenue at 9am" as a simple API call + pretty-print.
- **External event pollers.** Check an API, alert on state change.
- **Heartbeats.** Ping a dashboard every N minutes to prove the host is alive.

Choose a normal LLM-driven cron job when the agent must decide what to say — summarize a long document, pick the interesting items from a feed, or draft a friendly message. The no-agent path is strictly for the case where the script's stdout already IS the final message.

## Create One from Chat

The signature win of no-agent mode is that the agent sets the watchdog up for you — no editor, no shell, no remembering flags. You describe the behavior; Hermes writes the script, schedules it, and reports when it will fire. Under the hood the agent makes two tool calls — `write_file` to author the check script, then `cronjob(...)` with `no_agent=True` to schedule it:

```python
# 1. Write the check script
write_file(
    path="~/.hermes/scripts/memory-watchdog.sh",
    content='''#!/usr/bin/env bash
ram_pct=$(free | awk '/^Mem:/ {printf "%d", $3 * 100 / $2}')
if [ "$ram_pct" -ge 85 ]; then
  echo "RAM ${ram_pct}% on $(hostname)"
fi
# Empty stdout = silent tick; no message sent.
''',
)

# 2. Schedule it — no_agent=True skips the LLM on every tick
cronjob(
    action="create",
    schedule="every 5m",
    script="memory-watchdog.sh",
    no_agent=True,
    deliver="telegram",
    name="memory-watchdog",
)
```

From then on every tick is free: the scheduler runs the script, pipes non-empty stdout to Telegram, and never touches a model. You do **not** specify `--no-agent` yourself — Hermes' `cronjob` tool description tells it to reach for `no_agent=True` whenever the message content is fully determined by the script (e.g. "alert me when X", "every N minutes check Y and tell me if Z"), and to fall back to the LLM-driven path when the request needs reasoning ("summarize the new issues", "pick the most interesting headlines", "draft a friendly reminder"). The agent can also pause, resume, edit, and remove jobs from chat the same way it creates them — `cronjob(action='pause'|'update'|..., job_id=...)` — so the full create / list / update / pause / resume / run-now / remove lifecycle is reachable without learning any CLI commands.

## Create One from the CLI

The CLI path produces the same result in three commands — write the script, schedule it, verify:

```bash
# 1. Write your script
cat > ~/.hermes/scripts/memory-watchdog.sh <<'EOF'
#!/usr/bin/env bash
# Alert when RAM usage is over 85%. Silent otherwise.
RAM_PCT=$(free | awk '/^Mem:/ {printf "%d", $3 * 100 / $2}')
if [ "$RAM_PCT" -ge 85 ]; then
  echo "⚠ RAM ${RAM_PCT}% on $(hostname)"
fi
# Empty stdout = silent run; no message sent.
EOF
chmod +x ~/.hermes/scripts/memory-watchdog.sh

# 2. Schedule it
hermes cron create "every 5m" \
  --no-agent \
  --script memory-watchdog.sh \
  --deliver telegram \
  --name "memory-watchdog"

# 3. Verify
hermes cron list
hermes cron run <job_id>    # fire it once to test
```

No prompt, no skill, no model.

## How Script Output Maps to Delivery

The exit code and stdout of each run determine what gets delivered:

| Script behavior | Result |
|-----------------|--------|
| Exit 0, non-empty stdout | stdout is delivered verbatim |
| Exit 0, empty stdout | Silent tick — no delivery |
| Exit 0, stdout contains `{"wakeAgent": false}` on the last line | Silent tick (shared gate with LLM jobs) |
| Non-zero exit code | Error alert is delivered (so a broken watchdog doesn't fail silently) |
| Script timeout | Error alert is delivered |

The "silent when empty" rule is the heart of the watchdog pattern: the script is free to run every minute, but the channel only sees a message when something actually needs attention. The `{"wakeAgent": false}` last-line gate is shared with LLM jobs, so the same silent-tick mechanism applies in both modes.

## Script Rules, Schedule Syntax & Delivery Targets

**Script location is sandboxed.** Scripts must live in `~/.hermes/scripts/`, enforced at both job-creation time and run time — absolute paths, `~/` expansion, and path-traversal patterns (`../`) are rejected. This is the same directory shared with the pre-check script gate used by LLM jobs. **Interpreter is chosen by file extension** — `.sh`/`.bash` run under `/bin/bash`; anything else runs under `sys.executable` (the current Python). Hermes intentionally does NOT honour `#!/...` shebangs, keeping the trusted interpreter set explicit and small.

**Schedule syntax** is identical to all other cron jobs — interval (`every 5m`, `every 2h`), standard cron (`0 9 * * *` = 9am daily), or one-shot (`30m` = run once in 30 minutes):

```bash
hermes cron create "every 5m"        # interval
hermes cron create "0 9 * * *"       # standard cron: 9am daily
hermes cron create "30m"             # one-shot: run once in 30 minutes
```

**Delivery targets** (`--deliver`) accept everything the gateway knows: `telegram` (platform home channel), `telegram:-1001234567890` (specific chat), `telegram:-1001234567890:17585` (specific forum topic), `discord:#ops`, `slack:#engineering`, `signal:+15551234567`, or `local` (save to `~/.hermes/cron/output/`). No running gateway is required at script-run time for bot-token platforms (Telegram, Discord, Slack, Signal, SMS, WhatsApp) — the tool calls each platform's REST endpoint directly using the credentials already in `~/.hermes/.env` / `~/.hermes/config.yaml`.

The lifecycle commands mirror LLM jobs exactly: `hermes cron list`, `pause <job_id>`, `resume <job_id>`, `edit <job_id> --schedule "every 10m"`, `edit <job_id> --agent` (flip to LLM mode), `edit <job_id> --no-agent --script …` (flip back), and `remove <job_id>`.

## Worked Example & When to Use OS Cron Instead

A disk-space watchdog: silent when both filesystems are under 90%, firing exactly one line per over-threshold filesystem when one fills up:

```bash
cat > ~/.hermes/scripts/disk-alert.sh <<'EOF'
#!/usr/bin/env bash
# Alert when / or /home is over 90% full.
THRESHOLD=90
df -h / /home 2>/dev/null | awk -v t="$THRESHOLD" '
  NR > 1 && $5+0 >= t {
    printf "⚠ Disk %s full on %s\n", $5, $6
  }
'
EOF
chmod +x ~/.hermes/scripts/disk-alert.sh

hermes cron create "*/15 * * * *" \
  --no-agent \
  --script disk-alert.sh \
  --deliver telegram \
  --name "disk-alert"
```

Comparison with the alternatives: `cronjob --no-agent` (this page) runs your script on Hermes' schedule for recurring watchdogs/alerts/metrics that don't need reasoning; the default `cronjob` (LLM) runs an agent with an optional pre-check script when the message content requires reasoning over data; and OS-level cron + `curl` to a webhook subscription runs your script on the OS schedule when Hermes itself might be unhealthy (the thing you're monitoring). For critical system-health watchdogs that must fire *even when the gateway is down*, use OS cron with a plain `curl` to a Hermes webhook subscription (or any external alerting endpoint) — those run as independent OS processes and don't depend on Hermes being up. The in-gateway scheduler is the right choice when the thing being monitored is external.

**Source**: https://hermes-agent.nousresearch.com/docs/guides/cron-script-only
**Last Updated**: 2026-06-19
**Status**: Active
