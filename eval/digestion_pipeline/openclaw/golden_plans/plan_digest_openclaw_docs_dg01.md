---
title: Sub-Plan dg01 — OpenClaw Docs: Diagnostics
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["diagnostics/flags"]
---

# Sub-Plan dg01: Diagnostics

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML + `## Overview` … `## Related Notes` … `## References`), dedup-before-create, the 9-GATE table, cross-refs, and the entry-point decision are all inherited from the master and not re-derived here.

## Scope

The single Diagnostics page (`diagnostics/flags`): how OpenClaw's opt-in diagnostics flags enable targeted, subsystem-scoped debug logs (and profiler/timeline timing spans) **without** raising global logging levels. Covers flag syntax + wildcards, enabling via config vs the `OPENCLAW_DIAGNOSTICS` env override, the `=0` process-level disable, profiler flags (`profiler`/`reply.profiler`/`codex.profiler`), the `timeline` artifact + `openclaw.diagnostics.v1` envelope, where logs land (`/tmp/openclaw/openclaw-YYYY-MM-DD.log`, JSONL, redaction), and `rg`/`tail` extraction recipes. Priority **P2 (Phase B)** per master; this is operator/support-facing troubleshooting reference. The code-side `repo_openclaw_gateway` / `repo_openclaw` notes are LINKED, not recreated.

**Source**: OpenClaw docs, 1 page, 606 measured words. **Planned: 1 note.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| diagnostics/flags | /diagnostics/flags | 606 | 16 | 9 | 0 | procedure |

(Measured via `wc -w` = 606; `grep -c '```' = 32 ⇒ 16 fenced code blocks; 9 H2 headings, 0 H3.)

## Content Strategy

- **Prioritize**: the operator decision surface — flag syntax/wildcards, the config-vs-env enable paths, the `OPENCLAW_DIAGNOSTICS=0` process-level disable, and the log location/format/redaction facts a support engineer needs.
- **Do NOT split**: 606 words (well under the 2,500-word cap) and one cohesive `building_block: procedure` (enable + read targeted diagnostics). All 9 H2 sections describe the same task cluster; splitting would fragment a single workflow. ⇒ **1 note.** (Master's ~2-note estimate was a planning placeholder; measured content = 1 well-scoped note.)
- **Code-block budget**: the source has 16 fences but the density cap is ≤6 code blocks. Reproduce only the ~6 highest-value, verbatim snippets — pick one representative from each cluster: (1) config `diagnostics.flags` JSON, (2) `OPENCLAW_DIAGNOSTICS=…` env-override line, (3) `OPENCLAW_DIAGNOSTICS=0` disable, (4) a profiler-flag run (`OPENCLAW_DIAGNOSTICS=profiler openclaw gateway run`), (5) the `timeline` + `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH` block, (6) one extraction recipe (`rg`/`tail` against `/tmp/openclaw/openclaw-*.log`). Describe the remaining variants in prose.
- **Skip / link-out**: log destinations/levels/redaction internals → link `/logging` (top-level, sub-plan rt02) instead of duplicating; broader gateway diagnostics + troubleshooting → link `gateway/diagnostics` (gw02) and `gateway/troubleshooting` (gw07); `openclaw logs --follow` → link `cli/logs` (cl04). Telemetry vocab links existing `term_observability_agent_systems` / `term_data_observability` / `term_trace`, not redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_diagnostics_flags.md` | procedure | diagnostics/flags.md: How it works · Enable via config · Env override (one-off) · Profiling flags · Timeline artifacts · Where logs go · Extract logs · Notes · Related | 650 | Enabling OpenClaw's opt-in diagnostics flags for targeted subsystem debug logs without raising global log levels: flag syntax + wildcards, config vs `OPENCLAW_DIAGNOSTICS` env enable, `=0` process disable, profiler flags, the `timeline` JSONL artifact + `openclaw.diagnostics.v1` envelope, log location/format/redaction, and `rg`/`tail` extraction. |

## Section Coverage Map

```
diagnostics/flags.md
├── (intro: opt-in, no effect unless subsystem checks) → note 1 (oc_diagnostics_flags) Overview
├── How it works (strings, case-insensitive; config/env; wildcards `telegram.*`, `*`) → note 1
├── Enable via config (diagnostics.flags JSON; multiple flags; restart) ───────────── → note 1
├── Env override (one-off) (OPENCLAW_DIAGNOSTICS=…; =0 process-level disable) ─────── → note 1
├── Profiling flags (profiler / reply.profiler / codex.profiler; config; =0 disable) → note 1
├── Timeline artifacts (timeline flag; TIMELINE_PATH; 1/all/* enable it;
│   openclaw.diagnostics.v1 envelope; treat as local diagnostics) ─────────────────── → note 1
├── Where logs go (/tmp/openclaw/openclaw-YYYY-MM-DD.log; logging.file; JSONL;
│   logging.redactSensitive) ──────────────────────────────────────────────────────── → note 1
├── Extract logs (ls -t latest; rg telegram/brave http; tail -f) ─────────────────── → note 1
├── Notes (logging.level>warn suppresses; brave.http privacy; safe to leave on) ──── → note 1
└── Related (/gateway/diagnostics, /gateway/troubleshooting; + /cli/logs, /logging
    referenced inline) ──────────────────────────────────────────────────────────── → note 1 References
```
No orphaned sections — all 9 H2 sections + intro map to note 1. The `/logging`, `/cli/logs`, `/gateway/diagnostics`, `/gateway/troubleshooting` pointers are rendered as `## References` / Related Notes links (sibling sub-plans rt02/cl04/gw02/gw07), not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | `diagnostics/flags.md` is 606 words (≪ 2,500 cap), single BB (procedure). No split. Code-block count (16) is reduced to ≤6 by selective verbatim reproduction (see Content Strategy), not by splitting. |

## Summary Statistics & Building Block Distribution

- Source pages: **1** (606 words). New `oc_` notes: **1**. New `term_dictionary` notes: **0** (expected per master).
- BB distribution: procedure ×1.
- Est. digest words ~650 (1 note). 16 source code fences reduced to ≤6 verbatim snippets in the note; remaining variants described in prose.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_diagnostics_flags (9t · 12s · 18d · 5 repos)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the open-source self-hosted gateway whose diagnostics subsystem this note documents; relevance: the entire page is OpenClaw's `diagnostics.flags` / `OPENCLAW_DIAGNOSTICS` feature.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — observability surface (logs/traces/spans) for agent runtimes; relevance: diagnostics flags + profiler/timeline spans ARE OpenClaw's agent-gateway observability surface.
- [Data Observability](../../term_dictionary/term_data_observability.md) — structured-log + data-quality monitoring concept; relevance: the JSONL diagnostics log file + `logging.redactSensitive` redaction are a data-observability concern.
- [Trace](../../term_dictionary/term_trace.md) — distributed-trace / span timing data; relevance: profiler-gated timing spans + the `timeline` artifact emit phase/span names + durations (the `openclaw.diagnostics.v1` envelope is span data).
- [Structured Output](../../term_dictionary/term_structured_output.md) — one-JSON-object-per-line / schema-bound output; relevance: diagnostics logs are JSONL (one JSON object per line) and the timeline uses the `openclaw.diagnostics.v1` schema envelope.
- [Langfuse](../../term_dictionary/term_langfuse.md) — open-source LLM/agent tracing + observability platform; relevance: cross-tool analog for collecting agent span/trace timing data, exactly what the `profiler`/`timeline` flags produce locally.
- [PII](../../term_dictionary/term_pii.md) — personally-identifiable / sensitive data; relevance: `logging.redactSensitive`, the `brave.http` "search queries can be sensitive" caveat, and "review timeline files before sharing" are PII-redaction guidance.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol connector layer OpenClaw routes; relevance: gateway subsystem diagnostics flags can scope MCP/connector subsystems (wildcard `gateway.*` / per-subsystem flags), the connector vocabulary being diagnosed.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-runtime client protocol (Codex/ACP harness); relevance: the `codex.profiler` flag profiles Codex app-server startup/tool/thread spans — an ACP-runtime subsystem made diagnosable by these flags.

- [CC: OTel Configuration Variables](../claude_code/cc_otel_configuration_variables.md) — env-var-driven telemetry/observability configuration; relevance: closest cross-tool analog to the `OPENCLAW_DIAGNOSTICS` / `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH` env-override enable path.
- [CC: OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry analysis + privacy/redaction posture; relevance: parallels the redaction (`logging.redactSensitive`) + "treat timeline files as local artifacts, review before sharing" privacy guidance.
- [CC: OTel Traces](../claude_code/cc_otel_traces.md) — trace/span emission reference; relevance: the structured-span analog of OpenClaw's profiler timing spans + `openclaw.diagnostics.v1` timeline events.
- [CC: Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — opt-in telemetry + privacy posture for a coding-agent tool; relevance: directly analogous opt-in-diagnostics + redaction stance ("flags are opt-in, no effect unless checked").
- [CC: Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — targeted debug logging without global verbosity; relevance: same core idea as this page — "targeted debug logs without turning on verbose logging everywhere".
- [CC: Monitoring with OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel monitoring setup; relevance: parallel to OpenClaw's profiler/timeline timing spans and the planned `gateway/opentelemetry` exporter.
- [CC: SDK Observability with OpenTelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK-level structured observability/spans; relevance: the structured-span counterpart of the `openclaw.diagnostics.v1` envelope (process id, phase/span names, durations).
- [CC: Install Diagnostics](../claude_code/cc_install_diagnostics.md) — install/runtime diagnostics collection; relevance: cross-tool diagnostics-bundle analog for support engineers (the operator-facing audience of this page).
- [CC: Environment Variables](../claude_code/cc_environment_variables.md) — env-var configuration reference; relevance: `OPENCLAW_DIAGNOSTICS`, `OPENCLAW_DIAGNOSTICS=0`, and `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH` are the OpenClaw env-var analogs documented here for Claude Code.
- [Hermes: LSP Diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — diagnostics surface in the sibling Hermes agent; relevance: the closest sibling-agent diagnostics doc (Hermes is the same coding-agent-gateway lineage as OpenClaw).
- [Bedrock AgentCore: Observability Overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — agent-runtime observability (traces/spans/logs) overview; relevance: cross-corpus managed-agent-runtime analog for the same trace/span/structured-log diagnostics OpenClaw emits locally.
- [oc_gateway_diagnostics](oc_gateway_diagnostics.md) — (planned, this series, gw02) gateway-scoped diagnostics; relevance: the exact page `diagnostics/flags` links under "Related — Gateway diagnostics".
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) — (planned, this series, gw07) gateway troubleshooting; relevance: the other "Related" link on this page.
- [oc_gateway_logging](oc_gateway_logging.md) — (planned, this series, gw03, `gateway/logging`); relevance: log destinations/levels/redaction the `/logging` inline pointer references (`logging.file`, `logging.level`, `logging.redactSensitive`).
- [oc_cli_logs](oc_cli_logs.md) — (planned, this series, cl04, `cli/logs`); relevance: `openclaw logs --follow` for remote gateways, the explicit `[/cli/logs]` pointer in the Extract-logs section.
- [oc_logging](oc_logging.md) — (planned, this series, rt02, top-level `/logging`); relevance: change log destinations/levels/redaction — the `[/logging]` pointer in the Notes section.
- [oc_gateway_opentelemetry](oc_gateway_opentelemetry.md) — (planned, this series, gw04, `gateway/opentelemetry`); relevance: sibling telemetry exporter — the OTel-export path for the same timing spans the `profiler`/`timeline` flags produce.
- [oc_gateway_prometheus](oc_gateway_prometheus.md) — (planned, this series, gw05, `gateway/prometheus`); relevance: sibling metrics exporter in the same observability cluster.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway binary; relevance: `openclaw gateway run` consumes `OPENCLAW_DIAGNOSTICS` and emits the diagnostics/profiler/timeline spans — closest code-side counterpart.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: houses the diagnostics-flag plumbing, the `/tmp/openclaw/openclaw-*.log` file convention, and the `openclaw.diagnostics.v1` envelope.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channel plugins; relevance: the `telegram.*` / `telegram.http` / `brave.http` example flags target channel/provider subsystems implemented here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security module; relevance: backs the redaction (`logging.redactSensitive`) + "treat timeline files as local diagnostics artifacts" privacy guidance.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — sibling coding-agent gateway; relevance: its logging-setup / redaction / cli-logs / doctor source is the code-side analog of OpenClaw's diagnostics plumbing (most cited snippets below come from it).

- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logger setup, levels, sinks; relevance: code-side analog of "Where logs go" + `logging.level`/`logging.file` behavior.
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — Langfuse span/trace export plugin; relevance: the implementation pattern for collecting the timing spans the `profiler`/`timeline` flags emit.
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — CLI logs/follow command; relevance: the code-side analog of `openclaw logs --follow` (the `[/cli/logs]` pointer) and the `tail -f` extraction recipe.
- [snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md) — doctor/early-diagnostic checks; relevance: sibling diagnostics-command implementation (the broader gateway-diagnostics cluster this page links).
- [snippet_hermes_agent_core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md) — auxiliary diagnostics emission; relevance: how subsystem-scoped diagnostics events are produced — the code behind "no effect unless a subsystem checks them".
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — sensitive-value redaction patterns; relevance: the implementation of `logging.redactSensitive` log redaction.
- [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — redact-on-export of trajectory artifacts; relevance: the analog of "review timeline files before sharing outside your machine".
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap reading env + config; relevance: the code path that parses `OPENCLAW_DIAGNOSTICS`/`=0` env overrides vs `diagnostics.flags` config.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — gateway startup / ACP prewarm; relevance: the startup phase whose timing the profiler/timeline startup spans measure (the "earliest config-loading spans" caveat).
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway run entry/dispatch; relevance: where `OPENCLAW_DIAGNOSTICS=… openclaw gateway run` takes effect for a single run.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime security/exec audit; relevance: the privacy-of-local-artifacts posture ("treat timeline files as local diagnostics artifacts").

## Undigested Terms Plan

| Term (page vocabulary) | Disposition |
|---|---|
| diagnostics flags | Subject of THIS doc note (`oc_diagnostics_flags`); not a `term_dictionary` capture. |
| `OPENCLAW_DIAGNOSTICS` (env var) | OpenClaw-specific config token → documented inline in the note; not a term. |
| wildcard flag (`telegram.*`, `*`) | Inline mechanic of the note; not a reusable cross-cutting term. |
| profiler flags / spans (`reply.profiler`, `codex.profiler`) | OpenClaw-specific runtime tokens → inline in note; observability concept links `term_trace`. |
| timeline artifact / `openclaw.diagnostics.v1` envelope | OpenClaw-specific schema → inline in note; structured-log concept links `term_structured_output`. |
| JSONL log file / redaction (`logging.redactSensitive`) | Logging mechanic → inline; concept links `term_data_observability` / `term_structured_output`. |
| observability / telemetry | Existing terms `term_observability_agent_systems` / `term_data_observability` / `term_trace` — **link existing**, do NOT create. |
| OpenTelemetry / Prometheus | No existing `term_dictionary` note (searched; absent). Out of scope for THIS page (covered by gw04 `gateway/opentelemetry` and gw05 `gateway/prometheus`). **No new-term candidate proposed here** — defer ownership to those sub-plans if a cross-cutting term is warranted. |

**New `term_dictionary` candidates from this sub-plan: 0** (per master's corpus-wide design — OpenClaw vocabulary is digested as `oc_*` doc notes, only existing terms are linked). No genuinely cross-cutting, vault-reusable term lacking an existing note appears on this page.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — this sub-plan authors zero `term_dictionary` notes. The multi-source-research + glossary-update mandate (inherited from master, W5) applies only if augment surfaces a new term; none is expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (1 note, P2). The 9-GATE table is identical to the master's shared gate set; all must PASS before commit.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` (fixed YAML field order; `## Overview` + `## Related Notes` present; `**Source**`/`**Last Updated**`/`**Status**` footer). |
| G2 | Grounding | Diff note claims vs `inbox/openclaw_docs/diagnostics/flags.md` — every flag/env-var/path/snippet faithful, no invented behavior. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, single BB; all 9 source H2 sections covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` links + `repo_openclaw*` + sibling `oc_*` + cross-corpus doc, each with a relevance statement; indexed `[text](path.md)` link format. |
| G5 | Ghost-reference detect + redirect | Every cited existing target resolves in DB; sibling `oc_*` marked `(planned)` until created. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex; 0 broken links. |
| G7/G8 | Discoverability (in-degree ≥1, anti-island) | `oc_diagnostics_flags` RECEIVES ≥1 inbound link from outside `documentation/openclaw/` — satisfied via `entry_openclaw_docs.md` (W1 pre-step), plus candidate inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_diagnostics_flags"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  grep -Eq "$REQ_SECTIONS" "$f" || echo "MISSING REQ SECTION: $n"
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # at least one sibling oc_ cross-link
  grep -q "(${SIBLING_PREFIX}" "$f" || echo "NO SIBLING oc_ LINK: $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done

# G1 YAML frontmatter
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: DB-verify each cited EXISTING note_id resolves
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for id in \
  resources/term_dictionary/term_openclaw.md \
  resources/term_dictionary/term_observability_agent_systems.md \
  resources/term_dictionary/term_data_observability.md \
  resources/term_dictionary/term_trace.md \
  resources/term_dictionary/term_structured_output.md \
  resources/term_dictionary/term_mcp.md \
  areas/code_repos/repo_openclaw_gateway.md \
  areas/code_repos/repo_openclaw.md \
  areas/code_repos/repo_openclaw_channels_messaging.md \
  areas/code_repos/repo_openclaw_security.md \
  resources/documentation/claude_code/cc_data_usage_and_telemetry.md \
  resources/documentation/claude_code/cc_debug_your_configuration.md \
  resources/documentation/claude_code/cc_monitoring_opentelemetry_setup.md \
  resources/documentation/claude_code/cc_sdk_observability_opentelemetry.md \
  resources/documentation/claude_code/cc_install_diagnostics.md \
  echo "$id => ${r:-MISSING}"
done

# G6 broken links after incremental reindex
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_diagnostics_flags | procedure | 650 | 6 | ✅ (≤400 L, ≤2,500 w, ≤6 code, single BB) |

Source has 16 fences; reduced to ≤6 verbatim snippets (config JSON, env override, `=0` disable, profiler run, timeline block, one extraction recipe) — the remaining variants described in prose. No note approaches the word/line caps (606 source words → ~650 digest words including Overview + Related Notes).

## Entry Point Decision (inherited from master)

Contributes **1 row** to `entry_openclaw_docs.md` (CREATED as the master W1 pre-step) under a **Diagnostics** cluster (alongside the master's `db01` Debug). `oc_diagnostics_flags` receives its entry-point back-link at finalization. No new entry point created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution, for G7/G8 in-degree ≥1):
- `entry_openclaw_docs.md` → `oc_diagnostics_flags` (primary anti-island guarantee; W1 pre-step).
- `areas/code_repos/repo_openclaw_gateway.md` → `oc_diagnostics_flags` (code↔docs cross-link: the gateway emits the diagnostics/timeline spans).
- `areas/code_repos/repo_openclaw.md` → `oc_diagnostics_flags` (monorepo housing the flag plumbing).
- `resources/term_dictionary/term_observability_agent_systems.md` → `oc_diagnostics_flags` (reciprocal: the agent-observability term gains a concrete OpenClaw diagnostics example).
- `resources/documentation/claude_code/cc_data_usage_and_telemetry.md` → `oc_diagnostics_flags` (cross-corpus "see also" for the analogous telemetry/diagnostics doc).

## Pacing Rules (inherited from master)

Single phase, 1 note; run all 8 gates before commit. Re-read `inbox/openclaw_docs/diagnostics/flags.md`; reproduce config/env snippets verbatim. One BB per note. `git pull --rebase --autostash origin main` first; commit + push the sub-plan in one cycle; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. (Trivially under the ~30-agent fan-out cap — this sub-plan is 1 note.)

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Per-note counts.**

| Note | Terms | Snippets | Docs (existing + planned) | Repos | Floors met (≥8t · ≥10s · ≥10d) |
|---|---:|---:|---|---:|---|


**New-term candidates + best-fit glossary.** **0 new `term_dictionary` candidates** — confirmed consistent with the master's corpus-wide design (OpenClaw vocabulary is digested as `oc_*` doc notes; only existing terms are linked). No genuinely cross-cutting, vault-reusable term lacking an existing note appears on this page. The page vocabulary (`diagnostics flags`, `OPENCLAW_DIAGNOSTICS`, wildcard flags, `reply.profiler`/`codex.profiler`, the `timeline` artifact / `openclaw.diagnostics.v1` envelope, JSONL/`logging.redactSensitive`) is OpenClaw-specific config tokens documented inline in the note, not reusable terms. OpenTelemetry/Prometheus have no existing `term_dictionary` note and are out of scope for THIS page (owned by gw04/gw05); no candidate proposed here. The Undigested Terms Plan stands unchanged (0 captures); the augment re-read surfaced no new undigested terms (<3, so no upstream plan-digestion quality flag).

**Issues.** None blocking. (`cc_debug.md` was checked as a candidate doc and is NOT in the vault — it was excluded; the cited `cc_debug_your_configuration.md` is the correct present note.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance + relevance-statement per link) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; oc_diagnostics_flags = 9 terms · 12 snippets · 18 docs · 5 repos; every link carries a `— what it is; relevance: …` statement; ≥8t/≥10s/≥10d floors all met. |
| CP2 | 9-GATE table present per batch (G1–G6 + G7/G8 Discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost detect+redirect, G6 Broken-link fix, G7/G8 Discoverability (in-degree ≥1) for the single execution phase. |
| CP3 | Entry point inherited / specified | **PASS** | `## Entry Point Decision` contributes 1 row to `entry_openclaw_docs.md` (planned/created as master W1 pre-step) under a Diagnostics cluster; no new entry point created by this sub-plan (correct per <15-note size rule + master inheritance). |
| CP4 | Size | **PASS** | 1 planned note (≪30); no split needed (606 source words ≪ 2,500-word cap, single BB procedure). |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master's Format Definition, itself derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `## Overview` / `## Related Notes` / `## References` + bold `**Source**`/`**Last Updated**`/`**Status**` footer + fixed YAML field order; matches existing target-type notes. |
| CP6 | Density | **PASS** | Density Re-Assessment: ~650 digest words, ≤6 code blocks (16 source fences reduced by selective verbatim reproduction, NOT splitting), ≤400 lines, single BB — within all caps; not borderline. |
| CP7 | Sources measured | **PASS** | Source re-read 2026-06-21: `wc -w` = 606 words, 16 fenced blocks (32 ``` lines / 2), 9 H2 / 0 H3 — matches the plan's measured Source table exactly (ratio 1.0, well within ±30%). |
| CP8 | Undigested terms + authoring requirements | **PASS** | `## Undigested Terms Plan` present (0 new captures, design-consistent with master); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, mandate inherited from master W5 if a term surfaces). Augment re-read surfaced no new undigested terms. |
| CP8f | Slug specificity + collision audit (all planned notes; term AND doc) | **PASS** | The single planned note is a `oc_*` doc note, NOT a `term_*` slug; collision audit (term_dictionary AND documentation/) confirms `oc_diagnostics_flags` does not duplicate any existing term or doc note — OpenClaw's `diagnostics/flags` page has no existing vault home; nearest existing notes (`term_observability_agent_systems`, `term_data_observability`, `cc_*` OTel docs) are cross-tool/concept and are LINKED, not duplicated. No too-general slug; no removal/rename needed. |
| CP9 | Discoverability / inlinks (G8, in-degree ≥1 from outside folder) | **PASS** | `## Inlinks (existing notes → new notes)` plans ≥5 outside-folder inbound links (`entry_openclaw_docs`, `repo_openclaw_gateway`, `repo_openclaw`, `term_observability_agent_systems`, `cc_data_usage_and_telemetry`); G7/G8 in the gate table; inlink addition is an EXECUTED phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** All checkpoints pass and the single note meets all raised floors (≥8 terms · ≥10 snippets · ≥10 docs). Plan status advanced `pending → ready`.
