---
tags:
  - resource
  - terminology
  - llm
  - agentic_ai
  - agent_skills
  - context_engineering
  - prompt_engineering
keywords:
  - progressive disclosure
  - on-demand skill loading
  - skills_list
  - skill_view
  - token efficiency
  - context window management
  - agentskills.io
topics:
  - Large Language Models
  - Agentic AI Architecture
  - Context Window Management
  - Agent Skills
language: markdown
date of note: 2026-06-15
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://agentskills.io/specification
---

# Progressive Disclosure

## Definition

**Progressive disclosure** is a token-efficiency pattern for loading agent **skills** (on-demand knowledge documents) in tiers, so that an LLM agent reads only the minimal information it needs at each step instead of pulling every skill's full content into its context window up front. At startup the agent sees only a lightweight index of skill names and descriptions; it loads a skill's full body only after it decides the skill is relevant to the task; and it loads bundled reference files, scripts, or assets only when a specific sub-task calls for them. The Anthropic engineering team describes the pattern by analogy to "a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix" — the agent never reads the whole manual to answer one question.

The core motivation is the finite, contended nature of the [context window](term_context_window.md): every token spent on skill instructions the agent does not currently need is a token unavailable for the actual task, and excess context degrades attention. By deferring the bulk of a skill's payload until it is provably needed, progressive disclosure lets a skill library scale to an effectively unbounded amount of bundled material while keeping each turn's prompt small. It is the loading discipline codified by the [agentskills.io](https://agentskills.io/specification) open standard and implemented by skill systems in Hermes Agent, Claude Code, and similar agent harnesses.

## Context

Progressive disclosure is the loading contract of the Hermes Agent **skills system** (documented in `hermes_skills_system`) and is shared, near-identically, with [Claude Code](term_claude_code.md)'s skills and the cross-vendor [agentskills.io](https://agentskills.io/specification) specification. In Hermes it manifests as a three-call ladder over the `skills` toolset:

- **Level 0 — `skills_list()`**: returns `[{name, description, category}, ...]` for every installed skill (~3k tokens in Hermes; ~100 tokens per skill in the agentskills.io spec, since only `name` + `description` frontmatter are surfaced). This index is what the agent scans to recognize a relevant skill.
- **Level 1 — `skill_view(name)`**: loads the full `SKILL.md` body (instructions, recommended under ~5000 tokens / ~500 lines) once the agent has decided the skill applies.
- **Level 2 — `skill_view(name, path)`**: loads a specific bundled reference file (`references/`, `scripts/`, `assets/`) only when that sub-task demands it.

The pattern is invoked every time an agent uses a slash command (`/plan`, `/gif-search`) or natural-language skill request, and it underpins the secure-setup-on-load and conditional-activation behaviors of the [skill manifest](term_skill_manifest.md). It sits alongside the broader discipline of [context engineering](term_context_engineering.md): where context engineering governs *what* assembled information reaches the model, progressive disclosure governs *when* skill knowledge is paged in. Note it is unrelated to *progressive summarization* (a context-compaction technique) despite the similar name.

## Key Characteristics

- **Tiered, lazy loading.** Three escalating levels — metadata index → full body → bundled resources — each loaded only when the prior level signals a need. Mirrors lazy evaluation / lazy loading in software.
- **Metadata always resident.** Skill `name` + `description` are pre-loaded into the system prompt at session start for *all* skills (the always-in-context tier); everything heavier is deferred.
- **Bounded per-turn cost, unbounded library size.** Because most of a skill's bytes live behind Level 1/2, the total knowledge a skill can bundle is effectively unbounded while the standing context cost stays roughly constant in the number of skills.
- **Filesystem- and tool-mediated.** The deeper tiers are read via file-reading and code-execution tools; scripts can even run without their source ever entering context.
- **Agentic decision point.** The agent itself decides when to escalate a level, based on the description match — a model-driven routing choice rather than a static include.
- **Standard-aligned.** Codified by the agentskills.io specification (recommend ≤500-line `SKILL.md`, reference files one level deep) and implemented by Hermes, Claude Code, and other harnesses for portability.
- **Token-budget rationale.** Directly reduces prompt token usage and attention dilution, a concern shared with [prompt caching](term_prompt_caching.md) and other context-window optimizations.

## Related Terms


## References

- [Hermes Agent — Skills System (Progressive Disclosure)](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
- [agentskills.io — Specification (Progressive Disclosure, SKILL.md format)](https://agentskills.io/specification)
- [Anthropic Engineering — Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude — Introducing Agent Skills](https://claude.com/blog/skills)
