---
tags:
  - resource
  - terminology
  - data_engineering
  - streaming
  - messaging
  - distributed_computing
  - open_source
keywords:
  - Apache Kafka
  - Kafka
  - event streaming
  - publish-subscribe
  - topics
  - partitions
  - consumer groups
  - brokers
  - distributed log
  - message queue
topics:
  - data engineering
  - event streaming platforms
  - distributed messaging
  - real-time data infrastructure
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Apache Kafka

## Definition

**Apache Kafka** is an open-source distributed event streaming platform designed for high-throughput, fault-tolerant, publish-subscribe messaging and real-time data pipelines. Originally developed at LinkedIn in 2010 by Jay Kreps, Neha Narkhede, and Jun Rao to handle the company's massive-scale activity stream data, Kafka was open-sourced in 2011 and became an Apache top-level project in 2012. Unlike traditional message queues that delete messages after consumption, Kafka is built on a **distributed commit log** architecture -- messages are persisted to disk, replicated across brokers, and retained for configurable periods (hours to indefinitely), allowing multiple consumers to independently read the same data at their own pace. Kafka can handle trillions of messages per day with millisecond latency, making it the de facto backbone for event-driven architectures, stream processing pipelines, change data capture, and microservices communication in modern data engineering.

## Core Concepts

### Kafka Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Kafka Cluster                          │
│                                                            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│  │ Broker 1 │   │ Broker 2 │   │ Broker 3 │              │
│  │ (Leader  │   │ (Replica │   │ (Replica │              │
│  │  P0, P2) │   │  P0, P1) │   │  P1, P2) │              │
│  └──────────┘   └──────────┘   └──────────┘              │
│        ↑              ↑              ↑                     │
│        └──────────────┼──────────────┘                     │
│                       │                                     │
│              ZooKeeper / KRaft                              │
│           (metadata & coordination)                         │
└──────────────────────────────────────────────────────────┘
         ↑                                    ↓
   ┌───────────┐                       ┌───────────┐
   │ Producers │                       │ Consumers │
   │ (write)   │                       │ (read)    │
   └───────────┘                       └───────────┘
```

### Topics, Partitions, and Offsets

```
Topic: "order-events"
┌────────────────────────────────────────────────────┐
│ Partition 0:  [0] [1] [2] [3] [4] [5] [6] ...     │
│ Partition 1:  [0] [1] [2] [3] [4] ...              │
│ Partition 2:  [0] [1] [2] [3] [4] [5] [6] [7] ... │
└────────────────────────────────────────────────────┘
                 ↑
        Each [] = one message with an offset number
        Order guaranteed WITHIN a partition only
```

### Key Abstractions

| Concept | Description |
|---------|-------------|
| **Topic** | Named category/feed to which records are published (like a database table for events) |
| **Partition** | Ordered, immutable sequence of records within a topic; unit of parallelism |
| **Offset** | Sequential ID for each record within a partition; consumers track position via offsets |
| **Broker** | A Kafka server that stores partitions and serves client requests |
| **Producer** | Application that publishes records to topics |
| **Consumer** | Application that reads records from topics |
| **Consumer Group** | Set of consumers that cooperatively consume a topic; each partition assigned to exactly one consumer in the group |
| **Replication Factor** | Number of copies of each partition across brokers (typically 3) |
| **Leader / Follower** | One broker leads reads/writes for a partition; followers replicate for fault tolerance |

### Consumer Group Mechanics

```
Topic: "transactions" (4 partitions)

Consumer Group A (3 consumers):
  Consumer 1 ← Partition 0, Partition 1
  Consumer 2 ← Partition 2
  Consumer 3 ← Partition 3

Consumer Group B (2 consumers):    (independent, reads same data)
  Consumer 1 ← Partition 0, Partition 1
  Consumer 2 ← Partition 2, Partition 3

Rule: Each partition → exactly one consumer per group
      More consumers than partitions → some consumers idle
```

## Key Properties

- **High throughput**: Delivers millions of messages per second per broker through sequential disk I/O, zero-copy transfer, and batching
- **Durability**: Messages are persisted to disk and replicated across multiple brokers; data survives broker failures
- **Scalability**: Horizontally scalable by adding brokers and partitions; supports clusters with thousands of brokers
- **Ordering guarantees**: Messages within a partition are strictly ordered; no global ordering across partitions
- **Consumer independence**: Multiple consumer groups can independently read the same topic at different speeds without interference
- **Retention-based**: Messages are retained for a configurable period (or indefinitely with compaction), not deleted upon consumption
- **Exactly-once semantics**: Supported via idempotent producers and transactional APIs (Kafka Streams, 0.11+)
- **Log compaction**: Retains only the latest value per key, enabling Kafka as a changelog/state store
- **Ecosystem richness**: Kafka Connect (data integration), Kafka Streams (stream processing library), Schema Registry (schema governance)

## Kafka Ecosystem

| Component | Purpose |
|-----------|---------|
| **Kafka Brokers** | Core message storage and serving |
| **KRaft** | Built-in metadata management (replacing ZooKeeper in Kafka 3.x+) |
| **Kafka Connect** | Framework for connecting Kafka to external systems (databases, S3, Elasticsearch) |
| **Kafka Streams** | Lightweight stream processing library embedded in applications |
| **Schema Registry** | Schema management and compatibility enforcement (Avro, Protobuf, JSON Schema) |
| **ksqlDB** | SQL interface for stream processing on Kafka topics |
| **MirrorMaker** | Cross-cluster replication for disaster recovery and geo-distribution |

## Related Terms

### Stream Processing
- **[Message Queue](term_message_queue.md)**: Traditional message queues (SQS, RabbitMQ) delete messages after consumption; Kafka retains them as a durable log — the fundamental distinction between queue and event streaming semantics
- **[Term: Stream Processing](term_stream_processing.md)** -- Kafka is the primary transport layer for stream processing architectures
- **[Term: Apache Flink](term_flink.md)** -- Stream processor that commonly reads from and writes to Kafka topics
- **[Term: Apache Spark](term_spark.md)** -- Spark Structured Streaming integrates with Kafka as a source and sink
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Kafka is the canonical implementation of event-driven systems

### Data Engineering
- **[LSM Tree](term_lsm_tree.md)**: Kafka's log-structured storage shares the append-only, sequential I/O philosophy of LSM trees
- **[Term: ETL](term_etl.md)** -- Kafka enables streaming ETL via Kafka Connect and stream processors
- **[Term: Change Data Capture](term_change_data_capture.md)** -- CDC pipelines commonly use Kafka as the transport (Debezium + Kafka)
- **[Term: Batch Processing](term_batch_processing.md)** -- Kafka bridges batch and streaming; consumers can read historical data in batch mode
- **[Term: Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Kafka as core infrastructure across ingestion and serving stages

### Infrastructure
- **[HAProxy](term_haproxy.md)**: HAProxy can load-balance TCP connections to Kafka brokers; both are infrastructure components in distributed event-driven systems
- **[NGINX](term_nginx.md)**: In event-driven microservices stacks, NGINX handles synchronous HTTP/gRPC ingress while Kafka handles asynchronous event streaming between services

### System Design
- **[Scalability](term_scalability.md)**: Kafka is horizontally scalable by adding partitions and brokers; consumer group protocol distributes partitions across consumers for read throughput scaling
- **[WebSocket](term_websocket.md)**: Kafka is used as a pub-sub backbone to fan out WebSocket messages across horizontally scaled server instances

### Distributed Transactions
- **[Saga Pattern](term_saga_pattern.md)**: Kafka serves as the event backbone for choreography-based sagas, where each service publishes domain events to Kafka topics that trigger the next saga step

### Messaging Patterns
- **[Pub/Sub](term_pub_sub.md)**: Kafka implements the pub/sub pattern via consumer groups -- fan-out across groups (pub/sub) and competing consumers within a group (point-to-point), unifying both messaging models

### Reliability and Monitoring
- **[SLI](term_sli.md)**: Service Level Indicator -- Kafka SLIs include consumer lag (freshness), throughput (messages/sec), broker uptime (availability), and end-to-end latency
- **[SLO](term_slo.md)**: Service Level Objective -- Kafka durability and consumer group resilience directly support throughput and availability SLOs for event-driven systems
- **[Throughput](term_throughput.md)**: Kafka clusters handle 1M-10M messages/second; throughput limited by disk sequential I/O and network bandwidth

### AWS / Platform
- **[Term: Kinesis](term_kinesis.md)** -- AWS managed streaming alternative to Kafka (Amazon MSK provides managed Kafka)
- **[Term: Clickstream](term_clickstream.md)** -- Common data type transported via Kafka topics
- **[Term: DataOps](term_dataops.md)** -- Operational practices for managing Kafka clusters and topics

## References

### Vault References
- [Digest: Fundamentals of Data Engineering](../digest/digest_fundamentals_data_engineering_reis.md) -- Kafka as a key ingestion and messaging technology

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media.
- Kreps, J. (2014). "I Heart Logs: Event Data, Stream Processing, and Data Integration." O'Reilly Media.
- Narkhede, N., Shapira, G., & Palino, T. (2017). *Kafka: The Definitive Guide*. O'Reilly Media.
- Apache Kafka Official: https://kafka.apache.org/
- Confluent Documentation: https://docs.confluent.io/

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Open-source distributed event streaming platform |
| **Origin** | LinkedIn (2010), Apache top-level project (2012) |
| **Core abstraction** | Distributed, partitioned, replicated commit log |
| **Throughput** | Millions of messages/second per broker |
| **Latency** | Single-digit millisecond publish-to-subscribe |
| **Durability** | Disk-persisted, replicated (configurable retention) |
| **Key components** | Brokers, Topics, Partitions, Consumer Groups, Connect, Streams |
| **Deployment** | Self-managed, Amazon MSK, Confluent Cloud |

**Key Insight**: Kafka's fundamental innovation is treating messaging as a **distributed commit log** rather than a transient queue. Traditional message brokers (RabbitMQ, ActiveMQ) delete messages after delivery, making them single-purpose pipes. Kafka's log retention means the same data can serve multiple purposes simultaneously: real-time stream processing, batch ETL backfills, audit trails, database replication (CDC), and event sourcing -- all from the same topic. This "store and process" duality is why Kafka evolved from a messaging system into the central nervous system of modern data architectures. The partition model provides horizontal scalability and ordering guarantees, while consumer groups enable parallel processing with exactly-once semantics per consumer group.

---

**Last Updated**: March 22, 2026
**Status**: Active - foundational event streaming platform in data engineering
