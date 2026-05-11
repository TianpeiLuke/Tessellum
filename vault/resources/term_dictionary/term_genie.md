---
tags:
  - resource
  - terminology
  - graph
  - data_preparation
  - core_relations
  - infrastructure
keywords:
  - GENIE
  - Graph Preparation
  - CoRe
  - Graph Universe
  - Graphene
  - CREL
  - data pipeline
  - graph signals
topics:
  - graph preparation
  - data infrastructure
  - CoRe services
  - graph ML
language: markdown
date of note: 2026-02-06
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/
---

# Term: GENIE (Graph prEparatioN servIcE)

## Definition

**GENIE (Graph prEparatioN servIcE)** is CoRe's (Core Relations) singular graph preparation solution that filters and transforms data from authoritative sources into normalized graph data for consumption by graph computation components. GENIE is an essential step of all graph use-cases, preparing domain-specific **Graph Universes (GU)** usable by downstream systems like GraMS, ACIS, OACIS, and EV 2.0.

**Key Function**: Transform raw data events into graph-ready signals (entities, edges, properties) and provide self-service onboarding of new graph signals to CoRe's graph catalog.

**Scope**: Not just a replacement of legacy CoRe offerings (CREL, ORAS, Graphene) but their logical evolution to support next-generation graph preparation requirements including **synthetic signals** (derived/normalized signals beyond organic relationship data).

## Core Concepts

### Graph Preparation Mental Model

| Stage | Description | Example |
|-------|-------------|---------|
| **Graph Preparation** | Transform raw events → normalized graph data | GENIE |
| **Graph Computation** | Execute algorithms on prepared graph | GraMS, ACIS, OACIS, EV 2.0 |

### Terminology

| Term | Definition |
|------|------------|
| **Graph Signal** | Entity, edge, or property of the graph |
| **Raw Event** | Event received from authoritative data source (e.g., WalletService) |
| **Graph Event** | Collection of graph signals: entity + optional properties + timestamp |
| **Graph Universe (GU)** | Property-based graph representing state of the world for a problem space |
| **Organic Signals** | Naturally occurring graph signals (credit card, IP, device) |
| **Synthetic Signals** | Derived signals (fuzzy-matched, normalized, behavioral) |

### GENIE vs Legacy Systems

| Capability | Legacy (CREL/ORAS/Graphene) | GENIE |
|------------|---------------------------|-------|
| **Signal Onboarding** | Manual, labor-intensive | Self-service catalog |
| **Graph Universe** | Monolithic common graph | Multiple domain-specific GUs |
| **Data Storage** | EDX (Graphene) | Andes 3.0 datalake |
| **Synthetic Signals** | Limited/none | First-class support |
| **Infra Sharing** | Siloed per team | Shared SPS infrastructure |

## Architecture

### Overall Flow

```
Authoritative Data Sources
        ↓
    GENIE Pipeline
    ├── Signal Onboarding (self-service)
    ├── Transformation (raw event → graph event)
    ├── Normalization (optional: fuzzy match, noise clean)
    └── Storage (GENIE Datalake → Andes 3.0)
        ↓
    Graph Universe (GU)
    ├── Domain-specific graph per use case
    └── Neptune DB / Andes 3.0 backed
        ↓
    Graph Computation
    ├── GraMS (online GNN inference)
    ├── ACIS (real-time relationship insights)
    ├── OACIS (batch relationship computation)
    └── EV 2.0 (risk propagation)
```

### Key Components

| Component | Description |
|-----------|-------------|
| **Signal Catalog** | Repository of onboarded graph signals |
| **Transform Catalog** | Reusable transformation logic |
| **GENIE Datalake** | Centralized repository (Andes 3.0) for auditing, backfilling, experimentation |
| **Graph Universe Manager** | Self-service GU creation and provisioning |
| **Routing Layer** | Data routing to appropriate GU data stores |

### GENIE Datalake Design

| Feature | Description |
|---------|-------------|
| **Storage** | BDT's Andes 3.0 (cairns data-plane) |
| **Signal Types** | Edges, entity properties, edge properties |
| **Access Patterns** | Time-series access + compacted snapshots |
| **Compliance** | OD3 compliant (2 year deletion after OD3 request) |
| **Use Cases** | Auditing, backfilling, experimentation |

**Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Design/Datalake/

## Integration with GraMS

### GENIE → GraMS Flow

```
GENIE Signal Catalog
        ↓
Graph Universe Definition
        ↓
GENIE Datalake (Andes 3.0)
        ↓
GraMS Neptune DB
├── Streaming ingestion (CREL → Lambda)
└── Bulk load (backfill)
        ↓
SageMaker Model (TGN/GNN)
        ↓
OTF (score storage)
```

### COSA Integration

For COSA (Continuous One Step Ahead), GENIE provides the graph preparation layer:

| Component | Role |
|-----------|------|
| **CREL** | Event listener for customer lifecycle events (currently used, GENIE to replace) |
| **GENIE** | Future: singular graph preparation pipeline |
| **GraMS** | Neptune graph database + SageMaker model execution |

**Current State (COSA)**: Uses CREL (legacy) for event ingestion → Graphene → GraMS Neptune
**Future State**: GENIE → GENIE Datalake → GraMS Neptune

## Vision & Roadmap

### CoRe 3YAP Vision

| Capability | Description |
|------------|-------------|
| **Self-Service Signal Onboarding** | Clients onboard new signals to graph catalog |
| **Signal Sharing** | Share signals with other business teams |
| **Self-Service GU Creation** | Create graph universe from catalog signals |
| **Self-Service Provisioning** | Automatic GU data store provisioning and routing |
| **BYOD** | Bring Your Own Data - client-authored pipelines |

### Onboarding Efficiency

> "The time required to onboard new graph use-cases to CoRe will be inversely proportional to the size of the graph signal catalog in GENIE, as clients will leverage GENIE's self-service abilities to create their own custom graph universe."

### Evolution from Graphene

| Aspect | Graphene (Legacy) | GENIE Datalake |
|--------|-------------------|----------------|
| **Storage** | EDX | Andes 3.0 |
| **Model** | Monolithic common graph | Datalake + multiple GUs |
| **Signal Types** | Organic only | Organic + Synthetic |
| **Onboarding** | Manual | Self-service |
| **Status** | KTLO (migrate to GENIE) | Active development |

## Graph Signals

### Organic Signals (Naturally Occurring)

| Signal Type | Examples |
|-------------|----------|
| **Payment** | Credit card, bank account, payment token |
| **Identity** | Email, phone, device ID, UBID, FUBID |
| **Location** | Address, IP, residence ID |
| **Account** | Customer ID, account status |

### Synthetic Signals (Derived)

| Signal Type | Examples |
|-------------|----------|
| **Fuzzy-Matched** | Normalized addresses, standardized names |
| **Behavioral** | Session patterns, purchasing behavior |
| **Computed** | Risk scores, cluster assignments |

## Onboarding Process

### Two-Step Onboarding

1. **Graph Signal Onboarding**: Add new signals to GENIE catalog
   - Wiki: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/SignalOnboarding

2. **Graph Universe Onboarding**: Create GU from catalog signals
   - Wiki: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/GUOnboarding

### Onboarding Guide

**Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Onboarding/

## Dashboards & Monitoring

### GENIE Signals Dashboard

**Dashboard**: https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/Dashboards/ (GENIE Signals section)

### Metrics to Monitor

| Metric | Description |
|--------|-------------|
| **Signal Ingestion Rate** | Events processed per second |
| **Transformation Latency** | Time from raw event to graph event |
| **Datalake Write Rate** | Events written to Andes 3.0 |
| **GU Update Latency** | Time to propagate to graph universe |

## Data Privacy & Compliance

### OD3 Compliance

| Data Store | Retention Policy | OD3 Compliance |
|------------|-----------------|----------------|
| **GENIE Datalake** | 2 years | Deletes customer data 2 years after OD3 request |
| **Graphene Deltas** | 2 years | OD3 compliant |
| **Graphene Snapshots** | 3 months | Deletes + 2 year OD3 |
| **GraMS (Neptune)** | 6 months | TTL-based |

**Privacy Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/CoReDataPrivacyWiki/

## CoRe Services Ecosystem

### How GENIE Fits

| Service | Role | Relationship to GENIE |
|---------|------|----------------------|
| **GENIE** | Graph preparation | Source of truth for graph signals |
| **GraMS** | Online GNN inference | Consumes GENIE-prepared graphs |
| **ACIS** | Real-time relationship insights | Uses GENIE signals |
| **OACIS** | Batch relationship computation | Uses GENIE datalake |
| **EV 2.0** | Risk propagation | Uses GENIE graph structure |
| **ASEDO** | Scientific tooling SDK | Accesses GENIE data |
| **Graphene** | Legacy datalake | Being replaced by GENIE |
| **CREL** | Legacy event listener | Being replaced by GENIE |
| **ORAS** | Legacy offline access | Being replaced by GENIE |

### CoRe Trio (Concept → Experiment → Production)

```
ASEDO (Experimentation)
        ↓
OACIS (Offline Production)
        ↓
ACIS (Real-Time Production)
```

**GENIE provides the underlying graph preparation for all three.**

## Best Practices

### When to Use GENIE

| Use Case | Recommendation |
|----------|----------------|
| **New graph signal onboarding** | ✅ Use GENIE self-service |
| **Custom graph universe needed** | ✅ Use GENIE GU creation |
| **Existing Graphene consumer** | 📅 Migrate to GENIE datalake |
| **Ad-hoc graph exploration** | Consider ASEDO + GENIE |
| **Real-time relationship lookup** | ACIS (fed by GENIE) |
| **Batch relationship computation** | OACIS (fed by GENIE) |

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| **Bypassing GENIE for custom pipelines** | Use BYOD capabilities within GENIE |
| **Creating separate data silos** | Leverage shared signal catalog |
| **Ignoring synthetic signals** | Explore fuzzy-matching, behavioral signals |
| **Not using signal catalog** | Check existing signals before onboarding |

## Related Terms

### CoRe Services
- **[GraMS](term_grams.md)** - Graph Modeling System (consumes GENIE data)
- **[Neptune](term_neptune.md)** - Graph database (storage layer for GraMS)
- **[COSA](term_cosa.md)** - Continuous One Step Ahead (first GraMS MVP)
- **[ACIS](term_acis.md)** - Account Clustering Insight Service
- **[Graphene](term_graphene.md)** - Legacy relationship datalake (being replaced)

### Graph ML Platforms
- **[GraphStorm](term_graphstorm.md)** - AWS distributed GNN training framework (trains models deployed via GraMS)

### Data Infrastructure
- **[Andes](term_andes.md)** - Andes 3.0 (GENIE datalake storage)
- **[EDX](term_edx.md)** - Legacy data exchange (Graphene storage)
- **[OTF](term_otf.md)** - On The Fly variables (consumes graph insights)

### Graph Technologies
- **[Knowledge Graph](term_knowledge_graph.md)** - Graph representation of entities
- **[Ontology](term_ontology.md)** - Schema definition for graphs
- **[GNN](term_gnn.md)** - Graph Neural Networks (uses GENIE data)

## References

### Amazon Resources
- **GENIE Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/
- **HLD Design**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Design/HLD/
- **Datalake Design**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Design/Datalake/
- **Onboarding Guide**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Onboarding/
- **Signal Onboarding**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/SignalOnboarding
- **GU Onboarding**: https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/GUOnboarding
- **CoRe Main Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/
- **CoRe User Guide**: https://w.amazon.com/bin/view/Ohio/COreRElations/UserGuide/
- **5 Min Introduction**: https://broadcast.amazon.com/embed/1354726

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Graph prEparatioN servIcE |
| **Type** | Graph preparation pipeline |
| **Function** | Transform raw events → normalized graph data |
| **Owner Team** | CoRe (Core Relations) - ohio-engineering |
| **Replaces** | CREL, ORAS, Graphene |
| **Storage** | GENIE Datalake (Andes 3.0) |
| **Output** | Graph Universes (GU) for GraMS, ACIS, OACIS, EV 2.0 |
| **Key Innovation** | Self-service signal onboarding, synthetic signals support |
| **Status** | ✅ Active development - singular graph preparation solution |

**Key Insight**: GENIE is CoRe's strategic evolution from monolithic graph infrastructure to a self-service platform enabling any SPS team to onboard signals, create domain-specific graph universes, and leverage shared graph preparation infrastructure. The shift from "common graph" to "multiple graph universes" allows teams to tailor graphs to their specific fraud/abuse detection needs while sharing the underlying signal catalog and infrastructure. This dramatically reduces onboarding time - the larger the signal catalog grows, the faster new use cases can be deployed.

---

**Last Updated**: February 6, 2026  
**Status**: Active - singular graph preparation solution for CoRe  
**Team Owner**: CoRe (Core Relations) - ohio-engineering@
