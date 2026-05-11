---
tags:
  - resource
  - terminology
  - data_engineering
  - data_pipeline
  - distributed_computing
keywords:
  - batch processing
  - ETL
  - scheduled processing
  - data pipeline
  - bulk data
  - offline processing
  - data warehouse
  - Datanet
  - Cradle
topics:
  - data engineering
  - data processing paradigms
  - analytics infrastructure
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Batch Processing

## Definition

**Batch processing** is a data processing paradigm in which data is collected over a period of time and then processed as a discrete, finite group (a "batch") at a scheduled interval, rather than being handled continuously as it arrives. This is the traditional paradigm for ETL workflows, data warehousing, and analytics pipelines. In batch processing, jobs run on a defined schedule (hourly, daily, weekly), process all accumulated data in one execution, and produce results that become available only after the entire batch completes. Batch processing trades latency for throughput, simplicity, and cost efficiency -- making it the dominant pattern for workloads where real-time results are not required, such as financial reconciliation, ML model training, regulatory reporting, and historical analytics.

## Core Concepts

### Batch Processing Workflow

```
Data Accumulation          Batch Execution              Results Available
─────────────────     ──────────────────────────     ──────────────────
Events arrive         Scheduler triggers job         Output tables updated
  continuously        Job reads accumulated data     Dashboards refresh
Data written to       Transform (clean/join/agg)     ML training kicks off
  staging area        Write to target warehouse      Reports generated
```

### Batch vs. Stream Processing Comparison

| Dimension | Batch Processing | Stream Processing |
|-----------|-----------------|-------------------|
| **Data scope** | Finite, bounded dataset | Unbounded, continuous flow |
| **Latency** | Minutes to hours | Milliseconds to seconds |
| **Throughput** | Very high (optimized for bulk) | Variable (per-record overhead) |
| **Complexity** | Lower (simpler state mgmt) | Higher (windowing, watermarks) |
| **Cost** | Lower (off-peak, shared resources) | Higher (always-on infrastructure) |
| **Error handling** | Reprocess entire batch | Complex (exactly-once, retries) |
| **Use cases** | ETL, reporting, ML training | Fraud detection, monitoring |

### Scheduling Patterns

```
┌─────────────────────────────────────────────────────────┐
│              Batch Scheduling Strategies                  │
├──────────────┬──────────────────────────────────────────┤
│ Time-based   │ Cron: "0 2 * * *" (daily at 2 AM)       │
│ Event-based  │ Triggered when upstream job completes     │
│ Dependency   │ DAG-based: run after all parents finish   │
│ Hybrid       │ Micro-batch: small batches every 5-15 min │
└──────────────┴──────────────────────────────────────────┘
```

## Key Properties

- **Bounded data**: Operates on a finite, well-defined dataset with a clear beginning and end
- **High throughput**: Optimized for processing large volumes efficiently by amortizing setup costs across many records
- **Latency tolerance**: Results are delayed until the entire batch completes -- acceptable when freshness requirements are measured in hours or days
- **Idempotency**: Well-designed batch jobs are re-runnable without side effects; reprocessing a batch produces the same output
- **Resource efficiency**: Can run during off-peak hours, using spot instances or shared compute clusters
- **Simpler error recovery**: If a batch fails, rerun the entire batch; no need for complex checkpoint/offset management
- **Backfill capability**: Historical data can be reprocessed by re-running batch jobs over past time ranges
- **Sequential dependencies**: Jobs form DAGs where downstream jobs wait for upstream completion before starting

## Common Batch Processing Frameworks

| Framework | Type | Scale | Key Feature |
|-----------|------|-------|-------------|
| **Apache Spark** | Distributed engine | Petabyte-scale | In-memory processing, DAG optimization |
| **Apache Hadoop (MapReduce)** | Distributed engine | Petabyte-scale | Disk-based, fault-tolerant |
| **dbt** | SQL transformation | Warehouse-scale | Declarative SQL transforms |
| **Apache Airflow** | Orchestrator | Any | DAG-based workflow scheduling |
| **AWS Glue** | Managed ETL | Cloud-scale | Serverless Spark |
| **Datanet/ETLM** | SQL ETL | Redshift-scale | Cron + dependency tracking |
| **Cradle** | Spark ETL | 50TB+ | Distributed S3/Andes processing |

## Batch Processing Anti-Patterns

- **Unbounded batch growth**: Batch size grows faster than processing capacity, causing cascading delays
- **Tight coupling**: Downstream jobs assume specific completion times rather than using dependency triggers
- **Missing idempotency**: Jobs that insert without deduplication, producing duplicates on rerun
- **Monolithic batches**: Single massive job instead of decomposed, independently retriable stages

## Related Terms

### Processing Paradigms
- **[Message Queue](term_message_queue.md)**: Message queues shift processing from scheduled batches to continuous, event-triggered consumption; contrasting paradigm to batch processing
- **[Term: Stream Processing](term_stream_processing.md)** -- Continuous processing counterpart; handles unbounded data in real-time
- **[Term: MapReduce](term_mapreduce.md)** -- Original distributed batch processing model (Google, 2004)
- **[Term: ETL](term_etl.md)** -- Extract, Transform, Load; the canonical batch processing workflow pattern

### Frameworks and Platforms
- **[Term: Apache Spark](term_spark.md)** -- Dominant engine for modern batch (and micro-batch) processing
- **[Term: Cradle](term_cradle.md)** -- Amazon's Spark-based batch ETL platform for large-scale processing
- **[Term: Kinesis](term_kinesis.md)** -- AWS streaming platform; contrast with batch patterns
- **[Term: Directed Acyclic Graph](term_directed_acyclic_graph.md)** -- DAG structure used to model batch job dependencies

### Architecture
- **[Term: Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Batch processing as a core stage in the data lifecycle
- **[Term: DataOps](term_dataops.md)** -- Operational practices for managing batch (and streaming) pipelines
- **[Term: Data Parallelism](term_data_parallelism.md)** -- Parallelization strategy used within batch frameworks

### Performance
- **[Latency](term_latency.md)**: Batch processing sacrifices per-item latency for aggregate processing efficiency — items wait to fill a batch
- **[Throughput](term_throughput.md)**: Batch processing maximizes throughput by amortizing per-request overhead across multiple items
- **[TPS](term_tps.md)**: Alternative to real-time TPS — processes data in bulk with higher aggregate throughput but delayed results

## References

### Vault References
- [Digest: Fundamentals of Data Engineering](../digest/digest_fundamentals_data_engineering_reis.md) -- Chapter coverage of batch ingestion patterns and orchestration

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media. -- Chapters on ingestion, transformation, and orchestration
- Dean, J. & Ghemawat, S. (2004). "MapReduce: Simplified Data Processing on Large Clusters." OSDI.
- AWS Documentation: https://aws.amazon.com/batch/

## Summary

| Aspect | Details |
|--------|---------|
| **Paradigm** | Process data in discrete, scheduled chunks |
| **Data model** | Bounded, finite datasets |
| **Latency** | Minutes to hours |
| **Throughput** | Very high (bulk-optimized) |
| **Scheduling** | Cron, event-triggered, or DAG-based |
| **Key frameworks** | Spark, Hadoop MapReduce, dbt, Airflow, Cradle, Datanet |
| **Best for** | ETL, reporting, ML training, reconciliation, backfills |
| **Trade-off** | Higher latency in exchange for simplicity, cost, and throughput |

**Key Insight**: Batch processing remains the workhorse of data engineering despite the rise of streaming. The majority of analytical workloads -- ML model training, financial reporting, data warehouse population -- are inherently batch-oriented because they require complete, consistent snapshots of data rather than incremental updates. The modern trend is not to replace batch with streaming, but to use both: streaming for latency-sensitive operational use cases and batch for throughput-intensive analytical workloads. Frameworks like Apache Spark blur this boundary with "micro-batch" processing (Structured Streaming), where small batches run at sub-minute intervals, offering a pragmatic middle ground.

---

**Last Updated**: March 22, 2026
**Status**: Active - foundational data processing paradigm in data engineering
