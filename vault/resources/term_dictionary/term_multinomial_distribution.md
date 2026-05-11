---
tags:
  - resource
  - terminology
  - statistics
  - probability
keywords:
  - multinomial distribution
  - multivariate binomial
  - categorical outcomes
  - multi-class
  - probability vector
topics:
  - probability theory
  - statistical modeling
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# Multinomial Distribution

## Definition

The **multinomial distribution** generalizes the binomial distribution from two outcomes to $k > 2$ categories. It models the counts of outcomes across $k$ categories in $n$ independent trials, where each trial produces exactly one of $k$ possible outcomes with fixed probabilities $p_1, p_2, \ldots, p_k$ satisfying $\sum_{i=1}^{k} p_i = 1$.

The probability mass function (PMF) is:

$$
P(X_1 = x_1, \ldots, X_k = x_k) = \frac{n!}{x_1!\, x_2!\, \cdots\, x_k!} \prod_{i=1}^{k} p_i^{x_i}
$$

where $x_i \geq 0$ are non-negative integers with $\sum_{i=1}^{k} x_i = n$. The coefficient $\frac{n!}{x_1! \cdots x_k!}$ is the **multinomial coefficient**, counting the number of ways to partition $n$ trials into groups of sizes $x_1, \ldots, x_k$.

We write $(X_1, \ldots, X_k) \sim \text{Multinomial}(n, \mathbf{p})$ where $\mathbf{p} = (p_1, \ldots, p_k)$.

## Key Properties

- **Mean**: $E[X_i] = n p_i$
- **Variance**: $\text{Var}(X_i) = n p_i (1 - p_i)$
- **Covariance**: $\text{Cov}(X_i, X_j) = -n p_i p_j$ for $i \neq j$
  - The negative covariance reflects the constraint $\sum x_i = n$: if one category count increases, others must decrease.
- **Marginals**: Each $X_i \sim \text{Binomial}(n, p_i)$.
- **Relation to Binomial**: When $k = 2$, the multinomial reduces to the binomial distribution with $X_1 \sim \text{Binomial}(n, p_1)$.
- **Conjugate prior**: The [Dirichlet distribution](term_dirichlet_distribution.md) is the conjugate prior for the multinomial, just as the Beta distribution is conjugate for the binomial.

## Applications

| Domain | Use Case |
|---|---|
| **Text Classification** | Bag-of-words models treat documents as multinomial draws over a vocabulary; word counts follow a multinomial distribution |
| **Genetics** | Allele frequency estimation models observed genotype counts as multinomial draws from a population |
| **Topic Modeling (LDA)** | Latent Dirichlet Allocation models each document's word distribution as a multinomial parameterized by a Dirichlet-drawn topic mixture |
| **Customer Segmentation** | Categorizing customers into $k$ segments based on behavioral patterns, where segment assignment counts are multinomial |
| **Goodness-of-Fit Testing** | The chi-squared test compares observed multinomial counts against expected counts under a null hypothesis |

## Related Terms

- [Binomial Distribution](term_binomial_distribution.md) — special case when $k = 2$
- [Dirichlet Distribution](term_dirichlet_distribution.md) — conjugate prior for the multinomial probability vector
- [Conjugate Prior](term_conjugate_prior.md) — Bayesian concept linking the Dirichlet–Multinomial pair
- **[Beta Distribution](term_beta_distribution.md)**: The k=2 case reduces Dirichlet-Multinomial to Beta-Binomial

- **[Word2Vec](term_word2vec.md)**: Word2Vec softmax is Multinomial over vocabulary
- **[Bag of Words](term_bag_of_words.md)**: BoW word counts follow Multinomial distribution
- **[HMM](term_hmm.md)**: HMM uses Multinomial emissions (discrete) or Gaussian emissions (continuous)
- **[LDA](term_lda.md)**: LDA uses Multinomial for document-topic and topic-word distributions
- **[HMM](term_hmm.md)**: Discrete HMM uses Multinomial emission distributions
- **[CRF](term_crf.md)**: CRF output layer is Multinomial over label sequences
- **[Normal Distribution](term_normal_distribution.md)**: Multinomial approaches multivariate normal for large counts (CLT)
- **[Concentration Inequality](term_concentration_inequality.md)**: Multinomial tail bounds via method of types

- **[WordPiece](term_wordpiece.md)**: WordPiece merge criterion uses PMI over Multinomial token counts
- **[SentencePiece](term_sentencepiece.md)**: Unigram model is Multinomial over subword vocabulary

## References

- [Multinomial distribution — Wikipedia](https://en.wikipedia.org/wiki/Multinomial_distribution)
- [MultinomialDistribution — Wolfram MathWorld](https://reference.wolfram.com/language/ref/MultinomialDistribution.html)
