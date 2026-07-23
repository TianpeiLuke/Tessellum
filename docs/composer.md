# Composer

## The idea

Composer turns a written procedure into a running one. A skill in Tessellum is a
prose document — a standard operating procedure a human could read and follow.
Composer takes that document, plus a small machine-readable sidecar, and compiles
it into a typed dependency graph of LLM calls it can then execute against a batch
of inputs, writing each result into the vault. It is the bridge between capture
(System P, the markdown substrate) and retrieval (System D): everything Composer
does ends in a note on disk.

The deep move is a separation of *deciding* from *running*. Compilation is a pure
program — it never calls a model. It reads the sidecar, checks every contract,
sorts the steps, and estimates the prompt budget, and if anything is wrong it
fails the build. Only after the shape is proven correct does any token get spent.
Structure is cheap and deterministic; inference is expensive and uncertain; keeping
them apart is what makes the whole system testable in CI and honest about cost.

## The model

```
skill_*.md (canonical: prose SOP + section anchors)
   +  skill_*.pipeline.yaml (sidecar: per-step declarations)
        │
        │  load  →  Pipeline (validated in 3 stages)
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

Two files describe one skill. The canonical is the single prose source of truth,
the procedure a person reads. The sidecar lifts the machine-readable facts out of
it — each step's role, what it materializes, what it depends on, the schema of its
output. The two are joined by a section id: every step in the sidecar must point
at a matching anchor comment in the canonical, and loading fails if any anchor is
missing. Neither file duplicates the other. The prose stays readable; the
declarations stay checkable.

From there the pieces have clean roles. The compiler produces a typed object. The
scheduler drives that object. The executor is the single unit of work the scheduler
repeats — one step against one input. And the materializer is the only sanctioned
way anything reaches the filesystem. That last constraint is deliberate: if writes
can only happen through one channel, every write is audited by construction.

The unit the pipeline runs against is a *leaf* — one input item, such as one
section of a document to digest. A step is either per-leaf (it runs once per leaf)
or corpus-wide (it runs once over the whole set). Steps chain: a downstream step
reads the accumulated outputs of the steps it depends on. This accumulated context
is the spine of the whole run, and preserving its exact shape is what lets the fast
path stay faithful to the slow one.

## How a run flows

**Compile.** Loading validates the sidecar in three passes — its JSON shape, then
its typed model, then cross-file consistency with the canonical's anchors — and
returns a `Pipeline`, or nothing at all when the skill declares it has no pipeline.
The compiler then walks each step and enforces its contracts. A step names a
materializer; that name must be known, and the step's declared output must promise
at least the fields that materializer requires. It sorts the steps by their
dependencies, rejecting cycles and — pointedly — forward references, since a
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
relevant upstream outputs, and any retry context — into a concrete request; call
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

A single step failing is normal; the executor distinguishes *why*. It keeps two
separate retry budgets — one for logic failures (a bad schema, a contract miss) and
one for crashes (the backend raised, or the watchdog stalled). They are separate on
purpose: an algorithmic defect and a network flake call for different remedies and
must not starve each other. On top of that sits a short-circuit — if the last few
attempts all produced the *same* error, retrying clearly will not help, so it bails
before the budget runs out. Backoff between attempts is opt-in, so the default path
stays byte-identical to a world without it. Each retry feeds the prior error back
into the prompt, so the model gets a chance to correct rather than blindly repeat.

When the dust settles, a step's result is classified into one closed set of
outcomes — succeeded, retries exhausted, watchdog killed, stuck in a same-error
loop, contract violation, or budget exhausted. This discriminated union enforces a
discipline: you can only read a step's produced note when the outcome is *success*;
asking for the artifact of any other outcome is a type error. It becomes structurally
impossible to consume a note that never validated. The ordering of outcomes is
considered too — a contract defect is surfaced ahead of a mere exhausted budget, so
the reported cause is the one a fix loop can actually act on.

Across a whole run, the resume manifest is the crash-safety ledger. Its guiding
principle is that it is never the source of truth — the vault is. The manifest can
always be rebuilt from which notes exist on disk, so a lost or corrupt one is never
fatal; it can be regenerated. It is written atomically, replacing the old file in
one step and rotating a few backups, and on a bad read it falls back to the newest
good backup or starts empty with a warning rather than trusting garbage. Two workers
never own the same leaf, because claiming a leaf is a compare-and-swap that only one
can win, and a worker records a leaf *done* durably before it releases its claim, so
the leaf leaves the claimable set the moment the write lands. (Skipping already-done
leaves on resume is deliberately not wired yet — today a fresh run re-executes every
task, which keeps it identical to the serial path.)

## Gates: the note only counts when it passes

A gate is a named, scoped, pure-program check — never an LLM call. There is exactly
one gate abstraction, reused at the plan, session, and wave scopes; there is no
second mechanism. The close-gate runs after a note is captured and is ordered
cheapest-first: a format check (delegated to Tessellum's own note validator, not
reimplemented) followed by a grounding check. Grounding is the one semantic concern,
but even it stays a program — it *reads* a verdict produced independently by an
agent and decides pass or fail. A missing or auth-blocked verdict fails closed. The
gate never guesses at plausibility, so a fabricated citation cannot slip through by
looking convincing.

The ordering of gate and commit is the load-bearing rule. The note file is written
during capture, but the leaf is only marked done — and the result only treated as
clean — *after* the gate passes. A gate failure turns an otherwise-clean capture
into an errored, blocked result. A note that failed its gate is never silently
recorded as done. The wave-gate adds one check a per-session gate structurally
cannot make: catching two leaves that resolved to the same target path.

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
Before dispatching each task the dynamic scheduler charges one unit against a run
budget, atomically and all-or-nothing; a refused leaf halts with a
budget-exhausted outcome and the backend is never called. Credentials are pooled
alongside: the pool leases the least-used key per call, and when a call fails it
classifies the cause. A hard rate-limit, quota, or auth failure benches that key
for an absolute cooldown that survives a restart and releases the lease so the next
attempt draws a different key; a transient blip keeps the lease. Crucially the pool
holds key *ids*, never secrets — the caller maps id to secret out of band, so this
layer never touches a credential.

Sign-off is the approval ladder from plan to execute, climbed cheapest-first. A
program gate is a pure structural pre-filter that can reject outright; an agent
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
- **The materializer is the only write channel.** Contracts default to demanding a
  tool-free backend so a model cannot smuggle out an undocumented write; one audited
  path or none.
- **Gates are pure programs and fail closed.** The agent gathers evidence; the
  program decides. An unverifiable source is a failure, never a pass, so fabrication
  cannot pass as plausible.
- **The vault is the source of truth, not the manifest.** A lost or half-written
  ledger is regenerated from disk or falls back to a good backup — a resume can
  never be corrupted by manifest state.
- **Composer writes; it does not rank.** Ranking notes is retrieval's job in a
  separate subsystem. Composer's output is always a note on disk.

**Reference:** [reference/composer.md](reference/composer.md) — API, symbols, and signatures.
