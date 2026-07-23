# Building Block (BB) Ontology — `tessellum.bb`

## Purpose

`tessellum.bb` is the source-of-truth for Tessellum's typed substrate: the 8 Building Block types and the ~16-edge schema graph of epistemic transitions between them. It splits a **schema view** (finite, closed, type-level — what transitions are *allowed*) from a **corpus view** (open, growing, instance-level — what edges the vault *actually realises*), so the DKS runtime can type-check its FSM walk and `tessellum bb audit` can measure structural balance across the real corpus.

## Architecture / Data Flow

Two layers, mirroring the schema-vs-corpus split (`bb/__init__.py:15-21`):

```
  bb/types.py  (schema — closed, type-level)
    BBType (8 enum members)  ── the FSM states
    EpistemicEdgeType        ── one typed transition (source, target, label)
    BB_SCHEMA = EPISTEMIC(8) + NAVIGATION(7) + DKS_EXTENSIONS(1) + USER_EXTENSIONS(0+)
    fold_schema_events / BB_SCHEMA_AT_VERSION / BB_SCHEMA_VERSION  ── event-sourced growth
          │
          │  find_edge_type(src.bb_type, tgt.bb_type)  (the type-check)
          ▼
  bb/graph.py  (corpus — open, instance-level, read-only)
    BBNode (+ 8 per-type subclasses), BBEdge (with provenance)
    BBGraph.schema()   ── synthetic 8-node graph over BB_SCHEMA
    BBGraph.from_db()  ── loads corpus from the index DB
          │
          ▼
  cli/bb.py  (tessellum bb audit / migrate)
```

Flow: `frontmatter_spec.VALID_BUILDING_BLOCKS` is derived from `BBType` (`format/frontmatter_spec.py:30`), so every captured note's `building_block:` YAML field must be one of the 8. `BBGraph.from_db` reads the built index DB (`indexer.db.Database`), keeps only notes whose `building_block` parses as a `BBType`, and materialises two edge families — body-links and folgezettel-parent links — stamping each with the schema edge it instantiates (or `None` if untyped). `tessellum bb audit` walks that corpus graph for telemetry; `tessellum bb migrate` reconciles each note's frozen `bb_schema_version` against the current schema version.

## Key Modules + Abstractions

| File | Role |
|------|------|
| `bb/types.py` | Schema source-of-truth: `BBType` (8), `EpistemicEdgeType`, the four schema tuples composing `BB_SCHEMA`, the event-sourcing machinery (`SchemaEditEvent`, `fold_schema_events`, `set_user_extensions_from_events`), versioning (`BB_SCHEMA_VERSION`, `BB_SCHEMA_AT_VERSION`), and lookups (`find_edge_type`, `edges_from`, `edges_to`, `is_valid_transition`). |
| `bb/graph.py` | Corpus (instance) view: `BBNode` + 8 per-type subclasses, `BBEdge` (with provenance), `BBGraph` with `schema()`/`from_db()` constructors, O(1) node/edge indexes, and audit helpers (`untyped_edges`, `unrealised_schema_edges`, `edges_by_type`). |
| `bb/__init__.py` | Public façade re-exporting both layers under `tessellum.bb`. |
| `cli/bb.py` | `tessellum bb {audit,migrate}` — corpus telemetry and retroactive `bb_schema_version` classification. |
| `format/building_blocks.py` | **Legacy parallel implementation** (`BuildingBlock` enum, `EPISTEMIC_EDGES` = 10, `BB_SPECS`). Still exported from `tessellum` top-level; see caveat below. |

### `BBType` — 8 types (`bb/types.py:35-57`)

A `StrEnum`: `EMPIRICAL_OBSERVATION`, `CONCEPT`, `MODEL`, `HYPOTHESIS`, `ARGUMENT`, `COUNTER_ARGUMENT`, `PROCEDURE`, `NAVIGATION`. This is the single source of truth — `frontmatter_spec.VALID_BUILDING_BLOCKS` derives from it, and DKS dataclasses carry a `bb_type` class-attribute pointing here.

### `EpistemicEdgeType` — one typed transition (`bb/types.py:68-86`)

Frozen dataclass `(source: BBType, target: BBType, label: str)`. It is a *type*, not an *instance*: a corpus `BBEdge` is one realisation of one `EpistemicEdgeType`. The schema graph holds ~16 such types; the corpus can hold many edges per type.

### `BB_SCHEMA` — four composed tuples, ~16 edges (`bb/types.py:377-382`)

`BB_SCHEMA = BB_SCHEMA_EPISTEMIC + BB_SCHEMA_NAVIGATION + BB_SCHEMA_DKS_EXTENSIONS + BB_SCHEMA_USER_EXTENSIONS`:

- **`BB_SCHEMA_EPISTEMIC` — 8 edges** (`bb/types.py:99-108`), the dialectic cycle: OBS→CON (naming), CON→MOD (structuring), MOD→HYP (predicting), MOD→PRO (codifying), HYP→ARG (testing), ARG→CTR (challenging), CTR→OBS (motivates_new), PRO→OBS (execution_data).
- **`BB_SCHEMA_NAVIGATION` — 7 edges** (`bb/types.py:119-130`), generated as NAV→X (`"indexes"`) for each of the 7 non-navigation types. FZ 1's narrative collapses these into one "Navigation → all" family; the implementation expands them so the FSM can type-check NAV-to-X transitions like any other.
- **`BB_SCHEMA_DKS_EXTENSIONS` — 1 edge** (`bb/types.py:145-149`): `COUNTER_ARGUMENT → MODEL` (`"pattern_of_failure"`). Runtime-required by DKS step 6's pattern discovery but absent from FZ 1's 10-edge narrative; committed in package source rather than event-sourced.
- **`BB_SCHEMA_USER_EXTENSIONS` — 0+ edges** (`bb/types.py:250`): event-sourced, ships empty by default.

So the shipped default is 8 + 7 + 1 + 0 = **16 edges**.

### `BBNode` + 8 subclasses (`bb/graph.py:47-132`)

`BBNode` is a frozen, kw-only dataclass (`note_id`, `note_name`, `bb_type`, `folgezettel`, `folgezettel_parent`, `note_status`). Per design decision D1, there is one subclass per `BBType` (`EmpiricalObservationNode`, `ConceptNode`, …, `NavigationNode`), each fixing `bb_type` via `field(default=X, init=False)` so the discriminator stays out of every constructor call while remaining statically typed. `_NODE_CLASS_BY_BB_TYPE` / `node_class_for` map a type to its subclass; `BBGraph.from_db` uses this to instantiate the right subclass per corpus note.

### `BBEdge` with provenance (`bb/graph.py:135-157`)

Frozen dataclass `(source_note_id, target_note_id, edge_type: EpistemicEdgeType | None, provenance: str)`. `edge_type=None` means the corpus edge instantiates no schema edge (an *untyped* edge — a validator/audit candidate). `provenance` is `"body_link"`, `"folgezettel_parent"`, `"schema"` (synthetic), or `"contradicts"` (reserved for a future DKS writer — not yet emitted by `from_db`).

### `BBGraph` — typed corpus view (`bb/graph.py:163-401`)

Two constructors:
- `BBGraph.schema()` (`bb/graph.py:192-217`) — synthetic graph: 8 `BBNode`s (one per type, `note_id = bb.value`) + one `BBEdge` per `BB_SCHEMA` entry (`provenance="schema"`). For "what transitions are allowed?" without touching the corpus.
- `BBGraph.from_db(db_path)` (`bb/graph.py:219-304`) — loads the corpus. Lazily imports `indexer.db.Database` (so BB consumers don't pay the sqlite cost at import), walks `all_notes()` keeping BB-typed notes, then walks `all_links()` for body-link edges (both endpoints must be BB nodes) and adds a second family from `folgezettel_parent → folgezettel` resolution. Each edge's `edge_type` is set by `find_edge_type(src.bb_type, tgt.bb_type)`.

The constructor builds `_nodes_by_id`, `_nodes_by_type`, `_out_edges`, `_in_edges` up-front so reads are O(1) / O(|out-edges|). Read API: `node`, `nodes_of_type`, `out_edges`, `in_edges`, `edges`, `node_count`, `edge_count`, plus `__iter__/__len__/__contains__`. Audit helpers: `untyped_edges()`, `unrealised_schema_edges()` (matches by `(source, target)` BB-pair only, not label), `edges_by_type()` (label→count, untyped grouped under `"(untyped)"`).

## Invariants / Design Decisions + WHY

- **Schema is closed and finite; corpus is open and view-only.** `bb/types.py` mutates only via disciplined revision; `bb/graph.py` never writes the substrate (`bb/graph.py:26-27`). WHY: this is R-P's productive half — the FSM exercises whatever the schema declares, and schema growth is a deliberate, auditable act, not a runtime side-effect.

- **A corpus edge instantiates exactly one schema edge, or is untyped.** `find_edge_type` matches by `(source, target)` (unique across `BB_SCHEMA` today, so "first" = "only" — `bb/types.py:394-402`). WHY: makes the schema a type-checker for realised links; untyped edges surface as either a bad link or a missing schema edge (the R-P productive-half signal).

- **Schema growth is event-sourced, retractions first-class (`bb/types.py:152-284`).** `BB_SCHEMA_USER_EXTENSIONS` is the *fold* over an append-only `SchemaEditEvent` log — the surface the **meta-DKS** mutates. `fold_schema_events` handles `added` / `retracted` / `refined` (`refined` = drop prior `(source,target)` + add new); the log is never rewritten. WHY (per D3): schema *state* must be retractable but schema *history* append-only, so a retracted edge's corpus instances become untyped (a TESS-005 migration signal) without losing the audit trail.

- **Frozen-at-creation `bb_schema_version` (D8).** Every captured note records the schema version it was created under; `BB_SCHEMA_VERSION` bumps once per landed `added`/`retracted` event (`refined` doesn't bump separately — it's a retract+add composition, `bb/types.py:277-279`). `BB_SCHEMA_AT_VERSION(v)` reconstructs the schema as of version `v` by folding the event-log prefix, memoised per `(version, log-length, log-identity)` (`bb/types.py:290-352`). WHY: validators (TESS-005) check a note against the schema it was *born under*, not the current one — otherwise every schema edit would retroactively invalidate old notes. The core epistemic + navigation + DKS-extension tuples are constant across all versions; only `USER_EXTENSIONS` varies.

- **Default event log is empty; real events live outside package + vault.** Events land via `tessellum dks --meta --apply` at `runs/dks/meta/schema_events.jsonl`, same shape as `warrant_history.jsonl` (`bb/types.py:161-165`). `set_user_extensions_from_events` rebuilds `BB_SCHEMA`, `BB_SCHEMA_VERSION`, and clears the version cache in one call (`bb/types.py:253-279`). WHY: separates shipped code from per-deployment schema state.

- **Per-`BBType` subclass hierarchy (D1)** keeps the discriminator statically typed and out of constructors (`bb/graph.py:73-127`). Synthetic schema nodes use bare `BBNode` with explicit `bb_type` since they aren't real corpus instances.

- **`from_db` streams then closes the DB.** It pulls `all_notes()`/`all_links()` inside a `with Database(...)` block and builds in memory, rather than holding the connection (`bb/graph.py:242-244`). Untyped corpus edges are *kept* (`edge_type=None`) so callers can audit them, not dropped.

- **Enforcement is currently narrow.** `is_valid_transition` is available for a general "every realised BB-link must instantiate a declared edge" rule, but TESS-004 today only enforces `counter_argument → argument` and TESS-005 is WARNING-only (`bb/types.py:415-424`, `cli/bb.py:366-374`). Say so plainly: the schema *can* type-check every link, but the wired validators do not yet.

## Public API / CLI

Import surface (`bb/__init__.py:37-110`), all under `tessellum.bb`:

- Schema: `BBType`, `VALID_BB_TYPE_VALUES`, `EpistemicEdgeType`, `BB_SCHEMA_EPISTEMIC`, `BB_SCHEMA_NAVIGATION`, `BB_SCHEMA_DKS_EXTENSIONS`, `BB_SCHEMA_USER_EXTENSIONS`, `BB_SCHEMA`, `BB_SCHEMA_AT_VERSION`, `BB_SCHEMA_VERSION`, `SCHEMA_EDIT_KIND`, `SchemaEditEvent`, `fold_schema_events`, `set_user_extensions_from_events`, `schema_event_log`.
- Lookups: `find_edge_type`, `edges_from`, `edges_to`, `is_valid_transition`.
- Corpus: `BBNode`, `BBEdge`, `BBGraph`, the 8 node subclasses, `node_class_for`.

CLI — `tessellum bb` is one of Tessellum's 11 CLI commands (wired in `cli/main.py:14`), with two sub-subcommands (`cli/bb.py`):

- **`tessellum bb audit [--db PATH] [--format human|json] [--show-untyped]`** — builds `BBGraph.from_db` and reports: nodes by BB type, edges by schema label, untyped corpus edges (count + BB-pair breakdown, full list under `--show-untyped`), orphan BB nodes (no inbound/outbound edges), and unrealised schema edges (0 corpus instances). JSON omits the verbose per-edge list unless `--show-untyped` (`cli/bb.py:111-292`).
- **`tessellum bb migrate [--vault PATH] [--target-version current|N] [--apply] [--format ...]`** — walks the vault, finds notes whose recorded `bb_schema_version` is below target, runs `validate()` to classify each as would-pass / would-fail under TESS-005, and (with `--apply`) bumps the frontmatter version on would-pass notes only. Would-fail notes are reported but **never auto-rewritten** — manual review required (`cli/bb.py:303-482`). Absent `bb_schema_version` defaults to 1.

Exit codes: `0` completed (warnings are not failure), `2` invocation error (DB/vault missing).

## Extension Points

- **Add a schema edge at runtime** — append a `SchemaEditEvent(kind="added", …)` to the event log and call `set_user_extensions_from_events`; this is how meta-DKS grows the schema (`bb/types.py:253`). The `motivating_failure` field anchors the dialectical justification.
- **Commit a schema edge in source** — for edges the project team owns (not per-deployment), add to `BB_SCHEMA_DKS_EXTENSIONS` (`bb/types.py:145`), the canonical place for runtime-driven growth the static palette would miss.
- **New audit heuristics** — `BBGraph.untyped_edges` and `unrealised_schema_edges` feed meta-DKS heuristics (e.g. Heuristic-2 retract-unused-edge consumes `unrealised_schema_edges`, `bb/graph.py:359-387`).
- **New provenance family** — `BBEdge.provenance` already reserves `"contradicts"` for a future DKS writer; `from_db` would gain a third edge-building loop.
- **Tighten enforcement** — generalise TESS-004 to call `is_valid_transition` over all realised BB-pairs, and/or promote TESS-005 from WARNING to ERROR.

## Caveat: Two Parallel BB Implementations

There are **two** BB ontology implementations in the tree, both exported from the top-level `tessellum` package:

1. **`tessellum.bb`** (this doc) — `BBType` `StrEnum`, `EpistemicEdgeType`, `BB_SCHEMA` (~16 edges, versioned + event-sourced). This is the source of truth wired into validation: `frontmatter_spec.VALID_BUILDING_BLOCKS` derives from `BBType` (`format/frontmatter_spec.py:30`).
2. **`tessellum.format.building_blocks`** (legacy) — a separate `BuildingBlock` `str, Enum` (same 8 string values), `EpistemicLayer`, `BBSpec`/`BB_SPECS` (per-type metadata: question, function, required sections), and `EPISTEMIC_EDGES` — a **10-edge** tuple (8 core + 2 explicit NAV edges, with the rest of the NAV family generated on demand by `all_edges_with_navigation_complete`). It is re-exported from both `tessellum.format` (`format/__init__.py:19-28`) and the top-level `tessellum` package (`tessellum/__init__.py:27-42`), and `cli/main.py:57` advertises `from tessellum import BuildingBlock, BB_SPECS, EPISTEMIC_EDGES` in its help text.

The two enums are byte-compatible at the string level (identical 8 values), but they are distinct Python types with different edge counts (16 vs 10) and different data models (`EpistemicEdgeType` vs `BBEdge`+`BBSpec`). The validator path and `tessellum bb` CLI use only `tessellum.bb`; `building_blocks.py` survives for its per-type `BB_SPECS` metadata (required sections, epistemic function/question, layer grouping) which `tessellum.bb` does not carry. Contributors should treat `tessellum.bb.BBType` / `BB_SCHEMA` as canonical for typing and transitions, and reach for `format.building_blocks.BB_SPECS` only when they need the descriptive per-type spec. Consolidating the two remains an open cleanup.
