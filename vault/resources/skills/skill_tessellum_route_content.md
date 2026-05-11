---
tags:
  - resource
  - skill
  - procedure
  - organize
  - routing
  - capture_dispatch
keywords:
  - route content
  - tessellum-route-content
  - sub-category novelty
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
bb_schema_version: 1
pipeline_metadata: ./skill_tessellum_route_content.pipeline.yaml
---

# Procedure: tessellum-route-content (Canonical Body)

This is the **single canonical body** for the `tessellum-route-content` skill — the agent-invocable surface for *routing classified content to vault sub-categories + paths*. Takes a classification report (from [`tessellum-classify-content`](skill_tessellum_classify_content.md)) and decides:

1. **Sub-category novelty** — does this leaf fit an existing sub-category under `(BB, PARA)`, or does it warrant a new one? (3-criterion framework)
2. **Sub-category label** — existing label OR new label justified by the criteria
3. **Target path** — directory + filename, derived from `tessellum.capture.REGISTRY` for known flavors or from the new sub-category label

The skill is **vault-specific** by design — it encodes Tessellum's directory structure, naming conventions, and the capture-registry default mapping.

## Skill description <!-- :: section_id = skill_description :: -->

Route classified content segments to vault sub-categories + paths. Reads a per-segment classification report and emits a per-segment routing decision. Pure planning — does not write notes; the caller (e.g. a multi-segment capture run) executes the plan.

Use when:

- A long mixed note has been classified by [`tessellum-classify-content`](skill_tessellum_classify_content.md) and segments need to be filed to the correct directories.
- An agent is about to invoke `tessellum capture <flavor> <slug>` and needs to choose `--destination` + `--prefix` overrides.
- Onboarding new content with a domain Tessellum hasn't seen before, and the agent needs to decide whether to use an existing sub-category or propose a new one.

## Scope Boundary <!-- :: section_id = scope_boundary :: -->

| Decision | Owner | Where it lives |
|---|---|---|
| Building block per segment (BB, 8 types) | `tessellum-classify-content` | sibling skill |
| Sub-category: existing or new? (3-criterion framework) | `tessellum-route-content` (this skill) | this skill |
| Sub-category label (existing OR new label) | `tessellum-route-content` (this skill) | this skill |
| `target_path` (directory + filename) | `tessellum-route-content` (this skill) | this skill, derived from `tessellum.capture.REGISTRY` + the sub-category decision |
| Capture-skill choice (when delegating body authoring) | the agent invoking this skill | downstream |
| Body content | the chosen capture skill | the capture-flavor canonical |

Rule of thumb: this skill answers *"WHERE in the corpus does this leaf go, and is its sub-category one we already have or do we need a new one?"*. It does NOT answer *"what kind of knowledge atom is this?"* (the classifier's job) or *"which skill writes the body?"* (a downstream selector).

## Sub-Category Novelty Framework (3-criterion) <!-- :: section_id = sub_category_novelty_framework :: -->

When deciding whether a segment's sub-category should be **existing** or **new**, the agent applies three criteria. Each yields an `existing | novel | n/a` signal.

### (a) Source — where does the original content come from?

Query the corpus index for prior notes from the same source family (similar `source_url` prefix, `source_type`, or directory under the same BB):

```bash
tessellum search "<source_prefix or marker>" --building-block <BB> --limit 10
```

| Finding | Signal |
|---|---|
| ≥3 notes share the prefix → familiar source family | `existing` |
| <3 notes share the prefix → first-time-or-rare source family | `novel` |
| Source unknown / no index hit | `n/a` |

### (b) Operational tasks — what role / workflow consumes this?

Read the segment's source content + heading. Ask: which user role would consult this note in which workflow? Compare to existing sub-categories under the same `(BB, PARA)`:

| Finding | Signal |
|---|---|
| Same audience + same workflow as existing → fits existing | `existing` |
| Different audience (e.g. agent-facing vs human-facing) OR different workflow (debugging vs onboarding) | `novel` |
| Cannot infer audience/workflow from content | `n/a` |

Examples:

- A `concept` segment that defines a Tessellum-vault primitive → fits `term_dictionary` (existing).
- A `concept` segment that's a third-party-tool API definition referenced in code reviews → potentially `api_reference` (novel).

### (c) Maintenance schedule — does this require a different update mechanism?

Ask: if this note exists in 6 months, who updates it, when, and on what trigger?

| Finding | Signal |
|---|---|
| Cadence + trigger match an existing sub-category's contract | `existing` |
| Cadence or trigger differ from all existing sub-categories under `(BB, PARA)` | `novel` |
| No clear maintenance contract implied by content | `n/a` |

Examples:

- Append-only term entries → `term_dictionary/` (existing).
- Quarterly-rotated paper digests → `digest/` (existing).
- A `procedure` that needs monthly version refresh → could be a new sub-category (`runbook_monthly/`) if no existing one matches.

### Decision rule

| `novel` count across (a, b, c) | Sub-category decision |
|---|---|
| 0 of 3 | **Existing** — pick best-match existing sub-category |
| 1 of 3 | **Existing** — pick best-match, AND emit `routing_warning` with the single novel signal for drift-candidate audit |
| 2 of 3 | **New** — propose new sub-category label; record full `subcategory_rationale` |
| 3 of 3 | **New** — propose new sub-category label; high-confidence novelty |

`routing_warning` rows feed a periodic audit: the system collects evidence; the human decides whether to crystallize a new sub-category from the drift candidates.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.58 or later
tessellum index build       # so the source-signal lookup can query the corpus
```

## Resources <!-- :: section_id = resources :: -->

- **Capture registry** (the routing source of truth): `tessellum.capture.REGISTRY` — Python module exposing the default `(flavor, BB, destination, filename_prefix)` mapping. Inspect via `python -c "from tessellum.capture import REGISTRY; ..."`.
- **BB index**: [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — the 8-BB picker matrix + the canonical exemplars + the "default directory" column (defaults, not constraints — per v0.0.57).
- **Sibling skill**: [`tessellum-classify-content`](skill_tessellum_classify_content.md) — produces the classification report this skill consumes.

## Step 1: Read Classification Report <!-- :: section_id = step_1_read_classification_report :: -->

Read the classification report from [`tessellum-classify-content`](skill_tessellum_classify_content.md) (in current context). Each row carries: `segment_id`, `lines`, `heading`, `building_block`, `content_domain`, `confidence`.

If no classification report is available, run [`tessellum-classify-content`](skill_tessellum_classify_content.md) first.

## Step 2: Map (Building Block, Content Domain) → Routing Candidate <!-- :: section_id = step_2_map_to_routing_candidate :: -->

For each segment, derive a **starting-point routing candidate** from `tessellum.capture.REGISTRY` + the BB index's "default directory" column:

```python
from tessellum.capture import REGISTRY
spec = REGISTRY[<flavor>]  # flavor = "concept" / "model" / "procedure" / ...
default_destination = spec.destination     # e.g. "resources/term_dictionary"
default_prefix = spec.filename_prefix      # e.g. "term_"
```

The flavor maps from `building_block` per the BB index's canonical convention:

| Building Block | Default flavor | Default destination | Default prefix |
|---|---|---|---|
| `concept` | `concept` | `resources/term_dictionary` | `term_` |
| `model` | `model` | `areas` | `model_` |
| `procedure` | `procedure` or `skill` or `code_snippet` (agent picks) | `resources/how_to` / `resources/skills` / `resources/code_snippets` | `howto_` / `skill_` / `snippet_` |
| `empirical_observation` | `empirical_observation` or `experiment` | `resources/analysis_thoughts` or `archives/experiments` | `observation_` / `experiment_` |
| `hypothesis` | `hypothesis` | `resources/analysis_thoughts` | `hypothesis_` |
| `argument` | `argument` | `resources/analysis_thoughts` | `thought_` |
| `counter_argument` | `counter_argument` | `resources/analysis_thoughts` | `counter_` |
| `navigation` | `entry_point` / `acronym_glossary` / `navigation` | `0_entry_points` | `entry_` |

**These defaults are the starting point.** The agent overrides them via `--destination <subdir> --prefix <name_>` (per v0.0.57) when the content_domain suggests a sub-category. Example:

- `(model, "code repo")` → override to `areas/code_repos/` + `repo_` prefix
- `(model, "team")` → override to `areas/teams/` + `team_` prefix
- `(model, "tool / algorithm")` → override to `areas/tools/` + `tool_` prefix
- `(procedure, "skill canonical")` → use `skill` flavor (already a separate flavor) → `resources/skills/` + `skill_`
- `(procedure, "code snippet")` → use `code_snippet` flavor → `resources/code_snippets/` + `snippet_`

## Step 3: Apply the 3-criterion Novelty Framework <!-- :: section_id = step_3_apply_novelty_framework :: -->

For each segment, gather the three signals (source / operational_task / maintenance) per the section above. Determine the `subcategory_novelty` outcome from the decision rule.

For `novel` outcomes (2-of-3 or 3-of-3), the agent proposes a new sub-category label. The label should:

- Be lowercase snake_case (matches directory naming convention).
- Be specific enough to scope to one (BB, PARA) — not as broad as "misc".
- Encode the maintenance contract if non-obvious (`api_reference` vs generic `reference`).

For `existing` outcomes, pick the closest-match existing sub-category from the BB index.

## Step 4: Apply Corpus Coherence Bias <!-- :: section_id = step_4_corpus_coherence_bias :: -->

When multiple segments in the same routing run already chose a sub-category, **prefer the majority** unless the new segment's source content strongly resists it. This prevents fragmenting a coherent multi-segment note across many one-off sub-categories.

Heuristic: if ≥60% of sibling segments in the current report routed to sub-category X under the same `(BB, PARA)`, and the current segment has `confidence: medium` or lower, route it to X too.

## Step 5: Compute target_path <!-- :: section_id = step_5_compute_target_path :: -->

Per segment, emit:

- `destination`: the directory (relative to vault root). Existing sub-category → from REGISTRY + the BB-index "default directory" column. New sub-category → derive a new directory from the proposed label (e.g., new sub-category `api_reference` under (concept, resource) → `resources/api_reference/`).
- `filename_prefix`: existing sub-category → from REGISTRY. New sub-category → derive from the label (often the label itself + `_`, e.g. `api_reference_`).
- `slug`: the filesystem-safe slug for the segment's heading or title.
- Full `target_path` = `<destination>/<filename_prefix><slug>.md`.

## Step 6: Output Routing Plan <!-- :: section_id = step_6_output_routing_plan :: -->

Emit a structured per-segment routing plan. The plan is the input the caller passes to `tessellum capture` (with `--destination` + `--prefix` overrides) or to a multi-segment decomposer.

```
| # | Segment | BB | Domain | Sub-category | Novelty | Target path |
|---|---------|----|--------|--------------|---------|-------------|
| 1 | "Warrant definition" | concept | term | term_dictionary | existing | resources/term_dictionary/term_warrant.md |
| 2 | "DKS architecture" | model | architecture | code_repos | existing | areas/code_repos/repo_<...>.md |
| 3 | "Run a cycle" | procedure | tutorial | how_to | existing | resources/how_to/howto_run_dks_cycle.md |
| 4 | "References" | navigation | — | — | skip | — |
```

If a segment has `subcategory_novelty = drift_candidate_one_of_three`, include the `routing_warning` text in a separate column or as a per-row annotation.

## Output JSON shape (machine-readable) <!-- :: section_id = output_json_shape :: -->

Each routed segment serialises as:

```json
{
  "segment_id": 1,
  "building_block": "concept",
  "second_category": "term_dictionary",
  "subcategory_novelty": "existing",
  "subcategory_rationale": {
    "source_signal": "existing",
    "operational_task_signal": "existing",
    "maintenance_signal": "n/a"
  },
  "destination": "resources/term_dictionary",
  "filename_prefix": "term_",
  "slug": "warrant",
  "target_path": "resources/term_dictionary/term_warrant.md",
  "rationale": "1-3 sentence summary citing source content + corpus state + sibling context",
  "routing_warning": null
}
```

Fields:

- `subcategory_novelty` ∈ `{existing, new_two_of_three, new_three_of_three, drift_candidate_one_of_three}`.
- `subcategory_rationale` records the per-criterion signal: `existing | novel | n/a` for each of source / operational_task / maintenance.
- `routing_warning` is non-null only when `subcategory_novelty == drift_candidate_one_of_three` — text describing which single criterion fired.

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| No classification report | Caller skipped step 1 | Run [`tessellum-classify-content`](skill_tessellum_classify_content.md) first |
| Unknown BB type | Classification produced label outside the 8 BB types | Reject; ask classifier to relabel |
| Source signal unavailable | `tessellum index build` not run | Emit `source_signal: n/a` and proceed with the other two criteria |
| All segments collapse to one sub-category | Corpus coherence bias too strong | Re-run with bias disabled to verify; user-confirm |
| New sub-category proposed but conflicts with existing directory | Naming collision | Append `_v2` or pick a more specific label |

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **No vault writes.** This skill produces a routing plan; it never creates notes. The caller (or downstream capture skill) executes the plan.
2. **Do NOT re-classify BB.** The classification arrives upstream from [`tessellum-classify-content`](skill_tessellum_classify_content.md). If a segment's BB looks wrong, surface a `routing_warning` — do not silently re-label.
3. **Capture REGISTRY is the source of truth for defaults.** The Step-2 table above is illustrative; query `tessellum.capture.REGISTRY` programmatically when authoring code that consumes this skill's output.
4. **New sub-categories require all three rationale fields populated.** A `novel` decision without recorded rationale is rejected — the framework's value depends on the trail of evidence.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — the 8-BB picker matrix + canonical exemplars + default directories; the table this skill's routing decisions resolve against.
- [`entry_skill_catalog`](../../0_entry_points/entry_skill_catalog.md) — full vault skill index; this skill sits in the "capture-side helpers" group alongside [`tessellum-classify-content`](skill_tessellum_classify_content.md).
