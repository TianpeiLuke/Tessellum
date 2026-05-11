---
tags:
  - resource
  - terminology
  - agentic_ai
  - llm_operations
  - monitoring
  - debugging
  - mlops
keywords:
  - observability
  - LLM observability
  - agent observability
  - tracing
  - monitoring
  - debugging
  - LangSmith
  - Arize Phoenix
  - OpenTelemetry
  - token usage
  - latency tracking
  - cost tracking
  - drift detection
  - trajectory tracing
  - prompt logging
  - Langfuse
  - Weights and Biases Weave
topics:
  - LLM Operations
  - Agent Engineering
  - Production AI Systems
language: markdown
date of note: 2026-03-12
status: active
building_block: concept
---

# Observability (Agent Systems)

## Definition

**Observability** in the context of LLM-based agent systems is the practice of monitoring, tracing, and analyzing every aspect of an AI agent's execution -- from the prompts sent to the model, through intermediate reasoning steps and tool invocations, to the final responses generated -- in order to understand system behavior, diagnose failures, optimize performance, control costs, and ensure quality in production.

Adapted from traditional software observability (the "three pillars" of logs, metrics, and traces), LLM/agent observability extends these concepts with domain-specific telemetry:
- **Prompt/completion logging** replaces traditional request/response logging
- **Token usage and cost tracking** replaces traditional resource utilization metrics
- **Trajectory tracing** (the sequence of reasoning steps, tool calls, and decisions an agent makes) replaces traditional distributed request tracing
- **Quality evaluation** (factuality, relevance, toxicity, groundedness) replaces traditional correctness assertions

The field emerged as a distinct discipline in 2023-2024 as LLM applications moved from prototypes to production, and the non-deterministic nature of LLM outputs made traditional monitoring approaches insufficient.

## Historical Context

| Year | Milestone | Significance |
|------|-----------|-------------|
| **2010s** | Traditional observability matures (Prometheus, Grafana, Jaeger, Datadog) | Three pillars (logs, metrics, traces) become industry standard for software systems |
| **2017** | OpenTelemetry predecessor projects (OpenTracing, OpenCensus) | Vendor-neutral telemetry collection standards emerge |
| **2021-2022** | MLOps observability (Weights & Biases, MLflow) | Model training monitoring (loss curves, hyperparameters, experiment tracking); focused on training, not inference |
| **2023 (Mar)** | **LangSmith** beta launched (LangChain) | First purpose-built LLM application observability platform; trace-level visibility into chain/agent execution |
| **2023 (Aug)** | **Arize Phoenix** open-source release | Open-source LLM observability built on OpenTelemetry; tracing, evaluation, and debugging |
| **2023** | **Helicone**, **Langfuse**, **Braintrust** emerge | Ecosystem of specialized LLM observability startups; both open-source and commercial options |
| **2024 (Apr)** | **OpenTelemetry GenAI Semantic Conventions** SIG formed | Industry standardization effort: defines schema for LLM spans, token metrics, prompt/completion events, tool call attributes |
| **2024** | **W&B Weave** launched | Weights & Biases pivots from training-focused to inference/agent observability with @weave.op decorator pattern |
| **2024** | **Datadog LLM Observability** GA | Enterprise observability vendors (Datadog, Splunk, New Relic) add LLM-specific features, bridging traditional and AI observability |
| **2025** | **OpenTelemetry AI Agent Semantic Conventions** proposed | Extends GenAI conventions with agent-specific concepts: tasks, actions, agents, teams, artifacts, memory |
| **2025** | LangSmith reaches 1B+ trace logs | Scale validation; production adoption across thousands of companies (Klarna, Elastic, etc.) |

## Relationship to Traditional Observability

| Traditional Pillar | Traditional Software | LLM/Agent Equivalent | Key Difference |
|--------------------|---------------------|----------------------|----------------|
| **Logs** | Application logs (structured events) | Prompt/completion logs; tool call logs; guardrail activation logs | LLM logs contain natural language content (prompts, completions) requiring semantic analysis, not just pattern matching |
| **Metrics** | Latency (P50/P99), error rates, throughput, CPU/memory | Token usage, cost per request, latency per LLM call, error rates, quality scores (factuality, relevance, toxicity) | LLM metrics include model-specific dimensions (tokens, cost) and quality dimensions (no traditional analog) |
| **Traces** | Distributed request traces (spans across microservices) | Trajectory traces: spans for each reasoning step, tool invocation, retrieval, and LLM call in an agent's execution | Agent traces are trees/DAGs of cognitive steps, not just service-to-service calls; include non-deterministic branching |

### What LLM Observability Adds Beyond Traditional

| Capability | Description | Why Traditional Tools Cannot Provide This |
|-----------|-------------|------------------------------------------|
| **Semantic evaluation** | Automated scoring of output quality (factuality, groundedness, relevance, toxicity) | Traditional tools check structural correctness (HTTP 200, schema validation); LLM outputs require semantic judgment |
| **Prompt versioning** | Track which prompt template version produced which outputs; A/B test prompt variants | No analog in traditional software (code versioning exists, but prompt behavior is non-deterministic) |
| **Cost attribution** | Token-level cost tracking per request, per user, per feature, per model | Traditional compute costs are infrastructure-level; LLM costs are request-level and vary by input/output length |
| **Drift detection** | Detect when model behavior changes over time (output distribution shifts, topic drift, quality degradation) | Traditional drift detection exists for ML models, but LLM drift involves semantic changes in natural language output |
| **Human feedback loops** | Capture user thumbs-up/down, corrections, and escalations linked to specific traces | Traditional user feedback is product-level; LLM feedback must be linked to specific model interactions |

## Taxonomy of Observability Capabilities

### Core Telemetry

| Capability | Description | Key Metrics |
|-----------|-------------|-------------|
| **Tracing** | End-to-end visibility into agent execution: every LLM call, tool invocation, retrieval step, and reasoning decision captured as spans in a trace tree | Span duration, span count, trace depth, branching factor |
| **Prompt/Completion Logging** | Capture full input prompts and output completions for every LLM interaction | Prompt length (tokens), completion length, prompt template ID, model ID |
| **Token Accounting** | Track token consumption across input, output, and total; map to cost | Input tokens, output tokens, total tokens, cost per request, cost per user/feature |
| **Latency Monitoring** | Measure time for each component: LLM inference, tool execution, retrieval, guardrail checks | P50/P95/P99 latency, time-to-first-token (TTFT), tokens-per-second (TPS) |
| **Error Tracking** | Capture and categorize failures: model errors, tool failures, timeout, guardrail blocks, rate limits | Error rate, error type distribution, retry rate, fallback activation rate |

### Quality and Evaluation

| Capability | Description | Methods |
|-----------|-------------|---------|
| **Automated Evaluation** | Score outputs on quality dimensions without human review | LLM-as-judge, NLI-based factuality checks, semantic similarity, toxicity classifiers |
| **Groundedness Checking** | Verify that RAG-generated answers are supported by retrieved documents | Entailment models, citation verification, source attribution scoring |
| **Hallucination Detection** | Identify outputs that contain fabricated facts or unsupported claims | Cross-reference with knowledge base, self-consistency checks, confidence scoring |
| **Human Feedback Integration** | Capture explicit (thumbs up/down) and implicit (follow-up questions, abandonment) user signals | Feedback rate, positive/negative ratio, feedback-to-trace linking |

### Operational Intelligence

| Capability | Description | Use Case |
|-----------|-------------|----------|
| **Cost Tracking** | Real-time and historical cost analysis by model, feature, user segment, prompt template | Budget management, cost optimization, model selection decisions |
| **Drift Detection** | Identify shifts in model behavior, output distribution, or quality over time | Cluster visualization, embedding drift monitoring, quality score trend analysis |
| **Regression Detection** | Detect when model or prompt changes degrade output quality | Automated eval suites run on production traces; alert on quality score drops |
| **Usage Analytics** | Understand how users interact with the AI system: feature adoption, conversation patterns, drop-off points | Product decisions, UX improvement, capacity planning |

### Agent-Specific Observability

| Capability | Description | Why Agents Need This |
|-----------|-------------|---------------------|
| **Trajectory Tracing** | Capture the full decision sequence of an agent: which tools it considered, which it selected, what arguments it passed, what results it received | Agents make autonomous multi-step decisions; understanding the reasoning path is essential for debugging |
| **Tool Call Logging** | Record every tool invocation with input arguments, output results, latency, and success/failure | Agents delegate work to tools; tool failures or incorrect tool selection are common failure modes |
| **Decision Point Capture** | Log the model's reasoning at branching points where it chose one action over alternatives | Understanding *why* an agent chose a particular path (vs. alternatives) is critical for optimization |
| **Memory/State Inspection** | Observe the agent's working memory, context accumulation, and state transitions across steps | Long-running agents accumulate context; memory corruption or context overflow causes subtle failures |
| **Multi-Agent Coordination** | Trace interactions between multiple agents in a multi-agent system; message passing, delegation, conflict resolution | Multi-agent systems have emergent behaviors that are invisible without cross-agent tracing |

## Key Properties

1. **Non-determinism as the core challenge**: Unlike traditional software, LLM outputs vary across identical inputs. Observability must capture not just what happened, but the distribution of what could have happened -- requiring statistical analysis of output quality over many invocations, not single-request debugging.

2. **Semantic telemetry**: Traditional observability operates on structured data (HTTP status codes, latency numbers). LLM observability must analyze natural language content (prompts, completions) semantically -- requiring NLP techniques, embedding analysis, and LLM-as-judge evaluation.

3. **Cost as a first-class metric**: In traditional software, compute cost is an infrastructure concern. In LLM systems, cost is a per-request, per-token variable that directly impacts business viability. Observability must track cost with the same granularity as latency and errors.

4. **Trace depth and complexity**: Agent traces are significantly deeper and more complex than traditional distributed traces. A single agent task may generate dozens of LLM calls, tool invocations, and retrieval operations in a tree/DAG structure with non-deterministic branching.

5. **Evaluation is continuous, not periodic**: Traditional ML model monitoring runs batch evaluations on held-out test sets. LLM observability requires continuous, real-time evaluation of production outputs because the model's behavior is prompt-dependent and context-sensitive.

6. **Privacy and data sensitivity**: Prompt and completion logs contain user data, potentially including PII, proprietary information, or sensitive queries. Observability systems must handle this data with appropriate access controls, redaction, and retention policies.

7. **Vendor-agnostic standardization emerging**: OpenTelemetry GenAI Semantic Conventions (2024-2025) are establishing a vendor-neutral schema for LLM telemetry, enabling interoperability across observability platforms and reducing vendor lock-in.

8. **Dual-audience design**: LLM observability serves both engineers (debugging, performance optimization) and business stakeholders (cost management, quality assurance, compliance reporting), requiring different views of the same underlying telemetry.

9. **Feedback loop integration**: Observability is not passive monitoring -- it feeds back into prompt engineering (identifying underperforming prompts), model selection (comparing models on production data), and guardrail tuning (adjusting thresholds based on false positive/negative rates).

10. **Scale challenges**: Production LLM applications generate massive telemetry volumes. LangSmith processes 1B+ traces; each trace may contain multiple spans with full prompt/completion text. Storage, indexing, and querying at this scale requires purpose-built infrastructure.

## Notable Systems and Implementations

| System | Provider | Type | Key Features | License |
|--------|----------|------|-------------|---------|
| **LangSmith** | LangChain (2023) | Commercial (free tier) | Framework-agnostic tracing; custom dashboards (token usage, latency P50/P99, error rates, cost); 1B+ trace scale; agent execution graphs; evaluation datasets; prompt playground | Proprietary |
| **Arize Phoenix** | Arize AI (2023) | Open-source | Built on OpenTelemetry (OTLP); auto-instrumentation for LlamaIndex, LangChain, DSPy, Vercel AI SDK; tracing + evaluation + experiments; embedding drift visualization | Apache 2.0 / Elastic 2.0 |
| **Langfuse** | Langfuse (2023) | Open-source | Self-hosted or cloud; prompt management + tracing + evaluation; session tracking; user-level analytics; cost tracking | MIT |
| **W&B Weave** | Weights & Biases (2024) | Commercial (free tier) | @weave.op decorator for automatic tracing; OpenAI Agents SDK and MCP integration; cost/latency capture; evaluation framework | Proprietary |
| **Braintrust** | Braintrust (2023) | Commercial | Evaluation-first approach; dataset curation from production traces; prompt comparison; quality scoring; real-time monitoring | Proprietary |
| **Datadog LLM Observability** | Datadog (2024) | Commercial | Native OpenTelemetry GenAI semantic conventions support; integrates LLM traces with existing infrastructure monitoring; cost/quality dashboards | Proprietary |
| **Splunk AI Observability** | Splunk (2024) | Commercial | LLM-specific dashboards within Splunk platform; hallucination management; drift detection; cost monitoring | Proprietary |
| **Opik** | Comet (2024) | Open-source | Fast trace logging (~23s for log + eval); evaluation framework; experiment tracking | Apache 2.0 |
| **Helicone** | Helicone (2023) | Open-source (core) | Proxy-based (one-line integration); request logging; cost tracking; rate limiting; caching; prompt versioning | Apache 2.0 |
| **OpenLLMetry** | Traceloop (2024) | Open-source | OpenTelemetry-native; auto-instrumentation for LLM providers; semantic conventions aligned with OTel GenAI SIG | Apache 2.0 |

## OpenTelemetry GenAI Semantic Conventions

The OpenTelemetry GenAI Semantic Conventions (SIG formed April 2024) define a standardized schema for LLM telemetry:

| Convention Area | Attributes Defined | Status (2025) |
|----------------|-------------------|---------------|
| **GenAI Spans** | gen_ai.system, gen_ai.request.model, gen_ai.request.max_tokens, gen_ai.response.finish_reason | Experimental |
| **Token Metrics** | gen_ai.usage.input_tokens, gen_ai.usage.output_tokens, gen_ai.usage.total_tokens | Experimental |
| **Prompt/Completion Events** | gen_ai.prompt (input content), gen_ai.completion (output content) | Experimental |
| **Tool Calls** | gen_ai.tool.name, gen_ai.tool.description, gen_ai.tool.parameters | Experimental |
| **Agent Conventions** | gen_ai.agent.name, gen_ai.task, gen_ai.action, gen_ai.team, gen_ai.artifact, gen_ai.memory | Proposed (2025) |

These conventions enable interoperability: telemetry collected by any OTel-compatible instrumentation can be consumed by any OTel-compatible backend (Phoenix, Datadog, Jaeger, etc.).

## Challenges and Limitations

1. **Telemetry volume explosion**: A single agent task can generate dozens of LLM calls, each producing prompt/completion pairs that may be thousands of tokens. At production scale, storage and indexing costs for observability data can exceed the cost of the LLM calls themselves.

2. **Privacy and compliance**: Full prompt/completion logging captures user data. GDPR right-to-deletion, HIPAA PHI requirements, and data residency rules complicate observability data retention. PII redaction in observability pipelines adds latency and complexity.

3. **Evaluation subjectivity**: Automated quality evaluation (LLM-as-judge) is itself non-deterministic and subject to biases. Different judge models produce different quality scores for the same output. No ground-truth exists for "good" LLM output in most open-ended tasks.

4. **Standardization immaturity**: OpenTelemetry GenAI semantic conventions are still experimental (2025). Agent-specific conventions are in proposal stage. Early adopters risk schema changes that break existing tooling.

5. **Tool fragmentation**: The ecosystem has 15+ competing platforms with overlapping features but different data formats, APIs, and integration patterns. Organizations often adopt multiple tools, creating fragmented observability.

6. **Causal attribution difficulty**: When an agent produces a bad output, attributing the failure to a specific cause (bad prompt, wrong tool selection, retrieval miss, model limitation) requires deep trace analysis. Automated root cause analysis for LLM failures is nascent.

7. **Multi-agent observability gap**: Most tools are designed for single-agent workflows. Multi-agent systems with inter-agent communication, delegation, and emergent behaviors require cross-agent tracing that current tools handle poorly.

8. **Real-time vs. batch tension**: Production systems need real-time alerting (detect quality drops immediately), but thorough evaluation requires batch analysis (run evaluations across thousands of traces). Balancing both in a single platform is architecturally challenging.

9. **Cost of observability itself**: Running LLM-as-judge evaluations on every production trace is expensive. Organizations must sample intelligently -- but sampling means some failures go undetected.

10. **Drift detection immaturity**: While conceptually important, practical drift detection for LLM outputs (detecting when output quality or distribution shifts) is still poorly defined. What constitutes "drift" in natural language output is ambiguous and domain-specific.

## Related Terms

- **[Health Check](term_health_check.md)**: Health checks are one pillar of infrastructure observability alongside metrics, logs, and traces; agent observability extends these traditional pillars with LLM-specific telemetry

- [Guardrails](term_guardrails.md) -- guardrail activations are a key observability signal; observability informs guardrail threshold tuning
- [Compound AI System](term_compound_ai_system.md) -- compound systems with multiple components require end-to-end observability across all components
- [MLOps](term_mlops.md) -- LLM observability extends MLOps practices from training-time to inference-time monitoring
- [LLM](term_llm.md) -- the system being observed; LLM-specific metrics (tokens, cost) define observability requirements
- [Hallucination](term_hallucination.md) -- hallucination detection is a key observability quality metric
- [RAG](term_rag.md) -- RAG pipelines require retrieval-specific observability (relevance scoring, source attribution)
- [MCP](term_mcp.md) -- Model Context Protocol interactions generate tool call telemetry that observability systems capture
- [Multi-Agent Collaboration](term_multi_agent_collaboration.md) -- multi-agent systems present unique observability challenges (cross-agent tracing, emergent behavior monitoring)
- [Red Teaming](term_red_teaming.md) -- observability data from production informs red teaming priorities (identifying common failure patterns)
- **[API Gateway](term_api_gateway.md)**: Centralized gateway logging feeds observability pipelines, providing request metrics, latency tracking, and error rates for monitoring distributed systems
- **[Rate Limiting](term_rate_limiting.md)**: Rate limiter metrics (rejection rate, HTTP 429 count, latency percentiles) are critical observability signals for monitoring system health and detecting abuse patterns
- **[TPS](term_tps.md)**: Transactions Per Second — throughput metric for model inference endpoints

## References

### External Sources
- [OpenTelemetry: An Introduction to Observability for LLM-based Applications (2024)](https://opentelemetry.io/blog/2024/llm-observability/) -- foundational blog post on applying OTel to LLM systems
- [OpenTelemetry: AI Agent Observability - Evolving Standards and Best Practices (2025)](https://opentelemetry.io/blog/2025/ai-agent-observability/) -- agent-specific semantic conventions proposal
- [OpenTelemetry: Semantic Conventions for Generative AI Systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/) -- official specification for GenAI telemetry attributes
- [LangSmith: AI Agent & LLM Observability Platform](https://www.langchain.com/langsmith/observability) -- reference commercial platform documentation
- [Arize Phoenix: Open-Source LLM Observability](https://arize.com/docs/phoenix) -- open-source reference implementation built on OpenTelemetry
- [Splunk: LLM Observability Explained - Prevent Hallucinations, Manage Drift, Control Costs](https://www.splunk.com/en_us/blog/learn/llm-observability.html) -- enterprise perspective on LLM observability components
- [Comet: Best LLM Observability Tools of 2025](https://www.comet.com/site/blog/llm-observability-tools/) -- ecosystem landscape and tool comparison
- [Datadog: LLM Observability Natively Supports OpenTelemetry GenAI Semantic Conventions](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) -- enterprise adoption of OTel GenAI standards
- [Langfuse: Open-Source LLM Engineering Platform](https://langfuse.com) -- MIT-licensed self-hostable alternative
- [Braintrust: 7 Best AI Observability Platforms for LLMs in 2025](https://www.braintrust.dev/articles/best-ai-observability-platforms-2025) -- comparative analysis of observability platforms
