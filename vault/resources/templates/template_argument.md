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
folgezettel: ""              # if part of an FZ trail; empty/absent otherwise. Parent is derived from the ID's prefix (e.g. "7b1" descends from "7b")
argument_perspective: ""     # optional: the perspective this argument was generated from (e.g. "conservative", "exploratory", "empirical"). Open vocabulary. Phase 10+.
---

<!--
NOTE ON FOLGEZETTEL FIELDS:
- For trail ROOTS: set `folgezettel: "<root-id>"` (e.g., "7", "10", "14"). A
  single-segment ID is a root and has no parent.
- For trail CHILDREN: set `folgezettel: "<id>"`. The parent is DERIVED from the
  ID's prefix at index time — do NOT author it. Example: `folgezettel: "7b1"`
  descends from "7b" (which descends from "7") by prefix.
- For NON-TRAIL argument notes: omit the `folgezettel:` field entirely.
- Only `folgezettel:` is authored. There is no `folgezettel_parent:`/`fz_parent:`
  YAML field — the parent is computed from the prefix, and a stray one is
  flagged TESS-002.
-->


# Argument: <Claim, Stated Sharply>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/resources/analysis_thoughts/thought_<topic>.md`.
2. If this argument is part of a Folgezettel trail, add `folgezettel: "<id>"`
   to the YAML frontmatter. The parent is derived from the ID's prefix — a
   single-segment ID (e.g., "7") is a root with no parent.
3. Update YAML — tags[1] is usually `analysis`.
4. Fill required sections: Claim, Reason, Evidence, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Claiming): an argument note asserts a position with reason
and evidence. It answers "Is the prediction true?" An argument invites a
counter-argument; that's how the dialectic engine works. The strongest arguments
make a single, sharp claim that survives counter-arguments.
-->

## Claim

<One sentence. The claim (a.k.a. thesis) is the load-bearing assertion this
note makes. It must be specific enough to be falsifiable — vague claims that
everyone already agrees with don't earn an argument note.

Note: "Claim" is the BB_SPECS contract header for argument notes; "Thesis" is
an accepted synonym in prose if it fits your register, but keep the H2 as
"Claim" so the note satisfies the building-block section contract.>

> The claim is: <state it sharply, in one sentence>.

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
