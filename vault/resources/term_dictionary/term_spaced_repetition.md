---
tags:
  - resource
  - terminology
  - learning_science
keywords:
  - spaced repetition
  - distributed practice
  - spacing effect
  - Ebbinghaus
  - forgetting curve
  - Leitner system
  - SuperMemo
  - Anki
  - SRS
  - massed practice
topics:
  - learning science
  - cognitive psychology
  - study techniques
  - knowledge retention
language: markdown
date of note: 2026-03-07
status: active
building_block: concept
---

# Term: Spaced Repetition

## Definition

**Spaced repetition** (also called **distributed practice**) is a learning technique in which review sessions are distributed over increasing time intervals rather than concentrated into a single intensive session (massed practice or cramming). The method exploits a fundamental property of human memory: the **spacing effect**, which holds that information is retained more effectively when study episodes are separated by gaps of time, particularly when those gaps allow some forgetting to occur before the next review.

The core mechanism is counterintuitive: the partial forgetting that occurs between spaced review sessions forces the learner to engage in more effortful retrieval, which strengthens the memory trace far more than easy, immediate re-exposure. As Brown, Roediger, and McDaniel write in *Make It Stick*, "When learning is spaced, forgetting is the friend of learning." This makes spaced repetition a canonical example of a desirable difficulty -- a strategy that feels harder during practice but produces dramatically superior long-term retention.

Spaced repetition has one of the longest research histories of any learning technique, dating to Hermann Ebbinghaus's pioneering self-experiments in the 1880s. A comprehensive 2006 meta-analysis of 317 studies by Cepeda et al. confirmed the superiority of distributed practice over massed practice across a wide range of materials, retention intervals, and learner populations. Modern spaced repetition systems (SRS) such as Anki and SuperMemo use algorithms to automate optimal scheduling of review intervals for thousands of items simultaneously.

## Full Name

Also known as:
- **Distributed practice** (the academic/research term)
- **Spaced practice** (informal synonym)
- **Spacing effect** (the underlying cognitive phenomenon)
- **SRS** -- Spaced Repetition System (the software/tool category)

Contrast with:
- **Massed practice** / **cramming** -- concentrating all study into a single session with no spacing
- **Blocked practice** -- practicing one topic exhaustively before moving to the next

## History and Development

### Timeline of Key Milestones

| Year | Event |
|------|-------|
| **1885** | Hermann Ebbinghaus publishes *Uber das Gedachtnis* (*On Memory*), documenting the **forgetting curve** and discovering the spacing effect through self-experimentation with nonsense syllables |
| **1917** | Arthur Gates demonstrates that children retain more when recitation time is distributed over sessions |
| **1939** | Herbert Spitzer shows that spaced testing in schools improves retention over 63 days |
| **1973** | Sebastian Leitner publishes *So lernt man lernen* ("Learning to Learn"), introducing the **Leitner system** -- a flashcard-based spaced repetition method using graduated boxes |
| **1985** | Piotr Wozniak formulates the first mathematical algorithm for optimal spacing intervals |
| **1987** | Wozniak creates **SuperMemo 1.0** for DOS -- the first computer-based spaced repetition system, using the SM-2 algorithm |
| **2006** | Cepeda et al. publish a meta-analysis of 317 experiments confirming the spacing effect across diverse contexts |
| **2006** | Damien Elmes releases **Anki**, a free open-source SRS that becomes the most widely used spaced repetition tool worldwide |
| **2014** | Brown, Roediger, and McDaniel feature spaced practice as one of seven core evidence-based strategies in *Make It Stick* |

### The Ebbinghaus Forgetting Curve

Ebbinghaus's foundational discovery was the **forgetting curve** -- a mathematical model showing that memory decays exponentially after initial learning, with the steepest decline occurring in the first hours and days. His critical finding was that each review session "resets" the curve with a shallower slope: after several well-timed reviews, the rate of forgetting slows dramatically, and the memory approaches permanent retention.

### The Leitner System

Sebastian Leitner's 1973 system organized flashcards into a series of boxes (typically 3-5). New or incorrectly answered cards go into Box 1 (reviewed daily). Cards answered correctly advance to Box 2 (reviewed every few days), then Box 3 (weekly), and so on. Incorrect answers at any stage send the card back to Box 1. This simple mechanical system implements the core principle of spaced repetition without requiring any technology.

## Why Spaced Repetition Works

### Cognitive Mechanisms

1. **Effortful retrieval**: Forgetting between sessions forces the learner to reconstruct the memory with greater effort, which strengthens the trace (aligned with Bjork's desirable difficulties framework)
2. **Encoding variability**: Each review occurs in a slightly different context (mood, environment, time of day), creating multiple retrieval cues and making the memory more robust
3. **Consolidation cycles**: Spacing allows time for memory consolidation -- the biological process by which short-term memories are stabilized into long-term storage, with sleep playing a crucial role
4. **Retrieval route multiplication**: Each successful spaced retrieval creates additional neural pathways to the stored information

### The Spacing-Retention Interaction

Research reveals an important nuance: the **optimal spacing interval depends on the desired retention interval**. Cepeda et al. (2008) found that for a desired retention of 1 week, the optimal gap between study sessions is approximately 1 day; for 1 month retention, the optimal gap is about 1 week; for 1 year retention, approximately 3-4 weeks between reviews. This has been formalized as the "optimal gap ratio."

### Recommended Spacing Schedule

A practical schedule from *Make It Stick*:
- Review new material within **the same day**
- Revisit after **several days** (2-3 days)
- Again after **1 week**
- Again after **2-4 weeks**
- **Monthly** reviews for well-mastered material

## Key Research and Evidence

| Study | Year | Key Finding |
|-------|------|-------------|
| **Ebbinghaus** | 1885 | Discovered the spacing effect and forgetting curve through self-experimentation |
| **Spitzer** | 1939 | 3,600 students -- spaced testing improved long-term retention in schools |
| **Dempster** | 1988 | Review of 100+ years of spacing research; called it "one of the most dependable and replicable phenomena in experimental psychology" |
| **Cepeda et al.** | 2006 | Meta-analysis of 317 experiments: spacing consistently superior to massing across ages, materials, and retention intervals |
| **Cepeda et al.** | 2008 | Optimal gap between sessions depends on desired retention interval (gap-retention interaction) |
| **Karpicke & Bauernschmidt** | 2011 | Combined spacing with retrieval practice produces the strongest learning outcomes |

## Practical Applications

### Modern Spaced Repetition Software (SRS)

| Tool | Algorithm | Notes |
|------|-----------|-------|
| **SuperMemo** | SM-2 through SM-18 | First SRS (1987); Wozniak's original; most advanced algorithms |
| **Anki** | Modified SM-2 / FSRS | Free, open-source; most popular SRS worldwide; cross-platform |
| **Mnemosyne** | Modified SM-2 | Open-source; research-oriented |
| **Quizlet** | Proprietary | Popular commercial platform; less rigorous spacing than dedicated SRS |
| **RemNote** | Proprietary | Combines SRS with note-taking |

### In Knowledge Management and Zettelkasten

Spaced repetition aligns naturally with SlipBox / Zettelkasten practices:

- **Periodic note review**: Revisiting and refining notes at increasing intervals embodies the spacing principle
- **Graph-based surfacing**: A SlipBox can surface notes for review based on their age, connectivity, and staleness -- functioning as an organic SRS
- **Progressive summarization**: Each review pass is an opportunity to refine, compress, and deepen the note -- combining spacing with elaboration
- **Stub-to-active workflow**: Notes begin as stubs and are progressively expanded over time, with each visit serving as a spaced retrieval and elaboration event

### In Education and Training

- Design curricula with **cumulative review** built into every session (not just new material)
- Use **low-stakes quizzes** that revisit earlier topics at expanding intervals
- Assign **homework that interleaves** current and past material
- Communicate to students that the difficulty of spaced review is a feature, not a flaw

## Criticisms and Limitations

- **Requires planning and discipline**: Unlike cramming, spaced repetition demands advance scheduling and consistent follow-through; many learners abandon the practice
- **Diminished returns for procedural skills**: The spacing effect is strongest for declarative (factual) knowledge; motor and procedural skills may benefit more from massed practice in early stages
- **Optimal intervals are uncertain in practice**: While the spacing effect is robust, determining the exact optimal interval for a given item and learner remains an open research question
- **Metacognitive illusion**: Massed practice produces rapid visible gains that feel productive; spaced practice feels slower and more frustrating, leading many learners to prefer the less effective strategy (Kornell, 2009)
- **Not a substitute for understanding**: Spacing optimizes retention of already-understood material; it cannot compensate for poor initial comprehension
- **Algorithm limitations**: SRS algorithms assume a simplified model of memory; individual variation in forgetting rates, sleep quality, and prior knowledge is difficult to capture

## Related Terms

- [Term: Retrieval Practice](term_retrieval_practice.md) -- spaced repetition is most effective when combined with retrieval practice at each review session
- [Term: Desirable Difficulties](term_desirable_difficulties.md) -- spacing is a canonical desirable difficulty; the forgetting between sessions is the productive struggle
- Term: Interleaving -- interleaving naturally introduces spacing between repetitions of a given topic
- [Term: Elaborative Interrogation](term_elaborative_interrogation.md) -- asking "why" during spaced review sessions deepens encoding at each repetition
- Term: Cognitive Bias -- the fluency of massed practice creates a bias toward believing cramming works better
- Term: System 1 and System 2 -- spaced repetition forces System 2 effortful retrieval rather than System 1 familiarity
- Term: Availability Heuristic -- recently crammed material is highly "available" (easy to recall) but not durably stored
- [Term: Zettelkasten](term_zettelkasten.md) -- periodic note review in a Zettelkasten embodies spaced repetition
- [Term: SlipBox](term_slipbox.md) -- SlipBox note lifecycle (stub to active) naturally implements spaced review
- [Compound Effect](term_compound_effect.md) -- spaced repetition is compounding applied to memory; each review session builds on prior sessions exponentially
- Deliberate Practice -- spaced scheduling is a deliberate practice technique that structures practice across time for optimal retention
- [Progressive Summarization](term_progressive_summarization.md) — each revisit-and-layer cycle creates natural spaced repetition for the note's content

## References

- Source: Digest: Make It Stick
- Source: [Digest: How to Take Smart Notes](../digest/digest_smart_notes_ahrens.md) — periodic review of slip-box notes creates natural spaced repetition
- [Wikipedia: Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) -- comprehensive overview of history, research, and software implementations
- [Wikipedia: Forgetting Curve](https://en.wikipedia.org/wiki/Forgetting_curve) -- Ebbinghaus's foundational discovery
- [Bjork Lab -- Desirable Difficulties](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf) -- framework paper covering spacing as a desirable difficulty
- [SuperMemo -- The True History of Spaced Repetition](https://www.supermemo.com/en/blog/the-true-history-of-spaced-repetition) -- Piotr Wozniak's comprehensive account of SRS development
- [Cepeda et al. (2006) -- Distributed Practice in Verbal Recall Tasks](https://psycnet.apa.org/record/2006-04897-002) -- meta-analysis of 317 experiments confirming the spacing effect

---

**Last Updated**: March 7, 2026
**Status**: Active -- learning science terminology
