---
tags:
  - resource
  - terminology
  - prompting
  - innovation
  - meta_science
  - nlp
keywords:
  - prompt exaptation
  - prompt engineering
  - borrowed techniques
  - cognitive exaptation
  - chain of thought origin
  - few-shot prompting origin
  - role-playing prompts
  - pedagogical transfer
  - human-to-LLM transfer
  - prompting taxonomy
  - exaptation
  - adjacent possible
topics:
  - Prompt Engineering
  - Innovation Patterns
  - Meta-Science
  - Cognitive Science
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Prompt Exaptation

## Definition

**Prompt Exaptation** is the pattern in LLM prompt engineering where techniques originally developed in human cognitive, pedagogical, or professional domains are repurposed for LLM interaction, producing capabilities not predicted by the technique's original context. The term applies the [Architectural Exaptation](term_architectural_exaptation.md) framework — borrowed from evolutionary biology (Gould & Vrba, 1982) — to the prompting domain: just as deep learning architectures progress through component reuse rather than invention, prompt engineering advances primarily by exapting human practices into LLM interfaces. The canonical example is [Chain of Thought](term_chain_of_thought.md) prompting (Wei et al., 2022): the pedagogical technique of "showing your work" — developed for mathematics education to help students externalize reasoning — was exapted into LLM prompting, where it enables multi-step inference that standard prompting cannot achieve. Prompt exaptation is the dominant mode of innovation in prompt engineering: nearly every major prompting technique traces back to a pre-existing human practice.

## Full Name

**Prompt Exaptation** (also: Cognitive-to-Prompt Transfer, Prompting by Analogy)

**Also Known As**: Prompt borrowing, technique transfer to prompts, human-practice-to-prompt mapping

## Taxonomy of Prompt Exaptations

### Level 1: Direct Exaptation (Human Practice → LLM Prompt)

Individual techniques from human cognitive or professional domains repurposed as prompting strategies:

| Prompting Technique | Source Domain | Original Purpose | Exapted Purpose in LLM | Year |
|---------------------|-------------|-----------------|----------------------|------|
| **[Chain of Thought](term_chain_of_thought.md)** | Mathematics pedagogy ("show your work") | Help students externalize reasoning steps | Enable LLMs to solve multi-step problems via intermediate tokens | 2022 |
| **Few-shot prompting** | Pedagogy (worked examples) | Demonstrate expected performance via exemplars | In-context learning without weight updates | 2020 |
| **Zero-shot CoT** ("Let's think step by step") | Metacognitive self-talk | Regulate one's own thinking process | Activate reasoning capability without exemplars | 2022 |
| **Role-playing** ("You are an expert in...") | Theater / method acting | Embody a character's knowledge and perspective | Activate domain-specific knowledge distributions | 2022-23 |
| **[Socratic prompting](term_socratic_questioning.md)** | Socratic method (philosophy, 400 BC) | Probe assumptions through directed questions | Force LLMs to examine and justify their reasoning | 2023 |
| **Least-to-Most** | Scaffolding (Vygotsky, ZPD) | Build complexity gradually within zone of proximal development | Decompose problems for compositional generalization | 2022 |
| **Self-Consistency** | Ensemble methods / democratic voting | Aggregate multiple independent judgments | Sample multiple reasoning paths, majority-vote the answer | 2022 |
| **Tree of Thought** | Search algorithms (BFS/DFS) | Systematically explore solution spaces | Structured reasoning with backtracking over thought branches | 2023 |
| **Constitutional AI prompting** | Legal/ethical frameworks (constitutions) | Establish behavioral norms through codified principles | Self-critique and alignment through principle-based revision | 2022 |
| **Debate prompting** | Adversarial legal proceedings | Surface truth through opposing arguments | Multiple LLM agents argue opposing positions to improve accuracy | 2023 |

### Level 2: Cross-Domain Prompt Exaptation (Prompt Technique → New Domain)

Once a prompting technique is established, it gets exapted *again* into domains far from its original application:

| Technique | Original LLM Domain | Exapted Domain | Surprise Factor |
|-----------|---------------------|---------------|-----------------|
| **CoT** | Math word problems (GSM8K) | Code generation, scientific reasoning, abuse investigation ([GreenTEA](term_greentea.md)), ethical analysis | High — "show your work" for non-math tasks |
| **Few-shot** | NLP classification | Image generation (DALL-E), audio (Whisper), tabular (TabPFN) | Very high — text exemplars for non-text tasks |
| **Role-playing** | Knowledge QA | Creative writing, therapy simulation, red-teaming, [investigator-LLM interaction](term_ari.md) | Moderate — natural extension of persona |
| **Self-Consistency** | Arithmetic reasoning | Medical diagnosis, legal analysis, code review | Moderate — voting works across domains |

### Level 3: Reverse Exaptation (LLM Prompt Insights → Human Practice)

The rarest and most theoretically interesting: insights from LLM prompting exapted *back* into human cognitive practices:

| LLM Finding | Reverse Application | Status |
|-------------|-------------------|--------|
| CoT improves reasoning by externalizing intermediate steps | Renewed emphasis on "think aloud" protocols in education and decision-making | Active |
| Role-playing activates domain-specific knowledge | "Cognitive role-switching" in problem-solving workshops | Emerging |
| Self-consistency (multiple attempts + voting) improves accuracy | Structured group deliberation protocols in organizations | Active |
| Constitutional AI (principle-based self-critique) | Principle-based decision frameworks for human teams | Emerging |

## Why Prompts Are Uniquely Exaptable

Four properties make prompt engineering an unusually fertile ground for exaptation:

| Property | Mechanism | Comparison to Architecture Exaptation |
|----------|-----------|---------------------------------------|
| **Natural language interface** | Prompts use human language, so *any* human communication technique is a candidate for transfer | Architecture exaptation requires technical implementation; prompt exaptation requires only natural language |
| **Zero-cost transfer** | No training, no code changes — pure inference-time adaptation | Architecture changes require retraining; prompt changes are instantaneous |
| **Training data as bridge** | LLMs are trained on human text that *contains examples* of humans using these techniques (textbook solutions, Socratic dialogues, legal arguments) | Architecture components must be re-implemented; prompt techniques are already "in the weights" |
| **Low experimentation barrier** | Anyone with API access can test a new prompting technique | Architecture changes require ML engineering expertise |

The training data bridge is the critical mechanism: CoT works (hypothesis) because the pretraining corpus contains millions of examples of humans "showing their work" in textbooks, forum posts, and tutorials. The prompt doesn't *teach* the model to reason step-by-step — it *activates* reasoning patterns already encoded from training data where humans used the same technique.

## The Adjacent Possible of Prompt Exaptation

Applying Steven Johnson's [adjacent possible](term_architectural_exaptation.md) framework: each successful prompt exaptation expands the space of conceivable prompting techniques.

```
Pedagogy ──→ Few-shot (2020) ──→ CoT (2022) ──→ Zero-shot CoT (2022)
                                      │
Search ────────────────────────────────┼──→ Tree of Thought (2023)
                                      │
Ensemble ──────────────────────────────┼──→ Self-Consistency (2022)
                                      │
Scaffolding ───────────────────────────┼──→ Least-to-Most (2022)
                                      │
Verification ──────────────────────────┴──→ Process Reward Models (2023)
```

CoT was the **keystone exaptation**: once it demonstrated that structuring the prompt could unlock capabilities invisible to standard prompting, it opened the adjacent possible for all subsequent reasoning-focused techniques. Without CoT, Tree of Thought, Self-Consistency, and PRM would likely not have been conceived in their current form.

## Connection to Architectural Exaptation

Prompt exaptation operates at **Level 3 (paradigm exaptation)** in the [Architectural Exaptation](term_architectural_exaptation.md) taxonomy — entire problem-solving paradigms from human cognition are transferred to the LLM interaction layer:

| Level | Architectural Example | Prompt Example |
|-------|----------------------|----------------|
| **Level 1: Component** | RMSNorm from GPT-3 → LLaMA | "Let's think step by step" from metacognition → Zero-shot CoT |
| **Level 2: Pattern** | Pre-train → fine-tune from NLP → all domains | CoT from math → code, science, abuse investigation |
| **Level 3: Paradigm** | Self-supervised learning from NLP → vision | Human pedagogy → entire prompt engineering field |

The key difference: architectural exaptation transfers *computational components* between models; prompt exaptation transfers *cognitive strategies* between humans and models. Both follow the same innovation dynamic — recombination outperforms invention — but operate at different layers of the stack.

## Implications for Prompt Engineering Research

| Strategy | Description | Expected Value |
|----------|-------------|---------------|
| **Systematic mining** | Survey human cognitive/pedagogical/professional techniques and test each as a prompting strategy | High — large unexplored space (therapy, coaching, debugging, scientific method) |
| **Cross-domain transfer** | Take a prompting technique proven in one domain and test it in unrelated domains | Moderate-high — Level 2 exaptation has high success rate |
| **Reverse engineering** | Analyze successful but unexplained prompts; trace back to the human practice they implicitly exapt | Moderate — explains why techniques work, enabling principled improvement |
| **Reverse exaptation** | Take LLM prompting insights and test whether they improve human cognitive performance | Novel — least explored, highest potential for cognitive science contribution |

## Applications to Our Work

- **Prompt design for abuse detection**: When designing prompts for [GreenTEA](term_greentea.md) or [ARI](term_ari.md), systematically mine investigator cognitive strategies (pattern matching, red-flagging, escalation heuristics) as candidates for prompt exaptation — the investigator's mental process may directly translate into effective prompting
- **[SPOT-X](term_spot_x.md) reasoning traces**: SPOT-X's chain-of-thought decision rules are a Level 2 exaptation of CoT from math reasoning into abuse classification — understanding this lineage helps evaluate which CoT properties (interpretability, decomposition) transfer and which (verifiability, mathematical rigor) do not
- **Cross-team prompting knowledge**: Techniques proven in one abuse detection domain (e.g., CoT for DNR classification) can be systematically exapted to other domains (e.g., CoT for A-to-Z investigation) — the exaptation framework provides a structured methodology for prompt reuse

## Questions

### Validation (Socratic)
1. The "training data as bridge" hypothesis — that CoT works because pretraining data contains millions of examples of humans showing their work — is presented as the leading explanation for why prompt exaptation succeeds. But what information is *missing* from this hypothesis? If the bridge mechanism is correct, prompt exaptation should fail for human practices that are (a) rare in web text, (b) primarily oral/gestural, or (c) culturally specific. What is the base rate of prompt exaptation *failure*, and does it correlate with the frequency of the source practice in training corpora? *(WYSIATI lens)*
2. The taxonomy presents prompt exaptation as a *deliberate innovation strategy* (systematically mining human practices for prompting ideas). But historically, most prompt exaptations were *discovered accidentally* — Wei et al. did not set out to "exapt pedagogy"; they tried adding reasoning steps and it worked. Is prompt exaptation better modeled as a *post-hoc explanatory framework* (recognizing borrowed origins after the fact) or a *generative methodology* (predicting which human practices will transfer before testing)? What evidence distinguishes these two interpretations? *(Framing Check lens)*

### Application (Taxonomic)
3. The note identifies "systematic mining" of human cognitive techniques as a high-expected-value strategy. Apply this concretely: what are the top 5 *untested* human cognitive/professional practices most likely to produce effective prompting techniques? Consider debugging (rubber duck debugging → "explain to a novice"), scientific method (hypothesis → experiment → revision → prompt cycle), meditation (focused attention → constrained generation), forensic investigation (evidence chains → structured evidence prompting), and coaching (motivational interviewing → preference elicitation). Which has the strongest transfer case? *(Adjacent Possible lens)*
4. Reverse exaptation (LLM prompting insights → improved human practice) is flagged as "least explored, highest potential." Can you elaborate on a concrete test? For example: if Self-Consistency (multiple reasoning paths + voting) improves LLM accuracy by 10-20%, would implementing the same protocol in human decision-making (have each team member independently reason, then vote) produce similar gains? What organizational experiment would test this? *(Elaborative Depth lens)*

### Synthesis (Lateral)
5. The [Scaling Law](term_scaling_law.md) note shows that CoT emergence requires ~100B parameters — below this threshold, CoT *degrades* performance. If CoT is an exaptation of human pedagogy, and human pedagogy works for humans of all "parameter counts" (i.e., children can benefit from "show your work"), what does the scale threshold tell us about the *difference* between how humans and LLMs process exapted techniques? Does this imply that smaller models lack the "training data bridge" (insufficient examples of humans reasoning step-by-step in pretraining), or that they lack the *computational capacity* to execute multi-step reasoning regardless of prompt format? *(Liquid Network lens — bridging with term_scaling_law)*
6. [Constitutional AI](term_constitutional_ai.md) prompting is listed as an exaptation of legal/ethical frameworks. But CAI operates at the *training* level (RLAIF), not just the *prompting* level — the constitutional principles are used to generate preference data that modifies model weights. Does this make CAI a *prompt exaptation* (the principles are expressed as prompts) or an *architectural exaptation* (the principles modify the model's behavior through training)? This boundary case tests whether the prompt/architecture distinction in the exaptation taxonomy is clean or whether there is a continuum. -> Follow-up: [[term_prompt_architecture_boundary]] *(Exaptation lens — testing the taxonomy's own boundaries)*

## Related Terms

### Core Framework
- [Architectural Exaptation](term_architectural_exaptation.md) — Parent concept; prompt exaptation is a specific instance of Level 3 paradigm exaptation applied to the prompting domain
- [Chain of Thought](term_chain_of_thought.md) — Canonical example of prompt exaptation; pedagogy ("show your work") exapted into LLM reasoning
- [Socratic Questioning](term_socratic_questioning.md) — Source domain for Socratic prompting; philosophy exapted into LLM interrogation

### Prompting Techniques (Exaptation Instances)
- [LLM](term_llm.md) — The models whose natural language interface enables prompt exaptation
- [Scaling Law](term_scaling_law.md) — CoT emergence threshold (~100B) constrains which prompt exaptations are effective at which scales
- [System 1 and System 2](term_system_1_and_system_2.md) — Cognitive framework exapted into prompt design: standard prompting elicits System 1, CoT externalizes System 2

### Production Systems Using Prompt Exaptation
- [GreenTEA](term_greentea.md) — Uses CoT-style reasoning (Level 2 exaptation from math to abuse investigation)
- [SPOT-X](term_spot_x.md) — Generates chain-of-thought decision rules (Level 2 exaptation from reasoning to classification)
- [ARI](term_ari.md) — Investigator-LLM interaction using role-playing and CoT prompts

### Innovation Framework
- [Design Thinking](term_design_thinking.md) — Human-centered methodology; a candidate source domain for future prompt exaptation
- [Question Storming](term_question_storming.md) — Brainstorming variant; exapted into prompt generation strategies
- [Constitutional AI](term_constitutional_ai.md) — Boundary case between prompt and architectural exaptation

### Key Papers
- [Wei et al. (2022)](../papers/lit_wei2022chain.md) — CoT paper; canonical prompt exaptation from pedagogy
- [LLaMA (Touvron et al., 2023)](../papers/lit_touvron2023llama.md) — Architectural exaptation paper from which the broader exaptation framework was developed

## References

### Prompt Exaptation Instances
- Wei, J. et al. (2022). [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](../papers/lit_wei2022chain.md). NeurIPS. arXiv:2201.11903. *Canonical prompt exaptation: mathematics pedagogy → LLM reasoning.*
- Kojima, T. et al. (2022). Large Language Models are Zero-Shot Reasoners. NeurIPS. *Zero-shot CoT: metacognitive self-talk → LLM prompt.*
- Wang, X. et al. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. arXiv:2203.11171. *Ensemble voting → prompt strategy.*
- Yao, S. et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. *Search algorithms (BFS/DFS) → structured LLM reasoning.*
- Bai, Y. et al. (2022). [Constitutional AI: Harmlessness from AI Feedback](../papers/lit_bai2022constitutional.md). arXiv:2212.08073. *Legal/ethical frameworks → self-critique prompting.*

### Exaptation Theory
- Gould, S.J. & Vrba, E.S. (1982). Exaptation — A Missing Term in the Science of Form. *Paleobiology*, 8(1), 4-15.
- Johnson, S. (2010). *Where Good Ideas Come From: The Natural History of Innovation*. Riverhead Books.

### Cognitive Source Domains
- Vygotsky, L.S. (1978). *Mind in Society: Development of Higher Psychological Processes*. Harvard University Press. *Zone of proximal development → scaffolding → Least-to-Most prompting.*
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. *System 1/System 2 → standard vs. CoT prompting framing.*
- Source: [Digest: Where Good Ideas Come From](../digest/digest_good_ideas_johnson.md) — Johnson's adjacent possible and exaptation as innovation patterns
