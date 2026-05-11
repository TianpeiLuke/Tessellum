---
tags:
  - resource
  - terminology
  - problem_solving
  - cognitive_science
  - artificial_intelligence
  - decision_making
  - mathematical_reasoning
keywords:
  - heuristic
  - heuristics
  - heuristic reasoning
  - heuriskein
  - mental shortcut
  - rule of thumb
  - problem-solving strategy
  - bounded rationality
  - satisficing
  - cognitive heuristic
  - metaheuristic
  - Polya
  - Herbert Simon
  - Tversky and Kahneman
  - Gigerenzer
topics:
  - Problem Solving Methodology
  - Cognitive Psychology
  - Artificial Intelligence
  - Decision Theory
language: markdown
date of note: 2026-03-13
status: active
building_block: concept
---

# Heuristic

## Definition

A **heuristic** (from Greek *heuriskein*, "to find" or "to discover") is any approach to problem solving, learning, or decision making that employs a practical method that is not guaranteed to be optimal, perfect, or fully rational, but is sufficiently effective for reaching an immediate, approximate goal. The term spans three distinct but historically connected traditions:

1. **Classical/mathematical tradition** (Polya): Heuristic as the **study of methods and rules of discovery** — a systematic discipline for teaching problem-solving strategies such as analogy, decomposition, generalization, specialization, and working backwards. In this tradition, heuristics are *tools for finding solutions*.

2. **Cognitive/psychological tradition** (Simon, Tversky & Kahneman): Heuristic as a **mental shortcut** that simplifies complex judgments under uncertainty — fast, automatic cognitive processes that are generally adaptive but can produce systematic biases. In this tradition, heuristics are *descriptions of how minds actually work*.

3. **Computational tradition** (AI, operations research): Heuristic as an **algorithm or search strategy** that trades optimality guarantees for speed — practical methods that find good-enough solutions to computationally intractable problems (NP-hard, combinatorial). In this tradition, heuristics are *engineering approximations*.

The unifying thread across all three traditions is the contrast with **algorithms**: where an algorithm guarantees a correct solution through exhaustive, systematic procedure, a heuristic provides a practical shortcut that usually works well enough but offers no guarantee of optimality or correctness.

## Historical Context

The concept of heuristic has evolved through four major phases, each redefining its scope and significance:

| Period | Figure(s) | Contribution | Tradition |
|--------|-----------|-------------|-----------|
| Ancient Greece | Archimedes, Pappus | *Heuriskein* — the art of discovery; Archimedes' "Eureka!" is the archetypal heuristic moment | Proto-mathematical |
| 1945 | **George Polya** | *How to Solve It* — formalized heuristic reasoning as a teachable discipline; identified 67 named heuristic strategies; established the four-step problem-solving method | Mathematical |
| 1950s-1960s | **Herbert A. Simon** | Introduced **bounded rationality** and **satisficing** — humans use heuristics because cognitive resources are limited; won 1978 Nobel Prize in Economics | Cognitive/Economic |
| 1974 | **Amos Tversky, Daniel Kahneman** | "Judgment Under Uncertainty: Heuristics and Biases" (*Science*, 1974) — identified representativeness, availability, and anchoring as three primary cognitive heuristics that produce systematic biases; Kahneman won 2002 Nobel Prize | Cognitive/Psychological |
| 1990s-present | **Gerd Gigerenzer** | "Fast and frugal heuristics" program — argued that heuristics are not cognitive defects but **ecologically rational** adaptations; heuristics can outperform complex algorithms in uncertain environments | Ecological Rationality |
| 1970s-present | Newell & Simon, AI research | Heuristic search (A*, simulated annealing, genetic algorithms) — computational methods that use domain knowledge to prune search spaces | Computational/AI |

**Key inflection point**: The Tversky-Kahneman program shifted the connotation of "heuristic" from Polya's positive sense (a discovery tool) to a negative sense (a source of bias). Gigerenzer's later work partially restored the positive connotation by showing that heuristics are often ecologically rational — well-adapted to the structure of real-world environments.

## Taxonomy

### By Tradition and Function

| Type | Definition | Examples | Emphasis |
|------|-----------|----------|----------|
| **Problem-solving heuristics** (Polya) | Named strategies for attacking unfamiliar problems | Analogy, decomposition, working backwards, generalization, specialization, auxiliary problem | Discovery — how to find solutions |
| **Cognitive heuristics** (Tversky & Kahneman) | Automatic mental shortcuts for judgment under uncertainty | Availability, representativeness, anchoring, affect heuristic | Bias — where judgment goes wrong |
| **Fast and frugal heuristics** (Gigerenzer) | Simple decision rules that exploit environmental structure | Recognition heuristic, take-the-best, 1/N rule | Ecological rationality — when simple rules beat complex models |
| **Computational heuristics** (AI/OR) | Algorithms that trade optimality for tractability | A* search, greedy algorithms, hill climbing, beam search | Approximation — good-enough solutions fast |
| **Metaheuristics** (optimization) | Higher-level frameworks for guiding search across problem classes | Simulated annealing, genetic algorithms, tabu search, ant colony optimization | Generalization — domain-independent optimization |

### Kahneman-Tversky Cognitive Heuristics (Canonical Three)

| Heuristic | Mechanism | Typical Bias Produced |
|-----------|-----------|----------------------|
| **Representativeness** | Judge probability by similarity to a prototype | Base rate neglect, conjunction fallacy |
| **Availability** | Judge frequency/probability by ease of recall | Overweight vivid/recent events |
| **Anchoring and adjustment** | Start from an initial value, adjust insufficiently | Systematic under/over-estimation |

### Polya's Problem-Solving Heuristics (Major Categories)

| Category | Strategies | Step in Four-Step Method |
|----------|-----------|------------------------|
| **Representation** | Draw a figure, introduce notation, restate the problem | Step 1 (Understand) |
| **Search** | Find a related problem, analogy, decomposition, working backwards | Step 2 (Plan) |
| **Transformation** | Generalization, specialization, variation, auxiliary problem | Step 2 (Plan) |
| **Verification** | Check the result, derive differently, examine limiting cases | Step 4 (Look Back) |

## Key Properties

- **Speed-accuracy tradeoff**: Heuristics sacrifice guaranteed optimality for practical efficiency — faster decisions at the cost of occasional errors
- **Bounded rationality**: Heuristics are adaptive responses to cognitive constraints (limited time, knowledge, and computational capacity), not defects of reasoning
- **Domain dependence**: Polya's heuristics are domain-independent strategies; cognitive heuristics are domain-general mental processes; computational heuristics are often domain-specific
- **Ecological rationality**: A heuristic's effectiveness depends on the match between its structure and the environment's statistical structure (Gigerenzer's "less is more" principle)
- **Systematicity of error**: Cognitive heuristics produce not random errors but *systematic, predictable* biases — the foundation of behavioral economics
- **Teachability**: Polya demonstrated that heuristic reasoning can be explicitly taught and improved through practice; this is not universally accepted for cognitive heuristics (debiasing is difficult)
- **Contrast with algorithms**: An algorithm guarantees a correct answer in finite steps; a heuristic provides no such guarantee but is often the only practical option for complex problems
- **Dual-process connection**: In Kahneman's System 1/System 2 framework, cognitive heuristics are System 1 (fast, automatic, effortless); Polya's problem-solving heuristics require System 2 (slow, deliberate, effortful)
- **Composability**: Heuristics can be combined — Polya's method chains multiple heuristics sequentially; metaheuristics compose lower-level heuristics into higher-level search strategies
- **Historical semantic drift**: The term has shifted from purely positive (Polya: "art of discovery") through negative (Kahneman: "source of bias") to nuanced (Gigerenzer: "ecologically rational tools")

## Notable Systems / Implementations

| System | Mechanism | Domain |
|--------|-----------|--------|
| **Polya's Four-Step Method** (1945) | Structured heuristic protocol: Understand → Plan → Execute → Look Back | Mathematics education, general problem solving |
| **GPS (General Problem Solver)** (Newell & Simon, 1957) | Means-ends analysis — reduce difference between current state and goal | Artificial intelligence |
| **A* Search** (Hart, Nilsson, Raphael, 1968) | Heuristic function h(n) estimates cost to goal; guarantees optimality if h is admissible | Pathfinding, AI planning |
| **Heuristics-and-Biases Program** (Tversky & Kahneman, 1974) | Experimental identification of systematic cognitive biases from three heuristics | Behavioral economics, psychology |
| **Satisficing** (Simon, 1956) | Accept the first option that meets a minimum threshold rather than optimizing | Organizational decision making |
| **Fast-and-Frugal Trees** (Gigerenzer et al., 1999) | Binary decision trees using few cues; shown to match or beat regression models | Medical diagnosis, legal judgment |
| **Simulated Annealing** (Kirkpatrick et al., 1983) | Metaheuristic inspired by metallurgical annealing; accepts worse solutions with decreasing probability | Combinatorial optimization |
| **Genetic Algorithms** (Holland, 1975) | Metaheuristic inspired by natural selection; evolves solution populations | Optimization, machine learning |

## Applications

| Domain | Heuristic Type | Application |
|--------|---------------|-------------|
| **Mathematics education** | Polya's problem-solving heuristics | Teaching students to approach unfamiliar proofs and problems systematically |
| **AI search and planning** | Computational heuristics (A*, beam search) | Robot navigation, game playing, scheduling, constraint satisfaction |
| **Behavioral economics** | Cognitive heuristics (Kahneman) | Predicting consumer behavior, designing choice architectures (nudges) |
| **Medical diagnosis** | Fast-and-frugal heuristics (Gigerenzer) | Triage decisions, emergency room protocols, diagnostic trees |
| **Operations research** | Metaheuristics (SA, GA, tabu search) | Vehicle routing, supply chain optimization, network design |
| **Software engineering** | Code heuristics, design patterns | Code review rules, refactoring heuristics, bug-finding strategies |
| **UX design** | Nielsen's usability heuristics | Heuristic evaluation of user interfaces (10 usability heuristics) |

## Challenges and Limitations

### Conceptual Challenges

- **Definitional ambiguity**: The term "heuristic" means different things in different fields — a problem-solving strategy (Polya), a cognitive bias source (Kahneman), or an approximate algorithm (CS). This can cause confusion in interdisciplinary work
- **Positive vs. negative framing**: The Kahneman tradition emphasizes heuristics as bias sources; the Gigerenzer tradition emphasizes them as adaptive tools. Neither is universally correct — the value depends on the environment
- **Debiasing difficulty**: Cognitive heuristics are largely automatic (System 1); teaching people to override them is hard and often requires restructuring the environment rather than the person

### Practical Challenges

- **No optimality guarantee**: By definition, heuristics cannot guarantee the best solution — knowing when a heuristic's output is "good enough" requires domain expertise
- **Ecological validity**: A heuristic that works well in one environment may fail in another (e.g., availability heuristic works well for predicting common events but fails for rare, catastrophic ones)
- **Overgeneralization**: Applying a problem-solving heuristic (e.g., analogy) to a problem where it doesn't fit can be worse than no strategy at all
- **Metaheuristic tuning**: Computational metaheuristics (SA, GA) require parameter tuning that is itself a heuristic process — turtles all the way down

### Ongoing Debates

- **Gigerenzer vs. Kahneman**: Are cognitive heuristics primarily adaptive or primarily error-prone? The field remains divided
- **When to use heuristics vs. algorithms**: No general theory determines when a heuristic will outperform an exact algorithm; this remains an empirical question
- **Teachability of cognitive heuristics**: Can awareness of cognitive biases actually improve decision making, or does it merely provide vocabulary for describing errors?

## Related Terms

- **[Availability Heuristic](term_availability_heuristic.md)**: A specific cognitive heuristic — judging probability by ease of recall; a key example of the Kahneman-Tversky program
- **[Affect Heuristic](term_affect_heuristic.md)**: A specific cognitive heuristic — judging risk/benefit by emotional reaction; added to the Kahneman-Tversky framework by Paul Slovic
- **[Cognitive Bias](term_cognitive_bias.md)**: Systematic errors in judgment that often result from cognitive heuristics; the bias is the *effect*, the heuristic is the *mechanism*
- **[Anchoring](term_anchoring.md)**: A specific cognitive heuristic — insufficient adjustment from an initial value; one of the original three Kahneman-Tversky heuristics
- **[Confirmation Bias](term_confirmation_bias.md)**: A bias that interacts with heuristic reasoning — once a heuristic produces a judgment, confirmation bias resists updating it
- **[Satisficing](term_satisficing.md)**: Herbert Simon's term for accepting "good enough" solutions; the decision-theoretic formalization of heuristic reasoning
- **[Critical Thinking](term_critical_thinking.md)**: The disciplined application of reasoning to overcome heuristic biases; System 2 overriding System 1
- **[Socratic Questioning](term_socratic_questioning.md)**: A questioning method that surfaces hidden heuristic assumptions; related to Polya's guided discovery
- **[Design Thinking](term_design_thinking.md)**: An iterative problem-solving methodology that operationalizes several of Polya's heuristics (decomposition, prototyping, reframing)
- **[MECE](term_mece.md)**: A decomposition heuristic — mutually exclusive, collectively exhaustive partitioning of a problem space
- **[Five Whys](term_five_whys.md)**: A root cause analysis heuristic — iterative "Why?" questioning to trace effects to causes
- **[Narrative Fallacy](term_narrative_fallacy.md)**: A bias produced by the representativeness heuristic — constructing coherent stories from random events

### In AI Search Algorithms (computational use of "heuristic")
- **[Best-First Search](term_best_first_search.md)**: Graph-search family that expands nodes in order of a heuristic evaluation function — the canonical CS use of "heuristic"
- **[A\* Search](term_a_star_search.md)**: Optimal best-first variant; admissibility ($h \le h^*$) and consistency are the two heuristic-quality properties that govern A\*'s correctness
- **[MCTS](term_mcts.md)**: Monte Carlo Tree Search — uses random rollouts as a stochastic heuristic estimate of node value

## References

### Vault Sources
- [Digest: How to Solve It](../digest/digest_how_to_solve_it_polya.md) — Polya's foundational text on heuristic reasoning; the four-step method and 67 named heuristic strategies
- [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md) — Kahneman's System 1/System 2 framework; cognitive heuristics as automatic mental processes that produce systematic biases
- [Digest: The 5 Elements of Effective Thinking](../digest/digest_effective_thinking_burger.md) — Burger/Starbird's five thinking habits operationalize Polya's heuristic strategies for non-mathematical domains
- [Digest: Algorithms to Live By](../digest/digest_algorithms_to_live_by_christian.md) — Christian/Griffiths bridge computational heuristics (explore/exploit, optimal stopping) with everyday decision making
- [Digest: Strategic Problem Solving](../digest/digest_strategic_problem_solving_hartley.md) — Hartley's seven-step framework modernizes Polya's heuristic method with data analysis and stakeholder communication
- [Digest: A More Beautiful Question](../digest/digest_beautiful_question_berger.md) — Berger's questioning framework is a heuristic for discovery: Why → What If → How

### External Sources
- [Polya, G. (1945). *How to Solve It*. Princeton University Press](https://press.princeton.edu/books/paperback/9780691119663/how-to-solve-it) — the foundational text on heuristic reasoning as a teachable discipline
- [Tversky, A. & Kahneman, D. (1974). "Judgment Under Uncertainty: Heuristics and Biases." *Science*, 185(4157)](https://www.science.org/doi/10.1126/science.185.4157.1124) — the landmark paper establishing the heuristics-and-biases program
- [Simon, H.A. (1956). "Rational choice and the structure of the environment." *Psychological Review*, 63(2)](https://psycnet.apa.org/record/1957-01652-001) — introduced bounded rationality and satisficing
- [Gigerenzer, G. et al. (1999). *Simple Heuristics That Make Us Smart*. Oxford University Press](https://global.oup.com/academic/product/simple-heuristics-that-make-us-smart-9780195143812) — the fast-and-frugal heuristics program; argues heuristics are ecologically rational
- [Wikipedia: Heuristic](https://en.wikipedia.org/wiki/Heuristic) — overview of the concept across traditions
- [Wikipedia: Heuristic (computer science)](https://en.wikipedia.org/wiki/Heuristic_(computer_science)) — computational heuristics and metaheuristics
- [Britannica: Heuristic Reasoning](https://www.britannica.com/topic/heuristic-reasoning) — definition, etymology, and historical development
- [Groner, M. et al. (2023). "A brief history of heuristics." *Humanities and Social Sciences Communications*, 10(1)](https://www.nature.com/articles/s41599-023-01542-z) — comprehensive historical survey of the heuristic concept across all traditions
