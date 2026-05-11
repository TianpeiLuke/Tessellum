---
tags:
  - resource
  - terminology
  - generative_ai
  - llm_engineering
  - prompt_design
keywords:
  - prompt engineering
  - context engineering
  - few-shot prompting
  - zero-shot prompting
  - chain of thought
  - system prompt
  - prompt optimization
  - in-context learning
  - prompt injection
  - DSPy
  - ReAct
  - Tree of Thought
topics:
  - LLM Engineering
  - Prompt Design
  - AI Interaction Design
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Prompt Engineering

## Definition

**Prompt engineering** is the discipline of designing, structuring, and optimizing natural language inputs to Large Language Models (LLMs) to elicit desired outputs — spanning task instructions, contextual information, examples, formatting directives, and reasoning scaffolds. It is the primary interface through which humans and systems communicate intent to LLMs, and its effectiveness determines the quality, reliability, and safety of LLM-powered applications.

The field has evolved rapidly from ad-hoc prompt crafting (2020) to systematic methodologies incorporating cognitive science, software engineering, and optimization theory. Andrej Karpathy (2025) proposed reframing the discipline as **"[context engineering](term_context_engineering.md)"** — emphasizing that the practitioner's job is to assemble the right information (retrieved documents, tool outputs, conversation history, structured instructions) into the model's context window, not merely to write clever prompt text.

Prompt engineering operates at the intersection of LLM capabilities and human intent, making it foundational to [function calling](term_function_calling.md), [agent orchestration](term_agent_orchestration.md), [structured output](term_structured_output.md), and all agentic AI applications.

## Historical Context

| Year | Contributor | Contribution |
|------|------------|--------------|
| **2020** | Brown et al. (OpenAI) | GPT-3 paper demonstrated **few-shot prompting** — task performance from examples in the prompt without fine-tuning; established in-context learning as a paradigm |
| **2021** | Reynolds & McDonough | Coined "prompt engineering" in the academic literature; systematic study of prompt design patterns |
| **2022** | Wei et al. (Google) | **Chain-of-Thought (CoT)** prompting — intermediate reasoning steps in exemplars dramatically improve multi-step reasoning; NeurIPS |
| **2022** | Kojima et al. | **Zero-shot CoT** — "Let's think step by step" unlocks reasoning without exemplars |
| **2022** | Yao et al. | **ReAct** — interleaving reasoning and action (tool use) in prompts; foundational for agentic AI |
| **2022** | Wang et al. | **Self-Consistency** — sample multiple CoT paths, majority-vote the answer; reduces variance |
| **2023** | Yao et al. | **Tree of Thought (ToT)** — deliberate exploration of reasoning branches using BFS/DFS |
| **2023** | Zhou et al. (Google) | **APE (Automatic Prompt Engineer)** — LLM-generated and LLM-evaluated prompts outperform human-written ones |
| **2023** | Yang et al. (Google) | **OPRO** — LLMs as optimizers for prompt engineering; iterative prompt refinement via optimization |
| **2023** | Khattab et al. | **DSPy** — programmatic prompt optimization replacing hand-written prompts with compiled programs |
| **2024** | Anthropic | System prompt best practices formalized; emphasized structured XML-tagged prompts, role assignment, and explicit constraint specification |
| **2025** | Karpathy | Proposed reframing as **"context engineering"** — assembling the right context (tools, retrieval, history, instructions) matters more than prompt wording |

## Taxonomy

### By Technique Category

| Category | Techniques | When to Use |
|----------|-----------|-------------|
| **Basic prompting** | Zero-shot, few-shot, role prompting, system prompts | Simple tasks; known output format |
| **Reasoning augmentation** | [Chain of Thought](term_chain_of_thought.md), Self-Consistency, Tree of Thought, Least-to-Most | Multi-step reasoning; math; logic |
| **Agentic prompting** | [ReAct](term_react.md), Reflexion, plan-and-solve, tool-use instructions | Tasks requiring external tools or multi-turn interaction |
| **Automatic optimization** | DSPy, APE, OPRO, EvoPrompt, [GreenTEA](term_greentea.md) | Production systems needing consistent, optimized prompts at scale |
| **Security** | Prompt injection defense, system prompt hardening, input sanitization | Any user-facing LLM application |

### By Prompt Component

| Component | Purpose | Example |
|-----------|---------|---------|
| **System prompt** | Persistent instructions defining model behavior, role, and constraints | "You are a fraud analyst. Always cite evidence." |
| **User prompt** | Per-request input with task description and data | "Classify this return request as legitimate or suspicious." |
| **Few-shot examples** | In-context demonstrations of desired input→output mapping | 3-5 labeled examples before the query |
| **Reasoning scaffold** | Explicit structure for the model's reasoning process | "First, identify the key signals. Then, assess each signal. Finally, provide your verdict." |
| **Output format** | Specification of response structure | "Respond in JSON with fields: verdict, confidence, reasoning" |
| **Context/retrieval** | Retrieved documents, tool outputs, or conversation history | RAG-retrieved passages, previous agent actions |

### Evolution: Prompt Engineering → Context Engineering

| Aspect | Prompt Engineering (2020-2023) | Context Engineering (2024+) |
|--------|-------------------------------|----------------------------|
| **Focus** | Crafting the right words | Assembling the right information |
| **Input** | Text prompt only | Prompt + retrieved docs + tool outputs + memory + history |
| **Optimization** | Manual iteration | Programmatic (DSPy, OPRO, APE) |
| **Skill** | Writing craft | Systems design + information architecture |
| **Scope** | Single model call | Multi-turn, multi-tool orchestrated workflows |

## Key Properties

- **Training-free**: Prompt engineering modifies model behavior without gradient updates, fine-tuning, or parameter changes — operating entirely through the input interface
- **Emergent capability gating**: Many prompting techniques (CoT, few-shot) only work above certain model scale thresholds — GPT-3.5+ for CoT, GPT-4+ for complex agentic prompting
- **Sensitivity and fragility**: Small changes in prompt wording, example ordering, or formatting can produce dramatically different outputs — a known challenge for production reliability
- **Composability**: Prompt components (system instructions, examples, reasoning scaffolds, output formats) compose modularly, enabling systematic prompt construction
- **Task generality**: The same prompting techniques (CoT, few-shot, role prompting) transfer across diverse tasks — translation, classification, reasoning, code generation, creative writing
- **Model-specific variation**: Optimal prompts differ across model families (GPT-4 vs. Claude vs. Gemini vs. open-source) — requiring per-model prompt adaptation
- **Diminishing returns from wording**: As models improve, the specific choice of words matters less while the information content (context, examples, tools) matters more — hence the shift to "context engineering"
- **Inverse relationship with fine-tuning**: As prompts become more complex and task-specific, fine-tuning becomes more cost-effective; prompt engineering is preferred for flexibility, fine-tuning for consistent high volume
- **Security surface**: Prompts are the primary attack surface for LLM applications — [prompt injection](term_jailbreak.md) exploits the model's inability to distinguish instructions from data
- **Measurable optimization target**: Prompt quality can be evaluated quantitatively (accuracy, F1, cost per query, latency), enabling systematic optimization via automated methods

## Notable Systems

| System | Year | Approach | Significance |
|--------|------|----------|-------------|
| **GPT-3** | 2020 | In-context learning via few-shot prompting | Established prompt engineering as a paradigm; 175B parameters |
| **CoT (Wei et al.)** | 2022 | Reasoning step exemplars | Unlocked multi-step reasoning; spawned entire subfield |
| **ReAct** | 2022 | Interleaved reasoning + tool actions | Foundation for agentic AI prompting |
| **DSPy** | 2023 | Programmatic prompt compilation and optimization | Replaced hand-crafted prompts with compiled programs; Stanford NLP |
| **APE** | 2023 | LLM-generated prompts outperform human-written | Automated prompt search via LLM scoring |
| **OPRO** | 2023 | LLMs as optimizers for prompt engineering | Meta-optimization: use LLMs to optimize LLM prompts |
| **[GreenTEA](term_greentea.md)** | 2024 | Multi-agent prompt optimization (Predictor + Error Analyzer + Prompt Generator) | Production deployment; +9% AUC; KDD 2025 |
| **Claude System Prompts** | 2024 | XML-structured system prompts with explicit constraints | Formalized best practices for structured prompting |

## Challenges and Limitations

### Fundamental
1. **Prompt sensitivity**: Small, semantically irrelevant changes (punctuation, word order, example ordering) can cause large output differences — undermining reproducibility
2. **No formal semantics**: Prompts are natural language instructions interpreted by neural networks — there is no formal guarantee of how any prompt will be interpreted
3. **Prompt injection vulnerability**: The model cannot fundamentally distinguish between developer instructions and user-injected instructions, creating an unsolved security challenge

### Practical
4. **Evaluation difficulty**: Measuring prompt quality requires representative test sets, automated evaluation, and human judgment — often as expensive as the prompting itself
5. **Transfer across models**: Prompts optimized for one model often underperform on another, requiring re-optimization when switching providers or model versions
6. **Context window limits**: Complex prompts with many examples, retrieved documents, and reasoning scaffolds can exceed context windows, requiring careful context budget management
7. **Cost scaling**: Longer prompts (more examples, more context) cost more per API call — creating a direct trade-off between prompt quality and cost
8. **Skill gap**: Effective prompt engineering requires understanding of both the domain (what you want the model to do) and the model (how it processes instructions) — a rare combination

## Related Terms

- **[Chain of Thought](term_chain_of_thought.md)**: The most influential prompt engineering technique — intermediate reasoning steps in prompts unlock multi-step reasoning
- **[Function Calling](term_function_calling.md)**: Prompts instruct models to invoke tools; the system prompt defines available tools and usage patterns
- **[Structured Output](term_structured_output.md)**: Prompt engineering specifies desired output format; constrained decoding enforces it at the token level
- **[Agent Orchestration](term_agent_orchestration.md)**: Agent system prompts define agent roles, capabilities, and collaboration patterns within orchestration frameworks
- **[Guardrails](term_guardrails.md)**: System prompts are the first line of defense for safety constraints; guardrails provide enforcement beyond prompt-level instructions
- **[Prompt Exaptation](term_prompt_exaptation.md)**: Pattern where human cognitive practices (pedagogy, Socratic method, legal reasoning) are repurposed as prompt techniques — explains why prompt engineering works
- **[GreenTEA](term_greentea.md)**: Production system that automates prompt engineering via multi-agent optimization — transforms SOPs into optimized LLM prompts
- **[RAG](term_rag.md)**: Retrieval-Augmented Generation provides contextual information to prompts — the "context" part of context engineering
- **[Red Teaming](term_red_teaming.md)**: Adversarial prompt testing to discover safety failures and prompt injection vulnerabilities

## References

### Vault Sources
- [Digest: Designing Multi-Agent Systems](../digest/digest_multi_agent_systems_dibia.md) — covers prompt design for multi-agent systems

### External Sources
- [Brown, T. et al. (2020). "Language Models are Few-Shot Learners." NeurIPS](https://arxiv.org/abs/2005.14165) — GPT-3 paper establishing in-context learning
- [Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS](https://arxiv.org/abs/2201.11903) — Chain of Thought
- [Yao, S. et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR](https://arxiv.org/abs/2210.03629) — ReAct prompting
- [Khattab, O. et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines."](https://arxiv.org/abs/2310.03714) — programmatic prompt optimization
- [Zhou, Y. et al. (2023). "Large Language Models Are Human-Level Prompt Engineers." ICLR](https://arxiv.org/abs/2211.01910) — APE
- [Yang, C. et al. (2023). "Large Language Models as Optimizers." arXiv](https://arxiv.org/abs/2309.03409) — OPRO
- [Schulhoff, S. et al. (2024). "The Prompt Report: A Systematic Survey of Prompting Techniques." arXiv](https://arxiv.org/abs/2406.06608) — comprehensive survey of 58+ techniques
- [Wikipedia: Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering)
