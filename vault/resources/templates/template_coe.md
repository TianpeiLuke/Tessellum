---
tags:
  - resource
  - template
  - coe
keywords:
  - coe template
  - correction of error
  - postmortem skeleton
  - note format
topics:
  - Note Format
  - Templates
language: markdown
date of note: 2026-07-26
status: template
building_block: empirical_observation
---

# CoE: <Incident / error in one line>

<!--
HOW TO USE THIS TEMPLATE:
1. Copy to vault/resources/analysis_thoughts/coe_<lowercase_underscored>.md.
2. Rename the file; set tags[1]=coe, add domain tags; keywords >=3, topics >=2.
3. date of note = today; status = active.
4. Fill the sections. Required (per BB_SPECS[empirical_observation]): Observation, Method, Result, References.
   For a CoE these read as: Observation = incident summary; Method = timeline + root-cause
   analysis; Result = corrective actions + prevention + key lesson.
5. Remove this HOW TO USE block.
6. Run `tessellum format check --path <your-file.md>` before committing.

EPISTEMIC FUNCTION (Testing, empirical_observation BB): a CoE records what
happened and what it teaches. It is evidence — an observed failure + its analysis.
-->

## Observation

<Incident summary: what went wrong, impact, and blast radius, in 1-3 sentences.>

## Method

<Timeline of events with timestamps (detection, diagnosis, mitigation, resolution),
then the root-cause analysis — distinguish trigger from underlying cause (5-whys).>

## Result

<Corrective actions taken + the durable prevention (a gate, test, guardrail, or
process change) + the one transferable Key Lesson so a future reader avoids it.>

## References

<Link ALL genuinely-relevant content notes — the affected system/skill/script,
related CoEs (completeness by relevance, exclude entry-point hubs), each with a
one-line relationship gloss.>
