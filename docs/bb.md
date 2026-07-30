# Building Block Ontology — `tessellum.bb`

## The mental model

Every note in Tessellum carries a type — one of eight Building Blocks. This module answers a single question about those types: given a note of type A that links to a note of type B, is that a *legal* move in Tessellum's grammar of thought? A concept can be structured into a model; a hypothesis can be tested into an argument; an argument can be challenged by a counter-argument. Those transitions are not decoration. They are the finite alphabet of epistemic moves the system knows how to make, and `tessellum.bb` is where that alphabet is written down.

The deep idea is a split between two very different kinds of graph. One is the **schema**: closed, finite, type-level — the roughly sixteen transitions the ontology *permits*. The other is the **corpus**: open, growing, instance-level — the thousands of links the vault *actually contains*. Keeping these apart is what lets the schema act as a type-checker for the corpus. A real link between two typed notes either instantiates one of the permitted transitions, or it does not — and the ones that do not are exactly the signals worth looking at.

## The model

The module is two layers, one per side of that split. `types.py` holds the schema; `graph.py` holds the corpus view. The schema is the source of truth, and the corpus view depends on it — never the reverse.

```
  types.py  (schema — closed, type-level)
    BBType (8 members)  ── the FSM's states
    EpistemicEdgeType   ── one typed transition (source, target, label)
    BB_SCHEMA = epistemic + navigation + DKS-extension + user-extension edges
        │
        │  find_edge_type(source_bb, target_bb)  ── the type-check
        ▼
  graph.py  (corpus — open, instance-level, read-only)
    BBNode, BBEdge (with provenance)
    BBGraph.schema()   ── synthetic graph over the schema
    BBGraph.from_db()  ── loads the real corpus from the index
        │
        ▼
  tessellum bb audit / migrate  ── corpus telemetry + version reconciliation
```

The eight types are the states. Seven of them form a dialectic cycle — observation names a concept, the concept is structured into a model, the model predicts a hypothesis and codifies a procedure, the hypothesis is tested into an argument, the argument is challenged by a counter-argument, and the counter motivates a fresh observation that restarts the loop. The eighth type, Navigation, sits outside the cycle: it is the index node, pointing at each of the other seven without ever being part of the argument.

A **transition** in the schema is a typed edge: a source type, a target type, and a label naming the operation ("naming", "structuring", "testing", and so on). This is a *type*, not an instance. The schema declares each transition once; the corpus can realise it many times. That one-to-many relationship is the whole reason the two layers exist separately.

On the corpus side, a **node** is a real BB-typed note pulled from the index, and an **edge** is a real link between two such notes, stamped with the schema transition it instantiates — or stamped as *untyped* when it matches no permitted transition. Each corpus edge also carries its **provenance**: whether it came from a markdown link in a note's body, or from a Folgezettel parent relationship. The `BBGraph` is the queryable view that holds these together, built either synthetically from the schema (to ask "what is allowed?") or from the live index (to ask "what exists?").

## How work flows through it

The type system starts at capture time, upstream of this module. The set of legal `building_block:` values in a note's YAML is derived directly from the eight-member enum here, so there is exactly one place where the vocabulary of types is defined. Everything downstream inherits it.

The corpus view is assembled on demand by `BBGraph.from_db`. It opens the built index, streams every note whose declared building block parses as a known type, and drops the rest. Then it walks the links twice. First it takes every body link whose two endpoints are both typed notes and turns it into an edge. Then it derives a second family of edges from Folgezettel parentage — where a note names another as its trail parent, that becomes an edge too. Each edge, from either family, is run through the schema's lookup to find the transition it instantiates. Matches get typed; the rest are kept as untyped, deliberately, because the untyped ones are the interesting ones. The graph builds its lookup indexes in memory and closes the database rather than holding the connection open.

From that graph, `tessellum bb audit` produces the vault's structural telemetry. It counts nodes by type and edges by transition label, surfaces the untyped edges (the ones a validator or a schema author should examine), flags orphan nodes with no connections at all, and lists the schema transitions the corpus has never once realised. The last of these matters more than it looks: a schema with a "challenging" edge and zero challenges in the corpus is telling you something about the health of the thinking, not just the data.

The second command, `tessellum bb migrate`, advances recorded schema-version
stamps. Today it is deliberately passive: it walks lagging notes and runs the
current validator, but `TESS-005` is warning-only and validation still uses
each note's recorded schema rather than the target schema. Consequently every
parseable lagging note is currently eligible for `--apply`; this command
should not be read as proof that a note conforms to the target schema.

## Design decisions and why

**The schema is closed; the corpus is view-only.** The schema changes only through deliberate, auditable revision. The corpus layer never writes to the substrate — it reads the index and nothing more. This is the productive discipline at the heart of the design: the runtime may exercise any transition the schema declares, but growing the schema is an act of intent, not a runtime side-effect.

**A corpus edge instantiates exactly one transition, or none.** The lookup matches on the source-and-target pair, which is unique across the schema today, so "the first match" and "the only match" coincide. This is what turns the schema into a type-checker. An untyped edge is never ignored; it is a fork in the road. Either the link is wrong, or the schema is missing a transition that reality has started to demand — and the second case is precisely how the ontology learns it needs to grow.

**Schema growth is event-sourced, and retraction is first-class.** New transitions are not edited into a list. They arrive as events on an append-only log, and the active schema is the *fold* over that log. Events can add, retract, or refine, and a refinement is simply a retract composed with an add. The log is never rewritten. The reason is a sharp distinction: schema *state* must be retractable, but schema *history* must be permanent. When a transition is retracted, the corpus edges that used to instantiate it become untyped — a migration signal — without any loss of the record of why the edge once existed.

**Notes are validated against the schema they were born under.** Because the schema can change, every note freezes its schema version at creation. The module can reconstruct the schema as of any past version by folding the right prefix of the event log, and it memoises that reconstruction. The version bumps once per landed add or retract; a refine does not bump separately, since it is already an add-plus-retract. The payoff is that a later schema edit cannot retroactively invalidate notes written before it. Only the user-extension portion of the schema varies across versions — the core epistemic, navigation, and DKS-extension transitions are constant.

**Shipped code and per-deployment state are kept apart.** The package ships with an empty event log. Real events live outside both the package and the vault, written by the meta-DKS runtime that proposes schema edits. So the same installed code can carry different schemas in different deployments, and the schema a team owns is never entangled with the schema a single vault has grown.

**There is one node subclass per type.** Rather than pass the type as a constructor argument on every call, each type gets its own frozen node class that fixes its own type. The discriminator stays statically checkable and stays out of the constructor. Synthetic schema nodes, which are not real corpus instances, use the bare base node with the type set explicitly.

**Enforcement is deliberately narrow today.** The schema *can* type-check every realised link, and the lookup to do so exists. But the wired validators do not yet use it broadly: one rule enforces a single transition, and the version-checking rule is warning-only. This is worth stating plainly rather than implying the type system is fully enforced — the capability is present; the enforcement is not yet turned all the way up.

## A caveat: two parallel implementations

There are two BB ontologies in the tree, and only the older one is re-exported from the top-level package — `from tessellum import BuildingBlock, BB_SPECS` gives you the legacy module, while the canonical types must be imported explicitly via `from tessellum.bb import BBType, BB_SCHEMA, BBGraph`. (The two modules also both define a class named `BBEdge`; the top-level export is the legacy one.) This module, `tessellum.bb`, is the canonical one — it is what validation and the `tessellum bb` CLI are wired to, and it is what the note format's legal-value set derives from. The older `tessellum.format.building_blocks` defines a separate enum with the same eight string values but a different edge count and a different data model. It survives for one reason: it carries per-type descriptive metadata — each type's guiding question, its epistemic function, its required sections — that the canonical module does not. Treat `tessellum.bb` as authoritative for types and transitions, and reach for the legacy module only when you need that descriptive per-type spec. Consolidating the two remains an open cleanup.

**Reference:** [reference/bb.md](reference/bb.md) — API, symbols, and signatures.
