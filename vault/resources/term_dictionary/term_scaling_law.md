---
tags:
  - resource
  - terminology
  - deep_learning
  - training
  - language_model
keywords:
  - scaling law
  - power law
  - neural scaling
  - compute optimal
  - Chinchilla
  - Kaplan
  - Hoffmann
  - tokens per parameter
  - IsoFLOP
  - emergent abilities
  - broken scaling law
  - inference scaling
topics:
  - Deep Learning
  - Language Models
  - Training Efficiency
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Scaling Law

## Definition

**Scaling Law** refers to empirical power-law relationships describing how neural network performance (measured by cross-entropy loss) improves as a function of model size (N, non-embedding parameters), dataset size (D, training tokens), and training compute (C, FLOPs). First systematically characterized by Kaplan et al. (2020) for decoder-only Transformers, these laws reveal that loss follows L(X) = (X_c / X)^α_X + L_∞ across 7+ orders of magnitude, where α_X is a small exponent (0.05–0.10) and L_∞ is the irreducible entropy of natural language. The compute-optimal allocation — how to split a fixed compute budget between model size and data — was revised by Hoffmann et al. (2022, "Chinchilla"), who showed N and D should scale equally (N ∝ C^0.50, ~20 tokens per parameter), contradicting Kaplan's model-size-heavy recommendation (N ∝ C^0.73). Scaling laws have since been extended to vision, multimodal, and code domains, with the universal finding that power-law improvement persists but with domain-specific exponents.

## Full Name

**Scaling Law** (also: Neural Scaling Law, Power-Law Scaling)

**Also Known As**: Compute scaling, data scaling, Chinchilla scaling (when referring specifically to compute-optimal allocation)

## Core Power-Law Equations

### Primary Scaling Laws (Kaplan et al., 2020)

When the other two resources are not bottlenecked, each resource independently determines loss:

| Equation | Formula | Exponent | Interpretation |
|----------|---------|----------|----------------|
| **L(N)** | L(N) = (N_c / N)^α_N | α_N ≈ 0.076 | 10× more parameters → ~19% loss reduction |
| **L(D)** | L(D) = (D_c / D)^α_D | α_D ≈ 0.095 | 10× more data → ~22% loss reduction |
| **L(C_min)** | L(C_min) = (C_c / C_min)^α_C | α_C ≈ 0.050 | 10× more compute → ~12% loss reduction |

### Joint Scaling (Overfitting)

Combined model/data dependence, capturing how overfitting emerges when D is too small for N:

```
L(N, D) = [ (N_c / N)^(α_N/α_D) + D_c / D ]^α_D
```

The overfitting penalty δL depends on a single ratio: N^0.74 / D. This predicts the minimum data needed: D ≳ 5×10³ · N^0.74.

### Critical Batch Size

```
B_crit(L) = B* / L^(1/α_B)    where B* ≈ 2×10⁸ tokens, α_B ≈ 0.21
```

Defines the transition between compute-efficient (B ≪ B_crit) and sample-efficient (B ≫ B_crit) training regimes.

## Compute-Optimal Allocation: Kaplan vs. Chinchilla

The most practically important question: given a fixed compute budget C, how should it be split between model size N and training tokens D?

| Dimension | Kaplan et al. (2020) | Chinchilla (Hoffmann et al., 2022) |
|-----------|---------------------|-----------------------------------|
| **N scaling** | N_opt ∝ C^0.73 | N_opt ∝ C^0.50 |
| **D scaling** | D_opt ∝ C^0.27 | D_opt ∝ C^0.50 |
| **Tokens/param** | ~1.7 (GPT-3 era) | ~20 (Chinchilla rule) |
| **Prescription** | Prioritize model size | Scale N and D equally |
| **Methodology** | Single approach, cosine LR | 3 independent methods (IsoFLOP, parametric, envelope) |
| **Practical result** | GPT-3: 175B params, 300B tokens | Chinchilla: 70B params, 1.4T tokens (beat 280B Gopher) |

### Why Kaplan's Allocation Was Revised

1. **Parameter counting**: Kaplan excluded embeddings; Chinchilla included them, affecting small-model measurements
2. **Learning rate coupling**: Kaplan's cosine LR schedule conflated model size effects with learning dynamics
3. **Training duration**: Small models trained suboptimally short, making them appear less data-hungry
4. **Single methodology**: Chinchilla's three independent estimation methods converged; Kaplan used one

### Chinchilla Replication (Epoch AI, 2024)

Besiroglu & Erdil et al. (2024) found issues with Chinchilla's Method 3 (parametric fitting), deriving a corrected estimate of ~25.6 tokens/parameter. The core qualitative conclusion — equal N/D scaling — remains valid.

### Beyond Chinchilla: Inference-Aware Scaling

Sardana et al. (2024) showed that when serving at scale, inference cost (proportional to N per token) dominates. The modified objective:

```
Total Cost = Training FLOPs + Inference FLOPs = 6ND + 2N × (requests × tokens)
```

At high inference demand, it is cheaper to train smaller models much longer. This explains modern practice: LLaMA-3.1 8B trained on 15T tokens (~1,875 tokens/param) is optimized for inference cost, far beyond Chinchilla's 20 tokens/param.

## Architecture Independence

Kaplan's surprising finding: when total non-embedding parameter count N is held fixed, architectural details have minimal effect on performance:

| Variation | Range Tested | Loss Impact |
|-----------|-------------|-------------|
| Width vs. depth (aspect ratio) | 40× variation | <3% loss change |
| Number of attention heads | Varied with d_model fixed | Minimal |
| Feed-forward dimension | d_ff variations | Negligible |

**Only total N matters.** This simplifies model design: choose depth/width based on engineering constraints (parallelism, memory) rather than performance.

## Extensions and Boundaries

### Multimodal Scaling

Henighan et al. (2020) extended scaling laws to image, video, multimodal, and math domains using autoregressive Transformers. The optimal model size exponent N_opt ∝ C^0.7 is remarkably consistent across all modalities, despite different irreducible losses and token vocabularies.

| Domain | Scaling Behavior | Notable Work |
|--------|-----------------|--------------|
| **Vision (ViT)** | Power-law test error vs. compute | Zhai et al. (2022): ViT-G/14 → 90.45% ImageNet |
| **CLIP** | Reproducible scaling for contrastive image-text | Cherti et al. (2023): LAION-5B scaling curves |
| **Code** | Power-law loss, but downstream inflection points | Similar to language with task-specific breaks |
| **Protein** | Data quality saturation limits scaling gains | AMPLIFY, ProGen3 (46B parameters) |

### Emergent Abilities Debate

The relationship between smooth loss scaling and discrete task capabilities is contested:

| Position | Claim | Key Paper |
|----------|-------|-----------|
| **Emergence is real** | 137+ abilities appear suddenly at scale (chain-of-thought reasoning, arithmetic) | Wei et al. (2022), TMLR |
| **Emergence is a mirage** | 92%+ of claimed emergent abilities arise from discontinuous metrics (Exact String Match, Multiple Choice Grade); continuous metrics show smooth improvement | Schaeffer et al. (2023), NeurIPS |
| **Current consensus** | Metric-induced discontinuities explain most "emergence," but large predictability gaps across scales may still indicate genuine capability transitions | Ongoing debate (2024–2025) |

### Broken Neural Scaling Laws (BNSL)

Caballero et al. (2023) showed that standard power laws cannot model two phenomena: **double descent** (non-monotonic loss) and **inflection points** (S-shaped task curves). They proposed a smoothly broken power law:

```
L(x) ≈ a · x^(-α₁) · (1 + (x/x_break)^((α₁-α₂)/γ))^(-γ)
```

This handles regime transitions and extrapolates with ~14% lower RMSE than simple power laws, applied across vision, language, audio, video, and alignment domains.

### Test-Time Compute Scaling (2024–2025)

A new scaling axis: for a fixed pretrained model, performance on reasoning tasks scales as a power law with inference-time compute (chain-of-thought steps, search iterations). OpenAI's o1/o3 models demonstrated this, achieving 96.1% on reasoning benchmarks through increased test-time compute. This suggests training-time scaling laws alone are insufficient to predict reasoning capability.

## Predicted Breakdown

Kaplan's own analysis predicts scaling laws must transition to a different regime beyond:

| Variable | Breakdown Point |
|----------|----------------|
| N* | ~10^12 parameters |
| D* | ~10^12 tokens |
| C* | ~10^4 PF-days |
| L* | ~1.7 nats/token |

The overfitting and compute-efficient scaling equations make contradictory predictions at this scale, signaling a regime change.

## Practical Applications

### How Labs Use Scaling Laws

1. **Proxy model grid**: Train 10-20 small models at 0.01–0.1% of final compute budget across various (N, D) splits
2. **Fit scaling parameters**: Determine a, b, α, β from the small-run loss curves
3. **Extrapolate**: Predict optimal (N*, D*) for the full compute budget
4. **Validate**: GPT-4's performance was reportedly predicted from 0.1% of its training compute

### IsoFLOP Curves

The most operationally straightforward method: fix total FLOPs C, train ~10-20 models varying the N/D split, and find the loss valley identifying N_opt. Requires actual runs but avoids parametric assumptions.

### Downstream Performance Prediction

A two-stage pipeline: C → [Scaling Law] → Pretrain Loss L → [Task Scaling Map] → Downstream Accuracy. The first stage is well-characterized; the second is task-specific and can fail for tasks with phase transitions.

## Applications to Our Work

Scaling laws inform model sizing decisions for abuse detection:
- **Data requirements**: Given a [BSM-BERT](../../areas/models/model_rnr_bsm_bert.md) model with N parameters, minimum data to avoid overfitting is D ≳ 5×10³ · N^0.74
- **Architecture selection**: The architecture independence finding validates choosing depth/width based on serving constraints (latency, memory) for [CrossBERT](term_crossbert.md)
- **Transfer expectations**: In-distribution scaling laws predict out-of-distribution performance with constant offset, supporting cross-marketplace transfer in [CrossBERT](term_crossbert.md)
- **Compute budgeting**: For fixed training budgets, scaling curves from pilot experiments can predict performance at larger model sizes before committing resources

## Questions

### Validation (Socratic)
1. The architecture independence finding ("only total N matters") was tested on *decoder-only Transformers* across a 40× width/depth range. What information is missing about *encoder-only* (BERT), *encoder-decoder* (T5), *Mixture-of-Experts* (Mixtral), and *state-space models* (Mamba)? MoE models have a total parameter count 10-100× larger than their active parameter count — does "only N matters" refer to active or total parameters? If architecture independence breaks for non-decoder-only models, what does that imply about the generality of scaling laws as a predictive framework? *(WYSIATI lens)*
2. Chinchilla's revision of Kaplan's compute-optimal allocation presents four simultaneous corrections: parameter counting, learning rate coupling, training duration, and methodology (single vs. three methods). These are presented as independent findings, but they are **confounded** — the revised training duration affects the LR schedule, which affects the parameter sensitivity. Which correction was *causally* responsible for changing the exponent from C^0.73 to C^0.50? Would fixing only the LR schedule issue have been sufficient? The Epoch AI replication (2024) found issues with Chinchilla's *own* Method 3 — does this suggest the "ground truth" allocation is still uncertain? *(Causal vs. Correlational lens)*
3. The emergent abilities debate is a textbook **Simpson's Paradox** case: aggregate metrics (Exact String Match) show discontinuous jumps at scale, while continuous metrics (token-level probability) show smooth improvement. Could this same metric-induced discontinuity affect *other* scaling law predictions in this note — for example, the downstream performance prediction pipeline (C → Loss → Accuracy)? If a downstream task uses a threshold-based metric (e.g., "success" = solving 100% of sub-steps), could smooth loss scaling mask a genuine capability gap? *(Simpson's Paradox lens)*

### Application (Taxonomic)
4. The downstream performance prediction pipeline is described as two stages: C → [Scaling Law] → Pretrain Loss L → [Task Scaling Map] → Downstream Accuracy. The note states the first stage is "well-characterized" but the second "can fail for tasks with phase transitions." Can you explain the *mechanism* of this failure? Is it because (a) the mapping from loss to accuracy is nonlinear and task-dependent, (b) multiple different loss values can produce the same accuracy, or (c) the tasks require compositional capabilities that emerge at a loss threshold not predictable from the scaling curve? What would a principled "Task Scaling Map" look like? *(Elaborative Depth lens)*
5. The predicted breakdown at N* ~ 10^12 parameters and D* ~ 10^12 tokens is where the overfitting and compute-efficient equations make "contradictory predictions." Current frontier models (GPT-4, Claude 3.5) are plausibly at or near 10^12 parameters. If we have already crossed or are approaching the breakdown point, what *new* scaling regime might emerge? Would the exponents change, would the power law break entirely, or would a fundamentally different functional form (e.g., BNSL's broken power law) become necessary? Is there any empirical evidence from frontier model training that the standard power law is already failing? *(Scale Shift lens)*
6. What if scaling laws are an artifact of the *training paradigm* (autoregressive next-token prediction on web text) rather than a fundamental property of neural networks? If we changed the training objective — e.g., from next-token prediction to energy-based modeling, or from web text to purely synthetic data with known structure — would the same power-law exponents hold? Would the architecture independence finding survive? This tests whether scaling laws describe the *model* or the *data distribution*. *(What If / Divergent lens)*

### Synthesis (Lateral)
7. [Chain of Thought](term_chain_of_thought.md) is presented as an emergent ability that smooth loss-based scaling laws *cannot predict* — it appears "suddenly" at ~100B parameters. This creates a fundamental tension: if scaling laws are the "theory of everything" for LLMs, CoT is the phenomenon that breaks the theory. Could a unified framework reconcile these? For instance, could CoT emergence be predicted by a *different* scaling variable (e.g., scaling in the number of in-context reasoning steps, or in the rank of internal representations) that is itself a power-law function of N? *(Liquid Network lens — bridging with term_chain_of_thought)*
8. Scaling laws were formalized for English language modeling, then *exapted* to vision (ViT), multimodal (CLIP), code, and protein domains — each time with the same functional form but different exponents. This is a Level 3 (paradigm) [Architectural Exaptation](term_architectural_exaptation.md): the *idea* that performance follows power laws was transferred across domains. What does the universality of the functional form imply — is there a deeper mathematical reason (e.g., information-theoretic bounds, power-law structure in natural data) why L(X) ∝ X^(-α) holds across all these domains? Or is it a coincidence of the Transformer architecture being used in all cases? *(Exaptation lens)*

## Related Terms

### Core Concepts
- [LLM](term_llm.md) — Large Language Models whose design is guided by scaling laws
- [Foundation Model](term_foundation_model.md) — Foundation models scaled according to these laws
- [Transformer](term_transformer.md) — Architecture for which scaling laws were first characterized

### Training and Optimization
- [Self-Supervised Learning](term_ssl.md) — Pre-training paradigm that benefits from scale
- [Fine-Tuning](term_fine_tuning.md) — Downstream adaptation of scaled models; transfer consistency validates the paradigm
- [Adam](term_adam.md) — Optimizer used in scaling experiments; adaptive scaling properties
- [Embedding](term_embedding.md) — Non-embedding parameter count N is the key scaling variable

### Architecture
- [BERT](term_bert.md) — Encoder-only Transformer; scaling behavior may differ from decoder-only
- [Attention Mechanism](term_attention_mechanism.md) — Paper shows attention heads have minimal independent effect on scaling
- [CrossBERT](term_crossbert.md) — Multi-entity model where scaling considerations inform architecture choices

### Related Phenomena
- [Transfer Learning](term_transfer_learning.md) — Scaling laws predict transfer performance with constant offset
- [Masked Language Model](term_mlm.md) — Pre-training objective; scaling laws derive from MLM/autoregressive loss

- **[Amdahl's Law](term_amdahls_law.md)**: Constrains how efficiently compute can be parallelized to achieve neural scaling
- **[Scalability](term_scalability.md)**: Neural scaling laws describe how model performance scales with compute, data, and parameters — an empirical counterpart to system scalability theory
## References

### Primary Sources
- Kaplan, J. et al. (2020). [Scaling Laws for Neural Language Models](../papers/lit_kaplan2020scaling.md). arXiv:2001.08361.
- Hoffmann, J. et al. (2022). Training Compute-Optimal Large Language Models (Chinchilla). NeurIPS. arXiv:2203.15556.
- Henighan, T. et al. (2020). Scaling Laws for Autoregressive Generative Modeling. arXiv:2010.14701.

### Extensions and Revisions
- Caballero, E. et al. (2023). Broken Neural Scaling Laws. ICLR. arXiv:2210.14891.
- Sardana, N. et al. (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. ICML. arXiv:2401.00448.
- Besiroglu, T. & Erdil, E. et al. (2024). Chinchilla Scaling: A Replication Attempt. arXiv:2404.10102.

### Emergent Abilities
- Wei, J. et al. (2022). Emergent Abilities of Large Language Models. TMLR. arXiv:2206.07682.
- Schaeffer, R. et al. (2023). Are Emergent Abilities of Large Language Models a Mirage? NeurIPS. arXiv:2304.15004.

### Multimodal Scaling
- Zhai, X. et al. (2022). Scaling Vision Transformers. CVPR. arXiv:2106.04560.
- Cherti, M. et al. (2023). Reproducible Scaling Laws for Contrastive Language-Image Learning. CVPR. arXiv:2212.07143.
