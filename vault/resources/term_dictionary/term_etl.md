---
tags:
  - resource
  - terminology
  - data_engineering
  - data_pipeline
keywords:
  - ETL
  - Extract Transform Load
  - ELT
  - data pipeline
  - data warehouse
  - data engineering
topics:
  - data engineering
  - data pipelines
  - analytics infrastructure
language: markdown
date of note: 2026-03-02
status: active
building_block: concept
---

# Term: ETL - Extract, Transform, Load

## Definition

**ETL** (Extract, Transform, Load) is the data engineering pattern for moving data between systems: **extracting** raw data from source systems (event streams, batch feeds, catalogs, external APIs), **transforming** it by cleaning, aggregating, joining, and enriching it according to business logic, and **loading** it into target warehouses or catalogs for analytics and ML consumption. ETL pipelines are the backbone of most analytics and ML data stacks — converting raw events into structured, ML-ready features and ground-truth labels.

## Core Concepts

### The ETL Process

```
Source Systems                  Transform                     Target
─────────────────────     ──────────────────────────     ──────────────
Event streams (RT)     →  Clean / deduplicate         →  Data warehouse
Batch feeds            →  Join tables                 →  ML training store
Catalog datasets       →  Aggregate / window          →  Enriched catalog
Operational systems    →  Apply business logic        →  Feature store
Labeling data          →  Add ground truth labels     →  Feature store
```

**Extract**: Pull data from upstream sources at defined cadences (real-time via streaming, daily batch, or on-demand via API)

**Transform**: Apply SQL/Spark logic to clean, enrich, and reshape data:
- Join fact and dimension tables
- Add derived labels and categories
- Compute aggregate features (trailing rates, velocity, windows)
- Apply ground-truth labeling from downstream outcomes

**Load**: Write processed data to target destinations:
- Warehouse tables (analytics and ML feature queries)
- ML training / modeling data stores
- Catalog datasets (for catalog-based consumption)
- Real-time feature-serving stores

## ETL Tools and Platforms

Common ETL/ELT platforms include SQL-based warehouse pipeline schedulers, distributed Spark processing engines, and managed ingestion services. In general:

- **SQL-based, warehouse-targeted schedulers** run cron-scheduled SQL transformations with dependency tracking and merge/insert load templates. Best for medium-scale data, daily/weekly batch, and standard analytics/feature tables.
- **Distributed Spark engines** handle large-scale (50TB+) processing, complex transformations requiring Python/Scala, and graph or network processing.

**When to use a distributed engine vs a SQL scheduler**:
- Very large datasets (50TB+) → distributed engine
- Complex transformations requiring Python/Scala → distributed engine
- Standard SQL on warehouse-scale data → SQL scheduler
- Standard analytics pipelines → SQL scheduler

### ELT vs ETL (Modern Pattern)

Modern data stacks increasingly use **ELT** (Extract, Load, Transform), which reverses the T and L steps: raw data is loaded directly into the target warehouse or lake first, then transformed in-place using the warehouse's own compute engine.

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform location** | External staging area or ETL server | Inside the target warehouse |
| **Raw data retention** | Often discarded after transform | Preserved in warehouse/lake |
| **Compute dependency** | Dedicated ETL infrastructure | Warehouse compute (elastic) |
| **Flexibility** | Must re-extract to change transforms | Re-run transforms on stored raw data |
| **Best fit** | On-premise, structured, compliance-heavy | Cloud-native, high-volume, iterative |

ELT became practical with cloud warehouses (Redshift, Snowflake, BigQuery) that decouple storage from compute. Key ELT tools include **dbt** (data build tool) for SQL-based transformations, and **Fivetran/Airbyte** for managed ingestion.

## ETL Job Lifecycle

```
1. Data arrives → Source systems (operational event, transaction, action)
         ↓
2. Ingestion → Streaming (real-time) or batch (daily)
         ↓
3. Raw storage → Object store / catalog / raw datasets
         ↓
4. Transform (SQL or Spark)
   - Clean nulls/duplicates
   - Join fact + dimension tables
   - Apply derived labels
   - Compute aggregate features
         ↓
5. Load → Data warehouse or catalog
         ↓
6. Feature computation → Real-time variables
         ↓
7. ML model training → Feature snapshots
         ↓
8. Analytics → Dashboards, model metrics
```

## ETL Best Practices

1. **Idempotency**: ETL jobs should be re-runnable without duplicating data (use Merge not Insert when possible)
2. **Partitioning**: Partition by date to enable efficient backfills and time-range queries
3. **Dependency management**: Use job dependencies to avoid stale data
4. **Backfill pipelines**: Maintain separate backfill pipelines for historical data corrections
5. **Data quality monitoring**: Track freshness, completeness, and schema drift to catch pipeline failures early

## Related Terms

### ETL Target and Source Systems
- **[Term: Redshift](term_redshift.md)** - Cloud data warehouse; common ETL/ELT target
- **[Term: Kinesis](term_kinesis.md)** - Real-time event streaming (upstream ETL source)
- **[Term: SQL](term_sql.md)** - Language used to write ETL transform logic

### ETL and Distributed Systems Concepts
- **[Message Queue](term_message_queue.md)**: Message queues decouple ETL pipeline stages, enabling asynchronous data flow between extract, transform, and load phases
- **[Pub/Sub](term_pub_sub.md)**: Pub/Sub enables fan-out from ETL outputs to multiple downstream consumers (dashboards, ML training, alerting)
- **[CAP Theorem](term_cap_theorem.md)**: Data pipeline consistency vs availability affects data freshness
- **[Consistency](term_consistency.md)**: ETL jobs must decide between consistent snapshots and available partial data
- **[Partition Tolerance](term_partition_tolerance.md)**: Data pipelines must handle transient network partitions

## References

### External Resources
- [Wikipedia: Extract, transform, load](https://en.wikipedia.org/wiki/Extract,_transform,_load)
- [dbt Documentation](https://docs.getdbt.com/)

## Summary

**ETL Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Extract, Transform, Load |
| **Modern Variant** | ELT (transform in-warehouse after load) |
| **Key Transform Logic** | Labeling, feature aggregation, ground-truth joining |
| **Key Output** | Warehouse analytics tables, ML training features, real-time variables |
| **Scheduling** | Cron-based (SQL schedulers), trigger-based (distributed engines) |
| **Data Volume** | SQL scheduler: warehouse-scale; distributed engine: 50TB+ |

**Key Insight**: ETL is not just data movement — it is where **raw events become analytics-ready and ML-ready intelligence**. Labeling and feature-aggregation ETL jobs join transactional, event, and outcome data to produce the labels and features that drive downstream ML models, review queues, and analytics dashboards. Without properly functioning ETL, model training labels degrade, queues go stale, and detection performance deteriorates.

---

**Last Updated**: March 2, 2026  
**Status**: Active - foundational data engineering pattern powering analytics and ML
