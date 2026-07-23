# `tessellum.bb` — Reference

API, symbols, and signatures for the BB ontology. For the mental model and how work flows through it, see [../bb.md](../bb.md).

## File → role

| File | Role |
|------|------|
| `bb/types.py` | Schema source-of-truth. `BBType` (8), `EpistemicEdgeType`, the four schema tuples composing `BB_SCHEMA`, event-sourcing (`SchemaEditEvent`, `fold_schema_events`, `set_user_extensions_from_events`, `schema_event_log`), versioning (`BB_SCHEMA_VERSION`, `BB_SCHEMA_AT_VERSION`), and lookups (`find_edge_type`, `edges_from`, `edges_to`, `is_valid_transition`). |
| `bb/graph.py` | Corpus (instance) view. `BBNode` + 8 per-type subclasses, `BBEdge` (with provenance), `BBGraph` with `schema()` / `from_db()` constructors, O(1) node/edge indexes, and audit helpers. |
| `bb/__init__.py` | Public façade re-exporting both layers under `tessellum.bb`. |
| `cli/bb.py` | `tessellum bb {audit,migrate}` — corpus telemetry and retroactive `bb_schema_version` classification. Registered in `cli/main.py`. |
| `format/building_blocks.py` | **Legacy parallel implementation** (`BuildingBlock` enum, `EpistemicLayer`, `BBSpec` / `BB_SPECS`, `EPISTEMIC_EDGES` = 10). Still exported from `tessellum` top-level; see [../bb.md](../bb.md) caveat. |

## Schema layer — `tessellum.bb.types`

### Types

- `BBType(StrEnum)` — the 8 building-block types: `EMPIRICAL_OBSERVATION`, `CONCEPT`, `MODEL`, `HYPOTHESIS`, `ARGUMENT`, `COUNTER_ARGUMENT`, `PROCEDURE`, `NAVIGATION` (string values are the lowercase names). Source of truth; `format.frontmatter_spec.VALID_BUILDING_BLOCKS` derives from it.
- `VALID_BB_TYPE_VALUES: frozenset[str]` — the 8 string values, for callers wanting the `frozenset[str]` shape.
- `EpistemicEdgeType` — `@dataclass(frozen=True)` with `source: BBType`, `target: BBType`, `label: str`. One typed transition; a type, not an instance.
- `SCHEMA_EDIT_KIND = Literal["added", "retracted", "refined"]`.
- `SchemaEditEvent` — `@dataclass(frozen=True)`: `timestamp: str` (UTC ISO-8601), `kind: SCHEMA_EDIT_KIND`, `edge: EpistemicEdgeType`, `motivating_failure: str = ""`, `superseded_by: str | None = None`.

### Schema data

| Symbol | Type | Contents |
|--------|------|----------|
| `BB_SCHEMA_EPISTEMIC` | `tuple[EpistemicEdgeType, ...]` (8) | The dialectic cycle. See table below. |
| `BB_SCHEMA_NAVIGATION` | `tuple[EpistemicEdgeType, ...]` (7) | `NAVIGATION → X` labelled `"indexes"`, for each of the 7 non-navigation types. |
| `BB_SCHEMA_DKS_EXTENSIONS` | `tuple[EpistemicEdgeType, ...]` (1) | `COUNTER_ARGUMENT → MODEL` labelled `"pattern_of_failure"` (DKS step 6 pattern discovery). |
| `BB_SCHEMA_USER_EXTENSIONS` | `tuple[EpistemicEdgeType, ...]` (0+) | The fold over the in-memory event log; ships empty. |
| `BB_SCHEMA` | `tuple[EpistemicEdgeType, ...]` | `EPISTEMIC + NAVIGATION + DKS_EXTENSIONS + USER_EXTENSIONS`. Shipped default = 8 + 7 + 1 + 0 = **16**. |
| `BB_SCHEMA_VERSION` | `int` | Ships at `1`; bumps once per landed `added` / `retracted` event (`refined` does not bump). |

`BB_SCHEMA_EPISTEMIC` — the 8 edges:

| Source | Target | Label |
|--------|--------|-------|
| `EMPIRICAL_OBSERVATION` | `CONCEPT` | `naming` |
| `CONCEPT` | `MODEL` | `structuring` |
| `MODEL` | `HYPOTHESIS` | `predicting` |
| `MODEL` | `PROCEDURE` | `codifying` |
| `HYPOTHESIS` | `ARGUMENT` | `testing` |
| `ARGUMENT` | `COUNTER_ARGUMENT` | `challenging` |
| `COUNTER_ARGUMENT` | `EMPIRICAL_OBSERVATION` | `motivates_new` |
| `PROCEDURE` | `EMPIRICAL_OBSERVATION` | `execution_data` |

### Functions

- `find_edge_type(source: BBType, target: BBType, label: str | None = None) -> EpistemicEdgeType | None` — first schema edge matching the pair (and label if given). The `(source, target)` pair is unique across `BB_SCHEMA` today, so "first" = "only". `None` when no match.
- `edges_from(source: BBType) -> tuple[EpistemicEdgeType, ...]` — all schema edges leaving `source`.
- `edges_to(target: BBType) -> tuple[EpistemicEdgeType, ...]` — all schema edges entering `target`.
- `is_valid_transition(source: BBType, target: BBType) -> bool` — `True` iff `(source, target)` is a declared schema edge (`find_edge_type(...) is not None`).
- `fold_schema_events(events: Sequence[SchemaEditEvent]) -> tuple[EpistemicEdgeType, ...]` — compute the active user-extension set. `added` inserts; `retracted` removes; `refined` drops the prior `(source, target)` (any label) and adds the new edge. Returns an insertion-ordered, deduplicated tuple.
- `set_user_extensions_from_events(events: Sequence[SchemaEditEvent]) -> None` — replace the in-memory event log; recompute `BB_SCHEMA_USER_EXTENSIONS`, `BB_SCHEMA`, and `BB_SCHEMA_VERSION`; clear the `BB_SCHEMA_AT_VERSION` cache. Used at CLI startup and in tests.
- `schema_event_log() -> tuple[SchemaEditEvent, ...]` — defensive copy of the in-memory event log.
- `BB_SCHEMA_AT_VERSION(version: int) -> tuple[EpistemicEdgeType, ...]` — reconstruct the full `BB_SCHEMA` as of `version` by folding the event-log prefix whose post-fold version is `≤ version`. `version=1` = the core static schema (no user extensions). Raises `ValueError` if `version < 1`. Memoised per `(version, len(log), id(log))`.

Real events live at `runs/dks/meta/schema_events.jsonl` (outside the package and vault), written by `tessellum dks meta --apply`.

## Corpus layer — `tessellum.bb.graph`

### Node dataclasses

- `BBNode` — `@dataclass(frozen=True, kw_only=True)`: `note_id: str = ""`, `note_name: str = ""`, `bb_type: BBType = BBType.NAVIGATION`, `folgezettel: str | None = None`, `folgezettel_parent: str | None = None`, `note_status: str | None = None`.
- 8 per-type subclasses, each fixing `bb_type` via `field(default=..., init=False)`: `EmpiricalObservationNode`, `ConceptNode`, `ModelNode`, `HypothesisNode`, `ArgumentNode`, `CounterArgumentNode`, `ProcedureNode`, `NavigationNode`.
- `node_class_for(bb_type: BBType) -> type[BBNode]` — the subclass for a given type (backed by `_NODE_CLASS_BY_BB_TYPE`).

### Edge dataclass

- `BBEdge` — `@dataclass(frozen=True)`: `source_note_id: str`, `target_note_id: str`, `edge_type: EpistemicEdgeType | None`, `provenance: str`. `edge_type=None` ⇒ untyped (instantiates no schema edge). `provenance` ∈ `"body_link"`, `"folgezettel_parent"`, `"schema"` (synthetic), `"contradicts"` (reserved for a future DKS writer; not emitted by `from_db`).

### `BBGraph`

Constructors:

- `BBGraph(nodes: Iterable[BBNode], edges: Iterable[BBEdge])` — builds `_nodes_by_id`, `_nodes_by_type`, `_out_edges`, `_in_edges` up front.
- `BBGraph.schema() -> BBGraph` — synthetic graph: 8 nodes (one per type, `note_id = bb.value`) + one `BBEdge` per `BB_SCHEMA` entry (`provenance="schema"`).
- `BBGraph.from_db(db_path: Path | str) -> BBGraph` — load the corpus. Lazily imports `indexer.db.Database`, opens it in a `with` block, reads `all_notes()` / `all_links()`, then closes. Keeps notes whose `building_block` parses as a `BBType`; builds body-link edges (both endpoints BB-typed) and a `folgezettel_parent → folgezettel` edge family. Each edge's `edge_type` is set by `find_edge_type(src.bb_type, tgt.bb_type)`; untyped edges are kept (`edge_type=None`). Self-loops and unresolvable FZ parents are skipped. Requires the DB to exist.

Read API:

| Member | Returns |
|--------|---------|
| `node_count` (property) | `int` |
| `edge_count` (property) | `int` |
| `node(note_id)` | `BBNode \| None` |
| `nodes_of_type(bb_type)` | `tuple[BBNode, ...]` |
| `out_edges(source_note_id)` | `tuple[BBEdge, ...]` |
| `in_edges(target_note_id)` | `tuple[BBEdge, ...]` |
| `edges()` | `tuple[BBEdge, ...]` (insertion order) |
| `__iter__` / `__len__` / `__contains__` | iterate nodes / node count / `note_id in graph` |

Audit helpers:

- `untyped_edges() -> tuple[BBEdge, ...]` — corpus edges with `edge_type is None`.
- `unrealised_schema_edges() -> tuple[EpistemicEdgeType, ...]` — `BB_SCHEMA` edges with zero realised instances. Matches by `(source, target)` BB-pair only, not by label.
- `edges_by_type() -> dict[str, int]` — `label → count`; untyped edges grouped under `"(untyped)"`.

## Public API — `tessellum.bb`

Re-exported from `bb/__init__.py`:

- **Schema:** `BBType`, `VALID_BB_TYPE_VALUES`, `EpistemicEdgeType`, `BB_SCHEMA_EPISTEMIC`, `BB_SCHEMA_NAVIGATION`, `BB_SCHEMA_DKS_EXTENSIONS`, `BB_SCHEMA_USER_EXTENSIONS`, `BB_SCHEMA`, `BB_SCHEMA_AT_VERSION`, `BB_SCHEMA_VERSION`, `SCHEMA_EDIT_KIND`, `SchemaEditEvent`, `fold_schema_events`, `set_user_extensions_from_events`, `schema_event_log`.
- **Lookups:** `find_edge_type`, `edges_from`, `edges_to`, `is_valid_transition`.
- **Corpus:** `BBNode`, `BBEdge`, `BBGraph`, the 8 node subclasses, `node_class_for`.

## CLI — `tessellum bb`

One of Tessellum's 11 CLI commands. Two sub-subcommands. Exit codes: `0` completed (warnings are not failure), `2` invocation error (DB/vault missing, bad `--target-version`).

### `tessellum bb audit`

Builds `BBGraph.from_db` and reports telemetry.

| Flag | Default | Effect |
|------|---------|--------|
| `--db PATH` | `./data/tessellum.db` | Index DB path. Must exist (else exit 2). |
| `--format {human,json}` | `human` | Output format. |
| `--show-untyped` | off | Include the full per-edge untyped list. Human: prints all untyped edges. JSON: retains the verbose `untyped_edges` array (omitted by default). |

Reports: nodes by BB type, edges by schema label, untyped corpus edges (count + BB-pair breakdown), orphan BB nodes (no inbound/outbound edges), unrealised schema edges (0 corpus instances).

### `tessellum bb migrate`

Retroactive `bb_schema_version` classification + passive migration. Walks `*.md` under the vault, parses each note, and defaults absent `bb_schema_version` to `1`.

| Flag | Default | Effect |
|------|---------|--------|
| `--vault PATH` | `./vault` | Vault root to scan. Must be a directory (else exit 2). |
| `--target-version {current,N}` | `current` | `current` = live `BB_SCHEMA_VERSION`; else an integer version. |
| `--apply` | off | Bump `bb_schema_version` in frontmatter on would-pass notes only. Would-fail notes are reported, never auto-rewritten. |
| `--format {human,json}` | `human` | Output format. |

For each note recorded below target, runs `format.validate` and classifies by whether any `TESS-005` ERROR surfaces (would-fail) or not (would-pass). `TESS-005` is WARNING-only today. `--apply` rewrites the `bb_schema_version:` frontmatter line on would-pass notes (idempotent; injects after `building_block:` if absent).
