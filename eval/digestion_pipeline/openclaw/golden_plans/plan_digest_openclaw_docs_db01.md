---
title: Sub-Plan db01 — OpenClaw Docs: Debug (Node + tsx __name crash)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["debug/node-issue"]
---

# Sub-Plan db01: Debug

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing / format / dedup / undigested-terms / 9-GATE / cross-refs / entry-point ALL inherited from the master; this file re-reads + measures its one source page and locks per-note scope, coverage, and candidate cross-references.

## Scope

The single OpenClaw **Debug** page (`debug/node-issue`): a focused troubleshooting writeup of the
`TypeError: __name is not a function` crash that appears when OpenClaw is started under Node + `tsx`
(esbuild's `keepNames` `__name` helper missing/overwritten in the Node 25 loader path). It covers the
failing stack trace, affected environment (Node 25.x / tsx 4.21.0 / macOS), Node-version test matrix,
the Bun→tsx regression (`commit 2871657e`), root-cause hypothesis, workarounds (use Bun, build then run
`node openclaw.mjs`, type-check with `tsgo`), and next steps. Priority **P2** (Phase B): an operational
troubleshooting reference, useful when standing up OpenClaw from source via the Node toolchain, complementary
to the `install/node` and `gateway/troubleshooting` pages (digested by other sub-plans).

**Source**: OpenClaw docs, 1 page, **414 measured words**. **Planned: 1 note.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| node-issue | debug/node-issue | 414 | 4 | 11 | 0 | argument (troubleshooting writeup: symptom → hypothesis → workaround) |

(Measured 2026-06-20 from `inbox/openclaw_docs/debug/node-issue.md`: `wc -w` = 414; code fences = 8 ÷ 2 = 4;
11 `##` headings — Summary, Environment, Repro (Node-only), Minimal repro in repo, Node version check,
Notes / hypothesis, Regression history, Workarounds, References, Next steps, Related; 0 `###`.)

## Content Strategy

- **Prioritize**: the symptom + root-cause hypothesis (`__name`/`keepNames` esbuild helper missing under the
  Node 25 loader) and the actionable workarounds — these are the load-bearing, reusable parts of the page.
- **Do NOT split**: 414 words, 4 code blocks, all 11 H2 sections form ONE coherent troubleshooting narrative
  (single argument BB: symptom → environment → repro → version matrix → hypothesis → regression → workaround →
  next steps). Far under every density cap; splitting would fragment a single diagnosis. ⇒ **1 note.**
- **Mirror, do not editorialize**: reproduce the stack trace and the bash repro/workaround blocks verbatim
  (selectively, ≤6 fences); keep the speculative root cause flagged as a hypothesis (the source does).
- **Link-out, don't duplicate**: the page's own `## Related` links (`/install/node`, `/gateway/troubleshooting`)
  point at pages owned by `in04` (`install/node`) and `gw07` (`gateway/troubleshooting`); reference the planned
  sibling `oc_*` notes (marked "(planned)") instead of re-digesting that content here.
- **No term definitions inlined** (master rule): Node/tsx/esbuild/Bun terminology is linked to existing
  `term_*` notes where they exist, never redefined in this digest note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_debug_node_issue.md` | argument | debug/node-issue.md — all 11 H2 (Summary, Environment, Repro (Node-only), Minimal repro in repo, Node version check, Notes/hypothesis, Regression history, Workarounds, References, Next steps, Related) | 450 | OpenClaw's `TypeError: __name is not a function` crash under Node + tsx: the failing `createSubsystemLogger`/auth-profiles stack trace, the affected environment (Node 25.x, tsx 4.21.0), the Node-version test matrix, the Bun→tsx regression (commit 2871657e), the esbuild `keepNames`/`__name`-helper root-cause hypothesis, and the workarounds (use Bun, build then run `node openclaw.mjs`, type-check with tsgo) plus next steps. |

Filename derivation (master rule): slug `debug/node-issue` → `/` and `-` replaced by `_` → `oc_debug_node_issue.md`.

## Section Coverage Map

```
debug/node-issue.md
├── Summary (stack trace, createSubsystemLogger/auth-profiles) → note 1 (oc_debug_node_issue)
├── Environment (Node 25.x, tsx 4.21.0, macOS) ─────────────── → note 1
├── Repro (Node-only) (node --import tsx src/entry.ts status) ─ → note 1
├── Minimal repro in repo (scripts/repro/tsx-name-repro.ts) ── → note 1
├── Node version check (25.3.0 fails, 22.22.0 fails, 24 TBD) ─ → note 1
├── Notes / hypothesis (esbuild keepNames → __name helper) ─── → note 1
├── Regression history (2871657e: Bun → tsx, 2026-01-06) ───── → note 1
├── Workarounds (Bun / tsgo + node openclaw.mjs / disable keepNames) → note 1
├── References (opennext / esbuild keep-names / esbuild#1031) ─ → note 1 (## References, external URLs)
├── Next steps (repro on Node 22/24, pin tsx, file upstream) ─ → note 1
└── Related (/install/node, /gateway/troubleshooting) ──────── → note 1 (→ planned oc_install_node, oc_gateway_troubleshooting)
```
No orphaned sections. The two `## Related` link-outs are owned by other sub-plans (`in04`: `install/node`;
`gw07`: `gateway/troubleshooting`) and are referenced as planned siblings, not re-digested here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | `debug/node-issue.md` is 414 words / 4 code blocks / single argument BB — one coherent troubleshooting narrative, well under every density cap (≤2500w, ≤6 code, ≤400 lines). 1 page → 1 note. |

## Summary Statistics & Building Block Distribution

- Source pages: **1** (414 words, 4 code fences, 11 H2 / 0 H3).
- New `oc_*` notes: **1** (`oc_debug_node_issue.md`).
- New `term_dictionary` notes: **0** (Node/tsx/esbuild/Bun vocab is linked to existing terms where present;
  no genuinely cross-cutting reusable term lacks both a doc home and an existing note — see Undigested Terms Plan).
- BB distribution: argument ×1.
- Est. digest words: ~450 (one note). Source's 4 code fences (stack trace + 3 bash repro/workaround blocks)
  reproduce selectively, ≤6 per note.
- Cross-refs (LOCKED at xref-augment 2026-06-21): `oc_debug_node_issue` maps **11 terms · 12 snippets · 12 docs
  (10 EXISTING + 2 planned siblings) · 4 repos** — relevance-selected (no padding), all EXISTING targets
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Relative paths computed FROM the note at `resources/documentation/openclaw/oc_debug_node_issue.md`:
> term → `../../term_dictionary/`; snippet → `../../code_snippets/`; doc → `../<folder>/`; repo →
> `../../../areas/code_repos/`; sibling `oc_*` → `oc_*.md` (this series); entry → `../../../0_entry_points/`.
> `(planned, this series)` = sibling `oc_*` not yet created (counts toward the 10-doc floor; ≥5 docs are

### oc_debug_node_issue (11t · 12s · 12d (10 existing + 2 planned) · 4 repos)

Source: `debug/node-issue.md` (all 11 H2). OpenClaw's `TypeError: __name is not a function` crash under Node + `tsx`:
the `createSubsystemLogger` / `auth-profiles/constants.ts` stack trace, the affected environment (Node 25.x / tsx
4.21.0 / macOS), the Node-version test matrix, the Bun→tsx regression (commit `2871657e`), the esbuild
`keepNames`/`__name`-helper root-cause hypothesis, and the workarounds (use Bun, `tsgo` + `node openclaw.mjs`,
disable keepNames) plus next steps.

- [Node.js](../../term_dictionary/term_node_js.md) — the JavaScript runtime whose loader path triggers the crash; relevance: the failure is Node-25.x/22.x-specific (the version matrix is the whole diagnosis), so Node.js is the central environment variable.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed JS compiled/transformed before execution; relevance: OpenClaw's source is TS run through `tsx`, and the crash lives in the TS→ESM transform's injected `__name` helper.
- [npm](../../term_dictionary/term_npm.md) — the Node package manager / registry ecosystem; relevance: `tsx`, esbuild, and `pnpm install` (the repro's first step) are all npm-ecosystem packages whose versions the note pins to reproduce the bug.
- [AST](../../term_dictionary/term_ast.md) — abstract syntax tree produced by a parser before code transformation; relevance: esbuild parses TS into an AST and, under `keepNames`, wraps function definitions with `__name(...)` during AST→code emit — the exact mechanism the hypothesis blames.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway being run from source; relevance: this is an OpenClaw operational troubleshooting note — its CLI/gateway is what fails to start.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime scaffolding that boots an agent (logging, auth, tools); relevance: the failing frames (`createSubsystemLogger`, `auth-profiles/constants`) are harness-startup code, not user code.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the class of self-hosted coding-agent gateways; relevance: OpenClaw belongs to this class, and the run-from-source Node toolchain failure is a class-wide operational concern.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — OpenClaw's per-agent credential/identity configuration; relevance: the second crash frame is `src/agents/auth-profiles/constants.ts:25`, i.e. the auth-profiles module is on the failing import chain at startup.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — OpenClaw's agent⇄client RPC protocol layer; relevance: ACP server entry is part of the same CLI/gateway startup path the crash interrupts (`openclaw status` / `gateway:watch`), so an ACP-mode launch hits the same failure.
- [DevOps](../../term_dictionary/term_devops.md) — build/release/runtime operational practice; relevance: the note's substance is dev-toolchain ops — version pinning (`tsx 4.21.0`), runtime selection (Bun vs Node), and build-then-run (`node openclaw.mjs`) workarounds.

- [Claude Code: Install Diagnostics](../claude_code/cc_install_diagnostics.md) — diagnosing a coding agent's install/startup failures; relevance: direct analog procedure for triaging a coding-agent CLI that won't launch.
- [Claude Code: Install Failures Reference](../claude_code/cc_install_failures_reference.md) — reference catalog of install/launch failure modes + fixes; relevance: the `__name` crash is exactly the failure-mode-plus-workaround shape this reference indexes for a sibling agent.
- [Claude Code: SDK TypeScript Installation](../claude_code/cc_sdk_typescript_installation.md) — installing/configuring the TS/Node toolchain for the SDK; relevance: this note diagnoses a breakage of that same TS+Node toolchain (tsx/esbuild loader path).
- [Claude Code: Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — step-by-step config/runtime debugging for a coding agent; relevance: parallel troubleshooting workflow (repro → check versions → isolate → workaround) to this note's structure.
- [Claude Code: Performance and Stability](../claude_code/cc_performance_and_stability.md) — runtime stability/crash troubleshooting for a coding agent; relevance: a startup TypeError crash is a stability failure-class with the same repro-and-mitigate playbook.
- [Claude Code: Update and Release Channels](../claude_code/cc_update_and_release_channels.md) — pinning/rolling agent versions across release channels; relevance: the note's "pin tsx / test Node LTS 22/24" remediation is the same version-pinning discipline this doc describes.
- [Hermes: Installation](../hermes_agent/hermes_installation.md) — installing a sibling coding-agent harness (Node/runtime prerequisites); relevance: same install-time Node-runtime prerequisites whose mismatch produces this crash.
- [Hermes: LSP Diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — TS language-server / type-check diagnostics for a sibling harness; relevance: the workaround uses `tsgo` (type-check then run built output), the same TS-tooling lane this doc covers.
- [Pi: Development](../pi/pi_development.md) — building/running a sibling coding agent from source (dev scripts, toolchain); relevance: direct analog — dev-script toolchain (build vs watch vs run) is exactly where the Bun→tsx regression bites.
- [Pi: Containerization](../pi/pi_containerization.md) — reproducible runtime environments for a sibling agent; relevance: pinning the runtime in a container sidesteps the host Node-25 version skew that triggers the crash.
- [OpenClaw: Install Node](oc_install_node.md) (planned, this series — `in04`) — installing the Node toolchain OpenClaw needs; relevance: the source page's own `/install/node` link and the prerequisite this troubleshooting note assumes.
- [OpenClaw: Gateway Troubleshooting](oc_gateway_troubleshooting.md) (planned, this series — `gw07`) — general gateway troubleshooting; relevance: the source page's own `/gateway/troubleshooting` link; this Node/tsx crash is one entry in the broader gateway-startup troubleshooting set.

- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the top-level OpenClaw codebase run from source; relevance: the dev scripts (Bun→tsx, the `2871657e` regression) and `package.json` runtime config live here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agents module; relevance: contains `src/agents/auth-profiles/constants.ts`, the second file named in the crash stack.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the CLI / setup-wizard module; relevance: the crash surfaces as `Failed to start CLI`, i.e. on this module's startup path.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway server module; relevance: `gateway:watch` (one of the dev scripts that broke) and `createSubsystemLogger` startup logging run inside the gateway boot path.

- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — OpenClaw CLI `runMain` bootstrap; relevance: the exact startup entry whose `Failed to start CLI` path raises the TypeError.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — primary CLI run loop; relevance: the early CLI execution that triggers the import of the failing logging/auth modules.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing (`status`, subcommands); relevance: `openclaw status` (the repro command) dispatches through this routing layer.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root/entry guard; relevance: a pre-command guard in the same startup sequence the crash aborts.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — gateway entry-point dispatch; relevance: `gateway:watch` (broken by the Bun→tsx switch) enters through this dispatch.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime/env detection; relevance: where Node-version / runtime detection happens — the axis (Node 25 vs 22 vs Bun) that determines whether the crash fires.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache / process respawn at startup; relevance: closely tied to the build-then-run (`node openclaw.mjs`) workaround vs the tsx on-the-fly-transform path that fails.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — auth-profiles external-CLI handling; relevance: lives in `src/agents/auth-profiles/`, the module on the crash's second stack frame.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profiles credential ordering / `constants`; relevance: `auth-profiles/constants.ts:25` is the exact line in the crash trace; this snippet documents that constants/credential module.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agents runtime config load; relevance: agents-module config that loads during the same startup chain that imports the failing constants.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — sibling harness's core logging setup; relevance: the first crash frame is `createSubsystemLogger` in `src/logging/subsystem.ts`; this is the analogous subsystem-logger init in the sibling Hermes harness.
- [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — sibling harness core bootstrap; relevance: analog of the early-bootstrap import sequence (before user code) where this Node/tsx loader crash occurs.

**Entry point** (`0_entry_points/` — planned, master pre-step):

**Excluded false-positives (relevance-discarded, not padded):** `term_discriminated_union` / `term_plugin_sdk`
(TS/plugin concepts, not load-bearing to this Node-loader crash), `term_health_check` (the failure is startup,
not a liveness probe), `aws_lambda_nodejs_best_practices` (Lambda-runtime guidance, not a from-source-build
loader crash). Non-existent vocab (`term_esbuild`, `term_bun`, `term_pnpm`, `term_tsx`) is handled inline + in
the Undigested Terms Plan — none promoted.

## Undigested Terms Plan

> Per master: OpenClaw vocab is digested as `oc_*` doc notes by its home sub-plan, never as new
> `term_dictionary` entries; the only `term_dictionary` interaction is LINKING existing terms. Expected 0 new
> term captures for this page. Each candidate below was three-way checked (bm25 + dense + filename grep intent /
> DB existence). No term definition is inlined in the `oc_*` note.

| Term | Disposition |
|---|---|
| Node.js / Node | Link existing `term_node_js` (EXISTING). No capture. |
| TypeScript | Link existing `term_typescript` (EXISTING). No capture. |
| OpenClaw | Link existing `term_openclaw` (EXISTING). No capture. |
| agent harness | Link existing `term_agent_harness` (EXISTING). No capture. |
| `tsx` (TS/ESM Node loader) | Page-local tooling detail; not vault-cross-cutting. Explain inline in `oc_debug_node_issue` as the loader; no new term. NOT promoted. |
| esbuild | Page-local build dependency (the `keepNames`/`__name` source); explain inline in the hypothesis section. No `term_esbuild` exists; not cross-cutting enough to warrant capture. NOT promoted. |
| Bun | Page-local alternative runtime (workaround/regression context); explain inline. No `term_bun` exists; NOT promoted. |
| pnpm | Page-local package-manager command (`pnpm install`/`pnpm tsgo`); incidental. No `term_pnpm`; NOT promoted. |
| `tsgo` / `tsc` | Page-local type-check tooling in the workaround; explain inline. NOT promoted. |
| `keepNames` / `__name` helper | The specific esbuild mechanism at the heart of the crash; explained inline in the note (load-bearing detail, not a reusable vault term). NOT promoted. |
| keepNames esbuild issue (GitHub #1031) | External reference URL only → `## References`. Not a term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an
existing note. (If augment surfaces a reusable cross-cutting term — e.g. a generic "esbuild keepNames helper"
concept recurring across multiple OpenClaw dev pages — it would be captured via `/tessellum-capture-term-note` and
added to a dev-tooling acronym glossary, e.g. `acronym_glossary_gen_ai_dev.md`. Not expected for this single page.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** No new `term_dictionary` notes are created by this sub-plan; only existing terms are linked.
(Inherited from master: were a new term proposed, it would be authored via `/tessellum-capture-term-note` with the

## Per-Phase Validation Gate (G1–G9)

Single execution phase (1 note). Inherited verbatim from the master 9-GATE.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` on `oc_debug_node_issue.md` | YAML field order/tags/keywords/topics valid; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; no forbidden YAML fields. |
| G2 Grounding | Diff note body vs `inbox/openclaw_docs/debug/node-issue.md` | Every claim traces to the source page (stack trace, version matrix, regression commit, workarounds); no invented facts; hypothesis flagged as hypothesis. |
| G3 Density + Coverage | Word/code caps + Section Coverage Map | ≤2500 words, ≤6 code blocks, ≤400 lines; all 11 source H2 mapped to the note (no omission, no over-compression). |
| G4 Cross-Reference | `## Related Notes` per the LOCKED Per-Note Related Notes Mapping: ≥8 `term_dictionary` terms + ≥10 `code_snippets` + ≥10 docs (existing + planned siblings) + `repo_openclaw*`, each indexed `[text](path.md)` with a relevance statement. | ≥8 terms · ≥10 snippets · ≥10 docs (locked: 11t/12s/12d/4repos); all links indexed format; per-link relevance present. |
| G5 Ghost-reference detect + redirect | Every cited EXISTING `note_id` present in DB; planned siblings clearly marked "(planned)". | 0 ghost references (DB-verify; redirect any miss). |
| G6 Broken-link fix | `/tessellum-fix-broken-links` after reindex | 0 broken links from/to the new note. |
| G7/G8 Discoverability | New note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island). | in-degree ≥1 via `entry_openclaw_docs.md` (master W1 pre-step) + any inlinks from §Inlinks. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
# Resolve DB path (single source of truth)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

# --- G5 ghost-reference DB-verify — LOCKED set (all returned 1 on 2026-06-21) ---
for id in \
  resources/term_dictionary/term_node_js.md \
  resources/term_dictionary/term_typescript.md \
  resources/term_dictionary/term_npm.md \
  resources/term_dictionary/term_ast.md \
  resources/term_dictionary/term_openclaw.md \
  resources/term_dictionary/term_agent_harness.md \
  resources/term_dictionary/term_autonomous_coding_agents.md \
  resources/term_dictionary/term_auth_profile.md \
  resources/term_dictionary/term_acp_agent_client_protocol.md \
  resources/term_dictionary/term_devops.md \
  areas/code_repos/repo_openclaw.md \
  areas/code_repos/repo_openclaw_agents.md \
  areas/code_repos/repo_openclaw_cli_wizard.md \
  areas/code_repos/repo_openclaw_gateway.md \
  resources/code_snippets/snippet_openclaw_cli_run_main_bootstrap.md \
  resources/code_snippets/snippet_openclaw_cli_run_main_primary.md \
  resources/code_snippets/snippet_openclaw_cli_route.md \
  resources/code_snippets/snippet_openclaw_cli_root_guard.md \
  resources/code_snippets/snippet_openclaw_gateway_entry_dispatch.md \
  resources/code_snippets/snippet_openclaw_gateway_runtime_env.md \
  resources/code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md \
  resources/code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md \
  resources/code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md \
  resources/code_snippets/snippet_openclaw_agents_runtime_config.md \
  resources/code_snippets/snippet_hermes_agent_core_logging_setup.md \
  resources/code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md \
  resources/documentation/claude_code/cc_install_diagnostics.md \
  resources/documentation/claude_code/cc_install_failures_reference.md \
  resources/documentation/claude_code/cc_sdk_typescript_installation.md \
  resources/documentation/claude_code/cc_debug_your_configuration.md \
  resources/documentation/claude_code/cc_performance_and_stability.md \
  resources/documentation/claude_code/cc_update_and_release_channels.md \
  resources/documentation/hermes_agent/hermes_installation.md \
  resources/documentation/hermes_agent/hermes_lsp_diagnostics.md \
  resources/documentation/pi/pi_development.md \
  resources/documentation/pi/pi_containerization.md ; do
done
# (oc_install_node / oc_gateway_troubleshooting / entry_openclaw_docs = (planned) — expected MISSING until created)

# --- G1/G3/G4 gate sweep (after the note is written) ---
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
python3 scripts/check_note_format.py --path "$GATE_DIR/oc_debug_node_issue.md"
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR/oc_debug_node_issue.md"
# Required-section presence (G1) + source_url presence (REQUIRE_SOURCE_URL)
for f in "$GATE_DIR"/oc_debug_node_issue.md; do
  echo "== $f =="
  grep -Eq "$REQ_SECTIONS" "$f" && echo "REQ_SECTIONS ok" || echo "REQ_SECTIONS MISSING"
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url:' "$f" && echo "source_url ok" || echo "source_url MISSING"; }
  grep -q "$SIBLING_PREFIX" "$f" && echo "sibling ($SIBLING_PREFIX) link present" || echo "no sibling link"
done

# --- G6 broken links + reindex ---
bash scripts/update_notes_database.sh --force
# then: /tessellum-fix-broken-links ; verify note_links populated for the new note (G4/G7)
```

## Density Re-Assessment

| Note | Est. words | Cap (≤2500) | Code blocks | Cap (≤6) | Lines | Cap (≤400) | One BB? | Verdict |
|---|---:|---|---:|---|---:|---|---|---|
| `oc_debug_node_issue.md` | ~450 | ✅ far under | ≤4 (stack trace + ≤3 bash) | ✅ under | ~140 | ✅ under | argument (single) | ✅ no split; comfortably within all caps. |

Borderline check: none. Source is 414w/4-fence; the digest adds an Overview + Related Notes + References framing
and stays ~450w. No section is over-compressed (all 11 H2 represented); no section is bloated.

## Entry Point Decision (inherited from master)

Per master **W1**: a dedicated `0_entry_points/entry_openclaw_docs.md` is created as a pre-step (the OpenClaw-docs
series is >30 notes corpus-wide). This sub-plan does **not** create a new entry point (1 note); it **contributes
its row** to `entry_openclaw_docs.md`:

- **Section row:** under the **Debug** section/sub-plan table — `db01 | Debug | 1 page | oc_debug_node_issue.md`.
- **Note row:** `oc_debug_node_issue.md` — "Node + tsx `__name is not a function` crash: diagnosis + workarounds"
  (argument BB, source `debug/node-issue`).

This contribution supplies the required inbound link (G7/G8 anti-island) into the new note from outside
`documentation/openclaw/`.

## Inlinks (existing notes → new notes)

Candidate inbound links to add at execute (each must be a real, relevance-justified link; from OUTSIDE

| Source note (EXISTING) | → Target | Rationale for inlink |
|---|---|---|
| `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step) | `oc_debug_node_issue.md` | Required navigation/anti-island link; Debug section row (in-degree ≥1). |
| `areas/code_repos/repo_openclaw_agents.md` | `oc_debug_node_issue.md` | The crash stack names `src/agents/auth-profiles/constants.ts` in this repo's module → cross-link code↔docs (add a "Known issues / docs" pointer). |
| `areas/code_repos/repo_openclaw.md` | `oc_debug_node_issue.md` | Top-level repo; dev-scripts (Bun→tsx) toolchain note belongs in its docs cross-links (per master W3 code↔docs wiring pattern). |
| `resources/term_dictionary/term_node_js.md` | `oc_debug_node_issue.md` | (optional) reciprocal: a Node-runtime-specific OpenClaw failure mode, if the term note carries a "See also" list. |

Primary required inlink = `entry_openclaw_docs` (master pre-step). Repo inlinks are the code↔docs reciprocal
bridges; the term inlink is optional and added only if it fits the source note's structure.

## Pacing Rules (inherited from master)

Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script (don't rely on `Workflow` `args`
binding); use `${=VAR}` word-splitting under zsh. This sub-plan is a single-note phase — pilot = execute (no
fan-out needed). Commit per sub-plan / per wave: `git pull --rebase --autostash origin main` first; reindex
incrementally (`bash scripts/update_notes_database.sh --force`); verify `note_links` populated + 0 broken links
before commit; `git push origin main` in the same turn; **no Claude co-author trailer**.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` (this file) | 🟢 DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | 🟢 DONE (xref-augment 2026-06-21 — Related Notes locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE (2026-06-21 — 9/9 PASS → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this augment:** xref-augment — re-read the single source page (`inbox/openclaw_docs/debug/node-issue.md`,
414 measured words) and locked the per-note Related Notes mapping at the **raised floors** (≥8 terms · ≥10 snippets ·
≥10 docs per note). The plan already carried all 15 mandatory sections (section coverage map, split decisions, density
re-assessment, pacing rules, validation scripts incl. ghost-detect, inlink mapping, Undigested Terms Plan with
slug-specificity + collision dedup, Term-Note Authoring Requirements N/A, Entry Point Decision); those are unchanged
and re-verified present.

**What was locked (single planned note):**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| `oc_debug_node_issue.md` | 11 | 12 | 12 (10 existing + 2 planned siblings) | 4 | MET |

  relevance statement tying it to the crash (Node loader path, esbuild AST `keepNames` transform, `auth-profiles`
  stack frame, harness startup, dev-toolchain ops).
  `cli_run_main_primary`, `cli_route`, `cli_root_guard`), gateway boot (`gateway_entry_dispatch`,
  `gateway_runtime_env`, `gateway_compile_cache_respawn`), the `auth-profiles` module on the crash's 2nd frame
  (`auth_profiles_external_cli`, `auth_profiles_order_credential`, `agents_runtime_config`), and the sibling-harness
  logging/bootstrap analogs for the 1st frame (`hermes_core_logging_setup`, `hermes_core_bootstrap_utf8`).
  cc_install_failures_reference, cc_sdk_typescript_installation, cc_debug_your_configuration,
  cc_performance_and_stability, cc_update_and_release_channels, hermes_installation, hermes_lsp_diagnostics,
  pi_development, pi_containerization; planned siblings — oc_install_node (`in04`), oc_gateway_troubleshooting
  (`gw07`). ≥5-existing-doc requirement satisfied (10 existing ≥ 5).
  repo_openclaw_gateway.
- **Entry point:** entry_openclaw_docs (planned, master W1 pre-step) — required G7/G8 inbound link.

**Relevance discards (NOT padded):** `term_discriminated_union`, `term_plugin_sdk` (TS/plugin concepts not
load-bearing to a Node-loader crash), `term_health_check` (startup failure, not a liveness probe),
`aws_lambda_nodejs_best_practices` (Lambda-runtime guidance, not a from-source build-loader crash — dropped from the
original candidate list during relevance review). All discards documented in the mapping section.

**New-term candidates:** none. Re-read surfaced the same page-local tooling vocabulary the plan already dispositioned
(`tsx`, `esbuild`, `Bun`, `pnpm`, `tsgo`/`tsc`, `keepNames`/`__name` helper) — all page-local, none cross-cutting or
vault-reusable, none promoted. Best-fit glossary IF a future cross-OpenClaw dev-tooling term were ever promoted:
`acronym_glossary_gen_ai_dev.md` (not triggered here). 0 new `term_dictionary` captures for this sub-plan.

**DB-verify:** all 11 terms + 12 snippets + 10 existing docs + 4 repos returned `1` from
marked `(planned)` and excluded from the existing-target count.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_db01.md` — Date: 2026-06-21 — Reviewer pass: 9 mandatory checkpoints.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | Locked mapping = 11 terms · 12 snippets · 12 docs · 4 repos for `oc_debug_node_issue`; each link carries `- [Name](relpath.md) — what; relevance: why`. Raised floors (≥8t/≥10s/≥10d) met with margin; no bare links. |
| CP2 | 9-GATE present per batch | **PASS** | Single execution phase; `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference (updated to ≥8t/≥10s/≥10d), G5 Ghost-detect+redirect, G6 Broken-link fix, G7/G8 Discoverability. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)` — contributes Debug section + note rows to `entry_openclaw_docs.md` (master W1 pre-step); no new entry point for a 1-note sub-plan (correct per size rule). |
| CP4 | Size | **PASS** | 1 source page (414w) → 1 note. Far ≤30. Single-note phase; no split needed. |
| CP5 | Format derived | **PASS** | YAML/body format inherited verbatim from master Format Definition, which derives from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (`## Overview` + `## Related Notes`, not invented `## Definition`). G1 enforces it. |
| CP6 | Density | **PASS** | Density Re-Assessment: ~450w / ≤4 code fences / ~140 lines / single argument BB — comfortably under all caps (≤2500w/≤6 code/≤400 lines); no borderline note. |
| CP7 | Sources measured | **PASS** | Source table = 414 measured words (`wc -w` on `inbox/openclaw_docs/debug/node-issue.md`); re-read at this augment confirms 11 H2 / 0 H3 / 4 code fences. Measured, not estimated. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (12 rows, all dispositioned, 0 TBD); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherited mandate stated). New-term candidates: none. |
| CP8f | Slug/collision dedup audit | **PASS** | 0 new term slugs to rename. Collision audit run across term_dictionary AND documentation/: the 1 doc note (`oc_debug_node_issue`) duplicates no existing term/doc (no `oc_debug_*` exists; not a re-name of any `term_*`). Relevance discards documented (no created duplicates). |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks` table: ≥1 outside-folder inbound link planned (entry_openclaw_docs + repo_openclaw_agents + repo_openclaw) → in-degree ≥1; G8-Discoverability in the gate table marked as executed/verified at execute. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
