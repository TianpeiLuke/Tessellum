---
tags:
  - project
  - plan
  - tessellum
  - architecture
  - layout
  - cqrs
  - long_term_context
keywords:
  - CQRS repository layout
  - knowledge capture workflow
  - knowledge retrieval workflow
  - first-class plans folder
  - run artifacts
  - intermediate artifacts
  - long-term context management
topics:
  - Repository Layout
  - CQRS
  - Project Management
  - System Architecture
language: markdown
date of note: 2026-05-10
status: completed
building_block: procedure
---

# Plan — CQRS Repository Layout (Workflows → Folders)

## Problem

The current Tessellum repo layout doesn't reflect the CQRS principle Tessellum's own architecture rests on. Two concrete symptoms:

- **Plans are buried** in `inbox/plans/`. `inbox/` is conventionally a *drop zone* for raw incoming content awaiting editorial digestion into typed atomic notes — that's a **System P input queue**. Plans are governance documents, not System P input.
- **Pipeline run artifacts have no home.** When the composer chain runs (DKS), when the indexer rebuilds, when retrieval is benchmarked — each generates intermediate JSON, LLM call traces, mid-stream files. These currently scatter to `/tmp` or get buried in `data/`.

This plan reorganizes the top-level folders so each one maps to a defined CQRS role. Replaces the previous narrower plan (`plan_promote_plans_to_first_class.md`); kept the file via `git mv` so history is preserved.

## CQRS in Tessellum (recap)

Tessellum is built on six pillars; CQRS is the sixth. The principle:

> Two systems share one substrate; they're joined by one cross-system rule; the boundary at the read path is sacred.
>
> — *[term_cqrs.md](../vault/resources/term_dictionary/term_cqrs.md)*

- **System P (Prescriptive)** — typed authoring, editorial discipline, the substrate of typed atomic notes.
- **System D (Descriptive)** — computational retrieval, indexes, statistical models, BB-aware re-ranking.
- **The substrate** — `vault/`. P writes; D reads.

The folder layout should make these roles visible.

## The two workflows + the bridge

### Workflow 1 — Knowledge Capture (System P)

```
External input              Editorial action            Substrate
──────────────              ────────────────            ─────────
papers/drafts/ideas    →    capture skill            →  vault/<para>/<sub>/
in inbox/<type>/            (digest, distill,           typed atomic note
                            decompose, atomize,
                            link)
                                  ↑
                            template + spec from
                            vault/resources/templates/
                            vault/resources/skills/
```

- **Reads**: `inbox/`, `vault/resources/templates/`, `vault/resources/skills/`
- **Writes**: `vault/<bucket>/<sub>/<note>.md`
- **Run artifacts**: capture-pipeline traces (currently homeless)

### Workflow 2 — Knowledge Retrieval (System D)

```
Substrate                   Built artifact              User
─────────                   ──────────────              ────
vault/   (read-only    →    data/<db>.sqlite       →   CLI / MCP query
 from D's view)             data/embeddings/           answer + citations
                            (BM25 + sqlite-vec +
                             FTS5 + PPR cache)
                                  ↑
                            indexer reads vault,
                            writes data/
```

- **Reads**: `vault/`
- **Writes**: `data/<db>` (gitignored, regenerable)
- **Run artifacts**: retrieval evaluation traces, search benchmark output (currently homeless)

### The bridge — Composer (DKS chains)

The composer pipeline is **both P and D in one chain**: it reads vault (D-style) to inform constructing new vault notes (P-style). It needs:

- **Pipeline definitions** (config YAMLs alongside skill canonicals) → permanent, committed.
- **Pipeline run traces** (intermediate JSON, LLM calls, decision logs) → session-scoped, gitignored.

Pipeline configs live in the skill bundle (`vault/resources/skills/skill_<name>.pipeline.yaml`, mirroring the parent project). Run traces are currently homeless.

## Why the current layout is wrong

Three concrete defects:

1. **`inbox/plans/` falsely claims plans are System P input.** Items in `inbox/` await editorial digestion into typed atomic notes; plans are not raw input awaiting digestion — they're decisions about how the systems get built.
2. **Run artifacts (capture, retrieval, composer) have no home.** Today they scatter to `/tmp`, get buried in `data/`, or vanish at session end. Long-term context management requires a defined home.
3. **`data/` conflates "built artifacts" with "run traces."** A DB rebuild is a regenerable build artifact; a composer chain trace is a forensic record. Same gitignored status, but different lifecycles and use cases.

## Design principles

1. **One folder per System I/O role.** vault = substrate. inbox = P input queue. data = D build output. plans = governance. runs = both-system traces.
2. **Tracked for permanent, governance, definitions.** Plans, pipeline configs, skill canonicals, templates.
3. **Gitignored for session, regenerable, traces.** DB, embeddings, run traces.
4. **Plans + run artifacts sit OUTSIDE both systems.** Plans are governance (meta to both). Run traces are runtime forensics. Neither is read or written by either system at substrate level — they don't belong in `vault/` or `inbox/` or `data/`.
5. **Mirror in `tessellum init` seed vault.** When users run `tessellum init <my-vault>`, they should get the same first-class structure.

## Proposed top-level layout

```
Tessellum/
├── src/tessellum/      Code — engines for both systems P and D
├── vault/              Shared substrate — typed atomic notes
│   ├── 0_entry_points/
│   ├── resources/      ← skills, templates, term_dictionary, how_to, ...
│   ├── projects/  areas/  archives/  examples/
├── inbox/              System P input queue (drop zone for raw incoming)
│   ├── papers/         drafts/  ...    ← (no more inbox/plans/)
├── data/               System D build output (gitignored, regenerable)
│   ├── tessellum.db    embeddings/
├── runs/               Both-system runtime traces (gitignored)  ← NEW
│   ├── capture/        capture-pipeline traces
│   ├── retrieval/      retrieval eval + benchmark traces
│   └── composer/       DKS chain run traces
├── plans/              Governance — meta to both systems (committed)  ← NEW (top-level)
│   └── plan_<topic>.md
├── experiments/        Experiment outputs (mostly committed)
├── scripts/            Operational utilities (capture/retrieval/maintenance code)
└── tests/              Test suite
```

## System × lifecycle matrix

| Folder | System | Role | Git status |
|---|---|---|---|
| `vault/` | shared substrate | typed atomic notes; P writes, D reads | tracked |
| `vault/resources/templates/` | System P spec | copy-and-fill skeletons | tracked |
| `vault/resources/skills/` | both | skill canonicals + pipeline sidecars | tracked |
| `inbox/` | **System P input queue** | drop zone for raw incoming content | tracked |
| `data/` | **System D build output** | DB + embeddings + indexes | gitignored |
| `runs/capture/` | System P runtime | capture-pipeline traces | gitignored |
| `runs/retrieval/` | System D runtime | retrieval eval + benchmark traces | gitignored |
| `runs/composer/` | both — bridge runtime | DKS chain run traces | gitignored |
| `plans/` | **governance — meta to both** | project decisions, layout, milestones | tracked |
| `experiments/` | mostly System D | benchmark results, ablations | mixed |
| `scripts/` | **meta — dev/maintenance** | one-off vault migrations, repo maintenance, contributor helpers; **not** shipped in the wheel. Core capabilities live in `src/tessellum/cli/` instead. | tracked |
| `src/tessellum/` | both | code | tracked |
| `tests/` | both | test suite | tracked |

### `scripts/` vs `src/tessellum/cli/`

A subtlety worth calling out, since both directories hold "things you run from a terminal":

- **`src/tessellum/cli/<subcommand>.py`** — recurring capabilities exposed via the `tessellum` console script. Ships in the wheel. Examples (shipped or planned): `format_check.py`, `init.py`, `capture.py`, `index.py`, `search.py`. Users invoke via `tessellum format check vault/`, `tessellum init my-vault/`, etc.
- **top-level `scripts/`** — one-off operational utilities. NOT shipped in the wheel. Examples (potential): `rename_legacy_tag.py` (one-time vault migration after a convention change), `backfill_status.py` (one-time repo cleanup), `run_all_checks.sh` (contributor convenience). Run via `python scripts/<name>.py` from the repo checkout, never via the installed `tessellum` command.

**Decision rule**: if it represents a recurring capability users will run ≥3 times, it's a CLI subcommand. If it's a one-time migration or contributor helper, it's a top-level script.

See [`scripts/README.md`](../scripts/README.md) for more.

## Concrete examples — what lives in each folder

- **`plans/plan_v01_src_tessellum_layout.md`** — milestone plan for v0.1 release.
- **`plans/plan_cqrs_repo_layout.md`** — this very plan (after migration step 3).
- **`runs/composer/2026-05-10T14-30-22_chain_decompose-paper-abc.json`** — single composer run trace; agent calls + intermediate artifacts.
- **`runs/retrieval/bench_2026-05-10_query-recall.json`** — retrieval benchmark output.
- **`runs/capture/digest_paper-foo_2026-05-10.log`** — capture skill run log.
- **`data/tessellum.db`** — built SQLite + sqlite-vec + FTS5 unified backend.
- **`data/embeddings/all-MiniLM-L6-v2/`** — cached dense embeddings.
- **`inbox/papers/2026-arxiv-foo.pdf`** — paper waiting to be digested.
- **`vault/resources/skills/skill_tessellum_format_check.md`** — canonical body.
- **`vault/resources/skills/skill_tessellum_decompose-note.pipeline.yaml`** — pipeline sidecar (when shipped).

## Migration steps

Execute as ONE commit (separate from this planning commit):

1. **Create `plans/`** at repo root with a short `README.md` explaining the convention (status field, recommended sections).
2. **Create `runs/`** at repo root with a short `README.md` and three subdirectories: `capture/`, `retrieval/`, `composer/`. Each subdirectory gets a `.gitkeep`.
3. **Move existing plans:**
   - `inbox/plans/plan_v01_src_tessellum_layout.md` → `plans/plan_v01_src_tessellum_layout.md`
   - `inbox/plans/plan_cqrs_repo_layout.md` (this file) → `plans/plan_cqrs_repo_layout.md`
4. **Remove `inbox/plans/`** (now empty).
5. **Update `.gitignore`** to ignore `runs/` contents but track the structure:

   ```gitignore
   runs/**
   !runs/
   !runs/README.md
   !runs/*/
   !runs/*/.gitkeep
   ```

6. **Update `pyproject.toml` `[tool.hatch.build.targets.sdist]`:**
   - Add `"plans"` to `include` (plans ship in sdist for transparency).
   - Add `"runs"` to `exclude` (session traces don't ship).
7. **Update `README.md` § Project Structure** with the new top-level tree (this plan's `## Proposed top-level layout` block is the authoritative diagram).
8. **Update `DEVELOPING.md` § Layout Convention** with the same structural change + a brief paragraph linking the layout to CQRS workflows.
9. **Update `vault/0_entry_points/entry_master_toc.md`** — add a `plans/` row to the navigation surface so the vault reader can find project-state from the navigation root.
10. **No `tessellum init` change yet** — that command isn't shipped. Note in v0.1 plan: when init is built, scaffold `plans/` + `runs/` + `inbox/` + `data/` as part of the seed.
11. **Re-run `tessellum format check vault/ plans/`** to confirm both directories validate clean.

## Plan-note convention (stays as in the previous plan)

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

Filename: `plan_<topic_or_initiative>.md`. Status is a YAML field — no `plans/active/`, `plans/completed/` subdirs (avoids move-churn).

Recommended H2 sections: `## Problem`, `## Why This Matters` (when load-bearing), `## Design Principles`, `## Proposed <Approach>`, `## Migration Steps` / `## Order of Operations`, `## Open Questions`, `## See Also`.

## Run-artifact convention

`runs/` is gitignored except for `README.md` and `.gitkeep` files. Subdirectories hold per-run traces with timestamps in filenames for chronological ordering: `<runs-subdir>/<YYYY-MM-DDThh-mm-ss>_<chain-or-task>.<ext>`.

When `tessellum compose <chain>` ships in v0.1+, it should write its trace to `runs/composer/`. When `tessellum search --eval` ships, it writes to `runs/retrieval/`. Capture skills that go through multi-step LLM chains should write to `runs/capture/`.

## Open questions

- **`runs/README.md` granularity** — one top-level README, or one per subdirectory? Lean: one top-level + one per subdir, each ≤30 lines.
- **`experiments/` semantics** — currently sparsely used; should we redefine as "always committed" + move "throwaway run output" to `runs/`? Defer to a follow-up.
- **ADR (Architecture Decision Record) format** — could be a `plans/decisions/` subdir, or a separate top-level `decisions/`, or fold into `vault/resources/analysis_thoughts/`. Defer until we have ≥3 ADRs to migrate.
- **Should plans link bidirectionally with `vault/resources/analysis_thoughts/`?** A plan describes *project state*; a thought note describes *knowledge state*. The two often relate (plan_v01_src_tessellum_layout cites thought_six_pillars_architecture). Yes — encourage cross-links, no folder change needed.

## See Also

- [`term_cqrs.md`](../vault/resources/term_dictionary/term_cqrs.md) — the principle this layout implements
- [`plan_v01_src_tessellum_layout.md`](plan_v01_src_tessellum_layout.md) — v0.1 src/ shipping plan (will move to `plans/` per Step 3)
- [README.md § Project Structure](../README.md#project-structure) — current layout (will be updated per Step 7)
- [DEVELOPING.md § Layout Convention](../DEVELOPING.md#layout-convention) — design rationale (will be updated per Step 8)
- [`entry_master_toc.md`](../vault/0_entry_points/entry_master_toc.md) — vault navigation root (will gain a `plans/` row per Step 9)

---

**Last Updated**: 2026-05-10
**Status**: **Complete** — all 11 migration steps shipped.

| Step | Description | Verified |
| ---- | ----------- | -------- |
| 1 | Create `plans/` with README | `plans/README.md` exists |
| 2 | Create `runs/` with `capture/`, `retrieval/`, `composer/` subdirs + `runs/README.md` | `runs/README.md` + 3 subdirs present |
| 3 | Move plans out of `inbox/plans/` to top-level `plans/` | all 4 plans live at `plans/*.md` |
| 4 | Remove now-empty `inbox/plans/` | `inbox/` no longer has a `plans/` subdir |
| 5 | `.gitignore` ignores `runs/**` but tracks structure | Confirmed: `runs/**` + `!runs/`, `!runs/README.md`, `!runs/*/`, `!runs/*/.gitkeep` |
| 6 | `pyproject.toml` sdist `include: plans` + `exclude: runs` | Verified in `[tool.hatch.build.targets.sdist]` |
| 7 | Update `README.md` § Project Structure | Done |
| 8 | Update `DEVELOPING.md` § Layout Convention | Done |
| 9 | Update `entry_master_toc.md` with `plans/` row | Done |
| 10 | Defer `tessellum init` change until init ships | `tessellum init` since shipped; the seed scaffold matches this layout |
| 11 | Re-run `tessellum format check vault/ plans/` | Passing as part of the 464-test suite |

**Run-artifact convention in active use:** `runs/composer/<filesystem-safe-timestamp>_<skill>.json` is written by the Composer scheduler (Wave 3). The `runs/capture/` and `runs/retrieval/` paths are reserved per convention but no skill currently writes there.

**Open questions still open:**

- *`runs/README.md` granularity*: shipped one top-level README; per-subdir READMEs not written (no demand yet).
- *`experiments/` semantics*: deferred; unchanged.
- *ADR format*: deferred — still no ADRs to migrate.
- *Plan ↔ analysis_thoughts cross-links*: encouraged; nothing enforced.
