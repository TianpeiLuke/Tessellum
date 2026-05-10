---
tags:
  - resource
  - terminology
  - knowledge_management
  - organization
  - tessellum_core
keywords:
  - PARA
  - Projects Areas Resources Archives
  - Tiago Forte
  - Building a Second Brain
  - knowledge organization
  - actionability
topics:
  - Knowledge Management
  - Personal Knowledge Management
  - Note Organization
language: markdown
date of note: 2026-05-09
status: active
building_block: concept
---

# Term: PARA Method

## Definition

**PARA** is an organizational method for personal knowledge management coined by [Tiago Forte](https://fortelabs.com) in 2017 ([*Building a Second Brain*](https://www.buildingasecondbrain.com), 2022). The acronym stands for the four top-level categories every piece of digital knowledge belongs in:

- **P** — **Projects**: short-term efforts with a defined end and outcome ("Ship v0.1 of Tessellum")
- **A** — **Areas**: ongoing responsibilities with no end date ("Maintain the unified backend")
- **R** — **Resources**: topics or themes of interest, reference material ("PageRank algorithm", "MCP protocol spec")
- **A** — **Archives**: items from the other three categories that are no longer active

The defining principle is **organizing by actionability, not by topic**. Two notes about "machine learning" might live in different PARA categories — a *project* note ("ML model launch checklist for Q3") versus a *resource* note ("ML algorithm survey") — because actionability differs even when topic is identical.

## Why PARA Matters for Tessellum

PARA is the **second pillar** of Tessellum's six-pillar architecture (Z + **PARA** + BB + Epistemic Function + DKS + CQRS). It provides the *organizational scheme* — the four-fold layer that governs **where a note lives in the directory tree**, distinct from the [Building Block](term_building_block.md) layer that governs **what type the note is** and the [Folgezettel](term_folgezettel.md) layer that governs **how trails connect**.

The three layers are orthogonal:
- A `procedure` BB note (the "what") about "deploying Tessellum" (the "topic") becomes a Project note when actively running, an Archive note when complete.
- A `concept` BB note (the "what") about "PageRank" (the "topic") is always a Resource — it's reference material, not bound to any single project.
- An `argument` BB note can sit in either Projects/ (if it's the load-bearing argument of a current paper draft) or Resources/ (if it's a stable architectural claim).

## The Four Categories in Detail

### Projects

**Definition**: short-term, time-bound, outcome-defined efforts. A project has a clear endpoint at which it succeeds or fails.

**Tessellum convention**: `vault/projects/<project-slug>/` — one subdirectory per project. The project's notes (kickoff, milestones, retrospective) all live in this subdirectory. When the project ends, the directory moves to `vault/archives/projects/<project-slug>/` or stays in place with status `archived`.

**Examples**:
- "Ship Tessellum v0.1 public beta"
- "Migrate retrieval backend to sqlite-vec"
- "Author the AMLC research paper"

### Areas

**Definition**: ongoing responsibilities with no defined end. Areas describe roles, capabilities, or domains you maintain over time.

**Tessellum convention**: `vault/areas/<area-slug>/` — one subdirectory per area of responsibility. Areas accumulate domain knowledge (code repos you own, models you maintain, datasets you steward).

**Examples**:
- "Code repos I maintain" → `vault/areas/code_repos/`
- "Tools I administer" → `vault/areas/tools/`
- "Teams I'm responsible to" → `vault/areas/teams/`

### Resources

**Definition**: topics, themes, or domains of interest — reference material useful across multiple projects and areas.

**Tessellum convention**: `vault/resources/<category>/` — typed by content category. The bulk of a typed-knowledge vault lives here:
- `vault/resources/term_dictionary/` — concept BB notes (definitions)
- `vault/resources/how_to/` — procedure BB notes
- `vault/resources/analysis_thoughts/` — argument / counter / hypothesis BB notes (often forming Folgezettel trails)
- `vault/resources/skills/` — skill canonical bodies
- `vault/resources/papers/` — digested literature
- `vault/resources/code_snippets/` — reusable code components

### Archives

**Definition**: items from the other three categories that are no longer active. Archiving preserves the history without cluttering active workspace.

**Tessellum convention**: `vault/archives/<subcategory>/` — typed by archive subcategory:
- `vault/archives/experiments/` — past experiment results
- `vault/archives/projects/` — completed projects
- `vault/archives/launch_announcements/` — past announcements

The archive layer is **not deletion**. Archive notes remain searchable and cite-able; they just don't surface in active retrieval rankings (lower PageRank weight, deprioritized in graph traversal).

## The Decision Rule

Tiago Forte's actionability principle gives a single decision rule for placing a new note:

| If the note... | Goes in |
|---|---|
| Is needed for an active, time-bound effort | **Projects** |
| Describes an ongoing responsibility you maintain | **Areas** |
| Is reference material useful across projects/areas | **Resources** |
| Is no longer active | **Archives** |

A note's placement can **change over time** as actionability shifts — a Resource (reference) might get pulled into a Project (active use) and then return to Resources (or move to Archives if the project's done with it).

## How PARA Differs From Topic-Based Organization

Topic-based organization (the default in most note-taking tools) groups notes by *what they are about*. PARA groups by *how actionable they are*. The difference matters because:

- **Topic-based orgs scale poorly** — a note about "Python" might appear in 30 different projects, areas, and resources. Where does it live?
- **Actionability-based orgs scale gracefully** — the *Python project* lives under Projects (or Archives if done); the *Python language reference* lives under Resources; *the Python codebase you maintain* lives under Areas.

Topic-based organization conflates *content* with *context*. PARA separates them. The Building Block ontology then governs *content* (what type of knowledge); PARA governs *context* (how is it being used).

## How Tessellum Implements PARA

The `vault/` directory has exactly four top-level content categories (plus one navigation category):

```
vault/
├── 0_entry_points/    # Navigation layer (Master TOC, per-surface entries)
├── projects/          # P
├── areas/             # A
├── resources/         # R
├── archives/          # A
└── examples/          # Worked examples (kept distinct from Resources for discoverability)
```

The category prefix `0_` on entry points keeps them at the top of any sorted listing — they're the "you are here" layer that helps a reader navigate the other four.

## Related

- [Term: Zettelkasten](term_zettelkasten.md) — PARA's organizational complement; Zettelkasten governs note structure, PARA governs note placement
- [Term: Building Block](term_building_block.md) — the type taxonomy orthogonal to PARA
- [Term: Folgezettel](term_folgezettel.md) — trail structure orthogonal to both
- [Term: Slipbox](term_slipbox.md) — the parent system class
- [DEVELOPING.md](../../../DEVELOPING.md) — how Tessellum's directory layout maps to PARA

## References

- Forte, T. (2017). *The PARA Method: A Universal System for Organizing Digital Information*. [fortelabs.com/blog/para](https://fortelabs.com/blog/para)
- Forte, T. (2022). *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*. Profile Books.
- The PARA acronym is sometimes also rendered as PARA = Projects, Areas, Resources, Archives — order is canonical (Projects first because they're the most actionable; Archives last because they're inactive).
