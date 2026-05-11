---
tags:
  - resource
  - template
  - concept
keywords:
  - concept template
  - concept skeleton
  - note format
  - building block concept
  - term note template
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: concept
---

# Term: <Concept Name>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy this file to the appropriate vault subdirectory.
   Most concept notes live in `vault/resources/term_dictionary/term_<your-topic>.md`.
2. Rename the file (filename should be `term_<lowercase_underscored>.md`).
3. Update YAML frontmatter:
   - tags[1] is usually `terminology` (for term-dictionary entries) but can be other open
     values like `metric`, `signal`, etc.
   - tags[2..] should describe the topic in lowercase underscore form
   - keywords ≥ 3, topics ≥ 2, all lowercase
   - date of note = today; status = active
4. Fill the H2 sections below. Required: Definition, Examples, References.
5. Remove this <!-- HOW TO USE --> commentary block.
6. Run `python scripts/check_note_format.py --path <your-file.md>` before committing.

EPISTEMIC FUNCTION (Naming): a concept note defines a thing — gives it a label
and boundaries. It answers "What is it called?" One concept per note. The
defining feature is that the term, once named, can be referenced from other notes.
-->

## Definition

<One-paragraph precise definition. State what the concept IS. Avoid hedging — if
the concept is contested, state the contested status explicitly and pick the
definition this note uses.>

<Optionally: a 1-2 sentence framing of why the concept matters or what problem
it solves.>

## Key Properties

<3-7 bullet points capturing what's essential about the concept. This is the
section a reader scans to verify understanding. Each property should be either
a defining characteristic (something true of every instance) or a load-bearing
implication (something the concept enables / forces).>

- <**Property 1**: brief explanation>
- <**Property 2**: brief explanation>
- <**Property 3**: brief explanation>

## Examples

<2-4 concrete examples. Examples make the concept tangible — abstract definitions
without examples often fail to land. Each example should clearly satisfy the
definition above.>

- **Example 1**: <description>
- **Example 2**: <description>
- **Example 3**: <description>

## See Also

<Cross-references to closely related but distinct concepts. Use this section
for "if you understood X, you might also want to know about Y" relations.>

- Related Term A — <how it relates>
- Related Term B — <how it relates>

## References

<Required. Cite the sources of the definition + any background readings.>

- <Author, Year, Title, Publisher / URL>
- <Cross-reference to a digest note in `vault/resources/digest/` if applicable>
