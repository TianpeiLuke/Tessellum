---
tags:
  - resource
  - terminology
  - gen_ai_dev
  - software_development
  - ai_paradigm
keywords:
  - vibe coding
  - natural language programming
  - AI-dependent programming
  - prompt-driven development
  - code generation
  - NL to code
topics:
  - AI-assisted development
  - programming paradigms
  - code generation
language: markdown
date of note: 2026-05-17
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Vibe Coding - Natural Language AI-Dependent Programming Paradigm

## Definition

**Vibe coding** is an AI-dependent programming paradigm where developers describe problems in natural language prompts to large language models, which then generate software code. The programmer's role shifts from manual coding to guiding, testing, and refining AI-generated code. While this approach can accelerate development and prototyping, it requires careful review and understanding of generated code to avoid introducing bugs, security vulnerabilities, or standards violations.

The term is still evolving in the developer community with multiple interpretations: some view it as rapid prototyping, others see it as potentially sacrificing code quality for speed, while others consider it part of a balanced workflow with proper verification through human-in-the-loop practices.

## Context

- **Contrast with spec-driven development**: Vibe coding = unstructured NL prompts; Spec-driven = structured specifications with EARS format, design docs, task breakdowns
- **Tools enabling vibe coding**: Claude Code, Cline (Act mode) — all accept natural language descriptions
- **Risk profile**: Higher for production code (hallucinations, security issues); acceptable for prototyping/exploration

## Key Characteristics

- **Natural language input**: Developer describes desired functionality in conversational English rather than writing code directly
- **Rapid iteration**: Low regeneration cost means quickly trying different approaches
- **Reduced typing**: Developer focuses on "what" not "how"
- **Quality risks**:
  - Overcomplicating (agent adds unrequested features)
  - Defensive coding (catches errors instead of failing appropriately)
  - Lack of refactoring (bloat from additions rather than restructuring)
  - Misleading output (claims completion when build fails)
- **Best practices**:
  - Use for prototyping, exploration, learning — not blindly for production
  - Combine with testing (TDD approach recommended)
  - Start fresh sessions for new tasks (avoid context drift)
  - Work in small units (large imprecise tasks → hallucinations)
  - Review output carefully before committing
- **Complementary approach**: Spec-driven development provides the structure that pure vibe coding lacks

## Related Terms


## References

