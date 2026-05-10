---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - glossary
  - acronyms
keywords:
  - acronyms
  - glossary index
  - terminology reference
  - quick lookup
topics:
  - Navigation
  - Acronyms
  - Glossaries
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Acronym Glossaries — Master Index

A typed-knowledge slipbox accumulates a lot of jargon. This page indexes the per-domain acronym glossaries that ship with Tessellum's seed vault. Each glossary covers one foundational area in depth — pick the one that matches the term you're trying to look up, or scan all of them when you've spotted an unfamiliar acronym whose domain isn't obvious.

## Glossaries

| Glossary | Acronyms | Domain |
| -------- | -------- | ------ |
| [`acronym_glossary_statistics.md`](acronym_glossary_statistics.md) | 54 | Causal inference, Bayesian methods, hypothesis testing, distributions |
| [`acronym_glossary_critical_thinking.md`](acronym_glossary_critical_thinking.md) | 31 | Logic, fallacies, reasoning patterns, argumentation |
| [`acronym_glossary_cognitive_science.md`](acronym_glossary_cognitive_science.md) | 130 | Cognitive biases, dual-process theory, decision heuristics, memory |
| [`acronym_glossary_network_science.md`](acronym_glossary_network_science.md) | 48 | Graph theory, centrality, community detection, network metrics |
| [`acronym_glossary_llm.md`](acronym_glossary_llm.md) | 134 | LLM architectures, training methods, RAG, agents, evaluation |

Total: 5 glossaries, **397 acronyms**. Every entry is a self-contained dictionary record (definition + related terms + sources where applicable). Most entries cross-link with their longer-form `term_*.md` notes in `vault/resources/term_dictionary/` — the glossary is the *index*, the term notes are the *substrate*.

## How to use

- **Looking up a term you don't know**: pick the glossary whose domain matches and `Cmd-F` for the acronym; or run `tessellum search --bm25 <acronym>` from the vault root and read the highest-ranked term note.
- **Adding a new acronym**: edit the matching glossary directly. Each H3 is one acronym. Keep the `**Full Name**: ...`, `**Description**: ...`, `**Related**: [...]` shape.
- **Adding a new domain glossary**: capture via `tessellum capture acronym_glossary <domain>`, populate, then add a row to this index.

## Convention

Each glossary follows the same shape:

```markdown
---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - glossary
  - <domain>
...
---

# <Domain> Glossary

**Purpose**: <one-line>

## <H2 sub-domain>

### <ACRONYM> - <full name>
**Full Name**: <expansion>
**Description**: <2-3 sentences>
**Documentation**: <link to term note in resources/term_dictionary/>
**Related**: [<sibling acronyms>](#anchor)
```

Glossaries are `building_block: navigation` notes — they index without making first-class claims about the domain. The expanded definitions live in `term_*.md` notes; the glossary is the surface that lets you find them.

---

**Last Updated**: 2026-05-10
**Status**: Active — 5 glossaries indexing 397 acronyms
