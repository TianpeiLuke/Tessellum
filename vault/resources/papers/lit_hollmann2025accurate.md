---
tags:
  - resource
  - literature_note
  - machine_learning
  - tabular_data
  - foundation_models
  - transformer
  - small_data
keywords:
  - TabPFN
  - tabular foundation model
  - small data
  - transformer
  - synthetic data
  - gradient boosting
  - XGBoost
  - prior-data fitted network
  - few-shot learning
topics:
  - Machine Learning
  - Tabular Data
  - Foundation Models
  - Small Data Learning
domain: "Tabular ML"
paper_title: "Accurate predictions on small data with a tabular foundation model"
authors:
  - Noah Hollmann
  - Samuel G. Müller
  - Lennart Purucker
  - Arjun Krishnakumar
  - Max Körfer
  - Shi Bin Hoo
  - R. Schirrmeister
  - Frank Hutter
year: 2025
source: Nature
venue: "Nature"
DOI: "10.1038/s41586-024-08328-6"
arXiv: ""
semantic_scholar_id: "6b238b17e419c7dd3912b9845449496bfb0a571a"
zotero_key: ""
paper_id: hollmann2025accurate
status: active
language: markdown
building_block: hypothesis
date of note: 2026-03-07
---

# Accurate predictions on small data with a tabular foundation model

## Metadata

| Field | Value |
|-------|-------|
| **Paper** | Accurate predictions on small data with a tabular foundation model |
| **Authors** | Noah Hollmann, Samuel G. Müller, Lennart Purucker, Arjun Krishnakumar, Max Körfer, Shi Bin Hoo, R. Schirrmeister, Frank Hutter |
| **Year** | 2025 |
| **Venue** | Nature |
| **DOI** | 10.1038/s41586-024-08328-6 |
| **PubMed** | 39780007 |
| **Citations** | 618 (74 influential) |
| **Semantic Scholar** | 6b238b17e419c7dd3912b9845449496bfb0a571a |

## Abstract

Tabular data, spreadsheets organized in rows and columns, are ubiquitous across scientific fields, from biomedicine to particle physics to economics and climate science. The fundamental prediction task of filling in missing values of a label column based on the rest of the columns is essential for various applications as diverse as biomedical risk models, drug discovery and materials science. Although deep learning has revolutionized learning from raw data and led to numerous high-profile success stories, gradient-boosted decision trees have dominated tabular data for the past 20 years. Here we present the Tabular Prior-data Fitted Network (TabPFN), a tabular foundation model that outperforms all previous methods on datasets with up to 10,000 samples by a wide margin, using substantially less training time. In 2.8 s, TabPFN outperforms an ensemble of the strongest baselines tuned for 4 h in a classification setting. As a generative transformer-based foundation model, this model also allows fine-tuning, data generation, density estimation and learning reusable embeddings. TabPFN is a learning algorithm that is itself learned across millions of synthetic datasets, demonstrating the power of this approach for algorithm development. By improving modelling abilities across diverse fields, TabPFN has the potential to accelerate scientific discovery and enhance important decision-making in various domains.

## Table of Contents

| Section | Paper Note | Key Content |
|---------|-----------|-------------|
| **Introduction** | [paper_hollmann2025accurate_intro](paper_hollmann2025accurate_intro.md) | Problem: gradient-boosted trees dominate tabular data for 20 years; deep learning hasn't succeeded; need for better small-data methods |
| **Contribution** | [paper_hollmann2025accurate_contrib](paper_hollmann2025accurate_contrib.md) | TabPFN: transformer-based foundation model trained on 100M synthetic datasets; 2.8s training vs 4h baselines; generative capabilities |
| **Method** | [paper_hollmann2025accurate_model](paper_hollmann2025accurate_model.md) | Prior-data fitted network architecture; synthetic data generation with causal relationships; transformer-based prediction |
| **Experiment Design** | [paper_hollmann2025accurate_exp_design](paper_hollmann2025accurate_exp_design.md) | Benchmarks on datasets <10K samples; comparison with XGBoost, LightGBM, ensembles; evaluation on outliers and missing values |
| **Results** | [paper_hollmann2025accurate_exp_result](paper_hollmann2025accurate_exp_result.md) | Outperforms all baselines by wide margin; 50% data for same accuracy; excels on small tables, outliers, missing values |
| **Review** | [review_hollmann2025accurate](review_hollmann2025accurate.md) | OpenReview-style evaluation; 5 strengths, 5 weaknesses, 7 questions (5 review lenses applied) |

## Summary

<!-- VERIFY -->

**Introduction**: Tabular data is ubiquitous across scientific fields, but gradient-boosted decision trees (XGBoost, LightGBM) have dominated for 20 years while deep learning has failed to make significant inroads. The challenge is particularly acute for small datasets (<10,000 samples) with outliers and missing values, where existing algorithms are unreliable. The paper addresses the need for a method that can learn effectively from small tabular data without extensive hyperparameter tuning.

**Contribution**: TabPFN (Tabular Prior-data Fitted Network) is a transformer-based foundation model trained on 100 million synthetic datasets with causal relationships. It achieves superior performance in 2.8 seconds compared to 4-hour tuned ensembles. Unlike traditional methods, TabPFN is a "learning algorithm that is itself learned," demonstrating meta-learning at scale. The model supports fine-tuning, data generation, density estimation, and reusable embeddings, making it a true foundation model for tabular data.

**Method**: TabPFN uses a transformer architecture trained on synthetically generated tabular datasets where column relationships are causally linked. The training process teaches the model to evaluate various possible causal relationships and use them for predictions. The approach leverages prior-data fitting, where the model learns to make predictions by conditioning on the training data directly, similar to in-context learning in large language models.

**Results**: TabPFN outperforms all previous methods on datasets with up to 10,000 samples by a wide margin. It requires only 50% of the data to achieve the same accuracy as the previously best model. The method especially excels on small tables with fewer than 10,000 rows, many outliers, or a large number of missing values. Training time is reduced from hours to seconds while maintaining or improving accuracy.

## Relevance to Our Work

This paper is highly relevant to Buyer Abuse Prevention in the following ways:

- **[XGBoost](../term_dictionary/term_xgboost.md)**: TabPFN directly challenges XGBoost's dominance in tabular data, which is the primary algorithm used in BAP (~60% of production models). Could potentially replace or augment XGBoost for small-data scenarios.

- **Small Data Scenarios**: Many abuse detection use cases have limited labeled data (new fraud patterns, emerging abuse vectors, new payment methods). TabPFN's ability to work with <10K samples is directly applicable.

- **Rapid Training**: 2.8s training time enables rapid iteration and response to new threats, compared to hours for traditional hyperparameter tuning.

- **[Transfer Learning](../term_dictionary/term_transfer_learning.md)**: TabPFN's meta-learning approach aligns with BRP's need for rapid adaptation to new abuse patterns.

- **[Transformer](../term_dictionary/term_transformer.md)**: Demonstrates successful application of transformer architecture to tabular data, opening new possibilities for abuse detection.

- **[LightGBM](../term_dictionary/term_lightgbm.md)**: Outperforms LightGBM, another key algorithm in BRP's toolkit.

## Questions

1. How does TabPFN perform on imbalanced datasets typical in fraud detection (e.g., 1% abuse rate)?
2. Can TabPFN handle categorical features with high cardinality (e.g., customer IDs, product ASINs)?
3. What is the inference latency compared to PMML-deployed XGBoost models (<10ms requirement)?
4. Can TabPFN be deployed in AMES infrastructure for real-time scoring?
5. How does the model handle concept drift over time in adversarial environments?
6. Can the synthetic data generation approach be adapted to generate realistic fraud scenarios?
7. What is the maximum dataset size TabPFN can handle (paper focuses on <10K)?
8. How interpretable are TabPFN's predictions compared to tree-based models?

## Related Documentation

- [XGBoost](../term_dictionary/term_xgboost.md) - Current dominant algorithm in BAP that TabPFN outperforms
- [LightGBM](../term_dictionary/term_lightgbm.md) - Alternative gradient boosting method also outperformed by TabPFN
- [Transformer](../term_dictionary/term_transformer.md) - Architecture underlying TabPFN
- [Transfer Learning](../term_dictionary/term_transfer_learning.md) - Meta-learning paradigm that TabPFN exemplifies
- [LLM](../term_dictionary/term_llm.md) - Foundation models that inspired TabPFN's approach
- [Meta-Learning](../term_dictionary/term_meta_learning.md) - "Learning to learn" paradigm that TabPFN implements

## Domain Mappings

- **Problem Facet**: [map_hollmann2025accurate_problem](map_hollmann2025accurate_problem.md) - Small data challenges in buyer abuse (new stores, payment methods, emerging fraud)
- **Solution Facet**: [map_hollmann2025accurate_solution](map_hollmann2025accurate_solution.md) - Foundation model approach for transfer learning and few-shot detection
- **Data Facet**: [map_hollmann2025accurate_data](map_hollmann2025accurate_data.md) - Tabular feature integration with OTF and customer profiling

- [Term: TabPFN](../term_dictionary/term_tabpfn.md) — Tabular Prior-data Fitted Network
