---
tags:
  - resource
  - terminology
  - software_architecture
  - modularity
  - software_engineering
keywords:
  - connascence
  - coupling
  - modularity
  - dependency strength
  - Meilir Page-Jones
  - static connascence
  - dynamic connascence
topics:
  - Software Architecture
  - Modularity Metrics
  - Software Engineering
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Connascence

## Definition

**Connascence** is a software quality metric introduced by Meilir Page-Jones in *What Every Programmer Should Know About Object-Oriented Design* (1996) that describes the strength and type of dependency between software components. Two components are connascent if a change in one requires a corresponding change in the other to maintain system correctness. Unlike simple coupling measures (afferent/efferent counts), connascence provides a **9-type taxonomy** organized from weakest (most desirable) to strongest (most problematic), split into static (compile-time) and dynamic (runtime) categories. Richards and Ford adopt connascence in *Fundamentals of Software Architecture* as a richer modularity metric than coupling alone.

## Taxonomy

### Static Connascence (Detectable at Compile Time)

| Type | Description | Example | Strength |
|------|-------------|---------|----------|
| **Name** | Components agree on a name | Method name, variable name | Weakest |
| **Type** | Components agree on a data type | Parameter types, return types | Weak |
| **Meaning** | Components agree on value semantics | `true` = enabled, `1` = active | Moderate |
| **Position** | Components agree on parameter order | Function argument ordering | Moderate |
| **Algorithm** | Components agree on a computation | Same hashing algorithm on both sides | Strong |

### Dynamic Connascence (Detectable Only at Runtime)

| Type | Description | Example | Strength |
|------|-------------|---------|----------|
| **Execution** | Components must execute in a specific order | Init before use, open before read | Moderate |
| **Timing** | Components depend on execution timing | Race conditions, timeout dependencies | Strong |
| **Values** | Multiple values must change together | Distributed transactions, constraint sets | Strong |
| **Identity** | Components reference the same instance | Shared mutable state | Strongest |

## Key Properties

- **Rule of Degree**: Stronger connascence is acceptable *within* a module but should be minimized *across* module boundaries
- **Rule of Locality**: The closer two components are (same module, same service), the more connascence they can tolerate
- **Rule of Transformation**: Refactor stronger connascence into weaker forms when possible (e.g., convert positional parameters to named parameters: Position -> Name)
- Static connascence is generally preferable to dynamic connascence because it can be detected by compilers and static analysis tools
- Connascence subsumes and extends the traditional coupling/cohesion metrics -- every coupling type maps to one or more connascence types, but connascence provides finer granularity
- The taxonomy provides actionable refactoring guidance: identify the connascence type, then apply the transformation rule to weaken it

## Historical Context

Meilir Page-Jones introduced connascence in *What Every Programmer Should Know About Object-Oriented Design* (1996) as a generalization of coupling for object-oriented systems. Jim Weirich later popularized it in the Ruby community through conference talks (2009-2012). Richards and Ford brought it into the mainstream architecture conversation in *Fundamentals of Software Architecture* (2020), positioning it as a key modularity metric alongside cohesion and coupling.

## Related Terms

- **[Modularity](term_modularity.md)** -- the broader design quality that connascence measures; modularity = high cohesion + low connascence across boundaries
- **[Component Cohesion Principles](term_component_cohesion_principles.md)** -- REP, CCP, CRP govern what goes inside components; connascence governs how components interact
- **[Clean Architecture](term_clean_architecture.md)** -- Martin's Dependency Rule can be understood as minimizing cross-boundary connascence
- **[Architectural Quantum](term_architectural_quantum.md)** -- the deployment boundary within which synchronous connascence is expected
- **[DIP (Dependency Inversion Principle)](term_dip.md)** -- converts strong connascence (concrete dependency) to weak connascence (name/type through interfaces)

## References

### Vault Sources
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) -- connascence as modularity metric alongside cohesion and coupling
- [Digest: Clean Architecture (Martin)](../digest/digest_clean_architecture_martin.md) -- component coupling principles that connascence extends

### External Sources
- Page-Jones, M. (1996). *What Every Programmer Should Know About Object-Oriented Design*. Dorset House.
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapter 3.
- [Connascence.io](https://connascence.io/) -- community reference site with examples
- [Wikipedia: Connascence](https://en.wikipedia.org/wiki/Connascence)
