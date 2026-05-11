---
tags:
  - resource
  - terminology
  - machine_learning
  - llm
  - context_engineering
  - retrieval
  - genai
keywords:
  - RAG
  - retrieval augmented generation
  - retrieval-augmented generation
  - context retrieval
  - knowledge base
  - vector database
  - embeddings
  - LLM augmentation
  - grounding
topics:
  - machine learning
  - large language models
  - context engineering
  - information retrieval
  - generative AI
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/Agents/RAG/
related_wiki_2: https://docs.hub.amazon.dev/docs/golden-path/llm-integrated-applications/recommendation/design/5-retrieval-augmented-generation-rag/
related_wiki_3: https://w.amazon.com/bin/view/TC_Forge/Builder_Resources/rag_introduction/
---

# RAG - Retrieval Augmented Generation

## Definition

**Retrieval Augmented Generation (RAG)** is an optimization technique that enhances Large Language Models (LLMs) by connecting them to external, authoritative knowledge sources. Instead of relying solely on pre-trained knowledge (which has training cutoff dates and lacks domain-specific information), RAG systems dynamically retrieve relevant information from external databases, documents, or APIs and incorporate this context into the response generation process.

RAG addresses three critical LLM limitations:
1. **Knowledge Cutoff**: LLMs are trained on static datasets with temporal boundaries
2. **Domain Gap**: LLMs lack organization-specific knowledge and proprietary data
3. **Hallucination**: Without grounding, LLMs may generate plausible but incorrect information

> **Simple Definition**: RAG allows AI models to "look up" current, accurate information from your organization's knowledge base before generating responses, combining the language capabilities of LLMs with the accuracy and currency of real-time data.

## Key Highlights

**Architecture and Pipeline**: RAG follows a four-stage pipeline -- data preparation (vectorization), retrieval (similarity search), augmentation (context injection), and generation (LLM response). The architecture relies on vector databases (OpenSearch, Pinecone, Redis), embedding models (Titan, Cohere, E5), and chunking strategies (fixed-size, semantic, hierarchical) to convert documents into searchable representations. For full architecture details, component specifications, Amazon implementation profiles (Bedrock, Amazon Q, Nexus, GreenTEA, Abuse Slipbox), and comparison with Zettelkasten-enhanced RAG, see [RAG Architecture, Evaluation, and Comparisons](../analysis_thoughts/thought_rag_architecture_and_evaluation.md).

**Advantages over Alternatives**: RAG is more cost-effective than fine-tuning because knowledge base updates do not require model retraining, it preserves the model's general capabilities, and it enables source attribution and explainability. Compared to prompt engineering alone, RAG adds dynamic external knowledge; compared to pre-training, it avoids the cost of building foundation models from scratch. RAG is best suited for dynamic knowledge, frequent updates, and domain-specific data requirements.

**Implementation and Operations**: Successful RAG deployments require quality data preparation, optimal chunking with overlap, hybrid search (semantic + BM25), re-ranking, and structured prompt engineering with fallback behavior. Key operational challenges include "lost in the middle" (mitigated by zig-zag ordering), hallucination despite grounding (mitigated by firm system prompts and citation requirements), and stale knowledge (mitigated by automated refresh pipelines). For detailed best practices, performance optimization, and troubleshooting guidance, see [RAG Implementation Best Practices](../policy_sops/sop_rag_implementation_best_practices.md).

## Amazon RAG Resources

### Documentation

- **Bedrock User Guide**: [RAG with Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- **BuilderHub**: [LLM RAG Recommendations](https://docs.hub.amazon.dev/docs/golden-path/llm-integrated-applications/recommendation/design/5-retrieval-augmented-generation-rag/)
- **Agentic AI Portal**: [RAG Comprehensive Guide](https://w.amazon.com/bin/view/Agents/RAG/)
- **Forge Workbench**: [RAG in Forge](https://w.amazon.com/bin/view/TC_Forge/Builder_Resources/rag_introduction/)

### Training

- **MLU**: [Building Applications with LangChain](https://mlu.corp.amazon.com/courses/wksp-building-applications-langchain/)
- **GenAI 101**: [MLU GenAI Introduction](https://mlu.corp.amazon.com/courses/ml4l-genai/)
- **Bedrock Workshop**: [Amazon Bedrock Workshop](https://github.com/aws-samples/amazon-bedrock-workshop/)

### Tools

- **Amazon Bedrock**: Managed RAG via Knowledge Bases
- **Amazon Q**: Enterprise Q&A with RAG
- **Amazon Kendra**: Enterprise search
- **LangChain**: RAG pipeline framework
- **Builder MCP**: Amazon internal context retrieval

## Related Concepts

### Related Terms

- **[Term: LLM](term_llm.md)** - Large Language Models that RAG enhances
- **[Term: Zettelkasten](term_zettelkasten.md)** - Knowledge management methodology informing Slipbox RAG
- **[Term: Knowledge Graph](term_knowledge_graph.md)** - Graph structures for context organization
- **[Term: Vector Database](term_vector_database.md)** - Specialized storage and search for high-dimensional vectors
- **[Term: Embedding](term_embedding.md)** - Dense vector representations for similarity search
- **[Term: DeepCARE](term_deepcare.md)** - k-NN similarity search for investigations
- **[Term: GreenTEA](term_greentea.md)** - SOP-driven RAG for abuse investigations
- **[Term: Nexus](term_nexus.md)** - Graph-RAG for buyer abuse prevention
- **[Term: Bedrock](term_bedrock.md)** - Amazon Bedrock managed RAG infrastructure
- **[Term: MCP](term_mcp.md)** - Model Context Protocol for LLM tool integration
- **[Term: DPR](term_dpr.md)** - Dense Passage Retrieval — the neural retriever backbone used in the original RAG architecture
- **[Term: Dense Retrieval](term_dense_retrieval.md)** - The IR family that ranks documents by embedding similarity; the canonical retriever inside RAG pipelines
- **[Term: Cosine Similarity](term_cosine_similarity.md)** - The scoring function the dense retriever uses to compare query and passage embeddings
- **[Term: PageRank](term_pagerank.md)** - Graph-based importance algorithm; PageRank-family methods power graph-augmented RAG (HippoRAG, GraphRAG)
- **[Term: PPR](term_ppr.md)** - Personalized PageRank (GraphRAG context); the seed-relative variant used inside graph-augmented RAG retrievers at Amazon
- **[Term: Personalized PageRank](term_ppr.md)** - The foundational PPR algorithm; random walks with restart that underpin GraphRAG entity retrieval and Pinterest-scale recommendation
- **[Term: Hallucination](term_hallucination.md)** - LLM failure mode that RAG mitigates through factual grounding in retrieved documents
- **[Term: FAISS](term_faiss.md)** - Facebook AI Similarity Search — approximate nearest neighbor index used in RAG's retriever
- **[Term: GraphRAG](term_graphrag.md)** - Graph-based RAG using community detection + hierarchical summarization for global sensemaking queries (Edge et al., 2024)
- **[Term: HippoRAG](term_hipporag.md)** - Graph-augmented RAG using PPR over open KG for multi-hop factual retrieval (Gutierrez et al., 2025)

### Related Areas

- **[Area: DeepCARE](../../areas/area_deepcare.md)** - Investigation automation using similarity retrieval
- **[Area: MALTA](../../areas/area_malta.md)** - ML-powered investigation with context retrieval

### Related Glossaries

- **[ML Glossary](../../0_entry_points/acronym_glossary_ml.md)** - Machine learning terms including LLM, embeddings
- **[Tools Glossary](../../0_entry_points/acronym_glossary_tools.md)** - Bedrock, LangChain, vector databases

## Summary

**Retrieval Augmented Generation (RAG)** is a foundational technique for building effective LLM applications:

**Key Characteristics**:
- **Combines LLM + External Knowledge**: Language capabilities + factual grounding
- **Dynamic Context**: Retrieves relevant information at query time
- **Cost-Effective**: No model retraining when knowledge changes
- **Explainable**: Can cite sources for generated content

**Core Components**:
1. **Knowledge Base**: Documents converted to vector embeddings
2. **Retrieval**: Similarity search finds relevant context
3. **Augmentation**: Context added to LLM prompt
4. **Generation**: LLM produces grounded response

**Amazon Applications**:
- **Amazon Bedrock Knowledge Bases**: Managed RAG service
- **Amazon Q**: Enterprise Q&A with RAG
- **Nexus AskNexus**: Graph-RAG for abuse detection
- **GreenTEA**: SOP-driven investigation automation
- **Abuse Slipbox**: Zettelkasten-enhanced knowledge retrieval

**When to Use RAG**:
- Domain-specific knowledge required
- Frequently changing information
- Source attribution needed
- Organization-specific data
- Hallucination mitigation critical

RAG represents a fundamental shift from static, pre-trained knowledge to dynamic, context-aware AI applications—essential for enterprise deployments where accuracy, currency, and explainability matter.

## See Also

- [RAG Architecture, Evaluation, and Comparisons](../analysis_thoughts/thought_rag_architecture_and_evaluation.md) — Architecture details, pipeline walkthrough, Amazon implementations (Bedrock, Q, Nexus, GreenTEA, Slipbox), component specifications (vector DBs, embeddings, chunking), and comparative analysis (RAG vs fine-tuning, RAG vs Zettelkasten)
- [RAG Implementation Best Practices](../policy_sops/sop_rag_implementation_best_practices.md) — Data preparation, chunking optimization, retrieval tuning, prompt engineering for RAG, performance/scalability guidance, and common challenge solutions (lost-in-the-middle, hallucination, stale knowledge)

---

- **[Vector Space Model](term_vector_space_model.md)**: RAG retrieval uses VSM (sparse) or dense embeddings

## References

### Primary Source
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../papers/lit_lewis2020retrieval.md) — Lewis et al. (2020), NeurIPS 2020. arXiv:2005.11401. *Foundational paper: DPR retriever + BART generator, two formulations (RAG-Sequence, RAG-Token), SOTA on 3 QA benchmarks, index hot-swapping, 11,802 citations.*

### Extensions
- [From RAG to Memory (Gutierrez et al., 2025)](../papers/lit_gutierrez2025rag.md) — Survey tracing RAG's evolution from this foundational paper through advanced RAG, modular RAG, and memory-augmented architectures.
- [GraphRAG (Edge et al., 2024)](../papers/lit_edge2024local.md) — Graph-based RAG using community detection + hierarchical summarization for global sensemaking. 72-83% comprehensiveness win rate over vector RAG.

### Internal Documentation
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) — Managed RAG service implementing the RAG architecture pattern
- [Agentic AI Portal — RAG Guide](https://w.amazon.com/bin/view/Agents/RAG/) — Comprehensive internal RAG implementation guide
- [BuilderHub RAG Recommendations](https://docs.hub.amazon.dev/docs/golden-path/llm-integrated-applications/recommendation/design/5-retrieval-augmented-generation-rag/) — Golden path recommendations for RAG applications

### Related Code Repos
- [SlipBot](../../areas/code_repos/repo_slipbot.md) — RAG-style chatbot using SQL search + note retrieval over the abuse slipbox

---

**Document Version**: 1.3
**Last Updated**: March 15, 2026
**Primary References**: Lewis et al. (2020), Amazon Agentic AI Portal, BuilderHub GenAI Recommendations, Amazon Bedrock Documentation
