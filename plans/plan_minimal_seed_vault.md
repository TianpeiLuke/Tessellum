---
tags:
  - project
  - plan
  - tessellum
  - seed_vault
  - onboarding
  - regularization
keywords:
  - minimal seed vault
  - onboarding bundle
  - format regularization
  - typed atomic note reference
  - shipped vault content
  - two-audience seed
topics:
  - Onboarding
  - Vault Content
  - Format Specification
  - v0.1 Roadmap
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Minimal Necessary Seed Vault

## Problem

`tessellum init <dir>` currently scaffolds 8 pillar/supporting term notes, 5 acronym glossaries, a master glossary index, 15 templates, and a per-vault `entry_master_toc.md`. That's a respectable start, but it answers only one half of the question: **what concepts does this system rest on?**

It does NOT answer:

1. **(User question)** *"I just ran `pip install tessellum` and `tessellum init my-vault` — what does this system actually do, and how do I use it?"* The user needs a fast on-ramp: enough orientation to be productive in 10-15 minutes, and a vocabulary to navigate the rest.
2. **(System / agent question)** *"What are the rules I have to follow when authoring a new note here? What's the format contract? Which fields are required? Which enums are closed? What's a valid link?"* The system (the validator, an LLM agent acting against the vault, a contributor adding a new note) needs the format regularization as readable specification — not just enforced silently by `tessellum format check`.

These are the **two audiences** of the seed vault. A note that helps a human onboard isn't necessarily the right shape for a runtime agent learning the constraints; a tight format spec isn't the right shape for a first-time reader. The seed needs to cover both, and currently it covers neither fully.

## Why this matters

The promise of Tessellum is "typed atomic notes that scale." That promise rests on two preconditions:

- The **user** trusts that authoring a note is worth the typing discipline — they have to see the payoff in the architecture, not just the syntax.
- The **system** can enforce the typing without humans memorizing the spec — the regularization has to be readable, machine-parseable, and self-consistent, so a new contributor (human OR agent) can resolve any "what's the rule?" question by reading a note in the vault.

If either half is missing, the cost-benefit shifts:

- Without a user on-ramp, users bounce after 5 minutes — they capture one note, hit a format error, and uninstall.
- Without a regularization reference, agents authoring notes drift from the convention — the validator complains, but the agent can't read *why* the rule exists or how to fix it.

Both failure modes are predictable from the current seed. This plan fixes them by adding a small, deliberate set of notes that **every installed vault must contain**, regardless of what else the user adds later.

## The two audiences in detail

### User (human, first 30 minutes)

Already has:
- 8 pillar terms — `term_building_block`, `term_epistemic_function`, `term_dialectic_knowledge_system`, `term_cqrs`, `term_zettelkasten`, `term_para_method`, `term_slipbox`, `term_folgezettel`
- Master TOC + acronym glossary index
- `README.md` (in the vault root, written by `init`)

Needs:
- A single "start here" reading order — *which term do I read first? Then what?*
- A practical walkthrough — *how do I actually capture my first note? Index? Search? Run a skill?*
- Conceptual primer — *why is this typed? Why these 8 BB types?* (Currently scattered across the pillar terms; needs a synthesis.)

### System / agent (runtime + future contributors)

Already has:
- 15 templates in `data/templates/` — *one per BB-type, with placeholder content + "HOW TO USE" commentary*
- `template_yaml_header.md` — the closed-enum YAML specification
- `template_skill.pipeline.yaml` — Composer sidecar reference
- The validator (`tessellum format check`) and capture registry — enforced silently
- The 8 pillar term notes — describe the ontology *conceptually*

Needs:
- **A single readable spec** of the format contract: which fields are required, which enums are closed, what each tag means, what `building_block:` must hold per BB, how filenames map to flavors, what counts as a link. Today this lives in `template_yaml_header.md` (good) but isn't called out as THE spec.
- **The BB ontology as data**, not just as prose — the 8 types × their epistemic function × the 10 edges in a single table the agent can scan when classifying a new note.
- **The naming + directory convention** — *where does a `concept` note land vs. a `code_snippet` note? What prefix does the filename take?* The capture registry has this; it's not currently mirrored as a readable note.
- **The link-and-trail convention** — relative-path links to other notes, no wikilinks in YAML, the Folgezettel ID convention for trails.

## Design principles

1. **Two audiences, two reading paths, one vault.** The seed must serve a human on-ramp AND a machine-readable spec without duplicating itself. Cross-link aggressively; let each note do one thing.
2. **"Minimal" means load-bearing.** Every shipped seed note must be required, not nice-to-have. If a user could ship `tessellum init` and immediately have a usable, self-explanatory vault, we've hit the bar. If they need to read external docs to make sense of what they got, we haven't.
3. **The format spec lives in one note, not three.** A `term_format_spec.md` (or equivalent canonical name) is the single source of truth for "what's a valid note." The validator's error messages cite it; the templates link to it; the master TOC features it. No spec-by-osmosis.
4. **The BB ontology gets a table view.** The pillar term `term_building_block.md` is conceptual — narrative + epistemic function + when-to-use. A separate `entry_building_block_index.md` (or `thought_*`) gives the agent-readable matrix: 8 rows × {function, primary purpose, valid second-categories, valid epistemic edges}. The pillar term explains *why*; the index says *what holds*.
5. **The pipeline is documented in a how-to, not implied by the CLI.** A new user shouldn't have to read four pillar terms before they see "run these 5 commands and you have a working vault." A `howto_first_vault.md` is the pipeline foundation in vault form.
6. **No new force-include without a verified file.** Every entry added to `pyproject.toml`'s `[tool.hatch.build.targets.wheel.force-include]` must point at an existing, validated note in the dogfooded vault. The seed manifest is the contract; the validator is the gate.
7. **Skill canonicals are not seed material.** They ship under `vault/resources/skills/` for users who want to run Composer, but they're not part of the "minimal necessary" set — a vault is valid without them. The seed is concepts + spec + how-to, not pre-built workflows.

## Current state — inventory + necessity audit

What ships today (v0.0.28), with a Day-1 necessity rating per file:

| File | Lines | Day-1 necessity | Why |
| ---- | -----:| --------------- | --- |
| `term_building_block.md` | 178 | **REQUIRED** | The 8-type ontology *is* the system. Without it, BB is an arbitrary label. |
| `term_para_method.md` | 144 | **REQUIRED** | Tells the user where notes live (resources / projects / areas / archives). |
| `term_epistemic_function.md` | 153 | recommended | Explains *what each BB does*. Useful but a user can read it on day 3, not day 1. |
| `term_slipbox.md` | 117 | recommended | Definitional — names the system class. Not load-bearing for authoring a note. |
| `term_folgezettel.md` | 143 | optional | Trail mechanism. Advanced. Not needed until the user wants to grow a thread. |
| `term_zettelkasten.md` | 297 | optional | Historical foundation. Skippable. |
| `term_dialectic_knowledge_system.md` | 160 | optional | DKS protocol. Advanced; v0.2+ when the dialectic surface ships. |
| `term_cqrs.md` | 101 | optional | Architectural thesis. Interesting but doesn't change what the user types. |
| `entry_acronym_glossary.md` + 5 glossaries | ~3330 | optional | **Lookup tools**, 397 acronyms. Useful when the user encounters jargon, but ~150 KB of content they didn't ask for. |

**Bundle size today:** 14 vault notes (~5500 lines, ~160 KB) + 15 templates + 1 generated TOC. Of the 14 notes, only **2 are load-bearing for Day-1 authoring**. The other 12 are valuable but not minimal-necessary.

**What's missing for Day-1 success:**

| Gap | Why it matters |
| --- | -------------- |
| No single format-spec note | User hits a `tessellum format check` ERROR and has nowhere readable to look up the rule. The validator cites issue codes (TESS-003, YAML-015, LINK-003); a note must explain each. |
| No BB-classification matrix | The user looking at the 14 templates can't quickly answer "which BB type for my note?" — `term_building_block.md` is 178 lines of narrative, not a table. |
| No pipeline walkthrough | README has a Quick Start; the vault doesn't. Users who open the freshly-init'd vault in Obsidian don't see the CLI flow. |

## Proposed approach — a single default seed + glossary opt-out

Earlier drafts of this plan proposed a tiered seed (Tier M minimal + `--primer` + `--glossaries`). User feedback corrected the framing: **the conceptual foundation IS the minimal**. A user installing Tessellum needs to know what a Slipbox is, what Zettelkasten is, what PARA is, what CQRS is, what Folgezettel are, what BASB and CODE are — these are not "deep architectural extras." They are the load-bearing vocabulary that makes everything else legible.

So: ship the conceptual foundation by default. Make only the high-volume **glossary block** opt-out.

### Default seed — `tessellum init` (14 vault notes, ~2200 lines)

**Conceptual foundation (11 term notes — the vocabulary):**

| Term note | Lines | What it provides |
| --------- | -----:| ---------------- |
| `term_knowledge_building_blocks.md` | 152 | The predecessor concept (Sascha Fast / zettelkasten.de) — what "knowledge building blocks" are in general |
| `term_building_block.md` | 178 | Tessellum's 8-type typed atomic ontology — the system's load-bearing structure |
| `term_epistemic_function.md` | 153 | What each BB *does* (name / structure / claim / refute / observe / predict / act / index) |
| `term_dialectic_knowledge_system.md` | 160 | DKS — the closed-loop dialectic protocol that gives the BB graph teeth |
| `term_cqrs.md` | 101 | System P (write) ⊥ System D (read), shared substrate |
| `term_zettelkasten.md` | 297 | The historical foundation (Luhmann; ~90k connected ideas) |
| `term_slipbox.md` | 117 | The system class (Tessellum is one Slipbox implementation) |
| `term_folgezettel.md` | 143 | Trail mechanism — encoding *how thinking developed* |
| `term_para_method.md` | 144 | Tiago Forte's organizational scheme (Projects / Areas / Resources / Archives) |
| `term_basb.md` | 117 | Building a Second Brain — the personal-knowledge-management movement Tessellum descends from |
| `term_code_method.md` | 108 | CODE (Capture / Organize / Distill / Express) — Forte's PKM lifecycle |

**System regularization (3 new notes — the format contract):**

| Note | Status | What it provides |
| ---- | ------ | ---------------- |
| **`term_format_spec.md`** | **NEW** | YAML frontmatter contract + tag conventions + link rules + validator issue codes (TESS-NNN, YAML-NNN, LINK-NNN) — the system regularization |
| **`entry_building_block_index.md`** | **NEW** | 8-row BB matrix (BB × epistemic function × default directory × valid epistemic edges) — the scannable picker for "which BB type fits my note?" |
| **`howto_first_vault.md`** | **NEW** | 8-step CLI walkthrough: init → capture → format check → index → search → composer validate / compile / run |

**Already shipped (outside the vault):**

- 15 templates in `data/templates/` (per-BB exemplars + YAML reference + skill sidecar)
- `entry_master_toc.md` (generated per-vault by `init`, sequences the reading order)
- `README.md` (generated per-vault by `init`)

**Default install footprint:** 14 vault notes + 15 templates + 2 generated = 31 files, ~2200 lines.

### Glossary block — `tessellum init --no-glossaries` to omit (default: include)

The 6 acronym files (5 universal + master index, ~3400 lines, 397 acronyms) ship by default. Users with a tight install budget can pass `--no-glossaries` to skip them.

| File | Lines | Domain |
| ---- | -----:| ------ |
| `entry_acronym_glossary.md` | 80 | Master index |
| `acronym_glossary_cognitive_science.md` | 1092 | Cognitive biases, dual-process theory, decision heuristics |
| `acronym_glossary_llm.md` | 1038 | LLM architectures, RAG, agents, evaluation |
| `acronym_glossary_statistics.md` | 422 | Causal inference, Bayesian methods, distributions |
| `acronym_glossary_critical_thinking.md` | 394 | Logic, fallacies, reasoning patterns |
| `acronym_glossary_network_science.md` | 385 | Graph theory, centrality, community detection |

**Total default install:** 14 conceptual + 6 glossaries = 20 vault notes + 15 templates + 2 generated = 37 files, ~5600 lines.

### Why drop the tiered `--primer` flag

The original `--primer` proposal split the conceptual primer behind an opt-in. The user's directive made the choice clearer: **the conceptual foundation is what makes the rest of the system legible**. Splitting Zettelkasten and CQRS out of the default leaves a user staring at term_building_block without the surrounding vocabulary. The cost of shipping 11 small term notes (~1700 lines) is negligible; the cost of *not* shipping them is comprehension friction.

The remaining opt-out flag (`--no-glossaries`) is justified by size — glossaries are 60% of the total seed weight and most users use them as lookup, not reading. Letting the budget-conscious user skip them is the right escape hatch.

## The 3 new notes (Tier M additions)

### 1. `vault/resources/term_dictionary/term_format_spec.md` — the format contract (System)

A `building_block: model` note that IS the format spec. Single source of truth for:
- YAML frontmatter required fields (`tags`, `keywords`, `topics`, `language`, `date of note`, `status`, `building_block`)
- Closed enums:
  - `building_block:` — 8 BB types + `navigation`
  - `status:` — `active | archived | draft | superseded | template`
  - `language:` — open string but uses standard names (`markdown`, `python`, etc.)
- Tag conventions:
  - `tags[0]` = PARA bucket (`resource | project | area | archive`)
  - `tags[1]` = second category (drives directory)
  - `tags[2..]` = free-form domain tags (lowercase, underscores, no spaces)
- Filename + directory rules per flavor (derived from `capture.REGISTRY`, kept in sync via a test)
- Link rules: relative paths only, no wikilinks (`[[...]]`) anywhere, no markdown links inside YAML
- The 5 validator severities (`ERROR`, `WARNING`, `INFO`, `TESS-NNN`, `YAML-NNN`, `LINK-NNN` issue codes) with example fixes

**Why a term note (not entry_point):** the format spec IS a model — a structural description of what holds. `term_format_spec.md` is the readable name; `building_block: model` is the type.

### 2. `vault/0_entry_points/entry_building_block_index.md` — BB ontology table (System)

The 8-row matrix the agent scans when classifying:

| BB type | Epistemic function | Second-category tags | Default directory | Valid epistemic edges |
| ------- | ------------------ | -------------------- | ----------------- | --------------------- |
| concept | name | `terminology` | `resources/term_dictionary/` | `concept → procedure`, `concept → model`, ... |
| procedure | structure (action) | `how_to`, `skill` | `resources/how_to/` | ... |
| model | structure (relational) | `terminology`, `code_repos` | `resources/term_dictionary/` | ... |
| argument | claim | `analysis` | `resources/analysis_thoughts/` | ... |
| counter_argument | refute | `analysis` | `resources/analysis_thoughts/` | ... |
| hypothesis | predict | `analysis` | `resources/analysis_thoughts/` | ... |
| empirical_observation | observe | `analysis`, `experiment` | `resources/analysis_thoughts/` | ... |
| navigation | index | `index`, `navigation` | `0_entry_points/` | (no outbound — leaf) |

Plus the **10 epistemic edges** (the DKS dialectic graph) as a separate table:

| Source BB | Edge | Target BB |
| --------- | ---- | --------- |
| argument | refuted by | counter_argument |
| counter_argument | synthesizes into | argument |
| ... | ... | ... |

`building_block: navigation` — the note is an index, not a model.

### 3. `vault/resources/how_to/howto_first_vault.md` — the pipeline walkthrough (User)

The CLI Quick Start in vault form, ~80 lines:

- Step 1: `tessellum init my-vault` — what files appear
- Step 2: `tessellum capture concept page_rank` — your first typed atomic note
- Step 3: Fill the template — what to keep, what to remove (the HOW TO USE block)
- Step 4: `tessellum format check .` — fix any errors using the codes in `term_format_spec.md`
- Step 5: `tessellum index build` — build the unified DB
- Step 6: `tessellum search "PageRank"` — hybrid retrieval default
- Step 7: `tessellum capture skill my_skill` — get a paired canonical + sidecar
- Step 8: `tessellum composer validate` then `compile` then `run` — run the skill end-to-end

Each step has the expected output (one line of CLI output, or "the file is created here") so the user can verify they're on track.

`building_block: procedure` — it's a how-to.

### 4. Update `_render_master_toc` in `src/tessellum/init.py` (User)

The auto-rendered TOC gets two new rows:

- "**First time here? Read this:**" → `howto_first_vault.md`
- "**Format rules:**" → `term_format_spec.md`

And a "Reading order" section that sequences the 8 pillar terms:

1. `term_zettelkasten` — the historical foundation
2. `term_slipbox` — the system class
3. `term_para_method` — the organizational scheme
4. `term_building_block` — the typed atomic ontology (LOAD-BEARING)
5. `term_epistemic_function` — what each BB does
6. `term_folgezettel` — how thinking trails are encoded
7. `term_dialectic_knowledge_system` — the closed-loop dialectic
8. `term_cqrs` — the read/write split that ties it together

Reading order is opinionated but defensible: history → class → buckets → atomic types → functions → trails → dialectic → architectural thesis. A new user reading top-to-bottom gets the full conceptual model in ~45 minutes.

## What this is NOT

- **Not a tutorial library.** One how-to is enough; subsequent how-tos are user-authored.
- **Not a complete BB-example collection.** The plan calls for `examples/` directory with one note per BB type later; that's not seed material because each example reveals authorial taste. Templates are spec; examples are taste.
- **Not skill canonicals.** Skills ship for users who run Composer (`vault/resources/skills/skill_tessellum_*.md`), but they're not "minimal necessary." A vault without skills is still a valid Tessellum vault.
- **Not pre-authored projects / areas / archives.** PARA buckets ship empty (`.gitkeep`) — the user adds their own content.

## Verification criteria

The Tier-M seed is "minimal necessary" when all of the following hold:

1. **Tier-M alone is self-sufficient.** Default `tessellum init` (5 notes + templates + TOC) lets a user author + validate + index + search their first note without reading external docs. Tier C and Tier G are *enhancements*, not prerequisites.
2. **Editable + wheel install parity** — every tier combination produces identical file lists across `pip install -e .` and `pip install tessellum`.
3. **Every shipped seed note passes `tessellum format check`** with 0 errors. Warnings (`LINK-003` for placeholder links to non-seed notes) are acceptable.
4. **Every internal link inside Tier M resolves.** Tier-M notes reference each other and the templates; none reference Tier C or Tier G notes (otherwise Tier M isn't self-sufficient). Tier-C and Tier-G notes may link forward to Tier M; the reverse must not happen.
5. **The user-on-ramp test:** a developer with no prior Tessellum knowledge runs `pip install tessellum && tessellum init demo && cd demo` and reaches "a working captured + validated + indexed + searchable vault" in under 10 minutes, using only files in Tier M.
6. **The agent-spec test:** an LLM agent given only the Tier-M vault as context can correctly classify a fresh note as one of the 8 BB types, set its frontmatter, and place it in the right directory.
7. **The reading order is opinionated and short.** Tier-M's master TOC sequences the 5 notes for a first-time reader: `howto_first_vault` (action) → `term_format_spec` (rules) → `entry_building_block_index` (picker) → `term_building_block` (depth on the picker) → `term_para_method` (where things land). 5 notes in this order, ~30 min reading.

## Migration steps

Execute as **one commit** (small, atomic, easy to revert if a check fails):

### Step group A — Author the 3 new Tier-M notes

1. **`term_format_spec.md`** under `vault/resources/term_dictionary/`. Cross-reference `template_yaml_header.md` and the validator's issue codes (TESS-*, YAML-*, LINK-*). Validate. ~150-200 lines.
2. **`entry_building_block_index.md`** under `vault/0_entry_points/`. Two tables: 8 BB types × {function, default directory, valid epistemic edges} + the 10 epistemic edges. Cross-reference `term_building_block.md` and `term_epistemic_function.md`. Validate. ~100 lines.
3. **`howto_first_vault.md`** under `vault/resources/how_to/`. 8 steps, each with command + expected output line. Validate. ~80 lines.

### Step group B — Restructure the seed manifest into tiers

4. **`pyproject.toml`** — already ships the full set via `force-include`. Keep it (the wheel still grafts everything; runtime tier selection is the gate). Add 3 new entries for the Tier-M notes.
5. **`src/tessellum/init.py`** — split `_SEED_VAULT_MANIFEST` into three named tuples: `_SEED_TIER_M`, `_SEED_TIER_C`, `_SEED_TIER_G`. Compose at runtime based on CLI flags.
6. **`src/tessellum/cli/init.py`** — add `--primer` and `--glossaries` flags (each defaulting to `False`); add `--all` shorthand. Pass through to `scaffold(..., include_primer=..., include_glossaries=...)`.
7. **`scaffold()` signature** — add the two boolean kwargs; iterate the manifests that are selected.
8. **`_render_master_toc()`** — render different content based on which tiers are present:
   - Always: "First time here" → `howto_first_vault.md`, "Format rules" → `term_format_spec.md`, BB matrix → `entry_building_block_index.md`
   - If Tier C: add the "Six Pillars" reading-order section pointing at the 6 conceptual primer terms
   - If Tier G: add the "Acronym Glossaries" row pointing at the master glossary index

### Step group C — Verify

9. **Smoke test all three tier combinations**:
   - `tessellum init /tmp/m` → 5 vault notes + 15 templates + master TOC + README = ~22 files
   - `tessellum init /tmp/mc --primer` → 5 + 7 + templates + TOC + README = ~30 files
   - `tessellum init /tmp/all --all` → 5 + 7 + 6 + templates + TOC + README = ~36 files
   - Every case passes `tessellum format check . ` with 0 errors
   - Editable mode (`pip install -e .`) and wheel mode produce identical file lists per tier

### Step group D — Ship

10. **Bump version** to v0.0.29. CHANGELOG entry. Commit + push.
11. **PyPI push** — `python -m build && twine upload dist/tessellum-0.0.29-*`.

### Step group E — Update v0.0.28's docs

12. **README.md** — update Quick Start to mention `--primer` / `--glossaries` / `--all`. Mention that default `tessellum init` ships Tier M only.
13. **`__about__.py` status** — describe the tiered seed.

## Open questions

- **Default tier on bare `tessellum init`** — Tier M only (lean: yes), or Tier M + C (the conceptual primer included by default)? Lean Tier M: the goal of "minimal-necessary" is to *not* push more than necessary. A user wanting the primer is one flag away (`--primer`).
- **Should glossaries be runtime-installable** instead of bundled in the wheel? E.g., `tessellum glossary install statistics` fetches from a registry. Lean: defer. Wheel-bundling is simpler and the user can delete files they don't want. Revisit if the install size becomes a complaint.
- **`term_format_spec.md` vs `entry_format_spec.md`** — model (term) or navigation (entry point)? Lean: term note, because it's structural. The format spec is a model of what a valid note looks like — it's not a navigation surface.
- **Should `entry_building_block_index.md` ship with hardcoded edge content, or derive from `EPISTEMIC_EDGES` in `src/tessellum/format/building_blocks.py`?** Lean: hardcoded with a CI test diffing the table against the Python source. The note is readable as static documentation; the test catches drift.
- **Should `howto_first_vault.md` mention `tessellum composer`?** Lean: yes, in a "Going further" section. Composer is the major v0.1 feature; flagging it in the first how-to is honest.
- **Should the seed ship `examples/` notes** — one per BB type? Lean: defer. Templates are the spec; examples reveal authorial taste.
- **Backwards compatibility** — does adding Tier-M notes to existing vaults break anything? Lean: skip-if-exists by default, `--force` overwrites. Current init already follows this pattern.

## See Also

- [`plan_v01_src_tessellum_layout.md`](plan_v01_src_tessellum_layout.md) — the v0.1 release plan; this plan operationalizes its "seed vault" line item
- [`plan_code_artifacts_port.md`](plan_code_artifacts_port.md) — the precedent for "scrub-and-port from AbuseSlipBox + validate via format check"
- [`plan_composer_port.md`](plan_composer_port.md) — defines `template_skill.pipeline.yaml` which is the system-facing seed material for Composer
- `src/tessellum/init.py` — `_SEED_VAULT_MANIFEST` is the load-bearing data structure this plan extends
- `src/tessellum/format/validator.py` — the validator whose issue codes `term_format_spec.md` must mirror
- `src/tessellum/capture.py` — `REGISTRY` is the source of truth that `entry_building_block_index.md`'s "default directory" column must agree with

---

**Last Updated**: 2026-05-10
**Status**: Active — draft pending user approval. Ships as v0.0.29 across one commit, then PyPI push.

## Summary — the load-bearing claim

**Tier M (5 notes, default):**

```
vault/0_entry_points/
    entry_master_toc.md                  (generated per-vault)
    entry_building_block_index.md        NEW — the BB picker table
vault/resources/term_dictionary/
    term_building_block.md               (already ships) — what's a BB
    term_para_method.md                  (already ships) — where things live
    term_format_spec.md                  NEW — the YAML / link / naming contract
vault/resources/how_to/
    howto_first_vault.md                 NEW — the 8-step CLI walkthrough
vault/resources/templates/
    (15 templates — already ship)
README.md                                (generated per-vault)
```

Every install gets these. Together they answer:

1. **User: "what does this system do?"** → `term_building_block` + `term_para_method` + `howto_first_vault` answer in concrete terms.
2. **System / agent: "what regularization should I follow?"** → `term_format_spec` + `entry_building_block_index` + templates answer in machine-readable terms.

**Tier C (`--primer`):** 8 additional pillar terms — for users who want the conceptual depth.

**Tier G (`--glossaries`):** 6 acronym-glossary files — for users who want the 397-acronym lookup tools.

**`--all`:** Tier M + C + G.
