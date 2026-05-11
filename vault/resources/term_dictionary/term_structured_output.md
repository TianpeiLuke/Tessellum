---
tags:
  - resource
  - terminology
  - generative_ai
  - llm_engineering
  - constrained_decoding
keywords:
  - structured output
  - constrained decoding
  - JSON mode
  - schema-constrained generation
  - finite state machine
  - grammar-guided generation
  - Pydantic
  - Outlines
  - guided generation
  - type-safe LLM output
topics:
  - LLM Engineering
  - Constrained Generation
  - Type-Safe AI Systems
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Structured Output

## Definition

**Structured output** refers to techniques and mechanisms that constrain a Large Language Model's generation to conform to a predefined schema — typically JSON Schema, XML, or a formal grammar — guaranteeing that the output is machine-parseable and type-safe. Unlike free-form text generation, where LLMs may produce syntactically invalid or schema-violating responses, structured output mechanisms enforce validity at the **token level** during decoding, making post-hoc parsing failures impossible.

The core technical approach is **constrained decoding**: at each generation step, a finite state machine (FSM) or context-free grammar (CFG) derived from the target schema masks the logit distribution, setting the probability of invalid tokens to zero before sampling. This guarantees that every generated sequence is a valid instance of the schema without sacrificing the model's semantic capabilities.

Structured output bridges the gap between LLMs (which produce natural language) and software systems (which require typed data structures), making it a foundational capability for [function calling](term_function_calling.md), agentic workflows, and any application where LLM outputs must be programmatically consumed.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| **2023** | Willard & Louf | Published "Efficient Guided Generation for Large Language Models" — introduced FSM-based constrained decoding via the **Outlines** library; first practical framework for grammar-guided generation |
| **2023** | OpenAI | Released JSON mode for GPT-4 — guaranteed valid JSON output but without schema enforcement |
| **2024 (Feb)** | Instructor library | Gained popularity as a wrapper using Pydantic models for structured extraction with retry logic |
| **2024 (Aug)** | OpenAI | Launched **Structured Outputs** — native JSON Schema enforcement in the API; 100% schema compliance; based on constrained decoding |
| **2024** | Microsoft | Released **llguidance** — Rust-based constrained decoding engine supporting JSON Schema, regex, and CFGs; integrated into Guidance library |
| **2025** | MLX Community | **XGrammar** — compiled grammar-based decoding for local/edge LLMs |
| **2025 (Nov)** | Anthropic | Added structured output support to Claude API — JSON Schema enforcement with `response_format` parameter |
| **2026** | Industry-wide | Structured output becomes standard across major LLM providers (OpenAI, Anthropic, Google, Mistral); server-side enforcement is the norm |

## Taxonomy

### By Enforcement Mechanism

| Mechanism | How It Works | Guarantee | Examples |
|-----------|-------------|-----------|----------|
| **Prompt-based** | Instructions in the system/user prompt asking for JSON | None — model may still produce invalid output | Early ChatGPT usage, basic prompting |
| **Retry-based** | Generate freely, validate, retry on failure | Probabilistic (eventually valid) | Instructor library, LangChain output parsers |
| **JSON mode** | Provider-level guarantee of valid JSON (no schema) | Syntactically valid JSON | OpenAI JSON mode (2023), Anthropic |
| **Schema-constrained** | FSM/CFG masks invalid tokens at each decoding step | 100% schema compliance | OpenAI Structured Outputs, Outlines, llguidance |
| **Function calling** | Schema defined via tool/function definitions; output is structured tool call | Schema-compliant tool invocations | OpenAI function calling, Anthropic tool use |

### By Constraint Formalism

| Formalism | Expressiveness | Use Case |
|-----------|---------------|----------|
| **Regular expression** | Token-level patterns | Dates, phone numbers, enums, formatted strings |
| **JSON Schema** | Nested objects, arrays, enums, unions | API responses, data extraction, form filling |
| **Context-free grammar** | Recursive structures, programming languages | Code generation, mathematical expressions |
| **Pydantic / Zod models** | Type-safe objects with validation | Python/TypeScript application integration |

### By Integration Point

| Integration | Description | Trade-offs |
|-------------|-------------|------------|
| **Server-side (API)** | Provider enforces constraints in their inference pipeline | Best performance; limited to provider-supported schemas |
| **Client-side wrapper** | Library wraps API calls with validation + retry | Works with any model; no guarantee without retries |
| **Local inference** | Constrained decoding in local serving framework (vLLM, llama.cpp) | Full control; requires hosting infrastructure |

## Key Properties

- **Token-level enforcement**: Invalid tokens are masked before sampling — the model never generates an invalid sequence, unlike post-hoc validation which catches errors after generation
- **Zero-overhead guarantee**: Schema compliance adds negligible latency because the FSM/CFG state machine is pre-compiled and token masking is a simple bitwise operation during decoding
- **Semantic preservation**: Constraining syntax does not significantly degrade the model's ability to produce semantically correct content — the model retains its full reasoning capability within the valid token space
- **Schema coverage**: Modern implementations support the full JSON Schema draft 2020-12 specification including `$ref`, `anyOf`, `allOf`, `oneOf`, recursive schemas, and string format constraints
- **Composability**: Structured outputs compose naturally with function calling — tool definitions are JSON Schemas, and the model's tool invocation is a structured output
- **Streaming compatible**: Constrained decoding works with streaming APIs — each streamed token is guaranteed to be part of a valid final output
- **Model-agnostic principle**: The constrained decoding technique (FSM masking) works with any autoregressive language model regardless of architecture or training
- **Nested validation**: Supports deeply nested objects, arrays of objects, optional fields, and union types — matching the expressiveness of real-world API schemas
- **Deterministic parsing**: Because the output is guaranteed schema-valid, parsing never fails — eliminating an entire class of runtime errors in LLM-integrated applications
- **Reduced token usage**: Structured output typically uses fewer tokens than asking the model to produce markdown or natural language that must be parsed, because it eliminates explanatory text

## Notable Systems

| System | Year | Approach | Key Feature |
|--------|------|----------|-------------|
| **Outlines** | 2023 | FSM-based token masking from regex/JSON Schema | First practical open-source guided generation; academic foundation (Willard & Louf) |
| **OpenAI Structured Outputs** | 2024 | Server-side constrained decoding via JSON Schema | 100% schema compliance; native API support; `strict: true` parameter |
| **Instructor** | 2024 | Pydantic wrapper with retry logic | Developer-friendly Python API; works with multiple providers; validation + retry |
| **llguidance** (Microsoft) | 2024 | Rust engine supporting JSON Schema + regex + CFG | High performance; integrated into Guidance library; supports complex grammars |
| **XGrammar** | 2025 | Compiled grammar-based constrained decoding | Optimized for local/edge deployment; fast grammar compilation |
| **Anthropic Structured Outputs** | 2025 | Server-side JSON Schema enforcement for Claude | `response_format` parameter; supports tool use schemas |
| **vLLM + Outlines** | 2024 | Integration of Outlines into vLLM serving framework | Production-grade serving with guided generation |
| **LangChain Output Parsers** | 2023 | Prompt + parse + retry pattern | Widely adopted; works with any LLM; no decoding-level guarantee |
| **Marvin** | 2023 | Pydantic-first LLM extraction library | Type-safe Python; maps Python types to LLM prompts |

## Challenges and Limitations

### Fundamental
1. **Schema expressiveness vs. model capability**: Highly constrained schemas (e.g., requiring specific numeric ranges or complex conditional logic) may force the model into outputs that are syntactically valid but semantically nonsensical
2. **Recursive schema complexity**: Deeply recursive or self-referencing schemas can cause exponential blowup in the FSM state space, increasing compilation time and memory usage
3. **Cross-field dependencies**: JSON Schema cannot express arbitrary constraints between fields (e.g., "if field A is 'premium', field B must be > 100") — these require post-validation logic

### Practical
4. **Provider lock-in**: Server-side structured output features vary across providers in schema support, parameter names, and behavior — making multi-provider applications harder
5. **Schema design skill**: Writing effective JSON Schemas for LLM consumption requires understanding both Schema specification and LLM behavior — poor schemas produce valid but useless outputs
6. **Latency for complex schemas**: While token masking itself is fast, compiling complex schemas into FSMs can add startup latency, especially for schemas with many union types
7. **Streaming partial objects**: Streaming structured output requires careful handling of partial JSON — consumers must buffer until a complete object boundary
8. **Hallucination within schema**: Structured output guarantees format, not factual correctness — the model can produce a perfectly valid JSON object with completely fabricated content

## Related Terms

- **[Function Calling](term_function_calling.md)**: Structured output is the enforcement mechanism for function/tool call arguments — every function call is a structured output constrained by the tool's parameter schema
- **[Guardrails](term_guardrails.md)**: Structured output is a form of output guardrail that enforces format constraints; guardrails also cover content safety, which structured output does not address
- **[Agent Orchestration](term_agent_orchestration.md)**: Multi-agent workflows depend on structured output for type-safe inter-agent communication — agent outputs must conform to defined interfaces
- **[Prompt Engineering](term_prompt_engineering.md)**: Before constrained decoding, structured output relied entirely on prompt engineering techniques; prompt design still matters for semantic quality within the schema
- **[LLM-as-a-Judge](term_llm_as_a_judge.md)**: Evaluation systems use structured output to enforce consistent scoring formats (e.g., JSON with `score`, `reasoning`, `verdict` fields)
- **[Chain of Thought](term_chain_of_thought.md)**: Structured output can capture reasoning traces in typed format — combining CoT reasoning with schema enforcement for interpretable structured responses
- **[Observability (Agent Systems)](term_observability_agent_systems.md)**: Structured output enables systematic logging and tracing of agent interactions — every input/output conforms to a known schema

## References

### Vault Sources
- [Digest: Designing Multi-Agent Systems](../digest/digest_multi_agent_systems_dibia.md) — Dibia's picoagents framework emphasizes structured output as a core agent component

### External Sources
- [Willard, B. & Louf, R. (2023). "Efficient Guided Generation for Large Language Models." arXiv:2307.09702](https://arxiv.org/abs/2307.09702) — foundational paper on FSM-based constrained decoding
- [OpenAI (2024). "Introducing Structured Outputs in the API." OpenAI Blog](https://openai.com/index/introducing-structured-outputs-in-the-api/) — announcement of native JSON Schema enforcement
- [Outlines library — GitHub](https://github.com/dottxt-ai/outlines) — open-source guided generation framework
- [Instructor library — GitHub](https://github.com/jxnl/instructor) — Pydantic-based structured extraction for LLMs
- [llguidance — Microsoft GitHub](https://github.com/microsoft/llguidance) — Rust-based constrained decoding engine
- [Anthropic (2025). "Structured Output Support." Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/structured-output) — Claude structured output documentation
- [Wikipedia: Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine) — the theoretical foundation for constrained decoding
