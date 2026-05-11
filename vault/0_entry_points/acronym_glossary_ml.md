---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - glossary
  - machine_learning
  - algorithms
keywords:
  - machine learning
  - deep learning
  - algorithms
  - models
  - ML techniques
  - Algorithms to Live By
  - Brian Christian
  - Tom Griffiths
  - optimal stopping
  - 37% rule
  - scheduling algorithms
  - LRU cache
  - game theory
  - Nash equilibrium
  - mechanism design
  - satisficing
  - bounded rationality
  - overfitting
  - simulated annealing
  - relaxation
  - sorting algorithms
  - exponential backoff
topics:
  - ML algorithms
  - deep learning
  - model architectures
  - optimization
  - foundational algorithms
language: markdown
date of note: 2026-01-24
status: active
building_block: navigation
---

# Machine Learning Glossary

**Purpose**: Quick reference for machine learning algorithms, techniques, model architectures, and evaluation metrics used in buyer abuse prevention.

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md)

---

## ML Automation & Parsing

### ML Automation
**Full Name**: ML Automation
**Description**: Tools, processes, and systems that automate the machine learning lifecycle from data preparation through model deployment and monitoring. In BAP, ML automation encompasses automated model retraining pipelines, automated rule calibration (ARC), and automated UDV generation. **Reduces manual toil** so data scientists can focus on research rather than repetitive operational tasks.
**Documentation**: [ML Automation Term](../resources/term_dictionary/term_ml_automation.md)
**Related**: [Rule Optimization](../resources/term_dictionary/term_rule_optimization.md), [XGBoost](#xgboost), [Continual Learning](../resources/term_dictionary/term_continual_learning.md)

### AST - Abstract Syntax Tree
**Full Name**: Abstract Syntax Tree
**Description**: Tree representation of the abstract syntactic structure of rule expressions enabling programmatic analysis for ML automation systems. Critical component of ARROW Everywhere's enhanced parser capabilities, constructing hierarchical representations of rule conditions for automated threshold calibration and optimization. Increased ruleset parsing coverage from 45% to 100% through deterministic parsing of nested expressions, UDV chains, and complex patterns that enable sophisticated ML-driven rule optimization workflows.
**Documentation**: [AST Term](../resources/term_dictionary/term_ast.md)
**Wiki**: https://w.amazon.com/bin/view/RMP/
**Related**: [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md), [Rule Optimization](../resources/term_dictionary/term_rule_optimization.md), [RMP](../resources/term_dictionary/term_rmp.md), [UDV](../resources/term_dictionary/term_udv.md), [ML Automation](../resources/term_dictionary/term_ml_automation.md)

### BPE - Byte Pair Encoding
**Full Name**: Byte Pair Encoding
**Description**: Subword tokenization algorithm that iteratively merges the most frequent adjacent symbol pairs, producing a vocabulary between character-level and word-level. GPT-2 introduced **byte-level BPE** (base vocabulary: 256 bytes) with character-category boundary enforcement, enabling tokenization of any text without `<UNK>` tokens. Compression: ~3.5 chars/token (GPT-2, 50K vocab). BPE tokenizer choice affects perplexity comparability across models. Non-English languages face higher fertility (more tokens/word), consuming more context budget.
**Documentation**: [Byte Pair Encoding Term](../resources/term_dictionary/term_byte_pair_encoding.md)
**Related**: [BERT](../resources/term_dictionary/term_bert.md), [Embedding](../resources/term_dictionary/term_embedding.md), [Perplexity](#ppl---perplexity)

---

## ML Algorithms & Frameworks

### ML System Complexity Score
**Full Name**: ML System Complexity Score
**Description**: A BRP metric measuring overall ML system complexity through normalized structural and operational scores. **Quantifies model count, feature count, ruleset complexity, retraining frequency, and monitoring burden to evaluate simplification impact.** Includes a QuickSight dashboard for trend tracking and an R Shiny simulator for what-if analysis of proposed consolidation actions.
**Documentation**: [ML System Complexity Score](../resources/term_dictionary/term_ml_system_complexity_score.md)
**Related**: [Global Modeling](#global-modeling), [Consortium Model](#consortium-model)

### Pangaea
**Full Name**: Pangaea (Global Modeling Feature Engineering Project)
**Description**: A BRP project providing foundational feature engineering techniques for global/consortium modeling. **Its two core contributions are currency conversion (mapping local-currency features to a common currency) and cross-border variables (indicators identifying international orders).** These techniques directly reduce feature-level conflicts that degrade consortium model performance. Widely adopted across NA SQ, CSSW, Amazon Pay, and other BRP consortium models.
**Documentation**: [Pangaea](../resources/term_dictionary/term_pangaea.md)
**Related**: [Global Modeling](#global-modeling), [Conflict Measurement](#conflict-measurement)

### AmazonBoost
**Full Name**: AmazonBoost (Conflict-Aware Gradient Boosting)
**Description**: A conflict-aware gradient boosted decision tree algorithm that handles domain conflicts during multi-domain model training. Introduces a Conflict Index measuring gradient disagreement between domains and projects conflicting gradients onto a common direction. **Built on LightGBM, it extends standard GBDT to prevent one domain from dominating training in global/consortium models.** Deployed in Amazon Pay global model.
**Documentation**: [AmazonBoost](../resources/term_dictionary/term_amazonboost.md)
**Related**: [Conflict Measurement](#conflict-measurement), [LightGBM](#lightgbm)

### Conflict Measurement
**Full Name**: Conflict Measurement (Feature/Domain Level)
**Description**: A quantitative framework for analyzing why global models lose performance when combining data from multiple domains. Measures the L1 distance between conditional distributions p(y|x) across domain pairs for each feature. **Produces feature-level and domain-level conflict vectors that identify harmful features and incompatible domains.** Validated on NA SQ (4 countries) and CSSW (13 countries) datasets. Complements AmazonBoost's gradient-level Conflict Index.
**Documentation**: [Conflict Measurement](../resources/term_dictionary/term_conflict_measurement.md)
**Related**: [Global Modeling](#global-modeling), [Consortium Model](#consortium-model)

### Consortium Model
**Full Name**: Consortium Model
**Description**: A single ML model trained on combined data from multiple domains (regions, business concepts, or pipelines) to serve all simultaneously. At BRP, consortium models replace dedicated per-domain models to reduce operational complexity. **The key distinction from federated learning is that training data is centralized, producing one unified model artifact.** Notable BRP examples include ERA, DeepCARE EU, CSSW (13 countries), and Physical Stores cross-concept models.
**Documentation**: [Consortium Model](../resources/term_dictionary/term_consortium_model.md)
**Related**: [Global Modeling](#global-modeling), [Ensemble Learning](#ensemble-learning)

### OCR - Optical Character Recognition
**Full Name**: Optical Character Recognition
**Description**: Technology converting images of text into machine-readable text. In BAP, extracts information from police reports, ID documents, and invoices for automated validation. **Uses Amazon Textract (primary), Cairo (template-based ID), and Tesseract (open-source)** with NER for structured field extraction.
**Documentation**: [OCR Term](../resources/term_dictionary/term_ocr.md)
**Related**: [Computer Vision](../resources/term_dictionary/term_computer_vision.md), [Nile](../resources/term_dictionary/term_nile.md)

### GAN - Generative Adversarial Network
**Full Name**: Generative Adversarial Network
**Description**: Deep learning architecture with generator and discriminator networks trained in competition. In BAP, relevant as both threat (fake documents/images) and tool (data augmentation, anomaly detection). **Generator produces synthetic data while discriminator distinguishes real from fake.**
**Documentation**: [GAN Term](../resources/term_dictionary/term_gan.md)
**Related**: [Deep Learning](../resources/term_dictionary/term_deep_learning.md), [GenAI](../resources/term_dictionary/term_genai.md)

### Global Modeling
**Full Name**: Global Modeling / Regional Modeling
**Description**: The practice of consolidating multiple domain-specific ML models into a single model serving multiple geographical regions or business domains. At BRP, global modeling aims to reduce pipeline complexity while detecting cross-boundary fraud patterns. **The central challenge is handling "conflicts" — when the same feature has different predictive relationships across domains.** Approaches include currency conversion, cross-border variables, domain identifiers, and representation alignment.
**Documentation**: [Global Modeling](../resources/term_dictionary/term_global_modeling.md)
**Related**: [Guide: Global Modeling Playbook](../resources/policy_sops/guide_global_modeling_playbook.md), [XGBoost](#xgboost), [LightGBM](#lightgbm)

### XGBoost
**Full Name**: eXtreme Gradient Boosting
**Description**: **Dominant algorithm in BAP (~60% production models)** for tabular abuse detection. Native PMML = ultra-low latency (<10ms) via AMES. Key differentiator vs LightGBM: level-wise growth (lower overfitting), more stable for noisy labels. Infrastructure: DAWS (one-click), MODS (SageMaker).
**Documentation**: [XGBoost Term](../resources/term_dictionary/term_xgboost.md)
**Wiki**: [DAWS Integration](https://w.amazon.com/bin/view/CMLS/ME/IntegrateXGBoostModelToDAWS/), [DAWS Auto-Refresh](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/DAWS_AutoRefresh_Setup/)
**Use Cases**: Binary abuse classification, ranking, risk scoring
**Key Models**: DNR/PDA/MDR/FLR/NSR/RNP XGBoost (concessions), LANTERN/PACMAN/IDA (MAA), A-to-Z XGBoost (MFN), BEARS (account-level), CAP routing models
**Infrastructure**: DAWS, MODS, MMS, AMES (PMML), SageMaker, Cradle
**Related**: [LightGBM](#lightgbm), [GBDT](#gbdt---gradient-boosted-decision-trees), [MTL](#mtl---multi-task-learning)

### LightGBM
**Full Name**: Light Gradient Boosting Machine
**Description**: Microsoft's gradient boosting framework optimized for efficiency and speed. Alternative to XGBoost with faster training on large datasets.
**Documentation**: [LightGBM Term](../resources/term_dictionary/term_lightgbm.md)
**Advantages**: Faster training, lower memory usage, handles large-scale data
**Related**: [XGBoost](#xgboost), Gradient Boosting

### MTT-E - Masked Tabular Transformer with Experts
**Full Name**: Masked Tabular Transformer with Experts
**Description**: Neural architecture for unified BAA detection across multiple ContREE trigger points. **Decouples representation learning (shared transformer encoder) from decision specialization (lightweight MLP experts)**, handling heterogeneous feature schemas via mask-conditioned tokenization. Outperforms XGBoost by +256 bps recall at 95% precision on multi-trigger fraud detection.
**Documentation**: [MTT-E Term](../resources/term_dictionary/term_mtt_e.md)
**Related**: [XGBoost](#xgboost), [ContREE](../resources/term_dictionary/term_contree.md), [ConAM](../resources/term_dictionary/term_conam.md)

### GRAIL - Graph-Retrieval-Augmented Intelligent Language Model
**Full Name**: Graph-Retrieval-Augmented Intelligent Language Model
**Description**: Knowledge graph-grounded LLM reasoning system for appeal automation. **Constructs on-the-fly KGs from Paragon data and enforcement records to provide structured grounding that mitigates LLM hallucination** in high-stakes enforcement decisions. Uses a four-stage pipeline: data refinement, KG construction, multi-strategy graph traversal, and KG-guided SOP query reasoning.
**Documentation**: [GRAIL Term](../resources/term_dictionary/term_grail.md)
**Related**: [RAG](../resources/term_dictionary/term_rag.md), [Knowledge Graph](../resources/term_dictionary/term_knowledge_graph.md), [DeepCARE](../resources/term_dictionary/term_deepcare.md)

### MetaGuard - Unified Meta-Learning for MAA
**Full Name**: MetaGuard
**Description**: A unified meta-learning framework built on CNAPS (Simple Conditional Neural Adaptive Processes) that consolidates PACMAN and LANTERN into a single adaptive model for Multi-Account Abuse detection. **Adapts to new abuse patterns via lightweight forward pass with no gradient updates required.** Designs meta-training tasks across payment methods, GL product groups, and abuse program types for generalizable representations.
**Documentation**: [MetaGuard Term](../resources/term_dictionary/term_metaguard.md)
**Related**: [PACMAN](../resources/term_dictionary/term_pacman.md), [LANTERN](../resources/term_dictionary/term_lantern.md), [Meta-Learning](../resources/term_dictionary/term_meta_learning.md)

### IOS - Identity Obfuscation Score
**Full Name**: Identity Obfuscation Score
**Description**: A multi-dimensional risk assessment using an LLM as a reasoning engine to detect identity obfuscation in post-IDV safelisted customers. **Performs chain-of-thought reasoning across five evidence dimensions** (payment methods, sign-in patterns, name/address consistency, ID submissions, ID duplicates) to produce risk categories with confidence scores. Addresses the post-IDV gap where 35% of safelisted customers commit abuse.
**Documentation**: [IOS Term](../resources/term_dictionary/term_ios.md)
**Related**: [IDV](../resources/term_dictionary/term_idv.md), [CrossBERT](../resources/term_dictionary/term_crossbert.md), [Chain of Thought](../resources/term_dictionary/term_chain_of_thought.md)

### Feature Engineering
**Full Name**: Feature Engineering
**Description**: Process of creating, selecting, and transforming input variables for ML models. In BAP, transforms customer behavior, order attributes, and seller signals into predictive features via OTF (real-time) and ETLM (batch). **Bridges raw data and model training by encoding domain knowledge into numerical representations.**
**Documentation**: [Feature Engineering Term](../resources/term_dictionary/term_feature_engineering.md)
**Related**: [OTF](../resources/term_dictionary/term_otf.md), [Sugar Index](../resources/term_dictionary/term_sugar_index.md)

### GBDT - Gradient Boosted Decision Trees
**Full Name**: Gradient Boosted Decision Trees
**Description**: Ensemble learning technique building sequential decision trees where each tree corrects errors of previous trees. Foundation for XGBoost and LightGBM.
**Documentation**: [GBDT Term](../resources/term_dictionary/term_gbdt.md)
**Related**: [XGBoost](#xgboost), [LightGBM](#lightgbm)

### Multi-Modal
**Full Name**: Multi-Modal (Multimodal Learning)
**Description**: ML approaches integrating multiple data modalities (text, images, tabular, graph). In BAP, combines behavioral data, evidence photos, CS contacts, and graph signals. **SOPA, AIDE, and VISTA VLM are key multi-modal models.**
**Documentation**: [Multi-Modal Term](../resources/term_dictionary/term_multi_modal.md)

### Rule Generation
**Full Name**: Automated Rule Generation
**Description**: Automated creation of fraud detection rules using ML and agentic AI. **GUARDIAN achieved 85% reduction in rule development time.** Approaches: XGBoost+KS (GUARDIAN), Apriori (Hyperloop), tree-based (FROST), LLM+RL (QRN).
**Documentation**: [Rule Generation Term](../resources/term_dictionary/term_rule_generation.md)

### FROST - Framework for Rule Optimization and Structure Transformation
**Full Name**: Framework for Rule Optimization and Structure Transformation
**Description**: A tree-structured rule generation framework that employs FP-Growth algorithm with specialized redundancy elimination, **reducing search time complexity from O(2^n) to O(n)** compared to Apriori. Handles both numeric and categorical features through optimized binning and enables 'OR' logic via rule-to-tree pruning. Integrated into Hyperloop for automated weekly rule deployment across ContREE intents.
**Documentation**: [FROST Term](../resources/term_dictionary/term_frost.md)
**Wiki**: https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/BotMitigationML/HyperLoop/
**Related**: [Hyperloop](../resources/term_dictionary/term_hyperloop.md), [ROCK](../resources/term_dictionary/term_rock.md), [RMP](../resources/term_dictionary/term_rmp.md)

### HyperOrchestrator
**Full Name**: HyperOrchestrator
**Description**: A journey-aware, globally optimized automated rule generation framework that evolves Hyperloop from independent per-trigger-point rule generation into coordinated cross-journey optimization. **Formulates rule deployment as a sequential decision process solved via reinforcement learning**, where an RL agent jointly optimizes rule selection across trigger points to maximize cumulative recall while favoring early detection. Pursues cross-feature enrichment and cross-ruleset coordination in parallel.
**Documentation**: [HyperOrchestrator Term](../resources/term_dictionary/term_hyperorchestrator.md)
**Wiki**: https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/BotMitigationML/HyperLoop/
**Related**: [Hyperloop](../resources/term_dictionary/term_hyperloop.md), [RL](../resources/term_dictionary/term_rl.md), [ContREE](../resources/term_dictionary/term_contree.md)

### Multi-Agent
**Full Name**: Multi-Agent Systems
**Description**: Architectures where specialized AI agents collaborate via DAG orchestration. **ACD uses central + domain agents; GUARDIAN uses 3 coordinated agents.** Enables parallel processing and scalable addition of new capabilities.
**Documentation**: [Multi-Agent Term](../resources/term_dictionary/term_multi_agent.md)

### Global Model
**Full Name**: Global/Consortium Modeling
**Description**: Training single ML model on data from multiple marketplaces. **Reduces system complexity and enables emerging marketplace coverage.** Requires currency conversion, cross-border variables, and global binning. 12+ initiatives across BRP.
**Documentation**: [Global Model Term](../resources/term_dictionary/term_global_model.md)

### Autoencoder
**Full Name**: Autoencoder (Auto-Encoder)
**Description**: Neural network learning compressed latent representations via encoder-decoder architecture. In BAP, used for anomaly detection (high reconstruction error = anomalous) and embedding generation (DeepCARE KNN). **Unsupervised — learns from data structure without labels.**
**Documentation**: [Autoencoder Term](../resources/term_dictionary/term_autoencoder.md)

### DGL - Deep Graph Library
**Full Name**: Deep Graph Library
**Description**: Open-source Python framework for building and training GNNs. **Foundation for GraphStorm-based models** (Nexus GNN, COSA TGN). Provides efficient message passing, graph convolution, and attention on PyTorch backend. Supports heterogeneous graphs critical for Nexus.
**Documentation**: [DGL Term](../resources/term_dictionary/term_dgl.md)
**Related**: [GNN](../resources/term_dictionary/term_gnn.md), [GraphStorm](../resources/term_dictionary/term_graphstorm.md)

### Deep Learning
**Full Name**: Deep Learning
**Description**: Subset of machine learning using neural networks with multiple layers to learn hierarchical representations. In BAP, powers BERT (NLP), ResNet (CV), GNN (graph), TSA (temporal), and LLM-based models. **Excels on unstructured data (text, images, graphs) while gradient boosting dominates tabular data.**
**Documentation**: [Deep Learning Term](../resources/term_dictionary/term_deep_learning.md)
**Related**: [BERT](../resources/term_dictionary/term_bert.md), [GNN](../resources/term_dictionary/term_gnn.md), [LLM](../resources/term_dictionary/term_llm.md)

### Drift Detection
**Full Name**: Drift Detection (Model/Data/Concept Drift)
**Description**: Process of identifying when statistical properties of data or model performance change over time. Critical in BAP because adversarial bad actors continuously adapt tactics. **Three types: data drift (feature distributions), concept drift (label relationships), model drift (prediction degradation).** Detected via KS tests, PSI, and performance monitoring.
**Documentation**: [Drift Detection Term](../resources/term_dictionary/term_drift_detection.md)
**Related**: [MODS](../resources/term_dictionary/term_mods.md), [MO](../resources/term_dictionary/term_mo.md)

### Ensemble Learning
**Full Name**: Ensemble Learning
**Description**: Combining multiple models to improve prediction performance. Reduces overfitting and increases robustness.
**Documentation**: [Ensemble Term](../resources/term_dictionary/term_ensemble.md)
**Methods**: Bagging, boosting, stacking
**Related**: [XGBoost](#xgboost), [Random Forest](#random-forest)

### Random Forest
**Full Name**: Random Forest
**Description**: Ensemble of decision trees using bagging. Robust baseline model for classification and regression tasks.
**Documentation**: [Random Forest Term](../resources/term_dictionary/term_random_forest.md)
**Related**: [XGBoost](#xgboost), Decision Trees

### Logistic Regression
**Full Name**: Logistic Regression
**Description**: Statistical model for binary classification using logistic function. Simple, interpretable baseline for abuse detection.
**Documentation**: [Logistic Regression Term](../resources/term_dictionary/term_logistic_regression.md)
**Related**: Linear Models, GLM

### LDA - Latent Dirichlet Allocation
**Full Name**: Latent Dirichlet Allocation (Blei, Ng, Jordan 2003)
**Description**: Generative probabilistic model for topic modeling. Each document is a mixture of topics (Dirichlet prior), each topic is a mixture of words (Dirichlet prior). **Uses Dirichlet-Multinomial conjugacy for tractable inference via variational EM or Gibbs sampling.** Predecessor: pLSA (Hofmann 1999). Extensions: HDP (nonparametric), CTM (correlated topics), STM (structural). Applied to document clustering, information retrieval, and abuse pattern discovery.
**Documentation**: [LDA Term](../resources/term_dictionary/term_lda.md)
**Related**: [Logistic Regression](#logistic-regression), [BERT](acronym_glossary_llm.md#bert---bidirectional-encoder-representations-from-transformers)

### PMML - Predictive Model Markup Language
**Full Name**: Predictive Model Markup Language
**Description**: **Primary model deployment format for AMES** - XML standard for model portability. Pipeline: Training → PMML Conversion → MMS Upload → AMES (<10ms latency). Supports XGBoost (primary), RF, LightGBM, GBT. Limitation: >2000 trees may exceed memory; DNN requires SageMaker instead.
**Documentation**: [PMML Term](../resources/term_dictionary/term_pmml.md)
**Wiki**: [XGBoost DAWS Integration](https://w.amazon.com/bin/view/CMLS/ME/IntegrateXGBoostModelToDAWS/), [uploadPmmlToMms](https://w.amazon.com/bin/view/MachineLearningTools/uploadPmmlToMms/)
**Inference Latency**: <10ms (typical for PMML on AMES)
**Key Models**: DNR/PDA/MDR/FLR XGBoost, LANTERN/PACMAN/IDA, A-to-Z, Secure Delivery, CAP routing
**Infrastructure**: DAWS (training), MMS (storage), AMES (execution), FORTRESS (orchestration)
**Status**: ✅ Active - primary model deployment format for AMES
**Related**: [AMES](../resources/term_dictionary/term_ames.md), [DAWS](../resources/term_dictionary/term_daws.md), [XGBoost](#xgboost), [MODS](../resources/term_dictionary/term_mods.md)

### k-NN - k-Nearest Neighbors
**Full Name**: k-Nearest Neighbors
**Description**: **Core mechanism in DeepCARE** - finds k most similar historical cases for consensus decision. Uses 440 neighbors via ElasticSearch. Key advantage: **continuous adaptive learning** without retraining (new decisions immediately available). 493K investigations automated, 90%+ precision.
**Documentation**: [k-NN Term](../resources/term_dictionary/term_knn.md)
**Architecture**: Embedding Generation (Order2Vector/eSNN, 64-dim) → ElasticSearch k-NN (cosine similarity) → Consensus Voting → Decision
**k Value**: 440 neighbors (typical for DeepCARE)
**Use Cases**: DeepCARE investigation automation, ALMOND v1 MO detection, BOT email detection, IPP ASIN matching
**Performance**: 493K investigations automated, 90%+ precision, 24.4% automation rate on sidelined orders
**Advantage**: No retraining required, interpretable (show similar cases), adaptive, handles edge cases
**Limitation**: Higher latency than model inference, cold start, embedding quality dependency
**Wiki**: [DeepCARE Wiki](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/DeepCARE/)
**Related**: [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [eSNN](#esnn---extended-siamese-neural-network), [ALMOND](#almond---adaptive-learning-for-mo-detection), ElasticSearch

---

## Deep Learning Frameworks

### PyTorch
**Full Name**: PyTorch
**Description**: Open-source deep learning framework developed by Meta. Primary framework for neural network development at Amazon due to flexibility and dynamic computation graphs.
**Documentation**: [PyTorch Term](../resources/term_dictionary/term_pytorch.md)
**Use Cases**: Deep learning models, MTL models, GNN models
**Related**: [MTL](#mtl---multi-task-learning), [GNN](#gnn---graph-neural-networks)

### TensorFlow
**Full Name**: TensorFlow
**Description**: Google's open-source deep learning framework. Alternative to PyTorch with strong production deployment support.
**Documentation**: [TensorFlow Term](../resources/term_dictionary/term_tensorflow.md)
**Related**: [PyTorch](#pytorch), Keras

---

## Distributed Training

### Data Parallelism - Distributed Data Parallel (DDP)
**Full Name**: Data Parallelism
**Description**: Distributed training strategy where the model is replicated across $N$ devices, each processing a $1/N$ partition of the mini-batch. Gradients are aggregated via AllReduce (typically Ring-AllReduce) so all replicas apply identical updates. Mathematically equivalent to single-device training with $N\times$ batch size. **Most widely adopted distributed training strategy** — the default first step for scaling. Scaling limit: beyond critical batch size $B_{\text{crit}}$, convergence degrades. Modern implementations (PyTorch DDP, Horovod, DeepSpeed ZeRO) overlap gradient communication with backward computation for near-linear throughput scaling.
**Documentation**: [Data Parallelism Term](../resources/term_dictionary/term_data_parallelism.md)
**Key Implementations**: PyTorch DDP, Horovod, DeepSpeed ZeRO, JAX pmap
**Related**: [Model Parallelism](#model-parallelism---tensor--pipeline-parallelism), [Expert Parallelism](#expert-parallelism---moe-device-placement), [MoE](../resources/term_dictionary/term_moe.md), [Scaling Law](../resources/term_dictionary/term_scaling_law.md)

### Model Parallelism - Tensor & Pipeline Parallelism
**Full Name**: Model Parallelism
**Description**: Distributed training strategy that partitions the model itself across devices, enabling training of models too large for single-device memory. Two forms: **Tensor parallelism** (intra-layer) splits weight matrices within layers using ColumnParallel/RowParallel linear layers (Megatron-LM), requiring high-bandwidth NVLink. **Pipeline parallelism** (inter-layer) assigns layer groups to pipeline stages and pipelines micro-batches through them (GPipe, PipeDream), with bubble overhead $(p-1)/(M+p-1)$. In **3D parallelism**, tensor (intra-node) + pipeline (inter-node) + data (across replicas) are combined for trillion-parameter training.
**Documentation**: [Model Parallelism Term](../resources/term_dictionary/term_model_parallelism.md)
**Key Frameworks**: Megatron-LM, GPipe, PipeDream, DeepSpeed, Colossal-AI
**Related**: [Data Parallelism](#data-parallelism---distributed-data-parallel-ddp), [Expert Parallelism](#expert-parallelism---moe-device-placement), [Tensor Parallelism](#tp---tensor-parallelism), [Pipeline Parallelism](#pp---pipeline-parallelism), [MoE](../resources/term_dictionary/term_moe.md)

### TP - Tensor Parallelism
**Full Name**: Tensor Parallelism (Intra-Layer Model Parallelism)
**Description**: Distributed training strategy that partitions weight tensors within individual layers across devices. Each device computes a slice of every layer's matrix multiplication. For Transformers, MLP uses **ColumnParallelLinear** (first layer split column-wise) + **RowParallelLinear** (second layer split row-wise), producing only two AllReduce operations per Transformer block. Attention heads are split across devices with independent parallel computation. **Requires NVLink** (900 GB/s) due to per-layer communication — typically limited to intra-node (2-8 GPUs). Extensions: sequence parallelism (Korthikanti et al. 2023) and context parallelism (Ring Attention, DeepSpeed-Ulysses) extend TP to non-tensor-parallel regions and long sequences.
**Documentation**: [Tensor Parallelism Term](../resources/term_dictionary/term_tensor_parallelism.md)
**Key Papers**: Shoeybi et al. (2019) Megatron-LM — arXiv:1909.08053
**Related**: [Model Parallelism](#model-parallelism---tensor--pipeline-parallelism), [Pipeline Parallelism](#pp---pipeline-parallelism), [Data Parallelism](#data-parallelism---distributed-data-parallel-ddp)

### PP - Pipeline Parallelism
**Full Name**: Pipeline Parallelism (Inter-Layer Model Parallelism)
**Description**: Distributed training strategy that partitions consecutive layer groups (stages) across devices and pipelines micro-batches through them. Key efficiency metric: **bubble overhead** = $(p-1)/(M+p-1)$ where $p$ = stages and $M$ = micro-batches. Four scheduling generations: **GPipe** (2018, fill-drain), **1F1B/PipeDream** (2019, reduced memory via interleaved forward-backward), **Interleaved 1F1B** (2021, virtual stages reduce bubble by factor $v$), and **Zero Bubble PP** (2024, decouples weight gradients for near-zero idle time). Works across nodes via point-to-point communication — lower bandwidth requirement than tensor parallelism.
**Documentation**: [Pipeline Parallelism Term](../resources/term_dictionary/term_pipeline_parallelism.md)
**Key Papers**: Huang et al. (2019) GPipe; Narayanan et al. (2019) PipeDream; Qi et al. (2024) Zero Bubble PP
**Related**: [Model Parallelism](#model-parallelism---tensor--pipeline-parallelism), [Tensor Parallelism](#tp---tensor-parallelism), [Data Parallelism](#data-parallelism---distributed-data-parallel-ddp)

### Expert Parallelism - MoE Device Placement
**Full Name**: Expert Parallelism
**Description**: Distributed training strategy specific to [Mixture of Experts (MoE)](../resources/term_dictionary/term_moe.md) architectures, where each expert sub-network is placed on a separate device. Tokens are routed to the correct device via **all-to-all** collective communication (dispatch), processed by the local expert, and returned via a second all-to-all (combine). Enables scaling to thousands of experts and trillions of parameters (Switch Transformer: 2,048 experts on 2,048 TPU cores). Key challenge: load balancing — uneven routing wastes capacity and drops tokens beyond the expert capacity buffer.
**Documentation**: [Expert Parallelism Term](../resources/term_dictionary/term_expert_parallelism.md)
**Key Systems**: GShard, Switch Transformer, DeepSpeed-MoE, Mixtral
**Related**: [Data Parallelism](#data-parallelism---distributed-data-parallel-ddp), [Model Parallelism](#model-parallelism---tensor--pipeline-parallelism), [MoE](../resources/term_dictionary/term_moe.md), [Conditional Computation](../resources/term_dictionary/term_conditional_computation.md)

---

## Neural Network Architectures

### Graph
→ **Moved to [Network Science Glossary](acronym_glossary_network_science.md#graph)**. See there for the foundational concept; this glossary covers graph ML architectures below.

### GGM - Gaussian Graphical Model
**Full Name**: Gaussian Graphical Model (Undirected)
**Description**: Undirected graphical model with multivariate Gaussian joint distribution. **Graph structure encoded in precision matrix $\Theta = \Sigma^{-1}$: edge exists iff $\Theta_{ij} \neq 0$ (conditional dependence).** Estimated via GraphLasso (L1-penalized MLE). Applications: gene regulatory networks, brain connectivity, financial networks, abuse ring detection (customer interaction graphs).
**Documentation**: [GGM Term](../resources/term_dictionary/term_gaussian_graphical_model.md)
**Related**: [GNN](#gnn---graph-neural-networks), [PGM](#pgm---probabilistic-graphical-model)

### PGM - Probabilistic Graphical Model
**Full Name**: Probabilistic Graphical Model
**Description**: Framework for representing complex distributions using graph structure. **Two families: directed (Bayesian networks, DAGs) and undirected (Markov random fields, MRFs).** Factorization theorem: joint = product of local factors. Inference: variable elimination, junction tree, belief propagation, variational, MCMC. Examples: HMM, CRF, LDA, GGM. Foundation for structured prediction in NLP and abuse risk scoring.
**Documentation**: [PGM Term](../resources/term_dictionary/term_probabilistic_graphical_model.md)
**Related**: [GGM](#ggm---gaussian-graphical-model), [LDA](#lda---latent-dirichlet-allocation), [GNN](#gnn---graph-neural-networks)

### HMM - Hidden Markov Model
**Full Name**: Hidden Markov Model
**Description**: Directed PGM for sequential data with hidden states. **Three problems: evaluation (forward), decoding (Viterbi), learning (Baum-Welch/EM).** Classic for speech recognition, NER, gene finding. In BAP, models temporal abuse behavior sequences (MO patterns). Replaced by RNN/Transformer for most NLP but still used for structured sequence modeling.
**Documentation**: [HMM Term](../resources/term_dictionary/term_hmm.md)
**Related**: [PGM](#pgm---probabilistic-graphical-model), [CRF](#crf---conditional-random-field)

### CRF - Conditional Random Field
**Full Name**: Conditional Random Field (Lafferty et al., 2001)
**Description**: Discriminative undirected PGM for structured prediction. **Models $P(y|x)$ directly — avoids HMM's independence assumption on observations.** Linear-chain CRF for sequences; global normalization avoids label bias. BiLSTM-CRF was pre-Transformer standard for NER. CRF is to MRF as logistic regression is to naive Bayes.
**Documentation**: [CRF Term](../resources/term_dictionary/term_crf.md)
**Related**: [HMM](#hmm---hidden-markov-model), [PGM](#pgm---probabilistic-graphical-model), [NER](acronym_glossary_llm.md#ner---named-entity-recognition)

### Variational Inference
**Full Name**: Variational Inference (VI)
**Description**: Approximate Bayesian inference by optimization: minimize $\\text{KL}(q \\| p(\\theta|x))$ or equivalently maximize ELBO. **Turns inference into optimization — faster than MCMC for large datasets.** Mean-field (factored $q$), amortized VI (neural encoder, used in VAE), stochastic VI for scalability. Standard inference for LDA.
**Documentation**: [Variational Inference Term](../resources/term_dictionary/term_variational_inference.md)
**Related**: [PGM](#pgm---probabilistic-graphical-model), [LDA](#lda---latent-dirichlet-allocation)

### Belief Propagation
**Full Name**: Belief Propagation (Message Passing / Sum-Product Algorithm)
**Description**: Message-passing algorithm for inference in graphical models. **Exact on trees; approximate (loopy BP) on graphs with cycles.** Sum-product for marginals, max-product for MAP. Forward-backward algorithm (HMM) is BP on a chain. Equivalent to variational inference with Bethe free energy.
**Documentation**: [Belief Propagation Term](../resources/term_dictionary/term_belief_propagation.md)
**Related**: [PGM](#pgm---probabilistic-graphical-model), [Variational Inference](#variational-inference), [HMM](#hmm---hidden-markov-model)

### MRF - Markov Random Field
**Full Name**: Markov Random Field (Undirected Graphical Model)
**Description**: Undirected PGM where joint factorizes over cliques: $P(x) = \frac{1}{Z}\prod_c \psi_c(x_c)$. **Hammersley-Clifford theorem: positive distribution + Markov property ↔ Gibbs factorization.** GGM is a Gaussian MRF. CRF is a discriminative MRF. Used in image segmentation, spatial statistics, network modeling.
**Documentation**: [MRF Term](../resources/term_dictionary/term_markov_random_field.md)
**Related**: [PGM](#pgm---probabilistic-graphical-model), [GGM](#ggm---gaussian-graphical-model), [CRF](#crf---conditional-random-field)

### Factor Graph
**Full Name**: Factor Graph (Bipartite Graphical Model)
**Description**: Bipartite graph with variable nodes and factor nodes. **Unifies directed (Bayesian networks) and undirected (MRFs) representations.** Joint: $P(x) = \frac{1}{Z}\prod_a f_a(x_a)$. Belief propagation operates naturally on factor graphs. Used in error-correcting codes, LDPC, turbo codes.
**Documentation**: [Factor Graph Term](../resources/term_dictionary/term_factor_graph.md)
**Related**: [PGM](#pgm---probabilistic-graphical-model), [MRF](#mrf---markov-random-field), [Belief Propagation](#belief-propagation)

### PAC Learning
**Full Name**: PAC Learning — Probably Approximately Correct (Valiant, 1984)
**Description**: Computational learning theory framework. A concept class is PAC-learnable if an algorithm can output a hypothesis with error $\leq \epsilon$ with probability $\geq 1-\delta$ given $m \geq m_0(\epsilon, \delta)$ samples. **Sample complexity depends on VC dimension.** Uses concentration inequalities (Hoeffding) for generalization bounds. Foundation of statistical learning theory.
**Documentation**: [PAC Learning Term](../resources/term_dictionary/term_pac_learning.md)
**Related**: [Concentration Inequalities](acronym_glossary_statistics.md#concentration-inequalities), [Hoeffding's Inequality](acronym_glossary_statistics.md#hoeffdings-inequality)

### GNN - Graph Neural Networks
**Full Name**: Graph Neural Networks
**Description**: ML on graph-structured data capturing relational patterns tabular ML cannot express. **+10-20% fraud improvement** over XGBoost. Key architectures: GCN, GraphSAGE, GAT, HGT, TGN. Amazon projects: GRADE (AUC 0.95→0.963), GRAF (INR 460MM savings), Nexus GNN, SPIDER. Infrastructure: GraphStorm, DGL, GraMS.
**Documentation**: [GNN Term](../resources/term_dictionary/term_gnn.md)
**Wiki**: [GRADE](https://w.amazon.com/bin/view/BuyerRiskPreventionML/GNN/), [AMLC GML Workshop](https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/AGML/AMLC2023-GMLWorkshop/)
**Key Architectures**: GCN, GraphSAGE, GAT, R-GCN, HGT, TGN
**Amazon Projects**: GRADE, GRAF, Nexus GNN, Graph PACMAN, SPIDER
**Training**: GraphStorm (distributed), DGL (library), GraMS (real-time DB)
**Use Cases**: MAA detection, PFOC scoring, cold-start risk, relationship modeling, MO clustering
**Performance**: +10-20% over tabular ML on fraud detection
**Status**: ✅ Active - core graph ML technology for fraud/abuse detection
**Related**: [HGT](#hgt---heterogeneous-graph-transformers), [TGN](#tgn---temporal-graph-network), [MAA](../resources/term_dictionary/term_maa.md), [Nexus](../resources/term_dictionary/term_nexus.md), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### GRAF - Graph Based Risk Assessment Functionality
**Full Name**: Graph Based Risk Assessment Functionality
**Description**: Graph Neural Network-based ML model developed by Amazon's International Machine Learning (IML) team for buyer abuse prevention in India marketplace. GRAF detects hit-and-run abuse by modeling orders and customers as nodes on a graph to capture multi-hop relationship information that traditional clustering methods miss. It uses EdgeAV-GAT attention layers and manages 30MM nodes while achieving +3% AUC improvement over baseline models. Production deployment enables pre-fulfillment order cancellation with estimated savings of INR 460MM annualized and 90% precision at order cancellation.
**Documentation**: [GRAF Term](../resources/term_dictionary/term_graf.md)
**Wiki**: [GRAF Main](https://w.amazon.com/bin/view/AIML/GRAF/), [GRAF Concessions](https://w.amazon.com/bin/view/IML/IML_IndiaDataScienceBLR/TeamProjects/GRAF_Concessions/)
**Team**: International Machine Learning (IML) - India
**Use Cases**: Hit-and-run abuse detection, concessions abuse prevention, multi-hop relationship modeling
**Performance**: +3% AUC improvement, INR 460MM estimated annual savings, 90% precision
**Status**: ✅ Active - Production deployment in India marketplace
**Related**: [GNN](#gnn---graph-neural-networks), [HGT](#hgt---heterogeneous-graph-transformers), [Customer Clustering](#cd---community-detection)

### RGAT - Relational Graph Attention Network
**Full Name**: Relational Graph Attention Network
**Description**: Graph neural network architecture extending GAT for heterogeneous graphs with multiple relation types. Uses relation-specific attention weights and multi-head attention mechanisms.
**Documentation**: [RGAT Term](../resources/term_dictionary/term_rgat.md)
**Use Cases**: Node classification for PFOC, heterogeneous graph learning, risk score prediction
**Related**: [RGCN](#rgcn---relational-graph-convolutional-network), [HGT](#hgt---heterogeneous-graph-transformers), [GNN](#gnn---graph-neural-networks)

### RGCN - Relational Graph Convolutional Network
**Full Name**: Relational Graph Convolutional Network
**Description**: GNN architecture designed for multi-relational data, extending GCN to handle multiple edge types through relation-specific weight matrices with basis decomposition for efficiency.
**Documentation**: [RGCN Term](../resources/term_dictionary/term_rgcn.md)
**Use Cases**: Node classification for PFOC, multi-relation graph learning, knowledge graph completion
**Related**: [RGAT](#rgat---relational-graph-attention-network), [HGT](#hgt---heterogeneous-graph-transformers), [GNN](#gnn---graph-neural-networks)

### TGAT - Temporal Graph Attention Network
**Full Name**: Temporal Graph Attention Network
**Description**: GNN architecture for dynamic graphs incorporating temporal information through time-encoding functions and attention mechanisms to capture evolving graph structure.
**Documentation**: [TGAT Term](../resources/term_dictionary/term_tgat.md)
**Use Cases**: Nexus V3 development, temporal pattern detection
**Status**: 📅 In Development - ETA March 2026
**Related**: [TGN](#tgn---temporal-graph-network), [HGT](#hgt---heterogeneous-graph-transformers), [GNN](#gnn---graph-neural-networks)

### KG Embeddings - Knowledge Graph Embeddings
**Full Name**: Knowledge Graph Embeddings
**Description**: Low-dimensional vector representations of entities and relationships in a knowledge graph. Methods include TransE, TransR, ComplEx, and GNN encoders (HGT, RGCN).
**Documentation**: [KG Embeddings Term](../resources/term_dictionary/term_kg_embeddings.md)
**Performance**: AtoZ abuse detection improved PR-AUC 86%→92%, F1 78%→85%
**Use Cases**: Order-level risk scoring, customer similarity search, clustering
**Related**: [Nexus](../resources/term_dictionary/term_nexus.md), [GNN](#gnn---graph-neural-networks)

### GAT - Graph Attention Network
**Full Name**: Graph Attention Network
**Description**: GNN with **attention-weighted** neighbor aggregation - learns which neighbors matter. Amazon: GRACE (part of GRADE, AUC 0.95→0.963). Multi-head attention for stability. Limitation: single edge type only; use HGT for heterogeneous graphs (customer-device-payment).
**Documentation**: [GAT Term](../resources/term_dictionary/term_gat.md)
**Wiki**: [GRADE/GRACE](https://w.amazon.com/bin/view/BuyerRiskPreventionML/GNN/)
**Amazon Project**: GRACE (GRaph Attention Customer Embedding) in GRADE
**Architecture**: Attention-weighted neighbor aggregation with multi-head attention
**Use Cases**: Customer-level fraud embedding, relationship importance learning
**Performance**: AUC 0.95 → 0.963 on fraud detection (GRADE)
**Status**: ✅ Active - foundational GNN architecture (HGT preferred for heterogeneous)
**Related**: [GNN](#gnn---graph-neural-networks), [HGT](#hgt---heterogeneous-graph-transformers), [Transformer](#transformer), [GRADE](../resources/term_dictionary/term_gnn.md)

### HGT - Heterogeneous Graph Transformers
**Full Name**: Heterogeneous Graph Transformers
**Description**: GNN for **heterogeneous graphs** (multiple node/edge types) with type-aware attention - "shares credit card" ≠ "shares IP". Deployments: Gift Card ($5MM), SpiderWeb (+1.6% AUC), EU13 ($5MM), CSMO F1=0.84. vs TGN: HGT for entity semantics, TGN for temporal dynamics.
**Documentation**: [HGT Term](../resources/term_dictionary/term_hgt.md)
**Key Innovation**: Type-specific attention mechanisms for semantic edge relationships
**Deployments**:
  - Gift Card Lifecycle HGT ($5MM annual savings)
  - SpiderWeb Enhancement (+1.6% AUC, 200K BAA/ATO cleaned)
  - EU13 Consortium Model (+0.9% AP, $5MM savings)
  - CSMO HGT-GRAHIES (F1 0.84 for MO detection)
**Teams**: GCAT, BAP ML Tattletale, AIT, AUSAIN
**vs TGN**: HGT better for multi-entity semantics; TGN better for pure temporal
**Wiki**: [SPS Graph Modeling Working Group](https://w.amazon.com/bin/view/SPS_Graph_Modeling_Working_Group/)
**Related**: [GNN](#gnn---graph-neural-networks), [TGN](#tgn---temporal-graph-network), [Transformer](#transformer), [Community Detection](#cd---community-detection), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### TGN - Temporal Graph Network
**Full Name**: Temporal Graph Network
**Description**: GNN for **dynamic/temporal graphs** via memory module + temporal attention - predicts **future risk trajectories**. TFCM: **37-day lead time** before first fraud, $12MM savings. COSA: real-time scoring, +13% BAA. First TGN at Amazon.
**Documentation**: [TGN Term](../resources/term_dictionary/term_tgn.md)
**Key Innovation**: Memory module + temporal attention for trajectory prediction (reactive → proactive)
**Deployments**:
  - **TFCM** - Temporal Fraud Closure Model ($12MM annual savings, 37-day lead time)
  - **COSA** - Continuous One Step Ahead (real-time scoring at lifecycle events)
  - **TSFC** - Temporal Seller Fraud Closure Model (AUC 0.78 vs 0.69 static, <1% reinstatement)
  - **TACM** - Temporal Abuse Closure Model (concessions abuse research)
**Performance**: +1.04% AUC, +13% TPR vs static methods; detects intra-day fraud (25%+ of chargebacks)
**Infrastructure**: GraMS (Neptune graph DB + SageMaker + AMES + URES)
**vs HGT**: TGN for temporal dynamics; HGT for heterogeneous entity semantics
**Team**: BRP ML AUSAIN / OSA (One Step Ahead)
**Wiki**: [TFCM Wiki](https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/TFCM/)
**Related**: [GNN](#gnn---graph-neural-networks), [HGT](#hgt---heterogeneous-graph-transformers), [COSA](#cosa---continuous-one-step-ahead), [PFW](../resources/term_dictionary/term_pfw.md), [MAA](../resources/term_dictionary/term_maa.md)

### COSA - Continuous One Step Ahead
**Full Name**: Continuous One Step Ahead
**Description**: **First online TGN at Amazon** (March 2023) - continuous scoring at lifecycle events vs daily batch. **Real-time MO wipeout**: when PFW detects bad actor, COSA scores all related customers immediately. Performance: +13% BAA, +9% CB savings, 18-day lead time.
**Documentation**: [COSA Term](../resources/term_dictionary/term_cosa.md)
**Key Innovation**: Continuous lifecycle event scoring + real-time MO wipeout (batch → online)
**Launch**: March 2023 (FR), November 2023 (EU/NA billion-node scale)
**Performance**:
  - **+13% BAA detection** (system-missed Bad Actor Accounts)
  - **+9% chargeback savings** (incremental)
  - **18-day lead time** before first CB order
  - 2000 TPS evaluation, billion-node graphs
**Infrastructure**: GraMS (Neptune + SageMaker + AMES + URES + OTF)
**Abuse Integration**: Same COSA graph supports buyer abuse detection (+10% incremental abuse detection in TR)
**Dashboards**: [Science](https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/COSA-Dashboard/) | [Ingestion](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/IngestionDashboard)
**Team**: BRP ML AUSAIN / OSA + CoRe
**Wiki**: [COSA FR Announcement](https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/COSA-FR-announcement/) | [GraMS](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/)
**Related**: [TGN](#tgn---temporal-graph-network), [GNN](#gnn---graph-neural-networks), [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [PFW](../resources/term_dictionary/term_pfw.md)

### BEAD - Benchmark Estimation and Anomaly Detection
**Full Name**: Benchmark Estimation and Anomaly Detection
**Description**: An unsupervised ML framework from the POE Science team that detects ASINs with severe product quality issues. **BEAD works in two stages: ASIN grouping via semi-supervised clustering, then anomaly detection via boxplot outliers, contingency table testing, and robust regression with Huber loss.** It identified 0.2% of ASINs in US Hardlines as anomalies driving 10% of defective complaints. Used in Search Reranking via Graded Demotion to demote problematic ASINs.
**Documentation**: [BEAD](../resources/term_dictionary/term_bead.md)
**Related**: [D3](../resources/term_dictionary/term_d3.md), [Ship2Vec](../resources/term_dictionary/term_ship2vec.md)

### ROOT - Rule Online OpTimization
**Full Name**: Rule Online OpTimization
**Description**: A reinforcement learning system for real-time optimization of fraud prevention rules in RMP. **ROOT uses Twin Delayed DDPG (TD3) with offline RL variants (CQL, BCQ) to dynamically adjust rule thresholds based on incoming traffic patterns.** It bridges the gap between investigator decisions and system actions through moderators on rule conditions. Published at AMLC 2021 and deployed in production for multiple intents.
**Documentation**: [ROOT](../resources/term_dictionary/term_root.md)
**Related**: [ARROW](../resources/term_dictionary/term_arrow.md), [RMP](../resources/term_dictionary/term_rmp.md)

### Ship2Vec - Shipment Sequence Embedding Model
**Full Name**: Ship2Vec
**Description**: A pre-trained BERT-based sequence embedding model that transforms shipment tracking event sequences into dense vector representations for Pre-Delivery Abuse (PDA) detection. **Ship2Vec uses Masked-Language(event) Modeling to learn representations from shipment event codes, enabling clustering of abusive shipment patterns.** Contributed approximately $10MM in PDA savings as of late 2023. Succeeded by Diffusion-Based Multi-Modal and Seq2Risk approaches.
**Documentation**: [Ship2Vec](../resources/term_dictionary/term_ship2vec.md)
**Related**: [MODE](../resources/term_dictionary/term_mode.md), [NUTS](../resources/term_dictionary/term_nuts.md)

### X2Risk - CrossBERT Identity Risk Model
**Full Name**: X2Risk (X2R)
**Description**: A unified abuse detection model built on the CrossBERT dual-stream Transformer architecture that consolidates Email2Risk and Domain2Risk into a single model. **X2Risk scores textual identity entities (emails, names, domains) for abuse risk, capturing inter-correlations between entity types.** Powers two rules in US PFW intent delivering ~$2M/year in savings. Launched January 2026.
**Documentation**: [X2Risk](../resources/term_dictionary/term_x2risk.md)
**Related**: [CrossBERT](../resources/term_dictionary/term_crossbert.md), [PFOC](../resources/term_dictionary/term_pfoc.md)

### TFCM - Temporal Fraud Closure Model
**Full Name**: Temporal Fraud Closure Model
**Description**: **First TGN deployed at Amazon** - predicts future fraud enabling proactive enforcement **37 days before** first fraud. Performance: +1.04% AUC, +13% TPR, $12MM savings. Variants: TFCM (buyer), TSFC (seller), TACM (abuse).
**Documentation**: [TFCM Term](../resources/term_dictionary/term_tfcm.md)
**Architecture**: Temporal Graph Network (TGN) with memory module + temporal attention
**Use Cases**: Buyer fraud prediction, seller fraud (TSFC variant), concessions abuse (TACM variant)
**Performance**: 37-day lead time, +1.04% AUC vs static, +13% TPR, $12MM annual savings, detects 25%+ intra-day chargebacks
**Variants**: TFCM (buyer), TSFC (seller, AUC 0.78 vs 0.69 static, <1% reinstatement), TACM (abuse research)
**Infrastructure**: GraMS (Neptune + SageMaker + AMES + URES)
**Team**: BRP ML AUSAIN / OSA (One Step Ahead)
**Launch**: August 2022 (OSA 3YP), August 2023 (In-Store fraud)
**Wiki**: [TFCM Wiki](https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/TFCM/)
**Related**: [TGN](#tgn---temporal-graph-network), [COSA](#cosa---continuous-one-step-ahead), [GNN](#gnn---graph-neural-networks)

### CNN - Convolutional Neural Network
**Full Name**: Convolutional Neural Network
**Description**: Deep neural network using convolutional layers for hierarchical spatial feature extraction from images. Key architectures: AlexNet (2012), ResNet (2015), EfficientNet (2019), BiT (2020). Inductive biases: locality, translation equivariance, hierarchical features. Dominated vision 2012-2020; displaced by ViT for large-scale tasks but still preferred for real-time inference and small datasets. Amazon: VISTA, content moderation, product classification, OCR pipelines.
**Key Papers**: [ViT (Dosovitskiy et al., 2020)](../resources/papers/lit_dosovitskiy2020image.md) — showed pure Transformer matches CNNs at scale
**Documentation**: [CNN Term](../resources/term_dictionary/term_cnn.md)
**Use Cases**: Image-based fraud detection, spatial pattern recognition, real-time inference, edge deployment
**Related**: [ViT](#vit---vision-transformer), [Computer Vision](acronym_glossary_llm.md#computer-vision---cv), [Inductive Bias](#inductive-bias), [SWIN Transformer](acronym_glossary_llm.md#swin-transformer---shifted-window-transformer)

### Inductive Bias
**Full Name**: Inductive Bias (Architectural Prior)
**Description**: Assumptions a ML model makes about data structure through its architecture. CNNs: strong biases (locality, equivariance) → better on small data. Transformers: minimal biases → better on large data. ViT demonstrated empirically: on ImageNet (1.3M images) CNNs win; on JFT-300M (303M images) ViT overtakes. "Large-scale training trumps inductive bias." Practical rule: scarce data → strong bias models; abundant data → Transformers.
**Key Papers**: [ViT (Dosovitskiy et al., 2020)](../resources/papers/lit_dosovitskiy2020image.md), [Attention is All You Need (Vaswani et al., 2017)](../resources/papers/lit_vaswani2017attention.md)
**Documentation**: [Inductive Bias Term](../resources/term_dictionary/term_inductive_bias.md)
**Related**: [CNN](#cnn---convolutional-neural-network), [Scaling Law](#scaling-law), [ViT](#vit---vision-transformer)

### LSTM - Long Short-Term Memory
**Full Name**: Long Short-Term Memory
**Description**: Recurrent neural network architecture designed to learn long-term dependencies in sequential data. Handles vanishing gradient problem through memory cells and gates.
**Documentation**: [LSTM Term](../resources/term_dictionary/term_lstm.md)
**Use Cases**: Temporal sequence modeling, time-series analysis, sequential behavior analysis
**Related**: [RNN](#rnn---recurrent-neural-networks), [Transformer](#transformer)

### MoE - Mixture of Experts
**Full Name**: Mixture of Experts (Sparsely-Gated Mixture-of-Experts)
**Description**: Neural network architecture that increases model capacity without proportional compute by routing each input through a small subset ($k$) of many parallel expert sub-networks ($n$), selected by a learned gating network. Output: $y = \sum_i G(x)_i \cdot E_i(x)$ where $G(x)$ is sparse. First made practical at scale by Shazeer et al. (2017) with Noisy Top-K gating and load-balancing losses, achieving >1000× capacity gains. Modern MoE models (GShard, Switch Transformer, Mixtral, DeepSeek-MoE) combine MoE feed-forward layers with Transformer attention. Amazon: Pop-MoE (risk score combination, +65 bps), Clickstream MoE (behavioral pattern specialization).
**Key Papers**: [Outrageously Large Neural Networks (Shazeer et al., 2017)](../resources/papers/lit_shazeer2017outrageously.md) — first practical MoE at scale; 137B params, 24% lower perplexity
**Documentation**: [MoE Term](../resources/term_dictionary/term_moe.md)
**Key Architectures**: Shazeer (2017, LSTM+MoE) → GShard (2021) → Switch Transformer (2022) → Mixtral (2024) → DeepSeek-MoE (2024)
**Amazon Projects**: [Pop-MoE](../projects/project_pop_moe.md) (EGC score combination), [Clickstream MoE](../projects/project_clickstream_moe.md) (abuse detection)
**Use Cases**: Large-scale language modeling, multi-domain/multi-task learning, efficient capacity scaling
**vs Dense Models**: Same FLOPs, $n/k$× more parameters; experts specialize by input type without supervision
**Status**: ✅ Active - increasingly adopted in frontier models and internal research
**Related**: [Transformer](#transformer), [LSTM](#lstm---long-short-term-memory), [Scaling Law](#scaling-law), [Conditional Computation](../resources/term_dictionary/term_conditional_computation.md), [Gating Network](../resources/term_dictionary/term_gating_network.md)

### RNN - Recurrent Neural Networks
**Full Name**: Recurrent Neural Networks
**Description**: Neural networks with loops allowing information persistence across sequence steps. Foundation for sequence modeling but suffers from vanishing gradient issues.
**Documentation**: [RNN Term](../resources/term_dictionary/term_rnn.md)
**Related**: [LSTM](#lstm---long-short-term-memory), [GRU](#gru---gated-recurrent-unit)

### GRU - Gated Recurrent Unit
**Full Name**: Gated Recurrent Unit
**Description**: Simplified version of LSTM with fewer parameters. Uses reset and update gates to control information flow.
**Documentation**: [GRU Term](../resources/term_dictionary/term_gru.md)
**Related**: [LSTM](#lstm---long-short-term-memory), [RNN](#rnn---recurrent-neural-networks)

### Siamese Network
**Full Name**: Siamese Neural Network
**Description**: Twin networks with shared weights for **similarity learning** - enables few-shot learning (compare vs classify). Amazon: Iridium (duplicates), Tattletale Diff Transformer (RASP, AUC 0.90), brand matching. Losses: Contrastive, Triplet.
**Documentation**: [Siamese Network Term](../resources/term_dictionary/term_siamese_network.md)
**Architecture**: Twin networks with shared weights → embeddings → distance/similarity function
**Loss Functions**: Contrastive Loss, Triplet Loss, Binary Cross-Entropy
**Use Cases**: Duplicate detection, similarity learning, verification tasks, RASP detection (Diff Transformer)
**Key Models**: Tattletale Diff Transformer (AUC 0.90), Iridium Duplicate Detection, Brand Matching
**Wiki**: [Iridium Deep Siamese Networks](https://w.amazon.com/bin/view/Iridium/Development/Deep_Siamese_Networks/)
**Related**: [eSNN](#esnn---extended-siamese-neural-network), [Contrastive Learning](#contrastive-learning), [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), Metric Learning

### eSNN - Extended Siamese Neural Network
**Full Name**: Extended Siamese Neural Network
**Description**: DeepCARE's Siamese architecture learning from **~1,500 variables without feature engineering** (vs 300 hand-picked for AutoEncoder). Contrastive training → k-NN (440 neighbors) in ElasticSearch. Performance: $10MM fraud reduction (US 2022), IPP 2.88MM ASINs at 98%.
**Documentation**: [eSNN Term](../resources/term_dictionary/term_esnn.md)
**Architecture**: Embedding Layer (Siamese Network, 64-dim) + Distance/Similarity Layer + ElasticSearch k-NN
**Training**: Pair generation → Contrastive loss optimization → Extract embedding layer
**Inference**: New order → eSNN embedding → ElasticSearch k-NN (k=440) → Majority vote decision
**Performance**: $10MM fraud chargeback reduction (US Physical 2022), 2.88MM ASIN decisions at 98% precision (IPP 2025)
**Use Cases**: BRP fraud detection (PFW), IPP IP infringement detection (combined with multilingual E5), Seller risk
**Evolution**: AutoEncoder DeepCARE → eSNN DeepCARE (2022) → eSNN + FSL++ (2023+)
**Wiki**: [DeepCARE Experiments - ESNN](https://w.amazon.com/bin/view/URES/URESAutomation/AutomationEvaluation/ESNN/)
**Related**: [Siamese Network](#siamese-network), [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [Contrastive Learning](#contrastive-learning)

### Transformer
**Full Name**: Transformer Architecture ("Attention Is All You Need")
**Description**: Foundation of modern deep learning - **parallel self-attention** vs sequential RNN/LSTM. Variants: Encoder (BERT), Decoder (GPT), Graph (HGT/TGN). BAP deployments: Polygraph ($100K/week), HGT ($5MM), TFCM ($12MM), GreenTEA (15%→50% PFW). O(n²) attention; efficient variants exist.
**Documentation**: [Transformer Term](../resources/term_dictionary/term_transformer.md)
**Wiki**: [Neural Networks Fundamentals](https://w.amazon.com/bin/view/Amazon_business_search/Cibeles/AILearningResources/NeuralNetworksDeepLearningFundamentals/), [GenAI Resources](https://w.amazon.com/bin/view/User/lmmagier/GenAIOpinionatedResources/)
**Key Components**: Multi-head attention, self-attention (Q·K·V), positional encoding, feed-forward network, layer normalization, residual connections
**Architecture Variants**: Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5), Graph (HGT/TGN), Vision (ViT)
**Use Cases**: Text classification (Polygraph, BSM), text generation (GreenTEA, AutoSignality), graph learning (TFCM, COSA, Gift Card), sentence embeddings (SBERT/GoldMiner)
**vs RNN/LSTM**: Parallel processing (vs sequential), O(1) path length (vs O(n) for long-range), no vanishing gradients
**Status**: ✅ Active - foundational architecture for ALL modern deep learning at BRP
**Related**: [BERT](#bert---bidirectional-encoder-representations-from-transformers), [SBERT](#sbert---sentence-bert), [LLM](#llm---large-language-models), [HGT](#hgt---heterogeneous-graph-transformers), [TGN](#tgn---temporal-graph-network), [GAT](#gat---graph-attention-network), [LSTM](#lstm---long-short-term-memory)

### Attention Mechanism
**Full Name**: Attention Mechanism (Self-Attention, Multi-Head Attention, Scaled Dot-Product Attention)
**Description**: Neural network component computing weighted combinations of **value** vectors based on query-key compatibility, enabling selective focus on relevant parts of the input. Core building block of Transformers — multi-head self-attention replaces sequential RNN processing with parallel, position-independent computation. Types: self-attention (BERT encoder), causal/masked attention (GPT decoder), cross-attention (encoder-decoder models). Efficient variants: Flash Attention (2-4x faster, exact), GQA (grouped KV heads), KV-Cache (autoregressive speedup). Complexity: O(n²d) time — quadratic bottleneck for long sequences.
**Documentation**: [Attention Mechanism Term](../resources/term_dictionary/term_attention_mechanism.md)
**Key Types**: Self-attention (bidirectional), Causal attention (autoregressive), Cross-attention (encoder-decoder)
**Efficient Variants**: Flash Attention, Multi-Query Attention, Grouped-Query Attention, KV-Cache
**Related**: [Transformer](#transformer), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [GNN](#gnn---graph-neural-networks), [GAT](#gat---graph-attention-network), [HGT](#hgt---heterogeneous-graph-transformers)

### Self-Attention
**Full Name**: Self-Attention (Intra-Attention)
**Description**: Special case of attention where queries, keys, and values all derive from the same sequence, enabling each position to attend to all other positions in O(1) operations. Replaces sequential RNN processing with parallel, position-independent computation. Variants: bidirectional (BERT encoder), causal/masked (GPT decoder — prevents attending to future tokens), local/windowed (Longformer). Permutation-equivariant without positional encoding. Complexity: O(n²·d) per layer.
**Documentation**: [Self-Attention Term](../resources/term_dictionary/term_self_attention.md)
**BRP Applications**: BERT-based abuse classifiers (bidirectional), TSA temporal models (transaction sequences), CrossBERT (within buyer/seller representations), graph transformers (HGT/TGN node-level)
**Related**: [Attention Mechanism](#attention-mechanism), [Multi-Head Attention](#multi-head-attention---mha), [Transformer](#transformer), [TSA](#tsa---temporal-self-attention)

### Multi-Head Attention (MHA)
**Full Name**: Multi-Head Attention
**Description**: Attention variant that projects Q, K, V into $h$ parallel subspaces, computes scaled dot-product attention independently in each, then concatenates and projects results: $\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$. Heads specialize in different relational patterns (syntactic, positional, semantic) without explicit supervision. Ablation: single head = -0.9 BLEU (most impactful ablation in the Transformer paper). Efficient variants: MQA (1 shared KV head), GQA (grouped KV heads — LLaMA 2).
**Documentation**: [Multi-Head Attention Term](../resources/term_dictionary/term_multi_head_attention.md)
**Configurations**: Transformer base (h=8, d_k=64), BERT-BASE (h=12, d_k=64), GPT-3 (h=96, d_k=128)
**Related**: [Self-Attention](#self-attention), [Attention Mechanism](#attention-mechanism), [Transformer](#transformer), [BERT](#bert---bidirectional-encoder-representations-from-transformers)

### Positional Encoding (PE)
**Full Name**: Positional Encoding
**Description**: Mechanism for injecting sequence order into Transformers (self-attention is permutation-equivariant). Original: sinusoidal functions $PE_{(pos,2i)} = \sin(pos/10000^{2i/d})$ with linear-transform relative position property. Types: sinusoidal (fixed, 2017), learned embeddings (BERT, 512 max), RoPE (rotary, LLaMA — extrapolates), ALiBi (linear bias, BLOOM — extrapolates). TSA adapts sinusoidal encoding for timestamps (continuous time) rather than discrete positions.
**Documentation**: [Positional Encoding Term](../resources/term_dictionary/term_positional_encoding.md)
**BRP Applications**: BERT models (learned, 512-token limit), TSA TimeEncoder (continuous sinusoidal for irregular transaction intervals)
**Related**: [Transformer](#transformer), [Self-Attention](#self-attention), [Embedding](#embedding), [TSA](#tsa---temporal-self-attention)

### LayerNorm - Layer Normalization
**Full Name**: Layer Normalization
**Description**: Normalizes activations across the feature dimension within each training example: $\text{LayerNorm}(x) = \gamma \cdot (x-\mu)/\sqrt{\sigma^2+\epsilon} + \beta$. Unlike batch normalization, no batch-size dependence — suitable for variable-length sequences. In the Transformer: $\text{LayerNorm}(x + \text{Sublayer}(x))$ after every residual sub-layer. Placement: post-norm (original Transformer, BERT) vs. pre-norm (GPT-2, LLaMA — more stable for deep models). Modern variant: RMSNorm (10-15% faster, used in LLaMA/Mistral).
**Documentation**: [Layer Normalization Term](../resources/term_dictionary/term_layer_normalization.md)
**BRP Applications**: All BERT-based abuse classifiers (post-norm), TSA temporal attention blocks, fine-tuning stability (LayerNorm params typically kept trainable in LoRA/PEFT)
**Related**: [Transformer](#transformer), [Multi-Head Attention](#multi-head-attention---mha), [Fine-Tuning](#fine-tuning), [PEFT](#peft---parameter-efficient-fine-tuning)

### ViT - Vision Transformer
**Full Name**: Vision Transformer ("Transformers for Image Recognition at Scale")
**Description**: **Dominant backbone for Vision Language Models (VLMs)** - applies transformer self-attention directly to image patches without convolutions. Amazon applications: Document VLM (94% vs 51% OCR), BCIvNext (business customer ID), fashion compatibility. Global attention enables multimodal fusion but requires large datasets. Key innovation: treats images as sequences of patches, enabling direct integration with text transformers in VLMs.
**Key Papers**: [ViT (Dosovitskiy et al., 2020)](../resources/papers/lit_dosovitskiy2020image.md) — 88.55% ImageNet at 2-4× less compute than CNNs
**Documentation**: [ViT Term](../resources/term_dictionary/term_vit.md)
**Wiki**: [Computer Vision Working Group](https://w.amazon.com/bin/view/WW-CT-ML-Foundational-Capabilities/Computer_Vision_Working_Group/), [BCIvNext Launch](https://w.amazon.com/bin/view/PSME/TechHub/PSMEMarTech/LaunchAnnouncements/BCIvNext/)
**Architecture**: Transformer encoder applied to image patches (16×16 or 32×32), 86M-632M parameters
**Amazon Applications**: Document VLM (CSSW, 94% accuracy), BCIvNext (first ViT for multivariate time-series), fashion compatibility prediction
**Model Variants**: ViT-B/16 (86M), ViT-L/16 (307M), ViT-H/14 (632M parameters)
**Use Cases**: VLM backbone, multimodal AI, document verification, business customer identification, large-scale image classification
**vs SWIN**: Global vs window-based attention, single-scale vs hierarchical, VLM backbone vs document classification
**vs CNN**: Global receptive field from layer 1, minimal inductive bias, requires larger datasets
**Infrastructure**: SageMaker (training), AMES (serving), Bedrock (foundation models)
**Status**: ✅ Active - standard backbone for Amazon's multimodal AI systems
**Related**: [SWIN Transformer](#swin-transformer---shifted-window-transformer), [Transformer](#transformer), [CNN](#cnn---convolutional-neural-network), [Inductive Bias](#inductive-bias), [VLM](acronym_glossary_llm.md#vlm---vision-language-model), [Computer Vision](acronym_glossary_llm.md#computer-vision---cv)

---

## Advanced ML Techniques

### Meta-Learning
**Full Name**: Meta-Learning (Learning to Learn)
**Description**: ML paradigm that learns how to adapt to new tasks quickly with minimal data by leveraging prior knowledge from related tasks. Enables rapid fraud prevention for new abuse patterns, payment methods, and business launches. **Key benefit**: 5x faster adaptation compared to vanilla RL, enabling early-stage fraud detection with limited data. Critical for BRP's 20+ Alternative Payment Method launches and emerging fraud pattern response.
**Documentation**: [Meta-Learning Term](../resources/term_dictionary/term_meta_learning.md)
**Wiki**: [Meta-Learning Expansion in BRP](https://w.amazon.com/bin/view/Users/chienluc/meta_learning/)
**Related**: [Transfer Learning](../resources/term_dictionary/term_transfer_learning.md), [LoRA](#lora---low-rank-adaptation), [PEFT](#peft---parameter-efficient-fine-tuning)

### HyperNetwork
**Full Name**: HyperNetwork (Weight-Generating Network)
**Description**: Neural network that generates the weights (parameters) of a separate target network, rather than learning fixed weights directly. Introduced by Ha, Dai, and Le (ICLR 2017). Two variants: (1) **Static hypernetworks** for deep ConvNets — relaxed weight-sharing across layers via learned layer embeddings; (2) **Dynamic hypernetworks** (HyperLSTM) — timestep-adaptive weight scaling for recurrent networks. In BAP, hypernetworks are the core mechanism of **CNAPS** (meta-learning model for EU/NA investigation queues), where a FiLM-based adaptation network generates task-specific classifier parameters from small support sets, enabling same-week adaptation to new Alternative Payment Methods instead of months-long data collection. Key insight: instead of training a model *for* a task, train a meta-model that knows *how to configure* a model *given* a task's context.
**Documentation**: [Hypernetwork Term](../resources/term_dictionary/term_hypernetwork.md)
**Paper**: [Ha et al. (2016) — HyperNetworks](../resources/papers/lit_ha2016hypernetworks.md) (ICLR 2017, ~1840 citations)
**BAP Application**: CNAPS-based EU/NA Meta-Learning Model — 751 bps uplift, $3M est. annual savings
**Key Properties**: Weight generation, context conditioning, zero-shot adaptation, parameter efficiency
**Related**: [Meta-Learning](#meta-learning), [LoRA](#lora---low-rank-adaptation), [CNAPS](../resources/term_dictionary/term_cnaps.md), [FiLM](../resources/term_dictionary/term_film.md), [Few-Shot Learning](#few-shot-learning---fsl)

### Few-Shot Learning
**Full Name**: Few-Shot Learning (N-way K-shot Learning)
**Description**: ML paradigm where models generalize to new classes or tasks from only 1–5 labeled examples (the "support set"). In N-way K-shot classification, the model distinguishes among N classes given K examples each. Three main approach families: **metric-based** (Prototypical Networks, Siamese Networks — learn similarity in embedding space), **gradient-based** (MAML — learn initialization for fast fine-tuning), and **hypernetwork-based** (CNAPS — generate task-specific weights in a single forward pass). In BAP, few-shot learning addresses the **cold start problem**: new APMs, new geographies, and emerging fraud patterns arrive with insufficient labeled data for traditional supervised learning. CNAPS-based meta-learning enables same-week model adaptation for 20+ new APM launches across 24+ stores, achieving 751 bps uplift and $3M estimated annual savings. DeepCARE eSNN + FSL++ extends few-shot capabilities for evolving abuse pattern detection.
**Documentation**: [Few-Shot Learning Term](../resources/term_dictionary/term_few_shot_learning.md)
**BAP Application**: CNAPS EU/NA Meta-Learning Model (APM fraud), DeepCARE eSNN + FSL++ (evolving patterns), Siamese Networks (Iridium duplicates)
**Key Methods**: Prototypical Networks (metric), MAML (gradient), CNAPS (hypernetwork), LLM in-context learning (prompting)
**Related**: [Meta-Learning](#meta-learning), [HyperNetwork](#hypernetwork), [CNAPS](../resources/term_dictionary/term_cnaps.md), [Transfer Learning](../resources/term_dictionary/term_transfer_learning.md), [Siamese Network](#siamese-network)

### Agentic Memory
**Full Name**: Agentic Memory (A-MEM)
**Description**: Memory paradigm for LLM agents where the agent has agency over how memories are stored, organized, connected, and evolved — rather than relying on developer-specified schemas or fixed operations. Introduced by Xu et al. (2025) in A-MEM, inspired by the Zettelkasten method. Three-stage pipeline: (1) **Note Construction** — structured notes with LLM-generated keywords, tags, context descriptions, embeddings; (2) **Link Generation** — embedding top-k pre-filter + LLM analysis to establish bidirectional connections; (3) **Memory Evolution** — LLM updates existing memories when new memories arrive, enabling continuous knowledge refinement. Achieves rank 1.0-1.6 across 6 models on LoCoMo/DialSim, 2x+ multi-hop improvement, 85-93% token reduction vs. baselines (MemGPT, MemoryBank). Key distinction: agency at storage/organization level, not just retrieval level.
**Documentation**: [Agentic Memory Term](../resources/term_dictionary/term_agentic_memory.md)
**Paper**: [Xu et al. (2025) — A-MEM: Agentic Memory for LLM Agents](../resources/papers/lit_xu2025amem.md) (arXiv, ~300 citations)
**Key Properties**: Self-organizing, non-parametric, incremental, model-agnostic, token-efficient
**Related**: [Zettelkasten](../resources/term_dictionary/term_zettelkasten.md), [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md), [Prompt Optimization](#prompt-optimization), [RAG](../resources/term_dictionary/term_rag.md), [Continual Learning](#continual-learning)

### Prompt Optimization
**Full Name**: Prompt Optimization (Context Engineering)
**Description**: Automated process of refining LLM input contexts (system prompts, instructions, strategy playbooks) to improve task performance without modifying model weights. Operates entirely in input space — no gradient computation required, enabling 86-91% lower adaptation latency than weight-based methods. Approaches range from discrete search (APE, OPRO) to gradient-inspired text optimization (DSPy, TextGrad) to agentic context engineering (ACE) with structured evolving playbooks. Two key failure modes of prior methods: **brevity bias** (LLM summarization drops domain-specific insights) and **context collapse** (iterative rewriting erodes accumulated knowledge). ACE (Zhang et al., 2025) addresses both via incremental delta updates with non-LLM deterministic merging, achieving +17.1% on AppWorld agent tasks while matching GPT-4.1-based systems with a smaller open-source model (DeepSeek-V3.1).
**Documentation**: [Prompt Optimization Term](../resources/term_dictionary/term_prompt_optimization.md)
**Paper**: [Zhang et al. (2025) — ACE: Agentic Context Engineering](../resources/papers/lit_zhang2025agentic.md) (ICLR 2026, ~68 citations)
**Key Methods**: APE (2022), OPRO (2023), DSPy (2023), TextGrad (2024), MIPROv2 (2024), SPO (2024), Dynamic Cheatsheet (2025), ACE (2025)
**Related**: [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md), [Meta-Learning](#meta-learning), [Few-Shot Learning](#few-shot-learning), [Fine-Tuning](../resources/term_dictionary/term_fine_tuning.md), [RAG](../resources/term_dictionary/term_rag.md)

### Textual Gradient
**Full Name**: Textual Gradient (Natural Language Gradient)
**Description**: Natural language feedback generated by an LLM that serves as the analogue of a numerical gradient in automatic differentiation. Given a variable v and a loss L, the textual gradient ∂L/∂v describes how to modify v to improve L, expressed in natural language rather than as a numerical vector. Introduced by ProTeGi (Pryzant et al., 2023) for prompt optimization and generalized by TextGrad (Yuksekgonul et al., 2024) to arbitrary computation graphs including code, molecules, and treatment plans. Key limitation: no convergence guarantees, and monolithic application can cause context collapse (identified by ACE).
**Documentation**: [Textual Gradient Term](../resources/term_dictionary/term_textual_gradient.md)
**Paper**: [Yuksekgonul et al. (2024) — TextGrad](../resources/papers/lit_yuksekgonul2024textgrad.md) (~109 citations, Stanford)
**Related**: [Prompt Optimization](#prompt-optimization), [Backpropagation](../resources/term_dictionary/term_backpropagation.md), [Gradient Descent](../resources/term_dictionary/term_gradient_descent.md), [Instance Optimization](#instance-optimization), [Compound AI System](#compound-ai-system)

### Compound AI System
**Full Name**: Compound AI System
**Description**: AI application combining multiple interacting components — LLM calls, retrieval modules, code executors, domain-specific tools — orchestrated together to solve complex tasks. The paradigm shift from training individual monolithic models to building multi-component systems where overall behavior emerges from component interactions. Coined by Zaharia et al. (2024). TextGrad (Yuksekgonul et al., 2024) proposes modeling compound AI systems as computation graphs and optimizing them via textual backpropagation. Examples: RAG pipelines, agent systems, scientific AI (LLM + domain simulator).
**Documentation**: [Compound AI System Term](../resources/term_dictionary/term_compound_ai_system.md)
**Paper**: [Yuksekgonul et al. (2024) — TextGrad](../resources/papers/lit_yuksekgonul2024textgrad.md)
**Related**: [RAG](../resources/term_dictionary/term_rag.md), [Textual Gradient](#textual-gradient), [Prompt Optimization](#prompt-optimization), [Self-Evolving Agent](../resources/term_dictionary/term_self_evolving_agent.md)

### Data Flywheel
**Full Name**: Data Flywheel (Data Flywheel Effect)
**Description**: Self-reinforcing cycle where user interactions generate feedback data that improves model training, which improves the product, which attracts more users who generate more data. Borrows the flywheel metaphor from Jim Collins' *Good to Great* (2001) and applies it to AI/ML systems. **Chip Huyen identifies this as the most durable competitive moat for AI applications**, since foundation models commoditize technology and incumbents own distribution. Cold start is the primary barrier: without initial users there is no data, and without data there is no compelling product. Canonical examples include Tesla Autopilot (fleet sensor data), Netflix recommendations (viewing patterns), and Amazon product suggestions (purchase/browse data).
**Documentation**: [Data Flywheel Term](../resources/term_dictionary/term_data_flywheel.md)
**Related**: [Feedback Loop](../resources/term_dictionary/term_feedback_loop.md), [Active Learning](#active-learning), [RLHF](../resources/term_dictionary/term_rlhf.md), [Fine-Tuning](../resources/term_dictionary/term_fine_tuning.md), [Human in the Loop](#human-in-the-loop---interactive-ml-system-design)

### Instance Optimization
**Full Name**: Instance Optimization (Test-Time Optimization)
**Description**: Process of iteratively refining a specific individual solution (code, exam answer, molecule, treatment plan) at test time using textual gradient feedback, as opposed to prompt optimization which finds a single generalizable prompt across queries. Introduced by TextGrad (Yuksekgonul et al., 2024) as the key novel contribution. Textual gradients are applied to the solution variable itself (e.g., a LeetCode solution, a SMILES molecule string) rather than to the system prompt. Results: LeetCode Hard 36% (+5% over Reflexion), GPQA 55% (+4% over CoT), molecules competitive with clinically approved drugs.
**Documentation**: [Instance Optimization Term](../resources/term_dictionary/term_instance_optimization.md)
**Paper**: [Yuksekgonul et al. (2024) — TextGrad](../resources/papers/lit_yuksekgonul2024textgrad.md)
**Related**: [Textual Gradient](#textual-gradient), [Prompt Optimization](#prompt-optimization), [Compound AI System](#compound-ai-system)

### MTL - Multi-Task Learning
**Full Name**: Multi-Task Learning
**Description**: Single model predicting multiple abuse vectors (DNR, PDA, RR, MDR, FLR, PFW enforcement). **BAP's first MTL**: Sept 2023 (MultiTab), May 2024 (MTGBM, 6 tasks). Key benefit: N models → 1, shared learning across vectors. Algorithms: MultiTab (deep learning), MTGBM (LightGBM).
**Documentation**: [MTL Term](../resources/term_dictionary/term_mtl.md)
**Algorithms**: MultiTab (Deep Learning, TabNet-inspired), MTGBM (LightGBM, Zhenzhe et al 2022)
**Current Model**: US MTL 2024-Q2 (`pr-2024-05-03-08652-big-chalk`)
**Tasks**: DNR, PDA, RR, MDR, FLR, PFW Enforcement (6 tasks)
**Launch**: September 2023 (first BAP MTL), May 2024 (expanded to 6 tasks)
**Use Cases**: AFN abuse detection (order-level scoring for multiple vectors simultaneously)
**Key Benefit**: One model vs 6 separate models - reduced maintenance, shared learning across vectors
**Team**: trms-aps@
**Wiki**: [US MTL 2024-Q2](https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/US_MTL_Model_2024Q2/), [US MTL 2023-Q3](https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/US_MTL_Model_2023Q3/)
**Related**: [BEARS](../resources/term_dictionary/term_bears.md), [XGBoost](#xgboost), [LightGBM](#lightgbm), Transfer Learning

### UCM - Unified Concessions Model
**Full Name**: Unified Concessions Model
**Description**: Multi-market, multi-abuse consortium ML model developed by Amazon's International Machine Learning (IML) team for concessions abuse prevention across emerging marketplaces. UCM replaces individual market-specific models with a unified framework that learns from abuse patterns across multiple markets simultaneously, using continual learning techniques with Gradient Episodic Memory (GEM) to adapt without catastrophic forgetting. Production deployment achieved $7MM concession savings and 11 bps reduction in abusive concessions while reducing model refresh cycles by 40% through advanced consortium modeling approach.
**Documentation**: [UCM Term](../resources/term_dictionary/term_ucm.md)
**Wiki**: [UCM MENA 2024](https://w.amazon.com/bin/view/IML-NCL/Unified_Concessions_Model_MENA_2024/), [AMLC 2022 Global Model](https://w.amazon.com/bin/view/Amazon-Science/events/AMLC/2022/Workshops/Workshop_on_Machine_Learning_in_Fraud_Abuse_Credit_Risk_Security_and_Defect/Posters/GlobalModel/)
**Team**: International Machine Learning (IML) - NCL
**Use Cases**: Multi-market abuse prevention, emerging marketplace scaling, cross-market knowledge transfer
**Performance**: $7MM savings, 11 bps concession reduction, 40% fewer refresh cycles
**Status**: ✅ Active - Production deployment across MENA regions (UAE, Saudi Arabia, Egypt)
**Related**: [Continual Learning](../resources/term_dictionary/term_continual_learning.md), [XGBoost](#xgboost), [MOCM](../resources/term_dictionary/term_mocm.md), [GRAF](#graf---graph-based-risk-assessment-functionality)

### MOCM - Multi Objective Concession Model
**Full Name**: Multi Objective Concession Model
**Description**: Machine learning model that jointly optimizes for multiple concession abuse types (DNR, FLR, MDR) simultaneously rather than training separate models per abuse vector. **Learns shared feature representations across abuse types**, improving data efficiency and balancing precision/recall trade-offs across programs. Part of the concessions abuse model family alongside UCM and GRAF, focusing on multi-objective optimization within a single market.
**Documentation**: [MOCM Term](../resources/term_dictionary/term_mocm.md)
**Related**: [UCM](#ucm---unified-concessions-model), [MTL](#mtl---multi-task-learning), [XGBoost](#xgboost), [GRAF](#graf---graph-based-risk-assessment-functionality)

### Active Learning
**Full Name**: Active Learning
**Description**: Machine learning paradigm and optimization technique used in Amazon's buyer abuse prevention to strategically select the most informative samples for manual investigation and labeling, maintaining model performance while drastically reducing human-annotated training data volume. Amazon's breakthrough BDAL (Batch-mode Deep Active Learning) algorithm achieves superior performance using only 3% of investigation budget compared to traditional uncertainty sampling requiring >20% budget. Critical bridge technology enabling transition from real-time manual investigations to automated decision-making while preserving model accuracy, with potential to reduce investigation volume from 1,200K to 50K orders monthly. Developed through 2020 internship research, BDAL uses deep learning architecture with imitation learning to mimic expert investigator decisions through batch selection of multiple complementary samples simultaneously.
**Documentation**: [Active Learning Term](../resources/term_dictionary/term_active_learning.md)
**Wiki**: [Active Learning Research](https://w.amazon.com/bin/view/Users/kruoyan/), [BRP RL Working Group](https://w.amazon.com/bin/view/SPS_RL_Working_Group/)
**Key Innovation**: BDAL algorithm - 3% budget for superior performance vs >20% traditional methods
**Research Team**: Ruoyan Kong (intern), Zhanlong Qiu & Yang Liu (mentors), Scott Nickleach (manager)
**Performance**: 97% reduction in manual investigation volume with improved model accuracy
**Applications**: Investigation assignment optimization, model training enhancement, automation transition support
**Business Impact**: Cost reduction, performance improvement, customer experience enhancement
**Status**: ✅ Research complete - foundational technique for automation transition
**Related**: [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [ARI](../resources/term_dictionary/term_ari.md), [Human in the Loop](#human-in-the-loop---interactive-ml-system-design), [SCAP](#scap---supervised-cluster-abusive-probability), [Continual Learning](../resources/term_dictionary/term_continual_learning.md)

### Human in the Loop - Interactive ML System Design
**Full Name**: Human-in-the-Loop Machine Learning (HITL, HIL)
**Description**: ML paradigm creating symbiotic relationships between human expertise and automated systems, where humans provide feedback and validation for complex cases while machines handle routine tasks at scale. Critical bridge toward full automation in complex domains like fraud prevention, enabling strategic human involvement to accelerate automation goals. At Amazon/BRP, powers DeepCARE's 5% control group (90%+ precision), Payment Risk's enterprise program targeting 100% automation by 2027, and ARI's 22% worldwide automation through human-trained models.
**Documentation**: [Human in the Loop Term](../resources/term_dictionary/term_human_in_the_loop.md)
**Use Cases**: Investigation automation, model validation, feedback loops, progressive automation
**Related**: [Active Learning](#active-learning), [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [AutoSignality](#autosignality)

### Nucleus - Tattletale Detection Pipeline
**Full Name**: Nucleus (Tattletale Detection Pipeline)
**Description**: Weekly batch pipeline detecting new MO patterns. Pipeline: Seeding → **MODE** (clustering) → **EVINCE** (expansion) → **SCAP** (prioritization) → TTUX queues. Infrastructure: Cradle, Step Functions, SageMaker (nucleus-bl-v3).
**Documentation**: [Nucleus Term](../resources/term_dictionary/term_nucleus.md)
**Pipeline**: Seeding → **MODE** (clustering) → **EVINCE** (expansion) → **SCAP** (prioritization) → TTUX
**Infrastructure**: Cradle (batch), Step Functions (orchestration), SageMaker (endpoints), ETLM (features)
**Schedule**: Weekly batch (Monday execution → Thursday queue population → Friday ARM investigation)
**Wiki**: [Tattletale Nucleus](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/Nucleus/)
**Team**: [BAP Tattletale](../resources/teams/team_bap_tattletale.md)
**Related**: [Tattletale](../resources/term_dictionary/term_tattletale.md), [MODE](../resources/term_dictionary/term_mode.md), [EVINCE](../resources/term_dictionary/term_evince.md), [SCAP](#scap---supervised-cluster-abusive-probability)

### MODE - MO Detection Engine
**Full Name**: MO Detection Engine
**Description**: Graph-based behavioral clustering stage (Stage 2) in the Tattletale Nucleus pipeline that groups seed accounts into communities using **17+ linkage attributes** (strong: credit card, address, email, phone; weak: IP, device fingerprint; behavioral: product preferences, order timing, concession velocity) to reveal coordinated MO patterns invisible at the individual account level. MODE discovers **2-3x more abusive accounts** than single-account models by analyzing transitive relationships (accounts 2-3 hops apart in the linkage graph), and produces behavioral embedding vectors alongside the clusters — these embeddings are consumed by **Consensus Clustering (CC)** to address MODE's key limitation of cluster fragmentation (1.6 clusters per MO reduced to 1.2 with CC, +25% completeness). Runs as a weekly batch job on SageMaker endpoint `nucleus-bl-v3` with quarterly retraining, with separate regional models for NA, EU, and FE. The fundamental insight: coordinated MO abusers deliberately keep individual account concession counts below enforcement thresholds — MODE reveals the coordination by finding the shared identity and behavioral signatures that expose the group as a whole.
**Documentation**: [MODE Term](../resources/term_dictionary/term_mode.md)
**Wiki**: [Tattletale Nucleus](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/Nucleus/)
**Pipeline Position**: Seeding → **MODE** → CC/EVINCE → SCAP → TTUX
**Infrastructure**: SageMaker (nucleus-bl-v3), Cradle, Step Functions
**Key Limitation**: Cluster fragmentation (1.6 clusters/MO) → addressed by Consensus Clustering (CC)
**Related**: [Nucleus](#nucleus---tattletale-detection-pipeline), [Tattletale](../resources/term_dictionary/term_tattletale.md), [CC](#cc---consensus-clustering), [EVINCE](../resources/term_dictionary/term_evince.md), [SCAP](#scap---supervised-cluster-abusive-probability), [HDBSCAN](#hdbscan---hierarchical-density-based-clustering), [MAA](../resources/term_dictionary/term_maa.md)

### SCAP - Supervised Cluster Abusive Probability
**Full Name**: Supervised Cluster Abusive Probability
**Description**: ML model within Tattletale detection pipeline that prioritizes and ranks detected suspicious account communities for ARM investigation. Formulated as an active learning problem, SCAP optimizes ARM's limited investigation capacity by predicting which communities have the highest probability of containing true abuse patterns (Modus Operandi). Uses AutoGluon weighted-ensemble model trained on order/concession/Sugar Index/graph features with reward score labels.
**Documentation**: [SCAP Term](../resources/term_dictionary/term_scap.md)
**Pipeline Position**: Seeding → MODE → EVINCE → **SCAP** → TTUX
**Variants**: Risk-based (Q2 2022), Reward-based (Q4 2022), Community-level (2024)
**Performance**: 31% detection account-level yield (offline testing)
**Wiki**: [Tattletale Nucleus](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/Nucleus/)
**Related**: [Tattletale](../resources/term_dictionary/term_tattletale.md), [MODE](../resources/term_dictionary/term_mode.md), [EVINCE](../resources/term_dictionary/term_evince.md), [Active Learning](#active-learning), [Nucleus](#nucleus---tattletale-detection-pipeline)

### PECANS - MO Prevention Model (Legacy)
**Full Name**: Pattern Evaluation for Concession Abuse and Network Scoring
**Description**: Early Modus Operandi (MO) prevention model developed by BAP Tattletale team - one of the first models to prevent known abuse patterns by scoring orders before fulfillment. Used reference-based scoring with K-NN similarity to compare incoming orders to known MO patterns. Superseded by ALMOND (2022) which added adaptive learning and online capability, then NUTS (2023+) which unified prevention approaches. Historical significance: established the pattern of connecting MO detection (Tattletale) to MO prevention.
**Documentation**: [PECANS Term](../resources/term_dictionary/term_pecans.md)
**Status**: ⚠️ Legacy - replaced by NUTS (via ALMOND)
**Evolution**: PECANS (pre-2022) → ALMOND (2022) → NUTS (2023+)
**Wiki**: [Tattletale](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/)
**Related**: [ALMOND](#almond---adaptive-learning-for-mo-detection), [NUTS](../resources/term_dictionary/term_nuts.md), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### ALMOND - Adaptive Learning for MO Detection
**Full Name**: Adaptive Learning for MO Network Detection
**Description**: Multiclass LightGBM predicting **which MO** an order matches (vs PECANS binary). Now unified into NUTS (hierarchical). Real-time PFW scoring: outputs `mo_ticket`, `pred_risk`. Learns adaptively from ARM enforcement. 4 regional models (NA, EU, FE, IN).
**Documentation**: [ALMOND Term](../resources/term_dictionary/term_almond.md)
**Status**: ⚠️ Unified into NUTS framework
**Algorithm**: LightGBM Multiclass (Hierarchical Classification)
**Evolution**: v1 (Autoencoder+k-NN) → v2 (LightGBM) → NUTS (Hierarchical)
**Wiki**: [ALMOND Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ALMOND/)
**Code**: [BADS-Almond](https://code.amazon.com/packages/BADS-Almond/trees/mainline)
**Related**: [PECANS](#pecans---mo-prevention-model-legacy), [NUTS](#nuts---unified-mo-prevention-framework), [LightGBM](#lightgbm), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### NUTS - Unified MO Prevention Framework
**Full Name**: Network-based Unified Tattletale Scoring
**Description**: **Current MO prevention framework** - unifies PECANS (binary) + ALMOND (multiclass) into hierarchical LightGBM. Stage 1: MO/Not, Stage 2-3: Which MO (Top40+Rest). 4 regional models (11→4). Outputs: `mo_ticket`, `pred_risk`. Actions: CAP routing, auto-cancel, ARI queue.
**Documentation**: [NUTS Term](../resources/term_dictionary/term_nuts.md)
**Status**: ✅ Active - current MO prevention framework
**Algorithm**: Hierarchical LightGBM Classification (Miranda et al., 2023)
**Architecture**: Stage 1 (Binary: MO/Not) + Stage 2-3 (Multiclass: Which MO)
**Evolution**: PECANS (binary) + ALMOND (multiclass) → NUTS (unified hierarchical)
**Wiki**: [NUTS/ALMOND Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ALMOND/)
**Regions**: NA, EU, FE, IN (4 models total)
**Actions**: CAP routing, auto-cancellation, ARI queuing
**Related**: [PECANS](#pecans---mo-prevention-model-legacy), [ALMOND](#almond---adaptive-learning-for-mo-detection), [LightGBM](#lightgbm), [Tattletale](../resources/term_dictionary/term_tattletale.md), [PFW](../resources/term_dictionary/term_pfw.md)

### OBE - Outlier Behavior Enumeration
**Full Name**: Outlier Behavior Enumeration
**Description**: Unsupervised system that identifies emerging risky clusters of events by exhaustively monitoring combinations of features commonly found in MO tickets. **OBE flags clusters exceeding a purity threshold without requiring labels or model training**, detecting coordinated entity-level patterns that individual order-scoring models miss. The system automates the intuition of Risk Mining analysts by tracking 28 features and uses sharded cluster generation for scalability.
**Documentation**: [OBE Term](../resources/term_dictionary/term_obe.md)
**Related**: [NUTS](#nuts---unified-mo-prevention-framework), [Nucleus](#nucleus---tattletale-detection-pipeline), [Tattletale](../resources/term_dictionary/term_tattletale.md), [Risk Mining](../resources/term_dictionary/term_risk_mining.md)

### LANTERN - muLti AccouNT abusE oRder caNcellation
**Full Name**: muLti AccouNT abusE oRder caNcellation
**Description**: XGBoost model for **MAA detection on mature accounts (90+ days)** vs PACMAN (0-90 days). Evaluates PFOC based on relationships with known abusers. Features: seed variables (abuser relations), Address Intelligence. Financial impact: $20.2M annual savings (US).
**Documentation**: [LANTERN Term](../resources/term_dictionary/term_lantern.md)
**Wiki**: [MAA Main Wiki](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/MAA/), [MALTA Onboarding](https://w.amazon.com/bin/view/MLAnalyticsOnboarding/MALTA/)
**Dashboard**: [LANTERN Dashboard](https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/dashboards/ec7f331a-c8cb-4e90-84a0-346d9e7e000d), [Analysis](https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/analyses/c7dfe4df-1ea4-4b41-8683-db3727240df4)
**Algorithm**: XGBoost (supervised, regional models)
**Target**: Mature accounts (90+ days) with abuser relationships
**Evaluation**: Real-time at order placement
**Action**: PFOC (Pre-Fulfillment Order Cancellation), CAP routing, ARI queuing
**Regions**: NA, EU, FE (regional models)
**Features**: Seed variables + Address Intelligence (ResidenceID, Geolocation)
**Financial Impact**: US Model $20.2M annual savings (per LTA reference)
**Team**: [MALTA](../resources/term_dictionary/term_malta.md) (Multi-Account and Large Transaction Abuse)
**vs PACMAN**: LANTERN for mature accounts (90+ days), PACMAN for new accounts (0-90 days)
**Status**: ✅ Active - core MAA detection model for PFOC
**Related**: [MAA](#maa---multi-account-abuse), [PACMAN](#pacman---proactive-multi-account-abuse-prevention), [IDA](#ida---identity-association), [COSA](#cosa---continuous-one-step-ahead), [PFOC](../resources/term_dictionary/term_pfoc.md), [PFW](../resources/term_dictionary/term_pfw.md)

### BEARS - Buyer Enforcement Abuse Risk Score
**Full Name**: Buyer Enforcement Abuse Risk Score
**Description**: **Account-level** risk score (vs order-level DNR/MDR models) - answers "should this account be enforced?" XGBoost with sequence features (LSTM/attention) across DNR, MDR, NSR, FLR, RR, MFN. 21 marketplaces, 3 regional models. Use: ARI queue routing, FP filtering.
**Documentation**: [BEARS Term](../resources/term_dictionary/term_bears.md)
**Wiki**: [BEARS Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BEARS/), [Model Reports](https://w.amazon.com/bin/view/Trms/AbuseAnalytics/ModelReports/)
**Algorithm**: XGBoost with sequence features (LSTM/attention for temporal patterns)
**Scope**: Account-level (vs order-level for DNR/MDR models)
**Label Source**: ARI enforcement decisions (Solicit, Warn, Close)
**Regional Models**: NA (US, CA, MX, BR), EU (EU5+), FE (JP, AU, SG), ROW (March 2022)
**Coverage**: 21 marketplaces worldwide
**Evaluation Timing**: Updated at order placement
**Output**: Enforcement probability (0-1)
**Use Cases**: 
  - ARI queue routing (high-risk accounts → investigation)
  - False positive filtering (low BEARS → bypass enforcement)
  - Workflow integration (RI, Post-Concession, BRW, A-to-Z, CAP Referrals)
  - NEAT routing (auto-prioritizes reinstate appeals)
**OTF Variable**: `Abuse.DataSheet.abuse_bears_score_by_customer_id` (NA/EU/FE)
**Redshift**: `trmsdw.o_mds_cas_order_evals`
**External Access**: ORS (Onboarding Risk Services) via Andes table
**Owner**: Buyer-Abuse-RnD (LDAP)
**Team**: [BAP ML Team](../resources/teams/team_bap_ml.md)
**Status**: ✅ Active - core account-level abuse risk model
**Related**: [MTL](#mtl---multi-task-learning), [ARI](../resources/term_dictionary/term_ari.md), [BRW](../resources/term_dictionary/term_brw.md), [CAP](../resources/term_dictionary/term_cap.md), [NEAT](#neat---noise-email-advise-transfer), [XGBoost](#xgboost)

### CD - Community Detection
*Moved to [Network Science Glossary](acronym_glossary_network_science.md#community-detection)* — graph partitioning theory and algorithms. For Tattletale pipeline usage: Seeding → MODE → CD (within EVINCE) → SCAP → TTUX; Greedy Modularity Maximization; +25% MO detection.
**Documentation**: [Community Detection Term](../resources/term_dictionary/term_community_detection.md)
**Related**: [EVINCE](../resources/term_dictionary/term_evince.md), [SCAP](#scap---supervised-cluster-abusive-probability), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### CC - Consensus Clustering
**Full Name**: Consensus Clustering (Ensemble Clustering)
**Description**: Ensemble clustering technique within **Tattletale detection pipeline** that fuses **MODE embeddings** (behavioral similarity) with **physical/behavioral linkages** (SpiderWeb identity signals) into a **consensus matrix**, then applies **HDBSCAN** for density-based clustering that is more stable and complete than MODE alone. Addresses MODE's key limitation of cluster fragmentation (1.6 clusters per MO) by combining behavioral + identity signals, achieving **25% cluster completeness improvement** (UK DNR: clusters per MO from 1.6→1.2) and **28% cluster quality score improvement** (0.19→0.24) for evolving MOs. Launched Q4 2024 in MFN/NCL queues with AFN expansion planned; also enables the **UCC (Unclassified Concessions) program** with 4% account-level yield. CC operates between MODE and EVINCE in the Tattletale pipeline, enriching initial clusters before graph expansion.
**Documentation**: [Consensus Clustering Term](../resources/term_dictionary/term_consensus_clustering.md)
**Wiki**: [Tattletale Program](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/)
**Algorithm**: HDBSCAN on consensus matrix (MODE embeddings + physical/behavioral linkages)
**Pipeline Position**: Seeding → MODE → **CC** → EVINCE → Community Detection → SCAP → TTUX
**Input Signals**: MODE embeddings, SpiderWeb identity linkages, behavioral linkages
**Performance**: 25% cluster completeness improvement, 28% quality score improvement, UCC 4% yield
**⚠️ Disambiguation**: Not CC (Credit Card), CCP (Cluster Cleaning Process), or CCS (Customer Clustering Service)
**Status**: ✅ Active - core clustering enhancement in Tattletale pipeline
**Related**: [CD](#cd---community-detection), [Tattletale](../resources/term_dictionary/term_tattletale.md), [MODE](../resources/term_dictionary/term_mode.md), [EVINCE](../resources/term_dictionary/term_evince.md), [SCAP](#scap---supervised-cluster-abusive-probability)

### HDBSCAN - Hierarchical Density-Based Clustering
**Full Name**: Hierarchical Density-Based Spatial Clustering of Applications with Noise
**Description**: Density-based clustering algorithm that constructs a **hierarchy of clusters at varying density thresholds**, automatically selecting the most stable clusters without requiring k (number of clusters) or ε (density threshold) — only **min_cluster_size** parameter needed. Naturally handles **noise points** (outlier label -1), **varying-density clusters**, and **arbitrary shapes**, making it ideal for abuse detection where MO cluster sizes range from 10 to 200+ accounts with unknown count. In Tattletale, HDBSCAN is the core algorithm in **Consensus Clustering (CC)** applied to the fused consensus matrix (MODE embeddings + SpiderWeb linkages), achieving 25% cluster completeness improvement and 28% quality score improvement. Also powers **MO Governance** lifecycle tracking through incremental hierarchical clustering for pattern birth/split/death/drift analysis.
**Documentation**: [HDBSCAN Term](../resources/term_dictionary/term_hdbscan.md)
**Wiki**: [Tattletale Program](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/)
**Algorithm**: Mutual reachability distance → MST → Hierarchy → Condense → Extract stable clusters (EOM)
**Key Parameter**: min_cluster_size (only required parameter)
**Advantages**: No k required, noise handling, varying densities, hierarchical, stability metric
**vs K-Means**: No k, handles noise/arbitrary shapes; K-Means requires k, forces assignment, convex only
**vs GMM**: No Gaussian assumption; GMM requires k, assumes elliptical distributions
**vs DBSCAN**: No ε needed, handles varying densities; DBSCAN requires ε, single density level
**BRP Applications**: Consensus Clustering (Tattletale, 25%/28% improvement), MO Governance (lifecycle tracking), RASP detection
**Status**: ✅ Active - core clustering algorithm in Tattletale CC and MO Governance
**Related**: [CC](#cc---consensus-clustering), [CD](#cd---community-detection), [MODE](../resources/term_dictionary/term_mode.md), [Tattletale](../resources/term_dictionary/term_tattletale.md), [Embedding](#embedding)

### EV2 - Evaluation Variables 2.0
**Full Name**: Evaluation Variables 2.0 (also: Link Variables 2.0, Abuse Link Variables 2.0)
**Description**: PageRank-style graph propagation algorithm transmitting fraud/abuse risk between customer IDs and 14+ shared identity attributes (credit card, IP, device, UBID, fingerprint, email, address, phone, session) — known abuser labels propagate iteratively through the attribute bipartite graph so that customers sharing attributes with abusers inherit elevated risk scores even without direct enforcement history ("guilt by association"). **Abuse EV2** (BAP/MAA team, launched Q2 2022) uses **abuse-specific input tags** (DNR/MDR/FLR Sugar Index, order ratios, 24-month account closure status) to generate 500+ daily-refreshed OTF variables deployed across all major BAP intents (PFW, CAP, RFS, Secure Delivery, A-to-Z) in 21 marketplaces. The pipeline runs via Cradle/OACIS and serves through OTF+FeatureHub (migrated from DataWave+Tugboat in 2024). EV2 variables **substitute CCS variables** in refreshed DNR/MDR models, making EV2 one of the top features in BAP's abuse detection stack.
**Documentation**: [EV2 Term](../resources/term_dictionary/term_ev2.md)
**Wiki**: [Abuse EV2 Wiki](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/MAA/Abuse-EV2/), [CoRe EV2 Wiki](https://w.amazon.com/bin/view/Ohio/COreRElations/EV2/)
**Algorithm**: PageRank-style iterative risk propagation (bipartite: CID ↔ 14+ attribute types, 150-day window)
**Key Variables**: `dnrSi_evWMaxLinkScore`, `mdrOrderSi_evWMeanLinkScore`, `abuseStatus_evWLinkScore`
**Refresh**: Daily batch; 8-20h lag; Cradle/OACIS
**Slack**: #abuse-ev2-interest
**Related**: [GNN](#gnn---graph-neural-networks), [MAA](../resources/term_dictionary/term_maa.md), [OTF](../resources/term_dictionary/term_otf.md), [CoRe](../resources/term_dictionary/term_core.md), [GENIE](../resources/term_dictionary/term_genie.md), [VTAG](../resources/term_dictionary/term_vtag.md)

### Clustering
**Full Name**: Clustering (Unsupervised Machine Learning)
**Description**: Unsupervised ML technique grouping data points by similarity without predefined labels — one of the most critical techniques in BAP for detecting coordinated fraud networks that individual account-level models miss. In BRP/BAP, clustering operates across four paradigms: **graph-based behavioral clustering** (MODE: 17+ linkage attributes, 2-3x more abusive accounts discovered), **density-based clustering** (HDBSCAN in Consensus Clustering: reduces cluster fragmentation from 1.6→1.2 per MO, +25% completeness), **account identity clustering** (CCS: links accounts sharing credit cards/devices/addresses for MAA detection), and **text/annotation clustering** (K-means in GoldMiner: converts 10M+ investigator annotations into structured reason codes). The fundamental value is revealing **emergent group patterns**: bad actors deliberately keep individual behaviors below enforcement thresholds, but clustering exposes coordinated signatures — enabling the ~$40-60M annual MO prevention in BRP that would be impossible through single-account detection alone.
**Documentation**: [Clustering Term](../resources/term_dictionary/term_clustering.md)
**Wiki**: [Tattletale Program](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/Tattletale/)
**Core Algorithms**: Graph clustering (MODE), HDBSCAN (CC), K-means (GoldMiner), Greedy Modularity (Community Detection), CCS identity linking
**Key BAP Applications**: MO detection (Tattletale), MAA account linking (CCS), annotation analysis (GoldMiner)
**Related**: [HDBSCAN](#hdbscan---hierarchical-density-based-clustering), [CC](#cc---consensus-clustering), [MODE](../resources/term_dictionary/term_mode.md), [CD](#cd---community-detection), [CCS](../resources/term_dictionary/term_ccs.md), [Tattletale](../resources/term_dictionary/term_tattletale.md), [GoldMiner](#goldminer---annotation-processor)

### Anomaly Detection
**Full Name**: Anomaly Detection (Outlier Detection, Novelty Detection, One-Class Classification)
**Description**: ML techniques identifying data points that deviate significantly from expected behavior — essential for fraud/abuse detection where anomalies are rare, diverse, and evolving. Methods span statistical (Z-score), distance-based (LOF), tree-based (Isolation Forest), one-class (Deep SVDD, DeepSAD), reconstruction-based (autoencoders, VAE), and graph-based (GNN + AD). BRP applications: PDA Anomaly Detection (Z-score, 47% vs 9% yield), D3 Data Drift Detector (600K+ metrics), autoencoder embeddings for DNR. Key challenge: extreme class imbalance — AUPRC preferred over AUROC when anomaly rate <1%.
**Documentation**: [Anomaly Detection Term](../resources/term_dictionary/term_anomaly_detection.md)
**Key Methods**: Isolation Forest, LOF, Deep SVDD, DeepSAD, Autoencoders, Z-score
**BRP Applications**: PDA Anomaly Detection (47% yield), D3 (600K+ metrics), DNR autoencoder embeddings
**Related**: [Clustering](#clustering), [HDBSCAN](#hdbscan---hierarchical-density-based-clustering), [GNN](#gnn---graph-neural-networks), [Active Learning](#active-learning), [Contrastive Learning](#contrastive-learning)

### Contrastive Learning
**Full Name**: Contrastive Learning (Contrastive Representation Learning)
**Description**: Learns embeddings by contrasting similar vs dissimilar pairs - high-quality representations without expensive labeling. Frameworks: SimCLR, MoCo, SimCSE. BRP applications: eSNN ($10MM fraud reduction), SEC (AMLC 2023), GoldMiner (22%→32% automation), AutoSignality (+100 bps AUC).
**Documentation**: [Contrastive Learning Term](../resources/term_dictionary/term_contrastive_learning.md)
**Wiki**: [SEC AMLC 2023](https://w.amazon.com/bin/view/AMLC_2023_Workshop_of_Multi-Objective_Decision_Making_under_Uncertainty/SEC_Sentence_Embedding_Via_Contrastive_Learning_In_Return_Annotation/), [DeepCARE ESNN](https://w.amazon.com/bin/view/URES/URESAutomation/AutomationEvaluation/ESNN/)
**Loss Functions**: InfoNCE, Triplet Loss, NT-Xent, Supervised Contrastive
**Major Frameworks**: SimCLR, MoCo, BYOL, SwAV, SimCSE
**BRP Applications**: SEC, eSNN/DeepCARE, SBERT/GoldMiner, TabNet SupCon, Product DNA
**Key Advantage**: High-quality embeddings from unlabeled/weakly-labeled data
**Best For**: Embedding generation, similarity search, clustering, transfer learning
**Status**: ✅ Active - foundational technique for BRP embedding generation
**Related**: [eSNN](#esnn---extended-siamese-neural-network), [SBERT](#sbert---sentence-bert), [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [GoldMiner](#goldminer---annotation-processor), [Siamese Network](#siamese-network), Self-supervised Learning, Metric Learning

### KD - Knowledge Distillation
**Full Name**: Knowledge Distillation (Model Distillation, Teacher-Student Learning)
**Description**: Model compression and knowledge transfer technique where a small **student** network is trained to reproduce the behavior of a larger **teacher** network (or ensemble) by learning from temperature-scaled **soft targets** — the teacher's full output probability distribution — which encode inter-class similarity structure (**dark knowledge**). Formalized by Hinton et al. (2015). Three knowledge types: **response-based** (logit matching), **feature-based** (intermediate layer matching, FitNets), **relation-based** (structural/pairwise similarity). Three schemes: **offline** (frozen teacher), **online** (mutual learning), **self-distillation** (self-referential). Critical for deploying large sparse MoE models as dense models: Switch Transformer distills 7.4B sparse → 223M dense preserving 30% of quality gains (Fedus et al., 2022). Also foundational for LLM compression: DistilBERT (97% GLUE at 60% size), TinyBERT (96.8% at 13% size). Paradigm: **train large, deploy small**.
**Documentation**: [Knowledge Distillation Term](../resources/term_dictionary/term_knowledge_distillation.md)
**Key Methods**: Hinton KD (2015), FitNets (2015), Attention Transfer (2017), DML (2018), Born-Again Networks (2018), DistilBERT (2019), TinyBERT (2020), CRD (2020)
**BRP Relevance**: Compress large abuse detection models (BERT, MoE) to meet <10ms AMES latency; distill ensembles into single models; sparse-to-dense deployment
**Related**: [MoE](#moe---mixture-of-experts), [Transfer Learning](#transfer-learning), [Contrastive Learning](#contrastive-learning), [Transformer](#transformer), [Scaling Law](../resources/term_dictionary/term_scaling_law.md), [Conditional Computation](../resources/term_dictionary/term_conditional_computation.md)

### SSL - Self-Supervised Learning
**Full Name**: Self-Supervised Learning
**Description**: ML paradigm deriving supervisory signals from the structure of unlabeled data itself — no external human annotations required. Constructs **pretext tasks** (masked token prediction, next token prediction, contrastive augmentations) that generate pseudo-labels from the data. SSL is the dominant paradigm behind modern foundation models: BERT (masked token prediction), GPT (next token prediction), SimCLR/MoCo (contrastive vision), CLIP (image-text matching). Families: generative/predictive (MLM, autoregressive LM), contrastive (InfoNCE objective), non-contrastive (BYOL, SimSiam), masked prediction in vision (MAE). SSL pre-trains transferable representations that are then fine-tuned on downstream tasks.
**Documentation**: [SSL Term](../resources/term_dictionary/term_ssl.md)
**Key Methods**: MLM (BERT), Autoregressive LM (GPT), SimCLR, MoCo, BYOL, MAE, CLIP
**BRP Relevance**: BERT-based abuse detection models initialized from SSL pre-training (MLM), then fine-tuned on abuse classification data
**Related**: [Contrastive Learning](#contrastive-learning), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Transfer Learning](#transfer-learning), [Embedding](#embedding)

### SimCLR - Simple Framework for Contrastive Learning of Visual Representations
**Full Name**: Simple Framework for Contrastive Learning of Visual Representations
**Description**: Self-supervised contrastive learning framework (Chen et al., Google, ICML 2020) that learns visual representations by maximizing agreement between differently augmented views of the same image. Uses four components: stochastic data augmentation, ResNet-50 encoder, projection head (2-layer MLP), and **NT-Xent contrastive loss** (normalized temperature-scaled cross-entropy). The key insight is that augmentation composition matters more than architecture — random crop with color distortion is critical. Benefits from large batch sizes (up to 8192) for more negative pairs.
**Documentation**: [SimCLR Term](../resources/term_dictionary/term_simclr.md)
**Related**: [Contrastive Learning](#contrastive-learning), [SSL](#ssl---self-supervised-learning), [SSCD](#sscd---self-supervised-copy-detection), [DINO](#dino---self-distillation-with-no-labels)

### SSCD - Self-Supervised Copy Detection
**Full Name**: Self-Supervised Copy Detection
**Description**: Image copy detection model (Pizzi et al., Meta, CVPR 2022) producing compact 512-dimensional descriptors optimized for detecting near-duplicate and manipulated image copies. Adapts contrastive learning with **copy-aware augmentations** (mixup, cutmix) that simulate partial copies, GeM pooling for spatial aggregation, and entropy regularization to prevent dimensional collapse. Outperforms SimCLR descriptors by 48% absolute on the DISC2021 benchmark.
**Documentation**: [SSCD Term](../resources/term_dictionary/term_sscd.md)
**Related**: [SimCLR](#simclr---simple-framework-for-contrastive-learning-of-visual-representations), [Contrastive Learning](#contrastive-learning), [Deep Metric Learning](#deep-metric-learning)

### DINO - Self-Distillation with No Labels
**Full Name**: Self-Distillation with No Labels
**Description**: Self-supervised learning method for Vision Transformers (Caron et al., Meta, ICCV 2021) using self-distillation — a student network learns to match a momentum-updated teacher on different augmented views. The key discovery is that **ViT attention maps spontaneously segment objects** without any segmentation supervision. Uses multi-crop strategy (global crops to teacher, local crops to student) with centering and sharpening to prevent collapse. DINOv2 (2023) scales the approach with curated data and register tokens for universal visual features.
**Documentation**: [DINO Term](../resources/term_dictionary/term_dino.md)
**Related**: [SSL](#ssl---self-supervised-learning), [SimCLR](#simclr---simple-framework-for-contrastive-learning-of-visual-representations), [Knowledge Distillation](../resources/term_dictionary/term_knowledge_distillation.md), [ViT](acronym_glossary_llm.md#vit---vision-transformer)

### Deep Metric Learning
**Full Name**: Deep Metric Learning (DML)
**Description**: Training paradigm that learns neural network embeddings where semantically similar items are close and dissimilar items are far apart — optimizing distance relationships rather than discrete class labels. Core loss functions include **triplet loss** (anchor-positive-negative with margin), contrastive loss (positive-negative pairs), and NT-Xent. Critical techniques: hard negative mining, GeM pooling (learnable generalized mean), L2 normalization, and PK batch sampling. Originated from face recognition (FaceNet, 2015) and expanded to image retrieval, copy detection, and product matching.
**Documentation**: [Deep Metric Learning Term](../resources/term_dictionary/term_deep_metric_learning.md)
**Related**: [SimCLR](#simclr---simple-framework-for-contrastive-learning-of-visual-representations), [Contrastive Learning](#contrastive-learning), [Embedding](#embedding), [k-NN](#k-nn---k-nearest-neighbors)

### LoFTR - Detector-Free Local Feature Matching with Transformers
**Full Name**: Detector-Free Local Feature Matching with Transformers
**Description**: Detector-free method for local feature matching (Sun et al., CVPR 2021) that uses Transformer self-attention and cross-attention to establish dense correspondences between image pairs without keypoint detection. Operates coarse-to-fine: CNN features at 1/8 resolution → Transformer matching → sub-pixel refinement. **Robust to low-texture regions and repetitive patterns** where traditional detectors (SIFT, SuperPoint) fail. se2LoFTR adds rotation equivariance; Efficient LoFTR achieves sparse-like speed with linear attention.
**Documentation**: [LoFTR Term](../resources/term_dictionary/term_loftr.md)
**Related**: [Deep Metric Learning](#deep-metric-learning), [Computer Vision](acronym_glossary_llm.md#computer-vision---cv), [DINO](#dino---self-distillation-with-no-labels)

### CP - Conformal Prediction
**Full Name**: Conformal Prediction (Conformal Inference, Distribution-Free Prediction Sets)
**Description**: Statistical framework creating **valid uncertainty intervals** (prediction sets) for ML predictions with **guaranteed coverage probability** — the true label is within the set ≥(1-α)% of the time, regardless of model or data distribution. **Distribution-free** and **model-agnostic** (works with XGBoost, k-NN, LLM), providing per-prediction confidence vs traditional summary metrics (AUC, Precision). Applied to **DeepCARE's k-NN stage** by SWAT team, improving precision from **84% to 97%** at same 30% automation rate while guaranteeing zero "close/warn" cases auto-passed. AWS open-source **Fortuna** library (Dec 2022) provides CP implementations; proposed for URES onboarding as standard confidence layer across BAP models.
**Documentation**: [Conformal Prediction Term](../resources/term_dictionary/term_conformal_prediction.md)
**Wiki**: [Fortuna Launch](https://github.com/aws-labs/fortuna)
**Key Properties**: Distribution-free, model-agnostic, finite-sample valid, coverage guarantee, adaptive set size
**BRP Application**: DeepCARE k-NN precision 84%→97% at 30% automation; proposed URES standard integration
**vs Bayesian**: CP = finite-sample guarantee + model-agnostic + low cost; Bayesian = asymptotic only + architecture-specific + high cost
**Fortuna Library**: AWS open-source (Dec 2022) — CP + Bayesian methods for uncertainty quantification
**Status**: ✅ Research complete with production-ready results — proposed for URES onboarding
**Related**: [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [k-NN](#k-nn---k-nearest-neighbors), [Precision](#precision), [False Positive](#false-positive---type-i-error--over-enforcement), [URES](../resources/term_dictionary/term_ures.md)

### Causal Inference
**Full Name**: Causal Inference (CI)
**Description**: Statistical and ML methodologies that estimate the causal effect of an action on an outcome — answering "what would happen if we acted differently?" (counterfactual) rather than "what outcome will occur?" (predictive). In BRP/BAP, causal inference underpins three key applications: (1) **DSI measurement** — treatment-control matching to quantify how enforcement actions (closures, warnings, Secure Delivery) affect customer value over 30–270 day horizons; (2) **HonestSpot uplift modeling** — identifying the 60% of falsely-enforced customers who silently abandon rather than reinstating, with top 20% predicted silent customers showing 2.26x higher abandonment rates; and (3) **MFN fault attribution** — T/X-Learner and Q-Learning to distinguish buyer vs seller responsibility in RFS suppression. The core challenge is the fundamental counterfactual problem: only one outcome (enforce or pass) is observed per customer, making treatment effect estimation — formalized as CATE: τ(x) = E[Y_treatment - Y_control | x] — inherently difficult. Key methods include uplift random forests, meta-learners (T/S/X-Learner), treatment-control matching, regression discontinuity design (RDD), and A/B testing via Weblab.
**Documentation**: [Causal Inference Term](../resources/term_dictionary/term_causal_inference.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/CausalMLvsRL/
**Key Applications**: DSI, HonestSpot (silent FP), Causal ML vs RL (fault attribution), Seq2DSI
**Key Methods**: Uplift RF, T/X-Learner, Treatment-Control Matching, RDD, Weblab A/B Testing
**Key Libraries**: CausalML, EconML, scikit-uplift
**Related**: [DSI](../resources/term_dictionary/term_dsi.md), [Weblab](../resources/term_dictionary/term_weblab.md), [XGBoost](#xgboost), [RL](#rl---reinforcement-learning), [Active Learning](#active-learning), [False Positive](#false-positive---type-i-error--over-enforcement)

### Continual Learning
**Full Name**: Continual Learning (Incremental Learning, Lifelong Learning)
**Description**: Machine learning paradigm enabling models to continuously acquire new knowledge and adapt to changing data distributions without catastrophically forgetting previously learned information. Critical for fraud detection where abuse patterns constantly evolve and retraining from scratch is computationally expensive. Key algorithms include Gradient Episodic Memory (GEM) and Elastic Weight Consolidation (EWC) that balance stability (retaining past knowledge) and plasticity (learning new patterns). BRP applications include UCM (40% reduction in refresh cycles), TSA models, and XGBoost-M variant for tree-based continual learning, enabling adaptive fraud detection systems that maintain performance on recurring abuse patterns.
**Documentation**: [Continual Learning Term](../resources/term_dictionary/term_continual_learning.md)
**Wiki**: [BRP Continual Learning](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/ContinualLearning/), [Alexa SAIF](https://w.amazon.com/bin/view/Alexa-AI-Homepage/SAIF/Compute/Science/IncrementalLearning/)
**Key Algorithms**: GEM (Gradient Episodic Memory), EWC (Elastic Weight Consolidation), HAT (Hard Attention to Task)
**Applications**: UCM (cross-market learning), TSA (temporal pattern preservation), TGN/COSA (large-scale graph adaptation)
**Performance**: 40% reduction in model refresh cycles, better OOT performance on recurring patterns
**Status**: ✅ Active - Core technique for adaptive ML systems in dynamic fraud environments
**Related**: [UCM](#ucm---unified-concessions-model), [Neural Networks](../resources/term_dictionary/term_neural_networks.md), [Transfer Learning](#transfer-learning), [Active Learning](#active-learning), [Catastrophic Forgetting](#catastrophic-forgetting)

### Catastrophic Forgetting
**Full Name**: Catastrophic Forgetting (Catastrophic Interference)
**Description**: Phenomenon where neural networks abruptly lose previously learned knowledge when trained on new data, as gradient updates overwrite weights critical for old tasks. **Central challenge motivating continual learning research at BRP**, where retrained abuse models forget older MO patterns that bad actors then exploit. Mitigation strategies include regularization (EWC, LwF), replay (experience replay, generative replay via diffusion models), and architecture-based methods. Also the primary reason RAG has become dominant over fine-tuning for LLM knowledge updates.
**Documentation**: [Catastrophic Forgetting Term](../resources/term_dictionary/term_catastrophic_forgetting.md)
**Wiki**: [BRP Continual Learning](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/ContinualLearning/)
**Related**: [Continual Learning](#continual-learning), [Transfer Learning](#transfer-learning), [RAG](#rag---retrieval-augmented-generation), [HippoRAG](#hipporag---hippocampus-inspired-retrieval-augmented-generation)

---

## Vector Search, Quantization & Similarity Technologies

### PCA - Principal Component Analysis
**Full Name**: Principal Component Analysis
**Description**: Linear dimensionality reduction (Pearson 1901, Hotelling 1933) that projects data onto orthogonal axes maximizing variance. **The most widely-used dimensionality reduction method.** Computes eigenvectors of the covariance matrix; eigenvalues indicate variance per component. Variants: kernel PCA (nonlinear), sparse PCA (interpretable), randomized PCA (fast). Also known as Karhunen-Loève transform (signal processing), SVD (linear algebra).
**Documentation**: [PCA Term](../resources/term_dictionary/term_pca.md)
**Related**: [CCA](#cca---canonical-correlation-analysis), [Dimensionality Reduction](#dimensionality-reduction), [JL Lemma](#jl-lemma---johnson-lindenstrauss-lemma)

### CCA - Canonical Correlation Analysis
**Full Name**: Canonical Correlation Analysis
**Description**: Multivariate method (Hotelling 1936) finding linear combinations of **two variable sets** with maximum correlation. **Extends PCA from single-set variance maximization to cross-set correlation maximization.** Modern deep CCA (DCCA) learns nonlinear projections. CLIP's contrastive objective can be viewed as a nonlinear, stochastic generalization of CCA for image-text alignment.
**Documentation**: [CCA Term](../resources/term_dictionary/term_cca.md)
**Related**: [PCA](#pca---principal-component-analysis), [Dimensionality Reduction](#dimensionality-reduction), [CLIP](acronym_glossary_llm.md#clip---contrastive-language-image-pre-training)

### Dimensionality Reduction
**Full Name**: Dimensionality Reduction
**Description**: Transforming data from high-dimensional to lower-dimensional space while preserving meaningful properties. **Addresses the curse of dimensionality.** Methods: linear (PCA, random projection), nonlinear/manifold (t-SNE, UMAP), neural (autoencoders), feature selection. JL lemma provides theoretical guarantees for random projection-based reduction.
**Documentation**: [Dimensionality Reduction Term](../resources/term_dictionary/term_dimensionality_reduction.md)
**Related**: [PCA](#pca---principal-component-analysis), [CCA](#cca---canonical-correlation-analysis), [JL Lemma](#jl-lemma---johnson-lindenstrauss-lemma), [ANN](#ann---approximate-nearest-neighbor-search)

### ANN - Approximate Nearest Neighbor Search
**Full Name**: Approximate Nearest Neighbor Search
**Description**: Problem of finding points close to a query in high-dimensional space, relaxing exactness for sublinear query time. **Essential for billion-scale vector databases where brute-force $O(nd)$ is prohibitive.** Four main method families: graph-based (HNSW), partition-based (IVF), hash-based (LSH), and quantization-based (PQ, RaBitQ). HNSW dominates in practice for recall-speed tradeoff; IVF-PQ is the production standard for memory-constrained settings.
**Documentation**: [ANN Search Term](../resources/term_dictionary/term_ann_search.md)
**Related**: [LSH](#lsh---locality-sensitive-hashing), [VQ](#vq---vector-quantization), [FAISS](acronym_glossary_llm.md#faiss---facebook-ai-similarity-search)

### JL Lemma - Johnson-Lindenstrauss Lemma
**Full Name**: Johnson-Lindenstrauss Lemma
**Description**: Fundamental result (1984) showing $n$ points in high-dimensional space can be embedded in $O(\log n / \varepsilon^2)$ dimensions preserving all pairwise distances within $(1 \pm \varepsilon)$. **Target dimension depends only on $\log n$, not the original dimension $d$.** Random matrices provide the projection. Foundation for LSH, compressed sensing, and modern quantization methods. **QJL (Quantized JL)** extends to 1-bit codes, used in TurboQuant for unbiased inner product correction.
**Documentation**: [JL Lemma Term](../resources/term_dictionary/term_johnson_lindenstrauss_lemma.md)
**Related**: [LSH](#lsh---locality-sensitive-hashing), [VQ](#vq---vector-quantization), [ANN](#ann---approximate-nearest-neighbor-search)

### LSH - Locality-Sensitive Hashing
**Full Name**: Locality-Sensitive Hashing
**Description**: Family of randomized hashing techniques where **similar items map to the same hash bucket with high probability** — enabling sublinear-time ANN search. Hash families include SimHash (cosine via random hyperplanes), MinHash (Jaccard via random permutations), and cross-polytope (Euclidean). Introduced by Indyk & Motwani (1998). Applications: ANN search, duplicate detection, clustering, audio fingerprinting.
**Documentation**: [LSH Term](../resources/term_dictionary/term_lsh.md)
**Key Paper**: Indyk & Motwani (1998, STOC)
**Related**: [ANN](#ann---approximate-nearest-neighbor-search), [JL Lemma](#jl-lemma---johnson-lindenstrauss-lemma), [VQ](#vq---vector-quantization)

### PQ - Product Quantization
**Full Name**: Product Quantization
**Description**: Vector compression technique (Jégou et al., 2011) that decomposes D-dimensional vectors into M subvectors, each quantized independently via k-means codebooks. **Dominant compression method for billion-scale ANN search** (FAISS IVF-PQ). Enables lookup-table distance computation ($O(M)$ instead of $O(D)$) with dramatic memory reduction. Data-dependent (requires k-means training); no theoretical error bounds (unlike RaBitQ). Note: not to be confused with PQ (Product Quality) in abuse prevention.
**Documentation**: [Product Quantization Term](../resources/term_dictionary/term_product_quantization.md)
**Related**: [VQ](#vq---vector-quantization), [IVF](#ivf---inverted-file-index), [ANN](#ann---approximate-nearest-neighbor-search), [FAISS](acronym_glossary_llm.md#faiss---facebook-ai-similarity-search)

### IVF - Inverted File Index
**Full Name**: Inverted File Index
**Description**: Partition-based ANN indexing structure that divides vector space into C Voronoi cells via k-means, then searches only the nprobe nearest cells at query time. **Rarely used alone — serves as coarse partitioning combined with PQ (IVF-PQ) or HNSW (IVF-HNSW).** IVF-PQ is the production standard for billion-scale search in FAISS. The "inverted file" concept is borrowed from text information retrieval.
**Documentation**: [IVF Term](../resources/term_dictionary/term_ivf.md)
**Related**: [PQ](#pq---product-quantization), [ANN](#ann---approximate-nearest-neighbor-search), [FAISS](acronym_glossary_llm.md#faiss---facebook-ai-similarity-search), [IR](#ir---information-retrieval)

### IR - Information Retrieval
**Full Name**: Information Retrieval
**Description**: Field concerned with finding relevant documents/passages from large collections, ranking results by relevance rather than returning exact matches. **Spans lexical (BM25, TF-IDF via inverted indices) and dense/neural methods (DPR, ColBERT via embeddings + ANN).** Founded by Mooers (1950) and Salton (1960s). Modern IR provides the "R" in RAG — retrieval-augmented generation connects IR to LLMs. Evaluation: precision, recall, nDCG.
**Documentation**: [Information Retrieval Term](../resources/term_dictionary/term_information_retrieval.md)
**Related**: [ANN](#ann---approximate-nearest-neighbor-search), [IVF](#ivf---inverted-file-index), [LSH](#lsh---locality-sensitive-hashing), [VQ](#vq---vector-quantization), [Cosine Similarity](#cosine-similarity)

### Cosine Similarity
**Full Name**: Cosine Similarity
**Description**: Magnitude-invariant similarity score between two vectors equal to the cosine of the angle between them — the dot product divided by the product of L2 norms. **The dominant scoring function for dense retrieval and the basis of contrastive embedding training**, because it makes similarity insensitive to vector length (which would otherwise bias longer documents). Reduces to a single dot product when both vectors are L2-normalized — the optimization that makes Tier-1 dense search fast (one matrix-vector multiply against pre-normalized corpus embeddings).
**Documentation**: [Cosine Similarity Term](../resources/term_dictionary/term_cosine_similarity.md)
**Related**: [IR](#ir---information-retrieval), [ANN](#ann---approximate-nearest-neighbor-search), [LSH](#lsh---locality-sensitive-hashing)

### VQ - Vector Quantization
**Full Name**: Vector Quantization
**Description**: Technique from Shannon's source coding theory that maps high-dimensional continuous vectors to a finite codebook, minimizing distortion. **Includes Product Quantization (PQ) for ANN search, GPTQ/AWQ for LLM weights, and RaBitQ/TurboQuant for randomized near-optimal compression.** Data-dependent methods (PQ, GPTQ) learn codebooks; data-oblivious methods (RaBitQ, TurboQuant) use random rotation. Foundation: Lloyd-Max algorithm, distortion-rate theory.
**Documentation**: [VQ Term](../resources/term_dictionary/term_vector_quantization.md)
**Related**: [ANN](#ann---approximate-nearest-neighbor-search), [LSH](#lsh---locality-sensitive-hashing), [JL Lemma](#jl-lemma---johnson-lindenstrauss-lemma), [RaBitQ](acronym_glossary_llm.md#rabitq---randomized-bit-quantization), [TurboQuant](acronym_glossary_llm.md#turboquant---online-vector-quantization-with-near-optimal-distortion)

> **See also**: [LLM Glossary](acronym_glossary_llm.md) for LLM-specific quantization methods (RaBitQ, TurboQuant, GPTQ, AWQ, PTQ, QLoRA) and vector search tools (FAISS, HNSW, Embedding)

---


## ML Algorithms & Frameworks

### XAI - Explainable AI
**Full Name**: Explainable AI (Explainable Artificial Intelligence)
**Description**: AI systems designed to provide human-understandable explanations for their decisions, predictions, and behaviors, enabling users to comprehend, trust, and effectively manage AI-driven processes. At Amazon, XAI serves critical functions across buyer abuse prevention and fraud detection by generating natural language explanations for ML model decisions, enabling human investigators to understand why customers are flagged as high-risk. Demonstrated through Phi-3.5-mini FAISS experiment achieving 60x cost reduction compared to cloud alternatives with complete local processing privacy. Bridges the gap between complex AI systems and human decision-makers through interpretable outputs supporting audit compliance, trust building, and knowledge transfer.
**Documentation**: [XAI Term](../resources/term_dictionary/term_xai.md)
**Wiki**: [AGI xAI Toolkit](https://w.amazon.com/bin/view/AGI/xAI/xAIToolkit/), [LESS Toolkit](https://w.amazon.com/bin/view/AGI/xAI/xAIToolkit/LESS/)
**Organization**: Amazon AGI with cross-organizational initiatives
**BAP Applications**: Investigation support, fraud detection explanations, decision transparency, audit compliance
**Cost Benefits**: 60x cost reduction through local processing (Phi-3.5-mini experiment)
**Key Methods**: LIME, SHAP, attention visualization, natural language generation
**Related**: [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [k-NN](#k-nn---k-nearest-neighbors), [FAISS](#faiss---facebook-ai-similarity-search), [LLM](#llm---large-language-models)

### Transfer Learning
**Full Name**: Transfer Learning
**Description**: A machine learning paradigm that reuses knowledge from a source task or domain (via pre-trained weights or embeddings) to accelerate and improve model performance on a related target task — dramatically reducing labeled data requirements. In BAP/BRP, transfer learning solves the cold-start problem for new marketplace launches, where it initializes risk models from US/EU-trained checkpoints rather than training from scratch; fine-tunes pre-trained BERT models for investigation automation (e.g., NEAT Transfer Model achieves 98% precision across 20+ marketplaces); and enables few-shot onboarding of new abuse intents (DeepCARE-FSL). The adversarial domain adaptation approach **GlobalLearn** (AMLC 2019) demonstrated transfer across multiple Amazon business domains simultaneously, achieving a promising path to global fraud detection. Transfer learning is the foundational enabler of Amazon's global abuse prevention scale: without it, every new market and new abuse vector would require months of data collection before any ML model could deploy.
**Documentation**: [Transfer Learning Term](../resources/term_dictionary/term_transfer_learning.md)
**Use Cases**: Cross-marketplace model initialization, BERT/LLM fine-tuning for NLP, few-shot new intent onboarding, offline RL policy initialization (LBP)
**Related**: [MTL](#mtl---multi-task-learning), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Continual Learning](#continual-learning), [Active Learning](#active-learning), [NEAT](#neat---noise-email-advise-transfer), Fine-tuning, Domain Adaptation

### TSA - Temporal Self-Attention
**Full Name**: Temporal Self-Attention
**Description**: Transformer-style self-attention for time series - captures **long-range temporal dependencies** in abuse patterns. Upcoming **Cursus** pipeline (Completed 2026/01). vs LSTM: parallel processing, no vanishing gradients. vs RCF: preserves temporal structure. Use cases: DNR patterns, return abuse sequences, MAA temporal coordination.
**Documentation**: [TSA Term](../resources/term_dictionary/term_tsa.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/CursusAutomaticSageMakerPipelineCompiler/
**Framework**: Cursus (BAP ML pipeline compiler)
**Status**: 📅 In Development - ETA Q2 2026 for Cursus pipeline support
**Cursus Pipeline Steps**: Temporal Transformation → TSA Training → Inference
**Architecture**: Multi-head self-attention with temporal embedding (positional encoding)
**Advantage vs RCF**: Preserves temporal structure (RCF drops it)
**Advantage vs LSTM**: Parallel processing, better long-range dependency capture
**Use Cases**: DNR pattern detection, return abuse sequences, concession rate anomalies, MAA temporal coordination, account activity monitoring
**Team**: BAP ML Team (Cursus development)
**Related**: [Transformer](#transformer), [LSTM](#lstm---long-short-term-memory), [Cursus](../resources/term_dictionary/term_cursus.md), [MODS](../resources/term_dictionary/term_mods.md)

---

## Investigation Automation Systems

### DeepCARE - Deep Representation Learning for Continuously Adaptive Risk Evaluation
**Full Name**: Deep Representation Learning for Continuously Adaptive Risk Evaluation
**Description**: **Primary ML automation system for BAP** - resolves predictable cases via k-NN similarity search (k=440, 8-week lookback). Key innovation: **continuous adaptive learning** without retraining. Performance: 493K investigations automated, 90%+ precision, 6+ intents. Metrics: precision (5% control), LPA (loss per action).
**Documentation**: [DeepCARE Term](../resources/term_dictionary/term_deepcare.md)
**Wiki**: [DeepCARE Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/DeepCARE/), [Quicksight Dashboard](https://us-east-1.quicksight.aws.amazon.com/sn/accounts/764946308314/dashboards/ecc0cfa5-20e3-4a53-8e8f-509c77691cbb?directory_alias=amazonbi#)
**Architecture**: FAP Events → Variable Enrichment → Order2Vector (DNN) → N-dim Vector → ElasticSearch k-NN (EMR Spark) → Consensus Decision → FORTRESS Rules → Action
**Key Metrics**: 
  - Automation Rate: % of queued tasks automated (goal: maximize)
  - Model Precision: Agreement with manual investigators via 5% control group (goal: ≥90%)
  - Loss Per Action: Concession value per action (goal: lower than manual)
**Performance**: 493K investigations automated (Nov 2022 - Jan 2023), 90%+ precision maintained across workflows
**Supported Workflows**: PFW, CAP Referral, BRW, AFN RI, MFN RI, AtoZ (6+ intents)
**Coverage**: All major marketplaces (NA, EU, FE) - US/CA/MX/BR, UK/DE/FR/IT/ES/BE/NL/PL/SE/TR/AE/EG/SA, JP/AU/SG
**Evolution**: AutoEncoder DeepCARE → eSNN DeepCARE (2022, $10MM fraud reduction) → eSNN + FSL++ (2023+)
**Launch Timeline**: 2019 (TRMS/IOS concept) → 2022-11 (eSNN US) → 2023-01 (BAP PFW) → 2023-12 (6 intents) → 2024-12 (Bad Actor Accounts)
**Status**: ✅ Active - core automation system for BAP
**Related**: [ARI](../resources/term_dictionary/term_ari.md), [k-NN](#k-nn---k-nearest-neighbors), [URES](../resources/term_dictionary/term_ures.md), [eSNN](#esnn---extended-siamese-neural-network), [CAP](../resources/term_dictionary/term_cap.md), [AutoSignality](#autosignality), [GreenTEA](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### NEAT - Noise Email Advise Transfer
**Full Name**: Noise Email Advise Transfer
**Description**: ML pipeline managing ARI email queues - removes spam/BOT, routes to appropriate queue. Models: BERT spam classifier (99% precision, 86% recall), Transfer model (98% precision). GoldMiner integration: automation 22%→32%, defects 10%→5%. Coverage: 20+ marketplaces.
**Documentation**: [NEAT Term](../resources/term_dictionary/term_neat.md)
**Wiki**: [NEAT Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/NEAT/), [NEAT Science](https://w.amazon.com/bin/view/BuyerAbuseDataScience/Science/NEAT/)
**Architecture**: Email → CSC → MDS (cscemailcontacts) → NEAT GMRA Workflow → AMES (NLP models) → RMP (rules) → URES (action execution)
**ML Models**:
  - **Spam Classifier**: BERT-based, 99% precision, 86% recall
  - **Transfer Model**: BERT multilingual 3-class (ARI/CS/BRI), 98% precision
  - **BOT Detection**: DeepCARE-based ElasticSearch k-NN similarity
**Four Email Groups**: (1) Cleaning - auto-resolve spam/BOT/last-worded, (2) Management - route to appropriate queue, (3) Feedback - flag for special handling, (4) Recommendation - advise on evidence
**Key Metrics**:
  - Automation Rate: ~35% WW (June 2023)
  - Defect Rate: 5% (post-GoldMiner integration)
  - Investigator Capacity: 6+ FTEs freed from manual filtering
**GoldMiner Integration**: June 2023 integration increased automation 22%→32%, reduced defects 10%→5%
**Coverage**: 20+ marketplaces (US, CA, MX, BR, EU5+, MENA, IN, AU, JP, SG)
**Launch**: Q1 2021 (US), expanded 2021-2023 globally
**Dashboard**: [NEAT Performance](https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/e8d075e0-c11b-48e3-86d2-6b08eca55bd6)
**Contact**: buyer-abuse-neat@amazon.com
**CTI**: TRMS / Abuse RnD / NEAT
**Related**: [DeepCARE](#deepcare---deep-representation-learning-for-continuously-adaptive-risk-evaluation), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [ARI](../resources/term_dictionary/term_ari.md), [GoldMiner](#goldminer---annotation-processor), [AMES](../resources/term_dictionary/term_ames.md), [URES](../resources/term_dictionary/term_ures.md)

### GoldMiner - Annotation Processor
**Full Name**: GoldMiner Annotation Processor for Buyer Abuse Prevention
**Description**: NLP system extracting insights from investigator annotations (10M+/year) into reason codes, blurbs, categories. Technology: Sentence-BERT + K-means clustering. Outputs: `appeal_deny`, `dnr_warning_writeback`. NEAT integration: automation 22%→32%. GreenTEA: +9% AUC via topic modeling.
**Documentation**: [GoldMiner Term](../resources/term_dictionary/term_goldminer.md)
**Wiki**: [GoldMiner Wiki](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/GoldMiner/)
**Architecture**: Cradle Jobs (EDX→S3) → AWS Lambda → Step Function (NLP models) → Output Cradle (S3→EDX) → OTF Variables/Redshift
**Technology**: 
  - **Sentence-BERT** - Vector representations for topic modeling
  - **K-means clustering** - Group annotations by topic
  - **NLP classification** - Reason code prediction
**Outputs**:
  - **Reason Codes**: `appeal_deny`, `dnr_abuse_confirmed`
  - **Blurbs**: `dnr_warning_writeback`, `mdr_appeal_denied`
  - **Investigation Categories**: `ARI`, `ARM`, `MAA`
**Key Metrics**:
  - Email Automation: 22%→32% (NEAT integration, June 2023)
  - Defect Reduction: 10%→5%
  - Coverage: 20 stores (US, EU5, MENA, FE)
**Use Cases**:
  - NEAT email automation (last-worded detection, customer history tracking)
  - GreenTEA prompt optimization (+9% AUC via topic modeling)
  - Queue diagnosis dashboards
  - Model feedback loop (decision gap identification)
**OTF Variables**: `Abuse.DataSheet.abuse_edx_goldminer_by_cid_with_email` (NA/EU/FE)
**Dashboard**: [Queue Diagnosis](https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/e8d075e0-c11b-48e3-86d2-6b08eca55bd6)
**Owner**: Buyer-Abuse-RnD (LDAP)
**Code**: [BAPML-GoldMinerAnnotationDev](https://code.amazon.com/packages/BAPML-GoldMinerAnnotationDev)
**Publication**: [AMLC 2022 Paper](https://amlc.corp.amazon.com/paper/07b63190-dc83-11ec-9aa8-b96a67d7bb89/content)
**Status**: ✅ Active - core annotation processing for BAP automation
**Related**: [NEAT](#neat---noise-email-advise-transfer), [GreenTEA](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [ARI](../resources/term_dictionary/term_ari.md), [OTF](../resources/term_dictionary/term_otf.md)

---

## Optimization

### Gradient Descent - First-Order Optimization Algorithm
**Full Name**: Gradient Descent
**Description**: Fundamental iterative optimization algorithm that finds minimum of differentiable functions by moving in direction of steepest descent using gradient information. Core optimization engine powering virtually all machine learning model training at Amazon, from XGBoost gradient boosting to neural network backpropagation in BERT and transformer architectures. Essential competency for Applied Scientists, serving as the foundation algorithm underlying automated systems like GreenTEA's prompt optimization and optimization components within ARROW Everywhere's rule calibration workflows. Provides theoretical and computational foundation for advanced optimization systems with reliable convergence properties on convex problems.
**Documentation**: [Gradient Descent Term](../resources/term_dictionary/term_gradient_descent.md)
**Wiki**: https://w.amazon.com/bin/view/AppliedScientist/Competencies/
**Related**: [SGD](#sgd---stochastic-gradient-descent), [Convex Programming](#convex-programming---convex-optimization), [XGBoost](#xgboost), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [GreenTEA](#greentea---gradient-descent-with-topic-modeling-and-evolutionary-auto-prompting)

### SGD - Stochastic Gradient Descent
**Full Name**: Stochastic Gradient Descent
**Description**: Computationally efficient variant of gradient descent that uses randomly selected mini-batches of training data to compute gradient estimates, enabling efficient training on large-scale datasets. Primary training algorithm for large-scale models where computational constraints require efficient optimization approaches, with stochastic noise helping escape local minima while dramatically reducing computational cost per iteration. Essential for training complex models like transformers, neural networks, and deep learning architectures used in buyer abuse prevention including BERT-based NLP models and GraphSAGE neighborhood sampling. Core competency for Applied Scientists, serving as foundation for advanced optimizers like Adam and RMSprop used throughout Amazon's ML training infrastructure.
**Documentation**: [SGD Term](../resources/term_dictionary/term_sgd.md)
**Wiki**: https://w.amazon.com/bin/view/AppliedScientist/Competencies/
**Related**: [Gradient Descent](#gradient-descent---first-order-optimization-algorithm), [ADAM](#adam---adaptive-moment-estimation), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [GNN](#gnn---graph-neural-networks), [Neural Networks](../resources/term_dictionary/term_neural_networks.md)

### ADAM - Adaptive Moment Estimation
**Full Name**: ADAM (Adaptive Moment Estimation)
**Description**: Most widely adopted optimization algorithm in modern deep learning, combining adaptive per-parameter learning rates with momentum-based acceleration and bias correction to achieve robust training across diverse model architectures. Default optimizer for training sophisticated models including transformer-based architectures like BERT for NLP-based abuse detection and deep neural networks for complex pattern recognition. Eliminates need for manual learning rate tuning while providing stable convergence properties, making it essential for training state-of-the-art models used in buyer abuse prevention systems. Core competency for Applied Scientists, serving as the standard optimization choice throughout Amazon's ML training infrastructure for complex model development.
**Documentation**: [ADAM Term](../resources/term_dictionary/term_adam.md)
**Wiki**: https://w.amazon.com/bin/view/AppliedScientist/Competencies/
**Related**: [SGD](#sgd---stochastic-gradient-descent), [Gradient Descent](#gradient-descent---first-order-optimization-algorithm), [BP](#bp---back-propagation), [BERT](#bert---bidirectional-encoder-representations-from-transformers), [Transformer](#transformer)

### BP - Back-Propagation
**Full Name**: Back-Propagation (Backpropagation)
**Description**: Fundamental algorithm for training neural networks that computes gradients of loss function with respect to network parameters by applying chain rule of calculus in reverse through network layers. Most significant algorithmic breakthrough in deep learning, enabling efficient training of multi-layer networks by automatically computing gradients through automatic differentiation. Core training mechanism for deep learning models including transformer architectures like BERT for NLP-based abuse detection and neural networks for complex pattern recognition. Essential foundation algorithm that enabled the deep learning revolution and modern AI capabilities at Amazon, underlying virtually all neural network training procedures.
**Documentation**: [BP Term](../resources/term_dictionary/term_backpropagation.md)
**Wiki**: https://w.amazon.com/bin/view/DeepLearning/Backpropagation/
**Related**: [Gradient Descent](#gradient-descent---first-order-optimization-algorithm), [SGD](#sgd---stochastic-gradient-descent), [ADAM](#adam---adaptive-moment-estimation), [Neural Networks](../resources/term_dictionary/term_neural_networks.md), [BERT](#bert---bidirectional-encoder-representations-from-transformers)

### Linear Programming - Linear Optimization
**Full Name**: Linear Programming (LP)
**Description**: Foundational mathematical optimization technique for problems with linear objective functions and linear constraints, where all decision variables are continuous. Serves as the basis for more advanced optimization techniques like MILP and forms crucial component of optimization systems used in Amazon's automated rule calibration workflows. Enables efficient solution methods with guaranteed global optimality through established algorithms like simplex method, providing theoretical and computational foundation for advanced optimization systems in buyer abuse prevention and fraud detection.
**Documentation**: [Linear Programming Term](../resources/term_dictionary/term_linear_programming.md)
**Wiki**: https://w.amazon.com/bin/view/OperationsResearch/
**Related**: [Convex Programming](#convex-programming---convex-optimization), [MILP](#milp---mixed-integer-linear-programming), [Operations Research](../resources/term_dictionary/term_operations_research.md), [Simplex Method](../resources/term_dictionary/term_simplex_method.md), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md)

### Convex Programming - Convex Optimization

### Coordinate Descent
**Full Name**: Coordinate Descent (Block Coordinate Descent)
**Description**: Optimizes one variable at a time while holding others fixed. **Standard solver for LASSO and Elastic Net (glmnet)** — each coordinate update has closed-form via soft-thresholding. Block CD solves GraphLasso. Warm-start along regularization path. Simple, parallelizable, converges for convex problems.
**Documentation**: [Coordinate Descent Term](../resources/term_dictionary/term_coordinate_descent.md)
**Related**: [LASSO](acronym_glossary_statistics.md#lasso), [GraphLasso](acronym_glossary_statistics.md#graphlasso), [ADMM](#admm---alternating-direction-method-of-multipliers)

### ADMM - Alternating Direction Method of Multipliers
**Full Name**: ADMM (Boyd et al., 2011)
**Description**: Solves $\min f(x) + g(z)$ s.t. $Ax + Bz = c$ by alternating x-update, z-update, and dual update. **Handles non-smooth terms (L1 via proximal operator), naturally distributed/parallel.** $O(1/k)$ convergence. Used for distributed LASSO, consensus optimization, and large-scale GraphLasso.
**Documentation**: [ADMM Term](../resources/term_dictionary/term_admm.md)
**Related**: [Coordinate Descent](#coordinate-descent), [LASSO](acronym_glossary_statistics.md#lasso), [Convex Programming](#convex-programming---convex-optimization)

### Convex Programming - Convex Optimization
**Full Name**: Convex Programming (Convex Optimization)
**Description**: Subclass of mathematical optimization problems where the objective function is convex and feasible region is convex set, guaranteeing global optimality of any local optimum. Provides mathematical foundation for gradient-based learning algorithms, model training procedures, and optimization components within automated rule calibration systems at Amazon. Essential competency for Applied Scientists, enabling efficient and reliable optimization procedures with convergence guarantees. Foundation for gradient descent and specialized solvers used in ML model training, risk evaluation, and fraud detection systems.
**Documentation**: [Convex Programming Term](../resources/term_dictionary/term_convex_programming.md)
**Wiki**: https://w.amazon.com/bin/view/OperationsResearch/
**Related**: [Linear Programming](#linear-programming---linear-optimization), [MILP](#milp---mixed-integer-linear-programming), [XGBoost](#xgboost), [Gradient Descent](../resources/term_dictionary/term_gradient_descent.md), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md)

### MILP - Mixed Integer Linear Programming
**Full Name**: Mixed Integer Linear Programming
**Description**: Mathematical optimization technique extending linear programming to handle problems with integer decision variables while maintaining linear objective functions and constraints. Critical foundation for ARROW Everywhere's Gurobi Optimizer Integration, enabling formulation of rule calibration as global optimization problems for automated threshold optimization. Provides provably optimal solutions for multi-threshold rules through simultaneous optimization considering interdependencies and constraints that exhaustive search methods cannot handle efficiently. Essential mathematical framework enabling Amazon's shift toward rigorous automated rule optimization approaches.
**Documentation**: [MILP Term](../resources/term_dictionary/term_milp.md)
**Wiki**: https://w.amazon.com/bin/view/URES/ARROWEverywhere/
**Related**: [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md), [Gurobi](../resources/term_dictionary/term_gurobi.md), [RMP](../resources/term_dictionary/term_rmp.md), [UDV](../resources/term_dictionary/term_udv.md), [Convex Programming](#convex-programming---convex-optimization)

### Gurobi - Commercial Optimization Solver
**Full Name**: Gurobi Optimization Solver
**Description**: State-of-the-art commercial mathematical optimization solver for LP, MILP, and QP problems, used as the solver backend for rule optimization in BAP. **Consistently ranks among the fastest solvers** in independent benchmarks. Implements simplex, barrier, and branch-and-bound algorithms with Python API (`gurobipy`) for model building. Used in ARC project for automated ruleset creation and threshold calibration.
**Documentation**: [Gurobi Term](../resources/term_dictionary/term_gurobi.md)
**Related**: [MILP](#milp---mixed-integer-linear-programming), [Linear Programming](#linear-programming---linear-optimization), [Rule Optimization](../resources/term_dictionary/term_rule_optimization.md), [Simplex Method](../resources/term_dictionary/term_simplex_method.md)

### Operations Research - Applied Optimization Science
**Full Name**: Operations Research
**Description**: Interdisciplinary field applying mathematical modeling, statistical analysis, and optimization techniques to complex decision-making problems. Encompasses linear programming, integer programming, combinatorial optimization, and queuing theory. **Provides the mathematical foundations** for rule optimization, enforcement strategy design, and resource allocation in abuse prevention. Complements ML by optimizing decisions on top of ML predictions.
**Documentation**: [Operations Research Term](../resources/term_dictionary/term_operations_research.md)
**Related**: [Linear Programming](#linear-programming---linear-optimization), [MILP](#milp---mixed-integer-linear-programming), [Gurobi](#gurobi---commercial-optimization-solver), [Simplex Method](../resources/term_dictionary/term_simplex_method.md)

### Simplex Method - Linear Programming Algorithm
**Full Name**: Simplex Method
**Description**: Classic algorithm for solving linear programming problems by traversing vertices of the feasible polytope, moving to adjacent vertices with better objective values until optimality is reached. Developed by Dantzig (1947), it remains one of the most widely used LP algorithms despite exponential worst-case complexity. **Highly efficient in practice** and serves as a core subroutine within solvers like Gurobi for LP relaxations in branch-and-bound MILP solving.
**Documentation**: [Simplex Method Term](../resources/term_dictionary/term_simplex_method.md)
**Related**: [Linear Programming](#linear-programming---linear-optimization), [MILP](#milp---mixed-integer-linear-programming), [Gurobi](#gurobi---commercial-optimization-solver), [Operations Research](../resources/term_dictionary/term_operations_research.md)

### Rule Optimization - Automated Rule Calibration
**Full Name**: Rule Optimization
**Description**: Process of automatically calibrating thresholds, conditions, and parameters of abuse detection rules in RMP to maximize detection while minimizing false positives. Formulates rule calibration as MILP optimization problems solved by Gurobi. **Replaces manual rule tuning** with algorithmic optimization subject to business constraints (false positive limits, coverage targets). Featured in BRP science reviews as a key research area, with recent exploration of LLM-assisted approaches.
**Documentation**: [Rule Optimization Term](../resources/term_dictionary/term_rule_optimization.md)
**Related**: [MILP](#milp---mixed-integer-linear-programming), [Gurobi](#gurobi---commercial-optimization-solver), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md), [ML Automation](#ml-automation)

---

## Reinforcement Learning

### RL - Reinforcement Learning
**Full Name**: Reinforcement Learning
**Description**: Agent learns optimal decisions via rewards - **auto-adapts to adversarial patterns** without manual tuning. Amazon: ROOT (hourly rule optimization, SAC), Action Orchestration (cross-touchpoint). Offline RL preferred for safety. vs XGBoost: RL for decision optimization (rules), XGBoost for risk scoring (features).
**Documentation**: [RL Term](../resources/term_dictionary/term_rl.md) ✅
**Wiki**: [SPS RL Working Group](https://w.amazon.com/bin/view/SPS_RL_Working_Group/), [BRP ML RL Group](https://w.amazon.com/bin/view/BRP_ML_Reinforcement_Learning_Working_Group/)
**Working Group Email**: trms-rl-wg@amazon.com
**Core Components**: Agent, Environment, State, Action, Reward, Policy, Return
**Amazon Projects**: ROOT (rule optimization), RELSER (neural ruleset), Action Orchestration, LBP (transfer learning), Non-Stationary RL
**Algorithms**: SAC (Soft Actor-Critic), CQL (Conservative Q-Learning), CMAB (Contextual Multi-Armed Bandit)
**Online vs Offline**: Offline preferred for safety (no live exploration)
**Use Cases**: Rule threshold optimization (ROOT), action orchestration across touchpoints, MFA challenge selection
**Key Advantage**: Automatic adaptation to adversarial fraud patterns without manual tuning
**Limitation**: Reward design challenging (delayed feedback), offline RL preferred for safety
**Status**: ✅ Active - emerging technology for fraud/abuse optimization
**Related**: [MAB](#mab---multi-armed-bandits), [Active Learning](#active-learning), [Transfer Learning](#transfer-learning), Policy Learning

### Offline RL - Offline Reinforcement Learning
**Full Name**: Offline Reinforcement Learning (Batch RL)
**Description**: Learns policies entirely from fixed historical data without environment interaction — critical for safety-sensitive domains where exploration is dangerous. **Addresses the key constraint that we cannot experiment on real customers.** Used in ROOT (action orchestration), Dupin (pre-training adversarial policies), and Action Orchestration (optimal friction sequences from logged interactions).
**Documentation**: [Offline RL Term](../resources/term_dictionary/term_offline_rl)
**Related**: [RL](#rl---reinforcement-learning), [ROOT](../resources/term_dictionary/term_root.md), [Dupin](../resources/term_dictionary/term_dupin.md)

### MORL - Multi-Objective Reinforcement Learning
**Full Name**: Multi-Objective Reinforcement Learning
**Description**: Extends RL to simultaneously optimize multiple conflicting objectives (vector rewards) — finding Pareto-optimal policies where no objective improves without degrading another. **Directly relevant to BAP's core tradeoff: fraud detection rate vs. false positive rate (CX impact).** Approaches include scalarization, envelope methods, constraint-based, and preference-conditioned policies.
**Documentation**: [MORL Term](../resources/term_dictionary/term_morl)
**Related**: [RL](#rl---reinforcement-learning), [Offline RL](#offline-rl---offline-reinforcement-learning), [DSI](../resources/term_dictionary/term_dsi.md)

### Reward - Reward Design
**Full Name**: Reward Function Design (Reward Engineering, Reward Shaping)
**Description**: The scalar signal defining what an RL agent should optimize — widely considered the hardest part of applying RL to real problems. **Reward misspecification leads to reward hacking where agents find unintended shortcuts.** In BAP: Dupin reward (maximize concessions while minimizing detection), ROOT reward (multi-objective fraud/CX/cost), SAFE reward (detection with FP penalty).
**Documentation**: [Reward Term](../resources/term_dictionary/term_reward)
**Related**: [RL](#rl---reinforcement-learning), [Reward Hacking](../resources/term_dictionary/term_reward_hacking.md), [MORL](#morl---multi-objective-reinforcement-learning)

### MDP - Markov Decision Process
**Full Name**: Markov Decision Process
**Description**: Mathematical framework for modeling **sequential decision-making under uncertainty**, defined as a 5-tuple (S, A, T, R, γ) of states, actions, transition probabilities, rewards, and discount factor. The **Bellman equation** provides the recursive characterization of optimal value, solvable via value iteration, policy iteration, or model-free methods like Q-learning. MDPs assume full state observability (the Markov property) and provide the formal foundation for all reinforcement learning — every RL algorithm implicitly or explicitly operates on an MDP formulation. Generalized by POMDPs (partial observability) and Dec-POMDPs (multi-agent).
**Documentation**: [MDP Term](../resources/term_dictionary/term_mdp.md)
**Related**: [RL](#rl---reinforcement-learning), [POMDP](#pomdp---partially-observable-markov-decision-process), [MAB](#mab---multi-armed-bandits)

### MAB - Multi-Armed Bandits
**Full Name**: Multi-Armed Bandit (K-Armed Bandit)
**Description**: Foundational RL framework for **sequential decision-making under uncertainty** where an agent repeatedly selects from a fixed set of actions ("arms") and receives stochastic rewards, learning to balance **exploration** (trying less-known actions) with **exploitation** (using best-known action). Simplest RL formulation — no state transitions, no context features (unlike CMAB) — making it safer and more interpretable for production fraud systems. Core algorithms include **Thompson Sampling** (Bayesian, powers GoldMiner Optimizer yield 13%→22%), **UCB** (optimistic, provable bounds), **ε-Greedy** (simple baseline), and **Exp3** (adversarial, tested for ALBL query strategy). Extended by CMAB (adds context features) for Hyperloop CAPTCHA selection and CABLE active learning; foundation for full RL (ROOT, Action Orchestration).
**Documentation**: [MAB Term](../resources/term_dictionary/term_mab.md)
**Wiki**: [SPS RL Working Group](https://w.amazon.com/bin/view/SPS_RL_Working_Group/), [BRP ML RL Working Group](https://w.amazon.com/bin/view/BRP_ML_Reinforcement_Learning_Working_Group/)
**Core Algorithms**: Thompson Sampling, UCB, ε-Greedy, Exp3, Softmax
**Variants**: Standard (stochastic), Contextual (CMAB), Adversarial, Non-Stationary, Combinatorial
**BRP Applications**: GoldMiner Optimizer (Thompson Sampling, budget allocation), A/B testing (adaptive allocation), ALBL (Exp3 query strategy), Weblab integration
**Key Concept**: Exploration-exploitation trade-off — pure exploitation misses better options, pure exploration wastes on bad arms
**⚠️ Disambiguation**: Not MAA (Multi-Account Abuse)
**Status**: ✅ Active - foundational RL framework for BRP adaptive decision-making
**Related**: [RL](#rl---reinforcement-learning), [CMAB](#cmab---contextual-multi-armed-bandit), [Hyperloop](../resources/term_dictionary/term_hyperloop.md), [GoldMiner](#goldminer---annotation-processor), [Active Learning](#active-learning)

### CMAB - Contextual Multi-Armed Bandit
**Full Name**: Contextual Multi-Armed Bandit (Contextual Bandit)
**Description**: RL framework where an agent selects **actions based on contextual features** and receives immediate rewards, balancing **exploration** (trying new strategies) with **exploitation** (using known best), with each decision **independent** (no state transitions) making it safer than full RL for production fraud systems. Three major BRP deployments: **Hyperloop Challenge Recommender** (CMAB selects optimal CAPTCHA for BAA detection, part of $11MM+ savings), **CABLE** (contextual bandit for dynamic active learning query strategy, 8-14% labeling cost reduction), and **GoldMiner Optimizer** (Thompson Sampling for ARI investigation budget allocation, yield improved 13%→22%). Common algorithms include Thompson Sampling, ε-Greedy, UCB, Exp3, and LinUCB, with offline evaluation via CoCo counterfactual bandit framework applied to GCAP.
**Documentation**: [Contextual Bandit Term](../resources/term_dictionary/term_contextual_bandit.md)
**Wiki**: [SPS RL Working Group](https://w.amazon.com/bin/view/SPS_RL_Working_Group/), [BRP ML RL Working Group](https://w.amazon.com/bin/view/BRP_ML_Reinforcement_Learning_Working_Group/)
**Key Distinction**: Context-aware (uses features) + single-step (no state transitions) = safer than full RL
**BRP Applications**: Hyperloop Challenge Recommender (CAPTCHA selection), CABLE (query strategy), GoldMiner Optimizer (budget allocation), PRIDE (personalized risk), CoCo (counterfactual evaluation)
**Algorithms**: Thompson Sampling, ε-Greedy, UCB, Exp3, LinUCB
**Exploration-Exploitation**: Balance trying new actions (exploration) with using best known (exploitation) guided by context
**⚠️ Disambiguation**: Not CB (Chargeback) or MAB (simpler, no context features)
**Status**: ✅ Active - key RL technique for adaptive decision-making in BRP
**Related**: [RL](#rl---reinforcement-learning), [MAB](#mab---multi-armed-bandits), [Hyperloop](../resources/term_dictionary/term_hyperloop.md), [Active Learning](#active-learning), [GoldMiner](#goldminer---annotation-processor), [CAPTCHA](../resources/term_dictionary/term_captcha.md)

### UCB - Upper Confidence Bound
**Full Name**: Upper Confidence Bound (UCB1, LinUCB, SW-UCB)
**Description**: Family of bandit algorithms resolving exploration-exploitation through **"optimism in the face of uncertainty"** — selecting the action with the highest upper confidence bound on estimated reward, naturally exploring under-sampled actions (wide confidence intervals) while exploiting high-reward actions (tight estimates). Provides **provable regret bounds** O(√T log T) and **deterministic** decisions (unlike Thompson Sampling's stochastic approach), making it interpretable and reproducible for compliance-sensitive fraud systems. Key variants include **LinUCB** (contextual extension used in PRIDE personalized Amazon Pay risk detection) and **SW-UCB/Discounted UCB** for non-stationary fraud pattern adaptation. Formula: `UCB(a) = Q̂(a) + c × √(ln(t) / N(a))` where confidence bonus shrinks as action is sampled more, automatically balancing exploration.
**Documentation**: [UCB Term](../resources/term_dictionary/term_ucb.md)
**Wiki**: [SPS RL Working Group](https://w.amazon.com/bin/view/SPS_RL_Working_Group/)
**Formula**: UCB(a) = Q̂(a) + c × √(ln(t) / N(a))
**Principle**: "Optimism in the face of uncertainty" — explore uncertain arms, exploit known good ones
**Variants**: UCB1 (classic), LinUCB (contextual), Discounted UCB, SW-UCB (sliding window), KL-UCB
**Properties**: Deterministic, provable regret bounds, automatic exploration decay, high interpretability
**BRP Applications**: Rule selection, PRIDE (LinUCB for Amazon Pay), Hyperloop (UCB foundation), non-stationary fraud adaptation (SW-UCB)
**vs Thompson Sampling**: UCB = deterministic + provable bounds; TS = stochastic + better empirical performance
**Status**: ✅ Active - core bandit algorithm in MAB/CMAB family
**Related**: [MAB](#mab---multi-armed-bandits), [CMAB](#cmab---contextual-multi-armed-bandit), [RL](#rl---reinforcement-learning), [Hyperloop](../resources/term_dictionary/term_hyperloop.md), [ARROW](../resources/term_dictionary/term_arrow.md)

### POMDP - Partially Observable Markov Decision Process
**Full Name**: Partially Observable Markov Decision Process
**Description**: Generalization of the MDP to settings where the agent **cannot directly observe the underlying state**, instead receiving noisy observations and maintaining a probability distribution (belief state) over possible states. Defined as a 7-tuple (S, A, T, R, Ω, O, γ) adding observations and an observation function to the MDP formulation. **Belief states are sufficient statistics** for the entire action-observation history, enabling conversion to a continuous-state belief MDP. Unlike MDPs, POMDPs can assign value to information-gathering actions that reduce uncertainty. Finite-horizon POMDP planning is PSPACE-complete; key solvers include SARSOP (offline) and POMCP (online Monte Carlo tree search).
**Documentation**: [POMDP Term](../resources/term_dictionary/term_pomdp.md)
**Related**: [MDP](#mdp---markov-decision-process), [RL](#rl---reinforcement-learning), [MAB](#mab---multi-armed-bandits)

### Q-Learning
**Full Name**: Q-Learning (Quality Learning)
**Description**: Model-free, off-policy reinforcement learning algorithm that learns the optimal action-value function $Q^*(s, a)$ directly from experience using temporal difference updates. **The $\max$ operator over next-state actions makes it off-policy** — it learns the value of the optimal greedy policy regardless of the behavior policy used for exploration. Invented by Watkins (1989); convergence proved by Watkins & Dayan (1992). Extended to high-dimensional inputs via Deep Q-Networks (DQN, Mnih et al. 2015), which achieved human-level Atari performance and launched modern deep RL. Key variants include Double Q-learning (addresses maximization bias), Dueling DQN, and Rainbow (combines six improvements).
**Documentation**: [Q-Learning Term](../resources/term_dictionary/term_q_learning.md)
**Related**: [RL](#rl---reinforcement-learning), [SARSA](#sarsa---state-action-reward-state-action), [MDP](#mdp---markov-decision-process)

### SARSA - State-Action-Reward-State-Action
**Full Name**: State-Action-Reward-State-Action
**Description**: On-policy temporal difference (TD) control algorithm that learns action-value functions by updating Q-values based on the action the agent **actually takes** under its current policy, not the greedy action. **The on-policy nature makes SARSA more conservative and safer than Q-learning** — in the classic Cliff Walking problem, SARSA learns a path away from the cliff edge while Q-learning walks along it. Named by Sutton after the quintuple $(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})$; originally invented by Rummery & Niranjan (1994) as "Modified Connectionist Q-Learning." Key variants include Expected SARSA (lower variance; reduces to Q-learning under greedy policy) and SARSA($\lambda$) (eligibility traces for efficient credit assignment).
**Documentation**: [SARSA Term](../resources/term_dictionary/term_sarsa.md)
**Related**: [RL](#rl---reinforcement-learning), [Q-Learning](#q-learning), [MDP](#mdp---markov-decision-process)

### DQN - Deep Q-Network
**Full Name**: Deep Q-Network
**Description**: Value-based deep reinforcement learning algorithm that extends tabular Q-learning to high-dimensional state spaces by replacing the Q-table with a deep convolutional neural network. **Two key innovations stabilize training**: experience replay (random minibatch sampling from a buffer of stored transitions to break temporal correlations) and a target network (separate, periodically updated copy for stable TD targets). Achieved human-level performance on 49 Atari games from raw pixels (Mnih et al., Nature 2015) — the landmark result that launched modern deep RL. Key variants include Double DQN (reduces overestimation bias), Dueling DQN (value-advantage decomposition), and Rainbow (combines six improvements).
**Documentation**: [DQN Term](../resources/term_dictionary/term_dqn.md)
**Related**: [Q-Learning](#q-learning), [RL](#rl---reinforcement-learning), [Actor-Critic](#actor-critic), [MDP](#mdp---markov-decision-process)

### Actor-Critic
**Full Name**: Actor-Critic
**Description**: Family of reinforcement learning algorithms combining a policy network (actor) that selects actions with a value network (critic) that evaluates those actions via temporal-difference learning. **The advantage function reduces variance** compared to pure policy gradient methods while maintaining unbiased gradient estimates. Handles both discrete and continuous action spaces, making it the dominant paradigm for modern deep RL. Key variants include PPO (clipped surrogate objective — de facto standard for RLHF in LLM alignment), SAC (maximum entropy framework for sample-efficient off-policy learning), DDPG/TD3 (deterministic policies for continuous control), and A3C (asynchronous parallel training).
**Documentation**: [Actor-Critic Term](../resources/term_dictionary/term_actor_critic.md)
**Related**: [RL](#rl---reinforcement-learning), [Q-Learning](#q-learning), [DQN](#dqn---deep-q-network), [RLHF](../resources/term_dictionary/term_rlhf.md)

### TD - Temporal Difference Learning
**Full Name**: Temporal Difference Learning
**Description**: Class of model-free reinforcement learning methods that learn value functions by combining ideas from Monte Carlo methods and dynamic programming. **TD methods bootstrap — updating estimates based partly on other estimates without waiting for a final outcome.** The TD error $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ is the foundational learning signal for Q-learning, SARSA, and actor-critic methods. TD(0) uses one-step bootstrapping, while TD($\lambda$) with eligibility traces interpolates between TD(0) and Monte Carlo. The dopamine-TD connection (Schultz et al., 1997) showed that midbrain dopamine neurons encode TD error.
**Documentation**: [TD Learning Term](../resources/term_dictionary/term_td_learning.md)
**Related**: [Q-Learning](#q-learning), [SARSA](#sarsa---state-action-reward-state-action), [Actor-Critic](#actor-critic), [RL](#rl---reinforcement-learning)

### PPO - Proximal Policy Optimization
**Full Name**: Proximal Policy Optimization
**Description**: On-policy actor-critic reinforcement learning algorithm that uses a clipped surrogate objective to constrain policy updates, preventing destructively large steps. **The clipped probability ratio provides implicit trust-region behavior with only first-order optimization**, making PPO simpler than its predecessor TRPO while achieving equal or better performance. The de facto standard algorithm for RLHF in LLM alignment (InstructGPT, ChatGPT, Claude). Also scaled to defeat Dota 2 world champions (OpenAI Five, 2019). Supports both discrete and continuous action spaces.
**Documentation**: [PPO Term](../resources/term_dictionary/term_ppo.md)
**Related**: [Actor-Critic](#actor-critic), [RLHF](../resources/term_dictionary/term_rlhf.md), [A2C](#a2c---advantage-actor-critic), [RL](#rl---reinforcement-learning)

### SAC - Soft Actor-Critic
**Full Name**: Soft Actor-Critic
**Description**: Off-policy actor-critic deep reinforcement learning algorithm based on the maximum entropy framework, maximizing both expected reward and policy entropy. **Automatic temperature tuning via dual gradient descent eliminates a critical hyperparameter**, and twin Q-networks reduce overestimation bias. Uses a squashed Gaussian stochastic policy for built-in exploration without external noise. Among the most sample-efficient model-free algorithms for continuous control, demonstrated on real-world robots at UC Berkeley BAIR. Designed for continuous action spaces only.
**Documentation**: [SAC Term](../resources/term_dictionary/term_sac.md)
**Related**: [Actor-Critic](#actor-critic), [PPO](#ppo---proximal-policy-optimization), [TD](#td---temporal-difference-learning), [RL](#rl---reinforcement-learning)

### A2C - Advantage Actor-Critic
**Full Name**: Advantage Actor-Critic
**Description**: Synchronous, on-policy actor-critic reinforcement learning algorithm where multiple parallel environment instances collect experience simultaneously, then a single synchronized gradient update is performed on a shared network. **A2C is the synchronous variant of A3C, matching its performance with simpler implementation and better GPU utilization** (OpenAI, 2017). Uses the advantage function as a variance-reducing baseline for the policy gradient. Largely superseded by PPO's clipped surrogate objective for more stable training.
**Documentation**: [A2C Term](../resources/term_dictionary/term_a2c.md)
**Related**: [A3C](#a3c---asynchronous-advantage-actor-critic), [PPO](#ppo---proximal-policy-optimization), [Actor-Critic](#actor-critic), [RL](#rl---reinforcement-learning)

### A3C - Asynchronous Advantage Actor-Critic
**Full Name**: Asynchronous Advantage Actor-Critic
**Description**: On-policy actor-critic reinforcement learning algorithm using multiple asynchronous parallel actors, each running in its own environment instance with its own network copy. **First deep RL algorithm to demonstrate that parallelism across CPU threads could replace experience replay for decorrelating training data** (Mnih et al., 2016). Each actor independently computes gradients and pushes them to a shared global network. Largely superseded by the synchronous variant A2C (simpler, deterministic, better GPU utilization) and PPO (more stable updates).
**Documentation**: [A3C Term](../resources/term_dictionary/term_a3c.md)
**Related**: [A2C](#a2c---advantage-actor-critic), [PPO](#ppo---proximal-policy-optimization), [Actor-Critic](#actor-critic), [RL](#rl---reinforcement-learning)

### ER - Experience Replay
**Full Name**: Experience Replay
**Description**: Technique in reinforcement learning where an agent stores interaction transitions $(s, a, r, s')$ in a fixed-size memory buffer and later samples random mini-batches for training. **Experience replay was one of two critical innovations (alongside the target network) that made Deep Q-Networks (DQN) practical**, breaking temporal correlations in sequential data and enabling multiple reuse of each transition. Key variants include Prioritized Experience Replay (PER) which samples by TD error magnitude, and Hindsight Experience Replay (HER) for sparse reward settings. First proposed by Lin (1992) but became essential when Mnih et al. (2015) demonstrated human-level Atari play with DQN.
**Documentation**: [Experience Replay Term](../resources/term_dictionary/term_experience_replay.md)
**Related**: [DQN](#dqn---deep-q-network), [Q-Learning](#q-learning), [RL](#rl---reinforcement-learning)

### PG - Policy Gradient
**Full Name**: Policy Gradient
**Description**: Class of reinforcement learning algorithms that directly optimize a parameterized policy $\pi_\theta(a|s)$ by performing gradient ascent on expected cumulative return. **The Policy Gradient Theorem (Sutton et al., 1999) enables computing the gradient from sampled trajectories without knowing environment dynamics**, making these methods model-free and compatible with continuous action spaces. REINFORCE (Williams, 1992) was the first algorithm; modern variants include Actor-Critic, TRPO, PPO, and SAC. Policy gradient methods are the foundation of RLHF for LLM alignment.
**Documentation**: [Policy Gradient Term](../resources/term_dictionary/term_policy_gradient.md)
**Related**: [PPO](#ppo---proximal-policy-optimization), [Actor-Critic](#actor-critic), [SAC](#sac---soft-actor-critic), [RL](#rl---reinforcement-learning)

### PI - Policy Iteration
**Full Name**: Policy Iteration
**Description**: Dynamic programming method for solving Markov Decision Processes (MDPs) that alternates between policy evaluation (computing the value function for the current policy) and policy improvement (constructing a greedy policy from those values). **First explicitly formulated by Ronald Howard (1960), policy iteration is guaranteed to converge to the optimal policy in a finite number of iterations for finite MDPs.** Through the concept of Generalized Policy Iteration (GPI), the evaluation/improvement loop is recognized as the unifying structure behind virtually all RL algorithms, from Q-learning to modern actor-critic methods.
**Documentation**: [Policy Iteration Term](../resources/term_dictionary/term_policy_iteration.md)
**Related**: [Q-Learning](#q-learning), [Actor-Critic](#actor-critic), [RL](#rl---reinforcement-learning)

### OAPL - Optimal Advantage-based Policy Learning
**Full Name**: Optimal Advantage-based Policy optimization with Lagged inference
**Description**: Off-policy RL algorithm for post-training LLMs, introduced in KARL (Chang et al., 2026). Minimizes a least-square regression objective derived from the KL-regularized RL optimal policy: $\min_{\pi} \sum (\beta \ln \pi(y|x)/\pi_{\text{ref}}(y|x) - (r(x,y) - \hat{V}^*(x)))^2$. Uses two-parameter variant ($\beta_1$ for value estimation, $\beta_2$ for KL regularization). Avoids online rollout generation during training (the main bottleneck of [GRPO](../resources/term_dictionary/term_grpo.md)), and requires no stability heuristics for [MoE](../resources/term_dictionary/term_moe.md) architectures. Supports iterative training by replacing $\pi_{\text{ref}}$ with the latest policy.
**Documentation**: [OAPL Term](../resources/term_dictionary/term_oapl.md)
**Key Properties**: Off-policy (uses pre-collected rollouts), stable for MoE, iterative, sample efficient
**Related**: [RL](#rl---reinforcement-learning), [GRPO](../resources/term_dictionary/term_grpo.md), [RLHF](../resources/term_dictionary/term_rlhf.md), [MoE](../resources/term_dictionary/term_moe.md)

### KARLBench - Knowledge Agent RL Benchmark
**Full Name**: Knowledge Agent Reinforcement Learning Benchmark
**Description**: 6-task evaluation suite for grounded reasoning agents (Chang et al., 2026). Tasks: BrowseComp-Plus (constraint entity search), TREC-Biogen (cross-document report synthesis), FinanceBench (tabular numerical reasoning), QAMPARI (exhaustive entity retrieval), FreshStack (procedural reasoning), PMBench (enterprise fact aggregation). Uses nugget-based evaluation with [LLM-as-a-Judge](../resources/term_dictionary/term_llm_as_a_judge.md). Explicit in-distribution (BrowseComp-Plus, TREC-Biogen) vs OOD (remaining 4) split for generalization evaluation.
**Documentation**: [KARLBench Term](../resources/term_dictionary/term_karlbench.md)
**Related**: [RL](#rl---reinforcement-learning), [RAG](../resources/term_dictionary/term_rag.md), [LLM-as-a-Judge](../resources/term_dictionary/term_llm_as_a_judge.md)

---

## Adversarial ML & AI Safety

### Adversarial - Adversarial Dynamics
**Full Name**: Adversarial Dynamics in Fraud Prevention
**Description**: The fundamental dynamic where bad actors actively adapt strategies to evade detection, creating a continuous arms race. **Unlike static prediction, adversarial settings mean distributions shift intentionally.** Manifests as MO evolution, attribute spoofing (Ghost MAA), and policy exploitation. Addressed by TattleTale (reactive), Dupin/SAFE (proactive simulation).
**Documentation**: [Adversarial Term](../resources/term_dictionary/term_adversarial)
**Related**: [Adversarial ML](#adversarial-ml), [Dupin](../resources/term_dictionary/term_dupin.md), [SAFE](../resources/term_dictionary/term_safe_t.md)

### Adversarial ML - Adversarial Machine Learning
**Full Name**: Adversarial Machine Learning
**Description**: Discipline studying ML vulnerabilities to intentional manipulation and developing defenses. **Three threat models: evasion (test-time), poisoning (train-time), model extraction (query access).** In BAP: abusers learn SI thresholds (evasion), create clean history before abuse (poisoning), infer model behavior from grant/deny patterns (extraction).
**Documentation**: [Adversarial ML Term](../resources/term_dictionary/term_adversarial_ml)
**Related**: [Adversarial](#adversarial---adversarial-dynamics), [Robustness](#robustness---model-robustness), [GAN](#gan---generative-adversarial-network)

### Adversarial Examples
**Full Name**: Adversarial Examples (Adversarial Perturbations)
**Description**: Inputs intentionally perturbed to cause misclassification while remaining imperceptible. First demonstrated by Szegedy et al. (2013). **In abuse domain: small behavior modifications (address munging, timing changes) that cross detection decision boundaries.** Key property: transferability — examples crafted for one model often fool others.
**Documentation**: [Adversarial Examples Term](../resources/term_dictionary/term_adversarial_examples)
**Related**: [Adversarial ML](#adversarial-ml), [Robustness](#robustness---model-robustness)

### Robustness - Model Robustness
**Full Name**: Model Robustness (Adversarial Robustness, Distributional Robustness)
**Description**: A model's ability to maintain performance under perturbations, distribution shifts, and adversarial inputs. **Critical in BAP because adversaries actively probe and adapt, patterns drift over time, and models must generalize across 23 marketplaces.** Approaches: adversarial training, DRO, ensemble diversity, continuous retraining.
**Documentation**: [Robustness Term](../resources/term_dictionary/term_robustness)
**Related**: [Adversarial ML](#adversarial-ml), [Adversarial Examples](#adversarial-examples)

### Attack Simulation
**Full Name**: Attack Simulation (Adversarial Red-Teaming)
**Description**: Proactively testing detection systems by simulating adversarial behavior — generating synthetic attacks, replaying historical MOs with variations, or training RL agents to discover novel evasion strategies. **Finds vulnerabilities before real adversaries exploit them.** Implemented via Dupin (RL-based) and SAFE (multi-agent co-evolution).
**Documentation**: [Attack Simulation Term](../resources/term_dictionary/term_attack_simulation)
**Related**: [Dupin](../resources/term_dictionary/term_dupin.md), [SAFE](../resources/term_dictionary/term_safe_t.md), [Adversarial](#adversarial---adversarial-dynamics)

### Multi-Agent Systems - MAS
**Full Name**: Multi-Agent Systems (Multi-Agent Reinforcement Learning)
**Description**: Computational systems where multiple autonomous agents interact — cooperating, competing, or mixed motives. **In BAP: SAFE (attacker-defender co-evolution), Dupin (multiple simulated abuser agents), organized abuse rings (real-world multi-agent problem).** Game-theoretic framing: abuse prevention as Stackelberg game.
**Documentation**: [Multi-Agent Systems Term](../resources/term_dictionary/term_multi_agent_systems)
**Related**: [SAFE](../resources/term_dictionary/term_safe_t.md), [RL](#rl---reinforcement-learning), [Multi-Agent](../resources/term_dictionary/term_multi_agent.md)

### AI Safety
**Full Name**: AI Safety (Alignment, Responsible AI)
**Description**: Ensuring AI systems behave as intended, don't cause unintended harm, and remain under human control. **In BAP: enforcement fairness, reward hacking prevention in RL systems, Human-in-the-Loop for edge cases, simulation containment (SAFE/Dupin).** Encompasses alignment, robustness, interpretability, and governance.
**Documentation**: [AI Safety Term](../resources/term_dictionary/term_ai_safety)
**Related**: [Robustness](#robustness---model-robustness), [Reward](#reward---reward-design), [RLHF](../resources/term_dictionary/term_rlhf.md)

---

## Model Evaluation & Metrics

### AUC - Area Under the Curve
**Full Name**: Area Under the Curve (ROC-AUC)
**Description**: Model's ability to distinguish classes (0.5=random, 1.0=perfect). BAP standards: ≥0.80 production, ≥0.90 excellent. Operational: evaluate at FPR thresholds (1%, 5%) not overall AUC. Limitation: high AUC ≠ good performance at operational FPR. Examples: DNR ~0.72-0.75, BSM 0.89.
**Documentation**: [AUC Term](../resources/term_dictionary/term_auc.md) ✅
**Wiki**: [ROC Deep Dive Review](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Internal/Models/Model_Review/)
**Interpretation**: 
  - AUC > 0.9: Excellent discrimination
  - AUC 0.8-0.9: Good discrimination  
  - AUC 0.7-0.8: Fair discrimination
  - AUC < 0.7: Poor discrimination (needs improvement)
**Operational Points**: TPR@1%FPR (stringent), TPR@5%FPR (standard), TPR@10%FPR (recall-focused)
**Complement**: [PR AUC](#precision) for imbalanced data (abuse is rare positive class)
**Tools**: sklearn.metrics.roc_auc_score, R's pROC package
**Related**: ROC Curve, [Precision](#precision), [Recall](#recall), [F1-Score](#f1-score), PR AUC

### False Positive - Type I Error / Over-Enforcement
**Full Name**: False Positive (FP / FPR — False Positive Rate)
**Description**: Occurs when a detection system incorrectly classifies a **legitimate customer as abusive** (predicted abuse, actual non-abuse), directly measuring **customer experience harm** in BAP. BAP maintains strict graduated FPR targets by enforcement severity: **<1% for account closures**, **<2% for warnings**, **10-15% for CAP routing**, and **<5% for RFS suppression** — reflecting the philosophy of prioritizing **precision over recall** for severe enforcement while accepting higher FPR for lighter friction. False positives generate VP escalations (483 in 2024, +15% YoY), $28M annual manual transfer costs, and long-term customer trust erosion measured via DSI. Reduction mechanisms include graduated friction, safelist (90-day bypass), RSPR standardized guidance, precision-based risk bands, CDA optimization, and SOPA LLM audit (98.9% accuracy).
**Documentation**: [False Positive Term](../resources/term_dictionary/term_false_positive.md)
**Wiki**: [BAP Product & Program](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseProductProgram/), [CAP Routing Rules](https://w.amazon.com/bin/view/ConcessionsAbusePrevention/Resources/Routing_Rules/)
**Formula**: FPR = FP / (FP + TN); Precision = TP / (TP + FP)
**FPR Targets**: Account Closure (<1%), Warn (<2%), Solicit (<5%), CAP Routing (10-15%), PFOC (<5%), RFS (<5%)
**CX Impact**: 483 VP escalations (2024), $28M manual transfer costs, trust erosion (DSI-measured)
**Reduction Mechanisms**: Graduated friction, Safelist (90-day), RSPR, Precision-Based Risk Bands, CDA, Model Retraining, SOPA LLM Audit
**Philosophy**: Precision over recall for severe enforcement; higher FPR acceptable for lighter friction
**⚠️ Disambiguation**: Not to be confused with FP (Fingerprint) — device identification signal
**Status**: ✅ Active - fundamental classification metric across all BAP programs
**Related**: [Precision](#precision), [Recall](../resources/term_dictionary/term_recall.md), [AUC](../resources/term_dictionary/term_auc.md), [CDA](../resources/term_dictionary/term_cda.md), [OE](../resources/term_dictionary/term_oe.md), [DSI](../resources/term_dictionary/term_dsi.md), [CAP Routing](../resources/term_dictionary/term_cap_routing.md), [Safelist](../resources/term_dictionary/term_safelist.md)

### Precision
**Full Name**: Precision (Positive Predictive Value / PPV)
**Description**: TP / (TP + FP) - "of flagged cases, how many are actually abuse?" BAP standards: ≥90% (production), ≥95% (automation), ≥98% (account closure). **BAP prioritizes precision** - FP cost (blocking good customer) exceeds FN cost. Validation: 5% control group agreement.
**Documentation**: [Precision Term](../resources/term_dictionary/term_precision.md) ✅
**Wiki**: [MENA Promotion ML](https://w.amazon.com/bin/view/MENA/Keen/Abuse/Projects/PromotionLimitAbuse/ML/), [DeepCARE](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Programs/DeepCARE/)
**Formula**: TP / (TP + FP)
**BAP Targets**: ≥90% (production), ≥95% (enforcement), ≥98% (account closure)
**Trade-off**: Higher precision → lower recall (cannot maximize both)
**Tools**: sklearn.metrics.precision_score, precision_recall_curve
**Related**: [Recall](#recall), [F1-Score](#f1-score), [AUC](#auc---area-under-the-curve), PR AUC

### Recall
**Full Name**: Recall (Sensitivity / True Positive Rate / TPR / Hit Rate)
**Description**: TP / (TP + FN) - "of actual abuse, how many did model catch?" BAP targets: ≥80% (discovery), ≥70% (queuing), 40-60% (automation). Trade-off: lower threshold = higher recall, lower precision. **Dollar Recall** often more important - aligns with business impact.
**Documentation**: [Recall Term](../resources/term_dictionary/term_recall.md) ✅
**Wiki**: [GPS ML Model](https://w.amazon.com/bin/view/Alexa_Shopping/DAE/Data_Science/Projects/GPS/), [ADEMA Dashboard](https://w.amazon.com/bin/view/DigitalSecurity/DeviceAbusePrevention/ADEMA_Dashboard/)
**Formula**: TP / (TP + FN)
**BAP Targets**: ≥80% (discovery), ≥70% (queuing), 40-60% (automation)
**Trade-off**: Higher recall → lower precision (cannot maximize both)
**ROC Component**: Y-axis of ROC curve (TPR)
**When Prioritized**: MO detection (Tattletale), high-value fraud, research/discovery
**Complement**: [Dollar Recall](#dollar-recall) - $ value of detected abuse (aligns with business impact)
**Tools**: sklearn.metrics.recall_score, precision_recall_curve
**Related**: [Precision](#precision), [F1-Score](#f1-score), [AUC](#auc---area-under-the-curve), [Tattletale](../resources/term_dictionary/term_tattletale.md)

### F1-Score
**Full Name**: F1 Score (F-measure, F1)
**Description**: Harmonic mean of precision and recall - balanced measure when both FP and FN matter. BAP: ≥0.85 excellent, 0.70-0.85 good. Example: CSMO F1=0.84. F-beta: β<1 favors precision, β>1 favors recall. Best for model comparison; production uses P/R directly.
**Documentation**: [F1 Score Term](../resources/term_dictionary/term_f1_score.md) ✅
**Wiki**: [ML Metrics](https://w.amazon.com/bin/view/Users/Andriy/learning/ml-metrics/), [KYT-AI](https://w.amazon.com/bin/view/TOPS_Tech_Team/COMS/KYT-AI/)
**Formula**: 2 × (Precision × Recall) / (Precision + Recall)
**Range**: 0.0 to 1.0 (higher is better)
**BAP Standards**: ≥0.85 (excellent), 0.70-0.85 (good), 0.60-0.70 (acceptable)
**Best For**: Model comparison, threshold optimization, balanced queue sizing
**Limitation**: Requires binary threshold; treats FP=FN equally
**Generalization**: F-beta (β<1 favors precision, β>1 favors recall)
**Tools**: sklearn.metrics.f1_score, fbeta_score
**Related**: [Precision](#precision), [Recall](#recall), [AUC](#auc---area-under-the-curve)


### PPL - Perplexity
**Full Name**: Perplexity
**Description**: Standard intrinsic evaluation metric for language models — the exponentiated average negative log-likelihood per token. PPL of $k$ means the model is as uncertain as choosing uniformly among $k$ options. Lower is better. Mathematically equivalent to exp(cross-entropy loss). GPT-2 achieved zero-shot SOTA on 7/8 LM benchmarks. **Caution**: PPL values are not comparable across different tokenizers (BPE vs WordPiece). Related metrics: bits per byte (BPB), bits per character (BPC). For abuse detection: PPL on domain text measures how well a pre-trained model covers abuse language patterns.
**Documentation**: [Perplexity Term](../resources/term_dictionary/term_perplexity.md)
**Formula**: PPL = exp(−1/N × Σ log p(xᵢ | x<ᵢ))
**Range**: 1.0 (perfect) to ∞ (higher = worse)
**Benchmarks**: 5-20 (excellent), 20-50 (good), 50-100 (moderate), 100+ (poor)
**Related**: [F1-Score](#f1-score), [AUC](#auc---area-under-the-curve), [BPE](#bpe---byte-pair-encoding)

### PPR - Personalized PageRank
**Full Name**: Personalized PageRank
**Description**: A graph ranking algorithm that measures every node's relevance to a specified seed node (or weighted set of seeds) by simulating random walks with restart. At each step the walker follows an edge with probability (1 − α) or teleports back to the seed with restart probability α (typically 0.15–0.20), producing scores that decay exponentially with graph distance from the seed. **Personalized PageRank is the foundational retrieval mechanism in GraphRAG systems**, ranking knowledge-graph entities for LLM queries without any learned parameters. It scales to billion-node graphs via Monte Carlo approximation (Pinterest's Pixie system, WWW 2018) and is used in abuse risk propagation to spread labels from confirmed-abuser seeds through buyer–seller–product networks.
**Documentation**: [Personalized PageRank Term](../resources/term_dictionary/term_ppr.md)
**Wiki**: https://dl.acm.org/doi/10.1145/3178876.3186183
**Related**: [PPR (GraphRAG)](../resources/term_dictionary/term_ppr.md), [Pixie Random Walk](../resources/term_dictionary/term_pixie_random_walk.md), [Random Walk](../resources/term_dictionary/term_random_walk.md), [GNN](#gnn---graph-neural-networks), [Knowledge Graph](../resources/term_dictionary/term_knowledge_graph.md)

### Question Type Classification
**Full Name**: Question Type Classification (Retrieval Evaluation)
**Description**: A 10-category taxonomy of information needs used to evaluate retrieval performance in the Abuse SlipBox. Each type maps to specific note subcategories as gold targets: definition (term notes), procedural (SOPs), enumeration (entry points), architectural (area/ETL notes), organizational (team notes), factual (table/repo notes), temporal (launch announcements), relational (graph paths), multi-hop (link chains), and gold FAQ (human-written Q&A). **The per-type Hit@5 breakdown is the primary diagnostic for identifying retrieval strategy failures**. Questions are generated deterministically from the database using template-based phrasing and SQL-derived gold labels.
**Documentation**: [Question Type Classification](../resources/term_dictionary/term_question_type_classification.md)
**Related**: [Knowledge Building Blocks](../resources/term_dictionary/term_knowledge_building_blocks.md), [Hit@K / MRR / NDCG](#performance-metrics), [RAG](../resources/term_dictionary/term_rag.md), [Information Retrieval](../resources/term_dictionary/term_information_retrieval.md)

---

## Optimization & Foundational Algorithms

### Feedback Loop
**Full Name**: Feedback Loop
**Description**: A system structure in which the output of a process is routed back as input to that same process, forming a closed circuit of circular causality. **The two fundamental types — reinforcing (positive) loops and balancing (negative) loops — are the building blocks of all dynamic system behavior.** Reinforcing loops amplify change (exponential growth or decline), while balancing loops counteract change and drive systems toward equilibrium or a goal. Formalized by Norbert Wiener in *Cybernetics* (1948) and applied extensively in Donella Meadows' system dynamics work. Understanding feedback loops is essential for diagnosing why systems resist intervention and produce unintended consequences.
**Documentation**: [Feedback Loop](../resources/term_dictionary/term_feedback_loop.md)
**Source**: Wiener, N. (1948). *Cybernetics*; Meadows, D.H. (2008). *Thinking in Systems: A Primer*
**Related**: [Systems Thinking](acronym_glossary_cognitive_science.md#systems-thinking), [Stocks and Flows](acronym_glossary_cognitive_science.md#stocks-and-flows), [Emergence](acronym_glossary_cognitive_science.md#emergence), [Habit Loop](acronym_glossary_cognitive_science.md#habit-loop), [Compound Effect](acronym_glossary_cognitive_science.md#compound-effect)

### Overfitting
**Full Name**: Overfitting (Over-Parameterization)
**Description**: When a model fits past data so perfectly that it captures **noise rather than signal**, producing poor performance on new data. The **bias-variance trade-off**: underfitting (high bias) misses signal; overfitting (high variance) memorizes noise. Countermeasures: **cross-validation** (test on unseen data), **regularization** (L1/L2 penalties, early stopping, dropout), and **Occam's razor** (prefer simpler models). Christian & Griffiths extend to life decisions: with sparse data, simple heuristics beat elaborate analysis — "when you have less data, you should think less." Setting a deliberation deadline is a form of regularization.
**Documentation**: [Overfitting Term](../resources/term_dictionary/term_overfitting.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 7
**Related**: [XGBoost](#xgboost), [Ensemble Learning](#ensemble-learning), [Simulated Annealing](#simulated-annealing)

### Simulated Annealing
**Full Name**: SA — Simulated Annealing
**Description**: Probabilistic optimization inspired by metallurgical annealing. Starts "hot" (accepting random moves including bad ones) and slowly "cools" (becoming more selective). Escapes **local optima** that trap greedy algorithms. Part of the randomized algorithms family: **sampling** (test a random subset), **Monte Carlo simulation** (simulate many random outcomes), and **randomized algorithms** (introduce deliberate randomness). Maps to the explore/exploit lifecycle: early in a process embrace randomness; as time passes, narrow focus.
**Documentation**: [Simulated Annealing Term](../resources/term_dictionary/term_simulated_annealing.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 9; Kirkpatrick et al. (1983)
**Related**: [Relaxation](#relaxation-optimization), [MAB](../resources/term_dictionary/term_mab.md), [Overfitting](#overfitting)

### Relaxation (Optimization)
**Full Name**: Mathematical Relaxation (Constraint / Continuous / Lagrangian)
**Description**: Technique for handling intractable (NP-hard) problems by temporarily loosening constraints. Three types: **constraint relaxation** (drop a hard constraint), **continuous relaxation** (treat discrete 0/1 choices as continuous 0.0–1.0), **Lagrangian relaxation** (convert hard constraints to penalties). The **relaxation gap** (relaxed solution − true optimal) measures how much constraints actually cost — a small gap means you're already near optimal. Life application: "What would I do if money weren't an issue?" reveals ideal solutions before practical constraints are reapplied.
**Documentation**: [Relaxation Term](../resources/term_dictionary/term_relaxation_optimization.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 8
**Related**: [Simulated Annealing](#simulated-annealing), [MILP](../resources/term_dictionary/term_milp.md), [Overfitting](#overfitting)

### Sorting Algorithms
**Full Name**: Sorting Algorithms (Comparison and Non-Comparison Sorts)
**Description**: Algorithms for arranging elements into defined order. Key algorithms: **bubble sort** (O(n²), error-robust), **merge sort** (O(n log n), error-sensitive), **bucket sort** (O(n), categorizes only). Proven **lower bound**: Ω(n log n) comparisons required for comparison-based sorting — you cannot rank n items in fewer comparisons. The **search-sort trade-off**: if search is rare, don't sort (sequential scan is fine); if search is frequent, pre-sorting pays off. "The messiest desk may be the most rationally organized."
**Documentation**: [Sorting Algorithms Term](../resources/term_dictionary/term_sorting_algorithms.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 3
**Related**: [LRU Cache](../resources/term_dictionary/term_lru_cache.md), [Scheduling Algorithms](../resources/term_dictionary/term_scheduling_algorithms.md)

### Exponential Backoff
**Full Name**: Exponential Backoff (Binary Exponential Backoff / AIMD)
**Description**: Retry strategy where wait time doubles after each failure (2^n intervals). Foundational for congestion management in shared systems. Key principles: **flow control** (match output to receiver capacity), **buffer management** (drop requests when queue is full — better than infinite delay), **AIMD** (Additive Increase, Multiplicative Decrease — gradually increase rate, sharply cut on congestion). TCP's sawtooth congestion control pattern. Human analog: gradually take on more commitments; when overwhelmed, cut back by half, not by a little.
**Documentation**: [Exponential Backoff Term](../resources/term_dictionary/term_exponential_backoff.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 10; Jacobson (1988)
**Related**: [Scheduling Algorithms](#scheduling-algorithms), [LRU Cache](#lru-cache)

### Optimal Stopping
**Full Name**: Optimal Stopping (Secretary Problem / 37% Rule)
**Description**: Sequential decision framework for choosing the best option from a series presented one at a time. The **37% rule**: observe and reject the first 37% (1/e) of candidates to set a baseline, then commit to the next option exceeding the best seen. Provably optimal yet failing two-thirds of the time — illustrating that a sound process does not guarantee a sound outcome. Variants include recall (can revisit rejected options), known distributions (use absolute thresholds), and cost-of-search adjustments.
**Documentation**: [Optimal Stopping Term](../resources/term_dictionary/term_optimal_stopping.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 1
**Related**: [MAB](../resources/term_dictionary/term_mab.md), [Satisficing](#satisficing), [Sorting Algorithms](#sorting-algorithms)

### Scheduling Algorithms
**Full Name**: Scheduling Algorithms (EDD, SPT, Moore's, WSJF)
**Description**: Systematic strategies for task ordering to optimize a specific objective. **Earliest Due Date (EDD)** prevents extreme lateness; **Shortest Processing Time (SPT)** minimizes total waiting time (GTD's "two-minute rule"); **Moore's Algorithm** minimizes the count of late tasks; **Weighted Shortest Job First (WSJF)** maximizes value per effort. Equally important: **context switching** costs (every task switch incurs overhead), **thrashing** (when managing the schedule consumes more time than doing work — cure: do less), and **interrupt coalescing** (batch interruptions like Knuth's quarterly mail review).
**Documentation**: [Scheduling Algorithms Term](../resources/term_dictionary/term_scheduling_algorithms.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 5
**Related**: [Optimal Stopping](#optimal-stopping), [LRU Cache](#lru-cache), [Exponential Backoff](#exponential-backoff)

### LRU Cache
**Full Name**: LRU — Least Recently Used (Cache Eviction Policy)
**Description**: Cache eviction strategy that removes the item not accessed for the longest time, exploiting **temporal locality**. Best general-purpose caching strategy. Extended to physical organization: **piling (not filing) is rational** because a pile naturally implements LRU — the most recently used item is on top. The memory hierarchy (registers → cache → RAM → disk) maps to human storage (working memory → desk → filing cabinet → archives). Other strategies: LFU (least frequently used), random eviction (surprisingly competitive).
**Documentation**: [LRU Cache Term](../resources/term_dictionary/term_lru_cache.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 4
**Related**: [Scheduling Algorithms](#scheduling-algorithms), [Sorting Algorithms](#sorting-algorithms), [Exponential Backoff](#exponential-backoff)

### Game Theory
**Full Name**: Game Theory (Nash Equilibrium, Mechanism Design, Vickrey Auction)
**Description**: Mathematical study of strategic interaction. Key concepts: **Nash equilibrium** (stable state where no player benefits from unilateral change), **mechanism design** (design rules so selfish behavior produces good outcomes — "reverse game theory"), **price of anarchy** (efficiency loss from selfishness vs. cooperation), **Vickrey auction** (second-price sealed bid where truthful bidding is dominant strategy). Central insight: design systems where **honest behavior is the best policy**, rather than relying on altruism.
**Documentation**: [Game Theory Term](../resources/term_dictionary/term_game_theory.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*, Chapter 11
**Related**: [Information Cascades](#information-cascades), [Satisficing](#satisficing), [Relaxation](#relaxation-optimization)

### Satisficing
**Full Name**: Satisficing (Satisfy + Suffice)
**Description**: Decision strategy aiming for "good enough" rather than optimal, coined by Herbert Simon (1956). Grounded in **bounded rationality** — real agents face limited time, information, and computation. Since most real-world problems are **intractable** (NP-hard), "good enough" solutions found quickly beat perfect solutions found too late. Satisficing is not lazy thinking; it is the computationally rational response to intractability. Research (Schwartz) shows satisficers report higher life satisfaction than maximizers despite objectively similar outcomes.
**Documentation**: [Satisficing Term](../resources/term_dictionary/term_satisficing.md)
**Source**: Christian, B. & Griffiths, T. (2016). *Algorithms to Live By*; Simon, H.A. (1956)
**Related**: [Optimal Stopping](#optimal-stopping), [Overfitting](#overfitting), [Computational Kindness](#computational-kindness)

### Best-First Search
**Full Name**: Best-First Search (Priority-First / Informed Graph Search)
**Description**: A class of graph-traversal algorithms that expands frontier nodes in order of an evaluation function $f(n)$, using a **priority queue** (min-heap) to always pop the most-promising candidate next. The umbrella covers **greedy best-first search** ($f = h$, fast but suboptimal), **A\*** ($f = g + h$, optimal under admissible $h$), **Dijkstra** ($h = 0$, optimal but uninformed), and **breadth-first search** (constant heuristic). Formalized in Pearl's 1984 textbook *Heuristics*. Used for pathfinding, planning, theorem proving, NLP parsing, and knowledge-graph retrieval (the SlipBox's Strategy 6 is a greedy best-first BFS with cosine-similarity heuristic).
**Documentation**: [Best-First Search Term](../resources/term_dictionary/term_best_first_search.md)
**Source**: Pearl, J. (1984). *Heuristics: Intelligent Search Strategies*. Addison-Wesley
**Related**: [A\*](#a-search), [MCTS](../resources/term_dictionary/term_mcts.md), [PageRank](#pagerank), [Random Walk](#random-walk), [Cosine Similarity](#cosine-similarity)

### A\* Search
**Full Name**: A\* (A-Star) — Optimal Best-First Search with $f = g + h$
**Description**: The canonical informed best-first algorithm: expands nodes in order of $f(n) = g(n) + h(n)$, where $g$ is the actual cost from start and $h$ is a heuristic estimate of cost to goal. **Invented by Hart, Nilsson & Raphael (1968) at Stanford for Shakey the robot**, A\* is **optimal** when $h$ is admissible (never overestimates) on tree search and when $h$ is consistent (monotone) on graph search. Dechter & Pearl (1985) proved A\* is **optimally efficient** — no other admissible algorithm using the same $h$ can expand fewer nodes. Time complexity $O(b^d)$ worst case; memory is the binding constraint, motivating bounded variants (weighted A\*, IDA\*, SMA\*, D\*). Default algorithm for video-game pathfinding, robotic navigation, and informed planning.
**Documentation**: [A\* Search Term](../resources/term_dictionary/term_a_star_search.md)
**Source**: Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968). *A Formal Basis for the Heuristic Determination of Minimum Cost Paths.* IEEE Trans. SSC 4(2)
**Related**: [Best-First Search](#best-first-search), [MCTS](../resources/term_dictionary/term_mcts.md), [Heuristic](../resources/term_dictionary/term_heuristic.md), [PageRank](#pagerank)

---

## Large Language Models

> **Note**: LLM-related terms have been extracted to their own dedicated glossary.
> See **[Large Language Models (LLM) Glossary](acronym_glossary_llm.md)** for:
> LLM, Claude, GenAI, LILA, CRFM, RAG, HippoRAG, PPR, KG, LoRA, PEFT, NLP, BERT, SBERT,
> CrossBERT, OpenIE, NLI, Bidirectional Entailment, SE (Semantic Entropy), SEP (Semantic Entropy Probes),
> UAG (Uncertainty-Aware Generation), VLM, Computer Vision, SWIN Transformer, Diffusion Model,
> LLM as a Judge, Ontology, GreenTEA, SOPA, SPOT-X, AutoSignality, Polygraph, SessionMiner,
> MLA-E, Sandstone, AgentSpace, Rufus, Amelia.

---
## Quick Reference Table

### By Task Type

| Task | Algorithms | Use Cases |
|------|-----------|-----------|
| Tabular Classification | XGBoost, LightGBM, Random Forest | Risk scoring, abuse detection |
| Sequence Modeling | LSTM, GRU, Transformer | Behavior analysis, temporal patterns |
| Graph Learning | GNN | Multi-account abuse, relationship modeling |
| Text Analysis | LLM, NLP, Transformer | Message analysis, policy interpretation |
| Multi-Task | MTL | Simultaneous prediction of multiple abuse types |

### By Model Complexity

| Complexity | Models | Characteristics |
|------------|--------|-----------------|
| Simple | Logistic Regression, Decision Trees | Interpretable, fast, baseline |
| Medium | XGBoost, Random Forest | High performance, moderate complexity |
| Complex | GNN, LLM, Transformer | State-of-art, requires more data/compute |

### Performance Metrics

| Metric | Focus | When to Use |
|--------|-------|-------------|
| AUC | Overall discrimination | General model quality |
| Precision | Minimize false positives | Avoid over-enforcement |
| Recall | Minimize false negatives | Catch all abuse |
| F1-Score | Balance both | Find optimal trade-off |

---


## In-Context Learning & Meta-Learning (New Q1 2026)

### MLA-E — Meta Learner Analytic Engine
**Full Name**: Meta Learner Analytic Engine
**Definition**: [term_mla_e](../resources/term_dictionary/term_mla_e.md) — In-context learning meta-classifier (internal TabPFN v2) for fraud/abuse detection without task-specific training.

### TabPFN — Tabular Prior-data Fitted Network
**Full Name**: Tabular Prior-data Fitted Network
**Definition**: [term_tabpfn](../resources/term_dictionary/term_tabpfn.md) — Transformer foundation model for zero-shot tabular classification via in-context learning.

### ConAM — Continuous Attack Mitigator
**Full Name**: Continuous Attack Mitigator
**Definition**: [term_conam](../resources/term_dictionary/term_conam.md) — Unified RL framework for continuous fraud detection across customer journey checkpoints (BCQL + Bayesian optimization).

## ML Research Conferences

### AMLC - Amazon Machine Learning Conference
**Full Name**: Amazon Machine Learning Conference
**Description**: Amazon's premier internal ML research conference, held annually since 2013. AMLC provides a peer-reviewed, triple-blind venue for Amazonians to present ML research across 17 submission categories including Fraud/Security/Abuse Prevention and ML Algorithms & Tools. Papers follow NeurIPS single-column format (4–8 pages) and require a mandatory Customer Problem Statement. **The conference achieves academic-grade rigor with ~22% acceptance rate and 1,400+ reviewers**, making it the primary internal venue for validating ML research novelty at Amazon.
**Documentation**: [AMLC](../resources/term_dictionary/term_amlc.md)
**Wiki**: https://w.amazon.com/bin/view/Amazon-Science/events/AMLC/2026/
**Related**: [Cursus](../resources/term_dictionary/term_cursus.md), [SageMaker](../resources/term_dictionary/term_sagemaker.md), [MLOps](../resources/term_dictionary/term_mlops.md)

## Related Glossaries

- [Systems & Platform](acronym_glossary_systems.md) - ML infrastructure (SAIS, MODS, MIMS)
- [Data & Metrics](acronym_glossary_data_metrics.md) - Training data and metrics
- [Teams & Organizations](acronym_glossary_teams.md) - Applied Scientists, ML teams

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md)

---

**Last Updated**: February 16, 2026  
**Entries**: 38+ ML algorithms, architectures, and techniques
