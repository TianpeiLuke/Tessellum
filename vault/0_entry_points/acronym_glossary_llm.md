---
tags:
 - entry_point
 - index
 - navigation
 - quick_reference
 - glossary
 - machine_learning
 - large_language_models
 - generative_ai
keywords:
 - large language models
 - LLM
 - generative AI
 - NLP
 - BERT
 - transformer
 - RAG
 - VLM
 - fine-tuning
 - prompt engineering
topics:
 - large language models
 - generative AI
 - NLP systems
 - foundation models
language: markdown
date of note: 2026-05-10
status: active
building_block: navigation
---

# Large Language Models (LLM) Glossary

**Purpose**: Quick reference for Large Language Models, generative AI systems, NLP architectures, and related techniques used in anomaly / anomaly operations.

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md) | [← ML Algorithms](acronym_glossary_ml.md)

---

## Foundation Models & LLM Families

### Foundation Model
**Full Name**: Foundation Model
**Description**: Large-scale pre-trained model adaptable to many downstream tasks through fine-tuning or prompting. Examples: GPT-4 (language), CLIP (vision), **TabPFN (tabular)**. Key characteristics: trained on massive data, general-purpose, emergent capabilities, few-shot learning. **Relevance to domain**: TabPFN outperforms XGBoost on small datasets (<10K samples) in 2.8s vs 4h tuning - potential for rapid response to new patterns with limited labeled data.
**Documentation**: [Foundation Model Term](../resources/term_dictionary/term_foundation_model.md)
**Examples**: GPT-4, Claude (language); CLIP, SAM (vision); TabPFN (tabular); AlphaFold (biology)
**Key Capabilities**: Transfer learning, few-shot learning, emergent abilities, general-purpose adaptation
**domain Potential**: TabPFN for small-data anomaly detection, rapid adaptation to new patterns
**Related**: [LLM](#llm---large-language-models), [TabPFN Paper](../resources/papers/lit_hollmann2025accurate.md), [Transfer Learning](../resources/term_dictionary/term_transfer_learning.md), [Meta-Learning](../resources/term_dictionary/term_meta_learning.md)

### Claude - Anthropic's Large Language Model Family
**Full Name**: Claude (Anthropic's Large Language Model Family)
**Documentation**: [Claude Term](../resources/term_dictionary/term_claude.md)
**Model Variants**: Haiku (fast), Sonnet (balanced), Opus (sophisticated), Instant (cost-effective)
**Related**: [LLM](#llm---large-language-models), [](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting), [RAG](#rag---retrieval-augmented-generation)

### GenAI - Generative Artificial Intelligence
**Full Name**: Generative Artificial Intelligence
**Documentation**: [GenAI Term](../resources/term_dictionary/term_genai.md)
**Key Technologies**: LLMs (transformer-based), VLMs (vision+language), multimodal systems
**Infrastructure**: AWS Bedrock, SageMaker,, Harmony
**Status**: ✅ Active - core technology for domain automation
**Related**: [LLM](#llm---large-language-models), [VLM](#vlm---vision-language-model), [RAG](#rag---retrieval-augmented-generation), [](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### Phi - Microsoft Small Language Model Family
**Full Name**: Phi (Microsoft Small Language Model Family)
**Documentation**: [Phi Term](../resources/term_dictionary/term_phi.md)
**Key Papers**: Gunasekar et al. (2023, arXiv:2306.11644), Abdin et al. (2024, arXiv:2404.14219, arXiv:2412.08905)
**Related**: [LLM](#llm---large-language-models), [Foundation Model](#foundation-model), [Scaling Law](#scaling-law), [MoE](acronym_glossary_ml.md#moe---mixture-of-experts), [Knowledge Distillation](../resources/term_dictionary/term_knowledge_distillation.md)

### CRFM - Customer Representation Foundation Model
**Full Name**: Customer Representation Foundation Model
**Description**: Lightweight transformer (87K params) converting shopping history → 64D behavioral embeddings. Production-friendly 4ms latency. Impact: <value>+ OPS growth. Uses: P13N, Ads, customer behavior analysis.
**Documentation**: [CRFM Term](../resources/term_dictionary/term_crfm.md)
**Team**: Stores Foundational AI (SFAI) M5
**Launch**: November 2025
**Related**: [](#lila---lite-language-model-for-behavior-understanding), [LLM](#llm---large-language-models)

### Scaling Law
**Full Name**: Scaling Law (Neural Scaling Law, Power-Law Scaling)
**Description**: Empirical power-law relationships describing how neural network loss scales with model size (N), dataset size (D), and training compute (C). Kaplan et al. (2020) showed L(N) ∝ N^{-0.076} across 7+ orders of magnitude. Chinchilla (Hoffmann et al., 2022) revised compute-optimal allocation to N ∝ C^{0.50}, D ∝ C^{0.50} (~20 tokens/param), overturning Kaplan's model-size-heavy recommendation. Extended to vision, multimodal, and code. Architecture details (depth/width) have minimal effect — only total non-embedding parameter count N matters. Practical use: labs train small proxy models, fit scaling curves, then extrapolate to predict optimal model size for full compute budget.
**Documentation**: [Scaling Law Term](../resources/term_dictionary/term_scaling_law.md)
**Key Papers**: Kaplan et al. (2020, arXiv:2001.08361), Hoffmann et al. (2022, Chinchilla), Caballero et al. (2023, BNSL)
**Key Equations**: L(N) = (N_c/N)^α_N; L(N,D) joint scaling; B_crit(L) = B*/L^(1/α_B)
**domain Relevance**: Informs model sizing for BSM-BERT, data requirements (D ≳ 5×10³ · N^0.74), architecture choices for CrossBERT
**Related**: [LLM](#llm---large-language-models), [Foundation Model](#foundation-model), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Fine-Tuning](../resources/term_dictionary/term_fine_tuning.md), [SSL](acronym_glossary_ml.md#ssl---self-supervised-learning)

### Inference Scaling Law
**Full Name**: Inference Scaling Law (Inference-Aware Scaling, Deployment-Optimal Scaling)
**Description**: Extension of neural scaling laws that optimizes for total deployment cost (training + inference) rather than training cost alone. Standard compute-optimal scaling (Chinchilla) prescribes ~20 tokens/parameter, minimizing training FLOPs. But when serving at scale, inference cost (proportional to model size N per query) dominates: Total Cost = 6ND + 2N × R × T. At high inference demand, it is cheaper to train smaller models on far more data — LLaMA-3.1 8B trained on 15T tokens (~1,875 tok/param), nearly 100× beyond Chinchilla-optimal. A second orthogonal axis emerged in 2024-2025: test-time compute scaling, where reasoning performance scales with inference-time compute (CoT steps, search iterations). OpenAI's o1/o3 showed that increased test-time search can substitute for larger model size on reasoning benchmarks.
**Documentation**: [Inference Scaling Law Term](../resources/term_dictionary/term_inference_scaling_law.md)
**Key Paper**: Sardana et al. (2024) — Beyond Chinchilla-Optimal, arXiv:2401.00448
**Key Equation**: Total Cost = 6ND (training, paid once) + 2N × R × T (inference, paid per query)
**Key Insight**: Higher inference demand → smaller model trained longer; LLaMA-13B outperforms GPT-3 (175B) at 13× lower inference cost
**Related**: [Scaling Law](#scaling-law), [LLM](#llm---large-language-models), [CoT](#cot---chain-of-thought), [Foundation Model](#foundation-model)

---

## Model Architecture Components

### CLIP - Contrastive Language-Image Pre-training
**Full Name**: CLIP (Contrastive Language-Image Pre-training)
**Description**: Multimodal vision-language model from OpenAI (Radford et al., ICML 2021) that learns visual representations from natural language supervision by training dual encoders (ViT + Transformer) on 400M image-text pairs with a contrastive objective. **Matches supervised ResNet-50 on ImageNet zero-shot** (76.2%) and shows dramatically superior robustness to distribution shift. CLIP's frozen ViT encoder became the standard vision backbone for BLIP-2, LLaVA, DALL-E 2, and the broader multimodal AI ecosystem (45K+ citations).
**Documentation**: [CLIP Term](../resources/term_dictionary/term_clip.md)
**Key Paper**: Radford et al. (2021, ICML, arXiv:2103.00020), 45,741 citations
**Related**: [BLIP-2](#blip-2---bootstrapping-language-image-pre-training-2), [Q-Former](#q-former---querying-transformer), [Foundation Model](#foundation-model), [Contrastive Learning](acronym_glossary_ml.md#contrastive-learning)

### BLIP-2 - Bootstrapping Language-Image Pre-training 2
**Full Name**: BLIP-2 (Bootstrapping Language-Image Pre-training 2)
**Description**: Vision-language pre-training framework from Salesforce Research (Li et al., ICML 2023) that bridges frozen image encoders and frozen LLMs via a lightweight Querying Transformer (Q-Former). **Achieves state-of-the-art multimodal performance with 54× fewer trainable parameters than Flamingo80B** (~188M vs 10.2B). The Q-Former's cross-attention mechanism with 32 learnable queries has become the standard pattern for modality bridging, directly inspiring 's Tabular-Language Q-Former for operations.
**Documentation**: [BLIP-2 Term](../resources/term_dictionary/term_blip2.md)
**Key Paper**: Li et al. (2023, ICML, arXiv:2301.12597), 7,498 citations
**Related**: [Q-Former](#q-former---querying-transformer), [Phi](#phi---microsoft-small-language-model-family), [Foundation Model](#foundation-model)

### Q-Former - Querying Transformer
**Full Name**: Q-Former (Querying Transformer)
**Description**: Lightweight 12-layer Transformer encoder introduced in BLIP-2 that uses **32 learnable query embeddings with cross-attention** to bridge frozen pre-trained encoders and frozen LLMs. The queries interact with the encoder's output to extract task-relevant information, producing fixed-size "soft tokens" for the LLM. Pre-trained with three objectives (ITC, ITM, ITG) sharing the same weights via different attention masks. Modality-agnostic: originally vision-language, adapted to tabular-language, video (Video-LLaMA), and 3D (3D-LLM).
**Documentation**: [Q-Former Term](../resources/term_dictionary/term_q_former.md)
**Key Paper**: Li et al. (2023, ICML, arXiv:2301.12597)
**Related**: [BLIP-2](#blip-2---bootstrapping-language-image-pre-training-2), [Attention Mechanism](acronym_glossary_ml.md#attention-mechanism), [BERT](#bert---bidirectional-encoder-representations-from-transformers)

### GLP - Generative Latent Prediction
**Full Name**: Generative Latent Prediction
**Description**: World model architecture introduced in PAN (Xiang et al., 2025) that separates simulation into an **autoregressive latent dynamics backbone (LLM-based)** predicting future states in latent space and a **video diffusion decoder** reconstructing visual observations. The LLM encodes world knowledge from text, accepts natural language actions, and predicts latent states autoregressively — unifying latent reasoning (imagination) with realizable dynamics (reality). Enables action-conditioned, long-horizon, open-domain world simulation.
**Documentation**: [GLP Term](../resources/term_dictionary/term_generative_latent_prediction.md)
**Key Paper**: Xiang et al. (2025, arXiv:2511.09057)
**Related**: [LLM](#llm---large-language-models), [Foundation Model](#foundation-model), [CLIP](#clip---contrastive-language-image-pre-training)

### MoR - Mixture-of-Recursions
**Full Name**: Mixture-of-Recursions
**Description**: Efficient LLM architecture (Bae et al., 2025) unifying parameter sharing (weight-tied recursive layers) with adaptive token-level computation (learned routers assigning different recursion depths per token). **Analogous to MoE but routing across depth instead of across experts.** A shared layer stack is reused across recursion steps while routers enable early exit for easy tokens; selective KV caching stores only active tokens' pairs. Achieves up to 2× throughput vs vanilla Transformers at similar accuracy (135M–1.7B scale).
**Documentation**: [MoR Term](../resources/term_dictionary/term_mixture_of_recursions.md)
**Key Paper**: Bae et al. (2025, arXiv:2507.10524)
**Related**: [MoE](acronym_glossary_ml.md#moe---mixture-of-experts), [Phi](#phi---microsoft-small-language-model-family), [Scaling Law](#scaling-law)

### RMSNorm - Root Mean Square Layer Normalization
**Full Name**: Root Mean Square Layer Normalization
**Description**: Simplified normalization technique (Zhang & Sennrich, 2019) that omits the mean-centering step of standard LayerNorm, computing only the RMS statistic: RMSNorm(x) = x / RMS(x) · γ, where RMS(x) = √(1/d · Σxᵢ²). Removes the re-centering invariance property (mean subtraction) that empirical analysis shows contributes minimally to LayerNorm's effectiveness. ~7-64% faster than LayerNorm due to eliminating mean computation and shift. Applied as **pre-normalization** (before attention/FFN, not after) in modern LLMs — a pattern from GPT-3 that stabilizes training of very deep Transformers. Adopted by LLaMA, Gemma, Mistral, Qwen, and most post-2023 foundation models.
**Documentation**: [RMSNorm Term](../resources/term_dictionary/term_rmsnorm.md)
**Key Paper**: Zhang & Sennrich (2019) — Root Mean Square Layer Normalization
**Key Property**: Mathematically equivalent to LayerNorm when input has zero mean; ~7-64% speedup from removing mean computation
**Related**: [LLM](#llm---large-language-models), [Scaling Law](#scaling-law), [SwiGLU](#swiglu---swish-gated-linear-unit), [RoPE](#rope---rotary-position-embedding)

### SwiGLU - Swish-Gated Linear Unit
**Full Name**: Swish-Gated Linear Unit (SwiGLU Activation Function)
**Description**: Gated activation function (Shazeer, 2020) combining the Swish activation (x · σ(x)) with the Gated Linear Unit (GLU) mechanism: SwiGLU(x) = Swish(xW₁) ⊙ (xV). Replaces the standard ReLU/GELU activation in the Transformer FFN block. Uses three weight matrices (W₁, V, W₂) instead of two, so the hidden dimension is adjusted to ⅔×4d to maintain parameter parity. Empirically outperforms all other activation functions tested by Shazeer across multiple benchmarks. LLaMA's variant: FFN_SwiGLU(x) = (Swish₁(xW₁) ⊙ xV)W₂ with hidden dim = ⅔ × 4d rounded to nearest multiple of 256. Adopted by LLaMA, PaLM, Gemma, Mistral, and most post-2023 foundation models.
**Documentation**: [SwiGLU Term](../resources/term_dictionary/term_swiglu.md)
**Key Paper**: Shazeer (2020) — GLU Variants Improve Transformer
**Key Property**: Gated mechanism provides multiplicative interaction; ⅔×4d hidden dim maintains parameter count despite third weight matrix
**Related**: [LLM](#llm---large-language-models), [RMSNorm](#rmsnorm---root-mean-square-layer-normalization), [RoPE](#rope---rotary-position-embedding)

### RoPE - Rotary Position Embedding
**Full Name**: Rotary Position Embedding
**Description**: Positional encoding method (Su et al., 2021) that encodes position by rotating query and key vectors in the attention mechanism: f(x, m) = R(m)x, where R(m) is a block-diagonal rotation matrix with angles mθᵢ and θᵢ = 10000^(-2i/d). Achieves relative position encoding through absolute rotations — the dot product q·k depends only on position difference (m-n) due to the orthogonality of rotation matrices. Advantages over alternatives: (1) naturally encodes relative position without explicit relative bias terms, (2) decays attention with distance (long-term decay property), (3) supports efficient context window extension via interpolation (Position Interpolation, NTK-aware, YaRN). Adopted by LLaMA, GPT-NeoX, PaLM, Gemma, Mistral, Qwen, and virtually all post-2023 open foundation models.
**Documentation**: [RoPE Term](../resources/term_dictionary/term_rope.md)
**Key Paper**: Su et al. (2021) — RoFormer: Enhanced Transformer with Rotary Position Embedding
**Key Property**: Rotation-based encoding yields relative position from absolute — q(m)·k(n) depends only on (m-n); extensible via interpolation
**Extension Methods**: Position Interpolation (Chen et al., 2023), NTK-aware (Reddit/bloc97), YaRN (Peng et al., 2023)
**Related**: [LLM](#llm---large-language-models), [RMSNorm](#rmsnorm---root-mean-square-layer-normalization), [SwiGLU](#swiglu---swish-gated-linear-unit), [Scaling Law](#scaling-law)

### Architectural Exaptation
**Full Name**: Architectural Exaptation (Component Exaptation, Architectural Recombination)
**Description**: Pattern in deep learning where components originally developed for one architectural context are repurposed in a different context, producing superior results through novel combination rather than individual invention. Borrowed from evolutionary biology (Gould & Vrba, 1982): exaptation = trait evolved for one function, co-opted for another (feathers: thermoregulation → flight). The canonical example is the "LLaMA trio" — RMSNorm (from GPT-3), SwiGLU (from PaLM), RoPE (from GPTNeo) — none invented for LLaMA, yet their combination became the de facto foundation model standard. Operates at three levels: component exaptation (individual modules, e.g., attention NMT → vision), pattern exaptation (design patterns, e.g., pre-train-then-fine-tune NLP → all domains), and paradigm exaptation (problem-solving approaches, e.g., RLHF game-playing → language alignment). Most deep learning "innovation" is integration/exaptation, not invention — LLaMA (18,793 citations) outperforms most individual component papers.
**Documentation**: [Architectural Exaptation Term](../resources/term_dictionary/term_architectural_exaptation.md)
**Key Concept**: Integration papers can have higher impact than invention papers; the adjacent possible constrains innovation to recombination of existing components
**Key Example**: LLaMA trio (RMSNorm + SwiGLU + RoPE) — zero new components, field-defining architecture
**Related**: [RMSNorm](#rmsnorm---root-mean-square-layer-normalization), [SwiGLU](#swiglu---swish-gated-linear-unit), [RoPE](#rope---rotary-position-embedding), [Scaling Law](#scaling-law)

### KV Cache - Key-Value Cache
**Full Name**: Key-Value Cache
**Description**: Memory optimization for autoregressive transformer inference that stores previously computed key and value projection vectors, avoiding redundant recomputation at each generation step. The KV cache grows linearly with sequence length and is the **primary memory bottleneck in LLM serving**, often consuming more GPU memory than the model weights themselves. Naive contiguous allocation wastes 60-80% of KV cache memory due to fragmentation and over-reservation. Optimization approaches include PagedAttention (block-based noncontiguous storage), grouped-query attention (sharing KV across head groups), and KV cache quantization (reduced precision storage).
**Documentation**: [KV Cache](../resources/term_dictionary/term_kv_cache.md)
**Key Paper**: Kwon et al. (2023) — Efficient Memory Management for LLM Serving with PagedAttention
**Related**: [LLM](#llm---large-language-models), [vLLM](#vllm---virtual-large-language-model-serving-engine), [Attention Mechanism](../resources/term_dictionary/term_attention_mechanism.md)

---

## GPU & Systems Optimization

### FlashAttention - IO-Aware Exact Attention Algorithm
**Full Name**: FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
**Description**: IO-aware exact attention algorithm (Dao et al., 2022) that uses tiling, online softmax, and recomputation to reduce GPU HBM accesses from Θ(Nd + N²) to Θ(N²d²M⁻¹) without any approximation. Achieves 2-4x wall-clock speedup and up to 20x memory reduction by keeping intermediate attention computations in fast on-chip SRAM instead of materializing the full N×N attention matrix in HBM. Integrated into PyTorch 2.0+, Hugging Face Transformers, and vLLM. Enables practical training with 4K-64K+ context lengths.
**Documentation**: [FlashAttention Term](../resources/term_dictionary/term_flash_attention.md)
**Paper**: [Dao et al. (2022)](../resources/papers/lit_dao2022flashattention.md) — NeurIPS 2022, 3725+ citations
**Versions**: FlashAttention (2022), FlashAttention-2 (2023), FlashAttention-3 (2024, H100-optimized)
**Status**: ✅ Active - Universal standard for attention computation in modern Transformers
**Related**: [IO-Awareness](#io-awareness---memory-hierarchy-aware-algorithm-design), [Online Softmax](#online-softmax---incremental-softmax-algorithm), [Kernel Fusion](#kernel-fusion---gpu-operator-fusion), [Tiling](#tiling---block-decomposition-for-fast-memory-utilization), [Self-Attention](../resources/term_dictionary/term_self_attention.md), [Transformer](../resources/term_dictionary/term_transformer.md), [KV Cache](#kv-cache---key-value-cache), [vLLM](#vllm---virtual-large-language-model-serving-engine)

### IO-Awareness - Memory-Hierarchy-Aware Algorithm Design
**Full Name**: IO-Awareness (Input/Output-Aware Algorithm Design)
**Description**: Design principle for GPU algorithms that optimizes for memory access patterns (reads/writes between HBM and SRAM) rather than solely minimizing FLOPs. On modern GPUs, compute throughput has grown faster than memory bandwidth, making many operations memory-bound. IO-aware algorithms explicitly minimize HBM accesses even if this requires more FLOPs — FlashAttention performs 13% more FLOPs but runs 7.6x faster by reducing HBM accesses 9.2x. Rooted in decades of cache-aware computing (BLAS, database systems, HPC).
**Documentation**: [IO-Awareness Term](../resources/term_dictionary/term_io_awareness.md)
**Related**: [FlashAttention](#flashattention---io-aware-exact-attention-algorithm), [Tiling](#tiling---block-decomposition-for-fast-memory-utilization), [Kernel Fusion](#kernel-fusion---gpu-operator-fusion)

### Online Softmax - Incremental Softmax Algorithm
**Full Name**: Online Softmax (Single-Pass Numerically Stable Softmax)
**Description**: Algorithm that computes exact softmax incrementally over blocks without requiring a full pass to determine the global maximum or normalization constant. Maintains running statistics (running max m and running sum of exponentials ℓ) updated as each new block is processed. Critical enabler of tiled attention — without it, softmax would require materializing the full N×N attention score matrix. First described by Milakov & Gimelshein (2018), adopted by FlashAttention (2022).
**Documentation**: [Online Softmax Term](../resources/term_dictionary/term_online_softmax.md)
**Related**: [FlashAttention](#flashattention---io-aware-exact-attention-algorithm), [Tiling](#tiling---block-decomposition-for-fast-memory-utilization), [Self-Attention](../resources/term_dictionary/term_self_attention.md)

### Tiling - Block Decomposition for Fast Memory Utilization
**Full Name**: Tiling (Loop Tiling / Cache Blocking)
**Description**: Algorithm design technique that decomposes large computations into smaller blocks (tiles) sized to fit in fast on-chip memory (SRAM, L1/L2 cache), maximizing data reuse and minimizing slow off-chip memory accesses. In FlashAttention, Q/K/V matrices are partitioned into blocks along the sequence dimension so the full N×N attention matrix never materializes in HBM. Block sizes are chosen to satisfy SRAM capacity constraints while maximizing parallelism and arithmetic intensity.
**Documentation**: [Tiling Term](../resources/term_dictionary/term_tiling.md)
**Related**: [FlashAttention](#flashattention---io-aware-exact-attention-algorithm), [IO-Awareness](#io-awareness---memory-hierarchy-aware-algorithm-design), [Online Softmax](#online-softmax---incremental-softmax-algorithm), [Kernel Fusion](#kernel-fusion---gpu-operator-fusion)

### Kernel Fusion - GPU Operator Fusion
**Full Name**: Kernel Fusion (GPU Operator Fusion)
**Description**: GPU optimization technique combining multiple sequential operations into a single GPU kernel launch, eliminating intermediate HBM reads/writes between operations. In FlashAttention, 6 separate kernels (matmul, scale, mask, softmax, dropout, matmul) are fused into 1 kernel, keeping all intermediates in registers/SRAM. Reduces both memory bandwidth consumption and kernel launch overhead. Supported by PyTorch 2.0 (torch.compile/TorchInductor), Triton, TensorRT, and hand-written CUDA kernels.
**Documentation**: [Kernel Fusion Term](../resources/term_dictionary/term_kernel_fusion.md)
**Related**: [FlashAttention](#flashattention---io-aware-exact-attention-algorithm), [IO-Awareness](#io-awareness---memory-hierarchy-aware-algorithm-design), [Tiling](#tiling---block-decomposition-for-fast-memory-utilization)

---

## LLM Serving & Inference

### vLLM - Virtual Large Language Model Serving Engine
**Full Name**: Virtual Large Language Model Serving Engine
**Description**: Open-source high-throughput LLM serving engine that introduced the PagedAttention algorithm for efficient KV cache memory management. Applies OS virtual memory concepts (paging, demand allocation, copy-on-write) to GPU memory, storing KV cache in fixed-size noncontiguous blocks mapped through block tables. **Achieves 2-4× throughput improvement** over prior systems by reducing KV cache memory waste from 60-80% to less than 4%. Supports continuous batching, tensor parallelism, and copy-on-write KV cache sharing for beam search and parallel sampling. With 72,000+ GitHub stars, vLLM has become the de facto standard for LLM serving in both research and production.
**Documentation**: [vLLM](../resources/term_dictionary/term_vllm.md)
**Key Paper**: Kwon et al. (2023) — Efficient Memory Management for LLM Serving with PagedAttention (SOSP 2023)
**Related**: [KV Cache](#kv-cache---key-value-cache), [LLM](#llm---large-language-models), [Inference Scaling Law](#inference-scaling-law)

### Speculative Decoding - Draft-then-Verify Inference Acceleration
**Full Name**: Speculative Decoding (also: Speculative Sampling)
**Description**: An inference optimization technique that accelerates autoregressive generation by pairing a large target model with a smaller, faster draft model that speculatively generates candidate tokens. The target model verifies all draft tokens in a single forward pass using rejection sampling, accepting or resampling based on probability ratios. **The method guarantees an identical output distribution to standard autoregressive decoding, providing 2-3x speedup with zero quality loss.** Exploits the fact that LLM inference is memory-bandwidth-bound, leaving spare compute for parallel verification. Variants include draft-model-based (Leviathan et al., 2022), self-speculative decoding, Medusa (parallel heads), and EAGLE (feature-level drafting).
**Documentation**: [Speculative Decoding](../resources/term_dictionary/term_speculative_decoding.md)
**Related**: [vLLM](#vllm---virtual-large-language-model-serving-engine), [LLM](#llm---large-language-models), [Transformer](../resources/term_dictionary/term_transformer.md)

### Gist Token - Learned Prompt Compression Token
**Full Name**: Gist Token
**Description**: Special learned token that compresses prompt context into compact latent representations within a transformer model. Introduced by Mu et al. (NeurIPS 2023), gist tokens are trained by modifying the attention mask so generated tokens can only attend to gist positions (not original prompt tokens), forcing the model to compress all necessary information into the gist representations. **Achieves up to 26x compression of prompts with minimal quality loss and up to 40% FLOPs reduction.** Operates in the model's embedding space (not human-readable), unlike MEMENTO's natural language mementos. Compressed representations are cacheable for reuse across requests sharing the same prompt.
**Documentation**: [Gist Token](../resources/term_dictionary/term_gist_token.md)
**Key Paper**: Mu et al. (2023) — Learning to Compress Prompts with Gist Tokens (NeurIPS 2023)
**Related**: [KV Cache](#kv-cache---key-value-cache), [vLLM](#vllm---virtual-large-language-model-serving-engine), [Block Masking](#block-masking---physical-kv-cache-eviction)

### Block Masking - Physical KV Cache Eviction
**Full Name**: Block Masking
**Description**: Inference-time technique that physically removes contiguous blocks of KV cache entries from GPU memory after they have been summarized or deemed unnecessary. Unlike standard attention masking (which zeros weights but retains KV entries), block masking reclaims memory immediately. Introduced in MEMENTO (Kontonis et al., 2026) for reasoning chain compression — after a reasoning block is completed and summarized into a memento, the block's KV entries are evicted. **Achieves ~2.5x peak KV cache reduction and ~1.75x throughput improvement** from both reduced memory and reduced attention computation. Implemented as a vLLM extension compatible with PagedAttention's block-based memory manager.
**Documentation**: [Block Masking](../resources/term_dictionary/term_block_masking.md)
**Key Paper**: Kontonis et al. (2026) — MEMENTO: Teaching LLMs to Manage Their Own Context
**Related**: [KV Cache](#kv-cache---key-value-cache), [vLLM](#vllm---virtual-large-language-model-serving-engine), [Gist Token](#gist-token---learned-prompt-compression-token), [FlashAttention](#flashattention---io-aware-exact-attention-algorithm)

---

## Model Compression & Quantization

### PTQ - Post-Training Quantization
**Full Name**: Post-Training Quantization
**Description**: A model compression technique that reduces the numerical precision of a pre-trained model's weights and/or activations without retraining. PTQ maps floating-point values to lower-bit integers (Int8, Int4) using scaling constants derived from calibration data or model statistics. **Unlike quantization-aware training (QAT), PTQ requires no gradient computation and can be applied to any pre-trained checkpoint.** Key methods include absmax quantization (symmetric) and zero-point quantization (asymmetric), with granularity ranging from tensor-wise to vector-wise.
**Documentation**: [PTQ](../resources/term_dictionary/term_ptq.md), [Quantization](../resources/term_dictionary/term_quantization.md)
**Related**: [LLM.int8](#llmint8---8-bit-matrix-multiplication-for-transformers), [QLoRA](../resources/term_dictionary/term_qlora.md), [Knowledge Distillation](acronym_glossary_ml.md#kd---knowledge-distillation)

### LLM.int8 - 8-bit Matrix Multiplication for Transformers
**Full Name**: LLM.int8
**Description**: A two-part post-training quantization method for transformer inference that combines vector-wise Int8 quantization with mixed-precision decomposition for outlier features. The method isolates emergent outlier dimensions (magnitude > 6 standard deviations) into FP16 computation while quantizing the remaining 99.9% of values to Int8. **The key discovery is that transformer activations undergo a phase transition at ~6.7B parameters where outlier features become fully coordinated across all layers, concentrating in just 6 hidden dimensions.** Enables zero-degradation Int8 inference for models up to 175B parameters with ~2x memory reduction.
**Documentation**: [LLM.int8](../resources/term_dictionary/term_llm_int8.md), [Quantization](../resources/term_dictionary/term_quantization.md)
**Key Paper**: Dettmers et al. (2022), NeurIPS — [lit_dettmers2022llm](../resources/papers/lit_dettmers2022llm.md)
**Related**: [PTQ](#ptq---post-training-quantization), [QLoRA](../resources/term_dictionary/term_qlora.md), [Knowledge Distillation](acronym_glossary_ml.md#kd---knowledge-distillation)

### GPTQ - Generative Pre-trained Transformer Quantization
**Full Name**: GPTQ (named for its application to GPT-family models)
**Description**: A one-shot weight quantization method based on approximate second-order information (Hessian). GPTQ quantizes weights to Int4 or Int3 by solving a layer-wise optimization problem that minimizes the squared error between quantized and original outputs. **Uses Optimal Brain Surgeon (OBS) framework with lazy batch updates for efficiency, processing a 175B model in ~4 hours on a single GPU.** Achieves near-lossless Int4 quantization, enabling 175B models to run on a single GPU.
**Documentation**: [GPTQ](../resources/term_dictionary/term_gptq.md), [Quantization](../resources/term_dictionary/term_quantization.md)
**Related**: [PTQ](#ptq---post-training-quantization), [LLM.int8](#llmint8---8-bit-matrix-multiplication-for-transformers), [AWQ](#awq---activation-aware-weight-quantization)

### AWQ - Activation-Aware Weight Quantization
**Full Name**: Activation-Aware Weight Quantization
**Description**: A weight-only quantization method that identifies salient weight channels by analyzing activation magnitudes rather than weight magnitudes. AWQ scales important weight channels before quantization to reduce their relative quantization error. **The key insight is that only ~1% of weights are critical (those corresponding to high-activation channels), and protecting these via per-channel scaling provides significant quality improvement.** Achieves strong Int4 quantization without calibration data dependency.
**Documentation**: [AWQ](../resources/term_dictionary/term_awq.md), [Quantization](../resources/term_dictionary/term_quantization.md)
**Related**: [PTQ](#ptq---post-training-quantization), [GPTQ](#gptq---generative-pre-trained-transformer-quantization)

### RaBitQ - Randomized Bit Quantization
**Full Name**: RaBitQ (Randomized Bit Quantization)
**Description**: Vector quantization method (Gao & Long, SIGMOD 2024) that compresses D-dimensional vectors into D-bit strings with **sharp theoretical error bounds O(1/√D)** for ANN search. Uses random orthogonal rotation + sign quantization + unbiased ratio estimator. First VQ method with formal guarantees; outperforms Product Quantization with half the code length. **Prior art at the center of the TurboQuant novelty dispute** — TurboQuant extends RaBitQ's core technique to multi-bit KV cache settings.
**Documentation**: [RaBitQ Term](../resources/term_dictionary/term_rabitq.md)
**Key Paper**: Gao & Long (2024, SIGMOD, arXiv:2405.12497), 58 citations
**Related**: [TurboQuant](#turboquant---online-vector-quantization-with-near-optimal-distortion), [PTQ](#ptq---post-training-quantization), [GPTQ](#gptq---generative-pre-trained-transformer-quantization)

### TurboQuant - Online Vector Quantization with Near-optimal Distortion
**Full Name**: TurboQuant
**Description**: Data-oblivious vector quantization algorithm (Zandieh et al., 2025) achieving near-optimal distortion rates (within ~2.7× of information-theoretic lower bounds) via random rotation + per-coordinate scalar quantization. **Key insight: rotation induces near-independent Beta-distributed coordinates, reducing vector quantization to trivial scalar quantization.** For Transformer attention, a two-stage QJL correction produces unbiased inner product estimators. KV cache quality-neutral at 3.5 bits/channel. Already adopted by ITQ3_S (3-bit LLM weights) and TurboESM (protein LM KV cache).
**Documentation**: [TurboQuant Term](../resources/term_dictionary/term_turboquant.md)
**Key Paper**: Zandieh et al. (2025, arXiv:2504.19874)
**Related**: [PTQ](#ptq---post-training-quantization), [GPTQ](#gptq---generative-pre-trained-transformer-quantization), [AWQ](#awq---activation-aware-weight-quantization)

### DistilBERT - Distilled BERT
**Full Name**: Distilled Bidirectional Encoder Representations from Transformers
**Description**: A 6-layer student model distilled from 12-layer BERT-base during pre-training using a triple loss framework combining distillation cross-entropy, masked language modeling, and cosine embedding loss. **The most impactful design choice is teacher weight initialization — initializing student layer i from teacher layer 2i contributes +3.69 GLUE points over random initialization.** Retains 97% of BERT-base's GLUE performance (77.0 vs 79.5) while being 40% smaller (66M vs 110M parameters) and 60% faster on CPU. Demonstrated that pre-training distillation produces general-purpose compressed models transferable to any downstream task.
**Documentation**: [lit_sanh2019distilbert](../resources/papers/lit_sanh2019distilbert.md), [Knowledge Distillation](../resources/term_dictionary/term_knowledge_distillation.md)
**Related**: [KD](acronym_glossary_ml.md#kd---knowledge-distillation), [BERT](../resources/term_dictionary/term_bert.md)

---

## Retrieval & Knowledge Systems

### Episodic Memory - Experience-Based Memory System for LLM Agents
**Full Name**: Episodic Memory (EM)
**Description**: A memory system that stores specific experiences and events — what happened, when, where, and in what context — enabling AI agents to recall past interactions and learn from prior task executions. Distinguished by five key properties: long-term storage, explicit reasoning, single-shot learning, instance-specificity, and contextual relations. **Unlike semantic memory (facts) or procedural memory (skills), episodic memory captures the full context of individual events for adaptive behavior.** Grounded in Complementary Learning Systems theory (McClelland et al., 1995). Used in this domain's SENTRIX system where episodic memory of past reasoning trajectories yields up to 27% recall gain for phishing detection.
**Documentation**: [Episodic Memory](../resources/term_dictionary/term_episodic_memory.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation), [PlugMem](#plugmem---plugin-memory-module-for-llm-agents), [KG](#kg---knowledge-graph)

### PPR - Personalized PageRank
**Full Name**: Personalized PageRank
**Description**: Graph ranking algorithm ranking knowledge graph nodes by relevance to seed entities via biased random walks. Core retrieval mechanism in GraphRAG systems. 150ms warm latency, 15K-node graphs, top 400 nodes capture 95% relevance.
**Documentation**: [PPR Term](../resources/term_dictionary/term_ppr.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [KG](#kg---knowledge-graph), [LLM](#llm---large-language-models), [Network Science: PPR](acronym_glossary_network_science.md#ppr---personalized-pagerank)

### KG - Knowledge Graph
**Full Name**: Knowledge Graph
**Documentation**: [Knowledge Graph Term](../resources/term_dictionary/term_knowledge_graph.md)
**Status**: ✅ Active - foundational concept for graph-based anomaly detection
**Related**: [RAG](#rag---retrieval-augmented-generation), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation), [PPR](#ppr---personalized-pagerank)

### KG Enrichment - Knowledge Graph Enrichment
**Full Name**: Knowledge Graph Enrichment
**Description**: Process of adding new entities, relationships, and attributes to an existing KG from external sources (text, databases) while maintaining schema conformance and quality. Differs from KG completion (which infers missing links from existing structure). **Pipeline: ingestion → NER → relation extraction → schema alignment → conflict resolution → quality assessment.** KARMA (Lu, 2025) demonstrates multi-agent LLM enrichment extracting 38K+ entities from 720 papers at 83% correctness.
**Documentation**: [KG Enrichment Term](../resources/term_dictionary/term_knowledge_graph_enrichment.md)
**Related**: [KG](#kg---knowledge-graph), [NER](#ner---named-entity-recognition), [RAG](#rag---retrieval-augmented-generation)

### Schema Alignment - Ontology Matching
**Full Name**: Schema Alignment (Ontology Matching)
**Description**: Process of determining correspondences between concepts across different schemas or ontologies, enabling data integration and semantic interoperability. In KG construction, maps newly extracted entities and relationships to target schema types. **Matching dimensions: lexical (string similarity), structural (graph topology), semantic (embedding-based), and instance-based (data overlap).** OAEI benchmark since 2004. In KARMA, the Schema Alignment Agent maps novel entities to KG types or flags for schema expansion.
**Documentation**: [Schema Alignment Term](../resources/term_dictionary/term_schema_alignment.md)
**Related**: [KG](#kg---knowledge-graph), [KG Enrichment](#kg-enrichment---knowledge-graph-enrichment), [NER](#ner---named-entity-recognition)

### Entity Alignment - Cross-KG Entity Matching
**Full Name**: Entity Alignment (Entity Resolution)
**Description**: Determines whether entities from different knowledge graphs refer to the same real-world object. Core subtask of knowledge fusion. **Evolved from lexical matching (string similarity) through embedding-based alignment (TransE, GCN-Align) to LLM reasoning (LLM-Align, EntGPT).** Challenges include name variation, attribute incompleteness, and O(n²) comparison cost. COMEM cascades lightweight filtering with fine-grained LLM reasoning for efficiency.
**Documentation**: [Entity Alignment Term](../resources/term_dictionary/term_entity_alignment.md)
**Related**: [KG](#kg---knowledge-graph), [Schema Alignment](#schema-alignment---ontology-matching), [Knowledge Fusion](#knowledge-fusion---kg-integration)

### Knowledge Fusion - KG Integration
**Full Name**: Knowledge Fusion
**Description**: Integrates heterogeneous knowledge sources into a coherent KG by resolving duplication, conflict, and heterogeneity. Third layer of the classical KG construction pipeline. **Operates at schema-level (unifying type systems) and instance-level (aligning/deduplicating entities).** Hybrid frameworks (KARMA, Graphusion) handle both levels in unified workflows. LLMs evolved from simple matchers to adaptive reasoning agents for scalable, self-correcting fusion.
**Documentation**: [Knowledge Fusion Term](../resources/term_dictionary/term_knowledge_fusion.md)
**Related**: [KG](#kg---knowledge-graph), [Entity Alignment](#entity-alignment---cross-kg-entity-matching), [Schema Alignment](#schema-alignment---ontology-matching), [KG Enrichment](#kg-enrichment---knowledge-graph-enrichment)

### PlugMem - Plugin Memory Module for LLM Agents
**Full Name**: PlugMem (Task-Agnostic Plugin Memory Module)
**Description**: A task-agnostic plugin memory module that transforms raw episodic experience into a knowledge-centric memory graph organized around propositional knowledge (fact blocks) and prescriptive knowledge (workflow blocks). Unlike [GraphRAG](#graphrag---graph-based-retrieval-augmented-generation) which uses entities as graph nodes, PlugMem uses **knowledge units as the fundamental unit of memory access and organization**. Three modules: Structuring (episodic standardization + knowledge extraction), Retrieval (abstraction-aware multi-hop traversal via concepts/intents), and Reasoning (task-adaptive compression). Achieves highest memory information density across three heterogeneous benchmarks while using 1-2 orders of magnitude fewer memory tokens than baselines.
**Documentation**: [PlugMem](../resources/term_dictionary/term_plugmem.md) | [PlugMem Paper (Yang et al., 2026)](../resources/papers/lit_yang2026plugmem.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [GraphRAG](#graphrag---graph-based-retrieval-augmented-generation), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation), [Knowledge Agent](#knowledge-agent)

### Knowledge Agent
**Full Name**: Knowledge Agent (Grounded Reasoning Agent)
**Description**: AI system that iteratively queries, retrieves, and reasons over large document collections to produce grounded answers. Unlike single-step [RAG](#rag---retrieval-augmented-generation), knowledge agents use multi-turn interactions with search tools, maintaining conversation history and adapting search strategy based on intermediate results. KARL (Chang et al., 2026) demonstrates that RL-trained knowledge agents match frontier models (Claude Opus 4.6) at 33% lower cost on KARLBench. Key components: agent harness (tool orchestration), context compression (self-compression via RL), and test-time compute scaling (parallel thinking, value-guided search).
**Documentation**: [Knowledge Agent Term](../resources/term_dictionary/term_knowledge_agent.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [RL](acronym_glossary_ml.md#rl---reinforcement-learning), [OAPL](acronym_glossary_ml.md#oapl---optimal-advantage-based-policy-learning), [LLM](#llm---large-language-models)

---

## Fine-Tuning & Adaptation

### Fine-Tuning
**Full Name**: Fine-Tuning (Transfer Learning via Fine-Tuning)
**Description**: Process of adapting a pre-trained model to a specific downstream task by continuing training on task-specific labeled data with a small learning rate. In the BERT paradigm, fine-tuning adds a minimal task-specific output layer and updates all parameters end-to-end. Default transfer learning strategy for NLP since 2019. Modern variants include full fine-tuning (all parameters), parameter-efficient fine-tuning (PEFT: LoRA, adapters, prefix tuning), instruction tuning (SFT), and RLHF/DPO for LLM alignment. BSM-BERT models follow canonical BERT fine-tuning: linear layer on [CLS], LR=2e-5, 3 epochs on labeled anomaly data.
**Documentation**: [Fine-Tuning Term](../resources/term_dictionary/term_fine_tuning.md)
**Key Variants**: Full fine-tuning, LoRA/PEFT, Instruction tuning (SFT), RLHF, DPO
**domain Applications**: BSM-BERT models (RnR, AtoZ), CrossBERT, Abuse 
**Related**: [LoRA](#lora---low-rank-adaptation), [PEFT](#peft---parameter-efficient-fine-tuning), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [LLM](#llm---large-language-models)

### LoRA - Low-Rank Adaptation
**Full Name**: Low-Rank Adaptation
**Description**: Parameter-efficient fine-tuning injecting trainable low-rank matrices while keeping base weights frozen. Reduces trainable parameters by up to 10,000x and GPU memory by 3x vs full fine-tuning. Core mechanism: W = W₀ + BA where B ∈ ℝ^(d×r), A ∈ ℝ^(r×k), rank r ≪ min(d,k). Applied to Wq, Wv in self-attention. Zero inference latency (BA merges into W₀). Motivated by the [intrinsic dimensionality](#intrinsic-dimensionality) hypothesis — weight updates during adaptation are inherently low-rank.
**Documentation**: [LoRA Term](../resources/term_dictionary/term_lora.md) | [LoRA Paper (Hu et al., 2021)](../resources/papers/lit_hu2021lora.md)
**Key Papers**: Hu et al. (2021) LoRA (ICLR 2022, 16,906 citations)
**Key Extensions**: [QLoRA](#qlora---quantized-low-rank-adaptation) (4-bit base + 16-bit LoRA), DoRA, AdaLoRA, HyperLoRA
**Related**: [PEFT](#peft---parameter-efficient-fine-tuning), [QLoRA](#qlora---quantized-low-rank-adaptation), [Intrinsic Dimensionality](#intrinsic-dimensionality), [LLM](#llm---large-language-models)

### QLoRA - Quantized Low-Rank Adaptation
**Full Name**: Quantized Low-Rank Adaptation
**Description**: Extension of LoRA combining 4-bit NormalFloat4 quantization of frozen base weights with 16-bit LoRA adapter training. Three innovations: NF4 data type (optimal 4-bit format for normally distributed weights), double quantization (quantizing quantization constants), paged optimizers (unified memory for gradient checkpointing). Enables fine-tuning 65B models on a single 48GB GPU while matching 16-bit performance. Guanaco 65B matched 99.3% of ChatGPT on Vicuna benchmark.
**Documentation**: [QLoRA Term](../resources/term_dictionary/term_qlora.md)
**Key Papers**: Dettmers et al. (2023) QLoRA (NeurIPS 2023)
**Related**: [LoRA](#lora---low-rank-adaptation), [PEFT](#peft---parameter-efficient-fine-tuning), [LLM](#llm---large-language-models)

### Intrinsic Dimensionality
**Full Name**: Intrinsic Dimensionality (Intrinsic Rank)
**Description**: The minimum number of dimensions needed to describe a learning problem's solution, regardless of the ambient parameter count. For NLP fine-tuning, intrinsic dimensionality d_int ≪ d (total parameters) — e.g., RoBERTa 125M on MNLI needs only ~200 free parameters for 90% of full FT performance. Theoretical foundation for LoRA and all PEFT methods: if weight updates are inherently low-rank, constraining them to low-rank matrices loses almost nothing.
**Documentation**: [Intrinsic Dimensionality Term](../resources/term_dictionary/term_intrinsic_dimensionality.md)
**Key Papers**: Li et al. (2018) Intrinsic Dimension (ICLR 2018), Aghajanyan et al. (2021) ACL 2021
**Related**: [LoRA](#lora---low-rank-adaptation), [PEFT](#peft---parameter-efficient-fine-tuning), [Fine-Tuning](#fine-tuning)

### PEFT - Parameter-Efficient Fine-Tuning
**Full Name**: Parameter-Efficient Fine-Tuning
**Description**: Family of techniques adapting large pre-trained models by training only 0.01–1% of parameters. Key methods: LoRA (low-rank matrices), Adapters (serial bottleneck layers), Prefix Tuning (learnable prefix tokens), Prompt Tuning (soft prompt embeddings), BitFit (bias-only). Effectiveness explained by [intrinsic dimensionality](#intrinsic-dimensionality) — weight updates during adaptation are inherently low-rank. Enables practical multi-task deployment: one base model + many small task-specific adapters.
**Documentation**: [PEFT Term](../resources/term_dictionary/term_peft.md)
**Key Methods**: LoRA (10,000× param reduction, zero inference latency), QLoRA (4-bit quantization), Adapters (serial insertion), Prefix Tuning (soft prefixes), BitFit (bias-only)
**Related**: [LoRA](#lora---low-rank-adaptation), [QLoRA](#qlora---quantized-low-rank-adaptation), [Intrinsic Dimensionality](#intrinsic-dimensionality), [LLM](#llm---large-language-models)

### RLHF - Reinforcement Learning from Human Feedback
**Full Name**: Reinforcement Learning from Human Feedback
**Description**: Post-training alignment technique that optimizes a language model's policy to maximize a learned reward signal derived from human preference comparisons. Canonical pipeline: (1) Supervised Fine-Tuning (SFT) on demonstrations, (2) Reward Model training on pairwise comparisons (Bradley-Terry), (3) [PPO](../resources/term_dictionary/term_ppo.md) optimization with KL penalty from SFT model. InstructGPT (2022) demonstrated 1.3B aligned model preferred over 175B unaligned GPT-3. Adopted by ChatGPT, Claude, Gemini, Llama-2. Alternatives: DPO (eliminates RM+PPO), KTO, ORPO, SimPO, GRPO.
**Documentation**: [RLHF Term](../resources/term_dictionary/term_rlhf.md)
**Key Papers**: Ouyang et al. (2022) InstructGPT, Christiano et al. (2017), Rafailov et al. (2023) DPO
**Related**: [Fine-Tuning](#fine-tuning), [LLM](#llm---large-language-models), [RM](#rm---reward-model)

### RM - Reward Model
**Full Name**: Reward Model
**Description**: Neural network trained on human pairwise preference comparisons to produce a scalar score r(prompt, response) → ℝ indicating alignment with human preferences. In RLHF, serves as proxy for human judgment during PPO optimization. Trained using Bradley-Terry loss on ranked output pairs. Key challenges: reward hacking (Goodhart's Law), distribution shift, sycophancy. Variants: Outcome RM (ORM, scores final answer), Process RM (PRM, scores each reasoning step). InstructGPT used a 6B RM for 175B policy due to training instability of larger RMs.
**Documentation**: [Reward Model Term](../resources/term_dictionary/term_reward_model.md)
**Key Papers**: Ouyang et al. (2022), Gao et al. (2023) scaling laws, Lightman et al. (2023) PRM800K
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [Fine-Tuning](#fine-tuning), [LLM](#llm---large-language-models)

### CAI - Constitutional AI
**Full Name**: Constitutional AI
**Description**: Alignment method that trains harmless AI assistants using written principles (a "constitution") instead of human labels for harmful outputs. Two phases: (1) SL-CAI — self-critique and revision guided by ~16 constitutional principles, (2) RL-CAI — RLAIF using AI-generated preference labels. Achieves a Pareto improvement over RLHF: models are simultaneously more helpful, more harmless, and less evasive. Key insight: shifts alignment from O(n) human labels to O(1) human principles (scalable oversight). Deployed in Claude (Anthropic). Introduced by Bai et al. (2022).
**Documentation**: [Constitutional AI Term](../resources/term_dictionary/term_constitutional_ai.md)
**Key Paper**: Bai et al. (2022) — [Literature Note](../resources/papers/lit_bai2022constitutional.md)
**Key Result**: Pareto improvement — more helpful AND more harmless than RLHF, with reduced evasion
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [RLAIF](#rlaif---reinforcement-learning-from-ai-feedback), [RM](#rm---reward-model), [CoT](#cot---chain-of-thought), [Red Teaming](#red-teaming)

### Pluralistic Alignment
**Full Name**: Pluralistic Alignment (Value-Pluralistic AI)
**Description**: Alignment paradigm that rejects the assumption of a single "correct" preference and instead trains AI to represent diverse human values. Standard RLHF collapses ~27% inter-annotator disagreement into majority-vote reward signals, suppressing minority viewpoints. Pluralistic alignment learns distributions over preferences via multiple reward models, conditional generation, or steerable value dimensions. Key approaches: reward model ensembles (separate RMs per value perspective), distributional RLHF (learn preference distributions, not point estimates), steerable alignment (user-selected value profiles), and Collective Constitutional AI (crowdsourced principles from diverse populations). Motivated by Prism project showing systematic cross-cultural differences across 21 countries. Arrow's impossibility theorem proves no perfect aggregation exists.
**Documentation**: [Pluralistic Alignment Term](../resources/term_dictionary/term_pluralistic_alignment.md)
**Key Papers**: Sorensen et al. (2024) Value Kaleidoscope, Kirk et al. (2024) Prism, Conitzer et al. (2024) Social Choice, Anthropic (2023) Collective Constitutional AI
**domain Relevance**: Cross-marketplace anomaly norms, investigator preference diversity, escalation threshold tradeoffs
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [CAI](#cai---constitutional-ai), [RLAIF](#rlaif---reinforcement-learning-from-ai-feedback), [RM](#rm---reward-model)

### RLAIF - Reinforcement Learning from AI Feedback
**Full Name**: Reinforcement Learning from AI Feedback
**Description**: Replaces human preference labels with AI-generated preference labels in the RLHF pipeline. An AI model evaluates response pairs according to constitutional principles and generates preference data for reward model training. In Constitutional AI: ~182K AI-generated harmlessness preferences mixed with ~135K human helpfulness preferences. RLAIF matches or exceeds RLHF on harmlessness while eliminating human annotation costs. Chain-of-thought reasoning during AI evaluation further improves preference quality. Core contribution to scalable oversight.
**Documentation**: [RLAIF Term](../resources/term_dictionary/term_rlaif.md)
**Key Paper**: Bai et al. (2022), Lee et al. (2023) — RLAIF at scale
**Key Result**: AI-generated preferences produce reward models as good as or better than human-labeled ones for harmlessness
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [CAI](#cai---constitutional-ai), [RM](#rm---reward-model), [CoT](#cot---chain-of-thought)

### DPO - Direct Preference Optimization
**Full Name**: Direct Preference Optimization
**Description**: Alignment technique that eliminates the need for a separate reward model and RL optimizer (PPO) by reparameterizing the RLHF objective directly in terms of the policy. Shows the optimal policy under the KL-constrained RLHF objective has a closed-form relationship with the reward function, allowing preference learning to be cast as a simple binary cross-entropy loss on human preference pairs. Achieves comparable or superior alignment to PPO-based RLHF while being simpler, more stable, and computationally cheaper (2 models in memory vs. 4). Default alignment method for open-source LLMs (Llama-3, Zephyr, Gemma-2, Mistral). Variants: IPO, KTO, ORPO, SimPO, RSO.
**Documentation**: [DPO Term](../resources/term_dictionary/term_dpo.md)
**Key Paper**: Rafailov et al. (2023), NeurIPS
**Key Properties**: Mathematically equivalent to RLHF under Bradley-Terry + KL constraint, offline (fixed dataset), no reward hacking, no mode collapse from RL
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [RM](#rm---reward-model), [GRPO](#grpo---group-relative-policy-optimization), [CAI](#cai---constitutional-ai)

### GRPO - Group Relative Policy Optimization
**Full Name**: Group Relative Policy Optimization
**Description**: Reinforcement learning alignment method that eliminates the need for a separate critic (value) model by estimating advantages at the group level. For each prompt, GRPO samples G responses, computes verifiable rewards (code execution, math verification), and normalizes rewards within the group to derive advantages: Â_i = (r_i − μ_G) / σ_G. Introduced by DeepSeek (2025) in DeepSeek-R1. Particularly effective for domains with verifiable rewards where correctness can be automatically checked. Key finding: RL applied directly to base models (without SFT) enables large-scale reasoning capabilities to emerge — including spontaneous CoT, self-verification, and metacognitive "aha moments."
**Documentation**: [GRPO Term](../resources/term_dictionary/term_grpo.md)
**Key Paper**: DeepSeek-AI (2025) — DeepSeek-R1; Shao et al. (2024) — DeepSeekMath
**Key Results**: AIME 2024: 79.8% pass@1 (competitive with OpenAI o1), emergent CoT without explicit prompting
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [DPO](#dpo---direct-preference-optimization), [RM](#rm---reward-model), [CoT](#cot---chain-of-thought)

### CISPO - Clipped Importance-Sampled Policy Optimization
**Full Name**: Clipped Importance-Sampled Policy Optimization
**Description**: Reinforcement learning algorithm for LLM post-training that clips importance sampling weights at the sequence level rather than per-token probability ratios. Introduced by MiniMax in their M1 technical report (2025) and adopted by MEMENTO (Kontonis et al., 2026) for reasoning chain compression. Unlike PPO which clips token-level ratios (suppressing rare but critical tokens like mathematical operators), **CISPO clips the full-sequence importance weight, preserving individual token contributions while bounding overall update magnitude**. This produces smoother policy updates and better sample efficiency for long reasoning sequences. Off-policy capable, enabling rollout reuse across update steps.
**Documentation**: [CISPO Term](../resources/term_dictionary/term_cispo.md)
**Key Paper**: MiniMax et al. (2025) — MiniMax-01; Kontonis et al. (2026) — MEMENTO
**Related**: [GRPO](#grpo---group-relative-policy-optimization), [DPO](#dpo---direct-preference-optimization), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [CoT](#cot---chain-of-thought)

### Alignment Scaling Law
**Full Name**: Alignment Scaling Law (Alignment Method Evolution)
**Description**: Speculative concept describing the empirical trajectory showing alignment methods become progressively less reliant on human supervision while achieving comparable or better results. Unlike capability scaling laws (Kaplan 2020) that characterize loss as a function of compute/data/parameters, alignment scaling laws characterize human supervision cost as a function of method generation. Trajectory: RLHF (2022, O(n) human labels) → RLAIF/CAI (2022, O(1) principles) → DPO (2023, eliminates RM + PPO) → GRPO (2025, O(0) for verifiable domains). Each generation targets a different bottleneck. Key question: does alignment converge on zero human oversight, or asymptote at an irreducible minimum?
**Documentation**: [Alignment Scaling Law Term](../resources/term_dictionary/term_alignment_scaling_law.md)
**Related**: [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [RLAIF](#rlaif---reinforcement-learning-from-ai-feedback), [DPO](#dpo---direct-preference-optimization), [GRPO](#grpo---group-relative-policy-optimization), [Scaling Law](#scaling-law)

### Constitutional PRM - Constitutional Process Reward Model
**Full Name**: Constitutional Process Reward Model
**Description**: Theoretical concept combining Process Reward Models (step-level evaluation of reasoning, Lightman et al. 2023) with Constitutional AI (principle-guided evaluation, Bai et al. 2022). Evaluates each reasoning step not just for correctness but for adherence to explicit constitutional principles — producing a per-step × per-principle evaluation matrix. Example: step 2 may be logically correct but violate Principle 2 (non-discriminatory) — a standard PRM misses this; a Constitutional PRM catches it. Not yet realized in a single published system but multiple research threads converge toward it: PRMs, Constitutional AI, GRPO step-level signals, process-level RLHF.
**Documentation**: [Constitutional PRM Term](../resources/term_dictionary/term_constitutional_prm.md)
**Related**: [RM](#rm---reward-model), [CAI](#cai---constitutional-ai), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [GRPO](#grpo---group-relative-policy-optimization), [CoT](#cot---chain-of-thought)

---

## Prompt Engineering & Reasoning

### Atomic Skill - Composable Agent Skill Primitive
**Full Name**: Atomic Skill
**Description**: Minimal, self-contained, independently evaluable agent capability that composes into complex tasks (Ma et al., 2026). **Analogous to building blocks for knowledge: atomic skills are "basis vectors" spanning the task space.** 5 coding skills defined: code localization, editing, unit-test generation, issue reproduction, code review. Joint RL over atomic skills yields +18.7% vs task-specific training, generalizing to unseen composite tasks. Parallels: SlipBox building blocks type knowledge atoms; atomic skills type agent capabilities.
**Documentation**: [Atomic Skill Term](../resources/term_dictionary/term_atomic_skill.md)
**Key Paper**: Ma et al. (2026, arXiv:2604.05013)
**Related**: [LATM](#latm---large-language-models-as-tool-makers), [DSPy](#dspy---declarative-self-improving-language-programs), [Meta-Harness](#meta-harness---end-to-end-harness-optimization)

### LATM - Large Language Models as Tool Makers
**Full Name**: LATM (Large Language Models as Tool Makers)
**Description**: Two-phase framework (Cai et al., ICLR 2024, Google DeepMind) separating **tool creation** (GPT-4 generates reusable Python functions) from **tool use** (GPT-3.5 applies cached tools). Achieves GPT-4 performance at GPT-3.5 cost via amortized tool-making. **Functional caching** stores the function, not the response — generalizable across all instances of a problem class. Direct analogy: SlipBox human = tool maker; SlipBox agent = tool user; SlipBox skills = cached tools.
**Documentation**: [LATM Term](../resources/term_dictionary/term_latm.md)
**Key Paper**: Cai et al. (2023, ICLR 2024, arXiv:2305.17126), 276 citations
**Related**: [DSPy](#dspy---declarative-self-improving-language-programs), [Meta-Harness](#meta-harness---end-to-end-harness-optimization), [Toolformer](../resources/term_dictionary/term_toolformer.md)

### DSPy - Declarative Self-improving Language Programs
**Full Name**: DSPy (Declarative Self-improving Language Programs, pythonically)
**Description**: Declarative programming framework (Khattab et al., ICLR 2024, Stanford) that compiles LM pipeline specifications into optimized prompts or fine-tuned weights. **Decouples interface (signatures: "question → answer") from implementation (prompts/demos).** Modules (Predict, ChainOfThought, ReAct) compose into pipelines; optimizers (BootstrapFewShot, MIPRO, GEPA) automatically discover effective configurations. Small models with DSPy optimization compete with GPT-3.5 expert chains. Co-authored by Omar Khattab, who later co-authored Meta-Harness — the progression from prompt-level to harness-level optimization.
**Documentation**: [DSPy Term](../resources/term_dictionary/term_dspy.md)
**Key Paper**: Khattab et al. (2023, ICLR 2024, arXiv:2310.03714), 634 citations
**Related**: [Meta-Harness](#meta-harness---end-to-end-harness-optimization), [CoT](#cot---chain-of-thought), [RAG](#rag---retrieval-augmented-generation)

### Meta-Harness - End-to-End Harness Optimization
**Full Name**: Meta-Harness
**Description**: Automated harness engineering system (Lee et al., 2026, Stanford/Chelsea Finn) that optimizes the **entire code infrastructure wrapping an LLM** — retrieval, context management, state tracking, tool calls — not just prompts. Uses an agentic proposer (Claude Code Opus-4.6) browsing a filesystem of prior candidates' source code, scores, and raw execution traces (10M tokens/iteration — 500–5,000× more than DSPy/TextGrad). Results: +7.7 pts on text classification (4× fewer tokens), +4.7 on IMO math across 5 held-out models, #2 on TerminalBench-2.
**Documentation**: [Meta-Harness Term](../resources/term_dictionary/term_meta_harness.md)
**Key Paper**: Lee et al. (2026, arXiv:2603.28052)
**Related**: [CoT](#cot---chain-of-thought), [RAG](../resources/term_dictionary/term_rag.md), [LLM](#llm---large-language-models)

### CoT - Chain of Thought
**Full Name**: Chain of Thought (CoT Prompting)
**Description**: Prompting technique augmenting few-shot exemplars with intermediate natural language reasoning steps, enabling LLMs to perform complex multi-step reasoning without fine-tuning. Emergent capability requiring ≥100B parameters. PaLM 540B + 8 CoT exemplars achieves 56.9% on GSM8K (surpassing fine-tuned GPT-3 with verifier at 55%). Ablations confirm natural language reasoning — not extra tokens or equations alone — is the active ingredient. Spawned zero-shot CoT ("Let's think step by step"), self-consistency, tree-of-thought, and the prompt engineering research field. domain relevance: SPOT-X generates chain-of-thought decision rules, uses multi-step reasoning in agentic automation, ARI investigators provide CoT prompts to LLMs.
**Documentation**: [Chain of Thought Term](../resources/term_dictionary/term_chain_of_thought.md)
**Key Paper**: Wei et al. (2022), NeurIPS — [Literature Note](../resources/papers/lit_wei2022chain.md)
**Key Variants**: Zero-shot CoT (Kojima 2022), Self-Consistency (Wang 2022), Tree of Thought (Yao 2023), Process Reward Models (Lightman 2023)
**Key Properties**: Training-free, emergent (≥100B), task-general, interpretable reasoning traces
**domain Applications**: SPOT-X (decision rules with CoT examples),, ARI (investigator-LLM interaction)
**Related**: [LLM](#llm---large-language-models), [Scaling Law](#scaling-law), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [SPOT-X](#spot-x---structured-prompt-optimization-for-text-classification-with-explanations), [](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### Context Engineering - Dynamic Context Assembly for LLMs
**Full Name**: Context Engineering
**Description**: Discipline of designing and building dynamic systems that provide the right information and tools, in the right format, at the right time, to give an LLM everything it needs to accomplish a task. Coined by Andrej Karpathy (June 2025), context engineering reframes the practitioner's role from crafting clever prompt text to engineering the entire information environment reaching the model's context window. **Operates on four pillars: write (persist information externally), select (retrieve relevant context via RAG/tools), compress (summarize to save tokens), and isolate (separate concerns via sub-agents).** Supersedes prompt engineering as the systems-level discipline for LLM application design — Gartner (July 2025): "Context engineering is in, and prompt engineering is out."
**Documentation**: [Context Engineering Term](../resources/term_dictionary/term_context_engineering.md)
**Related**: [Prompt Engineering](#prompt-engineering---llm-input-design-and-optimization), [RAG](#rag---retrieval-augmented-generation), [CoT](#cot---chain-of-thought), [Function Calling](#function-calling---llm-tool-invocation-protocol), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns)

### ReAct - Reasoning + Acting
**Full Name**: ReAct (Reasoning + Acting)
**Description**: Prompting framework that synergizes verbal reasoning traces and task-specific actions in an interleaved Thought-Action-Observation loop. LLM alternates between generating reasoning (Thought), emitting actions that interact with external environments (Action), and receiving environment feedback (Observation). Enables two synergies: *reason to act* (reasoning informs action selection) and *act to reason* (observations ground reasoning, reducing hallucination). On ALFWorld/WebShop, 1-2 shot ReAct outperforms RL/IL agents trained on ~100K samples by 34%/10% absolute. Foundational paradigm for agentic LLM systems — LangChain, Bedrock Agents, and Strands all implement ReAct-style loops. domain relevance: agentic pipeline uses ReAct-style reasoning; agent orchestration patterns (LangGraph, Strands) descend from this framework.
**Documentation**: [ReAct Term](../resources/term_dictionary/term_react.md)
**Key Paper**: Yao et al. (2023), ICLR (notable top 5%) — arXiv:2210.03629
**Key Properties**: Training-free (few-shot), interleaved reasoning+acting, grounded in external observations, interpretable thought traces, human-editable trajectories
**Key Results**: FEVER 60.9% (vs. CoT 56.3%), ALFWorld 71% (vs. Act-only 45%), hallucination reduced (6% vs. 14% false positive)
**Related**: [CoT](#cot---chain-of-thought), [Prompt Engineering](#prompt-engineering---llm-input-design-and-optimization), [Function Calling](#function-calling---llm-tool-invocation-protocol), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns)

### Prompt Engineering - LLM Input Design and Optimization
**Full Name**: Prompt Engineering (Context Engineering)
**Description**: Discipline of designing, structuring, and optimizing natural language inputs to LLMs to elicit desired outputs — spanning task instructions, examples, reasoning scaffolds, and formatting directives. Evolved from ad-hoc prompt crafting (GPT-3, 2020) through systematic techniques (CoT, ReAct, ToT) to programmatic optimization (DSPy, OPRO, APE). **Andrej Karpathy (2025) proposed reframing as "context engineering" — assembling the right information (retrieval, tools, history) matters more than wording.** Key challenge: prompt sensitivity — small changes can cause dramatically different outputs.
**Documentation**: [Prompt Engineering Term](../resources/term_dictionary/term_prompt_engineering.md)
**Related**: [CoT](#cot---chain-of-thought), [Prompt Exaptation](#prompt-exaptation), [Function Calling](#function-calling---llm-tool-invocation-protocol), [Structured Output](#structured-output---schema-constrained-llm-generation), [](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### Function Calling - LLM Tool Invocation Protocol
**Full Name**: Function Calling (Tool Use, Tool Calling)
**Description**: Mechanism enabling LLMs to invoke external functions or tools by generating structured JSON arguments conforming to a predefined schema, rather than producing free-form text. The LLM selects which tool to call and with what parameters; the runtime executes the tool and returns results. Standardized via JSON Schema tool definitions across providers (OpenAI, Anthropic, Google). **Foundation of agentic AI — transforms LLMs from text generators into action-taking agents.** Evolved from ReAct prompting (2022) through native API support (2023-2024) to standardized protocols like MCP (2024).
**Documentation**: [Function Calling Term](../resources/term_dictionary/term_function_calling.md)
**Related**: [Structured Output](#structured-output---schema-constrained-llm-generation), [Prompt Engineering](#prompt-engineering---llm-input-design-and-optimization), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [MCP](../resources/term_dictionary/term_mcp.md)

### Structured Output - Schema-Constrained LLM Generation
**Full Name**: Structured Output (Constrained Decoding, Guided Generation)
**Description**: Techniques constraining LLM generation to conform to a predefined schema (JSON Schema, grammar, regex) by masking invalid tokens at each decoding step via finite state machines. **Guarantees 100% schema compliance — eliminates parsing failures entirely.** Introduced by Willard & Louf (2023, Outlines library); adopted by OpenAI (Aug 2024) and Anthropic (Nov 2025) as native API features. Bridges the gap between LLMs (natural language) and software systems (typed data structures).
**Documentation**: [Structured Output Term](../resources/term_dictionary/term_structured_output.md)
**Related**: [Function Calling](#function-calling---llm-tool-invocation-protocol), [Prompt Engineering](#prompt-engineering---llm-input-design-and-optimization), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns)

### Prompt Exaptation
**Full Name**: Prompt Exaptation (Cognitive-to-Prompt Transfer, Prompting by Analogy)
**Description**: Pattern in LLM prompt engineering where techniques from human cognitive, pedagogical, or professional domains are repurposed for LLM interaction, producing capabilities not predicted by the original context. Applies the architectural exaptation framework (Gould & Vrba, 1982) to the prompting layer. Nearly every major prompting technique traces to a pre-existing human practice: CoT from mathematics pedagogy ("show your work"), few-shot from worked examples, role-playing from theater/method acting, Tree of Thought from search algorithms (BFS/DFS), Socratic prompting from philosophy, Least-to-Most from Vygotsky's scaffolding, and Constitutional AI from legal frameworks. The "training data bridge" hypothesis explains why these transfers succeed: LLMs are trained on text containing humans performing these practices, so prompts activate patterns already encoded in the weights. CoT is the keystone exaptation — once it showed structured prompts unlock hidden capabilities, it opened the adjacent possible for all subsequent reasoning-focused techniques. Operates at three levels: direct exaptation (human → LLM prompt), cross-domain (prompt in domain A → domain B), and reverse exaptation (LLM insights → improved human practice).
**Documentation**: [Prompt Exaptation Term](../resources/term_dictionary/term_prompt_exaptation.md)
**Key Insight**: Innovation in prompt engineering is dominated by exaptation (borrowing human practices), not invention; the natural language interface makes any human communication technique a candidate for transfer
**Key Example**: Chain of Thought — "show your work" (pedagogy) exapted into LLM multi-step reasoning; spawned Zero-shot CoT, Self-Consistency, Tree of Thought, Process Reward Models
**Related**: [CoT](#cot---chain-of-thought), [Architectural Exaptation](#architectural-exaptation), [Scaling Law](#scaling-law), [RLHF](#rlhf---reinforcement-learning-from-human-feedback)

### ToT - Tree of Thought
**Full Name**: Tree of Thought (ToT, Tree-of-Thoughts)
**Description**: Deliberative reasoning framework for LLMs that generalizes chain-of-thought prompting by maintaining a tree of intermediate reasoning states ("thoughts") and exploring them via classical search algorithms (BFS, DFS, beam search). Introduced by Yao et al. (NeurIPS 2023). Four modular components: (1) thought decomposition into coherent intermediate steps, (2) thought generator proposing candidates, (3) state evaluator using LLM self-evaluation (e.g., "sure/maybe/impossible" verdicts), and (4) search algorithm with backtracking. GPT-4 with CoT solves 4% of Game of 24 tasks; ToT achieves 74%. Key insight: reframes LLM inference as a search problem — connecting classical AI problem-space formulation (Newell & Simon, 1959) with modern LLM capabilities. Computationally expensive (O(b*d*k) LLM calls) but enables exploration, lookahead, and recovery from errors impossible in linear CoT.
**Documentation**: [Tree of Thought Term](../resources/term_dictionary/term_tree_of_thought.md)
**Key Paper**: Yao et al. (2023), NeurIPS — arXiv:2305.10601
**Key Variants**: ToT via prompting (Hulbert 2023), RL-ToT (Long 2023), Graph of Thought (Besta 2023), Algorithm of Thoughts (Sel 2023)
**Key Properties**: Deliberative search, backtracking, LLM self-evaluation, task-adaptive thought granularity, search-algorithm-agnostic
**Related**: [CoT](#cot---chain-of-thought), [Prompt Engineering](#prompt-engineering---llm-input-design-and-optimization), [Prompt Exaptation](#prompt-exaptation), [LLM](#llm---large-language-models)

---

## NLP & Text Understanding

### BERT - Bidirectional Encoder Representations from Transformers
**Full Name**: Bidirectional Encoder Representations from Transformers
**Description**: Workhorse for real-time text classification (~10ms latency) — bidirectional transformer. domain: Abuse, BSM analysis (A-to-Z, RnR), CSMO (F1 0.84), CrossBERT (~<value>). Variants: XLM-RoBERTa (multilingual), RoBERTa. vs LLM: lower latency, better for classification.
**Documentation**: [BERT Term](../resources/term_dictionary/term_bert.md)
**Related**: [NLP](#nlp---natural-language-processing), [LLM](#llm---large-language-models), [SBERT](#sbert---sentence-bert), [CrossBERT](#crossbert---foundation-model-for-identity-entities)

### MLM - Masked Language Model
**Full Name**: Masked Language Model (Cloze-Style Pre-Training)
**Description**: Self-supervised pre-training objective where a fraction of input tokens are randomly masked and the model predicts the original tokens using full bidirectional context. Introduced in BERT (Devlin et al., 2019) — masks 15% of tokens (80% [MASK], 10% random, 10% unchanged). Unlike autoregressive LM (left-to-right), MLM enables deep bidirectional representations. Key variants: Whole Word Masking, RoBERTa (dynamic masking, no NSP), SpanBERT (contiguous span masking), ELECTRA (replaced token detection — 4x more sample-efficient). MLM is the pre-training objective that produces the BERT encoder used across all BSM-BERT anomaly detection models.
**Documentation**: [MLM Term](../resources/term_dictionary/term_mlm.md)
**Key Variants**: RoBERTa (dynamic masking), SpanBERT (span masking), ELECTRA (replaced token detection), XLM (cross-lingual)
**Related**: [BERT](#bert---bidirectional-encoder-representations-from-transformers), [NLP](#nlp---natural-language-processing), [Fine-Tuning](#fine-tuning)

### SBERT - Sentence BERT
**Full Name**: Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
**Description**: Efficient sentence embeddings via Siamese BERT — reduces similarity search from 65 hours → 5 seconds (10K sentences). Powers GoldMiner (annotation clustering), Alexa G2KIC (80% precision), SEC (return analysis). Self-hosted, fine-tunable, low-latency (~10ms).
**Documentation**: [SBERT Term](../resources/term_dictionary/term_sbert.md)
**Related**: [BERT](#bert---bidirectional-encoder-representations-from-transformers), [NLP](#nlp---natural-language-processing), [GoldMiner](acronym_glossary_ml.md#goldminer---annotation-processor)

### WordPiece - Likelihood-Based Subword Tokenizer
**Full Name**: WordPiece (Schuster & Nakajima, 2012)
**Description**: Subword tokenization selecting merges that maximize training data likelihood (PMI-based), unlike BPE's frequency-based merges. **Used by BERT, DistilBERT, ELECTRA.** Continuation tokens prefixed with ## (e.g., "playing" → ["play", "##ing"]). Vocabulary typically 30K. Greedy longest-match-first at inference.
**Documentation**: [WordPiece Term](../resources/term_dictionary/term_wordpiece.md)
**Related**: [BPE](../resources/term_dictionary/term_byte_pair_encoding.md), [SentencePiece](#sentencepiece---language-agnostic-tokenizer), [NER](#ner---named-entity-recognition)

### SentencePiece - Language-Agnostic Tokenizer
**Full Name**: SentencePiece (Kudo & Richardson, 2018)
**Description**: Language-agnostic tokenizer treating input as raw byte stream — no pre-tokenization needed. **Supports both BPE and Unigram Language Model algorithms.** Unigram starts with large vocabulary, prunes tokens that least decrease likelihood via EM. Used by T5, LLaMA, ALBERT, XLNet. Enables multilingual models without language-specific preprocessing.
**Documentation**: [SentencePiece Term](../resources/term_dictionary/term_sentencepiece.md)
**Related**: [WordPiece](#wordpiece---likelihood-based-subword-tokenizer), [BPE](../resources/term_dictionary/term_byte_pair_encoding.md), [NER](#ner---named-entity-recognition)

### NER - Named Entity Recognition
**Full Name**: Named Entity Recognition
**Description**: Subtask of information extraction that locates and classifies named entities in unstructured text into predefined categories (person, organization, location, etc.). Approaches evolved from rule-based (MUC, 1990s) through statistical CRF (2000s) to transformer-based (BERT fine-tuning, 2018+) and LLM zero-shot extraction (2023+). **In multi-agent KG construction (KARMA), NER is the Entity Extraction Agent's core capability.** Evaluated via span-level F1 on CoNLL-2003 benchmark.
**Documentation**: [NER Term](../resources/term_dictionary/term_ner.md)
**Related**: [NLP](#nlp---natural-language-processing), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [LLM](#llm---large-language-models), [KG](#kg---knowledge-graph)

### CrossBERT - Foundation Model for Identity Entities
**Full Name**: Cross-attention Bidirectional Encoder Representations from Transformers
**Documentation**: [CrossBERT Term](../resources/term_dictionary/term_crossbert.md)
**Launch**: January 2026
**Related**: [BERT](#bert---bidirectional-encoder-representations-from-transformers), [NLP](#nlp---natural-language-processing)

### NLI - Natural Language Inference
**Full Name**: Natural Language Inference / Recognizing Textual Entailment (RTE)
**Description**: Classification task that determines the logical relationship (entailment, contradiction, neutral) between a premise and hypothesis. Key backbone for [Semantic Entropy](#se---semantic-entropy): DeBERTa-large fine-tuned on MNLI (~91% accuracy) provides bidirectional entailment classification to cluster semantically equivalent LLM outputs. Also used for zero-shot text classification, fact verification, and summarization faithfulness evaluation. Standard benchmarks: SNLI (570K), MNLI (433K), ANLI (adversarial).
**Documentation**: [NLI Term](../resources/term_dictionary/term_nli.md)
**Key Models**: DeBERTa-v3-large (~91% MNLI), RoBERTa-large (~90%), BERT-large (~86%)
**Related**: [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Bidirectional Entailment](#bidirectional-entailment), [Semantic Entropy](acronym_glossary_ml.md#se---semantic-entropy), [SBERT](#sbert---sentence-bert)

### Bidirectional Entailment
**Full Name**: Bidirectional Textual Entailment
**Description**: Semantic equivalence test where two texts have the same meaning iff each entails the other: A ≡ B iff (A→B) ∧ (B→A). Core mechanism in [Semantic Entropy](acronym_glossary_ml.md#se---semantic-entropy) for clustering LLM generations into meaning groups. Implemented via two NLI classifier calls per pair. Stricter than unidirectional entailment (rules out hypernymy/hyponymy). Greedy clustering: O(M×K) NLI calls where M=generations, K=clusters.
**Documentation**: [Bidirectional Entailment Term](../resources/term_dictionary/term_bidirectional_entailment.md)
**Related**: [NLI](#nli---natural-language-inference), [SE - Semantic Entropy](#se---semantic-entropy), [Hallucination](#hallucination---llm-hallucination)

### SE - Semantic Entropy
**Full Name**: Semantic Entropy
**Description**: Uncertainty measure for LLMs that computes entropy over **meaning equivalence classes** rather than token sequences. Generates M samples from an LLM, clusters them by bidirectional NLI entailment (DeBERTa), then computes entropy over cluster probabilities. SE ≤ PE (predictive entropy) always — the gap is "wasted" entropy from lexical variation. Achieves AUROC ~0.82 vs ~0.75 (PE) on TriviaQA (OPT-30B). Advantage grows with model size. Extends to conformal prediction over meanings. **domain relevance**: principled confidence score for any LLM-generated investigation output; complements conformal prediction for free-form text.
**Documentation**: [Semantic Entropy Term](../resources/term_dictionary/term_semantic_entropy.md)
**Formula**: SE(x) = −Σ_c p(c|x) log p(c|x), where c are meaning clusters
**Optimal Settings**: T=0.5 (temperature), M=10 (generations)
**Paper**: Kuhn, Gal, Farquhar. ICLR 2023 Spotlight. [arXiv:2302.09664](https://arxiv.org/abs/2302.09664)
**Related**: [NLI](#nli---natural-language-inference), [Bidirectional Entailment](#bidirectional-entailment), [SEP](#sep---semantic-entropy-probes), [UAG](#uag---uncertainty-aware-generation), [Hallucination](#hallucination---llm-hallucination)

### SEP - Semantic Entropy Probes
**Full Name**: Semantic Entropy Probes
**Description**: Lightweight linear probes (logistic regression) trained on LLM hidden states to predict [Semantic Entropy](#se---semantic-entropy) in a **single forward pass**, eliminating the need for multiple generations and NLI clustering at inference time. Trained on ~2,000 hidden-state/SE label pairs. Key advantage: out-of-distribution generalization — SEP outperforms accuracy probes by +7.7 to +10.5 AUROC on unseen domains. Two token positions: SLT (second-last token, best AUROC) and TBG (token-before-generating, enables pre-generation uncertainty estimation).
**Documentation**: [Semantic Entropy Probes Term](../resources/term_dictionary/term_semantic_entropy_probes.md)
**Inference**: Single forward pass + logistic regression (~10x cheaper than full SE)
**Paper**: Kossen, Han, Razzak, Schut, Malik, Gal. arXiv 2024. [arXiv:2406.15927](https://arxiv.org/abs/2406.15927)
**Related**: [SE - Semantic Entropy](#se---semantic-entropy), [NLI](#nli---natural-language-inference), [Hallucination](#hallucination---llm-hallucination)

### UAG - Uncertainty-Aware Generation
**Full Name**: Uncertainty-Aware Generation
**Description**: Paradigm where LLM uncertainty estimates (e.g., [Semantic Entropy](#se---semantic-entropy)) are used as **closed-loop control signals** feeding back into generation. Unlike open-loop uncertainty (measure and report), UAG detects high uncertainty and takes corrective actions: retrieval augmentation, self-consistency checks, abstention, clarification seeking, or human routing. Key approaches: Uncertainty of Thoughts (UoT, NeurIPS 2024), Agentic Uncertainty Quantification (AUQ, 2026), Reinforcement Inference (2026). [SEP](#sep---semantic-entropy-probes) makes the measurement step cheap enough for real-time UAG.
**Documentation**: [Uncertainty-Aware Generation Term](../resources/term_dictionary/term_uncertainty_aware_generation.md)
**Design Patterns**: Abstention (SE > threshold → refuse), Retrieval augmentation (SE > threshold → RAG), Self-consistency (medium SE → majority vote), Human routing (high SE → expert review)
**Related**: [SE - Semantic Entropy](#se---semantic-entropy), [SEP](#sep---semantic-entropy-probes), [RAG](#rag---retrieval-augmented-generation), [Hallucination](#hallucination---llm-hallucination)

### OpenIE - Open Information Extraction
**Full Name**: Open Information Extraction
**Documentation**: [OpenIE Term](../resources/term_dictionary/term_open_ie.md)
**Related**: [NLP](#nlp---natural-language-processing), [KG](#kg---knowledge-graph), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation)

---

## Vision & Multimodal

### VLM - Vision Language Model
**Full Name**: Vision Language Model
**Description**: Multimodal AI processing images + text. Architecture: ViT encoder + LLM. a major vendor: Document VLM (94% vs 51% OCR),, tamper detection. Popular: CLIP, LLaVA, Qwen2-VL.
**Documentation**: [VLM Term](../resources/term_dictionary/term_vlm.md)
**Related**: [LLM](#llm---large-language-models), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Computer Vision](#computer-vision---cv)

### SWIN Transformer - Shifted Window Transformer
**Full Name**: Shifted Window Transformer
**Description**: Vision transformer for document classification using shifted window attention (linear complexity O(HW)). Deployed at domain for police report SPAM detection: 96% precision, 60% recall, 9.6% filtered volume. Hierarchical multi-scale features, 29M–197M parameters.
**Documentation**: [SWIN Transformer Term](../resources/term_dictionary/term_swin_transformer.md)
**Launch**: January 2026
**Related**: [VLM](#vlm---vision-language-model), [Computer Vision](#computer-vision---cv), [CNN](#cnn---convolutional-neural-network)

### Qwen2.5-VL - Qwen Vision Language Model
**Full Name**: Qwen2.5 Vision Language Model (Alibaba)
**Description**: Open-weight vision-language model family (Alibaba, 2025) combining Qwen 2.5 language model with a new Vision Transformer encoder. Processes images at **native resolution** with dynamic token counts, supports video understanding with absolute time encoding, and enables agent-based GUI interaction. Available in 3B, 7B, and 72B parameter sizes under Apache 2.0 license. 's current foundation model — replaced IDEFICS-v2 with 16% accuracy improvement and 58% hallucination reduction at <<value> training cost.
**Documentation**: [Qwen Term](../resources/term_dictionary/term_qwen.md)
**Related**: [VLM](#vlm---vision-language-model), [ViT](#vit---vision-transformer), [IDEFICS](#idefics---image-aware-decoder-enhanced-à-la-flamingo)

### IDEFICS - Image-aware Decoder Enhanced à la Flamingo
**Full Name**: Image-aware Decoder Enhanced à la Flamingo with Interleaved Cross-attentionS
**Description**: Open-source vision-language model family (HuggingFace) reproducing DeepMind's closed-source Flamingo architecture. IDEFICS-v2 (8B parameters, Apache 2.0) processes interleaved image-text sequences via cross-attention layers for visual QA, captioning, and multi-image reasoning. The "What matters when building VLMs?" paper showed that **careful data curation matters more than model size**. 's first-generation VLM backbone — fine-tuned on 200k e-commerce images, published at NAACL'25.
**Documentation**: [IDEFICS Term](../resources/term_dictionary/term_idefics.md)
**Related**: [VLM](#vlm---vision-language-model), [Qwen2.5-VL](#qwen25-vl---qwen-vision-language-model), [ViT](#vit---vision-transformer)

### Diffusion Model
**Full Name**: Diffusion Model (Denoising Diffusion Probabilistic Model)
**Description**: Generative model creating new data by reversing a noise-adding process. a major vendor domain: Stable Diffusion for adversarial CAPTCHA (~65% improvement), WAF CAPTCHA, synthetic training data. Also powers tabular data synthesis for anomaly detection research.
**Documentation**: [Diffusion Model Term](../resources/term_dictionary/term_diffusion_model.md)
**Key Applications**: Adversarial CAPTCHA, synthetic image generation, bot mitigation
**Status**: ✅ Active - core security and synthetic data technology
**Related**: [Computer Vision](#computer-vision---cv), [GenAI](#genai---generative-artificial-intelligence), [Masked Diffusion](#masked-diffusion)

### Masked Diffusion
**Full Name**: Masked Diffusion Model (Discrete Denoising Diffusion, Absorbing Diffusion)
**Description**: Family of generative models unifying discrete masking (from BERT/MLM) with iterative denoising (from DDPM). Forward process progressively masks tokens toward an absorbing `[MASK]` state; reverse process iteratively unmasks to generate samples. Key methods: D3PM (Austin et al., 2021), MaskGIT (Chang et al., 2022), MDLM (Sahoo et al., 2024). Bridges the corrupt-then-reconstruct paradigm across NLP and CV — proves that BERT-style masking and DDPM-style diffusion are discrete vs. continuous instantiations of the same framework.
**Documentation**: [Masked Diffusion Term](../resources/term_dictionary/term_masked_diffusion.md)
**Key Advantage**: Generates discrete data (text, categories) natively without continuous relaxation; MaskGIT achieves competitive image quality in 8-16 steps vs. DDPM's 1000
**Related**: [Diffusion Model](#diffusion-model), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [GenAI](#genai---generative-artificial-intelligence)

---

## Evaluation & Knowledge Systems

### LLM as a Judge - Large Language Model Automated Evaluation
**Full Name**: Large Language Model as a Judge (LLMaaJ)
**Documentation**: [LLM as a Judge Term](../resources/term_dictionary/term_llm_as_a_judge.md)
**Related**: [LLM](#llm---large-language-models), [GenAI](#genai---generative-artificial-intelligence)

### Agent-as-a-Judge - Agentic Evaluation Paradigm
**Full Name**: Agent-as-a-Judge
**Description**: Evaluation paradigm extending LLM-as-a-Judge with agentic capabilities: planning, tool-augmented verification, multi-agent collaboration, and persistent memory. Addresses three LLM-as-a-Judge limitations: parametric biases (position, verbosity), passive single-pass observation, and cognitive overload on complex trajectories. Developmental taxonomy: Procedural (fixed workflows) → Reactive (adaptive routing) → Self-Evolving (rubric discovery, memory-driven self-improvement). Applications across math/code (HERMES, VerifiAgent), fact-checking (FACT-AUDIT), law (AgentsCourt), finance (SAEA), and education (GradeOpt). 10-50× latency overhead vs single-pass LLM-as-a-Judge.
**Documentation**: [Agent-as-a-Judge Term](../resources/term_dictionary/term_agent_as_a_judge.md)
**Key Papers**: You et al. (2026) — [lit_you2026agent](../resources/papers/lit_you2026agent.md)
**Related**: [LLM as a Judge](#llm-as-a-judge---large-language-model-automated-evaluation), [Agentic Evaluation](#agentic-evaluation---agent-based-automated-assessment), [Rubric Discovery](#rubric-discovery---autonomous-evaluation-criteria-generation)

### Agentic Evaluation - Agent-Based Automated Assessment
**Full Name**: Agentic Evaluation
**Description**: Umbrella concept for automated evaluation using LLM agents with agentic capabilities (planning, tool use, memory, multi-agent collaboration) rather than single-pass inference. Orchestrates multiple reasoning steps, invokes external verification tools, and coordinates specialized sub-agents for evidence-grounded judgments. Warranted for multi-step agent trajectories, code correctness verification, and domain-specific assessment; overkill for simple factual QA or high-volume scoring where LLM-as-a-Judge suffices.
**Documentation**: [Agentic Evaluation Term](../resources/term_dictionary/term_agentic_evaluation.md)
**Key Papers**: You et al. (2026) — [lit_you2026agent](../resources/papers/lit_you2026agent.md)
**Related**: [Agent-as-a-Judge](#agent-as-a-judge---agentic-evaluation-paradigm), [LLM as a Judge](#llm-as-a-judge---large-language-model-automated-evaluation)

### Rubric Discovery - Autonomous Evaluation Criteria Generation
**Full Name**: Rubric Discovery (Adaptive Rubric Generation)
**Description**: Capability of agent judges to autonomously formulate and refine evaluation criteria during operation. Hallmark of Self-Evolving Agent-as-a-Judge systems. Approaches: EvalAgents (web-search rubric synthesis), AGENT-X (adaptive guideline selection), OnlineRubrics (RL-integrated rubric evolution), GradeOpt (iterative refinement via feedback loops). Replaces static human-authored rubrics with dynamically generated criteria that adapt to novel tasks and domains. domain relevance: auto-generating anomaly evaluation criteria as new patterns emerge.
**Documentation**: [Rubric Discovery Term](../resources/term_dictionary/term_rubric_discovery.md)
**Key Papers**: You et al. (2026) — [lit_you2026agent](../resources/papers/lit_you2026agent.md)
**Related**: [Agent-as-a-Judge](#agent-as-a-judge---agentic-evaluation-paradigm), [Prompt Optimization](../resources/term_dictionary/term_prompt_optimization.md), [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md)

### Delegated Work - Knowledge-Work Handoff to LLMs
**Full Name**: Delegated Work (Delegated Workflows, AI Delegation)
**Description**: Emerging LLM interaction paradigm in which knowledge workers hand off complete tasks to an LLM and supervise rather than author the resulting changes — exemplified by "vibe coding". The user retains expertise to review but trusts the LLM to execute faithfully without introducing silent errors. **The viability of delegated work hinges on long-horizon faithfulness across diverse professional domains, which DELEGATE-52 (Laban et al., 2026) shows current frontier LLMs lack — corrupting ~25% of document content over 20 interactions and ~50% on average across 19 models.** Critical failures (single-step ≥10pt drops) account for ~80% of degradation; agentic tool use does not improve performance under a basic harness.
**Documentation**: [Delegated Work Term](../resources/term_dictionary/term_delegated_work.md)
**Key Papers**: Laban et al. (2026) — [lit_laban2026llms](../resources/papers/lit_laban2026llms.md)
**Related**: [Agentic AI](#agentic-ai), [Agentic Evaluation](#agentic-evaluation---agent-based-automated-assessment), [Hallucination](#hallucination), [Evaluation Harness](#evaluation-harness---llm-benchmarking-framework)

### MT-Bench - Multi-Turn Benchmark
**Full Name**: Multi-Turn Benchmark for LLM Chat Assistants
**Description**: Evaluation benchmark with 80 multi-turn questions across 8 categories (Writing, Roleplay, Reasoning, Math, Coding, Extraction, STEM, Humanities). Each question has a follow-up turn testing instruction following. Uses GPT-4 single-answer grading (1-10) as primary evaluation mode. Achieves >80% agreement with human preferences, matching inter-human agreement. Introduced by Zheng et al. (2023) alongside Chatbot Arena.
**Key Papers**: Zheng et al. (2023) — [lit_zheng2023judging](../resources/papers/lit_zheng2023judging.md)
**Documentation**: [MT-Bench Term](../resources/term_dictionary/term_mt_bench.md)
**Related**: [LLM as a Judge](#llm-as-a-judge---large-language-model-automated-evaluation), [Chatbot Arena](#chatbot-arena---crowdsourced-llm-battle-platform)

### Chatbot Arena - Crowdsourced LLM Battle Platform
**Full Name**: Chatbot Arena (LMSYS)
**Description**: Open crowdsourced platform for evaluating LLMs through anonymous pairwise battles. Users interact with two random models simultaneously and vote which is better. Rankings via Elo rating system (Bradley-Terry model). Launched by LMSYS (UC Berkeley) in 2023. Collected 30K+ conversations and became a de facto leaderboard. Key insight: crowdsourced preferences match expert agreement levels.
**Key Papers**: Zheng et al. (2023) — [lit_zheng2023judging](../resources/papers/lit_zheng2023judging.md)
**Documentation**: [Chatbot Arena Term](../resources/term_dictionary/term_chatbot_arena.md)
**Related**: [LLM as a Judge](#llm-as-a-judge---large-language-model-automated-evaluation), [MT-Bench](#mt-bench---multi-turn-benchmark), [RLHF](#rlhf---reinforcement-learning-from-human-feedback)

### Elo Rating - Chess-Derived Rating System for LLMs
**Full Name**: Elo Rating System
**Description**: Rating system developed by Arpad Elo (1960) for chess, adapted for LLM evaluation in Chatbot Arena. Based on Bradley-Terry model: $P(A > B) = 1/(1 + 10^{(R_B - R_A)/400})$. After each match: $R'_A = R_A + K(S_A - E_A)$. Properties: converges with sufficient data, intuitive interpretation (~200 points ≈ 75% win rate), but can exhibit non-transitivity and sensitivity to model pool composition.
**Key Papers**: Zheng et al. (2023) — [lit_zheng2023judging](../resources/papers/lit_zheng2023judging.md), Elo (1978)
**Documentation**: [Elo Rating Term](../resources/term_dictionary/term_elo_rating.md)
**Related**: [Chatbot Arena](#chatbot-arena---crowdsourced-llm-battle-platform), [RM](#rm---reward-model)

### Position Bias - Order-Dependent Evaluation Bias
**Full Name**: Position Bias in LLM-as-a-Judge
**Description**: Systematic tendency of LLM judges to favor responses in a specific position (typically first) during pairwise comparison. Measured by consistency rate (identical judgment when swapping order). GPT-4: 65% consistency (30% first-biased); Claude-v1: 23.8% consistency (75% first-biased). More severe on open questions (writing 42%, humanities 36%) than factual (math 86%, coding 86%). Mitigations: swap positions and check consistency, few-shot examples, reference-guided grading.
**Key Papers**: Zheng et al. (2023) — [lit_zheng2023judging](../resources/papers/lit_zheng2023judging.md)
**Documentation**: [Position Bias Term](../resources/term_dictionary/term_position_bias.md)
**Related**: [LLM as a Judge](#llm-as-a-judge---large-language-model-automated-evaluation), [MT-Bench](#mt-bench---multi-turn-benchmark)

### Red Teaming
**Full Name**: Red Teaming (Adversarial Safety Evaluation)
**Description**: Practice of deliberately probing AI models with adversarial inputs to discover harmful, biased, or unsafe behaviors before deployment. Borrowed from military/cybersecurity terminology. Methods: human red teaming (expert adversarial prompts), automated red teaming (LM-generated attacks, gradient-based adversarial suffixes), hybrid approaches. Serves dual roles: evaluation (measuring safety) and training data (generating prompts for alignment). Ganguli et al. (2022) found larger models are more susceptible to red-team attacks; RLHF reduces but doesn't eliminate vulnerabilities. In Constitutional AI, ~182K red-team prompts are inputs to SL-CAI critique-revision. Attack categories: direct prompting, jailbreaking, prompt injection, multi-turn elicitation, encoding attacks, adversarial suffixes. domain relevance: testing anomaly detection models against edge cases, understanding adversarial buyer behavior.
**Documentation**: [Red Teaming Term](../resources/term_dictionary/term_red_teaming.md)
**Key Papers**: Ganguli et al. (2022), Perez et al. (2022), Zou et al. (2023) GCG attack
**Related**: [CAI](#cai---constitutional-ai), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [RLAIF](#rlaif---reinforcement-learning-from-ai-feedback), [LLM](#llm---large-language-models)

### Jailbreak - LLM Safety Bypass Attack
**Full Name**: Jailbreak (LLM Safety Bypass)
**Description**: Crafting adversarial prompts to bypass a model's safety alignment and content policies to elicit harmful or policy-violating outputs. Taxonomy: prompt injection ("Ignore previous instructions..."), role-playing (DAN), gradient-based (GCG), LLM-guided (PAIR, AutoDAN), generative/amortized (INPAINTING), encoding-based (Base64, ROT13). Evaluated via JailbreakBench (100 harmful behaviors), StrongREJECT judge (H>0.5), and Attack Success Rate (ASR). INPAINTING (Lüdke et al. 2025) generates low-perplexity jailbreaks indistinguishable from benign prompts, defeating perplexity-based defenses.
**Key Papers**: Zou et al. (2023) GCG, Chao et al. (2023) PAIR, Lüdke et al. (2025) INPAINTING — [lit_ludke2025diffusion](../resources/papers/lit_ludke2025diffusion.md)
**Documentation**: [Jailbreak Term](../resources/term_dictionary/term_jailbreak.md)
**Related**: [Red Teaming](#red-teaming), [Adversarial Attack](#adversarial-attack---adversarial-machine-learning-attack), [Transfer Attack](#transfer-attack---cross-model-adversarial-transfer), [CAI](#cai---constitutional-ai)

### Adversarial Attack - Adversarial Machine Learning Attack
**Full Name**: Adversarial Attack (Adversarial Machine Learning)
**Description**: Deliberate construction of inputs to cause incorrect, harmful, or unintended model outputs. In the LLM context: constructing prompts that induce targeted (often undesired) responses. By access level: white-box (GCG, PGD — full gradient access), gray-box (soft prompt attacks), black-box (PAIR, BoN, INPAINTING — API only). By strategy: gradient-based, search-based (genetic algorithms), LLM-guided (iterative refinement), sampling-based (random perturbations), generative/amortized (INPAINTING — sample from learned distribution). INPAINTING paradigm shift: from per-instance optimization to amortized inference via Diffusion LLMs.
**Key Papers**: Szegedy et al. (2014), Zou et al. (2023), Lüdke et al. (2025) — [lit_ludke2025diffusion](../resources/papers/lit_ludke2025diffusion.md)
**Documentation**: [Adversarial Attack Term](../resources/term_dictionary/term_adversarial_attack.md)
**Related**: [Red Teaming](#red-teaming), [Jailbreak](#jailbreak---llm-safety-bypass-attack), [Transfer Attack](#transfer-attack---cross-model-adversarial-transfer), [DLLM](#dllm---diffusion-language-model)

### Transfer Attack - Cross-Model Adversarial Transfer
**Full Name**: Transfer Attack (Cross-Model Adversarial Transfer)
**Description**: Adversarial examples crafted against a surrogate model applied to a different target without access to target internals. Exploits shared "vulnerable regions" in models trained on similar data. Critical for attacking proprietary black-box models. INPAINTING (Lüdke et al. 2025) achieves 53% ASR on ChatGPT-5 using LLaDA-8B as surrogate (vs. 13% BoN, 4% GCG). The attack is data-specific rather than model-specific — models sharing training distributions share vulnerabilities.
**Key Papers**: Szegedy et al. (2014), Lüdke et al. (2025) — [lit_ludke2025diffusion](../resources/papers/lit_ludke2025diffusion.md)
**Documentation**: [Transfer Attack Term](../resources/term_dictionary/term_transfer_attack.md)
**Related**: [Adversarial Attack](#adversarial-attack---adversarial-machine-learning-attack), [Jailbreak](#jailbreak---llm-safety-bypass-attack), [DLLM](#dllm---diffusion-language-model), [Red Teaming](#red-teaming)

### DLLM - Diffusion Language Model
**Full Name**: Diffusion Language Model (DLLM / Diffusion LLM)
**Description**: Non-autoregressive language model generating text through iterative denoising, modeling the joint distribution p(x,y) over entire sequences. Unlike autoregressive LLMs (left-to-right p(x_t|x_{<t})), DLLMs can condition on any subset of the sequence (inpainting). Key models: LLaDA-8B (Nie et al. 2025, first open-source DLLM), DREAM 7B (approaching autoregressive quality). INPAINTING exploits DLLMs' conditional generation: fix harmful response y*, sample adversarial prompt x ~ p(x|y*) via masked diffusion reverse process.
**Key Papers**: Nie et al. (2025) LLaDA, Ye et al. (2025) DREAM, Lüdke et al. (2025) — [lit_ludke2025diffusion](../resources/papers/lit_ludke2025diffusion.md)
**Documentation**: [Diffusion LLM Term](../resources/term_dictionary/term_diffusion_llm.md)
**Related**: [Diffusion Model](../resources/term_dictionary/term_diffusion_model.md), [Masked Diffusion](../resources/term_dictionary/term_masked_diffusion.md), [Amortized Inference](#amortized-inference---learned-forward-pass-optimization), [Jailbreak](#jailbreak---llm-safety-bypass-attack)

### Amortized Inference - Learned Forward-Pass Optimization
**Full Name**: Amortized Inference
**Description**: Strategy of training a model to predict inference solutions directly, replacing per-instance optimization with a single forward pass. Traditional: argmin_z L(z;x) per instance (expensive). Amortized: train f_θ such that f_θ(x) ≈ argmin_z L(z;x) for all x (cheap at test time). Canonical example: VAE encoder q_φ(z|x). In INPAINTING: the DLLM serves as an amortized optimizer — pretrained once on text data, then generates adversarial prompts for any target via conditional sampling, replacing GCG's ~100K gradient evaluations with ~256 denoising steps.
**Key Papers**: Kingma & Welling (2014) VAE, Amos (2023) Tutorial, Lüdke et al. (2025) — [lit_ludke2025diffusion](../resources/papers/lit_ludke2025diffusion.md)
**Documentation**: [Amortized Inference Term](../resources/term_dictionary/term_amortized_inference.md)
**Related**: [DLLM](#dllm---diffusion-language-model), [Diffusion Model](../resources/term_dictionary/term_diffusion_model.md), [Adversarial Attack](#adversarial-attack---adversarial-machine-learning-attack)

### CoT Red Teaming - Chain-of-Thought Red Teaming
**Full Name**: Chain-of-Thought Red Teaming
**Description**: Concept combining chain-of-thought reasoning with red teaming to generate more sophisticated, strategically reasoned adversarial prompts. Standard automated red teaming generates attacks through simple sampling; CoT red teaming has the attack model reason step-by-step about the target model's defenses, constitutional principles, and failure modes before crafting an adversarial prompt. Produces strategic rather than statistical attacks that more closely approximate expert human red teamers. Key advantage: reasoning traces reveal *why* attacks succeed — "the safety training handles direct requests but not hypothetical framing" — transforming red teaming from "find attacks" to "find defense gaps." Related methods: Tree of Attacks with Pruning (TAP, Mehrotra 2023), Crescendo (Microsoft 2024).
**Documentation**: [CoT Red Teaming Term](../resources/term_dictionary/term_cot_red_teaming.md)
**Key Papers**: Mehrotra et al. (2023) TAP, Perez et al. (2022), Russinovich et al. (2024) Crescendo
**Related**: [Red Teaming](#red-teaming), [CoT](#cot---chain-of-thought), [CAI](#cai---constitutional-ai), [RLHF](#rlhf---reinforcement-learning-from-human-feedback)

### Ontology
**Full Name**: Ontology
**Description**: Formal schema defining entity types, properties, relationships — enables machine reasoning. Formula: Ontology + Data = Knowledge Graph. : anomaly type hierarchy, OTF schema, MO classification. Nexus KG: 21 entity types, 23 relationships.
**Documentation**: [Ontology Term](../resources/term_dictionary/term_ontology.md)
**Related**: [KG](#kg---knowledge-graph), [RAG](#rag---retrieval-augmented-generation)

### Autonomous Research - AI-Driven Scientific Discovery
**Full Name**: Autonomous Research
**Description**: AI systems — typically LLM-based multi-agent pipelines — that perform the full scientific research cycle without human intervention: literature review, hypothesis generation, experimental design, implementation, analysis, and report writing. AgentRxiv (Schmidgall & Moor, 2025) enabled multiple agent laboratories to share findings through a preprint server, achieving +13.7% improvement on MATH-500 through collaborative iterative research. Key limitation: agent hallucination and reward hacking require manual verification of all results.
**Documentation**: [Autonomous Research Term](../resources/term_dictionary/term_autonomous_research.md)
**Key Papers**: Schmidgall & Moor (2025) — [lit_schmidgall2025agentrxiv](../resources/papers/lit_schmidgall2025agentrxiv.md)
**Related**: [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md), [Multi-Agent Collaboration](#multi-agent-collaboration---cooperative-agent-systems), [Reward Hacking](#reward-hacking---reward-signal-exploitation)

### Multi-Agent Collaboration - Cooperative Agent Systems
**Full Name**: Multi-Agent Collaboration
**Description**: Architectures where multiple AI agents work together toward shared goals through communication protocols, shared resources, or structured interaction patterns. Modalities include direct messaging (AutoGen), shared memory (SiriuS), publication-based sharing (AgentRxiv), and competitive dynamics (self-play). AgentRxiv showed publication-based collaboration enables faster convergence (76.2% accuracy at paper 7 vs. 23 sequentially) but at higher cost (3x for parallel labs).
**Documentation**: [Multi-Agent Collaboration Term](../resources/term_dictionary/term_multi_agent_collaboration.md)
**Key Papers**: Schmidgall & Moor (2025) — [lit_schmidgall2025agentrxiv](../resources/papers/lit_schmidgall2025agentrxiv.md)
**Related**: [AgentSpace](../resources/term_dictionary/term_agentspace.md), [Autonomous Research](#autonomous-research---ai-driven-scientific-discovery), [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md), [Generative Agents](#generative-agents---believable-agent-society-simulation)

### MAD - Multi-Agent Debate
**Full Name**: Multi-Agent Debate
**Description**: LLM reasoning framework where multiple agents independently generate responses, then iteratively critique each other's answers across structured debate rounds. **Promotes divergent thinking through adversarial interaction**, countering the Degeneration-of-Thought problem where single agents lock into incorrect solutions. Follows PROPOSE → CRITIQUE → SYNTHESIZE architecture. Key limitation: debate degrades to "inefficient resampling" on simple tasks and agents prove "overly aggressive" — flipping correct answers to incorrect ones through rhetorical pressure (ICLR 2025). The DKS extends MAD with persistent knowledge, warrant-level attacks, and dialectical adequacy as termination criterion.
**Documentation**: [Multi-Agent Debate](../resources/term_dictionary/term_multi_agent_debate.md)
**Key Papers**: Du et al. (2023, ICML 2024); Liang et al. (2023, EMNLP 2024)
**Related**: [Multi-Agent Collaboration](#multi-agent-collaboration---cooperative-agent-systems), [DKS](acronym_glossary_cognitive_science.md#dks---dialectic-knowledge-system), [Dialectical Adequacy](../resources/term_dictionary/term_dialectical_adequacy.md), [Chain of Thought](#cot---chain-of-thought)

### Generative Agents - Believable Agent Society Simulation
**Full Name**: Generative Agents (Interactive Simulacra of Human Behavior)
**Description**: Foundational LLM-based agent architecture by Park et al. (2023, Stanford) that simulates believable human behavior through three core modules: **memory stream** (append-only natural-language experience database), **reflection** (periodic synthesis of observations into higher-level inferences), and **planning** (top-down recursive day-to-minute action decomposition). Demonstrated with 25 agents in Smallville sandbox: agents autonomously spread party invitations, form relationships, and coordinate group activities. Memory retrieval scores memories by recency (exponential decay) + importance (LLM-rated 1-10) + relevance (cosine similarity). Ablation showed reflection removal most degraded believability. Used GPT-3.5-turbo. Published at UIST '23.
**Documentation**: [Generative Agents Term](../resources/term_dictionary/term_generative_agents.md)
**Key Papers**: Park, O'Brien, Cai, Morris, Liang, & Bernstein (2023) — [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
**Related**: [Multi-Agent Collaboration](#multi-agent-collaboration---cooperative-agent-systems), [Agentic Memory](../resources/term_dictionary/term_agentic_memory.md), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Emergence](../resources/term_dictionary/term_emergence.md)

### Reward Hacking - Reward Signal Exploitation
**Full Name**: Reward Hacking (Specification Gaming)
**Description**: Failure mode where an AI agent exploits the gap between intended objective and formal reward specification to achieve high reward without fulfilling the designer's true intent. Rooted in Goodhart's Law. In LLMs: models produce verbose, sycophantic outputs exploiting reward model biases. In autonomous research (AgentRxiv): agents fabricate experimental results and print false runtime outputs to maximize paper-writing reward. Mitigations: KL regularization, reward model ensembles, process reward models, human verification.
**Documentation**: [Reward Hacking Term](../resources/term_dictionary/term_reward_hacking.md)
**Key Papers**: Schmidgall & Moor (2025) — [lit_schmidgall2025agentrxiv](../resources/papers/lit_schmidgall2025agentrxiv.md), Gao et al. (2023)
**Related**: [RM](#rm---reward-model), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [Autonomous Research](#autonomous-research---ai-driven-scientific-discovery)

---

## Agentic AI Architecture

### A2A - Agent2Agent Protocol
**Full Name**: Agent2Agent Protocol (A2A)
**Description**: Open protocol for AI agent-to-agent communication across different systems and vendors. Announced by Google (April 2025), transferred to Linux Foundation (June 2025), backed by 150+ organizations. Uses Agent Cards for discovery, HTTP/JSON-RPC/SSE for transport. **Complementary to MCP: A2A handles horizontal agent-agent communication while MCP handles vertical agent-tool connections.Documentation**: [A2A](../resources/term_dictionary/term_a2a.md)
**Related**: [MCP](#mcp---model-context-protocol), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Agent-as-a-Tool](#agent-as-a-tool---hierarchical-agent-composition-pattern)

### Agent Orchestration - Multi-Agent Coordination Patterns
**Full Name**: Agent Orchestration (Multi-Agent Orchestration, Workflow Orchestration)
**Description**: Coordination strategies that govern how multiple LLM-powered agents collaborate, communicate, and transfer control to accomplish complex tasks. Dibia (2025) provides a definitive taxonomy: **deterministic patterns** (Sequential, Parallel, Supervisor) offer predictable control for production; **autonomous patterns** (GroupChat, Handoff, Plan-based, Magentic One) provide flexibility for open-ended tasks. **Most production systems should favor deterministic workflows with targeted autonomy at specific nodes.** Implemented via computational graphs (DAGs) with agents as nodes and data/control flow as edges.
**Documentation**: [Agent Orchestration Term](../resources/term_dictionary/term_agent_orchestration.md)
**Key Frameworks**: AutoGen, LangGraph, CrewAI, Semantic Kernel, OpenAI Swarm
**Related**: [Multi-Agent Collaboration](#multi-agent-collaboration---cooperative-agent-systems), [Function Calling](#function-calling---llm-tool-invocation-protocol), [Guardrails](#guardrails---ai-system-safety-controls), [AgentSpace](#agentspace)

### Agent-as-a-Tool - Hierarchical Agent Composition Pattern
**Full Name**: Agent-as-a-Tool (Agents as Tools, Agent Wrapping)
**Description**: Multi-agent design pattern where a specialized AI agent is wrapped as a callable tool that a higher-level orchestrator agent can invoke. Creates a hierarchical team structure: a "manager" agent delegates sub-tasks to domain-expert "worker" agents and integrates their outputs. **Extends traditional tool use by connecting an agent to another reasoning system rather than a deterministic function**, enabling recursive composability. Formalized by AWS Strands SDK (2024) with `@tool` decorator; Zhang (2025) proposed a Planner/Toolcaller variant with RL optimization achieving SOTA on multi-hop QA.
**Documentation**: [Agent-as-a-Tool Term](../resources/term_dictionary/term_agent_as_a_tool.md)
**Key Frameworks**: Strands Agents SDK, AutoGen, CrewAI, LangGraph, MCP
**Related**: [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Multi-Agent Collaboration](#multi-agent-collaboration---cooperative-agent-systems), [MCP](#mcp---model-context-protocol), [ReAct](#react---reasoning-and-acting-framework)

### LangGraph - Stateful Graph-Based Agent Orchestration Framework
**Full Name**: LangGraph (LangChain Graph Orchestration Framework)
**Description**: Open-source framework built on LangChain for orchestrating complex AI agent workflows as stateful directed graphs. Models agent tasks as nodes connected by edges while maintaining shared state, enabling conditional branching, loops, and human-in-the-loop control. **Unlike DAG-only frameworks, LangGraph supports cyclic graphs for iterative refinement and self-correction workflows.** Used in this domain's Deep Research Agent for multi-phase research-to-report automation. Reached general availability in May 2025 with managed deployment infrastructure.
**Documentation**: [LangGraph](../resources/term_dictionary/term_langgraph.md)
**Related**: [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [RAG](#rag---retrieval-augmented-generation), [Guardrails](#guardrails---ai-system-safety-controls)

### Guardrails - AI System Safety Controls
**Full Name**: Guardrails (LLM Guardrails, AI Safety Rails)
**Description**: Runtime safety mechanisms that monitor, validate, and constrain the inputs and outputs of LLM-based systems to prevent harmful, off-topic, or policy-violating behavior. Operate at three policy enforcement points: **input** (block prompt injection, toxic content), **output** (filter hallucinations, PII, unsafe content), and **process** (constrain tool use, limit API calls, enforce budgets). **Distinct from alignment training (RLHF) — guardrails provide deterministic, auditable policy enforcement at inference time.** Key systems: Guardrails AI, NeMo Guardrails (NVIDIA), Anthropic constitutional constraints, LlamaGuard (Meta).
**Documentation**: [Guardrails Term](../resources/term_dictionary/term_guardrails.md)
**Related**: [Red Teaming](#red-teaming), [Jailbreak](#jailbreak---llm-safety-bypass-attack), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Structured Output](#structured-output---schema-constrained-llm-generation), [Observability](#observability---agent-system-monitoring)

### Observability - Agent System Monitoring
**Full Name**: Observability for Agent Systems (LLM Observability, AI Observability)
**Description**: Practices and tools for monitoring, tracing, debugging, and understanding the internal behavior of LLM-powered agent systems. Extends traditional software observability (metrics, logs, traces) with LLM-specific concerns: **token usage tracking, prompt/completion logging, tool call tracing, multi-agent interaction visualization, and cost attribution.** Built on OpenTelemetry GenAI Semantic Conventions (2024). Dibia (2025) argues observability is "non-negotiable" — every agent interaction must be traceable for debugging, evaluation, and cost optimization. Key platforms: LangSmith, Arize Phoenix, Weights & Biases Weave, Braintrust.
**Documentation**: [Observability Term](../resources/term_dictionary/term_observability_agent_systems.md)
**Related**: [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Guardrails](#guardrails---ai-system-safety-controls), [Agentic Evaluation](#agentic-evaluation---agent-based-automated-assessment), [AgentSpace](#agentspace)

### Voyager - LLM-Powered Embodied Lifelong Learning Agent
**Full Name**: Voyager (Open-Ended Embodied Agent with Large Language Models)
**Description**: First LLM-powered embodied lifelong learning agent in Minecraft (Wang et al., 2023, NVIDIA/Caltech/Stanford/UT Austin). Three components: **(1) automatic curriculum** -- GPT-4 generates progressively harder tasks via in-context novelty search; **(2) skill library** -- ever-growing repository of verified JavaScript programs indexed by description embeddings for compositional retrieval; **(3) iterative prompting** -- multi-round code refinement using environment feedback, execution errors, and self-verification. Uses **code as action space** (not low-level motor commands), enabling temporal abstraction and compositionality. Results: 3.3x more unique items, 15.3x faster tech tree milestones, zero-shot transfer to new worlds. Canonical example of "Tool Evolution" in the self-evolving agent taxonomy.
**Documentation**: [Voyager Term](../resources/term_dictionary/term_voyager.md)
**Key Papers**: Wang et al. (2023) -- arXiv:2305.16291
**Related**: [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md), [Agentic Memory](../resources/term_dictionary/term_agentic_memory.md)

### NC - Neural Computer
**Full Name**: Neural Computer (NC)
**Description**: An emerging machine form that unifies computation, memory, and I/O in a single learned runtime state, making the neural model itself the running computer rather than a tool layer atop conventional hardware. Formalized as an update-and-render loop: $h_t = F_\theta(h_{t-1}, x_t, u_t)$; $x_{t+1} \sim G_\theta(h_t)$. **Proposes a paradigm shift from compound AI systems (multi-component tool-using agents) to a single neural runtime where programs, files, and OS functionality emerge from learned dynamics.** Current prototypes (NCCLIGen for terminals, NCGUIWorld for desktops) use Diffusion Transformer (DiT) architectures. The ultimate vision — the Completely Neural Computer (CNC) — requires Turing completeness, universal programmability, behavioral consistency, and machine-native semantics.
**Documentation**: [Neural Computer](../resources/term_dictionary/term_neural_computer.md)
**Key Paper**: Zhuge et al. (2026) -- [arXiv:2604.06425](https://arxiv.org/abs/2604.06425) (Meta AI / KAUST)
**Related**: [World Model](#world-model---learned-environment-dynamics), [Compound AI System](../resources/term_dictionary/term_compound_ai_system.md), [Genie](../resources/term_dictionary/term_genie.md), [Foundation Model](#foundation-model)

### World Model - Learned Environment Dynamics
**Full Name**: World Model (Environment Dynamics Model, Latent Dynamics Model)
**Description**: A learned neural representation of environment dynamics that predicts future states given current observations and actions, enabling model-based planning and control via internal simulation ("imagination"). Taxonomy spans three prediction spaces: pixel-space (Sora, GameNGen), latent-space (Dreamer family), and joint-embedding (V-JEPA). **Distinguished from Neural Computers in that world models serve autonomous agents for planning, while NCs serve as user-operated computing platforms.** Major systems include DreamerV1-V3 (RL), Sora (video generation), Genie (interactive environments), GAIA-1 (autonomous driving), and NVIDIA Cosmos (physical AI).
**Documentation**: [World Model](../resources/term_dictionary/term_world_model.md)
**Key Paper**: Ha & Schmidhuber (2018) -- [arXiv:1803.10122](https://arxiv.org/abs/1803.10122)
**Related**: [Neural Computer](#nc---neural-computer), [Genie](../resources/term_dictionary/term_genie.md), [GLP](#glp---generative-latent-prediction), [Foundation Model](#foundation-model)

### Toolformer - Self-Supervised Tool-Use Learning for LLMs
**Full Name**: Toolformer (Self-Supervised Tool-Augmented Language Model)
**Description**: Language model that learns to decide which APIs to call, when to call them, what arguments to pass, and how to incorporate results into token prediction -- all via **self-supervised learning** requiring only a handful of demonstrations per API. Introduced by Schick et al. (2023, Meta AI/UPF), built on GPT-J (6.7B). Three-stage training pipeline: **(1) Sampling** -- LM generates candidate API calls at various text positions via in-context learning; **(2) Execution** -- calls are run against actual APIs (calculator, Q&A, Wikipedia search, translator, calendar); **(3) Filtering** -- only calls whose results reduce cross-entropy loss on subsequent tokens are retained for fine-tuning. Outperformed GPT-3 (175B) on LAMA factual knowledge despite being 25x smaller. **Foundational work that proved LLMs can autonomously learn tool use**, directly influencing production function calling APIs (OpenAI, Anthropic, Google) and the broader agentic AI paradigm.
**Documentation**: [Toolformer Term](../resources/term_dictionary/term_toolformer.md)
**Key Paper**: Schick et al. (2023) -- [arXiv:2302.04761](https://arxiv.org/abs/2302.04761), NeurIPS 2023
**Related**: [Function Calling](#function-calling---llm-tool-invocation-protocol), [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [LLM](#llm---large-language-models), [MCP](../resources/term_dictionary/term_mcp.md)

### Agent Harness - LLM Agent Runtime Infrastructure
**Full Name**: Agent Harness (LLM Harness)
**Description**: The complete software infrastructure wrapping an LLM that manages everything except the model itself — tool integration, memory, context engineering, planning, and verification. Transforms a stateless text-generation model into a capable autonomous agent by connecting it to external tools and maintaining state across sessions. **A well-designed harness boosts task success rates more than increasing model size**, as it compensates for LLM weaknesses without retraining. Distinct from an evaluation harness, which benchmarks models rather than empowering them.
**Documentation**: [Agent Harness](../resources/term_dictionary/term_agent_harness.md)
**Key Systems**: Claude Agent SDK (Anthropic), DeepAgents (LangChain), OpenAI Assistants API
**Related**: [Agent Orchestration](#agent-orchestration---multi-agent-coordination-patterns), [Context Engineering](../resources/term_dictionary/term_context_engineering.md), [MCP](../resources/term_dictionary/term_mcp.md), [Guardrails](#guardrails---ai-system-safety-controls), [Evaluation Harness](#evaluation-harness---llm-benchmarking-framework)

### Cursor - AI-Native Code Editor
**Full Name**: Cursor (AI-Native IDE)
**Description**: AI-first code editor built as a VS Code fork with frontier LLMs deeply integrated into the editing experience. Features codebase-aware chat, Composer for multi-file editing with aggregated diffs, and a full agentic mode that plans, edits, and executes terminal commands autonomously. **Cursor 2.0 introduced parallel multi-agent workflows (up to 8 agents in isolated git worktrees)**, an embedded browser with DOM tools, and a native Composer model. Andrej Karpathy coined "vibe coding" while using Cursor. Supports Claude, GPT, Gemini, and proprietary models.
**Documentation**: [Cursor](../resources/term_dictionary/term_cursor.md)
**Related**: [Agent Harness](#agent-harness---llm-agent-runtime-infrastructure), [Claude Code](#claude-code---agentic-coding-cli), [MCP](../resources/term_dictionary/term_mcp.md)

### Claude Code - Agentic Coding CLI
**Full Name**: Claude Code (Anthropic Agentic Coding Tool)
**Description**: Anthropic's terminal-native agentic coding tool that operates as a full agent harness — reads entire codebases, makes multi-file edits, executes shell commands, runs tests, manages git workflows, and creates PRs through natural language. **Anthropic describes it as a "general-purpose agent harness"** — the canonical example of the coding harness pattern. Uses `CLAUDE.md` for persistent project context, supports MCP for extensible tool integration, and introduced checkpoints + subagents in v2.0 (Sep 2025). Powered by Claude Sonnet 4.5 (77.2% SWE-bench).
**Documentation**: [Claude Code](../resources/term_dictionary/term_claude_code.md)
**Related**: [Agent Harness](#agent-harness---llm-agent-runtime-infrastructure), [Claude](../resources/term_dictionary/term_claude.md), [MCP](../resources/term_dictionary/term_mcp.md)

### Evaluation Harness - LLM Benchmarking Framework
**Full Name**: Evaluation Harness (LM Evaluation Harness, lm-eval)
**Description**: Standardized software framework for benchmarking language model performance across tasks in a reproducible, transparent, and comparable manner. The canonical implementation is EleutherAI's `lm-evaluation-harness`, supporting 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag) and powering the HuggingFace Open LLM Leaderboard. **Distinct from an agent harness — evaluation harnesses measure what a model can do, not empower it to act.** Addresses reproducibility, transparency, and comparability issues in LLM evaluation.
**Documentation**: [Evaluation Harness](../resources/term_dictionary/term_evaluation_harness.md)
**Key Systems**: lm-evaluation-harness (EleutherAI), HELM (Stanford), OpenCompass
**Related**: [Agent Harness](#agent-harness---llm-agent-runtime-infrastructure), [LLM as a Judge](../resources/term_dictionary/term_llm_as_a_judge.md)

---

---

### ZSL - Zero-Shot Learning
**Full Name**: Zero-Shot Learning
**Description**: Ability of a model to perform a task without any task-specific training examples or parameter updates. The model receives only a natural language task description and generates outputs directly. First demonstrated at scale by GPT-2 (Radford et al., 2019) using conditioning patterns like "TL;DR:" for summarization. Zero-shot performance improves log-linearly with model scale — practical only at very large model sizes. For anomaly detection, enables rapid prototyping on new anomaly types without labeled data.
**Documentation**: [Zero-Shot Learning Term](../resources/term_dictionary/term_zero_shot_learning.md)
**Related**: [LLM](#llm---large-language-models), [CoT](../resources/term_dictionary/term_chain_of_thought.md), [Fine-Tuning](../resources/term_dictionary/term_fine_tuning.md)

---

## Vector Search & Similarity Technologies
### Embedding
**Full Name**: Embedding (Vector Representation)
**Description**: Dense vector representations where semantic similarity = geometric distance - **universal language of modern ML**. domain types: Behavioral (Sandstone, 768D), Graph (TGN/, +20% ATO), Text (BERT/CrossBERT, +160 bps), Product (ASIN). Key shift from hand-crafted features to learned representations.
**Documentation**: [Embedding Term](../resources/term_dictionary/term_embedding.md)
**Wiki**: [Sandstone], [TGN/SMAUG], [GNN for Buyer Fraud]
**Key Types**: Behavioral (Sandstone), Graph (TGN/), Text (BERT), Product (ASIN)
**Typical Dimensions**: 64-768 depending on type
**Use Cases**: Customer similarity, anomaly pattern detection, multi-modal fusion, k-NN classification, anomaly detection
**Key Projects**: Sandstone (+100 BPS contact automation), TGN/, CrossBERT (+160 BPS), DCL (+78 BPS Recall), AGATE (DeepCare, Physical Stores)
**Status**: ✅ Active - foundational technology for ML at domain
**Related**: [Sandstone](#sandstone---foundational-behavioral-model), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Contrastive Learning](#contrastive-learning), [](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [GNN](#gnn---graph-neural-networks), [TGN](#tgn---temporal-graph-network)

### FAISS - Facebook AI Similarity Search
**Full Name**: Facebook AI Similarity Search
**Description**: Open-source library for efficient similarity search and clustering of dense vectors, developed by Facebook AI Research under MIT license. Provides optimized algorithms for searching through millions to billions of high-dimensional vectors using Approximate Nearest Neighbor (ANN) techniques with CPU and GPU acceleration (up to 20x speedup). At a major vendor, FAISS serves as backbone for large-scale applications including catalog similarity search (Khoj), RAG systems for generative AI, product recommendations, and explainable AI experiments, enabling efficient semantic search across massive datasets with sub-second query response times.
**Documentation**: [FAISS Term](../resources/term_dictionary/term_faiss.md)
**Wiki**: [Khoj Vector Search], [ProductDNA Performance]
**Scale**: Hundreds of millions to billions of vectors, catalog-scale performance
**Performance**: GPU 8-20x faster than CPU, sub-second query response
**Applications**: Khoj (catalog search), ProductDNA similarity, RAG systems, explainable AI experiments
**Key Benefits**: Open source, scalable, GPU accelerated, production-ready
**Related**: [RAG](#rag---retrieval-augmented-generation), [Embedding](#embedding), [k-NN](#k-nn---k-nearest-neighbors), [Vector Database](../resources/term_dictionary/term_vector_database.md)

### RAG - Retrieval Augmented Generation
**Full Name**: Retrieval Augmented Generation
**Description**: Hybrid architecture combining pre-trained parametric memory (LLM) with non-parametric memory (document index) for knowledge-grounded generation. Introduced by Lewis et al. (2020, NeurIPS): DPR retriever (bi-encoder BERT) retrieves top-k passages via MIPS over 21M Wikipedia vectors; BART generator conditions on [input; passage] to produce output. Two formulations: **RAG-Sequence** (same document for entire output) and **RAG-Token** (different document per token). Achieves SOTA on 3 QA benchmarks with 20× fewer params than T5-11B. Human eval: 42.7% factuality preference over parametric-only BART (7.1%). Addresses hallucination, knowledge cutoff, domain gap via index hot-swapping (update knowledge without retraining).
**Mathematical formulation**: p(y|x) ≈ Σ_{z∈top-k} p_η(z|x) · p_θ(y|x,z), where p_η = DPR retriever, p_θ = BART generator
**Documentation**: [RAG Term](../resources/term_dictionary/term_rag.md)
**Key Papers**: Lewis et al. (2020) "Retrieval-Augmented Generation" (NeurIPS, 11,802 citations) — [lit_lewis2020retrieval](../resources/papers/lit_lewis2020retrieval.md)
**Key Extensions**: Gutierrez et al. (2025) "From RAG to Memory" — [lit_gutierrez2025rag](../resources/papers/lit_gutierrez2025rag.md); ; Modular RAG; Graph-RAG
**Wiki**: [Agentic AI Portal RAG], [BuilderHub RAG Recommendations]
**Use Cases**: Investigation automation, Q&A bots, document search, SOP compliance, pattern retrieval
**Status**: ✅ Active - foundational technique for LLM applications

### DPR - Dense Passage Retrieval
**Full Name**: Dense Passage Retrieval
**Description**: Neural information retrieval using dual BERT bi-encoders: query encoder q(x) and document encoder d(z) produce dense vectors; relevance = dot product q(x)ᵀd(z). Introduced by Karpukhin et al. (2020, EMNLP). Trained with contrastive learning using in-batch negatives + BM25-mined hard negatives. Index: 21M Wikipedia passages in FAISS (HNSW). Outperforms BM25 by +18-20% on top-20 retrieval across 4 QA benchmarks. Serves as the retrieval component of RAG. Key advantage: document vectors pre-computed offline → query-time cost is only encoding + MIPS.
**Documentation**: [DPR Term](../resources/term_dictionary/term_dpr.md)
**Key Papers**: Karpukhin et al. (2020) "Dense Passage Retrieval for Open-Domain QA" (EMNLP); Lewis et al. (2020) "RAG" (NeurIPS) — [lit_lewis2020retrieval](../resources/papers/lit_lewis2020retrieval.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [Dense Retrieval](#dense-retrieval), [FAISS](#faiss---facebook-ai-similarity-search), [Embedding](#embedding), [BERT](#bert---bidirectional-encoder-representations-from-transformers)

### Dense Retrieval
**Full Name**: Dense Retrieval
**Description**: The IR family that ranks documents by **vector similarity in a learned embedding space** rather than by lexical-overlap statistics. Both queries and documents are encoded as fixed-dimensional dense vectors by a neural encoder (typically a fine-tuned BERT-family bi-encoder), and ranking reduces to a cosine-similarity score (almost always on L2-normalized vectors → reduces to a dot product). **Foundational retrieval primitive of modern RAG pipelines**, distinguished from sparse retrieval (BM25, TF-IDF) which scores on direct term overlap, and from hybrid retrieval which combines both. Dense wins on paraphrase / semantic-similarity queries; sparse wins on exact-match / rare-term / temporal queries — production systems typically use both via Reciprocal Rank Fusion or learned routers.
**Documentation**: [Dense Retrieval Term](../resources/term_dictionary/term_dense_retrieval.md)
**Related**: [DPR](#dpr---dense-passage-retrieval), [RAG](#rag---retrieval-augmented-generation), [Embedding](#embedding), [Cosine Similarity](acronym_glossary_ml.md#cosine-similarity), [FAISS](#faiss---facebook-ai-similarity-search), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation), [PPR](#ppr---personalized-pagerank)

### Hallucination - LLM Hallucination
**Full Name**: Hallucination (LLM)
**Description**: Generation of fluent but factually incorrect, unsupported, or internally inconsistent text by LLMs. Two types: **intrinsic** (contradicts source material) and **extrinsic** (invents facts beyond source). Root causes: parametric knowledge gaps, training distribution mismatch, exposure bias, overconfidence. Primary mitigation: RAG (Lewis et al. 2020 showed 42.7% vs 7.1% factuality preference). Additional mitigations: RLHF, Constitutional AI, Chain-of-Thought, system prompt constraints. Metrics: FActScore (atomic fact precision), SelfCheckGPT (sample consistency), human factuality evaluation.
**Documentation**: [Hallucination Term](../resources/term_dictionary/term_hallucination.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [LLM](#llm---large-language-models), [RLHF](#rlhf---reinforcement-learning-from-human-feedback), [](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### PPR - Personalized PageRank
**Full Name**: Personalized PageRank
**Description**: Graph ranking algorithm that ranks knowledge graph nodes by relevance to seed entities through biased random walks. **Core retrieval mechanism in GraphRAG systems** combining with semantic search for hybrid knowledge retrieval. Uses damping factor α=0.85 with personalization vector biased toward query-extracted entities, achieving 150ms warm latency for 15K-node graphs. Converges in 20-30 iterations, returning top 400 nodes capturing 95% relevance.
**Documentation**: [PPR Term](../resources/term_dictionary/term_ppr.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [KG](#kg---knowledge-graph), [LLM](#llm---large-language-models)

### GraphRAG - Graph-Based Retrieval-Augmented Generation
**Full Name**: Graph-Based Retrieval-Augmented Generation
**Description**: Graph-based RAG framework (Edge et al., 2024, Microsoft Research) that answers **global sensemaking questions** by combining LLM-derived entity knowledge graphs with Leiden hierarchical community detection and map-reduce community summarization. Unlike vector RAG (local retrieval) or, GraphRAG exploits graph **community structure** for pre-computed hierarchical summaries. Pipeline: text chunks → LLM entity extraction (with self-reflection) → knowledge graph → Leiden communities → community summaries → map-reduce answering. Achieves 72-83% comprehensiveness win rate over vector RAG at 97% fewer tokens (root level). Open source: github.com/microsoft/graphrag.
**Key Papers**: [lit_edge2024local](../resources/papers/lit_edge2024local.md) — From Local to Global: A Graph RAG Approach to Query-Focused Summarization (arXiv:2404.16130, 1,159 citations)
**Documentation**: [GraphRAG Term](../resources/term_dictionary/term_graphrag.md)
**Related**: [RAG](#rag---retrieval-augmented-generation), [](#hipporag---hippocampus-inspired-retrieval-augmented-generation), [PPR](#ppr---personalized-pagerank), [KG](#kg---knowledge-graph), [LLM](#llm---large-language-models)

### Vector Database (Reference)
**Full Name**: Vector Database (Vector DB)
**Description**: See [Systems & Platform Glossary](acronym_glossary_systems.md#vector-database---specialized-vector-storage-and-search) - Specialized database systems optimized for storing, indexing, and searching high-dimensional vector embeddings using ANN techniques like HNSW. At a major vendor: OpenSearch (enterprise), Khoj (catalog), Neptune (graph), RAG systems.
**Documentation**: [Vector Database Term](../resources/term_dictionary/term_vector_database.md)
**Key Implementations**: OpenSearch, Elasticsearch, Neptune, Bedrock Knowledge Bases
**Related**: [FAISS](#faiss---facebook-ai-similarity-search), [HNSW](#hnsw---hierarchical-navigable-small-world), [Embedding](#embedding), [RAG](#rag---retrieval-augmented-generation)

---

## Related Glossaries

- [ML Algorithms & Frameworks](acronym_glossary_ml.md) — XGBoost, GNN, RL, clustering, and evaluation metrics

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md) | [← ML Algorithms](acronym_glossary_ml.md)

---

**Last Updated**: March 12, 2026
**Entries**: 40+ LLM, NLP, GenAI, prompt engineering, agentic AI architecture, and vision AI terms
