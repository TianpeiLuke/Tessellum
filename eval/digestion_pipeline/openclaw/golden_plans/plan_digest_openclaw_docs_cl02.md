---
title: Sub-Plan cl02 — OpenClaw Docs: CLI (clawbot, commitments, completion, config, configure, crestodian, cron)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/clawbot", "cli/commitments", "cli/completion", "cli/config", "cli/configure", "cli/crestodian", "cli/cron"]
---

# Sub-Plan cl02: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order, `## Overview` → body → `## Related Notes` → `## References` → footer), dedup-before-create, the 9-GATE table, cross-references, and the Undigested-Terms ownership decision are all inherited verbatim from the master; this file holds only the cl02-specific scope, measured source, planned notes, coverage map, and candidate cross-references.

## Scope

The 7 alphabetically-grouped `cli/c*` command-reference pages: the legacy `clawbot` alias namespace, inferred-follow-up `commitments`, shell `completion`, the non-interactive `config` editor (get/set/patch/unset/file/schema/validate), the interactive `configure` wizard, the configless-safe `crestodian` setup/repair helper, and the `cron` scheduler. **Priority P1 (Phase A)** — these are the operational core (config editing + scheduling + repair) that the rest of the OpenClaw docs reference. The code-side counterparts `repo_openclaw` / `repo_openclaw_cli_wizard` / `repo_openclaw_gateway` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 7,323 measured body words (8,323 total incl. frontmatter). **Planned: 9 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| clawbot | cli/clawbot | 72 | 0 | 2 | 0 | procedure |
| commitments | cli/commitments | 240 | 7 | 5 | 0 | procedure |
| completion | cli/completion | 169 | 1 | 4 | 0 | procedure |
| config | cli/config | 2,095 | 20 | 11 | 3 | procedure (split: edit vs validate/write-safety) |
| configure | cli/configure | 553 | 1 | 3 | 0 | procedure |
| crestodian | cli/crestodian | 1,553 | 14 | 9 | 0 | concept + procedure |
| cron | cli/cron | 2,400 | 15 | 11 | 11 | procedure (split: author/deliver vs run/admin) |

(Word counts are body-only via `sed -n '/^---$/,/^---$/!p' | wc -w`; H2/H3 via `grep -c '^## '` / `'^### '`. The page-1 `#` title is not counted as an H2.)

## Content Strategy

- **Prioritize**: the `config` get/set/patch/SecretRef-builder editing workflow and the `config` write-safety/validate/dry-run safety model (every operator change goes through these); the `cron` scheduling + delivery contract and the `cron` model/run/admin surface (the scheduler the rest of automation references); and the `crestodian` configless-safe security model (the repair surface for a broken gateway).
- **Split**: `config.md` (2,095w / 20 fences, mixed task clusters) → an editing-operations note + a validation/write-safety/dry-run note; `cron.md` (2,400w / 15 fences / 11 H2 / 11 H3, two task clusters) → a job-authoring/scheduling/delivery note + a model/run-output/retention/admin note. Both exceed the comfort band for one atomic note and mix distinct task clusters.
- **Keep 1 note**: `clawbot`, `commitments`, `completion`, `configure` (each well under caps); `crestodian` stays a single note (1,553w / 14 fences ≤ caps) because its TUI/safe-startup/approval/planner/rescue sections form one cohesive "configless-safe helper" concept — splitting would fragment the security contract.
- **Link-out (do NOT duplicate)**: the conceptual `commitments` guide (`/concepts/commitments`), `heartbeat` (`/gateway/heartbeat`), the cron conceptual guide (`/automation/cron-jobs`), gateway `configuration` reference (`/gateway/configuration`), `secretref-credential-surface` (`/reference/...`), `doctor`/`tui`/`sandbox`/`security` CLI siblings (cl03/cl06/cl07, this series), and `onboard`/`setup`/`channels` (cl05/cl07, this series) are cross-referenced as links, not re-documented here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_clawbot.md` | procedure | clawbot.md: full page (legacy alias namespace, Migration) | 250 | The `openclaw clawbot` legacy alias namespace kept for backward compatibility, its one surviving alias (`clawbot qr` → `qr`), and the migration guidance to modern top-level commands. |
| 2 | `oc_cli_commitments.md` | procedure | commitments.md: Usage, Options, Examples, Output | 380 | The `openclaw commitments` command to list and dismiss inferred follow-up commitments: subcommands (list/dismiss), filter options (`--all`/`--agent`/`--status`/`--json`), worked examples, and text vs JSON output fields. |
| 3 | `oc_cli_completion.md` | procedure | completion.md: Usage, Options, Notes | 320 | The `openclaw completion` command to generate and install shell completion scripts for zsh/bash/fish/PowerShell: shell target, `--install` profile injection, `--write-state` caching to `$OPENCLAW_STATE_DIR/completions`, and eager command-tree loading. |
| 4 | `oc_cli_config_edit.md` | procedure | config.md: Root options, Examples, `config schema`, Paths, Values, `config set` modes, `config patch`, Provider builder flags, Subcommands | 650 | Non-interactive editing of `openclaw.json`: dot/bracket paths, JSON5 values + `--strict-json`/`--merge`/`--replace`, `config set` four modes (value / SecretRef-builder / provider-builder / batch), `config patch`, provider-builder flags, `config schema`, and `config file`. |
| 5 | `oc_cli_config_validate.md` | procedure | config.md: Dry run (+ JSON output shape), Write safety, Validate, Nix-mode note | 550 | Validating and safely writing OpenClaw config: `--dry-run` (schema + SecretRef resolvability, `--allow-exec`, JSON report), `config validate`, write-safety (post-change validation, `.rejected.*` payloads, symlink/Nix-immutable restrictions), and the TUI-assisted repair loop. |
| 6 | `oc_cli_configure.md` | procedure | configure.md: full page (interactive prompts, Model/Web sections, Options, Examples) | 500 | The `openclaw configure` interactive wizard for targeted changes (credentials, model allowlist, web search, gateway, daemon, channels, plugins, skills, health): repeatable `--section` filters, model-allowlist merge semantics, provider-preference defaults, and daemon-install SecretRef guards. |
| 7 | `oc_cli_crestodian.md` | concept | crestodian.md: full page (What it shows, Safe startup, Operations/approval, Setup bootstrap, Model-Assisted Planner, Switching, Message rescue mode + security contract) | 700 | Crestodian, OpenClaw's configless-safe setup/repair helper that stays reachable when the agent path is broken: TUI startup probe, safe-startup conditions, typed read-only vs approval-gated operations, setup bootstrap backend selection, the bounded model-assisted planner, agent handoff, and the message-channel rescue-mode security contract. |
| 8 | `oc_cli_cron_jobs.md` | procedure | cron.md: Create jobs quickly (prompt/webhook/command), Sessions, Delivery (+ ownership, failure delivery), Scheduling (one-shot, recurring, manual runs), Common edits | 700 | Authoring `openclaw cron` jobs: `create`/`add` (prompt vs `--webhook` vs `--command`), session keys (main/isolated/current/session:id), delivery modes + ownership + failure-destination resolution, one-shot vs recurring (retry backoff) vs manual (`--wait`/`--due`) scheduling, and common edits. |
| 9 | `oc_cli_cron_run.md` | procedure | cron.md: Models (+ precedence, fast mode, switch retries), Run output and denials, Retention, Migrating older jobs, Common admin commands | 650 | Running and administering `openclaw cron` jobs: per-job model selection + isolated precedence + fast mode + live-switch retries, run-output handling (stale-ack suppression, silent-token suppression, structured denials), retention/pruning config, legacy-job migration via `doctor --fix`, and `list`/`get`/`show`/`run`/`runs` admin commands. |

## Section Coverage Map

```
clawbot.md
├── (intro: legacy alias namespace, clawbot qr) ──── → note 1 (oc_cli_clawbot)
├── ## Migration ──────────────────────────────────── → note 1
└── ## Related ─────────────────────────────────────── → note 1 (References)
commitments.md
├── (intro: opt-in short-lived follow-ups) ────────── → note 2 (oc_cli_commitments)
├── ## Usage ───────────────────────────────────────── → note 2
├── ## Options ─────────────────────────────────────── → note 2
├── ## Examples ────────────────────────────────────── → note 2
├── ## Output ──────────────────────────────────────── → note 2
└── ## Related ─────────────────────────────────────── → note 2 (References + link concepts/commitments, gateway/heartbeat, automation/cron-jobs)
completion.md
├── (intro: generate/install completion scripts) ──── → note 3 (oc_cli_completion)
├── ## Usage ───────────────────────────────────────── → note 3
├── ## Options ─────────────────────────────────────── → note 3
├── ## Notes ───────────────────────────────────────── → note 3
└── ## Related ─────────────────────────────────────── → note 3 (References)
config.md
├── (intro + Nix-mode immutability Note) ──────────── → note 4 (oc_cli_config_edit) [Nix immutability also referenced in note 5 Write safety]
├── ## Root options ────────────────────────────────── → note 4
├── ## Examples ────────────────────────────────────── → note 4
├── ### config schema ──────────────────────────────── → note 4
├── ### Paths ──────────────────────────────────────── → note 4
├── ## Values ──────────────────────────────────────── → note 4
├── ## config set modes ────────────────────────────── → note 4
├── ## config patch ────────────────────────────────── → note 4
├── ## Provider builder flags ──────────────────────── → note 4
├── ## Dry run (+ ### JSON output shape) ───────────── → note 5 (oc_cli_config_validate)
├── ## Write safety ────────────────────────────────── → note 5
├── ## Subcommands (config file) ───────────────────── → note 4
├── ## Validate ────────────────────────────────────── → note 5
└── ## Related ─────────────────────────────────────── → notes 4 + 5 (References)
configure.md
├── (intro + Model/Web Notes + Tip + provider follow-ups) → note 6 (oc_cli_configure)
├── ## Options (sections) ──────────────────────────── → note 6
├── ## Examples ────────────────────────────────────── → note 6
└── ## Related ─────────────────────────────────────── → note 6 (References)
crestodian.md
├── (intro: local setup/repair helper, bare-openclaw behavior) → note 7 (oc_cli_crestodian)
├── ## What Crestodian shows ───────────────────────── → note 7
├── ## Examples ────────────────────────────────────── → note 7
├── ## Safe startup ────────────────────────────────── → note 7
├── ## Operations and approval ─────────────────────── → note 7
├── ## Setup bootstrap ─────────────────────────────── → note 7
├── ## Model-Assisted Planner ──────────────────────── → note 7
├── ## Switching to an agent ───────────────────────── → note 7
├── ## Message rescue mode (+ security contract, config shape, test lanes) → note 7
└── ## Related ─────────────────────────────────────── → note 7 (References)
cron.md
├── (intro + Tip → automation/cron-jobs) ──────────── → note 8 (oc_cli_cron_jobs)
├── ## Create jobs quickly ─────────────────────────── → note 8
├── ## Sessions (### keys, ### isolated semantics) ── → note 8
├── ## Delivery (### ownership, ### failure delivery) → note 8
├── ## Scheduling (### one-shot, ### recurring, ### manual runs) → note 8
├── ## Models (### precedence, ### fast mode, ### switch retries) → note 9 (oc_cli_cron_run)
├── ## Run output and denials (### stale-ack, ### silent-token, ### structured denials) → note 9
├── ## Retention ───────────────────────────────────── → note 9
├── ## Migrating older jobs ────────────────────────── → note 9
├── ## Common edits ────────────────────────────────── → note 8
├── ## Common admin commands ───────────────────────── → note 9
└── ## Related ─────────────────────────────────────── → notes 8 + 9 (References)
```
No orphaned sections. The `config` Nix-immutability Note is primarily mapped to note 4 (edit refusal) and referenced again in note 5's Write-safety context. The `cron` "Common edits" section is delivery/scheduling edits → note 8; "Common admin commands" (list/get/show/run/runs + retargeting) → note 9. Conceptual guides (`concepts/commitments`, `automation/cron-jobs`, `gateway/heartbeat`, `gateway/configuration`, `reference/secretref-credential-surface`) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| config.md (2,095w, 20 fences, 11 H2 / 3 H3) | notes 4 + 5 | Two distinct task clusters: (a) editing config (paths/values/`set` modes/`patch`/provider-builder/`schema`) vs (b) validating & safely writing config (`--dry-run` + JSON report, write-safety/`.rejected.*`, `validate`, TUI repair loop). Splitting keeps each ≤650w / ≤6 fences and one focused procedure. |
| cron.md (2,400w, 15 fences, 11 H2 / 11 H3) | notes 8 + 9 | Exceeds 2,500w-comfort band with 22 headings spanning two task clusters: (a) authoring/scheduling/delivering jobs (create/sessions/delivery/scheduling/common-edits) vs (b) running & administering them (models/run-output+denials/retention/migration/admin commands). Split per word-cap + mixed-task-cluster rules; each note ≤700w / ≤6 fences. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (7,323 body words). New `oc_` notes: **9**. New `term_dictionary` notes: 0 (expected).
- BB distribution: procedure ×8 (notes 1–6, 8–9) · concept ×1 (note 7, crestodian — the configless-safe-helper architecture/security model).
- Est. digest words ~4,700 (avg ~520/note); all ≤700w, well under the 2,500w / 400-line cap.
- Code-block budget: the 58 source fences (0/7/1/20/1/14/15) are reproduced selectively and verbatim, each note kept ≤6. The two split pages (config 20, cron 15) are the reason for splitting so each child stays ≤6.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


> Plan-stage substitutions corrected at augment: `term_json_schema` EXISTS (plan said MISSING) — used directly in notes 4/5; `term_audit_operations` EXISTS (plan flagged DB-verify) — used in notes 5/7/9; `term_idempotency` + `term_idempotency_key` both EXIST; `term_session_persistence` EXISTS (used for the SQLite-state link in note 9, since `term_sqlite` is MISSING). Still MISSING and substituted: `term_command_line_interface` / `term_environment_variable` / `term_session` / `term_backward_compatibility` / `term_scheduler` / `term_sqlite`.

### oc_cli_clawbot (8t · 10s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway whose CLI this command belongs to; relevance: `openclaw clawbot` is one namespace of the OpenClaw CLI.
- [OpenShell](../../term_dictionary/term_openshell.md) — OpenClaw's shell/terminal surface; relevance: substitutes for the MISSING `term_command_line_interface` as the CLI-surface concept the alias resolves on.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the harness the CLI drives; relevance: top-level commands the alias forwards to drive the harness.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class OpenClaw fronts; relevance: the CLI is the operator entrypoint to these agents.
- [Idempotency](../../term_dictionary/term_idempotency.md) — stable-output property; relevance: substitutes for MISSING `term_backward_compatibility` — a kept alias must resolve identically to its modern target (`clawbot qr` == `qr`).
- [Claude Code](../../term_dictionary/term_claude_code.md) — sibling coding-agent CLI; relevance: cross-tool reference for how a coding-agent CLI keeps deprecated-but-supported aliases.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the command/tool registration surface; relevance: aliases are registered entries in the command tree that map to canonical commands.

**Docs** (≥10):
- [Claude Code CLI Commands](../claude_code/cc_cli_commands.md) — the cc CLI command reference; relevance: sibling-tool model for a top-level command namespace and its surviving aliases.
- [Claude Code CLI Flags](../claude_code/cc_cli_flags.md) — cc flag reference; relevance: shows how a coding-agent CLI documents legacy vs current flags/commands.
- [Pi CLI Reference](../pi/pi_cli_reference.md) — Pi's CLI command surface; relevance: parallel sibling-tool CLI reference for command/alias layout.
- [Hermes CLI Interface](../hermes_agent/hermes_cli_interface.md) — Hermes CLI command structure; relevance: ecosystem-cousin CLI namespace model.
- [Hermes Profile Commands Reference](../hermes_agent/hermes_profile_commands_reference.md) — Hermes command reference; relevance: shows command-namespace organization in the same agent family.
- [Hermes Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — OpenClaw→Hermes migration guide; relevance: the migration-guidance pattern this note's Migration section mirrors.
- [Claude Code Commands Reference](../claude_code/cc_commands_reference.md) — cc slash/CLI command catalog; relevance: catalog precedent for how the full command surface (where the alias forwards) is enumerated.
- [Pi Interactive Usage](../pi/pi_interactive_usage.md) — Pi interactive command usage; relevance: shows the modern top-level commands an operator should prefer over legacy aliases.
- [oc_cli_completion](oc_cli_completion.md) — (planned, this series) the shell-completion command; relevance: both are thin utility commands in the same cl02 cluster, and completion enumerates the very alias namespace this note documents.
- [oc_cli_crestodian](oc_cli_crestodian.md) — (planned, this series) bare-`openclaw` routing helper; relevance: the no-command/legacy-routing behavior is the sibling concern to a legacy alias namespace.

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the CLI host repo; relevance: the `clawbot` alias is registered in this codebase's command tree.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the CLI command-tree/wizard repo; relevance: alias registration + command routing live here.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command/alias registry; relevance: the alias namespace is an entry in this catalog.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — top-level command routing; relevance: how `clawbot qr` routes to the canonical `qr` command.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — bare/root command guard; relevance: same router layer that resolves legacy aliases.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: where the command tree (incl. aliases) is built at startup.
- [snippet_hermes_agent_cli_main_argparse_root](../../code_snippets/snippet_hermes_agent_cli_main_argparse_root.md) — root argparse/command tree; relevance: sibling-tool model for registering top-level commands + aliases.
- [snippet_hermes_agent_cli_inventory](../../code_snippets/snippet_hermes_agent_cli_inventory.md) — CLI command inventory; relevance: shows enumerating the full command surface a legacy alias forwards into.
- [snippet_hermes_agent_cli_dump](../../code_snippets/snippet_hermes_agent_cli_dump.md) — CLI command dump; relevance: command-tree introspection comparable to listing aliases.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI→gateway dispatch; relevance: how a CLI subcommand (alias or canonical) dispatches to the runtime.
- [snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md) — CLI subcommand switch logic; relevance: command-dispatch switch pattern aliases hook into.
- [snippet_hermes_agent_cli_main_cmd_chat](../../code_snippets/snippet_hermes_agent_cli_main_cmd_chat.md) — a concrete CLI subcommand impl; relevance: example of the canonical command an alias resolves to.

### oc_cli_commitments (8t · 10s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw commitments` is its follow-up-management command.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — the gateway wakeup/check-in mechanism; relevance: commitments are what heartbeat may deliver (the page's "auditing what heartbeat may deliver" use-case).
- [Commitment Device](../../term_dictionary/term_commitment_device.md) — the precommitment concept; relevance: inferred commitments are the agentic analog — short-lived precommitted follow-ups.
- [Compaction](../../term_dictionary/term_compaction.md) — conversation memory compaction; relevance: commitments are short-lived memories distilled from conversation context.
- [Session Data](../../term_dictionary/term_session_data.md) — per-agent session scope; relevance: substitutes MISSING `term_session` — commitments are scoped per agent/session and `--agent` filters them.
- [Cron](../../term_dictionary/term_cron.md) — the scheduler; relevance: scheduled check-in delivery is the cron analog of a due commitment.
- [Open Loops](../../term_dictionary/term_open_loops.md) — unresolved follow-up threads; relevance: commitments are exactly the open-loop / pending check-in the agent tracks.
- [Persistent Goal](../../term_dictionary/term_persistent_goal.md) — standing agent objective; relevance: a commitment is a lightweight, expiring standing follow-up the agent will revisit.

**Docs** (≥10):
- [Pi Sessions](../pi/pi_sessions.md) — Pi session-scoped state; relevance: commitments are session/agent-scoped records, the same lifecycle concern.
- [Claude Code Sessions](../claude_code/cc_sessions.md) — cc session model; relevance: follow-ups attach to a session the way cc tracks per-session state.
- [Claude Code SDK Sessions Overview](../claude_code/cc_sdk_sessions_overview.md) — session lifecycle in cc SDK; relevance: scope/expiry parallels for short-lived per-session records.
- [Hermes Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle; relevance: status transitions (pending/sent/dismissed/expired) mirror session-lifecycle states.
- [Hermes Session Search & Storage](../hermes_agent/hermes_session_search_storage.md) — session storage backend; relevance: commitments have a store path (the page's JSON output exposes it).
- [Hermes Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — scheduled-job semantics; relevance: due-time + delivery of a commitment is the cron-scheduling analog.
- [Hermes Guide: Daily Briefing Bot](../hermes_agent/hermes_guide_daily_briefing_bot.md) — scheduled check-in bot; relevance: a concrete "scheduled follow-up delivered to chat" workflow.
- [Band Agent API: Context & Activity](../band/band_agent_api_context_activity.md) — agent activity/context records; relevance: cross-framework model for tracking inferred follow-up activity items.
- [oc_cli_cron_jobs](oc_cli_cron_jobs.md) — (planned, this series) cron authoring; relevance: scheduled-delivery analog; the page's Related links to `/automation/cron-jobs`.
- [oc_cli_crestodian](oc_cli_crestodian.md) — (planned, this series) repair helper; relevance: cl02 sibling sharing the CLI-inspection surface.

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI host; relevance: the `commitments` command lives here.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the memory subsystem; relevance: commitments are conversation-derived memories backed by the memory store.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway/heartbeat host; relevance: heartbeat (delivery of due commitments) runs in the gateway.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delivery path; relevance: the delivery channel a due commitment rides.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine internals; relevance: commitments are stored/retrieved via the memory engine.
- [snippet_openclaw_memory_host_session_files_text](../../code_snippets/snippet_openclaw_memory_host_session_files_text.md) — session-scoped memory files; relevance: the per-session store backing commitment records.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunking; relevance: commitments are derived during conversation compaction.
- [snippet_hermes_agent_honcho_session_messages](../../code_snippets/snippet_hermes_agent_honcho_session_messages.md) — session message store; relevance: sibling model for per-session message-derived records.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat session persistence; relevance: persists the session context commitments are inferred from.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command/subcommand catalog; relevance: `commitments list`/`dismiss` subcommands register here.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — command routing; relevance: routes the `commitments` subcommands.
- [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — due-time/scheduling helpers; relevance: due-time resolution comparable to commitment "earliest due time".
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery dispatch; relevance: how a due follow-up is delivered to a chat target.

### oc_cli_completion (8t · 10s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw completion` generates its shell-completion scripts.
- [OpenShell](../../term_dictionary/term_openshell.md) — OpenClaw's shell surface; relevance: completions install into the shell profile this manages.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config/state model; relevance: substitutes MISSING `term_environment_variable` — `$OPENCLAW_STATE_DIR/completions` is part of the state/config layout.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-run-safe property; relevance: `--install` writes a single completion block idempotently into the profile.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — command/tool registration; relevance: completion eagerly loads the command tree (the tool/command registry) to enumerate nested subcommands.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the harness the CLI drives; relevance: completion covers the harness-driving command surface.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class; relevance: completion is operator ergonomics for driving these agents from the shell.

**Docs** (≥10):
- [Claude Code CLI Commands](../claude_code/cc_cli_commands.md) — cc command reference; relevance: the command tree completion must enumerate, sibling-tool form.
- [Claude Code CLI Flags](../claude_code/cc_cli_flags.md) — cc flag reference; relevance: completion offers flag suggestions; this is the flag surface.
- [Pi Terminal Setup](../pi/pi_terminal_setup.md) — Pi terminal/shell setup; relevance: closest sibling-tool analog for shell-integration/profile setup.
- [Claude Code Terminal Configuration](../claude_code/cc_terminal_configuration.md) — cc terminal config; relevance: shell-profile integration parallel (zsh/bash/fish).
- [Claude Code Statusline Setup](../claude_code/cc_statusline_setup.md) — cc shell-profile statusline install; relevance: another "write a block into your shell profile" install pattern.
- [Hermes Terminal Backends](../hermes_agent/hermes_terminal_backends.md) — Hermes terminal backends; relevance: shell/terminal target variety (zsh/bash/fish/PowerShell).
- [Pi Platform: Windows/Termux](../pi/pi_platform_windows_termux.md) — Pi shell on Windows/Termux; relevance: PowerShell completion target parallel.
- [Claude Code Quickstart](../claude_code/cc_quickstart.md) — cc first-run setup; relevance: shell-completion install is part of first-run ergonomics.
- [oc_cli_clawbot](oc_cli_clawbot.md) — (planned, this series) thin utility command; relevance: same cl02 utility-command cluster; both touch the command catalog.
- [oc_cli_configure](oc_cli_configure.md) — (planned, this series) interactive setup; relevance: both write into operator-local files (profile vs config) with confirm prompts (`-y/--yes`).

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI host; relevance: the `completion` command lives here.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI command-tree/wizard; relevance: completion eagerly loads this command tree.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — command catalog; relevance: completion enumerates exactly this catalog.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — command routing; relevance: nested-subcommand routing completion must reflect.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: eager command-tree load happens at this bootstrap.
- [snippet_hermes_agent_cli_main_argparse_root](../../code_snippets/snippet_hermes_agent_cli_main_argparse_root.md) — root argparse tree; relevance: sibling model for the command tree completion walks.
- [snippet_hermes_agent_cli_inventory](../../code_snippets/snippet_hermes_agent_cli_inventory.md) — command inventory; relevance: full command enumeration completion needs.
- [snippet_hermes_agent_cli_dump](../../code_snippets/snippet_hermes_agent_cli_dump.md) — command dump; relevance: introspection of the command tree to generate completions.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive prompter; relevance: the `--install` confirmation prompt (`-y/--yes` skip) uses this prompter layer.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer that writes shell/profile artifacts; relevance: model for `--install` writing a block into the shell profile.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup module imports; relevance: where state-dir paths (`$OPENCLAW_STATE_DIR`) are resolved for `--write-state`.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — CLI dispatch; relevance: command dispatch the completion tree mirrors.

### oc_cli_config_edit (9t · 11s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: edits `openclaw.json`, OpenClaw's config file.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — the config object; relevance: paths/values/`set`/`patch` all mutate this model.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential/secret management; relevance: SecretRef-builder + provider-builder modes write credential refs, not plaintext.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema definition (EXISTS; plan said MISSING); relevance: `config schema` prints the generated JSON schema for `openclaw.json`.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — the runtime RPC protocol; relevance: `config.schema.lookup` is the runtime RPC the doc references for path-scoped schema drill-down.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/secret-provider plugins; relevance: provider-builder mode targets `secrets.providers.<alias>` (env/file/exec providers).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token credentials; relevance: token SecretRefs (e.g. `channels.discord.token`) are the canonical builder-mode example.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP/plugin config blocks are edited through these same paths.
- [Idempotency](../../term_dictionary/term_idempotency.md) — re-run-safe / no-clobber; relevance: `--merge` vs `--replace` and protected-map refusal keep edits non-destructive.

**Docs** (≥10):
- [Claude Code Settings Files](../claude_code/cc_settings_files.md) — cc config-file editing; relevance: sibling-tool model for non-interactive settings-file edits.
- [Claude Code Settings Reference](../claude_code/cc_settings_reference.md) — cc settings keys; relevance: dotted-path settings model paralleling OpenClaw config paths.
- [Claude Code Environment Variables](../claude_code/cc_environment_variables.md) — cc env vars; relevance: env-sourced credentials parallel `--ref-source env` SecretRefs.
- [Pi Settings Reference](../pi/pi_settings_reference.md) — Pi config schema/keys; relevance: config-schema analog for path/value editing.
- [Hermes Config Files & Precedence](../hermes_agent/hermes_config_files_precedence.md) — config file layering; relevance: config-file resolution (`OPENCLAW_CONFIG_PATH`) precedent.
- [Hermes Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential pool config; relevance: provider-builder `secrets.providers.*` is the credential-pool surface.
- [Hermes Env Vars: Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: env-backed provider secrets edited via builder mode.
- [Claude Code Server-Managed Settings](../claude_code/cc_server_managed_settings.md) — managed/immutable settings; relevance: parallels the `OPENCLAW_NIX_MODE=1` immutable-config refusal.
- [oc_cli_config_validate](oc_cli_config_validate.md) — (planned, this series) the validation/write-safety half; relevance: edits made here are validated/dry-run there.
- [oc_cli_configure](oc_cli_configure.md) — (planned, this series) the interactive wizard; relevance: `config` without a subcommand opens the same wizard.

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — config-writer host; relevance: `config set/patch/unset` writers live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — consumes the config; relevance: the gateway reads the edited `openclaw.json` and hot-reloads.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider entries; relevance: `models.providers.*` / `agents.defaults.models` edits target these.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config shape; relevance: the `agents.defaults.*` structure these paths write.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolution; relevance: the resolution model behind builder-mode SecretRefs.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: `auth.profiles` is a protected map edited here.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `config set` impl; relevance: sibling implementation of path-based config set.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config loading; relevance: how edited config is reloaded.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway config schema; relevance: the schema `config schema` emits.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config in the server; relevance: `plugins.entries.*` edits this surface.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution (env/file/exec); relevance: maps to provider-builder `--provider-source env|file|exec`.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete provider entry; relevance: example of a `models.providers.*` block edited via config.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider entry; relevance: `models.providers.ollama.models` `--merge` example from the page.

### oc_cli_config_validate (9t · 10s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: validates/safely writes `openclaw.json`.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — the config validated; relevance: `config validate` checks the full post-change config shape.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation (EXISTS); relevance: dry-run + validate run schema validation against the active schema.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — the RPC layer; relevance: `--dry-run --json` emits a structured RPC-shaped report (ok/operations/checks/errors).
- [Idempotency](../../term_dictionary/term_idempotency.md) — no-clobber property; relevance: rejected payloads are saved as `openclaw.json.rejected.*` while the active config is left untouched.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret resolution; relevance: dry-run runs SecretRef resolvability checks (`--allow-exec` for exec refs).
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — write/operation logging (EXISTS; plan flagged DB-verify); relevance: rejected-write payloads + doctor-repair recovery form the write-safety audit trail.
- [Retry Pattern](../../term_dictionary/term_retry_pattern.md) — repair/retry loop; relevance: the documented compare→edit→re-validate→doctor repair loop.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — exec/file/env providers; relevance: exec SecretRef provider checks (skipped unless `--allow-exec`).

**Docs** (≥10):
- [Claude Code Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — cc config validation/repair; relevance: the closest sibling-tool validate-and-repair workflow.
- [Pi Settings Reference](../pi/pi_settings_reference.md) — Pi config schema; relevance: schema-validation analog.
- [Claude Code Settings Files](../claude_code/cc_settings_files.md) — cc settings-file model; relevance: the file being validated/safely written.
- [Hermes Config Files & Precedence](../hermes_agent/hermes_config_files_precedence.md) — config resolution; relevance: which file `config file` resolves and validates.
- [Claude Code Login/Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth/credential failure repair; relevance: SecretRef-resolvability failures and their remediation.
- [Hermes Guide: Cron Troubleshooting](../hermes_agent/hermes_guide_cron_troubleshooting.md) — config-driven failure diagnosis; relevance: the validate→fix loop pattern applied to runtime config issues.
- [Hermes Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway runtime ops; relevance: the gateway treats direct edits as untrusted until they validate (hot-reload skip / startup fail).
- [Claude Code Server-Managed Settings](../claude_code/cc_server_managed_settings.md) — immutable/managed config; relevance: the Nix-immutable write-refusal restriction.
- [oc_cli_config_edit](oc_cli_config_edit.md) — (planned, this series) the editing half; relevance: edits validated here; `--dry-run` is shared.
- [oc_cli_crestodian](oc_cli_crestodian.md) — (planned, this series) `doctor --fix`/repair surface; relevance: the TUI-assisted repair loop and whole-file recovery route through Crestodian/doctor.

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — config writer + validator; relevance: write-safety + `validate` live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — treats direct edits as untrusted until validated; relevance: hot-reload/startup validation behavior.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — write-safety/SecretRef policy; relevance: unsupported-SecretRef-surface policy + rejected-payload handling.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolvability; relevance: the resolvability check dry-run runs.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway config schema; relevance: the schema validation checks against.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — config loading/validation; relevance: post-change validation before commit.
- [snippet_hermes_agent_cli_model_switch_validate](../../code_snippets/snippet_hermes_agent_cli_model_switch_validate.md) — validation pre-commit; relevance: validate-before-apply pattern.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin/min-host-version trust; relevance: `minHostVersion` skew stays loud (page's write-safety note).
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit-record composition; relevance: rejected-write/repair audit trail.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config/plugin load; relevance: invalid direct edits are skipped by hot reload here.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: exec/file/env resolvability paths exercised by `--allow-exec`.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — fallback context on invalid config; relevance: how the gateway behaves when config fails validation.

### oc_cli_configure (8t · 10s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw configure` is its interactive setup wizard.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — what the wizard writes; relevance: configure writes through typed config operations.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the model allowlist/catalog; relevance: the Model section multi-selects `agents.defaults.models` (what shows in `/model`).
- [Model Router](../../term_dictionary/term_model_router.md) — default-model selection/routing; relevance: provider-preference defaults + preserving `model.primary` on re-auth.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret/SecretRef validation; relevance: daemon-install token must be a resolvable SecretRef.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — provider auth/token; relevance: provider auth sections (Grok/xAI OAuth, Kimi/Moonshot key) prompt for tokens.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugins; relevance: provider-scoped setup merges that provider's models into the allowlist.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored auth profile; relevance: re-running provider auth from configure manages auth profiles without clobbering the primary.

**Docs** (≥10):
- [Pi Provider Auth](../pi/pi_provider_auth.md) — Pi interactive provider auth; relevance: the closest sibling-tool interactive provider-auth flow.
- [Claude Code Settings Files](../claude_code/cc_settings_files.md) — cc config setup; relevance: configure's targeted-section edits write the same settings surface.
- [Hermes Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — provider onboarding; relevance: the provider-auth section's merge-into-allowlist behavior.
- [Hermes Env Vars: Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env; relevance: token vs key prompts and their env-backing.
- [Hermes Provider: xAI/Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — Grok/xAI OAuth setup; relevance: the page's Grok `x_search` + xAI OAuth follow-up prompts.
- [Hermes Provider: MiniMax OAuth](../hermes_agent/hermes_provider_minimax_oauth.md) — provider OAuth follow-ups; relevance: provider-specific follow-up-prompt pattern (region/model picks) like Kimi/Moonshot.
- [Claude Code Login/Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth setup/repair; relevance: daemon-install token-SecretRef remediation guidance.
- [Hermes Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential config; relevance: daemon `gateway.auth.token` SecretRef management.
- [oc_cli_config_edit](oc_cli_config_edit.md) — (planned, this series) `config get|set|unset`; relevance: the non-interactive analog (`config` w/o subcommand opens this wizard).
- [oc_cli_crestodian](oc_cli_crestodian.md) — (planned, this series) chat-first setup; relevance: Crestodian `setup` is the chat-first analog to `configure`'s interactive setup.

**Repos**:
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the wizard implementation; relevance: closest repo — `configure` is implemented here.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI host; relevance: `configure` is dispatched from the CLI.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider auth choices; relevance: provider sections drive these provider plugins.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup-config writer; relevance: the core of `configure`'s typed-config writes.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive prompter; relevance: the prompt/multi-select UI the wizard uses.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard module wiring; relevance: how the section filters/handlers are composed.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — wizard migration/import; relevance: configure installs downloadable plugins after local config writes.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent-defaults config; relevance: the `agents.defaults.model*` the Model section writes.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode guards; relevance: the daemon-install token/password/mode validation the page describes.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth auth-profile portability; relevance: re-auth preserves the primary while adding provider auth.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — sibling setup wizard; relevance: cross-tool model for a sectioned interactive wizard.
- [snippet_hermes_agent_cli_main_provider_flows](../../code_snippets/snippet_hermes_agent_cli_main_provider_flows.md) — provider auth flows; relevance: provider-auth section prompts + default-model selection.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback handling; relevance: the OAuth profile flow Grok/xAI auth uses.

### oc_cli_crestodian (10t · 12s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: Crestodian is its configless-safe setup/repair helper (bare-`openclaw` lands here).
- [Sandbox](../../term_dictionary/term_sandbox.md) — sandboxing posture; relevance: remote rescue is disabled when sandboxing is active; the `auto` posture requires sandbox `off` (YOLO).
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the sandbox runtime; relevance: the YOLO posture (`sandbox=off`, `exec.security=full`) is a sandbox-backend resolution.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — applied-op logging (EXISTS); relevance: applied writes go to `~/.openclaw/audit/crestodian.jsonl` with before/after config hashes.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret handling; relevance: `config set-ref` sets SecretRefs and rescue reports availability, never echoes secret values.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — typed config ops; relevance: Crestodian uses typed operations instead of editing config ad hoc.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the broken agent path Crestodian bypasses; relevance: it stays reachable when the normal agent path is dead.
- [LLM](../../term_dictionary/term_llm.md) — the model; relevance: the model-assisted planner makes one bounded planner turn through a model.
- [Claude](../../term_dictionary/term_claude.md) — Claude Code CLI fallback; relevance: `claude-cli/claude-opus-4-8` is a planner/setup fallback backend.
- [Webhook](../../term_dictionary/term_webhook.md) — webhook channels; relevance: rescue must refuse unauthenticated webhooks/anonymous channels.

**Docs** (≥10):
- [Pi Security Model](../pi/pi_security_model.md) — Pi security/repair model; relevance: closest sibling-tool security model for a privileged repair surface.
- [Claude Code Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — cc config repair; relevance: the doctor/validate/repair operations Crestodian exposes.
- [Claude Code Security Architecture](../claude_code/cc_security_architecture.md) — cc security model; relevance: the read-only-vs-approval-gated operation split and trust boundaries.
- [Claude Code Sandbox Modes](../claude_code/cc_sandbox_modes.md) — cc sandbox modes; relevance: the sandbox-active rescue denial + YOLO/off posture.
- [Claude Code Prompt Injection Defenses](../claude_code/cc_prompt_injection_defenses.md) — cc untrusted-input defenses; relevance: keeping remote rescue deterministic so a compromised agent path can't be a config editor.
- [Hermes Security: Isolation & Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — Hermes isolation/credential security; relevance: never-echo-secrets + owner-identity-required rescue contract.
- [Hermes Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — gateway ops; relevance: "if Gateway alive, prefer Gateway typed operations" branch.
- [Pi Custom Provider Registration](../pi/pi_custom_provider_registration.md) — provider/backend setup; relevance: setup-bootstrap backend selection order (OpenAI/Anthropic/Claude CLI/Codex).
- [oc_cli_config_validate](oc_cli_config_validate.md) — (planned, this series) `doctor`/`validate config`; relevance: Crestodian surfaces these typed config ops.
- [oc_cli_configure](oc_cli_configure.md) — (planned, this series) setup analog; relevance: `setup` is Crestodian's chat-first version of `configure`.

**Repos**:
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — Crestodian host + bare-`openclaw` routing; relevance: the no-command entrypoint and TUI live here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — rescue security contract; relevance: sandbox-denial, owner-identity, audit, never-echo rules.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway reachability/typed operations; relevance: Crestodian probes Gateway and prefers its typed ops.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — setup bootstrap; relevance: `setup`/onboarding bootstrap shares wizard machinery.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — bare-`openclaw` no-command routing; relevance: the root guard that starts Crestodian when config has authored settings.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: the safe-startup path (`--help`/`--version` fast paths, noninteractive exit message).
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef inspection; relevance: report availability without echoing values.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit-log composition; relevance: `crestodian.jsonl` audit entries with config hashes.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: auditing applied/persistent operations only (discovery not audited).
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-op denial; relevance: rescue refusing sandboxed/unauthenticated operations.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: plugin install is local-only by default (downloads executable code).
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway entry dispatch; relevance: "prefer Gateway typed operations when alive" routing.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup-config writer; relevance: `setup` bootstrap writes config through typed ops.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval-gating policy; relevance: persistent ops require conversational approval (`--yes` to bypass).
- [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval roundtrip UI; relevance: the `/crestodian yes` rescue approval roundtrip.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic backend setup; relevance: `ANTHROPIC_API_KEY → anthropic/claude-opus-4-8` setup-bootstrap order.

### oc_cli_cron_jobs (8t · 12s · 11d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw cron` manages jobs for its Gateway scheduler.
- [Cron](../../term_dictionary/term_cron.md) — the scheduler concept; relevance: this command authors cron jobs (create/add).
- [Cron Expression](../../term_dictionary/term_cron_expression.md) — the schedule syntax; relevance: jobs take a `"0 7 * * *"` cron expression as the first arg.
- [Webhook](../../term_dictionary/term_webhook.md) — webhook delivery; relevance: `--webhook <url>` POSTs the finished payload instead of chat delivery.
- [Session Data](../../term_dictionary/term_session_data.md) — session scope; relevance: substitutes MISSING `term_session` — `--session main|isolated|current|session:<id>` keys.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — retry backoff; relevance: recurring jobs back off 30s→1m→5m→15m→60m after consecutive errors.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — wakeup/scheduled delivery; relevance: cron is the "scheduled jobs and wakeups" surface (page's read_when).
- [Idempotency](../../term_dictionary/term_idempotency.md) — run-once semantics; relevance: one-shot jobs delete-after-success unless `--keep-after-run`.

**Docs** (≥10):
- [Hermes Cron Scheduling](../hermes_agent/hermes_cron_scheduling.md) — cron schedule authoring; relevance: the closest sibling model for one-shot vs recurring scheduling.
- [Hermes Cron Advanced Jobs](../hermes_agent/hermes_cron_advanced_jobs.md) — advanced cron jobs; relevance: command jobs, webhook delivery, isolated sessions.
- [Hermes Guide: GitHub PR Review Cron](../hermes_agent/hermes_guide_github_pr_review_cron.md) — a concrete cron job; relevance: end-to-end authored job with delivery target.
- [Hermes Guide: Daily Briefing Bot](../hermes_agent/hermes_guide_daily_briefing_bot.md) — scheduled briefing; relevance: the morning-brief job archetype the page's examples show.
- [Claude Code Create Routine](../claude_code/cc_create_routine.md) — cc routine creation; relevance: sibling-tool "create a scheduled job" authoring flow.
- [Claude Code Scheduled Task Execution Model](../claude_code/cc_scheduled_task_execution_model.md) — cc scheduled-task model; relevance: session/delivery semantics of a scheduled run.
- [EventBridge Scheduler Overview](../aws_eventbridge/eventbridge_scheduler_overview.md) — managed scheduler model; relevance: one-shot vs recurring + delivery-target concepts in a managed scheduler.
- [EventBridge Scheduler Create](../aws_eventbridge/eventbridge_scheduler_create.md) — creating a schedule; relevance: managed-scheduler analog of `cron create` (schedule + target + payload).
- [oc_cli_cron_run](oc_cli_cron_run.md) — (planned, this series) the run/admin half; relevance: jobs authored here are run/administered there.
- [oc_cli_commitments](oc_cli_commitments.md) — (planned, this series) inferred follow-ups; relevance: scheduled-follow-up analog (both deliver due items to chat).
- [oc_cli_crestodian](oc_cli_crestodian.md) — (planned, this series) admin/repair surface; relevance: command cron jobs require `operator.admin`, the admin posture Crestodian gates.

**Repos**:
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the Gateway scheduler; relevance: scheduled runs execute in the Gateway process.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI host; relevance: `cron create/add/edit` dispatched from the CLI.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel delivery routing; relevance: announce/`--channel`/`--to` resolve to channel targets here.

**Snippets** (≥10, all EXISTING):
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + delivery notifications; relevance: the scheduler service that runs jobs + announce/webhook delivery.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — job create/edit/remove; relevance: the `cron create`/`add`/`edit` CRUD surface.
- [snippet_hermes_agent_cron_job_schema](../../code_snippets/snippet_hermes_agent_cron_job_schema.md) — job schema/fields; relevance: delivery mode, session key, webhook fields stored per job.
- [snippet_hermes_agent_cron_job_validate](../../code_snippets/snippet_hermes_agent_cron_job_validate.md) — job validation; relevance: rejecting `--webhook` combined with chat-delivery flags.
- [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — cron CLI command; relevance: the sibling `cron` CLI surface.
- [snippet_hermes_agent_tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — cron-job registration; relevance: how an authored job is registered with the scheduler.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery dispatch; relevance: announce/webhook/none delivery-ownership resolution.
- [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — cron timing helpers; relevance: `--at`/`--tz` one-shot datetime + due-time resolution.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — cron-job handoff to runtime; relevance: how an authored job is handed to the scheduler for execution.
- [snippet_hermes_agent_gw_session_context](../../code_snippets/snippet_hermes_agent_gw_session_context.md) — session/context binding; relevance: `--session isolated` resets ambient context (page's isolated semantics).
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session persistence; relevance: `session:<id>` persistent session keys.

### oc_cli_cron_run (9t · 11s · 10d)

**Terms** (≥8):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: running/administering its cron jobs.
- [Cron](../../term_dictionary/term_cron.md) — the scheduler; relevance: `cron run/list/get/show/runs` admin surface.
- [Model Router](../../term_dictionary/term_model_router.md) — per-run model selection/routing; relevance: per-job `--model` + isolated-cron model precedence (Gmail-hook → `--model` → cron-session → agent default).
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback model chains; relevance: per-job `fallbacks` list / empty-list strict mode / no hidden agent-primary retry.
- [Retry Pattern](../../term_dictionary/term_retry_pattern.md) — bounded retry; relevance: `LiveSessionModelSwitchError` retry loop bounded to two switch retries.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — run-history persistence; relevance: substitutes MISSING `term_sqlite` — jobs/run-history live in the shared SQLite state DB.
- [Session Data](../../term_dictionary/term_session_data.md) — isolated run sessions; relevance: `cron.sessionRetention` prunes completed isolated run sessions.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — run/denial logging (EXISTS); relevance: structured execution-denial metadata + run-history diagnostics surface the authoritative denial signal.
- [Throttling](../../term_dictionary/term_throttling.md) — rate-limiting/backoff; relevance: dead-endpoint preflight caches matching providers for 5 min to avoid hammering local servers.

**Docs** (≥10):
- [Hermes Cron Internals](../hermes_agent/hermes_cron_internals.md) — cron run internals; relevance: closest sibling model for run execution + run history.
- [Hermes Guide: Cron Troubleshooting](../hermes_agent/hermes_guide_cron_troubleshooting.md) — cron run debugging; relevance: run-output denials, stale-ack/silent-token, phase-specific errors.
- [Claude Code Scheduling Options Comparison](../claude_code/cc_scheduling_options_comparison.md) — cc scheduling comparison; relevance: per-run model/precedence + retention tradeoffs across scheduling backends.
- [Claude Code Loop Scheduled Tasks](../claude_code/cc_loop_scheduled_tasks.md) — cc looped scheduled runs; relevance: recurring run execution + skip/retry behavior.
- [Claude Code Desktop Scheduled Tasks](../claude_code/cc_desktop_scheduled_tasks.md) — cc scheduled run admin; relevance: run/list/inspect admin parallel.
- [Hermes Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback chains; relevance: per-job `fallbacks`/strict mode + local-provider preflight.
- [EventBridge Scheduler Retry & DLQ](../aws_eventbridge/eventbridge_scheduler_retry_dlq.md) — retry/failure handling; relevance: failure delivery + retry-on-error analog in a managed scheduler.
- [EventBridge Scheduler Monitoring](../aws_eventbridge/eventbridge_scheduler_monitoring.md) — run monitoring; relevance: `cron runs`/`status` field + delivery diagnostics analog.
- [oc_cli_cron_jobs](oc_cli_cron_jobs.md) — (planned, this series) the authoring half; relevance: jobs created there are run/administered here.
- [oc_cli_config_edit](oc_cli_config_edit.md) — (planned, this series) `cron.*` config; relevance: `cron.sessionRetention`/`cron.runLog.*` retention config edited via `config set`.

**Repos**:
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — cron run execution + run history; relevance: isolated/command runs execute in the Gateway and record history.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI admin commands; relevance: `cron list/get/show/run/runs` dispatched from the CLI.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — isolated run sessions/retention; relevance: `sessionRetention` prunes completed isolated run sessions.

**Snippets** (≥10, all EXISTING):
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — run-job execution; relevance: the isolated-run turn + denial/output handling.
- [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — run setup/preflight; relevance: pre-model watchdog + local-provider preflight (`/api/tags`, `/models`).
- [snippet_hermes_agent_cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — run state/status; relevance: the `status` field (disabled/running/ok/error/skipped/idle).
- [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — scheduler tick loop; relevance: recurring-run dispatch + skip/backoff bookkeeping.
- [snippet_hermes_agent_cli_model_switch_swap](../../code_snippets/snippet_hermes_agent_cli_model_switch_swap.md) — live model switch; relevance: `LiveSessionModelSwitchError` persist-and-retry behavior.
- [snippet_hermes_agent_cli_model_switch_validate](../../code_snippets/snippet_hermes_agent_cli_model_switch_validate.md) — model allow/validate; relevance: cron fails the run if `--model` not allowed/resolvable.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + failure notifications; relevance: run-failure delivery + denial reporting.
- [snippet_hermes_agent_gw_runner_errors](../../code_snippets/snippet_hermes_agent_gw_runner_errors.md) — runner error/denial classification; relevance: structured execution-denial metadata vs prose-refusal handling.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway run dispatch; relevance: how a manual/scheduled run is enqueued (`{ok,enqueued,runId}`).

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| clawbot / crestodian / commitments / completion / configure (command names) | OpenClaw vocabulary → digested as `oc_cli_*` doc notes (this sub-plan); NOT promoted to `term_dictionary`. |
| config / configure / `config set` modes / `config patch` / `config schema` | Documented in `oc_cli_config_edit` / `oc_cli_config_validate`; link existing `term_configuration_model`, not redefined. |
| SecretRef / SecretRef-builder / provider-builder / batch mode | OpenClaw config-credential vocabulary → documented in the config notes; link existing `term_secrets_manager`, not redefined. |
| cron job / one-shot / recurring / isolated session / delivery (announce/webhook/none) | Documented in `oc_cli_cron_jobs` / `oc_cli_cron_run`; link existing `term_cron`, `term_webhook`, `term_session_data`. |
| model-assisted planner / message rescue mode / YOLO posture / typed operations | Crestodian vocabulary → documented in `oc_cli_crestodian`; link existing `term_sandbox`, `term_secrets_manager` (no new term — these are product-specific, not cross-cutting). |
| shell completion / `$OPENCLAW_STATE_DIR` | Documented in `oc_cli_completion`; link existing `term_openshell`; `OPENCLAW_STATE_DIR` is a config path, not a term. |
| heartbeat / commitments concept / cron-jobs concept | Existing/other-sub-plan concepts → linked (`term_heartbeat`; concept pages owned by co02/au01), not duplicated. |

**Expected new `term_dictionary` captures: 0.** No genuinely cross-cutting, vault-reusable term without an existing note appears in these 7 pages — the agentic/LLM glossary already covers config, secrets, cron, OAuth/token, session, sandbox, model-routing, retry/backoff, idempotency, audit. (Candidate gaps `term_command_line_interface` / `term_environment_variable` / `term_json_schema` / `term_scheduler` are real cross-cutting concepts, but per the master's ownership decision they are out of scope for a CLI doc-page digest and are substituted with the closest existing terms above; if augment judges one genuinely reusable, propose it then.)

## Term-Note Authoring Requirements

**N/A (0 new terms)** — this sub-plan authors zero `term_dictionary` notes; it only links existing terms. Inherited from master (if augment proposes a genuinely cross-cutting new term, the master's multi-source-research + acronym-glossary requirement applies, best-fit glossary `acronym_glossary_a_e.md` for a CLI/config term).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (9 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + body H2s + footer) | `scripts/check_note_format.py` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (no content not in source) | diff each note vs `inbox/openclaw_docs/cli/<page>.md` |
| G3 | Density + Coverage (≤400L / ≤2500w / ≤6 code; every H2/H3 mapped) | per-note word/code count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + repo/sibling/doc, each with relevance statement) | review `## Related Notes` |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex |
| G7 | Discoverability (every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`) | `entry_openclaw_docs.md` rows + term/repo inlinks |
| G8 | In-degree ≥1 (anti-island) | query `note_links` after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
OC=the vault/resources/documentation/openclaw
GATE_DIR=resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_clawbot oc_cli_commitments oc_cli_completion oc_cli_config_edit oc_cli_config_validate oc_cli_configure oc_cli_crestodian oc_cli_cron_jobs oc_cli_cron_run"
for n in ${=NOTES}; do
  f="$OC/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in "## Overview" "## Related Notes"; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$OC"
# Gate sweep helper vars exported for the augment/execute runbook:
echo "GATE_DIR=$GATE_DIR REQ_SECTIONS=$REQ_SECTIONS REQUIRE_SOURCE_URL=$REQUIRE_SOURCE_URL SIBLING_PREFIX=$SIBLING_PREFIX"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Note code budget | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_cli_clawbot | procedure | 250 | 0 | 1 | ✅ |
| 2 | oc_cli_commitments | procedure | 380 | 7 | ≤4 | ✅ |
| 3 | oc_cli_completion | procedure | 320 | 1 | 1 | ✅ |
| 4 | oc_cli_config_edit | procedure | 650 | (from config 20) | ≤6 | ✅ |
| 5 | oc_cli_config_validate | procedure | 550 | (from config 20) | ≤6 | ✅ |
| 6 | oc_cli_configure | procedure | 500 | 1 | ≤3 | ✅ |
| 7 | oc_cli_crestodian | concept | 700 | 14 | ≤6 | ✅ |
| 8 | oc_cli_cron_jobs | procedure | 700 | (from cron 15) | ≤6 | ✅ |
| 9 | oc_cli_cron_run | procedure | 650 | (from cron 15) | ≤6 | ✅ |

No note approaches the 2,500w / 400-line cap. The code-heavy pages (config 20, cron 15, crestodian 14, commitments 7) keep each note ≤6 fences — config and cron split for exactly this reason; crestodian reproduces only the most load-bearing fences (rescue config shape, operator flow, setup-backend order) and link-outs the test-lane commands.

## Entry Point Decision (inherited from master)

Contributes 9 rows to `entry_openclaw_docs.md` (CREATE as a master pre-step, W1) under the **CLI** section / cl02 cluster; each note receives the entry-point back-link at finalization (satisfies G7/G8). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-`documentation/openclaw/` inbound links (DB-verify + add at execution; ≥1 per new note for G7/G8):

- `entry_openclaw_docs.md` → all 9 notes (primary anti-island guarantor; created in W1).
- `term_cron.md` → notes 8, 9 (the cron command reference).
- `term_secrets_manager.md` → notes 4, 5, 7 (SecretRef config/inspection).
- `term_configuration_model.md` → notes 4, 5, 6 (config editing/validation/wizard).
- `term_sandbox.md` → note 7 (rescue-mode sandbox gating).
- `term_heartbeat.md` → note 2 (commitments delivered via heartbeat).
- `term_openshell.md` → note 3 (shell completion).
- `term_model_router.md` → note 9 (per-job model selection).
- `repo_openclaw.md` → notes 1, 4, 5, 7 (CLI/config/repair host).
- `repo_openclaw_cli_wizard.md` → notes 1, 3, 6 (CLI command tree + wizard).
- `repo_openclaw_gateway.md` → notes 5, 8, 9 (validates config; runs the scheduler).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Cap dynamic-workflow fan-out ≤30 agents/run; embed the per-note contract manifest in the execution script; re-read each source page (config snippets reproduced verbatim, one BB per note). `git pull --rebase --autostash` first; commit+push after the phase (no Claude co-author trailer). Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref locked at raised floors; per-note ≥8t/≥10s/≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


- `term_json_schema` **EXISTS** (plan said MISSING) — now used directly in notes 4 (`config schema`) and 5 (schema validation).
- `term_audit_operations` **EXISTS** (plan flagged "DB-verify") — used in notes 5, 7, 9 for write-safety / rescue-audit / run-history logging.
- `term_idempotency` and `term_idempotency_key` **both EXIST**; `term_idempotency` used for no-clobber / run-once semantics.
- `term_session_data`, `term_session_persistence`, `term_sandbox`, `term_sandbox_backend`, `term_compaction`, `term_commitment_device`, `term_model_catalog`, `term_model_failover`, `term_cron_expression`, `term_auth_profile`, `term_open_loops`, `term_persistent_goal`, `term_tool_registry`, `term_throttling`, `term_claude`, `term_claude_code` **all EXIST** and were used to reach the ≥8-term floor with genuine relevance.
- Eventbridge docs confirmed at `resources/documentation/aws_eventbridge/` (relpath `../aws_eventbridge/eventbridge_*.md`), used as managed-scheduler analogs for notes 8/9.

**Still MISSING (substituted with the closest EXISTING term, per master's CLI-doc-page ownership decision — NOT promoted):** `term_command_line_interface` (→ `term_openshell`), `term_environment_variable` (→ `term_configuration_model`), `term_session` (→ `term_session_data`), `term_backward_compatibility` (→ `term_idempotency`), `term_scheduler` (→ `term_cron`), `term_sqlite` (→ `term_session_persistence`).

**Per-note locked counts (terms / snippets / docs / repos · floors met):**

| Note | Terms | Snippets | Docs | Repos | ≥8t/≥10s/≥10d met? |
|---|---:|---:|---:|---:|---|
| oc_cli_clawbot | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| oc_cli_commitments | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| oc_cli_completion | 8 | 10 | 10 (8 existing + 2 sibling) | 2 | ✅ |
| oc_cli_config_edit | 9 | 11 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| oc_cli_config_validate | 9 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| oc_cli_configure | 8 | 10 | 10 (8 existing + 2 sibling) | 3 | ✅ |
| oc_cli_crestodian | 10 | 12 | 10 (8 existing + 2 sibling) | 4 | ✅ |
| oc_cli_cron_jobs | 8 | 12 | 11 (8 existing + 3 sibling) | 3 | ✅ |
| oc_cli_cron_run | 9 | 11 | 10 (8 existing + 2 sibling) | 3 | ✅ |

**New-term candidates.** **0.** No genuinely cross-cutting, vault-reusable term without an existing note appears in these 7 CLI pages. The four plan-noted candidate gaps (`term_command_line_interface`, `term_environment_variable`, `term_scheduler`, `term_sqlite`) are real cross-cutting concepts but are out of scope for a CLI doc-page digest per the master's ownership decision and were substituted with existing terms above. If any is later judged genuinely reusable, capture via `/tessellum-capture-term-note` + add to **`acronym_glossary_a_e.md`** (best-fit glossary for a CLI/config/env term) per the master's W5 + Term-Note Authoring Requirements. The Undigested Terms Plan and Term-Note Authoring Requirements (N/A — 0 new terms) sections are unchanged and remain valid.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_cl02.md` · Date: 2026-06-21 · Reviewer: xref-augment + review pass

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every planned note has ≥8 terms / ≥10 snippets / ≥10 docs, each link carries a "relevance:" statement; per-note counts table in the Augmentation Report. |
| CP2 | 9-GATE present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-detect, G6 Broken-link-fix, G7 Discoverability, G8 In-degree≥1 (anti-island). Single execution phase; all gates apply. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)` — contributes 9 rows to `entry_openclaw_docs.md` (CREATE as master pre-step W1); each note gets the back-link at finalization (G7/G8). Master `>30`-note size threshold → CREATE required (satisfied at hub level). |
| CP4 | Size | **PASS** | 9 planned notes ≤30; sub-plan of a master+sub-plan structure (105 sub-plans). |
| CP5 | Format derived (not invented) | **PASS** | Inherits master Format Definition derived from existing `claude_code/`/`pi/` doc corpora: `## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; forbidden-field list present. |
| CP6 | Density | **PASS** | `## Density Re-Assessment` table — all 9 notes ≤700w / ≤6 code fences; config (20 fences) and cron (15 fences) split into 4/5 + 8/9 specifically to stay ≤6; crestodian (14 fences) reproduces only load-bearing fences. No borderline note unaddressed. |
| CP7 | Sources measured | **PASS** | `## Source Pages (Measured 2026-06-20)` table with body-word counts via `sed`/`wc`; re-read of all 7 pages at augment confirms sizes (clawbot 72, commitments 240, completion 169, config 2,095, configure 553, crestodian 1,553, cron 2,400 body words) — consistent with the plan estimates, no >1.5× under-estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (every command/config/cron/crestodian token mapped to an `oc_*` doc or an existing term link); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; master multi-source + acronym-glossary mandate inherited if a term is later proposed). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to rename. All-notes collision audit (term_dictionary AND documentation/) performed: the 9 planned `oc_cli_*` doc notes do NOT duplicate any existing term — they link existing `term_cron`/`term_secrets_manager`/`term_configuration_model`/`term_sandbox`/etc. rather than redefining. 6 plan-cited "MISSING" terms re-checked post-correction; substituted, not created. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** YAML `status: pending → ready`.
