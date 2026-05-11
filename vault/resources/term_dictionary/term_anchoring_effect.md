---
tags:
  - resource
  - terminology
  - cognitive_science
  - behavioral_economics
  - cognitive_bias
keywords:
  - anchoring effect
  - anchoring bias
  - cognitive bias
  - heuristic
  - decision making
  - behavioral economics
topics:
  - cognitive science
  - behavioral economics
  - decision making
language: markdown
date of note: 2026-04-16
status: active
building_block: concept
---

# Anchoring Effect

## Definition

The anchoring effect is a cognitive bias where individuals rely too heavily on the first piece of information encountered (the "anchor") when making subsequent judgments or decisions. Once an anchor is set, adjustments from that anchor tend to be insufficient, leading to systematically biased estimates. In abuse prevention, anchoring can affect both investigators (anchoring on initial risk scores) and ML model design (anchoring on historical thresholds).

## Context

- **Investigation bias**: ARI investigators may anchor on initial risk band or sugar index when evaluating cases
- **Threshold setting**: ML model operating points can anchor on historical precision/recall targets
- **Customer behavior**: Abusers may exploit anchoring by establishing a pattern of legitimate behavior before abuse
- **Experimental design**: A/B test interpretation can be anchored by prior expectations

## Key Characteristics

- **First-information dominance**: Initial values disproportionately influence final judgments
- **Insufficient adjustment**: People adjust away from anchors but not enough
- **Ubiquitous**: Affects experts and novices alike, even when anchors are arbitrary
- **Mitigation**: Awareness, structured decision frameworks, multiple independent assessments

## Related Terms

- **[Sugar Index](term_sugar_index.md)**: Customer risk score — can serve as anchor for investigators
- **[Precision](term_precision.md)**: Model precision — threshold anchoring in ML
- **[ARI](term_ari.md)**: Investigators subject to anchoring bias
- **[SOP](term_sop.md)**: Structured procedures that help mitigate anchoring

## References

- [Wikipedia: Anchoring](https://en.wikipedia.org/wiki/Anchoring_(cognitive_bias))
