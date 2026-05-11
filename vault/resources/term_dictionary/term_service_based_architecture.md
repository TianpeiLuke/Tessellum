---
tags:
  - resource
  - terminology
  - software_architecture
  - architecture_style
  - distributed
keywords:
  - service-based architecture
  - coarse-grained services
  - domain services
  - shared database
  - pragmatic distributed
topics:
  - Software Architecture
  - Architecture Styles
  - Distributed Architecture
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Service-Based Architecture

## Definition

**Service-based architecture** is a distributed architecture style that deploys functionality as **coarse-grained domain services** (typically 4-12) that share a single database. Richards and Ford present it in *Fundamentals of Software Architecture* (2020) as the **pragmatic default** for distributed systems — it provides most benefits of distributed architectures (independent deployability, domain-level separation, fault isolation) with far less operational complexity than microservices. Each service encompasses an entire domain or subdomain rather than a single function, resulting in fewer services to manage, fewer inter-service communication challenges, and simpler data consistency because services share a database.

## Topology

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Order   │  │ Payment  │  │ Customer │  │ Shipping │
│ Service  │  │ Service  │  │ Service  │  │ Service  │
│ (domain) │  │ (domain) │  │ (domain) │  │ (domain) │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
     └─────────────┴─────────────┴─────────────┘
                        │
              ┌─────────┴─────────┐
              │  Shared Database  │
              └───────────────────┘
```

## Architecture Characteristics

| Characteristic | Rating | Notes |
|---------------|--------|-------|
| **Simplicity** | Medium | Fewer services than microservices; shared database simplifies data management |
| **Deployability** | Medium-High | Services deploy independently; shared DB may require coordination |
| **Scalability** | Medium | Services scale independently; shared DB is the bottleneck |
| **Fault tolerance** | Medium-High | Service failures are isolated; shared DB is a single point of failure |
| **Testability** | High | Services can be tested independently with the shared database |
| **Cost** | Medium | Moderate infrastructure; much less than microservices |
| **Domain partitioning** | High | Services align with business domains |

## Comparison with Microservices

| Dimension | Service-Based | Microservices |
|-----------|--------------|---------------|
| **Service count** | 4-12 | Dozens to hundreds |
| **Service granularity** | Coarse (entire domain) | Fine (single function/capability) |
| **Database** | Shared | Each service owns its data |
| **Data consistency** | ACID transactions | Eventual consistency (saga pattern) |
| **Operational complexity** | Moderate | High |
| **Inter-service communication** | Minimal (shared DB) | Extensive (API calls, events) |
| **Team structure** | Feature teams can span services | Each service has dedicated team |
| **Typical quantum** | 1-few | Many |

## Key Properties

- **Start here unless you have strong reasons not to** — Richards and Ford recommend service-based as the default distributed architecture because it balances flexibility with pragmatism
- The shared database is both the **greatest strength** (ACID transactions, simpler queries) and the **greatest weakness** (single point of failure, coupling through schema)
- Services are **domain-partitioned**, not technically partitioned — each service owns a complete business capability, not a technical layer
- Services communicate through **direct calls** (REST, gRPC) or through the **shared database** — no event bus required
- Migration path: start monolith → service-based → microservices (if needed). Most systems never need to progress beyond service-based

## Related Terms

- **[Microservices Architecture](term_microservices_architecture.md)** — finer-grained distributed style with independent databases; more flexible but more complex
- **[Layered Architecture](term_layered_architecture.md)** — monolithic alternative; service-based adds independent deployability and domain partitioning
- **[Architectural Quantum](term_architectural_quantum.md)** — service-based has 1-few quanta; the shared database limits quantum independence
- **[Architecture Characteristics](term_architecture_characteristics.md)** — service-based balances most characteristics at "medium-high" rather than excelling at any one
- **[Event-Driven Architecture](term_event_driven_architecture.md)** — can be combined with service-based for asynchronous communication between services
- **[HAProxy](term_haproxy.md)**: HAProxy routes traffic between domain services in service-based architectures as the shared infrastructure layer
- **[NGINX](term_nginx.md)**: NGINX serves as the shared infrastructure layer in service-based architectures, providing centralized routing and cross-cutting concerns
- **[REST](term_rest.md)**: REST is the primary synchronous communication protocol between domain services in service-based architectures
- **[gRPC](term_grpc.md)**: gRPC is an alternative synchronous communication protocol for service-based architectures, offering binary serialization and streaming for higher-performance inter-service calls

## References

### Vault Sources
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) — service-based as the pragmatic default distributed style

### External Sources
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapter 13.
- Richards, M. (2020). *Software Architecture Patterns* (2nd ed.). O'Reilly Media. — expanded coverage of service-based patterns
