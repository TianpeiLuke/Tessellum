---
tags:
  - resource
  - terminology
  - ai_engineering
  - llm
  - context_engineering
  - prompt_engineering
  - retrieval
  - genai
  - agentic_ai
keywords:
  - context engineering
  - context window management
  - context assembly
  - context curation
  - prompt engineering evolution
  - dynamic context
  - token optimization
  - RAG
  - retrieval augmented generation
  - context distraction
  - context compression
  - agentic context
topics:
  - AI Engineering
  - Large Language Models
  - Information Retrieval
  - Context Window Management
language: markdown
date of note: 2026-03-17
status: active
building_block: concept
---

# Context Engineering

## Definition

**Context engineering** is the discipline of designing and building dynamic systems that provide the right information and tools, in the right format, at the right time, to give a Large Language Model (LLM) everything it needs to accomplish a task. Coined by Andrej Karpathy in June 2025, the term reframes the practitioner's role from crafting clever prompt text to engineering the entire information environment that reaches the model's context window.

While [prompt engineering](term_prompt_engineering.md) focuses on *how you phrase instructions* (the wording, structure, and reasoning scaffolds of the prompt itself), context engineering focuses on *what information the model sees* — selecting, filtering, compressing, and ordering the retrieved documents, tool outputs, conversation history, memory, and structured data that populate the context window. In Karpathy's formulation: "Context engineering is the delicate art and science of filling the context window with just the right information for the next step."

Context engineering treats the context window as a finite, precious resource — an "attention budget" with diminishing marginal returns. Every token occupying the window either helps or hinders the model's ability to attend to what matters. The discipline thus requires systems thinking: building pipelines that dynamically assemble context from multiple sources (developers, users, prior interactions, tool outputs, external databases) rather than relying on static prompt templates.

> **Simple distinction**: If prompt engineering is writing a good exam question, context engineering is curating the entire open-book reference packet the student gets to use during the exam.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| **2020** | Lewis et al. | **RAG** paper introduced dynamic retrieval into LLM generation — the first systematic approach to context augmentation beyond the prompt |
| **2022** | Wei et al., Yao et al. | **CoT** and **ReAct** expanded what goes into the context window (reasoning traces, tool observations) beyond simple instructions |
| **2023** | Khattab et al. | **DSPy** introduced programmatic prompt compilation — treating prompt + context assembly as a software engineering problem |
| **2024** | Anthropic, Google | System prompt best practices formalized; tool-use protocols (function calling, MCP) standardized how tools inject information into context |
| **June 2025** | Andrej Karpathy | Coined/popularized **"context engineering"** in an X post: "+1 for 'context engineering' over 'prompt engineering'... in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information" |
| **June 2025** | Tobi Lutke (Shopify CEO) | Amplified the term, describing context engineering as the "full screenplay" for AI vs. prompt engineering's "magical sentence" |
| **June 2025** | Harrison Chase (LangChain) | Formalized definition: "building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task" |
| **July 2025** | Gartner | Explicitly stated: "Context engineering is in, and prompt engineering is out. AI leaders must prioritize context over prompts." |
| **Oct 2025** | Wang et al. | Published **ACE (Agentic Context Engineering)** — first academic paper treating context as evolving playbooks for self-improving agents (arXiv:2510.04618) |
| **Nov 2025** | Spotify Engineering | Published detailed case study on context engineering for background coding agents ("Honk, Part 2") |
| **2025-2026** | Industry-wide | Context engineering adopted as standard terminology across Google ADK, LangChain, Anthropic, and enterprise AI platforms |

## Taxonomy

### By Strategy (Four Pillars)

| Strategy | Description | Techniques | Example |
|----------|-------------|-----------|---------|
| **Write** | Creating or persisting information outside the context window for later retrieval | Scratchpads, structured note-taking, agentic memory, persistent state files | Claude Code writing to CLAUDE.md; agents maintaining task progress notes |
| **Select** | Pulling relevant information into the context from external sources | [RAG](term_rag.md), tool invocation, database queries, API calls, file retrieval | Retrieving relevant code files via grep before answering a coding question |
| **Compress** | Retaining only the tokens required to perform a task | Summarization, conversation compaction, context pruning, clearing tool results | Summarizing a 50-turn conversation into key decisions and open issues |
| **Isolate** | Separating different types of context to prevent interference | Sub-agent architectures, multi-agent delegation, sandboxed context windows | Spawning a research sub-agent with a clean context, returning a 1-2K token summary |

### By Context Component

| Component | Source | Purpose | Example |
|-----------|--------|---------|---------|
| **System Instructions** | Developer | Define model behavior, role, constraints | "You are a fraud analyst. Cite evidence for every claim." |
| **User Prompt** | User | Per-request input with task description | "Classify this return request as legitimate or suspicious." |
| **Retrieved Knowledge** | [RAG](term_rag.md) pipeline | Ground responses in factual, current data | Passages from internal documentation retrieved via vector search |
| **Tool Definitions** | Developer | Specify available tools and their schemas | JSON Schema definitions of APIs the model can call |
| **Tool Outputs** | Runtime | Results from tool invocations | Database query results, API responses, file contents |
| **Conversation History** | Runtime | Prior turns in the interaction | Previous messages, summarized or full |
| **Long-Term Memory** | Persistent store | User preferences, past interactions, learned facts | User's timezone, past investigation patterns, organizational context |
| **Task Metadata** | Environment | Temporal, environmental, and organizational signals | Current date, user role, active project, deadline constraints |

### By Retrieval Strategy

| Strategy | Description | Trade-offs |
|----------|-------------|-----------|
| **Pre-computed (eager)** | Index and retrieve ahead of time via embeddings/RAG | Fast at runtime; may include stale or irrelevant results |
| **Just-in-time (lazy)** | Retrieve dynamically via tool calls during inference | Always current; slower, costs more LLM reasoning tokens |
| **Hybrid** | Pre-computed retrieval + autonomous exploration at agent discretion | Balances speed and coverage; more complex to implement |
| **Progressive disclosure** | Incrementally discover context layer by layer | Avoids overwhelming the model; may miss globally relevant info |

## Key Properties

- **Finite attention budget**: The context window is a fixed-size resource where every token either helps or hinders; models exhibit diminishing returns and degraded recall as context length increases, even with million-token windows
- **Dynamic assembly**: Context is constructed at runtime from multiple sources, not statically authored — requiring pipeline engineering, not just text editing
- **Superset of prompt engineering**: Prompt engineering (instruction wording) is one component; context engineering additionally manages retrieval, tool output, memory, history, and metadata
- **Model-agnostic discipline**: The principles (select, compress, isolate, write) apply across all LLM providers and architectures, though implementation details vary
- **Systems design skill**: Requires software engineering and information architecture thinking, not just natural language craft — designing retrieval pipelines, memory systems, and multi-agent coordination
- **Quality over quantity**: Research shows model performance drops around 32K tokens due to context distraction, even in models with 128K+ windows — careful curation outperforms naive context stuffing
- **Context failure modes**: Three distinct failure patterns — context poisoning (hallucinations entering context), context distraction (irrelevant information overwhelming signal), and context confusion (conflicting information causing errors)
- **Measurable optimization target**: Context quality can be evaluated via task success rate, retrieval precision/recall, token efficiency (useful tokens / total tokens), and latency
- **Quadratic cost scaling**: Transformer attention scales O(n^2) with context length, making unnecessary tokens expensive in both compute and latency
- **Compaction trade-off**: Overly aggressive compression risks losing subtle but critical context whose importance only becomes apparent later in the task

## Notable Systems / Implementations

| System | Mechanism | Application |
|--------|-----------|-------------|
| **Claude Code** | Hybrid context: CLAUDE.md pre-loaded + glob/grep for just-in-time file retrieval; structured note-taking for persistent memory | Coding assistant with codebase-scale context |
| **Cursor** | Full codebase indexing with dependency mapping; context-aware code completion assembling relevant files | AI-powered IDE with project-wide context |
| **GitHub Copilot** | Repository-level context selection; cross-file reference resolution | Code completion with multi-file awareness |
| **Google ADK** | Agent Development Kit with native context stack supporting all four pillars (write/select/compress/isolate) | Multi-agent framework for enterprise applications |
| **LangGraph** | Stateful agent orchestration with shared memory, context handoff between specialized sub-agents | Complex multi-agent workflows |
| **Anthropic MCP** | [Model Context Protocol](term_mcp.md) standardizing how tools and data sources inject context into LLM conversations | Universal tool integration protocol |
| **ACE (Wang et al.)** | Agentic Context Engineering treating contexts as evolving playbooks with generation, reflection, and curation phases | Self-improving language model agents |
| **Spotify Honk** | Background coding agent with systematic context engineering for autonomous code changes | Production coding automation |
| **Dex Horthy's 12-Factor Agent** | Engineering principles (stateless design, modularity, structured tool outputs) adapted from cloud-native development to LLM systems | Agent architecture framework |

## Applications

| Domain | Context Engineering Application | Key Technique |
|--------|-------------------------------|---------------|
| **Coding assistants** | Assembling relevant source files, dependencies, test results, and documentation for code generation | Hybrid retrieval (index + just-in-time search) |
| **Enterprise Q&A** | [RAG](term_rag.md) pipelines retrieving organizational knowledge to ground LLM responses | Select (retrieval) + Compress (re-ranking) |
| **Agentic workflows** | Multi-step agents maintaining working memory across tool calls and sub-task delegation | Write (memory) + Isolate (sub-agents) |
| **Customer support** | Loading customer history, product catalog, and policy documents into context for accurate responses | Select (multi-source retrieval) |
| **Investigation automation** | Assembling case evidence, SOP requirements, and historical decisions for fraud analysis | All four pillars |
| **Research synthesis** | Progressive retrieval and summarization of academic literature for comprehensive analysis | Select + Compress |
| **Conversational AI** | Managing multi-turn dialogue with compaction, memory retrieval, and persona consistency | Write + Compress |

## Challenges and Limitations

### Context Window Constraints
1. **Lost in the middle**: LLMs exhibit U-shaped attention — information at the beginning and end of context is recalled better than information in the middle, requiring strategic ordering
2. **Context distraction**: Irrelevant information in the context actively degrades performance, even when the relevant information is also present
3. **Quadratic cost**: Transformer attention scales O(n^2), making each additional token increasingly expensive in compute and latency
4. **Diminishing returns**: Research shows effective performance drops around 32K tokens regardless of nominal window size

### Retrieval and Selection
5. **Relevance-completeness trade-off**: Aggressive filtering may discard subtly relevant information; permissive inclusion wastes attention budget
6. **Stale context**: Pre-computed indexes and cached context can become outdated, requiring refresh mechanisms
7. **Context poisoning**: If hallucinated or incorrect information enters the context (e.g., from a previous model turn), it can propagate through subsequent reasoning

### System Design
8. **Compaction information loss**: Summarization inherently discards details — and the importance of those details may only become apparent later
9. **Tool result bloat**: Poorly designed tools return excessive output, consuming context budget with low-value tokens
10. **Multi-agent coordination**: Isolating context into sub-agents requires careful design of what information flows between agents and what stays scoped
11. **Evaluation difficulty**: Measuring context quality requires end-to-end task evaluation, not just retrieval metrics — context that scores well on retrieval precision may still cause task failures

### Emerging Concerns
12. **Context clash**: Gathered information and tools may directly conflict with other information already in context, requiring conflict resolution strategies
13. **Memory selection bias**: Automated memory retrieval can inject unexpected or privacy-sensitive information (e.g., location data surfaced without user intent)
14. **No formal guarantees**: Like prompt engineering, context engineering lacks formal semantics — there is no guarantee of how any context arrangement will be interpreted

## Related Terms

- **[Prompt Engineering](term_prompt_engineering.md)**: The predecessor discipline focusing on instruction wording; context engineering is its systems-level evolution
- **[RAG](term_rag.md)**: Retrieval Augmented Generation — the most established context engineering technique, implementing the "select" pillar
- **[LLM](term_llm.md)**: Large Language Models — the systems whose context windows context engineering optimizes
- **[Embedding](term_embedding.md)**: Dense vector representations enabling similarity-based context retrieval in RAG pipelines
- **[Vector Database](term_vector_database.md)**: Specialized storage for embeddings enabling fast similarity search for context selection
- **[MCP](term_mcp.md)**: Model Context Protocol — standardized protocol for injecting tool outputs and external data into LLM context
- **[AgentZ](term_agentz.md)**: Amazon's agent platform whose DAPE engine performs context assembly for each task step
- **[Chain of Thought](term_chain_of_thought.md)**: Reasoning technique that consumes context tokens for intermediate steps — a key context budget trade-off
- **[Transformer](term_transformer.md)**: The architecture whose attention mechanism creates the quadratic cost that motivates context engineering
- **[Hallucination](term_hallucination.md)**: LLM failure mode that context engineering mitigates through factual grounding, but that context poisoning can amplify
- **[Prompt Optimization](term_prompt_optimization.md)**: Automated optimization of prompt text — a component within the broader context engineering discipline
- **[Fine-Tuning](term_fine_tuning.md)**: Alternative to context engineering that bakes knowledge into model weights rather than providing it at inference time
- **[Knowledge Graph](term_knowledge_graph.md)**: Structured knowledge representation enabling graph-based context retrieval strategies
- **[Gist Token](term_gist_token.md)**: Gist tokens implement the "compress" pillar of context engineering by distilling long context into fewer virtual tokens
- **[Block Masking](term_block_masking.md)**: Block masking enables self-managed context compression by dynamically evicting irrelevant context blocks at the KV cache level

## References

### Vault Sources

### External Sources
- [Anthropic (2025). "Effective context engineering for AI agents."](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — comprehensive guide covering compaction, sub-agents, and progressive disclosure strategies
- [Schmid, P. (2025). "The New Skill in AI is Not Prompting, It's Context Engineering."](https://www.philschmid.de/context-engineering) — seven context components framework (instructions, user prompt, state, memory, RAG, tools, output)
- [Chase, H. / LangChain (2025). "The Rise of Context Engineering."](https://blog.langchain.com/the-rise-of-context-engineering/) — definition and relationship to prompt engineering as a subset
- [Karpathy, A. (2025). X post on context engineering.](https://x.com/karpathy/status/1937902205765607626) — original coinage: "the delicate art and science of filling the context window with just the right information"
- [Wang et al. (2025). "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models." arXiv:2510.04618](https://arxiv.org/abs/2510.04618) — first academic paper on agentic context engineering (ACE)
- [Spotify Engineering (2025). "Background Coding Agents: Context Engineering (Honk, Part 2)."](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2) — production case study
- [Elastic (2025). "What is context engineering? Components, techniques, and best practices."](https://www.elastic.co/search-labs/blog/context-engineering-overview) — component taxonomy and implementation guide
- [FlowHunt (2025). "Context Engineering: The Definitive 2025 Guide."](https://www.flowhunt.io/blog/context-engineering/) — comprehensive overview with Gartner's endorsement
- [DataCamp (2025). "Context Engineering: A Guide With Examples."](https://www.datacamp.com/blog/context-engineering) — context failure modes (poisoning, distraction, confusion)

---

**Document Version**: 1.0
**Last Updated**: March 17, 2026
**Primary References**: Karpathy (2025), Anthropic (2025), LangChain (2025), Wang et al. (2025)
