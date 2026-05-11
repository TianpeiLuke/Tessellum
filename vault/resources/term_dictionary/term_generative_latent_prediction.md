---
tags:
  - resource
  - terminology
  - world_model
  - generative_ai
  - latent_dynamics
  - llm
  - video_generation
keywords:
  - Generative Latent Prediction
  - GLP
  - PAN
  - world model
  - latent dynamics
  - autoregressive
  - video diffusion
  - action conditioning
  - latent space reasoning
topics:
  - World Models
  - Generative AI
  - Latent Space Reasoning
language: markdown
date of note: 2026-03-31
status: active
building_block: concept
---

# Generative Latent Prediction (GLP)

## Definition

**Generative Latent Prediction (GLP)** is a world model architecture introduced in PAN (Xiang et al., 2025) that separates world simulation into two components: (1) an **autoregressive latent dynamics backbone** based on a large language model that predicts future world states in a continuous latent space, conditioned on history and natural language actions, and (2) a **video diffusion decoder** that reconstructs perceptually detailed, temporally coherent visual observations from the predicted latent states.

GLP achieves a unification between **latent space reasoning (imagination)** — fast, abstract, leveraging LLM world knowledge — and **realizable world dynamics (reality)** — grounded, visually detailed, physically plausible. The key insight is that predicting the next latent state is computationally cheaper and more semantically meaningful than predicting the next pixel, while the diffusion decoder handles the expensive visual reconstruction only when needed.

## Key Properties

- **Separation of reasoning and rendering**: Latent dynamics (fast LLM inference) decoupled from visual reconstruction (expensive diffusion); each can be independently scaled
- **LLM as dynamics engine**: Pre-trained LLM encodes world knowledge from text, enabling open-domain dynamics prediction beyond training domains
- **Natural language action space**: Actions specified in natural language ("open the door," "turn left") rather than domain-specific encodings
- **Long-horizon consistency**: Autoregressive prediction in latent space accumulates errors more slowly than pixel-level prediction
- **Action-conditioned simulation**: Supports interactive "what if?" reasoning — predict consequences of hypothetical actions
- **Open-domain generalization**: LLM text knowledge provides priors for domains not directly seen during video training

## Architecture

| Component | Role | Implementation |
|-----------|------|----------------|
| **Visual encoder** | Encodes past observations into latent representations | Learned encoder mapping video frames to latent space |
| **Latent dynamics backbone** | Predicts next latent state $z_{t+1}$ from history $z_{1:t}$ and action $a_t$ | Pre-trained LLM fine-tuned for latent autoregression |
| **Video diffusion decoder** | Reconstructs visual observation $o_{t+1}$ from latent $z_{t+1}$ | Diffusion model generating temporally coherent video frames |
| **Action encoder** | Converts natural language actions to conditioning signal | LLM's native language understanding |

## Related Terms

- **[LLM](term_llm.md)**: Serves as the autoregressive latent dynamics backbone in GLP
- **[Foundation Model](term_foundation_model.md)**: LLM as a foundation for world modeling beyond text
- **[Transformer](term_transformer.md)**: Architecture of the LLM dynamics backbone
- **[Contrastive Learning](term_contrastive_learning.md)**: Related self-supervised approach; GLP uses generative prediction instead
- **[Zero-Shot Learning](term_zero_shot_learning.md)**: GLP aims for open-domain generalization via LLM world knowledge
- **[Scaling Law](term_scaling_law.md)**: GLP's two-component design allows independent scaling of dynamics and rendering
- **[World Model](term_world_model.md)**: GLP is a world model architecture that predicts in latent space rather than pixel space

## References

### Vault Sources

- [PAN Literature Note](../papers/lit_xiang2025pan.md) — Full paper digest with section notes
- [PAN Review](../papers/review_xiang2025pan.md) — OpenReview-style evaluation (Overall 6/10)

### External Sources

- [Xiang et al. (2025). "PAN: A World Model for General, Interactable, and Long-Horizon World Simulation." arXiv:2511.09057](https://arxiv.org/abs/2511.09057) — Paper introducing GLP
