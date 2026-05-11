---
tags:
  - resource
  - terminology
  - deep_learning
  - model_compression
  - transfer_learning
keywords:
  - Knowledge Distillation
  - KD
  - teacher-student
  - soft targets
  - temperature scaling
  - model compression
  - dark knowledge
  - Hinton
  - response-based distillation
  - feature-based distillation
  - relation-based distillation
  - Switch Transformer distillation
topics:
  - deep learning
  - model compression
  - transfer learning
  - efficient inference
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Term: Knowledge Distillation (KD)

## Definition

**Knowledge Distillation (KD)** is a model compression and knowledge transfer technique in which a small **student** network is trained to reproduce the behavior of a larger, more capable **teacher** network (or ensemble). The student learns not only from hard labels but from the teacher's **soft predictions** — the full probability distribution over classes — which encode richer inter-class similarity structure (termed **dark knowledge**). The standard distillation loss (Hinton et al., 2015) combines a hard-label cross-entropy with a soft-label KL divergence:

$$\mathcal{L}_{\text{KD}} = (1 - \alpha) \cdot \mathcal{L}_{\text{CE}}(y, \sigma(z_s)) + \alpha \cdot T^2 \cdot D_{\text{KL}}(\sigma(z_t / T) \| \sigma(z_s / T))$$

where $z_t$ and $z_s$ are teacher and student logits, $T$ is a **temperature** hyperparameter that softens the probability distributions (typically $T \in [3, 20]$), and $\alpha$ balances the two loss terms. The $T^2$ factor compensates for the gradient magnitude reduction at high temperatures. At $T=1$, soft targets reduce to standard softmax outputs; as $T \to \infty$, the distribution approaches uniform, maximizing information transfer about inter-class relationships. Introduced conceptually by Buciluǎ et al. (2006) for model compression and formalized by Hinton, Vinyals, and Dean (2015), knowledge distillation has become a cornerstone technique enabling deployment of large models — including sparse MoE models, large language models, and ensembles — in resource-constrained production environments.

## Full Name

Knowledge Distillation (KD)

**Synonyms & Related Terms**:
- Model Distillation
- Dark Knowledge Transfer (Hinton's original framing)
- Teacher-Student Learning
- Soft Target Training
- Model Compression (broader category)

## Taxonomy of Knowledge Types

### Response-Based Knowledge (Logit Distillation)

The student mimics the teacher's **final output layer** — the soft probability distribution over classes. This is the original formulation by Hinton et al. (2015) and remains the most widely used approach due to its simplicity and task-agnosticism.

$$\mathcal{L}_{\text{response}} = D_{\text{KL}}(\sigma(z_t / T) \| \sigma(z_s / T))$$

**Strengths**: Simple to implement, no architectural constraints on student.
**Limitations**: Ignores intermediate representations; limited for tasks where final logits do not capture full teacher knowledge.

### Feature-Based Knowledge (Intermediate Representation Distillation)

The student learns to match the teacher's **intermediate feature representations** (hidden layer activations, attention maps). Pioneered by FitNets (Romero et al., 2015), which introduced hint layers — selected teacher intermediate layers that guide the student's internal representation learning.

$$\mathcal{L}_{\text{feature}} = \|f_t(x) - r(f_s(x))\|_2^2$$

where $f_t$ and $f_s$ are teacher and student intermediate features, and $r$ is a learned regressor that aligns dimensionalities when teacher and student architectures differ.

**Strengths**: Captures richer structural knowledge than logit-only distillation.
**Limitations**: Requires architectural alignment or adapter layers; choosing which layers to align is non-trivial.

### Relation-Based Knowledge (Structural Distillation)

The student learns to preserve the **relationships between data samples** or between layers as captured by the teacher. Rather than matching individual outputs or features, it matches structural patterns — e.g., pairwise similarity matrices across a mini-batch (PKT, Passalis & Tefas, 2018) or the mutual information between layers (CRD, Tian et al., 2020).

$$\mathcal{L}_{\text{relation}} = \|G_t(f_t(x_i), f_t(x_j)) - G_s(f_s(x_i), f_s(x_j))\|$$

where $G$ computes pairwise relationships (e.g., cosine similarity, Gram matrices).

**Strengths**: Architecture-agnostic; transfers structural knowledge independent of representation dimensionality.
**Limitations**: Computationally more expensive (pairwise computation); batch-size sensitive.

## Distillation Schemes

| Scheme | Description | Teacher Training | Key Property |
|--------|-------------|-----------------|--------------|
| **Offline Distillation** | Teacher is pre-trained and frozen; student learns from teacher outputs | Separate, prior | Simple, most common; teacher quality is fixed |
| **Online Distillation** | Teacher and student are trained simultaneously; they learn from each other | Joint, concurrent | No pre-trained teacher needed; mutual learning (DML, Zhang et al., 2018) |
| **Self-Distillation** | A model distills knowledge from its own deeper layers to shallower layers, or from later training epochs to earlier ones | Self-referential | Born-Again Networks (Furlanello et al., 2018); no separate teacher needed |

## Key Distillation Methods

| Method | Year | Knowledge Type | Key Innovation |
|--------|------|---------------|----------------|
| Buciluǎ et al. | 2006 | Response | Model compression via pseudo-labeled data from ensemble |
| Hinton et al. (KD) | 2015 | Response | Temperature-scaled soft targets + dark knowledge framework |
| FitNets (Romero et al.) | 2015 | Feature | Hint-based intermediate layer matching; deeper thinner students |
| Attention Transfer (Zagoruyko) | 2017 | Feature | Attention map transfer across layers |
| PKT (Passalis & Tefas) | 2018 | Relation | Probabilistic knowledge transfer via kernel similarity |
| DML (Zhang et al.) | 2018 | Response | Online mutual distillation — no pre-trained teacher |
| Born-Again (Furlanello et al.) | 2018 | Response | Self-distillation: student of same architecture surpasses teacher |
| CRD (Tian et al.) | 2020 | Relation | Contrastive representation distillation |
| TinyBERT (Jiao et al.) | 2020 | Feature + Response | BERT distillation: embedding + attention + prediction layers |
| DistilBERT (Sanh et al.) | 2019 | Response + Feature | 60% size BERT retaining 97% performance |
| Switch Transformer Distillation (Fedus et al.) | 2022 | Response | Sparse MoE → dense distillation; 30% quality gain preserved |

## MoE-to-Dense Distillation (Switch Transformer Case Study)

A critical application of knowledge distillation is compressing **sparse Mixture-of-Experts (MoE)** models into dense models for practical deployment. Fedus et al. (2022) demonstrated this in Switch Transformers:

| Configuration | Parameters | SuperGLUE | Quality Gain Preserved |
|--------------|-----------|-----------|----------------------|
| T5-Base (baseline) | 223M | 74.6 | — |
| Switch-Base (teacher, sparse) | 7.4B | 81.3 | 100% |
| Distilled T5-Base (best) | 223M | 76.6 | **30%** |

Key findings:
- **99% parameter compression** (7.4B → 223M) preserves **30% of quality gains**
- Non-expert weight initialization from the teacher is the **single most impactful** distillation technique
- Mixing soft and hard losses (0.75/0.25) outperforms either alone
- Distilled dense model requires **no MoE infrastructure** at inference time
- Paradigm: **train large sparse, deploy dense** — practical for production systems with latency constraints

This demonstrates knowledge distillation as a **deployment strategy**: leverage the superior training efficiency of sparse models while deploying a simple dense model that fits standard inference infrastructure.

## Temperature: The Critical Hyperparameter

Temperature $T$ controls the entropy of the teacher's output distribution:

| Temperature | Distribution Shape | Information Transferred | Use Case |
|------------|-------------------|----------------------|----------|
| $T = 1$ | Sharp (standard softmax) | Mostly top-class info | Baseline, no distillation benefit |
| $T \in [3, 5]$ | Moderately soft | Good inter-class similarity | Most classification tasks |
| $T \in [5, 20]$ | Very soft | Maximum dark knowledge | When teacher is highly confident |
| $T \to \infty$ | Uniform | Only ordinal ranking | Rarely useful |

The **dark knowledge** insight: a teacher that assigns probabilities [0.7, 0.2, 0.08, 0.02] to [cat, dog, car, boat] reveals that "cat is similar to dog but not to car" — information absent from the hard label. Temperature amplifies these small but informative probabilities.

## Distillation for LLMs

Knowledge distillation has become essential for making large language models deployable:

| Source Model | Distilled Model | Compression | Quality Retention |
|-------------|----------------|-------------|-------------------|
| BERT-Base (110M) | DistilBERT (66M) | 40% smaller | 97% on GLUE |
| BERT-Base (110M) | TinyBERT (14.5M) | 87% smaller | 96.8% on GLUE |
| GPT-3 (175B) | Various student LLMs | 10-100x smaller | Task-dependent |
| Switch-Base (7.4B sparse) | T5-Base (223M dense) | 99% fewer params | 30% of gains |

Challenges specific to LLM distillation:
- **Autoregressive distillation**: Sequence generation requires word-level or sequence-level KD
- **Capacity gap**: Large teacher-student capacity gaps degrade distillation effectiveness (TAKD introduces teaching assistants as intermediaries)
- **Distribution mismatch**: Student's autoregressive errors compound during generation (exposure bias)
- **Privacy concerns**: Teacher outputs may leak training data

## Knowledge Distillation at Amazon / BRP

### Potential Applications
- **Model compression for real-time inference**: Distill large BERT/Transformer-based abuse detection models into compact students that meet <10ms AMES latency requirements
- **MoE deployment**: Train large sparse MoE models (e.g., Pop-MoE, Clickstream MoE) and distill into dense models for inference, following the Switch Transformer paradigm
- **Cross-domain transfer**: Use distillation to transfer knowledge from data-rich abuse domains (US DNR) to data-scarce domains (new marketplace launches) without sharing raw data
- **Ensemble compression**: Distill ensemble of XGBoost + deep learning models into a single unified model, reducing operational complexity

### When to Use Knowledge Distillation

| Scenario | Recommendation | Reason |
|----------|---------------|--------|
| Large model, strict latency budget | Distill | Compress teacher to meet inference SLA |
| MoE model, no MoE inference infra | Distill | Dense student needs only standard infrastructure |
| Ensemble in production | Distill | Single model is cheaper to serve and maintain |
| Small dataset, no large teacher | Skip | Distillation requires a strong teacher first |
| Student architecture very different from teacher | Use feature-based KD | Response-based may not transfer well |
| Privacy-constrained data | Distill with care | Teacher soft labels may leak information |

## Related Terms

- **[Mixture of Experts (MoE)](term_moe.md)**: MoE models are a primary distillation source — large sparse MoE models are distilled into dense models for deployment (Fedus et al., 2022)
- **[Scaling Law](term_scaling_law.md)**: Knowledge distillation enables practical use of scaling law improvements — train at scale, deploy compressed
- **[Conditional Computation](term_conditional_computation.md)**: The broader paradigm whose inference cost problem is partly solved by distilling into dense models
- **[Transfer Learning](term_transfer_learning.md)**: Knowledge distillation is a form of transfer learning from teacher to student; both transfer learned representations
- **[Embedding](term_embedding.md)**: Feature-based distillation transfers embedding-level representations from teacher to student
- **[Transformer](term_transformer.md)**: Primary architecture for modern distillation (DistilBERT, TinyBERT, Switch distillation)
- **[Multi-Task Learning](term_mtl.md)**: MTL and distillation can be combined — multi-task teacher distilling into specialized students

## Vault Sources

- [Switch Transformers — Model Architecture (Fedus et al., 2022)](../papers/paper_fedus2022switch_model.md) — Describes the sparse-to-dense distillation methodology and non-expert weight initialization
- [Switch Transformers — Experimental Results (Fedus et al., 2022)](../papers/paper_fedus2022switch_exp_result.md) — Distillation results: 7.4B sparse → 223M dense, 30% quality gain preservation, soft/hard loss mixing
- [Outrageously Large Neural Networks — Review (Shazeer et al., 2017)](../papers/review_shazeer2017outrageously.md) — Foundational MoE work that motivated distillation as a deployment strategy for sparse models

## References

- Hinton, G., Vinyals, O., & Dean, J. (2015). "Distilling the Knowledge in a Neural Network." arXiv:1503.02531 — Foundational KD paper; introduced temperature-scaled soft targets and dark knowledge
- Buciluǎ, C., Caruana, R., & Niculescu-Mizil, A. (2006). "Model Compression." KDD — Original model compression via pseudo-labeling
- Romero, A., et al. (2015). "FitNets: Hints for Thin Deep Nets." ICLR — Feature-based distillation via hint layers
- Fedus, W., Zoph, B., & Shazeer, N. (2022). "Switch Transformers: Scaling to Trillion Parameter Models." JMLR — MoE-to-dense distillation preserving 30% of sparse gains
- Sanh, V., et al. (2019). "DistilBERT, a Distilled Version of BERT." arXiv — 40% compression retaining 97% GLUE performance
- Jiao, X., et al. (2020). "TinyBERT: Distilling BERT for Natural Language Understanding." EMNLP — Multi-layer distillation (embedding + attention + prediction)
- Gou, J., et al. (2021). "Knowledge Distillation: A Survey." IJCV — Comprehensive survey of KD taxonomy and methods
- Tian, Y., et al. (2020). "Contrastive Representation Distillation." ICLR — Relation-based KD via contrastive objectives

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Knowledge Distillation |
| **Key Innovation** | Transfer dark knowledge via temperature-scaled soft targets from teacher to student |
| **Core Mechanism** | Student minimizes KL divergence to teacher's softened output distribution + hard-label cross-entropy |
| **Knowledge Types** | Response-based (logits), Feature-based (intermediate layers), Relation-based (structural) |
| **Distillation Schemes** | Offline (frozen teacher), Online (mutual learning), Self-distillation |
| **Critical Hyperparameter** | Temperature $T$ — controls softness of teacher distribution ($T \in [3, 20]$ typical) |
| **MoE Application** | Switch Transformer: 7.4B sparse → 223M dense, 30% quality preserved (Fedus et al., 2022) |
| **LLM Application** | DistilBERT (97% GLUE at 60% size), TinyBERT (96.8% at 13% size) |
| **Deployment Paradigm** | Train large (sparse/ensemble), deploy small (dense/single) |
| **Foundational Paper** | Hinton, Vinyals, Dean (2015) — "Distilling the Knowledge in a Neural Network" |

---

**Last Updated**: March 15, 2026
**Status**: Active
