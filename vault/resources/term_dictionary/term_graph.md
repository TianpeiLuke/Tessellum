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
---

# Graph

## Definition

A **Graph** is a mathematical structure consisting of a set of **nodes** (also called vertices) and a set of **edges** (also called links or arcs) that connect pairs of nodes. Formally, a graph G is defined as G = (V, E), where V is the set of vertices and E ⊆ V × V is the set of edges. Graphs provide a natural way to represent relationships, interactions, and connections between entities.

In fraud and abuse prevention, graphs are a foundational data structure for modeling relationships between customers, orders, devices, payment methods, addresses, and other entities. Graph-based approaches enable the detection of abuse patterns that are invisible in tabular data — such as clusters of accounts sharing devices, coordinated abuse rings, and suspicious network structures.

## Context

Graphs are used extensively across fraud detection and knowledge-representation systems:

- **Entity relationship modeling**: Connecting customers, devices, addresses, and payment methods into an entity graph for account linking and multi-account abuse detection
- **Graph machine learning**: Graph Neural Network (GNN) variants (including temporal and heterogeneous models) score nodes and edges for fraud detection across concessions, returns, and account-abuse problems
- **Knowledge graphs**: Structured entity-relationship representations used for reasoning and retrieval-augmented generation

## Key Characteristics

- **Directed vs. Undirected**: Edges may have direction (directed graph/digraph) or not (undirected graph). Customer-order relationships are typically directed; device-sharing relationships are undirected.
- **Weighted vs. Unweighted**: Edges can carry weights representing strength, frequency, or confidence of a relationship.
- **Heterogeneous vs. Homogeneous**: Heterogeneous graphs have multiple node and edge types (e.g., customer nodes, device nodes, "uses" edges, "purchased" edges), which is the common case in abuse prevention.
- **Temporal**: Temporal graphs capture time-evolving relationships, critical for detecting abuse patterns that emerge over time.
- **Bipartite**: A graph where nodes split into two disjoint sets with edges only between sets (e.g., customers ↔ products).
- **DAG (Directed Acyclic Graph)**: A directed graph with no cycles, used in pipeline orchestration and dependency modeling.
- **Adjacency representation**: Graphs are stored as adjacency matrices, adjacency lists, or in graph databases depending on scale and query patterns.
- **Key operations**: Traversal (BFS, DFS), shortest path, connected components, community detection, label propagation, and message passing.

## Related Terms

- **[GNN - Graph Neural Networks](term_gnn.md)**: Neural network architectures that operate on graph-structured data for node classification and fraud detection
- **[TGN - Temporal Graph Networks](term_tgn.md)**: GNN variant that models time-evolving graphs for real-time abuse detection
- **[HGT - Heterogeneous Graph Transformer](term_hgt.md)**: Transformer-based GNN for heterogeneous graphs with multiple node/edge types
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured representation of entities and relationships as triples, used for reasoning and RAG
- **[Directed Acyclic Graph](term_directed_acyclic_graph.md)**: A directed graph with no cycles, used in pipeline and dependency modeling
- **[GraphRAG](term_graphrag.md)**: Graph-enhanced retrieval augmented generation combining knowledge graphs with LLMs

## References

- [Graph (discrete mathematics) — Wikipedia](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics))
- [Hamilton, W.L. (2020). *Graph Representation Learning*. Morgan & Claypool](https://www.cs.mcgill.ca/~wlh/grl_book/) — foundational text on graph machine learning
