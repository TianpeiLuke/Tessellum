---
tags:
  - resource
  - skill
  - procedure
  - vault_query
  - retrieval
keywords:
  - search notes
  - retrieval router
  - decision tree
  - multi-strategy search
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
  - Retrieval
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
related_skill_headers: []
pipeline_metadata: ./skill_tessellum_search_notes.pipeline.yaml
---

# Procedure: tessellum-search-notes (Canonical Body)

This is the canonical body for the `tessellum-search-notes` skill. Pairs with [`skill_tessellum_search_notes.pipeline.yaml`](skill_tessellum_search_notes.pipeline.yaml) — the typed contract for Composer dispatch (Wave 4+ runs the steps; v0.0.18 ships the canonical + sidecar but the runtime is pending).

The skill picks the right retrieval surface for a query and returns ranked notes. Five surfaces are available — the decision is heuristic (cheap, transparent) rather than ML-routed.

## Skill description <!-- :: section_id = skill_description :: -->

Search the indexed Tessellum vault using the most appropriate retrieval strategy for the query intent. Returns ranked notes with diagnostic metadata (per-ranker scores, depth/path for graph traversal, matched fields). Wraps `tessellum.retrieval.{bm25,dense,hybrid,best_first_bfs,metadata}_search` behind a decision-tree router (`tessellum.retrieval.classify_query`).

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version  # ensure v0.0.18+

# Index must exist with FTS5 + sqlite-vec populated for full strategy support.
tessellum index build --vault vault --db data/tessellum.db
```

## Resources <!-- :: section_id = resources :: -->

- **Library entry**: `tessellum.retrieval.route(db_path, query, *, k)` — returns `(decision, hits)`.
- **Library primitives**: `bm25_search`, `dense_search`, `hybrid_search`, `best_first_bfs`, `metadata_search`.
- **CLI**: `tessellum search <query>` (content) + `tessellum filter <flags>` (metadata).
- **Index DB**: `data/tessellum.db` (build via `tessellum index build`).
- **Plan**: [`plan_retrieval_port.md`](../../../plans/plan_retrieval_port.md) — five-wave port + the three load-bearing lessons (hybrid as default, no PPR, validate on answer quality).

## Validation rules reference <!-- :: section_id = validation_rules_reference :: -->

| Rule | Severity | Check |
|---|---|---|
| RTR-001 | ERROR | Query is non-empty |
| RTR-002 | INFO | Single-token query → BM25 |
| RTR-003 | INFO | Path-shaped query → BFS |
| RTR-004 | INFO | Multi-word / question-shaped query → hybrid |
| RTR-005 | INFO | Empty query → hybrid fallback (with warning) |
| RTR-006 | WARNING | Index DB missing required tables (notes_fts / notes_vec) — fall back gracefully |

These are diagnostic-class rules, not validator-enforced (the search-notes skill is read-only — it doesn't mutate the vault).

## When to use <!-- :: section_id = when_to_use :: -->

- **Free-form retrieval requests** — "find notes about X", "what's related to Y?", "where did I write about Z?"
- **As an agent's first retrieval step** before context assembly (`skill_tessellum_answer_query` calls this).
- **For ablation / diagnostics** — pass `--bm25` / `--dense` / `--hybrid` / `--bfs` / `--filter` directly to bypass the router.
- **When you want diagnostic info** — the router returns `(decision, hits)`; agents can render the `decision.reason` to users.

## When NOT to use <!-- :: section_id = when_not_to_use :: -->

- **For known structured queries** — if you already know the filter (`building_block=concept` and `tag=cqrs`), call `tessellum filter` directly.
- **For broken-link / format-check workflows** — use `tessellum format check` instead. The search-notes skill assumes the index is well-formed.
- **For composing a long-form answer** — that's `skill_tessellum_answer_query`'s job. This skill returns the ranked notes; answer composition is a separate stage.

## Step 1: parse query intent <!-- :: section_id = step_1_parse_intent :: -->

Call `classify_query(query)` to get a `RouterDecision`. The classifier is heuristic:

1. **Vault path with `.md`** → `bfs` (treat the query as a seed note_id and traverse the link graph).
2. **Single short token / identifier** (≤ 30 chars, no spaces) → `bm25` (lexical lookup beats fusion overhead).
3. **Question-shaped** (ends with `?`) or **multi-word** (≥ 4 tokens) → `hybrid` (BM25 + dense fused via RRF — the +12pp production winner).
4. **Empty / unknown** → `hybrid` fallback (with `decision.reason` carrying a warning).

The agent can override by calling the primitive directly. The router's job is a sensible default, not a binding decision.

## Step 2: dispatch to the recommended primitive <!-- :: section_id = step_2_dispatch :: -->

```python
from tessellum.retrieval import route

decision, hits = route("data/tessellum.db", query, k=20)
print(f"Strategy: {decision.strategy} — {decision.reason}")
for hit in hits:
    # hit is one of BM25Hit / DenseHit / HybridHit / GraphHit / MetadataHit
    print(f"  {hit.note_name}  ({hit.score:.3f})")
```

For CLI agents:

```bash
tessellum search "<query>"        # uses hybrid by default; ~30ms warm
tessellum search --bm25 "<token>" # for single-token lexical
tessellum search --bfs "<seed>"   # for path-shaped queries
tessellum filter --tag cqrs       # for structured filtering
```

## Step 3: return ranked hits with diagnostics <!-- :: section_id = step_3_return_hits :: -->

The agent should surface:

- **The strategy used** + the router's reason (so the user understands why these results).
- **Top-N hits** with note_name, score, and per-strategy diagnostics (BM25 snippet, hybrid bm25_rank/dense_rank, BFS depth/path, metadata flags).
- **Empty-result handling** — if the chosen strategy returns no hits, optionally re-try with a fallback strategy (e.g. BM25 → dense for misspellings).

For programmatic callers, return the `(decision, hits)` tuple unchanged.

## Output <!-- :: section_id = output :: -->

```json
{
  "decision": {
    "strategy": "hybrid",
    "reason": "multi-word / question-shaped: hybrid wins on real answer-quality"
  },
  "hits": [
    {"note_id": "...", "note_name": "term_cqrs", "score": 0.0318, ...}
  ]
}
```

## Validation <!-- :: section_id = validation :: -->

```bash
# Verify the canonical's pipeline sidecar pairs cleanly with this skill.
tessellum composer validate vault/resources/skills/skill_tessellum_search_notes.md

# Verify the canonical itself passes format check.
tessellum format check vault/resources/skills/skill_tessellum_search_notes.md

# End-to-end smoke (Python):
python -c "
from tessellum.retrieval import route
decision, hits = route('data/tessellum.db', 'composer', k=3)
print(decision.strategy, '→', [h.note_name for h in hits])
"
```

## Error handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|---|---|---|
| `FileNotFoundError: index DB not found` | DB missing | Run `tessellum index build` first |
| `sqlite3.OperationalError: no such table: notes_fts` | Build was `--no-dense` and BM25 surface unavailable | Re-run `tessellum index build --force` (FTS5 is now mandatory; only `--no-dense` skips embeddings) |
| `sqlite3.OperationalError: no such table: notes_vec` | Build was `--no-dense` | Either rebuild with embeddings, or pass `--bm25` to bypass dense |
| Empty result list | No matches | Try a different strategy; widen `k`; check spelling for BM25 |

## Related entry points <!-- :: section_id = related_entry_points :: -->

- [`skill_tessellum_answer_query.md`](skill_tessellum_answer_query.md) — calls this skill for retrieval, then assembles a synthesized answer.
- [`skill_tessellum_format_check.md`](skill_tessellum_format_check.md) — vault format validation; orthogonal but commonly run before re-indexing.
- [`plan_retrieval_port.md`](../../../plans/plan_retrieval_port.md) — the design rationale + lessons learned (no PPR; hybrid as default; +12pp validation).
- [`term_cqrs.md`](../term_dictionary/term_cqrs.md) — System D (retrieval) is one half of the CQRS substrate this skill operates on.
