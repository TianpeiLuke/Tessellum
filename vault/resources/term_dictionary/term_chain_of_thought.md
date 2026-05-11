---
tags:
  - resource
  - terminology
  - nlp
  - reasoning
  - prompting
keywords:
  - chain of thought
  - CoT
  - reasoning steps
  - few-shot prompting
  - emergent abilities
  - GSM8K
  - step-by-step reasoning
  - prompt engineering
  - zero-shot CoT
  - self-consistency
topics:
  - Natural Language Processing
  - Reasoning
  - Prompt Engineering
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Chain of Thought (CoT)

## Definition

**Chain of Thought (CoT)** is a prompting technique that augments few-shot exemplars with intermediate natural language reasoning steps, enabling large language models to perform complex multi-step reasoning at inference time without any fine-tuning or architectural changes. Introduced by Wei et al. (2022), CoT prompting transforms standard (question, answer) exemplars into (question, reasoning chain, answer) triples, causing the model to generate similar step-by-step reasoning before producing its final answer. CoT is an **emergent capability**: it provides meaningful gains only for models with roughly 100B or more parameters, while smaller models see flat or degraded performance. PaLM 540B with just 8 hand-written CoT exemplars achieved 56.9% on GSM8K, surpassing fine-tuned GPT-3 with a verifier (55%).

## Full Name

**Chain of Thought (CoT)**

**Also Known As**: Chain-of-thought prompting, CoT prompting, step-by-step reasoning, intermediate reasoning steps

## Prompt Format

### Standard Few-Shot (Baseline)

In standard few-shot prompting, the model receives k input-output pairs and must generate the answer directly — all reasoning is implicit in a single forward pass:

```
[Question_1, Answer_1, Question_2, Answer_2, ..., Question_k, Answer_k, Question_test]
→ Model generates: Answer_test
```

### Chain-of-Thought Few-Shot

CoT augments each exemplar with intermediate reasoning steps between question and answer:

```
[Question_1, CoT_1, Answer_1, Question_2, CoT_2, Answer_2, ..., Question_k, CoT_k, Answer_k, Question_test]
→ Model generates: CoT_test, Answer_test
```

### Concrete Example

**Standard**:
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
   Each can has 3 tennis balls. How many tennis balls does he have now?
A: The answer is 11.
```

**Chain-of-Thought**:
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
   Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls.
   5 + 6 = 11. The answer is 11.
```

The only structural difference is the presence of intermediate reasoning steps. The final answer is extracted via a trigger phrase ("The answer is ...").

## Key Properties

| Property | Description |
|----------|-------------|
| **Emergent** | Gains appear only at ~100B+ parameters; smaller models degrade (incoherent chains introduce noise before the answer) |
| **Training-free** | Pure inference-time strategy — no labeled rationale data, no verifier, no architectural changes |
| **Task-general** | Same technique works across arithmetic, commonsense, and symbolic reasoning with no task-specific adaptation |
| **Interpretable** | Produces human-readable reasoning traces enabling qualitative error analysis and failure diagnosis |
| **Exemplar-robust** | Robust to annotator variation (3 annotators all outperform standard prompting), exemplar selection, and ordering |

## Empirical Results

### Headline Results (PaLM 540B)

| Category | Benchmark | Standard | CoT | Delta |
|----------|-----------|:--------:|:---:|:-----:|
| Arithmetic | GSM8K | 17.9% | 56.9% | **+39.0** |
| Arithmetic | SVAMP | 69.4% | 79.0% | +9.6 |
| Arithmetic | MAWPS | 79.2% | 93.3% | +14.1 |
| Commonsense | StrategyQA | 68.6% | 77.8% | +9.2 |
| Commonsense | Sports | 80.5% | 95.4% | +14.9 |
| Symbolic (OOD) | Last letter (4 words) | ~0% | 63.0% | +63.0 |
| Symbolic (OOD) | Coin flip (4 flips) | ~50% | 90.2% | +40.2 |

### Ablation Studies (LaMDA 137B, GSM8K)

| Condition | Accuracy | Rules Out |
|-----------|:--------:|-----------|
| Equation only | 5.4% | Math notation alone is insufficient |
| Variable compute (dots) | 6.4% | Extra tokens / compute budget alone don't explain gains |
| Reasoning after answer | 6.1% | Post-hoc reasoning has no causal effect; chain must precede answer |
| **Full Chain of Thought** | **14.3%** | **Natural language reasoning steps are the active ingredient** |

### Emergence Threshold (GPT-3, GSM8K)

| Model Size | Standard | CoT | Effect |
|:----------:|:--------:|:---:|--------|
| 350M | 2.2% | 0.5% | Negative (degradation) |
| 1.3B | ~3% | ~2% | Negative |
| 6.7B | ~6% | ~5% | Flat / slightly negative |
| **175B** | **15.6%** | **46.9%** | **+31.3 (large gain)** |

The threshold is approximately **100B parameters**. This pattern holds across GPT-3, LaMDA, and PaLM — it is a property of scale, not a specific model family.

## Key Variants and Extensions

| Variant | Paper | Year | Innovation | Relationship to CoT |
|---------|-------|------|------------|---------------------|
| **Zero-shot CoT** | Kojima et al. | 2022 | "Let's think step by step" — no exemplars needed | Removes exemplar requirement; slightly weaker |
| **Self-Consistency** | Wang et al. | 2022 | Sample multiple reasoning paths, majority-vote the answer | Improves reliability by ~10-20% over single-path CoT |
| **Tree of Thought (ToT)** | Yao et al. | 2023 | Deliberate search over reasoning tree with backtracking | Extends linear chains to branching exploration |
| **Process Reward Model (PRM)** | Lightman et al. | 2023 | Score each reasoning step individually, not just final answer | Addresses CoT's lack of step-level verification |
| **Least-to-Most** | Zhou et al. | 2022 | Decompose problem into sub-problems, solve sequentially | Addresses length generalization failure |
| **Scratchpad** | Nye et al. | 2021 | Fine-tune model to produce intermediate steps | Pre-CoT approach; requires training (CoT is training-free) |
| **Graph of Thought (GoT)** | Besta et al. | 2023 | Model reasoning as a DAG with merge/refine operations | Generalizes linear and tree reasoning to arbitrary graphs |

## CoT vs Related Approaches

| Dimension | Standard Few-Shot | CoT Prompting | Fine-Tuned Rationale | Scratchpad |
|-----------|:-----------------:|:-------------:|:--------------------:|:----------:|
| **Training required** | No | No | Yes | Yes |
| **Scale requirement** | Moderate | Very Large (≥100B) | Moderate | Large |
| **Task generality** | Broad | Broad | Narrow | Narrow |
| **Interpretable output** | No | Yes | Yes | Partial |
| **Exemplar cost** | Low | Low (8 hand-written) | High (labeled rationales) | High (fine-tuning data) |
| **Reasoning quality** | Poor on multi-step | Good at scale | Good | Good |

## Limitations

1. **Scale dependency**: Requires ≥100B parameter models, excluding practitioners with smaller open-source or cost-constrained models. Later work showed fine-tuning on CoT traces enables the capability at 7B scale, but the prompting-only version remains scale-dependent.
2. **No mechanistic explanation**: The paper demonstrates *that* CoT works but not *why*. Is the model performing genuine multi-step inference, or retrieving and adapting memorized reasoning patterns from training data? This remains an open question.
3. **Hallucinated reasoning**: Models can reach correct or incorrect final answers via plausible-but-wrong intermediate steps. The reasoning trace is interpretable but not necessarily factually reliable.
4. **Output cost**: CoT generates 5-10× more tokens per problem than standard prompting, increasing latency and inference cost with no wall-clock time analysis provided.
5. **No partial credit**: Accuracy treats each problem as binary — a model performing 7 of 8 steps correctly with an arithmetic error in the last step gets 0 credit, same as a model that hallucinates from step 1.
6. **Exemplar information content**: 8 CoT exemplars contain significantly more tokens and implicit domain knowledge than 8 standard exemplars. The comparison may not be token-count-fair.

## Applications to Our Work

- **[SPOT-X](term_spot_x.md)** generates structured decision sets with chain-of-thought examples as part of its output — the disambiguated rules include explicit reasoning traces that investigators can follow.
- **[GreenTEA](term_greentea.md)** investigation automation uses multi-step reasoning in its agentic pipeline; CoT principles inform how prompts decompose complex abuse classification decisions.
- **[ARI](term_ari.md)** investigators provide chain-of-thought prompts to LLMs when using investigation tools, applying the technique in human-AI collaborative workflows.
- **[Human-in-the-Loop](term_human_in_the_loop.md)** systems in payment risk use CoT-style reasoning traces to make LLM decisions auditable and reviewable by human operators.
- Any LLM-based reasoning pipeline in abuse detection benefits from understanding CoT's requirements (scale, exemplar quality) and failure modes (hallucinated reasoning, scale dependency).

## Questions

### Validation (Socratic)
1. The 100B emergence threshold was measured on GPT-3, LaMDA, and PaLM — all *dense decoder-only* models from 2022. What information is missing about (a) Mixture-of-Experts models where "100B" active parameters differs from total parameters, (b) post-2022 smaller models fine-tuned on CoT traces (e.g., Llama-2 7B with reasoning data shows CoT ability), and (c) non-English languages where reasoning patterns in pretraining data may differ? Has the emergence threshold already been *invalidated* by fine-tuning on reasoning data, making it an artifact of the training distribution rather than a fundamental scale requirement? *(WYSIATI lens)*
2. The ablation study concludes "natural language reasoning steps are the active ingredient" — but the comparison was against *equation only*, *variable compute (dots)*, and *reasoning after answer*. The critical missing comparison is **structured reasoning in a formal language** (Python code, first-order logic, symbolic notation). If CoT were tested against "solve this step-by-step using Python" and the Python version performed equally well, would the conclusion change from "natural language reasoning" to "any explicit intermediate computation"? This would fundamentally reframe CoT as a *computation allocation* technique rather than a *language* technique. *(Framing Check lens)*

### Application (Taxonomic)
3. The note explicitly states "no mechanistic explanation" for why CoT works. Can you elaborate on the leading hypotheses? Is CoT (a) *activating memorized reasoning patterns* from pretraining — essentially retrieval of similar worked examples, (b) *distributing computation* across more autoregressive steps — giving the model more serial depth to solve problems it cannot solve in a single forward pass, or (c) *linearizing the reasoning graph* — converting branching logic into a sequential chain that the autoregressive architecture can process? What experiment would *distinguish* between these three hypotheses? *(Elaborative Depth lens)*
4. What if CoT exemplars contained *deliberately incorrect reasoning* with plausible-looking intermediate steps leading to wrong answers? Would the model (a) follow the wrong pattern and produce wrong answers (suggesting CoT is *imitation*, not *reasoning*), (b) ignore the incorrect reasoning and produce correct answers (suggesting the model has genuine reasoning ability that CoT merely *activates*), or (c) produce correct reasoning despite wrong exemplars (suggesting the exemplars serve as a *format template*, not a *content guide*)? This distinguishes the "CoT teaches reasoning" hypothesis from the "CoT activates existing capabilities" hypothesis. *(What If / Divergent lens)*

### Synthesis (Lateral)
5. CoT is itself a paradigm [exaptation](term_architectural_exaptation.md) — the pedagogical technique of "showing your work" (developed for human mathematics education) exapted into LLM prompting. The Related Terms section links to [Socratic Questioning](term_socratic_questioning.md) and [System 1 and System 2](term_system_1_and_system_2.md), but these connections are descriptive, not mechanistic. Could the Socratic method's effectiveness in *human* reasoning (breaking complex questions into manageable steps, forcing explicit justification) explain *why* CoT works in LLMs — because the training data contains examples of humans reasoning Socratically, and CoT exemplars activate those patterns? -> Follow-up: [term_prompt_exaptation](term_prompt_exaptation.md) *(Exaptation lens — applied to the prompting domain)*
6. The Applications section lists [SPOT-X](term_spot_x.md), [GreenTEA](term_greentea.md), and [ARI](term_ari.md) all using CoT-style reasoning in production abuse detection. But limitation #3 (hallucinated reasoning — correct answers via wrong intermediate steps) creates a critical tension in these deployments: the *interpretability benefit* of CoT reasoning traces is undermined if the traces are unreliable. How do these production systems address this? Does [Human-in-the-Loop](term_human_in_the_loop.md) review catch hallucinated reasoning, or does it create a false sense of auditability? What would a [Process Reward Model](../papers/lit_wei2022chain.md) look like applied to abuse investigation reasoning chains? *(Liquid Network lens — bridging CoT limitations with production deployment notes)*

## Related Terms

### Core Concepts
- [LLM](term_llm.md) — CoT is a prompting technique for large language models; the capability emerges only at ~100B+ parameters
- [Scaling Law](term_scaling_law.md) — CoT is a key example of emergent ability: it appears discontinuously with scale, which smooth loss-based scaling laws cannot predict
- [Transfer Learning](term_transfer_learning.md) — CoT exemplars enable few-shot transfer, where reasoning patterns from pretraining are activated through in-context demonstration

### Cognitive Framework
- [System 1 and System 2](term_system_1_and_system_2.md) — Standard prompting elicits System 1 (fast, automatic) responses; CoT explicitly externalizes System 2 (slow, deliberate) reasoning
- [Socratic Questioning](term_socratic_questioning.md) — CoT's step-by-step decomposition parallels the Socratic method of breaking complex questions into manageable steps

### Complementary Techniques
- [RLHF](term_rlhf.md) — RLHF instruction tuning and CoT prompting are complementary: RLHF improves the base model, CoT improves the prompting strategy
- [Fine-Tuning](term_fine_tuning.md) — CoT is training-free; fine-tuning on CoT traces (distillation) enables reasoning in smaller models
- [MLM](term_mlm.md) — MLM pre-trains the encoder representations that underlie understanding tasks; CoT operates at inference time on the decoder/generation side

### Production Systems
- [GreenTEA](term_greentea.md) — Uses multi-step reasoning in agentic automation; CoT principles inform prompt decomposition
- [SPOT-X](term_spot_x.md) — Generates structured decision rules with chain-of-thought examples
- [Project: SPOT-X](../../projects/project_spot_x.md) — Uses CoT demonstrations in decision rules

## References

### Primary Source
- Wei, J. et al. (2022). [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](../papers/lit_wei2022chain.md). NeurIPS 2022. arXiv:2201.11903. *Primary reference — introduced and empirically validated CoT prompting across 12 benchmarks.*

### Key Extensions
- Kojima, T. et al. (2022). Large Language Models are Zero-Shot Reasoners. NeurIPS 2022. *Zero-shot CoT: "Let's think step by step."*
- Wang, X. et al. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. arXiv:2203.11171. *Multiple reasoning paths + majority vote.*
- Yao, S. et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. *Branching search over reasoning trees.*
- Lightman, H. et al. (2023). Let's Verify Step by Step. ICLR 2024. *Process Reward Models for step-level verification.*

### Related Literature
- [GPT-3 (Brown et al., 2020)](../papers/lit_brown2020language.md) — Introduced few-shot in-context learning, the paradigm CoT extends
- [Scaling Laws (Kaplan et al., 2020)](../papers/lit_kaplan2020scaling.md) — Smooth loss scaling; CoT shows discrete capability emergence not predicted by scaling laws
- [InstructGPT (Ouyang et al., 2022)](../papers/lit_ouyang2022training.md) — RLHF instruction following is complementary to CoT prompting
