---
tags:
  - resource
  - terminology
  - software_architecture
  - architecture_style
  - monolithic
keywords:
  - layered architecture
  - n-tier architecture
  - presentation layer
  - business layer
  - persistence layer
  - sinkhole anti-pattern
topics:
  - Software Architecture
  - Architecture Styles
  - Monolithic Architecture
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Layered Architecture

## Definition

**Layered architecture** (also called n-tier architecture) is a monolithic architecture style that organizes components into horizontal layers, each responsible for a specific concern. The standard four-layer topology is: **presentation** → **business** → **persistence** → **database**. Each layer forms a barrier — requests flow top-down, and each layer can only access the layer directly below it (closed layers) or skip layers (open layers). It is the de facto standard for most applications and the natural default when no other style is explicitly chosen. Richards and Ford classify it as the simplest architecture style in *Fundamentals of Software Architecture* (2020), with one architectural quantum.

## Topology

```
┌──────────────────────────┐
│   Presentation Layer     │  ← UI, API endpoints, views
├──────────────────────────┤
│   Business Layer         │  ← Business rules, workflows, validation
├──────────────────────────┤
│   Persistence Layer      │  ← Data access, ORM, repositories
├──────────────────────────┤
│   Database Layer         │  ← Tables, schemas, stored procedures
└──────────────────────────┘
```

## Architecture Characteristics

| Characteristic | Rating | Notes |
|---------------|--------|-------|
| **Simplicity** | High | Easy to understand, build, and maintain |
| **Cost** | Low | Minimal infrastructure requirements |
| **Deployability** | Low | Entire application deploys as one unit |
| **Scalability** | Low | Only vertical scaling; cannot scale layers independently |
| **Fault tolerance** | Low | Failure in one layer cascades to all |
| **Testability** | Medium | Layers can be mocked, but integration testing is complex |
| **Modularity** | Low | Technical partitioning; changes often span multiple layers |

## Key Properties

- **Separation of concerns**: Each layer has a distinct role — presentation handles UI, business handles rules, persistence handles data access
- **Technical partitioning**: Layers are organized by technical function, not by business domain (contrast with domain partitioning in service-based and microservices)
- **Closed layers**: A layer can only access the layer directly below it — prevents tight coupling across layers but adds pass-through overhead
- **Open layers**: Some implementations allow layers to be skipped (e.g., presentation → persistence), trading isolation for performance
- **Sinkhole anti-pattern**: When requests pass through layers doing no work — a sign that layered architecture may be the wrong choice for the problem

## Anti-Patterns

| Anti-Pattern | Description | Signal |
|-------------|-------------|--------|
| **Sinkhole** | Requests pass through layers without processing (simple pass-through) | >80% of requests do no work in at least one layer |
| **Architecture by implication** | Defaulting to layered because nothing else was considered | No explicit architecture decision |
| **Monolith growth** | Layers become tightly coupled as the system grows | Changes to one feature require modifying all layers |

## Related Terms

- **[Clean Architecture](term_clean_architecture.md)** — Martin's concentric circles model inverts the dependency direction compared to traditional layered architecture
- **[Microservices Architecture](term_microservices_architecture.md)** — distributed alternative that replaces technical layering with domain-based service decomposition
- **[Service-Based Architecture](term_service_based_architecture.md)** — pragmatic middle ground between monolithic layered and fully distributed microservices
- **[Screaming Architecture](term_screaming_architecture.md)** — Martin's principle that architecture should reveal domain intent; layered architecture "screams" its technical concerns instead
- **[Architecture Characteristics](term_architecture_characteristics.md)** — layered architecture favors simplicity and cost at the expense of scalability and deployability
- **[Modularity](term_modularity.md)** — layered architecture achieves technical modularity but not domain modularity
- **[NGINX](term_nginx.md)** — NGINX often serves as the entry point (reverse proxy/load balancer) sitting in front of a layered application, routing requests to the presentation layer
- **[SSL Termination](term_ssl_termination.md)**: SSL termination embodies the layered principle -- the TLS layer is handled at the edge, cleanly separated from application logic layers

## References

### Vault Sources
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) — layered as the simplest monolithic style
- [Digest: Clean Architecture (Martin)](../digest/digest_clean_architecture_martin.md) — the Dependency Rule inverts the traditional top-down layer dependency

### External Sources
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapter 10.
- [Wikipedia: Multitier Architecture](https://en.wikipedia.org/wiki/Multitier_architecture)
