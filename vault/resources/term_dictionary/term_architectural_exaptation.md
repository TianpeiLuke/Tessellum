---
tags:
  - resource
  - terminology
  - deep_learning
  - architecture
  - innovation
  - meta_science
keywords:
  - architectural exaptation
  - component reuse
  - innovation by integration
  - borrowed techniques
  - LLaMA trio
  - modular architecture
  - evolutionary analogy
  - exaptation
  - adjacent possible
  - combinatorial innovation
topics:
  - Deep Learning
  - Architecture Design
  - Innovation Patterns
  - Meta-Science
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Architectural Exaptation

## Definition

**Architectural Exaptation** is a pattern in deep learning where components originally developed for one architectural context are repurposed in a different context, often producing superior results through novel combination rather than individual invention. The term borrows from evolutionary biology — "exaptation" (Gould & Vrba, 1982) describes a trait evolved for one function that is co-opted for a different function (e.g., feathers evolved for thermoregulation, exapted for flight). In deep learning, architectural exaptation is the dominant mode of progress: most "innovations" are integrations of existing components into new configurations, not inventions of new primitives. The canonical example is [LLaMA](../papers/lit_touvron2023llama.md) (Touvron et al., 2023), which combined [RMSNorm](term_rmsnorm.md) (from GPT-3's pre-normalization), [SwiGLU](term_swiglu.md) (from PaLM's FFN), and [RoPE](term_rope.md) (from GPTNeo's position encoding) — none invented for LLaMA, yet their combination became the de facto standard for all subsequent open foundation models.

## Full Name

**Architectural Exaptation** (also: Component Exaptation, Architectural Recombination)

**Also Known As**: Borrowed techniques, modular innovation, integration-driven progress, combinatorial architecture design

## Biological Origin: Exaptation

The concept was introduced by paleontologists Stephen Jay Gould and Elisabeth Vrba (1982) to distinguish two evolutionary processes:

| Mechanism | Definition | Biological Example | Architectural Example |
|-----------|-----------|-------------------|----------------------|
| **Adaptation** | Trait shaped by natural selection for its *current* function | Eyes evolved for seeing | Attention mechanism invented for sequence-to-sequence translation |
| **Exaptation** | Trait shaped for one function, *co-opted* for a different function | Feathers: thermoregulation → flight | Attention: NMT → vision (ViT), protein folding (AlphaFold) |

Steven Johnson popularized exaptation as an innovation pattern in *Where Good Ideas Come From* (2010), arguing that most transformative innovations are exaptations — old ideas repurposed in new contexts — rather than purely novel inventions. The deep learning ecosystem is a textbook liquid network for exaptation: ideas from different subfields (NLP, vision, optimization, hardware) collide and recombine.

## The LLaMA Trio: Canonical Example

[LLaMA](../papers/lit_touvron2023llama.md)'s architecture is a pure exaptation — every key component was borrowed:

| Component | Original Context | Year | Original Purpose | Exapted in LLaMA |
|-----------|-----------------|------|-----------------|------------------|
| [RMSNorm](term_rmsnorm.md) | Zhang & Sennrich (2019) | 2019 | Simplify LayerNorm for NMT | Pre-normalization for training stability at scale |
| Pre-normalization | GPT-3 (Brown et al., 2020) | 2020 | Stabilize very deep Transformers | Combined with RMSNorm (GPT-3 used LayerNorm) |
| [SwiGLU](term_swiglu.md) | Shazeer (2020), used in PaLM | 2020 | Improve FFN expressiveness | Replace standard FFN activation |
| [RoPE](term_rope.md) | Su et al. (2021), used in GPTNeo | 2021 | Relative position via rotation | Position encoding for all model sizes |
| BPE tokenizer | SentencePiece (Kudo, 2018) | 2018 | Subword tokenization for NMT | Tokenization with digit splitting |
| AdamW optimizer | Loshchilov & Hutter (2019) | 2019 | Decoupled weight decay | Training optimization |

**What LLaMA invented**: Nothing. **What LLaMA created**: The standard foundation model recipe that Llama-2, Llama-3, Mistral, Gemma, Qwen, and virtually all post-2023 models adopted.

## Exaptation Taxonomy in Deep Learning

### Level 1: Component Exaptation (most common)

Individual modules borrowed from one architecture to another:

| Component | Origin → Exapted Context | Impact |
|-----------|-------------------------|--------|
| **Attention mechanism** | NMT (Bahdanau, 2014) → Vision (ViT, 2020), Protein (AlphaFold, 2021), Audio (Whisper, 2022) | Became universal sequence modeling primitive |
| **Skip connections** | ResNet (He, 2015) → Transformer residual connections (Vaswani, 2017) | Enabled arbitrarily deep architectures |
| **Dropout** | Srivastava et al. (2014) → Standard in every architecture | Became implicit architectural component |
| **Layer normalization** | Ba et al. (2016) → Pre-norm Transformers → RMSNorm simplification | Progressively simplified through exaptation |
| **Gating mechanisms** | LSTM (Hochreiter, 1997) → GLU (Dauphin, 2017) → SwiGLU (Shazeer, 2020) | Gate concept migrated from RNN to FFN |

### Level 2: Pattern Exaptation

Design patterns — not individual components — transferred across domains:

| Pattern | Origin → Exapted Context |
|---------|-------------------------|
| **Encoder-decoder** | NMT → Image segmentation (U-Net) → Diffusion models |
| **Pre-train then fine-tune** | NLP (BERT, GPT-2) → Vision (MAE) → Protein (ESM) → Tabular (TabPFN) |
| **Tokenize everything** | NLP subword tokenization → Image patches (ViT) → Audio spectrograms |
| **Autoregressive generation** | Language modeling → Image generation (DALL-E) → Code (Codex) |

### Level 3: Paradigm Exaptation (rarest, highest impact)

Entire problem-solving paradigms transferred:

| Paradigm | Origin → Exapted Context |
|----------|-------------------------|
| **Self-supervised learning** | NLP (masked LM) → Vision (MAE, DINO) → Multimodal (CLIP) |
| **Scaling laws** | Language (Kaplan, 2020) → Vision, multimodal, code (Henighan, 2020) |
| **RLHF** | Game playing (Atari) → Language alignment (InstructGPT) → Reasoning (o1) |

## Why Exaptation Dominates Invention

### The Adjacent Possible Constraint

Innovation is bounded by the **adjacent possible** (Johnson, 2010) — what's achievable given current components. Deep learning's modular architecture creates a combinatorial explosion of possible configurations:

```
Available components:  ~20 normalization methods
                     × ~15 activation functions
                     × ~10 position encoding methods
                     × ~5 attention variants
                     × ~10 optimizer choices
                     = ~150,000 possible configurations
```

The probability that the optimal configuration uses all-new components is vanishingly small. Integration (exaptation) has higher expected value than invention.

### Selection Pressure: Why Specific Combinations Win

Not all exaptations succeed. The LLaMA trio won because each component addressed a specific bottleneck at scale:

| Bottleneck | Component | Why It Won |
|-----------|-----------|-----------|
| Training instability at depth | RMSNorm pre-normalization | Simpler than LayerNorm, equally stable, ~10% faster |
| FFN expressiveness | SwiGLU | Best empirical performance among activation variants (Shazeer's ablation) |
| Position generalization | RoPE | Relative encoding via absolute rotation; extensible to longer contexts |

The combination was validated at scale first by PaLM (SwiGLU + RoPE), then LLaMA (RMSNorm + SwiGLU + RoPE). LLaMA's open release allowed rapid community verification, creating a lock-in effect through the open-source ecosystem.

### Implications for Research Strategy

| Strategy | Description | Expected Value | Risk |
|----------|-------------|---------------|------|
| **Pure invention** | Design novel components from scratch | High if successful, but low probability | High (most fail) |
| **Exaptation** | Borrow proven components into new contexts | Moderate, high probability | Low (components pre-validated) |
| **Integration** | Combine known components optimally | Moderate-high, very high probability | Very low |
| **Ablation archaeology** | Mine published ablations for winning variants | Moderate, high probability | Low (data exists) |

The LLaMA lesson: **integration papers can have higher impact than invention papers** — LLaMA (18,793 citations) outperforms most individual component papers.

## Applications to Our Work

- **Model architecture selection**: When designing abuse detection models, prefer exaptation of proven components (e.g., pre-trained embeddings, attention patterns from NLP) over novel architectures — lower risk, faster iteration
- **Cross-domain transfer**: Techniques from NLP abuse detection (BERT classifiers, CoT reasoning) can be exapted into vision abuse detection (document fraud, image manipulation) — the pattern transfer is the innovation
- **Innovation audit**: When evaluating ML research proposals, distinguish between Level 1 exaptation (low novelty, high reliability), Level 2 pattern exaptation (moderate novelty), and genuine invention (high novelty, high risk)

## Questions

### Validation (Socratic)
1. The note claims "most deep learning innovation is integration, not invention," but this could be **survivorship bias** — we remember successful exaptations (LLaMA trio) and forget the many combinations that failed silently. What is the base rate of exaptation failure? For every successful component borrowing, how many attempted combinations produced no improvement or degraded performance? What information about failed exaptations is missing from this analysis? *(WYSIATI lens)*
2. If [LLaMA](../papers/lit_touvron2023llama.md) had NOT been released as open weights, would the deep learning community still have converged on the same RMSNorm + SwiGLU + RoPE combination as the standard recipe? Was the component combination the critical variable, or was **open release** the actual cause of lock-in — making this a story about ecosystem dynamics rather than architectural merit? *(Counterfactual lens)*

### Application (Taxonomic)
3. What if we deliberately pursued **anti-exaptation** — building a foundation model entirely from novel, never-before-combined components (new normalization, new activation, new position encoding, new attention)? Would the resulting model likely underperform the exapted standard, and if so, what does that reveal about whether the LLaMA trio is a *local optimum* or close to a *global optimum* in architecture space? *(What If / Divergent lens)*
4. The note presents a 3-level taxonomy (component → pattern → paradigm exaptation). Can you explain the *mechanism* by which the LLaMA trio combination is superior — does each component contribute *independently* (additive), or are there *interaction effects* where RMSNorm + SwiGLU together are better than the sum of their individual improvements? What ablation evidence exists? *(Elaborative Depth lens)*

### Synthesis (Lateral)
5. [Chain of Thought](term_chain_of_thought.md) is itself a paradigm exaptation — human step-by-step reasoning exapted into LLM prompting. Could the exaptation lens be applied to **prompt engineering** as a field? Are techniques like few-shot prompting, role-playing, and tree-of-thought all exaptations from pedagogy, theater, and search algorithms respectively? -> Follow-up: [term_prompt_exaptation](term_prompt_exaptation.md) *(Exaptation lens — applied recursively to the concept itself)*
6. An economist would frame this note's 150,000-configuration space as an **efficient market for architectural components**, where successful exaptations are "arbitrage" — exploiting underpriced components from one domain in another. What would market failure look like in this analogy? Are there components sitting in niche domains (e.g., [diffusion models](term_diffusion_model.md), [graph networks](term_gnn.md)) that are systematically underexplored for exaptation into LLM architectures? *(Question Storming lens — economist's perspective)*

## Related Terms

### Core Architecture
- [Transformer](term_transformer.md) — The architecture whose modularity enables component-level exaptation
- [RMSNorm](term_rmsnorm.md) — Component exapted from GPT-3 into LLaMA's pre-normalization
- [SwiGLU](term_swiglu.md) — Activation function exapted from PaLM into LLaMA's FFN
- [RoPE](term_rope.md) — Position encoding exapted from GPTNeo into LLaMA
- [Attention Mechanism](term_attention_mechanism.md) — The most widely exapted component in deep learning (NMT → vision → protein → audio)
- [Layer Normalization](term_layer_normalization.md) — Normalization component with a rich exaptation history

### Key Papers
- [LLaMA (Touvron et al., 2023)](../papers/lit_touvron2023llama.md) — Canonical example of pure exaptation producing a field-defining architecture
- [Attention Is All You Need (Vaswani et al., 2017)](../papers/lit_vaswani2017attention.md) — Transformer itself exapted attention from Bahdanau's NMT into a standalone architecture
- [GPT-3 (Brown et al., 2020)](../papers/lit_brown2020language.md) — Introduced pre-normalization pattern exapted by LLaMA

### Innovation Framework
- [Scaling Law](term_scaling_law.md) — Paradigm exaptation from language to vision, multimodal, and code
- [Inference Scaling Law](term_inference_scaling_law.md) — Co-spawned concept from the same LLaMA analysis
- [Foundation Model](term_foundation_model.md) — The pre-train-then-fine-tune pattern is itself a Level 2 exaptation from NLP to all domains

## References

### Biological Origin
- Gould, S.J. & Vrba, E.S. (1982). Exaptation — A Missing Term in the Science of Form. *Paleobiology*, 8(1), 4-15.

### Innovation Theory
- Johnson, S. (2010). *Where Good Ideas Come From: The Natural History of Innovation*. Riverhead Books.
- Arthur, W.B. (2009). *The Nature of Technology: What It Is and How It Evolves*. Free Press.

### Deep Learning Architecture
- Touvron, H. et al. (2023). [LLaMA: Open and Efficient Foundation Language Models](../papers/lit_touvron2023llama.md). arXiv:2302.13971.
- Shazeer, N. (2020). GLU Variants Improve Transformer. arXiv:2002.05202.
- Su, J. et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding. arXiv:2104.09864.
- Zhang, B. & Sennrich, R. (2019). Root Mean Square Layer Normalization. NeurIPS. arXiv:1910.07467.
- Source: [Digest: Where Good Ideas Come From](../digest/digest_good_ideas_johnson.md) — Johnson's exaptation framework: repurposing components from one domain to another
