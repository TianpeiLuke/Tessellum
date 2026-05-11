---
tags:
  - resource
  - terminology
  - computer_science
  - parallel_computing
  - performance
  - scalability
keywords:
  - Amdahl's Law
  - parallel speedup
  - serial bottleneck
  - scalability limit
  - parallelization
  - Gene Amdahl
topics:
  - parallel computing limits
  - system scalability
  - performance optimization
language: markdown
date of note: 2026-04-17
status: active
building_block: concept
related_wiki: null
---

# Amdahl's Law - Parallel Speedup Limit

## Definition

Amdahl's Law, formulated by Gene Amdahl in 1967, states that the maximum speedup of a program through parallelization is limited by the fraction of the program that must execute sequentially. If a fraction $p$ of a program can be parallelized and the remaining fraction $s = 1 - p$ is inherently serial, then the maximum speedup with $n$ processors is:

$$S(n) = \frac{1}{s + \frac{p}{n}} = \frac{1}{(1 - p) + \frac{p}{n}}$$

As $n \to \infty$, the speedup approaches $\frac{1}{s}$. For example, if 95% of a program is parallelizable ($p = 0.95$), the maximum speedup is $\frac{1}{0.05} = 20\times$, regardless of how many processors are used.

## Context

Amdahl's Law is fundamental to system design decisions about when parallelization is worth the investment. In ML pipeline infrastructure, it explains why distributed training speedup plateaus: data loading, gradient synchronization, and checkpoint saving are serial bottlenecks that limit the benefit of adding more GPUs. For distributed systems more broadly, the law governs the scalability of any system with a serial component — from database transactions requiring coordination to pipeline steps that must execute sequentially.

## Key Characteristics

- **Serial bottleneck dominates**: Even a small serial fraction severely limits speedup — 5% serial caps speedup at 20×, 10% serial caps at 10×
- **Diminishing returns**: Adding more processors yields progressively less benefit — the first doubling helps most, subsequent doublings help less
- **Applies beyond CPUs**: The law governs any parallel system — distributed databases, MapReduce jobs, multi-GPU training, microservice scaling
- **Gustafson's Law (counterpoint)**: John Gustafson (1988) argued that as processors increase, problem size also increases, so the serial fraction shrinks — "scaled speedup" can be nearly linear
- **Universal Scalability Law (extension)**: Neil Gunther extended Amdahl's with contention and coherence penalties — throughput can actually *decrease* with more nodes due to coordination overhead
- **Practical implication**: Optimize the serial path first — parallelizing the already-parallel part yields diminishing returns
- **In ML**: Data parallelism (DDP/FSDP) is limited by gradient all-reduce (serial synchronization); pipeline parallelism is limited by bubble time between stages

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: Both are fundamental impossibility/limitation results — CAP limits distributed data stores, Amdahl's limits parallel speedup
- **[FLP Impossibility](term_flp_impossibility.md)**: Another fundamental limit — consensus impossibility in async systems. Together with CAP and Amdahl's, these form the "impossible trinity" of distributed systems theory
- **[Data Parallelism](term_data_parallelism.md)**: Distributed training strategy directly governed by Amdahl's Law — gradient synchronization is the serial bottleneck
- **[Scaling Law](term_scaling_law.md)**: Neural scaling laws describe how model performance scales with compute — Amdahl's constrains how efficiently that compute can be parallelized
- **[Power Law](term_power_law.md)**: Amdahl's speedup curve follows a diminishing-returns pattern similar to power law relationships
- **[Zipf's Law](term_zipfs_law.md)**: Another fundamental law governing distributions — Zipf in data, Amdahl in computation
- **[PACELC](term_pacelc.md)**: PACELC and Amdahl's Law both expose fundamental trade-offs in distributed systems — PACELC limits consistency-latency, Amdahl's limits parallel speedup
- **[Space-Based Architecture](term_space_based_architecture.md)**: Architecture pattern that minimizes serial bottlenecks through in-memory data grids
- **[Microservices Architecture](term_microservices_architecture.md)**: Scaling microservices is governed by Amdahl's — the slowest synchronous call in a chain limits overall throughput
- **[MoE](term_moe.md)**: Mixture of Experts uses expert parallelism to scale model capacity — routing overhead is the Amdahl serial fraction
- **[Scalability](term_scalability.md)**: Amdahl's Law defines the theoretical upper bound on scalability — the serial fraction of a workload caps the maximum speedup achievable through horizontal scaling

## References

- Amdahl, G. (1967). "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities." *AFIPS Conference Proceedings*, 30, 483–485.
- [Amdahl's Law — Wikipedia](https://en.wikipedia.org/wiki/Amdahl%27s_law)
- Gustafson, J. (1988). "Reevaluating Amdahl's Law." *Communications of the ACM*, 31(5), 532–533.
- Gunther, N. (2007). *Guerrilla Capacity Planning*. Springer. (Universal Scalability Law)
