---
tags:
  - resource
  - documentation
  - hermes_agent
  - cron
  - troubleshooting
keywords:
  - cron troubleshooting
  - jobs not firing
  - delivery failures
  - skill loading failures
  - gateway ticker
  - diagnostic commands
topics:
  - Hermes Agent
  - Cron Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting
access_control_group: ["general"]
---

# Cron Troubleshooting

## Overview

Cron Troubleshooting is the **diagnostic runbook** for Hermes cron jobs that aren't behaving as expected. It works through failure modes in order, organized so that almost every cron problem falls into one of four categories — **timing** (jobs not firing), **delivery** (the job ran but nothing arrived), **permissions**, or **skill loading** — plus a perf section and a diagnostic-command cheat sheet. The guiding model is that a cron job is a *fresh* AIAgent (or no-agent script) session fired by the gateway's background ticker; most failures are therefore a missing ticker, a silently-defaulted schedule, a misconfigured delivery target, or an uninstalled/disabled skill, rather than a bug in the job's prompt. This note is the debugging companion to the [cron automation guide](hermes_guide_automate_with_cron.md) and the [script-only cron guide](hermes_guide_cron_script_only.md); the full cron feature reference lives in the cron concept and the cron repository module.

## Jobs Not Firing

Work through four timing checks in order:

**Check 1 — Verify the job exists and is active.** Run `hermes cron list` and confirm the state is `[active]`, not `[paused]` or `[completed]`. A `[completed]` job has exhausted its repeat count — edit the job to reset it.

**Check 2 — Confirm the schedule is correct.** A misformatted schedule **silently defaults to one-shot or is rejected entirely**. Test the expression against the expected evaluation: `0 9 * * *` → 9:00 AM every day; `0 9 * * 1` → 9:00 AM every Monday; `every 2h` → every 2 hours from now; `30m` → 30 minutes from now; `2025-06-01T09:00:00` → an absolute UTC timestamp. If a job fires once and then disappears from the list, it was a one-shot schedule (`30m`, `1d`, or an ISO timestamp) — expected behavior.

**Check 3 — Is the gateway running?** Cron jobs are fired by the gateway's background **ticker thread, which ticks every 60 seconds**. A regular CLI chat session does **not** automatically fire cron jobs. To fire jobs automatically you need a running gateway (`hermes gateway` foreground, or `hermes gateway start` for the installed service). For one-off debugging, manually trigger a tick with `hermes cron tick`.

**Check 4 — Check the system clock and timezone.** Jobs use the local timezone. A wrong clock or unexpected timezone fires jobs at the wrong times:

```bash
date
hermes cron list   # Compare next_run times with local time
```

## Delivery Failures

When a job runs but nothing arrives, the job still completes — it just doesn't send. Four checks:

**Check 1 — Verify the deliver target is correct.** Delivery targets are **case-sensitive** and require the matching platform to be configured; a misconfigured target silently drops the response. The per-platform requirements: `telegram` needs `TELEGRAM_BOT_TOKEN`, `discord` needs `DISCORD_BOT_TOKEN`, `slack` needs `SLACK_BOT_TOKEN` (all in `~/.hermes/.env`); `whatsapp`/`signal`/`matrix` need their gateway/homeserver configured; `email` needs SMTP in `config.yaml`; `sms` needs an SMS provider; `local` needs write access to `~/.hermes/cron/output/`; `origin` delivers back to the chat where the job was created. Other supported platforms include `mattermost`, `homeassistant`, `dingtalk`, `feishu`, `wecom`, `weixin`, `bluebubbles`, `qqbot`, and `webhook`. You can target a specific chat with `platform:chat_id` syntax (e.g., `telegram:-1001234567890`). Check `hermes cron list` for an updated `last_error` field.

**Check 2 — Check `[SILENT]` usage.** If the job produces no output, delivery is suppressed; if the agent response includes the cron quiet marker `[SILENT]`, delivery is **also** suppressed. This is intentional for monitoring jobs, but verify the prompt is not accidentally suppressing everything. Use prompts like "respond with only [SILENT] if nothing changed" — avoid embedding `[SILENT]` inside a longer explanation, because cron treats the marker as a suppression signal.

**Check 3 — Platform token permissions.** Each bot needs specific permissions: a **Telegram** bot must be an admin in the target group/channel; a **Discord** bot must have permission to send in the target channel; a **Slack** bot must be added to the workspace and have the `chat:write` scope.

**Check 4 — Response wrapping.** By default cron responses are wrapped with a header and footer (`cron.wrap_response: true`). Some platforms don't handle this well — disable it in `config.yaml`:

```yaml
cron:
  wrap_response: false
```

## Skill Loading Failures

**Check 1 — Verify skills are installed.** Run `hermes skills list`. Skills must be installed before they can be attached to cron jobs; if missing, install with `hermes skills install <skill-name>` or via `/skills` in the CLI.

**Check 2 — Check skill name vs. skill folder name.** Skill names are case-sensitive and must match the installed folder name. Confirm the exact name from `hermes skills list`.

**Check 3 — Skills that require interactive tools.** Cron jobs run with the **`cronjob`, `messaging`, and `clarify` toolsets disabled**. This prevents recursive cron creation, direct message sending (delivery is handled by the scheduler), and interactive prompts. A skill that relies on these toolsets won't work in a cron context — check its docs to confirm it works in non-interactive (headless) mode.

**Check 4 — Multi-skill ordering.** Multiple skills load in order. If Skill A depends on context from Skill B, ensure B loads first:

```bash
/cron add "0 9 * * *" "..." --skill context-skill --skill target-skill
```

Here `context-skill` loads before `target-skill`.

## Job Errors and Failures

**Check 1 — Review recent job output.** Error context appears in: (1) the chat where the job delivers (if delivery succeeded), (2) `~/.hermes/logs/agent.log` for scheduler messages (or `errors.log` for warnings), and (3) the job's `last_run` metadata via `hermes cron list`.

**Check 2 — Common error patterns.** *"No such file or directory" for scripts* — the `script` path must be absolute (or relative to the Hermes config directory); verify the file exists and re-point it with `hermes cron edit <job_id> --script ~/.hermes/scripts/your-script.py`. *"Skill not found" at job execution* — the skill must be installed on the machine running the scheduler; skills don't sync across machines, so reinstall after moving. *Job runs but delivers nothing* — likely a delivery-target issue, no output, or a `[SILENT]` quiet marker. *Job hangs or times out* — the scheduler uses an **inactivity-based timeout** (default 600s, configurable via `HERMES_CRON_TIMEOUT`, `0` for unlimited); the agent can run as long as it's actively calling tools, and the timer fires only after sustained inactivity, so long-running jobs should offload data collection to scripts and deliver only the result.

**Check 3 — Lock contention.** The scheduler uses **file-based locking** to prevent overlapping ticks. If two gateway instances run (or a CLI session conflicts with a gateway), jobs may be delayed or skipped — find and kill duplicates, keeping only one:

```bash
ps aux | grep hermes
# Kill duplicate processes, keep only one
```

**Check 4 — Permissions on `jobs.json`.** Jobs are stored in `~/.hermes/cron/jobs.json`. If the file is not readable/writable by your user, the scheduler **fails silently** — check `ls -la` and `chmod 600` so your user owns it.

## Performance Issues

**Slow job startup.** Each cron job creates a fresh AIAgent session, which may involve provider authentication and model loading. For time-sensitive schedules, add buffer time (e.g., `0 8 * * *` instead of `0 9 * * *`).

**Too many overlapping jobs.** The scheduler executes jobs **sequentially within each tick**. If multiple jobs are due simultaneously they run one after another — stagger schedules (e.g., `0 9 * * *` and `5 9 * * *`) to avoid delays.

**Large script output.** Scripts that dump megabytes of output slow the agent and may hit token limits. Filter/summarize at the script level — emit only what the agent needs to reason about.

## Diagnostic Commands

```bash
hermes cron list                    # Show all jobs, states, next_run times
hermes cron run <job_id>            # Schedule for next tick (for testing)
hermes cron edit <job_id>           # Fix configuration issues
hermes logs                         # View recent Hermes logs
hermes skills list                  # Verify installed skills
```

## Getting More Help

If the issue persists after working through this guide: (1) run the job with `hermes cron run <job_id>` (fires on the next gateway tick) and watch for errors in the chat output; (2) check `~/.hermes/logs/agent.log` for scheduler messages and `~/.hermes/logs/errors.log` for warnings; (3) open an issue at [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) with the job ID and schedule, the delivery target, what you expected vs. what happened, and the relevant error messages from the logs. For the complete cron reference, see the cron automation guide and the cron feature reference.

**Source**: `inbox/hermes_agent_docs/guides/cron-troubleshooting.md`
**Last Updated**: 2026-06-19
**Status**: Active
