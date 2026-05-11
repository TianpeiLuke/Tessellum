---
tags:
  - resource
  - terminology
  - product_management
  - quality_management
  - customer_satisfaction
  - feature_prioritization
  - user_experience
keywords:
  - Kano Model
  - Kano analysis
  - Noriaki Kano
  - attractive quality theory
  - must-be quality
  - one-dimensional quality
  - delighters
  - feature prioritization
  - customer satisfaction
  - feature decay
  - functional dysfunctional questionnaire
topics:
  - Product Management
  - Quality Management
  - Customer Satisfaction
  - Feature Prioritization
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Kano Model

## Definition

The **Kano Model** is a theory of product development and customer satisfaction that classifies product or service features into categories based on their nonlinear relationship to customer satisfaction. Developed by Japanese quality researcher Noriaki Kano and colleagues in 1984, the model challenges the assumption that improving any feature proportionally increases satisfaction. Instead, it reveals that different feature types have fundamentally different satisfaction dynamics: some features only prevent dissatisfaction (must-haves), some scale linearly with investment (performance), and some create disproportionate delight when present but cause no dissatisfaction when absent (delighters). The framework provides a structured methodology for feature prioritization by helping product teams understand which features to invest in, which to ensure meet baseline expectations, and which offer opportunities for competitive differentiation.

## Historical Context

The Kano Model was formally introduced in 1984 by Professor Noriaki Kano along with co-authors Nobuhiko Seraku, Fumio Takahashi, and Shin-ichi Tsuji in the paper "Attractive Quality and Must-Be Quality" published in the *Journal of the Japanese Society for Quality Control*. Kano drew key inspiration from Frederick Herzberg's two-factor theory of motivation (which distinguishes hygiene factors from motivators) and Abraham Maslow's hierarchy of needs. The core insight was that customer satisfaction is not one-dimensional: the absence of certain features causes dissatisfaction, but their presence does not create satisfaction. This asymmetry was revolutionary in the quality management field of the 1980s, which had largely assumed linear relationships between product attributes and customer satisfaction.

The theory has since been adopted widely beyond Japanese manufacturing into software product management, UX design, and service design. Dan Olsen's *The Lean Product Playbook* (2015) prominently features the Kano Model as a key framework for identifying and prioritizing features in the Lean Product Process.

## Taxonomy

The Kano Model classifies features into five categories:

| Category | Also Called | When Present | When Absent | Satisfaction Curve |
|----------|-----------|--------------|-------------|-------------------|
| **Must-Be** | Basic, threshold, dissatisfiers | Neutral (expected) | Strong dissatisfaction | Asymptotic ceiling |
| **One-Dimensional** | Performance, satisfiers, linear | Proportional satisfaction | Proportional dissatisfaction | Linear |
| **Attractive** | Delighters, exciters, wow factors | Disproportionate delight | No dissatisfaction | Exponential rise |
| **Indifferent** | Neutral | No effect | No effect | Flat |
| **Reverse** | Anti-features | Dissatisfaction | Satisfaction | Inverted |

A sixth category, **Questionable**, captures contradictory survey responses that indicate the respondent misunderstood the question or the feature.

## Key Properties

- **Asymmetry of satisfaction**: Must-be features can only prevent dissatisfaction, never create satisfaction. This is the model's most counterintuitive and important insight.
- **Nonlinear dynamics**: Unlike traditional quality models, the relationship between feature investment and customer satisfaction is nonlinear and varies by category.
- **Feature decay over time**: Features migrate from Attractive to One-Dimensional to Must-Be as customer expectations rise and competitors adopt similar features. What delights today becomes expected tomorrow.
- **Hedonic adaptation**: The decay phenomenon is driven by the same psychological mechanism as the [hedonic treadmill](term_hedonic_treadmill.md) — customers adapt to improvements and recalibrate their baseline expectations.
- **Loss-aversion alignment**: Must-be features align with [loss aversion](term_loss_aversion.md) — their absence is felt more strongly than their presence, because customers frame missing basics as a loss.
- **Context dependence**: A feature's Kano category depends on the market segment, customer persona, and competitive landscape — not on the feature itself.
- **Measurable via questionnaire**: Categories are empirically determined using paired functional/dysfunctional survey questions, not assumed by the product team.
- **Prioritization heuristic**: Invest first in Must-Be (table stakes), then One-Dimensional (competitive differentiation), then Attractive (delight and loyalty).

## Notable Systems / Implementations

| Application | Mechanism | Domain |
|------------|-----------|--------|
| Kano Questionnaire | Paired functional/dysfunctional questions with 5-point scale | Survey methodology |
| Lean Product Process | Kano analysis integrated into feature prioritization step | Product management |
| Six Sigma / TQM | Kano analysis for Voice of Customer (VOC) translation | Quality management |
| UX Research | Kano surveys combined with usability testing | User experience |
| Agile Backlog Grooming | Kano categories inform story prioritization and sprint planning | Software development |

## Applications

| Domain | Application |
|--------|------------|
| **Product management** | Feature prioritization for roadmaps; identifying MVP scope (must-haves) vs. differentiators |
| **Quality management** | Voice of Customer analysis; understanding which quality dimensions matter most |
| **UX design** | Distinguishing hygiene features from delight opportunities in user interfaces |
| **Service design** | Mapping service attributes to satisfaction drivers for hospitality, healthcare, etc. |
| **Competitive strategy** | Identifying competitor table-stakes vs. differentiation opportunities |
| **Pricing** | Understanding willingness to pay by feature category — delighters command premium pricing |

## Challenges and Limitations

- **Static snapshot**: The Kano questionnaire captures a point-in-time classification; feature categories shift as markets evolve, requiring periodic re-evaluation.
- **Survey design complexity**: Writing good functional/dysfunctional question pairs is non-trivial; ambiguous questions produce high rates of "questionable" responses.
- **Segment sensitivity**: Results vary by customer segment, so aggregated Kano results can obscure important differences between personas.
- **No magnitude measurement**: The model classifies features into categories but does not quantify the strength of satisfaction or dissatisfaction within a category.
- **Assumes feature independence**: The model evaluates features in isolation, not accounting for interaction effects between features.

## Related Terms

- **[Hedonic Treadmill](term_hedonic_treadmill.md)**: The psychological adaptation mechanism that explains why Kano feature categories decay over time — customers adapt to improvements and reset expectations.
- **[Loss Aversion](term_loss_aversion.md)**: Explains the asymmetry in must-be features — the pain of a missing basic feature exceeds the satisfaction from its presence.
- **[Lean](term_lean.md)**: The Lean Product Process integrates Kano analysis as a key step in identifying underserved customer needs and prioritizing features.
- **[PR/FAQ](term_prfaq.md)**: Amazon's working backwards document that often describes features whose Kano category (must-have vs. delighter) shapes the value proposition narrative.
- **[Cognitive Bias](term_cognitive_bias.md)**: Kano dynamics are rooted in cognitive biases including hedonic adaptation, loss aversion, and expectation anchoring.

## References

### Vault Sources
- [The Lean Product Playbook — Dan Olsen (Digest)](../digest/digest_lean_product_playbook_olsen.md) — Prominently features the Kano Model as a framework for feature prioritization in the Lean Product Process

### External Sources
- [Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive Quality and Must-Be Quality." Journal of the Japanese Society for Quality Control, 14(2), 39-48.](https://www.jstage.jst.go.jp/article/quality/14/2/14_KJ00002952366/_article/-char/en) — Original paper introducing the Kano Model
- [Löfgren, M. & Witell, L. (2008). "Theory of Attractive Quality and the Kano Methodology — the Past, the Present, and the Future." Total Quality Management, 19(4), 371-386.](https://www.researchgate.net/publication/262868045_Theory_of_attractive_quality_and_the_Kano_methodology_-_the_past_the_present_and_the_future) — Comprehensive review of attractive quality theory evolution
- [Wikipedia: Kano Model](https://en.wikipedia.org/wiki/Kano_model) — Overview of model categories, questionnaire methodology, and applications
- [ProductPlan: Kano Model Glossary](https://www.productplan.com/glossary/kano-model/) — Product management perspective on Kano analysis
- [Folding Burritos: The Complete Guide to the Kano Model](https://foldingburritos.com/blog/kano-model/) — Detailed practitioner guide with questionnaire methodology and examples
