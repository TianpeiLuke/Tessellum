---
tags:
  - resource
  - terminology
  - llm
  - reasoning
  - prompting
  - search_algorithms
  - planning
keywords:
  - tree of thought
  - ToT
  - deliberative reasoning
  - thought decomposition
  - state evaluation
  - breadth-first search
  - depth-first search
  - beam search
  - backtracking
  - multi-path reasoning
  - planning with LLMs
  - search over thoughts
topics:
  - LLM Reasoning
  - Prompt Engineering
  - Deliberative Problem Solving
  - Search Algorithms
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Term: Tree of Thought (ToT)

## Definition

**Tree of Thought (ToT)** is a deliberative reasoning framework for large language models that generalizes [chain-of-thought (CoT)](term_chain_of_thought.md) prompting by maintaining a tree of intermediate reasoning states ("thoughts") and exploring them via classical search algorithms. Introduced by Yao et al. (2023) and published at NeurIPS 2023, ToT treats each problem as a search over a tree where nodes are partial solutions (coherent language sequences representing intermediate reasoning steps) and edges are thought-generation steps. The framework combines four modular components: (1) **thought decomposition** into coherent intermediate steps, (2) a **thought generator** that proposes candidate next steps, (3) a **state evaluator** that heuristically assesses progress via LLM self-evaluation, and (4) a **search algorithm** (BFS, DFS, or beam search) that systematically explores the tree with the ability to look ahead and backtrack. On the Game of 24 benchmark, GPT-4 with CoT prompting solves only 4% of tasks, while ToT achieves 74% -- a 70-point improvement demonstrating the power of deliberate search over linear reasoning chains.

## Full Name

**Tree of Thought (ToT)**

**Also Known As**: Tree-of-Thoughts, ToT prompting, deliberate problem solving with LLMs, thought tree search

## Historical Context

ToT emerged from a convergence of two research threads: (1) the success of [chain-of-thought](term_chain_of_thought.md) prompting (Wei et al., 2022) in unlocking multi-step reasoning in [LLMs](term_llm.md), and (2) decades of classical AI research on tree search algorithms (BFS, DFS, A*, Monte Carlo Tree Search) for planning and problem solving. While CoT demonstrated that intermediate reasoning steps dramatically improve LLM performance, it constrains reasoning to a single left-to-right path with no mechanism for exploring alternatives or recovering from errors. Yao et al. recognized that tasks requiring exploration, strategic lookahead, or where initial decisions are pivotal expose CoT's fundamental limitation: it inherits the autoregressive model's token-level, unidirectional generation process.

The key intellectual contribution was reframing LLM inference as a search problem -- connecting Newell, Shaw, and Simon's (1959) classical "problem space" formulation with modern language model capabilities. The LLM serves dual roles: as a thought generator (proposing candidate steps) and as a heuristic evaluator (assessing which candidates are promising), while the search algorithm provides the systematic exploration structure that autoregressive generation lacks.

## Key Properties

| Property | Description |
|----------|-------------|
| **Deliberative** | Explicitly explores multiple reasoning paths before committing, unlike CoT's single-pass approach |
| **Modular** | Four decoupled components (decomposition, generation, evaluation, search) can be independently configured per task |
| **Backtracking** | Can abandon unproductive paths and return to earlier states -- impossible in standard autoregressive generation |
| **Self-evaluating** | Uses the LLM itself to assess intermediate states (e.g., "sure/maybe/impossible" verdicts), no external reward model required |
| **Search-algorithm-agnostic** | Compatible with BFS, DFS, beam search, or any tree traversal strategy |
| **Task-adaptive** | Thought granularity (single word, single line, multi-sentence paragraph) is configured per task domain |
| **Computationally expensive** | Requires many more LLM calls than CoT (multiple generations + evaluations per node in the tree) |

## Core Components

### 1. Thought Decomposition
The problem is decomposed into a sequence of intermediate thought steps. The granularity is task-dependent:
- **Game of 24**: Each thought is one arithmetic equation (3 steps total)
- **Creative Writing**: Each thought is a coherent paragraph plan
- **Mini Crosswords**: Each thought is a word fill for one clue

### 2. Thought Generator (G)
Two strategies for generating candidate thoughts at each node:
- **Sample**: Draw i.i.d. samples from the LLM via temperature sampling (works when the thought space is rich, e.g., creative writing)
- **Propose**: Use a structured "propose prompt" to generate multiple distinct candidates in a single LLM call (more efficient when thoughts are constrained, e.g., Game of 24)

### 3. State Evaluator (V)
The LLM evaluates each state's promise toward solving the problem:
- **Value**: Independently scores each state (e.g., assign "sure/likely/impossible")
- **Vote**: Compares multiple states and votes for the most promising one
- Acts as a heuristic function guiding the search -- analogous to evaluation functions in classical game-playing AI

### 4. Search Algorithm
- **Breadth-First Search (BFS)**: Maintains a set of the b most promising states at each depth; suitable for tasks with bounded branching (Game of 24 uses b=5)
- **Depth-First Search (DFS)**: Explores depth-first with pruning via the state evaluator; suitable for tasks where early pruning is effective (Mini Crosswords)
- **Beam Search**: Retains top-k candidates at each level, balancing breadth and depth

## Taxonomy of Reasoning Frameworks

| Framework | Topology | Exploration | Backtracking | Key Innovation |
|-----------|----------|-------------|--------------|----------------|
| **Standard Prompting** | Point | None | No | Direct input-output mapping |
| **[CoT](term_chain_of_thought.md)** | Linear chain | Single path | No | Intermediate reasoning steps |
| **Self-Consistency** | Linear (sampled) | Multiple independent paths | No | Majority voting over k chains |
| **ToT** | Tree | Systematic (BFS/DFS) | Yes | LLM-guided search with evaluation |
| **Graph of Thought (GoT)** | DAG | Arbitrary | Yes | Merge and refine operations across branches |
| **Algorithm of Thoughts (AoT)** | Dynamic | Algorithmic | Implicit | Internalizes search within a single prompt |

## Notable Results

### Game of 24
| Method | Success Rate |
|--------|:-----------:|
| Standard prompting (GPT-4) | 7.3% |
| CoT prompting (GPT-4) | 4.0% |
| CoT + self-consistency (k=100) | 9.0% |
| **ToT (b=5, BFS)** | **74.0%** |

### Creative Writing
ToT with a two-step process (generate plans, then passages) produced coherent stories rated significantly higher by GPT-4 evaluation on coherence metrics, compared to both standard and CoT prompting.

### Mini Crosswords (5x5)
| Method | Word-Level Success |
|--------|:-----------------:|
| Standard prompting | 16% |
| CoT prompting | 15.6% |
| **ToT (DFS, pruning)** | **60%** |

## Variants and Extensions

| Variant | Authors | Year | Key Innovation |
|---------|---------|------|----------------|
| **ToT (original)** | Yao et al. | 2023 | External search algorithms (BFS/DFS) over LLM-generated thoughts |
| **ToT via prompting** | Hulbert | 2023 | Single-prompt ToT using expert roleplay -- no external search code |
| **RL-ToT** | Long | 2023 | Reinforcement learning-trained "ToT Controller" for adaptive tree traversal |
| **Graph of Thought** | Besta et al. | 2023 | Extends tree to DAG; enables merging and refining across branches |
| **Algorithm of Thoughts** | Sel et al. | 2023 | LLM internalizes search behavior within a single generation |
| **Tree of Uncertain Thoughts (TouT)** | - | 2024 | Quantifies uncertainty at each thought node for more reliable decisions |
| **PanelGPT** | Sun | 2023 | Multi-LLM panel discussion extending ToT to collaborative reasoning |

## Applications

### General Problem Solving
- **Mathematical reasoning**: Game of 24, complex arithmetic, and planning tasks where single-path reasoning fails
- **Creative generation**: Multi-paragraph story writing with coherence constraints
- **Puzzle solving**: Crosswords, Sudoku, and constraint-satisfaction problems
- **Code generation**: Exploring multiple implementation strategies before selecting the best approach

### Relevance to Abuse Detection
- **Complex investigation workflows**: Abuse investigation cases that require exploring multiple hypotheses (e.g., "is this return fraud, wardrobing, or legitimate dissatisfaction?") could benefit from ToT-style multi-path reasoning where the LLM evaluates each hypothesis branch
- **[GreenTEA](term_greentea.md)** and similar agentic systems could incorporate ToT for cases where the initial reasoning path reaches a dead end, enabling backtracking to try alternative investigation strategies
- **Decision audit trails**: ToT's explicit tree structure provides richer audit trails than linear CoT, showing not just the chosen reasoning path but also the alternatives considered and why they were rejected

## Challenges

1. **Computational cost**: ToT requires O(b * d * k) LLM calls for branching factor b, depth d, and k evaluation samples per node -- orders of magnitude more expensive than single-pass CoT
2. **Evaluation reliability**: The state evaluator (the LLM itself) may misjudge which branches are promising, leading to systematic search errors that compound across tree depth
3. **Task decomposition sensitivity**: Performance depends heavily on choosing the right thought granularity; too coarse loses the benefit of search, too fine explodes the search space
4. **Diminishing returns with stronger models**: As base LLM reasoning improves (e.g., o1, o3 with internal chain-of-thought), the marginal benefit of external search structures like ToT may decrease -- the model may internalize the search
5. **Limited theoretical grounding**: No formal analysis of when ToT is expected to outperform CoT; the choice between them remains empirical and task-specific
6. **Prompt engineering overhead**: Each task requires custom thought decomposition, generation prompts, and evaluation prompts -- ToT is not a drop-in replacement for CoT

## Related Terms

### Direct Predecessors
- [Chain of Thought (CoT)](term_chain_of_thought.md) -- ToT generalizes CoT's linear reasoning chain into a branching tree; CoT is a special case of ToT with branching factor 1 and no backtracking
- [Prompt Engineering](term_prompt_engineering.md) -- ToT is an advanced prompting framework that structures multi-step LLM interaction for deliberative reasoning

### Core Concepts
- [LLM](term_llm.md) -- ToT operates on large language models, using them as both thought generators and state evaluators
- [Scaling Law](term_scaling_law.md) -- ToT demonstrates inference-time scaling: investing more computation at inference (via search) improves performance beyond what model scale alone provides

### Algorithmic Foundations
- Classical tree search (BFS, DFS, beam search) -- ToT adapts these algorithms to operate over natural language thought states rather than formal state representations
- Monte Carlo Tree Search (MCTS) -- Related approach from game-playing AI (AlphaGo); ToT uses heuristic LLM evaluation rather than random rollouts for node assessment

### Extensions and Variants
- Graph of Thought (GoT) -- Generalizes ToT's tree to a directed acyclic graph, enabling thought merging and refinement across branches (Besta et al., 2023)
- Self-Consistency (Wang et al., 2022) -- Samples multiple independent CoT paths and majority-votes; less structured than ToT but simpler to implement

### Production Systems
- [GreenTEA](term_greentea.md) -- Agentic automation system that could incorporate ToT-style multi-hypothesis exploration for complex abuse cases
- [SPOT-X](term_spot_x.md) -- Structured decision rules that could benefit from ToT when generating explanations for ambiguous classification cases

## References

### Primary Source
- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601. *Primary reference -- introduced the ToT framework with BFS/DFS search over LLM-generated thoughts.*

### Key Predecessor
- Wei, J. et al. (2022). [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](../papers/lit_wei2022chain.md). NeurIPS 2022. arXiv:2201.11903. *CoT prompting -- the linear reasoning paradigm that ToT generalizes.*

### Extensions
- Besta, M. et al. (2023). Graph of Thoughts: Solving Elaborate Problems with Large Language Models. arXiv:2308.09687. *Extends ToT from tree to DAG with merge/refine operations.*
- Long, J. (2023). Large Language Model Guided Tree-of-Thought. arXiv:2305.08291. *RL-trained ToT controller for adaptive tree traversal.*
- Wang, X. et al. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. arXiv:2203.11171. *Multiple CoT paths + majority vote -- simpler alternative to ToT's structured search.*

### Classical Foundations
- Newell, A., Shaw, J. C., & Simon, H. A. (1959). Report on a general problem-solving program. IFIP Congress. *Original "problem space" formulation that ToT connects to LLM inference.*
