---
tags:
  - resource
  - terminology
  - cognitive_science
  - epistemology
  - statistical_reasoning
keywords:
  - silent evidence
  - the cemetery
  - Nassim Nicholas Taleb
  - survivorship bias
  - invisible failures
  - selection bias
  - missing data
  - Diagoras
  - Casanova
keywords_alt:
  - cemetery of the invisible
  - hidden evidence
  - absent evidence
topics:
  - Cognitive Biases and Thinking Errors
  - Epistemology and Knowledge Formation
  - Risk Assessment and Uncertainty
language: markdown
date of note: 2026-03-15
status: active
building_block: concept
---

# Silent Evidence

## Definition

**Silent evidence** is the systematically invisible population of failures, near-misses, and unrealized possibilities that never enters our analysis because it failed to survive, was never recorded, or was never considered. The term was coined by Nassim Nicholas Taleb in *The Black Swan* (2007) and further explored in *Fooled by Randomness* (2001), where he argues that silent evidence "pervades everything connected to the notion of history." Taleb also calls this phenomenon **"the cemetery"** --- the vast, unseen graveyard of outcomes that did not make it into the historical record.

Silent evidence is closely related to survivorship bias but is conceptually broader. Survivorship bias refers specifically to the error of studying only entities that passed through a selection filter (successful companies, returning aircraft, published papers). Silent evidence encompasses this but extends to all forms of absent data: events that were never observed, possibilities that were never entertained, and counterfactuals that were never examined. We study only what survived --- successful companies, winning strategies, published research --- while the vastly larger population of failures remains invisible, not because it is hidden, but because the mechanisms that would have preserved it (success, publication, survival) are precisely the ones it lacked.

The concept is best captured by the ancient anecdote Taleb borrows from Cicero. The nonbeliever Diagoras was shown painted tablets depicting worshippers who had prayed and then survived a shipwreck, offered as proof of the power of prayer. Diagoras asked: "Where are the pictures of those who prayed, then drowned?" The drowned believers are the silent evidence --- they cannot testify because the very outcome (drowning) that would refute the claim also eliminates the witness. This self-silencing structure is what makes silent evidence so dangerous: the bias is not merely difficult to detect, it is actively concealed by the same process that produces the visible evidence.

## Historical Context

The intellectual roots of silent evidence extend back to antiquity. Cicero (106--43 BC) recorded the Diagoras anecdote in *De Natura Deorum*, making it one of the earliest documented challenges to survivorship-based reasoning. The statistician Abraham Wald formalized a related insight during World War II when he recognized that bullet holes on returning aircraft represented survivable damage, not vulnerability --- the planes that were truly vulnerable never returned to be studied.

Taleb synthesized these threads in his *Incerto* series. In *Fooled by Randomness* (2001), Chapter 11 ("Randomness and Our Mind: We Are Probability Blind") introduced the problem of silent evidence in the context of financial markets, where failed traders disappear from databases and their strategies are never studied. In *The Black Swan* (2007), Chapter 8 ("Giacomo Casanova's Unfailing Luck: The Problem of Silent Evidence") gave the concept its definitive treatment. Taleb used the adventurer Casanova as an archetype: Casanova believed he had a "lucky star" protecting him, but for every Casanova whose risks paid off, dozens of equally daring adventurers perished silently, leaving no memoirs.

The concept gained further traction in research methodology through growing awareness of publication bias --- the systematic non-publication of studies with null or negative results. Entire fields have been distorted by a scientific record composed exclusively of "surviving" (published) findings, with the failed replications and null results constituting a vast cemetery of silent evidence.

## Taxonomy

| Variant | Mechanism | Example |
|---------|-----------|---------|
| **Survivorship bias** | Failed cases are destroyed or removed from the dataset by the selection process itself | Mutual fund databases exclude defunct funds, inflating average returns |
| **Publication bias** | Studies with null results are not published, distorting the scientific record | Meta-analyses overestimate effect sizes because negative studies are missing |
| **Cemetery of failed strategies** | Strategies that failed are abandoned and forgotten; only winning strategies are documented | Business books study successful companies, never the thousands that used identical strategies and failed |
| **Anthropic selection** | We can only observe conditions compatible with our own existence as observers | The apparent "fine-tuning" of physical constants reflects the fact that observers can only exist in universes that permit observers |
| **Historical record bias** | Events, people, and cultures that left no records are excluded from historical analysis | History is disproportionately the story of literate, powerful civilizations; oral cultures are underrepresented |

## Key Properties

- **Self-concealing**: the very process that creates silent evidence (failure, destruction, non-publication) also ensures it cannot be observed, making the bias structurally invisible
- **Broader than survivorship bias**: encompasses not just filtered-out failures but also unconsidered possibilities, unrecorded events, and unimagined counterfactuals
- **Distorts perceived causality**: when only successes are visible, their shared traits appear causal rather than incidental, generating false "success formulas"
- **Inflates confidence in predictions**: a historical record composed only of survivors appears more orderly and predictable than reality, feeding overconfidence
- **Compounds with narrative fallacy**: once silent evidence is removed, the remaining visible data is easily woven into compelling but misleading causal stories
- **Undermines inductive reasoning**: conclusions drawn from visible cases do not generalize to the full population, because the visible cases are a biased sample
- **Scales with stakes**: the higher the stakes (war, finance, entrepreneurship), the more completely failures are eliminated from the record, and the stronger the distortion
- **Resistant to correction**: you cannot simply "add back" evidence that was never collected or entities that were destroyed; mitigation requires structural changes to data collection
- **Pervades expert judgment**: experts trained on surviving cases develop systematically skewed intuitions about what works and what is dangerous

## Notable Systems / Implementations

| Domain | Manifestation | Impact |
|--------|---------------|--------|
| **WWII Aircraft Analysis** | Abraham Wald recognized that damage patterns on returning aircraft showed where planes could survive hits, not where they were vulnerable | Reversed the military's armor-placement decision; became a canonical example of correcting for silent evidence |
| **Mutual Fund Databases** | Elton, Gruber & Blake (1996) showed that excluding defunct funds inflated reported average returns by ~1% per year | Led to survivorship-bias-free databases and SEC reporting changes |
| **Clinical Trials Registry** | ClinicalTrials.gov (est. 2000) requires pre-registration of trials to combat publication bias | Reduces the cemetery of unpublished negative results in medicine |
| **Pre-registration in Social Science** | Open Science Framework and journal-level Registered Reports | Makes the full base of attempted studies visible, regardless of outcome |
| **Startup Failure Post-mortems** | CB Insights and similar databases that systematically collect failure narratives | Partially recovers silent evidence from the startup cemetery |

## Applications

| Domain | How Silent Evidence Distorts | Countermeasure |
|--------|------------------------------|----------------|
| **Finance** | Only surviving funds, strategies, and traders are studied; failures vanish from databases | Survivorship-bias-free databases; tracking "dead" funds and strategies |
| **Business Strategy** | Success literature studies only winners (e.g., *Good to Great*), never the companies that did the same things and failed | Base-rate analysis; systematic study of matched failures |
| **Research Methodology** | Publication bias creates a scientific record of positive results only, inflating effect sizes | Pre-registration; Registered Reports; meta-analytic corrections for publication bias |
| **History** | Only literate, victorious civilizations leave extensive records; the defeated and illiterate are invisible | Archaeological and oral-history methods; explicit acknowledgment of record gaps |
| **Criminal Justice** | We understand crime only through failed criminals who were caught; successful criminals are invisible | Victimization surveys; dark-figure-of-crime estimation techniques |

## Challenges and Limitations

- **Cannot be fully corrected**: by definition, silent evidence is evidence that was never recorded; no statistical technique can perfectly reconstruct what was never observed
- **Awareness is insufficient**: knowing about silent evidence provides limited protection because our cognitive systems automatically process only available data (WYSIATI)
- **Quantification is difficult**: estimating the size of the "cemetery" requires assumptions about the full population that are themselves uncertain
- **Overcorrection risk**: excessive skepticism about all visible evidence can lead to analytical paralysis or nihilism about the possibility of learning from data
- **Domain-specific solutions are fragile**: pre-registration works for clinical trials but has no equivalent in entrepreneurship, military history, or evolutionary biology

## Related Terms

- **[Survivorship Bias](term_survivorship_bias.md)**: the most well-known specific instance of silent evidence; focuses on the selection filter that removes failures from view
- **[Black Swan](term_black_swan.md)**: Taleb's broader framework; silent evidence is one of the cognitive mechanisms that blinds us to rare, high-impact events
- **[Narrative Fallacy](term_narrative_fallacy.md)**: once silent evidence is removed, the remaining visible data is easily woven into compelling but false causal stories
- **[WYSIATI](term_wysiati.md)**: Kahneman's "What You See Is All There Is" --- the mind builds the best story from available information without noticing what is missing, which is precisely the mechanism that makes silent evidence invisible
- **[Availability Heuristic](term_availability_heuristic.md)**: we judge probability by how easily examples come to mind; silent evidence, by definition, provides no examples to recall
- **[Confirmation Bias](term_confirmation_bias.md)**: we seek evidence confirming existing beliefs, and silent evidence ensures that disconfirming data is never encountered
- **[Base Rate Neglect](term_base_rate_neglect.md)**: silent evidence removes the denominator (total attempts) that is essential for accurate base-rate estimation
- **[Cognitive Bias](term_cognitive_bias.md)**: parent concept; silent evidence is both a bias itself and a structural amplifier of many other biases

## References

### Vault Sources
- [Digest: The Black Swan](../digest/digest_black_swan_taleb.md) --- Taleb's definitive treatment of silent evidence in Chapter 8, "Giacomo Casanova's Unfailing Luck"
- [Digest: The Art of Thinking Clearly](../digest/digest_thinking_clearly_dobelli.md) --- Dobelli's treatment of survivorship bias as a core thinking error
- [Digest: Thinking, Fast and Slow](../digest/digest_thinking_fast_and_slow_kahneman.md) --- Kahneman's WYSIATI framework and the cognitive mechanisms that make silent evidence invisible

### External Sources
- Taleb, N. N. (2007). *The Black Swan: The Impact of the Highly Improbable.* Random House. Chapter 8: "Giacomo Casanova's Unfailing Luck: The Problem of Silent Evidence."
- Taleb, N. N. (2001). *Fooled by Randomness: The Hidden Role of Chance in Life and in the Markets.* Random House. Chapter 11: "Randomness and Our Mind: We Are Probability Blind."
- Cicero. *De Natura Deorum* (45 BC). Book III --- the Diagoras anecdote on shipwreck survivors.
- Elton, E. J., Gruber, M. J., & Blake, C. R. (1996). "Survivorship Bias and Mutual Fund Performance." *Review of Financial Studies*, 9(4), 1097--1120.
- [Shortform: Silent Evidence](https://www.shortform.com/blog/silent-evidence/) --- accessible overview of Taleb's concept with examples.
- [Sigma Actuarial: Silent Evidence](https://www.sigmaactuary.com/2017/12/13/silent-evidence/) --- actuarial perspective on silent evidence in risk assessment.
