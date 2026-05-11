---
tags:
  - resource
  - terminology
  - data_engineering
  - software_architecture
  - distributed_systems
  - messaging
keywords:
  - event-driven architecture
  - EDA
  - publish-subscribe
  - event bus
  - event broker
  - asynchronous messaging
  - loose coupling
  - event sourcing
  - CQRS
  - reactive systems
topics:
  - software architecture
  - data engineering
  - distributed systems design
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Event-Driven Architecture

## Definition

**Event-Driven Architecture (EDA)** is a software architecture pattern in which the flow of the program is determined by **events** -- significant changes in state or occurrences that are emitted, transmitted, and consumed asynchronously by decoupled components. In an EDA system, **producers** emit events without knowledge of who will consume them, and **consumers** react to events independently, enabling loose coupling, horizontal scalability, and real-time responsiveness. Events are routed through an **event broker** (such as Apache Kafka or RabbitMQ) that decouples producers from consumers. EDA is a foundational pattern in modern data engineering, microservices architectures, and real-time analytics systems. It contrasts with request-response (synchronous) architectures where components directly call each other and wait for responses.

## Core Concepts

### EDA Components

```
┌────────────┐     ┌──────────────────┐     ┌────────────────┐
│  Event      │     │   Event Broker    │     │  Event          │
│  Producers  │────►│   (Kafka, SNS,   │────►│  Consumers      │
│             │     │    EventBridge)   │     │                 │
│ • Services  │     │                  │     │ • Services      │
│ • Sensors   │     │ • Routing        │     │ • Processors    │
│ • Users     │     │ • Persistence    │     │ • Databases     │
│ • Databases │     │ • Replay         │     │ • Dashboards    │
└────────────┘     └──────────────────┘     └────────────────┘
```

### Event Anatomy

| Field | Description | Example |
|-------|-------------|---------|
| **Event type** | What happened | `order.placed`, `refund.issued` |
| **Event ID** | Unique identifier | `evt-2026-03-22-a7f3` |
| **Timestamp** | When the event occurred | `2026-03-22T14:30:00Z` |
| **Source** | System that produced the event | `order-service` |
| **Payload** | Data about the event | `{ orderId: "123", amount: 49.99 }` |
| **Metadata** | Correlation IDs, schema version | `{ correlationId: "abc", v: 2 }` |

### Communication Patterns

```
1. Publish-Subscribe (Fan-out):
   Producer ──► Topic ──► Consumer A
                     ├──► Consumer B
                     └──► Consumer C

2. Event Streaming (Ordered Log):
   Producer ──► Kafka Topic ──► Consumer Group
                (persistent, replayable)

3. Event Queue (Competing Consumers):
   Producer ──► Queue ──► Consumer 1 (processes msg)
                     └──► Consumer 2 (idle, standby)

4. Event Sourcing (State as Event Log):
   Command ──► Event Store ──► [e1, e2, e3, ...] ──► Materialize State
              (append-only)     (complete history)
```

### EDA Topology Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Mediator** | Central coordinator orchestrates event flow between steps | Complex workflows with defined steps |
| **Broker** | No central coordinator; components react independently to events | Highly decoupled, autonomous services |
| **Event Sourcing** | State derived from append-only log of all events | Audit trail, temporal queries, undo |
| **CQRS** | Separate models for reads (queries) and writes (commands) | High-read/write asymmetry workloads |
| **Saga** | Distributed transaction via compensating events | Cross-service transactions without 2PC |

## Key Properties

- **Loose coupling**: Producers and consumers have no direct dependencies; new consumers can be added without modifying producers
- **Asynchronous communication**: Producers emit events without waiting for consumer responses, enabling non-blocking execution
- **Scalability**: Consumers can be independently scaled based on event volume and processing requirements
- **Real-time responsiveness**: Events are processed as they occur, enabling immediate reactions to state changes
- **Temporal decoupling**: Producers and consumers do not need to be running simultaneously; event brokers buffer messages
- **Replay capability**: Persistent event logs (Kafka) allow reprocessing historical events for debugging, backfills, or new consumer onboarding
- **Eventual consistency**: Systems achieve consistency over time rather than immediately, trading strong consistency for availability and partition tolerance
- **Auditability**: Event logs provide a complete, immutable record of what happened and when

## EDA vs. Request-Response

| Dimension | Event-Driven | Request-Response |
|-----------|-------------|-----------------|
| **Coupling** | Loose (fire-and-forget) | Tight (caller knows callee) |
| **Communication** | Asynchronous | Synchronous |
| **Failure handling** | Consumer failure does not block producer | Callee failure blocks caller |
| **Scalability** | Independent scaling per component | Scaling requires all tiers |
| **Latency model** | Variable (eventual) | Predictable (immediate) |
| **Debugging** | Harder (distributed traces) | Easier (call stack) |
| **Data flow** | Push-based | Pull-based |

## Related Terms

### Messaging and Streaming
- **Health Check**: Health check failures often trigger events (alerts, auto-scaling, failover) in event-driven infrastructure
- **Message Queue**: Message queues serve as the point-to-point event transport layer between decoupled producers and consumers in EDA
- **Pub/Sub**: Pub/Sub is the foundational fan-out communication pattern underlying event-driven systems
- **Rate Limiting**: Asynchronous event-driven patterns reduce synchronous request pressure; rate limiting protects synchronous API endpoints that EDA complements with async flows
- **REST**: REST provides synchronous request-response communication while EDA provides asynchronous event-based communication — often combined in the same system
- **Term: Apache Kafka** -- De facto event broker for EDA; distributed commit log with publish-subscribe and retention
- **Term: Apache Flink** -- Stream processor for complex event processing in EDA systems
- **Term: Stream Processing** -- Processing paradigm that operates on event streams produced by EDA
- **Term: Apache Spark** -- Can consume event streams via Structured Streaming for analytical processing

### Distributed Systems Theory
- **PACELC**: EDA's asynchronous nature is an explicit choice for low latency over strong consistency — the EL (Else Latency) side of PACELC

### Data Engineering Patterns
- **Term: Change Data Capture** -- Database changes emitted as events; a key EDA pattern for data integration
- **Term: ETL** -- Traditional batch pattern; EDA enables streaming ETL as an alternative
- **Term: Batch Processing** -- Contrasting paradigm; EDA shifts from scheduled to event-triggered processing
- **Term: Clickstream** -- User interaction events commonly processed through EDA patterns

### Infrastructure
- **HAProxy**: HAProxy can proxy event stream connections (WebSocket, SSE) and is often combined with event-driven frontends in distributed architectures
- **NGINX**: NGINX handles synchronous HTTP/gRPC ingress at the edge while event-driven architecture handles asynchronous internal communication between services
- **Reverse Proxy**: Reverse proxies handle synchronous ingress traffic; EDA handles asynchronous internal communication -- complementary patterns in modern architectures
- **Round Robin**: In event-driven systems, Round Robin distributes events across consumer instances in a competing-consumers pattern (e.g., Kafka consumer group partition assignment)

### Caching
- **Cache Invalidation**: Event-driven cache invalidation consumes change events from producers to invalidate or update cache entries in real time, replacing polling-based invalidation
- **Cache Stampede**: Event-driven architectures can mitigate cache stampedes by broadcasting cache-miss events to a single handler rather than allowing concurrent regeneration

### System Design
- **API Gateway**: API Gateways serve as the synchronous ingress layer that often routes requests into asynchronous event-driven pipelines for downstream processing
- **GraphQL**: GraphQL subscriptions provide an event-driven API pattern where clients subscribe to real-time data changes over WebSocket connections
- **Scalability**: Asynchronous messaging decouples producers from consumers, enabling each to scale independently; Kafka consumer groups scale read throughput by adding consumers
- **WebSocket**: WebSocket enables event-driven real-time communication between client and server; events pushed without polling
- **Write-Back Cache**: The async flush in write-back caching is conceptually similar to EDA's asynchronous event processing; both decouple producers from downstream persistence
- **Write-Through Cache**: Write-back caching often uses event-driven async writes; write-through avoids this complexity by using synchronous writes

### Architecture
- **Term: Data Engineering Lifecycle** -- EDA influences the ingestion and serving stages of the lifecycle
- **Term: DataOps** -- Operational practices for managing event-driven data pipelines
- **Term: Directed Acyclic Graph** -- Event flow topologies can form DAGs of processing stages

### Performance
- **Throughput**: Event-driven architecture achieves high throughput through asynchronous processing and message queue buffering

### Architectural Patterns
- **[CQRS](term_cqrs.md)**: Command Query Responsibility Segregation is the natural pairing — commands produce events that feed read-side projections; event-driven systems are the typical substrate for CQRS implementations

## References

### Vault References
- Digest: Fundamentals of Data Engineering -- Event-driven patterns in data ingestion and architecture

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media. -- Architecture patterns for ingestion and serving
- Richards, M. (2015). *Software Architecture Patterns*. O'Reilly Media. -- Chapter on Event-Driven Architecture
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapters 11-12 on stream processing and event-driven systems
- Stopford, B. (2018). *Designing Event-Driven Systems*. O'Reilly Media / Confluent.
- Fowler, M. (2017). "What do you mean by 'Event-Driven'?" -- https://martinfowler.com/articles/201701-event-driven.html

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Software architecture pattern |
| **Core principle** | Program flow driven by events (state changes), not direct calls |
| **Communication** | Asynchronous, publish-subscribe via event broker |
| **Coupling** | Loose -- producers and consumers are independent |
| **Key benefit** | Scalability, responsiveness, extensibility |
| **Key challenge** | Eventual consistency, distributed debugging, event ordering |
| **Key patterns** | Pub-sub, event sourcing, CQRS, saga, mediator, broker |
| **Key technologies** | Kafka, SNS/SQS, EventBridge, RabbitMQ, Pulsar |

**Key Insight**: Event-Driven Architecture inverts the traditional control flow of software systems. Instead of Service A calling Service B (creating a runtime dependency), Service A emits an event ("something happened") and Service B independently decides to react. This inversion has profound consequences: (1) producers can evolve independently of consumers, (2) new consumers can be added without changing producers, (3) the event log becomes a shared, replayable source of truth, and (4) the system naturally supports real-time processing. However, EDA introduces **eventual consistency** as a fundamental trade-off -- the system state may be temporarily inconsistent across services. The data engineering significance is that EDA transforms data pipelines from periodic batch operations into continuous, real-time flows, making the architecture itself an expression of the data engineering lifecycle.

---

**Last Updated**: March 22, 2026
**Status**: Active - foundational architecture pattern in modern data engineering and microservices
