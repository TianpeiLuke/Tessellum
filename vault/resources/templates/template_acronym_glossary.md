---
tags:
  - entry_point
  - template
  - index
  - navigation
  - quick_reference
  - glossary
keywords:
  - acronym glossary template
  - glossary template
  - quick lookup
  - acronym index
  - terminology reference
topics:
  - Note Format
  - Templates
  - Acronym Glossaries
language: markdown
date of note: 2026-05-10
status: template
building_block: navigation
---

# <Domain> Glossary

<!--
HOW TO USE THIS TEMPLATE:

This template is for ACRONYM GLOSSARY notes — surfaces that index ALL term
notes in the vault (or a domain subset of them) via their acronyms. The
vault's acronym glossary covers every term note; whenever a term note exists,
its acronym should appear in some glossary.

TWO USAGE PATTERNS:

  A. SINGLE MASTER (small vault, < 50 terms):
     - One file: `vault/0_entry_points/acronym_glossary.md`
     - Indexes EVERY term note in the vault, organized by topical sections
     - Use this template — fill all topical sections inline

  B. PARTITIONED (large vault, > 50 terms — recommended):
     - Multiple per-field files: `vault/0_entry_points/acronym_glossary_<field>.md`
       (e.g., `acronym_glossary_ml.md`, `acronym_glossary_security.md`,
       `acronym_glossary_statistics.md`)
     - Plus one master `vault/0_entry_points/entry_acronym_glossary.md` that
       AGGREGATES the per-field sub-glossaries (uses template_entry_point.md
       — it's just an index of indexes)
     - Each sub-glossary uses THIS template, scoped to one field
     - Per-acronym entries live in the relevant sub-glossary, not the master

The collective union of all per-field sub-glossaries MUST cover every term
note in the vault. An acronym appearing in a term note but in NO glossary is
a vault-health issue (run a coverage check periodically).

INSTRUCTIONS:
1. Pick pattern A or B based on vault size.
2. Copy this file to:
     A → `vault/0_entry_points/acronym_glossary.md`
     B → `vault/0_entry_points/acronym_glossary_<field>.md` per sub-glossary
3. Update YAML:
   - tags[0]=entry_point, tags[1]=index, plus `navigation`, `quick_reference`,
     `glossary`, and a domain tag (e.g., `machine_learning`).
   - building_block: navigation
4. Fill the body. The pattern: Purpose + back-link header → topical sections →
   per-acronym entries (using `### ACRONYM` H3 with structured sub-fields).
5. Remove this commentary block.

EPISTEMIC FUNCTION (Indexing): an acronym glossary is a specialized entry point
that maps acronyms to their expansions and term-note documentation. It's a
quick-lookup surface — the reader knows the acronym, wants the definition + a
pointer to the deeper term note.

Distinction from related templates:
  - `template_entry_point.md` — for the MASTER `entry_acronym_glossary.md` in
    pattern B (it's just an entry point listing the sub-glossaries; doesn't
    have per-acronym entries itself).
  - This template (`template_acronym_glossary.md`) — for both:
      • the single `acronym_glossary.md` in pattern A
      • the per-field `acronym_glossary_<field>.md` files in pattern B
    Both have per-acronym `### ACRONYM` entries.

The repeating ### entry pattern is the load-bearing structure: each acronym
gets exactly one ### heading + four sub-fields (Full Name / Description /
Documentation / Related). This makes the glossary scannable and the format
machine-parseable for export to other glossary surfaces.
-->

# <Domain> Glossary

**Purpose**: Quick reference for <domain> acronyms, terms, and abbreviations used in <project context>. Indexes every term note in `vault/resources/term_dictionary/` whose subject matter falls under <domain>.

**Navigation**: ← Back to Main Glossary <!-- pattern B; remove this line in pattern A -->

## <Section A — Primary Topical Group>

<Group acronyms by topical sub-area. Common groupings:
- By stack layer (data / models / serving / monitoring)
- By methodology (algorithms / metrics / techniques)
- By workflow phase (training / evaluation / deployment)
- Alphabetical (only for very large glossaries)

Each acronym gets its own ### entry following the structured format below.>

### ACRONYM-1
**Full Name**: <Full expansion of the acronym>
**Description**: <1-3 sentences explaining what it is and why it matters in this domain. Use **bold** for the load-bearing claim or definition.>
**Documentation**: <Term Note Title>
**Related**: [Related Acronym](#related-acronym), Other Term

### ACRONYM-2
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: <Term Note Title>
**Related**: [Related Acronym](#related-acronym)

### ACRONYM-3
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: <Term Note Title>
**Related**: [Related Acronym](#related-acronym)

## <Section B — Secondary Topical Group>

<Continue with another topical sub-area. Same per-acronym pattern.>

### ACRONYM-4
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: <Term Note Title>
**Related**: <links>

## Quick Reference Table

<Optional but valuable for glossaries with > 20 entries. A flat table that
compresses the per-acronym detail into one scannable view.>

| Acronym | Full Name | Documentation |
|---|---|---|
| ACRONYM-1 | <full name> | term_topic |
| ACRONYM-2 | <full name> | term_topic |
| ACRONYM-3 | <full name> | term_topic |

## Search Tips

<Optional. Help readers find acronyms when they don't remember the exact
spelling or section. Common patterns:
- "Use Ctrl-F for the acronym you remember"
- "If you don't know the domain, start with the Main Glossary"
- "For full definitions and context, follow the Documentation links to term notes">

- Use Ctrl-F to search this page for an acronym.
- For full context and related concepts, follow the **Documentation** link on each entry to the corresponding term note in `vault/resources/term_dictionary/`.
- For acronyms not in this glossary, check the Main Glossary which lists all domain glossaries.

## Coverage Promise

<Optional but recommended for vaults using pattern B (partitioned glossaries).
State explicitly which term notes this sub-glossary covers, so the union of
all sub-glossaries provably covers every term note.>

This sub-glossary covers term notes in `vault/resources/term_dictionary/`
matching: <criteria — e.g., "all terms tagged with `machine_learning` or
`deep_learning`">.

Term notes outside this scope live in:
- acronym_glossary_<related> — <criteria>
- acronym_glossary_<related> — <criteria>

## Related Entry Points

- Main Glossary — master index aggregating all per-field sub-glossaries (pattern B); omit this row if you're using pattern A
- Related Glossary A — <related domain>
- Related Glossary B — <related domain>
- [Term Dictionary](../resources/term_dictionary/) — the underlying term notes this glossary indexes

## References

<Optional. Include sources for acronyms and definitions when authoritative
references exist.>

- <Author, Year, Title, URL>
- <External standard or specification>

---

**Last Updated**: YYYY-MM-DD
**Status**: Active — <count> acronyms indexed
