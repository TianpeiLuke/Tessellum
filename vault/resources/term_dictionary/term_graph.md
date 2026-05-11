---
tags:
  - resource
  - terminology
  - mathematics
  - data_structure
  - machine_learning
  - graph
keywords:
  - Graph
  - graph theory
  - nodes
  - edges
  - vertices
  - adjacency
  - network
  - graph structure
topics:
  - mathematics
  - data structures
  - machine learning
  - fraud detection
  - abuse prevention
language: markdown
date of note: 2026-03-11
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/BuyerRiskPreventionML/GNN/
---

# Graph

## Definition

A **Graph** is a mathematical structure consisting of a set of **nodes** (also called vertices) and a set of **edges** (also called links or arcs) that connect pairs of nodes. Formally, a graph G is defined as G = (V, E), where V is the set of vertices and E ⊆ V × V is the set of edges. Graphs provide a natural way to represent relationships, interactions, and connections between entities.

In the context of Amazon Buyer Abuse Prevention (BAP), graphs are the foundational data structure for modeling relationships between customers, orders, devices, payment methods, addresses, and other entities. Graph-based approaches enable the detection of abuse patterns that are invisible in tabular data — such as clusters of accounts sharing devices, coordinated abuse rings, and suspicious network structures.

## Context

Graphs are used extensively across BAP and the broader Amazon fraud prevention ecosystem:

- **Buyer Abuse ML Team**: Uses graph-based models (GNN, TGN, HGT) for fraud detection and abuse scoring across concessions, returns, and multi-account abuse programs
- **Core Relations (CoRe)**: Maintains the entity graph infrastructure connecting customers, devices, addresses, and payment methods via Neptune graph databases
- **GraMS (Graph Modeling System)**: CoRe's platform for deploying online graph models, connecting SageMaker models to Neptune graphs
- **CCS/IDA**: Customer Clustering Service and Identity Disambiguation use graph-based account linking to detect multi-account abuse
- **Research projects**: Spiderweb, LaPulse, DomSpot, and Project Nexus all leverage graph structures for abuse detection

## Key Characteristics

- **Directed vs. Undirected**: Edges may have direction (directed graph/digraph) or not (undirected graph). Customer-order relationships are typically directed; device-sharing relationships are undirected.
- **Weighted vs. Unweighted**: Edges can carry weights representing strength, frequency, or confidence of a relationship.
- **Heterogeneous vs. Homogeneous**: Heterogeneous graphs have multiple node and edge types (e.g., customer nodes, device nodes, "uses" edges, "purchased" edges), which is the common case in abuse prevention.
- **Temporal**: Temporal graphs capture time-evolving relationships, critical for detecting abuse patterns that emerge over time (modeled by TGN).
- **Bipartite**: A graph where nodes split into two disjoint sets with edges only between sets (e.g., customers ↔ products).
- **DAG (Directed Acyclic Graph)**: A directed graph with no cycles, used in pipeline orchestration and dependency modeling.
- **Adjacency representation**: Graphs are stored as adjacency matrices, adjacency lists, or in graph databases (Neptune, NebulaGraph) depending on scale and query patterns.
- **Key operations**: Traversal (BFS, DFS), shortest path, connected components, community detection, label propagation, and message passing.

## Related Terms

- **[GNN - Graph Neural Networks](term_gnn.md)**: Neural network architectures that operate on graph-structured data for node classification and fraud detection
- **[TGN - Temporal Graph Networks](term_tgn.md)**: GNN variant that models time-evolving graphs, deployed via COSA for real-time abuse detection
- **[HGT - Heterogeneous Graph Transformer](term_hgt.md)**: Transformer-based GNN for heterogeneous graphs with multiple node/edge types
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured representation of entities and relationships as triples, used for reasoning and RAG
- **[GraMS - Graph Modeling System](term_grams.md)**: CoRe's platform for deploying online graph models on Neptune
- **[COSA](term_cosa.md)**: Continuous One Step Ahead — real-time graph inference system
- **[Neptune](term_neptune.md)**: Amazon's managed graph database service used for storing entity relationship graphs
- **[GraphStorm](term_graphstorm.md)**: AWS framework for graph machine learning at scale
- **[Directed Acyclic Graph](term_directed_acyclic_graph.md)**: A directed graph with no cycles, used in pipeline and dependency modeling
- **[Graphene](term_graphene.md)**: Graph-based entity resolution system
- **[NebulaGraph](term_nebulagraph.md)**: Distributed graph database used in abuse prevention infrastructure
- **[GraphRAG](term_graphrag.md)**: Graph-enhanced retrieval augmented generation combining knowledge graphs with LLMs
- **[Abuse Polygraph](term_abuse_polygraph.md)**: Graph-based abuse detection system

## References

- [BRP ML GNN Wiki](https://w.amazon.com/bin/view/BuyerRiskPreventionML/GNN/)
- [Buyer Abuse ML Team Wiki](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/)
- [CoRe GraMS Wiki](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/)
