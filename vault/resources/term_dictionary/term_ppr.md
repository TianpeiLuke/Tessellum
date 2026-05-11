---
tags:
  - resource
  - terminology
  - machine_learning
  - graph_algorithms
  - information_retrieval
keywords:
  - PPR
  - Personalized PageRank
  - PageRank
  - graph ranking
  - knowledge graph
  - GraphRAG
  - random walk with restart
  - Pixie
  - recommendation systems
  - seed node
topics:
  - graph algorithms
  - information retrieval
  - knowledge graphs
  - RAG systems
language: markdown
date of note: 2026-03-03
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/ABSearch/KB/SemanticSearchKG_Guide/
---

# PPR - Personalized PageRank

## Definition
Personalized PageRank (PPR) is a graph ranking algorithm that ranks all nodes in a knowledge graph by their relevance to a set of seed entities. It extends the classic PageRank algorithm by introducing a personalization vector that biases the random walk to restart at specific seed nodes rather than uniformly across all nodes. In the context of GraphRAG and LLM-powered knowledge systems, PPR is used to retrieve relevant entities and relationships from knowledge graphs by computing relevance scores based on graph structure and connectivity.

## Context
PPR is primarily used in GraphRAG (Graph-based Retrieval Augmented Generation) systems at Amazon, particularly in the AB Search and Checkout teams' knowledge base implementations. It serves as a deterministic, mathematical approach to graph traversal that complements semantic search in hybrid retrieval systems. The algorithm is implemented using NetworkX in Python and runs within AWS Lambda functions to provide fast, consistent entity ranking for LLM query systems. PPR is used alongside Bedrock Knowledge Bases to merge vector search results with graph-based retrieval.

## Key Characteristics
- **Random Walk with Restart**: Simulates a random walker that follows edges with 85% probability (damping factor α=0.85) and teleports back to seed entities with 15% probability
- **Personalization Vector**: Biases the walk to restart at query-extracted seed entities rather than uniformly across all nodes
- **Iterative Convergence**: Typically converges in 20-30 iterations using the power iteration method
- **Score Distribution**: Top 400 nodes capture 95% of total relevance, with scores decaying exponentially with graph distance from seeds
- **Deterministic Output**: Same query and seed entities always produce identical rankings, unlike LLM-guided approaches
- **Sparse Matrix Operations**: Optimized using scipy sparse matrices for graphs with 15K-50K nodes, achieving 150ms warm latency
- **Multi-Seed Support**: Handles multiple seed entities with uniform distribution (1/|S| for each seed)
- **Fuzzy Entity Matching**: Uses Levenshtein distance (threshold=0.6) to match LLM-extracted entities to graph node names

## Performance / Metrics
- **Latency**: 150ms warm (cached graph), 800ms cold (includes graph loading from S3)
- **Scalability**: Handles graphs up to 50K nodes efficiently; 2-3s for larger graphs
- **Memory**: ~16MB for 15K nodes + 27K edges graph in Lambda
- **Convergence**: 20-30 iterations typical with tolerance 1e-6
- **Coverage**: Top 400 results capture 95% of relevance score distribution
- **Precision**: 88% top-5 precision, 82% top-10 precision in production testing
- **Recall**: 95% recall compared to exhaustive graph search

## Related Terms
- **[PageRank](term_pagerank.md)**: Parent algorithm — PPR is the personalized variant with seed-concentrated teleportation
- **[Random Walk](term_random_walk.md)**: Underlying stochastic process whose stationary distribution PPR computes
- **[Dense Retrieval](term_dense_retrieval.md)**: Content-based ranking complementary to PPR; PPR's `--seed-strategy dense` chains the two
- **[Cosine Similarity](term_cosine_similarity.md)**: Scoring function used by the dense seed-selection upstream of PPR
- **[ANN Search](term_ann_search.md)**: PPR is a graph-based relevance scoring method; complementary to embedding-based ANN for hybrid retrieval
- **[LSH](term_lsh.md)**: Hash-based ANN in embedding space; PPR provides graph-based relevance — different similarity paradigms
- **[Johnson-Lindenstrauss Lemma](term_johnson_lindenstrauss_lemma.md)**: JL provides distance-preserving embeddings; PPR provides graph-proximity scoring — both are dimensionality-aware
- **[RAG](term_rag.md)**: Retrieval Augmented Generation — PPR enhances RAG via graph-based ranking alongside vector search
- **[LLM](term_llm.md)**: Large Language Models used for entity extraction and query synthesis in GraphRAG systems
- **[Embedding](term_embedding.md)**: Vector representations used for semantic similarity alongside PPR
- **[BERT](term_bert.md)**: Transformer model architecture used in embedding models for semantic search components
- **[Pixie Random Walk](term_pixie_random_walk.md)**: Pinterest's Monte Carlo approximation of PPR — trades matrix exactness for trivial parallelism. FZ 5e2b1a empirically showed random-seeded Pixie underperforms dense-seeded PPR by ~30 pp Hit@5; the signal lives in the seeds, not in the walk.

## References
- [Semantic Search + Knowledge Graph: Technical Playbook](https://w.amazon.com/bin/view/ABSearch/KB/SemanticSearchKG_Guide/)
- [GraphRAG Overview](https://w.amazon.com/bin/view/Users/rawlsimo/graphrag/)
- [TFL GraphRAG Project](https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/TFL-GraphRAG/)
