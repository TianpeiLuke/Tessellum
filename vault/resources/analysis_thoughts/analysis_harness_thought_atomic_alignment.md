---
tags:
  - resource
  - thought
  - atomicity
  - digestion_pipeline
  - granularity
  - information_architecture
keywords:
  - realized atomicity
  - thought-atomic granularity
  - section-atomic notes
  - note-size ceiling
  - decompose thought-first
  - review-gate calibration
  - augment inventory preservation
  - writer word budget
  - benchmark 31x atomicity gap
  - profile-selectable granularity
topics:
  - atomicity evaluation
  - knowledge management systems
  - note-taking methodology
language: markdown
date of note: 2026-09-10
status: active
building_block: empirical_observation
folgezettel: "7b1"
author: lukexie
---

# Realized Atomicity: The Harness Emitted Section-Scale Notes, and Aligning It to Thought-Atomic Was a Five-Layer Cascade (FZ 7b1)

## What Is Being Settled

[FZ 7b](thought_atomicity_evaluation_vault.md) evaluated the vault against Sascha's principle *in design* — "one knowledge building block per note." This node settles what the digestion harness actually PRODUCED, and whether it can be moved to the granularity a benchmark says wins. The benchmark arc on a sibling vault (the MultiHop-RAG evaluation) had found the harness's realized unit was **~346 words against a winning unit of ~11** — self-containment right, atomicity backwards by ~31×: the notes were *section-atomic* (one building block per SECTION, ~1,400–1,800 words) where the effective retrieval unit is *thought-atomic* (one THOUGHT per note, ~40–250 words by block type). One-BB-per-note was satisfied; one-THOUGHT-per-note was not. The question here is narrow and mechanical: can Tessellum's own pipeline be aligned to thought-atomic granularity end to end, and what stands in the way?

## Method

Granularity was made a **selectable profile** rather than a rewrite: `composer digest --granularity {thought,section}` (default `thought`), where the deterministic PLAN-004 ceiling / PLAN-008 floor read env-selectable accessors (thought 300/40 words, section 1800/1143 preserved so the calibrated golden eval is byte-identical). Then the native `plan → augment → review → execute` pipeline was run on a 2,161-word two-document MultiHop-RAG bundle via Claude Sonnet-4-5 on Bedrock, iterating until it built end to end. **Every fix was verified by re-running the real digest and reading the actual failure** — agent self-reports were not treated as evidence; the note bodies, gate verdicts, and materializer errors were read from disk.

## Finding — the section→thought switch was not one bug but a stack of them

Flipping the ceiling did not "just work." The bottleneck moved DOWN one pipeline layer at a time, each section-era default invisible until the layer above it was fixed:

1. **Decompose (planner).** With the thought ceiling and an 8–55 note band, the planner still emitted **4 section-sized notes (~600w)** for the 2,161-word bundle — because the decompose step was SECTION-FIRST ("classify each source heading → one note per heading"), which caps the count at the heading count regardless of the density band. Flipping it THOUGHT-FIRST (enumerate the content's atomic units, apply the split test, THEN check coverage) → **25 notes @ ~95w median**, passing every deterministic gate.
2. **Review gates.** CP1/CP4/CP6 were calibrated for section notes (≥8 term links per note, a note-COUNT plan ceiling, an 1,800-word atomicity smell). Under 25 small notes they rejected a good plan. Re-derived to the ACTIVE profile (CP6 cites the active ceiling + the split test; CP1's link floor scales with note size, SECTION ≥8 / THOUGHT ≥1, and is N-of-N; CP4 keys on SOURCE WORDS not note count) → the plan passes for the right reasons.
3. **Augment.** Steps 3–4 never received the note inventory, so the augment LLM re-imposed its section prior — it collapsed the 25-note plan to **"SECTION (2 notes): each document maps to one comprehensive section note"** and wrote per-note mappings for only 2 of 25. Feeding it the authoritative inventory + an N-of-N preservation guard (the inventory is FIXED; never re-decompose) → review APPROVES on the first pass.
4. **Execute (materializer).** The writer emitted frontmatter WITHOUT the leading `---`; the materializer rejected it and the retry ladder looped the same error. Structural absorption (restore the fence when the head is YAML carrying `output_path`) → **0 first-attempt frontmatter failures** (was ~34/run).
5. **Execute (writer verbosity).** Bodies then ran **374–638w against ~250w plans** because the per-note word target never reached the writer — it defaulted to the ≤400-line pacing cap. Threading a WORD BUDGET onto the leaf (mirroring the code-block budget) → bodies fell to **239w median, 310 max**, inside the 40–250 band.

Result: the pipeline now runs `plan → augment → review (approved, 0 rounds) → execute → completed` with all phases at 0 errors, **22 thought-atomic notes @ ~239w median** — the first thought-atomic-aligned build. All five fixes are non-destructive: section mode is byte-unchanged and the full suite (2,346 tests) stays green. Shipped to Tessellum `main`.

## What This Does and Does Not Establish

- **Does.** Tessellum CAN reproduce thought-atomic granularity end to end; the "the harness only emits section notes" barrier is removed, so 7b's principle is now realisable in practice and not just in design. The load-bearing lesson is architectural: **aligning one parameter (the atomic size) requires aligning every downstream consumer of the old assumption.** The 31× gap was not a single wrong constant — it was a *cascade* of section-era defaults (a section-first decomposer, section-calibrated review gates, a section-priored augmenter, a section-tolerant materializer, an unbudgeted writer), each of which silently re-imposed section granularity until the one above it was fixed. Atomicity is a whole-pipeline property, not a threshold.
- **Does not.** This is a SINGLE stochastic Sonnet build — by the noise-floor discipline established in the benchmark arc, one build is not a finding, only an existence proof that the path completes. The writer still over-writes the tiniest targets ~3× (75w plan → 239w body) — an LLM self-sufficiency floor: a note carrying subject + date + resolved references + a Related-Notes section rarely drops below ~150w, so ~150–250w is the realistic thought-atomic floor for THIS format, not v3's leaner ~90w. And it does NOT re-run the reader evaluation on the new thought-atomic vault: whether thought-scale notes actually lower reader refusal or fit a fixed token budget better — the budget×granularity confound the sibling vault's reader-refusal experiment left open — is the licensed next test, now buildable.

## Related Notes

- [FZ 7b: Atomicity Evaluation of the Vault](thought_atomicity_evaluation_vault.md) — the parent: evaluated one-BB-per-note in principle; this node reports that the builder's realized unit violated one-THOUGHT-per-note, and corrects it.
- [FZ 7: Atomicity Is a Universal Scaling Principle](thought_atomicity_as_universal_scaling_principle.md) — the root the correction serves: the atom's SIZE, not just its type, is the scaling variable.

## References

- Tessellum `main` — the five commits: profile-selectable granularity + thought-first decompose; review gates CP1/CP4/CP6 re-derived; augment inventory preservation; materializer frontmatter absorption; per-note writer WORD BUDGET. See `CHANGELOG.md` `[Unreleased]` (2026-09-10).
- Verification digests: the 2,161-word MultiHop-RAG bundle under `--granularity thought` (planned ~75–95w → built 22 notes @ 239w median), all phases 0 errors.
- The 31× atomicity gap and the winning ~11-word unit are the sibling MultiHop-RAG benchmark arc's finding (AbuseSlipbox vault, FZ 8c5b11a13a5g1b5i7), which motivated this alignment.
