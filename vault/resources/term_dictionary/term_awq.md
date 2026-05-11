---
tags:
  - resource
  - terminology
  - quantization
  - efficient_inference
  - model_compression
keywords:
  - AWQ
  - Activation-Aware Weight Quantization
  - weight quantization
  - salient channels
  - activation magnitudes
  - per-channel scaling
  - Int4
  - weight-only quantization
topics:
  - Efficient Inference
  - Model Quantization
language: markdown
date of note: 2026-03-16
status: active
building_block: concept
---

# AWQ (Activation-Aware Weight Quantization)

## Definition

**AWQ** (Activation-Aware Weight Quantization) is a weight-only post-training quantization method that identifies salient (important) weight channels by analyzing activation magnitudes rather than weight magnitudes. The key insight is that approximately 1% of weights are critical for preserving model quality -- specifically those in channels where the corresponding activations consistently exhibit large magnitudes during inference. Rather than using mixed-precision (keeping salient channels in FP16), AWQ protects these channels via per-channel scaling before quantization, which reduces their relative quantization error while maintaining a uniform low-bit representation that is hardware-friendly.

AWQ was introduced by Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han at MIT. The paper was published at MLSys 2024, where it received the **Best Paper Award**. The preprint is available as arXiv:2306.00978. AWQ achieves strong Int4 quantization quality with a simpler algorithm than alternatives like GPTQ -- it requires no backpropagation, no Hessian computation, and no layer-wise reconstruction, relying only on forward passes over a small calibration set.

The practical significance of AWQ lies in enabling large-scale LLM deployment on resource-constrained hardware. By compressing model weights to 4 bits with minimal accuracy loss, AWQ -- combined with the TinyChat inference engine -- enables models like Llama-2 70B to run on a single desktop GPU or even mobile devices. This positions AWQ as one of the most widely adopted weight quantization methods in the open-source LLM ecosystem, with native support in frameworks such as vLLM, HuggingFace Transformers, and TensorRT-LLM.

## Algorithm

AWQ is built on a sequence of observations that lead to an elegant per-channel scaling solution. The method operates on each linear layer independently, applying the same scaling-then-quantize pipeline across all attention projection matrices and MLP layers in the Transformer:

1. **Observation -- Not all weights are equal**: Skipping just 1% of salient weight channels (identified by activation magnitudes rather than weight magnitudes) during quantization preserves model quality even at aggressive bit-widths like Int3. Channels with consistently large activation magnitudes are disproportionately important because the product $w \cdot x$ is dominated by the activation magnitude.
2. **Problem with mixed-precision**: The naive fix -- keeping salient channels in FP16 while quantizing the rest (as in LLM.int8()) -- creates a mixed-precision layout that is hardware-unfriendly for weight-only quantization. Separate FP16 and Int4 GEMM kernels waste compute and complicate deployment.
3. **Solution -- Per-channel scaling**: Before quantization, multiply each salient weight channel by a scaling factor $s > 1$. This amplifies the weight values in that channel, reducing their *relative* quantization error (the ratio of quantization noise to signal). The corresponding activation channel is divided by $s$ to maintain mathematical equivalence: $y = (w \cdot s) \cdot (x / s) = w \cdot x$. The result is a uniform Int4 representation with no mixed-precision overhead.
4. **Optimal scale search**: AWQ performs a grid search over per-channel scaling factors to find the values that minimize the mean squared quantization error on a small calibration set (typically 128 samples). The search space is parameterized as $s = s_x^\alpha$ where $s_x$ is the per-channel activation magnitude and $\alpha \in [0, 1]$ controls scaling strength.
5. **No backpropagation**: Unlike GPTQ, which uses Hessian (second-order) information and iterative weight reconstruction, AWQ requires only forward passes for calibration. This makes quantization fast -- typically completing in minutes rather than hours for large models.

The mathematical equivalence of the scaling transformation ensures that the quantized model produces identical outputs to the original model in the absence of quantization noise. In practice, the per-channel scaling concentrates quantization noise on less important channels, where its impact on model outputs is minimal.

## Key Properties

- **Weight-only quantization** at Int4 (primary target) and Int3; activations remain in FP16 during inference
- **No backpropagation or reconstruction** -- only forward-pass calibration is needed
- **Fast quantization** -- minutes rather than hours for models up to 70B parameters
- **Hardware-friendly** -- uniform bit-width across all channels; no mixed-precision decomposition
- **Per-group quantization** with group size $g = 128$ for fine-grained scaling constants
- **Strong accuracy at Int4** -- matches or exceeds GPTQ on LLaMA and Llama-2 model families
- **Activation-magnitude-guided** saliency detection, more robust than weight-magnitude heuristics
- **Open-source implementation** available at [mit-han-lab/llm-awq](https://github.com/mit-han-lab/llm-awq) with TinyChat inference engine achieving 3x+ speedup over HuggingFace FP16

## Performance

On LLaMA and Llama-2 model families at Int4 (group size 128), AWQ consistently achieves lower perplexity than both Round-To-Nearest (RTN) quantization and GPTQ across model sizes from 7B to 70B parameters. For example, on LLaMA-2 7B, AWQ achieves WikiText-2 perplexity within 0.1-0.2 points of the FP16 baseline, outperforming GPTQ by a small but consistent margin.

AWQ demonstrates particular strength on instruction-tuned models and was the first method to successfully quantize multimodal LLMs (e.g., LLaVA). The TinyChat deployment framework built on AWQ enables the Llama-2 70B model to run on a single 48GB desktop GPU and even on mobile GPUs, achieving over 3x speedup compared to FP16 inference. AWQ also shows better robustness than GPTQ when the calibration data distribution diverges from the evaluation distribution, making it a safer default choice for production deployment.

## Comparison with GPTQ

Both AWQ and GPTQ are post-training weight quantization methods targeting Int4 with per-group scaling ($g = 128$), but they differ fundamentally in how they minimize quantization error:

| Dimension | AWQ | GPTQ |
|-----------|-----|------|
| **Approach** | Per-channel scaling guided by activation magnitudes | Layer-wise weight reconstruction using Hessian information |
| **What it optimizes** | Reduces relative quantization error of salient channels | Minimizes layer-wise output reconstruction error |
| **Calibration requirement** | Forward passes on ~128 samples | Forward passes + Hessian computation on ~128 samples |
| **Speed to quantize** | Minutes (no reconstruction loop) | Hours for large models (iterative per-column updates) |
| **Accuracy at Int4** | Strong; slightly better perplexity on average | Strong; comparable, sometimes better on specific tasks |
| **Hardware friendliness** | Uniform bit-width, no mixed-precision | Uniform bit-width, no mixed-precision |
| **Backpropagation needed** | No | No (but uses second-order Hessian approximation) |

## Challenges and Limitations

- **Weight-only quantization**: AWQ does not quantize activations, so it cannot exploit INT4/INT8 tensor-core arithmetic for the full GEMM; speedup comes primarily from reduced memory bandwidth for weight loading, which is the bottleneck in autoregressive decoding
- **Calibration data still required**: Although the calibration set is small (~128 samples), the choice of calibration data can affect quality, and distribution mismatch remains a risk
- **Does not address outlier activations directly**: Unlike SmoothQuant or LLM.int8(), AWQ does not explicitly handle activation outliers -- it only uses activation magnitudes as a signal for weight importance
- **Per-channel scaling overhead**: The scaling factors and group-wise quantization constants add a small storage overhead (~0.5 bits/param at $g = 128$)
- **Less explored at extreme low-bit**: AWQ's primary results are at Int4; performance at Int2 or sub-3-bit remains less validated compared to methods with explicit reconstruction
- **No task-specific adaptation**: The calibration optimizes for general language modeling loss; task-specific quantization quality (e.g., code generation, mathematical reasoning) may vary and is not explicitly optimized

## Related Terms

- [Quantization](term_quantization.md) -- parent concept covering all quantization techniques
- [QLoRA](term_qlora.md) -- alternative combining NF4 quantization with LoRA for memory-efficient fine-tuning
- [LoRA](term_lora.md) -- parameter-efficient fine-tuning method; can be applied on top of AWQ-quantized models
- [Knowledge Distillation](term_knowledge_distillation.md) -- alternative model compression via teacher-student training
- [Transformer](term_transformer.md) -- target architecture whose linear layers AWQ quantizes
- [GPTQ](term_gptq.md) -- alternative Int4 post-training quantization method using Hessian-based weight reconstruction
- [LLM.int8()](term_llm_int8.md) -- complementary Int8 mixed-precision method that handles both activations and weights
- [PTQ](term_ptq.md) -- the broader post-training quantization category that AWQ belongs to

## References

### Vault Sources

- [LLM.int8() Literature Note](../papers/lit_dettmers2022llm.md) -- Dettmers et al. (2022); foundational Int8 quantization work that identifies emergent outlier features, providing context for the quantization landscape AWQ operates in. AWQ's activation-magnitude analysis builds on the same observation that certain hidden dimensions are disproportionately important.

### External Sources

- Lin, J., Tang, J., Tang, H., Yang, S., Chen, W.-M., Wang, W.-C., Xiao, G., Dang, X., Gan, C., & Han, S. (2023). AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration. MLSys 2024 Best Paper. arXiv:2306.00978.
- AWQ GitHub Repository: [https://github.com/mit-han-lab/llm-awq](https://github.com/mit-han-lab/llm-awq)
- AWQ Project Page: [https://hanlab.mit.edu/projects/awq](https://hanlab.mit.edu/projects/awq)
- Lei Mao's AWQ Walkthrough: [https://leimao.github.io/blog/AWQ-Activation-Aware-Weight-Quantization/](https://leimao.github.io/blog/AWQ-Activation-Aware-Weight-Quantization/)
- Maarten Grootendorst -- Which Quantization Method is Right for You? (GPTQ vs. GGUF vs. AWQ): [https://newsletter.maartengrootendorst.com/p/which-quantization-method-is-right](https://newsletter.maartengrootendorst.com/p/which-quantization-method-is-right)
