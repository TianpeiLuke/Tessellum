---
tags:
  - resource
  - terminology
  - software_architecture
  - architecture_style
  - distributed
  - microservices
keywords:
  - microservices
  - microservices architecture
  - independently deployable
  - bounded context
  - domain-driven design
  - service mesh
  - API gateway
topics:
  - Software Architecture
  - Architecture Styles
  - Distributed Systems
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Microservices Architecture

## Definition

**Microservices architecture** is a distributed architecture style where functionality is decomposed into **fine-grained, independently deployable services**, each owning its own data and implementing a single bounded context. Each service runs in its own process, communicates via lightweight protocols (REST, gRPC, messaging), and can be developed, deployed, and scaled independently. Richards and Ford present it in *Fundamentals of Software Architecture* (2020) as the style that **maximizes architectural quantum count** — each service is its own quantum with independent architecture characteristics — at the cost of significant operational complexity.

## Topology

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│Order Svc│  │Payment  │  │Customer │  │Inventory│  │Shipping │
│         │  │ Svc     │  │ Svc     │  │ Svc     │  │ Svc     │
│ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │
│ │ DB  │ │  │ │ DB  │ │  │ │ DB  │ │  │ │ DB  │ │  │ │ DB  │ │
│ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     └────────────┴───────┬────┴────────────┴────────────┘
                    ┌─────┴──────┐
                    │ API Gateway│
                    │ / Svc Mesh │
                    └────────────┘
```

## Architecture Characteristics

| Characteristic | Rating | Notes |
|---------------|--------|-------|
| **Deployability** | Very High | Each service deploys independently |
| **Scalability** | Very High | Scale individual services based on their load |
| **Fault tolerance** | High | Service failures are isolated (circuit breaker pattern) |
| **Modularity** | Very High | Services are independently developed and maintained |
| **Testability** | High | Services testable in isolation; integration testing is complex |
| **Evolutionary** | Very High | Services can be replaced, rewritten, or upgraded independently |
| **Operational complexity** | Very High | Service discovery, monitoring, distributed tracing, data consistency |
| **Data consistency** | Low | Each service owns its data; cross-service transactions require saga pattern |
| **Performance** | Medium | Network latency for inter-service calls |

## Key Properties

- **Each service owns its data** — no shared database; this maximizes independence but requires eventual consistency patterns (saga, event sourcing) for cross-service transactions
- **Bounded context alignment** — services map to DDD bounded contexts; service boundaries should follow domain boundaries, not technical boundaries
- **Independent deployment** — each service can be deployed without deploying or coordinating with other services
- **Technology heterogeneity** — different services can use different languages, frameworks, and databases (polyglot persistence)
- **Operational overhead is significant** — requires service discovery, API gateway, circuit breakers, distributed tracing, centralized logging, container orchestration (Kubernetes)
- **The distributed monolith anti-pattern** — microservices that share a database or require coordinated deployment are microservices in name only
- Richards and Ford advise: **don't start with microservices** — start with a monolith or service-based architecture and migrate to microservices only when the benefits outweigh the operational cost

## Supporting Infrastructure

| Component | Purpose | Examples |
|-----------|---------|---------|
| **API Gateway** | Single entry point for clients; routing, auth, rate limiting | Kong, Tyk |
| **Service Mesh** | Service-to-service communication, observability, security | Istio, Linkerd |
| **Container Orchestration** | Deploy, scale, manage service instances | Kubernetes, ECS |
| **Circuit Breaker** | Prevent cascade failures when a service is unavailable | Hystrix, Resilience4j |
| **Distributed Tracing** | Track requests across service boundaries | Jaeger, Zipkin, X-Ray |

## Related Terms

- **Service-Based Architecture** — coarser-grained alternative with shared database; pragmatic default before microservices
- **[Event-Driven Architecture](term_event_driven_architecture.md)** — often combined with microservices for asynchronous inter-service communication
- **Architectural Quantum** — each microservice is its own quantum with independent characteristics
- **Architecture Characteristics** — microservices maximize deployability, scalability, and fault tolerance at the cost of data consistency and operational simplicity
- **Connascence** — microservices minimize cross-service connascence; strong connascence between services is a boundary smell
- **Kafka** — common event backbone for inter-service communication in microservices architectures
- **Layered Architecture** — monolithic alternative; microservices replace technical layering with domain-based decomposition

- **CAP Theorem**: Each service boundary is a potential partition point requiring C-vs-A trade-offs
- **Partition Tolerance**: Inter-service communication failures are network partitions
- **FLP Impossibility**: Distributed coordination between microservices faces FLP constraints
- **Amdahl's Law**: Slowest synchronous call in a chain limits overall throughput
- **Availability**: Each microservice must make its own availability trade-offs
- **PACELC**: Each microservice boundary introduces PACELC trade-offs — inter-service calls face latency-consistency choices even without partitions
- **Health Check**: Health checks are essential in microservices for service discovery, load balancer routing, and automated failover of independently deployed service instances
- **HAProxy**: HAProxy commonly serves as the ingress load balancer or API gateway layer in microservices deployments, distributing traffic across service instances
- **NGINX**: NGINX commonly serves as the API gateway and load balancer in microservices deployments, routing requests to independently deployed services
- **Reverse Proxy**: Reverse proxies serve as the unified entry point (ingress) for routing traffic to independently deployed microservices
- **Round Robin**: Round Robin is the default load balancing algorithm for distributing requests across instances of a microservice behind a Layer 7 load balancer
- **Session Persistence**: Microservices architectures favor stateless services with externalized state, reducing the need for session persistence at the load balancer
- **SSL Termination**: SSL termination at an API gateway or ingress controller is a standard pattern in microservices deployments, centralizing TLS handling for many small services
- **API Gateway**: The API Gateway serves as the single entry point for all client requests in a microservices architecture, providing routing, authentication, rate limiting, and response aggregation
- **CDN (Content Delivery Network)**: CDNs sit in front of microservices-based backends, caching API responses and serving static assets to reduce load on individual services
- **Circuit Breaker**: Circuit breakers are critical in microservices to prevent cascading failures when one service-to-service call fails repeatedly
- **EKS**: Managed Kubernetes for microservices requiring pod-level isolation and service mesh
- **Consistent Hashing**: Consistent hashing is used for request routing and session affinity across microservice instances
- **Load Balancer**: Microservices rely heavily on load balancers (both external and internal/service mesh) for inter-service communication and scaling
- **Message Queue**: Message queues enable asynchronous, loosely coupled communication between independently deployable microservices
- **Rate Limiting**: Rate limiting is essential in microservices to prevent cascading failures when one service overwhelms another
- **Redis**: Shared state infrastructure in microservices architectures — serves as distributed cache, session store, pub/sub message bus, rate limiter, and distributed lock manager across service boundaries
- **GraphQL**: GraphQL often serves as the unified API gateway aggregating data from multiple microservices into a single client-facing endpoint
- **gRPC**: gRPC is the primary high-performance communication protocol for synchronous inter-service calls in microservices architectures
- **Pub/Sub**: Pub/Sub enables asynchronous, decoupled inter-service communication in microservices via topic-based message routing
- **REST**: REST is the most common inter-service and external-facing API protocol in microservices architectures
- **Scalability**: Microservices enable fine-grained horizontal scaling -- each service scales independently based on its own load profile
- **WebSocket**: WebSocket gateways in microservices require special handling for connection routing, sticky sessions, and service discovery
- **Two-Phase Commit**: 2PC coordinates distributed transactions across microservices, but its blocking nature makes it a poor fit for high-availability microservice architectures
- **Saga Pattern**: Sagas are the preferred pattern for distributed transactions across microservices, using a sequence of local transactions with compensating actions instead of global locks
- **Latency**: Microservices add inter-service network latency (0.5ms per hop); fan-out patterns cause tail latency amplification
- **Throughput**: Microservices enable independent scaling — each service can be scaled for its specific throughput requirements
- **[CQRS](term_cqrs.md)**: Command Query Responsibility Segregation is often used inside microservices boundaries — read-side and write-side become separate services with their own scaling profiles

## References

### Vault Sources
- Digest: Fundamentals of Software Architecture (Richards & Ford) — microservices as maximum-quantum distributed style
- Digest: AI Engineering (Huyen) — microservices patterns applied to ML system architecture

### External Sources
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. Chapter 17.
- Newman, S. (2021). *Building Microservices* (2nd ed.). O'Reilly Media. — the definitive microservices reference
- [Wikipedia: Microservices](https://en.wikipedia.org/wiki/Microservices)
- [Martin Fowler — Microservices](https://martinfowler.com/articles/microservices.html) — the 2014 article that popularized the term
