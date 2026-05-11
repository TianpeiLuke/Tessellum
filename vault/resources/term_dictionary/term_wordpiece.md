---
tags:
  - resource
  - terminology
  - nlp
  - tokenization
keywords:
  - WordPiece
  - subword tokenization
  - Schuster Nakajima 2012
  - likelihood maximization
  - BERT tokenizer
  - vocabulary
  - subword unit
  - "## prefix"
topics:
  - NLP
  - tokenization
  - text preprocessing
language: markdown
date of note: 2026-04-04
status: active
building_block: concept
---

# WordPiece

## Definition

**WordPiece** is a subword tokenization algorithm introduced by Schuster & Nakajima (2012) for Japanese and Korean voice search. Unlike [BPE](term_byte_pair_encoding.md), which merges the most *frequent* pair, WordPiece selects the merge that *maximizes the likelihood* of the training data.

Given a current vocabulary $V$, the algorithm merges the symbol pair $(a, b)$ that maximizes:

$$\arg\max_{(a,b)} \frac{P(ab)}{P(a) \cdot P(b)}$$

This is equivalent to choosing the pair with the highest **pointwise mutual information (PMI)** — the pair whose co-occurrence is most surprising relative to independent occurrence.

WordPiece is the tokenizer used by **BERT**, DistilBERT, and ELECTRA. Continuation subword tokens are prefixed with `##` to distinguish them from word-initial tokens. For example:

> `"playing"` → `["play", "##ing"]`

At inference time, tokenization uses a **greedy longest-match-first** strategy against the learned vocabulary.

## Comparison with BPE

| Aspect | BPE | WordPiece | SentencePiece |
|---|---|---|---|
| **Merge criterion** | Most frequent pair | Highest likelihood (PMI) | Unigram LM or BPE |
| **Prefix convention** | None (merge in-place) | `##` for continuation | `▁` for word-initial |
| **Used by** | GPT, RoBERTa, LLaMA | BERT, DistilBERT, ELECTRA | T5, ALBERT, XLNet |
| **Input assumption** | Pre-tokenized words | Pre-tokenized words | Raw byte stream (language-agnostic) |
| **Inference strategy** | Sequential merge replay | Greedy longest-match-first | Viterbi / sampling |

## Key Properties

- **Likelihood-based merge criterion** — selects merges by PMI rather than raw frequency, favoring linguistically coherent subwords.
- **`##` prefix** — continuation tokens are marked with `##`, making word boundaries recoverable.
- **Vocabulary size** — typically 30,522 tokens for BERT-base (30K subwords + special tokens).
- **OOV handling** — unknown words are decomposed into known subword units; only individual characters fall back to `[UNK]`.
- **Greedy longest-match-first** — at inference, each word is tokenized left-to-right by the longest matching vocabulary entry.
- **Training** — starts from a character-level vocabulary and iteratively merges pairs until the target vocabulary size is reached.

## Related Terms

- [Byte Pair Encoding](term_byte_pair_encoding.md) — frequency-based subword alternative
- [SentencePiece](term_sentencepiece.md) — language-agnostic tokenization wrapper
- [Tokenization](term_tokenization.md) — parent concept for text segmentation
- [BERT](term_bert.md) — primary model using WordPiece
- [Word Embedding](term_word_embedding.md) — subword tokens map to dense embeddings
- [Word2Vec](term_word2vec.md) — word-level embedding predecessor
- [Multinomial Distribution](term_multinomial_distribution.md) — likelihood model over vocabulary
- [Exponential Family](term_exponential_family.md) — log-linear model underlying merge selection
- [NLP](term_nlp.md) — broader field
- [LDA](term_lda.md) — bag-of-words tokenization contrast
- [Named Entity Recognition](term_ner.md) — token-level task sensitive to tokenizer choice

## References

1. Schuster, M., & Nakajima, K. (2012). *Japanese and Korean voice search*. IEEE ICASSP.
2. Wu, Y., et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv:1609.08144.
3. [WordPiece — Wikipedia](https://en.wikipedia.org/wiki/WordPiece)
4. [Hugging Face Tokenizers — WordPiece](https://huggingface.co/docs/tokenizers/api/models#tokenizers.models.WordPiece)
