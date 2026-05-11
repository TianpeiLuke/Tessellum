---
tags:
  - resource
  - terminology
  - nlp
  - tokenization
  - multilingual
keywords:
  - SentencePiece
  - Kudo Richardson 2018
  - language-agnostic tokenizer
  - unigram language model
  - raw byte stream
  - BPE
  - multilingual
  - pre-tokenization free
topics:
  - NLP
  - tokenization
  - multilingual NLP
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# SentencePiece

## Definition

SentencePiece is a **language-agnostic tokenizer library** introduced by Kudo & Richardson (2018). Unlike traditional tokenizers that rely on language-specific pre-tokenization rules (e.g., whitespace splitting for English, MeCab for Japanese), SentencePiece treats the input as a **raw byte stream** and learns subword units directly from the raw text. This makes it applicable to any language without modification.

SentencePiece supports two subword segmentation algorithms:

1. **Byte Pair Encoding (BPE)** — bottom-up, frequency-based merging of character pairs.
2. **Unigram Language Model** — top-down, likelihood-based pruning from a large initial vocabulary.

The **Unigram Language Model** (Kudo, 2018) starts with a large seed vocabulary and iteratively removes tokens that least decrease the marginal likelihood over the training corpus $D$:

$$\mathcal{L} = \sum_{s \in D} \log P(s) = \sum_{s \in D} \log \left(\sum_{x \in S(s)} \prod_{i=1}^{|x|} p(x_i)\right)$$

where $S(s)$ is the set of all possible segmentations of sentence $s$, and $p(x_i)$ is the unigram probability of subword token $x_i$. The EM algorithm optimizes token probabilities, and the least-useful tokens are pruned each iteration until the target vocabulary size is reached.

SentencePiece is the tokenizer behind **T5**, **LLaMA**, **ALBERT**, **XLNet**, and many multilingual models (e.g., mBART, XLM-RoBERTa).

## Comparison with BPE and WordPiece

| Aspect | BPE | WordPiece | Unigram (SentencePiece) |
|---|---|---|---|
| **Direction** | Bottom-up merges | Bottom-up merges | Top-down pruning |
| **Criterion** | Frequency of pair | Likelihood gain | Likelihood loss on removal |
| **Vocabulary init** | Characters | Characters | Large superset |
| **Pre-tokenization** | Typically required | Typically required | Not required |
| **Segmentation** | Deterministic | Deterministic | Probabilistic (can sample) |

> **Note:** The SentencePiece *library* wraps both BPE and Unigram as selectable algorithms. The term "SentencePiece" often refers to the Unigram variant specifically, but the library supports both.

## Key Properties

- **Language-agnostic**: operates on raw Unicode byte streams with no pre-tokenization step.
- **Whitespace as character**: encodes whitespace using the meta-symbol `▁` (U+2581) as a prefix, enabling **reversible tokenization** — the original text can be reconstructed losslessly from tokens.
- **Dual algorithm support**: BPE mode and Unigram mode are both available via a single library.
- **Unigram uses EM**: the Expectation-Maximization algorithm jointly optimizes token probabilities $p(x_i)$ and prunes the vocabulary.
- **Vocabulary size is a hyperparameter**: the user specifies the target vocabulary size (e.g., 32k for T5, 32k for LLaMA).
- **Subword regularization**: the Unigram model can sample from multiple segmentations during training, acting as a data augmentation technique.

## Related Terms

- [Byte Pair Encoding](term_byte_pair_encoding.md) — BPE algorithm that SentencePiece wraps as one of its two modes
- [WordPiece](term_wordpiece.md) — likelihood-based subword algorithm used by BERT; similar goal, different approach
- [Tokenization](term_tokenization.md) — parent concept covering all text-to-token methods
- [BERT](term_bert.md) — uses WordPiece, not SentencePiece; a key architectural contrast
- [Word Embedding](term_word_embedding.md) — tokens produced by SentencePiece map to dense embedding vectors
- [Multinomial Distribution](term_multinomial_distribution.md) — the unigram model defines a multinomial over the vocabulary
- [Exponential Family](term_exponential_family.md) — the log-linear unigram model belongs to the exponential family
- [Variational Inference](term_variational_inference.md) — EM algorithm used for unigram vocabulary optimization
- [NLP](term_nlp.md) — broader field in which SentencePiece operates
- [LDA](term_lda.md) — shares the unigram (bag-of-words) assumption at the token level
- [Bag of Words](term_bag_of_words.md) — unigram tokenization is conceptually a bag of subwords

## References

1. Kudo, T., & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing*. EMNLP.
2. Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL.
3. [SentencePiece — Wikipedia](https://en.wikipedia.org/wiki/SentencePiece)
