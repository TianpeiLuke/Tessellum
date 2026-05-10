---
tags:
  - project
  - plan
  - tessellum
  - architecture
  - layout
  - long_term_context
keywords:
  - first-class plans folder
  - intermediate artifacts
  - long-term context management
  - repository layout
  - pipeline run artifacts
topics:
  - Repository Layout
  - Project Management
  - Long-term Context Management
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Promote `plans/` to a Top-Level Folder + Frame Intermediate-Artifact Layout

## Problem

Planning documents are a load-bearing artifact for Tessellum, but the current layout buries them:

- `plan_v01_src_tessellum_layout.md` lives at `inbox/plans/plan_*.md`.
- `inbox/` is conventionally a *drop zone* — incoming content awaiting processing into `vault/`. Plans are not transient drop-zone material; they're decisions that drive future work.
- Co-locating plans with `inbox/papers/` and `inbox/drafts/` confuses lifecycle: a plan is **load-bearing context**, not raw input awaiting digestion.

The deeper issue is **long-term context management**. Conversations end (this session has already hit context-window compression once today). Decisions need durable, navigable homes outside transcripts. Plans aren't the only such artifact — pipeline intermediates, build logs, evaluation traces, and decision records all belong in their own first-class spaces, with explicit git-tracked vs gitignored status.

This plan addresses **Step 1**: promote `plans/` to top-level. Subsequent steps (run-artifact directory, decision-record format, etc.) are scoped to a follow-up plan.

## Why This Matters — The Long-Term Context Argument

Tessellum dogfoods itself. The same arguments that motivate `vault/` (typed atomic notes for *knowledge*) apply to *project state*:

1. **Decisions deserve persistence.** A plan note ("here's how we'll structure X") encodes architectural commitment; it should outlive the chat session that produced it.
2. **Pipelines generate intermediate state.** The composer pipeline, indexer, retrieval evaluator — each emits run artifacts (logs, mid-stream JSON files, traces). These need a defined home so they're findable later, not scattered in `/tmp` or buried in `data/`.
3. **Tessellum is a system for managing knowledge construction**, not just knowledge consumption. Plans and run artifacts are *part of the construction process* — they describe and record how the vault was built.
4. **Users will need this too.** When someone runs `tessellum init <my-vault>`, they should get the same first-class plans/run-artifact structure. Bake it into the seed vault.

In short: Tessellum's value proposition (typed knowledge, long-term context) requires that *project-management state* be treated with the same first-class care as *knowledge content*.

## Survey — Tessellum's Intermediate Artifact Types

| Artifact | Example | Lifetime | Git status | Current location |
|---|---|---|---|---|
| Plan note | `plan_v01_src_tessellum_layout.md` | weeks–months | tracked | `inbox/plans/` ❌ |
| Decision record | "We chose hatch force-include over symlinks" | permanent | tracked | scattered (not a directory yet) |
| Pipeline definition | `*.pipeline.yaml` (composer chain configs) | permanent | tracked | `vault/resources/skills/` (sidecar) |
| Skill canonical | `skill_tessellum_*.md` | permanent | tracked | `vault/resources/skills/` ✓ |
| Template | `template_concept.md` | permanent | tracked | `vault/resources/templates/` ✓ |
| Built artifact | `tessellum.db`, embedding cache | regenerable | gitignored | `data/` ✓ |
| Run log | pytest output, build logs, indexer run logs | session | gitignored | (no defined home) ❌ |
| Pipeline trace | composer mid-stream JSON, retrieval eval traces | session–weeks | gitignored | (no defined home) ❌ |
| Experiment output | benchmark results, ablation matrices | varies | mixed | `experiments/` ✓ (sparsely used) |

Three rows are flagged ❌ — plans live in the wrong directory, decision records have no home, run-artifacts have no defined home. This plan addresses the first; the others are follow-ups.

## Design Principles

1. **First-class for what has long-term value.** Plans, decisions, skills, templates — these survive sessions. They get top-level or `vault/`-level homes.
2. **Gitignored for ephemeral run outputs.** Logs, traces, mid-stream pipeline files — these are session-scoped. Defined directory, but excluded from commits.
3. **`inbox/` stays a drop zone.** Don't repurpose it for "things awaiting processing" → `inbox/`. Plans are *decisions*, not drafts.
4. **Mirror in the seed vault.** `tessellum init <dir>` should scaffold `plans/` (and eventually `runs/`) so users get the structure for free.
5. **Status via YAML, not directory.** Plans use `status:` field (`active`, `completed`, `archived`, `superseded`). No `plans/active/`, `plans/completed/` subdirs — those duplicate state and create move-churn.

## Proposed Layout — This Plan's Scope

```
Tessellum/
├── src/tessellum/      Python code only
├── vault/              Knowledge vault (typed atomic notes)
├── plans/              ← NEW. Top-level. Project-management plan notes.
│   └── plan_<topic>.md
├── inbox/              Drop zone (papers, drafts, raw content awaiting processing)
│   ├── papers/
│   └── drafts/
│   └── (no more plans/ subdirectory)
├── data/               Built artifacts (gitignored, regenerable)
├── experiments/        Experiment outputs (mostly committed)
├── scripts/            Operational utilities
└── tests/              Test suite
```

**Out of scope for this plan** (deferred to follow-up `plan_run_artifacts_layout.md`):

- A `runs/` directory for gitignored run logs, traces, pipeline intermediates.
- A formal Architecture Decision Record (ADR) format and home (could be `plans/decisions/` or `vault/resources/analysis_thoughts/` — TBD).
- Promotion of `experiments/` semantics (currently sparsely used; should it always be committed, or split into `experiments/results/` committed + `experiments/runs/` gitignored?).

## Plan-Note Conventions

A plan note is a `procedure` BB note with a few specific fields:

```yaml
---
tags:
  - project              # or area for ongoing initiatives
  - plan
  - <other-topic-tags>
keywords: ...            # ≥ 3
topics: ...              # ≥ 2
language: markdown
date of note: YYYY-MM-DD
status: active           # active | completed | archived | superseded
building_block: procedure
---
```

Filename: `plan_<topic_or_initiative>.md`.

Required H2 sections (recommended pattern, not validator-enforced yet):

- `## Problem` — what this plan addresses
- `## Why This Matters` (optional but recommended) — load-bearing rationale
- `## Design Principles` (optional) — what constraints we're optimizing under
- `## Proposed <Approach>` — the concrete action
- `## Migration Steps` or `## Order of Operations` — numbered list of steps
- `## Open Questions` — what's not yet decided
- `## See Also` — cross-links to related plans, vault notes, code

## Migration Steps

1. **Create `plans/` at repo root.**
2. **Move existing plans:**
   - `inbox/plans/plan_v01_src_tessellum_layout.md` → `plans/plan_v01_src_tessellum_layout.md`
   - `inbox/plans/plan_promote_plans_to_first_class.md` (this file) → `plans/plan_promote_plans_to_first_class.md`
3. **Remove `inbox/plans/`** (now empty).
4. **Update `README.md` § Project Structure** to show `plans/` at top level; remove the `inbox/plans/` mention.
5. **Update `DEVELOPING.md` § Layout Convention** with the same.
6. **Update `pyproject.toml` `[tool.hatch.build.targets.sdist]`** — add `"plans"` to the `include` list so plans ship in the sdist (pip users get visibility into the project's planning history).
7. **Update `vault/0_entry_points/entry_master_toc.md`** to add a `plans/` reference under the navigation surface.
8. **No `tessellum init` change yet** — that command isn't shipped (per v0.1 plan step 3). When it is, the seed-vault scaffold should include an empty `plans/` directory with a placeholder README explaining the convention.
9. **Validator/CLI compatibility** — `tessellum format check` operates on any path; no code change needed. The non-note skip list already excludes `README.md` etc., which is the only file in plans/ that would need exemption.
10. **Author a follow-up plan** `plan_run_artifacts_layout.md` for the `runs/` directory + ADR format question.

## Open Questions

- **Should `plans/` have a `README.md` describing the convention?** Lean: yes — short (≤30 lines), explains the YAML pattern, lists active plans by status. The CLI skip list already exempts `README.md`, so it won't trigger validation errors.
- **Should plans link into `vault/`?** Yes. Plans are project-state; `vault/resources/analysis_thoughts/` holds *knowledge-state* (architectural arguments, FZ trails). A plan can cite a vault thought note as its rationale. The reverse is also fine — a vault note can mention an active plan.
- **Should plans be linked from a vault entry point?** Yes — add a `plans/` row to `entry_master_toc.md` so the vault reader can find project-state from the navigation root.
- **Is `archive`-status PARA bucket appropriate for completed plans?** Maybe — completed plans could move to `archives/plans/` after some time. Defer until we have ≥10 completed plans.
- **Tests?** None needed for this plan (pure file-move + doc updates). The validator runs on plans/ as on any directory; format-check parity is automatic.

## See Also

- `inbox/plans/plan_v01_src_tessellum_layout.md` — the v0.1 src/ layout plan (will move to `plans/` per Step 2)
- [README.md § Project Structure](../../README.md#project-structure) — current layout (will be updated per Step 4)
- [DEVELOPING.md § Layout Convention](../../DEVELOPING.md#layout-convention) — design rationale (will be updated per Step 5)
- [Master TOC](../../vault/0_entry_points/entry_master_toc.md) — vault navigation (will gain a `plans/` row per Step 7)

---

**Last Updated**: 2026-05-10
**Status**: Active — awaiting approval, then steps 1-9 execute as one commit; Step 10 is a follow-up plan.
