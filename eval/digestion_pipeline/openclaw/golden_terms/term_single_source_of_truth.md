---
tags:
  - resource
  - terminology
  - software_engineering
  - data_modeling
  - architecture
keywords:
  - Single Source of Truth
  - SSOT
  - single source of truth
  - canonical source
  - authoritative source
  - source of record
topics:
  - software architecture
  - data modeling
  - configuration management
language: markdown
date of note: 2026-06-27
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# SSOT - Single Source of Truth

## Definition

**Single Source of Truth (SSOT)** is the architectural principle that every piece of data, configuration, or definition in a system should have exactly **one authoritative, canonical place where it is defined**, with all other usages derived from (referencing, projecting, or generated off) that one source rather than independently re-declaring it. When a fact lives in only one place, updating it there propagates everywhere consistently; when the same fact is duplicated across multiple locations, the copies drift, contradict each other, and create a class of bugs where "the system disagrees with itself."

SSOT is the structural counterpart to the **DRY (Don't Repeat Yourself)** principle: DRY says *don't duplicate knowledge*, and SSOT names *the one place the knowledge should live*. It applies to source code (one definition of a type or constant), data systems (one authoritative table or registry for an entity), and configuration (one config file or registry that downstream artifacts are generated from). A violation of SSOT is typically diagnosed as a maintenance hazard — two or more sources that must be kept in sync by hand and will eventually diverge.

## Key Characteristics

- **One authoritative definition**: exactly one canonical location declares each fact; everything else references or is generated from it.
- **Derivation over duplication**: downstream artifacts (code, config, docs, indexes) are *generated* or *projected* from the source, never hand-copied.
- **Drift elimination**: because there is no second copy to fall out of sync, whole classes of "the copies disagree" bugs become structurally impossible.
- **Single point of update**: a change is made once at the source and propagates; this is what makes the system maintainable at scale.
- **DRY's structural form**: SSOT is how the DRY principle is realized for data/config/definitions, not just code logic.
- **Common realizations**: a canonical registry (e.g., a step-names YAML, a tool registry), a system of record table, a single config file, or a generated-from-source build step.
- **Violation smell**: any place where two artifacts "must be kept in sync manually" is an SSOT violation and a candidate for consolidation.

## Related Terms


## References

- [Single source of truth (Wikipedia)](https://en.wikipedia.org/wiki/Single_source_of_truth)
- [Don't repeat yourself (Wikipedia)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
