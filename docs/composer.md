# Composer

## The idea

Composer turns a written procedure into a running one. A skill in Tessellum is a
single self-contained markdown note — a standard operating procedure a human could
read and follow. Each pipeline step is a section of that note: a typed contract
block declaring the step's machine-readable facts, followed by the prompt prose the
model actually runs. Composer compiles that one document into a typed dependency
graph of LLM calls it can then execute against a batch of inputs, writing each
result into the vault. It is the bridge between capture (System P, the markdown
substrate) and retrieval (System D): everything Composer does ends in a note on
disk.

The deep move is a separation of *deciding* from *running*. Compilation is a pure
program — it never calls a model. It reads each step's contract block, checks every
contract, sorts the steps, and estimates the prompt budget, and if anything is wrong
it fails the build. Only after the shape is proven correct does any token get spent.
Structure is cheap and deterministic; inference is expensive and uncertain; keeping
them apart is what makes the whole system testable in CI and honest about cost.

## The model

```
skill_*.md (one self-contained canonical:
            per-step section = contract block + prompt prose)
        │
        │  load  →  Pipeline (validated in 2 stages)
        ▼
   compile_skill   (ZERO LLM)
        │  · resolve + check materializer contracts
        │  · topo-sort by dependencies; reject cycles + forward refs
        │  · pull each step's prompt text out of the canonical
        │  · estimate the context budget (warn, or fail over the hard cap)
        ▼
   CompiledPipeline (steps in dependency order)
        │
        ├── run_pipeline           (serial reference — the default)
        └── run_pipeline_dynamic   (opt-in parallelism, gates, resume, budgets)
                │
                │  for each (step, leaf):
                ▼
   resolve the prompt  →  call the backend (under a watchdog)  →  validate  →  materialize
        │
        ▼   (dynamic path only)
   close-gate → fix loop → wave-gate → save manifest → statistics / trace
```

One file describes one skill. The canonical is the single source of truth, the
procedure a person reads. Each pipeline step is an H2 section marked by an anchor
comment; directly under the heading sits a fenced contract block that carries the
machine-readable facts — the step's role, the inputs it consumes, what it
materializes, what it depends on, the schema of its output — and after the block
comes the prompt prose the step runs.
The contract and the prompt live in the same section, joined by construction rather
than by a cross-file pointer, so they can never drift apart. Sections without a
contract block (setup, resources, the skill description) are prose, not steps. The
prose stays readable; the declarations stay checkable.

From there the pieces have clean roles. The compiler produces a typed object. The
scheduler drives that object. The executor is the single unit of work the scheduler
repeats — one step against one input. Model-authored step output reaches the
filesystem only through the materializer; the explicit close-gate fixer may later
rewrite that same note in place. Keeping ordinary publication behind one channel
makes paths, contracts, and effects auditable by construction.

The unit the pipeline runs against is a *leaf* — one input item, such as one
section of a document to digest. A step is either per-leaf (it runs once per leaf)
or corpus-wide (it runs once over the whole set). Steps chain: a downstream step
reads the accumulated outputs of the steps it depends on. This accumulated context
is the spine of the whole run, and preserving its exact shape is what lets the fast
path stay faithful to the slow one.

## How a run flows

**Compile.** Loading reads every step section's contract block from the canonical
in document order and validates each in two passes — its JSON shape, then its typed
model — returning a `Pipeline`, or nothing at all when the canonical has no step
sections and so declares no pipeline. Because each step's section id comes straight
from its anchor rather than a separate file, a step can never name a section that
does not exist. The compiler then walks each step and enforces its contracts. A step names a
materializer; that name must be known, and the step's declared output must promise
at least the fields that materializer requires. An input-closure audit, held to
zero findings in CI, checks each prompt's placeholders against the step's declared
inputs — every hole declared, every declaration referenced. It sorts the steps by
their dependencies, rejecting cycles and — pointedly — forward references, since a
dependency naming a step that appears later is almost always author confusion. It
pulls each step's prompt text out of the canonical by section id. Finally it
estimates how large each step's rendered prompt will grow once upstream outputs are
folded in, warning past a fraction of the cap and failing outright above it. The
result is a `CompiledPipeline` whose steps are already in the order they must run.

**Run, the reference way.** `run_pipeline` is the serial default. It walks the
steps in order, runs each one leaf by leaf, and accumulates every step's structured
output into a shared context under that step's output key. This path is the anchor
of correctness — the exact bytes it produces are the definition of a right answer,
and every faster or fancier feature is measured against it.

**Execute one step.** Whichever path is driving, the atom of work is the same:
resolve the step's prompt template — substituting in the current leaf's fields, the
relevant upstream outputs, any retry context, and by-reference artifacts, the large
durable payloads the driver injects from an integrity-checked store rather than
letting a prior step lossily re-emit them — into a concrete request, refusing the
dispatch outright when a declared-required input is absent; call
the backend under a watchdog; validate the response against the step's schema; and
hand a clean result to the materializer, which writes the note. The watchdog matters
because a model call can hang. It runs the call with a timeout, and on a stall
returns a failed result rather than blocking forever. It does not kill the
background call — Python cannot safely abort a running thread — so the call is left
to finish and its result discarded.

**Run, the dynamic way.** `run_pipeline_dynamic` produces the same output as the
serial path but overlaps the work. Its scheduling core is a pure function: given
which steps are done and which are in flight, it computes the ready set — every
step whose dependencies are all satisfied — and hands back a closed reason for each
one it skips. That core touches no clock, no I/O, no model, so it is fully
reproducible and unit-testable; a thin effectful driver acts on its verdict. Ready
work goes into a shared thread pool, and the driver reacts the instant any step's
whole leaf scope finishes rather than waiting for a whole wave — which kills the
straggler stall where one slow step blocks everything behind it.

The concurrency is made safe by a discipline about the shared context, not by
locks. When a step is promoted to run, its workers are handed a frozen snapshot of
the accumulated context. Workers only ever read their snapshot; the shared context
is mutated on the main thread alone, between promotions, when a finished step
publishes its output. A worker therefore never reads a half-written context, and
because results are ordered by their step and leaf position rather than by when they
happen to finish, the downstream context is byte-identical to the serial order no
matter how the threads interleave.

## Resilience: retries, outcomes, resume

A single step failing is normal; the executor distinguishes *why*. It keeps a
separate retry budget per failure class — logic failures (a bad schema, a contract
miss), crashes (the backend raised, or the watchdog stalled), truncation (a
truncated result escalates max_tokens on its own budget rather than replaying the
same cap), and empty responses (a transient service window, retried on its own
bounded budget). They are separate on purpose: each class calls for a different
remedy and must not starve the others. On top of that sits a short-circuit — if
the last few attempts all produced the *same* error, retrying clearly will not
help, so it bails before the budget runs out — except for empty responses, whose
identical errors are the transient blip's nature and are exempt. Backoff between
attempts is opt-in, so
the default path stays byte-identical to a world without it — except for
empty-response retries, where waiting is the only correct move and full-jitter
backoff is forced even when backoff is off. Each retry feeds the prior error back
into the prompt, so the model gets a chance to correct rather than blindly repeat.

When the dust settles, a step's result is classified into one closed set of
outcomes — succeeded, retries exhausted, watchdog killed, stuck in a same-error
loop, contract violation, budget exhausted, or wave short-circuited by the
run-level breaker. This discriminated union enforces a
discipline: you can only read a step's produced note when the outcome is *success*;
asking for the artifact of any other outcome is a type error. It becomes structurally
impossible to consume a note that never validated. The ordering of outcomes is
considered too — a contract defect is surfaced ahead of a mere exhausted budget, so
the reported cause is the one a fix loop can actually act on.

Across a whole run, the resume manifest is the crash-safety ledger. Its guiding
principle is that it is never the source of truth — the vault is. The manifest can
always be discarded safely: a missing or invalid entry causes re-execution, never
trust in unproven output. It is written atomically, replacing the old file in one
step and rotating a few backups, and on a bad read it falls back to the newest good
backup or starts empty with a warning rather than trusting garbage.

Resume now skips real work, but only after proving that the prior commit is still
the same computation. Each successful entry records the execution generation,
pipeline and capability identity, a hash of the leaf plus its frozen upstream
inputs, the structured output needed by downstream steps, and every filesystem
artifact's path, size, and SHA-256. On restart, the scheduler verifies all of those
fields and re-hashes every artifact. A verified entry is reconstructed as a normal
successful `StepResult`, including its structured output, so dependent steps receive
the same upstream context without another model call. Any mismatch, missing file, or
old manifest entry simply runs again.

The execute wave's manifest has a linear-phase sibling: the digestion driver
checkpoints the plan-of-record after every phase fold, and an opt-in resume replays
from the latest checkpoint — skipping the already-paid plan and review work — but
only after proving source identity: the checkpoint's code-measured ledger must
equal one recomputed from the claimed source, and every code-owned field is
re-stamped, so a checkpoint never overrides what code measures.

Two fences keep this safe under concurrency. Claiming a leaf is a compare-and-swap
that only one worker can win, and a successful commit must still match the claim's
owner and generation. A reclaimed or stale worker therefore cannot mark its output
done after a newer worker has taken ownership. The dynamic scheduler also accepts a
cooperative cancellation check and evaluates it before each leaf dispatch; the
executor checks again before materialization, and the digestion driver checks the
same signal between phases. Callers may also supply an effect guard around
materializer writes, fix-loop restoration, and manifest saves. An arbitrary
user-supplied fixer is responsible for its own fencing; the automatic runtime
constructs its LLM fixer with the job's lease guard. Diagnostic trace, event,
statistics, source-leaf, and plan files are run artifacts rather than vault effects
and are not lease-fenced by Composer.

## Gates: the note only counts when it passes

A gate is a named, scoped, pure-program check — never an LLM call. There is exactly
one gate abstraction, reused at the plan, session, and wave scopes; there is no
second mechanism. The close-gate runs after a note is captured and is ordered
cheapest-first: a format check (delegated to Tessellum's own note validator, not
reimplemented) followed by a grounding check. Grounding is the one semantic concern,
but even it stays a program — it *reads* a typed verdict produced independently by
a verifier and decides. The default verifier is itself deterministic and free:
every code-like identifier a note asserts must literally appear in the source, so
an invented API surface self-announces on a string check; a calibrated
model-backed scorer is the opt-in deeper tier. A grounded verdict may still carry
a non-blocking advisory — an identifier real in the source but foreign to the
note's owned slice — recorded without blocking. A missing or auth-blocked verdict
fails closed. The gate never guesses at plausibility, so a fabricated citation
cannot slip through by looking convincing.

The ordering of gate and commit is the load-bearing rule. The note file is written
during capture, but the leaf is only marked done — and the result only treated as
clean — *after* the gate passes. A gate failure turns an otherwise-clean capture
into an errored, blocked result. A note that failed its gate is never silently
recorded as done. The wave-gate makes the checks a per-session gate structurally
cannot: two leaves resolving to the same target path; a cross-note link that stays
unresolved once every sibling in the wave has landed — a check no single note's
close can time right; and whether each written note actually leaves a trace of
every source section it owns. The latter two land as advisory warnings recorded in
the run events — the composite verdict is evaluated in full, not fail-fast — with
a calibrated strict mode as the promotion path. When a
wave gate is active, manifest success commits are deferred until that gate accepts
the whole wave; rejected leaves return to claimable work. Standalone Composer may
leave an inspected but rejected note on disk. The automatic runtime adds a durable
per-job effect journal and restores every touched vault path when digestion is
rejected, cancelled, or killed before acceptance.

When the close-gate fails, the fix loop repairs the note without ever making it
worse. It scores the note by its count of blocking issues — fewer is better — and
before each attempt it checkpoints the current bytes and score, keeping the best it
has seen. Each round builds an informed context: the current issues plus what prior
attempts already tried, so the fixer does not repeat a failed strategy. If a later
round regresses the note below the best snapshot, the loop restores the best bytes.
A fixer that crashes simply wastes a round; it never raises. The loop owns all the
safety, so a fixer only has to *attempt* an improvement.

## Spending less: planning, budgets, sign-off

Two planning checks decide what not to do, and both only advise the driver rather
than dispatch work themselves. Change detection runs before the scheduler, at the
point leaves are admitted, so it never disturbs the mid-run context accumulation.
It fingerprints each leaf's content and skips only leaves that exactly match a
recorded fingerprint — new, changed, or unkeyed leaves always run, failing open
toward doing the work. Depth classification routes each leaf to a fast or full plan
from cheap signals, defaulting to full when unsure, because a mis-planned novel leaf
costs more than an over-planned trivial one.

The budget is the runaway-fan-out breaker a static compile check cannot provide.
Immediately before every backend call, including retry and informed-fixer calls,
the executor charges one unit against the shared run budget atomically and
all-or-nothing. A refused call halts the leaf with a budget-exhausted outcome
without dispatching. Beside the token budget sits an error-class circuit breaker:
once a proportional share of dispatched leaves fail on the same systemic wall (an
expired credential pool, a marketplace-wide rate limit), the wave short-circuits —
remaining leaves get a distinct breaker-tripped outcome and are marked blocked,
never retried into the same wall. Credentials are pooled alongside: the pool
leases the least-used key per call, and when a call fails it classifies the cause. A hard
rate-limit, quota, or auth failure benches that key for an absolute cooldown
that survives a restart and releases the lease so the next attempt draws a
different key; a transient blip keeps the lease. Crucially the pool holds key
*ids*, never secrets — the caller maps id to secret out of band, so this layer
never touches a credential.

Sign-off is the approval ladder from plan to execute, climbed cheapest-first. A
program gate is a pure structural pre-filter that can reject outright — and on the
digestion path it now includes a deterministic note-atomicity gate that fails a plan
on objective signals a program can measure (a note over the density ceiling, a plan
shredded into more notes than the measured source supports, a multi-block building
block, a source section left out of coverage, a mandatory plan section missing,
reported per section), plus an advisory balance check that flags a note whose owned
source span far exceeds the density ceiling, and loops a failing plan back to
re-planning, so the split-the-notes rules are enforced by code rather than left to
the planner's goodwill. An agent
judge returns an approve-or-reject with a confidence; and a human seam is reached
*only* when agent confidence is low or the blast radius is high. The rung callables
are injected — this module owns the ladder's logic, not the model or the UI behind
any rung — and when the human rung is required but disabled it returns a
needs-human signal for an out-of-band decision.

## Backends and skills-as-tools

Every model call goes through one backend protocol — a single `call` method from a
request to a response — so the rest of Composer is indifferent to the provider. A
mock backend serves canned responses with no network for tests and is the only
backend registered by default. Real backends reach Anthropic's API directly or
through Bedrock on the ambient AWS credential chain, and a pooled backend wraps any
inner backend with the credential pool and its rotation logic, re-raising failures
so the executor's retry ladder still owns the retry.

A compiled skill can also be projected into a tool. This view exposes a skill's
input and output schemas, side effects, gates, and routing key as a read-only
capability — and it delegates all compilation back to the one compiler, so it is a
view, never a second implementation. A capability registry routes in two tiers: a
deterministic table resolves a unique match directly, and zero or many matches hand
the open-set semantic choice back to the caller with the candidate list. The
registry itself never calls a model. Around the edges, a batch runner fans many
skill-and-leaves jobs across the *serial* path with coarse per-job resume, and an
eval framework scores runs with structural assertions plus an LLM-judged rubric.

## The knowledge transaction

The pipeline so far writes one note at a time. A multi-document digestion asks for
more: many notes, cross-linked, that must appear together or not at all, planned
against a base that may move under them. The knowledge-transaction track answers
that. It turns a whole digestion into a single snapshot-pinned transaction — plan
the edits as typed data, stage them off to the side, prove them safe, then make them
visible to readers in one atomic step. It is built in additive phases, each byte-
identical when its opt-in path is off, so nothing above changes until you ask for it.

The seam to the digestion pipeline is the plan itself. The `plan → augment → review →
execute` driver's plan phase can emit a typed intent graph — its notes and all their
connective edges as machine-checked data rather than prose — and when it does, the
execute wave is derived straight from that graph, one building-block-atomic leaf per
planned note. So the transaction is not a separate mechanism bolted on beside
digestion; it is what a digestion *is* once its plan is typed. See
[digestion.md](digestion.md) for that end-to-end flow.

**Typed intent, staged off to the side.** A transaction begins as typed proposals,
never free text — add, update, merge, drop, reroute — each naming the notes it
touches and carrying content-addressed hashes so two plans can be compared and merged
by value. Those proposals compose into a plan: a graph of note intents, each tagged
with its one building block, its cited source spans, the entry points it joins, and
the backlinks it owes. The plan is staged into an overlay that layers the pending
changes over the live index without mutating it — an update shadows the base row, a
delete tombstones it, a re-authored note declares its own edges — so every gate and
dedup query reads exactly the view the promotion will publish, before anything is
committed.

**The exact write set.** A transaction commits an exact set of rows, and the system
refuses to guess at it. From the typed invariants alone — the note, its index
projection, its navigation row under each entry point, the backlinks other notes must
gain, the reciprocal rows its Folgezettel dependencies must gain — it derives the
precise closure of what must land. The derivation reads the intents and nothing about
graph shape, so it cannot look at how central a target is and cannot prune a mandatory
row under a busy hub. A separate boundary proof then checks that no edge carrying a
write escapes that set, and an edge whose class cannot be determined fails the proof
rather than being waved through. A second, clearly separated question — which existing
notes might now be stale and want re-checking — is answered by a short bounded walk
that may only *widen* what gets re-verified, never change what commits; when its fan-
out exceeds a calibrated bound it says so and hands back the whole set rather than
quietly trimming it.

**Reader-visible publication.** Publication is the one point where in-flight work
becomes visible, and it is built so a reader sees a whole generation or nothing.
Each generation is an immutable directory of notes plus index; a reader pins one
pointer file once and reads only from the generation it names. The commit runs in
three phases — write the generation into a private staging area and flush it, still
invisible; then under an exclusive lock re-check that the pinned base is still live,
promote the directory, record a durable commit marker, and swap the pointer; then
acknowledge, idempotently. The compare and the swap happen under the same held lock,
so the check is a real atomic test-and-set: two publishers that planned against the
same base cannot both win, and a snapshot's recorded read-set is re-validated at the
last moment so a file that changed underneath aborts the publish instead of losing an
update. Recovery treats the pointer swap as the sole authority on what committed — it
completes an unacknowledged live generation, reclaims staged or promoted directories
that never reached the marker, and never touches a committed or current one.

**Structural admission, human-supervised.** Before a capsule may publish, a battery
of pure-program checks proves it is safe to *write*: every note cites a source span,
every claim names its provenance, each note carries exactly one building block, each
declared entry point is actually a write in the capsule so the note is reachable, each
owed backlink is real, and the merged index gains no dangling reference. These are
decidable without a model, which is exactly why they can fail closed — a check that
cannot prove pass is a fail. But structural safety is a ceiling, not a warrant: a
program can confirm a claim *has* provenance, never that the claim is *entailed* by
it. So admission stays supervised. A capsule publishes only when the structural suite
passes and a signed approval bound to that exact capsule is present; a structural
failure blocks outright and never reaches the human step, and a clean-but-unapproved
capsule is held. Because the approval binds to a content-derived identity, changing
the plan voids the old sign-off — it cannot be lifted onto a mutated capsule.

**The calibrated semantic certificate.** The certificate is the measured path that
lets a capsule promote without the human artifact, and it keeps Composer's boundary
intact: an injected model produces evidence, a frozen program decides. Each claim is
scored against its cited span by a pluggable entailment scorer — the real model is a
dependency, never bundled here — and the note is only as grounded as its weakest
claim, since the scores are aggregated by minimum, not averaged. A mean would let a
pile of easy claims mask one fabrication, which is the failure the gate exists to
catch. Thresholds are set per failure class from labelled examples: the widest accept
region whose observed false-accept rate sits at or under the target, class by class,
with an unreachable cutoff for any class that cannot meet the bound so it always
abstains. The gate fails closed everywhere uncertainty enters — an empty claim set, a
note outside the calibrated domain, a claim the scorer could not judge — routing those
to a human. One honest limit bounds the promise: this is an empirical, in-sample
calibration, not yet a distribution-free guarantee. The certificate now runs end to end —
a reference scorer, note-to-claim extraction, the runtime seam, and an A7.5 go/no-go gate
all ship — and a first calibration ships with it: the reference scorer was calibrated
on a labelled pilot corpus (threshold fixed per failure class, the faithful set
accepting and a set carrying one fabrication abstaining, live), the artifact is
committed, and the runtime can load it to back the note-level grounding gate — over
the full source span, since a pilot of the owned-slice variant was refuted by
measurement. Thresholds are scorer-specific by construction. Capsule promotion
without the human artifact still awaits a GO on a production-scale corpus of
wrong-but-well-formed notes; until then promotion stays
supervised. See [semantic-certificate.md](semantic-certificate.md) for the full mechanism.

**Bounded planning that always halts.** When a planner re-plans from review evidence,
the loop makes a deliberately modest promise: it always halts, in bounded time, at one
of two terminal states — the obligations are discharged, or the loop is blocked. It
does not promise the planner will succeed. The distinction is principled, since
digesting one note can surface new terms to digest, so a general planner is not a
shrinking process over a fixed set and a blanket convergence claim would be false. Within
a frozen episode, progress is measured by a plain non-negative integer count of open
ghosts, broken links, undigested terms, and coverage gaps — never a model's opinion —
and a revision is accepted only if that count strictly drops. A count that cannot
descend forever is what makes the frozen loop provably finite, and zero is recognized
as success before any blocking rule is even considered. Three hard stops cover the
open-universe case where no such monotonicity holds: a ceiling on accepted revisions,
a budget on planner calls, and oscillation detection that trips when the planner keeps
returning to the same shape without progress. Every exit writes a terminal result, so
the loop cannot livelock.

**One transaction, end to end.** The effect classes are now complete — create,
update, merge, drop, skip — each governed by a preimage rule: a create forbids a prior
image because its target must not exist, while update, merge, and drop require the
pinned pre-image the promotion re-checks. What ties the phases together is an
acceptance matrix that wires them for real rather than mocking the seam between them:
a source bundle becomes an intent graph, projects to a deterministic write closure
with its boundary proof, stages into the overlay, clears the structural suite and
human approval, earns a semantic certificate inside the calibrated domain, and
publishes through the snapshot CAS — with crash recovery and byte-identical replay
proven on the same path, and a stale-base capsule refused at the commit point. After
the structural phase the system is a safe, human-supervised, frozen-epoch constructor;
after the certificate it can run unattended inside a measured domain, once that domain
is actually measured.

One scope note keeps the picture honest. This track is built, verified, and additive,
but it is not yet the live commit path the automatic runtime uses. Today a runtime-driven
digestion still publishes note by note and rebuilds the index atomically in the commit
tail; the versioned publication here is the same fail-closed, atomic idea one layer up,
waiting to be wired in as the accept point. That final wiring is the one deferred step,
so for now the whole track runs opt-in and stays byte-identical when its flags are off.

## Invariants worth remembering

The invariants below are the ones that give Composer its character; the reference
records the rest.

- **Compile spends zero tokens.** Every structural decision is program logic, so a
  contract drift fails a build instead of costing money, and the whole compile step
  runs in CI.
- **The dynamic path is entirely opt-in; the serial path is the definition of
  correct.** Manifest, gates, budget, fixer, context strategy all default to off,
  and parity with the serial output is the acceptance test for every one of them.
  A new capability must never silently change existing output.
- **Model-authored step output uses one write channel.** Contracts default to
  demanding a tool-free backend so a model cannot smuggle out an undocumented
  write. Agent paths must be relative and resolve beneath `vault_root`, and
  multi-edit payloads preflight every path before writing the first file. The
  explicit fixer can only repair the note path already selected by materialization.
- **Gates are pure programs and fail closed.** The agent gathers evidence; the
  program decides. An unverifiable source is a failure, never a pass, so fabrication
  cannot pass as plausible.
- **The vault is the source of truth, not the manifest.** A lost or half-written
  ledger falls back to a good backup or causes safe re-execution. Resume only trusts
  entries whose computation identity and artifact hashes still verify.
- **Composer writes; it does not rank.** Ranking notes is retrieval's job in a
  separate subsystem. Composer's output is always a note on disk.
- **A knowledge transaction is atomic and fail-closed.** Its write set is derived
  from typed invariants, never guessed from graph shape; it becomes visible in one
  pointer swap or not at all; and every gate between plan and publish — structural
  checks, the boundary proof, the semantic certificate — treats an unprovable pass
  as a failure. Unattended promotion is earned by measurement, not assumed.

**Reference:** [reference/composer.md](reference/composer.md) — API, symbols, and signatures.
