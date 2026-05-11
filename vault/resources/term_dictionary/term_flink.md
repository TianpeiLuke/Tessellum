---
tags:
  - resource
  - terminology
  - data_engineering
  - streaming
  - distributed_computing
  - open_source
keywords:
  - Apache Flink
  - Flink
  - stream processing
  - event-time processing
  - exactly-once semantics
  - watermarks
  - checkpointing
  - stateful computation
  - DataStream API
  - distributed snapshots
topics:
  - data engineering
  - stream processing frameworks
  - distributed computing
  - real-time analytics
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Apache Flink

## Definition

**Apache Flink** is an open-source distributed stream processing framework designed for stateful computations over unbounded (streaming) and bounded (batch) data. Developed at the Technical University of Berlin as the "Stratosphere" research project starting in 2010, Flink became an Apache top-level project in 2014. Flink's defining characteristic is **true event-at-a-time stream processing** with **exactly-once state consistency** -- unlike Spark's micro-batch approach, Flink processes each event individually as it arrives, enabling millisecond-level latency while maintaining strong correctness guarantees. Flink achieves fault tolerance through a distributed snapshot algorithm (based on Chandy-Lamport), advanced event-time processing via watermarks, and managed state with incremental checkpointing. It treats batch processing as a special case of streaming (a bounded stream), making it a truly stream-first unified engine. Flink is widely used for real-time analytics, complex event processing, fraud detection, and mission-critical streaming applications.

## Core Concepts

### Flink Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Flink Cluster                         │
│                                                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │               JobManager (Master)                 │    │
│  │  • Receives job graph (JobGraph)                  │    │
│  │  • Coordinates checkpoints                        │    │
│  │  • Manages task scheduling                        │    │
│  │  • Handles failure recovery                       │    │
│  └──────────────────────────────────────────────────┘    │
│          ↓              ↓              ↓                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │TaskManager │  │TaskManager │  │TaskManager │         │
│  │ (Worker)   │  │ (Worker)   │  │ (Worker)   │         │
│  │ • Task     │  │ • Task     │  │ • Task     │         │
│  │   Slots    │  │   Slots    │  │   Slots    │         │
│  │ • State    │  │ • State    │  │ • State    │         │
│  │   Backend  │  │   Backend  │  │   Backend  │         │
│  └────────────┘  └────────────┘  └────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### Event Time vs. Processing Time

```
Event occurs    Network delay    Event arrives    Event processed
    │                                │                 │
    ▼                                ▼                 ▼
────●────────────────────────────────●─────────────────●────► time
    │                                │                 │
    └── Event Time                   └── Ingestion     └── Processing
        (embedded in event)              Time               Time

Flink processes based on EVENT TIME:
  → Correct results even with out-of-order or late events
  → Watermarks track progress of event time across the stream
```

### Checkpointing and Exactly-Once

```
Stream: ──[e1]──[e2]──[e3]──║──[e4]──[e5]──║──[e6]──[e7]──►
                             ║              ║
                          Barrier 1      Barrier 2

Checkpoint Barriers flow through the data stream:
  1. JobManager injects barrier into source
  2. Barrier propagates through all operators
  3. Each operator snapshots its state when barrier passes
  4. State persisted to durable storage (S3, HDFS)
  5. On failure: restart from last completed checkpoint
     → Each event affects output EXACTLY ONCE
```

### Watermarks and Late Data

| Concept | Description |
|---------|-------------|
| **Watermark** | Assertion: "no events with timestamp < W will arrive after this point" |
| **Allowed lateness** | Grace period after watermark for late events (configurable) |
| **Side output** | Channel for extremely late events that miss the lateness window |
| **Idle sources** | Sources with no data; Flink advances watermark past them |

```
Events:     [t=3] [t=1] [t=5] [t=2] [t=7]   ← out of order
Watermark:          W=1        W=2     W=5    ← advances conservatively
Window [0,5):       accumulating...     FIRE!  ← triggered when W >= 5
```

## Key Properties

- **True streaming**: Processes events one at a time (not micro-batch), enabling sub-second latency for stateful computations
- **Event-time processing**: First-class support for reasoning about when events occurred, independent of arrival order or processing delays
- **Exactly-once state consistency**: Distributed snapshot algorithm guarantees each event affects application state exactly once, even during failures
- **Managed state**: Flink manages operator state (keyed state, operator state) with pluggable backends (memory, RocksDB, HashMapStateBackend)
- **Incremental checkpoints**: Only persists state changes since the last checkpoint, enabling checkpointing of terabyte-scale state
- **Savepoints**: Manually triggered, portable snapshots for application upgrades, migrations, and A/B testing
- **Backpressure handling**: Natural backpressure through network buffer pool; slow operators automatically throttle upstream
- **Batch as streaming**: Bounded datasets are processed as finite streams, sharing the same runtime and optimizations
- **Rich windowing**: Tumbling, sliding, session, and custom windows with flexible triggers and eviction policies
- **Connectors**: Native integration with Kafka, Kinesis, Pulsar, JDBC, Elasticsearch, S3, HDFS, and more

## Flink APIs

| API Level | Abstraction | Use Case |
|-----------|-------------|----------|
| **SQL / Table API** | Declarative SQL | Analytics, ETL, ad-hoc queries |
| **DataStream API** | Event-level control | Custom stateful processing, CEP |
| **ProcessFunction** | Low-level event access | Timers, side outputs, raw state |
| **Stateful Functions (StateFun)** | Distributed functions | Microservice-style stateful apps |

## Flink vs. Other Engines

| Dimension | Flink | Spark Streaming | Kafka Streams | Storm |
|-----------|-------|-----------------|---------------|-------|
| **Model** | True streaming | Micro-batch | True streaming | True streaming |
| **Latency** | Milliseconds | Seconds | Milliseconds | Milliseconds |
| **State management** | Rich, managed | Limited | Embedded (RocksDB) | Minimal |
| **Exactly-once** | Yes (checkpoints) | Yes (micro-batch) | Yes (transactions) | No (at-least-once) |
| **Event time** | First-class | Supported | Supported | Limited |
| **Batch support** | Yes (stream-first) | Yes (batch-first) | No | No |
| **Deployment** | Cluster or K8s | Cluster | Embedded in app | Cluster |

## Related Terms

### Stream Processing
- **[Term: Stream Processing](term_stream_processing.md)** -- The processing paradigm Flink implements with true event-at-a-time semantics
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Flink powers event-driven applications with stateful stream processing
- **[Term: Apache Kafka](term_kafka.md)** -- Primary event transport for Flink applications (Kafka source/sink connectors)

### Processing Engines
- **[Term: Apache Spark](term_spark.md)** -- Alternative unified engine using micro-batch for streaming (contrast with Flink's true streaming)
- **[Term: MapReduce](term_mapreduce.md)** -- Predecessor batch-only model that Flink (and Spark) superseded
- **[Term: Batch Processing](term_batch_processing.md)** -- Flink treats batch as a special case of streaming (bounded streams)

### Data Engineering
- **[Term: ETL](term_etl.md)** -- Flink enables streaming ETL with exactly-once guarantees
- **[Term: Change Data Capture](term_change_data_capture.md)** -- Flink CDC connectors enable streaming database replication
- **[Term: Kinesis](term_kinesis.md)** -- AWS streaming source; Flink has native Kinesis connectors (also Amazon Managed Flink)
- **[Term: Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Flink as a transformation and serving engine in the lifecycle
- **[Term: Directed Acyclic Graph](term_directed_acyclic_graph.md)** -- Flink's job graph is a DAG of operators with dataflow edges
- **[Term: Data Parallelism](term_data_parallelism.md)** -- Flink parallelizes operators across task slots by key partitioning

## References

### Vault References
- [Digest: Fundamentals of Data Engineering](../digest/digest_fundamentals_data_engineering_reis.md) -- Coverage of streaming frameworks and real-time processing

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media.
- Carbone, P. et al. (2015). "Apache Flink: Stream and Batch Processing in a Single Engine." *IEEE Data Engineering Bulletin*, 38(4).
- Hueske, F. & Kalavri, V. (2019). *Stream Processing with Apache Flink*. O'Reilly Media.
- Apache Flink Official: https://flink.apache.org/
- Chandy, K.M. & Lamport, L. (1985). "Distributed Snapshots: Determining Global States of Distributed Systems." *ACM TOCS*, 3(1).

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Open-source distributed stream processing framework |
| **Origin** | TU Berlin Stratosphere project (2010), Apache top-level (2014) |
| **Core model** | True event-at-a-time streaming (batch as bounded stream) |
| **Latency** | Milliseconds (true streaming, not micro-batch) |
| **Fault tolerance** | Distributed snapshots with exactly-once state consistency |
| **State** | Managed, keyed state with RocksDB or heap backends |
| **Event-time** | First-class watermarks, late data handling, session windows |
| **APIs** | SQL, Table, DataStream, ProcessFunction, StateFun |

**Key Insight**: Flink's intellectual contribution to stream processing is the rigorous separation of **event time** from **processing time** combined with **exactly-once state consistency** via distributed snapshots. Most early streaming systems (Storm, Spark Streaming) either sacrificed correctness for speed or sacrificed speed for correctness. Flink proved you can have both: millisecond latency AND exactly-once guarantees AND correct event-time semantics. The watermark mechanism -- a pragmatic solution to the fundamental impossibility of knowing "all data has arrived" in a distributed system -- allows developers to make explicit tradeoffs between completeness and latency. This is why Flink has become the engine of choice for mission-critical streaming workloads where both speed and correctness are non-negotiable, such as financial fraud detection, real-time billing, and safety-critical monitoring.

---

**Last Updated**: March 22, 2026
**Status**: Active - leading stream processing framework in data engineering
