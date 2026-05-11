---
tags:
  - resource
  - terminology
  - agentic_ai
  - tool_use
  - self_supervised_learning
  - function_calling
  - llm_research
keywords:
  - Toolformer
  - self-supervised tool use
  - API calling
  - tool-augmented language models
  - GPT-J
  - Meta AI
  - loss filtering
  - tool learning
  - API annotation
  - Schick et al.
topics:
  - LLM tool use
  - self-supervised learning
  - agentic AI
  - tool-augmented generation
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Toolformer

## Definition

**Toolformer** is a language model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction -- all in a **self-supervised** manner. Introduced by Schick et al. (2023) at Meta AI, Toolformer demonstrated that LLMs can **teach themselves** to use external tools without requiring large-scale human annotations of tool-use behavior.

The core insight is that a language model can annotate its own training data with potential API calls, execute those calls, and then filter them based on whether they actually reduce the model's perplexity on subsequent tokens. The model is then fine-tuned on this self-curated, tool-augmented dataset.

Toolformer represents a foundational step in the evolution from LLMs as passive text generators to LLMs as **tool-augmented agents**, directly influencing the design of modern [function calling](term_function_calling.md) APIs and [agent orchestration](term_agent_orchestration.md) systems.

## Historical Context

| Date | Event | Significance |
|------|-------|--------------|
| **Oct 2022** | ReAct paper (Yao et al.) | Established interleaved reasoning + acting paradigm via prompting |
| **Feb 2023** | **Toolformer published** (Schick et al., Meta AI) | First self-supervised approach to tool learning in LLMs; arXiv:2302.04761 |
| **Jun 2023** | OpenAI function calling launch | First production API for structured tool invocation, influenced by Toolformer's conceptual framing |
| **2023** | Gorilla, ToolLLM | Extended tool-use to retrieval-augmented and large-scale API settings |
| **Nov 2024** | Anthropic MCP | Standardized protocol for tool integration, building on the tool-use paradigm Toolformer helped establish |

Toolformer was published at NeurIPS 2023 after its February 2023 arXiv release. It occupies a pivotal position between early prompting-based tool use (ReAct) and the production-grade, API-native function calling that followed.

## Key Properties

### 1. Self-Supervised Tool Learning
Toolformer requires only **a handful of demonstrations** (few-shot examples) for each API. It does not rely on large-scale human-annotated tool-use datasets. Instead, it leverages the language model itself to generate, execute, and filter API call annotations -- making tool learning scalable and annotation-efficient.

### 2. Loss-Based Filtering
The critical innovation is a **perplexity-based filtering criterion**. After generating candidate API calls at various positions in a text, Toolformer computes the weighted cross-entropy loss with and without each API call result. Only API calls that **reduce the loss on subsequent tokens** (i.e., actually help the model predict what comes next) are retained in the training data. This ensures the model learns to invoke tools only when they genuinely improve its predictions.

### 3. In-Text API Call Representation
Toolformer uses special tokens (`<API>` and `</API>`) to delimit API calls within the text stream. The arrow token (`->`) separates the API call from its response. During inference, when the model generates an `<API>` token, decoding pauses, the API is executed, the result is inserted, and decoding resumes after the `</API>` token.

### 4. No Sacrifice of General Capabilities
Unlike approaches that trade general language ability for specialized tool use, Toolformer preserves its core language modeling performance while adding tool invocation capabilities. This is achieved by mixing the original training data with the tool-augmented data during fine-tuning.

### 5. Autonomous Tool Selection
The model learns **when** to use a tool, not just how. It decides autonomously whether a given context warrants an API call, which API to invoke, and what arguments to pass -- without explicit instruction.

## Architecture

### Three-Stage Training Pipeline

```
Stage 1: SAMPLING
  - For each position in a text sequence, the LM generates up to k
    candidate API call positions using probability thresholds
  - For each position, m different API calls are sampled via
    in-context learning with few-shot demonstrations

Stage 2: EXECUTION
  - All candidate API calls are executed against the actual APIs
  - Results are formatted as text sequences:
    <API> tool_name(arguments) -> result </API>

Stage 3: FILTERING + FINE-TUNING
  - For each candidate, compute:
    L_with    = loss on subsequent tokens WITH the API call + result
    L_without = loss on subsequent tokens WITHOUT the API call
  - Retain only calls where: L_without - L_with >= threshold
  - Fine-tune the model on the augmented dataset (original text +
    filtered API calls interleaved at learned positions)
```

### Base Model

Toolformer was built on **GPT-J** (6.7 billion parameters), a publicly available autoregressive language model from EleutherAI. Training data for annotation was drawn from a **subset of CCNet**, a large web-crawled corpus.

### Supported Tools

| Tool | API Function | Purpose |
|------|-------------|---------|
| **Calculator** | `[Calculator: expression]` | Arithmetic (four basic operations) |
| **Q&A System** | `[QA: question]` | Answering factual questions |
| **Wikipedia Search** | `[WikiSearch: query]` | Information retrieval from Wikipedia |
| **Machine Translation** | `[MT: text, target_lang]` | Translating text between languages |
| **Calendar** | `[Calendar: ]` | Retrieving the current date |

## Notable Systems and Descendants

| System | Year | Relationship to Toolformer |
|--------|------|---------------------------|
| **ReAct** (Yao et al.) | 2022 | Precursor; prompting-based reasoning + acting, no self-supervised learning |
| **Toolformer** (Schick et al.) | 2023 | Self-supervised tool learning; foundational |
| **Gorilla** (UC Berkeley) | 2023 | Retrieval-augmented API calling; fine-tuned LLaMA for API accuracy |
| **ToolLLM** (Tsinghua) | 2023 | Scaled to 16,000+ real-world APIs; introduced ToolBench benchmark |
| **GPT-4 Function Calling** (OpenAI) | 2023 | Production API-native tool invocation; conceptually builds on Toolformer's insight |
| **Claude Tool Use** (Anthropic) | 2024 | Native tool use via Messages API with structured schemas |
| **MCP** (Anthropic) | 2024 | Standardized protocol for tool discovery and invocation across providers |

## Applications

1. **Arithmetic and calculation**: The model learns to invoke a calculator for mathematical expressions it would otherwise compute poorly.
2. **Factual knowledge retrieval**: Wikipedia search and Q&A system calls allow the model to ground its responses in verified information, reducing hallucination.
3. **Temporal reasoning**: The calendar API enables the model to answer questions about current dates and temporal relationships.
4. **Cross-lingual tasks**: Machine translation API calls extend the model's language coverage beyond its training data distribution.
5. **Foundation for agentic AI**: Toolformer's self-supervised paradigm influenced the design of modern tool-use APIs and agent frameworks that underpin systems like [MCP](term_mcp.md) and [agent orchestration](term_agent_orchestration.md) platforms.

## Evaluation Results

Toolformer was evaluated on several downstream benchmarks in a **zero-shot** setting:

- **LAMA** (factual knowledge): Outperformed GPT-3 (175B parameters) despite being 25x smaller (6.7B)
- **Mathematical reasoning**: Substantially improved over the base GPT-J model
- **Question answering**: Competitive with much larger models
- **Multilingual QA**: Underperformed on some multilingual tasks due to limited language coverage in GPT-J's training data
- **Temporal datasets**: Improved via calendar tool integration

## Challenges and Limitations

1. **No tool chaining**: Toolformer cannot invoke one tool and use its result as input to another tool within a single generation pass. Each API call is independent, limiting the complexity of achievable workflows.
2. **No interactive tool use**: The model cannot engage in multi-turn interactions with a tool (e.g., refining a search query based on initial results).
3. **Input sensitivity**: Performance is sensitive to how queries are worded, since the model's decision to invoke a tool depends on the surface form of the input text.
4. **Computational cost**: The three-stage pipeline (sampling, executing, filtering) is computationally expensive, requiring processing of many candidate API calls per training example.
5. **Sample inefficiency**: The filtering step discards a large fraction of generated API call candidates, making the overall process data-inefficient.
6. **Limited to text-in/text-out APIs**: Toolformer only supports tools that accept and return text, excluding APIs with structured input/output schemas (JSON, binary data).
7. **Base model ceiling**: The 6.7B parameter base model limits the quality of tool-use decisions; scaling to larger models was not explored in the original paper.
8. **Static tool set**: The set of available tools is fixed at training time; adding new tools requires rerunning the full training pipeline.

## Related Terms

- [Function Calling](term_function_calling.md) -- Toolformer is a foundational precursor to modern function calling APIs; demonstrated that LLMs can learn to invoke tools autonomously
- [LLM](term_llm.md) -- Toolformer extends large language model capabilities from text generation to tool-augmented generation
- [MCP](term_mcp.md) -- the Model Context Protocol standardizes the tool integration paradigm that Toolformer helped establish
- [Agent Orchestration](term_agent_orchestration.md) -- Toolformer's single-agent tool use is a building block for multi-agent orchestration systems
- [Prompt Engineering](term_prompt_engineering.md) -- Toolformer uses few-shot prompting for API call annotation but moves beyond prompt-only approaches via fine-tuning

## References

### External Sources
- [Schick, T., Dwivedi-Yu, J., Dessi, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." NeurIPS 2023. arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
- [Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629](https://arxiv.org/abs/2210.03629) -- foundational reasoning + acting framework
- [Patil, S. et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." arXiv:2305.15334](https://arxiv.org/abs/2305.15334) -- retrieval-augmented API calling
- [Qin, Y. et al. (2023). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." arXiv:2307.16789](https://arxiv.org/abs/2307.16789) -- large-scale tool-use benchmark

### Vault Sources
- [LLM Glossary](../../0_entry_points/acronym_glossary_llm.md) -- glossary entry for Toolformer
