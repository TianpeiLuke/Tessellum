# Changelog

All notable changes to Tessellum are documented here. The format is loosely [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.1.0 — Public Beta

- Engine port from parent project (composer + retrieval primitives)
- 20 essential skills (capture / search / answer / trail management / maintenance)
- 8 BB-type example notes (one per Building Block)
- Conceptual primer term notes (Z + PARA + BB + Epistemic Function + DKS + CQRS)
- Public-facing how-to library (getting-started, note-format, agent-integration, growing a trail)
- MCP server exposing v0.1 skills as tools
- CI workflow (ruff + pytest + format/link validators)
- `tessellum init` / `capture` / `format check` / `search` CLI subcommands
- Hatch `force-include` wiring so `vault/resources/templates/` ships in the wheel

## [0.0.35] — 2026-05-10

### Added — Correction of Errors (COE) review-and-reflect surface

The seed vault now ships the full COE practice — the method, the agent-executable skill, and the index — generalised as public knowledge. Every install can document and learn from incidents using a structured, blameless format.

#### 4 new files

| File | Role |
|------|------|
| `vault/resources/term_dictionary/term_coe.md` | The method, the 9-section document shape, the 5 Whys discipline, the action-item priorities, the anti-patterns. Scrubbed of all Amazon-internal references (`coe.a2z.com`, `w.amazon.com`, "coe-watchers@", Leadership Principles, "all Amazonians"). |
| `vault/resources/skills/skill_tessellum_write_coe.md` | Agent-executable skill canonical. 6 steps: gather incident details → 5 Whys → write COE → check duplicates → verify → update index. Renamed from `slipbox-write-coe` → `tessellum-write-coe`; the `note_second_category`, `related_skill_headers`, and FZ-12a references are stripped. |
| `vault/resources/skills/skill_tessellum_write_coe.pipeline.yaml` | Composer-compatible sidecar. Dropped `mcp_dependencies: session-mcp` — agents pass incident details directly via leaf metadata (`title` + `summary`). Schema converted from non-standard `format: markdown_with_frontmatter` / `xml_tag_list` to Tessellum's JSON-schema shape with `required: [output_path]` / `[edits]`. |
| `vault/0_entry_points/entry_coes.md` | The COE index — Quick Stats counters + COE Index table + Recurring Patterns section. Step 6 of the skill updates this file with each new COE. |

#### Composer integration

```
$ tessellum composer validate vault/resources/skills/skill_tessellum_write_coe.md
OK   skill_tessellum_write_coe.md (6 steps)

$ tessellum composer compile vault/resources/skills/skill_tessellum_write_coe.md
compiled skill_tessellum_write_coe — 6 steps:
  1. step_1_gather_incident_details             [CORE/per_leaf]   ⇒ no_op
  2. step_2_perform_5_whys_root_cause_analysis  [CORE/per_leaf]   ⇒ no_op
  3. step_3_write_coe_note                      [CORE/per_leaf]   ⇒ body_markdown_frontmatter_to_file
  4. step_4_check_for_duplicates                [CORE/per_leaf]   ⇒ no_op
  5. step_5_verify                              [CORE/per_leaf]   ⇒ no_op
  6. step_6_update_coe_entry_point              [DEFERRED/cross_leaf] ⇒ edits_apply_xml_tags
```

Run end-to-end with `tessellum composer run vault/resources/skills/skill_tessellum_write_coe.md --leaves leaves.json` where `leaves.json` carries one `{title, summary}` object per incident.

#### Scrubs

What was removed from the source notes to ship as public knowledge:

- Amazon-internal URLs (`coe.a2z.com`, `w.amazon.com`, `broadcast.amazon.com`, `t.corp.amazon.com`, `learn.a2z.com`)
- Amazon-specific Leadership Principles section (Ownership / Customer Obsession / Dive Deep / etc.)
- Visibility classifications (Standard / Secure / Team-Only COE — Amazon's mailing-list-based escalation)
- "All Amazonians" / "coe-watchers@" / "VP escalation" / "manager-level" — replaced with neutral "team" / "organization" language
- Two-week mandatory timeline framed as a *common convention* rather than a corporate mandate
- Internal training-doc links to AB-specific paths
- Specific COE examples (Amazon Video EU outage, S3 multi-region) — dropped

What's kept (the load-bearing content):

- 5 Whys method + stop-sign list
- 9-section document structure
- Action item priorities (High 30d / Medium 60d / Low 90d / None 365d) — framed as one common convention
- SMART action item definition
- Anti-pattern list (don't blame individuals, don't stop at "operator error", etc.)
- The blameless / systems-and-processes-only principle

#### Master TOC update

The dogfood vault's `entry_master_toc.md` gets a "Document a failure / learn from a mistake" row in the *I'm new — where do I start?* table, plus a row for `entry_coes` in the *Entry Points by Surface* table.

### Seed manifest

- `_seed_manifest.py` extended from 33 → 37 entries (3 new .md files + 1 sidecar yaml = 4 grafts).
- `tessellum init` now scaffolds **54 markdown files** (was 51 in v0.0.34) + 1 sidecar yaml = 55 total.

### Verification

- All 4 new files pass `tessellum format check` with **0 errors and 0 warnings**.
- `tessellum composer validate` on the skill: passes.
- `tessellum composer compile` on the skill: produces a clean 6-step DAG with all materializer contracts resolved.
- Editable + wheel mode both produce identical file lists.
- Full suite: 468 passed, 1 skipped.

## [0.0.34] — 2026-05-10

### Changed — Single source of truth for the seed-vault file list

Adding a seed file used to require editing **two** files: `pyproject.toml` (force-include mapping) and `src/tessellum/init.py` (`_SEED_VAULT_MANIFEST`). The two had to stay in sync; a missed edit on either side meant the wheel either shipped a file the runtime didn't copy, or copied a file the wheel didn't ship.

v0.0.34 collapses this to **one** edit point. The Python tuple in `src/tessellum/data/_seed_manifest.py` (`SEED_VAULT_MANIFEST`) is now the only place the list is declared. Both ends of the pipeline read it:

- **Wheel build time**: a custom Hatch build hook (`hatch_build.py`) loads the manifest via `importlib.util` and registers each entry as a `force_include` mapping (`vault/X` → `src/tessellum/data/seed_vault/X`). Discovered automatically because Hatch picks up the `[tool.hatch.build.targets.wheel.hooks.custom]` block in pyproject.
- **Runtime**: `src/tessellum/init.py` imports `SEED_VAULT_MANIFEST` directly from the same module. The `tessellum init` copy loop iterates it.

#### New files

- `src/tessellum/data/_seed_manifest.py` — the canonical tuple (33 entries currently, grouped by category with inline comments).
- `hatch_build.py` (repo root) — the build hook. Implements `BuildHookInterface.initialize` to set `build_data["force_include"]` from the manifest.

#### Files changed

- `pyproject.toml` — the per-file `force-include` block (33 entries) deleted; replaced with a 4-line `[tool.hatch.build.targets.wheel.hooks.custom]` registration. The `vault/resources/templates → src/tessellum/data/templates` directory-copy entry stays as a static `force-include` (different shape from the manifest's per-file mappings).
- `src/tessellum/init.py` — the inline `_SEED_VAULT_MANIFEST` tuple (50 lines) replaced with `from tessellum.data._seed_manifest import SEED_VAULT_MANIFEST as _SEED_VAULT_MANIFEST`.

#### Verification

- Editable mode: `python3 -c "from tessellum.data._seed_manifest import SEED_VAULT_MANIFEST; print(len(SEED_VAULT_MANIFEST))"` → 33.
- Wheel build: `python -m build` succeeds; `unzip -l dist/tessellum-0.0.34-py3-none-any.whl | grep -c seed_vault` → 33 files (matches manifest).
- Editable + wheel mode `tessellum init` both produce **51 markdown files** (33 manifest + 15 templates + master TOC + README + 1 template directory README).
- Full suite: 468 passed, 1 skipped.

#### Adding a seed file from v0.0.34 onward

```python
# src/tessellum/data/_seed_manifest.py
SEED_VAULT_MANIFEST: tuple[str, ...] = (
    # ... existing entries ...
    "resources/term_dictionary/term_my_new_concept.md",   # ← one new line
)
```

That's it. The build hook picks it up at the next `python -m build`; `tessellum init` picks it up on the next install.

## [0.0.33] — 2026-05-10

### Added — Trail 3 (Retrieval / System D)

The seed vault now ships **three FZ trails** (was two in v0.0.32). The new trail documents how Tessellum's retrieval system was tested into shape — the 14-strategy bake-off across 4,823 questions, the unified-engine breakthrough, the +12pp hybrid-RRF lift, and the Hit@K-to-answer-quality disconnect that ruled out PPR.

#### Trail 3 — Retrieval (2 nodes)

```
3     thought_retrieval_evolution    (NEW — 8-step experimental descent)
└── 3a  thought_retrieval_synthesis  (NEW — 1 substrate + 4 surfaces + 1 metadata filter)
```

| FZ | Note | Role |
|----|------|------|
| `3` | `thought_retrieval_evolution.md` | Eight experimental steps: foundational benchmark (Dense Hit@5=0.815) → shared LIKE bottleneck → gold-design confound → unified-engine hypothesis → parity test (BM25 fails ρ=0.85; Plan B triggered) → Plan B + hybrid RRF (+12pp lift) → priority-graph rescues PPR on Hit@K → ★ Hit@K-to-answer-quality disconnect (ρ=0.37) rules out PPR for production. |
| `3a` | `thought_retrieval_synthesis.md` | The shipped design: one substrate (SQLite + sqlite-vec + FTS5 in one file), four retrieval surfaces (hybrid RRF default + BM25 + dense + best-first BFS) plus one parallel metadata-filter surface (`tessellum filter`). Five operational rules + a 2×2 of question-shape-to-surface mapping. |

#### `entry_retrieval_trail.md` (NEW per-trail entry point)

Same shape as the existing Architecture and Dialectic trail entries: ASCII tree, FZ table, summary table of the 8 experimental moves, what's shipped (Wave 1-5 mapping), what the trail rejects, reading order, related trails. The per-trail entry is the place to start when reading Trail 3.

#### Updated master `entry_folgezettel_trails.md`

One new row in the trail index pointing at the new per-trail entry. Status line updated to "3 trails shipped, 8 nodes total."

### Seed manifest

- `pyproject.toml` — 3 new `force-include` entries (2 thoughts + 1 entry point).
- `init.py` — `_SEED_VAULT_MANIFEST` extended 30 → 33 relative paths.
- `tessellum init` now scaffolds **51 markdown files** (was 48 in v0.0.32).

### Verification

- All 3 new files pass `tessellum format check` with **0 errors and 0 warnings** each.
- Updated `entry_folgezettel_trails.md` also passes 0/0.
- Editable + wheel mode both produce 51 files.
- Full suite: 468 passed, 1 skipped.

## [0.0.32] — 2026-05-10

### Added — Trail 2 (Dialectic / DKS) + per-trail entry-point refactor

The seed vault now ships **two FZ trails** (was one in v0.0.31). The new trail documents how the Dialectic Knowledge System (DKS) was reasoned into shape; the refactor cleans up the trail-map structure so each trail has its own per-trail entry point and the master map stays slim.

#### Trail 2 — Dialectic (2 nodes)

```
2     thought_dks_evolution         (NEW — six-step descent)
└── 2a  thought_dks_design_synthesis  (NEW — 7-component pattern + 3 foundations + 2 timescales)
```

| FZ | Note | Role |
|----|------|------|
| `2` | `thought_dks_evolution.md` | Six-step descent: (1) library → learning loop, (2) three-layer framing rejected, (3) empirical anchor from a production closed loop, (4) formal foundations (Dung AF + Toulmin + IBIS), (5) substrate-protocol separation counter, (6) six completing innovations. |
| `2a` | `thought_dks_design_synthesis.md` | The 7-component pattern (one per BB-to-BB epistemic edge), three formal foundations, four design commitments (queryable+mutable substrate; warrant-level learning; dialectical adequacy termination; confidence-gated escalation), two timescales (intra-record minutes + inter-cycle weeks), five "what DKS is NOT" carve-outs. |

The trail is short by design — two notes is enough to record the architectural commitment that constrains how the DKS runtime gets built in v0.2+.

#### Per-trail entry-point refactor

`entry_folgezettel_trails.md` was carrying both *master-index* duties (which trails exist) and *Trail 1 detail* duties (Trail 1's ASCII tree, FZ table, reading order). As a second trail joins the vault, that bundling becomes noise. Refactor:

- **`entry_folgezettel_trails.md`** — slim master index. One row per trail (root link, per-trail entry-point link, node count, subject). Includes a "how to grow a new trail" section.
- **`entry_architecture_trail.md`** (NEW) — Trail 1's per-trail entry. ASCII tree, FZ table, dialectic-in-one-line summary, reading order, "what this trail rejects" carve-outs, related trails.
- **`entry_dialectic_trail.md`** (NEW) — Trail 2's per-trail entry. Same shape as Architecture trail's entry point; summarises the six-move dialectic progress that produced DKS.

When a user grows a new trail, they'll author `entry_<trail>_trail.md` and add one row to the master map. Same convention every time.

### Seed manifest

- `pyproject.toml` — 4 new `force-include` entries (2 thoughts + 2 entry points). `entry_folgezettel_trails.md` rewritten in place.
- `init.py` — `_SEED_VAULT_MANIFEST` extended 26 → 30 relative paths.
- `tessellum init` now scaffolds **48 markdown files** (was 44 in v0.0.31).

### Verification

- All 4 new files pass `tessellum format check` with **0 errors and 0 warnings** each.
- Refactored `entry_folgezettel_trails.md` also passes 0/0.
- Editable + wheel mode both produce 48 files.
- Full suite: 468 passed, 1 skipped.

## [0.0.31] — 2026-05-10

### Added — Architecture FZ trail (an example trail in the seed vault)

Every Tessellum install now ships **Trail 1 — Architecture**, a 4-note Folgezettel descent that documents how Tessellum's CQRS architecture was reasoned into shape. The trail exists for two purposes simultaneously:

1. **Architectural reasoning record** — a contributor asking "why two systems and not three?" reads the trail and gets the explicit argument.
2. **Worked FZ example** — a user authoring their first trail copies the trail's shape (linear descent, both-or-neither parent/child IDs, master-map row in `entry_folgezettel_trails.md`).

#### The 4-note descent

```
  1       Building Block Ontology Relationships  (substrate)
  └── 1a  How the CQRS Architecture Evolved      (four-step narrative)
      └── 1a1   Two-Systems CQRS Synthesis       (pivot — the moment of clarity)
          └── 1a1a   The Essence of CQRS for Tessellum  (distilled thesis)
```

| FZ ID | Note | Role |
|-------|------|------|
| `1` | `thought_building_block_ontology_relationships.md` | The 8 BB types + 10 epistemic edges Sascha-extension graph that everything else descends from. Pre-existed in v0.0.28+; v0.0.31 adds FZ fields (`folgezettel: "1"`, `folgezettel_parent: ""`) to mark it as trail root. |
| `1a` | `thought_cqrs_design_evolution.md` (NEW) | The four-step descent: substrate → three-regime framing (rejected) → two-systems counter → CQRS synthesis. The "what was tried and why" record. |
| `1a1` | `thought_synthesis_two_systems_cqrs_value_proposition.md` | The pivotal synthesis — System P (Ontology + DKS, prescriptive) ⊥ System D (Retrieval, descriptive) ⊥ one shared substrate. Pre-existed in v0.0.28+; v0.0.31 renumbers from AB's `7g1a1a1a1a1` to Tessellum-native `1a1`. |
| `1a1a` | `thought_cqrs_essence_for_tessellum.md` (NEW) | The distilled user-facing thesis: one boundary (declaration vs computation), two disciplines, one substrate. Plus the 5 rules that fall out, and the explicit "what CQRS is *not*" carve-outs. |

#### `entry_folgezettel_trails.md` — the trail map (NEW)

The new entry point indexes all FZ trails in the vault (currently just Trail 1) and demonstrates the convention:

- Per-trail table row with root link, node count, reading time, subject.
- ASCII descent diagram showing `1 → 1a → 1a1 → 1a1a`.
- Detailed per-node table (FZ ID, note link, BB type, role).
- "How to grow a trail" — concrete instructions for adding child nodes.
- Reading order — top-down for the first read, leaf-up for re-reads.

#### Seed manifest + wheel

- `pyproject.toml` — 5 new `force-include` entries (4 thoughts + 1 entry point).
- `init.py` — `_SEED_VAULT_MANIFEST` extended from 21 to 26 relative paths.
- `tessellum init` now scaffolds **44 markdown files** (was 39 in v0.0.30).

#### Verification

- All 4 trail notes pass `tessellum format check` with **0 errors**. Warnings are only `LINK-003` (links to non-shipped notes — expected).
- FZ parent/child consistency: every `folgezettel_parent:` resolves to a shipped sibling node. Trail-root note uses `folgezettel_parent: ""` per the validator's both-or-neither rule.
- Editable + wheel install parity: both produce 44 files.
- Full suite: 468 passed, 1 skipped.

## [0.0.30] — 2026-05-10

### Added — System-regularization layer in the seed vault

Four new notes complete the minimal-seed mission set by `plans/plan_minimal_seed_vault.md`. The seed now answers both **user questions** ("what is this system?", "how do I use it?") and **system / agent questions** ("which BB type fits my note?", "what's the format contract?") without external docs.

#### 1. `term_format_spec.md` — The format contract in vault form (220 lines)

The validator's authoritative spec, written as a readable note. Documents:

- Required YAML frontmatter fields + their issue codes (`YAML-010` … `YAML-101`)
- The closed enums for `building_block:` (8 types) and `status:` (5 values)
- Tag conventions — `tags[0]` = PARA bucket, `tags[1]` = second category, `tags[2..]` = domain tags
- Folgezettel both-or-neither rule (`TESS-001`/`TESS-002`)
- Forbidden field rules (`TESS-003`)
- Link rules — relative paths only, no wikilinks, `.md` required (`LINK-001` … `LINK-006`)
- Filename + directory conventions per capture flavor
- A complete quick-reference table mapping every validator issue code to its meaning

When `tessellum format check` cites a code, this note explains what it means and how to fix it.

#### 2. `entry_building_block_index.md` — The BB picker matrix (~100 lines)

The 8-row scannable matrix every agent / contributor consults when classifying a new note:

| Column | What it tells you |
|---|---|
| BB type | The `building_block:` value to use |
| Question it answers | "What is it called?" / "How is this structured?" / etc. |
| Epistemic function | Naming / Structuring / Predicting / Claiming / Refuting / Observing / Doing / Indexing |
| Layer | Knowledge / Reasoning / Action / Meta |
| Required sections | The H2 headings the note must contain |
| Default directory | Where the file lands |

Plus the 10 epistemic edges (the DKS dialectic graph) as a separate table. Data derived from `tessellum.format.building_blocks.BB_SPECS` + `EPISTEMIC_EDGES` — the note is the readable shadow of the Python source.

#### 3. `acronym_glossary_tessellum_foundations.md` — One-glance lookup for the 11 foundation terms (~150 lines)

A glossary in the same format as the existing 5 universal glossaries, but covering Tessellum's foundation vocabulary: Z, Slipbox, FZ, PARA, BASB, CODE, Knowledge BB, BB, EF, DKS, CQRS. Each entry: one-line "what it is" + key idea + `→` link to the full term note + source citation. Organized into "Methodology Lineage" (7 terms Tessellum descends from) and "Tessellum-Specific Architecture" (4 terms unique to this project). Closes with an "How these fit together" diagram and an opinionated 7-step reading order.

Added as a new row in `entry_acronym_glossary.md` under a "Tessellum-specific (read first)" header.

#### 4. `howto_first_vault.md` — The 8-step CLI walkthrough in vault form (~150 lines)

The README Quick Start re-authored as a vault how-to, so users who open a fresh `tessellum init` vault in Obsidian (rather than reading the GitHub README) see the procedural on-ramp. 8 steps:

1. Scaffold a vault (`tessellum init`)
2. Capture your first note (`tessellum capture concept page_rank`)
3. Fill the template
4. Validate (`tessellum format check`)
5. Index (`tessellum index build`)
6. Search (`tessellum search`)
7. Capture a skill (paired canonical + sidecar)
8. Compose (`tessellum composer validate / compile / run`)

Each step has the exact command + expected output line so the user can verify they're on track. Closes with a verification table and a "Going further" section.

### Updated — Wheel manifest + init.py

- `pyproject.toml` — 4 new `force-include` entries graft each new note into `src/tessellum/data/seed_vault/`.
- `init.py` — `_SEED_VAULT_MANIFEST` extended from 17 to 21 relative paths.

### Verification

- All 4 new notes pass `tessellum format check` with **0 errors and 0 warnings** each.
- Editable-mode `tessellum init` produces 39 markdown files (was 35 in v0.0.29).
- Wheel-mode init produces the same 39 files.
- Full suite: 468 passed, 1 skipped.
- Cross-links: the 4 new notes reference each other and the existing 11 foundation terms; the existing 11 foundation terms now have inbound links from the new spec / picker / glossary / how-to.

### Closes the plan

`plans/plan_minimal_seed_vault.md` is now complete. The default `tessellum init` ships:

- **15 templates** (the executable per-BB spec)
- **11 foundation term notes** (the conceptual vocabulary)
- **1 system-regularization term note** (`term_format_spec.md` — the format contract)
- **2 entry-point indexes** (master TOC + BB picker)
- **6 acronym glossaries** (Tessellum foundations + 5 universal lookups)
- **1 master glossary index** (`entry_acronym_glossary.md`)
- **1 how-to** (`howto_first_vault.md` — the practical walkthrough)
- **1 README** (per-vault, generated)

Every install gets the same 39 files. Every file passes format check with 0 errors.

## [0.0.29] — 2026-05-10

### Added — 3 more foundation term notes (BASB, CODE, Knowledge Building Blocks)

Per user feedback that the v0.0.28 seed didn't cover enough of the foundational vocabulary, three more pillar/lineage term notes now ship by default:

- **`term_knowledge_building_blocks.md`** (152 lines) — Sascha Fast's historical taxonomy of knowledge atoms (premises, logical form, conclusion, definitions, distinctions, heuristics). This is the predecessor concept Tessellum's typed BB ontology builds on. Without it, `term_building_block.md` lacks its historical anchor.
- **`term_basb.md`** (117 lines) — *Building a Second Brain* by Tiago Forte. The PKM movement Tessellum descends from on the personal-knowledge-management side. Defines what "second brain" means and why it matters.
- **`term_code_method.md`** (108 lines) — CODE (Capture / Organize / Distill / Express) — Forte's lifecycle framework. The procedural complement to PARA's organizational scheme.

Seed now ships 11 foundation term notes total — every term a new user needs to make the rest of the vocabulary legible.

### Fixed — Scrubbed residual internal references from 3 shipped term notes

The v0.0.28 ship included three terms with leftover Amazon / abuse-domain references in their bodies. Scrubbed to ship as general public knowledge:

| Term | Was | Now |
| ---- | --- | --- |
| `term_zettelkasten.md` | 8 internal hits — a whole "Application in Abuse Prevention" H2 section, "Internal Examples" sub-section, internal-wiki link list in References, footer status referencing the parent project | 0 hits. Application section dropped. Internal Examples replaced with a "Public Implementations" section pointing at Tessellum. Tools-supporting table cleaned (dropped Quip / internal entries; added Logseq and Tessellum). Internal-wiki link list removed. Footer status simplified. |
| `term_slipbox.md` | 4 internal hits — "Abuse slipbox" H3 sub-section, internal-wiki link list, contact line | 0 hits. Internal sub-section dropped. Internal-wiki link list dropped. Contact line dropped. |
| `term_dialectic_knowledge_system.md` | 2 internal hits — one row in the "Dialectic Spectrum" table, one See Also link referring to internal architecture | 0 hits. Table row genericized to "typical typed slipbox". See Also link genericized to "a typed-slipbox architecture". |

All 11 foundation terms now pass `tessellum format check` with 0 errors, 0 Amazon-internal word-boundary hits, and 0 Amazon-domain phrase hits.

### Added — `pyproject.toml` force-include entries

Three new entries graft `term_knowledge_building_blocks.md`, `term_basb.md`, `term_code_method.md` into `src/tessellum/data/seed_vault/resources/term_dictionary/` at wheel build time.

### Updated — `_SEED_VAULT_MANIFEST` in `init.py`

The explicit manifest now lists all 11 foundation terms (was 8 in v0.0.28). The rendered master TOC in `_render_master_toc` reorganizes the conceptual primer into two tables: "Methodology lineage" (7 terms: Z, Slipbox, FZ, PARA, BASB, CODE, Knowledge BB) and "Tessellum-specific architecture" (4 terms: BB, EF, DKS, CQRS).

### Verification

- Editable-mode `tessellum init` produces 35 markdown files (was 32 in v0.0.28).
- Full suite: 468 passed, 1 skipped.
- Clean-venv wheel install lands all 11 foundation terms in `resources/term_dictionary/`.

## [0.0.28] — 2026-05-10

### Added — Seed vault gains 14 starter notes

`tessellum init <dir>` now scaffolds a substantially richer vault. Before v0.0.28, init produced one term note (`term_building_block.md`) plus the templates. Now it produces:

- **8 pillar / supporting term notes** in `resources/term_dictionary/`:
  - `term_building_block.md` — the 8 BB-type ontology + 10 epistemic edges
  - `term_epistemic_function.md` — what each BB does (name / structure / predict / claim / refute / observe / act / index)
  - `term_dialectic_knowledge_system.md` — closed-loop dialectic compaction protocol
  - `term_cqrs.md` — System P (typed substrate) ⊥ System D (retrieval) ⊥ one shared substrate
  - `term_zettelkasten.md` — atomic notes + bidirectional links (Luhmann's method)
  - `term_para_method.md` — Projects / Areas / Resources / Archives
  - `term_slipbox.md` — the typed-atomic-note system class
  - `term_folgezettel.md` — alphanumeric trail mechanism

- **6 entry points** in `0_entry_points/`:
  - `entry_acronym_glossary.md` — master index of the 5 domain glossaries
  - `acronym_glossary_statistics.md` — 54 acronyms (causal inference, Bayesian, distributions)
  - `acronym_glossary_critical_thinking.md` — 31 acronyms (logic, fallacies, argumentation)
  - `acronym_glossary_cognitive_science.md` — 130 acronyms (biases, decision heuristics)
  - `acronym_glossary_network_science.md` — 48 acronyms (graph theory, centrality)
  - `acronym_glossary_llm.md` — 134 acronyms (LLM architectures, RAG, agents)

The per-vault master TOC (`entry_master_toc.md`) is still rendered inline by init so it reflects the vault's actual name. Its body now links the 6 pillar terms directly under a "Six Pillars" table, plus the master glossary index for acronym lookup.

#### `_SEED_VAULT_MANIFEST` — explicit, not rglob

The seed copy in `init.py` uses an explicit `_SEED_VAULT_MANIFEST` tuple of 14 relative paths. An earlier draft used `rglob("*.md")` over `seed_vault_dir()`, which works in wheel mode (data/seed_vault/ has only the shipped files) but blows up in editable mode (the fallback path is `vault/` itself, ~5000 files). The manifest pattern means wheel and editable installs produce identical vaults.

#### `pyproject.toml` force-include additions

14 new `force-include` entries graft the seed content from `vault/` into `src/tessellum/data/seed_vault/` at wheel build time. Single source of truth in the dogfooded vault; no two-copy drift.

#### Verification

Editable-mode and wheel-mode init both produce 32 markdown files (8 terms + 6 entry points + 1 master TOC + 17 templates + README) in ~30 ms. Both pass `tessellum format check` with 0 errors. Full suite: 468 passed, 1 skipped.

## [0.0.27] — 2026-05-10

### Added — `tessellum composer scaffold-sidecar`

A new subcommand that closes the gap between hand-authoring a skill canonical and getting Composer integration. Given an existing canonical with `<!-- :: section_id = X :: -->` anchors, it generates a starter `<skill>.pipeline.yaml` sidecar with one placeholder CORE step per anchor (chained linearly via `depends_on`).

```
$ tessellum composer scaffold-sidecar vault/resources/skills/skill_my_new_thing.md
scaffolded vault/resources/skills/skill_my_new_thing.pipeline.yaml
  4 step(s) from 4 section anchor(s):
    - step_1_load
    - step_2_classify
    - step_3_write
    - step_4_verify

  next: fill in materializer / expected_output_schema / prompt_template per step,
        then `tessellum composer validate skill_my_new_thing.md`
```

Flags: `--output / -o` to override the destination path, `--force` to overwrite, `--stdout` to print without writing. The previously documented authoring flow was "use `tessellum capture skill <slug>` to get a paired canonical + sidecar at creation time" — that's still right for new skills, but until v0.0.27, importing an existing canonical (e.g. when porting from another vault) required hand-authoring the sidecar. Now the scaffold does it in one command.

### Fixed — wheel ships `tessellum/data/__init__.py`

The previous `[tool.hatch.build.targets.sdist]` had an unanchored exclude pattern `"data"` that matched anywhere — including `src/tessellum/data/`. The wheel was missing `tessellum/data/__init__.py`, breaking `from tessellum.data import templates_dir` on a fresh install (caught when smoke-testing the v0.0.26 wheel in a clean venv). Anchored the patterns to top-level: `"/data"`, `"/experiments"`, `"/inbox"`, `"/runs"`, `"/tests"`, `"/notebook"`.

### Removed — 9 unused dependencies

Pruned the dependency list to match actual imports. Declared but never imported:

| Removed | Reason |
| ------- | ------ |
| `rank-bm25` | FTS5's built-in BM25 ranking is what we use |
| `tiktoken`, `numpy` | Not imported directly; transitively available via sentence-transformers if needed |
| `matplotlib`, `Pillow` | No plotting in Tessellum proper |
| `fa2`, `igraph` | No graph layout / community detection (could come back as `[viz]` extras when needed) |
| `click` | CLI uses argparse |
| `rich` | Output uses plain `print()` |

Install footprint drops substantially (matplotlib + Pillow + igraph + fa2 are heavy). Users get `sqlite-vec`, `sentence-transformers`, `networkx`, `PyYAML`, `jsonschema`, `pydantic` — the actual runtime dependency set.

## [0.0.26] — 2026-05-10

### Added — Two ported capture skills (closes `plan_code_artifacts_port`)

Phase 3 (final) of the code-artifact port. Two production-grade capture skill canonicals + Composer pipeline sidecars ported from AbuseSlipBox and adapted to Tessellum's runtime.

```
vault/resources/skills/
├── skill_tessellum_capture_code_repo_note.md          # 9-step procedure
├── skill_tessellum_capture_code_repo_note.pipeline.yaml
├── skill_tessellum_capture_code_snippet.md            # 7-step procedure
└── skill_tessellum_capture_code_snippet.pipeline.yaml
```

#### `skill_tessellum_capture_code_repo_note` (9 steps)

Compiles to a 9-step DAG that orchestrates the production of a code-repo note set (one main note + N module sub-notes) from a public repo URL:

1. **step_1_check_for_existing_notes** (per_leaf, `no_op`) — duplicate check against the index
2. **step_2_read_repository_structure** (per_leaf, no materializer) — fetch tree + README + recent commits
3. **step_3_identify_modules_for_sub_notes** (per_leaf, batchable `no_op`) — choose which modules deserve sub-notes
4. **step_4_search_vault_for_context** (per_leaf, batchable `no_op`) — find related terms / FAQs / how-tos / teams to cross-reference
5. **step_5_write_main_note** (per_leaf, `body_markdown_frontmatter_to_file`) — produce the parent note
6. **step_6_write_sub_notes_with_full_references** (per_leaf, `edits_apply_xml_tags`) — produce N module sub-notes in one shot
7. **step_7_update_entry_point** (cross_leaf, `edits_apply_xml_tags`) — add the new repo to `entry_code_repos.md`
8. **step_8_add_inlinks_from_related_notes** (cross_leaf, `edits_apply_xml_tags`) — backlink from 10-20 related notes
9. **step_9_update_database** (INFRA) — `tessellum index build`

#### `skill_tessellum_capture_code_snippet` (7 steps)

Compiles to a 7-step DAG that orchestrates the production of a single code-snippet note with BB-typed format branching (concept → MathJax, procedure → Mermaid, model → architecture diagram):

1. **step_1_read_source_code** (per_leaf, no materializer) — fetch source + extract key symbols
2. **step_2_determine_building_block_type** (per_leaf, batchable `no_op`) — pick concept / procedure / model from the source
3. **step_3_check_for_duplicates** (per_leaf, batchable `no_op`) — index lookup
4. **step_4_search_vault_for_cross_references** (per_leaf, batchable `no_op`) — find related terms / repos / teams / projects
5. **step_5_write_snippet_note** (per_leaf, `body_markdown_frontmatter_to_file`) — produce the snippet using the `## Patterns` template (Index + dual-block per pattern)
6. **step_6_update_entry_point** (cross_leaf, `edits_apply_xml_tags`) — add to `entry_code_snippets.md`
7. **step_7_verify** (INFRA) — structural validation pass

#### Adaptations from AbuseSlipBox

Both skills were ported via systematic find-replace + manual editing:

- **Rename**: `slipbox-*` → `tessellum-*` across header, slugs, sidecar filename, and `pipeline_metadata:` references.
- **Source repo URLs**: `code.amazon.com/packages/.../trees/mainline` → `https://github.com/<owner>/<repo>` placeholder. `code.amazon.com/packages/.../blobs/mainline/--/<path>` → `https://github.com/<owner>/<repo>/blob/main/<path>`.
- **Internal URL scrubs**: `*.amazon.com` patterns replaced with placeholders or removed.
- **Script invocations**: `bash scripts/update_notes_database.sh` → `tessellum index build`; `python3 $SCRIPTS_DIR/bm25_search.py` → `tessellum search --bm25`.
- **Setup block**: replaced the AB-specific `SCRIPTS_DIR=./scripts; DB_PATH=...; VAULT_PATH=...` bootstrap with `VAULT_PATH="."   # run from your vault root`.
- **Ecosystem shims**: dropped `related_skill_headers:` YAML key (no `.claude/skills/` or `.kiro/skills/` thin headers in Tessellum). Replaced the "thin headers point here" paragraph with a direct-invocation note.
- **MCP dependencies**: stripped `mcp_dependencies:` blocks from sidecars. Tessellum's Composer Wave 4 ships an `AnthropicBackend` but no MCP dispatcher (deferred per `plan_composer_port.md`). The `builder-mcp` references that fetched from `code.amazon.com` are gone; the agent now does the fetching directly.
- **Schema rewrite**: AB used a non-standard `expected_output_schema` with `format: markdown_with_frontmatter`, `required_frontmatter_keys: [output_path]`. Tessellum's compiler expects JSON Schema with `required: [output_path]` — converted via regex. Same for `format: xml_tag_list` → `required: [edits]`.
- **Forbidden field**: dropped `note_second_category:` from frontmatter (Tessellum's validator says `tags[1]` is the canonical source of truth for the second category).
- **FZ trail references** (e.g., `(FZ 12a)`) — stripped from headers.
- **Reference-example paths**: AB-specific example notes (`repo_amazon_cursus.md`, `snippet_slipbox_resolve_ghost_term_matches.md`) → generic `<example>` placeholders.

#### Validation

- `tessellum composer validate`: both skills pass (`OK skill_tessellum_capture_code_repo_note.md (9 steps)`, `OK skill_tessellum_capture_code_snippet.md (7 steps)`).
- `tessellum composer compile`: both produce well-formed typed DAGs with all materializer contracts resolved and all dependencies topologically valid.
- `tessellum format check`: code_repo skill passes with 0 errors / 0 warnings; code_snippet skill passes with 0 errors / 1 warning (link to a `<example>` placeholder path in the body — expected).

Full suite: **468 passed, 1 skipped** (the optional Anthropic-SDK constructor test).

#### Closes the plan

`plans/plan_code_artifacts_port.md` is now complete across all three phases:

| Phase | Version | What landed |
| ----- | ------- | ----------- |
| 1     | v0.0.24 | `template_code_snippet.md` + `template_code_repo.md` + capture-flavor wiring (14 flavors total) |
| 2     | v0.0.25 | 5 universal acronym glossaries (397 acronyms) + master index |
| 3     | v0.0.26 | 2 capture skill canonicals + Composer sidecars |

All Amazon-internal references scrubbed across the three phases; the public vault reads clean.

## [0.0.25] — 2026-05-10

### Added — 5 universal acronym glossaries to the seed vault

Phase 2 of the code-artifact port (see `plans/plan_code_artifacts_port.md`). The seed vault now ships 5 acronym glossaries indexing **397 acronyms** across foundational technical domains, plus a master index that lets newcomers resolve unfamiliar jargon without leaving the vault.

```
vault/0_entry_points/
├── entry_acronym_glossary.md                  # master index of the 5
├── acronym_glossary_statistics.md             # 54 acronyms — causal inference, Bayesian, distributions
├── acronym_glossary_critical_thinking.md      # 31 acronyms — logic, fallacies, argumentation
├── acronym_glossary_cognitive_science.md      # 130 acronyms — biases, dual-process, decision heuristics
├── acronym_glossary_network_science.md        # 48 acronyms — graph theory, centrality, communities
└── acronym_glossary_llm.md                    # 134 acronyms — LLM architectures, RAG, agents, eval
```

#### Why these 5 (and not the original 16)

The source library (AbuseSlipBox) has 16 glossaries built around the parent project's domain: fraud / abuse / Amazon-internal tooling. Many sections in those glossaries reference internal-only systems (Cradle, Wasabi, Paragon, Triton, Brazil, Coral, Midway, etc.) or Amazon-domain examples (BRP, CUBES, DSI, Weblab, Guardian, GREENTea, etc.) that don't belong in a public OSS slipbox.

Per the plan's design principle ("the public vault must read clean — a first-time reader should not encounter internal jargon"), 11 glossaries were dropped entirely rather than partially scrubbed:

- **`tools`** — overwhelmingly Amazon-internal tool names.
- **`security`** — Amazon-internal security framework (AAA, ASR, Anvil, Shepherd).
- **`developer`** — Amazon-internal infrastructure (LDAP/POSIX groups, BuilderHub, AgentSpaces, Cloud Desktop, Bindle, Brazil).
- **`data_governance`** — Amazon-internal compliance frameworks (RED/Orange/Yellow taxonomy, CAZ, Shepherd).
- **`ml`** — too entwined with Amazon-internal ML projects (Pangaea, GRAIL, BEAD, Ship2Vec, AmazonBoost, COSA, TFCM, GUARDIAN, etc.). The universal ML concepts are still findable via published references; we don't need to gate access to "Transformer" or "GBDT" through a glossary.
- **`business`**, **`workflows`**, **`teams`**, **`systems`**, **`data_metrics`**, **`abuse_networks`** — all heavily Amazon-internal.

The 5 kept glossaries (statistics, critical thinking, cognitive science, network science, LLM) are dominated by published research concepts. Each was scrubbed of:

- Sections whose H3 title named an Amazon-internal tool or project codename.
- Sections whose body opened with an Amazon-domain example (BRP, fraud, abuse, enforcement).
- Inline mentions of `Amazon`, `BRP`, `CUBES`, `DSI`, `Weblab` (replaced with neutral phrasings or removed).
- Internal-host URLs (`*.amazon.com`, `*.corp.amazon.com`, `*.a2z.com`).
- `**Source**: Internal: ...` lines.
- "Back to Main Glossary" footer links pointing at non-existent index.
- YAML keyword entries naming internal tools.

After scrubbing, the 5 files have **0 word-boundary hits** for `Amazon`, `BRP`, `CUBES`, `DSI`, `Weblab`, `Cradle`, `Wasabi`.

#### `entry_acronym_glossary.md` — master index

The master index is the first place a newcomer should land. It explains the convention (one H3 per acronym, `**Full Name**` + `**Description**` + `**Documentation**` + `**Related**`), tells users how to look up a term, and points at the 5 per-domain files. Captured via the existing `acronym_glossary` flavor (no new capture flavor needed).

#### Validation

All 6 files pass `tessellum format check` with 0 errors. Warnings are expected (links to `term_*.md` notes that aren't in the Tessellum seed vault yet — users who add their own term notes will resolve them; the glossary entries still work as standalone records).

#### What's coming

- **v0.0.26 — Phase 3 of `plan_code_artifacts_port.md`**: port two capture skills (`skill_tessellum_capture_code_repo_note` + `skill_tessellum_capture_code_snippet`) from AbuseSlipBox with sidecars, validated via `tessellum composer validate`.

## [0.0.24] — 2026-05-10

### Added — `code_snippet` + `code_repo` capture flavors

Phase 1 of the code-artifact port (see `plans/plan_code_artifacts_port.md`). Adds two new templates and wires them into the capture registry, taking the flavor count from 12 → 14.

```
$ tessellum capture code_snippet my_algo
created: ./resources/code_snippets/snippet_my_algo.md
  flavor:  code_snippet
  next:    fill placeholders, then `tessellum format check ./resources/code_snippets/snippet_my_algo.md`

$ tessellum capture code_repo my_repo
created: ./areas/code_repos/repo_my_repo.md
  flavor:  code_repo
  next:    fill placeholders, then `tessellum format check ./areas/code_repos/repo_my_repo.md`
```

#### `template_code_snippet.md`

Distills AbuseSlipBox's snippet shape (FZ 12a) into a Tessellum-clean placeholder template:

- YAML frontmatter with `building_block: procedure` (the most common; concept/model are alternatives via comment)
- BB-specific block between Purpose and Patterns: `## Procedure` (Mermaid flowchart) for procedures, `## Mathematical Definition` (MathJax) for concepts, `## Architecture / Model` (Mermaid flowchart or classDiagram) for models
- **`## Patterns` template with `### Index` table + `### Pattern N` sub-sections, each carrying both a verbatim `**In this script (Lxx-Lyy):**` block AND an `**Adapted to <new domain>:**` block** — the load-bearing innovation: the source proves provenance, the adaptation proves comprehension
- Code-block rules captured in the HOW-TO commentary: signatures + algorithm + branches + return shape stay verbatim; logging / argv / docstrings / paths may be elided
- `## Source` (file:line range) + `## References` (related snippet/repo/term links)

#### `template_code_repo.md`

Distills the repo-note shape (parent + sub-notes):

- YAML with `building_block: model` and `code_repo_url:` placeholder pointing at `https://example.com/owner/repo` (no Amazon-internal URLs)
- `## Overview` with attribute table (URL, language, license, owner, deps, install)
- Optional `## Architecture` (only for repos with 3+ subsystems worth diagramming)
- Optional `## Sub-Notes` (one row per module that has its own sub-note declaring `**Parent**: repo_<slug>.md`)
- `## Code Structure` tree
- `## References` with related terms / repos / snippets / external links

#### Capture registry

Two new entries in `src/tessellum/capture.py`:

```python
"code_snippet": TemplateSpec(
    flavor="code_snippet",
    template_filename="template_code_snippet.md",
    destination="resources/code_snippets",
    filename_prefix="snippet_",
    bb_type="procedure",
    second_category="code_snippets",
    description="Code snippet documenting one component or algorithm",
),
"code_repo": TemplateSpec(
    flavor="code_repo",
    template_filename="template_code_repo.md",
    destination="areas/code_repos",
    filename_prefix="repo_",
    bb_type="model",
    second_category="code_repos",
    description="Code repository documentation note",
),
```

`tessellum init` automatically scaffolds the destination dirs (driven by `REGISTRY.values()`), so a freshly-init'd vault works with the new flavors out of the box.

#### Tests

Existing `@pytest.mark.parametrize("flavor", sorted(REGISTRY))` smoke tests automatically extend to the new flavors. One assertion bumped from `len(flavors) == 12` → `14`. Full suite: 468 passed, 1 skipped.

#### What's coming

- v0.0.25 — Phase 2: 10 acronym glossaries dropped into `vault/0_entry_points/` with Amazon-internal references scrubbed.
- v0.0.26 — Phase 3: two capture skills (`skill_tessellum_capture_code_repo_note` + `skill_tessellum_capture_code_snippet`) ported from AbuseSlipBox with sidecars, `tessellum composer validate` as the gate.

## [0.0.23] — 2026-05-10

### Added — Composer Wave 5b: eval framework (closes the Composer port)

`tessellum composer eval <scenarios/>` runs YAML-defined scenarios against compiled skills, scoring each on two complementary dimensions:

1. **Structural assertions** (deterministic, no LLM): did the right number of steps fire, did the expected files land in the vault, do the LLM responses contain the substrings we're looking for?
2. **LLMJudge 5-dim rubric** (optional, content quality): relevance, completeness, accuracy, clarity, structural_integrity — each scored 1-5 by a separate LLM judge.

Together they catch the load-bearing wiring + the load-bearing content. Structural assertions tell you the pipeline ran; the rubric tells you whether what it produced is any good.

```
$ tessellum composer eval tests/scenarios/ --backend anthropic --judge-backend anthropic
eval: 12 passed, 1 failed, 0 errored (of 13 scenarios)
  PASS   skill_search_intent_extraction
  PASS   skill_capture_term_note__edge_case_long_title
  FAIL   skill_decompose__pathological_recursion
            ✗ step_count_eq(): expected 4, got 7
            • relevance: 4/5  Output addresses the prompt directly.
            • completeness: 3/5  Two of three required facets present.
            ...

Mean scores:
  relevance: 4.31
  completeness: 4.08
  accuracy: 4.42
  clarity: 4.15
  structural_integrity: 4.46
```

#### Scenario YAML format

```yaml
name: "Skill X handles edge-case Y"
skill: ../skills/skill_x.md
expected_output_description: "A summary note with three facets..."
leaves:
  - {id: "case_1", input: "..."}
vault: ../vault
assertions:
  - kind: no_errors
  - kind: step_count_eq
    expected: 3
  - kind: file_written
    target: notes/expected.md
  - kind: response_contains
    target: step_2
    expected: "facet_a"
rubric_dimensions: [relevance, clarity]   # optional; full set by default
```

Five assertion kinds: `no_errors`, `error_count_eq`, `step_count_eq`, `file_written`, `response_contains`. All deterministic — no LLM round-trip needed. Failed assertions surface with a clear `expected X, got Y` message.

#### `tessellum.composer.LLMJudge`

- Wraps any `LLMBackend` to produce `(JudgeScore × dimensions)` tuples.
- Strict system prompt: integer 1-5 per dim, JSON return only.
- **Tolerant parsing**: strict JSON first, then regex-extracts the first `{…}` block from prose-wrapped responses. Unparseable responses → score 0 with `justification="judge response unparseable"` (eval continues; the bad scenario is visible in the report).
- Out-of-range scores are clamped to `[0, 5]`.
- Missing dimensions in the response → score 0 with `justification="missing dimension X"`.

#### `tessellum.composer.run_eval`

```python
from tessellum.composer import (
    load_scenarios, run_eval, LLMJudge, MockBackend, AnthropicBackend
)

scenarios = load_scenarios(Path("tests/scenarios/"))
result = run_eval(
    scenarios,
    backend=AnthropicBackend(model="claude-sonnet-4-6"),
    judge=LLMJudge(AnthropicBackend(model="claude-opus-4-7")),
)
print(result.passed_count, result.failed_count)
print(result.mean_score_by_dim)
```

The judge backend is **independent** of the pipeline backend — typical pattern is a faster model running the pipeline and a stronger model grading it.

#### `tessellum composer eval` CLI

```
tessellum composer eval <scenarios_dir>
    [--backend mock|anthropic]                 # pipeline backend
    [--judge-backend none|mock|anthropic]      # rubric backend
    [--mock-responses mock.json]
    [--judge-mock-responses judge_mock.json]
    [--model claude-sonnet-4-6]
    [--dry-run]
    [--format human|json]
```

Default `--judge-backend=mock` returns canned 4/5 scores (lets you verify the rubric pipeline runs end-to-end without burning tokens). `--judge-backend=none` skips the rubric entirely (structural assertions only).

#### Tests

28 new tests: 18 library smokes (scenario YAML loading happy/error paths, default vs custom rubric dimensions, all 5 assertion kinds, LLMJudge full rubric / clamping / unparseable / missing dim / prose-wrapped JSON, end-to-end run_eval with judge aggregating mean scores, compile-failure → error_count, no-judge skip rubric) + 10 CLI smokes (human + JSON output, default mock judge, failing scenario → exit 1, missing dir → 2, empty dir → 0, invalid scenario YAML → 2).

Full suite: 464 passed, 1 skipped.

#### What's done

The Composer port from AbuseSlipBox is now feature-complete for Tessellum v0.1. Six waves shipped across v0.0.9 → v0.0.23:

| Wave | What            | Module                                    |
| ---- | --------------- | ----------------------------------------- |
| 1    | Foundation      | `loader.py`, `contracts.py`, `skill_extractor.py` |
| 2    | Compiler        | `compiler.py`                             |
| 3    | Executor        | `executor.py`, `scheduler.py`, `materializer.py`, `llm.py` (mock) |
| 4    | LLM bridge      | `llm.py` (Anthropic)                      |
| 5a   | Batch runner    | `batch.py`                                |
| 5b   | Eval framework  | `eval.py`                                 |

The agent ↔ program boundary holds end-to-end: programs handle structure (DAG, schema validation, materializer dispatch, file I/O, batch resume, assertion checks, judge response parsing); agents handle content (every LLM-mediated decision lives behind one Protocol method, swappable from MockBackend → AnthropicBackend → future OpenAI/local backends without touching the runtime).

#### Deferred (not in v0.1)

- **Bootstrapped confidence intervals** on judge scores — v0.2+ if needed.
- **Multi-judge ensembles** — v0.2+ if needed; the architecture (separate pipeline + judge backends) supports it without runtime changes.
- **Pairwise / preference judging** — v0.2+ if needed; the 5-dim rubric is what users want first.
- **MCP dispatcher** — kept on the deferred list per `plan_composer_port.md`. Add later when a Tessellum user has a concrete MCP integration need.
- **OpenAI / local-model backends** — same Protocol, separate `[agent_openai]` / `[agent_local]` extras when users ask. The lazy-import pattern in `AnthropicBackend` is the template.

## [0.0.22] — 2026-05-10

### Added — Composer Wave 5a: parallel batch runner with resume

`tessellum composer batch <jobs.json>` runs many `(skill, leaves)` jobs through `run_pipeline` in parallel. Drops the wall-clock cost of bulk operations from O(jobs) to O(jobs / parallelism) — essential for the eval framework (Wave 5b) and for any vault-wide bulk regeneration (e.g., refreshing trail summaries or re-scoring an entire corpus after a skill rev).

```
$ tessellum composer batch eval-jobs.json --parallelism 8
batch: 47 completed, 3 skipped, 0 failed.
  COMPLETED  skill_a__leaf_001  (3 step(s); 0 error(s); 1240ms)
  COMPLETED  skill_a__leaf_002  (3 step(s); 0 error(s); 1180ms)
  ...
```

#### `tessellum.composer.run_batch`

- **`BatchJob`** — frozen dataclass (`job_id`, `skill_path`, `leaves`, `vault_root`, `runs_dir`). `job_id` is the resume key.
- **`ThreadPoolExecutor`** — LLM calls are I/O-bound; ~95% of wall time is waiting on the network. Threads (not processes) are the right tool. Default parallelism: `4` (saturates typical API rate limits without overwhelming them).
- **Sequential fallback** — `parallelism=1` skips the executor entirely. Easier to debug; identical observable result.
- **Failure isolation** — exceptions inside any job (compile failure, executor error, malformed materializer response) become `BatchJobResult(status="failed", error=…)` rather than killing the batch. The runner reports `completed`/`skipped`/`failed` counts at the end.
- **Result file** — each completed job writes `<runs_dir>/<job_id>.result.json` with the full step-result summary. The Wave 3 trace lands at `<runs_dir>/<timestamp>_<skill>.json` as before.

#### Resume semantics

- Default: if `<runs_dir>/<job_id>.result.json` exists, the job is `"skipped"` and the prior payload is loaded back into `BatchJobResult.previous_payload`. **No backend dispatch happens** — restarts after a crash recover all completed work and don't pay tokens twice for it.
- `--no-resume` / `resume=False` — re-runs everything, overwriting result files.
- Corrupt result file (unparseable JSON or unreadable) → `status="failed"` with a clear message, NOT silently re-run. Avoids wedging the cache.

#### `tessellum composer batch` CLI

```
tessellum composer batch <jobs.json>
    [--parallelism 4]                  # max concurrent jobs
    [--no-resume]                      # force re-run of cached jobs
    [--dry-run]                        # skip filesystem writes
    [--mock-responses mock.json]
    [--backend mock|anthropic]
    [--model claude-sonnet-4-6]
    [--format human|json]
```

`jobs.json` schema: a JSON list of `{job_id, skill, leaves?, vault?, runs_dir?}`. Per-job validation surfaces with exit code `2`. Exit `0` if all jobs `completed` or `skipped`; exit `1` if any failed.

#### Tests

19 new tests: 9 library smokes (sequential + parallel paths, resume hit/miss, force re-run, compile-failure capture, dry-run pass-through, empty-jobs, corrupt-cache marked failed, result-file format) + 10 CLI smokes (human + JSON output, resume + `--no-resume`, missing/invalid jobs file, missing job_id field, compile-failure exit-1, empty jobs list).

Full suite: 436 passed, 1 skipped.

#### Deferred (per `plans/plan_composer_port.md`)

- **Token-budget pacing** — the parent project's `BatchPolicy` includes a tokens-per-minute throttle. Skipped for v0.1; the Anthropic SDK already retries on rate-limit responses, and the eval framework can layer pacing in Wave 5b if real workloads need it.
- **Cross-job upstream dependencies** — each job is independent here. A skill's internal pipeline still has dependencies (Wave 3); we just don't chain across jobs at the batch layer.
- **Streaming progress callbacks** — the runner returns once everything finishes. Wave 5b's eval framework adds in-flight progress reporting if needed.

## [0.0.21] — 2026-05-10

### Added — Composer Wave 4: Anthropic LLM bridge

`AnthropicBackend` extends Wave 3's `LLMBackend` Protocol with a real Claude implementation. Behind the `[agent]` extras dependency group — install once, set `ANTHROPIC_API_KEY`, and Composer pipelines dispatch through any Claude model (Sonnet 4.6 by default). MockBackend remains the default for tests + offline development.

```
$ pip install tessellum[agent]
$ export ANTHROPIC_API_KEY=sk-ant-...
$ tessellum composer run vault/resources/skills/skill_tessellum_search_notes.md \
    --backend=anthropic --model=claude-opus-4-7 \
    --leaves leaves.json --vault vault/
```

#### `tessellum.composer.AnthropicBackend`

- **Lazy import** — the `anthropic` package import happens inside `__init__`, so importing `tessellum.composer.llm` doesn't require `[agent]`. Users who only need MockBackend never pay the dependency cost.
- **Default model**: `claude-sonnet-4-6` — fast + capable, the right default for most Composer workloads. Pass `model="claude-opus-4-7"` when reasoning depth matters or `model="claude-haiku-4-5-20251001"` for cost-sensitive batch jobs.
- **API key resolution**: `ANTHROPIC_API_KEY` env var by default; explicit override via `api_key=` constructor arg.
- **Test injection**: `AnthropicBackend(client=fake_client)` lets tests substitute any object with a `messages.create(**kwargs)` method — no SDK install required for the tests, no real network calls.
- **Response handling**: extracts text from the SDK's content-block list (skipping non-text blocks like tool_use), records `model`, `stop_reason`, `input_tokens`, `output_tokens` in `LLMResponse.metadata` for the run trace.

#### `tessellum composer run --backend`

```
tessellum composer run <skill>
    [--backend mock|anthropic]    # default: mock
    [--model claude-sonnet-4-6]   # only used when --backend=anthropic
    ... (existing Wave 3 flags)
```

`--backend=anthropic` without `[agent]` installed returns exit code `2` with a clear hint:

```
tessellum composer run: --backend=anthropic requires the [agent] extras: pip install tessellum[agent]
```

`--mock-responses` is silently ignored (with a stderr note) when `--backend=anthropic` — the responses come from Claude, not a fixture.

#### Tests

11 new smoke tests covering: backend ID + default model + custom model, request payload mapping, multi-block text concatenation, non-text block skipping, dict-shaped block support, token-count metadata, real-SDK construction (skipped when `anthropic` not installed), CLI `--backend=anthropic` happy path + missing-SDK exit-2 path. Full suite: 427 passed, 1 skipped (12 of 23 conditional on SDK availability).

#### Why this matters

Composer end-to-end is real now. The same skill canonical that compiles to a typed DAG (Wave 2), executes through MockBackend in tests (Wave 3), can swap to a live Claude call by flipping one CLI flag. The agent ↔ program boundary holds: programs handle structure (DAG, schema validation, materializer dispatch, file I/O); agents handle content (every LLM-mediated decision lives behind one Protocol method). Wave 5+ (batch + eval) builds on this foundation without disturbing the runtime.

#### Deferred (per `plans/plan_composer_port.md`)

- **MCP dispatcher** — kept on the deferred list per the plan's "DEFER unless real demand" guidance. Tessellum v0.1 doesn't need to match the parent project's full MCP architecture; add later when a Tessellum user has a concrete MCP integration need.
- **OpenAI / local-model backends** — same Protocol, separate `[agent_openai]` / `[agent_local]` extras when users ask. The lazy-import pattern in `AnthropicBackend` is the template.

## [0.0.20] — 2026-05-10

### Added — Composer Wave 3: executor + scheduler + materializers + mock LLM

`tessellum composer run <skill>` executes a compiled pipeline end-to-end against a list of leaves. Wave 3 turns the static DAG produced by Wave 2's compiler into a running orchestrator. Five new modules (`llm.py`, `materializer.py`, `executor.py`, `scheduler.py`, plus the `run` CLI subcommand) — together ~700 LOC of typed, side-effect-aware runtime.

```
$ tessellum composer run vault/resources/skills/skill_tessellum_search_notes.md \
    --vault vault/ --mock-responses tests/fixtures/mock-responses.json
ran skill_tessellum_search_notes  (3 step invocation(s); 0 error(s); 4.2ms)
  OK  step_1_parse_intent  [corpus]  1.1ms
  OK  step_2_dispatch  [corpus]  1.4ms
  OK  step_3_return_hits  [corpus]  1.7ms

trace: runs/composer/2026-05-10T20-32-19_skill_tessellum_search_notes.json
```

#### `tessellum.composer.llm` — backend abstraction

`LLMBackend` Protocol with one method (`call(LLMRequest) → LLMResponse`). Wave 3 ships `MockBackend` — substring-pattern → canned-response map, with all requests recorded on `backend.calls` for test assertions. The real `AnthropicBackend` ships in Wave 4 behind the `[agent]` extras dependency group, sharing the same Protocol.

#### `tessellum.composer.materializer` — five wire-format handlers

One handler per `MaterializerContract` registered in `MATERIALIZER_CONTRACTS`:

| Key                                  | Mode      | Wire format               |
| ------------------------------------ | --------- | ------------------------- |
| `no_op`                              | DESCRIBE  | JSON (tolerant)           |
| `body_markdown_to_file`              | PRODUCE   | JSON envelope             |
| `body_markdown_frontmatter_to_file`  | PRODUCE   | markdown w/ frontmatter   |
| `edits_apply_to_files`               | APPLY     | JSON `{edits: [...]}`     |
| `edits_apply_xml_tags`               | APPLY     | `<edit><file>…</file>…`   |

Each returns a `MaterializedOutput(structured, files_written, files_applied, notes)`. All support `dry_run=True` (structured payloads still flow downstream so `{{upstream.X}}` resolves correctly during a dry run). `MaterializerError` surfaces malformed wire-format, missing required fields, or unknown keys; the executor catches it and writes the message to `StepResult.error` rather than propagating — one bad step doesn't kill the pipeline.

#### `tessellum.composer.executor` — single-step unit operation

`execute_step(step, leaf=…, upstream=…, backend=…, vault_root=…, dry_run=…)` resolves placeholders, invokes the backend, validates the response, and materializes.

- **`{{leaf.X}}`** — looked up in the per-leaf data dict.
- **`{{upstream.Y}}`** — looked up in the running upstream context (Wave 3 minimum).
- **`{{existing.Z}}`** — APPLY-mode pre-fetch deferred; the materializer enforces APPLY file existence at write time instead.

Missing keys leave `<missing leaf.X>` / `<missing upstream.Y>` sentinels (easier to debug than a silently-empty prompt). Schema validation runs against `expected_output_schema` via `jsonschema.validate`; failures populate `StepResult.error` without raising.

#### `tessellum.composer.scheduler` — end-to-end orchestration

`run_pipeline(pipeline, leaves=…, backend=…, vault_root=…, dry_run=…, runs_dir=…)` topologically iterates the compiler's already-sorted steps:

- **`per_leaf`**: one invocation per leaf; outputs collected into `upstream[output_key]` as a list of structured dicts.
- **`corpus_wide` / `cross_leaf`**: one invocation; output stored as a single dict.
- **`INFRA`**: skipped (informational glue, no LLM dispatch).

Synthetic single leaf `{"_id": "corpus"}` is injected if `leaves=None or empty`. When `runs_dir` is set, writes a JSON trace to `runs_dir/<filesystem-safe-timestamp>_<skill>.json` carrying leaf count, step invocation count, error count, per-step `elapsed_ms`, and the files written/applied per invocation.

#### `tessellum composer run` CLI

```
tessellum composer run <skill>
    [--leaves leaves.json]            # JSON list of leaf dicts
    [--vault vault/]                  # default ./vault
    [--mock-responses mock.json]      # pattern → canned response
    [--dry-run]                       # skip filesystem writes
    [--no-trace]                      # skip runs/composer/ trace
    [--runs-dir runs/composer/]
    [--format human|json]
```

Exit codes: `0` clean run, `1` step errors or compile failure, `2` invocation error (missing skill, bad JSON in `--leaves` / `--mock-responses`, etc.). The `composer compile` semantics are preserved exactly.

#### Tests

41 new smoke tests across:

- `tests/smoke/test_composer_materializer.py` — 5 materializers × happy + error paths.
- `tests/smoke/test_composer_executor.py` — placeholder resolution, mock backend, schema validation, materializer dispatch.
- `tests/smoke/test_composer_scheduler.py` — per-leaf vs corpus-wide, INFRA skip, upstream flow, trace writing, dry-run, synthetic leaf injection.
- `tests/cli/test_composer_run_cli.py` — CLI integration (human + JSON output, `--mock-responses`, `--leaves`, `--dry-run`, error paths, `pipeline_metadata: none` short-circuit).

#### Deferred (per `plans/plan_composer_port.md`)

- **Cross-leaf scoping** — Wave 3 collapses into corpus_wide for now; a true cross-leaf scope (e.g., synthesizing across all leaves with shared context) lands when a skill needs it.
- **`{{existing.Z}}` pre-fetch** — APPLY-mode prompts can't see the current file content yet (the materializer just overwrites). Wave 5+ if real demand emerges.
- **Column-oriented batching** — group N `per_leaf` instances into one LLM call. Per FZ 5e1c3a1a5 evidence, ~4× cost reduction; defer until backend pricing motivates it.
- **MCP dispatcher** — kept on the deferred list per the plan.

#### Why this matters

Composer is now functionally complete on the mock-backend side: capture (skill canonical) + compile (typed DAG) + run (executor dispatching through MockBackend with file-side-effects). Wave 4 swaps the mock for an Anthropic backend behind one Protocol method; Wave 5+ adds batch + eval. The agent ↔ program boundary stays clean — programs handle structure/I/O/policy lookups (file I/O, schema parse, tree assembly, recursion plumbing); agents handle every decision that requires reading source content.

## [0.0.19] — 2026-05-10

### Added — Composer Wave 2: the compiler

`tessellum composer compile <skill>` builds a typed DAG from a skill+sidecar pair. **Zero LLM calls.** Per `plans/plan_composer_port.md` Wave 2 — the compiler is the next layer above Wave 1's loader/validator.

```
$ tessellum composer compile vault/resources/skills/skill_tessellum_search_notes.md
compiled skill_tessellum_search_notes
  pipeline_version: 1.0
  steps: 3

  1. step_1_parse_intent  [CORE/corpus_wide]  ⇒ no_op
  2. step_2_dispatch  [CORE/corpus_wide]  ⇒ no_op  ← step_1_parse_intent
  3. step_3_return_hits  [CORE/corpus_wide]  ⇒ no_op  ← step_2_dispatch
```

#### What the compiler does

The compiler is pure logic — five passes over a loaded `Pipeline`:

1. **Topological sort** by `depends_on` edges. The pipeline list is the canonical ordering; the compiler enforces no forward references (a step's `depends_on` must reference a step appearing earlier in the list).
2. **Cycle detection** via DFS on the dependency graph.
3. **Contract resolution**: every step's `materializer` key is looked up in `MATERIALIZER_CONTRACTS`. Unknown keys raise `ContractViolation(KIND_UNKNOWN_MATERIALIZER)`.
4. **Required-output-fields check**: for CORE/DEFERRED steps with a materializer that has `required_output_fields`, the step's `expected_output_schema.required` must include them. Drift raises `ContractViolation(KIND_MISSING_REQUIRED_OUTPUT_FIELD)`.
5. **Prompt-section extraction**: each step's section text is pulled from the canonical via `load_skill_section`. Missing sections raise `CompilerError`.

Output: `CompiledPipeline` (frozen dataclass) — list of `CompiledStep` in topological order, each carrying its resolved `MaterializerContract`, JSON Schema, prompt text, and `output_key`.

#### What the compiler doesn't do (Wave 3+ scope)

- **Plan-doc + leaves** — Wave 2 compiles a single skill into a "pipeline template"; Wave 3 will instantiate per-leaf step instances against concrete data.
- **APPLY-mode pre-fetching** — `applies_to_files` resolution requires indexer-query support; surfaces in Wave 3.
- **LLMBackendContract / MCPContract validation** — backends + MCPs ship with Wave 4.
- **Prompt-template `apply_mode` directive checks** — minor; defer.

#### `tessellum.composer.compile_skill`

```python
from tessellum.composer import compile_skill, to_dag_json

compiled = compile_skill("vault/resources/skills/skill_foo.md")
# CompiledPipeline(skill_path=..., skill_name='skill_foo',
#                  pipeline_version='1.0', steps=(...), compiled_at=...)

dag = to_dag_json(compiled, include_prompts=True)
# {"format_version": "1.0", "skill_name": "...", "step_count": ..., "steps": [...]}
```

`CompilerError` for DAG-level errors (cycles, forward refs, missing prompts). `ContractViolation` for contract drift (already raised by Wave 1's loader). `PipelineValidationError` from Wave 1a still applies upstream.

#### `tessellum composer compile` CLI

```bash
tessellum composer compile <skill>                    # human summary
tessellum composer compile <skill> --format json      # to stdout
tessellum composer compile <skill> -o pipeline_dag.json  # to file
tessellum composer compile <skill> -o dag.json --no-prompts  # compact
```

Exit codes:
- `0` — compiled clean (or `pipeline_metadata: none` → 0-step pipeline)
- `1` — compilation failure (validation, contract violation, or compiler error)
- `2` — invocation error (file missing, not markdown, etc.)

The `--no-prompts` flag swaps `prompt_section_text` for `prompt_section_text_chars` (just the length) — useful for indexing pipeline DAGs without bloating the JSON.

#### Tests

24 new tests, all passing. **364 total** (340 prior + 24 new).

- `tests/smoke/test_composer_compiler.py` (15 tests):
  - Returns typed `CompiledPipeline` / `CompiledStep`
  - Topological order preserved; depends_on points to earlier steps only
  - Materializer contracts resolved correctly
  - Prompt-section text extracted
  - Unknown materializer → ContractViolation
  - Missing required output field → ContractViolation(KIND_MISSING_REQUIRED_OUTPUT_FIELD)
  - Forward reference → CompilerError
  - Unknown depends_on target → CompilerError
  - `pipeline_metadata: none` → 0-step compilation
  - `to_dag_json` round-trip; `--no-prompts` mode
  - Real-skill compile: search-notes (3 steps) + answer-query (5 steps) both pass.
- `tests/cli/test_composer_compile_cli.py` (9 tests):
  - Human + JSON output; `-o` to file; `--no-prompts`; missing skill → 2; non-md → 2; validation failure → 1; `pipeline_metadata: none` → 0; real skill compiles via CLI.

#### CLI banner updated

```
tessellum composer validate <skill>  — validate a skill's pipeline sidecar
tessellum composer compile <skill>   — compile to a typed DAG (Wave 2)

Roadmap:
  tessellum composer run <skill>       — Composer Wave 3 (executor)
  tessellum composer + LLM bridge      — Composer Wave 4
```

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.19"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.19"`.
- 364/364 tests pass (340 prior + 24 new).

### What remains for v0.1

- **Composer Wave 3** — Executor + materializers (~1200 LOC). Resolves placeholders (`{{leaf.X}}`, `{{upstream.Y}}`, `{{existing.Z}}`), invokes the LLM (mock at first), checks responses against `expected_output_schema`, applies materializers (5 concrete: `body_markdown_to_file`, `body_markdown_frontmatter_to_file`, `edits_apply_to_files`, `edits_apply_xml_tags`, `no_op`).
- **Composer Wave 4** — LLM bridge (~300 LOC + extras). Anthropic SDK wrapper behind `[agent]` extras; optional MCP dispatcher behind `[mcp]`. Makes the answer-query and search-notes skills shipped in v0.0.18 actually executable end-to-end.

Composer Waves 5+ (multi-corpus batch + eval framework) are deferred to v0.2.

## [0.0.18] — 2026-05-10

### Added — Retrieval Wave 5: skill orchestration (v0.1 retrieval scope COMPLETE)

The last item in `plans/plan_retrieval_port.md`. Two skill canonicals + two pipeline sidecars + one router module close the v0.1 retrieval track:

```
vault/resources/skills/skill_tessellum_search_notes.md           ← decision-tree router
vault/resources/skills/skill_tessellum_search_notes.pipeline.yaml ← typed contract (3 steps)
vault/resources/skills/skill_tessellum_answer_query.md           ← 5-stage QA pipeline
vault/resources/skills/skill_tessellum_answer_query.pipeline.yaml ← typed contract (5 steps)
src/tessellum/retrieval/router.py                                ← classify_query + route
```

Three skills now validate via `tessellum composer validate`:

```
$ tessellum composer validate vault/resources/skills/
OK   skill_tessellum_answer_query.md (5 steps)
OK   skill_tessellum_format_check.md (pipeline_metadata: none)
OK   skill_tessellum_search_notes.md (3 steps)
```

#### `tessellum.retrieval.router`

```python
from tessellum.retrieval import classify_query, route

decision = classify_query("How does Composer compile?")
# RouterDecision(strategy="hybrid",
#                reason="multi-word / question-shaped: hybrid wins on ...")

decision, hits = route("data/tessellum.db", "composer", k=5)
# decision.strategy == "bm25" (single token)
# hits = list[BM25Hit]
```

Heuristic decision tree:

| Query shape | Strategy | Why |
|---|---|---|
| Vault `.md` path with `/` | `bfs` | Treat as seed for graph traversal |
| Single short token (≤30 chars, no spaces) | `bm25` | Lexical lookup beats fusion overhead |
| `?`-suffixed or ≥4 tokens | `hybrid` | Wave 3's +12pp winner on real questions |
| Empty or unrecognized | `hybrid` (fallback) | Default of last resort |

The router is **heuristic, not ML-routed** — cheap, transparent, deterministic. Override by calling the primitive directly when intent is mis-classified.

#### `skill_tessellum_search_notes.md`

3-step canonical encoding the decision tree as agent-readable procedure. Steps mirror `tessellum.retrieval.router`'s logic (`classify_query` → `route` → render). Sidecar declares CORE / no_op / corpus_wide step contracts.

#### `skill_tessellum_answer_query.md`

5-stage QA pipeline canonical:

1. **Query expansion** — acronym detection + synonym variants + term-promotion seeds
2. **Multi-strategy retrieval** — calls `skill_tessellum_search_notes` for each variant
3. **Working memory** — score by strategy presence × in-degree × recency × BB priority; truncate to top 20
4. **Context assembly** — token-budgeted (default 6K) hierarchical context: grounded terms + primary sources + supporting excerpts
5. **Synthesis with citations** — every load-bearing claim cites a note inline; "see also" footer

Sidecar declares 5 CORE steps with full `expected_output_schema` + `prompt_template` for each.

End-to-end execution requires **Composer Wave 4 (LLM bridge)** which ships later. Until then, this skill is documentation: a typed-contract spec any LLM agent can follow procedurally. The validator (`tessellum composer validate`) confirms the canonical's section_id anchors and the sidecar's step structure are well-formed.

#### Tests

8 new tests in `tests/smoke/test_retrieval_router.py`:
- empty/whitespace query → hybrid fallback with reason
- vault path → BFS
- single token → BM25
- short identifier → BM25
- question → hybrid
- multi-word → hybrid
- typed `RouterDecision` returned
- strategy is in the closed enum

**340 total tests passing** (332 prior + 8 new).

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.18"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.18"`.
- 340/340 tests pass.

### v0.1 retrieval scope — COMPLETE

| Wave | Component | Version |
|---|---|---|
| 1 | BM25 + FTS5 | v0.0.13 |
| 2 | Dense + sqlite-vec | v0.0.14 |
| 3 | Hybrid RRF (default) | v0.0.15 |
| 4 | Best-first BFS (no PPR) | v0.0.16 |
| 4.5 | Metadata filter (`tessellum filter`) | v0.0.17 |
| **5** | **Skill orchestration (router + 2 skills)** | **v0.0.18 ← this release** |

Five retrieval surfaces (BM25 / dense / hybrid / BFS / metadata) all live, all CLI-accessible, all wrapped in agent-facing skill canonicals.

### What remains for v0.1

The Composer track is the only major remaining v0.1 scope:

- **Composer Wave 2** — Compiler (~600 LOC, zero LLM calls). Builds the typed DAG from skill+sidecar pairs; validates contracts at compile time.
- **Composer Wave 3** — Executor (~1200 LOC). Resolves placeholders, dispatches LLM calls, applies materializers.
- **Composer Wave 4** — LLM bridge (~300 LOC + extras). Anthropic SDK wrapper + optional MCP dispatcher. **This is what makes the answer-query and search-notes skills actually executable.**

Composer Waves 5+ (multi-corpus batch + eval framework) are deferred to v0.2.

## [0.0.17] — 2026-05-10

### Added — `tessellum filter` — metadata search (Retrieval Wave 4.5)

The simplest retrieval surface — direct SQL filtering on the structured YAML fields. Reach for this when you know *what kind* of note you want, not *what content*. **Was missing from the 5-wave plan; called out by the user as a gap before Wave 5.**

```bash
tessellum filter --building-block concept --status active
tessellum filter --tag cqrs --date-after 2026-01-01
tessellum filter --building-block argument --topic "Knowledge Management"
tessellum filter --has-folgezettel       # all FZ-trail notes
tessellum filter --folgezettel-prefix 7  # all notes in trail 7
tessellum filter                          # list every note (up to --k)
```

#### Filter dimensions

12 orthogonal filters, all AND-combined:

| Field | Flag | Backed by |
|---|---|---|
| `building_block` (closed enum) | `--building-block` | exact match |
| `status` (closed enum) | `--status` | exact match |
| `tags[0]` / PARA bucket | `--category` | exact match |
| `tags[1]` / second category | `--second-category` | exact match |
| `tags[2..]` (open vocabulary) | `--tag` | `json_each` exact-value |
| `keywords[]` | `--keyword` | `json_each` exact-value |
| `topics[]` | `--topic` | `json_each` exact-value |
| `date of note` | `--date-after`, `--date-before` | string range (YYYY-MM-DD) |
| `folgezettel` prefix | `--folgezettel-prefix` | LIKE prefix |
| FZ membership | `--has-folgezettel` / `--no-folgezettel` | NULL check |

JSON-array fields (`tags`, `keywords`, `topics`) use SQLite's built-in `json_each` to avoid LIKE false-positives — `tag='cqrs'` will match `["cqrs"]` but never `["cqrsy"]`.

#### `tessellum.retrieval.metadata_search`

```python
from tessellum.retrieval import metadata_search, MetadataHit

hits = metadata_search(
    "data/tessellum.db",
    building_block="concept",
    status="active",
    tag="cqrs",
    date_after="2026-01-01",
    k=20,
)
```

Returns `MetadataHit` (slimmer than `NoteRow` — only the fields filters care about). Callers needing the full row can follow up with `Database.note_by_id(hit.note_id)`.

#### Schema fix — empty strings → NULL

While building the filter, surfaced a bug: templates author `folgezettel: ""` (empty string) as a placeholder. The old `_str_or_none` helper preserved empty strings, which made `folgezettel != NULL` and falsely matched `--has-folgezettel`. Fixed: `_str_or_none` now coerces empty strings AND the literal `"null"` to `None`. Applies to `status`, `language`, `building_block`, `folgezettel`, and `folgezettel_parent`. Re-run `tessellum index build --force` to apply.

End-to-end on the real Tessellum vault:
- Before fix: `--has-folgezettel` returned 5 hits (3 templates with empty FZ + 2 real)
- After fix: returns the 2 real FZ-trail notes only

#### CLI banner

The bare `tessellum` banner now shows 6 commands:

```
tessellum init <dir>                — scaffold a new vault
tessellum format check <path>       — validate notes against the YAML spec
tessellum capture <flavor> <slug>   — create a new note from a template
tessellum index build               — build the unified SQLite index
tessellum search <query>            — content retrieval (--bm25/--dense/--hybrid/--bfs)
tessellum filter --tag <t> [--bb …] — metadata filter (tags, BB, status, dates, ...)
tessellum composer validate <skill> — validate a skill's pipeline sidecar
```

#### Tests

34 new tests, all passing. **332 total** (298 prior + 34 new).

- `tests/smoke/test_retrieval_metadata.py` (22 tests):
  - typed return; no-filter → all notes; each filter dimension (BB, status, category, second-category, tag via json_each, keyword via json_each, topic via json_each, date_after / date_before / range, FZ prefix, has_folgezettel True/False); AND-combine; no-match → empty; k limit; k=0 → empty; missing DB; **empty-string folgezettel correctly treated as NULL**; integration test against real vault.
- `tests/cli/test_filter_cli.py` (12 tests):
  - filter by each major dimension; combined filters; no-match exit 0; no-filters lists all; --k limit; JSON output structure (filters echo + hits); missing DB → 2; --has-folgezettel / --no-folgezettel mutex; date range; banner mention.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.17"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.17"`.
- 332/332 tests pass (298 prior + 34 new).

### Composition with content search (future work)

For now, `tessellum filter` and `tessellum search` are separate subcommands. A future enhancement could let metadata filters compose as **post-filters** on content search results (e.g. `tessellum search "graph" --bm25 --building-block concept`). That's tracked as a Wave 5+ enhancement, not blocking.

### What's NEXT (Wave 5 — last v0.1 retrieval item)

- `vault/resources/skills/skill_tessellum_search_notes.md` — decision-tree router invoking the five retrieval surfaces (bm25, dense, hybrid, bfs, filter) by query intent.
- `vault/resources/skills/skill_tessellum_answer_query.md` — 5-stage QA pipeline: query expansion → multi-strategy retrieval → working memory scoring → context assembly → synthesis with citations.
- Optional small `tessellum.retrieval.router` Python module the search-notes skill calls into (~150 LOC).

## [0.0.16] — 2026-05-10

### Added — Retrieval Wave 4: Best-first BFS over `note_links`

`tessellum search --bfs <seed_note_id>` ships the fourth retrieval strategy. Per `plans/plan_retrieval_port.md` Wave 4. **No PPR** — FZ 5e2b1c established that PPR optimizes Hit@K (correlation with answer-quality only ρ=0.37) and is Pareto-dominated by best-first BFS in production.

```bash
$ tessellum search --bfs resources/term_dictionary/term_cqrs.md --k 5 --depth 2
BFS matches for 'resources/term_dictionary/term_cqrs.md'  (5 hits)

   1. thought_synthesis_two_systems_cqrs_value_proposition  (0.5000)
       [depth=1  path=term_cqrs.md → thought_synthesis_two_systems_cqrs_value_proposition.md]

   2. term_circle_of_influence  (0.5000)
       [depth=1  path=term_cqrs.md → term_circle_of_influence.md]

   3. term_dual_paradigm_framework  (0.5000)
       ...
```

#### `tessellum.retrieval.best_first_bfs`

```python
from tessellum.retrieval import best_first_bfs, GraphHit

hits = best_first_bfs(
    "data/tessellum.db",
    seed="resources/term_dictionary/term_cqrs.md",
    k=20,
    max_depth=3,
    hub_threshold=50,
)
# [GraphHit(note_id=..., note_name=..., score=0.5, depth=1, path=(seed, hit)), ...]
```

Four design points worth knowing:

1. **Undirected adjacency for traversal.** Note-link relationships flow conceptually both ways: if A links to B, B is also "near" A. We walk the undirected projection of the directed `note_links` graph. So BFS from B will reach A even though the edge is A→B.

2. **Directed in-degree as hub signal.** A note with many *inbound* links is a popular hub (`term_zettelkasten`, `term_cqrs`, etc.). Hub-skip prevents combinatorial blowup ("everything connects to everything via the most-linked note") by NOT expanding neighbors of nodes whose in-degree exceeds `hub_threshold` (default 50). Hub nodes still appear as hits — only their onward connections are suppressed.

3. **Priority queue keyed depth-major, hub-minor.** Closer-to-seed surfaces first; among ties, less-popular (= more-specific) notes are preferred. This produces focused, contextually-relevant traversal.

4. **Score is `1 / (1 + depth)`.** Depth 1 → 0.5; depth 2 → 0.333; depth 3 → 0.25. Higher = closer to seed. Hub-skip affects priority-queue ordering only; the displayed score stays interpretable.

`GraphHit` carries diagnostic `depth` and `path` fields. Path is a tuple of note_ids from seed to hit (inclusive of both endpoints). `len(path) == depth + 1`.

#### CLI `--bfs` flag

```bash
tessellum search <query>                               # hybrid (default)
tessellum search --bm25 <query>                        # lexical
tessellum search --dense <query>                       # semantic
tessellum search --bfs <seed_note_id>                  # graph traversal
tessellum search --bfs <seed> --depth 2 --k 10         # tune traversal
tessellum search --bfs <seed> --hub-threshold 100      # less aggressive hub-skip
```

The `query` positional is interpreted as a vault-relative `note_id` when `--bfs` is set (e.g. `resources/term_dictionary/term_cqrs.md`). All four strategy flags are in one `argparse` mutex group.

JSON output includes `depth` and `path` per hit:

```json
{
  "strategy": "bfs",
  "hits": [
    {
      "note_id": "...",
      "note_name": "term_epistemic_function",
      "score": 0.5,
      "depth": 1,
      "path": [
        "resources/term_dictionary/term_zettelkasten.md",
        "resources/term_dictionary/term_epistemic_function.md"
      ]
    }
  ]
}
```

#### Tests

19 new tests, all passing. **298 total** (279 prior + 19 new).

- `tests/smoke/test_retrieval_graph.py` (16 tests):
  - typed return; seed excluded from results; depth-1 neighbors correct; `max_depth` limits traversal; depth-2 reachable when allowed; islands skipped; **score formula verified** (`1 / (1 + depth)`); path is `(seed, ..., hit)`; `k` limits; `k=0` and `max_depth=0` → empty; unknown seed → empty; missing DB → FileNotFoundError; **undirected traversal verified** (BFS from a target reaches its source via the inbound edge); **hub-skip verified** (popular hub appears as hit, but its grandchildren don't); integration test against real vault.
- `tests/cli/test_search_cli.py` (3 new):
  - `--bfs` flag → "BFS matches" output
  - Unknown seed → exit 0 with "no matches"
  - `--bfs --format json` exposes `depth` + `path` fields
  - All 4 strategy flags mutually exclusive (verified for `--bm25 --bfs` and `--hybrid --bfs` as well as previous combos).

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.16"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.16"`.
- 298/298 tests pass (279 prior + 19 new).

### What's NOT in this release (Wave 5)

- **Wave 5 (v0.0.17)** — Skill orchestration: `skill_tessellum_search_notes` (8-strategy decision-tree router invoking the 4 retrieval primitives) + `skill_tessellum_answer_query` (5-stage QA pipeline). The first user-facing answer-the-question capability. Closes the v0.1 retrieval scope.

### Why no PPR?

Per `plans/plan_retrieval_port.md` § Three lessons:

> Per FZ 5e2b1c — the **Hit@K-to-answer-quality disconnect** (correlation ρ=0.37). Hit@5 measures whether the right note is in the top-5; answer quality measures whether the LLM's response is actually good. PPR optimizes Hit@K through expensive multi-hop walks (αat 0.85, ~250ms per query). Best-first BFS is simpler (single hop, priority-queue frontier), faster (~30ms), and yields equivalent or better answer quality on real queries. PPR's "lift" is largely benchmark theater; BFS is Pareto-optimal in production.

Best-first BFS is the production graph strategy. Users who want PPR can add it as a custom retrieval module — `tessellum.retrieval.best_first_bfs` is a function call, easy to compose with alternative implementations.

## [0.0.15] — 2026-05-10

### Added — Retrieval Wave 3: Hybrid RRF (now the default)

`tessellum search <query>` flips its default from BM25 (Wave 1) to **hybrid** (BM25 + dense fused via Reciprocal Rank Fusion). Per `plans/plan_retrieval_port.md` Wave 3 — the parent project's experiments measured **+12 percentage points Hit@5 lift** over the best single strategy on real queries (FZ 5e1c3a1a1). The lift comes from BM25 and dense retrieving *different* documents; hybrid surfaces the union.

```bash
$ tessellum search "knowledge graph" --k 5
HYBRID matches for 'knowledge graph'  (5 hits)

   1. term_dialectic_knowledge_system  (0.0318)
       resources/term_dictionary/term_dialectic_knowledge_system.md
       [bm25=#4 dense=#2]               ← agrees both rankers

   2. term_zettelkasten  (0.0318)
       resources/term_dictionary/term_zettelkasten.md
       [bm25=#2 dense=#4]               ← agrees both rankers

   3. term_epistemic_function  (0.0308)
       [bm25=#5 dense=#5]

   4. thought_building_block_ontology_relationships  (0.0305)
       [bm25=#11 dense=#1]              ← semantic-only outlier (BM25 missed it)

   5. thought_synthesis_two_systems_cqrs_value_proposition  (0.0303)
       [bm25=#6 dense=#6]
```

Notice how hit #4 — `thought_building_block_ontology_relationships` — was rank 11 in BM25 (would never have surfaced in BM25's top-10) but rank 1 in dense. Hybrid retrieves it because semantic relevance compensates for poor lexical overlap. This is the +12pp lift in action.

#### Reciprocal Rank Fusion formula

Per Cormack, Clarke, Buettcher (2009):

```
RRF_score(d) = Σ over rankers r: 1 / (k1 + rank_r(d))
```

Where ``k1`` is a smoothing constant (60 default; smaller amplifies top ranks, larger flattens) and ``rank_r(d)`` is the 1-indexed rank of document ``d`` in ranker ``r``'s top-K. Documents absent from a ranker contribute 0 from that ranker.

#### `tessellum.retrieval.hybrid_search`

```python
from tessellum.retrieval import hybrid_search, HybridHit

hits = hybrid_search("data/tessellum.db", "knowledge graph", k=5)
# [HybridHit(note_id=..., note_name=..., score=0.0318,
#            bm25_rank=4, dense_rank=2), ...]
```

`HybridHit` carries diagnostic per-ranker ranks:
- `bm25_rank: int | None` — 1-indexed rank in BM25's top-K, or `None` if not in BM25 results.
- `dense_rank: int | None` — 1-indexed rank in dense's top-K, or `None` if not in dense results.

These let users see *why* each note was retrieved. A note ranked 2 in BM25 and 5 in dense is a "both-rankers agree" hit (high RRF). A note ranked 1 in dense but absent from BM25 is a "semantic-only" hit (lower RRF, but possibly interesting per the example above).

Implementation: `hybrid_search` runs `bm25_search` and `dense_search` in sequence, then fuses in Python. A single-SQL fusion (UNION ALL of both top-K, GROUP BY note_id, SUM of reciprocal ranks) would shave a millisecond on hot DBs but loses readability. Revisit if profiling shows the dual roundtrip is material — for v0.0.15 we optimize for clarity.

`per_strategy_k` parameter controls how many candidates each ranker contributes before fusion. Default `max(2*k, 20)` — wider fetch gives richer fusion at minor latency cost. Set explicitly for ablation.

If the index was built with `--no-dense`, `hybrid_search` falls back to BM25-only fusion (dense ranks all `None`). Better than failing the query.

#### CLI default flipped

```bash
tessellum search <query>           # Hybrid (NEW DEFAULT)
tessellum search --hybrid <query>  # Explicit hybrid
tessellum search --bm25 <query>    # Lexical only
tessellum search --dense <query>   # Semantic only
```

All three strategy flags are in one `argparse` mutex group — passing two raises an invocation error.

JSON output for hybrid includes `bm25_rank` and `dense_rank` fields per hit.

The bare `tessellum` banner now lists hybrid as the default search behavior:

```
tessellum search <query>            — hybrid retrieval (BM25 + dense via RRF)
```

#### Tests

14 new tests, all passing. **279 total** (265 prior + 14 new).

- `tests/smoke/test_retrieval_hybrid.py` (12 tests):
  - typed return; in-both-rankers ≥ in-one-ranker score; **RRF formula verified** (`score == sum(1/(k1+rank)) over rankers`); descending scores; `k` limits; `k=0` → empty; bm25_rank present when in BM25; dense_rank present when in dense; `--no-dense` build → BM25-only fallback; missing DB → FileNotFoundError; `per_strategy_k` widens fetch; **integration test against real vault verifies both rankers contribute hits**.
- `tests/cli/test_search_cli.py` (2 new):
  - `--hybrid` explicit flag → "HYBRID matches" output
  - All three strategy flags mutually exclusive (`--bm25 --dense`, `--bm25 --hybrid`, `--dense --hybrid` all raise SystemExit).
  - Hybrid JSON output includes `bm25_rank` + `dense_rank` diagnostic fields.

Three pre-existing CLI tests updated to reflect the default flip (`test_search_no_match_returns_0`, `test_search_bm25_json_output_structure` (renamed from `_json_output_structure`), `test_search_no_snippet_flag_omits_snippet`) — they now pass `--bm25` explicitly since the test is BM25-specific.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.15"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.15"`.
- 279/279 tests pass (265 prior + 14 new).

### What's NOT in this release (Waves 4-5)

- **Wave 4 (v0.0.16)** — Best-first BFS graph traversal. **No PPR** per FZ 5e2b1c (Hit@K↔answer-quality disconnect, ρ=0.37 — best-first BFS is Pareto-optimal in production).
- **Wave 5 (v0.0.17)** — Skill orchestration: `skill_tessellum_search_notes` (8-strategy decision-tree router) + `skill_tessellum_answer_query` (5-stage QA pipeline).

## [0.0.14] — 2026-05-10

### Added — Retrieval Wave 2: Dense + sqlite-vec

`tessellum search --dense <query>` ships. Per `plans/plan_retrieval_port.md` Wave 2. Both lexical (BM25) and semantic (dense) retrieval are now available; Wave 3 (v0.0.15) will combine them via Reciprocal Rank Fusion as the production default.

```bash
tessellum search "knowledge graph" --bm25
# BM25 matches by lexical overlap — finds "knowledge" + "graph" tokens.

tessellum search "knowledge graph" --dense
# DENSE matches by semantic similarity — finds notes about knowledge
# organization, building-block ontologies, dialectic systems.
```

The two strategies retrieve different ranked sets — exactly the diversity that hybrid RRF in Wave 3 will exploit (parent project: +12pp Hit@5 lift over best single strategy, per FZ 5e1c3a1a1).

#### Schema extension — `notes_vec` virtual table + `note_int_id`

`src/tessellum/indexer/schema.sql`:

```sql
-- notes table gains a surrogate key for the join:
note_int_id INTEGER UNIQUE
CREATE INDEX idx_notes_int_id ON notes(note_int_id);

-- New virtual table:
CREATE VIRTUAL TABLE notes_vec USING vec0(
    note_int_id INTEGER PRIMARY KEY,
    embedding   FLOAT[384] distance_metric=cosine
);
```

**`distance_metric=cosine`** is critical. sqlite-vec defaults to L2 (Euclidean), which gives correct ranking for normalized embeddings but yields scores in `[0, 2]` that don't map cleanly to "1 = identical, 0 = orthogonal". Cosine distance gives `[0, 2]` too but for normalized vectors `score = 1 - distance` IS exactly cosine similarity ∈ `[-1, 1]`. Users see meaningful scores like `0.487` (moderate semantic match) instead of `-0.013` (which was actually `1 - L2_distance` for distance ≈ 1).

**Schema migration**: existing v0.0.13 DBs lack `notes_vec` and the `note_int_id` column. Users re-run `tessellum index build --force` to rebuild.

#### Build pipeline — embedding generation

`src/tessellum/indexer/build.py`:

- Allocates sequential `note_int_id` (1, 2, 3, ...) per note as the join key for `notes_vec`.
- Lazy-loads `sentence-transformers/all-MiniLM-L6-v2` via a module-level singleton — `~1.5s` first-call cost; in-process re-builds are fast.
- Encodes each note's text (`note_name + keywords + topics + tags + body`, joined by `\n`) with `normalize_embeddings=True` so cosine distance behaves predictably.
- Writes embeddings to `notes_vec` as packed little-endian float32 blobs.
- New `with_dense: bool = True` parameter on `build()`. Pass `False` to skip embedding generation entirely (faster builds when only BM25 is needed).
- New `--no-dense` CLI flag on `tessellum index build`.
- `BuildResult.embeddings_generated` reports the count.

End-to-end on the real Tessellum vault: 5.8s build (71 notes, 71 embeddings, 547 links) on a warm sentence-transformers cache; ~20s on a cold cache.

#### `tessellum.retrieval.dense_search`

`src/tessellum/retrieval/dense.py`:

```python
from tessellum.retrieval import dense_search, DenseHit

hits = dense_search("data/tessellum.db", "knowledge graph", k=5)
# [DenseHit(note_id=..., note_name=..., distance=0.513, score=0.487), ...]
```

`DenseHit` has both `score` (cosine similarity, `1 - distance`, "higher = more similar") and `distance` (raw cosine distance, "lower = closer"). Both fields are useful: `score` mirrors `BM25Hit.score`'s convention; `distance` is what the SQL actually returns.

Lazy-loads the encoder via the same module-level singleton pattern as `build`. First query in a process loads the model; subsequent queries are fast.

#### `tessellum search` CLI gains `--dense`

```bash
tessellum search <query>           # BM25 (Wave 1 default; Wave 3 flips to hybrid)
tessellum search --bm25 <query>    # explicit BM25
tessellum search --dense <query>   # dense semantic
```

`--bm25` and `--dense` are mutually exclusive (argparse `add_mutually_exclusive_group`). JSON output for dense includes both `score` and `distance` fields.

#### Tests

17 new tests, all passing. **265 total** (248 prior + 17 new).

- `tests/smoke/test_retrieval_dense.py` (14 tests): typed return, semantic ranking (graph query → graph note ranks higher than cooking note; cooking query inverts), score in `[-1, 1]`, distance in `[0, 2]`, scores descend / distance ascends, `k` flag, `k=0` → empty, missing DB → FileNotFoundError, `--no-dense` build → empty dense results (not error), `with_dense=True/False` toggles correctly, integration test against real vault.
- `tests/cli/test_search_cli.py` (3 new): `--dense` flag uses dense strategy + DENSE-labeled output; `--dense --format json` includes `distance` field; `--bm25 --dense` is mutually exclusive (raises SystemExit).

Per-test runtime is dominated by the embedding model load (~1.5s once); module-scoped fixture builds the test DB once.

#### End-to-end smoke on real vault

```
$ tessellum search "knowledge graph" --bm25 --k 3
BM25 matches for 'knowledge graph'  (3 hits)
  1. term_slipbox  (0.056)
      ...<<<Knowledge>>> <<<Graph>>>...
  2. term_zettelkasten  (0.055)
  3. term_information_retrieval  (0.053)

$ tessellum search "knowledge graph" --dense --k 3
DENSE matches for 'knowledge graph'  (3 hits)
  1. thought_building_block_ontology_relationships  (0.487)
  2. term_dialectic_knowledge_system  (0.383)
  3. term_para_method  (0.371)
```

The two strategies return DIFFERENT ranked sets — BM25 finds tokens; dense finds concepts. Wave 3's hybrid RRF will exploit this diversity for the +12pp lift.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.14"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.14"`.
- 265/265 tests pass (248 prior + 17 new).

### What's NOT in this release (Waves 3-5)

- **Wave 3 (v0.0.15)** — Hybrid RRF (the production winner). One SQL `UNION ALL` of BM25 + dense top-K, ranked by `1/(rank + k1)` summed across both. Becomes the default `tessellum search <query>`.
- **Wave 4 (v0.0.16)** — Best-first BFS graph traversal. **No PPR** per FZ 5e2b1c.
- **Wave 5 (v0.0.17)** — Skill orchestration: `skill_tessellum_search_notes` + `skill_tessellum_answer_query` canonicals.

## [0.0.13] — 2026-05-10

### Added — Retrieval Wave 1: BM25 + FTS5

`tessellum search <query>` ships. **The first user-facing query capability** — System D is no longer empty. Per `plans/plan_retrieval_port.md` Wave 1.

```bash
tessellum index build  # populates notes_fts alongside notes + note_links
tessellum search composer
# BM25 matches for 'composer'  (5 hits)
#   1. term_dspy  (2.931)
#       resources/term_dictionary/term_dspy.md
#       ...modules <<<compose>>> (via a Python program)...
#   2. term_atomic_skill  (2.895)
#       ...
```

#### Schema extension — `notes_fts` virtual table

`src/tessellum/indexer/schema.sql` adds:

```sql
CREATE VIRTUAL TABLE notes_fts USING fts5(
    note_id UNINDEXED,
    note_name,
    body,
    tokenize='porter unicode61'
);
```

`UNINDEXED` on `note_id` because we use it for joins, not match. The `porter` stemmer + `unicode61` tokenizer is SQLite's standard for English text with full Unicode normalization.

`src/tessellum/indexer/build.py` populates `notes_fts` from each note's body — no extra disk read since `parse_note` already returned the body in memory.

**Schema migration**: existing `data/tessellum.db` files don't have `notes_fts`. Users re-run `tessellum index build --force` to rebuild. Per the plan: "schema migrations are destructive within v0.x."

#### `tessellum.retrieval.bm25_search`

`src/tessellum/retrieval/__init__.py` + `bm25.py`:

```python
from tessellum.retrieval import bm25_search, BM25Hit

hits = bm25_search("data/tessellum.db", "composer", k=5, snippet_length=30)
# [BM25Hit(note_id=..., note_name=..., score=2.93, snippet="...<<<compose>>>...")]
```

Three details worth knowing:

1. **Score sign**: SQLite's `bm25()` returns lower-is-better. Tessellum's API negates it so `BM25Hit.score` is "higher = more relevant" — matches how users naturally read scores. The internal `ORDER BY bm25(notes_fts)` is unchanged (still ranks correctly).
2. **Snippet generation**: SQLite's `snippet()` wraps matched terms in `<<<...>>>` markers (terminal-friendly, easy to grep). Set `snippet_length=None` to skip generation for batch queries.
3. **Query syntax**: Passed straight to FTS5's `MATCH`. Supports prefix (`foo*`), phrase (`"x y"`), boolean (`AND`/`OR`/`NOT`), and column filters (`note_name:term`). Malformed queries raise `sqlite3.OperationalError`.

#### `tessellum search <query>` CLI

`src/tessellum/cli/search.py` wired into the dispatcher.

| Flag | Default | Purpose |
|---|---|---|
| `<query>` (positional) | required | FTS5 MATCH query |
| `--bm25` | (implicit default) | Forward-compat selector for Waves 2-3 |
| `--db PATH` | `./data/tessellum.db` | Index DB path |
| `--k N` | 20 | Max results |
| `--no-snippet` | off | Skip snippet generation |
| `--format {human,json}` | human | Output format |

Exit codes: 0 success (results may be empty), 2 invocation error (DB missing, malformed query).

In v0.0.13, `tessellum search foo` and `tessellum search --bm25 foo` are equivalent — `--bm25` is reserved for Waves 2-3 when `--dense` and `--hybrid` join. Per the plan: "Wave 3 flips the default to hybrid; document in CHANGELOG."

#### CLI banner

Banner now lists 6 subcommands in usage order:

```
tessellum init <dir>                — scaffold a new vault
tessellum format check <path>       — validate notes against the YAML spec
tessellum capture <flavor> <slug>   — create a new note from a template
tessellum index build               — build the unified SQLite index
tessellum search <query>            — BM25 lexical retrieval (v0.0.13)
tessellum composer validate <skill> — validate a skill's pipeline sidecar
```

#### Tests

25 new tests, all passing. **248 total** (223 prior + 25 new).

- `tests/smoke/test_retrieval_bm25.py` (16 tests):
  - bm25_search returns typed BM25Hit list
  - Ranking: relevant terms rank higher; unique-term lookup; specific-term filter
  - Empty result for unknown query
  - Score sign: positive (negation of FTS5 convention)
  - Scores descend
  - `k` flag limits; `k=0` returns empty
  - Snippet present by default; `snippet_length=None` omits
  - Missing DB raises FileNotFoundError
  - Malformed FTS5 query raises OperationalError
  - Phrase query (`"foundational layer"`)
  - Prefix query (`supersym*`)
  - note_id + note_name shape verified
  - Integration: against the real Tessellum vault.
- `tests/cli/test_search_cli.py` (9 tests):
  - basic search → 0
  - no-match → 0 with "no matches" message
  - missing DB → 2 with stderr message
  - malformed query → 2
  - `--k` limits (verified via `--format json`)
  - JSON output structure (query, strategy, hit_count, hits[*])
  - `--no-snippet` flag omits snippets
  - `--bm25` flag accepted (forward-compat)
  - banner mentions search.

#### End-to-end smoke

```bash
$ tessellum index build --vault vault --db /tmp/test.db
built index at: /tmp/test.db
  notes indexed:  71
  links indexed:  547
  duration:       0.12s

$ tessellum search composer --db /tmp/test.db --k 5
BM25 matches for 'composer'  (5 hits)
  1. term_dspy  (2.931)
  2. term_atomic_skill  (2.895)
  3. term_intermediate_packets  (2.886)
  4. term_dialectic_knowledge_system  (2.621)
  5. template_model  (2.271)
```

All five hits make sense — DSPy is the LM-composition framework that inspired Tessellum's typed-contract approach, atomic_skill describes composable skills, etc. BM25 ranking is doing real work.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.13"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.13"`.
- Removed obsolete `src/tessellum/retrieval/.gitkeep` (replaced by real content).
- 248/248 tests pass (223 prior + 25 new).

### What's NOT in this release (Waves 2-5)

- **Wave 2 (v0.0.14)** — Dense retrieval via sqlite-vec + sentence-transformers. `tessellum search --dense`. Adds `notes_vec` virtual table.
- **Wave 3 (v0.0.15)** — Hybrid RRF (the production winner per FZ 5e1c3a1a1's +12pp finding). `tessellum search` becomes hybrid-by-default; `--bm25` and `--dense` become explicit overrides.
- **Wave 4 (v0.0.16)** — Best-first BFS graph traversal. `tessellum search --bfs <seed>`. **No PPR** per FZ 5e2b1c (Hit@K↔answer-quality disconnect).
- **Wave 5 (v0.0.17)** — Skill orchestration. `skill_tessellum_search_notes.md` (decision-tree router) + `skill_tessellum_answer_query.md` (5-stage QA pipeline).

## [0.0.12] — 2026-05-10

### Added — Indexer Wave 1 (System D substrate)

`tessellum index build` ships the SQLite-backed unified index. **Step 5 of `plans/plan_v01_src_tessellum_layout.md` partially complete** — the substrate-level structure is in place. FTS5 + sqlite-vec + retrieval CLI layer on top in v0.0.13+.

```bash
tessellum index build
# built index at: data/tessellum.db
#   notes indexed:  71
#   links indexed:  547
#   duration:       0.11s
```

#### `src/tessellum/indexer/schema.sql`

Two-table schema, ported verbatim from the parent project's column conventions:

- **`notes`** (18 columns): `note_id`, `note_name`, `note_location`, PARA bucket (`note_category`), second-category (`note_second_category`), `note_status`, dates, file metadata, JSON-encoded `tags`/`keywords`/`topics`, `language`, `building_block`, `folgezettel` + `folgezettel_parent`, indexing timestamps. Six indexes for common access patterns.
- **`note_links`** (6 columns): `link_id`, `source_note_id`, `target_note_id`, `link_context` (±50 chars around the link), `link_type` (`'markdown'` or `'markdown_broken_path'`), `created_at`. UNIQUE constraint on (source, target). Three indexes.

Deliberately **deferred to v0.0.13**: `ghost_notes`, `broken_links`, `folgezettel_trails` (diagnostic tables); FTS5 virtual table; sqlite-vec virtual table; `static_ppr_score`, `in_degree`, `note_int_id` columns (need supporting subsystems first).

#### `src/tessellum/indexer/build.py`

`build(vault_path, db_path, *, force=False) -> BuildResult` — single transactional entry point.

- Walks the vault via `vault.rglob("*.md")` with the same non-note skip list as the format-check CLI (`README.md`, `CHANGELOG.md`, `Rank_*.md`, etc.).
- Parses each note via `tessellum.format.parse_note` (no duplicate parser code).
- Determines `note_category` from the first path segment (PARA bucket); `note_second_category` from `tags[1]` (with parent-folder fallback).
- Extracts internal markdown links with **broken-path detection**: if the relative path doesn't resolve but the target's stem uniquely names an existing note, the link is recorded as `link_type='markdown_broken_path'` with `target_note_id` pointing at the unique match. Useful for retrieval — the link is still a real relationship even if the path is wrong.
- Skips: external `http(s)://`/`mailto:` links, anchor-only `#fragment` links, links inside fenced code blocks, ambiguous broken paths.
- Idempotent: `force=True` deletes + recreates the DB; row counts match across re-runs.

#### `src/tessellum/indexer/db.py`

`Database(db_path)` — read-oriented wrapper around the SQLite connection.

Public methods (typed `NoteRow` / `LinkRow` dataclasses with JSON columns parsed):

| Method | Purpose |
|---|---|
| `all_notes()` | Every row in `notes` |
| `note_by_id(note_id)` | Single lookup |
| `notes_by_building_block(bb)` | Filter by BB enum |
| `notes_by_category(cat)` | Filter by PARA bucket |
| `notes_by_second_category(sub)` | Filter by `tags[1]` |
| `notes_by_folgezettel_root(root)` | All notes whose FZ starts with `root` (string-prefix; full topological sort in v0.0.13+) |
| `links_from(note_id)` | Outbound links |
| `links_to(note_id)` | Inbound links |
| `note_count()` / `link_count()` | Aggregate counts |

Use as a context manager (recommended) or call `close()` explicitly.

#### `src/tessellum/cli/index.py`

`tessellum index build [--vault PATH] [--db PATH] [--force]`

Defaults: `--vault ./vault`, `--db ./data/tessellum.db`. Creates the DB's parent directory as needed. Refuses to overwrite an existing DB without `--force`.

Exit codes: 0 success, 1 DB exists without `--force`, 2 vault doesn't exist.

#### CLI banner reorganized

The bare `tessellum` banner now lists 5 subcommands in the natural usage order:

1. `tessellum init <dir>` — scaffold a vault
2. `tessellum format check <path>` — validate format
3. `tessellum capture <flavor> <slug>` — create a typed note
4. `tessellum index build` — build the unified index
5. `tessellum composer validate <skill>` — validate a skill's pipeline sidecar

#### Tests

29 new tests, all passing. 223 total (194 prior + 29 new).

- `tests/smoke/test_indexer.py` (24 tests):
  - build creates DB with correct row counts
  - build refuses overwrite without `--force`; `--force` works
  - build is idempotent (consecutive runs → same counts)
  - build creates parent dirs as needed
  - missing vault → FileNotFoundError
  - Database queries: `all_notes`, `note_by_id`, `notes_by_building_block`, `notes_by_category`, `notes_by_second_category`, `notes_by_folgezettel_root`, `links_from`, `links_to`, `link_count`, `note_count`
  - JSON columns (tags/keywords/topics) parsed back to tuples
  - external links not indexed; code-block links not indexed; broken-path link uses `markdown_broken_path` type
  - non-note files (README, CHANGELOG, Rank_*) skipped
  - integration test against the real Tessellum vault
- `tests/cli/test_index_cli.py` (5 tests): basic build, refuses overwrite, `--force` works, missing vault → 2, banner mentions index build.

#### End-to-end smoke against the real Tessellum vault

```bash
$ tessellum index build --vault vault --db /tmp/test.db
built index at: /tmp/test.db
  notes indexed:  71
  links indexed:  547
  duration:       0.11s
```

71 notes (matches `tessellum format check vault/`'s file count); 547 internal markdown links resolved (skipping external/anchor/code-block links and ambiguous-broken paths). Indexing runs in ~110ms — fast enough for sub-second CI integration.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.12"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.12"`.
- Removed obsolete `src/tessellum/indexer/.gitkeep` (replaced by real content).
- 223/223 tests pass (194 prior + 29 new).

### What's NOT in this release (deferred)

- **FTS5 lexical retrieval** (v0.0.13/14) — `notes_fts` virtual table + `tessellum search --bm25 <query>` CLI.
- **sqlite-vec dense retrieval** (v0.0.14/15) — `notes_vec` virtual table + sentence-transformers integration + `tessellum search --dense <query>`.
- **Hybrid retrieval** (v0.1.0) — RRF fusion of BM25 + dense + PPR.
- **Diagnostic tables** (v0.0.13) — `ghost_notes`, `broken_links`, `folgezettel_trails`.
- **Incremental update** (v0.0.13) — `tessellum index update` (mtime-based).
- **Composer applies_to_files_query resolution** (Composer Wave 2) — uses the indexer's Database queries to resolve the schema's `term_backlink_candidates`, `related_term_notes`, `related_notes_by_keywords` query kinds.

## [0.0.11] — 2026-05-10

### Added — `tessellum init <dir>` CLI subcommand

Completes step 4c of `plans/plan_v01_src_tessellum_layout.md` and **closes the v0.1 minimum** (format library + the four core CLI subcommands: `init`, `format check`, `capture`, `composer validate`). Users can now scaffold a new vault from scratch:

```bash
tessellum init my-vault
# → 11 dirs created, 16 files copied (templates + seed term), 2 files written (master TOC + README)
cd my-vault
tessellum capture concept zettelkasten --vault .
tessellum format check .
```

#### What `tessellum init` scaffolds

- **All PARA top-level dirs**: `0_entry_points/`, `projects/`, `areas/`, `archives/` (incl. `archives/experiments/`).
- **All capture-flavor destination dirs**: derived from `tessellum.capture.REGISTRY` so every flavor's destination exists out of the box. `tessellum capture skill foo --vault .` works immediately after init.
- **All 13 templates + starter sidecar**: copied from `tessellum.data.templates_dir()` into `resources/templates/`.
- **One seed term note**: `term_building_block.md` (the load-bearing concept), copied from `tessellum.data.seed_vault_dir()`.
- **Generic master TOC**: written inline at `0_entry_points/entry_master_toc.md`, parameterized with the target dir's name. Validates clean (zero ERROR-severity issues).
- **README.md**: top-level vault overview with quick-start commands.

The full set of pillar terms (Z, PARA, BB, EF, DKS, CQRS) is **deferred** to a future `--with-pillars` flag. v0.0.11 ships only `term_building_block.md` to keep the seed minimal; users add the rest via `tessellum capture concept zettelkasten` etc.

#### `tessellum.init.scaffold(target, *, force=False) -> ScaffoldResult`

Library API for programmatic scaffolding. Returns a `ScaffoldResult` with `target`, `dirs_created`, `files_copied`, `files_written`. Raises `FileExistsError` if the target exists and is non-empty (without `--force`); raises `FileNotFoundError` if package data is missing.

#### `tessellum.data.seed_vault_dir()` accessor

Mirrors the existing `templates_dir()` pattern. Resolves the seed-vault root via `Path(__file__).parent / "seed_vault"` in installed mode; falls back to the source-tree `vault/` directly in editable mode (since seed-vault content is force-included from there). Same dual-mode resolution; same import works in dev and production.

#### Force-include — per-file mapping verified

Added a per-file entry to `pyproject.toml`'s `[tool.hatch.build.targets.wheel.force-include]`:

```toml
"vault/resources/term_dictionary/term_building_block.md" = "src/tessellum/data/seed_vault/resources/term_dictionary/term_building_block.md"
```

Hatch supports per-file mapping (not just whole-directory grafting) — verified by `python -m build && unzip -l dist/*.whl | grep seed_vault`. This pattern can be reused to add more seed terms incrementally without grafting the entire `term_dictionary/`.

#### Tests

21 new tests, all passing. 194 total (173 prior + 21 new).

- `tests/smoke/test_init.py` (15 tests) — directory structure, every flavor has a destination, all templates copied, starter sidecar copied, seed term copied + has frontmatter, master TOC has vault name + quick-start, README mentions Tessellum, **scaffolded vault validates with 0 ERROR-severity issues** (templates have placeholder LINK-003 warnings — by design), empty existing dir OK, non-empty dir refused without `--force`, `--force` preserves existing files, target-is-file → error, capture works against scaffolded vault, capture-skill paired emission works against scaffolded vault.
- `tests/cli/test_init_cli.py` (6 tests) — basic scaffold, existing non-empty → 1, `--force` → 0, target-is-file → 1, banner mentions init, help has `--force`.

#### End-to-end smoke

```bash
$ tessellum init /tmp/my-vault
scaffolded vault at: /tmp/my-vault
  directories created: 11
  files copied:        16
  files written:       2

Next steps:
  cd /tmp/my-vault
  tessellum capture concept my_topic --vault .
  tessellum format check .

$ tessellum format check /tmp/my-vault
validated 15 file(s); 0 error(s), 81 warning(s), 0 info(s)

$ tessellum capture concept hello_world --vault /tmp/my-vault
created: /tmp/my-vault/resources/term_dictionary/term_hello_world.md

$ tessellum format check /tmp/my-vault
validated 16 file(s); 0 error(s), 83 warning(s), 0 info(s)
```

Zero errors. Warnings are template placeholder broken-links (LINK-003) and orphan notes (LINK-006) — expected, by design.

### CLI banner reorganized

The bare `tessellum` banner now lists four "Available now (CLI)" entries in the natural usage order:

1. `tessellum init <dir>` — scaffold a vault
2. `tessellum format check <path>` — validate format
3. `tessellum capture <flavor> <slug>` — create a typed note
4. `tessellum composer validate <skill>` — validate a skill's pipeline sidecar

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.11"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.11"`; new `force-include` entry for `term_building_block.md`.

### v0.1 minimum status

The v0.1 plan's minimum (`plans/plan_v01_src_tessellum_layout.md` step 1-4 + Composer Wave 1) is now complete:

| Item | Version |
|---|---|
| Format library | v0.0.2 + v0.0.4 |
| `tessellum format check` | v0.0.3 |
| `tessellum capture` | v0.0.8 (+ paired-sidecar in v0.0.10) |
| Templates `force-include` | v0.0.7 |
| **`tessellum init`** | **v0.0.11 (this release)** |
| Composer Wave 1 (foundation library) | v0.0.9 |
| Composer Wave 1b (validate CLI) | v0.0.10 |

Pending for v0.1+: indexer (step 5), retrieval (step 6), Composer Waves 2-4 (compiler/executor/LLM bridge).

## [0.0.10] — 2026-05-10

### Added — Composer Wave 1b (user-facing surface)

Completes Composer Wave 1 per `plans/plan_composer_port.md`. The skill canonical ↔ pipeline.yaml pairing is now operationalized end-to-end at the CLI level — the user's load-bearing hint about "convert skill canonical note into sidebar yaml" is delivered.

#### `tessellum composer validate <skill>` CLI subcommand

```bash
tessellum composer validate vault/resources/skills/skill_foo.md
# → OK skill_foo.md (3 steps)        if pipeline_metadata points at a valid sidecar
# → OK skill_foo.md (pipeline_metadata: none)  if the skill has no Composer dispatch
# → FAIL skill_foo.md                 if any of the 3 validation stages fails

tessellum composer validate vault/resources/skills/
# Recurses over skill_*.md and reports per-file pass/fail
```

Mirrors the `tessellum format check` pattern: single file or directory, `--format json` for CI integration. Exit codes:

- **0** — every skill validates clean (or declares `pipeline_metadata: none`)
- **1** — at least one skill fails validation
- **2** — invocation error (path doesn't exist, etc.)

#### Paired sidecar emission via `tessellum capture skill <slug>`

`tessellum.capture.capture()` now does extra work for `flavor="skill"`: it emits BOTH `skill_<slug>.md` AND `skill_<slug>.pipeline.yaml` from the paired templates, and rewrites the canonical's `pipeline_metadata: none` to point at the new sidecar.

```bash
tessellum capture skill my_skill --vault vault
# → vault/resources/skills/skill_my_skill.md
# → vault/resources/skills/skill_my_skill.pipeline.yaml

tessellum composer validate vault/resources/skills/skill_my_skill.md
# → OK skill_my_skill.md (1 step)
```

The user's hint operationalized: capture-time conversion, not a one-off migration script. Authors who don't want Composer dispatch can delete the sidecar and revert `pipeline_metadata: ./...` to `none`.

`CaptureResult` gained a `sidecar_path: Path | None` attribute. `None` for non-skill flavors (and as a defensive fallback if the sidecar template is missing — but it ships with the package, so this case shouldn't fire in practice).

#### Starter sidecar template

New `vault/resources/templates/template_skill.pipeline.yaml` — schema-compliant skeleton with one CORE step (`step_1_first_action`) matching the canonical's first anchor. Includes detailed comments for every key (`role`, `aggregation`, `batchable`, `materializer`, `output_key`, `expected_output_schema`, `prompt_template`).

Ships in the wheel automatically — the existing `[tool.hatch.build.targets.wheel.force-include]` rule for `vault/resources/templates/` grafts ALL files in the directory.

#### CLI banner updated

The bare `tessellum` command now lists three subcommands under "Available now (CLI)":

- `tessellum format check <path>`
- `tessellum capture <flavor> <slug>`
- `tessellum composer validate <skill>`

#### Tests

16 new tests, all passing. 173 total (157 prior + 16 new).

- `tests/cli/test_composer_cli.py` (10 tests) — clean skill, `pipeline_metadata: none`, orphan section_id, missing sidecar, directory recursion, missing path, JSON output (clean + dirty), real-skill canonical (the shipped `skill_tessellum_format_check.md`), banner mentions composer.
- `tests/smoke/test_capture.py` (6 new tests on top of the existing 40) — paired sidecar emission for skill flavor, canonical's `pipeline_metadata` pointer, sidecar validates clean via `load_pipeline`, non-skill flavors have `sidecar_path=None`, `--force` overwrites both files, refuses overwrite when sidecar exists.

#### End-to-end smoke against a fresh vault

```bash
$ rm -rf /tmp/tessellum-paired-test-vault
$ mkdir -p /tmp/tessellum-paired-test-vault/resources/skills
$ tessellum capture skill foo --vault /tmp/tessellum-paired-test-vault
created: …/skill_foo.md
$ ls /tmp/tessellum-paired-test-vault/resources/skills/
skill_foo.md  skill_foo.pipeline.yaml
$ tessellum composer validate /tmp/…/skill_foo.md
OK   skill_foo.md (1 step)

validated 1 skill(s); 1 passed, 0 failed
```

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.10"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.10"`.

### What's NOT in this release (deferred to Wave 2+)

- **Compiler** (Wave 2) — DAG build, contract validation, zero LLM calls. `tessellum composer compile <plan_doc>`.
- **Executor + materializers** (Wave 3) — runtime placeholder resolution, agent dispatch, filesystem effect routing. `tessellum composer run <plan_doc>`.
- **LLM bridge** (Wave 4) — Anthropic SDK + optional MCP dispatcher. Behind `[agent]` / `[mcp]` extras.
- **Scale + eval** (Wave 5+) — batch runner, LLMJudge eval framework. Defer to v0.2+.

## [0.0.9] — 2026-05-10

### Added — Composer Wave 1 Foundation (library only)

Per `plans/plan_composer_port.md`. **Pure data + library.** No CLI yet, no LLM dispatch, no compiler. The library lets you load and validate skill pipeline sidecars in Python:

```python
from tessellum.composer import load_pipeline, Pipeline, ContractViolation
pipeline = load_pipeline("vault/resources/skills/skill_foo.md")
```

CLI subcommand (`tessellum composer validate`) and `tessellum capture skill` paired-sidecar emission ship in v0.0.10 (Wave 1 user-facing surface).

#### `src/tessellum/composer/schemas/pipeline.schema.json`

JSON Schema (draft-07) for the pipeline sidebar YAML format. Ported from the parent project with parent-internal references scrubbed:

- `$id` rewrites to `https://tessellum/composer/...`
- `MCPDependency.name` enum → open `pattern: ^[a-z][a-z0-9_-]*$` (Tessellum has no built-in MCPs; users register their own)
- FZ-trail-specific descriptions replaced with neutral language

The schema declares the structure: `version`, `pipeline` array of `Step` items, with required `section_id`/`role`/`aggregation`/`batchable`/`depends_on` per step. Materializer enum (5 values) covers the universal materializers; `applies_to_files_query` is documented as indexer-dependent (not yet shipped).

#### `src/tessellum/composer/contracts.py`

Three contract families as Pydantic V2 frozen models:

- **MaterializerContract** + 5 concrete subclasses (`BodyMarkdownToFileContract`, `BodyMarkdownFrontmatterToFileContract`, `EditsApplyToFilesContract`, `EditsApplyXmlTagsContract`, `NoOpContract`). Module-level registry `MATERIALIZER_CONTRACTS` keyed by materializer name.
- **LLMBackendContract** — declares backend capabilities (allowed_tools, max_user_message_chars, batching support). Default registry ships only `mock` for testing; real backends (Anthropic, OpenAI) ship with the LLM bridge in Wave 4.
- **MCPContract** — declares MCP server capabilities (available_tools, auth_required, rate_limit_qps, fallback_strategy). **Empty registry by default** — Tessellum is generic; users register their own MCPs.

`ContractViolation` exception with 10 violation kinds — defined here so library users can catch it the same way they import the contract types. The compiler (Wave 2) raises this on declaration drift.

#### `src/tessellum/composer/skill_extractor.py`

Three functions for working with skill canonicals:

- `load_skill_section(skill_path, section_id) -> str` — extracts the body text of a section identified by `<!-- :: section_id = X :: -->` anchor. Excludes the heading line; stops at the next H2 (anchored or not).
- `load_pipeline_metadata(skill_path) -> Path | None` — resolves the canonical's frontmatter `pipeline_metadata:` field. Returns `None` for the `"none"` sentinel or absent field; otherwise returns the absolute path to the sidecar (relative paths resolve against the skill's parent directory).
- `list_section_ids(skill_path) -> list[str]` — all section_ids in document order. Used by the loader for cross-file consistency checks.

#### `src/tessellum/composer/loader.py`

`load_pipeline(skill_path) -> Pipeline | None` — three-stage validation:

1. **JSON Schema** validation against `pipeline.schema.json` (structural — required keys, enum membership, pattern match)
2. **Pydantic V2** model construction (`Pipeline` and `PipelineStep` with typed access)
3. **Cross-file consistency** — every step's `section_id` must have a matching anchor in the canonical; orphan section_ids raise `PipelineValidationError`

Returns `None` if the canonical declares `pipeline_metadata: none` (skill has no Composer dispatch — e.g. `skill_tessellum_format_check.md` which is a CLI wrapper, not LLM-dispatched).

`Pipeline`, `PipelineStep`, `MCPDependency`, `Query` are Pydantic V2 frozen models mirroring the JSON schema's shape.

#### Tests

40 new tests across three files, all passing:

- `tests/smoke/test_composer_contracts.py` (18) — registry contents, contract immutability, extra-fields-forbidden, ContractViolation message format, parametrized round-trip serialization for all 5 materializer concrete classes.
- `tests/smoke/test_composer_skill_extractor.py` (11) — section extraction, body-text isolation (stops at next H2 with or without anchor), unknown section_id → error, no-anchors skill → error, document-order listing, pipeline_metadata resolution (relative path / `none` sentinel / absent field). Plus an integration test against the shipped `skill_tessellum_format_check.md` verifying its 10 anchored H2s yield non-empty bodies.
- `tests/smoke/test_composer_loader.py` (11) — happy path returns typed `Pipeline`, dependencies preserved, MCP dependencies typed, `pipeline_metadata: none` → `None`, missing sidecar → error, invalid YAML → error, schema violation (bad enum / missing required field) → error, orphan section_id → error, top-level non-mapping → error.

Total tests now 157/157 passing (117 prior + 40 new).

#### Wheel-build verification

```bash
$ python -m build --wheel
$ unzip -l dist/tessellum-0.0.9-py3-none-any.whl | grep composer
  tessellum/composer/__init__.py
  tessellum/composer/contracts.py
  tessellum/composer/loader.py
  tessellum/composer/skill_extractor.py
  tessellum/composer/schemas/pipeline.schema.json
```

Schema ships automatically because `src/tessellum/composer/schemas/` is inside `src/tessellum/` — no `force-include` needed (correctly noted in the revised plan after the post-research adjustments).

#### What's NOT in this release

Per the plan, the following ship in subsequent versions:

- v0.0.10 (Wave 1 user-facing): `tessellum composer validate` CLI; `template_skill.pipeline.yaml` starter; `tessellum capture skill` paired-sidecar emission.
- Wave 2: compiler (DAG build, contract validation, zero LLM calls).
- Wave 3: executor + materializer implementations.
- Wave 4: LLM backends (Anthropic SDK, optional MCP dispatcher).

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.9"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.9"`.

## [0.0.8] — 2026-05-10

### Added — `tessellum capture <flavor> <slug>` CLI subcommand

Step 4 of `plans/plan_v01_src_tessellum_layout.md` (capture half). Users can now create a new typed note from a template in one command:

```bash
tessellum capture concept page_rank
# → vault/resources/term_dictionary/term_page_rank.md (status: draft, date: today)

tessellum capture skill detect_atomicity_drift
# → vault/resources/skills/skill_detect_atomicity_drift.md

tessellum capture argument cqrs_thesis
# → vault/resources/analysis_thoughts/thought_cqrs_thesis.md
```

#### `tessellum.capture` library module

New `src/tessellum/capture.py` exposes:

- `REGISTRY: dict[str, TemplateSpec]` — 12 registered flavors (one per template under `vault/resources/templates/`, excluding `template_yaml_header` which is a spec reference, not a copy-and-fill skeleton).
- `TemplateSpec` — dataclass with `flavor`, `template_filename`, `destination`, `filename_prefix`, `bb_type`, `second_category`, `description`.
- `list_flavors()`, `get_spec(flavor)` — registry accessors.
- `capture(flavor, slug, vault_root, *, force=False, today=None) -> CaptureResult` — the load-bearing API.

The 12 flavors and their destinations:

| Flavor | Destination | Filename pattern |
|---|---|---|
| `concept` | `resources/term_dictionary/` | `term_<slug>.md` |
| `procedure` | `resources/how_to/` | `howto_<slug>.md` |
| `skill` | `resources/skills/` | `skill_<slug>.md` |
| `model` | `resources/term_dictionary/` | `term_<slug>.md` |
| `argument` | `resources/analysis_thoughts/` | `thought_<slug>.md` |
| `counter_argument` | `resources/analysis_thoughts/` | `thought_counter_<slug>.md` |
| `hypothesis` | `resources/analysis_thoughts/` | `thought_hypothesis_<slug>.md` |
| `empirical_observation` | `resources/analysis_thoughts/` | `thought_observation_<slug>.md` |
| `experiment` | `archives/experiments/` | `experiment_<slug>.md` |
| `navigation` | `0_entry_points/` | `<slug>.md` |
| `entry_point` | `0_entry_points/` | `entry_<slug>.md` |
| `acronym_glossary` | `0_entry_points/` | `acronym_glossary_<slug>.md` |

#### Capture transform — three-step

The capture function applies three transformations to the template content:

1. **Strip the `<!-- HOW TO USE THIS TEMPLATE: ... -->` HTML comment block.** Regex pattern is intentionally specific: requires `\n-->` (closing on its own line), since the instructional text inside the block contains a literal `<!-- HOW TO USE -->` mention ("5. Remove this `<!-- HOW TO USE -->` commentary block.") that would short-circuit a naive non-greedy match.
2. **Replace `date of note: <whatever>` with today's date** (or the explicit `today=` override).
3. **Replace `status: template` with `status: draft`** so the captured note is a real draft, not flagged as a template by search filters.

Other placeholder content (keywords, topics, body sections like `<Concept Name>`) is left for the user to fill — capture is a scaffold, not a content generator.

#### CLI

`src/tessellum/cli/capture.py` is a thin argparse wrapper. Wired into the dispatcher in `cli/main.py`:

- Positional args: `flavor` (one of 12 choices), `slug` (lowercase letters/digits/underscores only).
- Flags: `--vault PATH` (default `./vault`), `--force` / `-f` (overwrite existing).
- Exit codes: `0` success, `1` target file exists (without `--force`), `2` invalid flavor/slug or missing destination directory.

The bare `tessellum` banner now lists `tessellum capture <flavor> <slug>` under "Available now (CLI)".

#### Tests

48 new tests, all passing:

- `tests/smoke/test_capture.py` (40) — registry contents, accessors, slug validation (uppercase / space / hyphen rejected), date/status transforms, HOW TO USE strip (verifies "commentary block" and "EPISTEMIC FUNCTION" leak-text doesn't survive), refuse/force overwrite, parametrized "every flavor produces a validator-clean note" + "every flavor lands at registered destination".
- `tests/cli/test_capture_cli.py` (8) — basic create, invalid slug → 2, existing file → 1, `--force` → 0, missing vault → 2, banner mentions capture, help lists all 12 flavors.

`tests/cli/test_capture.py` was renamed to `test_capture_cli.py` to avoid a pytest module-name collision with `tests/smoke/test_capture.py`.

#### Real-vault smoke test

```bash
$ tessellum capture concept smoke_test_capture --vault vault
created: vault/resources/term_dictionary/term_smoke_test_capture.md
  flavor:  concept
  next:    fill placeholders, then `tessellum format check ...`

$ tessellum format check vault/resources/term_dictionary/term_smoke_test_capture.md
  WARNING[links] LINK-003: link target 'term_related_a.md' does not exist
  WARNING[links] LINK-003: link target 'term_related_b.md' does not exist
validated 1 file(s); 0 errors, 2 warning(s)
```

Two LINK-003 warnings are expected — they're placeholder targets in the template's See Also section that the user replaces when filling in the note.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.8"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.8"`.
- 117/117 tests pass (69 prior + 48 new).

## [0.0.7] — 2026-05-10

### Added — Templates ship in the wheel via `force-include`

Step 3 of `plans/plan_v01_src_tessellum_layout.md`. `pip install tessellum` users now get the 13 canonical BB-type templates without cloning the repo. Prerequisite for upcoming `tessellum init` and `tessellum capture <bb>` CLI subcommands.

#### `pyproject.toml` — `[tool.hatch.build.targets.wheel.force-include]`

```toml
[tool.hatch.build.targets.wheel.force-include]
"vault/resources/templates" = "src/tessellum/data/templates"
```

Hatch grafts files from `vault/resources/templates/` into the wheel at `tessellum/data/templates/` at build time. **Single source of truth in the dogfooded vault**; automatic inclusion in the wheel; no two-copy drift.

#### `tessellum.data.templates_dir()`

New module at `src/tessellum/data/__init__.py` exposing one helper:

```python
from tessellum.data import templates_dir
path = templates_dir()  # -> Path to the templates directory
```

The helper handles **both install modes**:

- **Wheel install**: returns `<site-packages>/tessellum/data/templates/` (where `force-include` grafted them).
- **Editable install** (`pip install -e .`): `force-include` doesn't run for editable installs, so the helper falls back to `<repo>/vault/resources/templates/` via `Path(__file__).resolve().parents[3]`. Same import works in both modes; no caller-side branching.

Raises `FileNotFoundError` if neither location exists (broken install or misconfigured `force-include`).

#### Tests

`tests/smoke/test_data_loader.py` (new, 16 tests):

- `templates_dir()` returns an existing directory
- The directory contains ≥ 13 `template_*.md` files
- Each of the 13 expected templates is present (parametrized)
- Every template starts with YAML frontmatter

All 16 pass in editable mode (the test environment).

#### Wheel-install verification

Build + clean-venv install + import smoke check:

```bash
$ python -m build --wheel
$ unzip -l dist/tessellum-0.0.7-py3-none-any.whl | grep templates
  tessellum/data/templates/README.md
  tessellum/data/templates/template_yaml_header.md
  tessellum/data/templates/template_concept.md
  ...  (13 templates total + README + __init__.py)

$ pip install dist/tessellum-0.0.7-py3-none-any.whl
$ python -c "from tessellum.data import templates_dir; print(templates_dir())"
  /tmp/.../site-packages/tessellum/data/templates
```

#### Out of scope (deferred to future commits)

- **Seed vault** for `tessellum init` (full directory skeleton, not just templates) — bigger scope, ships when `init` does.
- **Skills `force-include`** (so `vault/resources/skills/` is grafted too) — only needed when a CLI subcommand reads skill canonicals at runtime.
- **JSON schemas** under `tessellum.data.schemas/` — when the composer ships and needs schema-validated pipeline configs.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.7"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.7"`.
- All 69 tests pass (53 prior + 16 new in `test_data_loader.py`).

## [0.0.6] — 2026-05-10

### Changed — `scripts/` role clarified (docs-only)

Refined the convention for the top-level `scripts/` directory: **reserved for one-off operational utilities** (vault migrations, repo maintenance, contributor helpers) — *not* core capabilities. Recurring capabilities belong as CLI subcommands under `src/tessellum/cli/`, where they ship in the wheel and are invoked via `tessellum <subcommand>`.

Surfaced when reviewing what to port from the parent project's 60+ scripts: most are now-or-soon CLI subcommands (format check, indexer, retrieval, capture), library modules (config, parser), or already-ported skill canonicals. Only true one-offs (one-time migrations, contributor convenience) belong in `scripts/`.

The decision rule:

| Question | Destination |
|---|---|
| Recurring capability users run via the `tessellum` command? | `src/tessellum/cli/<subcommand>.py` |
| Re-usable library function? | `src/tessellum/<module>/` |
| One-off migration / repo maintenance / contributor helper? | top-level `scripts/` |

**Files updated**:

- `scripts/README.md` (new) — documents the convention with examples in both directions and the decision rule.
- `DEVELOPING.md § Layout Convention` — refined the `scripts/` row from "build / update / format utilities" to "one-off operational utilities, not shipped"; expanded the decision rule into 6 explicit cases.
- `plans/plan_cqrs_repo_layout.md` — refined the `scripts/` row in the System × lifecycle matrix; added a new subsection "scripts/ vs src/tessellum/cli/" calling out the subtlety.

This is a docs-only release. No code changes; library + CLI behavior unchanged. 53/53 tests still pass.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.6"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.6"`.

## [0.0.5] — 2026-05-10

### Changed — Repository layout (CQRS workflow → folder mapping)

Promoted `plans/` to a top-level directory and added `runs/` for runtime traces. Each top-level folder now maps to a defined CQRS role: System P (capture), System D (retrieval), governance (meta to both), or runtime forensics. See [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md) for the full framing.

**New top-level folders**:

- `plans/` — project-management plan notes (committed). Status tracked via YAML `status:` field, not folder layout. Includes `plan_v01_src_tessellum_layout.md` and `plan_cqrs_repo_layout.md` (moved from `inbox/plans/`) plus a README explaining the convention.
- `runs/` — session-scoped runtime traces (gitignored except for `README.md` and `.gitkeep` files). Three subdirectories: `capture/`, `retrieval/`, `composer/`. Filename convention: `<YYYY-MM-DDThh-mm-ss>_<task>.<ext>`.

**Other layout changes**:

- `inbox/plans/` removed — plans no longer claim to be System P input.
- `.gitignore` — `runs/**` ignored except `runs/`, `runs/README.md`, `runs/*/`, `runs/*/.gitkeep`.
- `pyproject.toml` `[tool.hatch.build.targets.sdist]` — `plans` added to `include`; `runs` added to `exclude`.
- `README.md § Project Structure` — rewritten directory tree with the new top-level folders.
- `DEVELOPING.md § Layout Convention` — table now has a System role column; added rows for `plans/` and `runs/`; CQRS framing paragraph; updated decision rule.
- `vault/0_entry_points/entry_master_toc.md` — new "Project State (Outside the Vault)" section listing active plans and pointing at `runs/`.

### Fixed — link_checker config-extension skip list

`tessellum.format.link_checker._NON_MD_EXTS` now exempts common config-file formats: `.toml`, `.cfg`, `.ini`, `.lock`, `.env`. Surfaced during the layout migration when `[pyproject.toml](../pyproject.toml)` in `plan_v01_src_tessellum_layout.md` tripped LINK-001 — `.toml` is a legitimate link target, not a missing-extension defect. Added a parametrized test case covering all five new extensions.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.5"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.5"`.

### Validation

- `tessellum format check plans/`: 2 files, 0 errors, **0 warnings** (was 1 warning pre-fix).
- `tessellum format check vault/`: 71 files, 0 errors, 613 warnings (no regression).
- `pytest tests/`: **53/53 passing** (52 pre-fix + 1 new test for config extensions).

## [0.0.4] — 2026-05-10

### Added — Tier-1 parity with the parent project's format checker

Studied the parent project's `scripts/check_note_format.py` + `skill_slipbox_check_note_format.md` and ported the high-leverage features. Brings Tessellum's checker close to feature-parity for the YAML-frontmatter + body-link surface; H1/H2 section rules and the vault summary report are deferred to a later release.

#### Stable rule IDs on every issue

`Issue` now carries a `rule_id: str` field. IDs follow three families:

- `YAML-NNN` — frontmatter rules (010–099 for presence/type/value, 100–199 for linkage).
- `LINK-NNN` — body markdown link rules.
- `TESS-NNN` — Tessellum-specific rules (folgezettel pair, forbidden fields).

Existing rules are mapped to the parent's IDs where the parent has one (`YAML-010`, `YAML-014`, etc.), so logs and grep patterns are portable. Output format updated to `SEVERITY[field] RULE-ID: message`.

#### `Severity.INFO` (third tier)

Added `Severity.INFO` alongside `ERROR` and `WARNING`. No rule emits INFO yet, but the type is now available for downstream rules that want a "soft suggestion" tier (the parent uses INFO for H1/H2 hints and for orphan-related findings).

#### YAML-100/101 — forbid links inside YAML field values

Wiki links (`[[...]]`) and markdown links (`[text](path.md)`) inside YAML field values silently break the parent project's indexer. Now flagged as ERROR with the line number where they appear. Detection uses the raw frontmatter text (preserved on `Note.raw_frontmatter`), not the parsed dict.

#### LINK-001/002/003/006 — body markdown link checks

New module `tessellum.format.link_checker`:

- **LINK-001** (WARNING) — internal link missing `.md` extension
- **LINK-002** (WARNING) — internal link uses an absolute path (prefer relative)
- **LINK-003** (WARNING) — internal link target does not exist on disk
- **LINK-006** (WARNING) — note has no internal links to other notes (orphan)

Skipped (not flagged): external `http(s)://` and `mailto:` links, anchor-only `#section` links, non-markdown extensions (images, PDFs, code, archives), placeholder targets (`<placeholder>`, `link`, `...`, `-`, etc.), directory links, and any link inside a fenced code block.

`Note.raw_frontmatter: str = ""` is the new required field on the dataclass — populated by `parse_text` / `parse_note` from the regex match.

#### `Note.raw_frontmatter` + parser refactor

Dropped runtime use of `python-frontmatter`; the parser now uses PyYAML directly with a regex to capture both the parsed dict and the raw YAML text. `python-frontmatter>=1.1` removed from runtime dependencies.

#### `--format json` output

`tessellum format check --format json` emits a machine-readable report:

```json
{
  "files": [
    {
      "path": "vault/resources/term_dictionary/term_zettelkasten.md",
      "issues": [
        {"rule_id": "LINK-006", "severity": "warning", "field": "links",
         "message": "note has no internal links to other notes (orphan)"}
      ]
    }
  ],
  "summary": {
    "files_checked": 70, "files_with_issues": 64,
    "errors": 0, "warnings": 613, "infos": 0
  }
}
```

Designed so a CI step can pipe it into `jq` and gate on `summary.errors`.

#### Non-note skip list

The CLI's directory recursion now skips `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`, and any `Rank_*.md`. The parent project skips these because they're not vault notes (no required frontmatter). Library-level `validate(path)` is unchanged — the skip list only applies to CLI directory mode.

#### Tests

20 new tests across 2 files:

- `tests/smoke/test_link_checker.py` (13 tests) — every LINK-* rule, plus negative tests for external/anchor/non-md/placeholder/directory targets and code-block-fenced links.
- `tests/smoke/test_format_validator.py` (7 new tests on top of the existing 16) — rule IDs are well-formed, `Severity.INFO` exists, YAML-100/101 fire on link-in-YAML, plus updated `test_issue_str_*` for the new ctor signature.
- `tests/cli/test_format_check.py` (3 new tests on top of the existing 9) — `--format json` clean + dirty paths, non-note skip list.

All 52 tests pass.

#### Dogfood (separate from this commit)

Running v0.0.4 over `vault/` surfaces **0 errors and 613 warnings**: many LINK-003 (links to planned-but-not-yet-authored notes like `term_folgezettel.md`) and LINK-006 (orphan term notes). These are real findings — the vault is in early build-out — and will be addressed in follow-up data work, not by silencing the checker.

#### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.4"`; status line updated.
- `pyproject.toml`: `project.version` → `"0.0.4"`; `python-frontmatter` removed from runtime deps.

#### Breaking change

`Issue` ctor signature is now `Issue(severity, rule_id, field, message)` (4 positional args). v0.0.2/v0.0.3 used 3 positional args. Library callers constructing `Issue` directly need to add a `rule_id` argument; `validate()` consumers are unaffected.

## [0.0.3] — 2026-05-10

### Added — `tessellum format check` CLI subcommand

The validator shipped in 0.0.2 is now reachable from the shell:

```bash
tessellum format check path/to/note.md     # single file
tessellum format check vault/              # recurse over *.md
tessellum format check vault/ --strict     # treat warnings as errors
tessellum format check vault/ --quiet      # suppress summary when clean
```

Exit codes:

- **0** — no errors (warnings allowed unless `--strict`)
- **1** — at least one ERROR-severity issue (or any WARNING under `--strict`)
- **2** — invocation error (path doesn't exist, not a `.md` file or directory)

Per-file output prints the relative path (anchored at the directory if recursing, otherwise at the file's parent), then one line per issue with severity + field locator + message. A trailing summary reports total files validated, files with issues, and error/warning counts.

The dispatcher in `tessellum.cli.main` now uses argparse subparsers; sibling subcommand modules (`tessellum.cli.format_check`) expose `add_subparser(subparsers)` for wiring. Bare `tessellum` still prints the version + capability banner and now lists `format check` under "Available now (CLI)".

9 smoke tests under `tests/cli/test_format_check.py`: clean file → 0, dirty file → 1, directory recursion, warnings-only → 0, `--strict` promotes warnings to failure, missing path → 2, `--quiet` suppresses summary, bare command prints banner, `--version` exits cleanly.

Bumped:
- `src/tessellum/__about__.py`: `__version__` → `"0.0.3"`; `__status__` updated
- `pyproject.toml`: `project.version` → `"0.0.3"`

Smoke-tested end-to-end in .venv: `tessellum format check vault/` validates all 71 vault notes clean (0 errors, 0 warnings).

## [0.0.2] — 2026-05-10

### Added — Format Library (parser + validator + closed-enum spec)

The typed substrate is now usable as a library: pip users can `from tessellum import validate` to lint their own notes against the spec.

- `tessellum.format.frontmatter_spec` — closed enums as Python data: `VALID_PARA_BUCKETS` (5), `VALID_BUILDING_BLOCKS` (8), `VALID_STATUSES` (21), `REQUIRED_FIELDS` (7), soft minima for tags/keywords/topics, `FORBIDDEN_FIELDS` (`note_second_category`)
- `tessellum.format.parser` — `Note` dataclass with convenience accessors (`tags`, `para_bucket`, `second_category`, `building_block`, `status`, `folgezettel`, `folgezettel_parent`); `parse_note(path)` and `parse_text(str)` entry points; `FrontmatterParseError` for unparseable frontmatter
- `tessellum.format.validator` — `validate(target) -> list[Issue]` and `is_valid(target) -> bool`; checks all 7 required fields, the 3 closed enums, the `YYYY-MM-DD` date format, lowercase-underscore tag format, the both-or-neither rule for `folgezettel:` / `folgezettel_parent:` (incl. legacy `fz_parent` alias), and the `note_second_category` forbidden-field rule
- `tessellum.Issue` and `tessellum.Severity` re-exported at top level for ergonomics
- 23 smoke tests under `tests/smoke/test_format_validator.py` cover every error path + warning path + the 8 BB enum values
- `__about__.py` bumped to `0.0.2`; the CLI banner now points users at `validate` / `parse_note` / `is_valid`

### Caught in dogfooding (separate commit)

The new validator immediately caught 2 real spec violations + 1 corrupted file in this repo's own `vault/`. Those are fixed in a follow-up data commit, demonstrating the library works on real content.

## [0.0.1] — 2026-05-09

### Added — Namespace Reservation

- Repository skeleton with target layout (no `src/` dumping ground; clean separation of code / vault / inbox / data / experiments / scripts / tests)
- `pyproject.toml` declaring the `tessellum` PyPI package with dependencies for the v0.1 engine port
- Top-level `src/tessellum/__init__.py` documenting the six-pillar thesis
- `src/tessellum/format/building_blocks.py` — typed Python registry of the 8 BB types, 4 epistemic layers, and 10 directed edges; the load-bearing primitive of the typed substrate
- `vault/0_entry_points/entry_master_toc.md` — Master TOC entry for the dogfooded vault
- `vault/resources/term_dictionary/term_building_block.md` — first conceptual primer term note
- README + LICENSE (MIT) + CONTRIBUTING + DEVELOPING + this CHANGELOG
- `.gitignore` for derived artifacts (`data/`, `experiments/`, build outputs)

### Architecture decision

Tessellum dogfoods itself: the project's public documentation lives in `vault/` as typed atomic notes, not in a separate `docs/` directory. See [DEVELOPING.md § Layout Convention](DEVELOPING.md#layout-convention).

[Unreleased]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.19...HEAD
[0.0.19]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.18...v0.0.19
[0.0.18]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.17...v0.0.18
[0.0.17]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.16...v0.0.17
[0.0.16]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.15...v0.0.16
[0.0.15]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.14...v0.0.15
[0.0.14]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/TianpeiLuke/Tessellum/releases/tag/v0.0.1
