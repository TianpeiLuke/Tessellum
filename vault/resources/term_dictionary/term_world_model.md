---
tags:
  - resource
  - terminology
  - deep_learning
  - reinforcement_learning
  - generative_models
keywords:
  - world model
  - environment dynamics
  - latent dynamics model
  - model-based reinforcement learning
  - Dreamer
  - RSSM
  - Sora
  - Genie
  - interactive simulation
  - video prediction
topics:
  - Reinforcement Learning
  - Generative Models
  - AI Systems Architecture
language: markdown
date of note: 2026-04-18
status: active
building_block: concept
---

# World Model

## Definition

A **world model** is a learned neural representation of environment dynamics that predicts future states given current observations and actions. World models enable **model-based planning and control** by allowing agents to simulate outcomes internally ("imagination") before acting in the real environment — reducing the need for costly real-world interaction.

Formally, a world model approximates the transition dynamics $p(s_{t+1} | s_t, a_t)$ and optionally the reward $r(s_t, a_t)$ and observation model $p(o_t | s_t)$. The model can operate in **pixel space** (predicting raw frames), **latent space** (predicting compressed representations), or **joint-embedding space** (predicting in a learned representation without pixel decoding).

The term was popularized by Ha & Schmidhuber (2018), though the concept of "internal models" of the world traces back to Kenneth Craik (1943) and has roots in model-based RL, control theory, and cognitive science.

## Historical Development

| Year | System | Innovation |
|------|--------|-----------|
| **1990** | Dyna (Sutton) | Model-based RL using learned model for simulated experience |
| **2018** | World Models (Ha & Schmidhuber) | VAE + MDN-RNN for latent dynamics; coined the modern term |
| **2020** | DreamerV1 (Hafner et al.) | RSSM latent dynamics with actor-critic learning entirely in imagination |
| **2021** | DreamerV2 (Hafner et al.) | Discrete latent representations; Atari from pixels with 200M frames |
| **2023** | DreamerV3 (Hafner et al.) | Domain-general world model; mastered Minecraft diamonds without task-specific tuning |
| **2023** | GameNGen (Google) | Ran DOOM interactively via neural video generation at 20+ FPS |
| **2024** | Sora (OpenAI) | Large-scale video generation framed as world simulation |
| **2024** | Genie (DeepMind) | Interactive world model from unlabeled video; 11B parameters |
| **2024** | GAIA-1 (Wayve) | Autonomous driving world model from multimodal inputs |
| **2024** | V-JEPA (LeCun et al.) | Joint-embedding video prediction without pixel reconstruction |
| **2025** | Genie 2 (DeepMind) | 3D interactive environments from single images |
| **2025** | NVIDIA Cosmos | Foundation world models for physical AI and robotics |
| **2025** | UniSim (Google) | Universal simulator via video generation; actions → video |
| **2025** | Genesis (Meta) | Generative simulation platform for robotics and embodied AI |
| **2026** | V-JEPA 2 (Meta) | Scaling joint-embedding world models to action prediction |

## Taxonomy

### By Prediction Space

| Type | Predicts | Pros | Cons | Examples |
|------|----------|------|------|---------|
| **Pixel-space** | Raw video frames | Human-interpretable; rich output | Computationally expensive; wastes capacity on irrelevant details | Sora, GameNGen, Genie |
| **Latent-space** | Compressed state vectors | Efficient; focuses on dynamics | Requires learned encoder/decoder; latent space may miss details | Dreamer family, RSSM-based |
| **Joint-embedding** | Predicted representations without decoding | Avoids pixel-level reconstruction loss; captures semantics | Cannot generate visual output directly; harder to interpret | I-JEPA, V-JEPA, V-JEPA 2 |

### By Architecture

| Architecture | Mechanism | Key Example |
|-------------|-----------|-------------|
| **RSSM** (Recurrent State-Space Model) | Deterministic + stochastic latent states via GRU | DreamerV1-V3 |
| **Transformer** | Autoregressive sequence prediction over tokenized states | GATO, Genie |
| **Diffusion** | Denoising diffusion for frame generation conditioned on actions | Sora, GameNGen, UniSim |
| **VAE + RNN** | Variational encoding + recurrent dynamics | Ha & Schmidhuber (2018) |
| **Joint-embedding** | Contrastive/non-contrastive prediction in embedding space | V-JEPA, I-JEPA |

### By Application Domain

| Domain | Role of World Model | Leading Systems |
|--------|-------------------|----------------|
| **RL / Robotics** | Simulated rollouts for planning; data augmentation | Dreamer family, TD-MPC |
| **Video Generation** | Controllable video synthesis as "simulated worlds" | Sora, Runway Gen-3 |
| **Gaming** | Interactive environment simulation | GameNGen, Genie, Oasis |
| **Autonomous Driving** | Scenario generation, behavior prediction | GAIA-1, NVIDIA Cosmos |
| **Embodied AI** | Physical world simulation for training agents | Genesis, UniSim |

## Key Properties

- **Imagination**: Enables "thinking ahead" — agents can plan by simulating trajectories in the model before acting
- **Sample efficiency**: Model-based methods learn from fewer real interactions by generating synthetic experience
- **Transfer**: A single world model can support multiple tasks and policies via planning
- **Compositional prediction**: Good world models generalize to novel state-action combinations not seen in training
- **Uncertainty quantification**: Stochastic models (RSSM, VAE) represent predictive uncertainty, enabling risk-aware planning
- **Action-conditional**: Distinguished from pure video prediction by conditioning on actions — the model responds to agent decisions
- **Multi-scale dynamics**: Advanced models capture both fast (frame-to-frame) and slow (episode-level) dynamics

## Challenges and Limitations

1. **Compounding prediction error**: Model errors accumulate over long rollout horizons, degrading plan quality — the fundamental challenge of model-based RL
2. **Distribution shift**: The model is trained on data from one policy but must predict under a different (improving) policy
3. **Temporal consistency**: Video-based world models struggle to maintain physical consistency (object permanence, conservation laws) over time
4. **Computational cost**: High-fidelity pixel-space models (Sora, Genie) are extremely expensive to train and run
5. **Sim-to-real gap**: Models trained in simulation may not transfer to real-world dynamics
6. **Partial observability**: Real environments are partially observable; the model must maintain belief states over hidden variables
7. **Multi-modal dynamics**: Environments with discontinuous transitions (contact, collision, breaking) are difficult to model with smooth neural networks
8. **Reward modeling**: Learning reward functions alongside dynamics adds complexity; reward hacking is possible in imagined rollouts
9. **Evaluation**: No standard benchmark spans all world model capabilities (visual fidelity, action accuracy, long-horizon consistency)
10. **Hallucination**: Like LLMs, world models can generate plausible but physically impossible dynamics

## World Model vs Neural Computer

| Dimension | World Model | [Neural Computer](term_neural_computer.md) |
|-----------|-------------|---------------------------------------------|
| **System object** | Agent (acts autonomously) | Computer (operated by user) |
| **Purpose** | Predict environment for planning | Serve as a user-operated computing platform |
| **Interaction** | Agent queries model internally | Human interacts via I/O (keyboard, screen) |
| **Output** | State predictions for policy optimization | Rendered screen frames for human consumption |
| **State** | Environment dynamics model | Full computer runtime state |

## Related Terms

- **[Neural Computer](term_neural_computer.md)**: Extends the world model concept from environment simulation to user-operated computing — the model becomes the computer itself
- **[Reinforcement Learning](term_rl.md)**: Parent paradigm; world models enable model-based RL by simulating environment transitions
- **[MDP](term_mdp.md)**: The formal framework world models approximate — learning the transition kernel $P(s'|s,a)$
- **[Diffusion Model](term_diffusion_model.md)**: Video diffusion is increasingly used as the world model backbone for pixel-space prediction
- **[Foundation Model](term_foundation_model.md)**: Large-scale world models (Sora, Cosmos) are foundation models trained on internet-scale video data
- **[Generative Latent Prediction](term_generative_latent_prediction.md)**: Prediction in latent space without pixel decoding — the V-JEPA approach to world modeling
- **[Genie](term_genie.md)**: Interactive world model generating playable 2D/3D environments from video — a key prototype system
- **[SSM](term_ssm.md)**: State Space Models share the state-transition formalism $h_t = f(h_{t-1}, x_t)$ with RSSM-based world models
- **[Autoencoder](term_autoencoder.md)**: VAE encoders compress observations into the latent space where dynamics are learned
- **[RNN](term_rnn.md)**: Recurrent networks provide the sequential dynamics backbone for latent-space world models (GRU in RSSM)
- **[Compound AI System](term_compound_ai_system.md)**: World models can serve as a component within compound systems for planning and simulation
- **[Self-Supervised Learning](term_ssl.md)**: Many world models are trained via self-supervised prediction objectives (next-frame, next-latent)
- **[Agentic AI](term_agentic_ai.md)**: World models empower agentic systems with internal simulation for planning before acting

## References

### Vault Sources
- [Neural Computers (Zhuge et al., 2026)](../papers/lit_zhuge2026neural.md) — positions world models as one of four system objects in the NC taxonomy

### External Sources
- [Ha, D. & Schmidhuber, J. (2018). "World Models." arXiv:1803.10122](https://arxiv.org/abs/1803.10122) — foundational paper popularizing the term
- [Hafner, D. et al. (2020). "Dream to Control: Learning Behaviors by Latent Imagination." ICLR. arXiv:1912.01603](https://arxiv.org/abs/1912.01603) — DreamerV1
- [Hafner, D. et al. (2021). "Mastering Atari with Discrete World Models." ICLR. arXiv:2010.02193](https://arxiv.org/abs/2010.02193) — DreamerV2
- [Hafner, D. et al. (2023). "Mastering Diverse Domains through World Models." arXiv:2301.04104](https://arxiv.org/abs/2301.04104) — DreamerV3
- [Sutton, R.S. (1990). "Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming." *ICML 1990*](https://dl.acm.org/doi/10.5555/645524.657613) — Dyna architecture
- [Wikipedia: World model](https://en.wikipedia.org/wiki/World_model)
