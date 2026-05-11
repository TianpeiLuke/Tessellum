---
tags:
  - resource
  - terminology
  - data_engineering
  - distributed_computing
  - big_data
  - open_source
keywords:
  - Apache Spark
  - Spark
  - RDD
  - DataFrame
  - DAG
  - Catalyst optimizer
  - distributed processing
  - PySpark
  - Spark SQL
  - Structured Streaming
topics:
  - data engineering
  - distributed computing
  - big data processing
  - analytics engines
language: markdown
date of note: 2026-03-22
status: active
building_block: concept
---

# Term: Apache Spark

## Definition

**Apache Spark** is an open-source, unified analytics engine for large-scale distributed data processing. Originally developed at UC Berkeley's AMPLab in 2009 by Matei Zaharia, Spark was designed to overcome the limitations of Hadoop MapReduce -- particularly its inefficiency with iterative algorithms and interactive queries due to repeated disk I/O. Spark's core innovation is **in-memory computation**: intermediate results are kept in memory across processing stages rather than written to disk, yielding 10-100x performance improvements over MapReduce for many workloads. Spark provides a unified API for batch processing, stream processing (Structured Streaming), SQL analytics (Spark SQL), machine learning (MLlib), and graph processing (GraphX), making it the dominant engine in modern data engineering stacks. Over 80% of Fortune 500 companies use Apache Spark.

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Driver Program                     │
│  ┌───────────────────────────────────────────────┐   │
│  │            SparkContext / SparkSession         │   │
│  │  • Builds DAG of transformations              │   │
│  │  • Submits jobs to Cluster Manager            │   │
│  └───────────────────────────────────────────────┘   │
│                        ↓                              │
│  ┌───────────────────────────────────────────────┐   │
│  │            Cluster Manager                     │   │
│  │  (YARN / Mesos / Kubernetes / Standalone)      │   │
│  └───────────────────────────────────────────────┘   │
│          ↓              ↓              ↓              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │ Executor  │  │ Executor  │  │ Executor  │        │
│  │ (Worker)  │  │ (Worker)  │  │ (Worker)  │        │
│  │ • Tasks   │  │ • Tasks   │  │ • Tasks   │        │
│  │ • Cache   │  │ • Cache   │  │ • Cache   │        │
│  └───────────┘  └───────────┘  └───────────┘        │
└─────────────────────────────────────────────────────┘
```

### Spark Ecosystem Components

| Component | Purpose | API |
|-----------|---------|-----|
| **Spark Core** | Distributed task scheduling, memory management, fault recovery | RDD API |
| **Spark SQL** | Structured data processing with SQL and DataFrames | SQL, DataFrame, Dataset |
| **Structured Streaming** | Incremental micro-batch stream processing | DataFrame API (streaming) |
| **MLlib** | Distributed machine learning algorithms | ML Pipeline API |
| **GraphX** | Graph computation and analytics | Graph API |
| **Pandas API on Spark** | pandas-compatible API for distributed data | pandas API |

### Data Abstractions Evolution

```
Spark 1.x                Spark 2.x+               Spark 3.x+
─────────────          ─────────────            ─────────────
RDD (2012)         →   DataFrame (2015)     →   Unified DataFrame
• Low-level            • Schema-aware             • Catalyst v2
• Manual optimization  • Catalyst optimizer        • Adaptive Query
• Type-safe            • Tungsten engine              Execution (AQE)
• Functional API       • SQL interface              • Dynamic partition
                                                       pruning
```

### DAG Execution Model

```
Transformations (lazy)              Actions (trigger execution)
──────────────────────              ──────────────────────────
map, filter, join,                  count, collect, save,
groupBy, select, where              show, write, foreach
        │                                    │
        ▼                                    ▼
   Build DAG of stages              Submit DAG to scheduler
   (logical plan)                   (physical plan → tasks)
        │                                    │
        ▼                                    ▼
   Catalyst Optimizer               Execute across cluster
   (rule-based + cost-based)        (parallelize by partition)
```

## Key Properties

- **In-memory computation**: Caches intermediate data in RAM, avoiding costly disk I/O between stages; 10-100x faster than MapReduce for iterative workloads
- **Lazy evaluation**: Transformations build a logical plan (DAG) without executing; execution only occurs when an action is called, enabling whole-pipeline optimization
- **Fault tolerance**: RDDs track lineage (the sequence of transformations); lost partitions are recomputed from source data, not replicated
- **Unified engine**: Single API and runtime for batch, streaming, SQL, ML, and graph processing -- reducing operational complexity
- **Catalyst optimizer**: Rule-based and cost-based SQL query optimizer that rewrites logical plans into efficient physical execution plans
- **Tungsten engine**: Off-heap memory management and code generation for CPU-efficient execution
- **Adaptive Query Execution (AQE)**: Spark 3.0+ dynamically adjusts query plans at runtime based on observed data statistics
- **Multi-language support**: Native APIs in Scala, Java, Python (PySpark), R, and SQL
- **Broad ecosystem**: Integrates with HDFS, S3, Kafka, Hive, Delta Lake, Iceberg, Cassandra, and hundreds of connectors

## Spark vs. Other Engines

| Dimension | Spark | MapReduce | Flink | Presto/Trino |
|-----------|-------|-----------|-------|-------------|
| **Processing model** | Batch + micro-batch | Batch only | True streaming + batch | Interactive SQL |
| **Speed** | Fast (in-memory) | Slow (disk-based) | Fast (streaming) | Fast (in-memory SQL) |
| **Streaming** | Micro-batch (Structured Streaming) | None | True event-at-a-time | None |
| **State** | Limited | None | Rich, managed state | None |
| **ML** | MLlib | Mahout (deprecated) | FlinkML (limited) | None |
| **Maturity** | Very high | Legacy | Growing | High (SQL only) |

## Related Terms

### Processing Paradigms
- **[Term: Batch Processing](term_batch_processing.md)** -- Spark's primary processing mode; processes bounded datasets
- **[Term: Stream Processing](term_stream_processing.md)** -- Spark Structured Streaming provides micro-batch stream processing
- **[Term: MapReduce](term_mapreduce.md)** -- Predecessor model that Spark was designed to replace

### Architecture and Concepts
- **[Term: Directed Acyclic Graph](term_directed_acyclic_graph.md)** -- DAG is Spark's core execution model for scheduling stages and tasks
- **[Term: Data Parallelism](term_data_parallelism.md)** -- Spark distributes data across partitions for parallel processing
- **[Term: ETL](term_etl.md)** -- Spark is a primary engine for ETL/ELT workloads
- **[Term: Cradle](term_cradle.md)** -- Amazon's Spark-based ETL platform built on top of Apache Spark

### Ecosystem
- **[Term: Apache Kafka](term_kafka.md)** -- Common streaming source for Spark Structured Streaming
- **[Term: Apache Flink](term_flink.md)** -- Alternative engine with true streaming (vs. Spark's micro-batch)
- **[Term: Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Spark spans ingestion, transformation, and serving stages
- **[Term: DataOps](term_dataops.md)** -- Operational practices for managing Spark pipelines at scale

## References

### Vault References
- [Digest: Fundamentals of Data Engineering](../digest/digest_fundamentals_data_engineering_reis.md) -- Coverage of Spark as a transformation and processing engine

### External References
- Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media.
- Zaharia, M. et al. (2016). "Apache Spark: A Unified Engine for Big Data Processing." *Communications of the ACM*, 59(11).
- Apache Spark Official: https://spark.apache.org/
- Damji, J. et al. (2020). *Learning Spark*, 2nd Edition. O'Reilly Media.

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Open-source unified analytics engine |
| **Origin** | UC Berkeley AMPLab (2009), Apache top-level project (2014) |
| **Core innovation** | In-memory distributed computation with DAG-based execution |
| **APIs** | Scala, Java, Python (PySpark), R, SQL |
| **Components** | Spark SQL, Structured Streaming, MLlib, GraphX |
| **Optimization** | Catalyst (query planner) + Tungsten (execution engine) + AQE |
| **Cluster managers** | YARN, Mesos, Kubernetes, Standalone |
| **Data sources** | HDFS, S3, Kafka, Hive, Delta Lake, Iceberg, JDBC, and more |

**Key Insight**: Spark's enduring dominance stems not from any single capability but from its **unification** -- one engine, one API, one cluster for batch, streaming, SQL, ML, and graph workloads. Before Spark, organizations needed separate systems for each paradigm (MapReduce for batch, Storm for streaming, Hive for SQL, Mahout for ML), each with its own operational overhead and data movement costs. Spark collapsed these into a single runtime with a consistent DataFrame abstraction. The Catalyst optimizer and lazy evaluation model mean that declarative, high-level code (SQL or DataFrame operations) is automatically optimized into efficient physical plans -- bridging the gap between developer productivity and execution performance.

---

**Last Updated**: March 22, 2026
**Status**: Active - dominant distributed data processing engine in modern data engineering
