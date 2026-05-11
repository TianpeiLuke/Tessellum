---
tags:
  - resource
  - terminology
  - system_design
  - messaging
  - distributed_systems
keywords:
  - pub/sub
  - publish-subscribe
  - messaging pattern
  - fan-out
  - topic-based messaging
  - content-based filtering
  - message broker
  - decoupling
  - asynchronous communication
  - event notification
topics:
  - system design
  - distributed messaging
  - asynchronous communication patterns
  - event-driven architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Pub/Sub (Publish-Subscribe)

## Definition

**Pub/Sub (Publish-Subscribe)** is an asynchronous messaging pattern in which **publishers** emit messages to named topics or channels without knowing who (if anyone) will receive them, and **subscribers** register interest in specific topics and receive messages without knowing who published them. An intermediary -- the **message broker** or **event bus** -- decouples producers from consumers, routing each published message to all matching subscribers. This decoupling is the pattern's defining property: publishers and subscribers have no direct dependencies on each other, and can be added, removed, or modified independently. Pub/Sub is a foundational building block of distributed systems, event-driven architectures, and microservices communication.

## Context

Pub/Sub is one of the core messaging patterns covered in system design fundamentals. It underpins the communication layer in event-driven architectures and is a critical concept in system design interviews. The pattern has been implemented across a wide range of technologies:

| Implementation | Type | Key Characteristics |
|----------------|------|---------------------|
| **Apache Kafka** | Distributed event streaming | Persistent log, consumer groups, exactly-once semantics, partitions |
| **Redis Pub/Sub** | In-memory broker | Ultra-low latency, no persistence (fire-and-forget), lightweight |
| **AWS SNS** | Managed cloud pub/sub | Fan-out to SQS, Lambda, HTTP; push-based delivery |
| **Google Cloud Pub/Sub** | Managed cloud pub/sub | Global, at-least-once delivery, dead-letter topics |
| **RabbitMQ** | Message broker | Exchange-based routing (fanout, topic, direct, headers), AMQP protocol |
| **Apache Pulsar** | Distributed messaging | Multi-tenancy, tiered storage, unified pub/sub + queue model |
| **Azure Event Grid / Service Bus** | Managed cloud messaging | Event Grid for reactive, Service Bus for enterprise messaging |

## Key Characteristics

### Publisher-Subscriber Decoupling

The core value proposition. Three dimensions of decoupling:

| Dimension | Description |
|-----------|-------------|
| **Space decoupling** | Publishers and subscribers do not need to know each other's network addresses or identities |
| **Time decoupling** | Publishers and subscribers do not need to be running simultaneously; the broker buffers messages |
| **Synchronization decoupling** | Publishing and subscribing are non-blocking; neither side waits for the other |

### Message Filtering

Two primary approaches determine which messages reach which subscribers:

```
Topic-Based Filtering:
  Publisher ──► Topic: "orders.created" ──► Subscriber A (subscribed to "orders.*")
                                        ├──► Subscriber B (subscribed to "orders.created")
                                        └──► Subscriber C (NOT subscribed -- does not receive)

Content-Based Filtering:
  Publisher ──► Broker ──► [Filter: amount > 100] ──► Subscriber A (receives)
                       └──► [Filter: region = "US"] ──► Subscriber B (receives if match)
```

- **Topic-based**: Subscribers register for named topics (channels). Simpler, faster, most common.
- **Content-based**: Subscribers define predicate filters on message attributes. More flexible, higher broker overhead.

### Fan-Out Pattern

A single published message is delivered to **all** subscribers on that topic. This is the defining difference from point-to-point queues:

```
Pub/Sub (Fan-Out):                    Message Queue (Point-to-Point):
  Publisher ──► Topic ──► Sub A         Producer ──► Queue ──► Consumer 1 (gets msg)
                     ├──► Sub B                            └── Consumer 2 (idle)
                     └──► Sub C
  (all 3 get the message)              (only 1 consumer processes each message)
```

### Delivery Semantics

| Guarantee | Description | Trade-off |
|-----------|-------------|-----------|
| **At-most-once** | Message delivered zero or one time; no retries on failure | Lowest latency, possible data loss (Redis Pub/Sub) |
| **At-least-once** | Message delivered one or more times; retried on failure | No data loss, possible duplicates (SNS, Kafka default) |
| **Exactly-once** | Message delivered exactly one time; deduplicated | Highest overhead, most complex (Kafka with idempotent producers + transactions) |

### Pub/Sub vs. Message Queue (Point-to-Point) Comparison

| Dimension | Pub/Sub | Message Queue |
|-----------|---------|---------------|
| **Delivery** | All subscribers get every message (fan-out) | One consumer gets each message (competing consumers) |
| **Coupling** | Publishers unaware of subscribers | Producers typically aware of queue |
| **Scaling model** | Add subscribers without changing publisher | Add consumers to share workload |
| **Use case** | Event notification, broadcast | Task distribution, work queues |
| **Examples** | SNS topics, Kafka topics, Redis channels | SQS, RabbitMQ queues, Celery |
| **Hybrid** | Kafka consumer groups combine both: fan-out across groups, competing consumers within a group |

### Consumer Groups (Kafka Model)

Kafka unifies pub/sub and message queue patterns via consumer groups:

```
Topic: "transactions" (3 partitions)

Consumer Group A (fan-out: gets ALL messages):
  Consumer A1 ← Partition 0
  Consumer A2 ← Partition 1, Partition 2

Consumer Group B (fan-out: also gets ALL messages):
  Consumer B1 ← Partition 0, Partition 1, Partition 2

Within each group: competing consumers (point-to-point)
Across groups: pub/sub (fan-out)
```

### Backpressure

When subscribers cannot keep up with the rate of published messages:

- **Buffering**: Broker stores messages (Kafka retains on disk; SNS/SQS queues buffer)
- **Rate limiting**: Broker throttles publisher or subscriber
- **Dropping**: Broker discards messages when buffer is full (Redis Pub/Sub drops for slow subscribers)
- **Flow control**: Reactive streams / pull-based consumers control their own consumption rate

### Ordering Guarantees

| System | Ordering Guarantee |
|--------|-------------------|
| **Kafka** | Ordered within a partition (not across partitions) |
| **SNS** | No ordering guarantee (FIFO SNS topics provide ordering within message groups) |
| **Google Cloud Pub/Sub** | No ordering by default; ordering keys provide per-key ordering |
| **RabbitMQ** | Ordered within a single queue |
| **Redis Pub/Sub** | Ordered per publisher connection |

## Related Terms

### Messaging Infrastructure
- **[Term: Apache Kafka](term_kafka.md)** -- Distributed event streaming platform; the most widely adopted pub/sub + log-based implementation
- **[Term: SNS (Simple Notification Service)](term_sns.md)** -- AWS managed pub/sub service for fan-out event notifications
- **[Term: SQS (Simple Queue Service)](term_sqs.md)** -- AWS managed message queue; often paired with SNS for pub/sub-to-queue fan-out (SNS + SQS pattern)

### Architecture Patterns
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Pub/Sub is the foundational communication pattern underlying event-driven systems
- **[Term: Microservices Architecture](term_microservices_architecture.md)** -- Pub/Sub enables asynchronous inter-service communication in microservices
- **[Term: Observer Pattern](term_observer_pattern.md)** -- In-process predecessor of Pub/Sub; defines one-to-many notification without a broker
- **[Term: Pipeline Architecture](term_pipeline_architecture.md)** -- Pub/Sub topics can connect processing stages in pipeline architectures
- **[Term: Hexagonal Architecture](term_hexagonal_architecture.md)** -- Pub/Sub fits naturally as a port/adapter for outbound events

### Data Engineering
- **[Term: Stream Processing](term_stream_processing.md)** -- Stream processors (Flink, Kafka Streams) consume from pub/sub topics as their input
- **[Term: Clickstream](term_clickstream.md)** -- Common data type transported via pub/sub topics for real-time analytics
- **[Term: Change Data Capture](term_change_data_capture.md)** -- Database changes published to topics for downstream consumption (Debezium + Kafka)
- **[Term: ETL](term_etl.md)** -- Pub/Sub enables streaming ETL as an alternative to batch ETL

### Distributed Systems Theory
- **[Term: CAP Theorem](term_cap_theorem.md)** -- Pub/Sub systems must navigate the consistency-availability-partition tolerance trade-off
- **[WebSocket](term_websocket.md)**: Pub/Sub backends (Redis Pub/Sub, Kafka) serve as the fan-out layer behind WebSocket servers, distributing messages across horizontally scaled WebSocket instances
- **[Redis](term_redis.md)**: Redis provides built-in Pub/Sub with ultra-low latency fire-and-forget delivery, plus Redis Streams for durable pub/sub with consumer groups
- **[Message Queue](term_message_queue.md)**: Point-to-point message queues deliver each message to exactly one consumer (competing consumers), contrasting with pub/sub's fan-out delivery to all subscribers

## References

### Vault References
- [Digest: Fundamental Concepts for System Design — SDDD](../digest/digest_sddd_fundamentals_podcast.md) -- Messaging systems as a core system design building block (Episode 2 - Fundamentals)

### External References
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapter 11: Stream Processing, messaging patterns
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. -- Messaging and event-driven patterns
- Eugster, P. et al. (2003). "The Many Faces of Publish/Subscribe." *ACM Computing Surveys*, 35(2), 114-131. -- Seminal academic survey of pub/sub systems
- Publisher-Subscriber Pattern -- Azure Architecture Center: https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber
- Publish-Subscribe Pattern -- AWS Prescriptive Guidance: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/publish-subscribe.html
- Pub/Sub Architecture -- Google Cloud: https://docs.cloud.google.com/pubsub/architecture
- Publish-Subscribe Pattern -- Wikipedia: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Asynchronous messaging pattern |
| **Core principle** | Publishers emit to topics; subscribers receive from topics; broker decouples both |
| **Decoupling** | Space, time, and synchronization decoupling between producers and consumers |
| **Delivery** | Fan-out: all subscribers receive every message (contrast with point-to-point queues) |
| **Filtering** | Topic-based (most common) or content-based |
| **Delivery semantics** | At-most-once, at-least-once, or exactly-once depending on implementation |
| **Key implementations** | Kafka, SNS, Google Cloud Pub/Sub, RabbitMQ, Redis Pub/Sub, Pulsar |
| **Key challenge** | Ordering, delivery guarantees, backpressure, subscriber failure handling |

**Key Insight**: Pub/Sub's power lies in its **triple decoupling** -- space, time, and synchronization -- which transforms tightly coupled request-response systems into loosely coupled, independently evolvable components. The critical design decision is not whether to use pub/sub, but which delivery guarantee to choose: at-most-once (fast but lossy), at-least-once (safe but requires idempotent consumers), or exactly-once (correct but expensive). In practice, most production systems choose at-least-once delivery with idempotent consumers, accepting the complexity of deduplication in exchange for data safety. Kafka's consumer group model elegantly unifies pub/sub (fan-out across groups) with message queues (competing consumers within a group), which is why Kafka has become the dominant implementation for serious distributed systems.

---

**Last Updated**: April 19, 2026
**Status**: Active - foundational messaging pattern in system design and distributed systems
