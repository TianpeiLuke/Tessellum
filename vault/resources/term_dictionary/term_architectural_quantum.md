---
tags:
  - resource
  - terminology
  - software_architecture
  - system_design
  - deployment
keywords:
  - architectural quantum
  - quantum
  - independently deployable
  - functional cohesion
  - synchronous connascence
  - deployment boundary
  - architecture characteristics
topics:
  - Software Architecture
  - System Design
  - Deployment Architecture
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Architectural Quantum

## Definition

An **architectural quantum** is the minimum deployable unit of a software system that includes all structural elements required for the system to function correctly. Introduced by Richards and Ford in *Fundamentals of Software Architecture* (2020), it is defined by three properties: **(1) independently deployable** -- can be deployed without coordinating with other components, **(2) high functional cohesion** -- contains everything needed for a bounded context, and **(3) synchronous connascence** -- components within the quantum call each other synchronously. The quantum concept is architecturally significant because it determines the **granularity of architecture characteristics**: each quantum can have its own set of "-ilities" (scalability, availability, performance), and the number of quanta determines how many different characteristic profiles a system can support.

## Key Properties

- A **monolith** has exactly one quantum -- the entire application is deployed as a unit and shares a single set of architecture characteristics
- **Microservices** have many quanta -- each service is its own quantum with independent characteristics (one service can optimize for throughput, another for latency)
- **Service-based architecture** typically has 4-12 quanta -- fewer than microservices, more than a monolith
- The quantum boundary determines **blast radius**: failures, deployments, and scaling events are contained within a quantum
- Database sharing reduces quantum independence -- if two services share a database, they form a single quantum regardless of separate deployment
- The quantum is the unit at which **fitness functions** (architecture compliance tests) should be evaluated
- Quantum size trades off: smaller quanta = more characteristic flexibility but more operational complexity; larger quanta = simpler operations but characteristic constraints

## Relationship to Architecture Styles

| Architecture Style | Typical Quanta | Characteristic Flexibility |
|-------------------|---------------|---------------------------|
| Layered | 1 | One set of characteristics for entire system |
| Pipeline | 1 | One set of characteristics |
| Microkernel | 1 | One set (plugins inherit core characteristics) |
| Service-Based | 1-few | Limited flexibility (shared database) |
| Event-Driven | Varies | Moderate flexibility |
| Space-Based | Varies | High flexibility (independent processing units) |
| Microservices | Many | Maximum flexibility (each service independent) |

## Related Terms

- **[Connascence](term_connascence.md)** -- synchronous connascence defines the internal binding of a quantum; minimizing connascence across quanta is the key modularity goal
- **[Architecture Characteristics](term_architecture_characteristics.md)** -- each quantum can support its own set of characteristics; the quantum is the unit of characteristic assignment
- **[Fitness Function](term_fitness_function.md)** -- fitness functions are evaluated at the quantum level to verify characteristic compliance
- **[Microservices Architecture](term_microservices_architecture.md)** -- the architecture style that maximizes quantum count for maximum characteristic independence
- **[Service-Based Architecture](term_service_based_architecture.md)** -- pragmatic middle ground with fewer quanta than microservices
- **[Modularity](term_modularity.md)** -- the quantum is the deployment-level expression of modularity principles
- **[API Gateway](term_api_gateway.md)**: The API Gateway sits at the boundary between quanta, mediating requests across independently deployable architectural units

## References

### Vault Sources
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) -- introduces architectural quantum as a core concept

### External Sources
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapter 8.
- Ford, N., Richards, M., Sadalage, P., & Dehghani, Z. (2021). *Software Architecture: The Hard Parts*. O'Reilly Media. -- extends quantum concept to data partitioning
