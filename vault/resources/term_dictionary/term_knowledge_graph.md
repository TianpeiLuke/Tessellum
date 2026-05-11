---
tags:
  - resource
  - terminology
  - ml
  - ai
  - knowledge_management
  - data_structure
keywords:
  - Knowledge Graph
  - KG
  - entity
  - relationship
  - graph database
  - RAG
  - LLM
  - GraphRAG
topics:
  - machine learning
  - artificial intelligence
  - knowledge representation
  - data modeling
  - GenAI
language: markdown
date of note: 2026-02-06
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/KnowledgeCon/
---

# Term: Knowledge Graph

## Definition

A **Knowledge Graph (KG)** is a structured representation of real-world entities and the relationships between them, stored as a graph where **nodes represent entities** (people, places, concepts, events) and **edges represent relationships** between those entities. Knowledge graphs store facts in the form of triples: `(head entity, relation, tail entity)`.

**Key Function**: Provide structured, explicit, and queryable knowledge representation that captures semantic relationships, enabling reasoning, inference, and contextual understanding for both human users and AI systems.

## Core Concepts

### Graph Structure

| Component | Description | Example |
|-----------|-------------|---------|
| **Node (Entity)** | A real-world object, concept, or event | "Amazon", "Customer", "Order" |
| **Edge (Relationship)** | A connection between two entities | "purchased", "lives_in", "works_for" |
| **Triple** | The basic unit: (subject, predicate, object) | (Customer123, purchased, ProductXYZ) |
| **Property** | Attributes attached to nodes or edges | "name", "date", "amount" |
| **Label** | Category or type of a node | "Person", "Product", "Abuse_Pattern" |

### Triple Examples

```
(Buyer:123, placed_order, Order:456)
(Order:456, contains, Product:789)
(Buyer:123, has_address, Address:001)
(Buyer:123, linked_to, Account:987)
(Account:987, flagged_for, AbusePattern:DNR)
```

### Knowledge Graph vs Traditional Database

| Aspect | Knowledge Graph | Relational Database |
|--------|-----------------|---------------------|
| **Structure** | Flexible graph | Fixed schema/tables |
| **Relationships** | First-class citizens | Foreign keys |
| **Query Language** | SPARQL, Cypher, Gremlin | SQL |
| **Schema Evolution** | Easy to extend | Schema migration required |
| **Multi-hop Queries** | Native support | Complex JOINs |
| **Semantic Meaning** | Built-in ontologies | External documentation |
| **Best For** | Connected, heterogeneous data | Structured, tabular data |

## Applications in ML/AI

### Knowledge Graph Benefits for LLMs

| Benefit | Description |
|---------|-------------|
| **Reduced Hallucination** | Grounds LLM responses in factual, structured knowledge |
| **Better Context** | Provides relationships between concepts for comprehensive understanding |
| **Multi-hop Reasoning** | Enables following relationship paths to answer complex queries |
| **Explainability** | Traces knowledge provenance through connected facts |
| **Knowledge Organization** | Structures information naturally, easier to update and maintain |
| **Scalability** | Efficient retrieval through graph traversal |

### LLM Limitations KGs Address

| LLM Limitation | How KG Helps |
|----------------|--------------|
| **Knowledge Cutoff** | KGs can be continuously updated with new facts |
| **Hallucination** | Structured facts provide verification |
| **Lack of Interpretability** | Graph structure makes reasoning visible |
| **Domain Specificity** | KGs can encode specialized domain knowledge |
| **Implicit Knowledge** | KGs make relationships explicit and queryable |

## GraphRAG (Graph-based RAG)

### Definition

**GraphRAG** combines **Knowledge Graphs** with **Retrieval-Augmented Generation (RAG)** to enhance LLM outputs by leveraging graph structures for more accurate, contextual, and explainable information retrieval.

### GraphRAG vs Traditional RAG

| Aspect | Traditional RAG | GraphRAG |
|--------|----------------|----------|
| **Retrieval Method** | Vector similarity (embeddings) | Graph traversal + vector search |
| **Context Quality** | Chunk-based, may miss relationships | Relationship-aware, multi-hop |
| **Query Types** | Simple factual queries | Complex analytical queries |
| **Answer Accuracy** | ~50% (baseline) | ~80% (with graph structure) |
| **Explainability** | Limited source attribution | Full provenance through graph |
| **Knowledge Structure** | Flat document chunks | Connected entity relationships |

### When to Use GraphRAG

1. **Better Context Understanding** - Creates connections between related information
2. **More Accurate Retrieval** - Uses graph structures to find relevant information
3. **Complex Query Handling** - Answers multi-hop questions requiring multiple connections
4. **Knowledge Organization** - Structures information naturally
5. **Reduced Hallucination** - Provides structured context and verification
6. **Improved Reasoning** - Helps LLMs follow logical paths

### GraphRAG Architecture

```
User Query
    ↓
Query Understanding (LLM)
    ↓
├── Vector Search (embeddings)
│       ↓
│   Document Chunks
│
├── Graph Traversal (KG)
│       ↓
│   Related Entities & Relationships
│
└── Hybrid Retrieval
        ↓
    Combined Context
        ↓
    LLM Generation with Graph Context
        ↓
    Response with Provenance
```

## Amazon Context

### Knowledge Graph Technologies at Amazon

| Technology | Description | Use Case |
|------------|-------------|----------|
| **Amazon Neptune** | Managed graph database service | Enterprise KG storage |
| **Neptune Analytics** | Graph analytics with vector search | GraphRAG applications |
| **Alexa Knowledge Graph** | Consumer product KG | Voice assistant reasoning |
| **AWS Knowledge Mesh** | Enterprise knowledge integration | Cross-service knowledge sharing |
| **Amazon Kendra** | Enterprise search with ML | RAG retrieval |

### Graph Query Languages

| Language | Description | Amazon Service |
|----------|-------------|----------------|
| **SPARQL** | W3C standard for RDF graphs | Neptune (RDF mode) |
| **Gremlin** | Apache TinkerPop graph traversal | Neptune (Property Graph) |
| **OpenCypher** | Graph query language (Neo4j origin) | Neptune (Property Graph) |

### Internal Amazon KG Applications

- **Product Catalog Graph** - Product relationships, attributes, categories
- **Alexa Knowledge Graph** - Entities, facts, relationships for voice Q&A
- **Fraud/Abuse Detection Graphs** - Account relationships, transaction patterns
- **Search Knowledge Graph** - Query understanding, entity linking
- **AWS Service Graph** - Service dependencies, relationships

## BAP Context

### Knowledge Graphs in Abuse Prevention

| Application | Description |
|-------------|-------------|
| **Account Link Analysis** | Graph of customer accounts, shared attributes, behavioral patterns |
| **Transaction Networks** | Relationships between orders, payments, addresses, devices |
| **Abuse Pattern Detection** | Graph-based clustering to identify coordinated abuse rings |
| **Multi-Account Abuse** | MALTA/PACMAN use graph relationships for account clustering |
| **Investigation Support** | Graph visualization for investigators to explore connections |

### BAP Graph-Based Systems

| System | Graph Use |
|--------|-----------|
| **MALTA** | Account-level clustering using relationship graphs |
| **PACMAN/LANTERN** | Multi-account abuse detection via link analysis |
| **COSA (Continuous One Step Ahead)** | Real-time graph for proactive detection |
| **Investigation Tools** | Graph visualization for abuse ring exploration |

### Example BAP Knowledge Graph Structure

```
Account:A123
├── [owns_device] → Device:D001
│                      └── [also_used_by] → Account:B456
├── [has_address] → Address:ADDR001
│                      └── [shared_by] → Account:B456
├── [placed_order] → Order:ORD001
│                      └── [contains] → Product:P001
│                      └── [claimed] → DNR_Claim:C001
└── [linked_to] → Payment:PAY001
                      └── [also_used_by] → Account:C789
```

### Graph ML in Fraud/Abuse Detection

| Technique | Application |
|-----------|-------------|
| **Graph Convolutional Networks (GCN)** | Learning node embeddings for abuse classification |
| **Graph-based Clustering** | Identifying abuse rings and coordinated attacks |
| **Link Prediction** | Predicting hidden relationships between accounts |
| **Community Detection** | Finding groups of related fraudulent accounts |
| **Graph Anomaly Detection** | Identifying unusual patterns in transaction graphs |

## Knowledge Graph Construction

### Construction Methods

| Method | Description | Effort |
|--------|-------------|--------|
| **Manual Curation** | Domain experts define entities and relationships | High quality, high effort |
| **Schema-based Extraction** | Extract from structured data sources | Medium quality, medium effort |
| **LLM-based Extraction** | Use LLMs to extract entities and relationships from text | Scalable, requires validation |
| **Hybrid** | Combine automated extraction with expert validation | Balanced approach |

### LLM-based KG Construction

1. **Entity Extraction** - LLM identifies entities from unstructured text
2. **Relationship Extraction** - LLM identifies relationships between entities
3. **Entity Resolution** - Match extracted entities to existing KG entities
4. **Validation** - Human/automated verification of extracted facts
5. **Integration** - Add validated facts to knowledge graph

## Best Practices

### Building Knowledge Graphs

| Practice | Description |
|----------|-------------|
| **Start with Use Case** | Define what questions the KG needs to answer |
| **Define Ontology** | Create clear schema for entity types and relationships |
| **Ensure Data Quality** | Validate facts before adding to graph |
| **Maintain Provenance** | Track source of each fact for traceability |
| **Plan for Evolution** | Design schema to accommodate future extensions |
| **Index Appropriately** | Create indexes for common query patterns |

### GraphRAG Implementation

| Practice | Description |
|----------|-------------|
| **Hybrid Retrieval** | Combine vector search with graph traversal |
| **Context Selection** | Choose relevant subgraphs for LLM context |
| **Prompt Engineering** | Structure prompts to leverage graph context |
| **Validation Layer** | Verify LLM outputs against graph facts |
| **Feedback Loop** | Use LLM interactions to improve graph quality |

## Related Terms

### AI/ML
- **[RAG](term_rag.md)** - Retrieval-Augmented Generation
- **[LLM](term_llm.md)** - Large Language Model
- **[Embedding](term_embedding.md)** - Vector representation
- **[GenAI](term_genai.md)** - Generative AI

### Data Systems
- **[Neptune](term_neptune.md)** - Amazon graph database
- **[Graph Database](term_graph_database.md)** - Database for graph data
- **[Ontology](term_ontology.md)** - Formal knowledge representation

### Knowledge Management
- **[Zettelkasten](term_zettelkasten.md)** - Note-taking method using atomic, interconnected notes (German: "slip box") - conceptually similar to KG with notes as nodes and links as edges
- **[Slipbox](term_slipbox.md)** - Implementation of Zettelkasten principles for domain knowledge organization - combines KG structure with curated human expertise

### BAP Systems
- **[MALTA](term_malta.md)** - Multi-Account and Large Transaction Abuse Prevention team - owns graph-based MAA detection (PACMAN, LANTERN, COSA)
- **[PACMAN](term_pacman.md)** - Proactive Multi-Account Abuse Prevention using graph relationships
- **[LANTERN](term_lantern.md)** - Real-time order-level MAA detection via identity graphs
- **[Nexus](term_nexus.md)** - Graph-based risk scoring system and AskNexus (GraphRAG for abuse Q&A)
- **[URES](term_ures.md)** - Universal Risk Evaluation Service

- **[CAP Theorem](term_cap_theorem.md)**: Distributed graph queries face CAP trade-offs
- **[GraphQL](term_graphql.md)**: GraphQL's graph-shaped query language is a natural fit for knowledge graph APIs, enabling clients to traverse entity relationships with flexible nested queries
- **[MongoDB](term_mongodb.md)**: Can store graph-like data but lacks native traversal — Neptune is better suited
## References

### Amazon Resources
- **KnowledgeCon**: https://w.amazon.com/bin/view/KnowledgeCon/KnowledgeCon2024/
- **GraphRAG Wiki**: https://w.amazon.com/bin/view/AWS/Teams/Proserve/GenAIID/GenAIIC/InnovativePrograms/PublicSector/ReusableAssets/GraphRAG/
- **ML on Graphs Workshop (AMLC)**: https://w.amazon.com/bin/view/AMLC2020_Workshop_Machine_Learning_on_Graphs/
- **Knowledge Graph Powered LLM**: https://w.amazon.com/bin/view/D2AS/Pegasus/KnowledgeGraph/Design/KnowledgeGraphPoweredLLMApplications/

### AMLC Workshops (ML for Fraud/Abuse)
- **4th Workshop ML Fraud/Abuse/Security (2023)**: https://w.amazon.com/bin/view/Amazon-Science/events/AMLC/2023/Workshops/4th_Workshop_on_Machine_Learning_in_Fraud_Abuse_Security_and_Defect/
- **5th Workshop ML Fraud/Abuse/Security (2024)**: https://w.amazon.com/bin/view/Amazon-Science/events/AMLC/2024/Workshops/ML_in_Fraud_Abuse_and_Security/
- **Graph ML Workshop (2022)**: https://w.amazon.com/bin/view/AMLC2022_2nd_Workshop_on_Graph_Machine_learning/

### External Resources
- **Neo4j**: Industry-leading graph database platform
- **Apache TinkerPop**: Graph computing framework
- **W3C RDF/SPARQL**: Semantic web standards

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Knowledge Graph |
| **Abbreviation** | KG |
| **Type** | Data structure for representing entities and relationships |
| **Structure** | Graph: Nodes (entities) + Edges (relationships) |
| **Basic Unit** | Triple: (subject, predicate, object) |
| **Query Languages** | SPARQL, Gremlin, Cypher |
| **Amazon Service** | Amazon Neptune |
| **ML Integration** | GraphRAG (KG + RAG for LLMs) |
| **BAP Applications** | Account link analysis, abuse ring detection, MALTA/PACMAN |
| **Key Benefit** | Explicit relationships enable multi-hop reasoning, reduces hallucination |
| **vs RAG** | GraphRAG achieves ~80% accuracy vs ~50% baseline RAG |

**Key Insight**: Knowledge Graphs complement LLMs by providing structured, explicit, and verifiable knowledge that LLMs lack. While LLMs represent knowledge implicitly in parameters (hard to interpret/validate), KGs store knowledge as explicit triples with clear provenance. GraphRAG combines both: using KGs to ground LLM responses in factual relationships, enabling multi-hop reasoning, and providing explainable answers with traceable sources. In abuse prevention, graph-based approaches like MALTA and PACMAN leverage relationship structures to detect coordinated abuse that single-order models miss.

---

**Last Updated**: February 6, 2026  
**Status**: Active - foundational concept in AI/ML and abuse prevention  
**Related Concepts**: RAG, LLM, Graph Database, Entity-Relationship
