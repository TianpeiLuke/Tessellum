---
tags:
  - resource
  - template
  - argument
keywords:
  - argument template
  - argument skeleton
  - claim template
  - thought trail template
  - Folgezettel template
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: argument
folgezettel: ""              # if part of an FZ trail; empty/absent otherwise
folgezettel_parent: ""       # if has a parent in the FZ trail; null for roots; empty/absent for non-trail notes
---

<!--
NOTE ON FOLGEZETTEL FIELDS:
- For trail ROOTS: set `folgezettel: "<root-id>"` (e.g., "7", "10", "14") and
  `folgezettel_parent: null` (or omit).
- For trail CHILDREN: set both `folgezettel: "<id>"` and
  `folgezettel_parent: "<parent-id>"`. Example: `folgezettel: "7b1"` with
  `folgezettel_parent: "7b"`.
- For NON-TRAIL argument notes: omit both FZ fields entirely.
- The canonical key is `folgezettel_parent:` (long form). The shorter
  `fz_parent:` is accepted as an alias but `folgezettel_parent:` is preferred.
-->


# Argument: <Claim, Stated Sharply>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/resources/analysis_thoughts/thought_<topic>.md`.
2. If this argument is part of a Folgezettel trail, add `folgezettel: "<id>"`
   and `fz_parent: "<parent-id>"` to the YAML frontmatter (or `fz_parent: null`
   for trail roots).
3. Update YAML — tags[1] is usually `analysis`.
4. Fill required sections: Claim, Reason, Evidence, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Claiming): an argument note asserts a position with reason
and evidence. It answers "Is the prediction true?" An argument invites a
counter-argument; that's how the dialectic engine works. The strongest arguments
make a single, sharp claim that survives counter-arguments.
-->

## Thesis

<One sentence. The thesis (a.k.a. claim) is the load-bearing assertion this
note makes. It must be specific enough to be falsifiable — vague claims that
everyone already agrees with don't earn an argument note.

Note: in the parent research vault, argument notes commonly title this section
"Thesis"; either "Thesis" or "Claim" is acceptable. Use whichever fits the
register of your note.>

> The thesis is: <state it sharply, in one sentence>.

## Reason

<Why should the reader believe the claim? State the inference structure: from
what premise(s), via what logic, to what conclusion. Aim for 1-3 paragraphs.>

The argument has the following structure:

1. **Premise A**: <state it>
2. **Premise B**: <state it>
3. **Therefore**: <how A + B yield the claim>

<Optionally: name the warrant — the implicit assumption that licenses the move
from premises to claim.>

## Evidence

<What data, observations, or prior arguments support the claim? Distinguish:
- Empirical evidence (link to `empirical_observation` notes)
- Theoretical evidence (link to other arguments or models)
- Authoritative evidence (citations of established work)>

| Evidence | Type | Strength |
|---|---|---|
| <fact / observation> | empirical | strong / medium / weak |
| <prior argument> | theoretical | strong / medium / weak |
| <citation> | authoritative | strong / medium / weak |

## Counter-Arguments Anticipated

<Optional but strongly recommended. What's the strongest objection to this claim?
Steelmanning anticipated counters here makes the argument more robust and gives
future counter-argument notes a target to latch onto. The dialectic engine of
the system depends on counter-arguments existing — make their authoring easier.>

- **Counter A**: <objection> — <how this argument addresses it, or where it's vulnerable>
- **Counter B**: <objection> — <response>

## References

- [Related Argument](thought_related.md) — <how it relates>
- [Related Concept](../term_dictionary/term_related.md)
- [Empirical Observation Cited](thought_or_observation_cited.md)
