# Digestion-Pipeline Evaluation Rubric

How to score a Tessellum digestion run (generated **plan** + generated **notes**)
against a golden slice. Every criterion below is derived from the actual
contracts the golden plans/notes were built and gated against — the same
`plan → augment → review → execute` skill contracts Tessellum's composer runs.

The rubric has three tiers. Tiers 1–2 are **deterministic** (no LLM); tier 3 is
the **LLM-judge** content-fidelity pass (reuses `tessellum.composer.eval.LLMJudge`).

---

## Tier 1 — Plan-level (score the generated plan vs `golden_facts.json → golden_plan`)

| # | Metric | How to measure | Pass / score |
|---|--------|----------------|--------------|
| P1 | **Planned-note count** | `count(generated planned notes)` vs golden `planned_note_count` | ratio in **[0.7, 1.4]** = pass; the golden count is a target, not exact (splits are judgment calls) |
| P2 | **BB distribution similarity** | compare generated per-note `building_block` histogram to golden `bb_distribution` | cosine similarity of the two histograms **≥ 0.8** |
| P3 | **Section-coverage completeness** | every source H2/H3 in the input pages maps to exactly one planned note (the plan's `## Section Coverage Map`); **no orphaned source section** | **0 orphans** required (this is gate G3) |
| P4 | **Split decisions present** | any input page over the caps (>2500 words OR >6 code blocks OR >400 lines) has an explicit split into ≥2 notes | every oversized page split; recorded in `## Split Decisions` |
| P5 | **Cross-ref contract declared** | the plan's `## Per-Note Related Notes Mapping` states a per-note floor matching the slice's `xref_floor_per_note` | floor declared + each planned note has an enumerated, relevance-annotated link list |
| P6 | **Gate table present** | the plan enumerates the G1..Gn validation gates (n = slice `gate_count`, 8 or 9) | all n gates named |
| P7 | **Mandatory plan sections** | the plan contains the `mandatory_plan_sections` list | ≥ 90% present |

## Tier 2 — Note-level (score each generated note; aggregate across the slice)

| # | Metric | How to measure | Pass |
|---|--------|----------------|------|
| N1 | **Frontmatter schema** | note has all `frontmatter_required_keys` in order | 9/9 keys present |
| N2 | **Forbidden-key absence** | note has NONE of `frontmatter_forbidden_keys` (esp. `title`, `note_second_category`, `folgezettel`, `last_updated`) | 0 forbidden keys |
| N3 | **Required H2 present** | `## Overview` and `## Related Notes` both present | both present |
| N4 | **Single-BB atomicity** | exactly one `building_block` value, in the closed 8-type enum | exactly 1, valid |
| N5 | **Density caps** | ≤ 2500 words, ≤ 400 lines, ≤ 6 fenced code blocks | all three under cap |
| N6 | **Cross-ref floor met** | the note's `## Related Notes` meets the slice's `xref_floor_per_note` per class (term / repo / snippet / doc) | each declared floor met |
| N7 | **Cross-ref links resolvable** | every internal `[title](rel/path.md)` in `## Related Notes` resolves to an existing note (0 ghosts, 0 broken) | 0 broken, 0 ghost (gates G5/G6) |
| N8 | **Discoverability** | the note receives ≥1 inbound link from OUTSIDE its own folder (the entry point counts) | in-degree ≥ 1 (gates G7/G8) |
| N9 | **Cross-ref block header** | the internal cross-reference block is `## Related Notes` (a `## References` section, if present, holds external URLs only) | header correct |

Aggregate a slice's Tier-2 score as the mean pass rate across its notes; report
per-metric pass rates so a regression pinpoints which contract slipped.

## Tier 3 — Content fidelity (LLM judge, per note, vs the named source page(s))

Reuse the shipped 6-dimension rubric (`DEFAULT_RUBRIC_DIMENSIONS` in
`tessellum.composer.eval`), judging each generated note against the input
page(s) its plan row cites:

- **relevance** — the note addresses the source content it claims to cover.
- **completeness** — every source H2/H3 mapped to this note is actually covered.
- **accuracy** — claims are supported by the source; no fabrication. Verbatim
  commands/config are faithful (this is gate G2, grounding).
- **clarity** — clear, well-structured prose.
- **structural_integrity** — honours the format contract (frontmatter, section
  shape, footer).
- **epistemic_congruence** — the note's shape matches its `building_block`
  (a `procedure` reads as steps; a `concept` defines; a `model` shows structure).

Each dimension 1–5. A slice passes tier 3 at **mean ≥ 4.0** across dimensions
and notes. Use `MockBackend` for a framework smoke; a real backend
(`AnthropicBackend`) for a scored run.

---

## Overall slice verdict

- **Structural (tiers 1–2):** the primary, deterministic signal — it is what the
  golden's gates enforced. Report per-metric pass rates.
- **Fidelity (tier 3):** the content-quality overlay.
- A slice is **GREEN** when tier-1 ≥ 6/7 metrics pass, tier-2 mean pass rate
  ≥ 0.9 with N2/N4/N7 (forbidden keys / single-BB / no-broken-links) at 100%,
  and tier-3 mean ≥ 4.0.

## Known golden caveats (do not penalize the generator for these)

- **Plan word estimates undershoot actuals** — the claude_code plans estimate
  ~450–650 words/note; the landed notes median ~1,430. Grade density against the
  **caps** (N5), not the plan's `~Words` estimate.
- **The benign thought_ / naming variation** — note filenames are judgment calls;
  match on the plan's declared filename set, not on a canonical spelling.
- **openclaw carries a `## References` (external) block in addition to
  `## Related Notes`** (dual blocks); claude_code and hermes use `## Related Notes`
  only. Key N9 on the slice's `cross_ref_block_header`, not a global assumption.
