---
tags:
  - project
  - plan
  - tessellum
  - v0_1_0
  - public_beta
  - roadmap
keywords:
  - v0.1.0 completion
  - public beta roadmap
  - deferred surface closure
  - argument_perspective
  - bb_schema_version validator
  - multi-revision authoring
  - MCP server
  - CI workflow
  - seed vault skills
  - BB-type example notes
topics:
  - Tessellum
  - Release Planning
  - v0.1.0 Public Beta
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
---

# Plan — v0.1.0 Completion Roadmap

## Problem

Two plans are now fully shipped:

- `plan_dks_expansion.md` — Phases 6-10 landed at v0.0.48 through v0.0.54. DKS is feature-complete: 7-component closed loop + multi-cycle orchestration + retrieval-grounded warrants + learned confidence + FSM dispatcher + meta-DKS schema-mutation runtime + multi-perspective debate with Dung grounded labelling.
- `plan_meta_dks_validation_and_polish.md` — Phase V (validation evidence at FZ 2c1a) + Phase B (six deferred items: composer skill canonical, LLM proposer, LLM attacker, `bb_schema_version` auto-population, `tessellum bb migrate`, BBGraph integration) shipped at v0.0.53.

What remains splits into two scopes:

1. **Surface-closure items** I shipped half-done during the alpha sequence:
   - Multi-revision authoring when `surviving_argument_fzs` has N>1 (Phase 10 emits one revision regardless)
   - Version-aware TESS-005 that *consumes* the `bb_schema_version` we now write on capture (Phase B records the field; the validator still validates against the live `BB_SCHEMA`)
   - `argument_perspective:` YAML field on argument notes (Phase 10 D5 deferred)
   - Hatch `force-include` for `vault/resources/templates/` so they ship in the wheel (status uncertain; verify)

2. **v0.1.0 public-beta product scope** from the CHANGELOG's "Planned for v0.1.0" list:
   - 20 essential skills (only 11 ship today)
   - 8 BB-type example notes (teaching-grade exemplars, one per BB type)
   - Conceptual primer term notes (Z, PARA, BB, Epistemic Function, DKS, CQRS)
   - Public-facing how-to library (4 guides: getting-started, note-format, agent-integration, growing-a-trail)
   - MCP server exposing v0.1 skills (`src/tessellum/mcp/` is currently a `.gitkeep` placeholder)
   - CI workflow (no `.github/workflows/` exists today)

The strategic question is sequencing — surface-closure first vs pivot-to-product first vs interleaved. This plan picks a sequencing, sequences the six remaining versions to v0.1.0, and specifies what each must ship.

## Priority rationale

Five criteria, in order:

1. **Closure-of-deferral first.** Items shipped half-done are easier to finish while context is hot. Multi-revision, version-aware TESS-005, and `argument_perspective:` are all in code paths I touched in v0.0.53-v0.0.54. The longer they wait, the more re-learning each refactor costs.
2. **Infrastructure before content.** A CI workflow protects every future release; landing it before authoring 20 skills + how-tos means PR-time regression detection catches the inevitable typos before content lands.
3. **Substrate before product surface.** Primer term notes and BB-type example notes teach the substrate; they're the foundation skill canonicals and how-tos reference. Author them first.
4. **Internal-facing before external-facing.** A good seed vault for self-use proves the substrate works before we polish for external eyes. Skill canonicals and how-tos depend on stable substrate.
5. **MCP server last.** It's a thin shim over the existing skill canonicals; safer to author once the skills are stable. Authoring earlier would create churn each time a skill canonical changes.

Two criteria do *not* drive priority:

- **Risk avoidance** isn't a tie-breaker — every remaining item is low-risk (additive, well-bounded). Skipping in priority for risk would invent reasons to defer.
- **User-visibility** isn't a tie-breaker either — alpha is alpha; we're not optimising for the next external eyeball yet. The v0.1.0 cut is the milestone where visibility matters.

The resulting sequence: surface closures (v0.0.55), CI (v0.0.56), substrate content (v0.0.57), skills (v0.0.58), MCP + how-tos (v0.0.59), public-beta cut (v0.1.0).

## What's already shipped (v0.0.54 baseline)

| Surface | Status | Where |
|---------|--------|-------|
| DKS — 7-component closed loop | ✓ | `tessellum.dks.core` |
| DKS — multi-cycle orchestration | ✓ | `DKSRunner` |
| DKS — confidence gating + learned calibration | ✓ | `tessellum.dks.confidence` |
| DKS — P-side retrieval client | ✓ | `tessellum.dks.retrieval_client` |
| DKS — warrant persistence + history | ✓ | `tessellum.dks.persistence` |
| DKS — FSM dispatcher | ✓ | `tessellum.dks.fsm` |
| DKS — meta-DKS (event-sourced schema + MetaCycle) | ✓ | `tessellum.dks.meta` |
| DKS — Dung grounded labelling | ✓ | `tessellum.dks.dung` |
| DKS — N-perspective cycle | ✓ | `DKSCycle.perspectives` kwarg |
| BB ontology — schema graph + corpus graph | ✓ | `tessellum.bb` |
| BB — `unrealised_schema_edges()` helper | ✓ | `BBGraph` |
| Composer — pipeline executor + LLM backends | ✓ | `tessellum.composer` |
| Retrieval — hybrid (BM25 + dense + graph) | ✓ | `tessellum.retrieval` |
| Indexer — unified SQLite + FTS5 + sqlite-vec | ✓ | `tessellum.indexer` |
| Format — TESS-001..TESS-005 validators | ✓ | `tessellum.format` |
| Capture — 14 typed templates + `bb_schema_version` field | ✓ | `tessellum.capture` |
| CLI — `dks` / `bb audit|migrate` / `capture` / `composer` / `format check` / `fz` / `index build` / `init` / `search` | ✓ | `tessellum.cli` |
| Vault — 18 FZ trail nodes across 3 trails | ✓ | `vault/resources/analysis_thoughts/` |
| Skill canonicals | 11 / 20 target | `vault/resources/skills/` |
| Templates | 14 (all 8 BB types covered) | `vault/resources/templates/` |
| MCP server | 0% — placeholder only | `src/tessellum/mcp/.gitkeep` |
| CI workflow | absent | `.github/workflows/` does not exist |
| How-to library | 1 / 4 target | `vault/resources/how_to/howto_first_vault.md` |
| BB-type example notes | 0 / 8 target | not yet authored |
| Primer term notes | partial (DKS + CQRS exist; Z + PARA + BB + Epistemic-Function gap-checked) | `vault/resources/term_dictionary/` |
| Tests | 844 passing | `tests/` |

## Resolved decisions

| # | Question | Resolution | Rationale |
|---|----------|------------|-----------|
| **D-1** | Should multi-revision authoring change `DKSRuleRevision` itself (multiple revisions per cycle) or stay one-per-cycle with caller-side selection? | **Multiple revisions per cycle**, emitted in the `DKSCycleResult.rule_revisions` *tuple* (additive; legacy `rule_revision` stays as `rule_revisions[0]` for back-compat) | The plan's stated outcome ("emits multiple revisions tagged with their FZs") matches what `surviving_argument_fzs` semantically implies. Caller-side selection would defer the question to every downstream consumer. |
| **D-2** | Version-aware TESS-005: store schema snapshots, or reconstruct from event log? | **Reconstruct from event log** via new `BB_SCHEMA_AT_VERSION(n)` helper | The event log is the source of truth (Phase B.1's D3). A snapshot table would duplicate state and risk drift. Reconstruction is O(events × edges per fold) — trivial. |
| **D-3** | `argument_perspective:` field — closed enum or open string? | **Open string with conventional values** (`conservative`, `exploratory`, `empirical`, ...). Same shape as `DKSCycle.perspectives`. | Closed enums force a vocabulary churn every time someone tries a 4th perspective. The runtime already accepts arbitrary strings. |
| **D-4** | CI provider: GitHub Actions, GitLab CI, or something else? | **GitHub Actions** | The repo lives at GitHub; native integration is free. No need to import a multi-provider abstraction at v0.1.0. |
| **D-5** | MCP server: standalone process (FastMCP / mcp-python) or in-process via `mcp_python_sdk`? | **Standalone process via the official `mcp` Python SDK** | Matches Anthropic's reference pattern. Skills become MCP tools 1:1; no executor surface to invent. |
| **D-6** | 20 essential skills — which 20? | **Resolved as** 5 capture + 5 search/answer + 5 trail management + 5 maintenance. Specific list in Phase IV §4.2 below. | Symmetry. The product surface needs balanced coverage across the substrate's four operational modes (write / read / reason / maintain). |
| **D-7** | BB-type example notes: synthesise for v0.1.0, or hand-pick from existing vault? | **Synthesise minimal exemplars** — one new note per BB type, designed specifically to be teaching examples (short, clean, cross-referencing the template) | Existing vault notes mix substantive content + format examples; the teaching role is muddier. Dedicated exemplars are clearer. |
| **D-8** | Should v0.1.0 PyPI release be a real beta tag, or just version `0.1.0`? | **Just `0.1.0`** (no `0.1.0b1` rc cycle) | Tessellum's PyPI history is already alpha-shaped; cutting `0.1.0` cleanly is the right discontinuity. RC cycles add ceremony without catching anything `0.0.54`-era testing hasn't already caught. |

## Phase I — v0.0.55 — Close deferred alpha surface (small, ~600 LOC)

**Goal**: finish the three Phase 10/B items shipped half-done. Refactor risk lowest while context is hot.

### I.1 — Multi-revision authoring (D-1)

- New field `DKSCycleResult.rule_revisions: tuple[DKSRuleRevision, ...]` — full set of revisions the cycle emits.
- Legacy `rule_revision: DKSRuleRevision | None` stays — populated as `rule_revisions[0] if rule_revisions else None` for back-compat.
- `DKSCycle._run_n_perspective` extension:
  - When `surviving_argument_fzs` has multiple IN labels AND the cycle reached step 7, emit *one revision per surviving FZ*. Each revision targets the surviving argument's warrant; `supersedes` references the IN argument's prior warrant if one is being replaced.
  - For N=2, emit a single revision (today's behaviour).
- `DKSRunner.run` extension:
  - Iterate `cycle.rule_revisions` (not `.rule_revision`) when threading warrant changes. Each revision becomes one or more `WarrantChange` entries.
- CLI trace serialiser: emit `rule_revisions: [...]` alongside the existing `rule_revision` field (both present; latter is `rule_revisions[0]` for compatibility).
- Tests: 5-8 new — N=3 cycle with 2 IN survivors emits 2 revisions; N=2 unchanged; legacy `rule_revision` getter still works.

### I.2 — Version-aware TESS-005 (D-2)

- New helper `tessellum.bb.types.BB_SCHEMA_AT_VERSION(n: int) -> tuple[EpistemicEdgeType, ...]`:
  - Reads `_SCHEMA_EVENT_LOG`; folds events whose post-fold version number is `≤ n`.
  - Returns the core epistemic edges (always present) + the version-`n` user extensions.
  - Caches per-`n` for perf.
- TESS-005 (`_check_bb_typed_edges`):
  - Reads `note.frontmatter.get("bb_schema_version")`. If present and integer, validate against `BB_SCHEMA_AT_VERSION(recorded_version)` instead of live `BB_SCHEMA`.
  - Issue message includes the version: "BB-pair not in BB_SCHEMA@v3 in either direction; current schema is v5."
  - Back-compat: missing/non-integer version → default to live `BB_SCHEMA` (today's behaviour).
- `tessellum bb migrate`:
  - Now consumes the version-aware validator. Previously this was the "behaviour change deferred to B.5" — now it lands.
- Tests: 6-8 new — note with `bb_schema_version: 2` validates against schema-as-of-v2 even when live is v5; behaviour change is observable.

### I.3 — `argument_perspective:` YAML field (D-3)

- `tessellum.format.frontmatter_spec`: add `argument_perspective: str | None` as an optional field on `argument`-typed notes. No validator enforcement at v0.0.55 (just spec'd).
- `tessellum capture argument`: template gains `argument_perspective: ""` placeholder.
- Composer skill canonical `skill_tessellum_dks_cycle.pipeline.yaml`:
  - Step 2 prompt emits `argument_perspective: "conservative"` in frontmatter.
  - Step 3 prompt emits `argument_perspective: "exploratory"`.
  - N>2 prompts (Phase 10) emit the user-supplied perspective string.
- Meta-DKS observation builder (`_run_dks_meta`):
  - When building `MetaObservation`, stratify `counter_strength_breakdown` and `sample_counter_quotes` by `argument_perspective` from the cycle traces. Surface as new `MetaObservation.per_perspective_breakdown: dict[str, dict[str, dict[str, int]]]` field (additive, default empty).
- Tests: 4-6 new — capture writes the field; spec validator allows it; meta-DKS observation surfaces it; non-N=2 perspective string carried through traces.

### Exit criteria

- 844 → ~860 tests passing (15-20 new).
- Clean-venv wheel imports + `tessellum dks` + `bb migrate` work.
- CHANGELOG entry + commit + push + PyPI.

## Phase II — v0.0.56 — CI workflow + force-include verification (small, ~150 LOC + YAML)

**Goal**: every future PR gets ruff + pytest + format-validator pre-merge. Wheel ships with templates.

### II.1 — GitHub Actions CI workflow

- `.github/workflows/ci.yml`:
  - Triggers: push to `main`, all pull requests.
  - Matrix: Python 3.11 + 3.12 (3.11 is `tessellum`'s minimum per `pyproject.toml`).
  - Jobs:
    - `lint`: `pip install ruff && ruff check src/ tests/`
    - `test`: `pip install -e .[agent,dev] && pytest tests/`
    - `format-validator`: `pip install -e . && tessellum format check vault/resources/**/*.md` (verifies the seed vault passes its own validators)
    - `build`: `pip install hatch && hatch build` — fails if wheel build breaks
  - Optional `[dev]` extra in `pyproject.toml` for `pytest`, `pytest-asyncio`, `pytest-cov` (currently they install via the venv but aren't declared).

### II.2 — Hatch force-include for templates

- Verify `vault/resources/templates/` ships in the wheel:
  - `pip install dist/tessellum-0.0.55-py3-none-any.whl && python -c "from tessellum.data import templates_dir; import os; print(os.listdir(templates_dir()))"`
  - If templates aren't included, add `[tool.hatch.build.force-include]` block to `pyproject.toml`:
    ```toml
    [tool.hatch.build.force-include]
    "vault/resources/templates" = "tessellum/data/templates"
    ```
  - Update `tessellum.data.templates_dir()` to find the wheel-installed location if needed.

### II.3 — Tests + checks

- CI workflow itself becomes the test — first push to main exercises every job.
- Re-run clean-venv smoke against the v0.0.56 wheel to confirm templates ship.

### Exit criteria

- CI green on a no-op PR.
- Clean-venv install + `tessellum init <somewhere>` works (init reads templates from the package).
- CHANGELOG + commit + push + PyPI.

## Phase III — v0.0.57 — Seed vault content (medium, ~14 notes + light skill work)

**Goal**: the substrate teaches itself. 8 BB-type exemplars + primer term notes that explain the typed-knowledge pattern.

### III.1 — 8 BB-type example notes (D-7)

One minimal teaching example per BB type. Naming convention: `example_<bb_type>_*.md`. Each:
- Short (≤ 150 lines body).
- Cross-references its template.
- Demonstrates the BB type's *epistemic role*, not just its formal shape.
- Lives under the type's canonical directory.

| BB type | Example note | Teaching role |
|---------|--------------|---------------|
| `empirical_observation` | `example_empirical_observation_dks_cycle.md` | A DKS cycle observation drawn from a real run |
| `concept` | `example_concept_warrant.md` | What Toulmin's "warrant" actually denotes |
| `model` | `example_model_argument_attack_pattern.md` | A small pattern about which warrants get attacked |
| `hypothesis` | `example_hypothesis_meta_dks_value.md` | A testable hypothesis about meta-DKS's contribution |
| `argument` | `example_argument_for_typed_notes.md` | One concrete argument for the substrate's value |
| `counter_argument` | `example_counter_argument_against_closed_loop.md` | A specific counter to the closed-loop claim |
| `procedure` | `example_procedure_running_dks_cycle.md` | Step-by-step "how to run one DKS cycle" |
| `navigation` | `example_navigation_dks_trail.md` | An entry-point-style index over the DKS trail |

### III.2 — Conceptual primer term notes

Gap-check + author missing notes:

| Term | Already exists? | If not, author |
|------|-----------------|----------------|
| `term_zettelkasten` | ✓ (verify) | If missing: 1 page on Z principles + the typed-knowledge variant |
| `term_para` | check | If missing: 1 page on the PARA buckets + Tessellum's `tags[0]` mapping |
| `term_building_block` | check | If missing: 1 page on the 8 BB types + their epistemic-edge graph |
| `term_epistemic_function` | check | If missing: 1 page on the role of typed warrants in epistemic load-bearing |
| `term_dialectic_knowledge_system` | ✓ | (already exists) |
| `term_cqrs` | check | If missing: 1 page on R-P / R-D / R-Cross + the productive halves |

Cross-link all primer terms to the BB-type examples (§III.1) so a reader following primer → example sees the typed pattern in action.

### III.3 — Seed manifest updates

Add every new note from §III.1 and §III.2 to `src/tessellum/data/_seed_manifest.py` so they ship in the seed vault.

### Exit criteria

- All 8 BB-type examples + ≥ 4 primer terms exist and pass `tessellum format check`.
- Seed manifest updated; clean-venv `tessellum init <dir>` produces a vault containing them.
- CHANGELOG + commit + push + PyPI.

## Phase IV — v0.0.58 — Skill canonical library (medium, ~20 canonicals + sidecars)

**Goal**: 20 essential skills, balanced across the substrate's four operational modes.

### IV.1 — Skill canonical inventory

| Mode | Skills (target = 5 per mode) | Already exists? |
|------|-------------------------------|-----------------|
| **Capture** | `tessellum-capture-empirical-observation` | author |
| | `tessellum-capture-argument` | author |
| | `tessellum-capture-counter-argument` | author |
| | `tessellum-capture-concept` | author |
| | `tessellum-capture-procedure` | author |
| **Search/Answer** | `tessellum-search-notes` | ✓ (verify) |
| | `tessellum-answer-query` | ✓ (verify) |
| | `tessellum-traverse-folgezettel` | ✓ (verify) |
| | `tessellum-summarise-trail` | author |
| | `tessellum-find-related` | author |
| **Trail mgmt** | `tessellum-append-to-trail` | ✓ (verify) |
| | `tessellum-manage-folgezettel` | ✓ (verify) |
| | `tessellum-branch-trail` | author |
| | `tessellum-extend-trail` | author |
| | `tessellum-merge-trail-summaries` | author |
| **Maintenance** | `tessellum-format-check` | ✓ (verify) |
| | `tessellum-write-coe` | ✓ (verify) |
| | `tessellum-rebuild-index` | author |
| | `tessellum-validate-bb-graph` | author |
| | `tessellum-bump-schema-version` | author |

Each new canonical follows the proven shape (today's 11 skills are the reference): description + setup + resources + step-by-step procedure + error handling + important constraints + sidecar YAML.

### IV.2 — `tessellum capture skill <slug>` already exists (D8.4 from earlier work)

Use it to scaffold each new canonical's frontmatter + sidecar pair. Saves hand-authoring of frontmatter.

### IV.3 — Skill canonical tests

Per skill: smoke test that the canonical + sidecar compile via `tessellum composer compile`. No end-to-end LLM runs at v0.0.58 — just structural validation.

### Exit criteria

- 20 skill canonicals + 20 paired sidecars in `vault/resources/skills/`.
- `tessellum composer compile <each>` returns 0 for all 20.
- Seed manifest updated.
- CHANGELOG + commit + push + PyPI.

## Phase V — v0.0.59 — MCP server + how-to library (medium, ~400 LOC + 4 how-tos)

**Goal**: external agents can invoke Tessellum skills as MCP tools; new users can follow guides to write their first vault.

### V.1 — MCP server (D-5)

- `src/tessellum/mcp/__init__.py` + `src/tessellum/mcp/server.py`:
  - Uses `mcp` Python SDK.
  - Exposes every skill canonical as one MCP tool (`tessellum_<skill_name>`).
  - Tool schemas derived from each sidecar's `expected_output_schema`.
  - Server entry point: `tessellum mcp serve` (new CLI subcommand).
- Each tool invocation pipes through `tessellum.composer.executor` — same code path as `tessellum composer run`.
- Tests: smoke test that the server can be instantiated, lists tools, and handles one minimal tool call (mock backend).

### V.2 — How-to library

4 guides under `vault/resources/how_to/`:

| Slug | Audience | Topic |
|------|----------|-------|
| `howto_getting_started.md` | new users | install + `tessellum init` + `tessellum capture argument` + open the result |
| `howto_note_format.md` | new users | YAML frontmatter spec — required fields, building_block enum, folgezettel pairing, `bb_schema_version` |
| `howto_agent_integration.md` | agent developers | invoke Tessellum skills from Claude Code / MCP / direct Composer pipeline |
| `howto_growing_a_trail.md` | knowledge curators | author the first FZ trail node, extend it, branch it, run `tessellum-append-to-trail` |

Each how-to is `building_block: procedure`, mid-length (~200 lines), cross-references the relevant primer terms (Phase III.2) + skill canonicals (Phase IV.1).

### V.3 — Seed manifest + entry-point updates

- Add new how-tos + MCP server-related notes (if any) to `_seed_manifest.py`.
- Update `entry_skill_catalog.md` to list all 20 skills.
- Add a new entry point `entry_mcp_tools.md` listing the MCP-exposed tools.

### Exit criteria

- `tessellum mcp serve` runs and responds to MCP `list_tools` + `call_tool`.
- 4 how-tos pass format check + render readably in markdown viewers.
- CHANGELOG + commit + push + PyPI.

## Phase VI — v0.1.0 — Public beta cut (small, mostly release ceremony)

**Goal**: cut a clean `0.1.0` release with a polished README, PyPI presence, and GitHub release notes.

### VI.1 — README polish

- `README.md`:
  - Top-of-fold: one-sentence pitch ("Typed atomic notes in a graph — a Zettelkasten that scales").
  - Install + quickstart (link to `howto_getting_started.md`).
  - Feature overview: BB ontology, DKS, retrieval, capture, MCP.
  - "What's in v0.1.0" section: pointers to skill catalog, how-to library, seed vault.
  - Links: PyPI, GitHub releases, vault on the web (if any), CHANGELOG.

### VI.2 — Version bump + sequencing

- Bump to `0.1.0` (D-8: no `0.1.0b1` rc cycle).
- CHANGELOG: move every line under `## [Unreleased] - Planned for v0.1.0` into the `0.1.0` section. Add "This version cuts public-beta — alpha cycle is complete."

### VI.3 — GitHub release

- `gh release create v0.1.0 --generate-notes` + manual polish on the notes.
- Attach the wheel + sdist as release assets.

### VI.4 — Tests + release-time validation

- Full pytest suite green.
- Clean-venv wheel smoke: `pip install tessellum==0.1.0 && tessellum init /tmp/myvault && cd /tmp/myvault && tessellum capture argument first_arg && tessellum format check`.
- README's quickstart literally executed by a fresh user (or by a fresh clean venv).

### Exit criteria

- `pip install tessellum` (no version pin) installs `0.1.0`.
- GitHub release page visible; CHANGELOG accurate.
- This plan reaches its terminal phase.

## Integration points across all phases

| Subsystem | I (v0.0.55) | II (v0.0.56) | III (v0.0.57) | IV (v0.0.58) | V (v0.0.59) | VI (v0.1.0) |
|-----------|------------|-------------|--------------|-------------|------------|------------|
| `tessellum.dks.core` | I.1 multi-revision | — | — | — | — | — |
| `tessellum.dks.meta.runtime` | I.3 stratified observation | — | — | — | — | — |
| `tessellum.bb.types` | I.2 `BB_SCHEMA_AT_VERSION` helper | — | — | — | — | — |
| `tessellum.format.validator` | I.2 version-aware TESS-005 | — | — | — | — | — |
| `tessellum.format.frontmatter_spec` | I.3 `argument_perspective` field | — | — | — | — | — |
| `tessellum.capture` | I.3 capture writes `argument_perspective` | — | — | — | — | — |
| `tessellum.cli` | I.1 cycle trace serialiser update | — | — | — | V.1 `tessellum mcp serve` subcommand | — |
| `tessellum.data._seed_manifest` | — | — | III.3 all new notes | IV.3 all new skills | V.3 how-tos + MCP entry | — |
| `tessellum.mcp` | — | — | — | — | V.1 MCP server | — |
| `vault/resources/term_dictionary/` | — | — | III.2 primer terms | — | — | — |
| `vault/resources/<bb-dirs>/` | — | — | III.1 8 example notes | — | — | — |
| `vault/resources/skills/` | — | — | — | IV.1 9 new canonicals + sidecars | — | — |
| `vault/resources/how_to/` | — | — | — | — | V.2 4 guides | — |
| `vault/0_entry_points/` | — | — | — | IV.3 catalog refresh | V.3 MCP tools entry | — |
| `.github/workflows/` | — | II.1 CI workflow | — | — | — | — |
| `pyproject.toml` | — | II.2 force-include + `[dev]` extras | — | — | — | VI.2 version 0.1.0 |
| `README.md` | — | — | — | — | — | VI.1 polish |
| `CHANGELOG.md` | every phase | every phase | every phase | every phase | every phase | VI.2 consolidate |

## Open questions

| # | Question | Lean |
|---|----------|------|
| **OQ-A** | Should the 20-skill target shrink if some "essential" skills are obviously redundant after authoring? | Yes — shrinking to 17-19 is fine if 5×4 symmetry forces duplicates. Symmetry serves coverage, not ritual. |
| **OQ-B** | Should the MCP server bundle authentication / authorization, or assume the operator handles it? | Operator-handles for v0.1.0. Auth is out-of-scope for an alpha → public-beta transition. Note this in the MCP entry-point doc. |
| **OQ-C** | Should `bb_schema_version` auto-bump when a corpus note's links pass under a newer version? | No — bumping requires explicit operator intent. The `bb migrate --apply` path remains the only way to advance. Documented in I.2. |
| **OQ-D** | What's the right number of CI matrix Python versions? | 3.11 + 3.12 for now. 3.13 once it's GA and the SDK deps support it. Drop 3.11 when its support window closes. |
| **OQ-E** | Should v0.1.0 ship with the LLMProposer/LLMAttacker prompts hidden behind feature flags? | No — v0.0.53 already shipped them opt-in via `--proposer llm`. v0.1.0 just preserves that. Documenting the LLM-mode tradeoffs is a how-to job. |
| **OQ-F** | Should the multi-revision authoring in I.1 also revise the *meta-cycle* attacker (when meta-DKS finds multiple surviving proposals)? | No — that's a separate concern (meta-DKS already aggregates via `survive_threshold`). Surface-closure scope only. |

## What this plan does NOT do

- **No new DKS phases.** `plan_dks_expansion.md` is complete; no Phase 11. Future learning-level work (learned proposer, multi-perspective RL) lives in a separate v0.2+ plan.
- **No retroactive corpus rewrites.** `bb migrate --apply` exists; `--rewrite-links` stays deferred per `plan_meta_dks_validation_and_polish.md`.
- **No Web UI.** Tessellum is a CLI + MCP + Python library; a web frontend is v0.2+ scope at earliest.
- **No multi-vault federation.** Each `tessellum init` creates one vault; cross-vault tooling is research, not engineering.
- **No graph-database backend.** SQLite + FTS5 + sqlite-vec stays the default; alternative backends are v0.3+ research.
- **No model-tuning / fine-tuning.** The LLM-driven proposer and attacker use whatever Anthropic Sonnet / Opus the user runs against. Fine-tuned variants are v0.3+ research.

## Sequencing summary

```
v0.0.54 ┌─ SHIPPED (Phase 10 — multi-perspective DKS + Dung labelling)
        │
v0.0.55 │   Phase I — Close deferred alpha surface
        │   ├─ I.1 multi-revision authoring (tuple of revisions)
        │   ├─ I.2 version-aware TESS-005 (BB_SCHEMA_AT_VERSION)
        │   └─ I.3 argument_perspective YAML field
        │
v0.0.56 │   Phase II — CI workflow + ship-the-wheel discipline
        │   ├─ II.1 GitHub Actions ci.yml
        │   └─ II.2 Hatch force-include verification
        │
v0.0.57 │   Phase III — Seed vault content
        │   ├─ III.1 8 BB-type example notes
        │   ├─ III.2 primer term notes (gap-check + author)
        │   └─ III.3 seed manifest updates
        │
v0.0.58 │   Phase IV — Skill canonical library (20 skills)
        │   ├─ IV.1 9 new canonicals (5 capture + 2 search/answer + 3 trail mgmt + 3 maintenance)
        │   ├─ IV.2 use `tessellum capture skill` for scaffolding
        │   └─ IV.3 structural validation per canonical
        │
v0.0.59 │   Phase V — MCP server + how-to library
        │   ├─ V.1 tessellum.mcp.server + `tessellum mcp serve` subcommand
        │   ├─ V.2 4 how-to guides
        │   └─ V.3 seed manifest + entry-point updates
        │
v0.1.0  └─ Phase VI — Public beta cut
            ├─ VI.1 README polish
            ├─ VI.2 version bump + CHANGELOG consolidation
            ├─ VI.3 GitHub release
            └─ VI.4 release-time clean-venv quickstart validation
```

## Related plans

- `plan_dks_expansion.md` — DKS feature plan, Phases 1-10 (all shipped through v0.0.54)
- `plan_meta_dks_validation_and_polish.md` — meta-DKS validation + Phase B polish (shipped at v0.0.53)
- `plan_minimal_seed_vault.md` — earlier seed-vault plan; this plan supersedes its v0.1.0 sections

---

**Last Updated**: 2026-05-11
**Status**: Active — drafted after v0.0.54 ship. Six versions (v0.0.55 → v0.1.0) to public-beta release; surface closures first, content + infrastructure middle, MCP + how-tos last.
