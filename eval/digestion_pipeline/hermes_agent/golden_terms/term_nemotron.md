---
tags:
  - resource
  - terminology
  - machine_learning
  - large_language_models
  - generative_ai
keywords:
  - Nemotron
  - NVIDIA Nemotron
  - nemotron-3-ultra
  - nemotron-3-super
  - NIM
  - open-weight model
topics:
  - foundation models
  - open-weight LLMs
  - reasoning models
  - agentic AI
language: markdown
date of note: 2026-06-20
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Nemotron - NVIDIA Open Foundation Model Family

## Definition

**Nemotron** is NVIDIA's family of open-weight foundation models built to advance
open frontier reasoning and agentic capabilities. Released under the broader
**Nemotron Coalition** — a group of AI labs (including Nous Research) collaborating
with NVIDIA on open foundation models — the family spans multiple sizes and tiers (e.g. `nemotron-3-super-120b-a12b`, `nemotron-3-ultra`). Nemotron models are distributed both as downloadable open weights and as hosted endpoints through NVIDIA's **NIM** (NVIDIA Inference Microservices) on [build.nvidia.com](https://build.nvidia.com), which expose an OpenAI-compatible chat-completions API.

Nemotron is relevant as one of the selectable inference providers in the [Hermes Agent](term_hermes_agent.md) CLI: Hermes wires NVIDIA NIM as a first-class provider (`provider: nvidia`) and also surfaces `nvidia/nemotron-3-ultra:free` via [Nous Portal](term_nous_portal.md). It therefore represents an open-weight alternative to closed frontier models ([Claude](term_claude.md) family) for the agentic and LLM-as-a-judge workflows.

## Context

- **Hermes Agent / Nous Portal**: Nemotron is a day-0-supported model in [Hermes Agent](term_hermes_agent.md). The provider docs document two paths — the NVIDIA NIM provider (`hermes chat --provider nvidia --model nvidia/nemotron-3-super-120b-a12b`, requiring `NVIDIA_API_KEY`) and a free-tier Nemotron 3 Ultra variant (`nvidia/nemotron-3-ultra:free`) routed through [Nous Portal](term_nous_portal.md).
- **NVIDIA NIM**: NIM hosts Nemotron (and other open models) with the same OpenAI-compatible API as a local NIM endpoint, so switching between cloud (`build.nvidia.com`) and on-prem (`NVIDIA_BASE_URL=http://localhost:8000/v1`, e.g. DGX Spark) is a one-line env-var change.
- **Training-data lineage**: NVIDIA used its NeMo Curator data-curation pipeline to prepare Nemotron training data — connecting Nemotron to the broader [synthetic data](term_synthetic_data.md) and data-curation tooling for open-model pretraining.
- **Comparison family**: Sits alongside other open-weight families surfaced in the same provider catalog ([DeepSeek](term_deepseek.md), Qwen, Llama) and Amazon's [Amazon Nova](term_amazon_nova.md) / [Bedrock](term_bedrock.md)-hosted models.

## Key Characteristics

- **Open-weight**: Distributed as downloadable weights plus hosted NIM endpoints, unlike closed API-only frontier models — enabling self-hosting for privacy or on-prem inference.
- **Sized tiers**: Multiple variants by parameter scale and capability tier; the `super` (e.g. `nemotron-3-super-120b-a12b`) naming follows the $\text{total-params}\,/\,\text{active-params}$ convention common to [Mixture-of-Experts (MoE)](term_moe.md) models, where only a subset of experts ($\approx 12\text{B}$ active of $\approx 120\text{B}$ total) fires per token:
  $$y = \sum_{i \in \mathcal{T}(x)} g_i(x)\, E_i(x)$$
  with $\mathcal{T}(x)$ the top-$k$ selected experts and $g_i$ the gating weights.
- **Reasoning / agentic focus**: Positioned for chain-of-thought reasoning and tool-calling agentic workflows, the same use pattern Hermes Agent exercises.
- **Transformer-based**: Like other modern LLMs it is a decoder-style [Transformer](term_transformer.md) and a [foundation model](term_foundation_model.md) adaptable to downstream tasks via prompting and fine-tuning.
- **OpenAI-compatible serving**: NIM exposes `/v1/chat/completions`, so any OpenAI-compatible client (Hermes, [vLLM](term_vllm.md)-style stacks) can target it without bespoke integration.
- **Billing-origin header**: Hermes auto-attaches a NIM billing-origin header on every `build.nvidia.com` request so consumption routes to the correct origin in NVIDIA's billing dashboard.

## Related Terms


## References
- [Run Nemotron 3 Ultra free in Hermes Agent (Hermes Agent docs)](https://hermes-agent.nousresearch.com/)
- [NVIDIA Build — NIM-hosted models](https://build.nvidia.com)
- [Nous Portal](https://portal.nousresearch.com)
- [NVIDIA Nemotron (Wikipedia / NVIDIA model family overview)](https://en.wikipedia.org/wiki/Nemotron)

---

**Last Updated**: 2026-06-20
**Status**: Active
