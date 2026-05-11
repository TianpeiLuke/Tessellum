---
tags:
  - resource
  - terminology
  - data_engineering
  - data_pipeline
  - buyer_abuse_prevention
keywords:
  - ETL
  - Extract Transform Load
  - Datanet
  - ETLM
  - data pipeline
  - Cradle
  - Redshift
  - data engineering
topics:
  - buyer abuse prevention
  - data engineering
  - data pipelines
  - analytics infrastructure
language: markdown
date of note: 2026-03-02
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/BDT/Products/Datanet/Overview
---

# Term: ETL - Extract, Transform, Load

## Definition

**ETL** (Extract, Transform, Load) is the data engineering pattern for moving data between systems: **extracting** raw data from source systems (Kinesis streams, EDX, Andes, external FCs), **transforming** it by cleaning, aggregating, joining, and enriching it according to business logic, and **loading** it into target warehouses (Redshift) or catalogs (Andes) for analytics and ML consumption. In Buyer Risk Prevention (BRP) and Buyer Abuse Prevention (BAP), ETL jobs are the **backbone of the abuse detection data stack** — converting raw events (order placements, concessions, return scans, investigator annotations) into structured, ML-ready features and ground-truth labels. Amazon's primary ETL tools are **Datanet** (also called ETLM — ETL Manager) for SQL-based Redshift pipelines and **Cradle** for large-scale Spark processing, both managed by BDT (Big Data Technologies).

## Core Concepts

### The ETL Process

```
Source Systems                  Transform                     Target
─────────────────────     ──────────────────────────     ──────────────
Kinesis (real-time)    →  Clean / deduplicate         →  Redshift (analytics)
EDX (batch events)     →  Join tables                 →  MDS (ML training)
Andes (catalog)        →  Aggregate / window          →  Andes (enriched)
FC systems (returns)   →  Apply business logic        →  OTF variables
Investigation data     →  Add ground truth labels     →  Feature store
```

**Extract**: Pull data from upstream sources at defined cadences (real-time via Kinesis, daily batch via Cradle/Datanet, on-demand via API)

**Transform**: Apply SQL/Spark logic to clean, enrich, and reshape data:
- Join order data with concession data
- Add abuse vector labels (DNR, MDR, FLR, PDA tags)
- Compute aggregate features (trailing concession rates, velocity)
- Apply ground truth labeling from investigator outcomes

**Load**: Write processed data to target destinations:
- Redshift tables (analytics and ML feature queries)
- MDS (Modeling Data Store, for ML training)
- Andes datasets (for catalog-based consumption)
- OTF (On-The-Fly) data streams (for real-time feature serving)

## ETL Tools in BRP/BAP

### 1. Datanet (ETLM - ETL Manager)

**Primary tool for SQL-based ETL pipelines targeting Redshift.**

| Attribute | Details |
|-----------|---------|
| **Full Name** | Datanet (formerly ETLM - ETL Manager) |
| **Type** | SQL-based, Redshift-targeted |
| **Scheduling** | Cron-based with dependency tracking |
| **Load Templates** | Merge (upsert/insert/update), Insert (table/partition) |
| **BAP Clusters** | trmsopsadhoc (dev), trmsopsetl1/2 (prod) |
| **Portal** | https://datacentral.a2z.com/dw-platform/servlet/dwp |
| **Owner** | BDT (Big Data Technologies) |

**Job Components**:
1. **Job Profile**: SQL query defining the transformation logic
2. **Scheduler**: Cron expression for execution frequency (daily, hourly)
3. **Dependencies**: Upstream job completion triggers
4. **Load Template**: How to write to target table (Merge vs Insert)

**When to use Datanet**:
- SQL-based transformations on Redshift
- Medium-scale data (fits within Redshift query limits)
- Daily/weekly batch processing
- Standard BAP analytics and feature tables

### 2. Cradle (Spark ETL)

**Used for large-scale distributed ETL processing on S3/Andes.**

| Attribute | Details |
|-----------|---------|
| **Full Name** | Cradle (formerly Dryad) |
| **Type** | Apache Spark, distributed |
| **Scale** | 50TB+, quadrillions of records |
| **Data Sources/Sinks** | S3, Andes, EDX, Redshift, Kinesis |
| **Cost** | ~$0.0004 per million records |
| **Profile Types** | SQL, Scala, Closure |
| **Owner** | BDT |

**When to use Cradle vs Datanet**:
- Very large datasets (50TB+) → Cradle
- Complex transformations requiring Python/Scala → Cradle
- Standard SQL on Redshift-scale data → Datanet
- Network detection or graph processing → Cradle
- Standard analytics pipelines → Datanet

### 3. ELT vs ETL (Modern Pattern)

Modern data stacks increasingly use **ELT** (Extract, Load, Transform), which reverses the T and L steps: raw data is loaded directly into the target warehouse or lake first, then transformed in-place using the warehouse's own compute engine.

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform location** | External staging area or ETL server | Inside the target warehouse |
| **Raw data retention** | Often discarded after transform | Preserved in warehouse/lake |
| **Compute dependency** | Dedicated ETL infrastructure | Warehouse compute (elastic) |
| **Flexibility** | Must re-extract to change transforms | Re-run transforms on stored raw data |
| **Best fit** | On-premise, structured, compliance-heavy | Cloud-native, high-volume, iterative |

ELT became practical with cloud warehouses (Redshift, Snowflake, BigQuery) that decouple storage from compute. Key ELT tools include **dbt** (data build tool) for SQL-based transformations, and **Fivetran/Airbyte** for managed ingestion. At Amazon, Cradle and Datanet both support ELT patterns — loading raw data to Andes/S3 first, then transforming in-place.

## Key BAP ETL Jobs

### Concession & Abuse Vector Tagging

| Job | Purpose | Output Table |
|-----|---------|-------------|
| **d_bap_concessions_vtag** | Master concession vector tagging (DNR/MDR/FLR/PDA/NSR) | buyer_abuse_prod.d_bap_concessions_vtag |
| **d_unified_concessions** | Unified concessions with financial metrics | BUYER_ABUSE_PROD.D_UNIFIED_CONCESSIONS |
| **d_unified_concessions_net** | Net concessions with recovery calculations | D_UNIFIED_CONCESSIONS_NET |

### Delivery & Shipment Data

| Job | Purpose | Source |
|-----|---------|--------|
| **d_pre_delivery_details** | Pre-delivery events for PDA detection | Perfect Mile OPLS events |
| **d_bad_returns** | FC grading for MDR/FLR/NSR labeling | BRW return inspection |
| **bap_mfn_concessions_vtag** | MFN-specific concession tagging | MFN seller grading (SGS) |

### ML Training Data

| Job | Purpose | Output |
|-----|---------|--------|
| **MDS pipeline** | Point-in-time ML feature snapshots | MDS (Modeling Data Store) |
| **GoldMiner pipeline** | Annotation extraction → reason codes/blurbs | buyer_abuse_prod/OTF |
| **OTF data streams** | Real-time feature computation | FORTRESS/URES |

## ETL Job Lifecycle in BAP

```
1. Data arrives → Source systems (FC scan, concession event, investigator action)
         ↓
2. Ingestion → Kinesis (real-time) or EDX batch (daily)
         ↓
3. Raw storage → S3 / Andes / EDX datasets
         ↓
4. Transform (Datanet SQL or Cradle Spark)
   - Clean nulls/duplicates
   - Join order + concession + shipment tables
   - Apply abuse vector labels (VTAG ETL)
   - Compute customer aggregate features
         ↓
5. Load → Redshift (buyer_abuse_prod schema) or Andes
         ↓
6. Feature computation → OTF real-time variables
         ↓
7. ML model training → MDS feature snapshots
         ↓
8. Analytics → WBR/QBR dashboards, model metrics
```

## BAP Data Schemas (Key Redshift Tables)

| Schema | Purpose |
|--------|---------|
| `buyer_abuse_prod.*` | Production BAP data (concessions, labels, models) |
| `buyer_abuse_dev.*` | Development/testing BAP data |
| `trmsdw.*` | TRMS data warehouse (enforcement history) |
| `booker.*` | Amazon retail order/return data |
| `brp_abuse.*` | Broader BRP abuse data |

**Key ETL-produced tables**:
- `BUYER_ABUSE_PROD.D_BAP_CONCESSIONS_VTAG` — abuse vector-tagged concessions
- `BUYER_ABUSE_PROD.D_FAP_GOLDMINER` — GoldMiner annotation extractions
- `BRP_ABUSE.BAP_ML_DSI_SECUREDDEL` — DSI measurement data
- `BRP_ABUSE.D_CAP_CDA_ASSESSMENT_FINAL` — CAP Decision Accuracy labels

## ETL Best Practices in BRP

1. **Idempotency**: ETL jobs should be re-runnable without duplicating data (use Merge not Insert when possible)
2. **Partitioning**: Partition by date to enable efficient backfills and time-range queries
3. **Dependency management**: Use Datanet job dependencies to avoid stale data
4. **TALFS compliance**: For fraud data requiring GDPR exemption, use `_TALFS` table variants
5. **DIG Score**: Monitor Redshift DIG score (target 90+) to ensure ETL efficiency
6. **Backfill pipelines**: Maintain separate backfill pipelines for historical data corrections

## Related Terms

### ETL Platforms
- **[Term: Datanet](term_datanet.md)** - Primary SQL-based ETL platform for Redshift (also called ETLM)
- **[Term: Cradle](term_cradle.md)** - Spark-based distributed ETL for large-scale S3/Andes processing
- **[Term: Kinesis](term_kinesis.md)** - Real-time event streaming (upstream ETL source)
- **[Term: EDX](term_edx.md)** - Legacy batch data exchange (ETL source, being deprecated)

### ETL Target Systems
- **[Term: Redshift](term_redshift.md)** - Primary data warehouse target for Datanet ETL jobs
- **[Term: Andes](term_andes.md)** - Amazon data catalog; source and target for Cradle ETL
- **[Term: MDS](term_mds.md)** - Modeling Data Store; receives ML training feature data from ETL

### ETL in BAP Context
- **[Term: SQL](term_sql.md)** - Language used to write Datanet ETL job transform logic
- **[Term: OTF](term_otf.md)** - On-The-Fly variable system; consumes ETL-produced data for real-time features

- **[Message Queue](term_message_queue.md)**: Message queues decouple ETL pipeline stages, enabling asynchronous data flow between extract, transform, and load phases
- **[Pub/Sub](term_pub_sub.md)**: Pub/Sub enables fan-out from ETL outputs to multiple downstream consumers (dashboards, ML training, alerting)
- **[CAP Theorem](term_cap_theorem.md)**: Data pipeline consistency vs availability affects data freshness
- **[Consistency](term_consistency.md)**: ETL jobs must decide between consistent snapshots and available partial data
- **[Partition Tolerance](term_partition_tolerance.md)**: Data pipelines must handle transient network partitions
## References

### Amazon Internal
- **Datanet Overview Wiki**: https://w.amazon.com/bin/view/BDT/Products/Datanet/Overview
- **Datanet Portal**: https://datacentral.a2z.com/dw-platform/servlet/dwp
- **BAP Datanet Report**: https://w.amazon.com/bin/view/BuyerAbuse/Engineering/BADE/DataEngineering/Datanet-Report/
- **Cradle Overview**: https://w.amazon.com/bin/view/BDT/Products/Cradle/Overview/
- **BDT Overview**: https://w.amazon.com/bin/view/BDT/

## Summary

**ETL Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Extract, Transform, Load |
| **Primary BAP Tool** | Datanet (SQL/Redshift) + Cradle (Spark/S3) |
| **Key Transform Logic** | Abuse vector labeling (VTAG), feature aggregation, ground truth joining |
| **Key Output** | Redshift analytics tables, MDS training features, OTF variables |
| **Core BAP ETL Jobs** | d_bap_concessions_vtag, d_bad_returns, d_pre_delivery_details, GoldMiner pipeline |
| **Scheduling** | Cron-based (Datanet), trigger-based (Cradle Step Functions) |
| **Data Volume** | Datanet: Redshift-scale; Cradle: 50TB+ distributed |

**Key Insight**: In BRP/BAP, ETL is not just data movement — it is where **raw events become abuse intelligence**. The concession vector tagging ETL job (`d_bap_concessions_vtag`) is perhaps the most critical pipeline: it joins order, shipment, return, and concession data to produce the `abuse_vector` labels that drive every downstream ML model, investigation queue, and analytics dashboard in the BAP ecosystem. Without properly functioning ETL, model training labels degrade, investigation queues go stale, and abuse detection performance deteriorates.

---

**Last Updated**: March 2, 2026  
**Status**: Active - foundational data engineering pattern powering BAP analytics, ML, and abuse detection