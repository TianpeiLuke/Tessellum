---
tags:
  - project
  - plan
  - tessellum
  - capture
  - code_repo
  - code_snippet
  - acronym_glossary
keywords:
  - code repo notes
  - code snippet notes
  - acronym glossaries
  - capture skills
  - amazon-internal scrub
topics:
  - Capture
  - Templates
  - v0.1 Roadmap
  - Vault Content
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Port Code-Artifact Notes & Glossaries to Tessellum

## Problem

AbuseSlipBox has a mature, tested capture surface for two code-artifact note types and a rich set of acronym glossaries that index domain terminology. None of it has been ported to Tessellum yet. The user wants:

1. **Acronym glossaries** in `vault/0_entry_points/` so newcomers can resolve unfamiliar acronyms without leaving the vault.
2. **`template_code_snippet.md`** + **`template_code_repo.md`** under `vault/resources/templates/` so `tessellum capture code_snippet <slug>` and `tessellum capture code_repo <slug>` work like the other 12 capture flavors.
3. **Two capture skills** ported and adapted: `skill_tessellum_capture_code_snippet.md` + sidecar, `skill_tessellum_capture_code_repo_note.md` + sidecar.
4. **All Amazon-internal content scrubbed** — references to `code.amazon.com`, internal tools (Nautilus, Paragon, Triton, LEADS, TTUX, CamShaft, Cradle, Wasabi, Brazil, Coral, Midway, Isengard, Sandalwood, etc.), abuse-domain teams/systems, and Amazon-business acronyms must NOT ship in the public vault.

## Why this matters

These three artifact types form a tight triangle: a code repo note documents a project; code snippet notes document algorithms or components inside the repo; acronym glossaries resolve the technical vocabulary used by both. A user who installs Tessellum and runs `tessellum capture code_snippet my_algo` should land on a template that produces a snippet note that other users can read without needing to know what "MTR" or "Cradle" means. Right now they can't capture either; once they can, the vault scaffold demonstrates the full Tessellum-as-public-slipbox workflow.

## Inventory — what's in the source

### Acronym glossaries (16 files in `src/buyer_abuse_slipbox_agent/abuse_slipbox/0_entry_points/`)

| Glossary | Lines | AB-internal mentions | Disposition |
| -------- | -----:| --------------------:| ----------- |
| `acronym_glossary_statistics.md` | 460 | 16 | **Keep + light scrub** — universal stats |
| `acronym_glossary_network_science.md` | 390 | 18 | **Keep + light scrub** — universal graph theory |
| `acronym_glossary_critical_thinking.md` | 396 | 29 | **Keep + light scrub** — universal logic/reasoning |
| `acronym_glossary_cognitive_science.md` | 1102 | 34 | **Keep + light scrub** — universal cog-sci |
| `acronym_glossary_security.md` | 546 | 63 | **Keep + scrub** — mostly universal infosec |
| `acronym_glossary_llm.md` | 1236 | 129 | **Keep + scrub** — core for an LLM-driven slipbox |
| `acronym_glossary_ml.md` | 1853 | 296 | **Keep + heavy scrub** — universal ML |
| `acronym_glossary_developer.md` | 1529 | 368 | **Keep + heavy scrub** — strip AB tools, keep universal dev |
| `acronym_glossary_tools.md` | 712 | 236 | **Keep + heavy scrub** — keep open-source/general tools only |
| `acronym_glossary_data_governance.md` | 317 | 31 | **Keep + scrub** — universal data-gov terminology |
| `acronym_glossary_abuse_networks.md` | 1016 | 343 | **Drop** — domain-specific to Amazon abuse fight |
| `acronym_glossary_business.md` | 588 | 112 | **Drop** — Amazon retail business metrics |
| `acronym_glossary_workflows.md` | 639 | 113 | **Drop** — Amazon-internal workflow tooling |
| `acronym_glossary_teams.md` | 773 | 217 | **Drop** — Amazon org structure |
| `acronym_glossary_systems.md` | 2291 | 548 | **Drop** — overwhelmingly AWS-internal |
| `acronym_glossary_data_metrics.md` | 1636 | 355 | **Drop** — Amazon retail data products |

Result: **10 glossaries kept, 6 dropped.**

### Existing code-artifact notes (source for template extraction)

- `src/buyer_abuse_slipbox_agent/abuse_slipbox/areas/code_repos/repo_*.md` — 30+ examples; main + sub-note structure with parent backlink, attribute table, code structure, and reference sections. **Pick one** as the canonical example to derive `template_code_repo.md`. Lean: `repo_slipbox_agent_databases.md` (clean, has the standard sections, only mild AB-internal).
- `src/buyer_abuse_slipbox_agent/abuse_slipbox/resources/code_snippets/snippet_*.md` — 100+ examples; the `## Patterns` template with dual code blocks per pattern is the load-bearing innovation. **Pick one** as canonical. Lean: `snippet_slipbot_ppr.md` (a procedure-BB snippet with mermaid diagram, 5 patterns; clean structure).

### Capture skills (~750 LOC each)

| Skill | Lines | Sidecar lines | What needs adapting |
| ----- | -----:| -------------:| ------------------- |
| `skill_slipbox_capture_code_repo_note.md` | 221 | 289 | URL refs (`code.amazon.com`), tool refs (Cradle/Wasabi), entry-point name (`entry_skill_catalog.md` → Tessellum has no equivalent yet) |
| `skill_slipbox_capture_code_snippet.md` | 558 | 227 | URL refs, package-naming convention assumptions, master-TOC-of-entry-points pattern |

## Design principles

1. **The public vault must read clean.** A first-time reader of any glossary, snippet, or repo note in `vault/` should not encounter Amazon-internal jargon. If a section can't be scrubbed without losing meaning, drop the section.
2. **Templates carry placeholder content, not example content.** A template's job is to teach the structure; it shouldn't ship with snippet of a real algorithm or a real-repo URL. Every concrete reference becomes `<placeholder>` or `<example>`.
3. **Skills are renamed `slipbox-*` → `tessellum-*`** and updated to use Tessellum's CLI surface (`tessellum index build`, BM25 / hybrid search) rather than AbuseSlipBox's `bm25_search.py` script.
4. **Capture flavor registry stays the source of truth.** Adding `code_repo` and `code_snippet` to `REGISTRY` in `src/tessellum/capture.py` is what makes `tessellum capture code_snippet my-algo` work — without it, the templates are inert.
5. **Hatch `force-include` mirrors templates into the wheel** automatically — no pyproject change needed (the `vault/resources/templates/` graft is already wired).
6. **Glossary YAML stays close to source format** — same `building_block: navigation`, same `tags: [entry_point, index, navigation, quick_reference, glossary, <domain>]`, same H2 structure. The scrub touches body content, not frontmatter shape.

## Proposed approach — three phases

### Phase 1 — Templates + capture-flavor wiring (smallest, lowest risk)

Adds two templates and wires them into the capture registry. Once landed, `tessellum capture code_repo <slug>` and `tessellum capture code_snippet <slug>` produce well-formed (placeholder-filled) notes. No skill yet.

1. **`vault/resources/templates/template_code_snippet.md`** — derive from `snippet_slipbot_ppr.md` shape:
   - YAML frontmatter with `building_block: <concept|procedure|model>` placeholder
   - `# Code Snippet: <Name> — <One-Line Description>`
   - `## Purpose` (2-3 sentences placeholder)
   - BB-specific section (Mathematical Definition / Procedure / Architecture)
   - `## Patterns` with `### Index` table + one example `### Pattern N` showing dual-block shape
   - `## Source` (file:line range)
   - `## References`
   - **Crucially**: scrub mermaid styling that uses Amazon palette colors; keep monochrome.
2. **`vault/resources/templates/template_code_repo.md`** — derive from `repo_slipbox_agent_databases.md` shape:
   - YAML frontmatter with `building_block: model`, `code_repo_url:` placeholder (no `code.amazon.com`)
   - `# Repository: <Name> — <One-Line>`
   - `## Overview` with attribute table (URL, language, owner, deps placeholder)
   - `## Architecture` (optional)
   - `## Sub-Notes` (optional)
   - `## Code Structure` tree
   - `## References`
3. **`src/tessellum/capture.py`** — append two `TemplateSpec` entries:
   ```python
   "code_snippet": TemplateSpec(
       flavor="code_snippet",
       template_filename="template_code_snippet.md",
       destination="resources/code_snippets",
       filename_prefix="snippet_",
       second_category="code_snippets",
       description="Code snippet documenting one component or algorithm",
   ),
   "code_repo": TemplateSpec(
       flavor="code_repo",
       template_filename="template_code_repo.md",
       destination="areas/code_repos",
       filename_prefix="repo_",
       second_category="code_repos",
       description="Code repository documentation note",
   ),
   ```
4. **Tests** — extend `tests/smoke/test_capture.py` and `tests/cli/test_capture_cli.py` with one happy-path test per new flavor (capture creates file at expected path, frontmatter parses).

**Milestone**: `tessellum capture code_snippet my_algo` and `tessellum capture code_repo my_repo` both produce valid notes that pass `tessellum format check`.

### Phase 2 — Acronym glossaries (10 files)

Per-glossary scrub + drop into `vault/0_entry_points/`. Each glossary is independent; they can ship in one commit.

1. For each kept glossary (10 files):
   - Copy verbatim to `vault/0_entry_points/`.
   - Run a scrub pass: drop entries that name internal tools (Nautilus, Paragon, Triton, LEADS, TTUX, CamShaft, etc.); rewrite section intros that reference Amazon roles ("SDEs and Applied Scientists at Amazon" → "developers and researchers"); replace `code.amazon.com` URLs with placeholder or generic GitHub references.
   - Update internal nav line: `[← Back to Main Glossary](entry_acronym_glossary.md)` → either drop (no master glossary in Tessellum yet) or point to the master TOC.
   - Validate `tessellum format check vault/0_entry_points/<file>.md` passes.
2. **Optional master glossary** (`entry_acronym_glossary.md`) — a thin TOC linking all 10. Lean: skip for now; users can find them by directory listing. Add later if there's demand.

**Milestone**: 10 glossaries land in `vault/0_entry_points/`, all pass format check, none mention Amazon-internal tooling.

### Phase 3 — Capture skills (the hard part)

Port both skill canonicals + sidecars, adapt to Tessellum's CLI + vault layout.

1. **`vault/resources/skills/skill_tessellum_capture_code_repo_note.md`** + sidecar:
   - Rename header from `slipbox-capture-code-repo-note` → `tessellum-capture-code-repo-note`.
   - Replace `code.amazon.com/packages/.../trees/mainline` → `https://github.com/<owner>/<repo>`.
   - Replace `bm25_search.py` script invocations with Tessellum CLI (`tessellum search --bm25 ...`).
   - Drop `related_skill_headers:` (no `.claude/skills/` or `.kiro/skills/` shims in Tessellum yet).
   - Update `pipeline_metadata` ref to point at the renamed sidecar.
   - Keep the `<!-- :: section_id = X :: -->` anchors intact (load-bearing for Composer).
   - Drop the "Update Database" step (`bash ./scripts/update_notes_database.sh` → `tessellum index build`).
2. **`vault/resources/skills/skill_tessellum_capture_code_snippet.md`** + sidecar — same treatment:
   - Rename slipbox → tessellum.
   - Replace AB-specific tool references in setup block.
   - Adapt the per-package entry-point pattern; Tessellum can drop "TOC-of-entry-points" complexity for v0.1 (single `entry_code_snippets.md` is fine until the snippet count justifies splitting).
   - Keep the BB-by-BB section structure (concept/procedure/model) verbatim — that's the load-bearing taxonomy.
   - Keep the `## Patterns` template (Index + dual-block per pattern).
3. **Sidecars** — both `.pipeline.yaml` files: bump anchor IDs to match the renamed canonicals; remove pipeline steps that reference dropped skill sections; validate via `tessellum composer validate`.
4. **Run `tessellum composer validate`** on both new skills as the final acceptance gate.
5. **Tests** — run the full suite; existing tests should continue to pass (the new skills are content, not code, so smoke-test count is unchanged).

**Milestone**: Both skills validate cleanly via `tessellum composer validate`, ready for `tessellum composer compile` and (in Wave 4 of the Composer port) real LLM dispatch.

## What we're explicitly NOT porting

- **`acronym_glossary_business`, `_workflows`, `_teams`, `_systems`, `_data_metrics`, `_abuse_networks`** — Amazon-internal in nature; would require rewriting from scratch rather than scrubbing. Public users don't need a glossary of internal team aliases.
- **AB-specific snippet examples** that demonstrate Amazon tools (Cradle pipelines, OTF datasheets, Wasabi, etc.). These can serve as private references in AbuseSlipBox; they don't ship in Tessellum's public vault.
- **`related_skill_headers:` mechanism** with `.claude/skills/` and `.kiro/skills/` thin shims. Tessellum's skill canonicals are self-contained; the multi-ecosystem header pattern is parent-project complexity that Tessellum doesn't need yet.
- **Composer pipeline steps referencing AB-specific scripts** (`update_notes_database.sh`, `bm25_search.py` direct script invocations). Tessellum's CLI subsumes these.

## Migration steps

Execute as **three commits** (one per phase):

### Commit 1 — Phase 1 (templates + capture wiring)
1. Author `template_code_snippet.md` (procedure-BB shape; placeholder content).
2. Author `template_code_repo.md` (model-BB shape; placeholder content).
3. Append `code_snippet` + `code_repo` to `REGISTRY` in `capture.py`.
4. Add tests covering both new flavors.
5. `tessellum capture code_snippet smoke_test_snippet` smoke-test against a fresh tmp vault.
6. Bump v0.0.24, CHANGELOG entry, commit + push.

### Commit 2 — Phase 2 (glossaries)
1. Copy 10 glossaries to `vault/0_entry_points/`.
2. Scrub Amazon-internal references (per-file pass — manual judgment per kept glossary).
3. Validate each via `tessellum format check`.
4. CHANGELOG entry: "v0.0.25 — adds 10 acronym glossaries to seed vault."
5. Commit + push.

### Commit 3 — Phase 3 (skills)
1. Copy + rename both skill canonicals.
2. Copy + rename both sidecars.
3. Scrub Amazon-internal references in skill bodies.
4. Run `tessellum composer validate` on each.
5. CHANGELOG entry: "v0.0.26 — adds tessellum-capture-code-repo-note + tessellum-capture-code-snippet skills."
6. Commit + push.

## Open questions

- **Should `capture` flavor names be `code_repo` (snake_case, matching directory) or `code-repo` (kebab, matching skill name conventions)?** Lean: snake_case for CLI symmetry — `tessellum capture code_repo` matches the existing `tessellum capture concept` etc.
- **Do we ship a `master entry_acronym_glossary.md` index of the 10 kept glossaries?** Lean: yes, small upside, ~30 lines. Decided in Phase 2.
- **Should the snippet template default to `building_block: procedure`** (most common) or omit the field for the user to fill? Lean: default to `procedure` and comment the alternatives in the template.
- **Per-package entry-point pattern for snippets** — port verbatim, or simplify to a single `entry_code_snippets.md` until snippet count justifies splitting? Lean: simplify for v0.1; document the master-TOC pattern as a v0.2+ growth story.
- **Should skill canonicals reference `tessellum search --bm25` or `tessellum search` (default hybrid)?** Lean: `tessellum search` (hybrid) — matches the Tessellum default and hides the ablation flags.

## See Also

- [`plan_composer_port.md`](plan_composer_port.md) — defines the skill-canonical + sidecar format that Phase 3 produces (now complete)
- [`plan_v01_src_tessellum_layout.md`](plan_v01_src_tessellum_layout.md) — defines `vault/resources/templates/` and the `force-include` graft that ships templates in the wheel
- [`plan_retrieval_port.md`](plan_retrieval_port.md) — defines the search CLI the ported skills will use (`tessellum search`, `tessellum filter`)
- AbuseSlipBox source skills: `src/buyer_abuse_slipbox_agent/abuse_slipbox/resources/skills/skill_slipbox_capture_code_*`

---

**Last Updated**: 2026-05-10
**Status**: Active — draft pending user approval, then ships across 3 commits as v0.0.24 / v0.0.25 / v0.0.26.
