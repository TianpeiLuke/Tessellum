---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - scheduling
keywords:
  - cronjob
  - scheduled tasks
  - hermes cron
  - /cron command
  - gateway scheduler
  - jobs.json
  - delivery options
topics:
  - Hermes Agent
  - Task Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
access_control_group: ["general"]
---

# Hermes Agent — Scheduled Tasks (Cron)

## Overview

Cron scheduling in Hermes Agent is the **unattended task surface**: it runs a fresh `AIAgent` session on a schedule and delivers the result, with no human in the loop each tick. Hermes exposes all cron management through a single `cronjob` tool with action-style operations (create / list / update / pause / resume / run / remove) rather than separate schedule/list/remove tools, so the whole lifecycle is chat-driven — you can create, pause, edit, and remove jobs by asking in plain language, with no CLI required. A cron job can schedule one-shot or recurring tasks, attach zero/one/multiple skills, and deliver output back to the origin chat, local files, or any configured platform target. This note covers the job *lifecycle procedure*: creating jobs (`/cron`, `hermes cron`, natural language), attaching skills, running inside a project directory (`workdir`), editing, lifecycle verbs with name-based lookup, the 60-second gateway scheduler, delivery options, schedule formats, repeat behavior, and `jobs.json` storage. The cost-control / data-flow model around cron (no-agent mode, `wakeAgent` gates, `context_from` chaining, toolset budgeting, provider recovery, `[SILENT]`) is documented separately in [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md).

Cron jobs use whatever provider `hermes model` selected; `hermes setup --portal` is the lowest-friction option for unattended runs since OAuth refresh is automatic. Cron-run sessions cannot recursively create more cron jobs — Hermes disables cron management tools inside cron executions to prevent runaway scheduling loops.

## What Cron Can Do Now

Cron jobs can:

- schedule one-shot or recurring tasks
- pause, resume, edit, trigger, and remove jobs
- attach zero, one, or multiple skills to a job
- deliver results back to the origin chat, local files, or configured platform targets
- run in fresh agent sessions with the normal static tool list
- run in **no-agent mode** — a script on a schedule, its stdout delivered verbatim, zero LLM involvement (see [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md))

## Creating Scheduled Tasks

Three entry points produce the same job. **In chat with `/cron`** the form is `/cron add <schedule> "<prompt>"` — e.g. `/cron add 30m "Remind me to check the build"` or `/cron add "every 2h" "Check server status"`; `--skill` is repeatable to attach one or more skills (`/cron add "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps`).

**From the standalone CLI** the schedule and prompt are positional:

```bash
hermes cron create "every 2h" "Check server status"
hermes cron create "every 1h" "Summarize new feed items" --skill blogwatcher
hermes cron create "every 1h" "Use both skills and combine the result" \
  --skill blogwatcher \
  --skill maps \
  --name "Skill combo"
```

**Through natural conversation** Hermes uses the unified `cronjob` tool internally — e.g. *"Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram."*

## Skill-backed Cron Jobs

A cron job can load one or more skills before it runs the prompt. Skills are loaded in order, and the prompt becomes the task instruction layered on top of them — letting a scheduled agent inherit reusable workflows without stuffing the full skill text into the cron prompt. Single skill uses `skill="..."`; multiple uses `skills=[...]`:

```python
cronjob(
    action="create",
    skills=["blogwatcher", "maps"],
    prompt="Look for new local events and interesting nearby places, then combine them into one short brief.",
    schedule="every 6h",
    name="Local brief",
)
```

## Running a Job Inside a Project Directory (`workdir`)

Cron jobs default to running detached from any repo — no `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` is loaded, and the terminal / file / code-exec tools run from whatever working directory the gateway started in. Pass `--workdir` (CLI) or `workdir=` (tool call) to change that:

```python
# From a chat, via the cronjob tool
cronjob(
    action="create",
    schedule="every 1d at 09:00",
    workdir="/home/me/projects/acme",
    prompt="Audit open PRs, summarize CI health, and post to #eng",
)
```

When `workdir` is set: `AGENTS.md`/`CLAUDE.md`/`.cursorrules` from that directory are injected into the system prompt (same discovery order as the interactive CLI); `terminal`, `read_file`, `write_file`, `patch`, `search_files`, and `execute_code` all use that directory as their cwd; the path must be an **absolute directory that exists** (relative/missing paths are rejected at create/update time); and `--workdir ""` (or `workdir=""`) on edit clears it. **Serialization:** jobs with a `workdir` run sequentially on the scheduler tick, not in the parallel pool — the cron worker applies the workdir through process-global terminal state, so two concurrent workdir jobs would corrupt each other's cwd. Workdir-less jobs still run in parallel.

## Editing Jobs

You do not need to delete and recreate jobs to change them. The `<job_id>` placeholder also accepts the job's **name** (case-insensitive); an exact ID takes precedence over name matches, and an ambiguous name (multiple jobs) is refused with the candidate IDs printed for disambiguation.

```bash
hermes cron edit <job_id> --schedule "every 4h"
hermes cron edit <job_id> --prompt "Use the revised task"
hermes cron edit <job_id> --skill blogwatcher --skill maps
hermes cron edit <job_id> --add-skill maps
hermes cron edit <job_id> --remove-skill blogwatcher
hermes cron edit <job_id> --clear-skills
```

Skill flags: repeated `--skill` **replaces** the attached skill list; `--add-skill` **appends** without replacing; `--remove-skill` removes specific skills; `--clear-skills` removes all attached skills.

## Lifecycle Actions

Cron jobs have a fuller lifecycle than just create/remove. The chat verbs (`/cron list|pause|resume|run|remove <job_id>`) mirror the CLI:

```bash
hermes cron list
hermes cron pause <job_id_or_name>
hermes cron resume <job_id_or_name>
hermes cron run <job_id_or_name>
hermes cron remove <job_id_or_name>
hermes cron edit <job_id_or_name> [...flags]
hermes cron status
hermes cron tick
```

What they do: `pause` keeps the job but stops scheduling it; `resume` re-enables it and computes the next future run; `run` triggers the job on the next scheduler tick; `remove` deletes it entirely; `edit` modifies schedule/prompt/delivery/etc.

**Name-based lookup.** All mutating verbs (`pause`, `resume`, `run`, `remove`, `edit`) plus the agent's `cronjob` tool accept a job **name** (case-insensitive) in place of the hex ID. The agent and CLI prefer an exact ID match if one exists; ambiguous name matches are refused with the full candidate-ID list. Names are not unique, so this guard is load-bearing — it prevents silently mutating the wrong job when two share a name. The agent-facing API is one tool: `cronjob(action="create"|"list"|"update"|"pause"|"resume"|"run"|"remove", ...)`; for `update`, pass `skills=[]` to remove all attached skills.

## How It Works (Gateway Scheduler)

**Cron execution is handled by the gateway daemon.** The gateway ticks the scheduler every 60 seconds, running any due jobs in isolated agent sessions. Install it as a user service (`hermes gateway install`), a Linux boot-time system service (`sudo hermes gateway install --system`), or run in the foreground (`hermes gateway`).

On each tick Hermes:

1. loads jobs from `~/.hermes/cron/jobs.json`
2. checks `next_run_at` against the current time
3. starts a fresh `AIAgent` session for each due job
4. optionally injects one or more attached skills into that fresh session
5. runs the prompt to completion
6. delivers the final response
7. updates run metadata and the next scheduled time

A file lock at `~/.hermes/cron/.tick.lock` prevents overlapping scheduler ticks from double-running the same job batch.

## Delivery Options

When scheduling a job you specify where the output goes; the agent's final response is delivered automatically, so you do **not** need to call `send_message` in the cron prompt. Tokens include `"origin"` (back to where the job was created — default on messaging platforms), `"local"` (save to `~/.hermes/cron/output/` only — default on CLI), and per-platform targets like `"telegram"`, `"telegram:123456"` (chat by ID), `"telegram:-100123:17585"` (`chat_id:thread_id` topic), `"discord"`, `"discord:#engineering"`, `"slack"`, `"whatsapp"`, `"signal"`, `"matrix"`, `"mattermost"`, `"email"`, `"sms"`, and others.

**Routing intent `all`** fans out to every connected home channel and is **resolved at fire time** — a job created before you wired up Telegram picks it up on the next tick once `TELEGRAM_HOME_CHANNEL` is set. `all` composes with explicit targets (`origin,all` delivers to the origin chat *plus* every other connected home channel, de-duplicating by `(platform, chat_id, thread_id)`); comma-separated lists (`telegram,discord`) target a specific set. Zero matching channels is fine — the job produces no delivery targets and is recorded as a delivery failure upstream.

**Telegram cron topic.** When Telegram topic mode is enabled, the root DM is reserved as a system lobby (replies there are rebuffed). Point cron at a dedicated forum topic by creating a topic, copying its `message_thread_id`, and setting `TELEGRAM_CRON_THREAD_ID=<id>`. This applies only to cron deliveries; explicit `deliver="telegram:chat_id:thread_id"` targets still win over the env var, and replies to cron messages arrive in the existing topic session.

**Response wrapping.** By default delivered output is wrapped with a `Cronjob Response: <name>` header/footer so the recipient knows it came from a scheduled task; set `cron.wrap_response: false` in `~/.hermes/config.yaml` to deliver the raw agent output.

## Schedule Formats

Four accepted formats. **Relative delays** are one-shot (`30m`, `2h`, `1d` → run once after that delay). **Intervals** recur (`every 30m`, `every 2h`, `every 1d`). **ISO timestamps** are one-time (`2026-03-15T09:00:00`). **Cron expressions** are 5-field crontab syntax:

```text
0 9 * * *       → Daily at 9:00 AM
0 9 * * 1-5     → Weekdays at 9:00 AM
0 */6 * * *     → Every 6 hours
30 8 1 * *      → First of every month at 8:30 AM
0 0 * * 0       → Every Sunday at midnight
```

## Repeat Behavior

| Schedule type | Default repeat | Behavior |
|--------------|----------------|----------|
| One-shot (`30m`, timestamp) | 1 | Runs once |
| Interval (`every 2h`) | forever | Runs until removed |
| Cron expression | forever | Runs until removed |

Override the default with `repeat=N` (e.g. `cronjob(action="create", schedule="every 2h", repeat=5, prompt="...")`).

## Self-contained Prompts and Security

Cron jobs run in a completely fresh agent session, so the prompt must contain everything the agent needs that is not already provided by attached skills. **BAD:** `"Check on that server issue"`. **GOOD:** `"SSH into server 192.168.1.100 as user 'deploy', check if nginx is running with 'systemctl status nginx', and verify https://example.com returns HTTP 200."`

For **security**, scheduled-task prompts are scanned for prompt-injection and credential-exfiltration patterns at creation and update time. Prompts containing invisible Unicode tricks, SSH backdoor attempts, or obvious secret-exfiltration payloads are blocked.

## Job Storage

Jobs are stored in `~/.hermes/cron/jobs.json`; output from job runs is saved to `~/.hermes/cron/output/{job_id}/{timestamp}.md`. Jobs may store `model` and `provider` as `null` — when those fields are omitted, Hermes resolves them at execution time from the global configuration, and they only appear in the job record when a per-job override is set. The storage uses atomic file writes so interrupted writes never leave a partially written job file behind.

**Source**: `inbox/hermes_agent_docs/user-guide/features/cron.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
**Last Updated**: 2026-06-19
**Status**: Active
