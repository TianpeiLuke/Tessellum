---
tags:
  - resource
  - terminology
  - ml
  - ai
  - knowledge_management
  - data_modeling
keywords:
  - Ontology
  - taxonomy
  - knowledge representation
  - semantic web
  - OWL
  - RDF
  - schema
  - knowledge graph
topics:
  - machine learning
  - artificial intelligence
  - knowledge representation
  - data modeling
  - semantic web
language: markdown
date of note: 2026-02-06
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/KnowledgeCon/KnowledgeCon2025/
---

# Term: Ontology

## Definition

An **Ontology** is a formal, explicit specification of a shared conceptualization within a domain, defining the types of entities (classes), their properties (attributes), and the relationships between them. Unlike simple taxonomies (hierarchical classifications), ontologies capture rich semantic relationships that enable machine reasoning, inference, and validation.

**Key Function**: Provide a structured schema that defines what entities exist in a domain, how they relate to each other, and what rules govern their interactions - enabling both humans and machines to share and reason about knowledge consistently.

## Core Concepts

### Ontology Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Class** | A category or type of entity | "Customer", "Order", "AbusePattern" |
| **Property** | Attributes of classes or relationships between classes | "has_name", "depends_on", "triggered_by" |
| **Instance** | A specific individual belonging to a class | "Customer123", "Order456" |
| **Relationship** | Defined connection between entities | "placed_order", "linked_to_account" |
| **Axiom** | Logical rules constraining the ontology | "Every Order must have exactly one Customer" |
| **Hierarchy** | Class inheritance structure | "DNRAbuse is-a ConcessionAbuse is-a AbuseType" |

### Ontology vs Taxonomy vs Schema

| Aspect | Taxonomy | Schema | Ontology |
|--------|----------|--------|----------|
| **Structure** | Hierarchical (tree) | Relational (tables) | Graph-based (flexible) |
| **Relationships** | Parent-child only | Foreign keys | Rich typed relationships |
| **Semantics** | Limited to hierarchy | Limited to constraints | Full semantic meaning |
| **Reasoning** | No inference | No inference | Automated inference |
| **Validation** | Manual | Constraint-based | Logic-based reasoning |
| **Evolution** | Rigid structure | Schema migration | Flexible extension |
| **Use Case** | Classification | Data storage | Knowledge representation |

### Formal vs Informal Ontology

| Aspect | Formal Ontology | Informal Ontology |
|--------|-----------------|-------------------|
| **Foundation** | Mathematical logic (OWL, RDF) | Human-readable descriptions |
| **Processing** | Machine-processable | Human interpretation only |
| **Validation** | Automatic via reasoners | Manual review |
| **Inference** | New facts derived automatically | No inference |
| **Standards** | W3C specifications | Custom formats |
| **Tools** | Protégé, reasoners (HermiT, Pellet) | Documents, wikis |

## Semantic Web Technology Stack

### Standard Technologies

| Technology | Purpose | Description |
|------------|---------|-------------|
| **RDF** | Data Model | Resource Description Framework - represents facts as triples |
| **RDFS** | Basic Schema | RDF Schema - defines classes, properties, hierarchies |
| **OWL** | Rich Ontology | Web Ontology Language - complex constraints, reasoning |
| **SPARQL** | Query Language | Query RDF graphs with pattern matching |
| **Reasoners** | Inference Engine | Apply logical rules, validate consistency |

### RDF Triple Structure

```
(Subject, Predicate, Object)

Examples:
(Customer:123, placed_order, Order:456)
(Order:456, has_amount, 150.00)
(Customer:123, rdf:type, HighRiskCustomer)
(Customer:123, linked_to, Customer:789)
```

### OWL Features

| Feature | Description | Example |
|---------|-------------|---------|
| **Subclass** | Inheritance relationship | `DNRAbuse ⊆ ConcessionAbuse` |
| **Transitive Property** | Relationship propagates | If A depends-on B, B depends-on C → A depends-on C |
| **Disjoint Classes** | Mutual exclusion | LegitimateCustomer ⊥ Abuser (cannot be both) |
| **Cardinality** | Quantity constraints | Order has exactly one CustomerId |
| **Domain/Range** | Property constraints | "placed_order" domain: Customer, range: Order |

## Knowledge Formula

```
Ontology (Schema) + Data (Instances) = Knowledge Graph
```

- **Ontology**: The conceptual model/schema defining what can exist
- **Data**: Actual instances and facts
- **Knowledge Graph**: Complete representation with explicit facts + inferred knowledge

## Amazon Context

### Amazon Ontology Teams and Systems

| Team/System | Focus Area | Wiki |
|-------------|------------|------|
| **Product Knowledge (PK)** | Product catalog ontology | https://w.amazon.com/bin/view/ProductKnowledge/ |
| **KnowledgeCon** | Annual ontology/KM conference | https://w.amazon.com/bin/view/KnowledgeCon/ |
| **UMP** | Universal Metadata Platform ontology | https://w.amazon.com/bin/view/Atambe/UMP_Ontology_Data_Model/ |
| **D2AS Pegasus** | Device support knowledge graph | https://w.amazon.com/bin/view/D2AS/Pegasus/KnowledgeGraph/ |
| **AWS IT Security** | Security issue ontology framework | https://w.amazon.com/bin/view/AWS_IT_Security/Products/Transduction/Ontology/ |

### Product Knowledge Ontology Tenets

From PK Knowledge Store Ontology Design Principles:

| Principle | Description |
|-----------|-------------|
| **Consistent Design Patterns** | Reuse patterns instead of creating new ones |
| **Decidability First** | OWL 2 DL compliant, expressiveness only when needed |
| **Losslessness** | Preserve all information in migrations |
| **Data-Tested Models** | Every model tested with real data |
| **Self-Documenting** | Store design decisions in rdfs:comment and rdfs:seeAlso |

### KnowledgeCon 2025 Sessions

| Session | Presenter | Topic |
|---------|-----------|-------|
| **From Taxonomy to Ontology** | Heather Hedden | Comparisons and how to extend taxonomy to ontology |
| **Knowledge at Scale** | Rayssa Küllian (BAP) | Building Nexus KG with billions of elements |
| **Evolving PK Data Model** | Heather Moore, Ben Middleton | Ontology primitives and agentic support |

## BAP Context

### Ontology in Abuse Prevention

| Application | Description |
|-------------|-------------|
| **Abuse Type Hierarchy** | Classification of abuse patterns (DNR, FLR, FRA, etc.) |
| **Entity Relationships** | Customer → Account → Order → Concession chains |
| **Risk Signal Schema** | OTF variables, model scores, behavioral signals |
| **Investigation Workflow** | Actions, outcomes, enforcement states |
| **Modus Operandi (MO)** | Abuse pattern definitions and relationships |

### BAP Domain Ontology Concepts

```
AbuseType
├── ConcessionAbuse
│   ├── DNR (Delivered Not Received)
│   ├── FLR (Failed Return)
│   └── FRA (Fraudulent Return)
├── AccountAbuse
│   ├── MAA (Multi-Account Abuse)
│   ├── ATO (Account Takeover)
│   └── NewAccountAbuse
├── TransactionAbuse
│   ├── QLA (Quantity Limits Abuse)
│   └── ResellerAbuse
└── FulfillmentAbuse
    ├── AFN (Amazon Fulfillment Network)
    └── MFN (Merchant Fulfillment Network)
```

### Nexus Knowledge Graph (BAP)

From KnowledgeCon 2025 - Rayssa Küllian (Principal Scientist, Buyer Abuse Fixed):

> "Nexus is a massive knowledge graph developed by Buyer Abuse Prevention to detect and prevent policy abuse on Amazon's marketplace. Our graph currently contains over **5.3 billion nodes** and **9.6 billion edges** spanning **21 entity types** and **23 relationship types** to form a complex network representing things like customers, orders, shipments, and financial instruments with over **19.8 billion property values**."

| Nexus Ontology Aspect | Details |
|----------------------|---------|
| **Nodes** | 5.3+ billion entities |
| **Edges** | 9.6+ billion relationships |
| **Entity Types** | 21 types (customers, orders, shipments, payments, etc.) |
| **Relationship Types** | 23 types (owns, placed, linked_to, etc.) |
| **Properties** | 19.8+ billion property values |
| **Write Throughput** | Up to 100K records/second |
| **Storage** | AWS Neptune |

### BAP Ontology Use Cases

| Use Case | Ontology Application |
|----------|---------------------|
| **Risk Signal Standardization** | OTF variable naming conventions and relationships |
| **Model Feature Organization** | Hierarchical feature groups with semantic meaning |
| **Investigation Workflow** | State machines and outcome taxonomies |
| **Abuse Pattern Classification** | MO hierarchy and detection rules |
| **Cross-Team Communication** | Shared vocabulary and entity definitions |

## Best Practices

### Ontology Design Principles

| Practice | Description |
|----------|-------------|
| **Start with Use Case** | Define what questions the ontology needs to answer |
| **Reuse Patterns** | Leverage existing design patterns before creating new ones |
| **Document Decisions** | Store rationale in ontology comments (rdfs:comment) |
| **Test with Real Data** | Validate with actual domain data before deployment |
| **Plan for Evolution** | Design schema to accommodate future extensions |
| **Maintain Consistency** | Use consistent naming conventions and structures |

### Ontology Development Workflow

1. **Domain Analysis** - Identify entities, relationships, constraints
2. **Conceptual Design** - Create class hierarchy and properties
3. **Formalization** - Express in OWL/RDF or equivalent
4. **Validation** - Test with reasoners and sample data
5. **Integration** - Connect to knowledge graph and applications
6. **Maintenance** - Evolve based on new requirements

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| **Over-engineering** | Start simple, add complexity as needed |
| **Ambiguous naming** | Use clear, domain-specific terminology |
| **Missing relationships** | Ensure all important connections are modeled |
| **Inconsistent hierarchy** | Apply single inheritance where possible |
| **Ignoring scalability** | Design for graph growth and query performance |

## Related Terms

### Knowledge Management
- **[Knowledge Graph](term_knowledge_graph.md)** - Data structure built on ontology schema
- **[Taxonomy](term_taxonomy.md)** - Hierarchical classification (simpler than ontology)
- **[Schema](term_schema.md)** - Data structure definition
- **[Zettelkasten](term_zettelkasten.md)** - Note-taking method with linked concepts

### Technologies
- **[RDF](term_rdf.md)** - Resource Description Framework
- **[OWL](term_owl.md)** - Web Ontology Language
- **[Neptune](term_neptune.md)** - Amazon graph database
- **[SPARQL](term_sparql.md)** - Graph query language

### BAP Systems
- **[Nexus](term_nexus.md)** - BAP knowledge graph using ontology for abuse detection
- **[OTF](term_otf.md)** - On-the-Fly features using structured variable schema
- **[MO](term_mo.md)** - Modus Operandi - abuse pattern taxonomy

## References

### Amazon Resources
- **KnowledgeCon 2025**: https://w.amazon.com/bin/view/KnowledgeCon/KnowledgeCon2025/
- **KnowledgeCon 2024**: https://w.amazon.com/bin/view/KnowledgeCon/KnowledgeCon2024/
- **PK Ontology Tenets**: https://w.amazon.com/bin/view/ProductKnowledge/PKKnowledgeStore/Ontology/KnowledgePlatformOntologyTenets/
- **UMP Ontology Data Model**: https://w.amazon.com/bin/view/Atambe/UMP_Ontology_Data_Model/
- **D2AS Knowledge Management**: https://w.amazon.com/bin/view/D2AS/Pegasus/KnowledgeGraph/Ontology/Design/KnowledgeManagement/
- **Ontologies and KG Technical Guide**: https://w.amazon.com/bin/view/Users/cslhui/Ontology/
- **AWS Security Ontology**: https://w.amazon.com/bin/view/AWS_IT_Security/Products/Transduction/Ontology/

### External Resources
- **W3C OWL**: https://www.w3.org/TR/owl2-overview/
- **Protégé**: https://protege.stanford.edu/ (Ontology editor)
- **RDF Primer**: https://www.w3.org/TR/rdf-primer/

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Ontology |
| **Type** | Formal knowledge representation framework |
| **Purpose** | Define entities, properties, relationships, and rules for a domain |
| **vs Taxonomy** | Richer relationships, reasoning, inference (not just hierarchy) |
| **vs Schema** | Semantic meaning, flexible evolution, logic-based validation |
| **Technologies** | RDF, RDFS, OWL, SPARQL |
| **Amazon Tools** | Protégé, Neptune, KnowledgeCon community |
| **BAP Application** | Nexus KG ontology, abuse type hierarchy, OTF variable schema |
| **Key Benefit** | Machine reasoning + shared understanding across teams |

**Key Insight**: An ontology is the conceptual backbone of a knowledge graph - it defines "what can exist" while the knowledge graph contains "what actually exists." In BAP, ontology thinking helps standardize abuse type definitions, risk signal naming, and entity relationships. The Nexus knowledge graph uses an ontology with 21 entity types and 23 relationship types to represent the complex web of customers, orders, payments, and abuse patterns. Good ontology design enables both machine reasoning (automated inference) and human understanding (shared vocabulary), making it essential for cross-team collaboration and scalable abuse detection systems.

---

**Last Updated**: February 6, 2026  
**Status**: Active - foundational concept in knowledge management and AI  
**Related Concepts**: Knowledge Graph, Taxonomy, Schema, RDF, OWL
