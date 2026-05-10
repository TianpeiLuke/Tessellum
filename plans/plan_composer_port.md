---
tags:
  - project
  - plan
  - tessellum
  - composer
  - dks
  - pipeline
keywords:
  - composer port
  - skill canonical sidecar
  - pipeline yaml
  - typed contract pipeline
  - five wave port
  - dks runtime
topics:
  - Composer
  - DKS Runtime
  - Pipeline Architecture
  - v0.1 Roadmap
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Composer Port to Tessellum (5-Wave)

## Problem

Composer is the largest single subsystem in the v0.1 plan and the **bridge between System P (capture) and System D (retrieval)** in Tessellum's CQRS framing. The parent project (AbuseSlipBox) has a mature Composer at `src/buyer_abuse_slipbox_agent/composer/` developed across the FZ 10d1e1a8a1a* trail, with ~3500 LOC of typed-contract orchestration plus eval framework and batch runner.

Tessellum currently has **none** of it. The CLI banner lists `tessellum compose <chain>` under "Roadmap" with no implementation behind it; `runs/composer/` is an empty gitignored directory waiting for a runtime to write to it.

This plan codifies what to port and in what order. Total scope: ~3500 LOC across 10 modules + JSON schema + tests + 1 new CLI subcommand family. Realistic timeline: **4 sprints (1 per wave) for v0.1**, with eval + batch runner deferred to v0.2+.

## Why this matters — Composer is the load-bearing capability

Three reasons Composer is the highest-leverage subsystem to port:

1. **It's the only way Tessellum scales beyond hand-authoring.** Without Composer, every typed atomic note must be hand-written. With Composer, a skill canonical + sidecar drives auto-digestion of papers, drafts, and code into typed notes. The vault grows by orchestrated LLM dispatch rather than by manual editing.
2. **It's the integration point with agents.** The user's recurring framing ("agents at the leaves, plan as backbone") describes Composer's runtime: the compiler builds the plan backbone; the executor calls agents (LLMs) at each leaf with a section-extracted prompt + typed expected_output_schema.
3. **Compile-time contracts are a competitive moat.** Most knowledge-construction systems either skip typed contracts (free-form prompts, drift-prone outputs) or bolt on weak validation. Composer refuses malformed pipelines *before any LLM fires*. Port that property and Tessellum inherits it.

## What Composer is — recap from FZ trail

> A planner-centric orchestrator. Compiles skill canonicals + pipeline.yaml sidecars into a typed DAG of LLM calls. Fans out column-oriented batched dispatch (~4× cost reduction per FZ 10d1e1a8a1a5). Validates 6 contract types at compile time. Routes all outputs through a single materializer layer for filesystem consistency.

Key properties:

- **Planner-centric**, not text-splitter-centric. The DAG is the artifact.
- **Two files per skill**: canonical markdown body (procedure) + `.pipeline.yaml` sidecar (typed contract). Linked by `<!-- :: section_id = X :: -->` anchor comments.
- **Compile-time validation**: Pydantic V2 contracts + JSON Schema + DAG acyclicity + enum violations all checked before any LLM dispatch. CompilerError raised on drift.
- **Single side-effect layer**: 5 concrete materializers (`body_markdown_frontmatter_to_file`, `edits_apply_xml_tags`, etc.). Every step's filesystem effect goes through one of them.
- **Eval framework** (v0.7+): LLMJudge 5-dim rubric + scenario assertions. Defer for Tessellum v0.1.

## The skill canonical ↔ pipeline.yaml pairing — load-bearing pattern

The two-file pairing is **the** core architectural decision. Don't merge them; don't auto-derive one from the other.

**Skill canonical** (`vault/resources/skills/skill_<name>.md`) — markdown body with H2 section anchors:

```markdown
## Step 2: Extract Three Facets <!-- :: section_id = step_2_extract_three_facets :: -->

[procedure prose for the agent — what it should do, input shape, expected output...]
```

**Pipeline sidecar** (`vault/resources/skills/skill_<name>.pipeline.yaml`) — typed contract:

```yaml
pipeline:
  - section_id: step_2_extract_three_facets
    role: CORE                          # CORE | DEFERRED | INFRA
    aggregation: per_leaf               # per_leaf | cross_leaf | corpus_wide
    batchable: true
    depends_on: [step_1_load_input]
    materializer: body_markdown_frontmatter_to_file
    output_key: facets
    expected_output_schema:
      type: object
      required: [facet_a, facet_b, facet_c]
      properties:
        facet_a: { type: string }
    prompt_template: |
      [Jinja-style; {{leaf.X}} resolved at compile-time, {{upstream.Y}} at runtime]
    mcp_dependencies:
      - name: builder-mcp
        calls: [InternalSearch]
        required: false
```

**At runtime**, `load_skill_section(skill="<name>", section_id="step_2_extract_three_facets")` reads the canonical, finds the anchor, and returns the section's text — that becomes the LLM's prompt. The sidecar declares the typed contract: schema, dependencies, materializer, batching policy.

**Why two files, not one**: the canonical is human-authored and human-read; it lives in the vault and gets indexed/searched like any other note. The sidecar is machine-validated; lifting the contract out keeps the canonical clean (per FZ 10d1e1a8a1a6: "lift 5,000 lines out of 85 markdown files").

**Reality check on conversion**: there is **no converter script** in AbuseSlipBox today. Authors hand-write both files. Migration scripts existed only as one-shots (e.g., `migrate_skill_to_in_vault_body.py` lifted metadata blocks *out* of canonicals *into* sidecars in v0.5.3). For Tessellum we have a choice between matching that convention (manual) or adding a scaffold step (`tessellum capture skill <name>` could emit a starter sidecar alongside the canonical) — see Open Questions.

## Design principles

1. **Two-file pairing is load-bearing.** Don't merge. Don't auto-derive. The canonical and sidecar serve different audiences (humans vs the compiler).
2. **Compile-time validation is mandatory.** Every contract — JSON schema, Pydantic models, DAG acyclicity, enum membership — runs before LLM dispatch. CompilerError stops the pipeline.
3. **Schema is the contract.** Port `pipeline.schema.json` verbatim from the parent. Don't redesign — divergence costs interop.
4. **Composer's load/validate path has no LLM dependency.** Wave 1 ships pure data + validators. Tessellum users can validate sidecars without an API key.
5. **Materializers are the only filesystem side-effect layer.** Every output goes through a declared materializer. Direct file writes from inside agent step code are forbidden.
6. **Run traces live in `runs/composer/`** — already decided in `plan_cqrs_repo_layout.md`. Each chain run gets one timestamped trace file.

## Proposed approach — 5-wave port

| Wave | Scope | LOC est. | Milestone |
|---|---|---|---|
| **Wave 1** | Foundation — pure data + validators | ~750 | `tessellum composer validate <skill>` works |
| **Wave 2** | Compiler — DAG build, zero LLM calls | ~600 | `tessellum composer compile <plan_doc>` outputs validated `pipeline_dag.json` |
| **Wave 3** | Executor — runtime + materializers | ~1200 | `tessellum composer run <plan_doc>` executes a single-corpus pipeline end-to-end with mock LLM |
| **Wave 4** | LLM bridge — Anthropic SDK + MCP dispatcher (optional) | ~300 + MCP | `tessellum composer run` with real LLM calls; vault writes succeed |
| **Wave 5+** | Scale + quality (optional, defer) | ~700 | Multi-corpus batch + eval framework |

### Wave 1 — Foundation (this plan's main scope)

Nine concrete deliverables (the user's hint about skill canonical → sidecar conversion is load-bearing — items 8 and 9 deliver that):

1. **`src/tessellum/composer/schemas/pipeline.schema.json`** — port verbatim from `src/buyer_abuse_slipbox_agent/composer/schemas/pipeline.schema.json`. The schema declares the sidecar's structure: required keys, role enum (CORE/DEFERRED/INFRA), aggregation enum (per_leaf/cross_leaf/corpus_wide), materializer enum, MCP contract shape.
2. **`src/tessellum/composer/contracts.py`** — Pydantic V2 models matching the parent's 6 contracts: `MaterializerContract`, `LLMBackendContract`, `MCPContract`, `DynamicResolverContract`, `RouterSubcategoryContract`, `OutputPathContract`. ~300 LOC.
3. **`src/tessellum/composer/skill_extractor.py`** — `load_skill_section(skill_name, section_id)` reads the canonical markdown, finds the `<!-- :: section_id = X :: -->` anchor, returns the section text. Plus `load_pipeline_metadata(skill_name)` reads the sidecar, validates against schema, returns parsed dict. ~200 LOC.
4. **`src/tessellum/composer/loader.py`** — pipeline-loader entry point: takes a skill name, resolves the canonical's `pipeline_metadata:` frontmatter field, loads + validates the sidecar, raises `PipelineValidationError` on drift. ~150 LOC.
5. **`src/tessellum/cli/composer.py`** + wire into dispatcher — `tessellum composer validate <skill>` subcommand. Loads + validates the skill's canonical + sidecar. Exit 0 if clean; exit 1 if validation fails; exit 2 on invocation errors. Mirrors the `tessellum format check` pattern.
6. **Verify `vault/resources/templates/template_skill.md` already has `<!-- :: section_id = X :: -->` markers** on every H2 heading. As of 2026-05-10, all 10 H2s in the template carry the markers — no body changes needed; the verification is structural-only. (If a future maintainer accidentally drops them, this step catches the regression.)
7. **`vault/resources/templates/template_skill.pipeline.yaml`** — starter sidecar with placeholder steps + schema-compliant skeleton. Each step matches one of the canonical's `section_id` anchors. Comments explain each key (`role`, `aggregation`, `batchable`, `materializer`, `expected_output_schema`, `prompt_template`).
8. **Extend `tessellum.capture` for `skill` flavor** — when `tessellum capture skill <slug>` runs, emit BOTH `skill_<slug>.md` AND `skill_<slug>.pipeline.yaml` in one call. The canonical's `pipeline_metadata:` frontmatter field is set to `./skill_<slug>.pipeline.yaml`. This **operationalizes the user's hint** about converting skill canonical into sidebar YAML — the conversion happens at capture time, not as a one-off script. Authors who don't need Composer dispatch can delete the sidecar and set `pipeline_metadata: none`.
9. **Update `pyproject.toml`**:
   - Schemas live at `src/tessellum/composer/schemas/pipeline.schema.json` — *no* `force-include` needed; content inside `src/tessellum/` ships in the wheel automatically.
   - Add `force-include` entry for `vault/resources/templates/template_skill.pipeline.yaml` → `src/tessellum/data/templates/template_skill.pipeline.yaml` (mirrors the existing templates graft) so `tessellum.data.templates_dir()` resolves the new starter sidecar in both editable and wheel-install modes.

### Wave 2 — Compiler (zero LLM)

- `src/tessellum/composer/compiler.py` — walks plan_doc + skill metadata, renders step instances, builds the DAG, validates acyclicity + enum violations, pre-fetches existing files for APPLY steps. Raises `CompilerError` at compile time. ~600 LOC.
- DAG output format: `pipeline_dag.json` (versioned schema).
- CLI: `tessellum composer compile <plan_doc>` outputs the DAG without running it.

### Wave 3 — Executor

- `src/tessellum/composer/executor.py` — runs a single step instance: resolve `{{leaf.X}}` / `{{upstream.Y}}` / `{{existing.Z}}` placeholders, invoke LLM (initially mock), check response against `expected_output_schema`, materialize via declared materializer. ~400 LOC.
- `src/tessellum/composer/scheduler.py` — topological sort + column-oriented batching. ~400 LOC.
- `src/tessellum/composer/materializer.py` — 5 concrete materializers. ~400 LOC.
- CLI: `tessellum composer run <plan_doc>` executes end-to-end. Run trace lands in `runs/composer/<YYYY-MM-DDThh-mm-ss>_<chain>.json`.

### Wave 4 — LLM bridge

- `src/tessellum/composer/llm.py` — Anthropic SDK wrapper (initial), pluggable for OpenAI/local. Behind `[agent]` extras dependency. ~150 LOC.
- `src/tessellum/composer/mcp_dispatcher.py` (optional) — match v0.5.4+ MCP contracts. Behind `[mcp]` extras. ~150 LOC. **DEFER unless real demand.**

### Wave 5+ — Scale + quality (defer to v0.2+)

- Batch runner (multi-corpus, parallelism, resume): ~200 LOC.
- Eval framework (LLMJudge 5-dim, scenario assertions): ~500 LOC.
- These are nice-to-have, not required for v0.1 launch.

## Wave 1 — Migration steps

Execute as 1-2 commits (Wave 1 is large; could split schema+contracts in one commit, extractor+loader+CLI+capture in another):

1. **Port `pipeline.schema.json`** from parent project. Adjust any AbuseSlipBox-specific enum values (e.g., remove ML-domain materializers if they reference parent-only filesystem layouts).
2. **Author `tessellum.composer.contracts`** — Pydantic V2 models. Match parent's contract types but rename any AbuseSlipBox-specific class names. Tests: model construction + serialization round-trip.
3. **Author `tessellum.composer.skill_extractor`** — section anchor regex matches `<!-- :: section_id = ([a-z0-9_]+) :: -->`. Tests: extract sections from `skill_tessellum_format_check.md` (already has these markers).
4. **Author `tessellum.composer.loader`** — uses PyYAML + jsonschema + Pydantic. Tests: valid sidecar loads; invalid sidecar raises with clear error message; `pipeline_metadata: none` is accepted as a sentinel for "skill has no Composer dispatch".
5. **Author `tessellum.cli.composer`** — `tessellum composer validate <skill>`. Wire into `cli/main.py` dispatcher. Tests: validate with mock skill files in `tmp_path`.
6. **Verify `template_skill.md` carries section_id markers on all H2s** (already true as of 2026-05-10 — 10/10 H2s have them; this is a regression-catch step, no body edits).
7. **Author starter sidecar template** `vault/resources/templates/template_skill.pipeline.yaml` — minimal schema-compliant skeleton with one CORE step + comments explaining each key. Section IDs in the starter must match the canonical's H2 anchors.
8. **Extend `tessellum.capture` for `skill` flavor** — when flavor is `skill`, emit BOTH `skill_<slug>.md` AND `skill_<slug>.pipeline.yaml` from the paired templates. Set the canonical's frontmatter `pipeline_metadata` field to `./skill_<slug>.pipeline.yaml`. Tests: capture creates both files; both validate; the canonical references the sidecar via frontmatter; running `tessellum composer validate <slug>` on the result passes (or fails with a clear "fill in the placeholders" error).
9. **Update `pyproject.toml`** — add `force-include` entry for `vault/resources/templates/template_skill.pipeline.yaml` → `src/tessellum/data/templates/template_skill.pipeline.yaml`. Schemas at `src/tessellum/composer/schemas/` ship automatically (no force-include needed). Verify wheel build by `python -m build && unzip -l dist/*.whl | grep -E '(schema|pipeline.yaml)'`.
10. **Bump to v0.0.9** (or v0.0.10 if split into two commits). CHANGELOG entry covers the schema port, contracts, extractor, loader, CLI, capture extension, and the starter sidecar template.
11. **Add Wave 1 milestone test**: `tessellum composer validate skill_tessellum_format_check` either passes (after authoring its sidecar) or accepts the `pipeline_metadata: none` sentinel without error. Pick one — see Open Questions.

## Open questions

- **Skill canonical → sidecar conversion**: hand-author both (parent's pattern) or auto-scaffold via `tessellum capture skill`? **Lean: auto-scaffold.** It's a small extension to capture and addresses the user's specific hint; authors can delete the sidecar if their skill doesn't need Composer dispatch.
- **MCP dispatcher in Wave 4**: ship or defer? **Lean: defer.** Tessellum v0.1 doesn't need to match parent's full MCP architecture. Add later when a Tessellum user has a concrete MCP integration need.
- **Eval framework**: ship in v0.1 or defer to v0.2+? **Lean: defer.** Eval is high-LOC and benefits later users more than first-release users. Get Composer working end-to-end first.
- **Anthropic-only LLM bridge in Wave 4, or pluggable from day one?** **Lean: Anthropic-only initially.** Add OpenAI/local as separate `[agent_openai]`, `[agent_local]` extras when users ask.
- **Pipeline schema version field**: include from day one (so future schema migrations are clean) or defer until v0.2 schema bump? **Lean: include.** `pipeline_version: "0.1"` is a one-liner and worth $0 to add; expensive to retrofit later.
- **Where do skills with no Composer pipeline live in the registry?** A skill like `skill_tessellum_format_check` has no LLM dispatch (it's a CLI wrapper). Its `pipeline_metadata: none` indicates "no sidecar". The validator should accept this. Tests must cover this case.

## See Also

- [`plan_v01_src_tessellum_layout.md`](plan_v01_src_tessellum_layout.md) — the v0.1 src/ shipping plan; Composer is its biggest open scope (steps 5-7 of that plan map to Waves 1-4 here)
- [`plan_cqrs_repo_layout.md`](plan_cqrs_repo_layout.md) — repo layout that decided where `runs/composer/` lives (gitignored, top-level)
- [`term_cqrs.md`](../vault/resources/term_dictionary/term_cqrs.md) — the principle Composer-as-bridge implements
- [`skill_tessellum_format_check.md`](../vault/resources/skills/skill_tessellum_format_check.md) — first Tessellum skill canonical; Wave 1 milestone is making this validate-ready
- AbuseSlipBox source: `src/buyer_abuse_slipbox_agent/composer/` (especially `compiler.py`, `contracts.py`, `skill_section_extractor.py`)
- AbuseSlipBox FZ trail: 10d1e1a8a1a* (rooted in `thought_composer_*`)

---

**Last Updated**: 2026-05-10
**Status**: Active — Wave 1 awaiting approval, then ships across 1-2 commits as v0.0.9 / v0.0.10.
