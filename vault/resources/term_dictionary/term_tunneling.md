---
tags:
  - resource
  - terminology
  - cognitive_science
  - risk_management
  - decision_theory
  - epistemology
keywords:
  - tunneling
  - tunnel vision
  - Nassim Nicholas Taleb
  - The Black Swan
  - known risks
  - unknown risks
  - known unknowns
  - unknown unknowns
  - attention narrowing
  - risk modeling
  - Value at Risk
  - VaR
topics:
  - Cognitive Biases and Thinking Errors
  - Risk Assessment and Uncertainty
  - Probability and Decision-Making
  - Epistemology and Knowledge Formation
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Tunneling

## Definition

**Tunneling** is a concept introduced by **Nassim Nicholas Taleb** in *The Black Swan: The Impact of the Highly Improbable* (2007) to describe the tendency to focus on a small number of well-defined sources of uncertainty while ignoring the much larger, unknown sources -- seeing the world through a narrow tunnel. When people tunnel, their understanding of uncertainty is based almost exclusively on what *has happened* in the past rather than what *could have happened* but did not. The result is an elaborate apparatus for managing known risks and a near-total blindness to the category of risks that have never been observed.

Tunneling is distinct from simple inattention or negligence. It is a *structural* cognitive failure: the more sophisticated one's tools for analyzing known risks become, the more confident one feels, and the less one notices that the entire framework excludes the risks that matter most. A risk manager who builds a precise Value-at-Risk model for a portfolio's exposure to interest-rate movements is not being lazy -- she is being diligent *within the tunnel*. The danger is that the tunnel excludes credit contagion, liquidity seizures, and systemic failures that lie outside the model's variable space. Tunneling is the cognitive mechanism by which expertise itself becomes a source of vulnerability: the better you understand the risks inside the tunnel, the more invisible the risks outside it become.

The concept is closely related to Kahneman's **[WYSIATI](term_wysiati.md)** (What You See Is All There Is) -- the tendency of System 1 to construct coherent narratives from whatever information is available without considering what information might be missing. Where WYSIATI describes the general cognitive machinery, tunneling describes its specific manifestation in professional risk assessment: the substitution of a well-modeled subset of risks for the full, unknowable risk landscape.

## Historical Context

Taleb introduced tunneling in *The Black Swan* (2007) as one of several interlocking cognitive biases that collectively blind us to [Black Swan](term_black_swan.md) events. The concept builds on an intellectual lineage that includes Frank Knight's distinction between *risk* (quantifiable uncertainty with known probability distributions) and *uncertainty* (unquantifiable uncertainty where the distribution itself is unknown), articulated in *Risk, Uncertainty, and Profit* (1921). It also connects to Donald Rumsfeld's 2002 taxonomy of "known knowns, known unknowns, and unknown unknowns" -- tunneling is the error of building elaborate defenses against known unknowns while ignoring unknown unknowns entirely.

Taleb's critique was sharpened by his direct experience as a derivatives trader and risk analyst in financial markets, where he observed that professional risk managers systematically committed the tunneling error. The 2008 global financial crisis provided dramatic vindication: firms employing dozens of risk managers and running sophisticated VaR models were bankrupted by precisely the category of risks their models excluded.

| Year | Development | Significance |
|------|------------|--------------|
| 1921 | Knight, *Risk, Uncertainty, and Profit* | Distinguished calculable risk from true uncertainty -- the intellectual foundation for the tunneling critique |
| 2002 | Rumsfeld's "known unknowns" speech | Made the known/unknown taxonomy part of public discourse |
| 2007 | Taleb, *The Black Swan* | Formally introduced tunneling as a named cognitive error in risk assessment |
| 2008 | Global financial crisis | Risk models (VaR, CDO pricing) failed catastrophically -- tunneling on modeled risks left firms blind to systemic contagion |
| 2012 | Taleb, *Antifragile* | Extended the argument: the response to tunneling is not better models but antifragile systems that benefit from the unexpected |

## Taxonomy

Tunneling manifests in several distinguishable forms depending on the domain and the mechanism of attention narrowing:

| Variant | Mechanism | Example |
|---------|-----------|---------|
| **Model tunneling** | Building elaborate quantitative models for known risk factors while excluding unmodeled variables | VaR models that capture market risk but exclude liquidity risk, counterparty contagion, and operational failures |
| **Historical tunneling** | Calibrating risk estimates exclusively on historical data, assuming the future will resemble the past | Stress tests that model "worst cases" from the 2008 crisis but cannot conceive of a structurally different crisis |
| **Expert tunneling** | Domain expertise creates deep but narrow vision; experts become prisoners of their own frameworks | Epidemiologists modeling pandemic risk from known pathogens while ignoring the possibility of a novel pathogen with unprecedented characteristics |
| **Regulatory tunneling** | Compliance frameworks define the risk categories that are monitored, rendering all others invisible | Basel III capital requirements that specify risk categories, inadvertently signaling that non-specified risks need not be managed |
| **Precision tunneling** | Mathematical precision of a risk metric creates false confidence that the metric captures all relevant risk | Quoting a portfolio's 99th-percentile loss to three decimal places while ignoring that the 99.9th-percentile loss is orders of magnitude larger |

## Key Properties

- **Inverse expertise effect**: The more sophisticated one's risk modeling tools become, the stronger the tunneling effect -- expertise deepens the tunnel rather than widening the field of vision
- **WYSIATI connection**: Tunneling is the risk-management instantiation of Kahneman's [WYSIATI](term_wysiati.md) principle -- the available risk factors are treated as "all there is," with no felt sense that entire categories of risk are absent from the analysis
- **Known unknowns vs. unknown unknowns**: Tunneling operates on the boundary between Rumsfeld's categories -- it is the systematic overinvestment in known unknowns (risks we know we face but cannot precisely quantify) at the expense of unknown unknowns (risks we do not even know exist)
- **Ludic fallacy overlap**: Tunneling is closely related to the [ludic fallacy](term_ludic_fallacy.md) -- both involve treating a tractable model as if it captures the full problem space; the ludic fallacy emphasizes the game-like nature of the model, while tunneling emphasizes the attentional narrowing
- **[Platonicity](term_platonicity.md) as root cause**: Tunneling is a downstream effect of Platonicity -- the preference for clean, well-defined abstractions over the messy, unbounded reality they claim to represent
- **Narrative reinforcement**: The [narrative fallacy](term_narrative_fallacy.md) amplifies tunneling by providing compelling explanatory stories about the risks inside the tunnel, making the framework feel complete and coherent
- **Asymmetric consequences**: The risks excluded by tunneling are precisely the ones with the most extreme consequences -- [tail risks](term_tail_risk.md) and systemic failures that models are structurally unable to capture
- **Professional incentive alignment**: Risk managers are rewarded for managing the risks they measure and face no consequences for risks they do not measure -- organizational incentive structures reinforce the tunnel
- **Self-reinforcing confidence**: Each period in which the modeled risks are successfully managed increases confidence in the model, even though the unmodeled risks remain unchanged -- survival within the tunnel feels like mastery of the full landscape

## Notable Systems / Implementations

| Domain | Tunneling Manifestation | Consequence |
|--------|------------------------|-------------|
| **Finance (VaR)** | Value-at-Risk models measured exposure to known market factors using historical distributions | 2008 crisis: firms with sophisticated VaR lost billions from risks their models excluded (counterparty contagion, liquidity seizure) |
| **Amaranth Advisors** | 12 risk managers built elaborate models based on past natural gas market performance | Lost $7 billion in days from price movements their models treated as impossible |
| **Pre-9/11 security** | Airport security focused on known threat categories (hijacking for ransom, smuggling) | The use of commercial aircraft as weapons was outside the tunnel of modeled threats |
| **Pandemic planning** | Models calibrated on SARS, H1N1, and influenza historical data | COVID-19 behaved outside historical parameters in a hyperconnected world |
| **Fraud detection** | Rule-based systems tuned to detect known abuse patterns | Novel abuse vectors that do not match historical signatures bypass the entire detection framework |

## Applications

| Domain | Application of the Concept |
|--------|---------------------------|
| **Risk management** | Recognize that the most dangerous risks are outside the model; supplement quantitative risk analysis with scenario planning for unmodeled threats |
| **Financial regulation** | Move beyond VaR-based capital requirements; mandate buffers for non-modeled tail risk and systemic contagion |
| **Decision theory** | Distinguish between decisions in [Mediocristan](term_mediocristan_and_extremistan.md) (where tunneling on known distributions is safe) and Extremistan (where it is catastrophic) |
| **Fraud and abuse prevention** | Design detection systems that flag anomalies (deviations from any pattern) rather than only matching known abuse signatures |
| **Intelligence analysis** | Apply structured analytic techniques (Analysis of Competing Hypotheses, Red Teaming) specifically designed to surface threats outside the analyst's tunnel |

## Challenges and Limitations

- **Actionability gap**: Recognizing that you are tunneling does not tell you what the excluded risks are -- by definition, unknown unknowns cannot be specified in advance. The critique identifies the problem without providing a specific solution.
- **Bounded rationality defense**: All analysis requires simplification. Models *must* tunnel to some degree because it is impossible to model everything. The question is not whether to tunnel but how to maintain awareness that one is doing so.
- **Over-correction risk**: Taken to an extreme, the tunneling critique could justify abandoning all quantitative risk management, which would be worse than imperfect models. The challenge is supplementing models with qualitative awareness of their boundaries.
- **Domain dependency**: In Mediocristan domains (e.g., life insurance actuarial tables), tunneling on historical distributions is appropriate because extreme outliers do not dominate. The critique is most powerful in Extremistan domains where fat tails prevail.
- **Organizational resistance**: Warning an organization that its carefully constructed risk framework is incomplete is politically difficult -- it challenges the expertise and institutional investment of the risk management function.

## Related Terms
- **[WYSIATI](term_wysiati.md)**: Kahneman's meta-bias -- tunneling is the risk-management instantiation of "What You See Is All There Is," where the modeled risks are treated as the complete risk landscape
- **[Black Swan](term_black_swan.md)**: Tunneling is the cognitive mechanism that blinds us to Black Swan events -- by focusing on known risks, we exclude the unprecedented events that carry the most extreme impact
- **[Ludic Fallacy](term_ludic_fallacy.md)**: The error of applying game-like, well-defined uncertainty to messy real-world uncertainty -- tunneling is the attentional narrowing that results from this substitution
- **[Platonicity](term_platonicity.md)**: The root cognitive tendency that drives tunneling -- the preference for clean, well-defined abstractions over intractable reality
- **[Narrative Fallacy](term_narrative_fallacy.md)**: Reinforces tunneling by providing coherent explanatory stories that make the modeled risk framework feel complete
- **[Silent Evidence](term_silent_evidence.md)**: The risks excluded by tunneling are a form of silent evidence -- they are invisible precisely because no historical data exists for them
- **[Confirmation Bias](term_confirmation_bias.md)**: Modelers seek data that confirms their framework's adequacy while ignoring signals that the framework is incomplete
- **[Mediocristan and Extremistan](term_mediocristan_and_extremistan.md)**: Tunneling is dangerous in Extremistan (where tail events dominate) but relatively safe in Mediocristan (where distributions are thin-tailed)
- **[Overconfidence Effect](term_overconfidence_effect.md)**: The precision of risk models creates unwarranted confidence that all relevant risks are being managed
- **[Antifragility](term_antifragility.md)**: Taleb's constructive response to tunneling -- rather than trying to model all risks, build systems that benefit from the volatility and disorder that tunneling obscures
- **[Barbell Strategy](term_barbell_strategy.md)**: The structural portfolio response to tunneling -- combine ultra-safe positions with small speculative bets, avoiding the middle where tunneled risk models give false comfort

## References

### Vault Sources
- [Digest: The Black Swan](../digest/digest_black_swan_taleb.md) -- Section 8 defines tunneling as one of the interlocking biases that blind us to Black Swan events

### External Sources
- [Taleb, N.N. (2007). *The Black Swan: The Impact of the Highly Improbable*. Random House](https://en.wikipedia.org/wiki/The_Black_Swan_(Taleb_book)) -- the source text where tunneling is introduced as a named cognitive error
- [Taleb, N.N. (2001). *Fooled by Randomness*. Random House](https://en.wikipedia.org/wiki/Fooled_by_Randomness) -- precursor work on how traders and risk managers systematically underestimate rare events
- [Taleb, N.N. "Against Value-at-Risk." *Fooled by Randomness* website](https://www.fooledbyrandomness.com/jorion.html) -- Taleb's extended critique of VaR as institutionalized tunneling
- [Wikipedia: Black Swan Theory](https://en.wikipedia.org/wiki/Black_swan_theory) -- overview including tunneling's role among Black Swan-enabling biases
- [Shortform: Black Swan Fallacy](https://www.shortform.com/blog/black-swan-fallacy/) -- accessible explanation of tunneling with the Amaranth Advisors case study
- [Wikipedia: Knightian Uncertainty](https://en.wikipedia.org/wiki/Knightian_uncertainty) -- the foundational risk vs. uncertainty distinction that tunneling violates

---

**Last Updated**: March 15, 2026
**Status**: Active -- cognitive science / risk management / decision theory terminology
