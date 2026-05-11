---
tags:
  - resource
  - terminology
  - data_engineering
  - streaming
  - real_time
  - distributed_computing
keywords:
  - stream processing
  - real-time processing
  - event streaming
  - unbounded data
  - windowing
  - watermarks
  - event time
  - micro-batch
  - Kafka
  - Flink
topics:
  - data engineering
  - data processing paradigms
  - real-time analytics
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Stream Processing

## Definition

**Stream processing** is a data processing paradigm in which data records are ingested, analyzed, transformed, and acted upon continuously as they arrive, rather than being collected into batches for periodic processing. In stream processing, data is modeled as an **unbounded, continuously arriving sequence of events** -- each record is processed individually or in small windows, enabling real-time or near-real-time insights and actions. This paradigm is essential for use cases where latency matters: fraud detection, real-time monitoring, live dashboards, IoT sensor analysis, and operational alerting. Stream processing introduces unique challenges around event ordering, late-arriving data, state management, and exactly-once semantics that do not arise in batch processing.

## Core Concepts

### Stream Processing Architecture

```
Event Sources              Stream Processor              Sinks / Actions
─────────────────     ──────────────────────────     ──────────────────
Clickstream events     Ingest (Kafka/Kinesis)        Real-time dashboards
Transaction logs   →   Parse & validate           →  Alerting systems
IoT sensor data        Window & aggregate            Database writes
User actions           Enrich (join with state)       ML model serving
CDC events             Apply business logic           Downstream streams
```

### Key Abstractions

| Concept | Description |
|---------|-------------|
| **Event** | An immutable record of something that happened, with a timestamp |
| **Stream** | An unbounded, ordered sequence of events |
| **Window** | A finite slice of a stream for aggregation (tumbling, sliding, session) |
| **Watermark** | A marker indicating "all events up to time T have arrived" |
| **Event time** | Timestamp embedded in the event (when it actually occurred) |
| **Processing time** | Wall-clock time when the event is processed by the system |
| **State** | Accumulated information maintained across events (counters, aggregates) |
| **Checkpoint** | Periodic snapshot of operator state for fault recovery |

### Windowing Strategies

```
Tumbling Window (fixed, non-overlapping):
  |----W1----|----W2----|----W3----|
  0         10         20         30  (seconds)

Sliding Window (fixed, overlapping):
  |----W1----|
       |----W2----|
            |----W3----|
  0    5   10   15   20   25  (seconds)

Session Window (activity-based, variable length):
  |--W1--|     |-----W2------|  |--W3--|
  events...gap..events.........gap..events
```

## Key Properties

- **Low latency**: Results available in milliseconds to seconds after event arrival, enabling real-time decision-making
- **Unbounded data**: Processes a potentially infinite stream; no concept of "all data is here"
- **Event-time processing**: Handles out-of-order and late-arriving events by reasoning about when events actually occurred, not when they were processed
- **Stateful computation**: Maintains state (counters, aggregates, ML model parameters) across events with exactly-once or at-least-once guarantees
- **Fault tolerance**: Achieves durability through checkpointing, replayable sources (Kafka offsets), and distributed snapshots
- **Backpressure**: Mechanism to slow down producers when consumers cannot keep up, preventing data loss
- **Exactly-once semantics**: Advanced frameworks (Flink, Kafka Streams) guarantee each event affects output exactly once, even during failures
- **Continuous operation**: Stream processors run indefinitely; they do not "complete" like batch jobs

## Stream Processing Frameworks

| Framework | Model | Strengths | Latency |
|-----------|-------|-----------|---------|
| **Apache Flink** | True streaming | Event-time, exactly-once, large state | Milliseconds |
| **Apache Kafka Streams** | Library-based | Embedded in apps, no cluster needed | Milliseconds |
| **Apache Spark Structured Streaming** | Micro-batch | Unified batch+stream API | Seconds |
| **Amazon Kinesis Data Analytics** | Managed Flink | Serverless, AWS-integrated | Milliseconds |
| **Apache Storm** | True streaming | Low latency, at-least-once (legacy) | Milliseconds |
| **Google Dataflow / Beam** | Unified model | Portable across runners | Variable |

## Architecture Patterns

### Lambda Architecture
Combines batch and stream processing layers:
```
                    ┌──────────────┐
                    │  Batch Layer │ (complete, accurate)
Raw Data ──────────►│  (Spark/MR)  │──────►┌──────────────┐
      │             └──────────────┘       │  Serving     │
      │             ┌──────────────┐       │  Layer       │──► Query
      └────────────►│  Speed Layer │──────►│  (merged)    │
                    │  (Flink/Storm)│       └──────────────┘
                    └──────────────┘ (fast, approximate)
```

### Kappa Architecture
Stream processing only -- batch is a special case of streaming:
```
Raw Data ──► Kafka ──► Stream Processor ──► Serving Layer ──► Query
                       (Flink / KStreams)
```

## Related Terms

### Processing Paradigms
- **[Message Queue](term_message_queue.md)**: Stream processors consume from message queues as one input source; message queues buffer events for downstream stream processing
- **[Pub/Sub](term_pub_sub.md)**: Stream processors (Flink, Kafka Streams) consume from pub/sub topics as their primary input
- **[Term: Batch Processing](term_batch_processing.md)** -- Complementary paradigm; processes bounded data in scheduled chunks
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Architectural pattern built on event streams and asynchronous processing
- **[Term: Change Data Capture](term_change_data_capture.md)** -- Captures database changes as a stream for downstream processing

### Frameworks and Platforms
- **[Term: Apache Kafka](term_kafka.md)** -- Distributed event streaming platform; primary stream transport layer
- **[Term: Apache Flink](term_flink.md)** -- True stream processing engine with event-time and exactly-once semantics
- **[Term: Apache Spark](term_spark.md)** -- Unified engine supporting micro-batch streaming (Structured Streaming)
- **[Term: Kinesis](term_kinesis.md)** -- AWS managed streaming service for real-time event ingestion

### Real-Time Communication
- **[WebSocket](term_websocket.md)**: WebSocket provides the real-time transport layer that feeds stream processing pipelines with client-side events
- **[Write-Back Cache](term_write_back_cache.md)**: The async flush in write-back caching resembles micro-batch processing in stream systems; both buffer and batch writes for throughput

### Caching and Invalidation
- **[Cache Invalidation](term_cache_invalidation.md)**: Stream processors (Kafka, Flink) can consume change events and trigger cache invalidation in real time

### Data Engineering Context
- **[Term: ETL](term_etl.md)** -- Traditional batch ETL evolving toward streaming ETL patterns
- **[Term: Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Stream processing as part of the ingestion and transformation stages
- **[Term: Clickstream](term_clickstream.md)** -- Common streaming data source (user web/app interaction events)
- **[Term: DataOps](term_dataops.md)** -- Operational practices for managing streaming pipelines
- **[Latency](term_latency.md)**: Stream processing provides low-latency event processing (milliseconds to seconds) compared to batch processing (minutes to hours)
- **[Throughput](term_throughput.md)**: Stream processing systems handle continuous high-throughput data flows with back-pressure mechanisms

## References

### Vault References
- [Digest: Fundamentals of Data Engineering](../digest/digest_fundamentals_data_engineering_reis.md) -- Streaming ingestion, transformation, and architecture patterns

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media. -- Chapters on ingestion (batch vs. streaming) and streaming systems
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapter 11: Stream Processing
- Akidau, T. et al. (2015). "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing." VLDB.

## Summary

| Aspect | Details |
|--------|---------|
| **Paradigm** | Continuous processing of records as they arrive |
| **Data model** | Unbounded, ordered event streams |
| **Latency** | Milliseconds to seconds |
| **Key challenges** | Ordering, late data, state management, exactly-once |
| **Key abstractions** | Windows, watermarks, event time, checkpoints |
| **Key frameworks** | Flink, Kafka Streams, Spark Structured Streaming, Kinesis |
| **Best for** | Fraud detection, monitoring, live dashboards, IoT, CDC |
| **Trade-off** | Lower latency in exchange for higher complexity and cost |

**Key Insight**: Stream processing fundamentally changes the data engineering mental model from "process all the data we have" to "process each datum as it arrives." The critical intellectual challenge is handling **time** -- specifically, the gap between when an event occurred (event time) and when it is processed (processing time). Watermarks, windowing, and late-arrival policies are the mechanisms that bridge this gap. Modern frameworks like Apache Flink have largely solved the correctness problem (exactly-once, event-time processing), making the choice between batch and streaming primarily a question of latency requirements and operational complexity rather than capability.

---

**Last Updated**: March 22, 2026
**Status**: Active - foundational data processing paradigm for real-time data engineering
