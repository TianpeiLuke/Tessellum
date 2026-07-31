---
title: Sub-Plan B11 — Claude Code Docs: Automation & Scheduling
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["routines", "scheduled-tasks", "desktop-scheduled-tasks", "headless"]
---

# Sub-Plan B11: Automation & Scheduling

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / 8-GATE / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 pages that cover running Claude Code unattended: cloud **routines** (scheduled / API / GitHub
triggers on Anthropic-managed infrastructure), session-scoped **`/loop` scheduled tasks** (the in-session
cron tools), **Desktop scheduled tasks** (local recurring runs), and **headless / non-interactive mode**
(`claude -p` for scripts and CI). P2 (Phase B) — these features are built on the P1 cores (agentic loop,
MCP, permissions, context window) and link back to them, so this runs after Phase A.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 9,906 measured words. **Planned: 10 notes.**

## Content Strategy

- **Prioritize**: the three-way scheduling comparison (Cloud vs Desktop vs `/loop`) that anchors the whole
  theme, plus the routine trigger model (schedule/API/GitHub) and the headless `-p` + `--bare` operating mode.
- **Group**: split `routines.md` (4.1Kw, >2,500 cap) by concept (what routines are + comparison) vs
  procedure (create) vs trigger-configuration (one note covering all three trigger types) vs management.
  Split `headless.md` (15 code blocks, >6 cap) into a concept/operating-mode note and an examples/patterns note.
- **Skip / link-out (own other sub-plans)**: cloud environment / network access / default allowlist →
  B12B (`claude-code-on-the-web`); MCP connectors → B08A (`mcp`); permission modes → B05A; tools-reference
  (Monitor / Bash background / CronCreate field details) → B03B; GitHub Actions / GitLab CI → B13B;
  Channels → B08B; `/goal` → B10B; worktrees → B10B; skills/commands → B06; env-vars (`CLAUDE_CODE_DISABLE_CRON`)
  → B03A; structured-output SDK callbacks / streaming SDK → B19C; CLI flags reference → B03B. These are
  referenced via links, never duplicated.
- **Terms**: routed per Pattern B (see Undigested Terms Plan); existing term notes linked, not re-digested.

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| routines | /routines | 4,085 | 4 | 7 | 12 | concept + procedure |
| scheduled-tasks | /scheduled-tasks | 2,216 | 8 | 8 | 7 | procedure + concept |
| desktop-scheduled-tasks | /desktop-scheduled-tasks | 1,537 | 0 | 8 | 0 | procedure |
| headless | /headless | 2,068 | 15 | 3 | 10 | concept + procedure |

> **H2 lists (document order):**
> - **routines**: Example use cases · Create a routine (H3 Create from the web, Create from the CLI) · Configure triggers (H3 Add a schedule trigger, Add an API trigger, Add a GitHub trigger) · Manage routines (H3 View and interact with runs, Edit and control routines, Repositories and branch permissions, Connectors, Environments and network access) · Usage and limits · Troubleshooting · Related resources
> - **scheduled-tasks**: Compare scheduling options · Run a prompt repeatedly with /loop (H3 Run on a fixed interval, Let Claude choose the interval, Run the built-in maintenance prompt, Customize the default prompt with loop.md, Stop a loop) · Set a one-time reminder · Manage scheduled tasks · How scheduled tasks run (H3 Jitter, Seven-day expiry) · Cron expression reference · Disable scheduled tasks · Limitations
> - **desktop-scheduled-tasks**: Compare scheduling options · Create a scheduled task · Schedule options · How scheduled tasks run · Missed runs · Permissions for scheduled tasks · Manage scheduled tasks · Related resources
> - **headless**: Basic usage (H3 Start faster with bare mode, Background tasks at exit) · Examples (H3 Pipe data through Claude, Add Claude to a build script, Get structured output, Stream responses, Auto-approve tools, Create a commit, Customize the system prompt, Continue conversations) · Next steps

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **10 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_scheduling_options_comparison.md` | concept | scheduled-tasks + desktop-scheduled-tasks: Compare scheduling options table; scheduled-tasks intro | 450 | The three ways to schedule (Cloud routines / Desktop / `/loop`) across machine-on, open-session, local-file, MCP, permission, interval axes; how to choose; links to the three dedicated notes. The hub note for the theme. |
| 2 | `cc_routines_overview.md` | concept | routines: intro, Example use cases, Usage and limits | 500 | What a cloud routine is (saved prompt+repos+connectors on Anthropic-managed infra); the three trigger types; combined triggers; six example use cases; plans/account scoping; daily run cap and overage. |
| 3 | `cc_create_routine.md` | procedure | routines: Create a routine (web + CLI) | 550 | Step-by-step creating a routine from web/Desktop/CLI: prompt+model, repositories (`claude/` branches), environment, trigger, connectors+permissions; `/schedule` natural-language CLI form and `list`/`update`/`run`. |
| 4 | `cc_routine_triggers.md` | procedure | routines: Configure triggers (schedule, API, GitHub) | 600 | Configuring the three trigger types: schedule (presets, timezone, stagger, custom cron, one-off), API (endpoint, token, `/fire` curl), GitHub (supported events, PR filters, session-per-event). Links to platform API ref. |
| 5 | `cc_manage_routines.md` | procedure | routines: Manage routines, Troubleshooting | 500 | Routine detail page: view/interact with runs, run-now/pause/edit/delete, repository+branch permissions, connectors source, environment/network access; green-status caveat; `/schedule` "Unknown command" + disabled-by-policy troubleshooting. |
| 6 | `cc_loop_scheduled_tasks.md` | procedure | scheduled-tasks: Run a prompt repeatedly with /loop, Set a one-time reminder | 600 | `/loop` modes (interval+prompt / prompt-only dynamic / bare maintenance / `loop.md`), fixed vs Claude-chosen interval, Monitor-tool fallback, stop with Esc, one-time natural-language reminders; Bedrock/Vertex/Foundry caveats. |
| 7 | `cc_scheduled_task_execution_model.md` | concept | scheduled-tasks: How scheduled tasks run (Jitter, Seven-day expiry), Cron expression reference, Manage scheduled tasks, Disable, Limitations | 600 | How session-scoped tasks fire (between-turns, low priority, local timezone), jitter offsets, 7-day expiry, resume restore rules, 50-task cap, the `CronCreate`/`CronList`/`CronDelete` tools, cron 5-field reference, `CLAUDE_CODE_DISABLE_CRON`, limitations. |
| 8 | `cc_desktop_scheduled_tasks.md` | procedure | desktop-scheduled-tasks: Create, Schedule options, How they run, Missed runs, Permissions, Manage | 650 | Creating/managing local Desktop scheduled tasks: fields (name/desc/instructions/schedule), worktree toggle, schedule presets, fresh-session firing, keep-awake, single catch-up for missed runs, per-task permission mode, `SKILL.md` on disk, `update_scheduled_task` self-reschedule. |
| 9 | `cc_headless_mode.md` | concept | headless: intro, Basic usage (bare mode, background tasks at exit) | 500 | Running Claude Code non-interactively with `claude -p`; what `-p` loads vs `--bare` (skips hook/skill/plugin/MCP/memory/CLAUDE.md discovery); bare-mode auth (API key / apiKeyHelper), default tools, flag-only context table; background-task termination at exit. |
| 10 | `cc_headless_examples.md` | procedure | headless: Examples (pipe, build script, structured output, stream, auto-approve, commit, system prompt, continue) | 650 | Reusable `-p` patterns: pipe stdin (10MB cap), build-script linter, `--output-format` text/json/stream-json + `--json-schema`, stream `api_retry`/`init`/`plugin_install` events, `--allowedTools`/permission-mode auto-approve, commit, `--append-system-prompt`, `--continue`/`--resume`. |

**Estimate: 10 notes** — concept ×4 (notes 1, 2, 7, 9), procedure ×6 (notes 3, 4, 5, 6, 8, 10). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (9,906 words). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,600 (avg ~560/note). Code blocks distributed: routines (curl/json) → note 4; scheduled-tasks (`/loop`, cron) → notes 6/7; headless (15 blocks) → split notes 9 (table-only) and 10 (≤6 code). No note exceeds the 6-code cap.
- **Building Block Distribution**: concept ×4 (notes 1, 2, 7, 9) · procedure ×6 (notes 3, 4, 5, 6, 8, 10). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_scheduling_options_comparison` (6 term notes)
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — A scheduled task is the core mechanism this comparison anchors; all three options express a recurring cadence as a cron-style schedule (minimum 1h cloud, 1m Desktop/`/loop`), the time-encoding this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note compares Claude Code's own three scheduling surfaces (cloud routines, Desktop tasks, in-session `/loop`), so the product term is the host whose features are being contrasted.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Every scheduling option runs Claude Code unattended (no human in the loop), the autonomous operating mode this term defines; the comparison axes (open-session, machine-on) describe degrees of that autonomy.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Each option is the same agent harness invoked on a timer in a different runtime (cloud session, local Desktop session, in-session loop), so the harness term grounds what "runs" in each column.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The comparison table has an explicit MCP-servers row (connectors per task vs config files vs inherited-from-session), making MCP one of the differentiating axes this note tabulates.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The table's permission-prompts row contrasts how each option handles approvals (autonomous cloud, configurable Desktop, session-inherited `/loop`), the progressive-permission concept this term defines.

### 2. `cc_routines_overview` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — A routine is a saved Claude Code configuration (prompt + repos + connectors) run automatically, so the product term is the engine the routine packages and replays.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note states routines run autonomously as full cloud sessions with no permission prompts, suited to unattended repeatable work — the defining behavior of an autonomous coding agent.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — The schedule trigger runs a routine on a recurring cadence (hourly/nightly/weekly or a custom cron interval), the time-scheduling concept this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — A routine bundles a set of MCP connectors it can call during each run; the example use cases (Slack summaries, Linear tickets) are connector-driven, so MCP is a first-class part of the routine config.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — Several example use cases (deploy verification, alert triage via API trigger, GitHub PR review) wire routines into CI/CD pipelines, the continuous-integration/delivery automation this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — A routine executes as a full Claude Code cloud session — i.e. the agent harness running on Anthropic-managed infrastructure with the routine's prompt, tools, and environment.

### 3. `cc_create_routine` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the procedure for creating a Claude Code routine, so the product term grounds what is being configured (prompt, model, repositories, environment).
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — The creation flow's trigger step picks a schedule (preset frequency or a custom cron via `/schedule update`), the recurring-time concept this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The Connectors step includes all connected MCP connectors by default and lets you scope which the routine can reach, a required part of the creation form this note walks through.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The Permissions step controls branch-push scope (`claude/`-prefixed only vs unrestricted) and the note notes routines run with no permission-mode picker, the trust-scoping concept this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note stresses the prompt must be self-contained because the routine runs autonomously with no approval prompts — the unattended-agent operating mode this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Creating a routine configures a cloud-hosted instance of the agent harness (its repos, environment, connectors, tools), so the harness term grounds what each created routine instantiates.

### 4. `cc_routine_triggers` (6 term notes)
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — The schedule trigger is configured by preset or a custom cron expression (minimum 1-hour interval, with stagger), the central time-encoding this note documents.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — The API and GitHub triggers wire routines into deploy pipelines and repository events (`pull_request.opened`, releases), the CI/CD automation this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Triggers are the start conditions for a Claude Code routine, so the product term grounds what each trigger launches (a cloud session of Claude Code).
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The API trigger's `/fire` endpoint is itself a callable HTTP tool that starts an agent session and returns a session URL — programmatic invocation analogous to the tool-use pattern this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Each trigger starts an unattended autonomous session (a GitHub event spawns one session per event), the no-human-in-the-loop behavior this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — A triggered run uses the routine's MCP connectors (e.g. an alert-triage API trigger reads a stack trace and opens a PR via connectors), so MCP is the tool layer each trigger's session draws on.

### 5. `cc_manage_routines` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note manages Claude Code routines (run-now, pause, edit, delete, view runs), so the product term grounds the entity being managed.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — Management includes pausing/resuming the schedule (the **Repeats** toggle) and editing trigger cadence, the recurring-schedule concept this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The Connectors section explains where a routine's MCP connectors come from (claude.ai integrations vs local `claude mcp add` vs committed `.mcp.json`), a managed dimension this note documents.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Branch-push permissions (`claude/`-only vs unrestricted) are managed per repository here, the trust-scoping concept this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The green-status caveat (started/exited without infra error ≠ task succeeded) reflects that routines run autonomously and must be inspected after the fact, the unattended-agent operating mode this term defines.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — Managing API tokens and GitHub triggers is how routines stay wired into deploy/CI pipelines, the continuous-integration automation this term defines.

### 6. `cc_loop_scheduled_tasks` (6 term notes)
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — `/loop` converts an interval into a cron expression and schedules the job; seconds round up to cron's one-minute granularity — the cron time-encoding this term defines is the core mechanism of the note.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `/loop` is a bundled Claude Code skill that re-runs a prompt in the open session, so the product term grounds the host that runs the loop.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — A bare `/loop` runs a built-in maintenance prompt (continue unfinished work, tend the PR, run cleanup passes) and can end itself when provably complete — autonomous self-paced agent behavior this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The note states `/loop` is a bundled skill and that you can pass another command/skill as the loop prompt (`/loop 20m /review-pr 1234`), so the skill term grounds both the loop itself and its payload.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The `loop.md` default-prompt file and the self-paced maintenance prompt are deliberate prompt designs (concise, ≤25KB, refined between iterations), the prompt/context-shaping discipline this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — In dynamic `/loop` mode Claude may use the Monitor tool to stream a background script instead of re-running the prompt, the agentic tool-invocation pattern this term defines.

### 7. `cc_scheduled_task_execution_model` (6 term notes)
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — The note's Cron expression reference (5-field `minute hour day-of-month month day-of-week`, wildcards/steps/ranges/lists, vixie-cron OR semantics, unsupported `L`/`W`/`?`) is the canonical content of this term, making it the primary anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — These are Claude Code's session-scoped scheduled tasks and their execution semantics (between-turns firing, local timezone, 50-task cap), so the product term grounds the runtime described.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — A scheduled prompt fires autonomously between turns at low priority while Claude is idle, the unattended-agent execution behavior this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The scheduler underlies the `/loop` bundled skill and the `CronCreate`/`CronList`/`CronDelete` tools it exposes, so the skill term connects this execution model to the user-facing loop skill.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Jitter, 7-day expiry, and the no-catch-up limitation are deliberate scheduler design choices that bound and shape how long an agent loop can run, the systems-design discipline this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Under the hood Claude manages tasks via the `CronCreate`/`CronList`/`CronDelete` tools, the agentic tool-invocation mechanism this term defines.

### 8. `cc_desktop_scheduled_tasks` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code Desktop's local scheduled tasks (fields, schedule presets, firing, management), so the product term grounds the surface being configured.
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — Desktop tasks run on a schedule (Manual/Hourly/Daily/Weekdays/Weekly presets, or a custom interval via natural language), the recurring-time concept this term defines (1-minute minimum interval).
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Each Desktop task has its own permission mode, allow-rules from `~/.claude/settings.json` apply, and approvals can be saved/revoked per task — the trust-scoping concept this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — A Desktop task starts a fresh autonomous session at the scheduled time (edit files, run commands, open PRs) independent of any manual session, the unattended-agent operating mode this term defines.
- [Git Worktree (Subagent isolation analog)](../../term_dictionary/term_subagent.md) — The note's worktree toggle gives each run its own isolated Git worktree "the same way parallel sessions work," an isolation pattern analogous to the fresh-context isolation this term defines for delegated work.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — A Desktop task's prompt lives on disk as `~/.claude/scheduled-tasks/<task>/SKILL.md` and a task can self-reschedule via `update_scheduled_task`, persistent agent state analogous to the durable-memory concept this term defines.

### 9. `cc_headless_mode` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents running Claude Code non-interactively with `claude -p`, so the product term grounds the runtime being invoked from scripts/CI.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `claude -p` and `--bare` invoke the same agent harness (tools, agent loop, context management) without the interactive UI; `--bare` strips the auto-loaded harness context (hooks/skills/plugins/MCP/memory/CLAUDE.md), so the harness term defines exactly what bare mode trims.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — The note positions `-p`/`--bare` as the mode for CI and scripts that need the same result on every machine, the continuous-integration automation this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Bare mode is a deliberate context-control choice: it skips auto-discovery so only explicitly-passed flags (settings, MCP config, agents, system-prompt additions) shape the context, the context-shaping discipline this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Headless `-p` runs Claude Code as a non-interactive autonomous agent in a pipeline (no human steering), the unattended-agent operating mode this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — In bare mode Claude has Bash/file-read/file-edit tools by default and background Bash tasks are terminated at exit, the tool-use mechanism this term defines.

### 10. `cc_headless_examples` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — These are reusable `claude -p` invocation patterns, so the product term grounds the command being scripted.
- [Structured Output](../../term_dictionary/term_structured_output.md) — A core example uses `--output-format json` with `--json-schema` to return data conforming to a JSON Schema in the `structured_output` field, exactly the schema-constrained-generation concept this term defines.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — The examples (build-script typo linter via `package.json`, commit creation, PR-diff security review) wrap `-p` into CI/build pipelines, the continuous-integration automation this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The auto-approve example uses `--allowedTools` and permission modes (`dontAsk`, `acceptEdits`) to scope what runs without prompting in locked-down CI, the progressive-permission concept this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `--allowedTools "Bash,Read,Edit"` and permission-rule syntax (`Bash(git diff *)`) control which agent tools may be called without asking, the tool-use mechanism this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The examples drive the agent harness from the CLI (pipe stdin, `--append-system-prompt`, `--continue`/`--resume`, stream `init`/`api_retry` events), so the harness term grounds what each flag configures.

## Section Coverage Map

```
routines.md
├── intro (what a routine is, triggers, plans, /schedule, admin toggle) → note 2 (cc_routines_overview)
├── Example use cases ──────────────────────── → note 2
├── Create a routine ───────────────────────── → note 3 (cc_create_routine)
│   ├── Create from the web (Steps) ────────── → note 3
│   └── Create from the CLI (/schedule) ─────── → note 3
├── Configure triggers ─────────────────────── → note 4 (cc_routine_triggers)
│   ├── Add a schedule trigger (+one-off) ───── → note 4
│   ├── Add an API trigger (+/fire, API ref) ── → note 4
│   └── Add a GitHub trigger (events, filters) ─ → note 4
├── Manage routines ────────────────────────── → note 5 (cc_manage_routines)
│   ├── View and interact with runs ────────── → note 5
│   ├── Edit and control routines ──────────── → note 5
│   ├── Repositories and branch permissions ── → note 5
│   ├── Connectors ─────────────────────────── → note 5 (→ B08A mcp)
│   └── Environments and network access ─────── → note 5 (→ B12B claude-code-on-the-web)
├── Usage and limits ───────────────────────── → note 2
├── Troubleshooting (/schedule unknown, policy) → note 5
└── Related resources ──────────────────────── → notes 2/5 (links)
scheduled-tasks.md
├── intro (session-scoped, resume) ─────────── → note 1 + note 6
├── Compare scheduling options (table) ─────── → note 1 (cc_scheduling_options_comparison)
├── Run a prompt repeatedly with /loop ─────── → note 6 (cc_loop_scheduled_tasks)
│   ├── Run on a fixed interval ────────────── → note 6
│   ├── Let Claude choose the interval ─────── → note 6 (Monitor tool → B03B)
│   ├── Run the built-in maintenance prompt ── → note 6
│   ├── Customize the default prompt loop.md ─ → note 6
│   └── Stop a loop ────────────────────────── → note 6
├── Set a one-time reminder ────────────────── → note 6
├── Manage scheduled tasks (Cron tools) ────── → note 7 (cc_scheduled_task_execution_model)
├── How scheduled tasks run ────────────────── → note 7
│   ├── Jitter ─────────────────────────────── → note 7
│   └── Seven-day expiry ───────────────────── → note 7
├── Cron expression reference ──────────────── → note 7
├── Disable scheduled tasks (env var) ──────── → note 7 (→ B03A env-vars)
└── Limitations ────────────────────────────── → note 7
desktop-scheduled-tasks.md
├── intro (Routines page, local vs remote) ── → note 8 (cc_desktop_scheduled_tasks)
├── Compare scheduling options (table) ─────── → note 1 (duplicate table → owned by note 1; note 8 links)
├── Create a scheduled task (+worktree note) ─ → note 8 (worktree → B10B)
├── Schedule options ───────────────────────── → note 8
├── How scheduled tasks run (keep-awake) ───── → note 8
├── Missed runs (single catch-up) ──────────── → note 8
├── Permissions for scheduled tasks ────────── → note 8 (→ B05A permissions)
├── Manage scheduled tasks (SKILL.md, update) → note 8
└── Related resources ──────────────────────── → note 8 (links)
headless.md
├── intro (Agent SDK, claude -p, credit note) → note 9 (cc_headless_mode) (Agent SDK → B19A)
├── Basic usage ────────────────────────────── → note 9
│   ├── Start faster with bare mode ────────── → note 9
│   └── Background tasks at exit ───────────── → note 9 (Bash background → B03B)
├── Examples ───────────────────────────────── → note 10 (cc_headless_examples)
│   ├── Pipe data through Claude ───────────── → note 10
│   ├── Add Claude to a build script ───────── → note 10
│   ├── Get structured output ──────────────── → note 10
│   ├── Stream responses (event tables) ────── → note 10 (SDK streaming → B19C)
│   ├── Auto-approve tools ─────────────────── → note 10 (permission modes → B05A)
│   ├── Create a commit ────────────────────── → note 10
│   ├── Customize the system prompt ────────── → note 10 (system-prompt flags → B03B)
│   └── Continue conversations ─────────────── → note 10 (sessions → B02B)
└── Next steps (cards) ─────────────────────── → notes 9/10 (links)
```
No orphaned sections. The duplicate **Compare scheduling options** table appears on both scheduled-tasks
and desktop-scheduled-tasks; it is owned once by note 1, and note 8 links to note 1 rather than re-tabulating it.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| routines.md (4.1Kw >2,500, 7 H2 mixed) | notes 2,3,4,5 + link-outs | exceeds density cap; distinct BBs/topics: overview+limits (concept) vs create (procedure) vs trigger config (procedure) vs management+troubleshooting (procedure). Environment/network + connectors detail linked to B12B/B08A. |
| scheduled-tasks.md (2.2Kw, 8 H2) | notes 6,7 + the comparison table to note 1 | `/loop` usage (procedure) vs the scheduler execution model + cron reference (concept) are different BBs; the cross-page comparison table is hoisted to the hub note 1 to avoid duplication. |
| desktop-scheduled-tasks.md (1.5Kw) | note 8 (single) + comparison table → note 1 | within caps as one procedure note; only the shared comparison table is delegated to note 1. |
| headless.md (2.1Kw, **15 code blocks** >6) | notes 9,10 | code-block cap is the binding constraint: operating-model/bare-mode concept (note 9, ≤6 code) vs the 8 example patterns (note 10, ≤6 code) keeps both within the 6-code-block cap. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_scheduling_options_comparison | concept | 450 | 1 | ✅ |
| 2 | cc_routines_overview | concept | 500 | 0 | ✅ |
| 3 | cc_create_routine | procedure | 550 | 1 | ✅ |
| 4 | cc_routine_triggers | procedure | 600 | 3 | ✅ |
| 5 | cc_manage_routines | procedure | 500 | 0 | ✅ |
| 6 | cc_loop_scheduled_tasks | procedure | 600 | 5 | ✅ |
| 7 | cc_scheduled_task_execution_model | concept | 600 | 2 | ✅ |
| 8 | cc_desktop_scheduled_tasks | procedure | 650 | 0 | ✅ |
| 9 | cc_headless_mode | concept | 500 | 2 | ✅ |
| 10 | cc_headless_examples | procedure | 650 | 6 | ✅ |

No note exceeds 650 words (cap 2,500), 6 code blocks (cap 6 — note 10 is exactly at cap, verified), or 400
lines. The headless split is what keeps note 10 at ≤6 code blocks. No over-compression — every H2/H3 maps
to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_scheduling_options_comparison cc_routines_overview cc_create_routine cc_routine_triggers cc_manage_routines cc_loop_scheduled_tasks cc_scheduled_task_execution_model cc_desktop_scheduled_tasks cc_headless_mode cc_headless_examples"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (10 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 10 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB confirms in-degree ≥1 for all 10 notes after inlinks applied; no graph-island | DB in-degree query post-execution |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 10 rows** under an "Automation & Scheduling" cluster + increments the
BB-distribution counts (concept ×4, procedure ×6). The entry-point back-link is added to each note at finalization.

## Undigested Terms Plan (Step 4e)

B11 creates **0 new `term_dictionary` captures** — every domain term on the 4 pages is covered by a B11
`cc_` doc-concept note, an existing substantive term note (link), or its home sub-plan (Pattern B). Dedup
checked across BOTH `term_dictionary/` AND `resources/documentation/`: no existing `cc_` scheduling/routines/
false-positives — not the same concept-same-sense.

| Term on B11 pages | Disposition |
|---|---|
| Routine | note 2 `cc_routines_overview` (doc concept) |
| Trigger (schedule / API / GitHub) | note 4 `cc_routine_triggers` (doc concept) |
| Scheduled task / `/loop` | notes 6, 7 (doc concept/procedure) |
| Bare mode / Non-interactive mode (`claude -p`) | note 9 `cc_headless_mode` (doc concept; master assigns "Bare mode/Non-interactive mode → B11") |
| Desktop scheduled task | note 8 `cc_desktop_scheduled_tasks` (doc concept) |
| Cron expression | link `term_cron_expression` (exists) |
| MCP / connectors | link `term_mcp` (exists) — full digest owned by B08A |
| Permission mode | link `term_graduated_trust` (exists) — full digest owned by B05A |
| Sandbox / cloud environment / network access | owned by B12B (`claude-code-on-the-web`) / B05B — linked, not digested here |
| Worktree | link to B10B (`cc_worktrees`) — owned there |
| `/goal` | link to B10B — owned there |
| Channels | link to B08B — owned there |
| GitHub Actions / GitLab CI | owned by B13B — linked |
| Structured output | link `term_structured_output` (exists) |
| Agent SDK | owned by B19A — linked |
| Monitor tool / Bash background tool / `CronCreate` field detail | owned by B03B (`tools-reference`) — linked |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/code
for newly-surfaced non-glossary terms. Candidates surfaced — **"jitter"**, **"seven-day expiry"**,
**"stagger"**, **"`/fire` endpoint"**, **"`loop.md`"**, **"`SKILL.md` (scheduled-task on-disk)"**,
**"catch-up run"** — but each is a *Claude-Code-specific feature mechanic* fully defined inside its owning
B11 doc note (notes 6/7/8/4), NOT a reusable cross-domain vocabulary term that warrants a `term_dictionary`
note (and none has a glossary entry). Per the master's CC-specific design decision (vocabulary terms are
digested as doc-concept notes by their home sub-plan), **0 new B11 `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B11 authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the B11 page concepts duplicate existing notes?)
was performed: `term_cron_expression`, `term_mcp`, `term_graduated_trust`, `term_structured_output`,
`term_ci_cd`, `term_autonomous_coding_agents`, `term_agent_harness`, `term_claude_code`, `term_skills`,
`term_function_calling`, `term_context_engineering`, `term_subagent`, `term_agentic_memory` all exist →
linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B11** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8 discoverability) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (curl/json/cron/`-p` examples copied exactly from source). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_cron_expression.md` | notes 1, 6, 7 | cron term → scheduling comparison / `/loop` / cron-reference execution model |
| `term_dictionary/term_claude_code.md` | notes 1, 2, 9 | product term → scheduling hub / cloud routines / headless mode |
| `term_dictionary/term_autonomous_coding_agents.md` | notes 2, 3 | autonomous-agent term → routines overview + create (unattended runs) |
| `term_dictionary/term_ci_cd.md` | notes 4, 10 | CI/CD term → routine triggers (API/GitHub) + headless build-script/commit patterns |
| `term_dictionary/term_structured_output.md` | note 10 | structured-output term → `-p --output-format json --json-schema` examples |
| `term_dictionary/term_mcp.md` | note 5 | MCP term → routine connectors management |
| `term_dictionary/term_graduated_trust.md` | note 8 | trust term → per-task Desktop permission modes |
| `term_dictionary/term_subagent.md` | note 8 | isolation term → Desktop worktree-per-run toggle |

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and verify DB in-degree ≥1 for all 10 (G7/G8); queue the 10 rows for `entry_claude_code_docs.md` under an "Automation & Scheduling" cluster; `/tessellum-check-broken-links`.
- Add intra-cluster sibling links: note 1 ↔ notes 2/6/8 (the three options it compares); notes 9 ↔ 10 (headless pair); notes 2/3/4/5 (routines family).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B11, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/`; measured words match the master's figure (routines 4,085 · scheduled-tasks 2,216 · desktop-scheduled-tasks 1,537 · headless 2,068 = 9,906). No >1.5× under-estimate. Two density-driven splits forced and documented (routines >2,500w; headless >6 code blocks).
- **Notes**: 10 (concept 4, procedure 6) — matches master estimate exactly. Splits documented in Split Decisions.
- **Step 2d new-term scan**: feature mechanics surfaced (jitter, seven-day expiry, stagger, `/fire`, `loop.md`, on-disk `SKILL.md`, catch-up run) → all are CC-specific feature internals owned by their B11 doc note per Pattern B; **0 new B11 term captures**.
- **Dedup (Step 2b/G-B)**: confirmed no existing `cc_` scheduling/routines/headless doc note and no same-concept `term_dictionary` or `documentation/` note; documentation grep hits ruled out as keyword false-positives.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Section Coverage Map, Validation Scripts (bash), Density Re-Assessment, Inlinks table, G5 verification note.
- **28-item checklist**: PASS (term-note items N/A — B11 authors no terms; entry-point + undigested-terms inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present incl. G7/G8 discoverability (single phase). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B11 contributes 10 rows under an "Automation & Scheduling" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | Inherits the master Format Definition verbatim: YAML field order, `## Overview` opener, source-mirrored H2s, `## Related Notes` indexed links, `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | routines (>2,500w) split into 4; headless (>6 code) split into 2; all 10 notes 450–650w, ≤6 code — none borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | All 4 pages `wc -w` measured 2026-06-13: routines 4,085 · scheduled-tasks 2,216 · desktop-scheduled-tasks 1,537 · headless 2,068 = 9,906 = master figure. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B11 authors 0 term notes; Undigested Terms Plan routes all page terms (Step 2d documented); Authoring Requirements inherited from master. |
| CP9 | Term-slug specificity + collision audit / Discoverability (G7/G8) | ✅ PASS | 10.5f N/A (0 new slugs); 13-term collision check documented (all linked, not recreated). Inlinks table is executable and gives every one of the 10 notes ≥1 inbound link from outside `claude_code/` (G7/G8). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.

**Source**: https://code.claude.com/docs/en
**Last Updated**: 2026-06-13
**Status**: Active
