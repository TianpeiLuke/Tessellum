# Digestion-Pipeline Evaluation Set

A golden evaluation set for Tessellum's **digestion pipeline** —
`plan → augment → review → execute` (`tessellum.composer.digestion.run_digestion_pipeline`).

## What makes this a valid golden

The reference plans and notes here were produced by the **exact same four
digestion skills** that Tessellum's composer runs as its `PHASE_SKILLS`
(`skill_tessellum_plan_digestion`, `..._augment_digestion_plan`,
`..._review_digestion_plan`, `..._execute_digestion_plan`), executed at
production scale in a real knowledge vault. So this is a **same-pipeline
reproduction test**: give Tessellum the same raw documentation, and its
generated plan + notes should match the golden's *measurable structure* —
building-block atomicity, section coverage, cross-reference floors, density
caps, schema conformance, and gate outcomes.

It is **not** a byte-for-byte test. Digestion is generative; prose differs
run-to-run. The golden pins the **contracts and measurable properties**
(Tiers 1–2, deterministic) and layers an LLM-judge content-fidelity pass on top
(Tier 3). See `rubric.md`.

## The three triples

Each triple is `raw docs → golden plan(s) → golden notes + entry point`, joinable
on the source page slug. All three come from **public third-party documentation**
(Anthropic Claude Code, NousResearch Hermes Agent, OpenClaw), digested into the
private vault.

| Source | Raw docs | Golden plans | Golden notes | BB skew |
|--------|---------:|-------------:|-------------:|---------|
| Claude Code | 134 | 41 | 339 | procedure 176 / concept 142 / argument 18 / model 3 |
| Hermes Agent | 348 | 27 | 226 | procedure 158 / model 48 / navigation 11 / concept 8 / obs 1 |
| OpenClaw | 665 | 106 | 816 | procedure 531 / concept 138 / model 117 / argument 30 |

Full corpora totals: **1,147 raw docs → 174 plans → 1,381 notes.**

## What is vendored here

Each curated slice is **self-contained** — it vendors the full triple:

```
<slice>/
  input_pages/     ← the raw source doc(s) fed to the pipeline (public third-party docs)
  golden_plan/     ← the plan the four skills produced from those pages
  golden_notes/    ← the notes the pipeline wrote from that plan
  golden_facts.json ← measured, machine-readable gradeable reference
```

**Scrubbing.** `~/Tessellum` is a **public** repo, and the plans/notes were
produced in a private vault. The vendored copies are **surgically scrubbed** of
private identifiers: internal vault paths → `vault/…`, the private DB name →
`vault_unified.db`, the private skill-command names → their public `/tessellum-*`
equivalents (the same four skills), and a handful of org-specific cross-reference
lines → generic public equivalents. The scrub touched **only** the
cross-reference tail and validation-script paths; the note **bodies** (the actual
digested knowledge) and the plans' **structure** are the real golden output,
verbatim. Link counts were preserved, so `golden_facts.json` still matches.

The `## Related Notes` blocks still cite the full private vault's note graph (363
distinct `.md` targets that do not exist inside this folder). Those are **not
dangling bugs** — they document the real cross-reference graph the golden built,
and the resolvable-links gate (N7) is scored against a vault DB, not within this
folder (see `rubric.md § Known golden caveats`). `manifest.json` records the full
corpora (by path + git SHA `59bdae36c`) for anyone reproducing at full scale.

Per-slice gradeable facts live in `golden_facts.json` (BB distribution, word /
line / code-block ranges, cross-reference floors, frontmatter schema, per-note
section lists, planned-note counts).

## Curated slices (nine, with a dev/test split)

| Slice | Split | Sub-plan | Input pages | Golden notes | Exercises |
|-------|-------|----------|------------:|-------------:|-----------|
| `claude_code_mcp` | dev | B08A (MCP) | 3 | 8 | aggressive split of a 6,822-word / 41-code-block page; concept↔procedure BB routing; ≥6 term-link floor |
| `hermes_getting_started` | dev | SP01 (Getting Started) | 8 | 9 | BB routing to navigation + model (not just procedure); the FOUR-FLOOR cross-ref (≥8 term / ≥5 repo / ≥10 snippet / ≥10 doc) |
| `openclaw_concepts` | dev | co01 (agent runtime core) | 7 | 8 | 9-gate variant; dual cross-ref blocks (`## Related Notes` internal + `## References` external); one-page→two-note split |
| `claude_code_hooks` | dev | B07A (Hooks Reference) | 1 | 10 | single 21,959-word reference page split into 10 notes; concept/procedure routing on reference material |
| `claude_code_sdk_core` | **test** | B19A (Agent SDK Core & Lifecycle) | 5 | 11 | SEQUESTERED — registered mechanically; scored only at declared release points |
| `hermes_protocols_providers` | dev | SP09 (Protocols & Providers) | 7 | 9 | multi-page fan-in; procedure/model/concept routing; the four-floor cross-ref |
| `hermes_build_extend` | **test** | SP17 (Guides: Build & Extend) | 10 | 13 | SEQUESTERED — registered mechanically; scored only at declared release points |
| `openclaw_gateway` | dev | gw02 (Gateway) | 7 | 13 | 9-gate variant; plan-amendment fidelity (11 planned → 13 shipped via recorded density splits) |
| `openclaw_plugins` | **test** | pl02 (Plugins) | 7 | 11 | SEQUESTERED — registered mechanically; one recorded golden imperfection (see manifest) |

### The dev/test split

The three original slices plus one new slice per source are the DEV set: they may
be read, swept, and tuned against, and numbers computed on them are training
objectives. The three `test` slices are SEQUESTERED: they were vendored
mechanically (scripts copied, scrubbed, measured, and scored them; no developer
read the content), they must never be swept or tuned against, and they are scored
only at declared release points. A test slice is **consumed by its first measured
contact** — once its score is published it converts to dev, and a fresh test
slice should be cut from the vendored corpora (`tools/make_golden_facts.py`
regenerates any slice's facts; `--check` is the oracle). First-contact scores on
test slices are the program's only generalization estimates.

## How to run

1. **Generate** — point Tessellum's digestion pipeline at a slice's
   `input_pages/`, producing a plan and a directory of notes.
2. **Score (Tier 1–2, deterministic)**:
   ```bash
   python eval/digestion_pipeline/score.py \
       eval/digestion_pipeline/claude_code_mcp \
       --plan   <generated_plan.md> \
       --notes  <generated_notes_dir>
   ```
   Emits per-metric pass rates + a GREEN / NEEDS_WORK verdict (exit 0 / 1).
3. **Score (Tier 3, content fidelity)** — reuse `tessellum.composer.eval.LLMJudge`
   with a real backend, judging each generated note against the source page(s)
   its plan row cites. See `rubric.md § Tier 3`.

The scorer is validated for **self-consistency**: scoring the golden notes
against their own `golden_facts.json` yields GREEN with every metric at 1.0 and
BB-similarity 1.0 for all three slices.

## Files

```
digestion_pipeline/
  README.md            ← this file
  manifest.json        ← corpora index + slice catalog + scoring config
  rubric.md            ← the 3-tier gradeable rubric (plan / note / fidelity)
  score.py             ← deterministic Tier-1/2 scorer (stdlib only)
  tools/               ← generators (make_golden_facts.py, vendor_full_corpora.py) + judges
  <slice>/             ← the 3 curated single-sub-plan exemplars
    input_pages/       ← raw source doc(s) — the pipeline's input
    golden_plan/       ← the plan the four skills produced
    golden_notes/      ← the notes the pipeline wrote
    golden_facts.json  ← measured, scrubbed golden reference
  <corpus>/            ← the 3 FULL corpora (claude_code / hermes_agent / openclaw)
    input_docs/        ← the complete raw source tree (public mirror, verbatim)
    golden_plans/      ← every sub-plan the pipeline produced
    golden_notes/      ← every note (bodies verbatim; internal cross-refs stripped)
    golden_terms/      ← the term notes the campaign authored (public-subject only)
    golden_facts.json  ← corpus-level measured reference (self-consistent)
```

## Full corpora (added 2026-07-31)

Beyond the three curated slices, the **complete** digestion output of each source
is now vendored — enlarging the eval from ~25 notes to **1,381 golden notes +
174 plans + 1,154 raw docs + 89 authored term notes**. Totals:

| Corpus | input_docs | golden_plans | golden_notes | golden_terms |
|--------|-----------:|-------------:|-------------:|-------------:|
| `claude_code`  | 134 |  41 | 339 | 13 |
| `hermes_agent` | 355 |  27 | 226 | 31 |
| `openclaw`     | 665 | 106 | 816 | 45 |

**Score a full corpus** exactly like a slice:

```bash
python eval/digestion_pipeline/score.py \
    eval/digestion_pipeline/openclaw \
    --notes eval/digestion_pipeline/openclaw/golden_notes
```

**Scrub for this public repo (deterministic).** `tools/vendor_full_corpora.py`
copies from the private vault and scrubs by rule — validated against the three
hand-scrubbed curated slices as its correctness oracle:

- **input_docs** — verbatim (public third-party mirrors; 0 internal markers).
- **golden_notes** — note *bodies* are verbatim (verified: 0 internal product
  tokens in any body). In the cross-reference tail, a bullet is **kept only if**
  every `.md` link target sits in a public-allowlisted dir (`term_dictionary`,
  `code_snippets`, `code_repos`, `pi`, `band`, `aws_*`, the three doc dirs)
  **and** no internal token appears on the line; every other bullet is deleted.
  Deletion cannot leak, so the `## Related Notes` graph here is a public subset
  of the private one (dangling cross-vault links, as in the slices, are expected
  and are scored against a vault DB — see `rubric.md § Known golden caveats`).
- **golden_plans** — mechanical scrub (private skill-command names → their
  public `/tessellum-*` equivalents, private path/DB → `vault`) + internal
  cross-ref bullets deleted + vault-search-narration lines dropped + residual
  internal product/path/domain tokens redacted to generic public equivalents.
- **golden_terms** — only the term notes each campaign **authored** (attributed
  via its digestion commits), public-concept subject only; an internal
  `related_wiki` is nulled, internal prose passages are removed from otherwise-
  public term bodies, and a few terms whose subject is itself a non-public system
  are excluded entirely.

`golden_facts.json` for each corpus is regenerated by `tools/make_golden_facts.py`
from the **scrubbed** notes, so scoring the golden against its own facts is GREEN
with BB-similarity 1.0 by construction.
