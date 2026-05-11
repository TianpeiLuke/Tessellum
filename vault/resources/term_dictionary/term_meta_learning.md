---
tags:
  - resource
  - terminology
  - machine_learning
  - deep_learning
  - transfer_learning
  - few_shot_learning
  - buyer_risk_prevention
  - buyer_abuse_prevention
keywords:
  - meta-learning
  - learning to learn
  - few-shot learning
  - transfer learning
  - model-agnostic meta-learning
  - MAML
  - rapid adaptation
  - fraud prevention
topics:
  - Machine Learning
  - Deep Learning
  - Transfer Learning
  - Fraud Prevention
  - Buyer Risk Prevention
language: markdown
date of note: 2026-03-04
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/Users/chienluc/meta_learning/
---

# Meta-Learning

## Definition

Meta-learning, often referred to as "learning to learn," is a machine learning paradigm that focuses on improving the learning process itself rather than optimizing for a specific task. The core idea is to enable a model to learn how to adapt to new tasks quickly and efficiently with minimal data by leveraging prior knowledge from related tasks. Unlike traditional machine learning which trains a model from scratch for each new task, meta-learning trains a model to become better at learning new tasks by exposing it to a distribution of related tasks during training.

A useful analogy: if you have been trained to fly a fighter jet, you don't need to start from scratch when learning to fly a Boeing 777—you leverage your prior flying knowledge to adapt quickly. Similarly, meta-learning models leverage patterns learned across many tasks to rapidly adapt to new, unseen tasks with just a few examples (few-shot learning) or even no examples (zero-shot learning).

## Context

Meta-learning is increasingly important in Buyer Risk Prevention (BRP) and Buyer Abuse Prevention (BAP) at Amazon due to the adversarial nature of fraud and the constant emergence of new abuse patterns. Traditional ML approaches require substantial historical data and lengthy training cycles, making them slow to respond to new fraud methods. Meta-learning addresses this by enabling rapid adaptation to new abuse vectors, payment methods, and business launches with minimal data.

Within BRP, meta-learning is being explored for: (1) rapid MO/fraud prevention at early stages (e.g., branded gift card launches in EU stores), (2) scalable solutions for new payment method launches (20+ Alternative Payment Methods across 24+ Amazon stores), and (3) quick adaptation to emerging fraud patterns without maintaining separate models for each abuse vector. The approach is particularly valuable for handling risky minority groups and new business launches where traditional FARM models struggle due to limited data.

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
- **Adaptation Speed**: 5x faster convergence compared to vanilla RL agents in BRP experiments
- **Data Efficiency**: Requires significantly less data for new task adaptation (orders of magnitude reduction)
- **Transfer Robustness**: Maintains performance even with distribution shift between source and target tasks
- **Early-Stage Detection**: Enables fraud prevention at early stages of new business launches (e.g., EU BGC launch)
- **Scalability**: Single meta-learned model can adapt to 20+ new payment methods without retraining from scratch

## Related Terms

- **[Transfer Learning](term_transfer_learning.md)**: The general paradigm of leveraging knowledge from one task to improve learning on another; meta-learning is an advanced form of transfer learning
- **[LoRA](term_lora.md)**: Low-Rank Adaptation technique that can be combined with meta-learning for parameter-efficient adaptation to new tasks
- **[PEFT](term_peft.md)**: Parameter-Efficient Fine-Tuning methods that align with meta-learning's goal of rapid adaptation with minimal parameter updates
- **[Hypernetwork](term_hypernetwork.md)**: Neural networks that generate weights for other networks; can be used in meta-learning to generate task-specific parameters
- **[LLM](term_llm.md)**: Large Language Models that exhibit meta-learning capabilities through in-context learning and few-shot prompting

## References

- [Meta-Learning Expansion in Buyer Risk Prevention](https://w.amazon.com/bin/view/Users/chienluc/meta_learning/) - Internal wiki page on meta-learning applications in BRP
- [BRP ML Research Weekly 2023](https://w.amazon.com/bin/view/BRPMLResearchWeeklyMeeting/2023/) - Research presentations including transfer learning and multi-task learning approaches
- [BRP Learn and Be Curious Expo Q4 2022](https://w.amazon.com/bin/view/BRP_and_Core_Service_Learn_and_Be_Curious_Expo_-_Q42022/Presenters/) - Presentations on transfer, federated, and few-shot learning
- [COAP: Context Enhanced Buyer Abuse Prevention](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_BuyerSellerMessaging/BSM_Prods_Roadmap/) - Project using zero-shot and few-shot learning for abuse detection
