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

## Curated slices (one representative sub-plan per source)

| Slice | Sub-plan | Input pages | Golden notes | Exercises |
|-------|----------|------------:|-------------:|-----------|
| `claude_code_mcp` | B08A (MCP) | 3 | 8 | aggressive split of a 6,822-word / 41-code-block page; concept↔procedure BB routing; ≥6 term-link floor |
| `hermes_getting_started` | SP01 (Getting Started) | 8 | 9 | BB routing to navigation + model (not just procedure); the FOUR-FLOOR cross-ref (≥8 term / ≥5 repo / ≥10 snippet / ≥10 doc) |
| `openclaw_concepts` | co01 (agent runtime core) | 7 | 8 | 9-gate variant; dual cross-ref blocks (`## Related Notes` internal + `## References` external); one-page→two-note split |

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
  <slice>/
    input_pages/       ← raw source doc(s) — the pipeline's input
    golden_plan/       ← the plan the four skills produced
    golden_notes/      ← the notes the pipeline wrote
    golden_facts.json  ← measured, scrubbed golden reference
```
