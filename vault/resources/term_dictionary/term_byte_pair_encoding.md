---
tags:
  - resource
  - terminology
  - nlp
  - tokenization
  - preprocessing
keywords:
  - byte pair encoding
  - BPE
  - tokenization
  - subword
  - vocabulary
  - byte-level BPE
  - WordPiece
  - SentencePiece
  - Unigram
  - merge operations
topics:
  - Natural Language Processing
  - Tokenization
  - Text Preprocessing
language: markdown
date of note: 2026-03-08
status: active
building_block: concept
---

# Term: Byte Pair Encoding

## Definition

**Byte Pair Encoding** (BPE) is a subword tokenization algorithm that iteratively merges the most frequent adjacent symbol pairs in a corpus, producing a vocabulary that interpolates between character-level and word-level representations. Originally a data compression technique (Gage, 1994), BPE was adapted for neural machine translation by Sennrich et al. (2015) to handle open vocabularies without `<UNK>` tokens. Common words become single tokens (e.g., "the" → `[the]`); rare words are decomposed into subword units (e.g., "unaffordable" → `[un, afford, able]`). GPT-2 (Radford et al., 2019) introduced **byte-level BPE**, which operates on raw bytes (base vocabulary: 256) rather than Unicode code points (base vocabulary: 130,000+), with character-category boundary enforcement to prevent cross-category merges.

## Full Name

**Byte Pair Encoding** (BPE)

**Also Known As**: Subword tokenization, BPE tokenization, byte-level BPE (when operating on bytes)

## Algorithm

### Standard BPE (Sennrich et al., 2015)

1. **Initialize**: Start with a vocabulary of all individual characters in the corpus, plus an end-of-word symbol
2. **Count**: Count all adjacent symbol pairs across the corpus
3. **Merge**: Replace the most frequent pair with a new merged symbol
4. **Repeat**: Steps 2-3 for a fixed number of merge operations (hyperparameter: vocabulary size)
5. **Result**: A vocabulary of subword units ordered by merge priority

**Example** (simplified):
```
Corpus: "low lower lowest"
Initial:  l o w </w>, l o w e r </w>, l o w e s t </w>
Merge 1:  lo w </w>, lo w e r </w>, lo w e s t </w>        (l + o → lo)
Merge 2:  low </w>, low e r </w>, low e s t </w>            (lo + w → low)
Merge 3:  low</w>, low er</w>, low est</w>                  (low + e → lowe? No — e+r and e+s compete)
...
```

The merge order is deterministic — the same corpus always produces the same vocabulary.

### Byte-Level BPE (Radford et al., 2019 — GPT-2)

Standard BPE operates on Unicode code points, requiring a large base vocabulary (~130,000 characters). GPT-2 introduced two innovations:

1. **Byte-level base vocabulary**: Start with 256 byte values instead of Unicode characters. Any byte sequence — and therefore any Unicode string — can be represented without `<UNK>` tokens.

2. **Character-category boundary enforcement**: BPE is prevented from merging symbols across character categories (letters, digits, punctuation), with an exception for spaces. This stops suboptimal vocabulary allocation where "dog", "dog.", "dog!", "dog?" would each learn separate merged tokens.

**Result**: A 50,257-token vocabulary that can tokenize any text in any language without preprocessing.

## Vocabulary Sizes Across Models

| Model | Tokenizer | Base Vocabulary | Final Vocabulary | Notes |
|-------|-----------|:--------------:|:----------------:|-------|
| Original Transformer | BPE (text) | Unicode chars | 37,000 (shared) | Shared source-target vocabulary |
| BERT | WordPiece | Unicode chars | 30,522 | Whole-word masking variant later |
| GPT-2 | Byte-level BPE | 256 bytes | 50,257 | Character-category boundary enforcement |
| GPT-3/4 | Byte-level BPE | 256 bytes | ~100,000 | Extended from GPT-2 |
| LLaMA | SentencePiece BPE | 256 bytes | 32,000 | Byte-fallback for unknown chars |
| Claude | BPE variant | 256 bytes | ~100,000 | Proprietary tokenizer |

## Comparison with Alternative Tokenizers

| Method | Training | Splitting Strategy | Handling Unknown Words | Used By |
|--------|----------|-------------------|----------------------|---------|
| **BPE** | Greedy merge (most frequent pair) | Bottom-up: characters → subwords | Decomposes to known subwords | GPT-2, GPT-3, RoBERTa |
| **WordPiece** | Greedy merge (max likelihood gain) | Bottom-up with likelihood criterion | Decomposes with `##` prefix | BERT, DistilBERT |
| **Unigram** | EM pruning from large vocabulary | Top-down: start large, prune | Multiple segmentations, choose best | T5, ALBERT, XLNet |
| **SentencePiece** | BPE or Unigram on raw text | Treats input as raw Unicode stream | No pre-tokenization needed | LLaMA, mBART |

**Key differences**:
- BPE is deterministic (one segmentation per input); Unigram is probabilistic (samples from multiple segmentations)
- WordPiece uses likelihood gain instead of frequency for merge decisions — similar in practice but handles rare pairs differently
- SentencePiece is language-agnostic — treats spaces as regular characters (uses `▁` prefix), making it ideal for multilingual models

## Tokenization Properties

### Compression Ratio

BPE achieves compression ratios of approximately 3-4 characters per token for English text:

| Model | Avg Characters/Token | Avg Tokens/Word |
|-------|:-------------------:|:---------------:|
| Character-level | 1.0 | ~5.0 |
| BPE (GPT-2, 50K vocab) | ~3.5 | ~1.3 |
| BPE (GPT-4, 100K vocab) | ~4.0 | ~1.1 |
| Word-level | ~5.0 | 1.0 |

Higher compression = fewer tokens per document = longer effective context window.

### Fertility (Tokens per Word)

BPE fertility varies significantly by language — languages underrepresented in training data require more tokens per word:

| Language | Relative Fertility (vs. English) |
|----------|:-------------------------------:|
| English | 1.0x |
| German | ~1.2x |
| Chinese | ~1.5x |
| Hindi | ~3.0x |
| Amharic | ~5.0x |

This "tokenizer tax" means non-English languages use more context window budget per word, creating a practical equity issue.

## Applications to Our Work

- **BERT tokenizers in abuse detection**: [RnR BSM BERT](../../areas/models/model_rnr_bsm_bert.md) and [CrossBERT](../../areas/models/model_x2risk_crossbert.md) use WordPiece tokenization — understanding subword decomposition is essential for interpreting attention patterns over buyer-seller messages
- **LLM prompt budgets**: BPE tokenization determines the effective length of prompts in LLM-based abuse classification — knowing the token-to-character ratio helps estimate how much context fits in the model's window
- **Multilingual abuse detection**: Non-English marketplaces face higher tokenization fertility, consuming more context budget for equivalent text length

## Related Terms

### Tokenization Family
- [Embedding](term_embedding.md) — Token embeddings are learned for each BPE vocabulary entry
- [Transformer](term_transformer.md) — Architecture that consumes BPE-tokenized input
- [LLM](term_llm.md) — All modern LLMs use BPE or BPE-derived tokenizers

### Models
- [BERT](term_bert.md) — Uses WordPiece (BPE variant) with 30,522 tokens
- [Positional Encoding](term_positional_encoding.md) — Position indices correspond to BPE token positions, not character positions

### Evaluation
- [Perplexity](term_perplexity.md) — Perplexity is computed per BPE token; different tokenizers produce non-comparable PPL values

- **[WordPiece](term_wordpiece.md)**: Likelihood-based alternative to BPE's frequency-based merges
- **[SentencePiece](term_sentencepiece.md)**: Library wrapping both BPE and Unigram algorithms

## References

- Gage, P. (1994). A New Algorithm for Data Compression. C Users Journal, 12(2), 23-38.
- Sennrich, R. et al. (2015). Neural Machine Translation of Rare Words with Subword Units. ACL. arXiv:1508.07909.
- Radford, A. et al. (2019). [Language Models are Unsupervised Multitask Learners](../papers/lit_radford2019language.md). OpenAI Technical Report.
- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. EMNLP. arXiv:1808.06226.
- Kudo, T. (2018). Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates. ACL. arXiv:1804.10959.
