---
tags:
  - resource
  - terminology
  - software_architecture
  - system_design
  - non_functional_requirements
keywords:
  - architecture characteristics
  - "-ilities"
  - non-functional requirements
  - quality attributes
  - operational characteristics
  - structural characteristics
  - cross-cutting characteristics
topics:
  - Software Architecture
  - System Design
  - Quality Attributes
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Architecture Characteristics

## Definition

**Architecture characteristics** (also called "-ilities," quality attributes, or non-functional requirements) are the system properties that an architecture must support beyond functional requirements. Richards and Ford organize them into three categories in *Fundamentals of Software Architecture* (2020): **operational** (how the system runs), **structural** (how the system is built and changed), and **cross-cutting** (concerns spanning all layers). The key architectural insight is that **a system can realistically support only 3-5 characteristics well** -- each additional characteristic introduces trade-offs where optimizing one degrades another. This constraint is why "everything in software architecture is a trade-off."

## Taxonomy

### Operational Characteristics

| Characteristic | Definition |
|---------------|-----------|
| **Availability** | System uptime and accessibility |
| **Reliability** | Consistency of correct behavior under load |
| **Performance** | Response time, throughput, latency |
| **Scalability** | Ability to handle increased load by adding resources |
| **Elasticity** | Ability to dynamically scale up/down with demand |
| **Recoverability** | Ability to recover from failures (MTTR) |

### Structural Characteristics

| Characteristic | Definition |
|---------------|-----------|
| **Modularity** | Logical separation of components |
| **Extensibility** | Ability to add new features |
| **Maintainability** | Ease of modifying and updating |
| **Portability** | Ability to run on different platforms |
| **Deployability** | Ease and frequency of deployment |
| **Testability** | Ease of testing components in isolation |

### Cross-Cutting Characteristics

| Characteristic | Definition |
|---------------|-----------|
| **Security** | Protection against unauthorized access |
| **Accessibility** | Usability for people with disabilities |
| **Authentication/Authorization** | Identity verification and permission management |
| **Legal/Regulatory** | Compliance with laws (GDPR, CCPA, SOX) |
| **Privacy** | Protection of personal data |
| **Usability** | Ease of use for end users |

## Key Properties

- **Implicit vs. explicit**: Some characteristics are stated in requirements (explicit); others are assumed by convention (implicit). Architects must surface implicit characteristics -- security is rarely listed but always expected
- **The 3-5 rule**: Supporting more than 3-5 characteristics well is architecturally unrealistic because optimizing for one often degrades another (e.g., security vs. performance, scalability vs. simplicity)
- **Architecture style selection**: The primary driver for choosing an architecture style is matching the style's natural strengths to the required characteristics
- Characteristics are assigned at the **architectural quantum** level -- different quanta can have different characteristic profiles
- **Fitness functions** make characteristics measurable and testable, transforming them from aspirational goals into enforceable contracts

## Related Terms

- **[Architectural Quantum](term_architectural_quantum.md)** -- the deployment unit that determines characteristic granularity; each quantum can have its own characteristic profile
- **[Fitness Function](term_fitness_function.md)** -- objective function that measures compliance with a specific characteristic
- **[Clean Architecture](term_clean_architecture.md)** -- Martin's model optimizes for testability, maintainability, and framework independence
- **[Modularity](term_modularity.md)** -- a structural characteristic measurable through cohesion, coupling, and connascence
- **[SAR](term_sar.md)** -- Scalability, Availability, Reliability — the three operational characteristics most critical for distributed systems, with pairwise trade-offs and the nines/MTBF/MTTR measurement framework
- **[Scalability](term_scalability.md)**: Scalability is a key operational architecture characteristic — the ability to handle increased load by adding resources, measured via throughput curves and saturation points

## References

### Vault Sources
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) -- taxonomy and the 3-5 rule
- [Digest: Clean Architecture (Martin)](../digest/digest_clean_architecture_martin.md) -- the Dependency Rule optimizes for specific structural characteristics

### External Sources
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapters 4-7.
- Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice* (3rd ed.). Addison-Wesley. -- canonical quality attributes framework
- [ISO 25010 Quality Model](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) -- international standard for software quality characteristics
