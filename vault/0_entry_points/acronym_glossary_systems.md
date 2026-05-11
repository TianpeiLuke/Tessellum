---
tags:
  - entry_point
  - index
  - navigation
  - quick_reference
  - glossary
  - systems
  - platforms
keywords:
  - ML systems
  - risk evaluation
  - URES
  - SAIS
  - platforms
topics:
  - ML platforms
  - risk evaluation
  - technical systems
language: markdown
date of note: 2026-01-24
status: active
building_block: navigation
---

# Systems & Platform Glossary

**Purpose**: Quick reference for core ML development, risk evaluation, and infrastructure platforms used by Buyer Abuse Prevention.

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md)

---

## ML Development Platforms

### AgentZ - Agentic AI Platform for Knowledge Operations Work
**Full Name**: AgentZ
**Description**: Amazon's multi-tenant, self-service agent creation platform developed by Applied AI for automating Knowledge Operations Work (KOW). Uses a **Dynamic Action Planning and Execution (DAPE)** engine that decomposes complex tasks into executable steps, leveraging a Capability Marketplace of reusable AI primitives (CV, NLP, web browsing, HITL). Supports both dynamic ReAct agents and deterministic workflow agents, with built-in human-in-the-loop quality assurance.
**Documentation**: [AgentZ](../resources/term_dictionary/term_agentz.md)
**Related**: [Agentic AI](../resources/term_dictionary/term_agentic_ai.md), [MCP](../resources/term_dictionary/term_mcp.md)

### SAIS - Secure AI Sandbox
**Full Name**: Secure AI Sandbox
**Description**: Primary ML development environment - Red-certified Jupyter Lab workspace for data exploration, model development, and rule testing
**Documentation**: [SAIS Term](../resources/term_dictionary/term_sais.md)
**Portal**: https://secure-ai-sandbox.ctps.amazon.dev/
**Status**: ✅ Primary compute environment (preferred over NAWS/MAWS)
**Related**: [SAIS Compute Guide](../resources/compute_environment/compute_sais_sandbox.md)

### BYOA - Bring Your Own Account
**Full Name**: Bring Your Own Account
**Description**: AWS account model where SAIS manages sandbox instances in the client team's own AWS account. **Teams are financially responsible for IMR costs** while Core Services handles operational costs. Each BYOA account gets team-shared and per-user S3 buckets, CodeCommit repos, and sandbox instances. Tenant config stored in CmlsByoaTenant package.
**Documentation**: [BYOA Term](../resources/term_dictionary/term_byoa.md)
**Wiki**: https://w.amazon.com/bin/view/CMLS/EE/Bring-Your-Own-Account/
**Related**: [SAIS](#sais---secure-ai-sandbox), [Secure PyPI](#secure-pypi---sais-private-python-repository)

### Secure PyPI - SAIS Private Python Repository
**Full Name**: Secure PyPI
**Description**: SAIS's private pip repository backed by Amazon CodeArtifact curation. Provides all PyPI.org packages minus those blocked by security/licensing compliance scanner. **Packages are NOT persisted between sandbox restarts** — use `!pip install` at the top of each notebook. Credential refresh via `/home/sandbox/scripts/secure-pypi-login.sh`.
**Documentation**: [Secure PyPI Term](../resources/term_dictionary/term_secure_pypi.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/SecureAISandbox/Guides/SecurePyPI/
**Related**: [SAIS](#sais---secure-ai-sandbox), [BYOA](#byoa---bring-your-own-account)

### BCCE - Banyan CX Central Evaluation
**Full Name**: Banyan CX Central Evaluation
**Description**: Centralized evaluation infrastructure for comprehensive **offline regression testing** across Customer Experiences (CX), primarily in the Alexa/AIDo domain. Provides standardized framework for running evaluations and making prompt promotion decisions. Calculates metrics including verbosity, friction, and on-topic scores. NOT a BAP term — belongs to Alexa AI evaluation.
**Documentation**: [BCCE Term](../resources/term_dictionary/term_bcce.md)
**Wiki**: https://w.amazon.com/bin/view/AIDoDataEngineering/BCCE/UserGuide/
**Related**: [SAIS](#sais---secure-ai-sandbox), [URES](../resources/term_dictionary/term_ures.md)

### CAP Theorem - Brewer's Theorem
**Full Name**: Consistency, Availability, Partition Tolerance Theorem
**Description**: A fundamental theorem in distributed systems stating that a distributed data store can guarantee at most two of three properties simultaneously: consistency, availability, and partition tolerance. Since network partitions are inevitable, the practical choice is between CP (consistent but may reject requests) and AP (available but may return stale data). **Modern systems like DynamoDB offer tunable consistency per operation**, allowing developers to choose the trade-off at the query level rather than the system level.
**Documentation**: [CAP Theorem](../resources/term_dictionary/term_cap_theorem.md)
**Related**: [DynamoDB](../resources/term_dictionary/term_ddb.md), [Redshift](../resources/term_dictionary/term_redshift.md), [Microservices Architecture](../resources/term_dictionary/term_microservices_architecture.md)

### Consistency - Data Consistency in Distributed Systems
**Full Name**: Data Consistency (CAP)
**Description**: In the CAP theorem, consistency means every read returns the most recent write — all nodes see the same data simultaneously. Strong consistency (linearizability) requires coordination between nodes via consensus protocols, introducing latency. **This is distinct from ACID's "C" which refers to database invariants.** Modern systems offer tunable consistency levels, from eventual consistency (cheapest) through causal consistency to strong consistency (most expensive).
**Documentation**: [Consistency](../resources/term_dictionary/term_consistency.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [ACID](../resources/term_dictionary/term_acid.md), [DynamoDB](../resources/term_dictionary/term_ddb.md)

### Availability - System Availability in Distributed Systems
**Full Name**: System Availability (CAP)
**Description**: In the CAP theorem, availability means every request to a non-failing node receives a response, without guarantee of containing the most recent write. AP systems like DynamoDB and Cassandra prioritize responding over freshness. **This is distinct from operational "high availability" measured as uptime percentage (e.g., 99.99%).** Availability is achieved through replication, failover, and graceful degradation.
**Documentation**: [Availability](../resources/term_dictionary/term_availability.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [DynamoDB](../resources/term_dictionary/term_ddb.md)

### Partition Tolerance - Network Partition Tolerance
**Full Name**: Network Partition Tolerance (CAP)
**Description**: In the CAP theorem, partition tolerance means the system continues operating despite arbitrary message loss between nodes. Since network partitions are inevitable in distributed systems, **partition tolerance is effectively non-negotiable**, making the real CAP choice between consistency and availability. Systems must handle split-brain scenarios and reconcile divergent state after partitions heal using strategies like vector clocks or CRDTs.
**Documentation**: [Partition Tolerance](../resources/term_dictionary/term_partition_tolerance.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [Microservices Architecture](../resources/term_dictionary/term_microservices_architecture.md)

### SAR - Scalability, Availability, Reliability
**Full Name**: Scalability, Availability, Reliability
**Description**: A framework for the three fundamental non-functional requirements of distributed systems. Scalability measures growth capacity, availability measures uptime (quantified in "nines"), and reliability measures correctness (quantified by MTBF/MTTR). **The key insight is that these three properties are in pairwise tension — optimizing one can degrade another.** The framework extends to include durability, resilience, and performance, and connects to the SLA → SLO → SLI hierarchy for formalizing quality commitments.
**Documentation**: [SAR](../resources/term_dictionary/term_sar.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [Availability](#availability---system-availability-in-distributed-systems), [Architecture Characteristics](../resources/term_dictionary/term_architecture_characteristics.md)

### FLP Impossibility - Fischer-Lynch-Paterson Result
**Full Name**: Fischer-Lynch-Paterson Impossibility Result
**Description**: A 1985 theorem proving that no deterministic algorithm can guarantee consensus in an asynchronous distributed system if even one process can crash. **This is considered the most fundamental impossibility result in distributed computing.** Practical systems circumvent FLP through randomization, partial synchrony (timeouts), or failure detectors. The result is more fundamental than the CAP theorem — CAP constrains data stores while FLP constrains the consensus protocols that underpin them.
**Documentation**: [FLP Impossibility](../resources/term_dictionary/term_flp_impossibility.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [Consistency](#consistency---data-consistency-in-distributed-systems)

### 2PC - Two-Phase Commit
**Full Name**: Two-Phase Commit Protocol
**Description**: A distributed consensus protocol that coordinates all participants in a distributed transaction to agree on whether to commit or abort. Operates in two phases: Prepare (participants vote YES/NO) and Commit (coordinator broadcasts global decision). **2PC is a blocking protocol — if the coordinator crashes after collecting votes, participants holding locks are stuck until recovery.** Used for cross-shard ACID transactions in sharded databases (Vitess, Citus, Spanner) and microservices requiring strong consistency.
**Documentation**: [Two-Phase Commit](../resources/term_dictionary/term_two_phase_commit.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [FLP Impossibility](#flp-impossibility---fischer-lynch-paterson-result), [Saga Pattern](#saga-pattern)

### CRDT - Conflict-free Replicated Data Type
**Full Name**: Conflict-free Replicated Data Type
**Description**: A family of data structures designed for replicated systems that guarantee automatic convergence without coordination. CRDTs achieve strong eventual consistency: all replicas that receive the same set of updates converge to the same state regardless of delivery order. **Two forms exist: state-based (CvRDT, ship full state) and operation-based (CmRDT, ship operations).** Common types include G-Counter (grow-only counter), PN-Counter (increment/decrement), G-Set (grow-only set), OR-Set (observed-remove set), and LWW-Register. Used in Riak, Redis Enterprise, and collaborative editing systems.
**Documentation**: [CRDT](../resources/term_dictionary/term_crdt.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [Consistency](#consistency---data-consistency-in-distributed-systems), [Availability](#availability---system-availability-in-distributed-systems)

### Idempotency
**Full Name**: Idempotency (Distributed-System Property)
**Description**: The property of an operation that produces the same result whether applied once or multiple times — formally, `F(F(x)) = F(x)`. Idempotency is the load-bearing primitive that makes safe retry possible across unreliable networks: a client uncertain whether its request reached the server can replay the same request without risking duplicate side effects. **HTTP encodes this in its method semantics — `GET`, `PUT`, `DELETE` are idempotent; `POST` is not — and APIs use `Idempotency-Key` headers (Stripe, AWS) to make `POST` retries safe.** Common implementation patterns: state-comparison reconciliation (Kubernetes, Terraform), idempotency-key dedup (payment APIs), conditional writes (DynamoDB, ETag PUT), or naturally-idempotent semantics (`SET x = 5`, `MKDIR -p`). Idempotency converts at-least-once delivery into effectively exactly-once processing and is the foundation under sagas, CRDTs, and replication-log replay.
**Documentation**: [Idempotency](../resources/term_dictionary/term_idempotency.md)
**Related**: [Saga Pattern](#saga-pattern), [CRDT](#crdt---conflict-free-replicated-data-type), [2PC](#2pc---two-phase-commit), [CAP Theorem](#cap-theorem---brewers-theorem)

### Saga Pattern
**Full Name**: Saga Pattern (Distributed Transaction Design Pattern)
**Description**: A design pattern for managing distributed transactions across multiple services without global locks. A saga decomposes operations into a sequence of local transactions with compensating transactions to undo completed steps on failure. **Two coordination styles: choreography (event-driven, no central controller) and orchestration (centralized saga coordinator).** Unlike 2PC, sagas are non-blocking and partition-tolerant but sacrifice strong isolation, requiring careful handling of intermediate states.
**Documentation**: [Saga Pattern](../resources/term_dictionary/term_saga_pattern.md)
**Related**: [2PC](#2pc---two-phase-commit), [CAP Theorem](#cap-theorem---brewers-theorem), [Consistency](#consistency---data-consistency-in-distributed-systems)

### Vitess - MySQL Horizontal Scaling Middleware
**Full Name**: Vitess (MySQL Sharding Middleware)
**Description**: An open-source CNCF graduated project that sits between application servers and MySQL instances, transparently managing query routing, connection pooling, shard management, and automatic failover. **Vitess makes a horizontally sharded MySQL deployment appear as a single logical database.** Architecture includes VTGate (stateless proxy), VTTablet (per-instance agent), and a topology service. Used by YouTube, Slack, Square, JD.com (35M QPS), and powers PlanetScale's managed database platform.
**Documentation**: [Vitess](../resources/term_dictionary/term_vitess.md)
**Related**: [MongoDB](#mongodb---document-oriented-nosql-database), [2PC](#2pc---two-phase-commit), [Citus](#citus---distributed-postgresql-extension)

### Citus - Distributed PostgreSQL Extension
**Full Name**: Citus (PostgreSQL Sharding Extension)
**Description**: An open-source PostgreSQL extension that transforms a single PostgreSQL database into a horizontally scalable distributed database. **Runs as a native extension, not middleware — preserving PostgreSQL's full SQL, ACID transactions, and extension ecosystem.** Supports distributed tables (hash-sharded), reference tables (replicated), and schema-based sharding (Citus 12+). Acquired by Microsoft in 2019, available as Azure Cosmos DB for PostgreSQL.
**Documentation**: [Citus](../resources/term_dictionary/term_citus.md)
**Related**: [Vitess](#vitess---mysql-horizontal-scaling-middleware), [MongoDB](#mongodb---document-oriented-nosql-database), [2PC](#2pc---two-phase-commit)

### Amdahl's Law - Parallel Speedup Limit
**Full Name**: Amdahl's Law (Gene Amdahl, 1967)
**Description**: A fundamental law stating that the maximum speedup from parallelization is limited by the serial fraction of the workload. If 5% of a program is serial, maximum speedup is 20× regardless of processor count. **The serial bottleneck always dominates at scale.** Gustafson's Law (1988) provides a counterpoint for scaled problems, and Gunther's Universal Scalability Law extends it with contention penalties where throughput can actually decrease with more nodes.
**Documentation**: [Amdahl's Law](../resources/term_dictionary/term_amdahls_law.md)
**Related**: [CAP Theorem](#cap-theorem---brewers-theorem), [FLP Impossibility](#flp-impossibility---fischer-lynch-paterson-result), [Data Parallelism](../resources/term_dictionary/term_data_parallelism.md)

### CJMS - Cradle Jobs Management Service
**Full Name**: Cradle Jobs Management Service
**Description**: Dragon team service that creates and monitors Cradle data collection jobs, replacing the historic SAIS-managed job creation. Used by MDSDataLoader and CradleDataLoader via `cradle_job_provider='CJMS'` parameter. **User experience is unchanged** — only the backend job management is migrated. Rollback by setting `cradle_job_provider='SAIS'`.
**Documentation**: [CJMS Term](../resources/term_dictionary/term_cjms.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/SecureAISandbox/Guides/WorkingWithMDSData
**Related**: [SAIS](#sais---secure-ai-sandbox), [DAWS](#daws---data-analytics-workflow-service), [MMS](#mms---model-management-service)

### DVS - Data Vault Store
**Full Name**: Data Vault Store
**Description**: CMLS tool providing fast, secure access to recent MDS data via FeatureHub integration. Unlike bulk Cradle downloads, DVS enables **low-latency lookups of individual records** by ID. Data retention is 3 months default (6 months max). Not all record sets are available — check dvs-dataset-kinesisstreams-* allow lists.
**Documentation**: [DVS Term](../resources/term_dictionary/term_dvs.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/SecureAISandbox/Guides/AccessDVSData/
**Related**: [SAIS](#sais---secure-ai-sandbox), [UMLC](#umlc---unified-machine-learning-catalog)

### RetroScore - MMS Model Comparison Tool
**Full Name**: RetroScore
**Description**: Tool for comparing MMS models by scoring historical data against them. Supports RFUGE and PMML model types. **Runs as a Docker container on sandbox** requiring 30+ GB disk space. Four score types: legacy-score, forest-score, score-percentile, calibrated-score. Accessed via `GenericMMSModel.load_from_mms()` and `model.run_retroscore()`.
**Documentation**: [RetroScore Term](../resources/term_dictionary/term_retroscore.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/SecureAISandbox/Guides/Retroscore
**Related**: [MMS](#mms---model-management-service), [DAWS](#daws---data-analytics-workflow-service), [SAIS](#sais---secure-ai-sandbox)

### CloudFormation - AWS Infrastructure-as-Code Service
**Full Name**: AWS CloudFormation
**Description**: AWS service for defining infrastructure in JSON/YAML templates that create and manage AWS resources as stacks. **Foundation for all CDK pipelines** — CDK generates CloudFormation templates, which are deployed via BATS/BARS/PDG. Supports any AWS resource creatable via API. Stacks can be created, updated, and deleted as a unit.
**Documentation**: [CloudFormation Term](../resources/term_dictionary/term_cloudformation.md)
**Wiki**: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
**Related**: [CDK](../resources/term_dictionary/term_cdk.md), [BATS](#bats---build-artifact-transform-service), [BONES](#bones---bootstrap-stack)

### CDKBuild - Brazil Build System for CDK
**Full Name**: CDKBuild
**Description**: TypeScript compound Brazil build system created by the Golden Path team. **Combines NpmPrettyMuch and CDK CLI** into a 5-step process: brazil-build → CDKBuild → NPM release → CDK synth → CloudFormation JSON in `./build/cdk.out/`. Provides convenience targets for personal account development (bootstrap, deploy:assets, cdkdeploy).
**Documentation**: [CDKBuild Term](../resources/term_dictionary/term_cdkbuild.md)
**Wiki**: https://code.amazon.com/packages/CDKBuild
**Related**: [CloudFormation](#cloudformation---aws-infrastructure-as-code-service), [Version Set](#version-set---brazil-version-management)

### Version Set - Brazil Version Management
**Full Name**: Version Set / VSR / VST
**Description**: Brazil mechanism for tracking versions of all code libraries in a software application. **VSR (Version Set Revision)** is a point-in-time snapshot mapping major versions to git commits. **VST (Version Set Targets)** filters to required packages, reducing build/deployment work. Commands: `brazil-vs-remove-major-versions`, `brazil-vs-revert`.
**Documentation**: [Version Set Term](../resources/term_dictionary/term_version_set.md)
**Wiki**: https://docs.hub.amazon.dev/docs/brazil/user-guide/concepts-version-set.html
**Related**: [CDKBuild](#cdkbuild---brazil-build-system-for-cdk), [BATS](#bats---build-artifact-transform-service)


### Alarmathon - Alarm Diagnostics & Remediation
**Full Name**: Alarm-a-thon (Alarm Diagnostics & Remediation Initiative)
**Description**: BAP initiative using AI-powered agents to systematically diagnose and remediate alarm configuration gaps across URES production intents. Built on the AIM framework with **three specialized agents**: Discovery (identifies live intents), Evaluator (validates configs against golden standard using live traffic data), and Deployment (publishes corrected LPT configs as CRs). Reduces alarm remediation from multi-day manual effort to single-command operation.
**Documentation**: [Alarmathon](../resources/term_dictionary/term_alarmathon.md)
**Wiki**: https://code.amazon.com/packages/BAPAlarmathon/trees/mainline
**Related**: [AIM](../resources/term_dictionary/term_aim.md), [URES](../resources/term_dictionary/term_ures.md)

### BATS - Build Artifact Transform Service
**Full Name**: Build Artifact Transform Service
**Description**: Converts build artifacts into deployment-ready bundles for Native AWS. Takes 3 inputs: transformer, parameters package, target package. **4 transformer types** (CodeDeploy, Docker, Lambda, RPM) and **4 publisher types** (CloudFormation preferred, ECR, S3, SAM). Aggregate transforms group multiple components with a UUID.
**Documentation**: [BATS Term](../resources/term_dictionary/term_bats.md)
**Wiki**: https://docs.hub.amazon.dev/docs/bats/index.html
**Related**: [BARS](#bars---build-artifact-replication-service), [BONES](#bones---bootstrap-stack), [PDG](#pdg---pipeline-deployment-groups)

### BARS - Build Artifact Replication Service
**Full Name**: Build Artifact Replication Service
**Description**: Shuttles BATS components (.zip in S3, Docker images in ECR) between AWS accounts/regions in a pipeline. **Decrypts with source KMS key, re-encrypts with target KMS key**, copies to target S3/ECR. Each account/region has its own S3 bucket and ECR repos in the BONES bootstrap stack.
**Documentation**: [BARS Term](../resources/term_dictionary/term_bars.md)
**Wiki**: https://docs.hub.amazon.dev/docs/bars/api-guide/index.html
**Related**: [BATS](#bats---build-artifact-transform-service), [BONES](#bones---bootstrap-stack), [PDG](#pdg---pipeline-deployment-groups)


### BLE - Bluetooth Low Energy
**Full Name**: Bluetooth Low Energy
**Description**: Wireless technology deployed for end-to-end package tracking in Amazon's supply chain (Project Meiga). **Light-sensitive BLE tags** applied to items detect if packages are opened or tampered. Phase 1 covers Under the Roof (FC to DS); Phase 2 covers Over the Road (DS to customer, pending legal). $1.8M funding approved for 19 sites.
**Documentation**: [BLE Term](../resources/term_dictionary/term_ble.md)
**Related**: [Blueberry](../resources/term_dictionary/term_blueberry.md), [Atlas](../resources/term_dictionary/term_atlas_secure_delivery.md)

### Bifrost - Amazon Business Enforcement Bridge
**Full Name**: Bifrost (Amazon Business Enforcement Bridge)
**Description**: Bidirectional enforcement synchronization architecture bridging Amazon Business (AB) and Buyer Abuse Prevention (BAP) systems using LEO orchestration. Bifrost ensures that enforcement actions (closures, deregistrations, reinstatements) taken in one domain automatically propagate to the other, closing the gap bad actors exploit between BAID-level and CID-level enforcement. **Phase 4 (March 2026) added automated MUA enforcement**, synchronizing multi-user account closures across BAP and ABRAM with a vetting safety net for high-value accounts. Phased roadmap spans Phase 1 (2023, AB→BAP one-way) through Phase 5 (planned ATS migration).
**Documentation**: [Bifrost](../resources/term_dictionary/term_bifrost.md)
**Wiki**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/SPADE/SPEAR/Projects/Bifrost/
**Related**: [ATS](../resources/term_dictionary/term_ats.md), [APWS](../resources/term_dictionary/term_apws.md), [MUA](../resources/term_dictionary/term_mua.md), [LEO](../resources/term_dictionary/term_leo.md), [ABRAM](../resources/term_dictionary/term_abram.md)

### BONES - Bootstrap Stack for CDK Pipelines
**Full Name**: BONES Bootstrap Stack
**Description**: CloudFormation stack in every AWS account/region that CDK pipelines deploy to. Contains **ECR repo, S3 bucket, KMS key, and IAM roles** for BARS replication, Pipelines invocation, change set approval, and Hydra testing. Created by DeploymentPipeline construct. Initial bootstrap requires manual `brazil-build bootstrap`.
**Documentation**: [BONES Term](../resources/term_dictionary/term_bones.md)
**Wiki**: https://docs.hub.amazon.dev/pipelines/cdk-guide/concepts-cdk-pipelines/
**Related**: [BATS](#bats---build-artifact-transform-service), [BARS](#bars---build-artifact-replication-service), [CloudFormation](#cloudformation---aws-infrastructure-as-code-service)

### PDG - Pipeline Deployment Groups
**Full Name**: Pipeline Deployment Groups
**Description**: Mechanism for deploying all BATS components from an aggregate transform as a **single pipeline target that succeeds or fails together**. Enables multi-stack deployment with dependency sequencing. CDK auto-infers dependencies from TypeScript constructor args. Scaffolding resources in us-west-2 are critical for both deployment and rollback.
**Documentation**: [PDG Term](../resources/term_dictionary/term_pdg.md)
**Wiki**: https://docs.hub.amazon.dev/docs/pipelines/user-guide/concepts-deployment-groups.html
**Related**: [BATS](#bats---build-artifact-transform-service), [BARS](#bars---build-artifact-replication-service), [BONES](#bones---bootstrap-stack)

### SageMaker
**Full Name**: Amazon SageMaker
**Description**: AWS's managed ML platform for training/deploying at scale - **primary BAP training infrastructure**. Flow: MODS → SageMaker Training → MIMS → AMES. Supports XGBoost, PyTorch, TensorFlow, custom containers. Endpoints: <100ms latency, auto-scaling. Cursus integration reduces 97% dev time.
**Documentation**: [SageMaker Term](../resources/term_dictionary/term_sagemaker.md)
**AWS Docs**: https://docs.aws.amazon.com/sagemaker/
**Portal**: https://aws.amazon.com/sagemaker/
**Python SDK**: https://sagemaker.readthedocs.io/
**BAP Wiki**: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Automation/MODS/
**Use Cases**: XGBoost abuse models, Deep Learning NLP (BSM), Hyperparameter Tuning, Cursus pipelines
**Key Resources**: Bindle (`BuyerAbuseMods`), Pipeline (https://pipelines.amazon.com/pipelines/BuyerAbuseMods ID: 5586005)
**Contacts**: BAP ML Team (rychardy@), CARML Model Oncall (carml-model)
**Status**: ✅ Active - primary training infrastructure for BAP ML models
**Related**: [SAIS](#sais---secure-ai-sandbox), [MODS](#mods---model-training-workflow-operation-and-development-system), [MIMS](#mims---model-inference-management-service), [AMES](#ames---active-model-execution-service), [DAWS](#daws---data-analytics-workflow-service), [Cursus](../resources/term_dictionary/term_cursus.md)

### UMLC - Unified Machine Learning Catalog
**Full Name**: Unified Machine Learning Catalog
**Description**: Central ML artifact repository - discover features, models, rules, datasheets and their lineage. 50K+ variables, 200K+ relations, 76.9% coverage. **ChatUMLC** reduces variable lineage from 2-3 days → 30 minutes. Portal: unified-ml-catalog.ctps.amazon.dev.
**Documentation**: [UMLC Term](../resources/term_dictionary/term_umlc.md)
**Wiki**: https://w.amazon.com/bin/view/CT/CoreServices/UnifiedMLCatalog
**Portal**: https://unified-ml-catalog.ctps.amazon.dev/
**AI Agent**: [ChatUMLC](../projects/project_chatumlc.md) - LLM-powered variable discovery
**Coverage**: 76.9%+ of CTPS ML artifacts
**Team**: Core Services (CMLS) - khashish@, Kay Kim, Yanbo Chen, Abhishek Joshi
**Related**: [SAIS](#sais---secure-ai-sandbox), [MODS](#mods---model-training-workflow-operation-and-development-system), [OTF](#otf---on-the-fly), [AMES](#ames---active-model-execution-service), [RMP](../resources/term_dictionary/term_rmp.md)

### LTRA - Long-Term Retention Architecture
**Full Name**: Long-Term Retention Architecture
**Description**: SPS-level framework for measuring and improving service resilience using a **0-260 point composite score** across alarm coverage, pipeline health, test coverage, and runbook documentation. Services are benchmarked by percentile rank. Designed to resist gaming through multi-dimensional scoring. SPS kingpin goal 972359 drives LTRA onboarding.
**Documentation**: [LTRA](../resources/term_dictionary/term_ltra.md)
**Related**: [URES](../resources/term_dictionary/term_ures.md), [Alarmathon](../resources/term_dictionary/term_alarmathon.md)

### MongoDB - Document-Oriented NoSQL Database
**Full Name**: MongoDB
**Description**: An open-source, document-oriented NoSQL database that stores data as flexible BSON (Binary JSON) documents. Unlike relational databases, MongoDB requires no predefined schema, allowing each document to have a different structure. **MongoDB is primarily a CP system in the CAP framework**, defaulting to strong consistency via single-primary replica sets. Supports multi-document ACID transactions since v4.0, horizontal scaling via sharding, and rich query/aggregation capabilities.
**Documentation**: [MongoDB](../resources/term_dictionary/term_mongodb.md)
**Related**: [DynamoDB](../resources/term_dictionary/term_ddb.md), [CAP Theorem](#cap-theorem---brewers-theorem), [SQL](../resources/term_dictionary/term_sql.md)

### MODS - Model Training Workflow Operation and Development System
**Full Name**: Model Training Workflow Operation and Development System
**Description**: ML model training workflow orchestration platform. Standardizes training workflows with reusable templates, version control, execution tracking, and automated deployment.
**Documentation**: [MODS Tool](../resources/tools/tool_mods.md) | **📊 [CMLS Tool Chain Analysis](../resources/analysis_thoughts/analysis_cmls_ml_tool_chain_integration.md)** | **📊 [ML Automation Comparison](../resources/analysis_thoughts/analysis_ml_automation_systems_comparison.md)**
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/MODS/
**Related**: [SAIS](../resources/term_dictionary/term_sais.md), [MDS](../resources/term_dictionary/term_mds.md), [MIMS](../resources/tools/tool_mims.md), [UMLC](#umlc---unified-machine-learning-catalog), [ML Pigeon](#ml-pigeon---ml-model-deployment-platform)

### MLOps - Machine Learning Operations
**Full Name**: Machine Learning Operations
**Description**: Practices combining machine learning, DevOps, and data engineering to deploy and maintain ML models in production reliably and efficiently. Covers the entire ML lifecycle: data preparation, model training, testing, deployment, monitoring, and retraining. **In BRP, MLOps infrastructure supports dozens of abuse detection models** across programs and marketplaces via automated retraining pipelines, RMP rule deployment, OTF feature engineering, and model performance monitoring.
**Documentation**: [MLOps Term](../resources/term_dictionary/term_mlops.md)
**Wiki**: [NintAI MLOps](https://w.amazon.com/bin/view/InTech/NintAI/Projects/MlOps/)
**Related**: [MODS](#mods---model-training-workflow-operation-and-development-system), [SageMaker](#sagemaker), [ML Pigeon](#ml-pigeon---ml-model-deployment-platform), [CI/CD](../resources/term_dictionary/term_ci_cd.md), [ML Automation](../resources/term_dictionary/term_ml_automation.md)

### ML Pigeon - ML Model Deployment Platform
**Full Name**: ML Pigeon
**Description**: **Red-certified** SageMaker wrapper for ML deployment with SE best practices. Operators: training, batch inference, deployment, tuning. 360+ teams. Portal: mlpigeon.selling-partners.amazon.dev. vs Excalibur: ML Pigeon is active, Excalibur is legacy maintenance.
**Portal**: https://mlpigeon.selling-partners.amazon.dev/
**Documentation**: [ML Pigeon Term](../resources/term_dictionary/term_ml_pigeon.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/MLPigeon/
**Workflow Wiki**: https://w.amazon.com/bin/view/MLPigeon/Workflow/
**Owner**: Core Services Fixed Team (BRP)
**MLForge Team**: ITA Data Reusable Services - ML Services Team
**Key Operators**: Training, Batch Inference, Model Deployment, Hyperparameter Tuning, Model Sharing
**Integration**: AMES, FORTRESS, MMS, OTF
**Security**: Red certified
**Support**: SEV 2 (weekly office hours)
**Status**: ✅ Active - primary ML model deployment platform for BRP
**Related**: [MODS](#mods---model-training-workflow-operation-and-development-system), [AMES](#ames---active-model-execution-service), [FORTRESS](#fortress---fraudulent-order-reduction-through-risk-evaluation-at-super-speed-legacy), [MMS](#mms---model-management-service), [SageMaker](#sagemaker)

### MIMS - Model Inference Management Service
**Full Name**: Model Inference Management Service
**Description**: Managed model deployment system that manages complete SageMaker Endpoints lifecycle including provisioning, load testing, scaling, monitoring, deletion, and lineage tracking.
**Documentation**: [MIMS Tool](../resources/tools/tool_mims.md) | **📊 [CMLS Tool Chain Analysis](../resources/analysis_thoughts/analysis_cmls_ml_tool_chain_integration.md)** | **📊 [ML Automation Comparison](../resources/analysis_thoughts/analysis_ml_automation_systems_comparison.md)**
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/MIMS/
**Related**: [MODS](../resources/tools/tool_mods.md), [URES](../resources/term_dictionary/term_ures.md), [AMES](../resources/term_dictionary/term_ames.md)

### MMS - Model Management Service
**Full Name**: Model Management Service
**Description**: **Control plane for AMES** - centralized model metadata and package storage. Aliases: ACTIVE (production), AUDIT (testing). 1,200+ models, 3,200 workflows. Flow: DAWS builds → MMS stores → AMES executes. Bindles access control since 2021.
**Documentation**: [MMS Term](../resources/term_dictionary/term_mms.md) | **📊 [CMLS Tool Chain Analysis](../resources/analysis_thoughts/analysis_cmls_ml_tool_chain_integration.md)**
**Wiki**: https://w.amazon.com/bin/view/ContinuousLearning/TRMSModelManagementService/
**Portal**: https://trms-data-analytics-na.amazon.com/ (UI), https://trms-mms-na.amazon.com/explorer/ (API)
**Owner**: CMLS (Core ML Services)
**Role**: Control plane for AMES (model metadata + packages)
**Aliases**: ACTIVE (production), AUDIT (testing)
**Scale**: 1,200+ models, 3,200 build workflows
**Access Control**: Bindles (since Jan 2021)
**Status**: ✅ Active - core model management infrastructure
**Related**: [AMES](#ames---active-model-execution-service), [DAWS](#daws---data-analytics-workflow-service), [MODS](#mods---model-training-workflow-operation-and-development-system), [UMLC](#umlc---unified-machine-learning-catalog), [PIPER](../resources/term_dictionary/term_piper.md), [ARROWEverywhere](../resources/term_dictionary/term_arrow_everywhere.md)

### DAWS - Data Analytics Workflow Service
**Full Name**: Data Analytics Workflow Service (TRMS Data Analytics Workflow Service)
**Description**: Template-based ML training with one-click model refresh (weeks → days). Supports XGBoost/RF via SageMaker, 18+ BAP models across US/EU5. Links offline training (MDS+OTF) to online deployment (AMES). Being supplemented by MODS.
**Documentation**: [DAWS Term](../resources/term_dictionary/term_daws.md) | **📊 [CMLS Tool Chain Analysis](../resources/analysis_thoughts/analysis_cmls_ml_tool_chain_integration.md)**
**Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/DAWS_AutoRefresh_Setup/
**Portal**: https://trms-data-analytics-na.amazon.com (NA), https://trms-data-analytics-eu.amazon.com (EU)
**Key Feature**: One-click model refresh with flexible tagging integration
**Status**: ✅ Active - primary ML training platform for buyer abuse models (legacy, being supplemented by MODS)
**Related**: [MODS](../resources/tools/tool_mods.md), [MDS](../resources/term_dictionary/term_mds.md), [OTF](../resources/term_dictionary/term_otf.md), [AMES](../resources/term_dictionary/term_ames.md), [RMP](../resources/term_dictionary/term_rmp.md)

### Dagster - Data Orchestration Platform
**Full Name**: Dagster
**Description**: Dagster is an open-source data orchestration platform that introduced the Software-Defined Assets (SDA) paradigm, where data assets are first-class citizens with automatic dependency inference from function signatures. **Its key innovation is implicit DAG construction from `@asset` function parameter names**, eliminating manual pipeline wiring. Dagster provides built-in asset lineage tracking, incremental materialization, and partitioned execution. It is the closest comparator to Cursus, sharing 3 of 5 innovations but optimizing for simplicity (1 file per asset) over richness (6 artifacts per tool).
**Documentation**: [Dagster](../resources/term_dictionary/term_dagster.md)
**Wiki**: https://docs.dagster.io/
**Related**: [Cursus](../resources/term_dictionary/term_cursus.md), [Apache Airflow](../resources/term_dictionary/term_airflow.md), [SageMaker](../resources/term_dictionary/term_sagemaker.md)

### DSP - TRMS Data Science Platform
**Full Name**: TRMS Data Science Platform
**Description**: Data science infrastructure and tools for TRMS teams. Provides standardized environment for data analysis, model development, and experimentation.
**Documentation**: [DSP Term](../resources/term_dictionary/term_dsp.md)
**Related**: [SAIS](../resources/term_dictionary/term_sais.md), [MODS](../resources/tools/tool_mods.md)

---

> **Note**: Data infrastructure entries (Andes, Redshift, MDS, Cradle, Datanet, EDX) are in [Data & Metrics Glossary](acronym_glossary_data_metrics.md#data-warehouses--storage)

---

## Workflow Orchestration Platform

### PDL - Process Definition Language
**Full Name**: Process Definition Language
**Description**: ORCA's native domain-specific language for workflow authoring with Java-like syntax. Built natively on Amazon ION data types and supports DAG modeling for complex multi-step workflows. **Provides the best developer experience among ORCA DSLs** with LSP-based IDE plugins, code generation from Smithy specifications, and Brazil-Build integration for compile-time validation. Also usable as in-line scripting within Herd XML graphs.
**Documentation**: [PDL](../resources/term_dictionary/term_pdl.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/language/process-definition-language
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [Herd](#herd---orca-execution-engine--xml-workflow-language), [SIL](#sil---service-integration-layer), [CDK](../resources/term_dictionary/term_cdk.md)

### Herd - ORCA Execution Engine & XML Workflow Language
**Full Name**: Herd (HerdEngine / HerdService)
**Description**: ORCA's original execution engine and XML-based workflow authoring language. As the runtime, it processes workflow definitions, manages state transitions, and coordinates service invocations across all ORCA DSLs. As a language, it provides graph-based state machine authoring with conditional transitions, fork-and-join parallelism, and subgraph composition. **Proven resiliency at Amazon scale handling tens of trillions of transactions per year.**
**Documentation**: [Herd](../resources/term_dictionary/term_herd.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/language/herd-xml
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [PDL](#pdl---process-definition-language), [SIL](#sil---service-integration-layer), [UVAS](#uvas---unified-visualization-analytics-and-search)

### SIL - Service Integration Layer
**Full Name**: Service Integration Layer
**Description**: ORCA's mechanism for hosting custom activity code that the workflow engine invokes during execution. Provides a standardized interface for registering, deploying, and invoking business activities within workflows. **Three deployment models: Local SIL (Docker on ECR, lowest latency), MAWS SIL (Managed AWS frameworks), and NAWS SIL (Native AWS).** Activities register with Herd for invocation and support CloudAuth, IAM, STS, and Bindle Brass authentication.
**Documentation**: [SIL](../resources/term_dictionary/term_sil.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/developer-guide/service-integrations/sil-integration
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [Herd](#herd---orca-execution-engine--xml-workflow-language), [PDL](#pdl---process-definition-language)

### SDO - Stores, Devices, and Other
**Full Name**: Stores, Devices, and Other (formerly CDO — Consumer, Digital, and Other, prior to Q3 2022)
**Description**: The non-AWS part of Amazon — one of the two top-level organizational divisions (Amazon = SDO + AWS). Encompasses Worldwide Amazon Stores (retail, operations, grocery, selling partners), Devices & Services (Kindle, Echo, Ring, AGI), and Other (Advertising, Prime Video, Twitch, cross-functional orgs). **SDO is the largest Enterprise customer for AWS** and the primary audience for Builder Tools (ASBX). Publishes the Golden Path recommending ORCA as the default workflow solution. SDO teams use Conduit-managed AWS accounts and operate on the Retail-Prod network fabric.
**Documentation**: [SDO](../resources/term_dictionary/term_sdo.md)
**Wiki**: https://w.amazon.com/bin/view/SDO/
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [MAWS](#maws---managed-aws), [NAWS](#naws---native-aws), [CDK](../resources/term_dictionary/term_cdk.md)

### UVAS - Unified Visualization, Analytics and Search
**Full Name**: Unified Visualization, Analytics and Search
**Description**: ORCA's comprehensive observability stack providing full visibility into workflow execution without log digging. Encompasses three query tiers: Workflow Index Query (pre-defined indexes), Elastic Query (1+ month, near real-time), and Lifecycle Query (1+ year, deep analytics). **Provides Hyper-process View for end-to-end visibility across different executions, teams, and environments**, reducing MTTR. Integrates with AXON for service map visibility.
**Documentation**: [UVAS](../resources/term_dictionary/term_uvas.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/developer-guide/search-and-analytics
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [Herd](#herd---orca-execution-engine--xml-workflow-language), [Carnaval](#carnaval---alarm-aggregation-system)

### MAWS - Managed AWS
**Full Name**: Managed AWS
**Description**: Amazon's internal managed cloud hosting environment with Amazon-specific management layers, CloudAuth authentication, and pre-configured compliance controls. Provides standardized tooling and operational support built on AWS primitives. **ORCA's multi-tenant cloud (ORCACloud) runs in MAWS**, and MAWS SIL hosts activity services within Coral and BSF frameworks. Supports SOX, HIPAA, GDPR, and DMA compliance out of the box.
**Documentation**: [MAWS](../resources/term_dictionary/term_maws.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/managed-hosting
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [NAWS](#naws---native-aws), [SIL](#sil---service-integration-layer), [CloudAuth](../resources/term_dictionary/term_cloudauth.md)

### NAWS - Native AWS
**Full Name**: Native AWS
**Description**: Amazon's internal hosting environment where teams manage their own AWS accounts directly using standard AWS services and IAM roles. Provides full control over AWS resources with access to the complete AWS service catalog. **ORCA Edge deploys in NAWS on ECS/EKS**, and NAWS SIL hosts activity services in native AWS. Uses IAM roles and STS for authentication, contrasting with MAWS's CloudAuth approach.
**Documentation**: [NAWS](../resources/term_dictionary/term_naws.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/developer-guide/service-integrations/authentication-and-authorization
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [MAWS](#maws---managed-aws), [ORCA Edge](#orca-edge---containerized-local-orchestration), [SIL](#sil---service-integration-layer)

### AXON - Cross-Runtime Process Visualization
**Full Name**: AXON
**Description**: Amazon's cross-runtime end-to-end process visualization system providing complete service maps with aggregated visibility of service call chains and service-level metrics. ORCA workflows register as a RouteType in AXON, enabling full service dependency graph visualization from the AXON console. **Spans beyond ORCA's execution boundary to show how workflows fit within the broader service ecosystem.** Complements UVAS by providing inter-service topology while UVAS shows intra-workflow execution details.
**Documentation**: [AXON](../resources/term_dictionary/term_axon.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/developer-guide/workflow-visualization/axon-integration
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [UVAS](#uvas---unified-visualization-analytics-and-search), [ORCA Studio](#orca-studio---workflow-portal)

### ORCA Edge - Containerized Local Orchestration
**Full Name**: ORCA Edge (OrcaEdge)
**Description**: Containerized lightweight ORCA stack deployed locally as an OCI-compliant Docker container for ultra-low latency orchestration. Executes entirely in-memory with no persistent storage, eliminating external network latency and ORCACloud dependency. **Achieves 3ms eligible-to-processing delay with >50% latency reduction vs ORCACloud.** Deploys on ECS, EKS, Kubernetes, or Docker-compose. Connects to ORCACloud for centralized definition management and execution history via UVAS.
**Documentation**: [ORCA Edge](../resources/term_dictionary/term_orca_edge.md)
**Wiki**: https://console.harmony.a2z.com/orca-docs/workflows/managed-hosting/orca-edge/overview
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [NAWS](#naws---native-aws), [UVAS](#uvas---unified-visualization-analytics-and-search), [ECR](../resources/term_dictionary/term_ecr.md)

### ORCA Studio - Workflow Portal
**Full Name**: ORCA Studio
**Description**: ORCA's browser-based one-stop portal for workflow authoring, deployment, execution, debugging, and analytics. Provides unified web interface for all ORCA-managed workflows with Graph View, Timeline View, Latency View, and Execution Explorer. **Integrates UVAS query capabilities, AXON service maps, and Visual Workflow Designer (OVWD) for low-code authoring.** Supports batch re-drive of failed workflows and includes a Pricing Estimator for cost planning.
**Documentation**: [ORCA Studio](../resources/term_dictionary/term_orca_studio.md)
**Wiki**: https://beta.us-west-2.studio.orca.amazon.dev/
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [UVAS](#uvas---unified-visualization-analytics-and-search), [AXON](#axon---cross-runtime-process-visualization)

### Definition Deployer - ORCA Definition Deployer CDK Construct
**Full Name**: ORCA Definition Deployer
**Description**: CDK construct provided by the ORCA team that deploys workflow definitions from a Brazil package to the ORCA runtime. Integrates with Amazon Pipelines for automated CI/CD with staged rollout across regions. **Recommended deployment method per the BuilderHub Golden Path for Workflow Orchestration (SDO).** Also provides a Local Definition Deployer variant for rapid development iteration from a Brazil workspace or Cloud Desktop.
**Documentation**: [Definition Deployer](../resources/term_dictionary/term_definition_deployer)
**Wiki**: https://console.harmony.a2z.com/orca-docs/developer-guide/deployment/definition-deployer
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [CDK](../resources/term_dictionary/term_cdk.md), [LCAP](#lcap---low-code-application-platform)

### LCAP - Low Code Application Platform
**Full Name**: Low Code Application Platform
**Description**: ORCA's solution for enabling non-technical users to build workflow definitions through a visual drag-and-drop interface without writing code. Delivers the ORCA Visual Workflow Designer (OVWD) as its primary authoring surface. **Reduces TCO and TTM by allowing SMEs, Automation Experts, and Research Analysts to compose workflows from pre-built native and business components.** Visual workflows are transpiled into Herd XML for execution on the ORCA runtime.
**Documentation**: [LCAP](../resources/term_dictionary/term_lcap)
**Wiki**: https://w.amazon.com/bin/view/Orchestration/ORCA/LCAP/
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [OVWD](#ovwd---orca-visual-workflow-designer), [Herd](#herd---orca-execution-engine--xml-workflow-language)

### OVWD - ORCA Visual Workflow Designer
**Full Name**: ORCA Visual Workflow Designer
**Description**: Drag-and-drop, click-and-configure user interface delivered by ORCA's Low Code Application Platform (LCAP). Enables non-technical users to author workflow definitions visually by composing pre-built components on a canvas. **Visual workflows are transpiled into Herd XML definitions that are functionally equivalent to hand-written code.** Hosted within ORCA Studio with change control integration via Barrister Service.
**Documentation**: [OVWD](../resources/term_dictionary/term_ovwd)
**Wiki**: https://w.amazon.com/bin/view/Orchestration/ORCA/LCAP/
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [LCAP](#lcap---low-code-application-platform), [ORCA Studio](#orca-studio---workflow-portal)

---

## Knowledge Graph & Advanced ML

### Nexus
**Full Name**: Nexus - Unified Risk Knowledge Graph Platform
**Description**: Unified Knowledge Graph for risk detection - combines lifecycle events, behavioral patterns, multi-modal signals. Addresses **Non-Linked MAA** ($401M/61% of total). Built on Neptune + GraphStorm + GENIE. AskNexus provides Graph-RAG GenAI interface. Launch: UK P0 (2025).
**Documentation**: [Nexus Term](../resources/term_dictionary/term_nexus.md) | [Nexus Area](../areas/area_nexus.md)
**Quip**: [Nexus Folder](https://quip-amazon.com/rXxbO0X2ucjR/Nexus) | [2025 ML Roadmap](https://quip-amazon.com/JVC9AA5SXsx) | [Tech Strategy](https://quip-amazon.com/GQX9AAbq5dd)
**Key Technologies**: AWS Neptune (graph database), GraphStorm (GNN training), GENIE (data ingestion), HGT/RGCN models (node classification), AskNexus (Graph-RAG GenAI interface), MO Slipbox (temporal MO tracking)
**Use Cases**: PFOC order risk scoring (80%+ precision target), CAP routing enhancement, MO detection/prevention, knowledge discovery, Tattletale 2.0 integration
**Architecture**: Three-layer (Gathering/Multi-Modal Processing → KG Preparation/Governance → Computation/Application), 4.7B+ nodes, 2.2B+ edges
**Launch Status**: UK P0 (2025), EU5 expansion (2025), worldwide (2026+)
**Related**: [AskNexus](#asknexus), [Tattletale](../resources/term_dictionary/term_tattletale.md), [MAA](../resources/term_dictionary/term_maa.md), [GraphStorm](#graphstorm), [Neptune](#neptune)

### ExGQL - Experience-enhanced NL-to-nGQL Translation
**Full Name**: Experience-enhanced NL-to-nGQL Translation
**Description**: An agentic framework that translates natural language queries into executable NebulaGraph queries (nGQL) through a 7-step pipeline (Schema Grounding → Intent Parsing → Traversal Planning → Constraint Synthesis → Query Synthesis → Validation → Execution & Refinement). **Maintains a persistent Skillbook of reusable patterns that grows with each interaction**, operating as a generator–reflector–curator loop. Powers both the NebulaGraph migration (>90% query parity) and AskNexus's natural language interface.
**Documentation**: [ExGQL Term](../resources/term_dictionary/term_exgql.md)
**Related**: [Nexus](../resources/term_dictionary/term_nexus.md), [NebulaGraph](../resources/term_dictionary/term_nebulagraph.md), [AskNexus](../resources/term_dictionary/term_asknexus.md)

### KG Quality Framework
**Full Name**: Knowledge Graph Quality Evaluation Framework
**Description**: A modular 4-level validation system for assessing knowledge graph integrity across database engines. **Levels: Schema Governance → Knowledge Completeness → Outlier Detection → Traversal Integrity.** Uses a common connector interface supporting Neptune and NebulaGraph for migration parity testing. Catches issues from schema violations to subtle multi-hop traversal data corruption.
**Documentation**: [KG Quality Framework Term](../resources/term_dictionary/term_kg_quality_framework.md)
**Related**: [Nexus](../resources/term_dictionary/term_nexus.md), [NebulaGraph](../resources/term_dictionary/term_nebulagraph.md), [ExGQL](#exgql---experience-enhanced-nl-to-ngql-translation)

### Ontology Pipeline
**Full Name**: LLM-guided Ontology Proposal Pipeline
**Description**: An automated system that takes raw data sources and proposes multiple candidate KG schemas modeling the data from different angles. **LLM analyzes data characteristics and proposes N schema candidates; all runtime extraction is deterministic and auditable with no LLM in the loop.** Generates complete implementation artifacts: schema definition (JSON), loader code, and extractor code for each candidate.
**Documentation**: [Ontology Pipeline Term](../resources/term_dictionary/term_ontology_pipeline.md)
**Related**: [Nexus](../resources/term_dictionary/term_nexus.md), [KG Quality Framework](#kg-quality-framework), [Knowledge Graph](../resources/term_dictionary/term_knowledge_graph.md)

### GraphStorm
**Full Name**: GraphStorm - Distributed Graph Neural Network Training Framework
**Description**: AWS's open-source enterprise graph machine learning framework developed jointly by AWS Graph ML, Search M5, and Amazon Neptune for industry-scale graph data processing and model training on graphs with billions of nodes and edges. Provides comprehensive model zoo including RGCN, RGAT, HGT, and GraphSAGE with distributed multi-GPU training capabilities across clusters, supporting fraud detection, search optimization, and recommendation systems. Delivers significant business impact including $89MM revenue in SP Ads Sourcing, $13MM cost savings in fraud detection, and $515MM OPS in Search ranking through advanced graph neural network applications. Framework enables both self-service mode for independent team usage and white-glove collaborative development with dedicated GraphStorm team resources for complex enterprise deployments.
**Documentation**: [GraphStorm Term](../resources/term_dictionary/term_graphstorm.md)
**GitHub**: https://github.com/awslabs/graphstorm
**Wiki**: [AWS-M5 GraphStorm Framework](https://w.amazon.com/bin/view/AWS/AmazonAI/AIRE/GSF/)
**Key Features**: Distributed training, multi-task learning, comprehensive model zoo, AWS integration, open-source availability
**Business Impact**: $89MM revenue (SP Ads), $13MM savings (fraud detection), $515MM OPS (search ranking)
**Collaboration**: Self-service mode (onboarding support) + White-glove mode (joint development)
**Applications**: Fraud detection, search optimization, recommendation systems, traffic quality, product quality
**Status**: ✅ Active - primary distributed GNN training platform for Amazon
**Related**: [Nexus](#nexus), [SageMaker](#sagemaker), [Neptune](#neptune), [MODS](#mods---model-training-workflow-operation-and-development-system), [GraMS](#grams)

### CFM - Chargeback Fraud Model
**Full Name**: Chargeback Fraud Model
**Description**: Payment Risk ML model predicting fraudulent chargeback likelihood. **Scores used in pre-fulfillment evaluation** for high-risk order cancellation. Works alongside 3DS and iRisk in payment fraud prevention.
**Documentation**: [CFM Term](../resources/term_dictionary/term_cfm.md)
**Related**: [DeepCare](../resources/term_dictionary/term_deepcare.md), [PFOC](../resources/term_dictionary/term_pfoc.md)

### 3DS - 3D Secure
**Full Name**: 3D Secure
**Description**: Payment authentication protocol adding extra verification during online card transactions. **Shifts chargeback liability from Amazon to card issuer** for authenticated transactions. Required by SCA in EU/UK; V2.0 supports frictionless flow for low-risk transactions.
**Documentation**: [3DS Term](../resources/term_dictionary/term_3ds.md)
**Related**: [CFM](../resources/term_dictionary/term_cfm.md), [PFW](../resources/term_dictionary/term_pfw.md)

### CMLS - Core ML Services
**Full Name**: Core ML Services / Centralized ML Service
**Description**: ML platform providing centralized infrastructure for model training, deployment, and serving. **Requires ASR certification for GenAI workloads.** Part of broader ML ecosystem alongside MODS, MIMS, SAIS.
**Documentation**: [CMLS Term](../resources/term_dictionary/term_cmls.md)

### TREX - TRMS Redshift Extract
**Full Name**: TRMS Redshift Extract
**Description**: Data extraction system within TRMS ecosystem providing Redshift-based data for ML training, investigation, and analytics. **Accesses FC grading signals, enforcement data, and investigation records.**
**Documentation**: [TREX Term](../resources/term_dictionary/term_trex.md)

### GACD - Global Automatic Call Distributor
**Full Name**: Global Automatic Call Distributor
**Description**: Amazon's custom-built contact routing system for phone calls, chats, emails, and work items across 80+ business units. **Powers CS call center operations for 15+ years**; routes contacts to specialized skills like CAP. Being migrated to Amazon Connect (hybrid).
**Documentation**: [GACD Term](../resources/term_dictionary/term_gacd.md)
**Wiki**: https://w.amazon.com/bin/view/Contact_Routing_Administrators/Support_Services/GACD/
**Related**: [CAP](../resources/term_dictionary/term_cap.md), [AC3](../resources/term_dictionary/term_ac3.md)

### Nile - Document Clustering Service
**Full Name**: Nile (Document Clustering Service)
**Description**: CandyLand/Identity service that detects forged documents during seller registration by performing exact-duplicate (MD5 hash) and near-duplicate (visual embedding similarity) detection on ID, financial, and business documents. **Uses AWS OpenSearch for feature storage and real-time similarity queries**, clustering sellers who submit the same or similar forged templates. High-confidence clusters are auto-declined at registration, reducing SIV/KYC investigation volume.
**Documentation**: [Nile Term](../resources/term_dictionary/term_nile.md)
**Wiki**: https://w.amazon.com/bin/view/SellerRegistrationVerification/CandyLand/Identity/Nile/
**Related**: [IDV](../resources/term_dictionary/term_idv.md), [KYC](../resources/term_dictionary/term_kyc.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md)

### NoSQL - Not Only SQL
**Full Name**: Not Only SQL
**Description**: An umbrella term for database systems that use non-relational data models — key-value (DynamoDB), document (MongoDB), column-family (Cassandra), and graph (Neptune). NoSQL databases trade relational guarantees like joins and full ACID for horizontal scalability, schema flexibility, and low-latency access. **Most NoSQL systems follow BASE (Basically Available, Soft state, Eventually consistent) rather than ACID**, and explicitly navigate CAP trade-offs. Widely used for feature stores, real-time serving, and high-velocity data ingestion.
**Documentation**: [NoSQL](../resources/term_dictionary/term_nosql.md)
**Related**: [MongoDB](#mongodb---document-oriented-nosql-database), [DynamoDB](../resources/term_dictionary/term_ddb.md), [CAP Theorem](#cap-theorem---brewers-theorem)

### Neptune
**Full Name**: AWS Neptune - Managed Graph Database
**Description**: Managed graph database for GraMS powering real-time GNN inference. **COSA** (first online TGN at Amazon, Mar 2023): +13% BAA detection, +9% CB savings, billion+ nodes, 2K TPS. Catches 25%+ intra-day fraud that batch methods miss.
**Documentation**: [Neptune Term](../resources/term_dictionary/term_neptune.md)
**Wiki**: [GraMS](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/), [CoRe User Guide](https://w.amazon.com/bin/view/Ohio/COreRElations/UserGuide/), [COSA Announcement](https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/COSA-FR-announcement/)
**Query Languages**: Gremlin (primary at BRP), OpenCypher, SPARQL (RDF)
**BRP System**: GraMS (Graph Modeling System) - use-case specific Neptune databases
**MVP Deployment**: COSA - first online TGN at Amazon (March 15, 2023)
**Scale**: Billion+ nodes, 2,000 TPS writes, 1,800 TPS reads
**Key Innovation**: Real-time GNN inference vs batch (catches intra-day fraud)
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Design Inspector**: https://design-inspector.a2z.com/?#IGraMS
**Status**: ✅ Active - core infrastructure for GraMS/COSA
**Related**: [Nexus](#nexus), [GENIE](#genie), [GraphStorm](#graphstorm), [GraMS](../resources/term_dictionary/term_grams.md), [COSA](../resources/term_dictionary/term_cosa.md), [TGN](../resources/term_dictionary/term_tgn.md), [CoRe](../resources/teams/team_core.md)

### Gremlin
**Full Name**: Gremlin - Graph Traversal Language (Apache TinkerPop)
**Description**: Graph traversal query language for Neptune property graphs. Relationship-first queries with multi-hop traversal efficiency. Used by GraMS/COSA for real-time GNN inference. SLA: 2s timeout, P99 <750ms, 2K TPS.
**Documentation**: [Gremlin Term](../resources/term_dictionary/term_gremlin.md)
**External Docs**: [Apache TinkerPop](http://tinkerpop.apache.org/docs/current/), [Practical Gremlin Book](http://kelvinlawrence.net/book/Gremlin-Graph-Guide.html)
**AWS Docs**: [Neptune Gremlin](https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-gremlin.html), [Neptune Differences](https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-gremlin-differences.html)
**GraMS Wiki**: https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/
**Type**: Graph traversal query language
**Framework**: Apache TinkerPop
**Database**: Amazon Neptune (primary at BRP)
**Graph Model**: Property Graph (vertices, edges, properties)
**BRP Usage**: GraMS, COSA, graph-based abuse detection
**Key Strength**: Multi-hop relationship traversal, relationship-first queries
**SLA (GraMS)**: 2s query timeout, P99 <750ms
**Alternative**: SPARQL (RDF graphs - limited use at BRP)
**Status**: ✅ Active - primary graph query language for BRP
**Related**: [Neptune](#neptune), [GraMS](#grams), [COSA](../resources/term_dictionary/term_cosa.md), [GENIE](#genie), [ACIS](#acis---account-clustering-insight-service), [TGN](../resources/term_dictionary/term_tgn.md)

### GraMS
**Full Name**: GraMS - Graph Modeling System
**Description**: CoRe's online graph model deployment solution. Connects SageMaker models to Neptune graphs via GENIE. **COSA MVP** (Mar 2023): first online TGN, +13% BAA, +9% CB savings. Catches 25%+ intra-day fraud that batch missed. Scale: 2K TPS, billion+ nodes.
**Documentation**: [GraMS Term](../resources/term_dictionary/term_grams.md)
**Wiki**: [GraMS Main](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/), [WBR Dashboard](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/GraMS/Dashboards/WBRDashboard/)
**Design Inspector**: [GraMS](https://design-inspector.a2z.com/?#IGraMS), [COSA](https://design-inspector.a2z.com/#ICoRe-COSA)
**COSA Announcement**: https://w.amazon.com/bin/view/PaymentRisk/MachineLearning/Teams/AUSAIN/OSA/COSA-FR-announcement/
**MVP**: COSA - first online TGN at Amazon (March 15, 2023)
**Graph Storage**: Amazon Neptune
**Model Hosting**: Amazon SageMaker
**Data Preparation**: GENIE (future), CREL (current)
**Key Innovation**: Real-time graph inference vs daily batch
**Impact**: +13% BAA detection, +9% CB savings, 18-day lead time
**Scale**: 2,000 TPS writes (NA), 1,800 TPS reads
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Status**: ✅ Active - Year 2 roadmap (offline experimentation, ad-hoc analytics)
**Related**: [Neptune](#neptune), [GENIE](#genie), [COSA](../resources/term_dictionary/term_cosa.md), [TGN](../resources/term_dictionary/term_tgn.md), [ACIS](#acis---account-clustering-insight-service), [CoRe](../resources/teams/team_core.md)

### GENIE
**Full Name**: GENIE - Graph prEparatioN servIcE
**Description**: CoRe's graph preparation solution - transforms authoritative data into normalized graphs for GraMS/ACIS/OACIS. Supports organic (CC, IP, device) and synthetic signals (fuzzy-matched, behavioral). Replaces CREL/ORAS/Graphene. Self-service onboarding to Graph Universes.
**Documentation**: [GENIE Term](../resources/term_dictionary/term_genie.md)
**Wiki**: [GENIE Main](https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/), [HLD Design](https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Design/HLD/), [Datalake Design](https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/Design/Datalake/)
**Onboarding**: [Signal Onboarding](https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/SignalOnboarding), [GU Onboarding](https://w.amazon.com/bin/view/Ohio/COreRElations/GENIE/GUOnboarding)
**5 Min Intro**: https://broadcast.amazon.com/embed/1354726
**Key Features**: Self-service signal catalog, Graph Universe creation, synthetic signal support, BYOD, Andes 3.0 datalake
**Replaces**: CREL, ORAS, Graphene (legacy)
**Output**: Graph Universes (GU) for GraMS, ACIS, OACIS, EV 2.0
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Status**: ✅ Active development - singular graph preparation solution for SPS
**Related**: [Nexus](#nexus), [Neptune](#neptune), [GraMS](../resources/term_dictionary/term_grams.md), [COSA](../resources/term_dictionary/term_cosa.md), [ACIS](#acis---account-clustering-insight-service), [Graphene](../resources/term_dictionary/term_graphene.md), [CoRe](../resources/teams/team_core.md)

---

## Risk Evaluation Platform (GMRA Architecture)

### FD - Fraud Document  
**Full Name**: Fraud Document
**Description**: Comprehensive data structure containing all order-related information used in URES risk evaluations. Includes order details, customer context, payment data, and metadata for abuse detection. Originally persisted by FDPS (deprecated 2025), now moving toward direct order source architecture. Enables variable computation for 32,000+ features in risk evaluation workflows.
**Documentation**: [FD Term](../resources/term_dictionary/term_fd.md)
**Wiki**: https://w.amazon.com/bin/view/URES/FraudDocument/
**Related**: [FDPS](../resources/term_dictionary/term_fdps.md), [URES](#ures---unified-risk-evaluation-system), [OTF](#otf---on-the-fly), [VCS](../resources/term_dictionary/term_vcs.md), [DWAR](#dwar---deferred-write-ahead-request)

### URES - Unified Risk Evaluation System
**Full Name**: Unified Risk Evaluation System
**Description**: Amazon's unified and extensible platform for multi-tenant, scalable, low-latency, high-availability risk evaluation. Central orchestration layer that integrates OTF, AMES, and RMP using GMRA paradigm.
**Documentation**: [URES Term](../resources/term_dictionary/term_ures.md)
**Docs**: https://docs.ctps.amazon.dev/ures/index.html
**Related**: [GMRA](../resources/term_dictionary/term_gmra.md), [OTF](../resources/term_dictionary/term_otf.md), [AMES](../resources/term_dictionary/term_ames.md)

### OLAP - Online Analytical Processing
**Full Name**: Online Analytical Processing
**Description**: Category of data processing technology enabling rapid analysis of multi-dimensional information from multiple perspectives, supporting complex analytical queries and business intelligence operations. In Amazon's buyer risk prevention ecosystem, OLAP is primarily represented through REOLAPS providing historical transaction data for risk evaluation testing and model validation. Critical foundation for ARROW Everywhere's automated rule calibration through offline simulation capabilities, enabling production-parity testing using millions of historical transactions. Supports sophisticated backtesting and rule optimization workflows essential for data-driven risk evaluation decisions.
**Documentation**: [OLAP Term](../resources/term_dictionary/term_olap.md)
**Wiki**: https://w.amazon.com/bin/view/URES/
**Related**: [REOLAPS](#reolaps---risk-evaluation-olap-system), [URES](#ures---unified-risk-evaluation-system), [MDS](../resources/term_dictionary/term_mds.md), [Redshift](../resources/term_dictionary/term_redshift.md), [LEX](../resources/term_dictionary/term_lex.md)

### REOLAPS - Risk Evaluation OLAP System
**Full Name**: Risk Evaluation OLAP System
**Description**: Amazon's specialized OLAP system designed specifically for risk evaluation and buyer abuse prevention workflows, providing historical transaction data storage and analytical capabilities for comprehensive backtesting and automated rule calibration. Critical enabler for ARROW Everywhere's automated threshold calibration, supplying millions of historical transactions through LEX offline simulation to ensure production-parity testing across all risk evaluation stages. Supports sophisticated multi-dimensional analysis across customer, order, and temporal dimensions, facilitating data-driven optimization and pattern discovery essential for effective fraud prevention. Bridges historical analysis with automated rule management systems, enabling Amazon's shift toward data-driven risk evaluation optimization.
**Documentation**: [REOLAPS Term](../resources/term_dictionary/term_reolaps.md)
**Wiki**: https://w.amazon.com/bin/view/URES/
**Related**: [URES](#ures---unified-risk-evaluation-system), [LEX](../resources/term_dictionary/term_lex.md), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md), [GMRA](#gmra---gathermodelruleact), [OLAP](#olap---online-analytical-processing)

### DPAC - Detect/Plan/Act/Close the Loop
**Full Name**: Detect → Plan → Act → Close the Loop
**Description**: Foundational **mental model** for Amazon's **Action Taking System (ATS)** defining four phases of unified risk evaluation and enforcement. **Phases**: (1) **Detect** - Human (ARI/Nautilus) or machine (URES) evaluation generates Evaluation Decision with risk level (confirmed risky/not risky/unconfirmed); (2) **Plan** - Action Planner matches Evaluation Decision to Decision Policy (WHY/WHAT/HOW) via Decision Policy Store (DPS), produces Decision Outcome with capabilities/workflows; (3) **Act** - Action Coordinator delegates to Capability Manager (ACDC) for graduated restrictions (SecureDelivery, PreventPhysicalOrders) and Workflow Manager for state changes (cancel orders, suppress listings), persists to Action History Store (AHS); (4) **Close the Loop** - Communication layer notifies customer (what changed, why, how to remediate), captures feedback to confirm/disconfirm risk prediction. **Key Interfaces**: Evaluation Decision (separates detecting from planning), Decision Policy (policy-driven configuration), Decision Outcome (actionable specification). **vs GMRA**: DPAC is enforcement framework (what happens AFTER risk identified); GMRA is evaluation framework (HOW risk is identified). **Benefits**: Policy-driven (DPC self-service), graduated enforcement, standardized communication, systematic feedback loop, centralized auditability (AHS).
**Documentation**: [DPAC Term](../resources/term_dictionary/term_dpac.md)
**Primary Reference**: [ATS Quick Start Guide](https://quip-amazon.com/iPkaA1FKT1YZ/ATS-Quick-Start-Guide)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Four Phases**: Detect (URES/Nautilus) → Plan (DPS/DPC) → Act (ACDC/Workflow) → Close the Loop (CSSW/AHD)
**Key Components**: Decision Policy Store (DPS), Decision Policy Commander (DPC), Action Coordinator, Capability Manager (ACDC), Workflow Manager, Action History Store (AHS)
**vs GMRA**: DPAC = enforcement (post-evaluation); GMRA = evaluation (risk identification)
**Owner**: SPS Actions Program, CTPS
**Status**: ✅ Active - core mental model for ATS unified enforcement
**Related**: [ATS](#ats---action-taking-system), [GMRA](#gmra---gathermodelruleact), [URES](#ures---unified-risk-evaluation-system), [CSSW](../resources/term_dictionary/term_cssw.md), [ACDC](../resources/term_dictionary/term_acdc.md)

### ATS - Action Taking System
**Full Name**: Action Taking System
**Description**: SPS's **unified and policy-driven enforcement pipeline** implementing the **DPAC** mental model (**Detect → Plan → Act → Close the Loop**) to provide consistent, graduated enforcement across buyer, seller, and brand risk programs. Addresses fragmented enforcement systems by enabling policy-driven configuration via Decision Policy Commander (DPC). **DPAC Flow**: (1) **Detect** - URES/Nautilus generates Evaluation Decision from lifecycle events; (2) **Plan** - Action Planner matches Decision Policy → Decision Outcome with capabilities/workflows; (3) **Act** - Action Coordinator delegates to Capability Manager (ACDC) and Workflow Manager; (4) **Close the Loop** - Customer notified via ENDR/CSSW with what changed, why, and remediation path. **Key Primitives**: Evaluation Decision (risk level from human/machine), Decision Policy (WHY/WHAT/HOW defined by RPOs), Decision Outcome (actions to execute). **Subsystems**: Action Catalog (workflow registry), Decision Policy Store (DPS), Action History Store (AHS), Capability Manager (ACDC), Workflow Manager.
**Documentation**: [ATS Term](../resources/term_dictionary/term_ats.md)
**Quick Start Guide**: [ATS Quick Start Guide](https://quip-amazon.com/iPkaA1FKT1YZ/ATS-Quick-Start-Guide) - **Primary Reference**
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Mental Model**: DPAC - Detect → Plan → Act → Close the Loop
**Key Primitives**: Evaluation Decision, Decision Policy, Decision Outcome
**Buyer Abuse Capabilities**: `SecureDelivery`, `PreventPhysicalOrders`, `PreventConcessions`, `RequireIDVerification`
**Key Innovation**: Granular capability control - restrict physical orders while preserving digital access
**Plan Components**: Action Planner, Decision Policy Store (DPS), Decision Policy Commander (DPC)
**Act Components**: Action Coordinator, Capability Manager (ACDC), Workflow Manager, Action History Store (AHS)
**Close Loop**: ENDR, Abbot, AHD, CSSW - communicate what/why/remediation
**Owner**: SPS Actions Program (vision), CTPS (platform infrastructure)
**Status**: ✅ Strategic - unified enforcement pipeline for SPS
**Related**: [URES](#ures---unified-risk-evaluation-system), [CARDS](../resources/term_dictionary/term_cards.md), [TOP](../resources/term_dictionary/term_top.md), [APWS](../resources/term_dictionary/term_apws.md), [FAPS](#faps---fraud-action-persistence-service), [ARI](../resources/term_dictionary/term_ari.md), [CAP](../resources/term_dictionary/term_cap.md), [Nautilus](../resources/term_dictionary/term_nautilus.md)

### ACDC - Capability Manager (Action Taking System)
**Full Name**: Capability Manager
**Description**: Component within ATS (Action Taking System) responsible for executing **graduated restrictions** on customer accounts during the "Act" phase of the DPAC enforcement framework. Manages fine-grained capability controls (SecureDelivery, PreventPhysicalOrders, PreventConcessions) that allow restricting specific account functions without full account closure. Enables proportional enforcement matching severity and type of detected abuse.
**Documentation**: [ACDC Term](../resources/term_dictionary/term_acdc.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Related**: [ATS](../resources/term_dictionary/term_ats.md), [DPAC](../resources/term_dictionary/term_dpac.md), [FAPS](../resources/term_dictionary/term_faps.md)

### AHS - Action History Store
**Full Name**: Action History Store
**Description**: Centralized persistence store within ATS for recording Decision Outcomes and the state of capabilities and state changes coordinated by the Action Coordinator. Provides a **single logical repository** of all enforcement actions across target types, queryable by Decision Policy. Tracks current state (pending, complete, waiting, in retry) and whether enforcement is active or suppressed via remediation/appeal. Communication layer subscribes to AHS completion events for customer notifications.
**Documentation**: [AHS Term](../resources/term_dictionary/term_ahs.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Related**: [ATS](../resources/term_dictionary/term_ats.md), [DPS](../resources/term_dictionary/term_dps.md), [ACDC](../resources/term_dictionary/term_acdc.md)

### DPC - Decision Policy Commander
**Full Name**: Decision Policy Commander
**Description**: Management UI built on top of the Decision Policy Store (DPS) within ATS. Enables Risk Policy Owners (RPOs) to **create and update enforcement policies without engineering dependency**. Provides a module for viewing and comparing risk policies across programs, enabling policy bar raisers to apply governance. RPOs define inputs, capabilities, workflows, conditional logic, and remediation paths through DPC.
**Documentation**: [DPC Term](../resources/term_dictionary/term_dpc.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Related**: [DPS](../resources/term_dictionary/term_dps.md), [ATS](../resources/term_dictionary/term_ats.md), [RPO](../resources/term_dictionary/term_rpo.md)

### DPS - Decision Policy Store
**Full Name**: Decision Policy Store
**Description**: Centralized persistence layer within ATS serving as the repository for managing Decision Policies. RPOs create, read, update, and archive policies via DPC. Specifications are consumed by the Action Planner which materializes them into Decision Outcomes. **Interoperable interface** — any ATS integrated with the Action Catalog can consume DPS policies. Also consulted by the communication layer for notification media/assets and channel types.
**Documentation**: [DPS Term](../resources/term_dictionary/term_dps.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Related**: [DPC](../resources/term_dictionary/term_dpc.md), [ATS](../resources/term_dictionary/term_ats.md), [AHS](../resources/term_dictionary/term_ahs.md)

### RPO - Risk Policy Owner
**Full Name**: Risk Policy Owner
**Description**: Role within ATS responsible for defining and managing Decision Policies that govern enforcement actions. RPOs use DPC to configure specifications defining what capabilities/workflows are available, why treatments are applied (conditional logic), and how customers can remediate. **Operates without engineering dependency** — configures enforcement through the DPC UI. Each risk program (DNR, MDR, FLR) has designated RPOs.
**Documentation**: [RPO Term](../resources/term_dictionary/term_rpo.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/Initiatives/2020/Actions3YAP/
**Related**: [DPC](../resources/term_dictionary/term_dpc.md), [DPS](../resources/term_dictionary/term_dps.md), [ATS](../resources/term_dictionary/term_ats.md)

### DRS - DisputeRulerService
**Full Name**: DisputeRulerService
**Description**: Rules engine in the A-to-Z claim processing pipeline, sitting in the Rules stage of the AtoZ GMRA pipeline. DRS gathers facts via VCL/OTF, retrieves model scores via HealBeamService, and applies policy/heuristic rules to determine claim outcomes. **Operates independently from URES** — AtoZ has its own evaluation pipeline. Works alongside DisputeExecutorService (DES) for orchestration and DBS for action execution.
**Documentation**: [DRS Term](../resources/term_dictionary/term_drs.md)
**Related**: [GMRA](#gmra---gathermodelruleact), [OTF](#otf---on-the-fly), [A-to-Z Claim](../resources/term_dictionary/term_atoz_claim.md), [AtoZ Eval](../resources/term_dictionary/term_atoz_eval.md)


### DBS - DisputeBusinessService
**Full Name**: DisputeBusinessService
**Description**: Core business logic service for A-to-Z Guarantee claim processing within SPS. DBS owns the **claim state machine**, defining status transitions (PEND → INVG → GRNT/NOGR/SRFD/BWDR/PLGR/PLNG) and mapping evaluation close reasons to terminal claim states via `ClaimHelper.java`. DisputeExecutorService (DES) delegates to DBS for all claim business logic including initialization, state transitions, and re-evaluation workflows.
**Documentation**: [DBS Term](../resources/term_dictionary/term_dbs.md)
**Source**: [DisputeBusinessService](https://code.amazon.com/packages/DisputeBusinessService)
**Related**: [A-to-Z Claim](../resources/term_dictionary/term_atoz_claim.md), [ATS](#ats---action-taking-system), [SAFE-T](../resources/term_dictionary/term_safe_t.md)

### GMRA - Gather/Model/Rule/Act
**Full Name**: Gather/Model/Rule/Act
**Description**: Evaluation paradigm and configuration framework used by URES to define how risk evaluations are performed.

### Holdout Analysis - False Positive Measurement via Account Closure Holdout
**Full Name**: Holdout Analysis (Hold Out Analysis)
**Description**: Measurement methodology that quantifies false positive account closures by holding out a random 10% sample of closures and observing customer behavior over a 90-day period. Implemented by AbuseHoldOutAnalyzerLambda, the first Native AWS Coral Service owned by Abuse. **Currently a manual observation process separate from ARI**, with the goal of automating observation and classification. Holdout FPR is tracked as a key ARM metric.
**Documentation**: [Holdout Analysis](../resources/term_dictionary/term_holdout_analysis.md)
**Wiki**: https://w.amazon.com/bin/view/BuyerAbuse/Engineering/Teams/SAGE/Systems/AbuseHoldOutAnalyzerLambda/
**Related**: [FPR](../resources/term_dictionary/term_fpr.md), [Account Closure](../resources/term_dictionary/term_account_closure.md), [ARI](../resources/term_dictionary/term_ari.md)
**Documentation**: [GMRA Term](../resources/term_dictionary/term_gmra.md)
**Docs**: https://docs.ctps.amazon.dev/gmra/index.html
**Four Phases**: Gather (OTF) → Model (AMES) → Rule (RMP) → Act
**Related**: [URES](../resources/term_dictionary/term_ures.md), [OTF](../resources/term_dictionary/term_otf.md), [DPAC](#dpac---detectplanactclose-the-loop)

### RMP - Rule Management Platform
**Full Name**: Rule Management Platform
**Description**: Self-service rule creation, management, and execution engine used within Amazon's risk evaluation ecosystem. Serves as the "R" (Rule) component in GMRA framework, processing gathered features and model scores to determine risk evaluation outcomes and enforcement actions. Largest consumer of CTPS risk evaluation systems with low-latency rule execution (<10ms typical) supporting millions of daily evaluations across buyer fraud, abuse prevention, and seller risk programs.
**Documentation**: [RMP Term](../resources/term_dictionary/term_rmp.md)
**Wiki**: https://w.amazon.com/bin/view/RuleManagementPlatform/
**Related**: [URES](#ures---unified-risk-evaluation-system), [GMRA](#gmra---gathermodelruleact), [CORBEL](#corbel---configuration-management-and-onboarding-of-risk-based-evaluation), [UDV](#udv---user-defined-variable), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md)

### UDV - User-Defined Variable
**Full Name**: User-Defined Variable
**Description**: Feature within Amazon's Rule Management Platform (RMP) that enables rule authors to define custom variables performing calculations or transformations on input data during rule evaluation. UDVs serve as reusable computational components that can aggregate model scores, perform complex calculations, and create derived features for use within rulesets. They execute before rule evaluation and support multi-level variable chains, enabling sophisticated risk evaluation logic and modular rule authoring.
**Documentation**: [UDV Term](../resources/term_dictionary/term_udv.md)
**Wiki**: https://w.amazon.com/bin/view/RMP/
**Related**: [RMP](#rmp---rule-management-platform), [URES](#ures---unified-risk-evaluation-system), [ARROW Everywhere](../resources/term_dictionary/term_arrow_everywhere.md), [CORBEL](../resources/term_dictionary/term_corbel.md), [GMRA](#gmra---gathermodelruleact)

### TEC - TRMS Evaluation Config
**Full Name**: TRMS Evaluation Config (Trust & Risk Management Services Evaluation Configuration)
**Description**: Configuration file format used by FORTRESS and URES to define GMRA (Gather/Model/Rule/Act) evaluations. TEC configurations specify how risk evaluations are structured, including events, hooks, intents, variables, models, and rulesets. Stored in Git repositories (Brazil packages: TRMSEvalConfigNA, TRMSEvalConfigEU, TRMSEvalConfigFE) with JSON format. **Key Entities**: Events (triggers), Hooks (event-to-intent routing), Intents (core evaluation units), GMRA stages (variable categories, models, rulesets), Outcome Scopes. **Architecture**: Team-owned packages → Git version control → Pipeline deployment (alpha → beta → gamma → prod). **Management**: CORBEL UI for viewing/editing, GMRA functional testing for validation, REACT for shadow comparison. **Benefits**: Self-service changes without engineering dependency, version control with rollback, independent team pipelines. **For BAP**: All abuse detection intents (DNR, MDR, QL, rapid-fire) defined as TEC configurations specifying variables from OTF, models from AMES, and rules from RMP.
**Documentation**: [TEC Term](../resources/term_dictionary/term_tec.md)
**Wiki**: https://w.amazon.com/bin/view/EvaluationPlatform/Projects/TEC-On-GIT/
**Docs**: https://docs.ctps.amazon.dev/gmra/index.html
**Format**: JSON configuration files in Brazil packages
**Packages**: TRMSEvalConfigNA (NA), TRMSEvalConfigEU (EU), TRMSEvalConfigFE (FE)
**Management UI**: CORBEL
**Status**: ✅ Active - core configuration format for URES evaluations
**Related**: [GMRA](#gmra---gathermodelruleact), [URES](#ures---unified-risk-evaluation-system), [CORBEL](#corbel---configuration-management-and-onboarding-of-risk-based-evaluation), [OTF](#otf---on-the-fly), [AMES](#ames---active-model-execution-service), [RMP](../resources/term_dictionary/term_rmp.md)

### CQLS - Customer Quantity Limit Service
**Full Name**: Customer Quantity Limit Service
**Description**: System enforcing quantity limits at Detail Page, Cart, and Checkout stages (stages 1-3). Owned by Retail/Pricing teams. Handles single-account enforcement only — BRP owns Stage 4 (post-order multi-account detection via IDA).
**Documentation**: [CQLS Term](../resources/term_dictionary/term_cqls.md)
**Related**: [QLA](../resources/term_dictionary/term_qla.md), [IDA](../resources/term_dictionary/term_ida.md), [CORBEL](#corbel---configuration-management-and-onboarding-of-risk-based-evaluation)

### CORBEL - Configuration management and Onboarding of Risk Based EvaLuation
**Full Name**: Configuration management and Onboarding of Risk Based EvaLuation
**Description**: Amazon's web portal for managing GMRA (Gather/Model/Rule/Act) configurations in URES (Unified Risk Evaluation System), providing self-service capabilities for SDEs, data scientists, and analysts to create, edit, and monitor risk evaluation intents without requiring platform team involvement. Core features include Intent Dashboard for monitoring evaluation health, Intent Creation/Edit for self-service GMRA configuration, and GMRES testing for validating configurations before production deployment. Regional portals (NA, EU, FE, CN) integrate with TEC service for git-based version control and support deployment pipeline progression through Shadow → OneBox → Production stages with comprehensive guardrails. For Buyer Abuse Prevention, CORBEL serves as the primary control plane managing all abuse detection intent configurations including DNR, MDR, QL, CAP routing, and PFW evaluations across their complete lifecycle from creation to production monitoring.
**Documentation**: [CORBEL Term](../resources/term_dictionary/term_corbel.md) | [CORBEL Tool Guide](../resources/tools/tool_corbel.md)
**Portal**: https://corbel-na.aka.amazon.com (NA), https://corbel-eu.aka.amazon.com (EU), https://corbel-fe.aka.amazon.com (FE), https://corbel-cn.aka.amazon.com (CN)
**Docs**: https://docs.ctps.amazon.dev/corbel/index.html
**Key Features**: Intent Dashboard, Creation/Edit, Evaluation Summary, Variable Latency Planner, GMRES Testing
**Backend**: TEC (TRMS Evaluation Configuration Service) - git-based configuration storage
**Status**: ✅ Active - primary UI for URES configuration management
**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md), [FORTRESS](../resources/term_dictionary/term_fortress.md), [OTF](../resources/term_dictionary/term_otf.md), [AMES](../resources/term_dictionary/term_ames.md), [RMP](../resources/term_dictionary/term_rmp.md)


### EDM - Evaluation Decision Mapper
**Full Name**: Evaluation Decision Mapper
**Description**: Translation component being built as part of the APWS-to-ATS migration. Maps Nautilus evaluation outcome handler results into Decision Policies and OLE (Orchestrated Lambda Execution) workflows, **bridging legacy SWF-based enforcement to modern Lambda/Step Function architecture**. Owned by BAE Team BRASS.
**Documentation**: [EDM](../resources/term_dictionary/term_edm.md)
**Related**: [ATS](../resources/term_dictionary/term_ats.md), [ORCA](../resources/term_dictionary/term_orca.md)

### FORTRESS - Fraudulent Order Reduction Through Risk Evaluation at Super Speed [LEGACY]
**Full Name**: Fraudulent Order Reduction Through Risk Evaluation at Super Speed
**Status**: ⚠️ **DEPRECATED** - Replaced by URES (Unified Risk Evaluation Services) since 2020
**Description**: Legacy buyer risk evaluation engine that orchestrated fraud and abuse evaluations using GMRA (Gather-Model-Rule-Action) framework. Originally TRMS's primary evaluation platform for buyer fraud prevention before transitioning to unified URES platform 2020-2021. **Historical Architecture**: Event → DWAR → FORTRESS → GMRA orchestration (Gather via OTF/VCS, Model via AMES, Rule via RMP, Action) → Decision (PASS/CANCEL/PENDING). Processed millions of daily evaluations for buyer fraud, abuse prevention, payment risk, and account integrity across all Amazon marketplaces. **Deprecation Reason**: Tight coupling with client customizations led to operational complexity and scalability limits. Separate FORTRESS (buyer) and COSMOS (seller) engines duplicated functionality. **Migration 2020**: FORTRESS made generic to support any evaluation type, then unified with COSMOS into URES providing better abstraction, self-service via CORBEL, and extensibility. **Modern Equivalent**: All FORTRESS functionality now in URES - same GMRA methodology, same integration partners (OTF, AMES, RMP, VCS), same evaluation types, but with unified platform and self-service tooling. **Current References**: Legacy wikis, old code comments, MDS table names (fortress_retail, fortress_digital data streams), and colloquial conversation still reference FORTRESS. **Correct Usage**: Use "URES evaluation" or "risk evaluation" instead of "FORTRESS" for new work. Wiki redirect: https://w.amazon.com/index.php/DigitalFraud/FORTRESS → https://w.amazon.com/bin/view/EvaluationPlatform/. **For BAP**: All buyer abuse evaluations (DNR, MDR, FLR, PDA, CAP routing, PFOC, Refund Interception) migrated from FORTRESS to URES with improved self-service capabilities.
**Documentation**: [FORTRESS Term](../resources/term_dictionary/term_fortress.md) - Comprehensive legacy system documentation
**Wiki**: https://w.amazon.com/index.php/DigitalFraud/FORTRESS (redirects to URES)
**Replacement**: [URES](#ures---unified-risk-evaluation-system) - Use this for all new work
**Migration**: 2020-2021 transition; FORTRESS name deprecated, GMRA concepts preserved in URES
**Key Message**: When you see "FORTRESS" in code/docs, mentally translate to "URES evaluation"
**Related**: [URES](#ures---unified-risk-evaluation-system), [GMRA](#gmra---gathermodelruleact), [COSMOS](../resources/term_dictionary/term_cosmos.md), [DWAR](#dwar---deferred-write-ahead-request), [FBS](../resources/term_dictionary/term_fbs.md)

### OTF - On The Fly
**Full Name**: On The Fly
**Description**: Real-time variable computation and feature engineering service (GMRA Gather phase). Calculates aggregate features and behavioral signals from streaming data sources.
**Documentation**: [OTF Term](../resources/term_dictionary/term_otf.md)
**Wiki**: https://w.amazon.com/bin/view/TRMSDataPlatform/OTFV2/
**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md), [OWEN](../resources/term_dictionary/term_owen.md), [FeatureHub](#featurehub---feature-hub)

### FeatureHub - Feature Hub
**Full Name**: Feature Hub (Feature Access & Management Service)
**Migration Path**: `VCOL` → `AbuseVCS` → `FeatureHub` (in progress)
**Description**: Amazon's centralized feature access and management platform that provides a unified API Gateway for accessing features from multiple feature providers (OTFv2, BuyerFraudVCS, AbuseVCS, DigitalVCL, SageMaker Feature Store, DVS). Owned by CMLS FAM (Feature Access & Management) team, FeatureHub decouples real-time data access from precomputed feature access, enabling self-service feature onboarding without requiring SDE involvement. Implements cross-cutting concerns like authorization, data governance, rate limiting, and access logging. **Key APIs**: GatherFeatures (evolution of ComputeVariables), ListKnownFeatures, GetFeatureMetadata, QueryMDSFeatures (replaces FDG for historical data). **VCS Migration**: Target platform for consolidating all VCS services - AbuseVCS migrating to AbuseFH namespace, BFVCS active migration, SVCS planned. **2025 Improvements**: FeatureHub Sandbox Java Sidecar achieved 50-65% latency reduction (P99: 101ms→44ms NA, 92ms→32ms IN). **Namespaces**: Abuse.* (legacy→AbuseFH), BuyerFraud.*, Digital.*, OTF.*. Enables scientists to launch features without SDE engagement (1-2 days saved per feature).
**Documentation**: [FeatureHub Term](../resources/term_dictionary/term_featurehub.md)
**Wiki**: https://w.amazon.com/bin/view/CMLS/Services/FeatureHub/
**HLD**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/FeatureHub/HighLevelDesign/
**Owner**: cmls-fam (LDAP) - CMLS FAM team
**Office Hours**: https://w.amazon.com/bin/view/CMLS/BuyerFraudVariableComputationService/VCSOfficeHour/
**Feature Providers**: OTFv2, BuyerFraudVCS, AbuseVCS, DigitalVCL, DVS, SageMaker Feature Store
**Key Innovation**: Self-service feature onboarding, unified API Gateway for all feature providers
**Status**: ✅ Active - strategic platform for VCS consolidation
**Related**: [AbuseVCS](#abusevcs---abuse-variable-computation-service), [VCOL](#vcol---variable-computation-orchestration-library-deprecated), [OTF](#otf---on-the-fly), [URES](#ures---unified-risk-evaluation-system), [AMES](#ames---active-model-execution-service), [DFG](#dfg---domain-feature-generator), [SAIS](#sais---secure-ai-sandbox)

### AMES - Active Model Execution Service

**Full Name**: Active Model Execution Service

**Description**: Amazon's TRMS service that loads machine learning models into memory and provides an online scoring API for real-time model evaluation. Serves as the "M" (Model) component in the GMRA framework, executing ML models against input features to generate risk scores and predictions used in fraud detection and abuse prevention. Supports multiple model types (Random Forest, GBT, DNN, PMML, SageMaker) with low latency (<50ms typical) and high availability (99.9%+). Organized into partitions hosting different model objectives with version control, aliases (Active/Audit), and lifecycle management.

**Key Features**: In-memory model hosting, real-time inference API, multi-model execution, partition-based scaling, shadow mode testing, model versioning

**Buyer Abuse Applications**: MTL_PDA model (pre-delivery abuse), DNR detection, FLR/MDR/NSR (return abuse), ACD (account compromise), synthetic identity detection

**Documentation**: [AMES Term](../resources/term_dictionary/term_ames.md)

**Wiki**: https://w.amazon.com/index.php/ContinuousLearning/ActiveModelExecutionService

**Dashboard**: https://w.amazon.com/bin/view/ContinuousLearning/ActiveModelExecutionService/Dashboard

**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md), [OTF](../resources/term_dictionary/term_otf.md), [RMP](../resources/term_dictionary/term_rmp.md), [MDS](../resources/term_dictionary/term_mds.md)

### ARCI - Auto Root Cause Identification
**Full Name**: Auto Root Cause Identification
**Description**: Framework within BRP Payment Risk ML providing extensible ML solutions and an interactive R-Shiny web interface for automated root cause analysis of metric anomalies. **Reduces ML OE workload** by automating deep-dive analysis that scientists previously performed manually. Deployed on NAWS infrastructure with Federate authentication. Developed through the Tech Excellence Working Group.
**Documentation**: [ARCI Term](../resources/term_dictionary/term_arci.md)
**Web App**: https://arci.iad.prod.brpml.payment-risk-buyer-fraud.trms.amazon.dev
**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md), [DAWS](../resources/term_dictionary/term_daws.md)

### COSMOS - Continual Seller Monitoring Service [DEPRECATED]
**Full Name**: Continual Seller Monitoring Service
**Status**: ⚠️ **DEPRECATED** - Fully migrated to URES as of January 25, 2023
**Description**: Legacy seller risk evaluation platform that allowed clients to detect the risk of fraud, abuse, or performance issues before they affected customers. All 158 Selling Partner use cases and 57 associated events have been migrated to URES. **Historical Architecture**: GMRAP workflow (Gather → Models → Rules → Actions → Publishers) triggered by seller lifecycle events (registration, sign-in, account changes, orders). **Historical Capabilities**: Collected ~8,000 variables per seller, executed 30+ ML models, took ~15K enforcement actions/day, evaluated 156 relationship attributes. **Why Deprecated**: FORTRESS (buyer-side) and COSMOS (seller-side) duplicated functionality - unified into URES providing better abstraction, self-service via CORBEL, and extensibility. **Modern Equivalent**: All COSMOS functionality now in URES - same GMRAP methodology, same integration partners (OTF, AMES, RMP, SES), same evaluation types, but unified platform with improved self-service. **Current References**: Legacy wikis, old code comments, MDS table names, and colloquial conversation still reference COSMOS. **Correct Usage**: Use "URES seller evaluation" instead of "COSMOS" for new work.
**Documentation**: [COSMOS Term](../resources/term_dictionary/term_cosmos.md) - Comprehensive legacy documentation
**Wiki**: https://w.amazon.com/index.php/Main/COSMOS (historical reference)
**Docs Hub**: https://docs.ctps.amazon.dev/cosmos-evaluation/cosmos-evaluation.html (deprecation notice)
**Replacement**: [URES](#ures---unified-risk-evaluation-system) - Use this for all new work
**Migration Date**: January 25, 2023 (158 use cases, 57 events migrated)
**Key Message**: When you see "COSMOS" in code/docs, mentally translate to "URES seller evaluation"
**Related**: [URES](#ures---unified-risk-evaluation-system), [FORTRESS](#fortress---fraudulent-order-reduction-through-risk-evaluation-at-super-speed-legacy), [SES](../resources/term_dictionary/term_ses.md), [RMP](../resources/term_dictionary/term_rmp.md), [CORBEL](#corbel---configuration-management-and-onboarding-of-risk-based-evaluation)

### DWAR - Deferred Write-Ahead Request
**Full Name**: Deferred Write-Ahead Request
**Description**: URES component enabling asynchronous evaluation. Allows clients to request evaluations that are processed asynchronously and results retrieved later.
**Documentation**: [DWAR Term](../resources/term_dictionary/term_dwar.md)
**Related**: [URES](../resources/term_dictionary/term_ures.md), [JUMICS](../resources/term_dictionary/term_jumics.md)

### JUMICS - Just Move It to Core Services
**Full Name**: Just Move It to Core Services
**Description**: Self-service framework that automates migrating offline risk evaluation pipelines (typically Cradle-based) to Core Services (URES) with zero ML scientist or engineering effort.
**Documentation**: [JUMICS Term](../resources/term_dictionary/term_jumics.md)
**Launch**: March 2024
**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md), [Cradle](../resources/term_dictionary/term_cradle.md), [UEL](#uel---ures-event-listener)

### UEL - URES Event Listener
**Full Name**: URES Event Listener
**Description**: Critical component of the JUMICS (Just Move It to Core Services) framework that enables event-driven integration between data pipelines and URES. Listens to and ingests client events from multiple sources (Kinesis streams, SNS topics, SQS queues) and forwards them to DWAR for URES evaluation. **Event Flow**: Cradle Job → Kinesis Stream → UEL → DWAR → URES → GMRA Evaluation. **Key Capabilities**: (1) Event Source Integration - Kinesis streams (primary), SNS topics, SQS queues, synchronous DWAR API; (2) Event Parsing & Validation - flattened JSON input, auto-conversion of non-standard fields to event variables; (3) DWAR Request Conversion - automatic transformation to DWAR-compliant format with zero client effort; (4) Rate Limiting - parallelism control formula: `(Required TPS × Avg Latency (ms)) / 1000`. **AWS Accounts**: Beta (339713103151), Prod (905418167828). **Regional Deployment**: us-east-1 (NA), us-west-2 (FE), eu-west-1 (EU), eu-south-2 (ZAZ). **JUMICS Role**: One of four core components (UEL, DWAR Request Converter, GMRA Converter, Cradle Integration) enabling zero-effort migration of offline evaluations to real-time URES. **Benefits**: Automatic event ingestion from Kinesis, standard DWAR conversion, zero ML scientist effort, self-service onboarding. **Monitoring**: Event ingestion rate, parsing errors, Kinesis lag, DWAR call success rate, end-to-end latency. **Use Cases**: Offline-to-online migration (Cradle → URES), seller risk evaluation, buyer abuse post-concession, graph-based evaluations (RGCN). **Key Insight**: Bridge between offline ML pipelines and real-time URES evaluation - ML scientists maintain familiar Cradle workflow while gaining production-grade Core Services benefits.
**Documentation**: [UEL Term](../resources/term_dictionary/term_uel.md)
**Wiki**: https://w.amazon.com/bin/view/IndiaRisk/DWAR/Runbook/JUMICSOnboardingGuide
**Onboarding SIM**: https://sim.amazon.com/issues/create?template=ffacb7ca-167f-49ea-bc8a-bbed8c7d9017
**Primary Source**: Kinesis Streams (from Cradle jobs)
**Output**: DWAR requests for URES evaluation
**AWS Accounts**: Beta: 339713103151, Prod: 905418167828
**Regions**: us-east-1 (NA), us-west-2 (FE), eu-west-1 (EU), eu-south-2 (ZAZ)
**Status**: ✅ Active - core component of JUMICS framework
**Related**: [JUMICS](#jumics---just-move-it-to-core-services), [URES](#ures---unified-risk-evaluation-system), [DWAR](#dwar---deferred-write-ahead-request), [GMRA](#gmra---gathermodelruleact), [Cradle](../resources/term_dictionary/term_cradle.md), [CORBEL](#corbel---configuration-management-and-onboarding-of-risk-based-evaluation)

---

## Account Security & Fraud Detection Systems

### ContREE - Continuous Risk Evaluation and Enforcement
**Full Name**: Continuous Risk Evaluation and Enforcement
**Description**: AIT's continuous post-sign-in risk monitoring using TRACE framework (NLP on session behavior). 5 use cases: SignIn+1HR, SignUp+1HR, SetMobile, Payment Updates, Contact Fraud. Detects ATO/BAA, ejects bad actors, shares risk via RCVS.
**Documentation**: [ContREE Term](../resources/term_dictionary/term_contree.md)
**Wiki**: https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/Program/ContREE/
**Key Innovation**: Journey-based risk evaluation leveraging additional time and behavioral signals for better differentiation between legitimate customers and attackers
**Coverage**: NA, EU (primary); expanding to WW
**Related**: [ATO](../resources/term_dictionary/term_ato.md), [TRACE], [CBBFCS](../resources/term_dictionary/term_cbbfcs.md), [LEO], [SpiderWeb], [RCVS]

### DTE - Dynamic Trigger Engine
**Full Name**: Dynamic Trigger Engine
**Description**: A behavior-driven triggering system that extends ContREE beyond static time- and event-based checkpoints. **DTE continuously monitors sessions via Traffic Stream data in near real-time**, firing risk evaluations when suspicious behavioral patterns emerge. Feeds into URES/GMRA/ATS for detection and mitigation, unifying risk evaluation across all event types.
**Documentation**: [DTE Term](../resources/term_dictionary/term_dte.md)
**Related**: [ContREE](../resources/term_dictionary/term_contree.md), [URES](../resources/term_dictionary/term_ures.md), [BAA](../resources/term_dictionary/term_baa.md)

### ME - Moderated Enforcement
**Full Name**: Moderated Enforcement
**Description**: A non-terminal enforcement mechanism that restricts specific account capabilities (e.g., order placement) rather than suspending the entire account. **Enables action against HIGH-risk accounts at 95%–99% precision** — a population previously unenforced due to the 99% threshold for suspension. Built by Payment Risk ACE team and shared across BRP pillars. North star: ensure no genuine customer experiences terminal enforcement.
**Documentation**: [Moderated Enforcement Term](../resources/term_dictionary/term_moderated_enforcement.md)
**Wiki**: https://w.amazon.com/bin/view/PaymentRisk/Engineering/Action_Taking_Systems/Moderated_Enforcement/
**Related**: [ContREE](../resources/term_dictionary/term_contree.md), [DeepCARE](../resources/term_dictionary/term_deepcare.md), [PFOC](../resources/term_dictionary/term_pfoc.md), [AOC](../resources/term_dictionary/term_aoc.md)

### RES - Risk Evaluation System
**Full Name**: Risk Evaluation System
**Description**: The at-gate risk evaluation system for Amazon account creation and registration. **Evaluates risk synchronously during sign-up to detect and prevent Bad Actor Accounts before they can commit fraud or abuse.** Assesses email domain risk, device fingerprints, and behavioral patterns; triggers challenges (CAPTCHAs, phone verification) or blocks creation when confidence thresholds are met. Dupin 1.0 penetration-tests RES to proactively identify weaknesses.
**Documentation**: [RES Term](../resources/term_dictionary/term_res.md)
**Wiki**: https://w.amazon.com/bin/view/TRMSAccountIntegrity/Account_Creation/
**Related**: [ContREE](../resources/term_dictionary/term_contree.md), [URES](../resources/term_dictionary/term_ures.md), [Dupin](../resources/term_dictionary/term_dupin.md)

### Unified Tagging Pipeline
**Full Name**: ContREE BAA Unified Tagging Pipeline
**Description**: AIT's centralized, automated ground-truth labeling pipeline for BAA detection across ContREE trigger points (PostSignUp, SetClaim, AddPayment). **Fully automated with no human-in-the-loop, reducing processing time from 2 days to 4 hours.** Uses N-hop propagation to discover 20% more BAAs than legacy tagging. Operates at dual cadence: 3-week matured tagging for model training and 1-week intermediate tagging for faster rule deployment.
**Documentation**: [Unified Tagging Term](../resources/term_dictionary/term_unified_tagging.md)
**Related**: [ContREE](../resources/term_dictionary/term_contree.md), [BAA](../resources/term_dictionary/term_baa.md), [FROST](../resources/term_dictionary/term_frost.md)

### Appeal Automation - BAA Appeal Automation
**Full Name**: BAA Appeal Automation
**Description**: Automated processing of Bad Actor on Account appeal cases using a three-component architecture: DeepCARE (eSNN + KNN similarity classification), AITAppealLLM (Claude 3 via Bedrock following SOP guidelines), and deterministic rules. **Expanded worldwide in Q1 2026, increasing automation from 11.72% to 29.09% while maintaining >95% precision.** Reduces resolution time from 23 hours to under one minute. Enables 137% increase in automated BAA suspensions.
**Documentation**: [Appeal Automation Term](../resources/term_dictionary/term_appeal_automation.md)
**Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/DeepCARE/
**Related**: [DeepCARE](../resources/term_dictionary/term_deepcare.md), [ContREE](../resources/term_dictionary/term_contree.md), [GRAIL](../resources/term_dictionary/term_grail.md)

### AARS - Amazon Account Risk Score
**Full Name**: Amazon Account Risk Score
**Description**: Model that identifies account risk proactively before any real fraud events happen. Continuous risk assessment throughout customer account lifecycle.
**Documentation**: [AARS Term](../resources/term_dictionary/term_aars.md)
**Quip**: https://quip-amazon.com/oUaaA8T2EVYq
**Related**: [ATO](../resources/term_dictionary/term_ato.md), [IS](../resources/term_dictionary/term_is.md)

### ACD - Account Compromise Detection
**Full Name**: Account Compromise Detection
**Description**: Service that determines whether to issue OTP challenge based on sign-in information. Evaluates high TPS authentication requests in real time with <150ms SLA.
**Documentation**: [ACD Term](../resources/term_dictionary/term_acd.md)
**Related**: [ATO](../resources/term_dictionary/term_ato.md), [OTP](../resources/term_dictionary/term_otp.md), [IS](../resources/term_dictionary/term_is.md)

### APSA - Adaptive Protection at Sign-up for Abuse
**Full Name**: Adaptive Protection at Sign-up for Abuse
**Description**: Account creation risk evaluation system that prevents bad actor account creation. Focuses on preventing abuse at account sign-up stage.
**Documentation**: [APSA Term](../resources/term_dictionary/term_apsa.md)
**Related**: [MAA](../resources/term_dictionary/term_maa.md), [IS](../resources/term_dictionary/term_is.md)

### BDS - Bot Detection Service
**Full Name**: Bot Detection Service
**Description**: Service that scores bot traffic attempting to access Amazon systems. Identifies automated account creation and credential stuffing attacks.
**Documentation**: [BDS Term](../resources/term_dictionary/term_bds.md)
**Related**: [BES](../resources/term_dictionary/term_bes.md), [Bot](../resources/term_dictionary/term_bot.md), [IS](../resources/term_dictionary/term_is.md)

### BES - Bot Evaluation Service
**Full Name**: Bot Evaluation Service
**Description**: Service that scores bot traffic. Works alongside BDS to identify and score automated malicious activity.
**Documentation**: [BES Term](../resources/term_dictionary/term_bes.md)
**Related**: [BDS](../resources/term_dictionary/term_bds.md), [Bot](../resources/term_dictionary/term_bot.md)

### BTS - BOT Tagging Service
**Full Name**: BOT Tagging Service
**Description**: Service that tags and tracks bot traffic for analysis and blocking. Works alongside BDS/BES to identify automated malicious activity.
**Documentation**: [BTS Term](../resources/term_dictionary/term_bts.md)
**Related**: [BDS](../resources/term_dictionary/term_bds.md), [BES](../resources/term_dictionary/term_bes.md), [Bot](../resources/term_dictionary/term_bot.md)

### CRE - Channel Risk Evaluation
**Full Name**: Channel Risk Evaluation (formerly Trusted Device Service/TDS)
**Description**: Real-time risk evaluation service that assesses compromise risk of communication channels (email, SMS, devices) for use in possession challenges during authentication. When Account Compromise Detection (ACD) identifies risky signin requiring possession challenge, CRE evaluates which channels are safe for verification (OTP, TIV). **Architecture**: EvaluateChannelRisk API - client provides channel, CRE returns RiskContext with CHANNEL_COMPROMISE risk type and risk level (LOW/MEDIUM/HIGH/UNKNOWN). **Why Renamed**: TDS was misnomer (evaluates ALL channels not just devices), "risk" terminology aligns with TRMS services vs inverse "trust". **Eliminated Dependencies**: No longer calls AuthService, DMS, Kiang - faster (~300ms), more reliable. **Channel Evaluation**: (1) Email - ML model + rules (untrusted domains, sanitization, PRA clean), (2) SMS - default LOW risk (lower fraud), future ML model, (3) Device - registration date, usage patterns, app presence. **Integration**: ACD flags risky signin → CVF fetches channels → CVF calls CRE per channel → CRE evaluates risk → CVF filters HIGH risk channels → Display only safe channels → Customer verifies → Attacker blocked. **Not Tier-1**: Clients implement fallback (fail open/closed). **Effectiveness**: Audit mode measures prevented ATOs, balance false positives vs false negatives. **Roadmap**: Publish to RCVS, mobile ML model, dynamic thresholds, multi-channel assessment, real-time compromise detection, expanded channel types (authenticator apps, passkeys, biometrics).
**Documentation**: [CRE Term](../resources/term_dictionary/term_cre.md)
**Wiki**: https://w.amazon.com/bin/view/CustomerAccountProtection/RiskEvaluationService/
**Legacy Name**: [TDS (Trusted Device Service)](../resources/term_dictionary/term_tds.md) - Deprecated
**API**: EvaluateChannelRisk (current), GetTrustedChannels (deprecated)
**Latency**: P50 ~100ms, P99 ~300ms, timeout 3s
**Key Principle**: Ensure authentication challenges use only channels attacker does NOT control
**Related**: [ACD](#acd---account-compromise-detection), [TDS](#tds---trusted-device-service-deprecated), [CVF](../resources/term_dictionary/term_cvf.md), [TIV](#tiv---transaction-intent-verification), [OTP](../resources/term_dictionary/term_otp.md), [IS](../resources/term_dictionary/term_is.md)

### Empresa - Business Entity Profile Service
**Full Name**: Empresa Service (Spanish for "business/company")
**Description**: Amazon Business (AB) Business Customer Platform (BCP) system that models real-world business entities (businesses, employees), enabling mapping of Amazon Business accounts to these entities and generating enriched profiles. **Key Entities**: Businesses (Empresa Entity ID), Business Accounts (BAID), Agents (employees), Business User Accounts (CID). **Architecture**: Composed of Empresa Core (data backbone), ECFG (fragment generators), ERIS (registration input), APV (account profile vending), EFM (fragment matching). **Profile Attributes**: business_account_id, empresaid, marketplaceid, businessname, industrytype, annualrevenue, numberOfUserAccounts, iscps (Sales Managed), iscpseligible. **Customer Tiers**: CPS (~20% GMS, large corporations) vs SSR (~80% GMS, small businesses). **Abuse Prevention Integration**: Critical for Bifrost bridge - when ABRM enforces a business account, Bifrost alerts BRP to close all associated CID accounts. Addresses enforcement gap where BRP operates at CID level while AB operates at BAID level. **Bad Actor Loophole (Pre-Bifrost)**: Closed BAIDs could add new CIDs to continue abuse; closed CIDs could join other BAIDs. **Profile Vending API**: GetBusinessProfile, GetBusinessAccountProfile, GetAgentProfile, SearchBusinesses.
**Documentation**: [Empresa Term](../resources/term_dictionary/term_empresa.md)
**Wiki**: https://w.amazon.com/bin/view/B2B/BCP/Services/Empresa/
**Profile Vending API**: https://w.amazon.com/bin/view/B2B/BCP/Services/Empresa/API/ProfileVending/
**Amazon Business Abuse**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/SPADE/SPEAR/AmazonBusinessAbuse/
**AB to Retail Bridge**: https://w.amazon.com/bin/view/AmazonBusiness/BARQ/Projects/ABToRetailBridge/
**Architecture Quip**: https://quip-amazon.com/5n72AqWt8V8j/Empresa-Q1-2022-Architecture
**Owner**: AB-BCP (ab-bcp POSIX group)
**Key Components**: Empresa Core, ECFG, ERIS, APV, EFM
**Marketplaces**: 9 worldwide
**Key Integration**: Bifrost (enforcement synchronization between AB and BRP)
**Status**: ✅ Active - core AB data infrastructure with abuse prevention integration
**Related**: [Bifrost](../resources/term_dictionary/term_bifrost.md), [BAID](../resources/term_dictionary/term_baid.md), [AB](../resources/term_dictionary/term_ab.md), [ABRM](../resources/term_dictionary/term_abrm.md), [Neptune](../resources/term_dictionary/term_neptune.md)

### TDS - Trusted Device Service [DEPRECATED]
**Full Name**: Trusted Device Service
**Status**: ⚠️ **DEPRECATED** - Renamed to Channel Risk Evaluation (CRE)
**Description**: Legacy name for channel trust evaluation service. **Why Deprecated**: (1) Misnomer - evaluated ALL channels (email, SMS, devices) not just devices, (2) "Trust" terminology inverse of "risk" causing confusion with TRMS services, (3) Customer focus - users want to know risky channels to avoid. **Legacy Architecture**: GetTrustedChannels API - service fetched channels from AuthService/DMS/Kiang AND evaluated trust, returned trust levels (HIGH/MEDIUM/LOW). **Problems**: 3 major dependencies made service complex, slow, prone to cascading failures. **Migration to CRE**: (1) API renamed EvaluateChannelRisk, (2) Client provides channels (not CRE), (3) Returns RiskContext not trust level, (4) Eliminated 3 dependencies, (5) "Risk" terminology aligned. **Benefits**: Faster, more reliable, clearer responsibility, standardized response. **Deprecation**: GetTrustedChannels API and trust levels deprecated, use CRE EvaluateChannelRisk and RiskContext instead.
**Documentation**: [TDS Term](../resources/term_dictionary/term_tds.md)
**Wiki**: https://w.amazon.com/bin/view/CustomerAccountProtection/TrustedDeviceService/
**Current Name**: [CRE (Channel Risk Evaluation)](../resources/term_dictionary/term_cre.md) - Use this instead
**Migration**: All clients should migrate to CRE APIs and terminology
**Related**: [CRE](#cre---channel-risk-evaluation), [ACD](#acd---account-compromise-detection), [IS](../resources/term_dictionary/term_is.md)

### BSTC - Buyer Seller Transaction Collusion
**Full Name**: Buyer Seller Transaction Collusion
**Description**: Sellers offer products at premium price, register/compromise buyer accounts with stolen credit cards, and purchases are made for high-priced items. Sellers disburse funds quickly before chargebacks arrive.
**Documentation**: [BSTC Term](../resources/term_dictionary/term_bstc.md)
**Wiki**: https://w.amazon.com/index.php/Fraud_Squad_Collusion_Project#HTypesofCollusion
**Related**: [MFN](../resources/term_dictionary/term_mfn.md), [MRI](../resources/term_dictionary/term_mri.md), [CB](../resources/term_dictionary/term_cb.md)

### FPP - Forgot Password Pipeline
**Full Name**: Forgot Password Pipeline
**Description**: Authentication workflow handling password reset requests. Critical security component monitoring for account takeover attempts during password recovery.
**Documentation**: [FPP Term](../resources/term_dictionary/term_fpp.md)
**Related**: [IS](../resources/term_dictionary/term_is.md), [ATO](../resources/term_dictionary/term_ato.md), [CCC](../resources/term_dictionary/term_ccc.md)

---

## Customer Service Platforms

### AC3 - Amazon Customer Care Center
**Full Name**: Amazon Customer Care Center (formerly Aviary)
**Description**: CS platform replacing CSC (mid-2024). 23 marketplaces, all verticals. **BAP Integration**: CAP routing, RSPR, OTF banners, CGW. Tech: Aviary framework, Caracara platform, Amazon Connect, CSALT GraphQL. Metrics: 99.8% handled, 9.12 min ACHT.
**Documentation**: [AC3 Term](../resources/term_dictionary/term_ac3.md)
**Wiki**: [CAP Tech Glossary](https://w.amazon.com/bin/view/CAPTech/Glossary/), [SDS AC3 Page](https://w.amazon.com/bin/view/Amazon_Customer_Care_Center%28AC3%29_landing_Page/Shipping_%26_Delivery_Support_%28SDS%29_AC3_Page/)
**Also Known As**: Aviary (codename - more refers to technology/framework behind AC3)
**Predecessor**: [CSC (Customer Service Central)](../resources/term_dictionary/term_csc.md) - deprecated
**Technology Stack**: Aviary framework, Caracara platform, Amazon Connect routing, CSALT GraphQL, CL-API
**Coverage**: 23 marketplaces, all CS verticals (Retail, AB, D2AS, SDS, CAP)
**BAP Integration**: CAP routing, RSPR, OTF banners, CGW (CAP Guided Workflow), Interventions
**Key Metrics**: 99.80% handled in AC3, 14.94% transfer rate, 9.12 min ACHT
**Key Components**: Remote Components, Solve Cards, Workflows/Wizards, Dobby (auth), CSALT
**Concession Types**: RR, SCR, Account GC, Refunds, Replacements, Bulk (up to 999 items)
**Status**: ✅ Active - primary CS platform (CSC deprecated mid-2024)
**Related**: [CSC](../resources/term_dictionary/term_csc.md), [CAP](../resources/term_dictionary/term_cap.md), [RSPR](../resources/term_dictionary/term_rspr.md), [CSA](../resources/term_dictionary/term_csa.md), [OTF](#otf---on-the-fly)

### ORC - Online Return Center
**Full Name**: Online Return Center
**Description**: Amazon's self-service web application where customers initiate product returns. Built on the Santana platform, ORC allows customers to select items for return, specify return reasons, create Return Merchandise Authorizations (RMAs), select return shipping methods, and print shipping labels. **Key Function**: Primary customer-facing entry point for the returns process, determining return eligibility, available return options, and concession pathways based on policy and abuse risk evaluation. **Technical Stack**: Santana platform (ported from Endless.com ~2012), CReturns backend, ReturnPolicyService, COMET, RMA Service. **Channel Support**: Full support for AFN (1P + FBA), limited support for MFN (displays contact seller message). **Return Options**: Refund on Return, Instant Refund, Refund at First Scan (RFS), Free Replacement, Auto-Replacement (India), Returnless Refund. **BAP Integration Critical Touchpoint**: When customers visit ORC, multiple abuse intents (FLR, MDR, NSR, PDA, RFS suppression) are evaluated to determine available return options. APP (Abuse Policy Plugin) integrates with CReturns during contract creation to evaluate abuse risk via URES and suppress high-risk options. **Graduated Enforcements**: ORC Messaging launched May 2020 - real-time warning messages for high-risk NSR customers, expanded to EU5 by Sept 2020. **Key Insight**: ORC is where customers declare return intent before physical return - evaluating abuse risk here enables proactive prevention rather than reactive detection.
**Documentation**: [ORC Term](../resources/term_dictionary/term_orc.md)
**Wiki**: [Customer Returns](https://w.amazon.com/bin/view/Customer_Returns/), [CReturns](https://w.amazon.com/bin/view/Wax/Services_Teams_in_Amazon/CReturns/), [FBA Returns Glossary](https://w.amazon.com/bin/view/FBA/ReLo/Projects/CustomerReturn/Glossary/)
**BAP Wiki**: [Failed Returns (FLR)](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/Failed_Returns/), [Launch Announcements](https://w.amazon.com/bin/view/BuyerAbuse/Status/LaunchAnnouncements/)
**Platform**: Santana (web application)
**Backend Services**: CReturns, ReturnPolicyService, COMET, RMA Service
**Channel Support**: AFN (full), MFN (limited)
**Return Options**: Refund, Instant Refund, RFS, Free Replacement, Returnless Refund
**Abuse Integration**: APP plugin, URES intent evaluation, Graduated Enforcements
**Key Intents**: FLR, MDR, NSR, RFS suppression
**Prevention Actions**: Option suppression, warning messages, RFS denial
**Launch (Abuse)**: May 2020 - ORC Messaging for Graduated Enforcements
**Status**: ✅ Active - core returns infrastructure with abuse prevention integration
**Related**: [APP](../resources/term_dictionary/term_app.md), [CReturns](../resources/term_dictionary/term_creturns.md), [RFS](../resources/term_dictionary/term_rfs.md), [CAP](../resources/term_dictionary/term_cap.md), [FLR](../resources/term_dictionary/term_flr.md), [MDR](../resources/term_dictionary/term_mdr.md), [NSR](../resources/term_dictionary/term_nsr.md), [RMA](../resources/term_dictionary/term_rma.md)

### CReturns - Customer Returns Platform
**Full Name**: Customer Returns (Return Contract System)
**Description**: Amazon's comprehensive returns platform managing the entire lifecycle of customer returns, from return initiation through refund processing. Defines a **Return Contract** (using Document Model) that captures all aspects of a customer return. **Core Services**: COMET (contract creation, hosts plugins like APP), CRATER (contract execution - RMA, labels, refunds), RPS (Return Policy Service - 13+ resolution offerings in 10ms), RTS (Return Transportation Service), RNS (Return Notification Service). **Key Function**: System of record for returns - tracks initiation via ORC/CS, manages transportation options, coordinates FC grading, executes refund/replacement workflows via CROW. **BAP Integration Critical**: Hosts **Abuse Policy Plugin (APP)** in COMET service for real-time abuse risk evaluation at return creation time. APP evaluates MDR/FLR/NSR risk, determines RFS eligibility suppression, routes high-risk returns to Advanced Detection RCs, applies graduated enforcement treatments. **Contract Lifecycle**: Draft → Signed → In Transit → Received → Processed → Refund. **Key Events**: ReturnContractCreated, ReturnContractSigned, CarrierFirstScan (triggers RFS), FCReceived, GradingComplete, RefundProcessed. **Configuration**: Business Configuration Manager (BCM) for marketplace/category-specific return policies via G2S2.
**Documentation**: [CReturns Term](../resources/term_dictionary/term_creturns.md)
**Wiki**: [CReturns Architecture](https://w.amazon.com/bin/view/Creturns/Architecture), [CReturns Overview](https://w.amazon.com/bin/view/Crtbry/CReturns-Overview/)
**Key Services**: COMET (creation), CRATER (execution), RPS (policy), RTS (transportation), RNS (notifications)
**Packages**: ReturnCOMETService, CRATERService, ReturnPolicyService
**BAP Integration**: APP plugin for abuse risk evaluation, RFS suppression, Advanced Detection routing
**Abuse Intents**: FLR, MDR, NSR, RFS suppression (evaluated via URES at return creation)
**Status**: ✅ Active - core returns infrastructure with abuse prevention integration
**Related**: [ORC](#orc---online-return-center), [APP](../resources/term_dictionary/term_app.md), [RFS](../resources/term_dictionary/term_rfs.md), [CROW](../resources/term_dictionary/term_crow.md), [RMA](../resources/term_dictionary/term_rma.md), [BRW](../resources/term_dictionary/term_brw.md)

### HB - HealBeam
**Full Name**: HealBeam
**Description**: Amazon's A-to-Z Guarantee claims processing service handling the end-to-end lifecycle of MFN marketplace dispute claims. **Core function**: manages claim submission, status transitions, refund processing, and buyer-seller communication for A-to-Z claims. Key components include HealBeamBusinessObjects (Reason.java enum for claim reason codes like NOTR/DIFF/RTRN, ShipmentStatus.java for tracking states like PEND/DELIVERED) and HealBeamService (claims processing API). Sits downstream of RoBO for claims workflow engineering and integrates with DisputeBusinessService and DisputeRulerService.
**Documentation**: [HealBeam](../resources/term_dictionary/term_healbeam.md)
**Packages**: HealBeamBusinessObjects, HealBeamService
**Status**: ✅ Active - core A-to-Z claims processing infrastructure
**Related**: [A-to-Z Claim](../resources/term_dictionary/term_atoz_claim.md), [A-to-Z Eval](../areas/area_atoz_eval.md), [Refund Reason Codes](../resources/tables/resource_refund_requested_reason_codes.md)

---

## Customer Communication & Context Analysis

### CS Contact - Customer Service Contact
**Full Name**: Customer Service Contact (also: CSC - Customer Service Contact)
**Description**: Umbrella term for all customer-initiated contacts with Amazon Customer Service across all three communication channels: **Chat** (real-time text), **Phone** (voice calls), and **Email** (asynchronous text). Each contact generates data captured by CS systems and streamed via Patronus for BAP abuse detection. **Chat** is primary channel (~60% of contacts) with full transcript capture via CS Scribe. **Phone** uses Amazon Connect routing with transcription via Connect Lens (rolling out). **Email** lowest volume but provides written record. All channels feed into Patronus's NA_PATRONUS_CS_CONTACT_EVAL_INTENT for real-time abuse evaluation. **Critical for BAP**: CS Contact data enables Context-Enhanced Abuse Prevention (COAP) - provides "Voice of Customer" context (refund reasons, complaint descriptions, negotiation patterns) missing from transactional data alone. Powers Abuse Polygraph (77% yield, 84% AUC), CSMO Detection ($40MM leakage identification), and CS MO Detection (57% closure rate). **Data Flow**: Customer → CS Channel (Chat/Phone/Email) → CS Systems → Patronus/Heartbeat → MDS/Andes → BAP ML Models → URES Evaluation.
**Documentation**: [CS Contact Term](../resources/term_dictionary/term_cs_contact.md)
**Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_NLP_CSContact/
**Channels**: Chat (primary, ~60%), Phone (voice), Email (async)
**Data Sources**: Patronus, Heartbeat, Junction Service
**Key Intent**: `na_patronus_cs_contact_eval_intent`
**BAP Use Cases**: Abuse Polygraph, CSMO, CS MO Detection, COAP
**Owner**: CS Scribe (chat), CS Connect (phone), various (email)
**Status**: ✅ Active - critical data source for context-enhanced abuse detection
**Related**: [CS Chat](#cs-chat---customer-service-chat), [Patronus](#patronus), [VoC](#voc---voice-of-customer), [CAP](../resources/term_dictionary/term_cap.md), [COAP](../resources/term_dictionary/term_coap.md)

### CS Chat - Customer Service Chat
**Full Name**: Customer Service Chat
**Description**: Amazon's real-time text-based communication channel enabling customers to connect with CSAs for issue resolution, order inquiries, refund requests, and general support. CS Chat provides the underlying chat infrastructure (media service, routing, transcript storage) distinct from the agent-facing UI applications (AC3/CSC). Supports both Sync (legacy) and Async (MessageUs) chat modes - MessageUs allows customers to leave and return within 24 hours. Routing transitioned from legacy GACD (TelephonyChatService) to Amazon Connect. **Critical BAP Data Source**: Chat transcripts fuel abuse detection - 80% of detected MO patterns exploit chat channels. Enables CSMO Detection (57% closure rate), Abuse Polygraph (77% yield, 84% AUC), CS MO Detection ($40MM leakage identification), and Context-Enhanced Abuse Prevention (COAP). **Data Access**: Real-time via CSCaseQueryService/CSMediaArchivalService (cs-sumac), batch via Junction Service (cs-neuron, 6 months history), streaming via Patronus/Heartbeat/Floodgates to Andes. **Key Services**: CS Scribe Chat Service (APIs), ScribeChatStreamProcessor (message streaming, CS-Blaze), CSMediaArchivalService (long-term archival). **Prevention Integration**: Patronus intents evaluate chat credibility in real-time, CSMO matches against Chat Catalogue of confirmed abuse patterns, CAP routing sends high-risk contacts to specialists.
**Documentation**: [CS Chat Term](../resources/term_dictionary/term_cs_chat.md)
**Wiki**: https://w.amazon.com/bin/view/CSTech/CSScribe/Chat/
**Chat Onboarding**: https://w.amazon.com/bin/view/CSTech/CSScribe/Chat/Onboarding/
**BAP Data Access**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_NLP_CSContact/
**Chat Types**: Sync (legacy), Async (MessageUs - primary)
**Routing**: GACD (legacy) → Amazon Connect (current)
**Agent UI**: AC3 (current), CSC (deprecated)
**Transcript Storage**: DynamoDB (active) → CSMediaArchivalService (archived)
**Owner**: CS Scribe team (cs-magus-chat)
**BAP Use Cases**: CSMO (57% closure), Abuse Polygraph (84% AUC), CS MO Detection ($40MM)
**Key Intents**: `na_patronus_cs_contact_eval_intent`, `na_buyer_abuse_contact_eval_csmo_intent`
**Data Sources**: Patronus MDS, Junction Service, AIT Eagles S3
**Status**: ✅ Active - primary text support channel and critical BAP data source
**Related**: [AC3](#ac3---amazon-customer-care-center), [CSMO](../resources/term_dictionary/term_csmo.md), [Patronus](#patronus), [VoC](#voc---voice-of-customer), [CAP](../resources/term_dictionary/term_cap.md), [BSM](#bsm---buyer-seller-messaging)

### BSM - Buyer-Seller Messaging
**Full Name**: Buyer-Seller Messaging
**Description**: Amazon's secure, anonymized communication platform enabling contacts between buyers and 3P sellers regarding product info, delivery, returns/refunds, and service issues. **MFN Policy Requirement**: Buyers must contact seller first and wait 48 hours before filing A-Z claim. **Critical for BAP**: Provides conversational context that fills the "why" gap in traditional transactional data - captures natural language descriptions, negotiation patterns, evidence quality, and sentiment missing from order/return data alone. **Data Availability**: Real-time (Kinesis), daily batch (EDX: bsm-prod), historical (Redshift). **BAP Use Cases**: Context-Enhanced Abuse Prevention (COAP) framework, Claim Abuse detection (A-Z workflow, Mar 2022 launch), Threat Abuse detection (protects sellers from harassment, Nov 2022 launch), GoldMiner annotation processor (32% email automation), Abuse Polygraph (77% yield/84% AUC via Patronus integration). **ML Models**: Transformer-based (BERT/RoBERTa) for multi-lingual conversation analysis. **Dual Purpose**: Benefits both buyer abuse prevention (detects fraudulent claims, manipulation) AND seller protection (blocks threats, harassment, SPI). **Platform Ownership**: Seller Customer Service team; BAP is data consumer. Coverage: 20+ marketplaces with multi-lingual support.
**Documentation**: [BSM Term](../resources/term_dictionary/term_bsm.md)
**Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_BuyerSellerMessaging/
**Key Insight**: "Contact seller first" policy creates documented conversation history essential for context-aware abuse detection
**Related**: [MFN](../resources/term_dictionary/term_mfn.md), [Patronus](#patronus), [VoC](#voc---voice-of-customer), [COAP](../resources/term_dictionary/term_coap.md), [A-Z Claim](../resources/term_dictionary/term_atoz_claim.md)

### Patronus
**Full Name**: Patronus - Streaming Defect Detection
**Description**: Real-time streaming defect detection system from Perfect Order Experience (POE) team that monitors 6 customer feedback sources (CS Contacts, Buyer-Seller Messaging, Product Reviews, Seller Feedback, Returns, Claims) via Heartbeat and Kinesis. Uses Apache Flink for stream processing, augments feedback with ASIN/order/seller context, and applies ML models (Text Mining CCR, MCM multi-class, BEA brand enforcement) to classify into 9 defect types. Critical data source for Buyer Abuse Prevention (BAP) team - powers Abuse Polygraph (77% yield, 84% AUC), CS MO Detection ($40MM leakage), and Review2Risk (77.9% AUC) models through URES intents. Enables both POE product quality enforcement and BAP's Context-Enhanced Abuse Prevention (COAP) initiatives by providing "Voice of Customer" context for concession abuse detection.
**Documentation**: [Patronus Term](../resources/term_dictionary/term_patronus.md)
**Wiki**: https://w.amazon.com/bin/view/Perfect_Order_Experience_Tech/DSPE/Patronus/
**BAP Integration**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/BuyerAbuse_NLP_CSContact/
**Related**: [BSM](#bsm---buyer-seller-messaging), [VoC](#voc---voice-of-customer), [OTF](../resources/term_dictionary/term_otf.md), [BAP](../resources/term_dictionary/term_bap.md)

### VoC - Voice of Customer
**Full Name**: Voice of Customer
**Description**: Amazon's methodology and platform for "listening to customers" through systematic collection, analysis, and operationalization of customer feedback from 16+ channels (CS Contacts, Product Reviews, Social Media, BSM, Returns, Claims, etc.). Primary tool is Heartbeat, providing dashboarding, visualization, and real-time streaming via Floodgates to Andes. Owned by WWDE-CET team, serves 65k+ Amazonians from 43 countries. Critical data source for POE (Patronus defect detection: 20+ marketplaces, 9 defect types) and BAP (Context-Enhanced Abuse Prevention: Abuse Polygraph 77% yield/84% AUC, CS MO Detection $40MM leakage, Review2Risk 77.9% AUC). Operationalizes "empty chair" philosophy by providing Voice of Customer context missing from transactional data alone.
**Documentation**: [VoC Term](../resources/term_dictionary/term_voc.md)
**Platform**: https://heartbeat.cs.amazon.dev/
**Wiki**: https://w.amazon.com/bin/view/VoiceOfTheCustomer/
**Related**: [Patronus](#patronus), [BSM](#bsm---buyer-seller-messaging), [CAP](../resources/term_dictionary/term_cap.md), [POE](../resources/term_dictionary/term_poe.md), [BAP](../resources/term_dictionary/term_bap.md), [Heartbeat](#heartbeat---voice-of-customer-platform)

### Heartbeat - Voice of Customer Platform
**Full Name**: Heartbeat - Voice of Customer Platform
**Description**: Amazon's official Voice of Customer (VoC) platform - an internal tool that enables users to search, visualize, classify, and operationalize customer feedback data from 16+ feedback channels. Serves 65,000+ Amazonians from 43 countries/regions, providing the capability to "listen to customers" at scale and transform feedback into actionable insights. **Core Philosophy**: "To be the ultimate steward that represents the 'empty chair' – allowing others to easily listen, analyze, and operationalize customer feedback." **Product Suite**: (1) **Heartbeat Dashboard** - search/query billions of feedback records, visualization, deep dive investigation; (2) **Textminer** - automated text classification at scale via keyword rules and theme extraction; (3) **Floodgates** - near real-time data streaming to Andes for BI integration; (4) **Nessie** - anomaly detection via SQL patterns and ML. **Data Sources (16+)**: CS Contacts, Product Reviews, Seller Feedback, Returns, Claims, Social Media, App Reviews, BSM, Surveys, Packaging Feedback, CSAT. **Access Levels**: HBS2 (metrics/scrubbed text - manager approval), HBS3 (full text - L4+ CS, L8+ other). **BAP Integration**: Feeds Patronus streaming defect detection which powers Abuse Polygraph (77% yield, 84% AUC), CS MO Detection ($40MM leakage), Review2Risk (77.9% AUC), CSMO Detection (57% closure rate). **Business Impact Examples**: D2CS VoC ($20B BOM savings), Food Safety (45% YoY incident reduction), Andon Cord ($6.6M annual concession savings). **Data Flow**: Customer Feedback → Heartbeat → Floodgates → Andes → BAP Analytics; also Heartbeat → Patronus → OTF/MDS → URES Evaluation.
**Documentation**: [Heartbeat Term](../resources/term_dictionary/term_heartbeat.md)
**Portal**: https://heartbeat.cs.amazon.dev/
**Textminer**: https://heartbeat.cs.amazon.dev/textminer/#/orgs
**Wiki**: https://w.amazon.com/bin/view/VoiceOfTheCustomer/, https://w.amazon.com/bin/view/Heartbeat/Discover/
**User Guide**: https://drive.corp.amazon.com/documents/Heartbeat/University/HB%20User%20Guide.pdf
**Heartbeat University**: https://w.amazon.com/bin/view/CSTech/Heartbeat/University/
**Office Hours**: https://w.amazon.com/bin/view/Heartbeat/Support/OfficeHours/
**Permissions**: https://w.amazon.com/bin/view/Heartbeat/Support/Permissions/
**Owner**: WWDE-CET (VoC Team), heartbeat-team LDAP
**Data Sources**: 16+ channels (CS contacts, reviews, social, returns, claims, BSM, etc.)
**Users**: 65,000+ Amazonians, 43 countries
**Access**: HBS2 (metrics), HBS3 (full text)
**Products**: Dashboard, Textminer, Floodgates, Nessie
**BAP Use Cases**: Abuse Polygraph, CS MO Detection, Review2Risk, CSMO, COAP
**Status**: ✅ Active - central VoC platform for Amazon
**Related**: [VoC](#voc---voice-of-customer), [Patronus](#patronus), [BSM](#bsm---buyer-seller-messaging), [Andes](../resources/term_dictionary/term_andes.md), [MDS](../resources/term_dictionary/term_mds.md)

### Hermod - Outbound Customer Communication Service
**Full Name**: Hermod
**Description**: Amazon's consolidated service for handling **outbound and inbound customer communications** in the Buyer Abuse Prevention and Customer Trust domain. Uses Real-Time Notification Service (RTNS) to send communications via SMS and email. Manages enforcement email blurbs (warnings, solicitations, account closures) and appeal processes. Named after the Norse messenger god. Queue-based processing for account status rule-based transfers.
**Documentation**: [Hermod Term](../resources/term_dictionary/term_hermod.md)
**Wiki**: https://w.amazon.com/bin/view/CustomerTrust/Catalog/FactSolicitation/
**Related**: [ARI](../resources/term_dictionary/term_ari.md), [CSSW](../resources/term_dictionary/term_cssw.md), [ATS](#ats---action-taking-system)

---

## Variable Computation Services

### VCS - Variable Computation Service
**Full Name**: Variable Computation Service
**Description**: Family of specialized services that compute machine learning features and variables for fraud detection and abuse prevention systems. Serves as the "Gather" phase in GMRA framework, providing real-time feature computation for URES risk evaluations. Domain-specific services (AbuseVCS, BFVCS, SVCS) compute aggregated behavioral signals and risk indicators from historical data. All VCS services migrating to FeatureHub for unified feature access platform.
**Documentation**: [VCS Term](../resources/term_dictionary/term_vcs.md)
**Wiki**: https://w.amazon.com/bin/view/CMLS/BuyerFraudVariableComputationService/VCSOfficeHour/
**Related**: [AbuseVCS](#abusevcs---abuse-variable-computation-service), [FeatureHub](#featurehub---feature-hub), [URES](#ures---unified-risk-evaluation-system), [OTF](#otf---on-the-fly), [GMRA](#gmra---gathermodelruleact)

### SigWin - Signality Web Interface
**Full Name**: Signality Web Interface (pronounced "sig-win")
**Description**: Automated browser-based real-time website data gatherer component within URES (ESGS) that enables raw data capture from any website by recording human interactions with Selenium IDE and replaying them on demand. Provides WYSIWYG (What-You-See-Is-What-You-Get) data parity between ML models and human investigators without requiring custom development per website. Critical data source for AutoSignality - captures Paragon/Nautilus investigation tool data (widgets, order history, sign-in events, annotations) enabling LLM-based automation. **Architecture**: SIDE files (Selenium IDE recordings) → ESGS datasource → URES evaluation trigger → Website interaction → Raw HTML capture → Base64+GZIP compression → OTF/Models/Storage consumption. **Key Features**: Multi-page navigation, runtime variables, JavaScript execution, dependency injection via Keyfields. **Output Formats**: Compressed GZIP HTML or JSON. **Latency**: Primarily determined by website load times; complex interactions can take minutes. **Supported Websites**: Nautilus, Paragon (internal); external websites supported with authentication constraints.
**Documentation**: [SigWin Term](../resources/term_dictionary/term_sigwin.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/Signality/Core/SigWin/
**Owner**: ures-sigma team (LDAP)
**Contact**: ritwip@
**Key Innovation**: Bridge data gap between ML and investigators via automated website data capture
**Primary Consumer**: [AutoSignality](../resources/term_dictionary/term_autosignality.md)
**Related**: [URES](#ures---unified-risk-evaluation-system), [ESGS](../resources/term_dictionary/term_esgs.md), [GMRA](#gmra---gathermodelruleact), [OTF](#otf---on-the-fly), [AutoSignality](../resources/term_dictionary/term_autosignality.md)

### WYSIWYG - What-You-See-Is-What-You-Get
**Full Name**: What-You-See-Is-What-You-Get
**Description**: Data capture and processing principle within Buyer Risk Prevention (BRP) ensuring ML models and automated systems have access to the exact same data that human investigators see when reviewing cases. In fraud detection and abuse prevention context, WYSIWYG means data extraction systems (like SigWin) capture raw website data exactly as it appears to investigators using Paragon/Nautilus, enabling data parity between ML models and human decision-makers. **Core Philosophy**: Human investigators outperform ML models partly due to richer, more contextual information access - WYSIWYG bridges this gap. **Implementation**: SigWin captures full HTML pages (not just selected fields), preserving all investigation context including order history, sign-in events, related accounts, annotations, payment/address histories. **Benefits**: (1) Complete data access - all investigation widget data available, (2) Future-proof - new UI features automatically captured, (3) Investigator-ML alignment - models trained on same data humans use, (4) Caching/reuse - raw responses cacheable for multiple consumers. **Trade-offs**: Higher latency (seconds-minutes vs milliseconds) and storage (full HTML vs extracted fields) in exchange for complete data fidelity.
**Documentation**: [WYSIWYG Term](../resources/term_dictionary/term_wysiwyg.md)
**Wiki**: https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/Signality/Core/SigWin/ (SigWin - primary WYSIWYG implementation)
**Key Innovation**: Bridge data gap between ML and investigators by capturing raw website data exactly as rendered
**Primary Implementation**: [SigWin](../resources/term_dictionary/term_sigwin.md)
**Primary Consumer**: [AutoSignality](../resources/term_dictionary/term_autosignality.md)
**Related**: [SigWin](#sigwin---signality-web-interface), [AutoSignality](../resources/term_dictionary/term_autosignality.md), [OTF](#otf---on-the-fly), [URES](#ures---unified-risk-evaluation-system)

### AbuseVCS - Abuse Variable Computation Service
**Full Name**: Abuse Variable Computation Service
**Migration Path**: `VCOL` → `AbuseVCS` → `FeatureHub` (in progress)
**Description**: Coral service that computes abuse-related variables for FORTRESS/URES evaluations. Originally a subcomponent of ConcessionAbuseService (CAS), AbuseVCS serves as the primary variable computation service for buyer abuse prevention ML models and rules. One of the Variable Computation Services (VCS) that vend machine learning features back to DWAR/FORTRESS alongside BuyerFraudVCS (BFVCS) and SellerVCS (SVCS). Java 8 service running on EC2 Apollo. Provides `computeVariables` API called by VCOL to fetch abuse-related variables with `Abuse.` namespace prefix. Includes customer history, order pattern, concession behavior, return pattern, and identity relationship calculators. Integrated with OTFv1 and OTFv2 through VCL-based client library for real-time variable computation. Critical infrastructure for BAP ML models including DNR, MDR, FLR, NSR, PDA, CAP routing, and A-to-Z claim evaluations.
**Documentation**: [AbuseVCS Term](../resources/term_dictionary/term_abuse_vcs.md)
**Wiki**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/Systems/AbuseVCS/
**Dashboard**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/Systems/AbuseVCS/Dashboards/
**Runbook**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/Systems/AbuseVCS/Runbook/
**UMLC Tool**: https://unified-ml-catalog.ctps.amazon.dev/explore (browse AbuseVCS variables)
**Owner**: policy-engineering-dev (POSIX) - Policy Engineering / Core Services
**Key Packages**: ConcessionAbuseService, AbuseVariableComputationLib, AbuseRuleExecutionFramework
**Pipeline**: https://pipelines.amazon.com/pipelines/ConcessionAbuseService-release
**Also Known As**: ConcessionAbuseService (CAS), AVCS
**Use Cases**: PFW evaluation, concession abuse prevention, return abuse prevention, CAP routing, A-to-Z claims
**Future**: Migrating to FeatureHub (AbuseFH namespace) as part of VCS consolidation
**Status**: ✅ Active - primary abuse variable computation service
**Related**: [VCOL](#vcol---variable-computation-orchestration-library-deprecated), [FORTRESS](../resources/term_dictionary/term_fortress.md), [URES](#ures---unified-risk-evaluation-system), [OTF](#otf---on-the-fly), [FeatureHub](#featurehub---feature-hub), [BAP](../resources/term_dictionary/term_bap.md)

### VCOL - Variable Computation Orchestration Library [DEPRECATED]
**Full Name**: Variable Computation Orchestration Library
**Status**: ⚠️ **DEPRECATED** - Replaced by direct AbuseVCS integration
**Migration Path**: `VCOL` → `AbuseVCS` → `FeatureHub` (in progress)
**Description**: Orchestration library that bridges FORTRESS and various Variable Computation Services (VCS). Routes variable computation requests to appropriate services (AbuseVCS, BFVCS, SVCS, FeatureHub) based on variable namespaces, executes parallel calls to minimize latency, and consolidates results. Critical infrastructure for FORTRESS - handles variable validation, registration in RMP through VBS, and metadata caching. Acts as single point of contact enabling FORTRESS to remain business-logic agnostic while accessing multiple specialized VCS services for real-time risk evaluation.
**Documentation**: [VCOL Term](../resources/term_dictionary/term_vcol.md)
**Wiki**: https://w.amazon.com/bin/view/EvaluationPlatform/Projects/VCOL/
**Key Role**: Orchestration layer between FORTRESS and all VCS services (AbuseVCS, BFVCS, SVCS, FeatureHub, DVCL)
**Best Practice**: Always use weblab for VCOL changes - massive blast radius affects all VCS and fraud evaluations
**Replacement**: [AbuseVCS](#abusevcs---abuse-variable-computation-service) - Use this for abuse variable computation
**Related**: [AbuseVCS](#abusevcs---abuse-variable-computation-service), [FORTRESS](../resources/term_dictionary/term_fortress.md), [URES](../resources/term_dictionary/term_ures.md), [OTF](../resources/term_dictionary/term_otf.md), [FeatureHub](#featurehub---feature-hub)

---

## Data Processing & Communication

### CDP - Content Delivery Platform
**Full Name**: Content Delivery Platform
**Description**: Amazon's core infrastructure service for ingesting, processing, storing, and delivering content and documents at scale. Foundational infrastructure layer for UCPP providing enterprise-grade capabilities for evidence and document workflows including virus scanning, format validation, storage management (S3-based with encryption, lifecycle policies), and content delivery (presigned URLs, CloudFront CDN). Handles multi-format support (images, PDFs, videos), automatic thumbnail generation, and event-driven processing. Clean separation of responsibilities: CDP handles content operations (ingest, store, deliver) while UCPP handles business logic (validation, analysis, decisions). Key integration points: CAP evidence workflows, BRW returns photos, Advanced Detection images, A-to-Z claims evidence, Paragon investigation display. Provides centralized security (virus scan, IAM access control), compliance (audit trails, retention policies), and operational excellence (shared monitoring, disaster recovery).
**Documentation**: [CDP Term](../resources/term_dictionary/term_cdp.md)
**Architecture**: S3 storage + Lambda processing + CloudFront delivery + EventBridge orchestration
**Key Capabilities**: Multi-format ingestion, virus scanning, presigned URLs, thumbnail generation, lifecycle management, ElasticSearch discovery
**BRP Use Cases**: Evidence upload/download, returns photos storage, claim documents, investigation evidence packages
**Technology**: S3, CloudFront, Lambda, API Gateway, KMS, CloudWatch, EventBridge
**Related**: [UCPP](#ucpp---unified-content-processing-pipelines), [S3], [CloudFront], [Lambda]

### UCPP - Unified Content Processing Pipelines
**Full Name**: Unified Content Processing Pipelines
**Description**: Amazon's foundational multi-modal content processing capability providing standardized patterns (DRFS: Notify-Ingest-Process-Store) for ingesting, validating, processing, and storing evidence and documents across BRP workflows. Core infrastructure for Evidence Intelligence enabling automated document validation, metadata extraction, and comprehensive content analysis with synchronous (<1s basic validation) and asynchronous (≤5 days detailed processing) capabilities. Processes 9M+ incident photos, 3.4M product photos, 1.4M police reports annually for CAP, Seller Grading, A-to-Z Claims workflows. Integrates with CDP (Content Delivery Platform) and VISTA (computer vision) to provide validation decisions (Valid/Not Valid/Not Sure) with comprehensive metadata (IP, timestamps, device info, document embeddings). Mental model shift: evidence as facts to confirm/disconfirm risk predictions rather than friction.
**Documentation**: [UCPP Term](../resources/term_dictionary/term_ucpp.md)
**Wiki**: https://w.amazon.com/bin/view/Users/rickgari/Quip/BuyerAbusePreventionBAPAutomation2YearVisionOffsiteSeptember15-17EmailReadout/
**Track Ownership**: Evidence Intelligence (Shalmali Barki - Product, Kevin Peisker/Brijesh Dankara - Engineering)
**Processing Pattern**: DRFS (Notify → Ingest → Process → Store) with modular components
**Integration Points**: CAP workflows, Seller grading (BRW), A-to-Z claims, Advanced Detection
**Impact**: 60-80% reduction in manual evidence review, enables evidence-based PFOC/RFS suppression
**Related**: [VISTA](../resources/term_dictionary/term_vista.md), [CDP](../resources/term_dictionary/term_cdp.md), [CAP](../resources/term_dictionary/term_cap.md), [BRW](../resources/term_dictionary/term_brw.md), [DeepCARE](../resources/term_dictionary/term_deepcare.md)

### Elasticsearch - Distributed Search and Analytics Engine  
**Full Name**: Elasticsearch
**Description**: Distributed, RESTful search and analytics engine built on Apache Lucene with specialized k-NN plugin enabling efficient vector similarity search for machine learning applications. At Amazon, Elasticsearch serves as critical component in buyer abuse prevention through DeepCARE's investigation automation system, performing k-NN similarity search across millions of order vectors using HNSW algorithm via NMSLIB integration. Enables DeepCARE to automate 493K+ investigations with 90%+ precision through similarity-based consensus decisions using 440 neighbors for automated fraud detection. Provides low-latency search capabilities, event-based cluster updates, and comprehensive filtering ideal for fraud detection applications requiring sub-second similarity search across high-dimensional vector spaces.
**Documentation**: [Elasticsearch Term](../resources/term_dictionary/term_elasticsearch.md)
**Wiki**: [URES Similarity Search](https://w.amazon.com/bin/view/SellingPartnerServices/CoreServices/URESAutomation/SimilaritySearch/), [DeepCARE BAP](https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/DeepCARE/)
**BAP Application**: DeepCARE investigation automation (493K+ cases automated, 90%+ precision)
**Technical Integration**: k-NN plugin with HNSW/NMSLIB, EMR Spark cluster, Order2Vector DNN
**Performance**: Sub-second similarity search, 440 neighbors consensus voting, distributed scaling
**Key Benefits**: Real-time updates, comprehensive filtering, investigation automation, fraud detection
**Related**: [DeepCARE](../resources/term_dictionary/term_deepcare.md), [k-NN](../resources/term_dictionary/term_knn.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md), [Vector Database](../resources/term_dictionary/term_vector_database.md)

### FTS5 - Full-Text Search version 5
**Full Name**: SQLite Full-Text Search version 5
**Description**: SQLite's built-in extension that implements an inverted-index-backed virtual table type with native BM25 ranking, configurable Unicode-aware tokenizers (`unicode61`, `porter`, `ascii`), and snippet/highlight auxiliary functions. **Lives inside the same `.db` file as relational data**, so per-row INSERT/UPDATE/DELETE participate in the same SQL transaction as the rest of the schema — no separate index artifact, no rebuild cascade. Peer to Elasticsearch and OpenSearch in the inverted-index-plus-BM25 algorithm family but at embedded/personal-scale rather than distributed. In the slipbox vault context, the leading candidate to replace the standalone `bm25_index.pkl` artifact under FZ 5e1c3a1's unified-index proposal — collapsing four index artifacts into one file would close the COE-2026-04-29 sync-script Bug A surface area.
**Documentation**: [FTS5 Term](../resources/term_dictionary/term_fts5.md)
**Wiki**: [SQLite FTS5 official spec](https://www.sqlite.org/fts5.html)
**Slipbox Application**: Candidate replacement for `bm25_index.pkl` under FZ 5e1c3a1's unified-index proposal; already used by MeshClaw session-memory retrieval (`snippet_meshclaw_memory_fts5`)
**Key Benefits**: Atomic with row writes; single-file backup; native BM25; snippet/highlight for answer attribution; no extra dependency
**Related**: [Elasticsearch](../resources/term_dictionary/term_elasticsearch.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md), [Information Retrieval](../resources/term_dictionary/term_information_retrieval.md), [Dense Retrieval](../resources/term_dictionary/term_dense_retrieval.md), [Vector Database](../resources/term_dictionary/term_vector_database.md), [Tokenization](../resources/term_dictionary/term_tokenization.md)

### sqlite-vec - SQLite Vector Search Extension (vec0 Module)
**Full Name**: sqlite-vec (vec0 virtual-table module)
**Description**: Pure-C, dependency-free SQLite extension by Alex Garcia that adds vector storage and KNN search via the `vec0` virtual table module — the rewrite of his earlier `sqlite-vss` (which depended on FAISS). Stores `FLOAT[N]` / `INT8[N]` / `BIT[N]` vectors in chunked shadow tables inside the same `.db` file; supports cosine, L2, L1, and hamming distance metrics declared at table creation; integer rowid PK enables direct SQL JOIN to relational tables without an external mapping. **Sister extension to FTS5** in the SQLite ecosystem — same virtual-table pattern, same single-file design, paired in FZ 5e1c3a1's unified-index proposal as the dense arm of hybrid retrieval (sqlite-vec for cosine KNN, FTS5 for BM25 sparse). Exact KNN is sub-50ms at slipbox's 9k-note scale; HNSW available as an optional index type when the vault grows past ~50k notes.
**Documentation**: [sqlite-vec Term](../resources/term_dictionary/term_sqlite_vec.md)
**Wiki**: [sqlite-vec official docs](https://alexgarcia.xyz/sqlite-vec/) | [GitHub](https://github.com/asg017/sqlite-vec)
**Slipbox Application**: Candidate replacement for `note_embeddings.npy + note_ids_order.json` under FZ 5e1c3a1's unified-index proposal; the `note_int_id` integer surrogate from `notes` becomes the vec0 rowid, eliminating the JSON-sidecar reconciliation step
**Key Benefits**: Single-file backup; atomic with row writes; multiple distance metrics; INT8/BIT quantization for memory savings; metadata pre-filter inside the engine; no daemon, no external dependency
**Related**: [FTS5](../resources/term_dictionary/term_fts5.md), [FAISS](../resources/term_dictionary/term_faiss.md), [HNSW](../resources/term_dictionary/term_hnsw.md), [Vector Database](../resources/term_dictionary/term_vector_database.md), [Vector Quantization](../resources/term_dictionary/term_vector_quantization.md), [Embedding](../resources/term_dictionary/term_embedding.md), [Dense Retrieval](../resources/term_dictionary/term_dense_retrieval.md)

### Kendra - Amazon Kendra Intelligent Enterprise Search
**Full Name**: Amazon Kendra (Intelligent Enterprise Search Service)
**Description**: AWS's fully managed, AI-powered enterprise search service using machine learning and natural language processing to deliver highly accurate search results across organizational documents through semantic understanding rather than keyword matching. Provides cognitive search and question-answering capabilities across heterogeneous enterprise document collections via 40+ built-in data source connectors with contextual understanding for search, Q&A, and content ranking. At Amazon, Kendra serves as critical component for RAG workflows, enhancing LLM applications through semantic search for enterprise knowledge management systems like Digital Acceleration Knowledge Base, TroubleTracer incident management, and SFSC quality engineering platforms. Combines ML optimization with natural language processing to understand query intent and organizational semantics, particularly effective for enterprise environments requiring precise information retrieval.
**Documentation**: [Kendra Term](../resources/term_dictionary/term_kendra.md)
**Wiki**: [DA Knowledge Base](https://w.amazon.com/bin/view/DAEngineeringProductivity/KnowledgeBase/), [TroubleTracer Design](https://w.amazon.com/bin/view/Import_Ordering/QuipToWiki/TroubleTracer/TroubleTracer_-_High_Level_Design/)
**Key Features**: Semantic search, natural language queries, intelligent ranking, 40+ data connectors
**Applications**: Enterprise search, RAG context retrieval, knowledge management, automated incident response
**Amazon Usage**: DA Knowledge Base, TroubleTracer, SFSC quality engineering, Amazon Q Business integration
**vs Vector DB**: Higher accuracy semantic search through ML+NLP vs pure mathematical vector similarity
**Related**: [Amazon Q](../resources/term_dictionary/term_amazon_q.md), [RAG](../resources/term_dictionary/term_rag.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md), [Vector Database](../resources/term_dictionary/term_vector_database.md)

### Bedrock - Amazon Bedrock Foundation Model Platform
**Full Name**: Amazon Bedrock (Fully Managed Foundation Model Platform)
**Description**: AWS's fully managed foundation model platform providing access to high-performing LLMs and foundation models from Amazon (Nova family, Titan), Anthropic (Claude), Meta, Mistral AI, and others through unified API with enterprise security and RAG integration using OpenSearch as default vector database. At Amazon, serves as primary foundation model platform powering investigation automation (GreenTEA, AutoSignality), customer service enhancement (Amazon Q), fraud detection (SOPA, Guardian), and enterprise productivity tools. Enables organizations to build generative AI applications without infrastructure management while offering model selection, fine-tuning, and responsible AI capabilities. Strategic platform enabling next-generation automation through applications achieving significant cost savings (GreenTEA +9% AUC, AutoSignality $2.05MM).
**Documentation**: [Bedrock Term](../resources/term_dictionary/term_bedrock.md)
**Wiki**: [Bedrock LLM Models](https://w.amazon.com/bin/view/Users/krishsir/Quip/AmazonBedrock-LLMModels/), [Bedrock 101](https://w.amazon.com/bin/view/Users/sripads/Bedrock-101/)
**Model Portfolio**: Amazon Nova/Titan, Anthropic Claude, Meta Llama, Mistral AI, Stability AI
**Key Features**: RAG integration, vector database (OpenSearch), fine-tuning, responsible AI, multi-modal capabilities
**Amazon Applications**: GreenTEA (investigation automation), AutoSignality (fraud detection), Amazon Q (enterprise AI), SOPA (SOP compliance)
**Pricing**: Pay-per-use, $0.06-$12.50 per 1M tokens, enterprise volume discounts
**Related**: [Amazon Q](../resources/term_dictionary/term_amazon_q.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md), [LLM](../resources/term_dictionary/term_llm.md), [RAG](../resources/term_dictionary/term_rag.md)

### OpenSearch - Amazon OpenSearch Service
**Full Name**: Amazon OpenSearch Service
**Description**: AWS's fully managed, open-source search and analytics suite combining traditional search, real-time analytics, and vector search capabilities in a unified platform, serving as AWS's recommended vector database solution for generative AI applications. Built on the open-source OpenSearch project with integration to multiple ANN libraries (FAISS, NMSLIB, Lucene), achieving 30-35ms latencies for billions of vectors through horizontal sharding and AVX-512 acceleration. Evolved from early k-NN implementations to highly optimized vector search, positioning as AWS's primary vector database for RAG systems, semantic search, recommendation engines, and enterprise applications. Provides unified platform combining traditional keyword search with semantic vector search, enabling hybrid search capabilities and gradual AI adoption.
**Documentation**: [OpenSearch Term](../resources/term_dictionary/term_opensearch.md)
**Wiki**: [OpenSearch Vector Database](https://w.amazon.com/bin/view/Users/rupeshti/opensearch-vector-database/), [Vector Stores Comparison](https://w.amazon.com/bin/view/Users/amsamala/Quip/AWSVectorstorescomparison/)
**AWS Integration**: Default Bedrock vector database, Kendra integration, SageMaker embedding support
**Performance**: 30-35ms latency, billions of vectors, horizontal scaling, 4x speed improvement
**Applications**: RAG systems, enterprise search, observability, security analytics, vector database
**Key Benefits**: Fully managed, open source, hybrid search, cost optimized, enterprise ready
**Related**: [Vector Database](../resources/term_dictionary/term_vector_database.md), [FAISS](../resources/term_dictionary/term_faiss.md), [RAG](../resources/term_dictionary/term_rag.md), [Bedrock](../resources/term_dictionary/term_bedrock.md)

### Vector Database - Specialized Vector Storage and Search
**Full Name**: Vector Database (Vector DB)
**Description**: Specialized database system optimized for storing, indexing, and searching high-dimensional vector embeddings rather than traditional data types, enabling efficient similarity searches through Approximate Nearest Neighbor (ANN) techniques to quickly retrieve semantically similar vectors across massive datasets. At Amazon, vector databases power critical infrastructure including OpenSearch for enterprise search, Khoj for catalog similarity, Neptune for graph relationships, and RAG systems supporting generative AI applications across fraud detection, customer service automation, and knowledge management. Fundamental shift from structured queries to similarity-based retrieval where mathematical proximity corresponds to semantic similarity.
**Documentation**: [Vector Database Term](../resources/term_dictionary/term_vector_database.md)
**Wiki**: [RAG and Vector Databases Guide](https://w.amazon.com/bin/view/Users/mardiks/HeliosTechTalk/), [OpenSearch Vector DB](https://w.amazon.com/bin/view/Users/rupeshti/opensearch-vector-database/)
**AWS Services**: OpenSearch (hybrid search), Neptune (graph vectors), Bedrock Knowledge Bases
**Applications**: RAG systems, semantic search, recommendations, fraud detection, knowledge management
**Key Benefits**: Semantic search, real-time similarity, scalable infrastructure, ANN optimization
**Related**: [FAISS](../resources/term_dictionary/term_faiss.md), [RAG](../resources/term_dictionary/term_rag.md), [Embeddings](../resources/term_dictionary/term_embedding.md), [OpenSearch](../resources/term_dictionary/term_opensearch.md)

### VISTA - Verification of Images Through Algorithms
**Full Name**: Verification of Images Through Algorithms
**Description**: Amazon's computer vision service leveraging state-of-the-art ML (Vision Transformers, Deep Metric Learning) to generate insights from images for buyer abuse prevention. India-first service automating visual evidence validation across Cost of Business Waste (CBW) processes. Analyzes X-ray images (Secure Delivery), customer-uploaded evidence photos, and return item images to detect duplicate images, multi-account abuse, fake/AI-generated images, wrong item returns, and tampering. Provides quality assessment (blur, lighting, resolution), forgery detection (EXIF metadata, ELA), object recognition (item identification, condition assessment), and similarity matching across accounts. Proven 2.5bps NR concession savings (2022 pilot), targeting 11.5 bps / INR 1.2B CBW savings by 2025. Processes INR 4.1B concessions annually (42% of India total). Integrates with UCPP for evidence orchestration and CDP for storage/delivery. Core component of COAP (Context-Enhanced Abuse Prevention) enabling multi-modal evidence validation. Global expansion in progress from India to NA/EU markets.
**Documentation**: [VISTA Term](../resources/term_dictionary/term_vista.md)
**Wiki**: https://w.amazon.com/bin/view/InternationalCountryExpansion/A2I/AbusePreventionTech/Projects/VISTA/
**Ownership**: India CBW Tech team (in-cbw-techies), IES organization
**ML Technologies**: Vision Transformers (ViT), Deep Metric Learning, YOLOv5/v8, ResNet, Siamese Networks
**Use Cases**: NR concessions, Secure Delivery X-ray, MDR detection (BRW), Seller Grading photos, A-to-Z evidence, multi-account abuse
**Impact**: 60-80% reduction in manual image review time, estimated $50-100M annual savings at global scale
**Integration**: UCPP workflow orchestration, CDP storage/delivery, URES abuse evaluation, Paragon investigation display
**Related**: [UCPP](#ucpp---unified-content-processing-pipelines), [CDP](#cdp---content-delivery-platform), [BRW](../resources/term_dictionary/term_brw.md), [Advanced Detection](../resources/term_dictionary/term_ad.md), [COAP](../resources/term_dictionary/term_coap.md)

### Quick Spaces - Amazon Quick Spaces
**Full Name**: Amazon Quick Spaces
**Description**: Collaborative workspaces within QuickSuite that aggregate files, dashboards, topics, knowledge bases, and actions into a unified knowledge center for teams. Spaces serve as the **dynamic knowledge layer** for chat agents, grounding AI responses with team-specific data while maintaining permission-aware retrieval. Support up to 10,000 files (1 GB total) in 40+ formats including markdown, PDF, code, audio, and video.
**Documentation**: [Quick Spaces Term](../resources/term_dictionary/term_quick_spaces.md)
**AWS Docs**: https://docs.aws.amazon.com/quick/latest/userguide/working-with-spaces.html
**Related**: [QuickSuite](../resources/term_dictionary/term_quicksuite.md), [Quick Flows](#quick-flows---amazon-quick-flows--quick-automate)

### Quick Flows - Amazon Quick Flows & Quick Automate
**Full Name**: Amazon Quick Flows & Amazon Quick Automate
**Description**: Workflow automation capabilities within QuickSuite. Quick Flows provides interactive workflows combining generative AI processing with structured automation steps. Quick Automate provides streamlined tools for common business processes. **No-code AI workflow builder** connecting to 25+ enterprise applications via action connectors. Flows can be scheduled (daily/weekly/on-demand) and triggered from chat conversations with QuickSuite agents.
**Documentation**: [Quick Flows Term](../resources/term_dictionary/term_quick_flows.md)
**AWS Docs**: https://docs.aws.amazon.com/quick/latest/userguide/how-quicksuite-works.html
**Related**: [QuickSuite](../resources/term_dictionary/term_quicksuite.md), [SPICE](#spice---super-fast-parallel-in-memory-calculation-engine)

### SPICE - Super-fast, Parallel, In-memory Calculation Engine
**Full Name**: Super-fast, Parallel, In-memory Calculation Engine
**Description**: Robust in-memory analytics engine powering Amazon Quick Sight (part of QuickSuite). SPICE rapidly performs advanced calculations and serves data by caching imported datasets in memory, enabling sub-second query response for interactive dashboards. **Automatically replicates data for high availability** and scales to hundreds of thousands of concurrent users. Capacity is managed at the account level as a separate pricing dimension alongside user subscriptions.
**Documentation**: [SPICE Term](../resources/term_dictionary/term_spice.md)
**AWS Docs**: https://docs.aws.amazon.com/quick/latest/userguide/quicksight-terminology.html
**Related**: [QuickSuite](../resources/term_dictionary/term_quicksuite.md), [Redshift](../resources/term_dictionary/term_redshift.md)

### SMS - Short Message Service
**Full Name**: Short Message Service (Standard text messaging protocol)
**Description**: Text messaging service component using standardized protocols that allow mobile devices to exchange short messages (160 characters GSM 7-bit, 70 characters Unicode). **Technical Infrastructure**: Uses cellular network (GSM/CDMA/LTE), SMSC (SMS Center) for store-and-forward routing, no internet required, 98% delivery rate. **At Amazon**: Legitimate use cases include 2FA/OTP (login codes, account security via AWS SNS), order/delivery notifications (tracking updates, delivery alerts via short codes like 262966), customer service communications (case updates, surveys), promotional marketing (Prime Day, deal alerts - requires TCPA/GDPR opt-in), device setup (Alexa, Ring, Fire TV). **SMS Gateway**: AWS SNS handles sending (multi-carrier support, 99.99% SLA, pay-per-message pricing $0.00645 US to $0.50+ international), manages opt-out (STOP keywords), tracks delivery status via CloudWatch. **In BAP Context**: Off-platform communication abuse vector where bad actors attempt to redirect buyer-seller communications from BSMP to unmonitored SMS, enabling fraud (address redirect: $4.5M+ exposure, Amazon impersonation: $12M+ merchandise attempts, payment diversion, PII exposure). **Detection**: Real-time BSMP message scanning using regex patterns (97%+ accuracy for phone number detection) + BERT transformer models (context-aware classification), automated action (suppress message, append policy banner, queue for ARI review) via LEO workflow (<50ms latency). **Policy**: All buyer-seller communication must use BSMP - SMS redirect violations trigger Solicit-Warn-Close enforcement. **Comparison**: SMS vs MMS/iMessage/WhatsApp - SMS advantages are universal availability (all phones), no internet required, no app required, high reliability (98%), trusted channel; disadvantages are no encryption (plaintext), character limits, per-message cost. **Security Note**: SMS vulnerable to SIM swapping attacks for 2FA - authenticator apps (TOTP) preferred.
**Documentation**: [SMS Term](../resources/term_dictionary/term_sms.md)
**Technical Specs**: 160 chars (GSM 7-bit), 70 chars (Unicode), concatenated SMS up to 918 chars, <10s delivery typical
**AWS Infrastructure**: SNS (Simple Notification Service), E.164 phone format, sender ID support, transactional vs promotional types
**BAP Use Cases**: BSM abuse detection (COAP framework), A-Z Claim Abuse (Mar 2022 launch, 550K evals/week WW), Threat Abuse detection
**Key Challenge**: Balance legitimate Amazon SMS usage vs detecting abuse redirect attempts in BSMP
**Related**: [BSM](#bsm---buyer-seller-messaging), [Patronus](#patronus), [VoC](#voc---voice-of-customer), [ARI](../resources/term_dictionary/term_ari.md), [BSMP](../resources/term_dictionary/term_bsmp.md), AWS SNS, [2FA](../resources/term_dictionary/term_2sv.md)

### SWF - Simple Workflow Service
**Full Name**: Amazon Simple Workflow Service
**Description**: Fully managed AWS workflow orchestration service that coordinates distributed application components. **Separates orchestration logic (deciders) from business logic (activity workers)**, handling task scheduling, state persistence, retry logic, and event history. Supports long-running workflows up to 1 year. In BAP/SPS, used for Trusted Seller Submission (`TrustedSellerSubmissionWF` domain) and MPANoticeWorkflow. AWS Step Functions is the newer alternative, but SWF remains in use for legacy systems.
**Documentation**: [SWF](../resources/term_dictionary/term_swf.md)
**Related**: [SQS](../resources/term_dictionary/term_sqs.md), [SNS](../resources/term_dictionary/term_sns.md), [DDB](../resources/term_dictionary/term_ddb.md)

### ShipTrack - Shipment Tracking Service
**Full Name**: Shipment Tracking Service
**Description**: Amazon's authoritative source for providing the status of all packages shipped from Amazon FCs, Dropship nodes, or 3P sellers. Consumes package movement information from multiple internal sources (Delay Alarms, SSP, COMP, SPEC, Scan Insertion Tool, AMZL) and external sources (Carrier EDI and tracking APIs), surfacing status to downstream clients via scan events and APIs. **Core Components**: Status Processor Service (SPS - ingestion), Customer Tracking Service (aggregation), LUWAK (MFN manifest generation), MOMA (MFN scan pulling). **Communication Models**: Push (EventBus/SNS for real-time notifications) and Pull (Quick/Full APIs for on-demand queries). **BAP Critical Data Source**: (1) ShiptrackLineItem_v2 datastream - 55 events enriched with order info, stored in MDS; (2) ShipTrackEventHistory (STEH) - 258 events for PDA/DNR detection, 33.5M shipments and 300M events daily in NA. **BAP Use Cases**: DNR detection (delivery confirmation), PDA prevention (LIT/RTS patterns), QL abuse (SAN ML), Secure Delivery (OTP/TamperProof), Amazon Fresh delivery events. **Key Insight**: "79% of PDA falls in grey area between operational defect and abuse" - ShipTrack signals enable differentiation. **Key Events**: EVENT_201 (arrived at facility), EVENT_202 (departed facility), EVENT_302 (out for delivery), EVENT_303 (delivered), EVENT_304 (attempted), EVENT_972 (rejected).
**Documentation**: [ShipTrack Term](../resources/term_dictionary/term_shiptrack.md)
**Wiki**: https://w.amazon.com/bin/view/Transportation/ShipTrack/
**BAP Wiki**: https://w.amazon.com/bin/view/AbusePrevention/Abuse_ML/ShipTrack_Data_Sources/
**SNS Topic**: ShipmentStatusBroadcast (owned by GMP team)
**Owner**: GMP (Global Messaging Platform) - fo-all LDAP group
**Scale**: 33.5M shipments/day, 300M events/day (NA), 55 events (BAP datastream), 258 events (STEH)
**Status**: ✅ Active - critical data source for DNR, PDA, QL abuse detection
**Related**: [SPS](../resources/term_dictionary/term_sps.md), [TCDA](../resources/term_dictionary/term_tcda.md), [GMP](../resources/term_dictionary/term_gmp.md), [DNR](../resources/term_dictionary/term_dnr.md), [PDA](../resources/term_dictionary/term_pda.md), [MFN](../resources/term_dictionary/term_mfn.md), [AFN](../resources/term_dictionary/term_afn.md)

### SNS - Simple Notification Service
**Full Name**: Simple Notification Service (Amazon Web Services)
**Description**: AWS's fully managed pub/sub messaging service that serves as the event distribution backbone for BRP. Enables fan-out patterns where publishers send to topics and all subscribers receive messages. **BRP Primary Topics**: ShipmentStatusBroadcast (GMP team, 55-258 shipment events for DNR/PDA/QL), OWEN Events (order lifecycle), CROW Events (reversals/refunds), C-Returns Events (customer returns). **SNS + SQS Fan-Out Pattern**: Event Source → SNS Topic → Multiple SQS Queues → Different Consumers (APFNC, MDS, Analytics). **Key Features**: Message filtering (eventType, marketplaceId), message attributes, delivery policies with exponential backoff, DLQ for failed deliveries. **BRP Usage**: ShipmentStatusBroadcast is critical BAP data source - APFNC subscribes via SQS, stores 55 events in ShiptrackLineItem_v2 and 258 events in STEH for ML training. **Best Practices**: Use SQS subscribers for reliability, apply filter policies, enable SSE encryption.
**Documentation**: [SNS Term](../resources/term_dictionary/term_sns.md)
**AWS Docs**: https://docs.aws.amazon.com/sns/
**BRP Wiki**: https://w.amazon.com/bin/view/ShipTrack/ShipmentStatusMessageSubscription/
**Key Topics**: ShipmentStatusBroadcast (GMP), OWEN Events, CROW Events, C-Returns Events
**Key Metrics**: NumberOfMessagesPublished, NumberOfNotificationsFailed, PublishSize
**Status**: ✅ Active - central event distribution for abuse detection pipelines
**Related**: [SQS](../resources/term_dictionary/term_sqs.md), [APFNC](../resources/term_dictionary/term_apfnc.md), [ShipTrack](../resources/term_dictionary/term_shiptrack.md), [CROW](../resources/term_dictionary/term_crow.md), [OWEN](../resources/term_dictionary/term_owen.md), [GMP](../resources/term_dictionary/term_gmp.md)

### SQS - Simple Queue Service
**Full Name**: Simple Queue Service (Amazon Web Services)
**Description**: AWS's fully managed message queuing service that serves as foundational infrastructure for BRP's event-driven architecture. Enables decoupling and scaling of microservices by transmitting any volume of data without losing messages. **Queue Types**: Standard (unlimited TPS, at-least-once delivery, best-effort ordering) and FIFO (3K msgs/s, exactly-once, strict ordering). **BRP Primary Use Cases**: APFNC polls SQS queues for CROW/OWEN/C-Returns/ShipTrack events; ShipTrack SPS consumes carrier scans; URES/DWAR async evaluation triggering; LEO lifecycle events; MDS data ingestion. **SNS + SQS Fan-Out Pattern**: SNS publishes events → multiple SQS queues → different consumers (MDS storage, real-time evaluation, analytics). **Key Configuration**: Visibility timeout (30-120s), message retention (4-14 days), long polling (20s), Dead Letter Queue (DLQ) for failed messages. **Best Practices**: Idempotent processing, batch operations, DLQ monitoring, long polling.
**Documentation**: [SQS Term](../resources/term_dictionary/term_sqs.md)
**AWS Docs**: https://docs.aws.amazon.com/sqs/
**BRP Wiki**: https://w.amazon.com/bin/view/AbusePrevention/AbusePreventionFeedNotificationConsumer/
**Key Metrics**: ApproximateNumberOfMessagesVisible (queue depth), ApproximateAgeOfOldestMessage (latency), DLQ depth
**Status**: ✅ Active - foundational infrastructure for event-driven abuse detection
**Related**: [SNS](../resources/term_dictionary/term_sns.md), [APFNC](../resources/term_dictionary/term_apfnc.md), [ShipTrack](../resources/term_dictionary/term_shiptrack.md), [URES](../resources/term_dictionary/term_ures.md), [DWAR](../resources/term_dictionary/term_dwar.md), [LEO](../resources/term_dictionary/term_leo.md)

### ADES - Abuse Data Extraction Service
**Full Name**: Abuse Data Extraction Service
**Description**: Aggregates abuse-relevant data from multiple sources
**Related**: [AFN](../resources/term_dictionary/term_afn.md), [BAP](../resources/term_dictionary/term_bap.md)

### APFNC - Abuse Prevention Feed Notification Consumer [DEPRECATED]
**Full Name**: Abuse Prevention Feed Notification Consumer
**Status**: ⚠️ **DEPRECATED** (January 1, 2025) - Replaced by LEO (Lifecycle Event Orchestrator)
**Migration Path**: `APFNC` → `LEO`
**Description**: Legacy data ingestion service within Buyer Abuse Engineering that consumed notifications from multiple data feeds about customer behavior, enriching them for storage in MDS (Modeling Data Store) or triggering real-time abuse evaluations through DWAR/FORTRESS. Primary event processing gateway that polled pre-configured SQS queues (subscribed to SNS topics from CROW, OWEN, C-Returns, Shiptrack), filtered/enriched raw event data, published enriched data to MDS via Sable for ML training, and triggered real-time risk assessments via DWAR. Core responsibilities included Sable publishing, concession abuse evaluation, message context enrichment, and QL wheel reset logic. Java/Spring-based service with regional deployments (NA, EU, FE, CN). **Deprecation**: As of January 1, 2025, all new event processing workflows should use LEO. Existing APFNC pipelines remain operational for legacy workflows but are in maintenance mode only.
**Documentation**: [APFNC Term](../resources/term_dictionary/term_apfnc.md)
**Wiki**: https://w.amazon.com/bin/view/AbusePrevention/AbusePreventionFeedNotificationConsumer/
**Code**: https://code.amazon.com/packages/AbusePreventionFeedNotificationConsumer
**Event Sources**: CROW (refunds), OWEN (orders/shipments), C-Returns, Shiptrack
**Main Activities**: Sable publishing (MDS storage), DWAR/FORTRESS evaluation triggering, data enrichment
**Technology**: Java, Spring, AWS SQS/SNS, Sable, DataWave
**Replacement**: [LEO (Lifecycle Event Orchestrator)](#leo---lifecycle-event-orchestrator) - Use for all new workflows
**Status**: ⚠️ Deprecated (2025-01-01) - existing pipelines in maintenance mode
**Related**: [MDS](../resources/term_dictionary/term_mds.md), [OTF](../resources/term_dictionary/term_otf.md), [DWAR](../resources/term_dictionary/term_dwar.md), [FORTRESS](../resources/term_dictionary/term_fortress.md), [LEO](#leo---lifecycle-event-orchestrator), [AMES](../resources/term_dictionary/term_ames.md), [RMP](../resources/term_dictionary/term_rmp.md)

### DING - Data INGestion
**Full Name**: Data INGestion
**Description**: The ingestion service that bridges abuse data streams into MDS and OTF. When ingesting data via DING, you get both MDS (historical data store) and OTF (real-time variable population). **DING is the only current recommended method for ingesting data into MDS.** Operates via SNS → SQS subscription pattern. Used by all major abuse data streams (CReturn, OWEN, ShipTrack, BSM).
**Documentation**: [DING](../resources/term_dictionary/term_ding.md)
**Related**: [MDS](../resources/term_dictionary/term_mds.md), [OTF](#otf---on-the-fly), [LEO](#leo---lifecycle-event-orchestrator)



### EI - Evidence Intelligence
**Full Name**: Evidence Intelligence
**Description**: Unified evidence processing pipeline that validates evidence (police reports, delivery photos, product photos) from buyers and sellers. **Built on ORCA with DeepSea/UCPP ML models and RMP rulesets for automated grading.** Provides single integration per evidence source, consistent cross-channel validation, unified HITL mechanism, and consistent investigator tooling. Part of CAP 2.0 initiative.
**Documentation**: [Evidence Intelligence](../resources/term_dictionary/term_evidence_intelligence.md)
**Related**: [ORCA](#orca---center-of-excellence-for-orchestration), [LEO](#leo---lifecycle-event-orchestrator), [DING](#ding---data-ingestion)
### LEO - Lifecycle Event Orchestrator
**Full Name**: Lifecycle Event Orchestrator
**Description**: NAWS-based service within Buyer Abuse Engineering that simplifies and accelerates event ingestion, enrichment, and processing using declarative asynchronous workflows and automated infrastructure deployment. Created to break apart legacy systems like APFNC into smaller, more maintainable components. **Core Concepts**: (1) **Recipes** - individual workflow configurations defining event source, processing steps, output destinations; (2) **Common Operations** - 70+ reusable processing components for enrichment, transformation, storage, evaluation; (3) **Admin Control Panel** - web UI for recipe management and monitoring. **Event Sources**: CROW (refunds), OWEN (orders), ShipTrack (shipment status 55-258 events), C-Returns (customer returns), BSM (buyer-seller messaging). **Event Flow**: Source → LEO Recipe → Common Operations → MDS/OTF/DWAR/ARI. **SCC (Single Compute Container)**: Cost-optimized architecture using ECS Fargate delivering **76% cost reduction** vs Step Functions + Lambda ($295K vs $1.24M). Uses open-source Conductor orchestration engine with multi-runtime support (Java, TypeScript). First SCC production: ShipTrack 1.8K TPS (Dec 2023). **IMR Impact**: $512K/year CloudWatch savings (84% reduction). **Scale**: 60+ client use cases, 8+ teams within SPS. **Key Pipelines**: BuyerAbuseLEOPolicyDeployer (5977054), LifecycleEventOrchestrator (2416149), LEOAdminControlPanel (5235190), LEO-Monitoring (3862667). **BAP Use Cases**: ShipTrack STEH (300M+ events/day), OWEN processing, BSM analysis, C-Returns processing. **Migration Status**: LEO for all new workflows; APFNC maintained for stable production pipelines.
**Documentation**: [LEO Term](../resources/term_dictionary/term_leo.md)
**Wiki**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/LEO/
**Newsletter**: https://w.amazon.com/bin/view/TRMS/PolicyAbuse/LEO/Newsletter/December2023/
**Creator**: jadgage (Principal Software Engineer)
**Owner**: policy-engineering-dev (POSIX)
**Architecture**: NAWS-based declarative workflows + SCC (ECS Fargate + Conductor)
**Common Operations**: 70+ reusable components
**Client Use Cases**: 60+ across 8 teams
**SCC Cost Savings**: 76% reduction vs Step Functions/Lambda
**IMR Savings**: $512K/year CloudWatch costs
**Status**: ✅ Active - standard platform for new BAP event processing
**Related**: [APFNC](#apfnc---abuse-prevention-feed-notification-consumer), [MDS](../resources/term_dictionary/term_mds.md), [OTF](../resources/term_dictionary/term_otf.md), [DWAR](#dwar---deferred-write-ahead-request), [URES](#ures---unified-risk-evaluation-system), [ShipTrack](#shiptrack---shipment-tracking-service), [BSM](#bsm---buyer-seller-messaging)

### ORCA - Center of Excellence for Orchestration
**Full Name**: Center of Excellence for Orchestration
**Description**: Amazon's largest Tier-1, serverless, multi-tenant runtime for hosting workflows as serverless applications at Amazon scale. **BAP uses ORCA for Evidence Intelligence pipeline, SellerGrading (migrated from LEO), and enforcement workflows.** 600+ SDO teams use ORCA. Supports multiple DSLs (Herd XML, PDL, ASL, RUNWAY, KIS). Secure-by-default (RED, HIPAA, SOX, GDPR).
**Documentation**: [Term: ORCA](../resources/term_dictionary/term_orca.md), [Service: ORCA](../areas/services/svc_orca.md)
**Related**: [LEO](#leo---lifecycle-event-orchestrator), [EI Pipeline](../resources/data_sources/data_source_ei_pipeline.md)

### Helis - Authorization Service
**Full Name**: Helis Authorization Service
**Description**: Central policy management system for CDO scale. **Enables resource owners to restrict access to order document fields based on authorization attributes.** PCE uses Helis for consent evaluation — calling services send a token with LOB info, Helis calculates consent. OWEN was first BuyerAbuseLEO use case.
**Documentation**: [Helis](../resources/term_dictionary/term_helis.md)
**Related**: [PCE](../resources/term_dictionary/term_pce.md), [LEO](#leo---lifecycle-event-orchestrator)

### ReturnComet - Return Service
**Full Name**: ReturnComet Return Contract Service
**Description**: Provides RMA ID lookup and return contract management. **Called by CReturn LEO recipe for rmaId linkage and by ORC/CS for return resolution options** (GPURR and CCURR APIs). Key service in the concession creation journey.
**Documentation**: [ReturnComet](../resources/term_dictionary/term_returncomet.md)
**Related**: [CReturn](../resources/data_sources/data_source_creturn.md), [PCE](../resources/term_dictionary/term_pce.md)

### Sable - Aggregation Service
**Full Name**: Sable Aggregation Service
**Description**: Legacy variable aggregation service predating OTF. **Provides pre-computed aggregate variables used alongside OTF in some data streams.** CReturn executors output to both MDS and Sable. Being gradually replaced by OTF datasheets and FeatureHub.
**Documentation**: [Sable](../resources/term_dictionary/term_sable.md)
**Related**: [OTF](#otf---on-the-fly), [MDS](../resources/term_dictionary/term_mds.md)

### SCC - Single Compute Containerization
**Full Name**: Single Compute Containerization
**Description**: Culmination of LEO architecture advancements. **Consolidates LEO Compute Harness operations with Conductor OSS workflow engine in same ECS Fargate service, reducing costs by up to 78%.** Removes Lambda network hops. First use case: ShipTrack. Also used by OWEN, CReturn, SellerGrading.
**Documentation**: [SCC](../resources/term_dictionary/term_scc.md)
**Related**: [LEO](#leo---lifecycle-event-orchestrator), [ORCA](#orca---center-of-excellence-for-orchestration)

### TCDA - Transportation Container Data Aggregator
**Full Name**: Transportation Container Data Aggregator
**Description**: Service providing container-level and item-level data for shipments. **Used by ShipTrack LEO recipe for ASIN, GL, delivery station, heavy/bulky flag, OTP required, and tamper-proof packaging.** Has in-memory cache. PCE used as fallback when TCDA data is missing.
**Documentation**: [TCDA](../resources/term_dictionary/term_tcda.md)
**Related**: [GMP](#gmp---global-marketplace-platform), [PCE](../resources/term_dictionary/term_pce.md)
**Full Name**: Center of Excellence for Orchestration
**Description**: Amazon's largest **Tier-1, serverless, multi-tenant runtime** for hosting workflows as serverless applications at Amazon scale. Part of GRID (Global Runtime Infrastructure for Developers) under BuilderWorks. ORCA empowers developers to model and manage business process applications as workflows, event-driven architectures, and schedules without managing hosting infrastructure. **Proven Results**: 98% reduction in TCO, TTM, and MTTR by 600+ SDO teams (Ordering, Prime Video, Pharmacy, Kindle, Alexa, FCs, Kiva Robots, FBA, BDT, Payments, Tax, HR). **Recommended solution** in Workflow Orchestration Golden Path for SDO. **Execution Modes**: Async, Sync, Event-Driven, Schedule-Driven. **Hosting**: Multi-tenant cloud, dedicated engine, containerized in-memory. **Authoring**: XML, PDL, ASL, RUNWAY, Drag-and-Drop, Custom DSL. **Environment Support**: Native AWS + MAWS. **Foundation**: Built on Herd with capabilities from Kindle Integration Service, Legos, Torch, Jarvis. **BAP Integration**: One of three workflow engines for BAP alongside LEO and OLE - shares Common Actions framework (AbuseOLEBasicActionLambda) for enforcement workflows (account closure, FAPS annotation, email, retrocharge). Uses Context JSON passing model vs LEO's Step Functions.
**Documentation**: [ORCA Term](../resources/term_dictionary/term_orca.md)
**Wiki**: https://w.amazon.com/bin/view/Orchestration/ORCA/
**Golden Path**: https://docs.hub.amazon.dev/workflow-orchestration/golden-path-sdo/
**Owner**: herd (POSIX) - GRID / BuilderWorks
**Service Tier**: Tier-1
**Adoption**: 600+ SDO teams
**Efficiency**: Up to 98% TCO/TTM/MTTR reduction
**BAP Packages**: AbuseOLEBasicActionOrcaDefinitions, AbuseOLEBasicActionLambda
**Status**: ✅ Active - Amazon's recommended workflow orchestration platform
**Related**: [LEO](#leo---lifecycle-event-orchestrator), [FAPS](#faps---fraud-action-persistence-service), [URES](#ures---unified-risk-evaluation-system), [DWAR](#dwar---deferred-write-ahead-request)

### CBBFCS - Customer Browsing Behavior Feature Computation Service
**Full Name**: Customer Browsing Behavior Feature Computation Service
**Description**: Service computing behavioral features from customer browsing patterns. Generates signals for fraud detection models based on navigation, clicks, and session behavior.
**Documentation**: [CBBFCS Term](../resources/term_dictionary/term_cbbfcs.md)
**Related**: [ROCKS](../resources/term_dictionary/term_rocks.md), [OTF](../resources/term_dictionary/term_otf.md), [IS](../resources/term_dictionary/term_is.md)

### DFG - Domain Feature Generator
**Full Name**: Domain Feature Generator
**Description**: Service for generating domain-specific features for ML models. Provides standardized feature engineering capabilities.
**Documentation**: [DFG Term](../resources/term_dictionary/term_dfg.md)
**Wiki**: https://w.amazon.com/bin/view/CTPS/BRP/AI-RED/Services/DFG/
**Related**: [OTF](../resources/term_dictionary/term_otf.md), [AMES](../resources/term_dictionary/term_ames.md)

---

## Account & Identity Management

### CBAP - Confidence Based Authorization Platform
**Full Name**: Confidence Based Authorization Platform
**Description**: Platform that provides confidence-based authorization for customer actions. Enables graduated responses based on confidence levels.
**Documentation**: [CBAP Term](../resources/term_dictionary/term_cbap.md)
**Related**: [IS](../resources/term_dictionary/term_is.md), [ATO](../resources/term_dictionary/term_ato.md)

### RISC - Risk and Incident Sharing and Coordination
**Full Name**: Risk and Incident Sharing and Coordination/Communication
**Description**: Working group where Amazon and industry partners work to protect Amazon accounts. RISC shares information about important security events and enables users and providers to coordinate to securely restore accounts following compromise.
**Documentation**: [RISC Term](../resources/term_dictionary/term_risc.md)
**Wiki**: https://w.amazon.com/index.php/TRMSAccountIntegrity/RISC
**Related**: [IS](../resources/term_dictionary/term_is.md), [ATO](../resources/term_dictionary/term_ato.md), [Ajax](../resources/term_dictionary/term_ajax.md)

### TIV - Transaction Intent Verification
**Full Name**: Transaction Intent Verification
**Description**: New authentication method that not only provides assurance that user was involved with transaction, but also that the transaction was what the user intended. Enhanced security beyond traditional authentication.
**Documentation**: [TIV Term](../resources/term_dictionary/term_tiv.md)
**Wiki**: https://w.amazon.com/bin/view/IdentityServices/Mobile/Internal/Proposals/Transaction_Intent_Verification/
**Related**: [IS](../resources/term_dictionary/term_is.md), [OTP](../resources/term_dictionary/term_otp.md), [2SV](../resources/term_dictionary/term_2sv.md)

---

## Clustering & Network Analysis

### ACIS - Account Clustering Insight Service
**Full Name**: Account Clustering Insight Service (LINK 2.0)
**Description**: CoRe's (Core Relations) online service that vends **real-time relationship insights** for clients to make more-informed risk evaluation decisions against accounts and events. ACIS is the client-facing component of **LINK 2.0** ecosystem, replacing legacy services (LINKService, CCS). **OACIS (Offline ACIS)** is the batch counterpart. **Key Improvements over Legacy**: (1) Global relationships (vs regional - catches cross-region fraud), (2) Noise removal via DECIBEL (hub-node filtering improves traversal quality), (3) Fast signal onboarding (~2 weeks vs months), (4) 45% IMR reduction ($2.2M → $1M/year), (5) Precomputed + Fresh data (99% precomputed + real-time fresh). **Architecture**: ACIS (API) → RAS (Relationship Access Service) → ORAS (Offline-RAS) + Fresh data → DECIBEL (noise filtering) → Graphene (datalake). **19 Edge Types** (1095-day lookback: Bank Account, Credit Card, Email, Phone; 365-day: UBID, FUBID, Device ID, Address; plus normalized, Amazon Business signals). **Hub-node limit**: 200 (CID and attribute). **SLAs**: 750ms latency, 1.5% fault/failure rate across NA/EU/FE. **ASEDO → OACIS → ACIS Pipeline**: Scientists experiment in ASEDO → deploy to OACIS (offline production) → output to EDX → DataWave (RODB) → ACIS vends real-time insights. **BAP Use Cases**: MAA detection, IDA model scoring, PACMAN proactive prevention, LANTERN order-level PFOC, BCA scoring, ARI investigation lookups.
**Documentation**: [ACIS Term](../resources/term_dictionary/term_acis.md)
**Wiki**: [ACIS/LINK 2.0](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/ACIS_LINK2.0/), [CoRe User Guide](https://w.amazon.com/bin/view/Ohio/COreRElations/UserGuide/)
**Design Inspector**: https://design-inspector.a2z.com/#ILINK2_0
**Edge Types Dictionary**: https://w.amazon.com/bin/view/RAIn/Graphene/Vertices/
**Part Of**: LINK 2.0 ecosystem
**Offline Counterpart**: [OACIS (Offline ACIS)](#oacis---offline-account-clustering-insight-service)
**Replaces**: LINKService, CCS (Customer Clustering Service)
**Key Components**: RAS, ORAS, DECIBEL, EDS, ETS
**Edge Types**: 19 (payment, identity, device, address, Amazon Business)
**SLA**: 750ms latency, 1.5% fault rate
**IMR Cost**: ~$1M/year (45% reduction from legacy $2.2M)
**Key Innovation**: Global relationships, noise removal, configurable freshness/latency
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Status**: ✅ Active - primary relationship insight service
**Related**: [CCS](../resources/term_dictionary/term_ccs.md), [OACIS](#oacis---offline-account-clustering-insight-service), [GraMS](#grams), [GENIE](#genie), [Graphene](../resources/term_dictionary/term_graphene.md), [IDA](../resources/term_dictionary/term_ida.md), [PACMAN](../resources/term_dictionary/term_pacman.md), [MAA](../resources/term_dictionary/term_maa.md)

### ODESA - OfflineDEmocraticSAndbox
**Full Name**: OfflineDEmocraticSAndbox
**Description**: CoRe's (Core Relations) **graph analytics experimentation library** built on top of the Graphene relationship graph. ODESA simplifies gathering, transforming, generating features, and executing models against Amazon's massive **200+ billion edge, 57+ billion node** relationship dataset from sign-in events, payment instruments, tax identification, gift cards, refunds, and more. **ODESA is the experimentation platform** upstream of OACIS (offline production) and ACIS (online production). **Pipeline**: Loading Data → Traversal → Feature Generation → Model Execution → Rule/Filter. **Key Value**: (1) Efficiency - makes data gathering, traversals, feature engineering efficient for research/model training, (2) Scale - handles 200B+ edges on distributed EMR clusters, (3) Democratization - simplifies complex graph operations into reusable library functions, (4) Discovery - "The bad guys are working together" - aids discovery and sharing. **Capabilities**: Multi-region relationships (globally precomputed), unlimited attribute analysis (4.2M CIDs sharing single credit card), temporal clustering (10.5M customers in 1M clusters via 30-min windows), historical CCS scoring (133M CIDs, 3B scores in <3 hours vs >30 days via CCS UI), model retraining features. **Infrastructure**: Requires EMR clusters (32 r4.8xlarge recommended), Apache Spark, Eider notebooks (Scala primary, Python via conversion), 90-day snapshot retention. **ODESA → OACIS → ACIS Pipeline**: Scientists use ODESA to experiment → reuse code in OACIS (Cradle/Dryad) → results to EDX → if low-latency needed → DataWave → ACIS vends real-time. **BAP Use Cases**: Abuse Closure Model (ACM - traverse linked accounts, generate features, score risk), CCS cluster precomputation, buyer risk network detection, abuse neg-scoring, household model, new buyer risk model, EV2 variables. **Extended Edge Types**: Beyond standard ACIS edges, ODESA accesses THIRD_PARTY_REWARDS_ACCOUNT, CHINA_BANK_ACCOUNT, CARRIER_BILLING, IP, FINGERPRINT, KYC documents, GIFT_CARD variants, and 40+ more.
**Documentation**: [ODESA Term](../resources/term_dictionary/term_odesa.md)
**Wiki**: [ODESA Main](https://w.amazon.com/bin/view/ODESA/), [ODESA Learnings](https://w.amazon.com/bin/view/ODESA/learnings/)
**Training Video**: https://broadcast.amazon.com/videos/164750
**Onboarding SIM**: https://sim.amazon.com/issues/create?template=19d20b87-3664-4590-b42e-acc9b0cdea77
**Office Hours**: https://w.amazon.com/bin/view/Related_Accounts_Engineering/OfficeHours/
**Sage Q&A**: https://sage.amazon.com/tags/odesa
**Type**: Graph analytics experimentation library
**Data Source**: Graphene (200B+ edges, 57B+ nodes)
**Platform**: Apache Spark on EMR clusters (32 r4.8xlarge recommended)
**Notebook**: Eider (Scala primary, Python via conversion)
**Downstream**: OACIS (offline production), ACIS (online production)
**Access**: oacis-experiment-members LDAP, Odesa-Users team
**Python Support**: AnchorCatalogPython package for AWS SageMaker/Studio
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Primary Contact**: fetterst@
**Status**: ✅ Active - primary graph experimentation platform
**Related**: [OACIS](#oacis---offline-account-clustering-insight-service), [ACIS](#acis---account-clustering-insight-service), [Graphene](../resources/term_dictionary/term_graphene.md), [GENIE](#genie), [ACM](../resources/term_dictionary/term_acm.md), [CCS](#ccs---customer-clustering-service), [Anchor](../resources/term_dictionary/term_anchor.md)

### OACIS - Offline Account Clustering Insight Service
**Full Name**: Offline Account Clustering Insight Service
**Description**: CoRe's (Core Relations) **batch computation system** that supports clients with offline graph processing requirements to compute relationship insights. OACIS is a combination of **Libraries, Infrastructures, and Processes** optimized for running **offline/precomputed jobs on large data volumes** with daily data freshness trade-off. Together with ACIS (online), OACIS forms the **client-facing services of the LINK 2.0 ecosystem**. **ODESA → OACIS → ACIS Pipeline**: Scientists experiment in ODESA → reuse code in OACIS (Cradle/Dryad offline production) → results output to EDX → if low-latency needed, copy to RODB (DataWave) → ACIS vends real-time. **Shared Foundation**: Both ACIS and OACIS built around **Workflow Transactions Framework** for component reusability. **Primary Datasets**: (1) **IDA (Identity Association)** - next-gen identity scoring via `oacis/ida-scoring-daily/prod-global` for buyer/seller, (2) **CCS (legacy)** - precomputed clusters via `oacis/clusters-daily/prod-{na|eu|fe}` with marketplace-specific and compacted variants. **EDX Output Schemas**: clusters-daily (fromAccountId, toAccountId, score, datasetDate), compacted-entity-clusters (id, clusters JSON with edges, datasetDate), compacted-pairwise (pairwise with edges). **OTF Integration**: Pre-computed identity clusters available via OTF datastreams (TRMS.DataStream.EDX_IDENTITY_OACIS_CLUSTERS_{NA|EU|FE}). **BAP Use Cases**: IDA model training, BCA (Bad Customer Associated) batch scoring, PACMAN feature generation, MAA bulk investigation analysis, model evaluation/backtesting, Sugar Index aggregation. **OD3 Compliance**: 2-year retention for delta datasets, 3-month retention for snapshot datasets, excludes OD3 customers from new snapshots after 2 years.
**Documentation**: [OACIS Term](../resources/term_dictionary/term_oacis.md)
**Wiki**: [OACIS Main](https://w.amazon.com/bin/view/OACIS/), [LINK 2.0](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/ACIS_LINK2.0/)
**Onboarding SIM**: https://sim.amazon.com/issues/create?template=19d20b87-3664-4590-b42e-acc9b0cdea77
**Office Hours**: https://w.amazon.com/bin/view/Ohio/COreRElations/OfficeHours/
**Part Of**: LINK 2.0 ecosystem
**Online Counterpart**: [ACIS (Account Clustering Insight Service)](#acis---account-clustering-insight-service)
**Execution Platform**: Cradle/Dryad EMR jobs
**Primary Output**: EDX datasets (IDA, CCS clusters)
**Data Freshness**: 1 day
**Primary Datasets**: IDA (recommended), CCS (legacy)
**Regions**: NA, EU, FE (all regions supported)
**Access Roles**: oacis-experiment-members (experimentation), oacis-prod-access (production with SLA)
**OTF Integration**: Pre-computed clusters via datastreams
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Primary Contact**: nguyenna@
**Status**: ✅ Active - primary batch clustering service
**Related**: [ACIS](#acis---account-clustering-insight-service), [ODESA](../resources/term_dictionary/term_odesa.md), [GENIE](#genie), [Graphene](../resources/term_dictionary/term_graphene.md), [IDA](../resources/term_dictionary/term_ida.md), [BCA](../resources/term_dictionary/term_bca.md), [PACMAN](../resources/term_dictionary/term_pacman.md), [MAA](../resources/term_dictionary/term_maa.md), [EDX](../resources/term_dictionary/term_edx.md), [Cradle](../resources/term_dictionary/term_cradle.md)
**Wiki**: [ACIS/LINK 2.0](https://w.amazon.com/bin/view/Ohio/COreRElations/Disco/ACIS_LINK2.0/), [CoRe User Guide](https://w.amazon.com/bin/view/Ohio/COreRElations/UserGuide/)
**Design Inspector**: https://design-inspector.a2z.com/#ILINK2_0
**Edge Types Dictionary**: https://w.amazon.com/bin/view/RAIn/Graphene/Vertices/
**Part Of**: LINK 2.0 ecosystem
**Offline Counterpart**: OACIS (Offline ACIS)
**Replaces**: LINKService, CCS (Customer Clustering Service)
**Key Components**: RAS, ORAS, DECIBEL, EDS, ETS
**Edge Types**: 19 (payment, identity, device, address, Amazon Business)
**SLA**: 750ms latency, 1.5% fault rate
**IMR Cost**: ~$1M/year (45% reduction from legacy $2.2M)
**Key Innovation**: Global relationships, noise removal, configurable freshness/latency
**Owner Team**: CoRe (Core Relations) - ohio-engineering
**Status**: ✅ Active - primary relationship insight service
**Related**: [CCS](../resources/term_dictionary/term_ccs.md), [OACIS](../resources/term_dictionary/term_oacis.md), [GraMS](#grams), [GENIE](#genie), [Graphene](../resources/term_dictionary/term_graphene.md), [IDA](../resources/term_dictionary/term_ida.md), [PACMAN](../resources/term_dictionary/term_pacman.md), [MAA](../resources/term_dictionary/term_maa.md)

### CCS - Customer Clustering Service
**Full Name**: Customer Clustering Service
**Status**: ⚠️ **DEPRECATED** - Being replaced by ACIS/IDA
**Description**: Legacy service that groups related customer accounts using ML models trained on production data to replicate human investigator judgment. CCS provides a generic numeric model confidence score indicating whether accounts are related (not whether they're abusive), allowing clients to make business decisions about potential fraudulent or abusive behavior. **Key Distinction**: CCS determines if accounts are **related** (operated by same entity) - does NOT determine if abusive. **Architecture**: Client calls CCS with PrimaryCID → CCS calls LinkService → Pulls all attributes (CC, UBID, FUBID, DeviceID, email, phone, address) linked to CID → Returns related customers with model scores (0-1), relationship types, account status, cluster tags. **Cluster Variables**: Enables cluster-level evaluation (aggregating rejects, cancels, Sugar Index across all related accounts vs individual). **Why Deprecated**: Legacy architecture replaced by modern IDA model with better accuracy and real-time capabilities via ACIS service. **Migration**: Q1 2019 ownership transferred to RAE (Phoenix), 2021 IDA launched as successor.
**Documentation**: [CCS Term](../resources/term_dictionary/term_ccs.md)
**Wiki**: [Customer Clustering Service](https://w.amazon.com/bin/view/CustomerClusteringService), [CCS in Abuse Prevention](https://w.amazon.com/bin/view/TRMS/AbuseAnalytics/)
**Owner**: RAE (Related Accounts Enforcement) - Phoenix
**Successor**: [ACIS](#acis---account-clustering-insight-service), [IDA](../resources/term_dictionary/term_ida.md)
**Key API**: GetRelatedCustomers (customerID, marketplaceID → related CIDs, model scores, cluster tags)
**Relationship Attributes**: CC (24mo), UBID, FUBID, DeviceID, ResidenceID, Email, Phone, Address
**Status**: ⚠️ Deprecated - use ACIS/IDA for new work
**Related**: [ACIS](#acis---account-clustering-insight-service), [IDA](../resources/term_dictionary/term_ida.md), [MAA](../resources/term_dictionary/term_maa.md), [PACMAN](../resources/term_dictionary/term_pacman.md), [QL](../resources/term_dictionary/term_qla.md), [BCA](../resources/term_dictionary/term_bca.md), [PFW](../resources/term_dictionary/term_pfw.md)

### UAM - Unified Address Matching
**Full Name**: Unified Address Matching (also: NorthStar)
**Description**: Strategic initiative enhancing Amazon's ability to detect and prevent buyer abuse by significantly improving address matching capabilities across BAP and IDA systems. Leverages Geospatial team's NorthStar platform for advanced address normalization using Authoritative Address Sets (US) and deep learning models to find highest probability match. **Key Components**: (1) Address Catalog - centralized repository of normalized addresses used by OWEN/CROW for enrichment, (2) Improved IDA Edge - normalized address token replacing legacy ResidenceId for better account clustering, (3) CARS Integration - Core Address Resolution Service for address hierarchy entity mapping. **Problem Solved**: Same physical address can have hundreds of variations (recipient names, typos, unit formatting, munged characters) that evaded legacy ResidenceId matching. UAM normalizes all variations to single canonical form enabling accurate address-based rules, account clustering, and abuse pattern detection. **Architecture**: Customer Event Service (CES) → Address Service → CARS (normalization) → MDS (BAP) or Graphene (IDA via EntityTokenizationService). **Regional Coverage**: US, UK, DE, FR, ES (CARS live marketplaces).
**Documentation**: [UAM Term](../resources/term_dictionary/term_uam.md)
**Wiki**: https://w.amazon.com/bin/view/BuyerAbuse/Engineering/Teams/SAGE/Systems/BuyerAbuseUnifiedAddressMatching/
**Pipeline (BAP)**: https://pipelines.amazon.com/pipelines/BuyerAbuseUAM
**Pipeline (CoRe)**: https://pipelines.amazon.com/pipelines/CoReUnifiedAddressMatching
**Key Components**: Address Catalog (OWEN/CROW), IDA Edge (Graphene), CARS (address resolution)
**Problem Solved**: Address variations evading legacy ResidenceId matching
**Impact**: Significant increase in recall of related customer pairs while maintaining high precision
**Related**: [IDA](../resources/term_dictionary/term_ida.md), [MAA](../resources/term_dictionary/term_maa.md), [Graphene](../resources/term_dictionary/term_graphene.md), [Munged Address](../resources/term_dictionary/term_munged_address.md)

### MILLAP - Next-Gen Address Normalization Model
**Full Name**: MILLAP
**Description**: Next-generation address normalization model planned to replace [UAM](#uam---unified-address-matching). Offers improved geographic coverage (more marketplaces beyond US/UK/DE/FR/ES) and higher normalization rates compared to UAM's CARS/NorthStar platform. Key enabler for expanding [Address Intelligence](../areas/area_address_intelligence.md) variables to additional marketplaces worldwide.
**Documentation**: [MILLAP Term](../resources/term_dictionary/term_millap.md)
**Replaces**: [UAM](#uam---unified-address-matching) (Unified Address Matching)
**Improvements**: Better geographic coverage, higher normalization success rate, better international address formats
**Status**: 🔜 Planned — future migration
**Related**: [UAM](#uam---unified-address-matching), [Address Intelligence](../areas/area_address_intelligence.md), [Address Normalization](../resources/term_dictionary/term_address_normalization.md), [IDA](../resources/term_dictionary/term_ida.md)

### Address Normalization
**Full Name**: Address Normalization
**Description**: Process of converting free-form customer shipping addresses into a standardized canonical format, enabling accurate matching across address variations. Critical for abuse prevention because the same physical location can be represented hundreds of different ways (typos, abbreviations, unit formatting, recipient names). Currently implemented via [UAM](#uam---unified-address-matching) (CARS/NorthStar), with planned migration to [MILLAP](#millap---next-gen-address-normalization-model).
**Documentation**: [Address Normalization Term](../resources/term_dictionary/term_address_normalization.md)
**Current System**: [UAM](#uam---unified-address-matching) via CARS
**Future System**: [MILLAP](#millap---next-gen-address-normalization-model)
**Status**: ✅ Active — US, UK, DE, FR, ES (expanding)
**Related**: [UAM](#uam---unified-address-matching), [MILLAP](#millap---next-gen-address-normalization-model), [Munged Address](../resources/term_dictionary/term_munged_address.md), [Residence ID](../resources/term_dictionary/term_residence_id.md)

---

## Infrastructure & Monitoring

### Active-Passive - High Availability Standby Pattern
**Full Name**: Active-Passive (Primary-Standby)
**Description**: Active-passive is a high availability deployment pattern where a primary (active) node handles all traffic while one or more standby (passive) replicas remain idle, ready to take over if the primary fails. The standby node is continuously synchronized with the primary through data replication but does not serve client requests during normal operation. **Three standby modes — hot (fully loaded, instant failover), warm (running but requires state catch-up), and cold (powered off, requires boot and restore) — trade recovery speed for cost.** Active-passive is simpler than active-active because it avoids write conflict resolution, but it wastes standby resources during normal operation and introduces a failover delay proportional to the standby temperature. Common in database deployments (RDS Multi-AZ, PostgreSQL streaming replication) and stateful services.
**Documentation**: [Active-Passive](../resources/term_dictionary/term_active_passive.md)
**Related**: [Database Replication](../resources/term_dictionary/term_database_replication.md), [Fault Tolerance](../resources/term_dictionary/term_fault_tolerance.md), [Redundancy](../resources/term_dictionary/term_redundancy.md), [Availability](#availability---system-availability-in-distributed-systems)

### ALM - Amazon Local Marketplace
**Full Name**: Amazon Local Marketplace
**Description**: Amazon's platform for managing local marketplace stores and their attributes, including Amazon Fresh, Whole Foods, and other physical retail locations. ALM provides hierarchical store management with fulfillment configurations, regional store attributes, and multi-tenant capabilities supporting different store brands under unified platform. Critical data source for buyer abuse prevention through store exclusion logic and geographic analysis.
**Documentation**: [ALM Term](../resources/term_dictionary/term_alm.md)
**Wiki**: [ALM Stores Platform](https://w.amazon.com/bin/view/UltraFastGrocery/ALMStoresPlatform/)
**Data Table**: andes.almstores.dim_alm_store_attributes
**Status**: ✅ Active - core store management platform for local marketplace programs
**Related**: [UFG](../resources/term_dictionary/term_ufg.md), [Fresh](../resources/term_dictionary/term_fresh.md), [Whole Foods](../resources/term_dictionary/term_whole_foods.md)

### API Gateway - Unified Service Entry Point
**Full Name**: API Gateway
**Description**: An API gateway is an infrastructure component that serves as the single entry point for all client requests in a microservices architecture, routing them to appropriate backend services, aggregating results, and returning consolidated responses. **It decouples clients from internal service topology, analogous to the Facade pattern applied at the network level, providing a unified API surface while hiding internal service decomposition.** Core responsibilities include request routing, centralized authentication, rate limiting, protocol translation (REST to gRPC), response aggregation, and circuit breaking. A key design consideration is avoiding gateway bloat by restricting it to cross-cutting infrastructure concerns rather than business logic.
**Documentation**: [API Gateway](../resources/term_dictionary/term_api_gateway.md)
**Related**: [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Rate Limiting](../resources/term_dictionary/term_rate_limiting.md)

### AVS - Address Verification Service
**Full Name**: Address Verification Service (also: Address Verification System)
**Description**: Service that verifies billing address matches credit card on file. Key fraud prevention tool for payment risk.
**Documentation**: [AVS Term](../resources/term_dictionary/term_avs.md)
**Related**: Payment Risk, [BRI](../resources/term_dictionary/term_bri.md)

### BAU - Business As Usual
**Full Name**: Business As Usual
**Description**: Normal, routine operational activities and processes that keep systems running day-to-day, as opposed to special projects, new launches, or process changes. Includes daily investigation queues, routine monitoring, standard ticket handling, recurring communications, and ongoing maintenance. Healthy teams maintain 50-60% time for feature development, 20-30% for Operational Excellence, and only 10-20% for routine BAU activities. Warning signs: >50% BAU indicates need for automation, high KTLO burden signals tech debt accumulation. In BAP context: investigation operations (ARI queues, case reviews), system monitoring (dashboards, alarms, WBR metrics), routine maintenance (config updates, model refresh, data quality checks), regular communications (ABC guidelines: BAU reiteration with no process changes, submit by Wednesday 9PM for next week publication), and standard support (oncall duties, partner questions). Key distinction from other work: BAU maintains existing capabilities vs. launches (new features), process updates (SOP changes), or projects (innovation initiatives).
**Documentation**: [BAU Term](../resources/term_dictionary/term_bau.md)
**Wiki**: [Buyer Abuse Broadcast Committee](https://w.amazon.com/bin/view/Buyer_Abuse_-_Abuse_Broadcast_Committee/)
**Healthy Distribution**: 10-20% BAU, 20-30% OE, 50-60% Features
**BAU Activities**: Investigation queues, monitoring, maintenance, communications, support
**Not BAU**: New launches, process changes, special projects, system upgrades
**Related**: [KTLO](#ktlo---keep-the-lights-on), [OE](#oe---operational-excellence), [COE](../resources/term_dictionary/term_coe.md), [WFM](../resources/term_dictionary/term_wfm.md)

### BSF - Brazil Service Framework
**Full Name**: Brazil Service Framework
**Description**: Amazon's internal service hosting and management framework built on the Brazil build system. Provides standardized patterns for building, deploying, and operating RPC services with Coral communication, Apollo deployment, and CloudWatch monitoring. **Referenced in SIL service operations for inspecting service dependencies via BSFExplorerQueries.** Integrates with Amazon's service registry for endpoint resolution and standardized health check patterns.
**Documentation**: [BSF](../resources/term_dictionary/term_bsf.md)
**Wiki**: https://w.amazon.com/bin/view/CSCentral/Development/BSFExplorerQueries/
**Related**: [Brazil](../resources/term_dictionary/term_brazil.md), [SIL](../resources/term_dictionary/term_sil.md), [ORCA](../resources/term_dictionary/term_orca.md), [Apollo](../resources/term_dictionary/term_apollo.md)

### BI - Business Intelligence
**Full Name**: Business Intelligence
**Description**: Field of study encompassing data warehousing, ETL, big data, machine learning, dashboarding, reports, alerts, data quality assurance, master data management, data virtualization, and data engineering.
**Documentation**: [BI Term](../resources/term_dictionary/term_bi.md)
**Wiki**: https://w.amazon.com/index.php/Business%20Intelligence
**Related**: [MDS](../resources/term_dictionary/term_mds.md), [SAIS](../resources/term_dictionary/term_sais.md)

### CBB - Configurable Buy Box
**Full Name**: Configurable Buy Box
**Description**: System controlling which seller wins the Buy Box for a product. Critical for seller competitiveness and customer experience.
**Documentation**: [CBB Term](../resources/term_dictionary/term_cbb.md)
**Related**: [MFN](../resources/term_dictionary/term_mfn.md), [MRI](../resources/term_dictionary/term_mri.md)

### CDN - Content Delivery Network
**Full Name**: Content Delivery Network
**Description**: A CDN is a geographically distributed network of edge servers that delivers web content from locations physically closer to the requesting user, reducing latency, offloading origin bandwidth, and improving fault tolerance. **Edge servers at Points of Presence (PoPs) cache static assets and serve them on cache hits, fetching from the origin server only on cache misses, with cache invalidation managed through TTL expiration, purge APIs, cache tags, or versioned URLs.** Two delivery models exist: pull (on-demand origin fetch) and push (proactive content upload), with most production systems using a hybrid approach. Modern CDNs extend beyond caching to include DDoS mitigation, WAF capabilities, edge compute, and TLS termination.
**Documentation**: [CDN](../resources/term_dictionary/term_cdn.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [SSL Termination](../resources/term_dictionary/term_ssl_termination.md)

### Chaos Engineering - Resilience Through Fault Injection
**Full Name**: Chaos Engineering
**Description**: Chaos engineering is the discipline of experimenting on a distributed system to build confidence in its ability to withstand turbulent conditions in production, originated at Netflix with Chaos Monkey in 2011. **Unlike traditional testing that verifies known behaviors, chaos engineering discovers unknown weaknesses by injecting real-world failure modes (server termination, network partitions, resource exhaustion) into running systems and observing whether steady-state behavior is maintained.** The practice reduces MTTR by forcing teams to encounter and fix failure modes proactively, and is funded by the error budget derived from the SLO-SLA gap. Blast radius is controlled by starting with the smallest scope and expanding gradually, using canary analysis and automatic rollback.
**Documentation**: [Chaos Engineering](../resources/term_dictionary/term_chaos_engineering.md)
**Related**: [Error Budget](../resources/term_dictionary/term_error_budget.md), [MTTR](../resources/term_dictionary/term_mttr.md), [Graceful Degradation](../resources/term_dictionary/term_graceful_degradation.md), [Circuit Breaker](../resources/term_dictionary/term_circuit_breaker.md)

### Circuit Breaker - Cascading Failure Prevention
**Full Name**: Circuit Breaker
**Description**: The circuit breaker is a stability pattern that prevents an application from repeatedly invoking a failing remote service by wrapping calls in a proxy that monitors failures and short-circuits subsequent calls when a threshold is exceeded. **It operates as a three-state machine: Closed (normal, requests pass through), Open (tripped, requests fail immediately with fallback), and Half-Open (probing, limited trial requests test recovery).** Popularized by Michael Nygard in Release It! and widely adopted through Netflix's Hystrix library, the pattern embodies the principle that failing fast is better than failing slow. It complements other resilience patterns including retry with backoff, bulkheads, timeouts, and rate limiting.
**Documentation**: [Circuit Breaker](../resources/term_dictionary/term_circuit_breaker.md)
**Related**: [Graceful Degradation](../resources/term_dictionary/term_graceful_degradation.md), [Rate Limiting](../resources/term_dictionary/term_rate_limiting.md), [Health Check](../resources/term_dictionary/term_health_check.md)

### Consistent Hashing - Minimal-Disruption Data Partitioning
**Full Name**: Consistent Hashing
**Description**: Consistent hashing is a distributed hashing technique that maps both data keys and server nodes onto a circular hash space (hash ring), assigning each key to the nearest node in the clockwise direction. **Its defining property is minimal disruption: when a node is added or removed, only K/N keys on average need redistribution, compared to traditional modular hashing where nearly all keys must be remapped.** Virtual nodes (vnodes), typically assigned at a rate of one hundred to two hundred fifty-six per physical node, smooth load distribution and support heterogeneous clusters. The technique underpins data partitioning in systems such as DynamoDB, Apache Cassandra, and Akamai's CDN.
**Documentation**: [Consistent Hashing](../resources/term_dictionary/term_consistent_hashing.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Round Robin](../resources/term_dictionary/term_round_robin.md), [Scalability](../resources/term_dictionary/term_scalability.md)

### DNS - Domain Name Service
**Full Name**: Domain Name Service
**Description**: Internet service translating domain names to IP addresses. Core infrastructure component.
**Documentation**: [DNS Term](../resources/term_dictionary/term_dns.md)
**Related**: Infrastructure

### ECS - Elastic Container Service
**Full Name**: Amazon Elastic Container Service
**Description**: AWS's fully managed container orchestration service that runs Docker containers at scale using either Fargate (serverless) or EC2 launch types. Supports task definitions as declarative blueprints for container images, CPU/memory, networking, and IAM roles. **Deployment target for ORCA Edge containerized workflows and BAP model serving pipelines.** Integrates natively with ALB, CloudWatch, ECR, and VPC networking for production container workloads.
**Documentation**: [ECS](../resources/term_dictionary/term_ecs.md)
**Wiki**: https://docs.aws.amazon.com/ecs/
**Related**: [ECR](../resources/term_dictionary/term_ecr.md), [EKS](#eks---elastic-kubernetes-service), [ORCA Edge](../resources/term_dictionary/term_orca_edge.md), [CDK](../resources/term_dictionary/term_cdk.md)

### EKS - Elastic Kubernetes Service
**Full Name**: Amazon Elastic Kubernetes Service
**Description**: AWS's managed Kubernetes service that runs the control plane across multiple AZs without requiring operators to maintain their own clusters. Provides certified Kubernetes-conformant environment supporting standard tooling (kubectl, Helm, operators). **Deployment target for ORCA Edge and BAP teams requiring Kubernetes-native features like custom operators, service meshes, or GPU scheduling.** Supports managed node groups, self-managed nodes, and Fargate profiles for serverless pods.
**Documentation**: [EKS](../resources/term_dictionary/term_eks.md)
**Wiki**: https://docs.aws.amazon.com/eks/
**Related**: [ECS](#ecs---elastic-container-service), [ECR](../resources/term_dictionary/term_ecr.md), [ORCA Edge](../resources/term_dictionary/term_orca_edge.md), [CDK](../resources/term_dictionary/term_cdk.md)

### EventBridge - Amazon EventBridge
**Full Name**: Amazon EventBridge
**Description**: Serverless event bus service that connects applications using events routed from AWS services, custom applications, and SaaS partners. Uses rules with JSON-based event patterns for content-based routing to targets (Lambda, SQS, SNS, Step Functions). **Native ORCA connector for routing workflow events to IAM role-enabled event buses.** Includes Schema Registry for event discovery, Archive & Replay for compliance, and Scheduler for cron-based triggers.
**Documentation**: [EventBridge](../resources/term_dictionary/term_eventbridge.md)
**Wiki**: https://docs.aws.amazon.com/eventbridge/
**Related**: [SNS](../resources/term_dictionary/term_sns.md), [SQS](../resources/term_dictionary/term_sqs.md), [Lambda](#lambda---aws-lambda), [ORCA](../resources/term_dictionary/term_orca.md)

### Error Budget - Allowable Unreliability Threshold
**Full Name**: Error Budget
**Description**: An error budget is the maximum allowable threshold for errors or unreliability in a service, calculated as 1 minus the SLO target. **It transforms the subjective question "are we reliable enough?" into an objective, data-driven decision: if budget remains, ship features; if budget is exhausted, freeze changes and focus on reliability.** Error budget burn rate measures how fast the budget is consumed relative to steady-state, enabling multi-window alerting that balances detection speed against false positives. The concept originates from Google SRE and bridges the fundamental tension between development velocity and operational stability.
**Documentation**: [Error Budget](../resources/term_dictionary/term_error_budget.md)
**Related**: [SLO](../resources/term_dictionary/term_slo.md), [SLI](../resources/term_dictionary/term_sli.md), [MTTR](../resources/term_dictionary/term_mttr.md)

### Fault Tolerance - Continued Operation Despite Failures
**Full Name**: Fault Tolerance
**Description**: Fault tolerance is a system's ability to continue operating correctly — possibly at reduced capacity — despite the failure of one or more of its components, without requiring human intervention. A fault-tolerant system detects failures, isolates the faulty component, and recovers or reroutes around it automatically. **Fault tolerance uses techniques like redundancy (duplicate components), replication (data copies across nodes), circuit breakers (fail-fast to prevent cascading), graceful degradation (reduced functionality over total outage), and bulkheads (failure isolation boundaries).** The level of fault tolerance is measured by how many simultaneous failures the system can sustain while maintaining its service-level objectives. Designing for fault tolerance requires assuming that failures are inevitable and architecting accordingly.
**Documentation**: [Fault Tolerance](../resources/term_dictionary/term_fault_tolerance.md)
**Related**: [Redundancy](../resources/term_dictionary/term_redundancy.md), [Active-Passive](../resources/term_dictionary/term_active_passive.md), [Circuit Breaker](#circuit-breaker---cascading-failure-prevention), [Availability](#availability---system-availability-in-distributed-systems)

### Failover - Automatic Standby Switching
**Full Name**: Failover
**Description**: Failover is the automatic switching to a standby system when the primary one fails, serving as the mechanism that achieves high availability by minimizing MTTR. **The two dominant patterns are active-passive (standby takes over upon primary failure, with cold/warm/hot variants trading cost for recovery speed) and active-active (all nodes serve traffic simultaneously, eliminating failover delay but requiring conflict resolution for concurrent writes).** The split-brain problem, where network partitions cause both primary and standby to accept divergent writes, is one of the most dangerous failure modes, mitigated by fencing mechanisms like STONITH. Failover strategy directly drives the choice between RTO (recovery time) and RPO (acceptable data loss) targets.
**Documentation**: [Failover](../resources/term_dictionary/term_failover.md)
**Related**: [Health Check](../resources/term_dictionary/term_health_check.md), [MTTR](../resources/term_dictionary/term_mttr.md), [Graceful Degradation](../resources/term_dictionary/term_graceful_degradation.md)

### Graceful Degradation - Partial Failure Resilience
**Full Name**: Graceful Degradation
**Description**: Graceful degradation is a design principle where a system continues to operate at reduced functionality when some of its components fail, rather than failing completely. **The key technique is transforming hard dependencies into soft dependencies by defining fallback behavior for each failure scenario, such as serving cached data, disabling non-critical features, or returning default responses.** Strategies include feature shedding (disable non-essential features), load shedding (reject a percentage of requests), and quality reduction (serve lower-quality responses). It complements the circuit breaker pattern, which detects failures, while graceful degradation defines what happens after the circuit trips.
**Documentation**: [Graceful Degradation](../resources/term_dictionary/term_graceful_degradation.md)
**Related**: [Circuit Breaker](../resources/term_dictionary/term_circuit_breaker.md), [Failover](../resources/term_dictionary/term_failover.md), [SLO](../resources/term_dictionary/term_slo.md)

### Graph Database - Graph-Structured Data Store
**Full Name**: Graph Database
**Description**: A graph database is a database designed for storing, querying, and analyzing graph-structured data consisting of nodes (vertices) representing entities and edges representing relationships between them. Unlike relational databases that require expensive join operations to traverse relationships, graph databases store relationships as first-class citizens alongside the data. **Index-free adjacency enables O(1) relationship traversal regardless of data size, making graph databases dramatically faster than relational databases for relationship-heavy queries like social networks, fraud rings, and knowledge graphs.** Query languages include Gremlin (Apache TinkerPop), Cypher (Neo4j), and SPARQL (RDF). Examples include Neo4j, Amazon Neptune, and TigerGraph.
**Documentation**: [Graph Database](../resources/term_dictionary/term_graph_database.md)
**Related**: [NoSQL](../resources/term_dictionary/term_nosql.md), [MongoDB](#mongodb---document-oriented-nosql-database), [Neptune](#neptune)

### In-Memory Database - RAM-Resident Data Store
**Full Name**: In-Memory Database (IMDB)
**Description**: A database management system that stores data primarily in main memory (RAM) rather than on disk, achieving sub-millisecond latency by eliminating disk I/O from the read/write path. **In-memory databases are a caching and real-time tier in polyglot architectures — they complement persistent databases rather than replacing them.** Common systems include Redis (multi-model: strings, hashes, sorted sets, streams), Memcached (simple key-value), VoltDB (in-memory relational), and SAP HANA (hybrid columnar). Use cases include session storage, rate limiting, leaderboards, feature flags, and real-time analytics.
**Documentation**: [In-Memory Database](../resources/term_dictionary/term_in_memory_database.md)
**Related**: [Redis](../resources/term_dictionary/term_redis.md), [Memcached](../resources/term_dictionary/term_memcached.md), [Cache-Aside](../resources/term_dictionary/term_cache_aside.md), [Polyglot Persistence](../resources/term_dictionary/term_polyglot_persistence.md)

### Polyglot Persistence - Multi-Database Architecture Pattern
**Full Name**: Polyglot Persistence
**Description**: An architectural pattern where a single system uses multiple database technologies, each selected to handle the specific workload it serves best. Rather than forcing all data through one general-purpose database, the system routes each data type to the storage engine optimized for its access pattern. **The production norm for modern systems — typically 2-4 database types, each serving a distinct access pattern (e.g., PostgreSQL for transactions + Redis for caching + Elasticsearch for search + Cassandra for event streams).** Progressive adoption recommended: start with PostgreSQL, add specialized databases only when demonstrably needed.
**Documentation**: [Polyglot Persistence](../resources/term_dictionary/term_polyglot_persistence.md)
**Related**: [PostgreSQL](../resources/term_dictionary/term_postgresql.md), [Redis](../resources/term_dictionary/term_redis.md), [DynamoDB](../resources/term_dictionary/term_ddb.md), [Microservices Architecture](../resources/term_dictionary/term_microservices_architecture.md)

### Document Database - Schema-Flexible JSON/BSON Store
**Full Name**: Document Database (Document Store)
**Description**: A NoSQL database that stores data as semi-structured documents (JSON or BSON), where each document is a self-contained unit with its own structure. Unlike relational databases that enforce uniform schemas, document databases allow each document within a collection to have different fields, nested objects, and arrays. **The document model eliminates object-relational impedance mismatch and supports hierarchical data that would require multiple joined tables in a relational database.** Most document databases use LSM tree storage engines optimized for write-heavy workloads. Examples include MongoDB (dominant), CouchDB, Firestore, and Amazon DocumentDB.
**Documentation**: [Document Database](../resources/term_dictionary/term_document_database.md)
**Related**: [MongoDB](../resources/term_dictionary/term_mongodb.md), [NoSQL](../resources/term_dictionary/term_nosql.md), [LSM Tree](../resources/term_dictionary/term_lsm_tree.md), [Polyglot Persistence](../resources/term_dictionary/term_polyglot_persistence.md)

### Key-Value Store - Distributed Hash Table Database
**Full Name**: Key-Value Store (KV Store)
**Description**: A NoSQL database implementing the simplest data model: a mapping from unique keys to opaque values, providing O(1) average-case lookups and the highest throughput of any database category. The database treats values as black boxes — it does not parse, index, or query within the value. **Key-value stores trade query expressiveness for performance, making them ideal for caching, session storage, rate limiting, and real-time scoring where access is always by primary key.** Systems range from purely in-memory (Redis, Memcached) to fully persistent (DynamoDB). Consistent hashing enables linear horizontal scaling.
**Documentation**: [Key-Value Store](../resources/term_dictionary/term_key_value_store.md)
**Related**: [Redis](../resources/term_dictionary/term_redis.md), [DynamoDB](../resources/term_dictionary/term_ddb.md), [Memcached](../resources/term_dictionary/term_memcached.md), [In-Memory Database](../resources/term_dictionary/term_in_memory_database.md), [Cache-Aside](../resources/term_dictionary/term_cache_aside.md)

### RDBMS - Relational Database Management System
**Full Name**: Relational Database Management System
**Description**: A database system that stores data in structured tables with predefined schemas, enforces referential integrity through foreign keys, and provides SQL as a declarative interface for querying and manipulating data. RDBMS provides ACID compliance — every transaction is atomic, consistent, isolated, and durable. **The practical recommendation from system design literature is "start with PostgreSQL" — a well-tuned RDBMS handles far more workload than most engineers expect; specialized databases are introduced only when RDBMS demonstrably cannot serve a workload.** B-tree storage engines optimize for read-heavy workloads. Examples include PostgreSQL, MySQL, SQL Server, Oracle, and SQLite.
**Documentation**: [RDBMS](../resources/term_dictionary/term_rdbms.md)
**Related**: [PostgreSQL](../resources/term_dictionary/term_postgresql.md), [SQL](../resources/term_dictionary/term_sql.md), [ACID](../resources/term_dictionary/term_acid.md), [B-Tree](../resources/term_dictionary/term_b_tree.md), [Polyglot Persistence](../resources/term_dictionary/term_polyglot_persistence.md)

### GRC - Governance, Risk & Compliance
**Full Name**: Governance, Risk & Compliance
**Description**: Centralized tool for managing, assessing, and reporting on risks, issues, and compliance requirements across Amazon.
**Documentation**: [GRC Term](../resources/term_dictionary/term_grc.md)
**Wiki**: https://w.amazon.com/index.php/GRC
**Related**: Compliance, Risk Management

### HAProxy - High Availability Proxy
**Full Name**: High Availability Proxy
**Description**: HAProxy is a free, open-source load balancer and reverse proxy for TCP and HTTP applications, widely adopted as the industry-standard software load balancer by organizations including GitHub, Airbnb, and Twitter. **It operates at both Layer 4 (TCP) and Layer 7 (HTTP), with native first-class TCP proxying and extensive built-in load balancing algorithms including roundrobin, leastconn, source hash, and URI hash.** HAProxy uses ACL-based routing for content-aware traffic decisions and provides active health checks in the open-source version, unlike NGINX which restricts active checks to its commercial offering. It is often deployed alongside NGINX, with HAProxy handling dedicated load balancing while NGINX serves static content.
**Documentation**: [HAProxy](../resources/term_dictionary/term_haproxy.md)
**Related**: [NGINX](../resources/term_dictionary/term_nginx.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [SSL Termination](../resources/term_dictionary/term_ssl_termination.md)

### Health Check - Service Health Monitoring
**Full Name**: Health Check
**Description**: A health check is a mechanism for monitoring the operational status of services, servers, or infrastructure components, enabling load balancers to determine which backends can receive traffic. **Active health checks proactively send periodic probe requests (HTTP, TCP, gRPC) while passive health checks monitor real traffic responses to infer server health without dedicated probes.** In Kubernetes, three distinct probe types exist: liveness (is the process alive), readiness (can it accept traffic), and startup (has initialization completed). Best practice separates shallow checks (process responding) from deep checks (dependencies also healthy) to avoid cascading failures where a shared dependency marks an entire chain of services as unhealthy.
**Documentation**: [Health Check](../resources/term_dictionary/term_health_check.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Failover](../resources/term_dictionary/term_failover.md), [Circuit Breaker](../resources/term_dictionary/term_circuit_breaker.md)

### Hotspot - Disproportionate Traffic Partition
**Full Name**: Hotspot (Data Partition Hotspot)
**Description**: A hotspot is a partition or shard in a distributed system that receives disproportionately more traffic — reads, writes, or both — than other partitions, creating a bottleneck that degrades overall system performance and can trigger cascading failures. Hotspots emerge from skewed key distributions, temporal access patterns (e.g., all writes targeting today's partition), or celebrity/viral content concentrated on a single shard. **Hotspots are the primary anti-pattern in sharded systems, caused by low-cardinality shard keys, temporal patterns, or celebrity users generating outsized traffic on a single partition.** Mitigation strategies include key salting (appending random suffixes), write sharding (splitting hot keys across sub-partitions), adaptive partitioning, and caching hot keys. DynamoDB's adaptive capacity automatically redistributes throughput to hot partitions.
**Documentation**: [Hotspot](../resources/term_dictionary/term_hotspot.md)
**Related**: [Sharding](../resources/term_dictionary/term_sharding.md), [Consistent Hashing](#consistent-hashing---minimal-disruption-data-partitioning), [DynamoDB](../resources/term_dictionary/term_ddb.md)

### KTLO - Keep The Lights On
**Full Name**: Keep The Lights On
**Description**: Maintenance mode where teams focus on minimum activities necessary to keep existing systems operational without adding new features. Includes bug fixes, security updates, mandates, operational burden (SEVs, tickets, COEs), infrastructure maintenance, and monitoring. **⚠️ KTLO ≠ Deprecation** - services in KTLO still require operational excellence bar and customer support. Can be temporary (budget, transitions) or permanent (mature products). High KTLO burden (>50% team time) signals need for operational efficiency investment. For BAP: EDX is in KTLO mode (migrate to Andes); track KTLO time to balance maintenance vs innovation.
**Documentation**: [KTLO Term](../resources/term_dictionary/term_ktlo.md)
**Wiki**: https://w.amazon.com/bin/view/AWS/Teams/GlobalServicesSecurity/Engineering/KtloServices/
**Key Principle**: No new features - only essential maintenance to sustain current functionality
**Related**: [OE](../resources/term_dictionary/term_oe.md) (Operational Excellence), [EDX](../resources/term_dictionary/term_edx.md) (example in KTLO mode)

### Lambda - AWS Lambda
**Full Name**: AWS Lambda
**Description**: Serverless compute service that runs code in response to events without provisioning servers, scaling automatically from zero to thousands of concurrent executions with per-millisecond billing. Supports Node.js, Python, Java, Go, .NET, Rust, and container images up to 10 GB. **Native ORCA connector for invoking functions as workflow activities; used in BAP model pipelines (Nexus GNN event pipeline uses Kotlin/TypeScript Lambda stacks for real-time graph ingestion).** Triggered by 200+ AWS services including API Gateway, S3, DynamoDB Streams, SNS, SQS, EventBridge, and Kinesis.
**Documentation**: [Lambda](../resources/term_dictionary/term_lambda.md)
**Wiki**: https://docs.aws.amazon.com/lambda/
**Related**: [ORCA](../resources/term_dictionary/term_orca.md), [EventBridge](#eventbridge---amazon-eventbridge), [SNS](../resources/term_dictionary/term_sns.md), [SQS](../resources/term_dictionary/term_sqs.md), [CDK](../resources/term_dictionary/term_cdk.md)

### Latency - Per-Request Response Time
**Full Name**: Latency (Response Time)
**Description**: Latency is the time elapsed between initiating a request and receiving the response — the primary measure of responsiveness in distributed systems. **Latency is reported as percentile distributions (p50, p95, p99) rather than averages, because averages hide the experience of the worst-affected users.** In fan-out architectures, tail latency amplification means overall latency is bounded by the slowest backend service. Latency and throughput are complementary metrics — optimizing one often trades off against the other, formalized by Little's Law (L = λW).
**Documentation**: [Latency](../resources/term_dictionary/term_latency.md)
**Related**: [Throughput](../resources/term_dictionary/term_throughput.md), [SLO](../resources/term_dictionary/term_slo.md), [CDN](../resources/term_dictionary/term_cdn.md), [Cache-Aside](../resources/term_dictionary/term_cache_aside.md)

### Load Balancer - Traffic Distribution Component
**Full Name**: Load Balancer
**Description**: A load balancer is a networking component that distributes incoming client requests across a pool of backend servers to optimize resource utilization, maximize throughput, minimize latency, and prevent any single server from becoming a bottleneck. **Load balancers operate at Layer 4 (transport layer, routing by TCP/UDP metadata) or Layer 7 (application layer, making content-aware routing decisions based on HTTP headers, URLs, and cookies).** Common algorithms include round robin, least connections, IP hash, and consistent hashing. High availability is achieved through active-passive (failover with floating VIP) or active-active (simultaneous serving via DNS or BGP Anycast) configurations.
**Documentation**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md)
**Related**: [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [NGINX](../resources/term_dictionary/term_nginx.md), [HAProxy](../resources/term_dictionary/term_haproxy.md), [Health Check](../resources/term_dictionary/term_health_check.md)

### Memcached - Distributed In-Memory Caching System
**Full Name**: Memcached
**Description**: Memcached is a free, open-source, distributed in-memory key-value caching system designed to speed up dynamic web applications by reducing database load. Originally developed at LiveJournal in 2003, it stores arbitrary data (strings, objects) as key-value pairs entirely in RAM with no persistence or disk backing. **Memcached is simpler than Redis — it offers no persistence, no data structures beyond key-value, but is multi-threaded and relies on client-side consistent hashing for distribution across a cluster of independent nodes.** Each node operates independently with no inter-node communication, making the architecture horizontally scalable but requiring clients to handle data distribution. Memcached uses an LRU eviction policy and is widely deployed as a caching layer in front of databases and APIs.
**Documentation**: [Memcached](../resources/term_dictionary/term_memcached.md)
**Related**: [Redis](../resources/term_dictionary/term_redis.md), [Cache-Aside](../resources/term_dictionary/term_cache_aside.md), [Consistent Hashing](#consistent-hashing---minimal-disruption-data-partitioning), [LRU Cache](../resources/term_dictionary/term_lru_cache.md)

### Message Queue - Asynchronous Communication Buffer
**Full Name**: Message Queue
**Description**: A message queue is an asynchronous communication mechanism where a producer sends messages to an intermediary buffer and a consumer retrieves and processes them independently, decoupling components in time, space, and execution. **Each message is delivered to exactly one consumer (point-to-point), distinguishing queues from publish-subscribe systems where messages fan out to all subscribers.** Most production systems use at-least-once delivery with idempotent consumers, combined with dead letter queues to isolate poison messages that cannot be processed. Common implementations include Amazon SQS, RabbitMQ, and Apache ActiveMQ.
**Documentation**: [Message Queue](../resources/term_dictionary/term_message_queue.md)
**Related**: [API Gateway](../resources/term_dictionary/term_api_gateway.md), [Rate Limiting](../resources/term_dictionary/term_rate_limiting.md), [Scalability](../resources/term_dictionary/term_scalability.md)

### MTBF - Mean Time Between Failures
**Full Name**: Mean Time Between Failures
**Description**: MTBF is a reliability metric measuring the average elapsed time between inherent failures of a repairable system during normal operation, serving as the primary indicator of system reliability. **It directly feeds the availability formula A = MTBF / (MTBF + MTTR), linking reliability and recoverability into a single availability metric.** For systems with N components in series, composite MTBF decreases as components are added, while redundancy (parallel components) increases it. Google SRE practice argues that reducing MTTR is often more cost-effective than increasing MTBF, because failures in complex distributed systems are inevitable.
**Documentation**: [MTBF](../resources/term_dictionary/term_mtbf.md)
**Related**: [MTTR](../resources/term_dictionary/term_mttr.md), [Error Budget](../resources/term_dictionary/term_error_budget.md), [SLO](../resources/term_dictionary/term_slo.md)

### MTTR - Mean Time To Recovery
**Full Name**: Mean Time To Recovery
**Description**: MTTR is the average time required to restore a system to full operational status after a failure, computed as the sum of detection, diagnosis, repair, and verification phases. **Reducing MTTR is the most effective lever for improving system availability, especially at high-availability targets where increasing MTBF yields diminishing returns.** The acronym is overloaded, standing for Recovery (full outage duration), Repair (active fix time only), Respond (alert-to-resolution), or Resolve (including root cause elimination). Best practices for reducing MTTR include real-time monitoring, structured logging, automated rollback, feature flags, and blameless postmortems.
**Documentation**: [MTTR](../resources/term_dictionary/term_mttr.md)
**Related**: [MTBF](../resources/term_dictionary/term_mtbf.md), [Failover](../resources/term_dictionary/term_failover.md), [Chaos Engineering](../resources/term_dictionary/term_chaos_engineering.md), [SLI](../resources/term_dictionary/term_sli.md)

### NGINX - High-Performance Web Server and Reverse Proxy
**Full Name**: NGINX
**Description**: NGINX (pronounced "engine-x") is a high-performance, open-source web server, reverse proxy, load balancer, and HTTP cache created to solve the C10K problem of handling tens of thousands of concurrent connections efficiently. **Its asynchronous, event-driven, non-blocking architecture uses a master-worker process model where each worker runs an event loop via epoll/kqueue, enabling massive concurrency with minimal memory overhead.** NGINX is commonly deployed as the entry point in distributed systems, handling SSL termination, static file serving, request routing, rate limiting, and load balancing across backend application servers. It supports multiple load balancing algorithms including Smooth Weighted Round Robin (default), least connections, and IP hash.
**Documentation**: [NGINX](../resources/term_dictionary/term_nginx.md)
**Related**: [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [HAProxy](../resources/term_dictionary/term_haproxy.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [SSL Termination](../resources/term_dictionary/term_ssl_termination.md)

### OCI - Open Container Initiative
**Full Name**: Open Container Initiative
**Description**: Industry-standard specifications for container image formats and runtimes, established under the Linux Foundation. Defines three specs: Image (how images are built/distributed), Runtime (how containers execute), and Distribution (registry push/pull API). **ORCA Edge distributes its orchestration runtime as OCI-compliant container images via ECR**, ensuring consistent deployment across ECS, EKS, Docker-compose, and Kubernetes environments.
**Documentation**: [OCI](../resources/term_dictionary/term_oci.md)
**Wiki**: https://opencontainers.org/
**Related**: [ECR](../resources/term_dictionary/term_ecr.md), [ECS](#ecs---elastic-container-service), [EKS](#eks---elastic-kubernetes-service), [ORCA Edge](../resources/term_dictionary/term_orca_edge.md)

### OE - Operational Excellence
**Full Name**: Operational Excellence
**Description**: Commitment to build software correctly while consistently delivering great customer experience through scalable, reliable, resilient, efficient software. **Four Pillars**: (1) Design/Build - scalability, reliability, resilience, security, code quality; (2) Test/Verify - TDD, comprehensive testing, quality gates; (3) Operate - oncall, incidents, CI/CD, change management; (4) Improve with Metrics - monitoring, dashboards, continuous improvement. **Critical Relationship**: **OE investments reduce future KTLO burden** - proactive improvements (automation, refactoring, tech debt reduction) minimize reactive maintenance. Healthy balance: 50-60% features, 20-30% OE, 10-20% KTLO. Track DORA metrics: deployment frequency, lead time, MTTR, change failure rate. For BAP: Invest in automation (MODS/MIMS, CI/CD), observability (dashboards, alarms), tech debt reduction (migrations, refactoring) to reduce future KTLO burden.
**Documentation**: [OE Term](../resources/term_dictionary/term_oe.md)
**Wiki**: https://w.amazon.com/bin/view/EE/Learn/OE/ (comprehensive training)
**Key Philosophy**: "Operational Excellence is a proxy for customer experience" - Andy Jassy
**Related**: [KTLO](../resources/term_dictionary/term_ktlo.md) (maintenance that OE reduces), [CI/CD](../resources/term_dictionary/term_ci_cd.md), [DevOps](../resources/term_dictionary/term_devops.md)

### PMET - Performance Metrics
**Full Name**: Performance Metrics
**Description**: Amazon's performance monitoring and metrics tracking system used for service health monitoring, alarming, and operational excellence across Buyer Risk Prevention (BRP) and related services. PMET provides infrastructure for tracking system performance (latency P50/P99/P100, throughput, error rates, availability), alerting on anomalies via integration with Carnaval alarm aggregation, certificate expiration monitoring with Redfort, and supporting incident response with real-time dashboards and historical trend analysis. **Architecture Flow**: Service → PMET (metrics collection) → SYMON/CloudWatch (storage) → Carnaval (alarm aggregation) → Alerts/Dashboards. **BRP Use Cases**: URES/FORTRESS evaluation latency, AMES model scoring performance, OTF variable computation delays, RMP rule throughput, MODS training job metrics, SageMaker endpoint health, MIMS deployment status, ARI queue depths, CAP routing throughput, enforcement action success rates, data pipeline freshness. **Common Scenarios**: Certificate expiration alerts ("Resolving as everything in PMET and Redfort looks fine"), stuck orders investigation, latency spike analysis. **Best Practices**: Create role-specific dashboards for oncall engineers, tune alarm thresholds to minimize false positives, ensure PMET feeds Carnaval for unified alerting, include in WBR operational excellence reviews.
**Documentation**: [PMET Term](../resources/term_dictionary/term_pmet.md)
**Wiki**: [BRP Guardians Glossary](https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/Guardians/Glossary/)
**Integration**: Carnaval (alarm aggregation), SYMON (monitoring platform), CloudWatch (AWS metrics), Redfort (security/compliance)
**BRP Monitored Services**: URES, AMES, OTF, RMP, MODS, MIMS, SageMaker endpoints
**Key Use Cases**: Service health monitoring, certificate expiration tracking, incident response, WBR dashboards
**Status**: ✅ Active - critical infrastructure monitoring for BRP services
**Related**: [Carnaval](../resources/term_dictionary/term_carnaval.md), [OE](#oe---operational-excellence), [KTLO](#ktlo---keep-the-lights-on), [URES](#ures---unified-risk-evaluation-system), [AMES](#ames---active-model-execution-service)

### Rate Limiting - Request Throttling
**Full Name**: Rate Limiting
**Description**: Rate limiting is a technique that controls the number of requests a client can make to a service within a specified time window, rejecting excess requests with HTTP 429 responses. **Common algorithms include token bucket, leaky bucket, fixed window, and sliding window, each balancing burst tolerance against enforcement accuracy.** It serves three purposes: API protection against resource monopolization, fair usage enforcement across consumers, and DDoS mitigation at the edge. Rate limiters are typically deployed at the API gateway layer so blocked requests never reach backend services.
**Documentation**: [Rate Limiting](../resources/term_dictionary/term_rate_limiting.md)
**Related**: [API Gateway](../resources/term_dictionary/term_api_gateway.md), [Circuit Breaker](../resources/term_dictionary/term_circuit_breaker.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md)

### Redundancy - Intentional Component Duplication for Reliability
**Full Name**: Redundancy
**Description**: Redundancy is the intentional duplication of critical system components — servers, databases, network paths, or entire data centers — to increase reliability and ensure continued operation when individual components fail. Redundancy is the foundational mechanism that enables both high availability and fault tolerance in distributed systems. **Types include active-active (all replicas serve traffic simultaneously), active-passive (standby takes over on failure), N+1 (one spare for N active), geographic (cross-region replication), data (replicated storage), and network (multiple paths between endpoints).** The cost of redundancy scales with the level of protection: cold standby is cheapest, hot standby is moderate, and active-active with geographic distribution is most expensive. Redundancy must be combined with failure detection and automated failover to be effective.
**Documentation**: [Redundancy](../resources/term_dictionary/term_redundancy.md)
**Related**: [Fault Tolerance](../resources/term_dictionary/term_fault_tolerance.md), [Active-Passive](../resources/term_dictionary/term_active_passive.md), [Database Replication](../resources/term_dictionary/term_database_replication.md), [Availability](#availability---system-availability-in-distributed-systems)

### Reverse Proxy - Server-Side Request Forwarding
**Full Name**: Reverse Proxy
**Description**: A reverse proxy is a server that sits between clients and backend servers, intercepting client requests and forwarding them to appropriate backends while hiding server identity and topology from clients. **Unlike a forward proxy that acts on behalf of clients, a reverse proxy acts on behalf of servers, shielding them from direct internet exposure.** Core functions include load balancing, SSL/TLS termination, caching, compression, security filtering, and request routing. Common implementations include NGINX, HAProxy, Envoy, and cloud-managed load balancers like AWS ALB.
**Documentation**: [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [NGINX](../resources/term_dictionary/term_nginx.md), [API Gateway](../resources/term_dictionary/term_api_gateway.md)

### Round Robin - Sequential Load Distribution
**Full Name**: Round Robin
**Description**: Round Robin is the simplest and most widely used load balancing algorithm, cycling through available servers sequentially in a circular list to distribute incoming requests. **It is a static, stateless algorithm requiring only a single counter, with O(1) time complexity per routing decision.** Variants include Weighted Round Robin for heterogeneous backends and Smooth Weighted Round Robin (NGINX default) that interleaves requests to prevent bursts. Best suited for homogeneous backends with stateless, uniform-cost requests.
**Documentation**: [Round Robin](../resources/term_dictionary/term_round_robin.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [NGINX](../resources/term_dictionary/term_nginx.md), [Consistent Hashing](../resources/term_dictionary/term_consistent_hashing.md)

### Scalability - System Growth Capacity
**Full Name**: Scalability
**Description**: Scalability is a system's ability to handle increased workload by adding resources while maintaining acceptable performance, without requiring fundamental redesign. The two primary strategies are **vertical scaling (adding power to a single machine) and horizontal scaling (adding more machines), with modern distributed systems overwhelmingly favoring horizontal scaling** to avoid single-point-of-failure risks and transcend physical machine limits. Horizontal scaling introduces coordination complexity including data partitioning, consistency challenges, and service discovery. Scalability is distinct from elasticity, which is the ability to dynamically add and remove resources in response to real-time demand.
**Documentation**: [Scalability](../resources/term_dictionary/term_scalability.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Consistent Hashing](../resources/term_dictionary/term_consistent_hashing.md), [CDN](../resources/term_dictionary/term_cdn.md)

### Scatter-Gather - Parallel Distributed Query Pattern
**Full Name**: Scatter-Gather
**Description**: Scatter-gather is a distributed query pattern where a coordinator sends a request to all shards or partitions in parallel ("scatter"), each shard processes its local subset independently, and the coordinator collects and merges all partial results into a final response ("gather"). This pattern is the standard approach for queries that cannot be routed to a single shard, such as global searches, aggregations, or top-K queries across partitioned datasets. **Latency is bounded by the slowest shard (tail latency problem), which is mitigated by shard pruning to skip irrelevant partitions and push-down aggregation to reduce data transferred from each shard.** The pattern is used extensively in distributed databases and search engines including Amazon Redshift, Citus, Vitess, and Elasticsearch.
**Documentation**: [Scatter-Gather](../resources/term_dictionary/term_scatter_gather.md)
**Related**: [Sharding](../resources/term_dictionary/term_sharding.md), [Redshift](../resources/term_dictionary/term_redshift.md), [Citus](#citus---distributed-postgresql-extension), [Vitess](#vitess---mysql-horizontal-scaling-middleware)

### Session Persistence - Sticky Sessions
**Full Name**: Session Persistence (Sticky Sessions)
**Description**: Session persistence is a load-balancing technique that ensures all requests from a given client during a session are routed to the same backend server, preserving server-side session state without cross-server synchronization. **The most common method is cookie-based persistence, where the load balancer injects or reads a cookie identifying the target server.** Other methods include IP-based, URL-based, and TLS session ID routing. While useful for stateful applications, sticky sessions create tension with horizontal scalability by causing uneven load distribution and reduced fault tolerance; modern best practice favors stateless architectures with externalized session stores.
**Documentation**: [Session Persistence](../resources/term_dictionary/term_session_persistence.md)
**Related**: [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [Round Robin](../resources/term_dictionary/term_round_robin.md), [HAProxy](../resources/term_dictionary/term_haproxy.md)

### SLI - Service Level Indicator
**Full Name**: Service Level Indicator
**Description**: An SLI is a carefully defined quantitative measure of a specific aspect of the level of service provided, serving as the metric that SLOs are defined against. **The Google SRE Book recommends treating every SLI as the ratio of good events to total events, expressed as a proportion between 0% and 100%.** Common SLI types include availability (successful requests / total requests), latency (requests faster than threshold / total), throughput, and error rate. SLIs should be measured as close to the user experience as possible, preferring load-balancer or client-side metrics over server-side metrics.
**Documentation**: [SLI](../resources/term_dictionary/term_sli.md)
**Related**: [SLO](../resources/term_dictionary/term_slo.md), [Error Budget](../resources/term_dictionary/term_error_budget.md), [Health Check](../resources/term_dictionary/term_health_check.md)

### SLO - Service Level Objective
**Full Name**: Service Level Objective
**Description**: An SLO is an internal target value or range for a service level measured by an SLI, set stricter than the external SLA to provide an early-warning margin before contractual violations occur. **The gap between the SLO and 100% defines the error budget, which creates a shared framework balancing development velocity against operational stability.** When error budget is available, teams ship features; when exhausted, they freeze changes and focus on reliability. SLO-based multi-burn-rate alerting reduces alert fatigue while catching both acute incidents and slow degradation.
**Documentation**: [SLO](../resources/term_dictionary/term_slo.md)
**Related**: [SLI](../resources/term_dictionary/term_sli.md), [Error Budget](../resources/term_dictionary/term_error_budget.md), [MTTR](../resources/term_dictionary/term_mttr.md)

### SSL Termination - TLS Offloading
**Full Name**: SSL Termination (TLS Termination)
**Description**: SSL termination is the practice of decrypting TLS-encrypted traffic at a network boundary device, typically a load balancer or reverse proxy, so that backend servers receive and process only plaintext HTTP. **This offloads CPU-intensive cryptographic operations from application servers, centralizes certificate management, and enables Layer 7 inspection for WAF rules, bot detection, and abuse signal extraction.** Three TLS handling modes exist: termination (plaintext internally), passthrough (end-to-end encryption), and bridging (decrypt, inspect, re-encrypt). The primary security trade-off is plaintext internal traffic, mitigated by network segmentation or mTLS for internal communication.
**Documentation**: [SSL Termination](../resources/term_dictionary/term_ssl_termination.md)
**Related**: [Reverse Proxy](../resources/term_dictionary/term_reverse_proxy.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md), [NGINX](../resources/term_dictionary/term_nginx.md)

### Throughput - System Capacity Rate
**Full Name**: Throughput (QPS / TPS / RPS)
**Description**: Throughput is the amount of work a system completes per unit of time — the rate at which requests, transactions, or data units are successfully processed. Common units include queries per second (QPS), transactions per second (TPS), and requests per second (RPS). **Throughput is the primary capacity planning metric: it determines when horizontal scaling is needed, and Little's Law (L = λW) formally links throughput, latency, and queue depth.** Systems degrade gracefully as throughput approaches capacity until a saturation point, then collapse. Batching increases throughput by amortizing per-request overhead at the cost of per-item latency.
**Documentation**: [Throughput](../resources/term_dictionary/term_throughput.md)
**Related**: [Latency](../resources/term_dictionary/term_latency.md), [Scalability](../resources/term_dictionary/term_scalability.md), [Sharding](../resources/term_dictionary/term_sharding.md), [Load Balancer](../resources/term_dictionary/term_load_balancer.md)

### TPS - Transactions Per Second
**Full Name**: Transactions Per Second
**Description**: TPS is the standard unit for measuring system throughput in transactional workloads — the number of discrete operations a service completes per second. In buyer abuse prevention, TPS quantifies real-time processing capacity of risk evaluation services, ML model inference endpoints, and feature stores. **Every ML model registered in MMS declares Expected TPS per region, driving infrastructure provisioning and auto-scaling decisions.** TPS differs from QPS (read-only queries) in implying state changes; RPS is the most generic variant. Peak TPS during Q4 can reach 5-10x sustained levels.
**Documentation**: [TPS](../resources/term_dictionary/term_tps.md)
**Related**: [Throughput](../resources/term_dictionary/term_throughput.md), [Latency](../resources/term_dictionary/term_latency.md), [URES](../resources/term_dictionary/term_ures.md), [OTF](../resources/term_dictionary/term_otf.md), [Scalability](../resources/term_dictionary/term_scalability.md)

### Time-Series Database - Time-Stamped Sequential Data Store
**Full Name**: Time-Series Database (TSDB)
**Description**: A time-series database is a database system optimized for storing, querying, and analyzing time-stamped sequential data with high write throughput. TSDBs are purpose-built for workloads like metrics collection, IoT sensor data, financial ticks, and event logging where data arrives continuously and queries primarily involve time-range aggregations. **TSDBs use time-based partitioning and columnar compression for efficient storage and range queries, enabling orders-of-magnitude better performance than general-purpose databases for temporal workloads.** Retention policies automatically downsample or expire old data, and continuous queries pre-compute common aggregations. Examples include InfluxDB, TimescaleDB, Amazon Timestream, and Prometheus.
**Documentation**: [Time-Series Database](../resources/term_dictionary/term_time_series_database.md)
**Related**: [NoSQL](../resources/term_dictionary/term_nosql.md), [Redshift](../resources/term_dictionary/term_redshift.md)

### VPC - Virtual Private Cloud
**Full Name**: Amazon Virtual Private Cloud
**Description**: Logically isolated virtual network within AWS providing complete control over IP addressing, subnets, route tables, gateways, and security settings. Enables launching AWS resources in a defined network topology with public/private subnets across multiple AZs. **BAP infrastructure uses VPCs for Lambda-Cradle CDK stacks, SAIS sandbox environments, and model serving endpoints to ensure sensitive abuse detection data remains within controlled network boundaries.** Key components include security groups (stateful), NACLs (stateless), VPC endpoints (private AWS service access), and NAT gateways.
**Documentation**: [VPC](../resources/term_dictionary/term_vpc.md)
**Wiki**: https://docs.aws.amazon.com/vpc/
**Related**: [ECS](#ecs---elastic-container-service), [EKS](#eks---elastic-kubernetes-service), [Lambda](#lambda---aws-lambda), [CDK](../resources/term_dictionary/term_cdk.md)

### Wide-Column Store - Column-Family NoSQL Database
**Full Name**: Wide-Column Store
**Description**: A wide-column store is a NoSQL database that organizes data by column families rather than rows, allowing each row to have a different set of columns and enabling efficient storage and retrieval of sparse, high-cardinality datasets. **Derived from Google's Bigtable paper (2006), wide-column stores store data in column families with dynamic columns per row, combining the row-key lookup efficiency of key-value stores with the columnar scan efficiency needed for analytical queries.** Data is sorted by row key within each column family, enabling efficient range scans. Wide-column stores excel at time-series data, event logging, and workloads requiring massive write throughput with flexible schemas. Examples include Apache Cassandra, Apache HBase, and Google Cloud Bigtable.
**Documentation**: [Wide-Column Store](../resources/term_dictionary/term_wide_column_store.md)
**Related**: [Cassandra](../resources/term_dictionary/term_cassandra.md), [NoSQL](../resources/term_dictionary/term_nosql.md), [DynamoDB](../resources/term_dictionary/term_ddb.md)

### Write-Around Cache - Database-Direct Write Strategy
**Full Name**: Write-Around Cache
**Description**: Write-around cache is a cache write strategy where writes go directly to the database, bypassing the cache entirely, so cached data is only populated when a subsequent read miss triggers a lazy load from the database. This approach prevents cache pollution from write-heavy workloads where written data is rarely read immediately. **Write-around reduces cache pollution for write-heavy workloads by only populating cache on read misses (lazy loading), making it ideal for logging, audit trails, and batch ingestion where immediate read-back is uncommon.** The trade-off is higher read latency for recently written data since it must be fetched from the database on the first read. Write-around is often combined with TTL-based expiration to manage eventual consistency.
**Documentation**: [Write-Around Cache](../resources/term_dictionary/term_write_around_cache.md)
**Related**: [Write-Through Cache](../resources/term_dictionary/term_write_through_cache.md), [Write-Back Cache](../resources/term_dictionary/term_write_back_cache.md), [Cache-Aside](../resources/term_dictionary/term_cache_aside.md), [Cache Invalidation](../resources/term_dictionary/term_cache_invalidation.md)

---

## Logistics & Delivery Infrastructure

### AMZL - Amazon Logistics
**Full Name**: Amazon Logistics
**Description**: Amazon's own courier/delivery service responsible for last-mile delivery of packages to customers. Critical partner for Buyer Abuse Prevention, particularly for Secure Delivery features (OTP, Signature Required) that reduce Delivered Not Received (DNR) concessions. AMZL provides the delivery infrastructure that enables proof-of-delivery verification, with drivers using the Flex App (Rabbit) to validate OTP codes and capture delivery confirmation. **DNR Scale (2021)**: 0.15% AMZL shipments resulted in DNR concession (US), 0.17% (EU); $310M US, $150M EU annualized DNR concessions disbursed. **Customer Abuse**: ~15% of DNR concessions, grew 67% YoY in Q1'22. **Customer Experience Impact**: DEX PRR drops from 82.3% (all AMZL) to 9.3% (DNR defect shipments) - DNR severely erodes customer trust. **OTP Secure Delivery**: At checkout, SDS flags high-risk items via DWAR/FORTRESS → Delivery Station receives SD treatment → Out-for-Delivery email sends 6-digit OTP to customer → DA arrives, requests OTP → Customer provides code → DA validates in Flex App → Delivery confirmed with proof-of-delivery. **OTP vs Signature**: OTP is **2.5x better** at preventing DNR defects - requires actual customer to verify vs any signature (can be forged/unclear). **OTP Markets**: UK, FR, DE, IT, ES, UAE, IN (live); US (piloting Q3-Q4'22). **Expected Savings**: $22M (attended markets) + $22M (US) + $5M (CA/AU) = $49M+ annually. **Driver Performance**: DNR DPMO (Defects Per Million) is key input to driver framework - OTP creates proof protecting good drivers from false DNR claims. **Driver Types**: Flex DPs (gig workers), DSP Drivers (Delivery Service Partner employees), DAs (generic term). **Partner Teams**: BRP (ML models), SDS (Secure Delivery feature), CAP (post-delivery concessions), WWDE (defect elimination), DEX (customer experience), LMT (driver apps/Rabbit), REX (notifications). **Coverage**: US, UK, DE, FR, IT, ES, IN, JP, UAE, SA, EG, CA, MX, AU, SG plus 3P carriers (UPS, FedEx, USPS, Royal Mail, DPD, Hermes). **SDS owns OTP only for AMZL deliveries** - non-AMZL carriers have separate implementations.
**Documentation**: [AMZL Term](../resources/term_dictionary/term_amzl.md)
**Wiki**: https://w.amazon.com/bin/view/SecureDelivery/, https://w.amazon.com/bin/view/SecureDelivery/OTP/
**Key Stats**: 0.15% DNR rate (US), $310M annual concessions, 2.5x OTP effectiveness vs Signature
**Driver App**: Flex App (Rabbit) - OTP verification at delivery
**Driver Types**: Flex DPs (gig), DSP (contracted), DA (generic)
**OTP Markets (Live)**: UK, FR, DE, IT, ES, UAE, IN
**OTP Markets (Planned)**: US, CA, AU
**Savings Potential**: $49M+ annually from OTP
**Key Insight**: AMZL is execution layer for Secure Delivery - drivers verify OTP at doorstep creating proof-of-delivery chain
**Related**: [SD](../resources/term_dictionary/term_secure_delivery.md), [SDS](../resources/term_dictionary/term_sds.md), [OTP](../resources/term_dictionary/term_otp.md), [DNR](../resources/term_dictionary/term_dnr.md), [CAP](../resources/term_dictionary/term_cap.md), [BRP](../resources/term_dictionary/term_brp.md), [LMT](../resources/term_dictionary/term_lmt.md), [AFN](../resources/term_dictionary/term_afn.md)

### LMT - Last Mile Technology
**Full Name**: Last Mile Technology
**Description**: Amazon's execution system and technology organization that controls the receipt, planning, and assignment of shipments for last mile Delivery Stations. LMT owns the technology products enabling drivers to deliver packages to customers, including the Rabbit/Flex App mobile application, routing systems, station operations technology, and driver safety systems. **Key Teams**: Amazon Flex (gig delivery), DSP Tech (Delivery Service Partner management), Routing & Planning (route optimization), Driver Experience (Rabbit/Flex App), Driver Safety & DAT, UTR Tech (Station Tech), Geospatial (LMOT - maps/navigation), EBT (Ship With Amazon, AMXL), Amazon Hub (Lockers), PRISM (program management), REALM (operational excellence), LMXD (design/research). **BRP Integration Critical**: LMT is the **execution layer for Secure Delivery (SD)** features - when BRP ML models flag high-risk items at checkout, LMT's Rabbit/Flex App prompts drivers to request and validate OTP codes at doorstep, creating cryptographic proof-of-delivery that prevents fraudulent DNR claims. **OTP Flow**: SDS flags via DWAR/FORTRESS → Delivery Station stages SD package → Out-for-Delivery email sends OTP → DA arrives, requests OTP → Customer provides code → DA validates in Flex App → Delivery confirmed. **OTP Effectiveness**: 2.5x better than signature at preventing DNR defects. **DNR Impact**: 0.15% AMZL shipments result in DNR (US), $310M annual concessions; OTP expected to save $49M+ annually. **Leader**: Beryl Tomay (reports to Udit Madan, VP Middle Mile and Last Mile).
**Documentation**: [LMT Term](../resources/term_dictionary/term_lmt.md)
**Wiki**: https://w.amazon.com/bin/view/Last_Mile_Employee_Hub/OrgOverview/, https://w.amazon.com/bin/view/Last_Mile_Technology/Glossary/

### LMDT - Last Mile Delivery and Technology
**Full Name**: Last Mile Delivery and Technology
**Description**: Amazon's comprehensive organization focused on building safe, sustainable, and convenient delivery experiences through innovative last-mile delivery solutions. LMDT encompasses 326 Tier-1 services supporting package delivery from delivery stations to customers' doorsteps, including core teams like DEX (Delivery Experience), Amazon Flex, DSP, AMZL, and Geospatial/Routing. The organization provides the technological foundation for secure delivery features and delivery verification systems that help distinguish legitimate delivery issues from fraudulent abuse claims. LMDT integrates delivery programs, underlying technology, and support services to drive innovation in customer delivery interactions across 20+ countries with 2,500+ delivery stations globally.
**Documentation**: [LMDT Term](../resources/term_dictionary/term_lmdt.md)
**Leader**: Beryl Tomay (VP, Last Mile Delivery Tech), Udit Madan (VP, Last Mile and Delivery Experience)
**Teams**: [DEX](../resources/teams/team_lmdt_dex.md), [AMZL](../resources/teams/team_amzl.md), Amazon Flex, DSP
**Parent Org**: Middle Mile and Last Mile (Udit Madan)
**Key Product**: Rabbit/Flex App (driver mobile application)
**BRP Integration**: OTP Secure Delivery validation at doorstep
**Key Teams**: Flex, DSP Tech, Routing, Driver Experience, Station Tech, Geospatial, Hub
**Abuse Prevention Role**: Proof-of-delivery for DNR prevention via OTP validation
**OTP Effectiveness**: 2.5x better than signature
**Status**: ✅ Active - critical partner for Secure Delivery abuse prevention
**Related**: [AMZL](../resources/term_dictionary/term_amzl.md), [SD](../resources/term_dictionary/term_secure_delivery.md), [SDS](../resources/term_dictionary/term_sds.md), [OTP](../resources/term_dictionary/term_otp.md), [DNR](../resources/term_dictionary/term_dnr.md), [BRP](../resources/term_dictionary/term_brp.md), [AFN](../resources/term_dictionary/term_afn.md)

### DSP - Delivery Service Partner (Last Mile)
**Full Name**: Delivery Service Partner
**Description**: Amazon's network of professional, independent contract delivery companies that power Amazon's in-house last mile delivery service (AMZL). DSPs are small business owners who operate their own delivery companies, managing fleets of vans and teams of **Delivery Associates (DAs)** who deliver Amazon packages to customers. **Vision**: "To be the world's best owner-operated business opportunity, empowering small business owners to build a better life for themselves, their associates, and their communities by operating safe, high quality, and sustainable logistics companies." **Program Versions**: DSP 1.0 (legacy - existing logistics companies, non-branded vehicles) and DSP 2.0 (flagship - business-in-a-box, Amazon-branded Armada vans, Value Added Services). **Key Teams**: DSP Product & Tech (Logistics Portal), DSP Business Coach Program, DSP Experience & Development, DSP Relations & Risk, Last Mile Payments. **BRP Integration Critical**: DSPs execute **Secure Delivery (SD)** features - their DAs use Rabbit/Flex App to validate OTP codes, capture proof-of-delivery photos, and execute delivery procedures that prevent **DNR** abuse. **DA Role in OTP**: DA arrives → Flex App prompts OTP request → Customer provides code → DA validates → Delivery confirmed with proof. **Key Metrics**: DNR DPMO (Defects Per Million), Concession Rate, OTP Compliance, Photo Compliance, DSP Scorecard. **DA Violations**: T1 Offboarding for Customer Delivery Escalations (CDEs), concessions investigations, safety violations, policy violations. **Comparison**: DSP DAs are employees of small business owners with regular routes vs Flex DPs are independent contractors with flexible blocks. **Training Video**: Eric Swanson DSP Intro (https://broadcast.amazon.com/videos/376088, 10 min).
**Documentation**: [DSP Term (Delivery)](../resources/term_dictionary/term_dsp.md)
**Wiki**: https://w.amazon.com/bin/view/LastMileDeliveryAndTechnology/DSP/, https://w.amazon.com/bin/view/DSP_Technical_Product/
**Model**: Small business owners managing Delivery Associates (DAs)
**Program Versions**: DSP 1.0 (legacy), DSP 2.0 (flagship - business-in-a-box)
**Key Platform**: Logistics Portal
**DA App**: Rabbit/Flex App (OTP validation, delivery confirmation)
**Vehicle Program**: Armada (Amazon-branded vans)
**Key Metric**: DNR DPMO (Defects Per Million Opportunities)
**BRP Integration**: Execute Secure Delivery at doorstep via OTP validation
**Abuse Prevention Role**: Proof-of-delivery to prevent fraudulent DNR claims
**Status**: ✅ Active - critical partner for last mile Secure Delivery execution
**Related**: [LMT](../resources/term_dictionary/term_lmt.md), [AMZL](../resources/term_dictionary/term_amzl.md), [SD](../resources/term_dictionary/term_secure_delivery.md), [OTP](../resources/term_dictionary/term_otp.md), [DNR](../resources/term_dictionary/term_dnr.md), [SDS](../resources/term_dictionary/term_sds.md)

### OBD - Open Box Delivery
**Full Name**: Open Box Delivery
**Description**: Amazon India's premium delivery service where Delivery Associates unbox and inspect products at the customer's doorstep using systematic six-side verification protocols guided by the Rabbit Application. Enhanced with VISTA computer vision integration for automated fraud detection and quality verification, OBD enables immediate rejection of defective products while documenting delivery condition through comprehensive image capture. The service achieves $6MM projected NCRC savings through proactive defect identification and prevention of fraudulent damage claims, transforming reactive issue resolution into transparent quality assurance at the point of delivery.
**Documentation**: [OBD Term](../resources/term_dictionary/term_obd.md)
**Coverage**: India marketplace exclusive (expanding to AE, EG, SA by 2026)
**Product Focus**: HCTP (High Consideration Technical Products), electronics, appliances
**VISTA Integration**: Q1-2026 deployment for automated verification
**Business Impact**: $6MM NCRC savings through quality assurance and fraud prevention
**Related**: [VISTA](../resources/term_dictionary/term_vista.md), [AMZL](../resources/term_dictionary/term_amzl.md), [Advanced Detection](../resources/term_dictionary/term_ad.md), [NCRC](../resources/term_dictionary/term_ncrc.md)

### SWA - Shipping With Amazon
**Full Name**: Shipping With Amazon (also: Amazon Shipping, Ship with Amazon)
**Description**: Amazon's transportation and logistics service offering shipping capabilities to third-party shippers and marketplace sellers. Provides end-to-end logistics including pickup, transportation, and delivery with integrated claims processing for lost/damaged shipments. BAP integration through SWA claims data (andes.swa_ppe.swa_claims_event_history) contributing to cross-program abuse detection and customer risk assessment with fraud detection capabilities.
**Documentation**: [SWA Term](../resources/term_dictionary/term_swa.md)
**Claims System**: SWAClaimsAndRefunds with automated fraud detection
**Team**: PPE (Post Purchase Experience)
**Data Table**: andes.swa_ppe.swa_claims_event_history
**Related**: [AMZL](../resources/term_dictionary/term_amzl.md), [LMT](../resources/term_dictionary/term_lmt.md), [DSP](#dsp---delivery-service-partner-last-mile), [Transportation](../resources/term_dictionary/term_transportation.md), [BAP](../resources/term_dictionary/term_bap.md)

> **Note**: Fulfillment network entries (FBA, AFN, MFN) are in [Abuse Vectors & Networks Glossary](acronym_glossary_abuse_networks.md#fulfillment-networks)

---

## Supporting Services

### RSPR - Risk Stratification and Policy Recommendation
**Full Name**: Risk Stratification and Policy Recommendation
**Description**: CAP's flagship investigation tool that automates risk assessment and policy recommendation for handling potentially abusive customer service contacts. Displays customer risk bands (0-9), provides guided investigation workflows, and recommends specific policy actions (grant, friction, deny, safelist, refer to ARI) based on abuse vector and risk severity. Synthesizes multiple signals: BAP ML model scores, ARI enforcement history, Sugar Index, account clusters. Transforms CAP from subjective investigation to standardized, data-driven policy application.
**Documentation**: [RSPR Term](../resources/term_dictionary/term_rspr.md)
**Wiki**: [SDS CAP Detection](https://w.amazon.com/bin/view/SDS-PDX/CapDetection/), [CAP Main Wiki](https://w.amazon.com/bin/view/ConcessionsAbusePrevention/)
**Owner**: SDS (platform), CAP Programs (operations)
**Access**: Via CAP Website in CS Central/AC3 order details page
**Key Features**: Risk bands (0-9), policy recommendations, guided workflows, investigation support, documentation automation
**Business Impact**: +490 bps policy adherence, -8.7% AHT (52 sec faster), $14MM concession savings
**Coverage**: US, CA, EU5, JP, IN (expanding to MX, BR, AU, MENA)
**Future**: CAP 2.0 - Evidence Intelligence, Policy Orchestrator, Disposition Decision Engine
**Related**: [CAP](../resources/term_dictionary/term_cap.md), [CAP Routing](../areas/area_cap_routing.md), [CDA](../resources/term_dictionary/term_cda.md), [OTF](../resources/term_dictionary/term_otf.md)

**Description**: Centralized action persistence service owned by the Saitama team (BRI) that records and persists all fraud and abuse-related enforcement actions taken on various entity types (Buyer, Order, Payment, Cluster) across BRP. Serves as the single source of truth for enforcement history, supporting ad-hoc queries on historical fraud action data. FAPS enables auditability, reproducibility, and historical analysis of fraud and abuse prevention decisions. **Tier-2 service** classified Red in Anvil (called by Tier-1 services like Fortress, Fraud Service). Data retention: **24 months** since creation. **Client Services**: Abuse Prevention, Fraud Prevention, Concession, QL Abuse, Triton Outcome Processor, CARDS, FBS. **Data Consumers**: APIs (real-time), DataWarehouse (offline analysis), SNS Events (downstream processing), WhyTool UI (investigation lookup at https://whytool.amazon.com/).
**Documentation**: [FAPS Term](../resources/term_dictionary/term_faps.md)
**Wiki**: https://w.amazon.com/bin/view/Armory/FAPS/FraudActionPersistenceService/, https://w.amazon.com/bin/view/Saitama/FraudActionPersistenceService/
**Runbook**: https://w.amazon.com/bin/view/SpartaDev/Runbooks/FAPS/
**WhyTool UI**: https://whytool.amazon.com/
**Owner**: Saitama Team (saitama-team) - BRI
**On-Call**: twinpeak
**Service Tier**: Tier-2 (Red in Anvil)
**Data Retention**: 24 months
**Key APIs**: RecordFraudAction, GetFraudActions, GetFraudActionsByType, SearchFraudActions
**Object Types**: Buyer, Order, Payment, Cluster
**Status**: ✅ Active - central action persistence for BRP enforcement
**Related**: [CARDS](../resources/term_dictionary/term_cards.md), [TOP](../resources/term_dictionary/term_top.md), [APWS](../resources/term_dictionary/term_apws.md), [ATS](../resources/term_dictionary/term_ats.md), [FORTRESS](#fortress---fraudulent-order-reduction-through-risk-evaluation-at-super-speed-legacy), [FBS](../resources/term_dictionary/term_fbs.md), [ARI](../resources/term_dictionary/term_ari.md)

### MU Bot - MessageUs Bot
**Full Name**: MessageUs Bot (Automated Concession Bot)
**Description**: Amazon's automated CS bot handling concession requests through the MessageUs (chat) channel. **Performs two-stage abuse check: whether to auto-grant concessions, and where to route if not auto-granting.** Integrates with CAP risk signals via CAPDataService (migrated from Carnac). A systemic gap was identified in the Repeat Abuse program where CAP checks were missing for CA, IN, BR, MX marketplaces — fixed July 2024. Chat channel is the primary RFC leakage vector (76% of CS-leaked RFC).
**Documentation**: [MU Bot Term](../resources/term_dictionary/term_mu_bot.md)
**Wiki**: https://w.amazon.com/bin/view/CAPTech/CS_Tapas/Projects/2021/Optimization/Phase4_MessageUs_Abuse_Check/
**Related**: [CAP](../resources/term_dictionary/term_cap.md), [RFC](../resources/term_dictionary/term_rapid_fire_concession.md), [CSMO](../resources/term_dictionary/term_csmo.md)

### MONRAD - Investigation Case/Task Management Service
**Full Name**: MONRAD (Investigation Case/Task Management Service)
**Description**: Multi-tenant case and task management service for investigation workflows, built around the **investigate-act** paradigm. Orchestrates investigations by managing task lifecycles (PENDING→QUEUED→ASSIGNED→REVIEWED→PROCESSED→COMPLETED), routing work to investigators via GlobalACD (GACD), and recording outcomes. Uses **Case-WorkUnit-Task** model where Tasks are business-agnostic containers for WorkUnits grouped under Cases.
**Documentation**: [MONRAD Term](../resources/term_dictionary/term_monrad.md)
**Wiki**: https://w.amazon.com/bin/view/InvestigationPlatform/Monrad/
**Design**: https://w.amazon.com/bin/view/InvestigationPlatform/Monrad/Design/
**Coral Service**: https://coral.amazon.com/MonradCaseService/NA/Prod/explorer
**Owner**: Investigation Platform (Armory team)
**Architecture**: Case → Task → WorkUnit hierarchy
**Lifecycle**: PENDING → QUEUED → ASSIGNED → REVIEWED → PROCESSED → COMPLETED (or HOLD/ABORTED)
**Key APIs**: RequestWork (create), GetTask, UpdateTask, LookupTasks, SearchTasks
**Notification**: SNS topics, GlobalACD (GACD) routing
**Data Tables**: O_MONRAD_TASK_HISTORY, STG_INVG_TARGET_MONRAD
**Legacy Replacement**: IWCase/IWTask APIs
**Status**: ✅ Active - core investigation orchestration for BRI/ARI
**Related**: [Nautilus](../resources/term_dictionary/term_nautilus.md), [Paragon](../resources/term_dictionary/term_paragon.md), [GOQU](../resources/term_dictionary/term_goqu.md), [FAPS](#faps---fraud-action-persistence-service), [ARI](../resources/term_dictionary/term_ari.md), [BRI](../resources/term_dictionary/term_bri.md)

### FBS - Fortress Backend Service
**Full Name**: Fortress Backend Service
**Description**: Post-evaluation processing service owned by the URES team that handles activities after FORTRESS/URES completes a risk evaluation. Serves as the critical bridge between evaluation decisions and downstream action-taking systems. **Key Responsibilities**: (1) Produce metrics - generate evaluation statistics, (2) Sideline orders - queue for manual investigation when rules dictate, (3) Idempotency persistence - ensure evaluation consistency, (4) Publish results - send outcomes via SNS to external systems. **SNS Publishing**: V1 (legacy, consumed by APWS - deprecated path) and V2 (current standard, consumed by LEO). **Investigation Flow**: FBS publishes → Monrad Case Service receives → creates case in Nautilus → investigators review → decisions reported back → TOP executes actions. **GMRA Role**: FBS is the "A" (Action) execution layer that takes the evaluated decision and triggers appropriate downstream actions. **Integration Points**: Upstream (FORTRESS/URES evaluation results), Downstream (SNS Topics, FAPS action persistence, FWSNC notification center, Monrad investigations, LEO orchestration).
**Documentation**: [FBS Term](../resources/term_dictionary/term_fbs.md)
**Wiki**: https://w.amazon.com/index.php/DigitalFraud/FortressBackend
**URES Docs**: https://docs.ctps.amazon.dev/ures/ures-overview.html
**Owner**: URES Team (Unified Risk Evaluation Services)
**Key Functions**: Metrics production, order sidelining, idempotency, SNS publishing
**SNS Versions**: V1 (legacy/APWS), V2 (current/LEO)
**GMRA Role**: "A" (Action) execution layer
**Primary Consumers**: Monrad, FAPS, FWSNC, APWS, LEO
**Status**: ✅ Active - critical post-evaluation processing for all URES evaluations
**Related**: [FORTRESS](#fortress---fraudulent-order-reduction-through-risk-evaluation-at-super-speed-legacy), [URES](#ures---unified-risk-evaluation-system), [FAPS](#faps---fraud-action-persistence-service), [LEO](#leo---lifecycle-event-orchestrator), [Monrad](../resources/term_dictionary/term_monrad.md), [TOP](../resources/term_dictionary/term_top.md)

### Fortress - Risk Detection Platform
**Full Name**: Fortress
**Description**: Amazon's enterprise risk detection and prevention platform. Primary client of URES for real-time abuse evaluation.
**Documentation**: [Fortress Term](../resources/term_dictionary/term_fortress.md)
**Related**: [URES](../resources/term_dictionary/term_ures.md), [GMRA](../resources/term_dictionary/term_gmra.md)

### RACE - Receivable And Charge Execution Service
**Full Name**: Receivable And Charge Execution Service
**Description**: Amazon's platform for tracking receivables and executing retrocharges within the Customer Returns ecosystem. When a customer is offered an advanced resolution (refund, replacement, exchange before returning the item), RACE creates a **receivable** to track the expected return and triggers a **retrocharge** if the customer fails to return the item within the specified time window (typically 30-40 days). **Core Functions**: (1) Receivable Tracking - create/track/manage receivables with lifecycle management (Waiting → Active → Closed/Expired), (2) Policy Management - chargeability, expiry windows, notification schedules, (3) Charge Execution - orchestrates retrocharges through REFLEX including tax calculations and accounting. **Architecture**: RACE Platform comprises Receivable Service (tracks receivables), REFLEX (charge execution and accounting), and CRATER (event orchestration). **BAP Integration**: Critical downstream system for [BAR](../resources/term_dictionary/term_bar.md) (Buyer Abuse Retrocharge) - when MARIA/FLR Job detects abuse, BAR signals RACE via CRATERService to arm retrocharges (set receivable to chargeable, schedule charge execution). **Key APIs**: createReceivable, closeReceivable, cancelReceivable, updateReceivablePolicies, getReceivableByIdAndType. **Platform Capabilities**: Flexible usage (receivable only, charge only, or integrated), partial charge support, instant charge (same-day), audit trails, non-C-Returns support. **Service Impact**: If down, advanced resolutions NOT offered to customers in ORC, Herd graphs stuck, retrocharges fail, abuse recovery gap.
**Documentation**: [RACE Term](../resources/term_dictionary/term_race.md)
**Wiki**: https://w.amazon.com/bin/view/RACE_Platform/
**API Wiki**: https://w.amazon.com/bin/view/RACE_Service_API/
**Owner**: RFT (Resolution Fulfillment Technology) / C-Returns PE
**Contact**: creturns-pe@amazon.com
**Key Components**: Receivable Service, REFLEX, CRATER
**Receivable States**: Waiting → Active → Closed/Expired/Cancelled
**Timer Windows**: 15-day notification, 30-40 day expiry
**BAP Integration**: Downstream from BAR for abuse-triggered retrocharges
**Status**: ✅ Active - core returns infrastructure
**Related**: [BAR](../resources/term_dictionary/term_bar.md), [Retrocharge](../resources/term_dictionary/term_retrocharge.md), [REFLEX](../resources/term_dictionary/term_reflex.md), [CRATERService](../resources/term_dictionary/term_craterservice.md), [MARIA](../resources/term_dictionary/term_maria.md), [RFT](../resources/term_dictionary/term_rft.md)

### PCE - Purchase Contract Engine
**Full Name**: Purchase Contract Engine
**Description**: Amazon's central authority on order information and the core interface for operating on order documents during checkout. PCE manages the purchase contract lifecycle from order placement through fulfillment, serving as the **canonical source of order data** (order details, shipment info, payment info) for downstream systems. In buyer abuse prevention, PCE-managed order signals feed into claim evaluation, risk scoring, and abuse detection pipelines.
**Documentation**: [PCE Term](../resources/term_dictionary/term_pce.md)
**Q&A**: [SAGE: PCE](https://sage.amazon.dev/tags/PCE)
**Status**: ✅ Active - core ordering infrastructure
**Related**: [A-to-Z Claim](../resources/term_dictionary/term_atoz_claim.md), [A-to-Z Eval](../areas/area_atoz_eval.md), [CASE](../resources/term_dictionary/term_case.md)

### Tickety - Native AWS Ticketing API
**Full Name**: Tickety (SIM Ticketing API)
**Description**: Amazon's Native AWS (NAWS) accessible API for SIM Ticketing (SIM-T), replacing the legacy Fluxo and WFAWebService APIs. **Uses AWS SigV4A authentication with a globally redundant endpoint across 3 regions, eliminating Fluxo's single-region BasicAuth security risks.** Provides full SDK support (Java, Python, Ruby, TypeScript) for programmatic ticket and configuration management. 67%+ of ticketing API traffic migrated by Aug 2024.
**Documentation**: [Tickety](../resources/term_dictionary/term_tickety.md)
**Related**: [CTI](../resources/term_dictionary/term_cti.md)

### SPIKE - Selling Partner Inferencing and Knowledge Engine
**Full Name**: Selling Partner Inferencing and Knowledge Engine
**Description**: MLA program providing centralized ML toolkit for seller-related challenges. **Transforms seller lifecycle data (registration, listings, interactions, performance) into production-ready embeddings for similarity, anomaly detection, and behavioral cohort classification.** Eliminates redundant data discovery, infrastructure, and feature engineering across teams, reducing development time from months to weeks.
**Documentation**: [SPIKE](../resources/term_dictionary/term_spike.md)
**Related**: [PDNA](../resources/term_dictionary/term_pdna.md), [MLA-E](../resources/term_dictionary/term_mla_e.md)

### SYNAPSE - SYNergistic Autonomous Problem-Solving Enablement
**Full Name**: SYNergistic Autonomous Problem-Solving Enablement
**Description**: MLA program for resolving complex buyer/seller issues using Amazon-internal tools with or without explicit SOPs. **Functions as a self-sustaining mechanism that continuously learns through human interaction and self-exploration, achieving 88% planning accuracy in audits.** Explores optimized resolution methodologies and reduces process errors from inadequate SOPs.
**Documentation**: [SYNAPSE](../resources/term_dictionary/term_synapse.md)
**Related**: [GreenTEA](../resources/term_dictionary/term_greentea.md), [ICE](../resources/term_dictionary/term_ice.md)

### Lucid - Hallucination Detection Service
**Full Name**: Lucid (Hallucination Detection Service)
**Description**: RED-certified Amazon-internal LLM-agnostic hallucination detection service developed by MLA. **Domain-agnostic model (fine-tuned Mistral-7b) performs within 3% of custom fine-tuned models, with sentence-level scoring to localize hallucinations.** Processes ~150K calls/day for SOP Automation. Outperforms Claude Sonnet 3 in AUC with lower latency and cost.
**Documentation**: [Lucid](../resources/term_dictionary/term_lucid.md)
**Related**: [Mathison](../resources/term_dictionary/term_mathison.md)

### Mathison - AI-Generated Content Detection
**Full Name**: Mathison (AI Text Detection Service)
**Description**: RED-certified Amazon-internal service that differentiates machine-generated text from human-authored content. **Provides probability scores and style embeddings that distinguish between different authors or prompt templates, consistently ranking top 3 on the RAID benchmark.** Validated across product reviews, books, essays, poetry, news, and more. Offers customizable domain-specific support sets.
**Documentation**: [Mathison](../resources/term_dictionary/term_mathison.md)
**Related**: [Lucid](../resources/term_dictionary/term_lucid.md)

### PDNA - Product DNA
**Full Name**: Product DNA
**Description**: End-to-end multi-lingual ML system for product similarity, classification, and anomaly detection across the full ASIN spectrum and multiple marketplaces. **Architecture consists of gene generation (text, image, transaction signals), gene blending (unitary representation), and ML model generation with multi-modal embeddings (CLIP, FastText, ResNet, InstructBLIP).** Self-service via Python SDK and CDK deployment.
**Documentation**: [PDNA](../resources/term_dictionary/term_pdna.md)
**Related**: [SPIKE](../resources/term_dictionary/term_spike.md)

### ICE - Issue Comprehension Engine
**Full Name**: Issue Comprehension Engine
**Description**: MLA NLP initiative providing SOP recommendations with dynamic step-by-step guidance for resolving seller contacts. **Action Orchestrator achieved 45.9% reduction in handling time and 19.3% decrease in case reopening rates, projecting $13.9M annual savings.** Action mining research (76.5% accuracy) transferred to SYNAPSE. Production transferred to SPX in March 2025.
**Documentation**: [ICE](../resources/term_dictionary/term_ice.md)
**Related**: [SYNAPSE](../resources/term_dictionary/term_synapse.md), [GreenTEA](../resources/term_dictionary/term_greentea.md)

### IDA (MLA) - Intelligent Data Agent
**Full Name**: Intelligent Data Agent
**Description**: MLA program streamlining data workflow creation via conversational chatbot interface powered by agentic LLM. **Custom knowledge base optimized for 20K+ Andes tables enables natural language data discovery, SQL generation, and Cradle profile creation.** Available via MCP server, playground web app, and API. Complementary to Andi (BDT): IDA is generalist/broad, Andi is specialist/precise.
**Documentation**: [Intelligent Data Agent](../resources/term_dictionary/term_intelligent_data_agent.md)
**Related**: [AIDE](../resources/term_dictionary/term_aide.md), [IDA (BAP)](../resources/term_dictionary/term_ida.md)

### IRONMAN - Intelligent Risk Orchestration and Mitigation Service
**Full Name**: Intelligent Risk Orchestration and Mitigation Service
**Description**: BRP's 3-Year Architecture Plan (3YAP) for continuous and holistic risk assessment across the entire customer journey. **IRONMAN envisions three universal buckets — features, models, and treatments — shared across the customer lifecycle, replacing isolated intent-specific evaluations.** The architecture uses a three-layered design (Trigger, Orchestrator, Agent) with a Treatment Agent that selects actions based on Down-Stream Impact. Currently in vision/experiment phase with WAVE validating cross-lifecycle model feasibility.
**Documentation**: [IRONMAN](../resources/term_dictionary/term_ironman.md)
**Wiki**: N/A
**Related**: [URES](../resources/term_dictionary/term_ures.md), [DSI](../resources/term_dictionary/term_dsi.md), [CUBES](../resources/term_dictionary/term_cubes.md)

### Carnaval - Alarm Aggregation System
**Full Name**: Carnaval
**Description**: Amazon's alarm aggregation and management system that sits on top of existing monitoring frameworks (SYMON, Snitch, CloudWatch).
**Documentation**: [Carnaval Term](../resources/term_dictionary/term_carnaval.md)
**Related**: [Alarm: FLR](../areas/alarms/alarm_flr.md), [Alarm: PDA](../areas/alarms/alarm_pda.md)

---

## Quick Reference Table

| System | Category | Primary Function |
|--------|----------|------------------|
| SAIS | Development | ML development environment |
| MODS | Development | Model training orchestration |
| MIMS | Deployment | Model deployment & management |
| URES | Evaluation | Real-time risk orchestration |
| GMRA | Framework | Evaluation paradigm |
| OTF | Features | Real-time feature computation |
| AMES | Inference | ML model scoring |
| RMP | Rules | Business logic & thresholds |
| JUMICS | Migration | Offline-to-online migration |
| VCOL | Orchestration | Variable computation routing |
| Fortress | Platform | Enterprise risk platform |

---

## Related Glossaries

- [Workflows & Processes](acronym_glossary_workflows.md) - Evaluation workflows
- [Data & Metrics](acronym_glossary_data_metrics.md) - Data platforms
- [Teams & Organizations](acronym_glossary_teams.md) - Platform owners

**Navigation**: [← Back to Main Glossary](entry_acronym_glossary.md)

---

**Last Updated**: April 19, 2026
**Entries**: 100+ ML, risk evaluation, infrastructure, and systems design platforms
