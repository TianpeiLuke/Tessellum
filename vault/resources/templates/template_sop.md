---
tags:
  - resource
  - template
  - sop
keywords:
  - sop template
  - standard operating procedure
  - procedure skeleton
  - note format
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-07-26
status: template
building_block: procedure
---

# SOP: <Standard operating procedure name>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to vault/resources/policy_sops/sop_<lowercase_underscored>.md.
2. Rename the file; set tags[1]=sop, add topic tags; keywords >=3, topics >=2.
3. date of note = today; status = active.
4. Fill the sections. Required (per BB_SPECS[procedure]): Setup, Steps, Validation, References.
5. Remove this HOW TO USE block.
6. Run `tessellum format check --path <your-file.md>` before committing.

EPISTEMIC FUNCTION (Doing, procedure BB): an SOP operationalizes a policy into a
repeatable procedure. One procedure per note; steps must be executable + verifiable.
-->

## Setup

<Purpose + scope of the SOP, and what must be in place before starting —
prerequisites, access, roles, preconditions.>

## Steps

<Numbered, imperative steps. Exact commands in fenced code blocks; note expected
output. Split a long procedure into sub-headed phases if needed.>

## Validation

<How to confirm the SOP was executed correctly — the expected end state, a check
command, and the escalation path if a step fails.>

## References

<Link ALL genuinely-relevant term/tool/related-SOP notes (completeness by
relevance, exclude entry-point hubs), each with a one-line relationship gloss.>
