---
tags:
  - resource
  - analysis
  - argument
  - system_review
  - audit
  - cqrs
  - dks
  - composer
keywords:
  - system review
  - src/tessellum audit
  - CQRS boundary check
  - DKS runtime gap
  - composer contract validation
  - architectural consistency
topics:
  - System Architecture
  - Audit
  - Code Review
  - Tessellum Foundations
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
---

# System Review: `src/tessellum/` Through CQRS, DKS, and Composer Lenses

## Thesis

The Tessellum codebase (9,469 LOC across 7 packages) **internally satisfies its three architectural commitments** — CQRS read/write separation, DKS as a typed-vocabulary commitment, and the Composer planner-centric typed-contract pattern. Where pieces are missing, the deferred status is correctly documented in vault notes. The single concrete bug is that the compiler advertises MCP-contract validation but does not implement it; the rest of the audit findings are documentation drift and one stale docstring. A two-hour PR can close every concrete gap.

This note records the audit findings as of v0.0.36 so a future contributor can compare-and-contrast — both to verify the invariants still hold, and to see which deferred items have since landed.

## Audit scope

| Package | LOC | Role |
|---------|----:|------|
| `format/` | 1,096 | Validator + parser + closed-enum spec |
| `indexer/` | 777 | Vault → SQLite unified-engine build |
| `retrieval/` | 1,020 | BM25 + dense + hybrid + BFS + metadata filter |
| `composer/` | 3,580 | Typed-contract pipeline runtime (the largest subsystem) |
| `cli/` | 2,116 | Six CLI subcommand dispatchers |
| `capture.py` + `init.py` | 653 | Note authoring + vault scaffold |
| `__init__.py` + `__about__.py` + `data/` | 289 | Package-level glue |
| **Total** | **9,469** | |

## Lens 1 — CQRS (System P ⊥ System D ⊥ shared substrate)

CQRS is defined in [`term_cqrs`](../term_dictionary/term_cqrs.md) and synthesised in [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md). The shape: System P (writes — Composer, capture, init) and System D (reads — indexer, retrieval) operate on one substrate (`vault/`) with **one boundary** between declaration and computation.

### What's working

| Boundary | Verdict | How verified |
|----------|---------|--------------|
| `composer/` doesn't import `retrieval/` or `indexer/` | ✓ clean | `grep -rn "tessellum.retrieval\|tessellum.indexer" src/tessellum/composer/` is empty |
| `retrieval/` and `indexer/` don't import `composer/` | ✓ clean | reverse grep is empty |
| Materializers write only under `vault_root` | ✓ clean | 5 `target.write_text()` calls in `materializer.py`, all resolved from `vault_root` |
| Indexer writes only to `data/` | ✓ clean | `db.unlink()` + `sqlite3.connect()` are the only mutations; both target `data/` |
| Retrieval writes nothing | ✓ clean | no `write_text` / mutating SQL in `retrieval/*` |
| Trace files (`runs/composer/`) live outside both systems | ✓ correct | scheduler + batch write only to `runs_dir` (default `runs/composer/`) |
| `tessellum capture` doesn't query the index | ✓ clean | `capture.py` has zero `indexer`/`retrieval` imports |
| CLI imports flow one-way (CLI → engines, never reverse) | ✓ clean | `cli/*` is the only place that pulls everything together |

The two-system split is honored at the **import-graph** level. A future architectural change that violates it would surface immediately in `grep`-able cross-imports.

### Gaps

1. **No test enforcing these invariants.** Boundaries are observed today; nothing prevents an unwary contributor from breaking them. A `tests/architecture/test_cqrs_boundaries.py` (~20 LOC) that scans imports and asserts the four invariants would lock the property into CI.
2. **Two slightly-different "master TOC" surfaces** — the dogfood `vault/0_entry_points/entry_master_toc.md` and the runtime-generated `init.py:_render_master_toc()` have diverged in content depth. This is *intentional* (different audiences) but creates a documentation-drift risk.

## Lens 2 — DKS (closed-loop 7-component dialectic)

DKS is the closed-loop dialectic protocol synthesised in [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md): 7 components × 3 formal foundations × 2 timescales × 1 termination criterion.

### What ships

- **As typed vocabulary** ✓ — `counter_argument` is one of the 8 BB types; `argument → counter_argument` is one of the 10 epistemic edges declared in `format/building_blocks.py`.
- **As documented design** ✓ — Trail 2 records the six-step descent (FZ 2) and the 7-component synthesis (FZ 2a).
- **As one DKS-shaped skill** ✓ — `skill_tessellum_write_coe` is a one-shot dialectic instance (5 Whys → counter-argument-as-root-cause → action items).

### Gaps

1. **No DKS runtime module.** Search for `dialectic | gap_report | warrant_revision` in `src/tessellum/` returns hits only in template strings and seed-vault paths. There is **no closed-loop dispatcher**, no "argument generator A vs B" component, no `pattern_discovery.py`, no `rule_improvement.py`. The 7-component cycle exists in vault notes but not in code.
   - This is **accurately disclosed** in `thought_dks_design_synthesis.md` ("the 7-component runtime is the substantial v0.2+ delta"). Known deferred gap, not a stealth one.
   - A placeholder `composer/dks.py` with one `NotImplementedError` + a docstring linking to the synthesis would signal the deferred work in the code itself, not only in the vault.
2. **BB ontology edges are declared but not enforced at runtime.** `EPISTEMIC_EDGES` is a tuple in `building_blocks.py`; nothing in the validator or compiler asks "does this counter_argument actually attack an existing argument?" The graph relationship lives in the data but isn't a load-bearing invariant. Same DKS-runtime gap, surfaced differently.
3. **COE skill is the *only* "review and reflect" surface today.** Correctly DKS-shaped but doesn't feed back — completing a COE doesn't *change* any warrants that future arguments rest on. The closed loop is open by design at this stage.

## Lens 3 — Composer (planner-centric typed-contract orchestrator)

Composer is the most disciplined subsystem. Every contract declared in the schema is checked at compile time before any LLM call fires.

### What's working

| Property | Verdict | Evidence |
|----------|---------|----------|
| Skill = canonical body + paired `.pipeline.yaml` sidecar | ✓ enforced | `skill_extractor.load_pipeline_metadata()` resolves `pipeline_metadata:` frontmatter; loader validates against `pipeline.schema.json` |
| Section anchors load-bearing for prompt extraction | ✓ enforced | `<!-- :: section_id = X :: -->` regex; compiler extracts per-step section text |
| Materializer key must resolve in `MATERIALIZER_CONTRACTS` | ✓ enforced | `compiler.py:281` raises `ContractViolation(KIND_UNKNOWN_MATERIALIZER)` |
| `expected_output_schema.required` covers materializer's required fields | ✓ enforced | compiler raises `KIND_MISSING_REQUIRED_OUTPUT_FIELD` |
| Topological sort + cycle detection | ✓ enforced | `_topological_sort()` + DFS cycle check in `compiler.py` |
| 5 materializers × 3 operation verbs separation | ✓ clean | `materializer.py` has a single dispatch table; each handler is independently testable |
| LLM backend pluggable via Protocol | ✓ clean | `MockBackend` + `AnthropicBackend` share `LLMBackend`; same dispatch through `executor.execute_step()` |
| `runs/composer/` traces are the bridge artifact | ✓ correct | scheduler writes trace JSON to `runs_dir`; never to `vault/` or `data/` |
| **session-mcp shipped (v0.0.36)** with `MCPContract` registered | ✓ partial — contract registered, dispatcher absent | session-mcp is in `MCP_CONTRACTS`; the stdio server exists; runtime invocation is up to the agent |

### Gaps

1. **`mcp_dependencies` is NOT validated by the compiler.** *(The most concrete bug surfaced by the audit.)*
   - `contracts.py` declares `MCPContract` Pydantic model ✓
   - `MCP_CONTRACTS` registry is populated (now ships `session-mcp`) ✓
   - `loader.py` parses `mcp_dependencies:` field in the sidecar ✓
   - `compiler.py` does **NOT** walk `step.mcp_dependencies[*]` to check that each `name` resolves in `MCP_CONTRACTS` and each `calls[*]` is in the contract's `available_tools` ✗

   The `contracts.py` docstring promises this validation ("*The compiler asserts every step's declared `mcp_dependencies` resolves against the `MCP_CONTRACTS` registry, and that each tool name in `mcp_dependencies[].calls` is in this contract's `available_tools`*") but the assertion isn't implemented. A user writing `mcp_dependencies: [{name: nonexistent-mcp, calls: [fake_tool]}]` gets no compile-time error today.

   **Fix shape**: ~30 LOC in `_compile_step()` mirroring the materializer-validation pattern. Add `KIND_UNKNOWN_MCP` + `KIND_UNKNOWN_MCP_TOOL` to `ContractViolation`. ~1 hour including tests.

2. **`llm_backend` contract validation also missing.** Same shape: `BACKEND_CONTRACTS` is in `contracts.py` (with `mock` and `anthropic` entries) but the compiler doesn't validate that a step's chosen backend (if specified) resolves. Less urgent because backends are typically global, not per-step.

3. **`compiler.py:26` docstring lies about MCP validation.** Lines 26-27 say *"LLMBackendContract / MCPContract validation. Backends + MCPs ship in Wave 4; the compiler will gain those checks then."* — this is stale (we're past Wave 4) AND it admits the gap. The docstring should be updated when the validation is implemented.

4. **Two undocumented validator codes**: `YAML-011` (tags must be a list) and `YAML-012` (tags must have ≥ N entries) are emitted by the validator but missing from [`term_format_spec`](../term_dictionary/term_format_spec.md)'s issue-code reference table.

5. **`templates_dir()` docstring says "13 BB-type templates"** but `vault/resources/templates/` now ships 17 files (15 .md + 1 .yaml + 1 README). Drift from when `template_code_snippet.md` and `template_code_repo.md` were added in v0.0.24.

6. **`cli/composer.py` is 1069 LOC** — by far the largest single file in the codebase. Six subcommands at ~180 LOC each. Functional but a future split into `cli/composer/{validate,compile,run,batch,eval,scaffold}.py` would parallel the modular shape of the engine side.

## Cross-cutting findings

### Three-way agreement on the per-flavor mapping

I cross-checked: [`term_format_spec`](../term_dictionary/term_format_spec.md)'s "Filename + Directory Conventions" table, [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md)'s "Default directory" column, and `capture.REGISTRY` (the actual code) **all agree** on the per-flavor mapping. Three places, one truth — and they're in sync as of v0.0.36.

### Documentation drift surfaces

| Drift | Code says | Docs say |
|-------|-----------|----------|
| Templates count | 17 actual files | "13 BB-type templates" in `data/__init__.py` |
| Validator codes | 28 codes emitted | 26 in `term_format_spec.md` (YAML-011 + YAML-012 missing) |
| Composer docstring | MCP validation implemented in registry, not in compiler | `compiler.py:26` claims it's future Wave 4 work |

All three are one-line fixes.

### What's deferred and recorded

| Deferred item | Recorded in | Future trigger |
|---------------|-------------|-----------------|
| DKS runtime (`composer/dks.py`) | `thought_dks_design_synthesis.md` "What ships today" | v0.2+ |
| MCP dispatcher (runtime invocation, not just contract) | `plan_composer_port.md` | when more skills need real MCP routing |
| OpenAI / local LLM backends | `plan_composer_port.md` | when a user asks |
| `tessellum.toml` per-vault config | `plan_v01_src_tessellum_layout.md` | when a real config knob requires it |
| Eval pipeline recording `(query, retrieved, answer, rating)` tuples | `thought_retrieval_synthesis.md` | v0.2+ |

These are correctly recorded; future contributors can find them.

## Prioritised fix list

A two-hour PR can close every concrete gap surfaced by this audit:

| # | Fix | Lens | Effort | Why |
|---|-----|------|--------|-----|
| 1 | Implement `mcp_dependencies` validation in `compiler.py` (and `llm_backend`) | Composer | ~1-2 h | Stops the docstring from lying; closes the last unimplemented contract |
| 2 | Add `tests/architecture/test_cqrs_boundaries.py` (import-graph assertions) | CQRS | ~30 min | Locks in what's currently true |
| 3 | Add `YAML-011` + `YAML-012` rows to `term_format_spec.md` | Format | ~5 min | Closes documentation drift |
| 4 | Update `templates_dir()` docstring (13 → 15 templates) | Misc | ~2 min | Drift fix |
| 5 | Update `compiler.py:26` docstring to reflect post-Wave-4 reality | Composer | ~5 min | Drift fix |
| 6 | Add placeholder `composer/dks.py` with `NotImplementedError` + docstring linking to FZ 2a | DKS | ~10 min | Signals the deferred work in code, not just in vault |
| 7 | Consider splitting `cli/composer.py` into per-subcommand modules | Composer | ~1 h | Quality-of-life; not load-bearing |

Items 1-5 are the load-bearing fixes; item 6 is signalling; item 7 is style.

## Verdict

The codebase is **internally consistent on all three architectural lenses**. The CQRS boundary is held at the import-graph level. The Composer typed-contract discipline is enforced at compile time (modulo the MCP-validation gap). DKS is honored in the vocabulary but not yet in the runtime — and that gap is properly disclosed.

The single concrete bug worth fixing soon is the MCP validation gap (item #1). The rest is documentation drift that surfaces while reading the codebase end-to-end.

## Related Notes

- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — the one-boundary thesis this audit checks the codebase against
- [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — FZ 2a — the 7-component synthesis whose runtime is the load-bearing DKS gap
- [`thought_retrieval_synthesis`](thought_retrieval_synthesis.md) — FZ 3a — the System-D synthesis the retrieval-side audit checks against
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — System P ⊥ System D ⊥ substrate
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical
- [`term_format_spec`](../term_dictionary/term_format_spec.md) — the format contract (target of audit findings #3, #4)
- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the architectural pivot

## See Also

- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map (this note could become the root of a future "system reviews" trail if more reviews are added)
- [`entry_master_toc`](../../0_entry_points/entry_master_toc.md) — vault navigation root

---

**Last Updated**: 2026-05-10
**Status**: Active — snapshot as of v0.0.36
