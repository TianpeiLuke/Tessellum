---
tags:
  - resource
  - terminology
  - distributed_systems
  - cloud_design_pattern
  - microservices
  - migration
keywords:
  - Strangler Fig Pattern
  - Strangler Fig Application
  - Strangler Application
  - incremental migration
  - legacy modernization
  - monolith decomposition
  - facade routing
topics:
  - System Design
  - Cloud Design Patterns
  - Migration and Modernization
  - Microservices
language: markdown
date of note: 2026-07-27
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Strangler Fig Pattern

## Definition

The **Strangler Fig Pattern** is a migration and modernization strategy for incrementally replacing a legacy system with new functionality, one piece at a time, until the old system has been entirely phased out. Rather than attempting a risky "big-bang" rewrite -- where the legacy system is switched off and a brand-new replacement is switched on in a single cutover -- the pattern routes incoming requests through an interception layer (a facade or proxy) that gradually redirects traffic away from legacy components and toward newly built services. Each increment is independently shippable, verifiable, and reversible, so the migration proceeds as a series of small, low-risk steps while the system remains fully operational throughout.

The pattern was named by Martin Fowler in his 2004 essay "StranglerApplication" (later retitled "StranglerFigApplication"), inspired by the strangler fig trees he observed in Australian rainforests: the fig seeds germinate in the upper branches of a host tree and grow their roots downward, gradually enveloping the host until the original tree dies and the fig stands in its place. By analogy, the new system "grows around" the legacy application, incrementally taking over its responsibilities until the legacy code can be safely retired. The pattern is documented as a first-class cloud design pattern in the Microsoft Azure Architecture Center and in AWS Prescriptive Guidance, and it is widely used by teams decomposing monoliths into microservices.

## Context

The Strangler Fig Pattern appears wherever an organization must modernize a large, business-critical legacy system without the downtime, cost, and risk of a full rewrite. The classic scenario is decomposing a monolithic application into a set of microservices: an HTTP-level facade (commonly an API gateway, reverse proxy, or ambassador/routing layer) sits in front of the monolith and inspects each request. Requests targeting already-migrated functionality are routed to the new services; everything else falls through to the legacy monolith. As more functionality is carved out and reimplemented, the facade's routing rules shift more traffic to the new implementations, and the legacy footprint shrinks until it can be decommissioned and the facade removed.

Because migration and the new services often need to coexist and stay consistent, the pattern is frequently combined with other structural patterns. Data that both the old and new systems must read or write may be synchronized via change data capture, event streaming, or the introduction of **CQRS** and **event sourcing** during the carve-out. The facade layer itself is where cross-cutting concerns -- authentication, TLS termination, routing, monitoring -- are consolidated, which is exactly the role of the ambassador and API gateway patterns. In distributed and cloud architectures the pattern is prized for its risk profile: each step is small enough to roll back independently, verification happens continuously in production, and the business never faces a single high-stakes cutover.

## Key Characteristics

- **Incremental replacement**: Functionality is migrated in small slices rather than all at once; the legacy and new systems run side by side for the duration of the migration.
- **Interception / facade layer**: A proxy, reverse proxy, API gateway, or ambassador component sits in front of both systems and routes each request to either the legacy or the new implementation based on configurable rules.
- **Independently shippable increments**: Each migrated slice can be released, tested, and observed in production on its own, decoupling the migration timeline from any single large deliverable.
- **Reversibility**: Because routing is controlled at the facade, traffic can be shifted back to the legacy path if a new increment misbehaves -- limiting blast radius and enabling safe experimentation.
- **Coexistence and data synchronization**: The old and new systems typically must share or reconcile state during the transition, often via event streaming, change data capture, or a shared data store, sometimes introducing CQRS/event sourcing along the way.
- **Eventual retirement**: The migration is complete when all traffic flows to new services; the legacy system -- and often the facade itself -- is then decommissioned.
- **Trade-offs**: The interception layer must not become a bottleneck or single point of failure; routing rules and dual-running data add operational complexity; and migrations that stall leave the system indefinitely half-strangled, carrying the cost of running two systems at once.

## Related Terms


## References

- [Fowler, M. (2004/2019). "StranglerFigApplication." martinfowler.com](https://martinfowler.com/bliki/StranglerFigApplication.html) -- The original essay that named the pattern after the strangler fig tree and argued for incremental replacement over big-bang rewrites.
- [Microsoft Azure Architecture Center. "Strangler Fig pattern."](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) -- Cloud design pattern reference describing the facade/interception approach, applicability, and issues to consider.
- [AWS Prescriptive Guidance. "Strangler fig pattern."](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/strangler-fig.html) -- AWS guidance on applying the pattern to incrementally decompose and modernize monolithic applications.
- [Microsoft Learn. "Modernize by using the Strangler Fig pattern."](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/modernization/strangler-fig-pattern) -- Worked example scenario illustrating a phased migration behind a routing facade.
