---
tags:
  - resource
  - terminology
  - data_engineering
  - data_integration
  - streaming
keywords:
  - Change Data Capture
  - CDC
  - database replication
  - log-based CDC
  - Debezium
  - Kafka Connect
  - event-driven architecture
  - data synchronization
  - transaction log
  - real-time ingestion
topics:
  - data engineering
  - data integration
  - database replication
  - event-driven architecture
  - streaming
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Change Data Capture (CDC)

## Definition

**Change Data Capture (CDC)** is a data integration pattern for identifying and capturing changes -- inserts, updates, and deletes -- made to data in a source database, then delivering those changes as an ordered stream of events to downstream systems in real-time or near-real-time. Rather than re-extracting entire datasets on a schedule (as in traditional batch ETL), CDC captures only the *deltas*, making it far more efficient for keeping systems in sync. In the **Data Engineering Lifecycle** (as described by Reis & Housley), CDC is a key **ingestion pattern** that sits between source systems and the storage/transformation layers, enabling event-driven data pipelines that minimize latency and source system load.

## Core Concepts

### Why CDC Exists

Traditional batch-oriented data movement (full table dumps, scheduled queries) suffers from three problems:
1. **Latency** -- downstream systems only see changes after the next batch run
2. **Load** -- re-reading entire tables wastes compute on the source database
3. **Lost deletes** -- full extracts cannot distinguish a deleted row from one that was never there

CDC solves all three by tapping into the database's own record of what changed, when, and how.

### The Three Main Approaches

| Approach | Mechanism | Pros | Cons |
|----------|-----------|------|------|
| **Log-based** | Reads the database transaction log (WAL, binlog, redo log) | Lowest overhead on source; captures all change types including deletes; preserves commit order | Requires access to internal logs; implementation varies by database engine |
| **Timestamp-based** (query-based) | Polls tables for rows where `updated_at > last_check` | Simple to implement; no special database permissions needed | Cannot capture hard deletes; adds query load to source; may miss changes between polls |
| **Trigger-based** | Database triggers fire on INSERT/UPDATE/DELETE, writing changes to shadow tables | Works on any database that supports triggers; captures deletes | Significant performance overhead (extra write per operation); tight coupling to schema; complex to maintain |

**Log-based CDC is the industry-standard approach for production systems.** It provides the best combination of low overhead, completeness (captures deletes), and ordering guarantees. The other two approaches are generally used only when transaction log access is unavailable.

### How Log-Based CDC Works

```
Source Database                CDC Connector              Message Broker / Target
───────────────             ─────────────────           ─────────────────────────
Application writes  ──→  Transaction Log (WAL/binlog)
                              │
                         CDC process reads log
                         and emits change events
                              │
                              ├──→  Kafka topic (one per table)
                              │         │
                              │         ├──→ Data warehouse (analytics)
                              │         ├──→ Search index (Elasticsearch)
                              │         ├──→ Cache (Redis)
                              │         └──→ Microservice (event consumer)
                              │
                              └──→  Direct replication target
```

Each change event typically contains:
- **Operation type**: INSERT, UPDATE, or DELETE
- **Before image**: the row state before the change (for updates and deletes)
- **After image**: the row state after the change (for inserts and updates)
- **Source metadata**: transaction ID, timestamp, table name, schema version

## Key Implementations

### Debezium (Open Source)

The most widely adopted open-source CDC platform. Built on **Apache Kafka Connect**, Debezium provides source connectors for PostgreSQL, MySQL, MongoDB, SQL Server, Oracle, and others. It reads database transaction logs, converts row-level changes into structured JSON events, and publishes them to Kafka topics (one topic per table). Downstream consumers -- Kafka Streams, Apache Flink, sink connectors -- can process events at their own pace without affecting the source database.

### Other Notable Platforms

| Platform | Type | Notes |
|----------|------|-------|
| **AWS Database Migration Service (DMS)** | Managed service | Supports CDC for migrations and ongoing replication to Redshift, S3, Kinesis |
| **Oracle GoldenGate** | Commercial | Enterprise-grade log-based CDC for Oracle and heterogeneous databases |
| **Fivetran / Airbyte** | Managed / open-source | SaaS and self-hosted connectors with built-in CDC modes |
| **Kafka Connect (JDBC)** | Open source | Timestamp/incrementing-column based; simpler but less capable than Debezium |
| **Maxwell's Daemon** | Open source | Lightweight MySQL binlog reader; outputs to Kafka, Kinesis, or other targets |

## CDC vs ETL vs Streaming

| Dimension | Batch ETL | CDC | Pure Streaming |
|-----------|-----------|-----|----------------|
| **Data scope** | Full table or large partition | Only changed rows | Individual events |
| **Latency** | Minutes to hours | Seconds to minutes | Milliseconds |
| **Source impact** | High (full scan) | Low (log read) | None (producer pushes) |
| **Delete capture** | Difficult | Native | N/A (events are appends) |
| **Ordering** | Per-batch | Per-transaction | Per-partition |
| **Typical use** | Warehouse loads, ML training | Database replication, cache sync | Real-time analytics, alerting |

CDC occupies a middle ground: it is *event-driven* like streaming but *database-aware* like ETL. In modern data stacks, CDC often feeds into streaming platforms (Kafka) which then drive both real-time consumers and batch warehouse loads.

## Common Use Cases

1. **Database replication** -- keep read replicas, analytics databases, or data warehouses in sync with OLTP sources
2. **Cache invalidation** -- update Redis or Memcached when underlying database rows change
3. **Search index sync** -- propagate changes to Elasticsearch or OpenSearch without dual writes
4. **Microservice integration** -- publish domain events from a service's database to an event bus (the "outbox pattern")
5. **Data lake ingestion** -- stream incremental changes to S3/data lake instead of periodic full dumps
6. **Audit and compliance** -- capture a complete, ordered history of all data modifications

## Tradeoffs and Considerations

**Advantages**:
- Minimal impact on source database performance (log-based)
- Near-real-time data availability in downstream systems
- Captures all change types, including deletes
- Preserves transaction order and consistency
- Reduces data transfer volume (deltas only)

**Challenges**:
- Schema evolution requires careful handling (schema registry recommended)
- Initial snapshot of existing data needed before streaming begins
- Transaction log retention limits (logs may be purged before CDC catches up)
- Exactly-once delivery semantics are hard to achieve end-to-end
- Operational complexity of managing connectors, Kafka, and consumer offsets

## Related Terms

- **[Message Queue](term_message_queue.md)**: CDC events are commonly published to message queues or event streams (via Debezium + Kafka) for downstream consumption
- **[Pub/Sub](term_pub_sub.md)**: Database changes published to pub/sub topics for downstream consumption is a key CDC delivery pattern
- **[Cache Invalidation](term_cache_invalidation.md)**: CDC streams database changes as events, enabling real-time cache invalidation without coupling the write path to cache logic
- **[Database Replication](term_database_replication.md)**: CDC reads the replication log (WAL/binlog) to stream changes to downstream systems -- replication and CDC share the same underlying log infrastructure
- **[Term: ETL - Extract, Transform, Load](term_etl.md)** -- the traditional batch pattern that CDC complements or replaces for incremental data movement
- **[Term: Clickstream](term_clickstream.md)** -- a streaming data source that, like CDC, feeds event-driven pipelines
- **[Term: Traffic Stream](term_traffic_stream.md)** -- another streaming concept relevant to real-time data flow
- **[Write-Back Cache](term_write_back_cache.md)**: CDC can capture the eventual database writes from write-back caching, enabling downstream systems to react to data changes that were initially buffered in cache
- **[Saga Pattern](term_saga_pattern.md)**: CDC enables the transactional outbox pattern for sagas -- local transactions write domain events to an outbox table, and CDC streams those events to the message broker for saga orchestration

## References

### Books
- **[Digest: Fundamentals of Data Engineering (Reis & Housley)](../digest/digest_fundamentals_data_engineering_reis.md)** -- covers CDC as a key ingestion pattern in the Data Engineering Lifecycle

### External Resources
- [What is Change Data Capture (CDC)? - Confluent](https://www.confluent.io/learn/change-data-capture/)
- [Change Data Capture - Wikipedia](https://en.wikipedia.org/wiki/Change_data_capture)
- [Debezium Documentation](https://debezium.io/documentation/)
- [CDC Fundamentals - Conduktor](https://conduktor.io/glossary/what-is-change-data-capture-cdc-fundamentals)
- [Change Data Capture: What It Is and How It Works - Striim](https://www.striim.com/blog/change-data-capture-cdc-what-it-is-and-how-it-works/)

## Summary

**CDC Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Change Data Capture |
| **Abbreviation** | CDC |
| **Primary Approach** | Log-based (reads database transaction log) |
| **Leading OSS Tool** | Debezium (on Kafka Connect) |
| **Managed Alternatives** | AWS DMS, Oracle GoldenGate, Fivetran |
| **Change Types Captured** | INSERT, UPDATE, DELETE |
| **Typical Latency** | Seconds to low minutes |
| **Key Advantage** | Low-overhead, real-time, delete-aware data replication |

**Key Insight**: CDC transforms a database from a passive store into an active event emitter. By treating the transaction log as an event stream, CDC enables the same database to serve both OLTP workloads and feed real-time analytics, search indexes, caches, and downstream microservices -- without the source application needing to know about any of those consumers. This "turning the database inside out" pattern (as coined by Martin Kleppmann) is foundational to modern event-driven and streaming architectures.

---

**Last Updated**: March 22, 2026
**Status**: Active - foundational data integration pattern for real-time data replication and event-driven architectures
