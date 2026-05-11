---
tags:
  - resource
  - terminology
  - infrastructure
  - compute_environment
  - container_orchestration
  - aws
  - kubernetes
keywords:
  - EKS
  - Elastic Kubernetes Service
  - Kubernetes
  - container orchestration
  - pod
  - cluster
  - managed Kubernetes
topics:
  - container orchestration
  - cloud infrastructure
  - deployment platforms
language: markdown
date of note: 2026-05-07
status: active
building_block: concept
related_wiki: https://docs.aws.amazon.com/eks/
---

# EKS - Elastic Kubernetes Service

## Definition

Amazon Elastic Kubernetes Service (EKS) is AWS's managed Kubernetes service that runs the Kubernetes control plane across multiple availability zones without requiring operators to install, operate, or maintain their own Kubernetes clusters. EKS provides a certified Kubernetes-conformant environment, enabling teams to use standard Kubernetes tooling (kubectl, Helm, operators) while AWS manages control plane availability, patching, and scaling.

In the buyer abuse prevention context, EKS is a deployment target for ORCA Edge containerized workflows and supports BAP teams that require Kubernetes-native features such as custom operators, service meshes, or GPU scheduling for ML inference workloads.

## Context

- **ORCA Edge**: EKS is a supported deployment platform for ORCA Edge alongside Docker-compose, ECS, and vanilla Kubernetes
- **BAP ML Inference**: Teams with complex scheduling requirements (GPU node pools, spot instances, custom autoscaling) use EKS for model serving
- **Platform Teams**: Infrastructure teams provide EKS clusters as shared compute platforms with namespace isolation per service team
- **Hybrid Deployments**: Some BAP services run on EKS when they need Kubernetes-specific features (CRDs, operators, Istio service mesh)

## Key Characteristics

- **Managed Control Plane**: AWS manages etcd, API server, scheduler, and controller manager across 3 AZs
- **Node Groups**: Managed (AWS patches nodes), self-managed (custom AMIs), or Fargate profiles (serverless pods)
- **Kubernetes Conformance**: Certified upstream Kubernetes — all standard APIs, CRDs, and operators work unmodified
- **IAM Integration**: IAM Roles for Service Accounts (IRSA) maps Kubernetes service accounts to IAM roles for fine-grained AWS permissions
- **Add-ons**: Managed add-ons for CoreDNS, kube-proxy, VPC CNI, EBS CSI driver, and observability agents
- **Multi-Tenancy**: Namespace-based isolation with RBAC, network policies, and resource quotas for shared clusters
- **GPU Support**: Native GPU scheduling for ML inference pods with NVIDIA device plugin


## Related Terms

- **[ECR](term_ecr.md)**: Container registry storing images pulled by EKS pods during deployment
- **[ORCA Edge](term_orca_edge.md)**: Containerized ORCA runtime deployable on EKS for Kubernetes-native orchestration
- **[ECS](term_ecs.md)**: AWS's alternative container orchestration — simpler but less flexible than EKS/Kubernetes
- **[Apollo](term_apollo.md)**: Amazon's deployment service that can target EKS clusters for container deployments
- **[SageMaker](term_sagemaker.md)**: ML platform that can use EKS for distributed training and inference via SageMaker Operators
- **[Microservices Architecture](term_microservices_architecture.md)**: Architectural pattern enabled by EKS pod isolation and service discovery
- **[NAWS](term_naws.md)**: Native AWS environment where EKS clusters run for BAP services
- **[CDK](term_cdk.md)**: Infrastructure-as-code used to provision EKS clusters and managed node groups
- **[DAG](term_dag.md)**: Kubernetes workflow engines (Argo) execute DAG-structured pipelines on EKS
- **[ORCA](term_orca.md)**: Workflow orchestration platform whose Edge runtime deploys on EKS

## References

- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [ORCA Edge Architecture](https://console.harmony.a2z.com/orca-docs/workflows/developer-guide/orca-edge)
