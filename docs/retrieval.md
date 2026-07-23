# Retrieval (`tessellum.retrieval`)

## The mental model

Once the vault is compiled into a SQLite index, someone has to ask questions of it. This is that read side: given the index and a query, it returns a ranked list of notes. It is deliberately small and passive. It never touches the markdown vault, never writes anything, and holds no state between calls beyond one cached embedding model. Everything it needs already sits in the index. Retrieval is not search from scratch — it is the art of ranking what is already there.

The core insight is that there is no single best way to find a note, because a question can arrive in several shapes. So retrieval offers five independent surfaces, each answering one shape: lexical keyword match, semantic similarity, a fusion of the two, graph traversal from a starting note, and structured metadata filtering. A caller picks the surface that fits the question. Hybrid — the fusion of keyword and semantic — is the production default, because it reliably surfaces notes that either method alone would miss.

## The model — how the pieces relate

The index is one SQLite database holding two base tables (the note records and the links between them) and two virtual tables (a full-text index for lexical search, a vector index for semantic search). Retrieval is a thin, read-only skin over those tables. Each surface reads exactly the tables it needs and nothing more.

```
query ──▶ [ bm25 | dense | hybrid | bfs | metadata ] ──▶ list[*Hit]
              │       │        │        │        │
          full-text  vector   │      link graph  note records
           index     index    └─(fuses bm25 + dense by rank)
                                      (in-degree = hub signal)
```

The relationships stay simple. BM25 reads the full-text index for keyword matches. Dense reads the vector index for semantic neighbors. Hybrid touches no table directly — it calls the BM25 and dense surfaces and merges their two ranked lists. BFS loads the link graph and walks outward from a starting note. Metadata filters the note records by their structured fields. Every surface follows one contract: take the index path plus a query, open a short-lived connection, run one query, close it, and return a list of immutable hit objects. That shared contract is what makes hybrid possible — it composes two surfaces for free — and it makes any surface trivially testable in isolation.

One convention unifies all five: the score. Every hit carries a `score` where higher always means more relevant, no matter what the underlying SQLite primitive returned. This lets a caller sort and compare results from any strategy without knowing anything about the machinery beneath.

## The procedure — how a query flows through

**Lexical (BM25).** The query is handed straight to the full-text index's match operator, so the whole FTS5 query language is available — prefix matches, quoted phrases, boolean operators, per-field filters. Malformed syntax surfaces as a plain SQLite error rather than a silent empty result. Results come back ranked by relevance, each optionally carrying a highlighted snippet so the matched terms are easy to spot in a terminal. Reach for this surface when you know the exact word you are looking for.

**Semantic (dense).** The query is encoded into a vector by a sentence-transformer model, then compared against the pre-computed note vectors to find the nearest neighbors by cosine similarity. The model loads lazily and is cached for the life of the process, so the first query pays a one-time startup cost and later ones do not. This surface finds notes that are *about* the same thing even when they share no vocabulary with the query — the case where keyword search goes blind.

**Hybrid (the default).** This runs the lexical and semantic searches in turn, then fuses their two ranked lists using Reciprocal Rank Fusion. Fusing on *rank* rather than raw score is the whole trick. BM25 and cosine scores live on incomparable scales, so adding them directly would be meaningless; ranks are scale-free, so they combine robustly. The fused hits also record where each note placed in each list, which lets a caller see *why* a note surfaced. A note that ranked high in both lists is a strong agreement hit; one that appeared only in the semantic list is a "semantic-only" find worth a second look. And if the semantic side is unavailable — say, an index built without vectors — hybrid does not fail. It quietly returns lexical-only results.

**Graph traversal (BFS).** Here the query is not free text but a seed note — the starting point. The traversal loads the link graph and walks outward from the seed with a best-first frontier. Two deliberate asymmetries govern the walk. Links are traversed as *undirected*, because a link conceptually relates both of its endpoints, so relatedness flows both ways. But a note's *inbound* link count is read as a popularity signal: a note that many notes point at is a hub. The frontier is ordered so that each ring of neighbors is exhausted before going deeper, and among equally distant notes the less-popular, more-specific ones surface first. Hubs above a threshold are returned as hits but are not expanded. This hub-skip is the load-bearing move — it stops the traversal from degenerating into "everything connects to everything through the most-linked note." The seed itself always expands, since it is the user's chosen entry point. Each hit's score decays with distance from the seed, and every hit carries the full path back.

**Metadata filtering.** The simplest surface, and a different question entirely: not *what content* but *what kind* of note. It builds a SQL `WHERE` clause from whatever structured filters the caller supplied — building block, status, category, date range, folgezettel prefix, and so on — and combines them all with AND. Exact-value and range fields use direct comparisons; the free-form array fields (tags, keywords, topics) are matched by exact membership rather than substring, so a filter for `cqr` never accidentally catches `cqrs`. "Show me all concept notes about CQRS that are still in draft" is a metadata query, not a content one.

## Design decisions and why

**One score convention, higher-is-better, everywhere.** The underlying primitives disagree with each other. The full-text ranker is lower-is-better; the vector index returns a distance where lower is closer. Each surface flips its primitive so the public score always reads the intuitive way — the lexical surface still *orders* by the raw value so the ranking stays correct, and only the displayed sign is flipped. The payoff is a single mental model for the caller: any hit from any strategy sorts and compares the same way.

**Stateless, index-in / hits-out.** Every surface opens and closes its own connection and shares no state across calls, except the cached embedding model, which is a pure process-level performance cache. This is exactly what lets the surfaces compose — hybrid literally calls two of them — and it keeps the layer free of locks and long-lived handles. The hit objects are frozen value objects, safe to pass around and cache.

**Hybrid degrades, it never fails.** A missing or broken semantic index should still answer queries, so a failure on the semantic side is swallowed and the query returns lexical-only results. Availability beats completeness. A partial answer serves the user; an exception does not.

**BFS uses an undirected walk but a directed hub signal.** These two facts pull in opposite directions on purpose. Reachability is bidirectional because conceptual relatedness is symmetric — a link means both endpoints are related. But popularity is specifically an *inbound* count: a hub is defined by how many notes point at it. Declining to expand hubs is what keeps results focused and bounded rather than letting one popular note flood the frontier.

**No PageRank, anywhere in this layer.** This is a load-bearing decision, not an omission. The empirical correlation between retrieval hit-rate and actual answer-quality was measured and came out weak. That finding is decisive: Personalized PageRank's expensive multi-hop walks would be optimizing a metric that does not translate into better answers. Best-first BFS is simpler, faster, and Pareto-optimal in practice, so it wins. Consistent with this, the shipped index does not even carry a PageRank column, and no surface references one. (A stale "ppr" mention survives in a module docstring — there is no such function, flag, or column.)

**The router exists but is not wired in.** Alongside the five surfaces sits a heuristic router that classifies a query and picks a strategy for you: a `.md` path routes to graph traversal, a bare identifier to lexical, and everything sentence-shaped to hybrid. It mirrors the decision tree the search-notes agent skill uses, but no CLI command calls it. It is there for programmatic callers — CI scripts, ablation tests, a future agent runtime — who want the strategy chosen for them without rendering the skill canonical. The CLI instead wires each strategy directly, keeping the router optional. Notably the router never picks metadata for free text: metadata is a surface you reach for only when you already hold structured filters.

**The CLI splits along the content/metadata seam.** Content retrieval lives under `tessellum search`, with mutually-exclusive strategy flags defaulting to hybrid. Metadata filtering lives under a separate `tessellum filter`. The split mirrors the underlying divide — one command asks about content, the other about kind — and keeps each command's flags coherent.

**Reference:** [reference/retrieval.md](reference/retrieval.md) — API, symbols, and signatures.
