---
tags:
  - resource
  - terminology
  - machine_learning
  - deep_learning
  - transfer_learning
  - few_shot_learning
keywords:
  - meta-learning
  - learning to learn
  - few-shot learning
  - transfer learning
  - model-agnostic meta-learning
  - MAML
  - rapid adaptation
topics:
  - Machine Learning
  - Deep Learning
  - Transfer Learning
language: markdown
date of note: 2026-03-04
status: active
building_block: concept
---

# Meta-Learning

## Definition

Meta-learning, often referred to as "learning to learn," is a machine learning paradigm that focuses on improving the learning process itself rather than optimizing for a specific task. The core idea is to enable a model to learn how to adapt to new tasks quickly and efficiently with minimal data by leveraging prior knowledge from related tasks. Unlike traditional machine learning which trains a model from scratch for each new task, meta-learning trains a model to become better at learning new tasks by exposing it to a distribution of related tasks during training.

A useful analogy: if you have been trained to fly a fighter jet, you don't need to start from scratch when learning to fly a Boeing 777—you leverage your prior flying knowledge to adapt quickly. Similarly, meta-learning models leverage patterns learned across many tasks to rapidly adapt to new, unseen tasks with just a few examples (few-shot learning) or even no examples (zero-shot learning).

## Context

Meta-learning is especially valuable in adversarial domains such as fraud and abuse prevention, where new attack patterns emerge constantly. Traditional ML approaches require substantial historical data and lengthy training cycles, making them slow to respond to new methods. Meta-learning addresses this by enabling rapid adaptation to new patterns, product launches, and low-data segments with minimal examples.

Typical applications include: (1) rapid detection at the early stages of a new business or product launch, before much labeled data has accumulated; (2) scalable adaptation across many related sub-tasks (for example, numerous payment methods or marketplaces) without maintaining a separate model for each; and (3) quick adaptation to emerging patterns. The approach is particularly useful for risky minority groups and cold-start scenarios where conventional models struggle due to limited data.

## Key Characteristics

- **Task Distribution Learning**: Trains on a distribution of related tasks rather than a single task, learning meta-knowledge that transfers across tasks
- **Rapid Adaptation**: Enables quick adaptation to new tasks with minimal data (few-shot) or no data (zero-shot)
- **Model-Agnostic**: Can be applied to various model architectures (neural networks, gradient boosting, etc.)
- **Prior Knowledge Leverage**: Explicitly learns how to leverage prior knowledge from related tasks for faster learning
- **Optimization-Based**: Often formulated as learning good initialization parameters that can be quickly fine-tuned
- **Metric-Based**: Alternative approaches learn embedding spaces where similar tasks cluster together
- **Memory-Augmented**: Some methods use external memory to store and retrieve task-specific knowledge
- **Episodic Training**: Training involves episodes where the model learns from support sets and is evaluated on query sets

## Performance / Metrics

- **Few-Shot Performance**: Achieves comparable accuracy to fully-trained models using only 5-10 examples per class
- **Adaptation Speed**: Substantially faster convergence than training a task-specific model from scratch
- **Data Efficiency**: Requires significantly less data for new task adaptation (orders of magnitude reduction)
- **Transfer Robustness**: Maintains performance even with distribution shift between source and target tasks
- **Early-Stage Detection**: Enables detection at the early stages of new business or product launches
- **Scalability**: A single meta-learned model can adapt to many related sub-tasks without retraining from scratch

## Related Terms

- **[Transfer Learning](term_transfer_learning.md)**: The general paradigm of leveraging knowledge from one task to improve learning on another; meta-learning is an advanced form of transfer learning
- **[LoRA](term_lora.md)**: Low-Rank Adaptation technique that can be combined with meta-learning for parameter-efficient adaptation to new tasks
- **[PEFT](term_peft.md)**: Parameter-Efficient Fine-Tuning methods that align with meta-learning's goal of rapid adaptation with minimal parameter updates
- **[Hypernetwork](term_hypernetwork.md)**: Neural networks that generate weights for other networks; can be used in meta-learning to generate task-specific parameters
- **[LLM](term_llm.md)**: Large Language Models that exhibit meta-learning capabilities through in-context learning and few-shot prompting

## References

- [Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (Finn et al., 2017)](https://arxiv.org/abs/1703.03400) - foundational MAML paper
- [Prototypical Networks for Few-shot Learning (Snell et al., 2017)](https://arxiv.org/abs/1703.05175) - metric-based meta-learning
- [Matching Networks for One Shot Learning (Vinyals et al., 2016)](https://arxiv.org/abs/1606.04080) - early few-shot meta-learning approach
- [Meta-Learning in Neural Networks: A Survey (Hospedales et al., 2020)](https://arxiv.org/abs/2004.05439) - comprehensive survey of meta-learning methods
