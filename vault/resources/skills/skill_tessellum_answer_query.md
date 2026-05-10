---
tags:
  - resource
  - skill
  - procedure
  - question_answering
  - retrieval
keywords:
  - answer query
  - QA pipeline
  - context assembly
  - synthesis
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
  - Retrieval
  - Question Answering
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
related_skill_headers: []
pipeline_metadata: ./skill_tessellum_answer_query.pipeline.yaml
---

# Procedure: tessellum-answer-query (Canonical Body)

This is the canonical body for the `tessellum-answer-query` skill. Pairs with [`skill_tessellum_answer_query.pipeline.yaml`](skill_tessellum_answer_query.pipeline.yaml) — the typed contract for Composer dispatch.

A 5-stage QA pipeline that takes a user question, retrieves relevant typed atomic notes from the vault, assembles them into a token-budgeted context, and synthesizes a grounded answer with citations.

## Skill description <!-- :: section_id = skill_description :: -->

Answer a free-form user question using the indexed Tessellum vault. Five sequential stages: (1) query expansion to surface variants and acronyms; (2) multi-strategy retrieval via `tessellum-search-notes`; (3) working-memory scoring to deduplicate and rerank; (4) context assembly within a token budget; (5) synthesis of an answer that cites every note used. Returns the answer plus the list of cited note_ids.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version  # ensure v0.0.18+
tessellum index build --vault vault --db data/tessellum.db  # FTS5 + sqlite-vec
```

## Resources <!-- :: section_id = resources :: -->

- **Search backend**: `skill_tessellum_search_notes.md` (Stage 2 calls this).
- **Library primitives**: `tessellum.retrieval.{bm25,dense,hybrid,best_first_bfs,metadata}_search`, `tessellum.retrieval.route`.
- **Index DB**: `data/tessellum.db`.
- **Format spec**: [`DEVELOPING.md`](../../../DEVELOPING.md) — the YAML frontmatter convention citation answers reference.
- **Plan**: [`plan_retrieval_port.md`](../../../plans/plan_retrieval_port.md) — Wave 5 (this skill) closes the v0.1 retrieval scope.

## Validation rules reference <!-- :: section_id = validation_rules_reference :: -->

| Rule | Severity | Check |
|---|---|---|
| QA-001 | ERROR | Question is non-empty |
| QA-002 | ERROR | Stage 2 retrieval returns ≥ 1 hit (else: explain "no relevant notes" upfront) |
| QA-003 | WARNING | Context exceeds budget after Stage 4 (truncate + warn) |
| QA-004 | ERROR | Stage 5 answer must cite every note used (no uncited synthesis) |
| QA-005 | INFO | Multiple retrieval strategies invoked → diagnostic info in response |

## When to use <!-- :: section_id = when_to_use :: -->

- **User asks an open-ended question** — "How does Composer compile?", "What's the difference between BM25 and dense?", "Where do plans live in the repo?"
- **An agent needs grounded answers from the vault** — instead of free-form synthesis, anchor the response in real notes.
- **For complex, multi-hop questions** — Stage 2's multi-strategy retrieval surfaces both lexical and semantic matches; Stage 4's context assembly threads them together.

## When NOT to use <!-- :: section_id = when_not_to_use :: -->

- **For navigation queries** — "show me concept notes" — use `tessellum filter` directly.
- **For known-item lookup** — "find term_cqrs.md" — use `tessellum search --bm25 cqrs`.
- **For graph exploration** — "what connects to term_zettelkasten?" — use `tessellum search --bfs <seed>` (or `skill_tessellum_search_notes` with that flag).
- **When the answer should be uncited / creative** — this skill enforces citation; bypass for free-form generation.

## Step 1: query expansion <!-- :: section_id = step_1_query_expansion :: -->

Expand the raw user question into retrieval-friendly variants:

1. **Acronym detection**: identify tokens that match the pattern `^[A-Z]{2,8}$` (CQRS, DKS, BB, BM25, RRF, FZ, ...). For each, look up its expansion in the vault's term dictionary (filter by `note_second_category=terminology` + name match).
2. **Synonym hint**: extract 2-3 semantic variants if the question is dense (long, abstract). E.g. "How does Tessellum handle retrieval?" → ["retrieval", "search", "BM25 dense hybrid"].
3. **Term promotion**: any term-note name appearing verbatim in the question is added as a high-priority retrieval seed.

Output: `{ original: str, variants: list[str], seeds: list[note_id] }`.

## Step 2: multi-strategy retrieval <!-- :: section_id = step_2_retrieval :: -->

For each query variant, dispatch via `skill_tessellum_search_notes`. Combine results:

- **Hybrid (the default)** for the main question.
- **BFS from each seed** in `expansion.seeds` (max_depth=2, k=10).
- **BM25** on each variant individually (k=10) for token-precision matches.
- (Optional) **Filter** if the question hints at a kind — "concept notes about X" → `building_block=concept` filter.

Aggregate hits by `note_id`; deduplicate; carry per-strategy diagnostics for the next stage.

## Step 3: working-memory scoring <!-- :: section_id = step_3_working_memory :: -->

Score each candidate note by combining:

- **Strategy presence** — note appearing in N strategies' top-K is more confident.
- **In-degree** (from `tessellum.indexer.Database.links_to(note_id)`) — popular hubs are likely relevant.
- **Recency** — `note_creation_date` later → higher (configurable; relevant for "what's the latest?" intent).
- **BB priority** — `argument` and `concept` rank above `navigation` for explanatory questions.

Sort by combined score; truncate to ~20 candidates.

## Step 4: context assembly <!-- :: section_id = step_4_context_assembly :: -->

Build a token-budgeted context (default ~6K tokens):

1. **Grounded terms** (~1K tokens): include term-note bodies for any acronym/term mentioned in the question.
2. **Primary sources** (~4K): the top 5-8 ranked candidates, full body.
3. **Supporting** (~1K): brief excerpts (~200 tokens) from the next 5-10 candidates.

Use `tiktoken` (already in deps) for token counting. If the budget is exceeded, truncate the supporting tier first, then the primary tier.

Output: `{ tokens_used: int, included_note_ids: list[str], context_md: str }`.

## Step 5: synthesis with citations <!-- :: section_id = step_5_synthesis :: -->

Compose the answer:

1. **Cite every fact** — each load-bearing claim references the note inline via `[<note_name>](<relative_path>.md)` (placeholder syntax; substitute the real names + paths).
2. **Use the question's structure** — if the user asks "How does X work?", structure the answer as a procedure; "What is X?" → definition; "Compare X and Y" → comparison.
3. **Surface diagnostic info** — at the end, list the retrieval strategies used, the candidates considered, and a "see also" with related notes the user didn't ask about.

Output: `{ answer_md: str, cited_note_ids: list[str], strategies_used: list[str] }`.

## Output <!-- :: section_id = output :: -->

```json
{
  "answer_md": "Composer compiles a typed DAG by ... [as detailed in [term_dks](term_dialectic_knowledge_system.md)]...",
  "cited_note_ids": ["resources/term_dictionary/term_dialectic_knowledge_system.md", ...],
  "strategies_used": ["hybrid", "bfs", "bm25"],
  "diagnostics": {
    "stages": {
      "1_expansion": {"variants": ["composer", "DKS", "compile"], "seeds": []},
      "2_retrieval": {"hybrid_hits": 8, "bfs_hits": 5, "bm25_hits": 6, "merged": 14},
      "3_working_memory": {"top_n": 20, "discarded": 5},
      "4_context_assembly": {"tokens_used": 5821, "included_notes": 12},
      "5_synthesis": {"cited": 8}
    }
  }
}
```

## Validation <!-- :: section_id = validation :: -->

```bash
tessellum composer validate vault/resources/skills/skill_tessellum_answer_query.md
tessellum format check vault/resources/skills/skill_tessellum_answer_query.md
```

End-to-end testing requires Composer Wave 4 (LLM bridge) which ships later. Until then, this skill is documentation: a typed-contract spec for the QA pipeline that any LLM agent can follow procedurally.

## Error handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|---|---|---|
| Stage 2 returns 0 hits | Vault has no relevant notes | Fall back to a synthesized "I don't see notes about X yet" answer; suggest related searches. |
| Stage 4 budget exhausted | Question hits many notes | Drop the supporting tier first; surface a warning to the user. |
| Stage 5 produces uncited claims | Synthesis drift | Re-run with explicit "every claim must cite" prompt; flag QA-004. |
| Index missing | DB not built | Run `tessellum index build` first. |
| Acronym not in dictionary | Term note doesn't exist | Skip expansion for that token; document in diagnostics. |

## Related entry points <!-- :: section_id = related_entry_points :: -->

- [`skill_tessellum_search_notes.md`](skill_tessellum_search_notes.md) — Stage 2 calls this for retrieval.
- [`skill_tessellum_format_check.md`](skill_tessellum_format_check.md) — orthogonal; run before re-indexing if format may have drifted.
- [`plan_retrieval_port.md`](../../../plans/plan_retrieval_port.md) — Wave 5 (this skill) closes the v0.1 retrieval scope.
- [`term_dialectic_knowledge_system.md`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS is the runtime that will dispatch this skill once Composer Wave 4 ships.
