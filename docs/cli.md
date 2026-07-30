# Tessellum CLI (`src/tessellum/cli/`)

## The idea

Tessellum is a system in layers: a markdown vault you author, a SQLite index that answers questions about it, and runtimes that reason over it or operate it continuously. The CLI is the single operator surface across all of them. Its governing idea is that it holds no knowledge of its own. Every command is a thin wrapper that parses flags, calls one runtime function, and turns the outcome into an exit code. The intelligence lives in the runtime packages; the CLI only frames the conversation with them.

That discipline is what keeps the system honest. The same runtime that `tessellum search` calls is the one the MCP server exposes and the one the tests exercise. Because behaviour is defined once and merely surfaced many times, no two surfaces can drift apart. The CLI is a lens, not a second implementation.

## The model

```
tessellum <command> [<sub>] [flags]
        │
        └─ main._build_parser()  ── one argparse tree ──▶  args.func(args)
                                                                │
        ┌───────────────────────────────────────────────────────┴───────────┐
        │                                                                    │
   P → P (filesystem)        P → D (index)         D → answers        runtimes
   init, capture,            index build           search, filter,    composer, dks,
   format check,             (vault → SQLite)      fz, bb audit       runtime, mcp serve
   bb migrate                                      (read the DB)      (LLM / service)
```

The whole dispatcher is one convention: an attribute named `func` on the parsed arguments. Each command module contributes an `add_subparser` call that registers its own parser and binds its own handler with `set_defaults(func=...)`. `main` parses, finds `func`, calls it, and returns its integer exit code. There is no registry and no lookup table. A command definition and the code that runs it sit in the same file, and `main.py` stays a flat list of registrations.

The twelve top-level command groups sort naturally by what they touch, and this is the mental map worth keeping. Some commands never leave the filesystem — they scaffold, capture, validate, or rewrite markdown, the write-side of the system. One command, `index build`, is the bridge from the vault to the index. A cluster of read commands — search, filter, and the Folgezettel and Building-Block explorers — only ever read that index back. Three commands are runtimes proper: Composer executes typed pipelines, DKS runs dialectic cycles, and `runtime` owns durable automatic inbox ingestion. The MCP server stands alongside them as a long-lived agent-facing process. This is the CQRS split made visible on the command line: writing and reading are different verbs with different consequences.

Grouped commands nest a second layer of the same trick. `composer`, `index`, `format`, and `runtime` demand a sub-subcommand and let argparse error if it is missing. But `fz`, `bb`, and `mcp` also answer to their bare form — typing `tessellum fz` with no verb reaches a handler that prints its usage and exits. The difference is deliberate: an interactive explorer should tell you your options, whereas a required-leaf group should fail loudly.

## How work flows through it

A first session runs the layers in order. You scaffold a vault with `init`, which copies a seed structure into an empty (or, with `--force`, a non-empty) directory. You author notes with `capture`, each one stamped from a typed template chosen by flavor. You check them with `format check`, which validates YAML frontmatter against the closed-enum spec and, on a directory, recurses over every markdown file while skipping the obvious non-notes like `README.md` and `Rank_*`. Then `index build` reads the whole vault into a single SQLite database — notes, links, full-text, and, unless you pass `--no-dense`, vector embeddings.

Once the index exists, the read commands answer questions against it. `search` is the content surface, and its four strategies are a single mutually-exclusive choice with hybrid as the default: BM25 for lexical matching, dense for semantic similarity, hybrid fusing the two by reciprocal rank, and best-first BFS that walks the link graph outward from a seed note. That last one is the exception worth remembering — its query argument is not free text but a vault-relative note path. `filter`, by contrast, is metadata-only. It answers *what kind* of note you want — a status, a building block, a tag, a date range, a Folgezettel prefix — by filtering columns directly, and all its predicates AND together. The division is clean by design: content lives under `search`, structure under `filter`.

The Folgezettel explorer, `fz`, treats the trail structure as a query rather than a stored artifact. Tessellum keeps only two columns per note — a Folgezettel id and its parent — and derives every path, depth, and trail at query time by walking that parent chain in Python. Its verbs read like the questions you actually ask of a trail: list the trails, show a subtree, trace the ancestors from root to a node, expand its descendants, or print the full path with siblings. The walks are cycle-safe by construction, so a malformed parent link degrades gracefully instead of looping.

The `bb` command reports on the Building-Block graph. Its `audit` verb loads
the corpus graph from the index and tallies node types, epistemic edges,
unrealized schema edges, and unconnected nodes. Its `migrate` verb advances
schema-version stamps on lagging parseable notes. The current check is passive:
`TESS-005` is warning-only and evaluates the recorded schema, not the target,
so `--apply` is not evidence of target-schema conformance.

The three runtimes carry the real weight. `composer` runs a pipeline defined by a single self-contained skill canonical whose step sections each carry a typed contract block: `validate` checks those contract blocks against the spec, `compile` turns them into a typed DAG with zero LLM calls, and `run` executes that DAG against a set of leaves. `batch` runs many such jobs in parallel with resume, `eval` scores scenarios against assertions and an LLM-judge rubric, `scaffold-sidecar` prints starter contract blocks, and `digest` runs the native plan → augment → review → execute flow. `dks` drives the Dialectic Knowledge System — a multi-cycle run over a JSONL of observations, with report, calibration, and schema-mutating meta modes that short-circuit the observation run.

`runtime` turns the native Composer digestion pipeline into an automatic service. Files arrive under one of eight named inbox lanes. Admission first resolves a stable regular file and confines it to the inbox, then copies its bytes into a content-addressed spool before committing an idempotent SQLite job. A supervisor claims one job under a generation-fenced lease, routes the lane to native digestion, executes its plan with heartbeats and cooperative cancellation, validates the output, atomically rebuilds the index unless disabled, and acknowledges the source only after commit. `runtime work` performs one claim; `runtime serve` repeatedly reconciles the inbox and supervises jobs until SIGINT or SIGTERM. Inspection, cancellation, linked retry, and health checks are separate subcommands over the same durable store. A task-manager plane sits over that store too: `status` shows every job's phase, lease, and per-leaf digestion rows (`--watch` to poll, `--job` to drill down), and an inspect-before-execute flow lets a human approve plans — `submit --profile inspect` parks the job paused after review, `plan` prints the accepted plan, `promote`/`reject` approve or discard it (promote only flips durable state; the execute wave still runs under the next worker claim), and `cancel --force` fences out a worker that ignores the cooperative signal. `submit --profile converge` turns on the review-revise loop for that job.

The automatic service deliberately reuses Composer rather than replacing it. Job-level SQLite leases decide which worker owns a source; Composer's manifest still owns leaf-level claim, recovery, and artifact verification inside that job. A reclaimed job can therefore resume verified leaves without repeating their model calls. `mcp serve` exposes deterministic vault APIs plus durable queue-control APIs over stdio, so an agent host can submit and manage work without becoming the worker itself.

## Design decisions and why

**Thin CLI over fat runtime.** Every handler does the same three things: translate flags into one runtime call, map the exceptions that call can raise onto exit codes, and format the result. It reimplements nothing. This is not a stylistic preference but the load-bearing invariant of the whole interface. Because the runtime is the single source of behaviour, the CLI, the MCP tools, and the test suite cannot disagree about what a command means.

**The exit code is a contract where a handler classifies failures.** Zero is success, one is a domain failure, and two is an invocation or supported-configuration failure. Composer, DKS, and MCP map the missing extras they handle to two. Runtime worker setup errors currently propagate, while unavailable PDF ingestion becomes a durable job failure. Automation should use each command's documented mapping rather than assume every exception is normalized.

**Machine-readable output is a contract.** Vault read and telemetry commands offer `--format json` alongside their human view (the `fz` trail explorer is the human-only exception). Durable runtime job commands always emit JSON because their primary consumers are operators, agents, and automation.

**The serial Composer path is the default and stays byte-identical.** `composer run` defaults to the serial reference executor. The wave-parallel dynamic scheduler is strictly opt-in behind `--dynamic`, and every flag that belongs to it — workers, manifest, close-gate, budgets, and the rest — is inert without that switch. The reason is trust: a faster runtime earns adoption only if it cannot silently change the reference semantics. Making the parallel path opt-in guarantees the default answer never moves.

**Compilation and the plan and wave gates never call an LLM.** `compile` produces a typed DAG with zero model calls, and the plan and wave gates that guard the dynamic path are deterministic checks. The close gate's grounding rung consumes a verifier verdict: the default identifier verifier is deterministic and free (`identifier_grounding`, on by default in the runtime policy), while the opt-in B3-calibrated grounding certificate (`grounding_gate` plus a `TESSELLUM_GROUNDING_CALIBRATION` artifact) spends scorer-model calls at gate time — the one deliberate exception to "only execution spends tokens." A note with no grounding verdict fails closed (GROUND-000), never passing by default. Validation and structure stay cheap, repeatable, and free of network flakiness, and keeping the boundary sharp means the parts you run constantly stay fast and offline.

**DKS is a peer runtime, not a Composer subcommand.** The Dialectic Knowledge System reuses Composer's backend abstractions but lives at the top level as `tessellum dks`. It has its own lifecycle and its own mode surface — report, calibrate, meta — that has nothing to do with pipeline execution. Nesting it under `composer` would conflate two independent runtimes.

**Automatic work is durable before it is executable.** `runtime submit` never points a worker directly at mutable inbox bytes. It writes a SHA-256 spool object first and only then admits the job. SQLite state, event history, generation-fenced leases, retry deadlines, and linked manual retries make process crashes and duplicate scans recoverable. The filesystem watcher is only a polling reconciliation loop; correctness does not depend on receiving an edge-triggered event.

**Job control and job execution are separate surfaces.** The `get`, `list`, `status`, `cancel`, `plan`, `promote`, `reject`, and `retry` commands only mutate or inspect the durable queue. They never construct an LLM backend. Conversely, `work` and `serve` are the only runtime commands that execute digestion and therefore the only ones with backend, model, AWS, mock-response, and index-rebuild flags. The same split carries into MCP: its five job tools control the queue but do not run a worker.

**Folgezettel topology is derived, not materialized.** There is no trail view in the schema. Trails are reconstructed in memory each time, because the vaults this targets are small — typically well under a thousand trail notes — and an in-memory walk is simpler and more portable than a recursive SQL query and needs no extra schema to maintain.

**Optional dependencies stay optional.** The MCP SDK, the Anthropic bridge, and the paper and ingest toolchains are all extras. None of them is imported at module load. Each is pulled in lazily at the exact call site that needs it. Handlers that explicitly map `ImportError`, including Composer and MCP commands, return exit two with an install hint; automatic-runtime backend setup errors currently propagate. The base CLI still loads and runs when no extras are installed.

**Reference:** [reference/cli.md](reference/cli.md) — API, symbols, and signatures.
