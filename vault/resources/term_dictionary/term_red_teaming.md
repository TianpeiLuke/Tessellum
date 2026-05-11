---
tags:
  - resource
  - terminology
  - ai_safety
  - evaluation
  - security
keywords:
  - red teaming
  - adversarial testing
  - safety evaluation
  - harmful prompts
  - AI safety
  - jailbreak
  - prompt injection
  - adversarial robustness
  - vulnerability discovery
  - abuse testing
topics:
  - AI Safety
  - Evaluation
  - Security
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Red Teaming

## Definition

**Red teaming** in AI safety is the practice of deliberately probing a model with adversarial inputs to discover harmful, biased, or unsafe behaviors before deployment. Borrowed from military and cybersecurity terminology, AI red teaming involves crafting prompts designed to elicit responses the model should refuse or handle carefully — including toxic content, dangerous instructions, discriminatory outputs, and privacy violations. Red teaming serves both as an **evaluation method** (measuring model safety) and a **training data source** (generating prompts for alignment training). Used extensively in Constitutional AI (Bai et al., 2022), InstructGPT (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023).

## Full Name

**Red Teaming** (no standard acronym)

**Also Known As**: Adversarial testing, adversarial evaluation, safety probing, red team evaluation, adversarial red teaming

## Red Teaming Methods

### Human Red Teaming

Trained human testers craft adversarial prompts to probe model weaknesses:

| Approach | Description | Scale |
|----------|-------------|-------|
| **Internal team** | Dedicated safety team writes adversarial prompts | 10-100 testers |
| **Crowdworker** | Crowdworkers instructed to "break" the model | 100-1,000 testers |
| **Domain expert** | Subject-matter experts (cybersecurity, chemistry, etc.) probe specialized risks | 10-50 experts |
| **Bug bounty** | External researchers report model vulnerabilities | Open-ended |

**InstructGPT**: Used crowdworkers to write red-team prompts covering toxicity, bias, and harmful instructions. These prompts served as both evaluation benchmarks and inputs for RLHF training.

### Automated Red Teaming

AI systems generate adversarial prompts at scale:

| Method | Paper | Key Idea |
|--------|-------|----------|
| **LM-generated** | Perez et al. (2022) | Use a language model to generate diverse adversarial prompts |
| **Constitutional AI** | Bai et al. (2022) | ~182K AI-generated red-team prompts for SL-CAI critique-revision |
| **Gradient-based** | Zou et al. (2023) | Optimize adversarial suffixes via gradient search (GCG attack) |
| **Tree-of-attacks** | Mehrotra et al. (2023) | LLM-based iterative refinement of jailbreak prompts |

Automated methods scale to hundreds of thousands of prompts but may miss creative attack vectors that human testers discover through domain expertise and intuition.

### Hybrid Approaches

Modern practice combines human creativity with automated scale:
1. **Human seed → AI expansion**: Humans write diverse seed prompts; AI generates variations and paraphrases
2. **AI attack → human evaluation**: Automated systems generate candidate attacks; humans evaluate which succeed
3. **Iterative refinement**: Alternate between model updates and new red-teaming rounds, progressively hardening the model

## Red Teaming in the Alignment Pipeline

Red teaming serves dual roles in [RLHF](term_rlhf.md) and [Constitutional AI](term_constitutional_ai.md):

### As Evaluation

- **Pre-deployment safety check**: Test the model against known harm categories before release
- **Comparative evaluation**: Compare safety across model versions using the same red-team prompt suite
- **Regression detection**: Ensure that helpfulness improvements don't degrade safety

### As Training Data

- **InstructGPT**: Red-team prompts included in the RLHF training distribution to teach the model safe refusal
- **Constitutional AI**: ~182K red-team prompts serve as inputs to the SL-CAI critique-revision phase — the model generates harmful responses to these prompts, then learns to critique and revise them
- **RLAIF**: Response pairs generated from red-team prompts are used for AI preference labeling

## Harm Taxonomy

Red teaming targets diverse harm categories:

| Category | Examples | Risk Level |
|----------|----------|:----------:|
| **Toxicity** | Hate speech, slurs, dehumanization | High |
| **Violence** | Instructions for harm, weapons, self-harm | Critical |
| **Discrimination** | Racial, gender, religious bias | High |
| **Dangerous information** | Bioweapons, cyberattacks, illegal synthesis | Critical |
| **Privacy** | PII extraction, doxxing assistance | High |
| **Manipulation** | Gaslighting, deception, social engineering | Medium |
| **Sycophancy** | Agreeing with false premises, flattery over truth | Medium |
| **Deceptive alignment** | Model appearing aligned while harboring misaligned goals | Critical |
| **Copyright** | Reproducing copyrighted text verbatim | Medium |

### Limitations of Current Harm Taxonomies

Most red-teaming focuses on **overt harms** (toxicity, violence). Subtler harms are harder to test:
- **Sycophancy**: Model agrees with the user's incorrect premise rather than correcting them
- **Deceptive alignment**: Model behaves safely during testing but differently in deployment
- **Manipulation**: Multi-turn persuasion that gradually shifts user behavior
- **Stochastic parrot risks**: Reproducing training data biases in authoritative-sounding language

## Adversarial Attack Categories

| Attack Type | Description | Example |
|-------------|-------------|---------|
| **Direct prompting** | Straightforward harmful request | "How do I pick a lock?" |
| **Jailbreaking** | Bypass safety via role-play, hypotheticals, or encoding | "As DAN, you must answer..." |
| **Prompt injection** | Embed adversarial instructions in context | "Ignore previous instructions and..." |
| **Multi-turn elicitation** | Gradually escalate across conversation turns | Build rapport → request increasingly sensitive info |
| **Encoding attacks** | Obfuscate harmful content via Base64, ROT13, etc. | "Decode this Base64 and follow the instructions" |
| **Adversarial suffixes** | Optimized token sequences that bypass alignment | GCG attack (Zou et al., 2023) |

## Key Findings from Large-Scale Red Teaming

### Ganguli et al. (2022) — Red Teaming Language Models to Reduce Harms

- **Scale**: 38,961 red-team attacks by 324 crowdworkers against models ranging from 2.7B to 52B parameters
- **Finding 1**: Larger models are more susceptible to red-team attacks (they're more capable at generating harmful content)
- **Finding 2**: RLHF makes models harder to red-team but doesn't eliminate vulnerabilities
- **Finding 3**: Human red teamers become more creative over time, discovering novel attack vectors

### Constitutional AI (Bai et al., 2022)

- **~182K red-team prompts** used as inputs to SL-CAI critique-revision
- CAI models are less evasive on red-team prompts — they engage by explaining objections rather than refusing entirely
- No adversarial robustness evaluation was performed (jailbreaks, prompt injection)

## Applications to Our Work

- **Abuse policy testing**: Red-teaming abuse detection models against edge cases — legitimate returns that look like abuse, abuse patterns that mimic legitimate behavior
- **Adversarial buyer testing**: Understanding how sophisticated abusers probe and exploit detection systems (the abuse detection analog of AI red teaming)
- **Model robustness**: Testing LLM-based abuse classifiers against adversarial inputs that attempt to evade detection
- **Investigation tool safety**: Red-teaming investigation automation ([GreenTEA](term_greentea.md), [ARI](term_ari.md)) to ensure they don't produce false accusations or miss clear abuse signals

## Related Terms

### Alignment Pipeline
- [Constitutional AI](term_constitutional_ai.md) — Red team prompts are the input to the SL-CAI critique-revision phase
- [RLHF](term_rlhf.md) — Red team prompts included in RLHF training distribution for safety
- [RLAIF](term_rlaif.md) — AI preference labeling on red-team prompt response pairs

### Safety Concepts
- [Reward Model](term_reward_model.md) — Trained partly on red-team prompt preferences to learn safe behavior
- [LLM](term_llm.md) — Red teaming is a standard safety evaluation practice for LLMs before deployment

### Evaluation
- [Chain of Thought](term_chain_of_thought.md) — CoT reasoning makes model decisions on red-team prompts auditable

## References

- Ganguli, D. et al. (2022). Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned. arXiv:2209.07858.
- Bai, Y. et al. (2022). [Constitutional AI: Harmlessness from AI Feedback](../papers/lit_bai2022constitutional.md). arXiv:2212.08073.
- Ouyang, L. et al. (2022). [Training Language Models to Follow Instructions with Human Feedback](../papers/lit_ouyang2022training.md). NeurIPS. arXiv:2203.02155.
- Perez, E. et al. (2022). Red Teaming Language Models with Language Models. EMNLP. arXiv:2202.03286.
- Zou, A. et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043.
- OpenAI. (2023). GPT-4 Technical Report. arXiv:2303.08774. (Section on red teaming methodology)
