# DKS — Dialectic Knowledge System runtime

## The mental model

Most knowledge systems store what you believe. DKS stores *how a belief survived being attacked*. It takes an observation, argues it from two or more perspectives, lets those arguments contradict each other, names exactly which part of the losing argument broke, generalizes the failure into a pattern, and rewrites the rule that failed. The rewritten rule feeds the next observation. That loop is the whole idea: a knowledge base that learns by disagreeing with itself, and records the disagreement as structure rather than throwing it away.

The unit of reasoning is a **warrant** — Toulmin's term for the standing rule that licenses the jump from data to claim. A warrant is the thing DKS revises. Every cycle is an attempt to find a warrant that was wrong and produce a better one, and every piece of that attempt — the observation, the arguments, the counter, the pattern, the revision — is deposited as a typed node on the same Folgezettel graph the rest of Tessellum writes to. DKS does not live beside the knowledge; it *is* knowledge construction, run as a protocol.

DKS is a peer of Composer, retrieval, and the indexer, not a feature inside any of them. It borrows exactly one thing from Composer: the `LLMBackend` abstraction that lets a cycle talk to a model without caring which model. Everything else — the argumentation, the graph allocation, the persistence — is its own.

## The model: how the pieces relate

One cycle is a fixed seven-component pipeline. Read top to bottom; each arrow is a step, and the right column is where the produced node lands on the trail.

```
observation                    (step 1, cycle root FZ)
   -> argument A               (step 2, FZ N.a)          perspective[0]
   -> argument B               (step 3, FZ N.b)          perspective[1]
   -> contradicts edge         (step 4, no FZ — a link, not a node)
   -> counter-argument         (step 5, FZ <attacked>.a) names broken Toulmin component
   -> pattern / model          (step 6, FZ <counter>.a)
   -> revised warrant(s)       (step 7, FZ <pattern>.a leaf)  -> procedure/concept note
```

Six of the seven components become nodes; the seventh, the contradicts edge, is deliberately *not* a node. It is a relation between two arguments — a disagreement is something that holds between claims, not a thing that exists on its own — so it gets a link and no Folgezettel ID. This is the first design commitment of the system: the graph distinguishes what is asserted (nodes) from what is contested (edges).

The steps also map onto Tessellum's typed Building-Block ontology. The observation is an empirical-observation node, each argument is an argument node, the counter is a counter-argument node, the pattern is a model node, and the revision becomes a procedure or concept note. The cycle is, in other words, a walk across the epistemic edges the schema already declares — a fact the system exploits twice over, once in the FSM view and once in meta-DKS.

Warrants thread *between* cycles, not just within them. A multi-cycle run feeds each cycle the current warrant set — the initial warrants plus every revision produced so far — and records a chronological diff of what changed. This is how the substrate learns across a session: cycle three argues against the rule cycle one wrote.

The recursion has a second floor. **Meta-DKS** runs the same dialectic shape one level up, over the schema itself. It reads the telemetry from ordinary cycles, notices that one kind of Toulmin failure keeps recurring, proposes a schema edit to name the missing relationship, attacks its own proposal, and lands the survivors as versioned schema events. The system that argues about warrants can, one level up, argue about the rules for arguing.

## The procedure: how work flows through a cycle

A cycle is driven by **the cycle dispatcher** (`DKSCycle.run`), and its first decision is whether to run at all. If a confidence model is wired in and it judges that the existing warrants already cover this observation, **the confidence gate** fires: the cycle produces the observation plus a single argument and stops. This is the cheap path, and it is meant to be common. Most observations are not surprising.

When the gate does not fire, the dispatcher generates argument A from the first perspective and argument B from the second. Then **the disagreement detector** compares their claims. By default this is a local string comparison — no model call — because whether two claims differ is usually obvious from their text. If the arguments agree, the cycle short-circuits: two arguments, no contradiction, no revision. Agreement is not failure; it means the warrants held, and there is nothing to repair.

If the arguments disagree, the loop closes. **The counter-argument step** asks the model which single Toulmin component of the losing argument broke — was the premise unsupported, the warrant wrong, was there a counter-example the warrant didn't anticipate, or did the qualifier not apply. Naming exactly one component is the point: it classifies the failure and constrains what kind of repair is legitimate. **The pattern step** then generalizes that single contradiction into a structural regularity — a model node describing the shape of the failure, not just the instance. Finally **the rule-revision step** authors a new warrant designed to prevent the same contradiction next time, deposited as the leaf of the cycle's subtree. That is a closed loop.

Multi-cycle runs wrap this in **the runner** (`DKSRunner`), which threads warrants forward and emits the change diff. Each revision is classified: a wholly new warrant is *added*; a warrant that supersedes a prior one is *revised*, paired with a *superseded* tombstone recording the displaced FZ. The runner never mutates the vault. Like the rest of DKS, it produces records; writing warrant *files* is a separate, downstream job.

### More than two perspectives

The two-perspective cycle is the default, but the argument step is not limited to two. Pass three or more perspectives and the disagreement step stops being a single edge and becomes a *graph*: a contradicts edge for every pair of arguments whose claims differ. Deciding which arguments survive that tangle of mutual attacks is no longer obvious, and this is where **the argumentation solver** enters.

The solver is Dung's abstract argumentation framework, the 1995 result that answers exactly this question — given a set of arguments and an attack relation, which arguments are acceptable? DKS uses its *grounded* semantics, the minimal, unique, always-defined answer: an argument is labelled `in` if all its attackers are `out`, `out` if any attacker is `in`, and `undec` if it sits in an unresolved mutual attack. The surviving warrants are the arguments labelled `in`. For two perspectives this collapses to the single-edge outcome, so the solver is purely *additive* — it generalizes the default rather than replacing it.

When grounded labelling leaves more than one survivor, the cycle writes one revision per survivor, each anchored under its own surviving argument rather than under the shared pattern. Distinct surviving warrants deserve distinct revisions.

### Telemetry the cycle cannot hide

Several points in the cycle call a model in a way that can fail — the optional semantic-disagreement check, the retrieval-context lookup, and the JSON parse of any step's response (argument, counter, pattern, and rule-revision all parse and can swallow). Each falls back gracefully rather than crash, which is correct for robustness but dangerous for honesty: a backend that silently fails every other call would quietly skew the whole Toulmin distribution. So each fallback records a one-line note of what it swallowed *before* falling back. The semantics are unchanged; the silence is now countable. Meta-DKS reads that count and discounts degraded runs.

## The procedure: how meta-DKS mutates the schema

Meta-DKS is the same four-move dialectic — build, filter, survive, emit — applied to the schema. It begins by assembling a **meta-observation** from the ordinary cycle traces: which warrants get attacked most, how the Toulmin failures distribute, which declared schema edges have never been realized in the corpus. That observation is the empirical anchor, exactly as a raw observation anchors an ordinary cycle.

A **proposer** turns the observation into schema-edit proposals. The default is a small heuristic: when one Toulmin failure mode dominates, propose the typed edge that would let the schema name it; when a declared edge has stayed unused long enough, propose retracting it. The alternative is an LLM proposer that reasons over the full observation — strength breakdowns, sample quotes, source metadata — and reports its own input-bias risk, so a proposal driven by skewed input can be recognized as such. An **attacker** then challenges the proposals. The default attacker is a no-op, so every well-formed proposal survives; the LLM attacker runs a real dialectical attack, naming a weakness from a closed vocabulary, and a survival threshold — strict, majority, or permissive — decides who lives.

Two guards make this safe. First, a cold-start guard: meta-DKS emits nothing until enough cycles have accumulated, because a failure distribution over a handful of cycles means nothing. Second, and more important, meta-DKS defaults to dry-run. It proposes; it does not write. Only an explicit apply turns surviving proposals into schema events on disk.

## Design decisions and why

**Three terminal shapes, told apart by one field.** A cycle ends full (all seven components), short-circuited (arguments agreed), or gated (confidence skipped the comparison). These are genuinely different — the gated path saves six of seven model round-trips — so the difference has to be first-class and observable, not inferred. The discriminator is deliberately simple: a cycle is gated exactly when its second argument is absent. Cheap-versus-rich is a property you can read off the result, not reconstruct.

**The gate is opt-in and biased toward caution.** No confidence model means every cycle runs full; the safe default is to do the work. When a model is present, gating fires only when confidence is *strictly greater* than the threshold — equality falls through to the full cycle. The bias is intentional: it is cheaper to run a full cycle you didn't need than to skip one you did. And because every gating decision is recorded with its score, the threshold itself becomes tunable from data rather than guessed.

**Grounded semantics because survival must be principled.** With many mutual attacks there are many ways to pick winners, and most are arbitrary or order-dependent. The grounded extension is none of those things: it is the minimal complete extension, unique, and always defined. When the substrate has to decide which warrants carry forward, it needs an answer that is not a matter of taste. `undec` counts as not surviving — an argument stuck in an unresolved cycle has not earned the right to revise anything.

**Retrieval is read-only, and one-directional by rule.** DKS may read the index to ground its arguments in existing material, but it can never write back through that path — there is no index, update, or delete on the retrieval client, and the underlying module exposes none. This is the R-Cross discipline: the productive system calls the descriptive system; the descriptive system never calls back. Retrieval is also optional and lazily imported, so the core cycle runs without it, and when it is present its hits only *augment* the argument prompt. They never replace a warrant. Evidence informs the argument; it does not become the rule.

**The meta-schema is hand-authored and PR-gated — the tower stops here.** Ordinary cycles edit warrants. Meta-DKS edits the Building-Block schema, and those edits are versioned and event-sourced. But the meta-schema that meta-DKS itself walks is *not* event-sourced; it is a small fixed schema changed only by human code review. The reason is blunt: the recursion has to stop somewhere, or there is an infinite tower of meta-meta-schemas. One level of self-editing is the architectural limit. And a schema edit never retroactively invalidates existing notes — every note is frozen at its creation version, so growing the schema cannot break the past.

**The default path never changes shape.** Every capability added over the life of this module — N-perspective debate, the Dung solver, multi-revision authoring, retrieval grounding, the FSM view — is additive. The two-perspective cycle still runs its original hand-coded steps and produces its original result. The FSM (`DKSStateMachine`) re-expresses a cycle as a typed walk over the schema for callers who want handler injection or want to extend the walk, but it delegates to the same dispatcher and changes nothing about it. New power is offered; the tested default is preserved.

**Persistence is out-of-band, and gates never call a model.** DKS classes emit JSON-line records; the CLI writes them to `runs/dks/`. Neither the warrant registry nor the history ever touches the vault substrate — the warrant *files* are materialized separately, by the DKS Composer skill. The split keeps the runtime pure: a cycle computes and records, and the decision to persist is someone else's. Likewise the gates, filters, and survival thresholds are all deterministic code. The model is asked to reason inside a step; it is never asked to decide whether a step should run. Control flow stays in code, where it can be tested.

**Reference:** [reference/dks.md](reference/dks.md) — API, symbols, and signatures.
