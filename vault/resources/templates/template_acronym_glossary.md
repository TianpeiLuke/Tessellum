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
1. Copy to `vault/0_entry_points/acronym_glossary_<domain>.md`. Acronym
   glossaries ALWAYS live in `0_entry_points/` (they're a kind of entry point
   indexing terms-by-acronym).
2. Filename convention: `acronym_glossary_<domain>.md` (e.g.,
   `acronym_glossary_ml.md`, `acronym_glossary_statistics.md`,
   `acronym_glossary_security.md`).
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

Distinction from `template_entry_point.md`: regular entry points index NOTES;
acronym glossaries index ACRONYMS (each acronym entry is a small structured
record, not just a link). Acronym glossaries also typically link BACK to a
master `entry_acronym_glossary.md` that aggregates them.

The repeating ### entry pattern is the load-bearing structure: each acronym
gets exactly one ### heading + four sub-fields (Full Name / Description /
Documentation / Related). This makes the glossary scannable and the format
machine-parseable for export to other glossary surfaces.
-->

# <Domain> Glossary

**Purpose**: Quick reference for <domain> acronyms, terms, and abbreviations used in <project context>.

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md)

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
**Documentation**: [<Term Note Title>](../resources/term_dictionary/term_<topic>.md)
**Related**: [Related Acronym](#related-acronym), [Other Term](../resources/term_dictionary/term_other.md)

### ACRONYM-2
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: [<Term Note Title>](../resources/term_dictionary/term_<topic>.md)
**Related**: [Related Acronym](#related-acronym)

### ACRONYM-3
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: [<Term Note Title>](../resources/term_dictionary/term_<topic>.md)
**Related**: [Related Acronym](#related-acronym)

## <Section B — Secondary Topical Group>

<Continue with another topical sub-area. Same per-acronym pattern.>

### ACRONYM-4
**Full Name**: <Full expansion>
**Description**: <description>
**Documentation**: [<Term Note Title>](../resources/term_dictionary/term_<topic>.md)
**Related**: <links>

## Quick Reference Table

<Optional but valuable for glossaries with > 20 entries. A flat table that
compresses the per-acronym detail into one scannable view.>

| Acronym | Full Name | Documentation |
|---|---|---|
| ACRONYM-1 | <full name> | [term_topic](../resources/term_dictionary/term_topic.md) |
| ACRONYM-2 | <full name> | [term_topic](../resources/term_dictionary/term_topic.md) |
| ACRONYM-3 | <full name> | [term_topic](../resources/term_dictionary/term_topic.md) |

## Search Tips

<Optional. Help readers find acronyms when they don't remember the exact
spelling or section. Common patterns:
- "Use Ctrl-F for the acronym you remember"
- "If you don't know the domain, start with the [Main Glossary](entry_acronym_glossary.md)"
- "For full definitions and context, follow the Documentation links to term notes">

- Use Ctrl-F to search this page for an acronym.
- For full context and related concepts, follow the **Documentation** link on each entry to the corresponding term note in `vault/resources/term_dictionary/`.
- For acronyms not in this glossary, check the [Main Glossary](entry_acronym_glossary.md) which lists all domain glossaries.

## Related Entry Points

- [Main Glossary](entry_acronym_glossary.md) — index of all domain glossaries
- [Related Glossary A](acronym_glossary_<related>.md) — <related domain>
- [Related Glossary B](acronym_glossary_<related>.md) — <related domain>

## References

<Optional. Include sources for acronyms and definitions when authoritative
references exist.>

- <Author, Year, Title, URL>
- <External standard or specification>

---

**Last Updated**: YYYY-MM-DD
**Status**: Active — <count> acronyms indexed
