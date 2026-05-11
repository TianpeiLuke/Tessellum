---
tags:
  - resource
  - terminology
  - machine_learning
  - transfer_learning
  - deep_learning
keywords:
  - fine-tuning
  - fine tuning
  - transfer learning
  - pre-train then fine-tune
  - domain adaptation
  - full fine-tuning
  - parameter-efficient fine-tuning
  - PEFT
  - LoRA
  - catastrophic forgetting
  - instruction tuning
  - RLHF
topics:
  - Machine Learning
  - Transfer Learning
  - Model Adaptation
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Fine-Tuning

## Definition

**Fine-Tuning** is the process of adapting a pre-trained model to a specific downstream task by continuing training on task-specific labeled data, typically with a small learning rate. In the BERT paradigm (Devlin et al., 2019), fine-tuning adds a minimal task-specific output layer on top of the pre-trained encoder and updates all parameters end-to-end. Fine-tuning is the default transfer learning strategy for NLP since 2019, replacing the prior feature-based approach (ELMo). Modern variants include parameter-efficient fine-tuning (PEFT), instruction tuning, and RLHF for aligning LLMs.

## Full Name

**Fine-Tuning** (also: fine tuning, finetuning)

**Also Known As**: Transfer learning (colloquially), domain adaptation (when target domain differs), task adaptation

## Full Fine-Tuning Procedure (BERT-Style)

### Steps

1. **Add task-specific head**: Attach a linear classification layer on top of the `[CLS]` representation (or token-level heads for NER/QA)
2. **Initialize from pre-trained weights**: Load all encoder parameters from the MLM-pre-trained checkpoint
3. **Train end-to-end**: Update all parameters (encoder + head) on task-specific labeled data

### Hyperparameters

| Parameter | Typical Range | Rationale |
|-----------|--------------|-----------|
| **Learning rate** | 2e-5 to 5e-5 | Small LR preserves pre-trained representations; too high causes catastrophic forgetting |
| **Epochs** | 2–4 | Few epochs prevent overfitting on small datasets |
| **Batch size** | 16 or 32 | Standard; larger batches may require LR scaling |
| **Warmup** | 6–10% of steps | Gradual warmup stabilizes early training |
| **Weight decay** | 0.01 | Regularization to prevent overfitting |
| **Max sequence length** | 128–512 | Task-dependent; shorter is faster |

### Task-Specific Output Layers

| Task Type | Output Layer | Example |
|-----------|-------------|---------|
| Sentence classification | Linear on `[CLS]` → softmax | Abuse detection, sentiment |
| Sentence pair | Linear on `[CLS]` → softmax | NLI, paraphrase detection |
| Token classification | Linear on each token → softmax | NER, POS tagging |
| Span extraction | Linear on each token → start/end logits | Question answering |

## Full Fine-Tuning vs. Feature-Based Transfer

| Dimension | Full Fine-Tuning | Feature-Based (Frozen) |
|-----------|-----------------|----------------------|
| **Parameters updated** | All (encoder + head) | Only the task head |
| **Accuracy** | Generally higher | Slightly lower (but competitive) |
| **Compute** | Higher (backprop through full model) | Lower (no encoder gradients) |
| **Overfitting risk** | Higher on small datasets | Lower (fewer trainable params) |
| **Multi-task** | Requires separate model per task | One frozen encoder, multiple heads |
| **BERT NER example** | F1 = 92.8 (fine-tuned) | F1 = 96.1 (last 4 layers concatenated) |

**When to use which**:
- **Full fine-tuning**: When you have sufficient task data (>1K examples) and need maximum accuracy
- **Feature-based**: When serving multiple tasks from one model, or when compute is constrained
- **PEFT**: When you want near-full-fine-tuning accuracy with feature-based efficiency

## Parameter-Efficient Fine-Tuning (PEFT)

PEFT methods update only a small fraction of parameters, dramatically reducing compute and storage while maintaining near-full-fine-tuning accuracy.

| Method | Paper | Trainable Params | Mechanism | Inference Overhead |
|--------|-------|-----------------|-----------|-------------------|
| **LoRA** | Hu et al., 2021 | 0.1–1% | Low-rank matrices $\Delta W = BA$ added to Q/K/V projections | **None** (merged at inference) |
| **QLoRA** | Dettmers et al., 2023 | 0.1–1% | 4-bit quantized base model + LoRA adapters | Quantization overhead |
| **Adapters** | Houlsby et al., 2019 | 3–8% | Bottleneck MLP modules inserted inside each Transformer layer | ~7% latency increase |
| **Prefix Tuning** | Li & Liang, 2021 | 0.1% | Trainable prefix vectors prepended to K/V at every layer | Slightly longer sequences |
| **Prompt Tuning** | Lester et al., 2021 | <0.01% | Trainable soft tokens at input only | Slightly longer input |
| **BitFit** | Ben Zaken et al., 2022 | ~0.08% | Only bias terms are trainable | **None** |

**LoRA** is the most widely adopted PEFT method. It decomposes weight updates as $W' = W + BA$ where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times d}$, and $r \ll d$ (typically $r = 4$–$64$). At inference, $BA$ is merged into $W$, adding zero latency.

## Instruction Fine-Tuning and Alignment

For LLMs, fine-tuning has evolved into a multi-stage pipeline:

| Stage | Method | Input | Goal |
|-------|--------|-------|------|
| 1. **Pre-training** | SSL (autoregressive) | Unlabeled text corpus | Learn language |
| 2. **SFT** (Supervised Fine-Tuning) | Standard fine-tuning | Instruction-response pairs | Follow instructions |
| 3. **RLHF** | Reinforcement learning from human feedback | Human preference rankings | Align with human values |
| 4. **DPO** (alternative to RLHF) | Direct preference optimization | Preference pairs | Align without RL complexity |

**RLHF** (Ouyang et al., 2022): Train a reward model on human preference rankings, then optimize the policy (LLM) to maximize reward while staying close to the SFT model via KL divergence constraint.

**DPO** (Rafailov et al., 2023): Eliminates the reward model entirely by reparameterizing the RLHF objective directly in terms of the policy. Simpler, more stable, increasingly preferred.

## Catastrophic Forgetting

**Definition**: The tendency of a neural network to abruptly lose previously learned knowledge when fine-tuned on new data. The new task's gradients overwrite the pre-trained weights that encoded general knowledge.

**Mitigation strategies**:

| Strategy | Mechanism |
|----------|-----------|
| **Small learning rate** | Limits the magnitude of weight changes |
| **PEFT** (LoRA, adapters) | Freezes most parameters, limiting forgetting by design |
| **Elastic Weight Consolidation (EWC)** | Penalizes changes to parameters important for prior tasks (via Fisher information) |
| **Gradual unfreezing** | Unfreeze layers progressively from top to bottom (ULMFiT, Howard & Ruder, 2018) |
| **Layer-wise LR decay** | Lower LR for earlier layers (preserve low-level features), higher for later layers |
| **Rehearsal/replay** | Mix task-specific data with a sample of pre-training data |

## Best Practices

| Practice | Description |
|----------|-------------|
| **Linear warmup + cosine decay** | Ramp LR from 0 to peak over warmup steps, then decay smoothly |
| **Layer-wise LR decay** | Multiply LR by $\eta^{L-l}$ for layer $l$ (e.g., $\eta = 0.95$); lower layers get smaller updates |
| **Gradual unfreezing** | Start by training only the head, then progressively unfreeze layers (ULMFiT) |
| **Early stopping** | Monitor validation loss; stop when it increases for N consecutive evaluations |
| **Mixed precision** | Use FP16/BF16 for faster training with minimal accuracy loss |
| **Gradient clipping** | Clip gradients to max norm (1.0) to prevent training instability |

## Fine-Tuning vs. Prompting vs. In-Context Learning

| Method | Parameters Updated | Data Required | Cost | Best For |
|--------|-------------------|---------------|------|----------|
| **Zero-shot prompting** | 0 | 0 | Lowest | Quick prototyping, broad tasks |
| **Few-shot ICL** | 0 | 3–50 examples | Low | Tasks with few labeled examples |
| **Prompt tuning** | <0.01% | 100+ | Low-Medium | Task adaptation at scale |
| **LoRA/PEFT** | 0.1–1% | 1K+ | Medium | Production models needing high accuracy |
| **Full fine-tuning** | 100% | 1K–100K+ | High | Maximum accuracy, specialized domains |

**Rule of thumb** (Mosbach et al., 2024): ~1,000–6,000 labeled examples are needed for fine-tuning to outperform few-shot in-context learning on most tasks.

## Applications to Our Work

- **BSM-BERT models** ([RnR BSM BERT](../../areas/models/model_rnr_bsm_bert.md), [AtoZ BSM BERT](../../areas/models/model_atoz_bsm_bert.md)) follow the canonical BERT fine-tuning procedure: add a linear layer on `[CLS]`, fine-tune with LR=2e-5 for 3 epochs on labeled abuse data.
- **[CrossBERT](term_crossbert.md)** fine-tunes BERT for cross-marketplace risk transfer.
- **[Abuse Polygraph](term_abuse_polygraph.md)** fine-tunes XLM-RoBERTa for deception detection in customer chats.
- PEFT methods (LoRA) could enable rapid adaptation of a single base BERT model to multiple abuse vectors without maintaining separate full models.

## Related Terms

### Core Concepts
- [Transfer Learning](term_transfer_learning.md) — Fine-tuning is the dominant transfer strategy since BERT
- [Self-Supervised Learning](term_ssl.md) — Pre-training stage that produces the model to be fine-tuned
- [Masked Language Model](term_mlm.md) — Pre-training objective for BERT (before fine-tuning)

### Parameter-Efficient Methods
- [PEFT](term_peft.md) — Parameter-efficient fine-tuning (umbrella term)
- [LoRA](term_lora.md) — Low-Rank Adaptation, most popular PEFT method

### Models
- [BERT](term_bert.md) — Established the pre-train/fine-tune paradigm for NLP
- [Transformer](term_transformer.md) — Architecture underlying fine-tuned models
- [LLM](term_llm.md) — Fine-tuned via SFT/RLHF/DPO for instruction following
- [Foundation Model](term_foundation_model.md) — Pre-trained models designed for fine-tuning

### Related Techniques
- [Meta-Learning](term_meta_learning.md) — "Learning to learn" — can be seen as learning a good initialization for fine-tuning

## References

- Devlin, J. et al. (2019). [BERT: Pre-training of Deep Bidirectional Transformers](../papers/lit_devlin2019bert.md). NAACL.
- Howard, J. & Ruder, S. (2018). Universal Language Model Fine-tuning for Text Classification (ULMFiT). ACL. arXiv:1801.06146.
- Hu, E. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. arXiv:2106.09685.
- Houlsby, N. et al. (2019). Parameter-Efficient Transfer Learning for NLP (Adapters). ICML.
- Li, X.L. & Liang, P. (2021). Prefix-Tuning: Optimizing Continuous Prompts for Generation. ACL.
- Lester, B. et al. (2021). The Power of Scale for Parameter-Efficient Prompt Tuning. EMNLP.
- Dettmers, T. et al. (2023). QLoRA: Efficient Finetuning of Quantized Language Models. NeurIPS. arXiv:2305.14314.
- Ouyang, L. et al. (2022). Training Language Models to Follow Instructions with Human Feedback (InstructGPT). NeurIPS.
- Rafailov, R. et al. (2023). Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS. arXiv:2305.18290.
- Xu, L. et al. (2024). A Survey on Parameter-Efficient Fine-Tuning for Large Models. arXiv:2403.14608.
