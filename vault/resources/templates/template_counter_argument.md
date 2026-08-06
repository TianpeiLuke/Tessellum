---
tags:
  - resource
  - template
  - counter_argument
keywords:
  - counter-argument template
  - refutation template
  - dialectic template
  - Folgezettel counter
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-05-10
status: template
building_block: counter_argument
folgezettel: ""              # the counter's own FZ ID; its prefix must be the target argument's FZ ID (parent is derived from the prefix)
---

<!--
NOTE ON FOLGEZETTEL FIELDS:
A counter-argument almost always has a parent — that's the argument it
refutes. In FZ-trail conventions, choose the counter's `folgezettel:` so its
prefix IS the target argument's FZ ID (NOT the parent in the topic graph — the
*argument being refuted*). The parent is DERIVED from that prefix at index
time, so the counter's ID is the next available child ID under the target.

Example: countering FZ 7b (an argument) → counter gets `folgezettel: "7b1"`,
which descends from "7b" by prefix. Subsequent counter-of-counter notes chain
deeper: `folgezettel: "7b1a"` descends from "7b1". This descent is what
TESS-004 enforces — a counter's FZ must be a prefix-extension of the argument
it attacks.

Non-trail counters (rare) omit the `folgezettel:` field.
-->


# Counter: <Counter-Claim, Stated Sharply>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to `vault/resources/analysis_thoughts/counter_<topic>.md`.
2. A counter MUST point at a target — the argument it refutes. Choose
   `folgezettel: "<id>"` for your own ID so that its prefix is the target
   argument's FZ ID; the parent is derived from that prefix, making the
   dialectic chain explicit (TESS-004).
3. Update YAML — tags[1] is usually `analysis`.
4. Fill required sections: Counter-claim, Reason, Strength, References.
5. Remove this commentary block.

EPISTEMIC FUNCTION (Refuting): a counter-argument note disrupts truth-transfer
from an argument. It answers "What are the flaws?" A counter MUST name its
target argument explicitly — counters without a target are decorative.
The strongest counters refute a specific load-bearing claim, not the argument's
overall vibe.

The DKS protocol depends on counters: arguments without counters can't be
sharpened. Authoring a counter is a contribution to the system, not an attack.
-->

## Counter-claim

<One sentence. What's the position this note advances? Must be specific enough
to refute the target without overreaching.>

> The counter-claim is: <state it sharply, in one sentence>.

## Target Argument

<Explicit reference to the argument being refuted. Without this, a counter
note is unmoored.>

This counter refutes: [<Argument Title>](thought_target.md)

The target's load-bearing claim was:

> <Quote or paraphrase the target's claim verbatim>

## Reason

<Which part of the target argument fails? Distinguish:
- **Premise attack**: target's premise A is false / unsupported
- **Warrant attack**: premises don't actually support the conclusion
- **Counter-example**: a case the argument can't accommodate
- **Undercutting**: the argument's evidence is irrelevant or misapplied
- **Scope attack**: the argument is right in scope X but the target overgeneralized

State which attack mode applies, then unpack it.>

**Attack mode**: <premise-attack | warrant-attack | counter-example | undercutting | scope-attack>

<Prose explanation of the refutation, 1-3 paragraphs.>

## Strength

<How strong is this counter? Honest self-assessment matters — overclaiming makes
the dialectic less useful. Distinguish:
- **Decisive**: the target argument cannot survive without changing its claim
- **Strong**: the target needs significant qualification or evidence
- **Moderate**: the target should acknowledge this concern but might survive
- **Weak**: the counter raises a real but bounded issue>

**Strength**: <decisive | strong | moderate | weak>

**What survives if the counter is accepted**: <if the target absorbs this
counter, what does the sharpened argument look like? This sets up the next move
in the dialectic — usually a synthesis or a sharpened argument.>

## References

- [Target Argument](thought_target.md) — what this counters
- [Related Counter](counter_related.md) — sibling counter, if any
- [Evidence cited](evidence_or_observation.md)
