# Digestion — how a source becomes connected notes

## The idea

Digestion is the procedure that turns a source document into typed atomic notes and
wires them into the graph that already exists. Two things have to happen, and a good
system refuses to do one without the other. The source must be *decomposed* — split
into notes small enough that each makes a single point and carries a single building
block. And each note must be *connected* — bound to the source it came from, placed on
a trail, registered under the entry points that make it findable, and linked to the
neighbours it belongs with. A pile of correct but unconnected notes is not knowledge;
it is a heap. Digestion's job is to prevent the heap.

The deep move is that digestion is planned before it is performed, and gated before it
is committed. A source is first read and turned into a plan — a decomposition on paper,
with its notes, its coverage, and its connections all decided but nothing yet written.
The plan is checked. Only a plan that passes is allowed to spend the execution wave that
actually authors notes. Structure is cheap to reason about; authoring is expensive and
irreversible-ish; deciding the shape first is what keeps digestion honest about both
cost and correctness.

## The four phases

Digestion runs as one pipeline of four phases — `plan → augment → review → execute` —
driven by four skill canonicals, one per phase. The first three are *linear*: each is a
single skill run over one shared plan artifact, and each phase's output threads into the
next, so augment sees the plan and review sees the augmented plan. The fourth, execute,
is the *fan-out*: it runs the parallel wave, one unit of work per planned note. A single
document — the plan — is the spine that runs through all four.

**Plan.** The first phase reads the source and decides the notes. It decomposes the
content into building-block-atomic units — exactly one building block per note — and it
splits anything too large to stay atomic, using explicit density limits (a note that
would exceed roughly four hundred lines, eighteen hundred words, or six code blocks is
split before it is written). It maps every section of the source to a note, so nothing
is dropped and nothing is double-covered. Crucially, it also plans the *connections*:
the cross-references each note will carry and the undigested terms the source leans on
that will need their own notes. The output is one plan document, not a single vault note.

**Augment.** The second phase hardens the draft into a contract. It re-reads the source
— on purpose, to catch over-compression, omission, or a term the plan missed — and it
fills in the parts a first pass leaves thin: a section-coverage map, the split decisions,
per-phase validation gates, a per-note cross-reference contract, and a plan for the
undigested terms. Where the plan phase sketches the connections, augment commits to them
in a form the later phases can check.

**Review.** The third phase is the gate, and it writes nothing. It runs a fixed battery
of checkpoints over the augmented plan and returns a typed verdict — `ready`, or `not
ready` with the specific gaps to fix. The checkpoints are not only about note quality;
they are, pointedly, about connection: that every note names its related notes, that
every note is discoverable under an entry point, that the undigested terms are accounted
for, that coverage has no holes and no overlaps. A verdict of `ready` is granted only
when every checkpoint passes. A rejection stops the pipeline here, before a single note
is authored — because the entire point of a gate is to not spend the execution wave on
an unsound plan.

**Execute.** The fourth phase authors the notes. It fans the reviewed plan out into the
parallel wave — one writer per planned note — and each authored note flows through the
same discipline every Composer write obeys: it is validated against its schema, written
through the one materializer channel, and passed through the close-gate that checks its
format and its grounding before the note is allowed to count. A note that fails its gate
is repaired by the fix loop or left blocked; it is never silently recorded as done.

## How a note joins the graph

Decomposition alone would leave islands. What makes a digested note part of the graph is
that the plan gives every note a typed set of edges, and the authoring honours them. A
note intent carries five kinds of connective tissue, and together they are the difference
between a filed note and a joined one.

**Provenance** binds a note to its source. Every note cites the spans it came from; a
note with no source is not a valid intent at all. This is the edge that points *back* to
where the knowledge originated, and it is what the grounding gate later checks.

**Navigation** registers a note under the entry points that index it. An entry point is a
hub note — a table of contents for a region of the vault — and a digested note declares
which hubs it belongs to, so it is reachable by someone browsing rather than searching.
A note that joins no hub is discoverable only by full-text luck; the review phase treats
that as a defect.

**Relevance links** are the note's outbound see-also edges — the plain `[text](path.md)`
links to the sibling notes it should sit near. These are the horizontal connections that
turn a set of notes into a web of ideas rather than a list.

Those relevance links are no longer left entirely to the writer's judgment. During the
execute phase each note's own thesis becomes a query, and retrieval finds the existing notes
most relevant to it — hybrid search picks seeds, a best-first walk expands their neighborhood
over the link graph — then rebases the hits to real paths relative to the new note and renders
them as a `## References` block the writer starts from. So every note ships with
relevance-ranked outbound edges by default, term notes are given room to meet the trail's
citation floor, and the verify step rejects a note that ends up with no resolvable outbound
reference at all.

**Required inlinks** are the reverse of that: the backlinks that *other* notes must gain
so the connection reads both ways. When a new note belongs next to an existing one, the
existing one is updated to point back, so neither end of the relationship is one-sided.

**Dependencies** place a note on its Folgezettel trail — the hierarchical parent-and-child
structure that records what a note builds on. This is the edge that gives the vault its
sense of sequence: not just that two notes are related, but that one comes after the
other in a line of thought.

Downstream, the indexer projects all of this into a queryable graph. Every `[text](path.md)`
link a note carries becomes a row in the link table, broken targets are flagged rather
than hidden, and the building-block ontology types the edges so retrieval and the
dialectic engine can walk them. The connections the plan decided become the connections
the graph exposes.

## Digestion as a snapshot-pinned transaction

Everything above is the shipped path: a digestion authors notes one at a time, and the
runtime commits by rebuilding the index atomically once the notes are on disk. The
knowledge-transaction track (phases P0–P9, described in [composer.md](composer.md#the-knowledge-transaction))
is the disciplined refinement of that path — it makes a whole multi-note digestion a
single transaction that is visible to readers all at once or not at all.

The two meet at a clean seam. The plan phase can emit a *typed intent graph* — the plan's
notes and all their connective edges as machine-checked data rather than prose — and when
it does, the execute phase derives its wave directly from that graph, one atomic leaf per
planned note. From there the transaction track takes over: the planned writes are staged
into an overlay layered over the live index, so gates read exactly the view the commit
will publish; the exact set of rows that must land — the note, its index projection, its
navigation rows, its backlinks, its trail edges — is derived from typed invariants rather
than guessed; a structural suite proves the capsule is safe to write and a calibrated
certificate (or a human sign-off) clears its semantics; and publication swaps one pointer
so the new generation appears atomically. The planner loop closes the review-and-repair
cycle that runs underneath all of this: it counts the plan's remaining deficits — open
ghosts, broken links, undigested terms, coverage gaps, exactly the signals the review
phase surfaces — and drives that count down to zero or halts, so re-planning provably
terminates.

One honest scope note. The transaction track is built, verified, and additive; it is not
yet the live commit path the automatic runtime uses. Today a runtime-driven digestion
still publishes through the per-note authoring path and the commit-tail's atomic index
rebuild. The transaction track's versioned publication is the same fail-closed, atomic
idea one layer up, waiting to be wired in as the accept point (the deferred A1.4 step);
until then it runs opt-in, and every path it adds is byte-identical when its flags are off.

## Corpus digestion — many documents, one coordinated pass

A single digestion takes one source. But a set of related documents — a whole wiki, the
chapters of a book, a design doc and its appendices — should be digested *together*, so
their notes share entry points, cross-link cleanly, and don't each independently coin a
duplicate of the same term. Corpus digestion is that coordinated pass. It is an additive
entry point built on everything above, and the single-source path stays exactly as it was.

**One joint plan, not N independent jobs.** The members of a source bundle are fanned *in*
to a single planning prompt rather than handed to the planner one file at a time, so the
plan is made with the whole corpus in view. From the corpus's total volume the planner
picks a shape: a small corpus stays one plan, a medium one runs in phases, and a large one
is decomposed into a master index plus several self-contained sub-plans. The threshold is
measured, not guessed, and the stronger of two axes — total words or expected note count —
decides.

**A hierarchy of sub-plans, each its own transaction.** A decomposed corpus becomes a
typed corpus plan: a master index — purely derived, never a second copy of the note tables
— over a set of sub-objectives. Each sub-objective owns a slice of the bundle, a priority,
and its dependencies on sibling sub-plans. Every sub-objective is then planned on its own,
through the same plan → augment → review → sign-off flow over just its slice, and every
accepted sub-plan is executed as its own snapshot-pinned transaction. A sub-plan that fails
review or execution is blocked on its own; the rest still promote.

**Dependencies decide the order; the whole is gated as one.** Sub-plans run in dependency
layers: a foundational sub-plan commits before the one whose cross-links point at it, so a
later sub-plan resolves its links against already-published notes, and independent sub-plans
in the same layer may run concurrently. Three corpus-wide checks hold the set together. A
term-ownership gate requires every term the corpus introduces to have exactly one owning
sub-plan, or the whole corpus is blocked before any planning cost is spent. A shared
cross-reference is resolved once at corpus scope — deduplicated, and dropped if its target
does not exist — rather than re-derived in every sub-plan. And a write-closure disjointness
gate refuses to let two sub-plans write the same note, so neither a race nor a
last-writer-wins clobber can corrupt shared knowledge. Above all of it, one whole-corpus
human gate can require sign-off on the total blast radius before anything is published.

## Operating a digestion

Two front doors run the same pipeline. A human runs `tessellum composer digest --source
<json>` to digest one source through `plan → augment → review → execute` directly. The
automatic runtime runs it continuously: it admits a source file from one of eight inbox
lanes, spools its bytes under a content address, leases the job to a worker, invokes the
native digestion driver, and — only after the notes are authored — performs the atomic
P-to-D index rebuild under a live-vault lock, so a reader never sees a half-written
digestion. The runtime's queue is operational state, never knowledge; losing it can lose
pending work, never the meaning of a committed note. See [runtime.md](runtime.md) for the
control plane and [architecture.md](architecture.md) for where digestion sits in the whole
system.

## What holds it together

- **No note without a source.** Provenance is required at plan time and checked at the
  grounding gate. An ungrounded note cannot be planned, and a note whose grounding cannot
  be verified fails closed rather than passing on plausibility.
- **No islands.** Every note declares its entry points, its neighbours, its backlinks,
  and its trail position; the review phase treats a note that joins nothing as a defect.
  Connection is a first-class plan obligation, not a later cleanup.
- **Plan, then author.** The decomposition and its connections are decided and gated
  before the execution wave spends anything. A rejected plan never reaches execute.
- **The vault is the source of truth.** Digestion writes markdown; the index is a pure
  re-projection of that markdown. Connections live in the notes; the graph merely exposes
  them.

**See also:** [composer.md](composer.md) (the pipeline runtime and the P0–P9 transaction
track), [bb.md](bb.md) (the building-block ontology and typed edges), [indexer.md](indexer.md)
(how links become a queryable graph), [runtime.md](runtime.md) (running digestion
continuously), and [architecture.md](architecture.md) (the whole-system map).
