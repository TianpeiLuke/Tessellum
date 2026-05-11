---
tags:
  - resource
  - terminology
  - agentic_ai
  - tool_use
  - function_calling
  - llm_api
  - structured_output
keywords:
  - function calling
  - tool use
  - tool calling
  - JSON schema
  - structured output
  - ReAct
  - Toolformer
  - OpenAI function calling
  - Claude tool use
  - Gemini function calling
  - parallel function calling
  - forced function calling
  - tool_choice
  - Model Context Protocol
  - MCP
  - chain-of-thought
  - reasoning and acting
topics:
  - LLM APIs
  - AI Agent Architecture
  - Tool-Augmented Language Models
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Function Calling (Tool Use)

## Definition

**Function calling** (also called **tool use** or **tool calling**) is a capability of large language models that allows them to invoke external functions, APIs, and tools by generating structured output (typically JSON) that specifies which function to call and what arguments to pass. Instead of producing only natural language text, the model analyzes a user's request, determines whether an external tool is needed, selects the appropriate function from a developer-defined schema, extracts the required parameters, and outputs a structured invocation request.

Critically, the LLM does not execute the function itself. It produces a structured JSON object containing the function name and arguments; the host application is responsible for executing the function and returning the result to the model for further processing. This separation of concerns -- the model decides *what* to call, the application decides *how* to execute -- is a foundational design principle.

Function calling transforms LLMs from **pure text generators** into **tool-augmented intelligent agents** capable of:
- Querying databases and APIs in real time
- Performing calculations and data transformations
- Interacting with external systems (email, calendars, file systems)
- Chaining multiple tool invocations to solve complex tasks

## Historical Context and Key Milestones

| Date | Milestone | Significance |
|------|-----------|-------------|
| **Oct 2022** | **ReAct paper** (Yao et al., Princeton/Google) | Proposed synergizing **reasoning** (chain-of-thought traces) and **acting** (tool invocation) in an interleaved loop; demonstrated that combining verbal reasoning with actions on external environments (e.g., Wikipedia API) overcomes hallucination and error propagation. Published at ICLR 2023. |
| **Feb 2023** | **Toolformer paper** (Schick et al., Meta AI) | Showed that LLMs can **teach themselves** to use tools via self-supervised learning; the model (GPT-J based) learned when to call APIs (calculator, search, Q&A, translation, calendar) and how to incorporate results — without human-annotated tool-use data. |
| **Jun 2023** | **OpenAI function calling launch** | First production-grade function calling API; developers describe functions as JSON schemas to GPT-3.5-turbo and GPT-4, and the model outputs structured JSON with function name and arguments. Used the `functions` parameter in the Chat Completions API. |
| **Nov 2023** | **OpenAI parallel function calling + `tools` parameter** | OpenAI upgraded from `functions` to the more general `tools` parameter; introduced parallel function calling (models released Nov 6, 2023+), allowing the model to issue multiple tool invocations simultaneously in a single response. |
| **Dec 2023** | **Google Gemini function calling** | Gemini models launched with native function calling support via Vertex AI; function declarations use a similar JSON schema approach. |
| **Apr 2024** | **Anthropic Claude tool use (beta)** | Claude 3 models gained tool use capabilities via the Messages API; tools defined as JSON schemas with `input_schema`; the model returns `tool_use` content blocks. |
| **May 2024** | **Anthropic Claude tool use GA** | Tool use became generally available across Claude API, Amazon Bedrock, and Google Vertex AI. |
| **Aug 2024** | **OpenAI Structured Outputs** | Introduced `strict: true` mode in function definitions (GPT-4o-2024-08-06); guarantees model output is 100% compliant with the provided JSON Schema. Constraint: not compatible with parallel function calling. |
| **Nov 2024** | **Anthropic Model Context Protocol (MCP)** | Open-source standard for connecting AI applications to external tools and data sources; enables a single tool definition to work across providers; rapidly adopted as the de facto tool interface standard. |
| **2025** | **Gorilla, ToolLLM, and open-source tool calling** | Extended function calling capabilities to open-source models (LLaMA, Mistral); Gorilla specifically trained for API calling accuracy. |
| **2025** | **Anthropic Tool Search Tool** | Advanced feature allowing Claude to search across thousands of tools without consuming context window; enables scaling to very large tool sets. |

## How Function Calling Works (Step by Step)

```
1. DEFINE     Developer defines available tools as JSON schemas
              (function name, description, parameters with types)

2. REQUEST    User sends a natural language query to the LLM
              along with the tool definitions

3. ANALYZE    LLM analyzes the query against available tools;
              determines if a tool call is needed

4. GENERATE   LLM outputs a structured JSON object:
              { "function": "get_weather",
                "arguments": { "location": "Seattle", "unit": "fahrenheit" } }

5. EXECUTE    Host application executes the function call
              (LLM does NOT execute it)

6. RETURN     Function result is sent back to the LLM as a
              tool result message

7. SYNTHESIZE LLM incorporates the result into its final
              natural language response to the user

8. ITERATE    (Optional) LLM may issue additional tool calls
              in a multi-step reasoning loop (ReAct pattern)
```

## Taxonomy of Function Calling Variants

### By Invocation Strategy

| Variant | Description | Supported By |
|---------|-------------|-------------|
| **Single function calling** | Model selects and invokes one function per turn | All providers |
| **Parallel function calling** | Model issues multiple function calls simultaneously in one response; enables parallel execution and faster results | OpenAI (Nov 2023+), Anthropic, Google |
| **Sequential (chained) function calling** | Model invokes functions one at a time across multiple turns; output of one informs the next | All providers (via ReAct-style loops) |
| **Forced function calling** (`tool_choice`) | Developer forces the model to call a specific function (or any function) rather than deciding autonomously | OpenAI (`tool_choice: {"type": "function", "function": {"name": "..."}}`), Anthropic (`tool_choice: {"type": "tool", "name": "..."}`), Google |
| **Auto function calling** | Model decides whether to call a function or respond in text (default behavior) | All providers (`tool_choice: "auto"`) |
| **None (disabled)** | Model is prevented from calling any functions | All providers (`tool_choice: "none"`) |

### By Schema Enforcement

| Mode | Description | Provider |
|------|-------------|---------|
| **Standard** | Model follows the schema with best effort; may occasionally produce invalid JSON | OpenAI (default), Anthropic |
| **Strict mode** (`strict: true`) | Guaranteed 100% JSON Schema compliance; uses constrained decoding | OpenAI Structured Outputs (Aug 2024+) |
| **Native schema enforcement** | Schema compliance enforced natively in the model | Google Gemini via Vertex AI |

### By Learning Approach (Research Taxonomy)

| Approach | Mechanism | Example |
|----------|-----------|---------|
| **API-native (provider-trained)** | Model fine-tuned on tool-use data; function calling is a built-in capability | GPT-4, Claude, Gemini |
| **Self-supervised tool learning** | Model learns when and how to use tools from self-generated training data | Toolformer (Meta AI, 2023) |
| **Retrieval-augmented tool selection** | Model retrieves relevant tools from a large tool registry before deciding | Gorilla (UC Berkeley), ToolLLM |
| **Prompt-based (few-shot)** | Tool use elicited via in-context examples without fine-tuning | ReAct prompting, early LangChain agents |

## Relationship to ReAct Pattern

The **ReAct** (Reasoning + Acting) framework (Yao et al., 2022) is the conceptual ancestor of modern function calling. ReAct interleaves:

1. **Thought**: The model generates a verbal reasoning trace (chain-of-thought)
2. **Action**: The model invokes a tool (e.g., Wikipedia search, calculator)
3. **Observation**: The tool result is fed back to the model
4. **Repeat**: The loop continues until the task is complete

Modern function calling APIs operationalize the ReAct pattern at the infrastructure level:

| ReAct Concept | Modern API Equivalent |
|---------------|----------------------|
| Thought | Model's internal reasoning (may be visible in chain-of-thought or hidden) |
| Action | `tool_calls` array in the API response |
| Observation | `tool` role message containing function result |
| Loop | Multi-turn conversation with alternating assistant/tool messages |

The key difference: ReAct was originally a **prompting technique** (few-shot examples instructing the model to output "Thought/Action/Observation"); modern function calling is an **API-level capability** where the model has been fine-tuned to produce structured tool invocations natively.

## JSON Schema Tool Definition (Cross-Provider Comparison)

### OpenAI Format
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": { "type": "string", "description": "City name" },
        "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
      },
      "required": ["location"]
    },
    "strict": true
  }
}
```

### Anthropic Format
```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City name" },
      "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["location"]
  }
}
```

### Google Gemini Format
```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "parameters": {
    "type": "OBJECT",
    "properties": {
      "location": { "type": "STRING", "description": "City name" },
      "unit": { "type": "STRING", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["location"]
  }
}
```

All three providers converge on JSON Schema as the tool definition language, with minor syntactic differences. The Model Context Protocol (MCP) aims to unify these into a single schema format.

## Key Properties

1. **Separation of decision and execution**: The LLM decides what function to call and with what arguments; the host application executes the function. This separation is a security boundary — the model never has direct access to external systems.
2. **JSON Schema as the universal tool language**: All major providers (OpenAI, Anthropic, Google) use JSON Schema to define function signatures, creating a convergent standard for tool descriptions.
3. **Structured output guarantee**: With strict mode (OpenAI) or native enforcement (Google), function calling output can be guaranteed to conform to the schema — critical for production reliability.
4. **Parallel invocation for efficiency**: Modern models can issue multiple tool calls in a single response, enabling concurrent execution and reduced round-trip latency.
5. **Composability with reasoning**: Function calling is the operational mechanism that makes ReAct-style reasoning loops possible at scale — each "action" in a reasoning chain is a function call.
6. **Context window cost**: Each tool definition consumes tokens in the context window; applications with hundreds of tools face context budget constraints (MCP's Tool Search Tool addresses this).
7. **Hallucinated function calls**: Models may generate calls to functions that do not exist, pass incorrect argument types, or fabricate parameter values — validation and error handling are essential.
8. **Token overhead**: The function call JSON output, tool definitions, and tool results all consume tokens; complex tool-use workflows can be expensive.
9. **Provider-specific fine-tuning**: Each provider trains its models specifically on tool-use data; tool calling accuracy varies significantly across models and is a key differentiator.
10. **Backward compatibility tension**: OpenAI's migration from `functions` to `tools` parameter, and from single to parallel calling, illustrates the ongoing API evolution; applications must handle version differences.
11. **Security surface**: Function calling creates an attack surface — adversarial prompts can attempt to trick the model into calling unintended functions or passing malicious arguments (prompt injection for tool use).
12. **Foundation for agentic systems**: Function calling is the primitive capability that enables agents, multi-agent orchestration, and autonomous workflows — without it, LLMs remain passive text generators.

## Notable Systems and Implementations

| System | Approach | Key Contribution |
|--------|----------|-----------------|
| **Toolformer** (Meta AI, 2023) | Self-supervised tool learning | Proved LLMs can autonomously learn when and how to use tools without human annotation |
| **GPT-4 / GPT-4o** (OpenAI) | API-native function calling | First production-scale implementation; introduced parallel calling and structured outputs |
| **Claude 3/4** (Anthropic) | Tool use via Messages API | Native tool use with `tool_use` content blocks; integrated with MCP ecosystem |
| **Gemini** (Google) | Function calling via Vertex AI | Native schema enforcement; deep integration with Google Cloud services |
| **Gorilla** (UC Berkeley, 2023) | Retrieval-augmented API calling | Fine-tuned LLaMA for accurate API invocation; outperformed GPT-4 on API call accuracy |
| **ToolLLM** (Tsinghua, 2023) | Large-scale tool-use training | Trained on 16,000+ real-world APIs; introduced ToolBench evaluation framework |
| **ReAct agents** (LangChain, LangGraph) | Framework-level ReAct implementation | Operationalized the ReAct loop as reusable agent components with tool registries |
| **Model Context Protocol (MCP)** (Anthropic, 2024) | Standardized tool interface | Universal protocol for tool discovery, schema definition, and invocation across providers |

## Challenges and Limitations

1. **Hallucinated tool calls**: Models may invoke non-existent functions, pass arguments of wrong types, or fabricate values — especially when the tool set is large or descriptions are ambiguous
2. **Schema complexity limits**: Very complex nested schemas with many optional fields increase error rates; models perform best with flat, well-described schemas
3. **Tool selection at scale**: With hundreds or thousands of available tools, models struggle to select the right one; retrieval-augmented approaches (Gorilla, MCP Tool Search) are needed
4. **Latency from multi-turn loops**: ReAct-style multi-step tool use requires sequential API calls, each adding latency; end-to-end response times can become unacceptable for interactive applications
5. **Cost amplification**: Each tool call requires at least two API calls (one to decide the call, one to process the result); complex workflows can consume 10-50x more tokens than a single completion
6. **Security and prompt injection**: Adversarial users can craft inputs that trick the model into calling sensitive functions or passing harmful arguments; robust input validation and output filtering are essential
7. **Provider fragmentation**: Despite convergence on JSON Schema, each provider's API has different tool definition formats, response structures, and feature sets (parallel calling, strict mode, streaming)
8. **Error recovery**: When a function call fails (network error, invalid response, timeout), the model must gracefully handle the error — but error-recovery behavior varies and is often poor without explicit prompting
9. **Structured output vs. parallel calling trade-off**: OpenAI's strict structured outputs are incompatible with parallel function calling, forcing developers to choose between schema guarantees and invocation efficiency
10. **Evaluation gaps**: No standardized benchmarks comprehensively evaluate tool calling accuracy across providers; ToolBench and API-Bank exist but are not universally adopted

## Related Terms

- [Agent Orchestration](term_agent_orchestration.md) -- function calling is the primitive that enables orchestrated agents to interact with external systems
- [Neuro-Symbolic AI](term_neuro_symbolic.md) -- function calling can serve as the interface between neural LLM components and symbolic verification systems
- [Dual-Paradigm Framework](term_dual_paradigm_framework.md) -- function calling is a neural/generative paradigm concept; symbolic agents use direct API calls, not LLM-mediated tool invocation

## References

### Vault Sources
- [Agentic AI Survey (Abou Ali & Dornaika, 2025)](../papers/lit_abouali2025agentic.md) -- covers tool use as a core capability of agentic AI systems

### External Sources
- [Yao et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629](https://arxiv.org/abs/2210.03629) -- foundational paper combining chain-of-thought reasoning with tool actions
- [Schick et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." Meta AI. arXiv:2302.04761](https://arxiv.org/abs/2302.04761) -- self-supervised tool learning in LLMs
- [OpenAI (2023). "Function Calling and Other API Updates." Blog announcement, June 2023](https://openai.com/index/function-calling-and-other-api-updates/) -- original launch announcement for function calling
- [OpenAI Function Calling API Documentation (2025)](https://platform.openai.com/docs/guides/function-calling) -- current API reference for function calling and tool_choice
- [OpenAI (2024). "Introducing Structured Outputs in the API." Blog announcement, August 2024](https://openai.com/index/introducing-structured-outputs-in-the-api/) -- strict mode for guaranteed schema compliance
- [Anthropic: How to Implement Tool Use - Claude API Documentation (2025)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) -- Claude tool use implementation guide
- [Anthropic (2024). "Introducing the Model Context Protocol." Blog announcement, November 2024](https://www.anthropic.com/news/model-context-protocol) -- MCP as the standardized tool interface layer
- [Martin Fowler (2024). "Function Calling Using LLMs."](https://martinfowler.com/articles/function-call-LLM.html) -- authoritative software engineering perspective on function calling architecture
- [The Evolution of LLM Tool-Use from API Calls to Agentic Applications. TechTalks (2025)](https://bdtechtalks.com/2025/12/29/llm-tool-use-agentic-ai/) -- historical overview of tool-use evolution
- [Google: Function Calling with the Gemini API (2025)](https://ai.google.dev/gemini-api/docs/function-calling) -- Google's function calling documentation and approach
